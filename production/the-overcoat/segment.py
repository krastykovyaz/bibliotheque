import json, re
ps = json.load(open("paras_ru.json", encoding="utf-8"))
out = []
for p in ps:
    if len(p.split()) <= 140: out.append(p); continue
    sents = re.split(r"(?<=[.!?…»])\s+(?=[«А-ЯЁ—])", p)
    cur, n = [], 0
    for s in sents:
        w = len(s.split())
        if cur and (n + w > 130 or (s.startswith("«") and n > 0 and n > 60)):
            out.append(" ".join(cur)); cur, n = [], 0
        cur.append(s); n += w
    if cur: out.append(" ".join(cur))
json.dump(out, open("segs_ru.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(out), [len(x.split()) for x in out])
