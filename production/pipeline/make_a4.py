#!/usr/bin/env python3
"""Reading edition on A4 pages: scales every page of the A5 reading PDF up to A4 (the two sizes have the same proportions, so nothing is cut or moved).

  make_a4.py <in_A5_reading.pdf> <out_A4_reading.pdf>"""
import sys
from pypdf import PdfReader, PdfWriter, Transformation
from pypdf.generic import RectangleObject

A4 = (595.276, 841.89)
r, w = PdfReader(sys.argv[1]), PdfWriter()
for src in r.pages:
    ww, hh = float(src.mediabox.width), float(src.mediabox.height)
    k = min(A4[0] / ww, A4[1] / hh)
    pg = w.add_page(src)
    pg.add_transformation(Transformation().scale(k, k))
    box = RectangleObject([0, 0, ww * k, hh * k])
    for name in ("mediabox", "cropbox", "trimbox", "bleedbox", "artbox"):
        setattr(pg, name, box)
w.add_metadata({k: v for k, v in (r.metadata or {}).items() if isinstance(v, str)})
w.write(sys.argv[2])
