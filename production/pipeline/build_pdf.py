#!/usr/bin/env python3
"""Builds book.html from translation_en.json and prints it to an A5 PDF with headless Chrome.
Runs twice: the first pass finds the page of every part, the second puts those numbers in the contents."""
import json, subprocess, sys, html, os, re
import pymupdf

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import book, lastpage
B, BASE = book.load()
PIPE = book.PIPE
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
LANG = os.environ.get("BOOK_LANG", "en")      # "en": the English translation; "ru": the Russian original (source_clean.json)
R = B.get("ru", {}) if LANG == "ru" else {}
TITLE, AUTHOR = R.get("title", B["title"]), R.get("author", B["author"])
OUT_PDF = os.path.join(BASE, f"{B['prefix']}_A5_reading{'_ru' if LANG == 'ru' else ''}.pdf")

if LANG == "ru":
    T = {x["part"]: x["paragraphs"] for x in json.load(open(os.path.join(BASE, "source_clean.json"), encoding="utf-8"))}
else:
    T = json.load(open(os.path.join(BASE, "translation_en.json"), encoding="utf-8"))
PARTS, NAMES, ART, ALT = B["parts"], R.get("names", B["names"]), B["art"], B["art_alt"]
GLOSSARY = [tuple(g) for g in B["glossary"]] if LANG != "ru" else []
COVER = "cover_ru" if LANG == "ru" else "cover"

CSS = """
@font-face{font-family:Lora;src:url(__FONTS__/lora-latin-400-normal.woff2) format("woff2");font-weight:400;font-style:normal;unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:Lora;src:url(__FONTS__/lora-latin-600-normal.woff2) format("woff2");font-weight:600;font-style:normal;unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:Lora;src:url(__FONTS__/lora-latin-700-normal.woff2) format("woff2");font-weight:700;font-style:normal;unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:Lora;src:url(__FONTS__/lora-latin-400-italic.woff2) format("woff2");font-weight:400;font-style:italic;unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:Lora;src:url(__FONTS__/lora-cyrillic-400-normal.woff2) format("woff2");font-weight:400;font-style:normal;unicode-range:U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116}
__RUFONTS__
@page{size:148mm 210mm;margin:17mm 15mm 21mm 15mm;
  @bottom-center{content:counter(page);font-family:Lora;font-size:9pt;color:#8a7762}}
@page cover{margin:0;@bottom-center{content:none}}
@page front{@bottom-center{content:none}}
*{box-sizing:border-box}
html{font-family:Lora,Georgia,serif;font-size:__FS__pt;line-height:__LH__;color:#2a211c;hyphens:auto;-webkit-hyphens:auto}
body{margin:0}
.cover{page:cover;break-after:page;width:148mm;height:210mm;position:relative;
  background:linear-gradient(to bottom,__C1__ 0,__C1__ 50%,__C2__ 50%,__C2__ 100%)}
.cover img{position:absolute;left:0;top:31mm;width:148mm;height:148mm;display:block}
.titlepage{page:front;break-after:page;text-align:center;padding-top:34mm}
.titlepage .by{letter-spacing:.32em;font-size:9.5pt;color:#9c4a2e;margin-bottom:12mm}
.titlepage h1{font-size:25pt;line-height:1.14;margin:0 8mm 10mm;font-weight:700;color:#1d2340}
.rule{width:34mm;border-top:1.2pt solid #c79a4a;margin:0 auto 1.6mm}.rule.s{width:20mm;border-top-width:.7pt}
.titlepage .note{margin:22mm 6mm 0;font-size:8.8pt;line-height:1.5;color:#5c4a3d;font-style:italic}
.titlepage .src{margin:7mm 6mm 0;font-size:8pt;line-height:1.45;color:#7a6a58}
.toc{page:front;break-after:page;padding-top:12mm}
.toc h2{font-size:15pt;letter-spacing:.2em;text-transform:uppercase;text-align:center;font-weight:600;color:#1d2340;margin:0 0 12mm}
.toc ol{list-style:none;margin:0;padding:0}
.toc li{display:flex;align-items:baseline;margin:0 0 3.3mm;font-size:10.6pt}
.toc .n{width:12mm;color:#9c4a2e;font-weight:600}.toc .t{flex:0 0 auto}.toc .d{flex:1;border-bottom:1pt dotted #b9a98f;margin:0 2mm;transform:translateY(-1.2mm)}
.toc .p{flex:0 0 auto;color:#5c4a3d}
.part{break-inside:auto}
.opening{break-inside:avoid}
.part.start{break-before:page}
.part:not(.start){margin-top:9mm}
figure{margin:0 0 7mm;break-inside:avoid}
figure img{display:block;width:100%;height:auto}
figure.inline{margin:5mm 0;padding:1.5mm;border:.35mm solid #d9c9a8;border-radius:1mm}
figure.inline img{border-radius:.6mm}
figure.inline figcaption{font-style:italic;font-size:8.5pt;line-height:1.25;text-align:center;color:#6b5a4a;margin:1.6mm 1mm 0}
.part h2{margin:0 0 5mm;text-align:center;break-after:avoid;font-weight:400}
.part h2 .num{display:block;font-size:22pt;line-height:1;color:#9c4a2e;font-weight:600;letter-spacing:.06em}
.part h2 .name{display:block;font-size:9.5pt;letter-spacing:.2em;text-transform:uppercase;color:#6b5a4a;margin-top:2mm}
.part p{margin:0;text-align:justify;text-indent:1.35em;orphans:3;widows:3}
.part p.first{text-indent:0}
.part p.lh{text-indent:0;text-align:center;font-size:8.6pt;letter-spacing:.2em;text-transform:uppercase;color:#6b5a4a;margin:5mm 0 2.5mm;break-after:avoid;orphans:2;widows:2}
.part p.first::first-letter{float:left;font-size:3.5em;line-height:.82;padding:.05em .09em 0 0;color:#9c4a2e;font-weight:600}
.back{page:front;break-before:page;padding-top:14mm}
.back h2{font-size:13pt;letter-spacing:.2em;text-transform:uppercase;text-align:center;font-weight:600;color:#1d2340;margin:0 0 9mm}
.back dl{margin:0;font-size:9.4pt;line-height:1.45}.back dt{font-weight:600;float:left;clear:left;width:30mm}.back dd{margin:0 0 2.6mm 32mm}
.back .small{margin-top:10mm;font-size:8.4pt;line-height:1.5;color:#6b5a4a;text-align:left}
"""


RUFONTS = ("@font-face{font-family:Lora;src:url(__FONTS__/lora-cyrillic-wght-normal.woff2) format('woff2');font-weight:400 700;font-style:normal;unicode-range:U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116}"
           "@font-face{font-family:Lora;src:url(__FONTS__/lora-cyrillic-wght-italic.woff2) format('woff2');font-weight:400 700;font-style:italic;unicode-range:U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116}") if LANG == "ru" else ""
CSS = CSS.replace("__RUFONTS__", RUFONTS)
if LANG == "ru":   # the static Cyrillic regular is replaced by the variable face above, which has the bold weights too
    CSS = "\n".join(l for l in CSS.split("\n") if "lora-cyrillic-400-normal" not in l)
    # Latin letters, digits and punctuation come from a second family, so that none of them falls back to a system font
    CSS = "\n".join(l.replace("font-family:Lora;", "font-family:LoraL;") if "lora-latin" in l else l for l in CSS.split("\n"))
    CSS = CSS.replace("font-family:Lora,Georgia,serif", "font-family:Lora,LoraL,serif")
FS = os.environ.get("BOOK_FS", "10.6")
LH = os.environ.get("BOOK_LH", "1.54")


CREDITS = (R["source_note"] + " Текст находится в общественном достоянии. Набрано шрифтом Lora (SIL Open Font License)." if R else
           B["source_note"] + " The text is in the public domain. English translation: machine draft. Typeset in Lora (SIL Open Font License).")
COMPACT = False
BACK = lastpage.section(LANG, B["slug"], B["title"], GLOSSARY, CREDITS)
CSS += lastpage.CSS


def page_html(page_numbers):
    toc = "".join(
        f'<li><span class="n">{p}</span><span class="t">{html.escape(NAMES[p])}</span><span class="d"></span><span class="p">{page_numbers.get(p, "")}</span></li>'
        for p in PARTS)
    parts = []
    for p in PARTS:
        start = p in ART
        fig = (f'<figure><img src="art/png/{ART[p]}.png" alt="{html.escape(ALT[ART[p]])}"></figure>' if start else "")
        ps, seen, n = [], False, 0
        # book.json "figures": [{"part": "I", "after": 3, "art": "name", "caption": "...", "caption_ru": "..."}] puts art/png/<name>.png, framed and captioned,
        # after the 3rd paragraph of that part (children's books want a picture about every 300-400 words)
        figs = {}
        for f in B.get("figures", []):
            if f["part"] == p:
                figs.setdefault(f["after"], []).append(f)
        for t in T[p]:
            if t.startswith("§ "):       # a letter heading (its date) or a section marker
                ps.append(f'<p class="lh">{html.escape(t[2:])}</p>')
            else:
                ps.append(f'<p class="{"" if seen else "first"}">{html.escape(t)}</p>'); seen = True
                n += 1
                for f in figs.get(n, []):
                    cap = (f.get("caption_ru") if LANG == "ru" else None) or f.get("caption", "")
                    alt = html.escape(ALT.get(f["art"], cap))
                    ps.append(f'<figure class="inline"><img src="art/png/{f["art"]}.png" alt="{alt}">' + (f"<figcaption>{html.escape(cap)}</figcaption>" if cap else "") + "</figure>")
        k = next(i for i, x in enumerate(ps) if "lh" not in x[:12])        # the opening block: heading, and the paragraph that follows the letter heading
        first, rest = "".join(ps[:k + 1]), "".join(ps[k + 1:])
        head = f'<h2><span class="num">{p}</span><span class="name">{html.escape(NAMES[p])}</span></h2>'
        # illustrated parts begin at the top of a page, so their first paragraph may run on; the others keep heading and first paragraph together
        body = (head + first + rest) if start else (f'<div class="opening">{head}{first}</div>' + rest)
        parts.append(f'<section class="part{" start" if start else ""}" id="part-{p}">{fig}{body}</section>')
    gloss = "".join(f"<dt>{html.escape(k)}</dt><dd>{v}</dd>" for k, v in GLOSSARY)
    return f"""<!doctype html><html lang="{LANG}"><head><meta charset="utf-8"><title>{TITLE}</title><style>{CSS.replace('__C1__', B.get('cover_bg', ['#171c3a', '#77552b'])[0]).replace('__C2__', B.get('cover_bg', ['#171c3a', '#77552b'])[1]).replace('__FS__', FS).replace('__LH__', LH).replace('__FONTS__', 'file://' + os.path.join(PIPE, 'fonts'))}</style></head><body>
<section class="cover"><img src="art/png/{COVER}_print.png" alt="{TITLE}"></section>
<section class="titlepage"><div class="by">{AUTHOR.upper()}</div><h1>{TITLE}</h1><div class="rule"></div><div class="rule s"></div>
<p class="note">{html.escape(R["note"]) if R else "Draft English translation from the Russian text supplied. Machine draft, checked once against the original: needs a human editor before publication."}</p>
<p class="src">{html.escape(R["source_note"]) if R else "Original: «" + B['title_original'] + "», " + str(B['year']) + ". " + B['source_note']}</p></section>
<section class="toc"><h2>{R.get("contents", "Contents")}</h2><ol>{toc}</ol></section>
{''.join(parts)}
{BACK}
</body></html>"""


def render(page_numbers):
    html_path = os.path.join(BASE, "book.html")
    open(html_path, "w", encoding="utf-8").write(page_html(page_numbers))
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=15000",
                    f"--print-to-pdf={OUT_PDF}", f"file://{html_path}"], check=True, capture_output=True)


def find_pages():
    """Page number (as printed, = PDF page) where each part heading starts: a big roman numeral span."""
    doc = pymupdf.open(OUT_PDF)
    found = {}
    for i, page in enumerate(doc):
        if i < 3:
            continue
        for b in page.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                for s in l["spans"]:
                    t = s["text"].strip()
                    if t in PARTS and 18 < s["size"] < 30 and t not in found:
                        found[t] = i + 1
    return found, len(doc)


_cp = os.path.join(BASE, f"art/png/{COVER}_print.png")
if not os.path.exists(_cp):
    from PIL import Image
    Image.open(os.path.join(BASE, f"art/png/{COVER}.png")).convert("RGB").resize((1800, 1800), Image.LANCZOS).save(_cp, optimize=True)
render({})
pages, n1 = find_pages()
render(pages)
pages2, n2 = find_pages()
print("pages:", n2, "| parts start on:", pages2)
if pages != pages2 or n1 != n2:
    print("page numbers moved between passes, rendering once more")
    render(pages2)
    pages3, n3 = find_pages()
    print("pages:", n3, "| parts start on:", pages3, "| stable" if pages3 == pages2 else "| STILL MOVING")


def last_page_overflows():
    """True when the last page (the one with the QR codes and 'Next on the shelf') spills onto a second page."""
    doc = pymupdf.open(OUT_PDF)
    key = lastpage.T[LANG]["listen"].upper().replace(" ", "")
    for i in range(len(doc) - 1, -1, -1):
        if key in doc[i].get_text().upper().replace(" ", "").replace("\n", ""):
            return i != len(doc) - 1
    return False


for level in (1, 2):
    if not last_page_overflows():
        break
    print(f"the last page spills over: building it again in the tighter layout (level {level})")
    BACK = lastpage.section(LANG, B["slug"], B["title"], GLOSSARY, CREDITS, compact=level)
    render(pages2)
    print("last page fits now" if not last_page_overflows() else "WARNING: the last page still spills over")
