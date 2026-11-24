// GET /grandlivre/callback: Grandlivre sends the browser back here after Allow or Deny.
import type { APIRoute } from 'astro';
import { getDeps, readSid } from '../../server/context.ts';
import { finishConnect } from '../../server/grandlivre.ts';
import { pageUrl } from '../../lib/i18n';

export const prerender = false;

export const GET: APIRoute = async ({ cookies, redirect, url }) => {
  const deps = getDeps();
  const sid = deps && readSid(cookies, deps);
  if (!deps || !sid) return redirect(pageUrl('en', '/settings/') + '?grandlivre=state', 303);
  const result = await finishConnect(deps, sid, url.searchParams);
  const lang = result.lang === 'ru' ? 'ru' : 'en';
  return redirect(pageUrl(lang, '/settings/') + '?grandlivre=' + (result.ok ? 'connected' : result.reason), 303);
};
