#!/usr/bin/env python3
"""Cuts the finished video into the episodes listed in book.json ("episodes": title, blurb, letters [first, last]) at letter
boundaries (these are the starts of the video's scenes, so the cut is clean and nothing is re-encoded), and writes a
description with chapters for every episode. Run on aak-llm in the book folder (BOOK_DIR) after the video exists.
Output: <prefix>_EP<n>.mp4 and <prefix>_EP<n>_youtube_description.txt"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import book
B, BASE = book.load()
P = B["prefix"]; LEAD = 1.0
timing = json.load(open(os.path.join(BASE, f"{P}_audiobook_timing.json")))
seg = {s["id"]: s["start"] for s in timing["segments"]}
rows = json.load(open(os.path.join(BASE, f"{P}_voice_script.json"), encoding="utf-8"))
letters = [(r["id"], r["text"]) for r in rows if r["speaker"] == "NARRATOR"]
def lstart(n): return 0.0 if n == 1 else max(0.0, seg[letters[n - 1][0]] - LEAD)
def stamp(t):
    t = int(t); h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"
eps, N = B["episodes"], len(B["episodes"])
for i, ep in enumerate(eps, 1):
    a, b = ep["letters"]
    t0 = lstart(a); t1 = lstart(b + 1) if b < len(letters) else timing["total"]
    out = os.path.join(BASE, f"{P}_EP{i}.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.3f}", "-to", f"{t1:.3f}", "-i", os.path.join(BASE, f"{P}_YouTube.mp4"),
                    "-c", "copy", "-avoid_negative_ts", "make_zero", "-movflags", "+faststart", out], check=True)
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out]))
    chapters = []
    for n in range(a, b + 1):
        head = letters[n - 1][1].split(".")[0]
        who = "Makar" if "Makar" in letters[n - 1][1] else "Varenka"
        chapters.append(f"{stamp(lstart(n) - t0)} Letter {n}: {head} ({who})")
    ch = ("\nChapters\n" + "\n".join(chapters) + "\n") if len(chapters) >= 3 else ""
    title = f"Poor Folk, Part {i} of {N}: {ep['title']} | Dostoevsky | Full-Cast Audiobook (English)"
    desc = f"""Poor Folk by Fyodor Dostoevsky (1846), part {i} of {N}: {ep['title']}. A full-cast audiobook in English, about {int(round(dur / 60))} minutes.

{ep['blurb']}

All {N} parts in order: https://www.youtube.com/playlist?list={B['series_playlist']}
{ch}
Read the text and download the book (PDF): https://biblio.unilu.space/book/{B['slug']}/

{B['hashtags']}
"""
    open(os.path.join(BASE, f"{P}_EP{i}_youtube_description.txt"), "w", encoding="utf-8").write(
        f"TITLE\n{title}\n\nDESCRIPTION\n{desc}\nTAGS\n{', '.join(B['tags'])}\n")
    print(f"part {i}: {stamp(t0)}-{stamp(t1)} = {dur / 60:.1f} min, {len(chapters)} chapters -> {out}")
