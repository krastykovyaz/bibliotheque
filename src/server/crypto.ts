// AES-256-GCM encryption for tokens at rest.
import { createCipheriv, createDecipheriv, randomBytes } from 'node:crypto';

/** Parses a 32-byte key given as base64 (GRANDLIVRE_TOKEN_KEY). */
export function parseKey(base64: string): Buffer {
  const key = Buffer.from(base64, 'base64');
  if (key.length !== 32) throw new Error('GRANDLIVRE_TOKEN_KEY must be 32 bytes, base64-encoded');
  return key;
}

export function encrypt(key: Buffer, plain: string): string {
  const iv = randomBytes(12);
  const cipher = createCipheriv('aes-256-gcm', key, iv);
  const data = Buffer.concat([cipher.update(plain, 'utf8'), cipher.final()]);
  return 'v1.' + Buffer.concat([iv, cipher.getAuthTag(), data]).toString('base64');
}

export function decrypt(key: Buffer, boxed: string): string {
  if (!boxed.startsWith('v1.')) throw new Error('unknown ciphertext format');
  const raw = Buffer.from(boxed.slice(3), 'base64');
  const decipher = createDecipheriv('aes-256-gcm', key, raw.subarray(0, 12));
  decipher.setAuthTag(raw.subarray(12, 28));
  return Buffer.concat([decipher.update(raw.subarray(28)), decipher.final()]).toString('utf8');
}
