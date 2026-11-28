#!/usr/bin/env python3
"""Appends the standard last page (QR codes, credits, next on the shelf) to a reading PDF we did not build ourselves (Lady with the
Little Dog), and re-makes its A4 booklet.
  production/pipeline/.venv/bin/python production/pipeline/add_last_page.py lady-with-the-little-dog lady"""
import os, subprocess, sys, tempfile
from pypdf import PdfReader, PdfWriter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lastpage
PIPE = os.path.dirname(os.path.abspath(__file__)); ROOT = lastpage.ROOT
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
slug, short = sys.argv[1], sys.argv[2]
INFO = {"lady-with-the-little-dog": {"en": ("The Lady with the Little Dog", "Anton Chekhov", 1899), "ru": ("Дама с собачкой", "Антон Чехов", 1899)}}[slug]
FONTS = f"""@font-face{{font-family:Lora;src:url(file://{PIPE}/fonts/lora-latin-400-normal.woff2) format("woff2");font-weight:400}}
@font-face{{font-family:Lora;src:url(file://{PIPE}/fonts/lora-latin-600-normal.woff2) format("woff2");font-weight:600}}
@font-face{{font-family:Lora;src:url(file://{PIPE}/fonts/lora-latin-400-italic.woff2) format("woff2");font-weight:400;font-style:italic}}
@font-face{{font-family:Lora;src:url(file://{PIPE}/fonts/lora-cyrillic-wght-normal.woff2) format("woff2");font-weight:400 700;font-style:normal;unicode-range:U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116}}
@font-face{{font-family:Lora;src:url(file://{PIPE}/fonts/lora-cyrillic-wght-italic.woff2) format("woff2");font-weight:400 700;font-style:italic;unicode-range:U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116}}
@page{{size:148mm 210mm;margin:17mm 15mm 21mm 15mm}}@page front{{}}
html{{font-family:Lora,serif;font-size:10.6pt;color:#2a211c}}body{{margin:0}}"""
for lang in ("en", "ru"):
    title, author, year = INFO[lang]
    credits = (f"{author}, «{title}» ({year}). The text is in the public domain. Typeset in Lora (SIL Open Font License)."
               if lang == "en" else f"{author}, «{title}» ({year}). Текст находится в общественном достоянии. Набрано шрифтом Lora (SIL Open Font License).")
    body = lastpage.section(lang, slug, INFO["en"][0], [], credits)
    tmp = tempfile.mkdtemp(); h = os.path.join(tmp, "p.html"); pdf = os.path.join(tmp, "p.pdf")
    open(h, "w", encoding="utf-8").write(f"<!doctype html><meta charset=utf-8><style>{FONTS}{lastpage.CSS}</style>{body}")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=10000", f"--print-to-pdf={pdf}", f"file://{h}"], check=True, capture_output=True)
    src = os.path.join(ROOT, "public/pdf", f"{short}-{lang}.pdf")
    base = PdfReader(src)
    pages = list(base.pages)
    if "biblio.unilu.space/" in pages[-1].extract_text():
        pages = pages[:-1]   # an earlier version of the last page: replace it with the current one
    add = PdfReader(pdf)
    assert len(add.pages) == 1, f"the last page has {len(add.pages)} pages"
    w = PdfWriter()
    for p in pages: w.add_page(p)
    w.add_page(add.pages[0])
    w.write(src + ".new"); os.replace(src + ".new", src)
    mk = os.path.join(PIPE, "make_booklet.py")
    pub = os.path.join(ROOT, "public/pdf")
    subprocess.run([sys.executable, "-W", "ignore", mk, src, os.path.join(pub, f"{short}-{lang}-booklet.pdf")], check=True)
    subprocess.run([sys.executable, "-W", "ignore", mk, src, os.path.join(pub, f"{short}-{lang}-booklet-duplex.pdf"), "--fold"], check=True)
    subprocess.run([sys.executable, "-W", "ignore", os.path.join(PIPE, "make_a4.py"), src, os.path.join(pub, f"{short}-{lang}-a4.pdf")], check=True)
    print(lang, "done:", len(pages) + 1, "pages")
