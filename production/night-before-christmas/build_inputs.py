#!/usr/bin/env python3
"""The Night Before Christmas: the translation (written by hand, paragraph for paragraph; the text lives in tr/en_*.py,
index = paragraph number in paras_ru.json), source_clean.json, the voice script and voices.
Inline markers <<SPEAKER>> ... <<N>> in the English text mark who speaks; they are removed from translation_en.json."""
import json, re, sys, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "tr")
import en_a, en_b, en_c, en_d, en_e, en_f, en_g
from scenes_def import SCENES
EN = {}
for m in (en_a, en_b, en_c, en_d, en_e, en_f, en_g): EN.update(m.EN)
ru = json.load(open("paras_ru.json", encoding="utf-8"))
BRK = "@@BREAK@@"
PARTS = {"I": (0, 17), "II": (19, 44), "III": (46, 71), "IV": (73, 90), "V": (92, 122), "VI": (124, 184), "VII": (186, 236), "VIII": (238, 265)}
NAMES = {"I": "The Stolen Moon", "II": "Oksana and Solokha", "III": "The Blizzard", "IV": "Solokha's Visitors",
         "V": "The Devil's Bargain", "VI": "The Sacks", "VII": "To Petersburg", "VIII": "Christmas Morning"}
ALIAS = {"WEAVER'S WIFE": "WEAVER_WIFE", "DEACON'S WIFE": "DEACON_WIFE", "N": "NARRATOR"}
TAG = re.compile(r"<<([^>]+)>>")


def clean(t): return re.sub(r"\s+", " ", TAG.sub("", t)).strip()


def pieces(t):
    """[(speaker, text)] from a marked paragraph; the part before the first marker is the narrator's."""
    out, spk, pos = [], "NARRATOR", 0
    for m in TAG.finditer(t):
        out.append((spk, t[pos:m.start()])); spk = ALIAS.get(m.group(1), m.group(1)); pos = m.end()
    out.append((spk, t[pos:]))
    res = []
    for s, x in out:
        x = re.sub(r"\s+", " ", x).strip()
        if not x: continue
        if res and res[-1][0] == s: res[-1] = (s, res[-1][1] + " " + x)
        else: res.append((s, x))
    return res


def chunks(x, lim=230):
    """a long narrator piece is cut at sentence ends into groups of about 150-200 words (so scenes can start inside a long paragraph)."""
    if len(x.split()) <= lim and not any(k in x for k, _ in SCENES): return [x]
    sents = re.split(r"(?<=[.!?])\s+(?=[A-Z“\"])", x)
    out, cur = [], []
    for s_ in sents:
        if cur and any(s_.startswith(k) for k, _ in SCENES) and sum(len(t.split()) for t in cur) >= 12: out.append(" ".join(cur)); cur = []
        cur.append(s_)
        if sum(len(t.split()) for t in cur) >= 150: out.append(" ".join(cur)); cur = []
    if cur:
        if out and sum(len(t.split()) for t in cur) < 60 and not any(cur[0].startswith(k) for k, _ in SCENES): out[-1] += " " + " ".join(cur)
        else: out.append(" ".join(cur))
    return out


T, S, rows, n = {}, [], [], 0
used = set()
for part, (a, b) in PARTS.items():
    idx = [i for i in range(a, b + 1) if ru[i] != BRK]
    used.update(idx)
    T[part] = [clean(EN[i]) for i in idx]
    S.append({"part": part, "paragraphs": [ru[i] for i in idx], "other_blocks": []})
    for k, i in enumerate(idx, 1):
        for spk, x in pieces(EN[i]):
            for y in (chunks(x) if spk == "NARRATOR" else [x]):
                n += 1; rows.append({"id": n, "part": part, "paragraph": k, "speaker": spk, "text": y})
assert used == {i for i, p in enumerate(ru) if p != BRK}, "some Russian paragraph is not covered"
assert all(i in EN for i in used)
json.dump(T, open("translation_en.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(S, open("source_clean.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(rows, open("Night_Before_Christmas_voice_script.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
with open("Night_Before_Christmas_voice_script.md", "w", encoding="utf-8") as f:
    cur = None
    for r in rows:
        if r["part"] != cur: cur = r["part"]; f.write(f"\n## {cur} · {NAMES[cur]}\n\n")
        f.write(f"**{r['speaker']}**: {r['text']}\n\n")
V = lambda v, s: {"voice": v, "speed": s, "lang": "en-gb"}
VOICES = {"NARRATOR": V("bm_george", 0.95), "VAKULA": V("bm_daniel", 1.04), "OKSANA": V("bf_emma", 1.0), "SOLOKHA": V("bf_isabella", 0.98),
          "CHUB": V("bm_lewis", 0.96), "DEVIL": V("bm_fable", 1.15), "PANAS": V("bm_fable", 0.9), "HEAD": V("bm_fable", 0.82),
          "DEACON": V("bm_lewis", 1.12), "PATSYUK": V("bm_fable", 0.78), "WEAVER": V("bm_daniel", 0.94), "ZAPOROZHIAN": V("bm_lewis", 0.88),
          "POTEMKIN": V("bm_fable", 0.88), "WRITER": V("bm_daniel", 0.92), "BISHOP": V("bm_fable", 0.84), "LADS": V("bm_daniel", 1.12),
          "EMPRESS": V("bf_isabella", 0.92), "GIRLS": V("bf_emma", 1.1), "WOMAN": V("bf_isabella", 1.06), "WIFE": V("bf_isabella", 1.0),
          "WEAVER_WIFE": V("bf_emma", 0.98), "DEACON_WIFE": V("bf_isabella", 1.12)}
speakers = {r["speaker"] for r in rows}
assert speakers <= set(VOICES), speakers - set(VOICES)
json.dump({k: v for k, v in VOICES.items() if k in speakers}, open("voices_kokoro.json", "w"), indent=1)
ew = {p: sum(len(x.split()) for x in v) for p, v in T.items()}
print(n, "segments,", sum(ew.values()), "English words,", sum(len(x.split()) for s in S for x in s["paragraphs"]), "Russian words")
print(ew)

# ---- scenes -> book.json (each scene starts at the first row whose text begins with the given words)
sc, pos = [], 0
for key, art in SCENES:
    j = next((k for k in range(pos, len(rows)) if rows[k]["text"].lstrip("“\"").startswith(key)), None)
    assert j is not None, "scene start not found: " + key
    sc.append({"id": rows[j]["id"], "art": art}); pos = j + 1
B = json.load(open("book.json", encoding="utf-8")); B["scenes"] = sc
json.dump(B, open("book.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
wc = {r["id"]: len(r["text"].split()) for r in rows}
ids = [x["id"] for x in sc] + [rows[-1]["id"] + 1]
mins = [sum(w for i, w in wc.items() if a <= i < b) / 150 for a, b in zip(ids, ids[1:])]
print(len(sc), "scenes;", len({x["art"] for x in sc}), "pictures; minutes per scene: min %.1f max %.1f" % (min(mins), max(mins)))
print([round(m, 1) for m in mins])
