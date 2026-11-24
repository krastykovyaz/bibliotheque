// Splits a book's text into pages for the reading mode: about TARGET words per page, always ending at a paragraph,
// and a new part (chapter) starts on a fresh page unless the page before it is nearly empty.
import type { ReadingPart } from './books';

export interface PageSection {
  partIndex: number;
  title: string;
  /** true on the page where the part starts: the heading is shown */
  heading: boolean;
  paragraphs: string[];
}
export interface ReaderPage {
  sections: PageSection[];
  words: number;
}

const TARGET = 220;
const NEARLY_EMPTY = 80;
const MAX = 300; // a long paragraph that would take a page past this starts the next page instead

export function paginate(parts: ReadingPart[]): { pages: ReaderPage[]; partPage: number[] } {
  const pages: ReaderPage[] = [];
  const partPage: number[] = [];
  let cur: ReaderPage = { sections: [], words: 0 };
  const flush = () => {
    if (cur.sections.some((s) => s.paragraphs.length)) pages.push(cur);
    cur = { sections: [], words: 0 };
  };
  parts.forEach((part, pi) => {
    if (cur.words >= NEARLY_EMPTY) flush();
    let sec: PageSection | null = null;
    let first = true;
    for (const p of part.paragraphs) {
      const w = p.split(/\s+/).length;
      if (cur.words >= 100 && cur.words + w > MAX) {
        flush();
        sec = null;
      }
      if (!sec) {
        sec = { partIndex: pi, title: part.title, heading: first, paragraphs: [] };
        cur.sections.push(sec);
        if (first) partPage[pi] = pages.length + 1;
        first = false;
      }
      sec.paragraphs.push(p);
      cur.words += w;
      if (cur.words >= TARGET) {
        flush();
        sec = null;
      }
    }
  });
  flush();
  return { pages, partPage };
}
