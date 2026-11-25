#!/usr/bin/env python3
"""A 1280x720 thumbnail for every episode in book.json ("episodes"): the picture on the right, title, 'PART n OF N' and the topic on the left."""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import book
B, BASE = book.load()
PIPE = book.PIPE
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
N = len(B["episodes"])
for i, ep in enumerate(B["episodes"], 1):
    art = os.path.join(BASE, "video_assets", f"art_{ep['thumb_art']}.png")
    focus = B["focus"].get(ep["thumb_art"], [[0.5, 0.5]])[0]
    html = f"""<style>
@font-face{{font-family:Lora;src:url(file://{PIPE}/fonts/lora-latin-400-normal.woff2) format("woff2");font-weight:400}}
@font-face{{font-family:Lora;src:url(file://{PIPE}/fonts/lora-latin-700-normal.woff2) format("woff2");font-weight:700}}
html,body{{margin:0}}body{{width:1280px;height:720px;background:#171c3a;position:relative;overflow:hidden;font-family:Lora,serif}}
.pic{{position:absolute;right:0;top:0;width:720px;height:720px;object-fit:cover;object-position:{int(focus[0]*100)}% 50%}}
.shade{{position:absolute;right:560px;top:0;width:160px;height:720px;background:linear-gradient(to right,#171c3a,rgba(23,28,58,0))}}
.by{{position:absolute;left:64px;top:70px;font-size:25px;letter-spacing:.34em;color:#e3c27a}}
.ti{{position:absolute;left:64px;top:120px;width:560px;font-size:{76 if len(B["title"]) < 14 else 56}px;line-height:1.1;font-weight:700;color:#f4e8c8}}
.part{{position:absolute;left:64px;top:300px;font-size:30px;letter-spacing:.28em;color:#e3c27a}}
.topic{{position:absolute;left:64px;top:360px;width:540px;font-size:42px;line-height:1.2;color:#f4e8c8}}
.line{{position:absolute;left:64px;top:280px;width:120px;border-top:3px solid #c79a4a}}
.sub{{position:absolute;left:64px;bottom:60px;font-size:22px;letter-spacing:.26em;color:#e3c27a;line-height:1.7}}</style>
<img class="pic" src="file://{art}"><div class="shade"></div>
<div class="by">{B["author"].upper()}</div><div class="ti">{B["title"]}</div><div class="line"></div>
<div class="part">PART {i} OF {N}</div><div class="topic">{ep['title']}</div>
<div class="sub">FULL-CAST AUDIOBOOK</div>"""
    tmp = os.path.join(BASE, "_ep.html")
    open(tmp, "w", encoding="utf-8").write(html)
    out = os.path.join(BASE, f"{B['prefix']}_EP{i}_thumbnail.png")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1", "--virtual-time-budget=8000",
                    f"--screenshot={out}", "--window-size=1280,720", f"file://{tmp}"], check=True, capture_output=True)
    os.remove(tmp)
    print("wrote", out)
