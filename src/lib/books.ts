// Loads and validates data/books.json. Everything the pages show comes from here.
import fs from 'node:fs';
import path from 'node:path';
import { imageSize } from 'image-size';
import raw from '../../data/books.json';
import { validateBooks, parseYouTubeId } from './validate.mjs';
import type { UiLang } from './i18n';

export interface BookLanguage {
  title: string;
  description: string;
  youtube: string;
  videoId: string;
  /** Optional full-text PDF, e.g. "/pdf/lady-en.pdf". */
  pdf?: string;
  /** Optional A4 print-booklet PDF, offered next to the reading PDF. */
  booklet?: string;
  /** Optional excerpt (public/preview/*.txt), shown on the book page without any registration. */
  preview?: string;
  previewParagraphs?: string[];
}
export interface Book {
  id: string;
  author: Record<string, string>;
  year: number;
  cover: string;
  coverWidth: number;
  coverHeight: number;
  languages: Record<string, BookLanguage>;
}

const publicDir = path.join(process.cwd(), 'public');
const { errors } = validateBooks(raw, publicDir);
if (errors.length) {
  throw new Error(`data/books.json has ${errors.length} problem(s):\n` + errors.map((e) => `  - ${e}`).join('\n'));
}

export const books: Book[] = (raw as any[]).map((b) => {
  const size = imageSize(fs.readFileSync(path.join(publicDir, b.cover)));
  const languages: Record<string, BookLanguage> = {};
  for (const [code, l] of Object.entries<any>(b.languages)) {
    const previewParagraphs = l.preview
      ? fs.readFileSync(path.join(publicDir, l.preview), 'utf8').split(/\n\s*\n/).map((x: string) => x.trim()).filter(Boolean)
      : undefined;
    languages[code] = { ...l, videoId: parseYouTubeId(l.youtube)!, previewParagraphs };
  }
  return { ...b, coverWidth: size.width, coverHeight: size.height, languages };
});

/** Texts of a book in the interface language, or English when the book has no such language. */
export const inLang = (book: Book, lang: UiLang) => book.languages[lang] ?? book.languages.en;
export const authorIn = (book: Book, lang: UiLang) => book.author[lang] ?? book.author.en;
