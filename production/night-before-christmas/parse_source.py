#!/usr/bin/env python3
"""Clean the raw ru.wikisource wikitext into paragraphs (paras_ru.json). Footnotes (<ref>) are dropped."""
import re, json
t = open("raw/night.wiki", encoding="utf-8").read()
t = t[t.index("}}\nПоследний") + 3:]
t = t[:t.index("----\n\n{{Примечания}}")]
t = re.sub(r"<ref[^>]*>.*?</ref>", "", t, flags=re.S)
t = re.sub(r"<ref[^>]*/>", "", t)
t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
t = t.replace("{{***}}", "\n\n@@BREAK@@\n\n")
# poem templates: {{poemx1||\n lines \n}}  -> lines joined by newline
t = re.sub(r"\{\{poemx1\|\|", "@@P@@", t)
for _ in range(4):
    t = re.sub(r"\{\{(?:langi|lang)\|[a-z]+\|([^{}]*)\}\}", r"\1", t)
    t = re.sub(r"\{\{(?:nobr|nowrap)\|([^{}]*)\}\}", r"\1", t)
t = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", t)
t = re.sub(r"<br\s*/?>", "\n", t)
t = re.sub(r"<[^>]+>", "", t)
t = t.replace("'''", "").replace("''", "").replace("\xa0", " ")
open("raw/after_clean.txt", "w", encoding="utf-8").write(t)
print([m.group() for m in re.finditer(r"\{\{[^}]*\}\}", t)][:20])
t = re.sub(r"\|\}\}", "", t)
t = t.replace("@@P@@", "")
blocks = [re.sub(r"\s*\n\s*", " ", b).strip() for b in re.split(r"\n\s*\n", t)]
blocks = [b for b in blocks if b]
json.dump(blocks, open("paras_ru.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(blocks), sum(len(b.split()) for b in blocks))
