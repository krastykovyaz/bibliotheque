#!/usr/bin/env python3
"""Builds book.html from translation_en.json and prints it to an A5 PDF with headless Chrome.
Runs twice: the first pass finds the page of every part, the second puts those numbers in the contents."""
import json, subprocess, sys, html, os, re
import pymupdf

BASE = os.path.dirname(os.path.abspath(__file__))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
TITLE, AUTHOR = "How Much Land Does a Man Need?", "Leo Tolstoy"
OUT_PDF = os.path.join(BASE, "How_Much_Land_A5_reading.pdf")

T = json.load(open(os.path.join(BASE, "translation_en.json"), encoding="utf-8"))
PARTS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]
NAMES = {"I": "Two Sisters", "II": "Land of His Own", "III": "Cramped", "IV": "A Thousand Roubles", "V": "The Bashkirs",
         "VI": "The Price of a Day", "VII": "The Dream", "VIII": "The Long Walk", "IX": "Sunset"}
# one illustration at the start of each group of parts
ART = {"I": "1_hut", "III": "2_river", "V": "3_camp", "VII": "4_dawn", "IX": "5_sunset"}
ALT = {"1_hut": "A lit peasant hut at night, smoke curling from the chimney",
       "2_river": "A paddle steamer on the Volga at sunrise, rye sheaves on the bank",
       "3_camp": "Felt tents and horses on the steppe at sunset",
       "4_dawn": "Dawn over the steppe, a low hill far away and marks in the grass",
       "5_sunset": "The sun going down behind the hill, a spade planted in the ground"}

GLOSSARY = [
    ("desyatina", "a Russian measure of land, about 1.09 hectares (2.7 acres)."),
    ("verst", "a Russian measure of distance, about 1.07 kilometres (two thirds of a mile)."),
    ("arshin", "a Russian measure of length, about 71 centimetres (28 inches)."),
    ("commune", "the village assembly (<i>mir</i>) that held the land and decided who could settle."),
    ("the red cock", "a peasant expression for setting a house on fire."),
    ("kumis", "fermented mare’s milk, a drink of the steppe peoples."),
    ("shikhan", "a small hill, in the Bashkir language."),
    ("rouble, kopeck", "Russian money; a rouble is a hundred kopecks."),
]

CSS = """
@font-face{font-family:Lora;src:url(fonts/lora-latin-400-normal.woff2) format("woff2");font-weight:400;font-style:normal;unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:Lora;src:url(fonts/lora-latin-600-normal.woff2) format("woff2");font-weight:600;font-style:normal;unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:Lora;src:url(fonts/lora-latin-700-normal.woff2) format("woff2");font-weight:700;font-style:normal;unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:Lora;src:url(fonts/lora-latin-400-italic.woff2) format("woff2");font-weight:400;font-style:italic;unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD}
@font-face{font-family:Lora;src:url(fonts/lora-cyrillic-400-normal.woff2) format("woff2");font-weight:400;font-style:normal;unicode-range:U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116}
@page{size:148mm 210mm;margin:17mm 15mm 21mm 15mm;
  @bottom-center{content:counter(page);font-family:Lora;font-size:9pt;color:#8a7762}}
@page cover{margin:0;@bottom-center{content:none}}
@page front{@bottom-center{content:none}}
*{box-sizing:border-box}
html{font-family:Lora,Georgia,serif;font-size:__FS__pt;line-height:__LH__;color:#2a211c;hyphens:auto;-webkit-hyphens:auto}
body{margin:0}
.cover{page:cover;break-after:page;width:148mm;height:210mm;position:relative;
  background:linear-gradient(to bottom,#171c3a 0,#171c3a 50%,#77552b 50%,#77552b 100%)}
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
.part h2{margin:0 0 5mm;text-align:center;break-after:avoid;font-weight:400}
.part h2 .num{display:block;font-size:22pt;line-height:1;color:#9c4a2e;font-weight:600;letter-spacing:.06em}
.part h2 .name{display:block;font-size:9.5pt;letter-spacing:.2em;text-transform:uppercase;color:#6b5a4a;margin-top:2mm}
.part p{margin:0;text-align:justify;text-indent:1.35em;orphans:3;widows:3}
.part p.first{text-indent:0}
.part p.first::first-letter{float:left;font-size:3.5em;line-height:.82;padding:.05em .09em 0 0;color:#9c4a2e;font-weight:600}
.back{page:front;break-before:page;padding-top:14mm}
.back h2{font-size:13pt;letter-spacing:.2em;text-transform:uppercase;text-align:center;font-weight:600;color:#1d2340;margin:0 0 9mm}
.back dl{margin:0;font-size:9.4pt;line-height:1.45}.back dt{font-weight:600;float:left;clear:left;width:30mm}.back dd{margin:0 0 2.6mm 32mm}
.back .small{margin-top:10mm;font-size:8.4pt;line-height:1.5;color:#6b5a4a;text-align:left}
"""


FS = os.environ.get("BOOK_FS", "10.6")
LH = os.environ.get("BOOK_LH", "1.54")


def page_html(page_numbers):
    toc = "".join(
        f'<li><span class="n">{p}</span><span class="t">{html.escape(NAMES[p])}</span><span class="d"></span><span class="p">{page_numbers.get(p, "")}</span></li>'
        for p in PARTS)
    parts = []
    for p in PARTS:
        start = p in ART
        fig = (f'<figure><img src="art/png/{ART[p]}.png" alt="{html.escape(ALT[ART[p]])}"></figure>' if start else "")
        ps = [f'<p class="{"first" if i == 0 else ""}">{html.escape(t)}</p>' for i, t in enumerate(T[p])]
        first, rest = ps[0], "".join(ps[1:])
        head = f'<h2><span class="num">{p}</span><span class="name">{html.escape(NAMES[p])}</span></h2>'
        # illustrated parts begin at the top of a page, so their first paragraph may run on; the others keep heading and first paragraph together
        body = (head + first + rest) if start else (f'<div class="opening">{head}{first}</div>' + rest)
        parts.append(f'<section class="part{" start" if start else ""}" id="part-{p}">{fig}{body}</section>')
    gloss = "".join(f"<dt>{html.escape(k)}</dt><dd>{v}</dd>" for k, v in GLOSSARY)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{TITLE}</title><style>{CSS.replace('__FS__', FS).replace('__LH__', LH)}</style></head><body>
<section class="cover"><img src="art/png/cover_print.png" alt="Cover: {TITLE}"></section>
<section class="titlepage"><div class="by">{AUTHOR.upper()}</div><h1>{TITLE}</h1><div class="rule"></div><div class="rule s"></div>
<p class="note">Draft English translation from the Russian text supplied. Machine draft, checked once against the original: needs a human editor before publication.</p>
<p class="src">Original: «Много ли человеку земли нужно», 1886. Text from ru.wikisource.org, after L. N. Tolstoy, Collected Works in 22 volumes, Moscow, 1982, vol. 10.</p></section>
<section class="toc"><h2>Contents</h2><ol>{toc}</ol></section>
{''.join(parts)}
<section class="back"><h2>Notes</h2><dl>{gloss}</dl>
<p class="small">The text of the story is in the public domain. The translation is a machine draft and may contain mistakes. The part titles and the illustrations are original to this edition. Typeset in Lora (SIL Open Font License).</p></section>
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
                    if t in PARTS and s["size"] > 18 and t not in found:
                        found[t] = i + 1
    return found, len(doc)


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
