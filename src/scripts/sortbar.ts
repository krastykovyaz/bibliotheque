// Sorting and the number of cards shown, above a card grid (home page and Children page).
// Cards carry data-title, data-author and data-year. The order is kept in the address (?sort=...), no storage.
// The search box (search.ts) hides cards and sends "cardschange" so the count follows.
const bar = document.querySelector<HTMLElement>('[data-sortbar]');
const grid = document.querySelector<HTMLElement>('[data-search-grid], [data-sort-grid]');
const select = bar?.querySelector<HTMLSelectElement>('[data-sort]');
const count = bar?.querySelector<HTMLElement>('[data-count]');

if (bar && grid && select && count) {
  const lang = document.documentElement.lang || 'en';
  type Item = { el: HTMLElement; i: number; title: string; author: string; year: number | null };
  const items: Item[] = [...grid.children].map((el, i) => ({
    el: el as HTMLElement,
    i,
    title: el.getAttribute('data-title') ?? '',
    author: el.getAttribute('data-author') ?? '',
    year: el.getAttribute('data-year') ? Number(el.getAttribute('data-year')) : null,
  }));
  const cmpText = (a: string, b: string) => a.localeCompare(b, lang, { sensitivity: 'base' });
  const byYear = (dir: 1 | -1) => (a: Item, b: Item) => {
    if (a.year === null && b.year === null) return a.i - b.i;
    if (a.year === null) return 1; // stories without a year (not made yet) go last
    if (b.year === null) return -1;
    return (a.year - b.year) * dir || cmpText(a.title, b.title);
  };
  const sorters: Record<string, (a: Item, b: Item) => number> = {
    shelf: (a, b) => a.i - b.i,
    title: (a, b) => cmpText(a.title, b.title),
    author: (a, b) => cmpText(a.author, b.author) || cmpText(a.title, b.title),
    year: byYear(1),
    'year-desc': byYear(-1),
  };

  const updateCount = () => {
    const shown = items.filter((x) => !x.el.hidden).length;
    count.textContent = (bar.dataset.showing ?? '{n}').replace('{n}', String(shown));
  };
  const apply = () => {
    const key = sorters[select.value] ? select.value : 'shelf';
    for (const x of [...items].sort(sorters[key])) grid.append(x.el);
    const url = new URL(location.href);
    if (key === 'shelf') url.searchParams.delete('sort');
    else url.searchParams.set('sort', key);
    history.replaceState(null, '', url);
    updateCount();
  };

  select.addEventListener('change', apply);
  grid.addEventListener('cardschange', updateCount);
  const q = new URL(location.href).searchParams.get('sort');
  if (q && sorters[q]) select.value = q;
  apply();
}
