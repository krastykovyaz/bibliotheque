#!/usr/bin/env python3
"""Pulls the story text out of one of our reading PDFs (A5, one story, parts with a big italic "I Title" heading,
a drop capital at the start of each part, indented paragraphs) into a plain text file for the site's reading page.

  python scripts/extract-text-from-pdf.py public/pdf/lady-en.pdf data/texts/lady-en.txt

Output format: "## I · Yalta" lines start a part; paragraphs are separated by blank lines.
Needs PyMuPDF (pip install pymupdf)."""
import re, sys
import pymupdf

src, out = sys.argv[1], sys.argv[2]
doc = pymupdf.open(src)
body_size, indent_min, indent_max = None, None, None

# 1. all text lines with their geometry
lines = []
for pno, page in enumerate(doc):
    H = page.rect.height
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            sp = [s for s in l["spans"] if s["text"].strip()]
            if not sp:
                continue
            x0, y0, x1, y1 = l["bbox"]
            lines.append({"p": pno, "y": y0, "x0": x0, "x1": x1, "text": "".join(s["text"] for s in l["spans"]).strip(),
                          "size": max(s["size"] for s in sp), "ital": any(s["flags"] & 2 for s in sp), "H": H})
# body text size = the most common size among longer lines
from collections import Counter
body_size = Counter(round(l["size"], 1) for l in lines if len(l["text"]) > 30).most_common(1)[0][0]
left = Counter(round(l["x0"], 0) for l in lines if abs(l["size"] - body_size) < 0.3 and len(l["text"]) > 30).most_common(1)[0][0]
# paragraphs begin with a first-line indent of about 16 pt
INDENT = (left + 14.5, left + 18.5)       # the lines beside a drop capital are indented more, so they do not match

parts, cur, para, cap = [], None, [], ""


def flush():
    global para
    if para and cur is not None:
        text = "".join(w if w.endswith("‐") else w + " " for w in para[:-1]) + para[-1]
        text = text.replace("‐", "")            # a line ended with a hyphen: the word is joined
        cur["paragraphs"].append(re.sub(r"\s+", " ", text).strip())
    para = []


for pno in range(len(doc)):
    page_lines = sorted((l for l in lines if l["p"] == pno), key=lambda l: (round(l["y"] / 4), l["x0"]))
    for l in page_lines:
        t = l["text"]
        if l["y"] > l["H"] - 50 and re.fullmatch(r"\d+", t):
            continue                                   # page number in the footer
        m = re.fullmatch(r"(I{1,3}|IV|V|VI{0,3}|IX|X) (.+)", t)
        if m and l["size"] >= 25:                      # big heading, e.g. "I Yalta"
            flush()
            cur = {"title": f"{m.group(1)} · {m.group(2)}", "paragraphs": []}
            parts.append(cur)
            cap = ""
            continue
        if cur is None:
            continue                                   # cover, title page, contents
        if l["size"] >= 25 and len(t) == 1:            # drop capital: the first letter of the part's first paragraph
            cap = t
            continue
        if l["size"] > body_size + 0.3:
            continue                                   # the small scene caption under the heading
        if abs(l["size"] - body_size) > 0.35:
            continue
        starts = (INDENT[0] <= l["x0"] <= INDENT[1]) or cap
        if starts:
            flush()
        if cap:
            t, cap = cap + t, ""
        para.append(t)
flush()

with open(out, "w", encoding="utf-8") as f:
    for part in parts:
        f.write(f"## {part['title']}\n\n")
        f.write("\n\n".join(part["paragraphs"]) + "\n\n")
words = sum(len(p.split()) for part in parts for p in part["paragraphs"])
print(f"{src}: {len(parts)} parts, {sum(len(p['paragraphs']) for p in parts)} paragraphs, {words} words -> {out}")
for part in parts:
    print(f"  {part['title']}: {len(part['paragraphs'])} paragraphs")
