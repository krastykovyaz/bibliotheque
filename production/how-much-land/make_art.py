#!/usr/bin/env python3
"""Draws the illustrations and the cover for "How Much Land Does a Man Need?" as SVG.
One palette throughout: indigo night, ochre feather-grass, rust and sunset orange, cream.
No known characters, no copies of existing paintings or covers."""
import random, math, os

OUT = "art"
os.makedirs(OUT, exist_ok=True)

INDIGO, DEEP = "#1d2340", "#2b3158"
OCHRE, STRAW, DRY = "#c79a4a", "#e3c27a", "#a8803a"
RUST, BRICK = "#9c4a2e", "#7a3322"
CREAM, GREEN = "#f4e8c8", "#5c6b4a"
ORANGE, RED = "#e07a3a", "#b8432b"


def svg(w, h, body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'<defs>{defs}</defs>{body}</svg>')


def grass(rnd, x0, x1, y0, y1, n, colors, length=(14, 34), lean=10, width=(1.4, 2.6)):
    """Many thin curved strokes: feather-grass."""
    out = []
    for _ in range(n):
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        l = rnd.uniform(*length) * (0.5 + 0.9 * (y - y0) / max(1, (y1 - y0)))
        d = rnd.uniform(-lean, lean)
        c = rnd.choice(colors)
        out.append(f'<path d="M{x:.0f} {y:.0f} q{d/2:.0f} {-l/2:.0f} {d:.0f} {-l:.0f}" stroke="{c}" '
                   f'stroke-width="{rnd.uniform(*width):.1f}" fill="none" stroke-linecap="round" opacity="0.85"/>')
    return "".join(out)


def stars(rnd, n, w, ymax):
    return "".join(f'<circle cx="{rnd.uniform(0,w):.0f}" cy="{rnd.uniform(0,ymax):.0f}" r="{rnd.uniform(1,2.8):.1f}" '
                   f'fill="{CREAM}" opacity="{rnd.uniform(0.4,0.95):.2f}"/>' for _ in range(n))


HORSE = ('<symbol id="horse" viewBox="0 0 120 90"><g fill="currentColor">'
         '<ellipse cx="58" cy="42" rx="34" ry="15"/><path d="M84 36 L104 14 L112 20 L96 46 Z"/>'
         '<path d="M104 14 L116 12 L118 22 L110 24 Z"/><path d="M26 38 C10 40 6 60 12 76 C16 66 22 56 30 50 Z"/>'
         '<rect x="34" y="50" width="5" height="32"/><rect x="46" y="52" width="5" height="30"/>'
         '<rect x="70" y="52" width="5" height="30"/><rect x="82" y="50" width="5" height="32"/></g></symbol>')


# ---------------------------------------------------------------- 1: the hut at night (parts I-II)
def art_hut():
    r = random.Random(1)
    defs = (f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#121733"/>'
            f'<stop offset="1" stop-color="#43406b"/></linearGradient>'
            f'<radialGradient id="glow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#f6cf78" stop-opacity="0.85"/>'
            f'<stop offset="1" stop-color="#f6cf78" stop-opacity="0"/></radialGradient>'
            f'<mask id="crescent"><rect width="1600" height="900" fill="#000"/><circle cx="1260" cy="170" r="48" fill="#fff"/><circle cx="1284" cy="156" r="44" fill="#000"/></mask>'
            f'<clipPath id="roof"><polygon points="430,528 680,372 930,528"/></clipPath>')
    b = f'<rect width="1600" height="900" fill="url(#sky)"/>' + stars(r, 70, 1600, 420)
    b += f'<rect width="1600" height="900" fill="{CREAM}" mask="url(#crescent)"/>'
    b += f'<path d="M0 560 C200 500 420 520 640 540 C900 560 1200 480 1600 520 L1600 900 L0 900 Z" fill="#2b2f58"/>'
    b += f'<path d="M0 640 C300 600 700 620 1000 610 C1250 600 1450 620 1600 630 L1600 900 L0 900 Z" fill="#232847"/>'
    b += f'<path d="M0 730 C400 700 900 720 1600 700 L1600 900 L0 900 Z" fill="#1b1f3a"/>'
    # light spilling from the window
    b += '<ellipse cx="640" cy="640" rx="260" ry="110" fill="url(#glow)"/>'
    b += '<polygon points="585,660 690,660 800,780 520,780" fill="#f6cf78" opacity="0.18"/>'
    # hut: logs, thatch, chimney
    b += f'<rect x="480" y="520" width="400" height="190" fill="#5a3a2c"/>'
    b += "".join(f'<rect x="480" y="{y}" width="400" height="3" fill="#3d261d"/>' for y in range(536, 710, 18))
    b += f'<polygon points="430,528 680,372 930,528" fill="#8a6a3a"/>'
    b += "".join(f'<path d="M{430+i*26} 528 L{680-(680-430-i*26)*0.0:.0f} 528" stroke="none"/>' for i in range(0))
    b += '<g clip-path="url(#roof)">' + "".join(f'<path d="M{x} 528 L{680+(x-680)*0.62:.0f} {400+abs(x-680)*0.06:.0f}" stroke="#6d522c" stroke-width="3" opacity="0.7"/>'
                 for x in range(450, 930, 30)) + '</g>'
    b += f'<rect x="770" y="396" width="48" height="90" fill="#4a3228"/><rect x="762" y="388" width="64" height="14" fill="#3a261f"/>'
    # smoke that curls into two small horns
    b += (f'<path d="M794 380 C770 330 830 300 800 250 C790 225 770 215 760 200" fill="none" stroke="#cfd0e6" '
          f'stroke-width="12" stroke-linecap="round" opacity="0.5"/>'
          f'<path d="M800 250 C830 235 845 212 838 190" fill="none" stroke="#cfd0e6" stroke-width="9" stroke-linecap="round" opacity="0.45"/>')
    # window and door
    b += f'<rect x="570" y="585" width="100" height="84" fill="#f6cf78"/><rect x="566" y="581" width="108" height="92" fill="none" stroke="#3a261f" stroke-width="8"/>'
    b += '<rect x="617" y="585" width="6" height="84" fill="#3a261f"/><rect x="570" y="623" width="100" height="6" fill="#3a261f"/>'
    b += f'<path d="M580 668 L580 640 Q600 624 612 640 L612 668 Z" fill="#a8602a" opacity="0.8"/>'  # stove glimpsed inside
    b += f'<rect x="740" y="590" width="64" height="120" fill="#2a1a14"/><circle cx="790" cy="652" r="4" fill="{STRAW}"/>'
    # fence and a bare birch
    b += "".join(f'<rect x="{x}" y="{650 + (x % 7)}" width="9" height="{70 - (x % 5)}" fill="#14172c"/>' for x in range(40, 430, 34))
    b += '<rect x="30" y="676" width="400" height="7" fill="#14172c"/>'
    b += f'<path d="M1190 720 L1196 380" stroke="#d9d4c8" stroke-width="14"/><path d="M1196 470 L1130 400 M1194 520 L1262 440 M1193 430 L1240 360 M1195 580 L1140 520" stroke="#d9d4c8" stroke-width="6" fill="none" stroke-linecap="round"/>'
    b += "".join(f'<rect x="{1186}" y="{y}" width="14" height="4" fill="#2a2a3a"/>' for y in range(430, 700, 38))
    return svg(1600, 900, b, defs)


# ---------------------------------------------------------------- 2: the long way, the Volga (parts III-IV)
def art_river():
    r = random.Random(2)
    defs = (f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8aa7b5"/>'
            f'<stop offset="0.7" stop-color="#f2d6a8"/><stop offset="1" stop-color="#eebb86"/></linearGradient>'
            f'<linearGradient id="water" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#86a9b4"/>'
            f'<stop offset="1" stop-color="#5f8493"/></linearGradient>'
            f'<radialGradient id="sun" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#fff3cf"/><stop offset="1" stop-color="#fff3cf" stop-opacity="0"/></radialGradient>')
    b = '<rect width="1600" height="900" fill="url(#sky)"/>'
    b += '<circle cx="330" cy="400" r="190" fill="url(#sun)"/><circle cx="330" cy="404" r="52" fill="#fff6dc"/>'
    b += '<path d="M0 470 C300 440 600 470 900 450 C1200 430 1400 460 1600 450 L1600 560 L0 560 Z" fill="#7d8f6c"/>'
    b += '<rect x="0" y="540" width="1600" height="120" fill="url(#water)"/>'
    b += "".join(f'<rect x="{r.uniform(0,1500):.0f}" y="{r.uniform(550,650):.0f}" width="{r.uniform(40,170):.0f}" height="3" fill="#e9f2f0" opacity="{r.uniform(0.25,0.6):.2f}"/>' for _ in range(40))
    b += '<path d="M0 650 C400 622 900 640 1600 618 L1600 900 L0 900 Z" fill="#c79a4a"/>'
    # steamer with side paddle and a long smoke trail
    b += ('<g transform="translate(900 470)"><path d="M0 70 L330 70 L300 110 L30 110 Z" fill="#2e2a28"/>'
          '<rect x="50" y="30" width="190" height="40" fill="#f1e6cd"/><rect x="90" y="4" width="110" height="28" fill="#f1e6cd"/>'
          + "".join(f'<rect x="{x}" y="42" width="14" height="14" fill="#35506a"/>' for x in range(64, 230, 30)) +
          '<rect x="100" y="-56" width="26" height="62" fill="#1b1a1a"/><rect x="156" y="-56" width="26" height="62" fill="#1b1a1a"/>'
          '<rect x="98" y="-62" width="30" height="8" fill="#9c4a2e"/><rect x="154" y="-62" width="30" height="8" fill="#9c4a2e"/>'
          '<circle cx="70" cy="92" r="30" fill="#9c4a2e"/><circle cx="70" cy="92" r="22" fill="none" stroke="#e8c29a" stroke-width="3"/>'
          '</g>')
    b += ('<path d="M1000 410 C940 370 880 380 820 340 C760 300 690 320 640 280" fill="none" stroke="#f4f0e6" stroke-width="30" stroke-linecap="round" opacity="0.7"/>'
          '<path d="M1050 408 C1010 360 960 370 900 330 C850 296 790 300 740 262" fill="none" stroke="#e8e3d8" stroke-width="22" stroke-linecap="round" opacity="0.55"/>')
    # sheaves of rye on the near bank, a road, and a lone walker
    b += f'<path d="M-20 900 C300 760 800 740 1620 800 L1620 900 Z" fill="{DRY}"/>'
    for i in range(46):
        x = r.uniform(0, 1600); y = r.uniform(690, 880); s = 0.5 + (y - 690) / 190 * 0.9
        b += (f'<path d="M{x:.0f} {y:.0f} l{-14*s:.0f} {6*s:.0f} l{14*s:.0f} {-36*s:.0f} l{14*s:.0f} {36*s:.0f} Z" fill="#e3c27a" stroke="#a8803a" stroke-width="1.5"/>')
    b += '<path d="M0 860 C380 800 760 800 1180 820 C1380 830 1500 850 1600 870 L1600 900 L0 900 Z" fill="#8d6a3a"/>'
    b += ('<g transform="translate(560 822)" fill="#1b1a1a"><circle cx="0" cy="-60" r="9"/><path d="M-12 -52 L12 -52 L16 -14 L-16 -14 Z"/>'
          '<rect x="-12" y="-14" width="7" height="24"/><rect x="5" y="-14" width="7" height="24"/><rect x="-24" y="-48" width="8" height="52" transform="rotate(8)"/>'
          '<rect x="14" y="-50" width="20" height="22" fill="#9c4a2e"/></g>')
    return svg(1600, 900, b, defs)


# ---------------------------------------------------------------- 3: the Bashkir camp (parts V-VI)
def art_camp():
    r = random.Random(3)
    defs = (f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6f6aa0"/>'
            f'<stop offset="0.55" stop-color="#f3b176"/><stop offset="1" stop-color="#f7d28a"/></linearGradient>'
            f'<radialGradient id="sun" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#fff0c4"/><stop offset="1" stop-color="#fff0c4" stop-opacity="0"/></radialGradient>' + HORSE)
    b = '<rect width="1600" height="900" fill="url(#sky)"/><circle cx="1180" cy="520" r="230" fill="url(#sun)"/><circle cx="1180" cy="530" r="62" fill="#fff0c4"/>'
    b += '<path d="M0 560 C300 520 700 560 1100 540 C1300 530 1500 548 1600 540 L1600 900 L0 900 Z" fill="#b98f48"/>'
    b += '<path d="M0 600 C400 580 900 610 1600 590 L1600 900 L0 900 Z" fill="#a8803a"/>'
    b += '<path d="M120 640 C420 600 560 690 900 650 C1200 615 1380 700 1600 660 L1600 720 C1380 760 1200 676 900 712 C560 750 420 660 120 700 Z" fill="#7f9aa0" opacity="0.85"/>'
    b += '<path d="M0 800 C400 740 1000 760 1600 730 L1600 900 L0 900 Z" fill="#8d6a3a"/>'
    b += grass(r, 0, 1600, 600, 880, 520, [DRY, OCHRE, STRAW, "#7c6a35"], lean=14)
    # felt tents
    def tent(cx, base, w, h, door=True):
        s = f'<ellipse cx="{cx}" cy="{base+6}" rx="{w*0.62:.0f}" ry="{w*0.08:.0f}" fill="#000" opacity="0.2"/>'
        s += f'<path d="M{cx-w/2:.0f} {base} L{cx-w/2:.0f} {base-h*0.55:.0f} Q{cx} {base-h*1.28:.0f} {cx+w/2:.0f} {base-h*0.55:.0f} L{cx+w/2:.0f} {base} Z" fill="#eadfc5"/>'
        s += f'<path d="M{cx-w/2:.0f} {base-h*0.5:.0f} Q{cx} {base-h*1.1:.0f} {cx+w/2:.0f} {base-h*0.5:.0f}" fill="none" stroke="{RUST}" stroke-width="7"/>'
        s += f'<path d="M{cx-w/2:.0f} {base-h*0.2:.0f} L{cx+w/2:.0f} {base-h*0.2:.0f}" stroke="#c9b88f" stroke-width="5"/>'
        if door:
            s += f'<path d="M{cx-w*0.12:.0f} {base} L{cx-w*0.12:.0f} {base-h*0.38:.0f} Q{cx} {base-h*0.5:.0f} {cx+w*0.12:.0f} {base-h*0.38:.0f} L{cx+w*0.12:.0f} {base} Z" fill="#4b2a1f"/>'
        s += f'<path d="M{cx} {base-h*1.2:.0f} C{cx-8} {base-h*1.45:.0f} {cx+16} {base-h*1.6:.0f} {cx+2} {base-h*1.85:.0f}" stroke="#7a6a64" stroke-width="9" fill="none" stroke-linecap="round" opacity="0.5"/>'
        return s
    b += tent(430, 700, 250, 190) + tent(720, 724, 300, 230) + tent(1010, 700, 220, 170) + tent(250, 740, 180, 140)
    # horses in the distance, foals tied behind the tents
    for i, (x, y, s) in enumerate([(1250, 690, .8), (1330, 700, .85), (1410, 682, .75), (1180, 704, .7), (1480, 716, .9)]):
        b += f'<use href="#horse" x="{x}" y="{y-60*s}" width="{120*s}" height="{90*s}" color="#4a2f20"/>'
    b += '<path d="M560 760 L880 764" stroke="#4a2f20" stroke-width="3"/>'
    for x in (600, 680, 760, 840):
        b += f'<use href="#horse" x="{x}" y="{722}" width="64" height="48" color="#5a3a28"/>'
    # a few people by the tents (plain silhouettes), a fire
    b += '<ellipse cx="560" cy="800" rx="34" ry="9" fill="#2b1810"/><path d="M548 800 q6 -34 12 -4 q4 -26 10 4 Z" fill="#f0a050"/>'
    for x in (500, 610, 650):
        b += f'<g transform="translate({x} 806)" fill="#2b1810"><circle cx="0" cy="-34" r="7"/><path d="M-11 -26 Q0 -30 11 -26 L16 0 L-16 0 Z"/></g>'
    return svg(1600, 900, b, defs)


# ---------------------------------------------------------------- 4: dawn on the steppe (parts VII-VIII)
def art_dawn():
    r = random.Random(4)
    defs = (f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#25294f"/>'
            f'<stop offset="0.45" stop-color="#8a5a7a"/><stop offset="0.78" stop-color="#ee9d68"/><stop offset="1" stop-color="#f9d28a"/></linearGradient>'
            f'<radialGradient id="sun" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#fff0c4"/><stop offset="0.35" stop-color="#ffd890" stop-opacity="0.6"/><stop offset="1" stop-color="#ffd890" stop-opacity="0"/></radialGradient>'
            f'<linearGradient id="mist" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f7dcb0" stop-opacity="0"/><stop offset="1" stop-color="#f7dcb0" stop-opacity="0.55"/></linearGradient>')
    b = '<rect width="1600" height="900" fill="url(#sky)"/>' + stars(r, 26, 1600, 260)
    b += '<circle cx="1150" cy="548" r="300" fill="url(#sun)"/><circle cx="1150" cy="552" r="70" fill="#fff3cf"/>'
    b += '<path d="M0 548 L1600 548 L1600 900 L0 900 Z" fill="#b08a44"/>'
    b += '<rect x="0" y="470" width="1600" height="100" fill="url(#mist)"/>'
    b += f'<path d="M0 560 C300 540 700 560 1000 552 C1300 546 1500 556 1600 552 L1600 900 L0 900 Z" fill="{OCHRE}"/>'
    # the shikhan: a low mound, with the small party on top
    b += '<path d="M60 575 C170 520 260 486 360 484 C460 486 560 524 660 575 Z" fill="#6f5a35"/><path d="M360 484 C460 486 560 524 660 575 L430 575 Z" fill="#8c7242" opacity="0.8"/>'
    for x in (326, 342, 358, 374, 392, 408):
        b += f'<g transform="translate({x} 486)" fill="#241a14"><circle cx="0" cy="-12" r="3.6"/><rect x="-3.5" y="-8" width="7" height="14"/></g>'
    b += '<g fill="#241a14"><rect x="288" y="480" width="24" height="9"/><circle cx="293" cy="491" r="4"/><circle cx="308" cy="491" r="4"/><rect x="425" y="480" width="24" height="9"/><circle cx="430" cy="491" r="4"/><circle cx="445" cy="491" r="4"/></g>'
    b += f'<ellipse cx="368" cy="494" rx="8" ry="4" fill="{ORANGE}"/>'
    # the walker's path: little earth marks, bigger as they come closer
    pts = [(420, 600), (520, 640), (640, 690), (780, 748), (930, 800), (1090, 842), (1250, 872)]
    b += "".join(f'<ellipse cx="{x}" cy="{y}" rx="{8+i*5}" ry="{3+i*1.5:.0f}" fill="#5a3f22"/><ellipse cx="{x}" cy="{y-1-i}" rx="{6+i*4}" ry="{2+i*1.2:.0f}" fill="#9a7a3c"/>' for i, (x, y) in enumerate(pts))
    b += grass(r, 0, 1600, 580, 900, 1300, [DRY, OCHRE, STRAW, "#7c6a35", "#d9c27c"], length=(16, 42), lean=14)
    # a lone walker in the foreground with a spade
    b += ('<g transform="translate(1180 872)" fill="#241a14"><circle cx="0" cy="-118" r="13"/><path d="M-18 -104 Q0 -112 18 -104 L22 -34 L-22 -34 Z"/>'
          '<rect x="-17" y="-34" width="12" height="40"/><rect x="5" y="-34" width="12" height="40"/>'
          '<rect x="16" y="-150" width="7" height="156" transform="rotate(10 20 -70)"/><path d="M26 -154 l18 -6 l4 20 l-20 6 Z"/></g>')
    return svg(1600, 900, b, defs)


# ---------------------------------------------------------------- 5: the sun goes down (part IX)
def art_sunset():
    r = random.Random(5)
    defs = (f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a1d3d"/>'
            f'<stop offset="0.45" stop-color="#9a3a44"/><stop offset="0.8" stop-color="#e5733a"/><stop offset="1" stop-color="#f6b25e"/></linearGradient>'
            f'<radialGradient id="sun" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#ffe9a8"/><stop offset="0.4" stop-color="#ffb35c" stop-opacity="0.7"/><stop offset="1" stop-color="#ff8a3a" stop-opacity="0"/></radialGradient>'
            f'<clipPath id="above"><rect x="0" y="0" width="1600" height="590"/></clipPath>')
    b = '<rect width="1600" height="900" fill="url(#sky)"/>'
    b += '<g clip-path="url(#above)"><circle cx="520" cy="610" r="360" fill="url(#sun)"/><circle cx="520" cy="610" r="120" fill="#fbd27a"/></g>'
    b += '<path d="M0 590 C300 572 700 592 1000 580 C1300 570 1500 584 1600 580 L1600 900 L0 900 Z" fill="#4b2230"/>'
    b += '<path d="M0 640 C400 620 900 650 1600 626 L1600 900 L0 900 Z" fill="#3b1c27"/>'
    b += grass(r, 0, 1600, 650, 900, 700, ["#5a2a2a", "#7a3b2a", "#8a4a2a", "#3a1a22"], length=(16, 40), lean=14)
    # the shikhan in the foreground (right), lit from the left by the last light
    b += '<path d="M860 900 C960 700 1100 610 1300 596 C1450 600 1560 680 1620 900 Z" fill="#2c1520"/><path d="M860 900 C960 700 1100 610 1300 596 C1220 640 1150 720 1100 900 Z" fill="#7a3a2e" opacity="0.65"/>'
    # tiny group on the mound, waving
    for x, a in ((1240, -18), (1262, 12), (1286, -10), (1312, 16), (1338, -14)):
        b += (f'<g transform="translate({x} 604)" fill="#150b12"><circle cx="0" cy="-20" r="5.5"/><rect x="-5" y="-14" width="10" height="20"/>'
              f'<rect x="4" y="-14" width="3.5" height="20" transform="rotate({a} 5 -12)"/></g>')
    # the fox-fur cap with the money beside it, and the elder
    b += (f'<g transform="translate(1180 672)"><ellipse cx="0" cy="10" rx="40" ry="9" fill="#150b12" opacity="0.5"/>'
          f'<path d="M-34 8 Q-30 -26 0 -28 Q30 -26 34 8 Z" fill="{RED}"/>'
          + "".join(f'<path d="M{x} -20 l{r.uniform(-5,5):.0f} {r.uniform(-12,-6):.0f}" stroke="#d98a52" stroke-width="3" stroke-linecap="round"/>' for x in range(-26, 30, 7)) +
          '<circle cx="52" cy="6" r="6" fill="#f2c867"/><circle cx="66" cy="9" r="6" fill="#f2c867"/><circle cx="59" cy="1" r="6" fill="#f2c867"/></g>')
    # in the foreground: a spade stuck in the ground and a long narrow patch of dug earth
    b += '<polygon points="140,880 330,790 372,794 190,890" fill="#150b12"/><polygon points="150,876 322,794 346,796 176,884" fill="#2a1420"/>'
    b += ('<g transform="translate(470 810)"><rect x="-5" y="-250" width="10" height="250" fill="#6b4a2c" transform="rotate(8)"/>'
          '<rect x="-19" y="-262" width="38" height="12" fill="#6b4a2c" transform="rotate(8 0 -256)"/>'
          '<path d="M-26 -6 L26 -6 L22 52 Q0 70 -22 52 Z" fill="#a9a29a" transform="rotate(8 0 0)"/></g>')
    b += '<path d="M470 872 C520 860 600 862 660 872" fill="none" stroke="#150b12" stroke-width="8" opacity="0.45"/>'
    return svg(1600, 900, b, defs)


# ---------------------------------------------------------------- cover (square)
def cover(lang='en'):
    r = random.Random(7)
    W = H = 3000
    defs = (f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#171c3a"/>'
            f'<stop offset="0.5" stop-color="#5a3552"/><stop offset="0.74" stop-color="#e0764a"/><stop offset="1" stop-color="#f5c06e"/></linearGradient>'
            f'<radialGradient id="sun" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#ffecb0"/><stop offset="0.4" stop-color="#ffbe6a" stop-opacity="0.55"/><stop offset="1" stop-color="#ff9a4a" stop-opacity="0"/></radialGradient>')
    b = f'<rect width="{W}" height="{H}" fill="url(#sky)"/>' + stars(r, 90, W, 1300)
    b += '<circle cx="1500" cy="1980" r="760" fill="url(#sun)"/><circle cx="1500" cy="1980" r="240" fill="#fbd68a"/>'
    b += '<path d="M0 1980 C500 1950 1100 1990 1700 1970 C2200 1955 2700 1980 3000 1975 L3000 3000 L0 3000 Z" fill="#7a4a35"/>'
    b += '<path d="M0 2120 C600 2080 1400 2140 3000 2090 L3000 3000 L0 3000 Z" fill="#8f6038"/>'
    b += '<path d="M0 2380 C700 2330 1500 2400 3000 2330 L3000 3000 L0 3000 Z" fill="#a8803a"/>'
    b += '<path d="M0 2700 C800 2640 1700 2720 3000 2650 L3000 3000 L0 3000 Z" fill="#7c5a2c"/>'
    b += grass(r, 0, 3000, 2100, 3000, 1800, [DRY, OCHRE, STRAW, "#6b4a28"], length=(40, 110), lean=30, width=(3, 6))
    # a lone figure with a spade, walking toward the sun, with a long shadow
    b += ('<g transform="translate(1180 2600)" fill="#1a0f14"><circle cx="0" cy="-230" r="26"/><path d="M-36 -204 Q0 -222 36 -204 L44 -70 L-44 -70 Z"/>'
          '<rect x="-34" y="-70" width="24" height="80"/><rect x="10" y="-70" width="24" height="80"/>'
          '<rect x="34" y="-300" width="12" height="310" transform="rotate(9 40 -150)"/><path d="M50 -306 l36 -12 l8 40 l-40 12 Z"/></g>')
    b += '<path d="M1180 2606 L1900 2640 L1930 2656 L1170 2620 Z" fill="#1a0f14" opacity="0.35"/>'
    pts = [(1380, 2560), (1560, 2512), (1740, 2470), (1900, 2434), (2040, 2404)]
    b += "".join(f'<ellipse cx="{x}" cy="{y}" rx="{34-i*4}" ry="{11-i}" fill="#3a2414" opacity="0.8"/>' for i, (x, y) in enumerate(pts))
    # title
    T = {"en": ("LEO TOLSTOY", "How Much Land", "Does a Man Need?"), "ru": ("ЛЕВ ТОЛСТОЙ", "Много ли человеку", "земли нужно?")}[lang]
    b += (f'<text x="1500" y="420" text-anchor="middle" font-family="Georgia, serif" font-size="92" letter-spacing="30" fill="{STRAW}">{T[0]}</text>'
          f'<text x="1500" y="740" text-anchor="middle" font-family="Georgia, serif" font-weight="bold" font-size="236" fill="{CREAM}">{T[1]}</text>'
          f'<text x="1500" y="1000" text-anchor="middle" font-family="Georgia, serif" font-weight="bold" font-size="236" fill="{CREAM}">{T[2]}</text>'
          f'<rect x="1200" y="1110" width="600" height="8" fill="{STRAW}"/><rect x="1330" y="1140" width="340" height="5" fill="{STRAW}"/>')
    return svg(W, H, b, defs)


FILES = {"1_hut": art_hut, "2_river": art_river, "3_camp": art_camp, "4_dawn": art_dawn, "5_sunset": art_sunset, "cover": cover, "cover_ru": lambda: cover("ru")}
for name, fn in FILES.items():
    with open(f"{OUT}/{name}.svg", "w", encoding="utf-8") as f:
        f.write(fn())
    print("wrote", f"{OUT}/{name}.svg")
