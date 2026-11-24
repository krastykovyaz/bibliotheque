// The search box in the header, on every page.
// On the home page it filters the book cards and the children's stories as you type (one common search).
// On any other page, pressing Enter opens the home page with the results (/?q=...).
// Without JavaScript the box is hidden. The query is kept in the address (?q=...) so a search can be shared.
const form = document.querySelector<HTMLFormElement>('.header-search');
const input = document.querySelector<HTMLInputElement>('#book-search');
const grid = document.querySelector<HTMLElement>('[data-search-grid]');
const status = document.querySelector<HTMLElement>('[data-search-status]');
const empty = document.querySelector<HTMLElement>('[data-search-empty]');

if (form && input && grid && status && empty) {
  // Lower case, no accents, "ё" = "е": "Bibliotheque" finds "Bibliothèque", "Чехов" finds "ЧЕХОВ".
  const norm = (s: string) => s.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/ё/g, 'е');
  // Children's stories (data-kid) are hidden cards: they show only while something is typed and they match.
  const cards = [...grid.children].map((el) => ({ el: el as HTMLElement, kid: el.hasAttribute('data-kid'), text: norm(el.getAttribute('data-search') ?? '') }));

  const run = () => {
    const words = norm(input.value).split(/\s+/).filter(Boolean);
    let shown = 0;
    for (const c of cards) {
      const match = words.every((w) => c.text.includes(w)) && (!c.kid || words.length > 0);
      c.el.hidden = !match;
      if (match) shown++;
    }
    empty.hidden = shown > 0;
    status.textContent = words.length ? (status.dataset.template ?? '').replace('{n}', String(shown)) : '';
    const url = new URL(location.href);
    if (input.value.trim()) url.searchParams.set('q', input.value.trim());
    else url.searchParams.delete('q');
    history.replaceState(null, '', url);
  };

  form.addEventListener('submit', (e) => e.preventDefault());
  input.addEventListener('input', run);
  const q = new URL(location.href).searchParams.get('q');
  if (q) {
    input.value = q;
    run();
  }
}
