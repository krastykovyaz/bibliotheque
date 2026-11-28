#!/usr/bin/env python3
"""Writes book.json for Olesya (run once after build_inputs.py; edit book.json afterwards if needed)."""
import json, re
parts = "I II III IV V VI VII VIII IX X XI XII XIII XIV".split()
NAMES = {"I": "The Forester's Lessons", "II": "The Witch of the Marsh", "III": "The Cabin on Hen's Legs", "IV": "The Cards", "V": "The Charm",
         "VI": "Evenings in the Forest", "VII": "Notice to Quit", "VIII": "The Constable and the Gun", "IX": "The Fever", "X": "The Moonlit Clearing",
         "XI": "A Proposal", "XII": "Trinity Day", "XIII": "The Hare and the Wolf", "XIV": "The Hail"}
RU = {"I": "Уроки лесника", "II": "Ведьма из болота", "III": "Избушка на курьих ножках", "IV": "Карты", "V": "Колдовство", "VI": "Вечера в лесу", "VII": "Приказ выселяться",
      "VIII": "Урядник и ружьё", "IX": "Лихорадка", "X": "Лунная просека", "XI": "Предложение", "XII": "Троицын день", "XIII": "Заяц и волк", "XIV": "Град"}
art = {"I": "1d_lesson", "II": "2_empty_house", "III": "3e_hut_ext", "IV": "4d_cards_olesya", "V": "5b_forest_road", "VI": "6_evening_path", "VII": "7_dejected",
       "VIII": "8b_cart", "IX": "9c_fever_bed", "X": "10d_moonlit", "XI": "11b_hawthorn", "XII": "12e_church_crowd", "XIII": "13e_hare_wolf", "XIV": "14d_beads"}
# (part, paragraph number as printed by show.py, picture): a scene starts there
SC = [("I", 1, "1_stove"), ("I", 5, "1b_village"), ("I", 9, "1c_patient"), ("I", 17, "1d_lesson"), ("I", 31, "1e_pen"),
      ("II", 1, "2_empty_house"), ("II", 6, "2b_stove_talk"), ("II", 17, "2c_witch_driven"),
      ("III", 1, "3_morning_guns"), ("III", 6, "3b_snow_forest"), ("III", 17, "3d_lost_marsh"), ("III", 21, "3e_hut_ext"), ("III", 24, "3f_hut_int"),
      ("III", 41, "3g_cards"), ("III", 58, "3h_olesya_enters"), ("III", 63, "3i_path_fence"), ("III", 87, "3k_olesya_close"), ("III", 100, "3j_red_skirt"),
      ("IV", 1, "4_spring_village"), ("IV", 5, "4c_spinning"), ("IV", 28, "4h_exile"), ("IV", 41, "4d_cards_olesya"), ("IV", 61, "4e_mill"), ("IV", 66, "4g_horror"),
      ("V", 1, "5_supper"), ("V", 5, "5b_forest_road"), ("V", 28, "5c_knife"), ("V", 36, "5d_fall"), ("V", 50, "5e_medusa"),
      ("VI", 1, "6_evening_path"), ("VI", 8, "6b_tall_house"), ("VI", 29, "6c_church_far"), ("VI", 42, "6d_yarmola_gloom"),
      ("VII", 1, "7_dejected"), ("VII", 13, "7b_notice"),
      ("VIII", 1, "8_rain_garden"), ("VIII", 6, "8b_cart"), ("VIII", 23, "8c_vodka_table"), ("VIII", 38, "8d_book"), ("VIII", 52, "8e_gun_gift"),
      ("IX", 1, "9_silent"), ("IX", 8, "9c_fever_bed"), ("IX", 9, "9d_fever_dreams"),
      ("X", 1, "10_threshold"), ("X", 12, "10b_leaving"), ("X", 33, "10c_clearing"), ("X", 46, "10d_moonlit"), ("X", 54, "10e_moon_face"),
      ("XI", 1, "11_june"), ("XI", 7, "11b_hawthorn"), ("XI", 24, "11d_pale_tree"), ("XI", 43, "6c_church_far"), ("XI", 49, "11e_scuffle"), ("XI", 50, "11f_young_moon"),
      ("XII", 1, "12_ride"), ("XII", 5, "12b_square"), ("XII", 6, "12c_lyre"), ("XII", 28, "12d_clerk"), ("XII", 39, "12e_church_crowd"), ("XII", 42, "12f_running"),
      ("XIII", 1, "13_gallop"), ("XIII", 5, "13b_bed"), ("XIII", 23, "13d_arm"), ("XIII", 44, "13b_bed"), ("XIII", 63, "13e_hare_wolf"), ("XIII", 66, "13f_farewell"), ("XIII", 80, "13g_black_cloud"),
      ("XIV", 1, "14_hail"), ("XIV", 5, "14b_yarmola_bed"), ("XIV", 14, "14c_empty_hut"), ("XIV", 17, "14d_beads")]
alt = {
 "1_stove": "A dark manor room in a blizzard: a forester squatting at an open stove with a bundle of firewood, a young gentleman standing by",
 "1b_village": "A snowy Polesye village of low thatched huts, three peasants in sheepskins standing in the road with their caps off",
 "1c_patient": "A table with bottles of medicine and two eggs, an old peasant woman standing by while the young gentleman looks on",
 "1d_lesson": "A forester with a black beard bent over a table by a candle, slowly drawing letters with a pen",
 "2_empty_house": "A big old manor house in a snowstorm, one lit window among dark ones, pines bent by the wind",
 "2b_stove_talk": "A room by lamplight with a green shade, a bearded forester at the glowing stove and the master pacing",
 "2c_witch_driven": "An old woman and a little girl driven out into the snowy forest by village lads with sticks, a broken hut behind them",
 "3_morning_guns": "A thaw-morning room: a single-barrelled gun on the table and a forester cleaning it by the bright window",
 "3b_snow_forest": "A pink winter morning in a pine forest, a hunter with a gun and a hare bounding across the snow",
 "3d_lost_marsh": "A hunter wading through a snowy marsh among hummocks, a small hut far away between the trees",
 "3e_hut_ext": "A hut on piles in a marsh, one side sunk so it looks lame, rags stuffed in its windows, snow on the thatch",
 "3f_hut_int": "Inside the hut: an old woman on the floor stripping feathers, a huge stove, two starlings on the ledge, a stranger at the door",
 "3g_cards": "An old woman laying worn cards in an eight-pointed star on a table, a hunter watching",
 "3h_olesya_enters": "A tall girl in a red skirt flinging open the door, holding up her apron with three tiny finches",
 "3i_path_fence": "A girl in a red skirt showing a hunter the path through the pines, a wattle fence beside them",
 "3j_red_skirt": "A hunter on a hillock looking back: far off, the hut with a red spot on its porch against the snow",
 "4_spring_village": "Early spring: brown streams in the village street, sparrows on the willows, white clouds in a blue sky",
 "4c_spinning": "Olesya spinning flax on a high bench, her granny at the stove, the guest on a low stool",
 "4d_cards_olesya": "Olesya with a red bead necklace sitting at the table with the cards, telling the guest his fortune",
 "4e_mill": "A water mill by a dark pond under the moon, one lit window and the wheel turning",
 "4h_exile": "A line of convicts in grey coats walking in chains along a snowy road, guarded by soldiers",
 "1e_pen": "A big rough hand drawing a wobbly letter with a pen on paper under a candle",
 "3k_olesya_close": "Olesya close up in the snow, proud and laughing, a red bead necklace at her throat",
 "8d_book": "The constable pushing out a thick finger as he counts the points of a police book on the table",
 "4g_horror": "Olesya's face with wide, fixed eyes, as if she saw something that is not there; red beads at her throat",
 "5_supper": "Supper in the hut: a steaming pot on an embroidered cloth, granny eating greedily, Olesya serving",
 "5b_forest_road": "A forest road at sunset with puddles and the first bluebells, a man and a girl in a red skirt walking",
 "5c_knife": "A small knife and a thin red cut on a forearm, three drops of blood falling",
 "5d_fall": "A man lying flat on the forest road, a girl laughing and clapping her hands behind him",
 "5e_medusa": "Olesya's stare, huge and dark blue, like a Medusa's head, a man recoiling at the edge",
 "6_evening_path": "Two figures walking slowly along the forest edge in the evening light, birches and pines",
 "6b_tall_house": "A seven-storey city house beside a tall pine of the same height, Olesya and the guest looking up",
 "6c_church_far": "A small village church with a green dome across the fields, Olesya and the guest standing apart",
 "6d_yarmola_gloom": "A forester at the gate of the manor turning away with a dark look, his dog at his feet, the master watching",
 "7_dejected": "The hut in gloom: granny rocking with her head in her hands, Olesya silent, the guest standing",
 "7b_notice": "A huge constable in a grey greatcoat in the hut doorway holding up a paper, the old woman cowering",
 "8_rain_garden": "A window onto a rainy garden of lilacs, a plan of a forest tract drawn on the table",
 "8b_cart": "A long chocolate-coloured horse with a drooping lip drawing a wicker cart whose one shaft is a rope; the constable driving",
 "8c_vodka_table": "A table with old bottles, red radishes and fresh butter; the master and the constable in a large coat",
 "8e_gun_gift": "A fine old gun held out across the table to the constable, who smiles",
 "9_silent": "The hut in an awkward silence: Olesya with her hands dropped, looking at the floor, the guest on his stool",
 "9c_fever_bed": "A sick man in bed at night, a lamp with a green shade, and a bright circle on the ceiling",
 "9d_fever_dreams": "A fever dream: many coloured boxes and a garland of grimacing and smiling faces",
 "10_threshold": "Olesya turning with a pale, radiant face as the guest stands in the doorway, granny shuffling aside",
 "10b_leaving": "Dusk by the hut: Olesya with a grey shawl walking out with the guest, granny watching",
 "10c_clearing": "A long straight forest clearing under a crimson sunset, two small figures at its foot",
 "10d_moonlit": "A moonlit pine and birch forest, a silver path of light and two figures walking arm in arm",
 "10e_moon_face": "Two faces close together in the moonlight, her red beads at her throat",
 "11_june": "A June meadow with lilies of the valley and tall pines, a man and a girl in a red skirt",
 "11b_hawthorn": "A forest path between bushes of flowering hawthorn, a man waiting at its turning",
 "11d_pale_tree": "Olesya, pale, leaning against a tree trunk while the man holds her hands",
 "11e_scuffle": "Two figures laughing and tumbling in the grass among hawthorn petals, a red kerchief flung in the air",
 "11f_young_moon": "A thin young moon over pines, Olesya with tears in her eyes holding the man's hands",
 "12_ride": "A man on a grey mottled horse riding across a green meadow, a white church ahead",
 "12b_square": "A village square full of carts and drunken, crowding peasants in the heat, the tavern at the right",
 "12c_lyre": "A blind lyre-player on a stool in the shade of a fence, villagers sitting around him",
 "12d_clerk": "A young estate clerk in a loud checked jacket and red tie laughing, the master angry",
 "12e_church_crowd": "Olesya in her red skirt at the church fence, ringed by hostile village women",
 "12f_running": "Olesya running down the road in torn clothes, stones flying after her, the crowd far behind",
 "13_gallop": "A rider on a foaming grey horse under a black thunder cloud, the road through the pines",
 "13b_bed": "Olesya lying on the bed with her face to the wall, granny beside her, the man at the door",
 "13d_arm": "A girl's arm with two dark bruises held in a man's hands",
 "13e_hare_wolf": "A wolf and a small hare face to face in a forest clearing, the story Olesya tells",
 "13f_farewell": "Olesya sitting up in bed and holding the man by the shoulders, saying goodbye",
 "13g_black_cloud": "A black cloud over half the sky, the hut under it, granny pointing, the man listening",
 "14_hail": "A night of hail and lightning: a house with stripped branches of the mulberry tree, great hailstones falling",
 "14b_yarmola_bed": "Morning sun streaming through shutter cracks, the bearded forester standing over the master's bed",
 "14c_empty_hut": "The empty hut after a hasty departure: bed frame, rags and rubbish on the floor, the door wide open",
 "14d_beads": "A string of cheap red beads hung on a window frame, the forest beyond",
}
focus = {
 "1_stove": [(.21, .62), (.56, .62), (.2, .5)], "1b_village": [(.45, .88), (.2, .6), (.7, .6)], "1c_patient": [(.79, .78), (.26, .8), (.5, .56)],
 "1d_lesson": [(.55, .55), (.27, .82), (.56, .66)], "2_empty_house": [(.43, .67), (.5, .45), (.08, .6)], "2b_stove_talk": [(.64, .75), (.37, .85), (.19, .55)],
 "2c_witch_driven": [(.62, .8), (.3, .85), (.16, .78)], "3_morning_guns": [(.62, .82), (.45, .6), (.8, .2)], "3b_snow_forest": [(.74, .86), (.22, .85), (.5, .4)],
 "3d_lost_marsh": [(.33, .82), (.78, .6), (.55, .9)], "3e_hut_ext": [(.5, .5), (.5, .78), (.43, .45)], "3f_hut_int": [(.4, .82), (.22, .27), (.74, .9)],
 "3g_cards": [(.55, .58), (.33, .85), (.78, .85)], "3h_olesya_enters": [(.57, .6), (.57, .65), (.2, .88)], "3i_path_fence": [(.4, .7), (.66, .75), (.2, .8)],
 "3j_red_skirt": [(.49, .62), (.19, .88), (.8, .7)], "4_spring_village": [(.5, .6), (.5, .88), (.06, .5)], "4c_spinning": [(.53, .4), (.69, .86), (.39, .9)],
 "4d_cards_olesya": [(.48, .5), (.74, .86), (.45, .7)], "4e_mill": [(.4, .55), (.62, .63), (.78, .18)], "4h_exile": [(.4, .8), (.65, .75), (.2, .85)], "1e_pen": [(.5, .55), (.7, .5), (.3, .55)], "3k_olesya_close": [(.5, .45), (.5, .7), (.3, .6)], "8d_book": [(.45, .65), (.7, .85), (.2, .85)],
 "4g_horror": [(.5, .58), (.5, .85), (.3, .7)], "5_supper": [(.47, .55), (.35, .8), (.75, .85)], "5b_forest_road": [(.6, .78), (.48, .8), (.2, .88)],
 "5c_knife": [(.52, .6), (.55, .82), (.3, .45)], "5d_fall": [(.35, .78), (.6, .9), (.5, .6)], "5e_medusa": [(.5, .6), (.16, .9), (.7, .5)],
 "6_evening_path": [(.52, .85), (.13, .65), (.5, .4)], "6b_tall_house": [(.52, .5), (.19, .5), (.86, .9)], "6c_church_far": [(.63, .55), (.45, .9), (.11, .6)],
 "6d_yarmola_gloom": [(.69, .85), (.3, .85), (.8, .95)], "7_dejected": [(.53, .62), (.82, .85), (.16, .85)], "7b_notice": [(.54, .7), (.72, .5), (.19, .92)],
 "8_rain_garden": [(.4, .45), (.22, .88), (.7, .3)], "8b_cart": [(.33, .8), (.55, .85), (.85, .5)], "8c_vodka_table": [(.4, .58), (.19, .88), (.78, .9)],
 "8e_gun_gift": [(.5, .45), (.19, .9), (.79, .85)], "9_silent": [(.47, .5), (.71, .8), (.86, .9)], "9c_fever_bed": [(.5, .2), (.3, .6), (.8, .55)],
 "9d_fever_dreams": [(.2, .3), (.6, .5), (.9, .4)], "10_threshold": [(.44, .55), (.77, .75), (.19, .9)], "10b_leaving": [(.56, .8), (.3, .65), (.69, .85)],
 "10c_clearing": [(.5, .9), (.5, .5), (.8, .5)], "10d_moonlit": [(.52, .9), (.74, .15), (.3, .6)], "10e_moon_face": [(.5, .55), (.81, .2), (.6, .8)],
 "11_june": [(.47, .87), (.2, .85), (.82, .2)], "11b_hawthorn": [(.51, .9), (.14, .65), (.82, .65)], "11d_pale_tree": [(.44, .7), (.63, .85), (.53, .15)],
 "11e_scuffle": [(.5, .78), (.78, .4), (.2, .8)], "11f_young_moon": [(.44, .78), (.8, .2), (.62, .88)], "12_ride": [(.42, .85), (.74, .65), (.1, .55)],
 "12b_square": [(.4, .8), (.95, .5), (.7, .9)], "12c_lyre": [(.5, .75), (.28, .9), (.75, .9)], "12d_clerk": [(.7, .8), (.3, .85), (.8, .3)],
 "12e_church_crowd": [(.49, .85), (.5, .55), (.7, .88)], "12f_running": [(.35, .88), (.2, .8), (.75, .9)], "13_gallop": [(.49, .8), (.6, .2), (.8, .6)],
 "13b_bed": [(.6, .7), (.24, .92), (.93, .92)], "13d_arm": [(.3, .72), (.73, .58), (.54, .62)], "13e_hare_wolf": [(.36, .9), (.72, .92), (.55, .5)],
 "13f_farewell": [(.56, .6), (.79, .9), (.2, .6)], "13g_black_cloud": [(.5, .2), (.62, .78), (.3, .95)], "14_hail": [(.5, .55), (.82, .7), (.46, .25)],
 "14b_yarmola_bed": [(.7, .88), (.4, .3), (.3, .65)], "14c_empty_hut": [(.5, .5), (.82, .75), (.5, .9)], "14d_beads": [(.74, .4), (.8, .5), (.3, .7)]}
snow = "1b_village 2_empty_house 2c_witch_driven 3b_snow_forest 3d_lost_marsh 3e_hut_ext 3i_path_fence 3j_red_skirt 3k_olesya_close 4h_exile".split()
flick = "1_stove 1c_patient 1d_lesson 1e_pen 2b_stove_talk 3f_hut_int 3g_cards 3h_olesya_enters 4c_spinning 4d_cards_olesya 5_supper 7_dejected 7b_notice 8c_vodka_table 8d_book 8e_gun_gift 9_silent 9c_fever_bed 10_threshold 13b_bed 13f_farewell 14c_empty_hut".split()
fx = {**{k: "snow" for k in snow}, "8_rain_garden": "rain", "14_hail": "rain", "8b_cart": "rain", **{k: "flicker" for k in flick}}
# the scene starts as row ids of the voice script
rows = json.load(open("Olesya_voice_script.json", encoding="utf-8"))
first = {}
for r in rows: first.setdefault((r["part"], r["paragraph"]), r["id"])
MERGE = {"III": [(52, 55)], "IV": [(49, 50)], "VI": [(38, 39)], "XII": [(7, 10), (12, 15), (16, 20)], "XIII": [(2, 3)]}
def knum(part, orig):
    absorbed = {k for a, b in MERGE.get(part, []) for k in range(a + 1, b + 1)}
    assert orig not in absorbed, (part, orig)
    return orig - len([k for k in absorbed if k < orig])
scenes = [{"id": first[(p, knum(p, n))], "art": a} for p, n, a in SC]
assert all(a in alt and a in focus for _, _, a in SC) and set(art.values()) <= set(alt)
T = json.load(open("translation_en.json", encoding="utf-8"))
words = {p: sum(len(x.split()) for x in T[p]) for p in parts}
B = {
 "slug": "olesya", "prefix": "Olesya", "lang": "en", "title": "Olesya", "author": "Alexander Kuprin", "author_ru": "Александр Куприн", "year": 1898,
 "title_original": "Олеся", "publication_note": "first published in the newspaper «Киевлянин» (Kyiv), 1898, with the subtitle «From memories of Volhynia»; first separate edition 1905",
 "source_note": "Text from ru.wikisource.org, after A. I. Kuprin, Complete Works (St Petersburg: A. F. Marx, 1912), vol. 5.", "translated_from": "the Russian original",
 "parts": parts, "names": NAMES, "art": art, "scenes": scenes, "art_alt": alt, "focus": {k: [list(p) for p in v] for k, v in focus.items()}, "fx": fx,
 "episodes": [
  {"title": "The Witch of the Marsh", "from_part": "I", "to_part": "III", "thumb_art": "3h_olesya_enters",
   "blurb": "A bored young writer snowed in at a Polesye village, a forester who cannot learn to read, a rumour of a witch in the marsh, and a girl with three finches in her apron."},
  {"title": "The Cards and the Charm", "from_part": "IV", "to_part": "VII", "thumb_art": "5b_forest_road",
   "blurb": "Spring comes. Olesya will not read the cards twice, shows him a charm on a forest road, and then the constable orders the two women out of the forest."},
  {"title": "Moonlight in the Pine Forest", "from_part": "VIII", "to_part": "XI", "thumb_art": "10d_moonlit",
   "blurb": "A gun for the constable, a fever, a night in the moonlit pines, and a June evening when Ivan Timofeyevich asks Olesya to be his wife."},
  {"title": "Trinity Day", "from_part": "XII", "to_part": "XIV", "thumb_art": "12e_church_crowd",
   "blurb": "Olesya goes to church for him. What the village does to her, the tale of the hare and the wolf, a storm of hail, and a string of red beads."}],
 "glossary": [
  ["Polesye", "a vast region of forest and marsh in the north of Ukraine and the south of Belarus; in Kuprin's time part of the Russian Empire."],
  ["Volhynia", "a province of the Russian Empire (now north-western Ukraine) in which the story is set."],
  ["verst", "a Russian measure of distance, a little over a kilometre (about two thirds of a mile)."],
  ["arshin", "an old Russian measure of length, about 71 centimetres."],
  ["constable (uryadnik)", "the lowest rank of rural police officer in the Russian Empire, in charge of a district."],
  ["zlot, kopeck", "small coins: a zlot was fifteen kopecks, a kopeck a hundredth of a rouble."],
  ["krupnik", "a thick pottage of groats (here buckwheat) with bacon, onion and potatoes."],
  ["Trinity Day", "the feast of Pentecost, a great church holiday and a day of fairs and heavy drinking in the village."],
  ["lyre-player (lirnik)", "a blind wandering singer who accompanied old ballads (dumas) on a hurdy-gurdy-like lyre."],
  ["Pochaev", "a famous monastery in Volhynia, defended in the legend against the Turks."],
  ["tar", "in Ukraine, to smear a girl's gate with tar was to brand her as dishonoured."]],
 "thumb_art": "3h_olesya_enters", "thumb_position": "50% 50%", "thumb_sub": "A NOVELLA<br>FULL-CAST AUDIOBOOK", "cover_bg": ["#0a1224", "#2a3e44"],
 "summary": "A young writer posted to a Polesye village goes looking for a witch in the marsh and finds Olesya, a free, proud forest girl who reads the cards, loves the birds, and will not be told what to fear. Kuprin's most tender story of first love and the cruelty of a village.",
 "site_description": "Ivan Timofeyevich, a city writer stranded for the winter in a village in Polesye, hears of a witch who lives in the marsh and goes to see her. In the cabin on hen's legs he meets her granddaughter Olesya, who tells fortunes, charms blood and does not fear anything but her fate. A story of a spring and summer in the forest, of love, of what a village does to the one who is different, and of a string of red beads. Kuprin's novella of 1898, one of the best loved in Russian.",
 "tags": ["Kuprin", "Alexander Kuprin", "Olesya", "audiobook", "full cast audiobook", "novella", "love story", "classic literature", "Russian literature", "Polesye", "public domain", "English audiobook"],
 "hashtags": "#Kuprin #audiobook #classicliterature #russianliterature #publicdomain", "playlist": "PLVuswr3XMg9E",
 "text_note": "",
 "ru": {"title": "Олеся", "author": "Александр Куприн", "names": RU,
        "note": "Повесть в издании для чтения с оригинальными иллюстрациями.",
        "source_note": "Текст с ru.wikisource.org, по изданию: А. И. Куприн, Полное собрание сочинений (СПб.: Т-во А. Ф. Маркс, 1912), т. 5.",
        "contents": "Содержание", "back": "О тексте",
        "small": "Текст повести находится в общественном достоянии. Строки стихов и обрывки фраз, разорванные при публикации, соединены. Названия глав и иллюстрации сделаны для этого издания. Набрано шрифтом Lora (SIL Open Font License).",
        "description": "Иван Тимофеевич, городской литератор, проводит зиму в глухой деревне на Полесье и идёт посмотреть на ведьму, которая живёт в болоте. В избушке на курьих ножках он встречает Олесю, гадалку и лесную девушку, которая ничего не боится, кроме своей судьбы. Повесть Куприна 1898 года о весне, любви и жестокости деревни."}}
json.dump(B, open("book.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
tot = sum(words.values())
est = lambda ps: sum(words[p] for p in ps) / 150
for e in B["episodes"]:
    a, b = parts.index(e["from_part"]), parts.index(e["to_part"]); print(e["title"], "%.1f min" % est(parts[a:b + 1]))
print("total %.1f min, %d scenes, %d pictures" % (tot / 150, len(scenes), len(alt)))
