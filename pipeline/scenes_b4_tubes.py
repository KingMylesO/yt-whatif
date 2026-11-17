"""Batch 04 scenes: What If the Transistor Was Never Invented? (+ tubes teaser, moth and chip-blackout Shorts).

Look: dark walnut/sepia, glowing amber filaments, brass and copper, cream type. Signature prop: a hand-drawn
glass vacuum tube. Every scene draws on a virtual 1920x1080 stage (Stage); in Shorts the stage is scaled into
the 0.255H..0.58H band and text sizes are multiplied by ts (1.75) so chips stay readable on a phone.
Static art (backgrounds, tube racks, documents) is cached into images so long renders stay fast.
"""
from common2 import *
import scenes_b3_kit as kit

WAL_T, WAL_B = "#140b06", "#2a170c"
AMBER, ORANGE = "#ffb347", "#ff7a1a"
BRASS, COPPER = "#c9853a", "#8a5a2b"
CREAM = "#f6e7c8"
INK = "#1d2a4a"
ELEC = "#9fd8ff"
CHIPBG = "#3a2212"
RED = "#ff5a4a"
GREEN = "#7bd88f"
PAL = dict(accent=AMBER, chip="#4a2a14", title2=ACCENT)
VW, VH = 1920, 1080

# ------------------------------------------------------------------ stage + helpers
class Stage:
    def __init__(self, c, S): self.c, self.S = c, S
    def __enter__(self):
        c, S = self.c, self.S; c.save()
        if S.P:
            sc = S.W * 0.96 / VW
            top = 0.255 * S.H + (0.325 * S.H - VH * sc) / 2
            c.translate(S.W * 0.02, top); c.scale(sc, sc)
        else:
            sc = S.W / VW; c.scale(sc, sc)
        return 1.75 if S.P else 1.0
    def __exit__(self, *e): self.c.restore()

def C(c, s, x, y, p, ts, size=34, **kw):
    kw.setdefault("bg", CHIPBG)
    chip(c, s, x, y, p, size * ts, **kw)

def T(c, s, x, y, size, ts, colr="#ffffff", a=1.0, w=900, maxw=1800, **kw):
    sz = fit(s, maxw, size * ts, w)
    text(c, s, x, y, sz, colr, a, w=w, shadow=kw.pop("shadow", 10), **kw)

def B_(S, n): return beats(S, n)
def is_long(S, n): return S.n() >= n

_IMG = {}
def cached(key, w, h, fn):
    if key not in _IMG:
        surf = skia.Surface(int(w), int(h)); cc = surf.getCanvas(); cc.clear(skia.ColorTRANSPARENT)
        fn(cc); _IMG[key] = surf.makeImageSnapshot()
    return _IMG[key]

def blit(c, img, x, y, a=1.0, scale=1.0):
    if a <= 0.003: return
    p = skia.Paint(); p.setAlphaf(clamp(a))
    if scale != 1.0:
        c.save(); c.translate(x, y); c.scale(scale, scale); c.drawImage(img, 0, 0, skia.SamplingOptions(skia.FilterMode.kLinear), p); c.restore()
    else:
        c.drawImage(img, x, y, skia.SamplingOptions(skia.FilterMode.kLinear), p)

# ------------------------------------------------------------------ background
def _bg_art(cc, W, H):
    cc.drawPaint(paint(shader=lin(0, 0, 0, H, [(0, WAL_T, 1), (1, WAL_B, 1)])))
    rng = random.Random(4)
    for k in range(70):  # wood grain
        y = rng.uniform(-0.05, 1.05) * H; amp = rng.uniform(4, 22) * H / 1080; ph = rng.random() * 6.28
        p = skia.Path(); p.moveTo(0, y)
        for i in range(1, 25):
            x = W * i / 24; p.lineTo(x, y + math.sin(i * 0.7 + ph) * amp + math.sin(i * 0.23 + ph * 2) * amp * 1.5)
        cc.drawPath(p, paint("#4a2a14" if k % 3 else "#000000", rng.uniform(0.05, 0.16), stroke=rng.uniform(1, 4) * H / 1080))
    cc.drawPaint(paint(shader=rad(W * 0.5, H * 0.45, max(W, H) * 0.75, [(0, "#ff9a3a", 0.10), (0.5, "#000000", 0.0), (1, "#000000", 0.6)])))

def bg_tube(c, W, H, t, S, dim=0.0):
    img = cached(("bg", W, H), W, H, lambda cc: _bg_art(cc, W, H))
    c.drawImage(img, 0, 0)
    rng = random.Random(9)  # floating dust motes in warm light
    u = S.u
    for k in range(16):
        x = (rng.random() * W + t * 8 * u * rng.uniform(0.3, 1)) % W; y = (rng.random() * H - t * 5 * u) % H
        circle(c, x, y, rng.uniform(1.5, 3.5) * u, AMBER, 0.18 + 0.1 * math.sin(t * 2 + k))
    if dim > 0: c.drawPaint(paint("#000000", dim))

# ------------------------------------------------------------------ the vacuum tube prop
def tube(c, x, y, s, t=0.0, glow=1.0, a=1.0, dead=False, seed=0, halo=True, crown=0.0):
    """Glass vacuum tube standing on (x, y) = bottom of its base; s = glass width. Height ~2.4 s."""
    if a <= 0.003: return
    w = s; h = s * 1.75; bh = s * 0.36; gy0 = y - bh; gy1 = gy0 - h
    fl = 0.0 if dead else glow * (0.9 + 0.1 * math.sin(t * 7 + seed * 1.7) * math.sin(t * 3.1 + seed))
    if halo and fl > 0.02:
        circle(c, x, gy0 - h * 0.45, s * 1.0, ORANGE, 0.28 * fl * a, blur=s * 0.38)
    # pins + base
    for k in (-0.28, -0.1, 0.1, 0.28):
        line(c, x + k * w, y - 2, x + k * w, y + s * 0.16, "#b9b2a6", max(1.5, s * 0.035), a)
    rrect(c, x - w * 0.52, gy0, w * 1.04, bh, s * 0.08, "#2a1a10", a)
    rrect(c, x - w * 0.52, gy0, w * 1.04, bh * 0.28, s * 0.05, "#3d271a", a)
    # glass envelope path
    p = skia.Path(); p.moveTo(x - w / 2, gy0); p.lineTo(x - w / 2, gy1 + w / 2)
    p.arcTo(skia.Rect.MakeLTRB(x - w / 2, gy1, x + w / 2, gy1 + w), 180, 180, False)
    p.lineTo(x + w / 2, gy0); p.close()
    c.drawPath(p, paint(mix("#3a2a20", CREAM, 0.25) if not dead else "#2a2420", (0.22 if not dead else 0.35) * a))
    if fl > 0.02:
        c.drawPath(p, paint(shader=rad(x, gy0 - h * 0.45, s * 0.9, [(0, AMBER, 0.45 * fl), (1, ORANGE, 0.0)]), a=a))
    # plate (box) + inner grid + filament
    px0, px1 = x - w * 0.3, x + w * 0.3; py0, py1 = gy0 - h * 0.72, gy0 - h * 0.14
    rect(c, px0, py0, px1 - px0, py1 - py0, "#6b6e75", a)
    rect(c, px0 + w * 0.06, py0, (px1 - px0) - w * 0.12, py1 - py0, "#3a3c42", a)
    for k in range(7):
        yy = lerp(py0 + h * 0.04, py1 - h * 0.04, k / 6)
        line(c, x - w * 0.16, yy, x + w * 0.16, yy, "#a9a196", max(1, s * 0.02), a * 0.9)
    fc = mix("#3a2a20", "#fff1b8", fl)
    pz = skia.Path(); pz.moveTo(x, py1 + h * 0.06)
    for k in range(7):
        pz.lineTo(x + (w * 0.06 if k % 2 == 0 else -w * 0.06), lerp(py1 + h * 0.02, py0 + h * 0.06, (k + 0.5) / 7))
    c.drawPath(pz, paint(fc, a, stroke=max(1.5, s * 0.03)))
    if fl > 0.02:
        c.drawPath(pz, paint(ORANGE, a * 0.6 * fl, stroke=max(3, s * 0.08), blur=s * 0.04))
    # supports + getter
    line(c, x - w * 0.36, gy0, x - w * 0.36, py0 - h * 0.05, "#8d877e", max(1, s * 0.02), a)
    line(c, x + w * 0.36, gy0, x + w * 0.36, py0 - h * 0.05, "#8d877e", max(1, s * 0.02), a)
    oval(c, x, gy1 + w * 0.26, w * 0.2, w * 0.07, "#8a8c94" if not dead else "#4a4a50", a * 0.8)
    # outline + highlight + exhaust tip
    c.drawPath(p, paint(CREAM, 0.55 * a, stroke=max(1.5, s * 0.025)))
    line(c, x - w * 0.36, gy0 - h * 0.12, x - w * 0.36, gy1 + w * 0.45, "#ffffff", max(2, s * 0.05), 0.35 * a)
    c.drawPath(poly([(x - w * 0.05, gy1 + 1), (x, gy1 - s * 0.1), (x + w * 0.05, gy1 + 1)]), paint(CREAM, 0.6 * a))
    if crown > 0:
        crown_icon(c, x, gy1 - s * 0.45, s * 0.55, crown * a)

def crown_icon(c, x, y, s, a=1.0, colr=ACCENT):
    if a <= 0: return
    p = poly([(x - s, y + s * 0.5), (x - s, y - s * 0.3), (x - s * 0.5, y + s * 0.1), (x, y - s * 0.55), (x + s * 0.5, y + s * 0.1), (x + s, y - s * 0.3), (x + s, y + s * 0.5)])
    c.drawPath(p, paint(colr, a)); c.drawPath(p, paint("#7a4a10", a, stroke=s * 0.08))
    for k in (-1, 0, 1): circle(c, x + k * s * (1 if k else 0), y - s * (0.3 if k else 0.55), s * 0.12, "#ffffff", a * 0.8)

def tube_grid_img(cols, rows, s, gapx, gapy, key, dead=()):
    W_ = cols * gapx + s; H_ = rows * gapy + s * 0.6
    def draw(cc):
        for r in range(rows):
            for k in range(cols):
                tube(cc, s * 0.5 + k * gapx + gapx * 0.5, (r + 1) * gapy, s, 0.0, 1.0, 1.0, dead=(r, k) in dead, seed=r * 31 + k, halo=True)
    return cached(key, W_, H_ + s * 0.2, draw)

# ------------------------------------------------------------------ small props
def phone(c, x, y, h, a=1.0, screen=1.0, t=0.0):
    w = h * 0.49
    rrect(c, x - w / 2 - h * 0.012, y - h / 2 - h * 0.012, w + h * 0.024, h * 1.024, w * 0.18, "#5a4a3e", a)
    rrect(c, x - w / 2, y - h / 2, w, h, w * 0.16, "#121216", a)
    sx, sy, sw, sh = x - w / 2 + h * 0.025, y - h / 2 + h * 0.025, w - h * 0.05, h * 0.95
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(sx, sy, sw, sh), w * 0.13, w * 0.13),
                paint(shader=lin(sx, sy, sx, sy + sh, [(0, "#3a2a5a", 1), (1, "#a8562a", 1)]), a=a * screen))
    cols = ["#ffb347", "#7bd88f", "#9fd8ff", "#ff8a7a", "#f6e7c8", "#c9a0ff"]
    for r in range(5):
        for k in range(4):
            ix = sx + sw * (0.14 + k * 0.24); iy = sy + sh * (0.14 + r * 0.13)
            rrect(c, ix - sw * 0.08, iy - sw * 0.08, sw * 0.16, sw * 0.16, sw * 0.045, cols[(r * 4 + k) % 6], a * screen * 0.9)
    rrect(c, x - w * 0.16, sy + h * 0.015, w * 0.32, h * 0.03, h * 0.015, "#121216", a)

def chip_icon(c, x, y, s, a=1.0, glow=0.0, label=None):
    if glow > 0: circle(c, x, y, s * 0.9, AMBER, glow * 0.25 * a, blur=s * 0.3)
    for k in range(6):
        q = (k + 0.5) / 6 - 0.5
        for (dx, dy, ex, ey) in ((q, -0.5, q, -0.62), (q, 0.5, q, 0.62), (-0.5, q, -0.62, q), (0.5, q, 0.62, q)):
            line(c, x + dx * s, y + dy * s, x + ex * s, y + ey * s, "#c9c2b6", s * 0.04, a, cap="butt")
    rrect(c, x - s / 2, y - s / 2, s, s, s * 0.08, "#24201e", a)
    rrect(c, x - s * 0.32, y - s * 0.32, s * 0.64, s * 0.64, s * 0.04, "#3a3430", a)
    if label: text(c, label, x, y, s * 0.18, CREAM, a, w=800, fam="Inter")

def person_s(c, x, y, h, colr="#0d0705", a=1.0, arm=0.0):
    person(c, x, y, h, colr, a=a, arm_up=arm)

def kettle(c, x, y, s, a=1.0, steam=0.0, t=0.0):
    c.drawPath(poly([(x - s * 0.45, y), (x - s * 0.35, y - s * 0.75), (x + s * 0.35, y - s * 0.75), (x + s * 0.45, y)]), paint("#d9d2c4", a))
    rect(c, x - s * 0.15, y - s * 0.85, s * 0.3, s * 0.1, "#3a2a20", a)
    p = skia.Path(); p.addArc(skia.Rect.MakeLTRB(x + s * 0.2, y - s * 0.7, x + s * 0.65, y - s * 0.2), -90, 180)
    c.drawPath(p, paint("#3a2a20", a, stroke=s * 0.1))
    c.drawPath(poly([(x - s * 0.38, y - s * 0.5), (x - s * 0.7, y - s * 0.75), (x - s * 0.62, y - s * 0.8), (x - s * 0.36, y - s * 0.62)]), paint("#d9d2c4", a))
    if steam > 0:
        for k in range(2):
            q = (t * 0.8 + k * 0.5) % 1
            circle(c, x - s * 0.7 + math.sin(q * 6) * s * 0.06, y - s * (0.85 + q * 0.6), s * (0.08 + q * 0.1), "#ffffff", steam * a * 0.5 * (1 - q))

def power_plant(c, x, y, s, a=1.0, col_="#d9cbb3"):
    for k, dx in enumerate((-0.35, 0.3)):
        c.drawPath(poly([(x + (dx - 0.22) * s, y), (x + (dx - 0.14) * s, y - s * 0.75), (x + (dx + 0.14) * s, y - s * 0.75), (x + (dx + 0.22) * s, y)]), paint(col_, a))
        circle(c, x + dx * s, y - s * 0.95, s * 0.13, "#ffffff", a * 0.35)
    rect(c, x - s * 0.1, y - s * 0.35, s * 0.2, s * 0.35, mix(col_, "#000000", 0.25), a)

def pool(c, x, y, s, a=1.0):
    rrect(c, x - s * 0.5, y - s * 0.25, s, s * 0.5, s * 0.05, "#2f8fd8", a)
    for k in range(1, 4): line(c, x - s * 0.46, y - s * 0.25 + k * s * 0.125, x + s * 0.46, y - s * 0.25 + k * s * 0.125, "#ffffff", s * 0.02, a * 0.7)
    rrect(c, x - s * 0.5, y - s * 0.25, s, s * 0.5, s * 0.05, "#e8f6ff", a, stroke=s * 0.04)

def doc_paper(c, x, y, w, h, a=1.0, rot=0.0, col_="#efe1c1"):
    c.save(); c.translate(x, y); c.rotate(rot)
    rect(c, -w / 2 + 8, -h / 2 + 10, w, h, "#000000", 0.35 * a, blur=10)
    rect(c, -w / 2, -h / 2, w, h, col_, a)
    c.restore()

def ruled_lines(c, x0, y0, w, n, gap, a=1.0, colr="#9a8a6a", seed=1, short=0.0):
    rng = random.Random(seed)
    for k in range(n):
        L = w * (rng.uniform(0.55, 1.0) if k < n - 1 else 0.5)
        line(c, x0, y0 + k * gap, x0 + L * (1 - short), y0 + k * gap, colr, gap * 0.16, a)

def moth(c, x, y, s, a=1.0, t=0.0, flap=0.0, ang=0.0):
    c.save(); c.translate(x, y); c.rotate(ang)
    f = 1 - flap * 0.5 * (1 + math.sin(t * 22))
    for sd in (-1, 1):
        c.save(); c.scale(sd * f if sd > 0 else -f, 1)
        p = skia.Path(); p.moveTo(0, -s * 0.05); p.cubicTo(s * 0.5, -s * 0.6, s * 1.1, -s * 0.35, s * 0.95, s * 0.05); p.cubicTo(s * 0.8, s * 0.2, s * 0.3, s * 0.15, 0, s * 0.05)
        c.drawPath(p, paint("#8a7556", a))
        p2 = skia.Path(); p2.moveTo(0, s * 0.05); p2.cubicTo(s * 0.45, s * 0.2, s * 0.7, s * 0.55, s * 0.4, s * 0.6); p2.cubicTo(s * 0.2, s * 0.6, s * 0.05, s * 0.35, 0, s * 0.15)
        c.drawPath(p2, paint("#6e5c42", a))
        circle(c, s * 0.55, -s * 0.15, s * 0.08, "#4a3b28", a)
        c.restore()
    oval(c, 0, s * 0.15, s * 0.1, s * 0.4, "#4a3b28", a)
    line(c, -s * 0.03, -s * 0.2, -s * 0.25, -s * 0.55, "#4a3b28", s * 0.03, a); line(c, s * 0.03, -s * 0.2, s * 0.25, -s * 0.55, "#4a3b28", s * 0.03, a)
    c.restore()

def relay(c, x, y, s, a=1.0, closed=0.0, hl=0.0):
    rect(c, x - s * 0.5, y + s * 0.3, s, s * 0.12, "#3d271a", a)
    rrect(c, x - s * 0.42, y - s * 0.35, s * 0.3, s * 0.65, s * 0.05, COPPER, a)  # coil
    for k in range(6): line(c, x - s * 0.42, y - s * 0.3 + k * s * 0.1, x - s * 0.12, y - s * 0.3 + k * s * 0.1, "#c98a4a", s * 0.025, a)
    ang = lerp(-14, 0, closed)
    c.save(); c.translate(x - s * 0.05, y - s * 0.42); c.rotate(ang)
    rect(c, 0, -s * 0.03, s * 0.5, s * 0.06, "#b9b2a6", a); c.restore()
    rect(c, x + s * 0.38, y - s * 0.45, s * 0.06, s * 0.75, "#b9b2a6", a)
    circle(c, x + s * 0.41, y - s * 0.4, s * 0.05, ACCENT, a)
    if hl > 0: rrect(c, x - s * 0.6, y - s * 0.6, s * 1.2, s * 1.1, s * 0.1, ACCENT, hl * a, stroke=s * 0.05)

def car(c, x, y, s, a=1.0, col_="#9a8a7a", old=False, lights=0.0):
    if old:
        rrect(c, x - s * 0.55, y - s * 0.35, s * 1.1, s * 0.22, s * 0.06, col_, a)
        rrect(c, x - s * 0.25, y - s * 0.58, s * 0.5, s * 0.26, s * 0.06, col_, a)
        rect(c, x - s * 0.18, y - s * 0.52, s * 0.15, s * 0.15, "#cfe3ff", a * 0.8); rect(c, x + s * 0.03, y - s * 0.52, s * 0.15, s * 0.15, "#cfe3ff", a * 0.8)
        for dx in (-0.35, 0.35):
            circle(c, x + dx * s, y - s * 0.1, s * 0.14, "#1a1410", a); circle(c, x + dx * s, y - s * 0.1, s * 0.06, "#b9b2a6", a)
        return
    p = skia.Path(); p.moveTo(x - s * 0.6, y - s * 0.12); p.lineTo(x - s * 0.58, y - s * 0.32); p.lineTo(x - s * 0.3, y - s * 0.36)
    p.lineTo(x - s * 0.15, y - s * 0.55); p.lineTo(x + s * 0.25, y - s * 0.55); p.lineTo(x + s * 0.42, y - s * 0.34); p.lineTo(x + s * 0.6, y - s * 0.3); p.lineTo(x + s * 0.62, y - s * 0.12); p.close()
    c.drawPath(p, paint(col_, a))
    c.drawPath(poly([(x - s * 0.12, y - s * 0.5), (x + s * 0.03, y - s * 0.5), (x + s * 0.03, y - s * 0.36), (x - s * 0.24, y - s * 0.36)]), paint("#cfe3ff", a * 0.7))
    c.drawPath(poly([(x + s * 0.07, y - s * 0.5), (x + s * 0.23, y - s * 0.5), (x + s * 0.35, y - s * 0.36), (x + s * 0.07, y - s * 0.36)]), paint("#cfe3ff", a * 0.7))
    for dx in (-0.36, 0.36):
        circle(c, x + dx * s, y - s * 0.1, s * 0.13, "#1a1410", a); circle(c, x + dx * s, y - s * 0.1, s * 0.06, "#b9b2a6", a)
    if lights > 0: circle(c, x + s * 0.6, y - s * 0.24, s * 0.05, "#fff1b8", a * lights)

def pylon(c, x, y, s, a=1.0, col_="#b9b2a6"):
    c.drawPath(poly([(x - s * 0.3, y), (x - s * 0.08, y - s), (x + s * 0.08, y - s), (x + s * 0.3, y)], close=False), paint(col_, a, stroke=s * 0.035))
    for k, yy in enumerate((0.8, 0.6)):
        line(c, x - s * 0.35, y - s * yy, x + s * 0.35, y - s * yy, col_, s * 0.035, a)
    for k in range(4):
        q = k / 4; line(c, x - s * 0.3 * (1 - q), y - s * q, x + s * 0.3 * (1 - q - 0.25), y - s * (q + 0.25), col_, s * 0.02, a)

def traffic_light(c, x, y, s, a=1.0, on=1.0, t=0.0):
    rect(c, x - s * 0.05, y - s * 0.4, s * 0.1, s * 0.4, "#3a3a40", a)
    rrect(c, x - s * 0.17, y - s * 1.2, s * 0.34, s * 0.82, s * 0.06, "#1a1a1e", a)
    for k, cl in enumerate((RED, ACCENT, GREEN)):
        lit = on * (1 if k == int(t * 0.5) % 3 else 0.15)
        circle(c, x, y - s * 1.06 + k * s * 0.26, s * 0.1, cl if lit > 0.2 else "#2a2a2e", a)
        if lit > 0.5: circle(c, x, y - s * 1.06 + k * s * 0.26, s * 0.18, cl, a * 0.3 * on, blur=s * 0.06)

def wind_clock(c, x, y, r, t, a=1.0):
    circle(c, x - r * 0.65, y - r * 0.85, r * 0.3, BRASS, a); circle(c, x + r * 0.65, y - r * 0.85, r * 0.3, BRASS, a)
    circle(c, x, y, r, BRASS, a); circle(c, x, y, r * 0.86, CREAM, a)
    for k in range(12):
        an = k * math.pi / 6; line(c, x + math.sin(an) * r * 0.72, y - math.cos(an) * r * 0.72, x + math.sin(an) * r * 0.8, y - math.cos(an) * r * 0.8, "#3a2a20", r * 0.04, a)
    an = t * 0.6; line(c, x, y, x + math.sin(an) * r * 0.65, y - math.cos(an) * r * 0.65, "#3a2a20", r * 0.05, a)
    an2 = t * 0.05 + 1; line(c, x, y, x + math.sin(an2) * r * 0.45, y - math.cos(an2) * r * 0.45, "#3a2a20", r * 0.07, a)
    line(c, x - r * 0.6, y + r * 0.9, x - r * 0.75, y + r * 1.15, BRASS, r * 0.08, a); line(c, x + r * 0.6, y + r * 0.9, x + r * 0.75, y + r * 1.15, BRASS, r * 0.08, a)

def bicycle(c, x, y, s, t, a=1.0, col_="#d9cbb3"):
    for dx in (-0.5, 0.5):
        circle(c, x + dx * s, y, s * 0.36, col_, a, stroke=s * 0.04)
        for k in range(6):
            an = t * 3 + k * math.pi / 3
            line(c, x + dx * s, y, x + dx * s + math.cos(an) * s * 0.34, y + math.sin(an) * s * 0.34, col_, s * 0.012, a * 0.7)
    pts = [(x - s * 0.5, y), (x - s * 0.1, y), (x + s * 0.3, y - s * 0.45), (x - s * 0.2, y - s * 0.45), (x - s * 0.1, y)]
    c.drawPath(poly(pts, close=False), paint(col_, a, stroke=s * 0.05))
    line(c, x - s * 0.2, y - s * 0.45, x - s * 0.5, y, col_, s * 0.05, a)
    line(c, x + s * 0.3, y - s * 0.45, x + s * 0.5, y, col_, s * 0.05, a)
    line(c, x + s * 0.3, y - s * 0.45, x + s * 0.25, y - s * 0.6, col_, s * 0.05, a); line(c, x + s * 0.18, y - s * 0.6, x + s * 0.34, y - s * 0.6, col_, s * 0.05, a)
    line(c, x - s * 0.28, y - s * 0.52, x - s * 0.1, y - s * 0.52, col_, s * 0.06, a)

def tube_radio(c, x, y, s, a=1.0, glow=1.0, t=0.0):
    """Big wooden tabletop tube radio sitting on (x, y)."""
    p = skia.Path(); p.moveTo(x - s * 0.6, y); p.lineTo(x - s * 0.6, y - s * 0.45)
    p.cubicTo(x - s * 0.6, y - s * 0.95, x + s * 0.6, y - s * 0.95, x + s * 0.6, y - s * 0.45); p.lineTo(x + s * 0.6, y); p.close()
    c.drawPath(p, paint("#6b3f1f", a)); c.drawPath(p, paint("#3a210e", a, stroke=s * 0.03))
    c.save(); pp = skia.Path(); pp.addCircle(x, y - s * 0.5, s * 0.3); c.clipPath(pp, doAntiAlias=True)
    circle(c, x, y - s * 0.5, s * 0.3, "#c8a878", a)
    for k in range(9): line(c, x - s * 0.3 + k * s * 0.075, y - s * 0.8, x - s * 0.3 + k * s * 0.075, y - s * 0.2, "#6b3f1f", s * 0.025, a)
    c.restore()
    rrect(c, x - s * 0.42, y - s * 0.16, s * 0.84, s * 0.1, s * 0.03, "#f1d9a0", a)
    if glow > 0:
        rrect(c, x - s * 0.42, y - s * 0.16, s * 0.84, s * 0.1, s * 0.03, AMBER, a * glow * 0.6)
        circle(c, x, y - s * 0.11, s * 0.3, ORANGE, a * glow * 0.2, blur=s * 0.1)
    line(c, x - s * 0.1 + math.sin(t * 0.3) * s * 0.2, y - s * 0.16, x - s * 0.1 + math.sin(t * 0.3) * s * 0.2, y - s * 0.06, RED, s * 0.012, a)
    circle(c, x - s * 0.45, y - s * 0.03, s * 0.05, "#3a210e", a); circle(c, x + s * 0.45, y - s * 0.03, s * 0.05, "#3a210e", a)

def notes(c, x, y, s, t, a=1.0):
    for k in range(3):
        q = (t * 0.5 + k / 3) % 1
        xx = x + k * s * 0.6 + math.sin(q * 6 + k) * s * 0.2; yy = y - q * s * 2
        al = a * math.sin(q * math.pi)
        oval(c, xx, yy, s * 0.16, s * 0.12, CREAM, al); line(c, xx + s * 0.14, yy, xx + s * 0.14, yy - s * 0.5, CREAM, s * 0.05, al)

def scope(c, x, y, w, h, t, amp_in, amp_out, a=1.0):
    rrect(c, x - w / 2 - 14, y - h / 2 - 14, w + 28, h + 28, 18, "#3d3a34", a)
    rrect(c, x - w / 2, y - h / 2, w, h, 10, "#06140c", a)
    for k in range(1, 6): line(c, x - w / 2 + k * w / 6, y - h / 2, x - w / 2 + k * w / 6, y + h / 2, "#1d4a2a", 1.5, a)
    for k in range(1, 4): line(c, x - w / 2, y - h / 2 + k * h / 4, x + w / 2, y - h / 2 + k * h / 4, "#1d4a2a", 1.5, a)
    for amp, col_, yo in ((amp_in, "#58ff9a", 0.0), (amp_out, ACCENT, 0.0)):
        if amp <= 0: continue
        p = skia.Path()
        for i in range(81):
            xx = x - w / 2 + w * i / 80; yy = y + yo - math.sin(i / 80 * 4 * math.pi * 2 + t * 4) * amp * h * 0.42
            (p.moveTo if i == 0 else p.lineTo)(xx, yy)
        c.drawPath(p, paint(col_, a * 0.35, stroke=10)); c.drawPath(p, paint(col_, a, stroke=3.5))

def cross(c, x, y, s, p):
    if p > 0: xmark(c, x, y, s, p, colr=RED)

def pop_flash(c, x, y, s, q, a=1.0):
    """little burst for 0<=q<=1"""
    if q <= 0 or q >= 1: return
    circle(c, x, y, s * (0.3 + q), "#fff1b8", a * (1 - q) * 0.9, stroke=s * 0.1 * (1 - q) + 1)
    for k in range(6):
        an = k * math.pi / 3 + 0.3
        line(c, x + math.cos(an) * s * (0.3 + q * 0.6), y + math.sin(an) * s * (0.3 + q * 0.6), x + math.cos(an) * s * (0.5 + q), y + math.sin(an) * s * (0.5 + q), "#fff1b8", s * 0.06, a * (1 - q))

# ------------------------------------------------------------------ kit wrappers
def motif_tube(c, W, H, t, S, cx, cy, s):
    u = S.u; sz = 230 * s * u * (1.2 if S.P else 1)
    for dx, k in ((-1.25, 0.62), (1.25, 0.62)):
        tube(c, cx + dx * sz, cy + sz * 1.0, sz * k, t, 0.85, 1.0, seed=int(dx * 10))
    tube(c, cx, cy + sz * 1.15, sz, t, 1.0, 1.0, seed=3)

def t_title(c, W, H, t, S): kit.title(c, W, H, t, S, bg_tube, motif_tube, PAL)
def t_card(c, W, H, t, S):
    def bgc(c, W, H, t, S):
        bg_tube(c, W, H, t, S)
        c.saveLayerAlpha(None, 110); motif_tube(c, W, H, t, S, W / 2, H * 0.42, 1.35 if not S.P else 1.0); c.restore()
    kit.card(c, W, H, t, S, bgc, PAL)
def t_end(c, W, H, t, S): kit.end(c, W, H, t, S, bg_tube, motif_tube, PAL)
def t_endshort(c, W, H, t, S): kit.end_short(c, W, H, t, S, bg_tube, motif_tube, PAL)

# ------------------------------------------------------------------ t_phone
def _switch_grid(c, x, y, s, n, t, a, speed=1.0, tubes=0.0):
    cell = s / n
    for r in range(n):
        for k in range(n):
            ph = (r * 7 + k * 13) % 17
            on = (math.sin(t * speed * (2 + ph * 0.4) + ph) > 0)
            cx_, cy_ = x - s / 2 + (k + 0.5) * cell, y - s / 2 + (r + 0.5) * cell
            rrect(c, cx_ - cell * 0.36, cy_ - cell * 0.36, cell * 0.72, cell * 0.72, cell * 0.1, AMBER if on else "#3a2a20", a * (1 - tubes))

def t_phone(c, W, H, t, S):
    o = S.opts; mode = o.get("mode", "intro")
    bg_tube(c, W, H, t, S)
    with Stage(c, S) as ts:
        if mode == "zoom":
            phone(c, 470, 560, 760, 1.0)
            pz = eout(prog(t, 0.3, 0.8))
            chip_icon(c, 470, 640, 110, 1.0, glow=0.6)
            line(c, 525, 590, lerp(525, 1000, pz), lerp(590, 250, pz), CREAM, 3, 0.6 * pz)
            line(c, 525, 690, lerp(525, 1000, pz), lerp(690, 930, pz), CREAM, 3, 0.6 * pz)
            rrect(c, 1000, 250, 680 * pz, 680, 30, "#24201e", pz)
            if pz > 0.6: _switch_grid(c, 1340, 590, 600, 10, t, (pz - 0.6) / 0.4, speed=2.5)
            return
        long_ = is_long(S, 3); B = B_(S, 3)
        # phone slides left as the chip panel opens
        q = ease(prog(t, B(0, 0.45), 1.2))
        px = lerp(960, 470, q)
        phone(c, px, 560, 760, 1.0)
        chip_icon(c, px, 640, 110, 1.0, glow=0.6 * q)
        pz = eout(prog(t, B(0, 0.55), 0.9))
        if pz > 0:
            line(c, px + 55, 590, lerp(px + 55, 1000, pz), lerp(590, 230, pz), CREAM, 3, 0.6 * pz)
            line(c, px + 55, 690, lerp(px + 55, 1000, pz), lerp(690, 950, pz), CREAM, 3, 0.6 * pz)
            rrect(c, 1000, 230, 720 * pz, 720, 30, "#24201e", pz)
            rrect(c, 1000, 230, 720 * pz, 720, 30, BRASS, pz * 0.6, stroke=4)
            tb = ease(prog(t, B(2, 0.35), 1.2))
            if pz > 0.6:
                _switch_grid(c, 1360, 590, 640, 10, t, (pz - 0.6) / 0.4 * (1 - tb), speed=1.0 + 3 * prog(t, B(1, 0), 2))
            if tb > 0:
                img = tube_grid_img(5, 3, 70, 128, 215, "phone_tubes")
                blit(c, img, 1360 - img.width() / 2, 590 - img.height() / 2 - 10, tb)
        if long_:
            C(c, "~19 BILLION TRANSISTORS", 1360, 175, vis(t, B(0, 0.6), B(2, 0.3)), ts, dot=AMBER)
            C(c, "ON / OFF, BILLIONS OF TIMES A SECOND", 1360, 1010, vis(t, B(1, 0.15), B(2, 0.3)), ts, size=30)
            C(c, "EVERY SWITCH = A VACUUM TUBE?", 1360, 175, vis(t, B(2, 0.45)), ts, dot=ORANGE)
            T(c, "?", 1360, 1000, 120, ts, AMBER, prog(t, B(2, 0.75), 0.4))
    kit.hook(c, W, H, t, S)

# ------------------------------------------------------------------ t_tube (how it works)
def _big_tube(c, x, y, s, t, flow, gridv, a=1.0, lab=0.0, ts=1.0):
    """Schematic cutaway: filament at bottom, grid mesh, plate on top. (x, y) = base bottom; s = glass width."""
    w = s; h = s * 1.55; bh = s * 0.22; gy0 = y - bh; gy1 = gy0 - h
    circle(c, x, gy0 - h * 0.25, s * 0.55, ORANGE, 0.22 * a, blur=s * 0.25)
    rrect(c, x - w * 0.52, gy0, w * 1.04, bh, s * 0.05, "#2a1a10", a)
    for k in (-0.3, -0.1, 0.1, 0.3): line(c, x + k * w, y, x + k * w, y + s * 0.08, "#b9b2a6", 6, a)
    p = skia.Path(); p.moveTo(x - w / 2, gy0); p.lineTo(x - w / 2, gy1 + w / 2)
    p.arcTo(skia.Rect.MakeLTRB(x - w / 2, gy1, x + w / 2, gy1 + w), 180, 180, False); p.lineTo(x + w / 2, gy0); p.close()
    c.drawPath(p, paint("#3a2a20", 0.35 * a))
    # plate (top)
    py = gy1 + h * 0.3
    rrect(c, x - w * 0.34, py - h * 0.05, w * 0.68, h * 0.07, 8, "#8d9098", a)
    line(c, x + w * 0.34, py - h * 0.015, x + w * 0.34, gy0, "#8d877e", 4, a)
    # grid mesh (middle)
    gyy = gy1 + h * 0.62
    for k in range(13):
        xx = x - w * 0.34 + k * w * 0.68 / 12
        circle(c, xx, gyy, 7, mix("#a9a196", ACCENT, gridv), a)
    line(c, x - w * 0.36, gyy, x + w * 0.36, gyy, mix("#a9a196", ACCENT, gridv), 2.5, a)
    line(c, x - w * 0.36, gyy, x - w * 0.36, gy0, "#8d877e", 4, a)
    # filament (bottom)
    fy = gy0 - h * 0.12
    pz = skia.Path(); pz.moveTo(x - w * 0.3, fy)
    for k in range(1, 13): pz.lineTo(x - w * 0.3 + k * w * 0.6 / 12, fy + (-14 if k % 2 else 0))
    c.drawPath(pz, paint(ORANGE, a * 0.7, stroke=16, blur=8)); c.drawPath(pz, paint("#fff1b8", a, stroke=5))
    # electrons
    if flow > 0:
        rng = random.Random(3)
        for k in range(60):
            xx = x + rng.uniform(-0.28, 0.28) * w; ph = rng.random(); sp = rng.uniform(0.5, 0.9)
            q = (t * sp + ph) % 1
            yy = lerp(fy - 10, py + h * 0.03, q)
            # electrons above the grid only pass when flow is high
            passed = (k % 10) < flow * 10
            if not passed and yy < gyy - 6:
                continue
            circle(c, xx + math.sin(q * 9 + k) * 6, yy, 6, ELEC, a * 0.95)
    c.drawPath(p, paint(CREAM, 0.6 * a, stroke=4))
    line(c, x - w * 0.4, gy0 - h * 0.1, x - w * 0.4, gy1 + w * 0.45, "#ffffff", 8, 0.3 * a)
    return dict(plate=(x + w * 0.36, py), grid=(x + w * 0.38, gyy), fil=(x + w * 0.33, fy), glass=(x - w * 0.5, gy1 + h * 0.25))

def radio_tower(c, x, y, h, t, a=1.0, waves=1.0):
    c.drawPath(poly([(x - h * 0.15, y), (x, y - h), (x + h * 0.15, y)], close=False), paint(BRASS, a, stroke=6))
    for k in range(5):
        q = k / 5; line(c, x - h * 0.15 * (1 - q), y - h * q, x + h * 0.15 * (1 - q - 0.2), y - h * (q + 0.2), BRASS, 3, a)
    circle(c, x, y - h, 9, ACCENT, a)
    if waves > 0:
        for k in range(4):
            q = (t * 0.6 + k / 4) % 1; r = 30 + q * h * 0.8
            for sd in (-1, 1):
                pp = skia.Path(); pp.addArc(skia.Rect.MakeLTRB(x - r, y - h - r, x + r, y - h + r), (-30 if sd > 0 else 150), 60)
                c.drawPath(pp, paint(AMBER, a * waves * (1 - q), stroke=5))

def t_tube(c, W, H, t, S):
    bg_tube(c, W, H, t, S)
    B = B_(S, 4)
    with Stage(c, S) as ts:
        # panel A: the rules
        pa = phase(t, None, B(1, 0))
        with Layer(c, pa) as on:
            if on:
                T(c, "EVERYTHING ELSE STAYS THE SAME", 960, 170, 64, ts, CREAM, vis(t, 0.2))
                items = [("ELECTRICITY", "bolt"), ("RADIO", "radio"), ("LIGHT BULB", "bulb")]
                for k, (lab, ic) in enumerate(items):
                    x = 360 + k * 460; pk = vis(t, B(0, 0.25 + k * 0.08))
                    if pk <= 0: continue
                    rrect(c, x - 180, 300, 360, 380, 30, "#2a1a10", pk); rrect(c, x - 180, 300, 360, 380, 30, BRASS, pk * 0.6, stroke=4)
                    if ic == "bolt":
                        c.drawPath(poly([(x + 20, 360), (x - 60, 500), (x - 5, 500), (x - 30, 620), (x + 60, 460), (x + 5, 460), (x + 40, 360)]), paint(ACCENT, pk))
                    elif ic == "radio":
                        tube_radio(c, x, 600, 260, pk, 0.8, t)
                    else:
                        circle(c, x, 450, 85, "#fff1b8", pk); circle(c, x, 450, 140, AMBER, 0.3 * pk, blur=40)
                        rect(c, x - 40, 530, 80, 70, "#b9b2a6", pk)
                    check(c, x + 120, 340, 34, pk)
                    T(c, lab, x, 720, 44, ts, CREAM, pk, maxw=380)
                px = 1740; pc = vis(t, B(0, 0.62))
                if pc > 0:
                    c.drawPath(poly([(px, 360), (px + 90, 470), (px, 620), (px - 90, 470)]), paint("#8fb6c9", pc * 0.85))
                    c.drawPath(poly([(px, 360), (px + 90, 470), (px, 620), (px - 90, 470)]), paint("#ffffff", pc * 0.7, stroke=4))
                    cross(c, px, 490, 70, pc)
                    T(c, "SOLID SWITCH", px, 720, 44, ts, RED, pc, maxw=340)
                C(c, "WE NEVER LEARN TO SWITCH WITH A CRYSTAL", 960, 900, vis(t, B(0, 0.75)), ts, dot=RED)
        # panel B: the tube diagram
        pb = phase(t, B(1, 0) - 0.3, B(3, 0))
        with Layer(c, pb) as on:
            if on:
                gridv = 0.0; flow = clamp(prog(t, B(1, 0.4), 1.0))
                tg = t - B(2, 0.2)
                if tg > 0: gridv = 0.5 + 0.5 * math.sin(tg * 2.0); flow = 0.15 + 0.85 * gridv
                d = _big_tube(c, 640, 1000, 520, t, flow, gridv, 1.0)
                al = vis(t, B(1, 0.05))
                hide = B(2, 0.2)
                C(c, "GLASS BULB, AIR PUMPED OUT", 1480, 470, vis(t, B(1, 0.05), hide), ts, dot=CREAM)
                C(c, "HOT FILAMENT BOILS OFF ELECTRONS", 1480, 560, vis(t, B(1, 0.35), hide), ts, dot=ORANGE)
                C(c, "ELECTRONS FLY TO THE PLATE", 1480, 650, vis(t, B(1, 0.65), hide), ts, dot=ELEC)
                for (lab, key, tt) in (("PLATE", "plate", 0.6), ("GRID", "grid", 2.0), ("FILAMENT", "fil", 0.3)):
                    if key == "grid": pp = vis(t, B(2, 0.05))
                    else: pp = vis(t, B(1, tt))
                    if pp <= 0: continue
                    x0, y0 = d[key]; line(c, x0 + 10, y0, 1000, y0, CREAM, 3, pp * 0.7)
                    T(c, lab, 1020, y0, 40, ts, ACCENT if key == "grid" else CREAM, pp, align="l", w=800)
                pg = vis(t, B(2, 0.25))
                if pg > 0:
                    # small knob -> big current meter
                    rrect(c, 1260, 520, 600, 300, 26, "#2a1a10", pg); rrect(c, 1260, 520, 600, 300, 26, BRASS, pg * 0.6, stroke=3)
                    T(c, "SMALL VOLTAGE", 1410, 570, 34, ts, ACCENT, pg, w=800, maxw=260)
                    circle(c, 1410, 680, 60, "#3d271a", pg); circle(c, 1410, 680, 60, BRASS, pg, stroke=6)
                    an = math.radians(-130 + 260 * gridv); line(c, 1410, 680, 1410 + math.sin(an) * 50, 680 - math.cos(an) * 50, ACCENT, 8, pg)
                    arrow(c, 1580, 680, 1580, 680, CREAM, 6, pg)
                    T(c, "BIG CURRENT", 1710, 570, 34, ts, ELEC, pg, w=800, maxw=260)
                    gauge(c, 1710, 730, 95, flow, "", 1.0, colr=ELEC, a=pg)
                C(c, "= AMPLIFIER", 1370, 900, vis(t, B(2, 0.6)), ts, dot=ACCENT)
                C(c, "= SWITCH", 1720, 900, vis(t, B(2, 0.75)), ts, dot=ACCENT)
                C(c, "THE SAME JOB A TRANSISTOR DOES", 1540, 990, vis(t, B(2, 0.88)), ts, size=30)
        # panel C: Audion 1906
        pc = phase(t, B(3, 0) - 0.3)
        with Layer(c, pc) as on:
            if on:
                tube(c, 520, 900, 280, t, 1.0, crown=0)
                radio_tower(c, 1180, 920, 560, t, 1.0, waves=vis(t, B(3, 0.4)))
                line(c, 1420, 620, 1800, 620, BRASS, 5, vis(t, B(3, 0.55)))
                for k in range(5): line(c, 1440 + k * 90, 620, 1440 + k * 90, 900, BRASS, 6, vis(t, B(3, 0.55)))
                T(c, "1906", 520, 170, 110, ts, ACCENT, vis(t, B(3, 0.05)))
                C(c, "THE AUDION · LEE DE FOREST", 520, 290, vis(t, B(3, 0.15)), ts, dot=ORANGE)
                C(c, "LONG-DISTANCE PHONE CALLS", 1610, 980, vis(t, B(3, 0.55)), ts, size=30)
                C(c, "RADIO BROADCASTING", 1180, 260, vis(t, B(3, 0.4)), ts, dot=AMBER)
    kit.hook(c, W, H, t, S)

# ------------------------------------------------------------------ t_eniac
def _cabinet_img(cols=6, rows=4, key="cab"):
    s = 46; gx = 70; gy = 128
    W_ = cols * gx + 60; H_ = rows * gy + 90
    def draw(cc):
        rrect(cc, 0, 0, W_, H_, 10, "#2b1d14"); rrect(cc, 0, 0, W_, H_, 10, BRASS, 0.5, stroke=4)
        rect(cc, 14, 14, W_ - 28, H_ - 28, "#120a06")
        for r in range(rows):
            for k in range(cols):
                tube(cc, 30 + gx * 0.5 + k * gx, 40 + (r + 1) * gy - 18, s, 0.0, 1.0, 1.0, seed=r * 7 + k)
        for k in range(cols * 2):
            circle(cc, 30 + k * (W_ - 60) / (cols * 2 - 1), H_ - 26, 6, "#d9cbb3", 0.8)
    return cached(key, W_, H_, draw)

def eniac_room(c, t, a=1.0, x0=40, scroll=0.0):
    img = _cabinet_img()
    n = 6; gap = 505
    c.save(); c.translate(-scroll, 0)
    for k in range(n):
        blit(c, img, x0 + k * gap, 220, a)
        # live blinking accumulator lights
        for j in range(8):
            on = math.sin(t * 5 + k * 1.3 + j * 0.9) > 0.3
            circle(c, x0 + k * gap + 40 + j * 46, 205, 7, ACCENT if on else "#3a2a20", a)
    c.restore()

def plugboard(c, x, y, w, h, t, a=1.0, grow=1.0):
    rrect(c, x, y, w, h, 12, "#1d130c", a); rrect(c, x, y, w, h, 12, BRASS, a * 0.6, stroke=3)
    for r in range(6):
        for k in range(14):
            circle(c, x + 30 + k * (w - 60) / 13, y + 30 + r * (h - 60) / 5, 6, "#c9c2b6", a * 0.8)
    rng = random.Random(5)
    for k in range(int(9 * grow)):
        x1 = x + 30 + rng.randrange(14) * (w - 60) / 13; y1 = y + 30 + rng.randrange(6) * (h - 60) / 5
        x2 = x + 30 + rng.randrange(14) * (w - 60) / 13; y2 = y + 30 + rng.randrange(6) * (h - 60) / 5
        p = skia.Path(); p.moveTo(x1, y1); p.cubicTo(x1, y1 + 120, x2, y2 + 120, x2, y2)
        c.drawPath(p, paint(["#e8443a", ACCENT, "#5ab0ff", GREEN][k % 4], a, stroke=6))

def colossus(c, t, a=1.0):
    img = _cabinet_img(5, 3, "colossus")
    blit(c, img, 300, 300, a); blit(c, img, 300 + img.width() + 30, 300, a)
    # paper-tape loop
    x0 = 300 + 2 * img.width() + 90
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x0, 300, 260, 420), 120, 120), paint(CREAM, a, stroke=22))
    for k in range(14):
        q = (k / 14 + t * 0.15) % 1
        yy = 330 + q * 360
        circle(c, x0 - 4, yy, 4, "#3a2a20", a)

def t_eniac(c, W, H, t, S):
    bg_tube(c, W, H, t, S)
    long_ = is_long(S, 4); B = B_(S, 4)
    with Stage(c, S) as ts:
        if not long_:  # Short: straight to the ENIAC room + counters
            eniac_room(c, t, 1.0, x0=40, scroll=t * 25)
            q = clamp(prog(t, 0.2, S.dur * 0.45))
            T(c, f"{round(17468 * eout(q)):,} TUBES", 960, 950, 90, ts, ACCENT, vis(t, 0.2))
            C(c, "~150 KW", 960, 110, vis(t, S.lt(0, 0.62)), ts, dot=ORANGE)
            return
        pa = phase(t, None, B(1, 0))
        with Layer(c, pa) as on:
            if on:
                colossus(c, t, 1.0)
                C(c, "COLOSSUS · BLETCHLEY PARK · WWII", 960, 150, vis(t, B(0, 0.05)), ts, dot=AMBER)
                C(c, "~2,500 TUBES EACH", 700, 860, vis(t, B(0, 0.4)), ts)
                C(c, "HELPED CRACK GERMAN CODES", 1250, 860, vis(t, B(0, 0.65)), ts, dot=GREEN)
        pb = phase(t, B(1, 0) - 0.3, B(3, 0))
        with Layer(c, pb) as on:
            if on:
                eniac_room(c, t, 1.0, x0=40, scroll=(t - B(1, 0)) * 20)
                c.drawRect(skia.Rect.MakeLTRB(-10, 820, 1930, 1090), paint(shader=lin(0, 820, 0, 1000, [(0, "#000000", 0), (1, "#000000", 0.75)])))
                T(c, "ENIAC · 1946", 960, 110, 70, ts, CREAM, vis(t, B(1, 0.02)))
                q = clamp(prog(t, B(1, 0.1), 3.5))
                C(c, f"{round(17468 * eout(q)):,} VACUUM TUBES", 520, 900, vis(t, B(1, 0.1)), ts, size=40, dot=ORANGE)
                C(c, "~5 MILLION HAND-SOLDERED JOINTS", 1360, 900, vis(t, B(1, 0.7)), ts, size=34)
                pk = vis(t, B(2, 0.0))
                if pk > 0:
                    rrect(c, 230, 300, 1460, 520, 30, "#1a0f08", 0.9 * pk)
                    T(c, "~30 TONS", 560, 400, 90, ts, CREAM, vis(t, B(2, 0.05)))
                    T(c, "~150 KILOWATTS", 1360, 400, 90, ts, ACCENT, vis(t, B(2, 0.3)))
                    for k in range(100):
                        pkk = vis(t, B(2, 0.35) + k * 0.025)
                        if pkk <= 0: break
                        kettle(c, 330 + (k % 25) * 52, 560 + (k // 25) * 62, 40, pkk, steam=0.8, t=t + k)
                    C(c, "≈ 100 KETTLES BOILING, ALL DAY", 960, 860, vis(t, B(2, 0.5)), ts, dot=AMBER)
        pc = phase(t, B(3, 0) - 0.3)
        with Layer(c, pc) as on:
            if on:
                plugboard(c, 260, 260, 1400, 440, t, 1.0, grow=clamp(prog(t, B(3, 0.4), 3)))
                for k in range(6):
                    person_s(c, 400 + k * 225, 1000, 240, "#0b0604", vis(t, B(3, 0.35) + k * 0.15), arm=0.6 if k % 2 else 0.9)
                T(c, "~5,000 ADDITIONS PER SECOND", 960, 150, 70, ts, ACCENT, vis(t, B(3, 0.02)))
                C(c, "6 FIRST PROGRAMMERS · CABLES + SWITCHES BY HAND", 960, 735, vis(t, B(3, 0.4)), ts, size=32, dot=CREAM)

# ------------------------------------------------------------------ t_burnout
GRID_C, GRID_R = 12, 4
def t_burnout(c, W, H, t, S):
    bg_tube(c, W, H, t, S)
    B = B_(S, 3)
    with Stage(c, S) as ts:
        s = 62; gx = 120; gy = 170
        img = tube_grid_img(GRID_C, GRID_R, s, gx, gy, "burn_grid")
        ox, oy = 960 - img.width() / 2, 230
        blit(c, img, ox, oy)
        rng = random.Random(12); events = []
        tt = 0.6
        while tt < S.dur:
            events.append((tt, rng.randrange(GRID_R), rng.randrange(GRID_C))); tt += rng.uniform(1.0, 2.2)
        n_dead = 0
        dark = _IMG.get("dead1") or cached("dead1", s * 1.3, s * 2.4, lambda cc: tube(cc, s * 0.65, s * 2.2, s, 0, 0, 1, dead=True, halo=False))
        for (te, r, k) in events:
            if t < te: break
            n_dead += 1
            x = ox + s * 0.5 + k * gx + gx * 0.5; y = oy + (r + 1) * gy
            rect(c, x - s * 0.75, y - s * 2.25, s * 1.5, s * 2.5, "#120a06")
            blit(c, dark, x - s * 0.65, y - s * 2.2)
            pop_flash(c, x, y - s * 1.0, s * 0.9, (t - te) / 0.6)
        T(c, f"FAILURES: {n_dead}", 960, 120, 72, ts, RED, vis(t, 0.3))
        C(c, "SEVERAL TUBES A DAY (EARLY ON)", 520, 1000, vis(t, B(0, 0.35), B(1, 0)), ts, dot=RED)
        C(c, "OUT OF ACTION ~HALF THE TIME", 1400, 1000, vis(t, B(0, 0.7), B(1, 0)), ts)
        pw = vis(t, B(1, 0.0), B(2, 0))
        if pw > 0:
            rrect(c, 360, 300, 1200, 520, 30, "#1a0f08", 0.92 * pw)
            # temperature curve: spikes at warm-up/cool-down
            p = skia.Path()
            for i in range(101):
                q = i / 100; yv = 0.15 + 0.7 * (math.exp(-((q - 0.12) / 0.05) ** 2) + math.exp(-((q - 0.88) / 0.05) ** 2))
                (p.moveTo if i == 0 else p.lineTo)(440 + q * 1040, 760 - yv * 380)
            c.drawPath(p, paint(RED, pw, stroke=7))
            T(c, "WARM-UP", 565, 340, 40, ts, ACCENT, pw, w=800); T(c, "COOL-DOWN", 1355, 340, 40, ts, ACCENT, pw, w=800)
            T(c, "MOST FAILURES", 960, 600, 46, ts, CREAM, pw, w=800)
            C(c, "SO: SWITCH IT OFF AS LITTLE AS POSSIBLE", 960, 1000, vis(t, B(1, 0.5), B(2, 0)), ts, dot=GREEN)
        p3 = vis(t, B(2, 0.05))
        if p3 > 0:
            hx = 300 + (math.sin((t - B(2, 0)) * 0.5) * 0.5 + 0.5) * 1320
            circle(c, hx, 560, 140, "#fff1b8", 0.18 * p3, blur=40)
            person_s(c, hx - 120, 1060, 300, "#050302", p3, arm=0.7)
            C(c, "STURDIER TUBES: ~1 FAILURE EVERY 2 DAYS", 960, 1000, p3, ts, dot=AMBER)

# ------------------------------------------------------------------ t_univac
def tape_drive(c, x, y, t, a=1.0, sp=1.0):
    rrect(c, x - 110, y - 330, 220, 420, 14, "#d9cbb3", a); rrect(c, x - 110, y - 330, 220, 420, 14, "#8a7a62", a, stroke=4)
    for k, yy in enumerate((y - 240, y - 70)):
        circle(c, x, yy, 66, "#2a1a10", a); circle(c, x, yy, 66, "#5a4a3e", a, stroke=6)
        for j in range(3):
            an = t * sp * (3 if k else -3) + j * 2.09
            line(c, x, yy, x + math.cos(an) * 56, yy + math.sin(an) * 56, "#8a7a62", 6, a)
        circle(c, x, yy, 14, "#c9c2b6", a)

def t_univac(c, W, H, t, S):
    bg_tube(c, W, H, t, S)
    B = B_(S, 2)
    with Stage(c, S) as ts:
        img = _cabinet_img(8, 4, "univac")
        blit(c, img, 140, 250)
        for k in range(3): tape_drive(c, 920 + k * 235, 820, t, 1.0)
        rrect(c, 140, 840, img.width(), 110, 12, "#3d271a");
        for j in range(16):
            on = math.sin(t * 4 + j * 1.7) > 0
            circle(c, 180 + j * 34, 895, 9, ACCENT if on else "#2a1a10")
        C(c, "UNIVAC I · 1951", 480, 160, vis(t, B(0, 0.05)), ts, size=40, dot=AMBER)
        C(c, "U.S. CENSUS BUREAU", 1250, 160, vis(t, B(0, 0.3)), ts)
        C(c, "ONE OF THE FIRST COMPUTERS SOLD", 1250, 250, vis(t, B(0, 0.5)), ts, size=30)
        C(c, "~5,000 TUBES", 480, 1010, vis(t, B(0, 0.8)), ts, dot=ORANGE)
        for k, s_ in enumerate(("RARE", "ENORMOUS", "EXPENSIVE")):
            pk = vis(t, B(1, 0.05 + k * 0.12))
            if pk > 0: stamp(c, s_, 1700, 420 + k * 170, pk, 0.8, color=ACCENT, rot=-6 + k * 4, size=64)

# ------------------------------------------------------------------ t_bell
def bench(c, t, a=1.0, amp=0.0):
    rect(c, 0, 820, 1920, 260, "#3d271a", a); rect(c, 0, 820, 1920, 18, "#5a3a22", a)
    # germanium slab on a metal base
    rect(c, 420, 720, 360, 100, "#6b6e75", a); rect(c, 450, 640, 300, 80, "#8c929c", a)
    for k in range(6): line(c, 460 + k * 50, 645, 480 + k * 50, 715, "#a9b0bb", 3, a * 0.6)
    # plastic wedge with gold foil
    c.drawPath(poly([(600, 380), (520, 640), (680, 640)]), paint("#e6eef5", a * 0.5))
    c.drawPath(poly([(600, 380), (520, 640), (680, 640)]), paint("#ffffff", a * 0.8, stroke=3))
    line(c, 560, 520, 596, 640, "#ffd34d", 6, a); line(c, 640, 520, 604, 640, "#ffd34d", 6, a)
    circle(c, 600, 640, 10, "#ffffff", a * 0.6 * (0.5 + 0.5 * math.sin(t * 6)), blur=6)
    # leads to scope
    p = skia.Path(); p.moveTo(560, 520); p.cubicTo(400, 400, 300, 600, 250, 820); c.drawPath(p, paint("#d9cbb3", a, stroke=4))
    p = skia.Path(); p.moveTo(640, 520); p.cubicTo(800, 360, 1000, 480, 1080, 560); c.drawPath(p, paint("#d9cbb3", a, stroke=4))
    scope(c, 1380, 560, 560, 360, t, 0.18, amp, a)
    T(c, "IN", 1150, 420, 34, 1.0, "#58ff9a", a * 0.9, w=800); T(c, "OUT", 1150, 470, 34, 1.0, ACCENT, a * amp / 0.85 if amp else 0, w=800)

def logbook(c, x, y, w, h, t, a=1.0, write=1.0, moth_a=1.0, ts=1.0, rot=-3, fs=38, ms=70):
    c.save(); c.translate(x, y); c.rotate(rot)
    rect(c, -w / 2 + 10, -h / 2 + 12, w, h, "#000000", 0.4 * a, blur=12)
    rect(c, -w / 2, -h / 2, w, h, "#f3e8cc", a)
    for k in range(14): line(c, -w / 2 + 20, -h / 2 + 50 + k * (h - 70) / 13, w / 2 - 20, -h / 2 + 50 + k * (h - 70) / 13, "#9fc3e0", 2, a * 0.6)
    line(c, -w / 2 + 110, -h / 2, -w / 2 + 110, h / 2, "#e89a9a", 2, a * 0.7)
    rng = random.Random(3)
    for k in range(5):
        yy = -h / 2 + 50 + k * (h - 70) / 13
        text(c, ["1525", "1545", "", "1600", "1700"][k], -w / 2 + 60, yy - 6, 26, INK, a * 0.85, w=500, fam="Inter")
        if k != 2: line(c, -w / 2 + 130, yy - 6, -w / 2 + 130 + rng.uniform(0.3, 0.75) * (w - 170), yy - 6, INK, 3, a * 0.5)
    # taped moth
    my = -h / 2 + 50 + 2 * (h - 70) / 13 + 60
    if moth_a > 0:
        moth(c, -w * 0.15, my, ms, a * moth_a, ang=8)
        for dx, an in ((-0.27, -20), (-0.03, 15)):
            c.save(); c.translate(-w * 0.15 + dx * ms * 6.5, my); c.rotate(an)
            rect(c, -ms * 0.7, -ms * 0.25, ms * 1.4, ms * 0.5, "#fff8dc", a * moth_a * 0.65); c.restore()
    if write > 0:
        s_ = "First actual case of bug being found."
        n = int(len(s_) * clamp(write))
        text(c, s_[:n], -w / 2 + 130, my + ms * 1.7, fs, INK, a, w=500, fam="Inter Display", align="l")
    c.restore()

def t_bell(c, W, H, t, S):
    bg_tube(c, W, H, t, S)
    B = B_(S, 4)
    with Stage(c, S) as ts:
        pa = phase(t, None, B(2, 0))
        with Layer(c, pa) as on:
            if on:
                amp = 0.85 * eout(prog(t, B(0, 0.7), 1.2))
                bench(c, t, 1.0, amp)
                C(c, "DECEMBER 1947 · BELL LABS, NEW JERSEY", 960, 110, vis(t, B(0, 0.05)), ts, size=36, dot=AMBER)
                C(c, "GERMANIUM", 600, 900, vis(t, B(0, 0.4)), ts)
                C(c, "2 GOLD CONTACTS", 600, 300, vis(t, B(0, 0.5)), ts, dot=ACCENT)
                C(c, "SIGNAL AMPLIFIED", 1380, 820, vis(t, B(0, 0.8)), ts, dot=ACCENT)
                pb = vis(t, B(1, 0.0))
                if pb > 0:
                    rrect(c, 360, 940 - 1, 1200, 120, 24, "#1a0f08", 0.0)
                    T(c, "THE FIRST TRANSISTOR", 960, 215, 80, ts, ACCENT, pb)
                    C(c, "NOBEL PRIZE IN PHYSICS · 1956", 1380, 940, vis(t, B(1, 0.45)), ts, dot=ACCENT)
                    C(c, "BARDEEN · BRATTAIN · SHOCKLEY", 1380, 1020, vis(t, B(1, 0.6)), ts, size=30)
                    C(c, "2 DAYS BEFORE CHRISTMAS", 600, 1010, vis(t, B(1, 0.25)), ts, size=30)
        pb2 = phase(t, B(2, 0) - 0.3, B(3, 0))
        with Layer(c, pb2) as on:
            if on:
                logbook(c, 900, 560, 1100, 760, t, 1.0, write=prog(t, B(2, 0.45), 2.0))
                C(c, "THE SAME YEAR · HARVARD", 1600, 140, vis(t, B(2, 0.05)), ts, dot=AMBER)
                C(c, "A REAL MOTH IN A RELAY", 1600, 230, vis(t, B(2, 0.3)), ts, size=30)
        pc = phase(t, B(3, 0) - 0.3)
        with Layer(c, pc) as on:
            if on:
                q = prog(t, B(3, 0.15), 1.2)
                c.saveLayerAlpha(None, int(255 * (1 - 0.75 * q))); bench(c, t, 1.0, 0.0); c.restore()
                c.drawPaint(paint("#000000", 0.45 * q))
                T(c, "DECEMBER 1947", 960, 200, 110, ts, CREAM, 1.0)
                lw = eout(prog(t, B(3, 0.1), 0.6))
                if lw > 0: line(c, 960 - 460, 200, 960 - 460 + 920 * lw, 200, RED, 16, 1.0)
                pt = vis(t, B(3, 0.55))
                if pt > 0:
                    tube(c, 960, 960, 220, t, 1.0, pt, crown=eout(prog(t, B(3, 0.7), 0.6)))
                    C(c, "THE TUBE KEEPS ITS CROWN", 960, 1030, vis(t, B(3, 0.75)), ts, dot=ACCENT)

# ------------------------------------------------------------------ t_radio
def pocket_radio(c, x, y, s, t, a=1.0, playing=True):
    rrect(c, x - s * 0.36, y - s * 0.55, s * 0.72, s * 1.1, s * 0.08, "#c0392b", a)
    rrect(c, x - s * 0.36, y - s * 0.55, s * 0.72, s * 1.1, s * 0.08, "#ffffff", a * 0.3, stroke=s * 0.015)
    circle(c, x - s * 0.05, y + s * 0.12, s * 0.24, "#e9dcc4", a)
    for r in range(5):
        for k in range(5):
            if (r - 2) ** 2 + (k - 2) ** 2 <= 5: circle(c, x - s * 0.05 + (k - 2) * s * 0.08, y + s * 0.12 + (r - 2) * s * 0.08, s * 0.022, "#5a2a1a", a)
    circle(c, x + s * 0.18, y - s * 0.32, s * 0.12, "#e9dcc4", a); circle(c, x + s * 0.18, y - s * 0.32, s * 0.12, "#5a2a1a", a, stroke=s * 0.015)
    if playing: notes(c, x + s * 0.4, y - s * 0.4, s * 0.35, t, a)

def hearing_aid(c, x, y, s, a=1.0):
    p = skia.Path(); p.moveTo(x, y + s * 0.6); p.cubicTo(x - s * 0.5, y + s * 0.3, x - s * 0.55, y - s * 0.6, x, y - s * 0.65); p.cubicTo(x + s * 0.4, y - s * 0.6, x + s * 0.3, y - s * 0.1, x + s * 0.05, y + s * 0.05)
    c.drawPath(p, paint("#e8c9a8", a, stroke=s * 0.22))
    circle(c, x + s * 0.12, y + s * 0.2, s * 0.14, "#e8c9a8", a)

def wall_socket(c, x, y, s, a=1.0):
    rrect(c, x - s / 2, y - s / 2, s, s, s * 0.12, "#e9dcc4", a)
    for dx in (-0.15, 0.15): rect(c, x + dx * s - s * 0.03, y - s * 0.15, s * 0.06, s * 0.2, "#3a2a20", a)

def t_radio(c, W, H, t, S):
    bg_tube(c, W, H, t, S)
    B = B_(S, 3)
    with Stage(c, S) as ts:
        pa = phase(t, None, B(2, 0))
        with Layer(c, pa) as on:
            if on:
                pocket_radio(c, 520, 560, 440, t, 1.0, playing=False); notes(c, 800, 600, 120, t, 1.0)
                T(c, "1954", 520, 170, 110, ts, ACCENT, vis(t, B(0, 0.05)))
                C(c, "FIRST TRANSISTOR RADIO (U.S.)", 520, 900, vis(t, B(0, 0.2)), ts, dot=AMBER)
                C(c, "$49.95", 520, 990, vis(t, B(0, 0.45)), ts, size=40, bg="#4a2a14")
                pk = vis(t, B(1, 0.0))
                if pk > 0:
                    hearing_aid(c, 1180, 520, 240, pk)
                    donut(c, 1560, 520, 170, 0.97 * eout(prog(t, B(1, 0.4), 1.4)), AMBER, pk, label="97%", u=1.0)
                    C(c, "1953: FIRST ALL-TRANSISTOR HEARING AID", 1370, 170, vis(t, B(1, 0.1)), ts, size=30, dot=ORANGE)
                    C(c, "OF HEARING AIDS: ALL-TRANSISTOR BY 1954", 1370, 830, vis(t, B(1, 0.5)), ts, size=30)
        pb = phase(t, B(2, 0) - 0.3)
        with Layer(c, pb) as on:
            if on:
                rect(c, 0, 860, 1920, 220, "#3d271a")
                tube_radio(c, 640, 860, 560, 1.0, glow=clamp(prog(t, B(2, 0.2), 4.0)), t=t)
                wall_socket(c, 1080, 640, 90)
                p = skia.Path(); p.moveTo(900, 840); p.cubicTo(1000, 900, 1080, 860, 1080, 680); c.drawPath(p, paint("#1a1410", 1, stroke=8))
                wu = clamp(prog(t, B(2, 0.2), 4.0))
                donut(c, 640, 220, 70, wu, ACCENT, 1.0, bg="#ffffff")
                T(c, "WARMING UP..." if wu < 1 else "READY", 640, 340, 40, ts, CREAM, 1.0, w=800)
                C(c, "AS BIG AS A LOAF OF BREAD", 640, 980, vis(t, B(2, 0.1)), ts, size=30)
                pocket_radio(c, 1520, 520, 300, t, 1.0, playing=False)
                cross(c, 1520, 520, 120, vis(t, B(2, 0.35)))
                C(c, "NO POCKET RADIO", 1520, 780, vis(t, B(2, 0.35)), ts, dot=RED)
                C(c, "HEARING AIDS STAY BULKY", 1520, 870, vis(t, B(2, 0.75)), ts, size=30)

# ------------------------------------------------------------------ t_apollo
def capsule(c, x, y, s, a=1.0, ang=0.0):
    c.save(); c.translate(x, y); c.rotate(ang)
    c.drawPath(poly([(-s * 0.35, -s * 0.5), (s * 0.35, -s * 0.5), (s * 0.5, s * 0.1), (-s * 0.5, s * 0.1)]), paint("#d9dee8", a))
    rect(c, -s * 0.45, s * 0.1, s * 0.9, s * 0.9, "#b9c0cc", a)
    c.drawPath(poly([(-s * 0.2, s * 1.0), (s * 0.2, s * 1.0), (s * 0.32, s * 1.3), (-s * 0.32, s * 1.3)]), paint("#6b6e75", a))
    rect(c, -s * 0.12, -s * 0.3, s * 0.24, s * 0.2, "#1a2233", a)
    c.restore()

def moon_big(c, x, y, r, a=1.0):
    circle(c, x, y, r, "#cfc8b8", a)
    rng = random.Random(3)
    for _ in range(14):
        an = rng.random() * 6.28; d = rng.random() ** 0.6 * r * 0.8; cr = r * rng.uniform(0.04, 0.14)
        circle(c, x + math.cos(an) * d, y + math.sin(an) * d, cr, "#a39c8c", a)
    c.drawCircle(x, y, r, paint(shader=rad(x - r * 0.4, y - r * 0.4, r * 1.8, [(0, "#ffffff", 0.15), (1, "#000000", 0.55)]), a=a))

def t_apollo(c, W, H, t, S):
    bg_tube(c, W, H, t, S, dim=0.25)
    stars(c, W, H, t, 0.5, seed=44, twinkle=False)
    B = B_(S, 3)
    with Stage(c, S) as ts:
        moon_big(c, 1600, 260, 200)
        pa = phase(t, None, B(1, 0))
        with Layer(c, pa) as on:
            if on:
                capsule(c, 1250, 520 + math.sin(t) * 10, 150, 1.0, ang=20)
                rrect(c, 160, 330, 720, 470, 24, "#1a0f08", 0.9); rrect(c, 160, 330, 720, 470, 24, BRASS, 0.6, stroke=3)
                n = int(48 * clamp(prog(t, B(0, 0.3), 3)))
                for k in range(n):
                    chip_icon(c, 230 + (k % 8) * 82, 395 + (k // 8) * 70, 46, 1.0)
                C(c, "APOLLO GUIDANCE COMPUTER", 520, 230, vis(t, B(0, 0.05)), ts, dot=AMBER)
                C(c, "~2,800 CHIPS · 2 LOGIC GATES EACH", 520, 880, vis(t, B(0, 0.55)), ts, size=32)
        pb = phase(t, B(1, 0) - 0.3, B(2, 0))
        with Layer(c, pb) as on:
            if on:
                img = _cabinet_img(8, 4, "univac")
                sq = 1 + 0.02 * math.sin(t * 9) * vis(t, B(1, 0.4))
                c.save(); c.translate(520, 560); c.scale(sq, 1 / sq); c.translate(-520, -560)
                blit(c, img, 520 - img.width() / 2, 560 - img.height() / 2)
                c.restore()
                arrow(c, 900, 560, 1120, 560, CREAM, 8, vis(t, B(1, 0.3)))
                capsule(c, 1300, 560, 150, 1.0, ang=0)
                cross(c, 1300, 560, 120, vis(t, B(1, 0.5)))
                C(c, "NO TRANSISTORS = NO CHIPS", 520, 180, vis(t, B(1, 0.05)), ts, dot=RED)
                C(c, "TOO HEAVY · TOO POWER-HUNGRY", 1300, 860, vis(t, B(1, 0.5)), ts)
        pc = phase(t, B(2, 0) - 0.3)
        with Layer(c, pc) as on:
            if on:
                capsule(c, 1250, 420, 110, 1.0, ang=15)
                rect(c, 0, 760, 1920, 320, "#2a1a10")
                for r in range(2):
                    for k in range(6):
                        person_s(c, 220 + k * 150, 840 + r * 110, 90, "#0b0604", 1.0)
                        rrect(c, 160 + k * 150, 800 + r * 110, 120, 44, 8, "#5a3a22")
                        rect(c, 175 + k * 150, 770 + r * 110, 40, 30, "#1a2a20"); rect(c, 180 + k * 150, 774 + r * 110, 30, 20, GREEN, 0.6)
                q = prog(t, B(2, 0.2), 1.0)
                dashed = [(1060 + i * (1250 - 1060) / 20, 800 - i * (420 - 800) / -20) for i in range(21)]
                p = skia.Path(); p.moveTo(1060, 800); p.lineTo(lerp(1060, 1250, q), lerp(800, 470, q))
                c.drawPath(p, paint(AMBER, q, stroke=5, dash=([18, 12], -t * 40)))
                C(c, "HARDER, NOT IMPOSSIBLE", 960, 150, vis(t, B(2, 0.05)), ts, size=40, dot=AMBER)
                C(c, "THE GROUND CREW DOES MORE OF THE THINKING", 640, 700, vis(t, B(2, 0.55)), ts, size=30)

# ------------------------------------------------------------------ t_phonecalc
def _ticker(c, x, y, t0, t, ts, a=1.0):
    n = int(max(0, t - t0) * 6.3)
    T(c, f"TUBES BURNED OUT: {n:,}", x, y - 20, 60, ts, RED, a)
    T(c, "MORE THAN 6 EVERY SECOND", x, y + 50, 32, ts, CREAM, a, w=700)
    for k in range(4):
        sd = -1 if k % 2 else 1
        pop_flash(c, x + sd * (560 + (k // 2) * 50), y - 20 + (k // 2) * 40, 40, (t * 3.15 + k / 4) % 1, a)

def _power(c, t, t0, ts, B=None, full=False):
    segs = [("8.5 W", ACCENT, 0.0), (" × ", CREAM, 0.3), ("19,000,000,000", CREAM, 0.6), (" = ", CREAM, 1.0), ("~160 GW", ORANGE, 1.3)]
    sz = fit("".join(s_ for s_, _, _ in segs), 1760, 100 * ts, 900)
    x = 960 - tw("".join(s_ for s_, _, _ in segs), sz, 900) / 2; xs = []
    for s_, cl, dt in segs:
        wd = tw(s_, sz, 900); xs.append(x + wd / 2)
        text(c, s_, x, 300, sz, cl, vis(t, t0 + dt), w=900, align="l", shadow=10); x += wd
    T(c, "PER TUBE", xs[0], 300 + sz * 0.85, 34, ts, CREAM, vis(t, t0 + 0.1), w=700)
    T(c, "TUBES", xs[2], 300 + sz * 0.85, 34, ts, CREAM, vis(t, t0 + 0.7), w=700)
    for k in range(160):
        pk = vis(t, t0 + 1.4 + k * 0.012)
        if pk <= 0: break
        power_plant(c, 220 + (k % 20) * 78, 560 + (k // 20) * 58, 48, pk)

def _pools(c, t, t0, ts):
    tube(c, 220, 520, 70, t, 1.0)
    T(c, "≈ THUMB-SIZED", 220, 590, 34, ts, CREAM, vis(t, t0), w=700)
    arrow(c, 330, 380, 470, 380, CREAM, 8, vis(t, t0 + 0.2))
    for k in range(150):
        pk = vis(t, t0 + 0.3 + k * 0.012)
        if pk <= 0: break
        pool(c, 580 + (k % 15) * 86, 220 + (k // 15) * 52, 70, pk)

def t_phonecalc(c, W, H, t, S):
    o = S.opts; mode = o.get("mode", "full")
    bg_tube(c, W, H, t, S)
    with Stage(c, S) as ts:
        if mode == "power":
            _power(c, t, 0.15, ts)
            return
        if mode == "pools":
            _pools(c, t, 0.1, ts)
            T(c, "~150 OLYMPIC POOLS", 1220, 765, 60, ts, ELEC, vis(t, 0.8))
            pk = vis(t, S.lt(0, 0.55))
            if pk > 0:
                rrect(c, 300, 880, 1320, 180, 30, "#1a0f08", 0.9 * pk)
                _ticker(c, 960, 970, S.lt(0, 0.55), t, ts, pk)
            return
        B = B_(S, 5)
        pa = phase(t, None, B(1, 0))
        with Layer(c, pa) as on:
            if on:
                phone(c, 480, 560, 640, 1.0)
                arrow(c, 760, 560, 1000, 560, CREAM, 10, vis(t, B(0, 0.3)))
                img = tube_grid_img(5, 3, 70, 128, 215, "phone_tubes")
                blit(c, img, 1380 - img.width() / 2, 560 - img.height() / 2, vis(t, B(0, 0.4)))
                C(c, "REBUILD ONE PHONE CHIP WITH TUBES", 960, 120, vis(t, B(0, 0.05)), ts, dot=AMBER)
        pb = phase(t, B(1, 0) - 0.3, B(3, 0))
        with Layer(c, pb) as on:
            if on:
                _power(c, t, B(1, 0.15), ts)
                C(c, "≈ 160 LARGE POWER PLANTS", 700, 1010, vis(t, B(2, 0.0)), ts, size=40, dot=ORANGE)
                C(c, "FOR ONE PHONE", 1400, 1010, vis(t, B(2, 0.5)), ts, size=40, bg="#5a1a10")
        pc = phase(t, B(3, 0) - 0.3)
        with Layer(c, pc) as on:
            if on:
                _pools(c, t, B(3, 0.1), ts)
                T(c, "~150 OLYMPIC POOLS OF TUBES", 1220, 790, 60, ts, ELEC, vis(t, B(3, 0.6)))
                pk = vis(t, B(4, 0.0))
                if pk > 0:
                    rrect(c, 300, 880, 1320, 180, 30, "#1a0f08", 0.9 * pk)
                    _ticker(c, 960, 970, B(4, 0.0), t, ts, pk)

# ------------------------------------------------------------------ t_world
def laptop(c, x, y, s, a=1.0, on=1.0):
    rrect(c, x - s * 0.5, y - s * 0.62, s, s * 0.6, s * 0.04, "#2a2a30", a)
    rect(c, x - s * 0.45, y - s * 0.58, s * 0.9, s * 0.52, mix("#05050a", "#4a6a9a", on), a)
    c.drawPath(poly([(x - s * 0.62, y + s * 0.04), (x - s * 0.5, y - s * 0.02), (x + s * 0.5, y - s * 0.02), (x + s * 0.62, y + s * 0.04)]), paint("#4a4a52", a))

def globe_icon(c, x, y, r, a=1.0, col_=ELEC):
    circle(c, x, y, r, col_, a, stroke=r * 0.08)
    oval(c, x, y, r * 0.45, r, col_, a, stroke=r * 0.06); line(c, x - r, y, x + r, y, col_, r * 0.06, a)
    line(c, x - r * 0.85, y - r * 0.5, x + r * 0.85, y - r * 0.5, col_, r * 0.05, a); line(c, x - r * 0.85, y + r * 0.5, x + r * 0.85, y + r * 0.5, col_, r * 0.05, a)

def map_pin(c, x, y, s, a=1.0, col_=RED):
    p = skia.Path(); p.moveTo(x, y + s); p.cubicTo(x - s * 0.9, y, x - s * 0.7, y - s, x, y - s); p.cubicTo(x + s * 0.7, y - s, x + s * 0.9, y, x, y + s)
    c.drawPath(p, paint(col_, a)); circle(c, x, y - s * 0.35, s * 0.28, "#ffffff", a)

def tv(c, x, y, s, a=1.0, on=1.0, t=0.0):
    rrect(c, x - s * 0.6, y - s * 0.45, s * 1.2, s * 0.85, s * 0.08, "#6b3f1f", a)
    rrect(c, x - s * 0.5, y - s * 0.37, s * 0.8, s * 0.68, s * 0.12, mix("#05050a", "#9fd8c8", on), a)
    for k in range(3): circle(c, x + s * 0.46, y - s * 0.2 + k * s * 0.2, s * 0.05, "#3a210e", a)
    line(c, x - s * 0.15, y - s * 0.45, x - s * 0.35, y - s * 0.75, "#b9b2a6", s * 0.02, a); line(c, x + s * 0.05, y - s * 0.45, x + s * 0.25, y - s * 0.75, "#b9b2a6", s * 0.02, a)

def calculator(c, x, y, s, a=1.0):
    rrect(c, x - s * 0.35, y - s * 0.5, s * 0.7, s, s * 0.06, "#3a3a40", a)
    rect(c, x - s * 0.27, y - s * 0.42, s * 0.54, s * 0.2, "#8fb39a", a)
    for r in range(4):
        for k in range(3): rrect(c, x - s * 0.26 + k * s * 0.19, y - s * 0.12 + r * s * 0.14, s * 0.14, s * 0.1, s * 0.02, "#d9cbb3", a)

def watch(c, x, y, s, a=1.0):
    rect(c, x - s * 0.2, y - s * 0.6, s * 0.4, s * 1.2, "#3a3a40", a)
    rrect(c, x - s * 0.35, y - s * 0.32, s * 0.7, s * 0.64, s * 0.1, "#1a1a1e", a)
    text(c, "12:00", x, y, s * 0.2, "#ff6a5a", a, w=800)

def gamepad(c, x, y, s, a=1.0):
    rrect(c, x - s * 0.6, y - s * 0.3, s * 1.2, s * 0.6, s * 0.3, "#3a3a40", a)
    rect(c, x - s * 0.42, y - s * 0.04, s * 0.24, s * 0.08, "#d9cbb3", a); rect(c, x - s * 0.34, y - s * 0.12, s * 0.08, s * 0.24, "#d9cbb3", a)
    for dx, dy, cl in ((0.3, -0.08, RED), (0.42, 0.04, GREEN)): circle(c, x + dx * s, y + dy * s, s * 0.06, cl, a)

def city_night(c, t, a=1.0, glow=1.0):
    rng = random.Random(17); x = -20
    while x < 1940:
        bw = rng.uniform(80, 170); bh = rng.uniform(180, 520)
        rect(c, x, 1000 - bh, bw, bh + 80, "#0b0604", a)
        for wy in range(int(bh / 46) - 1):
            for wx in range(int(bw / 36)):
                if rng.random() < 0.55:
                    fl = 0.75 + 0.25 * math.sin(t * 3 + wx * 1.3 + wy * 2.1 + x)
                    rect(c, x + 12 + wx * 36, 1000 - bh + 20 + wy * 46, 16, 22, AMBER, a * glow * fl)
        x += bw + rng.uniform(6, 20)
    c.drawRect(skia.Rect.MakeLTRB(0, 700, 1920, 1080), paint(shader=lin(0, 700, 0, 1080, [(0, ORANGE, 0), (1, ORANGE, 0.25 * a * glow)])))

def t_world(c, W, H, t, S):
    bg_tube(c, W, H, t, S)
    B = B_(S, 4)
    with Stage(c, S) as ts:
        pa = phase(t, None, B(1, 0))
        with Layer(c, pa) as on:
            if on:
                rect(c, 120, 230, 1680, 620, "#1a0f08"); rrect(c, 120, 230, 1680, 620, 20, BRASS, 0.5, stroke=4)
                img = _cabinet_img(5, 3, "colossus")
                for k in range(3): blit(c, img, 200 + k * 520, 330, 0.95)
                for k in range(5):
                    q = (t * 0.25 + k / 5) % 1
                    line(c, 140 + q * 1640, 260, 140 + q * 1640 + 80, 260, ELEC, 4, 0.5)
                C(c, "AIR-CONDITIONED HALLS", 960, 170, vis(t, B(0, 0.05)), ts, dot=ELEC)
                C(c, "GOVERNMENTS + BIG COMPANIES ONLY", 640, 930, vis(t, B(0, 0.35)), ts)
                house(c, 1500, 1010, 150, a=vis(t, B(0, 0.7)))
                cross(c, 1500, 940, 60, vis(t, B(0, 0.8)))
                C(c, "NONE AT HOME", 1500, 760, vis(t, B(0, 0.8)), ts, dot=RED)
        pb = phase(t, B(1, 0) - 0.3, B(3, 0))
        with Layer(c, pb) as on:
            if on:
                row1 = [("LAPTOP", lambda x, y, a: laptop(c, x, y + 60, 220, a, 0.6)), ("SMARTPHONE", lambda x, y, a: phone(c, x, y, 230, a)),
                        ("INTERNET", lambda x, y, a: globe_icon(c, x, y, 100, a)), ("MAP IN YOUR POCKET", lambda x, y, a: map_pin(c, x, y, 100, a))]
                for k, (lab, fn) in enumerate(row1):
                    x = 300 + k * 440; pk = vis(t, B(1, 0.05 + k * 0.15))
                    if pk <= 0: continue
                    fn(x, 330, pk); cross(c, x, 330, 90, vis(t, B(1, 0.12 + k * 0.15)))
                    T(c, lab, x, 500, 36, ts, CREAM, pk, w=800, maxw=400)
                row2 = [("TV", lambda x, y, a: tv(c, x, y, 190, a, 0.8), True), ("RADIO", lambda x, y, a: tube_radio(c, x, y + 90, 220, a, 0.8, t), True),
                        ("CALCULATOR", lambda x, y, a: calculator(c, x, y, 190, a), False), ("DIGITAL WATCH", lambda x, y, a: watch(c, x, y, 170, a), False),
                        ("GAME CONSOLE", lambda x, y, a: gamepad(c, x, y, 190, a), False)]
                for k, (lab, fn, ok) in enumerate(row2):
                    x = 220 + k * 370; pk = vis(t, B(2, 0.05 + k * 0.14))
                    if pk <= 0: continue
                    fn(x, 760, pk)
                    if ok: check(c, x + 120, 680, 36, pk)
                    else: cross(c, x, 760, 80, vis(t, B(2, 0.1 + k * 0.14)))
                    T(c, lab, x, 940, 34, ts, GREEN if ok else CREAM, pk, w=800, maxw=340)
        pc = phase(t, B(3, 0) - 0.3)
        with Layer(c, pc) as on:
            if on:
                c.drawPaint(paint("#05030a", 0.6))
                city_night(c, t, 1.0)
                for k in range(3):
                    p = skia.Path()
                    for i in range(121):
                        xx = 360 + i * 10; yy = 230 + k * 50 + math.sin(i * 0.35 + t * 8 + k) * 18 * math.sin(i / 120 * math.pi)
                        (p.moveTo if i == 0 else p.lineTo)(xx, yy)
                    c.drawPath(p, paint(AMBER, 0.5 - k * 0.12, stroke=4))
                C(c, "HUMMING, GLOWING CITIES", 960, 120, vis(t, B(3, 0.1)), ts, dot=ORANGE)

# ------------------------------------------------------------------ t_still
def microwave(c, x, y, s, a=1.0, t=0.0):
    rrect(c, x - s * 0.7, y - s * 0.4, s * 1.4, s * 0.8, s * 0.06, "#d9d2c4", a)
    rrect(c, x - s * 0.6, y - s * 0.3, s * 0.9, s * 0.6, s * 0.04, "#2a2420", a)
    circle(c, x - s * 0.15, y, s * 0.2, AMBER, a * (0.25 + 0.1 * math.sin(t * 5)), blur=s * 0.08)
    for k in range(3): circle(c, x + s * 0.52, y - s * 0.2 + k * s * 0.18, s * 0.05, "#3a3a40", a)

def magnetron(c, x, y, s, a=1.0):
    circle(c, x, y, s, "#b87333", a); circle(c, x, y, s * 0.35, "#1a1410", a)
    for k in range(8):
        an = k * math.pi / 4; circle(c, x + math.cos(an) * s * 0.62, y + math.sin(an) * s * 0.62, s * 0.14, "#1a1410", a)
        line(c, x + math.cos(an) * s * 0.35, y + math.sin(an) * s * 0.35, x + math.cos(an) * s * 0.5, y + math.sin(an) * s * 0.5, "#1a1410", s * 0.06, a)

def xray_tube(c, x, y, s, t, a=1.0):
    oval(c, x, y, s, s * 0.32, "#e6eef5", a * 0.25); oval(c, x, y, s, s * 0.32, CREAM, a * 0.7, stroke=4)
    rect(c, x - s * 0.7, y - s * 0.06, s * 0.35, s * 0.12, "#8d9098", a)
    c.drawPath(poly([(x + s * 0.25, y - s * 0.18), (x + s * 0.45, y + s * 0.15), (x + s * 0.25, y + s * 0.15)]), paint("#b87333", a))
    for k in range(5):
        q = (t * 1.2 + k / 5) % 1
        circle(c, lerp(x - s * 0.35, x + s * 0.3, q), y, 5, ELEC, a)
    for k in range(4):
        an = math.radians(70 + k * 12)
        line(c, x + s * 0.35, y + s * 0.1, x + s * 0.35 + math.cos(an) * s * 0.9, y + s * 0.1 + math.sin(an) * s * 0.9, "#c9a0ff", 4, a * 0.6, dash=([14, 10], -t * 40))

def amp_box(c, x, y, s, t, a=1.0):
    rrect(c, x - s * 0.6, y - s * 0.55, s * 1.2, s * 0.85, s * 0.04, "#1a1410", a)
    rect(c, x - s * 0.52, y - s * 0.3, s * 1.04, s * 0.52, "#c8a878", a)
    for k in range(14): line(c, x - s * 0.5 + k * s * 0.075, y - s * 0.3, x - s * 0.5 + k * s * 0.075, y + s * 0.22, "#a08060", s * 0.012, a)
    rect(c, x - s * 0.52, y - s * 0.5, s * 1.04, s * 0.16, "#2a2420", a)
    for k in range(6): circle(c, x - s * 0.4 + k * s * 0.13, y - s * 0.42, s * 0.035, "#d9cbb3", a)
    for k in range(4): tube(c, x - s * 0.36 + k * s * 0.24, y - s * 0.55, s * 0.13, t, 1.0, a, seed=k)

def guitar(c, x, y, s, a=1.0, ang=-30):
    c.save(); c.translate(x, y); c.rotate(ang)
    rect(c, s * 0.1, -s * 0.035, s * 0.85, s * 0.07, "#5a3a22", a)
    for k in range(5): line(c, s * 0.25 + k * s * 0.13, -s * 0.035, s * 0.25 + k * s * 0.13, s * 0.035, "#c9c2b6", s * 0.01, a)
    rrect(c, s * 0.92, -s * 0.07, s * 0.18, s * 0.14, s * 0.03, "#2a1a10", a)
    circle(c, -s * 0.22, 0, s * 0.27, "#b8442a", a); circle(c, s * 0.08, 0, s * 0.2, "#b8442a", a)
    rect(c, -s * 0.05, -s * 0.16, s * 0.12, s * 0.32, "#b8442a", a)
    circle(c, -s * 0.02, 0, s * 0.07, "#1a1410", a)
    rect(c, -s * 0.33, -s * 0.09, s * 0.06, s * 0.18, "#2a1a10", a)
    for k in range(4): line(c, -s * 0.3, -s * 0.03 + k * s * 0.02, s * 1.0, -s * 0.03 + k * s * 0.02, "#e9e2d0", s * 0.004, a)
    c.restore()

def t_still(c, W, H, t, S):
    bg_tube(c, W, H, t, S)
    B = B_(S, 2)
    with Stage(c, S) as ts:
        pa = phase(t, None, B(1, 0))
        with Layer(c, pa) as on:
            if on:
                microwave(c, 480, 480, 380, 1.0, t)
                magnetron(c, 480, 820, 80, vis(t, B(0, 0.3)))
                C(c, "MICROWAVE OVEN: MAGNETRON = A VACUUM TUBE", 760, 140, vis(t, B(0, 0.1)), ts, size=32, dot=AMBER)
                xray_tube(c, 1400, 480, 300, t, vis(t, B(0, 0.6)))
                C(c, "X-RAY MACHINES: AN X-RAY TUBE", 1400, 820, vis(t, B(0, 0.65)), ts, size=32, dot="#c9a0ff")
        pb = phase(t, B(1, 0) - 0.3)
        with Layer(c, pb) as on:
            if on:
                rect(c, 0, 900, 1920, 180, "#3d271a")
                amp_box(c, 760, 840, 600, t, 1.0)
                guitar(c, 1360, 640, 520, 1.0, ang=-35)
                notes(c, 1180, 300, 90, t, 1.0)
                C(c, "TUBE AMPS: \"WARM, CRUNCHY SOUND\"", 960, 120, vis(t, B(1, 0.1)), ts, dot=ORANGE)

# ------------------------------------------------------------------ t_mig
def jet(c, x, y, s, a=1.0, ang=0.0, col_="#9aa4b0"):
    """Generic swept-wing twin-tail jet silhouette, plan view, nose to the right. No markings."""
    c.save(); c.translate(x, y); c.rotate(ang)
    c.drawPath(poly([(s * 1.0, 0), (s * 0.7, -s * 0.07), (-s * 0.85, -s * 0.09), (-s * 0.95, 0), (-s * 0.85, s * 0.09), (s * 0.7, s * 0.07)]), paint(col_, a))
    for sd in (-1, 1):
        c.drawPath(poly([(s * 0.25, sd * s * 0.08), (-s * 0.35, sd * s * 0.7), (-s * 0.55, sd * s * 0.7), (-s * 0.35, sd * s * 0.08)]), paint(col_, a))
        c.drawPath(poly([(-s * 0.6, sd * s * 0.08), (-s * 0.85, sd * s * 0.38), (-s * 0.95, sd * s * 0.38), (-s * 0.85, sd * s * 0.08)]), paint(mix(col_, "#000000", 0.15), a))
    oval(c, s * 0.62, 0, s * 0.12, s * 0.04, "#2a3a4a", a)
    c.restore()

def avionics_bay(c, x, y, w, h, t, a=1.0):
    rrect(c, x, y, w, h, 16, "#3a3f46", a); rect(c, x + 16, y + 16, w - 32, h - 32, "#14100c", a)
    img = tube_grid_img(7, 2, 54, 92, 150, "bay_tubes")
    blit(c, img, x + w / 2 - img.width() / 2, y + h / 2 - img.height() / 2 - 10, a)

def nano_vacuum(c, x, y, s, t, a=1.0):
    rect(c, x - s, y, s * 2, s * 0.5, "#4a5a7a", a)
    T(c, "SILICON CHIP", x, y + s * 0.27, 34, 1.0, "#d9e3ff", a, w=700)
    c.drawPath(poly([(x - s * 0.8, y), (x - s * 0.8, y - s * 0.35), (x - s * 0.12, y - s * 0.35), (x - s * 0.04, y - s * 0.2), (x - s * 0.12, y)]), paint("#c0c4cc", a))
    rect(c, x + s * 0.12, y - s * 0.35, s * 0.68, s * 0.35, "#c0c4cc", a)
    rect(c, x - s * 0.5, y - s * 0.62, s * 1.0, s * 0.1, BRASS, a)
    for k in range(6):
        q = (t * 1.5 + k / 6) % 1
        circle(c, lerp(x - s * 0.04, x + s * 0.12, q), y - s * 0.2 + math.sin(k) * 6, 6, ELEC, a)
    T(c, "NANOMETER-WIDE VACUUM GAP", x, y - s * 0.75, 34, 1.0, CREAM, a, w=700)

def t_mig(c, W, H, t, S):
    o = S.opts; mode = o.get("mode", "long")
    bg_tube(c, W, H, t, S)
    with Stage(c, S) as ts:
        if mode == "short":
            jet(c, 560, 420, 380, 1.0, ang=-8 + math.sin(t) * 2)
            avionics_bay(c, 1000, 260, 820, 420, t, vis(t, 0.5))
            C(c, "1970s FIGHTER JET", 560, 780, vis(t, 0.2), ts, dot=AMBER)
            C(c, "TUBE ELECTRONICS", 1410, 780, vis(t, 0.9), ts, dot=ORANGE)
            return
        B = B_(S, 3)
        pa = phase(t, None, B(1, 0))
        with Layer(c, pa) as on:
            if on:
                q = clamp(prog(t, B(0, 0.0), 6.0))
                # sea + runway
                c.drawRect(skia.Rect.MakeLTRB(0, 640, 1920, 1080), paint(shader=lin(0, 640, 0, 1080, [(0, "#1d2a3a", 1), (1, "#0b1018", 1)])))
                c.drawPath(poly([(1500, 640), (1920, 600), (1920, 1080), (1400, 1080)]), paint("#3a3324"))
                rect(c, 1560, 760, 360, 40, "#5a5a5a");
                for k in range(6): rect(c, 1580 + k * 56, 776, 30, 8, "#e9e2d0")
                jx = lerp(200, 1600, ease(q)); jy = lerp(420, 700, ease(q) ** 2)
                jet(c, jx, jy, 260, 1.0, ang=lerp(-5, 8, q))
                C(c, "1976 · A SOVIET PILOT FLIES TO JAPAN", 760, 140, vis(t, B(0, 0.05)), ts, dot=AMBER)
                pb = vis(t, B(0, 0.55))
                if pb > 0:
                    rrect(c, 260, 220, 1400, 640, 24, "#1a0f08", 0.92 * pb)
                    avionics_bay(c, 340, 280, 1240, 460, t, pb)
                    C(c, "MUCH OF ITS ELECTRONICS: VACUUM TUBES", 960, 800, vis(t, B(0, 0.7)), ts, dot=ORANGE)
        pb2 = phase(t, B(1, 0) - 0.3, B(2, 0))
        with Layer(c, pb2) as on:
            if on:
                tube(c, 560, 900, 300, t, 1.0)
                chip_icon(c, 1360, 620, 260, 1.0)
                rng = random.Random(int(t * 10))
                for k in range(14):
                    q = (t * 0.9 + k / 14) % 1; yy = 160 + k * 55
                    for (tx, hit) in ((560, 680), (1360, 1360)):
                        xx = lerp(tx - 500, tx, q)
                        line(c, xx - 40, yy - 20, xx, yy, "#c9a0ff", 4, 0.7 * math.sin(q * math.pi))
                pc = vis(t, B(1, 0.4))
                if pc > 0:
                    for k in range(5):
                        an = rng.uniform(0, 6.28)
                        line(c, 1360, 620, 1360 + math.cos(an) * rng.uniform(40, 150), 620 + math.sin(an) * rng.uniform(40, 150), RED, 5, pc)
                C(c, "TUBES: TOUGH IN RADIATION", 560, 1000, vis(t, B(1, 0.3)), ts, dot=GREEN)
                C(c, "EARLY TRANSISTORS: FRAGILE", 1360, 1000, vis(t, B(1, 0.45)), ts, dot=RED)
        pc2 = phase(t, B(2, 0) - 0.3)
        with Layer(c, pc2) as on:
            if on:
                nano_vacuum(c, 960, 640, 520, t, 1.0)
                C(c, "NASA AMES: A NANOSCALE VACUUM TRANSISTOR", 960, 110, vis(t, B(2, 0.05)), ts, size=34, dot=ELEC)
                T(c, "460 GHz", 960, 980, 100, ts, ACCENT, vis(t, B(2, 0.6)))
                C(c, "EARLY TESTS", 1400, 980, vis(t, B(2, 0.75)), ts, size=28)

# ------------------------------------------------------------------ t_patent
def patent_doc(c, x, y, s, t, a=1.0, rot=-3, title="FIELD-EFFECT DEVICE"):
    w, h = s * 0.78, s
    doc_paper(c, x, y, w, h, a, rot)
    c.save(); c.translate(x, y); c.rotate(rot)
    text(c, "PATENT", 0, -h * 0.42, s * 0.06, INK, a, w=900, fam="Inter")
    text(c, title, 0, -h * 0.35, s * 0.035, INK, a, w=700, fam="Inter")
    # drawing: a slab with three electrodes
    rect(c, -w * 0.32, -h * 0.18, w * 0.64, h * 0.12, "#00000000", 0)
    c.drawRect(skia.Rect.MakeXYWH(-w * 0.32, -h * 0.18, w * 0.64, h * 0.12), paint(INK, a, stroke=3))
    for dx in (-0.25, 0.0, 0.25):
        c.drawRect(skia.Rect.MakeXYWH(dx * w - w * 0.05, -h * 0.25, w * 0.1, h * 0.07), paint(INK, a, stroke=3))
        line(c, dx * w, -h * 0.25, dx * w, -h * 0.3, INK, 3, a)
    for k in range(3): text(c, str(10 + k), (-0.25 + k * 0.25) * w + w * 0.08, -h * 0.29, s * 0.025, INK, a, w=500, fam="Inter")
    ruled_lines(c, -w * 0.4, h * 0.02, w * 0.8, 9, h * 0.045, a * 0.8, colr="#6a6a7a", seed=5)
    c.restore()

def t_patent(c, W, H, t, S):
    bg_tube(c, W, H, t, S)
    B = B_(S, 3)
    with Stage(c, S) as ts:
        pa = phase(t, None, B(1, 0))
        with Layer(c, pa) as on:
            if on:
                T(c, "22 YEARS EARLY", 960, 330, 160, ts, ACCENT, vis(t, 0.3))
                q = eout(prog(t, 0.6, 1.5))
                line(c, 360, 640, 360 + 1200 * q, 640, CREAM, 8)
                for x_, yr, tq in ((360, "1925", 0.6), (1560, "1947", 1.8)):
                    pk = vis(t, tq)
                    circle(c, x_, 640, 20, AMBER, pk)
                    T(c, yr, x_, 740, 80, ts, CREAM, pk)
        pb = phase(t, B(1, 0) - 0.3, B(2, 0))
        with Layer(c, pb) as on:
            if on:
                patent_doc(c, 600, 560, 900, t, 1.0)
                T(c, "1925", 1380, 230, 120, ts, ACCENT, vis(t, B(1, 0.05)))
                C(c, "FILED IN CANADA", 1380, 360, vis(t, B(1, 0.1)), ts, dot=AMBER)
                C(c, "JULIUS LILIENFELD", 1380, 460, vis(t, B(1, 0.2)), ts)
                C(c, "CURRENT IN A SOLID, CONTROLLED BY AN ELECTRIC FIELD", 1280, 620, vis(t, B(1, 0.45)), ts, size=26)
                T(c, "= A FIELD-EFFECT TRANSISTOR", 1380, 760, 52, ts, ELEC, vis(t, B(1, 0.75)), maxw=880)
        pc = phase(t, B(2, 0) - 0.3)
        with Layer(c, pc) as on:
            if on:
                patent_doc(c, 480, 560, 760, t, 1.0)
                C(c, "NO WORKING VERSION (AS FAR AS WE KNOW)", 480, 1010, vis(t, B(2, 0.05)), ts, size=28, dot=RED)
                C(c, "THE ULTRA-PURE MATERIALS DIDN'T EXIST YET", 480, 110, vis(t, B(2, 0.2)), ts, size=28)
                for k in range(3):
                    doc_paper(c, 1300 + k * 60, 520 + k * 40, 520, 640, vis(t, B(2, 0.4) + k * 0.2), rot=4 - k * 3, col_="#e9e2d0")
                pk = vis(t, B(2, 0.5))
                if pk > 0:
                    c.save(); c.translate(1420, 600); c.rotate(1)
                    text(c, "LATE-1940s PATENT CLAIMS", 0, -230, 34, INK, pk, w=800, fam="Inter")
                    ruled_lines(c, -200, -150, 400, 8, 36, pk * 0.8, colr="#6a6a7a", seed=9)
                    c.restore()
                stamp(c, "REJECTED", 1420, 640, prog(t, B(2, 0.7), 0.35), 1.0, color=RED, rot=-14, size=100)

# ------------------------------------------------------------------ t_mos
def mosfet(c, x, y, s, t, a=1.0, on=1.0):
    w = s; h = s * 0.5
    rect(c, x - w / 2, y, w, h, "#5a6e8a", a)  # silicon
    for k in range(18):
        for j in range(5): circle(c, x - w / 2 + 20 + k * (w - 40) / 17, y + 20 + j * (h - 40) / 4, 4, "#7a90b0", a * 0.6)
    c.save(); c.clipRect(skia.Rect.MakeXYWH(x - w / 2, y, w, h))
    for dx in (-0.36, 0.36): oval(c, x + dx * w, y, w * 0.13, h * 0.2, "#3a6ad0", a)
    c.restore()
    rect(c, x - w * 0.24, y - h * 0.1, w * 0.48, h * 0.1, "#bfe6ff", a * 0.9)  # thin glass
    rect(c, x - w * 0.24, y - h * 0.36, w * 0.48, h * 0.26, BRASS, a)  # gate
    for dx in (-0.36, 0.36): rect(c, x + dx * w - w * 0.05, y - h * 0.3, w * 0.1, h * 0.3, "#b9b2a6", a)
    if on > 0:
        for k in range(10):
            q = (t * 0.7 + k / 10) % 1
            circle(c, lerp(x - w * 0.36, x + w * 0.36, q), y + h * 0.05, 7, ELEC, a * on)
    return dict(gate=(x, y - h * 0.23), glass=(x + w * 0.24, y - h * 0.05), si=(x, y + h * 0.75), src=(x - w * 0.36, y - h * 0.3), drn=(x + w * 0.36, y - h * 0.3))

def t_mos(c, W, H, t, S):
    bg_tube(c, W, H, t, S)
    B = B_(S, 3)
    with Stage(c, S) as ts:
        pa = phase(t, None, B(1, 0))
        with Layer(c, pa) as on:
            if on:
                gate_on = 1.0 if math.sin(t * 1.2) > -0.3 else 0.0
                d = mosfet(c, 700, 470, 900, t, 1.0, on=gate_on * vis(t, B(0, 0.3)))
                lab = [("METAL GATE", "gate", 0.35, ACCENT), ("THIN GLASS LAYER", "glass", 0.5, ELEC), ("SILICON", "si", 0.2, CREAM)]
                for k, (s_, key, tq, cl) in enumerate(lab):
                    pk = vis(t, B(0, tq))
                    if pk <= 0: continue
                    x0, y0 = d[key]; yy = 300 + k * 230
                    line(c, x0 + 10, y0, 1280, yy, CREAM, 3, 0.6 * pk)
                    T(c, s_, 1300, yy, 44, ts, cl, pk, align="l", w=800, maxw=560)
                C(c, "1959 · BELL LABS · ATALLA & KAHNG", 960, 110, vis(t, B(0, 0.05)), ts, dot=AMBER)
                T(c, "THE MOSFET", 700, 1000, 80, ts, ACCENT, vis(t, B(0, 0.6)))
        pb = phase(t, B(1, 0) - 0.3, B(2, 0))
        with Layer(c, pb) as on:
            if on:
                q = eout(prog(t, B(1, 0.05), 4.0))
                zeros = int(21 * q)
                s_ = "13" + "0" * zeros
                grp = ""
                for i, ch in enumerate(reversed(s_)):
                    if i and i % 3 == 0: grp = "," + grp
                    grp = ch + grp
                T(c, grp, 960, 330, 110, ts, CREAM, vis(t, B(1, 0.05)), maxw=1800)
                T(c, "13 SEXTILLION TRANSISTORS (BY 2018)", 960, 470, 60, ts, ACCENT, vis(t, B(1, 0.3)))
                pk = vis(t, B(1, 0.6))
                donut(c, 760, 760, 150, 0.999 * eout(prog(t, B(1, 0.6), 1.2)), ELEC, pk, label="99.9%", u=1.0)
                T(c, "WERE MOSFETS", 1180, 760, 64, ts, CREAM, pk, align="l")
        pc = phase(t, B(2, 0) - 0.3)
        with Layer(c, pc) as on:
            if on:
                mosfet(c, 960, 640, 640, t, 1.0)
                crown_icon(c, 960, 430, 120, eout(prog(t, B(2, 0.2), 0.6)))
                T(c, "THE MOST MANUFACTURED THING", 960, 150, 80, ts, ACCENT, vis(t, B(2, 0.05)))
                T(c, "IN HUMAN HISTORY", 960, 260, 80, ts, CREAM, vis(t, B(2, 0.2)))

# ------------------------------------------------------------------ t_moth (Short)
def relay_panel(c, x0, y0, cols, rows, sp, t, a=1.0, hl=None, click=0.0, moth_at=None):
    rrect(c, x0 - 40, y0 - 60, cols * sp + 80, rows * sp + 80, 16, "#2b1d14", a)
    rrect(c, x0 - 40, y0 - 60, cols * sp + 80, rows * sp + 80, 16, BRASS, a * 0.5, stroke=4)
    n = 0
    for r in range(rows):
        for k in range(cols):
            n += 1
            cl = 0.0
            if click > 0: cl = 1.0 if math.sin(t * 9 + r * 1.3 + k * 2.1) > 0 else 0.0
            relay(c, x0 + k * sp + sp / 2, y0 + r * sp + sp / 2, sp * 0.8, a, closed=cl, hl=(hl if (r, k) == moth_at else 0))
    if moth_at:
        r, k = moth_at
        moth(c, x0 + k * sp + sp * 0.62, y0 + r * sp + sp * 0.32, sp * 0.32, a, t=t, ang=20)

def t_moth(c, W, H, t, S):
    o = S.opts; mode = o.get("mode", "intro")
    bg_tube(c, W, H, t, S)
    with Stage(c, S) as ts:
        if mode == "intro":
            circle(c, 960, 520, 420, "#fff1b8", 0.12, blur=80)
            rrect(c, 560, 220, 800, 620, 20, "#e6eef5", 0.08); rrect(c, 560, 220, 800, 620, 20, CREAM, 0.6, stroke=5)
            moth(c, 960, 520, 230 * eout(prog(t, 0.1, 0.8)), 1.0, t=t)
            rect(c, 520, 860, 880, 60, "#3d271a")
        elif mode in ("relay", "click"):
            mo = (2, 5)
            relay_panel(c, 260, 180, 9, 4, 160, t, 1.0, hl=vis(t, 0.8) if mode == "relay" else 0.0, click=1.0 if mode == "click" else 0.0, moth_at=mo)
            if mode == "relay":
                C(c, "HARVARD MARK II", 520, 1000, vis(t, 0.2), ts, dot=AMBER)
                C(c, "RELAY #70", 1400, 1000, vis(t, 1.0), ts, dot=ACCENT)
            else:
                pk = vis(t, S.lt(0, 0.6))
                if pk > 0:
                    x, y = 260 + 5 * 160 + 80, 180 + 2 * 160 + 80
                    circle(c, x, y, 110, RED, 0.25 * pk, blur=30); xmark(c, x + 120, y - 90, 40, pk, colr=RED)
                C(c, "CLICKED BY MAGNETS", 540, 1000, vis(t, 0.2), ts, dot=AMBER)
                C(c, "CIRCUIT FAILS", 1480, 1000, vis(t, S.lt(0, 0.6)), ts, dot=RED)
        elif mode == "log":
            logbook(c, 960, 540, 1500, 980, t, 1.0, write=prog(t, 0.6, 2.5), rot=-2, fs=68, ms=120)
        elif mode == "edison":
            doc_paper(c, 700, 560, 700, 860, 1.0, rot=4, col_="#e8d6b0")
            c.save(); c.translate(700, 560); c.rotate(4)
            text(c, "1878", 230, -360, 50, INK, 1.0, w=700, fam="Inter")
            ruled_lines(c, -290, -260, 580, 13, 42, 0.8, colr="#4a4a6a", seed=11)
            pk = vis(t, 0.8)
            rect(c, -60, -40, 230, 70, "#e8d6b0", 1.0)
            text(c, "\"bugs\"", 55, -6, 54, INK, 1.0, w=700, fam="Inter Display")
            if pk > 0: c.drawOval(skia.Rect.MakeLTRB(-90, -70, 200, 60), paint(RED, pk, stroke=8))
            c.restore()
            T(c, "\"BUG\" = A GLITCH", 1440, 420, 80, ts, ACCENT, vis(t, 1.2), maxw=760)
            T(c, "ALREADY SLANG", 1440, 560, 70, ts, CREAM, vis(t, 2.0), maxw=760)
        elif mode == "museum":
            rect(c, 0, 860, 1920, 220, "#1a0f08")
            circle(c, 960, 300, 500, "#fff1b8", 0.10, blur=90)
            c.drawPath(poly([(760, 40), (1160, 40), (1380, 860), (540, 860)]), paint("#fff1b8", 0.06))
            rect(c, 560, 760, 800, 120, "#3d271a")
            logbook(c, 960, 520, 520, 380, t, 1.0, write=1.0, rot=0)
            rrect(c, 640, 290, 640, 470, 10, "#e6eef5", 0.10); rrect(c, 640, 290, 640, 470, 10, CREAM, 0.7, stroke=4)
            C(c, "GRACE HOPPER MADE IT FAMOUS", 960, 140, vis(t, 0.2), ts, dot=AMBER)
            C(c, "NOW AT THE SMITHSONIAN", 960, 990, vis(t, S.lt(0, 0.6)), ts)
    kit.hook(c, W, H, t, S)

# ------------------------------------------------------------------ t_blackout (Short)
def card_terminal(c, x, y, s, a=1.0, on=1.0):
    rrect(c, x - s * 0.3, y - s * 0.5, s * 0.6, s, s * 0.08, "#2a2a30", a)
    rect(c, x - s * 0.22, y - s * 0.42, s * 0.44, s * 0.25, mix("#05050a", "#7bd88f", on), a)
    for r in range(3):
        for k in range(3): rrect(c, x - s * 0.2 + k * s * 0.15, y - s * 0.08 + r * s * 0.15, s * 0.1, s * 0.1, s * 0.02, "#6a6a72", a)

def water_pump(c, x, y, s, a=1.0, on=1.0, t=0.0):
    rect(c, x - s * 0.5, y - s * 0.3, s * 0.7, s * 0.3, "#5a6e8a", a)
    circle(c, x + s * 0.3, y - s * 0.3, s * 0.25, "#7a90b0", a)
    rect(c, x + s * 0.5, y - s * 0.38, s * 0.5, s * 0.14, "#7a90b0", a)
    if on > 0:
        for k in range(4):
            q = (t + k / 4) % 1
            circle(c, x + s * (1.0 + q * 0.3), y - s * 0.3 + q * q * s * 0.5, s * 0.05, ELEC, a * on)

def t_blackout(c, W, H, t, S):
    o = S.opts; mode = o.get("mode", "intro")
    bg_tube(c, W, H, t, S)
    off = eout(prog(t, S.lt(0, 0.45), 0.8))
    with Stage(c, S) as ts:
        if mode == "intro":
            for r in range(4):
                for k in range(9):
                    d = abs(k - 4) + abs(r - 1.5)
                    oo = eout(prog(t, 0.6 + d * 0.15, 0.3))
                    chip_icon(c, 330 + k * 158, 230 + r * 180, 100, 1.0, glow=1 - oo)
                    if oo > 0: rrect(c, 330 + k * 158 - 32, 230 + r * 180 - 32, 64, 64, 6, "#000000", 0.6 * oo)
        elif mode == "phones":
            items = [lambda a, on: phone(c, 300, 520, 400, a, screen=on), lambda a, on: laptop(c, 750, 640, 420, a, on),
                     lambda a, on: card_terminal(c, 1200, 520, 300, a, on), lambda a, on: tv(c, 1620, 560, 360, a, on, t)]
            for k, fn in enumerate(items):
                on = 1 - eout(prog(t, 0.6 + k * 0.6, 0.3))
                fn(1.0, max(0.0, on))
                if on < 0.5: cross(c, [300, 750, 1200, 1620][k], 520, 70, 1 - on)
        elif mode == "cars":
            rect(c, 0, 820, 1920, 260, "#2a2420")
            for k in range(3):
                car(c, 420 + k * 540, 820, 380, 1.0, col_=["#7a8a9a", "#9a6a5a", "#8a8a7a"][k])
                pk = vis(t, 0.8 + k * 0.5)
                if pk > 0: C(c, "WON'T START", 420 + k * 540, 460, pk, ts, dot=RED, size=30)
            C(c, "2021: JUST A CHIP SHORTAGE", 960, 1000, vis(t, S.lt(0, 0.35)), ts, dot=AMBER)
        elif mode == "grid":
            dk = eout(prog(t, 0.8, 3.0))
            city_night(c, t, 1.0, glow=1 - dk)
            pylon(c, 300, 760, 420, 1.0)
            traffic_light(c, 1550, 760, 300, 1.0, on=1 - dk, t=t)
            water_pump(c, 900, 760, 300, 1.0, on=1 - dk, t=t)
            c.drawPaint(paint("#000000", 0.45 * dk))
            C(c, "LIGHTS GOING OUT", 960, 120, vis(t, 1.2), ts, dot=RED)
        elif mode == "works":
            rect(c, 0, 840, 1920, 240, "#2a1a10")
            items = [(300, lambda a: wind_clock(c, 300, 560, 150, t * 3, a), "WIND-UP CLOCK"),
                     (760, lambda a: bicycle(c, 760, 720, 330, t, a), "BICYCLE"),
                     (1210, lambda a: car(c, 1210, 840, 380, a, col_="#3a5a4a", old=True), "OLD CAR"),
                     (1660, lambda a: tube_radio(c, 1660, 840, 360, a, 1.0, t), "TUBE RADIO")]
            for k, (x, fn, lab) in enumerate(items):
                pk = vis(t, 0.2 + k * 0.8)
                if pk <= 0: continue
                fn(pk); check(c, x + 130, 320, 40, pk)
                T(c, lab, x, 950, 46, ts, GREEN, pk, maxw=420)
    kit.hook(c, W, H, t, S)

SCENES = {k: v for k, v in globals().items() if k.startswith("t_") and callable(v)}
