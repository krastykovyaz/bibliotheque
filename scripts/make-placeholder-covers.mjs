// Generates the placeholder covers in public/covers. Run: node scripts/make-placeholder-covers.mjs
// Replace the PNG files with real covers whenever you like; this script is not part of the build.
import sharp from 'sharp';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const out = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../public/covers');
const covers = [
  { file: 'lady.png', color: '#7a2e22', lines: ['The Lady', 'with the', 'Little Dog'], author: 'Anton Chekhov' },
  { file: 'usher.png', color: '#2f4a3a', lines: ['The Fall', 'of the House', 'of Usher'], author: 'Edgar Allan Poe' },
];
for (const c of covers) {
  const text = c.lines
    .map((l, i) => `<text x="300" y="${360 + i * 78}" font-size="62" text-anchor="middle" fill="#f6ead4" font-family="Georgia, serif" font-style="italic">${l}</text>`)
    .join('');
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="600" height="900">
  <rect width="600" height="900" fill="${c.color}"/>
  <rect x="28" y="28" width="544" height="844" fill="none" stroke="#e0a94a" stroke-width="4"/>
  <rect x="44" y="44" width="512" height="812" fill="none" stroke="#e0a94a" stroke-width="1.5"/>
  <path d="M240 210h120M270 228h60" stroke="#e0a94a" stroke-width="3"/>
  ${text}
  <path d="M240 640h120" stroke="#e0a94a" stroke-width="3"/>
  <text x="300" y="720" font-size="30" text-anchor="middle" fill="#e0a94a" font-family="Georgia, serif">${c.author}</text>
  <text x="300" y="820" font-size="18" text-anchor="middle" fill="#f6ead4" font-family="Georgia, serif" letter-spacing="4">PLACEHOLDER COVER</text>
</svg>`;
  await sharp(Buffer.from(svg)).png({ palette: true, colours: 64 }).toFile(path.join(out, c.file));
  console.log('wrote', c.file);
}
