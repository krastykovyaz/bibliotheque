"""Characters and props for the Dead Princess pictures (friendly, rounded, soft colours)."""
from art_base import *

DARK = "#3a2a2a"


def hands(lh, rh, col, w=22):
    return (f'<path d="M{lh[0]*.55:.0f} -138 L{lh[0]} {lh[1]}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/><circle cx="{lh[0]}" cy="{lh[1]}" r="12" fill="{SKIN}"/>'
            f'<path d="M{rh[0]*.55:.0f} -138 L{rh[0]} {rh[1]}" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/><circle cx="{rh[0]}" cy="{rh[1]}" r="12" fill="{SKIN}"/>')


def crown(cx, cy, r, kind="crown"):
    if kind == "crown":
        return (f'<path d="M{cx-r*.7} {cy-r*.78} L{cx-r*.7} {cy-r*1.25} L{cx-r*.35} {cy-r*.98} L{cx} {cy-r*1.38} L{cx+r*.35} {cy-r*.98} L{cx+r*.7} {cy-r*1.25} L{cx+r*.7} {cy-r*.78} Z" fill="{GOLD}" stroke="#d9a020" stroke-width="4"/>'
                f'<circle cx="{cx}" cy="{cy-r*1.1}" r="{r*.08}" fill="{RED}"/>')
    if kind == "kokoshnik":     # a tall rounded Russian headdress with pearls
        return (f'<path d="M{cx-r*.95} {cy-r*.55} Q{cx-r*.9} {cy-r*1.6} {cx} {cy-r*1.65} Q{cx+r*.9} {cy-r*1.6} {cx+r*.95} {cy-r*.55} Q{cx} {cy-r*.95} {cx-r*.95} {cy-r*.55} Z" fill="#e0564a" stroke="{GOLD}" stroke-width="5"/>'
                + "".join(f'<circle cx="{cx+r*dx}" cy="{cy-r*dy}" r="{r*.07}" fill="#fff"/>' for dx, dy in ((-.6, .85), (-.3, 1.15), (0, 1.25), (.3, 1.15), (.6, .85), (0, .95))))
    return ""


def lady(x, y, s=1.0, robe="#e0564a", trim=GOLD, hair=DARK, hat="crown", mood="smile", lh=(-60, -80), rh=(60, -80), hold="", flip=1, old=False):
    """A princess or queen with a long dress, feet at (x, y), about 330 units tall."""
    g = f'<g transform="translate({x} {y}) scale({s*flip} {s})">'
    g += f'<ellipse cx="0" cy="6" rx="92" ry="13" fill="#000" opacity=".1"/>'
    g += f'<path d="M-46 -150 Q0 -176 46 -150 L96 -2 Q0 20 -96 -2 Z" fill="{robe}"/>'
    g += f'<path d="M-92 -12 Q0 14 92 -12 L96 -2 Q0 20 -96 -2 Z" fill="{trim}"/><path d="M-30 -136 Q0 -128 30 -136 L34 -112 Q0 -102 -34 -112 Z" fill="{trim}" opacity=".9"/>'
    g += f'<path d="M-40 -110 H40" stroke="{trim}" stroke-width="10" opacity=".9"/>'
    g += hands(lh, rh, robe)
    g += hold
    g += f'<rect x="-10" y="-176" width="20" height="30" fill="{SKIN}"/>'
    g += f'<path d="M-52 -214 Q-70 -150 -46 -90 Q-30 -100 -30 -140 L30 -140 Q30 -100 46 -90 Q70 -150 52 -214 Z" fill="{hair}"/>'
    g += f'<circle cx="0" cy="-208" r="46" fill="{SKIN}"/>'
    g += f'<path d="M-48 -214 Q-46 -262 0 -262 Q46 -262 48 -214 Q30 -240 0 -238 Q-30 -240 -48 -214 Z" fill="{hair}"/>'
    if old: g += f'<path d="M-52 -214 Q-50 -270 0 -272 Q50 -270 52 -214 L52 -190 Q0 -150 -52 -190 Z" fill="#2a2a38"/><circle cx="0" cy="-206" r="42" fill="{SKIN}"/>'
    g += crown(0, -222, 46, hat)
    g += face(0, -204, 46, mood)
    return g + '</g>'


def man(x, y, s=1.0, coat="#4a7ab8", hat="cap", beard="#7a4a2a", mood="smile", lh=(-70, -70), rh=(70, -70), hold="", flip=1, hatcol="#c0392b", pants="#3a3a5a", moustache=True, young=False):
    """A man or knight in a belted tunic, feet at (x, y), about 350 units tall."""
    g = f'<g transform="translate({x} {y}) scale({s*flip} {s})">'
    g += f'<ellipse cx="0" cy="6" rx="80" ry="12" fill="#000" opacity=".1"/>'
    g += f'<rect x="-34" y="-100" width="28" height="98" rx="12" fill="{pants}"/><rect x="6" y="-100" width="28" height="98" rx="12" fill="{pants}"/><rect x="-40" y="-16" width="38" height="20" rx="9" fill="#5a3a2a"/><rect x="2" y="-16" width="38" height="20" rx="9" fill="#5a3a2a"/>'
    g += f'<path d="M-52 -160 Q0 -186 52 -160 L62 -78 Q0 -60 -62 -78 Z" fill="{coat}"/><path d="M-60 -84 Q0 -64 60 -84 L62 -70 Q0 -50 -62 -70 Z" fill="{GOLD}"/>'
    g += f'<path d="M0 -170 V-70" stroke="#fff" stroke-width="5" opacity=".5"/>'
    g += hands(lh, rh, coat, 24) + hold
    g += f'<rect x="-11" y="-190" width="22" height="30" fill="{SKIN}"/><circle cx="0" cy="-226" r="46" fill="{SKIN}"/>'
    if beard:
        g += f'<path d="M-46 -230 Q-60 -150 0 -146 Q60 -150 46 -230 Q30 -190 0 -190 Q-30 -190 -46 -230 Z" fill="{beard}"/>'
        if moustache: g += f'<path d="M-30 -208 Q-14 -222 0 -210 Q14 -222 30 -208 Q14 -196 0 -204 Q-14 -196 -30 -208 Z" fill="{beard}"/>'
    if hat == "cap":
        g += f'<path d="M-52 -238 Q-46 -296 0 -296 Q46 -296 52 -238 Q0 -254 -52 -238 Z" fill="{hatcol}"/><rect x="-56" y="-248" width="112" height="18" rx="9" fill="#fff" opacity=".9"/><path d="M20 -288 Q60 -330 50 -270" stroke="#fff" stroke-width="8" fill="none" stroke-linecap="round"/>'
    elif hat == "prince":
        g += f'<path d="M-50 -240 Q-46 -300 0 -300 Q46 -300 50 -240 Q0 -256 -50 -240 Z" fill="{hatcol}"/><rect x="-54" y="-250" width="108" height="20" rx="10" fill="{GOLD}"/><path d="M10 -290 Q70 -340 54 -262" stroke="#fff" stroke-width="9" fill="none" stroke-linecap="round"/>'
    elif hat == "hood":
        g += f'<path d="M-58 -226 Q-60 -310 0 -310 Q60 -310 58 -226 Q50 -190 40 -170 L-40 -170 Q-50 -190 -58 -226 Z" fill="{hatcol}"/><circle cx="0" cy="-222" r="38" fill="{SKIN}"/>'
    else:
        g += f'<path d="M-48 -232 Q-44 -276 0 -274 Q44 -276 48 -232 Q30 -252 0 -250 Q-30 -252 -48 -232 Z" fill="{beard or "#7a4a2a"}"/>'
    g += face(0, -222, 46, mood)
    return g + '</g>'


def dog(x, y, s=1.0, flip=1, mood="smile", lying=False):
    """Sokolko, a loyal white-and-grey hound."""
    g = f'<g transform="translate({x} {y}) scale({s*flip} {s})">'
    g += f'<ellipse cx="0" cy="6" rx="110" ry="12" fill="#000" opacity=".1"/>'
    if lying:
        g += f'<ellipse cx="0" cy="-40" rx="100" ry="40" fill="#f2efe8"/><circle cx="84" cy="-52" r="38" fill="#f2efe8"/><path d="M62 -78 Q40 -40 66 -40 Z" fill="#a9a29a"/><ellipse cx="104" cy="-44" rx="14" ry="10" fill="{INK}"/><path d="M68 -62 Q78 -56 88 -62" stroke="{INK}" stroke-width="5" fill="none" stroke-linecap="round"/><path d="M-96 -44 Q-140 -50 -130 -20" stroke="#f2efe8" stroke-width="20" fill="none" stroke-linecap="round"/>'
        return g + '</g>'
    g += f'<path d="M-90 -90 Q-140 -140 -128 -170" stroke="#f2efe8" stroke-width="22" fill="none" stroke-linecap="round"/>'
    g += f'<ellipse cx="-10" cy="-86" rx="96" ry="46" fill="#f2efe8"/><ellipse cx="-30" cy="-102" rx="50" ry="24" fill="#a9a29a" opacity=".6"/>'
    g += "".join(f'<rect x="{lx}" y="-70" width="24" height="72" rx="11" fill="#f2efe8"/>' for lx in (-82, -50, 36, 66))
    g += f'<path d="M64 -110 Q84 -170 106 -156 L110 -96 Z" fill="#f2efe8"/><circle cx="112" cy="-146" r="42" fill="#f2efe8"/>'
    g += f'<path d="M92 -178 Q70 -140 84 -112 Q108 -126 112 -170 Z" fill="#a9a29a"/><ellipse cx="148" cy="-134" rx="16" ry="12" fill="{INK}"/>'
    if mood == "worry":
        g += f'<circle cx="122" cy="-154" r="5" fill="{INK}"/><path d="M110 -166 Q122 -176 134 -166" stroke="{INK}" stroke-width="4" fill="none"/><path d="M128 -112 Q148 -100 138 -88" stroke="#ff9c8c" stroke-width="9" fill="none" stroke-linecap="round"/>'
    elif mood == "bark":
        g += f'<circle cx="122" cy="-154" r="5" fill="{INK}"/><path d="M136 -118 Q156 -108 140 -98 Q128 -108 136 -118 Z" fill="#b04a3a"/>'
    else:
        g += f'<circle cx="122" cy="-154" r="5" fill="{INK}"/><path d="M130 -118 Q144 -104 150 -118" stroke="{INK}" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M134 -114 Q144 -96 140 -108" stroke="#ff9c8c" stroke-width="8" fill="none" stroke-linecap="round"/>'
    g += f'<path d="M80 -112 H130" stroke="{RED}" stroke-width="10" stroke-linecap="round"/>'
    return g + '</g>'


def horse(x, y, s=1.0, flip=1, col="#fafafa", mane="#c8c0b0", saddle=RED, rider=None, gallop=False):
    g = f'<g transform="translate({x} {y}) scale({s*flip} {s})">'
    g += f'<ellipse cx="0" cy="6" rx="170" ry="14" fill="#000" opacity=".1"/>'
    g += f'<path d="M-150 -150 Q-210 -110 -190 -30 Q-160 -90 -130 -110 Z" fill="{mane}"/>'
    if gallop:
        legs = [(-110, -70, -150, -4), (-70, -70, -30, -4), (60, -70, 20, -4), (100, -70, 140, -4)]
        g += "".join(f'<path d="M{a} {b} L{c} {d}" stroke="{col}" stroke-width="34" stroke-linecap="round"/>' for a, b, c, d in legs)
    else:
        g += "".join(f'<rect x="{lx}" y="-80" width="32" height="84" rx="14" fill="{col}"/>' for lx in (-120, -76, 52, 96))
    g += f'<ellipse cx="0" cy="-130" rx="160" ry="70" fill="{col}"/>'
    g += f'<path d="M100 -170 Q150 -250 190 -250 Q220 -240 232 -210 L240 -176 Q200 -150 150 -130 Z" fill="{col}"/>'
    g += f'<path d="M110 -200 Q130 -270 150 -240 Q150 -200 130 -170 Z" fill="{mane}"/>'
    g += f'<ellipse cx="236" cy="-196" rx="28" ry="22" fill="{col}"/><circle cx="214" cy="-224" r="7" fill="{INK}"/><circle cx="244" cy="-196" r="5" fill="#d8b0a0"/><path d="M226 -176 Q236 -168 246 -176" stroke="{INK}" stroke-width="4" fill="none" stroke-linecap="round"/>'
    g += f'<path d="M180 -246 L196 -284 L210 -244 Z" fill="{col}"/>'
    g += f'<path d="M-40 -194 Q0 -214 40 -194 L40 -150 Q0 -138 -40 -150 Z" fill="{saddle}"/><path d="M-40 -182 H40" stroke="{GOLD}" stroke-width="8"/>'
    if rider: g += rider
    return g + '</g>'


def mirror_obj(x, y, s=1.0, face_on=True, crack=False):
    """A tall standing oval mirror in a golden frame, with a friendly glow face inside."""
    g = f'<g transform="translate({x} {y}) scale({s})">'
    g += f'<rect x="-14" y="-90" width="28" height="94" rx="10" fill="#b0763c"/><rect x="-70" y="-6" width="140" height="18" rx="9" fill="#b0763c"/>'
    g += f'<ellipse cx="0" cy="-300" rx="150" ry="212" fill="{GOLD}" stroke="#d9a020" stroke-width="10"/><ellipse cx="0" cy="-300" rx="124" ry="186" fill="#d8f0ff"/><ellipse cx="0" cy="-300" rx="124" ry="186" fill="url(#sky)" opacity=".25"/>'
    g += f'<path d="M-70 -380 Q-40 -440 0 -450" stroke="#fff" stroke-width="14" fill="none" stroke-linecap="round" opacity=".8"/>'
    g += "".join(f'<circle cx="{cx}" cy="{cy}" r="9" fill="{c}"/>' for cx, cy, c in ((0, -520, RED), (-100, -440, "#6cbf72"), (100, -440, "#6cbf72"), (-140, -300, RED), (140, -300, RED)))
    if face_on:
        g += f'<g opacity=".92"><circle cx="0" cy="-300" r="74" fill="#fff6dc"/><circle cx="-26" cy="-312" r="8" fill="{INK}"/><circle cx="26" cy="-312" r="8" fill="{INK}"/><path d="M-28 -276 Q0 -250 28 -276" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round"/><circle cx="-46" cy="-288" r="12" fill="{ROSE}" opacity=".5"/><circle cx="46" cy="-288" r="12" fill="{ROSE}" opacity=".5"/></g>'
    if crack: g += f'<path d="M-30 -440 L10 -360 L-20 -300 L30 -230 M10 -360 L70 -340" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round"/><path d="M-30 -440 L10 -360 L-20 -300 L30 -230 M10 -360 L70 -340" stroke="#6a8aa8" stroke-width="2.5" fill="none"/>'
    return g + '</g>'


def oak(x, y, h, c1="#5fae6a", c2="#7cc77a"):
    w = h * .5
    return (f'<rect x="{x-h*.06}" y="{y-h*.5}" width="{h*.12}" height="{h*.52}" rx="{h*.05}" fill="{BROWN}"/>'
            f'<circle cx="{x}" cy="{y-h*.62}" r="{w*.62}" fill="{c1}"/><circle cx="{x-w*.5}" cy="{y-h*.5}" r="{w*.42}" fill="{c2}"/><circle cx="{x+w*.5}" cy="{y-h*.5}" r="{w*.44}" fill="{c2}"/><circle cx="{x}" cy="{y-h*.9}" r="{w*.4}" fill="{c2}"/>')


def fpine(x, y, h, col="#3f9a6a"):
    s = f'<rect x="{x-9}" y="{y-34}" width="18" height="38" rx="6" fill="{BROWN}"/>'
    for k in range(3):
        yy = y - 30 - h * .24 * k; w = h * .26 * (1 - k * .22)
        s += f'<path d="M{x-w:.0f} {yy:.0f} Q{x} {yy-h*.42:.0f} {x+w:.0f} {yy:.0f} Q{x} {yy+14:.0f} {x-w:.0f} {yy:.0f} Z" fill="{col}"/>'
    return s


def meadow(y=640, c1="#9edb8a", c2="#7fc774", h=900):
    return (f'<path d="M0 {y} Q300 {y-60} 650 {y-10} T1300 {y-24} T1600 {y-34} V{h} H0 Z" fill="{c1}"/>'
            f'<path d="M0 {y+90} Q500 {y+30} 900 {y+96} T1600 {y+54} V{h} H0 Z" fill="{c2}" opacity=".8"/>')


def hills(c1="#b8e6a4", c2="#a2d890"):
    return f'<path d="M0 560 Q250 440 520 540 T1100 520 T1600 500 V900 H0 Z" fill="{c1}"/><path d="M0 620 Q400 520 800 600 T1600 580 V900 H0 Z" fill="{c2}"/>'


def flowers(r, n, y0=640, y1=880, cols=("#ff9ec0", "#ffd36b", "#fff", "#c8a0f0")):
    return "".join(f'<circle cx="{r.randint(0,1600)}" cy="{r.randint(y0,y1)}" r="{r.randint(5,9)}" fill="{r.choice(cols)}"/>' for _ in range(n))


def room(wall="#ffe8c8", floor="#d9a56a", beams=True):
    b = f'<rect width="1600" height="900" fill="{wall}"/><rect y="690" width="1600" height="210" fill="{floor}"/><path d="M0 690 H1600" stroke="#b07a42" stroke-width="10"/>'
    if beams: b += "".join(f'<rect x="{x}" y="0" width="14" height="690" fill="#e8c898" opacity=".5"/>' for x in range(60, 1600, 160))
    return b


def window(x, y, w, h, out="#bfe6ff", snow=False, r=None):
    b = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="{out}" stroke="#9a6a46" stroke-width="16"/><path d="M{x+w/2} {y} V{y+h} M{x} {y+h/2} H{x+w}" stroke="#9a6a46" stroke-width="10"/>'
    if snow and r: b += "".join(f'<circle cx="{r.randint(x+14,x+w-14)}" cy="{r.randint(y+14,y+h-14)}" r="{r.uniform(3,8):.1f}" fill="#fff"/>' for _ in range(34))
    return b


def tilestove(x, y, s=1.0, lit=True):
    g = f'<g transform="translate({x} {y}) scale({s})"><rect x="-190" y="-340" width="380" height="340" rx="30" fill="#f4ecdc"/><path d="M-190 -340 Q0 -420 190 -340 Z" fill="#e8dcc4"/><rect x="-100" y="-210" width="200" height="130" rx="60" fill="#3a2418"/>'
    if lit: g += f'<ellipse cx="0" cy="-130" rx="80" ry="40" fill="{GOLD}" opacity=".85"/>'
    g += "".join(f'<rect x="{-170+i*68}" y="{-320+j*34}" width="58" height="24" rx="6" fill="#bfe0f4" opacity=".8"/>' for i in range(6) for j in (0, 1) if not (-100 < -170 + i * 68 + 29 < 100 and j == 1))
    return g + '</g>'


def terem(x, y, w, h, wall="#d98a5a", roof="#c0392b"):
    """A friendly carved wooden house: logs, a red roof, a round window, a porch."""
    g = f'<rect x="{x}" y="{y-h}" width="{w}" height="{h}" rx="18" fill="{wall}"/>'
    g += "".join(f'<path d="M{x} {y-h+i*h/6} H{x+w}" stroke="#b86a3a" stroke-width="5" opacity=".6"/>' for i in range(1, 6))
    g += f'<path d="M{x-40} {y-h+16} L{x+w/2} {y-h-w*.36} L{x+w+40} {y-h+16} Z" fill="{roof}"/><path d="M{x-40} {y-h+16} L{x+w/2} {y-h-w*.36} L{x+w+40} {y-h+16}" stroke="{GOLD}" stroke-width="10" fill="none" stroke-linejoin="round"/>'
    g += f'<circle cx="{x+w/2}" cy="{y-h-w*.1}" r="{w*.06}" fill="{GOLD}" stroke="#7a4a2a" stroke-width="6"/>'
    g += f'<rect x="{x+w*.12}" y="{y-h*.76}" width="{w*.24}" height="{h*.36}" rx="12" fill="{GOLD}" stroke="#7a4a2a" stroke-width="8"/><rect x="{x+w*.64}" y="{y-h*.76}" width="{w*.24}" height="{h*.36}" rx="12" fill="{GOLD}" stroke="#7a4a2a" stroke-width="8"/>'
    g += f'<rect x="{x+w*.41}" y="{y-h*.52}" width="{w*.18}" height="{h*.52}" rx="14" fill="#7a4a2a"/><circle cx="{x+w*.55}" cy="{y-h*.26}" r="8" fill="{GOLD}"/>'
    g += f'<rect x="{x+w*.34}" y="{y-8}" width="{w*.32}" height="14" rx="6" fill="#b57a4a"/>'
    return g


def apple(x, y, s=1.0, glow=True):
    g = f'<g transform="translate({x} {y}) scale({s})">'
    if glow: g += f'<circle cx="0" cy="0" r="60" fill="{GOLD}" opacity=".25"/>'
    return g + f'<circle cx="0" cy="0" r="32" fill="#ffc83a"/><circle cx="-10" cy="-10" r="9" fill="#fff" opacity=".75"/><path d="M0 -30 Q4 -50 16 -52" stroke="{BROWN}" stroke-width="6" fill="none" stroke-linecap="round"/><path d="M6 -42 Q26 -58 36 -40 Q18 -34 6 -42 Z" fill="#6cbf72"/></g>'


def sun_face(x, y, r, mood="smile"):
    g = "".join(f'<path d="M{x+math.cos(a)*r*1.15:.0f} {y+math.sin(a)*r*1.15:.0f} L{x+math.cos(a)*r*1.6:.0f} {y+math.sin(a)*r*1.6:.0f}" stroke="#ffb82e" stroke-width="{r*.12}" stroke-linecap="round"/>' for a in [i * math.pi / 8 for i in range(16)])
    return g + f'<circle cx="{x}" cy="{y}" r="{r*1.12}" fill="#fff3b0" opacity=".5"/><circle cx="{x}" cy="{y}" r="{r}" fill="#ffd54a"/>' + face(x, y + r * .08, r * .8, mood)


def moon_face(x, y, r):
    return (f'<circle cx="{x}" cy="{y}" r="{r*1.3}" fill="#fff6c8" opacity=".25"/><circle cx="{x}" cy="{y}" r="{r}" fill="#fff0a8"/><circle cx="{x+r*.42}" cy="{y-r*.1}" r="{r*.86}" fill="#2c3a78"/>'
            f'<circle cx="{x-r*.34}" cy="{y-r*.05}" r="{r*.07}" fill="{INK}"/><path d="M{x-r*.62} {y+r*.28} Q{x-r*.5} {y+r*.46} {x-r*.3} {y+r*.4}" stroke="{INK}" stroke-width="{r*.06}" fill="none" stroke-linecap="round"/><circle cx="{x-r*.55}" cy="{y+r*.12}" r="{r*.1}" fill="{ROSE}" opacity=".6"/>')


def cloud(x, y, s=1.0, col="#fff", op=.95):
    return f'<g transform="translate({x} {y}) scale({s})" opacity="{op}"><ellipse cx="0" cy="0" rx="130" ry="50" fill="{col}"/><circle cx="-60" cy="-30" r="50" fill="{col}"/><circle cx="20" cy="-50" r="64" fill="{col}"/><circle cx="84" cy="-20" r="46" fill="{col}"/></g>'


def knights_row(x0, y, gap, s, n=7, flip=1, moods=None):
    cols = ["#4a7ab8", "#c0392b", "#3a9a6a", "#8e5ac8", "#e08a2a", "#2a8aa0", "#b0507a"]
    hats = ["#c0392b", "#2a6ab8", "#e0a020", "#3a9a6a", "#8e5ac8", "#c0392b", "#2a8aa0"]
    beards = ["#7a4a2a", "#4a3326", "#c8a060", "#8a8a8a", "#a05a2a", "#3a2a2a", "#d8b878"]
    out = ""
    for i in range(n):
        out += man(x0 + i * gap, y + (i % 2) * 18, s, cols[i], "cap", beards[i], "smile", hatcol=hats[i], flip=flip, lh=(-66, -50), rh=(66, -50))
    return out
