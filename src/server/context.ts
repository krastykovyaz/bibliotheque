// Wires the Grandlivre module to this server: config from the environment, the SQLite store, the session cookie.
import fs from 'node:fs';
import path from 'node:path';
import type { AstroCookies } from 'astro';
import { parseKey } from './crypto.ts';
import { configFor, type Deps } from './grandlivre.ts';
import { SqliteStore } from './store.ts';

export const SID_COOKIE = 'bib_sid';
const ISSUER = 'https://app.portemonnaie.space';

const g = globalThis as { __bibDeps?: Deps | null };

/** Returns null when Grandlivre is not configured (no client id or no token key). */
export function getDeps(): Deps | null {
  if (g.__bibDeps !== undefined) return g.__bibDeps;
  if (!process.env.GRANDLIVRE_CLIENT_ID) {
    try {
      process.loadEnvFile();
    } catch {
      /* no .env file */
    }
  }
  const { GRANDLIVRE_CLIENT_ID: clientId, GRANDLIVRE_REDIRECT_URI: redirectUri, GRANDLIVRE_TOKEN_KEY: key } = process.env;
  if (!clientId || !redirectUri || !key) return (g.__bibDeps = null);
  const file = process.env.DATABASE_PATH || '.data/bibliotheque.sqlite';
  fs.mkdirSync(path.dirname(file), { recursive: true, mode: 0o700 });
  return (g.__bibDeps = {
    store: new SqliteStore(file, parseKey(key)),
    cfg: configFor(ISSUER, clientId, redirectUri),
  });
}

/** The session id from the cookie, if it is one of ours. */
export function readSid(cookies: AstroCookies, deps: Deps): string | null {
  const sid = cookies.get(SID_COOKIE)?.value;
  return sid && deps.store.hasSession(sid) ? sid : null;
}

export function setSid(cookies: AstroCookies, sid: string, url: URL) {
  cookies.set(SID_COOKIE, sid, {
    httpOnly: true,
    sameSite: 'lax',
    secure: url.protocol === 'https:',
    path: '/',
    maxAge: 60 * 60 * 24 * 180,
  });
}
