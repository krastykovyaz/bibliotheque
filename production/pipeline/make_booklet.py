#!/usr/bin/env python3
"""Lays out an A5 reading PDF as an A4 landscape saddle-stitch booklet (two pages per side).
Usage: python3 scripts/make-booklet.py reading.pdf booklet.pdf   (needs: pip install pypdf)
Print double-sided (flip on the short edge), fold the stack in half."""
import sys
from pypdf import PdfReader, PdfWriter, PageObject, Transformation

src = PdfReader(sys.argv[1])
n = len(src.pages)
total = (n + 3) // 4 * 4                      # pad with blanks to a multiple of 4
w, h = (float(x) for x in (src.pages[0].mediabox.width, src.pages[0].mediabox.height))
get = lambda i: src.pages[i] if i < n else None
out = PdfWriter()

def side(left, right):
    sheet = PageObject.create_blank_page(width=2 * w, height=h)
    for k, p in enumerate((left, right)):
        if p is not None:
            sheet.merge_transformed_page(p, Transformation().translate(k * w, 0))
    out.add_page(sheet)

for i in range(total // 4):
    side(get(total - 1 - 2 * i), get(2 * i))              # front of the sheet
    side(get(2 * i + 1), get(total - 2 - 2 * i))          # back of the sheet
out.write(sys.argv[2])
print(f"{n} pages -> {total} padded -> {len(out.pages)} landscape sides")
