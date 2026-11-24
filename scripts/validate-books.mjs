import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { validateBooks } from '../src/lib/validate.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const file = path.join(root, 'data/books.json');
let data;
try {
  data = JSON.parse(fs.readFileSync(file, 'utf8'));
} catch (e) {
  console.error(`\n✖ data/books.json is not valid JSON: ${e.message}\n`);
  process.exit(1);
}
const { errors, warnings } = validateBooks(data, path.join(root, 'public'));
warnings.forEach((w) => console.warn(`⚠ ${w}`));
if (errors.length) {
  console.error(`\n✖ data/books.json has ${errors.length} problem(s):\n`);
  errors.forEach((e) => console.error(`  - ${e}`));
  console.error('\nFix the file and run the build again.\n');
  process.exit(1);
}
console.log('✔ data/books.json is valid');
