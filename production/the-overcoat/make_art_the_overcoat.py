#!/usr/bin/env python3
"""Illustrations and cover for "The Overcoat" as SVG. Palette: Petersburg winter night, snow white, lamp gold, official grey-green,
and one colour that matters: the overcoat (old: threadbare brown-grey; new: deep green with a pale collar)."""
import random, math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "poor-folk"))
import make_art as _pf          # poor-folk's helpers (svg, sky, stars, win, person, lamp, building)
from make_art2 import candle, glow, paper, table, book, DWOOD, WOOD
svg, sky, stars, win, lamp, person, building = _pf.svg, _pf.sky, _pf.stars, _pf.win, _pf.lamp, _pf.person, _pf.building
PAPER, GOLD, RED = _pf.PAPER, _pf.GOLD, _pf.RED
OUT = "art"; os.makedirs(OUT, exist_ok=True)
SNOW, INK, OLD, NEW, FUR = "#e8eefc", "#0e0d14", "#6b5a4c", "#2f5442", "#c9b8a0"


def R(s): return random.Random(s)


def flakes(r, n, w=1600, h=900, op=.8): return "".join(f'<circle cx="{r.randint(0,w)}" cy="{r.randint(0,h)}" r="{r.uniform(2,5):.1f}" fill="#fff" opacity="{op}"/>' for _ in range(n))


def snowground(y=700, col="#dfe5f3", dark="#c4cee4"): return f'<rect y="{y}" width="1600" height="{900-y}" fill="{col}"/><path d="M0 {y+20} Q400 {y-20} 900 {y+20} T1600 {y+10} L1600 {y+80} L0 {y+80} Z" fill="{dark}"/>'


def street_walls(r, left="#3c3448", right="#4a3a44", lit=()):
    s = building(0, 520, 200 + r.randint(0, 80), left, 0, lit, 4) + building(1080, 520, 180 + r.randint(0, 80), right, 0, (), 4)
    return s


def man(x, y, s=1.0, coat=INK, collar=None, hat=True):
    """a walking man in a coat: a longer coat than person(); y is the ground line"""
    g = f'<g transform="translate({x} {y}) scale({s})"><rect x="-17" y="-30" width="13" height="30" fill="{INK}"/><rect x="4" y="-30" width="13" height="30" fill="{INK}"/>'
    g += f'<path d="M-26 -34 L-20 -112 Q0 -124 20 -112 L28 -34 Z" fill="{coat}"/><circle cx="0" cy="-130" r="14" fill="{INK}"/>'
    if hat: g += f'<rect x="-17" y="-148" width="34" height="9" fill="{INK}"/>'
    if collar: g += f'<path d="M-22 -112 Q0 -104 22 -112 L18 -122 Q0 -128 -18 -122 Z" fill="{collar}"/>'
    return g + '</g>'


def clerk(x, y, s=1.0, col="#17151e", head="#cdb08e", bald=False):
    """seated or standing clerk seen to the waist, y = shoulder line baseline"""
    g = f'<g transform="translate({x} {y}) scale({s})"><path d="M-44 90 Q-40 12 0 8 Q40 12 44 90 Z" fill="{col}"/><circle cx="0" cy="-24" r="22" fill="{head}"/>'
    g += f'<path d="M-22 -26 Q-20 -50 0 -50 Q20 -50 22 -26 Q10 -36 0 -34 Q-10 -36 -22 -26Z" fill="#3a2a20"/>' if not bald else '<path d="M-22 -22 Q-22 -34 -14 -40 L-18 -24Z M22 -22 Q22 -34 14 -40 L18 -24Z" fill="#6a4a30"/>'
    return g + '</g>'


def desk(x, y, w=300, lit=False):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="26" fill="#4a3226"/><rect x="{x+16}" y="{y+26}" width="22" height="{900-y-26}" fill="#2a1c16"/><rect x="{x+w-38}" y="{y+26}" width="22" height="{900-y-26}" fill="#2a1c16"/>'
    s += f'<polygon points="{x+20},{y} {x+w-20},{y} {x+w-50},{y-46} {x+50},{y-46}" fill="#6a4a38"/>' + f'<rect x="{x+90}" y="{y-44}" width="{w-180}" height="30" fill="{PAPER}" transform="rotate(-2 {x+w/2} {y-30})"/>'
    s += f'<rect x="{x+100}" y="{y-38}" width="{w-210}" height="3" fill="#b9a98a"/><rect x="{x+100}" y="{y-30}" width="{w-230}" height="3" fill="#b9a98a"/>'
    return s


def coat_shape(x, y, col, s=1.0, collar=FUR, holes=(), patch=None, shoulder=None):
    """a coat hanging from a hook at (x, y): shoulders, body, sleeves"""
    g = f'<g transform="translate({x} {y}) scale({s})">'
    g += f'<path d="M-70 40 Q-70 10 -30 0 L30 0 Q70 10 70 40 L96 330 L60 340 L48 120 L52 470 L-52 470 L-48 120 L-60 340 L-96 330 Z" fill="{col}"/>'
    g += f'<path d="M-30 0 Q0 22 30 0 L22 -14 Q0 -4 -22 -14 Z" fill="{collar}"/><path d="M0 24 V470" stroke="#00000044" stroke-width="4"/>'
    g += "".join(f'<circle cx="0" cy="{yy}" r="7" fill="#1a1612"/>' for yy in (80, 160, 240, 320))
    g += "".join(f'<ellipse cx="{hx}" cy="{hy}" rx="{hr}" ry="{hr*.8}" fill="#e9dfc4" opacity=".75"/>' for hx, hy, hr in holes)
    return g + '</g>'


def ghostly(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})" opacity=".92"><path d="M-30 -26 L-24 -112 Q0 -124 24 -112 L32 -26 Q0 -10 -30 -26Z" fill="#cfd8e6"/><circle cx="0" cy="-134" r="16" fill="#e6ecf4"/>'
            f'<path d="M-14 -142 H14" stroke="#10131d" stroke-width="3"/><circle cx="-5" cy="-136" r="2.4" fill="#10131d"/><circle cx="6" cy="-136" r="2.4" fill="#10131d"/><rect x="-3" y="-128" width="8" height="3" fill="#10131d"/>'
            f'<path d="M-30 -26 Q-50 40 -20 36 Q0 50 24 36 Q50 40 32 -26Z" fill="#cfd8e6" opacity=".35"/></g>')


# ---- Part I: A Certain Clerk -------------------------------------------------------------------------------
def a1_office():
    d, b = sky("#2b2f3a", "#3c3b40")
    b += '<rect y="640" width="1600" height="260" fill="#25211f"/>'
    b += "".join(f'<rect x="{x}" y="90" width="200" height="430" fill="#808ca8" opacity=".6"/><rect x="{x}" y="90" width="200" height="430" fill="none" stroke="#1a1620" stroke-width="10"/><line x1="{x+100}" y1="90" x2="{x+100}" y2="520" stroke="#1a1620" stroke-width="6"/><line x1="{x}" y1="270" x2="{x+200}" y2="270" stroke="#1a1620" stroke-width="6"/>' for x in (110, 480, 850))
    b += '<circle cx="1280" cy="170" r="62" fill="#d8c48a"/><circle cx="1280" cy="170" r="50" fill="#f1e6cc"/><line x1="1280" y1="170" x2="1280" y2="130" stroke="#2a1d1a" stroke-width="6"/><line x1="1280" y1="170" x2="1308" y2="186" stroke="#2a1d1a" stroke-width="5"/>'
    for i, x in enumerate((90, 420, 750)):
        b += clerk(x + 150, 520, 1.25, "#1c1a24") + desk(x, 650, 300)
    b += glow(1370, 520, 330, .3) + clerk(1370, 520, 1.3, "#201c22", "#d8b898", True) + desk(1230, 650, 300) + candle(1500, 640, 60)
    b += f'<rect x="1290" y="660" width="120" height="6" fill="{PAPER}"/>'
    return svg(b, d)


def a1_names():
    d, b = sky("#1d1a26", "#2e2630")
    b += '<rect y="640" width="1600" height="260" fill="#241c20"/>' + win(130, 100, 220, 320, False)
    b += f'<rect x="1000" y="470" width="480" height="180" fill="#6a5a54"/><rect x="1000" y="440" width="480" height="50" fill="{PAPER}" opacity=".9"/><rect x="1470" y="380" width="26" height="290" fill="{DWOOD}"/>'
    b += f'<ellipse cx="1180" cy="440" rx="46" ry="22" fill="#d8c8b0"/>'
    b += table(600, 420, 900) + glow(660, 470, 400, .3) + candle(520, 600, 70)
    b += f'<path d="M600 590 L680 560 L760 590 L760 600 L680 574 L600 600 Z" fill="{PAPER}"/><path d="M680 560 V574" stroke="#b9a98a" stroke-width="3"/>' + "".join(f'<rect x="{616+(j%2)*80}" y="{568+(j//2)*8}" width="{50-j*3}" height="3" fill="#8a7a62"/>' for j in range(4))
    b += person(300, 700, 1.7, "#100e16") + person(900, 700, 1.7, "#161320")
    b += f'<path d="M1100 560 q40 -20 80 0" stroke="#2a1d1a" stroke-width="8" fill="none"/>'
    return svg(b, d)


def a1_snow_paper():
    r = R(13); d, b = sky("#2b2f3a", "#3c3b40")
    b += '<rect y="640" width="1600" height="260" fill="#25211f"/>' + win(1100, 100, 300, 380, False)
    b += clerk(1000, 500, 1.4, "#1c1a24") + clerk(300, 500, 1.3, "#201c26") + f'<path d="M936 560 l-60 -90" stroke="#1c1a24" stroke-width="22"/><path d="M360 560 l60 -80" stroke="#201c26" stroke-width="22"/>'
    b += glow(660, 520, 380, .3) + clerk(660, 520, 1.5, "#241f26", "#d8b898", True) + desk(480, 650, 360) + candle(900, 640, 50)
    b += "".join(f'<rect x="{r.randint(420,900)}" y="{r.randint(150,620)}" width="{r.randint(16,30)}" height="{r.randint(10,18)}" fill="{PAPER}" transform="rotate({r.randint(0,180)} 600 400)" opacity=".92"/>' for _ in range(60))
    return svg(b, d)


# ---- Part II: The Copyist ----------------------------------------------------------------------------------
def a2_lamp_desk():
    d, b = sky("#15161f", "#2a2430")
    b += '<rect y="660" width="1600" height="240" fill="#2a1d1c"/>' + win(1120, 110, 260, 360, False) + "".join(f'<path d="M{1120+k*40} 470 q10 -60 30 -120" stroke="#cfe0ee" stroke-width="3" opacity=".25" fill="none"/>' for k in range(1, 6))
    b += table(640, 220, 1000) + glow(640, 520, 460, .3) + candle(760, 640, 90)
    b += "".join(paper(480 + i * 10, 640 - i * 18, 340, 18, i % 3 - 1) for i in range(4)) + f'<rect x="880" y="610" width="90" height="30" rx="6" fill="#4a3a30"/><circle cx="925" cy="600" r="5" fill="#2a1d18"/>'
    b += f'<g fill="#0e0d14"><path d="M330 660 Q340 450 480 430 Q580 430 590 520 L620 620 L540 660 Z"/><circle cx="520" cy="410" r="40"/></g><circle cx="508" cy="404" r="22" fill="#2a2430" opacity=".5"/>'
    b += f'<path d="M600 520 L640 600 L610 604 Z" fill="#0e0d14"/><path d="M628 600 L690 560 L684 552 L622 590Z" fill="{PAPER}"/>'
    return svg(b, d)


def a2_rubbish():
    r = R(22); d, b = sky("#1d2336", "#3a3a52")
    b += snowground(720) + building(0, 700, 150, "#52404a", 0, (), 5) + building(900, 700, 220, "#463a46", 0, (), 4)
    b += win(300, 270, 110, 140, True) + f'<rect x="270" y="410" width="180" height="16" fill="#2a1d1a"/>' + glow(355, 330, 300, .25)
    b += f'<g fill="#2a1d1a"><path d="M335 330 Q355 300 385 330 L388 410 L330 410Z"/></g><path d="M300 420 q-14 90 -20 170" stroke="#9a7a52" stroke-width="8" opacity=".5" fill="none"/>'
    for (x, y, rot) in ((340, 470, 20), (300, 540, -30), (390, 590, 60), (260, 650, 10)):
        b += f'<path d="M{x} {y} q20 -22 44 0 z" fill="#6a9a5a" transform="rotate({rot} {x} {y})"/><path d="M{x+4} {y+2} q16 -10 36 0" stroke="#d8e8c0" stroke-width="3" fill="none" transform="rotate({rot} {x} {y})"/>'
    b += man(560, 780, 1.5, "#4a3c34") + f'<ellipse cx="560" cy="605" rx="30" ry="14" fill="#9a8a6a"/><path d="M542 598 q18 -26 36 0 z" fill="#6a9a5a"/>' + lamp(1100, 560, 200) + flakes(r, 70, op=.6)
    return svg(b, d)


def a2_evening_windows():
    r = R(23); d, b = sky("#161a2e", "#2c3350")
    b += snowground(760) + f'<rect x="200" y="100" width="1200" height="680" fill="#4a3a44"/><rect x="180" y="86" width="1240" height="30" fill="#5a4a54"/>'
    lit = {(0, 0), (0, 2), (1, 1), (1, 3), (2, 0), (2, 2), (0, 4), (2, 4), (1, 5)}
    for i in range(4):
        for j in range(6):
            x, y = 250 + j * 190, 160 + i * 150
            if (i, j) == (3, 5): continue
            b += win(x, y, 110, 100, (i, j) in lit)
            if (i, j) in lit: b += f'<circle cx="{x+30}" cy="{y+60}" r="12" fill="#2a1c1a"/><circle cx="{x+72}" cy="{y+60}" r="12" fill="#2a1c1a"/>'
    b += win(1250, 610, 110, 100, False) + f'<rect x="1275" y="640" width="60" height="40" fill="{GOLD}" opacity=".18"/>' + lamp(150, 560, 220) + man(1010, 840, 1.1, "#4a3c34") + flakes(r, 90, op=.6)
    b += '<circle cx="1305" cy="665" r="10" fill="#0e0d14"/>'
    return svg(b, d)


# ---- Part III: The Frost and the Tailor ---------------------------------------------------------------------
def a3_frost():
    r = R(31); d, b = sky("#4a5a7e", "#e4c8b4")
    b += '<circle cx="1280" cy="250" r="56" fill="#fff3d8" opacity=".9"/>' + building(0, 520, 260, "#4a3a44", 0, (), 4) + building(1080, 520, 230, "#52424a", 0, (), 4) + snowground(700, "#d8def0")
    for i, (x, yy, s) in enumerate(((420, 790, 1.5), (620, 760, 1.3), (780, 820, 1.7), (960, 770, 1.35), (1120, 800, 1.5), (300, 840, 1.9))):
        b += man(x, yy, s, "#5a4c46") + f'<path d="M{x+16*s} {yy-132*s} q22 -4 40 -18" stroke="#fff" stroke-width="4" opacity=".6" fill="none"/>'
    b += lamp(700, 520, 190) + flakes(r, 100, op=.7)
    return svg(b, d)


def a3_old_coat():
    d, b = sky("#1b1b26", "#2e2630")
    b += '<rect y="700" width="1600" height="200" fill="#241c20"/>' + win(160, 120, 220, 320, False) + f'<rect x="1200" y="640" width="200" height="30" fill="{DWOOD}"/><rect x="1220" y="670" width="20" height="130" fill="{DWOOD}"/><rect x="1360" y="670" width="20" height="130" fill="{DWOOD}"/>'
    b += glow(800, 400, 560, .22) + f'<rect x="780" y="90" width="40" height="30" fill="#2a1d1a"/><rect x="796" y="110" width="8" height="40" fill="#8a7a62"/>'
    b += coat_shape(800, 150, OLD, 1.15, "#8a7860", holes=((-30, 80, 22), (30, 110, 16), (-8, 150, 12), (-50, 20, 12)))
    b += f'<path d="M-60 430 q60 -40 120 0" transform="translate(800 150)" stroke="#4a3e34" stroke-width="3" fill="none"/>'
    b += candle(1300, 640, 60) + glow(1300, 580, 260, .2)
    return svg(b, d)


def a3_stairs():
    r = R(33); d, b = sky("#2a2230", "#3a2c34")
    b += '<polygon points="0,900 0,300 1600,60 1600,900" fill="#241c24" opacity=".6"/>'
    for k in range(10):
        x, y = 160 + k * 120, 820 - k * 66
        b += f'<polygon points="{x},{y} {x+120},{y} {x+120},{y-66} {x},{y-66}" fill="{"#3a2c28" if k%2 else "#44342e"}"/><rect x="{x}" y="{y-8}" width="120" height="8" fill="#5a4a40"/>'
    b += f'<rect x="1300" y="60" width="300" height="300" fill="#e0a85a" opacity=".5"/><rect x="1330" y="90" width="240" height="270" fill="{GOLD}" opacity=".55"/>'
    b += "".join(f'<circle cx="{1400+r.randint(-120,160)}" cy="{r.randint(60,300)}" r="{r.randint(40,90)}" fill="#a8a2b8" opacity=".25"/>' for _ in range(14))
    b += man(640, 640, 1.5, "#6b5a4c") + '<ellipse cx="300" cy="840" rx="160" ry="22" fill="#4a5a76" opacity=".6"/>' + "".join(f'<path d="M{x} 860 q10 -10 30 0" stroke="#7a8aaa" stroke-width="3" fill="none"/>' for x in (200, 300, 380))
    b += glow(1450, 260, 340, .3)
    return svg(b, d)


def a3_tailor():
    d, b = sky("#28222a", "#3a3030")
    b += '<rect y="700" width="1600" height="200" fill="#241c1c"/>' + win(1100, 110, 300, 400, True) + glow(1250, 300, 500, .25)
    b += "".join(f'<rect x="{x}" y="{y}" width="150" height="60" rx="10" fill="{c}"/>' for x, y, c in ((100, 130, "#6a4a52"), (100, 200, "#4a5a6a"), (100, 270, "#7a6a4a"), (280, 150, "#5a3a3a")))
    b += f'<rect x="300" y="540" width="760" height="40" fill="#8a6a4a"/><rect x="340" y="580" width="30" height="320" fill="{DWOOD}"/><rect x="990" y="580" width="30" height="320" fill="{DWOOD}"/>'
    b += f'<path d="M420 540 Q560 470 760 520 L860 540Z" fill="{OLD}"/>'
    b += '<g fill="#14121a"><ellipse cx="660" cy="510" rx="150" ry="36"/><path d="M590 500 Q600 330 690 330 Q770 330 780 440 L780 510Z"/><circle cx="690" cy="300" r="50"/></g>'
    b += '<circle cx="676" cy="296" r="9" fill="#e8dcc0"/><rect x="706" y="290" width="26" height="8" fill="#10131d"/><path d="M630 350 Q690 380 750 350" stroke="#d8b050" stroke-width="8" fill="none"/>'
    b += '<ellipse cx="548" cy="520" rx="34" ry="16" fill="#d8b898"/><ellipse cx="774" cy="520" rx="34" ry="16" fill="#d8b898"/>' + candle(420, 540, 40)
    b += '<rect x="900" y="480" width="60" height="60" rx="8" fill="#14121a"/><path d="M900 480 L880 440 L980 440 L960 480Z" fill="#14121a"/>'
    return svg(b, d)


def a3_snuffbox():
    d, b = sky("#1b1b26", "#2e2630")
    b += f'<rect y="640" width="1600" height="260" fill="#3a2a22"/>' + f'<path d="M180 640 Q500 520 900 600 L1200 640Z" fill="{OLD}"/>' + glow(800, 520, 520, .25)
    b += '<ellipse cx="800" cy="530" rx="250" ry="250" fill="#9a8458"/><ellipse cx="800" cy="520" rx="226" ry="226" fill="#d8c48a"/>'
    b += '<circle cx="800" cy="540" r="150" fill="#6a5a46"/><path d="M700 640 Q720 560 800 540 Q880 560 900 640Z" fill="#3a5a4a"/><rect x="760" y="520" width="80" height="14" fill="#c9a84a"/>'
    b += f'<path d="M720 470 Q740 400 800 400 Q860 400 880 470 Q870 520 800 530 Q730 520 720 470Z" fill="#c8a888"/><rect x="760" y="440" width="84" height="84" fill="{PAPER}" transform="rotate(5 800 480)"/><path d="M766 450 l70 70 M836 450 l-70 70" stroke="#b9a98a" stroke-width="3" transform="rotate(5 800 480)"/>'
    b += '<path d="M1260 640 L1330 380 L1390 380 L1440 640 Z" fill="#14121a"/>'
    return svg(b, d)


def a3_sunday():
    r = R(36); d, b = sky("#6a789c", "#f0cfa0")
    b += snowground(690, "#dfe6f6") + building(0, 700, 220, "#52404a", 0, (), 4) + building(950, 650, 280, "#463a46", 0, (), 4)
    b += '<rect x="720" y="420" width="190" height="300" fill="#3a2c2e"/><rect x="745" y="450" width="140" height="270" fill="#5a4034"/><rect x="750" y="456" width="130" height="264" fill="#1a1210"/><rect x="770" y="470" width="40" height="40" fill="#2a1d1a"/>'
    b += '<circle cx="1220" cy="190" r="50" fill="#fff4d8" opacity=".9"/>' + man(600, 790, 1.5, OLD) + '<circle cx="640" cy="672" r="9" fill="#e3c27a"/>' + flakes(r, 50, op=.5)
    b += f'<path d="M600 700 L640 672" stroke="{INK}" stroke-width="10"/>'
    return svg(b, d)


# ---- Part IV: The Savings -----------------------------------------------------------------------------------
def a4_box():
    d, b = sky("#15161f", "#2a2430")
    b += f'<rect y="640" width="1600" height="260" fill="#3a2a22"/>' + "".join(f'<rect x="0" y="{y}" width="1600" height="3" fill="#2a1d18"/>' for y in range(670, 900, 34))
    b += glow(800, 540, 520, .28) + f'<rect x="560" y="440" width="480" height="260" rx="16" fill="#6a4a2a"/><rect x="560" y="440" width="480" height="60" rx="16" fill="#7a5a3a"/><rect x="740" y="470" width="120" height="8" rx="4" fill="#1a1008"/>'
    b += '<rect x="780" y="560" width="40" height="70" rx="6" fill="#c8a84a"/><circle cx="800" cy="580" r="10" fill="#1a1008"/>'
    b += "".join(f'<circle cx="{x}" cy="{y}" r="24" fill="{c}"/><circle cx="{x}" cy="{y}" r="16" fill="none" stroke="#00000033" stroke-width="3"/>' for x, y, c in ((340, 700, "#b8743a"), (420, 690, "#b8743a"), (500, 706, "#c0c8d0"), (1100, 700, "#c0c8d0"), (1180, 690, "#b8743a"), (1260, 704, "#c0c8d0"), (1140, 640, "#c0c8d0")))
    b += f'<g fill="{PAPER}" opacity=".85"><circle cx="800" cy="420" r="16" fill="#c0c8d0"/></g>' + candle(260, 640, 100) + glow(260, 480, 260, .2)
    return svg(b, d)


def a4_candle_work():
    d, b = sky("#1d1a24", "#2c2630")
    b += '<rect y="660" width="1600" height="240" fill="#2a1d1c"/>' + f'<rect x="1000" y="180" width="440" height="480" fill="#7a6048"/><rect x="1060" y="360" width="150" height="170" rx="10" fill="#1a1210"/><rect x="1080" y="400" width="110" height="120" fill="#e07a3a" opacity=".85"/>'
    b += glow(1130, 470, 360, .2) + table(630, 280, 900) + candle(470, 630, 90) + glow(470, 500, 440, .3)
    b += f'<g fill="#0e0d14"><path d="M560 660 Q570 500 680 480 Q760 490 770 560 L790 640 L700 660 Z"/><circle cx="660" cy="450" r="38"/></g>' + paper(620, 630, 220, 18, -3)
    b += f'<path d="M760 580 L820 600 L806 624 L750 604Z" fill="#0e0d14"/><path d="M300 740 q30 -30 60 0" stroke="#3a2a2a" stroke-width="6" fill="none"/>'
    b += '<rect x="130" y="300" width="14" height="14" fill="#cdb08e"/>'
    return svg(b, d)


def a4_cloth_shop():
    d, b = sky("#2a2230", "#3c3038")
    b += '<rect y="700" width="1600" height="200" fill="#2a1d1c"/>' + "".join(f'<rect x="{x}" y="{y}" width="{w}" height="70" rx="6" fill="{c}"/><circle cx="{x+w}" cy="{y+35}" r="35" fill="#00000030"/>' for x, y, w, c in ((100, 120, 260, "#3a5a4a"), (100, 200, 260, "#4a4a6a"), (100, 280, 260, "#6a3a42"), (100, 360, 260, "#8a7a5a"), (420, 120, 260, "#2a3a5a"), (420, 200, 260, "#5a5a52"), (420, 280, 260, "#7a4a3a"), (420, 360, 260, "#3a4a4a")))
    b += f'<rect x="760" y="560" width="760" height="40" fill="#6a4a38"/><rect x="780" y="600" width="26" height="200" fill="{DWOOD}"/><rect x="1470" y="600" width="26" height="200" fill="{DWOOD}"/>'
    b += f'<path d="M900 560 Q1000 470 1180 540 L1240 560Z" fill="{NEW}"/><path d="M1180 560 Q1270 500 1400 560Z" fill="#b8a88e"/>'
    b += person(660, 800, 1.6, "#14121a") + person(1000, 790, 1.5, "#2a2230") + win(1180, 100, 280, 340, True) + glow(1320, 280, 420, .2) + lamp(560, 400, 140, False)
    return svg(b, d)


# ---- Part V: The New Overcoat ---------------------------------------------------------------------------------
def a5_new_coat():
    d, b = sky("#1b2230", "#3a3a4a")
    b += '<rect y="700" width="1600" height="200" fill="#241c20"/>' + win(1160, 120, 260, 360, True) + glow(1290, 300, 500, .3)
    b += f'<rect x="780" y="90" width="40" height="30" fill="#2a1d1a"/><rect x="796" y="110" width="8" height="40" fill="#8a7a62"/>' + glow(800, 400, 560, .22)
    b += coat_shape(800, 150, NEW, 1.15, "#d8c8b0")
    b += '<path d="M-60 440 q60 20 120 0" transform="translate(800 150)" stroke="#1a3a2a" stroke-width="3" fill="none"/>'
    b += '<path d="M770 180 q-30 10 -30 70" stroke="#4a8a68" stroke-width="5" fill="none" opacity=".6"/>' + candle(300, 700, 90) + glow(300, 580, 300, .2)
    return svg(b, d)


def a5_fitting():
    d, b = sky("#28222a", "#3a3434")
    b += '<rect y="690" width="1600" height="210" fill="#241c1c"/>' + win(1160, 120, 260, 360, True) + glow(1290, 300, 420, .2)
    b += f'<g fill="#14121a"><path d="M560 700 L580 360 Q700 330 820 360 L850 700Z"/><circle cx="705" cy="310" r="44"/></g>' + f'<circle cx="705" cy="300" r="40" fill="#d8b898"/><path d="M670 290 Q705 250 740 290Z" fill="#6a4a30"/>'
    b += f'<path d="M540 700 L560 380 Q700 340 860 380 L890 700 Q700 730 540 700Z" fill="{NEW}"/><path d="M600 372 Q705 410 810 372 L804 346 Q705 360 606 346Z" fill="#d8c8b0"/>'
    b += f'<g fill="#1c1a24"><circle cx="1010" cy="380" r="44"/><path d="M930 700 L950 440 Q1010 420 1070 440 L1100 700Z"/><path d="M950 470 L880 400 L896 384 L970 450Z"/></g><circle cx="1010" cy="376" r="22" fill="#cdb08e" opacity=".3"/><rect x="988" y="368" width="14" height="10" fill="#e8dcc0"/>'
    b += '<rect x="880" y="400" width="90" height="26" fill="#f1e6cc" transform="rotate(-20 920 410)"/>'
    return svg(b, d)


def a5_porter():
    r = R(53); d, b = sky("#28303c", "#403c40")
    b += '<rect y="660" width="1600" height="240" fill="#2a2420"/>' + "".join(f'<rect x="{x}" y="180" width="14" height="40" fill="#8a7a62"/>' for x in range(160, 1500, 150))
    b += "".join(coat_shape(x, 230, c, .55, "#a89a82") for x, c in ((160, OLD), (310, "#3a3a4a"), (460, "#5a4a3a"), (610, "#2a3a4a"), (1010, "#4a3a3a"), (1160, "#3a4a3a"), (1310, OLD)))
    b += coat_shape(810, 230, NEW, .6, "#d8c8b0") + glow(810, 360, 260, .25)
    b += "".join(clerk(x, 580, 1.2, c) for x, c in ((420, "#1c1a24"), (560, "#241f26"), (1060, "#1c1a24"))) + f'<rect x="1220" y="560" width="140" height="150" fill="#4a3226"/><rect x="1210" y="545" width="160" height="25" fill="#5a4234"/>' + clerk(1290, 520, 1.1, "#2a2030")
    return svg(b, d)


# ---- Part VI: The Party ------------------------------------------------------------------------------------------
def a6_lit_window():
    r = R(61); d, b = sky("#12172b", "#2c3350")
    b += snowground(740) + building(0, 400, 330, "#3c3448", 0, (), 3) + f'<rect x="480" y="120" width="720" height="640" fill="#5a4448"/><rect x="460" y="100" width="760" height="34" fill="#6a5458"/>'
    for i in range(3):
        for j in range(4):
            x, y = 530 + j * 160, 180 + i * 190
            b += win(x, y, 100, 130, (i, j) in {(1, 1), (1, 2), (1, 3), (0, 3), (2, 0)})
    b += f'<rect x="525" y="365" width="110" height="140" fill="{GOLD}" opacity=".4"/>' + glow(1000, 470, 280, .25)
    b += f'<g fill="#2a1c1a"><circle cx="760" cy="440" r="14"/><circle cx="800" cy="450" r="14"/><rect x="745" y="450" width="30" height="40"/><rect x="786" y="460" width="30" height="30"/></g>'
    b += lamp(1320, 520, 220) + man(1000, 830, 1.6, NEW, "#d8c8b0") + flakes(r, 110, op=.7)
    return svg(b, d)


def a6_shop_picture():
    r = R(62); d, b = sky("#1c2030", "#3a3a52")
    b += snowground(720) + f'<rect x="300" y="120" width="1000" height="600" fill="{GOLD}" opacity=".2"/><rect x="300" y="120" width="1000" height="600" fill="none" stroke="#10101a" stroke-width="22"/>'
    b += f'<rect x="560" y="200" width="480" height="360" fill="#e8d4b0"/><rect x="560" y="200" width="480" height="360" fill="none" stroke="#6a4a2a" stroke-width="16"/>'
    b += '<path d="M700 540 Q720 420 800 400 Q880 420 900 540Z" fill="#b84a3a"/><circle cx="800" cy="372" r="30" fill="#e8c8a8"/><path d="M760 360 Q800 320 840 360 Q840 340 800 334 Q760 340 760 360Z" fill="#3a2a20"/><path d="M820 500 q60 20 90 -10" stroke="#e8c8a8" stroke-width="14" fill="none"/>'
    b += '<path d="M960 560 Q990 380 1000 330" stroke="#2a1c16" stroke-width="6" fill="none"/><circle cx="990" cy="350" r="26" fill="#d8b898"/><path d="M968 358 q22 24 44 0" stroke="#3a2a20" stroke-width="5" fill="none"/>'
    b += man(180, 860, 1.9, NEW, "#d8c8b0") + lamp(1450, 520, 220) + flakes(r, 120, op=.7)
    return svg(b, d)


def a6_hall():
    d, b = sky("#2a2430", "#3c3438")
    b += '<rect y="680" width="1600" height="220" fill="#2a2018"/>' + "".join(f'<rect x="{x}" y="150" width="12" height="36" fill="#8a7a62"/>' for x in range(100, 1500, 130))
    b += "".join(coat_shape(x, 190, c, .62, "#a89a82") for x, c in ((100, OLD), (230, "#3a3a4a"), (360, "#5a4a3a"), (490, "#2a3a4a"), (1000, "#4a3a3a"), (1130, "#3a4a3a"), (1260, "#5a3a42"), (1390, OLD)))
    b += "".join(f'<path d="M{x} 790 q30 -50 80 -10 v30 h-80 z" fill="#14121a"/>' for x in range(120, 700, 110))
    b += f'<ellipse cx="900" cy="640" rx="64" ry="72" fill="#b08a3a"/><rect x="840" y="702" width="120" height="10" fill="#8a6a2a"/><rect x="880" y="540" width="40" height="30" fill="#b08a3a"/>' + "".join(f'<path d="M{900+dx} 520 q-20 -50 0 -90 q20 -40 0 -80" stroke="#cfd0e6" stroke-width="10" fill="none" opacity=".4"/>' for dx in (-12, 12))
    b += glow(900, 640, 360, .2) + f'<rect x="700" y="260" width="120" height="360" fill="{GOLD}" opacity=".16"/>'
    return svg(b, d)


def a6_whist():
    d, b = sky("#241c24", "#3a2c30")
    b += '<rect y="660" width="1600" height="240" fill="#2a1d1c"/>' + win(80, 110, 220, 320, False)
    b += f'<ellipse cx="800" cy="640" rx="360" ry="70" fill="#2a5a46"/><rect x="760" y="650" width="80" height="200" fill="{DWOOD}"/>' + "".join(f'<rect x="{x}" y="{y}" width="36" height="52" rx="4" fill="{PAPER}" transform="rotate({a} {x+18} {y+26})"/>' for x, y, a in ((700, 600, -12), (760, 590, 4), (820, 604, 14), (880, 598, -6)))
    b += candle(620, 620, 50) + candle(980, 620, 50) + glow(800, 520, 560, .3)
    b += clerk(500, 470, 1.5, "#17151e") + clerk(1100, 470, 1.5, "#1c1a24") + clerk(800, 360, 1.3, "#201c26") + f'<g transform="translate(1320 600)"><rect x="0" y="0" width="60" height="100" rx="10" fill="{PAPER}"/><rect x="60" y="30" width="30" height="14" fill="{PAPER}"/></g>'
    b += '<path d="M1330 590 q-14 -50 10 -80 q26 -30 6 -70" stroke="#cfd0e6" stroke-width="8" fill="none" opacity=".35"/>'
    return svg(b, d)


# ---- Part VII: The Empty Square ------------------------------------------------------------------------------------
def a7_square():
    r = R(71); d, b = sky("#0e1226", "#2a3050")
    b += stars(r, 40, 1600, 300) + snowground(560, "#d8def0", "#b8c4e0") + '<polygon points="0,560 1600,560 1600,420 0,420" fill="#2a2e44" opacity=".5"/>'
    b += "".join(f'<rect x="{x}" y="{500}" width="{w}" height="60" fill="#2a2638"/>' for x, w in ((60, 120), (240, 80), (1300, 140), (1480, 100)))
    b += '<rect x="1040" y="498" width="40" height="64" fill="#3a2c28"/><rect x="1050" y="510" width="20" height="26" fill="#e07a3a"/><circle cx="1060" cy="500" r="60" fill="#e07a3a" opacity=".14"/>'
    b += "".join(f'<ellipse cx="{r.randint(100,1500)}" cy="{r.randint(640,860)}" rx="{r.randint(60,150)}" ry="10" fill="#b8c4e0" opacity=".5"/>' for _ in range(9))
    b += man(500, 790, 1.2, NEW, "#d8c8b0") + "".join(f'<ellipse cx="{500+k*40}" cy="{800+k*16}" rx="12" ry="6" fill="#b0bcd8" opacity=".6"/>' for k in range(-5, 0))
    b += flakes(r, 130, op=.6)
    return svg(b, d)


def a7_robbed():
    r = R(72); d, b = sky("#0e1226", "#2a3050")
    b += snowground(520, "#d8def0", "#b8c4e0") + '<rect x="1250" y="420" width="40" height="60" fill="#3a2c28"/><circle cx="1270" cy="430" r="40" fill="#e07a3a" opacity=".14"/>'
    b += f'<g fill="#1a1a2a"><circle cx="520" cy="740" r="30"/><path d="M440 780 Q470 700 560 720 L700 780 L690 830 L440 830Z"/></g><path d="M440 760 l-70 40" stroke="#1a1a2a" stroke-width="18"/><circle cx="508" cy="734" r="16" fill="#cdb08e"/>'
    b += '<g fill="#08080e"><circle cx="1000" cy="380" r="40"/><path d="M910 700 L930 450 Q1000 420 1070 450 L1100 700Z"/><rect x="940" y="690" width="40" height="120"/><rect x="1010" y="690" width="40" height="120"/><path d="M1070 480 L1180 430 L1196 456 L1086 520Z"/></g><path d="M960 450 Q1000 520 1040 450 L1100 700 L930 700Z" fill="#2a1c1a" opacity=".0"/>'
    b += '<rect x="920" y="360" width="160" height="14" fill="#08080e"/><path d="M1170 440 Q1220 400 1290 470 L1270 560 L1170 500Z" fill="#2f5442"/>'
    b += '<g fill="#08080e"><circle cx="1350" cy="560" r="34"/><path d="M1290 780 L1300 600 Q1350 580 1400 600 L1420 780Z"/></g><rect x="1300" y="630" width="130" height="14" fill="#08080e"/>'
    b += flakes(r, 150, op=.7)
    return svg(b, d)


def a7_police():
    r = R(73); d, b = sky("#2a2e44", "#4a4a5a")
    b += snowground(720) + building(0, 500, 220, "#3c3448", 0, (), 4) + f'<rect x="560" y="260" width="620" height="460" fill="#6a5a50"/><polygon points="540,270 870,160 1200,270" fill="{SNOW}"/>'
    b += f'<rect x="780" y="440" width="180" height="280" fill="#2a1c1a"/><rect x="800" y="460" width="140" height="260" fill="#1a1210"/>' + win(600, 320, 120, 160, True) + win(1020, 320, 120, 160, True) + f'<rect x="820" y="310" width="100" height="60" fill="#d8c8a0"/><rect x="835" y="330" width="70" height="8" fill="#2a1c1a"/>'
    b += man(660, 830, 1.8, "#5a4c46") + f'<path d="M640 700 L600 770" stroke="{INK}" stroke-width="10"/>' + man(1350, 810, 1.5, "#3a3a4a") + lamp(480, 540, 200) + flakes(r, 90, op=.6)
    return svg(b, d)


# ---- Part VIII: The Important Person ------------------------------------------------------------------------------
def a8_study():
    d, b = sky("#2a2230", "#3c2c34")
    b += '<rect y="660" width="1600" height="240" fill="#3a2428"/>' + f'<rect x="1150" y="60" width="400" height="640" fill="#5a2a32"/><rect x="1230" y="60" width="30" height="640" fill="#7a3a42"/><rect x="1380" y="60" width="30" height="640" fill="#7a3a42"/>'
    b += "".join(f'<rect x="{x}" y="{y}" width="{r_}" height="110" fill="{c}"/>' for x, y, r_, c in ((100, 130, 40, "#6a3a32"), (146, 130, 38, "#3a4a6a"), (190, 130, 44, "#4a6a4a"), (240, 130, 40, "#8a6a3a"), (290, 130, 40, "#5a3a6a"), (100, 330, 44, "#3a4a6a"), (150, 330, 38, "#6a3a32"), (194, 330, 44, "#8a6a3a")))
    b += f'<rect x="80" y="240" width="300" height="12" fill="{DWOOD}"/><rect x="80" y="440" width="300" height="12" fill="{DWOOD}"/>'
    b += f'<rect x="440" y="580" width="780" height="50" fill="#3a2418"/><rect x="480" y="630" width="40" height="270" fill="#2a1810"/><rect x="1140" y="630" width="40" height="270" fill="#2a1810"/><rect x="680" y="560" width="160" height="26" fill="#2a5a46"/>'
    b += clerk(560, 400, 1.7, "#1c3a2c", "#d8b898") + f'<rect x="500" y="360" width="120" height="20" fill="#b0902a" opacity=".0"/>' + f'<g fill="#e3c27a"><rect x="520" y="420" width="16" height="10"/><rect x="594" y="420" width="16" height="10"/></g>'
    b += clerk(1000, 440, 1.5, "#2a2030") + f'<rect x="990" y="470" width="120" height="14" fill="#cfd0e6" opacity=".0"/>'
    b += '<path d="M1060 470 q40 -20 70 -60" stroke="#cfd0e6" stroke-width="8" fill="none" opacity=".4"/>' + glow(800, 500, 400, .18)
    b += man(180, 840, 1.5, "#5a4c46") + f'<circle cx="180" cy="700" r="0" fill="none"/>'
    return svg(b, d)


def a8d_shouting():
    d, b = sky("#2a2230", "#3c2c34")
    b += '<rect y="660" width="1600" height="240" fill="#3a2428"/>' + f'<rect x="1200" y="60" width="400" height="640" fill="#5a2a32"/><rect x="1280" y="60" width="30" height="640" fill="#7a3a42"/>'
    b += win(120, 120, 260, 360, False) + glow(700, 460, 520, .18)
    b += f'<rect x="900" y="620" width="440" height="40" fill="#3a2418"/><rect x="930" y="660" width="30" height="240" fill="#2a1810"/><rect x="1280" y="660" width="30" height="240" fill="#2a1810"/>'
    b += clerk(1110, 440, 1.5, "#2a2030") + f'<path d="M1060 500 q40 -20 70 -60" stroke="#cfd0e6" stroke-width="8" fill="none" opacity=".4"/>'
    b += f'<g fill="#1c3a2c"><circle cx="640" cy="330" r="44"/><path d="M540 700 L560 410 Q640 380 720 410 L750 700Z"/><path d="M720 440 L800 340 L820 356 L744 470Z"/><rect x="570" y="690" width="50" height="130"/><rect x="660" y="690" width="50" height="130"/></g>'
    b += '<circle cx="640" cy="322" r="40" fill="#d8b898"/><path d="M606 318 Q640 280 674 318 Q640 300 606 318Z" fill="#3a2a20"/><path d="M622 340 q18 14 36 0" stroke="#3a2a20" stroke-width="6" fill="none"/><g fill="#e3c27a"><rect x="580" y="430" width="16" height="10"/><rect x="684" y="430" width="16" height="10"/></g>'
    b += '<g stroke="#f1e6cc" stroke-width="5" opacity=".7" fill="none"><path d="M540 330 l-40 -20"/><path d="M536 360 l-50 4"/><path d="M548 392 l-40 28"/></g>'
    b += '<ellipse cx="560" cy="826" rx="60" ry="12" fill="#00000040"/>' + man(260, 830, 1.5, "#5a4c46") + '<g stroke="#f1e6cc" stroke-width="3" opacity=".6"><path d="M200 690 l-20 -14"/><path d="M196 720 l-24 0"/></g>'
    return svg(b, d)


def a8_anteroom():
    d, b = sky("#242630", "#3a3a44")
    b += '<rect y="680" width="1600" height="220" fill="#2a2018"/>' + f'<rect x="640" y="130" width="320" height="560" fill="#3a2418"/><rect x="660" y="150" width="130" height="530" fill="#4a3022"/><rect x="800" y="150" width="140" height="530" fill="#1a1210"/><rect x="800" y="150" width="140" height="530" fill="{GOLD}" opacity=".28"/>'
    b += "".join(f'<rect x="{x}" y="560" width="110" height="26" fill="#4a3226"/><rect x="{x+8}" y="586" width="14" height="120" fill="{DWOOD}"/><rect x="{x+88}" y="586" width="14" height="120" fill="{DWOOD}"/><rect x="{x+8}" y="470" width="14" height="90" fill="{DWOOD}"/><rect x="{x+4}" y="470" width="102" height="14" fill="{DWOOD}"/>' for x in (120, 260, 400, 1100, 1250))
    b += man(980, 790, 1.7, "#1c3a2c") + f'<path d="M1010 620 L1040 560" stroke="{INK}" stroke-width="10"/>' + '<rect x="1020" y="540" width="50" height="34" fill="#f1e6cc" transform="rotate(-10 1040 556)"/>' + man(330, 810, 1.9, "#5a4c46") + lamp(1420, 400, 300, False)
    return svg(b, d)


def a8_blizzard():
    r = R(83); d, b = sky("#3a4256", "#9aa4b8")
    b += snowground(700, "#d0d8ec", "#b8c4e0") + building(0, 480, 220, "#4a3a44", 0, (), 4) + building(1120, 480, 260, "#52424a", 0, (), 4)
    b += lamp(560, 480, 220) + lamp(1080, 480, 220)
    b += "".join(f'<path d="M{r.randint(0,1600)} {r.randint(100,800)} h{r.randint(80,240)}" stroke="#fff" stroke-width="3" opacity=".5"/>' for _ in range(40))
    b += f'<g transform="rotate(14 800 780)">' + man(800, 800, 1.9, "#4a4a58") + '</g>' + flakes(r, 220, op=.85)
    return svg(b, d)


# ---- Part IX: The Fever -----------------------------------------------------------------------------------------
def a9_sickbed():
    d, b = sky("#1d1a24", "#2c2630")
    b += '<rect y="660" width="1600" height="240" fill="#2a1d1c"/>' + win(160, 110, 220, 320, False)
    b += f'<rect x="420" y="470" width="800" height="200" fill="#6a5a54"/><rect x="420" y="430" width="800" height="60" fill="{PAPER}" opacity=".9"/><rect x="400" y="380" width="30" height="300" fill="{DWOOD}"/><rect x="1210" y="440" width="30" height="240" fill="{DWOOD}"/>'
    b += f'<ellipse cx="560" cy="440" rx="60" ry="26" fill="{PAPER}"/><circle cx="560" cy="420" r="30" fill="#cdb08e"/><path d="M530 410 q0 -28 30 -28 q30 0 30 28" fill="#6a4a30"/>'
    b += table(620, 1290, 1560) + candle(1420, 620, 90) + glow(1420, 480, 440, .3)
    b += clerk(1010, 420, 1.7, "#100e16") + person(300, 780, 1.6, "#1a1622") + f'<rect x="920" y="520" width="26" height="24" fill="#cdb08e"/>'
    return svg(b, d)


def a9_empty_room():
    d, b = sky("#1d1a24", "#2c2630")
    b += '<rect y="660" width="1600" height="240" fill="#2a1d1c"/>' + win(1100, 110, 300, 400, False) + f'<rect x="780" y="90" width="40" height="30" fill="#2a1d1a"/><rect x="796" y="110" width="8" height="40" fill="#8a7a62"/>'
    b += coat_shape(800, 150, OLD, .95, "#8a7860", holes=((-30, 80, 22), (30, 110, 16), (-8, 150, 12)))
    b += f'<rect x="180" y="580" width="420" height="30" fill="#4a3226"/><rect x="200" y="610" width="26" height="200" fill="{DWOOD}"/><rect x="552" y="610" width="26" height="200" fill="{DWOOD}"/>'
    b += "".join(f'<path d="M{300+i*20} 570 l30 -60" stroke="#e8e0d0" stroke-width="4"/>' for i in range(6)) + paper(420, 580, 160, 18, 0)
    b += "".join(f'<ellipse cx="{x}" cy="{y}" rx="30" ry="12" fill="#6a6a78"/>' for x, y in ((1100, 830), (1180, 840), (1260, 826))) + '<circle cx="1000" cy="800" r="10" fill="#8a7a62"/><circle cx="1030" cy="810" r="10" fill="#8a7a62"/>'
    b += '<path d="M200 880 L1400 880" stroke="#3a2c2c" stroke-width="3"/>' + glow(800, 600, 600, .12)
    return svg(b, d)


def a9_new_clerk():
    d, b = sky("#2b2f3a", "#3c3b40")
    b += '<rect y="640" width="1600" height="260" fill="#25211f"/>' + "".join(f'<rect x="{x}" y="90" width="200" height="430" fill="#808ca8" opacity=".6"/><rect x="{x}" y="90" width="200" height="430" fill="none" stroke="#1a1620" stroke-width="10"/>' for x in (130, 700, 1270))
    b += clerk(800, 440, 1.8, "#2a2030", "#cdb08e") + desk(560, 650, 480) + f'<path d="M700 600 q40 -20 70 6 t80 -4" stroke="#1a1620" stroke-width="3" fill="none" opacity=".0"/>'
    b += "".join(f'<path d="M{700+i*30} 612 l14 -18" stroke="#1a1620" stroke-width="4"/>' for i in range(6)) + clerk(260, 540, 1.2, "#1c1a24") + desk(110, 650, 300) + clerk(1340, 540, 1.2, "#201c26") + desk(1190, 650, 300)
    return svg(b, d)


# ---- Part X: The Ghost --------------------------------------------------------------------------------------------
def a10_ghost_lamp():
    r = R(101); d, b = sky("#0e1226", "#2a3050")
    b += snowground(700, "#c8d0e4", "#a8b4d0") + building(0, 420, 300, "#2a2638", 0, (), 4) + building(1180, 420, 260, "#322a3c", 0, (), 4)
    b += lamp(800, 380, 330) + '<circle cx="800" cy="370" r="260" fill="#f4d27a" opacity=".1"/>'
    b += ghostly(660, 800, 2.1) + man(1050, 810, 1.6, "#4a4a58", "#c9b8a0", True) + '<path d="M690 590 l90 -30" stroke="#cfd8e6" stroke-width="12"/>'
    b += flakes(r, 130, op=.6)
    return svg(b, d)


def a10_bridge():
    r = R(102); d, b = sky("#0e1226", "#3a4262")
    b += f'<rect y="560" width="1600" height="340" fill="#1a2038"/>' + "".join(f'<rect x="{r.randint(0,1500)}" y="{r.randint(600,880)}" width="{r.randint(80,200)}" height="3" fill="#6a78a0" opacity=".5"/>' for _ in range(22))
    b += building(0, 360, 280, "#2a2638", 0, (), 4) + building(1240, 360, 300, "#322a3c", 0, (), 3)
    b += f'<path d="M360 560 Q800 330 1240 560 L1240 604 Q800 400 360 604Z" fill="#10131d"/><rect x="360" y="552" width="880" height="16" fill="#1a1f30"/>'
    b += "".join(lamp(x, 440, 110) for x in (470, 800, 1130)) + "".join(f'<rect x="{x-8}" y="640" width="16" height="70" fill="#f4d27a" opacity=".2"/>' for x in (470, 800, 1130))
    b += ghostly(800, 480, .8) + '<ellipse cx="800" cy="580" rx="700" ry="40" fill="#a8b4d0" opacity=".12"/>' + flakes(r, 80, op=.5)
    return svg(b, d)


def a10_sleigh():
    r = R(103); d, b = sky("#0e1226", "#2a3050")
    b += snowground(660, "#c8d0e4", "#a8b4d0") + building(0, 380, 280, "#2a2638", 0, (), 4) + lamp(1300, 440, 260)
    b += f'<path d="M420 700 Q420 600 500 600 L900 600 Q960 600 960 680 L940 700Z" fill="#3a2030"/><path d="M380 730 Q700 760 1000 720 Q1030 700 1010 690" stroke="#1a1218" stroke-width="12" fill="none"/>'
    b += f'<g fill="#1c3a2c"><circle cx="650" cy="470" r="38"/><path d="M570 610 L590 520 Q650 500 710 520 L740 610Z"/></g><path d="M610 520 Q650 560 690 520 L700 540 Q650 590 600 540Z" fill="#c9b8a0"/>'
    b += ghostly(830, 650, 1.1) + '<path d="M780 540 L700 520" stroke="#cfd8e6" stroke-width="14"/>'
    b += man(1100, 700, 1.1, "#2a2230") + '<g fill="#14121a"><ellipse cx="1170" cy="640" rx="90" ry="44"/><path d="M1240 620 l60 -60 l10 24 l-40 60z"/><rect x="1100" y="660" width="14" height="70"/><rect x="1230" y="660" width="14" height="70"/></g>'
    b += "".join(f'<path d="M{r.randint(0,1600)} {r.randint(100,800)} h{r.randint(80,240)}" stroke="#fff" stroke-width="3" opacity=".4"/>' for _ in range(30)) + flakes(r, 150, op=.8)
    return svg(b, d)


def a10_watchman():
    r = R(104); d, b = sky("#0e1226", "#2a3050")
    b += snowground(640, "#c8d0e4", "#a8b4d0") + building(0, 460, 260, "#2a2638", 0, (), 4) + building(1140, 460, 300, "#322a3c", 0, (), 3) + lamp(800, 380, 280)
    b += f'<g fill="#14121a"><circle cx="520" cy="560" r="34"/><path d="M450 830 L470 600 Q520 580 570 600 L600 830Z"/><rect x="620" y="400" width="10" height="440"/></g><path d="M610 400 l24 -50 l26 50z" fill="#8a8a98"/>'
    b += '<path d="M490 700 l80 -50" stroke="#14121a" stroke-width="16"/><path d="M560 640 q40 -30 60 -2" stroke="#a8884a" stroke-width="8" fill="none"/>'
    b += '<g stroke="#f1e6cc" stroke-width="4" opacity=".7" fill="none"><path d="M560 555 q40 -14 60 -4"/><path d="M570 575 q50 -2 74 8"/><path d="M552 540 q30 -34 46 -38"/></g>'
    b += ghostly(1000, 810, 1.9) + flakes(r, 90, op=.55)
    return svg(b, d)


def a10_obukhov():
    r = R(105); d, b = sky("#05070e", "#1a2038")
    b += '<rect y="620" width="1600" height="280" fill="#0e1220"/>' + f'<path d="M500 620 Q1000 400 1600 620 L1600 660 Q1000 460 500 660Z" fill="#08080e"/>' + "".join(f'<rect x="{r.randint(0,1600)}" y="{r.randint(660,880)}" width="{r.randint(80,200)}" height="3" fill="#3a4870" opacity=".5"/>' for _ in range(14))
    b += lamp(380, 440, 220) + f'<path d="M0 640 H520" stroke="#2a3050" stroke-width="3"/>'
    b += '<g transform="translate(700 800) scale(2.6)" opacity=".95"><path d="M-30 -26 L-24 -112 Q0 -124 24 -112 L32 -26 Q0 -10 -30 -26Z" fill="#cfd8e6"/><circle cx="0" cy="-134" r="16" fill="#e6ecf4"/><path d="M-24 -128 q12 -8 24 0 q12 -8 24 0 q-6 12 -12 6 q-12 -6 -24 0 q-6 6 -12 -6z" fill="#10131d"/><circle cx="-5" cy="-139" r="2.4" fill="#10131d"/><circle cx="6" cy="-139" r="2.4" fill="#10131d"/></g>'
    b += flakes(r, 100, op=.45)
    return svg(b, d)


# ---- covers -------------------------------------------------------------------------------------------------------
def cover(ru=False):
    r = R(8); d, b = sky("#0e1226", "#2c3350", 3000, 3000)
    b += stars(r, 90, 3000, 900) + '<circle cx="2300" cy="1250" r="170" fill="#fff4d8" opacity=".9"/>'
    b += '<rect y="2350" width="3000" height="650" fill="#e0e6f4"/><path d="M0 2380 Q700 2300 1500 2370 T3000 2350 L3000 2480 L0 2480Z" fill="#c8d2e6"/>'
    b += '<rect x="100" y="1500" width="600" height="850" fill="#2a2638"/><rect x="2300" y="1380" width="700" height="970" fill="#322a3c"/>'
    b += "".join(f'<rect x="{x}" y="{y}" width="80" height="110" fill="{GOLD if (x+y)%3 else "#2a3148"}"/>' for x in (160, 320, 480) for y in (1580, 1780, 1980))
    b += "".join(f'<rect x="{x}" y="{y}" width="80" height="110" fill="{GOLD if (x+y)%4 else "#2a3148"}"/>' for x in (2380, 2560, 2740) for y in (1460, 1680, 1900, 2120))
    b += f'<rect x="1100" y="1500" width="14" height="860" fill="#10131d"/><rect x="1060" y="1420" width="94" height="90" rx="10" fill="{GOLD}"/><rect x="1050" y="1400" width="114" height="26" fill="#10131d"/><circle cx="1107" cy="1460" r="320" fill="{GOLD}" opacity=".13"/><circle cx="1107" cy="1460" r="160" fill="{GOLD}" opacity=".16"/>'
    b += '<g transform="translate(1560 2370) scale(5.2)"><rect x="-17" y="-30" width="13" height="30" fill="#0e0d14"/><rect x="4" y="-30" width="13" height="30" fill="#0e0d14"/>'
    b += f'<path d="M-26 -34 L-20 -112 Q0 -124 20 -112 L28 -34 Z" fill="{NEW}"/><circle cx="0" cy="-130" r="14" fill="#0e0d14"/><rect x="-17" y="-148" width="34" height="9" fill="#0e0d14"/><path d="M-22 -112 Q0 -104 22 -112 L18 -122 Q0 -128 -18 -122 Z" fill="#d8c8b0"/></g>'
    b += '<path d="M1500 2420 q-20 20 -40 40 M1360 2470 q-20 18 -30 36" stroke="#b0bcd8" stroke-width="10" opacity=".6" fill="none"/>'
    b += "".join(f'<circle cx="{r.randint(0,3000)}" cy="{r.randint(900,3000)}" r="{r.uniform(4,9):.1f}" fill="#fff" opacity=".8"/>' for _ in range(180))
    T = ("НИКОЛАЙ ГОГОЛЬ", "Шинель") if ru else ("NIKOLAI GOGOL", "The Overcoat")
    size = 330 if ru else 270
    b += (f'<text x="1500" y="380" text-anchor="middle" font-family="Georgia, serif" font-size="92" letter-spacing="30" fill="#e3c27a">{T[0]}</text>'
          f'<text x="1500" y="780" text-anchor="middle" font-family="Georgia, serif" font-weight="bold" font-size="{size}" fill="{PAPER}">{T[1]}</text>'
          f'<rect x="1200" y="900" width="600" height="8" fill="#e3c27a"/><rect x="1330" y="930" width="340" height="5" fill="#e3c27a"/>')
    return svg(b, d, 3000, 3000)


FILES = {
    "1_office": a1_office, "1b_names": a1_names, "1c_snow_paper": a1_snow_paper,
    "2_lamp_desk": a2_lamp_desk, "2b_rubbish": a2_rubbish, "2c_evening_windows": a2_evening_windows,
    "3_frost": a3_frost, "3b_old_coat": a3_old_coat, "3d_tailor": a3_tailor, "3e_snuffbox": a3_snuffbox, "3f_sunday": a3_sunday,
    "4_box": a4_box, "4b_candle_work": a4_candle_work, "4c_cloth_shop": a4_cloth_shop,
    "5_new_coat": a5_new_coat, "5b_fitting": a5_fitting, "5c_porter": a5_porter,
    "6_lit_window": a6_lit_window, "6b_shop_picture": a6_shop_picture, "6c_hall": a6_hall, "6d_whist": a6_whist,
    "7_square": a7_square, "7b_robbed": a7_robbed, "7c_police": a7_police,
    "8_study": a8_study, "8d_shouting": a8d_shouting, "8b_anteroom": a8_anteroom, "8c_blizzard": a8_blizzard,
    "9_sickbed": a9_sickbed, "9b_empty_room": a9_empty_room, "9c_new_clerk": a9_new_clerk,
    "10_ghost_lamp": a10_ghost_lamp, "10b_bridge": a10_bridge, "10c_sleigh": a10_sleigh, "10e_obukhov": a10_obukhov,
    "cover": cover, "cover_ru": lambda: cover(True)}
if __name__ == "__main__":
    for n, fn in FILES.items():
        open(f"{OUT}/{n}.svg", "w", encoding="utf-8").write(fn()); print("wrote", n)
