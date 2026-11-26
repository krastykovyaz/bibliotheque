#!/usr/bin/env python3
"""The Tale of Tsar Saltan (Pushkin, 1831): the English verse (written by hand for children, paragraph by paragraph against the Russian lines),
source_clean.json (Russian lines kept as lines, the author's text only), the English and the Russian voice scripts, the scene list, the voices.
Reads raw/clean.json (made by clean_src.py from the Wikisource wikitext).

Paragraphs: (part, first line, last line, picture, English pieces). Line numbers are the 0-based numbers in raw/numbered.txt. The Russian voice
script only SPLITS those lines between speakers (SPEAK below): the Russian text is never changed. English pieces: "[SPEAKER] text" starts a piece."""
import json, re

d = json.load(open("raw/clean.json", encoding="utf-8"))["lines"]
assert len(d) == 996, len(d)

# ---- who speaks which Russian lines (everything else: the narrator) -----------------------------------------------------------------------
SPEAK = [(2, 5, "SISTER1"), (6, 9, "SISTER2"), (10, 13, "SISTER3"), (22, 31, "TSAR"), (78, 79, "TSAR"), (116, 123, "GVIDON"), (174, 189, "SWAN"),
         (238, 239, "GVIDON"), (241, 247, "SHIPMEN"), (249, 252, "GVIDON"), (258, 261, "SWAN"), (263, 265, "GVIDON"), (266, 269, "SWAN"),
         (300, 303, "TSAR"), (305, 317, "SHIPMEN"), (319, 321, "TSAR"), (326, 337, "COOK"),
         (354, 357, "SWAN"), (359, 369, "GVIDON"), (371, 375, "SWAN"), (389, 391, "GVIDON"),
         (410, 411, "GVIDON"), (413, 419, "SHIPMEN"), (421, 425, "GVIDON"), (458, 461, "TSAR"), (463, 491, "SHIPMEN"), (493, 495, "TSAR"), (502, 521, "WEAVER"),
         (540, 543, "SWAN"), (545, 547, "GVIDON"), (548, 548, "SWAN"), (549, 559, "GVIDON"), (561, 567, "SWAN"), (584, 594, "CHERNOMOR"),
         (608, 609, "GVIDON"), (611, 617, "SHIPMEN"), (619, 623, "GVIDON"), (658, 661, "TSAR"), (663, 687, "SHIPMEN"), (689, 691, "TSAR"), (695, 713, "BABARIKHA"),
         (736, 739, "SWAN"), (741, 743, "GVIDON"), (744, 744, "SWAN"), (745, 756, "GVIDON"), (760, 767, "SWAN"), (777, 779, "SWAN"), (797, 803, "GVIDON"),
         (824, 825, "GVIDON"), (827, 833, "SHIPMEN"), (835, 842, "GVIDON"), (862, 865, "TSAR"), (867, 909, "SHIPMEN"), (918, 920, "TSAR"), (932, 935, "GVIDON"),
         (977, 978, "TSAR")]
speaker_of = ["NARRATOR"] * len(d)
for a, b, s in SPEAK:
    for i in range(a, b + 1): speaker_of[i] = s

NAMES = {"I": "The Three Sisters", "II": "The Letter and the Barrel", "III": "The Swan and the Kite", "IV": "The Town of Prince Gvidon",
         "V": "The Squirrel with Golden Nuts", "VI": "The Thirty-three Knights", "VII": "The Swan Princess", "VIII": "The Feast"}
RU_NAMES = {"I": "Три сестры", "II": "Письмо и бочка", "III": "Лебедь и коршун", "IV": "Город князя Гвидона", "V": "Белка с золотыми орешками",
            "VI": "Тридцать три богатыря", "VII": "Царевна Лебедь", "VIII": "Пир"}

PARAS = []
def P(part, a, b, art, text): PARAS.append((part, a, b, art, text))

P("I", 0, 13, "1_sisters", """
[NARRATOR] Three girls sat spinning, side by side,
Beside the window, one late evening.
[SISTER1] “If I were queen,” the first one said,
“I'd give a feast, and I'd be glad:
I'd feed the whole wide world, I would,
With pies and puddings, all things good!”
[SISTER2] “If I were queen,” the second sighed,
“I'd weave all day, with joy and pride:
I'd weave enough fine linen cloth
To clothe the world, and not be loath!”
[SISTER3] “If I were queen,” the third one said,
“I'd give the Tsar, my lord, instead,
A hero son, so strong and brave,
A boy the land could trust and save!”""")
P("I", 14, 31, "2_tsar_door", """
[NARRATOR] She hardly finished. Creak! The door
Swung softly open, and in came
The Tsar himself, the ruler of that land.
All the time he had stood behind the fence,
And listened. And the last girl's wish
Had pleased him more than all the rest.
[TSAR] “Good evening, lovely maid,” he said.
“Be queen, and give me, when September comes,
A hero son. And you, dear sisters,
Leave this room, and follow after me,
After me and your sister:
One of you shall be the weaver,
The other shall be the cook.”""")
P("I", 32, 48, "3_wedding", """
[NARRATOR] The Tsar went out. They all set off
For the palace. He did not wait long:
That very evening, they were wed.
Tsar Saltan sat at the merry feast
With his young queen. And then the guests
Led the bride and groom to a bed
Of ivory, white and bright,
And left them there alone.
In the kitchen the cook was cross;
At her loom the weaver wept;
They envied the Tsar's new wife.
And the young queen, without delay,
Soon hoped for a baby of her own.""")
P("II", 49, 61, "4_farewell", """
[NARRATOR] Then war broke out. Tsar Saltan said
Goodbye, and mounted his good horse.
He told her: “Take good care of yourself,
Because you love me.” While he fought
Far away, long and hard,
The time came. God sent them a son,
Small, but as long as a yardstick.
And the queen watched over her baby
Like an eagle over her eaglet;
She sent a messenger with a letter
To make the father glad.""")
P("II", 62, 71, "5_plot", """
[NARRATOR] But the weaver and the cook,
With Babarikha, their neighbour,
Wished to do the queen a harm.
They stopped the messenger, and sent
Another, with this letter, word for word:
“The queen has had, this very night,
Not a son, nor yet a daughter,
Not a mouse, nor yet a frog,
But some strange little animal.”""")
P("II", 72, 79, "6_letter", """
[NARRATOR] When the Tsar heard what the messenger said,
He raged and stormed, and longed to punish him.
But then his heart grew softer, and he said:
[TSAR] “Wait until the Tsar comes home,
And then we shall judge it rightly.”""")
P("II", 80, 93, "7_swap", """
[NARRATOR] The messenger rode back with the Tsar's letter.
But the weaver and the cook,
With Babarikha, their neighbour,
Gave him wine until he slept,
And slipped into his empty bag
Another letter. The sleepy man
Brought it that same day:
“The Tsar commands his boyars,
Without wasting any time,
To put the queen and her little son
Secretly into the sea.”""")
P("II", 94, 105, "8_barrel_launch", """
[NARRATOR] There was nothing to be done. The boyars,
Sad for their Tsar and the young queen,
Came in a crowd to her room.
They told her the Tsar's will,
Her sad lot, and her son's,
Read the order out loud,
And that very hour, they put
The queen and her son in a barrel,
Closed it up with pitch, rolled it down,
And set it afloat on the Ocean:
So, they said, Tsar Saltan had ordered.""")
P("III", 106, 137, "9_wave", """
[NARRATOR] In the blue sky the stars shine bright,
In the blue sea the waves run white;
A cloud goes across the sky,
A barrel across the sea.
Like a sad widow, the queen
Weeps and trembles inside it,
And the baby grows, in there,
Not by the days, but by the hours.
A day went by. The queen cried out.
But the child called to the waves:
[GVIDON] “Wave, my wave, so wild and free!
You go wherever you like, you see;
You polish the stones in the deep,
You flood the land, you lift the ships:
Do not drown us, do not drown us!
Wash us up on the dry land!”
[NARRATOR] And the wave obeyed. At once
It carried the barrel to the shore,
Set it down softly, and rolled away.
Mother and baby were safe.
But who would lift them out?
Would God forget them? The boy stood up
On his little feet, pushed with his head,
Strained a little, and said:
“How can we make a window to the yard?”
He pushed out the bottom, and stepped out.""")
P("III", 138, 151, "10_oak", """
[NARRATOR] Mother and son were free at last.
They saw a hill in a wide field,
The blue sea all around, and over the hill
A green oak. The son thought:
“A good supper would be welcome.”
He broke a branch from the oak
And bent it into a strong bow,
Took the silk cord from his mother's cross
And strung the oak bow with it,
Broke a slender reed, and sharpened
It into a light little arrow,
And went to the edge of the valley
To look for game by the sea.""")
P("III", 152, 189, "11_swan_kite", """
[NARRATOR] He had barely come to the sea
When he heard a sound like a groan.
The sea was not quiet! He looked,
And saw a trouble: a swan
Was struggling among the waves,
And a kite was circling over her.
The poor thing splashed and stirred the water,
But the kite had spread his claws,
And sharpened his beak...
Just then the arrow sang, and grazed
The kite's neck. The kite fell
Into the sea. The prince lowered his bow,
And looked: the kite was sinking,
Crying out, not with a bird's cry,
And the swan swam round him,
Pecking him and hastening the end,
Beating him with her wing into the sea.
And then she spoke to the prince,
In human words:
[SWAN] “Prince, you are my rescuer,
My mighty deliverer!
Do not grieve that for me
You will go hungry for three days,
And that your arrow is lost in the sea;
That sorrow is no sorrow at all.
I will repay you with kindness,
I will serve you in my turn:
You did not rescue a swan,
You saved a maiden's life;
You did not kill a kite,
You shot a wicked wizard.
I shall never forget you:
You will find me everywhere.
But now go home,
Do not grieve, and go to bed.”""")
P("IV", 190, 221, "12_city", """
[NARRATOR] The swan flew away.
The prince and his mother, after a day like that,
Lay down hungry to sleep.
The prince opened his eyes,
Shook off the dreams of the night,
And, amazed, saw before him
A great town, with walls
Of many battlements,
And behind the white walls shone
The golden domes of churches
And of holy monasteries.
He woke his mother quickly. She gasped.
“What is this?” he said. “I see:
My swan is playing for us.”
Mother and son go to the town.
As soon as they passed the gate,
A deafening ringing of bells
Rose from every side.
The people came out to meet them,
The church choir praised God;
In golden carriages
A splendid court met them.
All hailed them aloud,
And crowned the prince
With the prince's cap, and chose him
As their ruler. And in the midst
Of his capital, with his mother's leave,
That same day he began to rule,
And was named Prince Gvidon.""")
P("IV", 222, 252, "13_harbor", """
[NARRATOR] The wind blew over the sea
And drove a little ship along.
It raced over the waves
With its sails billowing.
The sailors marvelled, crowding the deck:
On the island they knew so well,
They saw a wonder, wide awake:
A new golden-domed town,
A harbour with a strong gate;
The cannons on the pier fired,
Telling the ship to land.
The merchants came to the gate.
Prince Gvidon invited them,
Fed them and gave them drink,
And asked them:
[GVIDON] “What do you trade, good sirs,
And where are you sailing now?”
[NARRATOR] The sailors answered:
[SHIPMEN] “We have sailed round the whole world,
Trading in sables
And black-and-silver foxes;
And now our time has come:
We sail straight east,
Past the island of Buyan,
To the glorious land of Saltan.”
[NARRATOR] The prince said to them then:
[GVIDON] “A good journey, gentlemen,
Over the sea-ocean
To glorious Tsar Saltan;
Give him my greetings.”""")
P("IV", 253, 279, "14_mosquito", """
[NARRATOR] The merchants sailed; and Prince Gvidon,
With a sad heart, on the shore
Watched their far-off voyage.
Look! Over the flowing waters
A white swan comes swimming.
[SWAN] “Hello, my handsome prince!
Why so quiet, like a cloudy day?
What is troubling you?”
[NARRATOR] The prince answers sadly:
[GVIDON] “Sadness eats me up,
It has overcome me:
I long to see my father.”
[SWAN] “Is that the trouble? Well, listen:
Would you like to fly over the sea
After the ship? Then be a mosquito!”
[NARRATOR] And she flapped her wings,
Splashed the water with a noise,
And sprinkled him
From head to foot.
At once he shrank to a speck,
Turned into a mosquito,
Flew, and buzzed, and caught
The ship at sea,
Settled quietly on the deck,
And hid in a crack.""")
P("IV", 280, 297, "15_palace", """
[NARRATOR] The wind blows gaily, the ship runs gaily,
Past the island of Buyan,
To the glorious realm of Saltan,
And the longed-for land
Is seen far off at last.
The merchants came ashore.
Tsar Saltan invited them to his palace,
And after them flew our brave little fellow.
He saw: all shining in gold,
Tsar Saltan sat in his hall
On his throne, with his crown,
With a sad thought on his face;
And the weaver and the cook,
With Babarikha, their neighbour,
Sit beside the Tsar,
And look him in the eye.""")
P("IV", 298, 321, "16_sailors", """
[NARRATOR] Tsar Saltan sat the guests at his table,
And asked them:
[TSAR] “Dear guests, my lords,
Have you travelled long? And where?
Is it good beyond the sea, or bad?
And what wonder is there in the world?”
[NARRATOR] The sailors answered:
[SHIPMEN] “We have sailed round the whole world;
Beyond the sea the living is good;
But here is the wonder of the world:
In the sea there was a steep island,
No place to land, no one lived there;
It lay an empty plain,
With one little oak upon it;
And now there stands upon it
A new town with a palace,
With golden-domed churches,
With towers and gardens,
And Prince Gvidon sits in it;
He sends you his greetings.”
[NARRATOR] Tsar Saltan marvels at the wonder.
[TSAR] “If I live,” he says, “I will visit
That wonderful island,
And stay a while with Gvidon.”""")
P("IV", 322, 349, "17_cook_bite", """
[NARRATOR] But the weaver and the cook,
With Babarikha, their neighbour,
Do not want to let him go
To visit the wonderful island.
[COOK] “A wonder, really!” said the cook,
Winking slyly at the others.
“A town by the sea!
Now here is something that is no trifle:
A fir in the forest, a squirrel under the fir;
The squirrel sings little songs
And cracks nuts, nothing but nuts,
And the nuts are no common nuts:
The shells are all of gold,
The kernels pure emerald.
That is what people call a wonder!”
[NARRATOR] Tsar Saltan marvels at the wonder,
But the mosquito gets angrier and angrier,
And stings the aunt, just then,
Right in her right eye.
The cook turned pale, fainted,
And could not see out of that eye.
The servants, the neighbour and the sister
Chase the mosquito, shouting.
“You wretched midge! We'll catch you!”
But he went out of the window,
And calmly to his own island
Flew away across the sea.""")
P("V", 350, 375, "18_swan_sea", """
[NARRATOR] Again the prince walks by the sea,
Never taking his eyes from the blue water.
Look! Over the flowing waves
A white swan comes swimming.
[SWAN] “Hello, my handsome prince!
Why so quiet, like a cloudy day?
What is troubling you?”
[NARRATOR] Prince Gvidon answers her:
[GVIDON] “Sadness eats me up:
I should like to have a wonder of my own.
Somewhere there is a fir in a forest,
And under the fir, a squirrel;
A wonder, truly, not a trifle:
The squirrel sings little songs
And cracks nuts, nothing but nuts,
And the nuts are no common nuts:
The shells are all of gold,
The kernels pure emerald;
But perhaps people tell lies.”
[NARRATOR] The swan answers the prince:
[SWAN] “The world tells the truth of the squirrel;
I know that wonder.
Enough, prince, my dear,
Do not grieve; I am glad to do you a service,
And be your friend.”""")
P("V", 376, 397, "19_squirrel", """
[NARRATOR] With a lighter heart
The prince went home.
He had scarcely stepped into the wide courtyard,
When what? Under a tall fir
He saw a little squirrel, in front of them all,
Cracking a golden nut,
Taking out an emerald,
Gathering the shells,
Laying them in equal heaps,
And singing, with a little whistle,
Before all the honest people:
“In the garden, or the kitchen-garden.”
Prince Gvidon was astonished.
[GVIDON] “Well, thank you,” he said,
“What a swan! God bless her:
The same joy for me, too!”
[NARRATOR] The prince built the squirrel
A crystal house,
Set a guard to watch it,
And besides made a clerk
Keep strict count of the nuts.
The prince gained wealth, the squirrel honour.""")
P("V", 398, 425, "20_horses_ship", """
[NARRATOR] The wind blows over the sea
And drives a little ship along;
It races over the waves
With its sails hoisted,
Past the steep island,
Past the great town.
The cannons on the pier fire,
Telling the ship to land.
The merchants come to the gate.
Prince Gvidon invites them,
Feeds them and gives them drink,
And asks them:
[GVIDON] “What do you trade, good sirs,
And where are you sailing now?”
[NARRATOR] The sailors answered:
[SHIPMEN] “We have sailed round the whole world,
Trading in horses,
All Don stallions;
And now our time has come,
And our way lies far:
Past the island of Buyan,
To the glorious land of Saltan.”
[NARRATOR] The prince says to them then:
[GVIDON] “A good journey, gentlemen,
Over the sea-ocean
To glorious Tsar Saltan;
And tell him: Prince Gvidon
Sends his greetings to the Tsar.”""")
P("V", 426, 455, "21_fly_palace", """
[NARRATOR] The merchants bowed to the prince,
Went out, and set off on their way.
The prince goes to the sea, and the swan
Is already walking on the waves.
The prince begs: his soul asks,
It pulls him and carries him away...
So again she sprinkles him
All over in a moment:
The prince turned into a fly,
Flew, and settled
Between sea and sky
On the ship, and climbed into a crack.
The wind blows gaily, the ship runs gaily,
Past the island of Buyan,
To the realm of glorious Saltan,
And the longed-for land
Is seen far off at last.
The merchants came ashore.
Tsar Saltan invites them to his palace,
And after them flew our brave little fellow.
He saw: all shining in gold,
Tsar Saltan sat in his hall
On his throne, with his crown,
With a sad thought on his face.
And the weaver, with Babarikha
And the one-eyed cook,
Sit beside the Tsar,
Glaring like wicked toads.""")
P("V", 456, 495, "22_sailors2", """
[NARRATOR] Tsar Saltan sat the guests at his table,
And asked them:
[TSAR] “Dear guests, my lords,
Have you travelled long? And where?
Is it good beyond the sea, or bad?
And what wonder is there in the world?”
[NARRATOR] The sailors answered:
[SHIPMEN] “We have sailed round the whole world;
Beyond the sea the living is good;
But here is the wonder of the world:
An island lies in the sea,
A town stands on the island,
With golden-domed churches,
With towers and gardens;
A fir grows before the palace,
And under it a crystal house;
A tame squirrel lives there,
And what a clever one she is!
The squirrel sings little songs
And cracks nuts, nothing but nuts,
And the nuts are no common nuts:
The shells are all of gold,
The kernels pure emerald;
Servants guard the squirrel,
They wait on her in every way,
And a clerk is set over her
To keep strict count of the nuts;
The soldiers salute her;
From the shells they mint coins,
And send them out into the world;
The girls pour the emeralds
Into storerooms, under the floor;
Everyone on that island is rich;
There are no huts, only palaces;
And Prince Gvidon sits in it;
He sends you his greetings.”
[NARRATOR] Tsar Saltan marvels at the wonder.
[TSAR] “If only I live,” he says,
“I will visit that wonderful island,
And stay a while with Gvidon.”""")
P("V", 496, 535, "23_weaver_fly", """
[NARRATOR] But the weaver, the cook,
And Babarikha, their neighbour,
Do not want to let him go
To visit the wonderful island.
With a quiet smile,
The weaver says to the Tsar:
[WEAVER] “What is so wonderful? Well, there!
A squirrel gnaws little stones,
Tosses gold, and rakes
The emeralds into heaps;
You will not surprise us with that,
Whether you tell the truth or not.
There is another wonder in the world:
The sea heaves up in a boiling rage,
Boils over, and begins to roar,
Rushes over the empty shore,
Spreads out in a noisy run,
And there, on the beach, stand,
In scales, burning like fire,
Thirty-three knights,
All handsome, all brave,
Young giants, all alike, as if picked,
And with them uncle Chernomor.
That is a wonder, if you like!
One might truly say so!”
[NARRATOR] The wise guests keep silent;
They do not want to argue with her.
Tsar Saltan marvels at the wonder,
But Gvidon gets angrier and angrier...
He buzzed, and at once
Sat on the aunt's left eye,
And the weaver turned pale:
“Ow!” and went blind in that eye.
Everyone shouts: “Catch him, catch him,
And crush him, crush him...
Just you wait a minute,
Wait...” But the prince out of the window,
And calmly to his own island
Flew back across the sea.""")
P("VI", 536, 567, "24_swan_dusk", """
[NARRATOR] The prince walks by the blue sea,
Never taking his eyes from the blue water.
Look! Over the flowing waves
A white swan comes swimming.
[SWAN] “Hello, my handsome prince!
Why so quiet, like a cloudy day?
What is troubling you?”
[NARRATOR] Prince Gvidon answers her:
[GVIDON] “Sadness eats me up:
I should like to bring a wonder
Into my own land.”
[SWAN] “And what wonder is that?”
[GVIDON] “Somewhere the ocean swells
In a boiling rage, and begins to roar,
Rushes over the empty shore,
Spreads out in a noisy run,
And there, on the beach, stand,
In scales, burning like fire,
Thirty-three knights,
All handsome, all young,
Young giants, all alike, as if picked,
And with them uncle Chernomor.”
[NARRATOR] The swan answers the prince:
[SWAN] “Is that what troubles you?
Do not grieve, my dear: I know that wonder.
Those knights of the sea
Are all my own brothers.
Do not be sad, go home,
And wait for your brothers as guests.”""")
P("VI", 568, 595, "25_knights_sea", """
[NARRATOR] The prince went, forgetting his grief,
Sat on the tower, and began
To look at the sea; and suddenly the sea
Heaved all around,
Splashed out in a noisy run,
And left on the beach
Thirty-three knights;
In scales, burning like fire,
The knights come in pairs,
And, their grey hair shining,
Their uncle walks in front,
And leads them to the town.
The prince runs down from the tower
To meet his dear guests;
The people come hurrying;
The uncle says to the prince:
[CHERNOMOR] “The swan sent us to you,
And gave us this command:
To guard your glorious town,
And to walk round it as watchmen.
From now on, every day,
We shall come together, without fail,
Out of the sea, by your high walls;
So we shall see each other soon,
But now it is time for us to go back to the sea:
The air of the land is heavy for us.”
[NARRATOR] Then they all went home.""")
P("VI", 596, 637, "26_ship3", """
[NARRATOR] The wind blows over the sea
And drives a little ship along;
It races over the waves
With its sails hoisted,
Past the steep island,
Past the great town;
The cannons on the pier fire,
Telling the ship to land.
The merchants come to the gate.
Prince Gvidon invites them,
Feeds them and gives them drink,
And asks them:
[GVIDON] “What do you trade, good sirs,
And where are you sailing now?”
[NARRATOR] The sailors answered:
[SHIPMEN] “We have sailed round the whole world;
We traded in steel,
In pure silver and gold,
And now our time has come;
And our way lies far,
Past the island of Buyan,
To the glorious land of Saltan.”
[NARRATOR] The prince says to them then:
[GVIDON] “A good journey, gentlemen,
Over the sea-ocean
To glorious Tsar Saltan.
And tell him: Prince Gvidon
Sends his greetings to the Tsar.”
[NARRATOR] The merchants bowed to the prince,
Went out, and set off on their way.
The prince goes to the sea, and the swan
Is already walking on the waves.
The prince again: his soul asks...
It pulls him and carries him away...
And again she sprinkles him
All over in a moment.
Now he grew very small:
The prince turned into a bumblebee,
Flew, and buzzed;
Caught the ship at sea,
Quietly settled
On the stern, and hid in a crack.""")
P("VI", 638, 691, "27_bee_palace", """
[NARRATOR] The wind blows gaily, the ship runs gaily,
Past the island of Buyan,
To the realm of glorious Saltan,
And the longed-for land
Is seen far off at last.
The merchants came ashore.
Tsar Saltan invites them to his palace,
And after them flew our brave little fellow.
He saw: all shining in gold,
Tsar Saltan sat in his hall
On his throne, with his crown,
With a sad thought on his face.
And the cook, the weaver, and Babarikha
Sit beside the Tsar:
Between the three of them, they look
With only four eyes.
Tsar Saltan sat the guests at his table,
And asked them:
[TSAR] “Dear guests, my lords,
Have you travelled long? And where?
Is it good beyond the sea, or bad?
And what wonder is there in the world?”
[NARRATOR] The sailors answered:
[SHIPMEN] “We have sailed round the whole world;
Beyond the sea the living is good;
But here is the wonder of the world:
An island lies in the sea,
A town stands on the island,
And every day a marvel happens there:
The sea heaves up in a boiling rage,
Boils over, and begins to roar,
Rushes over the empty shore,
Spreads out in a swift run,
And on the beach there stay
Thirty-three knights,
In golden scales, burning,
All handsome, all young,
Young giants, all alike, as if picked;
And old uncle Chernomor
Comes out of the sea with them,
And leads them out in pairs,
To guard that island,
And walk round it as watchmen;
And there is no guard more reliable,
Nor braver, nor more careful.
And Prince Gvidon sits there;
He sends you his greetings.”
[NARRATOR] Tsar Saltan marvels at the wonder.
[TSAR] “If only I live,” he says,
“I will visit that wonderful island,
And stay a while with the prince.”""")
P("VI", 692, 731, "28_babarikha", """
[NARRATOR] The cook and the weaver
Say never a word. But Babarikha
Smiles and says:
[BABARIKHA] “Who will surprise us with that?
Men come out of the sea
And walk about as watchmen!
Whether they tell the truth or lie,
I see no wonder there.
Are there such wonders in the world?
Here is a true tale that goes about:
Beyond the sea there is a princess,
So lovely you cannot take your eyes off her:
By day she puts out the light of God's day,
By night she lights up the earth,
The moon shines under her braid,
And a star burns on her brow.
And she is stately, and glides
Like a peahen;
And when she speaks,
It is like a little brook murmuring.
One may truly say:
That is a wonder, if you like!”
[NARRATOR] The wise guests keep silent:
They do not want to argue with an old woman.
Tsar Saltan marvels at the wonder,
But the prince, though he is angry,
Spares the eyes
Of his old grandmother:
He buzzes over her, circles,
And lands right on her nose.
The knight stung her nose:
A blister rose on her nose.
And again there was an alarm:
“Help, for heaven's sake!
Guards! Catch him, catch him,
And crush him, crush him...
Just you wait a minute,
Wait!..” But the bumblebee out of the window,
And calmly to his own island
Flew back across the sea.""")
P("VII", 732, 767, "29_swan_bride", """
[NARRATOR] The prince walks by the blue sea,
Never taking his eyes from the blue water.
Look! Over the flowing waves
A white swan comes swimming.
[SWAN] “Hello, my handsome prince!
Why so quiet, like a cloudy day?
What is troubling you?”
[NARRATOR] Prince Gvidon answers her:
[GVIDON] “Sadness eats me up:
People marry; I look around,
And only I go about unmarried.”
[SWAN] “And whom have you in mind?”
[GVIDON] “Why, they say there is a princess
In the world, so lovely you cannot take your eyes off her.
By day she puts out the light of God's day,
By night she lights up the earth,
The moon shines under her braid,
And a star burns on her brow.
And she is stately, and glides like a peahen;
And she speaks so sweetly,
Like a little brook murmuring.
But is it true?”
[NARRATOR] The prince waits for the answer in fear.
The white swan is silent
And, after thinking, says:
[SWAN] “Yes! There is such a maiden.
But a wife is not a glove:
You cannot shake her off your white hand,
Nor tuck her into your belt.
Let me give you some advice:
Think about all of it
Carefully, so that you do not
Repent afterwards.”""")
P("VII", 768, 795, "30_swan_princess", """
[NARRATOR] The prince swore before her
That it was time for him to marry,
That he had thought over all of it
Carefully; that with a loving heart
He would walk on foot from here
For that lovely princess
Even beyond the ninth land beyond the ninth land.
The swan, sighing deeply,
Said:
[SWAN] “Why so far?
Know that your fate is near,
For that princess is I.”
[NARRATOR] Then she spread her wings,
Flew over the waves,
And from the height came down
Into the bushes on the shore,
Shook herself, and turned
Into a princess:
The moon shines under her braid,
And a star burns on her brow;
And she is stately, and glides like a peahen;
And when she speaks,
It is like a little brook murmuring.
The prince embraces the princess,
Presses her to his white breast,
And leads her quickly
To his dear mother.""")
P("VII", 796, 811, "31_blessing", """
[NARRATOR] The prince falls at her feet, begging:
[GVIDON] “My sovereign, my own mother!
I have chosen a wife for myself,
Your obedient daughter.
We both ask your permission,
Your blessing:
Bless your children
To live in counsel and love.”
[NARRATOR] Over their bowed heads
The mother, with a wonder-working icon,
Sheds tears, and says:
“God reward you, children.”
The prince did not wait long,
He married the princess;
They began to live and to be happy,
And to wait for a little one.""")
P("VII", 812, 845, "32_invite", """
[NARRATOR] The wind blows over the sea
And drives a little ship along;
It races over the waves
With its sails billowing,
Past the steep island,
Past the great town;
The cannons on the pier fire,
Telling the ship to land.
The merchants come to the gate.
Prince Gvidon invites them,
He feeds them and gives them drink,
And asks them:
[GVIDON] “What do you trade, good sirs,
And where are you sailing now?”
[NARRATOR] The sailors answered:
[SHIPMEN] “We have sailed round the whole world,
Trading, and not for nothing,
In goods that no one named;
And our way lies far:
Home, to the east,
Past the island of Buyan,
To the glorious land of Saltan.”
[NARRATOR] The prince said to them then:
[GVIDON] “A good journey, gentlemen,
Over the sea-ocean
To glorious Tsar Saltan;
And remind him,
Your sovereign:
He promised to visit us,
And has not come yet:
I send him my greetings.”
[NARRATOR] The merchants sailed; and Prince Gvidon
This time stayed at home,
And did not part from his wife.""")
P("VIII", 846, 909, "33_sailors_all", """
[NARRATOR] The wind blows gaily, the ship runs gaily,
Past the island of Buyan,
To the realm of glorious Saltan,
And the well-known land
Is seen far off at last.
The merchants came ashore.
Tsar Saltan invites them to his palace.
The guests see: in the palace
The Tsar sits in his crown,
And the weaver and the cook,
With Babarikha, their neighbour,
Sit beside the Tsar:
Between the three of them, they look
With only four eyes.
Tsar Saltan sat the guests at his table,
And asked them:
[TSAR] “Dear guests, my lords,
Have you travelled long? And where?
Is it good beyond the sea, or bad?
And what wonder is there in the world?”
[NARRATOR] The sailors answered:
[SHIPMEN] “We have sailed round the whole world;
Beyond the sea the living is good;
But here is the wonder of the world:
An island lies in the sea,
A town stands on the island,
With golden-domed churches,
With towers and gardens;
A fir grows before the palace,
And under it a crystal house;
A tame squirrel lives in it,
And what a wonder-worker she is!
The squirrel sings little songs
And cracks nuts, nothing but nuts;
And the nuts are no common nuts:
The shells are all of gold,
The kernels pure emerald;
They cherish the squirrel and guard her.
There is another wonder there:
The sea heaves up in a boiling rage,
Boils over, and begins to roar,
Rushes over the empty shore,
Spreads out in a swift run,
And on the beach there stand,
In scales, burning like fire,
Thirty-three knights,
All handsome, all brave,
Young giants, all alike, as if picked,
And with them uncle Chernomor.
And no guard is more reliable,
Nor braver, nor more careful.
And the prince has a wife,
So lovely you cannot take your eyes off her:
By day she puts out the light of God's day,
By night she lights up the earth;
The moon shines under her braid,
And a star burns on her brow.
Prince Gvidon rules that town,
Everyone praises him eagerly;
He sends you his greetings,
But he scolds you gently:
You promised to visit us,
And have not come yet.”""")
P("VIII", 910, 921, "34_decides", """
[NARRATOR] At this the Tsar could wait no longer,
And ordered a fleet made ready.
But the weaver and the cook,
With Babarikha, their neighbour,
Do not want to let the Tsar go
To visit the wonderful island.
But Saltan pays them no heed,
And at once silences them:
[TSAR] “What am I? A Tsar, or a child?”
He says, in earnest. “I am going today!”
[NARRATOR] Then he stamped his foot,
Went out, and slammed the door.""")
P("VIII", 922, 951, "35_fleet", """
[NARRATOR] Prince Gvidon sits by the window,
Looking silently at the sea:
It does not roar or splash,
It only trembles, hardly, hardly,
And in the blue distance
Ships appeared:
Over the plains of the Ocean
The fleet of Tsar Saltan sails.
Prince Gvidon then jumped up
And cried out in a loud voice:
[GVIDON] “My own dear mother!
You, young princess!
Look over there:
My father is coming here!”
[NARRATOR] The fleet is already nearing the island.
Prince Gvidon points his spyglass:
The Tsar stands on the deck
And looks at them through his glass;
With him the weaver and the cook,
With Babarikha, their neighbour;
They are amazed
At the unknown land.
All at once the cannons fired;
The bells rang in the belfries;
Gvidon himself goes to the sea;
There he meets the Tsar,
With the cook and the weaver,
With Babarikha, their neighbour;
He led the Tsar into the town,
Without saying anything.""")
P("VIII", 952, 975, "36_gates", """
[NARRATOR] Now they all go into the palace:
At the gates armour glitters,
And before the Tsar's eyes stand
Thirty-three knights,
All handsome, all young,
Young giants, all alike, as if picked,
And with them uncle Chernomor.
The Tsar stepped into the wide courtyard:
There, under a tall fir,
The squirrel sings a little song,
Cracks a golden nut,
Takes out an emerald
And drops it into a little bag;
And the big yard is sown
With golden shells.
The guests go on, in haste,
They look — and what? The princess is a wonder:
The moon shines under her braid,
A star burns on her brow;
And she is stately, and glides like a peahen,
And leads her mother-in-law.
The Tsar looks, and knows them...""")
P("VIII", 976, 995, "37_feast", """
[NARRATOR] His heart leapt up in him!
[TSAR] “What do I see? What is this?
How!”
[NARRATOR] And his breath caught.
The Tsar burst into tears,
He embraces the queen,
And his little son, and the young wife,
And they all sit down to the table,
And a merry feast began.
But the weaver and the cook,
With Babarikha, their neighbour,
Ran away to hide in the corners;
They were hardly found there.
Then they confessed everything,
Repented, and burst into tears;
The Tsar, for such a joy,
Let all three go home.
The day went by; and Tsar Saltan
Was put to bed, full of cheer.
I was there; I drank mead and beer,
And only wet my moustache.""")

# ---- build everything ------------------------------------------------------------------------------------------------------------------------
KEYS = list(NAMES)
assert [p[1] for p in PARAS[1:]] == [p[2] + 1 for p in PARAS[:-1]] and PARAS[0][1] == 0 and PARAS[-1][2] == 995
SPK = {"N": "NARRATOR"}

def pieces(text):
    out = []
    for ln in text.strip("\n").split("\n"):
        m = re.match(r"\[([A-Z0-9]+)\] ?(.*)$", ln)
        if m: out.append([SPK.get(m.group(1), m.group(1)), m.group(2)])
        else: out[-1][1] += "\n" + ln
    return out

T, S_, rows, sc_by_par, cnt = {k: [] for k in KEYS}, [], [], [], 0
ru_rows, ru_cnt = [], 1
ru_rows.append({"id": 1, "part": "I", "paragraph": 0, "speaker": "NARRATOR",
                "text": "Сказка о царе Салтане, о сыне его славном и могучем богатыре князе Гвидоне Салтановиче и о прекрасной царевне Лебеди. Александр Пушкин."})
par_in_part = {}
src_by_part = {k: [] for k in KEYS}
for part, a, b, art, text in PARAS:
    pi = par_in_part[part] = par_in_part.get(part, 0) + 1
    src_by_part[part].append("\n".join(d[a:b + 1]))
    pcs = pieces(text)
    T[part].append("\n".join(t for s, t in pcs))
    first = True
    for s, t in pcs:
        cnt += 1
        rows.append({"id": cnt, "part": part, "paragraph": pi, "speaker": s, "text": t.replace("\n", " ")})
        if first: sc_by_par.append((cnt, art)); first = False
    i = a
    while i <= b:                       # the Russian rows: runs of the same speaker, lines kept as lines
        j = i
        while j + 1 <= b and speaker_of[j + 1] == speaker_of[i]: j += 1
        ru_cnt += 1
        ru_rows.append({"id": ru_cnt, "part": part, "paragraph": pi, "speaker": speaker_of[i], "text": "\n".join(d[i:j + 1])})
        i = j + 1
for part in KEYS: S_.append({"part": part, "paragraphs": src_by_part[part], "other_blocks": []})

INTRO = ("The Tale of Tsar Saltan, of his glorious and mighty son, Prince Gvidon Saltanovich, and of the beautiful Swan Princess. A fairy tale in verse "
         "by Alexander Pushkin, written in eighteen thirty-one. Make yourself comfortable, and listen. It is a story about three sisters, a barrel on the sea, "
         "a magic town, a squirrel with golden nuts, a swan who is really a princess, and a prince who turns into a mosquito, a fly and a bumblebee.")
OUTRO = "And that is the end of the tale. Thank you for listening, and sleep well."
rows.insert(0, {"id": 0, "part": "I", "paragraph": 0, "speaker": "NARRATOR", "text": INTRO})
rows.append({"id": 0, "part": "VIII", "paragraph": len(T["VIII"]) + 1, "speaker": "NARRATOR", "text": OUTRO})
for i, r in enumerate(rows, 1): r["id"] = i
sc = []
for i, a in sc_by_par:
    i += 1                                  # the intro row shifted every id by one
    if not sc or sc[-1]["art"] != a: sc.append({"id": i, "art": a})
sc[0]["id"] = 1                             # the first picture starts with the spoken introduction

# the Russian outro is not read (the author's text ends the book); the Russian script holds the author's text only, plus the spoken title
json.dump(T, open("translation_en.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(S_, open("source_clean.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(rows, open("Tsar_Saltan_voice_script.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(ru_rows, open("Tsar_Saltan_voice_script_ru.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(sc, open("scenes.json", "w"), indent=1)
with open("Tsar_Saltan_voice_script.md", "w", encoding="utf-8") as f:
    cur = None
    for r in rows:
        if r["part"] != cur: cur = r["part"]; f.write(f"\n## {cur} · {NAMES[cur]}\n\n")
        f.write(f"**{r['speaker']}**: {r['text']}\n\n")
V = lambda v, s: {"voice": v, "speed": s, "lang": "en-gb"}
json.dump({"NARRATOR": V("bm_george", .92), "SISTER1": V("bf_lily", .97), "SISTER2": V("bf_isabella", .95), "SISTER3": V("bf_alice", .97), "TSAR": V("bm_lewis", .88),
           "GVIDON": V("bm_fable", .95), "SWAN": V("bf_emma", .9), "SHIPMEN": V("bm_daniel", .95), "COOK": V("bf_isabella", .82), "WEAVER": V("bf_alice", .85),
           "BABARIKHA": V("bf_isabella", .76), "CHERNOMOR": V("bm_lewis", .84)}, open("voices_kokoro.json", "w"), indent=1)
GV = lambda v: {"voice": v, "style": ""}
json.dump({"NARRATOR": GV("Sulafat"), "SISTER1": GV("Leda"), "SISTER2": GV("Kore"), "SISTER3": GV("Aoede"), "TSAR": GV("Algieba"), "GVIDON": GV("Puck"),
           "SWAN": GV("Vindemiatrix"), "SHIPMEN": GV("Orus"), "COOK": GV("Despina"), "WEAVER": GV("Autonoe"), "BABARIKHA": GV("Gacrux"), "CHERNOMOR": GV("Charon")},
          open("voices_gemini.json", "w"), indent=1)
w = sum(len(r["text"].split()) for r in rows)
print(len(rows), "EN rows,", w, "English words, about", round(w / 150, 1), "min at 150 wpm;", len(ru_rows), "RU rows; scenes", len(sc), "; paragraphs", sum(len(v) for v in T.values()))
print({k: sum(len(t.split()) for t in v) for k, v in T.items()})
