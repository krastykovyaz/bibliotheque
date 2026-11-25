// Creates a YouTube playlist (to be used as a podcast: open it in YouTube Studio > Content > Playlists and mark it as a podcast).
//   node scripts/youtube-create-playlist.mjs "<title>" "<description>" [public|unlisted|private]
// The sign-in needs the youtube scope (sign in with --playlists). Prints the playlist id.
import fs from 'node:fs';
const [title, description = '', privacy = 'public'] = process.argv.slice(2);
if (!title) { console.error('usage: node scripts/youtube-create-playlist.mjs "<title>" "<description>" [public|unlisted|private]'); process.exit(1); }
const c = JSON.parse(fs.readFileSync(process.env.YOUTUBE_CLIENT_FILE || '.data/youtube-client.json', 'utf8'));
const client = c.installed || c.web || c;
const t = JSON.parse(fs.readFileSync(process.env.YOUTUBE_TOKEN_FILE || '.data/youtube-token.json', 'utf8'));
const r = await fetch('https://oauth2.googleapis.com/token', { method: 'POST', headers: { 'content-type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({ grant_type: 'refresh_token', refresh_token: t.refresh_token, client_id: client.client_id, client_secret: client.client_secret || '' }) });
const tok = await r.json();
if (!tok.access_token) { console.error('sign-in failed:', tok.error_description || tok.error); process.exit(1); }
const res = await fetch('https://www.googleapis.com/youtube/v3/playlists?part=snippet,status', { method: 'POST',
  headers: { authorization: 'Bearer ' + tok.access_token, 'content-type': 'application/json' },
  body: JSON.stringify({ snippet: { title, description, defaultLanguage: 'en' }, status: { privacyStatus: privacy } }) });
const j = await res.json();
if (!res.ok) { console.error('failed:', JSON.stringify(j).slice(0, 400)); process.exit(1); }
console.log('playlist id:', j.id);
console.log('https://www.youtube.com/playlist?list=' + j.id);
