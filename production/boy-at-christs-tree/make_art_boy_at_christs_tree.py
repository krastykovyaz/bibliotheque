#!/usr/bin/env python3
"""Illustrations and cover for "The Boy at Christ's Christmas Tree" as SVG. Palette: frost blue night, shop-window gold, snow white, one warm tree of light."""
import random, math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "poor-folk"))
import make_art as _pf
from make_art2 import candle, glow, DWOOD
svg, sky, stars, win, lamp, person = _pf.svg, _pf.sky, _pf.stars, _pf.win, _pf.lamp, _pf.person
PAPER, GOLD, RED, LEAF = _pf.PAPER, _pf.GOLD, _pf.RED, _pf.LEAF
OUT = "art"; os.makedirs(OUT, exist_ok=True)
SNOW = "#e8eefc"


def R(s): return random.Random(s)


def flakes(r, n, w=1600, h=900, op=.8): return "".join(f'<circle cx="{r.randint(0,w)}" cy="{r.randint(0,h)}" r="{r.uniform(2,5):.1f}" fill="#fff" opacity="{op}"/>' for _ in range(n))


def boy(x, y, s=1.0, col="#0e0d14", arm=None):
    """A small child in a smock and cap; arm='out' stretches one hand forward."""
    g = f'<g transform="translate({x} {y}) scale({s})" fill="{col}"><circle cx="0" cy="-92" r="15"/><path d="M-15 -100 Q0 -118 15 -100 Z"/><path d="M-17 -76 Q0 -86 17 -76 L22 -22 L-22 -22 Z"/><rect x="-14" y="-24" width="10" height="38"/><rect x="4" y="-24" width="10" height="38"/>'
    if arm == "out": g += '<path d="M14 -70 L56 -58 L52 -48 L12 -56 Z"/>'
    return g + '</g>'


def bldg(x, w, top, col, rows, seed, lit=.45):
    r = R(seed); s = f'<rect x="{x}" y="{top}" width="{w}" height="{900-top}" fill="{col}"/><rect x="{x-8}" y="{top-14}" width="{w+16}" height="20" fill="{SNOW}"/>'
    cols = max(2, int(w // 90))
    for i in range(rows):
        for j in range(cols):
            s += win(x + 26 + j * (w - 52) / cols, top + 40 + i * 120, 44, 66, r.random() < lit)
    return s


# 1 -- the corner: a small boy in a thin smock with his hand out, passers-by, a lamp, snow
def a1():
    r = R(1); d, b = sky("#1a2038", "#4a4a68")
    b += bldg(0, 560, 200, "#3c3448", 4, 11) + bldg(1060, 540, 260, "#463a48", 3, 12)
    b += '<rect y="720" width="1600" height="180" fill="#dde3f2"/><path d="M0 740 Q500 710 1000 740 T1600 730 L1600 790 L0 790 Z" fill="#c4cee2"/>' + lamp(760, 440, 280) + lamp(1000, 470, 250)
    b += person(260, 800, 1.5, "#14121c", True) + person(1330, 820, 1.6, "#1a1620") + person(1440, 800, 1.3, "#14121c")
    b += f'<ellipse cx="840" cy="842" rx="70" ry="10" fill="{GOLD}" opacity=".25"/>' + boy(840, 836, 2.0, "#0e0d14", "out") + '<rect x="826" y="676" width="28" height="16" fill="#8a7a6a"/>'
    b += flakes(r, 110, op=.7)
    return svg(b, d)


# 2 -- the cellar: a vaulted room, a small high window, a bunk with a still shape, a boy on a chest breathing steam, an old woman in a corner
def a2():
    r = R(2); d, b = sky("#161a28", "#262c3c")
    b += '<rect y="660" width="1600" height="240" fill="#14161e"/>'
    b += '<path d="M0 0 H1600 V120 Q800 330 0 120 Z" fill="#1c2030"/>' + "".join(f'<path d="M{x} 0 Q{x+60} 200 {x+200} 260" stroke="#2e3448" stroke-width="10" fill="none"/>' for x in (200, 700, 1200))
    b += '<polygon points="560,60 760,60 1000,420 480,420" fill="#9fb4d8" opacity=".12"/><rect x="560" y="60" width="200" height="110" fill="#c8d6f0" opacity=".85"/><line x1="660" y1="60" x2="660" y2="170" stroke="#161a28" stroke-width="8"/><line x1="560" y1="115" x2="760" y2="115" stroke="#161a28" stroke-width="6"/>'
    b += f'<rect x="760" y="520" width="620" height="30" fill="{DWOOD}"/><rect x="780" y="550" width="20" height="150" fill="#2a1c18"/><rect x="1340" y="550" width="20" height="150" fill="#2a1c18"/>'
    b += '<path d="M800 520 Q1000 470 1330 520 Z" fill="#6a5a68"/><circle cx="1330" cy="500" r="30" fill="#4a3c4c"/><path d="M1290 520 Q1330 470 1380 500 L1390 530 L1290 530 Z" fill="#6a5a68"/>'
    b += f'<rect x="300" y="590" width="170" height="110" rx="6" fill="#4a3426"/><rect x="300" y="590" width="170" height="14" fill="#6a4a36"/>'
    b += '<g fill="#0e0d14"><circle cx="360" cy="520" r="30"/><path d="M335 500 Q360 480 385 500 L385 506 L335 506 Z"/><path d="M326 550 Q360 538 396 552 L408 592 L318 596 Z"/><rect x="334" y="592" width="14" height="50"/><rect x="364" y="592" width="14" height="50"/></g>'
    b += "".join(f'<circle cx="{432+i*20}" cy="{500-i*18}" r="{9+i*3}" fill="#dfe8f8" opacity="{.5-i*.1:.2f}"/>' for i in range(4))
    b += '<g fill="#2c2634"><ellipse cx="130" cy="700" rx="90" ry="46"/><circle cx="150" cy="640" r="30"/></g><path d="M60 700 Q130 740 210 700" stroke="#3a3244" stroke-width="10" fill="none"/>'
    b += '<rect x="1000" y="700" width="120" height="90" fill="#222"/><rect x="1180" y="620" width="30" height="80" fill="#1c1c24"/>'
    b += '<path d="M0 690 Q400 668 800 690 T1600 680" stroke="#2a3040" stroke-width="4" fill="none"/>'
    return svg(b, d)


# 3 -- the shop windows at night: a lit window with a Christmas tree and dancing children, and the window of three little fiddling dolls; a small boy at the glass
def a3():
    r = R(3); d, b = sky("#161a2e", "#34384e")
    b += '<rect y="740" width="1600" height="160" fill="#262a3c"/>' + f'<rect x="60" y="100" width="720" height="640" fill="{GOLD}" opacity=".25"/><rect x="60" y="100" width="720" height="640" fill="none" stroke="#10101a" stroke-width="22"/>'
    b += f'<polygon points="420,160 300,420 540,420" fill="#2f5a40"/><polygon points="420,260 250,560 590,560" fill="#2f5a40"/><polygon points="420,380 200,700 640,700" fill="#386a4a"/><rect x="400" y="700" width="40" height="40" fill="#4a3022"/>'
    b += "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="{c}"/>' for x, y, c in ((420, 220, GOLD), (360, 330, RED), (470, 340, GOLD), (300, 460, GOLD), (400, 470, RED), (520, 480, GOLD), (250, 620, RED), (350, 600, GOLD), (470, 610, RED), (570, 640, GOLD)))
    b += f'<polygon points="420,130 432,160 466,162 440,182 450,214 420,196 390,214 400,182 374,162 408,160" fill="{GOLD}"/>'
    b += '<g fill="#14121c"><circle cx="150" cy="620" r="18"/><path d="M130 640 L120 740 L180 740 L170 640 Z"/><circle cx="680" cy="610" r="18"/><path d="M652 636 Q680 626 708 636 L720 740 L640 740 Z"/></g>'
    b += f'<rect x="860" y="100" width="680" height="640" fill="{GOLD}" opacity=".18"/><rect x="860" y="100" width="680" height="640" fill="none" stroke="#10101a" stroke-width="22"/><rect x="860" y="560" width="680" height="30" fill="#4a3022"/>'
    for x, y, c, v in ((1040, 440, "#b83a3a", 1), (1210, 450, "#2f6a4a", 0), (1380, 440, "#b83a3a", 0)):
        b += f'<g><path d="M{x-40} {y+120} L{x-30} {y+10} Q{x} {y-20} {x+30} {y+10} L{x+40} {y+120} Z" fill="{c}"/><circle cx="{x}" cy="{y-30}" r="26" fill="#e8c8a8"/><rect x="{x-24}" y="{y-62}" width="48" height="14" fill="#2a1c16"/></g>'
    b += '<g stroke="#6a3a22" stroke-width="8" fill="none"><ellipse cx="1060" cy="500" rx="40" ry="22" fill="#a8603a"/><path d="M1000 450 L1210 380"/></g><path d="M1240 470 l60 -30 M1430 480 l-60 -40" stroke="#6a3a22" stroke-width="8"/>'
    b += '<rect x="1000" y="146" width="480" height="8" fill="#c8c8d8" opacity=".5"/>'
    b += '<g fill="#c8c8d8" opacity=".6">' + "".join(f'<path d="M{x} 80 q0 70 30 100 l-10 20 q-30 -40 -20 -120 z"/>' for x in (900, 1500)) + '</g>'
    b += boy(1000, 850, 2.4, "#0e0d14") + f'<ellipse cx="1000" cy="860" rx="100" ry="12" fill="{GOLD}" opacity=".25"/>' + flakes(r, 130, op=.75) + lamp(1580, 520, 220)
    return svg(b, d)


# 4 -- Christ's tree: a tree of light in a deep blue heaven, children as bright figures flying round it, a mother at the side, a small boy carried
def a4():
    r = R(4); d, b = sky("#0d1236", "#3a3f78")
    b += stars(r, 220, 1600, 700) + '<circle cx="800" cy="440" r="460" fill="#ffe9a8" opacity=".12"/><circle cx="800" cy="440" r="300" fill="#ffe9a8" opacity=".14"/>'
    b += '<rect x="780" y="640" width="40" height="100" fill="#6a4a30"/>'
    for k, (y, w) in enumerate(((560, 520), (430, 420), (310, 320), (200, 220), (110, 130))):
        b += f'<polygon points="{800-w/2},{y+150} 800,{y-20} {800+w/2},{y+150}" fill="{["#3a7a56","#448a60","#4e9a6a","#58a874","#62b680"][k]}"/>'
    for i in range(70):
        y = r.uniform(120, 680); wmax = max(20, 250 * (y - 90) / 600)
        x = 800 + r.uniform(-wmax, wmax) * .8
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(6,11):.1f}" fill="{r.choice([GOLD, "#fff4c0", "#ffd0a0", "#c8e0ff"])}"/>'
    b += f'<polygon points="800,40 812,70 846,72 820,92 830,126 800,106 770,126 780,92 754,72 788,70" fill="#fff4c0"/>'
    for i in range(16):
        a = i / 16 * 2 * math.pi; rx, ry = 520 + 80 * math.sin(i), 260 + 40 * math.cos(i * 2)
        x, y = 800 + rx * math.cos(a), 420 + ry * math.sin(a) * .9
        s = r.uniform(.5, .8); col = r.choice(["#f4f1ff", "#ffe9d0", "#dfe8ff"])
        b += f'<g transform="translate({x:.0f} {y:.0f}) rotate({r.randint(-30,30)}) scale({s})"><circle cx="0" cy="-30" r="16" fill="{col}"/><path d="M-18 -10 Q0 -20 18 -10 L24 50 L-24 50 Z" fill="{col}"/><path d="M-18 -4 Q-70 -40 -90 -4 Q-60 6 -18 10 Z M18 -4 Q70 -40 90 -4 Q60 6 18 10 Z" fill="{col}" opacity=".7"/></g>'
    b += '<rect y="780" width="1600" height="120" fill="#e8eefc" opacity=".14"/>'
    b += '<g fill="#d8d0e8"><circle cx="1330" cy="560" r="22"/><path d="M1300 590 Q1330 576 1360 590 L1380 720 L1280 720 Z"/></g><path d="M1300 600 Q1250 560 1220 520" stroke="#d8d0e8" stroke-width="14" fill="none"/>'
    b += '<g fill="#f4f1ff"><circle cx="1210" cy="500" r="12"/><path d="M1196 516 Q1210 508 1224 516 L1230 570 L1190 570 Z"/></g>'
    b += '<g fill="#d8d0e8"><circle cx="1450" cy="620" r="20"/><path d="M1424 646 Q1450 634 1476 646 L1494 760 L1406 760 Z"/></g>'
    return svg(b, d)


# 5 -- the back yard at dawn: a woodpile by a gateway, a small shape in the snow, the yard-keeper with a broom arriving
def a5():
    r = R(5); d, b = sky("#3a4468", "#f0c0a8")
    b += '<circle cx="1180" cy="520" r="110" fill="#fff0d0" opacity=".85"/><rect y="640" width="1600" height="260" fill="#e8ecf8"/><path d="M0 660 Q500 620 1000 660 T1600 650 L1600 740 L0 740 Z" fill="#d0d8ec"/>'
    b += bldg(0, 420, 160, "#4a3c48", 4, 21, .1) + bldg(1180, 420, 200, "#52444c", 4, 22, .1)
    b += f'<rect x="420" y="330" width="40" height="320" fill="#3a2a2a"/><rect x="760" y="330" width="40" height="320" fill="#3a2a2a"/><path d="M420 330 Q610 250 800 330 L800 360 Q610 290 420 360 Z" fill="#3a2a2a"/><rect x="420" y="322" width="380" height="14" fill="{SNOW}"/>'
    for row in range(5):
        for k in range(9 - row):
            x = 130 + row * 24 + k * 56; y = 780 - row * 44
            b += f'<rect x="{x}" y="{y}" width="52" height="40" rx="6" fill="{["#7a5236","#6a4630","#8a5e40"][(k+row)%3]}"/><circle cx="{x+26}" cy="{y+20}" r="12" fill="#a87c56" opacity=".8"/>'
    b += f'<path d="M130 740 Q330 700 560 740 L580 750 L110 750 Z" fill="{SNOW}"/>'
    b += '<ellipse cx="770" cy="812" rx="70" ry="12" fill="#b8c2dc" opacity=".6"/><path d="M706 804 Q716 748 770 744 Q824 748 832 804 Z" fill="#2c2634"/><circle cx="722" cy="772" r="22" fill="#e8c8a8"/><path d="M700 764 Q722 738 746 764 Z" fill="#14121c"/><path d="M730 792 Q790 780 832 802 L832 812 L720 812 Z" fill="#e8eefc" opacity=".9"/>'
    b += person(1120, 810, 1.6, "#1a1620") + '<rect x="1170" y="640" width="6" height="130" fill="#5a3a2a" transform="rotate(14 1170 700)"/>'
    b += "".join(f'<path d="M{x} 560 q10 -90 -14 -150" stroke="#fff" stroke-width="12" fill="none" opacity=".25"/>' for x in (260, 1300))
    b += flakes(r, 60, op=.55)
    return svg(b, d)


def cover(ru=False):
    r = R(8); d, b = sky("#0d1236", "#3a3f78", 3000, 3000)
    b += stars(r, 160, 3000, 1500) + '<circle cx="1500" cy="1800" r="900" fill="#ffe9a8" opacity=".1"/><circle cx="1500" cy="1800" r="560" fill="#ffe9a8" opacity=".12"/>'
    b += '<rect x="1470" y="2300" width="60" height="180" fill="#6a4a30"/>'
    for k, (y, w) in enumerate(((2000, 900), (1750, 740), (1500, 580), (1280, 420), (1110, 260))):
        b += f'<polygon points="{1500-w/2},{y+280} 1500,{y-40} {1500+w/2},{y+280}" fill="{["#3a7a56","#448a60","#4e9a6a","#58a874","#62b680"][k]}"/>'
    for i in range(110):
        y = r.uniform(1150, 2260); wmax = max(30, 420 * (y - 1060) / 1200)
        b += f'<circle cx="{1500 + r.uniform(-wmax, wmax) * .8:.0f}" cy="{y:.0f}" r="{r.uniform(10,20):.1f}" fill="{r.choice([GOLD, "#fff4c0", "#ffd0a0", "#c8e0ff"])}"/>'
    b += '<polygon points="1500,950 1526,1006 1590,1010 1540,1048 1558,1110 1500,1076 1442,1110 1460,1048 1410,1010 1474,1006" fill="#fff4c0"/>'
    for i in range(22):
        a = i / 22 * 2 * math.pi; x, y = 1500 + 1150 * math.cos(a) * (.85 + .1 * math.sin(i)), 1900 + 520 * math.sin(a)
        s = r.uniform(1.0, 1.5); col = r.choice(["#f4f1ff", "#ffe9d0", "#dfe8ff"])
        b += f'<g transform="translate({x:.0f} {y:.0f}) rotate({r.randint(-30,30)}) scale({s})"><circle cx="0" cy="-30" r="16" fill="{col}"/><path d="M-18 -10 Q0 -20 18 -10 L24 50 L-24 50 Z" fill="{col}"/><path d="M-18 -4 Q-70 -40 -90 -4 Q-60 6 -18 10 Z M18 -4 Q70 -40 90 -4 Q60 6 18 10 Z" fill="{col}" opacity=".7"/></g>'
    b += '<rect y="2620" width="3000" height="380" fill="#e8eefc" opacity=".16"/>'
    T = ("ФЁДОР ДОСТОЕВСКИЙ", ["Мальчик у Христа", "на ёлке"], 250) if ru else ("FYODOR DOSTOEVSKY", ["The Boy at Christ's", "Christmas Tree"], 270)
    b += f'<text x="1500" y="300" text-anchor="middle" font-family="Georgia, serif" font-size="92" letter-spacing="30" fill="#e3c27a">{T[0]}</text>'
    for i, line in enumerate(T[1]):
        b += f'<text x="1500" y="{560 + i*(T[2]+40)}" text-anchor="middle" font-family="Georgia, serif" font-weight="bold" font-size="{T[2]}" fill="{PAPER}">{line}</text>'
    b += '<rect x="1200" y="1060" width="600" height="8" fill="#e3c27a" opacity="0"/>'
    return svg(b, d, 3000, 3000)


FILES = {"1_hand_out": a1, "2_cellar": a2, "3_shop_windows": a3, "4_christs_tree": a4, "5_yard": a5, "cover": cover, "cover_ru": lambda: cover(True)}
if __name__ == "__main__":
    for n, fn in FILES.items():
        open(f"{OUT}/{n}.svg", "w", encoding="utf-8").write(fn()); print("wrote", n)
