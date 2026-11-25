// Sorting, "how many to show" and the number of cards shown, above a card grid (home page and Children page).
// Cards carry data-title, data-author and data-year. The choices are kept in the address (?sort=..&show=..), no storage.
// The search box (search.ts) hides cards (hidden) and sends "cardschange"; the limit hides the rest with data-cut.
const bar = document.querySelector<HTMLElement>('[data-sortbar]');
const grid = document.querySelector<HTMLElement>('[data-search-grid], [data-sort-grid]');
const count = bar?.querySelector<HTMLElement>('[data-count]');

type Item = { el: HTMLElement; i: number; title: string; author: string; year: number | null };

// A dropdown in the site's own style (a button and a listbox), instead of the system menu.
function dropdown(root: HTMLElement, initial: string, onChange: (value: string) => void) {
  const btn = root.querySelector<HTMLButtonElement>('[data-dd-btn]')!;
  const list = root.querySelector<HTMLElement>('[data-dd-list]')!;
  const current = root.querySelector<HTMLElement>('[data-dd-current]')!;
  const opts = [...list.querySelectorAll<HTMLElement>('[role=option]')];
  let value = '';
  let active = 0;
  const choose = (v: string, notify = true) => {
    const o = opts.find((x) => x.dataset.value === v) ?? opts[0];
    value = o.dataset.value ?? '';
    for (const x of opts) x.setAttribute('aria-selected', String(x === o));
    current.textContent = o.textContent?.replace('✓', '').trim() ?? '';
    if (notify) onChange(value);
  };
  const mark = (i: number) => {
    active = (i + opts.length) % opts.length;
    opts.forEach((o, k) => o.classList.toggle('is-active', k === active));
    list.setAttribute('aria-activedescendant', opts[active].id);
    opts[active].scrollIntoView({ block: 'nearest' });
  };
  const open = () => {
    document.dispatchEvent(new CustomEvent('dd-open', { detail: root }));
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
    else if (e.key === 'Enter' || e.key === ' ') (e.preventDefault(), choose(opts[active].dataset.value ?? ''), close());
    else if (e.key === 'Escape') (e.preventDefault(), close());
    else if (e.key === 'Tab') close(false);
  });
  list.addEventListener('click', (e) => {
    const o = (e.target as HTMLElement).closest<HTMLElement>('[role=option]');
    if (o) (choose(o.dataset.value ?? ''), close());
  });
  list.addEventListener('mousemove', (e) => {
    const o = (e.target as HTMLElement).closest<HTMLElement>('[role=option]');
    if (o) mark(opts.indexOf(o));
  });
  document.addEventListener('click', (e) => {
    if (!list.hidden && !(e.target as HTMLElement).closest('[data-dd]')) close(false);
  });
  document.addEventListener('dd-open', (e) => {
    if ((e as CustomEvent).detail !== root && !list.hidden) close(false);
  });
  choose(initial, false);
}

if (bar && grid && count) {
  // the count goes under the cards, on the right
  const foot = document.createElement('div');
  foot.className = 'sort-foot';
  foot.append(count);
  grid.after(foot);
  const lang = document.documentElement.lang || 'en';
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
  // a cover that fails once (a dropped connection) is asked for again, once
  grid.querySelectorAll<HTMLImageElement>('img').forEach((img) => {
    img.addEventListener('error', () => {
      if (img.dataset.retry) return;
      img.dataset.retry = '1';
      setTimeout(() => (img.src = img.currentSrc.split('?')[0] + '?r=1'), 800);
    });
  });
  const limits = ['6', '12', '24', '48', 'all'];
  let sort = 'shelf';
  let show = 'all';

  // the limit hides the cards beyond the first N of those that match the search; the count says how many are shown of how many match
  const refresh = () => {
    const limit = show === 'all' ? Infinity : Number(show);
    let matching = 0;
    let shown = 0;
    for (const item of [...items].sort(sorters[sort])) {
      const x = item.el;
      if (x.hidden) {
        x.removeAttribute('data-cut');
        continue;
      }
      matching++;
      if (matching > limit) x.setAttribute('data-cut', '');
      else {
        x.removeAttribute('data-cut');
        shown++;
      }
    }
    count.textContent = (bar.dataset.showing ?? '{n}').replace('{n}', String(shown)).replace('{total}', String(matching));
  };
  const apply = () => {
    // Sort with the CSS order property, not by moving the cards: moving a card with a lazy-loaded picture can make the picture fail to load.
    [...items].sort(sorters[sort]).forEach((x, k) => (x.el.style.order = String(k)));
    const url = new URL(location.href);
    if (sort === 'shelf') url.searchParams.delete('sort');
    else url.searchParams.set('sort', sort);
    if (show === '48') url.searchParams.delete('show');
    else url.searchParams.set('show', show);
    history.replaceState(null, '', url);
    refresh();
  };

  const params = new URL(location.href).searchParams;
  sort = sorters[params.get('sort') ?? ''] ? (params.get('sort') as string) : 'shelf';
  show = limits.includes(params.get('show') ?? '') ? (params.get('show') as string) : '48';
  dropdown(bar.querySelector<HTMLElement>('[data-dd=sort]')!, sort, (v) => ((sort = v), apply()));
  dropdown(bar.querySelector<HTMLElement>('[data-dd=show]')!, show, (v) => ((show = v), apply()));
  grid.addEventListener('cardschange', refresh);
  apply();
}
