"""Batch 04 scenes: What If You Shrank Down Inside a Computer Chip? (+ shrink, EUV and Moore's-law Shorts).

Look: a neon micro-city. Deep indigo/violet backgrounds, neon cyan traces, magenta accents, copper wiring,
silicon grey-blue. Signature motifs: an isometric chip die / stacked copper wiring levels, and a small glowing
"explorer" (generic humanoid outline) with a scale bar in every scale scene so you always know your size.
Every scene draws on a virtual 1920x1080 Stage; Shorts scale it into the 0.255H..0.58H band (text x1.75).
"""
from common2 import *
import scenes_b3_kit as kit

BG_T, BG_B = "#07051a", "#1a0f3d"
CY = "#36e7ff"
MG = "#ff3fb4"
CU, CU2 = "#e08a4a", "#ffb27a"
SI = "#8a9bc4"
VIO = "#6b4bd8"
CHIPBG = "#1d1347"
PAL = dict(accent=CY, chip="#2a1a5c", title2=ACCENT)
VW, VH = 1920, 1080

# ------------------------------------------------------------------ stage helpers
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
    """Chip on the virtual stage; centre is clamped so the chip never runs off the 1920-wide stage."""
    kw.setdefault("bg", CHIPBG)
    if kw.get("align", "c") == "c":
        sz = size * ts * 1.15; wch = tw(s, sz, 700, "Inter") + 2 * sz * 0.62 + (sz * 0.9 if kw.get("dot") else 0)
        x = clamp(x, 24 + wch / 2, VW - 24 - wch / 2) if wch < VW - 48 else VW / 2
    chip(c, s, x, y, p, size * ts, **kw)

def T(c, s, x, y, size, ts, colr="#ffffff", a=1.0, w=900, maxw=1800, **kw):
    sz = fit(s, min(maxw, VW - 60), size * ts, w)
    if kw.get("align", "c") == "c":
        wd = tw(s, sz, w); x = clamp(x, 30 + wd / 2, VW - 30 - wd / 2)
    text(c, s, x, y, sz, colr, a, w=w, shadow=kw.pop("shadow", 10), **kw)

def BB(S, E, keep=None):
    """Beat times. Long-form: beats(S, E). Shorts with fewer lines: only the beats in `keep` are shown,
    spread across the scene; earlier beats count as already done, later ones never happen."""
    if S.n() >= E or keep is None: return beats(S, E)
    keep = list(keep); n = len(keep); span = max(0.5, S.dur * 0.8)
    def g(i, f=0.0):
        if i in keep: return span * (keep.index(i) + f) / n
        return -99.0 if i < keep[0] else S.dur + 99
    return g

# ------------------------------------------------------------------ background: faint circuit traces + pulses
def _polyline_pt(pts, q):
    segs = [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    L = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in segs]; tot = sum(L) or 1
    d = q * tot
    for (a, b), l in zip(segs, L):
        if d <= l:
            f = d / l if l else 0; return a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f
        d -= l
    return pts[-1]

@lru_cache(maxsize=4)
def _traces(W, H, seed=4):
    rng = random.Random(seed); g = 60 * min(W, H) / 1080
    surf = skia.Surface(W, H); cc = surf.getCanvas(); cc.clear(skia.ColorTRANSPARENT)
    paths = []
    for k in range(int(W * H / 26000)):
        x = round(rng.uniform(0, W) / g) * g; y = round(rng.uniform(0, H) / g) * g; pts = [(x, y)]
        for s in range(rng.randint(2, 5)):
            if s % 2 == 0: x += rng.choice((-1, 1)) * rng.randint(1, 5) * g
            else: y += rng.choice((-1, 1)) * rng.randint(1, 4) * g
            pts.append((x, y))
        colr = CY if rng.random() < 0.75 else MG
        cc.drawPath(poly(pts, close=False), paint(colr, 0.13, stroke=2.2 * g / 60))
        for p_ in (pts[0], pts[-1]):
            cc.drawCircle(p_[0], p_[1], 4.5 * g / 60, paint(colr, 0.22))
        if len(paths) < 14: paths.append((pts, colr))
    return surf.makeImageSnapshot(), paths

@lru_cache(maxsize=4)
def _bg_full(W, H):
    surf = skia.Surface(W, H); cc = surf.getCanvas()
    fill_bg(cc, W, H, BG_T, BG_B)
    cc.drawImage(_traces(W, H)[0], 0, 0)
    cc.drawPaint(paint(shader=rad(W / 2, H / 2, max(W, H) * 0.75, [(0.5, "#000000", 0), (1, "#000000", 0.45)])))
    return surf.makeImageSnapshot()

def bg_chip(c, W, H, t, S, a=1.0):
    c.drawImage(_bg_full(W, H), 0, 0)
    img, paths = _traces(W, H)
    for k, (pts, colr) in enumerate(paths):
        q = (t * 0.18 + k * 0.137) % 1
        x, y = _polyline_pt(pts, q)
        al = a * math.sin(q * math.pi)
        circle(c, x, y, 5 * S.u, colr, 0.75 * al); circle(c, x, y, 14 * S.u, colr, 0.18 * al)

# ------------------------------------------------------------------ props
def explorer(c, x, y, h, a=1.0, t=0.0, colr=CY, walk=0.0, glow=True):
    """Generic glowing figure standing with feet at (x, y)."""
    if a <= 0.01 or h <= 0: return
    if glow and h > 20: circle(c, x, y - h * 0.5, h * 0.55, colr, 0.16 * a, blur=h * 0.25)
    sw = math.sin(t * 6) * walk
    hx, hy, hr = x, y - h + h * 0.11, h * 0.11
    lw = max(1.5, h * 0.075)
    fill = "#140c34"
    # legs + arms (thick outline then fill)
    limbs = [((x - h * 0.05, y - h * 0.42), (x - h * 0.1 - sw * h * 0.08, y)), ((x + h * 0.05, y - h * 0.42), (x + h * 0.1 + sw * h * 0.08, y)),
             ((x - h * 0.12, y - h * 0.74), (x - h * 0.22 + sw * h * 0.05, y - h * 0.46)), ((x + h * 0.12, y - h * 0.74), (x + h * 0.22 - sw * h * 0.05, y - h * 0.46))]
    for (a0, b0) in limbs: line(c, a0[0], a0[1], b0[0], b0[1], colr, lw + max(1.5, h * 0.03) * 2, a)
    for (a0, b0) in limbs: line(c, a0[0], a0[1], b0[0], b0[1], fill, lw, a)
    rrect(c, x - h * 0.14, y - h * 0.8, h * 0.28, h * 0.42, h * 0.1, fill, a)
    rrect(c, x - h * 0.14, y - h * 0.8, h * 0.28, h * 0.42, h * 0.1, colr, a, stroke=max(1.5, h * 0.03))
    circle(c, hx, hy, hr, fill, a); circle(c, hx, hy, hr, colr, a, stroke=max(1.5, h * 0.03))
    rrect(c, hx - hr * 0.2, hy - hr * 0.25, hr * 1.0, hr * 0.45, hr * 0.2, colr, 0.8 * a)  # visor

def scalebar(c, x, yb, h, label, ts, a=1.0, colr=ACCENT, side=1):
    if a <= 0.01: return
    line(c, x, yb, x, yb - h, colr, 4, a); line(c, x - 12, yb, x + 12, yb, colr, 4, a); line(c, x - 12, yb - h, x + 12, yb - h, colr, 4, a)
    C(c, label, x + side * 18, yb - h / 2, a, ts, size=30, bg="#2a1a5c", align="l" if side > 0 else "r")

class Iso:
    def __init__(self, ox, oy, s): self.ox, self.oy, self.s = ox, oy, s
    def P(self, x, y, z=0.0):
        s = self.s; return (self.ox + (x - y) * 0.866 * s, self.oy + (x + y) * 0.5 * s - z * s)
    def box(self, c, x, y, z, w, d, h, colr, a=1.0, edge=None, top=None):
        P = self.P
        topc = top or mix(colr, "#ffffff", 0.22)
        c.drawPath(poly([P(x, y + d, z), P(x + w, y + d, z), P(x + w, y + d, z + h), P(x, y + d, z + h)]), paint(colr, a))
        c.drawPath(poly([P(x + w, y, z), P(x + w, y + d, z), P(x + w, y + d, z + h), P(x + w, y, z + h)]), paint(mix(colr, "#000000", 0.38), a))
        c.drawPath(poly([P(x, y, z + h), P(x + w, y, z + h), P(x + w, y + d, z + h), P(x, y + d, z + h)]), paint(topc, a))
        if edge:
            c.drawPath(poly([P(x, y, z + h), P(x + w, y, z + h), P(x + w, y + d, z + h), P(x, y + d, z + h)]), paint(edge, a * 0.8, stroke=max(1, self.s * 0.03)))

def cached(key, w, h, draw):
    """Render static art once into an image of size (w, h) and return it."""
    if key not in _CACHE:
        surf = skia.Surface(int(w), int(h)); cc = surf.getCanvas(); cc.clear(skia.ColorTRANSPARENT)
        draw(cc); _CACHE[key] = surf.makeImageSnapshot()
    return _CACHE[key]
_CACHE = {}

def img_at(c, img, x, y, sc=1.0, a=1.0):
    if a <= 0.01: return
    p = skia.Paint(); p.setAlphaf(clamp(a))
    c.save(); c.translate(x, y); c.scale(sc, sc)
    c.drawImage(img, 0, 0, skia.SamplingOptions(skia.FilterMode.kLinear), p); c.restore()

# --- chip die (title / end motif)
def _die_art(cc, s):
    I = Iso(500 * s, 260 * s, 40 * s)
    I.box(cc, -1, -1, -0.9, 12, 12, 0.7, "#2b2160", edge="#4a3a9a")      # substrate
    for k in range(13):                                                   # pins along the edges
        I.box(cc, -1 + k * 0.92, 11, -1.15, 0.45, 0.55, 0.35, "#c9a24a")
        I.box(cc, 11, -1 + k * 0.92, -1.15, 0.55, 0.45, 0.35, "#c9a24a")
    I.box(cc, 1, 1, -0.2, 8, 8, 0.45, "#5e6f9e", edge=CY, top="#8a9bc4")  # die
    for i in range(3):
        for j in range(3):
            colr = [CY, MG, "#9d7bff"][(i + j) % 3]
            p = [I.P(1.5 + i * 2.5, 1.5 + j * 2.5, 0.27), I.P(3.6 + i * 2.5, 1.5 + j * 2.5, 0.27), I.P(3.6 + i * 2.5, 3.6 + j * 2.5, 0.27), I.P(1.5 + i * 2.5, 3.6 + j * 2.5, 0.27)]
            cc.drawPath(poly(p), paint(colr, 0.35)); cc.drawPath(poly(p), paint(colr, 0.9, stroke=2.2 * s))
            for k in range(4):
                a0 = I.P(1.75 + i * 2.5, 1.85 + j * 2.5 + k * 0.45, 0.27); b0 = I.P(3.35 + i * 2.5, 1.85 + j * 2.5 + k * 0.45, 0.27)
                cc.drawLine(a0[0], a0[1], b0[0], b0[1], paint("#ffffff", 0.35, stroke=1.4 * s))

def die_motif(c, W, H, t, S, cx, cy, s):
    u = S.u; k = s * u * (1.25 if S.P else 1.0)
    def art(cc):
        cc.drawCircle(500, 290, 330, paint(shader=rad(500, 290, 400, [(0, CY, 0.22), (0.6, CY, 0.08), (1, CY, 0)])))
        _die_art(cc, 1.0)
    img = cached(("die", 2), 1000, 700, art)
    c.save(); c.translate(cx, cy + math.sin(t * 1.2) * 6 * u); c.scale(k, k)
    img_at(c, img, -500, -350)
    I = Iso(0, -90, 40)
    for n in range(6):  # pulses running over the die
        q = (t * 0.35 + n / 6) % 1
        if n % 2: x, y = I.P(1 + q * 8, 1.6 + n * 1.2, 0.27)
        else: x, y = I.P(1.6 + n * 1.2, 1 + q * 8, 0.27)
        circle(c, x, y, 7, "#ffffff", math.sin(q * math.pi)); circle(c, x, y, 18, CY, 0.35 * math.sin(q * math.pi))
    c.restore()

# ------------------------------------------------------------------ kit scenes
def c_title(c, W, H, t, S): kit.title(c, W, H, t, S, bg_chip, die_motif, PAL)

def c_card(c, W, H, t, S):
    def bgc(c, W, H, t, S):
        bg_chip(c, W, H, t, S)
        txt = S.opts.get("text", "")
        sizes = {"1 MILLIMETER": 1.0, "1 MICROMETER": 0.7, "100 NANOMETERS": 0.45, "1 NANOMETER": 0.25}
        if txt in sizes:  # the explorer shrinks on every size card
            u = S.u; f = sizes[txt]; h = lerp(f * 1.6, f, eout(prog(t, 0.1, 1.2))) * 330 * u
            xx = W * (0.93 if not S.P else 0.5); yy = H * (0.9 if not S.P else 0.8)
            explorer(c, xx, yy, h, 0.85, t)
        else:
            die_motif(c, W, H, t, S, W / 2, H / 2, 1.3 if not S.P else 1.0)
            c.drawPaint(paint("#ff3a1a", 0.12 + 0.05 * math.sin(t * 5)))
    kit.card(c, W, H, t, S, bgc, PAL)

def c_end(c, W, H, t, S):
    def mot(c, W, H, t, S, cx, cy, s):
        die_motif(c, W, H, t, S, cx, cy, s)
        explorer(c, cx + 300 * S.u * s, cy + 120 * S.u * s, 120 * S.u * s, 1, t)
    kit.end(c, W, H, t, S, bg_chip, mot, PAL)

def c_endshort(c, W, H, t, S): kit.end_short(c, W, H, t, S, bg_chip, die_motif, PAL)

# ------------------------------------------------------------------ c_hair
def _hair_art(cc):
    R = 380; cx, cy = 400, 400
    cc.drawCircle(cx, cy, R, paint(shader=rad(cx - 90, cy - 110, R * 1.3, [(0, "#d9a066", 1), (0.6, "#8a5a2e", 1), (1, "#4a2c14", 1)])))
    rng = random.Random(3)
    for k in range(26):  # cuticle scales
        an = k / 26 * 2 * math.pi
        p = skia.Path(); p.addArc(skia.Rect.MakeXYWH(cx - R * 0.97, cy - R * 0.97, R * 1.94, R * 1.94), math.degrees(an), 13)
        cc.drawPath(p, paint("#f2c48a", 0.55, stroke=10))
    cc.drawCircle(cx, cy, R * 0.42, paint("#5a3418", 0.6))
    for k in range(60):
        an = rng.uniform(0, 6.28); r = rng.uniform(0, R * 0.85)
        cc.drawCircle(cx + math.cos(an) * r, cy + math.sin(an) * r, rng.uniform(3, 9), paint("#3a200c", 0.35))
    cc.drawCircle(cx, cy, R, paint("#ffe2b8", 0.6, stroke=4))

def c_hair(c, W, H, t, S):
    B = BB(S, 3, keep=[0, 2]); bg_chip(c, W, H, t, S)
    with Stage(c, S) as ts:
        img = cached("hair", 800, 800, _hair_art)
        p0 = eout(prog(t, B(0, 0.0), 0.8))
        hx, hy, R = 640, 560, 380
        img_at(c, img, hx - 400, hy - 400 + (1 - p0) * 60, 1.0, p0)
        T(c, "HUMAN HAIR (CROSS-SECTION)", hx, 110, 44, ts, "#ffe2b8", vis(t, B(0, 0.05)))
        pr = vis(t, B(0, 0.4))
        if pr > 0:
            ww = 2 * R * eout(prog(t, B(0, 0.4), 0.8))
            line(c, hx - R, hy + R + 50, hx - R + ww, hy + R + 50, ACCENT, 6, pr)
            for k in range(11):
                xx = hx - R + k * 2 * R / 10
                if xx <= hx - R + ww + 1: line(c, xx, hy + R + 36, xx, hy + R + 64, ACCENT, 4, pr)
            C(c, "80,000–100,000 NM WIDE", hx, hy + R + 110 if not S.P else hy + R - 40, pr, ts, size=32, bg="#3a2410")
        # transistors lining up across the diameter
        pt = prog(t, B(1, 0.05), 3.0)
        if pt > 0:
            n = int(120 * eout(pt))
            for k in range(n):
                xx = hx - R + 12 + k * (2 * R - 24) / 119
                rect(c, xx - 2, hy - 24, 4, 48, CY, 0.9)
            line(c, hx - R, hy, hx + R, hy, CY, 2, 0.4)
            # magnifier
            mx, my, mr = 1400, 470, 280
            pm = eout(prog(t, B(1, 0.3), 0.6))
            line(c, hx + R * 0.5, hy, mx - mr * 0.9, my + 60, CY, 3, 0.6 * pm)
            circle(c, mx, my, mr, "#0b0628", pm); circle(c, mx, my, mr, CY, pm, stroke=6)
            c.save(); pp = skia.Path(); pp.addCircle(mx, my, mr - 4); c.clipPath(pp, doAntiAlias=True)
            circle(c, mx, my, mr - 4, CY, 0.08 * pm)
            for k in range(-6, 7):
                xx = mx + k * 60 + (t * 8 % 60)
                rrect(c, xx - 12, my - 160, 24, 320, 7, "#c4cff0", pm); rrect(c, xx - 19, my - 60, 38, 120, 7, MG, pm)
                circle(c, xx, my - 160 + ((t * 0.8 + k * 0.17) % 1) * 320, 7, CY, pm)
            c.restore()
            circle(c, mx, my, mr + 10, CY, 0.25 * pm, stroke=14)
            C(c, "A FEW DOZEN NM APART", mx, my + mr + 50, vis(t, B(1, 0.45)), ts, size=34)
            C(c, "> 1,000 ACROSS ONE HAIR", mx, my - mr - 55, vis(t, B(1, 0.75)), ts, size=40, bg="#3a1250", dot=CY)
        pe = prog(t, B(2, 0.0), 0.5)
        if pe > 0:
            circle(c, hx, hy, R + 6, BG_T, 0.4 * eout(pe))   # hair dims only partly; the inset stays bright
            hh = lerp(420, 100, eout(prog(t, B(2, 0.2), 2.5)))
            explorer(c, 1790, 1010, hh, eout(pe), t)
            T(c, "?", 1790, 1010 - hh - 90, 140, ts, ACCENT, prog(t, B(2, 0.6), 0.4), shadow=20)
    kit.hook(c, W, H, t, S)

# ------------------------------------------------------------------ c_rules
def c_rules(c, W, H, t, S):
    B = BB(S, 2); bg_chip(c, W, H, t, S)
    with Stage(c, S) as ts:
        pa = phase(t, None, B(1, 0))
        with Layer(c, pa) as on:
            if on:
                for k in range(4):
                    hh = 520 * (0.75 ** k)
                    explorer(c, 300 + k * 150, 900, hh, (1 if k == 3 else 0.3) * vis(t, B(0, 0.02 + 0.06 * k)), t)
                rules = [("NO AIR NEEDED", CY), ("HEAT CAN'T HURT YOU", MG), ("YOU CAN STILL SEE", ACCENT)]
                for k, (s_, colr) in enumerate(rules):
                    C(c, s_, 1250, 330 + k * 170, vis(t, B(0, 0.25 + k * 0.22)), ts, size=40, dot=colr)
                T(c, "THE RULES", 1250, 160, 70, ts, "#ffffff", vis(t, B(0, 0.05)))
        pb = phase(t, B(1, 0))
        with Layer(c, pb) as on:
            if on:
                # generic laptop (no logo)
                lx, ly = 760, 640
                c.drawPath(poly([(lx - 420, ly), (lx + 420, ly), (lx + 500, ly + 120), (lx - 500, ly + 120)]), paint("#2a2450"))
                c.drawPath(poly([(lx - 420, ly), (lx + 420, ly), (lx + 500, ly + 120), (lx - 500, ly + 120)]), paint("#6a5fb0", 1, stroke=4))
                rrect(c, lx - 400, ly - 470, 800, 460, 22, "#1b1640"); rrect(c, lx - 400, ly - 470, 800, 460, 22, "#6a5fb0", 1, stroke=4)
                rrect(c, lx - 370, ly - 440, 740, 400, 10, "#0b0826")
                for k in range(8):
                    rrect(c, lx - 330, ly - 400 + k * 44, 300 + (k * 97 % 330), 18, 9, [CY, MG, "#9d7bff"][k % 3], 0.35)
                g = 0.6 + 0.4 * math.sin(t * 4)
                circle(c, lx, ly + 60, 110, CY, 0.35 * g, blur=40)
                rrect(c, lx - 60, ly + 30, 120, 60, 8, "#8a9bc4"); rrect(c, lx - 60, ly + 30, 120, 60, 8, CY, 1, stroke=4)
                arrow(c, lx + 200, ly + 220, lx + 80, ly + 95, CY, 6, vis(t, B(1, 0.1)))
                n = int(92e9 * eout(prog(t, B(1, 0.15), 1.8)))
                C(c, "M3 MAX CHIP", 1500, 250, vis(t, B(1, 0.05)), ts, size=38, dot=CY)
                T(c, f"{n:,}", 1500, 420, 92, ts, ACCENT, vis(t, B(1, 0.15)), maxw=760)
                T(c, "TRANSISTORS", 1500, 520, 52, ts, "#ffffff", vis(t, B(1, 0.2)))
                C(c, "> 10 FOR EVERY PERSON ON EARTH", 1500, 700, vis(t, B(1, 0.55)), ts, size=34, bg="#3a1250", dot=MG)
                for k in range(10):
                    explorer(c, 1310 + k * 42, 860, 60, vis(t, B(1, 0.6 + k * 0.02)), t, colr=ACCENT, glow=False)

# ------------------------------------------------------------------ c_package
def c_package(c, W, H, t, S):
    B = BB(S, 3); bg_chip(c, W, H, t, S)
    with Stage(c, S) as ts:
        pa = phase(t, None, B(1, 0))
        with Layer(c, pa) as on:
            if on:
                I = Iso(820, 330, 52)
                I.box(c, -0.6, -0.6, -0.2, 11.2, 11.2, 0.2, "#2a2155")
                I.box(c, 0, 0, 0, 10, 10, 1.6, "#1a1530", edge="#5a4aa0", top="#241d44")
                for k in range(5):
                    a0 = I.P(1 + k * 2, 1, 1.6); b0 = I.P(1 + k * 2, 9, 1.6)
                    line(c, a0[0], a0[1], b0[0], b0[1], "#3a3070", 3)
                ex, ey = I.P(10.8, 4.5, 0)
                explorer(c, ex, ey, 46, vis(t, B(0, 0.05)), t)
                # magnifier on the explorer
                pm = vis(t, B(0, 0.2)); mx, my, mr = 1560, 330, 190
                line(c, ex + 20, ey - 30, mx - mr * 0.8, my + mr * 0.6, CY, 3, pm * 0.7)
                circle(c, mx, my, mr, "#0b0628", pm); circle(c, mx, my, mr, CY, pm, stroke=6)
                explorer(c, mx - 30, my + 150, 280, pm, t)
                scalebar(c, mx + 90, my + 150, 280, "YOU: 1 MM", ts, pm)
                C(c, "THE PACKAGE: A PROTECTIVE SHELL", 760, 980, vis(t, B(0, 0.5)), ts, size=36, dot=CY)
        pb = phase(t, B(1, 0), B(2, 0))
        with Layer(c, pb) as on:
            if on:
                # cross-section: lid, die, bumps, substrate
                x0, x1 = 260, 1660; yb = 720
                lift = eout(prog(t, B(1, 0.05), 1.0)) * 160
                rect(c, x0, yb, x1 - x0, 90, "#2b2160"); rect(c, x0, yb, x1 - x0, 90, "#5a4aa0", 1, stroke=3)
                for k in range(26):
                    xx = x0 + 40 + k * (x1 - x0 - 80) / 25
                    circle(c, xx, yb + 112, 16, "#c9a24a")
                pbm = prog(t, B(1, 0.45), 1.2)
                for k in range(48):
                    xx = 560 + k * 800 / 47
                    circle(c, xx, yb - 12, 9, CU2, eout(clamp(pbm * 2 - k / 47)))
                rect(c, 540, yb - 110, 840, 90, "#8a9bc4"); rect(c, 540, yb - 110, 840, 90, CY, 1, stroke=4)
                for k in range(12): rect(c, 560 + k * 68, yb - 100, 46, 70, CY, 0.18)
                rrect(c, x0 + 60, yb - 260 - lift, x1 - x0 - 120, 120, 14, "#1a1530", 0.95)
                rrect(c, x0 + 60, yb - 260 - lift, x1 - x0 - 120, 120, 14, "#5a4aa0", 0.95, stroke=4)
                T(c, "LID", 960, yb - 200 - lift, 40, ts, "#9d8bd8")
                C(c, "THE DIE: A THIN SLAB OF SILICON", 960, 330 - lift * 0.6 if not S.P else 240, vis(t, B(1, 0.2)), ts, size=34, dot=CY)
                C(c, "THOUSANDS OF TINY METAL BUMPS", 1180, 960, vis(t, B(1, 0.5)), ts, size=34, dot=CU2)
                arrow(c, 1000, 920, 900, yb + 10, CU2, 5, vis(t, B(1, 0.5)))
        pc = phase(t, B(2, 0))
        with Layer(c, pc) as on:
            if on:
                # quartz -> wafer, purity
                qx, qy = 330, 560
                pts = [(qx - 70, qy + 160), (qx - 90, qy - 40), (qx, qy - 190), (qx + 90, qy - 40), (qx + 70, qy + 160)]
                c.drawPath(poly(pts), paint("#f4e6f2", 0.9)); c.drawPath(poly(pts), paint("#ffffff", 1, stroke=4))
                c.drawPath(poly([(qx, qy - 190), (qx - 10, qy + 160)], close=False), paint("#c9b4d8", 1, stroke=3))
                T(c, "QUARTZ", qx, qy + 230, 42, ts, "#f4e6f2", vis(t, B(2, 0.0)))
                arrow(c, qx + 130, qy, qx + 290, qy, ACCENT, 8, vis(t, B(2, 0.1)))
                wx, wy, wr = 680, 560, 170
                pw = vis(t, B(2, 0.12))
                c.drawCircle(wx, wy, wr, paint(shader=skia.GradientShader.MakeSweep(wx, wy, [col(c_, 1) for c_ in ("#8a9bc4", "#d6c8ff", "#7fe3ff", "#c4a0ff", "#8a9bc4")]), a=pw))
                for k in range(-4, 5):
                    line(c, wx + k * 34, wy - math.sqrt(max(0, wr * wr - (k * 34) ** 2)), wx + k * 34, wy + math.sqrt(max(0, wr * wr - (k * 34) ** 2)), "#3a3070", 2, 0.6 * pw)
                    line(c, wx - math.sqrt(max(0, wr * wr - (k * 34) ** 2)), wy + k * 34, wx + math.sqrt(max(0, wr * wr - (k * 34) ** 2)), wy + k * 34, "#3a3070", 2, 0.6 * pw)
                T(c, "SILICON", wx, wy + 230, 42, ts, SI, pw)
                digits = "99.9999999%"; nd = int(len(digits) * eout(prog(t, B(2, 0.25), 1.6)) + 0.5)
                T(c, digits[:max(nd, 1)], 1380, 330, 150, ts, ACCENT, vis(t, B(2, 0.25)), maxw=900)
                C(c, "NINE NINES", 1380, 470, vis(t, B(2, 0.45)), ts, size=40, dot=ACCENT)
                pg = vis(t, B(2, 0.6))
                if pg > 0:
                    for i in range(14):
                        for j in range(7):
                            colr = MG if (i, j) == (9, 3) else SI
                            circle(c, 1110 + i * 40, 600 + j * 40, 13 if colr == MG else 10, colr, pg * (1 if colr == MG else 0.6))
                    circle(c, 1110 + 9 * 40, 600 + 3 * 40, 26, MG, pg * (0.5 + 0.5 * math.sin(t * 5)), stroke=4)
                    C(c, "< 1 STRAY ATOM PER BILLION", 1380, 930, pg, ts, size=34, dot=MG)

# ------------------------------------------------------------------ c_wires: isometric copper stack
STK = dict(ox=560, oy=150, s=36)   # iso origin inside the cached image (image 1120 x 860)
def _levels():
    out = []; z = 0.0
    for L in range(15):
        f = L / 14; th = lerp(0.16, 0.85, f ** 1.6); n = int(round(lerp(18, 4, f ** 0.8)))
        out.append((L, z, th, n)); z += th + 0.32
    return out

def _stack_art(cc):
    I = Iso(STK["ox"], STK["oy"] + 360, STK["s"])
    I.box(cc, 0, 0, -0.9, 12, 12, 0.7, "#5e6f9e", top="#8a9bc4")    # silicon + transistors
    for i in range(24):
        for j in range(24):
            if (i + j) % 2 == 0:
                x, y = I.P(0.25 + i * 0.48, 0.25 + j * 0.48, -0.2); cc.drawCircle(x, y, 2.2, paint(CY, 0.8))
    for (L, z, th, n) in _levels():
        pitch = 12 / n; wd = pitch * 0.55
        colr = mix("#b8652e", CU, L / 14)
        if L % 2 == 0:
            for k in range(n): I.box(cc, 0, k * pitch + (pitch - wd) / 2, z, 12, wd, th, colr, top=CU2)
        else:
            for k in range(n): I.box(cc, k * pitch + (pitch - wd) / 2, 0, z, wd, 12, th, colr, top=CU2)
        # insulation sheet above the level
        zz = z + th + 0.12
        p = [I.P(0, 0, zz), I.P(12, 0, zz), I.P(12, 12, zz), I.P(0, 12, zz)]
        cc.drawPath(poly(p), paint("#b9a6ff", 0.10)); cc.drawPath(poly(p), paint("#b9a6ff", 0.25, stroke=1.5))

def stack_pt(x, y, z, ix, iy, k):
    I = Iso(STK["ox"], STK["oy"] + 360, STK["s"]); px, py = I.P(x, y, z)
    return ix + px * k, iy + py * k

def c_wires(c, W, H, t, S):
    B = BB(S, 4, keep=[0, 1]); bg_chip(c, W, H, t, S)
    with Stage(c, S) as ts:
        img = cached("stack", 1120, 860, _stack_art)
        k = 1.0; ix, iy = 860 - 560 * k, 100
        pin = eout(prog(t, B(0, 0.0), 1.0))
        c.save(); c.translate(0, (1 - pin) * 80); img_at(c, img, ix, iy, k, pin)
        lv = _levels(); ztop = lv[-1][1] + lv[-1][2]
        # explorer on the top level
        ex, ey = stack_pt(7, 8.2, ztop, ix, iy, k)
        explorer(c, ex, ey, 70, pin, t, walk=0.5)
        # pulses on the top two levels
        for n_ in range(10):
            q = (t * 0.4 + n_ * 0.1) % 1
            L, z, th, n = lv[-1 - (n_ % 2)]
            pitch = 12 / n
            if (L % 2) == 0: x, y = stack_pt(q * 12, (n_ % n) * pitch + pitch / 2, z + th, ix, iy, k)
            else: x, y = stack_pt((n_ % n) * pitch + pitch / 2, q * 12, z + th, ix, iy, k)
            circle(c, x, y, 7, "#ffffff", pin * math.sin(q * math.pi)); circle(c, x, y, 20, CY, 0.4 * pin * math.sin(q * math.pi))
        # insulation highlight
        pins = vis(t, B(2, 0.0), B(3, 0))
        if pins > 0:
            for (L, z, th, n) in lv[::3]:
                zz = z + th + 0.12
                p = [stack_pt(0, 0, zz, ix, iy, k), stack_pt(12, 0, zz, ix, iy, k), stack_pt(12, 12, zz, ix, iy, k), stack_pt(0, 12, zz, ix, iy, k)]
                c.drawPath(poly(p), paint(MG, 0.6 * pins * (0.6 + 0.4 * math.sin(t * 4)), stroke=4))
        c.restore()
        if not S.P:
            scalebar(c, ex - 70, ey, 70, "YOU: 1 µM", ts, vis(t, B(0, 0.2)), side=-1)
        if not S.P: C(c, "~15 LEVELS OF COPPER WIRING", 1560, 180, vis(t, B(0, 0.35)), ts, size=34, dot=CU2)
        if not S.P:
            C(c, "WIDE ON TOP: POWER", 1560, 300, vis(t, B(1, 0.05)), ts, size=32, dot=CU)
            C(c, "THINNER + DENSER BELOW", 1560, 860, vis(t, B(1, 0.15)), ts, size=32, dot=CU)
            C(c, "TRANSISTORS AT THE BOTTOM", 1560, 960, vis(t, B(1, 0.2)), ts, size=30, dot=CY)
            pk = vis(t, B(1, 0.45), B(3, 0))
            T(c, "TENS OF KM", 1560, 470, 84, ts, ACCENT, pk, maxw=640)
            T(c, "OF COPPER WIRE", 1560, 550, 44, ts, "#ffffff", pk, maxw=640)
            C(c, "SOME ESTIMATES: ~100 KM", 1560, 650, vis(t, B(1, 0.7), B(3, 0)), ts, size=32, bg="#3a1250")
            C(c, "INSULATION BETWEEN WIRES", 1560, 760, pins, ts, size=32, dot=MG)
            C(c, "ALL IN A FEW CM² OF SILICON", 300, 980, vis(t, B(2, 0.6), B(3, 0)), ts, size=32)
            p3 = vis(t, B(3, 0.0))
            if p3 > 0:
                rrect(c, 1240, 420, 640, 300, 26, "#120b30", 0.95 * p3); rrect(c, 1240, 420, 640, 300, 26, CU2, p3, stroke=4)
                T(c, "1997", 1560, 480, 64, ts, ACCENT, p3)
                rrect(c, 1290, 560, 200, 60, 12, "#b9c0cc", p3); T(c, "ALUMINUM", 1390, 660, 30, ts, "#b9c0cc", p3)
                arrow(c, 1510, 590, 1610, 590, "#ffffff", 7, p3)
                rrect(c, 1630, 560, 200, 60, 12, CU, p3); T(c, "COPPER", 1730, 660, 30, ts, CU2, p3)

# ------------------------------------------------------------------ c_clock
def c_clock(c, W, H, t, S):
    B = BB(S, 2); bg_chip(c, W, H, t, S)
    with Stage(c, S) as ts:
        # neon wire bus with racing pulses
        for k in range(5):
            y = 200 + k * 46
            line(c, 120, y, 1180, y, CU, 8, 0.75); line(c, 120, y, 1180, y, CU2, 2, 0.6)
            q = (t * 1.6 + k * 0.23) % 1; x = lerp(120, 1180, q)
            for j in range(6): circle(c, x - j * 14, y, 9 - j, CY, 0.9 * (1 - j / 6))
        # spinning clock
        ck = vis(t, B(0, 0.1)); cx, cy, r = 1540, 330, 180
        clock(c, cx, cy, r, (t * 3.1) % 1, ck, colr=MG)
        for j in range(5):  # motion blur hands
            an = -math.pi / 2 + 2 * math.pi * ((t * 3.1) % 1) - j * 0.25
            line(c, cx, cy, cx + math.cos(an) * r * 0.8, cy + math.sin(an) * r * 0.8, "#ffffff", r * 0.05, ck * 0.25 * (1 - j / 5))
        T(c, "~4,000,000,000", cx, cy + r + 80, 64, ts, ACCENT, vis(t, B(0, 0.3)), maxw=700)
        T(c, "TICKS PER SECOND", cx, cy + r + 145, 36, ts, "#ffffff", vis(t, B(0, 0.35)))
        # light-per-tick ruler
        pr = vis(t, B(1, 0.0))
        if pr > 0:
            x0, y0, cm = 160, 760, 125
            rect(c, x0 - 20, y0 - 20, cm * 10 + 40, 120, "#f4ecd8", pr)
            for k in range(101):
                hh = 46 if k % 10 == 0 else (30 if k % 5 == 0 else 18)
                line(c, x0 + k * cm / 10, y0 - 20, x0 + k * cm / 10, y0 - 20 + hh, "#2a2440", 2.5 if k % 10 == 0 else 1.5, pr)
                if k % 10 == 0: text(c, str(k // 10), x0 + k * cm / 10, y0 + 60, 30, "#2a2440", pr, w=800)
            T(c, "CM", x0 + cm * 10 + 60, y0 + 40, 30, ts, "#f4ecd8", pr)
            q = (t % 1.6) / 1.6; L = 7.5 * cm * eout(clamp(q / 0.6))
            line(c, x0, y0 - 60, x0 + L, y0 - 60, ACCENT, 10, pr); circle(c, x0 + L, y0 - 60, 16, "#ffffff", pr)
            circle(c, x0 + L, y0 - 60, 34, ACCENT, 0.35 * pr, blur=10)
            Ls = 0.6 * L
            line(c, x0, y0 - 100, x0 + Ls, y0 - 100, CY, 7, pr * 0.9); circle(c, x0 + Ls, y0 - 100, 11, CY, pr)
            C(c, "LIGHT IN 1 TICK: ~7.5 CM", 420, y0 - 260, pr, ts, size=34, dot=ACCENT)
            C(c, "SIGNALS IN WIRES: SLOWER", 420, y0 - 175, vis(t, B(1, 0.35)), ts, size=32, dot=CY)
            C(c, "DATA MUST ARRIVE ON TIME", 960, 1000, vis(t, B(1, 0.65)), ts, size=34, bg="#3a1250")

# ------------------------------------------------------------------ c_fins
def _fin_scene(c, I, t, rise, gate, flow, a=1.0, gaa=0.0):
    I.box(c, -1, -1, -0.6, 12, 9, 0.6, "#3a3f6e", top="#5e6f9e")
    fins = [1.0, 3.2, 5.4, 7.6] if gaa < 0.5 else []
    for fy in fins:
        I.box(c, 0, fy, 0, 10, 0.6, 2.4 * rise, "#8a9bc4", top="#c4cff0")
    if gaa >= 0.5:  # stacked ribbons
        for fy in (2.0, 5.2):
            for k in range(3):
                I.box(c, 0, fy, 0.5 + k * 0.85, 10, 1.6, 0.35, "#8a9bc4", top="#c4cff0")
    if gate > 0:
        drop = (1 - eout(gate)) * 4
        gc = mix("#7a2a6a", MG, 0.5)
        I.box(c, 4.2, -0.6, 0 + drop, 1.6, 9.8, 3.2, gc, a=0.85 * clamp(gate * 2) if gaa < 0.5 else 0.55, top=mix(MG, "#ffffff", 0.3))
    if flow > 0:
        for fy in (fins or [2.0, 5.2]):
            for k in range(7):
                q = (t * 0.5 + k / 7 + fy * 0.13) % 1
                zz = 2.4 * rise + 0.15 if gaa < 0.5 else 1.4
                x, y = I.P(q * 10, fy + 0.3 if gaa < 0.5 else fy + 0.8, zz)
                circle(c, x, y, 8, "#ffffff", flow * math.sin(q * math.pi)); circle(c, x, y, 20, CY, 0.4 * flow * math.sin(q * math.pi))

def c_fins(c, W, H, t, S):
    B = BB(S, 5, keep=[1, 2]); bg_chip(c, W, H, t, S)
    with Stage(c, S) as ts:
        I = Iso(760, 380, 58)
        rise = eout(prog(t, B(1, 0.0), 1.2))
        gate = prog(t, B(1, 0.45), 1.0)
        gaa = 1.0 if t >= B(4, 0) else 0.0
        on_ = 0.0
        if t >= B(2, 0):
            cyc = ((t - B(2, 0)) % 2.4) / 2.4; on_ = 1.0 if cyc < 0.55 else 0.0
            if t >= B(3, 0): on_ = 1.0
        pf = phase(t, None, B(4, 0)) if gaa < 0.5 else 0
        with Layer(c, 1.0 if gaa < 0.5 else 0):
            pass
        if gaa < 0.5:
            _fin_scene(c, I, t, rise, gate, on_ if t >= B(2, 0) else 0.0)
        else:
            pg = eout(prog(t, B(4, 0), 0.6))
            c.save(); c.translate(0, (1 - pg) * 40)
            _fin_scene(c, I, t, 1.0, 1.0, 1.0, gaa=1.0); c.restore()
        ex, ey = I.P(10.6, 8.5, 0)
        explorer(c, ex, ey, 80, vis(t, B(0, 0.05)), t)
        if not S.P: scalebar(c, ex + 60, ey, 80, "YOU: 100 NM", ts, vis(t, B(0, 0.2)))
        C(c, "THE TRANSISTORS", 300, 140, vis(t, B(0, 0.1), B(1, 0)), ts, size=40, dot=CY)
        C(c, "FINS: THIN WALLS OF SILICON", 340, 140, vis(t, B(1, 0.1), B(2, 0)), ts, size=36, dot=SI)
        C(c, "GATE DRAPES OVER TOP + SIDES", 1500, 140 if not S.P else 1010, vis(t, B(1, 0.55), B(2, 0)), ts, size=34, dot=MG)
        if B(2, 0) <= t < B(4, 0):
            p2 = vis(t, B(2, 0.0))
            T(c, "1" if on_ else "0", 1640, 440 if not S.P else 360, 260, ts, CY if on_ else "#ff4d6d", p2, shadow=24)
            C(c, "ON: ELECTRONS FLOW" if on_ else "OFF: FLOW STOPS", 1640, 640 if not S.P else 930, p2, ts, size=36, bg="#123d3a" if on_ else "#4a1230")
        C(c, "INTEL, 2011: FIRST MASS-PRODUCED 3D TRANSISTORS", 960, 1000, vis(t, B(3, 0.1), B(4, 0)), ts, size=32, bg="#3a1250")
        C(c, "NEWEST: STACKED RIBBONS", 360, 140, vis(t, B(4, 0.1)), ts, size=36, dot=SI)
        C(c, "GATE WRAPS ALL THE WAY AROUND", 1480, 140, vis(t, B(4, 0.4)), ts, size=34, dot=MG)

# ------------------------------------------------------------------ c_dust
def _rows_art(cc):
    I = Iso(560, 120, 26)
    I.box(cc, 0, 0, -0.5, 20, 20, 0.5, "#3a3f6e", top="#4e5a8a")
    for j in range(10):
        for i in range(10):
            I.box(cc, 0.6 + i * 1.9, 0.6 + j * 1.9, 0, 0.4, 1.3, 1.1, "#8a9bc4", top="#c4cff0")
            I.box(cc, 0.3 + i * 1.9, 1.05 + j * 1.9, 0, 1.0, 0.35, 1.4, mix("#7a2a6a", MG, 0.4))

def _boulder(c, x, y, r, a, seed=5, squash=0.0):
    rng = random.Random(seed); pts = []
    for k in range(14):
        an = k / 14 * 2 * math.pi; rr = r * rng.uniform(0.8, 1.05)
        pts.append((x + math.cos(an) * rr, y + math.sin(an) * rr * (1 - 0.15 * squash)))
    c.drawPath(poly(pts), paint("#7a6f80", a))
    c.drawPath(poly(pts), paint(shader=rad(x - r * 0.3, y - r * 0.4, r * 1.6, [(0, "#d9cfe0", 0.6), (1, "#20182c", 0.7)]), a=a))
    for k in range(6):
        an = rng.uniform(0, 6.28); d = rng.uniform(0, r * 0.6)
        circle(c, x + math.cos(an) * d, y + math.sin(an) * d, r * rng.uniform(0.06, 0.14), "#4a4258", a * 0.7)

def c_dust(c, W, H, t, S):
    B = BB(S, 2); bg_chip(c, W, H, t, S)
    with Stage(c, S) as ts:
        pa = phase(t, None, B(1, 0))
        with Layer(c, pa) as on:
            if on:
                img = cached("rows", 1120, 720, _rows_art)
                img_at(c, img, 380, 300, 1.0)
                fall = prog(t, B(0, 0.25), 0.7)
                bx, by = 960, lerp(-300, 640, ein(fall))
                if fall >= 1:
                    q = t - (B(0, 0.25) + 0.7)
                    circle(c, bx, 700, 330 * eout(clamp(q / 0.6)), "#ffffff", 0.35 * (1 - clamp(q / 0.6)), stroke=12)
                    xmark(c, 1290, 820, 40, prog(t, B(0, 0.6), 0.3))
                    C(c, "CRUSHED", 1290, 900, vis(t, B(0, 0.6)), ts, size=30, bg="#4a1230")
                _boulder(c, bx, by, 260, 1.0, squash=1.0 if fall >= 1 else 0)
                explorer(c, 520, 820, 52, 1, t)
                if not S.P: scalebar(c, 470, 820, 52, "YOU", ts, vis(t, B(0, 0.05)), side=-1)
                C(c, "DUST SPECK (1 µM) = 10× YOUR HEIGHT", 960, 120, vis(t, B(0, 0.35)), ts, size=36, dot="#d9cfe0")
        pb = phase(t, B(1, 0))
        with Layer(c, pb) as on:
            if on:
                rng = random.Random(9)
                for side, (x0, n, lab, colr) in enumerate([(160, 340, "ORDINARY ROOM AIR", "#ff9a6a"), (1040, 4, "CHIP CLEAN ROOM", CY)]):
                    pv = vis(t, B(1, 0.05 + side * 0.4))
                    rrect(c, x0, 220, 720, 600, 30, "#0e0a26", 0.95 * pv); rrect(c, x0, 220, 720, 600, 30, colr, pv, stroke=5)
                    for k in range(n):
                        px = x0 + 30 + (rng.random() * 660 + t * 20 * (1 + k % 3)) % 660; py = 250 + (rng.random() * 540 + math.sin(t + k) * 10) % 540
                        circle(c, px, py, 4 if n > 10 else 9, colr, pv * 0.8)
                    T(c, lab, x0 + 360, 180, 40, ts, colr, pv)
                    T(c, "TENS OF MILLIONS" if n > 10 else "A HANDFUL", x0 + 360, 880, 56, ts, "#ffffff", pv)
                    T(c, "PARTICLES PER CUBIC METER", x0 + 360, 950, 30, ts, "#cfc6ff", pv)

# ------------------------------------------------------------------ c_ruler: the 3 nm myth
def c_ruler(c, W, H, t, S):
    B = BB(S, 3, keep=[0, 1, 2]); bg_chip(c, W, H, t, S)
    with Stage(c, S) as ts:
        nmpx = 9.0   # 1 nm = 9 px
        x0, yb = 260, 760
        # gate row (side view): pitch 48 nm, metal lines pitch 24 nm above
        rect(c, 100, yb, 1720, 70, "#5e6f9e"); rect(c, 100, yb, 1720, 6, "#c4cff0")
        for k in range(4):
            gx = x0 + k * 48 * nmpx
            rrect(c, gx - 8 * nmpx, yb - 260, 16 * nmpx, 260, 10, mix("#7a2a6a", MG, 0.5))
            rrect(c, gx - 8 * nmpx, yb - 260, 16 * nmpx, 260, 10, MG, 1, stroke=3)
        for k in range(8):
            mx = x0 - 12 * nmpx + k * 24 * nmpx
            rrect(c, mx - 6 * nmpx, 300, 12 * nmpx, 70, 8, CU)
        ps = vis(t, B(0, 0.0))
        T(c, "SOLD AS:", 1500, 120, 40, ts, "#cfc6ff", ps)
        T(c, "3 NM", 1500, 210, 120, ts, ACCENT, ps)
        # the actual 3 nm ruler, tiny, wandering looking for a match
        q = (t * 0.25) % 1; rx = lerp(260, 1500, 0.5 - 0.5 * math.cos(q * 2 * math.pi))
        pr = vis(t, B(0, 0.25))
        line(c, rx, 560, rx + 3 * nmpx, 560, ACCENT, 8, pr, cap="butt")
        line(c, rx, 540, rx, 580, ACCENT, 4, pr); line(c, rx + 3 * nmpx, 540, rx + 3 * nmpx, 580, ACCENT, 4, pr)
        C(c, "REAL 3 NM", rx + 14, 620, pr, ts, size=26, bg="#3a2a10")
        T(c, "?", rx + 14, 470, 70, ts, ACCENT, pr * (0.5 + 0.5 * math.sin(t * 4)))
        p1 = vis(t, B(1, 0.05))
        if p1 > 0:
            gx0, gx1 = x0, x0 + 48 * nmpx
            line(c, gx0, yb + 120, gx1, yb + 120, CY, 5, p1); line(c, gx0, yb + 100, gx0, yb + 140, CY, 5, p1); line(c, gx1, yb + 100, gx1, yb + 140, CY, 5, p1)
            C(c, "GATES: ~48 NM APART", (gx0 + gx1) / 2 + 60, yb + 200, p1, ts, size=32, dot=MG)
            p2 = vis(t, B(1, 0.45)) if not S.P else 0
            mx0 = x0 - 12 * nmpx + 1 * 24 * nmpx; mx1 = mx0 + 24 * nmpx
            line(c, mx0, 250, mx1, 250, CY, 5, p2); line(c, mx0, 230, mx0, 270, CY, 5, p2); line(c, mx1, 230, mx1, 270, CY, 5, p2)
            C(c, "TIGHTEST WIRES: ~24 NM APART", (mx0 + mx1) / 2 + 220, 170, p2, ts, size=32, dot=CU2)
        stamp(c, "MARKETING", 1450, 520, prog(t, B(2, 0.0) if S.n() >= 3 else B(1, 0.85), 0.35), 1.0 * (1.4 if S.P else 1), color="#ff4d6d", rot=-12, size=90)

# ------------------------------------------------------------------ c_atoms: silicon lattice
LAT = 64  # px between neighbouring atom columns
def _lattice_art(cc):
    for j in range(-1, 18):
        for i in range(-1, 32):
            x = i * LAT + (LAT / 2 if j % 2 else 0); y = j * LAT * 0.62
            for dx, dy in ((LAT / 2, LAT * 0.62), (-LAT / 2, LAT * 0.62)):
                cc.drawLine(x, y, x + dx, y + dy, paint("#6b7ab8", 0.55, stroke=6))
    for j in range(-1, 18):
        for i in range(-1, 32):
            x = i * LAT + (LAT / 2 if j % 2 else 0); y = j * LAT * 0.62
            cc.drawCircle(x, y, 19, paint(shader=rad(x - 6, y - 7, 24, [(0, "#e6ecff", 1), (0.6, "#8a9bc4", 1), (1, "#3d4880", 1)])))

def c_atoms(c, W, H, t, S):
    B = BB(S, 3, keep=[0]); bg_chip(c, W, H, t, S)
    with Stage(c, S) as ts:
        img = cached("lattice", 2000, 1100, _lattice_art)
        pa = phase(t, None, B(2, 0))
        with Layer(c, pa) as on:
            if on:
                c.save(); dx = -(t * 12) % (LAT * 2)
                img_at(c, img, -40 + dx - LAT * 2, -20, 1.0, eout(prog(t, B(0, 0.0), 0.8)))
                c.drawPaint(paint(BG_T, 0.35)); c.restore()
                # explorer ~4 atoms tall
                explorer(c, 980, 820, 4 * LAT * 0.62 * 1.6, vis(t, B(0, 0.1)), t)
                if not S.P: scalebar(c, 1120, 820, 4 * LAT * 0.62 * 1.6, "YOU: 1 NM", ts, vis(t, B(0, 0.2)))
                C(c, "SILICON CRYSTAL", 420, 130, vis(t, B(0, 0.15)), ts, size=40, dot=SI)
                pq = vis(t, B(0, 0.55))
                ax, ay = 4 * LAT + LAT / 2, 5 * LAT * 0.62 - 20
                line(c, ax - 40, ay - 60, ax - 40 + LAT, ay - 60, ACCENT, 6, pq)
                C(c, "~0.25 NM APART", 1500, 130, pq, ts, size=36, dot=ACCENT)
                p1 = vis(t, B(1, 0.0))
                if p1 > 0:
                    rrect(c, 260, 900, 1400, 120, 30, "#0e0a26", 0.92 * p1)
                    n = int(300000 * eout(prog(t, B(1, 0.1), 2.5)))
                    for k in range(16):
                        circle(c, 330 + k * 30 + (t * 120) % 30, 960, 11, SI, p1)
                    T(c, f"{n:,}+ ATOMS ACROSS ONE HAIR", 1180, 960, 46, ts, ACCENT, p1, maxw=820)
        pb = phase(t, B(2, 0))
        with Layer(c, pb) as on:
            if on:
                # cross-section: gate / 5-atom insulator / channel
                rect(c, 200, 200, 1520, 200, "#7a2a6a"); rect(c, 200, 200, 1520, 200, MG, 1, stroke=4)
                T(c, "GATE", 960, 300, 56, ts, "#ffd6f0", pb)
                for row in range(5):
                    for i in range(40):
                        circle(c, 220 + i * 38 + (19 if row % 2 else 0), 425 + row * 34, 15, "#d9ddf0")
                for row in range(5):
                    for i in range(25):
                        circle(c, 230 + i * 61 + (30 if row % 2 else 0), 620 + row * 60, 22, SI)
                T(c, "SILICON CHANNEL", 960, 1000, 44, ts, SI, pb)
                line(c, 1760, 410, 1760, 575, ACCENT, 6, pb); line(c, 1740, 410, 1780, 410, ACCENT, 6, pb); line(c, 1740, 575, 1780, 575, ACCENT, 6, pb)
                C(c, "INSULATOR: ~1.2 NM = 5 ATOMS", 1240, 140, vis(t, B(2, 0.2)), ts, size=34, dot=ACCENT)
                C(c, "INTEL CHIPS, MID-2000S", 460, 140, vis(t, B(2, 0.5)), ts, size=30)

# ------------------------------------------------------------------ c_tunnel
def _electrons(c, t, wall_x, wall_w, thick, leak, a=1.0, n=14, seed=2):
    rng = random.Random(seed)
    for k in range(n):
        y = 260 + k * 46 + rng.uniform(-8, 8); ph = rng.random(); sp = rng.uniform(0.35, 0.55)
        q = (t * sp + ph) % 1
        through = (k % 5 == 0) and leak > 0
        if q < 0.5: x = lerp(150, wall_x - 14, q / 0.5); al = 1.0
        elif through: x = lerp(wall_x + wall_w + 14, 1780, (q - 0.5) / 0.5); al = leak
        else: x = lerp(wall_x - 14, 150, (q - 0.5) / 0.5); al = 1.0
        if through and q >= 0.45 and q < 0.55:  # ghosting through the wall
            gx = lerp(wall_x - 14, wall_x + wall_w + 14, (q - 0.45) / 0.1)
            circle(c, gx, y, 14, CY, 0.35 * a * leak); continue
        for j in range(3):
            wy = y + math.sin(x * 0.05 + j) * 6
        circle(c, x, y, 34, CY, 0.22 * a * al); circle(c, x, y, 14, "#ffffff", a * al)

def c_tunnel(c, W, H, t, S):
    B = BB(S, 3, keep=[0]); bg_chip(c, W, H, t, S)
    with Stage(c, S) as ts:
        pa = phase(t, None, B(2, 0))
        with Layer(c, pa) as on:
            if on:
                thick = prog(t, B(1, 0.35), 1.0)
                ww = lerp(60, 170, eout(thick)); wx = 960 - ww / 2
                colr = mix("#d9ddf0", MG, eout(thick))
                rect(c, wx, 220, ww, 680, colr, 0.92)
                for row in range(16):
                    for i in range(max(1, int(ww // 34))):
                        circle(c, wx + 17 + i * 34, 240 + row * 42, 12, mix("#ffffff", "#ffd6f0", thick), 0.5)
                leak = 1 - eout(thick)
                _electrons(c, t, wx, ww, thick, leak)
                C(c, "QUANTUM TUNNELING", 480, 130, vis(t, B(0, 0.1)), ts, size=40, dot=CY)
                pl = vis(t, B(0, 0.4)) * leak
                C(c, "LEAK!", 1500, 130, pl * (0.7 + 0.3 * math.sin(t * 8)), ts, size=40, bg="#4a1230", dot="#ff4d6d")
                C(c, "HAFNIUM-BASED INSULATOR", 960, 970, vis(t, B(1, 0.4)), ts, size=36, dot=MG)
                C(c, "LEAK CUT > 10×", 1500, 130, vis(t, B(1, 0.75)), ts, size=40, bg="#123d3a", dot="#4cd964")
        pb = phase(t, B(2, 0))
        with Layer(c, pb) as on:
            if on:
                rrect(c, 220, 260, 1480, 520, 40, "#120b30", 0.95); rrect(c, 220, 260, 1480, 520, 40, MG, 1, stroke=5)
                T(c, "“THE BIGGEST CHANGE IN TRANSISTOR", 960, 420, 60, ts, "#ffffff", vis(t, B(2, 0.05)), maxw=1380)
                T(c, "TECHNOLOGY SINCE THE LATE 1960s”", 960, 510, 60, ts, "#ffffff", vis(t, B(2, 0.1)), maxw=1380)
                T(c, "— GORDON MOORE, INTEL CO-FOUNDER (2007)", 960, 650, 40, ts, ACCENT, vis(t, B(2, 0.35)), w=800)

# ------------------------------------------------------------------ c_heat
def clock_graph(c, x0, y0, w, h, p, ts, a=1.0, label=True):
    """Schematic clock-speed history: rapid rise, then a plateau near ~4 GHz from the mid-2000s."""
    if a <= 0.01: return
    rect(c, x0, y0, w, h, "#0e0a26", 0.9 * a)
    line(c, x0, y0 + h, x0 + w, y0 + h, "#cfc6ff", 4, a); line(c, x0, y0, x0, y0 + h, "#cfc6ff", 4, a)
    years = list(range(1990, 2026))
    def ghz(yr):
        if yr <= 2004: return 4.0 * math.exp((yr - 2004) * 0.36)
        return 3.6 + 0.04 * (yr - 2004) + 0.15 * math.sin(yr)
    def X(yr): return x0 + (yr - 1990) / 35 * w
    def Y(g): return y0 + h - g / 6.0 * h
    yy = Y(4.0)
    line(c, x0, yy, x0 + w, yy, "#ff4d6d", 3, 0.7 * a, dash=([16, 12], 0))
    pts = [(X(yr), Y(ghz(yr))) for yr in years]
    m = max(2, int(len(pts) * clamp(p)))
    c.drawPath(poly(pts[:m], close=False), paint(ACCENT, a, stroke=7))
    circle(c, pts[m - 1][0], pts[m - 1][1], 11, "#ffffff", a)
    for yr in (1990, 2000, 2010, 2020):
        text(c, str(yr), X(yr), y0 + h + 34 * ts, 26 * ts, "#cfc6ff", a, w=700, fam="Inter")
    text(c, "~4 GHZ", x0 + w - 10, yy - 30 * ts, 30 * ts, "#ff8aa0", a, w=900, align="r")
    if label: text(c, "CPU CLOCK SPEED (SCHEMATIC)", x0 + 20, y0 + 36 * ts, 26 * ts, "#cfc6ff", a, w=700, fam="Inter", align="l")

def c_heat(c, W, H, t, S):
    B = BB(S, 4, keep=[0]); bg_chip(c, W, H, t, S)
    with Stage(c, S) as ts:
        pa = phase(t, None, B(1, 0))
        if S.n() < 4: C(c, "AIR-COOLED LIMIT: ~100 W", 960, 110, vis(t, 1.0), ts, size=34, bg="#4a1230", dot="#ff4d6d")
        with Layer(c, pa) as on:
            if on:
                heat = eout(prog(t, B(0, 0.2), 4.0))
                rng = random.Random(int(t * 10))
                for j in range(9):
                    for i in range(16):
                        on_ = rng.random() < 0.5
                        colr = mix(CY, "#ff7a3a", heat) if on_ else "#2a2155"
                        rrect(c, 380 + i * 72, 220 + j * 72, 56, 56, 8, colr, 0.95)
                c.drawPaint(paint(shader=rad(960, 540, 900, [(0, "#ff5a1a", 0.45 * heat), (1, "#ff5a1a", 0)])))
                C(c, "EVERY FLIP MAKES A LITTLE HEAT", 960, 970, vis(t, B(0, 0.3)), ts, size=36, dot="#ff7a3a")
        pb = phase(t, B(1, 0), B(3, 0))
        with Layer(c, pb) as on:
            if on:
                clock_graph(c, 200, 180, 1000, 640, prog(t, B(1, 0.1), 3.0), ts)
                C(c, "POWER WALL: ~100 W", 1560, 300, vis(t, B(1, 0.15)), ts, size=36, dot="#ff4d6d")
                C(c, "CLOCK SPEEDS STALLED", 1560, 420, vis(t, B(1, 0.5)), ts, size=36, dot=ACCENT)
                p2 = vis(t, B(2, 0.05))
                if p2 > 0 and not S.P:
                    rrect(c, 1270, 540, 600, 330, 26, "#2a0f18", 0.95 * p2); rrect(c, 1270, 540, 600, 330, 26, "#ff4d6d", p2, stroke=4)
                    T(c, "2001 WARNING", 1570, 610, 44, ts, "#ff8aa0", p2)
                    T(c, "HOTTER THAN A", 1570, 700, 52, ts, "#ffffff", p2, maxw=540)
                    T(c, "NUCLEAR REACTOR", 1570, 770, 52, ts, ACCENT, p2, maxw=540)
                    T(c, "(FOR ITS SIZE)", 1570, 835, 28, ts, "#cfc6ff", p2, w=700)
        pc = phase(t, B(3, 0))
        with Layer(c, pc) as on:
            if on:
                for k in range(8):
                    i, j = k % 4, k // 4
                    x, y = 420 + i * 290, 250 + j * 300
                    g = 0.5 + 0.5 * math.sin(t * 3 + k)
                    rrect(c, x, y, 250, 250, 20, "#1b1447"); rrect(c, x, y, 250, 250, 20, [CY, MG][k % 2], 0.6 + 0.4 * g, stroke=5)
                    T(c, f"CORE {k + 1}", x + 125, y + 50, 30, ts, "#cfc6ff", 1, w=800)
                    explorer(c, x + 125 + math.sin(t * 2 + k) * 50, y + 220, 120, 1, t + k, colr=[CY, MG][k % 2], walk=1.0)
                C(c, "MORE CORES: A TEAM, NOT ONE SPRINTER", 960, 950, vis(t, B(3, 0.3)), ts, size=36, dot=CY)

# ------------------------------------------------------------------ c_fab: EUV
def _wave(c, x0, x1, y, lam, amp, colr, a, t, w=6):
    if a <= 0.01: return
    p = skia.Path(); n = int((x1 - x0) / 3)
    for i in range(n + 1):
        x = x0 + i * 3; yy = y + math.sin((x - t * 200) / lam * 2 * math.pi) * amp
        (p.moveTo if i == 0 else p.lineTo)(x, yy)
    c.drawPath(p, paint(colr, a * 0.3, stroke=w * 3)); c.drawPath(p, paint(colr, a, stroke=w))

def fab_wave(c, t, a, ts, P):
    if a <= 0.01: return
    _wave(c, 160, 1760, 320, 520, 110, "#7aff8a", a, t)
    T(c, "VISIBLE LIGHT: ~400–700 NM", 960, 150, 40, ts, "#9dffaa", a)
    _wave(c, 160, 1760, 720, 16, 40, "#b77bff", a, t * 0.2, w=3)
    T(c, "EXTREME ULTRAVIOLET: 13.5 NM", 960, 880 if not P else 860, 52, ts, "#d9b8ff", a)

def fab_droplets(c, t, a, ts, P, plasma_lab=True, count="TENS OF THOUSANDS PER SECOND"):
    if a <= 0.01: return
    nx, ny = 960, 120
    rrect(c, nx - 50, 60, 100, 90, 14, "#5e6f9e", a)
    hit_y = 560
    for k in range(9):
        q = (t * 2.2 + k / 9) % 1; y = lerp(160, 1000, q)
        if y < hit_y: circle(c, nx, y, 14, "#d9dde8", a)
        elif y < hit_y + 90:
            e = (y - hit_y) / 90
            circle(c, nx, hit_y, 30 + 120 * e, MG, a * (1 - e) * 0.6, blur=20)
            circle(c, nx, hit_y, 20 + 60 * e, "#ffffff", a * (1 - e))
    # laser pulses from the left
    line(c, 100, hit_y, nx - 20, hit_y, "#ff3a3a", 10, a * (0.6 + 0.4 * math.sin(t * 30)))
    line(c, 100, hit_y, nx - 20, hit_y, "#ffd0d0", 3, a)
    rrect(c, 40, hit_y - 50, 120, 100, 14, "#3a2a4a", a); T(c, "LASER", 100, hit_y + 90, 30, ts, "#ff8a8a", a)
    circle(c, nx, hit_y, 90, "#b77bff", a * (0.35 + 0.15 * math.sin(t * 20)), blur=30)
    T(c, "MOLTEN TIN", nx + 160, 200, 34, ts, "#d9dde8", a, w=800)
    C(c, count, 1450, 380, a, ts, size=34, dot="#d9dde8")
    if plasma_lab:
        C(c, "PLASMA HOTTER THAN THE SUN'S SURFACE", 1380, 760, a, ts, size=32, dot=MG)

def fab_plasma(c, t, a, ts, P):
    if a <= 0.01: return
    x, y = 700, 540
    for k in range(5):
        circle(c, x, y, 260 - k * 45, [MG, "#b77bff", "#ffb0ff", "#ffffff", "#ffffff"][k], a * (0.25 + 0.15 * k), blur=30 - k * 5)
    for k in range(16):
        an = k / 16 * 6.28 + t; r = 200 + 40 * math.sin(t * 7 + k)
        line(c, x + math.cos(an) * 120, y + math.sin(an) * 120, x + math.cos(an) * r, y + math.sin(an) * r, "#ffd6ff", 5, a * 0.6)
    T(c, "TIN PLASMA", x, y + 330, 50, ts, "#ffd6ff", a)
    sun(c, 1470, 460, 120, t, a=a)
    T(c, "SUN'S SURFACE", 1470, 700, 40, ts, ACCENT, a)
    T(c, "<", 1100, 520, 160, ts, "#ffffff", a)

def fab_mirror(c, t, a, ts, P):
    if a <= 0.01: return
    rrect(c, 120, 120, 1680, 840, 40, "#0b0624", a * 0.9); rrect(c, 120, 120, 1680, 840, 40, "#6b4bd8", a, stroke=4, dash=([30, 18], 0))
    T(c, "VACUUM", 260, 170, 34, ts, "#b9a6ff", a, w=800)
    pts = [(260, 520), (700, 260), (1100, 760), (1500, 300), (1620, 820)]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        line(c, x0, y0, x1, y1, "#b77bff", 8, a * 0.9)
    q = (t * 0.5) % 1; x, y = _polyline_pt(pts, q); circle(c, x, y, 16, "#ffffff", a); circle(c, x, y, 34, "#b77bff", a * 0.4)
    for (mx, my), up in zip(pts[1:4], (1, -1, 1)):
        p = skia.Path(); p.addArc(skia.Rect.MakeXYWH(mx - 120, my - 40 * up - 40, 240, 80), 0 if up > 0 else 180, 180)
        c.drawPath(p, paint("#e6ecff", a, stroke=14))
    rect(c, 1520, 840, 200, 26, "#8a9bc4", a); T(c, "WAFER", 1620, 900, 30, ts, SI, a)
    circle(c, 260, 520, 50, MG, a * 0.6, blur=16)
    C(c, "MIRROR THE SIZE OF GERMANY?", 960, 1010 if not P else 990, a, ts, size=32, bg="#2a1a5c", dot="#e6ecff")
    C(c, "BIGGEST BUMP: ~0.1 MM", 1150, 620, a * clamp((t % 100) * 1), ts, size=34, bg="#3a1250", dot=ACCENT)

def fab_price(c, t, a, ts, P):
    if a <= 0.01: return
    # bus-sized machine silhouette + person for scale
    rrect(c, 160, 330, 1080, 480, 30, "#d9dde8", a); rrect(c, 160, 330, 1080, 480, 30, "#8a9bc4", a, stroke=6)
    for k in range(5): rect(c, 220 + k * 200, 400, 150, 60, "#3a3f6e", a)
    rect(c, 220, 520, 960, 20, MG, a * 0.6)
    explorer(c, 1320, 810, 190, a, t, colr=ACCENT, glow=False)
    T(c, "~$380,000,000", 1560, 300, 84, ts, ACCENT, a, maxw=720)
    T(c, "NEWEST MODEL", 1560, 390, 36, ts, "#ffffff", a)
    C(c, "ONLY ONE COMPANY BUILDS THEM", 960, 930, a, ts, size=36, dot=CY)

def c_fab(c, W, H, t, S):
    o = S.opts; mode = o.get("mode", "full"); bg_chip(c, W, H, t, S)
    with Stage(c, S) as ts:
        P = S.P
        if mode == "full":
            B = BB(S, 3)
            fab_wave(c, t, phase(t, None, B(1, 0)), ts, P)
            pb = phase(t, B(1, 0), B(2, 0))
            with Layer(c, pb) as on:
                if on: fab_droplets(c, t, 1.0, ts, P)
            pc = phase(t, B(2, 0))
            with Layer(c, pc) as on:
                if on: fab_mirror(c, t, 1.0, ts, P)
        elif mode == "intro":
            fab_droplets(c, t, eout(prog(t, 0, 0.5)), ts, P, plasma_lab=False, count="LIGHT FROM EXPLODING TIN")
        elif mode == "wave": fab_wave(c, t, eout(prog(t, 0, 0.5)), ts, P)
        elif mode == "droplets": fab_droplets(c, t, eout(prog(t, 0, 0.5)), ts, P, plasma_lab=False, count="LASER HITS EVERY DROPLET")
        elif mode == "plasma": fab_plasma(c, t, eout(prog(t, 0, 0.5)), ts, P)
        elif mode == "mirror": fab_mirror(c, t, eout(prog(t, 0, 0.5)), ts, P)
        elif mode == "price": fab_price(c, t, eout(prog(t, 0, 0.5)), ts, P)
    kit.hook(c, W, H, t, S)

# ------------------------------------------------------------------ c_twist
def _atom_figure(c, x, y, s, a, t):
    pts = [(0, -4.2), (0, -3.0), (-0.9, -2.6), (0.9, -2.6), (0, -1.8), (-0.6, -0.6), (0.6, -0.6), (-0.8, 0.5), (0.8, 0.5)]
    for (px, py) in pts:
        xx, yy = x + px * s, y + py * s + math.sin(t * 3 + px) * 2
        circle(c, xx, yy, s * 0.48, SI, a); circle(c, xx - s * 0.12, yy - s * 0.14, s * 0.18, "#e6ecff", a * 0.8)
        circle(c, xx, yy, s * 0.48, CY, a * 0.8, stroke=3)

def c_twist(c, W, H, t, S):
    B = BB(S, 5); bg_chip(c, W, H, t, S)
    with Stage(c, S) as ts:
        p0 = phase(t, None, B(1, 0))
        with Layer(c, p0) as on:
            if on:
                explorer(c, 960, 900, 560, 1, t)
                xmark(c, 960, 520, 140, prog(t, B(0, 0.3), 0.4))
                C(c, "YOU COULD NEVER TAKE THIS TRIP", 960, 130, vis(t, B(0, 0.1)), ts, size=40, bg="#4a1230")
        p1 = phase(t, B(1, 0), B(2, 0))
        with Layer(c, p1) as on:
            if on:
                _atom_figure(c, 960, 760, 95, 1, t)
                C(c, "ATOMS DON'T SHRINK", 520, 150, vis(t, B(1, 0.05)), ts, size=40, dot=SI)
                C(c, "1 NM YOU = A HANDFUL OF ATOMS", 1400, 150, vis(t, B(1, 0.4)), ts, size=36, dot=CY)
                for k, s_ in enumerate(("NO BRAIN", "NO EYES", "NO HEART")):
                    C(c, s_, 1560, 420 + k * 120, vis(t, B(1, 0.55 + k * 0.1)), ts, size=34, bg="#4a1230")
        p2 = phase(t, B(2, 0), B(3, 0))
        with Layer(c, p2) as on:
            if on:
                _wave(c, 100, 1820, 520, 900, 300, "#7aff8a", 1, t * 0.6, w=10)
                circle(c, 960, 520, 10, CY); circle(c, 960, 520, 30, CY, 0.4)
                T(c, "YOU", 960, 590, 34, ts, CY)
                C(c, "VISIBLE LIGHT WAVES: 400–700 NM", 960, 130, vis(t, B(2, 0.1)), ts, size=36, dot="#7aff8a")
                C(c, "LIKE FEELING SAND IN OVEN MITTS", 960, 960, vis(t, B(2, 0.6)), ts, size=36, bg="#3a1250")
        p3 = phase(t, B(3, 0), B(4, 0))
        with Layer(c, p3) as on:
            if on:
                _wave(c, 100, 1820, 360, 900, 160, "#7aff8a", 0.6, t * 0.6, w=8)
                _wave(c, 100, 1820, 700, 14, 30, CY, 1, t * 0.05, w=3)
                T(c, "VISIBLE LIGHT", 300, 180, 36, ts, "#9dffaa")
                T(c, "ELECTRON WAVES", 360, 820, 36, ts, CY)
                C(c, "ELECTRON MICROSCOPES: THOUSANDS OF TIMES SHORTER", 960, 960, vis(t, B(3, 0.3)), ts, size=32, dot=CY)
        p4 = phase(t, B(4, 0))
        with Layer(c, p4) as on:
            if on:
                fab_droplets(c, t, 1.0, ts, S.P, plasma_lab=False, count="SO THEY MADE SHORTER LIGHT")
                C(c, "EUV: 13.5 NM", 1450, 760, vis(t, B(4, 0.3)), ts, size=40, dot="#b77bff")

# ------------------------------------------------------------------ c_stack
def _tower_art(cc, layers=8):
    I = Iso(500, 640, 40)
    I.box(cc, -1, -1, -0.6, 12, 12, 0.6, "#2b2160", edge="#4a3a9a")
    for k in range(layers):
        z = k * 1.1
        I.box(cc, 1, 1, z, 9, 9, 0.8, "#4a3f8a" if k else "#5e6f9e", top=mix("#8a7bd8", CY, 0.15 * (k % 2)), edge=CY if k == layers - 1 else None)
        for j in range(6):
            x, y = I.P(1.8 + j * 1.4, 10, z + 0.4); cc.drawCircle(x, y, 4, paint(CY, 0.8))

def c_stack(c, W, H, t, S):
    short_only = S.n() < 2
    B = BB(S, 2); bg_chip(c, W, H, t, S)
    with Stage(c, S) as ts:
        pa = phase(t, None, B(1, 0)) if not short_only else 0
        with Layer(c, pa) as on:
            if on:
                x0, y0, w, h = 300, 220, 1320, 640
                rect(c, x0, y0, w, h, "#0e0a26", 0.9)
                line(c, x0, y0 + h, x0 + w, y0 + h, "#cfc6ff", 4); line(c, x0, y0, x0, y0 + h, "#cfc6ff", 4)
                n = 12; pw = prog(t, B(0, 0.1), 3.5)
                for k in range(int(n * pw) + 1):
                    if k >= n: break
                    bh = h * 0.92 * (k + 1) / n
                    rrect(c, x0 + 30 + k * (w - 60) / n, y0 + h - bh, (w - 60) / n - 14, bh, 6, [CY, MG][k % 2], 0.9)
                T(c, "TRANSISTORS PER CHIP: ~2× EVERY 2 YEARS", 960, 160, 44, ts, ACCENT, vis(t, B(0, 0.05)), maxw=1500)
                text(c, "LOG SCALE: EACH STEP = 2×", x0 + 20, y0 + 40, 28, "#cfc6ff", vis(t, B(0, 0.1)), w=700, fam="Inter", align="l")
                T(c, "FOR MORE THAN 50 YEARS", 960, 930, 40, ts, "#ffffff", vis(t, B(0, 0.4)))
        pb = phase(t, B(1, 0)) if not short_only else 1.0
        with Layer(c, pb) as on:
            if on:
                img = cached("tower", 1000, 900, _tower_art)
                t0 = B(1, 0) if not short_only else 0.0
                rise = eout(prog(t, t0, 2.5))
                c.save(); r_ = skia.Rect.MakeXYWH(0, lerp(1080, 60, rise), 1920, 1100); c.clipRect(r_)
                img_at(c, img, 460, 60, 1.0); c.restore()
                I = Iso(960, 700, 40)
                for k in range(4):  # vertical links glowing
                    x, y = I.P(3 + k * 1.6, 3 + k * 1.2, 0)
                    q = (t * 0.7 + k * 0.25) % 1
                    circle(c, x, y - q * 320 * rise, 9, "#ffffff", math.sin(q * math.pi) * rise)
                explorer(c, 1500, 900, 110, 1, t)
                C(c, "CHIPS STACKED INTO TOWERS", 420, 200, vis(t, t0 + 0.4), ts, size=36, dot=CY)
                if not short_only: C(c, "HIGH-BANDWIDTH MEMORY IN AI CHIPS", 1500, 300, vis(t, t0 + 1.2), ts, size=32, dot=MG)

# ------------------------------------------------------------------ c_moore (Short only)
def c_moore(c, W, H, t, S):
    o = S.opts; mode = o.get("mode", "intro"); bg_chip(c, W, H, t, S)
    with Stage(c, S) as ts:
        a = 1.0 if S.P else eout(prog(t, 0, 0.5))  # Shorts cut hard between scenes; no fade-from-empty
        if mode == "intro":
            T(c, "1965", 960, 140, 110, ts, ACCENT, a)
            x0, y0, w, h = 300, 260, 1320, 640
            rect(c, x0, y0, w, h, "#0e0a26", 0.9 * a)
            n = 10; pw = prog(t, 0.4, S.dur * 0.7)
            for k in range(min(n, int(n * pw) + 1)):
                bh = max(6, h * 0.92 * (2 ** k) / (2 ** (n - 1)))
                rrect(c, x0 + 30 + k * (w - 60) / n, y0 + h - bh, (w - 60) / n - 14, bh, 6, CY, a)
                text(c, "×2", x0 + 30 + k * (w - 60) / n + ((w - 60) / n - 14) / 2, y0 + h - bh - 30, 40, "#ffffff", a * (k > 0), w=900)
            T(c, "EVERY YEAR", 960, 960, 60, ts, "#ffffff", a)
        elif mode == "graph":
            T(c, "1975: EVERY ~2 YEARS", 960, 130, 80, ts, ACCENT, a, maxw=1600)
            x0, y0, w, h = 260, 240, 1400, 680
            rect(c, x0, y0, w, h, "#0e0a26", 0.9 * a)
            line(c, x0, y0 + h, x0 + w, y0 + h, "#cfc6ff", 4, a); line(c, x0, y0, x0, y0 + h, "#cfc6ff", 4, a)
            steps = 12; pw = prog(t, 0.3, S.dur * 0.75); m = int(steps * pw) + 1
            pts = []
            for k in range(min(m, steps)):
                x = x0 + k * w / steps; y = y0 + h - (k + 1) * h / steps * 0.95
                pts += [(x, y0 + h - k * h / steps * 0.95), (x, y), (x + w / steps, y)]
            if len(pts) > 1: c.drawPath(poly(pts, close=False), paint(MG, a, stroke=8))
            text(c, "TRANSISTORS PER CHIP (LOG SCALE)", x0 + 20, y0 + 40 * ts, 26 * ts, "#cfc6ff", a, w=700, fam="Inter", align="l")
        elif mode == "clock":
            clock_graph(c, 160, 160, 1600, 760, prog(t, 0.3, S.dur * 0.6), ts, a)
    kit.hook(c, W, H, t, S)

SCENES = {k: v for k, v in globals().items() if k.startswith("c_") and callable(v)}
