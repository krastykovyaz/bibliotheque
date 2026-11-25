#!/usr/bin/env python3
"""Multi-voice audiobook with Gemini text-to-speech. Same outputs as make_audio_kokoro.py (<Prefix>_audiobook.wav/.mp3 and
<Prefix>_audiobook_timing.json), so the video, PDF and delivery steps do not change. Runs on aak-llm (the key is in
~/.config/bibliotheque/gemini.key, put there with scripts/set-gemini-key.sh) or anywhere with GEMINI_API_KEY set.

  python make_audio_gemini.py --test-seconds 60     first minute only: hear it before spending the quota
  python make_audio_gemini.py                       the whole book

QUOTA: requests are paced (--rpm, default 6 a minute), a 429 answer is obeyed (it tells how long to wait), and when the DAILY
quota is used up the run stops cleanly (exit code 3) with every finished segment kept in segments_gemini/: start it again after
the quota resets (midnight Pacific time) and it carries on where it stopped. Nothing is ever made twice.

Voices: voices_gemini.json maps each speaker to {"voice": "<Gemini voice>", "style": "<how to say it>"}. If it does not exist it is
made from voices_kokoro.json (female/male kept, narrator warm) and saved, so you can edit it."""
import argparse, base64, json, os, re, subprocess, sys, time, urllib.error, urllib.request
import numpy as np
import soundfile as sf

PAUSE_SEGMENT, PAUSE_PARAGRAPH, PAUSE_PART = 0.30, 0.75, 2.5
TARGET_RMS, EDGE, KEEP = 0.065, 0.012, 0.04
SR_API = 24000
SEG_DIR = "segments_gemini"
DEFAULT_MODEL = "gemini-3.8-flash-tts"
FEMALE = ["Leda", "Aoede", "Autonoe", "Zephyr", "Callirrhoe", "Despina", "Kore", "Vindemiatrix"]
MALE = ["Puck", "Charon", "Achird", "Fenrir", "Orus", "Umbriel", "Iapetus", "Algieba", "Sadaltager"]
NARRATOR_VOICE = "Sulafat"
GENERIC_STYLE = "Say this warmly and clearly, like a kind storyteller reading to young children"

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import book
_B, _ = book.load()
_P = _B["prefix"]
ap = argparse.ArgumentParser()
ap.add_argument("--script", default=f"{_P}_voice_script.json")
ap.add_argument("--voices", default="voices_gemini.json")
ap.add_argument("--name", default=f"{_P}_audiobook")
ap.add_argument("--model", default=os.environ.get("GEMINI_TTS_MODEL", DEFAULT_MODEL))
ap.add_argument("--rpm", type=float, default=float(os.environ.get("GEMINI_RPM", 6)), help="requests per minute (stay under your quota)")
ap.add_argument("--test-seconds", type=float)
ap.add_argument("--assemble-only", action="store_true")
a = ap.parse_args()

key = os.environ.get("GEMINI_API_KEY") or (open(os.path.expanduser("~/.config/bibliotheque/gemini.key")).read().strip() if os.path.exists(os.path.expanduser("~/.config/bibliotheque/gemini.key")) else "")
if not key and not a.assemble_only:
    sys.exit("no Gemini key: run scripts/set-gemini-key.sh on the Mac, or set GEMINI_API_KEY")

rows = json.load(open(a.script, encoding="utf-8"))
os.makedirs(SEG_DIR, exist_ok=True)


def make_voices():
    k = json.load(open("voices_kokoro.json", encoding="utf-8"))
    out, f, m = {}, iter(FEMALE * 3), iter(MALE * 3)
    for sp, v in k.items():
        slow, fast = v.get("speed", 1) <= 0.88, v.get("speed", 1) >= 1.08
        pace = ", slowly and gravely" if slow else ", briskly and lightly" if fast else ""
        if sp.upper().startswith("NARRATOR"):
            out[sp] = {"voice": NARRATOR_VOICE, "style": GENERIC_STYLE + ", unhurried"}
        else:
            voice = next(f) if v["voice"].startswith(("bf_", "af_")) else next(m)
            out[sp] = {"voice": voice, "style": f"Say this as a friendly character in a children's tale{pace}"}
    json.dump(out, open(a.voices, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("made", a.voices, "from voices_kokoro.json: edit it to change a voice")
    return out


voices = json.load(open(a.voices, encoding="utf-8")) if os.path.exists(a.voices) else make_voices()

_last = [0.0]


def pace():
    gap = 60.0 / a.rpm
    wait = _last[0] + gap - time.time()
    if wait > 0:
        time.sleep(wait)
    _last[0] = time.time()


def synth(text, voice, style):
    """One request. Returns float32 samples at 24 kHz. Obeys the quota (see the top of the file)."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{a.model}:generateContent"
    body = {"contents": [{"parts": [{"text": f"{style}: {text}"}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
    data = json.dumps(body).encode()
    attempts = 0
    while True:
        attempts += 1
        pace()
        req = urllib.request.Request(url, data=data, headers={"content-type": "application/json", "x-goog-api-key": key})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                j = json.load(r)
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "replace")
            if e.code == 429:
                if re.search(r"PerDay|per day|daily", msg, re.I):
                    print("DAILY QUOTA used up. Finished segments are kept; run again after the quota resets (midnight Pacific).", flush=True)
                    sys.exit(3)
                m = re.search(r'"retryDelay":\s*"([\d.]+)s"', msg)
                wait = float(m.group(1)) + 2 if m else min(60, 10 * attempts)
                print(f"  quota answer 429: waiting {wait:.0f} s", flush=True)
                time.sleep(wait)
                if attempts < 12:
                    continue
            elif e.code >= 500 and attempts < 6:
                time.sleep(min(60, 5 * attempts))
                continue
            sys.exit(f"Gemini error {e.code}: {msg[:300]}")
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            if attempts < 6:
                time.sleep(min(60, 5 * attempts))
                continue
            sys.exit(f"network error: {e}")
        try:
            part = j["candidates"][0]["content"]["parts"][0]["inlineData"]
            pcm = base64.b64decode(part["data"])
            return np.frombuffer(pcm, dtype="<i2").astype(np.float32) / 32768.0
        except (KeyError, IndexError):
            # the model sometimes answers with text instead of audio: ask again (a few times)
            if attempts < 4:
                continue
            sys.exit(f"no audio in the answer for: {text[:60]!r}: {json.dumps(j)[:300]}")


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
    path = os.path.join(SEG_DIR, f"{r['id']:04d}_{r['speaker']}.wav")
    if not os.path.exists(path):
        if a.assemble_only:
            continue
        v = voices[r["speaker"]]
        t0 = time.time()
        samples = synth(text, v["voice"], v.get("style", GENERIC_STYLE))
        t_gen += time.time() - t0
        n_new += 1
        sf.write(path + ".tmp.wav", trim_and_level(samples, SR_API), SR_API, subtype="PCM_16")
        os.replace(path + ".tmp.wav", path)
        if n_new % 10 == 0:
            print(f"  {n_new} new segments, {t_gen:.0f} s so far", flush=True)
    data, sr = sf.read(path, dtype="float32")
    chosen.append((r, data, sr))
    total += len(data) / sr
    if a.test_seconds and total >= a.test_seconds:
        break

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
    key_ = (r["part"], r["paragraph"])
    par_t.setdefault(key_, {"part": r["part"], "paragraph": r["paragraph"], "start": round(start, 3)})["end"] = round(cursor, 3)
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
print(f"Done: {a.name}{suffix}.mp3, {len(chosen)} segments, length {int(mins)} min {cursor - int(mins) * 60:.0f} s, {n_new} requests this run")
