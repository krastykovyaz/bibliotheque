#!/usr/bin/env python3
"""Writes book.json for "The Little Humpbacked Horse" (Yershov). Run build_inputs.py and make_art_konek.py first."""
import json, re
sc = json.load(open("scenes.json")); T = json.load(open("translation_en.json"))
from make_art_konek import ARTNAMES
CAP = """01|The old man and his three sons: Danilo, Gavrilo, and Ivan the fool.|Старик и три его сына: Данило, Гаврило и Иван-дурак.
02|Someone is trampling the wheat. Danilo goes to watch, and hides in a haystack from the rain.|Кто-то топчет пшеницу. Данило идёт сторожить и прячется от дождя под сено.
03|Gavrilo is frightened by the frost and runs about all night by the neighbour's fence.|Гаврило пугается мороза и всю ночь бегает у соседского забора.
04|Ivan sings on the stove and will not go to watch the field, until his father promises him peas and beans.|Иван поёт на печи и не хочет идти в дозор, пока отец не обещает ему гороху и бобов.
05|At midnight Ivan jumps on a white mare, with his face to her tail, and she takes him flying over the fields.|В полночь Иван вскакивает на белую кобылицу, да задом наперёд, и она мчит его по полям.
06|The tired mare promises Ivan two golden-maned horses and a little humpbacked horse.|Усталая кобылица обещает Ивану двух коней золотогривых и конька-горбунка.
07|Ivan tells his brothers about the devil he caught, and they laugh until they cry.|Иван рассказывает братьям про пойманного чёрта, и те смеются до слёз.
08|Danilo and Gavrilo find two golden-maned horses and a tiny humpbacked horse in the shed.|Данило и Гаврило находят в балагане двух золотогривых коней и конька-горбунка.
09|The shed is empty, and the little horse dances round the weeping Ivan.|Балаган пуст, а горбунок пляшет вокруг плачущего Ивана.
10|The Little Humpbacked Horse flies like an arrow and catches the thieves.|Горбунок стрелой летит и настигает воров.
11|The brothers are ashamed, and Ivan goes with them to sell the horses.|Братьям стыдно, и Иван едет с ними продавать коней.
12|At night the brothers see a faraway light in the dark.|Ночью братья замечают вдали огонёк.
13|Ivan rides to the strange light that gives no warmth.|Иван скачет к чудному огоньку, который не греет.
14|It is a feather of the Firebird. The little horse warns Ivan, but he takes it anyway.|Это перо Жар-птицы. Конёк предупреждает Ивана, но тот берёт перо.
15|In the capital, the brothers set out the two horses in the market.|В столице братья ставят двух коней в конный ряд.
16|The whole town crowds round the horses with golden manes.|Весь город толпится вокруг коней с золотыми гривами.
17|The city warden tells the Tsar about the wonderful horses.|Городничий рассказывает царю о чудесных конях.
18|The Tsar buys the horses, and Ivan takes the Tsar's silver.|Царь покупает коней, а Иван получает царское серебро.
19|Ivan becomes the Tsar's chief groom and walks through the town, and the horses dance.|Иван становится царским конюшим и идёт по городу, а кони пляшут.
20|The brothers go home with their money, and soon they marry.|Братья возвращаются домой с деньгами и женятся.
21|The beginning of the tale: goats on the sea, a horse that flies to the sun, a maiden on a faraway island.|Присказка: козы на море, конь, летящий к солнцу, девица на дальнем острове.
22|The Chamberlain, who envies Ivan, hides in the stable under a heap of oats.|Спальник, завидуя Ивану, прячется в конюшне под овсом.
23|At midnight Ivan braids the horses' manes, and the Firebird's feather glows in the corner.|В полночь Иван заплетает коням гривы, а в углу сияет перо Жар-птицы.
24|While Ivan sleeps, the Chamberlain steals the feather.|Пока Иван спит, спальник крадёт перо.
25|The Tsar's messengers tumble over one another, and the Tsar laughs.|Царские посыльные кувырком падают, а царь хохочет.
26|The messengers try to wake Ivan, who sleeps like a hero.|Дворяне будят Ивана, а он спит богатырским сном.
27|Ivan trembles before the Tsar, who has found the feather.|Иван дрожит перед царём, нашедшим перо.
28|Ivan cries in the hayloft, and the little horse comforts him.|Иван плачет на сеновале, а конёк его утешает.
29|They ride east, to a mountain of pure silver.|Они едут на восток, к горе из чистого серебра.
30|Ivan hides under a trough of millet and wine while the Firebirds fly in.|Иван прячется под корытом с пшеном и вином, а жар-птицы слетаются.
31|The Firebird comes out of the sack, and the whole hall is flooded with light.|Жар-птица выходит из мешка, и весь покой заливает свет.
32|In the kitchen the servants read a book of tales, and the Chamberlain listens at the window.|На кухне слуги читают книжку сказок, а спальник слушает у окна.
33|A servant tells of the lovely Tsar-Maiden, who sails the ocean in a golden boat.|Слуга рассказывает о прекрасной Царь-девице, что плавает по окияну в золотой шлюпке.
34|The Tsar wants the Tsar-Maiden, and Ivan, in his nightshirt, has to promise to bring her.|Царь хочет Царь-девицу, и Иван в одной рубашке должен обещать её привезти.
35|Ivan and the little horse ride to the shore of the ocean.|Иван и конёк едут к берегу окияна.
36|The Tsar-Maiden sails to the gold tent, and plays her harp.|Царь-девица подплывает к златошвейному шатру и играет на гуслях.
37|Ivan falls asleep, and the little horse scolds him.|Иван засыпает, а конёк его бранит.
38|The next day Ivan catches the Tsar-Maiden by her long braid.|На другой день Иван хватает Царь-девицу за длинную косу.
39|The Tsar kneels before the Tsar-Maiden, but she turns away.|Царь стоит на коленях перед Царь-девицей, а она отворачивается.
40|The Tsar sends Ivan to the ocean for the Tsar-Maiden's ring.|Царь посылает Ивана за перстнем Царь-девицы на окиян.
41|The little horse flies like the wind towards the ocean.|Горбунок летит как ветер к окияну.
42|A great whale lies across the ocean, with a whole village on his back.|Поперёк окияна лежит чудо-юдо рыба-кит, а на спине у него село.
43|Ivan and the little horse ride up into the sky.|Иван и конёк въезжают на небо.
44|The crystal gates of the heavenly palace, with their golden snakes and three stars.|Хрустальные ворота небесного терема, обвитые золотыми змейками, с тремя звёздами.
45|Ivan talks with Moon Moonovich, the mother of the Tsar-Maiden.|Иван беседует с Месяцем Месяцовичем, матерью Царь-девицы.
46|The Moon tells Ivan how the whale can be forgiven, and says goodbye.|Месяц рассказывает Ивану, как простить кита, и прощается.
47|The little horse warns the villagers, and they run away with their carts.|Конёк предупреждает мужиков, и те уезжают на телегах.
48|The whale lets go of the thirty ships he swallowed.|Кит выпускает тридцать кораблей, которые проглотил.
49|The ships sail out, with white sails, flags, and songs.|Корабли выплывают с белыми парусами, флагами и песнями.
50|The whale king calls the sturgeons and orders them to find the ring.|Кит-царь зовёт осетров и велит найти перстень.
51|The dolphins find the quarrelsome ruff, who is fighting with a carp in a pond.|Дельфины находят ерша-забияку, который дерётся с карасём в пруду.
52|The sturgeons lift the heavy little chest from the sea-bed.|Осетры поднимают со дна тяжёлый сундучок.
53|At sunset the whale brings the little chest ashore.|На закате кит выносит сундучок на берег.
54|The Tsar-Maiden says she cannot marry a grey old man.|Царь-девица говорит, что не пойдёт за седого старика.
55|At night in the hayloft the little horse tells Ivan what to do about the cauldrons.|Ночью на сеновале конёк рассказывает Ивану, что делать с котлами.
56|Three cauldrons in the courtyard: cold water, boiled water, and milk.|Во дворе три котла: с холодной водой, с варёной и с молоком.
57|Ivan dives into the cauldrons and comes out a handsome prince.|Иван ныряет в котлы и выходит красавцем.
58|The Tsar-Maiden speaks to the people and names Ivan as their Tsar.|Царь-девица говорит народу и называет царём Ивана.
59|The wedding feast: Tsar Ivan and the Tsar-Maiden, and the whole people merry.|Свадебный пир: царь Иван и Царь-девица, и весь народ рад.""".split("\n")
CAPS = {ARTNAMES[int(l.split("|")[0]) - 1]: l.split("|")[1:] for l in CAP}
assert len(CAPS) == 59
A = {k: CAPS[k][0] for k in CAPS}
FOCI = [[[.5, .6], [.22, .72], [.8, .7]], [[.4, .7], [.72, .65], [.5, .3]], [[.62, .8], [.2, .75], [.5, .45]], [[.5, .55], [.15, .85], [.85, .75]], [[.3, .65], [.7, .6], [.5, .85]]]
F = {k: FOCI[i % 5] for i, k in enumerate(ARTNAMES)}
INDOOR = ("04", "07", "17", "22", "23", "24", "25", "26", "27", "28", "31", "32", "33", "34", "39", "40", "54", "55", "59")
FX = {k: "flicker" for k in ARTNAMES if k[:2] in INDOOR}; FX["02_danilo_hides"] = "rain"
OPEN = {"I": "01_old_man_sons", "II": "31_firebird_hall", "III": "42_whale_island"}
# PDF figures: a picture on every part opening (art) and one about every 340 words besides
FIG, used = [], set(OPEN.values())
art_of_par = {}
for part in T:
    for i in range(len(T[part])): pass
rows = json.load(open("The_Little_Humpbacked_Horse_voice_script.json", encoding="utf-8"))
par_art = {}; cur = None
sc_ids = [(s["id"], s["art"]) for s in sc]
for r in rows:
    for sid, a in sc_ids:
        if sid <= r["id"]: cur = a
    par_art.setdefault((r["part"], r["paragraph"]), cur)
for part in T:
    acc = 0
    for n, p in enumerate(T[part], 1):
        acc += len(p.split())
        a = par_art.get((part, n))
        if n == len(T[part]) or a is None: continue
        if acc >= 250 and a not in used:
            FIG.append({"part": part, "after": n, "art": a, "caption": CAPS[a][0], "caption_ru": CAPS[a][1]}); used.add(a); acc = 0
b = {
 "slug": "little-humpbacked-horse", "prefix": "The_Little_Humpbacked_Horse", "lang": "en", "title": "The Little Humpbacked Horse",
 "author": "Pyotr Yershov", "author_ru": "Пётр Ершов", "year": 1834,
 "title_original": "Конёк-горбунок",
 "publication_note": "a Russian fairy tale in verse in three parts, first published in 1834 (part one) and in full in 1834-1856",
 "source_note": "Text from ru.wikisource.org, the seventh edition of 1868 (St Petersburg), the last in the author's lifetime.",
 "translated_from": "the Russian original",
 "parts": ["I", "II", "III"],
 "names": {"I": "Ivan and the Golden Horses", "II": "The Firebird and the Tsar-Maiden", "III": "The Whale, the Moon and the Cauldrons"},
 "art": OPEN, "art_alt": A, "focus": F, "fx": FX, "scenes": sc,
 "episodes": [
  {"title": "Golden Horses and Firebird", "from_part": "I", "to_part": "II", "to_paragraph": 11, "thumb_art": "30_trough_trap",
   "chapters": [["I", 1, "Three brothers and the wheat thief", "Три брата и ночной вор"], ["I", 5, "The white mare", "Белая кобылица"], ["I", 8, "The golden horses and the Little Humpbacked Horse", "Золотогривые кони и Конёк-горбунок"], ["I", 14, "The Firebird's feather", "Перо Жар-птицы"], ["I", 15, "The Tsar buys the horses", "Царь покупает коней"], ["II", 1, "The tale begins again", "Сказка начинается снова"], ["II", 2, "The jealous Chamberlain", "Завистливый спальник"], ["II", 8, "The little horse's plan", "План конька"], ["II", 9, "The silver mountain", "Серебряная гора"], ["II", 10, "Catching the Firebird", "Ловля Жар-птицы"], ["II", 11, "The Firebird in the palace", "Жар-птица во дворце"]],
   "title_ru": "Золотогривые кони и Жар-птица", "blurb_ru": "Три брата сторожат пшеницу, и только Иван-дурак ловит ночную гостью. Белая кобылица дарит ему коней золотогривых и конька-горбунка; Иван становится царским конюшим и добывает Жар-птицу. Сказка для детей и для совместного слушания.",
   "blurb": "Three brothers, a wheat field watched by night, a white mare, a little humpbacked horse no taller than a loaf of bread, and a feather that glows like fire. Ivan becomes the Tsar's groom and is sent to catch the Firebird. A tale for children and for listening together."},
  {"title": "Tsar-Maiden and the Whale", "from_part": "II", "from_paragraph": 12, "to_part": "III", "thumb_art": "42_whale_island",
   "chapters": [["II", 12, "The Chamberlain plots again", "Спальник замышляет снова"], ["II", 16, "The Tsar-Maiden's boat", "Шлюпка Царь-девицы"], ["II", 19, "The ring from the sea", "Перстень со дна моря"], ["III", 2, "The whale with a village on his back", "Кит с селом на спине"], ["III", 3, "Up into the sky", "На небо"], ["III", 5, "The Moon", "Месяц"], ["III", 8, "The whale lets the ships go", "Кит отпускает корабли"], ["III", 10, "The whale king's court", "Двор кита"], ["III", 14, "The Tsar-Maiden's trick", "Хитрость Царь-девицы"], ["III", 16, "The three cauldrons", "Три котла"], ["III", 19, "The wedding feast", "Свадебный пир"]],
   "title_ru": "Царь-девица, кит и котлы", "blurb_ru": "Спальник посылает Ивана за Царь-девицей, а потом за её перстнем на дно моря. Кит с селом на спине, Месяц, тридцать кораблей, ёрш-забияка и три больших котла. Сказка для детей и для совместного слушания.",
   "blurb": "A jealous Chamberlain sends Ivan for the Tsar-Maiden, and then for her ring at the bottom of the sea. A whale with a village on his back, the Moon, thirty ships, a quarrelsome ruff, and three great cauldrons. A tale for children and for listening together."}],
 "glossary": [
  ["Tsar", "the king of old Russia. His wife is the tsaritsa, or queen."],
  ["Tsar-Maiden", "a princess from beyond the sea, the daughter of the Moon and the sister of the Sun."],
  ["Firebird", "a magic bird whose feathers shine like fire and give light but no warmth."],
  ["Humpbacked Horse", "the tiny magic horse, with two humps and ears a yard long, who is Ivan's faithful friend."],
  ["vershok", "an old Russian measure of about four and a half centimetres: the little horse is three vershoks tall, about as tall as a small loaf of bread."],
  ["Chamberlain", "the Tsar's bedchamber servant, who used to be in charge of the stables and is jealous of Ivan."],
  ["groom", "a servant who looks after horses."],
  ["trough", "a long wooden tub, here used to hide under."],
  ["ruff", "a small, prickly, quarrelsome river fish."],
  ["sturgeon", "a very big fish with a long body, in the tale a nobleman of the whale's court."],
  ["cauldron", "a very big iron pot for boiling water, hung over a fire."],
  ["mead", "a sweet drink made from honey."]],
 "thumb_art": "10_konek_ride", "thumb_position": "50% 40%", "thumb_sub": "A FAIRY TALE IN VERSE FOR CHILDREN<br>FULL-CAST AUDIOBOOK",
 "cover_bg": ["#2c3a78", "#8a9ad8"],
 "kids": True,
 "summary": "Ivan, the youngest brother and the fool of the family, catches a magic mare, is given a tiny humpbacked horse, and wins a place at the Tsar's court. Then he must bring the Firebird, the Tsar-Maiden, and her ring from the bottom of the sea. Pyotr Yershov's fairy tale in verse, for children and for listening together.",
 "site_description": "Three brothers watch the wheat field by night, and only Ivan the fool catches the thief: a white mare, who gives him two golden-maned horses and a little humpbacked horse with ears a yard long. Ivan sells the horses to the Tsar and becomes his groom, and his jealous rival sends him after the Firebird, then the Tsar-Maiden, then her ring from the bottom of the sea. A talking whale with a village on his back, the Moon and the Sun, thirty ships, and three cauldrons later, Ivan himself becomes the Tsar. Pyotr Yershov's fairy tale in verse (1834), in simple English verse for children and for listening together, as a full-cast audiobook in two parts with many illustrations.",
 "tags": ["Yershov", "Pyotr Yershov", "Little Humpbacked Horse", "Konyok-Gorbunok", "Ivan the Fool", "Firebird", "fairy tale", "fairy tale in verse", "bedtime story", "Christmas story", "children's audiobook", "audiobook", "full cast audiobook", "Russian fairy tale", "Russian literature", "public domain", "English audiobook"],
 "hashtags": "#fairytale #bedtimestory #audiobook #Yershov #publicdomain",
 "playlist": "PLVuswr3XMg9E",
 "text_note": "English verse written for children from the Russian original, a free rendering that keeps the story and its order of events but not the rhymes of the original.",
 "ru": {"title": "Конёк-Горбунок", "author": "Пётр Ершов",
  "names": {"I": "Иван и золотогривые кони", "II": "Жар-птица и Царь-девица", "III": "Кит, Месяц и котлы"},
  "note": "Сказка в стихах в издании для чтения с иллюстрациями.",
  "source_note": "Текст с ru.wikisource.org, по седьмому изданию 1868 года (Санкт-Петербург), последнему прижизненному.",
  "contents": "Содержание", "back": "О тексте",
  "small": "Текст сказки находится в общественном достоянии. Названия частей и иллюстрации сделаны для этого издания. Набрано шрифтом Lora (SIL Open Font License).",
  "description": "Три брата сторожат пшеницу, и только Иван-дурак ловит ночную гостью: белую кобылицу, которая дарит ему двух золотогривых коней и конька-горбунка. Иван становится царским конюшим, а завистливый спальник посылает его за Жар-птицей, за Царь-девицей и за её перстнем со дна моря. Сказка в стихах Петра Ершова, чтобы слушать вместе с детьми.",
  "hashtags": "#сказка #аудиокнига #длядетей #Ершов #сказкавстихах #русскиесказки",
  "tags": ["Ершов", "Пётр Ершов", "Конёк-Горбунок", "Иван-дурак", "Жар-птица", "Царь-девица", "сказка в стихах", "сказка на ночь", "аудиокнига для детей", "аудиосказка", "сказки для детей", "слушать сказку", "русская сказка"],
  "thumb_sub": "СКАЗКА В СТИХАХ<br>АУДИОКНИГА"},
 "shot_seconds": 15}
b["figures"] = FIG
json.dump(b, open("book.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("book.json written;", len(FIG), "figures,", len(sc), "scenes")
