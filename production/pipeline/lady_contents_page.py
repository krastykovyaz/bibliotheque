#!/usr/bin/env python3
"""Lady with the Little Dog (no production folder): moves the list of parts from the title page onto its own Contents page (page 2),
renumbers the printed page numbers, and re-makes the A4 reading file and both booklets.
  production/pipeline/.venv/bin/python production/pipeline/lady_contents_page.py"""
import os, subprocess, sys
import pymupdf
PIPE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(PIPE, "..", ".."))
F = "/System/Library/Fonts/Supplemental/Times New Roman"
GOLD, INK, GREY = (0x8a/255, 0x64/255, 0x10/255), (0x1b/255, 0x18/255, 0x28/255), (0x55/255, 0x50/255, 0x66/255)
R, I, B = pymupdf.Font(fontfile=F + ".ttf"), pymupdf.Font(fontfile=F + " Italic.ttf"), pymupdf.Font(fontfile=F + " Bold.ttf")
LANG = {"en": ("CONTENTS", [("I", "Yalta"), ("II", "Oreanda"), ("III", "The Grey Fence"), ("IV", "Moscow")], (364, 462)),
        "ru": ("СОДЕРЖАНИЕ", [("I", "Ялта"), ("II", "Ореанда"), ("III", "Серый забор"), ("IV", "Москва")], (327, 424))}

def put(page, x, y, text, font, size, color, name):
    tw = pymupdf.TextWriter(page.rect, color=color); tw.append((x, y), text, font=font, fontsize=size); tw.write_text(page)
    return font.text_length(text, fontsize=size)

for lang, (head, parts, (y0, y1)) in LANG.items():
    path = os.path.join(ROOT, "public/pdf", f"lady-{lang}.pdf")
    d = pymupdf.open(path)
    if d[1].get_text().strip().upper().startswith(head[:4]):
        print(lang, "already has the contents page"); continue
    # part start pages (old numbering): the big roman numeral + title line on the page
    starts = []
    for i, pg in enumerate(d):
        for b in pg.get_text("dict")["blocks"]:
            for ln in b.get("lines", []):
                t = "".join(s["text"] for s in ln["spans"]).strip()
                if i > 0 and ln["spans"][0]["size"] > 29 and " " in t and t.split(" ")[0] in ("I", "II", "III", "IV"): starts.append(i + 1)
    assert len(starts) == 4, starts
    # 1. the title page loses its list of parts and the two rules around it
    p1 = d[0]; p1.draw_rect(pymupdf.Rect(30, y0, 390, y1), color=None, fill=(1, 1, 1))
    # 2. printed page numbers +1 (pages 2 .. N-1)
    for i in range(1, len(d) - 1):
        pg = d[i]
        for b in pg.get_text("dict")["blocks"]:
            for ln in b.get("lines", []):
                t = "".join(s["text"] for s in ln["spans"]).strip()
                if ln["bbox"][1] > 560 and t.isdigit():
                    pg.add_redact_annot(pymupdf.Rect(ln["bbox"]) + (-3, -2, 3, 2), fill=(1, 1, 1)); pg.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE, graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)
                    s = str(int(t) + 1); w = R.text_length(s, fontsize=8.5); put(pg, 210 - w / 2, 574.5, s, R, 8.5, (0.35, 0.35, 0.4), "n")
    # 3. the Contents page
    c = d.new_page(pno=1, width=d[0].rect.width, height=d[0].rect.height)
    x = 210 - sum(B.text_length(ch, fontsize=14) + 3.2 for ch in head) / 2
    for ch in head:
        put(c, x, 130, ch, B, 14, INK, "h"); x += B.text_length(ch, fontsize=14) + 3.2
    for k, ((num, title), pnum) in enumerate(zip(parts, starts)):
        y = 190 + k * 30
        put(c, 76, y, num, I, 12, GOLD, "r"); put(c, 112, y, title, R, 12, INK, "t")
        s = str(pnum + 1); wn = R.text_length(s, fontsize=12); put(c, 344 - wn, y, s, R, 12, INK, "p")
        x0 = 112 + R.text_length(title, fontsize=12) + 6; x1 = 344 - wn - 6
        dots = pymupdf.Point(x0, y - 2)
        while dots.x < x1: c.draw_circle(dots, 0.45, color=None, fill=(0.65, 0.6, 0.55)); dots.x += 3.2
    d.save(path + ".new", garbage=3, deflate=True); d.close(); os.replace(path + ".new", path)
    mk = os.path.join(PIPE, "make_booklet.py"); pub = os.path.join(ROOT, "public/pdf")
    subprocess.run([sys.executable, "-W", "ignore", mk, path, os.path.join(pub, f"lady-{lang}-booklet.pdf")], check=True)
    subprocess.run([sys.executable, "-W", "ignore", mk, path, os.path.join(pub, f"lady-{lang}-booklet-duplex.pdf"), "--fold"], check=True)
    subprocess.run([sys.executable, "-W", "ignore", os.path.join(PIPE, "make_a4.py"), path, os.path.join(pub, f"lady-{lang}-a4.pdf")], check=True)
    print(lang, "done: parts start on pages", [s + 1 for s in starts])
