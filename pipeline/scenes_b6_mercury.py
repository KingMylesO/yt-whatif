"""Batch 06 scenes: What If You Lived on Mercury? (+ teaser, Mercury-day and Voyager 1 Shorts).

Look: "scorched glare". Near-black shadow backgrounds with a copper/ember sun-glare bleeding in from the upper left,
a textured copper-grey Mercury lit hard from one side, and a lens-flare chain (the motif) running from the Sun
across the frame. Cold accents (ice cyan, night blue) only where the story turns cold.
short_b6_mday has its own twilight-violet + gold clock look; short_b6_voyager is deep-space blue with a signal-cyan beam.
Every scene draws on a virtual 1920x1080 stage (Stage). In Shorts the stage is scaled into the 0.255H..0.58H band
and text sizes are multiplied by ts=1.75. Multi-part scenes are time-ordered panels.
"""
from common2 import *
import scenes_b3_kit as kit

VW, VH = 1920, 1080
BG_T, BG_B = "#08050a", "#1d0f0b"
COPPER = "#e07a3c"; SCORCH = "#ff9440"; EMBER = "#ff5a24"; GLARE = "#fff3d6"
ROCK = "#9b8d84"; ROCK_D = "#4b413d"; ICE = "#8fe9ff"; NIGHT = "#5b7cff"; RED = "#ff5b5b"; GREEN = "#7dffb0"
YEL = ACCENT; CHIPBG = "#2b150d"; MAGC = "#c79bff"
PAL = dict(accent=SCORCH, chip="#3a1a0e", title2=ACCENT)
# short_b6_mday: twilight violet + gold
MD_T, MD_B, GOLD, VIO = "#140a26", "#3b1a3e", "#ffcf5a", "#b48cff"
PAL_MD = dict(accent=GOLD, chip="#2a1640", title2=GOLD)
# short_b6_voyager: deep-space blue
VY_T, VY_B, SIG, VGOLD = "#01040f", "#0a1b3d", "#59d0ff", "#e8c26a"
PAL_VY = dict(accent=SIG, chip="#0d2350", title2=SIG)

# ------------------------------------------------------------------ stage + text helpers
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
    if a <= 0: return
    fam = kw.pop("fam", "Inter Display")
    sz = fit(s, maxw, size * ts, w, fam)
    text(c, s, x, y, sz, colr, a, w=w, fam=fam, shadow=kw.pop("shadow", 10), **kw)

def stage_bg(c, top, bot, a=1.0):
    c.drawRect(skia.Rect.MakeXYWH(0, 0, VW, VH), paint(shader=lin(0, 0, 0, VH, [(0, top, a), (1, bot, a)])))

_BG = {}
def bg_img(W, H, look="me"):
    k = (W, H, look)
    if k not in _BG:
        surf = skia.Surface(W, H); cc = surf.getCanvas(); M = max(W, H)
        if look == "me":
            fill_bg(cc, W, H, BG_T, BG_B)
            cc.drawPaint(paint(shader=rad(W * 0.05, H * 0.02, M * 0.85, [(0, "#ff8a3a", 0.30), (0.35, "#a8401a", 0.12), (1, "#000000", 0)])))
            cc.drawPaint(paint(shader=rad(W * 0.95, H * 1.0, M * 0.6, [(0, "#3a1408", 0.35), (1, "#000000", 0)])))
        elif look == "md":
            fill_bg(cc, W, H, MD_T, MD_B)
            cc.drawPaint(paint(shader=rad(W * 0.5, H * 1.05, M * 0.7, [(0, "#ff9a4a", 0.30), (0.5, "#7a2a5a", 0.12), (1, "#000000", 0)])))
            cc.drawPaint(paint(shader=rad(W * 0.85, H * 0.05, M * 0.5, [(0, VIO, 0.18), (1, "#000000", 0)])))
        else:
            fill_bg(cc, W, H, VY_T, VY_B)
            cc.drawPaint(paint(shader=rad(W * 0.8, H * 0.2, M * 0.7, [(0, "#2a4fa0", 0.25), (1, "#000000", 0)])))
            cc.drawPaint(paint(shader=rad(W * 0.1, H * 0.9, M * 0.5, [(0, "#3a1d6a", 0.22), (1, "#000000", 0)])))
        _BG[k] = surf.makeImageSnapshot()
    return _BG[k]

def bg_me(c, W, H, t, S, star_a=0.7, seed=61, look="me"):
    c.drawImage(bg_img(W, H, look), 0, 0)
    stars(c, W, H, t, star_a, seed=seed, drift=(-3, 0))

def run_panels(c, W, H, t, S, items, seed=61, look="me", zoom=None):
    """items: [(t_on, fn(c, ts)), ...] in time order. Each later panel covers the previous one."""
    bg_me(c, W, H, t, S, seed=seed, look=look)
    for i, (t0, fn) in enumerate(items):
        t1 = items[i + 1][0] if i + 1 < len(items) else None
        if t1 is not None and t >= t1 + 0.5: continue
        a = phase(t, t0 if i > 0 else None, t1)
        if a <= 0.003: continue
        with Layer(c, a) as on:
            if not on: continue
            if i > 0 and t < t0 + 0.55: bg_me(c, W, H, t, S, seed=seed, look=look)
            if S.P: c.clipRect(skia.Rect.MakeLTRB(0, 0.215 * H, W, 0.59 * H))
            with Stage(c, S) as ts:
                if zoom and S.P:
                    z, zx, zy = zoom; c.translate(zx, zy); c.scale(z, z); c.translate(-zx, -zy)
                fn(c, ts)
    kit.hook(c, W, H, t, S)

# ------------------------------------------------------------------ Sun with glare (the motif)
def glare_sun(c, x, y, r, t, a=1.0, flare_to=(960, 540), flare=1.0):
    if a <= 0 or r <= 0: return
    c.drawCircle(x, y, r * 7, paint(shader=rad(x, y, r * 7, [(0, GLARE, 0.55), (0.12, "#ffc070", 0.35), (0.4, "#ff6a2a", 0.10), (1, "#ff6a2a", 0)]), a=a))
    c.save(); c.translate(x, y); c.rotate(t * 3)
    for i in range(16):
        c.rotate(360 / 16)
        L = r * (1.9 + 0.35 * math.sin(t * 1.7 + i * 1.3)) * (1.25 if i % 2 else 1.0)
        c.drawPath(poly([(-r * 0.07, 0), (0, -L), (r * 0.07, 0)]), paint("#ffd7a0", 0.16 * a))
    c.restore()
    # anamorphic streak
    c.drawOval(skia.Rect.MakeLTRB(x - r * 9, y - r * 0.09, x + r * 9, y + r * 0.09), paint(shader=lin(x - r * 9, y, x + r * 9, y, [(0, "#ffb070", 0), (0.5, "#fff0d0", 0.55 * a), (1, "#ffb070", 0)])))
    c.drawCircle(x, y, r, paint(shader=rad(x - r * 0.2, y - r * 0.2, r * 1.3, [(0, "#ffffff", 1), (0.55, "#fff1c2", 1), (0.85, "#ffc46a", 1), (1, "#ff9a3a", 1)]), a=a))
    if flare > 0 and flare_to is not None:
        fx, fy = flare_to; dx, dy = fx - x, fy - y
        for k, (f, rr, colr, al) in enumerate([(0.45, 0.35, "#ffb35a", 0.16), (0.75, 0.18, "#ffe0a0", 0.25), (1.05, 0.6, "#ff9a5a", 0.08),
                                              (1.3, 0.12, "#ffe0a0", 0.3), (1.55, 0.9, "#ffc07a", 0.05)]):
            px, py = x + dx * f, y + dy * f
            hexa = [(px + math.cos(math.radians(30 + 60 * j)) * r * rr, py + math.sin(math.radians(30 + 60 * j)) * r * rr) for j in range(6)]
            pp = paint(colr, al * a * flare * 0.45); pp.setBlendMode(skia.BlendMode.kScreen); c.drawPath(poly(hexa), pp)
            pq = paint(colr, al * a * flare, stroke=max(1.5, r * 0.025)); pq.setBlendMode(skia.BlendMode.kScreen); c.drawPath(poly(hexa), pq)

# ------------------------------------------------------------------ Mercury
_MT = {}
def merc_img(R):
    R = max(4, int(R))
    if R not in _MT:
        if len(_MT) > 24: _MT.clear()
        n = 2 * R + 4; surf = skia.Surface(n, n); cc = surf.getCanvas(); cc.clear(skia.ColorTRANSPARENT)
        cx = cy = n / 2
        cc.save(); pth = skia.Path(); pth.addCircle(cx, cy, R); cc.clipPath(pth, doAntiAlias=True)
        cc.drawCircle(cx, cy, R, paint(shader=rad(cx, cy, R, [(0, "#a8998e", 1), (1, "#7a6c64", 1)])))
        rng = random.Random(16)
        for _ in range(9):  # dark low-reflectance terrain + lighter smooth plains
            ang = rng.random() * 6.28; d = rng.random() ** 0.7 * R * 0.8; rr = R * rng.uniform(0.15, 0.35)
            cc.drawCircle(cx + math.cos(ang) * d, cy + math.sin(ang) * d, rr, paint(rng.choice(["#5d5660", "#6a5f5c", "#b8a796"]), 0.45, blur=max(0.6, R * 0.06)))
        bx, by, br = cx + 0.32 * R, cy - 0.28 * R, 0.27 * R  # Caloris-like basin
        cc.drawCircle(bx, by, br, paint("#c4a98a", 0.55, blur=max(0.5, R * 0.02)))
        for k in (1.0, 1.18): cc.drawCircle(bx, by, br * k, paint("#5a4e48", 0.5, stroke=max(0.8, R * 0.012)))
        for _ in range(int(26 + R * 0.22)):
            ang = rng.random() * 6.28; d = rng.random() ** 0.55 * R * 0.97; cr = R * (0.012 + rng.random() ** 3 * 0.09)
            x, y = cx + math.cos(ang) * d, cy + math.sin(ang) * d
            cc.drawCircle(x + cr * 0.2, y + cr * 0.2, cr, paint("#3e3532", 0.55))
            cc.drawCircle(x - cr * 0.12, y - cr * 0.12, cr * 0.92, paint("#e9dccd", 0.35, stroke=max(0.6, cr * 0.22)))
        for (fx, fy) in ((-0.42, 0.38), (0.1, 0.55), (-0.2, -0.5)):  # bright rayed craters
            tx, ty = cx + fx * R, cy + fy * R
            for k in range(10):
                an = k / 10 * 6.28 + fx * 3
                cc.drawLine(tx, ty, tx + math.cos(an) * R * 0.3, ty + math.sin(an) * R * 0.3, paint("#f5ece2", 0.16, stroke=max(0.6, R * 0.01)))
            cc.drawCircle(tx, ty, R * 0.025, paint("#ffffff", 0.85))
        for k in range(4):  # lobate scarps: long wavy cliffs
            p = skia.Path(); x0 = cx + rng.uniform(-0.7, 0.4) * R; y0 = cy + rng.uniform(-0.6, 0.6) * R
            p.moveTo(x0, y0)
            for j in range(5): p.lineTo(x0 + (j + 1) * R * 0.09, y0 + math.sin(j * 1.7 + k) * R * 0.04 + (j + 1) * R * 0.03)
            cc.drawPath(p, paint("#3a312d", 0.5, stroke=max(0.6, R * 0.008)))
        cc.drawCircle(cx, cy, R, paint(shader=rad(cx, cy, R, [(0.6, "#000000", 0), (1, "#120a08", 0.45)])))
        cc.restore()
        _MT[R] = surf.makeImageSnapshot()
    return _MT[R]

def merc(c, x, y, R, sun_ang=200, night=0.93, a=1.0, glow=1.0):
    """Mercury disc. sun_ang: screen direction (degrees, 0 = right, 90 = down) from the planet toward the Sun."""
    if a <= 0 or R < 1: return
    if glow > 0: c.drawCircle(x, y, R * 1.25, paint(shader=rad(x, y, R * 1.25, [(0.78, SCORCH, 0.0), (0.82, SCORCH, 0.22 * glow), (1, SCORCH, 0)]), a=a))
    img = merc_img(R); pt = skia.Paint(); pt.setAlphaf(clamp(a))
    c.drawImageRect(img, skia.Rect.MakeXYWH(x - R - 2, y - R - 2, 2 * R + 4, 2 * R + 4), skia.SamplingOptions(skia.FilterMode.kLinear), pt)
    if night > 0:
        dx, dy = math.cos(math.radians(sun_ang)), math.sin(math.radians(sun_ang))
        c.save(); pth = skia.Path(); pth.addCircle(x, y, R); c.clipPath(pth, doAntiAlias=True)
        c.drawCircle(x, y, R + 1, paint(shader=lin(x + dx * R, y + dy * R, x - dx * R, y - dy * R,
                                                    [(0, "#ffb070", 0.10), (0.4, "#07040a", 0), (0.56, "#07040a", night * 0.92), (1, "#07040a", night)]), a=a))
        c.restore()
        arc = skia.Path(); arc.addArc(skia.Rect.MakeLTRB(x - R, y - R, x + R, y + R), sun_ang - 70, 140)
        c.drawPath(arc, paint("#ffd2a0", 0.55 * a, stroke=max(1.5, R * 0.018)))

# ------------------------------------------------------------------ BepiColombo stack, lander, astronaut
def bepi(c, x, y, s, ang=0.0, a=1.0, split=0.0, plume=0.0, t=0.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(ang)
    # solar wing (MPO's single long array)
    line(c, -0.6 * s, 0, -0.85 * s, 0, "#c9ccd6", s * 0.06, a)
    rrect(c, -3.0 * s, -0.3 * s, 2.15 * s, 0.6 * s, s * 0.04, "#1b2a5e", a)
    for k in range(1, 6): line(c, -3.0 * s + k * 0.36 * s, -0.3 * s, -3.0 * s + k * 0.36 * s, 0.3 * s, "#4a66b8", max(1, s * 0.02), a)
    line(c, -3.0 * s, 0, -0.85 * s, 0, "#4a66b8", max(1, s * 0.02), a)
    # MPO body
    rrect(c, -0.6 * s, -0.5 * s, 1.2 * s, 1.0 * s, s * 0.06, "#d6a23e", a)
    rect(c, -0.6 * s, -0.5 * s, 1.2 * s, 0.22 * s, "#eef0f4", a)
    for k in range(4): line(c, -0.5 * s + k * 0.33 * s, -0.2 * s, -0.42 * s + k * 0.33 * s, 0.45 * s, "#b98426", max(1, s * 0.015), a * 0.8)
    oval(c, 0.62 * s, 0.25 * s, 0.12 * s, 0.3 * s, "#eef0f4", a)  # dish
    # Mio (octagonal drum) + sunshield
    off = (0.95 + split * 2.4) * s
    if split < 0.2: c.drawPath(poly([(-0.55 * s, -0.5 * s), (0.55 * s, -0.5 * s), (0.4 * s, -0.68 * s), (-0.4 * s, -0.68 * s)]), paint("#e8e4d8", a * (1 - split * 5)))
    oy = -off
    c.drawPath(poly([(-0.5 * s, oy + 0.25 * s), (-0.35 * s, oy + 0.38 * s), (0.35 * s, oy + 0.38 * s), (0.5 * s, oy + 0.25 * s),
                     (0.5 * s, oy - 0.2 * s), (0.35 * s, oy - 0.33 * s), (-0.35 * s, oy - 0.33 * s), (-0.5 * s, oy - 0.2 * s)]), paint("#c9ccd6", a))
    rect(c, -0.5 * s, oy - 0.08 * s, 1.0 * s, 0.2 * s, "#2c4fa3", a)
    line(c, 0, oy - 0.33 * s, 0, oy - 0.75 * s, "#c9ccd6", max(1, s * 0.03), a)
    if plume > 0:
        fl = plume * s * (1.4 + 0.12 * math.sin(t * 40))
        c.drawPath(poly([(-0.18 * s, 0.5 * s), (0.18 * s, 0.5 * s), (0, 0.5 * s + fl)]), paint("#9fd8ff", 0.85 * a))
        c.drawPath(poly([(-0.08 * s, 0.5 * s), (0.08 * s, 0.5 * s), (0, 0.5 * s + fl * 0.6)]), paint("#ffffff", a))
    c.restore()

def lander(c, x, y, s, a=1.0, plume=0.0, t=0.0):
    if a <= 0: return
    for sg in (-1, 1):
        line(c, x + sg * 0.35 * s, y - 0.55 * s, x + sg * 0.75 * s, y, "#c9ccd6", s * 0.06, a)
        oval(c, x + sg * 0.75 * s, y, 0.12 * s, 0.04 * s, "#c9ccd6", a)
    if plume > 0:
        fl = plume * s * (0.9 + 0.1 * math.sin(t * 40))
        c.drawPath(poly([(x - 0.15 * s, y - 0.4 * s), (x + 0.15 * s, y - 0.4 * s), (x, y - 0.4 * s + fl)]), paint("#ffe2b0", 0.9 * a))
    c.drawPath(poly([(x - 0.5 * s, y - 0.45 * s), (x + 0.5 * s, y - 0.45 * s), (x + 0.4 * s, y - 1.1 * s), (x - 0.4 * s, y - 1.1 * s)]), paint("#d6a23e", a))
    rrect(c, x - 0.3 * s, y - 1.45 * s, 0.6 * s, 0.38 * s, 0.1 * s, "#eef0f4", a)
    circle(c, x + 0.1 * s, y - 1.27 * s, 0.09 * s, "#3a4a7a", a)

def astro(c, x, y, h, a=1.0, walk=0.0, t=0.0, hop=0.0, face=1):
    """suited explorer standing on (x, y); generic, not a real person."""
    if a <= 0: return
    y -= hop
    sw = math.sin(t * 7) * walk
    for k, s_ in enumerate((-1, 1)):
        lx = x + s_ * h * 0.07
        line(c, lx, y - h * 0.42, lx + sw * s_ * h * 0.12, y - h * 0.04, "#e9edf3", h * 0.11, a)
        oval(c, lx + sw * s_ * h * 0.12 + face * h * 0.03, y - h * 0.02, h * 0.08, h * 0.035, "#9aa3b5", a)
    rrect(c, x - face * h * 0.24, y - h * 0.82, h * 0.16, h * 0.34, h * 0.04, "#c3cad6", a)  # backpack
    rrect(c, x - h * 0.15, y - h * 0.82, h * 0.3, h * 0.44, h * 0.1, "#f2f4f8", a)
    line(c, x + face * h * 0.1, y - h * 0.72, x + face * h * 0.22, y - h * 0.5 - sw * h * 0.05, "#e9edf3", h * 0.09, a)
    circle(c, x, y - h * 0.92, h * 0.13, "#f2f4f8", a)
    oval(c, x + face * h * 0.04, y - h * 0.92, h * 0.085, h * 0.075, "#ffb347", a)
    oval(c, x + face * h * 0.06, y - h * 0.95, h * 0.03, h * 0.02, "#fff4d8", a * 0.9)
    rect(c, x - h * 0.06, y - h * 0.7, h * 0.12, h * 0.06, COPPER, a)

def boulder(c, x, y, s, a=1.0, lit=1.0):
    pts = [(x - s, y), (x - s * 0.85, y - s * 0.5), (x - s * 0.3, y - s * 0.85), (x + s * 0.35, y - s * 0.8), (x + s * 0.9, y - s * 0.35), (x + s, y)]
    c.drawPath(poly(pts), paint("#5d524d", a))
    c.drawPath(poly([(x - s * 0.3, y - s * 0.85), (x + s * 0.35, y - s * 0.8), (x + s * 0.9, y - s * 0.35), (x + s * 0.2, y - s * 0.3)]), paint(mix("#5d524d", "#e7a878", 0.5 * lit), a))

# ------------------------------------------------------------------ Mercury ground (cached) + sky
_GR = {}
def ground_img(hy, seed=3):
    k = (hy, seed)
    if k not in _GR:
        if len(_GR) > 8: _GR.clear()
        surf = skia.Surface(VW, VH); cc = surf.getCanvas(); cc.clear(skia.ColorTRANSPARENT)
        rng = random.Random(seed)
        pts = [(0, hy)]
        for i in range(41):
            pts.append((VW * i / 40, hy - 25 - 22 * math.sin(i * 0.7 + seed) - 14 * math.sin(i * 1.9) - rng.uniform(0, 10)))
        pts += [(VW, VH), (0, VH)]
        cc.drawPath(poly(pts), paint("#3c3431"))
        cc.drawRect(skia.Rect.MakeLTRB(0, hy, VW, VH), paint(shader=lin(0, hy, 0, VH, [(0, "#5b504a", 1), (1, "#2a2320", 1)])))
        for _ in range(26):
            yy = hy + 20 + rng.random() ** 1.3 * (VH - hy - 30); sc = 0.3 + (yy - hy) / (VH - hy)
            xx = rng.uniform(-40, VW + 40); rx = rng.uniform(40, 130) * sc; ry = rx * 0.22
            cc.drawOval(skia.Rect.MakeLTRB(xx - rx, yy - ry, xx + rx, yy + ry), paint("#2c2421", 0.8))
            cc.drawArc(skia.Rect.MakeLTRB(xx - rx, yy - ry, xx + rx, yy + ry), 10, 160, False, paint("#8a7c72", 0.7, stroke=max(1.5, ry * 0.25)))
        for _ in range(140):
            yy = hy + rng.random() * (VH - hy); xx = rng.uniform(0, VW)
            cc.drawCircle(xx, yy, rng.uniform(1, 3.5) * (0.4 + (yy - hy) / (VH - hy)), paint("#6e625b", 0.7))
        _GR[k] = surf.makeImageSnapshot()
    return _GR[k]

def mscape(c, t, hy=720, sun=None, heat=0.0, cold=0.0, seed=3, star_a=0.9, glare_to=(960, 700)):
    """black sky + stars + optional glare sun (x, y, r) + Mercury ground. heat/cold tint the ground."""
    stage_bg(c, "#020103", "#0b0608")
    stars(c, VW, VH, t, star_a, seed=71, drift=(-1.5, 0))
    if sun: glare_sun(c, sun[0], sun[1], sun[2], t, flare_to=glare_to)
    c.drawImage(ground_img(hy, seed), 0, 0)
    if heat > 0:
        c.drawRect(skia.Rect.MakeLTRB(0, hy - 60, VW, VH), paint(shader=lin(0, hy - 60, 0, VH, [(0, EMBER, 0.0), (0.3, EMBER, 0.28 * heat), (1, "#ffb060", 0.42 * heat)])))
    if cold > 0:
        c.drawRect(skia.Rect.MakeLTRB(0, hy - 60, VW, VH), paint(shader=lin(0, hy - 60, 0, VH, [(0, "#0a1440", 0.5 * cold), (1, "#1a2f80", 0.55 * cold)])))

# ------------------------------------------------------------------ orbit physics (for the day/year diagrams)
P_ORB, P_SPIN, ECC = 87.969, 58.646, 0.2056
def kepler(days):
    M = 2 * math.pi * days / P_ORB; E = M
    for _ in range(8): E -= (E - ECC * math.sin(E) - M) / (1 - ECC * math.cos(E))
    nu = 2 * math.atan2(math.sqrt(1 + ECC) * math.sin(E / 2), math.sqrt(1 - ECC) * math.cos(E / 2))
    return nu, 1 - ECC * math.cos(E)

def orbit_view(c, t, days, sx, sy, a_px, ts, pr=46, sun_r=60, show_marker=True, trail=True, colr=SCORCH, look="me", sun_draw=True):
    """Sun at the focus, Mercury on its real eccentric orbit; a surface marker spins 3x per 2 orbits."""
    b_px = a_px * math.sqrt(1 - ECC ** 2); cx = sx - a_px * ECC
    c.drawOval(skia.Rect.MakeLTRB(cx - a_px, sy - b_px, cx + a_px, sy + b_px), paint(colr, 0.35, stroke=3, dash=([14, 12], -t * 10)))
    if sun_draw:
        if look == "me": glare_sun(c, sx, sy, sun_r, t, flare=0)
        else: sun(c, sx, sy, sun_r, t)
    nu, r = kepler(days)
    px, py = sx + math.cos(nu) * r * a_px, sy - math.sin(nu) * r * a_px
    if trail:
        for k in range(1, 14):
            n2, r2 = kepler(days - k * 1.2)
            circle(c, sx + math.cos(n2) * r2 * a_px, sy - math.sin(n2) * r2 * a_px, pr * 0.16 * (1 - k / 14), colr, 0.5 * (1 - k / 14))
    sun_ang = math.degrees(math.atan2(sy - py, sx - px))
    merc(c, px, py, pr, sun_ang=sun_ang, glow=0.6)
    th = math.pi / 2 + 2 * math.pi * days / P_SPIN  # sunrise at t=0 (perihelion)
    mx, my = px + math.cos(th) * pr, py - math.sin(th) * pr
    phi = math.atan2(-(sy - py), sx - px)  # math-angle toward Sun
    lit = math.cos(th - phi) > 0
    if show_marker:
        line(c, px + math.cos(th) * pr * 0.6, py - math.sin(th) * pr * 0.6, px + math.cos(th) * pr * 1.45, py - math.sin(th) * pr * 1.45, YEL if lit else NIGHT, 7)
        circle(c, px + math.cos(th) * pr * 1.5, py - math.sin(th) * pr * 1.5, 13, YEL if lit else NIGHT)
    return px, py, lit

def days_map(t, segs):
    """segs: [(t0, d0), (t1, d1), ...] piecewise-linear scene time -> days."""
    if t <= segs[0][0]: return segs[0][1]
    for (a0, d0), (a1, d1) in zip(segs, segs[1:]):
        if t <= a1: return lerp(d0, d1, (t - a0) / max(1e-6, a1 - a0))
    return segs[-1][1]

# ------------------------------------------------------------------ title / cards / end
def motif_me(c, W, H, t, S, cx, cy, s):
    u = S.u * s * (1.1 if S.P else 1.0)
    R = int(200 * u)
    glare_sun(c, cx - 560 * u, cy - 260 * u, 70 * u, t, flare_to=(cx + 300 * u, cy + 200 * u))
    th = t * 0.45
    ox, oy = math.cos(th) * 330 * u, math.sin(th) * 95 * u
    front = math.sin(th) > 0
    if not front: bepi(c, cx + ox, cy + oy, 16 * u, ang=-15, a=0.9)
    c.drawOval(skia.Rect.MakeLTRB(cx - 330 * u, cy - 95 * u, cx + 330 * u, cy + 95 * u), paint(SCORCH, 0.35, stroke=2.5, dash=([12, 10], -t * 10)))
    merc(c, cx, cy, R, sun_ang=210)
    if front: bepi(c, cx + ox, cy + oy, 16 * u, ang=-15)

def bg_title(c, W, H, t, S): bg_me(c, W, H, t, S)
def me6_title(c, W, H, t, S): kit.title(c, W, H, t, S, bg_title, motif_me, PAL)
def me6_card(c, W, H, t, S):
    def cbg(c, W, H, t, S):
        bg_me(c, W, H, t, S)
        with Layer(c, 0.4):
            motif_me(c, W, H, t, S, W / 2, H / 2, 1.2 if not S.P else 0.9)
    kit.card(c, W, H, t, S, cbg, PAL)
def me6_end(c, W, H, t, S): kit.end(c, W, H, t, S, bg_title, motif_me, PAL)

def motif_md(c, W, H, t, S, cx, cy, s):
    u = S.u * s * (1.1 if S.P else 1.0)
    clock_dial(c, cx - 190 * u, cy, 150 * u, t * 0.5, "DAY", GOLD, u)
    clock_dial(c, cx + 190 * u, cy, 150 * u, t * 1.0, "YEAR", VIO, u)

def motif_vy(c, W, H, t, S, cx, cy, s):
    u = S.u * s * (1.1 if S.P else 1.0)
    voyager(c, cx + 120 * u, cy, 170 * u, t, ang=-12)
    circle(c, cx - 330 * u, cy + 60 * u, 7 * u, "#9fd0ff"); circle(c, cx - 330 * u, cy + 60 * u, 20 * u, "#9fd0ff", 0.25)
    q = (t * 0.5) % 1
    line(c, cx - 310 * u, cy + 55 * u, lerp(cx - 310 * u, cx - 10 * u, q), lerp(cy + 55 * u, cy + 10 * u, q), SIG, 4 * u, 0.8 * math.sin(q * math.pi))

def me6_endshort(c, W, H, t, S):
    look = S.opts.get("look")
    if look == "mday": kit.end_short(c, W, H, t, S, lambda c, W, H, t, S: bg_me(c, W, H, t, S, look="md"), motif_md, PAL_MD)
    elif look == "voy": kit.end_short(c, W, H, t, S, lambda c, W, H, t, S: bg_me(c, W, H, t, S, look="vy", star_a=1.0), motif_vy, PAL_VY)
    else: kit.end_short(c, W, H, t, S, bg_title, motif_me, PAL)

# ------------------------------------------------------------------ me6_hook
def me6_hook(c, W, H, t, S):
    nb = 3 if S.n() >= 3 else 1; B = beats(S, nb)
    tcap = B(0, 0.7) if nb == 3 else S.lt(0, 0.45)
    def pA(c, ts):
        mx, my, R = (1180, 560, 300) if not S.P else (960, 600, 400)
        glare_sun(c, 230, 160, 95, t, flare_to=(mx, my))
        q = prog(t, 0.0, max(0.5, tcap - 0.0))
        # approach along a curve, then circle on the capture orbit
        orx, ory = R * 1.55, R * 0.48
        if t < tcap:
            f = ease(q)
            bx = lerp(VW + 200, mx + orx * math.cos(-0.25), f); by = lerp(120, my + ory * math.sin(-0.25), f) + math.sin(f * math.pi) * 60
            th = None
        else:
            th = -0.25 + (t - tcap) * 0.5
            bx, by = mx + orx * math.cos(th), my + ory * math.sin(th)
        ring = prog(t, tcap - 0.2, 1.0)
        if ring > 0:
            p = skia.Path(); p.addArc(skia.Rect.MakeLTRB(mx - orx, my - ory, mx + orx, my + ory), -14, 360 * ease(ring))
            c.drawPath(p, paint(SCORCH, 0.7, stroke=4, dash=([16, 10], -t * 14)))
        behind = th is not None and math.sin(th) < 0
        bs = 40 if S.P else 26
        if behind: bepi(c, bx, by, bs, ang=-10, plume=0)
        merc(c, mx, my, R, sun_ang=205)
        if not behind: bepi(c, bx, by, bs, ang=-10, plume=0.7 * vis(t, tcap - 1.6, tcap + 0.4), t=t)
        if nb == 3 and not S.P:
            C(c, "21 NOV 2026", 330, 520, vis(t, B(0, 0.05)), ts, size=40, bg=YEL, fg="#0b1030", a=1)
            C(c, "ORBIT CAPTURE", 330, 640, vis(t, tcap), ts, size=36, dot=GREEN)
            C(c, "BEPICOLOMBO · ESA + JAXA", 1180, 950, vis(t, B(1, 0.05)), ts, size=36, dot=SCORCH)
            C(c, "ONLY THE 2ND MISSION TO ORBIT MERCURY", 1180, 1030, vis(t, B(1, 0.4)), ts, size=32)
            T(c, "LIVE THERE?", 330, 850, 96, ts, SCORCH, prog(t, B(2, 0.45), 0.4), shadow=16)
        elif S.P:
            C(c, "21 NOV 2026: IN ORBIT", 960, 120, vis(t, tcap), ts, size=36, bg=YEL, fg="#0b1030", a=1)
    run_panels(c, W, H, t, S, [(0, pA)])

# ------------------------------------------------------------------ me6_news
def timeline_bar(c, t, ts, items, y, x0=200, x1=1720, here=None, a=1.0):
    line(c, x0, y, x1, y, "#ffffff", 5, 0.35 * a)
    for (f, top, bot, t_on, colr) in items:
        x = lerp(x0, x1, f); p = vis(t, t_on)
        circle(c, x, y, 16 * eback(p), colr, a * p)
        T(c, top, x, y - 70, 40, ts, colr, a * p, maxw=420)
        T(c, bot, x, y + 70, 30, ts, "#e8dcd0", a * p, w=700, fam="Inter", maxw=420)
    if here is not None:
        hx = lerp(x0, x1, here[0]); p = vis(t, here[1])
        c.drawPath(poly([(hx, y - 34), (hx - 16, y - 60), (hx + 16, y - 60)]), paint(YEL, p))

def me6_news(c, W, H, t, S):
    B = beats(S, 4)
    def pA(c, ts):
        mx, my, R = 760, 600, 260
        glare_sun(c, 150, 130, 60, t, flare_to=(mx, my))
        th0 = B(0, 0.1); tb = B(0, 0.55)
        q = prog(t, th0, tb - th0)
        orx, ory = 520, 170
        if t < tb:
            f = ease(q); ang = lerp(-1.4, -0.3, f)
            bx, by = mx + lerp(900, orx, f) * math.cos(ang), my + lerp(400, ory, f) * math.sin(ang)
        else:
            ang = -0.3 + (t - tb) * 0.35; bx, by = mx + orx * math.cos(ang), my + ory * math.sin(ang)
        c.drawOval(skia.Rect.MakeLTRB(mx - orx, my - ory, mx + orx, my + ory), paint(SCORCH, 0.6 * vis(t, tb), stroke=3, dash=([14, 10], -t * 10)))
        behind = t >= tb and math.sin(ang) < 0
        if behind: bepi(c, bx, by, 20)
        merc(c, mx, my, R, sun_ang=215)
        if not behind: bepi(c, bx, by, 20, plume=vis(t, th0, tb), t=t)
        C(c, "21 NOV, EVENING: ENGINE BURN", 1450, 330, vis(t, B(0, 0.12)), ts, size=34, dot=SCORCH)
        C(c, "JUST AFTER MIDNIGHT: CONFIRMED", 1450, 450, vis(t, B(0, 0.5)), ts, size=34, dot=GREEN)
        C(c, "CAPTURED INTO ORBIT", 1450, 570, vis(t, B(0, 0.8)), ts, size=40, bg=YEL, fg="#0b1030", a=1)
        check(c, 1450, 700, 40, vis(t, B(0, 0.85)))
    def pB(c, ts):
        sp = ease(prog(t, B(1, 0.72), 1.6))
        cx, cy = 960, 560
        bepi(c, cx, cy + 80, 95, split=sp * 0.55)
        C(c, "MPO · ESA", cx - 420, cy + 120, vis(t, B(1, 0.12)), ts, size=36, dot="#d6a23e")
        C(c, "MIO · JAXA", cx + 380, cy - 120 - sp * 120, vis(t, B(1, 0.3)), ts, size=36, dot="#2c4fa3")
        C(c, "STUDIES THE MAGNETIC FIELD", cx + 380, cy - 20 - sp * 120, vis(t, B(1, 0.4)), ts, size=28)
        C(c, "SPLIT: 9–10 DEC 2026", 960, 150, vis(t, B(1, 0.7)), ts, size=40, bg=YEL, fg="#0b1030", a=1)
    def pC(c, ts):
        items = [(0.0, "20 OCT 2018", "LAUNCH", B(2, 0.0), "#e8dcd0"), (0.45, "21 NOV 2026", "IN ORBIT", B(2, 0.05), SCORCH),
                 (0.7, "9–10 DEC", "ORBITERS SPLIT", B(2, 0.15), "#9fb8ff"), (1.0, "APR 2027", "SCIENCE BEGINS", B(2, 0.25), GREEN)]
        timeline_bar(c, t, ts, items, 520, here=(0.47, B(2, 0.1)))
        C(c, "WE ARE HERE", lerp(200, 1720, 0.47), 300, vis(t, B(2, 0.1)), ts, size=30, bg=YEL, fg="#0b1030", a=1)
        C(c, "STILL UNKNOWN: WHAT THEY'LL FIND", 960, 860, vis(t, B(2, 0.6)), ts, size=36, dot=RED)
    def pD(c, ts):
        mx, my, R = 700, 560, 280
        glare_sun(c, 120, 150, 55, t, flare_to=(mx, my))
        orx, ory = 420, 330
        tc = B(3, 0.7)
        c.drawOval(skia.Rect.MakeLTRB(mx - orx, my - ory, mx + orx, my + ory), paint("#9fb8ff", 0.45 * (1 - vis(t, tc)), stroke=3, dash=([12, 10], -t * 10)))
        merc(c, mx, my, R, sun_ang=220)
        if t < tc:
            th = (t - B(3, 0)) * 1.3; px, py = mx + orx * math.cos(th), my + ory * math.sin(th)
            if t > tc - 0.8:
                f = ease((t - (tc - 0.8)) / 0.8); px, py = lerp(px, mx + R * 0.5, f), lerp(py, my - R * 0.6, f)
            circle(c, px, py, 12, "#e8eef8"); line(c, px - 22, py, px + 22, py, "#9fb8ff", 5)
        else:
            q = t - tc; fx, fy = mx + R * 0.5, my - R * 0.6
            circle(c, fx, fy, 10 + q * 60, "#ffe0a0", clamp(1 - q / 0.9) * 0.9, stroke=6)
            circle(c, fx, fy, 14, "#ffffff", clamp(1 - q / 0.5))
        C(c, "NASA MESSENGER", 1450, 300, vis(t, B(3, 0.05)), ts, size=38, dot="#9fb8ff")
        C(c, "ORBITED 2011–2015", 1450, 420, vis(t, B(3, 0.3)), ts, size=36)
        C(c, "ENDED: CRASHED INTO THE SURFACE", 1450, 540, vis(t, tc), ts, size=32, bg="#3a1010", dot=RED)
    run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB), (B(2, 0), pC), (B(3, 0), pD)])

# ------------------------------------------------------------------ me6_trip
def well_y(x, cx=960, top=260, depth=640, w=260):
    d = abs(x - cx)
    return top + depth * (w / (d + w)) ** 1.6

def me6_trip(c, W, H, t, S):
    B = beats(S, 5)
    def pA(c, ts):
        pts = [(x, well_y(x)) for x in range(0, VW + 1, 16)]
        p = skia.Path(); p.moveTo(*pts[0])
        for q in pts[1:]: p.lineTo(*q)
        c.drawPath(p, paint(SCORCH, 0.8, stroke=5))
        for k in range(1, 7):
            y0 = 300 + k * 90
            line(c, 0, y0, VW, y0, SCORCH, 1.5, 0.08)
        glare_sun(c, 960, well_y(960) + 40, 48, t, flare=0)
        for (x, lab, colr) in ((140, "PLUTO", "#cfd8ff"), (560, "EARTH", "#6fb6ff"), (790, "MERCURY", SCORCH)):
            yy = well_y(x)
            circle(c, x, yy - 22, 20 if lab != "PLUTO" else 12, colr)
            T(c, lab, x, yy - 85, 34, ts, colr, vis(t, B(0, 0.2)), maxw=300)
        # spacecraft rolls downhill from Earth toward Mercury, speeding up
        t0 = B(1, 0.0); q = ((t - t0) % 3.2) / 3.2 if t > t0 else 0
        if t > t0:
            f = q ** 2; x = lerp(580, 800, f); yy = well_y(x) - 26
            for k in range(1, 8):
                f2 = max(0, (q - k * 0.03)) ** 2; x2 = lerp(580, 800, f2)
                circle(c, x2, well_y(x2) - 26, 9 * (1 - k / 8), YEL, 0.5 * (1 - k / 8))
            circle(c, x, yy, 12, YEL)
        C(c, "THE SUN'S GRAVITY WELL", 960, 120, vis(t, B(0, 0.1)), ts, size=38, dot=SCORCH)
        C(c, "FALL IN → SPEED UP", 1460, 300, vis(t, B(1, 0.1)), ts, size=36, dot=YEL)
        C(c, "TO BE CAPTURED: SHED SPEED", 1460, 410, vis(t, B(1, 0.55)), ts, size=34, dot=RED)
    def pB(c, ts):
        C(c, "ENERGY NEEDED (SOME ESTIMATES)", 960, 170, vis(t, B(2, 0.0)), ts, size=36)
        bar(c, 420, 420, 1000, 60, 0.55 * ease(prog(t, B(2, 0.15), 0.8)), "#cfd8ff", 1.0, label=None)
        bar(c, 420, 640, 1000, 60, 0.85 * ease(prog(t, B(2, 0.35), 0.8)), SCORCH, 1.0, label=None)
        T(c, "TO PLUTO", 390, 450, 44, ts, "#cfd8ff", vis(t, B(2, 0.15)), align="r", maxw=360)
        T(c, "TO MERCURY", 390, 670, 44, ts, SCORCH, vis(t, B(2, 0.35)), align="r", maxw=360)
        T(c, "LESS", 420 + 550 + 40, 450, 40, ts, "#cfd8ff", vis(t, B(2, 0.5)), align="l", maxw=300)
        T(c, "MORE", 420 + 850 + 40, 670, 40, ts, SCORCH, vis(t, B(2, 0.6)), align="l", maxw=300)
    def pC(c, ts):
        sx, sy = 960, 560
        glare_sun(c, sx, sy, 40, t, flare=0)
        orbs = [(130, SCORCH, "MERCURY"), (250, "#f0d08a", "VENUS"), (345, "#6fb6ff", "EARTH")]
        for r, colr, lab in orbs: c.drawCircle(sx, sy, r, paint(colr, 0.35, stroke=2.5, dash=([10, 10], 0)))
        fb = [(345, 200), (250, 120), (250, 300), (130, 20), (130, 80), (130, 140), (130, 200), (130, 260), (130, 320)]
        q = ease(prog(t, B(3, 0.05), (B(3, 0.9) - B(3, 0.05))))
        n = int(q * 9 + 1e-6)
        # spiral path (stylised) from Earth inward
        p = skia.Path(); steps = 120
        for i in range(steps + 1):
            f = i / steps * q
            r = lerp(345, 130, min(1, f * 1.6)) ; ang = math.radians(200 + f * 1080)
            x, y = sx + math.cos(ang) * r, sy + math.sin(ang) * r * 0.98
            p.moveTo(x, y) if i == 0 else p.lineTo(x, y)
        c.drawPath(p, paint(YEL, 0.8, stroke=4))
        for i, (r, ang) in enumerate(fb[:n]):
            x, y = sx + math.cos(math.radians(ang)) * r, sy + math.sin(math.radians(ang)) * r
            circle(c, x, y, 16, ["#6fb6ff", "#f0d08a", "#f0d08a"][i] if i < 3 else SCORCH); circle(c, x, y, 26, "#ffffff", 0.7, stroke=3)
        T(c, f"FLYBYS: {n}/9", 1550, 300, 70, ts, YEL, vis(t, B(3, 0.05)), maxw=520)
        C(c, "1 EARTH · 2 VENUS · 6 MERCURY", 1550, 430, vis(t, B(3, 0.35)), ts, size=30)
        C(c, "EACH ONE STEALS SPEED", 380, 900, vis(t, B(3, 0.7)), ts, size=34, dot=RED)
    def pD(c, ts):
        sx, sy = 560, 560
        glare_sun(c, sx, sy, 40, t, flare=0)
        c.drawCircle(sx, sy, 170, paint(SCORCH, 0.5, stroke=3, dash=([10, 10], 0)))
        cx = sx + 130; a_, b_ = 300, 250
        c.drawOval(skia.Rect.MakeLTRB(cx - a_, sy - b_, cx + a_, sy + b_), paint("#9fb8ff", 0.6, stroke=3, dash=([14, 10], -t * 10)))
        th = (t - B(4, 0)) * 0.9
        circle(c, sx + 170 * math.cos(-th * 2), sy + 170 * math.sin(-th * 2), 16, SCORCH)
        circle(c, cx + a_ * math.cos(-th + 3.14), sy + b_ * math.sin(-th + 3.14), 10, "#e8eef8")
        circle(c, sx - 170, sy, 40, YEL, 0.25 + 0.25 * math.sin(t * 4), stroke=4)
        T(c, "GIUSEPPE “BEPI” COLOMBO", 1380, 330, 60, ts, "#ffffff", vis(t, B(4, 0.0)), maxw=900)
        T(c, "ITALIAN SCIENTIST · 1920–1984", 1380, 410, 34, ts, "#e8dcd0", vis(t, B(4, 0.1)), w=700, fam="Inter", maxw=900)
        C(c, "1970: A SECOND PASS FOR MARINER 10", 1380, 560, vis(t, B(4, 0.45)), ts, size=32, dot="#9fb8ff")
    run_panels(c, W, H, t, S, [(0, pA), (B(2, 0), pB), (B(3, 0), pC), (B(4, 0), pD)])

# ------------------------------------------------------------------ me6_land
def me6_land(c, W, H, t, S):
    mode = S.opts.get("mode")
    B = beats(S, 4)
    def pLand(c, ts):
        mscape(c, t, hy=760, sun=(-40, 700, 120), glare_to=(1300, 300))
        q = ease(prog(t, 0.2, B(0, 0.6) - 0.2))
        ly = lerp(250, 800, q)
        lander(c, 1100, ly, 110, plume=1 - prog(t, B(0, 0.6) - 0.2, 0.3), t=t)
        if q > 0.95:
            for k in range(14):
                d = (t - B(0, 0.6)) * 200
                circle(c, 1100 + (k - 7) * 30 + math.copysign(d, k - 7) * 0.4, 790 - abs(math.sin(k)) * 30, 14, "#8a7c72", 0.5 * clamp(1 - (t - B(0, 0.6)) / 1.5))
        C(c, "THE RULES", 420, 200, vis(t, B(0, 0.0)), ts, size=40, bg=YEL, fg="#0b1030", a=1)
        C(c, "HEAT-PROOF SUIT", 420, 310, vis(t, B(0, 0.2)), ts, size=34, dot=SCORCH)
        C(c, "A SMALL BASE", 420, 410, vis(t, B(0, 0.35)), ts, size=34, dot=SCORCH)
        C(c, "GOAL: STAY ALIVE", 420, 510, vis(t, B(0, 0.6)), ts, size=36, dot=GREEN)
    def pGrav(c, ts, t0, t1):
        mscape(c, t, hy=760, sun=(-40, 720, 120), glare_to=(1300, 300))
        hop = abs(math.sin((t - t0) * 2.2)) * 120 * ease(prog(t, t0 + 0.4, 0.5))
        astro(c, 480 if S.P else 560, 900 if S.P else 860, 380 if S.P else 230, hop=hop, t=t)
        sx = 1300 if S.P else 1350
        C(c, "GRAVITY", sx, 190, vis(t, t0), ts, size=38, dot=SCORCH)
        bar(c, sx - 330, 330, 660, 52, 1.0 * ease(prog(t, t0 + 0.2, 0.6)), "#6fb6ff", 1.0)
        bar(c, sx - 330, 470, 660, 52, 0.38 * ease(prog(t, t0 + 0.5, 0.6)), SCORCH, 1.0)
        T(c, "EARTH 100%", sx - 330, 300, 34, ts, "#6fb6ff", vis(t, t0 + 0.2), align="l", maxw=600, w=800)
        T(c, "MERCURY 38%", sx - 330, 440, 34, ts, SCORCH, vis(t, t0 + 0.5), align="l", maxw=600, w=800)
        if t1 is not None:
            C(c, "10 KG BACKPACK → FEELS LIKE ~3.8 KG", sx, 610, vis(t, t1), ts, size=30, bg=YEL, fg="#0b1030", a=1)
    def pSky(c, ts, t0):
        mscape(c, t, hy=760, sun=(1650, 420, 120), glare_to=(400, 900), star_a=1.0)
        rng = random.Random(5)
        for k in range(70):  # exosphere atoms kicked up from the ground
            ph = rng.random(); q = (ph + (t - t0) * 0.12) % 1
            x = rng.uniform(0, VW) - q * 160; y = 760 - q * rng.uniform(300, 640)
            colr = rng.choice([YEL, YEL, "#ff8f6a", "#9fd0ff", "#ffffff"])
            circle(c, x, y, rng.uniform(4, 7), colr, 0.85 * math.sin(q * math.pi) * vis(t, t0 + 0.6))
        for k in range(6):  # solar wind
            q = ((t - t0) * 0.6 + k / 6) % 1
            y = 300 + k * 70
            arrow(c, lerp(1500, 700, q), y, lerp(1440, 640, q), y + 10, "#ffd2a0", 5, 0.6 * math.sin(q * math.pi) * vis(t, t0 + 1.0))
        astro(c, 520, 900 if S.P else 860, 340 if S.P else 200, t=t)
        C(c, "BLACK SKY, EVEN AT NOON", 600, 170, vis(t, t0 + 0.05), ts, size=36, dot="#ffffff")
        C(c, "EXOSPHERE: A THIN HAZE OF ATOMS", 600, 280, vis(t, t0 + 0.6), ts, size=32, dot=YEL)
        if not S.P: C(c, "KNOCKED LOOSE BY SOLAR WIND + TINY METEORITES", 1150, 990, vis(t, t0 + 1.2), ts, size=28)
    def pSun(c, ts, t0):
        rrect(c, 100, 150, 820, 760, 30, "#3d7fd0", 1); rrect(c, 1000, 150, 820, 760, 30, "#020103", 1)
        c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(100, 150, 820, 760), 30, 30), doAntiAlias=True)
        c.drawRect(skia.Rect.MakeXYWH(100, 150, 820, 760), paint(shader=lin(0, 150, 0, 910, [(0, "#2f6fc4", 1), (1, "#a9d4ff", 1)])))
        sun(c, 510, 440, 40, t)
        hills(c, 920, 760, 30, "#4f8f4a", 21, H=910); c.restore()
        c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(1000, 150, 820, 760), 30, 30), doAntiAlias=True)
        stars(c, VW, VH, t, 0.9, seed=73)
        g = ease(prog(t, t0 + 0.2, 0.9))
        glare_sun(c, 1410, 440, lerp(40, 125, g), t, flare_to=(1410, 900), flare=0.5)
        c.drawImageRect(ground_img(760, 4), skia.Rect.MakeXYWH(0, 0, VW, VH), skia.Rect.MakeXYWH(1000, 0, VW, VH), skia.SamplingOptions(), skia.Paint())
        c.restore()
        T(c, "FROM EARTH", 510, 960, 42, ts, "#ffffff", vis(t, t0), maxw=780)
        T(c, "FROM MERCURY", 1410, 960, 42, ts, SCORCH, vis(t, t0 + 0.2), maxw=780)
        C(c, "3× WIDER", 1410, 230, vis(t, t0 + 0.9), ts, size=40, bg=YEL, fg="#0b1030", a=1)
        if not S.P or mode != "sun": C(c, "UP TO 7× BRIGHTER", 1410, 650, vis(t, t0 + 1.6), ts, size=34, dot=YEL)
    if mode == "sky":
        tb = S.lt(0, 0.55)
        run_panels(c, W, H, t, S, [(0, lambda c, ts: pGrav(c, ts, 0.0, None)), (tb, lambda c, ts: pSky(c, ts, tb))]); return
    if mode == "sun":
        run_panels(c, W, H, t, S, [(0, lambda c, ts: pSun(c, ts, 0.0))]); return
    run_panels(c, W, H, t, S, [(0, pLand), (B(1, 0), lambda c, ts: pGrav(c, ts, B(1, 0), B(1, 0.72))),
                               (B(2, 0), lambda c, ts: pSky(c, ts, B(2, 0))), (B(3, 0), lambda c, ts: pSun(c, ts, B(3, 0)))])

# ------------------------------------------------------------------ me6_heat
def lead_bar(c, x, y, s, melt, t):
    if melt < 1:
        h = s * 0.45 * (1 - melt)
        c.drawPath(poly([(x - s * 0.6, y), (x + s * 0.6, y), (x + s * 0.5, y - h), (x - s * 0.5, y - h)]), paint("#9aa3ad"))
        c.drawPath(poly([(x - s * 0.5, y - h), (x + s * 0.5, y - h), (x + s * 0.42, y - h - s * 0.06), (x - s * 0.42, y - h - s * 0.06)]), paint("#c9d0d8"))
        if h > s * 0.1: T(c, "Pb", x, y - h / 2, s * 0.22, 1.0, "#5a626c", 1.0, maxw=s)
    pw = s * (0.6 + 0.9 * melt)
    if melt > 0:
        oval(c, x, y, pw, s * 0.08 + s * 0.06 * melt, "#b8c2cc", 0.95)
        oval(c, x - pw * 0.3, y - s * 0.02, pw * 0.3, s * 0.03, "#ffffff", 0.6 + 0.2 * math.sin(t * 5))

def me6_heat(c, W, H, t, S):
    mode = S.opts.get("mode")
    B = beats(S, 4)
    def pHot(c, ts, t0, t1):
        mscape(c, t, hy=760, sun=(1500, 260, 110), heat=ease(prog(t, t0, 1.5)), glare_to=(500, 800))
        temp = lerp(20, 430, ease(prog(t, t0 + 0.2, max(0.8, (t1 - t0) * 0.6))))
        thermometer(c, 330, 470, 520, temp, tmax=450, tmin=-200)
        melt = ease(prog(t, t0 + (t1 - t0) * 0.55, 1.2))
        lead_bar(c, 1050, 880, 260, melt, t)
        C(c, "DAYTIME GROUND: ≈ 430 °C", 1050, 560, vis(t, t0 + 0.4), ts, size=36, dot=EMBER)
        C(c, "HOT ENOUGH TO MELT LEAD", 1050, 670, vis(t, t0 + (t1 - t0) * 0.55), ts, size=34, bg=YEL, fg="#0b1030", a=1)
    def pShade(c, ts):
        t0 = B(1, 0)
        mscape(c, t, hy=700, sun=(1700, 200, 90), heat=0.8, glare_to=(400, 700))
        c.drawPath(poly([(760, 860), (1000, 860), (420, 960), (160, 960)]), paint("#0a1030", 0.85))  # long shadow away from Sun
        boulder(c, 880, 870, 170)
        astro(c, 430, 935, 170, face=1, t=t)
        C(c, "SUNLIT GROUND", 1500, 560, vis(t, t0 + 0.1), ts, size=34, dot=EMBER)
        C(c, "SHADE STAYS COLD", 420, 520, vis(t, B(1, 0.25)), ts, size=34, dot=NIGHT)
        C(c, "NO AIR TO SPREAD THE HEAT", 960, 160, vis(t, B(1, 0.15)), ts, size=32)
        C(c, "NIGHT SIDE: ≈ −180 °C", 960, 270, vis(t, B(1, 0.65)), ts, size=38, bg="#101a4a", dot=ICE)
    def pRange(c, ts):
        t0 = B(2, 0)
        x0, x1, y = 260, 1660, 560
        c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(x0, y - 45, x1, y + 45), 45, 45),
                    paint(shader=lin(x0, y, x1, y, [(0, "#4a78ff", 1), (0.3, "#9fb8ff", 1), (0.6, SCORCH, 1), (1, EMBER, 1)])))
        f = lambda T_: lerp(x0 + 30, x1 - 30, (T_ + 180) / 610)
        for T_, lab in ((-180, "−180 °C"), (0, "0 °C"), (430, "430 °C")):
            line(c, f(T_), y + 50, f(T_), y + 90, "#ffffff", 4, vis(t, t0))
            T(c, lab, f(T_), y + 140, 44, ts, "#ffffff", vis(t, t0 + 0.1), maxw=360)
        q = ease(prog(t, t0 + 0.4, 1.2))
        line(c, f(-180), y - 110, lerp(f(-180), f(430), q), y - 110, YEL, 8)
        T(c, "≈ 600 °C SWING", 960, y - 200, 80, ts, YEL, vis(t, t0 + 1.0), maxw=1400)
    def pSlow(c, ts):
        t0 = B(3, 0)
        mscape(c, t, hy=760, sun=(700, 640 - (t - t0) * 2, 100), glare_to=(1300, 300))
        clock(c, 1450, 400, 150, ((t - t0) * 0.8) % 1)
        C(c, "HOURS PASS…", 1450, 620, vis(t, t0 + 0.4), ts, size=34)
        C(c, "THE SUN BARELY MOVES", 700, 300, vis(t, B(3, 0.5)), ts, size=38, bg=YEL, fg="#0b1030", a=1)
    if mode == "short":
        run_panels(c, W, H, t, S, [(0, lambda c, ts: pHot(c, ts, 0.0, S.le(0)))]); return
    run_panels(c, W, H, t, S, [(0, lambda c, ts: pHot(c, ts, 0.0, S.le(0))), (B(1, 0), pShade), (B(2, 0), pRange), (B(3, 0), pSlow)])

# ------------------------------------------------------------------ me6_dawn
def globe_term(c, x, y, R, t, term_ang, walker=None, a=1.0):
    """Mercury seen from above the north pole: day half toward the Sun (left), terminator rotating slowly."""
    merc(c, x, y, R, sun_ang=180, night=0.0, glow=0.5)
    c.save(); pth = skia.Path(); pth.addCircle(x, y, R); c.clipPath(pth, doAntiAlias=True)
    c.save(); c.translate(x, y); c.rotate(term_ang)
    c.drawRect(skia.Rect.MakeLTRB(0, -R - 2, R + 2, R + 2), paint("#05040c", 0.85))
    c.drawRect(skia.Rect.MakeLTRB(-6, -R - 2, 6, R + 2), paint(YEL, 0.9))
    c.restore(); c.restore()

def me6_dawn(c, W, H, t, S):
    B = beats(S, 5)
    def pSpin(c, ts):
        t0 = 0
        x, y, R = 640, 560, 280
        merc(c, x, y, R, sun_ang=180, night=0.6)
        th = (t - t0) * 0.35
        line(c, x + math.cos(th) * R * 0.95, y - math.sin(th) * R * 0.95, x + math.cos(th) * R * 1.25, y - math.sin(th) * R * 1.25, YEL, 10)
        circle(c, x + math.cos(th) * R * 1.3, y - math.sin(th) * R * 1.3, 18, YEL)
        p = skia.Path(); p.addArc(skia.Rect.MakeLTRB(x - R - 60, y - R - 60, x + R + 60, y + R + 60), -40, -80)
        c.drawPath(p, paint("#ffffff", 0.6, stroke=4)); arrow(c, x + (R + 60) * math.cos(math.radians(-118)), y + (R + 60) * math.sin(math.radians(-118)),
                                                               x + (R + 60) * math.cos(math.radians(-125)), y + (R + 60) * math.sin(math.radians(-125)), "#ffffff", 4, 0.6)
        C(c, "1 SPIN ≈ 59 EARTH DAYS", 1420, 380, vis(t, B(0, 0.1)), ts, size=38, dot=YEL)
        C(c, "1 ORBIT = 88 EARTH DAYS", 1420, 500, vis(t, B(0, 0.6)), ts, size=38, dot=SCORCH)
    def pCount(c, ts):
        t0 = B(1, 0)
        days = int(176 * ease(prog(t, B(1, 0.35), (B(1, 0.95) - B(1, 0.35)))))
        T(c, "SUNRISE → SUNRISE", 960, 300, 64, ts, "#ffffff", vis(t, t0), maxw=1500)
        T(c, f"{days}", 960, 540, 260, ts, YEL, vis(t, B(1, 0.3)), maxw=900, shadow=20)
        T(c, "EARTH DAYS", 960, 720, 56, ts, SCORCH, vis(t, B(1, 0.3)), maxw=900)
    def pWalk(c, ts):
        t0 = B(2, 0)
        x, y, R = 700, 560, 330
        glare_sun(c, 40, 560, 70, t, flare_to=(x, y), flare=0.5)
        globe_term(c, x, y, R, t, -90 + 4 * math.sin(t * 0.1) + (t - t0) * 1.2)
        ang = math.radians(-90 + (t - t0) * 1.2)
        wx, wy = x + math.cos(ang) * R * 0.75, y + math.sin(ang) * R * 0.75
        circle(c, wx, wy, 16, "#ffffff"); circle(c, wx, wy, 30, "#ffffff", 0.4, stroke=4)
        C(c, "DAWN LINE", x, 150, vis(t, t0 + 0.2), ts, size=34, dot=YEL)
        T(c, "≈ 3.5 KM/H", 1480, 420, 110, ts, YEL, vis(t, B(2, 0.45)), maxw=700)
        C(c, "BY OUR ROUGH MATH (EQUATOR, AVERAGE)", 1480, 540, vis(t, B(2, 0.5)), ts, size=26)
        C(c, "SLOWER THAN A BRISK WALK", 1480, 660, vis(t, B(2, 0.75)), ts, size=34, dot=GREEN)
    def pStrip(c, ts):
        t0 = B(3, 0)
        hy = 700
        stage_bg(c, "#020103", "#0b0608"); stars(c, VW, VH, t, 0.8, seed=74)
        c.drawImage(ground_img(hy, 5), 0, 0)
        tx = 960
        c.drawRect(skia.Rect.MakeLTRB(tx, hy - 80, VW, VH), paint(shader=lin(tx, 0, VW, 0, [(0, EMBER, 0.15), (1, EMBER, 0.5)])))
        c.drawRect(skia.Rect.MakeLTRB(0, hy - 80, tx, VH), paint(shader=lin(0, 0, tx, 0, [(0, "#0a1440", 0.75), (1, "#0a1440", 0.25)])))
        line(c, tx, hy - 120, tx, VH, YEL, 6, 0.9)
        glare_sun(c, VW + 40, hy - 150, 80, t, flare_to=(tx, 500), flare=0.4)
        astro(c, tx - 50, 900, 200, walk=1.0, t=t, face=-1)
        C(c, "NOON HEAT →", 1500, 300, vis(t, t0 + 0.4), ts, size=34, bg="#3a1408", dot=EMBER)
        C(c, "← NIGHT COLD", 420, 300, vis(t, t0 + 0.6), ts, size=34, bg="#101a4a", dot=ICE)
        C(c, "STAY AT DAWN FOREVER (IN THEORY)", 960, 150, vis(t, B(3, 0.45)), ts, size=34, bg=YEL, fg="#0b1030", a=1)
    def pCity(c, ts):
        t0 = B(4, 0)
        hy = 680
        stage_bg(c, "#020103", "#0b0608"); stars(c, VW, VH, t, 0.8, seed=75)
        c.drawImage(ground_img(hy, 6), 0, 0)
        glare_sun(c, VW + 20, hy - 60, 70, t, flare_to=(900, 400), flare=0.4)
        for k in range(2): line(c, 0, 880 + k * 30, VW, 880 + k * 30, "#c9ccd6", 5, 0.7)
        ox = 300 + (t - t0) * 12
        for i in range(5):
            x = ox + i * 230
            rrect(c, x, 760, 210, 110, 20, "#4a413d"); rect(c, x, 860, 210, 20, "#2a2320")
            p = skia.Path(); p.addArc(skia.Rect.MakeXYWH(x + 15, 650, 180, 220), 180, 180); p.close()
            c.drawPath(p, paint("#bfe3ff", 0.35)); c.drawPath(p, paint("#e8f4ff", 0.8, stroke=3))
            for k in range(3): rect(c, x + 40 + k * 50, 720, 22, 40, YEL, 0.7)
            for k in (40, 170): circle(c, x + k, 880, 18, "#c9ccd6")
        C(c, "“2312” · NOVEL BY KIM STANLEY ROBINSON", 960, 170, vis(t, t0 + 0.2), ts, size=32, dot="#ffffff")
        C(c, "A CITY ON RAILS: TERMINATOR", 960, 280, vis(t, B(4, 0.4)), ts, size=36, bg=YEL, fg="#0b1030", a=1)
        C(c, "SCIENCE FICTION", 1600, 400, vis(t, B(4, 0.2)), ts, size=26)
    run_panels(c, W, H, t, S, [(0, pSpin), (B(1, 0), pCount), (B(2, 0), pWalk), (B(3, 0), pStrip), (B(4, 0), pCity)])

# ------------------------------------------------------------------ me6_year
def sun_path(c, t, t0, x0, x1, hy, amp, dur, ts, colr=GLARE, look="me", r=46):
    """stylised double-sunrise: the Sun peeks up, sinks back, then rises for good (not to scale)."""
    def ypath(f):
        if f < 0.35: return hy - amp * 0.35 * math.sin(f / 0.35 * math.pi / 2)
        if f < 0.55: return hy - amp * 0.35 * math.cos((f - 0.35) / 0.2 * math.pi / 2) + amp * 0.1 * math.sin((f - 0.35) / 0.2 * math.pi)
        return hy - amp * (f - 0.55) / 0.45 * 1.0
    q = clamp((t - t0) / dur)
    p = skia.Path()
    for i in range(61):
        f = i / 60 * q; x = lerp(x0, x1, f); y = ypath(f)
        p.moveTo(x, y) if i == 0 else p.lineTo(x, y)
    c.drawPath(p, paint(YEL, 0.75, stroke=4, dash=([12, 8], 0)))
    x, y = lerp(x0, x1, q), ypath(q)
    if look == "me": glare_sun(c, x, y, r, t, flare=0)
    else: sun(c, x, y, r * 0.8, t)
    return q

def me6_year(c, W, H, t, S):
    B = beats(S, 5)
    segs = [(0, 0), (B(0, 0.85), 88), (B(1, 0.15), 88), (B(1, 0.95), 176)]
    def pOrbit(c, ts):
        days = days_map(t, segs)
        px, py, lit = orbit_view(c, t, days, 820, 560, 470, ts, pr=48, sun_r=55)
        yrs = days / P_ORB; spins = days / P_SPIN
        T(c, f"DAY {int(days)}", 1600, 250, 80, ts, "#ffffff", 1, maxw=560)
        C(c, f"ORBITS: {yrs:.1f}", 1600, 400, 1, ts, size=36, dot=SCORCH)
        C(c, f"SPINS: {spins:.1f}", 1600, 500, 1, ts, size=36, dot=YEL)
        C(c, "YEAR 1 OVER", 1600, 640, vis(t, B(0, 0.85), B(1, 0.2)), ts, size=36, bg=YEL, fg="#0b1030", a=1)
        C(c, "STILL THE SAME DAY", 1600, 640, vis(t, B(1, 0.2)), ts, size=36, dot=YEL)
        C(c, "3 SPINS : 2 ORBITS", 1600, 760, vis(t, B(1, 0.4)), ts, size=36, dot=GREEN)
        C(c, "1 DAY = 2 YEARS", 820, 1010, vis(t, B(1, 0.85)), ts, size=40, bg=YEL, fg="#0b1030", a=1)
    def pRadar(c, ts):
        t0 = B(2, 0)
        merc(c, 1450, 520, 170, sun_ang=180)
        circle(c, 300, 680, 70, "#6fb6ff")
        line(c, 300, 610, 340, 540, "#c9ccd6", 10); oval(c, 350, 525, 45, 22, "#e8eef8")
        for k in range(5):
            q = ((t - t0) * 0.5 + k / 5) % 1
            x = lerp(400, 1270, q)
            p = skia.Path(); p.addArc(skia.Rect.MakeLTRB(x - 60, 520 - 140, x + 60, 520 + 140), -40, 80)
            c.drawPath(p, paint(SIG, 0.8 * math.sin(q * math.pi), stroke=5))
        C(c, "1965: RADAR", 300, 300, vis(t, t0 + 0.1), ts, size=40, bg=YEL, fg="#0b1030", a=1)
        C(c, "OLD IDEA: ONE FACE ALWAYS TO THE SUN", 1000, 900, vis(t, B(2, 0.5)), ts, size=32)
        xmark(c, 1000 + (430 if not S.P else 760), 900, 34, vis(t, B(2, 0.75)))
    def pPeri(c, ts):
        t0 = B(3, 0)
        days = 75 + (t - t0) * 3.0
        orbit_view(c, t, days, 960, 560, 500, ts, pr=40, sun_r=50, show_marker=False)
        T(c, "FASTEST HERE", 960 + 500 * (1 - ECC) + 40, 470, 34, ts, YEL, vis(t, B(3, 0.4)), align="l", maxw=400)
        C(c, "STRETCHED ORBIT", 400, 160, vis(t, t0 + 0.1), ts, size=34, dot=SCORCH)
        C(c, "ORBIT BRIEFLY OUTRUNS THE SPIN", 960, 980, vis(t, B(3, 0.6)), ts, size=34, bg=YEL, fg="#0b1030", a=1)
    def pDouble(c, ts):
        t0 = B(4, 0)
        mscape(c, t, hy=760, star_a=1.0)
        q = sun_path(c, t, t0 + 0.2, 300, 1500, 790, 520, (B(4, 0.55) - t0 - 0.2), ts)
        c.drawImageRect(ground_img(760, 3), skia.Rect.MakeXYWH(0, 760, VW, VH - 760), skia.Rect.MakeXYWH(0, 760, VW, VH - 760), skia.SamplingOptions(), skia.Paint())
        C(c, "RISE", 420, 640, vis(t, t0 + 0.6), ts, size=30)
        C(c, "SINK BACK", 720, 900, vis(t, B(4, 0.15)), ts, size=30)
        C(c, "RISE AGAIN", 1300, 420, vis(t, B(4, 0.3)), ts, size=30)
        C(c, "DOUBLE SUNRISE", 960, 150, vis(t, B(4, 0.25)), ts, size=40, bg=YEL, fg="#0b1030", a=1)
        C(c, "NOT TO SCALE", 1700, 1010, vis(t, t0 + 0.3), ts, size=22)
        C(c, "ELSEWHERE: NOON SUN STALLS FOR WEEKS", 960, 260, vis(t, B(4, 0.65)), ts, size=30, dot=YEL)
    run_panels(c, W, H, t, S, [(0, pOrbit), (B(2, 0), pRadar), (B(3, 0), pPeri), (B(4, 0), pDouble)])

# ------------------------------------------------------------------ me6_night
def base(c, x, y, s, t, heat=0.0, a=1.0):
    p = skia.Path(); p.addArc(skia.Rect.MakeXYWH(x - s, y - s, 2 * s, 2 * s), 180, 180); p.close()
    c.drawPath(p, paint("#d8dde6", a)); c.drawPath(p, paint("#8a93a3", a, stroke=4))
    for k in range(3): rect(c, x - s * 0.6 + k * s * 0.45, y - s * 0.45, s * 0.25, s * 0.2, YEL, a * 0.9)
    rect(c, x + s * 0.8, y - s * 1.3, 8, s * 0.9, "#c9ccd6", a); oval(c, x + s * 0.84, y - s * 1.35, s * 0.25, s * 0.08, "#e8eef8", a)
    if heat > 0:
        for k in range(3):
            q = (t * 0.7 + k / 3) % 1
            circle(c, x, y - s * 0.4, s * (0.6 + q * 0.9), EMBER, heat * 0.4 * (1 - q), stroke=6)

def me6_night(c, W, H, t, S):
    mode = S.opts.get("mode")
    long_ = mode != "short"
    B = beats(S, 4)
    def pSet(c, ts, t0, t1):
        f = ease(prog(t, t1, 4.0)) if t1 is not None else 0
        mscape(c, t, hy=700, sun=(1500, 690 + f * 120, 95), cold=f, glare_to=(500, 500))
        base(c, 560, 700, 150, t, heat=0)
        C(c, "SUNSET: ~88 DAYS AFTER SUNRISE", 960, 170, vis(t, t1 if t1 is not None else t0), ts, size=34, dot=SCORCH)
        C(c, "NIGHT: ~3 EARTH MONTHS", 960, 280, vis(t, (t1 or t0) + 2.5), ts, size=36, bg="#101a4a", dot=ICE)
    def pCool(c, ts):
        t0 = B(2, 0)
        mscape(c, t, hy=700, cold=1.0, star_a=1.0)
        for k in range(9):
            q = ((t - t0) * 0.4 + k / 9) % 1; x = 200 + k * 190
            p = skia.Path(); y0 = 760 - q * 500
            p.moveTo(x, y0)
            for j in range(1, 7): p.lineTo(x + (12 if j % 2 else -12), y0 - j * 18)
            c.drawPath(p, paint("#ff9a6a", 0.6 * math.sin(q * math.pi), stroke=4))
        temp = lerp(100, -180, ease(prog(t, t0 + 0.3, 3.0)))
        thermometer(c, 1360, 420, 480, temp, tmax=450, tmin=-200)
        C(c, "HEAT ESCAPES TO SPACE", 700, 200, vis(t, t0 + 0.2), ts, size=36, dot="#ff9a6a")
    def pBase(c, ts):
        t0 = B(3, 0)
        mscape(c, t, hy=700, cold=1.0, star_a=1.0)
        base(c, 960, 720, 190, t, heat=1.0)
        C(c, "HEATERS, NOT COOLERS", 960, 230, vis(t, t0 + 0.1), ts, size=40, bg=YEL, fg="#0b1030", a=1)
        C(c, "SUN UP: FRY", 450, 400, vis(t, B(3, 0.45)), ts, size=36, bg="#3a1408", dot=EMBER)
        C(c, "SUN DOWN: FREEZE", 1470, 400, vis(t, B(3, 0.6)), ts, size=36, bg="#101a4a", dot=ICE)
    def pBars(c, ts):
        # Short: one full day = 88 days light + 88 days dark
        x0, x1, y = 200, 1720, 420
        q = ease(prog(t, 0.2, S.lt(0, 0.5)))
        xm = lerp(x0, x1, 0.5)
        rrect(c, x0, y - 50, (xm - x0) * clamp(q * 2), 100, 20, SCORCH)
        if q > 0.5: rrect(c, xm, y - 50, (x1 - xm) * clamp(q * 2 - 1), 100, 20, "#2a3f9a")
        T(c, "DAY ~88", lerp(x0, xm, 0.5), y, 48, ts, "#0b1030", vis(t, 0.5), maxw=650)
        T(c, "NIGHT ~88", lerp(xm, x1, 0.5), y, 48, ts, "#ffffff", vis(t, S.lt(0, 0.3)), maxw=650)
        T(c, "1 MERCURY DAY ≈ 176 EARTH DAYS", 960, 230, 56, ts, YEL, vis(t, 0.2), maxw=1700)
        thermometer(c, 760, 760, 360, lerp(430, -180, ease(prog(t, S.lt(0, 0.55), 1.5))), tmax=450, tmin=-200, size=1.7)
    if not long_:
        run_panels(c, W, H, t, S, [(0, pBars)]); return
    run_panels(c, W, H, t, S, [(0, lambda c, ts: pSet(c, ts, 0.0, B(1, 0.0))), (B(2, 0), pCool), (B(3, 0), pBase)])

# ------------------------------------------------------------------ me6_poles
def crater_xs(c, t, ts, ice=0.0, dark=0.0, sun=True, x0=160, x1=1760, floor=820, rim=520):
    """crater cross-section at the pole: grazing sunlight never reaches the floor."""
    mid = (x0 + x1) / 2
    stage_bg(c, "#020103", "#0b0608"); stars(c, VW, VH, t, 0.8, seed=76)
    if sun: glare_sun(c, -30, rim - 40, 80, t, flare_to=(mid, floor), flare=0.4)
    sp = skia.Path(); sp.moveTo(-20, rim + 40); sp.lineTo(x0, rim)
    sp.cubicTo(x0 + 220, rim, mid - 420, floor, mid, floor); sp.cubicTo(mid + 420, floor, x1 - 220, rim, x1, rim); sp.lineTo(VW + 20, rim + 40)
    p = skia.Path(sp); p.lineTo(VW + 20, VH + 20); p.lineTo(-20, VH + 20); p.close()
    c.drawPath(p, paint(shader=lin(0, rim, 0, VH, [(0, "#4a403b", 1), (1, "#1c1715", 1)])))
    # permanent shadow: the air below the grazing ray from the left rim, inside the crater
    slope = 60 / (x1 - 120 - x0)
    sh = skia.Path(); sh.moveTo(x0, rim); sh.lineTo(VW + 10, rim + slope * (VW + 10 - x0)); sh.lineTo(VW + 10, VH); sh.lineTo(x0, VH); sh.close()
    air = skia.Op(sh, p, skia.PathOp.kDifference_PathOp)
    if air: c.drawPath(air, paint("#0a1030", 0.55))
    lit = skia.Op(p, sh, skia.PathOp.kDifference_PathOp)
    if lit:
        c.save(); c.clipPath(lit, doAntiAlias=True); c.drawPath(sp, paint("#e0a070", 0.85, stroke=26)); c.restore()
    c.save(); c.clipPath(sh, doAntiAlias=True); c.drawPath(sp, paint("#20243a", 0.9, stroke=20)); c.restore()
    if sun:
        for k in range(4):
            yy = rim - 140 + k * 40
            line(c, 0, yy, VW, yy + 60 + k * 10, "#ffd9a0", 3, 0.35, dash=([30, 18], -t * 60))
    if ice > 0:
        c.save(); c.clipPath(p, doAntiAlias=True)
        oval(c, mid, floor + 10, 380 * ice, 40, ICE, 0.85)
        for k in range(10):
            x = mid - 300 + k * 66
            circle(c, x, floor + 2, 5, "#ffffff", 0.5 + 0.5 * math.sin(t * 3 + k))
        if dark > 0:
            oval(c, mid, floor + 2, 400 * dark, 26, "#1a1410", 0.95 * dark)
            for k in range(8): circle(c, mid - 280 + k * 80, floor - 6, 6, "#3a2a1a", dark)
        c.restore()
    return mid, floor

def me6_poles(c, W, H, t, S):
    mode = S.opts.get("mode")
    B = beats(S, 6)
    def pTilt(c, ts):
        t0 = 0
        for (x, ang, lab, colr, R) in ((560, 2, "MERCURY ~2°", SCORCH, 230), (1360, 23.4, "EARTH ~23°", "#6fb6ff", 230)):
            if lab.startswith("M"): merc(c, x, 540, R, sun_ang=180)
            else:
                earth(c, x, 540, R, rot=t * 6 + 40, sun_dir=-1)
            c.save(); c.translate(x, 540); c.rotate(ang)
            line(c, 0, -R - 90, 0, R + 90, "#ffffff", 5, 0.9, dash=([16, 10], 0)); c.restore()
            T(c, lab, x, 900, 46, ts, colr, vis(t, B(1, 0.05) if lab.startswith("M") else B(1, 0.2)), maxw=600)
        glare_sun(c, -60, 540, 80, t, flare_to=(960, 540), flare=0.3)
        C(c, "THE BEST ADDRESS: THE POLES?", 960, 120, vis(t, B(0, 0.4)), ts, size=36, dot=ICE)
    def pShadow(c, ts):
        crater_xs(c, t, ts)
        C(c, "SUN SKIMS THE HORIZON", 960, 150, vis(t, B(1, 0.45)), ts, size=36, dot=YEL)
        C(c, "NEVER SUNLIT", 960, 900, vis(t, B(1, 0.7)), ts, size=40, bg="#101a4a", dot=ICE)
    def pIce(c, ts, t0):
        crater_xs(c, t, ts, ice=ease(prog(t, t0 + 0.3, 1.0)))
        C(c, "2012: MESSENGER CONFIRMS", 960, 140, vis(t, t0 + 0.1), ts, size=36, dot="#9fb8ff")
        C(c, "WATER ICE", 960, 250, vis(t, t0 + 0.8), ts, size=44, bg=ICE, fg="#0b1030", a=1)
    def pTonnes(c, ts):
        t0 = B(3, 0)
        stage_bg(c, "#05060e", "#101a30")
        gy = 880
        rect(c, 0, gy, VW, VH - gy, "#2a2f3a")
        rng = random.Random(8); x = 860
        while x < 1880:
            bw = rng.uniform(30, 70); bh = rng.uniform(30, 110)
            rect(c, x, gy - bh, bw, bh, "#4a5060"); x += bw + 6
        q = ease(prog(t, B(3, 0.45), 1.6))
        hh = 700 * q
        c.drawRect(skia.Rect.MakeLTRB(860, gy - hh, 1880, gy), paint(shader=lin(0, gy - hh, 0, gy, [(0, "#d8f6ff", 0.85), (1, ICE, 0.65)])))
        c.drawRect(skia.Rect.MakeLTRB(860, gy - hh, 1880, gy), paint("#ffffff", 0.8, stroke=4))
        line(c, 820, gy, 820, gy - hh, "#ffffff", 4, vis(t, B(3, 0.6)))
        T(c, "> 3 KM", 690, gy - hh * 0.6, 64, ts, ICE, vis(t, B(3, 0.7)), maxw=360)
        T(c, "100 BILLION – 1 TRILLION", 470, 300, 54, ts, "#ffffff", vis(t, t0 + 0.1), maxw=820)
        T(c, "TONNES OF ICE (ESTIMATE)", 470, 380, 40, ts, ICE, vis(t, t0 + 0.2), maxw=820)
        C(c, "AN AREA THE SIZE OF WASHINGTON, D.C.", 470, 790, vis(t, B(3, 0.4)), ts, size=26)
    def pDark(c, ts):
        t0 = B(4, 0)
        mid, floor = crater_xs(c, t, ts, ice=1.0, dark=ease(prog(t, t0 + 0.2, 1.0)))
        q = ((t - t0) * 0.35) % 1
        cx_, cy_ = lerp(1700, 1100, q), lerp(80, 420, q)
        circle(c, cx_, cy_, 22, "#e8f4ff", 0.9 * math.sin(q * math.pi))
        line(c, cx_ + 20, cy_ - 14, cx_ + 160, cy_ - 110, "#bfe3ff", 10, 0.4 * math.sin(q * math.pi))
        C(c, "DARK LAYER: LIKELY ORGANIC", 960, 150, vis(t, t0 + 0.4), ts, size=36, dot="#c08a5a")
        C(c, "DELIVERED BY COMETS + ASTEROIDS?", 960, 260, vis(t, B(4, 0.55)), ts, size=30)
    def pUse(c, ts):
        t0 = B(5, 0)
        items = [("WATER", ICE), ("OXYGEN", "#bfe3ff"), ("FUEL", SCORCH), ("SOLAR POWER", YEL)]
        for k, (lab, colr) in enumerate(items):
            x = 300 + k * 440; p = vis(t, t0 + 0.2 + k * 0.6)
            circle(c, x, 500, 130 * eback(p), colr, 0.18 * p); circle(c, x, 500, 130 * eback(p), colr, p, stroke=6)
            if k == 0:
                pth = skia.Path(); pth.moveTo(x, 420); pth.cubicTo(x + 70, 500, x + 60, 580, x, 580); pth.cubicTo(x - 60, 580, x - 70, 500, x, 420)
                c.drawPath(pth, paint(colr, p))
            elif k == 1:
                for j, (dx, dy, r) in enumerate([(-30, 20, 40), (35, -10, 30), (5, -60, 22)]): circle(c, x + dx, 500 + dy, r, colr, p, stroke=6)
            elif k == 2:
                rrect(c, x - 40, 430, 80, 140, 20, colr, p); rect(c, x - 15, 410, 30, 24, colr, p)
            else:
                circle(c, x, 500, 50, colr, p)
                for j in range(8):
                    an = j * math.pi / 4; line(c, x + math.cos(an) * 70, 500 + math.sin(an) * 70, x + math.cos(an) * 95, 500 + math.sin(an) * 95, colr, 8, p)
            T(c, lab, x, 720, 40, ts, colr, p, maxw=420)
    if mode == "short":
        run_panels(c, W, H, t, S, [(0, lambda c, ts: pIce(c, ts, 0.0))]); return
    run_panels(c, W, H, t, S, [(0, pTilt), (B(1, 0.4), pShadow), (B(2, 0), lambda c, ts: pIce(c, ts, B(2, 0))), (B(3, 0), pTonnes),
                               (B(4, 0), pDark), (B(5, 0), pUse)])

# ------------------------------------------------------------------ me6_shrink
def scarp(c, x0, x1, y, h, t, a=1.0):
    """thrust-fault cliff: the right block rides up over the left one."""
    c.drawRect(skia.Rect.MakeLTRB(x0, y, x1, VH), paint(shader=lin(0, y, 0, VH, [(0, "#5b504a", a), (1, "#241e1b", a)])))
    m = (x0 + x1) / 2
    p = skia.Path(); p.moveTo(m - 80, y); p.cubicTo(m - 30, y - h * 0.2, m, y - h, m + 120, y - h)
    p.lineTo(x1, y - h); p.lineTo(x1, VH); p.lineTo(m - 80, VH); p.close()
    c.drawPath(p, paint(shader=lin(0, y - h, 0, VH, [(0, "#7a6c64", a), (1, "#2e2724", a)])))
    face = skia.Path(); face.moveTo(m - 80, y); face.cubicTo(m - 30, y - h * 0.2, m, y - h, m + 120, y - h); face.lineTo(m + 160, y - h + 30)
    face.cubicTo(m + 40, y - h * 0.6, m + 20, y - h * 0.1, m + 40, y + 20); face.close()
    c.drawPath(face, paint("#e0a070", 0.45 * a))
    rng = random.Random(9)
    for k in range(18):
        xx = rng.uniform(x0, x1); top = y - h if xx > m + 120 else y
        yy = top + 20 + rng.random() * 180; rx = rng.uniform(25, 70)
        oval(c, xx, yy, rx, rx * 0.22, "#2c2421", 0.7 * a)
    line(c, (x0 + x1) / 2 - 80, y, (x0 + x1) / 2 + 300, VH, "#1a1412", 4, a * 0.8, dash=([14, 10], 0))

def me6_shrink(c, W, H, t, S):
    B = beats(S, 4)
    def pCrack(c, ts):
        t0 = 0
        stage_bg(c, "#020103", "#0b0608"); stars(c, VW, VH, t, 0.8, seed=77)
        glare_sun(c, 1850, 360, 70, t, flare_to=(600, 700), flare=0.4)
        h = 260 * ease(prog(t, 0.3, max(1.0, S.le(0) - 0.3)))
        scarp(c, 0, VW, 720, h, t)
        astro(c, 520, 720, 160, t=t, face=1)
        C(c, "THE GROUND IS SHRINKING", 960, 160, vis(t, 0.2), ts, size=40, bg=YEL, fg="#0b1030", a=1)
    def pCore(c, ts):
        t0 = B(1, 0)
        x, y, R = 640, 560, 330
        merc(c, x, y, R, sun_ang=200, night=0.5)
        c.save(); c.translate(x, y)
        p = skia.Path(); p.moveTo(0, 0); p.arcTo(skia.Rect.MakeLTRB(-R, -R, R, R), -90, 90, False); p.close()
        cut = ease(prog(t, t0 + 0.2, 0.8))
        if cut > 0:
            c.drawPath(p, paint("#5a4a42", cut))
            q = skia.Path(); q.moveTo(0, 0); q.arcTo(skia.Rect.MakeLTRB(-R * 0.85, -R * 0.85, R * 0.85, R * 0.85), -90, 90, False); q.close()
            c.drawPath(q, paint(shader=rad(0, 0, R * 0.85, [(0, "#ffd08a", cut), (0.6, "#e0603a", cut), (1, "#9a3a22", cut)])))
        c.restore()
        line(c, x, y, x + R * 0.85, y, "#ffffff", 4, vis(t, B(1, 0.25)))
        T(c, "CORE ≈ 85% OF RADIUS", 1450, 300, 52, ts, SCORCH, vis(t, B(1, 0.25)), maxw=800)
        # peach analogy
        px, py = 1450, 600
        pa = vis(t, B(1, 0.5))
        circle(c, px, py, 120, "#ffb07a", pa); circle(c, px, py, 98, "#8a4a2a", pa)
        line(c, px, py - 120, px + 20, py - 160, "#5a3a1a", 8, pa)
        T(c, "A PEACH THAT'S ALMOST ALL STONE", px, py + 190, 32, ts, "#ffffff", pa, w=700, fam="Inter", maxw=800)
        C(c, "2ND DENSEST PLANET (AFTER EARTH)", 960, 1000, vis(t, B(1, 0.8)), ts, size=30, dot=YEL)
    def pShrink(c, ts):
        t0 = B(2, 0)
        x, y, R0 = 960, 560, 360
        q = ease(prog(t, t0 + 0.5, 2.5))
        R = R0 * (1 - 0.12 * q)
        c.drawCircle(x, y, R0, paint("#ffffff", 0.6, stroke=4, dash=([16, 12], 0)))
        merc(c, x, y, R, sun_ang=200, night=0.6)
        for k in range(8):
            an = k * math.pi / 4
            arrow(c, x + math.cos(an) * (R0 + 70), y + math.sin(an) * (R0 + 70), x + math.cos(an) * (R + 20), y + math.sin(an) * (R + 20), "#ffffff", 5, 0.7 * q)
        T(c, "UP TO 7 KM", 1620, 420, 80, ts, YEL, vis(t, B(2, 0.6)), maxw=500)
        T(c, "SMALLER RADIUS", 1620, 510, 36, ts, "#ffffff", vis(t, B(2, 0.6)), maxw=500)
        C(c, "MESSENGER MAPS, 2014", 300, 300, vis(t, B(2, 0.45)), ts, size=30, dot="#9fb8ff")
        C(c, "EXAGGERATED", 300, 820, vis(t, t0 + 0.5), ts, size=26)
    def pScarp(c, ts):
        t0 = B(3, 0)
        stage_bg(c, "#020103", "#0b0608"); stars(c, VW, VH, t, 0.8, seed=78)
        glare_sun(c, 1880, 300, 60, t, flare=0)
        scarp(c, 0, VW, 760, 300, t)
        C(c, "LOBATE SCARPS", 960, 150, vis(t, t0 + 0.1), ts, size=40, bg=YEL, fg="#0b1030", a=1)
        C(c, "HUNDREDS OF KM LONG", 520, 300, vis(t, B(3, 0.45)), ts, size=34, dot=SCORCH)
        C(c, "UP TO ~3 KM HIGH", 1420, 300, vis(t, B(3, 0.7)), ts, size=34, dot=SCORCH)
    run_panels(c, W, H, t, S, [(0, pCrack), (B(1, 0), pCore), (B(2, 0), pShrink), (B(3, 0), pScarp)])

# ------------------------------------------------------------------ me6_field
def field_lines(c, x, y, R, t, k=1.0, a=1.0, colr=MAGC, squash=0.55):
    for i in range(1, 6):
        L = R * (1.2 + i * 0.45)
        for s_ in (-1, 1):
            p = skia.Path()
            for j in range(41):
                th = -math.pi / 2 + j / 40 * math.pi
                r = L * math.cos(th) ** 2
                xx = x + s_ * r * math.cos(th) * (squash if s_ < 0 else 1.3) * k
                yy = y + r * math.sin(th) * k
                p.moveTo(xx, yy) if j == 0 else p.lineTo(xx, yy)
            c.drawPath(p, paint(colr, a * (0.6 - i * 0.07), stroke=3, dash=([18, 10], -t * 20 * s_)))

def me6_field(c, W, H, t, S):
    B = beats(S, 2)
    def pA(c, ts):
        x, y, R = 900, 560, 150
        for k in range(7):
            q = ((t * 0.5) + k / 7) % 1
            yy = 200 + k * 110
            arrow(c, lerp(-60, 500, q), yy, lerp(0, 560, q), yy, "#ffd2a0", 5, 0.6 * math.sin(q * math.pi))
        field_lines(c, x, y, R, t)
        merc(c, x, y, R, sun_ang=180)
        T(c, "SOLAR WIND →", 260, 120, 34, ts, "#ffd2a0", vis(t, 0.3), maxw=500)
        bar(c, 1350, 560, 450, 44, 1.0 * ease(prog(t, B(0, 0.3), 0.6)), "#6fb6ff", 1.0)
        bar(c, 1350, 700, 450, 44, 0.01 * ease(prog(t, B(0, 0.4), 0.6)) + 0.001, MAGC, 1.0)
        T(c, "EARTH 100%", 1350, 530, 32, ts, "#6fb6ff", vis(t, B(0, 0.3)), align="l", maxw=440, w=800)
        T(c, "MERCURY ~1%", 1350, 670, 32, ts, MAGC, vis(t, B(0, 0.4)), align="l", maxw=440, w=800)
        C(c, "A WEAK SHIELD", 1575, 380, vis(t, B(0, 0.7)), ts, size=34, dot=MAGC)
    def pB(c, ts):
        t0 = B(1, 0)
        mscape(c, t, hy=820, sun=(1800, 180, 70), glare_to=(600, 600))
        cx = 900
        for k in range(26):  # twisting funnel
            f = k / 25; y = 120 + f * 680; r = lerp(260, 30, f)
            ph = t * 3 + f * 9
            oval(c, cx + math.sin(f * 3 + t) * 30, y, r, r * 0.22, MAGC, 0.25 + 0.2 * math.sin(ph))
        rng = random.Random(4)
        for k in range(40):
            q = ((t - t0) * 0.4 + rng.random()) % 1; f = q; y = 120 + f * 680; r = lerp(260, 30, f)
            an = t * 4 + k
            circle(c, cx + math.sin(f * 3 + t) * 30 + math.cos(an) * r, y + math.sin(an) * r * 0.22, 6, YEL, 0.9)
        base(c, 1450, 820, 120, t)
        p = skia.Path(); p.addArc(skia.Rect.MakeXYWH(1450 - 210, 820 - 210, 420, 420), 180, 180)
        c.drawPath(p, paint("#9fd0ff", 0.7 * vis(t, B(1, 0.6)), stroke=8)); c.drawPath(p, paint("#9fd0ff", 0.12 * vis(t, B(1, 0.6))))
        C(c, "“MAGNETIC TORNADOES” (NASA)", 600, 180, vis(t, t0 + 0.1), ts, size=34, dot=MAGC)
        C(c, "RADIATION SHIELDING", 1450, 470, vis(t, B(1, 0.6)), ts, size=34, bg=YEL, fg="#0b1030", a=1)
    run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB)])

# ------------------------------------------------------------------ me6_einstein
def me6_einstein(c, W, H, t, S):
    B = beats(S, 4)
    def pRose(c, ts, t0, grid=False):
        sx, sy = 820, 560; a_ = 430; b_ = a_ * math.sqrt(1 - 0.45 ** 2)
        if grid:
            g = ease(prog(t, t0, 1.0))
            for k in range(-8, 9):
                p = skia.Path(); p2 = skia.Path()
                for j in range(61):
                    u_ = -900 + j * 30; v = k * 70
                    d = math.hypot(u_, v) + 1; sink = g * 9000 / (d + 120)
                    x1_, y1_ = sx + u_ - u_ / d * sink * 0.6, sy + v - v / d * sink * 0.6
                    x2_, y2_ = sx + v - v / d * sink * 0.6, sy + u_ - u_ / d * sink * 0.6
                    p.moveTo(x1_, y1_) if j == 0 else p.lineTo(x1_, y1_)
                    p2.moveTo(x2_, y2_) if j == 0 else p2.lineTo(x2_, y2_)
                c.drawPath(p, paint("#9fb8ff", 0.18, stroke=2)); c.drawPath(p2, paint("#9fb8ff", 0.18, stroke=2))
        glare_sun(c, sx, sy, 45, t, flare=0)
        prec = (t - t0) * 6
        for k in range(6):
            ang = prec - k * 12
            if ang < -1 and k > 0: continue
            c.save(); c.translate(sx, sy); c.rotate(ang); c.translate(-a_ * 0.45, 0)
            c.drawOval(skia.Rect.MakeLTRB(-a_, -b_, a_, b_), paint(SCORCH, 0.8 if k == 0 else 0.25 * (1 - k / 6), stroke=4 if k == 0 else 2))
            if k == 0:
                circle(c, a_ * 1.45 - a_ * 0.45 + a_ * 0.0, 0, 0, SCORCH)
                th = (t - t0) * 1.6
                merc(c, math.cos(th) * a_, math.sin(th) * b_, 26, sun_ang=0, night=0.4, glow=0.4)
            c.restore()
            rad_ = math.radians(ang); px, py = sx + math.cos(rad_) * a_ * 0.55, sy + math.sin(rad_) * a_ * 0.55
            circle(c, px, py, 10 if k == 0 else 6, YEL, 1 if k == 0 else 0.5)
    def pA(c, ts):
        pRose(c, ts, 0.0)
        C(c, "THE PLANET THAT HELPED PROVE EINSTEIN RIGHT", 960, 110, vis(t, 0.3), ts, size=32, bg=YEL, fg="#0b1030", a=1)
    def pB(c, ts):
        pRose(c, ts, B(1, 0))
        C(c, "THE ORBIT SLOWLY SWINGS AROUND", 1550, 300, vis(t, B(1, 0.1)), ts, size=30, dot=SCORCH)
        C(c, "1859: URBAIN LE VERRIER", 1550, 410, vis(t, B(1, 0.4)), ts, size=32, dot="#ffffff")
        C(c, "TOO FAST FOR NEWTON", 1550, 520, vis(t, B(1, 0.7)), ts, size=34, bg="#3a1010", dot=RED)
    def pC(c, ts):
        t0 = B(2, 0)
        T(c, "43″ PER CENTURY", 960, 260, 120, ts, YEL, vis(t, t0 + 0.1), maxw=1600)
        y = 700
        astro(c, 220, y + 60, 160, t=t)
        line(c, 300, y - 40, 1700, y - 40, "#ffffff", 3, vis(t, B(2, 0.4)), dash=([14, 12], 0))
        circle(c, 1720, y - 40, 7, YEL, vis(t, B(2, 0.5))); circle(c, 1720, y - 40, 22, YEL, 0.4 * vis(t, B(2, 0.5)), stroke=3)
        T(c, "A COIN, 100 M AWAY", 1000, y + 50, 44, ts, "#ffffff", vis(t, B(2, 0.5)), maxw=900)
        C(c, "BY OUR ROUGH MATH", 1000, y + 160, vis(t, B(2, 0.6)), ts, size=26)
    def pD(c, ts):
        pRose(c, ts, B(3, 0), grid=True)
        C(c, "GENERAL RELATIVITY", 1550, 330, vis(t, B(3, 0.1)), ts, size=36, dot="#9fb8ff")
        C(c, "PREDICTS THE EXTRA SWING", 1550, 440, vis(t, B(3, 0.35)), ts, size=32)
        check(c, 1550, 580, 50, vis(t, B(3, 0.6)))
    run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB), (B(2, 0), pC), (B(3, 0), pD)])

# ------------------------------------------------------------------ me6_twist
def me6_twist(c, W, H, t, S):
    B = beats(S, 4)
    def system(c, ts, t0, lines_=True):
        sx, sy = 760, 560; k = 470
        glare_sun(c, sx, sy, 38, t, flare=0)
        pl = [(0.387, 87.97, SCORCH, 16), (0.723, 224.7, "#f0d08a", 22), (1.0, 365.25, "#6fb6ff", 22)]
        pos = []
        days = (t - t0) * 40 + 120
        for r, P, colr, pr in pl:
            c.drawCircle(sx, sy, r * k, paint(colr, 0.3, stroke=2, dash=([10, 10], 0)))
            an = 2 * math.pi * days / P + r * 5
            x, y = sx + math.cos(an) * r * k, sy - math.sin(an) * r * k
            pos.append((x, y)); circle(c, x, y, pr, colr)
        if lines_:
            (mx, my), (vx, vy), (ex, ey) = pos
            line(c, ex, ey, vx, vy, "#f0d08a", 4, 0.8); line(c, ex, ey, mx, my, SCORCH, 4, 0.8)
            dv = math.hypot(ex - vx, ey - vy) / k; dm = math.hypot(ex - mx, ey - my) / k
            T(c, f"VENUS: {dv:.2f} AU", 1550, 520, 44, ts, "#f0d08a", vis(t, t0 + 0.3), maxw=640)
            T(c, f"MERCURY: {dm:.2f} AU", 1550, 620, 44, ts, SCORCH, vis(t, t0 + 0.5), maxw=640)
        return pos
    def pA(c, ts):
        system(c, ts, 0.0, lines_=False)
        T(c, "HARDEST TO REACH…", 1500, 400, 64, ts, "#ffffff", vis(t, B(0, 0.15)), maxw=760)
        T(c, "…CLOSEST ON AVERAGE", 1500, 520, 64, ts, YEL, vis(t, B(0, 0.55)), maxw=760)
    def pB(c, ts):
        system(c, ts, B(1, 0))
        C(c, "VENUS: CLOSEST AT ITS NEAREST", 1550, 300, vis(t, B(1, 0.05)), ts, size=30, dot="#f0d08a")
        C(c, "…BUT OFTEN FAR SIDE OF THE SUN", 1550, 780, vis(t, B(1, 0.35)), ts, size=28, dot="#f0d08a")
        C(c, "MERCURY NEVER STRAYS FAR", 1550, 880, vis(t, B(1, 0.7)), ts, size=30, dot=SCORCH)
    def pC(c, ts):
        t0 = B(2, 0)
        C(c, "PHYSICS TODAY, 2019 · AVERAGE DISTANCE FROM EARTH", 960, 150, vis(t, t0 + 0.1), ts, size=30)
        bar(c, 520, 420, 1000, 70, 1.04 / 1.3 * ease(prog(t, B(2, 0.5), 0.8)), SCORCH, 1.0)
        bar(c, 520, 620, 1000, 70, 1.14 / 1.3 * ease(prog(t, B(2, 0.6), 0.8)), "#f0d08a", 1.0)
        T(c, "MERCURY", 490, 455, 46, ts, SCORCH, vis(t, B(2, 0.5)), align="r", maxw=420)
        T(c, "VENUS", 490, 655, 46, ts, "#f0d08a", vis(t, B(2, 0.6)), align="r", maxw=420)
        T(c, "1.04 AU", 520 + 800 + 50, 455, 46, ts, "#ffffff", vis(t, B(2, 0.75)), align="l", maxw=400)
        T(c, "1.14 AU", 520 + 877 + 50, 655, 46, ts, "#ffffff", vis(t, B(2, 0.8)), align="l", maxw=400)
        C(c, "CLOSEST TO EVERY PLANET, ON AVERAGE", 960, 860, vis(t, B(2, 0.35)), ts, size=32, bg=YEL, fg="#0b1030", a=1)
    def pD(c, ts):
        t0 = B(3, 0)
        mx, my, R = 760, 560, 270
        glare_sun(c, 120, 140, 60, t, flare_to=(mx, my))
        orx, ory = 470, 150
        th = (t - t0) * 0.4
        c.drawOval(skia.Rect.MakeLTRB(mx - orx, my - ory, mx + orx, my + ory), paint(SCORCH, 0.5, stroke=3, dash=([14, 10], -t * 10)))
        if math.sin(th) < 0: bepi(c, mx + orx * math.cos(th), my + ory * math.sin(th), 20)
        merc(c, mx, my, R, sun_ang=215)
        if math.sin(th) >= 0: bepi(c, mx + orx * math.cos(th), my + ory * math.sin(th), 20)
        C(c, "MORE THAN 8 YEARS TO GET THERE", 1500, 330, vis(t, t0 + 0.1), ts, size=30, dot=SCORCH)
        C(c, "SCIENCE FROM APRIL 2027", 1500, 450, vis(t, B(3, 0.45)), ts, size=36, bg=YEL, fg="#0b1030", a=1)
        C(c, "HOW DID MERCURY FORM?", 1500, 570, vis(t, B(3, 0.7)), ts, size=32, dot=GREEN)
    run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB), (B(2, 0), pC), (B(3, 0), pD)])

# =====================================================================  SHORT: one day = two years (twilight-violet/gold look)
def clock_dial(c, x, y, r, frac, label, colr, u=1.0, a=1.0):
    circle(c, x, y, r, "#1a0f2e", 0.92 * a); circle(c, x, y, r, colr, a, stroke=r * 0.06)
    for k in range(12):
        an = k * math.pi / 6
        line(c, x + math.cos(an) * r * 0.82, y + math.sin(an) * r * 0.82, x + math.cos(an) * r * 0.92, y + math.sin(an) * r * 0.92, colr, r * 0.03, a)
    p = skia.Path(); p.moveTo(x, y); p.arcTo(skia.Rect.MakeXYWH(x - r * 0.75, y - r * 0.75, r * 1.5, r * 1.5), -90, 360 * (frac % 1), False); p.close()
    c.drawPath(p, paint(colr, 0.35 * a))
    an = -math.pi / 2 + 2 * math.pi * frac
    line(c, x, y, x + math.cos(an) * r * 0.72, y + math.sin(an) * r * 0.72, "#ffffff", r * 0.05, a)
    text(c, label, x, y + r * 1.25, r * 0.28, colr, a, w=900)

def me6_mday(c, W, H, t, S):
    mode = S.opts.get("mode", "intro")
    L = S.le(0)
    def pIntro(c, ts):
        clock_dial(c, 600, 500, 290, t * 0.25, "1 DAY", GOLD)
        clock_dial(c, 1320, 500, 290, t * 0.5, "2 YEARS", VIO)
        T(c, "=", 960, 560, 160, ts, "#ffffff", 1, maxw=200)
    def pYear(c, ts):
        days = 88 * ease(prog(t, 0.2, max(0.5, L - 0.5)))
        orbit_view(c, t, days, 760, 560, 440, ts, pr=70, sun_r=70, show_marker=False, colr=GOLD, look="md")
        T(c, f"{int(days)}", 1520, 480, 180, ts, GOLD, 1, maxw=600)
        T(c, "EARTH DAYS", 1520, 640, 46, ts, "#ffffff", 1, maxw=600)
    def pSpin(c, ts):
        x, y, R = 640, 560, 260
        merc(c, x, y, R, sun_ang=180, night=0.0)
        th = t * 0.9
        line(c, x + math.cos(th) * R * 0.9, y - math.sin(th) * R * 0.9, x + math.cos(th) * R * 1.25, y - math.sin(th) * R * 1.25, GOLD, 10)
        circle(c, x + math.cos(th) * R * 1.3, y - math.sin(th) * R * 1.3, 18, GOLD)
        spins = int(clamp((t - 0.3) / max(0.5, L - 0.6)) * 3 + 1e-6); orbs = int(clamp((t - 0.3) / max(0.5, L - 0.6)) * 2 + 1e-6)
        for k in range(3): circle(c, 1260 + k * 170, 400, 64, GOLD, 1 if k < spins else 0.2)
        for k in range(2): circle(c, 1345 + k * 170, 700, 64, VIO, 1 if k < orbs else 0.2)
        T(c, "SPINS", 1430, 270, 40, ts, GOLD, 1, maxw=500); T(c, "ORBITS", 1430, 830, 40, ts, VIO, 1, maxw=500)
    def pDay(c, ts):
        days = days_map(t, [(0.2, 0), (S.le(0) - 0.2, 176)])
        orbit_view(c, t, days, 760, 560, 440, ts, pr=70, sun_r=70, colr=GOLD, look="md")
        T(c, f"DAY {int(days)}", 1520, 420, 90, ts, GOLD, 1, maxw=600)
        C(c, f"YEARS: {days / P_ORB:.1f}", 1520, 560, 1, ts, size=36, bg="#2a1640", dot=VIO)
    def pDouble(c, ts):
        stage_bg(c, "#0d0618", "#2a1230"); stars(c, VW, VH, t, 0.8, seed=79)
        sun_path(c, t, 0.3, 300, 1600, 800, 520, max(1.0, L - 0.4), ts, look="md", r=60)
        c.drawRect(skia.Rect.MakeLTRB(0, 800, VW, VH), paint(shader=lin(0, 800, 0, VH, [(0, "#3a2440", 1), (1, "#140a1c", 1)])))
        line(c, 0, 800, VW, 800, GOLD, 3, 0.6)
        C(c, "NOT TO SCALE", 1700, 980, 1, ts, size=22, bg="#2a1640")
    def pTemp(c, ts):
        f = ease(prog(t, 0.3, max(0.5, L * 0.7)))
        thermometer(c, 420, 470, 560, lerp(430, -180, f), tmax=450, tmin=-200, size=1.6)
        x0 = 900
        rrect(c, x0, 340, 900, 140, 40, GOLD, 1); T(c, "DAYS: MONTHS OF SUN", x0 + 450, 410, 34, ts, "#140a1c", 1, maxw=840, shadow=0)
        rrect(c, x0, 560, 900, 140, 40, "#2a3f9a", vis(t, L * 0.4)); T(c, "NIGHTS: MONTHS OF DARK", x0 + 450, 630, 34, ts, "#ffffff", vis(t, L * 0.4), maxw=840)
    fn = dict(intro=pIntro, year=pYear, spin=pSpin, day=pDay, double=pDouble, temp=pTemp)[mode]
    run_panels(c, W, H, t, S, [(0, fn)], look="md", seed=81)

# =====================================================================  SHORT: Voyager 1 (deep-space blue look)
def voyager(c, x, y, s, t, ang=0.0, a=1.0):
    """generic Voyager-style probe: big dish, bus, three booms."""
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(ang)
    line(c, 0, 0, -2.6 * s, 0.6 * s, "#c9ccd6", s * 0.035, a)  # magnetometer boom
    line(c, 0, 0.2 * s, 1.3 * s, 0.9 * s, "#c9ccd6", s * 0.05, a)  # RTG boom
    for k in range(3): rrect(c, 0.8 * s + k * 0.22 * s, 0.55 * s + k * 0.12 * s, 0.2 * s, 0.3 * s, 0.04 * s, "#6a6f7a", a)
    line(c, 0, 0.2 * s, -1.0 * s, 1.0 * s, "#c9ccd6", s * 0.05, a)  # science boom
    rrect(c, -1.25 * s, 0.9 * s, 0.4 * s, 0.25 * s, 0.04 * s, "#c9ccd6", a)
    c.drawPath(poly([(-0.35 * s, 0.1 * s), (0.35 * s, 0.1 * s), (0.42 * s, 0.4 * s), (-0.42 * s, 0.4 * s)]), paint("#8a8f9a", a))
    oval(c, 0, -0.1 * s, 0.75 * s, 0.22 * s, "#eef0f4", a)
    oval(c, 0, -0.14 * s, 0.6 * s, 0.14 * s, "#d0d4dc", a)
    line(c, 0, -0.1 * s, 0, -0.5 * s, "#c9ccd6", s * 0.03, a); circle(c, 0, -0.52 * s, 0.05 * s, "#eef0f4", a)
    circle(c, 0.2 * s, 0.28 * s, 0.08 * s, VGOLD, a)
    c.restore()

def phone(c, x, y, s, msg, t, sent=1.0, a=1.0):
    rrect(c, x - 0.55 * s, y - s, 1.1 * s, 2.0 * s, 0.15 * s, "#0d1426", a); rrect(c, x - 0.55 * s, y - s, 1.1 * s, 2.0 * s, 0.15 * s, "#9fb8ff", a, stroke=4)
    rrect(c, x - 0.48 * s, y - 0.88 * s, 0.96 * s, 1.76 * s, 0.1 * s, "#101c3a", a)
    text(c, "VOYAGER 1", x, y - 0.75 * s, 0.11 * s, "#cfe0ff", a, w=800)
    if sent > 0:
        bw = 0.88 * s
        rrect(c, x + 0.44 * s - bw, y - 0.34 * s, bw, 0.36 * s, 0.16 * s, SIG, a * sent)
        text(c, msg, x + 0.44 * s - bw / 2, y - 0.16 * s, fit(msg, bw * 0.84, 0.17 * s, 900), "#02101f", a * sent, w=900)

def earth_dot(c, x, y, r, a=1.0):
    circle(c, x, y, r * 2.5, "#6fb6ff", 0.18 * a); circle(c, x, y, r, "#6fb6ff", a); circle(c, x - r * 0.3, y - r * 0.2, r * 0.4, "#8fd99a", a)

def me6_voy(c, W, H, t, S):
    mode = S.opts.get("mode", "intro")
    L = S.le(0)
    def pIntro(c, ts):
        phone(c, 500, 540, 420, "HI VOYAGER!", t, sent=vis(t, 0.4))
        voyager(c, 1460, 500, 220, t, ang=-10)
        q = prog(t, 0.8, 1.2)
        if 0 < q < 1:
            x = lerp(700, 1300, q); circle(c, x, 500, 12, SIG); line(c, x - 80, 500, x, 500, SIG, 6, 0.6)
    def pFar(c, ts):
        earth_dot(c, 160, 560, 34)
        voyager(c, 1640, 500, 150, t, ang=-8)
        line(c, 200, 680, 1680, 680, "#ffffff", 3, 0.7, dash=([16, 12], 0))
        T(c, "≈ 25.9 BILLION KM", 940, 760, 64, ts, "#ffffff", vis(t, L * 0.45), maxw=1300)
        T(c, "18 NOV 2026 · 10:16 UTC", 940, 300, 52, ts, SIG, vis(t, 0.3), maxw=1500)
        C(c, "FIRST HUMAN-MADE OBJECT THIS FAR", 940, 420, vis(t, L * 0.25), ts, size=30, bg="#0d2350")
    def pText(c, ts):
        earth_dot(c, 160, 560, 34)
        voyager(c, 1640, 500, 150, t, ang=-8)
        t1 = L * 0.55
        q = clamp(t / t1) if t < t1 else 1
        x = lerp(220, 1640, q); circle(c, x, 560, 12, SIG); line(c, max(220, x - 140), 560, x, 560, SIG, 6, 0.7)
        if t > t1:
            q2 = clamp((t - t1) / (L - t1 + 0.3)); x2 = lerp(1640, 220, q2)
            circle(c, x2, 600, 12, VGOLD); line(c, x2, 600, min(1640, x2 + 140), 600, VGOLD, 6, 0.7)
        hrs = 24 * q + (24 * clamp((t - t1) / (L - t1 + 0.3)) if t > t1 else 0)
        T(c, f"{int(hrs):02d} H", 940, 300, 120, ts, SIG if t < t1 else VGOLD, 1, maxw=700)
        C(c, "SPEED OF LIGHT", 940, 820, vis(t, 0.3), ts, size=30, bg="#0d2350")
    def pSpeed(c, ts):
        rng = random.Random(3)
        for k in range(40):
            y = rng.uniform(150, 950); x = (rng.uniform(0, VW) - t * 600 * rng.uniform(0.5, 1.2)) % VW
            line(c, x, y, x + 80, y, "#cfe0ff", 2, 0.5)
        voyager(c, 1060, 480, 260, t, ang=-6 + 2 * math.sin(t))
        T(c, "≈ 17 KM EVERY SECOND", 960, 880, 64, ts, "#ffffff", vis(t, L * 0.45), maxw=1500)
        C(c, "LAUNCHED 5 SEP 1977", 960, 170, vis(t, 0.2), ts, size=34, bg="#0d2350", dot=VGOLD)
    def pPower(c, ts):
        voyager(c, 560, 520, 230, t, ang=-6)
        p = clamp(1 - 0.35 * ease(prog(t, 0.3, max(0.5, L - 0.5))))
        bar(c, 1060, 300, 700, 50, p, VGOLD, 1.0)
        T(c, "NUCLEAR POWER", 1060, 260, 34, ts, VGOLD, 1, align="l", maxw=700, w=800)
        for k, (lab, on) in enumerate((("MAGNETOMETER", True), ("PLASMA WAVE", True), ("OTHERS", False))):
            p2 = vis(t, L * (0.45 + 0.12 * k))
            C(c, ("ON: " if on else "OFF: ") + lab, 1400, 480 + k * 150, p2, ts, size=34, bg="#0d2350" if on else "#2a1020", dot=GREEN if on else RED)
    def pGlitch(c, ts):
        # Deep Space Network dish receiving a carrier but no data frames
        dx, dy = 360, 760
        line(c, dx, dy, dx, dy - 160, "#c9ccd6", 14)
        c.save(); c.translate(dx, dy - 200); c.rotate(-30)
        oval(c, 0, 0, 170, 60, "#eef0f4"); line(c, 0, 0, 0, -90, "#c9ccd6", 6); c.restore()
        p = skia.Path()
        for j in range(120):
            x = 600 + j * 10; y = 480 + 40 * math.sin(j * 0.35 - t * 8)
            p.moveTo(x, y) if j == 0 else p.lineTo(x, y)
        c.drawPath(p, paint(SIG, 0.9, stroke=5))
        T(c, "SIGNAL: YES", 1200, 330, 50, ts, SIG, vis(t, 0.3), maxw=900)
        T(c, "DATA: NO", 1200, 650, 50, ts, RED, vis(t, L * 0.3), maxw=900)
        C(c, "SINCE 14 NOV 2026", 1200, 760, vis(t, L * 0.3), ts, size=30, bg="#2a1020")
        C(c, "EACH TEST: 2-DAY WAIT", 1200, 880, vis(t, L * 0.7), ts, size=30, bg="#0d2350", dot=VGOLD)
    fn = dict(intro=pIntro, far=pFar, text=pText, speed=pSpeed, power=pPower, glitch=pGlitch)[mode]
    run_panels(c, W, H, t, S, [(0, fn)], look="vy", seed=83)

SCENES = {k: v for k, v in globals().items() if k.startswith("me6_") and callable(v)}
