// Book page: audio-language switch (kept in ?lang=) and click-to-load YouTube player.
// No cookies, no storage. The page is fully readable without this script.
const root = document.querySelector<HTMLElement>('[data-book]');
if (root) {
  const panels = [...root.querySelectorAll<HTMLElement>('[data-panel]')];
  const chips = [...root.querySelectorAll<HTMLAnchorElement>('[data-lang]')];
  const note = root.querySelector<HTMLElement>('[data-note-box]')!;
  const names: Record<string, string> = JSON.parse(root.dataset.names || '{}');
  const has = (code: string) => panels.some((p) => p.dataset.panel === code);

  const stop = (player: HTMLElement) => {
    player.querySelector('iframe')?.remove();
    player.classList.remove('is-playing');
    player.querySelectorAll<HTMLElement>('[data-play], .player-hint').forEach((el) => (el.hidden = false));
  };

  const show = (requested: string) => {
    const active = has(requested) ? requested : 'en';
    for (const p of panels) {
      const on = p.dataset.panel === active;
      p.classList.toggle('is-active', on);
      if (!on) p.querySelectorAll<HTMLElement>('.player').forEach(stop);
      if (on) document.title = `${p.dataset.title}, ${root.dataset.author} | ${root.dataset.site}`;
    }
    for (const c of chips) {
      if (c.dataset.lang === active) c.setAttribute('aria-current', 'true');
      else c.removeAttribute('aria-current');
    }
    note.hidden = active === requested;
    if (active !== requested) {
      note.textContent = (root.dataset.note || '').replace('{lang}', names[requested] || requested.toUpperCase());
    }
  };

  const fromUrl = () => {
    const p = new URLSearchParams(location.search).get('lang');
    return p && /^[a-z]{2,3}$/.test(p) ? p : root.dataset.uiLang || 'en';
  };
  show(fromUrl());

  for (const c of chips) {
    c.addEventListener('click', (e) => {
      e.preventDefault();
      const code = c.dataset.lang!;
      show(code);
      const url = new URL(location.href);
      url.searchParams.set('lang', code);
      url.hash = '';
      history.replaceState(null, '', url);
    });
  }

  root.addEventListener('click', (e) => {
    const btn = (e.target as HTMLElement).closest<HTMLElement>('[data-play]');
    const player = btn?.closest<HTMLElement>('.player');
    if (!btn || !player) return;
    const frame = document.createElement('iframe');
    frame.src = `https://www.youtube-nocookie.com/embed/${player.dataset.video}?autoplay=1&rel=0`;
    frame.title = root.dataset.playerTitle || 'YouTube';
    frame.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
    frame.allowFullscreen = true;
    frame.referrerPolicy = 'strict-origin-when-cross-origin';
    player.querySelectorAll<HTMLElement>('[data-play], .player-hint').forEach((el) => (el.hidden = true));
    player.classList.add('is-playing');
    player.append(frame);
    frame.focus();
  });
}
