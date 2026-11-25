#!/usr/bin/env python3
"""Cleans raw/overcoat_pss1938.wiki into paras_ru.json (paragraphs of the 1842 text)."""
import re, json, unicodedata
t = open("raw/overcoat_pss1938.wiki", encoding="utf-8").read()
body = t.split('<div class="indent">', 1)[1].split("</div>", 1)[0]
body = re.sub(r"<ref[^>]*/>|<ref[^>]*>.*?</ref>", "", body, flags=re.S)
body = re.sub(r"\{\{lang[^|}]*\|[^|}]*\|([^}]*)\}\}", r"\1", body)
body = re.sub(r"\{\{[^}]*\}\}", "", body)
body = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", body)
body = re.sub(r"<[^>]+>", "", body)
body = body.replace("''", "")
body = unicodedata.normalize("NFC", body.replace("̀", "").replace("́", ""))
body = body.replace("\xa0", " ")
paras = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n+", body)]
paras = [p for p in paras if p]
json.dump(paras, open("paras_ru.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(paras), sum(len(p.split()) for p in paras))
