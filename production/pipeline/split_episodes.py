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
# episodes defined by parts ("from_part"/"to_part"): cut at part starts
parts_order = list(dict.fromkeys(r["part"] for r in rows))
first_row = {}
for r in rows:
    first_row.setdefault(r["part"], r["id"])
def pstart(part, par=None):
    if par is not None:     # start of paragraph <par> of the part (episodes that begin or end inside a part)
        rid = next(r["id"] for r in rows if r["part"] == part and r["paragraph"] == par)
        return 0.0 if rid == rows[0]["id"] else max(0.0, seg[rid] - LEAD)
    return 0.0 if part == parts_order[0] else max(0.0, seg[first_row[part]] - LEAD)
def stamp(t):
    t = int(t); h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"
eps, N = B["episodes"], len(B["episodes"])
for i, ep in enumerate(eps, 1):
    if "from_part" in ep:
        pa, pb = parts_order.index(ep["from_part"]), parts_order.index(ep["to_part"])
        t0 = pstart(parts_order[pa], ep.get("from_paragraph")); t1 = pstart(parts_order[pb + 1]) if pb + 1 < len(parts_order) else timing["total"]
        if "to_paragraph" in ep: t1 = pstart(ep["to_part"], ep["to_paragraph"] + 1)     # optional: end inside the last part
        pnames = B["names"]
    else:
        a, b = ep["letters"]
        t0 = lstart(a); t1 = lstart(b + 1) if b < len(letters) else timing["total"]
    out = os.path.join(BASE, f"{P}_EP{i}.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t0:.3f}", "-to", f"{t1:.3f}", "-i", os.path.join(BASE, f"{P}_YouTube.mp4"),
                    "-c", "copy", "-avoid_negative_ts", "make_zero", "-movflags", "+faststart", out], check=True)
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out]))
    chapters = []
    if "from_part" in ep:
        if ep.get("chapters"):      # optional: [[part, paragraph, title], ...]
            for cp, cpar, ctitle in ep["chapters"]:
                chapters.append(f"{stamp(max(0.0, pstart(cp, cpar) - t0))} {ctitle}")
        else:
          for q in range(pa, pb + 1):
            chapters.append(f"{stamp(pstart(parts_order[q]) - t0)} Part {parts_order[q]}: {pnames[parts_order[q]]}")
    else:
      for n in range(a, b + 1):
        head = letters[n - 1][1].split(".")[0]
        who = "Makar" if "Makar" in letters[n - 1][1] else "Varenka"
        chapters.append(f"{stamp(lstart(n) - t0)} Letter {n}: {head} ({who})")
    ch = ("\nChapters\n" + "\n".join(chapters) + "\n") if len(chapters) >= 3 else ""
    title = f"{B['title']}, Part {i} of {N}: {ep['title']} | {B['author'].split()[-1]} | Full-Cast Audiobook (English)"
    if len(title) > 100:  # YouTube cuts a title at 100 characters
        title = title.replace("Full-Cast Audiobook", "Audiobook")
    if len(title) > 100:
        raise SystemExit(f"the title of part {i} is {len(title)} characters, over YouTube's 100: shorten the episode title in book.json")
    desc = f"""{B['title']} by {B['author']} ({B['year']}), part {i} of {N}: {ep['title']}. A full-cast audiobook in English, about {int(round(dur / 60))} minutes.

{ep['blurb']}

All {N} parts in order: https://www.youtube.com/playlist?list={B['series_playlist']}
{ch}
Read the text and download the book (PDF): https://biblio.unilu.space/book/{B['slug']}/

{B['hashtags']}
"""
    open(os.path.join(BASE, f"{P}_EP{i}_youtube_description.txt"), "w", encoding="utf-8").write(
        f"TITLE\n{title}\n\nDESCRIPTION\n{desc}\nTAGS\n{', '.join(B['tags'])}\n")
    print(f"part {i}: {stamp(t0)}-{stamp(t1)} = {dur / 60:.1f} min, {len(chapters)} chapters -> {out}")
