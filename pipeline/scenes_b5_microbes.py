"""Batch 05 scenes: What If All the Bacteria in Your Body Vanished? (+ teaser and "You're about half bacteria" Shorts).

Look: "warm body, glowing swarm". Deep plum/aubergine backgrounds with soft magenta and teal bokeh, a coral-to-magenta
human silhouette, and lime + teal glowing microbes (cached glow sprites). Signature motifs: the body silhouette with its
swarm (and the swarm popping out of existence), a gut cross-section with fiber, bacteria and butyrate, and big counters.
Every scene draws on a virtual 1920x1080 stage (Stage). In Shorts the stage is scaled into the 0.255H..0.58H band and text
sizes are multiplied by ts=1.75. Multi-part scenes are drawn as time-ordered panels (run_panels).
"""
from common2 import *
import scenes_b3_kit as kit

BG_T, BG_B = "#12051a", "#2a0a2c"
CORAL, MAGENTA, PEACH = "#ff7a6b", "#e8457f", "#ffb199"
LIME, TEAL = "#b8ff3c", "#2ee6c8"
RED = "#ff4d5e"; PURP = "#9b5cff"; ICE = "#dff7ff"; GREY = "#8a7f93"
CHIPBG = "#3a1033"
PAL = dict(accent=LIME, chip="#4a1240", title2=ACCENT)
VW, VH = 1920, 1080

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

def C(c, s, x, y, p, ts, size=38, **kw):
    kw.setdefault("bg", CHIPBG)
    chip(c, s, x, y, p, size * ts, **kw)

def T(c, s, x, y, size, ts, colr="#ffffff", a=1.0, w=900, maxw=1800, **kw):
    if a <= 0: return
    fam = kw.pop("fam", "Inter Display")
    sz = fit(s, maxw, size * ts, w, fam)
    text(c, s, x, y, sz, colr, a, w=w, fam=fam, shadow=kw.pop("shadow", 10), **kw)

# ------------------------------------------------------------------ background
_BG = {}
def bg_img(W, H):
    k = (W, H)
    if k not in _BG:
        surf = skia.Surface(W, H); cc = surf.getCanvas()
        fill_bg(cc, W, H, BG_T, BG_B)
        M = max(W, H)
        cc.drawPaint(paint(shader=rad(W * 0.82, H * 0.18, M * 0.7, [(0, "#7a1650", 0.45), (1, "#000000", 0)])))
        cc.drawPaint(paint(shader=rad(W * 0.12, H * 0.9, M * 0.6, [(0, "#0d4a4a", 0.45), (1, "#000000", 0)])))
        rng = random.Random(5)
        for _ in range(26):  # out-of-focus microbe bokeh
            x, y, r = rng.random() * W, rng.random() * H, rng.uniform(10, 46) * M / 1920
            cc.drawCircle(x, y, r, paint(rng.choice([LIME, TEAL, MAGENTA, PEACH]), rng.uniform(0.04, 0.11), blur=r * 0.5))
        _BG[k] = surf.makeImageSnapshot()
    return _BG[k]

def bg_x(c, W, H, t, S):
    c.drawImage(bg_img(W, H), 0, 0)
    rng = random.Random(9); M = max(W, H)
    for i in range(12):  # slow drifting faint microbes
        x = (rng.random() * W + t * rng.uniform(4, 14) * M / 1920) % (W + 80) - 40
        y = rng.random() * H + math.sin(t * 0.4 + i) * 12
        bug(c, x, y, rng.uniform(7, 14) * M / 1920, rng.choice(["rod", "coc"]), rng.choice([LIME, TEAL]), rng.random() * 360 + t * 8, 0.18)

def run_panels(c, W, H, t, S, items):
    """items: [(t_on, fn(c, ts)), ...] in time order. Each later panel covers the previous one (own bg while fading in)."""
    bg_x(c, W, H, t, S)
    for i, (t0, fn) in enumerate(items):
        t1 = items[i + 1][0] if i + 1 < len(items) else None
        if t1 is not None and t >= t1 + 0.5: continue
        a = phase(t, t0 if i > 0 else None, t1)
        if a <= 0.003: continue
        with Layer(c, a) as on:
            if not on: continue
            if i > 0 and t < t0 + 0.55: bg_x(c, W, H, t, S)
            if S.P: c.clipRect(skia.Rect.MakeLTRB(0, 0.215 * H, W, 0.59 * H))
            with Stage(c, S) as ts:
                fn(c, ts)
    kit.hook(c, W, H, t, S)

def short1(S):
    """True for a Short scene with a single narration line (show only the essential panel)."""
    return S.P and S.n() <= 1

# ------------------------------------------------------------------ microbe sprites
_SPR = {}
def sprite(kind, colr):
    k = (kind, colr)
    if k not in _SPR:
        s = 40; N = 160
        surf = skia.Surface(N, N); cc = surf.getCanvas(); cc.clear(skia.ColorTRANSPARENT); cc.translate(N / 2, N / 2)
        cc.drawCircle(0, 0, s * 1.25, paint(colr, 0.33, blur=s * 0.45))
        dark = mix(colr, "#10301a", 0.55); light = mix(colr, "#ffffff", 0.55)
        if kind == "rod":
            for k2 in range(5):  # flagella
                p = skia.Path(); x0 = -s * 1.05; p.moveTo(x0, (k2 - 2) * s * 0.12)
                p.cubicTo(x0 - s * 0.3, (k2 - 2) * s * 0.3 - s * 0.2, x0 - s * 0.5, (k2 - 2) * s * 0.35 + s * 0.2, x0 - s * 0.75, (k2 - 2) * s * 0.4)
                cc.drawPath(p, paint(colr, 0.55, stroke=2.2))
            rrect(cc, -s * 1.1, -s * 0.45, s * 2.2, s * 0.9, s * 0.45, colr, 1)
            rrect(cc, -s * 0.9, -s * 0.3, s * 1.5, s * 0.22, s * 0.11, light, 0.6)
            rrect(cc, -s * 1.1, -s * 0.45, s * 2.2, s * 0.9, s * 0.45, dark, 0.8, stroke=3)
            circle(cc, s * 0.35, s * 0.08, s * 0.14, dark, 0.7)
        elif kind == "coc":
            for (dx, dy) in ((-0.42, -0.2), (0.42, -0.2), (0, 0.42)):
                circle(cc, dx * s, dy * s, s * 0.46, colr, 1)
                circle(cc, dx * s - s * 0.12, dy * s - s * 0.14, s * 0.14, light, 0.7)
                circle(cc, dx * s, dy * s, s * 0.46, dark, 0.8, stroke=3)
        else:  # spiral
            p = skia.Path(); p.moveTo(-s * 1.2, 0)
            for i in range(1, 25):
                x = -s * 1.2 + i * s * 0.1; p.lineTo(x, math.sin(i * 0.65) * s * 0.32)
            cc.drawPath(p, paint(colr, 1, stroke=s * 0.26)); cc.drawPath(p, paint(light, 0.5, stroke=s * 0.08))
        _SPR[k] = surf.makeImageSnapshot()
    return _SPR[k]

_SMP = skia.SamplingOptions(skia.FilterMode.kLinear)
def bug(c, x, y, s, kind="rod", colr=LIME, rot=0.0, a=1.0):
    """microbe of half-length ~s centred on (x, y)."""
    if a <= 0.01 or s <= 0.5: return
    img = sprite(kind, colr); k = s / 40
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(k, k)
    pt = skia.Paint(); pt.setAlphaf(clamp(a)); c.drawImage(img, -80, -80, _SMP, pt); c.restore()

def pop_ring(c, x, y, s, q, colr="#ffffff"):
    if 0 < q < 1: circle(c, x, y, s * (0.6 + 1.6 * eout(q)), colr, 0.8 * (1 - q), stroke=max(1.5, s * 0.15 * (1 - q)))

# ------------------------------------------------------------------ the body
_BODY = {}
def body_path(cx, top, h, arm_up=0.0):
    k = (round(cx), round(top), round(h), round(arm_up, 2))
    if k in _BODY: return _BODY[k]
    def rr(x, y, w, hh, r, ang=0.0, px=None, py=None):
        p = skia.Path(); p.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, hh), r, r))
        if ang: p.transform(skia.Matrix.RotateDeg(ang, skia.Point(px, py)))
        return p
    U = lambda a_, b_: skia.Op(a_, b_, skia.PathOp.kUnion_PathOp)
    p = skia.Path(); p.addCircle(cx, top + 0.068 * h, 0.066 * h)
    p = U(p, rr(cx - 0.032 * h, top + 0.11 * h, 0.064 * h, 0.06 * h, 0.01 * h))
    p = U(p, rr(cx - 0.125 * h, top + 0.155 * h, 0.25 * h, 0.33 * h, 0.07 * h))
    p = U(p, rr(cx - 0.115 * h, top + 0.42 * h, 0.23 * h, 0.13 * h, 0.05 * h))
    for sg in (-1, 1):
        sx, sy = cx + sg * 0.112 * h, top + 0.185 * h
        ang = -sg * 13 if not (sg < 0 and arm_up > 0) else lerp(13, 165, arm_up)
        p = U(p, rr(sx - 0.03 * h, sy - 0.02 * h, 0.06 * h, 0.39 * h, 0.03 * h, ang, sx, sy))
        lx = cx + sg * 0.06 * h
        p = U(p, rr(lx - 0.05 * h, top + 0.5 * h, 0.1 * h, 0.48 * h, 0.045 * h, -sg * 2.5, lx, top + 0.5 * h))
    _BODY[k] = p
    return p

def colon_path(cx, top, h):
    p = skia.Path()
    p.moveTo(cx - 0.075 * h, top + 0.545 * h); p.lineTo(cx - 0.08 * h, top + 0.405 * h)
    p.quadTo(cx - 0.08 * h, top + 0.37 * h, cx - 0.045 * h, top + 0.375 * h)
    p.cubicTo(cx - 0.01 * h, top + 0.39 * h, cx + 0.01 * h, top + 0.36 * h, cx + 0.05 * h, top + 0.375 * h)
    p.quadTo(cx + 0.08 * h, top + 0.38 * h, cx + 0.08 * h, top + 0.41 * h)
    p.lineTo(cx + 0.078 * h, top + 0.52 * h); p.quadTo(cx + 0.07 * h, top + 0.57 * h, cx + 0.01 * h, top + 0.565 * h)
    return p

def body(c, cx, top, h, a=1.0, arm_up=0.0, colon=0.0, glow=1.0, grey=0.0):
    if a <= 0: return
    p = body_path(cx, top, h, arm_up)
    c1, c2 = mix(PEACH, GREY, grey), mix(MAGENTA, "#4a3a55", grey)
    if glow: c.drawPath(p, paint(mix(MAGENTA, GREY, grey), 0.45 * a * glow, blur=h * 0.03))
    c.drawPath(p, paint(shader=lin(cx, top, cx, top + h, [(0, c1, 1), (0.55, mix(c1, c2, 0.6), 1), (1, c2, 1)]), a=a))
    c.save(); c.clipPath(p, doAntiAlias=True)
    c.drawPaint(paint(shader=rad(cx - 0.08 * h, top + 0.25 * h, h * 0.55, [(0, "#ffffff", 0.22), (1, "#000000", 0.0)]), a=a))
    c.restore()
    c.drawPath(p, paint("#ffe1d6", 0.5 * a, stroke=max(2, h * 0.004)))
    if colon > 0:
        cp = colon_path(cx, top, h)
        c.drawPath(cp, paint("#ff3d8b", 0.5 * a * colon, stroke=h * 0.05, blur=h * 0.01))
        c.drawPath(cp, paint("#c2185b", a * colon, stroke=h * 0.036))
        c.drawPath(cp, paint("#ff8fb8", 0.6 * a * colon, stroke=h * 0.012, dash=([h * 0.012, h * 0.018], 0)))

_SW = {}
def swarm_pts(cx, top, h, n=220, seed=3, arm_up=0.0):
    k = (round(cx), round(top), round(h), n, seed, round(arm_up, 2))
    if k in _SW: return _SW[k]
    rng = random.Random(seed); p = body_path(cx, top, h, arm_up); cp = colon_path(cx, top, h)
    meas = skia.PathMeasure(cp, False); L = meas.getLength(); pts = []
    while len(pts) < n:
        r = rng.random()
        if r < 0.62:  # colon
            pos, _ = meas.getPosTan(rng.random() * L)
            x, y = pos.x() + rng.gauss(0, 0.012 * h), pos.y() + rng.gauss(0, 0.012 * h)
            sz = rng.uniform(0.007, 0.012) * h
        elif r < 0.66:  # mouth
            x, y = cx + rng.gauss(0, 0.012 * h), top + 0.09 * h + rng.gauss(0, 0.006 * h); sz = 0.006 * h
        else:  # skin
            x, y = cx + rng.uniform(-0.3, 0.3) * h, top + rng.uniform(0, 1) * h
            if not p.contains(x, y): continue
            sz = rng.uniform(0.005, 0.009) * h
        kind = rng.choice(["rod", "rod", "coc", "coc", "spi"])
        pts.append((x, y, sz, kind, rng.choice([LIME, LIME, TEAL]), rng.random() * 360, rng.random() * 6.28, rng.random()))
    _SW[k] = pts
    return pts

def swarm(c, t, cx, top, h, a=1.0, n=220, vanish_t=None, grow=1.0, seed=3, arm_up=0.0, recolor=None):
    """glowing microbes in and on the body. vanish_t: they pop out over 0.7 s from then. grow: fraction visible (0..1)."""
    for (x, y, sz, kind, colr, rot, ph, d) in swarm_pts(cx, top, h, n, seed, arm_up):
        if d > grow: continue
        aa = a * clamp((grow - d) * 12) if grow < 1 else a
        if vanish_t is not None:
            q = prog(t, vanish_t + d * 0.7, 0.18)
            if q >= 1:
                continue
            if q > 0:
                pop_ring(c, x, y, sz * 1.8, q, ICE); aa *= 1 - q; sz *= 1 + 0.4 * q
        bug(c, x + math.sin(t * 1.7 + ph) * sz * 0.3, y + math.cos(t * 1.3 + ph) * sz * 0.3, sz, kind, recolor or colr, rot + 15 * math.sin(t + ph), aa)

# ------------------------------------------------------------------ icons
def apple_x(c, x, y, s, a=1.0): apple(c, x, y, s, a)

def soda_can(c, x, y, s, a=1.0):
    rrect(c, x - s * 0.36, y - s * 0.62, s * 0.72, s * 1.24, s * 0.12, "#d8dde6", a)
    rrect(c, x - s * 0.36, y - s * 0.4, s * 0.72, s * 0.8, s * 0.04, MAGENTA, a)
    rrect(c, x - s * 0.36, y - s * 0.4, s * 0.72, s * 0.12, s * 0.02, "#ffffff", 0.5 * a)
    oval(c, x, y - s * 0.62, s * 0.36, s * 0.07, "#aab2c0", a)

def toilet(c, x, y, s, a=1.0):
    rrect(c, x - s * 0.55, y - s * 1.0, s * 0.5, s * 0.75, s * 0.08, "#f1f4fa", a)
    oval(c, x + s * 0.15, y - s * 0.28, s * 0.62, s * 0.18, "#f1f4fa", a)
    p = skia.Path(); p.moveTo(x - s * 0.45, y - s * 0.28); p.quadTo(x + s * 0.15, y + s * 0.35, x + s * 0.7, y - s * 0.28); p.close()
    c.drawPath(p, paint("#f1f4fa", a))
    rrect(c, x - s * 0.05, y - s * 0.05, s * 0.32, s * 0.45, s * 0.05, "#dfe5ee", a)
    oval(c, x + s * 0.15, y - s * 0.3, s * 0.45, s * 0.1, "#9fb3c8", a)

def book(c, x, y, w, h, a=1.0, colr="#4a2a6a"):
    rrect(c, x - w / 2 - 10, y - h / 2 - 8, w + 20, h + 16, 14, mix(colr, "#000000", 0.3), a)
    rrect(c, x - w / 2, y - h / 2, w, h, 10, "#f6efe2", a)
    line(c, x, y - h / 2, x, y + h / 2, "#cdbfa8", 4, a)
    for k in range(5):
        yy = y - h / 2 + 40 + k * (h - 80) / 5
        line(c, x - w / 2 + 30, yy, x - 30, yy, "#d9ccb6", 6, a); line(c, x + 30, yy, x + w / 2 - 30, yy, "#d9ccb6", 6, a)

def human_cell(c, x, y, s, a=1.0, colr=CORAL):
    circle(c, x, y, s, colr, 0.85 * a); circle(c, x, y, s, mix(colr, "#ffffff", 0.4), a, stroke=max(1.5, s * 0.08))
    circle(c, x + s * 0.12, y - s * 0.05, s * 0.38, mix(colr, "#5a1030", 0.5), a)

def rbc(c, x, y, s, a=1.0):
    oval(c, x, y, s, s * 0.82, "#e0303f", a); oval(c, x, y, s * 0.5, s * 0.38, "#a61b2a", a * 0.8)

def capsule(c, x, y, s, label, a=1.0, ang=0, c1=ACCENT, c2="#ffffff"):
    c.save(); c.translate(x, y); c.rotate(ang)
    rrect(c, -s, -s * 0.45, s, s * 0.9, s * 0.45, c1, a); rrect(c, 0, -s * 0.45, s, s * 0.9, s * 0.45, c2, a)
    rrect(c, -s, -s * 0.45, s * 2, s * 0.9, s * 0.45, "#000000", 0.3 * a, stroke=max(1.5, s * 0.06))
    c.restore()
    if label: text(c, label, x, y, s * 0.6, "#2a0a2c", a, w=900)

def mouse(c, x, y, s, a=1.0, colr="#d9c3cf", face=1, tail=True, rat=False):
    """side view mouse standing on (x, y); s = body half-length."""
    f = face
    if tail:
        p = skia.Path(); p.moveTo(x - f * s * 0.9, y - s * 0.25)
        L = 1.9 if rat else 1.4
        p.cubicTo(x - f * s * 1.5, y - s * 0.1, x - f * s * 1.6, y - s * 0.7, x - f * s * L * 1.25, y - s * 0.55)
        c.drawPath(p, paint(mix(colr, "#ff9fb3", 0.4), a, stroke=s * 0.07))
    oval(c, x, y - s * 0.45, s, s * 0.48, colr, a)
    oval(c, x + f * s * 0.95, y - s * 0.55, s * 0.48, s * 0.32, colr, a)
    c.drawPath(poly([(x + f * s * 1.25, y - s * 0.68), (x + f * s * 1.6, y - s * 0.5), (x + f * s * 1.25, y - s * 0.4)]), paint(colr, a))
    circle(c, x + f * s * 1.58, y - s * 0.52, s * 0.07, "#ff8fa8", a)
    circle(c, x + f * s * 0.75, y - s * 0.92, s * 0.24, colr, a); circle(c, x + f * s * 0.75, y - s * 0.92, s * 0.14, "#ffb3c6", a)
    circle(c, x + f * s * 1.12, y - s * 0.63, s * 0.06, "#1a0a1e", a)
    for dx in (-0.55, -0.25, 0.35, 0.6):
        line(c, x + f * dx * s, y - s * 0.1, x + f * dx * s, y, mix(colr, "#ff9fb3", 0.4), s * 0.09, a)

def guinea_pig(c, x, y, s, a=1.0):
    mouse(c, x, y, s, a, colr="#e0a96d", tail=False)
    oval(c, x - s * 0.3, y - s * 0.55, s * 0.4, s * 0.3, "#fff2df", a * 0.9)

def beagle(c, x, y, s, a=1.0):
    col_ = "#c98a4b"
    rrect(c, x - s, y - s * 0.95, s * 1.7, s * 0.6, s * 0.3, col_, a)
    for dx in (-0.85, -0.55, 0.3, 0.55): rrect(c, x + dx * s, y - s * 0.5, s * 0.17, s * 0.5, s * 0.06, col_, a)
    oval(c, x + s * 0.95, y - s * 1.15, s * 0.36, s * 0.3, col_, a)
    rrect(c, x + s * 1.05, y - s * 1.12, s * 0.45, s * 0.25, s * 0.1, "#f3e3c8", a)
    circle(c, x + s * 1.48, y - s * 1.05, s * 0.06, "#1a0a1e", a)
    oval(c, x + s * 0.78, y - s * 0.98, s * 0.13, s * 0.3, "#6b3d1e", a)
    rrect(c, x - s * 0.55, y - s * 0.95, s * 0.6, s * 0.35, s * 0.15, "#2a1a10", a * 0.85)
    p = skia.Path(); p.moveTo(x - s * 0.95, y - s * 0.85); p.quadTo(x - s * 1.25, y - s * 1.2, x - s * 1.15, y - s * 1.45)
    c.drawPath(p, paint(col_, a, stroke=s * 0.12)); circle(c, x - s * 1.15, y - s * 1.45, s * 0.07, "#ffffff", a)
    circle(c, x + s * 1.1, y - s * 1.2, s * 0.05, "#1a0a1e", a)

def flask(c, x, y, s, a=1.0, colr=TEAL):
    p = poly([(x - s * 0.18, y - s), (x + s * 0.18, y - s), (x + s * 0.18, y - s * 0.45), (x + s * 0.65, y + s * 0.6),
              (x - s * 0.65, y + s * 0.6), (x - s * 0.18, y - s * 0.45)])
    c.save(); c.clipPath(p, doAntiAlias=True); rect(c, x - s, y, s * 2, s, colr, 0.8 * a); c.restore()
    c.drawPath(p, paint("#ffffff", a, stroke=s * 0.08))

def gear(c, x, y, r, rot, a=1.0, colr="#ffffff"):
    c.save(); c.translate(x, y); c.rotate(rot)
    for k in range(8):
        c.rotate(45); rrect(c, -r * 0.16, -r * 1.18, r * 0.32, r * 0.4, r * 0.06, colr, a)
    circle(c, 0, 0, r, colr, a); circle(c, 0, 0, r * 0.38, "#2a0a2c", a); c.restore()

def plate(c, x, y, s, a=1.0):
    oval(c, x, y + s * 0.1, s * 1.15, s * 0.36, "#000000", 0.3 * a, blur=s * 0.08)
    oval(c, x, y, s * 1.1, s * 0.34, "#f4f1ec", a); oval(c, x, y, s * 0.75, s * 0.22, "#e3ddd3", a)
    rng = random.Random(4)
    for k in range(9):
        cx_ = x + rng.uniform(-0.5, 0.5) * s; cy_ = y - s * 0.05 + rng.uniform(-0.1, 0.06) * s
        circle(c, cx_, cy_ - s * 0.06, s * rng.uniform(0.1, 0.17), rng.choice(["#4caf50", "#8bc34a", "#e53935", "#ffb74d", "#f6e7c1"]), a)

def house_icon(c, x, y, s, a=1.0, door=1.0):
    rect(c, x - s * 0.6, y - s * 0.75, s * 1.2, s * 0.75, "#3d1640", a)
    rect(c, x - s * 0.6, y - s * 0.75, s * 1.2, s * 0.75, PEACH, a, stroke=5)
    c.drawPath(poly([(x - s * 0.78, y - s * 0.72), (x, y - s * 1.3), (x + s * 0.78, y - s * 0.72)]), paint(PEACH, a, stroke=6))
    rect(c, x - s * 0.16, y - s * 0.48, s * 0.32, s * 0.48, "#0e0410", a)
    dw = s * 0.32 * (1 - 0.8 * door)
    rect(c, x - s * 0.16, y - s * 0.48, dw, s * 0.48, MAGENTA, a)
    for wx in (-0.42, 0.28): rect(c, x + wx * s, y - s * 0.6, s * 0.16, s * 0.16, "#0e0410", a)

def isolator(c, x, y, w, h, a=1.0, colr=TEAL, gloves=True, steel=False):
    """lab isolator box (flexible film, or steel tank) with glove ports; (x, y) = bottom centre."""
    if steel:
        rrect(c, x - w / 2, y - h, w, h, h * 0.5, "#8d97a6", a)
        rrect(c, x - w / 2, y - h, w, h, h * 0.5, "#dfe6ef", a, stroke=6)
        for k in range(3): circle(c, x - w * 0.3 + k * w * 0.3, y - h * 0.55, h * 0.18, "#1b2433", a)
    else:
        rrect(c, x - w / 2, y - h, w, h, 40, colr, 0.13 * a)
        rrect(c, x - w / 2, y - h, w, h, 40, colr, 0.8 * a, stroke=5)
        line(c, x - w / 2 + 40, y - h + 30, x - w / 2 + 120, y - h + 30, "#ffffff", 6, 0.4 * a)
    if gloves:
        for gx in (-0.22, 0.22):
            circle(c, x + gx * w, y - h * 0.35, h * 0.12, "#0e2a2a" if not steel else "#2b3442", a)
            circle(c, x + gx * w, y - h * 0.35, h * 0.12, "#ffffff", 0.6 * a, stroke=4)
    rect(c, x - w / 2 - 20, y, w + 40, 16, "#3a2a44", a)

def stink(c, x, y, t, a=1.0, s=1.0, colr="#c8e86a"):
    for k in range(3):
        p = skia.Path(); x0 = x + (k - 1) * 40 * s
        for i in range(14):
            yy = y - i * 14 * s; xx = x0 + math.sin(i * 0.7 - t * 4 + k) * 14 * s
            if i == 0: p.moveTo(xx, yy)
            else: p.lineTo(xx, yy)
        c.drawPath(p, paint(colr, a * 0.85, stroke=7 * s))

def yab(c, x, y, s, a=1.0, colr=ICE, rot=0):
    """Y-shaped antibody."""
    c.save(); c.translate(x, y); c.rotate(rot)
    line(c, 0, 0, 0, s, colr, s * 0.22, a); line(c, 0, 0, -s * 0.6, -s * 0.7, colr, s * 0.22, a); line(c, 0, 0, s * 0.6, -s * 0.7, colr, s * 0.22, a)
    c.restore()

def immune_cell(c, x, y, s, a=1.0, t=0.0):
    circle(c, x, y, s * 1.4, "#7fd4ff", 0.25 * a, blur=s * 0.4)
    circle(c, x, y, s, "#cdeeff", 0.9 * a); circle(c, x + s * 0.15, y - s * 0.1, s * 0.5, "#5a8fd6", a)
    for k in range(7):
        an = k / 7 * 6.28 + t * 0.6
        circle(c, x + math.cos(an) * s, y + math.sin(an) * s, s * 0.15, "#cdeeff", 0.9 * a)

def pathogen(c, x, y, s, a=1.0, rot=0, t=0.0):
    bug(c, x, y, s, "rod", PURP, rot, a)
    for k in range(6):
        an = k / 6 * 6.28 + t
        circle(c, x + math.cos(an) * s * 1.05, y + math.sin(an) * s * 0.5, s * 0.08, "#e3c6ff", 0.8 * a)

def scale_bar(c, x, y, w, frac, colr, label, val, ts, a=1.0, h=70):
    rrect(c, x, y - h / 2, w, h, h / 2, "#ffffff", 0.1 * a)
    if frac > 0: rrect(c, x, y - h / 2, max(h, w * clamp(frac)), h, h / 2, colr, a)
    T(c, label, x, y - h * 1.15, 34, ts, "#ffffff", a, w=700, maxw=w, fam="Inter", align="l", shadow=6)
    T(c, val, x + w * clamp(frac) - 24, y, 44, ts, "#2a0a2c", a, w=900, maxw=w * 0.6, align="r", shadow=0)

def fmt_count(v):
    return f"{int(v):,}"

# ------------------------------------------------------------------ gut cross-section
def gut(c, t, x0, x1, ya, yb, a=1.0, bugs=1.0, energy=1.0, fiber=1.0, flow=1.0, scfa=1.0, seed=1, gas=0.0, vanish_t=None, cells_grey=0.0):
    """horizontal slice of colon: walls of lining cells top and bottom, lumen in between."""
    if a <= 0: return
    wall = 120
    rect(c, x0, ya - wall, x1 - x0, yb - ya + 2 * wall, "#3a0f2e", a)
    # lumen
    c.drawRect(skia.Rect.MakeLTRB(x0, ya, x1, yb), paint(shader=lin(0, ya, 0, yb, [(0, "#4a1238", 1), (0.5, "#2e0a26", 1), (1, "#4a1238", 1)]), a=a))
    # mucus layer
    for yy, sg in ((ya, 1), (yb, -1)):
        c.drawRect(skia.Rect.MakeLTRB(x0, min(yy, yy + sg * 34), x1, max(yy, yy + sg * 34)), paint("#ffc2d9", 0.12 * a))
    # lining cells (columnar), glowing with energy
    cw = 46
    n = int((x1 - x0) / cw) + 1
    for side, (yw, sg) in enumerate(((ya, -1), (yb, 1))):
        for i in range(n):
            x = x0 + i * cw
            crypt = (i % 7 == 3)
            hh = wall * (1.0 if not crypt else 0.55)
            y_in = yw if sg > 0 else yw - hh
            e = energy * (0.75 + 0.25 * math.sin(t * 2 + i * 0.7 + side))
            colr = mix(mix("#7a2f55", CORAL, e), "#5a5060", cells_grey)
            rrect(c, x + 3, y_in, cw - 6, hh, 14, colr, a)
            if e > 0.05: rrect(c, x + 3, y_in, cw - 6, hh, 14, ACCENT, a * 0.35 * e, stroke=3)
            ny = yw + sg * hh * 0.62
            circle(c, x + cw / 2, ny, 9, mix("#4a1238", "#2a2030", cells_grey), a)
    # fiber strands
    if fiber > 0:
        rng = random.Random(seed)
        for k in range(9):
            sp = rng.uniform(60, 110) * flow; ph = rng.random()
            L = rng.uniform(140, 240); yy = rng.uniform(ya + 60, yb - 60)
            xx = x0 - 260 + ((ph * (x1 - x0 + 520) + t * sp) % (x1 - x0 + 520))
            p = skia.Path(); p.moveTo(xx, yy)
            for i in range(1, 9):
                p.lineTo(xx + L * i / 8, yy + math.sin(i * 1.2 + k + t) * 12)
            c.drawPath(p, paint("#f0d9a0", a * fiber * 0.9, stroke=9))
            c.drawPath(p, paint("#b48a4a", a * fiber * 0.6, stroke=3))
    # bacteria in lumen
    if bugs > 0:
        rng = random.Random(seed + 4)
        for k in range(26):
            bx = rng.uniform(x0 + 30, x1 - 30); by = rng.uniform(ya + 50, yb - 50); ph = rng.random() * 6.28
            sz = rng.uniform(16, 26); d = rng.random()
            aa = a * bugs
            if vanish_t is not None:
                q = prog(t, vanish_t + d * 0.6, 0.18)
                if q >= 1: continue
                if q > 0: pop_ring(c, bx, by, sz * 1.5, q, ICE); aa *= 1 - q
            bug(c, bx + math.sin(t * 1.5 + ph) * 10, by + math.cos(t * 1.1 + ph) * 8, sz, rng.choice(["rod", "coc", "rod"]), rng.choice([LIME, TEAL]), rng.random() * 360 + t * 20, aa)
    # SCFA molecules drifting to the walls
    if scfa > 0:
        rng = random.Random(seed + 9)
        for k in range(22):
            ph = rng.random(); x = rng.uniform(x0 + 20, x1 - 20); up = rng.random() < 0.5
            q = (ph + t * 0.35) % 1
            y = lerp((ya + yb) / 2 + rng.uniform(-60, 60), ya + 10 if up else yb - 10, q)
            hexa(c, x, y, 9, TEAL, a * scfa * (1 - q * 0.6))
    if gas > 0:
        rng = random.Random(seed + 13)
        for k in range(10):
            ph = rng.random(); q = (ph + t * 0.25) % 1; x = rng.uniform(x0 + 40, x1 - 40) + math.sin(t + k) * 10
            y = lerp(yb - 40, ya + 40, q)
            circle(c, x, y, rng.uniform(10, 22), "#ffffff", a * gas * 0.6 * (1 - q), stroke=3)

def hexa(c, x, y, r, colr, a=1.0):
    if a <= 0.01: return
    pts = [(x + math.cos(k * math.pi / 3) * r, y + math.sin(k * math.pi / 3) * r) for k in range(6)]
    c.drawPath(poly(pts), paint(colr, a)); circle(c, x, y, r * 2, colr, a * 0.25, blur=r)

def battery(c, x, y, s, lvl, a=1.0):
    rrect(c, x - s, y - s * 0.5, s * 2, s, s * 0.15, "#ffffff", a, stroke=s * 0.1)
    rect(c, x + s, y - s * 0.2, s * 0.18, s * 0.4, "#ffffff", a)
    colr = mix(RED, LIME, lvl)
    rrect(c, x - s * 0.85, y - s * 0.35, max(s * 0.12, s * 1.7 * clamp(lvl)), s * 0.7, s * 0.08, colr, a)

# ------------------------------------------------------------------ kit wrappers
def motif_x(c, W, H, t, S, cx, cy, s):
    u = S.u; h = 520 * s * u * (1.15 if S.P else 1)
    top = cy - h / 2
    c.save(); c.translate(cx, top); c.scale(h / 900, h / 900); c.translate(-450, 0)
    body(c, 450, 0, 900, 1.0, colon=1.0)
    swarm(c, t, 450, 0, 900, 1.0, n=170)
    c.restore()

def x5_title(c, W, H, t, S): kit.title(c, W, H, t, S, bg_x, motif_x, PAL)
def x5_card(c, W, H, t, S):
    def cbg(c, W, H, t, S):
        bg_x(c, W, H, t, S)
        with Layer(c, 0.3):
            motif_x(c, W, H, t, S, W / 2, H / 2, 1.6 if not S.P else 1.1)
    kit.card(c, W, H, t, S, cbg, PAL)
def x5_end(c, W, H, t, S): kit.end(c, W, H, t, S, bg_x, motif_x, PAL)
def x5_endshort(c, W, H, t, S): kit.end_short(c, W, H, t, S, bg_x, motif_x, PAL)

# ------------------------------------------------------------------ x5_body
BX, BT, BH = 560, 110, 880   # standard body placement on the stage

def x5_body(c, W, H, t, S):
    o = S.opts; mode = o.get("mode", "intro")
    if mode == "intro":
        B = beats(S, 3)
        def pA(c, ts):
            g = eout(prog(t, 0.1, B(0, 0.85) - 0.1 if S.n() >= 3 else 1.6))
            body(c, BX, BT, BH, colon=0.8); swarm(c, t, BX, BT, BH, grow=g)
            v = 38e12 * eout(prog(t, B(0, 0.1), B(0, 0.75) - B(0, 0.1) + 0.01))
            C(c, "BACTERIA IN AND ON YOU", 1380, 300, vis(t, 0.2), ts, dot=LIME)
            T(c, fmt_count(v), 1380, 470, 110, ts, LIME, prog(t, 0.2, 0.3), maxw=900 if not S.P else 780, shadow=20)
            C(c, "≈ 38 TRILLION", 1380, 640, vis(t, B(0, 0.75)), ts, size=40, bg=LIME, fg="#2a0a2c", a=1)
        items = [(0, pA)]
        if not short1(S):
            def pB(c, ts):
                body(c, BX, BT, BH, colon=0.8); swarm(c, t, BX, BT, BH)
                scale_bar(c, 1000, 330, 760, eout(prog(t, B(1, 0.0), 0.8)), LIME, "BACTERIA", "38 T", ts)
                scale_bar(c, 1000, 520, 760, eout(prog(t, B(1, 0.15), 0.8)) * 30 / 38, CORAL, "YOUR OWN CELLS", "30 T", ts)
                pa = prog(t, B(1, 0.55), 0.5)
                apple(c, 1150, 760, 70 * eback(pa), clamp(pa))
                T(c, "≈ 200 g", 1440, 760, 90, ts, "#ffffff", pa, maxw=520)
            def pC(c, ts):
                fl = 0.55 + 0.45 * math.sin(t * 9) ** 2
                body(c, BX, BT, BH, colon=0.8); swarm(c, t, BX, BT, BH, a=fl)
                T(c, "?", 1380, 480, 380, ts, LIME, prog(t, B(2, 0.2), 0.5), shadow=30)
                C(c, "WHAT IF THEY ALL VANISHED?", 1380, 800, vis(t, B(2, 0.3)), ts, size=38)
            items += [(B(1, 0), pB), (B(2, 0), pC)]
        run_panels(c, W, H, t, S, items)
    elif mode == "vanish":
        B = beats(S, 3); tv = B(0, 0.25) if not S.P else S.lt(0, 0.1)
        def pA(c, ts):
            body(c, BX, BT, BH, colon=0.8); swarm(c, t, BX, BT, BH, vanish_t=tv)
            clock(c, 1380, 330, 120, 1.0, colr=MAGENTA)
            C(c, "00:00 · MIDNIGHT", 1380, 520, vis(t, 0.2), ts, dot=LIME)
            if S.P:
                T(c, "−38 TRILLION", 1380, 720, 90, ts, LIME, prog(t, tv + 0.8, 0.4), maxw=820)
            else:
                C(c, "YOU FEEL… NOTHING", 1380, 660, vis(t, tv + 1.2), ts, size=40)
        items = [(0, pA)]
        if not short1(S):
            def pB(c, ts):
                body(c, BX, BT, BH, colon=0.35 + 0.25 * math.sin(t * 3) ** 2)
                T(c, "−200 g", 1380, 420, 190, ts, LIME, prog(t, B(1, 0.05), 0.5), shadow=24, maxw=900)
                C(c, "ALMOST ALL OF IT FROM YOUR COLON", 1380, 640, vis(t, B(1, 0.45)), ts, size=36, dot=MAGENTA)
            def pC(c, ts):
                x0, x1, y = 460, 1460, 560
                c.drawRect(skia.Rect.MakeLTRB(x0, 0, x1, 1080), paint(shader=lin(x0, 0, x1, 0, [(0, "#3a2414", 1), (0.35, "#8a5e36", 1), (0.6, "#6e4a2a", 1), (1, "#2e1c10", 1)])))
                for k in range(9): line(c, x0 + 40 + k * 110, 0, x0 + 60 + k * 110, 1080, "#a07850", 3, 0.35)
                n_on = int(100 * eout(prog(t, B(2, 0.25), 1.6)))
                for k in range(n_on):
                    circle(c, x0 + 10 * k + 5, y, 4.6, LIME if k % 2 else TEAL, 1)
                arrow(c, x0 + 40, 760, x0, 760, "#ffffff", 5, vis(t, B(2, 0.1))); arrow(c, x1 - 40, 760, x1, 760, "#ffffff", 5, vis(t, B(2, 0.1)))
                C(c, "WIDTH OF ONE HUMAN HAIR", 960, 760, vis(t, B(2, 0.1)), ts, size=34)
                pm = vis(t, B(2, 0.5)); mx, my = 1640, 300
                if pm > 0:
                    line(c, 960, y, mx - 120, my + 90, "#ffffff", 4, pm)
                    circle(c, mx, my, 170, "#1a0820", 0.95 * pm); circle(c, mx, my, 170, "#ffffff", pm, stroke=8)
                    for k in range(5): bug(c, mx - 120 + k * 60, my, 26, "coc" if k % 2 else "rod", LIME if k % 2 else TEAL, 0, pm)
                C(c, "≈ 100 BACTERIA ACROSS", 960, 160, vis(t, B(2, 0.35)), ts, size=40, bg=LIME, fg="#2a0a2c", a=1)
                C(c, "1 BACTERIUM ≈ 1 µm", 1640, 540, vis(t, B(2, 0.6)), ts, size=32)
            items += [(B(1, 0), pB), (B(2, 0), pC)]
        run_panels(c, W, H, t, S, items)
    else:  # odor
        B = beats(S, 2); tv = B(1, 0.55)
        h2 = 1500; cx2 = 700; top2 = 90
        def pA(c, ts):
            up = eout(prog(t, 0.0, 0.8))
            body(c, cx2, top2, h2, arm_up=up)
            swarm(c, t, cx2, top2, h2, n=160, seed=6, arm_up=1.0, a=up)
            ax, ay = cx2 - 0.12 * h2, top2 + 0.2 * h2
            stink(c, ax + 20, ay - 10, t, a=eout(prog(t, B(0, 0.3), 0.8)) * (1 - prog(t, tv, 0.8)), s=1.2)
            for k in range(4):
                q = (t * 0.6 + k * 0.25) % 1
                circle(c, ax + 30 + k * 18, ay + 40 + q * 120, 9, "#7fd4ff", 0.8 * (1 - q) * (1 - prog(t, tv, 0.6)))
            C(c, "SWEAT MOLECULES", 1420, 260, vis(t, B(0, 0.25)), ts, dot="#7fd4ff")
            T(c, "+", 1420, 345, 60, ts, "#ffffff", vis(t, B(0, 0.4)))
            C(c, "SKIN BACTERIA", 1420, 430, vis(t, B(0, 0.4)), ts, dot=LIME)
            T(c, "↓", 1420, 515, 60, ts, "#ffffff", vis(t, B(0, 0.55)))
            C(c, "PUNGENT SULFUR COMPOUNDS", 1420, 600, vis(t, B(0, 0.6)), ts, dot="#c8e86a", bg="#3b3a10")
            C(c, "SMELLABLE AT 1 PART PER TRILLION", 1420, 760, vis(t, B(1, 0.05)), ts, size=32, bg=ACCENT, fg="#2a0a2c", a=1)
            stamp(c, "NO BACTERIA", 1420, 900, prog(t, tv + 0.3, 0.4), 1.0, color=LIME, size=60, rot=-6)
        run_panels(c, W, H, t, S, [(0, pA)])

# ------------------------------------------------------------------ x5_rules (sterile room / bubble)
def x5_rules(c, W, H, t, S):
    o = S.opts; mode = o.get("mode", "rules")
    if mode == "rules":
        B = beats(S, 4); tv = B(0, 0.35)
        def pA(c, ts):
            body(c, BX, BT, BH, colon=0.6); swarm(c, t, BX, BT, BH, vanish_t=tv)
            clock(c, 1380, 300, 120, eout(prog(t, 0, tv)), colr=MAGENTA)
            C(c, "MIDNIGHT", 1380, 470, vis(t, 0.2), ts, dot=LIME)
            for k, s in enumerate(("GUT", "SKIN", "MOUTH")):
                xx = 1170 + k * 210
                C(c, s, xx, 640, vis(t, B(0, 0.5 + k * 0.1)), ts, size=34)
                xmark(c, xx, 730, 26, prog(t, B(0, 0.6 + k * 0.1), 0.3))
        def pB(c, ts):
            body(c, BX, BT, BH, colon=0.3)
            C(c, "VIRUSES & FUNGI: STAY", 1380, 330, vis(t, B(1, 0.05)), ts, dot=TEAL)
            C(c, "YOUR OWN CELLS: FINE", 1380, 480, vis(t, B(1, 0.45)), ts, dot=CORAL)
            check(c, 1380, 640, 50, prog(t, B(1, 0.6), 0.4))
        def pC(c, ts):
            sc_ = 0.82; bx = 700
            isolator(c, bx, 1000, 760, 900, a=1.0, gloves=False)
            body(c, bx, 1000 - 900 * sc_ - 40, 880 * sc_ * 0.98, colon=0.3)
            # filter + airflow
            rrect(c, bx - 200, 70, 400, 50, 12, "#dfe6ef", 1);
            for k in range(9): line(c, bx - 180 + k * 45, 78, bx - 180 + k * 45, 112, "#8d97a6", 4, 1)
            for k in range(6):
                q = (t * 0.5 + k / 6) % 1
                line(c, bx - 250 + k * 100, 140 + q * 300, bx - 250 + k * 100, 190 + q * 300, ICE, 4, 0.5 * (1 - q))
            C(c, "FILTERED AIR", 1450, 230, vis(t, B(2, 0.3)), ts, dot=ICE)
            soda_can(c, 1330, 520, 90 * eback(prog(t, B(2, 0.5), 0.4)))
            rrect(c, 1500, 470, 90, 120, 14, "#bfe9ff", 0.7 * vis(t, B(2, 0.6)))
            stamp(c, "STERILE", 1450, 700, prog(t, B(2, 0.7), 0.4), 1.0, color=TEAL, size=70, rot=-8)
        def pD(c, ts):
            for k in range(3):
                xx = 400 + k * 560; aa = vis(t, B(3, 0.05 + k * 0.12))
                isolator(c, xx, 760, 440, 330, a=aa)
                mouse(c, xx - 20, 700, 70, a=aa, face=1 if k % 2 == 0 else -1)
            C(c, "GERM-FREE ANIMALS", 960, 200, vis(t, B(3, 0.3)), ts, size=44, bg=TEAL, fg="#08201e", a=1)
            C(c, "DECADES OF LAB DATA", 960, 880, vis(t, B(3, 0.55)), ts)
        run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB), (B(2, 0), pC), (B(3, 0), pD)])
    else:  # bubble
        B = beats(S, 2)
        def pA(c, ts):
            isolator(c, 760, 900, 900, 560)
            # crib
            rrect(c, 560, 640, 400, 160, 20, "#f4e9f0", 1)
            for k in range(9): line(c, 580 + k * 45, 560, 580 + k * 45, 650, "#f4e9f0", 8, 1)
            line(c, 570, 560, 950, 560, "#f4e9f0", 10, 1)
            oval(c, 760, 625, 120, 40, "#ffd4c7", 1); circle(c, 650, 610, 38, "#ffd4c7", 1)
            C(c, "STERILE ISOLATION", 1500, 360, vis(t, B(0, 0.2)), ts, dot=TEAL)
            C(c, "WHILE WAITING FOR A", 1500, 500, vis(t, B(0, 0.6)), ts, size=32)
            C(c, "STEM CELL TRANSPLANT", 1500, 590, vis(t, B(0, 0.65)), ts, size=32, bg=ACCENT, fg="#2a0a2c", a=1)
        def pB(c, ts):
            p = prog(t, B(1, 0.0), 0.8)
            circle(c, 620, 540, 430, TEAL, 0.1); circle(c, 620, 540, 430, TEAL, 0.7, stroke=5)
            body(c, 620, 180, 700, colon=0.25)
            for k in range(3):
                capsule(c, 1200 + k * 150, 300, 56 * eback(prog(t, B(1, 0.1 + k * 0.06), 0.4)), "", ang=-20 + k * 20)
            C(c, "+ EXTRA VITAMINS", 1350, 420, vis(t, B(1, 0.15)), ts, dot=ACCENT)
            for k in range(3):
                gear(c, 1180 + k * 160, 640 + (k % 2) * 40, 52, t * 20 * (1 - p) * (1 if k % 2 else -1), 0.9, mix(LIME, GREY, p))
            C(c, "MACHINERY: SWITCHED OFF", 1350, 820, vis(t, B(1, 0.5)), ts, size=32, dot=GREY)
        run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB)])

# ------------------------------------------------------------------ x5_count (the headcount)
def p_myth(t, S, B, i):
    def f(c, ts):
        book(c, 560, 520, 760, 520)
        T(c, "10 : 1", 560, 470, 170, ts, "#3a0f2e", prog(t, B(i, 0.05), 0.4), shadow=0, maxw=640)
        T(c, "BACTERIA : HUMAN CELLS", 560, 620, 36, ts, "#7a5a6a", prog(t, B(i, 0.15), 0.4), w=800, shadow=0, maxw=640)
        for k in range(10):
            bug(c, 1150 + (k % 5) * 110, 380 + (k // 5) * 110, 34, "rod" if k % 2 else "coc", LIME, k * 33 + t * 30, vis(t, B(i, 0.3 + k * 0.03)))
        human_cell(c, 1370, 680, 50, vis(t, B(i, 0.65)))
        C(c, "WHAT TEXTBOOKS SAID FOR DECADES", 960 if S.P else 1370, 980 if S.P else 850, vis(t, B(i, 0.5)), ts, size=30)
    return f

def p_note(t, S, B, i):
    def f(c, ts):
        c.save(); c.translate(620, 500); c.rotate(-6)
        rrect(c, -340, -230, 680, 460, 8, "#fdf6d8", 1); rrect(c, -340, -230, 680, 460, 8, "#000000", 0.15, stroke=3)
        for k in range(7): line(c, -310, -150 + k * 55, 310, -150 + k * 55, "#b9d3ee", 2, 0.8)
        text(c, "gut ≈ 1 litre", -280, -150, 50, "#1f3b8a", prog(t, B(i, 0.05), 0.3), w=500, fam="Inter", align="l")
        text(c, "× 10¹¹ / gram", -280, -40, 50, "#1f3b8a", prog(t, B(i, 0.15), 0.3), w=500, fam="Inter", align="l")
        text(c, "≈ 10¹⁴ bacteria!", -280, 80, 62, "#c2185b", prog(t, B(i, 0.25), 0.3), w=700, fam="Inter", align="l")
        c.restore()
        C(c, "1972 · A QUICK ESTIMATE", 1420, 230, vis(t, B(i, 0.1)), ts, dot=ACCENT)
        n = int(7 * eout(prog(t, B(i, 0.5), 1.2)))
        for k in range(n):
            xx = 1260 + k * 40; yy = 420 + k * 36
            rrect(c, xx - 140, yy - 70, 280, 140, 14, "#f6efe2", 0.95); text(c, "10 : 1", xx, yy, 60, "#3a0f2e", 1, w=900)
        C(c, "REPEATED FOR 40+ YEARS", 1420, 880, vis(t, B(i, 0.6)), ts, size=34)
    return f

def p_bars(t, S, B, i):
    def f(c, ts):
        stamp(c, "2016 RECOUNT", 960, 170, prog(t, B(i, 0.0), 0.4), 1.0, color=ACCENT, size=70, rot=-4)
        rng = random.Random(2)
        for row, (n, colr, lab, val, y) in enumerate(((38, LIME, "BACTERIA", "≈ 38 TRILLION", 420), (30, CORAL, "HUMAN CELLS", "≈ 30 TRILLION", 690))):
            T(c, lab, 200, y - 110, 40, ts, colr, vis(t, B(i, 0.2 + row * 0.2)), w=800, fam="Inter", align="l", maxw=700)
            on = int(n / 2 * eout(prog(t, B(i, 0.2 + row * 0.2), 1.0)))
            for k in range(on):
                xx = 240 + k * 66
                if row == 0: bug(c, xx, y, 30, "rod" if k % 3 else "coc", LIME if k % 4 else TEAL, 90 + k * 12, 1)
                else: human_cell(c, xx, y, 27, 1)
            T(c, val, 1800, y - 110, 44, ts, "#ffffff", vis(t, B(i, 0.35 + row * 0.2)), align="r", maxw=640 if not S.P else 760)
        C(c, "≈ 1.3 : 1", 960, 900, vis(t, B(i, 0.75)), ts, size=46, bg=LIME, fg="#2a0a2c", a=1)
        if not S.P: T(c, "EACH ICON ≈ 2 TRILLION", 200, 1010, 26, ts, "#cfc1d6", vis(t, B(i, 0.4)), w=600, fam="Inter", align="l", maxw=700)
    return f

def p_rbc(t, S, B, i):
    def f(c, ts):
        fr = 0.84 * eout(prog(t, B(i, 0.15), 1.0))
        donut(c, 620, 520, 290, 1.0, CORAL, 0.35)
        donut(c, 620, 520, 290, fr, "#e0303f", 1.0, label=f"{int(round(fr * 100))}%")
        ys = (300, 520, 740) if S.P else (540, 650, 770)
        for k in range(5): rbc(c, 1180 + k * 120, 120 if S.P else 380, 46, vis(t, B(i, 0.3 + k * 0.05)))
        C(c, "OF YOUR CELLS ARE", 1420, ys[0], vis(t, B(i, 0.35)), ts, size=34)
        C(c, "RED BLOOD CELLS", 1420, ys[1], vis(t, B(i, 0.45)), ts, size=46 if not S.P else 38, bg="#e0303f", a=1)
        C(c, "BY COUNT", 1420, ys[2], vis(t, B(i, 0.6)), ts, size=30, dot=CORAL)
    return f

def p_colon(t, S, B, i):
    def f(c, ts):
        h = 1500; cx = 640; top = -330
        body(c, cx, top, h, colon=1.0); swarm(c, t, cx, top, h, n=200, seed=8)
        C(c, "YOUR COLON", 1420, 250, vis(t, B(i, 0.05)), ts, dot=MAGENTA)
        T(c, "≈ 0.4 LITERS", 1420, 420, 96, ts, LIME, prog(t, B(i, 0.3), 0.4), maxw=800)
        soda_can(c, 1340, 650, 120 * eback(prog(t, B(i, 0.6), 0.4)))
        T(c, "+ A BIT", 1560, 650, 50, ts, "#ffffff", vis(t, B(i, 0.7)), maxw=320)
    return f

def p_sites(t, S, B, i):
    def f(c, ts):
        body(c, BX, BT, BH, colon=1.0); swarm(c, t, BX, BT, BH)
        for k, (lab, y, yy_body, colr) in enumerate((("COLON: ≈ 38 TRILLION", 790, BT + 0.47 * BH, LIME),
                                                      ("SKIN: ≈ 1 TRILLION", 560, BT + 0.3 * BH, TEAL),
                                                      ("MOUTH: < 1% OF THE COLON", 330, BT + 0.09 * BH, PEACH))):
            p = vis(t, B(i, 0.05 + k * 0.28))
            if p > 0:
                line(c, BX + (0.13 * BH if k != 2 else 0.05 * BH), yy_body, 1050, y, colr, 4, p)
                circle(c, BX + (0.13 * BH if k != 2 else 0.05 * BH), yy_body, 12, colr, p)
            C(c, lab, 1420, y, p, ts, size=36, dot=colr)
    return f

def p_balance(t, S, B, i, tflip):
    def f(c, ts):
        fl = eout(prog(t, tflip, 0.9))
        ang = lerp(-9, 7, fl)
        cx, cy = 960, 330
        c.drawPath(poly([(cx - 70, 900), (cx + 70, 900), (cx + 18, cy), (cx - 18, cy)]), paint("#c9a6c4", 1))
        rect(c, cx - 160, 900, 320, 26, "#c9a6c4", 1)
        c.save(); c.translate(cx, cy); c.rotate(ang)
        rrect(c, -600, -14, 1200, 28, 14, "#efe1ec", 1)
        c.restore()
        for sg in (-1, 1):
            px = cx + sg * 560 * math.cos(math.radians(ang)); py = cy + sg * 560 * math.sin(math.radians(ang))
            line(c, px, py, px - 140, py + 230, "#efe1ec", 4, 1); line(c, px, py, px + 140, py + 230, "#efe1ec", 4, 1)
            oval(c, px, py + 240, 200, 36, "#efe1ec", 1)
            if sg < 0:
                k_on = 1 - 0.3 * fl
                for k in range(int(14 * k_on)):
                    bug(c, px - 140 + (k % 7) * 46, py + 205 - (k // 7) * 40, 20, "rod" if k % 2 else "coc", LIME, k * 40, 1)
                T(c, "BACTERIA", px, py + 330, 40, ts, LIME, 1, maxw=420)
            else:
                for k in range(12):
                    human_cell(c, px - 130 + (k % 6) * 52, py + 205 - (k // 6) * 44, 20, 1)
                T(c, "YOUR CELLS", px, py + 330, 40, ts, CORAL, 1, maxw=420)
        toilet(c, 300, 900, 120 * eback(prog(t, tflip - 0.6, 0.4)), clamp(prog(t, tflip - 0.6, 0.4)))
        C(c, "ONE TRIP TO THE TOILET", 960, 120, vis(t, tflip - 0.4), ts, size=36, dot=ACCENT)
    return f

def p_half(t, S):
    def f(c, ts):
        body(c, 960, 100, 880, colon=0.6)
        c.save(); c.clipRect(skia.Rect.MakeLTRB(960, 0, 2000, 1080)); swarm(c, t, 960, 100, 880, n=300, seed=11); c.restore()
        line(c, 960, 80, 960, 1000, "#ffffff", 4, 0.7, dash=([20, 14], -t * 30))
        T(c, "YOU", 520, 520, 110, ts, CORAL, prog(t, 0.2, 0.4), maxw=500)
        T(c, "BACTERIA", 1420, 520, 110, ts, LIME, prog(t, 0.6, 0.4), maxw=560)
    return f

def x5_count(c, W, H, t, S):
    mode = S.opts.get("mode", "census")
    if mode == "census":
        if short1(S):
            items = [(0, p_half(t, S))]
        else:
            B = beats(S, 4)
            items = [(0, p_myth(t, S, B, 0)), (B(1, 0), p_note(t, S, B, 1)), (B(2, 0), p_bars(t, S, B, 2)), (B(3, 0), p_rbc(t, S, B, 3))]
    elif mode == "where":
        if S.P:
            B = beats(S, 2)
            items = [(0, p_rbc(t, S, B, 0)), (B(1, 0), p_colon(t, S, B, 1))]
        else:
            B = beats(S, 3)
            items = [(0, p_colon(t, S, B, 0)), (B(1, 0), p_sites(t, S, B, 1)), (B(2, 0), p_balance(t, S, B, 2, B(2, 0.6)))]
    elif mode == "myth":
        B = beats(S, 2)
        items = [(0, p_myth(t, S, B, 0)), (B(1, 0), p_note(t, S, B, 1))]
    elif mode == "scale":
        B = lambda i, f=0.0: S.lt(0, f)
        items = [(0, p_bars(t, S, B, 0))]
    else:  # flip
        items = [(0, p_balance(t, S, None, 0, S.lt(0, 0.5)))]
    run_panels(c, W, H, t, S, items)

# ------------------------------------------------------------------ x5_genes
def x5_genes(c, W, H, t, S):
    B = beats(S, 2)
    def pA(c, ts):
        rrect(c, 230, 470, 70, 110, 10, CORAL, vis(t, B(0, 0.05)))
        T(c, "YOUR GENOME", 265, 650, 34, ts, CORAL, vis(t, B(0, 0.05)), w=800, fam="Inter", maxw=420)
        n = int(150 * eout(prog(t, B(0, 0.3), 2.2)))
        for k in range(n):
            col_ = k % 15; row = k // 15
            rrect(c, 520 + col_ * 88, 170 + row * 66, 70, 52, 8, LIME if (k * 7) % 3 else TEAL, 0.92)
        T(c, f"× {max(1, n)}", 1200, 880, 90, ts, LIME, vis(t, B(0, 0.3)), maxw=600)
        C(c, "3.3 MILLION BACTERIAL GENES", 1200, 990, vis(t, B(0, 0.55)), ts, size=34, dot=LIME)
    def pB(c, ts):
        lost = prog(t, B(1, 0.75), 0.6)
        for k, (lab, draw) in enumerate((("BREAK DOWN FOOD", "fiber"), ("MAKE VITAMINS", "pill"), ("BUILD CHEMICALS", "flask"))):
            x = 420 + k * 540; p = vis(t, B(1, 0.1 + k * 0.12))
            if p <= 0: continue
            rrect(c, x - 220, 260, 440, 440, 40, mix("#4a1240", "#2a2430", lost), p)
            rrect(c, x - 220, 260, 440, 440, 40, mix(LIME, GREY, lost), p, stroke=5)
            if draw == "fiber":
                for j in range(3):
                    pth = skia.Path(); pth.moveTo(x - 140, 420 + j * 50)
                    for i in range(1, 9): pth.lineTo(x - 140 + i * 35, 420 + j * 50 + math.sin(i + j + t * 2) * 14)
                    c.drawPath(pth, paint(mix("#f0d9a0", GREY, lost), p, stroke=12))
            elif draw == "pill":
                capsule(c, x, 470, 90, "K", p, ang=-20, c1=mix(ACCENT, GREY, lost))
            else:
                flask(c, x, 470, 120, p, colr=mix(TEAL, GREY, lost))
            T(c, lab, x, 780, 40, ts, "#ffffff", p, maxw=480)
        stamp(c, "ALL GONE", 960, 470, lost, 1.0, color=RED, size=110, rot=-8)
    run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB)])

# ------------------------------------------------------------------ x5_gut
def x5_gut(c, W, H, t, S):
    mode = S.opts.get("mode", "normal")
    B = beats(S, 3)
    if mode == "normal":
        def pA(c, ts):
            gut(c, t, 0, 1920, 330, 750, bugs=0, scfa=0, energy=0.55)
            C(c, "FIBER", 300, 540, vis(t, B(0, 0.2)), ts, size=40, dot="#f0d9a0")
            C(c, "YOUR ENZYMES CAN'T BREAK IT DOWN", 960, 990, vis(t, B(0, 0.5)), ts, size=34)
            C(c, "INSIDE YOUR COLON", 960, 90, vis(t, 0.2), ts, dot=MAGENTA)
        def pB(c, ts):
            gut(c, t, 0, 1920, 330, 750, bugs=1, scfa=eout(prog(t, B(1, 0.3), 0.8)), energy=0.7, gas=0.5)
            C(c, "BACTERIA FERMENT IT", 960, 90, vis(t, B(1, 0.05)), ts, dot=LIME)
            C(c, "ACETATE · PROPIONATE · BUTYRATE", 960, 990, vis(t, B(1, 0.45)), ts, size=36, dot=TEAL)
        def pC(c, ts):
            gut(c, t, 0, 1920, 330, 750, bugs=1, scfa=1, energy=1.0)
            C(c, "BUTYRATE = KEY FUEL FOR COLON CELLS", 960, 90, vis(t, B(2, 0.05)), ts, size=36, bg=ACCENT, fg="#2a0a2c", a=1)
            for k in range(4):
                bolt(c, 330 + k * 420, 260, 34, vis(t, B(2, 0.3 + k * 0.05)) * (0.7 + 0.3 * math.sin(t * 6 + k)))
            C(c, "OTHER CELLS BURN SUGAR. THESE RUN ON BACTERIAL FOOD.", 960, 990, vis(t, B(2, 0.5)), ts, size=30)
        run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB), (B(2, 0), pC)])
    else:  # starve
        def pA(c, ts):
            tv = 0.3
            gut(c, t, 0, 1920, 330, 750, bugs=1, scfa=1 - prog(t, tv, 0.8), energy=lerp(1.0, 0.0, prog(t, 0.6, 2.5)), flow=2.2,
                vanish_t=tv, cells_grey=0.6 * prog(t, 0.6, 2.5))
            for k in range(4): battery(c, 330 + k * 420, 255, 34, lerp(1, 0.08, prog(t, 0.6, 2.5)), vis(t, 0.8))
            if S.P:
                C(c, "COLON CELLS: LOW ON FUEL", 960, 990, vis(t, 0.8), ts, size=26)
            else:
                C(c, "ENERGY-STARVED · GERM-FREE MICE, 2011", 960, 990, vis(t, B(0, 0.25)), ts, size=34, dot=RED)
                C(c, "DIGESTING PARTS OF THEMSELVES", 960, 90, vis(t, B(0, 0.7)), ts, size=34)
        items = [(0, pA)]
        if not S.P:
            def pB(c, ts):
                rescue = eout(prog(t, B(1, 0.25), 1.2))
                gut(c, t, 0, 1920, 330, 750, bugs=0, scfa=rescue, energy=rescue, flow=2.2, cells_grey=0.6 * (1 - rescue))
                for k in range(4): battery(c, 330 + k * 420, 255, 34, lerp(0.08, 1, rescue), 1)
                C(c, "+ BUTYRATE", 960, 90, vis(t, B(1, 0.1)), ts, size=40, bg=TEAL, fg="#08201e", a=1)
                C(c, "ENERGY SHORTAGE: GONE", 960, 990, vis(t, B(1, 0.55)), ts, size=36, dot=LIME)
            def pC(c, ts):
                gut(c, t, 0, 1920, 330, 750, bugs=0, scfa=0, energy=0.15, flow=3.0, cells_grey=0.6, gas=1 - prog(t, B(2, 0.55), 0.8))
                C(c, "FIBER PASSES STRAIGHT THROUGH", 960, 90, vis(t, B(2, 0.05)), ts, size=36, dot="#f0d9a0")
                C(c, "NO FERMENTATION = A LOT LESS GAS", 960, 990, vis(t, B(2, 0.5)), ts, size=36, bg=ACCENT, fg="#2a0a2c", a=1)
            items += [(B(1, 0), pB), (B(2, 0), pC)]
        run_panels(c, W, H, t, S, items)

def bolt(c, x, y, s, a=1.0):
    if a <= 0: return
    c.drawPath(poly([(x + s * 0.2, y - s), (x - s * 0.5, y + s * 0.1), (x, y + s * 0.1), (x - s * 0.2, y + s), (x + s * 0.5, y - s * 0.1), (x, y - s * 0.1)]), paint(ACCENT, a))

# ------------------------------------------------------------------ x5_vitamins
def x5_vitamins(c, W, H, t, S):
    B = beats(S, 3)
    def pA(c, ts):
        # blood vessel along the bottom
        c.drawRect(skia.Rect.MakeLTRB(0, 700, 1920, 900), paint(shader=lin(0, 700, 0, 900, [(0, "#7a0f22", 1), (0.5, "#c21d3a", 1), (1, "#7a0f22", 1)])))
        for k in range(10):
            xx = (k * 220 + t * 120) % 2100 - 100; rbc(c, xx, 800 + math.sin(k) * 40, 34, 0.9)
        for k in range(3):
            bx = 400 + k * 560
            bug(c, bx, 330, 90, "rod", [LIME, TEAL, LIME][k], -10 + k * 15 + 5 * math.sin(t + k), 1)
            for j in range(3):
                q = (t * 0.45 + j / 3 + k * 0.2) % 1
                capsule(c, bx + 40 + j * 10, lerp(400, 760, q), 44, "K" if (j + k) % 2 == 0 else "B", 1 - q * 0.5, ang=q * 160)
        C(c, "VITAMIN K → HELPS BLOOD CLOT", 560, 120, vis(t, B(0, 0.3)), ts, size=34, dot=ACCENT)
        C(c, "+ SEVERAL B VITAMINS", 1450, 120, vis(t, B(0, 0.7)), ts, size=34, dot=TEAL)
    def pB(c, ts):
        x0, x1, y0, y1 = 300, 1650, 260, 800
        line(c, x0, y1, x1, y1, "#ffffff", 4, 0.8); line(c, x0, y0, x0, y1, "#ffffff", 4, 0.8)
        T(c, "CLOTTING PROTEIN IN BLOOD", x0 - 10, y0 - 50, 32, ts, "#ffffff", 1, w=700, fam="Inter", align="l", maxw=900)
        T(c, "WEEKS ON A LOW-VITAMIN-K DIET →", x1, y1 + 60, 30, ts, "#cfc1d6", 1, w=600, fam="Inter", align="r", maxw=900)
        p1 = eout(prog(t, B(1, 0.05), 1.5)); p2 = eout(prog(t, B(1, 0.5), 1.5))
        def curve(fn, p, colr, lab, ly):
            pth = skia.Path(); n = 40
            for i in range(int(n * p) + 1):
                xx = x0 + (x1 - x0) * i / n; yy = fn(i / n)
                if i == 0: pth.moveTo(xx, yy)
                else: pth.lineTo(xx, yy)
            c.drawPath(pth, paint(colr, 1, stroke=10))
            if p > 0.95: C(c, lab, x1 - 280, ly, 1, ts, size=28, dot=colr)
        curve(lambda f: y0 + 120 + 6 * math.sin(f * 9), p1, LIME, "DIET ONLY: FINE", y0 + 60)
        curve(lambda f: y0 + 130 + 330 * ease(clamp((f - 0.3) / 0.5)), p2, RED, "+ ANTIBIOTIC: DROPS", y0 + 540)
        capsule(c, x0 + (x1 - x0) * 0.3, y0 + 300, 40 * eback(prog(t, B(1, 0.5), 0.4)), "", ang=30, c1=RED)
    def pC(c, ts):
        # cage
        rrect(c, 260, 260, 900, 600, 20, "#ffffff", 0.06)
        for k in range(16): line(c, 290 + k * 56, 270, 290 + k * 56, 850, "#cfd6e0", 4, 0.55)
        line(c, 260, 270, 1160, 270, "#cfd6e0", 8, 0.8)
        mouse(c, 640, 820, 140, colr="#e8dde3", rat=True)
        oval(c, 980, 815, 110, 34, "#8a6a9a", 1); oval(c, 980, 800, 90, 22, "#c8a46a", 1)
        pk = prog(t, B(2, 0.75), 0.5)
        for k in range(3): capsule(c, 940 + k * 40, 770 - 30 * eback(pk), 22, "K", clamp(pk), ang=k * 30)
        C(c, "1950s · GERM-FREE RATS", 1500, 300, vis(t, B(2, 0.05)), ts, dot=ACCENT)
        stamp(c, "VITAMIN K DEFICIENT", 1500, 500, prog(t, B(2, 0.25), 0.4), 1.0, color=RED, size=48, rot=-6)
        C(c, "… UNLESS IT'S ADDED TO THE FOOD", 1500, 700, vis(t, B(2, 0.5)), ts, size=30, dot=LIME)
    run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB), (B(2, 0), pC)])

# ------------------------------------------------------------------ x5_mouse (giant cecum)
def mouse_xray(c, t, x, y, s, cec):
    mouse(c, x, y, s, colr="#e8dde3")
    cx, cy = x - s * 0.05, y - s * 0.45
    oval(c, cx, cy, s * 0.82, s * 0.38, "#3a0f2e", 0.85)
    p = skia.Path(); p.moveTo(cx + s * 0.75, cy - s * 0.1)
    for i in range(1, 30):
        f = i / 29; p.lineTo(cx + s * 0.75 - f * s * 1.4, cy - s * 0.1 + math.sin(f * 14) * s * 0.12)
    c.drawPath(p, paint(CORAL, 0.9, stroke=s * 0.05))
    r = s * lerp(0.13, 0.5, cec)
    ccx, ccy = cx - s * 0.1, cy + s * 0.05
    circle(c, ccx, ccy, r * 1.25, MAGENTA, 0.35, blur=r * 0.3)
    circle(c, ccx, ccy, r, MAGENTA, 0.95); circle(c, ccx - r * 0.3, ccy - r * 0.3, r * 0.3, "#ff9fc4", 0.6)
    circle(c, ccx, ccy, r, "#ffd0e2", 0.8, stroke=4)
    return ccx, ccy, r

def x5_mouse(c, W, H, t, S):
    B = beats(S, 3)
    def pA(c, ts):
        cec = 0.15 if not short1(S) else eout(prog(t, S.lt(0, 0.35), 1.6))
        mx, my, r = mouse_xray(c, t, 860 if short1(S) else 760, 980 if short1(S) else 900, 560 if short1(S) else 520, cec)
        C(c, "CECUM", mx, my - r - 60 if not short1(S) else 90, vis(t, 0.3), ts, size=40, bg=MAGENTA, a=1)
        if not short1(S):
            C(c, "GERM-FREE LAB MOUSE", 1520, 220, vis(t, B(0, 0.1)), ts, dot=TEAL)
            C(c, "WHERE MICE FERMENT A LOT OF FOOD", 1520, 340, vis(t, B(0, 0.6)), ts, size=28)
    items = [(0, pA)]
    if not short1(S):
        def pB(c, ts):
            cec = lerp(0.15, 1.0, eout(prog(t, B(1, 0.0), 2.5)))
            mx, my, r = mouse_xray(c, t, 760, 900, 520, cec)
            for k, lab in enumerate(("MUCUS", "ENZYMES", "WATER")):
                C(c, lab, 1520, 220 + k * 110, vis(t, B(1, 0.1 + k * 0.12)), ts, size=34, dot=[PEACH, ACCENT, "#7fd4ff"][k])
            # weight bar
            x0, y = 1260, 700; w = 520
            rrect(c, x0, y - 30, w, 60, 30, "#ffffff", 0.12)
            f = 0.2 * eout(prog(t, B(1, 0.55), 1.2))
            rrect(c, x0, y - 30, max(60, w * f), 60, 30, MAGENTA, 1)
            T(c, "UP TO 1/5 OF BODY WEIGHT", x0 + w / 2, y + 85, 36, ts, "#ffffff", vis(t, B(1, 0.6)), maxw=620)
            C(c, "IN SOME STRAINS", x0 + w / 2, y + 180, vis(t, B(1, 0.7)), ts, size=28)
        def pC(c, ts):
            body(c, 520, 120, 820, colon=0.4)
            circle(c, 520, 120 + 0.46 * 820, 90 * eback(prog(t, B(2, 0.3), 0.5)), MAGENTA, 0.9)
            beagle(c, 1350, 760, 180, vis(t, B(2, 0.45)))
            T(c, "≈ 14 kg", 1350, 300, 120, ts, LIME, prog(t, B(2, 0.35), 0.4), maxw=700)
            C(c, "HYPOTHETICAL: IF A HUMAN GUT DID THE SAME", 960, 960, vis(t, B(2, 0.05)), ts, size=30)
        items += [(B(1, 0), pB), (B(2, 0), pC)]
    run_panels(c, W, H, t, S, items)

# ------------------------------------------------------------------ x5_immune
def x5_immune(c, W, H, t, S):
    mode = S.opts.get("mode", "train")
    if mode == "train":
        B = beats(S, 4)
        def gut_with_immune(c, ts, train):
            gut(c, t, 0, 1920, 190, 470, bugs=1, scfa=0.6, energy=0.8, seed=3)
            rect(c, 0, 590, 1920, 160, "#2a0a2c", 1)
            for k in range(7):
                ix = 160 + k * 270; iy = 660 + 20 * math.sin(t + k)
                immune_cell(c, ix, iy, 34, 1, t + k)
                if train > 0:
                    line(c, ix, iy - 40, ix + 40, 420, "#7fd4ff", 3, train * (0.5 + 0.5 * math.sin(t * 4 + k)), dash=([10, 10], -t * 40))
        def pA(c, ts):  # the like-and-subscribe line plays here: keep the bottom band (y > 780) clear
            gut_with_immune(c, ts, 0.3)
            C(c, "YOUR GUT: HOME OF YOUR IMMUNE SYSTEM'S TRAINING CAMP", 960, 90, vis(t, 0.4), ts, size=30, dot="#7fd4ff")
        def pB(c, ts):
            gut_with_immune(c, ts, eout(prog(t, B(1, 0.4), 0.8)))
            C(c, "IT LEARNS BY MEETING YOUR BACTERIA", 960, 90, vis(t, B(1, 0.3)), ts, size=34, dot="#7fd4ff")
            C(c, "IMMUNE CELLS", 960, 860, vis(t, B(1, 0.2)), ts, size=32)
        def pC(c, ts):
            for k, (lab, n_ab, patch, nb) in enumerate((("NORMAL", 14, 1.0, 10), ("GERM-FREE", 3, 0.4, 0))):
                x = 520 + k * 880
                rrect(c, x - 380, 220, 760, 560, 40, "#ffffff", 0.06); rrect(c, x - 380, 220, 760, 560, 40, [LIME, GREY][k], 0.8, stroke=4)
                T(c, lab, x, 170, 48, ts, [LIME, "#ffffff"][k], vis(t, B(2, 0.05 + k * 0.1)), maxw=700)
                oval(c, x, 640, 220 * patch, 90 * patch, "#5a8fd6", 0.85)
                for j in range(int(6 * patch) + 1): immune_cell(c, x - 160 * patch + j * 60 * patch, 640, 20 * max(patch, 0.6), 1, t + j)
                rng = random.Random(k + 4)
                for j in range(n_ab): yab(c, x + rng.uniform(-300, 300), rng.uniform(300, 520), 26, vis(t, B(2, 0.5)), rot=rng.uniform(-30, 30))
                for j in range(nb): bug(c, x + rng.uniform(-320, 320), rng.uniform(280, 540), 18, "rod", LIME, rng.random() * 360, 0.6)
            C(c, "SMALLER GUT IMMUNE TISSUE · FEWER IMMUNE CELLS · LESS IgA", 960, 900, vis(t, B(2, 0.35)), ts, size=28 if not S.P else 18)
        def pD(c, ts):
            for k in range(30):
                bx = 860 + (k % 5) * 90 + (k // 5 % 2) * 45; by = 230 + (k // 5) * 100
                bug(c, bx, by, 30, "rod" if k % 3 else "coc", LIME if k % 2 else TEAL, 90 + 10 * math.sin(t * 2 + k), 1)
            q = (t - B(3, 0.1)) % 2.4
            px = lerp(200, 720, ease(clamp(q / 1.0))) - 300 * ease(clamp((q - 1.0) / 1.0))
            pathogen(c, px, 540, 50, vis(t, B(3, 0.1)), rot=0, t=t)
            if 0.95 < q < 1.4: circle(c, 780, 540, 60 + (q - 0.95) * 200, "#ffffff", (1.4 - q) * 1.5, stroke=6)
            C(c, "NO ROOM. NO FOOD.", 1450, 300, vis(t, B(3, 0.3)), ts, size=34)
            C(c, "COLONIZATION RESISTANCE", 960, 920, vis(t, B(3, 0.6)), ts, size=40, bg=LIME, fg="#2a0a2c", a=1)
        run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB), (B(2, 0), pC), (B(3, 0), pD)])
    else:  # cdiff
        B = beats(S, 3)
        def pA(c, ts):
            tz = B(0, 0.4)
            gut(c, t, 0, 1920, 300, 780, bugs=1, scfa=0, energy=0.6, vanish_t=tz, seed=5)
            ax = lerp(-200, 2100, prog(t, tz - 0.3, 1.2))
            capsule(c, ax, 540, 90, "", 1.0 if t < tz + 1.0 else 0, ang=0, c1=RED)
            grow = prog(t, B(0, 0.7), 2.5)
            rng = random.Random(8)
            for k in range(int(18 * grow)):
                pathogen(c, rng.uniform(100, 1820), rng.uniform(380, 700), 26, 1, rot=rng.random() * 360, t=t + k)
            C(c, "ANTIBIOTICS", 960, 120, vis(t, B(0, 0.25)), ts, dot=RED)
            C(c, "C. DIFF TAKES OVER", 960, 960, vis(t, B(0, 0.75)), ts, size=40, bg=PURP, a=1)
        def pB(c, ts):
            v1 = 450000 * eout(prog(t, B(1, 0.05), 1.4)); v2 = 29000 * eout(prog(t, B(1, 0.55), 1.2))
            T(c, fmt_count(v1) + "+", 960, 330, 150, ts, PURP, vis(t, B(1, 0.05)), maxw=1300)
            T(c, "INFECTIONS", 960, 450, 46, ts, "#ffffff", vis(t, B(1, 0.1)), maxw=900)
            T(c, "≈ " + fmt_count(v2), 960, 640, 120, ts, RED, vis(t, B(1, 0.55)), maxw=1100)
            T(c, "LINKED DEATHS", 960, 750, 46, ts, "#ffffff", vis(t, B(1, 0.6)), maxw=900)
            C(c, "UNITED STATES · ONE YEAR · CDC ESTIMATE", 960, 900, vis(t, B(1, 0.2)), ts, size=30)
        def pC(c, ts):
            house_icon(c, 760, 820, 480, door=eout(prog(t, B(2, 0.4), 0.8)))
            pathogen(c, 1350 - 120 * math.sin(t * 0.8), 700, 50, vis(t, B(2, 0.5)), t=t)
            C(c, "NOBODY HOME", 1450, 300, vis(t, B(2, 0.2)), ts, size=40)
            C(c, "DOORS UNLOCKED", 1450, 420, vis(t, B(2, 0.5)), ts, size=40, bg=RED, a=1)
        run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB), (B(2, 0), pC)])

# ------------------------------------------------------------------ x5_brain
def x5_brain(c, W, H, t, S):
    B = beats(S, 3)
    def pA(c, ts):
        for k, (lab, lvl) in enumerate((("NORMAL", 0.35), ("GERM-FREE", 0.85))):
            x = 560 + k * 800
            mouse(c, x, 820, 180, colr="#e8dde3", face=1)
            gauge(c, x, 430, 190, lvl * eout(prog(t, B(0, 0.4 + k * 0.1), 1.0)), "STRESS HORMONES", 1.0, colr=[LIME, RED][k])
            T(c, lab, x, 140, 46, ts, [LIME, "#ffffff"][k], vis(t, B(0, 0.1)), maxw=700)
        C(c, "2004 · JAPAN · AFTER BRIEF RESTRAINT", 960, 980, vis(t, B(0, 0.3)), ts, size=30)
    def pB(c, ts):
        x0, x1, y0, y1 = 260, 1660, 250, 850
        rect(c, x0, y0, (x1 - x0) / 2, y1 - y0, "#0d0410", 1)
        c.drawRect(skia.Rect.MakeLTRB((x0 + x1) / 2, y0, x1, y1), paint(shader=rad(1360, 400, 700, [(0, "#fff6d8", 0.95), (1, "#f0c86a", 0.6)])))
        rect(c, x0, y0, x1 - x0, y1 - y0, "#ffffff", 0.7, stroke=6)
        mouse(c, 560, 760, 100, colr="#bdb0b8", face=-1)
        T(c, "NORMAL", 560, 520, 40, ts, LIME, 1, maxw=500)
        q = (t * 0.25) % 1; gx = 1100 + 380 * math.sin(q * 6.28); gy = 700 + 60 * math.sin(q * 12.56)
        pth = skia.Path()
        for i in range(30):
            qq = q - i * 0.01; xx = 1100 + 380 * math.sin(qq * 6.28); yy = 700 + 60 * math.sin(qq * 12.56)
            if i == 0: pth.moveTo(xx, yy)
            else: pth.lineTo(xx, yy)
        c.drawPath(pth, paint(MAGENTA, 0.6, stroke=6, dash=([12, 10], 0)))
        mouse(c, gx, gy, 100, colr="#e8dde3", face=1 if math.cos(q * 6.28) > 0 else -1)
        T(c, "GERM-FREE", 1360, 360, 40, ts, "#2a0a2c", 1, shadow=0, maxw=500)
        C(c, "2011 · SWEDEN · BOLDER, MORE EXPLORING", 960, 970, vis(t, B(1, 0.2)), ts, size=30)
    def pC(c, ts):
        lvl = lerp(0.85, 0.38, eout(prog(t, B(2, 0.2), 1.2)))
        mouse(c, 560, 820, 180, colr="#e8dde3")
        for k in range(8): bug(c, 420 + k * 40, 560 + 20 * math.sin(k + t * 2), 18, "rod" if k % 2 else "coc", LIME, k * 40, vis(t, B(2, 0.1 + k * 0.03)))
        gauge(c, 560, 380, 170, lvl, "STRESS HORMONES", 1.0, colr=mix(RED, LIME, prog(t, B(2, 0.2), 1.2)))
        C(c, "+ BACTERIA EARLY IN LIFE", 560, 980, vis(t, B(2, 0.1)), ts, size=30, dot=LIME)
        body(c, 1400, 220, 700, a=vis(t, B(2, 0.6)))
        T(c, "?", 1400, 520, 260, ts, ACCENT, vis(t, B(2, 0.65)), shadow=24)
        C(c, "IN PEOPLE? OPEN QUESTION", 1400, 980, vis(t, B(2, 0.7)), ts, size=30)
    run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB), (B(2, 0), pC)])

# ------------------------------------------------------------------ x5_history
HIST = [("1880s", "PASTEUR: LIFE WITHOUT BACTERIA… IMPOSSIBLE?", "flask"),
        ("1890s", "BERLIN: FIRST GERM-FREE GUINEA PIGS (DAYS)", "gpig"),
        ("1940s", "SWEDEN: GERM-FREE RAT COLONIES", "rat"),
        ("1940s", "NOTRE DAME (LOBUND): STEEL CHAMBERS", "steel"),
        ("TODAY", "GERM-FREE MICE: A STANDARD LAB TOOL", "mice")]

def x5_history(c, W, H, t, S):
    B = beats(S, 4)
    def pA(c, ts):
        isolator(c, 960, 860, 820, 520)
        mouse(c, 900, 820, 110); mouse(c, 1100, 820, 80, face=-1)
        T(c, "COULD YOU LIVE LIKE THIS FOR YEARS?", 960, 170, 64, ts, "#ffffff", vis(t, 0.2), maxw=1700)
    def pB(c, ts):
        # pan along a timeline; active node follows the narration
        act = [B(1, 0.0), B(1, 0.5), B(2, 0.0), B(2, 0.55), B(3, 0.0)]
        k_act = max([k for k, tt in enumerate(act) if t >= tt - 0.3] or [0])
        pan = 0.0
        for k in range(1, 5): pan += 560 * ease(prog(t, act[k] - 0.4, 0.8))
        ylin = 860
        line(c, 0, ylin, 1920, ylin, "#ffffff", 5, 0.5)
        for k, (yr, lab, ic) in enumerate(HIST):
            x = 560 + k * 560 - pan
            if x < -500 or x > 2400: continue
            edge = clamp((x - 120) / 260) * clamp((1800 - x) / 260)
            on = vis(t, act[k] - 0.2) * edge; hi = 1.0 if k == k_act else 0.45
            circle(c, x, ylin, 22, LIME if k == k_act else "#cfc1d6", max(on, 0.3 * edge))
            T(c, yr, x, ylin + 70, 52, ts, LIME if k == k_act else "#cfc1d6", max(on, 0.3 * edge), maxw=500)
            with Layer(c, on * hi) as o2:
                if o2:
                    if ic == "flask": flask(c, x, 520, 170, 1, colr=MAGENTA)
                    elif ic == "gpig": isolator(c, x, 720, 420, 300, gloves=False); guinea_pig(c, x, 690, 110)
                    elif ic == "rat": isolator(c, x, 720, 440, 320); mouse(c, x, 690, 120, rat=True)
                    elif ic == "steel": isolator(c, x, 720, 460, 330, steel=True)
                    else:
                        isolator(c, x, 720, 440, 300); mouse(c, x - 70, 690, 60); mouse(c, x + 80, 690, 60, face=-1)
            if k == k_act: C(c, lab, 960, 170, on, ts, size=34 if not S.P else 24, dot=LIME)
        if t > act[4] + 0.5:
            C(c, "SOME STRAINS: THE GIANT CECUM CAUSES TROUBLE WITH AGE", 960, 990, vis(t, B(3, 0.55)), ts, size=28 if not S.P else 18, dot=MAGENTA)
    run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB)])

# ------------------------------------------------------------------ x5_out (opening the door)
def air_bugs(c, t, x0, x1, y0, y1, n, a=1.0, seed=2, rise=1.0):
    rng = random.Random(seed)
    for k in range(n):
        ph = rng.random(); x = rng.uniform(x0, x1); per = rng.uniform(3, 6)
        q = (ph + t / per) % 1
        y = lerp(y1, y0, q) if rise else rng.uniform(y0, y1)
        bug(c, x + math.sin(t * 1.3 + k) * 30, y, rng.uniform(10, 18), rng.choice(["rod", "coc", "spi"]), rng.choice([LIME, TEAL]), rng.random() * 360 + t * 40, a * math.sin(q * math.pi))

def x5_out(c, W, H, t, S):
    B = beats(S, 4)
    def pA(c, ts):
        rect(c, 0, 0, 1920, 1080, "#e8f6f4", 0.12)
        rect(c, 0, 900, 1920, 180, "#2a1430", 1)
        dx, dy, dw, dh = 860, 260, 360, 640
        op = eout(prog(t, B(0, 0.3), 1.2))
        c.drawRect(skia.Rect.MakeXYWH(dx, dy, dw, dh), paint(shader=lin(dx, dy, dx, dy + dh, [(0, "#ffe9b0", op), (1, "#ffb37a", op)])))
        air_bugs(c, t, dx, dx + dw + 600 * op, dy, dy + dh, int(40 * op), a=op, rise=0)
        rect(c, dx, dy, dw * (1 - 0.85 * op), dh, "#cfe7e4", 1)
        rect(c, dx, dy, dw, dh, "#ffffff", 0.9, stroke=8)
        body(c, 560, 380, 520, colon=0.2)
        C(c, "THE EXPERIMENT IS OVER", 960, 150, vis(t, B(0, 0.5)), ts, size=40, bg=RED, a=1)
    def pB(c, ts):
        rect(c, 0, 880, 1920, 200, "#3a2440", 1)
        body(c, 560, 260, 620, colon=0.2)
        air_bugs(c, t, 150, 1000, 300, 880, 46, a=1, seed=4)
        for k in range(60):
            rng = random.Random(k); circle(c, rng.uniform(100, 1100), 880 + rng.uniform(4, 40), rng.uniform(3, 7), "#b9a6a0", 0.6)
        v = 37e6 * eout(prog(t, B(1, 0.1) if not short1(S) else 0.2, 1.5))
        T(c, fmt_count(v), 1450, 400, 120, ts, LIME, vis(t, 0.1 if short1(S) else B(1, 0.05)), maxw=800)
        T(c, "BACTERIA PER HOUR", 1450, 520, 44, ts, "#ffffff", vis(t, 0.3 if short1(S) else B(1, 0.15)), maxw=800)
        if not S.P:
            C(c, "ONE PERSON IN A ROOM · YALE STUDY", 1450, 680, vis(t, B(1, 0.3)), ts, size=30, dot=TEAL)
            C(c, "MUCH OF IT STIRRED UP FROM FLOOR DUST", 1450, 790, vis(t, B(1, 0.6)), ts, size=30)
    def pC(c, ts):
        plate(c, 640, 620, 330)
        air_bugs(c, t, 380, 900, 360, 620, 26, a=1, seed=7)
        T(c, "~1 MILLION", 1430, 330, 90, ts, TEAL, vis(t, B(2, 0.2)), maxw=760)
        T(c, "TO > 1 BILLION", 1430, 470, 90, ts, LIME, vis(t, B(2, 0.45)), maxw=760)
        C(c, "LIVE MICROBES IN A DAY OF MEALS", 1430, 640, vis(t, B(2, 0.3)), ts, size=32, dot=LIME)
        C(c, "DEPENDING ON THE DIET", 1430, 760, vis(t, B(2, 0.6)), ts, size=30)
    def pD(c, ts):
        g = eout(prog(t, B(3, 0.1), 3.0))
        body(c, 960, 130, 860, colon=0.6); swarm(c, t, 960, 130, 860, grow=g, seed=12)
        for k, lab in enumerate(("BREATH", "HANDSHAKE", "BITE")):
            C(c, lab, [380, 1540, 380][k], [300, 520, 740][k], vis(t, B(3, 0.05 + k * 0.15)), ts, size=36, dot=LIME)
        C(c, "RECOLONIZING… RIGHT AWAY", 1540, 860, vis(t, B(3, 0.6)), ts, size=32, bg=LIME, fg="#2a0a2c", a=1)
    if short1(S): items = [(0, pB)]
    else: items = [(0, pA), (B(1, 0), pB), (B(2, 0), pC), (B(3, 0), pD)]
    run_panels(c, W, H, t, S, items)

# ------------------------------------------------------------------ x5_recover
def x5_recover(c, W, H, t, S):
    B = beats(S, 2)
    x0, x1, y0, y1 = 260, 1700, 260, 760
    def f_div(d):
        if d < 4: return 1 - 0.65 * d / 4
        return 0.35 + 0.55 * (1 - math.exp(-(d - 4) / 13))
    def chart(c, ts, p, a=1.0):
        line(c, x0, y1, x1, y1, "#ffffff", 4, 0.8 * a); line(c, x0, y0, x0, y1, "#ffffff", 4, 0.8 * a)
        T(c, "GUT BACTERIA (VARIETY)", x0 - 10, y0 - 50, 32, ts, "#ffffff", a, w=700, fam="Inter", align="l", maxw=800)
        line(c, x0, y0 + 40, x1, y0 + 40, "#ffffff", 3, 0.35 * a, dash=([16, 12], 0))
        for d, lab in ((0, "DAY 0"), (42, "6 WEEKS"), (180, "6 MONTHS")):
            xx = x0 + (x1 - x0) * d / 180
            T(c, lab, xx, y1 + 50, 30, ts, "#cfc1d6", a, w=600, fam="Inter", maxw=300)
        pth = skia.Path(); n = 180
        for i in range(int(n * p) + 1):
            xx = x0 + (x1 - x0) * i / n; yy = y1 - (y1 - y0 - 40) * f_div(i)
            if i == 0: pth.moveTo(xx, yy)
            else: pth.lineTo(xx, yy)
        c.drawPath(pth, paint(LIME, a, stroke=10))
    def pA(c, ts):
        p = eout(prog(t, B(0, 0.15), B(0, 0.95) - B(0, 0.15)))
        chart(c, ts, p)
        capsule(c, x0 + 30, y0 + 120, 40 * eback(prog(t, B(0, 0.2), 0.4)), "", ang=20, c1=RED)
        C(c, "12 HEALTHY MEN · 4-DAY ANTIBIOTIC MIX", 1100, 120, vis(t, B(0, 0.25)), ts, size=30, dot=RED)
        if p > 0.3: C(c, "≈ 6 WEEKS: NEAR NORMAL", x0 + (x1 - x0) * 42 / 180 + 200, y0 + 220, vis(t, B(0, 0.75)), ts, size=30, bg=LIME, fg="#2a0a2c", a=1)
    def pB(c, ts):
        with Layer(c, 0.35): chart(c, ts, 1.0)
        for k in range(9):
            x = 300 + k * 165; y = 540
            circle(c, x, y, 62, "#ffffff", 0.7, stroke=4, dash=([14, 10], -t * 20))
            bug(c, x, y, 34, ["rod", "coc", "spi"][k % 3], GREY, k * 40, 0.5 * vis(t, B(1, 0.2 + k * 0.03)))
        T(c, "9 SPECIES STILL MISSING", 960, 300, 90, ts, ACCENT, vis(t, B(1, 0.35)), maxw=1600)
        C(c, "IN MOST OF THEM · 6 MONTHS LATER", 960, 800, vis(t, B(1, 0.6)), ts, size=34)
    run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB)])

# ------------------------------------------------------------------ x5_baby
def fetus(c, x, y, s, a=1.0):
    col_ = "#ffc4b4"
    oval(c, x + s * 0.15, y + s * 0.15, s * 0.75, s * 0.6, col_, a)
    circle(c, x - s * 0.35, y - s * 0.4, s * 0.48, col_, a)
    p = skia.Path(); p.moveTo(x + s * 0.4, y + s * 0.6); p.quadTo(x - s * 0.2, y + s * 0.9, x - s * 0.5, y + s * 0.3)
    c.drawPath(p, paint(mix(col_, "#c2185b", 0.2), a, stroke=s * 0.18))
    circle(c, x - s * 0.52, y - s * 0.42, s * 0.05, "#7a2a3a", a)
    circle(c, x - s * 0.05, y - s * 0.38, s * 0.1, mix(col_, "#c2185b", 0.25), a)
    oval(c, x - s * 0.25, y + s * 0.05, s * 0.2, s * 0.12, mix(col_, "#c2185b", 0.15), a)
    p2 = skia.Path(); p2.moveTo(x + s * 0.1, y + s * 0.2); p2.cubicTo(x + s * 0.6, y + s * 0.2, x + s * 0.9, y - s * 0.6, x + s * 1.35, y - s * 0.75)
    c.drawPath(p2, paint("#e88aa0", a, stroke=s * 0.07))

def x5_baby(c, W, H, t, S):
    B = beats(S, 3)
    def pA(c, ts):
        circle(c, 640, 540, 380, "#ff7a9a", 0.18, blur=40)
        circle(c, 640, 540, 340, "#5a1438", 1); circle(c, 640, 540, 340, "#ff9fb3", 0.9, stroke=10)
        fetus(c, 660, 540, 210)
        circle(c, 640, 540, 300, ICE, 0.3 * (0.6 + 0.4 * math.sin(t * 2)), stroke=4, dash=([18, 12], t * 20))
        T(c, "0", 1430, 330, 200, ts, LIME, prog(t, B(0, 0.4), 0.4), shadow=24, maxw=600)
        C(c, "LIVE BACTERIA IN THE WOMB", 1430, 500, vis(t, B(0, 0.45)), ts, size=34, dot=LIME)
        C(c, "2023 · 46 EXPERTS", 1430, 620, vis(t, B(0, 0.3)), ts, size=30)
        C(c, "YOU STARTED LIFE ESSENTIALLY STERILE", 1430, 800, vis(t, B(0, 0.75)), ts, size=28 if not S.P else 20)
    def pB(c, ts):
        oval(c, 960, 590, 130, 90, "#f4e9f0", 1); circle(c, 960, 470, 78, "#ffc4b4", 1)
        circle(c, 932, 465, 7, "#5a2a3a", 1); circle(c, 988, 465, 7, "#5a2a3a", 1)
        pm = skia.Path(); pm.addArc(skia.Rect.MakeXYWH(940, 470, 40, 28), 20, 140); c.drawPath(pm, paint("#c2185b", 1, stroke=4))
        circle(c, 915, 490, 10, "#ff9fb3", 0.6); circle(c, 1005, 490, 10, "#ff9fb3", 0.6)
        for sg, (lab1, lab2, colr) in ((-1, ("VAGINAL BIRTH", "MOTHER'S VAGINAL MICROBES", TEAL)), (1, ("C-SECTION", "MORE SKIN MICROBES", LIME))):
            p = vis(t, B(1, 0.1 if sg < 0 else 0.5))
            arrow(c, 960 + sg * 160, 540, 960 + sg * 460, 540, "#ffffff", 8, p)
            C(c, lab1, 960 + sg * 560, 330, p, ts, size=34 if not S.P else 24, dot=colr)
            C(c, lab2, 960 + sg * 560, 780, p, ts, size=28 if not S.P else 18, bg=colr, fg="#08201e", a=1)
            rng = random.Random(3 + sg)
            for k in range(int(14 * p)):
                bug(c, 960 + sg * 560 + rng.uniform(-170, 170), 560 + rng.uniform(-110, 110), 20, rng.choice(["rod", "coc"]), colr, rng.random() * 360 + t * 30, 1)
    def pC(c, ts):
        body(c, 960, 120, 860, colon=0.6); swarm(c, t, 960, 120, 860, seed=12)
        air_bugs(c, t, 400, 760, 140, 1000, 18, seed=9); air_bugs(c, t, 1160, 1520, 140, 1000, 18, seed=10)
        C(c, "DAY ONE", 380, 260, vis(t, B(2, 0.2)), ts, size=36, dot=LIME)
        C(c, "COMING AND GOING EVER SINCE", 1450, 860, vis(t, B(2, 0.55)), ts, size=30)
    run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB), (B(2, 0), pC)])

SCENES = {k: v for k, v in globals().items() if k.startswith("x5_") and callable(v)}
