#!/usr/bin/env python3
"""Writes book.json (scene ids are found by a snippet of the text of the voice script). Run after build_inputs.py."""
import json, re
rows = json.load(open("The_Islanders_voice_script.json", encoding="utf-8"))
NAMES = json.load(open("translation_en.json")) and None
exec(open("build_inputs.py").read().split("SPK =")[0].split("ROMAN =")[1].join(["ROMAN =", ""]) if False else "")
ROMAN = ["I","II","III","IV","V","VI","VII","VIII","IX","X","XI","XII","XIII","XIV","XV","XVI"]
src = open("build_inputs.py", encoding="utf-8").read()
ns = {}; exec(src[src.index("NAMES = {"):src.index("SPK =")], ns)
N, RN = ns["NAMES"], ns["RU_NAMES"]
# (art, part, snippet of the first row of the scene; None = start of the part), fx
SC = [
 ("1_library","I",None,"flicker"),("1_street","I","Mr Dooley was already crossing the street",None),("1_spare_bed","I","“The one upstairs,” Campbell",None),("1_night_beds","I","At half past eleven Vicar Dooley",None),
 ("2_pince_nez","II",None,None),("2_bedside","II","Mrs Dooley kept trying",None),("2_okelly_doctor","II","In the morning the doctor came",None),
 ("3_doorsteps","III",None,None),("3_window_clouds","III","On Sunday morning, to the amazement",None),("3_drawing_room","III","The bell rang. The clouds thickened",None),("3_okelly_enters","III","We were just talking of you",None),("3_supper","III","They sat down to supper",None),("3_candle_door","III","Saying good night to Campbell","flicker"),
 ("4_office","IV",None,None),("4_didi_waiting","IV","In the waiting room a young lady",None),("4_theatre","IV","After a bottle of Romanée",None),
 ("5_pug","V",None,"flicker"),("5_church_lane","V","The evening was very quiet",None),("5_pug_floor","V","And at No. 72 the fire was covered",None),
 ("6_blue_vase","VI",None,None),("6_dinner","VI","Now everything was in order",None),("6_milly","VI","Lady Campbell could bear it no longer",None),("6_fire_letter","VI","At No. 72, as usual, the fire","flicker"),
 ("7_taxi","VII",None,None),("7_boxing","VII","From the two opposite corners",None),("7_campbell_ring","VII","The referee announced that Mr Smith",None),("7_night_room","VII","Campbell remembered dimly",None),
 ("8_newspaper","VIII",None,None),("8_meeting","VIII","Everything went according to the timetable",None),
 ("9_pug_kiss","IX",None,None),("9_bull","IX","Mr Dooley betook himself",None),
 ("10_moon","X",None,None),("10_okelly_visit","X","O'Kelly came in rarely now",None),("10_picnic","X","“Aha, pistachios?",None),("10_iron","X","And Campbell dreamed of an electric iron",None),
 ("11_army","XI",None,None),("11_armchair","XI","And the vicar, having breakfasted",None),("11_beach","XI","There was no escape from the sun at Sandy Bay",None),("11_cafe","XI","When after bathing they went into a café",None),
 ("12_letter","XII",None,"rain"),("12_shop","XII","And Campbell also definitely wanted to buy underclothes",None),("12_birthday","XII","In the evening O'Kelly turned up","flicker"),
 ("13_lilies","XIII",None,"rain"),("13_vaulted","XIII","Attached to O'Kelly's office","flicker"),("13_dining","XIII","Didi went off to the theatre",None),("13_lane_door","XIII","The streets were empty","rain"),
 ("14_waterman","XIV",None,None),("14_shot","XIV","O'Kelly sat in his study",None),("14_walk","XIV","A minute later the policeman",None),
 ("15_prison","XV",None,"rain"),("15_bedroom","XV","Towards night Mrs Dooley",None),
 ("16_sun","XVI",None,None),("16_bell","XVI","At a quarter to ten",None),
]
scenes, art_for_part, fx = [], {}, {}
first = {}
for r in rows: first.setdefault(r["part"], r["id"])
for art, part, snip, f in SC:
    if snip is None: sid = first[part]; art_for_part[part] = art
    else:
        hits = [r["id"] for r in rows if r["part"] == part and snip in r["text"]]
        assert hits, (art, snip)
        sid = hits[0]
    scenes.append({"id": sid, "art": art})
    if f: fx[art] = f
assert [s["id"] for s in scenes] == sorted(s["id"] for s in scenes), "scenes out of order"
ALT = {
 "1_library": "A vicar's library with timetables pinned in rows on the wall and the vicar standing stiffly beside a desk with a clock",
 "1_street": "A street of identical brick houses: a red motor car has stopped, a man lies in the road with his boots in the air, a red-haired man waves four arms and a vicar looks on",
 "1_spare_bed": "A spare bedroom: an injured man in bed with his boots under the blanket, a lady with a pince-nez, a doctor and a stern vicar",
 "1_night_beds": "A bedroom at night under a bright moon: a vicar lies awake in a nightcap with his hands crossed, and the other bed is empty",
 "2_pince_nez": "A lady's pince-nez lying alone on a table while she stands at a window with swelling clouds",
 "2_bedside": "A patient in bed in the dusk and a lady sitting close beside him",
 "2_okelly_doctor": "A timid doctor dropping his bag as a red-haired lawyer with four arms bursts into the sickroom",
 "3_doorsteps": "A row of identical houses with whitened doorsteps and a line of identical Sunday gentlemen in top hats",
 "3_window_clouds": "A lady at a window watching bright clouds race by, a book forgotten beside her",
 "3_drawing_room": "A parlour full of guests in pink and blue as a tall old lady in grey enters on her son's arm",
 "3_okelly_enters": "A red-haired lawyer in a rumpled jacket arrives late at the party while the guests nudge one another",
 "4_didi_waiting": "A waiting room: a girl with cropped hair smoking on a sofa, a huge man at the papers and a red-haired lawyer",
 "6_milly": "An old lady in grey carries off a white cat in indignation while a lawyer roars with laughter",
 "10_okelly_visit": "A firelit room with a pug on the mantel: a lawyer teasing a stiff man who is counting his savings",
 "3_supper": "A supper table: a man in a kilt, a red-haired lawyer waving an inflatable suitcase, a vicar checking his watch",
 "3_candle_door": "A corridor at night: a lady with a candle says good night to a square-chinned man at his bedroom door",
 "4_office": "A lawyer's office with four typists and a red-haired lawyer introducing his wives to a bewildered newcomer",
 "4_theatre": "A music-hall: a shadow dancer on a lit screen, two men in the stalls and a lady with a pince-nez in a box",
 "5_pug": "A cosy room with a firelit mantelpiece and a porcelain pug, a stiff man sitting on the carpet with papers",
 "5_church_lane": "Children in white collars march by the church, followed by a vicar, a lady and a man in a kilt; a young woman leans on a railing",
 "5_pug_floor": "A dying fire, a young woman lying on the carpet beside a porcelain pug and a man frowning in the doorway",
 "6_blue_vase": "A dining room with the blinds down, a portrait of a square-chinned gentleman, a brass gong and a blue vase of carnations",
 "6_dinner": "A solemn dinner: an old lady with long thin lips, a red-haired guest in a morning coat and a trembling servant in white gloves",
 "6_fire_letter": "A girl drying her hair by the fire over scattered letters, a lawyer on a pouffe and a huge man standing silently",
 "7_taxi": "A taxi racing at night with three people in it, streaks of lamplight behind",
 "7_boxing": "A boxing ring under bright lamps, a blue boxer and a black boxer, a roaring crowd",
 "7_campbell_ring": "A huge bare-chested man stands firm in the ring against the champion while the crowd roars",
 "7_night_room": "A moonlit room: a battered man on a couch, a girl in black pyjamas by him, a porcelain pug grinning on the mantelpiece",
 "8_newspaper": "A newspaper headline about an aristocrat boxer, with a lady and a vicar reading",
 "8_meeting": "A parish committee: a vicar before a list of seventeen items, a man in a kilt and ladies in pink and blue",
 "9_pug_kiss": "A girl in pyjamas holds a porcelain pug up to a shocked vicar's face",
 "9_bull": "A big man lowers his head like a bull and walks at a startled vicar",
 "10_moon": "A summer night in a park: a moon wearing a monocle and two shadowy figures in the bushes",
 "10_picnic": "A picnic of oysters and champagne on the carpet, a lawyer with waving arms, a laughing girl, a woman in a pink chemise at the door",
 "10_iron": "A dream of a gigantic electric iron gliding over a flat world, with a small man admiring it",
 "11_army": "Salvation Army soldiers march through a bright street with banners and a drum while a woman officer hammers at a door",
 "11_armchair": "A vicar dozing politely in an armchair as small reflected suns dance on the walls",
 "11_beach": "A seaside beach with bathers in orange, pink and violet caps, and two figures on the sand",
 "11_cafe": "A seaside café: a lady and a man in a kilt at one table, a red-haired lawyer with a strange parcel and a girl at another",
 "12_letter": "An anonymous letter and a narrow blue envelope on a table, a man at a foggy window with drops running down it",
 "12_shop": "A shop counter with thin silk underclothes, a huge embarrassed man with a box and a girl who hides her face",
 "12_birthday": "A birthday evening: champagne, a lawyer holding out a cheque, a girl tearing paper, an iron on the mantel beside a pug",
 "13_lilies": "A foggy lamplit street: a lawyer with white Easter lilies and a vicar with a flat hat watching from the other side",
 "13_vaulted": "A vaulted room with tapestries, iron lanterns and a low divan; a girl in black pyjamas by the fire and a lawyer",
 "13_dining": "A bright dining room: an old lady, a vicar making a speech, a trembling lady and a seated man",
 "13_lane_door": "A narrow foggy lane at night: an iron-bound door with a light above, a vicar, a man in a kilt holding an enormous key, and a huge man",
 "14_waterman": "A table with a revolver, a torn cheque and a fountain pen, and a huge man standing over it in the morning light",
 "14_shot": "An office desk strewn with papers, a lawyer fallen on them, a huge man with a revolver, wives gasping",
 "14_walk": "A policeman and a huge man walking side by side down a lane between tall smooth walls in the fog",
 "15_prison": "A night crowd outside a prison wall under a lantern, a huge grey bird above, a placard against the sirs",
 "15_bedroom": "A bedroom at night: a vicar asleep in his nightcap and his wife sitting up beside him, screaming",
 "16_sun": "A bright morning outside the prison: a crowd holding watches, a vicar and his wife, a little old man at the gate",
 "16_bell": "A great brass bell and dripping drops of brass, kneeling townsfolk, a woman crying out and a vicar beside her",
}
FOCUS = {
 "default": [[0.3,0.55],[0.7,0.5],[0.5,0.4]],
}
focus = {a: FOCUS["default"] for _, _, _, _ in [(0,0,0,0)] for a in ALT}
focus.update({
 "1_library": [[0.25,0.55],[0.6,0.3],[0.8,0.7]], "1_street": [[0.2,0.55],[0.7,0.8],[0.85,0.6]], "1_spare_bed": [[0.2,0.6],[0.75,0.6],[0.5,0.4]],
 "1_night_beds": [[0.2,0.6],[0.8,0.2],[0.6,0.6]], "2_pince_nez": [[0.28,0.78],[0.75,0.5],[0.5,0.6]], "2_bedside": [[0.25,0.65],[0.75,0.7],[0.5,0.5]],
 "2_okelly_doctor": [[0.15,0.65],[0.5,0.7],[0.9,0.65]], "3_doorsteps": [[0.2,0.65],[0.7,0.65],[0.5,0.3]], "3_window_clouds": [[0.5,0.4],[0.82,0.7],[0.7,0.3]],
 "3_okelly_enters": [[0.5,0.7],[0.2,0.8],[0.75,0.75]], "4_didi_waiting": [[0.72,0.7],[0.3,0.75],[0.2,0.3]], "6_milly": [[0.6,0.75],[0.4,0.8],[0.5,0.4]], "10_okelly_visit": [[0.6,0.7],[0.3,0.75],[0.8,0.3]],
 "3_drawing_room": [[0.78,0.55],[0.3,0.75],[0.55,0.7]], "3_supper": [[0.2,0.7],[0.75,0.65],[0.5,0.45]], "3_candle_door": [[0.45,0.7],[0.82,0.75],[0.6,0.3]],
 "4_office": [[0.8,0.7],[0.3,0.55],[0.55,0.6]], "4_theatre": [[0.5,0.2],[0.3,0.75],[0.8,0.8]], "5_pug": [[0.5,0.25],[0.2,0.75],[0.75,0.75]],
 "5_church_lane": [[0.6,0.8],[0.2,0.75],[0.85,0.35]], "5_pug_floor": [[0.5,0.88],[0.17,0.7],[0.8,0.45]], "6_blue_vase": [[0.5,0.3],[0.85,0.8],[0.5,0.7]],
 "6_dinner": [[0.15,0.75],[0.8,0.75],[0.5,0.65]], "6_fire_letter": [[0.55,0.9],[0.4,0.8],[0.8,0.3]], "7_taxi": [[0.5,0.65],[0.8,0.55],[0.3,0.3]],
 "7_boxing": [[0.35,0.65],[0.7,0.6],[0.5,0.2]], "7_campbell_ring": [[0.35,0.65],[0.7,0.6],[0.15,0.7]], "7_night_room": [[0.5,0.7],[0.85,0.8],[0.2,0.35]],
 "8_newspaper": [[0.5,0.35],[0.15,0.8],[0.9,0.8]], "8_meeting": [[0.5,0.45],[0.2,0.8],[0.85,0.8]], "9_pug_kiss": [[0.46,0.65],[0.7,0.8],[0.33,0.8]],
 "9_bull": [[0.35,0.7],[0.75,0.8],[0.5,0.4]], "10_moon": [[0.66,0.25],[0.5,0.88],[0.2,0.7]], "10_picnic": [[0.28,0.85],[0.8,0.4],[0.5,0.9]],
 "10_iron": [[0.5,0.6],[0.1,0.85],[0.8,0.55]], "11_army": [[0.5,0.7],[0.8,0.8],[0.2,0.8]], "11_armchair": [[0.5,0.6],[0.8,0.3],[0.2,0.2]],
 "11_beach": [[0.5,0.55],[0.78,0.85],[0.3,0.3]], "11_cafe": [[0.2,0.8],[0.7,0.8],[0.5,0.6]], "12_letter": [[0.28,0.78],[0.75,0.6],[0.8,0.2]],
 "12_shop": [[0.2,0.75],[0.55,0.75],[0.9,0.8]], "12_birthday": [[0.2,0.85],[0.7,0.8],[0.8,0.3]], "13_lilies": [[0.25,0.85],[0.75,0.8],[0.5,0.35]],
 "13_vaulted": [[0.56,0.85],[0.8,0.8],[0.45,0.45]], "13_dining": [[0.2,0.8],[0.5,0.7],[0.5,0.25]], "13_lane_door": [[0.5,0.4],[0.65,0.9],[0.3,0.85]],
 "14_waterman": [[0.5,0.78],[0.72,0.85],[0.2,0.4]], "14_shot": [[0.55,0.65],[0.83,0.85],[0.3,0.4]], "14_walk": [[0.45,0.9],[0.5,0.45],[0.7,0.9]],
 "15_prison": [[0.5,0.5],[0.7,0.9],[0.15,0.7]], "15_bedroom": [[0.2,0.65],[0.75,0.6],[0.5,0.3]], "16_sun": [[0.8,0.25],[0.25,0.5],[0.75,0.9]], "16_bell": [[0.5,0.25],[0.43,0.9],[0.6,0.9]],
})
eps = [
 {"title":"The Foreign Body","from_part":"I","to_part":"V","thumb_art":"5_pug","blurb":"A square-chinned gentleman is knocked down outside the house of the Reverend Dooley, author of the Covenant of Compulsory Salvation, and his orderly household begins to come off its rails. Then a lawyer with four arms, four typists who are all his wives, and a porcelain pug named Johnny."},
 {"title":"The Face of a Cultured Man","from_part":"VI","to_part":"X","thumb_art":"7_boxing","blurb":"Lady Campbell's gong and white gloves, a boxing match that goes wrong for the right reasons, a scandal in the Jesmond Star, a vicar kissed by a pug, and a dream of an electric iron that smooths the whole world flat."},
 {"title":"The Triumphant Sun","from_part":"XI","to_part":"XVI","thumb_art":"16_sun","blurb":"The Salvation Army knocks on every door, the seaside is too hot, a blue envelope arrives, and Campbell, who always believed that everything must be reasonable, finds the one thing that is not. Zamyatin's satire ends at half past nine."},
]
glossary = [["Jesmond","a respectable suburb of Newcastle upon Tyne, where Zamyatin lived while supervising the building of icebreakers in 1916-17."],
 ["vicar","the priest of an Anglican parish; here the Reverend Dooley of St Enoch's."],["pince-nez","spectacles without arms that clip onto the nose."],
 ["Honorary Bell-Ringers","a parish society; here a body of pious busybodies who decide what is moral."],["Salvation Army","an evangelical Christian charity with brass bands and a military style."],
 ["bobby","a London policeman, from Sir Robert Peel."],["Marquess of Queensberry rules","the rules of modern boxing, from 1867."],["Rizzio","David Rizzio, secretary of Mary, Queen of Scots, murdered in 1566."],
 ["Waterman pen","the best-known fountain pen of the day."],["the Empire","a music hall in the town."]]
b = {"slug":"the-islanders","prefix":"The_Islanders","lang":"en","title":"The Islanders","author":"Yevgeny Zamyatin","author_ru":"Евгений Замятин","year":1917,
 "title_original":"Островитяне","publication_note":"written in 1917 in Newcastle upon Tyne, first published in 1918 in Petrograd; Zamyatin died in 1937, so the text is in the public domain",
 "source_note":"Text from ru.wikisource.org, after E. I. Zamyatin, Selected Works in two volumes, vol. 1 (Moscow, 1990).","translated_from":"the Russian original",
 "parts":ROMAN,"names":N,"art":art_for_part,"scenes":scenes,"art_alt":ALT,"focus":focus,"fx":fx,"episodes":eps,"glossary":glossary,
 "thumb_art":"5_pug","thumb_position":"50% 50%","thumb_sub":"A NOVELLA<br>FULL-CAST AUDIOBOOK","cover_bg":["#2a3050","#3a2a34"],
 "summary":"In a respectable English town, a vicar who has reduced life to timetables is thrown off his rails when a stranger is run over outside his house. Yevgeny Zamyatin's satire of English order, written in Newcastle in 1917 by the author of We, is funny, sharp and quietly terrifying.",
 "site_description":"In Jesmond, an English town where everything, from the Sunday gentlemen to the doorsteps, is made at the same factory, the Reverend Dooley has reduced life to the timetables of his Covenant of Compulsory Salvation. Then a square-chinned stranger, Campbell, who believes that whatever ought to be, is, is knocked down outside his house, and the machinery begins to fail. Zamyatin wrote it in 1917 while he was building icebreakers in Newcastle, and it is the satire of order that led to his novel We.",
 "tags":["Zamyatin","Yevgeny Zamyatin","The Islanders","audiobook","full cast audiobook","novella","satire","classic literature","Russian literature","England","public domain","English audiobook"],
 "hashtags":"#Zamyatin #audiobook #classicliterature #russianliterature #publicdomain","playlist":"PLVuswr3XMg9E",
 "text_note":"",
 "ru":{"title":"Островитяне","author":"Евгений Замятин","names":RN,"note":"Повесть в издании для чтения с оригинальными иллюстрациями.",
  "source_note":"Текст с ru.wikisource.org, по изданию: Е. И. Замятин, Избранные произведения в двух томах, т. 1 (Москва, 1990).","contents":"Содержание","back":"О тексте",
  "small":"Текст повести находится в общественном достоянии (автор умер в 1937 году). Названия частей и иллюстрации сделаны для этого издания. Набрано шрифтом Lora (SIL Open Font License).",
  "description":"Викарий Дьюли превратил жизнь в расписание. Но в воскресенье у его дома под автомобиль попадает квадратный мистер Кембл, и машина викария начинает ломаться. Сатира Замятина на английский порядок, написанная в Ньюкасле в 1917 году."}}
json.dump(b, open("book.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
print(len(scenes),"scenes;", "first ids", [s["id"] for s in scenes][:10])
