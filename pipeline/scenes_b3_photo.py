"""Scenes: What If Humans Could Photosynthesize? (+ photo, sea slug and mantis shrimp Shorts).

Look: bright daylight greens + warm sunlight (light gradients), turquoise for reef/ocean scenes,
deep green for cards and titles. Motif: a green-skinned stylised figure with leaves and sun rays.
All scene art is drawn in a 1000 x 620 logical box (see stage()) so it fits 16:9 and the Shorts safe zone.
"""
import math, random
from contextlib import contextmanager
from common2 import *
import geo
import scenes_b3_kit as kit

LIME = "#B8F25C"
PAL = dict(accent=LIME, chip="#16401c", title2=ACCENT)
LEAF = "#3fae4a"; LEAF_D = "#25732f"; SKIN = "#d9a77c"; GSKIN = "#5cbf55"
NAVY = "#0b1030"

# ---------------------------------------------------------------- layout helpers
def box(S):
    W, H = S.W, S.H
    if S.P: x0, y0, x1, y1 = 0.03 * W, 0.25 * H, 0.97 * W, 0.58 * H
    else: x0, y0, x1, y1 = 0.03 * W, 0.11 * H, 0.97 * W, 0.95 * H
    k = min((x1 - x0) / 1000, (y1 - y0) / 620)
    return (x0 + x1) / 2, (y0 + y1) / 2, k

@contextmanager
def stage(c, S):
    cx, cy, k = box(S)
    c.save(); c.translate(cx, cy); c.scale(k, k)
    try: yield k
    finally: c.restore()

def CH(S): return 27 if not S.P else 31

def ch(c, S, s, x, y, p, **kw):
    chip(c, s, x, y, p, kw.pop("size", CH(S)), **kw)

def big(c, s, x, y, size, colr="#ffffff", a=1.0, w=900, align="c"):
    if a <= 0: return
    text(c, s, x, y, size, colr, a, w=w, align=align, stroke=size * 0.14, stroke_col=NAVY)
    text(c, s, x, y, size, colr, a, w=w, align=align)

def ground(c, S, yl, colr):
    cx_, cy_, k_ = box(S); gy = cy_ + yl * k_
    c.drawRect(skia.Rect.MakeLTRB(0, gy, S.W, S.H), paint(shader=lin(0, gy, 0, S.H, [(0, colr, 1), (0.25 if S.P else 1, mix(colr, "#0b3550", 0.65 if S.P else 0.2), 1), (1, mix(colr, "#0b3550", 0.8 if S.P else 0.25), 1)])))

def day_bg(c, W, H, top="#eaf8dc", bot="#a8d98e"): fill_bg(c, W, H, top, bot)
def sea_bg(c, W, H, top="#5fd3d6", bot="#0b6f86"):
    fill_bg(c, W, H, top, bot)

def rays(c, W, H, t, a=0.25, x=None):
    x = W * 0.75 if x is None else x
    for i in range(6):
        xx = x + (i - 2.5) * W * 0.09 + math.sin(t * 0.4 + i) * 20
        c.drawPath(poly([(xx - 30, 0), (xx + 30, 0), (xx - 160, H), (xx - 280, H)]), paint("#ffffff", a * (0.5 + 0.5 * math.sin(t * 0.7 + i * 1.3))))

# ---------------------------------------------------------------- props
def leaf_rot(c, x, y, s, ang, colr=LEAF, a=1.0, vein=True):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(ang)
    p = skia.Path(); p.moveTo(0, 0); p.quadTo(s * 0.55, -s * 0.5, 0, -s * 1.4); p.quadTo(-s * 0.55, -s * 0.5, 0, 0)
    c.drawPath(p, paint(colr, a))
    if vein: line(c, 0, -s * 0.05, 0, -s * 1.2, mix(colr, "#000000", 0.3), max(1.5, s * 0.06), a)
    c.restore()

def figure(c, x, y, h, skin=GSKIN, a=1.0, flat=0.0, leaves=0.0, arms=0.0, shirt=None, lie=False, hat=False, t=0.0):
    """Stylised person standing on (x, y). flat 0..1 widens into leaf-like flaps; arms 0 down .. 1 raised."""
    if a <= 0: return
    c.save(); c.translate(x, y)
    if lie: c.rotate(-90); c.translate(0, 0)
    dk = mix(skin, "#000000", 0.25)
    bw = h * (0.2 + 0.3 * flat)
    # flaps
    if flat > 0:
        for sgn in (-1, 1):
            for k in range(4):
                ang = sgn * (60 + k * 18 - 20 * flat) + math.sin(t * 1.3 + k) * 3
                leaf_rot(c, sgn * bw * 0.4, -h * (0.7 - k * 0.07), h * (0.22 + 0.2 * flat), ang, mix(skin, LEAF, 0.4), a * clamp(flat * 1.5))
    # legs
    lw = h * 0.075
    line(c, -h * 0.05, -h * 0.42, -h * 0.07, 0, dk, lw, a); line(c, h * 0.05, -h * 0.42, h * 0.07, 0, dk, lw, a)
    # arms
    for sgn in (-1, 1):
        ang = math.radians(90 + sgn * (12 + 120 * arms))
        sx, sy = sgn * bw * 0.42, -h * 0.74
        ex, ey = sx + math.cos(ang) * h * 0.36 * (1 if sgn < 0 else 1), sy + math.sin(ang) * h * 0.36
        line(c, sx, sy, sx + sgn * abs(ex - sx), ey, skin, h * 0.065, a)
    rrect(c, -bw / 2, -h * 0.79, bw, h * 0.42, h * 0.08, skin, a)
    if shirt:
        rrect(c, -bw / 2, -h * 0.79, bw, h * 0.2, h * 0.06, shirt, a)
    circle(c, 0, -h * 0.9, h * 0.095, skin, a)
    if hat:
        oval(c, 0, -h * 0.97, h * 0.17, h * 0.035, "#e8c56a", a); rrect(c, -h * 0.08, -h * 1.05, h * 0.16, h * 0.08, h * 0.03, "#e8c56a", a)
    if leaves > 0:
        leaf_rot(c, h * 0.02, -h * 0.98, h * 0.12, 25, LEAF, a * leaves)
        leaf_rot(c, -h * 0.02, -h * 0.98, h * 0.1, -30, mix(LEAF, "#ffffff", 0.2), a * leaves)
        leaf_rot(c, bw * 0.45, -h * 0.76, h * 0.1, 60, LEAF, a * leaves)
        leaf_rot(c, -bw * 0.45, -h * 0.76, h * 0.1, -60, LEAF, a * leaves)
    c.restore()

def sunball(c, x, y, r, t, a=1.0):
    sun(c, x, y, r, t, a=a, glow=0.8)

def chloroplast(c, x, y, s, ang=0, a=1.0, colr="#3c9a3a"):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(ang)
    oval(c, 0, 0, s, s * 0.55, mix(colr, "#ffffff", 0.35), a)
    oval(c, 0, 0, s * 0.88, s * 0.46, colr, a)
    for k in range(-2, 3):
        rrect(c, k * s * 0.32 - s * 0.1, -s * 0.18, s * 0.2, s * 0.36, s * 0.06, mix(colr, "#0b3a10", 0.5), a)
    c.restore()

def salamander(c, x, y, s, t, ang=0.0, a=1.0, colr="#232a3d"):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(ang)
    w = math.sin(t * 5) * 0.12
    tail = skia.Path(); tail.moveTo(-s * 0.45, -s * 0.09)
    tail.quadTo(-s * 0.9, -s * 0.05 + w * s, -s * 1.25, w * s * 1.8); tail.quadTo(-s * 0.9, s * 0.05 + w * s, -s * 0.45, s * 0.09)
    c.drawPath(tail, paint(colr, a))
    for sx, sgn in ((0.3, 1), (0.3, -1), (-0.3, 1), (-0.3, -1)):
        kk = math.sin(t * 5 + sx * 4) * 0.08 * sgn
        line(c, sx * s, sgn * s * 0.08, sx * s + s * (0.12 + kk), sgn * s * 0.26, colr, s * 0.06, a)
    oval(c, 0, 0, s * 0.55, s * 0.14, colr, a)
    oval(c, s * 0.6, 0, s * 0.17, s * 0.14, colr, a)
    for k in range(5):
        for sgn in (-1, 1):
            circle(c, s * (0.42 - k * 0.2), sgn * s * 0.07, s * 0.035, "#ffcf3a", a)
    circle(c, s * 0.68, -s * 0.08, s * 0.03, "#ffcf3a", a); circle(c, s * 0.68, s * 0.08, s * 0.03, "#ffcf3a", a)
    c.restore()

def egg(c, x, y, r, green=1.0, a=1.0, embryo=True, t=0.0):
    circle(c, x, y, r, mix("#dff3d8", "#7fcf6a", green), a * 0.55)
    circle(c, x, y, r, "#ffffff", a * 0.6, stroke=max(1.5, r * 0.05))
    if embryo:
        circle(c, x, y, r * 0.42, "#efe0b8", a)
        circle(c, x + r * 0.15, y - r * 0.1, r * 0.07, "#3a3a3a", a)
        c.drawCircle(x, y, r * 0.42, paint("#c9a86b", a, stroke=max(1, r * 0.04)))

def larva(c, x, y, s, t, a=1.0):
    salamander(c, x, y, s, t, 0, a, colr="#6f7f5a")

def bulb(c, x, y, s, glow, a=1.0, colr="#ffe58a"):
    if glow > 0: circle(c, x, y - s * 0.2, s * (0.9 + glow * 0.8), colr, a * 0.35 * glow, blur=s * 0.3)
    circle(c, x, y - s * 0.2, s * 0.62, mix("#f4f4f4", colr, glow), a)
    c.drawCircle(x, y - s * 0.2, s * 0.62, paint("#0b1030", a * 0.5, stroke=s * 0.05))
    rrect(c, x - s * 0.28, y + s * 0.35, s * 0.56, s * 0.42, s * 0.08, "#9aa4b8", a)
    for k in range(3): line(c, x - s * 0.28, y + s * (0.45 + k * 0.11), x + s * 0.28, y + s * (0.45 + k * 0.11), "#6b7488", s * 0.03, a)
    line(c, x - s * 0.15, y + s * 0.1, x, y - s * 0.25, "#d98a1f", s * 0.04, a); line(c, x + s * 0.15, y + s * 0.1, x, y - s * 0.25, "#d98a1f", s * 0.04, a)

def cracker(c, x, y, s, a=1.0, ang=0):
    c.save(); c.translate(x, y); c.rotate(ang)
    rrect(c, -s / 2, -s / 2, s, s, s * 0.08, "#e6b85c", a)
    rrect(c, -s / 2, -s / 2, s, s, s * 0.08, "#b9873a", a, stroke=s * 0.04)
    for i in range(3):
        for j in range(3): circle(c, (i - 1) * s * 0.28, (j - 1) * s * 0.28, s * 0.04, "#a5772f", a)
    c.restore()

def court(c, x, y, w, a=1.0):
    h = w * 10.97 / 23.77
    rect(c, x - w / 2, y - h / 2, w, h, "#3f8f5a", a)
    lw = max(2, w * 0.006)
    c.drawRect(skia.Rect.MakeXYWH(x - w / 2, y - h / 2, w, h), paint("#ffffff", a, stroke=lw))
    for f in (0.137, 0.863):
        line(c, x - w / 2, y - h / 2 + f * h, x + w / 2, y - h / 2 + f * h, "#ffffff", lw, a)
    for f in (0.27, 0.73): line(c, x - w / 2 + f * w, y - h / 2 + 0.137 * h, x - w / 2 + f * w, y + h / 2 - 0.137 * h, "#ffffff", lw, a)
    line(c, x - w / 2 + 0.27 * w, y, x - w / 2 + 0.73 * w, y, "#ffffff", lw, a)
    line(c, x, y - h / 2 - 8, x, y + h / 2 + 8, "#e8eef8", lw * 2, a)

def brain(c, x, y, s, a=1.0, colr="#f2a3b3"):
    for dx in (-0.28, 0.28):
        oval(c, x + dx * s, y, s * 0.45, s * 0.36, colr, a)
    d = mix(colr, "#7a2a3a", 0.45)
    rng = random.Random(5)
    for k in range(9):
        cx = x + rng.uniform(-0.6, 0.6) * s; cy = y + rng.uniform(-0.25, 0.25) * s
        p = skia.Path(); p.moveTo(cx - s * 0.12, cy); p.quadTo(cx, cy - s * 0.12, cx + s * 0.12, cy)
        c.drawPath(p, paint(d, a, stroke=s * 0.035))
    line(c, x, y - s * 0.32, x, y + s * 0.3, d, s * 0.035, a)
    rrect(c, x - s * 0.08, y + s * 0.25, s * 0.16, s * 0.25, s * 0.06, colr, a)

def tree_big(c, x, y, h, a=1.0, t=0.0, colr=LEAF, leaf_n=46, seed=3):
    rect(c, x - h * 0.05, y - h * 0.55, h * 0.1, h * 0.55, "#7a5236", a)
    for sgn in (-1, 1): line(c, x, y - h * 0.45, x + sgn * h * 0.22, y - h * 0.72, "#7a5236", h * 0.04, a)
    rng = random.Random(seed)
    for k in range(leaf_n):
        ang = rng.uniform(0, 6.28); d = rng.random() ** 0.6
        lx = x + math.cos(ang) * d * h * 0.42; ly = y - h * 0.72 + math.sin(ang) * d * h * 0.28
        cl = mix(colr, "#ffffff" if k % 3 == 0 else "#0b3a10", 0.15 + 0.1 * (k % 2))
        leaf_rot(c, lx, ly, h * 0.09, rng.uniform(-60, 60) + math.sin(t + k) * 4, cl, a, vein=False)

def dna(c, x, y, w, h, t, a=1.0, cols=("#4d96ff", "#ff6b6b")):
    n = 40
    for i in range(n):
        f = i / (n - 1); xx = x - w / 2 + f * w
        ph = f * 4 * math.pi + t * 1.5
        y1 = y + math.sin(ph) * h / 2; y2 = y - math.sin(ph) * h / 2
        if i % 3 == 0: line(c, xx, y1, xx, y2, "#ffffff", max(2, h * 0.03), a * 0.7)
        circle(c, xx, y1, h * 0.06, cols[0], a); circle(c, xx, y2, h * 0.06, cols[1], a)

def slug(c, x, y, s, t, a=1.0, glow=0.0, body=1.0, head=True, colr="#4caf50", ang=0.0):
    """Leaf-shaped Elysia: head at +x. body 0..1 = how much of the body exists (regrowth)."""
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(ang)
    wv = math.sin(t * 2) * 0.03
    if body > 0.1:
        L = s * 1.15 * body; Wd = s * 0.42 * (0.5 + 0.5 * body)
        p = skia.Path(); p.moveTo(s * 0.32, 0)
        p.cubicTo(s * 0.2, -Wd * 1.2, -L * 0.5, -Wd * (1.1 + wv), -L * 0.82, -Wd * 0.1)
        p.quadTo(-L * 0.9, 0, -L * 0.82, Wd * 0.1)
        p.cubicTo(-L * 0.5, Wd * (1.1 - wv), s * 0.2, Wd * 1.2, s * 0.32, 0)
        c.drawPath(p, paint(mix(colr, "#ffffff", 0.25), a))
        c.save(); c.clipPath(p, doAntiAlias=True)
        oval(c, -L * 0.25, 0, L * 0.62, Wd * 0.82, colr, a)
        for k in range(7):
            fx = s * 0.15 - k * L * 0.14
            for sgn in (-1, 1):
                pp = skia.Path(); pp.moveTo(fx, 0); pp.quadTo(fx - L * 0.06, sgn * Wd * 0.4, fx - L * 0.16, sgn * Wd * 0.95)
                c.drawPath(pp, paint(mix(colr, "#0b3a10", 0.45), a * 0.8, stroke=max(1.5, s * 0.018)))
        line(c, s * 0.25, 0, -L * 0.8, 0, mix(colr, "#0b3a10", 0.5), max(2, s * 0.03), a)
        if glow > 0:
            rng = random.Random(9)
            for k in range(40):
                gx = rng.uniform(-L * 0.75, s * 0.1); gy = rng.uniform(-1, 1) * Wd * 0.75 * (1 - abs(gx + L * 0.3) / (L * 0.9))
                circle(c, gx, gy, s * 0.028, "#c8ff7a", a * glow * (0.6 + 0.4 * math.sin(t * 3 + k)))
        c.restore()
    if head:
        oval(c, s * 0.42, 0, s * 0.16, s * 0.11, colr, a)
        for sgn in (-1, 1):
            p = skia.Path(); p.moveTo(s * 0.5, sgn * s * 0.05); p.quadTo(s * 0.62, sgn * s * 0.12, s * 0.6, sgn * s * 0.2)
            c.drawPath(p, paint(colr, a, stroke=s * 0.045))
        circle(c, s * 0.5, -s * 0.03, s * 0.015, "#0b1030", a); circle(c, s * 0.5, s * 0.03, s * 0.015, "#0b1030", a)
    c.restore()

def algae_strands(c, x, y, w, h, t, a=1.0, eaten=0.0):
    rng = random.Random(4)
    for k in range(14):
        sx = x - w / 2 + rng.random() * w * (1 - eaten * 0.8) + w * eaten * 0.8
        p = skia.Path(); p.moveTo(sx, y)
        for j in range(1, 6):
            p.lineTo(sx + math.sin(t * 1.2 + k + j) * 12, y - h * j / 5 * rng.uniform(0.6, 1))
        c.drawPath(p, paint(mix("#2f8f3a", "#7fd36a", rng.random()), a, stroke=5))

CLR = ["#2ec4b6", "#ff6b6b", "#ffd166", "#4d96ff", "#9b5de5", "#7ee081"]

def mantis(c, x, y, s, t, a=1.0, strike=0.0, eye_t=None):
    """Side view, head at left. strike 0..1 extends the club."""
    if a <= 0: return
    c.save(); c.translate(x, y)
    # tail fan
    for k in range(5):
        ang = math.radians(-40 + k * 20)
        c.save(); c.translate(s * 0.95, -s * 0.02); c.rotate(math.degrees(ang) * 0.6)
        oval(c, s * 0.14, 0, s * 0.16, s * 0.05, CLR[k % 6], a); c.restore()
    oval(c, s * 0.25, 0, s * 0.72, s * 0.18, "#13706a", a)
    for k in range(8):
        xx = s * (0.82 - k * 0.15); hh = s * (0.3 + 0.018 * k)
        line(c, xx - s * 0.02, hh * 0.45, xx - s * 0.06, hh * 0.45 + s * 0.12, mix(CLR[k % 6], "#000", 0.3), s * 0.025, a)
        rrect(c, xx - s * 0.1, -hh / 2, s * 0.17, hh, s * 0.07, CLR[k % 6], a)
        rrect(c, xx - s * 0.1, -hh / 2, s * 0.17, hh * 0.3, s * 0.07, "#ffffff", a * 0.18)
    oval(c, -s * 0.46, -s * 0.04, s * 0.24, s * 0.17, "#2ec4b6", a)
    oval(c, -s * 0.5, -s * 0.1, s * 0.14, s * 0.06, "#7ff0e0", a * 0.6)
    # antennae + scales
    for k, col_ in enumerate(("#ff9f1c", "#ffd166")):
        p = skia.Path(); p.moveTo(-s * 0.62, -s * 0.12)
        p.quadTo(-s * 0.95, -s * (0.45 + 0.1 * k) + math.sin(t * 2 + k) * s * 0.03, -s * (1.15 - 0.1 * k), -s * (0.3 + 0.2 * k))
        c.drawPath(p, paint(col_, a, stroke=s * 0.015))
    oval(c, -s * 0.8, -s * 0.2, s * 0.12, s * 0.035, "#ff6b6b", a)
    # eyes on stalks
    for k, base in enumerate((-0.55, -0.45)):
        ph = (eye_t if eye_t is not None else t) * (1.7 + k * 0.9) + k * 2
        ex = s * (base - 0.06 + 0.06 * math.sin(ph)); ey = -s * (0.42 + 0.04 * math.cos(ph * 1.3))
        line(c, s * base, -s * 0.18, ex, ey, "#2ec4b6", s * 0.04, a)
        eye(c, ex, ey, s * 0.085, ph * 20, a)
    # raptorial club
    ext = eout(strike)
    sx, sy = -s * 0.5, s * 0.08
    ex, ey = sx - s * (0.08 + 0.45 * ext), sy + s * (0.18 - 0.1 * ext)
    line(c, sx, sy, ex, ey, "#ff6b6b", s * 0.06, a)
    circle(c, ex, ey, s * 0.06, "#ff3d3d", a)
    for k in range(3): line(c, -s * (0.35 - k * 0.08), s * 0.1, -s * (0.38 - k * 0.08), s * 0.24, "#4d96ff", s * 0.025, a)
    c.restore()

def eye(c, x, y, r, ang, a=1.0):
    c.save(); c.translate(x, y); c.rotate(ang)
    oval(c, 0, 0, r, r * 0.8, "#3a4a5a", a)
    for k, col_ in enumerate(("#ffd166", "#ff6b6b", "#ffd166")):
        rect(c, -r * 0.95, (k - 1) * r * 0.16 - r * 0.06, r * 1.9, r * 0.12, col_, a)
    circle(c, -r * 0.3, -r * 0.35, r * 0.18, "#ffffff", a * 0.6)
    c.restore()

def snail(c, x, y, s, a=1.0, crack=0.0):
    circle(c, x, y, s, "#d9b48a", a)
    p = skia.Path(); p.moveTo(x, y)
    for k in range(40):
        an = k * 0.35; r = s * k / 40
        p.lineTo(x + math.cos(an) * r, y + math.sin(an) * r)
    c.drawPath(p, paint("#8a6a4a", a, stroke=s * 0.06))
    if crack > 0:
        for k in range(5):
            an = k * 1.25 + 0.3
            line(c, x - s * 0.9, y, x - s * 0.9 + math.cos(an) * s * 0.9 * crack, y + math.sin(an) * s * 0.9 * crack, "#3b2a1e", s * 0.05, a)

def lizard(c, x, y, s, t, a=1.0, colr="#7aa84a"):
    p = skia.Path(); p.moveTo(-s * 0.3, -s * 0.05); p.quadTo(-s * 1.0, -s * 0.0, -s * 1.3, s * 0.12 + math.sin(t) * s * 0.02)
    p.quadTo(-s * 0.9, s * 0.08, -s * 0.3, s * 0.07)
    c.drawPath(p, paint(colr, a))
    oval(c, x * 0, 0, s * 0.42, s * 0.11, colr, a)
    oval(c, s * 0.5, -s * 0.04, s * 0.16, s * 0.08, colr, a)
    for dx in (0.25, -0.2):
        for sgn in (1,):
            line(c, s * dx, s * 0.05, s * (dx + 0.08), s * 0.18, colr, s * 0.05, a)
            line(c, s * dx, s * 0.05, s * (dx - 0.08), s * 0.18, mix(colr, "#000", 0.2), s * 0.05, a)
    circle(c, s * 0.56, -s * 0.07, s * 0.02, "#0b1030", a)
    for k in range(6): circle(c, s * (0.3 - k * 0.12), -s * 0.04, s * 0.03, mix(colr, "#e8d26a", 0.6), a)

def lizard_at(c, x, y, s, t, a=1.0):
    c.save(); c.translate(x, y); lizard(c, 0, 0, s, t, a); c.restore()

def rock(c, x, y, w, h, a=1.0, colr="#b9a58a"):
    p = skia.Path(); p.moveTo(x - w / 2, y); p.cubicTo(x - w / 2, y - h, x - w * 0.1, y - h * 1.15, x + w * 0.2, y - h)
    p.cubicTo(x + w / 2, y - h * 0.9, x + w / 2, y - h * 0.2, x + w / 2, y); p.close()
    c.drawPath(p, paint(colr, a)); c.drawPath(p, paint(mix(colr, "#000", 0.3), a, stroke=3))

def rafflesia(c, x, y, s, t, a=1.0):
    for k in range(5):
        an = math.radians(-90 + k * 72)
        px, py = x + math.cos(an) * s * 0.55, y + math.sin(an) * s * 0.55
        circle(c, px, py, s * 0.42, "#c0392b", a)
        rng = random.Random(k)
        for j in range(7):
            circle(c, px + rng.uniform(-0.25, 0.25) * s, py + rng.uniform(-0.25, 0.25) * s, s * rng.uniform(0.03, 0.06), "#f6e3d0", a * 0.9)
    circle(c, x, y, s * 0.42, "#8e2a20", a)
    circle(c, x, y, s * 0.3, "#5a1a14", a)
    for k in range(12):
        an = k / 12 * 6.28; circle(c, x + math.cos(an) * s * 0.18, y + math.sin(an) * s * 0.18, s * 0.03, "#e8b9a0", a)

def coral_branch(c, x, y, h, colr, t, a=1.0, seed=1):
    rng = random.Random(seed)
    def br(x0, y0, ang, L, d):
        x1 = x0 + math.cos(ang) * L; y1 = y0 + math.sin(ang) * L
        line(c, x0, y0, x1, y1, colr, max(3, L * 0.22), a)
        if d == 0: circle(c, x1, y1, L * 0.16, mix(colr, "#ffffff", 0.3), a); return
        for s_ in (-1, 1): br(x1, y1, ang + s_ * rng.uniform(0.3, 0.6) + math.sin(t * 0.8 + seed) * 0.03, L * 0.72, d - 1)
    br(x, y, -math.pi / 2, h * 0.35, 3)

def fish(c, x, y, s, colr, a=1.0, flip=False):
    sg = -1 if flip else 1
    oval(c, x, y, s, s * 0.45, colr, a)
    c.drawPath(poly([(x - sg * s * 0.8, y), (x - sg * s * 1.4, y - s * 0.45), (x - sg * s * 1.4, y + s * 0.45)]), paint(colr, a))
    circle(c, x + sg * s * 0.5, y - s * 0.1, s * 0.09, "#0b1030", a)

def clam(c, x, y, s, t, a=1.0, glow=1.0):
    """Giant clam seen from the front-top: scalloped shell bowl with a glowing wavy mantle on top."""
    if glow > 0: circle(c, x, y - s * 0.15, s * 1.15, "#3fd3e0", a * 0.22 * glow, blur=s * 0.25)
    # shell bowl with ribs
    p = skia.Path(); p.moveTo(x - s, y - s * 0.15)
    for k in range(11):
        f = k / 10; xx = x - s + 2 * s * f
        p.quadTo(xx - s * 0.1, y - s * 0.3, xx, y - s * 0.15)
    p.cubicTo(x + s, y + s * 0.5, x - s, y + s * 0.5, x - s, y - s * 0.15); p.close()
    c.drawPath(p, paint("#e8e2d0", a))
    for k in range(1, 10):
        f = k / 10; xx = x - s + 2 * s * f
        line(c, xx, y - s * 0.12, lerp(xx, x, 0.55), y + s * 0.3, "#b9b09a", s * 0.02, a)
    # mantle
    m = skia.Path(); n = 40
    m.moveTo(x - s * 0.95, y - s * 0.12)
    for k in range(n + 1):
        f = k / n; m.lineTo(x - s * 0.95 + 1.9 * s * f, y - s * 0.32 - math.sin(f * 14 + t * 2) * s * 0.06 - math.sin(f * math.pi) * s * 0.12)
    for k in range(n + 1):
        f = 1 - k / n; m.lineTo(x - s * 0.95 + 1.9 * s * f, y - s * 0.1 + math.sin(f * 11 + t * 1.6) * s * 0.03)
    m.close()
    c.drawPath(m, paint(shader=lin(x - s, y, x + s, y, [(0, "#1b6fd1", 1), (0.5, "#2ec4b6", 1), (1, "#7b4dd1", 1)]), a=a))
    rng = random.Random(2)
    for k in range(30):
        f = rng.random()
        circle(c, x - s * 0.9 + 1.8 * s * f, y - s * (0.15 + rng.random() * 0.15) - math.sin(f * math.pi) * s * 0.08, s * 0.02, "#c8fff5", a * 0.85)
    line(c, x - s * 0.1, y - s * 0.21, x + s * 0.1, y - s * 0.21, "#0b3550", s * 0.03, a)

def hydra(c, x, y, h, t, a=1.0):
    col_ = "#5cbf55"
    p = skia.Path(); p.moveTo(x, y)
    p.cubicTo(x + math.sin(t) * h * 0.08, y - h * 0.3, x - math.sin(t) * h * 0.08, y - h * 0.6, x, y - h * 0.75)
    c.drawPath(p, paint(col_, a, stroke=h * 0.1))
    oval(c, x, y, h * 0.1, h * 0.04, col_, a)
    for k in range(6):
        ang = math.radians(-160 + k * 28)
        pp = skia.Path(); pp.moveTo(x, y - h * 0.75)
        pp.quadTo(x + math.cos(ang) * h * 0.25, y - h * 0.75 + math.sin(ang) * h * 0.3 - h * 0.05,
                  x + math.cos(ang) * h * 0.45 + math.sin(t * 1.5 + k) * h * 0.04, y - h * 0.75 + math.sin(ang) * h * 0.45 + h * 0.15)
        c.drawPath(pp, paint(col_, a, stroke=h * 0.03))
    rng = random.Random(3)
    for k in range(18):
        f = rng.random() * 0.7
        circle(c, x + math.sin(t + f * 3) * h * 0.02 + rng.uniform(-1, 1) * h * 0.03, y - h * f, h * 0.015, "#1f6a1f", a)

def upside_jelly(c, x, y, s, t, a=1.0):
    oval(c, x, y, s * 0.7, s * 0.14, "#d9c49a", a)  # bell flat on sand
    for k in range(8):
        ang = math.radians(-160 + k * 20)
        ex = x + math.cos(ang) * s * 0.6; ey = y + math.sin(ang) * s * 0.55 - s * 0.05
        line(c, x + math.cos(ang) * s * 0.15, y - s * 0.05, ex, ey, "#8a7a4a", s * 0.05, a)
        for j in range(4):
            circle(c, ex + math.sin(t * 2 + k + j) * s * 0.02 + (j - 1.5) * s * 0.05, ey - s * 0.04 * (j % 2), s * 0.07, mix("#7a8a3a", "#a7c25a", (j + k) % 3 / 2), a)

def calendar(c, x, y, s, n, a=1.0):
    rrect(c, x - s / 2, y - s / 2, s, s, s * 0.08, "#ffffff", a)
    rrect(c, x - s / 2, y - s / 2, s, s * 0.26, s * 0.08, "#e8443a", a)
    rect(c, x - s / 2, y - s / 2 + s * 0.15, s, s * 0.11, "#e8443a", a)
    text(c, "MONTH", x, y - s * 0.37, s * 0.13, "#ffffff", a, w=800)
    text(c, str(n), x, y + s * 0.12, s * 0.5, NAVY, a, w=900)

def drop(c, x, y, s, a=1.0, colr="#4da3ff"):
    p = skia.Path(); p.moveTo(x, y - s); p.cubicTo(x + s * 0.8, y - s * 0.1, x + s * 0.6, y + s * 0.6, x, y + s * 0.6)
    p.cubicTo(x - s * 0.6, y + s * 0.6, x - s * 0.8, y - s * 0.1, x, y - s); c.drawPath(p, paint(colr, a))

def sugar_cube(c, x, y, s, a=1.0):
    c.drawPath(poly([(x - s * 0.5, y - s * 0.2), (x, y - s * 0.45), (x + s * 0.5, y - s * 0.2), (x, y + 0.05 * s)]), paint("#ffffff", a))
    c.drawPath(poly([(x - s * 0.5, y - s * 0.2), (x, y + 0.05 * s), (x, y + s * 0.55), (x - s * 0.5, y + s * 0.3)]), paint("#e6e9f0", a))
    c.drawPath(poly([(x + s * 0.5, y - s * 0.2), (x, y + 0.05 * s), (x, y + s * 0.55), (x + s * 0.5, y + s * 0.3)]), paint("#cfd5e2", a))

def co2(c, x, y, s, a=1.0):
    circle(c, x, y, s * 0.35, "#4a4a4a", a); circle(c, x - s * 0.55, y, s * 0.28, "#ff6b6b", a); circle(c, x + s * 0.55, y, s * 0.28, "#ff6b6b", a)

def house(c, x, y, s, a=1.0, door=0.0):
    rect(c, x - s * 0.5, y - s * 0.65, s, s * 0.65, "#f2e6cf", a)
    c.drawPath(poly([(x - s * 0.62, y - s * 0.62), (x, y - s * 1.05), (x + s * 0.62, y - s * 0.62)]), paint("#c9653a", a))
    rect(c, x + s * 0.05, y - s * 0.4, s * 0.22, s * 0.4, "#3a2a1e", a)
    rect(c, x + s * 0.05, y - s * 0.4, s * 0.22 * (1 - 0.8 * door), s * 0.4, "#8a5a3a", a)
    rect(c, x - s * 0.35, y - s * 0.45, s * 0.22, s * 0.18, "#9fd3ff", a)

def donut2(c, x, y, r, frac, colr, label, sub=None, a=1.0, ink=NAVY):
    if a <= 0: return
    c.drawCircle(x, y, r, paint(ink, 0.12 * a, stroke=r * 0.28))
    p = skia.Path(); p.addArc(skia.Rect.MakeXYWH(x - r, y - r, 2 * r, 2 * r), -90, 360 * clamp(frac))
    c.drawPath(p, paint(colr, a, stroke=r * 0.28, cap="butt"))
    text(c, label, x, y - (r * 0.1 if sub else 0), r * 0.42, ink, a, w=900)
    if sub: text(c, sub, x, y + r * 0.3, r * 0.15, ink, a * 0.85, w=800, fam="Inter")

def bar_h(c, x, y, w, h, frac, colr, label, val, a=1.0, size=None):
    size = size or h * 0.8
    rrect(c, x, y - h / 2, w, h, h / 2, "#0b1030", 0.18 * a)
    if frac > 0: rrect(c, x, y - h / 2, max(h, w * clamp(frac)), h, h / 2, colr, a)
    text(c, label, x, y - h * 1.05, size * 0.75, NAVY, a, w=800, fam="Inter", align="l")
    if val: text(c, val, x + max(h, w * clamp(frac)) + 18, y, size, NAVY, a, w=900, align="l")

# ---------------------------------------------------------------- kit wrappers
def bg_photo(c, W, H, t, S):
    fill_bg(c, W, H, "#0b2410", "#1f5a26")
    c.drawPaint(paint(shader=rad(W * 0.78, H * 0.15, max(W, H) * 0.7, [(0, "#ffd166", 0.35), (0.5, "#ffd166", 0.06), (1, "#ffd166", 0)])))
    rng = random.Random(8)
    for k in range(14):
        x = (rng.random() * W + t * 18 * (1 + k % 3)) % (W + 100) - 50
        y = (rng.random() * H + t * 12 + math.sin(t + k) * 20) % (H + 100) - 50
        leaf_rot(c, x, y, 26 * S.u * (0.7 + 0.6 * rng.random()), rng.uniform(0, 360) + t * 20 * (1 if k % 2 else -1),
                 mix(LEAF, "#0b2410", 0.35), 0.5, vein=False)

def motif_photo(c, W, H, t, S, cx, cy, s):
    u = S.u * s
    for i in range(16):
        an = math.radians(i * 22.5 + t * 6)
        r0, r1 = 230 * u, (420 + 30 * math.sin(t * 2 + i)) * u
        c.drawPath(poly([(cx + math.cos(an - 0.06) * r0, cy - 40 * u + math.sin(an - 0.06) * r0), (cx + math.cos(an) * r1, cy - 40 * u + math.sin(an) * r1),
                         (cx + math.cos(an + 0.06) * r0, cy - 40 * u + math.sin(an + 0.06) * r0)]), paint("#ffd166", 0.3))
    circle(c, cx, cy - 40 * u, 250 * u, "#ffd166", 0.22)
    figure(c, cx, cy + 230 * u, 470 * u, GSKIN, 1, flat=0.25, leaves=1, arms=0.55 + 0.05 * math.sin(t * 1.5), t=t)

def p_title(c, W, H, t, S): kit.title(c, W, H, t, S, bg_photo, motif_photo, PAL)
def p_card(c, W, H, t, S): kit.card(c, W, H, t, S, bg_photo, PAL)
def p_end(c, W, H, t, S): kit.end(c, W, H, t, S, bg_photo, motif_photo, PAL)
def p_endshort(c, W, H, t, S): kit.end_short(c, W, H, t, S, bg_photo, motif_photo, PAL)

# ---------------------------------------------------------------- scenes
def pond_bg(c, W, H, t):
    fill_bg(c, W, H, "#3c8f78", "#173f37")
    rng = random.Random(6)
    for k in range(9):
        x, y = rng.random() * W, rng.random() * H; r = rng.uniform(50, 110) * min(W, H) / 1080
        p = skia.Path(); p.addArc(skia.Rect.MakeXYWH(x - r, y - r, 2 * r, 2 * r), 20 + k * 30, 320); p.lineTo(x, y); p.close()
        c.drawPath(p, paint("#4f9f4a", 0.85))
    for k in range(5):
        q = (t * 0.2 + k / 5) % 1
        circle(c, rng.random() * W, rng.random() * H, 200 * q, "#ffffff", 0.2 * (1 - q), stroke=3)

def p_salamander(c, W, H, t, S):
    o = S.opts
    if o.get("mode") == "hatch": return _sal_hatch(c, W, H, t, S)
    B = beats(S, 3)
    pa = phase(t, None, B(1, 0))
    with Layer(c, pa) as on:
        if on:
            pond_bg(c, W, H, t)
            with stage(c, S):
                ang = math.sin(t * 0.3) * 10
                salamander(c, -60 + math.sin(t * 0.4) * 60, 30, 330, t, ang)
                rng = random.Random(1)
                for k in range(18):
                    egg(c, 330 + rng.uniform(-90, 90), -150 + rng.uniform(-60, 60), 34, 0.7, 0.9, t=t)
                ch(c, S, "SPOTTED SALAMANDER", 0, -270, vis(t, B(0, 0.5)), dot="#ffcf3a")
                ch(c, S, "ALGAE INSIDE ITS CELLS", 0, 260, vis(t, B(0, 0.1)), bg="#16401c", dot=LIME)
    pb = phase(t, B(1, 0), B(2, 0))
    with Layer(c, pb) as on:
        if on:
            pond_bg(c, W, H, t)
            c.drawPaint(paint("#0b2410", 0.35))
            with stage(c, S):
                z = 1 + 0.08 * prog(t, B(1, 0), 6)
                c.save(); c.scale(z, z)
                egg(c, 0, 10, 250, 0.6, 1, embryo=False)
                circle(c, 0, 10, 130, "#efe0b8")
                rng = random.Random(3)
                cells = [(rng.uniform(-100, 100), rng.uniform(-90, 110)) for _ in range(40)]
                cells = [(x, y) for x, y in cells if x * x + (y - 10) ** 2 < 105 ** 2][:22]
                for (x, y) in cells: circle(c, x, y, 18, "#e2cf9e"); c.drawCircle(x, y, 18, paint("#c9a86b", 1, stroke=2))
                q = prog(t, B(1, 0.35), 3.0)
                for k in range(26):
                    an = k * 2.4 + t * 0.3; r = 200 + 20 * math.sin(t + k)
                    ax, ay = math.cos(an) * r, 10 + math.sin(an) * r * 0.9
                    if k < len(cells) and k % 2 == 0:
                        tx, ty = cells[k]; ax, ay = lerp(ax, tx, eout(q)), lerp(ay, ty, eout(q))
                    circle(c, ax, ay, 9, "#2f9a32"); circle(c, ax - 2, ay - 2, 3, "#a8f08a")
                c.restore()
                ch(c, S, "GREEN ALGAE IN THE JELLY", 0, -275, vis(t, B(1, 0.05), B(1, 0.45)), bg="#16401c", dot=LIME)
                ch(c, S, "…AND INSIDE THE EMBRYO'S CELLS", 0, -275, vis(t, B(1, 0.5)), bg="#16401c", dot=LIME)
    pc = phase(t, B(2, 0))
    with Layer(c, pc) as on:
        if on:
            day_bg(c, W, H)
            with stage(c, S):
                sunball(c, 300, -170, 70, t)
                q = prog(t, B(2, 0.3), 2.0)
                figure(c, -40, 280, 500, mix(SKIN, GSKIN, ease(q)), 1, leaves=q, arms=0.15)
                big(c, "?", 220, 40, 220, LIME, prog(t, B(2, 0.5), 0.4))
                ch(c, S, "FOOD FROM SUNLIGHT?", 0, -275, vis(t, B(2, 0.55)))

def _sal_hatch(c, W, H, t, S):
    B = beats(S, 2)
    pond_bg(c, W, H, t)
    c.drawPaint(paint("#0b2410", 0.25))
    with stage(c, S):
        q = prog(t, B(0, 0.45), 2.5)
        egg(c, -220, 0, 190, 0.6 * (1 - q * 0.6), 1, embryo=False)
        circle(c, -220, 0, 85, "#efe0b8")
        for k in range(12):
            an = k * 0.52 + t * 0.4
            circle(c, -220 + math.cos(an) * 140, math.sin(an) * 140, 9, "#2f9a32", 1 - q * 0.3)
        a1 = vis(t, B(0, 0.05))
        arrow(c, -120, -60, -30, -60, "#7fd3ff", 8, a1); text(c, "O₂", 0, -60, 44, "#ffffff", a1, w=900, align="l")
        arrow(c, -30, 60, -120, 60, "#d9b48a", 8, a1); text(c, "WASTE", 0, 60, 36, "#ffffff", a1, w=900, align="l")
        larva(c, lerp(170, 260, q), 0, 230 * (0.6 + 0.4 * q), t, q)
        rng = random.Random(4)
        for k in range(14):
            circle(c, lerp(150, 250, q) + rng.uniform(-90, 60), rng.uniform(-20, 20), 6, "#2f9a32", q * (1 - prog(t, B(0, 0.8), 2)))
        ch(c, S, "HATCH EARLIER & BIGGER", 0, -270, vis(t, B(0, 0.6), B(1, 0)), dot=LIME)
        ch(c, S, "A HEAD START, NOT A MEAL PLAN", 0, -270, vis(t, B(1, 0.05)), bg="#16401c", dot=LIME)

def p_rules(c, W, H, t, S):
    B = beats(S, 3)
    pa = phase(t, None, B(1, 0))
    with Layer(c, pa) as on:
        if on:
            day_bg(c, W, H)
            with stage(c, S):
                q = prog(t, B(0, 0.1), 3)
                rrect(c, -460, -200, 520, 400, 40, mix(SKIN, "#e7c3a0", 0.3))
                rng = random.Random(2)
                for k in range(int(70 * q)):
                    chloroplast(c, -440 + rng.random() * 480, -180 + rng.random() * 360, 22, rng.uniform(0, 180), 1)
                circle(c, 250, -20, 190, "#ffffff", 0.95); c.drawCircle(250, -20, 190, paint(NAVY, 1, stroke=10))
                line(c, 380, 115, 470, 210, NAVY, 26)
                c.save(); pth = skia.Path(); pth.addCircle(250, -20, 182); c.clipPath(pth, doAntiAlias=True)
                rect(c, 60, -210, 380, 380, "#e9f7dc")
                chloroplast(c, 250, -20, 120, 20 + t * 5, 1)
                c.restore()
                ch(c, S, "CHLOROPLASTS", 250, -255, vis(t, B(0, 0.25)), dot=LIME)
                ch(c, S, "~500,000 PER MM² OF LEAF", 0, 265, vis(t, B(0, 0.65)), bg="#16401c")
    pb = phase(t, B(1, 0), B(2, 0))
    with Layer(c, pb) as on:
        if on:
            day_bg(c, W, H, "#fff7d6", "#bfe6a0")
            with stage(c, S):
                items = [(-430, "sun"), (-300, "+"), (-190, "drop"), (-75, "+"), (70, "co2"), (225, "→"), (390, "sugar")]
                for k, (x, it) in enumerate(items):
                    p = prog(t, B(1, 0.02 + k * 0.05), 0.35); s_ = eback(p)
                    if p <= 0: continue
                    if it == "sun": sunball(c, x, -40, 55 * s_, t)
                    elif it == "drop": drop(c, x, -40, 70 * s_)
                    elif it == "co2": co2(c, x, -40, 90 * s_)
                    elif it == "sugar": sugar_cube(c, x, -40, 150 * s_)
                    else: big(c, it, x, -40, 90, NAVY if it == "+" else "#2f8f3a", p)
                for x, lab in ((-430, "SUNLIGHT"), (-190, "WATER"), (70, "CO₂"), (390, "SUGAR")):
                    text(c, lab, x, 80, 34, NAVY, prog(t, B(1, 0.3), 0.4), w=800, fam="Inter")
                ch(c, S, "YOU STILL EAT NORMALLY", 0, 200, vis(t, B(1, 0.45)), dot="#ffd166")
                ch(c, S, "SUNLIGHT = BONUS", 0, -250, vis(t, B(1, 0.55)), bg="#16401c", dot=LIME)
    pc = phase(t, B(2, 0))
    with Layer(c, pc) as on:
        if on:
            fill_bg(c, W, H, "#1f6a6a", "#0c3a3f")
            with stage(c, S):
                q = prog(t, B(2, 0.05), 3.5)
                circle(c, 0, 0, 240, "#cfe9d0", 0.85); c.drawCircle(0, 0, 240, paint("#ffffff", 0.8, stroke=8))
                circle(c, -70, -40, 70, "#9a7ac9", 0.8)  # nucleus
                bx = lerp(520, 90, eout(q)); by = lerp(-40, 60, eout(q))
                if q < 0.75:
                    c.save(); c.translate(bx, by); c.rotate(t * 20)
                    rrect(c, -70, -26, 140, 52, 26, "#2a9d8f"); line(c, -50, 0, 50, 0, "#1b5f57", 6); c.restore()
                cpa = prog(t, B(2, 0.05) + 3.5 * 0.7, 0.6)
                chloroplast(c, 90, 60, 70, 10, cpa)
                pd = prog(t, B(2, 0.42), 0.5) * cpa
                if pd > 0:
                    c.drawCircle(90, 60, 30 + 3 * math.sin(t * 3), paint("#ff6b6b", pd, stroke=7))
                    c.drawCircle(90, 60, 30 + 3 * math.sin(t * 3), paint("#ffd166", pd, stroke=3, dash=([10, 8], t * 20)))
                ch(c, S, "A CELL SWALLOWS A BACTERIUM", 0, -275, vis(t, B(2, 0.05), B(2, 0.55)), dot="#2a9d8f")
                ch(c, S, "1+ BILLION YEARS AGO", 0, -275, vis(t, B(2, 0.6)), bg="#16401c", dot=LIME)
                ch(c, S, "= CHLOROPLAST", 0, 280, vis(t, B(2, 0.3), B(2, 0.42)), dot=LIME)
                ch(c, S, "IT STILL CARRIES ITS OWN DNA", 0, 280, vis(t, B(2, 0.45)), dot="#ff6b6b")

def p_oxygen(c, W, H, t, S):
    B = beats(S, 2)
    q = prog(t, B(0, 0.2), 6)
    sky_t = mix("#e08a4a", "#7fc4ff", q); sky_b = mix("#f2b77a", "#d6efff", q)
    fill_bg(c, W, H, sky_t, sky_b)
    hy = (0.47 if S.P else 0.45) * H
    c.drawRect(skia.Rect.MakeLTRB(0, hy, W, H), paint(shader=lin(0, hy, 0, H, [(0, "#2a8fb0", 1), (1, "#0b3550", 1)])))
    u = min(W, H) / 1080
    sun(c, W * 0.85, hy * 0.35, 60 * u, t, glow=0.7)
    pa_ = 1 - prog(t, B(1, 0), 0.6)
    for k in range(7):
        x = W * (0.07 + k * 0.145); r = (90 + 30 * (k % 3)) * u
        p = skia.Path(); p.addArc(skia.Rect.MakeXYWH(x - r, H - r * 0.9, 2 * r, 2 * r), 180, 180); p.close()
        c.drawPath(p, paint("#4f7a3a", pa_))
        for j in range(3): c.drawArc(skia.Rect.MakeXYWH(x - r * (0.8 - j * 0.2), H - r * 0.9 + r * (0.2 + j * 0.2), 2 * r * (0.8 - j * 0.2), 2 * r), 180, 180, False, paint("#7fae5a", pa_, stroke=4 * u))
    rng = random.Random(5)
    for k in range(60):
        x = rng.random() * W; y0 = hy + rng.random() * (H - hy)
        circle(c, x + math.sin(t + k) * 6, y0, 5 * u, "#7fd36a", 0.9)
        qq = (t * 0.25 + rng.random()) % 1
        by = y0 - qq * (y0 - hy) * 1.0
        circle(c, x + math.sin(t * 2 + k) * 8, by, (5 + 5 * qq) * u, "#ffffff", 0.6 * (1 - qq), stroke=2.5 * u)
    pb = phase(t, B(1, 0))
    if pb > 0:
        rng = random.Random(7)
        for k in range(26):
            x = (rng.random() * W + t * 15) % W; y = hy + 40 * u + rng.random() * (H - hy - 80 * u)
            c.save(); c.translate(x, y); c.rotate(t * 20 + k * 30)
            r = (14 + rng.random() * 14) * u
            c.drawPath(poly([(math.cos(a_ / 3 * 6.28) * r, math.sin(a_ / 3 * 6.28) * r) for a_ in range(3)]) if k % 3 == 0 else poly([(math.cos(a_ / 8 * 6.28) * r, math.sin(a_ / 8 * 6.28) * r * 0.5) for a_ in range(8)]),
                       paint("#c8ff7a", pb * 0.9))
            c.restore()
    with stage(c, S):
        big(c, "O₂", -330, -150, 120, "#ffffff", vis(t, B(0, 0.4)))
        ch(c, S, "2.4 BILLION YEARS AGO", 0, -270, vis(t, B(0, 0.25), B(1, 0)), dot="#ffd166")
        ch(c, S, "PLANKTON: ~HALF OF EARTH'S OXYGEN", 0, -270, vis(t, B(1, 0.1)), bg="#0b4f6a", dot=LIME)
        ch(c, S, "EVERY BREATH: EXHAUST FROM SUNLIGHT", 0, 265, vis(t, B(1, 0.6)), bg="#16401c", dot="#ffd166")

def beam(c, x0, y0, x1, y1, colr, w, p, a=1.0):
    if p <= 0: return
    xe, ye = lerp(x0, x1, p), lerp(y0, y1, p)
    line(c, x0, y0, xe, ye, colr, w, a * 0.9)
    circle(c, xe, ye, w * 0.9, colr, a * 0.5)

def p_green(c, W, H, t, S):
    o = S.opts
    full = o.get("full") or S.n() >= 2
    B = beats(S, 2) if S.n() >= 2 else (lambda i, f=0.0: S.lt(0, (i + f) / 2))
    day_bg(c, W, H)
    with stage(c, S):
        sx, sy = -400, -200
        sunball(c, sx, sy, 60, t)
        if full and not o.get("hook"):
            q = prog(t, B(0, 0.2), 2.5)
            skin = mix(SKIN, GSKIN, ease(prog(t, B(0, 0.0), 1.5)))
            figure(c, 0, 290, 520, skin, 1, leaves=0.6)
            for k, (colr, dy) in enumerate((("#ff4d4d", -40), ("#3fd14a", 0), ("#4d7dff", 40))):
                beam(c, sx + 40, sy + 30 + dy * 0.3, -20, -20 + dy, colr, 12, prog(t, B(0, 0.1 + k * 0.05), 0.8))
            pr = vis(t, B(0, 0.5))
            for k, colr in enumerate(("#ff4d4d", "#4d7dff")):
                circle(c, -20, -60 + k * 80, 26 + 6 * math.sin(t * 6 + k), colr, 0.5 * pr)
            pg = prog(t, B(0.0, 0.0) if S.n() < 2 else B(1, 0.0), 0.9)
            beam(c, -20, -20, 330, -60, "#3fd14a", 14, pg)
            # eye
            ea = clamp(pg * 2)
            oval(c, 370, -60, 70, 40, "#ffffff", ea); circle(c, 370, -60, 26, "#3a7a3a", ea); circle(c, 370, -60, 12, NAVY, ea)
            c.drawOval(skia.Rect.MakeLTRB(300, -100, 440, -20), paint(NAVY, ea, stroke=6))
            ch(c, S, "RED + BLUE: ABSORBED", -230, 250, vis(t, B(0, 0.45)), dot="#ff4d4d")
            ch(c, S, "GREEN: BOUNCES BACK", 240, 60, vis(t, B(1, 0.05) if S.n() >= 2 else B(1, 0.0)), bg="#16401c", dot="#3fd14a")
        else:
            q = prog(t, 0.3, max(1.0, S.dur - 0.8))
            for i in range(10):
                an = math.radians(150 + i * 6)
                line(c, sx, sy, sx + math.cos(an + math.pi) * -900, sy - math.sin(an + math.pi) * -900, "#ffd166", 10, 0.25)
            figure(c, 60, 290, 520, mix(SKIN, GSKIN, ease(q)), 1, leaves=q, arms=0.6 * q)
            for k in range(8):
                an = k * 0.8 + t; r = 300 + 20 * math.sin(t * 2 + k)
                leaf_rot(c, 60 + math.cos(an) * r, 0 + math.sin(an) * r * 0.6, 26, an * 50, LEAF, q * 0.9, vein=False)
    kit.hook(c, W, H, t, S)

def p_morning(c, W, H, t, S):
    B = beats(S, 2)
    pa = phase(t, None, B(1, 0))
    with Layer(c, pa) as on:
        if on:
            q = prog(t, 0, B(1, 0))
            fill_bg(c, W, H, mix("#ffb37a", "#8fd0ff", q), mix("#ffe0b0", "#e9f7ff", q))
            cx_, cy_, k_ = box(S); gy = cy_ + 250 * k_
            hills(c, W, gy, 40 * k_, "#9fd38a", 2, H=H); rect(c, 0, gy, W, H - gy, "#6fae5a")
            with stage(c, S):
                sunball(c, 300, lerp(220, 60, ease(q)), 60, t)
                house(c, -300, 250, 260, door=prog(t, B(0, 0.1), 0.5))
                px = lerp(-245, -60, ease(prog(t, B(0, 0.15), 1.6)))
                figure(c, px, 250, 230, mix(GSKIN, "#7fd36a", 0.2), 1, leaves=0.5)
                bar_h(c, 60, -170, 400, 50, prog(t, B(0, 0.5), 5) * 0.35, "#ffb300", "SUGAR MADE TODAY", None, size=52)
                ch(c, S, "7 A.M.", -380, -260, 1, dot="#ffd166")
    pb = phase(t, B(1, 0))
    with Layer(c, pb) as on:
        if on:
            day_bg(c, W, H, "#fff7d6", "#cfeeb5")
            with stage(c, S):
                x0, x1, yb = -420, 420, 170
                line(c, x0, yb, x1, yb, NAVY, 5)
                p = skia.Path(); n = 60; q = prog(t, B(1, 0.0), 2.5)
                p.moveTo(x0, yb)
                for i in range(n + 1):
                    f = i / n
                    if f > q: break
                    p.lineTo(lerp(x0, x1, f), yb - 340 * math.sin(math.pi * f) ** 2)
                c.drawPath(p, paint("#ff9f1c", 1, stroke=10))
                for f, lab in ((0.0, "DAWN"), (0.5, "NOON"), (1.0, "DUSK")):
                    text(c, lab, lerp(x0, x1, f), yb + 40, 32, NAVY, 1, w=800, fam="Inter")
                sunball(c, 0, yb - 390, 34, t, a=prog(t, B(1, 0.1), 0.5))
                po = prog(t, B(1, 0.48), 0.6)
                if po > 0:
                    p2 = skia.Path(); p2.moveTo(x0, yb)
                    for i in range(n + 1):
                        f = i / n; p2.lineTo(lerp(x0, x1, f), yb - 340 * 0.3 * math.sin(math.pi * f) ** 2)
                    c.drawPath(p2, paint("#7a8aa0", po, stroke=9, dash=([22, 14], 0)))
                    cloud(c, lerp(-200, -20, eout(po)), yb - 385, 70, "#9aa4b8", po)
                    text(c, "OVERCAST", 300, yb - 120, 34, "#5a6a80", po, w=900)
                ch(c, S, "MOST SUGAR AROUND NOON", -280, -260, vis(t, B(1, 0.05)), dot="#ff9f1c")
                ch(c, S, "DAWN + DUSK: ALMOST NOTHING", 0, 275, vis(t, B(1, 0.3), B(1, 0.48)), bg="#16401c")
                ch(c, S, "GRAY DAY: A FRACTION OF THE HAUL", 0, 275, vis(t, B(1, 0.5)), bg="#3a4a60", dot="#dfe7ef")

def p_math(c, W, H, t, S):
    long_ = S.n() >= 3
    B = beats(S, 3) if long_ else beats(S, 2)
    pa = phase(t, None, B(1, 0))
    with Layer(c, pa) as on:
        if on:
            day_bg(c, W, H, "#fff4c8", "#cdeeb0")
            with stage(c, S):
                for i in range(7):
                    xx = -330 + (i - 3) * 40
                    line(c, xx + 120, -300, xx, -130, "#ffb300", 8, 0.7)
                c.save(); c.translate(-300, 20)
                c.skew(-0.4, 0); rect(c, -110, -110, 220, 220, "#ffe08a"); c.drawRect(skia.Rect.MakeXYWH(-110, -110, 220, 220), paint(NAVY, 1, stroke=6)); c.restore()
                big(c, "1,000 W", -300, 190, 72, "#ff9f1c", vis(t, B(0, 0.15)))
                text(c, "PER SQUARE METER", -300, 250, 30, NAVY, vis(t, B(0, 0.2)), w=800, fam="Inter")
                if long_:
                    pp = vis(t, B(0, 0.5))
                    figure(c, 250, 220, 420, GSKIN, pp, leaves=0.5)
                    c.save(); c.clipRect(skia.Rect.MakeLTRB(250, -300, 600, 300)); figure(c, 250, 220, 420, "#2e6b2a", pp * 0.85); c.restore()
                    ch(c, S, "1.8 M² SKIN · HALF LIT", 250, -270, pp, bg="#16401c", dot=LIME)
    pb = phase(t, B(1, 0), B(2, 0) if long_ else None)
    with Layer(c, pb) as on:
        if on:
            day_bg(c, W, H, "#fff4c8", "#cdeeb0")
            with stage(c, S):
                rows = [("THEORETICAL MAX", 0.06, "~6%", "#7fd36a"), ("BEST CROPS", 0.03, "2–3%", "#3fae4a"), ("TYPICAL PLANT", 0.01, "~1%", "#25732f")] if long_ else \
                       [("SUNLIGHT", 1.0, "100%", "#ffb300"), ("STORED BY PLANTS", 0.01, "~1%", "#25732f")]
                for k, (lab, fr, val, colr) in enumerate(rows):
                    p = prog(t, B(1, 0.08 + k * 0.22), 0.6)
                    y = -170 + k * 160
                    bar_h(c, -420, y, 640, 56, (fr / 0.06 if long_ else fr) * eout(p) * (0.9 if long_ else 1.0), colr, lab, val if p > 0.3 else None, a=clamp(p * 3), size=52)
                ch(c, S, "OF SUNLIGHT STORED AS FOOD", 0, -280, vis(t, B(1, 0.03)), dot="#ffd166")
    if long_:
        pc = phase(t, B(2, 0))
        with Layer(c, pc) as on:
            if on:
                fill_bg(c, W, H, "#16401c", "#0b2410")
                with stage(c, S):
                    for k in range(5):
                        x = -400 + k * 200; p = prog(t, B(2, 0.05 + k * 0.08), 0.4)
                        if k < 2: sunball(c, x, -150, 40 + 15 * k, t, a=p)
                        elif k == 2: cloud(c, x, -150, 60, "#dfe7ef", p)
                        else: moon(c, x, -150, 40, 0.8, p)
                    sh_ = eout(prog(t, B(2, 0.78), 0.6)) * 170
                    big(c, "≈ 1–2 W", -sh_, 80, 170, LIME, vis(t, B(2, 0.55)))
                    text(c, "AVERAGED OVER A DAY", -sh_, 210, 38, "#ffffff", vis(t, B(2, 0.6)), w=800, fam="Inter")
                    pc_ = vis(t, B(2, 0.8))
                    if pc_ > 0:
                        big(c, "<", 230, 80, 120, "#ffffff", pc_)
                        cx2 = 390
                        rrect(c, cx2 - 60, 20, 120, 130, 22, "#f4f4f4", pc_)
                        for dx in (-25, 25): rect(c, cx2 + dx - 7, -15, 14, 38, "#9aa4b8", pc_)
                        p3 = skia.Path(); p3.moveTo(cx2, 150); p3.cubicTo(cx2, 220, cx2 + 100, 200, cx2 + 110, 260)
                        c.drawPath(p3, paint("#f4f4f4", pc_, stroke=12))
                        text(c, "PHONE CHARGER", cx2, 290, 30, "#ffffff", pc_, w=900)

def p_tennis(c, W, H, t, S):
    long_ = S.n() >= 3
    B = beats(S, 3)
    pa = phase(t, None, B(1, 0))
    with Layer(c, pa) as on:
        if on:
            fill_bg(c, W, H, "#16401c", "#0b2410")
            with stage(c, S):
                bulb(c, -230, 0, 190, 1.0)
                bulb(c, 260, 60, 70, 0.25 * vis(t, B(0, 0.4)), a=vis(t, B(0, 0.3)))
                big(c, "100 W", -230, 230, 70, "#ffe58a", vis(t, B(0, 0.1)))
                text(c, "YOUR BODY", -230, 290, 30, "#ffffff", vis(t, B(0, 0.15)), w=800, fam="Inter")
                big(c, "1–2 W", 260, 230, 70, LIME, vis(t, B(0, 0.4)))
                text(c, "YOUR GREEN SKIN", 260, 290, 30, "#ffffff", vis(t, B(0, 0.45)), w=800, fam="Inter")
    pb = phase(t, B(1, 0), B(2, 0))
    with Layer(c, pb) as on:
        if on:
            day_bg(c, W, H, "#fff4c8", "#cdeeb0")
            with stage(c, S):
                donut2(c, -260, -10, 150, 0.01 * eout(prog(t, B(1, 0.1), 0.6)) + 0.004, "#25732f", "~1%")
                text(c, "OF DAILY ENERGY", -260, 200, 34, NAVY, 1, w=800, fam="Inter")
                p = eback(prog(t, B(1, 0.55), 0.5))
                cracker(c, 260, -10, 190 * p, ang=8)
                ch(c, S, "≈ A CRACKER A DAY", 260, 200, vis(t, B(1, 0.6)), bg="#16401c", dot="#e6b85c")
                ch(c, S, "ESTIMATE: LINDSAY TURNBULL, OXFORD", 0, -270, vis(t, B(1, 0.1)), dot=LIME)
    pc = phase(t, B(2, 0))
    with Layer(c, pc) as on:
        if on:
            day_bg(c, W, H, "#dff3cf", "#9fd38a")
            with stage(c, S):
                z = lerp(2.2, 1.0, eout(prog(t, B(2, 0.0), 2.2)))
                c.save(); c.scale(z, z)
                court(c, 0, 10, 820)
                figure(c, -170, 40, 62, "#ffd166", 1)
                c.restore()
                ch(c, S, "A TENNIS COURT OF SKIN", 0, -270, vis(t, B(2, 0.1)), dot=LIME)
                ch(c, S, "~150× THE SKIN YOU HAVE", 0, 265, vis(t, B(2, 0.55)), bg="#16401c", dot="#ffd166")

def p_leaf(c, W, H, t, S):
    B = beats(S, 3)
    day_bg(c, W, H, "#e3f6ff", "#bfe6a0")
    ground(c, S, 270, "#6fae5a")
    with stage(c, S):
        tree_big(c, -150, 280, 560, t=t)
        figure(c, 300, 280, 200, GSKIN, 1, leaves=0.4)
        ch(c, S, "A HUGE, THIN SOLAR ARRAY", -150, -280, vis(t, B(0, 0.4), B(1, 0)), dot=LIME)
        icons = ["WALKING", "STAYING WARM", "A BRAIN"]
        for k, lab in enumerate(icons):
            p = vis(t, B(1, 0.1 + k * 0.25), B(2, 0))
            y = -180 + k * 110
            ch(c, S, lab, 215, y, p, bg=NAVY, align="l")
            xmark(c, 175, y, 24, p)
        pd = vis(t, B(2, 0.1))
        if pd > 0:
            rng = random.Random(3)
            for k in range(26):
                q = (t * 0.35 + rng.random()) % 1
                drop(c, -150 + rng.uniform(-240, 240), -60 - q * 200 - rng.random() * 60, 20, pd * math.sin(q * math.pi))
            ch(c, S, "LARGE OAK: ~150,000 L OF WATER / YEAR", 0, -280, pd, bg="#0b4f6a", dot="#4da3ff")

def p_brain(c, W, H, t, S):
    long_ = S.n() >= 2
    B = beats(S, 2) if long_ else beats(S, 1)
    fill_bg(c, W, H, "#fde8ee", "#f6c9d4")
    with stage(c, S):
        pa = (1 - prog(t, B(1, 0), 0.5)) if long_ else 1.0
        if pa > 0:
            brain(c, -310, -20, 220, pa)
            e1 = eout(prog(t, B(0, 0.1), 0.8)); e2 = eout(prog(t, B(0, 0.5), 0.8))
            donut2(c, 60, -40, 105, 0.02 * e1, "#6b7488", "2%", "OF WEIGHT", a=pa * clamp(e1 * 3))
            donut2(c, 320, -40, 105, 0.2 * e2, "#e8443a", "20%", "OF ENERGY", a=pa * clamp(e2 * 3))
            ch(c, S, "YOUR BRAIN", -310, -270, vis(t, B(0, 0.05)) * pa, dot="#e8443a")
        if long_:
            pb = prog(t, B(1, 0.05), 0.6)
            if pb > 0:
                bar_h(c, -380, -60, 520, 60, 0.45 * eout(pb), "#3fae4a", "GREEN SKIN AT NOON", "~9 W", a=pb, size=52)
                bar_h(c, -380, 130, 520, 60, 1.0 * eout(prog(t, B(1, 0.2), 0.6)), "#e8443a", "YOUR BRAIN", "~20 W", a=pb, size=52)
                ch(c, S, "EVEN AT HIGH NOON", 0, -270, pb, dot="#ffd166")

def p_year(c, W, H, t, S):
    B = beats(S, 5)
    pa = phase(t, None, B(1, 0))
    with Layer(c, pa) as on:
        if on:
            day_bg(c, W, H, "#bfe6ff", "#e8f5c8")
            ground(c, S, 200, "#9fcf5a")
            with stage(c, S):
                for k in range(9): line(c, -500 + k * 120, 210, -560 + k * 120, 320, "#7fae3a", 6)
                pw = eout(prog(t, B(0, 0.62), 1.2))
                sunball(c, -380, lerp(-200, 150, pw), lerp(55, 40, pw), t)
                if pw > 0: c.drawPaint(paint("#4a6a9a", 0.18 * pw))
                figure(c, -150, 230, 300, GSKIN, 1, hat=True, arms=0.2 + 0.1 * math.sin(t * 2))
                # sunny vs cloudy
                circle(c, 230, -50, 72, "#ffd166"); text(c, "SUNNY", 230, 70, 32, NAVY, 1, w=900)
                cloud(c, 420, -40, 70, "#9aa4b8"); text(c, "CLOUDY", 420, 70, 32, NAVY, vis(t, B(0, 0.6)), w=900)
                big(c, ">", 335, -50, 70, NAVY, vis(t, B(0, 0.45)))
                ch(c, S, "A FREE SNACK EVERY SUNNY DAY", 0, -280, vis(t, B(0, 0.2), B(0, 0.62)), bg="#16401c", dot=LIME)
                ch(c, S, "FAR NORTH: LOW WINTER SUN = LEAN", 0, -280, vis(t, B(0, 0.65)), bg="#24406a", dot="#ffd166")
    pb = phase(t, B(1, 0), B(2, 0))
    with Layer(c, pb) as on:
        if on:
            day_bg(c, W, H, "#fff1e0", "#ffd8b8")
            with stage(c, S):
                figure(c, -220, 260, 440, GSKIN, 1, shirt="#4d96ff")
                rrect(c, -220 - 66, 260 - 440 * 0.79, 132, 150, 26, "#4d96ff")
                text(c, "SHADE", -220, 260 - 440 * 0.65, 30, "#ffffff", 1, w=900)
                figure(c, 230, 260, 440, GSKIN, vis(t, B(1, 0.4)), shirt="#ff6b6b", leaves=0.3)
                ch(c, S, "EVERY SHIRT COVERS YOUR PANELS", 0, -280, vis(t, B(1, 0.05)), dot="#4d96ff")
                ch(c, S, "SHORT + GREEN", 230, 290, vis(t, B(1, 0.6)), bg="#16401c", dot=LIME)
    pc = phase(t, B(2, 0), B(3, 0))
    with Layer(c, pc) as on:
        if on:
            fill_bg(c, W, H, "#241a48", "#0b1030")
            with stage(c, S):
                dna(c, 120, 30, 640, 170, t)
                for k in range(5):
                    q = (t * 0.6 + k / 5) % 1
                    x0 = -420 + k * 60; arrow(c, x0, -260, lerp(x0, x0 + 260, q), lerp(-260, -40, q), "#c77dff", 8, 1 - q)
                for k in range(4):
                    sp = vis(t, B(2, 0.5 + k * 0.08))
                    sx = 0 + k * 120; circle(c, sx, 30 + 50 * math.sin(k), 18 + 8 * math.sin(t * 6 + k), "#ffd166", 0.7 * sp)
                ch(c, S, "UV DAMAGES DNA", -230, -280, vis(t, B(2, 0.2)), dot="#c77dff")
                ch(c, S, "PLANTS: PIGMENTS + REPAIR", 120, 250, vis(t, B(2, 0.5)), bg="#16401c", dot="#ffd166")
    pd = phase(t, B(3, 0), B(4, 0))
    with Layer(c, pd) as on:
        if on:
            fill_bg(c, W, H, "#cfeeb5", "#7fbf6a")
            with stage(c, S):
                rrect(c, -480, -230, 960, 460, 40, "#9fd38a")
                op = 0.5 + 0.5 * math.sin(t * 1.2)
                for sgn in (-1, 1):
                    oval(c, sgn * (60 + 30 * op), 0, 70, 170, "#3fae4a"); oval(c, sgn * (60 + 30 * op), 0, 40, 130, "#5cc85a")
                oval(c, 0, 0, 10 + 30 * op, 120, "#1b3a1b")
                for k in range(4):
                    q = (t * 0.5 + k / 4) % 1
                    co2(c, lerp(-420, 0, q), -150 + k * 90 * (1 - q), 60, 1 - q * 0.8)
                ch(c, S, "STOMATA: TINY PORES", 0, -280, vis(t, B(3, 0.3)), dot=LIME)
                ch(c, S, "CO₂ IN", -300, 260, vis(t, B(3, 0.1)), bg=NAVY)
    pe = phase(t, B(4, 0))
    with Layer(c, pe) as on:
        if on:
            fill_bg(c, W, H, "#fff7d6", "#ffe0b0")
            with stage(c, S):
                sugar_cube(c, -300, -20, 160)
                text(c, "SUGAR ✓", -300, 140, 44, "#2f8f3a", 1, w=900)
                pp = vis(t, B(4, 0.35))
                oval(c, 120, 0, 120, 60, "#ffffff", pp)
                for k in range(3): oval(c, 70 + k * 50, -10, 26, 16, "#c9853a", pp)
                text(c, "PROTEIN", 120, 140, 38, NAVY, pp, w=900)
                xmark(c, 120, 200, 0, 0)
                pm = vis(t, B(4, 0.75))
                circle(c, 400, -40, 120, "#0b1030", pm)
                moon(c, 400, -40, 60, 0.9, pm)
                text(c, "NIGHT: OFF", 400, 140, 38, NAVY, pm, w=900)
                ch(c, S, "GREEN SKIN ONLY MAKES SUGAR", 0, -280, vis(t, B(4, 0.05)), bg="#16401c", dot=LIME)
                ch(c, S, "STILL NEED REAL FOOD", 120, 230, pp, dot="#c9853a")

def p_lizard(c, W, H, t, S):
    B = beats(S, 3)
    fill_bg(c, W, H, "#ffe9b0", "#e8b96a")
    ground(c, S, 250, "#d6a95a")
    with stage(c, S):
        sunball(c, 450, -255, 42, t)
        pa = 1 - prog(t, B(2, 0), 0.6)
        if pa > 0:
            rock(c, -230, 250, 420, 170, pa)
            lizard_at(c, -230, 85, 240, t, pa)
            small_mammal(c, 250, 245, 120, a=pa)
            pb = vis(t, B(1, 0.1)) * pa
            bar_h(c, 110, -120, 300, 44, 1.0 * eout(prog(t, B(1, 0.15), 0.6)), "#e8443a", "MAMMAL", "100%", a=pb, size=44)
            bar_h(c, -430, -120, 300, 44, 0.1 * eout(prog(t, B(1, 0.4), 0.6)), "#7aa84a", "REPTILE", "~10%", a=pb, size=44)
            ch(c, S, "COLD-BLOODED = LOW ENERGY BILL", 0, -275, vis(t, B(0, 0.4)) * pa, bg="#16401c", dot=LIME)
        pc = prog(t, B(2, 0), 0.6)
        if pc > 0:
            rock(c, 0, 250, 700, 140, pc)
            c.save(); c.translate(0, 100); c.rotate(-90)
            figure(c, 0, 0, 340, GSKIN, pc, leaves=0.6)
            c.restore()
            for k in range(3):
                text(c, "z", 250 + k * 40, -60 - k * 50 - (t * 30 % 50), 50 + k * 10, NAVY, pc * 0.7, w=900)
            ch(c, S, "STILL NOT ENOUGH", 0, -275, vis(t, B(2, 0.5)), dot="#e8443a")

def p_evolve(c, W, H, t, S):
    B = beats(S, 4)
    pa = phase(t, None, B(3, 0))
    with Layer(c, pa) as on:
        if on:
            day_bg(c, W, H, "#fff3c4", "#bfe6a0")
            with stage(c, S):
                sunball(c, 380, -220, 55, t)
                f = eout(prog(t, B(1, 0.0), (B(2, 0.2) - B(1, 0.0)) if S.n() >= 4 else 2))
                pl = eout(prog(t, B(2, 0.1), 2.5))
                xs = [-300, 0, 300]
                for k, x in enumerate(xs):
                    ff = f * (0.4 + 0.3 * k)
                    figure(c, x, 270, 380 * (1 - 0.15 * ff), mix(GSKIN, LEAF, ff), 1 - pl * (1 if k != 1 else 0), flat=ff, leaves=ff, arms=0.3 + 0.5 * ff, t=t)
                if pl > 0:
                    tree_big(c, 0, 280, 520 * pl, pl, t)
                ch(c, S, "MILLION-YEAR EXPERIMENT", 0, -275, vis(t, B(0, 0.2), B(1, 0)), dot="#ffd166")
                for k, lab in enumerate(["FLATTER", "WIDER", "THINNER"]):
                    ch(c, S, lab, -300 + k * 300, -275, vis(t, B(1, 0.05 + k * 0.12), B(2, 0)), bg="#16401c")
                ch(c, S, "BASICALLY A PLANT", 0, -275, vis(t, B(2, 0.15)), bg="#16401c", dot=LIME)
                ch(c, S, "FOOD FALLS FROM THE SKY", 0, 270, vis(t, B(2, 0.55)), dot="#ffd166")
    pb = phase(t, B(3, 0))
    with Layer(c, pb) as on:
        if on:
            fill_bg(c, W, H, "#1d3a1d", "#0e2210")
            with stage(c, S):
                p = skia.Path(); p.moveTo(-520, 220); p.cubicTo(-200, 150, 100, 300, 520, 200)
                c.drawPath(p, paint("#6b4a2f", 1, stroke=40))
                for k in range(6): leaf_rot(c, -480 + k * 180, 200 + 15 * math.sin(k), 60, 160 + 30 * (k % 2), "#2e6b2a", 1)
                rafflesia(c, 0, 20, 260 * eback(prog(t, B(3, 0.15), 0.8)), t)
                ch(c, S, "RAFFLESIA", -320, -270, vis(t, B(3, 0.1)), dot="#c0392b")
                ch(c, S, "GAVE UP PHOTOSYNTHESIS", 0, 280, vis(t, B(3, 0.35)), bg="#16401c", dot="#c0392b")

# ---------- reef / ocean
GBR = (141.5, -26.5, 154.5, -9.0)
REEF = [(143.6, -11.2), (143.9, -12.5), (144.4, -13.8), (145.3, -14.9), (145.9, -16.0), (146.4, -17.0), (147.0, -17.9),
        (148.0, -18.8), (149.2, -19.6), (150.3, -20.4), (151.2, -21.2), (151.9, -22.2), (152.4, -23.2), (152.8, -24.0)]

def reef_floor(c, W, H, t, white=0.0):
    sea_bg(c, W, H)
    rays(c, W, H, t, 0.12)
    u = min(W, H) / 1080
    c.drawRect(skia.Rect.MakeLTRB(0, 0.8 * H, W, H), paint("#e9d8a6"))
    cols = ["#ff7f6b", "#ffb347", "#c77dff", "#ff6bb3", "#7ee081", "#ffd166"]
    for k in range(10):
        x = W * (k + 0.5) / 10
        coral_branch(c, x, 0.82 * H, (220 + 90 * (k % 3)) * u, mix(cols[k % 6], "#f4f4f0", white), t, seed=k)

def p_coral(c, W, H, t, S):
    B = beats(S, 3)
    tm = S.lt(1, 0.48) if S.n() >= 3 else S.dur * 0.6
    pa = phase(t, None, B(1, 0))
    with Layer(c, pa) as on:
        if on:
            reef_floor(c, W, H, t)
            with stage(c, S):
                for k in range(4):
                    fish(c, ((t * 60 + k * 300) % 1300) - 650, -150 + k * 70, 30 + 5 * k, ["#ffd166", "#4d96ff", "#ff6b6b", "#ffffff"][k], flip=False)
                ch(c, S, "A MIDDLE PATH", 0, -275, vis(t, B(0, 0.1)), bg="#0b4f6a", dot=LIME)
    pb = phase(t, B(1, 0), tm)
    with Layer(c, pb) as on:
        if on:
            fill_bg(c, W, H, "#1aa3b0", "#075b6e")
            with stage(c, S):
                # a polyp, cut-away
                rrect(c, -380, -40, 260, 320, 60, "#ff9f7a")
                for k in range(8):
                    an = math.radians(-160 + k * 20)
                    line(c, -250, -40, -250 + math.cos(an) * 200, -40 + math.sin(an) * 160 + math.sin(t * 2 + k) * 10, "#ffb39a", 18)
                rng = random.Random(1)
                for k in range(30):
                    circle(c, -360 + rng.random() * 220, -10 + rng.random() * 270, 11, "#b5741f")
                q = prog(t, B(1, 0.15), 1.2)
                for k in range(5):
                    qq = (t * 0.5 + k / 5) % 1
                    sugar_cube(c, lerp(-130, 330, qq), 200 - 30 * math.sin(qq * 3), 50, q * math.sin(qq * math.pi))
                big(c, "UP TO 90%", 260, -30, 110, LIME, vis(t, B(1, 0.15)))
                text(c, "OF THE ALGAE'S FOOD", 260, 60, 36, "#ffffff", vis(t, B(1, 0.2)), w=800, fam="Inter")
                ch(c, S, "ALGAE INSIDE CORAL", -250, -280, vis(t, B(1, 0.03)), dot="#b5741f")
    pg = phase(t, tm, B(2, 0))
    with Layer(c, pg) as on:
        if on:
            fill_bg(c, W, H, "#020615", "#0b1030")
            stars(c, W, H, t, 0.8, seed=11)
            rr = gbr_rect(S)
            geo.draw_map(c, GBR, rr, land="#c99a5a", sea="#0b3f7a", outline_w=2)
            c.save(); c.clipRect(skia.Rect.MakeXYWH(*rr))
            rng = random.Random(4)
            pr = prog(t, tm + 0.2, 1.5)
            for i, (lo, la) in enumerate(REEF):
                if i / len(REEF) > pr: break
                for j in range(5):
                    x, y = geo.lonlat_xy(lo + rng.uniform(-0.4, 0.4), la + rng.uniform(-0.4, 0.4), GBR, rr)
                    circle(c, x, y, rr[2] * 0.012, "#5ff2e0", 0.9)
            c.restore()
            c.drawRect(skia.Rect.MakeXYWH(*rr), paint("#ffffff", 0.7, stroke=3))
            with stage(c, S):
                ch(c, S, "GREAT BARRIER REEF, FROM SPACE", 0, -280, vis(t, tm + 0.1), dot="#5ff2e0")
                ch(c, S, "LARGEST STRUCTURE BUILT BY LIFE", 0, 280, vis(t, tm + 0.8), bg="#0b4f6a")
    pc = phase(t, B(2, 0))
    with Layer(c, pc) as on:
        if on:
            w_ = eout(prog(t, B(2, 0.35), 2.0))
            reef_floor(c, W, H, t, white=w_)
            with stage(c, S):
                ch(c, S, "ALGAE = CORAL COLORS", 0, -275, vis(t, B(2, 0.05), B(2, 0.4)), bg="#0b4f6a", dot="#ff7f6b")
                ch(c, S, "NO ALGAE = BLEACHING", 0, -275, vis(t, B(2, 0.45)), dot="#ffffff")

_gbr = {}
def gbr_rect(S):
    k = (S.W, S.H)
    if k not in _gbr:
        if S.P: _gbr[k] = geo.map_rect(GBR, S.W / 2, 0.42 * S.H, height=0.3 * S.H)
        else: _gbr[k] = geo.map_rect(GBR, S.W / 2, 0.53 * S.H, height=0.72 * S.H)
    return _gbr[k]

def p_clam(c, W, H, t, S):
    B = beats(S, 3)
    pa = phase(t, None, B(1, 0))
    with Layer(c, pa) as on:
        if on:
            sea_bg(c, W, H); rays(c, W, H, t, 0.15, x=W * 0.5)
            ground(c, S, 210, "#e9d8a6")
            with stage(c, S):
                clam(c, 0, 170, 360, t)
                ch(c, S, "GIANT CLAM", 0, -275, vis(t, B(0, 0.05)), bg="#0b4f6a", dot="#2ec4b6")
                ch(c, S, "MANTLE SOAKS UP ~95% OF SUNLIGHT", 0, 285, vis(t, B(0, 0.5)), bg="#16401c", dot="#ffd166")
    pb = phase(t, B(1, 0), B(2, 0))
    with Layer(c, pb) as on:
        if on:
            fill_bg(c, W, H, "#bfe9d8", "#6fbfa8")
            with stage(c, S):
                hydra(c, -150, 250, 480, t)
                for k in range(3):
                    q = (t * 0.5 + k / 3) % 1
                    sugar_cube(c, lerp(-100, 250, q), -60 + k * 40, 50, math.sin(q * math.pi))
                    circle(c, lerp(250, -100, q), 80 + k * 40, 16, "#4d96ff", math.sin(q * math.pi))
                text(c, "SUGAR →", 300, -120, 40, "#16401c", 1, w=900)
                text(c, "← NITROGEN", 300, 200, 40, "#0b4f6a", 1, w=900)
                ch(c, S, "GREEN HYDRA", -150, -280, vis(t, B(1, 0.05)), dot="#5cbf55")
                ch(c, S, "SUGAR ↔ NITROGEN", 280, -280, vis(t, B(1, 0.4)), bg="#16401c")
    pc = phase(t, B(2, 0))
    with Layer(c, pc) as on:
        if on:
            sea_bg(c, W, H, "#7fe0e0", "#1a8fa0"); rays(c, W, H, t, 0.15, x=W * 0.5)
            ground(c, S, 220, "#e9d8a6")
            with stage(c, S):
                upside_jelly(c, -200, 220, 300, t)
                upside_jelly(c, 270, 230, 190, t + 1)
                for k in range(5):
                    q = (t * 0.6 + k / 5) % 1
                    arrow(c, -350 + k * 140, -260, -350 + k * 140, lerp(-260, 60, q), "#ffd166", 6, 0.8 * (1 - q))
                ch(c, S, "UPSIDE-DOWN JELLYFISH", 0, -275, vis(t, B(2, 0.1)), bg="#0b4f6a", dot="#d9c49a")
                ch(c, S, "ARMS UP = ALGAE IN THE SUN", 0, 285, vis(t, B(2, 0.5)), bg="#16401c", dot="#ffd166")

def p_slug(c, W, H, t, S):
    o = S.opts; mode = o.get("mode")
    if S.n() >= 3 and not mode: return _slug_long(c, W, H, t, S)
    sea_bg(c, W, H, "#9fe8d8", "#2a9a8a")
    rays(c, W, H, t, 0.14, x=W * 0.5)
    ground(c, S, 230, "#d9cfa0")
    with stage(c, S):
        T0 = S.lt(0, 0); T1 = S.lt(0, 1)
        q = prog(t, T0 + 0.2, T1 - T0)
        if mode is None:
            slug(c, 60 + math.sin(t * 0.5) * 20, 40, 380, t, glow=0.4)
            leaf_rot(c, -300, 150, 110, -70, "#3fae4a", 1)
            text(c, "LEAF?", -330, -180, 44, "#0b4f6a", prog(t, 0.6, 0.5), w=900)
            text(c, "SLUG!", 170, -180, 44, "#16401c", prog(t, 1.4, 0.5), w=900)
        elif mode == "steal":
            algae_strands(c, -200, 230, 360, 240, t, eaten=q * 0.7)
            sx = lerp(-60, 120, q)
            slug(c, sx + 80, 60, 360, t, glow=q)
            for k in range(12):
                f = ((t * 0.5 + k / 12) % 1)
                x = lerp(-160, sx + 40, f); y = lerp(150 - k * 10, 60, f)
                chloroplast(c, x, y, 14, k * 30, (1 - f) * clamp(q * 3))
            ch(c, S, "CHLOROPLASTS KEPT ALIVE", 0, -275, vis(t, T0 + 0.6 * (T1 - T0)), bg="#16401c", dot=LIME)
        elif mode == "months":
            slug(c, -170, 60, 360, t, glow=0.9)
            n = 1 + min(8, int(q * 9.5))
            calendar(c, 290, 0, 230 * eback(prog(t, T0, 0.4)), f"{n}" if q < 0.95 else "9+")
            ch(c, S, "NO FOOD NEEDED", 0, -275, vis(t, T0 + 0.5 * (T1 - T0)), bg="#16401c", dot=LIME)
        elif mode == "dna":
            slug(c, -160, 80, 280, t, glow=0.6)
            dna(c, 270, -20, 380, 150, t)
            xmark(c, 270, -20, 110, prog(t, T0 + 0.35 * (T1 - T0), 0.4))
            ch(c, S, "NO ALGAE GENES FOUND", 230, 180, vis(t, T0 + 0.4 * (T1 - T0)), bg="#16401c", dot="#ff6b6b")
        elif mode == "regrow":
            _regrow(c, t, q, S)
    kit.hook(c, W, H, t, S)

def _regrow(c, t, q, S, x0=0):
    sep = eout(clamp(q * 2.2)); grow = clamp((q - 0.45) / 0.5)
    slug(c, x0 - 120 - sep * 120, 70, 360, t, a=1 - grow * 0.85, head=False, glow=0.2)
    slug(c, x0 + 60 + sep * 120, 70, 360, t, body=0.1 + 0.9 * grow if grow > 0.02 else 0.0, glow=0.6 * grow)
    if 0.25 < q:
        ch(c, S, "NEW BODY", x0 + 120, -200, clamp((q - 0.5) * 4), bg="#16401c", dot=LIME)
        ch(c, S, "OLD BODY", x0 - 300, -200, clamp((q - 0.3) * 4), bg=NAVY)

def _slug_long(c, W, H, t, S):
    B = beats(S, 3)
    sea_bg(c, W, H, "#9fe8d8", "#2a9a8a"); rays(c, W, H, t, 0.14, x=W * 0.5)
    ground(c, S, 230, "#d9cfa0")
    pa = phase(t, None, B(2, 0))
    with Layer(c, pa) as on:
        if on:
            with stage(c, S):
                q = prog(t, B(0, 0.25), 3)
                algae_strands(c, -280, 230, 300, 230, t, eaten=q * 0.7)
                slug(c, 120 + lerp(-60, 60, q), 50, 380, t, glow=clamp(q * 1.5))
                ch(c, S, "ELYSIA CHLOROTICA", 0, -275, vis(t, B(0, 0.1), B(0, 0.7)), bg="#16401c", dot=LIME)
                ch(c, S, "9+ MONTHS WITHOUT EATING", 0, -275, vis(t, B(0, 0.75), B(1, 0.4)), dot="#ffd166")
                ch(c, S, "A FEW CM LONG", 330, 280, vis(t, B(1, 0.05)), bg="#0b4f6a")
                ch(c, S, "HOW MUCH SUN HELPS: DEBATED", 0, -275, vis(t, B(1, 0.45)), bg="#16401c", dot="#ff6b6b")
    pb = phase(t, B(2, 0))
    with Layer(c, pb) as on:
        if on:
            with stage(c, S):
                q = prog(t, B(2, 0.15), max(2.0, S.dur - B(2, 0.15) - 0.6))
                _regrow(c, t, q, S)
                ch(c, S, "SOME RELATIVES REGROW A BODY", 0, -275, vis(t, B(2, 0.05)), dot="#ffd166")

def p_mantis(c, W, H, t, S):
    mode = S.opts.get("mode", "cones")
    T0 = S.lt(0, 0); T1 = S.lt(0, 1); D = max(0.5, T1 - T0)
    q = prog(t, T0, D)
    fill_bg(c, W, H, "#0e3a5a", "#071a2e")
    rays(c, W, H, t, 0.06, x=W * 0.5)
    with stage(c, S):
        if mode == "cones":
            mantis(c, 260, 120, 210, t)
            x0, x1, yb = -470, -40, 120
            def curves(n, yb, a, cols, wd):
                for k in range(n):
                    mu = k / max(1, n - 1); colr = cols[k % len(cols)]
                    p = skia.Path()
                    for i in range(41):
                        f = i / 40; yy = yb - 150 * math.exp(-((f - (0.08 + mu * 0.84)) / wd) ** 2)
                        (p.moveTo if i == 0 else p.lineTo)(lerp(x0, x1, f), yy)
                    c.drawPath(p, paint(colr, a, stroke=5))
                line(c, x0, yb, x1, yb, "#ffffff", 3, a)
            a1 = prog(t, T0, 0.5)
            curves(3, -60, a1, ["#4d7dff", "#3fd14a", "#ff4d4d"], 0.22)
            text(c, "YOU: 3", x0, -250, 40, "#ffffff", a1, w=900, align="l")
            a2 = prog(t, T0 + D * 0.55, 0.6)
            rainbow = ["#b04dff", "#7d4dff", "#4d7dff", "#4dc3ff", "#4dffd8", "#3fd14a", "#a6e22e", "#ffe14d", "#ffb14d", "#ff7a4d", "#ff4d4d", "#c41e3a"]
            curves(12, 230, a2, rainbow, 0.06)
            text(c, "MANTIS SHRIMP: 12", x0, 40, 40, "#ffd166", a2, w=900, align="l")
        elif mode == "uv":
            mantis(c, 250, 120, 220, t)
            for k in range(6):
                qq = (t * 0.5 + k / 6) % 1
                x = lerp(-480, 40, qq)
                p = skia.Path()
                for i in range(30):
                    f = i / 29; xx = x - 120 + f * 120
                    yy = -150 + k * 4 + math.sin(f * 12 + t * 6) * 22
                    (p.moveTo if i == 0 else p.lineTo)(xx, yy + (k - 2.5) * 30)
                c.drawPath(p, paint("#c77dff", 1 - qq, stroke=5))
            # circular polarization helix
            for i in range(60):
                f = i / 59; ph = f * 6 * math.pi - t * 4
                xx = lerp(-480, 0, f); yy = 140 + math.sin(ph) * 50; r = 8 + 5 * math.cos(ph)
                circle(c, xx, yy, r, "#5ff2e0", 0.4 + 0.5 * (math.cos(ph) > 0))
            ch(c, S, "ULTRAVIOLET", -250, -270, vis(t, T0 + 0.1), bg="#3a1a5a", dot="#c77dff")
            ch(c, S, "CIRCULARLY POLARIZED", -250, 260, vis(t, T0 + D * 0.45), bg="#0b4f6a", dot="#5ff2e0")
        elif mode == "eyes":
            for k, x in enumerate((-200, 200)):
                ph = t * (1.3 + k * 0.9) + k * 2
                ex = x + 70 * math.sin(ph); ey = -40 + 40 * math.cos(ph * 1.3)
                line(c, x, 300, ex, ey, "#2ec4b6", 50)
                eye(c, ex, ey, 140, 25 * math.sin(ph * 0.8), 1)
            ch(c, S, "EACH EYE MOVES ON ITS OWN", 0, -270, vis(t, T0 + 0.1), dot="#2ec4b6")
            ch(c, S, "3 ZONES = DEPTH FROM ONE EYE", 0, 270, vis(t, T0 + D * 0.5), bg="#16401c", dot="#ffd166")
        elif mode == "test":
            for k, colr in enumerate(("#3fae7a", "#46b37a")):
                rrect(c, -300 + k * 170, -230, 150, 150, 20, colr)
            text(c, "~25 NM APART", -215, -40, 34, "#ffffff", 1, w=800, fam="Inter")
            a1 = vis(t, T0 + D * 0.35)
            figure(c, -330, 260, 200, SKIN, a1)
            check(c, -180, 160, 50, a1)
            text(c, "YOU: FEW NM", -255, 290, 32, "#ffffff", a1, w=900)
            a2 = vis(t, T0 + D * 0.6)
            mantis(c, 270, 150, 170, t, a2)
            xmark(c, 270, -60, 60, a2)
            text(c, "SHRIMP: OFTEN FAILS", 260, 290, 32, "#ffd166", a2, w=900)
        elif mode == "punch":
            st = (t * 0.7) % 1
            strike = clamp((st - 0.55) / 0.08) if st < 0.75 else clamp(1 - (st - 0.75) / 0.2)
            mantis(c, 190, 90, 245, t, strike=strike)
            sx = 190 - 245 * 1.03 - 62
            snail(c, sx, 90 + 245 * 0.1, 62, crack=clamp((st - 0.6) * 4))
            if 0.6 < st < 0.85:
                qq = (st - 0.6) / 0.25
                circle(c, sx + 40, 130, 30 + 120 * qq, "#ffffff", 0.8 * (1 - qq), stroke=8)
                circle(c, sx + 40, 130, 20 + 40 * qq, "#bfefff", 0.6 * (1 - qq))
            big(c, "20+ M/S", 0, -220, 110, "#ffd166", vis(t, T0 + 0.2))
            ch(c, S, "CAVITATION BUBBLE", sx + 20, 280, vis(t, T0 + D * 0.5), bg="#0b4f6a", dot="#bfefff")
    kit.hook(c, W, H, t, S)

SCENES = {"p_title": p_title, "p_card": p_card, "p_end": p_end, "p_endshort": p_endshort,
          "p_salamander": p_salamander, "p_rules": p_rules, "p_oxygen": p_oxygen, "p_green": p_green,
          "p_morning": p_morning, "p_math": p_math, "p_tennis": p_tennis, "p_leaf": p_leaf, "p_brain": p_brain,
          "p_year": p_year, "p_lizard": p_lizard, "p_evolve": p_evolve, "p_coral": p_coral, "p_clam": p_clam,
          "p_slug": p_slug, "p_mantis": p_mantis}
