"""Props and people for The Little Humpbacked Horse pictures (soft, rounded, friendly; same style as Tsar Saltan)."""
from art_props import *

IV = dict(coat="#e0564a", hat="cap", beard=None, hatcol="#3a7ad8", pants="#3a3a5a", young=True)
DAN = dict(coat="#4a7ab8", hat="cap", beard="#7a4a2a", hatcol="#8a5a3a", pants="#3a3a5a")
GAV = dict(coat="#4a9a6a", hat="cap", beard="#5a3a2a", hatcol="#8a5a3a", pants="#3a3a5a")
FAT = dict(coat="#9a7ab8", hat="cap", beard="#ecece8", hatcol="#8a5a3a", pants="#4a3a4a")
CHB = dict(coat="#7a4a8a", hat="cap", beard="#3a2a2a", hatcol="#4a2a5a", pants="#2a2a3a")
NOB = dict(coat="#2a8aa0", hat="cap", beard="#6a5a4a", hatcol="#c0392b", pants="#3a3a5a")
MAID = dict(robe="#eaf4ff", trim="#8cc4ee", hair="#e0b860", hat="kokoshnik")
QN = dict(robe="#ff9ec0", trim=GOLD, hair="#5a3a2a", hat="kokoshnik")
BLACKH = dict(col="#3a3f5a", mane=GOLD, saddle="#e0564a")


def konek(x, y, s=1.0, flip=1, mood="smile", jump=False):
    """The Little Humpbacked Horse: small, warm brown, two humps, very long ears."""
    c = "#c98a52"
    g = f'<g transform="translate({x} {y - (30*s if jump else 0)}) scale({s*flip} {s})"><ellipse cx="0" cy="6" rx="110" ry="10" fill="#000" opacity=".1"/>'
    g += "".join(f'<rect x="{lx}" y="-62" width="22" height="66" rx="10" fill="#a8703c"/>' for lx in (-70, -42, 36, 64))
    g += f'<path d="M-96 -96 Q-120 -70 -110 -30 Q-96 -64 -84 -76 Z" fill="#6a3a1a"/>'
    g += f'<ellipse cx="0" cy="-92" rx="100" ry="46" fill="{c}"/>'
    g += f'<ellipse cx="-34" cy="-134" rx="30" ry="34" fill="{c}"/><ellipse cx="22" cy="-132" rx="28" ry="32" fill="{c}"/>'
    g += f'<path d="M70 -112 Q96 -168 124 -168 Q146 -160 152 -138 L156 -112 Q130 -96 96 -88 Z" fill="{c}"/>'
    g += f'<ellipse cx="150" cy="-124" rx="20" ry="16" fill="{c}"/><circle cx="130" cy="-146" r="6" fill="{INK}"/><circle cx="130" cy="-148" r="2" fill="#fff"/><circle cx="156" cy="-124" r="3.5" fill="#d8a090"/>'
    g += f'<path d="M142 -108 Q150 {-100 if mood != "open" else -94} 160 -108" stroke="{INK}" stroke-width="3.5" fill="none" stroke-linecap="round"/><circle cx="112" cy="-130" r="9" fill="{ROSE}" opacity=".5"/>'
    g += f'<path d="M96 -158 Q74 -250 40 -272 Q50 -210 84 -150 Z" fill="{c}" stroke="#a8703c" stroke-width="3"/><path d="M104 -158 Q96 -250 120 -280 Q134 -220 118 -150 Z" fill="{c}" stroke="#a8703c" stroke-width="3"/>'
    g += f'<path d="M92 -168 Q60 -176 70 -128" stroke="#6a3a1a" stroke-width="14" fill="none" stroke-linecap="round"/>'
    return g + '</g>'


def ride(kx, ky, ks=1.0, flip=1, back=False, mood="smile", jump=False, who=IV, ms=.62, hold=""):
    """Ivan sitting on the little horse (a small man drawn over its back)."""
    m = man(kx - flip * 4 * ks, ky - (30*ks if jump else 0) - 95 * ks, ms * ks * 1.0, mood=mood, flip=flip * (-1 if back else 1), lh=(-40, -90), rh=(50, -80), hold=hold, **who)
    return konek(kx, ky, ks, flip, mood, jump) + m


def firebird(x, y, s=1.0, flip=1, mood="smile", glow=True):
    g = f'<g transform="translate({x} {y}) scale({s*flip} {s})">'
    if glow: g += f'<circle cx="0" cy="-40" r="150" fill="#ffd36b" opacity=".3"/><circle cx="0" cy="-40" r="100" fill="#ffb84a" opacity=".3"/>'
    for i, (dx, col) in enumerate(((-150, "#ff7a3a"), (-190, "#ffb84a"), (-120, "#e0564a"), (-210, "#ffd36b"))):
        g += f'<path d="M-30 -30 Q{dx} {-90 + i * 36} {dx - 60} {-120 + i * 70} Q{dx + 30} {-30 + i * 30} -10 0 Z" fill="{col}" opacity=".95"/>'
        g += f'<circle cx="{dx - 56}" cy="{-120 + i * 70}" r="12" fill="#fff6c8"/>'
    g += f'<ellipse cx="0" cy="-30" rx="64" ry="42" fill="#ff8a3a"/><path d="M-20 -40 Q30 -90 70 -40 Q30 -10 -20 -40 Z" fill="#ffb84a"/><circle cx="62" cy="-76" r="30" fill="#ff8a3a"/>'
    g += f'<path d="M80 -78 L112 -68 L82 -62 Z" fill="#ffd36b"/><circle cx="66" cy="-84" r="6" fill="{INK}"/><path d="M50 -104 Q40 -134 62 -128 M60 -106 Q58 -140 78 -130" stroke="#ffd36b" stroke-width="8" fill="none" stroke-linecap="round"/>'
    g += f'<path d="M-60 -30 Q-10 -90 30 -30" fill="#ffd36b" opacity=".8"/>'
    return g + '</g>'


def feather(x, y, s=1.0, rot=0):
    return (f'<g transform="translate({x} {y}) rotate({rot}) scale({s})"><circle r="90" fill="#ffd36b" opacity=".3"/><path d="M-70 14 Q0 -90 80 -30 Q10 0 -70 14 Z" fill="#ff8a3a"/>'
            f'<path d="M-70 14 Q-4 -30 70 -28" stroke="#fff6c8" stroke-width="5" fill="none"/></g>')


def whale(x, y, s=1.0, flip=1, village=False, mouth=False, mood="smile"):
    g = f'<g transform="translate({x} {y}) scale({s*flip} {s})">'
    g += f'<path d="M-380 -20 Q-380 -200 -120 -210 Q160 -230 310 -120 Q380 -60 380 20 Q150 70 -120 60 Q-330 50 -380 -20 Z" fill="#6a8ad8"/>'
    g += f'<path d="M-380 -20 Q-330 -190 -440 -230 Q-480 -160 -440 -90 Q-470 -20 -420 40 Q-370 20 -380 -20 Z" fill="#5a7ac8"/>'
    g += f'<path d="M-200 30 Q150 90 380 10 Q300 60 100 70 Q-120 80 -200 30 Z" fill="#c8dcf8"/>'
    g += f'<circle cx="300" cy="-50" r="18" fill="#fff"/><circle cx="306" cy="-48" r="9" fill="{INK}"/><circle cx="240" cy="-10" r="26" fill="{ROSE}" opacity=".5"/>'
    g += (f'<path d="M382 -4 Q300 40 220 20" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round"/>' if not mouth else
          f'<path d="M382 -10 Q300 90 200 40 Q300 20 382 -10 Z" fill="#a8445a"/><path d="M360 4 Q300 60 230 40" fill="#ff9c8c"/>')
    g += f'<path d="M-30 -214 Q-30 -300 -60 -330 M-30 -214 Q-10 -290 30 -320" stroke="#bfe6ff" stroke-width="12" fill="none" stroke-linecap="round"/>'
    if village:
        g += f'<path d="M-250 -170 Q-120 -230 60 -214 Q120 -204 150 -170 Q-60 -150 -250 -170 Z" fill="#8fd47c"/>'
        g += terem(-140, -190, 90, 60, "#d98a5a", "#c0392b") + terem(-20, -194, 80, 50, "#e0a060", "#4a7ab8") + fpine(70, -184, 120) + fpine(110, -184, 90)
    return g + '</g>'


def cauldron(x, y, s=1.0, kind="cold", steam=True):
    col = {"cold": "#7a9ad0", "water": "#9a8ab0", "milk": "#c8bca8"}[kind]
    fill = {"cold": "#bfe6ff", "water": "#e0eaf4", "milk": "#fffaf0"}[kind]
    g = f'<g transform="translate({x} {y}) scale({s})"><ellipse cx="0" cy="6" rx="140" ry="16" fill="#000" opacity=".12"/>'
    g += f'<path d="M-70 -30 Q-90 -90 -50 -110 L50 -110 Q90 -90 70 -30 Q0 -10 -70 -30 Z" fill="#e8742a"/><path d="M-40 -30 Q-30 -76 -4 -98 Q0 -60 14 -50 Q30 -76 40 -30 Z" fill="#ffd36b"/>'
    g += f'<ellipse cx="0" cy="-170" rx="130" ry="26" fill="{fill}"/><path d="M-130 -170 Q-140 -60 -60 -100 L60 -100 Q140 -60 130 -170 Q0 -130 -130 -170 Z" fill="{col}" stroke="#4a4a6a" stroke-width="6"/>'
    g += f'<ellipse cx="0" cy="-172" rx="124" ry="22" fill="{fill}" stroke="#4a4a6a" stroke-width="6"/>'
    if steam: g += "".join(f'<path d="M{dx} -200 Q{dx-26} -240 {dx} -280 Q{dx+26} -320 {dx} -360" stroke="#fff" stroke-width="12" fill="none" stroke-linecap="round" opacity=".7"/>' for dx in ((-40, 30) if kind != "cold" else ()))
    return g + '</g>'


def tent(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><path d="M-220 0 L0 -260 L220 0 Z" fill="#ffd36b" stroke="#d9a020" stroke-width="8"/><path d="M-220 0 L0 -260" stroke="#fff" stroke-width="0"/>'
            f'<path d="M0 -260 L-60 0 L60 0 Z" fill="#c0392b"/>' + "".join(f'<circle cx="{dx}" cy="{dy}" r="10" fill="#fff6c8"/>' for dx, dy in ((-130, -50), (130, -50), (-80, -100), (80, -100), (0, -190))) + '</g>')


def fish(x, y, s=1.0, flip=1, col="#ffb84a", mood="smile", spiky=False, mouth=False):
    g = f'<g transform="translate({x} {y}) scale({s*flip} {s})"><path d="M-70 0 Q-130 -40 -120 -10 Q-110 0 -120 10 Q-130 40 -70 0 Z" fill="{col}"/><ellipse cx="0" cy="0" rx="76" ry="42" fill="{col}"/>'
    g += f'<path d="M-30 -36 Q0 -80 40 -38 Z" fill="{col}" opacity=".8"/>' + (''.join(f'<path d="M{dx} -40 l6 -26 l6 26" fill="#e0564a"/>' for dx in (-20, 0, 20)) if spiky else '')
    g += f'<circle cx="38" cy="-8" r="9" fill="#fff"/><circle cx="41" cy="-8" r="5" fill="{INK}"/><path d="M52 16 Q62 {26 if not mouth else 34} 70 12" stroke="{INK}" stroke-width="4" fill="none" stroke-linecap="round"/><circle cx="20" cy="14" r="9" fill="{ROSE}" opacity=".5"/>'
    return g + '</g>'


def haystack(x, y, s=1.0):
    return f'<g transform="translate({x} {y}) scale({s})"><path d="M-140 0 Q-130 -150 0 -190 Q130 -150 140 0 Z" fill="#e8c460"/><path d="M-100 -20 Q-60 -90 -10 -120 M30 -140 Q70 -80 100 -20" stroke="#c8a040" stroke-width="6" fill="none"/></g>'


def hut(x, y, s=1.0, wall="#d9a56a"):
    return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-150" y="-170" width="300" height="170" rx="14" fill="{wall}"/><path d="M-185 -160 L0 -280 L185 -160 Z" fill="#e8c460"/><path d="M-185 -160 L0 -280 L185 -160" stroke="#c8a040" stroke-width="8" fill="none" stroke-linejoin="round"/>'
            f'<rect x="-40" y="-120" width="80" height="120" rx="10" fill="#8a5a3a"/><rect x="80" y="-130" width="46" height="46" rx="8" fill="{GOLD}" stroke="#8a5a3a" stroke-width="6"/></g>')


def wheat(r, y0=620, y1=880):
    b = ""
    for _ in range(120):
        x, y = r.randint(0, 1600), r.randint(y0, y1)
        b += f'<path d="M{x} {y} q-4 -40 2 -64" stroke="#d9a020" stroke-width="5" fill="none"/><ellipse cx="{x+2}" cy="{y-70}" rx="6" ry="16" fill="#f0c040"/>'
    return b


def sack(x, y, s=1.0, glow=False):
    return f'<g transform="translate({x} {y}) scale({s})"><path d="M-50 0 Q-70 -90 -26 -120 L26 -120 Q70 -90 50 0 Z" fill="#c8a870"/><path d="M-26 -120 Q0 -146 26 -120" fill="#a88850"/><path d="M-30 -118 H30" stroke="#6a4a2a" stroke-width="8"/>' + (f'<circle cy="-70" r="110" fill="#ffd36b" opacity=".35"/>' if glow else '') + '</g>'


def goat(x, y, s=1.0, flip=1):
    return (f'<g transform="translate({x} {y}) scale({s*flip} {s})"><rect x="-40" y="-40" width="12" height="44" rx="5" fill="#fff"/><rect x="26" y="-40" width="12" height="44" rx="5" fill="#fff"/><ellipse cx="0" cy="-60" rx="50" ry="28" fill="#fff"/>'
            f'<circle cx="52" cy="-86" r="20" fill="#fff"/><path d="M48 -104 Q40 -126 56 -124 M58 -104 Q64 -126 76 -118" stroke="#8a6a4a" stroke-width="5" fill="none"/><circle cx="58" cy="-88" r="3.5" fill="{INK}"/></g>')


def gal(x, y, s=1.0, flip=1, col="#3a3f5a", rider=None):
    return horse(x, y, s, flip, col=col, mane=GOLD, saddle="#e0564a", rider=rider)


def stall_row(r):
    b = room("#f0d8a8", "#c8985a")
    b += "".join(f'<rect x="{x}" y="260" width="30" height="440" fill="#9a6a3a"/>' for x in (60, 560, 1060, 1530))
    b += f'<rect x="60" y="260" width="1500" height="26" fill="#9a6a3a"/><path d="M0 520 H1600" stroke="#b07a42" stroke-width="0"/>'
    b += "".join(f'<path d="M{x} 700 q40 -40 80 0 q40 -50 80 0" fill="#e8c460" stroke="#c8a040" stroke-width="4"/>' for x in range(100, 1500, 260))
    return b


def kitchen(r):
    b = room("#f6e4c4", "#c8985a") + window(1180, 140, 260, 260, "#2c3a78")
    b += tilestove(300, 700, .8)
    b += f'<rect x="560" y="560" width="620" height="40" rx="12" fill="#a8703c"/><rect x="600" y="600" width="26" height="140" fill="#8a5a3a"/><rect x="1100" y="600" width="26" height="140" fill="#8a5a3a"/>'
    b += f'<path d="M720 560 l4 -50 h54 l4 50 Z" fill="#c8985a"/><path d="M730 510 h50" stroke="#fff6c8" stroke-width="10"/>'
    return b


def bubble(x, y, r, inner):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" opacity=".92" stroke="#d9c8a0" stroke-width="6"/><circle cx="{x-r*.7:.0f}" cy="{y+r*1.1:.0f}" r="{r*.14:.0f}" fill="#fff" opacity=".9"/>' + inner


def sky_land(r):
    b = "".join(cloud(r.randint(0, 1600), r.randint(380, 820), r.uniform(.8, 1.7), "#fff", .9) for _ in range(8))
    return b


def town_street(r):
    b = f'<circle cx="1360" cy="130" r="90" fill="#fff3b0"/>' + hills("#b2e29e", "#9ad088") + f'<rect y="700" width="1600" height="200" fill="#d9c8a0"/>'
    b += "".join(terem(x, 700, w, h, wc, rc) for x, w, h, wc, rc in ((20, 200, 180, "#d98a5a", "#c0392b"), (300, 180, 220, "#e0a060", "#4a7ab8"), (1180, 220, 200, "#d98a5a", "#8e5ac8"), (1420, 180, 170, "#e0a060", "#c0392b")))
    return b + town(800, 560, .55)


def courtyard(r):
    b = f'<circle cx="1360" cy="130" r="90" fill="#fff3b0"/>' + hills("#b2e29e", "#9ad088") + town(300, 520, .7) + f'<rect y="640" width="1600" height="260" fill="#e6d4a8"/><path d="M0 640 H1600" stroke="#c8b078" stroke-width="8"/>'
    return b + terem(1180, 660, 360, 280, "#d98a5a", "#c0392b")
