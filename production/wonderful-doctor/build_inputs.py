#!/usr/bin/env python3
"""The Wonderful Doctor: the translation (written by hand, paragraph for paragraph), source_clean.json, the voice script and voices."""
import json
ru = json.load(open("paras_ru.json", encoding="utf-8"))[:61]
SPLIT = {"I": (0, 6), "II": (7, 26), "III": (27, 45), "IV": (46, 52), "V": (53, 60)}
EN = [
# 0
"The following story is not the fruit of idle invention. Everything described here really happened in Kiev some thirty years ago, and to this day it is kept sacred, down to the smallest detail, in the memory of the family of whom I shall speak. For my part, I have only changed the names of some of the people in this touching story and given a written form to what was told aloud.",
# 1
"“Grisha, hey, Grisha! Look at the piglet... He's laughing... Yes... And what's in his mouth! Look, look... there's grass in his mouth, honestly, grass!... What a thing!”",
# 2
"And the two little boys, standing before the huge plate-glass window of a delicatessen, burst into uncontrollable laughter, nudging each other in the ribs with their elbows and dancing on the spot in spite of themselves because of the bitter cold. They had already been standing for more than five minutes in front of this magnificent display, which stirred their minds and their stomachs alike. Here, lit by the bright light of hanging lamps, rose whole mountains of firm red apples and oranges; there stood neat pyramids of tangerines, glowing softly gold through the tissue paper that wrapped them; on platters lay enormous smoked and pickled fish, their mouths hideously open and their eyes bulging; lower down, wreathed in garlands of sausages, were juicy sliced hams with a thick layer of pinkish fat... A countless number of little jars and boxes of salted, boiled and smoked delicacies completed this splendid picture, and looking at it both boys forgot for a minute the twelve degrees of frost and the important errand their mother had given them, an errand that had ended so unexpectedly and so sadly.",
# 3
"The older boy was the first to tear himself away from this enchanting sight. He tugged his brother's sleeve and said sternly:",
# 4
"“Come on, Volodya, let's go, let's go... There's nothing for us here...”",
# 5
"Suppressing a heavy sigh at the same moment (the older of them was only ten years old, and besides, both had eaten nothing since morning but thin cabbage soup) and casting a last loving, greedy glance at the delicatessen window, the little boys hurried off down the street. Sometimes, through the misted windows of some house, they saw a Christmas tree, which from far away looked like an enormous bunch of bright, shining spots, and sometimes they even heard the sounds of a merry polka... But they bravely drove away the tempting thought of stopping for a few seconds and pressing an eye to the glass.",
# 6
"As the boys walked on, the streets grew emptier and darker. The beautiful shops, the shining trees, the trotting horses racing along under their blue and red nets, the squeal of sleigh runners, the holiday bustle of the crowd, the cheerful hum of shouts and talk, the frost-reddened, laughing faces of elegant ladies, all was left behind. There stretched empty lots, crooked narrow lanes, gloomy unlit slopes... At last they reached a crooked, tumbledown house that stood by itself; its lower part, really a cellar, was of stone, and its upper part of wood. Going round a cramped, icy and filthy yard, which served all the tenants as a natural rubbish pit, they went down into the cellar, walked in the dark along the common corridor, felt for their own door and opened it.",
# 7
"The Merzalovs had been living in this underground hole for more than a year. Both little boys had long since grown used to these sooty walls that wept with damp, to the wet rags drying on a rope stretched across the room, and to that terrible smell of paraffin fumes, dirty children's linen and rats, the true smell of poverty. But today, after everything they had seen in the street, after the holiday rejoicing they had felt everywhere, their little hearts tightened with a sharp pain that was not a child's. In the corner, on a dirty wide bed, lay a girl of about seven; her face was burning, her breath was short and laboured, and her wide, shining eyes stared fixedly and aimlessly. Beside the bed, in a cradle hung from the ceiling, a baby was screaming, wrinkling its face, straining and choking. A tall, thin woman, with a worn, tired face that seemed blackened by grief, was kneeling by the sick girl, straightening her pillow and at the same time not forgetting to push the swinging cradle with her elbow. When the boys came in, and white clouds of frosty air burst into the cellar after them, the woman turned her anxious face toward them.",
# 8
"“Well? What happened?” she asked abruptly and impatiently.",
# 9
"The boys were silent. Only Grisha loudly wiped his nose on the sleeve of his coat, which had been made over from an old quilted dressing gown.",
# 10
"“Did you take the letter?... Grisha, I am asking you, did you hand over the letter?”",
# 11
"“I handed it over,” Grisha answered, his voice hoarse with the cold.",
# 12
"“Well, and then? What did you say to him?”",
# 13
"“Everything, just as you taught me. I said, here is a letter from Merzalov, your former steward. And he swore at us: ‘Get out of here, he says... You scum...’”",
# 14
"“But who was it? Who was talking to you?... Tell me properly, Grisha!”",
# 15
"“The porter was talking... Who else? I said to him: ‘Take the letter, uncle, pass it on, and I'll wait down here for an answer.’ And he said: ‘Oh yes, he says, hold out your pocket... The master has nothing better to do than read your letters...’”",
# 16
"“Well, and you?”",
# 17
"“I told him everything, just as you taught me: ‘We have nothing to eat... Mashutka is ill... She's dying...’ I said: ‘As soon as Father finds a job, he will thank you, Savely Petrovich, honestly he will.’ Well, and just then the bell rang and rang, and he said to us: ‘Get out of here, the devil take you! Don't let me see you here again!...’ And he even hit Volodya on the back of the head.”",
# 18
"“And he hit me on the back of the head,” said Volodya, who had been listening closely to his brother's story, and he scratched the back of his head.",
# 19
"The older boy suddenly began to rummage anxiously in the deep pockets of his gown. At last he pulled out a crumpled envelope, laid it on the table and said:",
# 20
"“Here it is, the letter...”",
# 21
"The mother asked no more questions. For a long time in the stuffy, clammy room there was nothing to be heard but the frantic crying of the baby and Mashutka's short, quick breathing, more like endless monotonous moans. Suddenly the mother said, turning round:",
# 22
"“There's some borscht, left over from dinner... Perhaps you would eat? Only it's cold, there's nothing to warm it with...”",
# 23
"At that moment unsteady footsteps were heard in the corridor, and the rustle of a hand feeling in the dark for the door. The mother and both boys, all three even pale with tense expectation, turned toward the sound.",
# 24
"Merzalov came in. He wore a summer coat and a summer felt hat, and no galoshes. His hands were swollen and blue with cold, his eyes were sunken, his cheeks clung around his gums like a dead man's. He did not say one word to his wife, and she did not ask him one question. They understood each other from the despair that they read in each other's eyes.",
# 25
"In this terrible, fateful year, misfortune after misfortune had fallen stubbornly and mercilessly on Merzalov and his family. First he himself fell ill with typhoid fever, and all their meagre savings went on his treatment. Then, when he recovered, he learned that his place, the modest post of house steward at twenty-five roubles a month, was already taken by someone else... There began a desperate, feverish hunt for odd jobs, for copying work, for any tiny position, the pawning and re-pawning of things, the selling of every scrap of household cloth. And then the children began to fall ill. Three months ago one girl had died, and now the other lay in a fever, unconscious. Elizaveta Ivanovna had to nurse the sick girl, feed the little one at her breast, and walk almost to the other end of the city to a house where she did washing by the day.",
# 26
"All of today had been spent in superhuman efforts to squeeze out from somewhere at least a few kopecks for Mashutka's medicine. For this purpose Merzalov had run round half the city, begging and humbling himself everywhere; Elizaveta Ivanovna had gone to her mistress; the children had been sent with a letter to the gentleman whose house Merzalov had formerly managed... But everyone made excuses, either the bustle of the holiday or lack of money... Some, like the porter of his former employer, simply drove petitioners off the steps.",
# 27
"For about ten minutes no one could utter a word. Suddenly Merzalov rose quickly from the chest on which he had been sitting until then and with a resolute movement pulled his tattered hat down further over his forehead.",
# 28
"“Where are you going?” Elizaveta Ivanovna asked anxiously.",
# 29
"Merzalov, who had already taken hold of the door handle, turned round.",
# 30
"“It is all the same, sitting here will help nothing,” he answered hoarsely. “I'll go out again... I'll try begging for alms, at least.”",
# 31
"Having come out into the street, he walked on aimlessly. He was looking for nothing, he hoped for nothing. He had long since lived through that burning time of poverty when you dream of finding a wallet full of money in the street or of suddenly receiving an inheritance from some unknown second cousin. Now he was seized by an irresistible desire to run anywhere, to run without looking back, only so as not to see the silent despair of his hungry family.",
# 32
"Beg for alms? He had already tried that today, twice. But the first time some gentleman in a raccoon fur coat had lectured him that one must work, not whine, and the second time they had promised to send him to the police.",
# 33
"Without noticing it, Merzalov found himself in the centre of the city, at the fence of a thick public garden. Since he had been going uphill all the time, he was out of breath and felt tired. Mechanically he turned in at the gate and, having walked along a long avenue of lime trees buried in snow, he sank down on a low garden bench.",
# 34
"It was quiet and solemn here. The trees, wrapped in their white robes, dozed in motionless majesty. Now and then a lump of snow broke off from an upper branch, and one could hear it rustling as it fell and caught on other branches. The deep silence and great calm that guarded the garden suddenly awoke in Merzalov's tormented soul an unbearable thirst for the same calm, the same silence.",
# 35
"“If only I could lie down and fall asleep,” he thought, “and forget about my wife, about my hungry children, about sick Mashutka.” Slipping his hand under his waistcoat, Merzalov felt a fairly thick rope that served him as a belt. The thought of suicide stood quite clearly in his mind. But he was not horrified by this thought, and did not shudder for a moment before the darkness of the unknown.",
# 36
"“Rather than perish slowly, is it not better to choose a shorter way?” He was already about to get up to carry out his terrible intention, but at that moment the creak of footsteps sounded at the end of the avenue, distinct in the frosty air. Merzalov turned in that direction with rage. Someone was walking along the avenue. First there was only the light of a cigar, now flaring, now dying. Then little by little Merzalov could make out an old man of small stature, in a warm cap, a fur coat and tall galoshes. Drawing level with the bench, the stranger suddenly turned sharply toward Merzalov and, lightly touching his cap, asked:",
# 37
"“Will you allow me to sit here?”",
# 38
"Merzalov deliberately turned sharply away from the stranger and moved to the edge of the bench. About five minutes passed in mutual silence, during which the stranger smoked his cigar and (Merzalov felt it) watched his neighbour out of the corner of his eye.",
# 39
"“What a lovely night,” the stranger suddenly began. “Frosty... still. What a charm there is in a Russian winter!”",
# 40
"His voice was soft, kindly, an old man's voice. Merzalov was silent, without turning round.",
# 41
"“And I have been buying little presents for the children of some friends,” the stranger went on (in his hands were several parcels). “And on the way I couldn't resist it, I made a detour to go through the garden: it is so very beautiful here.”",
# 42
"Merzalov was in general a gentle and shy man, but at the stranger's last words a sudden surge of desperate fury seized him. With a sharp movement he turned toward the old man and shouted, waving his arms foolishly and gasping:",
# 43
"“Presents!... Presents!... Presents for friends' children!... And I... and I, my dear sir, at this very moment have children dying of hunger at home... Presents!... And my wife's milk has dried up, and the baby has not eaten all day... Presents!...”",
# 44
"Merzalov expected that after these wild, angry cries the old man would get up and go away, but he was mistaken. The old man brought close to him his intelligent, serious face with its grey side-whiskers and said in a friendly but earnest tone:",
# 45
"“Wait... do not be agitated! Tell me everything in order and as briefly as you can. Perhaps together we shall think of something for you.”",
# 46
"There was something so calm and inspiring of trust in the stranger's remarkable face that Merzalov at once, without the slightest concealment, though in terrible agitation and haste, told his story. He told of his illness, of the loss of his place, of the death of his child, of all his misfortunes up to the present day. The stranger listened without interrupting him with a single word, and only looked more and more searchingly and intently into his eyes, as if wishing to penetrate to the very depths of this aching, rebellious soul. Suddenly, with a quick, quite youthful movement, he jumped up from his seat and seized Merzalov by the hand. Merzalov involuntarily stood up too.",
# 47
"“Let us go!” said the stranger, drawing Merzalov along by the hand. “Let us go quickly!... It is your luck that you met a doctor. Of course I cannot vouch for anything, but... let us go!”",
# 48
"Some ten minutes later Merzalov and the doctor were already entering the cellar. Elizaveta Ivanovna lay on the bed beside her sick daughter, her face buried in the dirty, greasy pillows. The boys were slurping borscht, sitting in the same places. Frightened by their father's long absence and their mother's stillness, they were crying, smearing the tears over their faces with dirty fists and shedding them copiously into the sooty iron pot. On entering the room, the doctor took off his coat and, remaining in an old-fashioned, rather shabby frock coat, went up to Elizaveta Ivanovna. She did not even raise her head as he approached.",
# 49
"“Come, come now, my dear,” said the doctor, gently stroking the woman's back. “Get up! Show me your sick girl.”",
# 50
"And just as in the garden a little while before, something kind and persuasive in his voice made Elizaveta Ivanovna get up from the bed at once and do without a word everything the doctor said. Two minutes later Grisha was already lighting the stove with firewood which the wonderful doctor had sent to the neighbours for, Volodya was blowing with all his might at the samovar, and Elizaveta Ivanovna was wrapping Mashutka in a warm compress... A little later Merzalov appeared too. With the three roubles received from the doctor he had managed in that time to buy tea, sugar and rolls and to get hot food at the nearest tavern. The doctor was sitting at the table writing something on a scrap of paper which he had torn from his notebook. Having finished this, and having drawn at the bottom some peculiar flourish in place of a signature, he stood up, covered what he had written with a tea saucer and said:",
# 51
"“With this paper you will go to the chemist's... give it every two hours, a teaspoonful. That will make the little one cough up the phlegm... Continue the warm compress... Besides that, even if your daughter gets better, in any case call in Doctor Afrosimov tomorrow. He is a capable physician and a good man. I shall warn him at once. And now, goodbye, ladies and gentlemen! God grant that the coming year may be a little more lenient to you than this one, and above all, never lose heart.”",
# 52
"Having shaken hands with Merzalov and Elizaveta Ivanovna, who still had not recovered from their astonishment, and having patted on the cheek, in passing, Volodya, who stood with his mouth open, the doctor quickly thrust his feet into his deep galoshes and put on his coat. Merzalov came to himself only when the doctor was already in the corridor, and he rushed after him.",
# 53
"Since it was impossible to make anything out in the dark, Merzalov shouted at random:",
# 54
"“Doctor! Doctor, wait!... Tell me your name, doctor! Let my children at least pray for you!”",
# 55
"And he moved his hands about in the air to catch the invisible doctor. But at that moment, at the other end of the corridor, a calm old man's voice said:",
# 56
"“Oh! What nonsense you have thought up!... Go back home quickly!”",
# 57
"When he came back, a surprise awaited him: under the tea saucer, together with the wonderful doctor's prescription, lay several large banknotes...",
# 58
"That same evening Merzalov learned the name of his unexpected benefactor as well. On the chemist's label attached to the bottle of medicine, in the chemist's clear hand, was written: “By the prescription of Professor Pirogov.”",
# 59
"I heard this story, and more than once, from the lips of Grigory Emelyanovich Merzalov himself, the very Grisha who on the Christmas Eve I have described shed tears into a sooty pot of cold borscht. He now holds a fairly large, responsible post in one of the banks, and has a name for being a model of honesty and of responsiveness to the needs of the poor. And each time, finishing his tale of the wonderful doctor, he adds in a voice trembling with hidden tears:",
# 60
"“From that time it was as if a kindly angel had come down into our family. Everything changed. At the beginning of January Father found a place, Mashutka got on her feet, and my brother and I were placed in school at public expense. That holy man simply worked a miracle. And we saw our wonderful doctor only once after that, when he was carried, dead, to his own estate of Vishnya. And even then we did not see him, because that great, mighty and holy thing which lived and burned in the wonderful doctor in his lifetime had been extinguished beyond return.”",
]
assert len(EN) == 61 == len(ru)
NAMES = {"I": "The Shop Window", "II": "The Cellar", "III": "The Garden", "IV": "The Doctor", "V": "The Name"}
SPEAKER = {1: "GRISHA", 4: "VOLODYA", 8: "MOTHER", 10: "MOTHER", 11: "GRISHA", 12: "MOTHER", 13: "GRISHA", 14: "MOTHER", 15: "GRISHA",
           16: "MOTHER", 17: "GRISHA", 18: "VOLODYA", 20: "GRISHA", 22: "MOTHER", 28: "MOTHER", 30: "MERZALOV", 37: "DOCTOR",
           39: "DOCTOR", 41: "DOCTOR", 43: "MERZALOV", 45: "DOCTOR", 47: "DOCTOR", 49: "DOCTOR", 51: "DOCTOR", 54: "MERZALOV",
           56: "DOCTOR", 60: "GRIGORY"}
T, S, rows, n = {}, [], [], 0
for part, (a, b) in SPLIT.items():
    T[part] = EN[a:b + 1]; S.append({"part": part, "paragraphs": ru[a:b + 1], "other_blocks": []})
    print(part, NAMES[part], sum(len(x.split()) for x in EN[a:b + 1]), "words")
    for k, i in enumerate(range(a, b + 1), 1):
        n += 1; rows.append({"id": n, "part": part, "paragraph": k, "speaker": SPEAKER.get(i, "NARRATOR"), "text": EN[i]})
json.dump(T, open("translation_en.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(S, open("source_clean.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(rows, open("Wonderful_Doctor_voice_script.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
with open("Wonderful_Doctor_voice_script.md", "w", encoding="utf-8") as f:
    cur = None
    for r in rows:
        if r["part"] != cur: cur = r["part"]; f.write(f"\n## {cur} · {NAMES[cur]}\n\n")
        f.write(f"**{r['speaker']}**: {r['text']}\n\n")
json.dump({"NARRATOR": {"voice": "bm_george", "speed": 0.95, "lang": "en-gb"},
           "GRISHA": {"voice": "bm_daniel", "speed": 1.06, "lang": "en-gb"},
           "VOLODYA": {"voice": "bm_daniel", "speed": 1.14, "lang": "en-gb"},
           "MOTHER": {"voice": "bf_emma", "speed": 0.95, "lang": "en-gb"},
           "MERZALOV": {"voice": "bm_lewis", "speed": 0.97, "lang": "en-gb"},
           "GRIGORY": {"voice": "bm_lewis", "speed": 0.93, "lang": "en-gb"},
           "DOCTOR": {"voice": "bm_fable", "speed": 0.9, "lang": "en-gb"}}, open("voices_kokoro.json", "w"), indent=1)
print(n, "segments,", sum(len(x.split()) for x in EN), "English words,", sum(len(x.split()) for x in ru), "Russian words")
