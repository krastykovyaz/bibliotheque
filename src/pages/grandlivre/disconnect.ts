// POST /grandlivre/disconnect: forget the tokens on our side.
import type { APIRoute } from 'astro';
import { getDeps, readSid } from '../../server/context.ts';
import { disconnect } from '../../server/grandlivre.ts';
import { pageUrl } from '../../lib/i18n';

export const prerender = false;

export const POST: APIRoute = async ({ request, cookies, redirect }) => {
  const lang = (await request.formData()).get('lang') === 'ru' ? 'ru' : 'en';
  const deps = getDeps();
  const sid = deps && readSid(cookies, deps);
  if (deps && sid) disconnect(deps, sid);
  return redirect(pageUrl(lang, '/settings/') + '?grandlivre=disconnected', 303);
};
