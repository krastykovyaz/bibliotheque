#!/usr/bin/env python3
"""Subtitles, YouTube description and thumbnail, all from the real audio timing (<prefix>_audiobook_timing.json)."""
import json, math, os, re, subprocess, textwrap

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import book
B, BASE = book.load()
PIPE = book.PIPE
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
LEAD = 1.0  # the picture changes this many seconds before a new part is heard (same value as make_video.py)
LANG = os.environ.get("BOOK_LANG", "en")     # "ru": Russian description, subtitles and thumbnail, from the Russian voice script and timing (<prefix>_RU_...)
RU = LANG == "ru"
TAG = "_RU" if RU else ""
NAMES = B["ru"]["names"] if RU else B["names"]

MODE = os.environ.get("PKG_MODE", "all")      # "all", "text" (subtitles + description; no Chrome needed) or "thumb" (thumbnail only; needs no audio)
timing = None if MODE == "thumb" else json.load(open(os.path.join(BASE, f"{B['prefix']}{TAG}_audiobook_timing.json")))
rows = {} if MODE == "thumb" else {r["id"]: r for r in json.load(open(os.path.join(BASE, f"{B['prefix']}_voice_script{'_ru' if RU else ''}.json"), encoding="utf-8"))}


def stamp(t, comma=True):
    ms = int(round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}{',' if comma else '.'}{ms:03d}"


def chunks(text, limit=74):
    """Break a segment's text into pieces of at most `limit` characters, at sentence ends, then commas, then words."""
    text = re.sub(r"\s+", " ", text).strip()
    out = []
    for sent in re.split(r"(?<=[.!?…])[”’\"]?\s+", text):
        if len(sent) <= limit:
            out.append(sent); continue
        cur = ""
        for piece in re.split(r"(?<=[,;:—])\s+", sent):
            if len(cur) + len(piece) + 1 <= limit:
                cur = f"{cur} {piece}".strip()
            else:
                if cur: out.append(cur)
                while len(piece) > limit:
                    cut = piece.rfind(" ", 0, limit); out.append(piece[:cut]); piece = piece[cut + 1:]
                cur = piece
        if cur: out.append(cur)
    # glue very short leftovers (a quotation mark, a word) onto their neighbour
    merged = []
    for c in out:
        if merged and (len(c) < 14 or len(merged[-1]) < 14) and len(merged[-1]) + len(c) + 1 <= limit:
            merged[-1] += " " + c
        else:
            merged.append(c)
    return merged


if MODE != "thumb":
    # ------------------------------------------------------------------ SRT
    srt, n = [], 0
    for seg in timing["segments"]:
        text = rows[seg["id"]]["text"].strip()
        if not text:
            continue
        pieces = chunks(text)
        weights = [max(1, len(p)) for p in pieces]
        span = seg["end"] - seg["start"]
        t = seg["start"]
        for p, w in zip(pieces, weights):
            d = span * w / sum(weights)
            n += 1
            srt.append(f"{n}\n{stamp(t)} --> {stamp(t + d - 0.02)}\n" + "\n".join(textwrap.wrap(p, 42)) + "\n")
            t += d
    open(os.path.join(BASE, f"{B['prefix']}{TAG}.srt"), "w", encoding="utf-8").write("\n".join(srt))
    print("subtitles:", n, "entries; last ends at", stamp(timing["total"]))

    # ------------------------------------------------------------------ description with chapters
    total = timing["total"]
    mins = int(round(total / 60))
    chapters = []
    for i, p in enumerate(timing["parts"]):
        t = 0 if i == 0 else max(0, int(math.floor(p["start"] - LEAD)))
        h, r = divmod(t, 3600); m, s = divmod(r, 60)
        chapters.append(f"{h}:{m:02d}:{s:02d} " if h else f"{m:02d}:{s:02d} ")
        chapters[-1] += f"{'Часть' if RU else 'Part'} {p['part']}: {NAMES[p['part']]}"
    R = B.get("ru", {})
    desc = f"""{R['title']}. {R['author']}: аудиокнига для детей, сказка для совместного слушания, около {mins} мин.

    {R['description']}

    Главы
    {chr(10).join(chapters)}

    Слушайте и читайте вместе: иллюстрированное издание для чтения (PDF и книжка для печати) есть на сайте Bibliothèque.
    Текст сказки и PDF: https://biblio.unilu.space/ru/book/{B['slug']}/

    {R.get('hashtags', '#сказка #аудиокнига #длядетей')}
    """ if RU else f"""{B['title']} by {B['author']} ({B['year']}), a full-cast audiobook in English, about {mins} minutes.

    {B['summary']}

    Chapters
    {chr(10).join(chapters)}

    Listen with the text: the illustrated reading edition (A5 PDF and a printable A4 booklet) is available on the Bibliothèque site.
    Read the text and download the book (PDF): https://biblio.unilu.space/book/{B['slug']}/

    {B['hashtags']}
    """
    desc = "\n".join(l.lstrip() for l in desc.split("\n"))     # the text above is indented in the source: no line may start with a space (YouTube chapters need 00:00 at the start of a line)
    open(os.path.join(BASE, f"{B['prefix']}{TAG}_youtube_description.txt"), "w", encoding="utf-8").write(
        (f"TITLE\n{B['ru']['title']} | {B['ru']['author']} | Аудиокнига для детей\n\nDESCRIPTION\n" + desc +
         "\nTAGS\n" + ", ".join(B["ru"].get("tags", [])) + "\n\n"
         f"THUMBNAIL\n{B['prefix']}{TAG}_thumbnail.png (1280x720)\n\nNOTES FOR UPLOAD\nSet the video to Unlisted or Public in YouTube Studio after uploading; tick the altered or synthetic content disclosure (AI voice); mark it as made for kids.\n") if RU else
        (f"TITLE\n{B['title']} | {B['author']} | Full-Cast Audiobook (English)\n\nDESCRIPTION\n" + desc +
        "\nTAGS\n" + ", ".join(B["tags"]) + "\n\n"
        f"THUMBNAIL\n{B['prefix']}_thumbnail.png (1280x720)\n\nNOTES FOR UPLOAD\nSet the video to Unlisted or Public in YouTube Studio after uploading with the script; tick the altered or synthetic content disclosure (AI voices).\n"))
    print("description chapters:", chapters)


if MODE != "text":
    # ------------------------------------------------------------------ thumbnail 1280x720
    mins = int(round(timing["total"] / 60)) if timing else 0
    art = os.path.join(BASE, "video_assets", f"art_{B['thumb_art']}.png")
    CYR = f"""@font-face{{font-family:Lora;src:url(file://{PIPE}/fonts/lora-cyrillic-wght-normal.woff2) format("woff2");font-weight:400 700;unicode-range:U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116}}""" if RU else ""
    T_AUTHOR, T_TITLE = (B["ru"]["author"], B["ru"]["title"]) if RU else (B["author"], B["title"])
    T_SUB = (B["ru"].get("thumb_sub") or f"АУДИОКНИГА<br>{mins} МИН") if RU else (B["thumb_sub"] if B.get("thumb_sub") else f"FULL-CAST AUDIOBOOK<br>{mins} MIN")
    html = f"""<style>{CYR}
    @font-face{{font-family:Lora;src:url(file://{PIPE}/fonts/lora-latin-400-normal.woff2) format("woff2");font-weight:400}}
    @font-face{{font-family:Lora;src:url(file://{PIPE}/fonts/lora-latin-700-normal.woff2) format("woff2");font-weight:700}}
    html,body{{margin:0}}body{{width:1280px;height:720px;background:#171c3a;position:relative;overflow:hidden;font-family:Lora,serif}}
    .pic{{position:absolute;right:0;top:0;width:720px;height:720px;object-fit:cover;object-position:{B.get('thumb_position', '34% 50%')}}}
    .shade{{position:absolute;right:560px;top:0;width:160px;height:720px;background:linear-gradient(to right,#171c3a,rgba(23,28,58,0))}}
    .by{{position:absolute;left:64px;top:104px;font-size:27px;letter-spacing:.34em;color:#e3c27a}}
    .ti{{position:absolute;left:64px;top:170px;width:560px;font-size:70px;line-height:1.1;font-weight:700;color:#f4e8c8}}
    .sub{{position:absolute;left:64px;bottom:76px;font-size:24px;letter-spacing:.26em;color:#e3c27a;line-height:1.7}}
    .line{{position:absolute;left:64px;bottom:196px;width:120px;border-top:3px solid #c79a4a}}</style>
    <img class="pic" src="file://{art}"><div class="shade"></div>
    <div class="by">{T_AUTHOR.upper()}</div><div class="ti">{T_TITLE}</div><div class="line"></div>
    <div class="sub">{T_SUB}</div>"""
    THUMB = os.path.join(BASE, f"{B['prefix']}{TAG}_thumbnail.png")
    tmp = os.path.join(BASE, "_thumb.html")
    open(tmp, "w", encoding="utf-8").write(html)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1", "--virtual-time-budget=8000",
                    f"--screenshot={THUMB}", "--window-size=1280,720", f"file://{tmp}"], check=True, capture_output=True)
    os.remove(tmp)
    print("thumbnail written")
