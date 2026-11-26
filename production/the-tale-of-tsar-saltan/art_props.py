"""Extra props for the Tsar Saltan pictures (sea, ships, swan, barrel, squirrel, town, insects, throne room). Soft, rounded, friendly."""
from art_chars import *

NOHAD = lambda s: s.replace('<ellipse cx="0" cy="6"', '<ellipse style="display:none" cx="0" cy="6"', 1)


def sea(y=560, c1="#6fb4e8", c2="#4f93d6", r=None, h=900):
    b = f'<rect y="{y}" width="1600" height="{h-y}" fill="{c1}"/>'
    for i, k in enumerate(range(0, 6)):
        yy = y + 40 + k * 60
        b += f'<path d="M0 {yy} Q100 {yy-26} 200 {yy} T400 {yy} T600 {yy} T800 {yy} T1000 {yy} T1200 {yy} T1400 {yy} T1600 {yy} V{h} H0 Z" fill="{c2 if k % 2 else c1}" opacity=".55"/>'
    if r:
        b += "".join(f'<path d="M{x} {yy} q14 -12 28 0 q14 -12 28 0" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" opacity=".7"/>'
                     for x, yy in ((r.randint(40, 1500), r.randint(y + 30, h - 30)) for _ in range(14)))
    return b


def ship(x, y, s=1.0, flip=1, sail="#fff6dc", hull="#b0763c", flag="#e0564a", cargo=True):
    g = f'<g transform="translate({x} {y}) scale({s*flip} {s})">'
    g += f'<ellipse cx="0" cy="8" rx="230" ry="18" fill="#fff" opacity=".35"/>'
    g += f'<path d="M-210 -80 Q-190 10 -120 20 L130 20 Q200 10 230 -90 Q0 -50 -210 -80 Z" fill="{hull}"/><path d="M-206 -72 Q0 -40 226 -82" stroke="{GOLD}" stroke-width="12" fill="none"/>'
    g += "".join(f'<circle cx="{cx}" cy="-30" r="12" fill="#fff6dc" stroke="#7a4a2a" stroke-width="5"/>' for cx in (-110, -40, 30, 100))
    g += f'<rect x="-8" y="-420" width="16" height="350" rx="6" fill="#7a4a2a"/>'
    g += f'<path d="M12 -400 Q140 -330 150 -150 Q60 -120 12 -130 Z" fill="{sail}" stroke="#e8d8b0" stroke-width="5"/>'
    g += f'<path d="M-12 -360 Q-110 -300 -118 -170 Q-60 -150 -12 -160 Z" fill="{sail}" stroke="#e8d8b0" stroke-width="5"/>'
    g += f'<path d="M0 -420 L-6 -470 L90 -450 L10 -430 Z" fill="{flag}"/><circle cx="0" cy="-424" r="9" fill="{GOLD}"/>'
    if cargo: g += f'<rect x="-170" y="-120" width="64" height="48" rx="8" fill="#c98a52"/><rect x="-100" y="-104" width="52" height="34" rx="8" fill="#d9a066"/>'
    return g + '</g>'


def swan(x, y, s=1.0, flip=1, mood="smile", star=False, wings=False):
    g = f'<g transform="translate({x} {y}) scale({s*flip} {s})">'
    g += f'<ellipse cx="0" cy="6" rx="150" ry="16" fill="#fff" opacity=".45"/>'
    g += f'<path d="M-140 -40 Q-170 -110 -90 -120 Q0 -140 90 -100 Q150 -70 130 -20 Q60 20 -60 14 Q-120 10 -140 -40 Z" fill="#fff" stroke="#dbe8f4" stroke-width="5"/>'
    g += f'<path d="M-110 -100 Q-30 -150 40 -100 Q-30 -60 -110 -100 Z" fill="#eef5fb" stroke="#cfe0ee" stroke-width="4"/>'
    if wings: g += f'<path d="M-40 -110 Q-120 -260 -220 -230 Q-170 -160 -100 -110 Z M-10 -110 Q60 -280 160 -250 Q120 -170 40 -110 Z" fill="#fff" stroke="#dbe8f4" stroke-width="5"/>'
    g += f'<path d="M96 -90 Q150 -150 120 -230 Q112 -270 150 -280" stroke="#fff" stroke-width="40" fill="none" stroke-linecap="round"/>'
    g += f'<circle cx="160" cy="-290" r="34" fill="#fff" stroke="#dbe8f4" stroke-width="4"/><path d="M186 -290 L236 -278 L188 -266 Z" fill="#ffa33a"/><circle cx="168" cy="-298" r="6" fill="{INK}"/>'
    g += f'<circle cx="150" cy="-276" r="9" fill="{ROSE}" opacity=".6"/>'
    if mood == "smile": g += f'<path d="M184 -277 Q200 -270 212 -276" stroke="{INK}" stroke-width="3" fill="none"/>'
    if star: g += f'<path d="M168 -334 l6 -18 l6 18 l18 6 l-18 6 l-6 18 l-6 -18 l-18 -6 Z" fill="{GOLD}"/>'
    return g + '</g>'


def kite(x, y, s=1.0, flip=1):
    """A cross dark bird of prey (a kite); round and rather grumpy than scary."""
    g = f'<g transform="translate({x} {y}) scale({s*flip} {s})">'
    g += f'<path d="M-30 0 Q-200 -90 -250 20 Q-150 30 -40 40 Z M30 0 Q200 -90 260 20 Q150 30 40 40 Z" fill="#6a4a3a"/>'
    g += f'<ellipse cx="0" cy="20" rx="70" ry="50" fill="#8a5a3a"/><ellipse cx="0" cy="34" rx="44" ry="28" fill="#d8b890"/>'
    g += f'<circle cx="0" cy="-34" r="42" fill="#8a5a3a"/><path d="M-6 -30 L14 -6 L-24 -14 Z" fill="#ffc23a"/>'
    g += f'<circle cx="-18" cy="-44" r="7" fill="{INK}"/><circle cx="16" cy="-44" r="7" fill="{INK}"/><path d="M-30 -62 L-4 -54 M30 -62 L6 -54" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>'
    return g + '</g>'


def barrel(x, y, s=1.0, tilt=0, faces=True, flip=1):
    g = f'<g transform="translate({x} {y}) rotate({tilt}) scale({s*flip} {s})">'
    g += f'<ellipse cx="0" cy="-120" rx="160" ry="150" fill="#b0763c"/><path d="M-160 -120 Q0 -300 160 -120 Q0 -160 -160 -120 Z" fill="#c98a52"/>'
    g += "".join(f'<path d="M{-150+k*0} {yy} Q0 {yy+30} 150 {yy}" stroke="#5a3a1c" stroke-width="12" fill="none"/>' for k, yy in enumerate((-190, -120, -52)))
    g += "".join(f'<path d="M{xx} -250 Q{xx*1.1} -120 {xx} -10" stroke="#8a5a2c" stroke-width="5" fill="none" opacity=".7"/>' for xx in (-90, -30, 30, 90))
    if faces:
        g += f'<circle cx="0" cy="-130" r="48" fill="#bfe6ff" stroke="#5a3a1c" stroke-width="10"/>'
        g += f'<circle cx="-16" cy="-130" r="17" fill="{SKIN}"/><circle cx="16" cy="-122" r="12" fill="{SKIN}"/><path d="M-30 -146 Q-16 -170 0 -146" fill="#7a4a2a"/>'
    return g + '</g>'


def squirrel(x, y, s=1.0, flip=1, nut=True):
    g = f'<g transform="translate({x} {y}) scale({s*flip} {s})">'
    g += f'<path d="M-30 -20 Q-150 -40 -130 -190 Q-100 -270 -20 -230 Q-80 -150 -20 -80 Z" fill="#e8913a" stroke="#c97020" stroke-width="5"/>'
    g += f'<ellipse cx="0" cy="-60" rx="56" ry="70" fill="#e8913a"/><ellipse cx="14" cy="-48" rx="32" ry="46" fill="#ffe0b8"/>'
    g += f'<circle cx="26" cy="-140" r="40" fill="#e8913a"/><path d="M6 -166 L0 -210 L30 -176 Z M42 -170 L58 -206 L62 -160 Z" fill="#e8913a"/>'
    g += f'<circle cx="38" cy="-146" r="6" fill="{INK}"/><ellipse cx="62" cy="-134" rx="8" ry="6" fill="{INK}"/><circle cx="24" cy="-128" r="10" fill="{ROSE}" opacity=".6"/>'
    if nut: g += f'<g transform="translate(70 -80)"><ellipse rx="26" ry="22" fill="#ffd54a" stroke="#d9a020" stroke-width="5"/><circle cx="-6" cy="-6" r="6" fill="#fff" opacity=".8"/></g><circle cx="86" cy="-70" r="8" fill="#5fd08a"/>'
    return g + '</g>'


def crystal_house(x, y, s=1.0):
    g = f'<g transform="translate({x} {y}) scale({s})">'
    g += f'<path d="M-120 0 V-170 L0 -250 L120 -170 V0 Z" fill="#d8f4ff" opacity=".85" stroke="#fff" stroke-width="8"/><path d="M-120 -170 H120 M0 -250 V0 M-60 -210 V0 M60 -210 V0" stroke="#fff" stroke-width="4" opacity=".7"/>'
    g += f'<circle cx="0" cy="-262" r="12" fill="{GOLD}"/><path d="M-90 -150 L-40 -90" stroke="#fff" stroke-width="8" stroke-linecap="round" opacity=".8"/>'
    return g + '</g>'


def town(x, y, s=1.0, tint="#fff0d8"):
    """A white walled town with golden domes, as it appears by magic."""
    g = f'<g transform="translate({x} {y}) scale({s})">'
    g += f'<rect x="-420" y="-220" width="840" height="220" fill="{tint}" stroke="#e0c8a0" stroke-width="6"/>'
    g += "".join(f'<rect x="{xx}" y="-250" width="38" height="40" fill="{tint}" stroke="#e0c8a0" stroke-width="5"/>' for xx in range(-420, 400, 76))
    for cx, hh, col in ((-250, 200, "#ffd54a"), (-60, 270, "#ffb82e"), (120, 220, "#ffd54a"), (300, 180, "#ffb82e")):
        g += f'<rect x="{cx-34}" y="{-220-hh}" width="68" height="{hh}" rx="10" fill="#fff" stroke="#e0c8a0" stroke-width="5"/><path d="M{cx-44} {-220-hh} Q{cx-50} {-220-hh-78} {cx} {-220-hh-110} Q{cx+50} {-220-hh-78} {cx+44} {-220-hh} Z" fill="{col}" stroke="#d9a020" stroke-width="5"/>'
        g += f'<path d="M{cx} {-220-hh-110} V{-220-hh-140} M{cx-12} {-220-hh-128} H{cx+12}" stroke="#d9a020" stroke-width="6"/><path d="M{cx-12} {-220-hh+40} q12 -22 24 0 v50 h-24 Z" fill="#8cc4ee"/>'
    g += f'<path d="M-70 0 V-110 Q0 -170 70 -110 V0 Z" fill="#c98a52" stroke="#7a4a2a" stroke-width="7"/><circle cx="26" cy="-60" r="7" fill="{GOLD}"/>'
    return g + '</g>'


def insect(x, y, s=1.0, kind="mosquito", flip=1):
    """The enchanted prince as a tiny winged friend (a red cap shows who he is)."""
    g = f'<g transform="translate({x} {y}) scale({s*flip} {s})">'
    wing = '<ellipse cx="-20" cy="-36" rx="22" ry="40" fill="#fff" opacity=".7" stroke="#bfe6ff" stroke-width="4" transform="rotate(-25 -20 -36)"/><ellipse cx="14" cy="-38" rx="22" ry="40" fill="#fff" opacity=".7" stroke="#bfe6ff" stroke-width="4" transform="rotate(25 14 -38)"/>'
    if kind == "mosquito":
        g += wing + '<ellipse cx="0" cy="0" rx="12" ry="40" fill="#6a6a7a" transform="rotate(80)"/><circle cx="-46" cy="0" r="14" fill="#6a6a7a"/><path d="M-58 4 L-96 20" stroke="#4a4a5a" stroke-width="4"/>'
        g += '<path d="M-10 18 L-20 56 M4 18 L0 58 M16 14 L26 54" stroke="#4a4a5a" stroke-width="4"/>'
    elif kind == "fly":
        g += wing + '<ellipse cx="0" cy="0" rx="30" ry="22" fill="#5a5a6a"/><circle cx="-34" cy="-4" r="18" fill="#6a6a7a"/><circle cx="-40" cy="-10" r="8" fill="#e0564a"/><path d="M-6 18 L-14 50 M10 18 L12 52" stroke="#4a4a5a" stroke-width="4"/>'
    else:   # bumblebee
        g += wing + '<ellipse cx="0" cy="0" rx="44" ry="32" fill="#ffd54a"/><path d="M-12 -30 V30 M10 -32 V32 M30 -24 V24" stroke="#3a2a2a" stroke-width="12"/><circle cx="-48" cy="2" r="22" fill="#4a3a3a"/><path d="M-56 -20 L-70 -44 M-44 -22 L-44 -48" stroke="#3a2a2a" stroke-width="4"/>'
    g += f'<path d="M-52 -18 Q-40 -44 -22 -18 Z" fill="#e0564a"/><circle cx="-42" cy="-3" r="3" fill="#fff"/>'
    return g + '</g>'


def tsar(x, y, s=1.0, mood="smile", coat="#c0392b", beard="#cfcfd8", lh=(-70, -60), rh=(70, -60), flip=1, hold=""):
    g = man(x, y, s, coat, "x", beard, mood, lh=lh, rh=rh, hold=hold, flip=flip, pants="#5a2a3a")
    return g + f'<g transform="translate({x} {y}) scale({s*flip} {s})">{crown(0, -226, 46, "crown")}</g>'


def throne_room(r, wall="#f6e0b8", carpet="#c0392b"):
    b = f'<rect width="1600" height="900" fill="{wall}"/><rect y="700" width="1600" height="200" fill="#d9a56a"/><path d="M0 700 H1600" stroke="#b07a42" stroke-width="10"/>'
    b += "".join(f'<rect x="{x}" y="0" width="70" height="700" rx="18" fill="#fff0d0" stroke="#e0c090" stroke-width="6"/><rect x="{x-14}" y="660" width="98" height="44" rx="12" fill="#e8d0a0"/>' for x in (110, 1420))
    b += f'<path d="M520 700 L1080 700 L1180 900 L420 900 Z" fill="{carpet}"/><path d="M520 700 L1080 700" stroke="{GOLD}" stroke-width="10"/>'
    b += f'<path d="M0 0 H1600 V120 Q800 190 0 120 Z" fill="#d6b070" opacity=".55"/>' + "".join(f'<circle cx="{x}" cy="150" r="12" fill="{GOLD}"/>' for x in (300, 600, 800, 1000, 1300))
    return b


def throne(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-120" y="-330" width="240" height="330" rx="40" fill="{GOLD}" stroke="#d9a020" stroke-width="8"/>'
            f'<rect x="-84" y="-290" width="168" height="150" rx="30" fill="#c0392b"/><rect x="-130" y="-150" width="260" height="60" rx="20" fill="#e0564a" stroke="#d9a020" stroke-width="6"/><circle cx="0" cy="-350" r="26" fill="{GOLD}"/></g>')


def trio(x, y, s=1.0, mood="sulk", eyepatch=None):
    """The weaver (blue), the cook (green, apron) and old Babarikha (purple, headscarf)."""
    g = lady(x - 190 * s, y, s, robe="#4a7ab8", trim="#9fc0e8", hair="#5a3a2a", hat="", mood=mood, lh=(-60, -60), rh=(60, -60))
    g += lady(x, y + 14 * s, s * .95, robe="#4a9a6a", trim="#fff", hair="#3a2a2a", hat="", mood=mood, lh=(-60, -60), rh=(60, -60))
    g += lady(x + 190 * s, y, s, robe="#8e5ac8", trim="#d8c0f0", hair="#cfcfd8", hat="", mood=mood, old=True, lh=(-60, -60), rh=(60, -60))
    return g


def hero33(x0, y, gap, s, n=6, flip=1):
    """Sea knights in shining scale armour, with old Chernomor in front (silver beard)."""
    out = ""
    cols = ["#7fc8e8", "#9ad8c8", "#8ab8f0", "#a8d8b0", "#8ad0e0", "#b0c8f0"]
    for i in range(n):
        out += man(x0 + i * gap, y + (i % 2) * 22, s, cols[i % 6], "prince", "#8a6a4a", "smile", hatcol="#ffd54a", pants="#4a7ab8", flip=flip, lh=(-66, -50), rh=(66, -50))
    return out


def stars(r, n=40, y1=400):
    return sparkles(r, n, 0, 1600, 20, y1, "#fff6c8")


def oak_big(x, y, s=1.0):
    return (f'<g transform="translate({x} {y}) scale({s})"><rect x="-34" y="-260" width="68" height="262" rx="24" fill="{BROWN}"/>'
            f'<circle cx="0" cy="-330" r="150" fill="#5fae6a"/><circle cx="-120" cy="-270" r="100" fill="#7cc77a"/><circle cx="120" cy="-270" r="106" fill="#7cc77a"/><circle cx="0" cy="-420" r="96" fill="#7cc77a"/>'
            f'<path d="M-30 -190 Q-90 -230 -130 -200" stroke="{BROWN}" stroke-width="16" fill="none" stroke-linecap="round"/></g>')
