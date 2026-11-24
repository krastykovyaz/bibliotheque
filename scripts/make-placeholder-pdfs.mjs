// Generates the placeholder PDFs in public/pdf. Run: node scripts/make-placeholder-pdfs.mjs
// Replace them with the real full-text PDFs; this script is not part of the build.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const out = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../public/pdf');
const files = {
  'lady-en.pdf': 'The Lady with the Little Dog (English)',
  'lady-ru.pdf': 'Dama s sobachkoy (Russian)',
  'usher-en.pdf': 'The Fall of the House of Usher (English)',
  'usher-de.pdf': 'Der Untergang des Hauses Usher (German)',
};
for (const [file, title] of Object.entries(files)) {
  const stream = `BT /F1 22 Tf 72 720 Td (${title}) Tj ET\nBT /F1 13 Tf 72 680 Td (Placeholder PDF. Replace this file with the full text.) Tj ET`;
  const objs = [
    '<< /Type /Catalog /Pages 2 0 R >>',
    '<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
    '<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>',
    `<< /Length ${stream.length} >>\nstream\n${stream}\nendstream`,
    '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>',
  ];
  let pdf = '%PDF-1.4\n';
  const offsets = objs.map((o, i) => {
    const at = pdf.length;
    pdf += `${i + 1} 0 obj\n${o}\nendobj\n`;
    return at;
  });
  const xref = pdf.length;
  pdf += `xref\n0 ${objs.length + 1}\n0000000000 65535 f \n` + offsets.map((o) => `${String(o).padStart(10, '0')} 00000 n \n`).join('');
  pdf += `trailer\n<< /Size ${objs.length + 1} /Root 1 0 R >>\nstartxref\n${xref}\n%%EOF\n`;
  fs.writeFileSync(path.join(out, file), pdf, 'latin1');
  console.log('wrote', file);
}
