#!/usr/bin/env python3
"""1920x1080, 30 fps video from the illustrations, timed from the real audio (<prefix>_audiobook_timing.json).

  python make_video.py --test-frames          write a few full-size test frames, render nothing else
  python make_video.py                        render everything: one finished file per scene, join without
                                              re-encoding, then add the sound without re-encoding the picture

Layout: the picture on top (1920x990) with a slow pan and zoom, a thin gold line and a small label under it.
The title card (the cover) shows for the first seconds while the narration starts. The camera shot changes
about every 25 seconds. Every frame time comes from the same arithmetic that joined the audio."""
import argparse, json, math, os, subprocess, sys
from concurrent.futures import ProcessPoolExecutor
import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import book
B, _BASE = book.load()

W, H, VH, FPS = 1920, 1080, 990, 30
TITLE_SECONDS, SHOT_SECONDS, LEAD = 5.0, 25.0, 1.0   # the picture changes LEAD seconds before the new part is heard
ASSETS = "video_assets"
ART = B["art_for_part"]
# points of interest in each picture, as fractions of its width and height
FOCUS = {k: [tuple(p) for p in v] for k, v in B["focus"].items()}
DEFAULT_FOCUS = [(0.3, 0.5), (0.7, 0.55), (0.5, 0.7)]
POOL = B.get("art_pool")          # optional: pictures per part; a new picture every SUB_SECONDS and at every letter (see plan_letters)
FX = B.get("fx", {})              # optional: {"picture name": "rain" | "snow" | "leaves" | "flicker"}
SUB_SECONDS = 180.0
SCENES = B.get("scenes")          # optional: [{"id": first voice-script row id of the scene, "art": picture name}, ...] a new picture where the place or the time changes


def moves(art, k):
    """Camera move number k for this picture: (zoom start, zoom end, centre start, centre end), centres as fractions."""
    A, B, C = FOCUS.get(art, DEFAULT_FOCUS)
    mid = (0.5, 0.5)
    table = [(1.00, 1.34, mid, A), (1.30, 1.30, (0.32, B[1]), (0.68, B[1])), (1.40, 1.00, B, mid),
             (1.26, 1.26, (0.70, C[1]), (0.30, C[1])), (1.12, 1.30, C, B), (1.32, 1.05, A, mid)]
    return table[k % len(table)]


def view(img, z, cx, cy):
    ih, iw = img.shape[:2]
    rw = iw / z
    rh = rw * VH / W
    cx = min(max(cx * iw, rw / 2), iw - rw / 2)
    cy = min(max(cy * ih, rh / 2), ih - rh / 2)
    patch = cv2.getRectSubPix(img, (int(round(rw)), int(round(rh))), (cx, cy))
    return cv2.resize(patch, (W, VH), interpolation=cv2.INTER_AREA)


def plan(timing):
    """Scenes with their frame ranges, and the shots inside each scene."""
    parts = timing["parts"]
    total_frames = int(math.ceil(timing["total"] * FPS))
    starts = [TITLE_SECONDS] + [p["start"] - LEAD for p in parts[1:]]
    bounds = [0] + [int(round(s * FPS)) for s in starts] + [total_frames]
    scenes = [{"name": "title", "part": None, "f0": bounds[0], "f1": bounds[1]}]
    for i, p in enumerate(parts):
        scenes.append({"name": f"part_{p['part']}", "part": p["part"], "f0": bounds[i + 1], "f1": bounds[i + 2]})
    for s in scenes:
        n = s["f1"] - s["f0"]
        k = max(1, int(round(n / FPS / SHOT_SECONDS))) if s["part"] else 1
        edges = [s["f0"] + int(round(n * j / k)) for j in range(k + 1)]
        s["shots"] = [(edges[j], edges[j + 1]) for j in range(k)]
    return scenes, total_frames


def letter_rows():
    """[(segment id, number, label)] for every letter: the narrator rows of the voice script announce them ("June 21. Makar Alexeyevich writes.")."""
    rows = json.load(open(f"{B['prefix']}_voice_script.json", encoding="utf-8"))
    out = []
    for r in rows:
        if r["speaker"] == "NARRATOR":
            date = r["text"].split(".")[0]
            who = "MAKAR" if "Makar" in r["text"] else "VARENKA"
            out.append((r["id"], r["part"], len(out) + 1, f"LETTER {len(out) + 1} · {date.upper()} · {who}"))
    return out


def plan_letters(timing):
    """Like plan(), but a scene for every stretch of at most SUB_SECONDS inside a letter, each with its own picture from the part's pool."""
    seg_start = {s["id"]: s["start"] for s in timing["segments"]}
    total_frames = int(math.ceil(timing["total"] * FPS))
    ls = letter_rows()
    starts = [(max(0.0, seg_start[i] - LEAD) if n > 1 else TITLE_SECONDS) for i, _, n, _ in ls] + [timing["total"]]
    scenes = [{"name": "title", "part": None, "f0": 0, "f1": int(round(TITLE_SECONDS * FPS)), "art": None, "strip": None}]
    seen = {}
    idx = 1
    for j, (sid, part, n, label) in enumerate(ls):
        t0, t1 = starts[j], starts[j + 1]
        pool = POOL[part]
        k_in_part = seen.get(part, 0); seen[part] = k_in_part + 1
        subs = max(1, int(round((t1 - t0) / SUB_SECONDS)))
        for q in range(subs):
            a = t0 + (t1 - t0) * q / subs; b = t0 + (t1 - t0) * (q + 1) / subs
            f0 = int(round(a * FPS)) if not (j == 0 and q == 0) else scenes[0]["f1"]
            f1 = int(round(b * FPS)) if j < len(ls) - 1 or q < subs - 1 else total_frames
            scenes.append({"name": f"s{idx:03d}", "part": part, "f0": f0, "f1": f1, "art": pool[(k_in_part + q) % len(pool)], "strip": f"L{n:02d}"})
            idx += 1
    for s in scenes:
        nfr = s["f1"] - s["f0"]
        k = max(1, int(round(nfr / FPS / SHOT_SECONDS))) if s["part"] else 1
        edges = [s["f0"] + int(round(nfr * j / k)) for j in range(k + 1)]
        s["shots"] = [(edges[j], edges[j + 1]) for j in range(k)]
    return scenes, total_frames


def plan_scenes(timing):
    """Scenes where the story changes place or time (book.json "scenes", by the id of the first voice-script row), plus a scene start at
    every part so the label under the picture is right. A part start without a listed scene keeps the previous picture."""
    seg_start = {s["id"]: s["start"] for s in timing["segments"]}
    rows = json.load(open(f"{B['prefix']}_voice_script.json", encoding="utf-8"))
    part_of = {r["id"]: r["part"] for r in rows}
    first_of_part = {}
    for r in rows:
        first_of_part.setdefault(r["part"], r["id"])
    want = {sc["id"]: sc["art"] for sc in SCENES}
    starts = {}
    for pid in first_of_part.values():
        starts[pid] = want.get(pid)
    for sid, art in want.items():
        starts[sid] = art
    order = sorted(starts)
    scenes = [{"name": "title", "part": None, "f0": 0, "f1": int(round(TITLE_SECONDS * FPS)), "art": None, "strip": None}]
    total_frames = int(math.ceil(timing["total"] * FPS))
    cur_art = None
    for k, sid in enumerate(order):
        cur_art = starts[sid] or cur_art or ART.get(part_of[sid])
        t0 = TITLE_SECONDS if k == 0 else max(0.0, seg_start[sid] - LEAD)
        t1 = timing["total"] if k == len(order) - 1 else max(0.0, seg_start[order[k + 1]] - LEAD)
        f0 = scenes[0]["f1"] if k == 0 else int(round(t0 * FPS))
        f1 = total_frames if k == len(order) - 1 else int(round(t1 * FPS))
        scenes.append({"name": f"s{k + 1:03d}", "part": part_of[sid], "f0": f0, "f1": f1, "art": cur_art, "strip": part_of[sid]})
    for s_ in scenes:
        nfr = s_["f1"] - s_["f0"]
        n = max(1, int(round(nfr / FPS / SHOT_SECONDS))) if s_["part"] else 1
        edges = [s_["f0"] + int(round(nfr * j / n)) for j in range(n + 1)]
        s_["shots"] = [(edges[j], edges[j + 1]) for j in range(n)]
    return scenes, total_frames


_P = {}


def fx_layer(img, kind, f):
    """Small animations drawn on top of the moving picture, all from the frame number (so any frame can be rendered alone)."""
    h, w = img.shape[:2]
    if kind == "flicker":                                   # candle or stove light: the whole picture breathes a little
        g = 1.0 + 0.035 * math.sin(f * 0.31) + 0.02 * math.sin(f * 0.93 + 1.0) + 0.012 * math.sin(f * 2.3)
        return cv2.convertScaleAbs(img, alpha=g, beta=0)
    if kind not in _P:
        r = np.random.RandomState(7)
        n = {"rain": 150, "snow": 130, "leaves": 34}[kind]
        _P[kind] = (r.rand(n), r.rand(n), r.rand(n), r.rand(n))
    x0, y0, a, b = _P[kind]
    ov = img.copy()
    if kind == "rain":
        for i in range(len(x0)):
            sp = 26 + 20 * a[i]; y = (y0[i] * h + f * sp) % h; x = (x0[i] * w - 0.25 * (y - y0[i] * h)) % w
            cv2.line(ov, (int(x), int(y)), (int(x - 7), int(y + 24 + 16 * a[i])), (225, 214, 201), 1, cv2.LINE_AA)
        return cv2.addWeighted(ov, 0.32, img, 0.68, 0)
    if kind == "snow":
        for i in range(len(x0)):
            y = (y0[i] * h + f * (1.4 + 2.2 * a[i])) % h; x = (x0[i] * w + 14 * math.sin(f / 25.0 + b[i] * 6.28)) % w
            cv2.circle(ov, (int(x), int(y)), 2 + int(3 * a[i]), (255, 250, 245), -1, cv2.LINE_AA)
        return cv2.addWeighted(ov, 0.8, img, 0.2, 0)
    for i in range(len(x0)):                               # leaves
        y = (y0[i] * h + f * (1.2 + 1.8 * a[i])) % h; x = (x0[i] * w + f * (1.0 + 1.6 * b[i]) + 30 * math.sin(f / 31.0 + a[i] * 6.28)) % w
        cv2.ellipse(ov, (int(x), int(y)), (10, 4), (f * 2 + i * 40) % 180, 0, 360, (46, 106, 184), -1, cv2.LINE_AA)
    return cv2.addWeighted(ov, 0.85, img, 0.15, 0)


def frame_at(f, scene, art_img, strip, title_img, art):
    """The finished 1920x1080 frame number f (a global frame index) of a scene."""
    if scene["part"] is None:
        fr = title_img.copy()
        fade = min(1.0, f / 24.0)                      # soft fade in from black on the first frames
        return (fr * fade).astype(np.uint8) if fade < 1 else fr
    shot_no = next(i for i, (a, b) in enumerate(scene["shots"]) if a <= f < b)
    a, b = scene["shots"][shot_no]
    t = (f - a) / max(1, b - a - 1)
    z0, z1, c0, c1 = moves(art, shot_no + 2 * int(scene["part_index"]))
    z = z0 + (z1 - z0) * t
    out = np.empty((H, W, 3), np.uint8)
    out[:VH] = view(art_img, z, c0[0] + (c1[0] - c0[0]) * t, c0[1] + (c1[1] - c0[1]) * t)
    if art in FX:
        out[:VH] = fx_layer(out[:VH], FX[art], f)
    out[VH:] = strip
    return out


def load(scene):
    title = cv2.imread(f"{ASSETS}/title_card.png")
    if scene["part"] is None:
        return None, None, title, None
    art = scene.get("art") or ART[scene["part"]]
    return cv2.imread(f"{ASSETS}/art_{art}.png"), cv2.imread(f"{ASSETS}/strip_{scene.get('strip') or scene['part']}.png"), title, art


def render_scene(args):
    scene, out = args
    art_img, strip, title, art = load(scene)
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-g", "60", "-keyint_min", "60",
           "-sc_threshold", "0", "-bf", "2", "-threads", "4", "-video_track_timescale", "15360", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in range(scene["f0"], scene["f1"]):
        p.stdin.write(frame_at(f, scene, art_img, strip, title, art).tobytes())
    p.stdin.close()
    if p.wait() != 0:
        raise SystemExit(f"ffmpeg failed on {scene['name']}")
    return scene["name"], scene["f1"] - scene["f0"]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--timing", default=f"{B['prefix']}_audiobook_timing.json")
    ap.add_argument("--audio", default=f"{B['prefix']}_audiobook.mp3")
    ap.add_argument("--out", default=f"{B['prefix']}_YouTube.mp4")
    ap.add_argument("--test-frames", action="store_true")
    ap.add_argument("--workers", type=int, default=9)
    a = ap.parse_args()
    timing = json.load(open(a.timing))
    scenes, total_frames = plan_scenes(timing) if SCENES else plan_letters(timing) if POOL else plan(timing)
    for i, s in enumerate(scenes):
        s["part_index"] = i
    for s in scenes[:12] + scenes[-3:]:
        print(f"{s['name']:>9}: frames {s['f0']:6d}-{s['f1']:6d}  ({(s['f1'] - s['f0']) / FPS:6.1f} s, {len(s['shots'])} shot(s))")
    print("total frames:", total_frames, "=", round(total_frames / FPS, 2), "s | audio:", timing["total"], "s")
    if a.test_frames:
        os.makedirs("test_frames", exist_ok=True)
        real = [x["name"] for x in scenes if x["part"]]
        if POOL or SCENES:
            picks = [("title", 2)] + [(real[min(len(real) - 1, int(len(real) * q))], 5) for q in (0, .2, .45, .7, .99)]
        else:
            picks = [("title", 20), ("part_I", 2), ("part_V", 5), ("part_VIII", 3), ("part_IX", 4), ("part_IX", 99999)]
        for name, off in picks:
            s = next(x for x in scenes if x["name"] == name)
            f = min(s["f0"] + int(off * FPS) if off < 1000 else s["f1"] - 2, s["f1"] - 1)
            art_img, strip, title, art = load(s)
            cv2.imwrite(f"test_frames/{name}_{f}.png", frame_at(f, s, art_img, strip, title, art))
        print("test frames written:", sorted(os.listdir("test_frames")))
        sys.exit(0)
    os.makedirs("scenes", exist_ok=True)
    jobs = [(s, f"scenes/{i:02d}_{s['name']}.mp4") for i, s in enumerate(scenes)]
    with ProcessPoolExecutor(max_workers=a.workers) as ex:
        for name, n in ex.map(render_scene, jobs):
            print(f"  rendered {name}: {n} frames", flush=True)
    open("scenes/list.txt", "w").write("".join(f"file '{os.path.basename(o)}'\n" for _, o in jobs))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "scenes/list.txt", "-c", "copy", "video_only.mp4"], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "video_only.mp4", "-i", a.audio, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", a.out], check=True)
    print("Done:", a.out)
