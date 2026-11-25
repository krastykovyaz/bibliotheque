// Marks videos as "made for kids" on YouTube (needs the youtube scope: the same sign-in as youtube-set-description.mjs).
//   node scripts/youtube-made-for-kids.mjs <video id> [<video id> ...]          sets selfDeclaredMadeForKids = true
//   node scripts/youtube-made-for-kids.mjs --check <video id> [...]            only shows the current setting
// Note: YouTube then switches off comments, personalised ads and notifications for those videos; that is its rule for kids' content.
import fs from 'node:fs';
const check = process.argv.includes('--check');
const ids = process.argv.slice(2).filter((a) => a !== '--check');
if (!ids.length) { console.error('usage: node scripts/youtube-made-for-kids.mjs [--check] <video id> ...'); process.exit(1); }
const c = JSON.parse(fs.readFileSync(process.env.YOUTUBE_CLIENT_FILE || '.data/youtube-client.json', 'utf8'));
const client = c.installed || c.web || c;
const t = JSON.parse(fs.readFileSync(process.env.YOUTUBE_TOKEN_FILE || '.data/youtube-token.json', 'utf8'));
const tok = await (await fetch('https://oauth2.googleapis.com/token', { method: 'POST', headers: { 'content-type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({ grant_type: 'refresh_token', refresh_token: t.refresh_token, client_id: client.client_id, client_secret: client.client_secret || '' }) })).json();
if (!tok.access_token) { console.error('sign-in failed:', tok.error_description || tok.error); process.exit(1); }
const auth = { authorization: 'Bearer ' + tok.access_token };
for (const id of ids) {
  const got = await (await fetch(`https://www.googleapis.com/youtube/v3/videos?part=status&id=${id}`, { headers: auth })).json();
  const st = got.items?.[0]?.status;
  if (!st) { console.log(id, 'video not found'); continue; }
  console.log(id, 'madeForKids:', st.madeForKids, '| selfDeclared:', st.selfDeclaredMadeForKids);
  if (check || st.selfDeclaredMadeForKids === true) continue;
  const body = { id, status: { privacyStatus: st.privacyStatus, embeddable: st.embeddable, license: st.license, publicStatsViewable: st.publicStatsViewable, selfDeclaredMadeForKids: true,
    ...(st.containsSyntheticMedia !== undefined ? { containsSyntheticMedia: st.containsSyntheticMedia } : {}) } };
  const u = await fetch('https://www.googleapis.com/youtube/v3/videos?part=status', { method: 'PUT', headers: { ...auth, 'content-type': 'application/json' }, body: JSON.stringify(body) });
  console.log(id, u.ok ? 'marked as made for kids' : `failed (${u.status}): ${(await u.text()).slice(0, 300)}`);
}
