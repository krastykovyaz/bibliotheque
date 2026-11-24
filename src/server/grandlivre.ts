// Grandlivre connection: OAuth 2.1 authorization-code flow with PKCE (S256), public client.
// This module has no framework code, so it can be tested with a fake fetch and an in-memory store.
// Tokens are never logged and never sent to the browser.
import { createHash, randomBytes, timingSafeEqual } from 'node:crypto';
import type { Store, TokenSet } from './store.ts';

export interface GrandlivreConfig {
  issuer: string;
  authorizationEndpoint: string;
  tokenEndpoint: string;
  clientId: string;
  redirectUri: string;
}
export interface Deps {
  store: Store;
  cfg: GrandlivreConfig;
  fetchFn?: typeof fetch;
  now?: () => number;
}

/** The connection is gone and the user has to connect again ("reconnect Grandlivre"). */
export class ReconnectNeeded extends Error {
  constructor() {
    super('reconnect Grandlivre');
    this.name = 'ReconnectNeeded';
  }
}

export const configFor = (issuer: string, clientId: string, redirectUri: string): GrandlivreConfig => ({
  issuer,
  authorizationEndpoint: `${issuer}/oauth/authorize`,
  tokenEndpoint: `${issuer}/oauth/token`,
  clientId,
  redirectUri,
});

export const pkceChallenge = (verifier: string) => createHash('sha256').update(verifier).digest('base64url');

const same = (a: string, b: string) => {
  const x = Buffer.from(a);
  const y = Buffer.from(b);
  return x.length === y.length && timingSafeEqual(x, y);
};

/** Step 1: remember a fresh verifier and state in the session, return the URL to send the browser to. */
export function startConnect({ store, cfg }: Deps, sid: string, lang = 'en'): string {
  const verifier = randomBytes(48).toString('base64url');
  const state = randomBytes(24).toString('base64url');
  store.setPending(sid, { state, verifier, lang });
  const url = new URL(cfg.authorizationEndpoint);
  url.search = new URLSearchParams({
    response_type: 'code',
    client_id: cfg.clientId,
    redirect_uri: cfg.redirectUri,
    code_challenge: pkceChallenge(verifier),
    code_challenge_method: 'S256',
    state,
  }).toString();
  return url.href;
}

export type ConnectResult =
  | { ok: true; lang: string }
  | { ok: false; lang: string; reason: 'state' | 'denied' | 'error' };

/** Step 2: the callback. Checks state first, then the denied case, then exchanges the code. */
export async function finishConnect(deps: Deps, sid: string, params: URLSearchParams): Promise<ConnectResult> {
  const { store, cfg } = deps;
  const pending = store.takePending(sid);
  const lang = pending?.lang ?? 'en';
  const state = params.get('state');
  if (!pending || !state || !same(state, pending.state)) return { ok: false, lang, reason: 'state' };
  const iss = params.get('iss');
  if (iss && iss !== cfg.issuer) return { ok: false, lang, reason: 'state' };
  const error = params.get('error');
  if (error) return { ok: false, lang, reason: error === 'access_denied' ? 'denied' : 'error' };
  const code = params.get('code');
  if (!code) return { ok: false, lang, reason: 'error' };

  const answer = await tokenRequest(deps, {
    grant_type: 'authorization_code',
    code,
    code_verifier: pending.verifier,
    client_id: cfg.clientId,
    redirect_uri: cfg.redirectUri,
  }).catch(() => null);
  if (!answer?.tokens) return { ok: false, lang, reason: 'error' };
  store.saveTokens(sid, answer.tokens);
  return { ok: true, lang };
}

/** Disconnect = forget the tokens on our side. */
export function disconnect({ store }: Deps, sid: string) {
  store.deleteTokens(sid);
}

async function tokenRequest(deps: Deps, body: Record<string, string>, oldRefresh?: string) {
  const res = await (deps.fetchFn ?? fetch)(deps.cfg.tokenEndpoint, {
    method: 'POST',
    headers: { 'content-type': 'application/x-www-form-urlencoded', accept: 'application/json' },
    body: new URLSearchParams(body).toString(),
  });
  if (!res.ok) return { status: res.status, tokens: null };
  const json = (await res.json()) as Record<string, unknown>;
  const refreshToken = typeof json.refresh_token === 'string' ? json.refresh_token : oldRefresh;
  if (typeof json.access_token !== 'string' || !refreshToken) return { status: res.status, tokens: null };
  const seconds = typeof json.expires_in === 'number' ? json.expires_in : 3600;
  const tokens: TokenSet = {
    accessToken: json.access_token,
    refreshToken,
    expiresAt: (deps.now ?? Date.now)() + seconds * 1000,
  };
  return { status: res.status, tokens };
}

// The refresh token is single-use, so two refreshes for one session must never run at the same time.
const refreshing = new Map<string, Promise<TokenSet>>();

/** Renews the tokens and ALWAYS saves the new refresh token before returning. */
export function refreshTokens(deps: Deps, sid: string): Promise<TokenSet> {
  let run = refreshing.get(sid);
  if (!run) {
    run = doRefresh(deps, sid).finally(() => refreshing.delete(sid));
    refreshing.set(sid, run);
  }
  return run;
}

async function doRefresh(deps: Deps, sid: string): Promise<TokenSet> {
  const current = deps.store.getTokens(sid);
  if (!current) throw new ReconnectNeeded();
  const answer = await tokenRequest(
    deps,
    { grant_type: 'refresh_token', refresh_token: current.refreshToken, client_id: deps.cfg.clientId },
    current.refreshToken,
  );
  if (answer.tokens) {
    deps.store.saveTokens(sid, answer.tokens);
    return answer.tokens;
  }
  if (answer.status >= 400 && answer.status < 500) {
    // Grandlivre refused the refresh token: the connection is lost.
    deps.store.deleteTokens(sid, true);
    throw new ReconnectNeeded();
  }
  throw new Error(`Grandlivre token endpoint answered ${answer.status}`);
}

/**
 * Calls the Grandlivre API for this session with "Authorization: Bearer <token>".
 * On 401: refresh, then retry once. If that fails, throws ReconnectNeeded.
 */
export async function grandlivreFetch(deps: Deps, sid: string, path: string, init: RequestInit = {}): Promise<Response> {
  const url = new URL(path, deps.cfg.issuer);
  if (url.origin !== new URL(deps.cfg.issuer).origin) throw new Error('grandlivreFetch only calls Grandlivre');
  const call = (t: TokenSet) => {
    const headers = new Headers(init.headers);
    headers.set('authorization', `Bearer ${t.accessToken}`);
    return (deps.fetchFn ?? fetch)(url, { ...init, headers });
  };
  let tokens = deps.store.getTokens(sid);
  if (!tokens) throw new ReconnectNeeded();
  if (tokens.expiresAt - (deps.now ?? Date.now)() < 30_000) tokens = await refreshTokens(deps, sid);
  let res = await call(tokens);
  if (res.status === 401) {
    tokens = await refreshTokens(deps, sid);
    res = await call(tokens);
    if (res.status === 401) {
      deps.store.deleteTokens(sid, true);
      throw new ReconnectNeeded();
    }
  }
  return res;
}
