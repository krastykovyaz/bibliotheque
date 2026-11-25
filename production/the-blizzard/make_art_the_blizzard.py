#!/usr/bin/env python3
"""Illustrations and cover for "The Blizzard" as SVG. Palette: winter-night blue, lamp and candle gold, snow white, one warm church window."""
import random, math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "poor-folk"))
import make_art as _pf
from make_art2 import candle, glow, paper, DWOOD, WOOD
svg, sky, stars, win, lamp, person = _pf.svg, _pf.sky, _pf.stars, _pf.win, _pf.lamp, _pf.person
PAPER, GOLD, RED, LEAF = _pf.PAPER, _pf.GOLD, _pf.RED, _pf.LEAF
OUT = "art"; os.makedirs(OUT, exist_ok=True)
SNOW = "#e8eefc"


def R(s): return random.Random(s)


def flakes(r, n, w=1600, h=900, op=.8, big=5): return "".join(f'<circle cx="{r.randint(0,w)}" cy="{r.randint(0,h)}" r="{r.uniform(2,big):.1f}" fill="#fff" opacity="{op}"/>' for _ in range(n))


def streaks(r, n, w=1600, h=900, op=.5): return "".join(f'<path d="M{(x:=r.randint(-100,w))} {(y:=r.randint(0,h))} q{r.randint(60,160)} {r.randint(-30,10)} {r.randint(200,380)} {r.randint(-10,40)}" stroke="#fff" stroke-width="{r.uniform(3,9):.1f}" fill="none" opacity="{op}" stroke-linecap="round"/>' for _ in range(n))


def pine(x, y, h, col="#1f3330", snow=True):
    s = f'<rect x="{x-7}" y="{y-30}" width="14" height="34" fill="#2a1c16"/>'
    for k in range(4):
        yy = y - 30 - h * .2 * k; w = h * .24 * (1 - k * .2)
        s += f'<polygon points="{x-w:.0f},{yy:.0f} {x},{yy-h*.34:.0f} {x+w:.0f},{yy:.0f}" fill="{col}"/>'
        if snow: s += f'<polygon points="{x-w*.8:.0f},{yy-6:.0f} {x},{yy-h*.34:.0f} {x+w*.8:.0f},{yy-6:.0f}" fill="{SNOW}" opacity=".5"/>'
    return s


def horse(x, y, s=1.0, col="#2a1c18", flip=1):
    return (f'<g transform="translate({x} {y}) scale({s*flip} {s})" fill="{col}"><ellipse cx="0" cy="-70" rx="75" ry="38"/><path d="M60 -90 L110 -150 L140 -140 L150 -115 L120 -108 L84 -62 Z"/>'
            f'<rect x="-62" y="-50" width="12" height="62"/><rect x="-36" y="-50" width="12" height="62"/><rect x="26" y="-50" width="12" height="62"/><rect x="52" y="-50" width="12" height="62"/><path d="M-72 -80 q-34 10 -30 50 q8 -30 30 -34 z"/><path d="M102 -148 l-8 -20 l14 6 z"/></g>')


def sleigh(x, y, s=1.0, col="#3a2420"):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M-110 0 q-30 -2 -30 -26" stroke="{col}" stroke-width="9" fill="none" stroke-linecap="round"/><path d="M-110 0 H110" stroke="{col}" stroke-width="9" stroke-linecap="round"/>'
            f'<path d="M-100 -12 L-86 -70 H80 L96 -12 Z" fill="#6a3a32"/><path d="M-100 -12 L-86 -70 H80 L96 -12 Z" fill="none" stroke="{col}" stroke-width="5"/><rect x="-86" y="-86" width="166" height="18" fill="#8a5a42"/></g>')


def cottage(x, y, w, h, lit=True, roof="#d8def0", wall="#4a3a38"):
    return (f'<rect x="{x}" y="{y-h}" width="{w}" height="{h}" fill="{wall}"/><polygon points="{x-18},{y-h+6} {x+w/2},{y-h-w*.28} {x+w+18},{y-h+6}" fill="{roof}"/>'
            + win(x + w * .15, y - h * .7, w * .22, h * .38, lit) + win(x + w * .6, y - h * .7, w * .22, h * .38, lit))


# 1 -- the pine grove and the old chapel: two small figures meeting in the winter dusk
def a1():
    r = R(1); d, b = sky("#3a4a78", "#e0b8a0")
    b += '<circle cx="1180" cy="280" r="54" fill="#fff0d0" opacity=".85"/><rect y="640" width="1600" height="260" fill="#e6ecf8"/><path d="M0 660 Q500 600 1000 660 T1600 640 L1600 720 L0 720 Z" fill="#cdd6ea"/>'
    b += "".join(pine(x, 660 + r.randint(0, 40), r.randint(280, 440)) for x in (60, 200, 340, 1250, 1400, 1530, 1100))
    b += f'<rect x="640" y="470" width="220" height="190" fill="#6a4a3a"/><polygon points="620,480 750,380 880,480" fill="{SNOW}"/><rect x="738" y="330" width="24" height="64" fill="{SNOW}"/><rect x="724" y="344" width="52" height="10" fill="{SNOW}"/><path d="M700 660 V560 q50 -50 100 0 V660 Z" fill="#2a1c16"/>'
    b += person(540, 780, 1.1, "#1a1624") + person(600, 786, 1.0, "#8a3a3a") + flakes(r, 70, op=.55)
    return svg(b, d)


# 2 -- the night of the flight: the dark house, a lit window, a sleigh and horses waiting in the storm
def a2():
    r = R(2); d, b = sky("#10163a", "#2e3858")
    b += '<rect y="660" width="1600" height="240" fill="#cfd8ec"/>' + cottage(120, 680, 520, 280, False, "#dfe6f6", "#3a2e34")
    b += win(260, 520, 90, 110, True) + f'<rect x="480" y="560" width="70" height="120" fill="#241a1c"/>'
    b += f'<g fill="#0e0d14"><circle cx="760" cy="640" r="20"/><path d="M732 668 Q760 650 788 668 L796 760 L724 764 Z"/></g>' + person(830, 764, .95, "#2a2438")
    b += horse(1130, 790, .95, "#2a1c18") + horse(1280, 800, .95, "#34221c") + sleigh(1030, 800, 1.0) + person(960, 740, .85, "#14121c")
    b += pine(1500, 700, 360, "#162624") + streaks(r, 30, op=.45) + flakes(r, 110, op=.8)
    return svg(b, d)


# 3 -- lost in the field: a small sleigh and one horse in the swirling white, a dark grove far away
def a3():
    r = R(3); d, b = sky("#9a9a8c", "#d8d4c4")
    b += '<rect y="560" width="1600" height="340" fill="#eef0f4"/><path d="M0 600 Q300 540 600 600 T1200 580 T1600 610 L1600 700 L0 700 Z" fill="#d6dae6"/>'
    b += "".join(pine(x, 580, 200, "#4a5a54") for x in (1150, 1210, 1280, 1340)) + '<rect x="1130" y="540" width="260" height="30" fill="#e8ecf2" opacity=".7"/>'
    b += horse(560, 780, 1.1, "#2a1c18") + sleigh(380, 790, 1.0) + person(360, 706, .8, "#14121c")
    b += f'<path d="M560 700 q-60 -40 -120 -10" stroke="#2a1c18" stroke-width="4" fill="none"/>'
    b += streaks(r, 70, op=.7) + flakes(r, 140, op=.85, big=7) + '<rect width="1600" height="900" fill="#e8e8e0" opacity=".18"/>'
    return svg(b, d)


# 4 -- the fever: a sickroom by candlelight, a bed, a mother keeping watch
def a4():
    d, b = sky("#1c1820", "#2a2230")
    b += '<rect y="680" width="1600" height="220" fill="#1c1418"/>' + win(1180, 200, 220, 280, False)
    b += f'<rect x="300" y="520" width="640" height="200" fill="#6a3a3a"/><rect x="300" y="470" width="640" height="60" rx="26" fill="{PAPER}"/><rect x="280" y="420" width="30" height="300" fill="{DWOOD}"/><rect x="930" y="460" width="30" height="260" fill="{DWOOD}"/><ellipse cx="400" cy="470" rx="46" ry="28" fill="#e8d4c0"/><path d="M360 440 q40 -60 90 -10 q-30 40 -90 10" fill="#3a2418"/>'
    b += f'<rect x="1000" y="560" width="200" height="30" fill="{WOOD}"/><rect x="1020" y="590" width="20" height="130" fill="{DWOOD}"/><rect x="1160" y="590" width="20" height="130" fill="{DWOOD}"/>' + candle(1100, 560, 90) + glow(1100, 440, 460, .3)
    b += person(1010, 820, 1.25, "#2a2230") + f'<rect x="1075" y="760" width="40" height="16" fill="#a8a09a"/>' if False else person(1010, 820, 1.25, "#2a2230")
    b += paper(1000, 560, 120, 10, 0)
    return svg(b, d)


# 5 -- the return of the regiments: riders and a banner on a country road, villagers waving
def a5():
    r = R(5); d, b = sky("#6a82b0", "#f0d8b0")
    b += '<rect y="600" width="1600" height="300" fill="#8a9a58"/><path d="M0 640 Q500 600 900 650 T1600 620 L1600 700 L0 700 Z" fill="#7a8a4c"/><path d="M0 760 Q800 690 1600 780 L1600 900 L0 900 Z" fill="#b8a07a"/>'
    b += cottage(1150, 640, 300, 150, True, "#a88a6a", "#7a5a4a") + cottage(60, 650, 260, 130, True, "#a88a6a", "#7a5a4a")
    for i, x in enumerate((420, 560, 700, 840)):
        b += horse(x, 800, .75, "#3a2a22" if i % 2 else "#2a1c18") + f'<g fill="#243a5a"><circle cx="{x+6}" cy="{800-170}" r="16"/><path d="M{x-16} {800-150} Q{x+6} {800-166} {x+28} {800-150} L{x+30} {800-92} L{x-18} {800-92} Z"/></g><rect x="{x}" y="{800-190}" width="26" height="14" fill="#c8a040"/>'
    b += f'<rect x="498" y="440" width="6" height="250" fill="#3a2a22"/><path d="M504 446 h110 l-24 30 l24 30 h-110 z" fill="#c4432e"/>'
    b += person(1020, 800, .9, "#6a3a3a") + person(1090, 810, .8, "#3a4a6a") + "".join(f'<ellipse cx="{x}" cy="{y}" rx="14" ry="8" fill="{PAPER}" transform="rotate({a} {x} {y})"/>' for x, y, a in ((980, 580, 20), (1060, 540, -30), (1130, 600, 10), (1010, 500, 40)))
    b += "".join(f'<ellipse cx="{r.randint(0,1600)}" cy="{r.randint(120,420)}" rx="{r.randint(60,130)}" ry="22" fill="#fff" opacity=".35"/>' for _ in range(6))
    return svg(b, d)


# 6 -- the garden pond: a willow, a girl in a white dress with a book, a hussar standing near
def a6():
    r = R(6); d, b = sky("#a8c0d8", "#f0e4c8")
    b += '<rect y="560" width="1600" height="340" fill="#7a8e50"/><ellipse cx="700" cy="760" rx="520" ry="110" fill="#6a8aa8"/><ellipse cx="700" cy="760" rx="420" ry="70" fill="#8aa8c0" opacity=".6"/>'
    b += '<rect x="1040" y="300" width="36" height="360" fill="#3a2a22"/>' + "".join(f'<path d="M{1058+r.randint(-30,30)} {320+r.randint(0,40)} q{r.randint(-120,120)} {r.randint(120,260)} {r.randint(-80,80)} {r.randint(300,420)}" stroke="#8aa04a" stroke-width="{r.randint(8,14)}" fill="none" opacity=".85"/>' for _ in range(34))
    b += f'<g><circle cx="1180" cy="580" r="18" fill="#e8d4c0"/><path d="M1150 604 Q1180 590 1210 604 L1250 740 L1110 740 Z" fill="{PAPER}"/><path d="M1160 560 q20 -30 44 0" fill="#3a2418"/><rect x="1196" y="640" width="46" height="30" fill="#6a3a32"/></g>'
    b += person(1360, 780, 1.1, "#243a5a") + f'<rect x="1340" y="630" width="40" height="10" fill="#c8a040"/>'
    b += "".join(f'<ellipse cx="{r.randint(80,1500)}" cy="{r.randint(100,500)}" rx="10" ry="6" fill="#d8a040" transform="rotate({r.randint(0,180)} 0 0)" opacity=".8"/>' for _ in range(18))
    return svg(b, d)


# 7 -- the wooden church in the storm: lit windows, sleighs at the fence, people on the porch
def a7():
    r = R(7); d, b = sky("#10163a", "#2c3258")
    b += '<rect y="640" width="1600" height="260" fill="#dce2f0"/>'
    b += f'<rect x="560" y="360" width="480" height="300" fill="#6a4a3a"/><polygon points="530,380 800,230 1070,380" fill="{SNOW}"/><rect x="780" y="140" width="40" height="110" fill="#6a4a3a"/><polygon points="770,150 800,70 830,150" fill="{SNOW}"/><rect x="792" y="30" width="16" height="50" fill="{GOLD}"/><rect x="780" y="42" width="40" height="8" fill="{GOLD}"/>'
    b += win(620, 430, 90, 150, True).replace(GOLD, "#e8a040") + win(890, 430, 90, 150, True).replace(GOLD, "#e8a040") + f'<path d="M760 660 V540 q40 -50 80 0 V660 Z" fill="#f0c060"/>' + glow(800, 560, 520, .1)
    b += "".join(f'<rect x="{x}" y="640" width="8" height="70" fill="#2a1c16"/>' for x in range(100, 560, 60)) + '<rect x="100" y="650" width="460" height="8" fill="#2a1c16"/>'
    b += sleigh(250, 780, 1.0) + horse(430, 790, .9) + sleigh(1250, 790, .9) + horse(1400, 800, .85, "#34221c")
    b += person(700, 790, .9, "#14121c") + person(900, 800, .9, "#2a2230") + person(950, 804, .8, "#8a3a3a")
    b += streaks(r, 36, op=.45) + flakes(r, 110, op=.8)
    return svg(b, d)


def cover(ru=False):
    r = R(9); d, b = sky("#10163a", "#2c3258", 3000, 3000)
    b += stars(r, 70, 3000, 800) + '<rect y="2400" width="3000" height="600" fill="#dce2f0"/>'
    b += '<g transform="translate(1500 2420) scale(.78) translate(-1500 -2420)">'
    b += f'<rect x="950" y="1560" width="1100" height="860" fill="#6a4a3a"/><polygon points="890,1580 1500,1180 2110,1580" fill="{SNOW}"/><rect x="1470" y="960" width="60" height="240" fill="#6a4a3a"/><polygon points="1450,980 1500,860 1550,980" fill="{SNOW}"/><rect x="1488" y="760" width="24" height="120" fill="{GOLD}"/><rect x="1458" y="790" width="84" height="18" fill="{GOLD}"/>'
    b += win(1040, 1700, 220, 340, True).replace(GOLD, "#e8a040").replace('stroke-width="5"', 'stroke-width="12"').replace('stroke-width="4"', 'stroke-width="9"') + win(1740, 1700, 220, 340, True).replace(GOLD, "#e8a040").replace('stroke-width="5"', 'stroke-width="12"').replace('stroke-width="4"', 'stroke-width="9"')
    b += f'<path d="M1400 2420 V2100 q100 -110 200 0 V2420 Z" fill="#f0c060"/>' + glow(1500, 2000, 1000, .1)
    b += '</g>'
    b += f'<g transform="translate(1450 2640) scale(2.2)"><g transform="translate(-60 0)">{horse(0, 0, 1.0)}</g><g transform="translate(-300 0)">{sleigh(0, 0, 1.0)}</g></g>'
    b += "".join(f'<path d="M{(x:=r.randint(-100,2900))} {(y:=r.randint(900,2900))} q{r.randint(100,260)} {r.randint(-60,20)} {r.randint(400,800)} {r.randint(-20,60)}" stroke="#fff" stroke-width="{r.uniform(6,16):.1f}" fill="none" opacity=".4" stroke-linecap="round"/>' for _ in range(34))
    b += "".join(f'<circle cx="{r.randint(0,3000)}" cy="{r.randint(900,3000)}" r="{r.uniform(5,12):.1f}" fill="#fff" opacity=".8"/>' for _ in range(220))
    T = ("АЛЕКСАНДР ПУШКИН", "Метель") if ru else ("ALEXANDER PUSHKIN", "The Blizzard")
    fs = 330 if ru else 270
    b += (f'<text x="1500" y="380" text-anchor="middle" font-family="Georgia, serif" font-size="92" letter-spacing="30" fill="#e3c27a">{T[0]}</text>'
          f'<text x="1500" y="740" text-anchor="middle" font-family="Georgia, serif" font-weight="bold" font-size="{fs}" fill="{PAPER}">{T[1]}</text>'
          f'<rect x="1200" y="860" width="600" height="8" fill="#e3c27a"/><rect x="1330" y="890" width="340" height="5" fill="#e3c27a"/>')
    return svg(b, d, 3000, 3000)


FILES = {"1_chapel": a1, "2_flight": a2, "3_field": a3, "4_sickroom": a4, "5_regiments": a5, "6_pond": a6, "7_church": a7, "cover": cover, "cover_ru": lambda: cover(True)}
if __name__ == "__main__":
    for n, fn in FILES.items():
        open(f"{OUT}/{n}.svg", "w", encoding="utf-8").write(fn()); print("wrote", n)
