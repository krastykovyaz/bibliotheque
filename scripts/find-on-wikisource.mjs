// Looks up every work from data/sources/russian-classics.json on Russian Wikisource
// (MediaWiki API, no key) and writes data/sources/wikisource-matches.json.
// Usage: node scripts/find-on-wikisource.mjs [source.json] [output.json]
import fs from 'node:fs';

const API = 'https://ru.wikisource.org/w/api.php';
const UA = 'classics-catalog-lookup/1.0';
const src = JSON.parse(fs.readFileSync(process.argv[2] ?? 'data/sources/russian-classics.json', 'utf8'));

const norm = (s) => s.toLowerCase().replace(/ё/g, 'е').replace(/[«»"“”„'’.,!?—–\-№]/g, ' ').replace(/\s+/g, ' ').trim();
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// Wikisource limits anonymous clients: go slowly and wait as long as a 429 answer asks.
async function api(params) {
  const url = API + '?' + new URLSearchParams({ format: 'json', formatversion: '2', maxlag: '5', ...params });
  for (let attempt = 0; attempt < 8; attempt++) {
    const res = await fetch(url, { headers: { 'User-Agent': UA } });
    if (res.ok) {
      const data = await res.json();
      if (!data.error) return data;
    }
    await sleep((Number(res.headers.get('retry-after')) || 5 * (attempt + 1)) * 1000 + 1000);
  }
  throw new Error('Wikisource API did not answer: ' + url);
}

async function findWork(title, surname) {
  const data = await api({ action: 'query', list: 'search', srnamespace: '0', srlimit: '30', srsearch: `intitle:"${title.replace(/"/g, '')}" ${surname}` });
  const want = norm(title);
  const roots = new Map();
  for (const r of data.query.search) {
    const root = r.title.split('/')[0];
    const base = norm(root.replace(/\s*\([^)]*\)\s*$/, ''));
    if (base !== want) continue;
    const score = (norm(root).includes(norm(surname)) ? 2 : 0) + (r.title === root ? 1 : 0);
    if (!roots.has(root) || roots.get(root) < score) roots.set(root, score);
  }
  const best = [...roots.entries()].sort((a, b) => b[1] - a[1])[0];
  if (!best) return { found: false, candidates: data.query.search.slice(0, 5).map((r) => r.title) };
  const info = await api({ action: 'query', prop: 'info', titles: best[0], redirects: '1' });
  const page = info.query.pages[0];
  return {
    found: !page.missing,
    author_confirmed: best[1] >= 2,
    page: page.title,
    url: 'https://ru.wikisource.org/wiki/' + encodeURIComponent(page.title.replace(/ /g, '_')),
    bytes: page.length ?? 0,
  };
}

// Results are saved after every work, so an interrupted run continues where it stopped.
const OUT = process.argv[3] ?? 'data/sources/wikisource-matches.json';
const out = fs.existsSync(OUT) ? JSON.parse(fs.readFileSync(OUT, 'utf8')) : [];
const done = new Set(out.map((m) => m.author + '|' + m.title_ru));
for (const a of src.authors) {
  const surname = a.name_ru.split(' ').pop();
  for (const w of a.works) {
    if (done.has(a.name_en + '|' + w.title_ru)) continue;
    const m = await findWork(w.title_ru, surname);
    out.push({ author: a.name_en, title_en: w.title_en, title_ru: w.title_ru, ...m });
    fs.writeFileSync(OUT, JSON.stringify(out, null, 2) + '\n');
    console.log(m.found ? (m.author_confirmed ? 'OK   ' : 'CHECK') : 'MISS ', a.name_en, '|', w.title_ru, '->', m.page ?? m.candidates.join('; '));
    await sleep(1500);
  }
}
const found = out.filter((m) => m.found).length;
console.log(`\n${found} of ${out.length} works found (${out.filter((m) => m.found && !m.author_confirmed).length} need an author check)`);
