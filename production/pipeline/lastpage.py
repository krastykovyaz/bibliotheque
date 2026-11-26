"""The last page of every reading PDF: notes (glossary), "Listen to this book" with QR codes (the video and the book page on the
site), credits, and "Next on the shelf". Used by build_pdf.py (as the back section) and add_last_page.py (as a page appended to a
PDF we did not build). Needs the `qrcode` package (in the pipeline venv)."""
import base64, io, json, html, os
import qrcode

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SITE = "https://biblio.unilu.space"
T = {
    "en": {"notes": "Notes", "listen": "Listen to this book", "watch": "Watch and listen", "read": "Read online, download", "next": "Next on the shelf"},
    "ru": {"notes": "О тексте", "listen": "Читать и слушать", "watch": "Смотреть и слушать", "read": "Читать онлайн, скачать", "next": "Скоро на полке"},
}
CSS = """
.back{page:notes;break-before:page;position:relative;box-sizing:border-box;height:209.4mm;padding:21mm 20mm 17mm;border:.35mm solid #d9c9a8;border-radius:1mm}
@page notes{margin:0;@bottom-center{content:none}}
.back h2{font-size:13pt;letter-spacing:.2em;text-transform:uppercase;text-align:center;font-weight:600;color:#1d2340;margin:0 0 5mm}
.qr{margin:0 0 6mm;break-inside:avoid}
.qr .row{display:flex;gap:6mm;justify-content:center}.qr .item{text-align:center;width:52mm}
.qr .item:only-child{width:100%}.qr .item img{width:26mm;height:26mm;display:block;margin:0 auto 1.5mm}
.qr .item b{display:block;font-size:9pt;color:#1d2340}.qr .item span{display:block;line-height:1.3;font-size:7.4pt;color:#6b5a4a;word-break:normal;overflow-wrap:anywhere}
.back dl{margin:0;font-size:8.2pt;line-height:1.3;display:grid;grid-template-columns:28mm 1fr;column-gap:2.5mm;row-gap:1.2mm}.back dt{font-weight:600;overflow-wrap:anywhere}.back dd{margin:0}
.back .credits{margin-top:3mm;font-size:7.6pt;line-height:1.4;color:#6b5a4a;text-align:left}
.back .next{margin-top:6mm;border-top:.8pt solid #c79a4a;padding-top:4mm;text-align:center}
.back .next small{display:block;letter-spacing:.2em;font-size:7.6pt;text-transform:uppercase;color:#9c4a2e}
.back .next i{font-size:12pt;color:#1d2340}.back .next em{display:block;font-size:8.6pt;color:#6b5a4a;margin-top:1mm}
"""


def qr_png(url):
    q = qrcode.QRCode(border=0, box_size=10)
    q.add_data(url); q.make(fit=True)
    b = io.BytesIO(); q.make_image(fill_color="#1d2340", back_color="white").save(b, format="PNG")
    return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()


def site_info(slug, lang):
    """(video url or None, book page url) for a book, from data/books.json (the video is None until it has a real link)."""
    video = None
    try:
        for b in json.load(open(os.path.join(ROOT, "data/books.json"), encoding="utf-8")):
            if b["id"] == slug:
                l = b["languages"].get(lang) or {}
                y = l.get("playlist") or l.get("youtube", "")
                if y and "PLACEHOLDER" not in y:
                    video = y
    except OSError:
        pass
    return video, f"{SITE}{'/ru' if lang == 'ru' else ''}/book/{slug}/"


def next_book(title_en, lang):
    try:
        for it in json.load(open(os.path.join(ROOT, "data/queue.json"), encoding="utf-8"))["items"]:
            if it["title_en"].strip().lower() != title_en.strip().lower():
                return (it["title_ru"], it["author_ru"]) if lang == "ru" else (it["title_en"], it["author_en"])
    except OSError:
        pass
    return None


def section(lang, slug, title_en, glossary, credits, compact=False):
    t = T[lang]
    video, book_url = site_info(slug, lang)
    items = []
    if video:
        items.append((t["watch"], video))
    items.append((t["read"], book_url))
    shown = lambda u: html.escape(u.replace("https://www.", "").replace("https://", "").rstrip("/"))
    row = "".join(f'<div class="item"><img src="{qr_png(u)}" alt=""><b>{html.escape(lbl)}</b><span>{shown(u)}</span></div>' for lbl, u in items)
    gl = "".join(f"<dt>{html.escape(k)}</dt><dd>{v}</dd>" for k, v in glossary)
    nb = next_book(title_en, lang)
    nxt = f'<div class="next"><small>{t["next"]}</small><i>{html.escape(nb[0])}</i><em>{html.escape(nb[1])} · biblio.unilu.space</em></div>' if nb else ""
    cls = " compact tight" if compact == 2 else " compact" if compact else ""
    return (f'<section class="back{cls}"><h2>{t["notes"]}</h2><div class="qr"><div class="row">{row}</div></div>'
            f'<dl>{gl}</dl><p class="credits">{html.escape(credits)}</p>{nxt}</section>')

# when the page still overflows, build_pdf asks for this tighter variant
CSS += """
.back.compact h2{margin-bottom:3mm}.back.compact .qr{margin-bottom:3mm}.back.compact .qr .item img{width:21mm;height:21mm}
.back.compact dl{font-size:7.4pt;line-height:1.22;row-gap:.8mm}.back.compact .credits{font-size:7pt;margin-top:2mm}.back.compact .next{margin-top:3mm;padding-top:2mm}
.back.tight h2{margin-bottom:2mm}.back.tight .qr{margin-bottom:2mm}.back.tight .qr .item img{width:18mm;height:18mm}
.back.tight dl{font-size:6.8pt;line-height:1.15;row-gap:.4mm}.back.tight .credits{font-size:6.4pt;margin-top:1.5mm}.back.tight .next{margin-top:2mm;padding-top:1.5mm}
"""
