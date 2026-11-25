#!/usr/bin/env python3
"""Raw wikitext -> paras_ru.json (templates, categories, links, html removed; headings dropped)."""
import re, json
t = open("raw/boy.wiki", encoding="utf-8").read()
t = t.split("__NOTOC__")[1]
t = re.sub(r"\[\[Категория:[^\]]*\]\]|\[\[fr:[^\]]*\]\]", "", t)
t = re.sub(r"<ref[^>]*>.*?</ref>", "", t, flags=re.S)
# the poem template -> plain two lines
def poem(m):
    inner = re.sub(r"<[^>]+>", "", m.group(1))
    return "\n\n" + " ".join(x.strip() for x in inner.strip().splitlines() if x.strip()) + "\n\n"
t = re.sub(r"\{\{poem1\|\|(.*?)\|\}\}", poem, t, flags=re.S)
t = re.sub(r"^=+.*?=+\s*$", "", t, flags=re.M)
t = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", t)
t = re.sub(r"<[^>]+>", "", t)
paras = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", t)]
paras = [p for p in paras if p]
json.dump(paras, open("paras_ru.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for i, p in enumerate(paras): print(i, len(p.split()), p[:50], "...", p[-40:])
