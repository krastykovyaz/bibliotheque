// Is a YouTube video public (or unlisted) yet? Asked from our own server, never from the visitor's browser,
// through YouTube's oEmbed endpoint: a private or removed video answers with an error.
export async function isPublicVideo(id: string): Promise<boolean> {
  if (!/^[A-Za-z0-9_-]{11}$/.test(id)) return false;
  try {
    const url = 'https://www.youtube.com/oembed?format=json&url=' + encodeURIComponent('https://www.youtube.com/watch?v=' + id);
    const res = await fetch(url, { signal: AbortSignal.timeout(6000), headers: { 'user-agent': 'bibliotheque-video-status/1.0' } });
    return res.ok;
  } catch {
    return false;
  }
}
