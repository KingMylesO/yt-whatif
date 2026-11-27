"""Batch 07 scenes: What If Every Volcano Erupted at Once? (+ teaser, Iwo Jima and deep-sea nodule Shorts).

Look: "ash and magma". Warm ash-grey smoky backgrounds (no starfield) with drifting ash flakes and a magma glow rising
from below; magma orange/yellow for anything hot, a cold steel-blue tint for the volcanic-winter chapter.
Motif: the glowing Ring of Fire, a dark globe centred on the Pacific with ~1,570 real volcano positions
(Smithsonian GVP Holocene list, via plotly/datasets volcano_db.csv) lighting up around the rim.
short_b7_nodule has its own abyss look (inky blue, marine snow, cyan bioluminescent accents).
Every scene draws on a virtual 1920x1080 stage (Stage). In Shorts the stage is scaled into the 0.255H..0.58H band and
text sizes are multiplied by ts=1.75. Panels are time-ordered; Shorts pick panels by name with opts["seq"].
"""
import json, os, subprocess
import numpy as np
from common2 import *
import scenes_b3_kit as kit

VW, VH = 1920, 1080
MAGMA = "#ff7a1f"; LAVA = "#ffb02e"; HOTW = "#fff1c8"; EMBER = "#ff4a1a"
ASH = "#b9b0a8"; ASH_D = "#5a524c"; ROCKC = "#3b3430"; COLD = "#9cc8ff"; RED = "#ff5b5b"; GREEN = "#7dffb0"
YEL = ACCENT; CHIPBG = "#2a1d16"; SEA = "#121a22"; LANDC = "#4a423c"
ABY = "#5ff2ff"; ABY_CHIP = "#06263a"
PAL = dict(accent=MAGMA, chip="#3a2216", title2=ACCENT)

# ------------------------------------------------------------------ volcano positions (real)
VDATA = "/home/claude/data/vo7/volcanoes.json"
def _load_volcanoes():
    if not os.path.exists(VDATA):
        os.makedirs(os.path.dirname(VDATA), exist_ok=True)
        csvp = VDATA.replace(".json", ".csv")
        subprocess.run(["curl", "-sS", "-m", "60", "-o", csvp, "https://raw.githubusercontent.com/plotly/datasets/master/volcano_db.csv"], check=True)
        import csv
        rows = list(csv.DictReader(open(csvp, encoding="latin-1")))
        json.dump([[round(float(r["Longitude"]), 2), round(float(r["Latitude"]), 2)] for r in rows if r["Latitude"] and r["Longitude"]], open(VDATA, "w"))
    a = np.array(json.load(open(VDATA)), np.float64)
    return a[:, 0], a[:, 1]
VLON, VLAT = _load_volcanoes()
_rng = np.random.default_rng(7)
VDEL = _rng.random(len(VLON))  # ignition order
def _ring_mask():
    lo, la = VLON, VLAT
    asia = (lo >= 95) & (la > -50) & (la < 65)
    amer = (lo <= -60) & (lo >= -180) & ~((la > 9) & (lo > -72)) & (la > -57)
    haw = (lo > -162) & (lo < -150) & (la > 15) & (la < 25)
    gal = (lo > -93) & (lo < -88) & (la > -3) & (la < 2)
    ice = (lo > -30) & (lo < -10)
    return (asia | amer) & ~haw & ~gal & ~ice & (la > -60)
RING = _ring_mask()
IWO = (141.32, 24.78)

# ------------------------------------------------------------------ stage + text helpers (pattern from batch 06)
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
    if ts > 1:  # keep chips inside the 1920 stage when scaled up
        def width(sz):
            f = sz * 1.15; return tw(s, f, 700, "Inter") + 2 * f * 0.62 + (f * 0.9 if kw.get("dot") else 0)
        sz = size * ts
        while width(sz) > 1840 and sz > 12: sz *= 0.95
        wd = width(sz); al = kw.get("align", "c")
        left = x - wd / 2 if al == "c" else (x if al == "l" else x - wd)
        x += max(0, 30 - left) - max(0, left + wd - 1890)
        chip(c, s, x, y, p, sz, **kw); return
    chip(c, s, x, y, p, size * ts, **kw)

def T(c, s, x, y, size, ts, colr="#ffffff", a=1.0, w=900, maxw=1800, **kw):
    if a <= 0: return
    fam = kw.pop("fam", "Inter Display"); al = kw.get("align", "c")
    if ts > 1 and al == "c": maxw = min(max(maxw, 600) * 1.2, 2 * min(x, VW - x) - 40)
    sz = fit(s, maxw, size * ts, w, fam)
    text(c, s, x, y, sz, colr, a, w=w, fam=fam, shadow=kw.pop("shadow", 10), stroke=kw.pop("stroke", 5 * ts), stroke_col=kw.pop("stroke_col", "#120c09"), **kw)

def stage_bg(c, top, bot, a=1.0):
    c.drawRect(skia.Rect.MakeXYWH(0, 0, VW, VH), paint(shader=lin(0, 0, 0, VH, [(0, top, a), (1, bot, a)])))

_BG = {}
def bg_img(W, H, look="ash"):
    k = (W, H, look)
    if k not in _BG:
        surf = skia.Surface(W, H); cc = surf.getCanvas(); M = max(W, H)
        if look == "ash":
            fill_bg(cc, W, H, "#141110", "#2b231f")
            cc.drawPaint(paint(shader=rad(W * 0.5, H * 1.15, M * 0.75, [(0, "#ff6a1a", 0.32), (0.4, "#8a2a0a", 0.12), (1, "#000000", 0)])))
            cc.drawPaint(paint(shader=rad(W * 0.15, H * 0.1, M * 0.6, [(0, "#6a625a", 0.22), (1, "#000000", 0)])))
        elif look == "cold":
            fill_bg(cc, W, H, "#1a1f26", "#353b43")
            cc.drawPaint(paint(shader=rad(W * 0.7, H * 0.15, M * 0.7, [(0, "#d8e4f0", 0.18), (1, "#000000", 0)])))
        else:  # abyss
            fill_bg(cc, W, H, "#010812", "#03182a")
            cc.drawPaint(paint(shader=rad(W * 0.5, H * 0.2, M * 0.7, [(0, "#0d4a6a", 0.28), (1, "#000000", 0)])))
        cc.drawPaint(paint(shader=rad(W / 2, H / 2, M * 0.75, [(0.55, "#000000", 0), (1, "#000000", 0.45)])))
        _BG[k] = surf.makeImageSnapshot()
    return _BG[k]

_FL = np.random.default_rng(11).random((90, 5))
def flakes(c, W, H, t, a=1.0, colr="#cfc6bc", down=1.0):
    """drifting ash flakes (or marine snow)."""
    for x0, y0, s, sp, ph in _FL:
        y = (y0 * H + t * (18 + 40 * sp) * down) % (H + 20) - 10
        x = (x0 * W + math.sin(t * 0.6 + ph * 6) * 20 + t * 9) % W
        r = (1.2 + 2.6 * s) * max(W, H) / 1920
        circle(c, x, y, r, colr, a * (0.12 + 0.25 * s))

def bg_v(c, W, H, t, S=None, look="ash"):
    c.drawImage(bg_img(W, H, look), 0, 0)
    flakes(c, W, H, t, 0.9 if look != "aby" else 0.7, colr="#e8f4ff" if look == "aby" else "#cfc6bc")

def run_panels(c, W, H, t, S, items, look="ash"):
    """items: [(t_on, fn(c, ts)), ...] in time order. Each later panel covers the previous one."""
    bg_v(c, W, H, t, S, look)
    for i, (t0, fn) in enumerate(items):
        t1 = items[i + 1][0] if i + 1 < len(items) else None
        if t1 is not None and t >= t1 + 0.5: continue
        a = phase(t, t0 if i > 0 else None, t1)
        if a <= 0.003: continue
        with Layer(c, a) as on:
            if not on: continue
            if i > 0 and t < t0 + 0.55: bg_v(c, W, H, t, S, look)
            if S.P: c.clipRect(skia.Rect.MakeLTRB(0, 0.215 * H, W, 0.59 * H))
            with Stage(c, S) as ts:
                fn(c, ts)
    kit.hook(c, W, H, t, S)

def go(c, W, H, t, S, P, default, look="ash"):
    """P: {name: fn(c, ts, lt, d)}; default: [(t0, name)]. Shorts: opts['seq'] = [names] share the scene evenly."""
    seq = S.opts.get("seq")
    sched = [(S.dur * i / len(seq) if i else 0.0, nm) for i, nm in enumerate(seq)] if seq else default
    items = []
    for i, (t0, nm) in enumerate(sched):
        t1 = sched[i + 1][0] if i + 1 < len(sched) else S.dur
        items.append((t0, (lambda f, a, b: (lambda c, ts: f(c, ts, t - a, b - a)))(P[nm], t0, t1)))
    run_panels(c, W, H, t, S, items, look)

def lsched(S, names, lines=None, lead=0.3):
    """one panel per narration line (or per given line index)."""
    lines = lines if lines is not None else list(range(len(names)))
    return [(0.0 if k == 0 else max(0.0, S.ls(li) - lead), nm) for k, (nm, li) in enumerate(zip(names, lines))]

# ------------------------------------------------------------------ props: volcano cone, plume, lava
def plume(c, x, y, h, t, a=1.0, seed=1, colr=ASH, dark="#4a423c", w=1.0):
    rng = random.Random(seed)
    for i in range(22):
        ph = rng.random(); q = (ph + t * 0.12) % 1
        r = (h * 0.08 + q * h * 0.22) * w
        xx = x + math.sin(q * 5 + i) * h * 0.08 * q * w + q * h * 0.1
        circle(c, xx, y - q * h, r, mix(colr, dark, rng.random() * 0.6), a * 0.85 * (1 - q ** 3))

def cone(c, x, y, w, h, t, erupt=1.0, a=1.0, seed=1, plume_h=None, lava=True):
    """stratovolcano silhouette standing on (x, y), crater at top, glowing vent and ash plume when erupt > 0."""
    if a <= 0: return
    top = y - h; cw = w * 0.11
    pth = poly([(x - w / 2, y), (x - cw, top + h * 0.02), (x + cw, top + h * 0.02), (x + w / 2, y)])
    c.drawPath(pth, paint(shader=lin(x - w / 2, top, x + w / 2, y, [(0, "#6b5f56", 1), (0.5, "#3e3530", 1), (1, "#201a17", 1)]), a=a))
    if erupt > 0:
        if plume_h is None: plume_h = h * 1.4
        circle(c, x, top, cw * 2.2, LAVA, 0.5 * erupt * a, blur=cw * 1.2)
        plume(c, x, top - cw * 0.4, plume_h * erupt, t, a * erupt, seed=seed, w=w / 600)
        if lava:
            for k, (dx, ln) in enumerate(((-0.6, 0.55), (0.35, 0.7), (0.05, 0.4))):
                p = skia.Path(); p.moveTo(x + dx * cw, top + h * 0.02)
                ex = x + dx * w * 0.38; ey = top + h * ln * erupt
                p.quadTo(x + dx * w * 0.2, top + h * ln * 0.5, ex, ey)
                c.drawPath(p, paint(MAGMA, a * 0.95, stroke=max(2, w * 0.018)))
                c.drawPath(p, paint(HOTW, a * 0.6, stroke=max(1, w * 0.006)))
        oval(c, x, top + h * 0.02, cw * 1.1, cw * 0.3, HOTW, a * erupt)

def glow_pts(c, pts, size, colr, a=1.0, halo=2.6):
    if len(pts) == 0 or a <= 0: return
    sp = [skia.Point(float(x), float(y)) for x, y in pts]
    p = paint(colr, 0.25 * a, stroke=size * halo); c.drawPoints(skia.Canvas.PointMode.kPoints_PointMode, sp, p)
    p = paint(colr, a, stroke=size); c.drawPoints(skia.Canvas.PointMode.kPoints_PointMode, sp, p)
    p = paint(HOTW, 0.8 * a, stroke=size * 0.4); c.drawPoints(skia.Canvas.PointMode.kPoints_PointMode, sp, p)

# ------------------------------------------------------------------ dark globe with volcano pins (the motif)
_GL = {}
def globe_im(R, rot, tilt=12, look="ash"):
    R = max(4, int(R) // 4 * 4); rq = round(rot * 2) / 2; k = (R, rq, tilt, look)
    if k not in _GL:
        if len(_GL) > 40: _GL.clear()
        arr = geo.globe_img(R, rq, tilt, light=(-0.5, 0.45, 0.75), ambient=0.3).astype(np.float32)
        rgb_ = arr[:, :, :3]; al = arr[:, :, 3:4] / 255.0
        sh = rgb_.max(axis=2, keepdims=True) / np.maximum(al * 255.0, 1)  # shading 0..1 (un-premultiplied)
        land = (rgb_[:, :, 1:2] > rgb_[:, :, 2:3] * 0.95) | (rgb_.min(axis=2, keepdims=True) > 150 * al)
        landc = np.array((118, 104, 92) if look == "ash" else (150, 160, 172), np.float32)
        seac = np.array((26, 32, 40), np.float32)
        out = np.where(land, landc, seac) * np.clip(sh * 1.25, 0, 1.2) * al
        arr = np.dstack([np.clip(out, 0, 255), arr[:, :, 3:4]]).astype(np.uint8)
        _GL[k] = skia.Image.fromarray(arr, colorType=skia.kRGBA_8888_ColorType, alphaType=skia.kPremul_AlphaType)
    return _GL[k], R

def globe_xy_np(lon, lat, cx, cy, R, rot, tilt=12):
    la = np.radians(lat); lo = np.radians(lon - rot); tr = math.radians(tilt)
    nxp = np.cos(la) * np.sin(lo); y2 = np.sin(la); z2 = np.cos(la) * np.cos(lo)
    ny = y2 * math.cos(tr) - z2 * math.sin(tr); nz = y2 * math.sin(tr) + z2 * math.cos(tr)
    return cx + nxp * R, cy - ny * R, nz

def vglobe(c, x, y, R, rot, t, ign=1.0, ring_only=0.0, a=1.0, tilt=12, look="ash", rim=1.0, pin=None):
    """dark globe; volcano pins ignite in random order with ign 0..1; ring_only dims non-Ring pins."""
    img, Rq = globe_im(R, rot, tilt, look)
    circle(c, x, y, Rq * 1.1, MAGMA, 0.22 * rim * a * clamp(ign * 2), blur=Rq * 0.12)
    p = skia.Paint(); p.setAlphaf(clamp(a))
    c.drawImageRect(img, skia.Rect.MakeXYWH(x - Rq, y - Rq, 2 * Rq, 2 * Rq), skia.SamplingOptions(skia.FilterMode.kLinear), p)
    if ign > 0:
        px, py, nz = globe_xy_np(VLON, VLAT, x, y, Rq, rot, tilt)
        on = (nz > 0.02) & (VDEL < ign)
        fl = 0.85 + 0.15 * math.sin(t * 7)
        sz = max(3.0, Rq * 0.016)
        ringm = on & RING; other = on & ~RING
        glow_pts(c, np.stack([px[other], py[other]], 1), sz, MAGMA, a * fl * (1 - 0.7 * ring_only))
        glow_pts(c, np.stack([px[ringm], py[ringm]], 1), sz * (1 + 0.35 * ring_only), LAVA if ring_only > 0 else MAGMA, a * fl)
    if pin:
        lon, lat, lab, pa = pin
        gx, gy, vis_ = geo.globe_xy(lon, lat, x, y, Rq, rot, tilt)
        if vis_ and pa > 0:
            circle(c, gx, gy, 12 + 6 * math.sin(t * 5), YEL, pa, stroke=4)
            return gx, gy
    return None

# ------------------------------------------------------------------ flat maps
WORLD = (-180, -58, 180, 78)
WRECT = geo.map_rect(WORLD, 960, 560, width=1800)
def wxy(lon, lat, rect=WRECT, bbox=WORLD): return geo.lonlat_xy(lon, lat, bbox, rect)

def world(c, a=1.0, land=LANDC, sea=SEA):
    with Layer(c, a):
        geo.draw_map(c, WORLD, WRECT, land=land, sea=sea, outline="#000000", outline_w=1.2)
        rrect(c, *WRECT, 10, "#ffffff", 0.18, stroke=2)

def world_pins(c, t, ign=1.0, mask=None, colr=MAGMA, size=5.5, a=1.0):
    x0, y0, w, h = WRECT
    px = x0 + (VLON + 180) / 360 * w; py = y0 + (WORLD[3] - VLAT) / (WORLD[3] - WORLD[1]) * h
    m = (VDEL < ign) & (VLAT > WORLD[1])
    if mask is not None: m &= mask
    glow_pts(c, np.stack([px[m], py[m]], 1), size, colr, a * (0.85 + 0.15 * math.sin(t * 6)))

# ------------------------------------------------------------------ title / cards / end
def motif_vo(c, W, H, t, S, cx, cy, s):
    u = S.u * s * (1.1 if S.P else 1.0)
    R = 230 * u
    vglobe(c, cx, cy, R, -178 + t * 2.5, t, ign=clamp(0.25 + t * 0.4), ring_only=0.8)
    c.drawOval(skia.Rect.MakeLTRB(cx - R * 1.32, cy - R * 0.36, cx + R * 1.32, cy + R * 0.36), paint(LAVA, 0.35, stroke=2.5 * u, dash=([14 * u, 10 * u], -t * 20)))

def bg_title(c, W, H, t, S): bg_v(c, W, H, t, S)
def vo7_title(c, W, H, t, S): kit.title(c, W, H, t, S, bg_title, motif_vo, PAL)
def vo7_card(c, W, H, t, S):
    look = "cold" if S.opts.get("text") in ("ONE YEAR LATER",) else "ash"
    def cbg(c, W, H, t, S):
        bg_v(c, W, H, t, S, look)
        with Layer(c, 0.35):
            motif_vo(c, W, H, t, S, W / 2, H / 2, 1.2 if not S.P else 0.9)
    kit.card(c, W, H, t, S, cbg, PAL)
def vo7_end(c, W, H, t, S): kit.end(c, W, H, t, S, bg_title, motif_vo, PAL)
def vo7_endshort(c, W, H, t, S):
    look = "aby" if S.opts.get("look") == "nod" else "ash"
    kit.end_short(c, W, H, t, S, lambda c, W, H, t, S: bg_v(c, W, H, t, S, look), motif_vo, PAL)

# ------------------------------------------------------------------ Iwo Jima (schematic outline, lon/lat)
IWO_POLY = [(141.285, 24.748), (141.292, 24.743), (141.300, 24.747), (141.306, 24.754), (141.320, 24.762), (141.336, 24.771),
            (141.350, 24.786), (141.353, 24.800), (141.346, 24.812), (141.331, 24.816), (141.316, 24.809), (141.305, 24.797),
            (141.298, 24.780), (141.292, 24.766), (141.287, 24.757)]
NEW_LAND = [(141.306, 24.754), (141.309, 24.750), (141.316, 24.748), (141.324, 24.752), (141.327, 24.758), (141.320, 24.762)]
VENT = (141.318, 24.746)

def ixy(lon, lat, cx=960, cy=560, k=9500):
    return cx + (lon - 141.32) * k * math.cos(math.radians(24.78)), cy - (lat - 24.78) * k

def island(c, t, cx=960, cy=560, k=9500, grow=0.0, erupt=0.0, pumice=0.0, glow=0.0, erode=0.0, a=1.0, label=True, ts=1.0, sat=False):
    P = lambda pts: poly([tuple(q) for q in geo._smooth([ixy(lo, la, cx, cy, k) for lo, la in pts], 3)])
    if sat:  # satellite-style ocean
        c.drawRect(skia.Rect.MakeXYWH(cx - 900, cy - 500, 1800, 1000), paint(shader=lin(0, cy - 500, 0, cy + 500, [(0, "#0d2a44", a), (1, "#0a2036", a)])))
    if pumice > 0:  # floating pumice streak toward the southeast
        vx, vy = ixy(*VENT, cx, cy, k); rng = random.Random(4)
        for i in range(160):
            q = rng.random(); d = q * 620 * pumice
            circle(c, vx + d * 0.85 + rng.gauss(0, 18 + q * 30), vy + d * 0.45 + rng.gauss(0, 10 + q * 22), rng.uniform(1.5, 4), "#d9d0bd", a * 0.55 * (1 - q * 0.6))
    # discoloured water around the vent
    if erupt > 0:
        vx, vy = ixy(*VENT, cx, cy, k)
        circle(c, vx, vy, 120 + 30 * math.sin(t), "#6fa58a", 0.35 * erupt * a, blur=40)
    c.drawPath(P(IWO_POLY), paint("#e7dcc4", a, stroke=10))  # beach rim
    c.drawPath(P(IWO_POLY), paint(shader=lin(cx - 300, cy - 300, cx + 300, cy + 300, [(0, "#5d6b48", 1), (1, "#46503a", 1)]), a=a))
    sx, sy = ixy(141.289, 24.751, cx, cy, k)  # Suribachi crater (SW tip)
    circle(c, sx, sy, k * 0.0035, "#6b5d4c", a); circle(c, sx, sy, k * 0.0016, "#3a3128", a)
    if grow > 0:
        pts = [ixy(lo, la, cx, cy, k) for lo, la in NEW_LAND]
        ctr = ixy(141.313, 24.756, cx, cy, k)
        g = eout(grow) * (1 - 0.6 * erode)
        pts = [(ctr[0] + (x - ctr[0]) * g, ctr[1] + (y - ctr[1]) * g) for x, y in pts]
        c.drawPath(poly(pts), paint("#2c2724", a))
        c.drawPath(poly(pts), paint(MAGMA, a * (0.35 + 0.5 * glow), stroke=4))
        if glow > 0: c.drawPath(poly(pts), paint(MAGMA, 0.55 * glow * a, blur=14))
    if erupt > 0:
        vx, vy = ixy(*VENT, cx, cy, k)
        circle(c, vx, vy, 16, HOTW, erupt * a)
        plume(c, vx + 30, vy - 10, 240 * erupt, t, a * erupt * 0.85, seed=3, colr="#e8e2da", dark="#7a706a", w=0.75)
    if label:
        C(c, "IWO JIMA (IŌ TŌ)", cx - 330 * k / 9500, cy - 260 * k / 9500, a, ts, size=28, dot=GREEN)

# ================================================================== LONG-FORM SCENES
def vo7_hook(c, W, H, t, S):
    def p_iwo(c, ts, lt, d):
        island(c, t, 960, 600 if not S.P else 560, 9500, grow=prog(lt, d * 0.35, d * 0.4), erupt=vis(lt, 0.3), pumice=prog(lt, 1, d * 0.6), glow=1.0, ts=ts)
        C(c, "27 OCT 2026", 260, 130, vis(lt, 0.5), ts, size=40, bg=YEL, fg="#1a120c", a=1)
        C(c, "UNDERWATER ERUPTION", 260, 230, vis(lt, 1.2), ts, size=32, dot=MAGMA, align="l") if not S.P else None
        C(c, "+≈50 HECTARES OF NEW LAND", 1420, 930, vis(lt, d * 0.62), ts, size=36, dot=MAGMA)
        C(c, "≈ 90 FOOTBALL FIELDS", 1420, 1020, vis(lt, d * 0.78), ts, size=30)
    def p_all(c, ts, lt, d):
        vglobe(c, 960, 560, 420, -178 + t * 3, t, ign=prog(lt, 0.4, d * 0.55))
        T(c, "EVERY VOLCANO?", 960, 1010, 72, ts, LAVA, vis(lt, d * 0.45))
    go(c, W, H, t, S, dict(iwo=p_iwo, all=p_all), [(0, "iwo"), (S.ls(2) - 0.2, "all")] if S.n() >= 3 else [(0, "iwo")])

def seismo(c, x0, y0, w, h, t, lt, spike_at, a=1.0):
    pts = []; rng = random.Random(2)
    for i in range(240):
        f = i / 239; tt = f * 10
        amp = 0.06 + (0.9 * math.exp(-max(0, tt - spike_at) * 0.6) if tt > spike_at else 0)
        pts.append((x0 + f * w, y0 + math.sin(i * 1.7 + t * 4) * h * amp * rng.uniform(0.4, 1)))
    vis_n = max(2, int(len(pts) * clamp(lt / 3.5)))
    c.drawPath(poly(pts[:vis_n], close=False), paint(MAGMA, a, stroke=4))

def vo7_news(c, W, H, t, S):
    def p_map(c, ts, lt, d):
        bb = (127, 19, 149, 40); rr = geo.map_rect(bb, 960, 560, height=900)
        geo.draw_map(c, bb, rr, land=LANDC, sea=SEA, outline="#000000", outline_w=1.2)
        tx, ty = geo.lonlat_xy(139.69, 35.69, bb, rr); ix, iy = geo.lonlat_xy(*IWO, bb, rr)
        circle(c, tx, ty, 10, "#ffffff"); C(c, "TOKYO", tx + 110, ty - 10, vis(lt, 0.3), ts, size=28)
        q = eout(prog(lt, 0.8, 1.4))
        line(c, tx, ty, lerp(tx, ix, q), lerp(ty, iy, q), "#ffffff", 3, 0.8, dash=([14, 10], 0))
        if q > 0.99:
            circle(c, ix, iy, 16 + 5 * math.sin(t * 5), MAGMA, 1, stroke=5); circle(c, ix, iy, 6, LAVA)
            C(c, "IWO JIMA", ix - 170, iy, 1, ts, size=30, dot=MAGMA)
        C(c, "≈1,200 KM SOUTH OF TOKYO", (tx + ix) / 2 + 300, (ty + iy) / 2, vis(lt, 2.2), ts, size=30)
        C(c, "THE ISLAND = TOP OF AN ACTIVE VOLCANO", 960, 1010, vis(lt, d * 0.6), ts, size=32, dot=MAGMA)
    def p_quake(c, ts, lt, d):
        rrect(c, 160, 230, 1600, 420, 20, "#0d0a09", 0.8); rrect(c, 160, 230, 1600, 420, 20, "#ffffff", 0.2, stroke=2)
        seismo(c, 200, 440, 1520, 170, t, lt, 5.5)
        T(c, "SEISMIC ACTIVITY (ILLUSTRATIVE)", 960, 690, 26, ts, "#bdb3aa", 1, w=700, fam="Inter")
        C(c, "LATE OCTOBER: SHARP JUMP", 600, 820, vis(lt, 1.5), ts, size=32, dot=MAGMA)
        C(c, "27 OCT: JMA REPORTS FIRST PHOTOS", 1300, 920, vis(lt, d * 0.5), ts, size=32, bg=YEL, fg="#1a120c", a=1)
    def p_sat(c, ts, lt, d):
        for i, (lab, xx) in enumerate([("26 OCT · BEFORE", 500), ("11 NOV · AFTER", 1420)]):
            c.save(); c.clipRect(skia.Rect.MakeXYWH(xx - 420, 160, 840, 760))
            island(c, t, xx, 560, 6200, grow=1.0 if i else 0, erupt=0.5 if i else 0, pumice=0.8 * i, glow=vis(lt, d * 0.45) if i else 0, label=False, sat=True)
            c.restore()
            rrect(c, xx - 420, 160, 840, 760, 14, "#ffffff", 0.5, stroke=3)
            C(c, lab, xx, 205, 1 if i == 0 else vis(lt, d * 0.25), ts, size=30, bg=YEL if i else CHIPBG, fg="#1a120c" if i else "#ffffff", a=1)
        C(c, "HEAT IN INFRARED", 1580, 640, vis(lt, d * 0.45), ts, size=28, dot=MAGMA)
        C(c, "FLOATING PUMICE", 1640, 830, vis(lt, d * 0.7), ts, size=28, dot="#d9d0bd")
        T(c, "LANDSAT 9 · ILLUSTRATION, NOT THE REAL IMAGE", 960, 980, 26, ts, "#bdb3aa", 1, w=700, fam="Inter")
    def p_conf(c, ts, lt, d):
        island(c, t, 760, 540, 10500, grow=1.0, erupt=0.35, glow=0.6 + 0.4 * math.sin(t * 3), ts=ts)
        nx, ny = ixy(141.316, 24.752, 760, 540, 10500)
        line(c, nx + 30, ny + 30, 1380, 860, "#ffffff", 3, vis(lt, 0.8))
        C(c, "NEW LAND ≈ 50 HA · +1.7%", 1420, 880, vis(lt, 0.8), ts, size=34, bg=YEL, fg="#1a120c", a=1)
        C(c, "JAPAN COAST GUARD · 16 NOV", 1420, 980, vis(lt, 1.6), ts, size=28, dot=GREEN)
        bx, by = ixy(141.343, 24.772, 760, 540, 10500)
        C(c, "SOUTHEAST BEACH", bx + 200, by + 10, vis(lt, d * 0.4), ts, size=28, dot=GREEN)
        T(c, "SCHEMATIC MAP", 1780, 120, 22, ts, "#bdb3aa", 1, w=700, fam="Inter")
    def p_erode(c, ts, lt, d):
        er = 0.5 + 0.5 * math.sin(t * 0.9)
        island(c, t, 760, 540, 10500, grow=1.0, erode=er * 0.6, ts=ts)
        nx, ny = ixy(141.316, 24.750, 760, 540, 10500)
        for k in range(5):
            q = ((t * 0.35 + k / 5) % 1)
            p = skia.Path(); p.addArc(skia.Rect.MakeXYWH(nx - 80 - 260 * (1 - q), ny - 40 - 160 * (1 - q), 2 * (80 + 260 * (1 - q)), 2 * (40 + 160 * (1 - q))), 10, 150)
            c.drawPath(p, paint("#cfe8ff", 0.6 * q, stroke=4))
        C(c, "2023: NEW LAND GONE IN WEEKS", 1480, 300, vis(lt, d * 0.4), ts, size=30, dot=RED)
        C(c, "2026: HOW LONG?", 1480, 400, vis(lt, d * 0.7), ts, size=34, bg=YEL, fg="#1a120c", a=1)
    def p_wait(c, ts, lt, d):
        island(c, t, 760, 540, 10500, grow=1.0, ts=ts)
        for i, (lab, t0, colr) in enumerate([("NASA'S DANIEL SLAYBACK:", 0.3, "#ffffff"), ("“WASH AWAY WITHIN A FEW MONTHS”", 0.9, LAVA),
                                              ("“WE'LL HAVE TO WAIT AND SEE”", d * 0.6, GREEN)]):
            T(c, lab, 1460, 380 + i * 130, 44 if i else 34, ts, colr, vis(lt, t0), maxw=820)
        C(c, "STILL UNKNOWN", 1460, 820, vis(lt, 0.5), ts, size=34, dot=RED)
    names = ["map", "quake", "sat", "conf", "erode", "wait"]
    go(c, W, H, t, S, dict(map=p_map, quake=p_quake, sat=p_sat, conf=p_conf, erode=p_erode, wait=p_wait), lsched(S, names))

def vo7_rules(c, W, H, t, S):
    def p_dots(c, ts, lt, d):
        world(c); world_pins(c, t, ign=prog(lt, 0.3, d * 0.5))
        C(c, "≈1,350 POTENTIALLY ACTIVE VOLCANOES (USGS)", 960, 110, vis(lt, 0.5), ts, size=34, bg=YEL, fg="#1a120c", a=1)
        C(c, "+ VOLCANIC RIDGES ON THE OCEAN FLOOR", 960, 1000, vis(lt, d * 0.6), ts, size=30, dot=COLD)
        T(c, "DOTS: SMITHSONIAN GVP HOLOCENE LIST", 1700, 1050, 18, ts, "#9a9088", 1, w=600, fam="Inter") if not S.P else None
    def p_year(c, ts, lt, d):
        world(c, 0.8); world_pins(c, t, ign=1, colr=ASH_D, size=4, a=0.8)
        world_pins(c, t, ign=0.035 * clamp(lt / 1.0), size=9)
        C(c, "A TYPICAL YEAR: 40–50 ERUPT", 960, 110, vis(lt, 0.3), ts, size=36, dot=MAGMA)
        C(c, "LESS THAN 1 IN 10", 960, 1000, vis(lt, d * 0.5), ts, size=34, bg=YEL, fg="#1a120c", a=1)
    def p_all(c, ts, lt, d):
        world(c); world_pins(c, t, ign=prog(lt, 0.0, 1.2), size=8)
        C(c, "ALL AT ONCE", 960, 110, vis(lt, 0.2), ts, size=40, bg=YEL, fg="#1a120c", a=1)
        if not S.P:
            C(c, "SOME OOZE LAVA", 600, 1000, vis(lt, d * 0.55), ts, size=30, dot=LAVA)
            C(c, "SOME EXPLODE", 1320, 1000, vis(lt, d * 0.75), ts, size=30, dot=RED)
    def p_q(c, ts, lt, d):
        for i, x in enumerate((420, 960, 1500)):
            cone(c, x, 900, 520, 380, t, erupt=vis(lt, 0.2 + i * 0.3), seed=i + 1)
        T(c, "POSSIBLE?", 960, 200, 90, ts, LAVA, vis(lt, 0.5))
        C(c, "WE'LL COME BACK TO THAT", 960, 320, vis(lt, d * 0.5), ts, size=32)
    go(c, W, H, t, S, dict(dots=p_dots, year=p_year, all=p_all, q=p_q), lsched(S, ["dots", "year", "all", "q"]))

# mid-Atlantic + other ridges, rough centre lines (lon, lat) for an illustrative overlay
RIDGES = [[(-18, 66), (-28, 58), (-33, 52), (-29, 45), (-37, 38), (-40, 30), (-45, 22), (-46, 12), (-38, 5), (-14, -5), (-13, -15), (-14, -30), (-15, -45), (-10, -54)],
          [(-110, -55), (-115, -40), (-112, -30), (-110, -15), (-104, -5), (-104, 8)],
          [(57, 12), (60, 5), (66, -5), (68, -15), (66, -25), (60, -33), (75, -40), (100, -48), (130, -52), (160, -57), (180, -60)],
          [(-180, -60), (-150, -62), (-125, -57), (-110, -55)]]

def vo7_ring(c, W, H, t, S):
    def p_globe(c, ts, lt, d):
        vglobe(c, 960, 560, 440, -170 + t * 2, t, ign=prog(lt, 0.2, d * 0.8))
    def p_plates(c, ts, lt, d):
        world(c); world_pins(c, t, ign=1, size=6)
        C(c, "≈60% SIT ON PLATE BOUNDARIES", 960, 110, vis(lt, d * 0.45), ts, size=36, dot=MAGMA)
        C(c, "WHERE EARTH'S CRUST MEETS", 960, 1000, vis(lt, d * 0.2), ts, size=30)
    def p_ring(c, ts, lt, d):
        rp = clamp(prog(lt, 0.3, 1.2))
        vglobe(c, 960, 560, 440, -175 + t * 1.5, t, ign=1, ring_only=rp)
        C(c, "THE RING OF FIRE", 960, 70, vis(lt, 0.5), ts, size=40, bg=YEL, fg="#1a120c", a=1)
        C(c, "≈40,000 KM", 380, 900, vis(lt, d * 0.45), ts, size=34, dot=LAVA)
        C(c, "450+ VOLCANOES", 1540, 900, vis(lt, d * 0.7), ts, size=34, dot=LAVA)
    def p_names(c, ts, lt, d):
        world(c, land="#3e3833"); world_pins(c, t, ign=1, mask=~RING, colr=ASH_D, size=4)
        world_pins(c, t, ign=1, mask=RING, colr=LAVA, size=7)
        for i, (lo, la, nm, dx, dy) in enumerate([(141.32, 24.78, "IWO JIMA", -60, 70), (138.73, 35.36, "MT FUJI", -40, -60),
                                                  (-122.18, 46.2, "MT ST HELENS", 40, -60), (-70, -25, "THE ANDES", 170, 0)]):
            x, y = wxy(lo, la); p = vis(lt, 0.3 + i * d * 0.18)
            circle(c, x, y, 14, YEL, p, stroke=4)
            C(c, nm, x + dx * (1.4 if ts > 1 else 1), y + dy, p, ts, size=26)
    def p_other(c, ts, lt, d):
        world(c, land="#3e3833"); world_pins(c, t, ign=1, mask=RING, colr=ASH_D, size=4)
        world_pins(c, t, ign=1, mask=~RING, colr=LAVA, size=7)
        for i, (lo, la, nm, dx, dy) in enumerate([(-19, 64.8, "ICELAND", 40, -60), (36, -3, "EAST AFRICAN RIFT", 220, 40), (-155.5, 19.4, "HAWAII", 30, 70)]):
            x, y = wxy(lo, la); p = vis(lt, 0.3 + i * d * 0.25)
            circle(c, x, y, 16, YEL, p, stroke=4)
            C(c, nm, x + dx * (1.3 if ts > 1 else 1), y + dy, p, ts, size=26)
    def p_sea(c, ts, lt, d):
        world(c, land="#3e3833"); world_pins(c, t, ign=1, colr=ASH_D, size=4, a=0.7)
        q = prog(lt, 0.2, d * 0.6)
        for rg in RIDGES:
            pts = [wxy(lo, la) for lo, la in rg]
            n = max(2, int(len(pts) * q) + 1)
            pp = poly(pts[:n], close=False)
            c.drawPath(pp, paint(MAGMA, 0.35, stroke=14, blur=6)); c.drawPath(pp, paint(LAVA, 0.9, stroke=4, dash=([16, 8], -t * 30)))
        C(c, "MOST VOLCANOES ARE UNDERWATER", 960, 110, vis(lt, 0.3), ts, size=34, dot=COLD)
        C(c, "MID-OCEAN RIDGES (SIMPLIFIED)", 960, 1000, vis(lt, d * 0.4), ts, size=28)
    go(c, W, H, t, S, dict(globe=p_globe, plates=p_plates, ring=p_ring, names=p_names, other=p_other, sea=p_sea),
       lsched(S, ["globe", "plates", "ring", "names", "other", "sea"]))

def shards(c, cx, cy, R, t, a=1.0):
    rng = random.Random(5)
    c.save(); p = skia.Path(); p.addCircle(cx, cy, R); c.clipPath(p, doAntiAlias=True)
    circle(c, cx, cy, R, "#e9e4dc", a)
    for i in range(46):
        x = cx + rng.uniform(-1, 1) * R; y = cy + rng.uniform(-1, 1) * R; s = rng.uniform(14, 42)
        an = rng.random() * 6.28 + t * 0.05
        pts = [(x + math.cos(an + k * 2.1 + rng.uniform(-0.4, 0.4)) * s * rng.uniform(0.5, 1.2), y + math.sin(an + k * 2.1) * s * rng.uniform(0.3, 1.0)) for k in range(3)]
        kind = rng.random()
        colr = "#7a8a96" if kind < 0.4 else ("#4a403a" if kind < 0.75 else "#b8a48c")
        c.drawPath(poly(pts), paint(colr, a * 0.9)); c.drawPath(poly(pts), paint("#ffffff", a * 0.35, stroke=1.5))
    c.restore()
    circle(c, cx, cy, R, "#2a2420", a, stroke=18); circle(c, cx, cy, R + 9, "#8a8078", a, stroke=3)

def jet(c, x, y, s, a=1.0, ang=0.0, dead=0.0):
    c.save(); c.translate(x, y); c.rotate(ang)
    oval(c, 0, 0, s, s * 0.11, "#e8ecf2", a)
    c.drawPath(poly([(-s * 0.1, 0), (s * 0.25, 0), (-s * 0.25, s * 0.75), (-s * 0.42, s * 0.75)]), paint("#c9d0da", a))
    c.drawPath(poly([(-s * 0.1, 0), (s * 0.25, 0), (-s * 0.25, -s * 0.75), (-s * 0.42, -s * 0.75)]), paint("#d8dee6", a))
    c.drawPath(poly([(-s * 0.8, 0), (-s * 0.95, -s * 0.32), (-s * 1.02, -s * 0.32), (-s * 0.95, 0)]), paint("#c9d0da", a))
    for k, (ex, ey) in enumerate(((-0.02, 0.3), (-0.13, 0.55), (-0.02, -0.3), (-0.13, -0.55))):
        oval(c, s * ex, s * ey, s * 0.09, s * 0.035, "#8a94a4", a)
        if dead > 0: xmark(c, s * ex - s * 0.18, s * ey, s * 0.04, a * dead)
    c.restore()

def vo7_ash(c, W, H, t, S):
    def p_ash(c, ts, lt, d):
        cone(c, 1350, 960, 900, 520, t, erupt=1.0, plume_h=700, seed=4)
        rng = random.Random(8)
        for i in range(220):
            q = (rng.random() + t * 0.05) % 1
            circle(c, lerp(1300, -100, q) + rng.gauss(0, 60), 300 + rng.gauss(0, 90) + q * 380, rng.uniform(2, 6), "#b9b0a8", 0.5)
        T(c, "NOT LAVA:", 520, 260, 60, ts, "#ffffff", vis(lt, 0.4))
        T(c, "ASH", 520, 470 if ts > 1 else 410, 140, ts, ASH, vis(lt, 1.0))
    def p_micro(c, ts, lt, d):
        shards(c, 620, 540, 330, t, vis(lt, 0.1))
        T(c, "UNDER THE MICROSCOPE (ILLUSTRATIVE)", 620, 950, 24, ts, "#bdb3aa", 1, w=700, fam="Inter")
        for i, (s_, colr) in enumerate([("ROCK", "#b8a48c"), ("MINERALS", "#7a8a96"), ("VOLCANIC GLASS", "#e9e4dc")]):
            C(c, s_, 1420, 280 + i * 110, vis(lt, 0.5 + i * 0.5), ts, size=34, dot=colr)
        C(c, "HARD · ABRASIVE", 1420, 640, vis(lt, d * 0.5), ts, size=32, bg="#3a1010", dot=RED)
        C(c, "DOESN'T DISSOLVE IN WATER", 1420, 750, vis(lt, d * 0.7), ts, size=30, bg="#3a1010", dot=RED)
    def p_jet(c, ts, lt, d):
        cloud_x = 1100
        rng = random.Random(3)
        for i in range(70):
            circle(c, cloud_x + rng.gauss(0, 260), 470 + rng.gauss(0, 130), rng.uniform(40, 110), mix("#8a8078", "#4a423c", rng.random()), 0.35)
        q = clamp(lt / max(1, d))
        jet(c, lerp(200, 1250, q), 470 + math.sin(t * 2) * 6, 170, dead=vis(lt, d * 0.75))
        C(c, "1982 · BRITISH AIRWAYS 747", 480, 150, vis(lt, 0.3), ts, size=32, dot="#cfd8e8")
        C(c, "ASH FROM GALUNGGUNG, INDONESIA", 1300, 150, vis(lt, d * 0.4), ts, size=30, dot=ASH)
        C(c, "ALL 4 ENGINES STOPPED", 960, 950, vis(lt, d * 0.78), ts, size=36, bg="#3a1010", dot=RED)
    def p_drop(c, ts, lt, d):
        x0, x1, y0, y1 = 260, 1700, 200, 860
        line(c, x0, y0, x0, y1, "#ffffff", 3, 0.6); line(c, x0, y1, x1, y1, "#ffffff", 3, 0.6)
        for km in (0, 4, 8, 12):
            yy = lerp(y1, y0, km / 12); T(c, f"{km} KM", x0 - 70, yy, 26, ts, "#d8cfc6", 1, w=700, maxw=140)
        Y = lambda km: lerp(y1, y0, km / 12)
        pts = []; q = clamp(lt / (d * 0.8))
        for i in range(101):
            f = i / 100
            if f > q: break
            km = 11.3 if f < 0.2 else (lerp(11.3, 3.8, (f - 0.2) / 0.5) if f < 0.7 else lerp(3.8, 4.5, (f - 0.7) / 0.3))
            pts.append((lerp(x0 + 40, x1 - 40, f), Y(km)))
        if len(pts) > 1: c.drawPath(poly(pts, close=False), paint(LAVA, 1, stroke=6))
        if pts: jet(c, pts[-1][0], pts[-1][1] - 30, 70, ang=12 if 0.2 < q < 0.7 else 0)
        C(c, "DROPPED ≈7.5 KM", lerp(x0, x1, 0.45), Y(8.5), vis(lt, d * 0.35), ts, size=32, dot=RED)
        C(c, "ENGINES RESTARTED IN CLEARER AIR", lerp(x0, x1, 0.72), Y(1.6), vis(lt, d * 0.62), ts, size=28, dot=GREEN)
        C(c, "LANDED SAFELY IN JAKARTA", 1120, 110, vis(lt, d * 0.82), ts, size=34, bg=YEL, fg="#1a120c", a=1)
    def p_europe(c, ts, lt, d):
        bb = (-30, 34, 32, 70); rr = geo.map_rect(bb, 960, 560, height=880)
        geo.draw_map(c, bb, rr, land=LANDC, sea=SEA, outline="#000000", outline_w=1.2)
        ix, iy = geo.lonlat_xy(-19.6, 63.6, bb, rr)
        circle(c, ix, iy, 12, MAGMA); circle(c, ix, iy, 26 + 6 * math.sin(t * 4), MAGMA, 0.8, stroke=4)
        q = eout(prog(lt, 0.3, d * 0.6)); rng = random.Random(6)
        c.save(); c.clipRect(skia.Rect.MakeXYWH(*rr))
        for i in range(260):
            f = rng.random() ** 0.8
            if f > q: continue
            ang = math.radians(rng.gauss(-25, 18) + 120 * f * 0)
            x = ix + f * 1050 * math.cos(math.radians(10 + rng.gauss(0, 16))); y = iy + f * 520 * (0.3 + rng.random() * 0.9)
            circle(c, x, y, rng.uniform(14, 40), "#a8a098", 0.18)
        c.restore()
        C(c, "APRIL 2010 · ONE ICELANDIC VOLCANO", 760, 80, vis(lt, 0.3), ts, size=32, dot=MAGMA)
        C(c, "100,000+ FLIGHTS CANCELLED IN A WEEK", 1250, 900, vis(lt, d * 0.4), ts, size=32, bg=YEL, fg="#1a120c", a=1)
        C(c, "≈7 MILLION TRAVELERS STUCK", 1250, 1000, vis(lt, d * 0.65), ts, size=30)
    def p_ground(c, ts, lt, d):
        world(c, 0.9); world_pins(c, t, ign=1, size=6)
        rng = random.Random(12)
        q = clamp(lt / (d * 0.7))
        for i in range(40):
            lo0, la0 = rng.uniform(-150, 150), rng.uniform(-40, 60); lo1, la1 = lo0 + rng.uniform(40, 110), la0 + rng.uniform(-20, 20)
            x0_, y0_ = wxy(lo0, la0); x1_, y1_ = wxy(min(lo1, 178), max(-55, min(75, la1)))
            p = skia.Path(); p.moveTo(x0_, y0_); p.quadTo((x0_ + x1_) / 2, min(y0_, y1_) - 60, x1_, y1_)
            c.drawPath(p, paint("#cfd8e8", 0.45 * (1 - q), stroke=2.5, dash=([10, 8], -t * 30)))
        C(c, "MOST AIR TRAFFIC STOPS", 960, 110, vis(lt, d * 0.45), ts, size=36, bg="#3a1010", dot=RED)
        T(c, "OUR ESTIMATE", 960, 1010, 26, ts, "#bdb3aa", vis(lt, d * 0.45), w=700, fam="Inter")
    go(c, W, H, t, S, dict(ash=p_ash, micro=p_micro, jet=p_jet, drop=p_drop, europe=p_europe, ground=p_ground),
       lsched(S, ["ash", "micro", "jet", "drop", "europe", "ground"]))

def alt_axis(c, ts, x0, y0, y1, top_km, a=1.0, step=10):
    line(c, x0, y0, x0, y1, "#ffffff", 3, 0.6 * a)
    for km in range(0, top_km + 1, step):
        yy = lerp(y0, y1, km / top_km); line(c, x0 - 10, yy, x0, yy, "#ffffff", 3, 0.6 * a)
        T(c, f"{km} KM", x0 - 80, yy, 24, ts, "#d8cfc6", a, w=700, maxw=150)
    return lambda km: lerp(y0, y1, km / top_km)

def droplets(c, x0, x1, y0, y1, t, a=1.0, n=120, colr="#f2e7b8"):
    rng = random.Random(9)
    for i in range(n):
        x = x0 + (rng.random() * (x1 - x0) + t * 12) % (x1 - x0); y = y0 + rng.random() * (y1 - y0)
        circle(c, x, y, rng.uniform(2, 5), colr, a * 0.7)

def vo7_sulfur(c, W, H, t, S):
    def p_fall(c, ts, lt, d):
        cone(c, 960, 980, 820, 420, t, erupt=1.0, plume_h=520, seed=5, lava=False)
        rng = random.Random(2)
        for i in range(120):
            q = (rng.random() + t * 0.2) % 1
            circle(c, 960 + rng.gauss(0, 380), 300 + q * 600, rng.uniform(2, 5), ASH, 0.6 * (1 - q))
        T(c, "ASH: FALLS OUT IN DAYS TO WEEKS", 520, 130, 34, ts, ASH, vis(lt, 0.3), maxw=900)
        q = prog(lt, d * 0.5, 2.5)
        for i in range(30):
            ph = (i * 0.137 + t * 0.15) % 1
            circle(c, 960 + math.sin(i * 2.3) * 300, 560 - ph * 450 * (0.3 + q), 9, "#f2e27a", q * 0.8 * (1 - ph))
        T(c, "SULFUR: GOES UP", 1450, 130, 44, ts, "#f2e27a", vis(lt, d * 0.55), maxw=700)
    def p_strat(c, ts, lt, d):
        Y = alt_axis(c, ts, 200, 960, 140, 50)
        c.drawRect(skia.Rect.MakeLTRB(220, Y(50), 1820, Y(12)), paint("#6a7aa0", 0.12))
        T(c, "STRATOSPHERE", 1600, Y(44), 32, ts, "#cfe0ff", 1, w=800, maxw=500)
        T(c, "WEATHER", 1600, Y(5), 30, ts, "#d8cfc6", 1, w=800, maxw=400)
        line(c, 220, Y(12), 1820, Y(12), "#cfe0ff", 2, 0.5, dash=([12, 10], 0))
        cone(c, 520, 960, 420, 150, t, erupt=1.0, plume_h=0, seed=6, lava=False)
        q = eout(prog(lt, 0.3, d * 0.35))
        for i in range(24):
            ph = (i / 24 + t * 0.1) % 1
            circle(c, 520 + math.sin(i * 1.7) * 60 * ph, lerp(Y(2), Y(12 + 18 * q), ph), 8, "#f2e27a", 0.8)
        hz = vis(lt, d * 0.4)
        droplets(c, 260, 1800, Y(30), Y(18), t, hz)
        sx, sy = 1500, Y(48)
        for k in range(3):
            x = 1020 + k * 260
            arrow(c, x - 110, Y(49), x, Y(31), "#ffe9a0", 5, hz)
            arrow(c, x, Y(31), x + 110, Y(49), "#ffe9a0", 4, hz * 0.7, dash=([10, 8], 0))
        T(c, "SUNLIGHT", 1280, Y(47), 26, ts, "#ffe9a0", hz, w=800, maxw=300)
        C(c, "TINY DROPLETS REFLECT SUNLIGHT", 1250, Y(9), vis(lt, d * 0.6), ts, size=30, dot="#f2e27a")
    def p_pina(c, ts, lt, d):
        Y = alt_axis(c, ts, 200, 960, 140, 45, step=15)
        q = eout(prog(lt, 0.2, d * 0.6))
        cone(c, 760, 960, 560, 160, t, erupt=1, plume_h=0, seed=7, lava=False)
        top = lerp(Y(1), Y(40), q)
        rng = random.Random(7)
        for i in range(40):
            f = i / 39; yy = lerp(Y(1.5), top + 40, f)
            circle(c, 760 + math.sin(i * 1.3 + t) * 12 + rng.uniform(-20, 20), yy, 50 + f * 50, mix("#9a9088", "#5a524c", rng.random()), 0.8)
        for i in range(9):
            circle(c, 760 + (i - 4) * 50 * q, top + 30 + abs(i - 4) * 4, 50 + 10 * math.sin(i + t), mix("#b0a8a0", "#6a625c", (i % 3) / 3), 0.85 * q)
        C(c, "MOUNT PINATUBO · 1991", 1400, 260, vis(lt, 0.2), ts, size=34, dot=MAGMA)
        C(c, "COLUMNS UP TO ≈40 KM", 1400, 380, vis(lt, d * 0.35), ts, size=32, dot=LAVA)
        C(c, "≈17 MILLION TONNES SO₂", 1400, 500, vis(lt, d * 0.6), ts, size=34, bg=YEL, fg="#1a120c", a=1)
    def p_spread(c, ts, lt, d):
        R = 400; rot = 120 + t * 4
        img, Rq = globe_im(R, rot, 12)
        c.drawImageRect(img, skia.Rect.MakeXYWH(960 - Rq, 540 - Rq, 2 * Rq, 2 * Rq), skia.SamplingOptions(skia.FilterMode.kLinear), skia.Paint())
        w1 = prog(lt, 0.3, d * 0.35); w2 = prog(lt, d * 0.5, d * 0.4)
        bandh = Rq * (0.12 + 0.2 * w1 + 0.68 * w2)
        c.save(); p = skia.Path(); p.addCircle(960, 540, Rq); c.clipPath(p, doAntiAlias=True)
        c.drawRect(skia.Rect.MakeLTRB(960 - Rq, 540 + Rq * 0.25 - bandh, 960 + Rq, 540 + Rq * 0.25 + bandh * 0.7), paint("#ffe9a0", 0.6 * clamp(w1 * 3), blur=24))
        c.restore()
        C(c, "AROUND THE EARTH: ≈3 WEEKS", 960, 80, vis(lt, 0.4), ts, size=34, dot="#f2e7b8")
        C(c, "WHOLE GLOBE: ≈1 YEAR", 960, 1010, vis(lt, d * 0.55), ts, size=34, bg=YEL, fg="#1a120c", a=1)
    def p_tonga(c, ts, lt, d):
        Y = alt_axis(c, ts, 220, 960, 140, 60)
        c.drawRect(skia.Rect.MakeLTRB(240, Y(60), 1820, Y(50)), paint("#8a6ad0", 0.15))
        T(c, "MESOSPHERE", 1650, Y(55), 28, ts, "#d8c8ff", 1, w=800, maxw=400)
        for i, (nm, km, x, colr, t0) in enumerate([("AIRLINER ≈11 KM", 11, 520, "#cfd8e8", 0.2), ("PINATUBO ≈35–40 KM", 38, 900, LAVA, 0.6), ("HUNGA TONGA ≈58 KM", 58, 1300, MAGMA, d * 0.35)]):
            q = eout(prog(lt, t0, 1.2))
            rrect(c, x - 50, Y(km * q), 100, Y(0) - Y(km * q), 12, colr, 0.85)
            C(c, nm, x, Y(km * q) - 45, vis(lt, t0 + 0.6), ts, size=26, bg=CHIPBG)
        C(c, "JAN 2022 · HIGHEST PLUME IN THE SATELLITE RECORD", 1000, 1030, vis(lt, d * 0.6), ts, size=28, dot=MAGMA)
    def p_many(c, ts, lt, d):
        rng = random.Random(4)
        for i in range(9):
            x = 160 + i * 200 + rng.uniform(-40, 40); s = rng.uniform(0.5, 0.9)
            cone(c, x, 1000, 320 * s, 220 * s, t, erupt=vis(lt, i * 0.25), plume_h=640 * s, seed=10 + i, lava=False)
        droplets(c, 0, 1920, 120, 260, t, vis(lt, d * 0.5), n=200)
        C(c, "ONE SHARED HAZE", 960, 200, vis(lt, d * 0.5), ts, size=36, bg=YEL, fg="#1a120c", a=1)
    go(c, W, H, t, S, dict(fall=p_fall, strat=p_strat, pinatubo=p_pina, spread=p_spread, tonga=p_tonga, many=p_many),
       lsched(S, ["fall", "strat", "pinatubo", "spread", "tonga", "many"]))

def field(c, t, hy=800, snow=0.0, dim=0.0, a=1.0):
    c.drawRect(skia.Rect.MakeLTRB(0, hy, VW, VH), paint(shader=lin(0, hy, 0, VH, [(0, mix("#5a6a3a", "#c8d0d8", snow), a), (1, mix("#2e3a20", "#8a96a4", snow), a)])))
    rng = random.Random(3)
    for i in range(40):
        x = rng.uniform(0, VW); h = rng.uniform(30, 70) * (1 - 0.5 * dim)
        line(c, x, hy + 10, x + math.sin(t + i) * 4, hy + 10 - h, mix("#7aa04a", "#6a6a5a", dim), 4, a)
    if snow > 0:
        for i in range(140):
            q = (rng.random() + t * 0.08) % 1
            circle(c, rng.uniform(0, VW) + math.sin(t + i) * 20, q * hy, rng.uniform(2, 5), "#ffffff", 0.8 * snow * a)
    if dim > 0: c.drawRect(skia.Rect.MakeXYWH(0, 0, VW, VH), paint("#0a0d12", 0.45 * dim * a))

def thermo(c, ts, x, y, h, val, lo=-1.0, hi=0.5, lab="", a=1.0, colr=COLD):
    w = 46
    rrect(c, x - w / 2, y - h / 2, w, h, w / 2, "#ffffff", 0.85 * a); circle(c, x, y + h / 2 + 30, 48, "#ffffff", 0.85 * a)
    f = clamp((val - lo) / (hi - lo)); top = y + h / 2 - f * h
    rrect(c, x - w / 2 + 8, top, w - 16, y + h / 2 - top + 20, (w - 16) / 2, colr, a); circle(c, x, y + h / 2 + 30, 36, colr, a)
    if lab: T(c, lab, x + 60, top, 46, ts, colr, a, align="l", maxw=700)

def vo7_winter(c, W, H, t, S):
    def p_milky(c, ts, lt, d):
        stage_bg(c, "#c9c4bd", "#e8d4c0")
        sx, sy = 1400, 330
        circle(c, sx, sy, 200, "#ff9a6a", 0.35, blur=80); circle(c, sx, sy, 70, "#ffd2b0", 0.9)
        field(c, t, hy=760, dim=0.3)
        droplets(c, 0, 1920, 60, 600, t, 0.5, n=180, colr="#ffffff")
        C(c, "A PALE, MILKY SKY", 480, 200, vis(lt, 0.3), ts, size=34, bg=CHIPBG, dot="#ffffff")
        C(c, "RED SUNSETS", 480, 310, vis(lt, d * 0.35), ts, size=32, dot="#ff7a5a")
        C(c, "THE PLANET COOLS", 480, 420, vis(lt, d * 0.6), ts, size=34, bg=YEL, fg="#1a120c", a=1)
    def p_pina(c, ts, lt, d):
        q = eout(prog(lt, 0.5, d * 0.5))
        thermo(c, ts, 620, 520, 520, -0.5 * q, lab=f"−{0.5 * q:.1f} °C" if q > 0.05 else "", a=1)
        C(c, "AFTER PINATUBO", 1300, 330, vis(lt, 0.2), ts, size=34, dot=MAGMA)
        C(c, "NORTHERN HEMISPHERE: UP TO ≈0.5 °C COOLER", 1300, 460, vis(lt, d * 0.45), ts, size=28, dot=COLD)
        C(c, "ONE VOLCANO", 1300, 590, vis(lt, d * 0.7), ts, size=34, bg=YEL, fg="#1a120c", a=1)
    def p_tam(c, ts, lt, d):
        bb = (100, -15, 130, 5); rr = geo.map_rect(bb, 960, 560, height=760)
        geo.draw_map(c, bb, rr, land=LANDC, sea=SEA, outline="#000000", outline_w=1.2)
        x, y = geo.lonlat_xy(118.0, -8.25, bb, rr)
        circle(c, x, y, 70 + 20 * math.sin(t * 3), MAGMA, 0.3, blur=20); circle(c, x, y, 14, LAVA)
        C(c, "MOUNT TAMBORA · 1815", x, y - 110, vis(lt, 0.3), ts, size=34, dot=MAGMA)
        C(c, "LARGEST ERUPTION EVER RECORDED", 960, 1000, vis(lt, d * 0.4), ts, size=34, bg=YEL, fg="#1a120c", a=1)
    def p_snow(c, ts, lt, d):
        stage_bg(c, "#9aa6b4", "#d8dee6")
        field(c, t, hy=720, snow=vis(lt, 0.5))
        rrect(c, 1340, 180, 380, 400, 26, "#f4efe6"); rrect(c, 1340, 180, 380, 110, 26, "#c8413a"); rect(c, 1340, 250, 380, 40, "#c8413a")
        text(c, "JULY", 1530, 235, 60, "#ffffff", w=900); text(c, "1816", 1530, 430, 140, "#1a120c", w=900)
        C(c, "THE YEAR WITHOUT A SUMMER", 600, 200, vis(lt, 0.3), ts, size=36, bg=YEL, fg="#1a120c", a=1)
        C(c, "SNOW IN NEW ENGLAND", 600, 320, vis(lt, d * 0.35), ts, size=32, dot=COLD)
        C(c, "CROPS FAILED: N. AMERICA, W. EUROPE, ASIA", 760, 960, vis(lt, d * 0.65), ts, size=28, dot=RED)
    def p_plunge(c, ts, lt, d):
        field(c, t, hy=820, snow=0.3, dim=0.6)
        q = prog(lt, 0.3, 2.0)
        thermo(c, ts, 960, 450, 560, lerp(0.3, -0.95, eout(q)), a=1)
        T(c, "?", 1160, 360, 220, ts, COLD, vis(lt, 1.2))
        C(c, "NO EXACT NUMBER", 520, 300, vis(lt, d * 0.3), ts, size=32, dot=COLD)
        C(c, "A VOLCANIC WINTER", 1420, 650, vis(lt, d * 0.6), ts, size=36, bg=YEL, fg="#1a120c", a=1)
    def p_fade(c, ts, lt, d):
        x0, x1, y0 = 260, 1660, 640
        line(c, x0, y0, x1, y0, "#ffffff", 4, 0.7)
        for i, yr in enumerate(("YEAR 0", "1", "2", "3")):
            x = lerp(x0, x1, i / 3); line(c, x, y0 - 14, x, y0 + 14, "#ffffff", 3); T(c, yr, x, y0 + 50, 30, ts, "#ffffff", 1, w=800, maxw=200)
        q = clamp(lt / (d * 0.8))
        pts = [(x0, y0 - 20)]
        for i in range(61):
            f = i / 60
            if f > q: break
            pts.append((lerp(x0, x1, f), lerp(y0 - 30, y0 - 380, (1 - f) ** 1.3)))
        if len(pts) > 2:
            pts.append((pts[-1][0], y0 - 20))
            c.drawPath(poly(pts), paint(shader=lin(0, y0 - 380, 0, y0, [(0, "#ffe9a0", 0.75), (1, "#ffe9a0", 0.15)])))
            c.drawPath(poly(pts[1:-1], close=False), paint("#ffe9a0", 1, stroke=5))
        T(c, "HAZE", x0 + 60, y0 - 420, 34, ts, "#ffe9a0", 1, w=800, align="l", maxw=300)
        C(c, "THE HAZE SLOWLY FALLS OUT", 960, 160, vis(lt, 0.3), ts, size=34, dot="#f2e7b8")
        C(c, "PINATUBO: COOLING FADED IN ≈3 YEARS", 960, 860, vis(lt, d * 0.5), ts, size=32, bg=YEL, fg="#1a120c", a=1)
    names = ["milky", "pina", "tambora", "snow", "plunge", "fade"]
    go(c, W, H, t, S, dict(milky=p_milky, pina=p_pina, tambora=p_tam, snow=p_snow, plunge=p_plunge, fade=p_fade),
       lsched(S, names, lines=[0, 2, 3, 4, 5, 6]), look="cold")

def vo7_co2(c, W, H, t, S):
    def p_swap(c, ts, lt, d):
        rrect(c, 360, 260, 360, 560, 30, "#cfe8ff", vis(lt, 0.2)); line(c, 360, 480, 720, 480, "#7a9ab8", 6, vis(lt, 0.2))
        T(c, "FREEZER", 540, 900, 44, ts, COLD, vis(lt, 0.3), maxw=500)
        arrow(c, 800, 540, 1100, 540, "#ffffff", 8, vis(lt, d * 0.5))
        rrect(c, 1180, 300, 420, 500, 30, "#3a2a24", vis(lt, d * 0.55)); rrect(c, 1230, 380, 320, 280, 20, "#1a0e08", vis(lt, d * 0.55))
        circle(c, 1390, 520, 110, MAGMA, 0.4 * vis(lt, d * 0.55), blur=40)
        T(c, "OVEN?", 1390, 900, 44, ts, MAGMA, vis(lt, d * 0.6), maxw=500)
        C(c, "VOLCANOES ALSO RELEASE CO₂", 960, 110, vis(lt, d * 0.25), ts, size=34, dot=ASH)
    def p_myth(c, ts, lt, d):
        cone(c, 600, 980, 700, 420, t, erupt=0.7, plume_h=420, seed=8, lava=False)
        T(c, "“VOLCANOES EMIT MORE CO₂ THAN HUMANS”", 1250, 250, 40, ts, "#ffffff", vis(lt, 0.2), maxw=1150)
        stamp(c, "MYTH", 1300, 560, prog(lt, d * 0.45, 0.35), 1.0 * ts, color=RED, size=120, rot=-8)
    def p_bars(c, ts, lt, d):
        x0, wmax = 360, 1400
        q1 = eout(prog(lt, 0.3, 1.0)); q2 = eout(prog(lt, d * 0.45, 2.0))
        T(c, "ALL VOLCANOES", x0, 430, 36, ts, ASH, 1, align="l", maxw=700)
        rrect(c, x0, 480, max(12, wmax * 0.3 / 40 * q1), 90, 12, MAGMA)
        T(c, "≈0.3 BILLION T / YEAR", x0 + 60, 525, 36, ts, LAVA, vis(lt, 0.8), align="l", maxw=800)
        T(c, "HUMANS", x0, 700, 36, ts, "#ffffff", vis(lt, d * 0.4), align="l", maxw=700)
        rrect(c, x0, 750, max(1, wmax * q2), 90, 12, "#d8dee6", vis(lt, d * 0.45))
        T(c, "≈40 BILLION T / YEAR", x0 + 20, 900, 36, ts, "#ffffff", vis(lt, d * 0.7), align="l", maxw=900)
        C(c, "CO₂ PER YEAR · NOAA CLIMATE.GOV", 960, 150, vis(lt, 0.2), ts, size=28)
    def p_60(c, ts, lt, d):
        T(c, "60×", 960, 450, 300, ts, YEL, vis(lt, 0.2), maxw=1200)
        T(c, "OR MORE", 960, 680, 60, ts, "#ffffff", vis(lt, 0.6), maxw=900)
        C(c, "HUMANS vs EVERY VOLCANO ON EARTH", 960, 860, vis(lt, 0.9), ts, size=32, dot=MAGMA)
    def p_nine(c, ts, lt, d):
        cx, cy, r = 700, 540, 260
        circle(c, cx, cy, r, "#120d0a", 0.9); circle(c, cx, cy, r, "#ffffff", 1, stroke=10)
        q = prog(lt, 0.4, d * 0.6) * 0.75
        p = skia.Path(); p.moveTo(cx, cy); p.arcTo(skia.Rect.MakeXYWH(cx - r * 0.85, cy - r * 0.85, r * 1.7, r * 1.7), -90, 360 * q, False); p.close()
        c.drawPath(p, paint(MAGMA, 0.85))
        for k in range(12):
            an = k / 12 * 2 * math.pi
            line(c, cx + math.sin(an) * r * 0.85, cy - math.cos(an) * r * 0.85, cx + math.sin(an) * r * 0.95, cy - math.cos(an) * r * 0.95, "#ffffff", 5)
        T(c, "≈9 HOURS", 1350, 420, 110, ts, LAVA, vis(lt, d * 0.4), maxw=800)
        C(c, "PINATUBO MATCHED HUMAN CO₂ OUTPUT", 1350, 600, vis(lt, 0.3), ts, size=30, dot=MAGMA)
    def p_long(c, ts, lt, d):
        cx, cy = 960, 520
        c.drawPath(poly([(cx - 160, cy - 260), (cx + 160, cy - 260), (cx, cy), (cx + 160, cy + 260), (cx - 160, cy + 260), (cx, cy)]), paint("#d8cfc6", 1, stroke=8))
        q = (t * 0.15) % 1
        c.drawPath(poly([(cx - 130 * (1 - q), cy - 240 + 230 * q), (cx + 130 * (1 - q), cy - 240 + 230 * q), (cx, cy)]), paint(MAGMA, 0.9))
        c.drawPath(poly([(cx - 130 * q, cy + 240 - 0 * q), (cx + 130 * q, cy + 240), (cx, cy + 240 - 200 * q)]), paint(MAGMA, 0.9))
        C(c, "THE REAL DANGER: TIME", 960, 900, vis(lt, d * 0.35), ts, size=36, bg=YEL, fg="#1a120c", a=1)
    go(c, W, H, t, S, dict(swap=p_swap, myth=p_myth, bars=p_bars, x60=p_60, nine=p_nine, long=p_long),
       lsched(S, ["swap", "myth", "bars", "x60", "nine", "long"]))

def vo7_super(c, W, H, t, S):
    def p_cube(c, ts, lt, d):
        q = eout(prog(lt, 0.4, 1.5)); s = 420 * q; x, y = 960, 640
        if s > 2:
            c.drawPath(poly([(x - s / 2, y - s / 2), (x + s / 2, y - s / 2), (x + s / 2 + s * 0.35, y - s / 2 - s * 0.3), (x - s / 2 + s * 0.35, y - s / 2 - s * 0.3)]), paint("#8a7a6a"))
            c.drawPath(poly([(x + s / 2, y - s / 2), (x + s / 2 + s * 0.35, y - s / 2 - s * 0.3), (x + s / 2 + s * 0.35, y + s / 2 - s * 0.3), (x + s / 2, y + s / 2)]), paint("#4a3e36"))
            rect(c, x - s / 2, y - s / 2, s, s, "#6a5c50")
        T(c, "> 1,000 KM³", 960, 160, 90, ts, LAVA, vis(lt, d * 0.35), maxw=1000)
        C(c, "A SUPER-ERUPTION (VEI 8)", 960, 980, vis(lt, d * 0.5), ts, size=34, dot=MAGMA)
    def p_city(c, ts, lt, d):
        skyline(c, VW, 900, VH, 21, "#2a2622", win=0.6, maxh=0.33)
        q = eout(prog(lt, 0.4, d * 0.5))
        top = lerp(900, 230, q)
        c.drawRect(skia.Rect.MakeLTRB(0, top, VW, 900), paint(shader=lin(0, top, 0, 900, [(0, "#8a7a6a", 0.95), (1, "#5a4c40", 0.95)])))
        line(c, 1780, 900, 1780, top, "#ffffff", 4, q); T(c, "≈640 M", 1660, (900 + top) / 2, 44, ts, "#ffffff", q, maxw=300)
        C(c, "ALL OF LONDON, BURIED", 700, 150, vis(lt, d * 0.5), ts, size=34, bg=YEL, fg="#1a120c", a=1)
        T(c, "OUR ROUGH MATH: 1,000 KM³ ÷ ≈1,570 KM²", 700, 1010, 26, ts, "#d8cfc6", vis(lt, d * 0.5), w=700, fam="Inter", maxw=1100)
    def p_taupo(c, ts, lt, d):
        bb = (164, -48, 180, -33); rr = geo.map_rect(bb, 760, 560, height=900)
        geo.draw_map(c, bb, rr, land=LANDC, sea=SEA, outline="#000000", outline_w=1.2)
        x, y = geo.lonlat_xy(175.9, -38.8, bb, rr)
        circle(c, x, y, 30 + 8 * math.sin(t * 3), MAGMA, 1, stroke=5); circle(c, x, y, 10, LAVA)
        C(c, "TAUPŌ, NEW ZEALAND", 1450, 400, vis(lt, 0.3), ts, size=34, dot=MAGMA)
        C(c, "≈27,000 YEARS AGO", 1450, 520, vis(lt, d * 0.45), ts, size=36, bg=YEL, fg="#1a120c", a=1)
        C(c, "MOST RECENT SUPER-ERUPTION", 1450, 640, vis(lt, d * 0.6), ts, size=28)
    def p_yell(c, ts, lt, d):
        bb = (-125, 25, -66, 50); rr = geo.map_rect(bb, 760, 560, width=1300)
        geo.draw_map(c, bb, rr, land=LANDC, sea=SEA, outline="#000000", outline_w=1.2)
        x, y = geo.lonlat_xy(-110.5, 44.6, bb, rr)
        circle(c, x, y, 30 + 8 * math.sin(t * 3), MAGMA, 1, stroke=5); circle(c, x, y, 10, LAVA)
        C(c, "YELLOWSTONE", x, y - 80, vis(lt, 0.3), ts, size=32, dot=MAGMA)
        T(c, "1 IN 730,000", 1500, 430, 76, ts, LAVA, vis(lt, d * 0.3), maxw=760)
        T(c, "CHANCE PER YEAR (USGS)", 1500, 530, 32, ts, "#ffffff", vis(lt, d * 0.35), w=800, maxw=700)
        C(c, "NO EVIDENCE ONE IS COMING", 1500, 700, vis(lt, d * 0.7), ts, size=32, bg="#123a2a", dot=GREEN)
    go(c, W, H, t, S, dict(cube=p_cube, city=p_city, taupo=p_taupo, yell=p_yell), lsched(S, ["cube", "city", "taupo", "yell"]))

US = [(-124.7, 48.4), (-123, 49), (-95, 49), (-89.5, 48), (-84.5, 46.5), (-82.5, 45.3), (-82.4, 43), (-79, 43.3), (-76, 44), (-74.7, 45), (-71.5, 45),
      (-69.2, 47.4), (-67.8, 47), (-67, 44.8), (-70, 43.7), (-70.6, 41.8), (-74, 40.6), (-75.5, 38.5), (-76, 36.9), (-75.5, 35.2), (-79, 33.6),
      (-81.2, 31.5), (-80.2, 27), (-80.4, 25.2), (-81.8, 26.3), (-82.8, 28), (-84.3, 30), (-88, 30.3), (-89.6, 29.2), (-94, 29.6), (-97.2, 26),
      (-99.5, 27.5), (-101.4, 29.8), (-103, 29), (-104.5, 29.7), (-106.5, 31.8), (-108.2, 31.3), (-111, 31.3), (-114.8, 32.5), (-117.1, 32.5),
      (-118.5, 34), (-120.6, 34.6), (-121.9, 36.6), (-123.7, 38.9), (-124.2, 41.9), (-124, 46.3)]

def vo7_twist(c, W, H, t, S):
    def p_once(c, ts, lt, d):
        T(c, "IT HAPPENED.", 960, 400, 130, ts, LAVA, vis(lt, 0.3), maxw=1600)
        T(c, "JUST NOT ALL AT ONCE.", 960, 600, 80, ts, "#ffffff", vis(lt, d * 0.5), maxw=1600)
    def p_pangea(c, ts, lt, d):
        pangea_globe(c, 700, 560, 380, rot=40 + t * 2, tilt=-30)
        q = vis(lt, d * 0.4)
        circle(c, 760, 300, 90 + 10 * math.sin(t * 3), MAGMA, 0.5 * q, blur=30); circle(c, 760, 300, 40, LAVA, 0.8 * q)
        C(c, "≈252 MILLION YEARS AGO", 1450, 380, vis(lt, 0.3), ts, size=36, bg=YEL, fg="#1a120c", a=1)
        C(c, "SIBERIA (ON PANGAEA)", 1450, 500, vis(lt, d * 0.4), ts, size=32, dot=MAGMA)
        T(c, "SCHEMATIC SUPERCONTINENT", 700, 1010, 24, ts, "#bdb3aa", 1, w=700, fam="Inter")
    def p_us(c, ts, lt, d):
        bb = (-128, 22, -64, 52); rr = geo.map_rect(bb, 960, 560, width=1500)
        geo.draw_map(c, bb, rr, land=LANDC, sea=SEA, outline="#000000", outline_w=1.2)
        q = eout(prog(lt, 0.4, d * 0.5)); pts = [geo.lonlat_xy(lo, la, bb, rr) for lo, la in US]
        c.drawPath(poly(pts), paint(MAGMA, 0.75 * q)); c.drawPath(poly(pts), paint(LAVA, q, stroke=4))
        c.drawPath(poly(pts), paint(EMBER, 0.4 * q, blur=20))
        C(c, "SIBERIAN TRAPS: AN AREA LIKE THE USA", 960, 120, vis(lt, 0.3), ts, size=32, dot=MAGMA)
        C(c, "≈1 KM DEEP", 960, 1000, vis(lt, d * 0.55), ts, size=38, bg=YEL, fg="#1a120c", a=1)
    def p_time(c, ts, lt, d):
        x0, x1, y = 160, 1760, 560
        X = lambda ky: lerp(x0, x1, (ky + 350) / 900)
        line(c, x0, y, x1, y, "#ffffff", 4, 0.7)
        q1 = eout(prog(lt, 0.3, d * 0.3)); q2 = eout(prog(lt, d * 0.5, d * 0.3))
        rrect(c, X(-300), y - 70, (X(0) - X(-300)) * q1, 60, 10, MAGMA, 0.9)
        rrect(c, X(0), y - 70, (X(500) - X(0)) * q2, 60, 10, LAVA, 0.6)
        line(c, X(0), y - 160, X(0), y + 40, RED, 6)
        T(c, "EXTINCTION", X(0), y - 200, 40, ts, RED, 1, maxw=500)
        for ky, lab in ((-300, "−300,000 YRS"), (0, "0"), (500, "+500,000 YRS")):
            T(c, lab, X(ky), y + 80, 30, ts, "#ffffff", 1, w=800, maxw=360)
        C(c, "ERUPTIONS BEGIN", X(-150), y + 220, vis(lt, 0.5), ts, size=28, dot=MAGMA)
        C(c, "⅓ OF THE MAGMA CAME AFTER", X(250), y + 220, vis(lt, d * 0.6), ts, size=28, dot=LAVA)
    def p_loss(c, ts, lt, d):
        for i, (lab, frac, x, colr) in enumerate([("OCEAN SPECIES", 0.96, 560, COLD), ("LAND SPECIES", 0.70, 1360, GREEN)]):
            q = eout(prog(lt, 0.5 + i * 1.0, 1.4))
            donut(c, x, 500, 230, frac * q, RED, label=f"{round(frac * 100 * q)}%", u=1.0)
            T(c, lab, x, 830, 40, ts, colr, vis(lt, 0.3 + i), maxw=600)
        C(c, "END-PERMIAN EXTINCTION · BY ONE ESTIMATE", 960, 100, vis(lt, 0.2), ts, size=30, dot=RED)
    def p_vs(c, ts, lt, d):
        T(c, "1,350 VOLCANOES × 1 DAY", 960, 330, 64, ts, "#d8cfc6", vis(lt, 0.3), maxw=1600)
        line(c, 500, 330, 1420, 330, RED, 10, vis(lt, d * 0.35))
        T(c, "1 REGION × HUNDREDS OF THOUSANDS OF YEARS", 960, 620, 54, ts, LAVA, vis(lt, d * 0.5), maxw=1700)
    go(c, W, H, t, S, dict(once=p_once, pangea=p_pangea, us=p_us, time=p_time, loss=p_loss, vs=p_vs),
       lsched(S, ["once", "pangea", "us", "time", "loss", "vs"]))

def vo7_why(c, W, H, t, S):
    def p_no(c, ts, lt, d):
        T(c, "COULD IT HAPPEN?", 960, 420, 110, ts, "#ffffff", vis(lt, 0.2), maxw=1600)
        T(c, "SCIENTISTS: NO", 960, 640, 100, ts, GREEN, vis(lt, d * 0.55), maxw=1400)
    def p_iwo(c, ts, lt, d):
        island(c, t, 960, 560, 10500, grow=1.0, erupt=0.3, ts=ts)
        C(c, "ISLAND BY ISLAND", 960, 1000, vis(lt, d * 0.5), ts, size=34, bg=YEL, fg="#1a120c", a=1)
    def p_plumb(c, ts, lt, d):
        stage_bg(c, "#1a1410", "#3a2216", 1)
        c.drawRect(skia.Rect.MakeLTRB(0, 520, VW, VH), paint(shader=lin(0, 520, 0, VH, [(0, "#4a3a2e", 1), (1, "#2a1a10", 1)])))
        for i, x in enumerate((360, 960, 1560)):
            cone(c, x, 520, 420, 260, t, erupt=0.0, seed=i)
            oval(c, x, 880, 150, 70, MAGMA, 0.9); oval(c, x, 880, 150, 70, LAVA, 0.6, blur=20)
            line(c, x, 810, x, 270, EMBER, 12, 0.9)
        p = vis(lt, d * 0.25)
        if p > 0:
            for x0, x1 in ((510, 810), (1110, 1410)):
                line(c, x0, 880, x1, 880, "#ffffff", 4, p, dash=([12, 10], 0)); xmark(c, (x0 + x1) / 2, 880, 30, vis(lt, d * 0.3))
        C(c, "EACH HAS ITS OWN MAGMA", 960, 110, vis(lt, 0.3), ts, size=34, dot=MAGMA)
        C(c, "NO SWITCH CONNECTS THEM", 960, 1010, vis(lt, d * 0.3), ts, size=32, bg="#3a1010", dot=RED)
    def p_fizz(c, ts, lt, d):
        gx, gy = 960, 560
        gl = [(gx - 220, gy - 330), (gx + 220, gy - 330), (gx + 170, gy + 360), (gx - 170, gy + 360)]
        c.drawPath(poly(gl), paint("#d0a84a", 0.55)); c.drawPath(poly(gl), paint("#ffffff", 0.7, stroke=6))
        rng = random.Random(1)
        for i in range(60):
            sp = rng.uniform(0.15, 0.6); q = (rng.random() + t * sp) % 1
            circle(c, gx + rng.uniform(-150, 150), gy + 340 - q * 660, rng.uniform(5, 12), "#fff6d8", 0.75, stroke=2.5)
        C(c, "EVERY BUBBLE, AT THE SAME MOMENT?", 960, 90, vis(lt, 0.3), ts, size=32, dot=YEL)
        T(c, "ANALOGY: SCIENCE FOCUS", 960, 1010, 24, ts, "#bdb3aa", 1, w=700, fam="Inter")
    def p_48(c, ts, lt, d):
        world(c); world_pins(c, t, ign=1, colr=ASH_D, size=4)
        idx = np.argsort(VDEL)[:48]; m = np.zeros(len(VLON), bool); m[idx] = True
        q = prog(lt, 0.3, d * 0.5)
        world_pins(c, t, ign=1, mask=m & (VDEL <= VDEL[idx].max() * q + 1e-9), size=10, colr=LAVA)
        C(c, "MARCH 2022: 48 ERUPTING (SMITHSONIAN GVP)", 960, 110, vis(lt, d * 0.3), ts, size=32, bg=YEL, fg="#1a120c", a=1)
        T(c, "DOTS: ILLUSTRATIVE, NOT THE REAL 48", 960, 1010, 24, ts, "#bdb3aa", 1, w=700, fam="Inter")
    P = dict(no=p_no, plumb=p_plumb, fizz=p_fizz, x48=p_48, iwo=p_iwo)
    if S.n() >= 4:
        tf = S.ls(1) + 0.6 * (S.le(1) - S.ls(1))
        sched = [(0, "no"), (S.ls(1) - 0.3, "plumb"), (tf, "fizz"), (S.ls(2) - 0.3, "x48"), (S.ls(3) - 0.3, "iwo")]
    else:
        sched = [(0, "no")]
    go(c, W, H, t, S, P, sched)

# ================================================================== IWO JIMA SHORT
def vo7_iwo(c, W, H, t, S):
    def p_grow(c, ts, lt, d):
        island(c, t, 960, 560, 10500, grow=prog(lt, 0.2, d * 0.8), erupt=0.8, pumice=0.5, glow=1.0, ts=ts, label=False)
        C(c, "+125 ACRES", 1450, 900, vis(lt, d * 0.6), ts, size=36, bg=YEL, fg="#1a120c", a=1)
    def p_map(c, ts, lt, d):
        bb = (127, 19, 149, 40); rr = geo.map_rect(bb, 960, 560, height=1000)
        geo.draw_map(c, bb, rr, land=LANDC, sea=SEA, outline="#000000", outline_w=1.2)
        tx, ty = geo.lonlat_xy(139.69, 35.69, bb, rr); ix, iy = geo.lonlat_xy(*IWO, bb, rr)
        circle(c, tx, ty, 12, "#ffffff"); C(c, "TOKYO", tx + 170, ty - 10, 1, ts, size=26)
        line(c, tx, ty, ix, iy, "#ffffff", 4, 0.7, dash=([16, 10], 0))
        circle(c, ix, iy, 22 + 6 * math.sin(t * 5), MAGMA, 1, stroke=6); circle(c, ix, iy, 8, LAVA)
        C(c, "IWO JIMA", ix - 250, iy, vis(lt, 0.3), ts, size=28, dot=MAGMA)
        C(c, "≈1,200 KM", (tx + ix) / 2 + 220, (ty + iy) / 2, vis(lt, 0.6), ts, size=26)
    def p_quake(c, ts, lt, d):
        island(c, t, 960, 560, 10500, grow=0.0, erupt=vis(lt, 0.4), ts=ts, label=False)
        C(c, "JAPAN METEOROLOGICAL AGENCY", 960, 130, vis(lt, 0.2), ts, size=28, dot=MAGMA)
    def p_before(c, ts, lt, d):
        island(c, t, 960, 560, 10500, grow=0.0, ts=ts, label=False, sat=True)
        C(c, "26 OCT · BEFORE", 960, 120, 1, ts, size=32, bg=CHIPBG)
        T(c, "ILLUSTRATION", 1720, 1010, 24, ts, "#bdb3aa", 1, w=700, fam="Inter")
    def p_after(c, ts, lt, d):
        island(c, t, 960, 560, 10500, grow=1.0, erupt=0.4, pumice=0.9, glow=1.0, ts=ts, label=False, sat=True)
        C(c, "11 NOV · AFTER", 960, 120, 1, ts, size=32, bg=YEL, fg="#1a120c", a=1)
        T(c, "ILLUSTRATION", 1720, 1010, 24, ts, "#bdb3aa", 1, w=700, fam="Inter")
    def p_new(c, ts, lt, d):
        island(c, t, 960, 520, 12500, grow=1.0, erupt=0.3, glow=0.5 + 0.5 * math.sin(t * 3), ts=ts, label=False)
        C(c, "NEW LAND · SOUTHEAST BEACH", 1330, 930, vis(lt, 0.3), ts, size=28, dot=MAGMA)
        C(c, "JAPAN COAST GUARD · 16 NOV", 1300, 130, vis(lt, d * 0.5), ts, size=28, dot=GREEN)
    def p_fields(c, ts, lt, d):
        n = int(90 * clamp(lt / (d * 0.7) + 0.05)); cols = 15
        for i in range(n):
            r_, k = divmod(i, cols); x = 300 + k * 88; y = 300 + r_ * 92
            rrect(c, x, y, 80, 46, 6, "#3e8a3a"); line(c, x + 40, y + 4, x + 40, y + 42, "#ffffff", 2, 0.7)
        T(c, f"{n}", 620, 900, 110, ts, YEL, 1, maxw=500)
        T(c, "FOOTBALL FIELDS", 1240, 900, 44, ts, "#ffffff", 1, maxw=560)
    def p_erode(c, ts, lt, d):
        er = clamp(lt / d)
        island(c, t, 960, 560, 10500, grow=1.0, erode=er * 0.8, ts=ts, label=False)
        nx, ny = ixy(141.316, 24.750, 960, 560, 10500)
        for k in range(5):
            q = ((t * 0.35 + k / 5) % 1)
            p = skia.Path(); p.addArc(skia.Rect.MakeXYWH(nx - 80 - 260 * (1 - q), ny - 40 - 160 * (1 - q), 2 * (80 + 260 * (1 - q)), 2 * (40 + 160 * (1 - q))), 10, 150)
            c.drawPath(p, paint("#cfe8ff", 0.6 * q, stroke=5))
        C(c, "2023: GONE IN WEEKS", 1300, 140, vis(lt, d * 0.5), ts, size=30, dot=RED)
    def p_wait(c, ts, lt, d):
        island(c, t, 960, 560, 10500, grow=1.0, ts=ts, label=False)
        T(c, "?", 1500, 520, 260, ts, YEL, vis(lt, 0.3))
        C(c, "NASA'S DANIEL SLAYBACK", 960, 130, vis(lt, 0.2), ts, size=28, dot=GREEN)
    P = dict(grow=p_grow, map=p_map, quake=p_quake, before=p_before, after=p_after, newland=p_new, fields=p_fields, erode=p_erode, wait=p_wait)
    go(c, W, H, t, S, P, [(0, "grow")])

# ================================================================== NODULE SHORT (abyss look)
def nodule(c, x, y, s, seed=1, a=1.0, cut=0.0, t=0.0, crowd=0.0):
    rng = random.Random(seed); pts = []
    for k in range(40):
        an = k / 40 * 2 * math.pi; r = s * (1 + 0.12 * math.sin(an * 3 + seed) + 0.07 * math.sin(an * 7 + seed * 2))
        pts.append((x + math.cos(an) * r * 1.2, y + math.sin(an) * r * 0.85))
    pth = poly(pts)
    c.drawPath(pth, paint(shader=rad(x - s * 0.4, y - s * 0.4, s * 2, [(0, "#5a4636", 1), (0.6, "#2a1e16", 1), (1, "#120c08", 1)]), a=a))
    for k in range(int(10 + s * 0.05)):
        an = rng.random() * 6.28; d = rng.random() * s * 0.8
        circle(c, x + math.cos(an) * d * 1.1, y + math.sin(an) * d * 0.75, s * rng.uniform(0.04, 0.12), "#6a5444", a * 0.6)
    if cut > 0:  # cross-section: growth layers, cracks, animals
        c.save(); c.clipPath(pth, doAntiAlias=True)
        for k in range(9, 0, -1):
            oval(c, x, y, s * 1.15 * k / 9, s * 0.8 * k / 9, mix("#3a2a20", "#8a6a50", (k % 2) * 0.5), a * cut)
        for k in range(7):
            an = rng.random() * 6.28; p = skia.Path(); p.moveTo(x, y)
            for j in range(1, 5): p.lineTo(x + math.cos(an + rng.uniform(-0.3, 0.3)) * s * 0.25 * j, y + math.sin(an + rng.uniform(-0.3, 0.3)) * s * 0.2 * j)
            c.drawPath(p, paint("#050302", a * cut, stroke=s * 0.04))
        n = int(crowd)
        for i in range(n):
            an = rng.random() * 6.28; d = rng.random() ** 0.6 * s * 0.9
            ax, ay = x + math.cos(an) * d * 1.1, y + math.sin(an) * d * 0.75
            critter(c, ax, ay, s * 0.05, i, t, a * cut)
        c.restore()
    c.drawPath(pth, paint("#ffffff", a * 0.12, stroke=2))

def critter(c, x, y, s, i, t, a=1.0):
    kind = i % 3
    if kind == 0:  # nematode
        p = skia.Path(); p.moveTo(x - s * 2, y)
        for j in range(1, 9): p.lineTo(x - s * 2 + j * s * 0.5, y + math.sin(j * 1.3 + t * 3 + i) * s * 0.5)
        c.drawPath(p, paint("#ffe9d0", a, stroke=max(1.5, s * 0.3)))
    elif kind == 1:  # copepod
        oval(c, x, y, s * 0.9, s * 0.5, ABY, a); line(c, x - s * 0.8, y, x - s * 2, y - s * 1.1, ABY, max(1, s * 0.15), a)
        line(c, x - s * 0.8, y, x - s * 2, y + s * 1.1, ABY, max(1, s * 0.15), a); line(c, x + s * 0.8, y, x + s * 1.8, y + math.sin(t * 4 + i) * s * 0.4, ABY, max(1, s * 0.2), a)
    else:  # foraminifera-like blob
        for k in range(3): circle(c, x + k * s * 0.5, y - k * s * 0.2, s * (0.5 - k * 0.1), "#ffd27a", a * 0.9)

def seafloor(c, t, hy=760, a=1.0):
    c.drawRect(skia.Rect.MakeLTRB(0, hy, VW, VH), paint(shader=lin(0, hy, 0, VH, [(0, "#1c2a30", a), (1, "#0a1216", a)])))
    rng = random.Random(4)
    for i in range(26):
        x = rng.uniform(0, VW); yy = hy + 20 + rng.random() ** 1.5 * 280; s = rng.uniform(14, 34) * (0.5 + (yy - hy) / 300)
        nodule(c, x, yy, s, seed=i + 3, a=a)

def vo7_nod(c, W, H, t, S):
    def p_intro(c, ts, lt, d):
        z = 1 + 0.06 * lt / max(1, d)
        nodule(c, 960, 560, 300 * z, seed=2, cut=vis(lt, d * 0.35), t=t, crowd=245 * prog(lt, d * 0.35, d * 0.5))
        C(c, "245 ANIMALS · ONE NODULE (THE RECORD)", 960, 980, vis(lt, d * 0.6), ts, size=30, bg=ABY_CHIP, dot=ABY)
    def p_deep(c, ts, lt, d):
        seafloor(c, t)
        c.drawPath(poly([(0, 0), (VW, 0), (VW, 200), (0, 200)]), paint(shader=lin(0, 0, 0, 200, [(0, "#2a6a9a", 0.5), (1, "#2a6a9a", 0)])))
        bb = (-170, 0, -90, 35); rr = geo.map_rect(bb, 1460, 360, width=760)
        geo.draw_map(c, bb, rr, land="#2a4a5a", sea="#061826", outline="#000000", outline_w=1)
        ccz = [(-158, 12), (-150, 18), (-118, 19), (-113, 15), (-118, 8), (-150, 5)]
        c.drawPath(poly([geo.lonlat_xy(lo, la, bb, rr) for lo, la in ccz]), paint(ABY, 0.3 * vis(lt, 0.5)))
        c.drawPath(poly([geo.lonlat_xy(lo, la, bb, rr) for lo, la in ccz]), paint(ABY, vis(lt, 0.5), stroke=3))
        rrect(c, *rr, 8, "#ffffff", 0.3, stroke=2)
        hx, hy_ = geo.lonlat_xy(-157, 21, bb, rr); T(c, "HAWAII", hx + 20, hy_ - 40, 24, ts, "#cfe8ff", 1, w=800, maxw=300)
        T(c, "MEXICO", rr[0] + rr[2] - 150, rr[1] + 70, 24, ts, "#cfe8ff", 1, w=800, maxw=300)
        C(c, "CLARION-CLIPPERTON ZONE (APPROX.)", 540, 120, vis(lt, 0.4), ts, size=26, bg=ABY_CHIP, dot=ABY)
    def p_grow(c, ts, lt, d):
        nodule(c, 700, 560, 260, seed=5, cut=1.0, t=t)
        q = (lt * 0.25) % 1
        oval(c, 700, 560, 260 * 1.15 * (0.98 + 0.02 * q), 260 * 0.8 * (0.98 + 0.02 * q), ABY, 0.8 * (1 - q), stroke=4)
        T(c, "A FEW MM", 1440, 430, 80, ts, ABY, vis(lt, 0.3), maxw=700)
        T(c, "PER MILLION YEARS", 1440, 560, 44, ts, "#ffffff", vis(lt, 0.6), maxw=760)
    def p_crack(c, ts, lt, d):
        seafloor(c, t, hy=700)
        rng = random.Random(9)
        for i in range(12):
            x = 200 + (i % 6) * 300; y = 250 + (i // 6) * 250
            nodule(c, x, y, 80, seed=i + 20, cut=vis(lt, 0.3 + i * 0.12), t=t, crowd=14)
        C(c, "244 NODULES", 960, 1010, vis(lt, 0.4), ts, size=32, bg=ABY_CHIP, dot=ABY)
    def p_count(c, ts, lt, d):
        q = eout(prog(lt, 0.2, d * 0.7)); n = int(4139 * q)
        rng = random.Random(3)
        for i in range(int(260 * q)):
            critter(c, rng.uniform(100, 1820), rng.uniform(120, 960), rng.uniform(5, 10), i, t, 0.6)
        T(c, f"{n:,}", 960, 420, 220, ts, ABY, 1, maxw=1200)
        T(c, "ANIMALS", 960, 780, 70, ts, "#ffffff", 1, maxw=900)
    def p_record(c, ts, lt, d):
        nodule(c, 520, 560, 220, seed=8, cut=1, t=t, crowd=17)
        nodule(c, 1400, 560, 260, seed=2, cut=1, t=t, crowd=245)
        T(c, "TYPICAL: ≈17", 520, 920, 54, ts, "#ffffff", vis(lt, 0.3), maxw=800)
        T(c, "RECORD: 245", 1400, 920, 54, ts, YEL, vis(lt, d * 0.3), maxw=800)
    def p_zoom(c, ts, lt, d):
        circle(c, 960, 540, 430, "#0b1a24", 0.95); circle(c, 960, 540, 430, ABY, 0.6, stroke=8)
        for i in range(2):
            x = 960 + (i - 0.5) * 420
            critter(c, x, 540 + math.sin(t + i) * 20, 60, i, t, 1)
            T(c, ["ROUNDWORM", "CRUSTACEAN"][i], x, 760, 30, ts, "#ffffff", vis(lt, 0.3 + i * 0.4), maxw=380)
        T(c, "< 1 MM", 960, 200, 70, ts, YEL, vis(lt, 0.2), maxw=600)
    def p_mud(c, ts, lt, d):
        seafloor(c, t, hy=640)
        nodule(c, 960, 520, 200, seed=4, cut=1, t=t, crowd=40)
        C(c, "NODULE CRACKS ≠ THE MUD AROUND THEM", 960, 120, vis(lt, 0.3), ts, size=30, bg=ABY_CHIP, dot=ABY)
    def p_mining(c, ts, lt, d):
        seafloor(c, t)
        x = lerp(1700, 1100, clamp(lt / d))
        rrect(c, x - 220, 600, 440, 160, 20, "#c8b050"); rrect(c, x - 240, 740, 480, 50, 20, "#3a3a3a")
        for i in range(40):
            q = (i / 40 + t * 0.2) % 1
            circle(c, x + 240 + q * 500, 720 - q * 160, 30 + q * 60, "#6a7a80", 0.3 * (1 - q))
        for i, (m, colr) in enumerate([("NICKEL", "#b8c4cc"), ("COBALT", "#4a7aff"), ("COPPER", "#d8844a")]):
            C(c, m, 360 + i * 340, 150, vis(lt, 0.3 + i * 0.3), ts, size=30, bg=ABY_CHIP, dot=colr)
        T(c, "ILLUSTRATIVE COLLECTOR", 1500, 1030, 22, ts, "#9ab0bc", 1, w=700, fam="Inter")
    def p_warn(c, ts, lt, d):
        nodule(c, 520, 560, 220, seed=11, cut=1, t=t, crowd=30)
        T(c, "“IRREVERSIBLE LOSS", 1300, 420, 56, ts, "#ffffff", vis(lt, 0.3), maxw=1100)
        T(c, "OF UNIQUE BIODIVERSITY”", 1300, 520, 56, ts, "#ffffff", vis(lt, 0.3), maxw=1100)
        C(c, "SABINE GOLLNER, NIOZ · CO-AUTHOR", 1300, 680, vis(lt, 0.8), ts, size=28, bg=ABY_CHIP, dot=ABY)
    P = dict(intro=p_intro, deep=p_deep, grow=p_grow, crack=p_crack, count=p_count, record=p_record, zoom=p_zoom, mud=p_mud, mining=p_mining, warn=p_warn)
    go(c, W, H, t, S, P, [(0, "intro")], look="aby")

SCENES = {k: v for k, v in globals().items() if k.startswith("vo7_") and callable(v)}
