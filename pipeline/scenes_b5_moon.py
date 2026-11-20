"""Batch 05 scenes: What If the Moon Disappeared? (+ teaser, drift and Pluto Shorts).

Look: "moonlit tide". Deep indigo night backgrounds with a silver-blue haze, a textured silver Moon,
and a glowing cyan tide-line: the ocean bulge drawn as a luminous ellipse around Earth (geo.globe) that
follows the Moon and relaxes when it vanishes. Sun-related elements are warm yellow for contrast.
Every scene draws on a virtual 1920x1080 stage (Stage). In Shorts the stage is scaled into the
0.255H..0.58H band and text sizes are multiplied by ts=1.75. Multi-part scenes are time-ordered panels.
"""
from common2 import *
import geo
import scenes_b3_kit as kit

BG_T, BG_B = "#03041a", "#111650"
SILVER = "#e6ecf8"; MBLUE = "#9db8ff"; TIDE = "#5ee0ff"; TIDE_D = "#1f7fd6"
RED = "#ff6b6b"; SUNY = "#ffd166"; GREEN = "#6fffb0"; YEL = ACCENT
CHIPBG = "#161b4f"
PAL = dict(accent="#8fd3ff", chip="#1c2260", title2=ACCENT)
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

_BG = {}
def bg_img(W, H):
    k = (W, H)
    if k not in _BG:
        surf = skia.Surface(W, H); cc = surf.getCanvas()
        fill_bg(cc, W, H, BG_T, BG_B)
        cc.drawPaint(paint(shader=rad(W * 0.82, H * 0.12, max(W, H) * 0.8, [(0, "#7f9bff", 0.22), (0.5, "#3a4aa0", 0.08), (1, "#000000", 0)])))
        cc.drawPaint(paint(shader=rad(W * 0.1, H * 0.95, max(W, H) * 0.6, [(0, "#2a1f6a", 0.35), (1, "#000000", 0)])))
        _BG[k] = surf.makeImageSnapshot()
    return _BG[k]

def bg_m(c, W, H, t, S, star_a=0.85, seed=51):
    c.drawImage(bg_img(W, H), 0, 0)
    stars(c, W, H, t, star_a, seed=seed, drift=(-3, 0))

def run_panels(c, W, H, t, S, items, seed=51, zoom=None):
    """items: [(t_on, fn(c, ts)), ...] in time order. Each later panel covers the previous one."""
    bg_m(c, W, H, t, S, seed=seed)
    for i, (t0, fn) in enumerate(items):
        t1 = items[i + 1][0] if i + 1 < len(items) else None
        if t1 is not None and t >= t1 + 0.5: continue
        a = phase(t, t0 if i > 0 else None, t1)
        if a <= 0.003: continue
        with Layer(c, a) as on:
            if not on: continue
            if i > 0 and t < t0 + 0.55: bg_m(c, W, H, t, S, seed=seed)
            if S.P: c.clipRect(skia.Rect.MakeLTRB(0, 0.215 * H, W, 0.59 * H))
            with Stage(c, S) as ts:
                if zoom and S.P:
                    z, zx, zy = zoom; c.translate(zx, zy); c.scale(z, z); c.translate(-zx, -zy)
                fn(c, ts)
    kit.hook(c, W, H, t, S)

def stage_bg(c, top, bot, a=1.0):
    c.drawRect(skia.Rect.MakeXYWH(0, 0, VW, VH), paint(shader=lin(0, 0, 0, VH, [(0, top, a), (1, bot, a)])))

# ------------------------------------------------------------------ the Moon
MARIA = [(-0.42, -0.28, 0.30), (0.02, -0.40, 0.17), (0.22, -0.08, 0.21), (0.62, -0.26, 0.12), (0.46, 0.18, 0.14),
         (-0.18, 0.34, 0.17), (-0.62, 0.02, 0.30), (0.30, 0.30, 0.09), (-0.45, 0.35, 0.12), (-0.05, 0.05, 0.10)]
_MI = {}
def moon_img(R):
    R = max(4, int(R))
    if R not in _MI:
        if len(_MI) > 30: _MI.clear()
        n = 2 * R + 4; surf = skia.Surface(n, n); cc = surf.getCanvas(); cc.clear(skia.ColorTRANSPARENT)
        cx = cy = n / 2
        cc.save(); pth = skia.Path(); pth.addCircle(cx, cy, R); cc.clipPath(pth, doAntiAlias=True)
        cc.drawCircle(cx, cy, R, paint("#cdd2dc"))
        for dx, dy, r in MARIA:
            cc.drawCircle(cx + dx * R, cy + dy * R, r * R, paint("#80879a", 0.8, blur=max(0.6, R * 0.05)))
        rng = random.Random(5)
        for _ in range(int(14 + R * 0.12)):
            ang = rng.random() * 6.28; d = rng.random() ** 0.6 * R * 0.95; cr = R * rng.uniform(0.015, 0.06)
            x, y = cx + math.cos(ang) * d, cy + math.sin(ang) * d
            cc.drawCircle(x + cr * 0.15, y + cr * 0.15, cr, paint("#6e7486", 0.55))
            cc.drawCircle(x - cr * 0.1, y - cr * 0.1, cr, paint("#e4e8ef", 0.35, stroke=max(0.6, cr * 0.25)))
        tx, ty = cx - 0.12 * R, cy + 0.66 * R  # bright rayed crater
        for k in range(12):
            an = k / 12 * 6.28 + 0.2
            cc.drawLine(tx, ty, tx + math.cos(an) * R * 0.45, ty + math.sin(an) * R * 0.45, paint("#f3f5f9", 0.18, stroke=max(0.6, R * 0.012)))
        cc.drawCircle(tx, ty, R * 0.035, paint("#ffffff", 0.9))
        cc.drawCircle(cx, cy, R, paint(shader=rad(cx - R * 0.25, cy - R * 0.25, R * 1.45, [(0, "#ffffff", 0.10), (0.7, "#000000", 0.0), (1, "#0a0d1c", 0.55)])))
        cc.restore()
        _MI[R] = surf.makeImageSnapshot()
    return _MI[R]

def moon_d(c, x, y, R, a=1.0, glow=1.0, phase_=None, waxing=True):
    """Moon disc. phase_: 0 new .. 0.5 quarter .. 1 full (lit fraction); waxing = lit on the right."""
    if a <= 0 or R < 1: return
    if glow > 0: circle(c, x, y, R * 1.7, "#bcd0ff", 0.16 * glow * a, blur=R * 0.45)
    img = moon_img(R); pt = skia.Paint(); pt.setAlphaf(clamp(a))
    c.drawImageRect(img, skia.Rect.MakeXYWH(x - R - 2, y - R - 2, 2 * R + 4, 2 * R + 4), skia.SamplingOptions(skia.FilterMode.kLinear), pt)
    if phase_ is not None and phase_ < 0.999:
        sh = phase_path(x, y, R, phase_, waxing)
        c.drawPath(sh, paint("#070914", 0.93 * a))

def phase_path(x, y, R, f, waxing=True):
    """dark part of the disc for lit fraction f (0..1)."""
    half = skia.Path(); s = -1 if waxing else 1
    half.addArc(skia.Rect.MakeLTRB(x - R, y - R, x + R, y + R), 90 if waxing else -90, 180); half.close()
    k = abs(1 - 2 * f)  # terminator ellipse half-width
    ell = skia.Path(); ell.addOval(skia.Rect.MakeLTRB(x - R * k, y - R, x + R * k, y + R))
    if f < 0.5: return skia.Op(half, ell, skia.PathOp.kUnion_PathOp) or half
    return skia.Op(half, ell, skia.PathOp.kDifference_PathOp) or half

def moon_vanish(c, x, y, R, t, tv, ghost=True, a=1.0, glow=1.0):
    if t < tv:
        moon_d(c, x, y, R, a, glow); return
    q = t - tv
    if q < 0.18:
        s = (1 + 0.1 * math.sin(q / 0.18 * math.pi)) * (1 - q / 0.18)
        moon_d(c, x, y, R * max(s, 0.02), a * (1 - q / 0.2), glow)
    fl = clamp(1 - q / 0.7)
    if fl > 0:
        circle(c, x, y, R * (1 + q * 4), SILVER, a * fl * 0.9, stroke=R * 0.1 * fl + 1)
        circle(c, x, y, R * 1.8, "#ffffff", a * fl * 0.3, blur=R * 0.5)
    if ghost:
        circle(c, x, y, R, MBLUE, a * 0.55 * eout((q - 0.3) / 0.8), stroke=max(2, R * 0.03), dash=([R * 0.16, R * 0.12], -t * 30))

# ------------------------------------------------------------------ Earth + tide bulge motif
def tide_bulge(c, x, y, R, ang, k, t, a=1.0, col_=TIDE):
    """glowing ocean bulge: ellipse stretched toward angle ang (degrees), drawn behind the globe."""
    if a <= 0 or k <= 0.001: return
    c.save(); c.translate(x, y); c.rotate(ang)
    rx, ry = R * (1 + k), R * (1 - k * 0.05)
    rr = skia.Rect.MakeLTRB(-rx, -ry, rx, ry)
    c.drawOval(rr, paint(shader=rad(0, 0, rx, [(0.55, col_, 0.0), (0.85, col_, 0.3 * a), (1, col_, 0.7 * a)])))
    c.drawOval(rr, paint(col_, 0.7 * a, stroke=R * 0.07, blur=R * 0.04))
    c.drawOval(rr, paint("#e6fbff", 0.9 * a, stroke=max(1.5, R * 0.012)))
    c.drawOval(rr, paint("#ffffff", 0.5 * a, stroke=max(1.0, R * 0.008), dash=([R * 0.08, R * 0.22], -t * R * 0.25)))
    c.restore()

def earth(c, x, y, R, rot, tilt=18, light=(-0.75, 0.35, 0.55), night=0.0, a=1.0, glow=1.0):
    geo.globe(c, x, y, int(R), rot=rot, tilt=tilt, light=light, night=night, a=a, glow=glow)

_STILL = {}
def still_earth(c, x, y, R, rot, tilt=18, light=(-0.75, 0.35, 0.55)):
    R = max(4, int(R) // 4 * 4); k = (R, rot, tilt, light)
    if k not in _STILL:
        if len(_STILL) > 12: _STILL.clear()
        pad = int(R * 0.3); n = 2 * (R + pad)
        surf = skia.Surface(n, n); cc = surf.getCanvas(); cc.clear(skia.ColorTRANSPARENT)
        geo.globe(cc, n / 2, n / 2, R, rot=rot, tilt=tilt, light=light)
        _STILL[k] = (surf.makeImageSnapshot(), pad)
    img, pad = _STILL[k]
    c.drawImage(img, x - R - pad, y - R - pad, skia.SamplingOptions(skia.FilterMode.kLinear))

def earth_moon(c, t, ex, ey, R, orbit=(520, 150), tilt_o=-8, mR=60, speed=0.35, ph0=2.4, tv=None, k=0.22, rot_speed=6, axis=0.0, a=1.0):
    """motif: Earth with glowing tide bulge and an orbiting Moon. tv: Moon vanishes then; bulge relaxes."""
    th = ph0 + speed * (t if tv is None or t < tv else tv)
    co, so = math.cos(math.radians(tilt_o)), math.sin(math.radians(tilt_o))
    ox, oy = math.cos(th) * orbit[0], math.sin(th) * orbit[1]
    mx, my = ex + ox * co - oy * so, ey + ox * so + oy * co
    front = math.sin(th) > 0
    gone = tv is not None and t >= tv
    kk = k if not gone else lerp(k, k * 0.32, ease((t - tv) / 1.6))
    mr = mR * (1 + 0.12 * math.sin(th))
    # orbit path
    c.save(); c.translate(ex, ey); c.rotate(tilt_o)
    oa = 0.35 * (1 - (ease((t - tv) / 1.0) if gone else 0)) * a
    if oa > 0.01:
        c.drawOval(skia.Rect.MakeLTRB(-orbit[0], -orbit[1], orbit[0], orbit[1]), paint(MBLUE, oa, stroke=3, dash=([14, 12], -t * 10)))
    c.restore()
    ang = math.degrees(math.atan2(my - ey, mx - ex))
    if not front: _moon_or_vanish(c, mx, my, mr, t, tv, a)
    tide_bulge(c, ex, ey, R, ang, kk, t, a)
    earth(c, ex, ey, R, rot=t * rot_speed + 40, tilt=18, a=a)
    if axis > 0:
        c.save(); c.translate(ex, ey); c.rotate(23.4)
        line(c, 0, -R * 1.32, 0, R * 1.32, "#ffffff", max(2, R * 0.018), 0.85 * axis * a, dash=([R * 0.07, R * 0.05], 0))
        c.restore()
    if front: _moon_or_vanish(c, mx, my, mr, t, tv, a)
    return mx, my

def _moon_or_vanish(c, x, y, R, t, tv, a):
    if tv is None: moon_d(c, x, y, R, a)
    else: moon_vanish(c, x, y, R, t, tv, a=a)

def motif_m(c, W, H, t, S, cx, cy, s):
    u = S.u * s
    earth_moon(c, t, cx, cy, int(170 * u * (1.15 if S.P else 1)), orbit=(400 * u * (1.1 if S.P else 1), 115 * u), mR=46 * u, speed=0.5, ph0=0.6)

def bg_title(c, W, H, t, S): bg_m(c, W, H, t, S)

def m5_title(c, W, H, t, S): kit.title(c, W, H, t, S, bg_title, motif_m, PAL)
def m5_card(c, W, H, t, S):
    def cbg(c, W, H, t, S):
        bg_m(c, W, H, t, S)
        with Layer(c, 0.35):
            motif_m(c, W, H, t, S, W / 2, H / 2, 1.3 if not S.P else 0.9)
    kit.card(c, W, H, t, S, cbg, PAL)
def m5_end(c, W, H, t, S): kit.end(c, W, H, t, S, bg_title, motif_m, PAL)
def m5_endshort(c, W, H, t, S): kit.end_short(c, W, H, t, S, bg_title, motif_m, PAL)

# ------------------------------------------------------------------ small props
def sun_d(c, x, y, r, t, a=1.0, glow=1.0): sun(c, x, y, r, t, a, glow)

def arrow2(c, x0, y0, x1, y1, colr, w, a=1.0): arrow(c, x0, y0, x1, y1, colr, w, a)

def crab(c, x, y, s, t, a=1.0, walk=0.0, colr="#e0402a"):
    if a <= 0: return
    ph = math.sin(t * 14 + x * 0.05) * walk
    for side in (-1, 1):
        for k in range(4):
            bx = x + side * s * 0.35; by = y + (k - 1.5) * s * 0.12
            kx = bx + side * s * 0.45; ky = by - s * 0.25 + (ph if k % 2 else -ph) * s * 0.12
            line(c, bx, by, kx, ky, mix(colr, "#000000", 0.25), s * 0.07, a)
            line(c, kx, ky, kx + side * s * 0.15, ky + s * 0.35, mix(colr, "#000000", 0.25), s * 0.06, a)
    for side in (-1, 1):
        line(c, x + side * s * 0.2, y - s * 0.2, x + side * s * 0.45, y - s * 0.55, colr, s * 0.1, a)
        oval(c, x + side * s * 0.5, y - s * 0.62, s * 0.16, s * 0.11, colr, a)
    oval(c, x, y, s * 0.48, s * 0.34, colr, a)
    oval(c, x - s * 0.1, y - s * 0.1, s * 0.22, s * 0.1, mix(colr, "#ffffff", 0.35), a * 0.6)
    for side in (-1, 1):
        line(c, x + side * s * 0.12, y - s * 0.28, x + side * s * 0.16, y - s * 0.45, colr, s * 0.05, a)
        circle(c, x + side * s * 0.16, y - s * 0.47, s * 0.05, "#1a0a08", a)

def beetle_ball(c, x, y, s, t, a=1.0):
    """dung beetle doing a 'handstand' behind its ball (ball to the right)."""
    bx = x + s * 0.75
    rot = t * 160
    circle(c, bx, y - s * 0.55, s * 0.55, "#5a3e28", a)
    c.save(); c.translate(bx, y - s * 0.55); c.rotate(rot)
    for k in range(5):
        an = k * 1.26
        circle(c, math.cos(an) * s * 0.3, math.sin(an) * s * 0.3, s * 0.07, "#6e4e34", a)
    c.restore()
    c.save(); c.translate(x, y - s * 0.45); c.rotate(-35)
    oval(c, 0, 0, s * 0.42, s * 0.26, "#141418", a)
    oval(c, -s * 0.12, -s * 0.08, s * 0.2, s * 0.08, "#4a5070", a * 0.6)
    circle(c, s * 0.45, s * 0.02, s * 0.13, "#141418", a)
    c.restore()
    for k in range(3):
        lk = math.sin(t * 10 + k * 2) * s * 0.08
        line(c, x - s * 0.1 + k * s * 0.15, y - s * 0.4, x - s * 0.25 + k * s * 0.22 + lk, y, "#141418", s * 0.06, a)
    line(c, x + s * 0.2, y - s * 0.6, x + s * 0.35, y - s * 0.75, "#141418", s * 0.06, a)

def acacia(c, x, y, h, colr, a=1.0):
    line(c, x, y, x - h * 0.05, y - h * 0.6, colr, h * 0.05, a)
    line(c, x - h * 0.03, y - h * 0.45, x + h * 0.25, y - h * 0.7, colr, h * 0.035, a)
    oval(c, x - h * 0.05, y - h * 0.72, h * 0.5, h * 0.1, colr, a)
    oval(c, x + h * 0.2, y - h * 0.76, h * 0.25, h * 0.07, colr, a)

def coral_branch(c, x, y, h, colr, seed, a=1.0, depth=0):
    rng = random.Random(seed)
    def br(x0, y0, ang, L, w, d):
        x1, y1 = x0 + math.cos(ang) * L, y0 + math.sin(ang) * L
        c.drawLine(x0, y0, x1, y1, paint(colr, a, stroke=w))
        if d < 3:
            for s_ in (-1, 0, 1):
                if s_ == 0 and rng.random() < 0.5: continue
                br(x1, y1, ang + s_ * rng.uniform(0.45, 0.8), L * rng.uniform(0.65, 0.85), w * 0.8, d + 1)
        else:
            circle(c, x1, y1, w * 0.75, mix(colr, "#ffffff", 0.35), a)
    for k in range(3):
        br(x + (k - 1) * h * 0.12, y, -math.pi / 2 + (k - 1) * 0.5, h * 0.22, h * 0.075, 0)

def brain_coral(c, x, y, r, colr, a=1.0):
    p = skia.Path(); p.addArc(skia.Rect.MakeLTRB(x - r, y - r, x + r, y + r), 180, 180); p.close()
    c.drawPath(p, paint(colr, a))
    for k in range(5):
        rr = r * (0.25 + 0.17 * k)
        q = skia.Path(); q.addArc(skia.Rect.MakeLTRB(x - rr, y - rr, x + rr, y + rr), 190, 160)
        c.drawPath(q, paint(mix(colr, "#000000", 0.3), a, stroke=max(2, r * 0.05)))

def table_coral(c, x, y, w, colr, a=1.0):
    line(c, x, y, x, y - w * 0.35, mix(colr, "#000000", 0.2), w * 0.08, a)
    oval(c, x, y - w * 0.38, w * 0.55, w * 0.09, colr, a)
    oval(c, x, y - w * 0.41, w * 0.5, w * 0.05, mix(colr, "#ffffff", 0.25), a)

_REEF = {}
def reef_img(glow):
    k = round(glow, 2)
    if k not in _REEF:
        if len(_REEF) > 8: _REEF.clear()
        surf = skia.Surface(VW, 420); cc = surf.getCanvas(); cc.clear(skia.ColorTRANSPARENT)
        rng = random.Random(3)
        cols = ["#7a5a9a", "#b06a8a", "#5a7aa0", "#9a7a5a", "#6a8a8a"]
        for i in range(22):
            x = 20 + i * 90 + rng.uniform(-25, 25)
            colr = mix(rng.choice(cols), "#0a1230", 0.45 - 0.3 * glow)
            kind = i % 4
            if kind == 1: table_coral(cc, x, 420, rng.uniform(220, 300), colr)
            elif kind == 3: brain_coral(cc, x, 425, rng.uniform(70, 110), colr)
            else: coral_branch(cc, x, 420, rng.uniform(260, 360), colr, i)
        for i in range(12):
            x = rng.uniform(0, VW); r = rng.uniform(40, 90)
            cc.drawOval(skia.Rect.MakeLTRB(x - r * 1.4, 420 - r * 0.7, x + r * 1.4, 420 + r * 0.7), paint(mix("#3a3a5a", "#0a1230", 0.4), 1))
        _REEF[k] = surf.makeImageSnapshot()
    return _REEF[k]

def underwater(c, t, glow=1.0, shafts=1.0):
    stage_bg(c, mix("#0b1d4a", "#06102a", 1 - glow), "#020614")
    if shafts > 0:
        for k in range(6):
            x0 = 300 + k * 270 + math.sin(t * 0.4 + k) * 30
            al = shafts * (0.07 + 0.04 * math.sin(t * 0.9 + k * 1.7))
            c.drawPath(poly([(x0 - 40, 0), (x0 + 40, 0), (x0 + 240, VH), (x0 + 60, VH)]), paint("#b9d2ff", al, blur=18))
    for k in range(40):  # surface ripples
        x = (k * 53 + t * 20) % VW
        line(c, x, 40 + 6 * math.sin(k + t), x + 30, 40 + 6 * math.sin(k + t), "#9fc3ff", 2, 0.25 * max(glow, 0.3))
    pt = skia.Paint(); c.drawImage(reef_img(glow), 0, VH - 420, skia.SamplingOptions(), pt)

def fish_school(c, t, a=1.0):
    rng = random.Random(21)
    for k in range(14):
        x = (rng.uniform(0, VW) + t * rng.uniform(40, 70)) % (VW + 200) - 100
        y = rng.uniform(380, 640) + math.sin(t * 1.3 + k) * 12
        s = rng.uniform(16, 26); colr = rng.choice(["#9fc3ff", "#cfe0ff", "#7fa8e0"])
        oval(c, x, y, s, s * 0.42, colr, 0.8 * a)
        c.drawPath(poly([(x - s * 0.9, y), (x - s * 1.5, y - s * 0.4), (x - s * 1.5, y + s * 0.4)]), paint(colr, 0.8 * a))

def spawn_bundles(c, t, t0, rate=1.0, a=1.0, sync=True, seed=4, n=160, ytop=60):
    """egg bundles rising from the reef; sync=True: a cloud starting at t0; else sparse random ones."""
    if a <= 0 or t < t0: return
    rng = random.Random(seed)
    for i in range(n):
        x0 = rng.uniform(60, VW - 60); st = t0 + (rng.uniform(0, 1.2) if sync else rng.uniform(0, 30))
        if not sync and rng.random() > 0.15 * rate: continue
        q = t - st
        if q < 0: continue
        y = VH - 260 - q * rng.uniform(70, 130)
        if y < ytop: continue
        x = x0 + math.sin(q * 1.5 + i) * 18
        r = rng.uniform(4, 8)
        circle(c, x, y, r * 2, "#ffc2a8", a * 0.18, blur=r)
        circle(c, x, y, r, rng.choice(["#ffb39a", "#ffd2b8", "#ff9fb0"]), a * clamp(q * 2) * 0.95)

def map_pin(c, x, y, s, t, a=1.0, colr=TIDE):
    pul = (t * 0.8) % 1
    circle(c, x, y, s * (1 + 2.2 * pul), colr, a * (1 - pul) * 0.8, stroke=3)
    circle(c, x, y, s * 0.55, colr, a); circle(c, x, y, s * 0.55, "#ffffff", a, stroke=3)

def bar_h(c, x, y, w, h, frac, colr, label, val, ts, a=1.0, icon=None):
    rrect(c, x, y - h / 2, w, h, h / 2, "#ffffff", 0.1 * a)
    if frac > 0: rrect(c, x, y - h / 2, max(h, w * frac), h, h / 2, colr, a)
    T(c, label, x, y - h * 1.15, 34, ts, "#cfe3ff", a, w=700, fam="Inter", align="l", shadow=6)
    if val: T(c, val, x + max(h, w * frac) + 24, y, 54, ts, colr, a, align="l")

# ------------------------------------------------------------------ m5_hook
def m5_hook(c, W, H, t, S):
    nb = 3 if S.n() >= 3 else 1; B = beats(S, nb)
    tv = B(2, 0.55) if nb == 3 else S.lt(0, 0.72)
    def pA(c, ts):
        ex, ey = (700, 560) if not S.P else (960, 560)
        orb = (480, 150) if not S.P else (700, 190)
        R = 230 if not S.P else 250
        mx, my = earth_moon(c, t, ex, ey, R, orbit=orb, mR=58 if not S.P else 70, speed=0.32, ph0=0.9, tv=tv, axis=vis(t, B(1, 0.68)) if nb == 3 else 0)
        if nb == 3 and not S.P:
            C(c, "4.5 BILLION YEARS", 1560, 170, vis(t, B(0, 0.15), tv - 0.3), ts, size=38, dot=SILVER)
            C(c, "PULLS THE OCEANS", 1560, 380, vis(t, B(1, 0.03), tv - 0.3), ts, dot=TIDE)
            C(c, "SETS NATURE'S CLOCK", 1560, 500, vis(t, B(1, 0.33), tv - 0.3), ts, dot=SILVER)
            C(c, "STEADIES EARTH'S TILT", 1560, 620, vis(t, B(1, 0.66), tv - 0.3), ts, dot=YEL)
            T(c, "TONIGHT?", 1560, 520, 110, ts, SILVER, prog(t, tv + 0.5, 0.4), shadow=16)
    run_panels(c, W, H, t, S, [(0, pA)], zoom=(1.05, 960, 560))

# ------------------------------------------------------------------ m5_rules
def m5_rules(c, W, H, t, S):
    B = beats(S, 4)
    def pA(c, ts):
        tv = B(0, 0.28)
        moon_vanish(c, 960, 470, 210, t, tv)
        for k, (s_, x) in enumerate((("NO EXPLOSION", 450), ("NO FALLING ROCKS", 960), ("NO GRAVITY", 1470))):
            p = vis(t, B(0, 0.42 + 0.17 * k))
            C(c, s_, x, 850, p, ts, size=36, bg="#2a1030" if k < 2 else CHIPBG, dot=RED if k < 2 else MBLUE)
    def pB(c, ts):
        sx, sy = 430, 540
        c.drawOval(skia.Rect.MakeLTRB(sx - 660, sy - 280, sx + 660, sy + 280), paint(SUNY, 0.35, stroke=3, dash=([16, 14], -t * 8)))
        sun_d(c, sx, sy, 105, t)
        an = 0.25 * (t - B(1, 0)) - 0.6
        ex, ey = sx + math.cos(an) * 660, sy + math.sin(an) * 280
        earth(c, ex, ey, 52, rot=t * 20, light=(-0.9, 0.0, 0.4))
        C(c, "EARTH KEEPS ORBITING", 1500, 190, vis(t, B(1, 0.1)), ts, size=38, dot=TIDE)
        check(c, 1500 + (370 if not S.P else 640), 190, 26, vis(t, B(1, 0.25)))
        C(c, "THE SUN KEEPS SHINING", 1500, 300, vis(t, B(1, 0.45)), ts, size=38, dot=SUNY)
        check(c, 1500 + (380 if not S.P else 660), 300, 26, vis(t, B(1, 0.6)))
    def pC(c, ts):
        earth(c, 620, 500, 320, rot=t * 5 + 20)
        moon_d(c, 1420, 500, 87, glow=0.6)
        for x0, x1, lab in ((300, 940, "12,742 KM"), (1333, 1507, "3,475 KM")):
            p = vis(t, B(2, 0.25 if x0 == 300 else 0.45))
            line(c, x0, 885, x1, 885, "#ffffff", 3, p); line(c, x0, 865, x0, 905, "#ffffff", 3, p); line(c, x1, 865, x1, 905, "#ffffff", 3, p)
            T(c, lab, (x0 + x1) / 2, 950, 46, ts, "#ffffff", p, maxw=700)
        C(c, "ABOUT 1/4 THE WIDTH", 1420, 250, vis(t, B(2, 0.65)), ts, size=40, bg=YEL, fg="#0b1030", a=1)
    def pD(c, ts):
        ex, mx, y = 190, 1640, 540
        earth(c, ex, y, 24, rot=t * 20, glow=0.6)
        moon_d(c, mx, y, 6.5, glow=1.5)
        T(c, "EARTH", ex, y - 70, 34, ts, TIDE, vis(t, B(3, 0.02)), maxw=300)
        T(c, "MOON", mx, y - 70, 34, ts, SILVER, vis(t, B(3, 0.02)), maxw=300)
        line(c, ex + 40, y + 70, mx, y + 70, "#ffffff", 3, 0.6, dash=([14, 12], 0))
        T(c, "384,400 KM", (ex + mx) / 2, y + 130, 64, ts, "#ffffff", vis(t, B(3, 0.05)))
        C(c, "EARTH AND MOON TO SCALE", 960, 200, vis(t, B(3, 0.0)), ts, size=38, dot=TIDE)
        t0 = B(3, 0.35)
        if t > t0:
            q = ((t - t0) % 2.4)
            f = clamp(q / 1.28)
            px = lerp(mx, ex + 30, f)
            if q < 1.28:
                c.drawLine(px, y, min(mx, px + 160), y, paint(shader=lin(px, y, px + 160, y, [(0, "#fffbe0", 0.9), (1, "#fffbe0", 0)]), stroke=5))
                circle(c, px, y, 9, "#ffffff", 1); circle(c, px, y, 26, "#fff3c0", 0.4, blur=10)
            else:
                circle(c, ex, y, 24 + (q - 1.28) * 80, "#fff3c0", clamp(1 - (q - 1.28) / 0.6) * 0.8, stroke=4)
            T(c, f"{1.28 * f:.2f} S", 960, 330, 80, ts, SUNY, vis(t, t0), maxw=600)
    run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB), (B(2, 0), pC), (B(3, 0), pD)])

# ------------------------------------------------------------------ m5_night
def moonscape(c, t, dark, moon_a, stars_extra, shadow_a, tv=None, ts=1.0):
    top = mix("#1a2766", "#02030a", dark); bot = mix("#33478c", "#04060f", dark)
    stage_bg(c, top, bot)
    stars(c, VW, VH, t, 0.35 + 0.65 * stars_extra, seed=61, drift=(-2, 0))
    if stars_extra > 0: stars(c, VW, VH, t, stars_extra, seed=62, drift=(-2, 0), density=2.2)
    mx, my = 1450, 220
    if tv is not None: moon_vanish(c, mx, my, 90, t, tv, ghost=False)
    elif moon_a > 0: moon_d(c, mx, my, 90, moon_a)
    sea_y = 700
    c.drawRect(skia.Rect.MakeLTRB(0, sea_y, VW, VH), paint(shader=lin(0, sea_y, 0, VH, [(0, mix("#28407a", "#03050c", dark), 1), (1, mix("#0e1a40", "#010205", dark), 1)])))
    g = 1 - dark
    if g > 0:  # moon glitter path
        rng = random.Random(9)
        for k in range(70):
            yy = sea_y + 10 + rng.random() ** 1.5 * 360; w = 30 + (yy - sea_y) * 0.5 * rng.random()
            xx = mx + rng.gauss(0, 18 + (yy - sea_y) * 0.25) + math.sin(t * 2 + k) * 8
            line(c, xx - w / 2, yy, xx + w / 2, yy, SILVER, 2.5, g * rng.uniform(0.3, 0.9) * (0.6 + 0.4 * math.sin(t * 3 + k)))
    c.drawPath(poly([(1100, sea_y + 2), (1500, sea_y - 14), (1920, sea_y - 4), (1920, sea_y + 6), (1100, sea_y + 6)]), paint(mix("#1a2550", "#020306", dark)))
    land = mix("#1a2448", "#020306", dark)
    c.drawPath(poly([(0, 800), (300, 760), (700, 790), (980, 840), (1100, 1080), (0, 1080)]), paint(land))
    px, py = 520, 790
    if shadow_a > 0:
        c.save(); c.translate(px, py); c.rotate(-8)
        c.drawPath(poly([(-14, 0), (14, 0), (-260, 40), (-300, 22)]), paint("#000000", 0.55 * shadow_a, blur=4))
        c.restore()
    person(c, px, py, 120, mix("#0c1230", "#000000", dark), look_up=1)

def m5_night(c, W, H, t, S):
    if S.n() < 3:  # Short: moonlit landscape -> dark, then reflectivity
        tv = S.lt(0, 0.18)
        def pB(c, ts):
            d = ease((t - tv) / 1.2) if t > tv else 0
            moonscape(c, t, d * 0.8, 1, d, 1 - d, tv=tv, ts=ts)
        def pC(c, ts): albedo(c, t, ts, S.lt(0, 0.5), 0.0)
        run_panels(c, W, H, t, S, [(0, pB), (S.lt(0, 0.5), pC)])
        return
    B = beats(S, 3)
    def pA(c, ts):
        stage_bg(c, "#4f8fe8", "#cfe6ff")
        sun_d(c, 1350, 260, 80, t)
        tv = B(0, 0.55)
        if t < tv + 0.4:
            al = 0.18 * (1 - clamp((t - tv) / 0.4))
            moon_d(c, 1150, 330, 55, al, glow=0)
            circle(c, 1150, 330, 55, "#ffffff", 3 * al, stroke=2, dash=([10, 8], 0))
        hills(c, VW, 800, 60, "#7fbf7a", 11, H=VH); hills(c, VW, 880, 40, "#4f9f5a", 12, H=VH)
        C(c, "NEW MOON: UP BY DAY, LOST IN THE GLARE", 760, 160, vis(t, B(0, 0.1)), ts, size=34, dot=SILVER)
        C(c, "NOBODY NOTICES", 1150, 470, vis(t, tv + 0.4), ts, size=36)
    def pB(c, ts):
        tv = B(1, 0.28)
        d = ease((t - tv) / 1.2) if t > tv else 0
        moonscape(c, t, d * 0.8, 1, d, 1 - d, tv=tv, ts=ts)
        C(c, "FULL MOON", 1450, 400, vis(t, B(1, 0.0), tv), ts, size=34, dot=SILVER)
        C(c, "YOUR MOON SHADOW", 330, 900, vis(t, B(1, 0.05), tv + 0.6), ts, size=32)
        C(c, "SHADOWS: GONE", 330, 900, vis(t, B(1, 0.55)), ts, size=32, bg="#2a1030", dot=RED)
        C(c, "FAR MORE STARS", 760, 200, vis(t, B(1, 0.75)), ts, size=38, dot=YEL)
    def pC(c, ts): albedo(c, t, ts, B(2, 0), B(2, 0.5))
    run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB), (B(2, 0), pC)])

def albedo(c, t, ts, t0, t1):
    """sunlight in, 12% reflected; then 'bright against black, grey against daylight'."""
    if t < t1 + 0.6 or t1 <= t0:
        mx, my = 1150, 540
        moon_d(c, mx, my, 220, glow=0.4)
        for k in range(7):
            yy = my - 270 + k * 90
            q = (t * 0.9 + k * 0.13) % 1
            x0 = lerp(80, mx - 230, q)
            arrow(c, x0 - 160, yy, x0, yy, SUNY, 9, 0.9 * math.sin(q * math.pi))
        q = (t * 0.9) % 1
        arrow(c, mx - 240, my - 20, lerp(mx - 260, 260, q), my + 220 * q, SILVER, 9, 0.95 * math.sin(q * math.pi))
        C(c, "SUNLIGHT IN", 300, 170, vis(t, t0 + 0.1), ts, size=34, dot=SUNY)
        C(c, "ONLY ~12% BOUNCES BACK", 1150, 900, vis(t, t0 + 0.6), ts, size=40, bg=YEL, fg="#0b1030", a=1)
    if t1 > t0 and t > t1:
        a = vis(t, t1, None, 0.6)
        with Layer(c, a):
            stage_bg(c, BG_T, BG_B)
            rrect(c, 1000, 120, 860, 760, 40, "#b8c7dc", 1)
            rrect(c, 60, 120, 860, 760, 40, "#000000", 1)
            moon_d(c, 490, 500, 230, glow=0.6)
            moon_d(c, 1430, 500, 230, glow=0)
            T(c, "AGAINST BLACK", 490, 950, 46, ts, "#ffffff", vis(t, t1 + 0.2), maxw=800)
            T(c, "AGAINST DAYLIGHT", 1430, 950, 46, ts, "#ffffff", vis(t, t1 + 0.5), maxw=800)
            C(c, "A DARK, DUSTY GREY", 1430, 190, vis(t, t1 + 0.8), ts, size=34)

# ------------------------------------------------------------------ m5_wobble
def m5_wobble(c, W, H, t, S):
    B = beats(S, 3)
    tv = B(2, 0.12)
    def pA(c, ts):
        bx, by = 760, 560
        th = 0.8 * (min(t, tv)) + 0.3
        e_rx, e_ry, m_rx, m_ry = 110, 40, 640, 230
        ex, ey = bx - math.cos(th) * e_rx, by - math.sin(th) * e_ry
        mx, my = bx + math.cos(th) * m_rx, by + math.sin(th) * m_ry
        fa = 1 - (ease((t - tv) / 1.0) if t > tv else 0)
        c.drawOval(skia.Rect.MakeLTRB(bx - m_rx, by - m_ry, bx + m_rx, by + m_ry), paint(MBLUE, 0.3 * fa, stroke=3, dash=([14, 12], -t * 10)))
        front = math.sin(th) > 0
        if not front: moon_vanish(c, mx, my, 42, t, tv)
        earth(c, ex, ey, 150, rot=t * 8 + 30)
        if front: moon_vanish(c, mx, my, 42, t, tv)
        c.drawOval(skia.Rect.MakeLTRB(bx - e_rx, by - e_ry, bx + e_rx, by + e_ry), paint(YEL, 0.9 * fa, stroke=4, dash=([10, 8], -t * 20)))
        pa = vis(t, B(0, 0.35))
        line(c, bx - 22, by, bx + 22, by, YEL, 6, pa); line(c, bx, by - 22, bx, by + 22, YEL, 6, pa)
        circle(c, bx, by, 34, YEL, 0.35 * pa, blur=12)
        C(c, "SHARED BALANCE POINT", 760, 830, vis(t, B(0, 0.45)), ts, size=36, dot=YEL)
        C(c, "4,670 KM FROM EARTH'S CENTER", 760, 935, vis(t, B(0, 0.7)), ts, size=34)
        C(c, "INSIDE THE EARTH", 1560, 180, vis(t, B(1, 0.05)), ts, size=36, dot=TIDE)
        C(c, "ONE WOBBLE A MONTH", 1560, 290, vis(t, B(1, 0.45)), ts, size=36, dot=SILVER)
        C(c, "WOBBLE: STOPPED", 1560, 400, vis(t, tv + 0.6), ts, size=36, bg="#2a1030", dot=RED)
    run_panels(c, W, H, t, S, [(0, pA)])

# ------------------------------------------------------------------ m5_tides
def polar_tides(c, t, x, y, R, k, ang=0.0, moon=True, mx=None, mR=70, tv=None, pin=False, ts=1.0, a=1.0):
    rot = -t * 18
    tide_bulge(c, x, y, R, ang, k, t, a)
    earth(c, x, y, R, rot=rot, tilt=90, light=(0.0, 0.0, 1.0) if moon else (-0.7, 0, 0.7), a=a)
    if moon and mx is not None:
        if tv is None: moon_d(c, mx, y, mR, a)
        else: moon_vanish(c, mx, y, mR, t, tv, a=a)
    if pin:
        px, py, vis_ = geo.globe_xy(-30, 52, x, y, R, rot, tilt=90)
        circle(c, px, py, 14, YEL, a); circle(c, px, py, 14, "#0b1030", a, stroke=3)
        return px, py

def m5_tides(c, W, H, t, S):
    mode = S.opts.get("mode")
    def pBul(c, ts, t0, t1):
        sp = lambda f: lerp(t0, t1, f)
        ex, ey, R = 720, 540, 230
        polar_tides(c, t, ex, ey, R, 0.2 * eout(prog(t, t0 + 0.2, 0.8)), 0, mx=1600, mR=72, pin=True)
        for k, (xa, L, lab) in enumerate(((ex + R * 0.82, 230, "STRONGEST PULL"), (ex, 160, None), (ex - R * 0.82, 100, "WEAKEST PULL"))):
            p = vis(t, sp(0.06 + k * 0.08))
            arrow(c, xa, ey, xa + L * eout(p), ey, "#ffffff", 9, p)
            if lab and mode != "short": C(c, lab, xa + (100 if k == 0 else -40), ey + (-90 if k == 0 else 300), vis(t, sp(0.12 + k * 0.1)), ts, size=30)
        C(c, "TWO TIDAL BULGES", 1500, 180 if mode != "short" else 150, vis(t, sp(0.35)), ts, size=38, dot=TIDE)
        if mode != "short": C(c, "2 HIGH TIDES A DAY", 1500, 900, vis(t, sp(0.7)), ts, size=36, dot=YEL)
    def pBars(c, ts, t0):
        C(c, "TIDE-RAISING PULL", 960, 170, vis(t, t0 + 0.05), ts, size=40, dot=TIDE)
        moon_d(c, 300, 430, 60, glow=0.5); sun_d(c, 300, 690, 52, t, glow=0.5)
        bar_h(c, 420, 430, 1150, 70, eout(prog(t, t0 + 0.2, 0.7)), MBLUE, "MOON", "100%", ts)
        bar_h(c, 420, 690, 1150, 70, 0.46 * eout(prog(t, t0 + 0.6, 0.7)), SUNY, "SUN", "46%", ts)
    if mode == "short":
        t1 = S.lt(0, 0.45)
        run_panels(c, W, H, t, S, [(0, lambda c, ts: pBul(c, ts, 0, t1)), (t1, lambda c, ts: pBars(c, ts, t1))])
        return
    B = beats(S, 5)
    def pA(c, ts):
        stage_bg(c, "#6fa0ec", "#ffd7b5")
        sun_d(c, 300, 560, 70, t, glow=0.6)
        lvl = lerp(860, 800, ease(prog(t, B(0, 0.1), 3)))
        c.drawRect(skia.Rect.MakeLTRB(0, 560, VW, VH), paint("#5a8fd0"))
        c.drawRect(skia.Rect.MakeLTRB(0, lvl, VW, VH), paint(shader=lin(0, lvl, 0, VH, [(0, "#2f6fb8", 1), (1, "#143a70", 1)])))
        for k in range(12):
            xx = (k * 170 + t * 30) % VW
            line(c, xx, lvl + 4 + 3 * math.sin(t * 2 + k), xx + 70, lvl + 4 + 3 * math.sin(t * 2 + k), "#cfe9ff", 3, 0.6)
        c.drawPath(poly([(0, VH), (0, 640), (500, 700), (1000, 840), (1600, 1080)]), paint("#e6c995"))
        rect(c, 1240, 420, 36, 600, "#6b4a2f")
        for k in range(9): line(c, 1240, 470 + k * 60, 1276, 470 + k * 60, "#ffffff", 3, 0.6)
        line(c, 1000, 620, 1500, 620, YEL, 5, vis(t, B(0, 0.15)), dash=([18, 12], 0))
        C(c, "USUAL HIGH TIDE", 1690, 620, vis(t, B(0, 0.2)), ts, size=30, bg="#3a2a10", dot=YEL)
        line(c, 1000, lvl, 1500, lvl, "#ffffff", 4, 0.9)
        C(c, "THIS MORNING", 1690, lvl, vis(t, B(0, 0.5)), ts, size=30, dot=TIDE)
        person(c, 420, 690, 110, "#2a2f45")
        rrect(c, 380, 560, 18, 150, 9, "#ff8a3c")
    def pD(c, ts):
        tv = B(3, 0.08)
        g = ease((t - tv) / 1.4) if t > tv else 0
        k = lerp(0.2, 0.09, g); ang = lerp(0, 180, ease((t - tv - 0.6) / 1.2)) if t > tv else 0
        polar_tides(c, t, 560, 540, 210, k, ang, mx=1180, mR=60, tv=tv)
        sun_d(c, 90, 540, 60, t, a=vis(t, tv + 0.6), glow=0.6)
        bx = [1420, 1700]; hh = [520, 520 * 0.46 / 1.46]
        for i, (lab, colr, sub) in enumerate((("BIGGEST SPRING TIDE", MBLUE, "MOON + SUN"), ("SUN ALONE", SUNY, "NO MOON"))):
            p = vis(t, B(3, 0.3 + i * 0.25))
            hgt = hh[i] * eout(p)
            rrect(c, bx[i] - 70, 880 - hgt, 140, hgt, 14, colr, p)
            T(c, sub, bx[i], 930, 30, ts, "#cfe3ff", p, w=700, fam="Inter", maxw=300)
            T(c, "TODAY'S BIGGEST" if i == 0 else "NO MOON", bx[i], 860 - hgt - 40, 30, ts, colr, p, w=800, maxw=300)
        C(c, "≈ 1/3 AS HIGH", 1560, 200, vis(t, B(3, 0.7)), ts, size=42, bg=YEL, fg="#0b1030", a=1)
    def pE(c, ts):
        tg = B(4, 0.6)
        for i, (lab, cx) in enumerate((("SPRING TIDES", 500), ("NEAP TIDES", 1420))):
            p = vis(t, B(4, 0.05 + 0.2 * i))
            with Layer(c, p):
                sun_d(c, cx - 330, 540, 50, t, glow=0.4)
                earth(c, cx, 540, 70, rot=t * 10)
                if i == 0: moon_vanish(c, cx + 230, 540, 26, t, tg)
                else: moon_vanish(c, cx, 540 - 220, 26, t, tg)
                T(c, lab, cx, 780, 52, ts, "#ffffff", 1, maxw=700)
                T(c, "LINED UP: BIGGER" if i == 0 else "AT RIGHT ANGLES: SMALLER", cx, 850, 30, ts, "#cfe3ff", 1, w=700, fam="Inter", maxw=800)
        stamp(c, "GONE", 960, 300, prog(t, tg + 0.3, 0.4), 1.0, color=RED, size=110)
    run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), lambda c, ts: pBul(c, ts, B(1, 0), B(2, 0))), (B(2, 0), lambda c, ts: pBars(c, ts, B(2, 0))),
                                (B(3, 0), pD), (B(4, 0), pE)])

# ------------------------------------------------------------------ m5_fundy
FUNDY_BB = (-68.6, 43.2, -62.2, 46.6)

def tide_gauge(c, t, x0, ts, amp_m, label=True, a=1.0):
    """harbour wall cross-section with a 5-storey building; amp_m: tidal range shown (m)."""
    base = 960; ppm = 33
    rect(c, x0, 300, 380, base - 300 + 40, "#2a2f4a", a)
    for k in range(6): line(c, x0 + 60, base - k * ppm * 3.2, x0 + 380, base - k * ppm * 3.2, "#ffffff", 2, 0.12 * a)
    lv = base - ppm * amp_m * (0.5 + 0.5 * math.sin(t * 1.1))
    c.drawRect(skia.Rect.MakeLTRB(x0 + 20, lv, x0 + 380, base + 40), paint(shader=lin(0, lv, 0, base, [(0, "#3d8fe0", 0.9 * a), (1, "#123a70", 0.9 * a)])))
    line(c, x0 + 20, lv, x0 + 380, lv, "#cfe9ff", 3, a)
    bx = x0 + 230; by = lv
    c.drawPath(poly([(bx - 60, by - 6), (bx + 60, by - 6), (bx + 45, by + 18), (bx - 45, by + 18)]), paint("#e8eef8", a))
    rect(c, bx - 4, by - 70, 6, 64, "#e8eef8", a)
    c.drawPath(poly([(bx + 2, by - 68), (bx + 40, by - 20), (bx + 2, by - 20)]), paint("#ffb347", a))
    # 5-storey building
    hb = 16 * ppm; bx0 = x0 + 430
    rect(c, bx0, base - hb, 170, hb, "#3a4370", a)
    for f in range(5):
        for w_ in range(3): rect(c, bx0 + 22 + w_ * 50, base - hb + 18 + f * hb / 5, 28, 40, "#ffd27a", 0.75 * a)
    line(c, x0 - 30, base, x0 - 30, base - hb, YEL, 4, a); line(c, x0 - 45, base, x0 - 15, base, YEL, 4, a); line(c, x0 - 45, base - hb, x0 - 15, base - hb, YEL, 4, a)
    if label: T(c, "16 M", x0 - 90, base - hb / 2, 54, ts, YEL, a, maxw=200)
    line(c, x0 - 40, base + 40, x0 + 640, base + 40, "#ffffff", 3, 0.3 * a)

def m5_fundy(c, W, H, t, S):
    B = beats(S, 3)
    def pA(c, ts):
        rr = geo.map_rect(FUNDY_BB, 520, 540, width=820)
        geo.draw_map(c, FUNDY_BB, rr, land="#3a4a7a", sea="#14306a", outline="#9db8ff", outline_w=2)
        rrect(c, rr[0], rr[1], rr[2], rr[3], 18, MBLUE, 0.7, stroke=4)
        px, py = geo.lonlat_xy(-64.3, 45.3, FUNDY_BB, rr)
        map_pin(c, px, py, 16, t, vis(t, B(0, 0.05)))
        C(c, "BAY OF FUNDY, CANADA", rr[0] + rr[2] / 2, rr[1] - 50, vis(t, B(0, 0.0)), ts, size=34, dot=TIDE)
        tide_gauge(c, t, 1180, ts, 16 * eout(prog(t, B(0, 0.1), 1.5)))
        C(c, "≈ A 5-STORY BUILDING", 1460, 220, vis(t, B(0, 0.6)), ts, size=34, dot=YEL)
    def pB(c, ts):
        g = ease(prog(t, B(1, 0.1), 2.0))
        tide_gauge(c, t, 1180, ts, lerp(16, 16 * 0.32, g), label=False)
        T(c, "WITHOUT THE MOON", 1460, 200, 50, ts, SILVER, vis(t, B(1, 0.1)), maxw=800)
        # tidal turbine
        cx, cy = 520, 560
        rect(c, cx - 14, cy, 28, 420, "#4a5378")
        spin = t * lerp(220, 50, g)
        c.save(); c.translate(cx, cy); c.rotate(spin)
        for k in range(3):
            c.rotate(120); c.drawPath(poly([(-14, 0), (0, -230), (14, 0)]), paint("#d9e2f2", 0.95))
        c.restore()
        circle(c, cx, cy, 30, "#9db8ff")
        for k in range(5):
            q = (t * lerp(0.6, 0.15, g) + k / 5) % 1
            arrow(c, 120 + q * 200, 420 + k * 70, 220 + q * 200, 420 + k * 70, TIDE, 6, 0.6 * math.sin(q * math.pi))
        C(c, "TIDAL POWER: MUCH WEAKER", 520, 220, vis(t, B(1, 0.45)), ts, size=36, bg="#2a1030", dot=RED)
    def pC(c, ts):
        stage_bg(c, "#2a3a7a", "#101a40")
        c.drawPath(poly([(0, 380), (1920, 900), (1920, VH), (0, VH)]), paint("#c9ab7a"))
        g = ease(prog(t, B(2, 0.25), 1.5))
        hi = lerp(470, 600, g); lo = lerp(850, 720, g)
        def yb(x): return 380 + x / 1920 * 520
        xh, xl = (hi - 380) / 520 * 1920, (lo - 380) / 520 * 1920
        c.drawPath(poly([(xh, yb(xh)), (xl, yb(xl)), (xl, yb(xl) + 30), (xh, yb(xh) + 30)]), paint(TIDE, 0.25))
        rng = random.Random(4)
        for k in range(26):
            x = rng.uniform(xh + 20, xl - 20); yy = yb(x) - 6
            kind = k % 3
            if kind == 0: oval(c, x, yy, 16, 9, "#1c2238")
            elif kind == 1:
                for j in range(3): line(c, x + j * 8, yy, x + j * 8 + 10 * math.sin(t * 2 + k + j), yy - 46, "#3f9a5a", 5)
            else: crab(c, x, yy - 6, 26, t, walk=0.0)
        c.drawPath(poly([(xl, yb(xl)), (1920, yb(1920)), (1920, VH), (xl, VH)]), paint("#2f6fb8", 0.85))
        line(c, xh, yb(xh) - 140, xh, yb(xh) + 40, YEL, 4, dash=([12, 10], 0)); line(c, xl, yb(xl) - 140, xl, yb(xl) + 40, TIDE, 4, dash=([12, 10], 0))
        T(c, "HIGH", xh, yb(xh) - 175, 36, ts, YEL, 1, maxw=300); T(c, "LOW", xl, yb(xl) - 175, 36, ts, TIDE, 1, maxw=300)
        C(c, "THE ZONE BETWEEN THE TIDES", 560, 150, vis(t, B(2, 0.05)), ts, size=36, dot=TIDE)
        C(c, "SHRINKS", 1500, 200, vis(t, B(2, 0.5)), ts, size=40, bg="#2a1030", dot=RED)
    run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB), (B(2, 0), pC)])

# ------------------------------------------------------------------ m5_reef
GBR_BB = (138.0, -27.0, 156.0, -9.0)

def m5_reef(c, W, H, t, S):
    mode = S.opts.get("mode")
    if mode == "short":
        tv = S.lt(1, 0.55) if S.n() > 1 else S.dur * 0.6
        def pS(c, ts):
            g = 1 - (ease((t - tv) / 1.2) if t > tv else 0)
            underwater(c, t, glow=max(g, 0.2), shafts=g)
            moon_vanish(c, 1500, -20, 110, t, tv, ghost=False)
            spawn_bundles(c, t, 0.3, sync=True, a=g, n=200)
            spawn_bundles(c, t, tv, sync=False, a=1 - g, n=200, rate=0.6, seed=8)
            C(c, "GREAT BARRIER REEF", 520, 160, vis(t, S.lt(1, 0.05) if S.n() > 1 else 0.2), ts, size=34, dot=TIDE)
            C(c, "SPAWNING CUE: LOST", 960, 560, vis(t, tv + 0.6), ts, size=40, bg="#2a1030", dot=RED)
        run_panels(c, W, H, t, S, [(0, pS)])
        return
    B = beats(S, 4)
    def pA(c, ts):
        underwater(c, t)
        circle(c, 1500, -40, 260, "#cfe0ff", 0.25, blur=80)
        fish_school(c, t)
        C(c, "MANY LIVING THINGS KEEP MOON TIME", 960, 200, vis(t, B(0, 0.1)), ts, size=38, dot=SILVER)
    def pB(c, ts):
        underwater(c, t)
        circle(c, 1500, -40, 260, "#cfe0ff", 0.3, blur=80)
        spawn_bundles(c, t, B(1, 0.35), sync=True, n=260)
        rr = geo.map_rect(GBR_BB, 260, 330, width=330)
        geo.draw_map(c, GBR_BB, rr, land="#3a4a7a", sea="#14306a", outline="#9db8ff", outline_w=1.5)
        rrect(c, rr[0], rr[1], rr[2], rr[3], 12, MBLUE, 0.7, stroke=3)
        for lon, lat in ((146.0, -16.5), (147.5, -18.5), (149.5, -20.5), (151.5, -22.5)):
            px, py = geo.lonlat_xy(lon, lat, GBR_BB, rr); circle(c, px, py, 6, TIDE, 0.9)
        C(c, "GREAT BARRIER REEF", 260, rr[1] - 40, vis(t, B(1, 0.0)), ts, size=30, dot=TIDE)
        C(c, "NIGHTS AFTER A FULL MOON", 1200, 170, vis(t, B(1, 0.2)), ts, size=36, dot=SILVER)
        C(c, "MASS SPAWNING", 1200, 280, vis(t, B(1, 0.45)), ts, size=36, dot="#ffb39a")
    def pC(c, ts):
        underwater(c, t, glow=0.6, shafts=0.4)
        moon_d(c, 1650, 150, 80)
        # blue light waves to the polyp
        for k in range(3):
            q = (t * 0.5 + k / 3) % 1
            p = skia.Path(); x0, y0, x1, y1 = 1560, 200, 820, 560
            for i in range(41):
                f = i / 40; xx, yy = lerp(x0, x1, f), lerp(y0, y1, f)
                off = math.sin(f * 30 - t * 6 + k) * 14
                pt = (xx + off * 0.44, yy + off * 0.9)
                if i == 0: p.moveTo(*pt)
                else: p.lineTo(*pt)
            c.drawPath(p, paint("#6aa8ff", 0.6 * (0.5 + 0.5 * math.sin(t * 2 + k)), stroke=4))
        # polyp
        px, py = 700, 760
        rrect(c, px - 70, py - 40, 140, 300, 50, "#b06a8a")
        for k in range(8):
            an = -math.pi / 2 + (k - 3.5) * 0.28
            L = 150 + 15 * math.sin(t * 2 + k)
            line(c, px, py - 20, px + math.cos(an) * L, py - 20 + math.sin(an) * L, "#e6a0b8", 14)
            circle(c, px + math.cos(an) * L, py - 20 + math.sin(an) * L, 10, "#ffd2e0")
        # DNA helix
        hx, hy = 1350, 640
        for i in range(24):
            yy = hy - 260 + i * 22; ph = i * 0.5 + t * 1.5
            xa, xb = hx + math.sin(ph) * 80, hx - math.sin(ph) * 80
            line(c, xa, yy, xb, yy, "#ffffff", 3, 0.35)
            circle(c, xa, yy, 9, TIDE); circle(c, xb, yy, 9, MBLUE)
        C(c, "2007: A LIGHT-SENSING GENE", 1350, 230 if not S.P else 300, vis(t, B(2, 0.05)), ts, size=36, dot=TIDE)
        C(c, "SENSES BLUE MOONLIGHT", 1350, 960, vis(t, B(2, 0.4)), ts, size=36, dot="#6aa8ff")
        C(c, "NO EYES NEEDED", 560, 230, vis(t, B(2, 0.75)), ts, size=34)
    def pD(c, ts):
        underwater(c, t, glow=0.15, shafts=0.0)
        spawn_bundles(c, t, B(3, 0), sync=False, n=300, rate=0.8, seed=9)
        C(c, "NO MOONLIGHT CUE", 960, 200, vis(t, B(3, 0.05)), ts, size=38, bg="#2a1030", dot=RED)
        C(c, "OUT OF SYNC = FEWER EGGS FERTILIZED", 960, 320, vis(t, B(3, 0.45)), ts, size=34)
    run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB), (B(2, 0), pC), (B(3, 0), pD)])

# ------------------------------------------------------------------ m5_crabs
XMAS_BB = (94.0, -22.0, 122.0, 2.0)

def m5_crabs(c, W, H, t, S):
    B = beats(S, 2)
    def pA(c, ts):
        rr = geo.map_rect(XMAS_BB, 470, 560, width=760)
        geo.draw_map(c, XMAS_BB, rr, land="#3a4a7a", sea="#14306a", outline="#9db8ff", outline_w=1.5)
        rrect(c, rr[0], rr[1], rr[2], rr[3], 16, MBLUE, 0.7, stroke=4)
        px, py = geo.lonlat_xy(105.6, -10.5, XMAS_BB, rr)
        map_pin(c, px, py, 14, t)
        T(c, "INDIAN OCEAN", rr[0] + rr[2] * 0.35, rr[1] + rr[3] * 0.8, 30, ts, "#9db8ff", 0.8, w=700, fam="Inter", maxw=400)
        C(c, "CHRISTMAS ISLAND", 470, rr[1] - 45, vis(t, B(0, 0.0)), ts, size=34, dot=RED)
        # crab march
        stage_x0 = 980
        rrect(c, stage_x0, 260, 880, 640, 30, "#1b2a2a")
        c.save(); c.clipRect(skia.Rect.MakeXYWH(stage_x0, 260, 880, 640))
        c.drawRect(skia.Rect.MakeXYWH(1700, 260, 200, 640), paint("#2f6fb8"))
        rng = random.Random(6)
        for k in range(40):
            x = stage_x0 + ((rng.random() * 900 + t * rng.uniform(40, 70)) % 760)
            y = 300 + rng.random() * 580
            crab(c, x, y, 34, t + k, walk=1.0)
        c.restore()
        rrect(c, stage_x0, 260, 880, 640, 30, MBLUE, 0.5, stroke=3)
        C(c, "MILLIONS MARCH TO THE SEA", 1420, 200, vis(t, B(0, 0.3)), ts, size=34, dot=RED)
    def pB(c, ts):
        stage_bg(c, "#1a2560", "#e8a07a")
        c.drawRect(skia.Rect.MakeLTRB(0, 620, VW, VH), paint(shader=lin(0, 620, 0, VH, [(0, "#2f6fb8", 1), (1, "#163f78", 1)])))
        c.drawPath(poly([(0, 760), (900, 700), (1150, 1080), (0, 1080)]), paint("#3a2a24"))
        for k in range(14):
            x = 300 + k * 50 + (k % 3) * 10; y = 780 + (k % 4) * 30 + 0.2 * (x - 300)
            crab(c, x, y, 40, t + k, walk=0.3)
            if t > B(1, 0.05):
                q = ((t - B(1, 0.05)) * 0.6 + k * 0.17) % 1
                for j in range(5):
                    circle(c, x + 60 + q * 220 + j * 9, y - 10 + math.sin(j + q * 6) * 12 + q * 40, 4, "#ffd2b8", 0.9 * (1 - q))
        tv = B(1, 0.68)
        mx, my = 1500, 230
        if t < tv: moon_d(c, mx, my, 85, phase_=0.5, waxing=False)
        else: moon_vanish(c, mx, my, 85, t, tv)
        C(c, "LAST QUARTER MOON", 1500, 380, vis(t, B(1, 0.15), tv), ts, size=34, dot=SILVER)
        C(c, "EGGS AT DAWN, AS THE HIGH TIDE TURNS", 760, 180, vis(t, B(1, 0.05)), ts, size=32, dot=TIDE)
        C(c, "CALENDAR: GONE", 1500, 380, vis(t, tv + 0.5), ts, size=36, bg="#2a1030", dot=RED)
    run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB)])

# ------------------------------------------------------------------ m5_beetle
def m5_beetle(c, W, H, t, S):
    B = beats(S, 3)
    def pA(c, ts):
        stage_bg(c, "#0d1440", "#25305e")
        stars(c, VW, VH, t, 0.5, seed=71)
        mx, my = 1600, 180
        moon_d(c, mx, my, 60)
        pa = vis(t, B(0, 0.25))
        if pa > 0:
            for gx in range(0, 21):
                for gy in range(0, 8):
                    x, y = 60 + gx * 92, 90 + gy * 80
                    dx, dy = x - mx, y - my; d = math.hypot(dx, dy)
                    if d < 140: continue
                    tx, ty = -dy / d, dx / d
                    al = pa * clamp(d / 1200) * (0.45 + 0.2 * math.sin(t * 2 + gx * 0.4 + gy))
                    line(c, x - tx * 22, y - ty * 22, x + tx * 22, y + ty * 22, TIDE, 4, al)
        c.drawPath(poly([(0, 800), (1920, 760), (1920, VH), (0, VH)]), paint("#151a2c"))
        acacia(c, 1500, 790, 380, "#0a0d18"); acacia(c, 240, 800, 260, "#0a0d18")
        x = lerp(320, 1250, ((t - B(0, 0)) * 0.06) % 1)
        line(c, 300, 880, 1400, 880, "#ffffff", 3, 0.35, dash=([10, 12], 0))
        beetle_ball(c, x, 890, 150, t)
        C(c, "SOUTH AFRICA", 420, 160, vis(t, B(0, 0.0)), ts, size=34, dot=YEL)
        C(c, "POLARIZED MOONLIGHT", 760, 270, vis(t, B(0, 0.3)), ts, size=34, dot=TIDE)
        C(c, "2003: FIRST KNOWN ANIMAL TO NAVIGATE THIS WAY", 900, 980, vis(t, B(0, 0.7)), ts, size=32)
    def pB(c, ts):
        t0, t1 = B(1, 0), B(2, 0)
        stage_bg(c, "#050820", "#020410")
        top = 230; bot = 1000; ppm = (bot - top - 40) / 60
        c.drawRect(skia.Rect.MakeLTRB(0, top, VW, bot), paint(shader=lin(0, top, 0, bot, [(0, "#0f2550", 1), (1, "#030814", 1)])))
        rrect(c, -20, top - 30, VW + 40, 44, 10, "#dfeefa")
        cyc = clamp((t - t0) / max(1.0, 2 * (B(1, 0.55) - t0)))
        lit = 0.5 - 0.5 * math.cos(cyc * 2 * math.pi)
        moon_d(c, 1600, 110, 55, phase_=max(0.02, lit), waxing=cyc < 0.5)
        circle(c, 1600, 110, 120, "#cfe0ff", 0.15 * lit, blur=40)
        for k in range(7):
            yy = top + 20 + k * 10 * ppm
            line(c, 150, yy, 175, yy, "#ffffff", 3, 0.6)
            if k % 2 == 0: T(c, f"{k * 10} M", 120, yy, 26, ts, "#cfe3ff", 0.8, w=700, fam="Inter", align="r", maxw=200)
        depth = 12 + 7 * math.sin((t - t0) * 2 * math.pi / 3.0) + 38 * lit ** 3
        rng = random.Random(4)
        for k in range(110):
            x = 320 + rng.random() * 1450 + math.sin(t + k) * 10
            y = top + 20 + (depth + rng.gauss(0, 4)) * ppm
            oval(c, x, y, 7, 4, "#ffcf9a", 0.9)
            line(c, x - 6, y - 2, x - 18, y - 9, "#ffcf9a", 1.5, 0.7)
        C(c, "ARCTIC POLAR NIGHT", 520, 120, vis(t, t0 + 0.1), ts, size=34, dot=SILVER)
        C(c, "ZOOPLANKTON FOLLOW MOON TIME", 1000, 330, vis(t, B(1, 0.2)), ts, size=32, dot=TIDE)
        C(c, "FULL MOON: SINK ~50 M", 1150, 880, vis(t, B(1, 0.55)), ts, size=34, dot=YEL)
    def pC(c, ts):
        for k, (lab, x) in enumerate((("COMPASS", 420), ("CLOCK", 960), ("HIDING CUE", 1500))):
            p = vis(t, B(2, 0.02 + k * 0.12))
            with Layer(c, p):
                rrect(c, x - 210, 260, 420, 460, 40, "#151b4f"); rrect(c, x - 210, 260, 420, 460, 40, MBLUE, 0.5, stroke=3)
                cy = 450
                if k == 0:
                    circle(c, x, cy, 110, "#ffffff", 0.9, stroke=8)
                    c.save(); c.translate(x, cy); c.rotate(20 + 8 * math.sin(t * 3))
                    c.drawPath(poly([(0, -95), (18, 0), (0, 95), (-18, 0)]), paint(RED)); c.restore()
                elif k == 1: clock(c, x, cy, 110, (t * 0.2) % 1, colr=MBLUE)
                else:
                    oval(c, x, cy, 120, 60, "#ffffff", 0.9); circle(c, x, cy, 42, "#1b2a60"); circle(c, x, cy, 18, "#000000")
                T(c, lab, x, 650, 46, ts, "#ffffff", 1, maxw=380)
            xmark(c, x + 150, 300, 40, prog(t, B(2, 0.3 + k * 0.08), 0.3))
        C(c, "MANY WOULD ADAPT. SOME MIGHT NOT.", 960, 860, vis(t, B(2, 0.65)), ts, size=38, dot=YEL)
    run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB), (B(2, 0), pC)])

# ------------------------------------------------------------------ m5_eclipse
_COR = {}
def corona(c, x, y, R, t, a=1.0):
    k = int(R)
    if k not in _COR:
        n = int(R * 6); surf = skia.Surface(n, n); cc = surf.getCanvas(); cc.clear(skia.ColorTRANSPARENT)
        cx = cy = n / 2; rng = random.Random(3)
        cc.drawCircle(cx, cy, R * 2.6, paint(shader=rad(cx, cy, R * 2.6, [(0.35, "#ffffff", 0.9), (0.45, "#dfe8ff", 0.5), (1, "#6f8fff", 0)])))
        for i in range(70):
            an = rng.random() * 6.28; L = R * rng.uniform(1.3, 2.8); w = R * rng.uniform(0.04, 0.12)
            p = skia.Path(); p.moveTo(cx + math.cos(an + 0.05) * R, cy + math.sin(an + 0.05) * R)
            p.quadTo(cx + math.cos(an) * L * 0.7, cy + math.sin(an) * L * 0.7, cx + math.cos(an) * L, cy + math.sin(an) * L)
            p.lineTo(cx + math.cos(an - 0.05) * R, cy + math.sin(an - 0.05) * R); p.close()
            cc.drawPath(p, paint("#f2f5ff", rng.uniform(0.15, 0.4), blur=w))
        _COR[k] = surf.makeImageSnapshot()
    img = _COR[k]; n = img.width()
    pt = skia.Paint(); pt.setAlphaf(clamp(a * (0.92 + 0.08 * math.sin(t * 2))))
    c.save(); c.translate(x, y); c.rotate(t * 1.5)
    c.drawImage(img, -n / 2, -n / 2, skia.SamplingOptions(skia.FilterMode.kLinear), pt); c.restore()

def total_eclipse(c, x, y, R, t, a=1.0, cover=1.0):
    corona(c, x, y, R, t, a * cover)
    sun_d(c, x, y, R, t, a * (1 - cover))
    if cover > 0: circle(c, x + (1 - cover) * R * 2.2, y, R * 1.01, "#05060c", a)

def tilt_earth(c, x, y, R, tilt, t, ts, label=True, a=1.0, mars=False):
    c.save(); c.translate(x, y); c.rotate(tilt)
    if mars: mars_d(c, 0, 0, R, t, a)
    else: geo.globe(c, 0, 0, int(R), rot=t * 18, tilt=0, light=(-0.8, 0.2, 0.55), a=a)
    line(c, 0, -R * 1.4, 0, R * 1.4, "#ffffff", max(3, R * 0.02), a)
    circle(c, 0, -R * 1.4, R * 0.05, YEL, a)
    c.restore()
    line(c, x, y - R * 1.5, x, y - R * 1.05, "#ffffff", 3, 0.4 * a, dash=([10, 8], 0))
    p = skia.Path(); r = R * 1.25
    p.addArc(skia.Rect.MakeLTRB(x - r, y - r, x + r, y + r), -90, tilt)
    c.drawPath(p, paint(YEL, a, stroke=6))
    if label:
        an = math.radians(-90 + tilt / 2)
        T(c, f"{tilt:.0f}°", x + math.cos(an) * r * 1.22, y + math.sin(an) * r * 1.22, 56, ts, YEL, a, maxw=300)

def mars_d(c, x, y, R, t, a=1.0):
    circle(c, x, y, R * 1.06, "#ff9a6a", 0.25 * a, blur=R * 0.06)
    circle(c, x, y, R, "#c4552e", a)
    rng = random.Random(2)
    c.save(); pth = skia.Path(); pth.addCircle(x, y, R); c.clipPath(pth, doAntiAlias=True)
    for k in range(10):
        an = rng.random() * 6.28; d = rng.random() * R * 0.8
        xx = x + ((math.cos(an) * d + t * R * 0.08) % (2 * R)) - R
        oval(c, xx, y + math.sin(an) * d, R * rng.uniform(0.15, 0.35), R * rng.uniform(0.08, 0.16), "#7a2f1a", a * 0.7)
    oval(c, x, y - R * 0.93, R * 0.35, R * 0.12, "#f4f0ea", a)
    c.drawCircle(x, y, R, paint(shader=rad(x - R * 0.4, y - R * 0.3, R * 1.8, [(0, "#ffffff", 0.15), (0.6, "#000000", 0), (1, "#000000", 0.6)]), a=a))
    c.restore()

def m5_eclipse(c, W, H, t, S):
    mode = S.opts.get("mode")
    if mode == "short":
        tv = S.lt(0, 0.22); t2 = S.lt(0, 0.5)
        def pS(c, ts):
            g = ease((t - tv) / 0.8) if t > tv else 0
            total_eclipse(c, 960, 520, 210, t, cover=1 - g)
            if t > tv: moon_vanish(c, 960, 520, 212, t, tv, ghost=False, glow=0)
            stamp(c, "NO MORE", 960, 930, prog(t, tv + 0.4, 0.4), 1.0, color=RED, size=80)
        def pT(c, ts):
            tilt_earth(c, 960, 560, 300, 23 + 30 * math.sin((t - t2) * 0.9) + 12 * math.sin((t - t2) * 2.3), t, ts)
        run_panels(c, W, H, t, S, [(0, pS), (t2, pT)])
        return
    B = beats(S, 5)
    def pA(c, ts):
        total_eclipse(c, 960, 420, 165, t)
        C(c, "TOTAL SOLAR ECLIPSE", 960, 120, vis(t, S.le(0) + 0.1), ts, size=36, dot=SILVER)
    def pB(c, ts):
        months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
        icons = {2: "s", 3: "l", 8: "s", 9: "l"}
        for i, mth in enumerate(months):
            x = 300 + (i % 6) * 264; y = 330 + (i // 6) * 300
            p = vis(t, B(1, 0.0) + i * 0.04)
            rrect(c, x - 110, y - 120, 220, 240, 20, "#151b4f", p); rrect(c, x - 110, y - 120, 220, 240, 20, MBLUE, 0.5 * p, stroke=3)
            T(c, mth, x, y - 80, 36, ts, "#cfe3ff", p, w=800, maxw=200)
            if i in icons:
                if icons[i] == "s":
                    circle(c, x, y + 20, 56, "#fff3c0", 0.6 * p, blur=14); circle(c, x, y + 20, 46, "#05060c", p)
                else: moon_d(c, x, y + 20, 46, p, glow=0); circle(c, x, y + 20, 46, "#c0392b", 0.55 * p)
                xmark(c, x, y + 20, 50, prog(t, B(1, 0.45) + (i % 6) * 0.06, 0.3))
        C(c, "NO SOLAR ECLIPSES", 620, 960, vis(t, B(1, 0.5)), ts, size=36, bg="#2a1030", dot=RED)
        C(c, "NO LUNAR ECLIPSES", 1300, 960, vis(t, B(1, 0.7)), ts, size=36, bg="#2a1030", dot=RED)
    def pC(c, ts):
        ex, ey = 140, 560; mxp, mr = 400, 32; sxp, sr = 1740, 199
        pa = vis(t, B(2, 0.35))
        for sgn in (-1, 1):
            line(c, ex, ey, sxp, ey + sgn * sr, "#ffffff", 2, 0.5 * pa, dash=([12, 10], 0))
        sun_d(c, sxp, ey, sr, t)
        moon_d(c, mxp, ey, mr, glow=0.8)
        circle(c, ex, ey, 22, TIDE); T(c, "YOU", ex, ey + 60, 30, ts, TIDE, 1, maxw=200)
        T(c, "MOON", mxp, ey + 80, 34, ts, SILVER, vis(t, B(2, 0.05)), maxw=300)
        C(c, "SUN: ~400× WIDER", sxp - 120, 230, vis(t, B(2, 0.15)), ts, size=36, dot=SUNY)
        C(c, "...AND ~400× FARTHER AWAY", 900, 860, vis(t, B(2, 0.4)), ts, size=36, dot=MBLUE)
        C(c, "SAME SIZE IN YOUR SKY", 900, 200, vis(t, B(2, 0.7)), ts, size=40, bg=YEL, fg="#0b1030", a=1)
    def pD(c, ts):
        total_eclipse(c, 330, 560, 170, t)
        for k in range(3):
            an = -0.6 + k * 0.5
            p = skia.Path(); bx, by = 330 + math.cos(an) * 170, 560 + math.sin(an) * 170
            p.moveTo(bx, by); p.cubicTo(bx + math.cos(an) * 90, by + math.sin(an) * 90 - 50, bx + math.cos(an + 0.3) * 120, by + math.sin(an + 0.3) * 120, 330 + math.cos(an + 0.25) * 170, 560 + math.sin(an + 0.25) * 170)
            c.drawPath(p, paint("#ff5a5a", 0.85, stroke=10))
        x0, x1, y = 760, 1820, 520
        c.drawRect(skia.Rect.MakeLTRB(x0, y - 70, x1, y + 70), paint(shader=skia.GradientShader.MakeLinear([skia.Point(x0, y), skia.Point(x1, y)],
                   [col(h) for h in ("#7a3cff", "#2f6bff", "#2fd0ff", "#3dff6f", "#fff23d", "#ff9a2f", "#ff3d3d")])))
        c.drawRect(skia.Rect.MakeLTRB(x0, y - 70, x1, y + 70), paint("#000000", 0.55))
        hx = x0 + (x1 - x0) * 0.62
        ph = prog(t, B(3, 0.3), 0.4)
        rect(c, hx - 5, y - 70, 10, 140, "#fff6a0", ph); circle(c, hx, y, 50, "#fff6a0", 0.4 * ph, blur=20)
        rrect(c, x0, y - 70, x1 - x0, 140, 8, "#ffffff", 0.5, stroke=3)
        C(c, "1868 ECLIPSE", 1290, 230, vis(t, B(3, 0.0)), ts, size=38, dot=SUNY)
        C(c, "A LINE NO KNOWN ELEMENT MADE", 1290, 700, vis(t, B(3, 0.35)), ts, size=32)
        stamp(c, "HELIUM", 1290, 860, prog(t, B(3, 0.6), 0.4), 1.0, color=YEL, size=90, rot=-6)
    def pE(c, ts):
        sx, sy = 1000, 560
        total_eclipse(c, sx, sy, 120, t)
        stx, sty = 1700, 330
        circle(c, stx, sty, 10, "#ffffff", 0.35); T(c, "TRUE POSITION", stx, sty + 55, 32, ts, "#cfe3ff", vis(t, B(4, 0.45)), w=700, fam="Inter", maxw=400)
        ex, ey = 160, 640
        circle(c, ex, ey, 20, TIDE); T(c, "EARTH", ex, ey + 55, 28, ts, TIDE, 1, maxw=200)
        pr = eout(prog(t, B(4, 0.1), 1.2))
        p = skia.Path(); p.moveTo(stx, sty); p.quadTo(sx + 40, sy - 210, ex, ey)
        c.drawPath(p, paint(SUNY, 0.9, stroke=5, dash=([2400 * pr, 3000], 0)))
        ap = vis(t, B(4, 0.45))
        line(c, ex, ey, 1760, 250, "#ffffff", 3, 0.6 * ap, dash=([12, 10], 0))
        circle(c, 1760, 250, 14, "#ffffff", ap); circle(c, 1760, 250, 30, "#ffffff", 0.35 * ap, blur=10)
        T(c, "WHERE IT APPEARS", 1640, 195, 32, ts, "#ffffff", ap, w=700, fam="Inter", maxw=400)
        C(c, "1919: STARLIGHT BENDS", 620, 200, vis(t, B(4, 0.0)), ts, size=38, dot=SUNY)
        C(c, "EINSTEIN'S PREDICTION", 1000, 900, vis(t, B(4, 0.7)), ts, size=36, dot=GREEN)
        check(c, 1000 + (290 if not S.P else 500), 900, 26, vis(t, B(4, 0.8)))
    run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB), (B(2, 0), pC), (B(3, 0), pD), (B(4, 0), pE)])

# ------------------------------------------------------------------ m5_sky
_MW = {}
def milky_way():
    if "mw" not in _MW:
        surf = skia.Surface(VW, VH); cc = surf.getCanvas(); cc.clear(skia.ColorTRANSPARENT)
        rng = random.Random(12)
        cc.save(); cc.translate(VW / 2, VH / 2); cc.rotate(-24)
        cc.drawRect(skia.Rect.MakeLTRB(-1300, -170, 1300, 170), paint(shader=lin(0, -170, 0, 170, [(0, "#8aa0ff", 0), (0.5, "#c9d4ff", 0.22), (1, "#8aa0ff", 0)])))
        for i in range(3500):
            x = rng.uniform(-1200, 1200); y = rng.gauss(0, 90)
            cc.drawCircle(x, y, rng.uniform(0.6, 1.8), paint(rng.choice(["#ffffff", "#dfe6ff", "#fff1d6"]), rng.uniform(0.3, 0.9)))
        for i in range(14):
            x = rng.uniform(-1100, 1100); y = rng.gauss(0, 40)
            cc.drawOval(skia.Rect.MakeLTRB(x - 90, y - 18, x + 90, y + 18), paint("#0a0c1a", 0.45, blur=14))
        cc.restore()
        for (gx, gy, r, an) in ((300, 230, 60, 30), (1600, 820, 45, -20), (1250, 180, 35, 60)):
            cc.save(); cc.translate(gx, gy); cc.rotate(an)
            cc.drawOval(skia.Rect.MakeLTRB(-r, -r * 0.4, r, r * 0.4), paint(shader=rad(0, 0, r, [(0, "#fff2dc", 0.9), (0.4, "#c9b8ff", 0.35), (1, "#000000", 0)])))
            cc.restore()
        _MW["mw"] = surf.makeImageSnapshot()
    return _MW["mw"]

def m5_sky(c, W, H, t, S):
    B = beats(S, 2)
    def pA(c, ts):
        stage_bg(c, "#020312", "#070a24")
        stars(c, VW, VH, t, 1.0, seed=81, density=1.5)
        g = 1 - ease(prog(t, B(0, 0.2), 1.6))
        pt = skia.Paint(); pt.setAlphaf(clamp(1 - g * 0.85))
        c.drawImage(milky_way(), 0, 0, skia.SamplingOptions(), pt)
        if g > 0:
            c.drawRect(skia.Rect.MakeXYWH(0, 0, VW, VH), paint(shader=rad(1500, 250, 1500, [(0, "#dfe8ff", 0.65 * g), (0.4, "#5a70b0", 0.4 * g), (1, "#1a2350", 0.3 * g)])))
            moon_d(c, 1500, 250, 80, g)
        c.drawPath(poly([(0, 950), (500, 900), (1100, 960), (1920, 910), (1920, VH), (0, VH)]), paint("#020208"))
        rect(c, 1350, 840, 60, 90, "#0b0d18"); c.drawPath(poly([(1330, 850), (1380, 800), (1430, 850)]), paint("#0b0d18"))
        C(c, "FULL MOON GLARE", 1500, 420, vis(t, B(0, 0.0), B(0, 0.3)), ts, size=32, dot=SILVER)
        C(c, "DARK SKIES, EVERY NIGHT", 760, 160, vis(t, B(0, 0.45)), ts, size=40, dot=YEL)
    def pB(c, ts):
        cx, cy, rr = 960, 540, 330
        gone = B(1, 0.72)
        for k in range(8):
            an = -math.pi / 2 + k * math.pi / 4
            x, y = cx + math.cos(an) * rr, cy + math.sin(an) * rr
            f = 0.5 - 0.5 * math.cos(k * math.pi / 4)
            p = vis(t, B(1, 0.02 + k * 0.04))
            ga = 1 - (ease((t - gone - k * 0.05) / 0.5) if t > gone else 0)
            moon_d(c, x, y, 52, p * ga, glow=0, phase_=max(0.03, f), waxing=k <= 4)
            circle(c, x, y, 52, MBLUE, p * (1 - ga) * 0.6, stroke=3, dash=([10, 8], 0))
        T(c, "29.5", cx, cy - 30, 140, ts, "#ffffff", vis(t, B(1, 0.2)), maxw=600)
        T(c, "DAYS", cx, cy + 70, 46, ts, "#cfe3ff", vis(t, B(1, 0.25)), maxw=400)
        C(c, "THE FIRST 'MONTH'", 330, 160, vis(t, B(1, 0.1)), ts, size=34, dot=SILVER)
        C(c, "MOON CALENDARS: NOTHING TO COUNT", 960, 980, vis(t, gone + 0.3), ts, size=34, bg="#2a1030", dot=RED)
    run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB)])

# ------------------------------------------------------------------ m5_tilt
def chaos_tilt(tt):
    return clamp(42 + 26 * math.sin(tt * 0.9) + 14 * math.sin(tt * 2.3 + 1) + 6 * math.sin(tt * 4.1 + 2), 0, 86)

def gauge_arc(c, x, y, r, lo, hi, a, ts, colr=RED, label=None):
    p = skia.Path(); p.addArc(skia.Rect.MakeLTRB(x - r, y - r, x + r, y + r), -90, 90)
    c.drawPath(p, paint("#ffffff", 0.15 * a, stroke=26, cap="butt"))
    p2 = skia.Path(); p2.addArc(skia.Rect.MakeLTRB(x - r, y - r, x + r, y + r), -90 + lo, hi - lo)
    c.drawPath(p2, paint(colr, a, stroke=26, cap="butt"))
    for d in (0, 30, 60, 90):
        an = math.radians(-90 + d)
        T(c, f"{d}°", x + math.cos(an) * (r + 60), y + math.sin(an) * (r + 60), 28, ts, "#cfe3ff", a, w=700, fam="Inter", maxw=200)
    if label: T(c, label, x + r * 0.45, y + 80, 34, ts, colr, a, maxw=600)

def m5_tilt(c, W, H, t, S):
    mode = S.opts.get("mode")
    if mode == "debate":
        B = beats(S, 3)
        def pG(c, ts):
            gx0, gy0, gx1, gy1 = 260, 220, 1700, 860
            rect(c, gx0, gy0, gx1 - gx0, gy1 - gy0, "#0b1030", 0.6)
            line(c, gx0, gy1, gx1, gy1, "#ffffff", 3, 0.7); line(c, gx0, gy0, gx0, gy1, "#ffffff", 3, 0.7)
            def yv(d): return gy1 - d / 90 * (gy1 - gy0)
            for d in (0, 30, 60, 90):
                T(c, f"{d}°", gx0 - 40, yv(d), 28, ts, "#cfe3ff", 0.8, w=700, fam="Inter", align="r", maxw=200)
                line(c, gx0, yv(d), gx1, yv(d), "#ffffff", 1, 0.12)
            T(c, "TILT OVER HUNDREDS OF MILLIONS OF YEARS", (gx0 + gx1) / 2, gy1 + 60, 30, ts, "#cfe3ff", 0.8, w=700, fam="Inter", maxw=1300)
            pr1 = eout(prog(t, B(0, 0.05), 1.5)); pr2 = eout(prog(t, B(0, 0.45), 2.5))
            for (fn, pr, colr, al) in ((lambda q: chaos_tilt(q * 14), pr1, RED, 0.55), (lambda q: 23 + 8 * math.sin(q * 9) + 4 * math.sin(q * 23 + 1), pr2, TIDE, 1.0)):
                if pr <= 0: continue
                p = skia.Path(); n = int(200 * pr) + 2
                for i in range(n):
                    q = i / 200; x = lerp(gx0, gx1, q); y = yv(fn(q))
                    if i == 0: p.moveTo(x, y)
                    else: p.lineTo(x, y)
                c.drawPath(p, paint(colr, al, stroke=6))
            C(c, "FEARED (1993)", 1500, 160, vis(t, B(0, 0.1)), ts, size=30, bg="#2a1030", dot=RED)
            C(c, "2011 SIMULATIONS", 1500, 260 if not S.P else 300, vis(t, B(0, 0.5)), ts, size=30, dot=TIDE)
            pb = vis(t, B(1, 0.1))
            if pb > 0:
                rect(c, gx0, yv(31), gx1 - gx0, yv(15) - yv(31), TIDE, 0.12 * pb)
                C(c, "~10–20° SWING", 1000, yv(52), pb, ts, size=38, bg=YEL, fg="#0b1030", a=1)
                C(c, "TODAY: ~2.6°", 520, yv(5), vis(t, B(1, 0.5)), ts, size=30)
        def pE(c, ts):
            tilt_earth(c, 760, 560, 270, 23 + 6 * math.sin(t * 1.3), t, ts)
            moon_d(c, 1450, 330, 70)
            C(c, "THE MOON HELPS", 1450, 500, vis(t, B(2, 0.1)), ts, size=36, dot=SILVER)
            C(c, "BUT MAYBE LESS WILD THAN FEARED", 1300, 860, vis(t, B(2, 0.4)), ts, size=34, dot=TIDE)
        run_panels(c, W, H, t, S, [(0, pG), (B(2, 0), pE)])
        return
    B = beats(S, 4)
    def pA(c, ts):
        tilt_earth(c, 960, 560, 300, 23.4, t, ts, label=t > B(0, 0.3))
        C(c, "EARTH'S TILT", 960, 120, vis(t, B(0, 0.05)), ts, size=38, dot=YEL)
    def pB(c, ts):
        tl = 23.25 + 1.3 * math.sin(t * 1.4)
        tilt_earth(c, 640, 560, 270, tl, t, ts)
        gauge_arc(c, 1450, 770, 280, 22.0, 24.5, 1, ts, colr=TIDE)
        C(c, "SEASONS", 1450, 150, vis(t, B(1, 0.05)), ts, size=34, dot=SUNY)
        C(c, "~22° TO ~24.5°", 1450, 245, vis(t, B(1, 0.4)), ts, size=36, dot=TIDE)
        C(c, "OVER ~40,000 YEARS", 1450, 340, vis(t, B(1, 0.6)), ts, size=34)
    def pC(c, ts):
        tl = chaos_tilt(t - B(2, 0))
        tilt_earth(c, 640, 560, 270, tl, t, ts)
        gauge_arc(c, 1450, 770, 280, 0, 85 * eout(prog(t, B(2, 0.55), 1.0)), 1, ts, colr=RED)
        C(c, "LASKAR ET AL., 1993", 1450, 150, vis(t, B(2, 0.05)), ts, size=34, dot=SILVER)
        C(c, "0° TO 85°+, CHAOTICALLY", 1450, 260, vis(t, B(2, 0.6)), ts, size=36, bg="#2a1030", dot=RED)
    def pD(c, ts):
        tl = 35 + 22 * math.sin((t - B(3, 0)) * 1.1) + 5 * math.sin(t * 2.7)
        tilt_earth(c, 640, 560, 250, tl, t, ts, mars=True)
        sun_d(c, 1700, 560, 70, t, glow=0.6)
        C(c, "MARS: NO BIG MOON", 1300, 170, vis(t, B(3, 0.05)), ts, size=36, dot="#ff8a5a")
        C(c, "BELOW 10° TO ABOVE 60°", 1300, 280, vis(t, B(3, 0.3)), ts, size=34)
        C(c, "POLES FACING THE SUN FOR MONTHS", 1200, 920, vis(t, B(3, 0.7)), ts, size=32, dot=SUNY)
    run_panels(c, W, H, t, S, [(0, pA), (B(1, 0), pB), (B(2, 0), pC), (B(3, 0), pD)])

# ------------------------------------------------------------------ m5_day
def rudist(c, x, y, s, t, a=1.0):
    p = skia.Path(); p.moveTo(x - s * 0.5, y - s * 1.6); p.lineTo(x + s * 0.5, y - s * 1.6); p.lineTo(x + s * 0.12, y + s * 0.4); p.lineTo(x - s * 0.12, y + s * 0.4); p.close()
    c.drawPath(p, paint(shader=lin(x - s * 0.5, y, x + s * 0.5, y, [(0, "#a88a62", a), (0.5, "#e8d6b0", a), (1, "#8a6e4a", a)])))
    for k in range(26):
        yy = y - s * 1.55 + k * s * 0.075; w = lerp(0.5, 0.14, k / 26) * s
        line(c, x - w, yy, x + w, yy, "#6b5236", max(1, s * 0.012), a * 0.6)
    oval(c, x, y - s * 1.6, s * 0.52, s * 0.12, "#c9b08a", a); oval(c, x, y - s * 1.6, s * 0.52, s * 0.12, "#6b5236", a, stroke=3)

def m5_day(c, W, H, t, S):
    mode = S.opts.get("mode")
    def pBrake(c, ts, t0, short=False):
        ex, ey, R = 760, 560, 230
        mx = 1650
        polar_tides(c, t, ex, ey, R, 0.2, 18, mx=mx, mR=62)
        p = skia.Path(); r = R * 1.42
        p.addArc(skia.Rect.MakeLTRB(ex - r, ey - r, ex + r, ey + r), 120, 110)
        c.drawPath(p, paint("#ffffff", 0.8, stroke=8))
        an = math.radians(230); hx, hy = ex + math.cos(an) * r, ey + math.sin(an) * r
        arrow(c, hx - 30, hy + 25, hx + 6, hy - 6, "#ffffff", 8)
        T(c, "SPIN", ex - r - 40, ey, 30, ts, "#ffffff", 0.8, w=800, align="r", maxw=200)
        pb = vis(t, t0 + 0.6)
        if pb > 0:
            p2 = skia.Path(); r2 = R * 1.62
            p2.addArc(skia.Rect.MakeLTRB(ex - r2, ey - r2, ex + r2, ey + r2), -60, 50)
            c.drawPath(p2, paint(RED, pb, stroke=10))
            C(c, "TIDAL BRAKE", 1300 if not S.P else 1250, 170 if not S.P else 120, pb, ts, size=38, bg="#2a1030", dot=RED)
        pm = vis(t, t0 + (1.6 if not short else 1.2))
        if pm > 0:
            arrow(c, mx, 470, mx + 90, 400, TIDE, 9, pm)
            C(c, "MOON NUDGED OUTWARD", 1560 if not S.P else 1250, 300 if not S.P else 960, pm, ts, size=30, dot=TIDE)
        if not short: C(c, "+1.8 MILLISECONDS PER CENTURY", 1200, 930, vis(t, B(0, 0.6)), ts, size=36, bg=YEL, fg="#0b1030", a=1)
    def pShell(c, ts, t0):
        rudist(c, 470, 820, 260, t)
        trex(c, 1640, 930, 110, t, colr="#0a0c1a", walk=True)
        clock(c, 1180, 470, 190, 23.5 / 24, colr=MBLUE)
        T(c, "23.5 H", 1180, 730, 80, ts, "#ffffff", vis(t, t0 + 0.3), maxw=500)
        C(c, "70 MILLION YEARS AGO", 900, 150, vis(t, t0 + 0.05), ts, size=36, dot=YEL)
        C(c, "372 DAYS A YEAR", 1180, 850, vis(t, t0 + (1.6 if not S.P else 1.2)), ts, size=34, dot=TIDE)
        T(c, "FOSSIL SHELL", 470, 950, 34, ts, "#cfe3ff", vis(t, t0 + 0.2), w=700, fam="Inter", maxw=500)
    if mode == "brake":
        t0 = S.ls(1) if S.n() > 1 else 0
        run_panels(c, W, H, t, S, [(0, lambda c, ts: pBrake(c, ts, t0, short=True))]); return
    if mode == "shell":
        run_panels(c, W, H, t, S, [(0, lambda c, ts: pShell(c, ts, 0))]); return
    B = beats(S, 3)
    def pG(c, ts):
        gx0, gy0, gx1, gy1 = 300, 230, 1650, 850
        line(c, gx0, gy1, gx1, gy1, "#ffffff", 3, 0.7); line(c, gx0, gy0, gx0, gy1, "#ffffff", 3, 0.7)
        T(c, "LENGTH OF DAY", gx0 - 30, gy0 - 40, 30, ts, "#cfe3ff", 0.9, w=700, fam="Inter", align="l", maxw=600)
        T(c, "NOW → FAR FUTURE", (gx0 + gx1) / 2, gy1 + 50, 30, ts, "#cfe3ff", 0.9, w=700, fam="Inter", maxw=800)
        pr = eout(prog(t, B(2, 0.05), 2.5))
        for (slope, colr, lab, ly) in ((0.85, SILVER, "WITH THE MOON", None), (0.08, TIDE, "SUN ONLY", None)):
            x1 = lerp(gx0, gx1, pr); y0 = gy1 - 120
            line(c, gx0, y0, x1, y0 - (x1 - gx0) * slope * 0.42, colr, 7)
            if pr > 0.6: C(c, lab, x1 - 120, y0 - (x1 - gx0) * slope * 0.42 - 60, vis(t, B(2, 0.05) + 1.6), ts, size=30, dot=colr)
        C(c, "DAYS STAY NEAR 24 HOURS", 1200, 950, vis(t, B(2, 0.6)), ts, size=34, bg=YEL, fg="#0b1030", a=1)
    run_panels(c, W, H, t, S, [(0, lambda c, ts: pBrake(c, ts, 0)), (B(1, 0), lambda c, ts: pShell(c, ts, B(1, 0))), (B(2, 0), pG)])

# ------------------------------------------------------------------ m5_drift
def m5_drift(c, W, H, t, S):
    mode = S.opts.get("mode")
    def pLeave(c, ts, t0, t1):
        ex, ey = 380, 560
        earth(c, ex, ey, 200, rot=t * 8)
        q = prog(t, t0, max(0.5, t1 - t0))
        mx = 1300 + 260 * ease(q)
        moon_d(c, mx, ey, 62)
        for k in range(4):
            line(c, mx - 90 - k * 40, ey, mx - 110 - k * 40, ey, SILVER, 4, 0.5 * (1 - k / 4) * (0.5 + 0.5 * math.sin(t * 6 - k)))
        line(c, ex + 230, ey + 160, mx, ey + 160, "#ffffff", 3, 0.6, dash=([14, 12], 0))
        arrow(c, mx - 10, ey + 160, mx + 60, ey + 160, "#ffffff", 5, 0.8)
        stamp(c, "ALREADY LEAVING", 1100, 280, prog(t, t0 + 0.4, 0.4), 1.0, color=YEL, size=90, rot=-6)
    def pLaser(c, ts, t0, short=False):
        ex, ey = 330, 700
        still_earth(c, ex, ey, 260, 60)
        ox, oy = ex + 260 * math.cos(-0.9), ey + 260 * math.sin(-0.9)
        c.drawPath(poly([(ox - 30, oy + 12), (ox + 30, oy - 20), (ox + 34, oy + 10), (ox - 26, oy + 40)]), paint("#e8eef8"))
        circle(c, ox + 4, oy - 4, 26, "#e8eef8")
        mx, my = 1560, 330
        moon_d(c, mx, my, 150)
        rx, ry = mx - 60, my + 40
        tl = t0 + 0.6
        if t > tl:
            q = (t - tl) % 3.4
            if q < 2.56:
                f = q / 1.28
                if f <= 1: px, py = lerp(ox, rx, f), lerp(oy, ry, f)
                else: px, py = lerp(rx, ox, f - 1), lerp(ry, oy, f - 1)
                line(c, ox, oy, rx, ry, GREEN, 2, 0.35)
                circle(c, px, py, 12, GREEN); circle(c, px, py, 32, GREEN, 0.4, blur=12)
            T(c, f"{min(q, 2.56):.2f} S", 960, 900 if not short else 820, 90, ts, GREEN, vis(t, tl), maxw=700)
        # reflector inset
        ix, iy = 1560, 690
        pi_ = vis(t, t0 + 0.2)
        rrect(c, ix - 190, iy - 110, 380, 220, 20, "#0b1030", 0.9 * pi_); rrect(c, ix - 190, iy - 110, 380, 220, 20, MBLUE, 0.6 * pi_, stroke=3)
        for gx in range(8):
            for gy in range(4):
                circle(c, ix - 140 + gx * 40, iy - 60 + gy * 40, 16, "#9fb6d8", pi_); circle(c, ix - 140 + gx * 40, iy - 60 + gy * 40, 16, "#ffffff", 0.5 * pi_, stroke=2)
        T(c, "APOLLO MIRRORS", ix, iy + 150, 32, ts, "#cfe3ff", pi_, w=700, fam="Inter", maxw=500)
        C(c, "LASER RANGING", 760, 170, vis(t, t0 + 0.1), ts, size=36, dot=GREEN)
    def pNail(c, ts, t0, t1, long_=False):
        x0, y0, ppc = 300, 640, 300
        rect(c, x0 - 20, y0, 5 * ppc + 40, 120, "#e8d6a0")
        for k in range(51):
            L = 50 if k % 10 == 0 else (32 if k % 5 == 0 else 18)
            line(c, x0 + k * ppc / 10, y0, x0 + k * ppc / 10, y0 + L, "#3a2a10", 3)
            if k % 10 == 0: T(c, f"{k // 10}", x0 + k * ppc / 10, y0 + 85, 30, ts, "#3a2a10", 1, w=800, maxw=100)
        g = eout(prog(t, t0 + 0.3, max(1.0, (t1 - t0) * (0.5 if long_ else 0.6))))
        rrect(c, x0, y0 - 80, 3.8 * ppc * g, 50, 25, TIDE)
        T(c, f"{3.8 * g:.1f} CM", x0 + 3.8 * ppc * g + 30, y0 - 55, 54, ts, TIDE, vis(t, t0 + 0.3), align="l", maxw=500)
        C(c, "PER YEAR", 520, 200, vis(t, t0 + 0.1), ts, size=36, dot=TIDE)
        # fingertip
        fx, fy = 1500, 330
        rrect(c, fx - 420, fy - 75, 520, 150, 75, "#e0b090")
        line(c, fx - 260, fy - 40, fx - 260, fy + 40, "#b88a6a", 4)
        rrect(c, fx - 70, fy - 58, 150 + 40 * g, 116, 50, "#f6dccb"); rrect(c, fx - 70, fy - 58, 150 + 40 * g, 116, 50, "#c08a70", 1, stroke=3)
        line(c, fx + 50, fy - 50, fx + 50, fy + 50, "#ffffff", 4, 0.8)
        C(c, "≈ HOW FAST NAILS GROW", 1450, 200 if not S.P else 150, vis(t, t0 + 1.2), ts, size=32)
        if long_:
            pt = vis(t, t1 - (t1 - t0) * 0.45)
            if pt > 0:
                C(c, "SAME TIDAL BRAKE", 1450, 930, pt, ts, size=34, bg="#2a1030", dot=RED)
    def pEcl(c, ts, t0, t1):
        q = ease(prog(t, t0 + 0.3, max(0.8, (t1 - t0) * 0.7)))
        R = 210
        mr = R * (lerp(1.04, 1.0, q / 0.75) if q < 0.75 else lerp(1.0, 0.88, (q - 0.75) / 0.25))
        g = clamp((1.0 - mr / R) / 0.03)
        corona(c, 960, 500, R, t, a=1 - g)
        sun_d(c, 960, 500, R, t, a=g)
        circle(c, 960, 500, mr, "#05060c")
        yrs = int(round(min(600, 800 * q) / 10) * 10)
        T(c, f"+{yrs} MILLION YEARS", 960, 860, 70, ts, "#ffffff", vis(t, t0 + 0.2), maxw=1300)
        C(c, "TOTAL SOLAR ECLIPSE" if q < 0.75 else "THEN: ONLY A RING OF FIRE", 960, 120, vis(t, t0 + 0.1), ts, size=38, dot=SUNY)
    if mode == "intro":
        run_panels(c, W, H, t, S, [(0, lambda c, ts: pLeave(c, ts, 0, S.dur))]); return
    if mode == "laser":
        run_panels(c, W, H, t, S, [(0, lambda c, ts: pLaser(c, ts, 0, short=True))]); return
    if mode == "nail":
        run_panels(c, W, H, t, S, [(0, lambda c, ts: pNail(c, ts, 0, S.dur))]); return
    if mode == "eclipse":
        run_panels(c, W, H, t, S, [(0, lambda c, ts: pEcl(c, ts, 0, S.dur))]); return
    B = beats(S, 4)
    run_panels(c, W, H, t, S, [(0, lambda c, ts: pLeave(c, ts, 0, B(1, 0))), (B(1, 0), lambda c, ts: pLaser(c, ts, B(1, 0))),
                                (B(2, 0), lambda c, ts: pNail(c, ts, B(2, 0), B(3, 0), long_=True)), (B(3, 0), lambda c, ts: pEcl(c, ts, B(3, 0), S.dur))])

# ------------------------------------------------------------------ m5_origin
def molten(c, x, y, R, t, a=1.0):
    circle(c, x, y, R * 1.15, "#ff7a2a", 0.3 * a, blur=R * 0.12)
    circle(c, x, y, R, "#5a1a10", a)
    rng = random.Random(8)
    c.save(); pth = skia.Path(); pth.addCircle(x, y, R); c.clipPath(pth, doAntiAlias=True)
    for k in range(26):
        an = rng.random() * 6.28; d = rng.random() * R
        xx, yy = x + math.cos(an) * d, y + math.sin(an) * d
        L = R * rng.uniform(0.15, 0.4); a2 = rng.random() * 6.28
        line(c, xx, yy, xx + math.cos(a2) * L, yy + math.sin(a2) * L, "#ffb347", a * (0.6 + 0.3 * math.sin(t * 3 + k)), R * 0.025)
    c.drawCircle(x, y, R, paint(shader=rad(x - R * 0.4, y - R * 0.4, R * 1.8, [(0, "#ffffff", 0.12), (0.6, "#000000", 0), (1, "#000000", 0.6)]), a=a))
    c.restore()

def m5_origin(c, W, H, t, S):
    B = beats(S, 2)
    def pRed(c, ts):
        q = ease(prog(t, B(0, 0.1), max(1.0, B(1, 0) - B(0, 0.1))))
        r = lerp(70, 900, q)
        x = -200 + 260 * (1 - q) + 0 * q
        circle(c, x + 200, 540, r * 1.25, mix("#ffb347", "#ff4a2a", q), 0.3, blur=r * 0.2)
        circle(c, x + 200, 540, r, mix("#ffd166", "#e8452a", q))
        earth(c, 1560, 540, 56, rot=t * 20, light=(-0.9, 0.0, 0.4))
        th = t * 1.2; moon_d(c, 1560 + math.cos(th) * 150, 540 + math.sin(th) * 50, 16, glow=0.5)
        C(c, "~5 BILLION YEARS FROM NOW", 1300, 170, vis(t, B(0, 0.1)), ts, size=36, dot=SUNY)
        C(c, "RED GIANT SUN", 1300, 280, vis(t, B(0, 0.35)), ts, size=36, bg="#3a1010", dot=RED)
        C(c, "THE MOON NEVER ESCAPES", 1300, 920, vis(t, B(0, 0.7)), ts, size=34)
    def pTheia(c, ts):
        t0 = B(1, 0); th = B(1, 0.28); tm = B(1, 0.72)
        ex, ey, R = 860, 580, 210
        if t < th:
            q = prog(t, t0, th - t0)
            tx, ty = lerp(-150, ex - R * 0.9, ease(q)), lerp(330, ey - R * 0.6, ease(q))
            mars_like = "#9a7a6a"
            circle(c, tx, ty, 110, mars_like); circle(c, tx, ty, 110, "#000000", 0.35, stroke=6)
            T(c, "THEIA", tx, ty + 160, 40, ts, "#ffffff", vis(t, t0 + 0.2), maxw=400)
        molten(c, ex, ey, R, t)
        if t >= th:
            q = t - th
            fl = clamp(1 - q / 1.0)
            circle(c, ex - R * 0.7, ey - R * 0.5, 80 + q * 600, "#fff3c0", fl * 0.8, blur=40)
            rng = random.Random(3)
            mq = ease(prog(t, tm, 1.2))
            for i in range(160):
                an = rng.random() * 6.28 + q * rng.uniform(0.3, 0.8)
                rr = R * rng.uniform(1.4, 2.6) * (1 - 0.0 * mq)
                px, py = ex + math.cos(an) * rr, ey + math.sin(an) * rr * 0.32
                tx, ty = 1560, 300
                px, py = lerp(px, tx, mq), lerp(py, ty, mq)
                circle(c, px, py, rng.uniform(3, 8), rng.choice(["#ffb347", "#ff7a2a", "#c9a07a"]), clamp(q * 2) * (1 - mq * 0.8))
            if mq > 0: moon_d(c, 1560, 300, 70 * mq, mq, glow=0.5)
        C(c, "~4.5 BILLION YEARS AGO", 1350, 120 if not S.P else 150, vis(t, t0 + 0.05), ts, size=36, dot=SUNY)
        C(c, "A MARS-SIZED WORLD", 1350, 230 if not S.P else 280, vis(t, t0 + 0.6), ts, size=34)
        C(c, "A MOON IN HOURS?", 1400, 900, vis(t, tm + 0.4), ts, size=36, bg=YEL, fg="#0b1030", a=1)
    run_panels(c, W, H, t, S, [(0, pRed), (B(1, 0), pTheia)])

# ------------------------------------------------------------------ m5_pluto
_PL = {}
def pluto_img(R):
    R = max(4, int(R))
    if R not in _PL:
        n = 2 * R + 4; surf = skia.Surface(n, n); cc = surf.getCanvas(); cc.clear(skia.ColorTRANSPARENT)
        cx = cy = n / 2
        cc.save(); pth = skia.Path(); pth.addCircle(cx, cy, R); cc.clipPath(pth, doAntiAlias=True)
        cc.drawCircle(cx, cy, R, paint("#d8c2a2"))
        for dx, dy, r in ((-0.6, 0.25, 0.45), (-0.2, 0.55, 0.35), (-0.85, -0.1, 0.3), (0.75, 0.5, 0.3)):
            cc.drawCircle(cx + dx * R, cy + dy * R, r * R, paint("#7a4a36", 0.85, blur=R * 0.06))
        hp = skia.Path(); hx, hy, s = cx + 0.25 * R, cy + 0.05 * R, R * 0.48
        hp.moveTo(hx, hy + s * 0.9)
        hp.cubicTo(hx - s * 1.3, hy + s * 0.1, hx - s * 0.9, hy - s * 0.9, hx - s * 0.1, hy - s * 0.45)
        hp.cubicTo(hx + s * 0.6, hy - s * 1.0, hx + s * 1.3, hy - s * 0.3, hx, hy + s * 0.9)
        cc.drawPath(hp, paint("#f6f1e8", 1, blur=R * 0.02))
        cc.drawCircle(cx, cy, R, paint(shader=rad(cx - R * 0.3, cy - R * 0.3, R * 1.5, [(0, "#ffffff", 0.12), (0.7, "#000000", 0), (1, "#140c08", 0.55)])))
        cc.restore()
        _PL[R] = surf.makeImageSnapshot()
    return _PL[R]

def pluto_d(c, x, y, R, a=1.0, glow=1.0):
    if a <= 0: return
    if glow > 0: circle(c, x, y, R * 1.6, "#ffe8c8", 0.18 * glow * a, blur=R * 0.4)
    pt = skia.Paint(); pt.setAlphaf(clamp(a))
    c.drawImageRect(pluto_img(R), skia.Rect.MakeXYWH(x - R - 2, y - R - 2, 2 * R + 4, 2 * R + 4), skia.SamplingOptions(skia.FilterMode.kLinear), pt)

def charon_d(c, x, y, R, a=1.0):
    circle(c, x, y, R, "#9a9aa2", a)
    oval(c, x, y - R * 0.7, R * 0.5, R * 0.25, "#6a3a2a", a * 0.8)
    c.drawCircle(x, y, R, paint(shader=rad(x - R * 0.3, y - R * 0.3, R * 1.5, [(0, "#ffffff", 0.12), (1, "#000000", 0.5)]), a=a))

def night_land(c, t):
    stage_bg(c, "#0b1240", "#28356e")
    stars(c, VW, VH, t, 0.7, seed=91)
    hills(c, VW, 900, 60, "#121a3a", 21, H=VH)
    for x in (180, 330, 1650, 1780): conifer(c, x, 960, 200, "#0a0f24")

def m5_pluto(c, W, H, t, S):
    mode = S.opts.get("mode", "intro")
    def pIntro(c, ts):
        night_land(c, t)
        tv = S.lt(0, 0.45)
        g = ease(prog(t, tv, 0.6))
        moon_d(c, 1150, 380, 150, 1 - g)
        pluto_d(c, 1150, 380, 103, g)
    def pSize(c, ts):
        moon_d(c, 600, 520, 230, glow=0.5)
        pluto_d(c, 1360, 520, 157, glow=0.5)
        T(c, "MOON", 600, 830, 44, ts, SILVER, 1, maxw=500)
        T(c, "3,475 KM", 600, 900, 40, ts, "#cfe3ff", 1, w=700, fam="Inter", maxw=500)
        T(c, "PLUTO", 1360, 830, 44, ts, "#ffd9b0", vis(t, 0.3), maxw=500)
        T(c, "2,377 KM", 1360, 900, 40, ts, "#cfe3ff", vis(t, 0.3), w=700, fam="Inter", maxw=500)
        line(c, 600, 290, 1360, 363, "#ffffff", 2, 0.3, dash=([10, 8], 0)); line(c, 600, 750, 1360, 677, "#ffffff", 2, 0.3, dash=([10, 8], 0))
    def pBright(c, ts):
        bar_h(c, 300, 420, 850, 70, 0.11 * eout(prog(t, 0.3, 0.6)) / 0.72, SILVER, "MOON REFLECTS", "~11%", ts)
        bar_h(c, 300, 680, 850, 70, eout(prog(t, 0.8, 0.8)), "#ffd9b0", "PLUTO REFLECTS", "~72%", ts)
        pluto_d(c, 1720, 560, 110, glow=1.4 + 0.3 * math.sin(t * 2))
        C(c, "BRIGHT NITROGEN AND METHANE ICE", 860, 170, vis(t, 0.2), ts, size=32, dot="#ffd9b0")
    def pTides(c, ts):
        polar_tides(c, t, 430, 560, 220, 0.06, 0, moon=False)
        x0 = 820; bw = 850 if not S.P else 640
        bar_h(c, x0, 380, bw, 60, 1.0 * eout(prog(t, 0.2, 0.5)), MBLUE, "OUR MOON", "100%", ts)
        bar_h(c, x0, 590, bw, 60, 0.46 * eout(prog(t, 0.5, 0.5)), SUNY, "THE SUN", "46%", ts)
        bar_h(c, x0, 800, bw, 60, 0.18 * eout(prog(t, 0.9, 0.5)), "#ffd9b0", "PLUTO", "~18%", ts)
        C(c, "TIDE-RAISING PULL", 1280, 200, vis(t, 0.1), ts, size=34, dot=TIDE)
    def pMelt(c, ts):
        sun_d(c, 160, 540, 110, t)
        px, py = 1250, 540
        g = ease(prog(t, S.lt(S.n() - 1, 0.2), 2.0))
        for k in range(60):
            q = ((t * 0.25 + k / 60) % 1)
            x = px + 60 + q * 650 * (0.3 + 0.7 * g); y = py + math.sin(k * 1.7) * (30 + q * 160) * g
            circle(c, x, y, 10 + q * 30, "#cfe8ff", g * 0.25 * (1 - q), blur=10)
        pluto_d(c, px, py, 130)
        C(c, "PLUTO'S SUNLIGHT ~1/1,500 OF OURS", 760, 170, vis(t, 0.2), ts, size=32, dot=SUNY)
        C(c, "NITROGEN ICE → GAS", 1350, 880, vis(t, S.lt(S.n() - 1, 0.55)), ts, size=36, dot=TIDE)
    def pCharon(c, ts):
        night_land(c, t)
        bx, by = 960, 450
        th = t * 1.0
        pr, cr = 150, 78
        dp, dc = 95, 300
        pluto_d(c, bx - math.cos(th) * dp, by - math.sin(th) * dp * 0.35, pr)
        charon_d(c, bx + math.cos(th) * dc, by + math.sin(th) * dc * 0.35, cr)
        line(c, bx - 14, by, bx + 14, by, YEL, 4); line(c, bx, by - 14, bx, by + 14, YEL, 4)
        C(c, "CHARON: HALF PLUTO'S SIZE", 960, 110, vis(t, 0.2), ts, size=32, dot="#c0c0c8")
        C(c, "ONE LAP EVERY 6.4 DAYS", 960, 960, vis(t, S.lt(0, 0.4), S.lt(0, 0.72)), ts, size=32, dot=YEL)
        C(c, "STAYING TOGETHER HERE? DOUBTFUL", 960, 960, vis(t, S.lt(0, 0.75)), ts, size=32, bg="#2a1030", dot=RED)
    fn = {"intro": pIntro, "size": pSize, "bright": pBright, "tides": pTides, "melt": pMelt, "charon": pCharon}[mode]
    run_panels(c, W, H, t, S, [(0, fn)])

SCENES = {k: v for k, v in globals().items() if k.startswith("m5_") and callable(v)}
