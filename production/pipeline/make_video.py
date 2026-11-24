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


def moves(art, k):
    """Camera move number k for this picture: (zoom start, zoom end, centre start, centre end), centres as fractions."""
    A, B, C = FOCUS[art]
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
    out[VH:] = strip
    return out


def load(scene):
    title = cv2.imread(f"{ASSETS}/title_card.png")
    if scene["part"] is None:
        return None, None, title, None
    art = ART[scene["part"]]
    return cv2.imread(f"{ASSETS}/art_{art}.png"), cv2.imread(f"{ASSETS}/strip_{scene['part']}.png"), title, art


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
    scenes, total_frames = plan(timing)
    for i, s in enumerate(scenes):
        s["part_index"] = i
    for s in scenes:
        print(f"{s['name']:>9}: frames {s['f0']:6d}-{s['f1']:6d}  ({(s['f1'] - s['f0']) / FPS:6.1f} s, {len(s['shots'])} shot(s))")
    print("total frames:", total_frames, "=", round(total_frames / FPS, 2), "s | audio:", timing["total"], "s")
    if a.test_frames:
        os.makedirs("test_frames", exist_ok=True)
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
