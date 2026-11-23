"""Batch 06 scenes: What If You Lived in Space for 10 Years? (+ teaser, 'taller' and ozone Shorts).

Look: "station white / teal". Deep teal-black backgrounds, a glowing teal body silhouette (the motif: one
outlined human figure that puffs, stretches and fills with fluid as the timeline advances), a generic T-shaped
station in white with teal solar wings, and an on-board MISSION CLOCK (T+ days) in the top-left corner of every
long-form scene. Warnings in coral, radiation in amber. The ozone Short has its own sky-blue / violet look.
Every scene draws on a virtual 1920x1080 stage (Stage). In Shorts the stage is scaled into the 0.255H..0.58H band
and text sizes are multiplied by ts=1.75. Multi-part scenes are time-ordered panels (run_panels).
"""
from common2 import *
from functools import lru_cache
import geo
import scenes_b3_kit as kit

BG_T, BG_B = "#020b10", "#07262b"
TEAL = "#3fe0c8"; TEAL_D = "#138a80"; WHITE = "#eef7f6"; CORAL = "#ff7a6b"; FLUID = "#4fb3ff"; BONE = "#f1e4c4"
AMBER = "#ffb347"; YEL = ACCENT; MINT = "#9dffe0"; GREEN = "#6fffb0"; MARS = "#d8673a"
CHIPBG = "#0b2c31"; NAVY = "#0b1030"
PAL = dict(accent=TEAL, chip="#0d3a40", title2=ACCENT)
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

def C(c, s, x, y, p, ts, size=34, **kw):
    kw.setdefault("bg", CHIPBG)
    sz = size * ts * 1.15
    w = tw(s, sz, 700, "Inter") + 2 * sz * 0.62 + (sz * 0.9 if kw.get("dot") else 0)
    x = min(max(x, 24 + w / 2), VW - 24 - w / 2)  # keep chips on the stage
    chip(c, s, x, y, p, size * ts, **kw)

def T(c, s, x, y, size, ts, colr="#ffffff", a=1.0, w=900, maxw=1800, **kw):
    if a <= 0: return
    fam = kw.pop("fam", "Inter Display")
    sz = fit(s, maxw, size * ts, w, fam)
    if kw.get("align", "c") == "c":
        wd = tw(s, sz, w, fam); x = min(max(x, 30 + wd / 2), VW - 30 - wd / 2)
    text(c, s, x, y, sz, colr, a, w=w, fam=fam, shadow=kw.pop("shadow", 10), **kw)

def mono(c, s, x, y, size, colr, a=1.0, w=700, cell=0.62):
    """fixed-advance digits so a ticking clock doesn't jitter (left aligned)."""
    for ch in s:
        adv = size * (cell if ch.isdigit() else (0.32 if ch in ":. " else 0.62))
        text(c, ch, x + adv / 2, y, size, colr, a, w=w, fam="Inter")
        x += adv
    return x

_BG = {}
def bg_img(W, H, kind="orbit"):
    k = (W, H, kind)
    if k not in _BG:
        surf = skia.Surface(W, H); cc = surf.getCanvas()
        if kind == "orbit":
            fill_bg(cc, W, H, BG_T, BG_B)
            cc.drawPaint(paint(shader=rad(W * 0.85, H * 0.1, max(W, H) * 0.75, [(0, "#2fb8a8", 0.20), (0.5, "#0f5c5a", 0.07), (1, "#000000", 0)])))
            cc.drawPaint(paint(shader=rad(W * 0.08, H * 0.95, max(W, H) * 0.6, [(0, "#0d4a63", 0.35), (1, "#000000", 0)])))
        else:  # ozone: sky blue / violet
            fill_bg(cc, W, H, "#0a0b33", "#24105a")
            cc.drawPaint(paint(shader=rad(W * 0.8, H * 0.12, max(W, H) * 0.8, [(0, "#7fd6ff", 0.22), (0.5, "#4a5fd0", 0.08), (1, "#000000", 0)])))
            cc.drawPaint(paint(shader=rad(W * 0.1, H * 0.9, max(W, H) * 0.6, [(0, "#9b5bff", 0.30), (1, "#000000", 0)])))
        _BG[k] = surf.makeImageSnapshot()
    return _BG[k]

def bg_o(c, W, H, t, S, star_a=0.8, seed=61, kind="orbit"):
    c.drawImage(bg_img(W, H, kind), 0, 0)
    stars(c, W, H, t, star_a, seed=seed, drift=(-4, 0))

def met_hud(c, W, H, t, days):
    """on-board mission clock, top-left (long-form only)."""
    u = W / 1920
    secs = days * 86400 + t * 377  # ticks visibly fast
    d = int(secs // 86400); hh = int(secs % 86400 // 3600); mm = int(secs % 3600 // 60); ss = int(secs % 60)
    x, y = 40 * u, 34 * u
    rrect(c, x, y, 470 * u, 92 * u, 18 * u, "#03181c", 0.78)
    rrect(c, x, y, 470 * u, 92 * u, 18 * u, TEAL, 0.35, stroke=2 * u)
    text(c, "MISSION CLOCK", x + 24 * u, y + 25 * u, 19 * u, TEAL, 0.95, w=700, fam="Inter", align="l")
    mono(c, f"T+ {d:04d}d {hh:02d}:{mm:02d}:{ss:02d}", x + 22 * u, y + 60 * u, 36 * u, WHITE, 1, w=700)
    # little orbit ring: one lap = '90 minutes' (9 s here)
    ox, oy, r = x + 425 * u, y + 46 * u, 24 * u
    circle(c, ox, oy, r, TEAL, 0.5, stroke=2 * u); circle(c, ox, oy, 9 * u, "#3b8fd9", 0.9)
    an = t / 9 * 2 * math.pi
    circle(c, ox + math.cos(an) * r, oy + math.sin(an) * r, 4.5 * u, WHITE, 1)

def run_panels(c, W, H, t, S, items, seed=61, met=None, kind="orbit"):
    """items: [(t_on, fn(c, ts)), ...] in time order. Each later panel covers the previous one."""
    bg_o(c, W, H, t, S, seed=seed, kind=kind)
    for i, (t0, fn) in enumerate(items):
        t1 = items[i + 1][0] if i + 1 < len(items) else None
        if t1 is not None and t >= t1 + 0.5: continue
        a = phase(t, t0 if i > 0 else None, t1)
        if a <= 0.003: continue
        with Layer(c, a) as on:
            if not on: continue
            if i > 0 and t < t0 + 0.55: bg_o(c, W, H, t, S, seed=seed, kind=kind)
            if S.P: c.clipRect(skia.Rect.MakeLTRB(0, 0.215 * H, W, 0.59 * H))
            with Stage(c, S) as ts:
                fn(c, ts)
    if met is not None and not S.P: met_hud(c, W, H, t, met)
    kit.hook(c, W, H, t, S)

def panels_for(S, fns, E=None):
    """one panel per line (squeezed for Shorts)."""
    B = beats(S, E or len(fns))
    return [(0 if i == 0 else B(i, 0), f) for i, f in enumerate(fns)]

# ------------------------------------------------------------------ geometry helpers
def capsule(x0, y0, x1, y1, w):
    L = math.hypot(x1 - x0, y1 - y0); ang = math.degrees(math.atan2(y1 - y0, x1 - x0))
    p = skia.Path(); p.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-w / 2, -w / 2, L + w / 2, w / 2), w / 2, w / 2))
    m = skia.Matrix(); m.setRotate(ang); m.postTranslate(x0, y0)
    p.transform(m); return p

def union(paths):
    out = paths[0]
    for q in paths[1:]:
        r = skia.Op(out, q, skia.PathOp.kUnion_PathOp)
        if r is not None: out = r
    return out

# ------------------------------------------------------------------ the body silhouette (motif)
@lru_cache(maxsize=256)
def _body_path(h, puff, legs, stretch, arms, spread):
    s = h; tor = 1 + stretch
    hip = -0.47 * s
    sh = hip - 0.30 * s * tor
    hr = 0.068 * s * (1 + 0.24 * puff)
    hy = sh - 0.05 * s - hr * 0.92
    parts = []
    p = skia.Path(); p.addCircle(0, hy, hr); parts.append(p)
    parts.append(capsule(0, hy + hr * 0.6, 0, sh + 0.02 * s, 0.06 * s))
    ch = skia.Path(); ch.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-0.135 * s, sh, 0.135 * s, sh + 0.18 * s * tor), 0.05 * s, 0.05 * s)); parts.append(ch)
    ab = skia.Path(); ab.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-0.112 * s, sh + 0.12 * s * tor, 0.112 * s, hip + 0.045 * s), 0.045 * s, 0.045 * s)); parts.append(ab)
    for sg in (-1, 1):
        a0 = math.radians(8 + 55 * arms)
        sx, sy = sg * 0.118 * s, sh + 0.035 * s
        ex, ey = sx + sg * math.sin(a0) * 0.17 * s, sy + math.cos(a0) * 0.17 * s
        a1 = math.radians(4 + 70 * arms)
        hx, hy2 = ex + sg * math.sin(a1) * 0.16 * s, ey + math.cos(a1) * 0.16 * s
        parts.append(capsule(sx, sy, ex, ey, 0.056 * s)); parts.append(capsule(ex, ey, hx, hy2, 0.046 * s))
        tx = sg * 0.062 * s
        kx, ky = sg * (0.068 + 0.05 * spread) * s, hip + 0.235 * s
        fx, fy = sg * (0.072 + 0.09 * spread) * s, -0.025 * s
        parts.append(capsule(tx, hip + 0.01 * s, kx, ky, 0.098 * s * legs)); parts.append(capsule(kx, ky, fx, fy, 0.072 * s * legs))
        parts.append(capsule(fx, fy, fx + sg * 0.03 * s, fy + 0.012 * s, 0.045 * s))
    return union(parts), dict(hy=hy, hr=hr, sh=sh, hip=hip)

def body(c, x, yf, h, a=1.0, puff=0.0, legs=1.0, stretch=0.0, arms=0.0, spread=0.0, rot=0.0, fill="#0d3b40", edge=TEAL,
         fluid=None, glow=0.6, highlight=None, spine=0.0):
    """Outlined human silhouette standing on (x, yf), height h. fluid: 0 legs-heavy .. 1 head-heavy (blue tint).
    highlight: list of (part, colour, alpha) with part in neck/back/thigh/calf/lowback. Returns anchors (screen)."""
    if a <= 0: return None
    q = lambda v, k=50: round(v * k) / k
    path, an = _body_path(round(h), q(puff), q(legs), q(stretch, 200), q(arms), q(spread))
    c.save(); c.translate(x, yf)
    if rot: c.translate(0, -h * 0.5); c.rotate(rot); c.translate(0, h * 0.5)
    if glow: c.drawPath(path, paint(edge, 0.35 * glow * a, stroke=h * 0.03, blur=h * 0.02))
    c.drawPath(path, paint(fill, 0.92 * a))
    if fluid is not None:
        c.save(); c.clipPath(path, doAntiAlias=True)
        top, bot = an["hy"] - an["hr"], 0
        f = clamp(fluid)
        c.drawRect(skia.Rect.MakeLTRB(-h, top, h, bot), paint(shader=lin(0, top, 0, bot, [
            (0, FLUID, a * lerp(0.10, 0.85, f)), (0.45, FLUID, a * lerp(0.25, 0.45, f)), (1, FLUID, a * lerp(0.85, 0.12, f))])))
        c.restore()
    if highlight:
        c.save(); c.clipPath(path, doAntiAlias=True)
        s = h
        for part, colr, al in highlight:
            if al <= 0: continue
            if part == "calf":
                for sg in (-1, 1): oval(c, sg * 0.09 * s, -0.13 * s, 0.05 * s, 0.11 * s, colr, al * a, blur=s * 0.01)
            elif part == "thigh":
                for sg in (-1, 1): oval(c, sg * 0.075 * s, an["hip"] + 0.12 * s, 0.06 * s, 0.12 * s, colr, al * a, blur=s * 0.01)
            elif part == "back":
                for sg in (-1, 1): oval(c, sg * 0.07 * s, an["sh"] + 0.13 * s, 0.05 * s, 0.13 * s, colr, al * a, blur=s * 0.012)
            elif part == "lowback":
                oval(c, 0, an["hip"] - 0.03 * s, 0.11 * s, 0.07 * s, colr, al * a, blur=s * 0.015)
            elif part == "neck":
                oval(c, 0, an["sh"] - 0.015 * s, 0.05 * s, 0.04 * s, colr, al * a, blur=s * 0.01)
        c.restore()
    if spine > 0:
        n = 12; y0, y1 = an["sh"] - 0.01 * h, an["hip"] - 0.005 * h
        for k in range(n):
            yy = lerp(y0, y1, (k + 0.5) / n); hh = (y1 - y0) / n * 0.62
            rrect(c, -0.018 * h, yy - hh / 2, 0.036 * h, hh, hh * 0.3, BONE, spine * a * 0.9)
    c.drawPath(path, paint(edge, 0.95 * a, stroke=max(2.0, h * 0.006)))
    c.restore()
    return dict(head=(x, yf + an["hy"], an["hr"]), sh=yf + an["sh"], hip=yf + an["hip"], top=yf + an["hy"] - an["hr"])

# ------------------------------------------------------------------ props
def station(c, x, y, s, t=0.0, a=1.0, rot=0.0):
    """generic T-shaped space station: two lab modules across a node, core module as the stem, big solar wings."""
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(rot)
    def wing(cx, cy, w, hh):
        rrect(c, cx - w / 2, cy - hh / 2, w, hh, 4, "#0f4f6a", a)
        for k in range(1, 6): line(c, cx - w / 2 + w * k / 6, cy - hh / 2, cx - w / 2 + w * k / 6, cy + hh / 2, TEAL, max(1, s * 0.006), a * 0.55)
        line(c, cx - w / 2, cy, cx + w / 2, cy, TEAL, max(1, s * 0.006), a * 0.55)
        rrect(c, cx - w / 2, cy - hh / 2, w, hh, 4, TEAL, a * 0.9, stroke=max(1.5, s * 0.008))
    # wings at the ends of the cross-bar
    for sg in (-1, 1):
        line(c, sg * 0.62 * s, 0, sg * 0.62 * s, -0.42 * s, "#b9c8cc", max(2, s * 0.012), a)
        line(c, sg * 0.62 * s, 0, sg * 0.62 * s, 0.42 * s, "#b9c8cc", max(2, s * 0.012), a)
        wing(sg * 0.62 * s, -0.28 * s, 0.2 * s, 0.26 * s); wing(sg * 0.62 * s, 0.28 * s, 0.2 * s, 0.26 * s)
    # core module (stem) with its own small wings
    rrect(c, -0.09 * s, 0, 0.18 * s, 0.62 * s, 0.07 * s, "#dfe8ea", a)
    for sg in (-1, 1): wing(sg * 0.22 * s, 0.42 * s, 0.24 * s, 0.1 * s)
    line(c, -0.34 * s, 0.42 * s, 0.34 * s, 0.42 * s, "#b9c8cc", max(2, s * 0.01), a)
    # cross-bar labs
    rrect(c, -0.6 * s, -0.08 * s, 1.2 * s, 0.16 * s, 0.07 * s, "#eef3f4", a)
    for xx in (-0.4, -0.2, 0.2, 0.4): line(c, xx * s, -0.08 * s, xx * s, 0.08 * s, "#9fb2b7", max(1, s * 0.006), a)
    c.drawRect(skia.Rect.MakeLTRB(-0.6 * s, -0.08 * s, 0.6 * s, 0.08 * s), paint(shader=lin(0, -0.08 * s, 0, 0.08 * s, [(0, "#ffffff", 0.0), (1, "#000000", 0.35)]), a=a))
    circle(c, 0, 0, 0.13 * s, "#f4f8f9", a); circle(c, 0, 0, 0.13 * s, "#9fb2b7", a, stroke=max(1, s * 0.008))
    circle(c, 0, 0, 0.05 * s, TEAL, a * (0.6 + 0.4 * math.sin(t * 3)))
    # visiting capsule at the bottom of the stem
    rrect(c, -0.06 * s, 0.62 * s, 0.12 * s, 0.14 * s, 0.03 * s, "#cfd9db", a)
    c.restore()

def suit(c, x, y, s, a=1.0, hl=0.0, dim=0.0):
    """generic astronaut icon (no face): big helmet with a gold visor, backpack, arms. y = centre of torso."""
    if a <= 0: return
    al = a * (1 - 0.6 * dim)
    if hl > 0: circle(c, x, y - s * 0.2, s * 1.15, YEL, 0.25 * hl * a, blur=s * 0.25)
    rrect(c, x - s * 0.62, y - s * 0.55, s * 1.24, s * 1.05, s * 0.2, "#9fb0b4", al)          # backpack
    for sg in (-1, 1):
        c.drawPath(capsule(x + sg * s * 0.5, y - s * 0.25, x + sg * s * 0.62, y + s * 0.45, s * 0.3), paint("#e4ebed", al))
    rrect(c, x - s * 0.48, y - s * 0.4, s * 0.96, s * 1.15, s * 0.3, "#f1f5f6", al)          # torso
    rect(c, x - s * 0.22, y + s * 0.02, s * 0.44, s * 0.24, "#6f8a90", al)
    circle(c, x - s * 0.1, y + s * 0.14, s * 0.05, CORAL, al); circle(c, x + s * 0.1, y + s * 0.14, s * 0.05, TEAL, al)
    circle(c, x, y - s * 0.72, s * 0.5, "#f1f5f6", al)                                       # helmet
    circle(c, x, y - s * 0.72, s * 0.5, "#b9c8cc", al, stroke=s * 0.05)
    c.drawOval(skia.Rect.MakeLTRB(x - s * 0.36, y - s * 0.98, x + s * 0.36, y - s * 0.5),
               paint(shader=lin(x - s * 0.3, y - s * 0.95, x + s * 0.3, y - s * 0.5, [(0, "#ffe08a", 1), (0.55, "#c98a1e", 1), (1, "#6b4a10", 1)]), a=al))
    oval(c, x - s * 0.14, y - s * 0.84, s * 0.1, s * 0.06, "#ffffff", al * 0.7)
    if hl > 0: circle(c, x, y - s * 0.2, s * 1.1, YEL, hl * a, stroke=s * 0.06)

def rocket(c, x, y, s, t, a=1.0, flame=1.0, gantry=0.0):
    """generic white launcher, base at (x, y)."""
    if a <= 0: return
    if gantry > 0:
        rect(c, x + s * 0.55, y - s * 3.1, s * 0.28, s * 3.1, "#3d4f55", a * gantry)
        for k in range(12): line(c, x + s * 0.55, y - k * s * 0.26, x + s * 0.83, y - (k + 1) * s * 0.26, "#6b8187", s * 0.03, a * gantry)
        rect(c, x - s * 1.2, y, s * 2.6, s * 0.18, "#3d4f55", a)
    if flame > 0:
        for k, (colr, L) in enumerate([("#ff6b1a", 1.6), ("#ffb347", 1.15), ("#fff2c0", 0.7)]):
            fl = L * (1 + 0.1 * math.sin(t * 23 + k))
            c.drawPath(poly([(x - s * 0.22, y), (x, y + s * fl * flame), (x + s * 0.22, y)]), paint(colr, a))
    for sg in (-1, 1):
        rrect(c, x + sg * s * 0.3 - s * 0.1, y - s * 1.1, s * 0.2, s * 1.1, s * 0.06, "#dfe7e9", a)
        c.drawPath(poly([(x + sg * s * 0.3 - s * 0.1, y - s * 1.1), (x + sg * s * 0.3, y - s * 1.35), (x + sg * s * 0.3 + s * 0.1, y - s * 1.1)]), paint("#dfe7e9", a))
    rrect(c, x - s * 0.18, y - s * 2.6, s * 0.36, s * 2.6, s * 0.06, "#f4f7f8", a)
    rect(c, x - s * 0.18, y - s * 1.9, s * 0.36, s * 0.08, CORAL, a)
    c.drawPath(poly([(x - s * 0.2, y - s * 2.6), (x - s * 0.2, y - s * 3.0), (x, y - s * 3.35), (x + s * 0.2, y - s * 3.0), (x + s * 0.2, y - s * 2.6)]), paint("#ffffff", a))
    line(c, x, y - s * 3.35, x, y - s * 3.75, "#c9d3d6", s * 0.04, a)

def capsule_chute(c, x, y, s, a=1.0, t=0.0):
    sw = math.sin(t * 1.5) * 3
    c.save(); c.translate(x, y); c.rotate(sw)
    p = skia.Path(); p.addArc(skia.Rect.MakeLTRB(-s * 1.4, -s * 3.2, s * 1.4, -s * 1.0), 180, 180); p.close()
    c.drawPath(p, paint("#ff8a5c", a))
    for k in range(-3, 4):
        if k: line(c, k * s * 0.4, -s * 2.1, k * s * 0.4, -s * 2.15 + abs(k) * s * 0.05, "#ffffff", s * 0.06, a * 0.8)
    for sg in (-1, 1): line(c, sg * s * 1.35, -s * 2.1, sg * s * 0.35, -s * 0.15, "#e9eef0", max(1.5, s * 0.03), a)
    line(c, 0, -s * 3.1, 0, -s * 2.1, "#ffffff", s * 0.05, a * 0.6)
    c.drawPath(poly([(-s * 0.45, 0), (-s * 0.25, -s * 0.5), (s * 0.25, -s * 0.5), (s * 0.45, 0)]), paint("#6f7d80", a))
    rrect(c, -s * 0.5, -s * 0.05, s * 1.0, s * 0.16, s * 0.06, "#3b2d28", a)
    c.restore()

@lru_cache(maxsize=12)
def globe_skimg(R, rot, tilt, light=(-0.75, 0.35, 0.55)):
    R = max(4, int(R) // 4 * 4)
    img = geo.globe_img(R, rot, tilt, "earth", light)
    return skia.Image.fromarray(img, colorType=skia.kRGBA_8888_ColorType, alphaType=skia.kPremul_AlphaType)

def globe_c(c, x, y, R, rot=40, tilt=18, spin=0.0, a=1.0, glow=1.0, light=(-0.75, 0.35, 0.55)):
    """cached globe image; 'spin' rotates the picture (fine for slow drifts)."""
    if a <= 0: return
    img = globe_skimg(int(R), rot, tilt, light); R = max(4, int(R) // 4 * 4)
    if glow: circle(c, x, y, R * 1.07, "#6fd6ff", 0.32 * glow * a, blur=R * 0.06)
    c.save(); c.translate(x, y); c.rotate(spin)
    p = skia.Paint(); p.setAlphaf(clamp(a))
    c.drawImageRect(img, skia.Rect.MakeXYWH(-R, -R, 2 * R, 2 * R), skia.SamplingOptions(skia.FilterMode.kLinear), p)
    c.restore()

def earth_limb(c, t, a=1.0, cy=2200, R=1400):
    globe_c(c, 960, cy, R, rot=-20, tilt=40, spin=-t * 0.5, a=a, glow=1.2, light=(0.0, 0.7, 0.7))
    c.drawCircle(960, cy, R + 6, paint("#8fe8ff", 0.5 * a, stroke=10, blur=8))

def mars_d(c, x, y, R, a=1.0):
    if a <= 0: return
    circle(c, x, y, R * 1.15, "#ff8a5c", 0.18 * a, blur=R * 0.15)
    circle(c, x, y, R, MARS, a)
    rng = random.Random(9)
    for _ in range(7):
        an = rng.random() * 6.28; d = rng.random() ** 0.7 * R * 0.7
        circle(c, x + math.cos(an) * d, y + math.sin(an) * d, R * rng.uniform(0.08, 0.2), "#a8462a", a * 0.7)
    oval(c, x, y - R * 0.86, R * 0.35, R * 0.1, "#f6efe8", a * 0.9)
    c.drawCircle(x, y, R, paint(shader=rad(x - R * 0.35, y - R * 0.35, R * 1.6, [(0, "#ffffff", 0.15), (1, "#000000", 0.55)]), a=a))

def porthole(c, x, y, r, t, a=1.0, inner=None, ticks=True, clock=None):
    """the motif frame: a station window that doubles as an on-board clock dial."""
    if a <= 0: return
    circle(c, x, y, r * 1.12, TEAL, 0.10 * a, blur=r * 0.12)
    circle(c, x, y, r, "#03161a", 0.9 * a)
    c.drawCircle(x, y, r, paint(shader=rad(x - r * 0.3, y - r * 0.4, r * 1.4, [(0, "#1c6b6e", 0.55), (1, "#02090c", 0.0)]), a=a))
    if inner:
        c.save(); pth = skia.Path(); pth.addCircle(x, y, r * 0.97); c.clipPath(pth, doAntiAlias=True); inner(); c.restore()
    c.drawCircle(x, y, r, paint("#cfe0e2", 0.95 * a, stroke=r * 0.07))
    c.drawCircle(x, y, r * 1.045, paint("#6b8a8f", 0.9 * a, stroke=r * 0.025))
    for k in range(8):
        an = k / 8 * 2 * math.pi + 0.2
        circle(c, x + math.cos(an) * r * 1.0, y + math.sin(an) * r * 1.0, r * 0.018, "#5d7479", a)
    if ticks:
        for k in range(60):
            an = k / 60 * 2 * math.pi
            L = 0.06 if k % 5 == 0 else 0.03
            line(c, x + math.cos(an) * r * 1.09, y + math.sin(an) * r * 1.09, x + math.cos(an) * r * (1.09 + L), y + math.sin(an) * r * (1.09 + L),
                 TEAL, max(1.5, r * (0.012 if k % 5 == 0 else 0.006)), a * 0.8)
    if clock is not None:  # sweeping hand around the rim
        an = -math.pi / 2 + clock * 2 * math.pi
        arc = skia.Path(); arc.addArc(skia.Rect.MakeLTRB(x - r * 1.2, y - r * 1.2, x + r * 1.2, y + r * 1.2), -90, 360 * (clock % 1))
        c.drawPath(arc, paint(YEL, 0.9 * a, stroke=r * 0.025))
        circle(c, x + math.cos(an) * r * 1.2, y + math.sin(an) * r * 1.2, r * 0.035, YEL, a)

def motif_o(c, W, H, t, S, cx, cy, s):
    u = S.u * s; r = 250 * u * (1.15 if S.P else 1)
    def inner():
        globe_c(c, cx + r * 0.25, cy + r * 1.55, r * 0.95, rot=10, tilt=30, spin=-t * 2, glow=0.8, light=(0.2, 0.8, 0.6))
        body(c, cx, cy + r * 0.5 + math.sin(t * 0.9) * r * 0.03, r * 0.98, puff=0.6, legs=0.75, arms=0.55, spread=0.5,
             rot=-12 + 7 * math.sin(t * 0.7), fluid=0.8, glow=0.8)
    rx, ry = r * 1.75, r * 0.42
    an = t * 0.6
    sx, sy = cx + math.cos(an) * rx, cy + math.sin(an) * ry
    ring = skia.Rect.MakeLTRB(cx - rx, cy - ry, cx + rx, cy + ry)
    c.drawOval(ring, paint(TEAL, 0.35, stroke=2.5 * u, dash=([14 * u, 12 * u], -t * 20)))
    if math.sin(an) <= 0: station(c, sx, sy, 70 * u, t)
    porthole(c, cx, cy, r, t, inner=inner, clock=t / 8)
    if math.sin(an) > 0: station(c, sx, sy, 70 * u, t)

def bg_title(c, W, H, t, S): bg_o(c, W, H, t, S)

def or6_title(c, W, H, t, S): kit.title(c, W, H, t, S, bg_title, motif_o, PAL)

def or6_card(c, W, H, t, S):
    def cbg(c, W, H, t, S):
        bg_o(c, W, H, t, S)
        with Layer(c, 0.35):
            motif_o(c, W, H, t, S, W / 2, H / 2, 1.25 if not S.P else 0.9)
    kit.card(c, W, H, t, S, cbg, PAL)
    if not S.P: met_hud(c, W, H, t, S.opts.get("met", 0))

def or6_end(c, W, H, t, S): kit.end(c, W, H, t, S, bg_title, motif_o, PAL)
def or6_endshort(c, W, H, t, S): kit.end_short(c, W, H, t, S, bg_title, motif_o, PAL)

# ================================================================== HOOK
def or6_hook(c, W, H, t, S):
    nb = 3 if S.n() >= 3 else 1; B = beats(S, nb)
    def pA(c, ts):
        earth_limb(c, t)
        sx = lerp(260, 1150, t / max(S.dur, 1))
        station(c, sx, 430, 190, t, rot=-6)
        C(c, "SHENZHOU-23 · LAUNCHED 24 MAY 2026", 1430, 160, vis(t, B(0, 0.1)), ts, size=34, dot=TEAL)
        C(c, "PLANNED STAY: ~6 MONTHS", 1430, 250, vis(t, B(0, 0.55)), ts, size=34, dot=WHITE)
        t1 = B(1, 0.0); t2 = B(1, 0.35)
        for k, x in enumerate((1380, 1530, 1680)):
            p = vis(t, t1 + 0.15 * k)
            if p <= 0: continue
            leave = ease(prog(t, t2, 1.2)) if k != 1 else 0
            suit(c, x, 560 + leave * 60, 52, a=p * (1 - 0.65 * leave), hl=ease(prog(t, t2, 0.6)) if k == 1 else 0)
        C(c, "STAYS ~1 YEAR", 1530, 720, vis(t, t2 + 0.3), ts, size=40, bg=YEL, fg=NAVY, a=1)
        C(c, "CHINA'S FIRST", 1530, 810, vis(t, B(1, 0.75)), ts, size=32)
    def pB(c, ts):
        r = 270 if not S.P else 330
        cx = 560 if not S.P else 960
        def inner():
            globe_c(c, cx + r * 0.25, 560 + r * 1.55, r * 0.95, rot=10, tilt=30, spin=-t * 2, glow=0.8, light=(0.2, 0.8, 0.6))
            body(c, cx, 560 + r * 0.5, r * 0.98, puff=0.6, legs=0.75, arms=0.55, spread=0.5, rot=-12 + 7 * math.sin(t * 0.7), fluid=0.8)
        porthole(c, cx, 560 - (0 if not S.P else 20), r, t, inner=inner, clock=(t - (B(2, 0) if nb == 3 else 0)) / 2.2)
        if not S.P:
            p1 = vis(t, B(2, 0.05)); p2 = vis(t, B(2, 0.45))
            T(c, "1 YEAR", 1360, 400, 120, ts, WHITE, p1, maxw=700)
            if p2 > 0: line(c, 1170, 400, 1550, 400, CORAL, 12, p2)
            T(c, "10 YEARS?", 1360, 600, 170, ts, YEL, p2, maxw=880, shadow=16)
    if nb == 3: run_panels(c, W, H, t, S, [(0, pA), (B(2, 0), pB)])
    else: run_panels(c, W, H, t, S, [(0, pB)])

# ================================================================== NEWS
def crew_row(c, t, ts, x, y, name, role, p, extra=None):
    if p <= 0: return
    suit(c, x, y + 14, 58, a=p)
    T(c, name, x + 80, y - 18, 56, ts, WHITE, p, align="l", maxw=760)
    text(c, role, x + 80, y + 38, 32 * ts, TEAL, p, w=700, fam="Inter", align="l")
    if extra: C(c, extra, x + 80 + tw(role, 32 * ts, 700, "Inter") + 200, y + 38, p, ts, size=26, bg=YEL, fg=NAVY, a=1)

def or6_news(c, W, H, t, S):
    B = beats(S, 4)
    def pA(c, ts):
        lift = eout(prog(t, 0.6, 5.0))
        y0 = 880 - lift * 420
        smoke(c, 330, y0 + 40, t, 1, a=0.7 * lift, seed=3, n=10, col_="#9fb2b7", rise=200)
        rocket(c, 330, y0, 95, t, flame=0.4 + 0.6 * lift)
        C(c, "SHENZHOU-23", 330, 930, vis(t, B(0, 0.02)), ts, size=40, dot=TEAL)
        C(c, "24 MAY 2026", 330, 1020, vis(t, B(0, 0.1)), ts, size=36, bg=YEL, fg=NAVY, a=1)
        crew_row(c, t, ts, 800, 330, "ZHU YANGZHU", "COMMANDER", vis(t, B(0, 0.3)))
        crew_row(c, t, ts, 800, 560, "ZHANG ZHIYUAN", "PILOT", vis(t, B(0, 0.42)))
        crew_row(c, t, ts, 800, 790, "LAI KA-YING", "PAYLOAD SPECIALIST", vis(t, B(0, 0.55)), extra="FIRST FROM HONG KONG")
    def pB(c, ts):
        T(c, "ONE OF THREE STAYS ABOUT A YEAR", 960, 150, 66, ts, WHITE, vis(t, B(1, 0.0)))
        x0, x1 = 420, 1720
        months = ["MAY", "AUG", "NOV", "FEB", "MAY"]
        for k, m in enumerate(months):
            xx = lerp(x0, x1, k / 4)
            line(c, xx, 300, xx, 820, "#ffffff", 2, 0.15)
            text(c, m, xx, 290, 28, "#b8d8d6", 0.9, w=700, fam="Inter")
        text(c, "2026", lerp(x0, x1, 0.12), 860, 26, "#7fa9a6", 0.9, w=600, fam="Inter")
        text(c, "2027", lerp(x0, x1, 0.88), 860, 26, "#7fa9a6", 0.9, w=600, fam="Inter")
        g = ease(prog(t, B(1, 0.1), 2.5))
        for k, y in enumerate((420, 570, 720)):
            suit(c, 300, y + 8, 36)
            end = 0.5 if k < 2 else 1.0
            e = lerp(0, end, g) if k < 2 else lerp(0, 0.5, g) + 0.5 * ease(prog(t, B(1, 0.45), 1.6))
            w_ = (x1 - x0) * e
            if w_ > 2:
                if k < 2: rrect(c, x0, y - 22, w_, 44, 22, TEAL, 0.9)
                else:
                    rrect(c, x0, y - 22, min(w_, (x1 - x0) * 0.5), 44, 22, TEAL, 0.9)
                    if w_ > (x1 - x0) * 0.5:
                        rrect(c, x0 + (x1 - x0) * 0.5 - 22, y - 22, w_ - (x1 - x0) * 0.5 + 22, 44, 22, YEL, 0.95)
        C(c, "~6 MONTHS", lerp(x0, x1, 0.25), 495, vis(t, B(1, 0.3)), ts, size=26)
        C(c, "~1 YEAR", lerp(x0, x1, 0.75), 795, vis(t, B(1, 0.7)), ts, size=30, bg=YEL, fg=NAVY, a=1)
        C(c, "CHINA MANNED SPACE AGENCY · 23 MAY 2026", 960, 960, vis(t, B(1, 0.5)), ts, size=26)
    def pC(c, ts):
        for k, x in enumerate((640, 960, 1280)):
            suit(c, x, 560, 95, hl=0.5 + 0.5 * math.sin(t * 3 - k * 2.1))
            ph = 0.5 + 0.5 * math.sin(t * 3 - k * 2.1)
            T(c, "?", x, 330 - ph * 14, 110, ts, YEL, 0.5 + 0.5 * ph, maxw=200)
        C(c, "WHICH ONE? NOT ANNOUNCED", 960, 820, vis(t, B(2, 0.1)), ts, size=40, bg=YEL, fg=NAVY, a=1)
        C(c, "CHOICE DEPENDS ON HOW THE MISSION GOES", 960, 920, vis(t, B(2, 0.5)), ts, size=28)
    def pD(c, ts):
        rocket(c, 520, 930, 118, t, flame=0, gantry=1.0)
        C(c, "SHENZHOU-24", 1350, 200, vis(t, B(3, 0.0)), ts, size=40, dot=TEAL)
        C(c, "ON THE PAD SINCE 17 NOV", 1350, 300, vis(t, B(3, 0.12)), ts, size=34)
        C(c, "FIRST FOREIGN VISITOR: PAKISTAN", 1350, 430, vis(t, B(3, 0.35)), ts, size=34, dot=YEL)
        C(c, "STAY: ABOUT 1 WEEK", 1350, 530, vis(t, B(3, 0.45)), ts, size=34)
        stamp(c, "NOT LAUNCHED YET", 1350, 730, prog(t, B(3, 0.75), 0.4), 1, color=CORAL, rot=-6, size=64)
        text(c, "AS OF 23 NOV 2026", 1350, 860, 30, "#b8d8d6", prog(t, B(3, 0.85), 0.4), w=700, fam="Inter")
    run_panels(c, W, H, t, S, panels_for(S, [pA, pB, pC, pD]))

# ================================================================== RULES
def or6_rules(c, W, H, t, S):
    B = beats(S, 4)
    def pA(c, ts):
        station(c, 960, 500, 460, t, rot=3 * math.sin(t * 0.4))
        for k, (s_, x, y, dot) in enumerate((("FOOD", 330, 220, YEL), ("AIR", 1590, 220, MINT), ("WATER", 330, 860, FLUID), ("GYM", 1590, 860, CORAL))):
            C(c, s_, x, y, vis(t, B(0, 0.45 + 0.12 * k)), ts, size=44, dot=dot)
        C(c, "A STATION IN LOW ORBIT", 960, 980, vis(t, B(0, 0.15)), ts, size=32)
    def pB(c, ts):
        globe_c(c, 960, 560, 300, rot=60, tilt=20, spin=t * 0.8)
        rx, ry = 470, 120
        c.save(); c.translate(960, 560); c.rotate(-12)
        c.drawOval(skia.Rect.MakeLTRB(-rx, -ry, rx, ry), paint(TEAL, 0.5, stroke=3, dash=([16, 12], -t * 20)))
        an = t * 1.2; station(c, math.cos(an) * rx, math.sin(an) * ry, 60, t)
        c.restore()
        T(c, "NEVER COME DOWN", 960, 150, 92, ts, WHITE, vis(t, B(1, 0.05)))
        C(c, "10 YEARS · NO TRIPS HOME", 960, 960, vis(t, B(1, 0.3)), ts, size=36, bg=YEL, fg=NAVY, a=1)
    def pC(c, ts):
        ox, oy, r = 700, 560, 300
        sun(c, 150, 560, 55, t, glow=0.7)
        c.drawRect(skia.Rect.MakeLTRB(ox, oy - 330, ox + 420, oy + 330), paint(shader=lin(ox, 0, ox + 420, 0, [(0, "#000000", 0.0), (0.2, "#000000", 0.0), (1, "#000000", 0.0)])))
        globe_c(c, ox, oy, 160, rot=80, tilt=15, spin=t * 2, light=(-1, 0, 0.3))
        circle(c, ox, oy, r, TEAL, 0.4, stroke=3, dash=([12, 10], 0))
        t0 = B(2, 0.0); per = 1.6
        an = math.pi + (t - t0) / per * 2 * math.pi
        sx, sy = ox + math.cos(an) * r, oy + math.sin(an) * r
        lit = math.cos(an) < 0.2
        station(c, sx, sy, 70, t, rot=math.degrees(an) + 90)
        if lit: circle(c, sx, sy, 50, YEL, 0.25, blur=16)
        n = int(clamp((t - t0) / per, 0, 16)) if t > t0 else 0
        if t < B(2, 0.62):
            T(c, f"{n}", 1450, 470, 220, ts, YEL, vis(t, t0), maxw=500)
            T(c, "SUNRISES TODAY", 1450, 650, 54, ts, WHITE, vis(t, t0))
            C(c, "ONE LAP ≈ 90 MINUTES", 1450, 780, vis(t, B(2, 0.12)), ts, size=32)
        else:
            p = vis(t, B(2, 0.62))
            T(c, "≈58,000", 1450, 470, 190, ts, YEL, p, maxw=760)
            T(c, "SUNRISES IN 10 YEARS", 1450, 650, 54, ts, WHITE, p)
            C(c, "ROUGH MATH: 16 × 3,652 DAYS", 1450, 780, p, ts, size=30)
    def pD(c, ts):
        ex, ey, mx = 330, 560, 1600
        globe_c(c, ex, ey, 110, rot=30, tilt=15, spin=t)
        moon(c, mx, ey, 34)
        line(c, ex + 130, ey - 50, mx - 50, ey - 50, TEAL, 4, 0.8, dash=([18, 12], -t * 40))
        line(c, mx - 50, ey + 50, ex + 130, ey + 50, TEAL, 4, 0.8, dash=([18, 12], -t * 40))
        arrow(c, mx - 120, ey - 50, mx - 50, ey - 50, TEAL, 4, 0.9); arrow(c, ex + 200, ey + 50, ex + 130, ey + 50, TEAL, 4, 0.9)
        q = ((t - B(3, 0)) / 3.0) % 1 if t > B(3, 0) else 0
        px = lerp(ex + 130, mx - 50, q * 2) if q < 0.5 else lerp(mx - 50, ex + 130, (q - 0.5) * 2)
        py = ey - 50 if q < 0.5 else ey + 50
        station(c, px, py, 46, t)
        T(c, "EVERY DAY ≈ TO THE MOON AND BACK", 960, 260, 62, ts, WHITE, vis(t, B(3, 0.05)))
        C(c, "~16 LAPS OF THE PLANET", 960, 820, vis(t, B(3, 0.4)), ts, size=34)
    run_panels(c, W, H, t, S, panels_for(S, [pA, pB, pC, pD]), met=0)

# ================================================================== DAY 1: FLUID SHIFT
def or6_fluid(c, W, H, t, S):
    B = beats(S, 3)
    def pA(c, ts):
        f = ease(prog(t, B(1, 0.15), max(0.6, B(1, 0.85) - B(1, 0.15))))
        pf = ease(prog(t, B(2, 0.0), 1.4))
        # ground body
        line(c, 330, 950, 790, 950, "#5d7a7e", 4, 0.9)
        body(c, 560, 945, 720, fluid=0.0, glow=0.4, edge="#7fb8b2")
        text(c, "ON EARTH", 560, 1010, 34 * ts if not S.P else 50, "#b8d8d6", vis(t, B(0, 0.1)), w=700, fam="Inter")
        bob = math.sin(t * 0.9) * 14
        body(c, 1220, 935 + bob, 720, fluid=f, puff=pf, legs=1 - 0.4 * pf, arms=0.35, spread=0.3, rot=-4 + 3 * math.sin(t * 0.6))
        text(c, "IN ORBIT", 1220, 1010, 34 * ts if not S.P else 50, TEAL, vis(t, B(0, 0.1)), w=700, fam="Inter")
        pa = vis(t, B(1, 0.15)) * (1 - prog(t, B(2, 0.5), 0.5))
        for k, xx in enumerate((1030, 1410)):
            yy = 820 - ((t * 120 + k * 90) % 300)
            arrow(c, xx, yy + 90, xx, yy, FLUID, 9, pa)
        C(c, "≈2 LITERS UPWARD", 1650, 470, vis(t, B(1, 0.45)), ts, size=36, bg=FLUID, fg=NAVY, a=1)
        C(c, "PUFFY FACE", 1650, 230, vis(t, B(2, 0.25)), ts, size=36, dot=CORAL)
        C(c, "BIRD LEGS", 1650, 760, vis(t, B(2, 0.5)), ts, size=36, dot=CORAL)
    run_panels(c, W, H, t, S, [(0, pA)], met=0.1)

# ================================================================== SPACE MOTION SICKNESS
def head_side(c, x, y, r, a=1.0, glow_brain=0.0, t=0.0):
    p = skia.Path()
    p.moveTo(x - r * 0.9, y + r * 0.2)
    p.cubicTo(x - r * 1.05, y - r * 0.9, x + r * 0.5, y - r * 1.25, x + r * 0.85, y - r * 0.35)
    p.lineTo(x + r * 1.02, y + r * 0.05); p.lineTo(x + r * 0.9, y + r * 0.15)
    p.cubicTo(x + r * 0.95, y + r * 0.4, x + r * 0.8, y + r * 0.55, x + r * 0.55, y + r * 0.62)
    p.lineTo(x + r * 0.5, y + r * 0.95); p.lineTo(x - r * 0.25, y + r * 1.05)
    p.cubicTo(x - r * 0.3, y + r * 0.7, x - r * 0.7, y + r * 0.6, x - r * 0.9, y + r * 0.2); p.close()
    c.drawPath(p, paint(TEAL, 0.3 * a, stroke=r * 0.05, blur=r * 0.03))
    c.drawPath(p, paint("#0d3b40", 0.95 * a)); c.drawPath(p, paint(TEAL, a, stroke=max(2, r * 0.015)))
    # brain
    bx, by = x - r * 0.05, y - r * 0.35
    for dx, dy, rr in [(-0.35, 0.05, 0.3), (-0.05, -0.18, 0.33), (0.3, -0.05, 0.28), (0.0, 0.15, 0.3), (-0.3, 0.25, 0.22)]:
        dx, dy, rr = dx * 0.75, dy * 0.75, rr * 0.75
        circle(c, bx + dx * r, by + dy * r, rr * r, mix("#e39aa6", CORAL, glow_brain), a * 0.9)
    if glow_brain > 0: circle(c, bx, by, r * 0.6, CORAL, 0.35 * glow_brain * a * (0.6 + 0.4 * math.sin(t * 8)), blur=r * 0.15)
    return (bx, by)

def ear_spiral(c, x, y, r, a=1.0, colr=YEL):
    p = skia.Path(); p.moveTo(x + r, y)
    for k in range(1, 60):
        an = k / 59 * 4 * math.pi; rr = r * (1 - k / 70)
        p.lineTo(x + math.cos(an) * rr, y + math.sin(an) * rr)
    c.drawPath(p, paint(colr, a, stroke=max(2, r * 0.18)))

def eye_icon(c, x, y, r, a=1.0):
    p = skia.Path(); p.moveTo(x - r, y); p.quadTo(x, y - r * 0.8, x + r, y); p.quadTo(x, y + r * 0.8, x - r, y); p.close()
    c.drawPath(p, paint("#ffffff", a)); circle(c, x, y, r * 0.38, "#2a8fbf", a); circle(c, x, y, r * 0.17, NAVY, a)

def or6_sick(c, W, H, t, S):
    B = beats(S, 3)
    def pA(c, ts):
        fr = ease(prog(t, B(0, 0.2), 1.5))
        donut(c, 600, 540, 230, 0.6 * fr, TEAL, 1)
        p2 = skia.Path(); p2.addArc(skia.Rect.MakeXYWH(370, 310, 460, 460), -90 + 216 * fr, 72 * fr)
        c.drawPath(p2, paint(TEAL, 0.45, stroke=230 * 0.28, cap="butt"))
        T(c, "60–80%", 600, 540, 110, ts, WHITE, vis(t, B(0, 0.3)), maxw=380)
        T(c, "SPACE MOTION", 1380, 430, 86, ts, WHITE, vis(t, B(0, 0.1)), maxw=900)
        T(c, "SICKNESS", 1380, 540, 86, ts, CORAL, vis(t, B(0, 0.2)), maxw=900)
        C(c, "OF SPACE TRAVELERS GET IT", 1380, 680, vis(t, B(0, 0.5)), ts, size=34)
    def pB(c, ts):
        hx, hy, r = 640, 600, 330
        gb = ease(prog(t, B(1, 0.6), 0.6))
        bx, by = head_side(c, hx, hy, r, glow_brain=gb, t=t)
        ex, ey = hx + r * 0.62, hy - r * 0.2
        eye_icon(c, ex, ey, r * 0.13)
        ax, ay = hx - r * 0.05, hy + r * 0.3
        ear_spiral(c, ax, ay, r * 0.11)
        pe = vis(t, B(1, 0.05)); pv = vis(t, B(1, 0.35))
        arrow(c, ax, ay - r * 0.1, bx - r * 0.1, by + r * 0.25, YEL, 7, pe)
        arrow(c, ex - r * 0.1, ey - r * 0.05, bx + r * 0.25, by + r * 0.2, FLUID, 7, pv)
        C(c, "INNER EAR: WHICH WAY IS DOWN?", 1400, 330, pe, ts, size=34, dot=YEL)
        C(c, "EYES: YOU'RE FLOATING", 1400, 450, pv, ts, size=34, dot=FLUID)
        C(c, "SIGNALS DON'T MATCH", 1400, 640, vis(t, B(1, 0.65)), ts, size=40, bg=CORAL, fg=NAVY, a=1)
        if gb > 0: T(c, "?!", bx, by - r * 0.55, 90, ts, CORAL, gb, maxw=200)
    def pC(c, ts):
        for k in range(4):
            x = 360 + k * 230; p = vis(t, B(2, 0.05 + 0.1 * k))
            rrect(c, x - 90, 330, 180, 200, 24, "#0d3b40", 0.95 * p); rrect(c, x - 90, 330, 180, 200, 24, TEAL, 0.8 * p, stroke=3)
            text(c, f"DAY {k + 1}", x, 370, 30, "#b8d8d6", p, w=700, fam="Inter")
            if k < 3:
                pth = skia.Path(); pth.moveTo(x - 50, 460)
                for j in range(1, 21): pth.lineTo(x - 50 + j * 5, 460 + math.sin(j * 1.2 + t * 6) * 12)
                c.drawPath(pth, paint(CORAL, p, stroke=7))
            else: check(c, x, 455, 40, p)
        C(c, "TYPICAL BOUT: 2–3 DAYS", 690, 640, vis(t, B(2, 0.2)), ts, size=36, bg=YEL, fg=NAVY, a=1)
        pr = vis(t, B(2, 0.5))
        body(c, 1500, 880, 460, a=pr, arms=0.5, spread=0.4, rot=35 * math.sin(t * 0.5) + 20, fluid=0.7, puff=0.5, legs=0.8)
        C(c, "DOWN = WHERE YOUR FEET ARE", 1500, 960, vis(t, B(2, 0.6)), ts, size=30)
    run_panels(c, W, H, t, S, panels_for(S, [pA, pB, pC]), met=1.5)

# ================================================================== WEEK 1: MUSCLES
def or6_muscle(c, W, H, t, S):
    B = beats(S, 4)
    def pA(c, ts):
        hl = [("neck", CORAL, vis(t, B(1, 0.2))), ("back", CORAL, vis(t, B(1, 0.12))), ("thigh", CORAL, vis(t, B(1, 0.08))),
              ("calf", CORAL, vis(t, B(1, 0.03)))]
        if t < B(1, 0): hl = [(k, TEAL, 0.5 + 0.3 * math.sin(t * 3)) for k in ("neck", "back", "thigh", "calf")]
        an = body(c, 620, 960, 840, highlight=hl, glow=0.5)
        labels = [("NECK", an["sh"] - 10, B(1, 0.2)), ("BACK", an["sh"] + 120, B(1, 0.12)), ("THIGHS", an["hip"] + 110, B(1, 0.08)), ("CALVES", 860, B(1, 0.03))]
        for s_, y, t0 in labels:
            p = vis(t, t0)
            line(c, 760, y, 1000, y, CORAL, 3, p * 0.8)
            T(c, s_, 1030, y, 50, ts, WHITE, p, align="l", maxw=500)
        C(c, "ANTIGRAVITY MUSCLES", 1450, 170, vis(t, B(1, 0.4)), ts, size=40, bg=CORAL, fg=NAVY, a=1)
        C(c, "NOTHING TO FIGHT UP HERE", 1450, 960, vis(t, B(1, 0.7)), ts, size=32)
    def pB(c, ts):
        g = ease(prog(t, B(2, 0.35), 2.0))
        x0, y0, w, h = 360, 520, 1200, 110
        rrect(c, x0, y0, w, h, 30, "#ffffff", 0.08)
        rrect(c, x0, y0, w * (1 - 0.2 * g), h, 30, TEAL, 0.95)
        if g > 0.02:
            rrect(c, x0 + w * (1 - 0.2 * g), y0, w * 0.2 * g, h, 30, CORAL, 0.35, stroke=4, dash=([14, 10], 0))
        text(c, "MUSCLE MASS", x0, y0 - 40, 36 * ts, "#b8d8d6", 1, w=700, fam="Inter", align="l")
        T(c, "UP TO −20%", 960, 330, 130, ts, CORAL, vis(t, B(2, 0.25)))
        C(c, "ON FLIGHTS OF JUST 5–11 DAYS", 960, 780, vis(t, B(2, 0.45)), ts, size=38, bg=YEL, fg=NAVY, a=1)
        text(c, "SOURCE: CANADIAN SPACE AGENCY", 960, 880, 28, "#7fa9a6", vis(t, B(2, 0.6)), w=600, fam="Inter")
    def pC(c, ts):
        # treadmill + harnessed runner
        rrect(c, 300, 870, 680, 40, 20, "#2a3f44", 1); rrect(c, 300, 870, 680, 40, 20, TEAL, 0.7, stroke=3)
        for k in range(10):
            xx = 300 + ((k * 70 - t * 260) % 680)
            line(c, xx, 878, xx, 902, "#5d7a7e", 3, 0.8)
        rx, base = 640, 868; ph = t * 7
        for sg in (-1, 1):
            a1 = sg * 0.6 * math.sin(ph)
            kx, ky = rx + math.sin(a1) * 150, base - 340 + math.cos(a1) * 150
            fx, fy = kx + math.sin(a1 - 0.5) * 140, ky + math.cos(a1 - 0.5) * 140
            c.drawPath(capsule(rx, base - 340, kx, ky, 46), paint("#0d3b40")); c.drawPath(capsule(kx, ky, fx, min(fy, base - 10), 36), paint("#0d3b40"))
            c.drawPath(capsule(rx, base - 340, kx, ky, 46), paint(TEAL, 1, stroke=3)); c.drawPath(capsule(kx, ky, fx, min(fy, base - 10), 36), paint(TEAL, 1, stroke=3))
            ax = rx + 20 + sg * 0.6 * math.sin(ph + math.pi) * 120
            c.drawPath(capsule(rx + 10, base - 560, ax, base - 420, 34), paint(TEAL, 1, stroke=3))
        torso = capsule(rx, base - 360, rx + 25, base - 580, 110)
        c.drawPath(torso, paint("#0d3b40")); c.drawPath(torso, paint(TEAL, 1, stroke=3))
        circle(c, rx + 35, base - 670, 52, "#0d3b40"); circle(c, rx + 35, base - 670, 52, TEAL, 1, stroke=3)
        for sg in (-1, 1): line(c, rx + sg * 40, base - 470, rx + sg * 150, base - 5, YEL, 4, 0.85, dash=([10, 8], 0))
        C(c, "BUNGEE HARNESS", 640, 140, vis(t, B(3, 0.3)), ts, size=30, dot=YEL)
        clock(c, 1380, 470, 200, ease(prog(t, B(3, 0.1), 1.5)) * 2.5 / 24)
        T(c, "2.5 HOURS A DAY", 1380, 760, 70, ts, WHITE, vis(t, B(3, 0.2)), maxw=760)
        C(c, "× 3,652 DAYS", 1380, 870, vis(t, B(3, 0.65)), ts, size=40, bg=YEL, fg=NAVY, a=1)
    run_panels(c, W, H, t, S, [(0, pA), (B(2, 0), pB), (B(3, 0), pC)], met=7)

# ================================================================== MONTH 1: BONE
def femur(c, x, y, L, a=1.0, ang=0, crack=0.0, colr=BONE):
    c.save(); c.translate(x, y); c.rotate(ang)
    r = L * 0.11
    rrect(c, -L / 2, -r * 0.55, L, r * 1.1, r * 0.5, colr, a)
    for sx in (-1, 1):
        circle(c, sx * L / 2, -r * 0.55, r * 0.85, colr, a); circle(c, sx * L / 2, r * 0.55, r * 0.85, colr, a)
    c.drawRect(skia.Rect.MakeLTRB(-L / 2 - r, -r * 1.4, L / 2 + r, r * 1.4), paint(shader=lin(0, -r * 1.4, 0, r * 1.4, [(0, "#ffffff", 0.0), (1, "#7a5a30", 0.35)]), a=a))
    if crack > 0:
        pts = [(-L * 0.05, -r * 0.6), (L * 0.02, -r * 0.15), (-L * 0.03, r * 0.15), (L * 0.04, r * 0.6)]
        n = max(2, int(len(pts) * crack + 0.999))
        c.drawPath(poly(pts[:n], close=False), paint(CORAL, a, stroke=r * 0.14))
    c.restore()

@lru_cache(maxsize=1)
def lattice():
    rng = random.Random(21); nodes = []
    while len(nodes) < 70:
        x, y = rng.uniform(-1, 1), rng.uniform(-1, 1)
        if x * x + y * y < 0.82: nodes.append((x, y))
    edges = []
    for i, (x, y) in enumerate(nodes):
        d = sorted(((math.hypot(x - u, y - v), j) for j, (u, v) in enumerate(nodes) if j != i))[:3]
        for _, j in d:
            if (j, i) not in edges: edges.append((i, j))
    order = list(range(len(edges))); rng.shuffle(order)
    return nodes, edges, order

def bone_section(c, x, y, r, loss, a=1.0, t=0.0):
    circle(c, x, y, r, "#2b1f1a", 0.9 * a)
    circle(c, x, y, r, BONE, a, stroke=r * 0.12)
    nodes, edges, order = lattice()
    keep = 1 - loss
    for rank, ei in enumerate(order):
        i, j = edges[ei]
        f = rank / len(order)
        al = clamp((keep - f) * 12)
        if al <= 0: continue
        (x1, y1), (x2, y2) = nodes[i], nodes[j]
        line(c, x + x1 * r * 0.85, y + y1 * r * 0.85, x + x2 * r * 0.85, y + y2 * r * 0.85, BONE, r * 0.035, a * al)
    if 0 < loss < 0.95:
        rng = random.Random(int(t * 3))
        for k in range(5):
            an = rng.random() * 6.28; d = rng.random() * r * 0.7
            circle(c, x + math.cos(an) * d, y + math.sin(an) * d, r * 0.05, CORAL, a * 0.8)

def or6_bone(c, W, H, t, S):
    B = beats(S, 4)
    def pA(c, ts):
        femur(c, 960, 520, 1000, ang=-8)
        T(c, "YOUR BONES", 960, 860, 110, ts, WHITE, vis(t, B(0, 0.4)))
    def pB(c, ts):
        loss = 0.55 * ease(prog(t, B(1, 0.55), 2.5))
        bone_section(c, 620, 540, 330, loss, t=t)
        C(c, "BONE REBUILDS TO MATCH THE LOAD", 1390, 380, vis(t, B(1, 0.15)), ts, size=32, dot=GREEN)
        C(c, "NO LOAD → TAKEN APART", 1390, 520, vis(t, B(1, 0.55)), ts, size=36, bg=CORAL, fg=NAVY, a=1)
    def pC(c, ts):
        x0, y0, y1 = 520, 860, 260
        text(c, "BONE DENSITY", 300, 210, 32 * ts, "#b8d8d6", 1, w=700, fam="Inter", align="l")
        line(c, x0 - 30, y0, 1640, y0, "#ffffff", 3, 0.5)
        g = prog(t, B(2, 0.1), 2.6)
        for m in range(7):
            p = clamp(g * 7 - m)
            if p <= 0: continue
            lo, hi = 1 - 0.015 * m, 1 - 0.01 * m
            hmax = y0 - y1
            def hh(v): return (v - 0.9) / 0.1 * hmax
            xx = x0 + m * 180
            rrect(c, xx - 55, y0 - hh(lo) * p, 110, hh(lo) * p, 10, TEAL, 0.95)
            rrect(c, xx - 55, y0 - hh(hi) * p, 110, (hh(hi) - hh(lo)) * p + 2, 6, TEAL, 0.35)
            text(c, "START" if m == 0 else f"MONTH {m}", xx, y0 + 40, 26, "#b8d8d6", p, w=700, fam="Inter")
        C(c, "SPINE & HIPS: −1 TO −1.5% A MONTH", 1080, 170, vis(t, B(2, 0.45)), ts, size=36, bg=YEL, fg=NAVY, a=1)
        text(c, "NASA · 4–6 MONTH MISSIONS · AXIS ZOOMED (90–100%)", 1080, 960, 26, "#7fa9a6", vis(t, B(2, 0.6)), w=600, fam="Inter")
    def pD(c, ts):
        femur(c, 760, 520, 900, ang=-8, crack=prog(t, B(3, 0.2), 0.8))
        C(c, "FRACTURE RISK", 1500, 400, vis(t, B(3, 0.25)), ts, size=40, dot=CORAL)
        C(c, "EARLY OSTEOPOROSIS", 1500, 520, vis(t, B(3, 0.45)), ts, size=40, dot=CORAL)
        text(c, "NASA WARNING", 1500, 630, 28, "#7fa9a6", vis(t, B(3, 0.5)), w=600, fam="Inter")
    run_panels(c, W, H, t, S, panels_for(S, [pA, pB, pC, pD]), met=30)

# ================================================================== YOU GROW (spine)
def vertebra(c, x, y, w, h, a=1.0):
    rrect(c, x - w / 2, y - h / 2, w, h, h * 0.25, BONE, a)
    c.drawPath(poly([(x + w * 0.45, y - h * 0.2), (x + w * 0.9, y + h * 0.05), (x + w * 0.45, y + h * 0.3)]), paint(BONE, a * 0.85))
    c.drawRect(skia.Rect.MakeXYWH(x - w / 2, y - h / 2, w, h), paint(shader=lin(0, y - h / 2, 0, y + h / 2, [(0, "#ffffff", 0.0), (1, "#7a5a30", 0.3)]), a=a))

def spine_col(c, x, ytop, n, vh, disc, a=1.0, pain=0.0, t=0.0, w=150):
    y = ytop
    for k in range(n):
        vertebra(c, x, y + vh / 2, w, vh, a)
        y += vh
        if k < n - 1:
            col_ = mix(TEAL, CORAL, pain if k >= n - 3 else 0)
            oval(c, x, y + disc / 2, w * 0.46, max(2, disc / 2), col_, a * 0.9)
            y += disc
    return y

def or6_spine(c, W, H, t, S):
    mode = S.opts.get("mode")
    nb = 4 if S.n() >= 4 else S.n()
    B = beats(S, 4) if nb == 4 else (lambda i, f=0.0: S.lt(min(i, S.n() - 1), f))
    def pA(c, ts, t0=None):
        t0 = B(0, 0) if t0 is None else t0
        g = ease(prog(t, t0 + 0.4, 2.0))
        h = 720; st = 0.03 * g / 0.30 * 0.97
        line(c, 440, 950, 900, 950, "#5d7a7e", 4, 0.9)
        a1 = body(c, 670, 945, h, glow=0.4, edge="#7fb8b2")
        a2 = body(c, 1250, 945 - 0.0, h, stretch=0.1 * g, puff=0.4, legs=0.8, arms=0.3, spread=0.15, fluid=0.7, spine=0.0)
        y1, y2 = a1["top"], a2["top"]
        line(c, 500, y1, 1500, y1, "#ffffff", 3, 0.6, dash=([14, 10], 0))
        if g > 0.05:
            line(c, 1050, y2, 1500, y2, YEL, 4, 0.9, dash=([14, 10], 0))
            arrow(c, 1540, y1, 1540, y2 - 2, YEL, 5, g)
        T(c, "+3%", 1670, (y1 + y2) / 2, 90, ts, YEL, g, maxw=300)
        text(c, "LAUNCH", 670, 1010, 34 * ts, "#b8d8d6", 1, w=700, fam="Inter")
        text(c, "IN ORBIT", 1250, 1010, 34 * ts, TEAL, 1, w=700, fam="Inter")
    def pB(c, ts, t0=None):
        t0 = B(1, 0) if t0 is None else t0
        g = ease(prog(t, t0 + 0.3, 2.2))
        spine_col(c, 600, 170, 7, 78, 16, w=170)
        spine_col(c, 1300, 170, 7, 78, 16 + 22 * g, w=170)
        text(c, "ON EARTH", 600, 120, 34 * ts, "#b8d8d6", 1, w=700, fam="Inter")
        text(c, "IN ORBIT", 1300, 120, 34 * ts, TEAL, 1, w=700, fam="Inter")
        C(c, "DISCS RELAX & SPREAD OUT", 960, 1000 if not S.P else 990, vis(t, t0 + 0.5), ts, size=34, bg=TEAL, fg=NAVY, a=1)
    def pC(c, ts, t0=None):
        t0 = B(2, 0) if t0 is None else t0
        g = ease(prog(t, t0 + 0.3, 1.6))
        rx = 900; ytop, ybot = 150, 950
        rect(c, rx - 70, ytop, 140, ybot - ytop, "#e9e3cf", 1)
        for cm in range(170, 191):
            yy = lerp(ybot, ytop, (cm - 170) / 20)
            L = 60 if cm % 5 == 0 else 30
            line(c, rx - 70, yy, rx - 70 + L, yy, NAVY, 3)
            if cm % 5 == 0: text(c, f"{cm}", rx + 25, yy, 28, NAVY, 1, w=700, fam="Inter")
        y180 = lerp(ybot, ytop, 0.5); y185 = lerp(ybot, ytop, 0.75)
        yy = lerp(y180, y185, g)
        circle(c, 640, yy + 80, 80, "#0d3b40"); circle(c, 640, yy + 80, 80, TEAL, 1, stroke=4)
        line(c, 640, yy, rx - 75, yy, YEL, 5, 1)
        line(c, 520, y180, rx - 75, y180, "#ffffff", 3, 0.5, dash=([12, 10], 0))
        T(c, "1.80 M", 360, y180, 60, ts, WHITE, 1, maxw=300)
        T(c, "+5 CM", 1360, yy, 120, ts, YEL, g, maxw=500)
        C(c, "UP TO 3% (NASA)", 1360, yy + 130, vis(t, t0 + 0.6), ts, size=34)
    def pD(c, ts, t0=None):
        t0 = B(3, 0) if t0 is None else t0
        pulse = 0.55 + 0.45 * math.sin(t * 6)
        body(c, 560, 960, 820, highlight=[("lowback", CORAL, vis(t, t0 + 0.2) * pulse)], glow=0.5)
        g = ease(prog(t, t0 + 0.8, 1.6))
        x0, y0, w, h = 1000, 560, 760, 80
        rrect(c, x0, y0, w, h, 26, "#ffffff", 0.08)
        rrect(c, x0, y0, w * (1 - 0.19 * g), h, 26, TEAL, 0.95)
        text(c, "LOWER-BACK MUSCLES", x0, y0 - 36, 32 * ts, "#b8d8d6", 1, w=700, fam="Inter", align="l")
        T(c, "−19%", x0 + w - 10, y0 + 170, 90, ts, CORAL, g, align="r", maxw=500)
        C(c, "MORE THAN HALF: BACK PAIN", 1380, 300, vis(t, t0 + 0.3), ts, size=36, bg=CORAL, fg=NAVY, a=1)
        text(c, "STUDY OF 6 ASTRONAUTS, 4–7 MONTHS IN ORBIT", 1380, 900, 26, "#7fa9a6", vis(t, t0 + 0.5), w=600, fam="Inter")
    if mode == "intro": items = [(0, pA)]
    elif mode == "discs": items = [(0, lambda c, ts: pB(c, ts, 0))]
    elif mode == "ruler": items = [(0, lambda c, ts: pC(c, ts, 0))]
    elif mode == "pain": items = [(0, lambda c, ts: pA(c, ts, -3)), (S.ls(1), lambda c, ts: pD(c, ts, S.ls(1)))]
    elif S.P: items = [(0, lambda c, ts: pB(c, ts, 0)), (S.lt(1, 0.0), lambda c, ts: pA(c, ts, S.lt(1, 0)))]
    else: items = panels_for(S, [pA, pB, pC, pD])
    run_panels(c, W, H, t, S, items, met=None if S.P else 45)

# ================================================================== MONTH 6: EYES (SANS)
def eyeball(c, x, y, r, flat=0.0, swell=0.0, a=1.0, t=0.0):
    """side cross-section, cornea on the left, optic nerve leaving on the right."""
    # optic nerve
    c.drawPath(capsule(x + r * 0.9, y, x + r * 1.9, y + r * 0.15, r * 0.34), paint("#e8b9a0", a))
    c.drawPath(capsule(x + r * 0.9, y, x + r * 1.9, y + r * 0.15, r * 0.34), paint("#ffffff", a * 0.5, stroke=max(2, r * 0.02)))
    p = skia.Path(); n = 90
    for k in range(n + 1):
        an = k / n * 2 * math.pi
        cx_, cy_ = math.cos(an), math.sin(an)
        rr = r
        if cx_ > 0: rr = r * (1 - flat * 0.16 * cx_ ** 6)  # back of the eye flattens
        px, py = x + cx_ * rr, y + cy_ * rr
        if k == 0: p.moveTo(px, py)
        else: p.lineTo(px, py)
    p.close()
    c.drawPath(p, paint("#f6f2ee", a))
    inner = skia.Path(); inner.addCircle(x, y, r * 0.9)
    c.drawPath(p, paint("#c96b5a", a * 0.9, stroke=r * 0.05))
    c.save(); c.clipPath(p, doAntiAlias=True)
    circle(c, x, y, r * 0.88, "#1b3d44", a)
    c.drawCircle(x, y, r * 0.88, paint(shader=rad(x - r * 0.3, y - r * 0.2, r * 1.2, [(0, "#2f6d75", 0.7), (1, "#0b2226", 0.0)]), a=a))
    c.restore()
    # cornea + iris + lens
    p2 = skia.Path(); p2.addArc(skia.Rect.MakeLTRB(x - r * 1.18, y - r * 0.5, x - r * 0.6, y + r * 0.5), 90, 180)
    c.drawPath(p2, paint("#bfe8ff", a * 0.8, stroke=r * 0.03))
    line(c, x - r * 0.86, y - r * 0.42, x - r * 0.86, y - r * 0.16, "#2a8fbf", r * 0.06, a)
    line(c, x - r * 0.86, y + r * 0.16, x - r * 0.86, y + r * 0.42, "#2a8fbf", r * 0.06, a)
    oval(c, x - r * 0.72, y, r * 0.12, r * 0.26, "#d9f1ff", a * 0.85)
    # optic disc (swells)
    oval(c, x + r * 0.84 * (1 - flat * 0.15), y, r * (0.06 + 0.07 * swell), r * (0.14 + 0.05 * swell), mix("#f0d6a0", CORAL, swell), a)
    if swell > 0: circle(c, x + r * 0.8, y, r * 0.25, CORAL, 0.25 * swell * a * (0.7 + 0.3 * math.sin(t * 5)), blur=r * 0.08)

def glasses(c, x, y, s, a=1.0):
    for sg in (-1, 1):
        rrect(c, x + sg * s * 0.55 - s * 0.45, y - s * 0.3, s * 0.9, s * 0.6, s * 0.25, "#9fe3ff", a * 0.25)
        rrect(c, x + sg * s * 0.55 - s * 0.45, y - s * 0.3, s * 0.9, s * 0.6, s * 0.25, WHITE, a, stroke=s * 0.08)
    line(c, x - s * 0.1, y - s * 0.05, x + s * 0.1, y - s * 0.05, WHITE, s * 0.08, a)

def or6_eyes(c, W, H, t, S):
    B = beats(S, 4)
    def pA(c, ts):
        eyeball(c, 620, 540, 290, t=t)
        C(c, "MONTH 6 · EYE CHECKS", 620, 150, vis(t, B(0, 0.1)), ts, size=34, dot=TEAL)
        fr = ease(prog(t, B(1, 0.3), 1.4))
        donut(c, 1500, 420, 150, 0.7 * fr, TEAL, vis(t, B(1, 0.25)), label="≈70%")
        T(c, "SANS", 1500, 700, 110, ts, YEL, vis(t, B(1, 0.55)))
        text(c, "SPACEFLIGHT ASSOCIATED", 1500, 790, 30, "#b8d8d6", vis(t, B(1, 0.6)), w=700, fam="Inter")
        text(c, "NEURO-OCULAR SYNDROME", 1500, 835, 30, "#b8d8d6", vis(t, B(1, 0.6)), w=700, fam="Inter")
        pa = vis(t, B(1, 0.05)) * (1 - prog(t, B(1, 0.6), 0.4))
        for k, xx in enumerate((300, 940)):
            yy = 980 - ((t * 140 + k * 120) % 260)
            arrow(c, xx, yy + 80, xx, yy, FLUID, 8, pa)
    def pB(c, ts):
        sw = ease(prog(t, B(2, 0.05), 1.0)); fl = ease(prog(t, B(2, 0.3), 1.0))
        eyeball(c, 620, 540, 290, flat=fl, swell=sw, t=t)
        C(c, "NERVE SWELLS", 1100, 330, vis(t, B(2, 0.08)), ts, size=32, dot=CORAL)
        C(c, "BACK OF THE EYE FLATTENS", 1050, 780, vis(t, B(2, 0.35)), ts, size=32, dot=CORAL)
        glasses(c, 1530, 470, 150, vis(t, B(2, 0.65)))
        C(c, "NEW GLASSES", 1530, 620, vis(t, B(2, 0.7)), ts, size=32)
        if t > B(3, 0) - 0.3:
            C(c, "NO PERMANENT VISION LOSS SO FAR", 1350, 150, vis(t, B(3, 0.05)), ts, size=32, bg=GREEN, fg=NAVY, a=1)
            C(c, "CAUSE NOT FULLY UNDERSTOOD", 1350, 960, vis(t, B(3, 0.4)), ts, size=32, bg=YEL, fg=NAVY, a=1)
    run_panels(c, W, H, t, S, [(0, pA), (B(2, 0), pB)], met=182)

# ================================================================== RADIATION
def field_lines(c, x, y, R, t, a=1.0):
    for L in (1.7, 2.4, 3.2):
        for sg in (-1, 1):
            p = skia.Path(); first = True
            for k in range(0, 121):
                lam = math.radians(-75 + 150 * k / 120)
                r = L * R * math.cos(lam) ** 2
                if r < R * 1.01: continue
                px, py = x + sg * r * math.cos(lam), y - r * math.sin(lam)
                if first: p.moveTo(px, py); first = False
                else: p.lineTo(px, py)
            c.drawPath(p, paint("#7fd6ff", 0.45 * a, stroke=3, dash=([10, 10], -t * 25 * sg)))

def ray(c, x0, y0, x1, y1, q, colr=AMBER, a=1.0, w=4):
    px, py = lerp(x0, x1, q), lerp(y0, y1, q)
    tx, ty = lerp(x0, x1, max(0, q - 0.12)), lerp(y0, y1, max(0, q - 0.12))
    c.drawLine(tx, ty, px, py, paint(shader=lin(tx, ty, px, py, [(0, colr, 0), (1, colr, a)]), stroke=w))
    circle(c, px, py, w * 1.3, "#fff1c9", a)

def xray(c, x, y, s, a=1.0):
    rrect(c, x - s * 0.4, y - s * 0.5, s * 0.8, s, s * 0.06, "#0f2a44", a)
    rrect(c, x - s * 0.4, y - s * 0.5, s * 0.8, s, s * 0.06, "#7fb6e6", a, stroke=s * 0.02)
    line(c, x, y - s * 0.4, x, y + s * 0.38, "#dfeefa", s * 0.04, a * 0.8)
    for k in range(5):
        yy = y - s * 0.28 + k * s * 0.13
        for sg in (-1, 1):
            p = skia.Path(); p.moveTo(x, yy); p.quadTo(x + sg * s * 0.3, yy - s * 0.06, x + sg * s * 0.28, yy + s * 0.1)
            c.drawPath(p, paint("#dfeefa", a * 0.75, stroke=s * 0.025))

def or6_rad(c, W, H, t, S):
    nb = 5; B = beats(S, nb)
    def pA(c, ts):
        ex, ey, R = 700, 430, 170
        field_lines(c, ex, ey, R, t)
        globe_c(c, ex, ey, R, rot=0, tilt=15, spin=t * 0.5)
        an = t * 0.9; station(c, ex + math.cos(an) * R * 1.25, ey + math.sin(an) * R * 0.5, 34, t)
        rng = random.Random(7)
        for k in range(10):
            ph = rng.random(); sp = rng.uniform(0.35, 0.6); yy = rng.uniform(80, 760)
            q = (t * sp + ph) % 1
            deflect = rng.random() < 0.6
            if deflect:
                x1, y1 = ex + 560, yy
                if q < 0.6: ray(c, 1900, yy, x1, y1, q / 0.6, a=0.9)
                else:
                    qq = (q - 0.6) / 0.4
                    ray(c, x1, y1, x1 + 200, y1 + (-300 if yy < ey else 300), qq, a=0.9 * (1 - qq))
            else:
                ray(c, 1900, yy, ex + R * 1.2, ey + (yy - ey) * 0.25, q, a=0.9)
        T(c, "RADIATION", 1470, 330, 120, ts, AMBER, vis(t, B(1, 0.05)), maxw=760)
        C(c, "YOU CAN'T FEEL IT", 1470, 460, vis(t, B(1, 0.3)), ts, size=36)
    def pB(c, ts):
        c.drawRect(skia.Rect.MakeLTRB(0, 120, 1920, 520), paint(shader=lin(0, 120, 0, 520, [(0, "#4fb3ff", 0.0), (1, "#4fb3ff", 0.25)])))
        line(c, 0, 520, 1920, 520, "#7fd6ff", 4, 0.6)
        text(c, "ATMOSPHERE + MAGNETIC FIELD", 960, 470, 32, "#bfe8ff", vis(t, B(2, 0.1)), w=700, fam="Inter")
        rng = random.Random(4)
        for k in range(7):
            q = (t * 0.5 + rng.random()) % 1; xx = rng.uniform(150, 1800)
            ray(c, xx, 0, xx - 60, 515, q, a=0.8)
        rect(c, 0, 900, 1920, 180, "#123c32", 1)
        body(c, 560, 905, 330, glow=0.4)
        gauge(c, 1330, 860, 230, 0.04, "", 1, valtxt=None, colr=GREEN)
        T(c, "2–3 mSv", 1330, 570, 84, ts, WHITE, vis(t, B(2, 0.3)), maxw=520)
        C(c, "PER YEAR ON THE GROUND", 1330, 990, vis(t, B(2, 0.4)), ts, size=32, bg=GREEN, fg=NAVY, a=1)
    def pC(c, ts):
        station(c, 560, 520, 420, t, rot=-4)
        rng = random.Random(9)
        for k in range(12):
            q = (t * 0.55 + rng.random()) % 1; yy = rng.uniform(150, 900)
            ray(c, 1100, yy, 0, yy + rng.uniform(-200, 200), q, a=0.9)
        fr = 0.25 + 0.45 * ease(prog(t, B(3, 0.4), 1.2)) + 0.02 * math.sin(t * 9)
        gauge(c, 1450, 640, 250, fr, "", 1, colr=AMBER)
        T(c, "0.2–0.5 mSv", 1450, 310, 80, ts, AMBER, vis(t, B(3, 0.45)), maxw=560)
        C(c, "PER DAY IN LOW ORBIT", 1450, 780, vis(t, B(3, 0.55)), ts, size=32, bg=AMBER, fg=NAVY, a=1)
        C(c, "WALLS CAN'T STOP EVERYTHING", 560, 960, vis(t, B(3, 0.25)), ts, size=30)
    def pD(c, ts):
        def cal(x, y, top, big, sub, colr, p):
            rrect(c, x - 190, y - 170, 380, 340, 30, "#0d3b40", 0.95 * p); rrect(c, x - 190, y - 170, 380, 80, 30, colr, p)
            text(c, top, x, y - 130, 32, NAVY, p, w=800, fam="Inter")
            T(c, big, x, y + 20, 110, ts, WHITE, p, maxw=340)
            text(c, sub, x, y + 115, 30, "#b8d8d6", p, w=700, fam="Inter")
        cal(560, 380, "IN ORBIT", "1", "DAY", AMBER, vis(t, B(4, 0.0)))
        T(c, "≈", 960, 380, 140, ts, WHITE, vis(t, B(4, 0.15)), maxw=200)
        cal(1360, 380, "ON THE GROUND", "1–2", "MONTHS", GREEN, vis(t, B(4, 0.2)))
        n = 2 + int(3 * ease(prog(t, B(4, 0.6), 1.4)))
        for k in range(5):
            p = vis(t, B(4, 0.55 + 0.06 * k)) * (1 if k < n else 0.25)
            xray(c, 660 + k * 150, 790, 150, p)
        text(c, "1 mSv ≈ 10 CHEST X-RAYS (NASA) → A FEW X-RAYS A DAY", 960, 950, 30, "#cfe3ff", vis(t, B(4, 0.6)), w=700, fam="Inter")
    run_panels(c, W, H, t, S, [(0, pA), (B(2, 0), pB), (B(3, 0), pC), (B(4, 0), pD)], met=200)

# ================================================================== ONE YEAR: TWINS
def chromosome(c, x, y, s, cap, a=1.0):
    for ang in (25, -25):
        c.save(); c.translate(x, y); c.rotate(ang)
        rrect(c, -s * 0.16, -s, s * 0.32, s * 2, s * 0.16, "#9b8cff", a)
        for sg in (-1, 1):
            L = cap * s * 0.42
            yy = -s - L * 0.2 if sg < 0 else s - L * 0.8
            rrect(c, -s * 0.16, yy, s * 0.32, L, s * 0.12, YEL, a)
        c.restore()
    circle(c, x, y, s * 0.17, "#6f5fe0", a)

def tel_curve(f):
    """telomere length vs normalised time: 0..0.2 pre, 0.2..0.7 flight (up), landing drop, ends a bit below."""
    if f < 0.2: return 1.0
    if f < 0.7: return 1.0 + 0.35 * ease((f - 0.2) / 0.5)
    if f < 0.76: return lerp(1.35, 0.93, ease((f - 0.7) / 0.06))
    return lerp(0.93, 0.96, (f - 0.76) / 0.24)

def or6_twins(c, W, H, t, S):
    B = beats(S, 5)
    def pA(c, ts):
        def inner():
            globe_c(c, 560 + 60, 470 + 380, 230, rot=-40, tilt=25, spin=-t, light=(0.2, 0.8, 0.6))
            body(c, 560, 470 + 150, 330, arms=0.5, spread=0.4, rot=-10 + 6 * math.sin(t * 0.7), fluid=0.8, puff=0.5, legs=0.8)
        porthole(c, 560, 470, 260, t, inner=inner, ticks=False)
        line(c, 1150, 780, 1650, 780, "#5d7a7e", 4, 0.9)
        body(c, 1400, 775, 470, glow=0.4, edge="#7fb8b2")
        T(c, "SCOTT · 340 DAYS IN ORBIT", 560, 830, 46, ts, TEAL, vis(t, B(1, 0.1)), maxw=820)
        T(c, "MARK · ON EARTH", 1400, 830, 46, ts, "#b8d8d6", vis(t, B(1, 0.3)), maxw=700)
        C(c, "IDENTICAL TWINS · 2015–16", 960, 140, vis(t, B(1, 0.05)), ts, size=36, bg=YEL, fg=NAVY, a=1)
        C(c, "10 RESEARCH TEAMS", 960, 960, vis(t, B(1, 0.7)), ts, size=34)
        C(c, "ONE YEAR: VERY FEW HAVE DONE IT", 1400, 240, vis(t, B(0, 0.2), B(1, 0.0)), ts, size=30)
    def pB(c, ts):
        f = clamp((t - B(2, 0.05)) / max(0.5, B(2, 0.95) - B(2, 0.05)))
        chromosome(c, 520, 540, 250, tel_curve(f))
        T(c, "TELOMERES", 520, 900, 56, ts, YEL, vis(t, B(2, 0.0)), maxw=600)
        gx0, gx1, gy = 960, 1780, 560
        line(c, gx0, gy + 200, gx1, gy + 200, "#ffffff", 3, 0.5); line(c, gx0, gy - 220, gx0, gy + 200, "#ffffff", 3, 0.5)
        rect(c, lerp(gx0, gx1, 0.2), gy - 220, (gx1 - gx0) * 0.5, 420, TEAL, 0.10)
        text(c, "IN SPACE", lerp(gx0, gx1, 0.45), gy - 250, 28, TEAL, 1, w=700, fam="Inter")
        text(c, "BACK HOME", lerp(gx0, gx1, 0.86), gy - 250, 28, "#b8d8d6", 1, w=700, fam="Inter")
        yb = gy + 40
        line(c, gx0, yb, gx1, yb, "#ffffff", 2, 0.4, dash=([10, 10], 0))
        p = skia.Path(); n = int(120 * f)
        for k in range(n + 1):
            ff = k / 120; yy = yb - (tel_curve(ff) - 1) * 600
            if k == 0: p.moveTo(gx0, yy)
            else: p.lineTo(lerp(gx0, gx1, ff), yy)
        if n > 0: c.drawPath(p, paint(YEL, 1, stroke=7))
        C(c, "LONGER IN SPACE", lerp(gx0, gx1, 0.45), gy + 265, vis(t, B(2, 0.35)), ts, size=26)
        C(c, "SHORTER ≈2 DAYS AFTER LANDING", lerp(gx0, gx1, 0.6), gy + 360, vis(t, B(2, 0.7)), ts, size=26, bg=CORAL, fg=NAVY, a=1)
    def pC(c, ts):
        fr = ease(prog(t, B(3, 0.05), 1.4))
        donut(c, 560, 470, 220, 0.913 * fr, GREEN, 1, label="91%")
        T(c, "GENE CHANGES BACK", 560, 790, 48, ts, WHITE, vis(t, B(3, 0.25)), maxw=760)
        T(c, "TO NORMAL IN 6 MONTHS", 560, 850, 48, ts, WHITE, vis(t, B(3, 0.25)), maxw=760)
        hx, hy = 1380, 470
        for dx, dy, rr in [(-70, 10, 95), (10, -45, 105), (95, -5, 90), (20, 55, 95), (-70, 75, 70)]:
            circle(c, hx + dx, hy + dy, rr, "#e39aa6", vis(t, B(3, 0.5)) * 0.9)
        arrow(c, hx + 240, hy - 80, hx + 240, hy + 100, CORAL, 12, vis(t, B(3, 0.6)))
        T(c, "SPEED & ACCURACY DOWN", 1380, 760, 46, ts, CORAL, vis(t, B(3, 0.6)), maxw=760)
        C(c, "STILL LOWER AT 6 MONTHS", 1380, 850, vis(t, B(3, 0.8)), ts, size=30)
    def pD(c, ts):
        T(c, "n = 2", 960, 470, 260, ts, WHITE, vis(t, B(4, 0.05)), maxw=1000)
        C(c, "TOO SMALL FOR FIRM RULES", 960, 760, vis(t, B(4, 0.35)), ts, size=40, bg=CORAL, fg=NAVY, a=1)
    run_panels(c, W, H, t, S, [(0, pA), (B(2, 0), pB), (B(3, 0), pC), (B(4, 0), pD)], met=365)

# ================================================================== RECORDS
def or6_records(c, W, H, t, S):
    B = beats(S, 4)
    def pA(c, ts):
        x0, x1 = 720, 1800
        rs = ease(prog(t, B(3, 0.2), 1.6))
        dmax = lerp(1200, 3800, rs)
        def X(d): return x0 + (x1 - x0) * d / dmax
        grid = [365 * k for k in range(1, 11)]
        for d in grid:
            if d > dmax: continue
            xx = X(d); line(c, xx, 210, xx, 880, "#ffffff", 2, 0.10)
            lab = f"{d // 365} YR" if d // 365 == 1 else f"{d // 365} YRS"
            text(c, lab, xx, 905, 24, "#7fa9a6", 0.9 if (d // 365 <= 3 or (d // 365) % 2 == 0) else 0, w=600, fam="Inter")
        rows = [("SCOTT KELLY", "ONE TRIP", 340, TEAL, 0.0, None),
                ("CHINA'S PLAN", "ONE TRIP, ~1 YEAR", 365, YEL, 0.0, "dash"),
                ("VALERI POLYAKOV", "ONE TRIP · 1994–95", 437, TEAL, B(0, 0.05), None),
                ("OLEG KONONENKO", "TOTAL · 5 FLIGHTS", 1111, MINT, B(2, 0.05), None),
                ("YOU", "10 YEARS", 3652, CORAL, B(3, 0.35), None)]
        for k, (nm, sub, d, colr, t0, sty) in enumerate(rows):
            y = 270 + k * 140
            p = vis(t, t0) if t0 else 1.0
            if k == 4 and t < t0: continue
            T(c, nm, 120, y - 14, 44, ts, WHITE if k != 4 else CORAL, p, align="l", maxw=560)
            text(c, sub, 120, y + 30, 26, "#b8d8d6", p, w=600, fam="Inter", align="l")
            g = ease(prog(t, t0 + 0.1, 1.2)) if t0 else 1.0
            w_ = (X(d) - x0) * g
            if sty == "dash": rrect(c, x0, y - 26, max(4, w_), 52, 26, colr, 0.9, stroke=4, dash=([14, 10], 0))
            else: rrect(c, x0, y - 26, max(4, w_), 52, 26, colr, 0.95 * p)
            hl = (k == 2 and B(0, 0) <= t < B(2, 0)) or (k == 3 and B(2, 0) <= t < B(3, 0))
            if hl: rrect(c, x0 - 8, y - 34, w_ + 16, 68, 34, YEL, 0.9, stroke=4)
            val = f"{d:,}" if k != 1 else "~365"
            text(c, f"{val} DAYS", x0 + w_ + 18, y, 30, WHITE, p * (g > 0.95), w=800, fam="Inter", align="l")
        C(c, "MIR · JAN 1994 – MAR 1995", 1250, 150, vis(t, B(0, 0.3), B(1, 0.0)), ts, size=30, dot=TEAL)
        C(c, "A TEST FOR MARS · HE WALKED OUT", 1250, 150, vis(t, B(1, 0.15), B(2, 0.0)), ts, size=30, dot=YEL)
        C(c, "FIRST PAST 1,000 DAYS · JUNE 2024", 1250, 150, vis(t, B(2, 0.2), B(3, 0.0)), ts, size=30, dot=MINT)
        C(c, "MORE THAN 3× ANYONE'S TOTAL", 1250, 150, vis(t, B(3, 0.6)), ts, size=32, bg=CORAL, fg=NAVY, a=1)
    run_panels(c, W, H, t, S, [(0, pA)], met=437)

# ================================================================== TEN YEARS: ROUGH MATH
def dose_chart(c, t, ts, t0, dur, x0=300, x1=1500, y0=880, y1=230, show_vals=True):
    def X(yr): return lerp(x0, x1, yr / 10)
    def Y(ms): return lerp(y0, y1, ms / 2000)
    line(c, x0, y0, x1 + 30, y0, "#ffffff", 3, 0.6); line(c, x0, y0, x0, y1 - 20, "#ffffff", 3, 0.6)
    for yr in range(0, 11, 2): text(c, f"{yr}", X(yr), y0 + 34, 26 * ts, "#b8d8d6", 1, w=700, fam="Inter")
    text(c, "YEARS IN ORBIT", (x0 + x1) / 2, y0 + 80 * (1 if ts < 1.5 else 1.3), 26 * ts, "#7fa9a6", 1, w=700, fam="Inter")
    for ms in (500, 1000, 1500, 2000):
        line(c, x0, Y(ms), x1, Y(ms), "#ffffff", 1.5, 0.08)
        text(c, f"{ms:,}", x0 - 18, Y(ms), 24 * ts, "#7fa9a6", 1, w=600, fam="Inter", align="r")
    text(c, "mSv", x0 - 18, y1 - 50, 24 * ts, "#7fa9a6", 1, w=700, fam="Inter", align="r")
    line(c, x0, Y(600), x1 + 30, Y(600), CORAL, 5, 1, dash=([20, 12], 0))
    text(c, "NASA CAREER LIMIT · 600", x0 + 20, Y(600) - 24 * ts, 26 * ts, CORAL, 1, w=800, fam="Inter", align="l")
    g = ease(prog(t, t0, dur)); yr = 10 * g
    lo, hi = 0.2 * 365.25, 0.5 * 365.25
    p = skia.Path(); p.moveTo(X(0), Y(0)); p.lineTo(X(yr), Y(hi * yr)); p.lineTo(X(yr), Y(lo * yr)); p.close()
    c.drawPath(p, paint(AMBER, 0.35))
    line(c, X(0), Y(0), X(yr), Y(hi * yr), AMBER, 5); line(c, X(0), Y(0), X(yr), Y(lo * yr), AMBER, 5)
    for rate, yl in ((0.5, 600 / (0.5 * 365.25)), (0.2, 600 / (0.2 * 365.25))):
        if yr >= yl:
            circle(c, X(yl), Y(600), 13, WHITE, 1); circle(c, X(yl), Y(600), 22, WHITE, 0.6, stroke=3)
            text(c, f"≈{yl:.0f} YRS" if yl > 4 else f"≈{yl:.1f} YRS".replace(".0", ""), X(yl), Y(600) + 50, 26 * ts, WHITE, 1, w=800, fam="Inter")
    if show_vals and g > 0.98:
        text(c, "≈1,800", X(10) + 20, Y(hi * 10), 34 * ts, AMBER, 1, w=900, align="l")
        text(c, "≈730", X(10) + 20, Y(lo * 10), 34 * ts, AMBER, 1, w=900, align="l")

def artery(c, x, y, s, a=1.0):
    c.drawPath(capsule(x - s, y + s * 0.3, x + s, y - s * 0.3, s * 0.55), paint("#c0445a", a))
    c.drawPath(capsule(x - s, y + s * 0.3, x + s, y - s * 0.3, s * 0.3), paint("#5a0f1f", a))

def antibody(c, x, y, s, a=1.0):
    line(c, x, y + s, x, y, MINT, s * 0.18, a)
    for sg in (-1, 1):
        line(c, x, y, x + sg * s * 0.6, y - s * 0.7, MINT, s * 0.18, a)
        line(c, x + sg * s * 0.2, y - s * 0.1, x + sg * s * 0.75, y - s * 0.75, MINT, s * 0.1, a * 0.7)

def or6_ten(c, W, H, t, S):
    if S.opts.get("mode") == "short":
        def pS(c, ts):
            dose_chart(c, t, 1.9, 0.3, max(1.0, S.dur - 1.5), x0=380, x1=1500, y0=900, y1=170)
        run_panels(c, W, H, t, S, [(0, pS)]); return
    B = beats(S, 5)
    def pA(c, ts):
        if t < B(1, 0.0) + 0.3:
            stamp(c, "ROUGH MATH, NOT A FORECAST", 960, 520, prog(t, B(0, 0.4), 0.4), 1, color=YEL, rot=-4, size=72)
        else:
            dose_chart(c, t, ts, B(2, 0.0), max(1.0, B(2, 0.95) - B(2, 0.0)))
            C(c, "ROUGH MATH", 1700, 150, 1, ts, size=28, bg=YEL, fg=NAVY, a=1)
    def pB(c, ts):
        femur(c, 760, 520, 820, ang=-8)
        T(c, "?", 760, 280, 200, ts, YEL, vis(t, B(3, 0.1)), maxw=200)
        C(c, "NOBODY HAS STAYED LONG ENOUGH", 1450, 420, vis(t, B(3, 0.2)), ts, size=32)
        C(c, "NASA: MORE RESEARCH NEEDED", 1450, 540, vis(t, B(3, 0.6)), ts, size=32, bg=YEL, fg=NAVY, a=1)
    def pC(c, ts):
        items = [(eye_icon, 520, "EYES"), (artery, 960, "ARTERIES"), (antibody, 1400, "IMMUNE SYSTEM")]
        for k, (fn, x, lab) in enumerate(items):
            p = vis(t, B(4, 0.05 + 0.1 * k))
            if p <= 0: continue
            with Layer(c, p):
                fn(c, x, 470, 110)
                T(c, "?", x + 120, 340, 90, ts, YEL, 1, maxw=200)
                T(c, lab, x, 650, 44, ts, WHITE, 1, maxw=420)
        T(c, "WE DON'T KNOW", 960, 860, 100, ts, CORAL, vis(t, B(4, 0.6)))
    run_panels(c, W, H, t, S, [(0, pA), (B(3, 0), pB), (B(4, 0), pC)], met=3652)

# ================================================================== MARS
def or6_mars(c, W, H, t, S):
    B = beats(S, 4)
    def pA(c, ts):
        globe_c(c, 420, 560, 170, rot=30, tilt=15, spin=t)
        mars_d(c, 1520, 560, 130)
        line(c, 620, 560, 1360, 560, TEAL, 4, 0.7, dash=([18, 12], -t * 40))
        q = ((t - B(0, 0)) / 4) % 1; station(c, lerp(640, 1340, q), 560 - math.sin(q * math.pi) * 60, 40, t)
        T(c, "THE REAL LONG HAUL", 960, 220, 90, ts, WHITE, vis(t, B(0, 0.3)))
    def pB(c, ts):
        sx, sy = 960, 430
        sun(c, sx, sy, 34, t, glow=0.6)
        rE, rM, k = 190, 300, 0.55
        c.drawOval(skia.Rect.MakeLTRB(sx - rE, sy - rE * k, sx + rE, sy + rE * k), paint(FLUID, 0.5, stroke=3))
        c.drawOval(skia.Rect.MakeLTRB(sx - rM, sy - rM * k, sx + rM, sy + rM * k), paint(MARS, 0.6, stroke=3))
        tt = B(1, 0.1); g = prog(t, tt, max(1.0, B(1, 0.9) - tt))
        # out: half ellipse from Earth (left) to Mars (right); back on the lower side
        a_ = (rE + rM) / 2; cxo = sx + (rM - rE) / 2
        def tr(f, top=True):
            an = math.pi * (1 - f) if top else math.pi + math.pi * f
            return cxo + math.cos(an) * a_ * (1 if top else -1) * (1 if top else 1), sy - math.sin(an) * a_ * k * (1 if top else -1)
        p = skia.Path(); seg = clamp(g / 0.21)
        for j in range(41):
            f = j / 40 * seg; x_ = cxo - math.cos(math.pi * f) * a_; y_ = sy - math.sin(math.pi * f) * a_ * k
            if j == 0: p.moveTo(x_, y_)
            else: p.lineTo(x_, y_)
        c.drawPath(p, paint(YEL, 1, stroke=5))
        if g > 0.79:
            p2 = skia.Path(); seg2 = clamp((g - 0.79) / 0.21)
            for j in range(41):
                f = j / 40 * seg2; x_ = cxo + math.cos(math.pi * f) * a_; y_ = sy + math.sin(math.pi * f) * a_ * k
                if j == 0: p2.moveTo(x_, y_)
                else: p2.lineTo(x_, y_)
            c.drawPath(p2, paint(YEL, 1, stroke=5, dash=([14, 10], 0)))
        circle(c, sx - rE, sy, 18, FLUID, 1); mars_d(c, sx + rM, sy, 16)
        # timeline bar
        x0, x1, y = 260, 1660, 860; tot = 860
        segs = [(180, YEL, "180 DAYS OUT"), (500, MARS, "≈500 DAYS ON MARS"), (180, YEL, "180 DAYS HOME")]
        xx = x0
        for d, colr, lab in segs:
            w_ = (x1 - x0) * d / tot; fill = clamp((g * tot - (xx - x0) / (x1 - x0) * tot) / d)
            rrect(c, xx, y - 26, w_ - 6, 52, 20, "#ffffff", 0.08)
            if fill > 0: rrect(c, xx, y - 26, (w_ - 6) * fill, 52, 20, colr, 0.95)
            text(c, lab, xx + w_ / 2, y + 60, 26, "#cfe3ff", 1 if fill > 0 else 0.4, w=700, fam="Inter")
            xx += w_
        C(c, "≈2.4 YEARS", 1790, 860, vis(t, B(1, 0.85)), ts, size=32, bg=YEL, fg=NAVY, a=1)
        C(c, "ONE NASA REFERENCE PLAN", 960, 130, vis(t, B(1, 0.05)), ts, size=30)
    def pC(c, ts):
        gauge(c, 560, 600, 260, 0.75 + 0.02 * math.sin(t * 9), "", 1, colr=AMBER)
        T(c, "1.8 mSv", 560, 250, 96, ts, AMBER, vis(t, B(2, 0.1)), maxw=520)
        C(c, "PER DAY IN DEEP SPACE", 560, 720, vis(t, B(2, 0.15)), ts, size=30, bg=AMBER, fg=NAVY, a=1)
        text(c, "MEASURED BY CURIOSITY'S RAD DETECTOR ON THE WAY TO MARS", 560, 820, 22, "#b8d8d6", vis(t, B(2, 0.2)), w=600, fam="Inter")
        x0, x1, y = 1050, 1780, 520
        def X(ms): return lerp(x0, x1, ms / 800)
        g = ease(prog(t, B(2, 0.45), 1.6))
        rrect(c, x0, y - 40, x1 - x0, 80, 30, "#ffffff", 0.08)
        rrect(c, x0, y - 40, (X(660) - x0) * g, 80, 30, AMBER, 0.95)
        line(c, X(600), y - 90, X(600), y + 90, CORAL, 6, 1)
        text(c, "LIMIT 600", X(600), y - 120, 30, CORAL, 1, w=800, fam="Inter")
        T(c, "≈660 mSv", (x0 + x1) / 2, y + 170, 80, ts, WHITE, g, maxw=700)
        text(c, "JUST THE FLIGHTS THERE AND BACK", (x0 + x1) / 2, y + 250, 28, "#b8d8d6", g, w=700, fam="Inter")
    def pD(c, ts):
        station(c, 600, 520, 380, t)
        arrow(c, 900, 520, 1350, 520, YEL, 10, vis(t, B(3, 0.3)))
        mars_d(c, 1530, 520, 120, vis(t, B(3, 0.3)))
        T(c, "LESSONS FOR DEEP SPACE", 960, 860, 76, ts, WHITE, vis(t, B(3, 0.45)))
    run_panels(c, W, H, t, S, panels_for(S, [pA, pB, pC, pD]), met=3652)

# ================================================================== TWIST: COMING HOME
def or6_twist(c, W, H, t, S):
    short = S.opts.get("mode") == "short"
    B = beats(S, 5) if not short else None
    def pA(c, ts):
        g = ease(prog(t, 0.0, max(1.0, B(1, 0) - 0.3)))
        rect(c, 0, 900, 1920, 180, "#2d4a36", 1)
        capsule_chute(c, 960, lerp(380, 860, g), 120, t=t)
        T(c, "COMING HOME", 960, 150, 100, ts, YEL, vis(t, 0.4))
    def pB(c, ts, t0=None, t1=None):
        t0 = B(1, 0.1) if t0 is None else t0
        g = ease(prog(t, t0, 1.8))
        line(c, 520, 950, 1400, 950, "#5d7a7e", 4, 0.9)
        a1 = body(c, 760, 945, 720, glow=0.4, edge="#7fb8b2")
        a2 = body(c, 1160, 945, 720, stretch=0.1 * (1 - g), legs=0.85 + 0.15 * g, puff=0.4 * (1 - g))
        y1, y2 = a1["top"], a2["top"]
        line(c, 560, y1, 1420, y1, "#ffffff", 3, 0.5, dash=([14, 10], 0))
        T(c, "−5 CM", 1600, y1 - 40, 90, ts, YEL, vis(t, t0 + 0.4), maxw=360)
        C(c, "WITHIN A FEW MONTHS", 1600, y1 + 70, vis(t, t0 + 0.6), ts, size=30)
        text(c, "BEFORE", 760, 1010, 34 * ts if not S.P else 46, "#b8d8d6", 1, w=700, fam="Inter")
        text(c, "AFTER LANDING", 1160, 1010, 34 * ts if not S.P else 46, TEAL, 1, w=700, fam="Inter")
    def pC(c, ts):
        items = [("HEIGHT", B(1, 0.6)), ("GUT BACTERIA", B(2, 0.2)), ("MOST GENE CHANGES", B(2, 0.5))]
        for k, (s_, t0) in enumerate(items):
            y = 330 + k * 170; p = vis(t, t0)
            check(c, 560, y, 46, p)
            T(c, s_, 660, y, 72, ts, WHITE, p, align="l", maxw=1100)
        T(c, "MOSTLY BACK TO NORMAL", 960, 900, 60, ts, GREEN, vis(t, B(2, 0.6)))
    def pD(c, ts):
        femur(c, 560, 450, 700, ang=-8)
        x0, y0, w = 1020, 420, 720
        g = ease(prog(t, B(3, 0.3), 1.5))
        text(c, "BONE LOST IN SPACE", x0, y0 - 50, 30, "#b8d8d6", 1, w=700, fam="Inter", align="l")
        rrect(c, x0, y0, w, 70, 26, CORAL, 0.9)
        rrect(c, x0, y0, w * 0.55 * g, 70, 26, GREEN, 0.95)
        text(c, "REGAINED AFTER 1 YEAR (PARTLY)", x0, y0 + 110, 28, GREEN, g, w=700, fam="Inter", align="l")
        C(c, "LASTING LOSS ≈ A DECADE OF AGING", 1380, 700, vis(t, B(3, 0.6)), ts, size=34, bg=CORAL, fg=NAVY, a=1)
        text(c, "STUDY OF 17 ASTRONAUTS · BAR IS ILLUSTRATIVE", 1380, 800, 24, "#7fa9a6", vis(t, B(3, 0.3)), w=600, fam="Inter")
    def pE(c, ts, t0=None):
        t0 = B(4, 0) if t0 is None else t0
        g = ease(prog(t, t0 + 0.4, 1.2))
        y = 200
        for k in range(5):
            vertebra(c, 620, y + 50, 220, 100)
            y += 100
            if k < 4:
                bul = g * (1 if k == 2 else 0)
                oval(c, 620 + bul * 70, y + 16, 110 * 0.92 + bul * 50, 16, mix(TEAL, CORAL, bul), 1)
                if bul > 0: circle(c, 620 + 130, y + 16, 40, CORAL, 0.35 * bul * (0.6 + 0.4 * math.sin(t * 7)), blur=12)
                y += 32
        T(c, "≈4×", 1400, 420, 200, ts, CORAL, g, maxw=500)
        C(c, "SLIPPED-DISC RISK", 1400, 620, vis(t, t0 + 0.5), ts, size=38, bg=CORAL, fg=NAVY, a=1)
        C(c, "IN THE MONTHS AFTER LANDING", 1400, 720, vis(t, t0 + 0.8), ts, size=30)
    if short:
        mid = S.lt(0, 0.5)
        items = [(0, lambda c, ts: pB(c, ts, 0.2)), (mid, lambda c, ts: pE(c, ts, mid))]
        run_panels(c, W, H, t, S, items); return
    run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB), (B(1, 0.55), pC), (B(3, 0), pD), (B(4, 0), pE)])

# ================================================================== OZONE SHORT
OZ_V = "#8b5cff"; OZ_S = "#7fd6ff"; OZ_P = "#c58bff"

@lru_cache(maxsize=1)
def hole_shape():
    rng = random.Random(33)
    return [(k / 48 * 2 * math.pi, 1 + 0.1 * math.sin(k / 48 * 6.28 * 2 + 0.7) + rng.uniform(-0.05, 0.05)) for k in range(48)]

def ozone_hole(c, x, y, R, t, a=1.0, scale=1.0, off=(0.06, 0.03)):
    """cap below ~64 S covers about 25 million km2 -> radius ~0.43 R on a polar view."""
    rr = 0.43 * R * scale
    pts = [(x + off[0] * R + math.cos(an + t * 0.15) * rr * m, y + off[1] * R + math.sin(an + t * 0.15) * rr * m) for an, m in hole_shape()]
    p = poly(pts)
    c.drawPath(p, paint(OZ_V, 0.55 * a, blur=R * 0.03))
    c.save(); c.clipPath(p, doAntiAlias=True)
    c.drawCircle(x, y, rr * 1.2, paint(shader=rad(x + off[0] * R, y + off[1] * R, rr * 1.2, [(0, "#3a0f8f", 0.85 * a), (0.7, OZ_V, 0.6 * a), (1, OZ_P, 0.3 * a)])))
    c.restore()
    c.drawPath(p, paint(OZ_P, a, stroke=max(2, R * 0.012)))
    return p

def pole_globe(c, x, y, R, t, a=1.0):
    globe_c(c, x, y, R, rot=0, tilt=-90, spin=t * 3, a=a, glow=1.0, light=(0.3, 0.5, 0.8))

def or6_oz(c, W, H, t, S):
    mode = S.opts.get("mode", "intro")
    def pIntro(c, ts):
        pole_globe(c, 960, 560, 400, t)
        ozone_hole(c, 960, 560, 400, t, a=0.6 + 0.4 * ease(prog(t, 0.2, 0.8)))
        C(c, "ANTARCTICA · SEPT–OCT 2026", 960, 1010, vis(t, 0.3), ts, size=26, bg="#1b1650")
    def pSize(c, ts):
        pole_globe(c, 560, 560, 400, t)
        ozone_hole(c, 560, 560, 400, t)
        C(c, "NASA & NOAA · 4 NOV 2026", 1430, 230, vis(t, S.lt(0, 0.05)), ts, size=26, bg="#1b1650")
        T(c, "AVERAGE SIZE", 1430, 340, 40, ts, OZ_S, vis(t, S.lt(0, 0.3)), maxw=900)
        T(c, "≈25M KM²", 1430, 460, 90, ts, WHITE, vis(t, S.lt(0, 0.35)), maxw=900)
        T(c, "≈ NORTH AMERICA", 1430, 620, 56, ts, YEL, vis(t, S.lt(0, 0.75)), maxw=900)
        C(c, "PEAK 27.1M KM² · 18 SEP", 1430, 820, vis(t, S.lt(0, 0.85)), ts, size=24, bg="#1b1650")
    def pVortex(c, ts, t0):
        pole_globe(c, 560, 560, 400, t)
        ozone_hole(c, 560, 560, 400, t)
        for k in range(6):
            an0 = k / 6 * 360 + t * 70
            p = skia.Path(); p.addArc(skia.Rect.MakeLTRB(560 - 300, 560 - 300, 560 + 300, 560 + 300), an0, 38)
            c.drawPath(p, paint(OZ_S, 0.9, stroke=12))
            ar = math.radians(an0 + 38)
            ax, ay = 560 + math.cos(ar) * 300, 560 + math.sin(ar) * 300
            tx, ty = -math.sin(ar), math.cos(ar)
            arrow(c, ax - tx * 10, ay - ty * 10, ax + tx * 18, ay + ty * 18, OZ_S, 12, 0.9)
        T(c, "STRONG", 1430, 380, 70, ts, OZ_S, vis(t, t0 + 0.2), maxw=900)
        T(c, "POLAR VORTEX", 1430, 470, 70, ts, OZ_S, vis(t, t0 + 0.3), maxw=900)
        t1 = S.lt(0, 0.55)
        C(c, "CHLORINE DOWN ~1/3 SINCE 1980s", 1400, 650, vis(t, t1), ts, size=30, bg="#1b1650", dot=GREEN)
        C(c, "RECOVERY BY THE 2070s", 1400, 800, vis(t, t1 + 0.4), ts, size=30, bg=GREEN, fg=NAVY, a=1)
    def pThinA(c, ts):
        globe_c(c, 960, 560, 360, rot=20, tilt=20, spin=t * 2)
        fl = 0.5 + 0.5 * math.sin(t * 7)
        c.drawCircle(960, 560, 395, paint(OZ_P, (0.35 + 0.4 * fl) * (1 - prog(t, S.lt(0, 0.6), 0.6) * 0.8), stroke=16, blur=4))
        T(c, "?", 1500, 300, 160, ts, YEL, vis(t, S.lt(0, 0.4)), maxw=200)
    def pThinB(c, ts, t0):
        g = ease(prog(t, t0 + 0.3, 1.4))
        # atmosphere column on the left
        x, y_top, y_bot = 380, 150, 950
        c.drawRect(skia.Rect.MakeLTRB(x - 120, y_top, x + 120, y_bot), paint(shader=lin(0, y_top, 0, y_bot, [(0, "#0a0b33", 1), (1, "#3a7fd0", 1)])))
        oz_top, oz_bot = lerp(y_bot, y_top, 35 / 50), lerp(y_bot, y_top, 15 / 50)
        rect(c, x - 120, oz_top, 240, oz_bot - oz_top, OZ_V, 0.55 * (1 - g) + 0.1)
        text(c, "15–35 KM", x, (oz_top + oz_bot) / 2, 30 * ts, WHITE, 1 - g * 0.6, w=800, fam="Inter")
        # squeezed strip -> 3 mm, beside two coins (to scale with each other)
        sx = 1000; base = 760
        hh = lerp(oz_bot - oz_top, 34, g)
        rect(c, sx - 160, base - hh, 320, hh, OZ_V, 0.9)
        if g > 0.05:
            arrow(c, x + 140, (oz_top + oz_bot) / 2, sx - 180, base - hh / 2, OZ_P, 7, g)
        for k in range(2):
            oval(c, 1450, base - 8 - k * 17, 150, 26, "#c97a4a", 1); oval(c, 1450, base - 12 - k * 17, 150, 26, "#e39a62", 1)
        T(c, "≈3 MM", 1000, base - 170, 110, ts, YEL, g, maxw=500)
        text(c, "ALL OF IT, SQUEEZED", 1000, base + 80, 30 * ts, WHITE, g, w=700, fam="Inter")
        text(c, "≈ 2 COINS", 1500, base + 80, 30 * ts, "#ffd9b8", g, w=700, fam="Inter")
    def pUV(c, ts, t1):
        sun(c, 170, 180, 90, t, glow=0.7)
        oz_y = 470
        rect(c, 0, oz_y - 40, 1920, 80, OZ_V, 0.5)
        text(c, "OZONE", 1880, oz_y, 30 * ts, WHITE, 1, w=800, fam="Inter", align="r")
        rect(c, 0, 900, 1920, 180, "#1d3b2c", 1)
        rays = [("UV-C", "#b06cff", 0.0, 520), ("UV-B", "#5aa8ff", 0.88, 900), ("UV-A", "#bfe8ff", 0.05, 1300)]
        for name, colr, block, x in rays:
            for j in range(3):
                q = ((t * 0.7 + j / 3) % 1)
                y = lerp(130, 900, q)
                if name == "UV-C" and y > oz_y: continue
                if name == "UV-B" and y > oz_y and j != 0: continue
                ray(c, x - 200 + j * 20, 130, x + 60, 900, q, colr, 1, w=12)
            T(c, name, x - 150, 250, 46, ts, colr, 1, maxw=400)
        text(c, "ALL", 540, 640, 34 * ts, "#d9b8ff", 1, w=800, fam="Inter")
        text(c, "MOST", 930, 640, 34 * ts, "#bfe0ff", 1, w=800, fam="Inter")
        text(c, "BLOCKED", 735, 740, 34 * ts, WHITE, 1, w=800, fam="Inter")
    def pUV2(c, ts, t1):
        clock(c, 600, 540, 260, ease(prog(t, t1 + 0.3, 1.5)) * 5 / 60, colr=CORAL)
        T(c, "5 MIN", 600, 900, 90, ts, CORAL, vis(t, t1 + 0.3), maxw=400)
        body(c, 1400, 930, 620, fill=mix("#0d3b40", "#b8443a", ease(prog(t, t1 + 0.5, 1.5))), edge=CORAL, glow=0.5)
        C(c, "NASA SIMULATION: NO OZONE TREATY, 2065", 1400, 160, vis(t, t1), ts, size=22, bg="#1b1650")
    if mode == "intro": items = [(0, pIntro)]
    elif mode == "size": items = [(0, pSize)]
    elif mode == "vortex": items = [(0, lambda c, ts: pVortex(c, ts, 0))]
    elif mode == "thin":
        t0 = S.ls(1)
        items = [(0, pThinA), (S.ls(2) - 0.2, lambda c, ts: pThinB(c, ts, S.ls(2) - 0.2))]
    else:  # uv
        t1 = S.lt(0, 0.5)
        items = [(0, lambda c, ts: pUV(c, ts, t1)), (t1, lambda c, ts: pUV2(c, ts, t1))]
    run_panels(c, W, H, t, S, items, seed=71, kind="ozone")

def motif_oz(c, W, H, t, S, cx, cy, s):
    R = 300 * S.u * s * (1.2 if S.P else 1)
    pole_globe(c, cx, cy, R, t); ozone_hole(c, cx, cy, R, t)

def bg_oz(c, W, H, t, S): bg_o(c, W, H, t, S, seed=71, kind="ozone")
def or6_ozend(c, W, H, t, S): kit.end_short(c, W, H, t, S, bg_oz, motif_oz, dict(accent=OZ_S, chip="#1b1650"))

SCENES = {k: v for k, v in globals().items() if k.startswith("or6_") and callable(v)}
