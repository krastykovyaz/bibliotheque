import { defineConfig } from 'astro/config';
import node from '@astrojs/node';

// Set SITE_URL at build time, e.g. SITE_URL=https://books.example npm run build
// Book, home and about pages are prerendered as static HTML. Only /settings/ and
// /grandlivre/* run on the Node server (they need a session cookie and token storage).
const site = process.env.SITE_URL || 'https://example.com';

export default defineConfig({
  site,
  // Hosts the server answers for. Needed so form posts (Connect, Disconnect) pass the same-origin check.
  security: { allowedDomains: [{ hostname: 'localhost' }, { hostname: new URL(site).hostname, protocol: new URL(site).protocol.replace(':', '') }] },
  base: process.env.BASE_PATH || '/',
  trailingSlash: 'ignore',
  build: { format: 'directory' },
  adapter: node({ mode: 'standalone' }),
  devToolbar: { enabled: false },
});
