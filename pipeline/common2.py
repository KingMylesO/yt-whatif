"""Shared props for Batch 02 scenes."""
import math, random
from functools import lru_cache
import skia
from core import *
from scenes import Ctx, vis, until_next, card as _card1
import geo

# ---------- small helpers ----------
def arrow(c, x0, y0, x1, y1, color, w, a=1.0, head=None, dash=None):
    head = head or w * 3.2
    ang = math.atan2(y1 - y0, x1 - x0)
    bx, by = x1 - math.cos(ang) * head * 0.8, y1 - math.sin(ang) * head * 0.8
    c.drawLine(x0, y0, bx, by, paint(color, a, stroke=w, dash=dash))
    pts = [(x1, y1), (x1 - math.cos(ang - 0.45) * head, y1 - math.sin(ang - 0.45) * head),
           (x1 - math.cos(ang + 0.45) * head, y1 - math.sin(ang + 0.45) * head)]
    c.drawPath(poly(pts), paint(color, a))

def stamp(c, txt, x, y, p, u, color="#ff4d4d", rot=-10, size=110):
    if p <= 0: return
    sc = lerp(1.8, 1.0, eout(p))
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(sc, sc)
    wdt = tw(txt, size * u, 900) + 60 * u
    rrect(c, -wdt / 2, -size * 0.72 * u, wdt, size * 1.44 * u, 18 * u, color, eout(p), stroke=10 * u)
    text(c, txt, 0, 0, size * u, color, eout(p), w=900)
    c.restore()

def gauge(c, x, y, r, frac, label, u, valtxt=None, colr=ACCENT, a=1.0, lo_col="#ff4d4d", hi_col="#4cd964"):
    p = skia.Path(); p.addArc(skia.Rect.MakeLTRB(x - r, y - r, x + r, y + r), 180, 180)
    c.drawPath(p, paint("#ffffff", 0.15 * a, stroke=r * 0.16, cap="butt"))
    p2 = skia.Path(); p2.addArc(skia.Rect.MakeLTRB(x - r, y - r, x + r, y + r), 180, 180 * clamp(frac))
    c.drawPath(p2, paint(colr, a, stroke=r * 0.16, cap="butt"))
    ang = math.pi + math.pi * clamp(frac)
    line(c, x, y, x + math.cos(ang) * r * 0.85, y + math.sin(ang) * r * 0.85, "#ffffff", r * 0.05, a)
    circle(c, x, y, r * 0.08, "#ffffff", a)
    text(c, label, x, y + r * 0.35, r * 0.16, "#cfe3ff", a, w=700, fam="Inter")
    if valtxt: text(c, valtxt, x, y - r * 0.38, r * 0.3, "#ffffff", a, w=900, shadow=8)

def bar(c, x, y, w, h, frac, colr, u, label=None, val=None, a=1.0):
    rrect(c, x, y, w, h, h / 2, "#ffffff", 0.12 * a)
    if frac > 0: rrect(c, x, y, max(h, w * clamp(frac)), h, h / 2, colr, a)
    if label: text(c, label, x, y - h * 0.9, h * 0.75, "#ffffff", a, w=700, fam="Inter", align="l")
    if val: text(c, val, x + w + 20 * u, y + h / 2, h * 0.8, colr, a, w=900, align="l")

def flame(c, x, y, s, t, seed=0, a=1.0):
    rng = random.Random(seed)
    for k, (colr, sc) in enumerate([("#ff4d1a", 1.0), ("#ff9a1f", 0.72), ("#ffe066", 0.42)]):
        fl = 1 + 0.12 * math.sin(t * 9 + seed + k)
        h = s * sc * fl; w = s * sc * 0.42
        p = skia.Path(); p.moveTo(x, y - h)
        p.cubicTo(x + w * 1.1, y - h * 0.45, x + w, y, x, y)
        p.cubicTo(x - w, y, x - w * 1.1, y - h * 0.45, x, y - h)
        c.drawPath(p, paint(colr, a * (0.9 if k == 0 else 1)))

def smoke(c, x, y, t, u, a=1.0, seed=1, n=10, col_="#3a3a44", rise=300):
    rng = random.Random(seed)
    for i in range(n):
        ph = rng.random(); q = (ph + t * 0.15) % 1
        r = (20 + q * 70) * u
        circle(c, x + math.sin(q * 4 + i) * 40 * u * q, y - q * rise * u, r, col_, a * 0.45 * (1 - q), blur=r * 0.4)

# ---------- forest props ----------
def forest_bg(c, W, H, t, u, dark=0.0, season=None, hy=0.62):
    sky_t = mix("#bfe6d2", "#0a1020", dark); sky_b = mix("#e9f6e8", "#141c30", dark)
    if season is not None:
        sky_t = mix(sky_t, ["#bfe6d2", "#f4c98f", "#dfe7ef", "#bfe6d2"][season % 4], 0.6)
    fill_bg(c, W, H, sky_t, sky_b)
    rng = random.Random(3)
    for layer, (colr, sc, yo) in enumerate([("#8fc59b", 0.7, 0.0), ("#5fa874", 0.9, 0.05)]):
        cl = mix(colr, "#0b1520", dark)
        x = -50
        while x < W + 80:
            h = rng.uniform(180, 320) * u * sc
            rect(c, x - 6 * u, hy * H + yo * H - h * 0.5, 12 * u, h * 0.6, mix("#5b4636", "#0b0f16", dark))
            circle(c, x, hy * H + yo * H - h * 0.7, h * 0.32, cl); circle(c, x - h * 0.2, hy * H + yo * H - h * 0.5, h * 0.25, cl)
            circle(c, x + h * 0.22, hy * H + yo * H - h * 0.55, h * 0.26, cl)
            x += rng.uniform(70, 140) * u
    c.drawRect(skia.Rect.MakeXYWH(0, hy * H + 0.05 * H, W, H), paint(shader=lin(0, hy * H, 0, H, [(0, mix("#6b8f4e", "#0a1210", dark), 1), (1, mix("#4a3a28", "#06080c", dark), 1)])))

def log(c, x, y, L, r, colr="#7a5236", ang=0, moss=0.0, a=1.0, crumble=0.0, seed=1):
    c.save(); c.translate(x, y); c.rotate(ang)
    Lc = L * (1 - 0.5 * crumble)
    rrect(c, -Lc / 2, -r, Lc, 2 * r, r * 0.5, colr, a)
    for k in range(4):
        yy = -r + r * 0.4 * (k + 0.5)
        line(c, -Lc / 2 + r * 0.6, yy, Lc / 2 - r * 0.3, yy + r * 0.06, mix(colr, "#000000", 0.25), max(1.5, r * 0.06), a)
    if moss > 0:
        rng = random.Random(seed)
        for k in range(int(10 * moss)):
            mx = rng.uniform(-Lc / 2 + r, Lc / 2 - r)
            oval(c, mx, -r * 0.85, r * rng.uniform(0.35, 0.7), r * 0.25, "#5aa34a", a * 0.9)
    if crumble > 0:
        rng = random.Random(seed + 7)
        for k in range(int(14 * crumble)):
            circle(c, rng.uniform(-Lc / 2, Lc / 2), r * rng.uniform(0.6, 1.3), r * rng.uniform(0.08, 0.2), mix(colr, "#3b2a1e", 0.4), a)
    circle(c, Lc / 2, 0, r, mix(colr, "#d9b48a", 0.45), a)
    for k in (0.7, 0.45, 0.2): circle(c, Lc / 2, 0, r * k, mix(colr, "#000000", 0.25), a * 0.7, stroke=max(1.2, r * 0.05))
    c.restore()

def shelf(c, x, y, s, colr="#c9853a", a=1.0):
    p = skia.Path(); p.addArc(skia.Rect.MakeXYWH(x - s, y - s * 0.55, 2 * s, s * 1.1), 180, 180); p.close()
    c.drawPath(p, paint(colr, a))
    p2 = skia.Path(); p2.addArc(skia.Rect.MakeXYWH(x - s * 0.7, y - s * 0.35, 1.4 * s, s * 0.7), 180, 180)
    c.drawPath(p2, paint("#f3d7a0", a * 0.8, stroke=max(1.5, s * 0.08)))

def mushroom(c, x, y, s, colr="#d9532b", a=1.0):
    rrect(c, x - s * 0.18, y - s * 0.9, s * 0.36, s * 0.9, s * 0.15, "#f2e8d5", a)
    p = skia.Path(); p.addArc(skia.Rect.MakeXYWH(x - s * 0.6, y - s * 1.3, s * 1.2, s * 0.9), 180, 180); p.close()
    c.drawPath(p, paint(colr, a))
    for dx in (-0.25, 0.1, 0.3): circle(c, x + dx * s, y - s * 1.08, s * 0.07, "#fff5e6", a)

def tree2(c, x, y, h, leaf="#2f8f55", trunk="#5b3e2a", a=1.0):
    rect(c, x - h * 0.045, y - h * 0.5, h * 0.09, h * 0.5, trunk, a)
    for dx, dy, r in [(0, -0.72, 0.26), (-0.18, -0.55, 0.2), (0.19, -0.57, 0.21), (0, -0.88, 0.16)]:
        circle(c, x + dx * h, y + dy * h, r * h, leaf, a)

def conifer(c, x, y, h, colr="#2e5e4e", snow=0.0, a=1.0):
    rect(c, x - h * 0.03, y - h * 0.15, h * 0.06, h * 0.15, "#4a3424", a)
    for k in range(3):
        yy = y - h * 0.15 - k * h * 0.25; w = h * (0.3 - k * 0.07)
        c.drawPath(poly([(x - w, yy), (x, yy - h * 0.38), (x + w, yy)]), paint(colr, a))
        if snow: c.drawPath(poly([(x - w * 0.4, yy - h * 0.23), (x, yy - h * 0.38), (x + w * 0.4, yy - h * 0.23)]), paint("#ffffff", a * snow))

def lycopsid(c, x, y, h, a=1.0, t=0.0):
    w = h * 0.045
    rect(c, x - w, y - h, 2 * w, h, "#4f6b3a", a)
    for k in range(int(h / (w * 1.6))):
        yy = y - k * w * 1.6
        for s_ in (-1, 1):
            c.drawPath(poly([(x + s_ * w * 0.2, yy), (x + s_ * w * 0.8, yy - w * 0.8), (x + s_ * w * 0.2, yy - w * 1.6)]), paint("#3d5a2c", a * 0.7))
    for k in range(5):
        ang = math.radians(-150 + k * 30) + 0.05 * math.sin(t + k)
        bx, by = x + math.cos(ang) * h * 0.12, y - h + math.sin(ang) * h * 0.12
        line(c, x, y - h, bx, by, "#4f6b3a", w * 0.8, a)
        for j in range(6):
            line(c, bx, by, bx + math.cos(ang + (j - 2.5) * 0.25) * h * 0.06, by + math.sin(ang + (j - 2.5) * 0.25) * h * 0.06, "#6b9a3a", w * 0.25, a)

def treefern(c, x, y, h, a=1.0, t=0.0):
    rect(c, x - h * 0.03, y - h, h * 0.06, h, "#5b4a2a", a)
    for k in range(7):
        ang = math.radians(-170 + k * 27) + 0.05 * math.sin(t * 1.3 + k)
        p = skia.Path(); p.moveTo(x, y - h)
        p.quadTo(x + math.cos(ang) * h * 0.25, y - h + math.sin(ang) * h * 0.25 - h * 0.05, x + math.cos(ang) * h * 0.38, y - h + math.sin(ang) * h * 0.38 + h * 0.06)
        c.drawPath(p, paint("#4e8b3a", a, stroke=h * 0.025))

def dragonfly(c, x, y, s, t, a=1.0, col_="#1c2a3a"):
    flap = math.sin(t * 30) * 0.25
    for side in (-1, 1):
        for k, off in enumerate((-0.12, 0.12)):
            c.save(); c.translate(x, y + off * s * 0.4); c.rotate(side * (8 + flap * 20) + (k * 6))
            oval(c, side * s * 0.55, 0, s * 0.55, s * 0.12, "#cfe8ff", a * 0.55)
            c.restore()
    rrect(c, x - s * 0.05, y - s * 0.15, s * 0.1, s * 1.1, s * 0.05, col_, a)
    circle(c, x, y - s * 0.2, s * 0.1, col_, a)

def millipede(c, x, y, s, t, a=1.0):
    n = 18
    for i in range(n):
        xx = x - i * s * 0.11; yy = y + math.sin(t * 3 + i * 0.6) * s * 0.02
        oval(c, xx, yy, s * 0.065, s * 0.05, "#7a4b2b" if i % 2 else "#8c5a34", a)
        for sgn in (-1, 1):
            line(c, xx, yy, xx + math.sin(t * 8 + i) * s * 0.02, yy + sgn * s * 0.07, "#3b2616", max(1, s * 0.008), a)

def termite(c, x, y, s, a=1.0, col_="#e8c79a"):
    oval(c, x + s * 0.5, y, s * 0.35, s * 0.22, col_, a); oval(c, x, y, s * 0.25, s * 0.2, col_, a)
    circle(c, x - s * 0.35, y, s * 0.18, mix(col_, "#7a4b2b", 0.4), a)
    for k in range(3):
        line(c, x - s * 0.1 + k * s * 0.15, y, x - s * 0.2 + k * s * 0.2, y + s * 0.38, mix(col_, "#000000", 0.4), max(1, s * 0.05), a)
        line(c, x - s * 0.1 + k * s * 0.15, y, x - s * 0.2 + k * s * 0.2, y - s * 0.38, mix(col_, "#000000", 0.4), max(1, s * 0.05), a)

def human(c, x, y, h, colr="#e8eef8", a=1.0):
    circle(c, x, y - h * 0.9, h * 0.08, colr, a)
    rrect(c, x - h * 0.09, y - h * 0.8, h * 0.18, h * 0.42, h * 0.07, colr, a)
    line(c, x - h * 0.05, y - h * 0.4, x - h * 0.06, y, colr, h * 0.06, a); line(c, x + h * 0.05, y - h * 0.4, x + h * 0.06, y, colr, h * 0.06, a)

# ---------- dinosaurs & life ----------
def trex(c, x, y, s, t=0.0, colr="#1a1f2e", a=1.0, walk=True):
    ph = math.sin(t * 4) if walk else 0
    p = skia.Path()
    p.moveTo(x - 1.2 * s, y - 0.55 * s)
    p.quadTo(x - 0.5 * s, y - 0.78 * s, x + 0.1 * s, y - 0.8 * s)
    p.quadTo(x + 0.45 * s, y - 1.05 * s, x + 0.62 * s, y - 1.05 * s)
    p.lineTo(x + 0.95 * s, y - 1.0 * s); p.lineTo(x + 0.95 * s, y - 0.85 * s); p.lineTo(x + 0.6 * s, y - 0.8 * s)
    p.quadTo(x + 0.45 * s, y - 0.6 * s, x + 0.2 * s, y - 0.48 * s)
    p.quadTo(x - 0.4 * s, y - 0.38 * s, x - 1.2 * s, y - 0.55 * s); p.close()
    c.drawPath(p, paint(colr, a))
    for k, off in enumerate((0.15, -0.15)):
        sw = ph * 0.15 * (1 if k == 0 else -1)
        line(c, x + off * s * 0.3, y - 0.5 * s, x + (off + sw) * s * 0.6, y - 0.22 * s, colr, s * 0.14, a)
        line(c, x + (off + sw) * s * 0.6, y - 0.22 * s, x + (off + sw) * s * 0.4 + 0.05 * s, y, colr, s * 0.1, a)
    line(c, x + 0.45 * s, y - 0.7 * s, x + 0.55 * s, y - 0.6 * s, colr, s * 0.04, a)

def sauropod(c, x, y, s, colr="#1a1f2e", a=1.0, t=0.0):
    oval(c, x, y - 0.5 * s, 0.6 * s, 0.28 * s, colr, a)
    p = skia.Path(); p.moveTo(x + 0.4 * s, y - 0.6 * s); p.quadTo(x + 0.8 * s, y - 1.3 * s, x + 1.0 * s, y - 1.45 * s + math.sin(t) * 0.03 * s)
    c.drawPath(p, paint(colr, a, stroke=0.14 * s)); circle(c, x + 1.02 * s, y - 1.45 * s + math.sin(t) * 0.03 * s, 0.09 * s, colr, a)
    p2 = skia.Path(); p2.moveTo(x - 0.5 * s, y - 0.55 * s); p2.quadTo(x - 1.1 * s, y - 0.5 * s, x - 1.4 * s, y - 0.25 * s)
    c.drawPath(p2, paint(colr, a, stroke=0.08 * s))
    for dx in (-0.35, -0.15, 0.2, 0.4): rect(c, x + dx * s - 0.05 * s, y - 0.4 * s, 0.1 * s, 0.4 * s, colr, a)

def small_mammal(c, x, y, s, colr="#6b5a4a", a=1.0, eyes=True):
    oval(c, x, y - s * 0.35, s * 0.55, s * 0.35, colr, a); circle(c, x + s * 0.5, y - s * 0.45, s * 0.25, colr, a)
    circle(c, x + s * 0.45, y - s * 0.72, s * 0.1, colr, a)
    p = skia.Path(); p.moveTo(x - s * 0.5, y - s * 0.3); p.quadTo(x - s * 1.0, y - s * 0.5, x - s * 1.1, y - s * 0.1)
    c.drawPath(p, paint(colr, a, stroke=s * 0.06))
    if eyes: circle(c, x + s * 0.6, y - s * 0.5, s * 0.06, "#ffe58a", a)

def asteroid(c, x, y, r, t=0.0, a=1.0, trail=0.0, ang=-35, glow=0.0):
    if trail > 0:
        tr = math.radians(ang + 180)
        tx, ty = x + math.cos(tr) * r * 8 * trail, y + math.sin(tr) * r * 8 * trail
        c.drawLine(x, y, tx, ty, paint(shader=lin(x, y, tx, ty, [(0, "#ffd166", 0.85 * a), (1, "#ff6b35", 0)]), stroke=r * 1.4))
    if glow: circle(c, x, y, r * 1.8, "#ffb347", glow * a, blur=r * 0.6)
    rng = random.Random(4); pts = []
    for k in range(14):
        an = k / 14 * 2 * math.pi + t * 0.3
        rr = r * rng.uniform(0.8, 1.05); pts.append((x + math.cos(an) * rr, y + math.sin(an) * rr))
    c.drawPath(poly(pts), paint("#6e6253", a))
    for k in range(4):
        an = rng.random() * 6.28; d = rng.random() * r * 0.6
        circle(c, x + math.cos(an) * d, y + math.sin(an) * d, r * rng.uniform(0.1, 0.22), "#4f463c", a)
    c.drawPath(poly(pts), paint(shader=rad(x - r * 0.4, y - r * 0.4, r * 1.8, [(0, "#ffffff", 0.18), (1, "#000000", 0.5)]), a=a))

# ---------- generic scenes ----------
def motif_art(c, W, H, t, u, motif, cx, cy, s=1.0, a=1.0):
    if motif == "log":
        log(c, cx, cy, 520 * u * s, 70 * u * s, moss=0.7)
        for k, dx in enumerate((-160, -40, 90)):
            shelf(c, cx + dx * u * s, cy - 45 * u * s, (38 - k * 6) * u * s)
        mushroom(c, cx - 230 * u * s, cy + 70 * u * s, 50 * u * s); mushroom(c, cx + 180 * u * s, cy + 75 * u * s, 36 * u * s, "#e0a43a")
    elif motif == "asteroid":
        geo.globe(c, cx, cy + 40 * u * s, int(190 * u * s), rot=95, tilt=15)
        asteroid(c, cx + 230 * u * s, cy - 170 * u * s, 30 * u * s, t, trail=1.0, ang=-35 + 180, glow=0.4)
    elif motif == "sea":
        bb = (-6, 29.5, 37, 46.5)
        rr = geo.map_rect(bb, cx, cy, width=min(W * 0.92, 1250 * u * s))
        c.save(); c.clipRect(skia.Rect.MakeXYWH(*rr))
        geo.draw_map(c, bb, rr, land="#d9c48a", sea="#1f6fd1", rim="#f1ece0", rim_w=(8 + 6 * math.sin(t)) * u * s)
        c.restore()
        rrect(c, rr[0], rr[1], rr[2], rr[3], 16 * u, "#ffffff", 0.8, stroke=4 * u)

def title2(c, W, H, t, S):
    u = S.u; o = S.opts; motif = o.get("motif")
    if motif == "log":
        forest_bg(c, W, H, t, u, dark=0.55, hy=0.3)
        c.drawRect(skia.Rect.MakeXYWH(0, 0.55 * H, W, 0.45 * H), paint(shader=lin(0, 0.55 * H, 0, H, [(0, "#0b1030", 0), (1, "#0b1030", 0.8)])))
        motif_art(c, W, H, t, u, motif, W / 2, 0.47 * H, 0.85 if not S.P else 0.6)
    else:
        space_bg(c, W, H, t, 1, seed=2, drift=(-6, 0))
        motif_art(c, W, H, t, u, motif, W / 2, 0.36 * H, 0.85 if not S.P else 0.6)
    sz = fit(o["l1"], W * 0.9, 110 * u, 900)
    p1 = prog(t, 0.15, 0.4); p2 = prog(t, 0.6, 0.4)
    text(c, o["l1"], W / 2, 0.72 * H + (1 - eout(p1)) * 30 * u, sz, "#ffffff", p1, w=900, shadow=14)
    sz2 = fit(o["l2"], W * 0.9, 125 * u, 900)
    text(c, o["l2"], W / 2, 0.72 * H + 135 * u + (1 - eout(p2)) * 30 * u, sz2, ACCENT, p2, w=900, shadow=14)

def card2(c, W, H, t, S):
    o = dict(S.opts)
    lab = o.get("label", "")
    # reuse batch-1 card but with a custom label
    u = S.u; txt = o["text"]
    space_bg(c, W, H, t, 0.6, seed=3, drift=(-10, 0))
    c.save(); z = 1 + 0.05 * t / S.dur; c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-W / 2, -H / 2)
    lines_ = [txt]; big = 190 * u
    if tw(txt, big, 900) > W * 0.86 and " " in txt:
        ws = txt.split(" ")
        best = min(range(1, len(ws)), key=lambda k: max(tw(" ".join(ws[:k]), big, 900), tw(" ".join(ws[k:]), big, 900)))
        lines_ = [" ".join(ws[:best]), " ".join(ws[best:])]
    p = eout(prog(t, 0.0, 0.35))
    chip(c, lab, W / 2, H / 2 - (150 if len(lines_) == 1 else 245) * u, prog(t, 0.05, 0.4), 30 * u, bg="#1b2250")
    for k, ln in enumerate(lines_):
        sz = fit(ln, W * 0.86, big, 900)
        yy = H / 2 + (k - (len(lines_) - 1) / 2) * sz * 1.02 + (1 - p) * 40 * u
        text(c, ln, W / 2, yy, sz, "#ffffff" if k == 0 else ACCENT, p, w=900, shadow=18)
    lw = W * 0.3 * eout(prog(t, 0.2, 0.6)); yb = H / 2 + (120 if len(lines_) == 1 else 220) * u
    line(c, W / 2 - lw / 2, yb, W / 2 + lw / 2, yb, ACCENT, 8 * u)
    c.restore()

def end2(c, W, H, t, S):
    u = S.u; o = S.opts
    if o.get("motif") == "log": forest_bg(c, W, H, t, u, dark=0.7, hy=0.5)
    else: space_bg(c, W, H, t, 1, seed=34, drift=(-8, 0))
    c.save(); lay = c.saveLayerAlpha(None, 150)
    motif_art(c, W, H, t, u, o.get("motif"), W / 2, 0.66 * H, 0.7)
    c.restore(); c.restore()
    p = prog(t, 0.2, 0.5)
    sz = fit(o["q"], W * 0.9, 96 * u, 900)
    text(c, o["q"], W / 2, 0.18 * H, sz, ACCENT, p, w=900, shadow=14)
    text(c, "Tell me in the comments", W / 2, 0.29 * H, 44 * u, "#ffffff", prog(t, 0.6, 0.5), w=600, fam="Inter")

def end_short2(c, W, H, t, S):
    u = S.u; o = S.opts
    if o.get("motif") == "log": forest_bg(c, W, H, t, u, dark=0.5, hy=0.3)
    else: space_bg(c, W, H, t, 1, seed=35, drift=(-8, 0))
    motif_art(c, W, H, t, u, o.get("motif"), W / 2, 0.42 * H, 0.75)
    p = prog(t, 0.1, 0.4)
    sz = fit(o["top"], W * 0.9, 100 * u, 900)
    text(c, o["top"], W / 2, 0.13 * H, sz, "#ffffff", p, w=900, shadow=14, stroke=8 * u, stroke_col="#0b1030")
    chip(c, "FULL VIDEO ON THE CHANNEL", W / 2, 0.21 * H, vis(t, S.lt(0, 0.4)), 44 * u, bg=ACCENT, fg="#0b1030", a=1)

def hook_text(c, W, H, t, S, y=0.3):
    o = S.opts
    if o.get("hook"):
        u = S.u; sz = fit(o["hook"], W * 0.9, 92 * u, 900)
        text(c, o["hook"], W / 2, y * H, sz, "#ffffff", eout(t / 0.25), w=900, stroke=10 * u, stroke_col="#0b1030")

def badge(c, W, H, t, S):
    o = S.opts
    if o.get("badge"):
        chip(c, o["badge"], W / 2, 0.14 * H if S.P else 0.1 * H, prog(t, 0.0, 0.35), 50 * S.u, bg=ACCENT, fg="#0b1030", a=1)

SCENES = {"title2": title2, "card2": card2, "end2": end2, "end_short2": end_short2}

# ---------- layout / timing ----------
def stage(S):
    return (S.W / 2, 0.40 * S.H, 0.92) if S.P else (S.W / 2, 0.5 * S.H, 1.0)

def beats(S, E):
    """time for beat (i, f) of a scene written for E lines; squeezes into fewer lines for Shorts."""
    n = S.n()
    if n >= E: return lambda i, f=0.0: S.lt(i, f)
    if n == 0: return lambda i, f=0.0: S.dur * (i + f) / E
    def g(i, f=0.0):
        x = (i + f) / E * n; k = min(int(x), n - 1)
        return S.lt(k, x - k)
    return g

def chips(c, t, items, x, y, gap, u, size=34, align="c"):
    """items: (t_on, t_off or None, text, dot)"""
    k = 0
    for (a, b, txt, dot) in items:
        chip(c, txt, x, y + k * gap, vis(t, a, b), size * u, dot=dot, align=align); k += 1

def xfade(t, t0, d=0.5): return ease(prog(t, t0, d))

# ---------- icons ----------
def xmark(c, x, y, s, a=1.0, colr="#ff4d4d"):
    if a <= 0: return
    p = eback(clamp(a)); s *= p
    line(c, x - s, y - s, x + s, y + s, colr, s * 0.35, clamp(a)); line(c, x - s, y + s, x + s, y - s, colr, s * 0.35, clamp(a))

def check(c, x, y, s, a=1.0, colr="#4cd964"):
    if a <= 0: return
    p = skia.Path(); p.moveTo(x - s, y); p.lineTo(x - s * 0.3, y + s * 0.7); p.lineTo(x + s, y - s * 0.7)
    c.drawPath(p, paint(colr, clamp(a), stroke=s * 0.35))

def padlock(c, x, y, s, a=1.0, colr="#ffc93c"):
    p = skia.Path(); p.addArc(skia.Rect.MakeXYWH(x - s * 0.45, y - s * 1.1, s * 0.9, s * 1.0), 180, 180)
    c.drawPath(p, paint("#d8dee9", a, stroke=s * 0.16, cap="butt"))
    line(c, x - s * 0.45, y - s * 0.6, x - s * 0.45, y - s * 0.2, "#d8dee9", s * 0.16, a, cap="butt")
    line(c, x + s * 0.45, y - s * 0.6, x + s * 0.45, y - s * 0.2, "#d8dee9", s * 0.16, a, cap="butt")
    rrect(c, x - s * 0.7, y - s * 0.25, s * 1.4, s * 1.05, s * 0.18, colr, a)
    circle(c, x, y + s * 0.2, s * 0.13, "#0b1030", a); rect(c, x - s * 0.05, y + s * 0.2, s * 0.1, s * 0.3, "#0b1030", a)

def coal_lump(c, x, y, s, a=1.0, glow=0.0, seed=2):
    rng = random.Random(seed); pts = []
    for k in range(9):
        an = k / 9 * 2 * math.pi; r = s * rng.uniform(0.75, 1.0)
        pts.append((x + math.cos(an) * r * 1.2, y + math.sin(an) * r * 0.8))
    if glow: circle(c, x, y, s * 1.6, "#ff7a1a", glow * 0.5 * a, blur=s * 0.5)
    c.drawPath(poly(pts), paint("#16161c", a))
    for k in range(3):
        an = rng.random() * 6.28
        c.drawPath(poly([(x + math.cos(an) * s * 0.3, y + math.sin(an) * s * 0.2), (x + math.cos(an + 0.6) * s * 0.7, y + math.sin(an + 0.6) * s * 0.5),
                         (x + math.cos(an + 0.3) * s * 0.75, y + math.sin(an + 0.3) * s * 0.3)]), paint("#4a4a5a", a * 0.8))
    if glow:
        c.drawPath(poly(pts), paint("#ff8a2a", glow * a, stroke=s * 0.08))

def leaf_icon(c, x, y, s, colr="#4caf50", a=1.0):
    p = skia.Path(); p.moveTo(x, y + s); p.quadTo(x - s * 0.9, y, x, y - s); p.quadTo(x + s * 0.9, y, x, y + s)
    c.drawPath(p, paint(colr, a)); line(c, x, y + s * 1.2, x, y - s * 0.7, mix(colr, "#000000", 0.35), s * 0.08, a)

def apple(c, x, y, s, a=1.0):
    circle(c, x - s * 0.3, y, s * 0.62, "#e8443a", a); circle(c, x + s * 0.3, y, s * 0.62, "#e8443a", a)
    line(c, x, y - s * 0.5, x + s * 0.1, y - s * 0.95, "#5b3e2a", s * 0.1, a); leaf_icon(c, x + s * 0.35, y - s * 0.8, s * 0.25, a=a)

def fishbone(c, x, y, s, a=1.0, colr="#e8eef8"):
    line(c, x - s, y, x + s * 0.6, y, colr, s * 0.08, a)
    for k in range(5):
        xx = x - s * 0.7 + k * s * 0.28
        line(c, xx, y - s * 0.35, xx + s * 0.1, y, colr, s * 0.06, a); line(c, xx, y + s * 0.35, xx + s * 0.1, y, colr, s * 0.06, a)
    c.drawPath(poly([(x + s * 0.6, y - s * 0.35), (x + s * 1.1, y), (x + s * 0.6, y + s * 0.35)]), paint(colr, a, stroke=s * 0.07))
    c.drawPath(poly([(x - s, y), (x - s * 1.35, y - s * 0.35), (x - s * 1.35, y + s * 0.35)]), paint(colr, a))

def microbe(c, x, y, s, t=0.0, a=1.0, colr="#7ee081"):
    c.save(); c.translate(x, y); c.rotate(20 + 10 * math.sin(t * 2))
    rrect(c, -s, -s * 0.42, 2 * s, s * 0.84, s * 0.42, colr, a)
    for k in range(4):
        line(c, -s + k * s * 0.6, s * 0.4, -s + k * s * 0.6 + math.sin(t * 6 + k) * s * 0.2, s * 0.8, colr, s * 0.08, a)
    circle(c, -s * 0.3, -s * 0.05, s * 0.15, mix(colr, "#000000", 0.35), a); c.restore()

def fungus_icon(c, x, y, s, a=1.0):
    shelf(c, x, y, s, a=a)
    for k in range(5):
        line(c, x - s * 0.6 + k * s * 0.3, y + s * 0.1, x - s * 0.7 + k * s * 0.35, y + s * 0.6, "#f4f0e6", s * 0.05, a * 0.8)

def beetle(c, x, y, s, a=1.0, colr="#2d3a2a"):
    oval(c, x, y, s * 0.5, s * 0.7, colr, a); circle(c, x, y - s * 0.75, s * 0.3, colr, a)
    line(c, x, y - s * 0.6, x, y + s * 0.65, mix(colr, "#ffffff", 0.2), s * 0.05, a)
    for k in (-0.35, 0, 0.35):
        line(c, x - s * 0.45, y + k * s, x - s * 0.85, y + k * s + s * 0.15, colr, s * 0.08, a)
        line(c, x + s * 0.45, y + k * s, x + s * 0.85, y + k * s + s * 0.15, colr, s * 0.08, a)

def pigeon(c, x, y, s, a=1.0, colr="#9aa4b8"):
    oval(c, x, y, s * 0.5, s * 0.3, colr, a); circle(c, x + s * 0.45, y - s * 0.25, s * 0.18, colr, a)
    c.drawPath(poly([(x + s * 0.6, y - s * 0.27), (x + s * 0.75, y - s * 0.22), (x + s * 0.6, y - s * 0.18)]), paint("#e0a43a", a))
    c.drawPath(poly([(x - s * 0.4, y - s * 0.05), (x - s * 0.95, y - s * 0.1), (x - s * 0.9, y + s * 0.1)]), paint(colr, a))
    c.drawPath(poly([(x - s * 0.1, y - s * 0.15), (x - s * 0.5, y - s * 0.75), (x + s * 0.2, y - s * 0.2)]), paint(mix(colr, "#000000", 0.2), a))

def house(c, x, y, s, wall="#e9d8b8", roof="#8a4b2f", a=1.0):
    rect(c, x - s * 0.5, y - s * 0.6, s, s * 0.6, wall, a)
    c.drawPath(poly([(x - s * 0.62, y - s * 0.58), (x, y - s * 1.02), (x + s * 0.62, y - s * 0.58)]), paint(roof, a))
    rect(c, x - s * 0.1, y - s * 0.32, s * 0.2, s * 0.32, roof, a); rect(c, x + s * 0.22, y - s * 0.45, s * 0.16, s * 0.14, "#9fd3ff", a)

def barn(c, x, y, s, a=1.0):
    rect(c, x - s * 0.6, y - s * 0.7, s * 1.2, s * 0.7, "#b23a2a", a)
    c.drawPath(poly([(x - s * 0.7, y - s * 0.68), (x - s * 0.35, y - s * 1.05), (x + s * 0.35, y - s * 1.05), (x + s * 0.7, y - s * 0.68)]), paint("#7a2a1f", a))
    rect(c, x - s * 0.22, y - s * 0.45, s * 0.44, s * 0.45, "#f4ead8", a)
    line(c, x - s * 0.22, y - s * 0.45, x + s * 0.22, y, "#b23a2a", s * 0.05, a); line(c, x + s * 0.22, y - s * 0.45, x - s * 0.22, y, "#b23a2a", s * 0.05, a)

def fence(c, x0, x1, y, s, a=1.0, colr="#d9b48a"):
    xx = x0
    while xx <= x1:
        c.drawPath(poly([(xx - s * 0.08, y), (xx - s * 0.08, y - s * 0.55), (xx, y - s * 0.65), (xx + s * 0.08, y - s * 0.55), (xx + s * 0.08, y)]), paint(colr, a))
        xx += s * 0.32
    rect(c, x0, y - s * 0.45, x1 - x0, s * 0.07, colr, a); rect(c, x0, y - s * 0.2, x1 - x0, s * 0.07, colr, a)

def clock(c, x, y, r, frac, a=1.0, colr=ACCENT):
    circle(c, x, y, r, "#0b1030", 0.9 * a); circle(c, x, y, r, "#ffffff", a, stroke=r * 0.08)
    p = skia.Path(); p.moveTo(x, y); p.arcTo(skia.Rect.MakeXYWH(x - r * 0.85, y - r * 0.85, r * 1.7, r * 1.7), -90, 360 * clamp(frac), False); p.close()
    c.drawPath(p, paint(colr, a * 0.85))
    an = -math.pi / 2 + 2 * math.pi * frac
    line(c, x, y, x + math.cos(an) * r * 0.8, y + math.sin(an) * r * 0.8, "#ffffff", r * 0.07, a)

def donut(c, x, y, r, frac, colr, a=1.0, bg="#ffffff", label=None, u=1.0, sub=None):
    c.drawCircle(x, y, r, paint(bg, 0.14 * a, stroke=r * 0.28))
    p = skia.Path(); p.addArc(skia.Rect.MakeXYWH(x - r, y - r, 2 * r, 2 * r), -90, 360 * clamp(frac))
    c.drawPath(p, paint(colr, a, stroke=r * 0.28, cap="butt"))
    if label: text(c, label, x, y - (r * 0.1 if sub else 0), r * 0.42, "#ffffff", a, w=900)
    if sub: text(c, sub, x, y + r * 0.3, r * 0.16, "#cfe3ff", a, w=700, fam="Inter")

def pangea_globe(c, x, y, R, rot=10, tilt=-10, cap_s=None, a=1.0, haze=0.0):
    geo.globe(c, x, y, int(R), rot=rot, tilt=tilt, kind="pangea", cap_s=cap_s, a=a, haze=haze)

class Layer:
    def __init__(self, c, a): self.c, self.a = c, clamp(a)
    def __enter__(self):
        if self.a < 0.995: self.c.saveLayerAlpha(None, int(255 * self.a))
        else: self.c.save()
        return self.a > 0.003
    def __exit__(self, *e): self.c.restore()

def phase(t, a, b=None, d=0.5):
    v = xfade(t, a, d) if a is not None else 1.0
    if b is not None: v *= 1 - xfade(t, b + d, 0.08)  # stay opaque until the next phase has faded in on top
    return v

def big_text(c, W, H, s, y, p, u, colr="#ffffff", size=120, maxw=0.88):
    sz = fit(s, W * maxw, size * u, 900)
    text(c, s, W / 2, y + (1 - eout(p)) * 30 * u, sz, colr, clamp(p), w=900, shadow=14, stroke=6 * u, stroke_col="#0b1030")

def counter_chip(c, label, x, y, p, u, size=40):
    chip(c, label, x, y, p, size * u, bg="#0b1030")

def soil(c, W, y, H, a=1.0, colr="#4a3424"):
    c.drawRect(skia.Rect.MakeLTRB(0, y, W, H), paint(shader=lin(0, y, 0, H, [(0, colr, a), (1, mix(colr, "#000000", 0.5), a)])))

def dark_bg(c, W, H, top="#0f1a2b", bot="#1b2a40"):
    fill_bg(c, W, H, top, bot)
