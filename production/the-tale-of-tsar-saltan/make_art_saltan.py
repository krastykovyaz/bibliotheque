#!/usr/bin/env python3
"""Illustrations and cover for "The Tale of Tsar Saltan" (Pushkin) as SVG: soft, bright, rounded picture-book style for children.
Characters and props: art_chars.py, art_props.py. Writes art/<name>.svg."""
from art_props import *

QUEEN = dict(robe="#ff9ec0", trim=GOLD, hair="#5a3a2a", hat="kokoshnik")
SIS = [dict(robe="#4a7ab8", trim="#9fc0e8", hair="#5a3a2a", hat=""), dict(robe="#4a9a6a", trim="#fff", hair="#3a2a2a", hat=""),
       dict(robe="#ff9ec0", trim=GOLD, hair="#7a4a2a", hat="")]
PRINCESS = dict(robe="#eaf4ff", trim="#8cc4ee", hair="#6a4a3a", hat="kokoshnik")
BOYAR = dict(coat="#5a4a7a", hat="x", beard="#6a5a5a", hatcol="#3a2a5a", pants="#3a3a4a")
NIGHT = ("#3a4a8a", "#8a9ad0")


def spinning(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><circle cx="0" cy="-70" r="62" fill="none" stroke="#b57a4a" stroke-width="12"/>'
            + "".join(f'<path d="M0 -70 L{62*math.cos(a):.0f} {-70+62*math.sin(a):.0f}" stroke="#b57a4a" stroke-width="6"/>' for a in [i * math.pi / 3 for i in range(6)])
            + f'<path d="M0 -8 L-40 60 M0 -8 L40 60" stroke="#8a5a2a" stroke-width="12" stroke-linecap="round"/></g>')


def scroll(x, y, s=1.0, rot=0):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})"><rect x="-60" y="-40" width="120" height="80" rx="10" fill="#fff6dc" stroke="#d9a020" stroke-width="5"/>'
            f'<path d="M-40 -16 H40 M-40 4 H40 M-40 24 H10" stroke="#9a7a4a" stroke-width="5"/><circle cx="46" cy="30" r="12" fill="{RED}"/></g>')


def bubble(x, y, r, inner):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" opacity=".9" stroke="#d9c8a0" stroke-width="6"/><circle cx="{x+r*.8:.0f}" cy="{y+r*1.05:.0f}" r="{r*.14:.0f}" fill="#fff" opacity=".9"/>' + inner


def evening_room(r, night=True):
    b = room("#ffe2c0", "#c98a5a") + window(560, 100, 480, 400, "#3a4a8a" if night else "#bfe6ff") + stars(r, 10, 480).replace('y="0"', '') if False else room("#ffe2c0", "#c98a5a") + window(560, 100, 480, 400, "#3a4a8a")
    b += "".join(f'<circle cx="{r.randint(580, 1020)}" cy="{r.randint(120, 480)}" r="{r.uniform(2, 5):.1f}" fill="#fff6c8"/>' for _ in range(16))
    b += f'<rect x="540" y="490" width="520" height="30" rx="10" fill="#b57a4a"/>'
    b += f'<rect x="80" y="620" width="140" height="40" rx="12" fill="#b57a4a"/><rect x="140" y="480" width="26" height="140" rx="8" fill="#e8d8a8"/><ellipse cx="153" cy="462" rx="22" ry="38" fill="{GOLD}"/><circle cx="153" cy="456" r="130" fill="{GOLD}" opacity=".14"/>'
    return b


def s1():   # three sisters spin by the window and dream
    r = R(1); b = evening_room(r)
    for i, x in enumerate((360, 800, 1240)):
        b += spinning(x + (90 if i != 1 else 100), 860, .95) + lady(x, 870, 1.28, mood="smile", lh=(-70, -60), rh=(60, -130 if i == 2 else -60), **SIS[i])
    b += sparkles(r, 12, 300, 1400, 120, 540, "#ffe27a")
    return svg(b, "#ffe2c0", "#ffe2c0")


def s2():   # the tsar listens behind the door and likes what the third sister says
    r = R(2); b = evening_room(r)
    b += f'<rect x="1260" y="180" width="260" height="520" rx="20" fill="#8a5a3a" stroke="#6a3a1a" stroke-width="10"/><circle cx="1290" cy="450" r="14" fill="{GOLD}"/>'
    b += f'<path d="M1260 180 L1130 150 L1130 740 L1260 700 Z" fill="#fff6c8" opacity=".5"/>'
    b += tsar(1340, 760, .95, "smile", lh=(-60, -60), rh=(40, -90)) + f'<rect x="1160" y="740" width="420" height="160" fill="#c98a5a"/>'
    for i, x in enumerate((220, 560, 900)):
        b += spinning(x + 90, 880, .85) + lady(x, 880, 1.18, mood="smile", lh=(-70, -60), rh=(60, -60), **SIS[i])
    return svg(b, "#ffe2c0", "#ffe2c0")


def s3():   # the wedding feast; the weaver and the cook are cross in the corners
    r = R(3); b = throne_room(r)
    b += f'<rect x="300" y="560" width="1000" height="60" rx="18" fill="#fff"/><rect x="340" y="620" width="30" height="180" fill="#b57a4a"/><rect x="1230" y="620" width="30" height="180" fill="#b57a4a"/>'
    b += "".join(f'<circle cx="{x}" cy="548" r="26" fill="{c}"/>' for x, c in ((420, "#ffd54a"), (560, "#e0564a"), (1040, "#6cbf72"), (1180, "#ffd54a")))
    b += tsar(660, 600, 1.0, "smile") + lady(940, 600, 1.0, mood="smile", lh=(-60, -60), rh=(60, -60), **QUEEN)
    b += f'<rect x="20" y="640" width="260" height="30" fill="#b57a4a"/>' + lady(120, 880, .95, mood="sulk", **SIS[0]) + spinning(250, 880, .8)
    b += f'<g transform="translate(1360 860)"><ellipse cx="0" cy="-50" rx="70" ry="42" fill="#5a5a6a"/><rect x="-80" y="-96" width="160" height="16" rx="8" fill="#3a3a4a"/></g>' + lady(1470, 880, .95, mood="sulk", **SIS[1])
    return svg(b + sparkles(r, 20, 300, 1300, 60, 520, "#fff6c8"), "#f6e0b8", "#f6e0b8")


def s4():   # the tsar rides to war; the queen waves, later with the baby
    r = R(4); b = f'<circle cx="1300" cy="200" r="120" fill="#fff3b0"/>' + hills("#b2e29e", "#9ad088") + meadow(660) + flowers(r, 50, 700, 890)
    b += f'<rect x="60" y="300" width="360" height="400" fill="#fff0d8" stroke="#e0c8a0" stroke-width="6"/><path d="M60 300 L240 190 L420 300 Z" fill="#c0392b"/><rect x="180" y="500" width="120" height="200" rx="60" fill="#8a5a3a"/>'
    b += horse(1060, 820, 1.0, 1, rider=man(0, -128, .85, "#c0392b", "x", "#cfcfd8", "smile", hatcol="#c0392b", pants="#5a2a3a", lh=(-60, -60), rh=(50, -90)).replace('<ellipse cx="0" cy="6"', '<ellipse style="display:none" cx="0" cy="6"', 1), gallop=True)
    b += f'<g transform="translate(1040 540) scale(.85)">{crown(0, 0, 46, "crown")}</g>'
    b += lady(560, 870, 1.25, mood="smile", lh=(-60, -60), rh=(80, -160), **QUEEN)
    b += f'<g transform="translate(440 650)"><ellipse cx="0" cy="0" rx="48" ry="36" fill="#fff"/><circle cx="-10" cy="-22" r="26" fill="{SKIN}"/>' + face(-10, -20, 26, "smile") + '</g>'
    b += "".join(f'<path d="M{x} {y} q14 -16 28 0 q14 -16 28 0" stroke="#7a7a8a" stroke-width="5" fill="none" stroke-linecap="round"/>' for x, y in ((700, 180), (820, 130), (940, 210)))
    return svg(b, "#ffe0b8", "#f2fbe6")


def s5():   # the three plot together over a letter
    r = R(5); b = room("#f0e4d8", "#a98060") + f'<rect width="1600" height="900" fill="#3a2a5a" opacity=".25"/>' + window(1160, 90, 300, 300, "#2c3a78") + f'<circle cx="1330" cy="230" r="46" fill="#fff0a8"/>'
    b += f'<rect x="420" y="560" width="760" height="40" rx="14" fill="#8a5a2a"/><rect x="460" y="600" width="30" height="200" fill="#6a3a1a"/><rect x="1110" y="600" width="30" height="200" fill="#6a3a1a"/>'
    b += scroll(800, 540, 1.3, -4) + f'<path d="M870 470 Q930 380 980 330" stroke="#fff" stroke-width="10" fill="none" stroke-linecap="round"/><path d="M980 330 L1010 300 L960 320 Z" fill="#fff"/>'
    b += f'<circle cx="800" cy="500" r="260" fill="{GOLD}" opacity=".13"/>' + trio(800, 880, 1.15, "sulk")
    b += man(210, 880, .95, "#4a7ab8", "cap", "#7a4a2a", "smile", hatcol="#c0392b", lh=(-60, -50), rh=(60, -50))
    return svg(b, "#f0e4d8", "#f0e4d8")


def s6():   # the tsar reads the letter, the messenger waits
    r = R(6); b = throne_room(r) + throne(800, 700, 1.1) + tsar(800, 730, 1.0, "sulk", lh=(-70, -40), rh=(60, -80), hold=scroll(60, -90, .7).replace('translate(60 -90)', 'translate(60 -90)'))
    b += man(340, 880, 1.0, "#4a7ab8", "cap", "#7a4a2a", "smile", hatcol="#c0392b", lh=(-60, -50), rh=(60, -50)) + lady(1280, 880, 1.2, mood="smile", robe="#7a5ad8", trim=GOLD, hair="#2a2a3a", hat="").replace("", "")
    return svg(b, "#f6e0b8", "#f6e0b8")


def s7():   # the messenger sleeps at the inn while the letter is swapped
    r = R(7); b = room("#f0e4d8", "#a98060") + f'<rect width="1600" height="900" fill="#2a2a5a" opacity=".25"/>' + window(110, 90, 300, 300, "#2c3a78") + f'<circle cx="260" cy="230" r="46" fill="#fff0a8"/>'
    b += f'<rect x="420" y="600" width="800" height="40" rx="14" fill="#8a5a2a"/><rect x="460" y="640" width="30" height="200" fill="#6a3a1a"/><rect x="1150" y="640" width="30" height="200" fill="#6a3a1a"/>'
    b += f'<g transform="translate(640 700) rotate(-90) scale(.8)">{NOHAD(man(0, 0, 1, "#4a7ab8", "cap", "#7a4a2a", "sleep", hatcol="#c0392b"))}</g>'
    b += f'<ellipse cx="560" cy="580" rx="46" ry="40" fill="#c98a52"/><rect x="528" y="526" width="64" height="16" rx="8" fill="#8a5a2a"/>'
    b += scroll(900, 590, 1.0, 6) + trio(1000, 890, 1.0, "smile")
    b += f'<text x="520" y="440" font-family="Georgia, serif" font-size="70" fill="#8a7ab8" opacity=".8">z z z</text>'
    return svg(b, "#f0e4d8", "#f0e4d8")


def s8():   # the boyars put the queen and the little prince into a barrel at the shore
    r = R(8); b = f'<circle cx="1300" cy="200" r="110" fill="#fff0c0" opacity=".9"/>' + sea(520, "#7fc0ea", "#5aa0dc", r)
    b += f'<path d="M0 640 Q500 600 900 650 T1600 640 V900 H0 Z" fill="#f2dcaa"/><path d="M0 760 Q600 720 1100 770 T1600 760 V900 H0 Z" fill="#e8cc90"/>'
    b += barrel(900, 800, 1.0, 0) + f'<path d="M960 720 q30 -30 60 0" stroke="#fff" stroke-width="6" fill="none"/>'
    for i, x in enumerate((260, 420, 1250, 1400)):
        b += man(x, 860, .95, "#5a4a7a", "x", "#6a5a5a", "sulk", hatcol="#3a2a5a", pants="#3a3a4a", lh=(-60, -50), rh=(60, -50), flip=1 if x < 800 else -1)
    return svg(b, "#ffd8c0", "#ffd8c0")


def s9():   # night on the sea: the barrel, the stars, the kind wave
    r = R(9); b = stars(r, 60, 420) + f'<circle cx="260" cy="170" r="90" fill="#fff0a8"/><circle cx="310" cy="146" r="80" fill="#2c3a78"/>' + sea(520, "#3a5aa8", "#2c4a98", r)
    b += f'<path d="M900 560 Q980 420 1120 480 Q1180 540 1060 600 Q1000 620 900 560 Z" fill="#8cc4ee" opacity=".9"/><circle cx="1050" cy="520" r="6" fill="#fff"/><path d="M0 0" />'
    b += face(1040, 546, 62, "smile") + barrel(640, 740, .85, -6) + f'<circle cx="640" cy="620" r="150" fill="{GOLD}" opacity=".13"/>'
    b += f'<path d="M1180 600 Q1300 520 1420 560 L1600 640 V700 H1180 Z" fill="#f2dcaa"/>' + sparkles(r, 10, 400, 900, 400, 640, "#fff")
    return svg(b, "#2c3a78", "#8a9ad0")


def s10():  # the prince has grown: he stands on the island by the old oak and makes a bow
    r = R(10); b = f'<circle cx="1300" cy="160" r="90" fill="#fff3b0"/>' + sea(600, "#7fc0ea", "#5aa0dc", r)
    b += f'<path d="M100 700 Q500 440 900 480 Q1300 460 1500 700 V900 H100 Z" fill="#8fd47c"/>' + oak_big(780, 600, 1.2) + flowers(r, 30, 700, 880)
    b += f'<g transform="translate(300 780) rotate(80) scale(.7)">{barrel(0, 0, 1, 0, False)}</g>' + lady(210, 870, 1.15, mood="smile", lh=(-60, -60), rh=(60, -50), **QUEEN).replace("kokoshnik", "")
    b += man(1080, 860, 1.25, "#2a6ab8", "prince", None, "smile", hatcol="#c0392b", pants="#2a3a6a", lh=(-70, -60), rh=(110, -120), hold=f'<path d="M130 -190 Q190 -110 130 -20" stroke="#8a5a2a" stroke-width="12" fill="none" stroke-linecap="round"/><path d="M130 -190 L130 -20" stroke="#fff" stroke-width="3"/>')
    return svg(b, "#bfe9ff", "#f2fbe6")


def s11():  # the swan fights the kite, the prince's arrow flies
    r = R(11); b = f'<circle cx="260" cy="160" r="90" fill="#fff3b0"/>' + sea(520, "#7fc0ea", "#5aa0dc", r) + f'<path d="M0 700 Q300 640 560 700 V900 H0 Z" fill="#8fd47c"/>'
    b += man(180, 860, 1.1, "#2a6ab8", "prince", None, "smile", hatcol="#c0392b", pants="#2a3a6a", lh=(-70, -60), rh=(110, -120)) + f'<path d="M330 640 Q760 300 1060 330" stroke="#fff" stroke-width="5" stroke-dasharray="10 10" fill="none"/><path d="M1060 330 l-26 -4 l12 22 Z" fill="{BROWN}"/>'
    b += swan(1000, 760, 1.2, -1, "smile", wings=True) + kite(1100, 300, 1.0, -1) + f'<path d="M1180 360 q16 24 0 48" stroke="#8cc4ee" stroke-width="6" fill="none" opacity=".0"/>'
    return svg(b, "#bfe9ff", "#f2fbe6")


def s12():  # a golden-domed town appears at dawn, bells ring
    r = R(12); b = f'<circle cx="800" cy="520" r="360" fill="#fff0a8" opacity=".45"/>' + sea(640, "#9ad0f0", "#7ab8e4", r) + f'<path d="M100 760 Q800 600 1500 760 V900 H100 Z" fill="#8fd47c"/>'
    b += town(800, 780, .95) + sparkles(r, 24, 200, 1400, 40, 500, "#fff6c8")
    b += lady(240, 880, 1.0, mood="open", lh=(-70, -60), rh=(60, -120), **QUEEN).replace("kokoshnik", "") + man(430, 880, 1.0, "#2a6ab8", "prince", None, "open", hatcol="#c0392b", pants="#2a3a6a", lh=(-70, -60), rh=(80, -140))
    b += "".join(f'<g transform="translate({x} 880)">{man(0, 0, .5, c, "cap", "#7a4a2a", "smile", hatcol=h)}</g>' for x, c, h in ((1130, "#c0392b", "#4a7ab8"), (1210, "#3a9a6a", "#e0a020"), (1290, "#8e5ac8", "#c0392b"), (1370, "#e08a2a", "#2a8aa0")))
    return svg(b, "#ffe8c0", "#fff6e6")


def harbor(seed, cargo_col="#c98a52", leaving=False, horses=False, swords=False, bee=None):
    r = R(seed); b = f'<circle cx="1360" cy="150" r="90" fill="#fff3b0"/>' + sea(520, "#7fc0ea", "#5aa0dc", r)
    b += f'<path d="M0 560 Q200 500 500 560 V900 H0 Z" fill="#8fd47c"/>' + town(180, 580, .5) + f'<rect x="300" y="720" width="460" height="40" rx="12" fill="#b57a4a"/><rect x="330" y="760" width="20" height="140" fill="#8a5a2a"/><rect x="700" y="760" width="20" height="140" fill="#8a5a2a"/>'
    b += ship(1100 if not leaving else 1180, 700, 1.1, 1 if not leaving else -1, cargo=not horses and not swords)
    if horses: b += "".join(f'<g transform="translate({1000+i*90} 620) scale(.55)">{horse(0, 0, 1, 1, col=["#fafafa", "#8a5a3a", "#d8c8a8"][i])}</g>' for i in range(3))
    if swords: b += "".join(f'<path d="M{1020+i*34} 640 V540" stroke="#cfd8e8" stroke-width="10" stroke-linecap="round"/><rect x="{1008+i*34}" y="640" width="26" height="10" fill="{GOLD}"/>' for i in range(5))
    b += man(560, 740, 1.05, "#2a6ab8", "prince", None, "smile", hatcol="#c0392b", pants="#2a3a6a", lh=(-70, -60), rh=(90, -150))
    b += "".join(f'<circle cx="{x}" cy="{y}" r="{k}" fill="#fff" opacity=".8"/>' for x, y, k in ((850, 650, 26), (880, 620, 34), (920, 600, 24)))
    if bee: b += insect(1180, 340, 1.4, bee, -1)
    return svg(b, "#bfe9ff", "#f2fbe6")


def s13(): return harbor(13)
def s14():  # the swan splashes the prince: he becomes a tiny mosquito and flies after the ship
    r = R(14); b = f'<circle cx="1360" cy="160" r="90" fill="#fff3b0"/>' + sea(520, "#7fc0ea", "#5aa0dc", r) + f'<path d="M0 700 Q400 640 800 700 V900 H0 Z" fill="#8fd47c"/>'
    b += swan(420, 760, 1.25, 1, "smile", wings=True) + "".join(f'<circle cx="{r.randint(300,620)}" cy="{r.randint(300,540)}" r="{r.randint(5,10)}" fill="#bfe6ff" stroke="#fff" stroke-width="3"/>' for _ in range(22))
    b += man(900, 860, 1.1, "#2a6ab8", "prince", None, "open", hatcol="#c0392b", pants="#2a3a6a", lh=(-70, -60), rh=(90, -130))
    b += insect(980, 380, 1.8, "mosquito", 1) + ship(1380, 560, .4, -1) + f'<path d="M1040 420 Q1180 360 1260 440" stroke="#fff" stroke-width="6" stroke-dasharray="4 12" fill="none" stroke-linecap="round"/>'
    return svg(b, "#bfe9ff", "#f2fbe6")


def palace(seed, kind=None, mode="sad", bub=None):
    r = R(seed); b = throne_room(r) + throne(800, 700, 1.1)
    if mode == "bite":
        b += tsar(800, 730, 1.0, "open", lh=(-70, -100), rh=(60, -110)) + trio(380, 890, 1.0, "open") + insect(1360, 300, 1.7, kind or "mosquito", -1)
        b += f'<path d="M1260 340 Q1180 420 1040 520" stroke="#fff" stroke-width="6" stroke-dasharray="4 12" fill="none" stroke-linecap="round"/>' + f'<text x="170" y="520" font-family="Georgia, serif" font-size="80" fill="#e0564a" opacity=".85">!</text>'
        b += window(1180, 140, 300, 300, "#bfe6ff") + insect(1330, 300, 1.4, kind or "mosquito", -1)
    else:
        b += tsar(800, 730, 1.0, "sulk" if mode == "sad" else "smile") + trio(1250, 890, .95, "sulk")
        if kind: b += insect(260, 260, 1.4, kind, 1)
        if mode == "tell":
            b += "".join(f'<g transform="translate({220+i*130} 880)">{man(0, 0, .85, c, "cap", "#7a4a2a", "smile", hatcol=h, lh=(-60, -50), rh=(60, -80))}</g>' for i, (c, h) in enumerate((("#4a7ab8", "#c0392b"), ("#3a9a6a", "#e0a020"), ("#8e5ac8", "#c0392b"))))
    if bub: b += bubble(560, 250, 150, bub)
    return svg(b, "#f6e0b8", "#f6e0b8")


def s15(): return palace(15, "mosquito", "sad")
def s16(): return palace(16, None, "tell", bubble(0, 0, 0, f'<g transform="translate(560 310) scale(.75)">{town(0, 0, .5)}</g>'))
def s17(): return palace(17, "mosquito", "bite")


def shore_swan(seed, dusk=False, star=False, kneel=False):
    r = R(seed); b = (stars(r, 40, 300) + f'<circle cx="1300" cy="150" r="80" fill="#fff0a8"/><circle cx="1350" cy="130" r="70" fill="#5a4a8a"/>' if dusk else f'<circle cx="1360" cy="150" r="90" fill="#fff3b0"/>')
    b += sea(520, "#5a70b8" if dusk else "#7fc0ea", "#3a50a0" if dusk else "#5aa0dc", r) + f'<path d="M0 700 Q400 640 800 700 V900 H0 Z" fill="{"#5a9a7a" if dusk else "#8fd47c"}"/>'
    b += f'<ellipse cx="260" cy="840" rx="120" ry="60" fill="#a8a8b8"/>' + man(260, 780, 1.1, "#2a6ab8", "prince", None, "sulk" if not kneel else "smile", hatcol="#c0392b", pants="#2a3a6a", lh=(-60, -50), rh=(60, -50))
    b += swan(1000, 700, 1.3, -1, "smile", star=star, wings=False) + sparkles(r, 10, 700, 1400, 420, 700, "#fff")
    return svg(b, NIGHT[0] if dusk else "#bfe9ff", NIGHT[1] if dusk else "#f2fbe6")


def s18(): return shore_swan(18)


def s19():  # the squirrel with golden nuts
    r = R(19); b = f'<circle cx="1360" cy="150" r="90" fill="#fff3b0"/>' + hills("#b2e29e", "#9ad088") + meadow(680) + flowers(r, 50, 720, 890)
    b += fpine(520, 760, 700, "#3f9a6a") + crystal_house(520, 840, 1.3) + squirrel(520, 600, 1.0, 1) + f'<circle cx="540" cy="520" r="140" fill="{GOLD}" opacity=".14"/>'
    b += "".join(f'<ellipse cx="{x}" cy="{y}" rx="26" ry="18" fill="#ffd54a" stroke="#d9a020" stroke-width="4"/>' for x, y in ((700, 860), (740, 840), (780, 870), (730, 810), (820, 850), (860, 828)))
    b += "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="#5fd08a"/>' for x, y in ((960, 870), (990, 850), (1020, 874)))
    b += man(1180, 880, 1.1, "#2a6ab8", "prince", None, "smile", hatcol="#c0392b", pants="#2a3a6a", lh=(-70, -60), rh=(80, -110)) + man(1400, 880, .9, "#6a5a8a", "cap", "#3a2a2a", "smile", hatcol="#3a2a5a", lh=(-60, -50), rh=(70, -60))
    return svg(b, "#bfe9ff", "#f2fbe6")


def s20(): return harbor(20, horses=True)
def s21(): return palace(21, "fly", "sad")
def s22(): return palace(22, None, "tell", bubble(0, 0, 0, f'<g transform="translate(560 330) scale(.6)">{squirrel(0, 0, 1)}</g>'))
def s23(): return palace(23, "fly", "bite")
def s24(): return shore_swan(24, dusk=True)


def s25():  # thirty-three knights rise out of the sea
    r = R(25); b = f'<circle cx="260" cy="150" r="90" fill="#fff3b0"/>' + sea(480, "#7fc0ea", "#5aa0dc", r) + f'<path d="M0 760 Q600 700 1100 760 T1600 740 V900 H0 Z" fill="#f2dcaa"/>'
    b += f'<path d="M1200 700 Q1450 560 1600 640 V900 H1200 Z" fill="#8fd47c"/>' + town(1420, 700, .5)
    b += f'<path d="M0 560 Q200 460 400 560 T800 560 T1200 560 V620 H0 Z" fill="#fff" opacity=".7"/>'
    b += man(640, 880, 1.2, "#9ad8c8", "prince", "#cfcfd8", "smile", hatcol="#ffd54a", pants="#4a7ab8", lh=(-70, -60), rh=(70, -60))
    b += hero33(120, 800, 90, .62, 6) + hero33(820, 760, 82, .6, 7).replace("x", "x") + f'<path d="M0 780 H1600" stroke="#fff" stroke-width="0"/>'
    return svg(b + sparkles(r, 24, 0, 1600, 440, 800, "#fff"), "#bfe9ff", "#f2fbe6")


def s26(): return harbor(26, swords=True, bee="bumblebee")
def s27(): return palace(27, "bumblebee", "sad")
def s28(): return palace(28, "bumblebee", "bite")


def s29():  # the prince asks the swan about the lovely princess
    return shore_swan(29, star=True, kneel=True)


def s30():  # the swan becomes the princess with the moon under her braid and a star on her forehead
    r = R(30); b = stars(r, 40, 380) + f'<circle cx="1280" cy="150" r="80" fill="#fff0a8"/><circle cx="1330" cy="130" r="70" fill="#5a4a8a"/>' + sea(560, "#5a70b8", "#3a50a0", r)
    b += f'<path d="M0 720 Q500 640 1000 720 T1600 700 V900 H0 Z" fill="#5a9a7a"/>' + "".join(f'<ellipse cx="{x}" cy="{y}" rx="16" ry="30" fill="#fff" opacity=".9" transform="rotate({a} {x} {y})"/>' for x, y, a in ((600, 420, -30), (640, 360, 20), (720, 300, 40), (900, 320, -40), (950, 400, 30), (560, 520, -50), (990, 520, 50)))
    b += lady(780, 860, 1.55, mood="smile", lh=(-60, -60), rh=(60, -60), **PRINCESS) + f'<path d="M754 456 l6 -20 l6 20 l20 6 l-20 6 l-6 20 l-6 -20 l-20 -6 Z" fill="{GOLD}"/>'
    b += f'<g transform="translate(870 760)"><circle r="26" fill="#fff0a8"/><circle cx="12" cy="-4" r="22" fill="#5a70b8"/></g>'
    b += man(340, 870, 1.15, "#2a6ab8", "prince", None, "open", hatcol="#c0392b", pants="#2a3a6a", lh=(-70, -60), rh=(70, -100)) + sparkles(r, 34, 400, 1200, 160, 800, "#fff6c8")
    return svg(b, "#2c3a78", "#8a9ad0")


def s31():  # the queen mother blesses the young couple with the holy icon
    r = R(31); b = throne_room(r, "#f6e0b8", "#7a5ad8")
    b += f'<g transform="translate(800 330)"><rect x="-70" y="-90" width="140" height="190" rx="70" fill="{GOLD}" stroke="#d9a020" stroke-width="8"/><circle cx="0" cy="-10" r="44" fill="#fff0c8"/><circle cx="0" cy="-16" r="18" fill="{SKIN}"/><circle cx="0" cy="-10" r="62" fill="{GOLD}" opacity=".12"/></g>'
    b += lady(800, 880, 1.45, mood="smile", lh=(-80, -120), rh=(80, -120), **QUEEN).replace("kokoshnik", "kokoshnik")
    b += f'<g transform="translate(420 880)">{man(0, 0, 1.05, "#2a6ab8", "prince", None, "smile", hatcol="#c0392b", pants="#2a3a6a", lh=(-60, -40), rh=(60, -40))}</g>' + lady(1180, 880, 1.2, mood="smile", lh=(-60, -50), rh=(60, -50), **PRINCESS)
    return svg(b + sparkles(r, 20, 300, 1300, 100, 500, "#fff6c8"), "#f6e0b8", "#f6e0b8")


def s32(): return harbor(32, leaving=True)


def s33(): return palace(33, None, "tell", bubble(0, 0, 0, f'<g transform="translate(450 300) scale(.5)">{squirrel(0, 0, 1)}</g><g transform="translate(560 330) scale(.5)">{town(0, 0, .4)}</g>'))


def s34():  # the tsar stamps and slams the door
    r = R(34); b = throne_room(r) + f'<rect x="1260" y="200" width="240" height="500" rx="20" fill="#8a5a3a" stroke="#6a3a1a" stroke-width="10"/>'
    b += tsar(900, 880, 1.15, "open", lh=(-90, -150), rh=(80, -140)) + trio(380, 890, .95, "open")
    b += f'<path d="M1180 780 l40 -30 M1160 820 l50 0 M1190 860 l36 30" stroke="{GOLD}" stroke-width="8" stroke-linecap="round"/>'
    return svg(b, "#f6e0b8", "#f6e0b8")


def s35():  # the fleet of the tsar sails over the calm sea; the prince looks through a spyglass
    r = R(35); b = f'<circle cx="1280" cy="150" r="100" fill="#fff3b0"/>' + sea(500, "#7fc0ea", "#5aa0dc", r)
    b += "".join(ship(x, y, s, -1) for x, y, s in ((1000, 640, .6), (1280, 620, .5), (760, 700, .75), (1450, 700, .55), (480, 790, .9)))
    b += f'<path d="M0 560 Q260 480 520 560 V900 H0 Z" fill="#8fd47c"/>' + town(150, 640, .45)
    b += man(180, 900, 1.15, "#2a6ab8", "prince", None, "open", hatcol="#c0392b", pants="#2a3a6a", lh=(-70, -60), rh=(110, -190), hold=f'<rect x="100" y="-280" width="120" height="26" rx="10" fill="{GOLD}" transform="rotate(-22 100 -280)"/>')
    return svg(b, "#bfe9ff", "#f2fbe6")


def s36():  # the tsar sees the gates, the knights, the squirrel and the princess
    r = R(36); b = f'<circle cx="1360" cy="150" r="90" fill="#fff3b0"/>' + hills("#b2e29e", "#9ad088") + meadow(680) + town(800, 650, .8) + f'<path d="M0 700 Q800 660 1600 700 V900 H0 Z" fill="#8fd47c"/>'
    b += hero33(60, 800, 78, .55, 5) + hero33(1050, 800, 78, .55, 5, -1) + squirrel(1450, 600, .45, -1) + fpine(1500, 700, 360)
    b += tsar(560, 890, 1.05, "open", lh=(-70, -90), rh=(70, -90)) + lady(840, 890, 1.3, mood="smile", lh=(-60, -50), rh=(60, -50), **PRINCESS) + lady(1010, 890, 1.1, mood="smile", lh=(-60, -50), rh=(60, -50), **QUEEN).replace("kokoshnik", "kokoshnik")
    return svg(b, "#bfe9ff", "#f2fbe6")


def s37():  # the happy feast; the three women hide in the corners
    r = R(37); b = throne_room(r)
    b += f'<rect x="200" y="560" width="1200" height="60" rx="18" fill="#fff"/><rect x="250" y="620" width="30" height="180" fill="#b57a4a"/><rect x="1320" y="620" width="30" height="180" fill="#b57a4a"/>'
    b += "".join(f'<circle cx="{x}" cy="546" r="26" fill="{c}"/>' for x, c in ((300, "#ffd54a"), (440, "#e0564a"), (1160, "#6cbf72"), (1300, "#ffd54a")))
    b += tsar(520, 600, 1.0, "smile", lh=(-60, -80), rh=(70, -120)) + lady(720, 600, .95, mood="smile", lh=(-60, -60), rh=(60, -60), **PRINCESS) + man(930, 600, 1.0, "#2a6ab8", "prince", None, "smile", hatcol="#c0392b", pants="#2a3a6a", lh=(-60, -60), rh=(70, -110)) + lady(1130, 600, .95, mood="smile", lh=(-60, -60), rh=(60, -60), **QUEEN)
    b += lady(90, 890, .8, mood="sulk", **SIS[0]) + lady(1500, 890, .8, mood="sulk", **SIS[1]) + sparkles(r, 40, 100, 1500, 60, 520, "#fff6c8")
    return svg(b, "#f6e0b8", "#f6e0b8")


def cover(ru=False):
    r = R(99); b = stars(r, 90, 1600).replace("", "")
    b = sparkles(r, 80, 0, 3000, 40, 1400, "#fff6c8")
    b += f'<circle cx="2420" cy="1420" r="250" fill="#fff0a8" opacity=".3"/><circle cx="2420" cy="1420" r="160" fill="#fff0a8"/><circle cx="2500" cy="1380" r="140" fill="#3a4a8a"/>'
    b += f'<path d="M0 2300 Q600 2150 1200 2260 T3000 2200 V3000 H0 Z" fill="#6a8ad0"/><path d="M0 2600 Q900 2480 1700 2620 T3000 2560 V3000 H0 Z" fill="#4a6ab8"/>'
    b += f'<g transform="translate(1500 2420) scale(1.7)">{town(0, 0, 1.0)}</g>'
    b += f'<g transform="translate(560 2880) scale(3.0)">{swan(0, 0, 1.0, 1, "smile", star=True)}</g>'
    b += f'<g transform="translate(2480 2740) scale(2.0)">{ship(0, 0, 1.0, -1)}</g>'
    b += f'<g transform="translate(2000 2960) scale(3.0)">{squirrel(0, 0, 1.0, -1)}</g>'
    T = ("АЛЕКСАНДР ПУШКИН", ["Сказка", "о царе Салтане"]) if ru else ("ALEXANDER PUSHKIN", ["The Tale of", "Tsar Saltan"])
    fs = 240 if ru else 250
    b += f'<text x="1500" y="330" text-anchor="middle" font-family="Georgia, serif" font-size="100" letter-spacing="30" fill="#fff6c8">{T[0]}</text>'
    b += "".join(f'<text x="1500" y="{680 + i*290}" text-anchor="middle" font-family="Georgia, serif" font-weight="bold" font-size="{fs}" fill="#fff">{t}</text>' for i, t in enumerate(T[1]))
    b += f'<rect x="1200" y="1300" width="600" height="10" rx="5" fill="{GOLD}"/>'
    return svg(b, "#2c3a78", "#8a9ad8", 3000, 3000)


FILES = {"1_sisters": s1, "2_tsar_door": s2, "3_wedding": s3, "4_farewell": s4, "5_plot": s5, "6_letter": s6, "7_swap": s7, "8_barrel_launch": s8,
         "9_wave": s9, "10_oak": s10, "11_swan_kite": s11, "12_city": s12, "13_harbor": s13, "14_mosquito": s14, "15_palace": s15, "16_sailors": s16,
         "17_cook_bite": s17, "18_swan_sea": s18, "19_squirrel": s19, "20_horses_ship": s20, "21_fly_palace": s21, "22_sailors2": s22, "23_weaver_fly": s23,
         "24_swan_dusk": s24, "25_knights_sea": s25, "26_ship3": s26, "27_bee_palace": s27, "28_babarikha": s28, "29_swan_bride": s29, "30_swan_princess": s30,
         "31_blessing": s31, "32_invite": s32, "33_sailors_all": s33, "34_decides": s34, "35_fleet": s35, "36_gates": s36, "37_feast": s37,
         "cover": cover, "cover_ru": lambda: cover(True)}
if __name__ == "__main__":
    import sys
    for n, fn in FILES.items():
        if len(sys.argv) > 1 and n not in sys.argv[1:]: continue
        open(f"{OUT}/{n}.svg", "w", encoding="utf-8").write(fn()); print("wrote", n)
