// GET /api/video-status?id=<video id>  ->  {"public": true|false}
// Lets a book page show its video as soon as it is made public, without a new build. Only ids that are in
// data/books.json are answered (so this is not an open proxy), and answers are cached in memory.
import type { APIRoute } from 'astro';
import { books } from '../../lib/books';
import { isPublicVideo } from '../../lib/youtube-status';

export const prerender = false;

const known = new Set(books.flatMap((b) => Object.values(b.languages).map((l) => l.videoId)));
const cache = new Map<string, { at: number; ok: boolean }>();

export const GET: APIRoute = async ({ url }) => {
  const id = url.searchParams.get('id') || '';
  const headers = { 'content-type': 'application/json', 'cache-control': 'public, max-age=60' };
  if (!known.has(id) || id === 'PLACEHOLDER') return new Response('{"public":false}', { status: 404, headers });
  const hit = cache.get(id);
  const ttl = hit?.ok ? 3_600_000 : 120_000;
  if (hit && Date.now() - hit.at < ttl) return new Response(JSON.stringify({ public: hit.ok }), { headers });
  const ok = await isPublicVideo(id);
  cache.set(id, { at: Date.now(), ok });
  return new Response(JSON.stringify({ public: ok }), { headers });
};
