#!/usr/bin/env python3
"""Merges the translated chunks into translation_en.json (parts -> paragraphs; "§ ..." paragraphs are letter headings)
and builds the multi-voice script Poor_Folk_voice_script.json/.md, source_clean.json (Russian, same structure) and voices_kokoro.json."""
import json, glob, re, os
PARTS = {  # part -> (name, name_ru, first letter, last letter)
 "I": ("April", "Апрель", 1, 6), "II": ("May", "Май", 7, 7), "III": ("The Notebook", "Тетрадь", 8, 8),
 "IV": ("June", "Июнь", 9, 17), "V": ("July", "Июль", 18, 26), "VI": ("Early August", "Начало августа", 27, 33),
 "VII": ("Mid-August", "Середина августа", 34, 38), "VIII": ("September", "Сентябрь", 39, 48), "IX": ("The Last Letters", "Последние письма", 49, 54)}
def strip(t):
    return re.sub(r"\s{2,}", " ", t.replace("{{right|", "").replace("{{", "").replace("}}", "")).strip()
ru = json.load(open("letters.json", encoding="utf-8"))
for L in ru:
    L["paras"] = [strip(p) for p in L["paras"]]
tr = {}
for f in sorted(glob.glob("chunks/out_*.json")):
    d = json.load(open(f, encoding="utf-8"))
    for k, v in d.items():
        v["paragraphs"] = [strip(p) for p in v["paragraphs"]]
        tr[int(k)] = v
missing = [i for i in range(1, 55) if i not in tr]
if missing:
    raise SystemExit(f"translations missing for letters {missing}")
T, S, rows = {}, [], []
n = 0
for part, (name, name_ru, a, b) in PARTS.items():
    T[part], rus = [], []
    para = 0
    for i in range(a, b + 1):
        L, E = ru[i - 1], tr[i]
        if len(L["paras"]) != len(E["paragraphs"]):
            raise SystemExit(f"letter {i}: {len(L['paras'])} Russian paragraphs, {len(E['paragraphs'])} English")
        who = "VARENKA" if L["from"] == "Varenka" else "MAKAR"
        head = f"{E['date']}."
        T[part].append("§ " + E["date"]); rus.append("§ " + L["date"])
        para += 1; n += 1
        rows.append({"id": n, "part": part, "paragraph": para, "speaker": "NARRATOR",
                     "text": f"{head} {'Makar Alexeyevich writes.' if who == 'MAKAR' else 'Varvara Alexeyevna writes.'}"})
        for k, (p_en, p_ru) in enumerate(zip(E["paragraphs"], L["paras"])):
            if i == 54 and k == 7:      # Makar's answer is fused into Varenka's last letter in the source: it is a letter of its own
                who = "MAKAR"
                T[part].append("§ " + E["date"]); rus.append("§ " + L["date"])
                para += 1; n += 1
                rows.append({"id": n, "part": part, "paragraph": para, "speaker": "NARRATOR", "text": f"{E['date']}. Makar Alexeyevich writes."})
            T[part].append(p_en); rus.append(p_ru)
            if p_en.startswith("§ "):       # notebook section marker: not spoken
                continue
            para += 1; n += 1
            rows.append({"id": n, "part": part, "paragraph": para, "speaker": who, "text": p_en})
    S.append({"part": part, "paragraphs": rus, "other_blocks": []})
json.dump(T, open("translation_en.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(S, open("source_clean.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(rows, open("Poor_Folk_voice_script.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
with open("Poor_Folk_voice_script.md", "w", encoding="utf-8") as f:
    cur = None
    for r in rows:
        if r["part"] != cur:
            cur = r["part"]; f.write(f"\n## {cur} · {PARTS[cur][0]}\n\n")
        f.write(f"**{r['speaker']}**: {r['text']}\n\n")
json.dump({"NARRATOR": {"voice": "bm_george", "speed": 0.95, "lang": "en-gb"},
           "MAKAR": {"voice": "bm_lewis", "speed": 0.97, "lang": "en-gb"},
           "VARENKA": {"voice": "bf_emma", "speed": 0.98, "lang": "en-gb"}}, open("voices_kokoro.json", "w"), indent=1)
w = sum(len(p.split()) for ps in T.values() for p in ps)
print(f"{len(rows)} spoken segments, {w} English words, {len(T)} parts")
