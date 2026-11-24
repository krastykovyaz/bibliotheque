// Registers this app with Grandlivre ONCE and writes the result to .env.
// Run: node scripts/grandlivre-register.mjs [redirect_uri]
// It refuses to run again while GRANDLIVRE_CLIENT_ID is already in .env.
import fs from 'node:fs';
import { randomBytes } from 'node:crypto';

const ISSUER = 'https://app.portemonnaie.space';
const redirectUri = process.argv[2] || 'http://localhost:4321/grandlivre/callback';
const envFile = '.env';
const env = fs.existsSync(envFile) ? fs.readFileSync(envFile, 'utf8') : '';
if (/^GRANDLIVRE_CLIENT_ID=.+/m.test(env)) {
  console.error('GRANDLIVRE_CLIENT_ID is already set in .env. Remove it first if you really want a new registration.');
  process.exit(1);
}
const meta = await (await fetch(`${ISSUER}/.well-known/oauth-authorization-server`)).json();
const res = await fetch(meta.registration_endpoint, {
  method: 'POST',
  headers: { 'content-type': 'application/json' },
  body: JSON.stringify({ client_name: 'Bibliothèque', redirect_uris: [redirectUri] }),
});
const body = await res.json().catch(() => ({}));
if (!res.ok || !body.client_id) {
  console.error(`Registration failed (${res.status}):`, body.error || body);
  process.exit(1);
}
let out = env && !env.endsWith('\n') ? env + '\n' : env;
out += `GRANDLIVRE_CLIENT_ID=${body.client_id}\nGRANDLIVRE_REDIRECT_URI=${redirectUri}\n`;
if (!/^GRANDLIVRE_TOKEN_KEY=.+/m.test(env)) out += `GRANDLIVRE_TOKEN_KEY=${randomBytes(32).toString('base64')}\n`;
fs.writeFileSync(envFile, out, { mode: 0o600 });
console.log(`Registered. client_id ${body.client_id} saved to .env (redirect ${redirectUri}).`);
