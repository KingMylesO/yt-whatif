"""Batch 05 scenes: What If All the Ice on Earth Melted? (+ ice teaser, Lake Vostok and Carnian Pluvial Episode Shorts).

Look: "glacial gauge". Deep-ocean navy backgrounds with slow caustic light, glacial cyan/white ice, a vertical
water-level GAUGE as the signature motif, real Natural Earth coastlines (geo.draw_map) with labelled city markers and
dashed highlight rings (never fake flood polygons: we have no elevation data), schematic cross-sections for ice/bedrock.
Long-form art is drawn on a virtual 1920x1080 stage. In Shorts that stage is scaled into the 0.265H..0.57H band (text x1.75).
Short-only scenes (i5_vostok, i5_rain) use a portrait stage of 1080x634 placed at 0.25H..0.58H.
"""
from common2 import *
import numpy as np, cv2
import geo
import scenes_b3_kit as kit

BG_T, BG_B = "#020d1d", "#06294a"
CYAN, ICE, ICE2 = "#7fe3ff", "#f2fbff", "#a9e4ff"
CORAL = "#ff6b5b"; YEL = ACCENT; GREENC = "#7ee0a0"
ROCK_T, ROCK_B = "#6a574c", "#2b211d"
LAND, SEA = "#4d6b5c", "#0b3a66"
CHIPBG = "#0b2b4c"
PAL = dict(accent=CYAN, chip="#0d3358", title2=ACCENT)
VW, VH = 1920, 1080
PW, PH = 1080, 634   # portrait stage (Short-only scenes)

# ------------------------------------------------------------------ stage + text
class Stage:
    def __init__(self, c, S, portrait=False): self.c, self.S, self.portrait = c, S, portrait
    def __enter__(self):
        c, S = self.c, self.S; c.save()
        if self.portrait:
            if S.P:
                c.translate(0, 0.25 * S.H); return 1.0
            sc = S.H / PH; c.translate((S.W - PW * sc) / 2, 0); c.scale(sc, sc); return 1.0
        if S.P:
            sc = S.W * 0.96 / VW
            top = 0.255 * S.H + (0.325 * S.H - VH * sc) / 2
            c.translate(S.W * 0.02, top); c.scale(sc, sc)
            return 1.75
        sc = S.W / VW; c.scale(sc, sc); return 1.0
    def __exit__(self, *e): self.c.restore()

def T(c, s, x, y, size, ts, colr="#ffffff", a=1.0, w=900, maxw=1800, align="c", shadow=10, fam="Inter Display", stroke=0):
    if a <= 0.003: return
    sz = fit(s, maxw, size * ts, w, fam)
    text(c, s, x, y, sz, colr, clamp(a), w=w, fam=fam, align=align, shadow=shadow, stroke=stroke, stroke_col="#021022")

def C(c, s, x, y, p, ts, size=32, **kw):
    kw.setdefault("bg", CHIPBG)
    chip(c, s, x, y, p, size * ts, **kw)

def F(t, a, d=0.5): return eout(prog(t, a, d))

def BB(S, E):
    """beats() that skips a leading like-and-subscribe line (opts cta == 0)."""
    off = 1 if S.opts.get("cta") == 0 and S.n() > 1 else 0
    if S.n() - off >= E: return lambda i, f=0.0: S.lt(i + off, f)
    return beats(S, E)

# ------------------------------------------------------------------ background
_BG = {}
def bg_img(W, H):
    k = (W, H)
    if k not in _BG:
        surf = skia.Surface(W, H); cc = surf.getCanvas()
        fill_bg(cc, W, H, BG_T, BG_B)
        cc.drawPaint(paint(shader=rad(W * 0.75, -H * 0.1, max(W, H) * 0.9, [(0, "#2a7fb8", 0.35), (1, "#000000", 0)])))
        cc.drawPaint(paint(shader=rad(W * 0.1, H * 1.05, max(W, H) * 0.6, [(0, "#0f4f7a", 0.4), (1, "#000000", 0)])))
        _BG[k] = surf.makeImageSnapshot()
    return _BG[k]

def bg_ice(c, W, H, t, S, flakes=True):
    c.drawImage(bg_img(W, H), 0, 0)
    u = S.u
    for k in range(5):  # slow caustic light shafts
        x = (0.12 + 0.2 * k) * W + math.sin(t * 0.3 + k) * 40 * u
        p = poly([(x - 30 * u, 0), (x + 60 * u, 0), (x + 220 * u, H), (x + 80 * u, H)])
        c.drawPath(p, paint("#9fe0ff", 0.035 + 0.02 * math.sin(t * 0.7 + k * 1.7), blur=30 * u))
    if flakes:
        rng = random.Random(5)
        for i in range(36):
            x0 = rng.random() * W; sp = rng.uniform(20, 55) * u; ph = rng.random() * H
            y = (ph + t * sp) % (H + 20) - 10; x = x0 + math.sin(t * 0.8 + i) * 18 * u
            circle(c, x, y, rng.uniform(1.2, 3.2) * u, "#e6f7ff", rng.uniform(0.15, 0.45))

def run_panels(c, W, H, t, S, items, portrait=False, bg=None):
    """items: [(t_on, fn(c, ts)), ...] in time order; each later panel fades in over the previous one."""
    bg = bg or bg_ice
    bg(c, W, H, t, S)
    for i, (t0, fn) in enumerate(items):
        t1 = items[i + 1][0] if i + 1 < len(items) else None
        if t1 is not None and t >= t1 + 0.6: continue
        a = phase(t, t0 if i > 0 else None, t1)
        if a <= 0.003: continue
        with Layer(c, a) as on:
            if not on: continue
            if i > 0 and t < t0 + 0.55: bg(c, W, H, t, S)
            if S.P: c.save(); c.clipRect(skia.Rect.MakeLTRB(0, 0.215 * H, W, 0.59 * H))
            with Stage(c, S, portrait) as ts:
                fn(c, ts)
            if S.P: c.restore()
    kit.hook(c, W, H, t, S)

# ------------------------------------------------------------------ geometry helpers
def spline(pts, p=None, move=True):
    p = p if p is not None else skia.Path()
    if move: p.moveTo(*pts[0])
    else: p.lineTo(*pts[0])
    n = len(pts)
    for i in range(n - 1):
        p0 = pts[i - 1] if i > 0 else pts[i]; p1 = pts[i]; p2 = pts[i + 1]; p3 = pts[i + 2] if i + 2 < n else pts[i + 1]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        p.cubicTo(c1[0], c1[1], c2[0], c2[1], p2[0], p2[1])
    return p

def fill_under(c, pts, ybot, shader_stops, a=1.0):
    """fill from a spline profile (left->right) down to ybot."""
    p = spline(pts); p.lineTo(pts[-1][0], ybot); p.lineTo(pts[0][0], ybot); p.close()
    ys = min(q[1] for q in pts)
    c.drawPath(p, paint(shader=lin(0, ys, 0, ybot, shader_stops), a=a))
    return p

def rock(c, pts, ybot=1080, a=1.0):
    fill_under(c, pts, ybot, [(0, ROCK_T, 1), (1, ROCK_B, 1)], a)
    c.drawPath(spline(pts), paint("#8e7869", 0.9 * a, stroke=3))

def ice_body(c, top, bed, a=1.0):
    """ice between a top profile and a bed profile (both left->right)."""
    if a <= 0.003: return
    p = spline(top); spline(bed[::-1], p, move=False); p.close()
    ys = min(q[1] for q in top); yb = max(q[1] for q in bed)
    c.drawPath(p, paint(shader=lin(0, ys, 0, yb, [(0, "#ffffff", 1), (0.55, "#d5f2ff", 1), (1, "#7fcff5", 1)]), a=a))
    c.save(); c.clipPath(p, doAntiAlias=True)
    for k in range(1, 7):  # faint annual layers
        q = [(x, y + (yb - y) * k / 7 * 0.9) for (x, y) in top]
        c.drawPath(spline(q), paint("#9fd8f5", 0.35 * a, stroke=2))
    c.restore()
    c.drawPath(spline(top), paint("#ffffff", a, stroke=4))

def water(c, x0, x1, yl, ybot, t, a=1.0, amp=6, top="#3aa0e8", bot="#062c55", alpha=0.92, hl=True):
    if a <= 0.003 or yl >= ybot: return
    n = 48; pts = []
    for i in range(n + 1):
        x = x0 + (x1 - x0) * i / n
        pts.append((x, yl + amp * math.sin(x * 0.012 + t * 2.2) + amp * 0.5 * math.sin(x * 0.031 - t * 1.4)))
    p = poly(pts + [(x1, ybot), (x0, ybot)])
    c.drawPath(p, paint(shader=lin(0, yl, 0, ybot, [(0, top, alpha), (1, bot, alpha)]), a=a))
    if hl: c.drawPath(poly(pts, close=False), paint("#bdeeff", 0.85 * a, stroke=3))

def dashed_h(c, x0, x1, y, colr="#ffffff", a=1.0, w=3, t=0.0):
    c.drawLine(x0, y, x1, y, paint(colr, a, stroke=w, dash=([18, 12], -t * 20)))

def gauge(c, x, ybot, pxm, maxv, level, ts, a=1.0, step=10, unit="M", readout=None, w=64, t=0.0, ticks=True, label_side="l", rcol=YEL, rside="r"):
    """THE motif: a vertical water-level gauge. level in metres."""
    if a <= 0.003: return
    h = pxm * maxv; top = ybot - h
    rrect(c, x - w / 2 - 8, top - 18, w + 16, h + 36, (w + 16) / 2, "#04162b", 0.9 * a)
    rrect(c, x - w / 2 - 8, top - 18, w + 16, h + 36, (w + 16) / 2, CYAN, 0.55 * a, stroke=3)
    c.save(); c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - w / 2, top - 10, w, h + 20), w / 2, w / 2), doAntiAlias=True)
    yl = ybot - pxm * clamp(level, 0, maxv * 1.02)
    water(c, x - w / 2, x + w / 2, yl, ybot + 20, t, a, amp=3, hl=True)
    c.restore()
    if ticks:
        v = 0
        while v <= maxv + 1e-6:
            yy = ybot - pxm * v
            line(c, x + w / 2 + 6, yy, x + w / 2 + 22, yy, "#cdefff", 3, 0.8 * a)
            if label_side == "l":
                T(c, f"{v:g}", x - w / 2 - 18, yy, 22, ts, "#cdefff", 0.8 * a, w=700, align="r", fam="Inter", shadow=0)
            v += step
    if readout:
        if rside == "r": C(c, readout, x + w / 2 + 36, yl, a, ts, size=30, bg=rcol, fg="#04162b", a=1, align="l")
        else: C(c, readout, x - w / 2 - 70, yl, a, ts, size=30, bg=rcol, fg="#04162b", a=1, align="r")

def snowflake(c, x, y, s, colr=ICE, a=1.0, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot)
    for k in range(6):
        c.rotate(60)
        line(c, 0, 0, 0, -s, colr, s * 0.1, a)
        line(c, 0, -s * 0.55, -s * 0.22, -s * 0.75, colr, s * 0.08, a); line(c, 0, -s * 0.55, s * 0.22, -s * 0.75, colr, s * 0.08, a)
    c.restore()

def droplet(c, x, y, s, colr="#3aa0e8", a=1.0):
    p = skia.Path(); p.moveTo(x, y - s)
    p.cubicTo(x + s * 0.25, y - s * 0.55, x + s * 0.7, y - s * 0.1, x + s * 0.7, y + s * 0.3)
    p.cubicTo(x + s * 0.7, y + s * 0.75, x + s * 0.35, y + s, x, y + s)
    p.cubicTo(x - s * 0.35, y + s, x - s * 0.7, y + s * 0.75, x - s * 0.7, y + s * 0.3)
    p.cubicTo(x - s * 0.7, y - s * 0.1, x - s * 0.25, y - s * 0.55, x, y - s); p.close()
    c.drawPath(p, paint(colr, a)); circle(c, x - s * 0.25, y + s * 0.25, s * 0.15, "#ffffff", 0.6 * a)

def pin(c, x, y, p, label, ts, dx=40, dy=-60, colr=CORAL, size=28, align="l", bg=CHIPBG, t=0.0, ring=True):
    if p <= 0: return
    a = clamp(p * 1.5)
    if ring:
        q = (t * 0.7) % 1
        circle(c, x, y, 14 + 34 * q, colr, a * (1 - q) * 0.9, stroke=3)
    lx, ly = x + dx, y + dy
    if abs(dx) + abs(dy) > 0: line(c, x, y, lx, ly, "#ffffff", 2.5, 0.75 * a)
    circle(c, x, y, 10, colr, a); circle(c, x, y, 10, "#ffffff", a, stroke=3)
    if label: C(c, label, lx, ly, p, ts, size=size, align=align, bg=bg)

# ------------------------------------------------------------------ custom globe (icy <-> green texture)
_TEX = {}
def _tex(kind):
    if kind in _TEX: return _TEX[kind]
    if kind == "icy":
        arr = geo.texture("earth")
    else:
        Wt, Ht = 2048, 1024
        surf = skia.Surface(Wt, Ht); cc = surf.getCanvas(); cc.clear(col("#1f6fd1"))
        p = paint("#4f9a5a")
        for poly_ in geo.land_polys("50m"):
            xs = (poly_[:, 0] + 180) / 360 * Wt; ys = (90 - poly_[:, 1]) / 180 * Ht
            path = skia.Path(); path.moveTo(xs[0], ys[0])
            for i in range(1, len(xs)): path.lineTo(xs[i], ys[i])
            path.close(); cc.drawPath(path, p)
        img = surf.makeImageSnapshot()
        arr = np.frombuffer(img.tobytes(), np.uint8).reshape(Ht, Wt, 4).copy()
        if img.imageInfo().colorType() == skia.kBGRA_8888_ColorType: arr = arr[:, :, [2, 1, 0, 3]]
        arr = np.ascontiguousarray(arr)
    _TEX[kind] = arr
    return arr

def globe2(c, x, y, R, rot, tilt=18, melt=0.0, a=1.0, light=(-0.75, 0.35, 0.55), glow=1.0):
    """textured globe; melt 0 = today's ice (white polar land), 1 = no ice on land (illustration)."""
    if R < 4 or a <= 0.003: return
    R = max(4, int(R) // 4 * 4)
    nx, ny, nz, alpha = geo._disk(R)
    tr = math.radians(tilt)
    y2 = ny * math.cos(tr) + nz * math.sin(tr); z2 = -ny * math.sin(tr) + nz * math.cos(tr)
    lat = np.arcsin(np.clip(y2, -1, 1)); lon = np.arctan2(nx, z2) + math.radians(rot)
    t1 = _tex("icy"); Ht, Wt = t1.shape[:2]
    mx = ((lon / (2 * math.pi) + 0.5) % 1.0 * Wt).astype(np.float32); my = ((0.5 - lat / math.pi) * Ht).astype(np.float32)
    out = cv2.remap(t1, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP)
    if melt > 0:
        o2 = cv2.remap(_tex("green"), mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP)
        out = (out.astype(np.float32) * (1 - melt) + o2.astype(np.float32) * melt).astype(np.uint8)
    L = np.array(light, np.float32); L /= np.linalg.norm(L)
    lam = np.clip(nx * L[0] + ny * L[1] + nz * L[2], 0, 1); shade = 0.25 + 0.75 * lam
    rgbf = out[:, :, :3].astype(np.float32) * shade[:, :, None]
    rim = np.clip((np.sqrt(nx * nx + ny * ny) - 0.82) / 0.18, 0, 1) ** 2
    rgbf = rgbf * (1 - 0.35 * rim[:, :, None]) + np.array([140, 200, 255], np.float32) * 0.35 * rim[:, :, None]
    al = (alpha * 255).astype(np.uint8)
    res = np.dstack([np.clip(rgbf, 0, 255).astype(np.uint8), al])
    res[:, :, :3] = (res[:, :, :3].astype(np.uint16) * al[:, :, None] // 255).astype(np.uint8)
    res = np.ascontiguousarray(res)
    if glow > 0: circle(c, x, y, R * 1.08, "#6fd0ff", 0.3 * glow * a, blur=R * 0.07)
    im = skia.Image.fromarray(res, colorType=skia.kRGBA_8888_ColorType, alphaType=skia.kPremul_AlphaType)
    pt = skia.Paint(); pt.setAlphaf(clamp(a))
    c.drawImageRect(im, skia.Rect.MakeXYWH(x - R, y - R, 2 * R, 2 * R), skia.SamplingOptions(skia.FilterMode.kLinear), pt)

def gxy(lon, lat, x, y, R, rot, tilt): return geo.globe_xy(lon, lat, x, y, R, rot, tilt)

def sea_ice(c, x, y, R, rot, tilt, lat0=76, a=1.0):
    pts = []
    for k in range(73):
        lon = k * 5; jitter = 1.6 * math.sin(k * 1.7) + 1.1 * math.sin(k * 0.6)
        px, py, vis_ = gxy(lon, lat0 + jitter * 0.6, x, y, R, rot, tilt)
        pts.append((px, py))
    p = poly(pts)
    c.drawPath(p, paint("#ffffff", 0.85 * a, blur=3)); c.drawPath(p, paint("#dff6ff", 0.6 * a, stroke=3))

# ------------------------------------------------------------------ title / card / end
def motif_i(c, W, H, t, S, cx, cy, s, period=7.0):
    u = S.u * s
    q = (t % period) / period; melt = ease(prog(q, 0.15, 0.5)) * (1 - ease(prog(q, 0.85, 0.15)))
    globe2(c, cx - 130 * u, cy, 230 * u, rot=-30 + t * 6, tilt=22, melt=melt)
    gauge(c, cx + 250 * u, cy + 230 * u, 6.4 * u, 70, 70 * melt, 1.0, step=70, w=60 * u, t=t, ticks=False)
    text(c, "+70 M", cx + 250 * u, cy - 268 * u, 40 * u, YEL, 0.4 + 0.6 * melt, w=900, shadow=8)

def bg_card(c, W, H, t, S): bg_ice(c, W, H, t, S)
def i5_title(c, W, H, t, S): kit.title(c, W, H, t, S, bg_card, motif_i, PAL)
def i5_card(c, W, H, t, S):
    def cbg(c, W, H, t, S):
        bg_ice(c, W, H, t, S)
        u = S.u; ybot = 0.98 * H
        lvl = 0.25 * H + 0.08 * H * math.sin(t * 0.8)
        water(c, 0, W, H - lvl, H + 10, t, 0.5, amp=10 * u)
    kit.card(c, W, H, t, S, cbg, PAL)
def i5_end(c, W, H, t, S): kit.end(c, W, H, t, S, bg_card, motif_i, PAL)
def i5_endshort(c, W, H, t, S): kit.end_short(c, W, H, t, S, bg_card, motif_i, PAL)

# ------------------------------------------------------------------ i5_city (hook)
BED_HOOK = [(0, 470), (180, 520), (380, 610), (560, 760), (760, 880), (980, 900), (1180, 790), (1380, 620), (1560, 470), (1740, 400), (1920, 380)]
TOP_HOOK = [(140, 440), (380, 250), (700, 160), (1000, 135), (1300, 160), (1600, 240), (1920, 300)]
SEA_Y = 470

def ice_section(c, ts, t, p_lbl, p_bed, a=1.0):
    water(c, 0, 1920, SEA_Y, 1080, t, a, amp=4)
    bed = BED_HOOK; top = TOP_HOOK
    ice_body(c, [(140, SEA_Y)] + top[1:], [(140, SEA_Y + 8)] + [q for q in bed if q[0] > 140], a)
    rock(c, bed, a=a)
    dashed_h(c, 0, 1920, SEA_Y, "#ffffff", 0.7 * F(t, p_lbl - 0.3), 3, t)
    C(c, "SEA LEVEL", 40, SEA_Y - 44, F(t, p_lbl), ts, size=26, align="l")
    C(c, "ANTARCTIC ICE SHEET", 1000, 230, F(t, p_lbl + 0.3), ts, size=34, bg="#0d3358", dot=CYAN)
    pb = F(t, p_bed)
    if pb > 0:
        line(c, 980, SEA_Y + 10, 980, 890, YEL, 5, pb); arrow(c, 980, 880, 980, 895, YEL, 5, pb)
        C(c, "GROUND: −2.5 KM", 1280, 840, pb, ts, size=34, bg=YEL, fg="#04162b", a=1)
    T(c, "SCHEMATIC", 1880, 1050, 20, ts, "#cdefff", 0.6 * a, w=700, align="r", fam="Inter", shadow=0)

BLDG = [(110, 150, 9), (280, 120, 14), (420, 160, 6), (600, 170, 20), (800, 130, 11), (950, 180, 16), (1160, 140, 8), (1320, 160, 13), (1500, 110, 18)]
def city(c, ts, t, level, a=1.0, hi=1.0):
    gy = 930; pxm = 8.0; fh = 3.2 * pxm
    rect(c, 0, gy, 1920, 150, "#0f2236", a)
    for i, (x, w, n) in enumerate(BLDG):
        h = n * fh; colr = "#16446b" if i != 3 else "#1d5a8a"
        rect(c, x, gy - h, w, h, colr, a)
        rng = random.Random(i)
        for f in range(n):
            for k in range(3):
                if rng.random() < 0.55:
                    rect(c, x + 16 + k * (w - 32) / 3, gy - h + f * fh + 7, (w - 32) / 3 - 10, fh - 13, "#ffd27a", a * 0.55)
    yl = gy - pxm * level
    water(c, 0, 1640, yl, 1080, t, a * clamp(level / 2), amp=6, alpha=0.78)
    x, w, n = BLDG[3]; h = n * fh
    if hi > 0:
        rrect(c, x - 6, gy - h - 6, w + 12, h + 12, 6, YEL, hi * a, stroke=5)
        C(c, "20 STOREYS", x + w / 2, gy - h - 60, hi, ts, size=30, bg=YEL, fg="#04162b", a=1)
    gauge(c, 1820, gy, pxm, 80, level, ts, a, step=10, t=t, readout=f"+{level:.0f} M" if level > 1 else None, rside="l")

def i5_city(c, W, H, t, S):
    o = S.opts; mode = o.get("mode", "intro")
    if mode == "short":
        def pS(c, ts):
            lv = 70 * ease(prog(t, S.lt(0, 0.15), S.dur * 0.65))
            city(c, ts, t, lv, hi=F(t, S.lt(0, 0.5)))
        run_panels(c, W, H, t, S, [(0, pS)]); return
    B = beats(S, 3)
    def pA(c, ts):
        z = 1 + 0.04 * prog(t, 0, B(1, 0))
        c.save(); c.translate(960, 540); c.scale(z, z); c.translate(-960, -540)
        ice_section(c, ts, t, B(0, 0.15), B(0, 0.55))
        c.restore()
    def pB(c, ts):
        lv = 70 * ease(prog(t, B(1, 0.15), max(0.5, B(1, 0.75) - B(1, 0.15))))
        city(c, ts, t, lv, hi=F(t, B(1, 0.7)))
        C(c, "ALL LAND ICE MELTS", 360, 110, F(t, B(1, 0.05)), ts, size=34, dot=CYAN)
    def pC(c, ts):
        gx, gy, R, rot, tilt = 700, 560, 400, 10 + (t - B(2, 0)) * 2, -5
        globe2(c, gx, gy, R, rot, tilt, melt=0.0)
        for k, (lon, lat, lab, dx, dy) in enumerate([(-42, 72, "GREENLAND", -380, -60), (10, 46.5, "THE ALPS", 340, -170),
                                                     (84, 29, "HIMALAYAS", 300, 40), (20, -76, "ANTARCTICA", 330, 90)]):
            x, y, v = gxy(lon, lat, gx, gy, R, rot, tilt)
            if v: pin(c, x, y, F(t, B(2, 0.05 + 0.12 * k)), lab, ts, dx=dx, dy=dy, colr=CYAN, align="c", t=t)
        T(c, "ALL OF IT?", 1560, 540, 120, ts, YEL, F(t, B(2, 0.55)), maxw=640)
    run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB), (B(2, 0), pC)])

# ------------------------------------------------------------------ i5_rules
def switch(c, x, y, s, on, ts, a=1.0):
    rrect(c, x - 120 * s, y - 230 * s, 240 * s, 460 * s, 50 * s, "#0a2440", a)
    rrect(c, x - 120 * s, y - 230 * s, 240 * s, 460 * s, 50 * s, CYAN, 0.6 * a, stroke=4)
    rrect(c, x - 40 * s, y - 170 * s, 80 * s, 340 * s, 40 * s, "#02101f", a)
    ky = lerp(-110, 110, eback(on)) * s
    circle(c, x, y + ky, 62 * s, mix(ICE, "#3aa0e8", on), a); circle(c, x, y + ky, 62 * s, "#ffffff", a, stroke=4)
    snowflake(c, x + 200 * s, y - 150 * s, 50 * s, ICE, a * (1 - 0.6 * on), rot=0)
    droplet(c, x + 200 * s, y + 150 * s, 50 * s, "#3aa0e8", a * (0.4 + 0.6 * on))
    T(c, "ICE", x + 300 * s, y - 150 * s, 44, ts, ICE, a, align="l", maxw=400)
    T(c, "WATER", x + 300 * s, y + 150 * s, 44, ts, "#7fc8ff", a, align="l", maxw=400)

def hourglass(c, x, y, s, t, a=1.0):
    q = (t * 0.15) % 1
    for sg in (-1, 1): rrect(c, x - 130 * s, y + sg * 210 * s - 14 * s, 260 * s, 28 * s, 10 * s, "#c9a46a", a)
    top = poly([(x - 100 * s, y - 195 * s), (x + 100 * s, y - 195 * s), (x + 12 * s, y), (x - 12 * s, y)])
    bot = poly([(x - 12 * s, y), (x + 12 * s, y), (x + 100 * s, y + 195 * s), (x - 100 * s, y + 195 * s)])
    c.drawPath(top, paint("#dff6ff", 0.12 * a)); c.drawPath(bot, paint("#dff6ff", 0.12 * a))
    c.save(); c.clipPath(top, doAntiAlias=True); rect(c, x - 110 * s, y - 195 * s + 160 * s * q, 220 * s, 200 * s, "#e9d29a", a); c.restore()
    c.save(); c.clipPath(bot, doAntiAlias=True); rect(c, x - 110 * s, y + 195 * s - 160 * s * q, 220 * s, 200 * s, "#e9d29a", a); c.restore()
    line(c, x, y, x, y + 190 * s, "#e9d29a", 4 * s, a)
    c.drawPath(top, paint("#dff6ff", 0.8 * a, stroke=4)); c.drawPath(bot, paint("#dff6ff", 0.8 * a, stroke=4))

def i5_rules(c, W, H, t, S):
    B = beats(S, 4)
    def pA(c, ts):
        on = prog(t, B(0, 0.22), 0.35)
        switch(c, 520, 560, 1.15, on, ts)
        if t > B(0, 0.22): circle(c, 520, 560, 60 + 600 * prog(t, B(0, 0.22), 0.8), "#ffffff", 0.5 * (1 - prog(t, B(0, 0.22), 0.8)), stroke=8)
        C(c, "EVERY BIT OF ICE ON LAND", 1060, 330, F(t, B(0, 0.1)), ts, size=34, align="l", dot=CYAN)
        C(c, "TURNS TO WATER, AT ONCE", 1060, 460, F(t, B(0, 0.3)), ts, size=34, align="l", dot="#3aa0e8")
        C(c, "IT ALL FLOWS INTO THE SEA", 1060, 590, F(t, B(0, 0.5)), ts, size=34, align="l", dot="#3aa0e8")
        C(c, "EVERYTHING ELSE: SAME", 1060, 720, F(t, B(0, 0.7)), ts, size=34, align="l", dot=YEL)
    def pB(c, ts):
        rot = (t - B(1, 0)) * 5
        globe2(c, 600, 560, 420, rot, tilt=-72)
        T(c, "ANTARCTICA", 1440, 220, 84, ts, ICE, F(t, B(1, 0.05)), maxw=760)
        C(c, "≈ 14 MILLION KM²", 1440, 400, F(t, B(1, 0.2)), ts, size=38)
        C(c, "≈ USA + MEXICO", 1440, 530, F(t, B(1, 0.4)), ts, size=38, bg="#13426b")
        C(c, "AVERAGE: 2+ KM THICK", 1440, 660, F(t, B(1, 0.7)), ts, size=38, bg=YEL, fg="#04162b", a=1)
    def pC(c, ts):
        rot = -42 + math.sin((t - B(2, 0)) * 0.4) * 6
        globe2(c, 600, 560, 420, rot, tilt=48)
        T(c, "GREENLAND", 1440, 200, 84, ts, ICE, F(t, B(2, 0.05)), maxw=760)
        C(c, "≈ 3 × TEXAS", 1440, 360, F(t, B(2, 0.15)), ts, size=38)
        C(c, "3+ KM THICK IN PLACES", 1440, 480, F(t, B(2, 0.3)), ts, size=38, bg="#13426b")
        pd = F(t, B(2, 0.55))
        if pd > 0:
            donut(c, 1300, 760, 110, 0.68 * pd, CYAN, a=pd)
            T(c, "68%+", 1300, 760, 56, 1.0, "#ffffff", pd)
            T(c, "OF EARTH'S", 1430, 735, 32, ts, "#cdefff", pd, w=800, align="l", fam="Inter", maxw=440)
            T(c, "FRESH WATER", 1430, 790, 40, ts, "#ffffff", pd, w=900, align="l", maxw=440)
    def pD(c, ts):
        hourglass(c, 470, 560, 1.2, t)
        C(c, "REAL WORLD: THOUSANDS OF YEARS", 1250, 330, F(t, B(3, 0.05)), ts, size=34)
        on = prog(t, B(3, 0.6), 0.35)
        switch(c, 1180, 700, 0.7, on, ts)
        if on > 0: T(c, "FLIP!", 1560, 700, 110, ts, YEL, F(t, B(3, 0.62)), maxw=420)
    run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB), (B(2, 0), pC), (B(3, 0), pD)])

# ------------------------------------------------------------------ i5_budget
def person_icon(c, x, y, h, colr="#e8eef8", a=1.0):
    circle(c, x, y - h * 0.9, h * 0.085, colr, a)
    rrect(c, x - h * 0.1, y - h * 0.8, h * 0.2, h * 0.42, h * 0.08, colr, a)
    line(c, x - h * 0.05, y - h * 0.4, x - h * 0.06, y, colr, h * 0.07, a); line(c, x + h * 0.05, y - h * 0.4, x + h * 0.06, y, colr, h * 0.07, a)
    line(c, x - h * 0.1, y - h * 0.75, x - h * 0.2, y - h * 0.45, colr, h * 0.06, a); line(c, x + h * 0.1, y - h * 0.75, x + h * 0.2, y - h * 0.45, colr, h * 0.06, a)

def mountains(c, x, y, s, a=1.0):
    for dx, hh, col_ in ((-60, 110, "#8796a8"), (30, 150, "#a3b2c4"), (110, 90, "#7a889a")):
        c.drawPath(poly([(x + dx * s - 80 * s, y), (x + dx * s, y - hh * s), (x + dx * s + 80 * s, y)]), paint(col_, a))
        c.drawPath(poly([(x + dx * s - 28 * s, y - hh * s * 0.65), (x + dx * s, y - hh * s), (x + dx * s + 28 * s, y - hh * s * 0.65)]), paint("#ffffff", a))

def i5_budget(c, W, H, t, S):
    B = beats(S, 4)
    def pA(c, ts):
        pxm = 11.5; ybot = 960
        a1 = 58 * ease(prog(t, B(0, 0.25), max(0.4, B(0, 0.95) - B(0, 0.25))))
        a2 = 7.4 * ease(prog(t, B(1, 0.1), 1.2)); a3 = 0.32 * ease(prog(t, B(2, 0.3), 1.0))
        lv = a1 + a2 + a3
        # 20-storey building next to the gauge (3.2 m per storey)
        bx, bw = 470, 120; bh = 64 * pxm
        rect(c, bx, ybot - bh, bw, bh, "#16446b", 0.9);
        for f in range(20): line(c, bx + 8, ybot - f * 3.2 * pxm, bx + bw - 8, ybot - f * 3.2 * pxm, "#2a6a9a", 2)
        T(c, "20 STOREYS", bx + bw / 2, ybot - bh - 30, 22, ts, "#cdefff", 0.8, w=800, fam="Inter", shadow=0)
        gauge(c, 300, ybot, pxm, 70, lv, ts, 1.0, step=10, t=t, readout=None, w=80)
        # segment brackets
        def seg(v0, v1, colr, lab, p):
            if p <= 0: return
            y0, y1 = ybot - pxm * v0, ybot - pxm * v1
            line(c, 360, y0 - 2, 360, y1 + 2, colr, 8, p)
        seg(0, a1, CYAN, "", F(t, B(0, 0.25)))
        seg(58, 58 + a2, "#c9f1ff", "", F(t, B(1, 0.1)))
        rows = [(250, "ANTARCTICA", f"{a1:.0f} M", B(0, 0.1), CYAN), (450, "GREENLAND", f"+{a2:.1f} M", B(1, 0.05), "#c9f1ff"),
                (650, "ALL OTHER GLACIERS", f"+{a3:.2f} M", B(2, 0.05), "#ffffff")]
        for y, lab, val, t0, colr in rows:
            p = F(t, t0)
            T(c, lab, 760, y, 54, ts, colr, p, align="l", maxw=530)
            T(c, val, 1340, y, 72, ts, YEL, p, align="l", maxw=360)
        mountains(c, 860, 760, 0.55, F(t, B(2, 0.2)))
        pk = F(t, B(2, 0.6))
        if pk > 0:
            px, py = 1790, 700; ph = 140
            person_icon(c, px, py, ph, a=pk)
            water(c, px - 90, px + 90, py - ph * 0.17, py + 6, t, pk, amp=2, alpha=0.8)
            T(c, "NOT EVEN KNEE-DEEP", 1900, py + 48, 26, ts, "#cdefff", pk, w=800, fam="Inter", shadow=0, maxw=520, align="r")
        pt_ = F(t, B(3, 0.1))
        if pt_ > 0:
            rrect(c, 700, 830, 1100, 190, 30, "#04162b", 0.9 * pt_); rrect(c, 700, 830, 1100, 190, 30, YEL, pt_, stroke=4)
            T(c, "≈ 66 M", 930, 925, 96, ts, YEL, pt_, maxw=440)
            C(c, "USGS: ABOUT 70 M", 1440, 925, F(t, B(3, 0.4)), ts, size=36, bg=YEL, fg="#04162b", a=1)
    run_panels(c, W, H, t, S, [(0, pA)])

# ------------------------------------------------------------------ i5_seaice
def glass(c, cx, ybot, w, h, a=1.0):
    rrect(c, cx - w / 2, ybot - h, w, h, 20, "#ffffff", 0.05 * a)
    p = skia.Path(); p.moveTo(cx - w / 2, ybot - h); p.lineTo(cx - w / 2 + 8, ybot - 20)
    p.quadTo(cx - w / 2 + 10, ybot, cx - w / 2 + 34, ybot); p.lineTo(cx + w / 2 - 34, ybot)
    p.quadTo(cx + w / 2 - 10, ybot, cx + w / 2 - 8, ybot - 20); p.lineTo(cx + w / 2, ybot - h)
    c.drawPath(p, paint("#dff6ff", 0.85 * a, stroke=6))

def cube(c, x, y, s, a=1.0, rot=8):
    if s <= 1: return
    c.save(); c.translate(x, y); c.rotate(rot)
    rrect(c, -s / 2, -s / 2, s, s, s * 0.14, "#f4fcff", a); rrect(c, -s / 2, -s / 2, s, s, s * 0.14, "#9fdcff", a, stroke=4)
    rrect(c, -s * 0.32, -s * 0.36, s * 0.26, s * 0.12, s * 0.06, "#ffffff", a)
    c.restore()

def glass_scene(c, ts, t, cx, ybot, mode, melt, a=1.0, title=None, t_lab=0.0):
    w, h = 420, 520; inner0, inner1 = cx - w / 2 + 12, cx + w / 2 - 12
    lvl0 = ybot - 270
    if mode == "float":
        rise = 3 * melt  # tiny (~3 %)
        s = 150 * (1 - melt) ** 0.7
        cube(c, cx, lvl0 - rise - s * 0.5 + s * 0.88, s, a)
        water(c, inner0, inner1, lvl0 - rise, ybot - 6, t, a, amp=3, alpha=0.75)
    else:
        rise = 120 * melt
        rect(c, cx - 70, lvl0 - 60, 140, ybot - lvl0 + 54, "#6a574c", a); rect(c, cx - 70, lvl0 - 60, 140, 12, "#8e7869", a)
        s = 150 * (1 - melt) ** 0.7
        cube(c, cx, lvl0 - 60 - s / 2 + 4, s, a, rot=0)
        water(c, inner0, inner1, lvl0 - rise, ybot - 6, t, a, amp=3, alpha=0.75)
        if melt > 0.02 and melt < 0.98:
            for k in range(3): droplet(c, cx - 50 + k * 50, lvl0 - 40 + ((t * 120 + k * 40) % 60), 9, "#7fc8ff", a)
    dashed_h(c, cx - w / 2 - 30, cx + w / 2 + 30, lvl0, YEL, 0.9 * a, 3, t)
    glass(c, cx, ybot, w, h, a)
    if title: C(c, title, cx, ybot - h - 60, F(t, t_lab), ts, size=34)

def i5_seaice(c, W, H, t, S):
    B = beats(S, 4)
    def polar(c, ts, melt, t_lab):
        R, rot, tilt = 400, 30 + t * 3, 78
        geo.globe(c, 640, 560, R, rot, tilt)
        sea_ice(c, 640, 560, R, rot, tilt, 77, a=1 - melt)
        T(c, "SEA ICE (APPROX.)", 640, 1020, 26, ts, "#cdefff", 0.8, w=700, fam="Inter", shadow=0)
        return t_lab
    def pA(c, ts):
        polar(c, ts, 0.0, 0)
        T(c, "THE NORTH POLE?", 1420, 420, 80, ts, ICE, F(t, B(0, 0.1)), maxw=820)
        C(c, "FLOATING SEA ICE", 1420, 580, F(t, B(0, 0.4)), ts, size=38, dot=CYAN)
    def pB(c, ts):
        m = ease(prog(t, B(1, 0.35), max(0.6, B(1, 0.95) - B(1, 0.35))))
        glass_scene(c, ts, t, 620, 900, "float", m, title="FLOATING ICE", t_lab=B(1, 0.0))
        C(c, "PUSHES ASIDE ITS OWN WEIGHT", 1360, 420, F(t, B(1, 0.15)), ts, size=34)
        pk = F(t, B(1, 0.8))
        check(c, 1150, 600, 40, pk); T(c, "LEVEL: ALMOST THE SAME", 1210, 600, 46, ts, "#7ee0a0", pk, align="l", maxw=680)
    def pC(c, ts):
        m = ease(prog(t, B(2, 0.2), 2.0))
        glass_scene(c, ts, t, 480, 900, "float", 1.0, title="FLOATING", t_lab=B(2, 0))
        glass_scene(c, ts, t, 1080, 900, "land", m, title="ON LAND", t_lab=B(2, 0.05))
        p = F(t, B(2, 0.45))
        bar(c, 1340, 420, 340, 44, 0.03 * p + 0.004, CYAN, 1.0, label="FLOATING", val="≈ 3%", a=p)
        bar(c, 1340, 620, 340, 44, 1.0 * p, CORAL, 1.0, label="SAME ICE ON LAND", val="100%", a=p)
        T(c, "NASA ESTIMATE", 1340, 740, 24, ts, "#cdefff", 0.8 * p, w=700, align="l", fam="Inter", shadow=0)
    def pD(c, ts):
        m = ease(prog(t, B(3, 0.05), max(0.5, B(3, 0.55) - B(3, 0.05))))
        polar(c, ts, m, 0)
        C(c, "ARCTIC ICE GONE", 1420, 340, F(t, B(3, 0.1)), ts, size=38)
        C(c, "SEA LEVEL: BARELY CHANGES", 1420, 470, F(t, B(3, 0.35)), ts, size=34, bg="#13426b")
        C(c, "DANGER: ICE ON ROCK", 1420, 640, F(t, B(3, 0.65)), ts, size=40, bg=CORAL, fg="#ffffff", a=1)
    run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB), (B(2, 0), pC), (B(3, 0), pD)])

# ------------------------------------------------------------------ i5_map (real coastlines, labelled markers only)
def map_frame(c, rect, a=1.0):
    X, Y, Wd, Hd = rect
    rrect(c, X - 4, Y - 4, Wd + 8, Hd + 8, 14, CYAN, 0.6 * a, stroke=4)

def draw_base(c, bbox, rect, a=1.0, glow_coast=0.0):
    geo.draw_map(c, bbox, rect, land=LAND, sea=SEA, outline="#021022", outline_w=2)
    if glow_coast > 0:
        c.save(); c.clipRect(skia.Rect.MakeXYWH(*rect))
        c.drawPath(geo.land_path(bbox, rect), paint(CYAN, 0.8 * glow_coast, stroke=5, blur=3))
        c.restore()
    map_frame(c, rect, a)

def region(c, bbox, rect, lon, lat, rx, ry, p, label, ts, dx=0, dy=-90, rot=0, t=0.0, colr=CYAN, size=28, align="c"):
    if p <= 0: return
    x, y = geo.lonlat_xy(lon, lat, bbox, rect)
    sx = rect[2] / (bbox[2] - bbox[0]); sy = rect[3] / (bbox[3] - bbox[1])
    a = clamp(p * 1.5); pul = 1 + 0.04 * math.sin(t * 3)
    c.save(); c.translate(x, y); c.rotate(rot)
    oval(c, 0, 0, rx * sx * pul, ry * sy * pul, colr, 0.2 * a)
    c.drawOval(skia.Rect.MakeLTRB(-rx * sx * pul, -ry * sy * pul, rx * sx * pul, ry * sy * pul), paint(colr, a, stroke=4, dash=([14, 10], -t * 25)))
    c.restore()
    if label:
        if abs(dx) + abs(dy) > 0: line(c, x, y, x + dx, y + dy, "#ffffff", 2.5, 0.75 * a)
        C(c, label, x + dx, y + dy, p, ts, size=size, align=align)

def city_pin(c, bbox, rect, lon, lat, p, label, ts, dx=40, dy=-60, t=0.0, align="l", colr=CORAL, size=28):
    x, y = geo.lonlat_xy(lon, lat, bbox, rect)
    pin(c, x, y, p, label, ts, dx=dx, dy=dy, colr=colr, size=size, align=align, t=t)

def side_gauge(c, ts, t, x=1820, a=1.0):
    gauge(c, x, 960, 10.5, 70, 70, ts, a, step=70, t=t, readout=None, w=56, ticks=False)
    T(c, "+70 M", x, 120, 40, ts, YEL, a, maxw=200)

def i5_map(c, W, H, t, S):
    mode = S.opts.get("mode", "americas")
    if mode == "americas":
        B = beats(S, 4)
        bbN = (-126, 22, -64, 50); rN = geo.map_rect(bbN, 870, 545, width=1560)
        bbS = (-84, -42, -32, 10); rS = geo.map_rect(bbS, 640, 545, height=930)
        def pN(c, ts):
            draw_base(c, bbN, rN)
            side_gauge(c, ts, t)
            C(c, "SOURCE: NATIONAL GEOGRAPHIC", rN[0] + 30, rN[1] + 50, F(t, B(0, 0.3)), ts, size=26, align="l")
            region(c, bbN, rN, -81.5, 28.0, 2.6, 3.4, F(t, B(1, 0.05)), "FLORIDA", ts, dx=200, dy=60, t=t)
            region(c, bbN, rN, -91.5, 29.9, 5.5, 1.4, F(t, B(1, 0.2)), "GULF COAST", ts, dx=-60, dy=110, t=t)
            path = [(-81.2, 31.5), (-78.5, 34), (-76.2, 36.5), (-75.2, 38.6), (-74.0, 40.4), (-71.5, 41.3), (-70.5, 42.6)]
            pp = F(t, B(1, 0.3))
            if pp > 0:
                pts = [geo.lonlat_xy(lo, la, bbN, rN) for lo, la in path]
                c.drawPath(spline(pts), paint(CYAN, pp, stroke=10, dash=([18, 12], -t * 25)))
                C(c, "ATLANTIC SEABOARD", pts[2][0] + 90, pts[2][1] + 20, pp, ts, size=28, align="l")
            city_pin(c, bbN, rN, -80.19, 25.76, F(t, B(1, 0.4)), "MIAMI: GONE", ts, dx=110, dy=50, t=t)
            city_pin(c, bbN, rN, -74.0, 40.71, F(t, B(1, 0.65)), "NEW YORK", ts, dx=-280, dy=-70, t=t)
            city_pin(c, bbN, rN, -71.06, 42.36, F(t, B(1, 0.75)), "BOSTON", ts, dx=-150, dy=-110, t=t)
            city_pin(c, bbN, rN, -122.42, 37.77, F(t, B(2, 0.05)), "SAN FRANCISCO: HILLS → ISLANDS", ts, dx=60, dy=-170, t=t)
            region(c, bbN, rN, -120.6, 37.4, 1.4, 3.3, F(t, B(2, 0.45)), "CENTRAL VALLEY → BAY", ts, dx=300, dy=90, rot=-32, t=t)
        def pS(c, ts):
            draw_base(c, bbS, rS)
            side_gauge(c, ts, t)
            region(c, bbS, rS, -60, -3.5, 11, 4.5, F(t, B(3, 0.1)), "AMAZON BASIN → ATLANTIC INLET", ts, dx=520, dy=-130, t=t, align="c")
            city_pin(c, bbS, rS, -58.38, -34.6, F(t, B(3, 0.6)), "BUENOS AIRES", ts, dx=160, dy=40, t=t)
        run_panels(c, W, H, t, S, [(0, pN), (B(3, 0), pS)])
    elif mode == "europe":
        B = beats(S, 2)
        bb = (-11, 28, 34, 60); r = geo.map_rect(bb, 720, 545, height=950)
        def pE(c, ts):
            draw_base(c, bb, r)
            side_gauge(c, ts, t)
            city_pin(c, bb, r, -0.13, 51.51, F(t, B(0, 0.08)), "LONDON", ts, dx=-250, dy=-40, t=t)
            city_pin(c, bb, r, 12.33, 45.44, F(t, B(0, 0.28)), "VENICE", ts, dx=90, dy=70, t=t)
            region(c, bb, r, 5.4, 52.3, 1.7, 1.3, F(t, B(0, 0.5)), "NETHERLANDS", ts, dx=-40, dy=-150, t=t)
            region(c, bb, r, 9.6, 56.0, 2.3, 1.6, F(t, B(0, 0.7)), "MOST OF DENMARK", ts, dx=120, dy=-110, t=t)
            city_pin(c, bb, r, 29.92, 31.2, F(t, B(1, 0.2)), "ALEXANDRIA", ts, dx=-330, dy=-70, t=t)
            city_pin(c, bb, r, 31.24, 30.04, F(t, B(1, 0.45)), "CAIRO: 150+ KM INLAND", ts, dx=-90, dy=60, t=t, align="r")
        run_panels(c, W, H, t, S, [(0, pE)])
    elif mode == "asia":
        B = beats(S, 3)
        bb = (66, 4, 126, 42); r = geo.map_rect(bb, 860, 545, width=1400)
        bbA = (-20, -37, 55, 38); rA = geo.map_rect(bbA, 760, 545, height=950)
        def pA(c, ts):
            draw_base(c, bb, r)
            side_gauge(c, ts, t)
            region(c, bb, r, 90.3, 23.6, 2.2, 2.6, F(t, B(0, 0.05)), "BANGLADESH: NEARLY ALL", ts, dx=-40, dy=-180, t=t)
            for path in ([(72.8, 21.5), (73.0, 18.5), (74.0, 15.0), (75.5, 11.5), (77.5, 8.3)], [(80.3, 13.3), (81.5, 16.3), (84.5, 19.0), (87.0, 21.3)]):
                pp = F(t, B(0, 0.3))
                if pp > 0:
                    pts = [geo.lonlat_xy(lo, la, bb, r) for lo, la in path]
                    c.drawPath(spline(pts), paint(CYAN, pp, stroke=10, dash=([18, 12], -t * 25)))
            x0, y0 = geo.lonlat_xy(74.2, 14.5, bb, r)
            C(c, "INDIA'S COAST", x0 - 120, y0 + 120, F(t, B(0, 0.3)), ts, size=28)
            region(c, bb, r, 116.5, 31.5, 4.5, 6.0, F(t, B(0, 0.6)), "CHINA: LAND HOME TO ~600 MILLION", ts, dx=-330, dy=-230, t=t)
            city_pin(c, bb, r, 121.47, 31.23, F(t, B(1, 0.05)), "SHANGHAI", ts, dx=-30, dy=170, t=t, align="r")
            C(c, "SUNK 3+ M SINCE THE 1800s", r[0] + r[2] - 40, r[1] + r[3] - 160, F(t, B(1, 0.3)), ts, size=28, align="r", bg="#13426b")
            C(c, "SEAWALLS: 5–7 M", r[0] + r[2] - 40, r[1] + r[3] - 60, F(t, B(1, 0.6)), ts, size=28, align="r", bg=YEL, fg="#04162b", a=1)
        def pAf(c, ts):
            draw_base(c, bbA, rA, glow_coast=0.6 + 0.3 * math.sin(t * 3))
            side_gauge(c, ts, t)
            C(c, "AFRICA", 1460, 360, F(t, B(2, 0.05)), ts, size=44)
            C(c, "LOSES LESS LAND", 1460, 500, F(t, B(2, 0.25)), ts, size=36, bg="#13426b")
            C(c, "THAN MOST CONTINENTS", 1460, 600, F(t, B(2, 0.35)), ts, size=36, bg="#13426b")
            C(c, "BUT ITS COASTS SHRINK", 1460, 760, F(t, B(2, 0.65)), ts, size=36, bg=CORAL, fg="#ffffff", a=1)
        run_panels(c, W, H, t, S, [(0, pA), (B(2, 0), pAf)])
    else:  # world (teaser): one fixed map, camera glides Europe -> Florida -> Bangladesh
        bb = (-140, -8, 145, 74); r = geo.map_rect(bb, 960, 540, width=2630)
        L0 = S.lt(0, 0); L1 = S.lt(0, 1)
        def fr(f): return L0 + (L1 - L0) * f
        def pW(c, ts):
            cams = [(5, 50, 3.0), (-81, 28, 2.6), (90, 23.5, 2.6)]
            ks = [fr(0.0), fr(0.42), fr(0.72)]
            if t < ks[1] - 0.6: cam = cams[0]
            elif t < ks[1]:
                q = ease(prog(t, ks[1] - 0.6, 0.6)); cam = tuple(lerp(cams[0][i], cams[1][i], q) for i in range(3))
            elif t < ks[2] - 0.6: cam = cams[1]
            elif t < ks[2]:
                q = ease(prog(t, ks[2] - 0.6, 0.6)); cam = tuple(lerp(cams[1][i], cams[2][i], q) for i in range(3))
            else: cam = cams[2]
            px, py = geo.lonlat_xy(cam[0], cam[1], bb, r); z = cam[2]
            c.save(); c.clipRect(skia.Rect.MakeXYWH(20, 20, 1880, 1040)); c.translate(960, 540); c.scale(z, z); c.translate(-px, -py)
            geo.draw_map(c, bb, r, land=LAND, sea=SEA, outline="#021022", outline_w=1.0)
            k = 1 / z
            def cp(lon, lat, p, lab, dx, dy, align="l"):
                x, y = geo.lonlat_xy(lon, lat, bb, r)
                c.save(); c.translate(x, y); c.scale(k, k); pin(c, 0, 0, p, lab, ts, dx=dx, dy=dy, t=t, align=align); c.restore()
            def rg(lon, lat, rx, ry, p, lab, dx, dy):
                x, y = geo.lonlat_xy(lon, lat, bb, r)
                sx = r[2] / (bb[2] - bb[0]); sy = r[3] / (bb[3] - bb[1])
                if p <= 0: return
                oval(c, x, y, rx * sx, ry * sy, CYAN, 0.22 * p)
                c.drawOval(skia.Rect.MakeLTRB(x - rx * sx, y - ry * sy, x + rx * sx, y + ry * sy), paint(CYAN, p, stroke=3 * k, dash=([10 * k, 7 * k], 0)))
                c.save(); c.translate(x, y); c.scale(k, k); C(c, lab, dx, dy, p, ts, size=30); c.restore()
            cp(-0.13, 51.51, F(t, fr(0.0)), "LONDON", -330, -60)
            cp(12.33, 45.44, F(t, fr(0.1)), "VENICE", 60, 120)
            rg(5.4, 52.3, 1.7, 1.3, F(t, fr(0.2)), "NETHERLANDS", 120, -230)
            rg(-81.5, 28.0, 2.6, 3.4, F(t, fr(0.45)), "FLORIDA", 330, -120)
            rg(90.3, 23.6, 2.2, 2.6, F(t, fr(0.75)), "BANGLADESH", 0, -260)
            c.restore()
            map_frame(c, (20, 20, 1880, 1040))
            C(c, "SEA LEVEL +70 M", 60, 90, 1.0, ts, size=30, align="l", bg=YEL, fg="#04162b", a=1)
        run_panels(c, W, H, t, S, [(0, pW)])

# ------------------------------------------------------------------ i5_albedo
def sunray_scene(c, ts, t, kind, a=1.0):
    gy = 760
    if kind == "ice":
        fill_under(c, [(0, gy), (480, gy - 20), (960, gy + 10), (1440, gy - 15), (1920, gy)], 1080, [(0, "#ffffff", 1), (1, "#9fdcff", 1)])
    else:
        water(c, 0, 1920, gy, 1080, t, 1.0, amp=8, top="#0b4a7d", bot="#021530")
    sun(c, 260, 180, 80, t)
    for k in range(10):
        x1 = 520 + k * 120; y1 = gy - 5
        q = ((t * 0.45 + k * 0.137) % 1)
        reflect = (kind == "ice" and k != 4) or (kind != "ice" and k == 6)
        if q < 0.5:
            f = q / 0.5; sx, sy = 330, 240
            x, y = lerp(sx, x1, f), lerp(sy, y1, f)
            arrow(c, lerp(sx, x1, max(0, f - 0.25)), lerp(sy, y1, max(0, f - 0.25)), x, y, YEL, 7, a)
        else:
            f = (q - 0.5) / 0.5
            if reflect:
                x2, y2 = x1 + 260, gy - 520
                x, y = lerp(x1, x2, f), lerp(y1, y2, f)
                arrow(c, lerp(x1, x2, max(0, f - 0.25)), lerp(y1, y2, max(0, f - 0.25)), x, y, "#ffffff", 7, a * (1 - f * 0.6))
            else:
                circle(c, x1, y1 + 30 + 60 * f, 22 * (1 - f) + 6, "#ff9a3c", a * (1 - f) * 0.8, blur=10)

def i5_albedo(c, W, H, t, S):
    B = beats(S, 4)
    def pA(c, ts):
        sunray_scene(c, ts, t, "ice")
        T(c, "≈ 90%", 1540, 300, 150, ts, ICE, F(t, B(0, 0.4)), maxw=600)
        T(c, "REFLECTED BY FRESH SNOW", 1540, 420, 36, ts, "#ffffff", F(t, B(0, 0.5)), maxw=700)
    def pB(c, ts):
        sunray_scene(c, ts, t, "ocean")
        T(c, "< 10%", 1540, 300, 150, ts, "#7fc8ff", F(t, B(1, 0.3)), maxw=600)
        T(c, "REFLECTED BY OPEN OCEAN", 1540, 420, 36, ts, "#ffffff", F(t, B(1, 0.4)), maxw=700)
        C(c, "THE REST IS ABSORBED", 1540, 540, F(t, B(1, 0.6)), ts, size=34, bg=CORAL, fg="#ffffff", a=1)
    def pC(c, ts):
        cx, cy, R = 960, 560, 300
        T(c, "ICE-ALBEDO FEEDBACK", 960, 110, 64, ts, YEL, F(t, B(2, 0.5)), maxw=1400)
        nodes = ["LESS ICE", "DARKER SURFACE", "MORE SUNLIGHT ABSORBED", "WARMER"]
        rot = (t - B(2, 0)) * 25
        for k in range(4):
            an = math.radians(-90 + k * 90); an2 = math.radians(-90 + (k + 1) * 90)
            pa = F(t, B(2, 0.1 + 0.12 * k))
            p = skia.Path(); p.addArc(skia.Rect.MakeXYWH(cx - R, cy - R, 2 * R, 2 * R), -90 + k * 90 + 22, 46)
            c.drawPath(p, paint(CYAN, pa, stroke=10))
            ex, ey = cx + math.cos(math.radians(-90 + k * 90 + 68)) * R, cy + math.sin(math.radians(-90 + k * 90 + 68)) * R
            tx, ty = cx + math.cos(math.radians(-90 + k * 90 + 72)) * R, cy + math.sin(math.radians(-90 + k * 90 + 72)) * R
            arrow(c, ex, ey, tx, ty, CYAN, 10, pa, head=36)
        for k, nm in enumerate(nodes):
            an = math.radians(-90 + k * 90)
            C(c, nm, cx + math.cos(an) * R, cy + math.sin(an) * R, F(t, B(2, 0.05 + 0.12 * k)), ts, size=34, bg="#0d3358" if k else "#13426b")
        circle(c, cx + math.cos(math.radians(rot)) * R * 0.55, cy + math.sin(math.radians(rot)) * R * 0.55, 14, YEL, F(t, B(2, 0.5)))
    def pD(c, ts):
        p1 = F(t, B(3, 0.55)); temp = lerp(14, 27, ease(prog(t, B(3, 0.3), 2.0)))
        thermometer(c, 560, 520, 520, 14, tmax=32, tmin=-5, label=False)
        thermometer(c, 1160, 520, 520, temp, tmax=32, tmin=-5, label=False)
        T(c, "TODAY ≈ 14 °C", 640, 975, 44, ts, "#ffffff", F(t, B(3, 0.7)), align="c", maxw=520)
        T(c, f"ICE-FREE WORLD ≈ {temp:.0f} °C", 1250, 975, 44, ts, CORAL, F(t, B(3, 0.25)), align="c", maxw=620)
        C(c, "ESTIMATE: NATIONAL GEOGRAPHIC", 1500, 200, F(t, B(3, 0.35)), ts, size=26)
    run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB), (B(2, 0), pC), (B(3, 0), pD)])

# ------------------------------------------------------------------ i5_currents (one continuous panel)
CUR_PATH = [(470, 440), (560, 560), (680, 720), (820, 790), (1100, 800), (1500, 795), (1920, 790)]
RET_PATH = [(1920, 470), (1400, 470), (900, 465), (520, 452)]
def along(pts, f):
    seg = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]; L = sum(seg); d = f * L
    for i, s in enumerate(seg):
        if d <= s: q = d / s; return (lerp(pts[i][0], pts[i + 1][0], q), lerp(pts[i][1], pts[i + 1][1], q))
        d -= s
    return pts[-1]

def i5_currents(c, W, H, t, S):
    B = beats(S, 3)
    def pA(c, ts):
        water(c, 0, 1920, 430, 1080, t, 1.0, amp=4, top="#1b6aa8", bot="#031a33")
        rock(c, [(0, 470), (250, 480), (420, 520), (560, 600), (700, 760), (820, 830), (1200, 840), (1600, 830), (1920, 845)])
        ice_body(c, [(0, 200), (180, 220), (330, 300), (440, 420), (470, 445)], [(0, 470), (250, 480), (420, 520), (470, 530)])
        T(c, "ANTARCTICA", 180, 150, 40, ts, ICE, F(t, B(0, 0.05)), maxw=420)
        fresh = ease(prog(t, B(1, 0.1), 3.0))
        if fresh > 0:
            wfr = 1450 * fresh
            rrect(c, 460, 425, wfr, 36, 18, "#bff3ff", 0.75)
            C(c, "FRESH MELTWATER: LIGHTER", 460 + max(320, wfr / 2), 380, F(t, B(1, 0.2)), ts, size=30, bg="#13426b")
        stall = clamp(0.6 * ease(prog(t, B(1, 0.3), 2.5)) + 0.4 * ease(prog(t, B(2, 0.0), 2.5)))
        flow_a = 1 - 0.7 * stall
        for k in range(16):
            f = ((t * 0.035 * (1 - 0.85 * stall) + k / 16) % 1)
            x, y = along(CUR_PATH, f)
            circle(c, x, y, 11, "#5fc0ff", 0.9 * flow_a, blur=2); circle(c, x, y, 5, "#ffffff", 0.9 * flow_a)
        for k in range(10):
            f = ((t * 0.04 * (1 - 0.85 * stall) + k / 10) % 1)
            x, y = along(RET_PATH, f)
            circle(c, x, y, 8, "#ffcf7a", 0.7 * flow_a)
        pl = F(t, B(0, 0.35))
        if pl > 0:
            arrow(c, 560, 520, 700, 700, "#5fc0ff", 9, pl * flow_a, head=34)
            hide = 1 - F(t, B(2, 0.3))
            C(c, "COLD, SALTY WATER SINKS", 900, 600, pl * hide, ts, size=30, align="l")
            C(c, "DEEP CURRENT", 1500, 730, F(t, B(0, 0.6)) * hide, ts, size=30, bg="#0d3358")
        C(c, "−40% BY 2050 (ONE MODEL, HIGH EMISSIONS)", 1200, 220, F(t, B(1, 0.55)) * (1 - F(t, B(2, 0.5))), ts, size=30, bg=YEL, fg="#04162b", a=1)
        pn = F(t, B(2, 0.35))
        if pn > 0:
            rng = random.Random(3)
            for k in range(40):
                x = rng.uniform(900, 1880); y = 815 - rng.uniform(0, 30) * pn
                circle(c, x, y, rng.uniform(4, 8), GREENC, 0.8 * pn)
            C(c, "NUTRIENTS STUCK IN THE DEEP", 1420, 660, pn, ts, size=30, bg="#13426b")
            for k in range(14):
                x = 700 + k * 85; circle(c, x, 495 + math.sin(t + k) * 6, 7, GREENC, 0.8 * (1 - 0.7 * pn))
            C(c, "LESS FOR SURFACE LIFE", 1200, 220, F(t, B(2, 0.7)), ts, size=30, bg=CORAL, fg="#ffffff", a=1)
    run_panels(c, W, H, t, S, [(0, pA)])

# ------------------------------------------------------------------ i5_spin
def skater(c, x, y, s, arms, t, spin_speed, a=1.0):
    ph = t * spin_speed
    for k in range(3):
        q = (ph * 0.25 + k / 3) % 1
        p = skia.Path(); p.addArc(skia.Rect.MakeXYWH(x - 260 * s, y - 120 * s, 520 * s, 120 * s), 200 + q * 360, 60)
        c.drawPath(p, paint(CYAN, a * 0.7, stroke=5 * s))
    circle(c, x, y - 300 * s, 34 * s, ICE, a)
    rrect(c, x - 30 * s, y - 260 * s, 60 * s, 170 * s, 26 * s, ICE, a)
    line(c, x - 14 * s, y - 95 * s, x - 22 * s, y + 60 * s, ICE, 18 * s, a); line(c, x + 14 * s, y - 95 * s, x + 30 * s, y + 60 * s, ICE, 18 * s, a)
    sw = math.cos(ph) ; ext = lerp(60, 230, arms)
    for sg in (-1, 1):
        ex = x + sg * ext * s * (0.55 + 0.45 * abs(sw)); ey = y - 230 * s + (1 - arms) * 90 * s
        line(c, x + sg * 22 * s, y - 230 * s, ex, ey, ICE, 15 * s, a)
    rect(c, x - 60 * s, y + 66 * s, 120 * s, 8 * s, "#cdefff", a)

def i5_spin(c, W, H, t, S):
    B = BB(S, 3)
    def pA(c, ts):
        gx, gy, R = 600, 470, 340
        globe2(c, gx, gy, R, rot=t * 18, tilt=12, melt=0.0)
        c.drawLine(gx, gy - R - 70, gx, gy + R + 70, paint("#ffffff", 0.7, stroke=4, dash=([16, 10], 0)))
        for sg in (-1, 1):
            for k, dx in enumerate((-0.45, 0.0, 0.45)):
                q = ((t * 0.5 + k * 0.33) % 1)
                y0 = gy + sg * R * 0.82; y1 = gy + sg * R * 0.12
                yy = lerp(y0, y1, q)
                arrow(c, gx + dx * R, lerp(y0, y1, max(0, q - 0.3)), gx + dx * R, yy, "#3aa0e8", 9, 0.9 * F(t, B(0, 0.25)), head=30)
        C(c, "MASS MOVES AWAY FROM THE AXIS", 1420, 420, F(t, B(0, 0.3)), ts, size=34)
        C(c, "POLES → EQUATOR", 1420, 550, F(t, B(0, 0.5)), ts, size=34, bg="#13426b", dot="#3aa0e8")
    def pB(c, ts):
        arms = ease(prog(t, B(1, 0.05), 1.5))
        skater(c, 640, 700, 1.4, arms, t, lerp(9, 4, arms))
        T(c, "ARMS OUT → SLOWER SPIN", 1400, 330, 54, ts, ICE, F(t, B(1, 0.1)), maxw=880)
        C(c, "+1.33 MS PER CENTURY", 1400, 520, F(t, B(1, 0.5)), ts, size=42, bg=YEL, fg="#04162b", a=1)
        T(c, "LONGER DAYS SINCE 2000 (2024 STUDY)", 1400, 620, 28, ts, "#cdefff", F(t, B(1, 0.6)), w=700, fam="Inter", maxw=880, shadow=0)
    def pC(c, ts):
        droplet(c, 560, 520, 150, "#3aa0e8", F(t, B(2, 0.0)))
        T(c, "MELTING ICE", 560, 760, 44, ts, "#7fc8ff", F(t, B(2, 0.0)), maxw=520)
        T(c, "VS", 960, 520, 90, ts, YEL, F(t, B(2, 0.2)))
        moon(c, 1360, 520, 150, 1.0, F(t, B(2, 0.3)))
        T(c, "THE MOON", 1360, 760, 44, ts, "#e6e6f2", F(t, B(2, 0.3)), maxw=520)
        C(c, "BY 2100, IF EMISSIONS STAY HIGH", 960, 900, F(t, B(2, 0.55)), ts, size=32)
    run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB), (B(2, 0), pC)])

# ------------------------------------------------------------------ i5_rebound
def crust_section(c, ts, t, dip, ice_a, ice_h, labels=1.0):
    top = []
    for i in range(25):
        x = i * 80
        d = dip * math.exp(-((x - 960) / 380) ** 2)
        top.append((x, 520 + d))
    p = spline(top); p.lineTo(1920, 680 + dip * 0.6);
    bot = [(x, y + 160) for (x, y) in top][::-1]
    fill_under(c, bot[::-1], 1100, [(0, "#c4562b", 1), (1, "#5a1d10", 1)])
    spline(bot, p, move=False); p.close()
    c.drawPath(p, paint(shader=lin(0, 500, 0, 760, [(0, "#8a7262", 1), (1, "#4a3a32", 1)])))
    c.drawPath(spline(top), paint("#b19a88", 1, stroke=4))
    if ice_a > 0.01:
        it = [(x, y - ice_h * math.exp(-((x - 960) / 330) ** 2 * 1.6)) for (x, y) in top if 420 <= x <= 1500]
        ice_body(c, it, [(x, y + 2) for (x, y) in top if 420 <= x <= 1500], ice_a)
        for k in range(5):
            xx = 760 + k * 100
            arrow(c, xx, 200, xx, 270, "#ffffff", 7, ice_a * 0.8, head=26)
    T(c, "CRUST", 180, 600, 34, ts, "#f0e0d0", labels, align="l", maxw=400)
    T(c, "HOT, SLOWLY FLOWING ROCK", 180, 900, 34, ts, "#ffd0b0", labels, align="l", maxw=800)

def i5_rebound(c, W, H, t, S):
    B = beats(S, 5)
    bbS = (4, 54, 33, 71); rS = geo.map_rect(bbS, 560, 545, height=950)
    def pA(c, ts):
        if t < B(1, 0.0):
            d = lerp(110, 60, ease(prog(t, 0, B(1, 0))))
            crust_section(c, ts, t, d, 0, 0)
            for k in range(4):
                q = ((t * 0.6 + k / 4) % 1)
                arrow(c, 780 + k * 120, 760 - q * 120, 780 + k * 120, 700 - q * 120, YEL, 8, 0.9 * (1 - q), head=28)
            C(c, "THE LAND IS RISING", 960, 200, F(t, B(0, 0.4)), ts, size=40, bg=YEL, fg="#04162b", a=1)
        else:
            press = ease(prog(t, B(1, 0.05), 1.2)); melt = ease(prog(t, B(1, 0.55), 0.8))
            rebound = ease(prog(t, B(1, 0.65), max(1.0, S.dur - B(1, 0.65))))
            d = lerp(lerp(30, 200, press), 30, rebound * 0.7)
            crust_section(c, ts, t, d, (1 - melt) * press, 260)
            if melt > 0.5:
                for k in range(4):
                    q = ((t * 0.5 + k / 4) % 1)
                    arrow(c, 780 + k * 120, 760 - q * 100, 780 + k * 120, 700 - q * 100, YEL, 8, 0.9 * (1 - q) * melt, head=28)
                C(c, "SPRINGS BACK… SLOWLY", 960, 160, F(t, B(1, 0.7)), ts, size=40, bg=YEL, fg="#04162b", a=1)
            else:
                C(c, "ICE PRESSES THE CRUST DOWN", 960, 160, F(t, B(1, 0.1)), ts, size=38)
    def pM(c, ts):
        draw_base(c, bbS, rS)
        ia = 1 - ease(prog(t, B(2, 0.15), 1.5))
        if ia > 0:
            x, y = geo.lonlat_xy(18, 64.5, bbS, rS)
            oval(c, x, y, 330, 420, "#ffffff", 0.55 * ia, blur=20)
            T(c, "ICE SHEET (SCHEMATIC)", x, y, 30, ts, "#04162b", ia, w=900, maxw=600, shadow=0)
        city_pin(c, bbS, rS, 18.3, 62.95, F(t, B(2, 0.55)), "HIGH COAST", ts, dx=-330, dy=-40, t=t, colr=YEL)
        city_pin(c, bbS, rS, 21.4, 63.35, F(t, B(2, 0.6)), "KVARKEN", ts, dx=140, dy=-130, t=t, colr=YEL)
        x, y = geo.lonlat_xy(20.8, 61.8, bbS, rS)
        T(c, "GULF OF BOTHNIA", x + 10, y + 70, 24, ts, "#cdefff", F(t, B(2, 0.5)), w=800, fam="Inter", maxw=300, shadow=6)
        cx = 1460
        C(c, "ICE: 3 KM THICK", cx, 230, F(t, B(2, 0.1)), ts, size=34)
        C(c, "MELTED ≈ 10,500 YEARS AGO", cx, 350, F(t, B(2, 0.3)), ts, size=34)
        C(c, "STILL RISING: 8–9 MM / YEAR", cx, 470, F(t, B(2, 0.7)), ts, size=34, bg=YEL, fg="#04162b", a=1)
        C(c, "+1 KM² OF NEW LAND / YEAR", cx, 640, F(t, B(3, 0.25)), ts, size=34, bg="#13426b")
        C(c, "≈ 100 M STILL TO GO", cx, 760, F(t, B(3, 0.65)), ts, size=34, bg="#13426b")
    def pH(c, ts):
        sea = 900; pxm = 2.0
        water(c, 0, 1920, sea, 1080, t, 1.0, amp=5)
        hill = [(0, 1000), (300, 960), (600, 800), (900, 560), (1150, 330), (1350, 230), (1550, 210), (1920, 240)]
        rock(c, hill)
        for k in range(16): conifer(c, 1000 + k * 55, 250 + abs(k - 7) * 12 + (300 if k < 3 else 0), 90, "#2e5e4e")
        ys = sea - 286 * pxm
        dashed_h(c, 0, 1920, ys, YEL, F(t, B(4, 0.2)), 4, t)
        C(c, "END-OF-ICE-AGE SHORELINE", 760, ys - 55, F(t, B(4, 0.3)), ts, size=32, bg=YEL, fg="#04162b", a=1)
        gauge(c, 140, sea, pxm, 300, 286 * ease(prog(t, B(4, 0.1), 1.8)), ts, 1.0, step=100, t=t, readout="+286 M", w=50)
        T(c, "HIGH COAST, SWEDEN", 1600, 120, 40, ts, ICE, F(t, B(4, 0.05)), maxw=600)
    run_panels(c, W, H, t, S, [(0, pA), (B(2, 0), pM), (B(4, 0), pH)])

# ------------------------------------------------------------------ i5_antarctica (schematic section)
SL = 520
BED_A = [(80, 600), (200, 470), (300, 640), (450, 860), (600, 690), (680, 480), (760, 620), (880, 700), (960, 460), (1060, 430),
         (1200, 410), (1320, 440), (1430, 470), (1500, 940), (1570, 470), (1680, 430), (1840, 480)]
TOP_A = [(80, 515), (300, 330), (600, 280), (900, 300), (1150, 160), (1450, 150), (1700, 260), (1840, 470)]
LIFT = [0.2, 0.5, 0.6, 0.6, 0.6, 0.55, 0.55, 0.6, 0.6, 0.7, 0.8, 0.8, 0.8, 0.8, 0.7, 0.5, 0.2]

def ant_section(c, ts, t, ice_a, rise=0.0, a=1.0, labels=0.0, t_lab=(1e9, 1e9, 1e9)):
    bed = [(x, y - rise * 140 * LIFT[i]) for i, (x, y) in enumerate(BED_A)]
    water(c, 80, 1840, SL, 1080, t, a, amp=4)
    ice_body(c, TOP_A, bed, ice_a * a)
    rock(c, bed, a=a)
    c.drawRect(skia.Rect.MakeLTRB(0, 0, 80, 1080), paint(BG_T, 0));
    dashed_h(c, 60, 1860, SL, "#ffffff", 0.6 * a, 3, t)
    T(c, "SEA LEVEL", 80, SL - 30, 24, ts, "#ffffff", 0.7 * a, w=800, align="l", fam="Inter", shadow=0, maxw=300)
    T(c, "SCHEMATIC · NOT TO SCALE", 1840, 1050, 22, ts, "#cdefff", 0.6 * a, w=700, align="r", fam="Inter", shadow=0, maxw=700)
    C(c, "WEST", 450, 150, F(t, t_lab[0]), ts, size=34, bg="#13426b"); C(c, "EAST", 1350, 90, F(t, t_lab[0]), ts, size=34, bg="#13426b")
    C(c, "ISLANDS", 450, 255, F(t, t_lab[1]), ts, size=38, bg=YEL, fg="#04162b", a=1)
    C(c, "ONE LANDMASS", 1350, 195, F(t, t_lab[1] + 0.3), ts, size=38, bg=YEL, fg="#04162b", a=1)

def i5_antarctica(c, W, H, t, S):
    mode = S.opts.get("mode", "full")
    if mode == "short":
        def pS(c, ts):
            melt = ease(prog(t, S.lt(0, 0.1), max(1.0, S.lt(1, 0.0) - S.lt(0, 0.1))))
            ant_section(c, ts, t, 1 - melt, t_lab=(S.lt(1, 0.0), S.lt(1, 0.35), 0))
        run_panels(c, W, H, t, S, [(0, pS)]); return
    B = beats(S, 5)
    def pA(c, ts):
        globe2(c, 640, 560, 420, rot=(t * 4), tilt=-78)
        T(c, "27 MILLION KM³", 1420, 420, 90, ts, ICE, F(t, B(0, 0.25)), maxw=820)
        T(c, "OF ICE: GONE", 1420, 540, 60, ts, YEL, F(t, B(0, 0.5)), maxw=820)
    def pB(c, ts):
        melt = ease(prog(t, B(1, 0.0), max(1.0, B(1, 0.45) - B(1, 0.0))))
        ant_section(c, ts, t, 1 - melt, t_lab=(B(1, 0.35), B(1, 0.6), 0))
        pb = F(t, B(2, 0.35))
        if pb > 0:
            line(c, 450, SL + 10, 450, 850, YEL, 5, pb); arrow(c, 450, 840, 450, 856, YEL, 5, pb)
            C(c, "BYRD BASIN: −2.5 KM", 760, 960, pb, ts, size=32, bg=YEL, fg="#04162b", a=1)
        C(c, "ROCK FLOOR BELOW SEA LEVEL", 960, 400, F(t, B(2, 0.05)) * (1 - F(t, B(2, 0.9))), ts, size=32, bg=CORAL, fg="#ffffff", a=1)
    def pC(c, ts):
        y0 = 240; pxm = 0.2
        dashed_h(c, 200, 1720, y0, "#ffffff", 0.8, 3, t)
        T(c, "SEA LEVEL", 200, y0 - 36, 26, ts, "#ffffff", 0.8, w=800, align="l", fam="Inter", shadow=0, maxw=400)
        for k, (lab, d, x, colr) in enumerate([("DEAD SEA SHORE", 413, 480, "#e9d29a"), ("BYRD BASIN", 2538, 960, CYAN), ("DENMAN CANYON", 3500, 1440, CORAL)]):
            p = ease(prog(t, B(3, 0.1 + 0.25 * k), 0.9))
            if p <= 0: continue
            hh = d * pxm * p
            rrect(c, x - 120, y0, 240, hh, 12, colr, 0.9)
            T(c, f"−{int(round(d * p)):,} M", x, y0 + hh + 50, 54, ts, colr, 1.0, maxw=420)
            T(c, lab, x, y0 + hh + 110, 30, ts, "#ffffff", 1.0, w=800, fam="Inter", maxw=420, shadow=6)
        C(c, "DEEPEST POINT ON LAND", 1440, 160, F(t, B(3, 0.85)), ts, size=32, bg=YEL, fg="#04162b", a=1)
    def pD(c, ts):
        rise = ease(prog(t, B(4, 0.1), max(1.0, B(4, 0.7) - B(4, 0.1))))
        ant_section(c, ts, t, 0, rise=rise, t_lab=(0, 1e9, 0))
        for k in range(5):
            q = ((t * 0.5 + k / 5) % 1)
            arrow(c, 300 + k * 300, 1000 - q * 90, 300 + k * 300, 950 - q * 90, YEL, 8, 0.8 * (1 - q) * (1 - rise * 0.5), head=26)
        C(c, "PART LAND, PART SEA", 960, 140, F(t, B(4, 0.6)), ts, size=44, bg=YEL, fg="#04162b", a=1)
    run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB), (B(3, 0), pC), (B(4, 0), pD)])

# ------------------------------------------------------------------ i5_clock
def bars_years(c, ts, t, rows, x0=520, x1=1780, y0=330, gap=190, ymax=12000):
    line(c, x0, y0 - 80, x0, y0 + gap * len(rows) - 60, "#ffffff", 3, 0.6)
    for k, (lab, yrs, colr, t_on, note) in enumerate(rows):
        p = ease(prog(t, t_on, 1.0))
        if p <= 0: continue
        y = y0 + k * gap
        T(c, lab, x0 - 30, y, 34, ts, "#ffffff", p, w=800, align="r", fam="Inter", maxw=480)
        rrect(c, x0, y - 30, (x1 - x0) * yrs / ymax * p, 60, 30, colr, p)
        T(c, note, x0 + (x1 - x0) * yrs / ymax * p + 24 if yrs / ymax < 0.7 else x0 + 30, y, 36, ts, "#ffffff" if yrs / ymax < 0.7 else "#04162b", p, align="l", maxw=900, shadow=0 if yrs / ymax >= 0.7 else 8)

def i5_clock(c, W, H, t, S):
    B = beats(S, 5)
    def pA(c, ts):
        hourglass(c, 620, 560, 1.4, t)
        T(c, "HOW LONG,", 1360, 440, 110, ts, ICE, F(t, B(0, 0.1)), maxw=820)
        T(c, "REALLY?", 1360, 580, 110, ts, YEL, F(t, B(0, 0.3)), maxw=820)
    def pB(c, ts):
        lv = 0.6 + 0.4 * math.sin(t * 2)
        gauge(c, 260, 960, 11.5, 70, lv * 0.2, ts, 1.0, step=10, t=t, readout="≈ 6 MM / YEAR (2024)", w=80)
        C(c, "NASA, 2024", 1260, 230, F(t, B(1, 0.05)), ts, size=30)
        T(c, "70 M ÷ 6 MM A YEAR", 1260, 420, 70, ts, "#ffffff", F(t, B(1, 0.45)), maxw=1100)
        T(c, "≈ 12,000 YEARS", 1260, 590, 130, ts, YEL, F(t, B(1, 0.65)), maxw=1100)
        T(c, "AT TODAY'S PACE", 1260, 700, 40, ts, "#cdefff", F(t, B(1, 0.75)), w=700, fam="Inter", maxw=900)
    def pC(c, ts):
        T(c, "YEARS TO MELT IT ALL", 1150, 130, 54, ts, ICE, F(t, B(2, 0.0)), maxw=1300)
        bars_years(c, ts, t, [("AT TODAY'S PACE", 12000, "#2c6fa3", B(2, 0.0), "≈ 12,000"),
                              ("SOME SCIENTISTS", 5000, CYAN, B(2, 0.35), "5,000+")], y0=360, gap=200)
    def pD(c, ts):
        gx, gy = 520, 560
        globe2(c, gx, gy, 340, rot=t * 4, tilt=-78, melt=0.0)
        oil = F(t, B(3, 0.15))
        if oil > 0:
            rect(c, 1240, 270, 420, 110, "#2a2f3a", oil); rect(c, 1240, 270, 420, 110, "#8a93a6", oil, stroke=3)
            for k in range(3):
                rect(c, 1290 + k * 130, 150, 44, 125, "#3a404c", oil)
                smoke(c, 1312 + k * 130, 140, t + k, 1.0, oil * 0.9, seed=k, n=7, col_="#6a6f7a", rise=130)
            C(c, "BURN ALL REACHABLE FOSSIL FUEL", 1450, 450, oil, ts, size=30, bg="#13426b")
        C(c, "ANTARCTICA: ALMOST ICE-FREE", 1450, 570, F(t, B(3, 0.45)), ts, size=30, bg="#13426b")
        C(c, "+3 M PER CENTURY", 1450, 700, F(t, B(3, 0.7)), ts, size=40, bg=YEL, fg="#04162b", a=1)
        T(c, "FOR THE FIRST 1,000 YEARS (WINKELMANN ET AL., 2015)", 1450, 790, 24, ts, "#cdefff", F(t, B(3, 0.75)), w=700, fam="Inter", maxw=860, shadow=0)
        pw = F(t, B(4, 0.2))
        if pw > 0:
            rrect(c, 1010, 860, 880, 150, 26, "#04162b", 0.92 * pw); rrect(c, 1010, 860, 880, 150, 26, CORAL, pw, stroke=4)
            T(c, "WEST ANTARCTICA TIPS AT", 1450, 905, 32, ts, "#ffffff", pw, w=800, fam="Inter", maxw=860, shadow=0)
            T(c, "600–800 BILLION TONNES OF CARBON", 1450, 965, 40, ts, CORAL, pw, maxw=880, shadow=0)
    run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB), (B(2, 0), pC), (B(3, 0), pD)])

# ------------------------------------------------------------------ i5_past
def i5_past(c, W, H, t, S):
    B = beats(S, 4)
    def tl(c, ts, hi):
        y = 900; x0, x1 = 260, 1760
        line(c, x0, y, x1, y, "#ffffff", 5, 0.8); arrow(c, x1 - 10, y, x1 + 30, y, "#ffffff", 5, 0.8)
        marks = [(260, "50 MILLION YEARS AGO"), (640, "34 MILLION"), (1380, "3 MILLION"), (1740, "TODAY")]
        for k, (x, lab) in enumerate(marks):
            on = hi == k
            circle(c, x, y, 16 if on else 11, YEL if on else "#cdefff")
            T(c, lab, x, y + 60, 30 if on else 26, ts, YEL if on else "#cdefff", 1.0 if on else 0.7, w=800, fam="Inter", maxw=420, shadow=6)
    def pA(c, ts):
        tl(c, ts, 3)
        T(c, "EARTH HAS DONE THIS BEFORE", 960, 420, 84, ts, ICE, F(t, B(0, 0.1)), maxw=1700)
    def pB(c, ts):
        tl(c, ts, 2)
        rot = -42 + math.sin(t * 0.3) * 8
        globe2(c, 520, 430, 330, rot, tilt=45, melt=0.75 * ease(prog(t, B(1, 0.35), 1.5)))
        x, y, v = gxy(-42, 72, 520, 430, 330, rot, 45)
        pin(c, x, y, F(t, B(1, 0.45)), "GREENLAND: LARGELY ICE-FREE", ts, dx=-60, dy=-170, colr=CYAN, t=t, align="c")
        T(c, "PLIOCENE", 1340, 130, 64, ts, YEL, F(t, B(1, 0.0)), maxw=700)
        C(c, "CO₂ ABOVE 400 PPM", 1340, 300, F(t, B(1, 0.1)), ts, size=34)
        C(c, "+3 TO 4 °C WARMER", 1340, 420, F(t, B(1, 0.3)), ts, size=34, bg="#13426b")
        C(c, "SEAS +15 TO 20 M", 1340, 540, F(t, B(1, 0.55)), ts, size=40, bg=YEL, fg="#04162b", a=1)
        C(c, "TODAY: ABOVE 400 PPM AGAIN", 1340, 680, F(t, B(1, 0.85)), ts, size=32, bg=CORAL, fg="#ffffff", a=1)
    def pC(c, ts):
        tl(c, ts, 0)
        gx, gy, R = 560, 430, 330; rot = 10 + t * 3; tilt = -60
        globe2(c, gx, gy, R, rot, tilt, melt=1.0)
        for k, (lon, lat) in enumerate([(-100, -75), (-80, -77), (-120, -78), (-90, -82), (-70, -73)]):
            x, y, v = gxy(lon, lat, gx, gy, R, rot, tilt)
            if v: conifer(c, x, y + 26, 64, "#0b2e1a", snow=0, a=F(t, B(2, 0.35 + 0.05 * k)))
        C(c, "LITTLE OR NO POLAR ICE", 1340, 330, F(t, B(2, 0.05)), ts, size=36)
        C(c, "FORESTS IN WEST ANTARCTICA", 1340, 470, F(t, B(2, 0.4)), ts, size=36, bg="#1f5a3a")
        T(c, "ILLUSTRATION", gx, gy + R + 50, 22, ts, "#cdefff", 0.6, w=700, fam="Inter", shadow=0)
    def pD(c, ts):
        tl(c, ts, 1)
        gx, gy, R = 560, 430, 330; rot = 10 + t * 3; tilt = -60
        g = ease(prog(t, B(3, 0.05), 2.2))
        globe2(c, gx, gy, R, rot, tilt, melt=1 - g)
        C(c, "THE PLANET COOLS", 1340, 300, F(t, B(3, 0.0)), ts, size=36)
        C(c, "ICE BUILDS ON ANTARCTICA", 1340, 430, F(t, B(3, 0.2)), ts, size=36, bg="#13426b", dot=CYAN)
        C(c, "SEAS SETTLE NEAR TODAY'S", 1340, 560, F(t, B(3, 0.55)), ts, size=36, bg=YEL, fg="#04162b", a=1)
    run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB), (B(2, 0), pC), (B(3, 0), pD)])

# ------------------------------------------------------------------ i5_finger (twist)
def finger_section(c, ts, t, pull, melt, a=1.0, lab_t=(1e9, 1e9, 1e9)):
    base = 560; xs = list(range(480, 1921, 40))
    def surf(x, f):
        near = min(1.0, math.exp(-(x - 640) / 380))
        bulge = 120 * near * (1 - f)
        drop = -70 * near * f
        far = 22 * f * (1 - near)
        return base - (bulge * pull) + (-drop) - far
    pts = [(x, surf(x, melt)) for x in xs]
    p = poly(pts + [(1920, 1080), (480, 1080)])
    c.drawPath(p, paint(shader=lin(0, 420, 0, 1080, [(0, "#3aa0e8", 0.95), (1, "#04203d", 0.95)]), a=a))
    c.drawPath(poly(pts, close=False), paint("#bdeeff", a, stroke=4))
    if melt > 0:
        old = [(x, base - 120 * min(1.0, math.exp(-(x - 640) / 380)) * pull) for x in xs if x >= 640]
        c.drawPath(poly(old, close=False), paint("#ffffff", 0.7 * a * min(1, melt * 3), stroke=3, dash=([14, 10], 0)))
    lift = 60 * melt
    bed = [(0, 560 - lift), (250, 540 - lift), (450, 520 - lift * 0.8), (580, 545 - lift * 0.5), (680, 720), (780, 900), (1920, 940)]
    rock(c, bed, a=a)
    ice_body(c, [(0, 240), (220, 210), (430, 260), (580, 360), (650, 420)], [(0, 562 - lift), (250, 542 - lift), (450, 522 - lift), (580, 547 - lift * 0.5), (650, 690)], a * (1 - melt))
    if pull > 0 and melt < 0.5:
        for k in range(4):
            q = ((t * 0.7 + k / 4) % 1)
            xx = 1250 - q * 380
            arrow(c, xx + 80, 470 - k * 4, xx, 470 - k * 4, YEL, 7, a * (1 - melt * 2) * (1 - q), head=26)
        C(c, "GRAVITY PULLS WATER TO THE ICE", 1300, 330, F(t, lab_t[0]) * (1 - melt), ts, size=30, bg=YEL, fg="#04162b", a=1)
    pn = F(t, lab_t[1])
    if pn > 0:
        arrow(c, 760, 400, 760, 520, CORAL, 10, pn, head=34)
        C(c, "NEAR: −20 TO −50 M", 900, 320, pn, ts, size=36, bg=CORAL, fg="#ffffff", a=1, align="l")
    pf = F(t, lab_t[2])
    if pf > 0:
        arrow(c, 1720, 640, 1720, 520, CYAN, 10, pf, head=34)
        C(c, "FAR AWAY: RISES MORE", 1700, 420, pf, ts, size=32, bg="#13426b", align="r")
    T(c, "NOT TO SCALE", 1880, 1050, 22, ts, "#cdefff", 0.6 * a, w=700, align="r", fam="Inter", shadow=0, maxw=500)

def ring_pts(lon0, lat0, dist_km, n=120):
    R = 6371.0; d = dist_km / R; la1 = math.radians(lat0); lo1 = math.radians(lon0); out = []
    for k in range(n + 1):
        b = 2 * math.pi * k / n
        la2 = math.asin(math.sin(la1) * math.cos(d) + math.cos(la1) * math.sin(d) * math.cos(b))
        lo2 = lo1 + math.atan2(math.sin(b) * math.sin(d) * math.cos(la1), math.cos(d) - math.sin(la1) * math.sin(la2))
        out.append((math.degrees(lo2), math.degrees(la2)))
    return out

def i5_finger(c, W, H, t, S):
    mode = S.opts.get("mode", "full")
    if mode == "short":
        def pS(c, ts):
            melt = ease(prog(t, S.lt(0, 0.35), 1.4))
            finger_section(c, ts, t, 1.0, melt, lab_t=(S.lt(0, 0.0), S.lt(0, 0.55), 1e9))
            T(c, "GREENLAND", 320, 170, 50, ts, ICE, 1 - melt * 0.5, maxw=600)
        run_panels(c, W, H, t, S, [(0, pS)]); return
    B = beats(S, 6)
    bbG = (-100, 38, 25, 84); rG = geo.map_rect(bbG, 760, 545, height=960)
    bbW = (-180, -72, 180, 78); rW = geo.map_rect(bbW, 960, 560, width=1840)
    def pA(c, ts):
        globe2(c, 560, 560, 420, rot=-42, tilt=50)
        T(c, "NEXT TO GREENLAND,", 1380, 420, 70, ts, ICE, F(t, B(0, 0.25)), maxw=960)
        T(c, "THE SEA FALLS", 1380, 540, 100, ts, YEL, F(t, B(0, 0.5)), maxw=960)
        arrow(c, 1380, 620, 1380, 760, CORAL, 14, F(t, B(0, 0.6)), head=44)
    def pB(c, ts):
        melt = ease(prog(t, B(2, 0.05), 1.6))
        finger_section(c, ts, t, ease(prog(t, B(1, 0.2), 1.2)), melt, lab_t=(B(1, 0.45), B(2, 0.6), B(2, 0.95)))
        C(c, "≈ 3,000 TRILLION TONNES OF ICE", 330, 140, F(t, B(1, 0.05)) * (1 - melt), ts, size=30, bg="#13426b")
        C(c, "THE LAND RISES TOO", 330, 600, F(t, B(2, 0.4)), ts, size=30, bg=YEL, fg="#04162b", a=1)
    def pC(c, ts):
        draw_base(c, bbG, rG)
        pr = F(t, B(3, 0.1))
        if pr > 0:
            pts = [geo.lonlat_xy(lo, la, bbG, rG) for lo, la in ring_pts(-42, 72, 2000)]
            c.save(); c.clipRect(skia.Rect.MakeXYWH(*rG))
            c.drawPath(poly(pts), paint(CYAN, 0.18 * pr)); c.drawPath(poly(pts), paint(CYAN, pr, stroke=5, dash=([16, 10], -t * 25)))
            c.restore()
        gx, gy = geo.lonlat_xy(-42, 72, bbG, rG)
        C(c, "SMALLER RISE, OR A FALL", gx, gy + 40, pr, ts, size=28, bg="#13426b")
        C(c, "~2,000 KM", gx + 40, gy + 330, F(t, B(3, 0.3)), ts, size=28)
        C(c, "BEYOND: MORE THAN AVERAGE", rG[0] + rG[2] - 30, rG[1] + rG[3] - 60, F(t, B(3, 0.6)), ts, size=30, bg=CORAL, fg="#ffffff", a=1, align="r")
    def pD(c, ts):
        geo.draw_map(c, bbW, rW, land=LAND, sea=SEA, outline="#021022", outline_w=1.5)
        map_frame(c, rW)
        ya = geo.lonlat_xy(0, -76, bbW, rW)[1]
        C(c, "ANTARCTICA MELTS", 960, ya - 10, F(t, B(4, 0.0)), ts, size=30, bg=CYAN, fg="#04162b", a=1)
        for k, (lon, lat, lab) in enumerate([(-150, 8, "PACIFIC"), (160, 18, "PACIFIC"), (75, -12, "INDIAN OCEAN"), (-58, 26, "W. ATLANTIC")]):
            x, y = geo.lonlat_xy(lon, lat, bbW, rW); p = F(t, B(4, 0.2 + 0.12 * k))
            if p <= 0: continue
            q = (t * 0.8 + k * 0.3) % 1
            arrow(c, x, y + 40 - q * 30, x, y - 10 - q * 30, CORAL, 9, p, head=30)
            C(c, lab, x, y + 80, p, ts, size=26)
        C(c, "EACH ICE SHEET HITS THE FAR SIDE HARDEST", 960, 120, F(t, B(4, 0.75)), ts, size=32, bg=YEL, fg="#04162b", a=1)
    def pE(c, ts):
        water(c, 0, 1920, 760, 1080, t, 1.0, amp=10)
        q = ((t - B(5, 0)) * 0.12) % 1.2 - 0.1
        sx = lerp(100, 1820, q); sy = 230
        rect(c, sx - 60, sy - 40, 120, 80, "#cfd8e6"); rect(c, sx - 250, sy - 22, 170, 44, "#2c5fa3"); rect(c, sx + 80, sy - 22, 170, 44, "#2c5fa3")
        c.drawPath(poly([(sx - 30, sy + 40), (sx + 30, sy + 40), (sx + 140, 745), (sx - 140, 745)]), paint(CYAN, 0.12))
        for k in range(5):
            r_ = ((t * 1.2 + k / 5) % 1)
            yy = lerp(sy + 45, 740, r_); hw = lerp(30, 140, r_)
            line(c, sx - hw, yy, sx + hw, yy, CYAN, 5, 0.9 * (1 - r_ * 0.7))
        C(c, "SATELLITES, 1993–2019", 960, 430, F(t, B(5, 0.1)), ts, size=36)
        C(c, "PATTERN CONFIRMED", 960, 600, F(t, B(5, 0.5)), ts, size=44, bg=YEL, fg="#04162b", a=1)
    run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB), (B(3, 0), pC), (B(4, 0), pD), (B(5, 0), pE)])

# ================================================================== SHORT-ONLY: Lake Vostok (portrait stage 1080x634)
def vostok_section(c, t, depth_f=1.0, lake_glow=0.0, heat=0.0, a=1.0, drill=0.0):
    sy, iy, ly = 70, 480, 560
    rect(c, 0, sy, PW, PH, "#000000", 0)
    p = skia.Path(); p.addRect(skia.Rect.MakeLTRB(0, sy, PW, PH))
    c.drawRect(skia.Rect.MakeLTRB(0, sy, PW, iy + 40), paint(shader=lin(0, sy, 0, iy, [(0, "#ffffff", 1), (0.5, "#d5f2ff", 1), (1, "#86d2f5", 1)]), a=a))
    for k in range(1, 9): line(c, 0, sy + (iy - sy) * k / 9, PW, sy + (iy - sy) * k / 9 + 6 * math.sin(k), "#9fd8f5", 2, 0.4 * a)
    lake = skia.Path(); lake.moveTo(150, iy); lake.cubicTo(300, iy - 30, 780, iy - 30, 930, iy); lake.cubicTo(780, iy + 70, 300, iy + 70, 150, iy); lake.close()
    rock(c, [(0, iy + 10), (150, iy + 2), (540, iy + 60), (930, iy + 2), (1080, iy + 14)], ybot=PH + 20, a=a)
    c.drawPath(lake, paint(shader=lin(0, iy - 30, 0, iy + 60, [(0, "#1d6fb0", 1), (1, "#04203d", 1)]), a=a))
    if lake_glow > 0: c.drawPath(lake, paint(CYAN, lake_glow * a, stroke=5))
    rrect(c, 760, sy - 52, 120, 52, 8, "#c9533a", a); rect(c, 776, sy - 40, 30, 20, "#ffd27a", a); line(c, 860, sy - 52, 860, sy - 120, "#cfd8e6", 5, a)
    rrect(c, 650, sy - 34, 90, 34, 6, "#5a6a7a", a)
    if heat > 0:
        for k in range(6):
            q = ((t * 0.5 + k / 6) % 1); x = 250 + k * 120
            line(c, x + 8 * math.sin(t * 3 + k), iy + 70 - q * 40, x, iy + 40 - q * 40, "#ff8a3c", 6, heat * a * (1 - q))
    if drill > 0:
        yb = sy + (iy - 25 - sy) * drill
        line(c, 540, sy - 20, 540, yb, "#2b2f3a", 9, a); line(c, 540, sy - 20, 540, yb, YEL, 3, a)
        c.drawPath(poly([(530, yb), (550, yb), (540, yb + 22)]), paint(YEL, a))

def i5_vostok(c, W, H, t, S):
    mode = S.opts.get("mode", "intro"); ts = 1.0
    def pnl(fn): run_panels(c, W, H, t, S, [(0, fn)], portrait=True)
    L = S.n() - 1  # main line index (after an optional CTA line)
    if mode == "intro":
        def f(c, ts):
            vostok_section(c, t, lake_glow=0.6 + 0.4 * math.sin(t * 3))
            gauge(c, 80, 480, 410 / 4.0, 4.0, 4.0 * ease(prog(t, 0.2, 1.6)), ts, 1.0, step=1, unit="KM", t=t, w=40, ticks=False)
            T(c, "≈ 4 KM OF ICE", 150, 270, 70, ts, "#04162b", F(t, S.lt(0, 0.2)), align="l", maxw=700, shadow=0)
            C(c, "LAKE VOSTOK", 540, 590, F(t, S.lt(0, 0.5)), ts, size=40, bg=YEL, fg="#04162b", a=1)
        pnl(f)
    elif mode == "lakes":
        def f(c, ts):
            gx, gy, R, rot, tilt = 540, 330, 280, 20 + t * 4, -80
            globe2(c, gx, gy, R, rot, tilt)
            for lon, lat, lab, dx, dy in [(106.0, -77.5, "VOSTOK", 200, -60), (-153.7, -84.2, "WHILLANS", -230, 40)]:
                x, y, v = gxy(lon, lat, gx, gy, R, rot, tilt)
                if v: pin(c, x, y, F(t, 0.3), lab, ts, dx=dx, dy=dy, align="c", colr=CYAN, t=t, size=30)
            n = int(675 * ease(prog(t, S.lt(0, 0.45), 1.2)))
            if n > 0: T(c, f"{n}", 900, 560, 90, ts, YEL, 1.0, maxw=300)
        pnl(f)
    elif mode == "cold":
        def f(c, ts):
            vostok_section(c, t, heat=F(t, S.lt(0, 0.05)))
            T(c, "HEAT FROM BELOW", 540, 610, 42, ts, "#ffb27a", F(t, S.lt(0, 0.1)), maxw=700)
            thermometer(c, 170, 230, 230, -89, tmax=10, tmin=-95, label=False)
            C(c, "AIR ABOVE VOSTOK: −89 °C", 600, 200, F(t, S.lt(0, 0.6)), ts, size=34, bg="#04162b")
        pnl(f)
    elif mode == "drill":
        def f(c, ts):
            d = ease(prog(t, S.lt(L, 0.05), max(1.0, S.lt(L, 0.85) - S.lt(L, 0.05))))
            vostok_section(c, t, drill=d, lake_glow=F(t, S.lt(L, 0.85)))
            T(c, f"{int(3769 * d):,} M", 700, 300, 80, ts, YEL, F(t, S.lt(L, 0.0)), align="l", maxw=380, stroke=6)
            C(c, "FEBRUARY 2012", 820, 590, F(t, S.lt(L, 0.2)), ts, size=34)
        pnl(f)
    elif mode == "sealed":
        def f(c, ts):
            vostok_section(c, t, lake_glow=0.5)
            padlock(c, 540, 330, 120, F(t, 0.2))
            n = 14 * ease(prog(t, S.lt(L, 0.1), 1.5))
            T(c, f"{n:.0f} MILLION+ YEARS", 540, 140, 64, ts, "#04162b", F(t, S.lt(L, 0.05)), maxw=960, shadow=0)
        pnl(f)
    elif mode == "life":
        def f(c, ts):
            circle(c, 540, 320, 280, "#04203d"); circle(c, 540, 320, 280, CYAN, 1, stroke=8)
            c.save(); p = skia.Path(); p.addCircle(540, 320, 274); c.clipPath(p, doAntiAlias=True)
            rng = random.Random(4)
            for k in range(26):
                x = 540 + rng.uniform(-250, 250) + 30 * math.sin(t * 0.8 + k); y = 320 + rng.uniform(-250, 250) + 20 * math.cos(t * 0.7 + k)
                microbe(c, x, y, rng.uniform(16, 30), t + k, a=F(t, 0.1 + k * 0.03), colr=rng.choice([GREENC, "#7fe3ff", "#ffd27a"]))
            c.restore()
            C(c, "LAKE WHILLANS", 540, 600, F(t, S.lt(0, 0.1)), ts, size=36, bg=YEL, fg="#04162b", a=1)
            T(c, "NO SUNLIGHT", 900, 80, 40, ts, "#cdefff", F(t, S.lt(0, 0.6)), maxw=300)
        pnl(f)
    else:  # dna
        def f(c, ts):
            for k in range(26):
                y = 60 + k * 20; ph = t * 2 + k * 0.45
                x1 = 400 + math.sin(ph) * 120; x2 = 400 - math.sin(ph) * 120
                line(c, x1, y, x2, y, "#5a7a9a", 4)
                circle(c, x1, y, 10, CYAN); circle(c, x2, y, 10, YEL)
            T(c, "?", 800, 300, 300, ts, CORAL, F(t, S.lt(0, 0.45)), shadow=20)
            C(c, "CONTAMINATION?", 760, 560, F(t, S.lt(0, 0.5)), ts, size=36, bg=CORAL, fg="#ffffff", a=1)
        pnl(f)

# ================================================================== SHORT-ONLY: the Carnian Pluvial Episode (portrait stage)
def bg_rain(c, W, H, t, S):
    fill_bg(c, W, H, "#0c1622", "#1d2f3a")
    c.drawPaint(paint(shader=rad(W * 0.5, H * 0.3, max(W, H) * 0.7, [(0, "#3a5566", 0.4), (1, "#000000", 0)])))

def rain_streaks(c, t, x0, x1, y0, y1, n=80, a=1.0, seed=2, speed=900):
    if a <= 0: return
    rng = random.Random(seed)
    for k in range(n):
        x = rng.uniform(x0, x1); ph = rng.random(); L = rng.uniform(30, 60)
        y = y0 + ((ph + t * speed / (y1 - y0) * rng.uniform(0.8, 1.2)) % 1) * (y1 - y0)
        line(c, x, y, x - L * 0.25, y + L, "#9fd0ff", 3, a * rng.uniform(0.35, 0.8))

def triassic(c, t, wet=1.0, a=1.0):
    for i in range(3):
        cloud(c, 160 + i * 360 + math.sin(t * 0.3 + i) * 30, 60 + (i % 2) * 30, 140, "#2c3a46", 0.95 * a)
    hills(c, PW, 470, 40, "#24402e", 3, a=a, H=PH + 10)
    for k, x in enumerate((90, 300, 820, 1000)):
        treefern(c, x, 520, 190 + 30 * (k % 2), a=a, t=t)
    for k, x in enumerate((180, 640, 900)): conifer(c, x, 520, 170, "#1f4a34", a=a)
    rect(c, 0, 520, PW, PH, "#3d3324", a)
    water(c, 380, 760, 535, 570, t, a * wet, amp=3, top="#5a7d96", bot="#2a3d4a")
    rain_streaks(c, t, -40, PW + 40, 0, PH, n=int(90 * wet), a=a * wet)
    if wet > 0.5 and (t % 4.3) < 0.12:
        c.drawRect(skia.Rect.MakeLTRB(0, 0, PW, PH), paint("#ffffff", 0.25 * a))

def footprint(c, x, y, s, dino=True, a=1.0, rot=0):
    c.save(); c.translate(x, y); c.rotate(rot)
    if dino:
        oval(c, 0, 0, s * 0.35, s * 0.42, "#1e160e", a)
        for an in (-28, 0, 28):
            r = math.radians(an - 90)
            line(c, 0, -s * 0.2, math.cos(r) * s, math.sin(r) * s, "#1e160e", s * 0.22, a)
    else:
        oval(c, 0, 0, s * 0.3, s * 0.32, "#1e160e", a)
        for k in range(5):
            r = math.radians(-150 + k * 30)
            circle(c, math.cos(r) * s * 0.55, math.sin(r) * s * 0.55, s * 0.12, "#1e160e", a)
    c.restore()

def ammonite(c, x, y, s, a=1.0, colr="#d9b48a"):
    p = skia.Path()
    for k in range(80):
        th = k / 80 * 4 * math.pi; r = s * (0.08 + 0.92 * k / 80)
        px, py = x + math.cos(th) * r * 0.9, y + math.sin(th) * r * 0.9
        if k == 0: p.moveTo(px, py)
        else: p.lineTo(px, py)
    c.drawPath(p, paint(colr, a, stroke=s * 0.16))

def i5_rain(c, W, H, t, S):
    mode = S.opts.get("mode", "intro"); L = S.n() - 1
    def pnl(fn): run_panels(c, W, H, t, S, [(0, fn)], portrait=True, bg=bg_rain)
    if mode == "intro":
        def f(c, ts):
            triassic(c, t)
            pangea_globe(c, 930, 470, 110, rot=10 + t * 3)
            C(c, "~234 MILLION YEARS AGO", 300, 600, F(t, S.lt(0, 0.1)), 1.0, size=32, bg="#2c3a46")
        pnl(f)
    elif mode == "volcano":
        def f(c, ts):
            hills(c, PW, 560, 20, "#2a2a2e", 7, H=PH + 10)
            cone = poly([(220, 560), (460, 250), (620, 250), (860, 560)])
            c.drawPath(cone, paint("#3a2f2a"))
            for k in range(4): line(c, 540 + (k - 1.5) * 30, 255, 540 + (k - 1.5) * 90 + math.sin(t * 2 + k) * 10, 520, "#ff6a1a", 10, 0.9)
            flame(c, 540, 260, 140, t, seed=3)
            smoke(c, 540, 220, t, 1.0, 1.0, seed=2, n=14, col_="#5a5560", rise=260)
            n = F(t, S.lt(0, 0.6))
            for k in range(6):
                q = ((t * 0.25 + k / 6) % 1)
                C(c, "CO₂", 760 + 60 * math.sin(k * 2.1), 220 - q * 200, n * (1 - q), 1.0, size=26, bg="#3a3f4a")
            C(c, "TODAY: WESTERN NORTH AMERICA", 540, 600, F(t, S.lt(0, 0.25)), 1.0, size=30, bg="#2c3a46")
        pnl(f)
    elif mode == "pulses":
        def f(c, ts):
            x0, x1, yb = 90, 990, 520
            pts = []
            for i in range(121):
                q = i / 120
                hum = sum(math.exp(-((q - m) / 0.06) ** 2) for m in (0.2, 0.42, 0.62, 0.82))
                pts.append((lerp(x0, x1, q), yb - 60 - 300 * min(hum, 1.0)))
            pr = ease(prog(t, S.lt(0, 0.05), max(1.0, S.lt(0, 0.9) - S.lt(0, 0.05))))
            k = max(2, int(len(pts) * pr))
            c.drawPath(poly(pts[:k], close=False), paint("#7fc8ff", 1, stroke=8))
            line(c, x0, yb, x1, yb, "#ffffff", 3, 0.7)
            T(c, "HUMID", x0, 120, 34, 1.0, "#7fc8ff", 0.9, align="l", maxw=300)
            T(c, "DRY", x0, yb - 30, 34, 1.0, "#e9d29a", 0.9, align="l", maxw=300)
            xh, yh = pts[k - 1]
            rain_streaks(c, t, xh - 60, xh + 60, 0, yh - 20, n=12, a=clamp((yb - 60 - yh) / 200))
            C(c, "SEVERAL PULSES", 540, 590, F(t, S.lt(0, 0.4)), 1.0, size=34, bg="#2c3a46")
        pnl(f)
    elif mode == "extinct":
        def f(c, ts):
            fill_bg(c, PW, PH, "#0b2a3a", "#06141f")
            for k in range(9):
                x = 220 + (k % 3) * 320; y = 120 + (k // 3) * 170
                dead = k in (1, 5, 6)
                p = F(t, S.lt(L, 0.25 + 0.1 * (k in (5,)) + 0.2 * (k == 6))) if dead else 0
                ammonite(c, x, y, 60, a=1 - 0.75 * p, colr="#d9b48a")
                if dead: xmark(c, x, y, 50, p)
        pnl(f)
    elif mode == "dinos":
        def f(c, ts):
            rect(c, 0, 0, PW, PH, "#6b5a46")
            rng = random.Random(8)
            for k in range(40): circle(c, rng.uniform(0, PW), rng.uniform(0, PH), rng.uniform(3, 9), "#5a4a38", 0.8)
            line(c, 540, 40, 540, 600, "#ffffff", 3, 0.6)
            for k in range(5):
                footprint(c, 90 + k * 95, 330 + (50 if k % 2 else -50), 44, dino=False, a=F(t, 0.2 + k * 0.15), rot=90)
            for k in range(6):
                footprint(c, 600 + k * 85, 290 + (55 if k % 2 else -55), 60, dino=True, a=F(t, S.lt(0, 0.3) + k * 0.12), rot=90)
            for k in range(4):
                footprint(c, 640 + k * 110, 490 + (35 if k % 2 else -35), 46, dino=True, a=F(t, S.lt(0, 0.45) + k * 0.12), rot=80)
            C(c, "BEFORE: NO DINOSAUR TRACKS", 270, 80, F(t, 0.1), 1.0, size=26, bg="#2c3a46")
            C(c, "AFTER: MANY", 810, 80, F(t, S.lt(0, 0.3)), 1.0, size=30, bg=YEL, fg="#04162b", a=1)
            C(c, "DOLOMITES, ITALY", 540, 600, F(t, S.lt(0, 0.05)), 1.0, size=28, bg="#2c3a46")
        pnl(f)
    else:  # modern
        def f(c, ts):
            fill_bg(c, PW, PH, "#0b2a3a", "#06141f")
            conifer(c, 200, 470, 300, "#2e7a52", a=F(t, 0.1))
            for k in range(7):
                an = math.radians(-160 + k * 23); L_ = 150 + 30 * (k % 2)
                line(c, 540, 470, 540 + math.cos(an) * L_, 470 + math.sin(an) * L_, "#ff8a7a", 22, F(t, S.lt(0, 0.3)))
                circle(c, 540 + math.cos(an) * L_, 470 + math.sin(an) * L_, 18, "#ffb0a0", F(t, S.lt(0, 0.3)))
            for k in range(6):
                an = k / 6 * 6.283
                circle(c, 880 + math.cos(an) * 60, 360 + math.sin(an) * 60, 34, "#cfe8ff", F(t, S.lt(0, 0.55)), stroke=6)
            circle(c, 880, 360, 40, "#9fd8f5", F(t, S.lt(0, 0.55)))
            for k, (x, lab, tt) in enumerate([(200, "CONIFERS", 0.1), (540, "REEFS", S.lt(0, 0.3)), (880, "PLANKTON", S.lt(0, 0.55))]):
                C(c, lab, x, 570, F(t, tt), 1.0, size=30, bg="#2c3a46")
        pnl(f)

SCENES = {"i5_title": i5_title, "i5_card": i5_card, "i5_end": i5_end, "i5_endshort": i5_endshort,
          "i5_city": i5_city, "i5_rules": i5_rules, "i5_budget": i5_budget, "i5_seaice": i5_seaice, "i5_map": i5_map,
          "i5_albedo": i5_albedo, "i5_currents": i5_currents, "i5_spin": i5_spin, "i5_rebound": i5_rebound,
          "i5_antarctica": i5_antarctica, "i5_clock": i5_clock, "i5_past": i5_past, "i5_finger": i5_finger,
          "i5_vostok": i5_vostok, "i5_rain": i5_rain}
