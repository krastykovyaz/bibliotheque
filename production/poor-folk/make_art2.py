#!/usr/bin/env python3
"""More illustrations for "Poor Folk" (a video of almost six hours needs a new picture every few minutes).
Same palette as make_art.py: St Petersburg dusk, mustard window light, brick, paper, one red geranium."""
import random, math, os
from make_art import *

OUT = "art"; os.makedirs(OUT, exist_ok=True)
WOOD, DWOOD = "#5a3a2c", "#3a2420"


def R(seed): return random.Random(seed)


def table(y=640, x0=200, x1=1400, col=WOOD):
    return f'<rect x="{x0}" y="{y}" width="{x1-x0}" height="28" fill="{col}"/><rect x="{x0+40}" y="{y+28}" width="22" height="{900-y-28}" fill="{DWOOD}"/><rect x="{x1-62}" y="{y+28}" width="22" height="{900-y-28}" fill="{DWOOD}"/>'


def glow(x, y, r=300, a=.2): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{GOLD}" opacity="{a*.6}"/><circle cx="{x}" cy="{y}" r="{r*.5}" fill="{GOLD}" opacity="{a}"/>'


def candle(x, y, h=90):
    return f'<rect x="{x-11}" y="{y-h}" width="22" height="{h}" fill="{PAPER}"/><path d="M{x} {y-h-34} q-14 22 0 32 q14 -10 0 -32" fill="{GOLD}"/>'


def paper(x, y, w=170, h=22, tilt=0): return f'<g transform="rotate({tilt} {x} {y})"><rect x="{x-w/2}" y="{y-h}" width="{w}" height="{h}" fill="{PAPER}"/><rect x="{x-w/2+10}" y="{y-h+6}" width="{w-20}" height="3" fill="#b9a98a"/><rect x="{x-w/2+10}" y="{y-h+13}" width="{w-50}" height="3" fill="#b9a98a"/></g>'


def book(x, y, w=150, h=36, col="#6a3a32"): return f'<rect x="{x}" y="{y-h}" width="{w}" height="{h}" fill="{col}"/><rect x="{x+6}" y="{y-h+6}" width="{w-12}" height="6" fill="{GOLD}" opacity=".6"/>'


def wall(c1="#2a2433", c2="#3a3040", floor="#201c26", fy=640):
    d, b = sky(c1, c2); return d, b + f'<rect y="{fy}" width="1600" height="{900-fy}" fill="{floor}"/>'


def street(seed, top, bottom, lampy=True, rain=False, snow=False, people=3, leaves=False, left="#3c3448", right="#4a3a44", sun=None):
    r = R(seed); d, b = sky(top, bottom)
    if sun: b += f'<circle cx="{sun[0]}" cy="{sun[1]}" r="{sun[2]}" fill="#fff0c0" opacity=".85"/>'
    b += building(0, 520, 240 + r.randint(0, 80), left, 0, (), 4) + building(1080, 520, 200 + r.randint(0, 100), right, 0, (), 4)
    b += f'<rect y="700" width="1600" height="200" fill="#2a2630"/><path d="M0 720 H1600" stroke="#3a3440" stroke-width="3"/>'
    b += '<path d="M520 900 L1080 900 L930 520 L690 520 Z" fill="#363040" opacity=".7"/>'
    if lampy:
        for x in (560, 1040): b += lamp(x, 480, 230)
    for i in range(people): b += person(r.randint(600, 1000), 760 + r.randint(0, 100), .5 + .35 * (i / 3), "#14121c", bundle=i == 0)
    if rain: b += "".join(f'<path d="M{x} {y} l-8 36" stroke="#c9d4ea" stroke-width="2" opacity=".35"/>' for x, y in ((r.randint(0, 1600), r.randint(0, 900)) for _ in range(180)))
    if snow: b += "".join(f'<circle cx="{r.randint(0,1600)}" cy="{r.randint(0,900)}" r="{r.uniform(2,5):.1f}" fill="#f4f6ff" opacity=".8"/>' for _ in range(160))
    if leaves: b += "".join(f'<ellipse cx="{r.randint(0,1600)}" cy="{r.randint(560,880)}" rx="14" ry="6" fill="#b86a2e" opacity=".8" transform="rotate({r.randint(0,180)} 800 700)"/>' for _ in range(36))
    return svg(b, d)


# ------------------------------------------------------------------ closeups (a table, a lamp, one object)
def closeup(seed, obj):
    d, b = sky("#15161f", "#2a2430"); r = R(seed)
    b += f'<rect y="640" width="1600" height="260" fill="#3a2a22"/>' + "".join(f'<rect x="0" y="{y}" width="1600" height="3" fill="#2a1d18"/>' for y in range(670, 900, 34))
    b += glow(800, 560, 520, .25)
    if obj == "geranium":
        b += f'<path d="M600 640 L640 470 H960 L1000 640 Z" fill="#a8583a"/><rect x="590" y="450" width="420" height="34" fill="#c06a46"/>'
        b += "".join(f'<path d="M800 460 Q{800+dx} {400-dy} {800+dx*1.6} {330-dy}" stroke="{LEAF}" stroke-width="12" fill="none"/>' for dx, dy in ((-140, 0), (-60, 30), (40, 40), (150, 10)))
        b += "".join(f'<circle cx="{x}" cy="{y}" r="{rr}" fill="{RED}"/>' for x, y, rr in ((650, 300, 44), (760, 250, 52), (880, 285, 46), (960, 330, 38)))
        b += "".join(f'<ellipse cx="{x}" cy="{y}" rx="48" ry="26" fill="{LEAF}" transform="rotate({a} {x} {y})"/>' for x, y, a in ((690, 400, -30), (860, 390, 25), (780, 350, 5)))
    elif obj == "letter":
        b += paper(760, 660, 560, 40, -3) + paper(980, 650, 330, 30, 6)
        b += f'<rect x="1080" y="540" width="110" height="110" rx="14" fill="#1a1a24"/><rect x="1100" y="505" width="70" height="40" fill="#1a1a24"/><path d="M1150 520 L1330 300 L1318 292 L1136 508 Z" fill="{PAPER}"/><path d="M1330 300 L1380 250 L1340 290 Z" fill="{PAPER}"/>'
        b += candle(430, 650, 120)
    elif obj == "sweets":
        b += "".join(book(520 + i * 12, 640 - i * 38, 300 - i * 14, 36, c) for i, c in enumerate(("#6a3a32", "#3a4a6a", "#4a6a4a", "#8a6a3a")))
        b += f'<path d="M980 640 L960 440 Q1090 400 1220 440 L1200 640 Z" fill="#d6b27a"/><path d="M960 440 Q1090 380 1220 440 Q1090 420 960 440" fill="#bfa06a"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="22" fill="{c}"/>' for x, y, c in ((1030, 600, RED), (1100, 620, GOLD), (1160, 600, "#6aa0c0")))
    elif obj == "poems":
        b += f'<path d="M480 640 L800 600 L1120 640 L1120 660 L800 624 L480 660 Z" fill="{PAPER}"/><path d="M800 600 V624" stroke="#b9a98a" stroke-width="4"/>' + "".join(f'<rect x="{540+i*0}" y="{610+j*12}" width="{200-j*8}" height="3" fill="#8a7a62"/>' for i in (0,) for j in range(4))
        b += f'<circle cx="1180" cy="600" r="44" fill="none" stroke="#c9b27a" stroke-width="8"/><circle cx="1290" cy="600" r="44" fill="none" stroke="#c9b27a" stroke-width="8"/><path d="M1224 600 H1246" stroke="#c9b27a" stroke-width="8"/>'
    elif obj == "clock":
        b += f'<circle cx="800" cy="470" r="210" fill="#d8c48a"/><circle cx="800" cy="470" r="190" fill="{PAPER}"/>' + "".join(f'<line x1="{800+170*math.cos(a*math.pi/6)}" y1="{470+170*math.sin(a*math.pi/6)}" x2="{800+150*math.cos(a*math.pi/6)}" y2="{470+150*math.sin(a*math.pi/6)}" stroke="#2a1d1a" stroke-width="6"/>' for a in range(12))
        b += '<line x1="800" y1="470" x2="800" y2="340" stroke="#2a1d1a" stroke-width="10"/><line x1="800" y1="470" x2="900" y2="520" stroke="#2a1d1a" stroke-width="8"/><circle cx="800" cy="470" r="12" fill="#2a1d1a"/>'
        b += f'<rect x="780" y="230" width="40" height="40" rx="10" fill="#d8c48a"/>'
    elif obj == "desk":
        b += "".join(paper(640 + i * 16, 640 - i * 22, 520, 22, i % 3 - 1) for i in range(5)) + book(1010, 640, 260, 44, "#3a4a6a") + book(1030, 596, 220, 40, "#6a3a32")
        b += f'<rect x="420" y="560" width="90" height="80" rx="10" fill="#1a1a24"/><path d="M470 560 L560 380 L548 372 L456 552 Z" fill="{PAPER}"/>'
    elif obj == "boots":
        for x, tilt in ((560, -4), (880, 3)):
            b += f'<g transform="rotate({tilt} {x} 620)"><path d="M{x} 380 h120 l8 150 q120 10 150 70 v40 h-300 z" fill="#1c1710"/><path d="M{x-10} 650 h300 v22 h-300 z" fill="#0e0c08"/><path d="M{x+30} 560 q60 30 120 0" stroke="#4a3a28" stroke-width="6" fill="none"/><path d="M{x+190} 600 l30 -20 l10 30 z" fill="#2a2018"/></g>'
        b += f'<circle cx="760" cy="700" r="9" fill="{GOLD}"/>'
    elif obj == "candle_letter":
        b += paper(800, 660, 520, 40, 2) + candle(1050, 660, 150) + '<path d="M560 640 L760 560 L748 548 L548 628 Z" fill="#e8e0c8"/>' + glow(1050, 480, 380, .3)
    elif obj == "button":
        b = d_floor = None
        d, b = sky("#2a2018", "#3a2c20")
        b += "".join(f'<rect x="{x}" y="0" width="{w}" height="900" fill="{c}"/>' for x, w, c in ((0, 200, "#4a3424"), (200, 200, "#3e2c1e"), (400, 200, "#4a3424"), (600, 200, "#3e2c1e"), (800, 200, "#4a3424"), (1000, 200, "#3e2c1e"), (1200, 200, "#4a3424"), (1400, 200, "#3e2c1e")))
        b += '<ellipse cx="800" cy="520" rx="300" ry="120" fill="#fff0b0" opacity=".12"/>'
        b += f'<circle cx="800" cy="540" r="46" fill="#c8a84a"/><circle cx="800" cy="540" r="34" fill="#a8883a"/><circle cx="788" cy="530" r="6" fill="#2a1d18"/><circle cx="812" cy="530" r="6" fill="#2a1d18"/><circle cx="788" cy="552" r="6" fill="#2a1d18"/><circle cx="812" cy="552" r="6" fill="#2a1d18"/>'
        b += '<path d="M1100 900 L1180 600 L1300 600 L1360 900 Z" fill="#0f0d0a"/><rect x="1130" y="540" width="170" height="70" rx="20" fill="#0f0d0a"/>'
        b += '<path d="M0 900 L140 620 L260 620 L300 900 Z" fill="#0f0d0a"/><rect x="40" y="560" width="170" height="70" rx="20" fill="#0f0d0a"/>'
    elif obj == "tears":
        b += paper(800, 660, 600, 44, -2) + "".join(f'<circle cx="{x}" cy="{y}" r="{rr}" fill="#c9d4ea" opacity=".55"/>' for x, y, rr in ((700, 640, 12), (820, 650, 16), (900, 636, 10), (760, 660, 9))) + candle(1180, 664, 100) + glow(1180, 520, 360, .3)
    return svg(b, d)


# ------------------------------------------------------------------ rooms
def room(seed, kind):
    d, b = wall("#2c2433", "#3a3040", "#241c20", 640); r = R(seed)
    if kind == "partition":      # Makar's corner behind the kitchen partition: bed, trunk, table, candle
        b += f'<rect x="0" y="0" width="560" height="640" fill="#4a3a34"/><rect x="540" y="120" width="40" height="520" fill="{DWOOD}"/>'
        b += f'<rect x="700" y="500" width="560" height="140" fill="#6a5a50"/><rect x="700" y="470" width="560" height="40" fill="{PAPER}"/><rect x="1230" y="440" width="80" height="200" fill="{DWOOD}"/>'
        b += table(600, 100, 480) + candle(300, 600, 90) + glow(300, 500, 380, .3) + paper(210, 600, 110, 14) + win(1000, 100, 180, 260, False)
        b += f'<rect x="1200" y="560" width="300" height="100" fill="#4a3226"/><rect x="1200" y="552" width="300" height="12" fill="#2a1c16"/>'
    elif kind == "books":        # Pokrovsky's room: shelves of books, a table
        b += "".join(f'<rect x="{x}" y="{y}" width="{r.randint(34,52)}" height="{r.randint(110,150)}" fill="{r.choice(["#6a3a32","#3a4a6a","#4a6a4a","#8a6a3a","#5a3a6a"])}"/>' for y in (160, 340, 520) for x in range(120, 700, 56))
        b += f'<rect x="100" y="300" width="620" height="12" fill="{DWOOD}"/><rect x="100" y="480" width="620" height="12" fill="{DWOOD}"/><rect x="100" y="660" width="620" height="12" fill="{DWOOD}"/>'
        b += win(980, 120, 220, 340, True) + table(620, 820, 1480) + candle(1100, 620, 80) + book(1240, 620, 160, 36) + person(1330, 620, 1.2, "#100e16")
    elif kind == "embroidery":   # Varenka at the embroidery frame by the window
        b += win(160, 120, 360, 460, True, True) + f'<path d="M780 640 L860 340 H1140 L1220 640 Z" fill="#5a3a2c"/><rect x="800" y="300" width="400" height="50" fill="#6a4a3a"/>'
        b += f'<rect x="760" y="360" width="500" height="330" rx="10" fill="#f1e6cc" opacity=".95"/><path d="M820 560 q80 -140 180 -20 t180 -120" fill="none" stroke="{RED}" stroke-width="10"/><circle cx="1000" cy="420" r="30" fill="{LEAF}"/>'
        b += person(620, 700, 1.7, "#1a1622") + glow(340, 340, 420, .22)
    elif kind == "sickroom":     # a bed, a candle, a chair
        b += f'<rect x="300" y="460" width="760" height="190" fill="#6a5a54"/><rect x="300" y="420" width="760" height="60" fill="{PAPER}" opacity=".9"/><rect x="280" y="380" width="30" height="290" fill="{DWOOD}"/><rect x="1060" y="440" width="30" height="230" fill="{DWOOD}"/>'
        b += table(600, 1200, 1500) + candle(1350, 600, 100) + glow(1350, 480, 420, .3) + win(420, 100, 200, 260, False) + person(1130, 700, 1.6, "#100e16")
    elif kind == "samovar":
        b += table(600, 300, 1300) + f'<ellipse cx="800" cy="520" rx="100" ry="110" fill="#b08a3a"/><rect x="700" y="610" width="200" height="12" fill="#8a6a2a"/><rect x="760" y="380" width="80" height="50" fill="#b08a3a"/><path d="M700 500 H640 V540" stroke="#b08a3a" stroke-width="14" fill="none"/>'
        b += "".join(f'<path d="M{800+dx} 360 q-20 -50 0 -90 q20 -40 0 -80" stroke="#cfd0e6" stroke-width="10" fill="none" opacity=".4"/>' for dx in (-14, 14)) + f'<ellipse cx="1060" cy="590" rx="60" ry="14" fill="{PAPER}"/><rect x="1010" y="540" width="100" height="50" rx="12" fill="{PAPER}"/>' + win(1160, 120, 240, 320, False) + glow(800, 520, 400, .22)
    elif kind == "stove":
        b += f'<rect x="1000" y="180" width="380" height="460" fill="#8a6a54"/><rect x="1060" y="360" width="140" height="160" rx="10" fill="#1a1210"/><rect x="1080" y="400" width="100" height="110" fill="#e07a3a" opacity=".9"/><circle cx="1130" cy="460" r="170" fill="#e07a3a" opacity=".16"/>'
        b += table(620, 200, 760) + candle(480, 620, 70) + book(300, 620, 140, 32) + person(620, 640, 1.7, "#100e16") + win(140, 120, 200, 300, False)
    elif kind == "trunk":
        b += f'<rect x="500" y="520" width="520" height="190" fill="#7a5a3a"/><rect x="500" y="500" width="520" height="40" fill="#6a4a2a"/><rect x="490" y="560" width="540" height="14" fill="#2a1d1a"/><rect x="740" y="560" width="40" height="60" fill="{GOLD}"/>'
        b += f'<rect x="1080" y="580" width="300" height="130" fill="#6a4a2a"/><rect x="1080" y="560" width="300" height="30" fill="#5a3a22"/>' + f'<rect x="160" y="540" width="260" height="170" fill="#8a6a46"/><rect x="150" y="530" width="280" height="24" fill="#6a4a2a"/>' + win(1100, 90, 260, 340, False) + candle(300, 520, 60)
    elif kind == "tavern":
        b += win(200, 130, 520, 420, True) + f'<rect x="180" y="540" width="560" height="26" fill="{DWOOD}"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="#cfd8ee" opacity=".6"/>' for x, y in ((300, 200), (420, 280), (560, 220), (640, 340))) + table(650, 900, 1500) + f'<rect x="1100" y="560" width="90" height="90" rx="14" fill="{PAPER}"/><rect x="1260" y="570" width="80" height="80" rx="14" fill="{PAPER}"/>' + person(1000, 720, 1.5, "#100e16") + person(1400, 740, 1.4, "#12101a") + glow(1200, 520, 340, .2)
    elif kind == "packed":
        b += "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}"/><rect x="{x-6}" y="{y+h*.45}" width="{w+12}" height="12" fill="#2a1d1a"/>' for x, y, w, h, c in ((300, 500, 360, 200, "#7a5a3a"), (700, 560, 300, 140, "#6a4a2a"), (1060, 480, 240, 220, "#8a6a46"), (520, 380, 200, 120, "#6a4a2a")))
        b += win(1180, 80, 300, 300, False) + candle(160, 640, 60) + person(1040, 740, 1.8, "#100e16", bundle=True)
    return svg(b, d)


# ------------------------------------------------------------------ outdoors
def land(seed, kind):
    r = R(seed)
    if kind == "estate":      # a country house among trees, evening
        d, b = sky("#6f7fa6", "#f0cf9a"); b += '<circle cx="1220" cy="300" r="80" fill="#fff0c0" opacity=".85"/><rect y="640" width="1600" height="260" fill="#4a6a3a"/><path d="M0 640 Q400 600 800 640 T1600 630 L1600 700 L0 700 Z" fill="#3e5a30"/>'
        b += f'<rect x="520" y="420" width="520" height="230" fill="#d8c48a"/><polygon points="490,430 780,300 1070,430" fill="#8a4a3a"/>' + "".join(win(x, 480, 60, 90, True) for x in (570, 700, 830, 960)) + f'<rect x="740" y="560" width="80" height="90" fill="{DWOOD}"/>'
        for x in (180, 300, 1250, 1380, 1500): b += f'<rect x="{x-10}" y="470" width="20" height="200" fill="#3a2a22"/><circle cx="{x}" cy="440" r="{r.randint(90,130)}" fill="#3e5a30"/><circle cx="{x+40}" cy="470" r="80" fill="#4d6a3c"/>'
    elif kind == "grove":     # birch grove and a pond
        d, b = sky("#8fb0c0", "#f4e6b0"); b += '<rect y="620" width="1600" height="280" fill="#5a7a4a"/><ellipse cx="800" cy="760" rx="520" ry="90" fill="#6fa0b0"/><ellipse cx="800" cy="760" rx="440" ry="60" fill="#8fc0cc" opacity=".6"/>'
        for x in range(60, 1600, 140): h = r.randint(300, 460); b += f'<rect x="{x}" y="{620-h}" width="{r.randint(18,26)}" height="{h}" fill="#f0ecdc"/>' + "".join(f'<rect x="{x}" y="{620-h+y}" width="20" height="6" fill="#2a2a2a"/>' for y in range(40, h, 70)) + f'<circle cx="{x+10}" cy="{620-h}" r="{r.randint(50,80)}" fill="#6a8a4a" opacity=".9"/>'
    elif kind == "snowhouse":
        d, b = sky("#2a3050", "#8a90b0"); b += '<rect y="620" width="1600" height="280" fill="#dfe6f4"/><path d="M0 640 Q400 600 800 640 T1600 630 L1600 700 L0 700 Z" fill="#c8d2e6"/>'
        b += f'<rect x="560" y="440" width="440" height="190" fill="#6a4a3a"/><polygon points="530,450 780,330 1030,450" fill="#e8eefc"/>' + win(620, 500, 90, 90, True) + win(840, 500, 90, 90, True) + f'<rect x="740" y="560" width="64" height="70" fill="{DWOOD}"/>' + '<path d="M900 330 q-10 -60 20 -100 q30 -50 -10 -100" stroke="#cfd0e6" stroke-width="12" fill="none" opacity=".5"/>' + glow(665, 560, 200, .2)
        b += "".join(f'<circle cx="{r.randint(0,1600)}" cy="{r.randint(0,880)}" r="{r.uniform(2,5):.1f}" fill="#fff" opacity=".85"/>' for _ in range(180))
    elif kind == "church":       # a church interior with candles
        d, b = sky("#1a1722", "#2c2430"); b += f'<rect x="0" y="0" width="1600" height="900" fill="#1a1722"/>' + "".join(f'<rect x="{x}" y="0" width="60" height="760" fill="#3a3040"/><path d="M{x+60} 0 Q{x+190} 200 {x+320} 0 Z" fill="#2c2430"/>' for x in (180, 560, 940, 1320))
        b += f'<rect x="560" y="520" width="480" height="40" fill="{DWOOD}"/><rect x="620" y="460" width="360" height="70" fill="#2a1d1a"/>' + "".join(candle(x, 460, 60) for x in (660, 760, 840, 940)) + glow(800, 380, 460, .3) + f'<rect y="760" width="1600" height="140" fill="#14121a"/>' + person(300, 800, 1.2, "#0c0a10") + person(1280, 800, 1.2, "#0c0a10")
    elif kind == "coldroad":     # a winter road behind a sledge
        d, b = sky("#3a4060", "#c8a8a0"); b += '<rect y="600" width="1600" height="300" fill="#e0e6f2"/><path d="M0 600 Q500 560 1000 600 T1600 590 L1600 640 L0 640 Z" fill="#c4cde0"/><path d="M700 900 L860 900 L790 600 L770 600 Z" fill="#b8c2d8"/>'
        b += "".join(f'<rect x="{x}" y="{440+r.randint(0,60)}" width="14" height="170" fill="#2a2630"/><circle cx="{x+7}" cy="{430+r.randint(0,40)}" r="60" fill="#e8eefc"/>' for x in (120, 260, 1330, 1470)) + f'<rect x="640" y="700" width="240" height="30" fill="{DWOOD}"/><path d="M630 730 q-30 20 20 20 H900" stroke="#1a1a24" stroke-width="8" fill="none"/>' + person(760, 700, .9, "#14121c")
        b += "".join(f'<circle cx="{r.randint(0,1600)}" cy="{r.randint(0,880)}" r="{r.uniform(2,4):.1f}" fill="#fff" opacity=".8"/>' for _ in range(120))
    elif kind == "boat":
        d, b = sky("#8fb0d0", "#f6dca0"); b += '<circle cx="1280" cy="280" r="70" fill="#fff6d0" opacity=".9"/><rect y="560" width="1600" height="340" fill="#4a7a8a"/>' + "".join(f'<rect x="{r.randint(0,1500)}" y="{r.randint(600,880)}" width="{r.randint(60,160)}" height="3" fill="#dff0f4" opacity=".55"/>' for _ in range(30))
        b += '<path d="M500 700 Q620 770 900 770 L1020 690 Z" fill="#2a1d1a"/><rect x="760" y="520" width="8" height="180" fill="#2a1d1a"/><path d="M768 520 L900 680 H768 Z" fill="#f1e6cc"/>' + person(640, 700, .5, "#14121c") + person(700, 704, .46, "#1a1622") + '<path d="M0 560 Q300 520 700 550 T1600 540 L1600 580 L0 590 Z" fill="#3e5a3a"/>'
    elif kind == "bench":
        d, b = sky("#9fc0d8", "#f8ecc0"); b += '<rect y="600" width="1600" height="300" fill="#6a8a50"/><path d="M0 600 Q500 560 1000 600 T1600 590 L1600 640 L0 640 Z" fill="#5a7a42"/>'
        for x, h in ((200, 420), (420, 360), (1250, 440), (1450, 380)): b += f'<rect x="{x-12}" y="{620-h*.45}" width="24" height="{h*.45}" fill="#3a2a22"/><circle cx="{x}" cy="{620-h*.5}" r="{h*.3}" fill="#4d6a3c"/><circle cx="{x-60}" cy="{640-h*.4}" r="{h*.2}" fill="#5c7a48"/>'
        b += f'<rect x="640" y="640" width="320" height="16" fill="{DWOOD}"/><rect x="650" y="656" width="12" height="60" fill="{DWOOD}"/><rect x="938" y="656" width="12" height="60" fill="{DWOOD}"/><rect x="640" y="580" width="320" height="12" fill="{DWOOD}"/>' + person(730, 640, .8, "#2a2236") + person(840, 640, .75, "#3a2a22") + '<circle cx="360" cy="180" r="60" fill="#fff6d0" opacity=".9"/>'
    elif kind == "carriage":
        d, b = sky("#232a42", "#8a5a5a"); b += stars(r, 24, 1600, 260) + '<rect y="640" width="1600" height="260" fill="#1a1d2c"/><path d="M0 640 Q400 590 800 640 T1600 620 L1600 680 L0 680 Z" fill="#161a28"/>'
        b += f'<rect x="560" y="500" width="360" height="180" rx="30" fill="#2a2030"/><rect x="600" y="530" width="120" height="100" fill="{GOLD}" opacity=".85"/><rect x="740" y="530" width="120" height="100" fill="#3a3248"/><circle cx="620" cy="700" r="60" fill="#10101a"/><circle cx="860" cy="700" r="60" fill="#10101a"/><rect x="900" y="560" width="200" height="12" fill="#10101a"/><use href="#h"/>' + lamp(1300, 440, 230)
        b += '<ellipse cx="1060" cy="600" rx="90" ry="50" fill="#14121c"/><rect x="1120" y="520" width="36" height="110" fill="#14121c"/><path d="M1140 520 L1190 470 L1200 490 L1150 540 Z" fill="#14121c"/>'
    elif kind == "emptywin":
        d, b = wall("#201c28", "#2c2434", "#18141c", 720); b += win(520, 100, 560, 560, False, True) + f'<rect x="500" y="660" width="600" height="30" fill="{DWOOD}"/><rect x="560" y="640" width="60" height="20" fill="#7a3a2a"/>'
        b += "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="#cfd8ee" opacity=".5"/>' for x, y in ((650, 300), (800, 220), (900, 400), (740, 480))) + '<path d="M520 100 L520 660" stroke="#10101a" stroke-width="4"/>'
    return svg(b, d)


NEW = {
 "10_dawn_court": lambda: street(10, "#6a7aa8", "#f0c08a", lampy=False, people=1, sun=(1200, 560, 60)),
 "11_geranium": lambda: closeup(11, "geranium"), "12_letter_desk": lambda: closeup(12, "letter"),
 "13_partition": lambda: room(13, "partition"),
 "14_spring_street": lambda: street(14, "#8aa0c8", "#f0d8a8", lampy=True, people=5, left="#c8a878", right="#b89868", sun=(300, 220, 70)),
 "15_sweets_books": lambda: closeup(15, "sweets"),
 "16_estate": lambda: land(16, "estate"), "17_grove": lambda: land(17, "grove"), "18_snow_house": lambda: land(18, "snowhouse"),
 "19_books_room": lambda: room(19, "books"), "20_church": lambda: land(20, "church"), "21_embroidery": lambda: room(21, "embroidery"),
 "22_sickroom": lambda: room(22, "sickroom"), "23_cold_road": lambda: land(23, "coldroad"),
 "24_boat": lambda: land(24, "boat"), "25_bench_day": lambda: land(25, "bench"),
 "26_study_evening": lambda: room(26, "books"), "27_june_street": lambda: street(27, "#9fc0e0", "#f8ecc0", lampy=False, people=6, left="#d8c090", right="#c0a070", sun=(1300, 200, 70)),
 "28_poems": lambda: closeup(28, "poems"), "29_clock": lambda: closeup(29, "clock"), "30_samovar": lambda: room(30, "samovar"),
 "31_tavern": lambda: room(31, "tavern"), "32_summer_rain": lambda: street(32, "#4a5878", "#8a98b0", lampy=True, rain=True, people=2),
 "33_desk": lambda: closeup(33, "desk"), "34_boots": lambda: closeup(34, "boots"), "35_stove": lambda: room(35, "stove"),
 "36_evening_street": lambda: street(36, "#3a3a5c", "#d89a6a", lampy=True, people=4),
 "37_trunk": lambda: room(37, "trunk"), "38_candle_letter": lambda: closeup(38, "candle_letter"),
 "39_button": lambda: closeup(39, "button"), "40_embankment": lambda: street(40, "#6a7088", "#c0b0a0", lampy=True, people=3, leaves=True, left="#5a4a54", right="#4a4a5a"),
 "41_snowy_street": lambda: street(41, "#3a4060", "#a8b0c8", lampy=True, snow=True, people=3, left="#4a4660", right="#524a64"),
 "42_rain_embankment": lambda: street(42, "#2a3248", "#5a6882", lampy=True, rain=True, people=2, leaves=True),
 "43_cold_stove": lambda: room(43, "stove"), "44_packed": lambda: room(44, "packed"), "45_carriage": lambda: land(45, "carriage"),
 "46_empty_window": lambda: land(46, "emptywin"), "47_tears": lambda: closeup(47, "tears"),
}
if __name__ == "__main__":
    for n, fn in NEW.items():
        open(f"{OUT}/{n}.svg", "w", encoding="utf-8").write(fn()); print("wrote", n)
