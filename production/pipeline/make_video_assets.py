#!/usr/bin/env python3
"""Renders the still images the video needs, with headless Chrome (so the Lora font is used):
  video_assets/art_*.png     the five illustrations at 3840x2160 (room to pan and zoom)
  video_assets/strip_*.png   the thin gold line and the small label under the picture, 1920x90
  video_assets/title_card.png  the cover, centred, 1920x1080"""
import os, subprocess

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import book
B, BASE = book.load()
PIPE = book.PIPE
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT = os.path.join(BASE, "video_assets")
os.makedirs(OUT, exist_ok=True)
NAMES = B["names"]
FONTS = f"""
@font-face{{font-family:Lora;src:url(file://{PIPE}/fonts/lora-latin-400-normal.woff2) format("woff2");font-weight:400}}
@font-face{{font-family:Lora;src:url(file://{PIPE}/fonts/lora-latin-600-normal.woff2) format("woff2");font-weight:600}}
"""


def shot(html, png, w, h):
    path = os.path.join(OUT, "_tmp.html")
    open(path, "w", encoding="utf-8").write(html)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--virtual-time-budget=8000", f"--screenshot={png}", f"--window-size={w},{h}", f"file://{path}"],
                   check=True, capture_output=True)


for n in sorted(set(B["art"].values())):
    shot(f'<style>html,body{{margin:0;background:#000}}img{{display:block;width:3840px;height:2160px}}</style>'
         f'<img src="file://{BASE}/art/{n}.svg">', os.path.join(OUT, f"art_{n}.png"), 3840, 2160)

for p, name in NAMES.items():
    label = f"PART {p} · {name.upper()}"
    shot(f"""<style>{FONTS}html,body{{margin:0}}body{{width:1920px;height:90px;background:#171c3a;position:relative;overflow:hidden}}
.line{{position:absolute;left:810px;width:300px;top:14px;border-top:2px solid #c79a4a}}
.t{{position:absolute;left:0;right:0;top:30px;text-align:center;font:400 27px Lora,serif;letter-spacing:.3em;color:#e3c27a}}</style>
<div class="line"></div><div class="t">{label}</div>""", os.path.join(OUT, f"strip_{p}.png"), 1920, 90)

# title card: the cover in the middle, its own blurred and darkened copy filling the sides (no hard seam)
shot(f"""<style>html,body{{margin:0}}body{{width:1920px;height:1080px;background:#171c3a;position:relative;overflow:hidden}}
.bg{{position:absolute;left:-240px;top:-620px;width:2400px;height:2400px;filter:blur(46px) brightness(.72);display:block}}
.fg{{position:absolute;left:420px;top:0;width:1080px;height:1080px;display:block}}</style>
<img class="bg" src="file://{BASE}/art/png/cover.png"><img class="fg" src="file://{BASE}/art/png/cover.png">""", os.path.join(OUT, "title_card.png"), 1920, 1080)
os.remove(os.path.join(OUT, "_tmp.html"))
print(sorted(os.listdir(OUT)))
