#!/usr/bin/env python3
"""Writes book.json for Ruslan and Ludmila (run after build_inputs.py; edit book.json afterwards if needed; keeps series_playlist if set)."""
import json, os
first = json.load(open("first_row_ids.json"))
parts = ["I", "II", "III", "IV", "V", "VI"]
names = {"I": "The Feast and the Stolen Bride", "II": "The Rivals and the Magic Garden", "III": "The Cap and the Giant Head", "IV": "The Castle of Maidens", "V": "The Beard and the Treachery", "VI": "The Living Water"}
art = {"I": "1_oak", "II": "2e_garden", "III": "3d_head_sleep", "IV": "4_castle", "V": "5_flight", "VI": "6e_ring"}
S = [("I", 0, "1_oak"), ("I", 6, "1b_feast"), ("I", 11, "1c_bedchamber"), ("I", 18, "1d_hall"), ("I", 24, "1e_crossroads"), ("I", 31, "1f_cave"), ("I", 41, "1g_naina_river"), ("I", 51, "1h_hag"), ("I", 64, "1f_cave"),
     ("II", 0, "2_ditch"), ("II", 9, "2b_old_woman"), ("II", 15, "2c_river"), ("II", 20, "2d_chamber"), ("II", 32, "2e_garden"), ("II", 41, "2f_dwarf_night"), ("II", 46, "2g_duel"),
     ("III", 0, "3_morning"), ("III", 12, "3b_cap"), ("III", 17, "3c_bones"), ("III", 25, "3d_head_sleep"), ("III", 30, "3e_head_fight"), ("III", 39, "3f_brothers"), ("III", 45, "3g_ground"),
     ("IV", 0, "4_castle"), ("IV", 12, "4b_bath"), ("IV", 16, "4c_moon_room"), ("IV", 20, "4d_mermaids"), ("IV", 23, "4e_invisible"), ("IV", 29, "4f_net"),
     ("V", 0, "5_flight"), ("V", 11, "5b_rampage"), ("V", 16, "5c_riding"), ("V", 25, "5d_head_dies"), ("V", 31, "5e_river_hut"), ("V", 36, "5f_two_knights"), ("V", 45, "5g_mound"), ("V", 49, "5h_dream"), ("V", 54, "5g_mound"),
     ("VI", 0, "6_dead_field"), ("VI", 8, "6b_palace"), ("VI", 17, "6c_living_water"), ("VI", 23, "6d_battle"), ("VI", 30, "6e_ring"), ("VI", 37, "6f_caucasus")]
scenes = [{"id": first[f"{p}:{i}"], "art": a} for p, i, a in S]
alt = {
 "1_oak": "A green oak on a curved sea shore under the moon with a golden chain round it, a learned black cat on the chain, a mermaid in the branches, a hut on hen's legs and thirty knights rising from the water",
 "1b_feast": "A wedding feast in Prince Vladimir's high hall: the old prince on his seat, the young couple beside him, guests along the table and three gloomy rivals at the end",
 "1c_bedchamber": "A dark bedchamber with a canopied bed and a bride, the bridegroom standing by, a candle, and a black whirling shape with a flash of lightning at the window",
 "1d_hall": "The old prince on his seat in the hall surrounded by knights and courtiers, asking who will ride after his stolen daughter",
 "1e_crossroads": "Four knights on horseback riding away on four different roads at a crossroads at dusk",
 "1f_cave": "A cave lit by a lamp where an old white-bearded sorcerer sits over an ancient book, and a knight in a red cloak stands before him",
 "1g_naina_river": "A young shepherd with a pipe on one bank and a girl weaving a wreath by a sunny river among meadows",
 "1h_hag": "A dark forest hut with a fire, a cauldron, an old hunchbacked witch with a shaking head and a young sorcerer shrinking from her",
 "2_ditch": "A boaster knight tumbled head over heels into a muddy spring ditch while his horse leaps clear and an angry rider with a sword raised stops at the edge",
 "2b_old_woman": "A little old woman with a staff pointing north to a knight standing by his horse on a muddy road",
 "2c_river": "Two knights on horseback facing each other on a steep river bank at dusk, a spear thrown between them",
 "2d_chamber": "A magic chamber with a golden bed where a captive princess sits, three maidens in fine dresses bringing her clothes, a window on a snowy plain",
 "2e_garden": "A magnificent magic garden with palms, pines, fountains and statues, and a small princess on a high bridge over a torrent",
 "2f_dwarf_night": "A row of dark guards with drawn sabres carrying a great beard on a cushion and a small dwarf in a tall cap, while a frightened princess sits up on her bed",
 "2g_duel": "A night duel by a river under a full moon: a knight on horseback lifts his enemy from the saddle to throw him into the waves",
 "3_morning": "A dwarf wizard in bed under his enormous white beard being combed by slaves, with a winged serpent flying in at the window",
 "3b_cap": "A girl in a blue sarafan trying on a wizard's cap before a tall mirror in which she has disappeared",
 "3c_bones": "An old battlefield with scattered bones, skulls, rusting spears and a shield, a lone knight on horseback riding through",
 "3d_head_sleep": "A gigantic sleeping head on a moonlit hill with a plumed helmet and owls flying up from its brows, a tiny knight on horseback at its side",
 "3e_head_fight": "The giant head blowing a gale with open mouth and wide eyes at a knight whose horse struggles, a spear flying at its tongue",
 "3f_brothers": "A giant striding over the mountains with a pine club and a small wizard sitting on his shoulder",
 "3g_ground": "A giant lying with his ear to the ground, a dwarf creeping up behind him with a sword raised and a second sword standing in the earth",
 "4_castle": "A castle with towers on a hill at sunset, a girl singing on the wall and a knight on horseback riding up",
 "4b_bath": "A steamy Russian bath with a young khan lying on a bench and girls in white with birch branches",
 "4c_moon_room": "A moonlit bedchamber with a young khan asleep and a girl in white at the door",
 "4d_mermaids": "A moonlit autumn forest with mermaids swaying on the branches and a knight riding quietly through the mist",
 "4e_invisible": "A sunny enchanted garden where golden fruit seems to float, a waterfall splashes by itself, and a dwarf watches from a tower window",
 "4f_net": "A marble arbour where a princess falls into a net, a pale false knight beside her and a dwarf with a long beard appearing",
 "5_flight": "A dwarf wizard flying high over the sea among clouds while a knight in a red cloak hangs on his long beard",
 "5b_rampage": "A knight with a great sword raging through a ruined garden, trees and arbours crashing down",
 "5c_riding": "A knight in a red cloak riding at sunrise with a sleeping princess laid across the saddle before him",
 "5d_head_dies": "The giant head dying on its hill, mouth open, and a knight on horseback arriving with the sleeping princess and a bag",
 "5e_river_hut": "A quiet river with a boat and a fisherman, a girl by a small hut, and a knight on the bank",
 "5f_two_knights": "Two friends talking on a river bank at night under a moon, a princess asleep under a cloak between them",
 "5g_mound": "A burial mound under a night sky with a sleeping knight and princess, a horse, a rider approaching with a sword and a cat at the edge",
 "5h_dream": "A silent hall where the old prince sits among motionless guests, a pale dead knight at the table and a traitor leading a girl by the hand",
 "6_dead_field": "A knight lying dead in an open field, his horse standing over him, a raven overhead and a bag with a dwarf peeping out",
 "6b_palace": "A princess asleep on a bier in a great hall, the old prince at her feet, a crowd of nobles and a window showing enemy tents",
 "6c_living_water": "A moonlit valley with two springs, an old sorcerer sprinkling water over a fallen knight",
 "6d_battle": "A battle before the walls of Kiev with a knight in a red cloak blowing a horn and riding into enemy horsemen",
 "6e_ring": "In the great hall a knight touches the sleeping princess's brow with a golden ring, the old prince weeping with joy beside them",
 "6f_caucasus": "A poet standing before the snowy peaks of the Caucasus at sunset with his lyre"}
focus = {
 "1_oak": [[.33, .58], [.12, .8], [.72, .68]], "1b_feast": [[.5, .5], [.7, .62], [.15, .72]], "1c_bedchamber": [[.46, .5], [.85, .3], [.53, .75]], "1d_hall": [[.5, .62], [.28, .88], [.75, .88]],
 "1e_crossroads": [[.3, .7], [.66, .65], [.85, .75]], "1f_cave": [[.45, .72], [.75, .8], [.5, .4]], "1g_naina_river": [[.64, .78], [.27, .78], [.2, .88]], "1h_hag": [[.56, .7], [.81, .72], [.16, .75]],
 "2_ditch": [[.47, .78], [.26, .62], [.65, .6]], "2b_old_woman": [[.56, .75], [.24, .8], [.9, .6]], "2c_river": [[.35, .58], [.74, .58], [.8, .25]], "2d_chamber": [[.19, .55], [.65, .85], [.62, .35]],
 "2e_garden": [[.5, .6], [.1, .55], [.88, .45]], "2f_dwarf_night": [[.81, .75], [.13, .5], [.5, .8]], "2g_duel": [[.35, .5], [.15, .18], [.8, .82]],
 "3_morning": [[.25, .55], [.72, .3], [.2, .88]], "3b_cap": [[.3, .7], [.64, .45], [.29, .5]], "3c_bones": [[.62, .62], [.2, .8], [.8, .8]], "3d_head_sleep": [[.46, .58], [.85, .9], [.65, .2]],
 "3e_head_fight": [[.26, .62], [.75, .85], [.55, .7]], "3f_brothers": [[.4, .5], [.64, .25], [.2, .9]], "3g_ground": [[.66, .75], [.25, .8], [.83, .7]],
 "4_castle": [[.6, .45], [.19, .78], [.56, .55]], "4b_bath": [[.37, .7], [.19, .8], [.6, .3]], "4c_moon_room": [[.42, .3], [.16, .85], [.67, .62]], "4d_mermaids": [[.35, .42], [.4, .88], [.82, .18]],
 "4e_invisible": [[.4, .7], [.62, .55], [.8, .3]], "4f_net": [[.43, .8], [.77, .7], [.19, .85]],
 "5_flight": [[.7, .3], [.24, .78], [.5, .95]], "5b_rampage": [[.5, .55], [.7, .45], [.15, .78]], "5c_riding": [[.52, .65], [.25, .55], [.9, .75]], "5d_head_dies": [[.35, .65], [.77, .78], [.35, .25]],
 "5e_river_hut": [[.45, .8], [.8, .72], [.16, .85]], "5f_two_knights": [[.5, .78], [.78, .2], [.85, .9]], "5g_mound": [[.5, .6], [.78, .88], [.92, .9]], "5h_dream": [[.5, .62], [.45, .92], [.62, .82]],
 "6_dead_field": [[.44, .88], [.69, .9], [.62, .55]], "6b_palace": [[.5, .65], [.79, .9], [.88, .35]], "6c_living_water": [[.62, .85], [.5, .9], [.2, .9]], "6d_battle": [[.51, .8], [.15, .5], [.8, .82]],
 "6e_ring": [[.52, .62], [.62, .8], [.83, .9]], "6f_caucasus": [[.27, .88], [.4, .3], [.75, .45]]}
fx = {"1c_bedchamber": "flicker", "1f_cave": "flicker", "1h_hag": "flicker", "2f_dwarf_night": "flicker", "4d_mermaids": "leaves", "6c_living_water": "flicker"}
glossary = [
 ["Prince Vladimir", "“Vladimir the Red Sun”, the Grand Prince of Kiev (reigned about 980–1015), the generous ruler of the Russian epic songs; here he is Ludmila's father."],
 ["Kiev and the Dnieper", "the old capital of Rus on the Dnieper river, in today's Ukraine."],
 ["Bayan", "a legendary bard of ancient Rus who sings to the gusli, a plucked harp-like instrument."],
 ["Lel", "the Slavic god of love, as Pushkin names him."],
 ["Chernomor", "the dwarf wizard of the northern mountains, whose power lies in his long beard."],
 ["Finn", "a sorcerer from the far north. Finland was thought of as the home of the best magicians."],
 ["Pechenegs", "a nomad people of the steppe who raided Kiev in the 10th and 11th centuries."],
 ["Khazars", "a Turkic people of the steppe north of the Caucasus; Ratmir is a khan of theirs."],
 ["Baba Yaga and Koshchei", "the witch in a flying mortar and the deathless miser king of Russian fairy tales."],
 ["mead", "a drink of fermented honey, served at feasts in the old halls."],
 ["sarafan", "a long sleeveless Russian dress worn over a blouse."],
 ["Moors", "the dark-skinned servants and guards of the palace, as the original calls them."],
 ["Orlovsky", "Alexander Orlovsky, a Russian painter famous for lively battle and horse scenes."],
 ["the northern Orpheus", "Vasily Zhukovsky, Pushkin's older fellow poet, whose ballad about twelve sleeping maidens Pushkin gently mocks."],
 ["Armida", "the enchantress whose magic gardens are famous in Tasso's epic."]]
book = {
 "slug": "ruslan-and-ludmila", "prefix": "Ruslan_and_Ludmila", "lang": "en", "title": "Ruslan and Ludmila", "author": "Alexander Pushkin", "author_ru": "Александр Пушкин", "year": 1820,
 "title_original": "Руслан и Людмила", "publication_note": "first published in St Petersburg, 1820; final text with the prologue and epilogue, 1828",
 "source_note": "Text from ru.wikisource.org, after A. S. Pushkin, Complete Works in 10 volumes, vol. 4 (Leningrad: Nauka, 1977), the final text with the prologue and epilogue.",
 "translated_from": "the Russian original", "parts": parts, "names": names, "art": art, "scenes": scenes, "art_alt": alt, "focus": focus, "fx": fx,
 "episodes": [
  {"title": "The Stolen Bride", "from_part": "I", "to_part": "III", "thumb_art": "3d_head_sleep",
   "blurb": "On the night of his wedding in Kiev, Prince Ruslan sees his bride Ludmila vanish in thunder and smoke. Cantos I to III: the three rival suitors, the sorcerer Finn and his sad love story, the magic garden of the wizard Chernomor, the cap that makes a girl invisible, and a gigantic talking head guarding a sword."},
  {"title": "The Beard and the Living Water", "from_part": "IV", "to_part": "VI", "thumb_art": "5_flight",
   "blurb": "Cantos IV to VI: the castle of the twelve maidens, Ludmila hiding invisible in the wizard's garden, the flight over the sea clinging to a magic beard, a faithless friend, and the living and dead water that bring a dead hero back to save Kiev."}],
 "glossary": glossary, "thumb_art": "1_oak", "thumb_position": "50% 50%", "thumb_sub": "A POEM<br>FULL-CAST AUDIOBOOK", "cover_bg": ["#0d1830", "#e0e6f4"],
 "summary": "On his wedding night the young prince Ruslan loses his bride Ludmila to an evil wizard and rides out to find her, through enchanted forests, a talking giant head, rival knights and a magic beard. Pushkin's first great poem, a fairy tale told with wit.",
 "site_description": "At the wedding feast of the Kiev prince's daughter Ludmila a clap of thunder puts out the lights, and the bride is gone, carried off by the dwarf wizard Chernomor. Three rivals and the bridegroom Ruslan ride out to find her. Pushkin's first great poem (1820), full of fairy-tale wonders, jokes and tender asides, here read as a full-cast English audiobook in a prose rendering of the Russian verse.",
 "tags": ["Pushkin", "Alexander Pushkin", "Ruslan and Ludmila", "audiobook", "full cast audiobook", "poem", "fairy tale", "Russian fairy tale", "classic literature", "Russian literature", "public domain", "English audiobook"],
 "hashtags": "#Pushkin #audiobook #classicliterature #russianliterature #publicdomain",
 "playlist": "PLVuswr3XMg9E", "text_note": "Prose rendering of the Russian verse by an AI, a draft that needs a human editor.",
 "ru": {"title": "Руслан и Людмила", "author": "Александр Пушкин", "names": {"I": "Пир и похищение", "II": "Соперники и волшебный сад", "III": "Шапка и Голова", "IV": "Замок дев", "V": "Борода и измена", "VI": "Живая вода"},
        "note": "Поэма в издании для чтения с оригинальными иллюстрациями.", "source_note": "Текст с ru.wikisource.org, по изданию: А. С. Пушкин, Полное собрание сочинений в 10 томах, т. 4 (Л.: Наука, 1977), окончательный текст с прологом и эпилогом.",
        "contents": "Содержание", "back": "О тексте", "small": "Текст поэмы находится в общественном достоянии. Строфы разбиты на более короткие группы строк для удобства чтения. Названия песен и иллюстрации сделаны для этого издания. Набрано шрифтом Lora (SIL Open Font License).",
        "description": "На свадебном пиру в Киеве гремит гром, гаснет свет, и Людмила исчезает: её похитил злой карлик Черномор. Руслан и три его соперника скачут на поиски. Первая поэма Пушкина (1820), сказка с шуткой и лирическими отступлениями."}}
old = json.load(open("book.json")) if os.path.exists("book.json") else {}
if old.get("series_playlist"): book["series_playlist"] = old["series_playlist"]
json.dump(book, open("book.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("scenes:", len(scenes))
