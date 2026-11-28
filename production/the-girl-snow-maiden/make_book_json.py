import json
sc = json.load(open("scenes.json"))
A = {"1_fireside": "A cosy room at night: two children under a blue blanket beside a glowing stove, a candle burning, and snow-sparkled stars in the window",
 "2_village": "A snowy village on a holiday: the old man holds a snowball at the gate beside the old woman, while children play with snowballs near a cosy cottage",
 "3_pot": "A little pot with a cloth on the sunny window sill, with the old man and the old woman leaning in to listen to the squeak",
 "4_girl": "The old man rocks the little Snow-Maiden wrapped in a soft towel while the old woman sews her a pink dress by the warm stove",
 "5_fox_door": "A fox with a bandaged head begs little dog Zhuchka at the shed door, with two hens peeping out in the snowy yard",
 "6_berries": "A sunny summer forest where three girls and the Snow-Maiden in her pale-blue dress pick red berries with their baskets",
 "7_tree": "The little Snow-Maiden sits high in a tree in the forest and cries, because she is lost",
 "8_bear": "A big friendly brown bear stands under the tree and looks up at the Snow-Maiden, who shakes her head",
 "8b_wolf": "A grey wolf walks under the tree while the bear walks away, and the Snow-Maiden watches from the branch",
 "8c_fox": "A fox walks round and round the tree and looks up, while the Snow-Maiden stays safely on her branch",
 "9_zhuchka": "Zhuchka the dog barks and licks the Snow-Maiden's face while the fox runs away and the bear hides behind a stump",
 "10_home": "At home the Snow-Maiden sleeps under a blue blanket, the old man and old woman smile with happy tears, and Zhuchka sits with a bowl of milk"}
F = {"1_fireside": [[.3, .62], [.55, .8], [.72, .25]], "2_village": [[.75, .5], [.82, .85], [.2, .55]], "3_pot": [[.52, .55], [.2, .7], [.82, .75]],
 "4_girl": [[.4, .65], [.7, .75], [.3, .6]], "5_fox_door": [[.3, .78], [.65, .55], [.12, .78]], "6_berries": [[.55, .85], [.32, .85], [.72, .82]],
 "7_tree": [[.62, .62], [.5, .3], [.2, .85]], "8_bear": [[.38, .62], [.74, .65], [.5, .35]], "8b_wolf": [[.6, .75], [.74, .65], [.1, .85]],
 "8c_fox": [[.58, .75], [.74, .65], [.3, .6]], "9_zhuchka": [[.4, .7], [.62, .85], [.1, .85]], "10_home": [[.48, .65], [.88, .6], [.3, .75]]}
FX = {k: "snow" for k in ("2_village", "5_fox_door")}
FX.update({"1_fireside": "flicker", "4_girl": "flicker", "10_home": "flicker", "7_tree": "leaves", "6_berries": "leaves"})
b = {
 "slug": "the-girl-snow-maiden", "prefix": "The_Girl_Snow_Maiden", "lang": "en", "title": "The Girl Snow-Maiden",
 "author": "Vladimir Dal", "author_ru": "Владимир Даль", "year": 1870, "title_original": "Девочка Снегурочка",
 "publication_note": "a folk tale retold by Vladimir Dal; first printed in «Pervaya pervinka», 1870",
 "source_note": "Text of Dal's retelling from nukadeti.ru (Wikisource does not have it), after V. I. Dal, Russian tales.",
 "translated_from": "the Russian original",
 "parts": ["I", "II", "III", "IV", "V", "VI", "VII"],
 "names": {"I": "The Snowball", "II": "The Snow-Maiden", "III": "Zhuchka and the Fox", "IV": "The Berries", "V": "Up in the Tree", "VI": "Zhuchka Comes", "VII": "Home Again"},
 "art": {"I": "2_village", "II": "4_girl", "III": "5_fox_door", "IV": "6_berries", "V": "8_bear", "VI": "9_zhuchka", "VII": "10_home"},
 "art_alt": A, "focus": F, "fx": FX, "scenes": sc,
 "glossary": [
  ["Snow-Maiden", "in Russian, Snegurochka (say sneh-goo-ROCH-ka): a girl made of snow who comes to life; “sneg” means snow."],
  ["Zhuchka", "a common name for a little dog in Russia (say ZHOOCH-ka); it comes from “zhuk”, a beetle or bug."],
  ["pot", "a small clay pot, the kind used in a Russian cottage for porridge and soup."],
  ["window sill", "the shelf under a window, where the pot stood in the sun."],
  ["cake", "in the lullaby, a “kokurochka”: a sweet, soft little bun, a loving name for a dear child."],
  ["Mistress Fox", "in Russian tales the fox is often called Lisa Patrikeevna, a clever and sly lady."],
  ["spring snow", "the last soft snow of spring, which melts quickly in the sun."],
  ["Hallo-o", "the long call people used in the forest to find one another when they were lost (in Russian, “Au!”)."]],
 "thumb_art": "9_zhuchka", "thumb_position": "48% 50%", "thumb_sub": "A WINTER TALE FOR CHILDREN<br>FULL-CAST AUDIOBOOK",
 "cover_bg": ["#9fd4ff", "#f8f4ec"],
 "kids": True,
 "summary": "An old man and an old woman have no children. One winter day the old man brings a snowball home and puts it in a pot on the window sill, and the sun turns it into a little girl, the Snow-Maiden. Then she gets lost in the forest, and a bear, a wolf and a fox try to lure her down from her tree. A gentle tale for children, to be listened to together, with a happy ending.",
 "site_description": "An old couple without children makes a wish over a snowball, and the spring sun turns it into a little girl: the Snow-Maiden. She grows up clever and kind, but one summer she goes to the forest to pick berries with her friends and is left behind. A bear, a wolf and a fox each try to coax her down from her tree, and she refuses them all, until she hears her friend Zhuchka the dog bark. Vladimir Dal's retelling of the Russian folk tale, for children and for listening together, in a full-cast English audiobook with many illustrations.",
 "tags": ["Dal", "Vladimir Dal", "Snow-Maiden", "Snegurochka", "fairy tale", "bedtime story", "Christmas story", "winter story", "children's audiobook", "audiobook", "full cast audiobook", "Russian fairy tale", "Russian literature", "public domain", "English audiobook"],
 "hashtags": "#fairytale #bedtimestory #audiobook #Snegurochka #publicdomain",
 "playlist": "PLVuswr3XMg9E",
 "text_note": "Machine translation from the Russian into simple English for children, a draft that needs a human editor. A short spoken introduction and a goodnight were added for the audiobook.",
 "ru": {"title": "Девочка Снегурочка", "author": "Владимир Даль",
  "names": {"I": "Снежный комочек", "II": "Снегурочка", "III": "Жучка и лиса", "IV": "Ягоды", "V": "На дереве", "VI": "Жучка идёт на помощь", "VII": "Снова дома"},
  "note": "Сказка в издании для чтения с оригинальными иллюстрациями.",
  "source_note": "Текст сказки в пересказе В. И. Даля, по сайту nukadeti.ru (на Викитеке этого текста нет).",
  "contents": "Содержание", "back": "О тексте",
  "small": "Текст сказки находится в общественном достоянии (В. И. Даль умер в 1872 году). Названия частей и иллюстрации сделаны для этого издания. Набрано шрифтом Lora (SIL Open Font License).",
  "description": "У старика со старухой не было детей. Старик принёс домой снежный комочек, а солнышко превратило его в девочку Снегурочку. Но однажды в лесу Снегурочка потерялась. Зимняя сказка Владимира Даля, чтобы слушать вместе с детьми."}}
FIG = [("I", 4, "3_pot", "The warm sun melts the snowball, and what is that squeaking in the pot?", "Тёплое солнышко топит снежный комочек, а кто это пищит в горшочке?"),
 ("III", 5, "12_zhuchka_goes", "Poor Zhuchka leaves the yard, and the Snow-Maiden is sorry to see her go.", "Бедная Жучка уходит со двора, и Снегурочке её жалко."),
 ("IV", 3, "7_tree", "Lost in the forest, the Snow-Maiden climbs a tree and calls: Hallo-o!", "Потерялась Снегурочка в лесу, залезла на дерево и кричит: «Ау!»"),
 ("V", 9, "8b_wolf", "The grey wolf comes, but the Snow-Maiden does not trust him.", "Пришёл серый волк, но Снегурочка ему не верит."),
 ("V", 15, "8c_fox", "The sly fox walks round and round the tree, but the girl will not come down.", "Хитрая лиса ходит вокруг дерева, а девочка не слезает.")]
b["figures"] = [{"part": a, "after": n, "art": art, "caption": c, "caption_ru": cr} for a, n, art, c, cr in FIG]
json.dump(b, open("book.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
