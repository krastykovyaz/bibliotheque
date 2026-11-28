#!/usr/bin/env python3
"""The Little Humpbacked Horse (Yershov, 1834/1868): English verse draft (tr/*.txt, paragraph by paragraph against the Russian stanzas), source_clean.json
(the Russian text kept as lines), EN and RU voice scripts, scenes, voices. Reads raw/clean.json (clean_src.py). The Russian is only SPLIT between speakers."""
import json, re
from spans import load, spans
d, BL = load(); SP = spans(d)
RUS = """DANILO DANILO FATHER GAVRILO GAVRILO FATHER IVAN FATHER IVAN MARE IVAN IVAN DANILO IVAN IVAN DANILO DANILO DANILO IVAN KONEK IVAN DANILO IVAN DANILO DANILO GAVRILO GAVRILO IVAN KONEK IVAN IVAN HERALD MERCHANT GUARD WARDEN WARDEN TSAR WARDEN WARDEN TSAR TSAR IVAN TSAR TSAR IVAN TSAR TSAR CHAMBERLAIN CHAMBERLAIN CHAMBERLAIN CHAMBERLAIN TSAR CHAMBERLAIN TSAR CHAMBERLAIN TSAR IVAN NOBLE IVAN IVAN TSAR IVAN TSAR IVAN TSAR TSAR IVAN TSAR IVAN TSAR KONEK IVAN KONEK IVAN KONEK KONEK KONEK IVAN IVAN IVAN KONEK IVAN TSAR IVAN IVAN IVAN TSAR HUNTER TSAR CHAMBERLAIN SERVANT COOKS SERVANT COOKS COOKS SERVANT COOKS SERVANT CHAMBERLAIN TSAR CHAMBERLAIN TSAR TSAR IVAN TSAR KONEK IVAN KONEK IVAN TSAR KONEK KONEK KONEK IVAN KONEK IVAN KONEK IVAN IVAN KONEK TSAR TSAR MAIDEN TSAR TSAR IVAN TSAR MAIDEN MAIDEN TSAR KONEK IVAN KONEK RAVEN FLY KONEK WHALE KONEK WHALE IVAN WHALE IVAN IVAN KONEK IVAN MOON IVAN MOON IVAN MOON IVAN MOON IVAN MOON IVAN MOON MOON WHALE KONEK KONEK KONEK SAILORS WHALE IVAN WHALE WHALE STURGEON WHALE DOLPHINS RUFF DOLPHINS RUFF WHALE WHALE RUFF WHALE WHALE RUFF CROWD RUFF RUFF IVAN WHALE WHALE KONEK IVAN KONEK TSAR IVAN TSAR MAIDEN TSAR MAIDEN TSAR MAIDEN TSAR MAIDEN TSAR MAIDEN TSAR MAIDEN IVAN TSAR IVAN TSAR KONEK IVAN KONEK KONEK TSAR TSAR IVAN CROWD MAIDEN CROWD CROWD""".split()
assert len(RUS) == len(SP), (len(RUS), len(SP))
speaker_of = ["NARRATOR"] * len(d)
for (a, b), s in zip(SP, RUS):
    for i in range(a, b + 1): speaker_of[i] = s

NAMES = {"I": "Ivan and the Golden Horses", "II": "The Firebird and the Tsar-Maiden", "III": "The Whale, the Moon and the Cauldrons"}
RU_NAMES = {"I": "Иван и золотогривые кони", "II": "Жар-птица и Царь-девица", "III": "Кит, Месяц и котлы"}
KEYS = list(NAMES)
FILES = {"I": ["tr/I.txt"], "II": ["tr/II_a.txt", "tr/II_b.txt"], "III": ["tr/III_a.txt"]}
ALIAS = {"N": "NARRATOR", "PEOPLE": "CROWD"}

def pieces(text):
    out = []
    for ln in text.strip("\n").split("\n"):
        m = re.match(r"\[([A-Z0-9]+)\] ?(.*)$", ln)
        if m: out.append([ALIAS.get(m.group(1), m.group(1)), m.group(2)])
        else: out[-1][1] += "\n" + ln
    return out

PARAS = []   # (part, line a, line b, art, text)
for part in KEYS:
    for fn in FILES[part]:
        for chunk in re.split(r"(?m)^@ ", open(fn, encoding="utf-8").read())[1:]:
            head, body = chunk.split("\n", 1)
            rng, art = head.split()
            x, y = (rng.split("-") + [rng])[:2] if "-" in rng else (rng, rng)
            PARAS.append((part, BL[part][int(x)][0], BL[part][int(y)][1], art, body))
# every Russian line used exactly once, in order
flat = [(a, b) for _, a, b, _, _ in PARAS]
assert flat[0][0] == 0 and all(flat[i + 1][0] == flat[i][1] + 1 for i in range(len(flat) - 1)) and flat[-1][1] == len(d) - 1, "paragraph ranges do not tile the text"

T, S_, rows, sc_by_par, cnt = {k: [] for k in KEYS}, [], [], [], 0
ru_rows, ru_cnt = [{"id": 1, "part": "I", "paragraph": 0, "speaker": "NARRATOR", "text": "Конёк-горбунок. Русская сказка. Пётр Ершов."}], 1
par_in_part, src_by_part = {}, {k: [] for k in KEYS}
for part, a, b, art, text in PARAS:
    pi = par_in_part[part] = par_in_part.get(part, 0) + 1
    src_by_part[part].append("\n".join(d[a:b + 1]))
    pcs = pieces(text)
    T[part].append("\n".join(t for s, t in pcs))
    first = True
    for s, t in pcs:
        cnt += 1
        rows.append({"id": cnt, "part": part, "paragraph": pi, "speaker": s, "text": t.replace("\n", " ")})
        if first: sc_by_par.append((cnt, art)); first = False
    i = a
    while i <= b:
        j = i
        while j + 1 <= b and speaker_of[j + 1] == speaker_of[i]: j += 1
        ru_cnt += 1
        ru_rows.append({"id": ru_cnt, "part": part, "paragraph": pi, "speaker": speaker_of[i], "text": "\n".join(d[i:j + 1])})
        i = j + 1
for part in KEYS: S_.append({"part": part, "paragraphs": src_by_part[part], "other_blocks": []})
assert "\n".join(l for r in ru_rows[1:] for l in r["text"].split("\n")) == "\n".join(d), "the Russian text changed"

INTRO = ("The Little Humpbacked Horse. A Russian fairy tale in verse by Pyotr Yershov, first told in eighteen thirty-four. Make yourself comfortable, and listen. "
         "It is a story about Ivan the fool, who is not a fool at all, a tiny magic horse with two humps and ears a yard long, a bird made of fire, "
         "a Tsar-Maiden from the sea, a whale with a village on his back, and three great cauldrons.")
OUTRO = "And that is the end of the tale. Thank you for listening, and sleep well."
rows.insert(0, {"id": 0, "part": "I", "paragraph": 0, "speaker": "NARRATOR", "text": INTRO})
rows.append({"id": 0, "part": "III", "paragraph": len(T["III"]) + 1, "speaker": "NARRATOR", "text": OUTRO})
for i, r in enumerate(rows, 1): r["id"] = i
sc = []
for i, a in sc_by_par:
    i += 1
    if not sc or sc[-1]["art"] != a: sc.append({"id": i, "art": a})
sc[0]["id"] = 1
json.dump(T, open("translation_en.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(S_, open("source_clean.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(rows, open("The_Little_Humpbacked_Horse_voice_script.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(ru_rows, open("The_Little_Humpbacked_Horse_voice_script_ru.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(sc, open("scenes.json", "w"), indent=1)
with open("The_Little_Humpbacked_Horse_voice_script.md", "w", encoding="utf-8") as f:
    cur = None
    for r in rows:
        if r["part"] != cur: cur = r["part"]; f.write(f"\n## {cur} · {NAMES[cur]}\n\n")
        f.write(f"**{r['speaker']}**: {r['text']}\n\n")
V = lambda v, s: {"voice": v, "speed": s, "lang": "en-gb"}
json.dump({"NARRATOR": V("bm_george", .92), "IVAN": V("bm_fable", .95), "KONEK": V("bf_lily", .97), "TSAR": V("bm_lewis", .88), "DANILO": V("bm_daniel", .95),
           "GAVRILO": V("bm_lewis", .96), "FATHER": V("bm_lewis", .8), "MARE": V("bf_emma", .9), "WARDEN": V("bm_daniel", .85), "HERALD": V("bm_lewis", 1.0),
           "MERCHANT": V("bm_fable", 1.05), "GUARD": V("bm_daniel", 1.0), "CHAMBERLAIN": V("bm_daniel", .84), "NOBLE": V("bm_george", .95), "SERVANT": V("bm_fable", .9),
           "COOKS": V("bf_isabella", .9), "HUNTER": V("bm_daniel", .95), "MAIDEN": V("bf_alice", .92), "MOON": V("bf_isabella", .85), "WHALE": V("bm_lewis", .8),
           "RUFF": V("bm_fable", 1.1), "DOLPHINS": V("bf_lily", 1.05), "STURGEON": V("bm_george", .85), "CROWD": V("bm_daniel", 1.0), "SAILORS": V("bm_daniel", .95),
           "RAVEN": V("bf_emma", .85), "FLY": V("bf_lily", 1.1)}, open("voices_kokoro.json", "w"), indent=1)
G = {"NARRATOR": "Sulafat", "IVAN": "Puck", "KONEK": "Achird", "TSAR": "Algieba", "DANILO": "Orus", "GAVRILO": "Fenrir", "FATHER": "Charon", "MARE": "Vindemiatrix",
     "WARDEN": "Rasalgethi", "HERALD": "Alnilam", "MERCHANT": "Zubenelgenubi", "GUARD": "Iapetus", "CHAMBERLAIN": "Enceladus", "NOBLE": "Schedar", "SERVANT": "Sadaltager",
     "COOKS": "Despina", "HUNTER": "Algenib", "MAIDEN": "Aoede", "MOON": "Kore", "WHALE": "Umbriel", "RUFF": "Sadachbia", "DOLPHINS": "Leda", "STURGEON": "Laomedeia",
     "CROWD": "Fenrir", "SAILORS": "Orus", "RAVEN": "Charon", "FLY": "Callirrhoe"}
json.dump({k: {"voice": v, "style": ""} for k, v in G.items()}, open("voices_gemini.json", "w"), indent=1)
used_en = {r["speaker"] for r in rows}; used_ru = {r["speaker"] for r in ru_rows}
assert used_en <= set(G) and used_ru <= set(G), (used_en - set(G), used_ru - set(G))
w = sum(len(r["text"].split()) for r in rows)
print(len(rows), "EN rows,", w, "words, about", round(w / 150, 1), "min at 150 wpm;", len(ru_rows), "RU rows; scenes", len(sc), "; paragraphs", sum(len(v) for v in T.values()))
print({k: sum(len(t.split()) for t in v) for k, v in T.items()}, "ru-only speakers:", used_ru - used_en)
