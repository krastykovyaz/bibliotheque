import json, sys
sys.path.insert(0, ".")
import make_art_the_scarlet_flower as A
sc = json.load(open("scenes.json"))
ALT = {n: v[1] for n, v in A.REG.items()}
FOCUS = {n: v[2] for n, v in A.REG.items()}
FX = {n: v[3] for n, v in A.REG.items() if v[3]}
NAMES = {"I": "The Three Gifts", "II": "The Shining Palace", "III": "The Scarlet Flower", "IV": "The Youngest Daughter", "V": "A New Home", "VI": "The Voice in the Garden",
         "VII": "The Beast Shows Himself", "VIII": "Three Days at Home", "IX": "The Spell Is Broken"}
NAMES_RU = {"I": "Три подарка", "II": "Волшебный дворец", "III": "Аленький цветочек", "IV": "Младшая дочь", "V": "Новый дом", "VI": "Голос в саду",
            "VII": "Лесной зверь показывается", "VIII": "Три дня дома", "IX": "Колдовство кончилось"}
ART = {"I": "1_house", "II": "9_palace", "III": "13_flower", "IV": "16_home", "V": "21_waking", "VI": "26_arbor", "VII": "28_dusk", "VIII": "31_home", "IX": "33_return"}
FIG = [  # part, after paragraph, art, English caption, Russian caption
 ("I", 8, "2_crown", "The eldest daughter wants a golden crown that shines in the dark.", "Старшая дочь просит золотой венец, который светит в темноте."),
 ("I", 15, "4_flower_ask", "The youngest asks for only a little scarlet flower.", "Младшая просит только аленький цветочек."),
 ("II", 3, "8_path", "The forest opens a shining path for the merchant.", "Лес открывает купцу светлую тропинку."),
 ("II", 9, "11_bed", "The merchant sleeps in a golden bed and dreams of his daughters.", "Купец спит на золотой кровати и видит во сне дочерей."),
 ("III", 6, "14_beast", "The Beast of the forest is sad about his flower.", "Лесной зверь огорчён из-за своего цветка."),
 ("III", 13, "15_ring", "The Beast gives the merchant a golden ring.", "Зверь дарит купцу золотой перстень."),
 ("IV", 6, "17_gifts", "The gifts are opened: a crown, a mirror and a scarlet flower.", "Подарки открыты: венец, зеркало и аленький цветочек."),
 ("IV", 14, "19_kneel", "“Give me your blessing, father. I will go.”", "«Благослови меня, батюшка. Я поеду».") ,
 ("IV", 21, "20_farewell", "The merchant puts the golden ring on his daughter's finger.", "Отец надевает дочери на пальчик золотой перстень."),
 ("V", 3, "22_replant", "The scarlet flower flies back to its stem and blooms even lovelier.", "Аленький цветочек сам возвращается на стебелёк и цветёт ещё краше."),
 ("V", 8, "23_fire", "Words of fire appear on the white marble wall.", "На белой мраморной стене появляются огненные слова."),
 ("V", 15, "24_maid", "The girl and her maid talk until dawn.", "Девушка и её горничная разговаривают до самой зари."),
 ("V", 18, "25_carriage", "A carriage without horses rides through the forest.", "Карета без лошадей катит по лесу."),
 ("VI", 11, "27_wish", "She begs to see her friend, who hides behind a tree.", "Она просит показаться её друга, а он прячется за деревом."),
 ("VII", 6, "29_friends", "Now they walk through the garden as good friends.", "Теперь они гуляют по саду как добрые друзья."),
 ("VIII", 5, "32_clocks", "The sisters secretly turn the clock back.", "Сёстры тайком переводят часы назад."),
 ("IX", 3, "34_hill", "“Wake up, my dear friend! I love you!”", "«Проснись, мой сердечный друг! Я люблю тебя!»"),
 ("IX", 7, "35_prince", "The spell is broken, and the Beast is a prince again.", "Колдовство кончилось, и зверь снова стал принцем."),
 ("IX", 8, "36_wedding", "A merry wedding feast for everyone.", "Весёлая свадьба для всех."),
]
b = {
 "slug": "the-scarlet-flower", "prefix": "The_Scarlet_Flower", "lang": "en", "title": "The Scarlet Flower",
 "author": "Sergey Aksakov", "author_ru": "Сергей Аксаков", "year": 1858, "title_original": "Аленький цветочек",
 "publication_note": "from «The Childhood Years of Bagrov the Grandson», 1858: the tale of the housekeeper Pelageya",
 "source_note": "Text from ru.wikisource.org, after «Skazki russkikh pisateley» (Moscow, Detskaya literatura, 1980), from S. T. Aksakov's tale as told by the housekeeper Pelageya.",
 "translated_from": "the Russian original",
 "parts": list(NAMES), "names": NAMES, "art": ART, "art_alt": ALT, "focus": FOCUS, "fx": FX, "scenes": sc,
 "figures": [{"part": p, "after": a, "art": n, "caption": c, "caption_ru": cr} for p, a, n, c, cr in FIG],
 "glossary": [
  ["scarlet", "a bright, glowing red colour; in the tale it is the colour of the magic flower."],
  ["merchant", "a man who buys and sells goods, often travelling far over land and sea."],
  ["Beast of the forest", "the strange master of the enchanted palace; in the Russian tale he is called “the wonder of the sea”, a creature nobody has seen before."],
  ["crystal", "very clear, shining glass-like stone; a crystal mirror is the finest kind."],
  ["Persia", "the old name of the country now called Iran."],
  ["word of honour", "a solemn promise that an honest person keeps."],
  ["blessing", "kind wishes and a prayer said over someone dear, especially before a long journey."],
  ["arbour", "a shady little shelter in a garden, woven from leaves, branches and flowers."],
  ["spell", "magic put on someone by a wicked witch; a kind deed can break it."],
  ["mead", "an old drink made from honey, which people drank at feasts."],
  ["Pelageya", "the housekeeper at the Aksakov family home, who told the tale to little Sergey; he wrote it down when he was grown up."]],
 "thumb_art": "29_friends", "thumb_position": "50% 50%", "thumb_sub": "A FAIRY TALE FOR CHILDREN<br>FULL-CAST AUDIOBOOK",
 "cover_bg": ["#ffd0d8", "#fff4d8"],
 "kids": True,
 "summary": "A merchant's youngest daughter asks her father for only a little scarlet flower. He finds it in an enchanted garden, and its shaggy master, the Beast of the forest, asks for one daughter in return. A gentle tale about kindness that sees beyond looks, for children and for listening together.",
 "site_description": "A merchant promises his three daughters gifts from over the sea: a golden crown, a crystal mirror, and, for the youngest, a little scarlet flower. He finds the flower in a magic garden, but the shaggy Beast of the forest who owns it will let him go only if one of his daughters comes to live in the palace. The youngest goes of her own free will. Sergey Aksakov's fairy tale of 1858, told to him as a child by the housekeeper Pelageya, for children and for listening together, in a full-cast English audiobook with many illustrations.",
 "tags": ["Aksakov", "Sergey Aksakov", "The Scarlet Flower", "Beauty and the Beast", "fairy tale", "bedtime story", "Christmas story", "children's audiobook", "audiobook", "full cast audiobook", "Russian fairy tale", "Russian literature", "public domain", "English audiobook"],
 "hashtags": "#fairytale #bedtimestory #audiobook #Aksakov #publicdomain",
 "playlist": "PLVuswr3XMg9E",
 "text_note": "Machine translation from the Russian into simple English for children, a draft that needs a human editor.",
 "ru": {"title": "Аленький цветочек", "author": "Сергей Аксаков", "names": NAMES_RU,
  "note": "Сказка ключницы Пелагеи в издании для чтения вслух, с иллюстрациями.",
  "source_note": "Текст с ru.wikisource.org, по изданию: «Сказки русских писателей» (М.: Детская литература, 1980).",
  "contents": "Содержание", "back": "О тексте",
  "small": "Текст сказки находится в общественном достоянии. Названия частей и иллюстрации сделаны для этого издания. Набрано шрифтом Lora (SIL Open Font License).",
  "description": "Младшая дочь купца просит у отца только аленький цветочек. Отец находит его в волшебном саду, но хозяин сада, лесной зверь, чудо морское, отпускает его лишь за обещание прислать одну из дочерей. Сказка Сергея Аксакова (1858), чтобы слушать вместе с детьми."}}
json.dump(b, open("book.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(len(sc), "scenes;", len(FIG), "figures;", len(ART), "openings")
