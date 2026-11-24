// Run: npm test
import test from 'node:test';
import assert from 'node:assert/strict';
import { randomBytes } from 'node:crypto';
import { SqliteStore } from '../src/server/store.ts';
import {
  ReconnectNeeded,
  configFor,
  disconnect,
  finishConnect,
  grandlivreFetch,
  pkceChallenge,
  refreshTokens,
  startConnect,
  type Deps,
} from '../src/server/grandlivre.ts';

const cfg = configFor('https://gl.test', 'client-1', 'http://localhost:4321/grandlivre/callback');

type Call = { url: string; body: URLSearchParams; auth: string | null };
type Handler = (call: Call) => Response;
const json = (status: number, data: unknown) =>
  new Response(JSON.stringify(data), { status, headers: { 'content-type': 'application/json' } });
const tokenAnswer = (n: number) => json(200, { access_token: `AT${n}`, refresh_token: `RT${n}`, expires_in: 3600 });

function setup(handler: Handler = () => json(500, {})) {
  const calls: Call[] = [];
  let time = 1_000_000;
  const store = new SqliteStore(':memory:', randomBytes(32), () => time);
  const fetchFn = (async (input: any, init: any = {}) => {
    const call = {
      url: String(input),
      body: new URLSearchParams(typeof init.body === 'string' ? init.body : ''),
      auth: new Headers(init.headers).get('authorization'),
    };
    calls.push(call);
    return handler(call);
  }) as typeof fetch;
  const deps: Deps = { store, cfg, fetchFn, now: () => time };
  const sid = store.createSession();
  return { deps, store, sid, calls, tick: (ms: number) => (time += ms) };
}
const tokenCalls = (calls: Call[]) => calls.filter((c) => c.url === cfg.tokenEndpoint);

test('authorize URL carries PKCE S256 and state; the code exchange sends the matching verifier', async () => {
  const s = setup(() => tokenAnswer(1));
  const url = new URL(startConnect(s.deps, s.sid, 'ru'));
  assert.equal(url.origin + url.pathname, cfg.authorizationEndpoint);
  assert.equal(url.searchParams.get('response_type'), 'code');
  assert.equal(url.searchParams.get('client_id'), 'client-1');
  assert.equal(url.searchParams.get('redirect_uri'), cfg.redirectUri);
  assert.equal(url.searchParams.get('code_challenge_method'), 'S256');
  const state = url.searchParams.get('state')!;

  const result = await finishConnect(s.deps, s.sid, new URLSearchParams({ code: 'abc', state }));
  assert.deepEqual(result, { ok: true, lang: 'ru' });
  const [call] = s.calls;
  assert.equal(call.url, cfg.tokenEndpoint);
  assert.equal(call.body.get('grant_type'), 'authorization_code');
  assert.equal(call.body.get('code'), 'abc');
  assert.equal(call.body.get('client_id'), 'client-1');
  assert.equal(call.body.get('redirect_uri'), cfg.redirectUri);
  assert.equal(pkceChallenge(call.body.get('code_verifier')!), url.searchParams.get('code_challenge'));
  assert.equal(s.store.status(s.sid), 'connected');
  assert.equal(s.store.getTokens(s.sid)!.refreshToken, 'RT1');
});

test('state check: a wrong or missing state is rejected and no token request is made', async () => {
  for (const params of [{ code: 'abc', state: 'not-ours' }, { code: 'abc' }]) {
    const s = setup(() => tokenAnswer(1));
    startConnect(s.deps, s.sid);
    const result = await finishConnect(s.deps, s.sid, new URLSearchParams(params as Record<string, string>));
    assert.deepEqual(result, { ok: false, lang: 'en', reason: 'state' });
    assert.equal(s.calls.length, 0);
    assert.equal(s.store.status(s.sid), 'none');
  }
});

test('state check: a callback without a started connection is rejected', async () => {
  const s = setup(() => tokenAnswer(1));
  const result = await finishConnect(s.deps, s.sid, new URLSearchParams({ code: 'abc', state: 'x' }));
  assert.equal(result.ok, false);
  assert.equal(s.calls.length, 0);
});

test('state check: a state value works only once', async () => {
  const s = setup(() => tokenAnswer(1));
  const state = new URL(startConnect(s.deps, s.sid)).searchParams.get('state')!;
  assert.equal((await finishConnect(s.deps, s.sid, new URLSearchParams({ code: 'a', state }))).ok, true);
  const again = await finishConnect(s.deps, s.sid, new URLSearchParams({ code: 'b', state }));
  assert.deepEqual(again, { ok: false, lang: 'en', reason: 'state' });
  assert.equal(s.calls.length, 1);
});

test('state check: a state older than 10 minutes is rejected', async () => {
  const s = setup(() => tokenAnswer(1));
  const state = new URL(startConnect(s.deps, s.sid)).searchParams.get('state')!;
  s.tick(11 * 60 * 1000);
  const result = await finishConnect(s.deps, s.sid, new URLSearchParams({ code: 'a', state }));
  assert.equal(result.ok, false);
  assert.equal(s.calls.length, 0);
});

test('denied: error=access_denied shows "not connected" and stops before the token request', async () => {
  const s = setup(() => tokenAnswer(1));
  const state = new URL(startConnect(s.deps, s.sid)).searchParams.get('state')!;
  const result = await finishConnect(s.deps, s.sid, new URLSearchParams({ error: 'access_denied', state }));
  assert.deepEqual(result, { ok: false, lang: 'en', reason: 'denied' });
  assert.equal(s.calls.length, 0);
  assert.equal(s.store.status(s.sid), 'none');
  assert.equal(s.store.getTokens(s.sid), null);
});

test('denied: the state is still checked first when an error is present', async () => {
  const s = setup();
  startConnect(s.deps, s.sid);
  const result = await finishConnect(s.deps, s.sid, new URLSearchParams({ error: 'access_denied', state: 'forged' }));
  assert.deepEqual(result, { ok: false, lang: 'en', reason: 'state' });
});

test('refresh rotation: every refresh sends the newest refresh token and saves the new one', async () => {
  let n = 1;
  const s = setup(() => tokenAnswer(++n));
  s.store.saveTokens(s.sid, { accessToken: 'AT1', refreshToken: 'RT1', expiresAt: 9e15 });

  await refreshTokens(s.deps, s.sid);
  assert.equal(s.calls[0].body.get('grant_type'), 'refresh_token');
  assert.equal(s.calls[0].body.get('refresh_token'), 'RT1');
  assert.equal(s.calls[0].body.get('client_id'), 'client-1');
  assert.equal(s.store.getTokens(s.sid)!.refreshToken, 'RT2');

  await refreshTokens(s.deps, s.sid);
  assert.equal(s.calls[1].body.get('refresh_token'), 'RT2');
  assert.deepEqual(
    { a: s.store.getTokens(s.sid)!.accessToken, r: s.store.getTokens(s.sid)!.refreshToken },
    { a: 'AT3', r: 'RT3' },
  );
});

test('refresh rotation: two refreshes at the same time use the single-use token only once', async () => {
  let n = 1;
  const s = setup(() => tokenAnswer(++n));
  s.store.saveTokens(s.sid, { accessToken: 'AT1', refreshToken: 'RT1', expiresAt: 9e15 });
  const [a, b] = await Promise.all([refreshTokens(s.deps, s.sid), refreshTokens(s.deps, s.sid)]);
  assert.equal(s.calls.length, 1);
  assert.equal(a.refreshToken, 'RT2');
  assert.equal(b.refreshToken, 'RT2');
});

test('401: refresh, then retry once with the new access token', async () => {
  const s = setup((call) => {
    if (call.url === cfg.tokenEndpoint) return tokenAnswer(2);
    return call.auth === 'Bearer AT2' ? json(200, { ok: true }) : json(401, {});
  });
  s.store.saveTokens(s.sid, { accessToken: 'AT1', refreshToken: 'RT1', expiresAt: 9e15 });
  const res = await grandlivreFetch(s.deps, s.sid, '/api/v1/pay-links');
  assert.equal(res.status, 200);
  assert.deepEqual(s.calls.map((c) => c.auth), ['Bearer AT1', null, 'Bearer AT2']);
  assert.equal(s.store.getTokens(s.sid)!.refreshToken, 'RT2');
});

test('401: when the refresh is refused the session needs "reconnect Grandlivre"', async () => {
  const s = setup((call) => (call.url === cfg.tokenEndpoint ? json(400, { error: 'invalid_grant' }) : json(401, {})));
  s.store.saveTokens(s.sid, { accessToken: 'AT1', refreshToken: 'RT1', expiresAt: 9e15 });
  await assert.rejects(grandlivreFetch(s.deps, s.sid, '/api/v1/pay-links'), ReconnectNeeded);
  assert.equal(s.store.status(s.sid), 'reconnect');
  assert.equal(s.store.getTokens(s.sid), null);
});

test('401: when the retry also gets 401 it stops after one retry', async () => {
  const s = setup((call) => (call.url === cfg.tokenEndpoint ? tokenAnswer(2) : json(401, {})));
  s.store.saveTokens(s.sid, { accessToken: 'AT1', refreshToken: 'RT1', expiresAt: 9e15 });
  await assert.rejects(grandlivreFetch(s.deps, s.sid, '/api/v1/pay-links'), ReconnectNeeded);
  assert.equal(s.calls.length, 3);
  assert.equal(s.store.status(s.sid), 'reconnect');
});

test('a server error on refresh keeps the tokens (the connection is not lost)', async () => {
  const s = setup(() => json(503, {}));
  s.store.saveTokens(s.sid, { accessToken: 'AT1', refreshToken: 'RT1', expiresAt: 9e15 });
  await assert.rejects(refreshTokens(s.deps, s.sid), /503/);
  assert.equal(s.store.getTokens(s.sid)!.refreshToken, 'RT1');
  assert.equal(s.store.status(s.sid), 'connected');
});

test('an expired access token is refreshed before the call', async () => {
  const s = setup((call) => (call.url === cfg.tokenEndpoint ? tokenAnswer(2) : json(200, {})));
  s.store.saveTokens(s.sid, { accessToken: 'AT1', refreshToken: 'RT1', expiresAt: 0 });
  await grandlivreFetch(s.deps, s.sid, '/api/v1/notices');
  assert.deepEqual(s.calls.map((c) => c.auth), [null, 'Bearer AT2']);
});

test('the access token is never sent to another host', async () => {
  const s = setup(() => json(200, {}));
  s.store.saveTokens(s.sid, { accessToken: 'AT1', refreshToken: 'RT1', expiresAt: 9e15 });
  await assert.rejects(grandlivreFetch(s.deps, s.sid, 'https://evil.test/steal'), /only calls Grandlivre/);
  assert.equal(s.calls.length, 0);
});

test('disconnect forgets the tokens', () => {
  const s = setup();
  s.store.saveTokens(s.sid, { accessToken: 'AT1', refreshToken: 'RT1', expiresAt: 9e15 });
  disconnect(s.deps, s.sid);
  assert.equal(s.store.getTokens(s.sid), null);
  assert.equal(s.store.status(s.sid), 'none');
});

test('storage: tokens, verifier and session id are not readable in the database', () => {
  const s = setup();
  startConnect(s.deps, s.sid);
  s.store.saveTokens(s.sid, { accessToken: 'ACCESS-SECRET', refreshToken: 'REFRESH-SECRET', expiresAt: 9e15 });
  const raw = JSON.stringify((s.store as SqliteStore).db.prepare('SELECT * FROM sessions').all());
  assert.ok(!raw.includes('ACCESS-SECRET') && !raw.includes('REFRESH-SECRET') && !raw.includes(s.sid));
  assert.ok(!raw.includes('verifier'));
  assert.equal(s.store.getTokens(s.sid)!.accessToken, 'ACCESS-SECRET');
  assert.equal(s.store.hasSession('someone-else'), false);
});
