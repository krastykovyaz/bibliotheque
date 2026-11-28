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
  /** Optional series: the video is split into parts, each with its own YouTube video; `youtube` is then part 1. */
  parts?: { title: string; youtube: string; videoId: string }[];
  /** Optional YouTube playlist holding all the parts. */
  playlist?: string;
  /** Optional full-text PDF, e.g. "/pdf/lady-en.pdf". */
  pdf?: string;
  /** Optional A4 print-booklet PDF, offered next to the reading PDF. */
  booklet?: string;
  /** Optional A4 booklet for two-sided printing (fold the stack), next to the one-sided booklet. */
  bookletDuplex?: string;
  pdfA4?: string;
  /** Optional excerpt (public/preview/*.txt), shown on the book page without any registration. */
  preview?: string;
  previewParagraphs?: string[];
  /** Optional full text for the reading page, a file in data/ such as "texts/lady-en.txt". */
  text?: string;
  /** Optional short note shown above the text, e.g. that it is a machine translation. */
  textNote?: string;
  readingParts?: ReadingPart[];
}
export interface ReadingPart {
  title: string;
  paragraphs: string[];
}
export interface Book {
  id: string;
  author: Record<string, string>;
  year: number;
  cover: string;
  /** Optional cover for the Russian interface (title and author in Russian). */
  coverRu?: string;
  coverWidth: number;
  coverHeight: number;
  languages: Record<string, BookLanguage>;
  /** A children's book: also listed on the Children page (same cards as the shelf). */
  kids?: boolean;
}

const publicDir = path.join(process.cwd(), 'public');
const dataDir = path.join(process.cwd(), 'data');
const { errors } = validateBooks(raw, publicDir, dataDir);
if (errors.length) {
  throw new Error(`data/books.json has ${errors.length} problem(s):\n` + errors.map((e) => `  - ${e}`).join('\n'));
}

/** "## Title" starts a part; blank lines separate paragraphs. */
function readText(file: string): ReadingPart[] {
  const parts: ReadingPart[] = [];
  for (const block of fs.readFileSync(path.join(dataDir, file), 'utf8').replace(/\r\n/g, '\n').split(/\n\s*\n/)) {
    const t = block.trim();
    if (!t) continue;
    const m = t.match(/^##\s+(.+)$/);
    if (m) parts.push({ title: m[1], paragraphs: [] });
    else {
      if (!parts.length) parts.push({ title: '', paragraphs: [] });
      parts[parts.length - 1].paragraphs.push(t.replace(/\s*\n\s*/g, ' '));
    }
  }
  return parts;
}

export const books: Book[] = (raw as any[]).map((b) => {
  const size = imageSize(fs.readFileSync(path.join(publicDir, b.cover)));
  const languages: Record<string, BookLanguage> = {};
  for (const [code, l] of Object.entries<any>(b.languages)) {
    const previewParagraphs = l.preview
      ? fs.readFileSync(path.join(publicDir, l.preview), 'utf8').split(/\n\s*\n/).map((x: string) => x.trim()).filter(Boolean)
      : undefined;
    languages[code] = { ...l, videoId: parseYouTubeId(l.youtube)!, parts: l.parts?.map((x: any) => ({ ...x, videoId: parseYouTubeId(x.youtube)! })), previewParagraphs, readingParts: l.text ? readText(l.text) : undefined };
  }
  return { ...b, coverWidth: size.width, coverHeight: size.height, languages };
});

/** The cover to show for an interface language: the Russian one on the Russian pages when the book has it. */
export const coverIn = (book: Book, lang: string): string => (lang === 'ru' && book.coverRu ? book.coverRu : book.cover);

/** Texts of a book in the interface language, or English when the book has no such language. */
export const inLang = (book: Book, lang: UiLang) => book.languages[lang] ?? book.languages.en;
export const authorIn = (book: Book, lang: UiLang) => book.author[lang] ?? book.author.en;
