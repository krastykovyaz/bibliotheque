#!/usr/bin/env python3
"""Square playlist cover (YouTube accepts only square images): the 16:9 series card sits in the middle band, a blurred copy fills the rest.
   production/pipeline/.venv/bin/python production/pipeline/make_series_square.py production/<slug>/<Prefix>_series_card.png"""
import sys
from PIL import Image, ImageFilter
src = sys.argv[1]
im = Image.open(src).convert("RGB")
S = 1080
band = im.resize((S, round(S * im.height / im.width)), Image.LANCZOS)
bg = im.resize((S, S), Image.LANCZOS).filter(ImageFilter.GaussianBlur(40))
bg.paste(band, (0, (S - band.height) // 2))
out = src.replace("_series_card.png", "_series_square.png")
bg.save(out, optimize=True); print(out)
