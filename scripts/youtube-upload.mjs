#!/usr/bin/env node
// Uploads an audiobook video to YouTube with the YouTube Data API (resumable upload).
// Title and description come from data/books.json, so the video matches the site.
//
//   node scripts/youtube-upload.mjs <video.mp4> --book <id> --lang <code> [options]    metadata from data/books.json
//   node scripts/youtube-upload.mjs <video.mp4> --package <file> [--lang en] [options]  metadata from a package file
//   node scripts/youtube-upload.mjs --auth-only [--playlists]                            sign in only (on a computer with a browser)
//   add  --playlist <id>  to put the new video into a playlist or podcast (the sign-in must then include --playlists)
//
// A package file has sections TITLE, DESCRIPTION and TAGS (see production/how-much-land/How_Much_Land_youtube_description.txt).
// Where the login lives: YOUTUBE_CLIENT_FILE and YOUTUBE_TOKEN_FILE (defaults: .data/youtube-client.json, .data/youtube-token.json).
// On a server without a browser: sign in with --auth-only on your own computer and copy the token file to the server.
//
//   --privacy private|unlisted|public   default: private (projects that Google has not
//                                       audited can only upload private videos)
//   --thumbnail <image.png>             optional, needs a phone-verified channel
//   --dry-run                           print what would be sent, call nothing
//
// One-time setup is in README.md ("Upload videos to YouTube"). Nothing here runs by itself.
import fs from 'node:fs';
import http from 'node:http';
import crypto from 'node:crypto';
import path from 'node:path';
import { execFile } from 'node:child_process';

const DATA_DIR = '.data';
const CLIENT_FILE = process.env.YOUTUBE_CLIENT_FILE || path.join(DATA_DIR, 'youtube-client.json');
const TOKEN_FILE = process.env.YOUTUBE_TOKEN_FILE || path.join(DATA_DIR, 'youtube-token.json');
const CHUNK = 8 * 1024 * 1024; // must be a multiple of 256 KiB

// ---------- arguments ----------
const args = process.argv.slice(2);
// Uploading needs only youtube.upload. Adding a video to a playlist needs the wider youtube scope, asked for only with --playlists.
const SCOPE = 'https://www.googleapis.com/auth/youtube.upload' + (args.includes('--playlists') ? ' https://www.googleapis.com/auth/youtube' : '');
const flag = (name) => {
  const i = args.indexOf('--' + name);
  return i === -1 ? undefined : args[i + 1];
};
const BOOLEAN = ['--dry-run', '--auth-only', '--playlists'];
const file = args.find((a, i) => !a.startsWith('--') && !(i > 0 && args[i - 1].startsWith('--') && !BOOLEAN.includes(args[i - 1])));
const bookId = flag('book');
const lang = flag('lang') ?? (flag('package') ? 'en' : undefined);
const packageFile = flag('package');
const authOnly = args.includes('--auth-only');
const privacy = flag('privacy') ?? 'private';
const thumbnail = flag('thumbnail');
const playlist = flag('playlist');
const dryRun = args.includes('--dry-run');

const die = (msg) => {
  console.error('Error: ' + msg);
  process.exit(1);
};
if (authOnly) {
  await accessToken();
  console.log('Signed in. The login is saved in ' + TOKEN_FILE);
  process.exit(0);
}
if (!file || !(packageFile || (bookId && lang))) die('usage: node scripts/youtube-upload.mjs <video.mp4> (--book <id> --lang <code> | --package <file>) [--privacy private|unlisted|public] [--thumbnail image.png] [--dry-run]   or   --auth-only');
if (!['private', 'unlisted', 'public'].includes(privacy)) die('--privacy must be private, unlisted or public');
if (!fs.existsSync(file)) die(`video not found: ${file}`);
if (thumbnail && !fs.existsSync(thumbnail)) die(`thumbnail not found: ${thumbnail}`);
if (packageFile && !fs.existsSync(packageFile)) die(`package file not found: ${packageFile}`);

// ---------- metadata: from a package file, or from data/books.json ----------
const aiNote = (code) =>
  code === 'ru'
    ? 'Произведение находится в общественном достоянии. Перевод и озвучка сделаны с помощью ИИ.'
    : 'The text is in the public domain. The translation and the voices are made with AI.';
let metadata;
if (packageFile) {
  // sections are lines in capitals: TITLE, DESCRIPTION, TAGS, ...
  const parts = fs.readFileSync(packageFile, 'utf8').split(/^([A-Z][A-Z ]+)\r?\n/m);
  const section = {};
  for (let i = 1; i < parts.length; i += 2) section[parts[i].trim()] = parts[i + 1].trim();
  if (!section.TITLE || !section.DESCRIPTION) die(`${packageFile} needs TITLE and DESCRIPTION sections`);
  const tags = (section.TAGS ?? '').split(',').map((t) => t.trim()).filter(Boolean);
  metadata = {
    snippet: { title: section.TITLE.slice(0, 100), description: section.DESCRIPTION.slice(0, 4900), tags, categoryId: '27', defaultLanguage: lang, defaultAudioLanguage: lang },
    status: { privacyStatus: privacy, selfDeclaredMadeForKids: false, containsSyntheticMedia: true, embeddable: true },
  };
} else {
  const books = JSON.parse(fs.readFileSync('data/books.json', 'utf8'));
  const book = books.find((b) => b.id === bookId) ?? die(`no book "${bookId}" in data/books.json (have: ${books.map((b) => b.id).join(', ')})`);
  const l = book.languages[lang] ?? die(`book "${bookId}" has no language "${lang}" (have: ${Object.keys(book.languages).join(', ')})`);
  const author = book.author[lang] ?? book.author.en;
  metadata = {
    snippet: {
      title: `${l.title} — ${author} | ${lang === 'ru' ? 'Аудиокнига' : 'Audiobook'}`.slice(0, 100),
      description: `${l.description}\n\n${aiNote(lang)}`,
      categoryId: '27', // Education
      defaultLanguage: lang,
      defaultAudioLanguage: lang,
    },
    status: {
      privacyStatus: privacy,
      selfDeclaredMadeForKids: false,
      containsSyntheticMedia: true, // AI voices: YouTube's disclosure for realistic synthetic audio
      embeddable: true, // the site plays it through youtube-nocookie.com
    },
  };
}
const size = fs.statSync(file).size;
console.log(`Video:   ${file} (${(size / 1e6).toFixed(1)} MB)`);
console.log(`Title:   ${metadata.snippet.title}`);
console.log(`Privacy: ${privacy}`);
if (playlist) console.log(`Playlist: ${playlist}`);
if (dryRun) {
  console.log('\n--dry-run: nothing was sent. Metadata:\n' + JSON.stringify(metadata, null, 2));
  process.exit(0);
}

// ---------- Google sign-in (OAuth, loopback redirect, PKCE) ----------
function b64url(buf) {
  return buf.toString('base64url');
}
function readClient() {
  if (!fs.existsSync(CLIENT_FILE)) die(`missing ${CLIENT_FILE}. Create an OAuth client of type "Desktop app" and save its JSON there (see README).`);
  const j = JSON.parse(fs.readFileSync(CLIENT_FILE, 'utf8'));
  const c = j.installed ?? j.web ?? j;
  if (!c.client_id || !c.client_secret) die(`${CLIENT_FILE} has no client_id / client_secret`);
  return c;
}
function saveToken(t) {
  fs.mkdirSync(path.dirname(TOKEN_FILE), { recursive: true });
  fs.writeFileSync(TOKEN_FILE, JSON.stringify(t), { mode: 0o600 });
}
async function tokenRequest(client, params) {
  const res = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ client_id: client.client_id, client_secret: client.client_secret, ...params }),
  });
  const j = await res.json();
  if (!res.ok) die(`Google refused the sign-in: ${j.error_description || j.error}`);
  return j;
}
async function signIn(client) {
  const verifier = b64url(crypto.randomBytes(32));
  const state = b64url(crypto.randomBytes(16));
  const server = http.createServer();
  await new Promise((r) => server.listen(0, '127.0.0.1', r));
  const redirect = `http://127.0.0.1:${server.address().port}`;
  const url =
    'https://accounts.google.com/o/oauth2/v2/auth?' +
    new URLSearchParams({
      client_id: client.client_id,
      redirect_uri: redirect,
      response_type: 'code',
      scope: SCOPE,
      access_type: 'offline',
      prompt: 'consent',
      state,
      code_challenge: b64url(crypto.createHash('sha256').update(verifier).digest()),
      code_challenge_method: 'S256',
    });
  console.log('\nOpening Google sign-in in your browser. If nothing opens, paste this link:\n' + url + '\n');
  execFile(process.platform === 'darwin' ? 'open' : 'xdg-open', [url], () => {});
  const code = await new Promise((resolve, reject) => {
    server.on('request', (req, res) => {
      const q = new URL(req.url, redirect).searchParams;
      res.end('You can close this tab and return to the terminal.');
      if (q.get('state') !== state) return reject(new Error('sign-in state did not match, try again'));
      if (q.get('error')) return reject(new Error('sign-in was not allowed: ' + q.get('error')));
      if (q.get('code')) resolve(q.get('code'));
    });
    setTimeout(() => reject(new Error('sign-in timed out after 5 minutes')), 300000);
  }).finally(() => server.close());
  const t = await tokenRequest(client, { grant_type: 'authorization_code', code, redirect_uri: redirect, code_verifier: verifier });
  const token = { refresh_token: t.refresh_token, access_token: t.access_token, expires_at: Date.now() + t.expires_in * 1000 };
  saveToken(token);
  return token;
}
async function accessToken() {
  const client = readClient();
  let t = fs.existsSync(TOKEN_FILE) ? JSON.parse(fs.readFileSync(TOKEN_FILE, 'utf8')) : await signIn(client);
  if (t.expires_at - Date.now() < 60000) {
    const r = await tokenRequest(client, { grant_type: 'refresh_token', refresh_token: t.refresh_token });
    t = { ...t, access_token: r.access_token, expires_at: Date.now() + r.expires_in * 1000 };
    saveToken(t);
  }
  return t.access_token;
}

// ---------- resumable upload ----------
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function upload() {
  let token = await accessToken();
  const start = await fetch('https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json; charset=UTF-8',
      'X-Upload-Content-Length': String(size),
      'X-Upload-Content-Type': 'video/*',
    },
    body: JSON.stringify(metadata),
  });
  if (!start.ok) die(`YouTube did not accept the upload request (${start.status}): ${(await start.text()).slice(0, 400)}`);
  const session = start.headers.get('location');

  const fd = await fs.promises.open(file, 'r');
  let offset = 0;
  let failures = 0;
  while (true) {
    const len = Math.min(CHUNK, size - offset);
    const buf = Buffer.alloc(len);
    await fd.read(buf, 0, len, offset);
    let res;
    try {
      res = await fetch(session, {
        method: 'PUT',
        headers: { 'Content-Length': String(len), 'Content-Range': `bytes ${offset}-${offset + len - 1}/${size}` },
        body: buf,
      });
    } catch (e) {
      res = null;
    }
    if (res && (res.status === 200 || res.status === 201)) {
      await fd.close();
      return res.json();
    }
    if (res && res.status === 308) {
      const range = res.headers.get('range'); // "bytes=0-N"
      offset = range ? Number(range.split('-')[1]) + 1 : 0;
      failures = 0;
      process.stdout.write(`\rUploaded ${(offset / 1e6).toFixed(0)} of ${(size / 1e6).toFixed(0)} MB`);
      continue;
    }
    // network error or 5xx: ask the server how much it has, then carry on
    if (++failures > 6 || (res && res.status < 500)) {
      await fd.close();
      die(`upload failed (${res ? res.status + ' ' + (await res.text()).slice(0, 300) : 'network error'}). Run the same command again to start over.`);
    }
    await sleep(2000 * failures);
    const probe = await fetch(session, { method: 'PUT', headers: { 'Content-Length': '0', 'Content-Range': `bytes */${size}` } }).catch(() => null);
    if (probe && probe.status === 308) {
      const range = probe.headers.get('range');
      offset = range ? Number(range.split('-')[1]) + 1 : 0;
    }
  }
}

const video = await upload();
console.log(`\n\nDone. Video id: ${video.id}`);
console.log(`Watch:  https://www.youtube.com/watch?v=${video.id}`);

if (thumbnail) {
  const res = await fetch(`https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId=${video.id}`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${await accessToken()}`, 'Content-Type': thumbnail.endsWith('.png') ? 'image/png' : 'image/jpeg' },
    body: fs.readFileSync(thumbnail),
  });
  console.log(res.ok ? 'Thumbnail set.' : `Thumbnail not set (${res.status}): YouTube only allows custom thumbnails on verified channels. Set it in YouTube Studio.`);
}

if (playlist) {
  const res = await fetch('https://www.googleapis.com/youtube/v3/playlistItems?part=snippet', {
    method: 'POST',
    headers: { Authorization: `Bearer ${await accessToken()}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ snippet: { playlistId: playlist, resourceId: { kind: 'youtube#video', videoId: video.id } } }),
  });
  console.log(res.ok
    ? `Added to the playlist ${playlist}.`
    : `Could not add it to the playlist (${res.status}): ${(await res.text()).slice(0, 300)}\nCheck the playlist id, and that the sign-in was made with --playlists. You can also add the video in YouTube Studio.`);
}

if (privacy === 'private') {
  console.log('\nThe video is PRIVATE, so the site cannot play it yet. Open YouTube Studio > Content, and set Visibility to Unlisted or Public.');
}
console.log(`\nThen put this in data/books.json (languages.${lang}.youtube):\n  "youtube": "https://www.youtube.com/watch?v=${video.id}"`);
