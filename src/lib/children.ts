// Children's authors and stories (data/sources/children.json) with a link to each Russian
// original on Wikisource (data/sources/wikisource-children.json, made by scripts/find-on-wikisource.mjs).
import list from '../../data/sources/children.json';
import matches from '../../data/sources/wikisource-children.json';

export interface ChildWork {
  titleEn: string;
  titleRu: string;
  /** Link to the Russian original, only when the page was found and the author confirmed. */
  url?: string;
}
export interface ChildAuthor {
  nameEn: string;
  nameRu: string;
  born: number;
  died: number;
  works: ChildWork[];
}

const link = new Map<string, string>();
for (const m of matches as any[]) {
  if (m.found && m.author_confirmed) link.set(m.author + '|' + m.title_ru, m.url);
}

export const childAuthors: ChildAuthor[] = (list.authors as any[]).map((a) => ({
  nameEn: a.name_en,
  nameRu: a.name_ru,
  born: a.born,
  died: a.died,
  works: a.works.map((w: any) => ({ titleEn: w.title_en, titleRu: w.title_ru, url: link.get(a.name_en + '|' + w.title_ru) })),
}));
