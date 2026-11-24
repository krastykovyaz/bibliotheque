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
NAMES = B["names"]

timing = json.load(open(os.path.join(BASE, f"{B['prefix']}_audiobook_timing.json")))
rows = {r["id"]: r for r in json.load(open(os.path.join(BASE, f"{B['prefix']}_voice_script.json"), encoding="utf-8"))}


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
open(os.path.join(BASE, f"{B['prefix']}.srt"), "w", encoding="utf-8").write("\n".join(srt))
print("subtitles:", n, "entries; last ends at", stamp(timing["total"]))

# ------------------------------------------------------------------ description with chapters
total = timing["total"]
mins = int(round(total / 60))
chapters = []
for i, p in enumerate(timing["parts"]):
    t = 0 if i == 0 else max(0, int(math.floor(p["start"] - LEAD)))
    h, r = divmod(t, 3600); m, s = divmod(r, 60)
    chapters.append(f"{h}:{m:02d}:{s:02d} " if h else f"{m:02d}:{s:02d} ")
    chapters[-1] += f"Part {p['part']}: {NAMES[p['part']]}"
desc = f"""{B['title']} by {B['author']} ({B['year']}), a full-cast audiobook in English, about {mins} minutes.

{B['summary']}

Chapters
{chr(10).join(chapters)}

The voices and the translation are made with AI. The English translation is a machine draft made from {B.get('translated_from', 'the original')} and may contain mistakes. The text is in the public domain. Original: «{B['title_original']}», {B.get('publication_note', 'first published ' + str(B['year']))}.

Listen with the text: the illustrated reading edition (A5 PDF and a printable A4 booklet) is available on the Bibliothèque site.
Read the text and download the book (PDF): https://biblio.unilu.space/book/{B['slug']}/

{B['hashtags']}
"""
open(os.path.join(BASE, f"{B['prefix']}_youtube_description.txt"), "w", encoding="utf-8").write(
    f"TITLE\n{B['title']} | {B['author']} | Full-Cast Audiobook (English)\n\nDESCRIPTION\n" + desc +
    "\nTAGS\n" + ", ".join(B["tags"]) + "\n\n"
    f"THUMBNAIL\n{B['prefix']}_thumbnail.png (1280x720)\n\nNOTES FOR UPLOAD\nSet the video to Unlisted or Public in YouTube Studio after uploading with the script; tick the altered or synthetic content disclosure (AI voices).\n")
print("description chapters:", chapters)

# ------------------------------------------------------------------ thumbnail 1280x720
art = os.path.join(BASE, "video_assets", f"art_{B['thumb_art']}.png")
html = f"""<style>
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
<div class="by">{B['author'].upper()}</div><div class="ti">{B['title']}</div><div class="line"></div>
<div class="sub">FULL-CAST AUDIOBOOK<br>{mins} MIN</div>"""
THUMB = os.path.join(BASE, f"{B['prefix']}_thumbnail.png")
tmp = os.path.join(BASE, "_thumb.html")
open(tmp, "w", encoding="utf-8").write(html)
subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1", "--virtual-time-budget=8000",
                f"--screenshot={THUMB}", "--window-size=1280,720", f"file://{tmp}"], check=True, capture_output=True)
os.remove(tmp)
print("thumbnail written")
