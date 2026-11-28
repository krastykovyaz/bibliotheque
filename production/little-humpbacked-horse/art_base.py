#!/usr/bin/env python3
"""Illustrations and cover for "The Tale of the Dead Princess and the Seven Knights" as SVG, soft, bright, rounded picture-book style for children:
pale winter blues, warm window gold, berry red, spring green; friendly round faces, no sharp or frightening shapes."""
import random, math, os
OUT = "art"; os.makedirs(OUT, exist_ok=True)
SKIN, ROSE, INK, GOLD, RED, GREEN, BROWN, SNOW, ICE, BLUE = "#ffdcbd", "#ff9c8c", "#4a3326", "#ffd36b", "#e0564a", "#6cbf72", "#9a6a46", "#ffffff", "#bfe6ff", "#8cc4ee"


def R(s): return random.Random(s)


def svg(body, c1="#bfe3ff", c2="#fff6e6", w=1600, h=900):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}"><defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs><rect width="{w}" height="{h}" fill="url(#sky)"/>{body}</svg>')


def flakes(r, n, w=1600, h=900, op=.9, big=6): return "".join(f'<circle cx="{r.randint(0,w)}" cy="{r.randint(0,h)}" r="{r.uniform(2,big):.1f}" fill="#fff" opacity="{op}"/>' for _ in range(n))


def face(cx, cy, r, mood="smile", old=False):
    e = f'<circle cx="{cx-r*.36}" cy="{cy-r*.05}" r="{r*.09}" fill="{INK}"/><circle cx="{cx+r*.36}" cy="{cy-r*.05}" r="{r*.09}" fill="{INK}"/>'
    e += f'<circle cx="{cx-r*.55}" cy="{cy+r*.22}" r="{r*.17}" fill="{ROSE}" opacity=".55"/><circle cx="{cx+r*.55}" cy="{cy+r*.22}" r="{r*.17}" fill="{ROSE}" opacity=".55"/>'
    if mood == "smile": e += f'<path d="M{cx-r*.3} {cy+r*.3} Q{cx} {cy+r*.6} {cx+r*.3} {cy+r*.3}" stroke="{INK}" stroke-width="{r*.08}" fill="none" stroke-linecap="round"/>'
    elif mood == "sulk": e += f'<path d="M{cx-r*.25} {cy+r*.5} Q{cx} {cy+r*.3} {cx+r*.25} {cy+r*.5}" stroke="{INK}" stroke-width="{r*.08}" fill="none" stroke-linecap="round"/><path d="M{cx-r*.5} {cy-r*.25} Q{cx-r*.36} {cy-r*.33} {cx-r*.2} {cy-r*.25} M{cx+r*.5} {cy-r*.25} Q{cx+r*.36} {cy-r*.33} {cx+r*.2} {cy-r*.25}" stroke="{INK}" stroke-width="{r*.06}" fill="none" stroke-linecap="round"/>'
    elif mood == "open": e += f'<ellipse cx="{cx}" cy="{cy+r*.42}" rx="{r*.2}" ry="{r*.24}" fill="#b04a3a"/>'
    elif mood == "sleep": e = f'<path d="M{cx-r*.5} {cy} Q{cx-r*.36} {cy+r*.12} {cx-r*.2} {cy} M{cx+r*.2} {cy} Q{cx+r*.36} {cy+r*.12} {cx+r*.5} {cy}" stroke="{INK}" stroke-width="{r*.07}" fill="none" stroke-linecap="round"/><circle cx="{cx-r*.58}" cy="{cy+r*.22}" r="{r*.17}" fill="{ROSE}" opacity=".55"/><circle cx="{cx+r*.58}" cy="{cy+r*.22}" r="{r*.17}" fill="{ROSE}" opacity=".55"/><path d="M{cx-r*.25} {cy+r*.4} Q{cx} {cy+r*.55} {cx+r*.25} {cy+r*.4}" stroke="{INK}" stroke-width="{r*.07}" fill="none" stroke-linecap="round"/>'
    return e
def sparkles(r, n, x0=0, x1=1600, y0=0, y1=900, col="#fff"):
    s = ""
    for _ in range(n):
        x, y, k = r.uniform(x0, x1), r.uniform(y0, y1), r.uniform(8, 20)
        s += f'<path d="M{x:.0f} {y-k:.0f} L{x+k*.28:.0f} {y-k*.28:.0f} L{x+k:.0f} {y:.0f} L{x+k*.28:.0f} {y+k*.28:.0f} L{x:.0f} {y+k:.0f} L{x-k*.28:.0f} {y+k*.28:.0f} L{x-k:.0f} {y:.0f} L{x-k*.28:.0f} {y-k*.28:.0f} Z" fill="{col}" opacity=".85"/>'
    return s
