#!/usr/bin/env python3
"""Runs the shared pipeline/build_pdf.py with one CSS change for the verse (English and Russian): lines keep their breaks (white-space: pre-line), left aligned,
a small gap between stanzas.  Usage in this folder:  [BOOK_LANG=ru] python3 build_pdf_verse.py   (both languages are verse)"""
import os, sys
PIPE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pipeline"))
src = open(os.path.join(PIPE, "build_pdf.py"), encoding="utf-8").read()
old = ".part p{margin:0;text-align:justify;text-indent:1.35em;orphans:3;widows:3}"
assert old in src
if True:                      # English and Russian: verse lines keep their breaks
    src = src.replace(old, ".part p{margin:0 0 3.2mm;text-align:left;text-indent:0;white-space:pre-line;hyphens:none;orphans:3;widows:3}")
sys.path.insert(0, PIPE)
g = {"__name__": "__main__", "__file__": os.path.join(PIPE, "build_pdf.py")}
exec(compile(src, os.path.join(PIPE, "build_pdf.py"), "exec"), g)
