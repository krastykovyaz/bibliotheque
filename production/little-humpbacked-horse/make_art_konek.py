#!/usr/bin/env python3
"""Illustrations and covers for "The Little Humpbacked Horse" (Yershov) as SVG, soft rounded picture-book style for children. Writes art/<name>.svg."""
from art_konek import *

DAYC, NIGHTC = ("#bfe9ff", "#f2fbe6"), ("#2c3a78", "#8a9ad0")
def moon(x=260, y=140, r=70): return f'<circle cx="{x}" cy="{y}" r="{r*1.5:.0f}" fill="#fff6c8" opacity=".25"/><circle cx="{x}" cy="{y}" r="{r}" fill="#fff0a8"/>'
def dayf(r, y=660): return f'<circle cx="1300" cy="140" r="90" fill="#fff3b0"/>' + hills() + meadow(y) + flowers(r, 30)
def nightf(r): return stars(r, 50, 400) + moon(1300, 150, 70) + hills("#3f8a74", "#2f7a64") + meadow(690, "#4a9a7a", "#3a8a6a")
def M(x, y, s, who, mood="smile", **k): return man(x, y, s, mood=mood, **{**who, **k})
def ground(c="#e6d4a8", y=700): return f'<rect y="{y}" width="1600" height="{900-y}" fill="{c}"/>'

def s01():
    r = R(1); b = dayf(r) + wheat(r, 700, 880) + terem(80, 700, 320, 250, "#d98a5a", "#c0392b") + oak(1480, 740, 300)
    b += M(560, 880, 1.0, FAT, lh=(-60, -60), rh=(70, -80)) + M(820, 880, 1.15, DAN) + M(1040, 880, 1.1, GAV) + M(1260, 880, 1.0, IV)
    return svg(b, *DAYC)
def s02():
    r = R(2); b = f'<rect width="1600" height="900" fill="#9ab4c8"/>' + cloud(300, 130, 1.8, "#7a8ea8") + cloud(1100, 150, 2, "#7a8ea8") + meadow(600, "#7aa88a", "#6a9a7a") + wheat(r, 620, 760)
    b += "".join(f'<path d="M{x} {y} l-14 38" stroke="#4a7ab8" stroke-width="4" stroke-linecap="round"/>' for x, y in ((r.randint(0, 1600), r.randint(200, 880)) for _ in range(90)))
    b += haystack(520, 880, 1.5) + M(520, 790, .55, DAN, "sleep") + f'<path d="M1080 560 q20 -30 40 0 q30 -40 50 0" stroke="#fff" stroke-width="0"/>'
    b += f'<g opacity=".5"><path d="M1000 760 q80 -90 160 0 q-50 30 -160 0 Z" fill="#c8a860"/></g>'
    return svg(b, "#8a9ab0", "#bcd0b8")
def s03():
    r = R(3); b = nightf(r) + f'<rect x="0" y="640" width="1600" height="26" fill="#9a6a3a"/>' + "".join(f'<rect x="{x}" y="590" width="20" height="120" fill="#9a6a3a"/>' for x in range(30, 1600, 190))
    b += M(800, 880, 1.2, GAV, "open", lh=(-70, -110), rh=(70, -110)) + sparkles(r, 24, 0, 1600, 300, 880, "#dff4ff")
    b += terem(1200, 700, 240, 180, "#c8986a", "#6a7ab8")
    return svg(b, *NIGHTC)
def s04():
    r = R(4); b = room("#ffe2c0", "#c98a5a") + window(1100, 120, 300, 300, "#2c3a78") + tilestove(560, 700, 1.15)
    b += M(560, 410, .6, IV, "open", lh=(-80, -110), rh=(80, -90)) + M(1000, 890, 1.2, FAT, lh=(-60, -60), rh=(-30, -140)) + M(220, 890, 1.0, DAN, "sulk") + M(1320, 890, 1.0, GAV, "sulk")
    b += f'<path d="M450 250 q14 -26 28 0 M500 230 q14 -26 28 0" stroke="{GOLD}" stroke-width="7" fill="none" stroke-linecap="round"/>'
    return svg(b, "#ffe2c0", "#ffe2c0")
def s05():
    r = R(5); b = nightf(r) + sparkles(r, 20, 0, 1600, 500, 840, "#fff6c8")
    b += gal(800, 800, 1.2, 1, "#fafafa", rider=man(0, -140, .62, mood="open", flip=-1, lh=(-60, -90), rh=(60, -100), **IV)).replace("#c8c0b0", GOLD)
    b += "".join(f'<path d="M{x} {y} q-60 4 -120 0" stroke="#fff" stroke-width="8" stroke-linecap="round" opacity=".5"/>' for x, y in ((420, 760), (380, 820), (460, 860)))
    return svg(b, *NIGHTC)
def s06():
    r = R(6); b = nightf(r) + horse(1100, 850, 1.1, -1, col="#fafafa", mane=GOLD) + M(430, 880, 1.2, IV, "open")
    b += bubble(300, 250, 130, f'<g transform="translate(300 300) scale(.55)">{konek(0, 0, 1)}</g>') + sparkles(r, 12, 600, 1400, 300, 700, "#ffe27a")
    return svg(b, *NIGHTC)
def s07():
    r = R(7); b = room("#ffe2c0", "#c98a5a") + window(1180, 120, 280, 280, "#2c3a78") + tilestove(520, 700, 1.15)
    b += M(520, 410, .6, IV, "open", lh=(-80, -110), rh=(80, -120)) + M(960, 890, 1.15, DAN, "open", lh=(-70, -50), rh=(-40, -40)) + M(1240, 890, 1.1, GAV, "open") + M(160, 890, 1.0, FAT, "open", lh=(-70, -60), rh=(30, -50))
    b += bubble(520, 160, 80, f'<g transform="translate(520 190) scale(.5)">{man(0, 0, 1, mood="smile", **{**IV, "coat": "#3a2a2a", "hat": "cap", "hatcol": "#3a2a2a"})}</g>')
    return svg(b, "#ffe2c0", "#ffe2c0")
def s08():
    r = R(8); b = dayf(r) + hut(300, 760, 1.4) + gal(900, 860, .9, -1, "#3a3f5a") + gal(1330, 800, .75, -1, "#4a3f5a") + konek(640, 860, .9, 1, "smile")
    b += M(1000, 640, .5, DAN, "open", lh=(-50, -90), rh=(50, -90)).replace("", "") + M(1130, 640, .5, GAV, "open", lh=(-50, -90), rh=(50, -90)) + sparkles(r, 16, 700, 1500, 380, 860, "#ffe27a")
    return svg(b, *DAYC)
def s09():
    r = R(9); b = nightf(r) + hut(560, 760, 1.5) + M(1100, 880, 1.25, IV, "sulk", lh=(-60, -40), rh=(30, -120)) + konek(280, 870, 1.1, 1, "smile", jump=True) + f'<path d="M180 760 q-20 -30 0 -50 M360 740 q20 -30 0 -50" stroke="#fff" stroke-width="6" fill="none" stroke-linecap="round"/>'
    return svg(b, *NIGHTC)
def s10():
    r = R(10); b = nightf(r) + ride(900, 800, 1.7, 1, "open") + "".join(f'<circle cx="{x}" cy="{y}" r="{k}" fill="#f0e8d8" opacity=".7"/>' for x, y, k in ((620, 810, 50), (540, 840, 40), (440, 820, 60), (350, 850, 36)))
    b += gal(1450, 640, .35, 1) + gal(1530, 650, .3, 1, "#4a3f5a")
    return svg(b, *NIGHTC)
def s11():
    r = R(11); b = nightf(r) + f'<path d="M0 760 Q800 700 1600 760 V900 H0 Z" fill="#b9a070"/>' + M(380, 860, 1.15, DAN, "sulk", lh=(-70, -50)) + M(660, 880, 1.1, GAV, "sulk") + gal(150, 800, .55, 1) + M(1150, 880, 1.2, IV, "open", lh=(-60, -110), rh=(70, -80)) + konek(1380, 870, 1.0, -1)
    return svg(b, *NIGHTC)
def s12():
    r = R(12); b = nightf(r) + oak(160, 760, 520) + oak(1480, 760, 480) + gal(300, 850, .6, 1) + gal(520, 860, .55, -1, "#4a3f5a") + M(800, 880, 1.0, DAN, "smile", lh=(-60, -50), rh=(80, -140)) + M(1000, 880, 1.0, GAV)
    b += f'<circle cx="1280" cy="650" r="70" fill="#ffd36b" opacity=".6"/><circle cx="1280" cy="650" r="26" fill="#fff6c8"/><rect x="740" y="860" width="60" height="26" rx="8" fill="#c8a870"/>'
    return svg(b, *NIGHTC)
def s13():
    r = R(13); b = nightf(r) + ride(560, 820, 1.5, 1, "open") + f'<circle cx="1300" cy="660" r="170" fill="#ffd36b" opacity=".35"/><circle cx="1300" cy="660" r="90" fill="#ffd36b" opacity=".5"/><circle cx="1300" cy="660" r="34" fill="#fff6c8"/>' + sparkles(r, 20, 1000, 1600, 460, 860, "#fff6c8")
    b += "".join(f'<path d="M{x} {y} q-70 4 -140 0" stroke="#fff" stroke-width="8" stroke-linecap="round" opacity=".5"/>' for x, y in ((300, 780), (250, 840)))
    return svg(b, *NIGHTC)
def s14():
    r = R(14); b = nightf(r) + f'<path d="M1000 880 Q1060 780 1120 880 Z" fill="#8a6a4a"/><rect x="1000" y="780" width="120" height="110" rx="20" fill="#8a6a4a"/>' + feather(1060, 720, 1.4, -20)
    b += M(640, 880, 1.2, IV, "open", lh=(-60, -60), rh=(50, -110)) + konek(330, 870, 1.0, 1, "open") + sparkles(r, 20, 800, 1400, 460, 860, "#ffe27a")
    return svg(b, *NIGHTC)
def s15():
    r = R(15); b = town_street(r)
    for i, x in enumerate((120, 520, 920, 1340)): b += f'<rect x="{x}" y="640" width="190" height="14" rx="6" fill="#c0392b"/><rect x="{x+10}" y="654" width="12" height="90" fill="#8a5a3a"/><rect x="{x+168}" y="654" width="12" height="90" fill="#8a5a3a"/>' + M(x + 95, 850, .6, [NOB, DAN, GAV, FAT][i])
    b += gal(560, 880, .7, 1) + gal(900, 880, .65, -1, "#4a3f5a") + M(740, 890, 1.0, IV)
    return svg(b, *DAYC)
def s16():
    r = R(16); b = town_street(r) + gal(700, 860, .9, 1) + gal(1000, 860, .9, -1, "#4a3f5a")
    b += "".join(M(x, 890, .8, [DAN, GAV, NOB, FAT][i % 4], "open", lh=(-60, -90), rh=(60, -90)) for i, x in enumerate((130, 330, 1220, 1440)))
    b += gal(260, 640, .5, 1, "#8a6a4a", rider=M(0, -150, .7, NOB, "smile")) + sparkles(r, 12, 600, 1100, 560, 860, "#ffe27a")
    return svg(b, *DAYC)
def s17():
    r = R(17); b = throne_room(r) + throne(800, 640, 1.1) + tsar(800, 640, .9, "open", lh=(-60, -60), rh=(70, -90)) + M(420, 890, 1.05, NOB, "open", lh=(-60, -120), rh=(60, -120)) + M(1180, 890, 1.0, NOB, "smile", coat="#7a4a8a")
    b += bubble(300, 200, 110, f'<g transform="translate(300 270) scale(.38)">{gal(0, 0, 1)}</g>')
    return svg(b, "#f6e0b8", "#f6e0b8")
def s18():
    r = R(18); b = town_street(r) + gal(300, 870, .8, 1) + gal(560, 870, .8, 1, "#4a3f5a") + tsar(900, 880, 1.15, "smile", lh=(-80, -60), rh=(70, -100)) + M(1250, 880, 1.15, IV, "smile", lh=(-30, -50), rh=(30, -50)) + M(1470, 890, .9, DAN, "sulk") + M(1560, 890, .7, GAV, "sulk")
    return svg(b, *DAYC)
def s19():
    r = R(19); b = town_street(r) + M(800, 880, 1.2, IV, "open", lh=(-80, -130), rh=(80, -130)) + gal(430, 850, .75, 1, rider=None) + gal(1180, 850, .75, -1, "#4a3f5a") + konek(800, 520, .0001)
    b += konek(650, 760, .8, 1, "open", jump=True) + "".join(M(x, 890, .7, [NOB, FAT, DAN][i % 3], "open", lh=(-60, -110), rh=(60, -110)) for i, x in enumerate((100, 1480, 1330))) + sparkles(r, 14, 300, 1300, 300, 600, "#fff6c8")
    return svg(b, *DAYC)
def s20():
    r = R(20); b = dayf(r) + terem(100, 720, 380, 280, "#d98a5a", "#c0392b") + terem(1100, 720, 380, 280, "#e0a060", "#4a7ab8")
    b += M(640, 880, 1.1, DAN, "smile", lh=(-60, -60), rh=(60, -90), hold=sack(70, -60, .4).replace("<g", "<g")) + lady(800, 890, 1.0, **QN, mood="smile") + M(1000, 880, 1.1, GAV, "smile") + lady(1160, 890, .95, mood="smile", robe="#8ac0a0", trim=GOLD, hair="#3a2a2a", hat="") + M(1500, 890, .9, FAT)
    return svg(b, *DAYC)
def s21():
    r = R(21); b = f'<circle cx="260" cy="150" r="90" fill="#fff3b0"/>' + sea(520, "#7fc0ea", "#5aa0dc", r) + "".join(goat(x, y, s) for x, y, s in ((300, 620, .8), (520, 680, .7), (700, 640, .75)))
    b += f'<path d="M1000 640 Q1250 520 1500 640 V700 H1000 Z" fill="#8fd47c"/>' + oak(1200, 640, 260) + f'<rect x="1260" y="590" width="130" height="60" rx="12" fill="#fff"/><rect x="1260" y="590" width="130" height="60" rx="12" fill="none" stroke="#d9a020" stroke-width="6"/>'
    b += horse(900, 330, .5, 1, "#fafafa", GOLD, gallop=True) + cloud(1300, 140, 1.6, "#9aa8c8") + f'<path d="M1300 200 l-40 70 h50 l-30 70" stroke="{GOLD}" stroke-width="10" fill="none" stroke-linejoin="round"/>' + sparkles(r, 16, 700, 1500, 40, 380, "#ffe27a")
    return svg(b, *DAYC)
def s22():
    r = R(22); b = stall_row(r) + gal(350, 700, .9, 1) + gal(900, 700, .9, 1, "#4a3f5a") + f'<path d="M1100 700 Q1200 540 1380 700 Z" fill="#e8c460"/><circle cx="1220" cy="640" r="12" fill="#fff"/><circle cx="1300" cy="640" r="12" fill="#fff"/><circle cx="1224" cy="640" r="5" fill="{INK}"/><circle cx="1304" cy="640" r="5" fill="{INK}"/>'
    b += M(1120, 900, .5, IV, "sleep") + f'<rect x="440" y="780" width="300" height="100" rx="20" fill="#c8985a"/>'
    return svg(b, "#f0d8a8", "#f0d8a8")
def s23():
    r = R(23); b = stall_row(r) + "<rect width='1600' height='900' fill='#1a1a3a' opacity='.45'/>" + gal(420, 700, .9, 1) + gal(980, 700, .9, 1, "#4a3f5a") + M(700, 890, 1.15, IV, "smile", lh=(-70, -80), rh=(70, -100))
    b += feather(1250, 700, 1.3, -10) + f'<rect x="1160" y="740" width="180" height="120" rx="14" fill="#8a6a3a"/>' + M(1480, 880, .6, CHB, "open") + sparkles(r, 20, 500, 1400, 300, 800, "#ffe27a")
    return svg(b, "#f0d8a8", "#f0d8a8")
def s24():
    r = R(24); b = stall_row(r) + "<rect width='1600' height='900' fill='#ffb88a' opacity='.25'/>" + gal(330, 700, .9, 1) + gal(1250, 700, .9, -1, "#4a3f5a") + M(640, 880, 1.15, IV, "sleep", lh=(-60, -20), rh=(60, -20)) + M(1000, 880, 1.1, CHB, "smile", lh=(-70, -60), rh=(70, -100)).replace("", "") + feather(1080, 560, .9, 10)
    return svg(b, "#f0d8a8", "#f0d8a8")
def s25():
    r = R(25); b = throne_room(r) + throne(800, 640, 1.1) + tsar(800, 640, .9, "open", lh=(-60, -60), rh=(70, -130)) + sack(0, 0, .0001)
    b += M(330, 860, .9, NOB, "open", lh=(-60, -120), rh=(60, -60)) + M(520, 890, .8, NOB, "open", coat="#7a4a8a") + M(1230, 880, .9, NOB, "open", coat="#4a8a5a", flip=-1) + f'<path d="M280 760 q-30 -20 -20 -50 M1300 740 q30 -20 20 -50" stroke="{GOLD}" stroke-width="7" fill="none" stroke-linecap="round"/>'
    return svg(b, "#f6e0b8", "#f6e0b8")
def s26():
    r = R(26); b = stall_row(r) + gal(300, 700, .9, 1) + gal(1250, 700, .9, -1, "#4a3f5a") + M(780, 870, 1.15, IV, "sleep", lh=(-60, -20), rh=(60, -20))
    b += M(480, 860, .9, NOB, "smile", lh=(-60, -70), rh=(60, -100)) + M(1080, 860, .9, NOB, "smile", coat="#7a4a8a", flip=-1) + f'<path d="M560 700 l60 40 M1000 700 l-60 40" stroke="#8a5a3a" stroke-width="10" stroke-linecap="round"/>'
    return svg(b, "#f0d8a8", "#f0d8a8")
def s27():
    r = R(27); b = throne_room(r) + throne(1050, 640, 1.0) + tsar(1050, 640, .85, "open", lh=(-80, -110), rh=(80, -110)) + M(470, 890, 1.15, IV, "open", lh=(-70, -50), rh=(70, -50)) + f'<rect x="1290" y="560" width="150" height="90" rx="12" fill="#8a5a3a" stroke="{GOLD}" stroke-width="8"/>' + feather(1365, 520, .8)
    return svg(b, "#f6e0b8", "#f6e0b8")
def s28():
    r = R(28); b = stall_row(r).replace("#f0d8a8", "#e8cf98") + haystack(1250, 880, 1.2) + M(560, 880, 1.2, IV, "sulk", lh=(-30, -70), rh=(60, -110)) + konek(930, 880, 1.2, -1, "smile") + f'<path d="M520 440 q30 -30 20 -60" stroke="#8ac0f0" stroke-width="8" fill="none" stroke-linecap="round"/>'
    return svg(b, "#f0d8a8", "#f0d8a8")
def s29():
    r = R(29); b = f'<circle cx="1360" cy="130" r="90" fill="#fff3b0"/>' + hills("#b2e29e", "#9ad088") + meadow(700) + flowers(r, 40)
    b += f'<path d="M300 760 Q800 120 1300 760 Z" fill="#dfe6f0"/><path d="M440 700 Q800 260 1160 700" stroke="#fff" stroke-width="14" fill="none"/><path d="M560 560 Q800 400 1000 560 L1100 640 Q800 560 520 640 Z" fill="{GOLD}" opacity=".6"/>' + fpine(200, 800, 400) + fpine(1450, 800, 380) + ride(1000, 880, 1.2, -1)
    return svg(b, *DAYC)
def s30():
    r = R(30); b = nightf(r) + f'<path d="M0 760 Q800 520 1600 760 V900 H0 Z" fill="#cfd8e8"/>' + f'<path d="M520 860 Q800 600 1080 860 Z" fill="#c8a060" stroke="#8a5a3a" stroke-width="8"/>' + M(640, 892, .0001, IV)
    b += f'<circle cx="800" cy="790" r="26" fill="{SKIN}"/><circle cx="790" cy="784" r="4" fill="{INK}"/><circle cx="812" cy="784" r="4" fill="{INK}"/>'
    b += "".join(firebird(x, y, s, f) for x, y, s, f in ((300, 400, .9, 1), (1250, 330, .8, -1), (600, 220, .6, 1), (1000, 520, .7, -1), (1400, 600, .55, -1))) + f'<circle cx="800" cy="500" r="260" fill="#ffd36b" opacity=".15"/>'
    return svg(b, *NIGHTC)
def s31():
    r = R(31); b = throne_room(r) + "<rect width='1600' height='900' fill='#2a2a4a' opacity='.35'/>" + f'<circle cx="800" cy="560" r="300" fill="#ffd36b" opacity=".35"/>' + firebird(800, 640, 1.5, 1) + tsar(1220, 890, 1.0, "open", lh=(-60, -120), rh=(70, -120)) + M(350, 890, 1.1, IV, "smile", lh=(-60, -60), rh=(60, -80)) + M(560, 890, .9, NOB, "open", lh=(-30, -140), rh=(30, -140)) + M(1470, 890, .8, NOB, "open", coat="#7a4a8a", lh=(-30, -140), rh=(30, -140)) + sparkles(r, 30, 300, 1300, 100, 700, "#fff6c8")
    return svg(b, "#f6e0b8", "#f6e0b8")
def s32():
    r = R(32); b = kitchen(r) + M(700, 600, .9, NOB, "smile", coat="#e0a040", beard="#7a4a2a") + M(900, 600, .9, DAN, "smile", coat="#4a9a6a") + M(1080, 600, .9, GAV, "open", coat="#c0392b") + M(1310, 400, .0001, CHB) + f'<g transform="translate(1310 340)"><circle r="40" fill="{SKIN}"/>{face(0,0,40,"smile")}<path d="M-40 -10 Q0 -64 40 -10 Z" fill="#4a2a5a"/></g>'
    return svg(b, "#f6e4c4", "#f6e4c4")
def s33():
    r = R(33); b = kitchen(r) + M(520, 600, 1.0, NOB, "open", coat="#e0a040", beard="#7a4a2a", lh=(-70, -90), rh=(60, -100)) + M(880, 600, .85, DAN, "open", coat="#4a9a6a") + M(1060, 600, .85, GAV, "open", coat="#c0392b")
    b += bubble(520, 160, 130, f'<g transform="translate(520 240)"><path d="M-90 40 Q0 70 90 40 L70 -10 H-70 Z" fill="{GOLD}"/>{lady(0, 20, .42, **MAID, mood="smile")}</g>')
    return svg(b, "#f6e4c4", "#f6e4c4")
def s34():
    r = R(34); b = room("#f0d8e0", "#b98a6a") + window(1180, 120, 280, 280, "#2c3a78") + f'<rect x="200" y="540" width="560" height="220" rx="30" fill="#e0564a"/><rect x="200" y="520" width="560" height="60" rx="30" fill="#fff"/>' + tsar(480, 540, .85, "open", lh=(-70, -70), rh=(80, -140), coat="#f6f0e0")
    b += M(1020, 890, 1.15, IV, "sulk", coat="#f6f0e0", pants="#f6f0e0", lh=(-40, -40), rh=(40, -60)) + sparkles(r, 10, 100, 700, 100, 400, "#ffe27a")
    return svg(b, "#f0d8e0", "#f0d8e0")
def s35():
    r = R(35); b = f'<circle cx="300" cy="170" r="90" fill="#ffd8a0"/>' + sea(520, "#7fc0ea", "#5aa0dc", r) + f'<path d="M0 760 Q400 700 900 780 T1600 760 V900 H0 Z" fill="#f2dcaa"/>' + fpine(160, 800, 420) + fpine(1480, 800, 380) + ride(520, 880, 1.3, 1)
    b += f'<path d="M980 560 q40 -50 90 -20 q60 -40 90 10" stroke="#fff" stroke-width="14" fill="none" stroke-linecap="round" opacity=".9"/>'
    return svg(b, "#ffd8b0", "#f2fbe6")
def s36():
    r = R(36); b = f'<circle cx="1300" cy="150" r="100" fill="#fff3b0"/>' + sea(480, "#7fc0ea", "#5aa0dc", r) + f'<path d="M0 700 Q500 660 1000 720 T1600 700 V900 H0 Z" fill="#f2dcaa"/>' + tent(560, 820, 1.7)
    b += f'<g transform="translate(1180 600)"><path d="M-130 0 Q0 80 130 0 Z" fill="{GOLD}" stroke="#d9a020" stroke-width="8"/><path d="M60 -10 L150 60" stroke="#c8d0d8" stroke-width="10" stroke-linecap="round"/></g>' + lady(1180, 600, .5, **MAID, mood="smile") + lady(560, 840, .85, **MAID, mood="smile", lh=(-60, -50), rh=(60, -50))
    b += f'<circle cx="1100" cy="500" r="1" fill="none"/>' + M(870, 880, .8, IV, "open", lh=(-60, -70), rh=(60, -90)) + sparkles(r, 20, 300, 1500, 520, 700, "#fff")
    return svg(b, *DAYC)
def s37():
    r = R(37); b = f'<path d="M0 0 H1600 V900 H0Z" fill="#fff"/>' + "".join(f'<circle cx="0" cy="0" r="0"/>' for _ in range(0)) + sea(520, "#7a90d8", "#5a70c0", r) + f'<path d="M0 740 Q600 700 1100 760 T1600 740 V900 H0 Z" fill="#f2dcaa"/>' + tent(420, 800, 1.5) + M(900, 880, 1.2, IV, "sleep", lh=(-40, -30), rh=(40, -30)) + konek(1250, 880, 1.2, -1, "open") + f'<path d="M1180 700 l-60 -30 M1300 690 l30 -50" stroke="{INK}" stroke-width="0"/>'
    return svg(b.replace('<path d="M0 0 H1600 V900 H0Z" fill="#fff"/>', ""), "#ffb88a", "#7a90d8")
def s38():
    r = R(38); b = f'<circle cx="1300" cy="150" r="100" fill="#fff3b0"/>' + sea(480, "#7fc0ea", "#5aa0dc", r) + f'<path d="M0 700 Q500 660 1000 720 T1600 700 V900 H0 Z" fill="#f2dcaa"/>' + tent(400, 840, 1.6) + lady(760, 880, 1.2, **MAID, mood="open", lh=(-70, -40), rh=(70, -140)) + M(1000, 880, 1.2, IV, "smile", lh=(-80, -80), rh=(-60, -140))
    b += f'<path d="M820 400 Q900 520 960 640" stroke="#e0b860" stroke-width="14" fill="none" stroke-linecap="round"/>' + konek(1380, 880, 1.1, -1, "open") + sparkles(r, 14, 500, 1300, 300, 700, "#fff6c8")
    return svg(b, *DAYC)
def s39():
    r = R(39); b = throne_room(r, "#f6e0b8", "#7a5ad8") + f'<rect x="520" y="560" width="560" height="50" rx="14" fill="#a8703c"/>' + lady(1020, 890, 1.35, **MAID, mood="sulk", flip=-1) + tsar(520, 890, 1.15, "smile", lh=(-70, -50), rh=(80, -140))
    b += f'<path d="M700 300 q16 -30 32 0 q16 -30 32 0 q-32 40 -64 0" fill="{RED}" opacity=".0"/>' + sparkles(r, 16, 300, 1300, 120, 520, "#ffd0e0")
    return svg(b, "#f6e0b8", "#f6e0b8")
def s40():
    r = R(40); b = throne_room(r) + tsar(480, 890, 1.15, "open", lh=(-70, -60), rh=(90, -120)) + M(900, 890, 1.1, IV, "sulk", lh=(-50, -50), rh=(40, -90)) + lady(1280, 890, 1.2, **MAID, mood="smile", lh=(-60, -60), rh=(70, -130))
    b += bubble(1230, 190, 90, f'<g transform="translate(1230 190)">{moon_face(-30, 0, 34)}{sun_face(40, 0, 26)}</g>')
    return svg(b, "#f6e0b8", "#f6e0b8")
def s41():
    r = R(41); b = sky_land(r) + "".join(f'<path d="M{x} {y} q-110 6 -220 0" stroke="#fff" stroke-width="12" stroke-linecap="round" opacity=".8"/>' for x, y in ((300, 480), (240, 560), (280, 640))) + ride(800, 700, 1.6, 1, "open") + sparkles(r, 24, 0, 1600, 80, 400, "#fff")
    return svg(b, "#9ad8ff", "#e8f6ff")
def s42():
    r = R(42); b = f'<circle cx="260" cy="150" r="90" fill="#fff3b0"/>' + sea(500, "#7fc0ea", "#5aa0dc", r) + whale(800, 720, 1.6, 1, village=True) + ride(900, 460, .5, 1, "open", ms=.7) + cloud(1300, 180, 1.2, "#fff")
    return svg(b, "#bfe9ff", "#e8f6ff")
def s43():
    r = R(43); b = f'<rect width="1600" height="900" fill="#8ad0ff"/>' + sky_land(r) + f'<path d="M0 760 Q400 680 800 740 T1600 720 V900 H0 Z" fill="#a8d8ff"/><path d="M0 820 Q500 760 1000 810 T1600 800 V900 H0 Z" fill="#8cc4ee"/>' + flowers(r, 30, 780, 880, ("#fff", "#ffd36b", "#c8e0ff"))
    b += ride(520, 800, 1.5, 1, "smile") + "".join(f'<path d="M{x} 300 V420" stroke="#b57a4a" stroke-width="10"/><ellipse cx="{x}" cy="290" rx="16" ry="30" fill="#fff6c8"/>' for x in (1100, 1230, 1360)) + sparkles(r, 16, 700, 1500, 100, 500, "#fff")
    return svg(b, "#8ad0ff", "#e8f6ff")
def s44():
    r = R(44); b = f'<rect width="1600" height="900" fill="#2c3a78"/>' + stars(r, 60, 500) + f'<path d="M0 740 Q400 680 800 740 T1600 720 V900 H0 Z" fill="#7aa8e8"/>'
    b += "".join(f'<rect x="{x}" y="260" width="46" height="480" rx="20" fill="#e8f4ff" opacity=".9"/><path d="M{x+23} 260 Q{x-10} 360 {x+23} 460 T{x+23} 700" stroke="{GOLD}" stroke-width="8" fill="none"/>' for x in (420, 1130)) + f'<path d="M400 270 Q790 90 1190 270 Z" fill="#e8f4ff" stroke="{GOLD}" stroke-width="8"/>'
    b += "".join(f'<path d="M{x} 130 l12 24 26 4 -19 18 5 26 -24 -13 -24 13 5 -26 -19 -18 26 -4 Z" fill="{GOLD}"/>' for x in (610, 800, 990)) + f'<path d="M780 30 h40 v100 h-40 Z M750 60 h100 v28 h-100 Z" fill="{GOLD}"/>'
    b += terem(660, 760, 280, 230, "#fff0d0", "#6a7ab8") + "".join(f'<g transform="translate({x} 560)"><rect x="-44" y="-10" width="88" height="90" rx="14" fill="none" stroke="{GOLD}" stroke-width="6"/><ellipse cx="0" cy="40" rx="20" ry="14" fill="#7ad0ff"/><circle cx="16" cy="28" r="8" fill="#7ad0ff"/></g>' for x in (230, 1370)) + ride(180, 880, 1.0, 1) + sparkles(r, 22, 100, 1500, 120, 700, "#fff6c8")
    return svg(b, "#2c3a78", "#8a9ad0")
def s45():
    r = R(45); b = f'<rect width="1600" height="900" fill="#2c3a78"/>' + stars(r, 60, 500) + f'<path d="M0 760 Q500 700 1000 760 T1600 740 V900 H0 Z" fill="#7aa8e8"/>' + moon_face(1060, 400, 190) + M(500, 890, 1.3, IV, "smile", lh=(-80, -70), rh=(60, -120)) + konek(250, 880, .8, 1) + sparkles(r, 24, 100, 1500, 100, 700, "#fff6c8")
    return svg(b, "#2c3a78", "#8a9ad0")
def s46():
    r = R(46); b = f'<rect width="1600" height="900" fill="#2c3a78"/>' + stars(r, 60, 500) + f'<path d="M0 760 Q500 700 1000 760 T1600 740 V900 H0 Z" fill="#7aa8e8"/>' + moon_face(900, 360, 200) + M(560, 890, 1.3, IV, "smile", lh=(-30, -150), rh=(60, -140)) + konek(1350, 880, .9, -1, "smile") + sparkles(r, 24, 100, 1500, 100, 700, "#ffd0e0")
    return svg(b, "#2c3a78", "#8a9ad0")
def s47():
    r = R(47); b = f'<circle cx="1300" cy="140" r="90" fill="#fff3b0"/>' + sea(480, "#7fc0ea", "#5aa0dc", r) + f'<path d="M0 640 Q500 560 1000 640 T1600 620 V900 H0 Z" fill="#8fd47c"/>' + "".join(terem(x, 700, 160, 120, "#d98a5a", "#c0392b") for x in (60, 300))
    for x, y in ((560, 800), (900, 820), (1220, 800)): b += f'<rect x="{x-90}" y="{y-80}" width="180" height="70" rx="12" fill="#a8703c"/><circle cx="{x-50}" cy="{y}" r="26" fill="#6a4a2a"/><circle cx="{x+50}" cy="{y}" r="26" fill="#6a4a2a"/><path d="M{x-70} {y-80} q70 -80 140 0 Z" fill="#e8c460"/>' + M(x + 130, y + 80, .55, [DAN, GAV, FAT][(x // 300) % 3], "open", lh=(-40, -110), rh=(40, -110))
    b += konek(1450, 880, .9, -1, "open") + "".join(f'<path d="M{x} {y} q-50 6 -100 0" stroke="#fff" stroke-width="8" stroke-linecap="round" opacity=".6"/>' for x, y in ((420, 760), (780, 780)))
    return svg(b, *DAYC)
def s48():
    r = R(48); b = f'<circle cx="260" cy="150" r="90" fill="#fff3b0"/>' + sea(460, "#7fc0ea", "#5aa0dc", r) + whale(1050, 700, 1.5, -1, mouth=True) + ship(380, 700, .55, 1) + ship(660, 640, .45, 1) + ship(230, 800, .5, 1)
    b += konek(250, 880, .0001) + ride(1450, 520, .55, -1, "open", ms=.7) + sparkles(r, 22, 100, 800, 460, 800, "#fff")
    return svg(b, *DAYC)
def s49():
    r = R(49); b = f'<circle cx="1300" cy="140" r="90" fill="#fff3b0"/>' + sea(480, "#7fc0ea", "#5aa0dc", r) + "".join(ship(x, y, s, f) for x, y, s, f in ((300, 640, .7, 1), (700, 700, .85, 1), (1100, 660, .7, -1), (1400, 780, .9, -1), (520, 560, .5, 1), (900, 560, .45, -1)))
    b += "".join(f'<circle cx="{x}" cy="{y}" r="{k}" fill="#fff" opacity=".8"/>' for x, y, k in ((460, 540, 28), (500, 520, 20), (1220, 520, 30), (1250, 490, 22))) + whale(800, 880, .7, -1) + sparkles(r, 20, 100, 1500, 140, 460, "#fff6c8")
    return svg(b, *DAYC)
def uw(r, c1="#3a8ad8", c2="#1a4a98"):
    b = f'<rect width="1600" height="900" fill="{c1}"/><rect y="500" width="1600" height="400" fill="{c2}" opacity=".5"/><path d="M0 800 Q400 740 800 800 T1600 790 V900 H0 Z" fill="#e8d8a8"/>'
    b += "".join(f'<circle cx="{r.randint(0,1600)}" cy="{r.randint(60,700)}" r="{r.randint(5,16)}" fill="#fff" opacity=".35"/>' for _ in range(30))
    b += "".join(f'<path d="M{x} 800 q-20 -80 0 -150 M{x} 800 q30 -60 10 -120" stroke="#ff9c8c" stroke-width="12" fill="none" stroke-linecap="round"/>' for x in (80, 1500))
    return b
def s50():
    r = R(50); b = uw(r) + whale(800, 640, 1.0, -1, mood="smile") + fish(200, 560, 1.0, 1, "#cfd8e8") + fish(360, 700, .9, 1, "#cfd8e8") + fish(1350, 480, .9, -1, "#8ac0a0") + f'<path d="M600 300 l30 -40 30 30 30 -40 30 40 Z" fill="{GOLD}"/>'
    return svg(b, "#3a8ad8", "#1a4a98")
def s51():
    r = R(51); b = uw(r, "#4aa0a0", "#2a6a6a") + f'<path d="M0 760 Q800 700 1600 760 V900 H0Z" fill="#8a7a5a"/>' + "".join(f'<path d="M{x} 800 q-10 -240 10 -420 M{x+20} 800 q20 -200 -4 -380" stroke="#6a9a5a" stroke-width="16" fill="none" stroke-linecap="round"/>' for x in (120, 1480, 1400))
    b += fish(760, 600, 1.1, 1, "#9a8a5a", spiky=True, mouth=True) + fish(1020, 620, 1.2, -1, "#c8a030", mouth=True) + f'<path d="M880 500 l-20 -40 M900 480 l10 -44" stroke="{GOLD}" stroke-width="8" stroke-linecap="round"/>'
    b += fish(280, 420, 1.0, 1, "#8ac0f0") + fish(420, 560, .9, 1, "#8ac0f0") + sparkles(r, 12, 700, 1100, 360, 700, "#fff")
    return svg(b, "#4aa0a0", "#2a6a6a")
def s52():
    r = R(52); b = uw(r) + f'<rect x="640" y="660" width="300" height="180" rx="22" fill="#a8703c" stroke="{GOLD}" stroke-width="10"/><path d="M640 740 H940" stroke="{GOLD}" stroke-width="10"/><circle cx="790" cy="740" r="18" fill="{GOLD}"/>'
    b += "".join(fish(x, y, .8, f, "#9ab8d8") for x, y, f in ((300, 640, 1), (380, 720, 1), (1200, 640, -1), (1130, 730, -1))) + fish(540, 420, 1.1, 1, "#cfd8e8") + fish(1050, 420, 1.1, -1, "#cfd8e8") + fish(800, 280, 1.0, 1, "#9a8a5a", spiky=True)
    return svg(b, "#3a8ad8", "#1a4a98")
def s53():
    r = R(53); b = f'<path d="M0 0 H1600 V900 H0Z" fill="#ff9c78"/>' + sea(500, "#8a90d8", "#6a70c0", r) + f'<circle cx="1300" cy="520" r="100" fill="#ffd36b"/>' + f'<path d="M0 740 Q600 700 1100 770 T1600 750 V900 H0 Z" fill="#f2dcaa"/>' + whale(1150, 640, .75, -1, mouth=False)
    b += f'<rect x="760" y="760" width="190" height="110" rx="18" fill="#a8703c" stroke="{GOLD}" stroke-width="8"/>' + M(450, 880, 1.2, IV, "open", lh=(-70, -60), rh=(70, -90)) + konek(240, 880, 1.0, 1, "smile", jump=True) + sparkles(r, 14, 100, 1500, 120, 440, "#fff6c8")
    return svg(b.replace('<path d="M0 0 H1600 V900 H0Z" fill="#ff9c78"/>', ""), "#ffb08a", "#8a90d8")
def s54():
    r = R(54); b = throne_room(r, "#f6e0b8", "#7a5ad8") + tsar(520, 890, 1.15, "open", beard="#fff", lh=(-80, -50), rh=(80, -110)) + lady(1000, 890, 1.35, **MAID, mood="sulk", flip=-1, lh=(-60, -50), rh=(60, -120)) + f'<rect x="1230" y="780" width="170" height="110" rx="18" fill="#a8703c" stroke="{GOLD}" stroke-width="8"/>'
    return svg(b, "#f6e0b8", "#f6e0b8")
def s55():
    r = R(55); b = stall_row(r).replace("#f0d8a8", "#e0c890") + window(1100, 120, 300, 300, "#2c3a78") + haystack(1250, 880, 1.2) + M(500, 880, 1.2, IV, "sulk", lh=(-40, -70), rh=(60, -110)) + konek(900, 880, 1.2, -1, "smile") + moon(1250, 270, 40)
    b += bubble(840, 330, 110, f'<g transform="translate(840 400) scale(.0001)"></g>' + cauldron(840, 440, .55, "milk", True))
    return svg(b, "#f0d8a8", "#f0d8a8")
def s56():
    r = R(56); b = courtyard(r) + cauldron(420, 880, 1.0, "cold") + cauldron(760, 870, 1.0, "water") + cauldron(1100, 880, 1.0, "milk") + tsar(1380, 660, .75, "open") + lady(1470, 660, .7, **MAID, mood="smile")
    b += M(580, 600, .5, NOB, "smile", coat="#e0a040") + M(930, 600, .5, DAN, "smile", coat="#4a9a6a") + M(250, 620, .5, GAV, "smile") + M(760, 480, .0001, IV) + sparkles(r, 10, 300, 1100, 140, 400, "#fff")
    return svg(b, *DAYC)
def s57():
    r = R(57); b = courtyard(r) + cauldron(300, 880, .9, "cold") + cauldron(1300, 880, .9, "milk") + M(800, 890, 1.4, IV, "smile", coat="#4a7ad8", hat="prince", hatcol="#c0392b", pants="#2a3a6a", lh=(-70, -60), rh=(70, -60)) + konek(480, 880, 1.0, 1, "open")
    b += "".join(M(x, 890, .8, [NOB, DAN, GAV, FAT][i % 4], "open", lh=(-50, -110), rh=(50, -110)) for i, x in enumerate((1050, 1170, 90, 1480))) + lady(1150, 700, .0001) + sparkles(r, 50, 500, 1100, 160, 780, "#fff6c8")
    return svg(b, *DAYC)
def s58():
    r = R(58); b = courtyard(r) + cauldron(760, 880, 1.3, "milk") + f'<g transform="translate(900 600) rotate(12)"><path d="M-50 0 L-50 -50 L-26 -26 L0 -62 L26 -26 L50 -50 L50 0 Z" fill="{GOLD}" stroke="#d9a020" stroke-width="5"/></g>'
    b += lady(1250, 890, 1.35, **MAID, mood="smile", lh=(-60, -60), rh=(60, -150)) + M(430, 890, 1.15, IV, "open", coat="#4a7ad8", hat="prince", hatcol="#c0392b", pants="#2a3a6a") + "".join(M(x, 890, .65, [NOB, DAN, GAV][i % 3], "open", lh=(-50, -110), rh=(50, -110)) for i, x in enumerate((90, 200, 1500)))
    return svg(b, *DAYC)
def s59():
    r = R(59); b = throne_room(r) + f'<rect x="150" y="580" width="1300" height="60" rx="18" fill="#fff"/><rect x="200" y="640" width="30" height="180" fill="#b57a4a"/><rect x="1370" y="640" width="30" height="180" fill="#b57a4a"/>'
    b += "".join(f'<circle cx="{x}" cy="566" r="26" fill="{c}"/>' for x, c in ((260, "#ffd54a"), (400, "#e0564a"), (1200, "#6cbf72"), (1340, "#ffd54a"), (560, "#ff9ec0"), (1040, "#ffd54a")))
    b += M(660, 620, 1.1, IV, "smile", coat="#4a7ad8", hat="prince", hatcol="#c0392b", pants="#2a3a6a", lh=(-60, -80), rh=(70, -130)) + lady(950, 620, 1.05, **MAID, mood="smile") + konek(1400, 880, .8, -1, "open", jump=True) + "".join(M(x, 890, .75, [NOB, DAN, GAV][i % 3], "open", lh=(-50, -100), rh=(50, -100)) for i, x in enumerate((80, 1500))) + sparkles(r, 50, 100, 1500, 60, 540, "#fff6c8")
    return svg(b, "#f6e0b8", "#f6e0b8")

def cover(ru=False):
    r = R(99); b = sparkles(r, 70, 0, 3000, 40, 1500, "#fff6c8")
    b += f'<circle cx="2420" cy="1420" r="250" fill="#fff0a8" opacity=".3"/><circle cx="2420" cy="1420" r="160" fill="#fff0a8"/><circle cx="2500" cy="1380" r="140" fill="#3a4a8a"/>'
    b += f'<path d="M0 2300 Q600 2150 1200 2260 T3000 2200 V3000 H0 Z" fill="#6a8ad0"/><path d="M0 2600 Q900 2480 1700 2620 T3000 2560 V3000 H0 Z" fill="#4a6ab8"/>'
    b += f'<g transform="translate(1500 2420) scale(1.7)">{town(0, 0, 1.0)}</g>' + f'<g transform="translate(900 2860) scale(3.4)">{ride(0, 0, 1.0, 1, "open")}</g>'
    b += f'<g transform="translate(2300 1900) scale(2.6)">{firebird(0, 0, 1.0, -1)}</g>' + f'<g transform="translate(2450 2900) scale(1.5)">{whale(0, 0, 1.0, -1)}</g>'
    T = ("ПЁТР ЕРШОВ", ["Конёк-", "Горбунок"]) if ru else ("PYOTR YERSHOV", ["The Little", "Humpbacked Horse"])
    fs = 240 if ru else 220
    b += f'<text x="1500" y="330" text-anchor="middle" font-family="Georgia, serif" font-size="100" letter-spacing="30" fill="#fff6c8">{T[0]}</text>'
    b += "".join(f'<text x="1500" y="{680 + i*290}" text-anchor="middle" font-family="Georgia, serif" font-weight="bold" font-size="{fs}" fill="#fff">{t}</text>' for i, t in enumerate(T[1]))
    b += f'<rect x="1200" y="1300" width="600" height="10" rx="5" fill="{GOLD}"/>'
    return svg(b, "#2c3a78", "#8a9ad8", 3000, 3000)

NAMES = {}
for i in range(1, 60):
    NAMES[i] = globals()[f"s{i:02d}"]
ARTNAMES = ["01_old_man_sons", "02_danilo_hides", "03_gavrilo_cold", "04_ivan_stove", "05_mare_ride", "06_mare_promise", "07_ivan_tells", "08_golden_horses", "09_empty_barn", "10_konek_ride", "11_brothers_bargain", "12_camp_fire", "13_ride_to_light", "14_firebird_feather", "15_capital_market", "16_horse_row", "17_warden_reports", "18_tsar_buys", "19_ivan_groom", "20_brothers_home", "21_prelude", "22_chamberlain_hides", "23_ivan_braids_manes", "24_feather_stolen", "25_courtiers_tumble", "26_waking_ivan", "27_ivan_before_tsar", "28_konek_advice", "29_silver_mountain", "30_trough_trap", "31_firebird_hall", "32_cooks_story", "33_servant_tells", "34_maiden_order", "35_ride_to_ocean", "36_maiden_boat", "37_ivan_asleep", "38_ivan_catches", "39_tsar_courts", "40_tsar_sends_ivan", "41_ride_flying", "42_whale_island", "43_sky_land", "44_crystal_gate", "45_moon_talks", "46_moon_farewell", "47_villagers_flee", "48_whale_frees_ships", "49_ships_sail", "50_whale_court", "51_ruff_fights_carp", "52_herring_chest", "53_whale_gives_chest", "54_tsar_too_old", "55_cauldrons_plan", "56_cauldrons_yard", "57_ivan_handsome", "58_tsar_cauldron", "59_wedding_feast"]
FILES = {n: NAMES[i + 1] for i, n in enumerate(ARTNAMES)}
FILES["cover"] = cover; FILES["cover_ru"] = lambda: cover(True)
if __name__ == "__main__":
    import sys
    for n, fn in FILES.items():
        if len(sys.argv) > 1 and n not in sys.argv[1:]: continue
        open(f"{OUT}/{n}.svg", "w", encoding="utf-8").write(fn()); print("wrote", n)
