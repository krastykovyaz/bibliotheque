// Sets the cover picture of a YouTube playlist (the "hero" image, the same square cover a podcast shows).
//   node scripts/youtube-playlist-image.mjs <playlist id> <image.png|jpg>   (16:9, for example 1280x720: the playlist tile crops a square picture to a wide band; replaces an existing cover)
// A playlist can have one such image; if it already has one the API answers "already exists".
import fs from 'node:fs';
const [pl, img] = process.argv.slice(2);
if (!pl || !img) { console.error('usage: node scripts/youtube-playlist-image.mjs <playlist id> <image>'); process.exit(1); }
const c = JSON.parse(fs.readFileSync(process.env.YOUTUBE_CLIENT_FILE || '.data/youtube-client.json', 'utf8')); const cl = c.installed || c.web || c;
const t = JSON.parse(fs.readFileSync(process.env.YOUTUBE_TOKEN_FILE || '.data/youtube-token.json', 'utf8'));
const r = await (await fetch('https://oauth2.googleapis.com/token', { method: 'POST', headers: { 'content-type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({ grant_type: 'refresh_token', refresh_token: t.refresh_token, client_id: cl.client_id, client_secret: cl.client_secret || '' }) })).json();
if (!r.access_token) { console.error('sign-in failed'); process.exit(1); }
// replace an existing cover: delete the old one first
const list = await (await fetch('https://www.googleapis.com/youtube/v3/playlistImages?part=snippet&parent=' + pl, { headers: { authorization: 'Bearer ' + r.access_token } })).json();
for (const it of list.items || []) await fetch('https://www.googleapis.com/youtube/v3/playlistImages?id=' + encodeURIComponent(it.id), { method: 'DELETE', headers: { authorization: 'Bearer ' + r.access_token } });
const mime = img.toLowerCase().endsWith('.png') ? 'image/png' : 'image/jpeg';
const b = 'xxBOUNDARYxx';
const body = Buffer.concat([Buffer.from(`--${b}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n${JSON.stringify({ snippet: { playlistId: pl, type: 'hero' } })}\r\n--${b}\r\nContent-Type: ${mime}\r\n\r\n`), fs.readFileSync(img), Buffer.from(`\r\n--${b}--`)]);
const res = await fetch('https://www.googleapis.com/upload/youtube/v3/playlistImages?part=snippet&uploadType=multipart', { method: 'POST', headers: { authorization: 'Bearer ' + r.access_token, 'content-type': `multipart/related; boundary=${b}` }, body });
const txt = await res.text();
console.log(res.ok ? 'cover set for ' + pl : `failed (${res.status}): ${txt.slice(0, 300)}`);
process.exit(res.ok ? 0 : 1);
