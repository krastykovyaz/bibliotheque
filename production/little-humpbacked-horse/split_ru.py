#!/usr/bin/env python3
"""Russian version of pipeline/split_episodes.py: cuts <Prefix>_RU_YouTube.mp4 into the episodes of book.json (parts, or from_paragraph / to_paragraph inside a part),
with Russian titles, chapters and descriptions. Runs ON aak-llm in the book folder after chain_ru.sh has rendered the video (BOOK_DIR, BOOK_LANG=ru).
Output: <Prefix>_RU_EP<n>.mp4 and <Prefix>_RU_EP<n>_youtube_description.txt"""
import json, os, subprocess
BASE = os.environ.get("BOOK_DIR", os.getcwd())
B = json.load(open(os.path.join(BASE, "book.json"), encoding="utf-8")); P = B["prefix"]; R = B["ru"]; LEAD = 1.0
timing = json.load(open(os.path.join(BASE, f"{P}_RU_audiobook_timing.json")))
seg = {s["id"]: s["start"] for s in timing["segments"]}
rows = json.load(open(os.path.join(BASE, f"{P}_voice_script_ru.json"), encoding="utf-8"))
order = list(dict.fromkeys(r["part"] for r in rows))
def pstart(part, par=None):
    rid = next(r["id"] for r in rows if r["part"] == part and (par is None or r["paragraph"] == par) and r["paragraph"] > 0)
    return 0.0 if rid == rows[1]["id"] else max(0.0, seg[rid] - LEAD)
def stamp(t):
    t = int(t); h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"
eps, N = B["episodes"], len(B["episodes"])
for i, ep in enumerate(eps, 1):
    pa, pb = order.index(ep["from_part"]), order.index(ep["to_part"])
    t0 = pstart(order[pa], ep.get("from_paragraph")); t1 = pstart(order[pb + 1]) if pb + 1 < len(order) else timing["total"]
    if "to_paragraph" in ep: t1 = pstart(ep["to_part"], ep["to_paragraph"] + 1)
    out = os.path.join(BASE, f"{P}_RU_EP{i}.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.3f}", "-to", f"{t1:.3f}", "-i", os.path.join(BASE, f"{P}_RU_YouTube.mp4"),
                    "-c", "copy", "-avoid_negative_ts", "make_zero", "-movflags", "+faststart", out], check=True)
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out]))
    ch = "\n".join(f"{stamp(0 if ci == 0 else max(0.0, pstart(c[0], c[1]) - t0))} {c[3]}" for ci, c in enumerate(ep["chapters"]))
    title = f"{R['title']}, часть {i} из {N}: {ep['title_ru']} | Ершов | Аудиокнига для детей"
    if len(title) > 100: title = title.replace("Аудиокнига для детей", "Аудиосказка")
    if len(title) > 100: raise SystemExit(f"the title of part {i} is {len(title)} characters, over YouTube's 100")
    desc = f"""{R['title']}, {R['author']} (1834), часть {i} из {N}: {ep['title_ru']}. Аудиокнига на русском языке, полный текст автора, около {int(round(dur / 60))} минут. Голоса сделаны с помощью ИИ.

{ep['blurb_ru']}

Главы
{ch}

Читать текст и скачать книгу (PDF): https://biblio.unilu.space/ru/book/{B['slug']}/

{R['hashtags']}
"""
    open(os.path.join(BASE, f"{P}_RU_EP{i}_youtube_description.txt"), "w", encoding="utf-8").write(f"TITLE\n{title}\n\nDESCRIPTION\n{desc}\nTAGS\n{', '.join(R['tags'])}\n")
    print(f"part {i}: {stamp(t0)}-{stamp(t1)} = {dur / 60:.1f} min -> {out}")
