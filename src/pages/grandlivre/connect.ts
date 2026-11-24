// POST /grandlivre/connect: the "Connect Grandlivre" button.
import type { APIRoute } from 'astro';
import { getDeps, readSid, setSid } from '../../server/context.ts';
import { startConnect } from '../../server/grandlivre.ts';
import { pageUrl } from '../../lib/i18n';

export const prerender = false;

export const POST: APIRoute = async ({ request, cookies, redirect, url }) => {
  const lang = (await request.formData()).get('lang') === 'ru' ? 'ru' : 'en';
  const deps = getDeps();
  if (!deps) return redirect(pageUrl(lang, '/settings/') + '?grandlivre=unconfigured', 303);
  let sid = readSid(cookies, deps);
  if (!sid) {
    sid = deps.store.createSession();
    setSid(cookies, sid, url);
  }
  return redirect(startConnect(deps, sid, lang), 303);
};
