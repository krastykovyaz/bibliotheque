// Server-side storage for anonymous sessions and their Grandlivre tokens.
// Tokens are encrypted before they are written. Session ids are stored hashed.
import { createHash, randomBytes } from 'node:crypto';
import { DatabaseSync } from 'node:sqlite';
import { decrypt, encrypt } from './crypto.ts';

export interface TokenSet {
  accessToken: string;
  refreshToken: string;
  /** Unix time in ms when the access token stops being valid. */
  expiresAt: number;
}
export interface Pending {
  state: string;
  verifier: string;
  lang: string;
}
export type Status = 'none' | 'connected' | 'reconnect';

export interface Store {
  /** Creates a session and returns its id (the cookie value). */
  createSession(): string;
  hasSession(sid: string): boolean;
  setPending(sid: string, pending: Pending): void;
  /** Returns the pending authorization and clears it, so a state value works only once. */
  takePending(sid: string): Pending | null;
  saveTokens(sid: string, tokens: TokenSet): void;
  getTokens(sid: string): TokenSet | null;
  /** Forgets the tokens. With reconnect = true the session is marked "reconnect Grandlivre". */
  deleteTokens(sid: string, reconnect?: boolean): void;
  status(sid: string): Status;
}

const PENDING_TTL_MS = 10 * 60 * 1000;
const hash = (sid: string) => createHash('sha256').update(sid).digest('hex');
const newSid = () => randomBytes(32).toString('base64url');

export class SqliteStore implements Store {
  db: DatabaseSync;
  key: Buffer;
  now: () => number;

  constructor(file: string, key: Buffer, now: () => number = Date.now) {
    this.db = new DatabaseSync(file);
    this.key = key;
    this.now = now;
    this.db.exec(`CREATE TABLE IF NOT EXISTS sessions (
      id TEXT PRIMARY KEY,
      created_at INTEGER NOT NULL,
      pending TEXT,
      pending_at INTEGER,
      tokens TEXT,
      reconnect INTEGER NOT NULL DEFAULT 0
    )`);
  }

  createSession() {
    const sid = newSid();
    this.db.prepare('INSERT INTO sessions (id, created_at) VALUES (?, ?)').run(hash(sid), this.now());
    return sid;
  }
  hasSession(sid: string) {
    return !!this.db.prepare('SELECT 1 FROM sessions WHERE id = ?').get(hash(sid));
  }
  setPending(sid: string, pending: Pending) {
    this.db
      .prepare('UPDATE sessions SET pending = ?, pending_at = ? WHERE id = ?')
      .run(encrypt(this.key, JSON.stringify(pending)), this.now(), hash(sid));
  }
  takePending(sid: string) {
    const row = this.db.prepare('SELECT pending, pending_at FROM sessions WHERE id = ?').get(hash(sid)) as
      | { pending: string | null; pending_at: number | null }
      | undefined;
    this.db.prepare('UPDATE sessions SET pending = NULL, pending_at = NULL WHERE id = ?').run(hash(sid));
    if (!row?.pending || !row.pending_at || this.now() - row.pending_at > PENDING_TTL_MS) return null;
    return JSON.parse(decrypt(this.key, row.pending)) as Pending;
  }
  saveTokens(sid: string, tokens: TokenSet) {
    this.db
      .prepare('UPDATE sessions SET tokens = ?, reconnect = 0 WHERE id = ?')
      .run(encrypt(this.key, JSON.stringify(tokens)), hash(sid));
  }
  getTokens(sid: string) {
    const row = this.db.prepare('SELECT tokens FROM sessions WHERE id = ?').get(hash(sid)) as
      | { tokens: string | null }
      | undefined;
    return row?.tokens ? (JSON.parse(decrypt(this.key, row.tokens)) as TokenSet) : null;
  }
  deleteTokens(sid: string, reconnect = false) {
    this.db.prepare('UPDATE sessions SET tokens = NULL, reconnect = ? WHERE id = ?').run(reconnect ? 1 : 0, hash(sid));
  }
  status(sid: string): Status {
    const row = this.db.prepare('SELECT tokens, reconnect FROM sessions WHERE id = ?').get(hash(sid)) as
      | { tokens: string | null; reconnect: number }
      | undefined;
    if (!row) return 'none';
    return row.tokens ? 'connected' : row.reconnect ? 'reconnect' : 'none';
  }
}
