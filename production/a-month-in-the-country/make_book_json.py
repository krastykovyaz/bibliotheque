#!/usr/bin/env python3
"""Writes book.json (run after build_inputs.py and make_art_month.py; edit afterwards if needed). Keeps series_playlist if already set."""
import json, os
plan = json.load(open("scenes_plan.json"))
old = json.load(open("book.json", encoding="utf-8")) if os.path.exists("book.json") else {}
names = {"I": "The Drawing-Room", "II": "The Garden", "III": "The Confession", "IV": "The Stone Hall", "V": "The Parting"}
b = {
 "slug": "a-month-in-the-country", "prefix": "A_Month_in_the_Country", "lang": "en", "title": "A Month in the Country", "author": "Ivan Turgenev",
 "author_ru": "Иван Тургенев", "year": 1855, "title_original": "Месяц в деревне",
 "publication_note": "a comedy in five acts, written 1848–1850, first printed in «Sovremennik», 1855",
 "source_note": "Text from ru.wikisource.org (the page «Месяц в деревне»).", "translated_from": "the Russian original",
 "parts": ["I", "II", "III", "IV", "V"], "names": names,
 "art": {"I": "1_cards", "II": "2_kite", "III": "3_confidence", "IV": "4_hall", "V": "5_parting"},
 "scenes": plan["scenes"], "art_alt": plan["art_alt"], "focus": plan["focus"], "fx": plan["fx"],
 "episodes": [
  {"title": "The New Tutor", "from_part": "I", "to_part": "I", "thumb_art": "1_cards", "blurb": "A summer afternoon on the Islayev estate. Natalya Petrovna is bored with her devoted friend Rakitin, the cards go round, and a young student, Belyaev, arrives as tutor to her son. The doctor Shpigelsky has a proposal for the ward Vera."},
  {"title": "Raspberries and a Kite", "from_part": "II", "to_part": "II", "thumb_art": "2_kite", "blurb": "In the garden Vera and Belyaev make a kite, the maid Katya is courted by two men, and the shy neighbour Bolshintsov is coached by the doctor in how to propose. Natalya Petrovna watches the young people and cannot hide her new feelings from Rakitin."},
  {"title": "Natalya Petrovna's Secret", "from_part": "III", "to_part": "III", "thumb_art": "3_confidence", "blurb": "Natalya Petrovna tries to marry her ward off, draws out Vera's secret and discovers her own. Rakitin names what is happening to her, and she summons Belyaev to dismiss him."},
  {"title": "The Declaration", "from_part": "IV", "to_part": "IV", "thumb_art": "4_hall", "blurb": "In an empty hall in the evening light the doctor proposes to the companion Lizaveta Bogdanovna, Vera confronts her guardian, and Natalya Petrovna and Belyaev say what they must not say."},
  {"title": "The Parting", "from_part": "V", "to_part": "V", "thumb_art": "5_parting", "blurb": "The morning after. Islayev asks his oldest friend the question he fears, Rakitin leaves, Belyaev leaves, Vera decides her future, and the household is left with what was said."}],
 "glossary": [["Natalya Petrovna", "Russians are addressed by first name and patronymic: Natalya, daughter of Pyotr; Arkady Sergeich is Arkady, son of Sergei. Close friends and family use short forms: Natasha, Arkasha, Verochka, Mishel (Michel)."],
   ["preference", "a Russian card game for three or four, played at the card table in Act One."], ["whist", "a card game for four players, a favourite pastime of country houses."],
   ["souls", "serfs; an estate was counted by its number of “souls” (male serfs), so “three hundred souls” means a wealthy landowner."],
   ["verst", "a Russian measure of distance, a little over a kilometre."], ["ward", "a girl brought up in a household as its dependent; Vera is an orphan raised by Natalya's family."],
   ["name-day", "the feast day of a person's saint, celebrated like a birthday; Natalya Petrovna's is a week away."], ["troika", "a carriage drawn by three horses; the doctor's reward for matchmaking."],
   ["tutor", "a young man hired to teach the family's son, here for the summer months."], ["Monte Cristo", "the novel by Alexandre Dumas that Rakitin reads aloud in the opening scene."],
   ["Talleyrand", "the famously crafty French diplomat; Natalya Petrovna mocks the doctor as a “district Talleyrand”."]],
 "thumb_art": "2_kite", "thumb_position": "50% 50%", "thumb_sub": "A PLAY IN FIVE ACTS<br>FULL-CAST AUDIOBOOK", "cover_bg": ["#22405a", "#7fa656"],
 "summary": "One summer month on a Russian country estate: a bored, clever wife, her devoted friend, a young student tutor and an innocent ward. Turgenev's play, a story of love told in dramatic form, in a full-cast English audiobook.",
 "site_description": "On the Islayev estate, in the early 1840s, Natalya Petrovna is bored with her loyal friend Rakitin until a twenty-one-year-old student, Belyaev, arrives as her son's tutor. Her seventeen-year-old ward Vera falls in love with him too, the doctor Shpigelsky and the shy neighbour Bolshintsov scheme over a marriage, and a month in the country changes everyone. Turgenev called it «a tale in dramatic form»; it became one of the most staged Russian plays. Full cast, five acts, English translation.",
 "tags": ["Turgenev", "Ivan Turgenev", "A Month in the Country", "audiobook", "full cast audiobook", "play", "radio play", "classic literature", "Russian literature", "drama", "public domain", "English audiobook"],
 "hashtags": "#Turgenev #audiobook #classicliterature #russianliterature #publicdomain", "playlist": "PLVuswr3XMg9E",
 "text_note": "Stage directions are shortened: cues of tone or of whom a speaker addresses are left out.",
 "ru": {"title": "Месяц в деревне", "author": "Иван Тургенев", "names": {"I": "Гостиная", "II": "Сад", "III": "Признание", "IV": "Сени", "V": "Прощание"},
        "note": "Пьеса в издании для чтения с оригинальными иллюстрациями.", "source_note": "Текст с ru.wikisource.org (страница «Месяц в деревне»).",
        "contents": "Содержание", "back": "О тексте",
        "small": "Текст пьесы находится в общественном достоянии. Названия действий и иллюстрации сделаны для этого издания; имя говорящего набрано заглавными. Набрано шрифтом Lora (SIL Open Font License).",
        "description": "Лето в усадьбе Ислаевых. Наталья Петровна скучает рядом с преданным другом Ракитиным, пока в доме не появляется молодой студент Беляев, учитель её сына. В него влюбляется и семнадцатилетняя воспитанница Вера. Пьеса Тургенева «Месяц в деревне»."}}
if "series_playlist" in old: b["series_playlist"] = old["series_playlist"]
json.dump(b, open("book.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("book.json written:", len(b["scenes"]), "scenes")
