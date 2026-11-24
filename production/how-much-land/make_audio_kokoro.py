#!/usr/bin/env python3
"""Multi-voice audiobook with Kokoro (local, no key, no quota). Runs on aak-llm.

  python make_audio_kokoro.py --test-seconds 150     first 2-3 minutes only: real length and real speed
  python make_audio_kokoro.py                        the whole book

Every segment is saved in segments/ and never made twice, so an interrupted run can simply be started again.
Pauses: 0.3 s between segments, 0.75 s between paragraphs, 2.5 s between parts. Silence at the start and end
of each segment is trimmed, loudness is levelled per segment and then for the whole file. Writes the MP3 and a
timing file (start of every segment, paragraph and part) made from the same arithmetic that joins the audio."""
import argparse, json, os, subprocess, sys, time
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

PAUSE_SEGMENT, PAUSE_PARAGRAPH, PAUSE_PART = 0.30, 0.75, 2.5
TARGET_RMS = 0.065          # about -24 dBFS speech level per segment before the final loudness pass
EDGE = 0.012                # amplitude below this counts as silence at the edges
KEEP = 0.04                 # seconds of natural silence kept around the speech

ap = argparse.ArgumentParser()
ap.add_argument("--script", default="How_Much_Land_voice_script.json")
ap.add_argument("--voices", default="voices_kokoro.json")
ap.add_argument("--name", default="How_Much_Land_audiobook")
ap.add_argument("--test-seconds", type=float, help="stop after about this many seconds of audio (a test run)")
ap.add_argument("--assemble-only", action="store_true", help="no speech synthesis, join what is in segments/")
a = ap.parse_args()

rows = json.load(open(a.script, encoding="utf-8"))
voices = json.load(open(a.voices, encoding="utf-8"))
os.makedirs("segments", exist_ok=True)
kokoro = None if a.assemble_only else Kokoro("models/kokoro-v1.0.onnx", "models/voices-v1.0.bin")
if kokoro:
    have = set(kokoro.get_voices())
    missing = sorted({v["voice"] for v in voices.values()} - have)
    if missing:
        sys.exit(f"Kokoro does not have these voices: {missing}. Available: {sorted(have)}")


def trim_and_level(x, sr):
    loud = np.where(np.abs(x) > EDGE)[0]
    if len(loud) == 0:
        return x
    k = int(KEEP * sr)
    x = x[max(0, loud[0] - k): min(len(x), loud[-1] + k)]
    rms = float(np.sqrt(np.mean(np.square(x[np.abs(x) > EDGE])))) or TARGET_RMS
    x = x * float(np.clip(TARGET_RMS / rms, 0.5, 2.5))
    peak = float(np.max(np.abs(x)))
    return x / peak * 0.97 if peak > 0.97 else x


chosen, total, t_gen, n_new = [], 0.0, 0.0, 0
for r in rows:
    text = r["text"].strip()
    if not text:
        continue
    path = os.path.join("segments", f"{r['id']:04d}_{r['speaker']}.wav")
    if not os.path.exists(path):
        if a.assemble_only:
            continue
        v = voices[r["speaker"]]
        t0 = time.time()
        samples, sr = kokoro.create(text, voice=v["voice"], speed=v["speed"], lang=v["lang"])
        t_gen += time.time() - t0
        n_new += 1
        sf.write(path + ".tmp.wav", trim_and_level(np.asarray(samples, dtype=np.float32), sr), sr, subtype="PCM_16")
        os.replace(path + ".tmp.wav", path)
        if n_new % 20 == 0:
            print(f"  {n_new} new segments, {t_gen:.0f} s of generation so far", flush=True)
    data, sr = sf.read(path, dtype="float32")
    chosen.append((r, data, sr))
    total += len(data) / sr
    if a.test_seconds and total >= a.test_seconds:
        break

# join with pauses, and keep the arithmetic for the timing file
SR = chosen[0][2]
pieces, cursor = [], 0.0
seg_t, par_t, part_t = [], {}, {}
last_part = last_par = None
for r, data, sr in chosen:
    if last_part is not None:
        gap = PAUSE_PART if r["part"] != last_part else PAUSE_PARAGRAPH if r["paragraph"] != last_par else PAUSE_SEGMENT
        pieces.append(np.zeros(int(round(gap * SR)), dtype=np.float32))
        cursor += len(pieces[-1]) / SR
    start = cursor
    pieces.append(data)
    cursor += len(data) / SR
    seg_t.append({"id": r["id"], "start": round(start, 3), "end": round(cursor, 3)})
    key = (r["part"], r["paragraph"])
    par_t.setdefault(key, {"part": r["part"], "paragraph": r["paragraph"], "start": round(start, 3)})["end"] = round(cursor, 3)
    part_t.setdefault(r["part"], {"part": r["part"], "start": round(start, 3)})["end"] = round(cursor, 3)
    last_part, last_par = r["part"], r["paragraph"]
audio = np.concatenate(pieces)
suffix = "_test" if a.test_seconds else ""
wav = f"{a.name}{suffix}.wav"
sf.write(wav, audio, SR, subtype="PCM_16")
json.dump({"sample_rate": SR, "total": round(cursor, 3), "segments": seg_t, "paragraphs": list(par_t.values()), "parts": list(part_t.values())},
          open(f"{a.name}{suffix}_timing.json", "w"), indent=1)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", "-ac", "1",
                "-b:a", "128k", f"{a.name}{suffix}.mp3"], check=True)
mins = cursor / 60
print(f"Done: {a.name}{suffix}.mp3, {len(chosen)} segments, length {int(mins)} min {cursor - int(mins) * 60:.0f} s")
if n_new:
    print(f"Speed this run: {n_new} new segments made in {t_gen:.0f} s of generation; speech made {sum(len(d) / s for _, d, s in chosen[-n_new:]):.0f} s of audio "
          f"= {sum(len(d) / s for _, d, s in chosen[-n_new:]) / t_gen:.2f}x real time")
