#!/usr/bin/env python3
"""Illustrations and cover for "The Wonderful Doctor" as SVG. Palette: Kiev Christmas-night blue, shop-window gold, cellar brown, snow white."""
import random, math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "poor-folk"))
import make_art as _pf          # poor-folk's helpers (svg, sky, stars, win, person ...)
from make_art2 import candle, glow, paper, table
svg, sky, stars, win, lamp, person = _pf.svg, _pf.sky, _pf.stars, _pf.win, _pf.lamp, _pf.person
from make_art2 import DWOOD
PAPER, GOLD, RED, LEAF = _pf.PAPER, _pf.GOLD, _pf.RED, _pf.LEAF
OUT = "art"; os.makedirs(OUT, exist_ok=True)
SNOW = "#e8eefc"


def R(s): return random.Random(s)


def flakes(r, n, w=1600, h=900, op=.8): return "".join(f'<circle cx="{r.randint(0,w)}" cy="{r.randint(0,h)}" r="{r.uniform(2,5):.1f}" fill="#fff" opacity="{op}"/>' for _ in range(n))


def boy(x, y, s=1.0, col="#0e0d14"):
    return f'<g transform="translate({x} {y}) scale({s})" fill="{col}"><circle cx="0" cy="-112" r="16"/><path d="M-22 -94 Q0 -106 22 -94 L28 -26 L-28 -26 Z"/><rect x="-18" y="-28" width="13" height="46"/><rect x="5" y="-28" width="13" height="46"/><path d="M-22 -94 L-34 -50 L-24 -48 Z"/><path d="M22 -94 L34 -50 L24 -48 Z"/></g>'


# 1 -- the delicatessen window: lit goods, a piglet, two small boys in the snow looking in
def a1():
    r = R(1); d, b = sky("#1c2030", "#3a3a52")
    b += '<rect y="740" width="1600" height="160" fill="#d0d8ec"/>'
    b += f'<rect x="440" y="110" width="1080" height="630" fill="#2a2018"/><rect x="460" y="130" width="1040" height="590" fill="{GOLD}" opacity=".5"/><rect x="460" y="130" width="1040" height="590" fill="#f0c860" opacity=".25"/>'
    # shelves
    b += '<rect x="460" y="330" width="1040" height="14" fill="#6a4a32"/><rect x="460" y="520" width="1040" height="14" fill="#6a4a32"/>'
    # orange pyramid
    for row, n in enumerate((6, 5, 4, 3, 2)):
        for k in range(n):
            x = 560 + k * 56 + row * 28; y = 312 - row * 44
            b += f'<circle cx="{x}" cy="{y}" r="27" fill="{"#e8832e" if (k+row)%2 else "#f0a040"}"/>'
    # tangerines in paper
    b += "".join(f'<circle cx="{x}" cy="{y}" r="22" fill="#f0b040"/><path d="M{x-14} {y-18} l14 -10 l14 10 z" fill="#f1e6cc"/>' for x, y in ((960, 306), (1010, 306), (985, 262), (1060, 306), (1110, 306), (1085, 262)))
    # fish on a platter
    b += '<ellipse cx="1330" cy="300" rx="130" ry="22" fill="#cfd0d8"/><path d="M1220 280 Q1330 220 1440 280 Q1330 316 1220 280 Z" fill="#8a7a6a"/><circle cx="1240" cy="276" r="7" fill="#f1e6cc"/><path d="M1440 280 l40 -26 l0 52 z" fill="#8a7a6a"/>'
    # sausage garlands
    b += '<path d="M480 360 Q640 440 800 360 Q960 440 1120 360 Q1280 440 1480 360" stroke="#a8503a" stroke-width="22" fill="none" stroke-linecap="round" stroke-dasharray="46 6"/>'
    # hams
    b += "".join(f'<ellipse cx="{x}" cy="{y}" rx="82" ry="52" fill="#d88a7a"/><ellipse cx="{x}" cy="{y}" rx="60" ry="34" fill="#e8a898"/><rect x="{x-82}" y="{y+30}" width="164" height="20" fill="#f1e6cc"/>' for x, y in ((620, 650), (840, 660)))
    # piglet with grass
    b += '<ellipse cx="1160" cy="640" rx="140" ry="62" fill="#e8b0a0"/><circle cx="1290" cy="620" r="46" fill="#eebcaa"/><path d="M1270 580 l-8 -34 l30 18 z M1310 584 l14 -34 l8 40 z" fill="#d89c8c"/><circle cx="1296" cy="610" r="6" fill="#2a1c16"/><ellipse cx="1330" cy="636" rx="18" ry="13" fill="#d88a7a"/><path d="M1318 650 q10 10 22 -4" stroke="#3a2a22" stroke-width="3" fill="none"/><path d="M1326 650 l-10 22 M1334 650 l4 26 M1342 648 l12 18" stroke="#5c7048" stroke-width="4"/><rect x="1040" y="690" width="60" height="30" fill="#e8b0a0"/><rect x="1200" y="690" width="60" height="30" fill="#e8b0a0"/>'
    b += '<rect x="440" y="110" width="1080" height="630" fill="none" stroke="#10101a" stroke-width="24"/><line x1="980" y1="110" x2="980" y2="740" stroke="#10101a" stroke-width="12"/>'
    b += lamp(1560, 420, 330, True) + boy(300, 840, 1.7) + boy(180, 850, 1.3) + flakes(r, 130, op=.8)
    return svg(b, d)


# 2 -- the cellar: a candle, sick girl in bed, a cradle on the ceiling, a rope of wet rags, two boys at the table, snow in a high window
def a2():
    d, b = sky("#1e1814", "#2e2420")
    b += f'<rect y="620" width="1600" height="280" fill="#1a1410"/><rect x="0" y="0" width="1600" height="40" fill="#14100e"/>'
    b += '<rect x="1000" y="70" width="320" height="130" fill="#2a3148"/><rect x="1000" y="70" width="320" height="130" fill="none" stroke="#14100e" stroke-width="12"/><line x1="1160" y1="70" x2="1160" y2="200" stroke="#14100e" stroke-width="8"/>' + flakes(R(2), 14, 320, 130, .9).replace('cx="', 'cx="').replace('<circle', '<circle transform="translate(1000 70)"')
    b += '<path d="M0 230 Q400 290 800 250 T1600 270" stroke="#4a3a30" stroke-width="5" fill="none"/>' + "".join(f'<path d="M{x} {252+int(30*math.sin(x/260))} v{h} h-44 v-{h} z" fill="{c}" opacity=".8"/>' for x, h, c in ((300, 100, "#6a5a50"), (520, 130, "#8a7a6a"), (700, 90, "#5a4a44"), (1250, 110, "#7a6a5c")))
    # bed with girl
    b += f'<rect x="90" y="520" width="560" height="60" fill="#4a3a30"/><rect x="110" y="580" width="22" height="140" fill="{DWOOD}"/><rect x="610" y="580" width="22" height="140" fill="{DWOOD}"/><rect x="110" y="480" width="520" height="50" rx="22" fill="#8a7a70"/><rect x="130" y="440" width="150" height="60" rx="26" fill="#a89a8a"/><circle cx="220" cy="470" r="38" fill="#e8c8a8"/><circle cx="220" cy="470" r="38" fill="#d86a5a" opacity=".3"/><path d="M180 450 q40 -34 80 0" fill="#3a2a22"/><rect x="300" y="500" width="320" height="38" rx="16" fill="#6a5a4a"/>'
    # cradle hung from ceiling
    b += f'<line x1="760" y1="40" x2="740" y2="400" stroke="#4a3a30" stroke-width="4"/><line x1="940" y1="40" x2="960" y2="400" stroke="#4a3a30" stroke-width="4"/><path d="M730 400 H970 Q960 470 850 470 Q740 470 730 400 Z" fill="#6a4a32"/><ellipse cx="850" cy="396" rx="108" ry="18" fill="#e8d8c0"/><circle cx="850" cy="388" r="28" fill="#e8c8a8"/>'
    # mother kneeling
    b += '<g fill="#14100e"><circle cx="440" cy="400" r="34"/><path d="M400 440 Q440 420 480 440 L520 640 L350 650 Z"/><rect x="360" y="630" width="180" height="26" rx="12"/></g><path d="M406 392 q34 -44 70 0" fill="#3a2a22"/>'
    # table, candle, boys
    b += table(660, 780, 1420, "#5a3a2c") + glow(1060, 520, 460, .3) + candle(1060, 660, 80) + '<ellipse cx="1260" cy="650" rx="50" ry="14" fill="#cfd0d8"/>'
    b += boy(930, 840, 1.15, "#0a0808") + boy(1200, 850, 1.0, "#0a0808")
    return svg(b, d)


# 3 -- the snowy garden at night: a bench in an avenue of lime trees, a dark slumped man, an old man with a cigar
def a3():
    r = R(3); d, b = sky("#10163a", "#2c3258")
    b += stars(r, 90, 1600, 360) + '<rect y="640" width="1600" height="260" fill="#dfe6f6"/><path d="M0 700 Q800 640 1600 700 L1600 900 L0 900 Z" fill="#c8d2e8"/><polygon points="660,900 940,900 820,630 780,630" fill="#b4c0dc" opacity=".6"/>'
    for side in (-1, 1):
        for k in range(5):
            s = 1.0 - k * .17; x = 800 + side * (330 + k * 90) * (1 if k else 1) - (0 if k else 0)
            x = 800 + side * (260 + k * 130 * s); h = 520 * s; y = 700 - k * 18
            b += f'<rect x="{x-16*s}" y="{y-h*.5}" width="{32*s}" height="{h*.5}" fill="#2a2630"/>'
            for dx, dy, rr in ((-1, .5, 90), (1, .55, 90), (0, .82, 110), (-.6, .72, 80), (.6, .74, 80)):
                b += f'<ellipse cx="{x+dx*70*s}" cy="{y-h*dy}" rx="{rr*s}" ry="{rr*.55*s}" fill="#eef2fc" opacity=".92"/>'
            b += f'<path d="M{x-90*s} {y-h*.55} q{90*s} {-60*s} {180*s} 0" stroke="#2a2630" stroke-width="{8*s}" fill="none"/>'
    # bench
    b += '<rect x="560" y="690" width="480" height="18" fill="#4a3a32"/><rect x="560" y="640" width="480" height="14" fill="#4a3a32"/><rect x="560" y="664" width="480" height="12" fill="#4a3a32"/><rect x="580" y="708" width="16" height="70" fill="#2a2018"/><rect x="1004" y="708" width="16" height="70" fill="#2a2018"/><rect x="560" y="680" width="480" height="8" fill="#e8eefc"/>'
    # slumped man
    b += '<g fill="#0e0d14"><circle cx="680" cy="600" r="30"/><path d="M640 630 Q690 600 730 640 L740 700 L630 700 Z"/><rect x="650" y="696" width="30" height="60"/></g><path d="M650 586 h60 l-8 -16 h-44 z" fill="#2a2630"/>'
    # old man with cigar
    b += '<g fill="#2a2430"><circle cx="930" cy="590" r="28"/><path d="M886 620 Q934 596 984 620 L996 706 L880 706 Z"/><rect x="896" y="700" width="30" height="64"/><rect x="940" y="700" width="30" height="64"/></g><path d="M900 570 q30 -40 62 0 z" fill="#14121a"/><path d="M906 606 q4 14 14 12 M956 606 q-4 14 -14 12" stroke="#cfd0d8" stroke-width="6" fill="none"/><rect x="858" y="600" width="26" height="6" fill="#d8c8a8"/><circle cx="856" cy="603" r="7" fill="#e8632e"/><circle cx="856" cy="603" r="22" fill="#e8632e" opacity=".3"/><rect x="990" y="650" width="46" height="38" fill="#c8a870"/><rect x="1004" y="670" width="40" height="30" fill="#a8503a"/>'
    b += lamp(380, 380, 330, True) + flakes(r, 110, op=.7)
    return svg(b, d)


# 4 -- the doctor in the cellar: a warm stove, a doctor writing at the table, samovar, a father, the boys at work
def a4():
    r = R(4); d, b = sky("#1e1814", "#33281f")
    b += '<rect y="640" width="1600" height="260" fill="#1a1410"/>'
    # stove
    b += f'<rect x="90" y="360" width="320" height="300" fill="#6a4a3a"/><rect x="90" y="340" width="320" height="30" fill="#4a3228"/><rect x="150" y="460" width="150" height="130" rx="10" fill="#14100e"/><rect x="170" y="490" width="110" height="80" fill="#f08a3a"/><rect x="190" y="520" width="70" height="50" fill="#f8c860"/>' + glow(230, 540, 520, .34)
    b += '<rect x="260" y="640" width="150" height="24" fill="#4a3228"/><rect x="290" y="620" width="14" height="30" fill="#4a3228"/><rect x="316" y="610" width="14" height="40" fill="#4a3228"/>'
    # table
    b += table(600, 540, 1360, "#6a4a32")
    # samovar
    b += '<g><rect x="1120" y="470" width="120" height="14" rx="6" fill="#c8a040"/><path d="M1130 484 Q1090 540 1130 600 H1230 Q1270 540 1230 484 Z" fill="#d8b050"/><rect x="1166" y="440" width="28" height="34" fill="#a88030"/><path d="M1100 530 q-40 -10 -30 -50" stroke="#c8a040" stroke-width="8" fill="none"/><path d="M1180 420 q-18 -40 10 -70 q22 -30 -4 -70" stroke="#cfd0e6" stroke-width="10" fill="none" opacity=".4"/></g>'
    # doctor seated writing
    b += '<g fill="#2a2430"><path d="M700 380 Q760 340 820 380 L840 600 L690 600 Z"/></g><circle cx="760" cy="326" r="38" fill="#e8c8a8"/><path d="M722 316 q38 -50 76 0 q-4 -20 -38 -22 q-34 2 -38 22" fill="#e8e0d0"/><path d="M726 340 q-14 24 6 34 M794 340 q14 24 -6 34" stroke="#e8e0d0" stroke-width="12" fill="none" stroke-linecap="round"/><path d="M790 430 L880 560" stroke="#2a2430" stroke-width="30" stroke-linecap="round"/>' + paper(900, 604, 130, 8, -4) + '<ellipse cx="640" cy="600" rx="40" ry="8" fill="#cfd0d8"/>'
    # father standing with bundle, mother at the bed (left-back)
    b += '<g fill="#0e0d14"><circle cx="1400" cy="430" r="34"/><path d="M1350 468 Q1400 444 1450 468 L1470 700 L1330 700 Z"/><rect x="1350" y="696" width="40" height="110"/><rect x="1410" y="696" width="40" height="110"/></g><rect x="1290" y="560" width="60" height="50" fill="#e8d8c0"/><circle cx="1320" cy="550" r="18" fill="#a8503a"/>'
    b += boy(470, 850, 1.25, "#0a0808") + boy(1000, 860, 1.1, "#0a0808")
    return svg(b, d)


# 5 -- the saucer: banknotes under the tea saucer, the prescription bottle, a candle, the cellar door left ajar to the dark corridor
def a5():
    d, b = sky("#161018", "#2a1e20")
    b += '<rect y="660" width="1600" height="240" fill="#1a1210"/>'
    b += '<rect x="1060" y="120" width="360" height="560" fill="#0a0808"/><path d="M1060 120 L1000 160 L1000 700 L1060 680 Z" fill="#3a2a22"/><polygon points="1060,680 1420,680 1420,740 1000,740" fill="#14100e"/><path d="M1060 140 H1420 V680 H1060 Z" fill="#14100e"/><polygon points="1110,680 1370,680 1410,740 1070,740" fill="#8a6a40" opacity=".25"/>'
    b += '<g fill="#2a2430" opacity=".9"><circle cx="1200" cy="360" r="30"/><path d="M1160 392 Q1200 372 1240 392 L1252 620 L1148 620 Z"/></g><circle cx="1196" cy="350" r="16" fill="#e8e0d0" opacity=".12"/>'
    b += table(640, 120, 1000, "#6a4a32") + glow(520, 480, 520, .34) + candle(250, 640, 90)
    # saucer & notes
    b += '<ellipse cx="560" cy="632" rx="150" ry="26" fill="#e8e0d0"/><ellipse cx="560" cy="624" rx="118" ry="18" fill="#f4eee0"/><path d="M470 624 h-40" stroke="#e8e0d0" stroke-width="2"/>'
    b += '<g transform="rotate(-6 560 600)"><rect x="440" y="602" width="150" height="38" fill="#7a9a6a"/><rect x="450" y="610" width="130" height="6" fill="#5c7048"/></g><g transform="rotate(5 600 600)"><rect x="520" y="596" width="150" height="40" fill="#c8a050"/><rect x="530" y="606" width="130" height="6" fill="#a88030"/></g><g transform="rotate(-2 580 590)"><rect x="500" y="588" width="150" height="38" fill="#a8606a"/></g>'
    b += '<ellipse cx="560" cy="604" rx="136" ry="22" fill="#f4eee0"/><ellipse cx="560" cy="598" rx="104" ry="14" fill="#e8e0d0"/>'
    b += paper(800, 636, 120, 6, 4)
    # bottle with label
    b += '<rect x="852" y="500" width="76" height="140" rx="10" fill="#5a8a8a" opacity=".85"/><rect x="876" y="470" width="28" height="36" fill="#5a8a8a" opacity=".85"/><rect x="872" y="458" width="36" height="16" fill="#8a6a40"/><rect x="858" y="548" width="64" height="62" fill="#f1e6cc"/><rect x="866" y="558" width="48" height="5" fill="#8a7a6a"/><rect x="866" y="570" width="40" height="5" fill="#8a7a6a"/><rect x="866" y="582" width="48" height="5" fill="#8a7a6a"/>'
    return svg(b, d)


def cover(ru=False):
    r = R(8); d, b = sky("#10163a", "#2c3258", 3000, 3000)
    b += stars(r, 110, 3000, 1100) + '<rect y="2350" width="3000" height="650" fill="#e0e6f4"/><path d="M0 2480 Q1500 2330 3000 2480 L3000 3000 L0 3000 Z" fill="#c8d2e8"/>'
    for side in (-1, 1):
        for k in range(4):
            s = 1.0 - k * .2; x = 1500 + side * (560 + k * 260 * s); h = 1200 * s; y = 2500 - k * 40
            b += f'<rect x="{x-34*s}" y="{y-h*.5}" width="{68*s}" height="{h*.5}" fill="#2a2630"/>'
            for dx, dy, rr in ((-1, .5, 190), (1, .55, 190), (0, .82, 230), (-.6, .72, 170), (.6, .74, 170)):
                b += f'<ellipse cx="{x+dx*150*s}" cy="{y-h*dy}" rx="{rr*s}" ry="{rr*.55*s}" fill="#eef2fc" opacity=".92"/>'
    # bench with two figures and a lamp
    b += '<rect x="1130" y="2470" width="740" height="26" fill="#4a3a32"/><rect x="1130" y="2400" width="740" height="20" fill="#4a3a32"/><rect x="1150" y="2496" width="24" height="120" fill="#2a2018"/><rect x="1826" y="2496" width="24" height="120" fill="#2a2018"/>'
    b += '<g fill="#0e0d14"><circle cx="1260" cy="2290" r="52"/><path d="M1190 2340 Q1260 2300 1330 2350 L1350 2470 L1180 2470 Z"/></g><g fill="#2a2430"><circle cx="1630" cy="2270" r="48"/><path d="M1560 2320 Q1630 2290 1700 2320 L1720 2470 L1550 2470 Z"/></g><path d="M1590 2236 q40 -56 82 0 z" fill="#14121a"/><circle cx="1520" cy="2290" r="11" fill="#e8632e"/><circle cx="1520" cy="2290" r="38" fill="#e8632e" opacity=".3"/>'
    b += f'<rect x="2440" y="1640" width="12" height="860" fill="#10131d"/><circle cx="2446" cy="1620" r="260" fill="{GOLD}" opacity=".14"/><circle cx="2446" cy="1620" r="120" fill="{GOLD}" opacity=".22"/><rect x="2410" y="1580" width="72" height="70" rx="10" fill="{GOLD}"/><rect x="2400" y="1560" width="92" height="20" fill="#10131d"/>'
    b += "".join(f'<circle cx="{r.randint(0,3000)}" cy="{r.randint(1200,3000)}" r="{r.uniform(4,9):.1f}" fill="#fff" opacity=".8"/>' for _ in range(170))
    T = ("АЛЕКСАНДР КУПРИН", "Чудесный", "доктор") if ru else ("ALEXANDER KUPRIN", "The Wonderful", "Doctor")
    b += (f'<text x="1500" y="340" text-anchor="middle" font-family="Georgia, serif" font-size="92" letter-spacing="30" fill="#e3c27a">{T[0]}</text>'
          f'<text x="1500" y="690" text-anchor="middle" font-family="Georgia, serif" font-weight="bold" font-size="290" fill="{PAPER}">{T[1]}</text>'
          f'<text x="1500" y="990" text-anchor="middle" font-family="Georgia, serif" font-weight="bold" font-size="290" fill="{PAPER}">{T[2]}</text>'
          f'<rect x="1200" y="1110" width="600" height="8" fill="#e3c27a"/><rect x="1330" y="1140" width="340" height="5" fill="#e3c27a"/>')
    return svg(b, d, 3000, 3000)


FILES = {"1_shop_window": a1, "2_cellar": a2, "3_garden": a3, "4_doctor": a4, "5_saucer": a5, "cover": cover, "cover_ru": lambda: cover(True)}
if __name__ == "__main__":
    for n, fn in FILES.items():
        open(f"{OUT}/{n}.svg", "w", encoding="utf-8").write(fn()); print("wrote", n)
