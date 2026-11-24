// Adds a line to the description of a video that is already on YouTube (the sign-in needs the youtube scope: --playlists).
//   node scripts/youtube-set-description.mjs <video id> "<line to add above the hashtags>"
//   node scripts/youtube-set-description.mjs <video id> --remove "<paragraph to remove>"
import fs from 'node:fs';
const remove = process.argv.includes('--remove');
const [id, line] = process.argv.slice(2).filter((a) => a !== '--remove');
if (!id || !line) { console.error('usage: node scripts/youtube-set-description.mjs <video id> "<line>"'); process.exit(1); }
const c = JSON.parse(fs.readFileSync(process.env.YOUTUBE_CLIENT_FILE || '.data/youtube-client.json', 'utf8'));
const client = c.installed || c.web || c;
const tf = process.env.YOUTUBE_TOKEN_FILE || '.data/youtube-token.json';
const t = JSON.parse(fs.readFileSync(tf, 'utf8'));
const r = await fetch('https://oauth2.googleapis.com/token', { method: 'POST', headers: { 'content-type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({ grant_type: 'refresh_token', refresh_token: t.refresh_token, client_id: client.client_id, client_secret: client.client_secret || '' }) });
const tok = await r.json();
if (!tok.access_token) { console.error('sign-in failed:', tok.error_description || tok.error); process.exit(1); }
const auth = { authorization: 'Bearer ' + tok.access_token };
const got = await (await fetch(`https://www.googleapis.com/youtube/v3/videos?part=snippet&id=${id}`, { headers: auth })).json();
const sn = got.items?.[0]?.snippet;
if (!sn) { console.error('video not found:', JSON.stringify(got).slice(0, 300)); process.exit(1); }
if (remove) {
  if (!sn.description.includes(line)) { console.log('nothing to remove'); process.exit(0); }
  const d2 = sn.description.replace(line, '').replace(/\n{3,}/g, '\n\n');
  const u2 = await fetch('https://www.googleapis.com/youtube/v3/videos?part=snippet', { method: 'PUT', headers: { ...auth, 'content-type': 'application/json' },
    body: JSON.stringify({ id, snippet: { title: sn.title, description: d2, categoryId: sn.categoryId, tags: sn.tags, defaultLanguage: sn.defaultLanguage } }) });
  console.log(u2.ok ? 'description updated' : `failed (${u2.status}): ${(await u2.text()).slice(0, 400)}`);
  process.exit(0);
}
if (sn.description.includes(line)) { console.log('already there'); process.exit(0); }
const marker = sn.description.indexOf('\n\n#');
const desc = marker > 0 ? sn.description.slice(0, marker) + '\n\n' + line + sn.description.slice(marker) : sn.description + '\n\n' + line;
const up = await fetch('https://www.googleapis.com/youtube/v3/videos?part=snippet', { method: 'PUT', headers: { ...auth, 'content-type': 'application/json' },
  body: JSON.stringify({ id, snippet: { title: sn.title, description: desc, categoryId: sn.categoryId, tags: sn.tags, defaultLanguage: sn.defaultLanguage } }) });
console.log(up.ok ? 'description updated' : `failed (${up.status}): ${(await up.text()).slice(0, 400)}`);
