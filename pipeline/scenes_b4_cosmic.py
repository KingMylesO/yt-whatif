"""Batch 04 scenes: What If a Cosmic Ray Flipped a Bit in Your Computer? (+ cosmic teaser and 4,096-votes Shorts).

Look: "terminal vs. cosmos". Near-black crimson-tinted backgrounds with faint scanlines, phosphor-green memory cells
(charge "buckets" labelled 0/1), particle tracks white-hot -> magenta -> violet, warning red for flipped bits.
Signature motif: a grid of memory cells with a particle streak slicing through and flipping one cell.
Every scene draws its art on a virtual 1920x1080 stage (Stage). In Shorts the stage is scaled into the
0.255H..0.58H band and text sizes are multiplied by ts=1.75. Multi-part scenes are drawn as time-ordered panels.
"""
from common2 import *
import geo
import scenes_b3_kit as kit

BG_T, BG_B = "#050409", "#1c0712"
GREEN = "#3dff8f"; GREEN_D = "#0b2a1a"
HOT, MAG, VIO = "#ffffff", "#ff4fd8", "#8a5cff"
RED = "#ff4d4d"; CHECKC = "#7dffb0"; YEL = ACCENT
CHIPBG = "#2a0c1c"
PAL = dict(accent=GREEN, chip="#3a0f26", title2=ACCENT)
MONO = "JetBrains Mono"
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
    chip(c, s, x, y, p, size * ts, **kw)

def T(c, s, x, y, size, ts, colr="#ffffff", a=1.0, w=900, maxw=1800, **kw):
    if a <= 0: return
    fam = kw.pop("fam", "Inter Display")
    sz = fit(s, maxw, size * ts, w, fam)
    text(c, s, x, y, sz, colr, a, w=w, fam=fam, shadow=kw.pop("shadow", 10), **kw)

def M(c, s, x, y, size, ts, colr=GREEN, a=1.0, align="l", maxw=1800):
    """terminal (monospace) text"""
    if a <= 0: return
    sz = fit(s, maxw, size * ts, 800, MONO)
    text(c, s, x, y, sz, colr, a, w=800, fam=MONO, align=align)

# ------------------------------------------------------------------ background
_BG = {}
def bg_img(W, H):
    k = (W, H)
    if k not in _BG:
        surf = skia.Surface(W, H); cc = surf.getCanvas()
        fill_bg(cc, W, H, BG_T, BG_B)
        cc.drawPaint(paint(shader=rad(W * 0.8, H * 0.15, max(W, H) * 0.75, [(0, "#5a0f2e", 0.45), (1, "#000000", 0)])))
        cc.drawPaint(paint(shader=rad(W * 0.1, H * 0.95, max(W, H) * 0.6, [(0, "#2a0f5a", 0.35), (1, "#000000", 0)])))
        for y in range(0, H, 4): cc.drawLine(0, y + 0.5, W, y + 0.5, paint("#000000", 0.16, stroke=1))
        _BG[k] = surf.makeImageSnapshot()
    return _BG[k]

def bg_k(c, W, H, t, S, star_a=0.55, seed=41):
    c.drawImage(bg_img(W, H), 0, 0)
    stars(c, W, H, t, star_a, seed=seed, drift=(-4, 0))

def run_panels(c, W, H, t, S, items, seed=41, zoom=None):
    """items: [(t_on, fn(c, ts)), ...] in time order. Each later panel covers the previous one (own bg while fading in)."""
    bg_k(c, W, H, t, S, seed=seed)
    for i, (t0, fn) in enumerate(items):
        t1 = items[i + 1][0] if i + 1 < len(items) else None
        if t1 is not None and t >= t1 + 0.5: continue
        a = phase(t, t0 if i > 0 else None, t1)
        if a <= 0.003: continue
        with Layer(c, a) as on:
            if not on: continue
            if i > 0 and t < t0 + 0.55: bg_k(c, W, H, t, S, seed=seed)
            if S.P: c.clipRect(skia.Rect.MakeLTRB(0, 0.215 * H, W, 0.59 * H))
            with Stage(c, S) as ts:
                if zoom and S.P:
                    z, zx, zy = zoom; c.translate(zx, zy); c.scale(z, z); c.translate(-zx, -zy)
                fn(c, ts)
    kit.hook(c, W, H, t, S)

def lines_text(S):
    return " ".join(L["text"] for L in S.lines).lower()

# ------------------------------------------------------------------ memory cells
def cell(c, x, y, s, bit, a=1.0, glow=0.0, col=GREEN, fill=None, digit=True):
    if a <= 0: return
    w = s; h = s * 1.15; f = bit if fill is None else fill
    if glow > 0: circle(c, x, y, s * 0.95, col, a * glow * 0.4, blur=s * 0.3)
    rrect(c, x - w / 2, y - h / 2, w, h, s * 0.16, "#07110c", a)
    if f > 0.01:
        fh = (h - s * 0.16) * clamp(f)
        rrect(c, x - w / 2 + s * 0.08, y + h / 2 - s * 0.08 - fh, w - s * 0.16, fh, s * 0.1, col, a * 0.6)
    rrect(c, x - w / 2, y - h / 2, w, h, s * 0.16, col, a * (0.5 + 0.5 * glow), stroke=max(1.5, s * 0.05))
    if digit:
        b = 1 if f >= 0.5 else 0
        text(c, str(b), x, y, s * 0.55, "#04170c" if b else col, a, w=800, fam=MONO)

_GRID = {}
def grid_img(cols, rows, s, gap, seed):
    k = (cols, rows, int(s), int(gap), seed)
    if k not in _GRID:
        rng = random.Random(seed)
        bits = [[1 if rng.random() < 0.5 else 0 for _ in range(cols)] for _ in range(rows)]
        Wd = int(cols * (s + gap) + gap + 40); Hd = int(rows * (s * 1.15 + gap) + gap + 40)
        surf = skia.Surface(Wd, Hd); cc = surf.getCanvas(); cc.clear(skia.ColorTRANSPARENT)
        for r in range(rows):
            for q in range(cols):
                cell(cc, 20 + gap + q * (s + gap) + s / 2, 20 + gap + r * (s * 1.15 + gap) + s * 0.575, s, bits[r][q])
        _GRID[k] = (surf.makeImageSnapshot(), bits, Wd, Hd)
    return _GRID[k]

def grid(c, cx, cy, cols, rows, s, seed=1, a=1.0, flips=()):
    """cached grid of cells centred on (cx, cy). flips: [(row, col, p)] animate a 0<->1 flip (red)."""
    s = int(s); gap = int(s * 0.22)
    img, bits, Wd, Hd = grid_img(cols, rows, s, gap, seed)
    x0 = cx - Wd / 2; y0 = cy - Hd / 2
    pt = skia.Paint(); pt.setAlphaf(clamp(a))
    c.drawImage(img, x0, y0, skia.SamplingOptions(skia.FilterMode.kLinear), pt)
    def pos(r, q): return (x0 + 20 + gap + q * (s + gap) + s / 2, y0 + 20 + gap + r * (s * 1.15 + gap) + s * 0.575)
    for (r, q, p) in flips:
        if p <= 0: continue
        x, y = pos(r, q); b = bits[r][q]
        f = lerp(b, 1 - b, eout(clamp(p)))
        cell(c, x, y, s, 0, a, glow=clamp(1 - abs(p - 0.35) * 2.2), col=RED, fill=f)
    return pos, bits

def bitrow(c, cx, cy, bits, s, a=1.0, flip=None, flip_p=0.0, cols=None, glows=None, gap=None):
    """row of cells; flip = index animated to the other value (red). cols: per-cell colour. returns x positions."""
    n = len(bits); gap = s * 0.18 if gap is None else gap
    x0 = cx - (n * s + (n - 1) * gap) / 2 + s / 2; xs = []
    for i, b in enumerate(bits):
        x = x0 + i * (s + gap); xs.append(x)
        g = glows[i] if glows else 0.0
        if flip == i and flip_p > 0:
            f = lerp(b, 1 - b, eout(clamp(flip_p)))
            cell(c, x, cy, s, 0, a, glow=max(g, clamp(1 - abs(flip_p - 0.35) * 2.2)), col=RED, fill=f)
        else:
            cell(c, x, cy, s, b, a, glow=g, col=(cols[i] if cols else GREEN))
    return xs

# ------------------------------------------------------------------ particles
def strike(c, tx, ty, t, th, ang=58, speed=2600, w=7, a=1.0, L=650, col2=MAG, ring=True):
    """particle that passes through (tx, ty) at time th, moving at angle ang (deg, y down)."""
    dt = t - th
    if a <= 0 or dt < -1.2 or dt > 0.8: return
    dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    hx, hy = tx + dx * dt * speed, ty + dy * dt * speed
    fade = clamp(1 - max(0.0, dt) / 0.8)
    sx, sy = hx - dx * L, hy - dy * L
    sh = lin(sx, sy, hx, hy, [(0, VIO, 0), (0.6, col2, 0.8), (1, HOT, 1)])
    c.drawLine(sx, sy, hx, hy, paint(stroke=w * 3, shader=sh, blur=w, a=0.55 * a * fade))
    c.drawLine(sx, sy, hx, hy, paint(stroke=w, shader=sh, a=a * fade))
    circle(c, hx, hy, w * 1.3, HOT, a * fade)
    circle(c, hx, hy, w * 4.5, col2, 0.3 * a * fade, blur=w * 2)
    if ring and 0 <= dt < 0.5:
        circle(c, tx, ty, w * (3 + 36 * dt), HOT, a * (1 - dt / 0.5) * 0.8, stroke=max(1.5, w * 0.6))

def rain(c, t, x0, x1, y0, y1, n=14, seed=3, a=1.0, speed=1500, w=4, ang=80, period=1.6):
    """continuous rain of thin particle tracks (muons)."""
    if a <= 0: return
    rng = random.Random(seed)
    for k in range(n):
        ph = rng.random() * period; xx = rng.uniform(x0, x1); per = period * rng.uniform(0.8, 1.3)
        q = ((t + ph) % per) / per
        dy = y1 - y0
        ty = y0 + q * (dy + 900) - 300
        strike(c, xx + (ty - y0) / math.tan(math.radians(ang)) * 0.0, ty, t, t, ang=ang, w=w, a=a * 0.85, L=260, ring=False)

@lru_cache(maxsize=8)
def shower_tree(seed, x0, y0, ybot):
    rng = random.Random(seed); segs = []
    def grow(x, y, ang, depth):
        if y > ybot or depth > 8: return
        L = rng.uniform(70, 125)
        x1 = x + math.sin(ang) * L; y1 = min(ybot + 40, y + math.cos(ang) * L)
        kind = "p" if depth == 0 else rng.choice(["mu", "n", "n", "e", "pi", "mu"])
        segs.append((x, y, x1, y1, depth, kind))
        nb = 2 if (depth < 4 and rng.random() < 0.85) else (2 if rng.random() < 0.18 else 1)
        for k in range(nb):
            grow(x1, y1, clamp(ang + rng.uniform(-0.18, 0.18) + (k - (nb - 1) / 2) * rng.uniform(0.35, 0.6), -1.0, 1.0), depth + 1)
    grow(x0, y0, 0.0, 0)
    return tuple(segs)

KCOL = {"p": HOT, "mu": MAG, "n": "#e6e6f2", "e": "#ffb36b", "pi": VIO}

def shower(c, x0, y0, ybot, g, a=1.0, seed=5, only=None, w=4.5):
    """branching cascade; g = growth front (y). only: highlight one particle kind."""
    if a <= 0: return
    for (xa, ya, xb, yb, d, k) in shower_tree(seed, x0, y0, ybot):
        if ya >= g: continue
        f = clamp((g - ya) / max(1.0, yb - ya))
        xe, ye = lerp(xa, xb, f), lerp(ya, yb, f)
        al = a * (1.0 if (only is None or k == only or d == 0) else 0.22)
        col_ = KCOL[k]
        c.drawLine(xa, ya, xe, ye, paint(col_, al * 0.35, stroke=w * 3, blur=w))
        c.drawLine(xa, ya, xe, ye, paint(col_, al, stroke=w))
        if f < 1: circle(c, xe, ye, w * 1.5, HOT, al)
        elif only is not None and k == only and d > 2:
            circle(c, xb, yb, w * 2.2, col_, al)

# ------------------------------------------------------------------ props
_IMG = {}
def cached(key, W, H, fn):
    if key not in _IMG:
        surf = skia.Surface(int(W), int(H)); cc = surf.getCanvas(); cc.clear(skia.ColorTRANSPARENT); fn(cc)
        _IMG[key] = surf.makeImageSnapshot()
    return _IMG[key]

def draw_img(c, img, x, y, a=1.0):
    pt = skia.Paint(); pt.setAlphaf(clamp(a))
    c.drawImage(img, x, y, skia.SamplingOptions(skia.FilterMode.kLinear), pt)

def galaxy(c, x, y, R, t, a=1.0):
    def mk(cc):
        rng = random.Random(9); cx = cy = R * 1.1
        cc.drawCircle(cx, cy, R * 0.5, paint(shader=rad(cx, cy, R * 0.5, [(0, "#ffe6f4", 0.9), (0.4, "#c24aa0", 0.4), (1, "#000000", 0)])))
        for arm in range(2):
            for i in range(900):
                q = i / 900; th = arm * math.pi + q * 3.6 * math.pi * 0.5 + rng.gauss(0, 0.12)
                r = R * (0.08 + 0.92 * q) + rng.gauss(0, R * 0.04)
                px, py = cx + math.cos(th) * r, cy + math.sin(th) * r * 0.42
                cc.drawCircle(px, py, rng.uniform(0.8, 2.4), paint(rng.choice(["#ffd9f0", "#c9b8ff", "#ffffff", "#ff8ad8"]), rng.uniform(0.3, 0.9)))
    img = cached(("gal", int(R)), R * 2.2, R * 2.2, mk)
    c.save(); c.translate(x, y); c.rotate(-12 + t * 1.5); draw_img(c, img, -R * 1.1, -R * 1.1, a); c.restore()

def supernova(c, x, y, r, t, a=1.0):
    if a <= 0: return
    pul = 0.5 + 0.5 * math.sin(t * 3)
    circle(c, x, y, r * 3.2, MAG, 0.18 * a, blur=r * 1.2)
    for k in range(3):
        q = (t * 0.5 + k / 3) % 1
        circle(c, x, y, r * (1 + 3.5 * q), "#ffb3ec", a * (1 - q) * 0.6, stroke=4)
    c.save(); c.translate(x, y); c.rotate(t * 10)
    for i in range(10):
        c.rotate(36); L = r * (1.6 + 0.4 * math.sin(t * 4 + i))
        c.drawPath(poly([(-r * 0.12, 0), (0, -L), (r * 0.12, 0)]), paint("#ffe0f6", 0.5 * a))
    c.restore()
    circle(c, x, y, r * (0.9 + 0.1 * pul), HOT, a)

def nucleus(c, x, y, s, a=1.0, n=4, seed=2):
    rng = random.Random(seed)
    for k in range(n):
        an = k / n * 6.28 + seed; d = s * 0.45 if n > 1 else 0
        circle(c, x + math.cos(an) * d, y + math.sin(an) * d, s * 0.55, RED if k % 2 == 0 else "#d8d8ea", a)

def flier(c, x, y, s, t, a=1.0, kind="p", ang=0):
    """cosmic-ray particle with a trail flying to the right."""
    if a <= 0: return
    c.drawLine(x - 260 * s, y, x, y, paint(shader=lin(x - 260 * s, y, x, y, [(0, VIO, 0), (1, MAG, 0.9 * a)]), stroke=7 * s))
    if kind == "p":
        circle(c, x, y, 18 * s, RED, a); text(c, "+", x, y - 1, 26 * s, "#ffffff", a, w=900)
    else:
        nucleus(c, x, y, 16 * s, a, n=4)

def balloon(c, x, y, s, a=1.0):
    p = skia.Path(); p.moveTo(x, y + s * 1.3)
    p.cubicTo(x - s * 1.4, y + s * 0.4, x - s * 1.1, y - s * 1.3, x, y - s * 1.3)
    p.cubicTo(x + s * 1.1, y - s * 1.3, x + s * 1.4, y + s * 0.4, x, y + s * 1.3); p.close()
    c.drawPath(p, paint("#e9e2d0", a)); c.drawPath(p, paint("#8f8577", a, stroke=s * 0.05))
    for k in (-0.5, 0, 0.5): line(c, x + k * s * 0.9, y - s * 0.9, x + k * s * 0.3, y + s * 1.2, "#b9b0a0", s * 0.03, a)
    for k in (-1, 1): line(c, x + k * s * 0.15, y + s * 1.3, x + k * s * 0.35, y + s * 1.9, "#d0c8b8", s * 0.03, a)
    rrect(c, x - s * 0.4, y + s * 1.9, s * 0.8, s * 0.45, s * 0.06, "#7a5236", a)

def meter(c, x, y, r, frac, a=1.0, label="RADIATION", ts=1.0):
    if a <= 0: return
    rrect(c, x - r * 1.2, y - r * 1.1, r * 2.4, r * 1.75, r * 0.12, "#160a12", a)
    rrect(c, x - r * 1.2, y - r * 1.1, r * 2.4, r * 1.75, r * 0.12, GREEN, 0.5 * a, stroke=3)
    for k in range(11):
        an = math.radians(200 + k * 14)
        line(c, x + math.cos(an) * r * 0.85, y + math.sin(an) * r * 0.85, x + math.cos(an) * r * 0.98, y + math.sin(an) * r * 0.98,
             RED if k > 7 else GREEN, 4, a)
    an = math.radians(200 + 140 * clamp(frac))
    line(c, x, y, x + math.cos(an) * r * 0.9, y + math.sin(an) * r * 0.9, HOT, 6, a)
    circle(c, x, y, r * 0.08, HOT, a)
    M(c, label, x, y + r * 0.35, 30, ts, GREEN, a, align="c", maxw=r * 2.2)

def baseball(c, x, y, r, a=1.0):
    circle(c, x, y, r, "#f4f1ea", a)
    for sd in (-1, 1):
        p = skia.Path(); p.addArc(skia.Rect.MakeXYWH(x + sd * r * 0.55 - r, y - r, 2 * r, 2 * r), 90 + (0 if sd > 0 else 180) + 35, 110)
        c.drawPath(p, paint("#d43a3a", a, stroke=r * 0.06, dash=([r * 0.08, r * 0.07], 0)))
    circle(c, x, y, r, "#c9c2b5", a, stroke=r * 0.03)

def phone(c, x, y, h, a=1.0, glow=0.0):
    w = h * 0.5
    rrect(c, x - w / 2, y - h / 2, w, h, w * 0.16, "#1a1a24", a)
    rrect(c, x - w / 2 + w * 0.06, y - h / 2 + w * 0.08, w * 0.88, h - w * 0.16, w * 0.1, mix("#0d2a3a", "#2a6a8a", glow), a)
    rrect(c, x - w / 2, y - h / 2, w, h, w * 0.16, "#9aa4b8", a, stroke=max(2, w * 0.03))
    for k in range(4): rrect(c, x - w * 0.32, y - h * 0.3 + k * h * 0.13, w * 0.64, h * 0.08, h * 0.02, GREEN, a * 0.35)

def laptop(c, x, y, s, a=1.0):
    rrect(c, x - s * 0.8, y - s * 1.0, s * 1.6, s * 1.0, s * 0.06, "#1a1a24", a)
    rect(c, x - s * 0.72, y - s * 0.93, s * 1.44, s * 0.86, "#0d2a3a", a)
    for k in range(4): rect(c, x - s * 0.6, y - s * 0.8 + k * s * 0.18, s * (0.9 - 0.15 * (k % 2)), s * 0.08, GREEN, a * 0.35)
    c.drawPath(poly([(x - s * 0.95, y + s * 0.08), (x + s * 0.95, y + s * 0.08), (x + s * 0.8, y), (x - s * 0.8, y)]), paint("#4a4a5a", a))

def plane_icon(c, x, y, s, a=1.0, colr="#e8eef8"):
    rrect(c, x - s, y - s * 0.09, s * 2, s * 0.18, s * 0.09, colr, a)
    c.drawPath(poly([(x - s * 0.15, y), (x + s * 0.25, y), (x - s * 0.35, y + s * 0.7), (x - s * 0.55, y + s * 0.7)]), paint(colr, a))
    c.drawPath(poly([(x - s * 0.15, y), (x + s * 0.25, y), (x - s * 0.35, y - s * 0.7), (x - s * 0.55, y - s * 0.7)]), paint(colr, a))
    c.drawPath(poly([(x - s * 0.8, y), (x - s * 0.95, y - s * 0.4), (x - s * 1.02, y - s * 0.4), (x - s * 0.95, y)]), paint(colr, a))

def hut(c, x, y, s, wall="#3a2a3a", roof="#5a2a3a", a=1.0, win=0.8):
    rect(c, x - s * 0.5, y - s * 0.6, s, s * 0.6, wall, a)
    c.drawPath(poly([(x - s * 0.62, y - s * 0.58), (x, y - s * 1.0), (x + s * 0.62, y - s * 0.58)]), paint(roof, a))
    rect(c, x - s * 0.3, y - s * 0.42, s * 0.18, s * 0.16, "#ffd27a", a * win); rect(c, x + s * 0.12, y - s * 0.42, s * 0.18, s * 0.16, "#ffd27a", a * win)

def telescope(c, x, y, s, a=1.0, ang=0):
    c.save(); c.translate(x, y); c.rotate(ang)
    for sd in (-1, 1): rect(c, -s * 0.5, sd * s * 0.42 - (s * 0.5 if sd < 0 else 0), s * 1.0, s * 0.5, "#3a5ad0", a)
    rrect(c, -s * 0.9, -s * 0.28, s * 1.8, s * 0.56, s * 0.1, "#d9dee8", a)
    rect(c, s * 0.9, -s * 0.24, s * 0.14, s * 0.48, "#8a93a8", a)
    c.restore()

def probe(c, x, y, s, a=1.0):
    line(c, x, y, x + s * 2.0, y + s * 0.9, "#c9ced8", s * 0.05, a)
    line(c, x, y, x - s * 1.6, y + s * 1.2, "#c9ced8", s * 0.05, a)
    rrect(c, x + s * 1.9, y + s * 0.8, s * 0.35, s * 0.25, s * 0.05, "#8a93a8", a)
    line(c, x, y, x + s * 0.4, y - s * 2.4, "#c9ced8", s * 0.035, a)
    rect(c, x - s * 0.45, y - s * 0.2, s * 0.9, s * 0.5, "#a8a090", a)
    c.drawPath(poly([(x - s * 0.45, y - s * 0.2), (x + s * 0.45, y - s * 0.2), (x + s * 0.3, y - s * 0.35), (x - s * 0.3, y - s * 0.35)]), paint("#c9c0ae", a))
    oval(c, x, y - s * 0.75, s * 1.15, s * 0.42, "#e8e6e0", a)
    oval(c, x, y - s * 0.75, s * 1.15, s * 0.42, "#8a8578", a, stroke=s * 0.04)
    line(c, x, y - s * 0.75, x, y - s * 1.35, "#c9ced8", s * 0.04, a); circle(c, x, y - s * 1.38, s * 0.06, "#ffffff", a)

def robot(c, x, y, s, t, a=1.0, squash=0.0):
    """generic cube robot (game character) standing on (x, y)."""
    sy = 1 - 0.15 * squash; sx = 1 + 0.12 * squash
    c.save(); c.translate(x, y); c.scale(sx, sy)
    for sd in (-1, 1): rect(c, sd * s * 0.22 - s * 0.08, -s * 0.28, s * 0.16, s * 0.28, "#2a8f8a", a)
    rrect(c, -s * 0.5, -s * 1.25, s, s, s * 0.14, "#3ad1c8", a)
    rrect(c, -s * 0.5, -s * 1.25, s, s, s * 0.14, "#1b6f6a", a, stroke=s * 0.05)
    for sd in (-1, 1):
        circle(c, sd * s * 0.2, -s * 0.85, s * 0.13, "#ffffff", a); circle(c, sd * s * 0.2 + s * 0.03, -s * 0.84, s * 0.06, "#101820", a)
    line(c, 0, -s * 1.25, 0, -s * 1.55, "#1b6f6a", s * 0.05, a); circle(c, 0, -s * 1.6, s * 0.09, GREEN, a)
    c.restore()

def block_row(c, x0, x1, y, s, a=1.0, colr="#5a2a3a"):
    xx = x0
    while xx < x1 - 1:
        rect(c, xx, y, s - 3, s - 3, colr, a); rect(c, xx, y, s - 3, (s - 3) * 0.18, mix(colr, "#ffffff", 0.25), a)
        line(c, xx + s * 0.5, y + s * 0.2, xx + s * 0.5, y + s * 0.6, mix(colr, "#000000", 0.3), 3, a)
        xx += s

def package(c, x, y, w, h, a=1.0):
    for k in range(14):
        xx = x - w * 0.45 + k * w * 0.9 / 13
        rect(c, xx - 7, y - h / 2 - 40, 14, 44, "#d9b45a", a); rect(c, xx - 7, y + h / 2 - 4, 14, 44, "#d9b45a", a)
    rrect(c, x - w / 2, y - h / 2, w, h, 18, "#d6cfc0", a)
    rrect(c, x - w / 2, y - h / 2, w, h, 18, "#9a9282", a, stroke=4)
    rrect(c, x - w * 0.22, y - h * 0.3, w * 0.44, h * 0.6, 10, "#8a8272", a)

def server_stick(c, x, y, w, a=1.0, label="ECC"):
    h = w * 0.22
    rrect(c, x - w / 2, y - h / 2, w, h, 8, "#1f6a3a", a)
    for k in range(9):
        rect(c, x - w / 2 + w * 0.04 + k * w * 0.103, y - h * 0.32, w * 0.085, h * 0.5, "#14141c" if k != 8 else "#3a2a10", a)
    for k in range(40): rect(c, x - w / 2 + w * 0.03 + k * w * 0.0235, y + h / 2 - 12, w * 0.012, 12, "#d9b45a", a)
    rect(c, x - 8, y + h / 2 - 12, 16, 12, "#1f6a3a", a)

def computer_box(c, x, y, s, txt, colr=GREEN, a=1.0, bad=False):
    rrect(c, x - s / 2, y - s * 0.6, s, s * 1.2, s * 0.08, "#1b1420", a)
    rrect(c, x - s * 0.4, y - s * 0.48, s * 0.8, s * 0.5, s * 0.05, "#06110b", a)
    rrect(c, x - s / 2, y - s * 0.6, s, s * 1.2, s * 0.08, (RED if bad else colr), 0.6 * a, stroke=4)
    text(c, txt, x, y - s * 0.23, s * 0.28, RED if bad else colr, a, w=800, fam=MONO)
    for k in range(3): rect(c, x - s * 0.35, y + s * 0.12 + k * s * 0.13, s * 0.7, s * 0.06, "#2a2030", a)

def relay_cabinet(c, x, y, s, t, a=1.0, stop=0.0):
    rrect(c, x - s * 0.9, y - s, s * 1.8, s * 2, s * 0.05, "#2a2028", a)
    for r in range(7):
        for q in range(6):
            xx = x - s * 0.75 + q * s * 0.28; yy = y - s * 0.8 + r * s * 0.24
            rect(c, xx, yy, s * 0.2, s * 0.14, "#6a6070", a)
            on = (math.sin(t * 7 + r * 1.7 + q * 2.3) > 0.3) and stop < 0.5
            circle(c, xx + s * 0.1, yy + s * 0.07, s * 0.035, "#ffd27a" if on else "#3a3040", a)
    blink = stop * (0.5 + 0.5 * math.sin(t * 9))
    circle(c, x, y + s * 0.88, s * 0.08, RED, a * max(0.25, blink)); circle(c, x, y + s * 0.88, s * 0.2, RED, a * blink * 0.4, blur=s * 0.08)

def pyramid_section(c, cx, base, half, hgt, a=1.0):
    c.drawPath(poly([(cx - half, base), (cx, base - hgt), (cx + half, base)]), paint("#c9a46a", a))
    for k in range(1, 10):
        yy = base - hgt * k / 10; hw = half * (1 - k / 10)
        line(c, cx - hw, yy, cx + hw, yy, "#a8854f", 2, a * 0.6)
    c.drawPath(poly([(cx - half, base), (cx, base - hgt), (cx + half, base)]), paint("#8a6a3a", a, stroke=4))
    # grand gallery (sloped) + chamber
    c.drawPath(poly([(cx - half * 0.18, base - hgt * 0.22), (cx + half * 0.02, base - hgt * 0.42), (cx + half * 0.02, base - hgt * 0.37),
                     (cx - half * 0.18, base - hgt * 0.17)]), paint("#4a3420", a))
    rect(c, cx + half * 0.02, base - hgt * 0.45, half * 0.14, hgt * 0.08, "#4a3420", a)

# ------------------------------------------------------------------ motif + kit scenes
def motif_k(c, W, H, t, S, cx, cy, s, period=4.0, t0=0.8):
    u = S.u; cs = int(64 * s * u * (1.2 if S.P else 1))
    k = int(max(0.0, t - t0) // period); th = t0 + k * period
    rng = random.Random(77 + k); r_, q_ = rng.randrange(5), rng.randrange(9)
    pos, _ = grid(c, cx, cy, 9, 5, cs, seed=3, a=0.95, flips=[(r_, q_, prog(t, th, 0.35))])
    tx, ty = pos(r_, q_)
    strike(c, tx, ty, t, th, ang=55, speed=2400 * s * u, w=max(3, 7 * s * u), L=600 * s * u)

def bg_cos(c, W, H, t, S): bg_k(c, W, H, t, S)

def k_title(c, W, H, t, S): kit.title(c, W, H, t, S, bg_cos, motif_k, PAL)
def k_card(c, W, H, t, S):
    def cbg(c, W, H, t, S):
        bg_cos(c, W, H, t, S)
        with Layer(c, 0.35):
            motif_k(c, W, H, t, S, W / 2, H / 2, 1.5 if not S.P else 1.0, t0=0.3)
    kit.card(c, W, H, t, S, cbg, PAL)
def k_end(c, W, H, t, S): kit.end(c, W, H, t, S, bg_cos, motif_k, PAL)
def k_endshort(c, W, H, t, S): kit.end_short(c, W, H, t, S, bg_cos, motif_k, PAL)

# ------------------------------------------------------------------ k_vote
BITS13 = [1] + [0] * 12

def machine(c, x, y, s, a, extra=0.0, ts=1.0, glitch=0.0):
    rrect(c, x - 330 * s, y - 300 * s, 660 * s, 560 * s, 30 * s, "#1b1420", a)
    rrect(c, x - 330 * s, y - 300 * s, 660 * s, 560 * s, 30 * s, "#ffffff", 0.14 * a, stroke=3)
    rrect(c, x - 290 * s, y - 262 * s, 580 * s, 400 * s, 16 * s, "#06110b", a)
    rrect(c, x - 290 * s, y - 262 * s, 580 * s, 400 * s, 16 * s, GREEN, 0.5 * a, stroke=3)
    M(c, "VOTES", x - 260 * s, y - 210 * s, 34 * s, 1.0, GREEN, a)
    for i, (nm, v) in enumerate((("CAND. A", 0.55), ("CAND. B", 0.38), ("CAND. C", 0.62))):
        yy = y - 120 * s + i * 95 * s
        M(c, nm, x - 260 * s, yy, 28 * s, 1.0, GREEN, a * 0.9)
        L = v * 250 * s
        rect(c, x - 40 * s, yy - 18 * s, L, 36 * s, GREEN, a * 0.8)
        if i == 1 and extra > 0:
            rect(c, x - 40 * s + L, yy - 18 * s, extra * 0.42 * 250 * s, 36 * s, RED, a * (0.75 + 0.25 * glitch))
    for q in range(4): rrect(c, x - 150 * s + q * 80 * s, y + 165 * s, 60 * s, 40 * s, 8 * s, "#2a2030", a)
    rect(c, x - 60 * s, y + 260 * s, 120 * s, 110 * s, "#120d16", a)
    rrect(c, x - 200 * s, y + 360 * s, 400 * s, 30 * s, 10 * s, "#120d16", a)

def k_vote(c, W, H, t, S):
    o = S.opts; mode = o.get("mode", "intro"); txt = lines_text(S)
    if mode == "intro":
        nb = 3 if S.n() >= 3 else 1; B = beats(S, nb)
        jump = B(0, 0.55) if nb == 3 else S.lt(0, 0.45)
        def pA(c, ts):
            pj = prog(t, jump, 0.6); gl = 0.5 + 0.5 * math.sin(t * 20)
            if S.P:
                machine(c, 540, 500, 1.25, 1.0, extra=pj, glitch=gl)
                T(c, "+4,096", 1430, 440, 135, ts, RED, eout(pj), shadow=20, maxw=760)
                C(c, "BELGIUM · 2003", 1430, 720, vis(t, 0.3), ts, size=30, dot=GREEN)
            else:
                machine(c, 620, 500, 1.0, 1.0, extra=pj, glitch=gl)
                C(c, "SCHAERBEEK, BELGIUM", 1400, 230, vis(t, B(0, 0.08)), ts, dot=GREEN)
                C(c, "18 MAY 2003 · ELECTRONIC VOTING", 1400, 340, vis(t, B(0, 0.25)), ts, size=30)
                T(c, "+4,096", 1400, 560, 190, ts, RED, eout(pj), shadow=24)
                C(c, "EXTRA VOTES FOR ONE CANDIDATE", 1400, 760, vis(t, jump + 0.4), ts, size=32, bg="#3a0f1a")
        items = [(0, pA)]
        if nb == 3:
            def pB(c, ts):
                C(c, "A HACKER?", 520, 210, vis(t, B(1, 0.0)), ts, size=40)
                xmark(c, 800, 210, 34, prog(t, B(1, 0.12), 0.3))
                C(c, "A SOFTWARE BUG?", 1300, 210, vis(t, B(1, 0.18)), ts, size=40)
                xmark(c, 1660, 210, 34, prog(t, B(1, 0.3), 0.3))
                th = B(1, 0.62)
                xs = bitrow(c, 960, 560, BITS13 if t > th + 0.3 else [0] * 13, 110, flip=0, flip_p=prog(t, th, 0.35) if t <= th + 0.3 else 0,
                            glows=[clamp(1 - (t - th - 0.3)) if (k == 0 and t > th + 0.3) else 0 for k in range(13)])
                strike(c, xs[0], 560, t, th, ang=62, w=8)
                C(c, "A PARTICLE FROM SPACE", 960, 780, vis(t, th - 0.4), ts, dot=MAG)
                C(c, "ONE FLIPPED BIT", 960, 880, vis(t, th + 0.4), ts, size=40, bg=YEL, fg="#0b1030", a=1)
            def pC(c, ts):
                motif_k(c, VW, VH, t - B(2, 0), _FakeS(), 800, 540, 1.3, period=2.6, t0=0.4)
                T(c, "?", 1600, 540, 360, ts, GREEN, prog(t, B(2, 0.2), 0.5), shadow=30)
            items += [(B(1, 0), pB), (B(2, 0), pC)]
        run_panels(c, W, H, t, S, items)
    elif mode == "recount":
        two = S.n() >= 2 or "four thousand" in txt
        B = beats(S, 2) if two else (lambda i, f=0.0: S.lt(0, f))
        def pA(c, ts):
            gone = prog(t, B(0, 0.55) if two else S.lt(0, 0.55), 1.0)
            machine(c, 540 if S.P else 620, 500, 1.25 if S.P else 0.95, 1.0, extra=1 - eout(gone))
            stamp(c, "RECOUNT", 1430 if S.P else 1400, 300, prog(t, B(0, 0.25) if two else S.lt(0, 0.3), 0.4), 1.0, color=YEL, size=120 if S.P else 90)
            T(c, "−4,096", 1430 if S.P else 1400, 620, 150, ts, GREEN, eout(gone), shadow=20, maxw=780 if S.P else 1800)
            if not S.P: C(c, "THE TOTAL DIDN'T ADD UP", 1400, 800, vis(t, B(0, 0.05)), ts)
        items = [(0, pA)]
        if two:
            def pB(c, ts):
                th = B(1, 0.15)
                yb = 520 if not S.P else 480
                xs = bitrow(c, 960, yb, BITS13 if t > th + 0.35 else [0] * 13, 112 if not S.P else 130,
                            gap=None if not S.P else 7, flip=0, flip_p=prog(t, th, 0.35) if t <= th + 0.35 else 0, glows=[0.6 if k == 0 else 0 for k in range(13)])
                strike(c, xs[0], yb, t, th, ang=62, w=8)
                T(c, "4,096 = 2¹² = THE 13TH BIT", 960, 250 if not S.P else 200, 84, ts, YEL, prog(t, th + 0.3, 0.5), maxw=1800)
                if not S.P:
                    C(c, "MOST LIKELY CAUSE: A SINGLE-EVENT UPSET", 960, 800, vis(t, B(1, 0.55)), ts, size=38, dot=MAG)
                else:
                    C(c, "ONE FLIPPED BIT", 960, 760, vis(t, th + 0.6), ts, size=26, dot=MAG)
            items.append((B(1, 0), pB))
        run_panels(c, W, H, t, S, items)
    else:  # "bit"
        th = S.lt(0, 0.62)
        def pA(c, ts):
            C(c, "FRAUD", 560, 170, vis(t, S.lt(0, 0.05)), ts, size=34)
            xmark(c, 560 + (190 if not S.P else 300), 170, 34, prog(t, S.lt(0, 0.15), 0.3))
            C(c, "SOFTWARE BUG", 1300, 170, vis(t, S.lt(0, 0.2)), ts, size=34)
            xmark(c, 1300 + (290 if not S.P else 470), 170, 34, prog(t, S.lt(0, 0.3), 0.3))
            xs = bitrow(c, 960, 560, BITS13 if t > th + 0.35 else [0] * 13, 130 if S.P else 120, gap=7 if S.P else None, flip=0, flip_p=prog(t, th, 0.35) if t <= th + 0.35 else 0,
                        glows=[0.7 if (k == 0 and t > th) else 0 for k in range(13)])
            strike(c, xs[0], 560, t, th, ang=62, w=9)
            M(c, "MEMORY", 960, 820, 44, ts, GREEN, vis(t, 0.3), align="c")
        run_panels(c, W, H, t, S, [(0, pA)])

class _FakeS:
    """landscape-sized context for drawing the motif inside the virtual stage."""
    P = False; u = 1.0; W = VW; H = VH

# ------------------------------------------------------------------ k_bits
_ROWS = ["0110 1001 1100", "1011 0010 0111", "0001 1110 1010", "1100 0101 0011"]

def k_bits(c, W, H, t, S):
    o = S.opts; mode = o.get("mode", "default")
    if mode == "place":
        B = beats(S, 2)
        def pA(c, ts):
            s = 112 if not S.P else 130; yrow = 470 if not S.P else 430
            vals = [2 ** (12 - k) for k in range(13)]
            lit = [0] * 13; glows = [0] * 13
            # line 0: light 1, 2, 4, 8, 16 in turn (right to left)
            for j in range(5):
                tj = B(0, 0.12 + j * 0.16)
                if tj <= t < tj + 0.7 and t < B(1, 0): lit[12 - j] = 1; glows[12 - j] = 0.8
            th = B(1, 0.45) if S.n() >= 2 or S.P else B(1, 0.3)
            if t >= th: lit[0] = 1; glows[0] = clamp(0.4 + 0.6 * math.sin((t - th) * 4) ** 2)
            if S.n() >= 2 and B(1, 0.05) <= t < B(1, 0.35): lit[12] = 1; glows[12] = 0.6
            xs = bitrow(c, 960, yrow, lit, s, gap=7 if S.P else None, cols=[YEL if k == 0 and t >= th else GREEN for k in range(13)], glows=glows)
            for k, x in enumerate(xs):
                lab = f"{vals[k]:,}" if vals[k] >= 1000 else str(vals[k])
                pa = vis(t, B(0, 0.05 + (12 - k) * 0.035))
                ly = yrow + s * 0.95 + ((s * 0.45) if (S.P and k % 2 == 0) else 0)
                M(c, lab, x, ly, 30 if not S.P else 34, ts, YEL if (k == 0 and t >= th) else "#9fdcbf", pa, align="c", maxw=s * 2)
            val = sum(vals[k] for k in range(13) if lit[k])
            vy = 170 if not S.P else 150
            T(c, f"= {val:,}", 960, vy, 110, ts, YEL if t >= th else GREEN, vis(t, B(0, 0.1)), fam=MONO, w=800)
            if not S.P:
                C(c, "EACH BIT IS WORTH DOUBLE THE ONE BEFORE", 960, 860, vis(t, B(0, 0.2), B(1, 0.1)), ts, size=34)
                C(c, "LOW BIT: TINY CHANGE", 960, 860, vis(t, B(1, 0.1), th - 0.2), ts, size=36)
                C(c, "THE 13TH BIT = 4,096 · REMEMBER IT", 960, 860, vis(t, th + 0.2), ts, size=38, bg=YEL, fg="#0b1030", a=1)
        run_panels(c, W, H, t, S, [(0, pA)])
        return
    B = beats(S, 3)
    def pA(c, ts):
        icons = [(420, "PHOTO"), (960, "BANK BALANCE"), (1500, "GAME SCORE")]
        for k, (x, lab) in enumerate(icons):
            p = vis(t, B(0, 0.08 + k * 0.22))
            if p <= 0: continue
            y = 330
            if k == 0:
                rrect(c, x - 130, y - 100, 260, 200, 12, "#2a1a30", p); rrect(c, x - 130, y - 100, 260, 200, 12, "#ffffff", p * 0.6, stroke=4)
                c.drawPath(poly([(x - 110, y + 80), (x - 30, y - 30), (x + 30, y + 30), (x + 70, y - 10), (x + 110, y + 80)]), paint("#3a8f6a", p))
                circle(c, x + 70, y - 55, 22, YEL, p)
            elif k == 1:
                M(c, "$1,024.00", x, y, 64, ts, "#ffffff", p, align="c")
            else:
                M(c, "SCORE 0450", x, y, 60, ts, "#ffffff", p, align="c")
            T(c, lab, x, y + 150, 38, ts, "#cfc2d8", p, w=800)
            pr = prog(t, B(0, 0.2 + k * 0.22), 0.8)
            arrow(c, x, y + 195, x, y + 270, GREEN, 6, pr)
            for j, row in enumerate(_ROWS):
                n = int(len(row) * clamp(pr * 1.6 - j * 0.25))
                rr = _ROWS[(j + k) % 4][:n]
                M(c, rr, x, y + 330 + j * 62, 40, ts, GREEN, pr, align="c")
    def pB(c, ts):
        bits = [1, 0, 1, 1, 0, 0, 1, 0]
        xs = bitrow(c, 960, 500, bits, 160, gap=36)
        C(c, "MAIN MEMORY", 960, 210, vis(t, B(1, 0.0)), ts, size=40, dot=GREEN)
        pf = vis(t, B(1, 0.35)); pe = vis(t, B(1, 0.6))
        arrow(c, xs[0], 790, xs[0], 620, YEL, 6, pf); C(c, "CHARGED = 1", xs[0] + 120, 850, pf, ts, size=36, bg=YEL, fg="#0b1030", a=1)
        arrow(c, xs[5], 790, xs[5], 620, YEL, 6, pe); C(c, "EMPTY = 0", xs[5] + 40, 850, pe, ts, size=36)
    def pC(c, ts):
        x, y, s = 760, 560, 420
        wob = math.sin(t * 5) * 3 * prog(t, B(2, 0.4), 0.5)
        c.save(); c.translate(x, y); c.rotate(wob)
        cell(c, 0, 0, s, 1, digit=False)
        rng = random.Random(4)
        for k in range(16):
            ex = rng.uniform(-0.32, 0.32) * s + math.sin(t * 3 + k) * 8; ey = rng.uniform(-0.1, 0.42) * s + math.cos(t * 2.6 + k) * 8
            circle(c, ex, ey, 11, "#d8fff0", 0.9); text(c, "−", ex, ey - 1, 18, "#0b2a1a", 1, w=900)
        c.restore()
        T(c, "TINY BUCKETS", 1470, 420, 90, ts, GREEN, vis(t, B(2, 0.05)))
        T(c, "EASY TO TIP OVER", 1470, 560, 64, ts, "#ffffff", vis(t, B(2, 0.4)))
        strike(c, 1000, 560, t, B(2, 0.8), ang=30, w=7, ring=False)
    run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB), (B(2, 0), pC)])

# ------------------------------------------------------------------ k_shower
def atmosphere(c, ytop, ybot, a=1.0):
    c.drawRect(skia.Rect.MakeLTRB(-600, ytop, 2520, ybot), paint(shader=lin(0, ytop, 0, ybot, [(0, "#0a0418", 0), (0.4, "#1e0a3a", 0.6 * a), (1, "#3a1240", 0.9 * a)])))
    for k in range(4):
        yy = lerp(ytop + 60, ybot - 40, k / 3)
        line(c, -600, yy, 2520, yy, "#b48aff", 2, a * 0.18, dash=([18, 16], 0))

def ground(c, y, a=1.0, seed=8):
    def mk(cc):
        rng = random.Random(seed); x = 0
        while x < 3200:
            bw = rng.uniform(50, 120); bh = rng.uniform(40, 170)
            cc.drawRect(skia.Rect.MakeXYWH(x, 200 - bh, bw, bh + 2), paint("#120814"))
            for wy in range(int(bh / 26) - 1):
                for wx in range(int(bw / 22)):
                    if rng.random() < 0.4: cc.drawRect(skia.Rect.MakeXYWH(x + 8 + wx * 22, 200 - bh + 12 + wy * 26, 9, 11), paint("#ffd27a", 0.7))
            x += bw + rng.uniform(4, 14)
        cc.drawRect(skia.Rect.MakeXYWH(0, 198, 3200, 200), paint("#120814"))
    img = cached(("city", seed), 3200, 400, mk)
    draw_img(c, img, -640, y - 200, a)

def k_shower(c, W, H, t, S):
    o = S.opts; mode = o.get("mode", "default"); txt = lines_text(S)
    if mode == "altitude":
        B = beats(S, 3)
        def pA(c, ts):
            atmosphere(c, 120, 940)
            shower(c, 960, 60, 900, 2000, 1.0, seed=11, only="n")
            ground(c, 960)
            C(c, "NEUTRONS", 360, 220, vis(t, B(0, 0.1)), ts, size=44, dot="#e6e6f2")
            C(c, "THE MAIN TROUBLEMAKERS FOR CHIPS ON THE GROUND", 960, 1010, vis(t, B(0, 0.35)), ts, size=32)
        def pB(c, ts):
            x0, yb, yt = 330, 930, 170
            line(c, x0, yt, x0, yb, "#ffffff", 4, 0.8)
            for km in (0, 4, 8, 12):
                yy = lerp(yb, yt, km / 12); line(c, x0 - 14, yy, x0, yy, "#ffffff", 4, 0.8)
                M(c, f"{km} KM", x0 - 30, yy, 30, ts, "#cfc2d8", 1, align="r")
            yp = lerp(yb, yt, 11 / 12); yg = yb
            plane_icon(c, 560, yp, 70, vis(t, B(1, 0.1)))
            pbar = eout(prog(t, B(1, 0.25), 1.2))
            rect(c, 700, yp - 28, 1050 * pbar, 56, MAG, 0.85)
            T(c, "~300×", 700 + 1050 * pbar - 20, yp, 64, ts, "#ffffff", pbar, align="r", w=900)
            C(c, "AIRLINER CRUISING ALTITUDE", 1100, yp + 90, vis(t, B(1, 0.3)), ts, size=30)
            hut(c, 560, yg, 90, a=vis(t, B(1, 0.05)))
            rect(c, 700, yg - 70, 4 * pbar + 2, 56, MAG, 0.85)
            M(c, "SEA LEVEL ×1", 740, yg - 42, 36, ts, "#ffffff", vis(t, B(1, 0.15)))
            C(c, "NEUTRON FLUX", 1250, 250, vis(t, B(1, 0.0)), ts, size=36, dot=MAG)
        def pC(c, ts):
            plane_icon(c, 520, 330, 150)
            p = vis(t, B(2, 0.0))
            rrect(c, 330, 470, 380, 120, 20, "#1b1420", p); rrect(c, 330, 470, 380, 120, 20, GREEN, 0.6 * p, stroke=4)
            M(c, "FLIGHT COMPUTER", 520, 530, 30, ts, GREEN, p, align="c", maxw=360)
            C(c, "DESIGNED FOR THESE HITS", 520, 690, vis(t, B(2, 0.1)), ts, size=34)
            pm = vis(t, B(2, 0.42))
            c.drawPath(poly([(1050, 820), (1300, 380), (1550, 820)]), paint("#3a2440", pm))
            c.drawPath(poly([(1225, 512), (1300, 380), (1375, 512), (1330, 490), (1300, 520), (1265, 490)]), paint("#e8e0f0", pm))
            hut(c, 1300, 600, 70, a=pm)
            rect(c, 1600, 820, 300, 40, "#d9c08a", pm * 0.9); hut(c, 1750, 820, 70, a=pm)
            line(c, 980, 860, 1920, 860, "#3a2440", 6, pm)
            rain(c, t, 1100, 1500, 120, 600, n=7, seed=21, a=pm, w=4, period=1.4)
            rain(c, t, 1650, 1850, 380, 820, n=2, seed=22, a=pm, w=4, period=2.6)
            C(c, "MOUNTAIN TOWN: MORE HITS", 1300, 940, pm, ts, size=30)
            C(c, "BEACH: FEWER", 1760, 1010, vis(t, B(2, 0.65)), ts, size=30)
        run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB), (B(2, 0), pC)])
        return

    def p_rays(c, ts, t0, t1):
        galaxy(c, 1330, 470, 560, t)
        supernova(c, 380, 470, 50, t)
        for k in range(7):
            q = ((t - t0) * 0.32 + k / 7) % 1
            flier(c, 380 + q * 1500, 470 + math.sin(k * 2.1) * 220 * q, 1.0, t, a=math.sin(q * math.pi) ** 0.5, kind="p" if k % 3 else "n")
        C(c, "COSMIC RAYS", 380, 160, vis(t, t0 + 0.1), ts, size=44, dot=MAG)
        C(c, "MOSTLY PROTONS + ATOMIC NUCLEI", 960, 830, vis(t, lerp(t0, t1, 0.2), lerp(t0, t1, 0.45)), ts, size=34)
        C(c, "NEARLY THE SPEED OF LIGHT", 960, 830, vis(t, lerp(t0, t1, 0.45), lerp(t0, t1, 0.68)), ts, size=36)
        C(c, "MANY THOUGHT TO COME FROM EXPLODING STARS", 960, 830, vis(t, lerp(t0, t1, 0.68)), ts, size=32)
        if not S.P: T(c, "EXPLODING STAR", 380, 640, 34, ts, "#ffb3ec", vis(t, lerp(t0, t1, 0.68)), w=800)

    def p_hess(c, ts, t0, t1):
        atmosphere(c, 0, 960)
        line(c, -600, 960, 2520, 960, "#3a2440", 8)
        q = eout(prog(t, t0 + 0.6, (t1 - t0) * 0.75))
        by = lerp(800, 260, q)
        x0 = 330
        line(c, x0, 940, x0, 200, "#ffffff", 4, 0.8)
        for km in range(6):
            yy = lerp(940, 260, km / 5); line(c, x0 - 14, yy, x0, yy, "#ffffff", 4, 0.8)
            M(c, f"{km} KM", x0 - 26, yy, 30, ts, "#cfc2d8", 1, align="r")
        balloon(c, 800, by - 120, 80)
        meter(c, 1450, 560, 170, 0.15 + 0.8 * q, ts=ts)
        C(c, "1912 · VICTOR HESS", 1450, 200, vis(t, t0 + 0.2), ts, size=40, dot=YEL)
        C(c, "STRONGER HIGHER UP", 1450, 860, vis(t, lerp(t0, t1, 0.55), lerp(t0, t1, 0.8)), ts, size=36)
        C(c, "IT'S COMING FROM SPACE", 1450, 860, vis(t, lerp(t0, t1, 0.8)), ts, size=36, bg=YEL, fg="#0b1030", a=1)

    def p_omg(c, ts, t0, t1):
        pb = vis(t, t0 + 0.3)
        for k in range(4): line(c, 260 - k * 40, 470 + (k - 1.5) * 50, 400 - k * 40, 470 + (k - 1.5) * 50, "#ffffff", 5, pb * 0.5)
        baseball(c, 560, 470, 140, pb)
        T(c, "~95 KM/H", 560, 700, 64, ts, "#ffffff", pb)
        T(c, "=", 960, 470, 200, ts, YEL, vis(t, lerp(t0, t1, 0.35)))
        pp = vis(t, lerp(t0, t1, 0.45))
        circle(c, 1380, 470, 90, MAG, 0.25 * pp, blur=40); circle(c, 1380, 470, 12, HOT, pp)
        circle(c, 1380, 470, 30 + 10 * math.sin(t * 6), MAG, 0.6 * pp, stroke=4)
        T(c, "ONE PARTICLE", 1380, 700, 64, ts, MAG, pp)
        C(c, "1991 · THE 'OH-MY-GOD' PARTICLE", 960, 170, vis(t, lerp(t0, t1, 0.6)), ts, size=40, bg=YEL, fg="#0b1030", a=1)

    def p_cascade(c, ts, t0, t1, phone_at=None):
        atmosphere(c, 120, 940)
        g = lerp(40, 960, eout(prog(t, t0 + 0.3, max(1.0, (t1 - t0) * 0.7))))
        strike(c, 960, 80, t, t0 + 0.25, ang=90, w=8, ring=False)
        shower(c, 960, 80, 920, g, 1.0, seed=5)
        ground(c, 960)
        if phone_at:
            phone(c, phone_at, 830, 280, glow=0.6)
        if not S.P:
            C(c, "TOP OF THE ATMOSPHERE", 380, 140, vis(t, t0 + 0.2), ts, size=34)
            C(c, "A SHOWER OF PARTICLES", 1500, 600, vis(t, lerp(t0, t1, 0.4)), ts, size=38, dot=MAG)
        elif phone_at is None:
            C(c, "PARTICLE SHOWER", 960, 140, vis(t, t0 + 0.4), ts, size=30, dot=MAG)

    def p_muon(c, ts, t0, t1):
        rain(c, t, 200, 1720, 0, 1080, n=11, seed=7, w=5)
        person(c, 520, 900, 520, "#3a3048")
        phone(c, 960, 640, 300)
        laptop(c, 1420, 820, 230)
        line(c, 200, 902, 1720, 902, "#3a2440", 6)
        M(c, "μ", 520, 180, 70, ts, MAG, vis(t, t0 + 0.2), align="c")
        if not S.P:
            C(c, "MUONS", 960, 150, vis(t, t0 + 0.1), ts, size=44, dot=MAG)
            C(c, "~1 PER CM² EVERY MINUTE", 960, 1000, vis(t, lerp(t0, t1, 0.3)), ts, size=38, bg=YEL, fg="#0b1030", a=1)
        # 1 cm square marker on the phone
        pm = vis(t, lerp(t0, t1, 0.25))
        rect(c, 930, 590, 60, 60, YEL, pm, stroke=4)
        M(c, "1 CM²", 1080, 620, 30, ts, YEL, pm, align="l")

    if S.n() == 1:
        t0, t1 = 0.0, S.dur
        if "muon" in txt: items = [(0, lambda c, ts: p_muon(c, ts, t0, t1))]; zm = (1.3, 960, 620)
        else: items = [(0, lambda c, ts: p_cascade(c, ts, -0.2, t1 + 1.5, phone_at=960))]; zm = (1.25, 960, 560)
        run_panels(c, W, H, t, S, items, zoom=zm)
        return
    B = beats(S, 5)
    bnd = [B(i, 0) for i in range(5)] + [S.dur]
    fns = [p_rays, p_hess, p_omg, p_cascade, p_muon]
    items = [(bnd[i] if i else 0, (lambda f, a_, b_: (lambda c, ts: f(c, ts, a_, b_)))(fns[i], bnd[i], bnd[i + 1])) for i in range(5)]
    run_panels(c, W, H, t, S, items)

# ------------------------------------------------------------------ k_hit
def silicon(c, x0, y0, x1, y1, a=1.0):
    def mk(cc):
        w, h = x1 - x0, y1 - y0
        cc.drawRect(skia.Rect.MakeXYWH(0, 0, w, h), paint(shader=lin(0, 0, 0, h, [(0, "#2a1650", 1), (1, "#120a26", 1)])))
        for yy in range(20, int(h), 34):
            for xx in range(20 + (17 if (yy // 34) % 2 else 0), int(w), 34):
                cc.drawCircle(xx, yy, 4, paint("#7a64b8", 0.55))
        cc.drawRect(skia.Rect.MakeXYWH(0, 0, w, h), paint("#b48aff", 0.5, stroke=4))
    img = cached(("si", x0, y0, x1, y1), x1 - x0, y1 - y0, mk)
    draw_img(c, img, x0, y0, a)

def k_hit(c, W, H, t, S):
    short = S.n() < 4
    B = beats(S, 4) if not short else (lambda i, f=0.0: S.lt(0, f) if i == 0 else S.dur + 99)
    th = B(0, 0.25) if not short else S.lt(0, 0.15)
    tf0, tf1 = (B(0, 0.55), B(0, 0.85)) if not short else (S.lt(0, 0.45), S.lt(0, 0.75))
    def pA(c, ts):
        silicon(c, 300, 620, 1620, 960)
        T(c, "SILICON", 420, 1000 if not S.P else 1010, 36, ts, "#b48aff", 1, w=800, align="l")
        cx, cy, cs = 1080, 470, 190
        rect(c, cx - 30, cy + cs * 0.58, 60, 620 - (cy + cs * 0.58), "#4a3a60")
        fill = lerp(0, 1, ease(prog(t, tf0, tf1 - tf0)))
        cell(c, cx, cy, cs, 0, glow=0.8 if tf0 < t < tf1 + 0.6 else 0, col=RED if fill > 0.05 else GREEN, fill=fill)
        if not S.P: T(c, "MEMORY CELL", cx + 260, cy - 60, 40, ts, GREEN, 1, w=800, align="l")
        # charge trail along the particle path inside the silicon
        x_hit = 960; ang = 70; dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        tt = (620 - 470) / dy
        strike(c, x_hit, 620, t, th, ang=ang, w=8, ring=False)
        if t > th:
            age = t - th; drift = ease(prog(t, tf0 - 0.2, tf1 - tf0 + 0.2))
            for k in range(14):
                q = k / 13; px = x_hit + dx * q * 330; py = 620 + dy * q * 330
                if (t - th) * 2600 < q * 330: continue
                tx_, ty_ = cx + (k % 3 - 1) * 30, cy + 40
                ex, ey = lerp(px + 14, tx_, drift * (1 if k % 2 == 0 else 0)), lerp(py, ty_, drift * (1 if k % 2 == 0 else 0))
                al = clamp(1.2 - drift * (0.0 if k % 2 == 0 else 1.0)) * (1 - drift * (1 if k % 2 == 0 else 0) * 0.9)
                circle(c, ex, ey, 11, MAG, al); text(c, "−", ex, ey - 1, 18, "#ffffff", al, w=900)
                circle(c, px - 14, py, 11, "#ffb36b", clamp(1.2 - age / 3)); text(c, "+", px - 14, py - 1, 18, "#ffffff", clamp(1.2 - age / 3), w=900)
            if not S.P: C(c, "A TRAIL OF CHARGE", 560, 520, vis(t, th + 0.4), ts, size=34, dot=MAG)
        T(c, "0 → 1", 560, 300 if not S.P else 330, 150 if not S.P else 110, ts, RED, prog(t, tf1, 0.4), fam=MONO, w=800)
    items = [(0, pA)]
    if not short:
        def pB(c, ts):
            T(c, "0 → 1", 960, 300, 230, ts, RED, 1, fam=MONO, w=800)
            C(c, "SOFT ERROR", 560, 600, vis(t, B(1, 0.15)), ts, size=48, dot=MAG)
            C(c, "SINGLE-EVENT UPSET", 1360, 600, vis(t, B(1, 0.3)), ts, size=48, dot=MAG)
            pn = vis(t, B(1, 0.55))
            C(c, "NOTHING IS BROKEN", 960, 820, pn, ts, size=44, bg="#123d2a")
            check(c, 1330, 820, 34, pn)
        def pC(c, ts):
            xs = (360, 960, 1560); labs = ("UNUSED MEMORY", "PROGRAM CRASH", "A NUMBER CHANGES")
            for k in range(3):
                p = vis(t, B(2, 0.08 + k * 0.28))
                if p <= 0: continue
                x = xs[k]
                rrect(c, x - 260, 250, 520, 520, 26, "#160a12", p); rrect(c, x - 260, 250, 520, 520, 26, (GREEN, RED, YEL)[k], 0.6 * p, stroke=4)
                if k == 0:
                    grid(c, x, 440, 5, 3, 56, seed=8, a=p * 0.6); check(c, x, 650, 40, p)
                    T(c, "NOTHING HAPPENS", x, 720, 34, ts, CHECKC, p, w=800)
                elif k == 1:
                    rrect(c, x - 170, 330, 340, 230, 12, "#2a2030", p); rect(c, x - 170, 330, 340, 40, RED, p * 0.85)
                    xmark(c, x, 460, 50, p)
                    T(c, "CRASH", x, 640, 60, ts, RED, p)
                else:
                    M(c, "1,000", x, 400, 70, ts, GREEN, p, align="c")
                    arrow(c, x, 460, x, 540, YEL, 6, p)
                    M(c, "1,016", x, 610, 70, ts, RED, p, align="c")
                    T(c, "QUIETLY", x, 720, 34, ts, YEL, p, w=800)
                T(c, labs[k], x, 860, 40, ts, "#ffffff", p, w=900, maxw=600)
        def pD(c, ts):
            bits = [0, 1, 0, 0, 1, 0, 1, 1]; th2 = B(3, 0.25); s = 150
            n = len(bits); x0 = 960 - (n * s + (n - 1) * 27) / 2 + s / 2
            fl = [prog(t, th2 + k * 0.06, 0.35) for k in range(3)]
            cur = [b for b in bits]
            for i, b in enumerate(bits):
                x = x0 + i * (s + 27)
                if 2 <= i <= 4 and fl[i - 2] > 0:
                    f = lerp(b, 1 - b, eout(fl[i - 2])); cell(c, x, 520, s, 0, glow=0.6, col=RED, fill=f)
                else: cell(c, x, 520, s, b)
            strike(c, x0 + 2 * (s + 27), 520, t, th2, ang=8, w=8, speed=2000, ring=False)
            C(c, "ONE PARTICLE, SEVERAL BITS", 960, 230, vis(t, B(3, 0.05)), ts, size=44, dot=MAG)
            C(c, "MULTI-BIT UPSET: HARDER TO FIX", 960, 820, vis(t, B(3, 0.55)), ts, size=40, bg=YEL, fg="#0b1030", a=1)
        items += [(B(1, 0), pB), (B(2, 0), pC), (B(3, 0), pD)]
    run_panels(c, W, H, t, S, items, zoom=(1.3, 960, 640))

# ------------------------------------------------------------------ k_voyager
_EARTH = {}
def still_globe(c, x, y, R, rot, tilt):
    R = max(4, int(R) // 4 * 4); k = (R, rot, tilt)
    if k not in _EARTH:
        pad = int(R * 0.3); n = 2 * (R + pad)
        surf = skia.Surface(n, n); cc = surf.getCanvas(); cc.clear(skia.ColorTRANSPARENT)
        geo.globe(cc, n / 2, n / 2, R, rot=rot, tilt=tilt)
        _EARTH[k] = (surf.makeImageSnapshot(), pad)
    img, pad = _EARTH[k]
    c.drawImage(img, x - R - pad, y - R - pad, skia.SamplingOptions(skia.FilterMode.kLinear))
    return R

GARB = "#%&@!?*~^$<>{}|\\=+"
def datastream(c, x0, x1, y, t, a, garbled, ts, seed=3):
    if a <= 0: return
    rng = random.Random(seed + int(t * 8))
    n = 18
    for k in range(n):
        q = ((t * 0.35 + k / n) % 1)
        x = lerp(x1, x0, q)
        ch = rng.choice(GARB) if garbled else ("1" if (k * 7 + seed) % 3 else "0")
        M(c, ch, x, y + math.sin(k * 1.3 + t * 3) * (12 if garbled else 0), 40, ts, RED if garbled else GREEN, a * math.sin(q * math.pi) ** 0.6, align="c")

def k_voyager(c, W, H, t, S):
    short = S.n() < 4
    B = beats(S, 4)
    def pSAA(c, ts):
        ex, ey = 700, 560
        R = still_globe(c, ex, ey, 300, -35, -22)
        bx, by, _ = geo.globe_xy(-40, -27, ex, ey, R, -35, -22)
        # radiation belt band
        for k, (rr, al) in enumerate(((1.55, 0.35), (1.9, 0.22))):
            c.save(); c.translate(ex, ey); c.rotate(-8)
            pth = skia.Path(); pth.addOval(skia.Rect.MakeLTRB(-R * rr, -R * rr * 0.36, R * rr, R * rr * 0.36))
            c.drawPath(pth, paint(MAG, al, stroke=R * 0.18, blur=R * 0.05)); c.restore()
        pul = 0.6 + 0.4 * math.sin(t * 3)
        circle(c, bx, by, R * 0.33, MAG, 0.45 * pul, blur=R * 0.12)
        circle(c, bx, by, R * 0.22, "#ffb3ec", 0.35 * pul, blur=R * 0.06)
        # telescope orbit
        an = t * 0.55
        ox, oy = ex + math.cos(an) * R * 1.3, ey + math.sin(an) * R * 0.5
        inside = math.hypot(ox - bx, oy - by) < R * 0.55 and math.sin(an) > -0.2
        c.drawOval(skia.Rect.MakeLTRB(ex - R * 1.3, ey - R * 0.5, ex + R * 1.3, ey + R * 0.5), paint("#ffffff", 0.25, stroke=2, dash=([12, 10], 0)))
        telescope(c, ox, oy, 46, ang=math.degrees(an) + 90)
        if not S.P:
            C(c, "SOUTH ATLANTIC ANOMALY", 1460, 220, vis(t, B(0, 0.12)), ts, size=40, dot=MAG)
            C(c, "RADIATION BELTS DIP CLOSE", 1460, 340, vis(t, B(0, 0.3)), ts, size=34)
            st = vis(t, B(0, 0.55))
            C(c, "SCIENCE OBSERVATIONS: PAUSED" if inside else "SPACE TELESCOPE: OBSERVING", 1460, 820, st, ts, size=32,
              bg="#3a0f1a" if inside else "#123d2a", dot=RED if inside else GREEN)
    def pVoy(c, ts, t0, t1):
        sp = lambda f: lerp(t0, t1, f)
        exx = 260 if S.P else 150; pxx = 1540 if S.P else 1640
        circle(c, exx, 480, 26, "#4f9bff"); circle(c, exx, 480, 60, "#4f9bff", 0.25, blur=20)
        T(c, "EARTH", exx, 560, 30, ts, "#9fc7ff", 1, w=800)
        probe(c, pxx, 470, 110)
        line(c, 230, 300, 1500, 300, "#ffffff", 3, 0.5, dash=([16, 14], 0))
        T(c, "MORE THAN 13 BILLION KM", 860, 250, 44, ts, "#ffffff", vis(t, t0 + 0.2), w=800)
        if not short: C(c, "2010 · VOYAGER 2", 860, 140, vis(t, t0 + 0.1), ts, size=40, dot=YEL)
        tg = sp(0.3 if short else 0.25); tfix = sp(0.62 if short else 1.6)
        garbled = tg < t < tfix + 0.3
        datastream(c, exx + 80, pxx - 140, 470, t, vis(t, t0 + 0.3), garbled, ts)
        if t < tg: pass
        # zoomed memory row + command
        tz = sp(0.42) if short else sp(1.0)
        pz = vis(t, tz)
        if pz > 0:
            rrect(c, 420, 640, 1080, 300, 24, "#160a12", pz * 0.95); rrect(c, 420, 640, 1080, 300, 24, GREEN, pz * 0.5, stroke=3)
            flipped = t < tfix + 0.3
            bits = [0, 1, 1, 0, 1, 0, 0, 1]
            fp = 1 - prog(t, tfix, 0.35)
            xs = bitrow(c, 960, 770, bits, 100, a=pz, flip=3, flip_p=fp if flipped else 0)
            M(c, "DATA COMPUTER MEMORY", 960, 690, 30, ts, GREEN, pz, align="c")
            # command packets
            tc = tfix - (0.9 if short else 1.6)
            if tc < t < tfix:
                q = prog(t, tc, tfix - tc)
                for k in range(4):
                    qq = clamp(q * 1.3 - k * 0.1)
                    if 0 < qq < 1: circle(c, lerp(200, 1560, qq), 400, 12, YEL, 1)
                if not S.P: T(c, "COMMAND: FLIP IT BACK", 860, 360, 36, ts, YEL, 1, w=800)
            if t > tfix + 0.3:
                check(c, 1650, 770, 40, vis(t, tfix + 0.3))
    def pSus(c, ts):
        probe(c, 960, 520, 140, 0.6)
        rain(c, t, 300, 1620, 100, 900, n=8, seed=17, w=5)
        C(c, "RADIATION: THE USUAL SUSPECT", 960, 200, vis(t, B(3, 0.1)), ts, size=44, dot=MAG)
        stamp(c, "NOT PROVEN", 960, 860, prog(t, B(3, 0.45), 0.4), 1.0, color=YEL, size=80)
    if short:
        run_panels(c, W, H, t, S, [(0, lambda c, ts: pVoy(c, ts, 0.0, S.dur))], zoom=(1.1, 900, 600))
        return
    run_panels(c, W, H, t, S, [(0, pSAA), (B(1, 0), lambda c, ts: pVoy(c, ts, B(1, 0), B(2, 0))), (B(3, 0), pSus)])

# ------------------------------------------------------------------ k_game
def k_game(c, W, H, t, S):
    B = beats(S, 2); th = B(0, 0.55)
    def pA(c, ts):
        def mk(cc):
            block_row(cc, 0, 1920, 0, 80, colr="#4a2036"); block_row(cc, 0, 1920, 80, 80, colr="#3a1a2c")
        img = cached(("floor",), 1920, 160, mk)
        draw_img(c, img, 0, 880)
        def mk2(cc): block_row(cc, 0, 560, 0, 70, colr="#5a2a46")
        draw_img(c, cached(("plat",), 560, 70, mk2), 1060, 450)
        up = prog(t, th + 0.05, 0.45)
        x = lerp(1180, 1300, ease(up))
        y = 880 if up <= 0 else lerp(880, 450, eback(up))
        if 0 < up < 1:
            for k in range(3): line(c, x - 40 + k * 40, y + 30, x - 40 + k * 40, y + 160, "#ffffff", 4, 0.5 * (1 - up))
        robot(c, x, y, 110, t, squash=clamp(1 - abs(t - th - 0.5) * 6) if up > 0.95 else 0)
        # height register
        rrect(c, 120, 140, 760, 250, 20, "#06110b", 0.95); rrect(c, 120, 140, 760, 250, 20, GREEN, 0.6, stroke=3)
        M(c, "HEIGHT", 160, 200, 36, ts, GREEN, 1)
        bits = [0, 0, 0, 1, 0, 1, 1, 0, 1, 0]
        xs = bitrow(c, 500, 300, bits, 62, flip=2, flip_p=prog(t, th, 0.3), gap=10)
        strike(c, xs[2], 300, t, th, ang=60, w=7)
        C(c, "2013 · A LIVESTREAMED SPEEDRUN", 1340, 160, vis(t, B(0, 0.08)), ts, size=34)
        if S.n() >= 2:
            C(c, "THEORY: ONE BIT OF THE HEIGHT FLIPPED", 960, 1010 if not S.P else 1000, vis(t, B(1, 0.05)), ts, size=34, dot=MAG)
            stamp(c, "NEVER PROVEN", 560, 640, prog(t, B(1, 0.5), 0.4), 1.0, color=YEL, size=80)
    run_panels(c, W, H, t, S, [(0, pA)])

# ------------------------------------------------------------------ k_alpha
def k_alpha(c, W, H, t, S):
    B = beats(S, 2)
    def pA(c, ts):
        cx, cy = 960, 560
        package(c, cx, cy, 1100, 460)
        fix = prog(t, B(1, 0.2), 0.8)
        pos, _ = grid(c, cx, cy, 6, 3, 52, seed=12)
        rng = random.Random(5)
        specks = [(cx + rng.choice([-1, 1]) * rng.uniform(300, 500), cy + rng.uniform(-180, 180), rng.choice(["U", "Th"])) for _ in range(6)]
        hits = []
        for k, (sx, sy, lab) in enumerate(specks):
            al = (1 - fix) * vis(t, B(0, 0.3))
            circle(c, sx, sy, 16, "#ff9a3a", al); circle(c, sx, sy, 34, "#ff9a3a", 0.3 * al, blur=12)
            text(c, lab, sx, sy - 34, 26, "#7a3a10", al, w=900)
            per = 2.2 + k * 0.37; q = ((t + k * 0.9) % per) / per
            r_, q_ = k % 3, (k * 2 + 1) % 6
            tx, ty = pos(r_, q_)
            if q < 0.4 and al > 0.05:
                f = q / 0.4; ax, ay = lerp(sx, tx, f), lerp(sy, ty, f)
                circle(c, ax - 5, ay, 7, RED, al); circle(c, ax + 5, ay, 7, "#e6e6f2", al)
                circle(c, ax, ay, 22, MAG, 0.35 * al, blur=8)
            elif q < 0.65 and al > 0.05:
                hits.append((r_, q_, (q - 0.4) / 0.25 * 0.9 + 0.1))
        for (r_, q_, p) in hits:
            x, y = pos(r_, q_); cell(c, x, y, 52, 0, glow=1 - p, col=RED, fill=1)
        C(c, "1978 · INTEL: TIMOTHY MAY & MURRAY WOODS", 960, 140, vis(t, B(0, 0.05)), ts, size=34, dot=YEL)
        C(c, "TRACES OF URANIUM + THORIUM IN THE PACKAGING", 960, 940, vis(t, B(0, 0.4), B(1, 0.15)), ts, size=32, dot="#ff9a3a")
        C(c, "THEY GIVE OFF ALPHA PARTICLES", 960, 1030 if not S.P else 1040, vis(t, B(0, 0.65), B(1, 0.15)), ts, size=30, dot=RED)
        pf = vis(t, B(1, 0.3))
        C(c, "FIX: PURER MATERIALS", 960, 960, pf, ts, size=44, bg="#123d2a")
        check(c, 1300, 960, 34, pf)
    run_panels(c, W, H, t, S, [(0, pA)])

# ------------------------------------------------------------------ k_squat
def k_squat(c, W, H, t, S):
    B = beats(S, 2); th = B(0, 0.45)
    def pA(c, ts):
        flipped = t > th + 0.2
        rrect(c, 260, 160, 1400, 130, 65, "#1b1420"); rrect(c, 260, 160, 1400, 130, 65, "#ffffff", 0.3, stroke=3)
        circle(c, 330, 225, 22, "#ffffff", 0.3, stroke=4)
        dom = "loudnote.example"
        w1 = tw("c" + dom, 64, 800, MONO); x0 = 960 - w1 / 2; wc = tw("c", 64, 800, MONO)
        text(c, "k" if flipped else "c", x0, 225, 64, RED if flipped else "#ffffff", 1, w=800, fam=MONO, align="l")
        text(c, dom, x0 + wc, 225, 64, "#ffffff", 1, w=800, fam=MONO, align="l")
        M(c, "MADE-UP EXAMPLE", 1630, 330, 26, ts, "#cfc2d8", 0.8, align="r")
        # ascii of the first letter
        bits = [0, 1, 1, 0, 0, 0, 1, 1]
        line(c, x0 + wc / 2, 270, 560, 440, "#ffffff", 3, 0.4)
        xs = bitrow(c, 760, 520, bits, 90, flip=4, flip_p=prog(t, th, 0.35), gap=14)
        strike(c, xs[4], 520, t, th, ang=58, w=7)
        M(c, "'c' = 01100011" if not flipped else "'k' = 01101011", 760, 660, 40, ts, RED if flipped else GREEN, 1, align="c")
        # lookalike server
        pr = prog(t, th + 0.6, 1.0)
        if pr > 0:
            rrect(c, 1450, 430, 260, 300, 18, "#1b1420", pr); rrect(c, 1450, 430, 260, 300, 18, RED, 0.6 * pr, stroke=4)
            for k in range(4): rect(c, 1480, 465 + k * 60, 200, 34, "#2a2030", pr); circle(c, 1660, 482 + k * 60, 7, GREEN, pr)
            T(c, "LOOKALIKE SITE", 1580, 790, 34, ts, RED, pr, w=800)
            for k in range(3):
                q = ((t - th) * 0.8 + k / 3) % 1
                circle(c, lerp(1250, 1440, q), 580, 10, YEL, pr * math.sin(q * math.pi))
        if S.n() >= 2:
            pc = vis(t, B(1, 0.05))
            rrect(c, 330, 800, 960, 230, 24, "#160a12", pc); rrect(c, 330, 800, 960, 230, 24, YEL, 0.6 * pc, stroke=3)
            n = int(52317 * ease(prog(t, B(1, 0.1), (B(1, 0.85) - B(1, 0.1)))))
            M(c, f"{n:,}", 810, 880, 90, ts, YEL, pc, align="c")
            T(c, "REQUESTS IN ~7 MONTHS", 810, 975, 36, ts, "#ffffff", pc, w=800)
            C(c, "2011 · ARTEM DINABURG", 1500, 900, vis(t, B(1, 0.3)), ts, size=30)
    run_panels(c, W, H, t, S, [(0, pA)])

# ------------------------------------------------------------------ k_rate
def k_rate(c, W, H, t, S):
    B = beats(S, 3)
    cards = [("1990s · IBM ESTIMATE", "~1 / MONTH", "ERROR PER 256 MB OF MEMORY", "OTHER ESTIMATES: FAR LOWER", GREEN),
             ("2009 · GOOGLE SERVERS", ">8%", "OF MEMORY MODULES: AN ERROR A YEAR", "MANY FROM WORN OR FAULTY CHIPS", YEL),
             ("2026 · MOZILLA ENGINEER", "~1 IN 10", "FIREFOX CRASHES LOOK LIKE BIT FLIPS", "MOSTLY BAD MEMORY", RED)]
    def pA(c, ts):
        for k, (top, big, sub, foot, col_) in enumerate(cards):
            p = vis(t, B(k, 0.03))
            if p <= 0: continue
            cur = B(k, 0) <= t < (B(k + 1, 0) if k < 2 else 1e9)
            dim = 1.0 if cur else 0.55
            x = 340 + k * 620; y0 = 180
            c.save(); c.translate(x, 540); sc = 1.0 if cur else 0.94; c.scale(sc, sc); c.translate(-x, -540)
            rrect(c, x - 285, y0, 570, 740, 28, "#160a12", p); rrect(c, x - 285, y0, 570, 740, 28, col_, 0.65 * p * dim, stroke=5)
            T(c, top, x, y0 + 70, 34, ts, "#cfc2d8", p * dim, w=800, maxw=520)
            T(c, big, x, y0 + 250, 110, ts, col_, p * dim, maxw=520)
            words = sub.split(" "); half = len(words) // 2 + 1
            T(c, " ".join(words[:half]), x, y0 + 420, 34, ts, "#ffffff", p * dim, w=800, maxw=520)
            T(c, " ".join(words[half:]), x, y0 + 470, 34, ts, "#ffffff", p * dim, w=800, maxw=520)
            pf = vis(t, B(k, 0.5)) * dim
            line(c, x - 200, y0 + 560, x + 200, y0 + 560, "#ffffff", 2, 0.3 * pf)
            fw = foot.split(" "); h2 = (len(fw) + 1) // 2
            T(c, " ".join(fw[:h2]), x, y0 + 620, 30, ts, "#cfc2d8", pf, w=700, fam="Inter", maxw=520)
            T(c, " ".join(fw[h2:]), x, y0 + 665, 30, ts, "#cfc2d8", pf, w=700, fam="Inter", maxw=520)
            c.restore()
    run_panels(c, W, H, t, S, [(0, pA)])

# ------------------------------------------------------------------ k_ecc
def k_ecc(c, W, H, t, S):
    o = S.opts; mode = o.get("mode", "default")
    if mode == "vote":
        B = beats(S, 2)
        def pA(c, ts):
            server_stick(c, 480, 300, 640)
            C(c, "ECC MEMORY · SERVERS", 480, 450, vis(t, B(0, 0.05)), ts, size=34, dot=GREEN)
            pc = vis(t, B(0, 0.3))
            bits = [1 if (k * 5 + 3) % 7 < 3 else 0 for k in range(39)]
            cols = [GREEN] * 32 + [YEL] * 7
            s = 40; x0 = 960 - (39 * s + 38 * 4) / 2 + s / 2
            with Layer(c, pc) as on:
                if on:
                    sweep = ((t - B(0, 0.4)) / 3.0) % 1 if t > B(0, 0.4) else -1
                    for k in range(39):
                        x = x0 + k * (s + 4)
                        g = clamp(1 - abs((x - x0) / (39 * (s + 4)) - sweep) * 12) if sweep >= 0 else 0
                        cell(c, x, 700, s, bits[k], glow=g, col=cols[k])
                    M(c, "32 DATA BITS", x0 + 16 * (s + 4) - s / 2, 790, 32, ts, GREEN, 1, align="c")
                    M(c, "+ 7 CHECK", x0 + 35 * (s + 4), 790, 32, ts, YEL, 1, align="c")
            C(c, "CASSINI'S DATA RECORDERS", 1380, 300, vis(t, B(0, 0.3)), ts, size=36, dot=YEL)
            C(c, "SCRUBBED EVERY 9 MINUTES", 960, 920, vis(t, B(0, 0.6)), ts, size=38)
        def pB(c, ts):
            vals = ["OK", "OK", "OK", "OK"]
            for k in range(4):
                p = vis(t, B(1, 0.05 + k * 0.06))
                computer_box(c, 330 + k * 320, 430, 220, vals[k], a=p)
                arrow(c, 330 + k * 320, 590, lerp(330 + k * 320, 810, 0.75), 760, GREEN, 5, vis(t, B(1, 0.4)))
            pv = vis(t, B(1, 0.45))
            rrect(c, 640, 760, 340, 110, 20, "#123d2a", pv); T(c, "AGREE", 810, 815, 50, ts, CHECKC, pv); check(c, 950, 815, 26, pv)
            pb = vis(t, B(1, 0.3))
            computer_box(c, 1620, 430, 220, "BACKUP", colr=YEL, a=pb)
            C(c, "SPACE SHUTTLE: 5 COMPUTERS · 4 COMPARE ANSWERS", 960, 160, vis(t, B(1, 0.15)), ts, size=34, dot=YEL)
        run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB)])
        return
    B = beats(S, 3)
    def pA(c, ts):
        with Layer(c, 0.55): motif_k(c, VW, VH, t, _FakeS(), 960, 470, 1.35, period=2.2, t0=0.3)
        p = vis(t, B(0, 0.25))
        sh = skia.Path(); sh.moveTo(960, 230); sh.lineTo(1160, 310); sh.lineTo(1140, 570); sh.quadTo(1080, 710, 960, 760)
        sh.quadTo(840, 710, 780, 570); sh.lineTo(760, 310); sh.close()
        c.drawPath(sh, paint("#123d2a", 0.9 * p)); c.drawPath(sh, paint(GREEN, p, stroke=8))
        check(c, 960, 490, 80, p)
        T(c, "ENGINEERS FIGHT BACK", 960, 960, 70, ts, "#ffffff", vis(t, B(0, 0.35)))
    def pB(c, ts):
        stop = clamp((math.sin(t * 0.9) + 0.3) * 3)
        relay_cabinet(c, 560, 560, 300, t, stop=stop)
        rrect(c, 1180, 300, 260, 300, 18, "#e8e0d0"); rect(c, 1180, 300, 260, 70, RED)
        T(c, "SAT · SUN", 1310, 335, 34, ts, "#ffffff", 1, w=900)
        M(c, "ERROR", 1310, 470, 50, ts, RED, 1, align="c")
        M(c, "STOP", 1310, 540, 40, ts, "#1b1420", 1, align="c")
        C(c, "1950 · RICHARD HAMMING · BELL LABS", 1310, 160, vis(t, B(1, 0.05)), ts, size=34, dot=YEL)
        C(c, "ERRORS KEPT STOPPING HIS WEEKEND JOBS", 1310, 740, vis(t, B(1, 0.3)), ts, size=30)
        C(c, "SO HE INVENTED ERROR-CORRECTING CODES", 1310, 860, vis(t, B(1, 0.7)), ts, size=30, bg=YEL, fg="#0b1030", a=1)
    def pC(c, ts):
        bits = [1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1]
        cols = [GREEN] * 8 + [YEL] * 4
        tf, tl, tb = B(2, 0.2), B(2, 0.45), B(2, 0.72)
        s = 120; gap = 22; n = 12
        x0 = 960 - (n * s + (n - 1) * gap) / 2 + s / 2
        for i in range(n):
            x = x0 + i * (s + gap) + (40 if i >= 8 else 0)
            if i == 5 and tf < t < tb + 0.4:
                f = lerp(0, 1, eout(prog(t, tf, 0.3))) if t < tb else lerp(1, 0, eout(prog(t, tb, 0.35)))
                cell(c, x, 540, s, 0, glow=0.7, col=RED if t < tb + 0.2 else GREEN, fill=f)
            else:
                cell(c, x, 540, s, bits[i], col=cols[i], glow=0.6 if (i >= 8 and tl < t < tb) else 0)
        strike(c, x0 + 5 * (s + gap), 540, t, tf, ang=60, w=7)
        if tl < t < tb + 0.5:
            pa = prog(t, tl, 0.4)
            for i in range(8, 12):
                xc = x0 + i * (s + gap) + 40
                arrow(c, xc, 640, lerp(xc, x0 + 5 * (s + gap), pa), lerp(640, 640, pa), YEL, 4, 0.8 * pa)
        M(c, "DATA BITS", x0 + 3.5 * (s + gap), 360, 40, ts, GREEN, vis(t, B(2, 0.0)), align="c")
        M(c, "CHECK BITS", x0 + 9.5 * (s + gap) + 40, 360, 40, ts, YEL, vis(t, B(2, 0.05)), align="c")
        C(c, "FOUND IT · FLIPPED BACK", 960, 840, vis(t, tb + 0.2), ts, size=40, bg="#123d2a")
        check(c, 1290, 840, 30, vis(t, tb + 0.3))
    run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB), (B(2, 0), pC)])

# ------------------------------------------------------------------ k_twist
def k_twist(c, W, H, t, S):
    B = beats(S, 3)
    def pA(c, ts):
        motif_k(c, VW, VH, t, _FakeS(), 960, 470, 1.3, period=1.8, t0=0.2)
        T(c, "COSMIC RAYS HELP, TOO", 960, 930, 80, ts, YEL, vis(t, B(0, 0.1)))
    def pB(c, ts):
        rrect(c, 120, 470, 620, 140, 30, "#4a4a5a"); rrect(c, 120, 470, 620, 140, 30, "#ffffff", 0.3, stroke=4)
        for k in range(5): rect(c, 180 + k * 110, 460, 30, 160, "#6a6a7a")
        rng = random.Random(3)
        for k in range(26):
            q = ((t * 1.4 + k / 26) % 1); y = 540 + rng.uniform(-50, 50)
            circle(c, lerp(740, 1240, q), y, 7, "#e6e6f2", 0.9 * (1 - q * 0.3))
        rrect(c, 1250, 340, 360, 420, 16, "#1f6a3a"); rrect(c, 1250, 340, 360, 420, 16, GREEN, 0.5, stroke=3)
        for r in range(3):
            for q in range(2):
                fl = 0.5 + 0.5 * math.sin(t * 9 + r * 2 + q * 3)
                rect(c, 1300 + q * 160, 380 + r * 125, 110, 90, "#14141c"); rect(c, 1300 + q * 160, 380 + r * 125, 110, 90, RED, 0.25 * fl)
        rect(c, 1410, 760, 40, 160, "#5a5a6a"); rect(c, 1330, 910, 200, 20, "#5a5a6a")
        clock(c, 1760, 230, 90, (t * 0.8) % 1)
        C(c, "NEUTRON BEAM TESTS", 430, 230, vis(t, B(1, 0.05)), ts, size=40, dot="#e6e6f2")
        C(c, "YEARS OF HITS → A FEW HOURS", 960, 1000, vis(t, B(1, 0.4)), ts, size=40, bg=YEL, fg="#0b1030", a=1)
    def pC(c, ts):
        cx, base, half, hgt = 960, 900, 600, 620
        pyramid_section(c, cx, base, half, hgt)
        rain(c, t, 360, 1560, 0, 900, n=10, seed=31, w=4, ang=88)
        for k in range(3): rect(c, cx - 260 + k * 200, base - 30, 120, 22, GREEN, 0.9)
        pv = prog(t, B(2, 0.5), 0.6)
        vx0, vy0 = cx - half * 0.16, base - hgt * 0.56
        c.drawPath(poly([(vx0, vy0), (vx0 + half * 0.36, vy0 - hgt * 0.1), (vx0 + half * 0.36, vy0 - hgt * 0.04), (vx0, vy0 + hgt * 0.06)]),
                   paint(MAG, 0.35 * pv))
        c.drawPath(poly([(vx0, vy0), (vx0 + half * 0.36, vy0 - hgt * 0.1), (vx0 + half * 0.36, vy0 - hgt * 0.04), (vx0, vy0 + hgt * 0.06)]),
                   paint(MAG, pv, stroke=6, dash=([16, 10], -t * 30)))
        C(c, "2017 · MUONS SEE INSIDE THE GREAT PYRAMID", 960, 120, vis(t, B(2, 0.05)), ts, size=36, dot=MAG)
        C(c, "HIDDEN VOID · AT LEAST 30 M LONG", 1380, 330, vis(t, B(2, 0.6)), ts, size=34, bg=YEL, fg="#0b1030", a=1)
        M(c, "DETECTORS", cx, base + 60, 30, ts, GREEN, vis(t, B(2, 0.2)), align="c")
    run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB), (B(2, 0), pC)])

SCENES = {k: v for k, v in globals().items() if k.startswith("k_") and callable(v)}
