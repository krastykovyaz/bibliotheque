import json
sc = json.load(open("scenes.json"))
sc[0]["id"] = 1   # the picture starts with the spoken title line
A = {"1_table": "A winter-night dining room: five children at a round table under a hanging lamp, lotto cards, a saucer of kopecks, nutshells and an apple",
 "2_greedy": "Grisha, the greedy nine-year-old with the shaven head, and clever, proud Anya, watching the saucer of coins closely",
 "3_calm": "Little Sonya laughing and clapping, round Alyosha puffing and staring, and the cook's son Andrei dreamily looking at the numbers",
 "4_cockroach": "A big cockroach runs across the tablecloth among the lotto cards, while Sonya cries out and Grisha digs in his father's cap for the next barrel",
 "5_window": "The children stare, mouths open, at the dark frosty window where a church and the reflected lamp can be seen",
 "6_vasya": "Sleepy, bored Vasya in his school uniform holds out a rouble note while the players tell him to put in a kopeck",
 "7_search": "The whole family on the floor with the lamp, hunting in the dark for a lost kopeck among nutshells",
 "8_bed": "Mama's big bed: Sonya, Alyosha, Grisha, Anya and Andrei fast asleep in a heap, with kopecks scattered over the quilt and the moon at the window"}
F = {"1_table": [[.5, .62], [.27, .5], [.8, .5]], "2_greedy": [[.3, .4], [.72, .4], [.5, .82]], "3_calm": [[.19, .42], [.5, .4], [.82, .45]],
 "4_cockroach": [[.6, .82], [.77, .3], [.25, .35]], "5_window": [[.5, .4], [.15, .62], [.85, .62]], "6_vasya": [[.8, .72], [.45, .45], [.25, .6]],
 "7_search": [[.5, .85], [.2, .8], [.85, .8]], "8_bed": [[.3, .45], [.6, .45], [.9, .45]]}
FX = {k: "flicker" for k in A}
FIG = [
 {"part": "I", "after": 9, "art": "4_cockroach", "caption": "“A cockroach, a cockroach!” cries Sonya.", "caption_ru": "«Прусак, прусак!» — вскрикивает Соня."},
 {"part": "III", "after": 18, "art": "7_search", "caption": "They take down the lamp and crawl under the table to look for the kopeck.", "caption_ru": "Снимают лампу и лезут под стол искать копейку."},
 {"part": "III", "after": 22, "art": "8_bed", "caption": "Good night!", "caption_ru": "Спокойной ночи!"}]
b = {
 "slug": "children-chekhov", "prefix": "Children", "lang": "en", "title": "Children",
 "author": "Anton Chekhov", "author_ru": "Антон Чехов", "year": 1886, "title_original": "Детвора",
 "publication_note": "first published in Peterburgskaya gazeta, 20 January 1886, under the pen name A. Chekhonte",
 "source_note": "Text from ru.wikisource.org, after A. P. Chekhov, Complete Works and Letters, vol. 4.",
 "translated_from": "the Russian original",
 "parts": ["I", "II", "III"],
 "names": {"I": "Lotto at the Table", "II": "Ears, Bells and Slaps", "III": "Vasya's Rouble"},
 "art": {"I": "1_table", "II": "5_window", "III": "6_vasya"},
 "art_alt": A, "focus": F, "fx": FX, "scenes": sc, "figures": FIG,
 "glossary": [
  ["lotto", "a number game, the ancestor of bingo. Each player has cards with numbers and covers them with glass counters as a keeper draws numbered wooden barrels out of a bag (here, the father's cap)."],
  ["kopeck, rouble", "Russian money; a hundred kopecks make a rouble. The children's stake is one kopeck, so Vasya's rouble is a hundred times too big for the game."],
  ["the numbers' nicknames", "in Russian lotto each number has a funny name; the children call seven “the poker”, eleven “the sticks”, seventy-seven “Semyon Semyonych”, ninety “grandfather”, and twenty-eight “we're mowing hay”."],
  ["two rows with one number missing", "in the Russian original, “two katernas”: a row on a card with four of its five numbers already covered."],
  ["christening", "the church ceremony at which a baby is named; the grown-ups are at a party after one."],
  ["preparatory class, fifth form", "school years in tsarist Russia: Grisha is in the first, preparatory class; Vasya is in the fifth class of the gymnasium (secondary school)."],
  ["Agafya Ivanovna, Philip Philipych", "Russians use a first name plus the father's first name (a patronymic): Agafya, daughter of Ivan; Philip, son of Philip. The nurse is Agafya Ivanovna; Philip Philipych is a grown-up the children know."],
  ["the cook's son", "Andrei is a servant's child, in a cotton shirt, and has no money of his own, which is why he cannot play when his kopecks are gone."],
  ["copper cross", "a small cross worn on a cord by Orthodox Christian children."],
  ["cockroach", "in the original, a “prusak”, the small reddish cockroach that lived in Russian houses."],
  ["chemise", "a plain white undergarment, worn under a dress or as a nightdress."]],
 "thumb_art": "3_calm", "thumb_position": "50% 40%", "thumb_sub": "A SHORT STORY<br>FULL-CAST AUDIOBOOK",
 "cover_bg": ["#3a1f26", "#efe3c8"],
 "summary": "While their parents are away at a christening, five children play lotto for kopecks at the dining table. A funny, tender sketch of greed, pride, fear and sleep, by Anton Chekhov.",
 "site_description": "Papa, Mama and Aunt Nadya have gone to a christening, and Grisha, Anya, Sonya, Alyosha and the cook's son Andrei sit up playing lotto for kopecks under the hanging lamp. Grisha plays for the money, Anya for pride, Sonya for the fun of it, Alyosha for the quarrels, and Andrei for the numbers themselves, until a bell is heard in the dark, the older brother Vasya wants to join in with a rouble, and a kopeck is lost under the table. Chekhov's early sketch of childhood, in a full-cast English audiobook.",
 "tags": ["Chekhov", "Anton Chekhov", "Children", "Detvora", "audiobook", "full cast audiobook", "short story", "Christmas story", "classic literature", "Russian literature", "public domain", "English audiobook"],
 "hashtags": "#Chekhov #audiobook #classicliterature #shortstory #publicdomain",
 "playlist": "PLVuswr3XMg9E",
 "text_note": "Translated from the Russian, a draft that needs a human editor.",
 "ru": {"title": "Детвора", "author": "Антон Чехов",
  "names": {"I": "Лото за столом", "II": "Уши, колокол и затрещины", "III": "Васин рубль"},
  "note": "Рассказ в издании для чтения с оригинальными иллюстрациями.",
  "source_note": "Текст с ru.wikisource.org, по изданию: А. П. Чехов. Полное собрание сочинений и писем, т. 4.",
  "contents": "Содержание", "back": "О тексте",
  "small": "Текст рассказа находится в общественном достоянии. Названия частей и иллюстрации сделаны для этого издания. Набрано шрифтом Lora (SIL Open Font License).",
  "description": "Папы, мамы и тёти Нади нет дома: они уехали на крестины. Гриша, Аня, Соня, Алёша и кухаркин сын Андрей сидят за столом под висячей лампой и играют в лото на копейки. Гриша играет ради денег, Аня из самолюбия, Соня для удовольствия, Алёша ради ссоры, Андрей ради самих цифр. Ранний рассказ Чехова о детях и о том, как незаметно приходит сон."}}
json.dump(b, open("book.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
