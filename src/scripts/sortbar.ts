// Sorting and the number of cards shown, above a card grid (home page and Children page).
// Cards carry data-title, data-author and data-year. The order is kept in the address (?sort=...), no storage.
// The search box (search.ts) hides cards and sends "cardschange" so the count follows.
const bar = document.querySelector<HTMLElement>('[data-sortbar]');
const grid = document.querySelector<HTMLElement>('[data-search-grid], [data-sort-grid]');
const btn = bar?.querySelector<HTMLButtonElement>('[data-dd-btn]');
const list = bar?.querySelector<HTMLElement>('[data-dd-list]');
const current = bar?.querySelector<HTMLElement>('[data-dd-current]');
const count = bar?.querySelector<HTMLElement>('[data-count]');

if (bar && grid && btn && list && current && count) {
  const opts = [...list.querySelectorAll<HTMLElement>('[role=option]')];
  let value = 'shelf';
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
    const key = sorters[value] ? value : 'shelf';
    for (const x of [...items].sort(sorters[key])) grid.append(x.el);
    const url = new URL(location.href);
    if (key === 'shelf') url.searchParams.delete('sort');
    else url.searchParams.set('sort', key);
    history.replaceState(null, '', url);
    updateCount();
  };

  // A dropdown in the site's own style (a button and a listbox), instead of the system menu.
  const choose = (v: string) => {
    value = sorters[v] ? v : 'shelf';
    for (const o of opts) o.setAttribute('aria-selected', String(o.dataset.value === value));
    current.textContent = opts.find((o) => o.dataset.value === value)?.textContent?.replace('✓', '').trim() ?? '';
    apply();
  };
  let active = 0;
  const mark = (i: number) => {
    active = (i + opts.length) % opts.length;
    opts.forEach((o, k) => o.classList.toggle('is-active', k === active));
    list.setAttribute('aria-activedescendant', opts[active].id);
    opts[active].scrollIntoView({ block: 'nearest' });
  };
  const open = () => {
    list.hidden = false;
    btn.setAttribute('aria-expanded', 'true');
    mark(Math.max(0, opts.findIndex((o) => o.dataset.value === value)));
    list.focus();
  };
  const close = (refocus = true) => {
    list.hidden = true;
    btn.setAttribute('aria-expanded', 'false');
    if (refocus) btn.focus();
  };
  btn.addEventListener('click', () => (list.hidden ? open() : close()));
  btn.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault();
      open();
    }
  });
  list.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowDown') (e.preventDefault(), mark(active + 1));
    else if (e.key === 'ArrowUp') (e.preventDefault(), mark(active - 1));
    else if (e.key === 'Home') (e.preventDefault(), mark(0));
    else if (e.key === 'End') (e.preventDefault(), mark(opts.length - 1));
    else if (e.key === 'Enter' || e.key === ' ') (e.preventDefault(), choose(opts[active].dataset.value ?? 'shelf'), close());
    else if (e.key === 'Escape') (e.preventDefault(), close());
    else if (e.key === 'Tab') close(false);
  });
  list.addEventListener('click', (e) => {
    const o = (e.target as HTMLElement).closest<HTMLElement>('[role=option]');
    if (o) (choose(o.dataset.value ?? 'shelf'), close());
  });
  list.addEventListener('mousemove', (e) => {
    const o = (e.target as HTMLElement).closest<HTMLElement>('[role=option]');
    if (o) mark(opts.indexOf(o));
  });
  document.addEventListener('click', (e) => {
    if (!list.hidden && !(e.target as HTMLElement).closest('[data-dd]')) close(false);
  });
  grid.addEventListener('cardschange', updateCount);
  const q = new URL(location.href).searchParams.get('sort');
  choose(q && sorters[q] ? q : 'shelf');
}
