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
ap.add_argument("--seg-dir", default="segments_gemini", help="folder for the finished segments (use another one for another language)")
ap.add_argument("--no-style", action="store_true", help="send the bare text, no style sentence (the style sentence is sometimes read aloud; a voices entry with \"style\": \"\" does the same for one speaker)")
ap.add_argument("--chunk", action="store_true", help="few big requests for the free tier: merge consecutive rows (up to --chunk-chars characters, 2 speakers at most); breaks at every part and scene start")
ap.add_argument("--chunk-chars", type=int, default=int(os.environ.get("GEMINI_CHUNK_CHARS", 2800)))
ap.add_argument("--max-requests", type=int, help="stop after this many new requests (testing); the finished chunks are assembled as a _test file")
ap.add_argument("--test-seconds", type=float)
ap.add_argument("--assemble-only", action="store_true")
a = ap.parse_args()

key = os.environ.get("GEMINI_API_KEY") or (open(os.path.expanduser("~/.config/bibliotheque/gemini.key")).read().strip() if os.path.exists(os.path.expanduser("~/.config/bibliotheque/gemini.key")) else "")
if not key and not a.assemble_only:
    sys.exit("no Gemini key: run scripts/set-gemini-key.sh on the Mac, or set GEMINI_API_KEY")

rows = json.load(open(a.script, encoding="utf-8"))
SEG_DIR = a.seg_dir
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


def synth(text, voice, style, speech=None, max_empty=4):
    """One request. Returns float32 samples at 24 kHz. Obeys the quota (see the top of the file). `speech` replaces the single-voice
    speechConfig (chunk mode with two speakers); `max_empty` is how many times a no-audio answer is tried."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{a.model}:generateContent"
    parts = text if isinstance(text, list) else [{"text": f"{style}: {text}" if style else text}]   # a list = one part per row, each with its speaker
    body = {"contents": [{"parts": parts}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": speech or {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
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
                ids = re.findall(r'"quotaId":\s*"([^"]+)"', msg)
                if any("PerDay" in q for q in ids) or (not ids and re.search(r"PerDay|per day", msg, re.I)):
                    print(f"DAILY QUOTA used up for {a.model} ({', '.join(ids) or 'no quota id'}). Finished segments are kept; run again after the quota resets "
                          f"(midnight Pacific), or use --model with another TTS model (each has its own daily quota).", flush=True)
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
            if attempts < max_empty:
                continue
            sys.exit(f"no audio in the answer for: {str(text)[:60]!r}: {json.dumps(j)[:300]}")


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


def break_ids():
    """Row ids where a chunk must start: every part start and every scene start (the video cuts pictures there and needs exact times)."""
    ids, seen = set(), set()
    for r in rows:
        if r["part"] not in seen:
            seen.add(r["part"])
            ids.add(r["id"])
    sc = _B.get("scenes")
    if sc:
        eng = f"{_P}_voice_script.json"
        if os.environ.get("BOOK_LANG", "en") == "ru" and os.path.exists(eng) and os.path.abspath(eng) != os.path.abspath(a.script):
            sc = book.map_scene_ids(sc, json.load(open(eng, encoding="utf-8")), rows)
        ids |= {x["id"] for x in sc}
    return ids


def plan_chunks():
    brk, out, cur, chars = break_ids(), [], [], 0
    for r in rows:
        t = " ".join(r["text"].split())
        if not t:
            continue
        sp = {x["speaker"] for x in cur} | {r["speaker"]}
        if cur and (r["id"] in brk or len(sp) > 2 or chars + len(t) > a.chunk_chars):
            out.append(cur)
            cur, chars = [], 0
        cur.append({**r, "text": t})
        chars += len(t)
    if cur:
        out.append(cur)
    return out


def chunk_request(ch):
    """(text, speech config) for one chunk: one speaker = bare text and the normal voice; two = 'Name: text' lines and multi-speaker voices."""
    names = list(dict.fromkeys(x["speaker"] for x in ch))
    if len(names) == 1:
        return " ".join(x["text"] for x in ch), {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voices[names[0]]["voice"]}}}
    label = {n: re.sub(r"[^A-Za-z0-9]", "", n).title() or f"Speaker{i + 1}" for i, n in enumerate(names)}
    text = [{"text": x["text"], "speechMetadata": {"speaker": label[x["speaker"]]}} for x in ch]   # newer models require the speaker on every part
    cfg = {"multiSpeakerVoiceConfig": {"speakerVoiceConfigs": [
        {"speaker": label[n], "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voices[n]["voice"]}}} for n in names]}}
    return text, cfg


def run_chunks():
    """Returns [(rows, samples, sr)] for the finished chunks (making the missing ones), in book order."""
    done, total, n_new, t_gen = [], 0.0, 0, 0.0
    chunks = plan_chunks()
    print(f"{len(chunks)} chunks for {sum(len(c) for c in chunks)} rows ({a.chunk_chars} characters at most each)", flush=True)
    for ch in chunks:
        first = ch[0]["id"]
        path = os.path.join(SEG_DIR, f"chunk_{first:04d}.wav")
        man = path[:-4] + ".json"
        ids = [x["id"] for x in ch]
        ok = os.path.exists(path) and os.path.exists(man) and json.load(open(man)).get("rows") == ids
        if not ok:
            if a.assemble_only or (a.max_requests and n_new >= a.max_requests):
                break
            text, cfg = chunk_request(ch)
            nchar = sum(len(x["text"]) for x in ch)
            t0 = time.time()
            for tryno in (1, 2):
                samples = trim_and_level(synth(text, None, "", speech=cfg, max_empty=3), SR_API)
                n_new += 1
                cps = nchar / (len(samples) / SR_API)
                if 8 <= cps <= 22:
                    break
                print(f"  chunk {first}: {cps:.1f} characters per second is implausible ({nchar} chars, {len(samples) / SR_API:.0f} s)"
                      + (": asking once more" if tryno == 1 else ": keeping it, CHECK THIS CHUNK"), flush=True)
            t_gen += time.time() - t0
            sf.write(path + ".tmp.wav", samples, SR_API, subtype="PCM_16")
            os.replace(path + ".tmp.wav", path)
            json.dump({"rows": ids, "chars": [len(x["text"]) for x in ch], "speakers": sorted({x["speaker"] for x in ch}), "model": a.model,
                       "seconds": round(len(samples) / SR_API, 3), "chars_per_second": round(cps, 2)}, open(man, "w"))
            print(f"  chunk {first}: {len(ids)} rows, {nchar} chars, {len(samples) / SR_API:.0f} s ({cps:.1f} chars/s); {n_new} requests this run", flush=True)
        data, sr = sf.read(path, dtype="float32")
        done.append((ch, data, sr))
        total += len(data) / sr
        if a.test_seconds and total >= a.test_seconds:
            break
    return done, n_new


if a.chunk:
    chunked, n_new = run_chunks()
    if not chunked:
        sys.exit("no finished chunks to assemble")
    all_planned = sum(len(c) for c, _, _ in chunked) == sum(1 for r in rows if r["text"].strip())
    if not all_planned:
        a.test_seconds = a.test_seconds or 1e9    # unfinished book: assemble what exists under the _test name
    chosen = [(ch, data, sr) for ch, data, sr in chunked]
else:
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
            samples = synth(text, v["voice"], "" if a.no_style else v.get("style", GENERIC_STYLE))
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


def add_row(r, start, end):
    seg_t.append({"id": r["id"], "start": round(start, 3), "end": round(end, 3)})
    key_ = (r["part"], r["paragraph"])
    par_t.setdefault(key_, {"part": r["part"], "paragraph": r["paragraph"], "start": round(start, 3)})["end"] = round(end, 3)
    part_t.setdefault(r["part"], {"part": r["part"], "start": round(start, 3)})["end"] = round(end, 3)


for item, data, sr in chosen:
    first = item[0] if a.chunk else item
    if last_part is not None:
        gap = PAUSE_PART if first["part"] != last_part else PAUSE_PARAGRAPH if first["paragraph"] != last_par else PAUSE_SEGMENT
        pieces.append(np.zeros(int(round(gap * SR)), dtype=np.float32))
        cursor += len(pieces[-1]) / SR
    start = cursor
    pieces.append(data)
    cursor += len(data) / SR
    if a.chunk:   # chunk start and end are exact; row boundaries inside are proportional to characters
        n_chars = [len(x["text"]) for x in item]
        cum = 0
        for x, n in zip(item, n_chars):
            add_row(x, start + (cursor - start) * cum / sum(n_chars), start + (cursor - start) * (cum + n) / sum(n_chars))
            cum += n
        last_part, last_par = item[-1]["part"], item[-1]["paragraph"]
    else:
        add_row(item, start, cursor)
        last_part, last_par = item["part"], item["paragraph"]
audio = np.concatenate(pieces)
suffix = "_test" if a.test_seconds else ""
wav = f"{a.name}{suffix}.wav"
sf.write(wav, audio, SR, subtype="PCM_16")
json.dump({"sample_rate": SR, "total": round(cursor, 3), "segments": seg_t, "paragraphs": list(par_t.values()), "parts": list(part_t.values())},
          open(f"{a.name}{suffix}_timing.json", "w"), indent=1)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", "-ac", "1",
                "-b:a", "128k", f"{a.name}{suffix}.mp3"], check=True)
mins = cursor / 60
print(f"Done: {a.name}{suffix}.mp3, {len(seg_t)} segments, length {int(mins)} min {cursor - int(mins) * 60:.0f} s, {n_new} requests this run")
