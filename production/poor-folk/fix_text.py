#!/usr/bin/env python3
"""Text fixes found in the translation check (2026-11-25). Changes translation_en.json and source_clean.json only
(the reading text and PDFs); the voice script and the audio stay as recorded.
- letter of September 27 (Varenka): Wikisource footnotes were fused into the text and broke one paragraph into three
- doubled quote marks, Phaldoni -> Faldoni, Evstafy -> Yevstafy"""
import json, re
T = json.load(open("translation_en.json", encoding="utf-8"))
S = json.load(open("source_clean.json", encoding="utf-8"))
def fix_en(p):
    return p.replace('""', '"').replace("Phaldoni", "Faldoni").replace("Evstafy", "Yevstafy").replace("YYevstafy", "Yevstafy")
for part in T:
    T[part] = [fix_en(p) for p in T[part]]
# the broken paragraph: find it by its fragments
def merge(lst, is_mid, clean):
    for i, p in enumerate(lst):
        if is_mid(p):
            lst[i - 1:i + 2] = [clean(lst[i - 1].rstrip() + lst[i] + " " + lst[i + 1].lstrip(". "))]
            return True
    return False
ok_en = merge(T["IX"], lambda p: p.startswith("; that it must be embroidered"), lambda s: s.replace("about the kanzu;", "about the canezou;"))
src = next(x for x in S if x["part"] == "IX")["paragraphs"]
ok_ru = merge(src, lambda p: p.startswith("; что его нужно вышивать"), lambda s: s.replace("канзуКанзу () — лёгкая кофточка без рукавов.", "канзу").replace("крошьюКрошь () — крючок.", "крошью."))
print("merged:", ok_en, ok_ru, "| paragraphs IX:", len(T["IX"]), len(src))
json.dump(T, open("translation_en.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(S, open("source_clean.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
