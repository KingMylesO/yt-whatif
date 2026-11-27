"""Batch 07 scenes: What If Earth Had Two Moons? (+ teaser, submoon and Uranus-tilt Shorts).

Look: "twin moonlight". Plum/aubergine night backgrounds with a lilac haze, two moons that never look alike
(the Moon in cool silver, the hypothetical twin in warm pearl-peach), and the motif of DOUBLE SHADOWS: wherever
two moons shine, objects cast two shadows (one lilac, one peach) in different directions, and orbit diagrams
always show two dashed rings (lilac outer = Moon, peach inner = twin).
short_b7_moonmoon uses a navy-black + mint "submoon" look; short_b7_uranus a dark teal + aqua "sideways" look.
Every scene draws on a virtual 1920x1080 stage (Stage). In Shorts the stage is scaled into the 0.255H..0.58H band
and text sizes are multiplied by ts=1.75. Multi-part scenes are time-ordered panels (run_panels).
"""
from common2 import *
import geo
import scenes_b3_kit as kit
import scenes_b6_now as NW  # rubble-pile rock() and cached Earth globe (earth_d)

VW, VH = 1920, 1080
BG_T, BG_B = "#0b0614", "#2b1238"
LILAC = "#b99bff"; PEACH = "#ffb38a"; SILVER = "#e4e8f4"; PEARL = "#ffe0cc"; SEA = "#4fb6ff"; SUNY = "#ffd36b"
RED = "#ff6b6b"; GREEN = "#7dffb0"; YEL = ACCENT; CHIPBG = "#24123a"; INK = "#0b1030"
PAL = dict(accent=LILAC, chip="#2a1446", title2=PEACH)
# short_b7_moonmoon: navy-black + mint
SB_T, SB_B, MINT = "#02040c", "#0d1a33", "#7dffd8"
PAL_SB = dict(accent=MINT, chip="#0e2238", title2=MINT)
# short_b7_uranus: dark teal + aqua
UR_T, UR_B, AQUA = "#020d10", "#0b2f36", "#8ff3ea"
PAL_UR = dict(accent=AQUA, chip="#0b2a30", title2=AQUA)
CHIP = {"mn": CHIPBG, "sub": "#0e2238", "ura": "#0b2a30"}

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
    size *= ts
    # keep the chip inside the stage
    def width(sz):
        f = sz * 1.15; return tw(s, f, 700, "Inter") + 2 * f * 0.62 + (f * 0.9 if kw.get("dot") else 0)
    while width(size) > 1840 and size > 12: size *= 0.95
    wd = width(size); al = kw.get("align", "c")
    left = x - wd / 2 if al == "c" else (x if al == "l" else x - wd)
    x += max(0, 30 - left) - max(0, left + wd - 1890)
    chip(c, s, x, y, p, size, **kw)

def T(c, s, x, y, size, ts, colr="#ffffff", a=1.0, w=900, maxw=1800, **kw):
    if a <= 0.003: return
    fam = kw.pop("fam", "Inter Display")
    sz = fit(s, maxw * (1.0 if ts == 1 else 1.05), size * ts, w, fam)
    text(c, s, x, y, sz, colr, clamp(a), w=w, fam=fam, shadow=kw.pop("shadow", 10), **kw)

def stage_bg(c, top, bot, a=1.0):
    c.drawRect(skia.Rect.MakeXYWH(0, 0, VW, VH), paint(shader=lin(0, 0, 0, VH, [(0, top, a), (1, bot, a)])))

_BG = {}
def bg_img(W, H, look="mn"):
    k = (W, H, look)
    if k not in _BG:
        surf = skia.Surface(W, H); cc = surf.getCanvas(); M = max(W, H)
        if look == "mn":
            fill_bg(cc, W, H, BG_T, BG_B)
            cc.drawPaint(paint(shader=rad(W * 0.82, H * 0.12, M * 0.7, [(0, "#8a6bff", 0.22), (0.5, "#4a2a8a", 0.08), (1, "#000000", 0)])))
            cc.drawPaint(paint(shader=rad(W * 0.12, H * 0.95, M * 0.6, [(0, "#ff9a7a", 0.16), (0.6, "#6a2a4a", 0.06), (1, "#000000", 0)])))
        elif look == "sub":
            fill_bg(cc, W, H, SB_T, SB_B)
            cc.drawPaint(paint(shader=rad(W * 0.5, H * 0.42, M * 0.55, [(0, "#2a5a7a", 0.22), (1, "#000000", 0)])))
        else:
            fill_bg(cc, W, H, UR_T, UR_B)
            cc.drawPaint(paint(shader=rad(W * 0.75, H * 0.3, M * 0.6, [(0, "#2a9a9a", 0.22), (1, "#000000", 0)])))
            cc.drawPaint(paint(shader=rad(W * 0.1, H * 0.85, M * 0.5, [(0, "#1a3a6a", 0.2), (1, "#000000", 0)])))
        _BG[k] = surf.makeImageSnapshot()
    return _BG[k]

def bg_mn(c, W, H, t, S, star_a=0.8, seed=73, look="mn"):
    c.drawImage(bg_img(W, H, look), 0, 0)
    stars(c, W, H, t, star_a, seed=seed, drift=(-2.5, 0))

def run_panels(c, W, H, t, S, items, seed=73, look="mn"):
    """items: [(t_on, fn(c, ts)), ...] in time order. Each later panel covers the previous one."""
    bg_mn(c, W, H, t, S, seed=seed, look=look)
    for i, (t0, fn) in enumerate(items):
        t1 = items[i + 1][0] if i + 1 < len(items) else None
        if t1 is not None and t >= t1 + 0.5: continue
        a = phase(t, t0 if i > 0 else None, t1)
        if a <= 0.003: continue
        with Layer(c, a) as on:
            if not on: continue
            if i > 0 and t < t0 + 0.55: bg_mn(c, W, H, t, S, seed=seed, look=look)
            if S.P: c.clipRect(skia.Rect.MakeLTRB(0, 0.215 * H, W, 0.59 * H))
            with Stage(c, S) as ts:
                fn(c, ts)
    kit.hook(c, W, H, t, S)

def panels_at(S, bounds):
    """bounds: list of beat start times -> (t_on) list with the first at 0."""
    return [0] + list(bounds)

# ------------------------------------------------------------------ moons
_MI = {}
def moon_img(R, kind="moon"):
    R = max(4, int(R)); k = (R, kind)
    if k not in _MI:
        if len(_MI) > 40: _MI.clear()
        n = 2 * R + 4; surf = skia.Surface(n, n); cc = surf.getCanvas(); cc.clear(skia.ColorTRANSPARENT)
        cx = cy = n / 2
        if kind == "twin": hi, lo, mar, seed = "#ffe9da", "#c9a596", "#8e6f6e", 29
        elif kind == "far": hi, lo, mar, seed = "#eef0f6", "#a9acb8", "#7c7f8e", 41
        elif kind == "phobos": hi, lo, mar, seed = "#b9a493", "#6b5a4e", "#4a3d36", 5
        else: hi, lo, mar, seed = "#eef1f8", "#a3a7b6", "#5f6476", 11
        cc.save(); pth = skia.Path(); pth.addCircle(cx, cy, R); cc.clipPath(pth, doAntiAlias=True)
        cc.drawCircle(cx, cy, R, paint(shader=rad(cx - R * 0.2, cy - R * 0.25, R * 1.2, [(0, hi, 1), (1, lo, 1)])))
        rng = random.Random(seed)
        nm = 0 if kind == "far" else 7
        for _ in range(nm):  # maria
            ang = rng.random() * 6.28; d = rng.random() ** 0.6 * R * 0.6; rr = R * rng.uniform(0.14, 0.3)
            cc.drawCircle(cx + math.cos(ang) * d, cy + math.sin(ang) * d, rr, paint(mar, 0.75 if kind == "moon" else 0.5, blur=max(0.6, R * 0.05)))
        ncr = int(18 + R * (0.35 if kind == "far" else 0.2))
        for _ in range(ncr):
            ang = rng.random() * 6.28; d = rng.random() ** 0.55 * R * 0.97; cr = R * (0.012 + rng.random() ** 3 * 0.08)
            x, y = cx + math.cos(ang) * d, cy + math.sin(ang) * d
            cc.drawCircle(x + cr * 0.2, y + cr * 0.2, cr, paint(mix(lo, "#000000", 0.45), 0.5))
            cc.drawCircle(x - cr * 0.1, y - cr * 0.1, cr * 0.9, paint("#ffffff", 0.3, stroke=max(0.6, cr * 0.22)))
        if kind in ("moon", "twin"):
            tx, ty = cx - 0.28 * R, cy + 0.55 * R  # rayed crater (Tycho-like)
            for kk in range(12):
                an = kk / 12 * 6.28
                cc.drawLine(tx, ty, tx + math.cos(an) * R * 0.35, ty + math.sin(an) * R * 0.35, paint("#ffffff", 0.14, stroke=max(0.6, R * 0.01)))
            cc.drawCircle(tx, ty, R * 0.03, paint("#ffffff", 0.8))
        cc.drawCircle(cx, cy, R, paint(shader=rad(cx, cy, R, [(0.62, "#000000", 0), (1, "#0a0614", 0.42)])))
        cc.restore()
        _MI[k] = surf.makeImageSnapshot()
    return _MI[k]

def moon_d(c, x, y, R, kind="moon", frac=1.0, sun_ang=0.0, a=1.0, glow=1.0, dark="#0b0614"):
    """Moon disc. frac: illuminated fraction (1 full, 0 new). sun_ang: screen direction toward the light (deg, 0 = right)."""
    if a <= 0.003 or R < 1: return
    gc = PEACH if kind == "twin" else ("#c9d4ff" if kind in ("moon", "far") else "#ffffff")
    if glow > 0: c.drawCircle(x, y, R * 1.6, paint(shader=rad(x, y, R * 1.6, [(0.55, gc, 0.28 * glow * frac), (1, gc, 0)]), a=a))
    img = moon_img(R, kind); pt = skia.Paint(); pt.setAlphaf(clamp(a))
    c.drawImageRect(img, skia.Rect.MakeXYWH(x - R - 2, y - R - 2, 2 * R + 4, 2 * R + 4), skia.SamplingOptions(skia.FilterMode.kLinear), pt)
    if frac < 0.995:
        c.save(); pth = skia.Path(); pth.addCircle(x, y, R + 0.5); c.clipPath(pth, doAntiAlias=True)
        c.translate(x, y); c.rotate(sun_ang)
        er = skia.Rect.MakeLTRB(-R * abs(1 - 2 * frac), -R - 1, R * abs(1 - 2 * frac), R + 1)
        dp = paint(dark, 0.9 * a)
        if frac <= 0.5:
            c.drawRect(skia.Rect.MakeLTRB(-R - 2, -R - 2, 0, R + 2), dp)
            c.drawOval(er, dp)
        else:
            ep = skia.Path(); ep.addOval(er); c.clipPath(ep, skia.ClipOp.kDifference, True)
            c.drawRect(skia.Rect.MakeLTRB(-R - 2, -R - 2, 0, R + 2), dp)
        c.restore()

def earth(c, x, y, R, rot=160, a=1.0, glow=1.0):
    NW.earth_d(c, x, y, R, rot=rot, a=a, glow=glow)

def orbit_ring(c, x, y, rx, ry, colr, t, a=1.0, w=3):
    c.drawOval(skia.Rect.MakeLTRB(x - rx, y - ry, x + rx, y + ry), paint(colr, 0.55 * a, stroke=w, dash=([14, 12], -t * 10)))

def sun_d(c, x, y, r, t, a=1.0):
    sun(c, x, y, r, t, a=a)

def qq8_xy(cx, cy, s, A=430, B=110, sq=0.5, k=4.3):
    """messy looping path (schematic) for the mini-moon."""
    return (cx + A * math.cos(s) + B * math.cos(k * s), cy + sq * (A * math.sin(s) + B * math.sin(k * s)))

def loop_path(c, cx, cy, s0, s1, colr, a=1.0, w=3, **kw):
    p = skia.Path(); n = max(2, int((s1 - s0) * 40))
    for i in range(n + 1):
        x, y = qq8_xy(cx, cy, lerp(s0, s1, i / n), **kw)
        if i == 0: p.moveTo(x, y)
        else: p.lineTo(x, y)
    c.drawPath(p, paint(colr, a, stroke=w))

def glint(c, x, y, s, a=1.0, colr="#ffffff"):
    if a <= 0: return
    circle(c, x, y, s * 2.4, colr, 0.25 * a, blur=s)
    line(c, x - s * 2.2, y, x + s * 2.2, y, colr, max(1.5, s * 0.25), 0.7 * a)
    line(c, x, y - s * 2.2, x, y + s * 2.2, colr, max(1.5, s * 0.25), 0.7 * a)
    circle(c, x, y, s * 0.6, colr, a)

# ------------------------------------------------------------------ ground + double shadows (the motif)
def ground(c, hy=800, a=1.0):
    pts = [(0, hy)]
    for i in range(33):
        pts.append((VW * i / 32, hy - 30 - 26 * math.sin(i * 0.55 + 1.2) - 12 * math.sin(i * 1.7)))
    pts += [(VW, VH), (0, VH)]
    c.drawPath(poly(pts), paint("#3a2a4e", a))
    c.drawRect(skia.Rect.MakeLTRB(0, hy, VW, VH), paint(shader=lin(0, hy, 0, VH, [(0, "#5e4e74", a), (1, "#8a78a0", a)])))
    rng = random.Random(9)
    for _ in range(40):
        yy = hy + 10 + rng.random() ** 1.4 * (VH - hy - 20); sc = 0.4 + (yy - hy) / (VH - hy)
        xx = rng.uniform(0, VW); rx = rng.uniform(10, 40) * sc
        c.drawOval(skia.Rect.MakeLTRB(xx - rx, yy - rx * 0.3, xx + rx, yy + rx * 0.3), paint("#4a3a5e", 0.6 * a))

def shadow(c, x, y, h, w, lx, ly, colr, a=1.0, maxlen=900):
    """cast a soft shadow on flat ground from an object (base x,y; height h; width w) lit by a light at (lx, ly)."""
    if a <= 0: return
    dx = x - lx; el = max(0.08, (y - ly) / max(1, abs(dx)))  # rough elevation slope
    L = min(maxlen, h / el * 1.1); sgn = 1 if dx >= 0 else -1
    tx_, ty_ = x + sgn * L * 0.85, y + L * 0.35
    pts = [(x - w / 2, y), (x + w / 2, y), (tx_ + w * 0.7, ty_), (tx_ - w * 0.7, ty_)]
    c.drawPath(poly(pts), paint(colr, 0.7 * a, blur=3))

def scene_objects(c, t, lights, hy=800, a=1.0, xs=(560, 1260)):
    """a person and a tree, each with one shadow per light. lights: [(lx, ly, colr, strength)]"""
    px, tx = xs
    for (lx, ly, colr, s) in lights:
        shadow(c, px, hy + 6, 190, 60, lx, ly, colr, a * s, maxlen=300)
        shadow(c, tx, hy + 6, 330, 110, lx, ly, colr, a * s, maxlen=420)
    tree2(c, tx, hy + 4, 330, leaf="#2a1a40", trunk="#1a1028", a=a)
    person(c, px, hy + 4, 190, "#1a1028", look_up=0.6, a=a)

# ------------------------------------------------------------------ title / cards / end
def motif_mn(c, W, H, t, S, cx, cy, s, look="mn"):
    u = S.u * s * (1.1 if S.P else 1.0)
    orbit_ring(c, cx, cy, 520 * u, 150 * u, LILAC, t, w=2.5 * u)
    orbit_ring(c, cx, cy, 300 * u, 88 * u, PEACH, t, w=2.5 * u)
    th1 = t * 0.25 + 1.0; th2 = t * 0.7 + 2.6
    m = (cx + math.cos(th1) * 520 * u, cy + math.sin(th1) * 150 * u)
    w2 = (cx + math.cos(th2) * 300 * u, cy + math.sin(th2) * 88 * u)
    items = [(math.sin(th1), lambda: moon_d(c, m[0], m[1], 62 * u, "moon", glow=0.8)),
             (math.sin(th2), lambda: moon_d(c, w2[0], w2[1], 62 * u, "twin", glow=0.8)),
             (0.0, lambda: earth(c, cx, cy, int(150 * u), rot=160))]
    for _, f in sorted(items, key=lambda q: q[0]): f()

def motif_sub(c, W, H, t, S, cx, cy, s):
    u = S.u * s * (1.1 if S.P else 1.0)
    orbit_ring(c, cx, cy, 330 * u, 110 * u, MINT, t, w=2.5 * u)
    th = t * 0.8
    sx, sy = cx + math.cos(th) * 330 * u, cy + math.sin(th) * 110 * u
    if math.sin(th) < 0: moon_d(c, sx, sy, 22 * u, "far", glow=0.5)
    moon_d(c, cx, cy, 200 * u, "moon", glow=0.8)
    if math.sin(th) >= 0: moon_d(c, sx, sy, 22 * u, "far", glow=0.5)

def uranus_d(c, x, y, R, t=0.0, a=1.0, rings=True, axis_deg=98, ring_a=0.7):
    """Uranus: pale aqua disc, faint bands and thin rings around the (tipped) equator; axis drawn at axis_deg from vertical."""
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(axis_deg)
    rr = skia.Rect.MakeLTRB(-R * 1.9, -R * 0.22, R * 1.9, R * 0.22)  # ring ellipse in the planet's equator plane
    if rings:
        c.save(); c.clipRect(skia.Rect.MakeLTRB(-R * 2, -R * 2, R * 2, 0))
        for k in (1.55, 1.7, 1.9): c.drawOval(skia.Rect.MakeLTRB(-R * k, -R * 0.22 * k / 1.9, R * k, R * 0.22 * k / 1.9), paint("#d8fbff", ring_a * a * 0.5, stroke=max(1.2, R * 0.018)))
        c.restore()
    c.drawCircle(0, 0, R * 1.2, paint(shader=rad(0, 0, R * 1.2, [(0.8, AQUA, 0.25 * a), (1, AQUA, 0)])))
    c.drawCircle(0, 0, R, paint(shader=rad(-R * 0.3, -R * 0.3, R * 1.4, [(0, "#d9fbf8", a), (0.6, "#8fd9dc", a), (1, "#3f8f9c", a)])))
    for k in (-0.5, -0.15, 0.3):
        c.save(); pth = skia.Path(); pth.addCircle(0, 0, R); c.clipPath(pth, doAntiAlias=True)
        c.drawRect(skia.Rect.MakeLTRB(-R, k * R, R, k * R + R * 0.06), paint("#ffffff", 0.08 * a)); c.restore()
    if rings:
        c.save(); c.clipRect(skia.Rect.MakeLTRB(-R * 2, 0, R * 2, R * 2))
        for k in (1.55, 1.7, 1.9): c.drawOval(skia.Rect.MakeLTRB(-R * k, -R * 0.22 * k / 1.9, R * k, R * 0.22 * k / 1.9), paint("#d8fbff", ring_a * a, stroke=max(1.2, R * 0.022)))
        c.restore()
    line(c, 0, -R * 1.45, 0, R * 1.45, "#ffffff", max(2, R * 0.025), 0.75 * a, dash=([R * 0.08, R * 0.06], 0))
    circle(c, 0, -R * 1.45, max(3, R * 0.04), YEL, a)
    c.restore()

def motif_ura(c, W, H, t, S, cx, cy, s):
    u = S.u * s * (1.1 if S.P else 1.0)
    uranus_d(c, cx + 170 * u, cy, 170 * u, t)
    c.save(); c.translate(cx - 300 * u, cy); c.rotate(-75); earth(c, 0, 0, int(110 * u), rot=150); c.restore()

def bg_title(c, W, H, t, S): bg_mn(c, W, H, t, S)
def mn7_title(c, W, H, t, S): kit.title(c, W, H, t, S, bg_title, motif_mn, PAL)
def mn7_card(c, W, H, t, S):
    def cbg(c, W, H, t, S):
        bg_mn(c, W, H, t, S)
        with Layer(c, 0.4):
            motif_mn(c, W, H, t, S, W / 2, H / 2, 1.2 if not S.P else 0.9)
    kit.card(c, W, H, t, S, cbg, PAL)
def mn7_end(c, W, H, t, S): kit.end(c, W, H, t, S, bg_title, motif_mn, PAL)
def mn7_endshort(c, W, H, t, S):
    look = S.opts.get("look")
    if look == "sub": kit.end_short(c, W, H, t, S, lambda c, W, H, t, S: bg_mn(c, W, H, t, S, look="sub"), motif_sub, PAL_SB)
    elif look == "ura": kit.end_short(c, W, H, t, S, lambda c, W, H, t, S: bg_mn(c, W, H, t, S, look="ura"), motif_ura, PAL_UR)
    else: kit.end_short(c, W, H, t, S, bg_title, motif_mn, PAL)

# ------------------------------------------------------------------ mn7_hook
def mn7_hook(c, W, H, t, S):
    nb = 3 if S.n() >= 3 else 1; B = beats(S, nb)
    def pA(c, ts):
        ex, ey = (760, 560) if not S.P else (900, 560)
        moon_d(c, 1600 if not S.P else 1640, 250, 70, "moon", frac=0.8, sun_ang=180)
        s = 0.6 + t * 0.55
        loop_path(c, ex, ey, max(0.0, s - 4.5), s, "#ffffff", 0.35, w=2.5)
        earth(c, ex, ey, 200, rot=150 + t * 2)
        qx, qy = qq8_xy(ex, ey, s)
        glint(c, qx, qy, 9, 1.0, PEARL)
        if nb == 3:
            C(c, "THE MOON", 1600, 380, vis(t, 0.4), ts, size=34, dot=SILVER)
            C(c, "2026 QQ8 · A FEW METERS AT MOST", 420, 960, vis(t, B(1, 0.3)), ts, size=30, dot=PEACH)
            twin = vis(t, B(2, 0.35), d=0.8)
            if twin > 0:
                moon_d(c, 1500, 760, 170, "twin", glow=1.0, a=twin)
                T(c, "TWO BIG MOONS?", 1500, 1010, 70, ts, PEACH, twin, maxw=800, shadow=16)
        else:
            C(c, "2026 QQ8 (TINY)", 1450, 900, vis(t, 0.5), ts, size=30, dot=PEACH)
    run_panels(c, W, H, t, S, [(0, pA)])

# ------------------------------------------------------------------ mn7_news
def eyepiece(c, x, y, r, t, dot_a=1.0):
    c.save(); p = skia.Path(); p.addCircle(x, y, r); c.clipPath(p, doAntiAlias=True)
    c.drawCircle(x, y, r, paint("#04030a"))
    rng = random.Random(5)
    for _ in range(90):
        circle(c, x + rng.uniform(-r, r), y + rng.uniform(-r, r), rng.uniform(1, 3.2), "#ffffff", rng.uniform(0.3, 0.9))
    q = (t * 0.12) % 1
    dx = lerp(-r * 0.7, r * 0.7, q); dy = lerp(r * 0.3, -r * 0.2, q)
    for k in range(6): circle(c, x + dx - k * 9, y + dy + k * 2, 5 - k * 0.6, PEARL, dot_a * (1 - k / 6))
    c.restore()
    c.drawCircle(x, y, r, paint("#cfc6e8", 0.8, stroke=10))
    for a_ in (0, 90, 180, 270):
        an = math.radians(a_); line(c, x + math.cos(an) * r * 0.85, y + math.sin(an) * r * 0.85, x + math.cos(an) * r * 0.97, y + math.sin(an) * r * 0.97, "#cfc6e8", 3, 0.6)

def scale_bar(c, t, ts, x, y, a=1.0):
    """person (1.8 m) next to a 1-2 m rock range."""
    person(c, x, y, 300, "#cfc6e8", a=a)
    NW.rock(c, x + 260, y - 85, 85, 31, sq=0.8, a=a)
    rrect(c, x + 160, y - 250, 200, 14, 7, PEACH, 0.35 * a)
    rrect(c, x + 175, y - 250, 85, 14, 7, PEACH, 0.9 * a)
    T(c, "1–2 M?", x + 260, y - 290, 40, ts, PEACH, a, maxw=300)
    T(c, "1.8 M", x, y - 340, 32, ts, "#cfc6e8", a, w=700, fam="Inter", maxw=200)

def mn7_news(c, W, H, t, S):
    mode = S.opts.get("mode", "long")
    B = beats(S, 4)
    def pSpot(c, ts):
        eyepiece(c, 600, 540, 330, t)
        C(c, "20 AUG 2026: A FAINT MOVING DOT", 1360, 360, vis(t, 0.3), ts, size=34, dot=PEARL)
        C(c, "ROCK... OR SPACE JUNK?", 1360, 480, vis(t, B(0, 0.55)), ts, size=36, bg=YEL, fg=INK, a=1)
        T(c, "?", 1360, 690, 160, ts, PEACH, vis(t, B(0, 0.6)), maxw=200)
    def pMPC(c, ts):
        p = vis(t, B(1, 0.0) if mode == "long" else 0.1)
        rrect(c, 260, 220, 900, 640, 30, "#170c24", 0.92 * p); rrect(c, 260, 220, 900, 640, 30, LILAC, 0.6 * p, stroke=4)
        T(c, "MINOR PLANET CENTER (IAU)", 710, 300, 34, ts, LILAC, p, w=700, fam="Inter", maxw=820)
        T(c, "29 OCTOBER 2026", 710, 360, 30, ts, "#cfc6e8", p, w=600, fam="Inter", maxw=820)
        T(c, "2026 QQ8", 710, 500, 130, ts, "#ffffff", p, maxw=820)
        check(c, 385, 660, 30, vis(t, (B(1, 0.45) if mode == "long" else 0.6)))
        T(c, "NATURAL · LIKELY A TINY ASTEROID", 760, 662, 34, ts, GREEN, vis(t, (B(1, 0.45) if mode == "long" else 0.6)), w=800, maxw=640)
        T(c, "TEMPORARY MINI-MOON", 710, 780, 40, ts, PEACH, vis(t, (B(1, 0.7) if mode == "long" else 1.2)), maxw=820)
        NW.rock(c, 1550, 470, 170, 31, sq=0.8, rot=t * 6)
        if mode != "long": scale_bar(c, t, ts, 1420, 1000, vis(t, S.lt(0, 0.5)))
    def pLoops(c, ts):
        ex, ey = 800, 560
        orbit_ring(c, ex, ey, 384 * 1.0, 384 * 0.5, LILAC, t, 0.9)
        c.drawOval(skia.Rect.MakeLTRB(ex - 568, ey - 568 * 0.5, ex + 568, ey + 568 * 0.5), paint(PEACH, 0.45, stroke=2.5))
        th = t * 0.12; moon_d(c, ex + math.cos(th) * 384, ey + math.sin(th) * 192, 30, "moon", glow=0.6)
        s = 0.4 + t * 0.45
        loop_path(c, ex, ey, max(0, s - 5.0), s, PEARL, 0.55, w=3, A=650, B=95, sq=0.5, k=4.6)
        earth(c, ex, ey, 90, rot=150 + t * 3)
        qx, qy = qq8_xy(ex, ey, s, A=650, B=95, sq=0.5, k=4.6); glint(c, qx, qy, 8, 1, PEARL)
        C(c, "CLOSEST QQ8 GETS: ≈568,000 KM", ex, ey + 335, 1, ts, size=30, dot=PEACH)
        if not S.P:
            C(c, "MOON: 384,400 KM", ex, ey - 225, 1, ts, size=28, dot=LILAC)
            C(c, "CAUGHT: ≈APRIL 2026", 1640, 300, vis(t, 0.3), ts, size=34, bg=YEL, fg=INK, a=1)
            C(c, "MESSY LOOPS", 1640, 420, vis(t, 0.8), ts, size=32)
            C(c, "≈1.5× THE MOON'S DISTANCE", 1640, 540, vis(t, B(2, 0.75)), ts, size=30)
        else:
            C(c, "≈1.5× THE MOON'S DISTANCE", ex, 40, vis(t, S.lt(0, 0.4)), ts, size=30, bg=YEL, fg=INK, a=1)
        C(c, "PATH: SCHEMATIC", 1700, 1010, 1, ts, size=22)
    def pUnknown(c, ts):
        T(c, "CONFIRMED", 480, 230, 50, ts, GREEN, 1, maxw=700)
        for k, s_ in enumerate(["NATURAL OBJECT", "BOUND TO EARTH SINCE ≈APRIL", "STAYS THROUGH DECEMBER"]):
            C(c, s_, 480, 340 + k * 105, vis(t, B(3, 0.0) + k * 0.25), ts, size=30, dot=GREEN)
        T(c, "STILL UNKNOWN", 1400, 230, 50, ts, PEACH, vis(t, B(3, 0.1)), maxw=700)
        scale_bar(c, t, ts, 1230, 820, vis(t, B(3, 0.15)))
        C(c, "EXIT DATE: EARLY 2027?", 1400, 930, vis(t, B(3, 0.55)), ts, size=34, bg=YEL, fg=INK, a=1)
    if mode == "short": items = [(0, pMPC)]
    elif mode == "loops": items = [(0, pLoops)]
    else: items = [(0, pSpot), (B(1, 0), pMPC), (B(2, 0), pLoops), (B(3, 0), pUnknown)]
    run_panels(c, W, H, t, S, items)

# ------------------------------------------------------------------ mn7_mini
def bus(c, x, y, w, a=1.0):
    h = w * 0.33
    rrect(c, x - w / 2, y - h, w, h, h * 0.15, "#e04a3a", a)
    for k in range(6): rrect(c, x - w / 2 + w * 0.06 + k * w * 0.15, y - h * 0.85, w * 0.11, h * 0.35, 4, "#ffe7c4", a * 0.85)
    for xx in (x - w * 0.3, x + w * 0.3): circle(c, xx, y, h * 0.16, "#160d22", a)

def mn7_mini(c, W, H, t, S):
    B = beats(S, 4)
    def pSix(c, ts):
        ex, ey = 800, 560
        for k in range(6):
            s = t * (0.35 + 0.05 * k) + k * 1.1
            x, y = qq8_xy(ex, ey, s, A=300 + 55 * k, B=50 + 10 * k, sq=0.5, k=3.6 + 0.4 * k)
            loop_path(c, ex, ey, s - 1.6, s, PEARL, 0.25, w=2, A=300 + 55 * k, B=50 + 10 * k, sq=0.5, k=3.6 + 0.4 * k)
            glint(c, x, y, 5, vis(t, 0.3 + k * 0.35), PEARL)
        earth(c, ex, ey, 110, rot=170 + t * 3)
        C(c, "IT HAPPENS ALL THE TIME", 1560, 330, vis(t, 0.2), ts, size=34)
        C(c, "UP TO 6 AT ONCE? (ONE ESTIMATE)", 1560, 450, vis(t, B(1, 0.45)), ts, size=30, bg=YEL, fg=INK, a=1)
        C(c, "MOST TOO SMALL TO SPOT", 1560, 570, vis(t, B(1, 0.85)), ts, size=30)
    def pPast(c, ts):
        x0, x1, y = 260, 1660, 470
        line(c, x0, y, x1, y, "#ffffff", 5, 0.35)
        for f, top, bot, tt, colr in [(0.15, "2020 CD3", "MONTHS", B(2, 0.05), LILAC), (0.55, "2024 PT5", "57 DAYS", B(2, 0.45), PEACH),
                                       (0.92, "2026 QQ8", "NOW", B(2, 0.0), GREEN)]:
            x = lerp(x0, x1, f); p = vis(t, tt)
            circle(c, x, y, 18 * eback(p), colr, p)
            T(c, top, x, y - 80, 50, ts, colr, p, maxw=480)
            T(c, bot, x, y + 75, 36, ts, "#e8dcf0", p, w=700, fam="Inter", maxw=420)
        p = vis(t, B(2, 0.6))
        bus(c, 1030, 860, 330, p); NW.rock(c, 1030, 720, 70, 13, sq=0.7, a=p)
        T(c, "PT5 ≈ 10 M ≈ A BUS", 1030, 960, 36, ts, PEACH, p, maxw=700)
    def pPT5(c, ts):
        ex, ey = 520, 600
        earth(c, ex, ey, 90, rot=150)
        p = skia.Path(); p.addArc(skia.Rect.MakeLTRB(ex - 300, ey - 300, ex + 300, ey + 300), 200, 90 * ease(prog(t, B(3, 0.0), 2.5)))
        c.drawPath(p, paint(PEACH, 0.85, stroke=5))
        T(c, "¼ OF A LOOP", ex, ey + 380, 40, ts, PEACH, vis(t, B(3, 0.2)), maxw=600)
        # spectra
        x0, x1, yb = 1000, 1780, 640
        rrect(c, x0 - 30, 330, x1 - x0 + 60, 400, 20, "#170c24", 0.9)
        for k, (colr, off) in enumerate([(SILVER, 0), (PEACH, 6)]):
            pp = vis(t, B(3, 0.2) + k * 0.6); pth = skia.Path()
            for i in range(61):
                x = lerp(x0, x1, i / 60); yy = yb - 180 * (0.35 + 0.5 * (i / 60) - 0.18 * math.exp(-((i - 18) / 7) ** 2) - 0.1 * math.exp(-((i - 45) / 6) ** 2)) - off
                if i == 0: pth.moveTo(x, yy)
                else: pth.lineTo(x, yy)
            c.drawPath(pth, paint(colr, pp, stroke=5))
        T(c, "MOON ROCK", 1180, 380, 30, ts, SILVER, vis(t, B(3, 0.2)), w=800, maxw=360)
        T(c, "2024 PT5", 1600, 380, 30, ts, PEACH, vis(t, B(3, 0.8)), w=800, maxw=360)
        C(c, "MATCH: MAYBE A PIECE OF THE MOON", 1390, 800, vis(t, B(3, 0.5)), ts, size=30, bg=YEL, fg=INK, a=1)
        C(c, "SPECTRA: SCHEMATIC", 1390, 900, vis(t, B(3, 0.5)), ts, size=22)
    run_panels(c, W, H, t, S, [(0, pSix), (B(2, 0), pPast), (B(3, 0), pPT5)])

# ------------------------------------------------------------------ mn7_rules
def mn7_rules(c, W, H, t, S):
    B = beats(S, 4)
    def pTwin(c, ts):
        moon_d(c, 620, 500, 230, "moon"); moon_d(c, 1300, 500, 230, "twin")
        T(c, "THE MOON", 620, 820, 50, ts, SILVER, 1, maxw=600); T(c, "THE TWIN", 1300, 820, 50, ts, PEACH, 1, maxw=600)
        C(c, "SAME SIZE · SAME ROCK · SAME MASS", 960, 950, vis(t, B(0, 0.5)), ts, size=34, bg=YEL, fg=INK, a=1)
    def pOrbit(c, ts):
        ex, ey = 720, 540
        orbit_ring(c, ex, ey, 620, 300, LILAC, t); orbit_ring(c, ex, ey, 310, 150, PEACH, t)
        d0 = max(0.0, t - B(1, 0.0))
        thm = 0.3 + d0 * 0.12; tht = 0.3 + d0 * 0.12 * 2.83
        mp = (ex + math.cos(thm) * 620, ey + math.sin(thm) * 300); tp = (ex + math.cos(tht) * 310, ey + math.sin(tht) * 150)
        earth(c, ex, ey, 80, rot=150 + t * 4)
        moon_d(c, mp[0], mp[1], 44, "moon", glow=0.6); moon_d(c, tp[0], tp[1], 44, "twin", glow=0.6)
        C(c, "MOON: 384,400 KM", ex - 330, ey - 330, vis(t, B(1, 0.1)), ts, size=28, dot=LILAC)
        C(c, "TWIN: ≈192,000 KM", ex - 330, ey - 250, vis(t, B(1, 0.35)), ts, size=28, dot=PEACH)
        T(c, "LAP TIME", 1640, 250, 40, ts, "#ffffff", vis(t, B(2, 0.1)), maxw=520)
        C(c, "TWIN: ≈9.7 DAYS", 1640, 360, vis(t, B(2, 0.35)), ts, size=32, dot=PEACH)
        C(c, "MOON: 27.3 DAYS", 1640, 460, vis(t, B(2, 0.35)), ts, size=32, dot=LILAC)
        lp = vis(t, B(3, 0.0))
        if lp > 0:
            q = ((t - B(3, 0.0)) * 0.7) % 1
            for (px, py, colr, sp) in ((tp[0], tp[1], PEACH, 2.0), (mp[0], mp[1], LILAC, 1.0)):
                qq = min(1, q * sp)
                circle(c, lerp(px, ex, qq), lerp(py, ey, qq), 9, colr, lp * (1 - qq * 0.3))
            C(c, "LIGHT: 0.64 S FROM THE TWIN", 1640, 640, lp, ts, size=28, dot=PEACH)
            C(c, "1.28 S FROM THE MOON", 1640, 740, vis(t, B(3, 0.5)), ts, size=28, dot=LILAC)
        C(c, "NOT TO SCALE (SIZES)", 1700, 1010, 1, ts, size=22)
    run_panels(c, W, H, t, S, [(0, pTwin), (B(1, 0), pOrbit)])

# ------------------------------------------------------------------ mn7_sky
def night_land(c, t, rise=1.0, both=True, ts=1.0, hy=800, shadows=True):
    tx, ty = lerp(380, 520, rise), lerp(900, 430, rise)
    mx, my = 1500, 260
    moon_d(c, mx, my, 70, "moon", frac=0.9, sun_ang=200, glow=1.0, a=1 if both else 0)
    moon_d(c, tx, ty, 150, "twin", glow=1.3)
    ground(c, hy)
    lights = [(tx, ty, "#21154f", 1.0)] + ([(mx, my, "#4a1236", 0.9)] if both else [])
    if shadows: scene_objects(c, t, lights, hy, xs=(860, 1240))
    c.drawRect(skia.Rect.MakeLTRB(0, hy - 120, VW, VH), paint(shader=lin(0, hy - 120, 0, VH, [(0, PEARL, 0.0), (1, PEARL, 0.06 * rise)])))
    return tx, ty

def phases_row(c, t, y, kind, period, days, x0=420, x1=1760, n=8, R=46):
    for k in range(n):
        d = days * k / (n - 1)
        f = 0.5 - 0.5 * math.cos(2 * math.pi * d / period)
        moon_d(c, lerp(x0, x1, k / (n - 1)), y, R, kind, frac=f, sun_ang=0 if (d / period) % 1 < 0.5 else 180, glow=0.3, dark="#1a0f28")

def mn7_sky(c, W, H, t, S):
    mode = S.opts.get("mode", "long")
    B = beats(S, 5)
    def pRise(c, ts):
        r = ease(prog(t, 0.2, 3.5 if mode == "long" else 1.6))
        tx, ty = night_land(c, t, r, both=True, ts=ts, shadows=False)
        p = vis(t, B(1, 0.15) if mode == "long" else S.lt(0, 0.4))
        C(c, "2× WIDER", 1150, 520, p, ts, size=40, bg=YEL, fg=INK, a=1)
        C(c, "4× THE AREA → ≈4× THE LIGHT", 1150, 640, vis(t, B(1, 0.45) if mode == "long" else S.lt(0, 0.7)), ts, size=32)
    def pPhases(c, ts):
        T(c, "30 NIGHTS", 960, 210, 44, ts, "#ffffff", 1, maxw=800)
        T(c, "TWIN", 210, 420, 40, ts, PEACH, 1, maxw=300); T(c, "MOON", 210, 640, 40, ts, SILVER, 1, maxw=300)
        phases_row(c, t, 420, "twin", 9.9, 30); phases_row(c, t, 640, "moon", 29.5, 30)
        C(c, "TWIN: NEW → FULL → NEW IN ≈10 DAYS", 960, 820, vis(t, B(2, 0.4)), ts, size=30, dot=PEACH)
        C(c, "BOTH FULL: SILVER NIGHTS", 960, 930, vis(t, B(3, 0.5)), ts, size=30, bg=YEL, fg=INK, a=1)
        C(c, "TIDALLY LOCKED: ONE FACE", 1500, 300, vis(t, B(2, 0.1)), ts, size=26)
    def pShadow(c, ts):
        night_land(c, t, 1.0, both=True, ts=ts)
        C(c, "TWO MOONS = TWO SHADOWS", 960, 140, vis(t, 0.3 if mode != "long" else B(4, 0.2)), ts, size=36, bg=YEL, fg=INK, a=1)
    if mode == "short": items = [(0, pRise)]
    elif mode == "shadows": items = [(0, pShadow)]
    else: items = [(0, pRise), (B(2, 0), pPhases), (B(4, 0), pShadow)]
    run_panels(c, W, H, t, S, items)

# ------------------------------------------------------------------ mn7_tide
def cube8(c, x, y, s, p, colr=PEACH):
    """2x2x2 cube = 8 (isometric)."""
    if p <= 0: return
    dx, dy = s * 0.87, s * 0.5
    order = [(i, j, k) for k in range(2) for j in range(2) for i in (1, 0)]
    for (i, j, k) in sorted(order, key=lambda q: (q[2], -q[1], q[0])):
        q = clamp(p * 8 - (i + 2 * j + 4 * k) * 0.6)
        if q <= 0: continue
        ox = x + (i - j) * dx; oy = y + (i + j) * dy - k * s
        top = [(ox, oy - s), (ox + dx, oy - s + dy), (ox, oy - s + 2 * dy), (ox - dx, oy - s + dy)]
        left = [(ox - dx, oy - s + dy), (ox, oy - s + 2 * dy), (ox, oy + 2 * dy), (ox - dx, oy + dy)]
        right = [(ox, oy - s + 2 * dy), (ox + dx, oy - s + dy), (ox + dx, oy + dy), (ox, oy + 2 * dy)]
        c.drawPath(poly(left), paint(mix(colr, "#000000", 0.35), q)); c.drawPath(poly(right), paint(mix(colr, "#000000", 0.15), q))
        c.drawPath(poly(top), paint(mix(colr, "#ffffff", 0.25), q))
        for pp in (top, left, right): c.drawPath(poly(pp), paint(INK, q * 0.8, stroke=3))

def beach(c, t, amp, period=6.0, hy=640, a=1.0):
    stage_bg(c, "#1a0e2a", "#3a1e44")
    stars(c, VW, VH, t, 0.5, seed=91)
    lvl = hy + amp * math.sin(2 * math.pi * t / period)
    c.drawPath(poly([(0, 980), (VW, 600), (VW, VH), (0, VH)]), paint("#9a7f8e", a))  # sloping shore
    for k in range(9):
        y = lerp(980, 600, k / 8) - 40; x = VW * k / 8
        line(c, x - 40, y + 60, x + 40, y + 48, "#6e5668", 4, 0.6 * a)
    c.save(); c.clipRect(skia.Rect.MakeLTRB(0, lvl, VW, VH))
    c.drawRect(skia.Rect.MakeLTRB(0, lvl, VW, VH), paint(shader=lin(0, lvl, 0, VH, [(0, "#3a7fd0", 0.92 * a), (1, "#14315f", 0.95 * a)])))
    for k in range(5): line(c, 0, lvl + 6 + k * 40, VW, lvl + 6 + k * 40 + 8 * math.sin(t + k), "#9fd0ff", 2, 0.25 * a)
    c.restore()
    return lvl

def tide_bulge(c, ex, ey, R, stretch, ang, t, a=1.0, colr=SEA):
    c.save(); c.translate(ex, ey); c.rotate(ang)
    c.drawOval(skia.Rect.MakeLTRB(-R * (1 + stretch), -R * (1 - stretch * 0.35), R * (1 + stretch), R * (1 - stretch * 0.35)), paint(colr, 0.35 * a))
    c.drawOval(skia.Rect.MakeLTRB(-R * (1 + stretch), -R * (1 - stretch * 0.35), R * (1 + stretch), R * (1 - stretch * 0.35)), paint(colr, 0.9 * a, stroke=4))
    c.restore()

def mn7_tide(c, W, H, t, S):
    mode = S.opts.get("mode", "long")
    B = beats(S, 5)
    def pSea(c, ts):
        beach(c, t, 120, 5.0)
        moon_d(c, 1500, 200, 80, "twin", glow=1.0); moon_d(c, 300, 160, 40, "moon", frac=0.6, sun_ang=180, glow=0.6)
    def pCube(c, ts):
        ex, ey = 560, 560
        st = 0.05 + 0.25 * ease(prog(t, (B(1, 0.6) if mode == "long" else 0.3), 1.2))
        tide_bulge(c, ex, ey, 200, st, 0, t)
        earth(c, ex, ey, 200, rot=150)
        moon_d(c, 1060, 560, 60, "twin", glow=0.8)
        for (yy, L, lab) in ((ey, 150, "NEAR SIDE: STRONGER"), (ey + 0, 0, "")):
            pass
        arrow(c, ex + 210, ey - 250, ex + 380, ey - 250, PEACH, 7)
        arrow(c, ex - 210, ey - 250, ex - 300, ey - 250, PEACH, 7)
        T(c, "PULL DIFFERS ACROSS EARTH", ex, ey - 330, 34, ts, "#ffffff", vis(t, 0.3), w=800, maxw=760)
        cube8(c, 1500, 470, 95, ease(prog(t, (B(1, 0.55) if mode == "long" else 0.4), 1.4)))
        T(c, "½ DISTANCE → 2 × 2 × 2 = 8×", 1500, 820, 40, ts, PEACH, vis(t, (B(1, 0.6) if mode == "long" else 0.6)), maxw=760)
        C(c, "TIDAL PULL ~ 1 / DISTANCE³", 1500, 930, vis(t, (B(1, 0.3) if mode == "long" else 0.9)), ts, size=30)
    def pBars(c, ts):
        x0, yb = 380, 900
        items = [("SUN", 0.46, SUNY, B(2, 0.5)), ("MOON", 1.0, SILVER, B(2, 0.1)), ("TWIN", 8.0, PEACH, B(2, 0.2))]
        for k, (lab, v, colr, tt) in enumerate(items):
            p = ease(prog(t, tt, 0.9)); x = x0 + k * 260; h = 70 * v * p
            rrect(c, x - 80, yb - h, 160, h, 12, colr, 1)
            T(c, lab, x, yb + 50, 34, ts, colr, 1, maxw=240)
            T(c, f"{v:g}×" if v != 0.46 else "≈0.46×", x, yb - h - 40, 34, ts, "#ffffff", p, maxw=240)
        # today vs with twin
        x2 = 1450; p2 = ease(prog(t, B(2, 0.6), 1.0))
        rrect(c, x2 - 170, yb - 70 * 1.46, 140, 70 * 1.46, 12, LILAC, 1)
        rrect(c, x2 + 30, yb - 70 * 9.46 * p2, 140, 70 * 9.46 * p2, 12, PEACH, 1)
        T(c, "TODAY'S MAX", x2 - 100, yb + 50, 26, ts, LILAC, 1, maxw=220); T(c, "WITH TWIN", x2 + 100, yb + 50, 26, ts, PEACH, 1, maxw=220)
        T(c, ">6×", x2 + 100, yb - 70 * 9.46 * p2 - 50, 56, ts, YEL, p2, maxw=260)
        C(c, "TIDAL PULL (MOON = 1)", 960, 95, 1, ts, size=26)
    def pFlats(c, ts):
        lvl = beach(c, t, 210, 4.0)
        C(c, "EXACT HEIGHTS: NOBODY KNOWS", 960, 150, vis(t, B(3, 0.1)), ts, size=34, bg=YEL, fg=INK, a=1)
        C(c, "EVERY COAST IS DIFFERENT", 960, 260, vis(t, B(3, 0.4)), ts, size=30)
    def pBeat(c, ts):
        x0, x1 = 160, 1760
        rows = [(320, "MOON TIDE", SILVER, lambda x: 0.35 * math.sin(x * 2 * math.pi / 12.42)),
                (560, "TWIN TIDE", PEACH, lambda x: 1.0 * math.sin(x * 2 * math.pi / 13.4)),
                (840, "TOGETHER", YEL, lambda x: 0.35 * math.sin(x * 2 * math.pi / 12.42) + math.sin(x * 2 * math.pi / 13.4))]
        for k, (y, lab, colr, f) in enumerate(rows):
            p = vis(t, B(4, 0.0) + k * 0.5)
            pth = skia.Path(); sh = (t - B(4, 0)) * 6
            for i in range(241):
                hr = i / 240 * 170 + sh; x = lerp(x0, x1, i / 240); yy = y - 80 * f(hr) * (0.75 if k == 2 else 1)
                if i == 0: pth.moveTo(x, yy)
                else: pth.lineTo(x, yy)
            c.drawPath(pth, paint(colr, p, stroke=5))
            T(c, lab, x0 + 140, y - 120 if k < 2 else y - 160, 30, ts, colr, p, w=800, maxw=360)
        C(c, "SCHEMATIC", 1700, 1020, 1, ts, size=22)
    if mode == "short": items = [(0, pCube)]
    else: items = [(0, pSea), (B(1, 0), pCube), (B(2, 0), pBars), (B(3, 0), pFlats), (B(4, 0), pBeat)]
    run_panels(c, W, H, t, S, items)

# ------------------------------------------------------------------ mn7_eclipse  (line 0 = like & subscribe: keep y > 790 clear)
def corona(c, x, y, r, t, a=1.0, hide=0.0):
    if a <= 0: return
    c.drawCircle(x, y, r * 3.2, paint(shader=rad(x, y, r * 3.2, [(0.3, "#ffffff", 0.55 * a), (0.45, "#e8e4ff", 0.25 * a), (1, "#e8e4ff", 0)])))
    c.save(); c.translate(x, y)
    for k in range(14):
        c.rotate(360 / 14 + 3 * math.sin(t * 0.3 + k))
        L = r * (2.0 + 0.8 * math.sin(k * 2.1))
        c.drawPath(poly([(-r * 0.12, -r * 0.95), (0, -L), (r * 0.12, -r * 0.95)]), paint("#f4f0ff", 0.18 * a, blur=r * 0.04))
    c.restore()

def mn7_eclipse(c, W, H, t, S):
    B = beats(S, 5)
    def pSlide(c, ts):
        sx, sy, sr = 1150, 360, 70
        q = ease(prog(t, B(1, 0.0), max(0.8, S.le(1) - S.ls(1))))
        sun_d(c, sx, sy, sr, t, a=1 - 0.85 * q)
        corona(c, sx, sy, sr, t, a=q)
        tx = lerp(380, sx, q); ty = lerp(250, sy, q)
        moon_d(c, tx, ty, 140, "twin", frac=1.0 - q, sun_ang=0, glow=0.6 * (1 - q), dark="#120a1c")
        moon_d(c, 1700, 200, 60, "moon", frac=0.5, sun_ang=180, glow=0.6)
        C(c, "AN ECLIPSE BY THE TWIN", 1150, 640, vis(t, B(1, 0.4)), ts, size=34)
    def pToday(c, ts):
        sx, sy, sr = 960, 450, 150
        corona(c, sx, sy, sr, t)
        circle(c, sx, sy, sr * 1.01, "#06030a")
        T(c, "TODAY: THE MOON ONLY JUST COVERS THE SUN", 960, 870, 40, ts, SILVER, 1, maxw=1500)
        C(c, "THE CORONA SHINES OUT AROUND IT", 960, 970, vis(t, B(2, 0.5)), ts, size=30)
    def pTwin(c, ts):
        for (x, rm, lab, colr) in ((560, 100, "MOON", SILVER), (1360, 200, "TWIN", PEACH)):
            corona(c, x, 440, 100, t)
            circle(c, x, 440, rm, "#06030a"); c.drawCircle(x, 440, rm, paint(colr, 0.5, stroke=3))
            T(c, lab, x, 780, 44, ts, colr, 1, maxw=400)
        C(c, "2× THE SUN'S WIDTH", 1360, 880, vis(t, B(3, 0.2)), ts, size=30, dot=PEACH)
        C(c, "WIDER SHADOW · LESS INNER CORONA", 1360, 970, vis(t, B(3, 0.6)), ts, size=28)
        C(c, "BY OUR ROUGH MATH", 560, 970, 1, ts, size=24)
    def pMutual(c, ts):
        q = ease(prog(t, B(4, 0.35), 2.5))
        moon_d(c, 960, 480, 120, "moon", frac=0.95, sun_ang=200, glow=0.8)
        moon_d(c, lerp(200, 960, q), lerp(430, 470, q), 240, "twin", frac=0.15, sun_ang=200, glow=0.3, dark="#120a1c")
        C(c, "ECLIPSES: PROBABLY FAR MORE OFTEN", 960, 860, vis(t, B(4, 0.0)), ts, size=30, dot=PEACH)
        C(c, "A MOON ECLIPSING A MOON", 960, 970, vis(t, B(4, 0.7)), ts, size=34, bg=YEL, fg=INK, a=1)
    run_panels(c, W, H, t, S, [(0, pSlide), (B(2, 0), pToday), (B(3, 0), pTwin), (B(4, 0), pMutual)])

# ------------------------------------------------------------------ mn7_spin
def grid64(c, x, y, s, p, colr=PEACH):
    for k in range(64):
        q = clamp(p * 64 - k * 0.6)
        if q <= 0: continue
        i, j = k % 8, k // 8
        rrect(c, x + i * s * 1.15, y + j * s * 1.15, s, s, s * 0.2, colr, q)

_PE = {}
def polar_earth(R):
    if R not in _PE:
        arr = geo.globe_img(R, 0, tilt=89, light=(0.0, 0.0, 1.0), ambient=0.55)
        _PE[R] = skia.Image.fromarray(arr, colorType=skia.kRGBA_8888_ColorType, alphaType=skia.kPremul_AlphaType)
    return _PE[R]

def mn7_spin(c, W, H, t, S):
    B = beats(S, 5)
    def pBrake(c, ts):
        ex, ey = 720, 560
        c.save(); c.translate(ex, ey); c.rotate(-14)
        c.drawOval(skia.Rect.MakeLTRB(-300, -205, 300, 205), paint(SEA, 0.35)); c.drawOval(skia.Rect.MakeLTRB(-300, -205, 300, 205), paint(SEA, 0.9, stroke=4))
        c.restore()
        # north-pole view of Earth: dark disc with spin arrow
        c.save(); c.translate(ex, ey); c.rotate(-t * 25)
        c.drawImage(polar_earth(230), -230, -230, skia.SamplingOptions(skia.FilterMode.kLinear), skia.Paint())
        c.restore()
        C(c, "VIEW FROM ABOVE THE NORTH POLE", ex, 1020, 1, ts, size=22)
        p = skia.Path(); p.addArc(skia.Rect.MakeLTRB(ex - 270, ey - 270, ex + 270, ey + 270), 200, 120); c.drawPath(p, paint("#ffffff", 0.8, stroke=7))
        arrow(c, ex + math.cos(math.radians(318)) * 270, ey + math.sin(math.radians(318)) * 270,
              ex + math.cos(math.radians(328)) * 270, ey + math.sin(math.radians(328)) * 270, "#ffffff", 7)
        moon_d(c, 1500, 560, 60, "moon", glow=0.7)
        line(c, ex + 290 * math.cos(math.radians(-14)), ey + 290 * math.sin(math.radians(-14)), 1440, 560, LILAC, 3, 0.6, dash=([10, 10], 0))
        C(c, "BULGE DRAGGED AHEAD", ex, 150, vis(t, B(1, 0.15)), ts, size=30, dot=SEA)
        C(c, "EARTH'S SPIN SLOWS", ex, 960, vis(t, B(1, 0.4)), ts, size=30, dot=RED)
        C(c, "MOON: +3.8 CM A YEAR", 1500, 700, vis(t, B(1, 0.75)), ts, size=30, bg=YEL, fg=INK, a=1)
        arrow(c, 1580, 560, 1720, 560, LILAC, 6, a=vis(t, B(1, 0.75)))
    def p64(c, ts):
        grid64(c, 1050, 230, 62, ease(prog(t, B(2, 0.3), 1.8)))
        rrect(c, 500, 465, 62, 62, 12, SILVER, 1)
        T(c, "MOON", 531, 600, 36, ts, SILVER, 1, maxw=300); T(c, "TWIN", 1400, 860, 36, ts, PEACH, 1, maxw=300)
        T(c, "×64", 760, 500, 110, ts, YEL, vis(t, B(2, 0.6)), maxw=400)
        C(c, "BRAKING ~ MASS² ÷ DISTANCE⁶ → 2⁶ = 64", 960, 980, vis(t, B(2, 0.4)), ts, size=30)
    def pClock(c, ts):
        q = ease(prog(t, B(3, 0.1), 2.5))
        clock(c, 560, 480, 230, q * 25 / 60, colr=PEACH)
        T(c, "+25 MIN", 560, 800, 64, ts, PEACH, 1, maxw=500)
        T(c, "PER MILLION YEARS (TWIN)", 560, 880, 30, ts, "#ffffff", 1, w=700, fam="Inter", maxw=600)
        clock(c, 1360, 480, 230, q * 25 / 60 / 65, colr=LILAC)
        T(c, "+23 S", 1360, 800, 64, ts, LILAC, vis(t, B(3, 0.5)), maxw=500)
        T(c, "PER MILLION YEARS (MOON ALONE, TIDES)", 1360, 880, 30, ts, "#ffffff", vis(t, B(3, 0.5)), w=700, fam="Inter", maxw=760)
        C(c, "BY OUR ROUGH MATH", 960, 990, 1, ts, size=24)
    def pSpiral(c, ts):
        ex, ey = 760, 560
        earth(c, ex, ey, 90, rot=150 + t)
        pth = skia.Path(); th_end = (t - B(4, 0)) * 1.6 + 2
        for i in range(301):
            th = th_end * i / 300; r = 150 + 18 * th
            x, y = ex + math.cos(th) * r, ey + math.sin(th) * r * 0.55
            if i == 0: pth.moveTo(x, y)
            else: pth.lineTo(x, y)
        c.drawPath(pth, paint(PEACH, 0.6, stroke=3, dash=([10, 8], 0)))
        r = 150 + 18 * th_end
        moon_d(c, ex + math.cos(th_end) * r, ey + math.sin(th_end) * r * 0.55, 40, "twin", glow=0.6)
        C(c, "TWIN: ≈45× FASTER", 1560, 360, vis(t, B(4, 0.1)), ts, size=32, dot=PEACH)
        C(c, "≈1.7 M A YEAR", 1560, 470, vis(t, B(4, 0.3)), ts, size=34, bg=YEL, fg=INK, a=1)
        C(c, "PAID FOR WITH EARTH'S SPIN", 1560, 580, vis(t, B(4, 0.65)), ts, size=28)
    run_panels(c, W, H, t, S, [(0, pBrake), (B(2, 0), p64), (B(3, 0), pClock), (B(4, 0), pSpiral)])

# ------------------------------------------------------------------ mn7_chaos
def flash(c, x, y, r, p, t):
    if p <= 0: return
    c.drawCircle(x, y, r * 2.5 * p, paint(shader=rad(x, y, r * 2.5 * p, [(0, "#ffffff", 0.95 * (1 - p * 0.5)), (0.3, PEACH, 0.6 * (1 - p * 0.5)), (1, PEACH, 0)])))
    rng = random.Random(4)
    for k in range(40):
        an = rng.random() * 6.28; sp = rng.uniform(0.4, 1.0)
        d = r * 3.2 * p * sp
        circle(c, x + math.cos(an) * d, y + math.sin(an) * d * 0.8, rng.uniform(3, 9) * (1 - p * 0.4), rng.choice([SILVER, PEARL, "#a8a0b8"]), 1 - p * 0.6)

def collision(c, t, t0, ts, cx=960, cy=500):
    q = clamp((t - t0) / 2.2)
    d = lerp(520, 0, ease(min(1, q * 1.4)))
    if q < 0.72:
        moon_d(c, cx - d * 0.6 - 60 * (1 - q), cy - d * 0.1, 150, "moon", glow=0.6)
        moon_d(c, cx + d * 0.6 + 60 * (1 - q), cy + d * 0.1, 150, "twin", glow=0.6)
    else:
        m = clamp((q - 0.72) / 0.28)
        orbit_ring(c, cx, cy, 330, 90, PEARL, t, a=m)
        moon_d(c, cx, cy, 190, "phobos", glow=0.6, a=m)
        c.drawCircle(cx, cy, 190, paint("#ff8a4a", 0.35 * m * (1 - clamp((t - t0 - 2.2) / 3)), blur=10))
    flash(c, cx, cy, 220, clamp((q - 0.6) / 0.4) * (1 - 0.8 * clamp((t - t0 - 1.8) / 1.5)), t)

def mn7_chaos(c, W, H, t, S):
    mode = S.opts.get("mode", "long")
    B = beats(S, 6)
    def pTug(c, ts):
        ex, ey = 760, 560
        orbit_ring(c, ex, ey, 620, 300, LILAC, t); orbit_ring(c, ex, ey, 310, 150, PEACH, t)
        thm = 0.3 + t * 0.08; tht = 0.3 + t * 0.08 * 2.83
        mp = (ex + math.cos(thm) * 620, ey + math.sin(thm) * 300); tp = (ex + math.cos(tht) * 310, ey + math.sin(tht) * 150)
        earth(c, ex, ey, 80, rot=150 + t * 4)
        moon_d(c, mp[0], mp[1], 44, "moon", glow=0.6); moon_d(c, tp[0], tp[1], 44, "twin", glow=0.6)
        al = max(0, math.cos(thm - tht)) ** 6
        line(c, mp[0], mp[1], tp[0], tp[1], YEL, 4 + 6 * al, 0.25 + 0.7 * al, dash=([12, 8], -t * 30))
        C(c, "EVERY LAP: A TUG", 1640, 300, vis(t, B(1, 0.2)), ts, size=32, dot=YEL)
        C(c, "MOON'S PULL ≈ 1/80 OF EARTH'S", 1640, 410, vis(t, B(1, 0.7)), ts, size=28)
    def pCreep(c, ts):
        ex, ey = 760, 560
        g = ease(prog(t, B(2, 0.1), 4.0)); rt = lerp(310, 540, g)
        orbit_ring(c, ex, ey, 620, 300, LILAC, t); orbit_ring(c, ex, ey, rt, rt * 0.48, PEACH, t)
        thm = 0.3 + t * 0.08; tht = 0.3 + t * 0.08 * lerp(2.83, 1.2, g)
        mp = (ex + math.cos(thm) * 620, ey + math.sin(thm) * 300); tp = (ex + math.cos(tht) * rt, ey + math.sin(tht) * rt * 0.48)
        earth(c, ex, ey, 80, rot=150 + t * 4)
        moon_d(c, mp[0], mp[1], 44, "moon", glow=0.6); moon_d(c, tp[0], tp[1], 44, "twin", glow=0.6)
        line(c, mp[0], mp[1], tp[0], tp[1], YEL, 6, 0.3 + 0.5 * g, dash=([12, 8], -t * 30))
        C(c, "GAP SHRINKS", 1640, 300, vis(t, B(2, 0.3)), ts, size=32, dot=PEACH)
        C(c, "TUGS START TO ADD UP", 1640, 410, vis(t, B(2, 0.7)), ts, size=30, bg=YEL, fg=INK, a=1)
    def pCanup(c, ts):
        rrect(c, 160, 200, 1600, 230, 28, "#170c24", 0.92); rrect(c, 160, 200, 1600, 230, 28, LILAC, 0.6, stroke=4)
        T(c, "CANUP, LEVISON & STEWART · 1999", 960, 275, 44, ts, "#ffffff", 1, maxw=1450)
        T(c, "MULTIPLE MOONS: \"TYPICALLY UNSTABLE\"", 960, 360, 36, ts, LILAC, vis(t, B(3, 0.25)), w=800, maxw=1450)
        p1 = vis(t, B(3, 0.55)); p2 = vis(t, B(3, 0.75))
        moon_d(c, 520, 680, 70, "moon", a=p1, glow=0.3); moon_d(c, 640, 690, 70, "twin", a=p1, glow=0.3); flash(c, 580, 685, 70, 0.35 * p1, t)
        T(c, "THEY COLLIDE", 580, 880, 44, ts, PEACH, p1, maxw=600)
        earth(c, 1330, 700, 90, a=p2); moon_d(c, 1430, 620, 40, "twin", a=p2, glow=0.3)
        arrow(c, 1480, 580, 1440, 610, PEACH, 5, a=p2)
        T(c, "OR ONE FALLS INTO EARTH", 1360, 880, 44, ts, PEACH, p2, maxw=700)
    def pMars(c, ts):
        mx, my, R = 700, 560, 260
        c.drawCircle(mx, my, R * 1.08, paint(shader=rad(mx, my, R * 1.08, [(0.85, "#ff8a5a", 0.3), (1, "#ff8a5a", 0)])))
        c.drawCircle(mx, my, R, paint(shader=rad(mx - R * 0.3, my - R * 0.3, R * 1.4, [(0, "#f0a070", 1), (0.6, "#c0603a", 1), (1, "#5a2414", 1)])))
        rng = random.Random(8)
        for _ in range(8): circle(c, mx + rng.uniform(-0.6, 0.6) * R, my + rng.uniform(-0.6, 0.6) * R, R * rng.uniform(0.08, 0.2), "#8a3a22", 0.45, blur=8)
        oval(c, mx, my - R * 0.8, R * 0.18, R * 0.08, "#fff4ee", 0.85)
        th = t * 1.2
        orbit_ring(c, mx, my, R * 1.45, R * 0.42, "#ffb08a", t)
        px, py = mx + math.cos(th) * R * 1.45, my + math.sin(th) * R * 0.42
        if math.sin(th) >= 0 or True:
            c.save(); c.translate(px, py); c.scale(1.4, 0.95); moon_d(c, 0, 0, 30, "phobos", glow=0.2); c.restore()
        C(c, "PHOBOS: ≈2 M CLOSER EVERY CENTURY", 1470, 360, vis(t, B(4, 0.3)), ts, size=28, dot="#ffb08a")
        C(c, "PULLED APART IN 30–50 MILLION YEARS", 1470, 480, vis(t, B(4, 0.65)), ts, size=28, bg=YEL, fg=INK, a=1)
        T(c, "MARS", mx, my + R + 70, 44, ts, "#ffb08a", 1, maxw=400)
    def pCrash(c, ts):
        collision(c, t, (B(5, 0.25) if mode == "long" else 0.3), ts)
        C(c, "PROBABLY NOT FOREVER", 960, 950, vis(t, (B(5, 0.6) if mode == "long" else S.lt(0, 0.6))), ts, size=34, bg=YEL, fg=INK, a=1)
    if mode == "short": items = [(0, pCrash)]
    else: items = [(0, pTug), (B(2, 0), pCreep), (B(3, 0), pCanup), (B(4, 0), pMars), (B(5, 0), pCrash)]
    run_panels(c, W, H, t, S, items)

# ------------------------------------------------------------------ mn7_twist
def mn7_twist(c, W, H, t, S):
    B = beats(S, 7)
    def pTwist(c, ts):
        T(c, "THE TWIST", 960, 300, 150, ts, PEACH, eout(prog(t, 0.1, 0.4)), maxw=1500, shadow=18)
        earth(c, 960, 720, 170, rot=170)
        c.drawCircle(960, 720, 170, paint("#ff6a3a", 0.25))
        moon_d(c, 1350, 640, 50, "moon", glow=0.6); moon_d(c, 1450, 590, 17, "far", glow=0.5)
        C(c, "EARTH MAY HAVE TRIED THIS", 960, 970, vis(t, S.lt(0, 0.5)), ts, size=30)
    def pTrojan(c, ts):
        ex, ey = 760, 560; R = 400
        orbit_ring(c, ex, ey, R, R * 0.6, LILAC, t)
        th = -0.6 + (t - B(1, 0)) * 0.05
        mp = (ex + math.cos(th) * R, ey + math.sin(th) * R * 0.6); cp = (ex + math.cos(th - math.pi / 3) * R, ey + math.sin(th - math.pi / 3) * R * 0.6)
        earth(c, ex, ey, 90, rot=170)
        moon_d(c, mp[0], mp[1], 60, "moon", glow=0.7); moon_d(c, cp[0], cp[1], 20, "far", glow=0.8)
        line(c, ex, ey, mp[0], mp[1], "#ffffff", 2, 0.3); line(c, ex, ey, cp[0], cp[1], "#ffffff", 2, 0.3)
        line(c, mp[0], mp[1], cp[0], cp[1], "#ffffff", 2, 0.3)
        T(c, "60°", ex + 110, ey - 110, 34, ts, "#ffffff", vis(t, B(2, 0.2)), maxw=200)
        C(c, "JUTZI & ASPHAUG · NATURE · 2011", 1560, 260, vis(t, B(1, 0.1)), ts, size=26)
        C(c, "⅓ AS WIDE · 1/30 THE MASS", 1560, 370, vis(t, B(1, 0.55)), ts, size=30, dot=PEACH)
        C(c, "SHARED ORBIT · STABLE POINT", 1560, 480, vis(t, B(2, 0.1)), ts, size=30, dot=LILAC)
        C(c, "TENS OF MILLIONS OF YEARS", 1560, 590, vis(t, B(2, 0.5)), ts, size=30, bg=YEL, fg=INK, a=1)
        C(c, "MODEL · SIZES NOT TO SCALE", 1640, 1010, 1, ts, size=22)
    def pCrawl(c, ts):
        q = ease(prog(t, B(3, 0.1), max(1.0, S.le(3) - S.ls(3) - 0.4)))
        moon_d(c, 1150, 540, 300, "moon", glow=0.6)
        cx = lerp(200, 1150 - 300 - 40, q)
        moon_d(c, cx, 540, 100, "far", glow=0.6)
        for k in range(4): line(c, cx - 140 - k * 50, 500 + k * 25, cx - 200 - k * 50, 500 + k * 25, PEARL, 4, 0.4 * (1 - q))
        C(c, "≈7,000 KM/H", 450, 820, vis(t, B(3, 0.4)), ts, size=40, bg=YEL, fg=INK, a=1)
        C(c, "\"THE SLOWEST POSSIBLE COLLISION\"", 450, 930, vis(t, B(3, 0.7)), ts, size=26)
    def pSplat(c, ts):
        q = ease(prog(t, B(4, 0.0), 2.4))
        mx, my, R = 960, 520, 320
        moon_d(c, mx, my, R, "moon", glow=0.6)
        # splatter layer on the left limb
        c.save(); pth = skia.Path(); pth.addCircle(mx, my, R + 40 * q); c.clipPath(pth, doAntiAlias=True)
        c.save(); cp_ = skia.Path(); cp_.addCircle(mx - R * 1.9, my, lerp(R * 0.9, R * 1.65, q)); c.clipPath(cp_, doAntiAlias=True)
        c.drawCircle(mx, my, R + 30 * q, paint(shader=rad(mx - R, my, R * 1.3, [(0, "#f4efe8", 0.95), (1, "#cfc7d8", 0.85)])))
        rng = random.Random(3)
        for _ in range(60):
            circle(c, mx - R * rng.uniform(0.3, 1.05), my + R * rng.uniform(-0.9, 0.9), R * rng.uniform(0.02, 0.06), "#a59eb4", 0.6)
        c.restore(); c.restore()
        if q < 0.6: moon_d(c, mx - R - 60 * (1 - q * 1.6), my, 100 * (1 - q * 1.5), "far", glow=0.4, a=1 - q / 0.6)
        C(c, "A LAYER TENS OF KM THICK", 520, 950, vis(t, B(4, 0.25)), ts, size=30, dot=PEARL)
        C(c, "→ FAR-SIDE HIGHLANDS?", 1400, 950, vis(t, B(4, 0.6)), ts, size=32, bg=YEL, fg=INK, a=1)
    def pSides(c, ts):
        moon_d(c, 560, 470, 250, "moon", glow=0.6); moon_d(c, 1360, 470, 250, "far", glow=0.6)
        c.save(); pth = skia.Path(); pth.addCircle(560, 470, 250); c.clipPath(pth, doAntiAlias=True)
        for (fx, fy, rr) in ((-0.25, -0.3, 0.32), (0.2, -0.15, 0.28), (-0.35, 0.15, 0.25), (0.05, 0.25, 0.2)):
            circle(c, 560 + fx * 250, 470 + fy * 250, rr * 250, "#4a4e60", 0.55, blur=12)
        c.restore()
        C(c, "DARK, SMOOTH PLAINS", 560, 880, vis(t, B(5, 0.5)), ts, size=26, dot=SILVER)
        C(c, "RUGGED HIGHLANDS", 1360, 880, vis(t, B(5, 0.5)), ts, size=26, dot=PEACH)
        T(c, "THE SIDE WE SEE", 560, 800, 40, ts, SILVER, 1, maxw=600); T(c, "THE FAR SIDE", 1360, 800, 40, ts, PEACH, 1, maxw=600)
        C(c, "LOOKED LIKE OURS?", 960, 120, vis(t, B(5, 0.2)), ts, size=30)
        C(c, "STILL A HYPOTHESIS · DEBATED", 960, 990, vis(t, B(6, 0.1)), ts, size=32, bg=YEL, fg=INK, a=1)
    run_panels(c, W, H, t, S, [(0, pTwist), (B(1, 0), pTrojan), (B(3, 0), pCrawl), (B(4, 0), pSplat), (B(5, 0), pSides)])

# ===================================================================== SHORT: submoons (navy + mint)
def planet_disc(c, x, y, R, cols, a=1.0, bands=0):
    c.drawCircle(x, y, R, paint(shader=rad(x - R * 0.3, y - R * 0.3, R * 1.4, [(0, cols[0], a), (0.6, cols[1], a), (1, cols[2], a)])))
    for k in range(bands):
        c.save(); pth = skia.Path(); pth.addCircle(x, y, R); c.clipPath(pth, doAntiAlias=True)
        yy = y - R + (k + 0.5) * 2 * R / bands
        c.drawRect(skia.Rect.MakeLTRB(x - R, yy - R * 0.05, x + R, yy + R * 0.05), paint("#ffffff", 0.07 * a)); c.restore()

def mascon_moon(c, x, y, R, t, a=1.0):
    moon_d(c, x, y, R, "moon", glow=0.6, a=a)
    for (fx, fy, rr) in ((-0.3, -0.25, 0.2), (0.25, -0.1, 0.16), (-0.05, 0.3, 0.18), (0.4, 0.35, 0.12)):
        circle(c, x + fx * R, y + fy * R, rr * R * (1 + 0.08 * math.sin(t * 4)), RED, 0.35 * a, blur=R * 0.03)

def mn7_sub(c, W, H, t, S):
    mode = S.opts.get("mode", "intro")
    L = S.le(0)
    def pIntro(c, ts):
        motif_sub(c, VW, VH, t, type("U", (), dict(u=1.0, P=False))(), 960, 540, 1.3)
        T(c, "?", 1500, 400, 150, ts, MINT, eout(prog(t, 0.4, 0.4)), maxw=200)
    def pNone(c, ts):
        planet_disc(c, 330, 560, 230, ("#f2dcae", "#c9a36a", "#5a4026"), bands=7)
        for k, (x, y, r) in enumerate([(780, 360, 44), (960, 560, 56), (1150, 380, 38), (1320, 640, 50), (1520, 420, 46), (1720, 640, 36)]):
            moon_d(c, x, y, r, ["far", "moon", "phobos"][k % 3], glow=0.3)
            c.drawCircle(x, y, r * 1.9, paint(RED, 0.6 * vis(t, 0.5 + k * 0.15), stroke=3, dash=([8, 8], 0)))
            xmark(c, x + r * 1.35, y - r * 1.35, 16, vis(t, 0.5 + k * 0.15))
        C(c, "MOONS WITH MOONS: 0 KNOWN", 1250, 900, vis(t, 0.6), ts, size=34, bg=YEL, fg=INK, a=1)
    def pTides(c, ts):
        planet_disc(c, 300, 560, 260, ("#f2dcae", "#c9a36a", "#5a4026"), bands=7)
        mx, my = 1250, 560
        moon_d(c, mx, my, 90, "far", glow=0.5)
        q = prog(t, 0.6, max(1.0, L - 0.8))
        r = 200 + 260 * q ** 2; th = t * 2.2
        sx, sy = mx + math.cos(th) * r, my + math.sin(th) * r * 0.55
        orbit_ring(c, mx, my, 200, 110, MINT, t, a=1 - q)
        moon_d(c, sx, sy, 18, "phobos", glow=0.3)
        arrow(c, sx, sy, lerp(sx, 560, 0.25), lerp(sy, 560, 0.25), RED, 5, a=vis(t, 0.8))
        arrow(c, sx, sy, lerp(sx, mx, 0.35), lerp(sy, my, 0.35), MINT, 5, a=vis(t, 0.8))
        C(c, "KOLLMEIER & RAYMOND · 2019", 960, 130, vis(t, 0.2), ts, size=28)
        C(c, "TIDES: PLANET + MOON", 960, 960, vis(t, L * 0.55), ts, size=32, bg=YEL, fg=INK, a=1)
    def pHosts(c, ts):
        hosts = [("TITAN", lambda x, y, r: planet_disc(c, x, y, r, ("#f6d08a", "#d79a3e", "#6a4210"))),
                 ("CALLISTO", lambda x, y, r: moon_d(c, x, y, r, "phobos", glow=0.2)),
                 ("IAPETUS", None), ("OUR MOON", lambda x, y, r: moon_d(c, x, y, r, "moon", glow=0.4))]
        for k, (lab, f) in enumerate(hosts):
            x = 300 + k * 440; y = 500; p = vis(t, 0.2 + k * 0.45)
            with Layer(c, p):
                if f: f(x, y, 140)
                else:
                    circle(c, x, y, 140, "#ece6da"); c.save(); pth = skia.Path(); pth.addCircle(x, y, 140); c.clipPath(pth, doAntiAlias=True)
                    c.drawCircle(x - 150, y + 30, 170, paint("#2a1e16")); c.restore()
                orbit_ring(c, x, y, 200, 60, MINT, t)
                th = t * 1.5 + k; circle(c, x + math.cos(th) * 200, y + math.sin(th) * 60, 9, MINT)
                T(c, lab, x, 760, 40, ts, MINT if lab == "OUR MOON" else "#ffffff", 1, maxw=420)
        C(c, "BIG MOONS · FAR FROM THEIR PLANETS", 960, 900, vis(t, 1.6), ts, size=28)
    def pOurs(c, ts):
        earth(c, 230, 560, 120, rot=160)
        mx, my = 1100, 540
        orbit_ring(c, mx, my, 560, 250, MINT, t)
        moon_d(c, mx, my, 200, "moon", glow=0.8)
        th = t * 0.9; sx, sy = mx + math.cos(th) * 560, my + math.sin(th) * 250
        if math.sin(th) < 0 or True: moon_d(c, sx, sy, 14, "far", glow=0.8)
        C(c, "SUBMOON: TENS OF KM WIDE", 1100, 900, vis(t, 0.5), ts, size=30, dot=MINT)
        C(c, "WIDE ORBIT · ON PAPER", 1100, 1000, vis(t, L * 0.5), ts, size=28)
    def pLumpy(c, ts):
        mascon_moon(c, 560, 560, 280, t)
        q = prog(t, 0.6, max(1.5, S.le(1) - 0.6 if S.n() > 1 else L - 0.6))
        th = t * 2.4; r = lerp(380, 300, q ** 1.5)
        sx, sy = 560 + math.cos(th) * r, 560 + math.sin(th) * r * 0.35
        if q < 1:
            line(c, sx - 60, sy, sx + 60, sy, "#7fb0ff", 8); rrect(c, sx - 24, sy - 18, 48, 36, 6, "#e6e2d0"); glint(c, sx + 20, sy - 14, 5, 0.8)
        else: flash(c, 560 + math.cos(th) * 280 * 0.8, 560 + math.sin(th) * 280 * 0.3, 40, 0.5, t)
        C(c, "APOLLO 16 SUBSATELLITE · 1972", 1400, 300, vis(t, 0.3), ts, size=26, dot=MINT)
        C(c, "MASCONS: LUMPY GRAVITY", 1400, 440, vis(t, S.lt(0, 0.5)), ts, size=28, dot=RED)
        C(c, "24 APRIL → 29 MAY", 1400, 580, vis(t, S.lt(0, 0.8)), ts, size=30, bg=YEL, fg=INK, a=1)
    fn = dict(intro=pIntro, none=pNone, tides=pTides, hosts=pHosts, ours=pOurs, lumpy=pLumpy)[mode]
    run_panels(c, W, H, t, S, [(0, fn)], look="sub", seed=83)

# ===================================================================== SHORT: Uranus tilt (dark teal + aqua)
def tipped_earth(c, x, y, R, tilt=98, a=1.0, light_ang=180, night=0.85):
    """Earth with its axis drawn at `tilt` degrees from vertical; light from screen direction light_ang (deg)."""
    c.save(); c.translate(x, y); c.rotate(tilt - 23)
    earth(c, 0, 0, R, rot=150, a=a)
    c.restore()
    c.save(); pth = skia.Path(); pth.addCircle(x, y, R); c.clipPath(pth, doAntiAlias=True)
    dx, dy = math.cos(math.radians(light_ang)), math.sin(math.radians(light_ang))
    c.drawCircle(x, y, R + 1, paint(shader=lin(x + dx * R, y + dy * R, x - dx * R, y - dy * R, [(0, "#000000", 0), (0.47, "#000000", 0), (0.55, "#020610", night * a), (1, "#020610", night * a)])))
    c.restore()
    c.save(); c.translate(x, y); c.rotate(tilt)
    line(c, 0, -R * 1.35, 0, R * 1.35, "#ffffff", max(2, R * 0.025), 0.8 * a, dash=([R * 0.08, R * 0.06], 0))
    circle(c, 0, -R * 1.35, max(4, R * 0.045), YEL, a)
    c.restore()

def mn7_uranus(c, W, H, t, S):
    mode = S.opts.get("mode", "intro")
    L = S.le(0)
    def pIntro(c, ts):
        tipped_earth(c, 620, 540, 260, tilt=lerp(23, 98, ease(prog(t, 0.2, 1.4))), light_ang=180, night=0.7)
        uranus_d(c, 1420, 540, 200, t)
        T(c, "EARTH", 620, 920, 40, ts, "#ffffff", 1, maxw=400); T(c, "URANUS", 1420, 920, 40, ts, AQUA, 1, maxw=400)
    def pSky(c, ts):
        rng = random.Random(12)
        for _ in range(140): circle(c, rng.uniform(0, VW), rng.uniform(0, VH), rng.uniform(1, 2.6), "#ffffff", rng.uniform(0.2, 0.7))
        hy = [(520, 640), (600, 580), (680, 520), (600, 700), (680, 760)]  # Hyades V (schematic)
        for x, y in hy: circle(c, x, y, 7, "#fff0d8")
        circle(c, 520, 640, 12, "#ffb070"); T(c, "TAURUS", 600, 860, 30, ts, "#bfe9e6", 1, w=700, fam="Inter", maxw=400)
        for k in range(7): circle(c, 1330 + 40 * math.cos(k * 0.9) * (1 + k % 2 * 0.4), 300 + 28 * math.sin(k * 1.3), 6, "#d8ecff")
        T(c, "PLEIADES", 1340, 220, 28, ts, "#bfe9e6", 1, w=700, fam="Inter", maxw=400)
        ux, uy = 1050, 470
        circle(c, ux, uy, 9, AQUA); circle(c, ux, uy, 26, AQUA, 0.25 + 0.15 * math.sin(t * 3))
        p = vis(t, 0.8)
        c.drawCircle(ux, uy, 170, paint(AQUA, p * 0.8, stroke=5)); c.drawCircle(ux, uy + 0, 170, paint(AQUA, p * 0.08))
        T(c, "URANUS", ux, uy + 230, 40, ts, AQUA, p, maxw=400)
        C(c, "MAG ≈5.6 · BINOCULARS", 1500, 900, vis(t, L * 0.5), ts, size=30, bg=YEL, fg=INK, a=1)
        C(c, "STAR POSITIONS: SCHEMATIC", 1700, 1020, 1, ts, size=20, bg=PAL_UR["chip"])
    def pTilt(c, ts):
        line(c, 200, 560, 1720, 560, "#ffffff", 2, 0.3, dash=([12, 10], 0))
        T(c, "ORBIT PLANE", 920, 530, 24, ts, "#bfe9e6", 1, w=700, fam="Inter", maxw=300)
        tipped_earth(c, 520, 560, 170, tilt=23, light_ang=180, night=0.5)
        T(c, "EARTH 23°", 520, 860, 40, ts, "#ffffff", 1, maxw=500)
        ang = lerp(0, 98, ease(prog(t, 0.3, 1.5)))
        uranus_d(c, 1320, 560, 200, t, axis_deg=ang)
        p = skia.Path(); p.addArc(skia.Rect.MakeLTRB(1320 - 330, 560 - 330, 1320 + 330, 560 + 330), -90, ang); c.drawPath(p, paint(YEL, 0.9, stroke=6))
        T(c, f"{int(round(ang))}°", 1700, 300, 70, ts, YEL, 1, maxw=300)
        C(c, "A GIANT COLLISION? (NASA)", 1320, 960, vis(t, L * 0.5), ts, size=30, dot=AQUA)
    def pSeasons(c, ts):
        sx, sy = 960, 540
        sun(c, sx, sy, 60, t)
        orbit_ring(c, sx, sy, 640, 260, AQUA, t)
        for k, (an, lab) in enumerate([(180, "POLE TO SUN"), (90, ""), (0, "OTHER POLE"), (270, "")]):
            x = sx + math.cos(math.radians(an)) * 640; y = sy + math.sin(math.radians(an)) * 260
            uranus_d(c, x, y, 60, t, axis_deg=98, rings=False, a=vis(t, 0.2 + k * 0.3))
            # night side shading away from the Sun
            dx, dy = x - sx, y - sy; d = math.hypot(dx, dy)
            c.save(); pth = skia.Path(); pth.addCircle(x, y, 60); c.clipPath(pth, doAntiAlias=True)
            c.drawCircle(x, y, 61, paint(shader=lin(x - dx / d * 60, y - dy / d * 60, x + dx / d * 60, y + dy / d * 60, [(0, "#000000", 0), (0.5, "#000000", 0), (0.56, "#01080a", 0.8 * vis(t, 0.2 + k * 0.3)), (1, "#01080a", 0.8 * vis(t, 0.2 + k * 0.3))])))
            c.restore()
        C(c, "1 ORBIT = 84 EARTH YEARS", 960, 120, vis(t, 0.4), ts, size=32, dot=AQUA)
        C(c, "21-YEAR WINTER NIGHT", 960, 960, vis(t, L * 0.5), ts, size=34, bg=YEL, fg=INK, a=1)
    def pEarth(c, ts):
        sun(c, 160, 540, 90, t)
        for k in range(5): line(c, 280, 380 + k * 80, 560, 380 + k * 80, SUNY, 4, 0.35)
        tipped_earth(c, 1000, 540, 300, tilt=-82, light_ang=180, night=0.85)
        C(c, "NORTH: NONSTOP DAY", 700, 150, vis(t, L * 0.3), ts, size=32, bg=YEL, fg=INK, a=1)
        C(c, "SOUTH: MONTHS OF NIGHT", 1500, 930, vis(t, L * 0.6), ts, size=32, dot="#6f8fff")
        C(c, "ONE SOLSTICE · SCHEMATIC", 300, 1010, 1, ts, size=20, bg=PAL_UR["chip"])
    def pOcean(c, ts):
        tipped_earth(c, 620, 540, 280, tilt=90, light_ang=180, night=0.55)
        for k, (x, lab) in enumerate([(1250, "POLE"), (1550, "EQUATOR")]):
            thermometer(c, x, 330, 420, 14 + 3 * k, tmax=40, tmin=-40, a=vis(t, 0.4 + k * 0.4), label=False, size=1.2)
            T(c, lab, x, 830, 32, ts, AQUA, vis(t, 0.4 + k * 0.4), maxw=300)
        C(c, "ONE MODEL (MIT, 2014): MILD", 1400, 930, vis(t, L * 0.4), ts, size=30, bg=YEL, fg=INK, a=1)
        C(c, "IF THE OCEAN IS DEEP ENOUGH", 1400, 1030, vis(t, L * 0.6), ts, size=24)
    fn = dict(intro=pIntro, sky=pSky, tilt=pTilt, seasons=pSeasons, earth=pEarth, ocean=pOcean)[mode]
    run_panels(c, W, H, t, S, [(0, fn)], look="ura", seed=87)

SCENES = {k: v for k, v in globals().items() if k.startswith("mn7_") and callable(v)}
