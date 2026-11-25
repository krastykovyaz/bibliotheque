#!/usr/bin/env python3
"""Russian voice script (The_Girl_Snow_Maiden_voice_script_ru.json) from source_clean.json: the author's text only SPLIT by speaker.
Same schema as the English script (id, part, paragraph, speaker, text); paragraph numbers are the 1-based numbers in source_clean.json,
paragraph 0 is the spoken title. Poem lines written "a / b / c" in the source are put on separate lines (a newline instead of " / ").
Every paragraph is checked: its pieces, joined with spaces, must give back exactly the source paragraph."""
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
src = json.load(open("source_clean.json", encoding="utf-8"))
TITLE = "Девочка Снегурочка. Сказка Владимира Даля."
N = "NARRATOR"
# who speaks a whole paragraph (everything not listed is the narrator); a list = pieces cut after the given text, speaker for each
WHOLE = {("I", 2): "OLDMAN", ("II", 1): "SNOW", ("II", 3): "OLDMAN", ("II", 4): "OLDMAN", ("III", 2): "FOX",
         ("V", 1): "BEAR", ("V", 2): "SNOW", ("V", 3): "BEAR", ("V", 4): "SNOW", ("V", 6): "WOLF", ("V", 7): "SNOW", ("V", 8): "WOLF",
         ("V", 9): "SNOW", ("V", 11): "FOX", ("V", 12): "SNOW", ("V", 13): "FOX", ("V", 14): "SNOW", ("VI", 2): "SNOW",
         ("VII", 2): "OLDMAN", ("VII", 3): "OLDMAN"}
CUT = {("I", 4): [("OLDWOMAN", "— Что же будешь делать — нет, так и взять негде."), (N, None)],
       ("III", 4): [("OLDMAN", "— Иди,"), (N, "— говорит,"), ("OLDMAN", None)],
       ("IV", 3): [(N, "вот и влезла на дерево и кричит:"), ("SNOW", '"Ау! Ау!"'), (N, None)],
       ("VI", 1): [("DOG", "— Гам, гам, гам!"), (N, None)]}
rows = [{"id": 1, "part": "I", "paragraph": 0, "speaker": N, "text": TITLE}]
for p in src:
    for i, para in enumerate(p["paragraphs"], 1):
        key = (p["part"], i)
        if key in CUT:
            rest, pieces = para, []
            for sp, end in CUT[key]:
                if end is None:
                    pieces.append((sp, rest.strip()))
                else:
                    assert rest.startswith(end) or end in rest, (key, end)
                    k = rest.index(end) + len(end)
                    pieces.append((sp, rest[:k].strip())); rest = rest[k:]
        else:
            pieces = [(WHOLE.get(key, N), para)]
        assert " ".join(t for _, t in pieces) == para, key
        for sp, t in pieces:
            rows.append({"id": len(rows) + 1, "part": p["part"], "paragraph": i, "speaker": sp, "text": t.replace(" / ", "\n")})
json.dump(rows, open("The_Girl_Snow_Maiden_voice_script_ru.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(rows), "rows;", sum(len(r["text"].split()) for r in rows), "words")
for r in rows: print(r["id"], r["part"], r["paragraph"], r["speaker"], r["text"][:60].replace("\n", " / "))
