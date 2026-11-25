#!/usr/bin/env python3
"""Illustrations and cover for "The Night Before Christmas" as SVG (1600x900; covers 3000x3000).
Palette: frosty deep-blue Ukrainian night, moon yellow, whitewashed huts under snow, warm window gold, a little red.
Helpers (svg, sky, stars, win, lamp, person ...) come from production/poor-folk. Original scenes, no copies of paintings."""
import random, math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "poor-folk"))
import make_art as _pf          # poor-folk's helpers
from make_art2 import candle, paper, table, DWOOD, WOOD
svg, sky, stars, win, lamp, person = _pf.svg, _pf.sky, _pf.stars, _pf.win, _pf.lamp, _pf.person
PAPER, GOLD, RED, LEAF = _pf.PAPER, _pf.GOLD, _pf.RED, _pf.LEAF
OUT = "art"; os.makedirs(OUT, exist_ok=True)
SNOW, SNOW2, MOON, INK = "#e8eefc", "#c3cfe8", "#fff1c4", "#0e0d14"
HUTW, THATCH = "#efe7d6", "#7a6038"
FIR = "#233d3a"


def R(s): return random.Random(s)


_G = [0]


def glow(x, y, r=300, a=.2, col=GOLD):
    """a soft round light (radial gradient, no hard edge)."""
    _G[0] += 1; i = f"g{_G[0]}"
    return (f'<defs><radialGradient id="{i}"><stop offset="0" stop-color="{col}" stop-opacity="{min(1,a*2.2):.2f}"/><stop offset=".5" stop-color="{col}" stop-opacity="{a*.9:.2f}"/>'
            f'<stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient></defs><circle cx="{x}" cy="{y}" r="{r}" fill="url(#{i})"/>')


def flakes(r, n, w=1600, h=900, op=.8): return "".join(f'<circle cx="{r.randint(0,w)}" cy="{r.randint(0,h)}" r="{r.uniform(2,5):.1f}" fill="#fff" opacity="{op}"/>' for _ in range(n))


def moon(cx, cy, r=60, halo=True):
    s = glow(cx, cy, r * 3.4, .16, MOON) if halo else ""
    return s + f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{MOON}"/><circle cx="{cx-r*.3}" cy="{cy-r*.2}" r="{r*.18}" fill="#e8d49a" opacity=".6"/><circle cx="{cx+r*.25}" cy="{cy+r*.3}" r="{r*.12}" fill="#e8d49a" opacity=".5"/>'


def ground(y=640, col=SNOW, h=900):
    return f'<rect y="{y}" width="1600" height="{h-y}" fill="{col}"/><path d="M0 {y+10} Q300 {y-30} 650 {y+8} T1300 {y+4} T1600 {y-10} L1600 {y+60} L0 {y+60} Z" fill="{SNOW2}" opacity=".7"/>'


def hut(x, y, w=260, h=130, lit=True, smoke=False, door=True, snow=True, wins=1):
    """x,y = left of the wall, y = ground line."""
    t = y - h
    s = f'<rect x="{x}" y="{t}" width="{w}" height="{h}" fill="{HUTW}"/><rect x="{x}" y="{y-14}" width="{w}" height="14" fill="#8a7a66"/>'
    s += f'<polygon points="{x-26},{t+12} {x+w/2},{t-88} {x+w+26},{t+12}" fill="{THATCH}"/>'
    if snow: s += f'<path d="M{x-22} {t+4} L{x+w/2} {t-84} L{x+w+22} {t+4} Q{x+w*.85} {t-6} {x+w*.7} {t+6} Q{x+w*.5} {t-8} {x+w*.3} {t+8} Q{x+w*.15} {t-4} {x-22} {t+4} Z" fill="{SNOW}"/>'
    ws = [(x + w * .14, t + h * .24)] if wins == 1 else [(x + w * .1, t + h * .24), (x + w * .62, t + h * .24)]
    for wx, wy in ws: s += win(wx, wy, w * .24, h * .4, lit)
    if door: s += f'<rect x="{x+w*.46}" y="{y-h*.62}" width="{w*.14}" height="{h*.62}" fill="#4a3022"/>' if wins == 1 else ""
    if lit: s = glow(x + w * .26, t + h * .5, w * .55, .14) + s
    if smoke: s += f'<rect x="{x+w*.7}" y="{t-80}" width="22" height="46" fill="{HUTW}"/><path d="M{x+w*.7+11} {t-84} q-26 -50 6 -100 q34 -50 -10 -110" stroke="#cfd4e8" stroke-width="22" fill="none" opacity=".4" stroke-linecap="round"/>'
    return s


def fir(x, y, h=300):
    s = f'<rect x="{x-8}" y="{y-30}" width="16" height="34" fill="#3a2a22"/>'
    for k in range(4):
        w = h * .26 * (1 - k * .2); yy = y - 30 - h * .22 * k
        s += f'<polygon points="{x-w},{yy} {x},{yy-h*.34} {x+w},{yy}" fill="{FIR}"/><polygon points="{x-w*.8},{yy-h*.05} {x},{yy-h*.34} {x+w*.8},{yy-h*.05} {x+w*.3},{yy-h*.12} {x},{yy-h*.06} {x-w*.4},{yy-h*.14}" fill="{SNOW}" opacity=".6"/>'
    return s


def witch(x, y, s=1.0, rot=-12, col=INK):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})"><path d="M-150 18 L-60 6 L-60 26 Z" fill="#7a5a32"/><path d="M-150 18 L-215 -4 L-212 24 L-218 46 Z" fill="#8a6a3a"/>'
            f'<rect x="-150" y="9" width="260" height="10" rx="5" fill="#5a3a22"/>'
            f'<path d="M-30 6 Q-20 -40 0 -62 L30 -60 Q40 -30 52 6 Z" fill="{col}"/><circle cx="14" cy="-78" r="17" fill="{col}"/>'
            f'<path d="M-2 -86 Q-50 -90 -76 -62 Q-40 -76 -4 -70 Z" fill="{col}"/><path d="M26 -40 L84 -4 L80 4 L24 -26 Z" fill="{col}"/>'
            f'<path d="M-30 6 Q-90 20 -110 60 Q-60 40 -20 30 Z" fill="{col}"/></g>')


def devil(x, y, s=1.0, flip=1, col="#1c1418", moonhold=None):
    g = f'<g transform="translate({x} {y}) scale({s*flip} {s})">'
    g += f'<path d="M-30 30 Q-110 40 -130 90 Q-90 70 -64 70 L-62 62 Z" fill="{col}"/><polygon points="-130,90 -154,70 -118,60 -110,100" fill="{col}"/>'      # tail with arrow tip
    g += f'<ellipse cx="0" cy="10" rx="42" ry="56" fill="{col}"/><rect x="-26" y="52" width="9" height="50" fill="{col}"/><rect x="10" y="52" width="9" height="50" fill="{col}"/>'
    g += f'<path d="M-30 100 l-10 14 l30 0 z M8 100 l-8 14 l30 0 z" fill="#3a2a22"/>'
    g += f'<circle cx="26" cy="-62" r="26" fill="{col}"/><ellipse cx="52" cy="-52" rx="22" ry="15" fill="#3a2a30"/><circle cx="46" cy="-52" r="3" fill="#0e0d14"/><circle cx="58" cy="-52" r="3" fill="#0e0d14"/>'
    g += f'<polygon points="14,-84 6,-120 28,-88" fill="{col}"/><polygon points="34,-84 44,-118 48,-82" fill="{col}"/><path d="M40 -38 q2 24 -10 36 q14 -6 20 -30 Z" fill="#2a2024"/>'
    g += '<circle cx="30" cy="-68" r="5" fill="#f6d34a"/>'
    g += f'<path d="M30 -20 L90 -40 L96 -30 L34 -2 Z" fill="{col}"/><path d="M-30 -10 L-76 -50 L-68 -58 L-18 -26 Z" fill="{col}"/>'
    if moonhold: g += f'<circle cx="104" cy="-52" r="{moonhold}" fill="{MOON}"/>'
    return g + '</g>'


def sack(x, y, s=1.0, col="#9a7a52", tied=True):
    g = f'<g transform="translate({x} {y}) scale({s})"><path d="M-70 0 Q-92 -90 -40 -150 L-26 -168 L26 -168 L40 -150 Q92 -90 70 0 Z" fill="{col}"/>'
    g += f'<path d="M-26 -168 L-34 -196 L-12 -180 L0 -204 L12 -180 L34 -196 L26 -168 Z" fill="{col}"/><path d="M-30 -160 Q0 -148 30 -160" stroke="#5a3a22" stroke-width="8" fill="none"/>'
    g += '<path d="M-40 -100 Q-10 -80 -52 -40" stroke="#7a5a3a" stroke-width="4" fill="none"/></g>'
    return g


def cossack(x, y, s=1.0, col=INK, hat="#2a1c14", fur=True):
    """a man in a sheepskin and a fur cap (person() with a hat and a moustache)."""
    g = person(x, y, s, col)
    g += f'<g transform="translate({x} {y}) scale({s})"><ellipse cx="0" cy="-138" rx="21" ry="13" fill="{hat}"/><rect x="-19" y="-130" width="38" height="8" fill="{hat}"/><path d="M-12 -112 q12 8 24 0" stroke="#5a4a3a" stroke-width="3" fill="none"/></g>'
    return g


def woman(x, y, s=1.0, col="#3a2a3a", scarf=RED, ribbons=False):
    g = f'<g transform="translate({x} {y}) scale({s})"><circle cx="0" cy="-122" r="15" fill="#d9b49a"/><path d="M-16 -124 Q0 -150 16 -124 Q10 -132 0 -134 Q-10 -132 -16 -124 Z" fill="{scarf}"/>'
    g += f'<path d="M-22 -104 Q0 -116 22 -104 L40 20 L-40 20 Z" fill="{col}"/><rect x="-26" y="-6" width="52" height="30" fill="{scarf}" opacity=".85"/>'
    if ribbons: g += f'<path d="M-8 -136 q-30 20 -26 70 M0 -136 q-36 30 -22 90 M8 -136 q-14 30 -6 80" stroke="{RED}" stroke-width="4" fill="none"/>'
    return g + '</g>'


def stove(x, y, w=380, h=330, glow_on=True):
    s = f'<rect x="{x}" y="{y-h}" width="{w}" height="{h}" fill="#e6dcc4"/><rect x="{x}" y="{y-h}" width="{w}" height="26" fill="#cbbf9f"/>'
    s += f'<path d="M{x+w*.2} {y} V{y-h*.42} Q{x+w*.5} {y-h*.64} {x+w*.8} {y-h*.42} V{y} Z" fill="#1c1210"/>'
    if glow_on: s += f'<path d="M{x+w*.28} {y} V{y-h*.36} Q{x+w*.5} {y-h*.54} {x+w*.72} {y-h*.36} V{y} Z" fill="#e8742e" opacity=".9"/><path d="M{x+w*.38} {y} q10 -50 30 -60 q20 10 24 60 Z" fill="#f6c24a"/>'
    s += f'<path d="M{x+w*.12} {y-h*.8} q20 -16 40 0 M{x+w*.64} {y-h*.8} q20 -16 40 0" stroke="#b05a3a" stroke-width="5" fill="none"/>'
    return s


def icon_corner(x, y):
    return (f'<rect x="{x}" y="{y}" width="110" height="150" fill="#3a2a22"/><rect x="{x+10}" y="{y+10}" width="90" height="130" fill="#c8a24a"/><circle cx="{x+55}" cy="{y+56}" r="26" fill="#8a5a3a"/>'
            f'<path d="M{x-24} {y-14} L{x+134} {y-14} L{x+120} {y+40} Q{x+55} {y+10} {x-10} {y+40} Z" fill="{PAPER}"/><path d="M{x-24} {y-14} H{x+134}" stroke="{RED}" stroke-width="8"/>'
            f'<circle cx="{x+55}" cy="{y+176}" r="8" fill="{GOLD}"/><circle cx="{x+55}" cy="{y+176}" r="40" fill="{GOLD}" opacity=".18"/>')


def room(c1="#2a2018", c2="#3a2c24", fy=650):
    d, b = sky(c1, c2)
    b += f'<rect y="{fy}" width="1600" height="{900-fy}" fill="#2a1d16"/>' + "".join(f'<rect y="{y}" width="1600" height="3" fill="#1e140f" opacity=".7"/>' for y in range(fy + 30, 900, 40))
    b += f'<rect y="{fy-14}" width="1600" height="14" fill="#4a3426"/>'
    return d, b


def bench(x, w, y=690): return f'<rect x="{x}" y="{y}" width="{w}" height="22" fill="{WOOD}"/><rect x="{x+16}" y="{y+22}" width="16" height="{900-y-30}" fill="{DWOOD}"/><rect x="{x+w-32}" y="{y+22}" width="16" height="{900-y-30}" fill="{DWOOD}"/>'


def church(x, y, s=1.0, lit=True):
    g = f'<g transform="translate({x} {y}) scale({s})"><rect x="-120" y="-200" width="240" height="200" fill="#f0eadc"/><rect x="-60" y="-300" width="120" height="110" fill="#f0eadc"/>'
    g += f'<path d="M-76 -300 Q0 -420 76 -300 Z" fill="#3a6a8a"/><rect x="-4" y="-470" width="8" height="60" fill="{GOLD}"/><rect x="-22" y="-452" width="44" height="7" fill="{GOLD}"/><circle cx="0" cy="-412" r="8" fill="{GOLD}"/>'
    g += f'<path d="M-128 -200 Q-60 -280 0 -200 Z" fill="#3a6a8a"/><path d="M0 -200 Q60 -280 128 -200 Z" fill="#3a6a8a"/>'
    g += f'<path d="M-30 0 V-80 Q0 -112 30 -80 V0 Z" fill="#3a2a22"/>'
    for wx in (-100, 70): g += f'<path d="M{wx} -90 V-150 Q{wx+15} -172 {wx+30} -150 V-90 Z" fill="{GOLD if lit else "#2a3148"}"/>'
    g += f'<path d="M-30 -230 V-280 Q0 -306 30 -280 V-230 Z" fill="{GOLD if lit else "#2a3148"}"/></g>'
    return g


def petersburg_row(top, y=640, n=7, lit=True, cols=("#8a8a9c", "#a09a8a", "#7a8aa0"), r=None):
    r = r or R(1); s = ""
    x = -20
    for i in range(n):
        w = r.randint(210, 280); h = r.randint(300, 440); c = cols[i % len(cols)]
        s += f'<rect x="{x}" y="{y-h}" width="{w}" height="{h}" fill="{c}"/><rect x="{x-6}" y="{y-h-14}" width="{w+12}" height="20" fill="#5a5666"/>'
        for rr in range(int(h // 100)):
            for cc in range(max(2, int(w // 70))):
                s += win(x + 18 + cc * (w - 30) / max(2, int(w // 70)), y - h + 30 + rr * 96, 30, 54, lit and r.random() > .15)
        x += w + 4
    return s


def a_frame(name, fn): return fn


# ============================================================== PART I
def i1():   # the village under the stars, a witch rising from a chimney
    r = R(11); d, b = sky("#0b1230", "#2a3a6c")
    b += stars(r, 140, 1600, 480) + moon(1230, 190, 60)
    b += ground(640)
    for x, w, c in ((60, 280, 1), (430, 250, 0), (880, 300, 1), (1260, 260, 0)):
        b += hut(x, 700 + r.randint(-20, 20), w, 130, True, smoke=bool(c))
    b += fir(1500, 700, 330) + fir(1420, 720, 250) + fir(30, 720, 280)
    b += witch(560, 330, 1.0, -14)
    b += '<path d="M470 340 q-60 70 -190 150" stroke="#cfd4e8" stroke-width="12" fill="none" opacity=".25"/>' + flakes(r, 60, op=.55)
    return svg(b, d)


def i2():   # high in the sky: a witch gathers stars in her sleeve, the devil approaches
    r = R(12); d, b = sky("#070c26", "#1f2c5c")
    b += stars(r, 200, 1600, 800) + '<path d="M0 700 Q400 560 900 640 T1600 560 L1600 900 L0 900 Z" fill="#0c1230"/><path d="M0 760 Q500 700 1000 740 T1600 700 L1600 900 L0 900 Z" fill="#e8eefc" opacity=".85"/>'
    b += witch(520, 320, 1.4, -8)
    b += "".join(f'<path d="M{x} {y} l5 -16 l5 16 l16 5 l-16 5 l-5 16 l-5 -16 l-16 -5 z" fill="{MOON}"/>' for x, y in ((650, 250), (720, 300), (590, 210), (780, 240)))
    b += devil(1180, 400, 1.3, -1)
    b += '<path d="M1060 250 q-40 -30 -10 -70" stroke="#e8eefc" stroke-width="3" fill="none" opacity=".3"/>' + moon(1380, 160, 38)
    return svg(b, d)


def i3():   # the devil has the moon in both hands, then in his pocket: darkness falls
    r = R(13); d, b = sky("#0a1028", "#161e44")
    b += stars(r, 70, 1600, 500)
    b += glow(780, 330, 520, .14, MOON)
    b += devil(760, 480, 2.1, 1, moonhold=0)
    b += moon(1030, 330, 82, halo=False)
    b += '<path d="M960 340 q10 -34 36 -30 M1100 330 q-4 -36 -26 -44" stroke="#f6d34a" stroke-width="4" fill="none"/>'
    b += '<path d="M0 780 Q500 700 1000 760 T1600 730 L1600 900 L0 900 Z" fill="#d6dff2" opacity=".35"/>'
    return svg(b, d)


def i4():   # Chub and his friend outside the hut, no moon, one lit window
    r = R(14); d, b = sky("#05071a", "#10163a")
    b += stars(r, 18, 1600, 300) + ground(660, "#7a86a8") + hut(980, 700, 420, 190, True, smoke=True, wins=1)
    b += cossack(520, 730, 1.9, "#1a1418") + cossack(720, 740, 1.8, "#2a2024", hat="#3a2a1c")
    b += '<path d="M590 700 L650 540" stroke="#5a3a22" stroke-width="7"/><path d="M650 540 q40 30 20 70" stroke="#2a1c14" stroke-width="4" fill="none"/>'
    b += glow(1100, 660, 300, .22) + fir(240, 740, 340) + fir(130, 760, 260)
    b += flakes(r, 40, op=.4)
    return svg(b, d)


# ============================================================== PART II
def ii1():   # Oksana at the mirror in her father's hut
    d, b = room()
    b += icon_corner(1300, 150) + win(160, 150, 240, 300, False)
    b += stove(1090, 660, 360, 300, False) if False else ""
    b += '<rect x="560" y="200" width="150" height="190" rx="10" fill="#5a5048"/><rect x="574" y="214" width="122" height="162" rx="6" fill="#cfd8e8"/><path d="M590 340 q50 -80 90 -60" stroke="#fff" stroke-width="5" opacity=".6" fill="none"/>'
    b += glow(640, 480, 520, .28) + candle(900, 690, 90)
    b += woman(640, 700, 2.6, "#3a2a50", RED, True)
    b += '<path d="M570 330 l-18 22 M720 330 l20 22" stroke="#d9b49a" stroke-width="6"/>' if False else ""
    b += bench(980, 520) + f'<rect x="1220" y="610" width="200" height="82" fill="#6a3a2c"/><rect x="1220" y="610" width="200" height="14" fill="{GOLD}" opacity=".6"/>'
    b += cossack(1180, 700, 1.0, "#1a1418") if False else ""
    return svg(b, d)


def ii2():   # Vakula and Oksana: the painted chest
    d, b = room("#241a14", "#34261e")
    b += win(180, 150, 220, 280, False) + icon_corner(1260, 140) + glow(780, 520, 560, .26)
    b += f'<rect x="560" y="520" width="520" height="190" fill="#4a3a8a"/><rect x="560" y="500" width="520" height="30" fill="#2a2a5a"/>'
    for k, (cx, cy, c) in enumerate(((620, 600, RED), (700, 640, "#f6d34a"), (790, 590, "#3a8ad0"), (880, 640, RED), (970, 600, "#f6d34a"), (1030, 650, "#3a8ad0"))):
        b += f'<circle cx="{cx}" cy="{cy}" r="22" fill="{c}"/><path d="M{cx} {cy+20} q-6 30 -26 44" stroke="{LEAF}" stroke-width="7" fill="none"/><circle cx="{cx}" cy="{cy}" r="8" fill="#fff" opacity=".6"/>'
    b += f'<rect x="570" y="705" width="500" height="22" fill="#2a2a5a"/>' + bench(120, 380, 700)
    b += woman(1200, 720, 2.5, "#3a2a50", RED, True) + person(460, 710, 2.7, "#14121c") + '<path d="M476 560 q10 -24 28 -10" stroke="#14121c" stroke-width="3" fill="none"/>'
    b += f'<rect x="395" y="560" width="26" height="24" fill="#5a5a60"/>'    # hammer-head hint
    return svg(b, d)


def ii3():   # Solokha's hut: the stove, pots, the witch has just slipped out of the chimney
    d, b = room("#241a16", "#34241c")
    b += stove(780, 690, 520, 470, True) + glow(1040, 540, 600, .3)
    b += "".join(f'<path d="M{x} 690 q-30 -2 -34 -44 q0 -26 34 -26 q34 0 34 26 q-4 42 -34 44 Z" fill="#2a2024"/><rect x="{x-38}" y="{610}" width="76" height="12" fill="#3a2a2c"/>' for x in (860, 960, 1150, 1230))
    b += win(160, 150, 240, 300, False) + bench(100, 560) + f'<path d="M180 690 h360" stroke="{PAPER}" stroke-width="4" opacity=".3"/>'
    b += woman(500, 730, 2.5, "#2a3a5a", "#3a8a5a") + '<path d="M470 690 q20 40 60 6" stroke="#d9b49a" stroke-width="6" fill="none"/>'
    b += '<path d="M1300 260 q-30 60 20 130" stroke="#cfd4e8" stroke-width="14" fill="none" opacity=".25"/>' + devil(1470, 760, .7, -1)
    return svg(b, d)


def ii4():   # the forge, and the painted board of Saint Peter driving the devil out of hell
    d, b = room("#1a1514", "#2a201c", 680)
    b += f'<rect x="920" y="130" width="560" height="440" fill="#3a2a22"/><rect x="940" y="150" width="520" height="400" fill="#c9a86a"/>'
    b += f'<circle cx="1050" cy="270" r="40" fill="#e8d6a0"/><rect x="1020" y="310" width="60" height="150" rx="10" fill="#5a6a9a"/><path d="M1080 340 L1110 330 L1110 420 L1090 420 Z" fill="{GOLD}"/>'
    b += f'<path d="M1260 220 q-60 70 -30 150 q50 40 130 -10 q30 -90 -100 -140 Z" fill="#c4432e" opacity=".9"/><circle cx="1290" cy="300" r="22" fill="#1c1418"/><polygon points="1276,282 1270,258 1286,278" fill="#1c1418"/><polygon points="1304,282 1316,260 1316,284" fill="#1c1418"/>'
    b += f'<path d="M1180 470 l90 -150" stroke="#2a1c14" stroke-width="7"/>'
    b += f'<rect x="150" y="480" width="360" height="180" rx="8" fill="#2a2a30"/><rect x="120" y="460" width="420" height="40" rx="8" fill="#3a3a44"/><rect x="190" y="660" width="40" height="40" fill="#2a2a30"/><rect x="420" y="660" width="40" height="40" fill="#2a2a30"/>'
    b += f'<path d="M560 330 H830 V680 H560 Z" fill="#4a3a32"/><path d="M590 680 V420 Q695 330 800 420 V680 Z" fill="#1a1010"/><path d="M620 680 V470 Q695 410 770 470 V680 Z" fill="#e8742e" opacity=".9"/>' + glow(695, 580, 480, .3)
    b += person(360, 440, 1.9, "#14121c") + f'<path d="M388 380 L470 300" stroke="#14121c" stroke-width="12"/><rect x="456" y="284" width="36" height="22" fill="#5a5a66" transform="rotate(-30 470 300)"/>'
    b += "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="#f6c24a"/>' for x, y in ((430, 470), (460, 440), (480, 480), (500, 450)))
    return svg(b, d)


# ============================================================== PART III
def iii1():  # the blizzard
    r = R(31); d, b = sky("#2a3050", "#8e98b8")
    b += ground(640, "#dfe6f6") + hut(1060, 720, 380, 170, True, smoke=False)
    b += cossack(520, 760, 1.7, "#2a2024") + cossack(380, 780, 1.5, "#1a1418", hat="#3a2a1c")
    for i in range(70):
        x = r.randint(-100, 1600); y = r.randint(0, 900); L = r.randint(60, 220)
        b += f'<path d="M{x} {y} q{L*.4} {-L*.1} {L} {L*.15}" stroke="#fff" stroke-width="{r.randint(3,9)}" fill="none" opacity="{r.uniform(.25,.7):.2f}" stroke-linecap="round"/>'
    b += devil(1180, 330, .7, -1) + flakes(r, 120, op=.8)
    return svg(b, d)


def iii2():  # Chub at his own door, which is Levchenko's... the blacksmith in the doorway
    r = R(32); d, b = sky("#0c1230", "#262e58")
    b += stars(r, 40, 1600, 300) + ground(650, "#c3cfe8") + hut(420, 740, 760, 360, True, door=False)
    b += f'<rect x="760" y="440" width="150" height="300" fill="{GOLD}"/><rect x="740" y="430" width="190" height="310" fill="none" stroke="#3a2418" stroke-width="16"/>' + glow(835, 600, 520, .3)
    b += person(835, 650, 2.9, "#14121c") + '<path d="M800 460 q40 -20 70 0" stroke="#ffffff" stroke-width="0" fill="none"/>'
    b += cossack(300, 790, 2.1, "#2a2024", hat="#3a2a1c") + '<path d="M370 640 L410 560" stroke="#2a1c14" stroke-width="7"/>'
    b += flakes(r, 90, op=.7)
    return svg(b, d)


def iii3():  # the moon escapes through Solokha's chimney: the village is silver again, carollers come out
    r = R(33); d, b = sky("#0b1230", "#2c3b72")
    b += stars(r, 110, 1600, 400) + moon(720, 190, 70) + ground(620, SNOW)
    b += hut(120, 720, 360, 160, True, smoke=True) + hut(1020, 700, 400, 170, True) + fir(1560, 720, 300)
    b += '<path d="M330 450 Q480 300 690 200" stroke="#fff1c4" stroke-width="4" fill="none" opacity=".4" stroke-dasharray="10 12"/>'
    for i, x in enumerate((620, 700, 780, 860, 940)):
        b += (woman if i % 2 else cossack)(x, 800, .9 + (i % 3) * .05, ["#3a2a50", "#2a2024", "#2a3a5a", "#1a1418", "#3a2a30"][i]) if i % 2 == 0 else woman(x, 800, .9, "#3a2a50", RED, True)
    b += f'<g fill="#fff" opacity=".9"><path d="M180 440 l8 -22 l8 22 l22 8 l-22 8 l-8 22 l-8 -22 l-22 -8 z"/></g>' + flakes(r, 80, op=.6)
    return svg(b, d)


# ============================================================== PART IV
def iv1():   # Solokha's hut: a table, the Headman and the deacon visiting, sacks on the floor
    d, b = room("#241a16", "#34261e")
    b += stove(60, 690, 440, 420, True) + win(640, 150, 200, 260, False) + glow(300, 520, 620, .28) + icon_corner(1200, 140)
    b += table(660, 650, 1250) + f'<rect x="820" y="590" width="40" height="70" rx="10" fill="#3a6a4a"/><rect x="830" y="560" width="20" height="34" fill="#3a6a4a"/><circle cx="1000" cy="640" r="26" fill="#d6c4a0"/>'
    b += woman(1010, 600, 2.1, "#2a3a5a", "#3a8a5a") if False else woman(740, 640, 2.4, "#2a3a5a", "#3a8a5a")
    b += cossack(1120, 700, 2.0, "#2a2a3a", hat="#2a1c14") + sack(560, 840, 1.0) + sack(1300, 850, .85, "#7a5a3a")
    return svg(b, d)


def iv2():   # the blacksmith's sacks: Vakula heaves them up, not knowing who is inside
    d, b = room("#241a16", "#2e2018")
    b += win(1180, 140, 220, 280, False) + glow(500, 500, 520, .24) + candle(380, 690, 70)
    b += sack(540, 830, 1.5) + sack(800, 840, 1.45, "#8a6a44") + sack(1000, 850, .95, "#7a5a3a")
    b += person(300, 700, 2.9, "#14121c") + '<path d="M270 540 q-30 40 20 80" stroke="#14121c" stroke-width="14" fill="none"/>'
    b += '<path d="M560 340 q30 -34 60 -10" stroke="#f6d34a" stroke-width="0" fill="none"/><circle cx="1010" cy="660" r="6" fill="#f6d34a"/><circle cx="1030" cy="662" r="6" fill="#f6d34a"/>'
    return svg(b, d)


def iv3():   # Vakula walks away through the frost with the sacks on his back, whistling
    r = R(43); d, b = sky("#0b1230", "#2c3b72")
    b += stars(r, 90, 1600, 400) + moon(1180, 170, 56) + ground(620, SNOW)
    b += hut(80, 700, 340, 150, True, smoke=True) + hut(1100, 720, 380, 160, True) + fir(620, 740, 300) + fir(540, 750, 220)
    b += sack(860, 800, 1.4) + sack(930, 790, 1.1) + person(820, 760, 2.6, "#14121c") + devil(760, 820, .5, 1)
    b += '<path d="M700 520 q16 -20 28 0 q12 -20 28 0" stroke="#e8eefc" stroke-width="4" fill="none" opacity=".7"/>' + flakes(r, 70, op=.55)
    return svg(b, d)


# ============================================================== PART V
def v1():    # carollers in the street under the moon
    r = R(51); d, b = sky("#0b1230", "#2c3b72")
    b += stars(r, 110, 1600, 380) + moon(1300, 170, 60) + ground(600, SNOW)
    b += hut(1050, 700, 420, 180, True, smoke=True) + hut(40, 690, 360, 170, True)
    b += f'<path d="M0 840 Q700 760 1600 830 L1600 900 L0 900 Z" fill="{SNOW2}" opacity=".6"/>'
    for i in range(9):
        x = 360 + i * 80 + r.randint(-14, 14)
        b += (cossack(x, 790 + (i % 3) * 20, 1.1, ["#2a2024", "#1a1418", "#2a2a3a"][i % 3]) if i % 2 == 0 else woman(x, 790 + (i % 3) * 20, 1.1, ["#3a2a50", "#2a3a5a", "#4a2a3a"][i % 3], RED, True))
    b += f'<path d="M560 640 l16 -40 l16 40 l40 16 l-40 16 l-16 40 l-16 -40 l-40 -16 z" fill="{GOLD}" transform="translate(300 -140) scale(.8)"/>' + flakes(r, 70, op=.55)
    return svg(b, d)


def v2():    # Patsyuk: a vast man in vast trousers on the floor, dumplings flying into his mouth
    d, b = room("#241a14", "#2e2118")
    b += glow(800, 500, 600, .24) + icon_corner(1250, 130) + win(140, 140, 230, 280, False)
    b += f'<ellipse cx="800" cy="720" rx="330" ry="100" fill="#3a5a7a"/><path d="M520 720 Q540 560 800 540 Q1060 560 1080 720 Z" fill="#a83a2a"/><path d="M520 720 Q540 600 800 580 Q1060 600 1080 720 Z" fill="#c4432e"/>'
    b += f'<circle cx="800" cy="440" r="64" fill="#d6a888"/><path d="M730 410 Q800 340 870 410 Q840 400 800 396 Q760 400 730 410 Z" fill="#14121c"/><path d="M754 424 q46 -22 92 0" stroke="#14121c" stroke-width="8" fill="none"/>'
    b += f'<ellipse cx="800" cy="470" rx="26" ry="16" fill="#5a2a22"/><path d="M800 400 l0 0" stroke="#14121c"/><path d="M770 500 Q800 530 830 500" stroke="#14121c" stroke-width="6" fill="none" opacity="0"/>'
    b += f'<rect x="760" y="470" width="80" height="18" rx="9" fill="#5a2a22"/>'
    for i, (x, y) in enumerate(((880, 360), (960, 330), (1040, 360))):
        b += f'<ellipse cx="{x}" cy="{y}" rx="34" ry="22" fill="#efe3c4" transform="rotate({-20+i*10} {x} {y})"/><path d="M{x-24} {y+4} q24 14 48 0" stroke="#c8b68a" stroke-width="3" fill="none"/>'
    b += f'<path d="M870 470 Q930 420 900 380" stroke="#efe3c4" stroke-width="3" fill="none" stroke-dasharray="4 8" opacity=".6"/>'
    b += f'<ellipse cx="1180" cy="760" rx="120" ry="30" fill="{WOOD}"/><ellipse cx="1180" cy="740" rx="100" ry="24" fill="#d6dff2"/>' + person(300, 750, 2.1, "#14121c")
    return svg(b, d)


def v3():    # Vakula seizes the devil by the tail and makes the sign of the cross
    r = R(53); d, b = sky("#0b1230", "#202a54")
    b += stars(r, 60, 1600, 360) + ground(640, SNOW2) + fir(1500, 740, 330) + fir(1400, 750, 240) + moon(250, 150, 48)
    b += devil(560, 690, 1.9, 1)
    b += person(1010, 790, 2.9, "#14121c") + '<path d="M980 560 L840 740" stroke="#1c1418" stroke-width="8"/><path d="M1040 540 L1100 440" stroke="#14121c" stroke-width="14"/>'
    b += f'<path d="M1100 380 v90 M1070 410 h60" stroke="{GOLD}" stroke-width="10"/>' + glow(1100, 420, 150, .2)
    b += flakes(r, 50, op=.5)
    return svg(b, d)


def v4():    # lifting off the roofs of Dikanka, the village getting small
    r = R(54); d, b = sky("#070c26", "#1c2858")
    b += stars(r, 160, 1600, 700) + moon(1280, 190, 64)
    b += f'<path d="M0 760 Q400 700 900 750 T1600 720 L1600 900 L0 900 Z" fill="#c8d4ec" opacity=".8"/>'
    b += hut(80, 880, 220, 100, True, smoke=True) + hut(1220, 870, 240, 100, True) + church(760, 880, .6)
    b += devil(640, 420, 1.9, 1) + person(780, 330, 1.3, "#14121c") + '<path d="M720 490 q40 40 120 30" stroke="#cfd4e8" stroke-width="4" fill="none" opacity=".4"/>'
    return svg(b, d)


# ============================================================== PART VI
def vi1():   # the girls pull a big sack on a sledge over the creaking snow
    r = R(61); d, b = sky("#0b1230", "#2c3b72")
    b += stars(r, 100, 1600, 360) + moon(260, 160, 56) + ground(620, SNOW)
    b += hut(1100, 700, 420, 180, True, smoke=True) + fir(980, 740, 300)
    b += f'<rect x="460" y="760" width="520" height="22" fill="{WOOD}"/><path d="M440 790 Q440 770 470 770 M1000 790 Q1000 770 970 770" stroke="#4a3022" stroke-width="10" fill="none"/><rect x="450" y="782" width="540" height="9" fill="#2a1c14"/>'
    b += sack(640, 764, 1.7) + sack(840, 770, 1.0, "#8a6a44")
    for i, x in enumerate((360, 300, 240, 180)): b += woman(x, 790 + i * 6, 1.2, ["#3a2a50", "#2a3a5a", "#4a2a3a", "#2a4a3a"][i], RED, True)
    b += f'<path d="M370 760 L460 780" stroke="#4a3022" stroke-width="5"/>' + flakes(r, 70, op=.55)
    return svg(b, d)


def vi2():   # the friend's wife with a poker, two men holding a sack
    d, b = room("#241a14", "#34261e")
    b += f'<rect x="1000" y="170" width="260" height="520" fill="{GOLD}" opacity=".85"/><rect x="1000" y="170" width="260" height="520" fill="none" stroke="#3a2418" stroke-width="16"/>' + glow(1130, 520, 600, .3)
    b += woman(1130, 700, 3.4, "#4a2a3a", "#6a2a2a") + '<path d="M1090 520 L960 380" stroke="#3a3a44" stroke-width="12"/><path d="M960 380 q-26 -10 -20 -32" stroke="#3a3a44" stroke-width="10" fill="none"/>'
    b += sack(620, 830, 1.7) + cossack(400, 790, 2.3, "#2a2024") + cossack(840, 810, 2.0, "#1a1418", hat="#3a2a1c")
    return svg(b, d)


def vi3():   # the sack opens and Chub climbs out
    d, b = room("#2a1e18", "#3a2a22")
    b += win(1250, 140, 210, 270, False) + glow(800, 520, 640, .3) + candle(360, 690, 90) + icon_corner(160, 130)
    b += sack(800, 840, 2.2, "#9a7a52") + cossack(800, 650, 3.0, "#2a2024", hat="#3a2a1c")
    b += f'<path d="M520 840 Q800 800 1090 840 L1090 880 L520 880 Z" fill="#2a1d16"/>' + woman(450, 790, 1.9, "#3a2a50", RED, True) + woman(1180, 790, 1.9, "#2a3a5a", RED, True) + woman(1280, 800, 1.7, "#4a2a3a", RED, True)
    b += '<path d="M610 480 l-30 -40 M1000 480 l30 -40 M800 420 v-50" stroke="#f6d34a" stroke-width="6" stroke-linecap="round"/>'
    return svg(b, d)


def vi4():   # Chub's hut: Oksana and the girls round the sack, a sausage on the table, the Headman climbing out
    d, b = room("#241a14", "#34261e")
    b += stove(1100, 700, 380, 340, True) + win(140, 150, 240, 300, False) + glow(1290, 560, 520, .26)
    b += table(690, 380, 980) + f'<ellipse cx="560" cy="676" rx="70" ry="14" fill="#efe3c4"/><path d="M700 670 q50 -30 100 0" stroke="#a8583a" stroke-width="18" fill="none" stroke-linecap="round"/><ellipse cx="860" cy="672" rx="40" ry="12" fill="#c8a870"/>'
    b += woman(470, 700, 2.3, "#3a2a50", RED, True) + woman(980, 710, 2.1, "#2a3a5a", RED, True) + woman(1040, 800, 1.5, "#4a2a3a", RED, True)
    b += sack(250, 860, 1.2) + '<circle cx="760" cy="560" r="0"/>'
    return svg(b, d)


# ============================================================== PART VII
def vii1():  # the flight to Petersburg, over clouds
    r = R(71); d, b = sky("#060a20", "#1c2858")
    b += stars(r, 220, 1600, 800) + moon(1250, 200, 90)
    b += "".join(f'<ellipse cx="{x}" cy="{y}" rx="{w}" ry="{h}" fill="#3a4a7a" opacity=".55"/>' for x, y, w, h in ((200, 720, 340, 70), (700, 780, 420, 80), (1280, 740, 400, 70), (1500, 800, 300, 60)))
    b += devil(660, 460, 2.0, 1) + person(800, 360, 1.7, "#4a5a8a") + f'<rect x="770" y="272" width="60" height="9" fill="{RED}"/>'
    b += '<path d="M430 520 q-110 30 -240 20 M470 560 q-120 50 -270 60" stroke="#cfd8f0" stroke-width="5" fill="none" opacity=".4"/>'
    b += '<g transform="translate(1000 560) rotate(8)">' + witch(0, 0, .6, 0, "#1a1428") + '</g>'
    return svg(b, d)


def vii2():  # the streets of Petersburg lit for a festival
    r = R(72); d, b = sky("#101638", "#4a4a7a")
    b += petersburg_row(0, 660, 7, True, r=r) + f'<rect y="660" width="1600" height="240" fill="#d6dff2"/><path d="M500 900 L1100 900 L900 660 L700 660 Z" fill="#aab6d4" opacity=".7"/>'
    b += "".join(lamp(x, 560, 110) for x in (240, 520, 1080, 1360))
    b += "".join(f'<circle cx="{x}" cy="{y}" r="9" fill="{GOLD}"/>' for x in range(30, 1600, 60) for y in (330, 560) if r.random() > .3)
    b += f'<path d="M660 800 q60 -80 160 -70 l90 4 q40 0 60 40 l10 34 H640 Z" fill="#2a2430"/><path d="M630 850 Q610 830 640 826 H980 Q1010 832 990 850 Z" fill="#14121c"/>'
    b += cossack(780, 760, .9, "#14121c") + flakes(r, 120, op=.7)
    return svg(b, d)


def vii3():  # the palace stairs: banisters of ironwork, lamps, a tiny figure climbing
    d, b = sky("#2a2030", "#4a3a44")
    b += f'<rect y="700" width="1600" height="200" fill="#6a5a60"/>'
    for i in range(10):
        y = 700 - i * 54; x0 = 300 + i * 40
        b += f'<rect x="{x0}" y="{y}" width="{1000-i*80}" height="54" fill="{["#d6cec6","#c6beb6"][i%2]}"/><rect x="{x0}" y="{y}" width="{1000-i*80}" height="8" fill="#f0eae2"/>'
    for i in range(0, 9):
        x = 280 + i * 40; y = 700 - i * 54
        b += f'<rect x="{x}" y="{y-150}" width="10" height="150" fill="#10101a"/><path d="M{x} {y-120} q20 -20 40 0 q-20 20 -40 0" stroke="{GOLD}" stroke-width="4" fill="none"/>'
        b += f'<rect x="{1320-i*40}" y="{y-150}" width="10" height="150" fill="#10101a"/>'
    b += f'<path d="M280 550 L640 130" stroke="#10101a" stroke-width="14"/><path d="M1330 550 L970 130" stroke="#10101a" stroke-width="14"/>'
    for x in (220, 1380): b += f'<rect x="{x-5}" y="440" width="10" height="260" fill="#10101a"/><circle cx="{x}" cy="430" r="30" fill="{GOLD}"/><circle cx="{x}" cy="430" r="110" fill="{GOLD}" opacity=".14"/>'
    b += f'<rect x="640" y="60" width="330" height="70" fill="#f0eae2"/><rect x="700" y="0" width="210" height="60" fill="#d6a84a"/>'
    b += cossack(780, 410, .75, "#2a4a3a") + cossack(720, 440, .8, "#2a4a3a", hat="#1a1418") + cossack(690, 480, .82, "#2a6a3a")
    return svg(b, d)


def vii4():  # the great hall: Zaporozhians on their knees, the Empress a small figure in a pale dress, glittering chandeliers
    d, b = sky("#3a2a30", "#6a4a44")
    b += f'<rect y="620" width="1600" height="280" fill="#8a6a54"/>' + "".join(f'<path d="M{x} 620 L{x-70} 900" stroke="#6a4a38" stroke-width="3" opacity=".6"/>' for x in range(100, 1600, 200))
    for x in (160, 460, 1140, 1440): b += f'<rect x="{x-24}" y="120" width="48" height="500" fill="#e8dcc8"/><rect x="{x-34}" y="100" width="68" height="30" fill="#d6a84a"/>'
    for x in (470, 800, 1130):
        b += f'<path d="M{x} 0 V90" stroke="#d6a84a" stroke-width="5"/><path d="M{x-80} 150 Q{x} 110 {x+80} 150 L{x+50} 180 H{x-50} Z" fill="{GOLD}"/>' + "".join(f'<circle cx="{x+dx}" cy="{y}" r="9" fill="#fff6d0"/>' for dx, y in ((-70, 140), (-30, 128), (30, 128), (70, 140))) + glow(x, 170, 300, .18)
    b += f'<rect x="760" y="300" width="80" height="320" fill="#a8483a"/><path d="M740 620 L760 520 H840 L860 620 Z" fill="#d6a84a"/>'
    b += f'<path d="M780 360 q20 -40 40 0 L840 560 H760 Z" fill="#d6e0f0"/><circle cx="800" cy="336" r="20" fill="#d9b49a"/><path d="M776 322 Q800 296 824 322 Q800 310 776 322 Z" fill="#e8e8f0"/>'
    for i, x in enumerate((340, 460, 580, 1020, 1140, 1260)):
        b += cossack(x, 800 + (i % 2) * 20, 1.2, ["#2a4a3a", "#8a2a2a", "#2a3a6a"][i % 3], hat="#1a1418")
    b += f'<g transform="translate(620 870) rotate(90)">{person(0, 0, .9, "#2a6a3a")}</g>' if False else ""
    return svg(b, d)


# ============================================================== PART VIII
def viii1():   # dawn over Dikanka, snow, smoke, the church bell
    r = R(81); d, b = sky("#2a2e5a", "#f0a888")
    b += glow(800, 610, 420, .3, "#fff0c0") + f'<circle cx="800" cy="610" r="130" fill="#fff0c0" opacity=".9"/>'
    b += stars(r, 40, 1600, 220) + ground(640, "#f0e6ee") + church(1180, 760, 1.2)
    b += hut(80, 730, 320, 150, True, smoke=True) + hut(520, 750, 280, 130, True, smoke=True) + fir(900, 760, 300)
    b += "".join(f'<ellipse cx="{r.randint(0,1600)}" cy="{r.randint(700,880)}" rx="{r.randint(40,120)}" ry="8" fill="#f8b8a8" opacity=".35"/>' for _ in range(8)) + flakes(r, 40, op=.5)
    return svg(b, d)


def viii2():   # the church on Christmas morning: candles, backs of the villagers, the choir loft missing its blacksmith
    d, b = sky("#1a1210", "#2a1e18")
    b += f'<rect y="640" width="1600" height="260" fill="#3a2a22"/><rect x="460" y="90" width="680" height="560" fill="#c8a24a"/>'
    for i in range(4):
        b += f'<rect x="{490+i*165}" y="120" width="140" height="500" fill="{["#4a3a8a","#8a3a2a","#2a5a4a","#4a3a8a"][i]}"/><circle cx="{560+i*165}" cy="240" r="46" fill="#e8d6a0"/><rect x="{525+i*165}" y="290" width="70" height="190" rx="12" fill="{["#c4432e","#2a4a8a","#c4432e","#2a4a8a"][i]}"/>'
    b += f'<rect x="460" y="620" width="680" height="24" fill="#2a1c14"/>' + "".join(f'<rect x="{x}" y="560" width="14" height="62" fill="{PAPER}"/><path d="M{x+7} 536 q-10 16 0 24 q10 -8 0 -24" fill="{GOLD}"/><circle cx="{x+7}" cy="548" r="46" fill="{GOLD}" opacity=".16"/>' for x in range(500, 1120, 80))
    for i, x in enumerate(range(160, 1500, 130)):
        b += (woman(x, 850, 1.7, ["#3a2a50", "#2a3a5a", "#4a2a3a"][i % 3], ["#f0eadc", RED, "#f0eadc"][i % 3]) if i % 2 else cossack(x, 860, 1.7, ["#2a2024", "#1a1418"][i % 2]))
    b += f'<rect x="1200" y="260" width="300" height="20" fill="{WOOD}"/><rect x="1210" y="140" width="10" height="120" fill="{WOOD}"/><rect x="1480" y="140" width="10" height="120" fill="{WOOD}"/>'
    return svg(b, d)


def viii3():   # Vakula asleep in the hay after the night; the cock has crowed; the devil flogged away
    r = R(83); d, b = sky("#2a2e5a", "#e0a090")
    b += f'<rect y="620" width="1600" height="280" fill="#6a5030"/>' + "".join(f'<path d="M{x} 640 l{r.randint(-30,30)} {r.randint(60,160)}" stroke="#c8a850" stroke-width="5"/>' for x in range(0, 1600, 14))
    b += f'<rect x="1180" y="120" width="260" height="360" fill="#fff0c0" opacity=".5"/><rect x="1180" y="120" width="260" height="360" fill="none" stroke="#4a3022" stroke-width="14"/><line x1="1310" y1="120" x2="1310" y2="480" stroke="#4a3022" stroke-width="10"/>'
    b += f'<ellipse cx="620" cy="740" rx="300" ry="62" fill="#14121c"/><circle cx="360" cy="700" r="46" fill="#d6a888"/><path d="M316 702 Q360 636 404 702 Q360 672 316 702 Z" fill="#14121c"/><rect x="480" y="690" width="260" height="70" rx="30" fill="#2a3a5a"/>'
    b += f'<text x="440" y="610" font-family="Georgia, serif" font-size="46" fill="#fff0c0" opacity=".7">z  z  z</text>'
    b += f'<rect x="1000" y="760" width="40" height="40" fill="#7a5a32"/>' + devil(1260, 790, .5, -1)
    b += '<path d="M1380 700 q20 -50 60 -40 l10 24 q-20 20 -40 20 z" fill="#c4432e"/><circle cx="1456" cy="660" r="12" fill="#c4432e"/><path d="M1462 650 l16 -8 l-6 14 z" fill="#f6d34a"/>'
    return svg(b, d)


def viii4():   # Vakula kneels at Chub's feet; the new cap and belt
    d, b = room("#241a14", "#34261e")
    b += stove(1060, 690, 420, 380, True) + win(140, 150, 250, 310, True) + glow(1270, 540, 520, .26) + icon_corner(600, 130)
    b += f'<rect x="0" y="640" width="1600" height="6" fill="none"/>'
    b += cossack(780, 700, 2.7, "#2a2024", hat="#3a2a1c") + '<path d="M690 560 L610 650" stroke="#2a1c14" stroke-width="7"/>'
    b += f'<g transform="translate(440 840)"><ellipse cx="0" cy="-30" rx="100" ry="30" fill="#2a4a3a"/><circle cx="-30" cy="-100" r="32" fill="#d6a888"/><path d="M-70 -110 Q-30 -150 10 -110 Z" fill="#14121c"/><path d="M-80 -70 Q0 -90 80 -70 L96 -10 L-96 -10 Z" fill="#2a4a3a"/></g>'
    b += f'<ellipse cx="1010" cy="860" rx="70" ry="24" fill="#3a2a1c"/><rect x="1130" y="850" width="150" height="14" fill="{RED}"/><rect x="1130" y="850" width="150" height="5" fill="{GOLD}"/>'
    return svg(b, d)


def viii5():   # the shoes: Vakula and Oksana, the pair of small embroidered shoes between them
    d, b = room("#2a1e1a", "#3c2a24")
    b += win(150, 140, 240, 300, True) + glow(800, 520, 700, .3) + icon_corner(1300, 130)
    b += f'<g transform="translate(740 840)"><path d="M0 0 Q-10 -60 30 -66 Q70 -64 90 -30 L100 0 Z" fill="{RED}"/><path d="M0 0 H100" stroke="{GOLD}" stroke-width="8"/><circle cx="40" cy="-40" r="8" fill="{GOLD}"/></g>'
    b += f'<g transform="translate(870 850)"><path d="M0 0 Q-10 -60 30 -66 Q70 -64 90 -30 L100 0 Z" fill="{RED}"/><path d="M0 0 H100" stroke="{GOLD}" stroke-width="8"/><circle cx="40" cy="-40" r="8" fill="{GOLD}"/></g>'
    b += woman(1020, 760, 3.0, "#3a2a50", RED, True) + person(560, 770, 3.2, "#2a3a5a") 
    b += '<path d="M600 640 Q690 700 970 650" stroke="#d9b49a" stroke-width="12" fill="none" stroke-linecap="round"/>'
    return svg(b, d)


def viii6():   # a year on: the painted hut, red-rimmed windows, Cossacks with pipes on the door; the bishop's carriage passes
    r = R(86); d, b = sky("#6a8ab8", "#e8d6c0")
    b += ground(600, "#f2f0f6") + f'<rect x="420" y="360" width="520" height="280" fill="{HUTW}"/><polygon points="380,380 680,230 980,380" fill="{THATCH}"/><path d="M394 372 L680 240 L966 372 Q840 356 680 366 Q520 356 394 372 Z" fill="{SNOW}"/>'
    for x in (470, 760): b += f'<rect x="{x}" y="420" width="130" height="150" fill="#6aa0d0"/><rect x="{x-12}" y="408" width="154" height="174" fill="none" stroke="#c4432e" stroke-width="12"/><line x1="{x+65}" y1="420" x2="{x+65}" y2="570" stroke="#c4432e" stroke-width="6"/>'
    b += f'<rect x="640" y="440" width="86" height="200" fill="#d6a848"/><g transform="translate(683 520)"><circle cx="0" cy="-20" r="9" fill="#14121c"/><path d="M-14 -10 L14 -10 L18 30 L-18 30 Z" fill="#c4432e"/><path d="M-26 40 q26 -34 52 0 Z" fill="#14121c"/></g>'
    b += "".join(f'<circle cx="{x}" cy="{y}" r="7" fill="#c4432e"/><circle cx="{x}" cy="{y}" r="3" fill="{GOLD}"/>' for x, y in ((440, 600), (900, 600), (460, 620), (880, 620)))
    b += woman(1060, 760, 2.0, "#3a2a50", RED, True) + f'<ellipse cx="1090" cy="660" rx="22" ry="14" fill="#f0eadc"/>'
    b += f'<path d="M1180 700 q40 -90 140 -80 l150 12 q40 6 50 50 l4 40 H1170 Z" fill="#2a2430"/><circle cx="1240" cy="754" r="34" fill="#14121c"/><circle cx="1430" cy="754" r="34" fill="#14121c"/><rect x="1260" y="640" width="170" height="70" fill="#6a2a2a"/>'
    b += fir(180, 700, 300) + fir(100, 720, 230) + church(1500, 640, .6, True) + flakes(r, 60, op=.6)
    return svg(b, d)



# ============================================================== EXTRA SCENE PICTURES (video)
def x33():   # the district clerk crawls out of the tavern; the moon dances
    r = R(133); d, b = sky("#0b1230", "#1c2858")
    b += stars(r, 80, 1600, 400) + moon(1100, 200, 60)
    b += '<path d="M1010 270 q-30 40 0 80 M1200 250 q30 40 0 80 M1100 300 q-10 40 -4 66" stroke="#fff1c4" stroke-width="5" fill="none" opacity=".5"/>'
    b += ground(660, SNOW2) + hut(160, 740, 520, 230, True, wins=2)
    b += f'<g fill="#14121c"><ellipse cx="1000" cy="770" rx="70" ry="30"/><circle cx="1090" cy="760" r="22"/><rect x="940" y="780" width="12" height="44"/><rect x="1010" y="780" width="12" height="44"/><rect x="1050" y="776" width="12" height="46"/></g><path d="M1070 745 q22 -26 44 -2" stroke="#14121c" stroke-width="10" fill="none"/>'
    b += glow(420, 640, 360, .2) + flakes(r, 40, op=.5)
    return svg(b, d)


def x34():   # in the sudden dark, the devil whispers to the witch
    r = R(134); d, b = sky("#03050f", "#0a0f26")
    b += stars(r, 24, 1600, 500) + '<path d="M0 760 Q400 720 900 760 T1600 740 L1600 900 L0 900 Z" fill="#141a38"/>'
    b += devil(640, 520, 1.9, 1) + witch(1060, 430, 1.5, 4, "#1a1428")
    b += '<path d="M780 400 q60 -30 130 0" stroke="#f6d34a" stroke-width="3" fill="none" opacity=".8"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="3" fill="{MOON}"/>' for x, y in ((1020, 520), (1040, 540), (1000, 545), (1070, 530)))
    b += glow(690, 450, 320, .1, "#f6d34a")
    return svg(b, d)


def x35():   # Chub's yard: stacks of grain, oxen, the bearded goat on the roof
    r = R(135); d, b = sky("#0c1230", "#2a3a6c")
    b += stars(r, 70, 1600, 380) + moon(1350, 160, 50) + ground(620, SNOW) + hut(560, 700, 480, 210, True, smoke=True)
    for x in (70, 190, 310, 1240, 1360, 1480):
        b += f'<path d="M{x-55} 760 Q{x-40} 640 {x} 600 Q{x+40} 640 {x+55} 760 Z" fill="#c8a850"/><path d="M{x-48} 690 Q{x} 570 {x+48} 690 Q{x} 660 {x-48} 690 Z" fill="{SNOW}"/>'
    b += f'<rect x="980" y="480" width="10" height="20" fill="#14121c"/>' + f'<g transform="translate(790 470)"><ellipse cx="0" cy="0" rx="38" ry="22" fill="#e8e0d0"/><circle cx="36" cy="-16" r="14" fill="#e8e0d0"/><path d="M44 -6 l6 34" stroke="#e8e0d0" stroke-width="5"/><rect x="-26" y="14" width="6" height="22" fill="#e8e0d0"/><rect x="18" y="14" width="6" height="22" fill="#e8e0d0"/></g>'
    for x in (380, 450):
        b += f'<g transform="translate({x} 780)"><ellipse cx="0" cy="-40" rx="60" ry="34" fill="#5a3a2a"/><circle cx="62" cy="-52" r="22" fill="#5a3a2a"/><path d="M56 -72 q-12 -22 -26 -18 M74 -72 q10 -22 24 -16" stroke="#e8e0d0" stroke-width="6" fill="none"/><rect x="-44" y="-12" width="12" height="40" fill="#4a2a1a"/><rect x="26" y="-12" width="12" height="40" fill="#4a2a1a"/></g>'
    b += flakes(r, 50, op=.5)
    return svg(b, d)


def x36():   # the tavern door in the dark, a sack lying in the road, the lean friend staring at it
    r = R(136); d, b = sky("#080c22", "#1c2650")
    b += stars(r, 40, 1600, 300) + moon(260, 150, 44) + ground(640, SNOW2) + hut(900, 720, 560, 250, True, wins=2)
    b += sack(500, 790, 1.6) + cossack(300, 800, 2.1, "#2a2024") + '<path d="M330 650 L420 700" stroke="#2a2024" stroke-width="12"/>' + glow(1180, 620, 380, .2) + flakes(r, 70, op=.6)
    return svg(b, d)


def x37():   # Odarka's new shoes; Vakula in the corner
    d, b = room("#241a14", "#34261e")
    b += win(1250, 140, 220, 280, False) + glow(640, 520, 640, .28) + icon_corner(120, 130)
    for i, x in enumerate((420, 560, 720, 860)): b += woman(x, 730 + (i % 2) * 30, 2.1, ["#3a2a50", "#2a3a5a", "#4a2a3a", "#2a4a3a"][i], RED, True)
    b += f'<g transform="translate(580 840)"><path d="M0 0 Q-6 -34 22 -40 Q50 -38 60 -16 L64 0 Z" fill="{RED}"/><path d="M0 0 H64" stroke="{GOLD}" stroke-width="6"/></g>'
    b += person(1230, 740, 2.8, "#14121c") + bench(1020, 380, 720)
    return svg(b, d)


def x38():   # the deacon's long fingers and Solokha's arm
    d, b = room("#241a16", "#34241c")
    b += stove(90, 690, 420, 400, True) + glow(300, 540, 560, .28) + win(1220, 150, 200, 260, False)
    b += woman(760, 730, 3.0, "#2a3a5a", "#3a8a5a") + f'<g transform="translate(1060 730) scale(1.0)">{cossack(0, 0, 2.5, "#2a2a3a", hat="#2a1c14")}</g>'
    b += '<path d="M940 500 L850 470" stroke="#2a2a3a" stroke-width="16" stroke-linecap="round"/>' + table(700, 1180, 1500) + f'<rect x="1260" y="640" width="30" height="60" rx="8" fill="#3a6a4a"/>'
    return svg(b, d)


def x39():   # Vakula runs away with a sack, the lads shout after him
    r = R(139); d, b = sky("#0b1230", "#2c3b72")
    b += stars(r, 100, 1600, 380) + moon(1280, 170, 56) + ground(620, SNOW) + hut(1100, 700, 380, 170, True, smoke=True)
    b += person(700, 790, 2.7, "#14121c") + sack(620, 800, 1.2) + '<path d="M740 560 L800 500" stroke="#14121c" stroke-width="14"/>'
    for i, x in enumerate((200, 290, 380, 460)): b += (cossack(x, 790 + (i % 2) * 18, 1.4, ["#2a2024", "#1a1418"][i % 2]) if i % 2 == 0 else woman(x, 790, 1.4, "#3a2a50", RED, True))
    b += '<path d="M470 600 l30 -20 M510 640 l40 -6" stroke="#fff1c4" stroke-width="5" opacity=".6"/>' + flakes(r, 60, op=.5)
    return svg(b, d)


def x40():   # the devil sits on Vakula's neck and whispers
    r = R(140); d, b = sky("#080c22", "#18224c")
    b += stars(r, 70, 1600, 380) + moon(1300, 150, 44) + ground(640, SNOW2) + hut(1060, 740, 440, 200, True, smoke=True) + fir(260, 760, 320)
    b += person(700, 780, 3.2, "#14121c") + devil(700, 380, .8, 1, col="#5a3a48") + glow(700, 470, 260, .12, "#f6d34a") + flakes(r, 50, op=.5)
    return svg(b, d)


def x41():   # Oksana at her gate, thinking about what she said
    r = R(141); d, b = sky("#0b1230", "#2c3b72")
    b += stars(r, 90, 1600, 380) + moon(300, 170, 56) + ground(640, SNOW) + hut(840, 720, 520, 220, True, smoke=True, wins=2)
    b += woman(520, 800, 2.8, "#3a2a50", RED, True) + f'<rect x="420" y="640" width="14" height="170" fill="{WOOD}"/><rect x="620" y="640" width="14" height="170" fill="{WOOD}"/><rect x="410" y="680" width="240" height="10" fill="{WOOD}"/>'
    for i, x in enumerate((150, 230, 1500)): b += woman(x, 810, 1.3, ["#2a3a5a", "#4a2a3a", "#2a4a3a"][i], RED, True)
    b += flakes(r, 60, op=.5)
    return svg(b, d)


def x42():   # the friend and the weaver carry the sack on sticks
    r = R(142); d, b = sky("#0b1230", "#2c3b72")
    b += stars(r, 90, 1600, 380) + moon(1250, 160, 54) + ground(620, SNOW) + hut(40, 700, 340, 160, True) + hut(1180, 710, 380, 170, True, smoke=True)
    b += cossack(520, 790, 2.2, "#2a2024") + cossack(900, 800, 2.1, "#1a1418", hat="#3a2a1c")
    b += f'<path d="M560 590 L950 600" stroke="{WOOD}" stroke-width="12"/>' + sack(740, 640, 1.2) + flakes(r, 50, op=.5)
    return svg(b, d)


def x43():   # the Zaporozhians on silk sofas, smoking; Vakula bows at the door
    d, b = room("#2a2030", "#4a3040")
    b += win(120, 130, 200, 300, True) + win(1280, 130, 200, 300, True) + glow(800, 520, 700, .26)
    b += "".join(f'<rect x="{x}" y="640" width="400" height="70" rx="20" fill="#7a2a3a"/><rect x="{x}" y="590" width="400" height="60" rx="16" fill="#8a3a4a"/>' for x in (340, 860))
    for i, (x, c) in enumerate(((420, "#2a3a8a"), (550, "#8a2a2a"), (940, "#2a6a3a"), (1080, "#8a2a2a"))):
        b += f'<g transform="translate({x} 610)"><circle cx="0" cy="-80" r="24" fill="#d9a888"/><path d="M-20 -86 Q0 -120 20 -86 Z" fill="#14121c"/><path d="M-28 -60 Q0 -76 28 -60 L40 10 L-40 10 Z" fill="{c}"/><path d="M-12 -70 q12 8 24 0" stroke="#14121c" stroke-width="5" fill="none"/></g><path d="M{x+30} 560 q30 -20 20 -60 q-10 -24 20 -40" stroke="#cfd4e8" stroke-width="8" fill="none" opacity=".4"/>'
    b += person(160, 800, 2.6, "#14121c") + f'<path d="M150 560 q-20 30 10 50" stroke="#14121c" stroke-width="12" fill="none"/>'
    return svg(b, d)


def x44():   # Vakula before a great painting in a palace hall
    d, b = sky("#3a2a30", "#5a4046")
    b += f'<rect y="640" width="1600" height="260" fill="#8a6a54"/>' + "".join(f'<path d="M{x} 640 L{x-80} 900" stroke="#6a4a38" stroke-width="3" opacity=".6"/>' for x in range(100, 1600, 200))
    b += f'<rect x="500" y="70" width="600" height="520" fill="#c8a24a"/><rect x="530" y="100" width="540" height="460" fill="#2a3a6a"/>'
    b += f'<circle cx="800" cy="260" r="60" fill="#e8d6a0"/><path d="M730 330 Q800 300 870 330 L900 540 H700 Z" fill="#8a2a3a"/><circle cx="830" cy="420" r="34" fill="#e8c8a0"/><circle cx="800" cy="260" r="80" fill="none" stroke="{GOLD}" stroke-width="5"/>' + glow(800, 330, 420, .2)
    b += person(360, 800, 3.0, "#2a6a3a") + f'<ellipse cx="360" cy="526" rx="28" ry="12" fill="#14121c"/>' + "".join(glow(x, 120, 280, .12) for x in (200, 1400))
    b += f'<rect x="1300" y="360" width="34" height="260" fill="{GOLD}" opacity=".8"/>'
    return svg(b, d)


def x45():   # the Empress, Vakula kneeling with the shoes, Potemkin behind
    d, b = sky("#3a2a30", "#6a4a44")
    b += f'<rect y="640" width="1600" height="260" fill="#8a6a54"/>' + glow(800, 420, 800, .25) + "".join(f'<rect x="{x-24}" y="80" width="48" height="560" fill="#e8dcc8"/>' for x in (120, 1480))
    b += f'<g transform="translate(980 760)"><path d="M-60 0 Q-70 -230 -20 -290 L40 -290 Q90 -230 80 0 Z" fill="#d6e0f0"/><path d="M-60 0 Q0 30 80 0 L90 40 L-70 40 Z" fill="#d6a84a"/><circle cx="10" cy="-330" r="36" fill="#e8c8a0"/><path d="M-30 -340 Q10 -400 50 -340 Q10 -370 -30 -340 Z" fill="#e8e8f0"/><path d="M-20 -372 l10 -26 l12 20 l12 -20 l10 26 Z" fill="{GOLD}"/></g>'
    b += f'<g transform="translate(560 830)"><ellipse cx="0" cy="-50" rx="110" ry="40" fill="#2a6a3a"/><circle cx="-40" cy="-130" r="34" fill="#d6a888"/><path d="M-80 -140 Q-40 -190 0 -140 Z" fill="#14121c"/><path d="M-90 -100 Q0 -120 90 -100 L110 -20 L-110 -20 Z" fill="#2a6a3a"/><path d="M60 -90 q60 -20 90 0" stroke="#d6a888" stroke-width="12" fill="none"/><path d="M150 -90 q10 -20 30 -6 l-4 14 Z" fill="{RED}"/></g>'
    b += cossack(1320, 780, 1.9, "#8a2a2a", hat="#1a1418") + person(1440, 780, 1.8, "#2a3a6a")
    return svg(b, d)


def x46():   # morning: a knot of women quarrelling in the street
    r = R(146); d, b = sky("#4a4a7a", "#f0b8a0")
    b += ground(640, "#f0e6ee") + hut(30, 700, 340, 160, True, smoke=True) + hut(1220, 710, 360, 170, True) + fir(900, 740, 300)
    for i, x in enumerate(range(520, 960, 80)): b += woman(x, 800 + (i % 2) * 20, 1.8, ["#3a2a50", "#4a2a3a", "#2a3a5a", "#2a4a3a", "#5a3a2a", "#3a2a3a"][i % 6], ["#f0eadc", RED, "#6aa0d0"][i % 3])
    b += '<path d="M600 520 l-20 -40 M780 520 l24 -44 M900 540 l30 -30" stroke="#14121c" stroke-width="8" stroke-linecap="round"/>' + flakes(r, 40, op=.5)
    return svg(b, d)


def x47():   # Oksana awake in bed, a bar of moonlight over the blanket
    d, b = sky("#0e0c1c", "#1c1830")
    b += f'<rect y="680" width="1600" height="220" fill="#241a16"/><rect x="120" y="120" width="260" height="340" fill="#2a3a6a"/><rect x="120" y="120" width="260" height="340" fill="none" stroke="#3a2418" stroke-width="12"/><line x1="250" y1="120" x2="250" y2="460" stroke="#3a2418" stroke-width="8"/>' + moon(250, 230, 36)
    b += f'<path d="M260 460 L1100 700 L1180 700 L440 450 Z" fill="{MOON}" opacity=".08"/>'
    b += f'<rect x="460" y="560" width="900" height="200" rx="26" fill="#4a3a6a"/><rect x="460" y="540" width="260" height="90" rx="30" fill="#efe7d6"/><circle cx="560" cy="540" r="46" fill="#d9b49a"/><path d="M500 540 q-30 80 -6 150 M610 520 q50 70 40 140" stroke="{RED}" stroke-width="10" fill="none"/><path d="M500 560 Q560 470 640 560 Z" fill="#14121c"/>'
    b += f'<path d="M700 600 Q900 540 1300 660 L1300 760 L700 760 Z" fill="#8a4a6a"/>' + candle(1450, 780, 60)
    return svg(b, d)


def x48():   # Patsyuk's hut at night: Vakula bowing at the door, a lit window
    r = R(148); d, b = sky("#080c22", "#1c2650")
    b += stars(r, 70, 1600, 360) + moon(1330, 150, 46) + ground(640, SNOW2) + hut(560, 740, 560, 260, True, door=False, smoke=True)
    b += f'<rect x="780" y="500" width="130" height="240" fill="{GOLD}"/><rect x="770" y="490" width="150" height="250" fill="none" stroke="#3a2418" stroke-width="12"/>' + glow(845, 620, 360, .3)
    b += person(560, 790, 2.5, "#14121c") + '<path d="M540 620 q-40 20 -70 70" stroke="#14121c" stroke-width="12" fill="none"/>' + sack(430, 800, 1.0) + fir(200, 760, 330) + flakes(r, 50, op=.5)
    return svg(b, d)


def x49():   # a varenik leaps from the bowl, through the sour cream, into the open mouth
    d, b = room("#241a14", "#2e2118", 700)
    b += glow(800, 480, 640, .3) + f'<ellipse cx="520" cy="780" rx="190" ry="48" fill="{WOOD}"/><ellipse cx="520" cy="760" rx="170" ry="38" fill="#efe3c4"/><ellipse cx="1060" cy="780" rx="190" ry="48" fill="{WOOD}"/><ellipse cx="1060" cy="760" rx="170" ry="38" fill="#d6dff2"/>'
    for x, y in ((470, 730), (560, 740), (520, 720)): b += f'<ellipse cx="{x}" cy="{y}" rx="40" ry="24" fill="#e8d8b0"/><path d="M{x-30} {y+4} q30 14 60 0" stroke="#c8b68a" stroke-width="3" fill="none"/>'
    b += f'<path d="M560 700 Q700 380 840 420" stroke="#efe3c4" stroke-width="3" fill="none" stroke-dasharray="6 10" opacity=".7"/><ellipse cx="700" cy="450" rx="44" ry="28" fill="#e8d8b0" transform="rotate(-25 700 450)"/>'
    b += f'<circle cx="1040" cy="380" r="90" fill="#d6a888"/><path d="M950 350 Q1040 270 1130 350 Q1090 336 1040 332 Q990 336 950 350 Z" fill="#14121c"/><path d="M980 340 q60 -24 120 0" stroke="#14121c" stroke-width="10" fill="none"/><ellipse cx="1000" cy="430" rx="52" ry="38" fill="#5a2a22"/><rect x="960" y="410" width="80" height="18" fill="#efe3c4"/>'
    b += f'<path d="M920 500 Q1040 560 1170 500 L1230 700 H860 Z" fill="#a83a2a"/>'
    return svg(b, d)


def x50():   # Vakula and Oksana on the bench: she with her mirror, he looking only at her
    d, b = room("#241a14", "#34261e")
    b += win(160, 150, 240, 300, False) + icon_corner(1300, 140) + glow(800, 520, 620, .28) + bench(380, 840, 700) + candle(1300, 700, 90)
    b += woman(1000, 700, 2.7, "#3a2a50", RED, True) + person(620, 700, 2.9, "#14121c")
    b += f'<rect x="1090" y="520" width="70" height="90" rx="10" fill="#5a5048"/><rect x="1098" y="528" width="54" height="74" rx="6" fill="#cfd8e8"/>'
    return svg(b, d)


def x51():   # Chub's daydream: warm on the stove-bench with a pipe, carols outside
    d, b = room("#241a14", "#34261e")
    b += stove(60, 690, 520, 420, True) + glow(330, 520, 620, .3) + win(1100, 150, 280, 320, False) + icon_corner(780, 120)
    b += f'<rect x="150" y="270" width="340" height="60" rx="20" fill="#7a5a3a"/>' + f'<g transform="translate(320 270)"><ellipse cx="0" cy="-20" rx="120" ry="40" fill="#2a2024"/><circle cx="-100" cy="-34" r="34" fill="#d6a888"/><ellipse cx="-110" cy="-62" rx="38" ry="18" fill="#3a2a1c"/><path d="M-70 -20 q70 -50 140 -30" stroke="{WOOD}" stroke-width="8" fill="none"/></g>'
    b += '<path d="M-10 0" /><path d="M196 236 q-10 -30 6 -50 q16 -20 0 -44" stroke="#cfd4e8" stroke-width="8" fill="none" opacity=".4"/>'
    b += "".join(f'<circle cx="{x}" cy="{y}" r="5" fill="#fff1c4" opacity=".7"/>' for x, y in ((1180, 200), (1260, 260), (1320, 210)))
    b += table(700, 760, 1500)
    return svg(b, d)


def x52():   # Potemkin comes into the hall, the generals bow
    d, b = sky("#3a2a30", "#6a4a44")
    b += f'<rect y="640" width="1600" height="260" fill="#8a6a54"/>' + "".join(f'<rect x="{x-24}" y="100" width="48" height="540" fill="#e8dcc8"/>' for x in (130, 1470)) + glow(800, 300, 800, .2)
    b += f'<g transform="translate(800 790)"><path d="M-70 0 Q-80 -240 -40 -300 L40 -300 Q80 -240 70 0 Z" fill="#2a4a8a"/><path d="M-40 -300 L0 -200 L40 -300 Z" fill="{GOLD}"/><circle cx="0" cy="-336" r="34" fill="#d6a888"/><path d="M-36 -350 Q0 -400 36 -350 Q0 -372 -36 -350 Z" fill="#14121c"/><rect x="-60" y="-8" width="40" height="46" fill="#e0b82a"/><rect x="20" y="-8" width="40" height="46" fill="#e0b82a"/></g>'
    for i, x in enumerate((300, 420, 1180, 1300, 520, 1080)):
        b += cossack(x, 800 - (i // 4) * 30, 1.5, ["#8a2a2a", "#2a3a6a", "#2a4a3a"][i % 3], hat="#d6a84a") + f'<rect x="{x-18}" y="{700-(i//4)*30}" width="36" height="14" fill="{GOLD}"/>'
    b += "".join(glow(x, 150, 260, .14) for x in (350, 800, 1250))
    return svg(b, d)

# ============================================================== COVERS
def cover(ru=False):
    r = R(8); d, b = sky("#0a0f2e", "#2c3a72", 3000, 3000)
    b += stars(r, 160, 3000, 1500)
    b += moon(2280, 1180, 190) + '<rect y="2200" width="3000" height="800" fill="#e8eefc"/><path d="M0 2230 Q700 2150 1500 2220 T3000 2200 L3000 2300 L0 2300 Z" fill="#c3cfe8" opacity=".8"/>'
    sc = 2.4
    b += f'<g transform="translate(0 0) scale(1)">' + hut(300, 2480, 760, 330, True, smoke=True).replace("<g", "<g") + '</g>'
    b += hut(1750, 2400, 900, 380, True) + fir(1500, 2540, 780) + fir(1300, 2600, 560) + fir(2850, 2560, 600)
    b += f'<g transform="translate(1320 1580) scale(3.2)">{witch(0, 0, 1, -14)}</g>'
    b += '<path d="M1180 1700 q-160 160 -480 330" stroke="#cfd4e8" stroke-width="30" fill="none" opacity=".25"/>' + "".join(f'<circle cx="{r.randint(0,3000)}" cy="{r.randint(1300,3000)}" r="{r.uniform(4,9):.1f}" fill="#fff" opacity=".8"/>' for _ in range(160))
    b += f'<g transform="translate(560 2740) scale(2.4)">{devil(0, 0, 1, 1)}</g>' if False else ""
    T = (("МИКОЛА ГОГОЛЬ".replace("МИКОЛА", "НИКОЛАЙ"), ("Ночь перед", "Рождеством")) if ru else ("NIKOLAI GOGOL", ("The Night Before", "Christmas")))
    b += (f'<text x="1500" y="340" text-anchor="middle" font-family="Georgia, serif" font-size="92" letter-spacing="30" fill="#e3c27a">{T[0]}</text>'
          f'<text x="1500" y="640" text-anchor="middle" font-family="Georgia, serif" font-weight="bold" font-size="250" fill="{PAPER}">{T[1][0]}</text>'
          f'<text x="1500" y="900" text-anchor="middle" font-family="Georgia, serif" font-weight="bold" font-size="250" fill="{PAPER}">{T[1][1]}</text>'
          f'<rect x="1200" y="990" width="600" height="8" fill="#e3c27a"/><rect x="1330" y="1020" width="340" height="5" fill="#e3c27a"/>')
    return svg(b, d, 3000, 3000)


FILES = {
    "1_village_night": i1, "2_witch_stars": i2, "3_devil_moon": i3, "4_chub_road": i4,
    "5_oksana_mirror": ii1, "6_chest": ii2, "7_solokha_stove": ii3, "8_forge_board": ii4,
    "9_blizzard": iii1, "10_chub_door": iii2, "11_moon_returns": iii3,
    "12_solokha_hut": iv1, "13_sacks_floor": iv2, "14_vakula_sacks": iv3,
    "15_carollers": v1, "16_patsyuk": v2, "17_devil_tail": v3, 
    "19_sledge": vi1, "20_poker": vi2, "21_chub_sack": vi3, "22_chub_hut": vi4,
    "23_flight": vii1, "24_petersburg": vii2, "25_palace_stairs": vii3, "26_great_hall": vii4,
    "27_dawn": viii1, "28_church": viii2, "29_hay": viii3, "30_chub_whip": viii4, "31_shoes": viii5, "32_painted_hut": viii6,
    "34_dark_embrace": x34, "35_chub_farm": x35, "36_tavern_sack": x36, "37_odarka_shoes": x37, "38_deacon_arm": x38,
    "39_farewell": x39, "40_devil_neck": x40, "41_oksana_gate": x41, "42_two_men_carry": x42, "43_zaporozhian_room": x43, "44_painting_hall": x44,
    "45_empress_shoes": x45, "48_patsyuk_door": x48, "49_varenik": x49, "50_bench_talk": x50, "51_chub_dream": x51, "52_potemkin": x52, "46_women_street": x46, "47_oksana_bed": x47,
    "cover": cover, "cover_ru": lambda: cover(True)}
if __name__ == "__main__":
    for n, fn in FILES.items():
        open(f"{OUT}/{n}.svg", "w", encoding="utf-8").write(fn()); print("wrote", n)
