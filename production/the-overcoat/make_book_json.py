#!/usr/bin/env python3
"""Writes book.json for The Overcoat (run once; edit book.json afterwards if needed)."""
import json
parts = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
names = {"I": "A Certain Clerk", "II": "The Copyist", "III": "The Frost and the Tailor", "IV": "The Savings", "V": "The New Overcoat", "VI": "The Party",
         "VII": "The Empty Square", "VIII": "The Important Person", "IX": "The Fever", "X": "The Ghost"}
art = {"I": "1_office", "II": "2_lamp_desk", "III": "3_frost", "IV": "4_box", "V": "5_new_coat", "VI": "6_lit_window", "VII": "7_square", "VIII": "8_study", "IX": "9_sickbed", "X": "10_ghost_lamp"}
pool = {"I": ["1b_names", "1_office", "1c_snow_paper"], "II": ["2_lamp_desk", "2b_rubbish", "2c_evening_windows"],
        "III": ["3_frost", "3b_old_coat", "3c_stairs", "3d_tailor", "3e_snuffbox", "3f_sunday"], "IV": ["4_box", "4b_candle_work", "4c_cloth_shop"],
        "V": ["5_new_coat", "5b_fitting", "5c_porter"], "VI": ["6_lit_window", "6b_shop_picture", "6c_hall", "6d_whist"], "VII": ["7_square", "7b_robbed", "7c_police"],
        "VIII": ["8_study", "8b_anteroom", "8d_shouting", "8c_blizzard"], "IX": ["9_sickbed", "9b_empty_room", "9c_new_clerk"],
        "X": ["10b_bridge", "10d_watchman", "10c_sleigh", "10_ghost_lamp", "10e_obukhov"]}
alt = {
 "1_office": "A government office: clerks bent over slanted desks under tall windows, one small bald clerk by a candle at the end of the row",
 "1b_names": "A christening scene by candlelight: an open calendar on a table, two godparents standing, a mother in bed",
 "1c_snow_paper": "Young clerks jeering at a lone copyist while scraps of paper fall on his head like snow",
 "2_lamp_desk": "A hunched man copying papers at a table by one candle, a frosted window behind him",
 "2b_rubbish": "A man in a hat walking under a lit window just as melon rinds and rubbish are thrown out",
 "2c_evening_windows": "A tenement at night with card-players in many lit windows, and one dark window; a lone man walks home",
 "3_frost": "Clerks in thin overcoats hurrying through a frosty morning street, breath steaming, snow falling",
 "3b_old_coat": "A threadbare overcoat on a hook, worn through at the shoulders and back, a candle on a stool",
 "3c_stairs": "A steep back staircase wet with slops, smoke pouring from a kitchen door at the top, a man climbing",
 "3d_tailor": "A one-eyed tailor sitting cross-legged on a wide table with thread round his neck, a window glowing behind",
 "3e_snuffbox": "A round snuffbox with a general's portrait whose face is pasted over with a square of paper, an old coat behind",
 "3f_sunday": "A snowy lane on a Sunday morning, a man in an old coat at the tailor's door with a coin in his hand",
 "4_box": "A small locked savings box with a slit in the lid, copper and silver coins on a table, a candle",
 "4b_candle_work": "A man copying papers by the light of his landlady's candle, a warm stove behind",
 "4c_cloth_shop": "A cloth shop: bolts of cloth on shelves, a tailor and a customer choosing green cloth at the counter",
 "5_new_coat": "A new dark-green overcoat with a pale collar hanging on a hook, bathed in lamplight",
 "5b_fitting": "A tailor draping the new green overcoat over a clerk's shoulders",
 "5c_porter": "The porter's lodge of the department: rows of coats on hooks, the new green one in the middle, clerks gathering",
 "6_lit_window": "A tall house at night with a brightly lit window full of guests, a man in a new green overcoat in the snowy street",
 "6b_shop_picture": "A man in a green overcoat stopping before a lit shop window with a picture of a woman taking off her shoe",
 "6c_hall": "A hall with coats on every wall, rows of galoshes on the floor and a steaming samovar",
 "6d_whist": "Clerks playing cards by candlelight at a green table, a tea glass steaming at the side",
 "7_square": "A vast empty snowy square at night, a single sentry-box light far away, a small man in a green overcoat crossing it",
 "7b_robbed": "A man lying in the snow while two big dark figures walk away, one carrying a green overcoat",
 "7c_police": "A snowy police station with lit windows, a man in an old coat at the door, hat in hand",
 "8_study": "A general's study: a stern man at a great desk with an old friend, and a small clerk waiting by the wall",
 "8d_shouting": "A general in a green coat stamping his foot and raising an arm over a small trembling clerk, a friend looking on",
 "8b_anteroom": "An anteroom with rows of empty chairs and a door ajar to a lit study, a secretary with papers",
 "8c_blizzard": "A man staggering through a blizzard between lamp-lit houses, wind and snow all around",
 "9_sickbed": "A sick man in bed by a candle, an old landlady and a doctor standing by",
 "9b_empty_room": "A bare room after a death: an old dressing gown on a hook, a few quills and paper on a table, three socks",
 "9c_new_clerk": "The office again, a new taller clerk sitting in the old place and writing in a slanting hand",
 "10_ghost_lamp": "A pale ghost of a clerk under a gas lamp, hand at the collar of a man in a fine coat, snow falling",
 "10b_bridge": "An arched bridge over a dark canal at night, gas lamps and fog, a pale figure on the bridge",
 "10c_sleigh": "A night sleigh racing through snow, a man in a fur-collared coat and a ghost grasping his collar",
 "10d_watchman": "A watchman with a halberd and snuff horn, a ghost looming behind him in the snow",
 "10e_obukhov": "A huge pale ghost with great moustaches walking towards a bridge in the dark",
}
focus = {
 "1_office": [(.85, .6), (.3, .55), (.5, .3)], "1b_names": [(.42, .65), (.75, .6), (.2, .45)], "1c_snow_paper": [(.42, .5), (.25, .5), (.6, .45)],
 "2_lamp_desk": [(.38, .65), (.5, .7), (.75, .4)], "2b_rubbish": [(.22, .4), (.35, .8), (.7, .55)], "2c_evening_windows": [(.5, .4), (.85, .75), (.2, .65)],
 "3_frost": [(.45, .85), (.3, .9), (.7, .45)], "3b_old_coat": [(.5, .45), (.5, .7), (.8, .75)], "3c_stairs": [(.4, .7), (.88, .2), (.2, .9)],
 "3d_tailor": [(.42, .58), (.7, .4), (.1, .2)], "3e_snuffbox": [(.5, .6), (.5, .5), (.85, .7)], "3f_sunday": [(.4, .85), (.52, .55), (.8, .3)],
 "4_box": [(.5, .6), (.2, .65), (.75, .8)], "4b_candle_work": [(.4, .6), (.7, .45), (.2, .85)], "4c_cloth_shop": [(.7, .7), (.2, .3), (.4, .85)],
 "5_new_coat": [(.5, .5), (.5, .3), (.75, .4)], "5b_fitting": [(.45, .55), (.65, .55), (.8, .4)], "5c_porter": [(.5, .45), (.3, .5), (.8, .75)],
 "6_lit_window": [(.45, .5), (.62, .9), (.8, .5)], "6b_shop_picture": [(.5, .4), (.12, .9), (.7, .5)], "6c_hall": [(.56, .75), (.3, .3), (.8, .3)], "6d_whist": [(.5, .65), (.3, .5), (.82, .7)],
 "7_square": [(.32, .88), (.66, .6), (.5, .5)], "7b_robbed": [(.35, .9), (.65, .6), (.85, .7)], "7c_police": [(.4, .85), (.55, .5), (.85, .8)],
 "8_study": [(.5, .4), (.35, .45), (.12, .9)], "8d_shouting": [(.4, .4), (.17, .9), (.7, .5)], "8b_anteroom": [(.6, .5), (.8, .85), (.2, .9)], "8c_blizzard": [(.5, .85), (.35, .5), (.7, .5)],
 "9_sickbed": [(.35, .6), (.63, .55), (.9, .6)], "9b_empty_room": [(.5, .4), (.3, .72), (.75, .9)], "9c_new_clerk": [(.5, .6), (.5, .45), (.15, .7)],
 "10_ghost_lamp": [(.42, .8), (.5, .5), (.65, .88)], "10b_bridge": [(.5, .5), (.3, .5), (.7, .55)], "10c_sleigh": [(.4, .7), (.52, .7), (.75, .75)],
 "10d_watchman": [(.33, .85), (.62, .9), (.5, .45)], "10e_obukhov": [(.44, .8), (.7, .7), (.3, .5)]}
snow = "2b_rubbish 2c_evening_windows 3_frost 3f_sunday 6_lit_window 6b_shop_picture 7_square 7b_robbed 7c_police 8c_blizzard 10_ghost_lamp 10b_bridge 10c_sleigh 10d_watchman 10e_obukhov".split()
flick = "8d_shouting 1_office 1b_names 2_lamp_desk 3b_old_coat 3c_stairs 3d_tailor 3e_snuffbox 4_box 4b_candle_work 5_new_coat 6c_hall 6d_whist 8_study 9_sickbed 9b_empty_room".split()
fx = {**{k: "snow" for k in snow}, **{k: "flicker" for k in flick}}
words = {"I": 1203, "II": 1038, "III": 2426, "IV": 1080, "V": 891, "VI": 998, "VII": 1175, "VIII": 1487, "IX": 656, "X": 1810}
SCENES = [(0, "1_office"), (2, "1b_names"), (5, "1c_snow_paper"), (9, "2_lamp_desk"), (11, "2b_rubbish"), (15, "2c_evening_windows"),
 (17, "3_frost"), (18, "3b_old_coat"), (23, "3d_tailor"), (29, "3e_snuffbox"), (49, "3f_sunday"), (52, "4_box"), (55, "4b_candle_work"), (58, "4c_cloth_shop"),
 (60, "5b_fitting"), (63, "5c_porter"), (65, "5_new_coat"), (66, "6b_shop_picture"), (68, "6_lit_window"), (69, "6c_hall"), (70, "6d_whist"),
 (73, "7_square"), (75, "7b_robbed"), (79, "7c_police"), (82, "8_study"), (86, "8b_anteroom"), (88, "8d_shouting"), (93, "8c_blizzard"),
 (94, "9_sickbed"), (96, "9b_empty_room"), (98, "9c_new_clerk"), (99, "10b_bridge"), (106, "10c_sleigh"), (107, "10_ghost_lamp"), (111, "10e_obukhov")]
SPLIT = {"I": (0, 8), "II": (9, 16), "III": (17, 51), "IV": (52, 59), "V": (60, 65), "VI": (66, 72), "VII": (73, 81), "VIII": (82, 93), "IX": (94, 98), "X": (99, 111)}
rows = json.load(open("The_Overcoat_voice_script.json", encoding="utf-8"))
first = {}
for r in rows: first.setdefault((r["part"], r["paragraph"]), r["id"])
def row_of(i):
    p = next(p for p, (a, b) in SPLIT.items() if a <= i <= b)
    return first[(p, i - SPLIT[p][0] + 1)]
scenes = [{"id": row_of(i), "art": a} for i, a in SCENES]
assert all(a in alt for _, a in SCENES)
B = {
 "slug": "the-overcoat", "prefix": "The_Overcoat", "lang": "en", "title": "The Overcoat", "author": "Nikolai Gogol", "author_ru": "Николай Гоголь", "year": 1842,
 "title_original": "Шинель", "publication_note": "first published in «Сочинения Николая Гоголя», vol. 3, St Petersburg, 1842",
 "source_note": "Text from ru.wikisource.org, after N. V. Gogol, Complete Works (1937–1952), vol. 3.", "translated_from": "the Russian original",
 "parts": parts, "names": names, "art": art, "scenes": scenes, "art_alt": alt,
 "focus": {k: [list(p) for p in v] for k, v in focus.items()}, "fx": fx,
 "episodes": [
  {"title": "The Clerk and His Overcoat", "from_part": "I", "to_part": "V", "thumb_art": "5_new_coat",
   "blurb": "Akaky Akakievich Bashmachkin, the humblest copying clerk in St Petersburg, is mocked by his colleagues and loves only his work, until the frost and a tailor named Petrovich teach him he needs a new overcoat."},
  {"title": "The Party, the Theft and the Ghost", "from_part": "VI", "to_part": "X", "thumb_art": "10_ghost_lamp",
   "blurb": "The new overcoat brings one happy evening and a night on an empty square. Then come a policeman, an Important Person who shouts, a fever, and a ghost who walks the streets of St Petersburg."}],
 "glossary": [
  ["titular councillor", "a low civil-service rank (ninth of fourteen); a “perpetual” one never rose any higher."],
  ["kopeck", "a hundredth of a rouble; a ten-kopeck piece was a small tip."],
  ["marten", "a costly fur used for coat collars; cat fur was the cheap imitation."],
  ["whist", "a card game for four, a favourite pastime of clerks."],
  ["watchman", "a street policeman who stood in a sentry box with a halberd."],
  ["district superintendent", "the police chief of a city district."],
  ["Falconet monument", "the Bronze Horseman, the statue of Peter the Great in St Petersburg."],
  ["Your Excellency", "the form of address for a general or an official of high rank."]],
 "thumb_art": "10_ghost_lamp", "thumb_position": "50% 50%", "thumb_sub": "A NOVELLA<br>FULL-CAST AUDIOBOOK", "cover_bg": ["#0e1226", "#e0e6f4"],
 "summary": "Akaky Akakievich is a poor copying clerk in St Petersburg whom everyone mocks and whose only joy is his work. When his old overcoat falls apart, he saves for months to buy a new one, and for one evening he is happy. One of the most influential stories in Russian literature.",
 "site_description": "Akaky Akakievich Bashmachkin is a humble copying clerk in St Petersburg, mocked by colleagues and content with his papers, until his old overcoat can no longer be mended. He starves himself to save for a new one, and for a single evening he is happy; then comes a night on an empty square, an Important Person who will not listen, and a ghost. Gogol's 1842 masterpiece of pity, comedy and the supernatural, the story from which, as Russians say, all of their literature came.",
 "tags": ["Gogol", "Nikolai Gogol", "The Overcoat", "audiobook", "full cast audiobook", "novella", "ghost story", "classic literature", "Russian literature", "St Petersburg", "public domain", "English audiobook"],
 "hashtags": "#Gogol #audiobook #classicliterature #russianliterature #publicdomain", "playlist": "PLVuswr3XMg9E",
 "text_note": "Translated from the Russian by an AI, a draft that needs a human editor.",
 "ru": {"title": "Шинель", "author": "Николай Гоголь",
        "names": {"I": "Один чиновник", "II": "Переписчик", "III": "Мороз и портной", "IV": "Копилка", "V": "Новая шинель", "VI": "Вечер", "VII": "Пустая площадь", "VIII": "Значительное лицо", "IX": "Горячка", "X": "Привидение"},
        "note": "Повесть в издании для чтения с оригинальными иллюстрациями.",
        "source_note": "Текст с ru.wikisource.org, по изданию: Н. В. Гоголь, Полное собрание сочинений (1937–1952), т. 3.",
        "contents": "Содержание", "back": "О тексте",
        "small": "Текст повести находится в общественном достоянии. Крупные абзацы автора разбиты на более короткие. Названия частей и иллюстрации сделаны для этого издания. Набрано шрифтом Lora (SIL Open Font License).",
        "description": "Акакий Акакиевич Башмачкин, бедный петербургский переписчик, которого все обижают и которому дорога только его работа, копит на новую шинель и один вечер бывает счастлив. Потом пустая площадь, значительное лицо, не пожелавшее выслушать, и привидение. Повесть Гоголя 1842 года."}}
for k in ("3c_stairs", "10d_watchman"):
    alt.pop(k, None); focus.pop(k, None); fx.pop(k, None)
assert set(art.values()) <= set(alt) and all(a in alt for v in pool.values() for a in v)
est = lambda ps: sum(words[p] for p in ps) / 150
print("EP1 %.1f min, EP2 %.1f min" % (est(parts[:5]), est(parts[5:])), "total %.1f" % est(parts))
json.dump(B, open("book.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
