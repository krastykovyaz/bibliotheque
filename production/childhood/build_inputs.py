#!/usr/bin/env python3
"""Childhood: translation_en.json, source_clean.json, voice script, voices_kokoro.json, book.json from tr/chNN.json, raw/clean.json and scenes_def/ep*.json."""
import json, re, glob
RO = "I II III IV V VI VII VIII IX X XI XII XIII XIV XV XVI XVII XVIII XIX XX XXI XXII XXIII XXIV XXV XXVI XXVII XXVIII".split()
raw = json.load(open("raw/clean.json", encoding="utf-8"))
EN_NAMES = ["The Tutor Karl Ivanych", "Maman", "Papa", "Lessons", "The Holy Fool", "Preparing for the Hunt", "The Hunt", "Games", "Something Like a First Love",
            "What Sort of Man Was My Father?", "Work in the Study and the Drawing Room", "Grisha", "Natalya Savishna", "The Parting", "Childhood", "Verses",
            "Princess Kornakova", "Prince Ivan Ivanovich", "The Ivins", "The Guests Gather", "Before the Mazurka", "The Mazurka", "After the Mazurka", "In Bed",
            "The Letter", "What Awaited Us in the Country", "Grief", "The Last Sad Memories"]
RU_NAMES = [c["title"] for c in raw]
parts = RO; names = dict(zip(RO, EN_NAMES))
TAG = re.compile(r"\[\[([A-Z]+)\]\]")
def split_long(t, n=130):
    sents = re.split(r"(?<=[.!?…”])\s+(?=[“A-Z])", t); out, cur, c = [], [], 0
    for s in sents:
        w = len(s.split())
        if cur and c + w > n: out.append(" ".join(cur)); cur, c = [], 0
        cur.append(s); c += w
    if cur: out.append(" ".join(cur))
    return out
T, S, rows, n = {}, [], [], 0
first = {}
for i, c in enumerate(raw):
    p = RO[i]; en = json.load(open(f"tr/ch{c['num']:02d}.json", encoding="utf-8"))
    assert len(en) == len(c["paras"]), (c["num"], len(en), len(c["paras"]))
    T[p] = [re.sub(r"\s+", " ", TAG.sub("", t)).strip() for t in en]
    S.append({"part": p, "paragraphs": c["paras"], "other_blocks": []})
    for k, t in enumerate(en, 1):
        bits = TAG.split(t); segs = [("NARRATOR", bits[0])] + [(bits[j], bits[j + 1]) for j in range(1, len(bits), 2)]
        for sp, tx in segs:
            tx = re.sub(r"\s+", " ", tx).strip()
            if not tx: continue
            for ch in (split_long(tx) if len(tx.split()) > 140 else [tx]):
                n += 1; rows.append({"id": n, "part": p, "paragraph": k, "speaker": sp, "text": ch}); first.setdefault((p, k), n)
json.dump(T, open("translation_en.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(S, open("source_clean.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(rows, open("Childhood_voice_script.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
with open("Childhood_voice_script.md", "w", encoding="utf-8") as f:
    cur = None
    for r in rows:
        if r["part"] != cur: cur = r["part"]; f.write(f"\n## {cur} · {names[cur]}\n\n")
        f.write(f"**{r['speaker']}**: {r['text']}\n\n")
V = lambda v, s: {"voice": v, "speed": s, "lang": "en-gb"}
voices = {"NARRATOR": V("bm_george", .95), "KARL": V("bm_daniel", .9), "PAPA": V("bm_lewis", .95), "MAMAN": V("bf_emma", .95), "VOLODYA": V("bm_fable", 1.0),
          "NATALYA": V("bf_isabella", .95), "GRANDMOTHER": V("bf_isabella", .82), "GRISHA": V("bm_daniel", .8), "GIRL": V("bf_emma", 1.1), "JEROME": V("bm_daniel", 1.05),
          "PRINCE": V("bm_lewis", .85), "LADY": V("bf_isabella", 1.05), "BOY": V("bm_fable", 1.12), "MAN": V("bm_lewis", 1.08)}
used = {r["speaker"] for r in rows}; assert used <= set(voices), used - set(voices)
json.dump(voices, open("voices_kokoro.json", "w"), indent=1)
# scenes
scenes, art, alt, focus, fx = [], {}, {}, {}, {}
import os
for e in ("1", "1x", "2", "2x", "3", "3x", "4", "4x"):
  if os.path.exists(f"scenes_def/ep{e}.json"):
    for s in json.load(open(f"scenes_def/ep{e}.json", encoding="utf-8")):
        p = RO[s["ch"] - 1]
        scenes.append({"id": first[(p, s["para"] + 1)], "art": s["art"]})
        alt[s["art"]] = s["alt"]; focus[s["art"]] = s["focus"]
        if s.get("fx"): fx[s["art"]] = s["fx"]
        if s.get("key"): art[p] = s["art"]
scenes.sort(key=lambda a: a["id"])
assert len(art) == 28 and len({a["id"] for a in scenes}) == len(scenes)
words = {p: sum(len(x.split()) for x in T[p]) for p in parts}
EPS = [("Karl Ivanych, Maman and Papa", "I", "VI", "05a_holy_fool", "A boy wakes in his country home, loved and scolded by his German tutor Karl Ivanych. Maman pours tea, Papa prepares to leave, lessons end badly, and a holy fool comes to dinner: Tolstoy's first memories of childhood."),
       ("The Hunt, First Love and Grisha", "VII", "XIII", "12b_grisha_prays", "A day's hunt in the birch wood, a game in the shade, a first stirring of love, a portrait of Papa the gambler, and a night when a boy hides to hear the holy fool Grisha pray. Then the life story of the old nurse Natalya Savishna."),
       ("Farewell to the Country and Moscow", "XIV", "XVIII", "14a_farewell_porch", "The family leaves the country for Moscow in tears. At Grandmother's house Nikolenka struggles to write a birthday poem, meets Princess Kornakova and Prince Ivan Ivanovich, and overhears what he was never meant to hear."),
       ("The Ivins and the Ball", "XIX", "XXIV", "21a_hunt_for_gloves", "The Ivin boys come to visit, the house is made ready for Grandmother's name-day ball, and Nikolenka learns what it is to be small among the grown-up dancers, and what it is to be unfaithful in love."),
       ("The Letter and the Last Sad Memories", "XXV", "XXVIII", "27a_night_coffin", "A letter from the country calls the family home. Maman is dying, and Nikolenka learns what grief is. The end of childhood, and the old nurse who is remembered to the end.")]
episodes = [{"title": t, "from_part": a, "to_part": b, "thumb_art": th, "blurb": bl} for t, a, b, th, bl in EPS]
for e in episodes: assert e["thumb_art"] in alt, e["thumb_art"]
est = lambda a, b: sum(words[p] for p in parts[parts.index(a):parts.index(b) + 1]) / 150
for e in episodes: print(e["title"], "%.1f min" % est(e["from_part"], e["to_part"]))
print(n, "rows,", sum(words.values()), "EN words, %.0f min total" % (sum(words.values()) / 150), len(scenes), "scenes")
B = {"slug": "childhood", "prefix": "Childhood", "lang": "en", "title": "Childhood", "author": "Leo Tolstoy", "author_ru": "Лев Толстой", "year": 1852,
 "title_original": "Детство", "publication_note": "first published in the magazine «Современник» (The Contemporary), St Petersburg, 1852",
 "source_note": "Text from ru.wikisource.org, after L. N. Tolstoy, Complete Works in 90 volumes, vol. 1.", "translated_from": "the Russian original",
 "parts": parts, "names": names, "art": art, "scenes": scenes, "art_alt": alt, "focus": focus, "fx": fx, "episodes": episodes,
 "glossary": [["Maman", "the French word for “mummy”, as upper-class Russian children called their mother; Papa is the father."],
  ["Karl Ivanych", "Karl Ivanovich, the German tutor; a Russian first name and patronymic as the family says them."],
  ["holy fool (yurodivy)", "a wandering pilgrim thought to be touched by God, who wore chains, prayed aloud and spoke truths to the powerful."],
  ["verst", "a Russian measure of distance, about 1.07 kilometres."],
  ["kopeck, rouble", "a hundred kopecks make one rouble."],
  ["linyeika", "a long open carriage with a bench on which the passengers sit sideways."],
  ["britzka", "a light open travelling carriage."],
  ["name-day", "the feast day of the saint whose name a person bears, celebrated like a birthday."],
  ["mazurka", "a lively Polish dance, the high point of a ball."],
  ["serf", "a peasant owned by the landowner and bound to his estate; most of the servants in the book are serfs."]],
 "thumb_art": "27a_night_coffin", "thumb_position": "50% 50%", "thumb_sub": "A NOVELLA<br>FULL-CAST AUDIOBOOK", "cover_bg": ["#1d2a3a", "#e8dcc0"],
 "summary": "Ten-year-old Nikolenka wakes on an August morning in the country house where he was born. Through his eyes: the German tutor, Maman, Papa, the holy fool, the hunt, a first love, Moscow, the ball, and the day his mother dies. Tolstoy's first published work.",
 "site_description": "Tolstoy's first published work (1852), the first part of his autobiographical trilogy. Nikolenka Irtenev, ten years old, tells the happiest and saddest days of his boyhood: the German tutor Karl Ivanych, Maman at the tea table, Papa the gambler, a holy fool at night, a hunt, a first love, a children's ball in Moscow, and the death of his mother. The book is Tolstoy's farewell to a lost paradise of childhood.",
 "tags": ["Tolstoy", "Leo Tolstoy", "Childhood", "audiobook", "full cast audiobook", "novella", "coming of age", "classic literature", "Russian literature", "autobiographical", "public domain", "English audiobook"],
 "hashtags": "#Tolstoy #audiobook #classicliterature #russianliterature #publicdomain", "playlist": "PLVuswr3XMg9E",
 "text_note": "German and French phrases are given in English.",
 "ru": {"title": "Детство", "author": "Лев Толстой", "names": dict(zip(RO, RU_NAMES)),
        "note": "Повесть в издании для чтения с оригинальными иллюстрациями.",
        "source_note": "Текст с ru.wikisource.org, по изданию: Л. Н. Толстой, Полное собрание сочинений в 90 томах, т. 1.",
        "contents": "Содержание", "back": "О тексте",
        "small": "Текст повести находится в общественном достоянии. Иностранные фразы даны как в оригинале. Названия глав и иллюстрации сделаны для этого издания. Набрано шрифтом Lora (SIL Open Font License).",
        "description": "Десятилетний Николенька просыпается августовским утром в родном доме. Учитель Карл Иваныч, maman, папа, юродивый, охота, первая любовь, Москва, бал и день, когда умирает мать. Первое произведение Толстого (1852)."}}
json.dump(B, open("book.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
