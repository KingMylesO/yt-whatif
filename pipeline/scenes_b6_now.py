"""Batch 06 happening-now Shorts: ESA's Hera at Dimorphos (nw6_hera) and supernova SN 2026ahvu (nw6_sn).

Two separate looks:
  * Hera: warm charcoal space, grey rubble-pile asteroids (procedural boulders), gold-foil spacecraft, amber accents.
  * Supernova: deep navy, a cyan/blue barred spiral galaxy (NGC 1433-like ring + bar) and a white-hot flash with spikes.
Shorts only: all content lives in the 0.215H..0.585H band (captions at 0.635H, badge 0.14H, hook 0.2H, CTA 0.75H).
Scenes draw straight in pixel coordinates of the 1080x1920 frame.
"""
import math, random
import numpy as np
import skia
from common2 import *
import geo
import scenes_b3_kit as kit

GOLD, GOLD_D = "#f2c14e", "#9c6a1c"
AMBER = "#ffb547"
ROCK_L, ROCK_D = "#a29a90", "#34302d"
HBG_T, HBG_B = "#07070b", "#1d1916"
NBG_T, NBG_B = "#01040f", "#071a44"
CYAN = "#7fe3ff"; HOT = "#fffaf0"; RED = "#ff5a5a"; GREEN = "#6fffb0"
CHIP_H = "#2a2118"; CHIP_N = "#0c1d4a"

BAND0, BAND1 = 0.215, 0.585

def band_clip(c, W, H):
    c.clipRect(skia.Rect.MakeLTRB(0, BAND0 * H, W, BAND1 * H))

def TX(c, s, x, y, size, colr="#ffffff", a=1.0, w=900, maxw=980, align="c", fam="Inter Display"):
    if a <= 0.003: return
    size *= 1.2; maxw = min(maxw * 1.2, 1000)
    if align == "c": maxw = min(maxw, 2 * min(x, 1080 - x) - 30)
    elif align == "l": maxw = min(maxw, 1080 - x - 30)
    sz = fit(s, maxw, size, w, fam)
    text(c, s, x, y, sz, colr, clamp(a), w=w, fam=fam, align=align, shadow=10, stroke=6, stroke_col="#05060c")
    text(c, s, x, y, sz, colr, clamp(a), w=w, fam=fam, align=align)

def CH(c, s, x, y, p, size=34, bg=CHIP_H, **kw):
    """chip scaled up for phone viewing, kept inside the frame (1080 wide)."""
    size *= 1.3
    def width(sz):
        f = sz * 1.15; return tw(s, f, 700, "Inter") + 2 * f * 0.62 + (f * 0.9 if kw.get("dot") else 0)
    while width(size) > 1000 and size > 12: size *= 0.95
    wdt = width(size); al = kw.get("align", "c")
    left = x - wdt / 2 if al == "c" else (x if al == "l" else x - wdt)
    x += max(0, 30 - left) - max(0, left + wdt - 1050)
    chip(c, s, x, y, p, size, bg=bg, **kw)

# ------------------------------------------------------------------ backgrounds
_IMG = {}
def _bg_img(W, H, kind):
    k = ("bg", W, H, kind)
    if k not in _IMG:
        surf = skia.Surface(W, H); cc = surf.getCanvas()
        if kind == "h":
            fill_bg(cc, W, H, HBG_T, HBG_B)
            cc.drawPaint(paint(shader=rad(W * 0.85, H * 0.28, H * 0.55, [(0, "#ffb060", 0.13), (0.5, "#6a3a10", 0.05), (1, "#000000", 0)])))
            cc.drawPaint(paint(shader=rad(W * 0.1, H * 0.62, H * 0.5, [(0, "#3a3a52", 0.18), (1, "#000000", 0)])))
        else:
            fill_bg(cc, W, H, NBG_T, NBG_B)
            cc.drawPaint(paint(shader=rad(W * 0.5, H * 0.4, H * 0.6, [(0, "#1a3a8a", 0.28), (0.6, "#0a1a50", 0.08), (1, "#000000", 0)])))
            cc.drawPaint(paint(shader=rad(W * 0.15, H * 0.15, H * 0.45, [(0, "#5a2a7a", 0.14), (1, "#000000", 0)])))
        _IMG[k] = surf.makeImageSnapshot()
    return _IMG[k]

def bg_h(c, W, H, t, S=None):
    c.drawImage(_bg_img(W, H, "h"), 0, 0)
    stars(c, W, H, t, 0.75, seed=61, drift=(-4, 0))

def bg_n(c, W, H, t, S=None):
    c.drawImage(_bg_img(W, H, "n"), 0, 0)
    stars(c, W, H, t, 0.95, seed=67, drift=(0, -3))

# ------------------------------------------------------------------ rubble-pile asteroids
def rock_img(R, seed, sq=1.0, ridge=0.0, light=ROCK_L, dark=ROCK_D):
    R = int(R); k = ("rock", R, seed, sq, ridge)
    if k in _IMG: return _IMG[k]
    size = int(R * 2.7); surf = skia.Surface(size, size); c = surf.getCanvas(); c.clear(skia.ColorTRANSPARENT)
    cx = cy = size / 2; rng = random.Random(seed)
    harm = [(j, rng.uniform(0.01, 0.045) / (1 + 0.15 * j), rng.random() * 6.28) for j in range(2, 9)]
    pts = []
    for i in range(72):
        th = 2 * math.pi * i / 72
        r = R * (1 + sum(a_ * math.sin(j * th + ph) for j, a_, ph in harm))
        r *= 1 + ridge * abs(math.cos(th)) ** 5
        pts.append((cx + math.cos(th) * r, cy + math.sin(th) * r * sq))
    path = poly(pts)
    c.drawPath(path, paint("#000000", 0.5, blur=R * 0.05))
    c.save(); c.clipPath(path, doAntiAlias=True)
    c.drawPaint(paint(shader=rad(cx - 0.45 * R, cy - 0.55 * R * sq, 2.0 * R, [(0, light, 1), (0.55, mix(light, dark, 0.5), 1), (1, dark, 1)])))
    for _ in range(int(R * 3)):  # gravel
        x = cx + rng.uniform(-1.1, 1.1) * R; y = cy + rng.uniform(-1.1, 1.1) * R * sq
        circle(c, x, y, rng.uniform(0.6, 1.6) * max(1, R / 120), rng.choice(["#000000", "#ffffff"]), rng.uniform(0.05, 0.18))
    bl = []
    for _ in range(int(40 + R * 0.35)):
        ang = rng.random() * 6.28; d = rng.random() ** 0.6
        s = R * rng.uniform(0.025, 0.11) * (1.2 if rng.random() < 0.12 else 1.0)
        bl.append((cx + math.cos(ang) * d * R, cy + math.sin(ang) * d * R * sq, s, rng.uniform(-0.12, 0.12)))
    bl.sort(key=lambda b: b[1])
    for x, y, s, tone in bl:
        base = mix(mix(light, dark, 0.45), "#ffffff" if tone > 0 else "#000000", abs(tone))
        oval(c, x + s * 0.3, y + s * 0.35, s * 1.05, s * 0.85, "#000000", 0.45)
        oval(c, x, y, s, s * 0.82, base, 1)
        oval(c, x - s * 0.3, y - s * 0.3, s * 0.45, s * 0.33, "#ffffff", 0.22)
    c.drawPaint(paint(shader=lin(cx - R, cy - R, cx + R, cy + R, [(0, "#000000", 0), (0.5, "#000000", 0.05), (1, "#000000", 0.78)])))
    c.restore()
    c.drawPath(path, paint("#fff1d8", 0.12, stroke=max(1.5, R * 0.012)))
    _IMG[k] = surf.makeImageSnapshot()
    return _IMG[k]

def rock(c, x, y, R, seed, sq=1.0, ridge=0.0, rot=0.0, a=1.0):
    if R < 3 or a <= 0.003: return
    Rq = max(8, int(R) // 6 * 6)
    img = rock_img(Rq, seed, sq, ridge); sc = R / Rq
    p = skia.Paint(); p.setAlphaf(clamp(a))
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(sc, sc)
    c.drawImage(img, -img.width() / 2, -img.height() / 2, skia.SamplingOptions(skia.FilterMode.kLinear), p)
    c.restore()

def didymos(c, x, y, R, rot=0.0, a=1.0): rock(c, x, y, R, 7, sq=0.84, ridge=0.16, rot=rot, a=a)
def dimorphos(c, x, y, R, rot=0.0, a=1.0): rock(c, x, y, R, 23, sq=0.78, ridge=0.0, rot=rot, a=a)

def binary(c, cx, cy, Rd, t, ang, a=1.0, orbit=True, tilt=0.26):
    """Didymos at centre, Dimorphos on a tilted orbit (separation ~2.95 Didymos radii; Dimorphos ~0.19 the size)."""
    rx = 2.95 * Rd; ry = rx * tilt; Rm = Rd * 0.2
    mx, my = cx + math.cos(ang) * rx, cy + math.sin(ang) * ry
    if orbit:
        c.drawOval(skia.Rect.MakeLTRB(cx - rx, cy - ry, cx + rx, cy + ry), paint(AMBER, 0.35 * a, stroke=2.5, dash=([10, 10], -t * 20)))
    back = math.sin(ang) < 0
    if back: dimorphos(c, mx, my, Rm * (0.93 + 0.07 * math.sin(ang)), a=a)
    didymos(c, cx, cy, Rd, rot=-6, a=a)
    if not back: dimorphos(c, mx, my, Rm * (0.93 + 0.07 * math.sin(ang)), a=a)
    return mx, my, Rm

# ------------------------------------------------------------------ spacecraft
def solar_wing(c, x, y, w, h, a=1.0, cells=4):
    rrect(c, x, y, w, h, 3, "#14203f", a)
    for i in range(1, cells):
        line(c, x + w * i / cells, y + 2, x + w * i / cells, y + h - 2, "#5a7ec4", 1.6, a * 0.8)
    line(c, x + 2, y + h / 2, x + w - 2, y + h / 2, "#5a7ec4", 1.6, a * 0.8)
    c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), paint(shader=lin(x, y, x + w, y + h, [(0, "#9fc4ff", 0.35), (0.5, "#9fc4ff", 0.0), (1, "#9fc4ff", 0.15)]), a=a))
    rrect(c, x, y, w, h, 3, "#c9d6f0", a * 0.6, stroke=2)

def hera(c, x, y, s, rot=0.0, a=1.0, glint=0.0):
    """ESA Hera-like probe: gold-foil box, two 2-panel solar wings, high-gain dish. s = body half-width."""
    if a <= 0.003 or s <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot)
    wl, wh = s * 3.6, s * 1.15
    line(c, -s * 1.0, 0, -s * 1.35, 0, "#c8c8c8", s * 0.12, a)
    line(c, s * 1.0, 0, s * 1.35, 0, "#c8c8c8", s * 0.12, a)
    solar_wing(c, -s * 1.35 - wl, -wh / 2, wl, wh, a, cells=6)
    solar_wing(c, s * 1.35, -wh / 2, wl, wh, a, cells=6)
    body = skia.Rect.MakeXYWH(-s, -s * 0.9, 2 * s, 1.8 * s)
    c.drawRRect(skia.RRect.MakeRectXY(body, s * 0.08, s * 0.08), paint(shader=lin(-s, -s, s, s, [(0, "#ffe6a0", 1), (0.45, GOLD, 1), (1, GOLD_D, 1)]), a=a))
    rng = random.Random(3)
    for _ in range(9):
        x0 = rng.uniform(-s, s); y0 = rng.uniform(-s * 0.9, s * 0.9)
        line(c, x0, y0, x0 + rng.uniform(-0.5, 0.5) * s, y0 + rng.uniform(-0.3, 0.3) * s, "#fff4c8", max(1, s * 0.03), a * 0.45)
    oval(c, 0, -s * 0.9, s * 0.75, s * 0.22, "#eef0f4", a)
    oval(c, 0, -s * 0.95, s * 0.62, s * 0.15, "#c9ccd4", a)
    line(c, 0, -s * 0.95, 0, -s * 1.3, "#dfe2e8", max(1.5, s * 0.06), a)
    rrect(c, -s * 0.55, s * 0.25, s * 0.45, s * 0.4, s * 0.06, "#2a2a30", a)
    circle(c, -s * 0.33, s * 0.45, s * 0.12, "#7fb0ff", a * 0.9)
    c.restore()
    if glint > 0:
        circle(c, x + s * 0.4, y - s * 0.4, s * 0.9, "#fff3c0", 0.35 * glint * a, blur=s * 0.5)
        for ang in (0, 90):
            c.save(); c.translate(x + s * 0.4, y - s * 0.4); c.rotate(ang + 20)
            line(c, -s * 1.6 * glint, 0, s * 1.6 * glint, 0, "#fff8e0", 2, 0.7 * glint * a)
            c.restore()

def dart_probe(c, x, y, s, a=1.0, ang=0.0):
    """Small silver box with two long thin roll-out solar arrays."""
    c.save(); c.translate(x, y); c.rotate(ang)
    for sgn in (-1, 1):
        rrect(c, -s * 0.35, sgn * s * 0.6 - (s * 2.4 if sgn < 0 else 0), s * 0.7, s * 2.4, s * 0.1, "#1a2a52", a)
        rrect(c, -s * 0.35, sgn * s * 0.6 - (s * 2.4 if sgn < 0 else 0), s * 0.7, s * 2.4, s * 0.1, "#9fb8e8", a * 0.6, stroke=1.5)
    rrect(c, -s * 0.6, -s * 0.6, s * 1.2, s * 1.2, s * 0.12, "#d8dce4", a)
    circle(c, s * 0.15, 0, s * 0.35, "#8a909c", a)
    c.restore()

def cubesat(c, x, y, s, a=1.0, colr="#e8e2d0", rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot)
    solar_wing(c, -s * 2.3, -s * 0.45, s * 1.6, s * 0.9, a, cells=2)
    solar_wing(c, s * 0.7, -s * 0.45, s * 1.6, s * 0.9, a, cells=2)
    rrect(c, -s * 0.7, -s * 0.7, s * 1.4, s * 1.4, s * 0.15, colr, a)
    rrect(c, -s * 0.45, -s * 0.45, s * 0.9, s * 0.9, s * 0.1, GOLD, a * 0.85)
    c.restore()

# ------------------------------------------------------------------ Earth (cached globe image)
def earth_img(R, rot=160, tilt=18):
    R = max(4, int(R) // 4 * 4); k = ("earth", R, rot, tilt)
    if k not in _IMG:
        arr = geo.globe_img(R, rot, tilt)
        _IMG[k] = skia.Image.fromarray(arr, colorType=skia.kRGBA_8888_ColorType, alphaType=skia.kPremul_AlphaType)
    return _IMG[k], R

def earth_d(c, x, y, R, rot=160, a=1.0, glow=1.0):
    img, Rq = earth_img(R, rot)
    if glow > 0: circle(c, x, y, R * 1.08, "#6fb6ff", 0.3 * glow * a, blur=R * 0.07)
    p = skia.Paint(); p.setAlphaf(clamp(a))
    c.drawImageRect(img, skia.Rect.MakeXYWH(x - R, y - R, 2 * R, 2 * R), skia.SamplingOptions(skia.FilterMode.kLinear), p)

# ------------------------------------------------------------------ small icons
def qmark(c, x, y, s, colr=AMBER, a=1.0):
    TX(c, "?", x, y, s, colr, a, maxw=s * 2)

def clock_face(c, x, y, r, hh, mm, a=1.0, colr=AMBER, strike=0.0):
    circle(c, x, y, r, "#120e0a", 0.92 * a); circle(c, x, y, r, colr, a, stroke=r * 0.07)
    for k in range(12):
        an = k / 12 * 2 * math.pi
        line(c, x + math.sin(an) * r * 0.78, y - math.cos(an) * r * 0.78, x + math.sin(an) * r * 0.9, y - math.cos(an) * r * 0.9, "#ffffff", r * 0.035, a * 0.7)
    am = mm / 60 * 2 * math.pi; ah = (hh % 12 + mm / 60) / 12 * 2 * math.pi
    line(c, x, y, x + math.sin(ah) * r * 0.5, y - math.cos(ah) * r * 0.5, "#ffffff", r * 0.08, a)
    line(c, x, y, x + math.sin(am) * r * 0.75, y - math.cos(am) * r * 0.75, colr, r * 0.05, a)
    circle(c, x, y, r * 0.07, "#ffffff", a)
    if strike > 0:
        line(c, x - r * 1.05, y + r * 1.05, x - r * 1.05 + 2.1 * r * eout(strike), y + r * 1.05 - 2.1 * r * eout(strike), RED, r * 0.09, a)

def ejecta(c, x, y, t, t0, ang=-160, spread=55, n=110, reach=420, a=1.0, seed=5):
    if t < t0: return
    q = t - t0; rng = random.Random(seed)
    for i in range(n):
        an = math.radians(ang + rng.uniform(-spread, spread) * rng.random() ** 0.5)
        sp = rng.uniform(0.25, 1.0); d = reach * sp * eout(clamp(q / 2.2)) + reach * 0.06 * q
        r = rng.uniform(1.5, 5.5) * (1 if rng.random() > 0.1 else 2)
        circle(c, x + math.cos(an) * d, y + math.sin(an) * d, r, mix("#d8c8b0", AMBER, rng.random() * 0.4), a * (0.9 - 0.25 * sp) * clamp(1.4 - q / 5))
    circle(c, x + math.cos(math.radians(ang)) * reach * 0.25 * eout(clamp(q / 2)), y + math.sin(math.radians(ang)) * reach * 0.25 * eout(clamp(q / 2)),
           reach * 0.35 * eout(clamp(q / 2)), "#e8d8c0", 0.18 * a * clamp(1.5 - q / 4), blur=40)

def flash(c, x, y, q, R=120, colr=HOT, a=1.0):
    """impact / explosion flash, q = seconds since start"""
    if q < 0: return
    f = clamp(1 - q / 0.9)
    if f > 0:
        circle(c, x, y, R * (0.4 + 1.6 * eout(clamp(q / 0.5))), colr, 0.85 * f * a, blur=R * 0.25)
        circle(c, x, y, R * 0.3 * (1 + q), "#ffffff", f * a)
    ring = clamp(q / 1.2)
    if ring < 1: circle(c, x, y, R * (0.5 + 2.2 * eout(ring)), colr, (1 - ring) * 0.7 * a, stroke=6)

# ================================================================== HERA SHORT
def nw6_hera(c, W, H, t, S):
    o = S.opts; mode = o.get("mode"); u = S.u
    L = lambda i, f=0.0: S.lt(i, f)
    bg_h(c, W, H, t)
    cy = 0.40 * H
    c.save(); band_clip(c, W, H)
    if mode == "intro":
        z = 1.0 + 0.06 * t / S.dur
        c.save(); c.translate(W / 2, cy + 30); c.scale(z, z); c.translate(-W / 2, -(cy + 30))
        mx, my, Rm = binary(c, W / 2 - 10, cy + 40, 160, t, 0.6 + t * 0.35)
        c.restore()
        hp = eout(prog(t, 0.9, 1.2))
        hx, hy = lerp(W + 160, W * 0.78, hp), lerp(0.25 * H, 0.29 * H, hp)
        hera(c, hx, hy, 34, rot=-12, glint=vis(t, 1.4) * (0.6 + 0.4 * math.sin(t * 5)))
        sc = vis(t, L(0, 0.55))
        if sc > 0:
            mxz = W / 2 + (mx - W / 2) * z; myz = (cy + 30) + (my - cy - 30) * z
            c.drawPath(poly([(hx, hy + 20), (mxz - 70, myz - 10), (mxz + 70, myz + 25)]), paint(AMBER, 0.16 * sc))
            circle(c, mxz, myz, 44 + 6 * math.sin(t * 6), AMBER, 0.8 * sc, stroke=4)
        CH(c, "CHECKING THE DAMAGE", W / 2, 0.545 * H, vis(t, L(0, 0.62)), 38, dot=AMBER)
    elif mode == "dart":
        ti = L(0, 0.55)
        didymos(c, 130, 0.36 * H, 220, rot=8, a=0.4)
        dx, dy = 700, 0.40 * H
        shake = 6 * math.sin(t * 60) * clamp(1 - (t - ti) / 0.4) if t > ti else 0
        dimorphos(c, dx + shake, dy, 165, rot=-4)
        if t < ti:
            q = prog(t, 0.2, ti - 0.2); px = lerp(-120, dx - 150, ein(q) * 0.85 + q * 0.15); py = lerp(dy - 240, dy - 40, q)
            ang = math.degrees(math.atan2(dy - 40 - (dy - 240), dx - 150 + 120))
            c.drawLine(px - 260 * math.cos(math.radians(ang)), py - 260 * math.sin(math.radians(ang)), px, py,
                       paint(shader=lin(px - 260 * math.cos(math.radians(ang)), py - 260 * math.sin(math.radians(ang)), px, py, [(0, "#9fc4ff", 0), (1, "#dfe9ff", 0.8)]), stroke=10))
            dart_probe(c, px, py, 20, ang=ang)
            if px > 140: CH(c, "NASA's DART", px + 10, py - 95, vis(t, 0.4), 30, bg="#18213f")
        else:
            ejecta(c, dx - 150, dy - 40, t, ti, ang=-150, reach=520)
            flash(c, dx - 150, dy - 40, t - ti, 150, colr="#fff3d0")
            if t > ti + 0.2:
                rr = 22 + 10 * min(1, (t - ti))
                circle(c, dx - 140, dy - 34, rr, "#1a1410", 0.6)
        CH(c, "580 KG AT 6.1 KM/S", W / 2, 0.545 * H, vis(t, ti + 0.35), 36, dot=AMBER)
        stamp(c, "ON PURPOSE", 760, 0.27 * H, prog(t, L(0, 0.86), 0.35), 0.75, color=AMBER, size=88, rot=-8)
    elif mode == "orbit":
        ang = -math.pi / 2 + t * 0.9
        mx, my, Rm = binary(c, W / 2, 0.33 * H, 100, t, ang, tilt=0.42)
        y2 = 0.485 * H; p1 = vis(t, L(0, 0.15)); p2 = vis(t, L(0, 0.55))
        clock_face(c, 270, y2, 90, 11, 55, p1, colr="#c8c0b4", strike=prog(t, L(0, 0.55), 0.4))
        TX(c, "BEFORE: 11 H 55 MIN", 270, y2 + 122, 32, "#d8d0c4", p1, w=800, maxw=440)
        clock_face(c, 810, y2, 90, 11, 23, p2, colr=AMBER)
        TX(c, "AFTER: ≈11 H 23 MIN", 810, y2 + 122, 32, AMBER, p2, w=800, maxw=440)
        if p2 > 0: arrow(c, 390, y2, 690, y2, AMBER, 6, p2)
        CH(c, "DIMORPHOS", mx, my - Rm - 40, vis(t, L(0, 0.05)), 28, bg="#2a2118")
    elif mode == "arrive":
        sz = 1 + 0.05 * t / S.dur
        binary(c, 300, 0.33 * H, 70, t, 2.2 + t * 0.4, a=0.95)
        hp = eout(prog(t, 0.0, 2.0))
        hx = lerp(W + 250, 760, hp); hy = lerp(0.36 * H, 0.44 * H, hp)
        hera(c, hx, hy, 62 * sz, rot=-8, glint=0.5 + 0.5 * math.sin(t * 3))
        CH(c, "ESA's HERA", hx, hy - 120, vis(t, 0.6), 34, bg="#18213f", dot=GOLD)
        pd = vis(t, L(0, 0.6))
        if pd > 0:
            y3 = 0.545 * H
            line(c, 300, y3, 300 + (hx - 300 - 120) * eout(pd), y3, "#ffffff", 3, 0.7 * pd, dash=([14, 10], 0))
            TX(c, "≈ 25–30 KM AWAY", (300 + hx - 120) / 2, y3 - 34, 40, "#ffffff", pd, maxw=520)
    elif mode == "gravity":
        tsplit = L(0, 0.47)
        a1 = 1 - ease(prog(t, tsplit, 0.3))
        if a1 > 0.003:
            with Layer(c, a1):
                earth_d(c, 250, 0.355 * H, 150)
                dimorphos(c, 830, 0.355 * H, 110)
                TX(c, "1×", 250, 0.49 * H, 70, "#ffffff", vis(t, 0.3), maxw=300)
                TX(c, "1/200,000", 830, 0.49 * H, 64, AMBER, vis(t, 1.0), maxw=400)
                TX(c, "GRAVITY", W / 2, 0.355 * H, 44, "#ffffff", vis(t, 0.2), w=800, maxw=300)
                CH(c, "A FEATHER-LIGHT WORLD", W / 2, 0.555 * H, vis(t, 1.8), 34, dot=AMBER)
        a2 = ease(prog(t, tsplit + 0.2, 0.35))
        if a2 > 0.003:
            with Layer(c, a2):
                ccx, ccy = W / 2, 0.385 * H
                binary(c, ccx, ccy, 60, t, t * 0.6, orbit=False)
                hw, hh = 400, 190
                pth = [(ccx - hw, ccy - hh), (ccx + hw, ccy - hh), (ccx + hw, ccy + hh), (ccx - hw, ccy + hh)]
                c.drawPath(poly(pth), paint(GOLD, 0.5, stroke=3, dash=([16, 12], -t * 15)))
                for (px, py) in pth: circle(c, px, py, 9, AMBER, 0.9)
                q = ((t - tsplit) * 0.09 + 0.1) % 1.0
                per = 4 * 0  # unused
                seg = q * 4; k = int(seg); f = seg - k
                x0, y0 = pth[k]; x1, y1 = pth[(k + 1) % 4]
                hera(c, lerp(x0, x1, f), lerp(y0, y1, f), 22, glint=0.6)
                TX(c, "12 CM/S", W / 2, ccy + hh + 70, 58, GOLD, vis(t, L(0, 0.75)), maxw=500)
                CH(c, "'RECTANGULAR ORBIT'", W / 2, ccy - hh - 45, vis(t, tsplit + 0.3), 30, dot=GOLD)
    elif mode == "job":
        tj = L(1, 0.0)
        dx, dy = 300, 0.385 * H
        dimorphos(c, dx, dy, 190, rot=-3)
        hera(c, 300 + 240, 0.25 * H, 26, rot=-20, glint=0.4)
        sweep = math.sin(t * 1.6) * 120
        line(c, 540, 0.25 * H + 10, dx + sweep, dy - 60, "#ff6060", 2.5, 0.7)
        circle(c, dx + sweep, dy - 60, 7, "#ff6060", 0.9)
        items = [("WEIGH IT: MASS?", L(1, 0.05)), ("A CRATER?", L(1, 0.45)), ("OR RESHAPED?", L(1, 0.72))]
        for i, (s_, t0) in enumerate(items):
            CH(c, s_, 790, 0.30 * H + i * 0.085 * H, vis(t, t0), 32, dot=[GOLD, AMBER, "#ff8a5a"][i])
        rp = prog(t, L(1, 0.72), 0.8)
        if rp > 0:
            c.drawOval(skia.Rect.MakeLTRB(dx - 190 * (1 + 0.15 * rp), dy - 150 * (1 - 0.1 * rp), dx + 190 * (1 + 0.15 * rp), dy + 150 * (1 - 0.1 * rp)),
                       paint("#ff8a5a", 0.7 * rp, stroke=4, dash=([12, 10], -t * 25)))
        cp = vis(t, L(1, 0.45))
        if cp > 0:
            circle(c, dx - 60, dy - 20, 46, AMBER, cp, stroke=4); qmark(c, dx - 60, dy - 20, 52, AMBER, cp)
        if t < tj:
            TX(c, "MEASURING THE CRASH SITE", W / 2, 0.555 * H, 36, "#ffffff", vis(t, 0.2), w=800, maxw=900)
    elif mode == "cubesat":
        hx, hy = 220, 0.27 * H
        hera(c, hx, hy, 30, rot=10, glint=0.3)
        dx, dy = 760, 0.42 * H
        dimorphos(c, dx, dy, 170, rot=5)
        for i, (nm, t0, tgt) in enumerate([("MILANI", 0.3, (520, 0.31 * H)), ("JUVENTAS", 0.9, (560, 0.47 * H))]):
            q = eout(prog(t, t0, 1.6))
            if q <= 0: continue
            x = lerp(hx + 30, tgt[0], q); y = lerp(hy + 30, tgt[1], q)
            cubesat(c, x, y, 16, rot=10 + 30 * q)
            CH(c, nm, x, y + 50, vis(t, t0 + 0.8), 26, bg="#18213f")
        rp = prog(t, L(0, 0.55), 0.5)
        if rp > 0:
            jx, jy = 560, 0.47 * H
            for k in range(4):
                q = ((t * 0.9 + k / 4) % 1.0)
                rr = 30 + q * 220
                p = skia.Path(); p.addArc(skia.Rect.MakeLTRB(jx - rr, jy - rr, jx + rr, jy + rr), -40, 80)
                c.drawPath(p, paint(GREEN, rp * (1 - q) * 0.9, stroke=4))
            # cut-away: interior rubble, unknown
            c.save(); pth = skia.Path(); pth.addCircle(dx, dy, 120 * eout(rp)); c.clipPath(pth, doAntiAlias=True)
            circle(c, dx, dy, 130, "#1a1612", 0.95)
            rng = random.Random(9)
            for _ in range(40):
                circle(c, dx + rng.uniform(-120, 120), dy + rng.uniform(-120, 120), rng.uniform(8, 26), mix("#5a524a", "#2a2622", rng.random()), 0.9)
            c.restore()
            circle(c, dx, dy, 120 * eout(rp), GREEN, 0.6 * rp, stroke=3)
            qmark(c, dx, dy, 110, GREEN, vis(t, L(0, 0.75)))
    elif mode == "unknown":
        dx, dy = W / 2 - 170, 0.385 * H
        dimorphos(c, dx, dy, 190, rot=-3, a=0.45)
        c.drawCircle(dx, dy, 220, paint("#07070b", 0.35, blur=40))
        qa = vis(t, 0.2)
        circle(c, dx - 40, dy - 20, 80 + 6 * math.sin(t * 3), AMBER, qa, stroke=5, dash=([16, 12], -t * 20))
        qmark(c, dx - 40, dy - 20, 120, AMBER, qa)
        # calendar
        cp = eback(prog(t, L(0, 0.55), 0.5)); cx_, cy_ = 820, 0.39 * H
        if cp > 0:
            c.save(); c.translate(cx_, cy_); c.scale(cp, cp)
            rrect(c, -130, -140, 260, 280, 26, "#f4efe6"); rrect(c, -130, -140, 260, 80, 26, "#d8413a"); rect(c, -130, -90, 260, 30, "#d8413a")
            text(c, "NOV", 0, -100, 46, "#ffffff", w=900)
            text(c, "25", 0, 35, 140, "#1a1410", w=900)
            for sx in (-70, 70): rrect(c, sx - 8, -160, 16, 44, 8, "#8a8a8a")
            c.restore()
            TX(c, "FIRST CLOSE-UPS DUE", cx_, cy_ + 200, 36, "#ffffff", vis(t, L(0, 0.7)), w=800, maxw=460)
    elif mode == "playbook":
        ex, ey = 230, 0.45 * H
        earth_d(c, ex, ey, 120)
        sx, sy = 1000, 0.25 * H
        ti = L(0, 0.35)
        q = prog(t, 0.0, ti)
        ax, ay = lerp(sx, 640, q), lerp(sy, 0.35 * H, q)
        line(c, sx, sy, ex + 60, ey - 30, RED, 3, 0.55 * (1 - vis(t, ti + 0.3)), dash=([14, 10], 0))
        if t >= ti:
            flash(c, 640, 0.35 * H, t - ti, 60, colr="#fff3d0")
            dq = eout(prog(t, ti, 1.6))
            pth = skia.Path(); pth.moveTo(640, 0.35 * H); pth.quadTo(420, 0.34 * H, 380 - 40 * dq, 0.25 * H)
            c.drawPath(pth, paint(GREEN, 0.8 * vis(t, ti + 0.2), stroke=4, dash=([14, 10], -t * 30)))
            ax, ay = lerp(640, 380, dq), lerp(0.35 * H, 0.255 * H, dq)
            CH(c, "NUDGED → MISSES", W / 2 + 120, 0.52 * H, vis(t, ti + 0.6), 34, bg="#123a2a", dot=GREEN)
        else:
            dq = prog(t, ti - 0.8, 0.8)
            dart_probe(c, lerp(380, 620, dq), lerp(0.47 * H, 0.36 * H, dq), 14, a=vis(t, ti - 0.9), ang=-40)
        asteroid(c, ax, ay, 34, t)
    c.restore()
    if mode == "intro": kit.hook(c, W, H, t, S)

# ================================================================== SUPERNOVA SHORT
def galaxy_img(R):
    """Barred spiral with an inner ring (NGC 1433-like), face-on, drawn once."""
    R = int(R); k = ("gal", R)
    if k in _IMG: return _IMG[k]
    size = int(R * 2.4); surf = skia.Surface(size, size); c = surf.getCanvas(); c.clear(skia.ColorTRANSPARENT)
    cx = cy = size / 2; rng = np.random.default_rng(14)
    c.drawCircle(cx, cy, R * 1.05, paint(shader=rad(cx, cy, R * 1.05, [(0, "#9fc8ff", 0.25), (0.5, "#3a6ac8", 0.08), (1, "#000000", 0)])))
    def dots(xs, ys, rs, colr, al):
        p = paint(colr, al)
        for x, y, r in zip(xs, ys, rs): c.drawCircle(float(cx + x), float(cy + y), float(r), p)
    # outer spiral arms (log spiral starting from ring ends)
    for arm in range(2):
        th0 = arm * math.pi
        n = 1400
        s_ = rng.random(n) ** 0.8
        th = th0 + s_ * 3.4
        rr = R * (0.42 + 0.55 * s_)
        jit = rng.normal(0, 0.05 * R, (2, n)) * (0.6 + s_)
        xs = np.cos(th) * rr + jit[0]; ys = np.sin(th) * rr + jit[1]
        dots(xs, ys, rng.uniform(0.6, 2.2, n), "#8fc4ff", 0.35)
        m = 70; idx = rng.choice(n, m)
        dots(xs[idx], ys[idx], rng.uniform(2, 4.5, m), "#ff8fc8", 0.45)
        idx = rng.choice(n, 120)
        dots(xs[idx], ys[idx], rng.uniform(1.5, 3, 120), "#e8f4ff", 0.7)
    # inner ring
    n = 1600; th = rng.uniform(0, 2 * math.pi, n); rr = R * 0.42 + rng.normal(0, 0.03 * R, n)
    dots(np.cos(th) * rr * 1.08, np.sin(th) * rr * 0.92, rng.uniform(0.6, 2.4, n), "#a8d8ff", 0.4)
    idx = rng.choice(n, 90); dots((np.cos(th) * rr * 1.08)[idx], (np.sin(th) * rr * 0.92)[idx], rng.uniform(2, 5, 90), "#ff9ad0", 0.5)
    # bar
    n = 1500; x = rng.normal(0, 0.18 * R, n); y = rng.normal(0, 0.05 * R, n)
    dots(x, y, rng.uniform(0.8, 2.4, n), "#ffe6b8", 0.35)
    c.drawOval(skia.Rect.MakeLTRB(cx - R * 0.42, cy - R * 0.1, cx + R * 0.42, cy + R * 0.1), paint("#ffe2b0", 0.25, blur=R * 0.06))
    c.drawCircle(cx, cy, R * 0.16, paint(shader=rad(cx, cy, R * 0.16, [(0, "#fffbe8", 1), (0.4, "#ffe2a8", 0.7), (1, "#ffd090", 0)])))
    _IMG[k] = surf.makeImageSnapshot()
    return _IMG[k]

def galaxy(c, x, y, R, rot=0.0, incl=0.62, a=1.0):
    img = galaxy_img(300); sc = R / 300
    p = skia.Paint(); p.setAlphaf(clamp(a))
    c.save(); c.translate(x, y); c.scale(sc, sc * incl); c.rotate(rot)
    c.drawImage(img, -img.width() / 2, -img.height() / 2, skia.SamplingOptions(skia.FilterMode.kLinear), p)
    c.restore()

def sn_pos(x, y, R, rot, incl=0.62):
    """supernova sits right of and slightly below the core (galaxy-frame offset rotated with it)."""
    ox, oy = 0.2 * R, 0.1 * R
    an = math.radians(rot)
    rx = ox * math.cos(an) - oy * math.sin(an); ry = ox * math.sin(an) + oy * math.cos(an)
    return x + rx, y + ry * incl

def star_burst(c, x, y, s, a=1.0, t=0.0, colr=HOT, halo="#9fd8ff"):
    if a <= 0.003 or s <= 0: return
    circle(c, x, y, s * 3.2, halo, 0.25 * a, blur=s * 1.5)
    circle(c, x, y, s * 1.3, colr, 0.7 * a, blur=s * 0.5)
    for k, ang in enumerate((0, 90, 45, 135)):
        L_ = s * (5.5 if k < 2 else 2.6) * (1 + 0.06 * math.sin(t * 4 + k))
        c.save(); c.translate(x, y); c.rotate(ang)
        c.drawPath(poly([(-L_, 0), (0, -s * 0.12), (L_, 0), (0, s * 0.12)]), paint(colr, 0.8 * a))
        c.restore()
    circle(c, x, y, s * 0.55, "#ffffff", a)

def telescope(c, x, y, s, a=1.0):
    c.save(); c.translate(x, y)
    line(c, 0, 0, -s * 0.5, s * 0.9, "#c8d4e8", s * 0.06, a); line(c, 0, 0, s * 0.5, s * 0.9, "#c8d4e8", s * 0.06, a); line(c, 0, 0, 0, s * 0.95, "#c8d4e8", s * 0.06, a)
    c.rotate(-35)
    rrect(c, -s * 0.5, -s * 0.16, s * 1.3, s * 0.32, s * 0.08, "#e8eef8", a)
    rrect(c, s * 0.8, -s * 0.2, s * 0.14, s * 0.4, s * 0.04, "#9fb0cc", a)
    rrect(c, -s * 0.7, -s * 0.08, s * 0.22, s * 0.16, s * 0.04, "#9fb0cc", a)
    c.restore()

def white_dwarf(c, x, y, r, a=1.0):
    circle(c, x, y, r * 2.4, "#bfe4ff", 0.3 * a, blur=r * 0.9)
    c.drawCircle(x, y, r, paint(shader=rad(x - r * 0.3, y - r * 0.3, r * 1.3, [(0, "#ffffff", 1), (1, "#a8d4ff", 1)]), a=a))

def nw6_sn(c, W, H, t, S):
    o = S.opts; mode = o.get("mode")
    L = lambda i, f=0.0: S.lt(i, f)
    bg_n(c, W, H, t)
    cy = 0.40 * H
    c.save(); band_clip(c, W, H)
    if mode == "intro":
        z = 1.0 + 0.08 * t / S.dur; rot = -20 + t * 1.5
        gx, gy = W / 2, 0.41 * H
        c.save(); c.translate(gx, gy); c.scale(z, z); c.translate(-gx, -gy)
        galaxy(c, gx, gy, 440, rot)
        sx, sy = sn_pos(gx, gy, 440, rot)
        q = t - 0.7
        if q > 0:
            flash(c, sx, sy, q, 120, colr="#dff2ff")
            star_burst(c, sx, sy, 14 + 6 * eout(clamp(q / 0.6)), 1, t)
        c.restore()
        tp = vis(t, L(0, 0.55))
        telescope(c, 170, 0.51 * H, 90, tp)
        CH(c, "SMALL TELESCOPE", 300, 0.555 * H, tp, 28, bg=CHIP_N, align="l")
    elif mode == "find":
        tf = L(0, 0.4)
        a1 = 1 - ease(prog(t, tf, 0.3))
        if a1 > 0.003:
            with Layer(c, a1):
                gx, gy = W / 2, 0.40 * H
                for i in range(7):
                    line(c, 0, 0.23 * H + i * 0.05 * H, W, 0.23 * H + i * 0.05 * H, "#3a6ac8", 1.5, 0.35)
                for i in range(7):
                    line(c, i * W / 6, 0.215 * H, i * W / 6, 0.585 * H, "#3a6ac8", 1.5, 0.35)
                sx_ = (t * 420) % (W + 300) - 150
                c.drawRect(skia.Rect.MakeLTRB(sx_ - 120, 0.215 * H, sx_, 0.585 * H), paint(shader=lin(sx_ - 120, 0, sx_, 0, [(0, CYAN, 0), (1, CYAN, 0.28)])))
                line(c, sx_, 0.215 * H, sx_, 0.585 * H, CYAN, 3, 0.8)
                CH(c, "ATLAS SKY SURVEY", W / 2, 0.30 * H, vis(t, 0.2), 40, bg=CHIP_N, dot=CYAN)
                TX(c, "SCANS THE WHOLE SKY", W / 2, 0.40 * H, 50, "#ffffff", vis(t, 0.6), maxw=900)
        a2 = ease(prog(t, tf + 0.2, 0.35))
        if a2 > 0.003:
            with Layer(c, a2):
                for i, (lab, xx) in enumerate([("BEFORE", 285), ("AFTER", 795)]):
                    fy = 0.375 * H; fs = 220
                    rrect(c, xx - fs, fy - fs, 2 * fs, 2 * fs, 16, "#02060f", 0.95)
                    c.save(); c.clipRect(skia.Rect.MakeLTRB(xx - fs, fy - fs, xx + fs, fy + fs))
                    galaxy(c, xx, fy, 190, -20)
                    if i == 1:
                        sx, sy = sn_pos(xx, fy, 190, -20)
                        pa = vis(t, tf + 0.5)
                        star_burst(c, sx, sy, 8, pa, t)
                        circle(c, sx, sy, 34, "#ffe066", pa, stroke=4)
                    c.restore()
                    rrect(c, xx - fs, fy - fs, 2 * fs, 2 * fs, 16, "#9fc4ff", 0.7, stroke=3)
                    TX(c, lab, xx, fy - fs + 36, 34, "#ffffff" if i == 0 else "#ffe066", 1, w=800, maxw=300)
                CH(c, "GALAXY NGC 1433 · HOROLOGIUM", W / 2, 0.545 * H, vis(t, L(0, 0.7)), 32, bg=CHIP_N, dot=CYAN)
    elif mode == "wd":
        tb = L(0, 0.6)
        wx, wy = 720, 0.38 * H
        if t < tb + 0.25:
            sx, sy = 240, 0.36 * H; sr = 150
            # companion star with tidal bulge toward the dwarf
            c.drawCircle(sx, sy, sr * 1.25, paint("#ff9a4a", 0.25, blur=40))
            c.save(); c.translate(sx, sy)
            c.drawPath(poly([(0, -sr * 0.95), (sr * 1.45, 0), (0, sr * 0.95)]), paint(shader=rad(0, 0, sr * 1.5, [(0, "#ffb070", 1), (1, "#d8602a", 1)])))
            c.restore()
            c.drawCircle(sx, sy, sr, paint(shader=rad(sx - sr * 0.3, sy - sr * 0.3, sr * 1.4, [(0, "#ffd8a0", 1), (0.6, "#ff9a4a", 1), (1, "#c8501f", 1)])))
            # stream + disk
            pth = skia.Path(); pth.moveTo(sx + sr * 1.4, sy); pth.cubicTo(500, sy + 10, 620, wy + 70, wx - 20, wy + 40)
            c.drawPath(pth, paint("#ffb070", 0.85, stroke=12))
            for k in range(14):
                q = ((t * 0.5 + k / 14) % 1)
                pt = (lerp(sx + sr * 1.4, wx - 20, q), lerp(sy, wy + 40, q ** 1.5))
                circle(c, pt[0], pt[1], 5, "#fff0c8", 0.8)
            c.save(); c.translate(wx, wy); c.rotate(-12)
            for k, (r_, colr) in enumerate([(120, "#ff9a4a"), (90, "#ffd090"), (62, "#fff0d0")]):
                oval(c, 0, 0, r_, r_ * 0.28, colr, 0.45, stroke=10)
            c.restore()
            white_dwarf(c, wx, wy, 26)
            CH(c, "COMPANION STAR", sx, 0.52 * H, vis(t, 0.2, tb), 28, bg=CHIP_N, dot="#ff9a4a")
            CH(c, "WHITE DWARF", wx, 0.27 * H, vis(t, 0.5, tb), 28, bg=CHIP_N, dot=CYAN)
        if t >= tb:
            q = t - tb
            flash(c, wx, wy, q, 110, colr="#e8f6ff")
            sh = 60 + 230 * eout(clamp(q / 2.5))
            circle(c, wx, wy, sh, "#bfe4ff", 0.6 * clamp(1.6 - q / 2), stroke=10)
            circle(c, wx, wy, sh * 0.92, "#ffffff", 0.12 * clamp(1.6 - q / 2), blur=30)
            star_burst(c, wx, wy, 26 * clamp(1.4 - q / 3) + 6, 1, t)
            TX(c, "BOOM", wx - 150, 0.53 * H, 70, HOT, vis(t, tb + 0.3), maxw=500)
    elif mode == "peak":
        x0, x1, y0, y1 = 130, 990, 0.245 * H, 0.52 * H
        rect(c, x0, y0, x1 - x0, y1 - y0, "#02060f", 0.7)
        def X(day): return lerp(x0 + 30, x1 - 30, (day - 1) / 29)
        def Y(mag): return lerp(y1 - 30, y0 + 40, (17.5 - mag) / 7.5)
        rect(c, X(18), y0, X(23) - X(18), y1 - y0, CYAN, 0.12)
        line(c, x0, y1, x1, y1, "#9fc4ff", 3, 0.8)
        for d in (2, 9, 16, 23, 30):
            TX(c, f"{d} NOV", X(d), y1 + 30, 26, "#cfe3ff", 1, w=700, maxw=140)
        pp = eout(prog(t, 0.2, max(0.6, L(0, 0.8) - 0.2)))
        pts = []
        for i in range(81):
            d = 2 + i * 0.35
            if d > 2 + 28 * pp: break
            m = 11.3 + 5.7 * (1 - clamp((d - 2) / 18.5)) ** 2.2 + 0.08 * max(0, d - 20.5) ** 1.6
            pts.append((X(d), Y(m)))
        if len(pts) > 1:
            c.drawPath(poly(pts, close=False), paint("#ffffff", 0.95, stroke=6))
        circle(c, X(2), Y(17), 9, "#ffe066", vis(t, 0.2))
        TX(c, "FOUND AT MAG 17", X(2) + 10, Y(17) - 40, 26, "#ffe066", vis(t, 0.3), w=800, align="l", maxw=360)
        pk = vis(t, L(0, 0.35))
        TX(c, "PEAK ≈ MAG 10.5–12", X(20.5), y0 + 26, 30, CYAN, pk, w=800, maxw=420)
        nowp = vis(t, L(0, 0.5))
        line(c, X(23), y0 + 50, X(23), y1, "#ffe066", 3, nowp, dash=([10, 8], 0))
        CH(c, "NOW", X(23) + 70, Y(13.6), nowp, 26, bg="#ffe066", fg="#0b1030")
        TX(c, "SCHEMATIC · BRIGHTER ↑", x0 + 20, y1 - 20, 22, "#8fa8d0", 0.9, w=700, align="l", maxw=360)
        CH(c, "SOUTHERN SKY", W / 2, 0.565 * H, vis(t, L(0, 0.75)), 30, bg=CHIP_N, dot=CYAN)
    elif mode == "candle":
        tsplit = L(0, 0.5)
        a1 = 1 - ease(prog(t, tsplit, 0.3))
        if a1 > 0.003:
            with Layer(c, a1):
                for i in range(5):
                    p = vis(t, 0.15 + i * 0.35)
                    x = 160 + i * 190; y = 0.37 * H; s = 34 * (1 - i * 0.17)
                    star_burst(c, x, y, s * 0.5, p * (1 - i * 0.17), t)
                    TX(c, ["NEAR", "", "", "", "FAR"][i], x, 0.46 * H, 30, "#cfe3ff", p if i in (0, 4) else 0, w=800, maxw=200)
                TX(c, "SAME BLAST, DIMMER = FARTHER", W / 2, 0.27 * H, 42, "#ffffff", vis(t, 0.5), maxw=980)
        a2 = ease(prog(t, tsplit + 0.2, 0.35))
        if a2 > 0.003:
            with Layer(c, a2):
                q = t - tsplit; z = 1 + 0.12 * q
                rng = random.Random(3)
                for k in range(15):
                    gx = rng.uniform(-1, 1) * 440; gy = rng.uniform(-1, 1) * 250
                    x = W / 2 + gx * z; y = 0.39 * H + gy * z
                    galaxy(c, x, y, rng.uniform(40, 72), rng.uniform(0, 180), incl=rng.uniform(0.4, 0.9), a=0.9)
                    if k % 3 == 0:
                        arrow(c, x + gx * 0.05, y + gy * 0.05, x + gx * 0.16, y + gy * 0.16, CYAN, 3, 0.6)
                CH(c, "THE EXPANDING UNIVERSE", W / 2, 0.545 * H, vis(t, tsplit + 0.3), 34, bg=CHIP_N, dot=CYAN)
    elif mode == "near":
        t1 = L(1, 0.0); tz = L(1, 0.35)
        sx, sy = W / 2, 0.39 * H
        if t < tz + 0.5:
            a1 = 1 - ease(prog(t, tz, 0.3))
            with Layer(c, a1):
                earth_d(c, sx, sy, 150)
                c.drawCircle(sx, sy, 172, paint("#7fd0ff", 0.55, stroke=6))
                c.drawCircle(sx, sy, 172, paint("#7fd0ff", 0.25, stroke=18, blur=10))
                CH(c, "OUR OZONE LAYER", sx, 0.545 * H, vis(t, 0.3), 32, bg=CHIP_N, dot="#7fd0ff")
                if t > t1:
                    star_burst(c, 900, 0.26 * H, 12, vis(t, t1 + 0.1), t)
                    qmark(c, 950, 0.30 * H, 70, "#ffe066", vis(t, t1 + 0.3))
        a2 = ease(prog(t, tz + 0.2, 0.35))
        if a2 > 0.003:
            with Layer(c, a2):
                gp = eout(prog(t, tz, 1.2)); R50 = 250 * gp
                if R50 > 1:
                    c.drawCircle(sx, sy, R50, paint(RED, 0.10))
                    c.drawCircle(sx, sy, R50, paint(RED, 0.8, stroke=4, dash=([14, 10], -t * 20)))
                    line(c, sx, sy, sx + R50, sy, "#ffffff", 3, 0.8)
                circle(c, sx, sy, 16, "#ffd166"); circle(c, sx, sy, 40, "#ffd166", 0.3, blur=14)
                TX(c, "SUN & EARTH", sx, sy + 56, 26, "#ffffff", vis(t, tz + 0.2), w=800, maxw=300)
                TX(c, "50 LIGHT-YEARS", sx, sy - 285, 34, "#ffffff", vis(t, tz + 0.7), w=900, maxw=400)
                CH(c, "OZONE DAMAGE ZONE (NASA)", W / 2, 0.545 * H, vis(t, L(1, 0.7)), 32, bg="#3a1020", dot=RED)
                rng = random.Random(8)
                for k in range(6):
                    an = rng.uniform(0, 6.28); d = rng.uniform(320, 470)
                    star_burst(c, sx + math.cos(an) * d * 1.05, sy + math.sin(an) * d * 0.62, 3, 0.6 * gp, t)
    elif mode == "nearest":
        x0, x1, yb = 100, 980, 0.40 * H
        def X(ly): return lerp(x0, x1, ly / 200)
        p = eout(prog(t, 0.1, 0.8))
        line(c, x0, yb, x0 + (x1 - x0) * p, yb, "#cfe3ff", 6, 0.9)
        rrect(c, X(0), yb - 26, (X(50) - X(0)) * p, 52, 10, RED, 0.35 * p)
        for ly in (0, 50, 100, 150, 200):
            line(c, X(ly), yb - 14, X(ly), yb + 14, "#cfe3ff", 3, p)
            TX(c, f"{ly}", X(ly), yb + 50, 28, "#cfe3ff", p, w=700, maxw=100)
        TX(c, "LIGHT-YEARS FROM EARTH", W / 2, yb + 100, 28, "#8fa8d0", p, w=700, maxw=600)
        TX(c, "DANGER ZONE", X(25), yb - 60, 28, RED, vis(t, 0.5), w=800, maxw=240)
        circle(c, X(0), yb, 12, "#ffd166");
        mp = vis(t, L(0, 0.35))
        if mp > 0:
            ph = t * 2.2
            white_dwarf(c, X(150) + math.cos(ph) * 22, yb - 110 + math.sin(ph) * 8, 11, mp)
            white_dwarf(c, X(150) - math.cos(ph) * 22, yb - 110 - math.sin(ph) * 8, 8, mp)
            line(c, X(150), yb - 80, X(150), yb - 18, "#ffe066", 3, mp)
            TX(c, "NEAREST KNOWN TYPE Ia CANDIDATE", X(150) - 60, yb - 175, 28, "#ffe066", mp, w=800, maxw=640)
        CH(c, "NOWHERE NEAR CLOSE ENOUGH", W / 2, 0.555 * H, vis(t, L(0, 0.8)), 32, bg="#123a2a", dot=GREEN)
    elif mode == "unknown":
        x0, x1, yb = 120, 960, 0.43 * H
        def X(mly): return lerp(x0, x1, mly / 70)
        line(c, x0, yb, x1, yb, "#cfe3ff", 5, 0.9)
        for m in (0, 30, 60):
            line(c, X(m), yb - 14, X(m), yb + 14, "#cfe3ff", 3)
            TX(c, f"{m}" if m else "EARTH", X(m), yb + 48, 28, "#cfe3ff", 1, w=700, maxw=160)
        TX(c, "MILLION LIGHT-YEARS", X(45), yb + 95, 26, "#8fa8d0", 1, w=700, maxw=460)
        ph = 0.5 - 0.5 * math.cos(t * 1.6)
        gx = lerp(X(30), X(60), ph)
        galaxy(c, gx, yb - 150, 170, -20 + t * 3)
        for m in (30, 60):
            circle(c, X(m), yb, 10, "#ffe066", vis(t, 0.4))
        qmark(c, gx + 190, yb - 220, 70, "#ffe066", vis(t, 0.3))
        CH(c, "~30 OR ~60 MILLION?", W / 2, 0.255 * H, vis(t, L(0, 0.45)), 32, bg=CHIP_N, dot="#ffe066")
        CH(c, "NEXT TO YOUNG STARS? NOT CONFIRMED", W / 2, 0.565 * H, vis(t, L(0, 0.8)), 26, bg=CHIP_N, dot=CYAN)
    c.restore()
    if mode == "intro": kit.hook(c, W, H, t, S)

# ================================================================== end card (both Shorts -> b6_mercury)
def mercury_motif(c, W, H, t, S, cx, cy, s):
    R = 200 * s
    circle(c, cx + R * 1.3, cy - R * 0.6, R * 1.6, "#ffcf6a", 0.35, blur=R * 0.5)
    circle(c, cx + R * 1.3, cy - R * 0.6, R * 0.75, "#fff2c0", 0.9, blur=R * 0.1)
    c.drawCircle(cx, cy, R, paint(shader=rad(cx + R * 0.4, cy - R * 0.4, R * 1.6, [(0, "#d8cfc4", 1), (0.6, "#8a8078", 1), (1, "#2a2622", 1)])))
    rng = random.Random(41)
    c.save(); pth = skia.Path(); pth.addCircle(cx, cy, R); c.clipPath(pth, doAntiAlias=True)
    for _ in range(26):
        an = rng.random() * 6.28; d = rng.random() ** 0.7 * R * 0.9; r = R * rng.uniform(0.04, 0.14)
        x, y = cx + math.cos(an) * d, cy + math.sin(an) * d
        circle(c, x, y, r, "#5a524a", 0.55); circle(c, x + r * 0.2, y + r * 0.2, r * 0.75, "#b8aea2", 0.25)
    c.drawPaint(paint(shader=lin(cx + R, cy - R, cx - R, cy + R, [(0, "#000000", 0), (0.55, "#000000", 0.1), (1, "#000000", 0.75)])))
    c.restore()

def nw6_endshort(c, W, H, t, S):
    look = S.opts.get("look", "h")
    bg = bg_n if look == "n" else bg_h
    kit.end_short(c, W, H, t, S, lambda c, W, H, t, S: bg(c, W, H, t), mercury_motif, dict(accent=AMBER if look != "n" else CYAN))

SCENES = {k: v for k, v in globals().items() if k.startswith("nw6_") and callable(v)}
