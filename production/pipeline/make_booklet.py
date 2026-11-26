#!/usr/bin/env python3
"""Lays out an A5 reading PDF as an A4 landscape saddle-stitch booklet (two pages per side).
Usage: python3 make_booklet.py reading.pdf booklet.pdf [--fold]   (needs: pypdf)
Default (what we publish): print SINGLE-sided; sheet k carries page N+1-k on the left and page k on the right (24|1, 23|2, 22|3 ...
13|12 for N=24). Cut the whole stack down the middle: the right-hand pile is pages 1..N/2 in order, the left-hand pile is
N..N/2+1, so turn it over to get N/2+1..N and put it behind the first pile. Glue or bind at the left edge.
--fold: saddle-stitch order for double-sided printing (flip on the short edge), fold the stack in half."""
import sys
from pypdf import PdfReader, PdfWriter, PageObject, Transformation

FOLD = '--fold' in sys.argv
src = PdfReader(sys.argv[1])
n = len(src.pages)
total = (n + 3) // 4 * 4 if FOLD else (n + 1) // 2 * 2   # blanks: multiple of 4 (fold) / even (plain)
w, h = (float(x) for x in (src.pages[0].mediabox.width, src.pages[0].mediabox.height))
get = lambda i: src.pages[i] if i < n else None
out = PdfWriter()

# Every page is shrunk a little and moved away from the centre line, so that nothing is near the fold / the cut when the sheet is halved
# and a printer's unprintable edge cannot take a letter: inner gap = 75 % of the spare width, outer gap = 25 %.
SCALE, INNER = 0.94, 0.75
def side(left, right):
    sheet = PageObject.create_blank_page(width=2 * w, height=h)
    spare = w * (1 - SCALE)
    for k, p in enumerate((left, right)):
        if p is not None:
            x = k * w + (spare * (1 - INNER) if k == 0 else spare * INNER)
            sheet.merge_transformed_page(p, Transformation().scale(SCALE, SCALE).translate(x, h * (1 - SCALE) / 2))
    out.add_page(sheet)

if FOLD:
    for i in range(total // 4):
        side(get(total - 1 - 2 * i), get(2 * i))              # front of the sheet
        side(get(2 * i + 1), get(total - 2 - 2 * i))          # back of the sheet
else:
    for i in range(total // 2):
        side(get(total - 1 - i), get(i))                      # single-sided: N|1, N-1|2, N-2|3, ...
out.write(sys.argv[2])
print(f"{n} pages -> {total} padded -> {len(out.pages)} landscape sides")
