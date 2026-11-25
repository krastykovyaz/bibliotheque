// Build-time validation of data/books.json. Shared by scripts/validate-books.mjs and src/lib/books.ts.
import fs from 'node:fs';
import path from 'node:path';

export function parseYouTubeId(url) {
  try {
    const u = new URL(url);
    const host = u.hostname.replace(/^www\./, '');
    let id = null;
    if (host === 'youtu.be') id = u.pathname.slice(1);
    else if (host === 'youtube.com' || host === 'youtube-nocookie.com' || host === 'm.youtube.com') {
      if (u.pathname === '/watch') id = u.searchParams.get('v');
      else if (/^\/(embed|shorts|live)\//.test(u.pathname)) id = u.pathname.split('/')[2];
    }
    return id && /^[A-Za-z0-9_-]{11}$/.test(id) ? id : null;
  } catch {
    return null;
  }
}

const isStr = (v) => typeof v === 'string' && v.trim().length > 0;

export function validateBooks(books, publicDir, dataDir) {
  const errors = [];
  const warnings = [];
  if (!Array.isArray(books) || books.length === 0) {
    return { errors: ['data/books.json must be a non-empty array of books.'], warnings };
  }
  const seen = new Set();
  books.forEach((b, i) => {
    const where = `book #${i + 1}${b && b.id ? ` ("${b.id}")` : ''}`;
    const err = (field, msg) => errors.push(`${where} → ${field}: ${msg}`);
    if (!b || typeof b !== 'object') return err('(book)', 'must be an object');
    if (!isStr(b.id)) err('id', 'missing or empty');
    else {
      if (!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(b.id)) err('id', 'use lowercase letters, digits and hyphens only');
      if (seen.has(b.id)) err('id', 'duplicate id');
      seen.add(b.id);
    }
    if (!b.author || typeof b.author !== 'object') err('author', 'missing (expected { "en": "Name", "ru": "Имя" })');
    else if (!isStr(b.author.en)) err('author.en', 'missing or empty (English is required)');
    if (!Number.isInteger(b.year)) err('year', 'missing or not an integer');
    if (!isStr(b.cover) || !b.cover.startsWith('/')) err('cover', 'missing; must be a path like "/covers/name.png"');
    else if (!fs.existsSync(path.join(publicDir, b.cover))) err('cover', `file not found: public${b.cover}`);
    if (b.coverRu !== undefined && (!isStr(b.coverRu) || !fs.existsSync(path.join(publicDir, b.coverRu)))) err('coverRu', `file not found: public${b.coverRu}`);
    if (!b.languages || typeof b.languages !== 'object') return err('languages', 'missing');
    if (!b.languages.en) err('languages.en', 'missing (English is required: it is the fallback language)');
    for (const [code, l] of Object.entries(b.languages)) {
      if (!/^[a-z]{2,3}$/.test(code)) err(`languages.${code}`, 'language code must be 2-3 lowercase letters');
      for (const f of ['title', 'description', 'youtube']) {
        if (!l || !isStr(l[f])) err(`languages.${code}.${f}`, 'missing or empty');
      }
      if (l && l.pdf !== undefined) {
        if (!isStr(l.pdf) || !l.pdf.startsWith('/')) err(`languages.${code}.pdf`, 'must be a path like "/pdf/name.pdf"');
        else if (!fs.existsSync(path.join(publicDir, l.pdf))) err(`languages.${code}.pdf`, `file not found: public${l.pdf}`);
      }
      if (l && l.booklet !== undefined) {
        if (l.pdf === undefined) err(`languages.${code}.booklet`, 'needs a "pdf" field next to it');
        else if (!isStr(l.booklet) || !l.booklet.startsWith('/')) err(`languages.${code}.booklet`, 'must be a path like "/pdf/name-booklet.pdf"');
        else if (!fs.existsSync(path.join(publicDir, l.booklet))) err(`languages.${code}.booklet`, `file not found: public${l.booklet}`);
      }
      if (l && l.text !== undefined) {
        if (!isStr(l.text) || l.text.startsWith('/')) err(`languages.${code}.text`, 'must be a path like "texts/name.txt", relative to the data folder');
        else if (dataDir && !fs.existsSync(path.join(dataDir, l.text))) err(`languages.${code}.text`, `file not found: data/${l.text}`);
      }
      if (l && l.textNote !== undefined && !isStr(l.textNote)) err(`languages.${code}.textNote`, 'must be a short text');
      if (l && l.preview !== undefined) {
        if (!isStr(l.preview) || !l.preview.startsWith('/')) err(`languages.${code}.preview`, 'must be a path like "/preview/name.txt"');
        else if (!fs.existsSync(path.join(publicDir, l.preview))) err(`languages.${code}.preview`, `file not found: public${l.preview}`);
      }
      if (l && l.register !== undefined) err(`languages.${code}.register`, 'no longer used, remove it (the download box now offers "Connect Grandlivre")');
      if (l && l.parts !== undefined) {
        if (!Array.isArray(l.parts) || !l.parts.length) err(`languages.${code}.parts`, 'must be a list of { "title", "youtube" }');
        else l.parts.forEach((x, k) => {
          if (!x || !isStr(x.title)) err(`languages.${code}.parts[${k}].title`, 'missing or empty');
          if (!x || !isStr(x.youtube) || !parseYouTubeId(x.youtube)) err(`languages.${code}.parts[${k}].youtube`, 'not a valid YouTube video URL');
        });
      }
      if (l && l.playlist !== undefined && (!isStr(l.playlist) || !/^https:\/\/(www\.)?youtube\.com\/playlist\?list=[\w-]+$/.test(l.playlist))) err(`languages.${code}.playlist`, 'must be a link like https://www.youtube.com/playlist?list=...');
      if (l && isStr(l.youtube)) {
        const id = parseYouTubeId(l.youtube);
        if (!id) err(`languages.${code}.youtube`, `not a valid YouTube video URL: ${l.youtube}`);
        else if (id === 'PLACEHOLDER') warnings.push(`${where} → languages.${code}.youtube: placeholder link, replace before publishing`);
      }
    }
  });
  return { errors, warnings };
}
