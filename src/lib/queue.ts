// "Next on the shelf": one book from data/queue.json per day, in order, starting at the file's "start" date.
// The page is built ahead of time, so a rebuild each day (see README) moves it on.
import queue from '../../data/queue.json';

export interface QueueItem {
  author_en: string;
  author_ru: string;
  title_en: string;
  title_ru: string;
}

if (!Array.isArray(queue.items) || queue.items.length === 0) throw new Error('data/queue.json needs a non-empty "items" list');

const day = (d: Date) => Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()) / 86400000;

/** The book announced on the given day, and that day. Before "start" it shows the first book. */
export function nextBook(now: Date = new Date()): { item: QueueItem; date: Date } {
  const [y, m, d] = queue.start.split('-').map(Number);
  const n = queue.items.length;
  const offset = Math.max(0, day(now) - day(new Date(y, m - 1, d)));
  return { item: queue.items[offset % n] as QueueItem, date: now };
}
