#!/usr/bin/env python3
"""Illustrations and cover for "Poor Folk" as SVG. One palette: St Petersburg dusk blue-grey, mustard window light,
brick, paper cream, a single red geranium. No known characters, no copies of existing paintings."""
import random, math, os
OUT = "art"; os.makedirs(OUT, exist_ok=True)
NIGHT, DUSK, SLATE = "#1c2233", "#2c3550", "#3d4866"
MUST, GOLD, BRICK, DBRICK = "#eab94e", "#f4d27a", "#8f5a44", "#6a4034"
PAPER, RED, LEAF = "#f1e6cc", "#c4432e", "#5c7048"


def svg(body, defs="", w=1600, h=900):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><defs>{defs}</defs>{body}</svg>'


def sky(c1, c2, w=1600, h=900):
    return (f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>',
            f'<rect width="{w}" height="{h}" fill="url(#sky)"/>')


def stars(r, n, w, ymax):
    return "".join(f'<circle cx="{r.uniform(0,w):.0f}" cy="{r.uniform(0,ymax):.0f}" r="{r.uniform(1,2.6):.1f}" fill="{PAPER}" opacity="{r.uniform(.4,.9):.2f}"/>' for _ in range(n))


def win(x, y, w, h, lit=True, curtain=False):
    f = GOLD if lit else "#2a3148"
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{f}"/>'
    s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="#2a1d1a" stroke-width="5"/>'
    s += f'<line x1="{x+w/2}" y1="{y}" x2="{x+w/2}" y2="{y+h}" stroke="#2a1d1a" stroke-width="4"/><line x1="{x}" y1="{y+h*.45}" x2="{x+w}" y2="{y+h*.45}" stroke="#2a1d1a" stroke-width="4"/>'
    if curtain: s += f'<path d="M{x} {y} L{x+w*.38} {y} Q{x+w*.2} {y+h*.5} {x+w*.08} {y+h*.8} L{x} {y+h*.8} Z" fill="{PAPER}" opacity=".9"/>'
    return s


def lamp(x, y, h=170, glow=True):
    s = f'<rect x="{x-3}" y="{y}" width="6" height="{h}" fill="#10131d"/><rect x="{x-16}" y="{y-26}" width="32" height="30" rx="5" fill="{GOLD}"/><rect x="{x-20}" y="{y-34}" width="40" height="9" fill="#10131d"/>'
    if glow: s = f'<circle cx="{x}" cy="{y-10}" r="90" fill="{GOLD}" opacity=".16"/><circle cx="{x}" cy="{y-10}" r="46" fill="{GOLD}" opacity=".2"/>' + s
    return s


def person(x, y, s=1.0, col="#10131d", bundle=False):
    g = f'<g transform="translate({x} {y}) scale({s})" fill="{col}"><circle cx="0" cy="-122" r="15"/><path d="M-20 -104 Q0 -116 20 -104 L26 -28 L-26 -28 Z"/><rect x="-18" y="-30" width="13" height="48"/><rect x="5" y="-30" width="13" height="48"/>'
    if bundle: g += '<rect x="22" y="-92" width="34" height="30" rx="4"/>'
    return g + '</g>'


def building(x, w, top, col, wins, lit_idx=(), rows=4, r=None):
    s = f'<rect x="{x}" y="{top}" width="{w}" height="{900-top}" fill="{col}"/>'
    cols = max(2, int(w // 90))
    for i in range(rows):
        for j in range(cols):
            cx = x + 28 + j * (w - 56) / cols; cy = top + 40 + i * 115
            s += win(cx, cy, 46, 70, lit=(i, j) in lit_idx)
    return s


# 1 -- two facing walls of a courtyard, one lit window with a geranium (April)
def a1():
    d, b = sky(NIGHT, DUSK); r = random.Random(1); d2 = d
    b += stars(r, 40, 1600, 250)
    b += building(0, 640, 120, DBRICK, 0, (), 5) + building(960, 640, 150, BRICK, 0, (), 5)
    lit = [(1, 1), (3, 0), (2, 1), (0, 2), (4, 2)]
    b = b.replace('</svg>', '')
    b += win(160, 270, 84, 112, True, True) + f'<rect x="150" y="380" width="104" height="14" fill="#2a1d1a"/><circle cx="188" cy="364" r="13" fill="{RED}"/><circle cx="212" cy="360" r="11" fill="{RED}"/><path d="M200 380 q-10 -20 -12 -30 M204 380 q8 -18 14 -26" stroke="{LEAF}" stroke-width="5" fill="none"/>'
    b += win(1180, 300, 84, 112, True, True)
    b += '<polygon points="640,900 960,900 860,700 740,700" fill="#12151f" opacity=".6"/>'
    b += f'<rect x="0" y="780" width="1600" height="120" fill="#141824"/><path d="M0 790 H1600" stroke="#2c3550" stroke-width="3"/>' + lamp(800, 600, 200)
    return svg(b, d2)


# 2 -- a canal with an arched bridge and gas lamps, May evening
def a2():
    d, b = sky("#3b3f66", "#e0a05a"); r = random.Random(2)
    b += '<circle cx="1180" cy="520" r="90" fill="#f6d98a" opacity=".85"/>'
    b += f'<rect y="560" width="1600" height="340" fill="#2a3150"/>' + building(0, 420, 330, DBRICK, 0, (), 2) + building(1180, 420, 300, BRICK, 0, (), 3)
    b += f'<path d="M380 560 Q800 380 1220 560 L1220 600 Q800 430 380 600 Z" fill="#10131d"/><rect x="380" y="556" width="840" height="14" fill="#1a1f30"/>'
    for x in (480, 800, 1120): b += lamp(x, 470, 90)
    b += person(640, 560, .55) + person(950, 556, .5, bundle=True)
    b += "".join(f'<rect x="{x}" y="{620+i*26}" width="{90-i*8}" height="5" fill="{GOLD}" opacity=".35"/>' for i, x in enumerate((780, 770, 765, 775, 780)))
    return svg(b, d)


# 3 -- the notebook: a candle, an open notebook, a girl's silhouette at a table
def a3():
    d, b = sky("#171b2b", "#2b2f45")
    b += f'<rect y="620" width="1600" height="280" fill="#20202c"/><rect x="900" y="150" width="420" height="330" fill="#2a3552"/>{win(940,190,160,250,False)}{win(1130,190,160,250,False)}'
    b += '<circle cx="640" cy="470" r="330" fill="#f4d27a" opacity=".13"/><circle cx="640" cy="470" r="160" fill="#f4d27a" opacity=".2"/>'
    b += f'<rect x="380" y="600" width="520" height="22" fill="#4a2f28"/><rect x="400" y="620" width="18" height="230" fill="#3a2420"/><rect x="860" y="620" width="18" height="230" fill="#3a2420"/>'
    b += f'<path d="M480 588 L640 560 L800 588 L800 600 L640 574 L480 600 Z" fill="{PAPER}"/><path d="M640 560 V574" stroke="#b9a98a" stroke-width="3"/>'
    b += "".join(f'<path d="M{500+i*0} {592-0} " />' for i in range(0))
    b += f'<rect x="700" y="500" width="22" height="84" fill="{PAPER}"/><path d="M711 474 q-12 20 0 28 q12 -8 0 -28" fill="{GOLD}"/>'
    b += person(560, 600, 1.9, "#0f111a")
    return svg(b, d)


# 4 -- June: an island garden by the river, a bench and a small boat
def a4():
    d, b = sky("#6f8fb0", "#f2d9a0"); r = random.Random(4)
    b += '<circle cx="320" cy="260" r="70" fill="#fff3c8" opacity=".9"/>'
    b += f'<rect y="560" width="1600" height="340" fill="#4a6a7a"/>' + "".join(f'<rect x="{r.randint(0,1500)}" y="{r.randint(600,880)}" width="{r.randint(60,160)}" height="3" fill="#cfe3e8" opacity=".5"/>' for _ in range(24))
    b += f'<path d="M0 560 Q300 500 620 540 T1600 520 L1600 600 L0 600 Z" fill="#3e5a3a"/>'
    for x, h in ((1200, 360), (1330, 300), (1460, 400), (1540, 280)): b += f'<rect x="{x-8}" y="{520-h*.2}" width="16" height="{h*.4}" fill="#3a2a22"/><circle cx="{x}" cy="{520-h*.35}" r="{h*.28}" fill="{LEAF}"/><circle cx="{x-50}" cy="{540-h*.3}" r="{h*.2}" fill="#4d6a3c"/>'
    b += f'<rect x="180" y="520" width="170" height="12" fill="#3a2a22"/><rect x="190" y="532" width="8" height="50" fill="#3a2a22"/><rect x="332" y="532" width="8" height="50" fill="#3a2a22"/><rect x="180" y="480" width="170" height="10" fill="#3a2a22"/>'
    b += '<path d="M700 700 Q760 740 880 740 L940 690 Z" fill="#2a1d1a"/><rect x="800" y="640" width="6" height="64" fill="#2a1d1a"/><path d="M806 640 L870 690 H806 Z" fill="#f1e6cc"/>'
    return svg(b, d)


# 5 -- white night over the canal: pale sky, dark houses, golden reflections, a bridge
def a5():
    d, b = sky("#8b94b8", "#f0cf9a")
    b += f'<rect y="610" width="1600" height="290" fill="#59638a"/>' + building(0, 520, 280, "#3c3448", 0, (), 3) + building(1060, 540, 240, "#4a3a44", 0, (), 4)
    b += f'<rect x="520" y="560" width="540" height="40" fill="#2a2433"/><path d="M520 560 Q790 430 1060 560" fill="none" stroke="#2a2433" stroke-width="22"/>'
    for x in (600, 790, 980): b += lamp(x, 470, 90)
    b += "".join(f'<rect x="{600+i*190-30}" y="{650+j*28}" width="60" height="5" fill="{GOLD}" opacity=".4"/>' for i in range(3) for j in range(4))
    b += f'<circle cx="1240" cy="140" r="40" fill="#fff7dc" opacity=".8"/>'
    return svg(b, d)


# 6 -- the office: slanted desks, a green lamp, piles of paper, a quill
def a6():
    d, b = sky("#2a2f3f", "#3d3a3a")
    b += f'<rect y="620" width="1600" height="280" fill="#2a2420"/><rect x="0" y="0" width="1600" height="620" fill="#3a3630" opacity=".55"/>'
    b += win(150, 90, 240, 340, True) + win(1180, 90, 240, 340, True)
    for x in (260, 760, 1160):
        b += f'<path d="M{x} 650 L{x+300} 650 L{x+260} 560 L{x+40} 560 Z" fill="#5a3a2c"/><rect x="{x+16}" y="650" width="14" height="150" fill="#3a2420"/><rect x="{x+270}" y="650" width="14" height="150" fill="#3a2420"/>'
        b += f'<rect x="{x+80}" y="540" width="120" height="22" fill="{PAPER}"/><rect x="{x+90}" y="522" width="100" height="20" fill="#e3d6b6"/>'
        b += f'<line x1="{x+220}" y1="560" x2="{x+250}" y2="480" stroke="{PAPER}" stroke-width="4"/>'
        b += person(x+150, 650, 1.1, "#141018")
    b += '<path d="M780 420 L820 420 L830 470 L770 470 Z" fill="#3d7a5a"/><circle cx="800" cy="500" r="120" fill="#6fd6a0" opacity=".08"/>'
    return svg(b, d)


# 7 -- a rainy window, the street lamp blurred into a halo
def a7():
    d, b = sky("#222a3c", "#3a4660"); r = random.Random(7)
    b += f'<circle cx="1000" cy="360" r="170" fill="{GOLD}" opacity=".18"/><circle cx="1000" cy="360" r="70" fill="{GOLD}" opacity=".35"/><rect x="994" y="400" width="12" height="360" fill="#10131d"/>'
    b += f'<rect y="740" width="1600" height="160" fill="#161a28"/>' + building(0, 380, 360, "#2a2236", 0, (), 3) + building(1320, 280, 300, "#2a2236", 0, (), 4)
    for _ in range(140):
        x = r.randint(0, 1600); y = r.randint(0, 880); l = r.randint(30, 120)
        b += f'<path d="M{x} {y} q3 {l/2} 0 {l}" stroke="#cfd8ee" stroke-width="{r.uniform(1.5,4):.1f}" fill="none" opacity="{r.uniform(.15,.5):.2f}" stroke-linecap="round"/>'
    b += f'<rect x="0" y="0" width="1600" height="900" fill="none" stroke="#10131d" stroke-width="90"/><line x1="800" y1="0" x2="800" y2="900" stroke="#10131d" stroke-width="40"/>'
    return svg(b, d)


# 8 -- an autumn street; a cart loaded with trunks at the door
def a8():
    d, b = sky("#5a5870", "#d6a56a"); r = random.Random(8)
    b += f'<rect y="640" width="1600" height="260" fill="#3a3238"/>' + building(0, 560, 220, DBRICK, 0, (), 4, r) + building(1040, 560, 260, BRICK, 0, (), 4, r)
    for x in (700, 820, 940):
        b += f'<rect x="{x}" y="520" width="12" height="140" fill="#2a1d1a"/>' + "".join(f'<path d="M{x+6} 540 L{x+r.randint(-90,90)} {r.randint(420,500)}" stroke="#2a1d1a" stroke-width="6" fill="none"/>' for _ in range(5))
    b += "".join(f'<ellipse cx="{r.randint(640,1000)}" cy="{r.randint(700,860)}" rx="14" ry="6" fill="#c0702e" opacity=".8" transform="rotate({r.randint(0,180)} 800 780)"/>' for _ in range(40))
    b += f'<rect x="520" y="690" width="420" height="40" fill="#2a1d1a"/><circle cx="580" cy="748" r="48" fill="#1a1210"/><circle cx="880" cy="748" r="48" fill="#1a1210"/>'
    b += f'<rect x="560" y="600" width="140" height="92" fill="#6a4a2a"/><rect x="720" y="630" width="170" height="62" fill="#7a5a34"/><rect x="600" y="540" width="100" height="60" fill="#5a3a22"/>'
    b += person(1020, 700, 1.0, "#12141c", bundle=True)
    return svg(b, d)


# 9 -- the end: an empty road at dusk, one lamp, a small figure walking away
def a9():
    d, b = sky("#232a42", "#7a5a5a"); r = random.Random(9)
    b += stars(r, 30, 1600, 300)
    b += f'<path d="M0 620 L1600 600 L1600 900 L0 900 Z" fill="#1a1d2c"/><path d="M700 900 L860 900 L820 600 L780 600 Z" fill="#2c3048"/>'
    b += f'<path d="M0 620 Q400 560 800 600 T1600 580 L1600 640 L0 660 Z" fill="#161a28"/>' + lamp(1100, 420, 220)
    b += person(790, 640, .5, "#0d0f17", bundle=True)
    b += "".join(f'<ellipse cx="{r.randint(300,1500)}" cy="{r.randint(640,880)}" rx="13" ry="5" fill="#a85a2a" opacity=".7" transform="rotate({r.randint(0,180)} 800 780)"/>' for _ in range(26))
    return svg(b, d)


# cover (square)
def cover():
    r = random.Random(3)
    d, b = sky("#161a2b", "#3a3e5e", 3000, 3000)
    b += stars(r, 90, 3000, 1100)
    b += building(0, 1000, 1500, DBRICK, 0, (), 3) .replace('width="46" height="70"', 'width="90" height="130"') if False else ""
    b += f'<rect y="1650" width="3000" height="1350" fill="#10131d"/>'
    b += f'<rect x="0" y="1500" width="1020" height="1500" fill="{DBRICK}"/><rect x="1980" y="1450" width="1020" height="1550" fill="{BRICK}"/>'
    for i in range(3):
        for j in range(3):
            b += win(110 + j * 300, 1580 + i * 420, 130, 210, (i, j) in ((1, 1),), False).replace("stroke-width=\"5\"", "stroke-width=\"9\"")
            b += win(2090 + j * 300, 1560 + i * 420, 130, 210, (i, j) in ((0, 2), (2, 0)), False).replace("stroke-width=\"5\"", "stroke-width=\"9\"")
    b += win(1200, 1850, 600, 800, True, True).replace('stroke-width="5"', 'stroke-width="14"').replace('stroke-width="4"', 'stroke-width="10"')
    b += f'<rect x="1160" y="2640" width="680" height="50" fill="#2a1d1a"/><circle cx="1360" cy="2580" r="60" fill="{RED}"/><circle cx="1470" cy="2560" r="50" fill="{RED}"/><circle cx="1280" cy="2610" r="44" fill="{RED}"/><path d="M1400 2640 q-30 -90 -40 -130 M1420 2640 q40 -80 70 -120 M1380 2640 q-70 -50 -100 -80" stroke="{LEAF}" stroke-width="16" fill="none"/>'
    b += (f'<text x="1500" y="360" text-anchor="middle" font-family="Georgia, serif" font-size="92" letter-spacing="30" fill="#e3c27a">FYODOR DOSTOEVSKY</text>'
          f'<text x="1500" y="760" text-anchor="middle" font-family="Georgia, serif" font-weight="bold" font-size="330" fill="{PAPER}">Poor Folk</text>'
          f'<rect x="1200" y="880" width="600" height="8" fill="#e3c27a"/><rect x="1330" y="910" width="340" height="5" fill="#e3c27a"/>')
    return svg(b, d, 3000, 3000)


def cover_ru():
    s = cover()
    s = s.replace("FYODOR DOSTOEVSKY", "ФЁДОР ДОСТОЕВСКИЙ").replace(">Poor Folk<", ">Бедные люди<").replace('font-size="330"', 'font-size="300"')
    return s


FILES = {"1_window": a1, "2_canal": a2, "3_notebook": a3, "4_island": a4, "5_whitenight": a5, "6_office": a6, "7_rain": a7, "8_autumn": a8, "9_road": a9, "cover": cover, "cover_ru": cover_ru}
if __name__ == "__main__":
    for name, fn in FILES.items():
        open(f"{OUT}/{name}.svg", "w", encoding="utf-8").write(fn()); print("wrote", name)
