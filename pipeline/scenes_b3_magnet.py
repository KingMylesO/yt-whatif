"""Batch 03 scenes: What If Earth's Magnetic Field Switched Off? (+ magnet, pole-flip and no-clouds Shorts).

Look: deep teal-black space, cyan field lines, orange solar-wind streaks, aurora greens/magentas.
Every scene draws its art on a virtual 1920x1080 stage (Stage). In Shorts the stage is scaled into the
0.255H..0.58H content band and text sizes are multiplied by S_ts so chips stay readable on a phone.
"""
from common2 import *
import geo
import scenes_b3_kit as kit

TEAL_T, TEAL_B = "#03141c", "#0b2e3a"
CYAN = "#5ef2d6"
WIND = "#ffa24a"
AUR_G, AUR_M = "#46ff9a", "#ff4fd8"
CHIPBG = "#0a2a33"
PAL = dict(accent=CYAN, chip="#0d3a44", title2=ACCENT)
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

def vrect(c, y0, y1, top, bot, a=1.0, x0=-600, x1=2520):
    """Gradient band in virtual coords; extends edges far so Shorts are filled."""
    yy0 = y0 if y0 > -1 else -4000; yy1 = y1 if y1 < VH + 1 else 6000
    c.drawRect(skia.Rect.MakeLTRB(x0, yy0, x1, yy1), paint(shader=lin(0, max(y0, 0), 0, min(y1, VH), [(0, top, a), (1, bot, a)])))

def bg_space(c, W, H, t, S, seed=21, a=1.0):
    fill_bg(c, W, H, TEAL_T, TEAL_B)
    stars(c, W, H, t, 0.8 * a, seed=seed, drift=(-5, 0))

def C(c, s, x, y, p, ts, size=34, **kw):
    kw.setdefault("bg", CHIPBG)
    chip(c, s, x, y, p, size * ts, **kw)

def T(c, s, x, y, size, ts, colr="#ffffff", a=1.0, w=900, maxw=1800, **kw):
    sz = fit(s, maxw, size * ts, w)
    text(c, s, x, y, sz, colr, a, w=w, shadow=kw.pop("shadow", 10), **kw)

def B_(S, n): return beats(S, n)

# ------------------------------------------------------------------ props
def dipole(c, cx, cy, R, Ls, a=1.0, colr=CYAN, comp=1.0, stretch=1.0, tilt=0.0, width=3.0, grow=1.0, flow=None, wob=0.0, t=0.0):
    if a <= 0.01: return
    ct, st = math.cos(math.radians(tilt)), math.sin(math.radians(tilt))
    for j, L in enumerate(Ls):
        th0 = math.asin(min(1, math.sqrt(1 / L)))
        for side in (-1, 1):
            p = skia.Path(); n = 48; m = max(2, int(n * clamp(grow)))
            for i in range(m + 1):
                th = th0 + (math.pi - 2 * th0) * i / n
                r = L * R * math.sin(th) ** 2
                x = side * r * math.sin(th); y = -r * math.cos(th)
                if wob: x += math.sin(th * 5 + t * 2 + j) * wob * R; y += math.cos(th * 4 + t * 1.7 + j) * wob * R
                x *= comp if x < 0 else stretch
                X = cx + x * ct - y * st; Y = cy + x * st + y * ct
                if i == 0: p.moveTo(X, Y)
                else: p.lineTo(X, Y)
            al = a * (0.85 - 0.1 * j / max(1, len(Ls)))
            c.drawPath(p, paint(colr, al * 0.25, stroke=width * 3.5))
            c.drawPath(p, paint(colr, al, stroke=width, dash=([18, 14], -t * 40) if flow else None))

def wind(c, t, a, x0, x1, y0, y1, n=46, seed=3, bow=None, hit=None, speed=0.45, size=1.0):
    """Orange streaks flowing right. bow=(nose_x, cy, k): deflect around x >= nose + (y-cy)^2/k.
    hit=(cx, cy, R): particles stop at the circle and sparkle."""
    if a <= 0.01: return
    rng = random.Random(seed)
    for k in range(n):
        yb = rng.uniform(y0, y1); ph = rng.random(); sp = speed * rng.uniform(0.8, 1.3)
        q = (t * sp + ph) % 1; x = x0 + q * (x1 - x0); y = yb
        L = 46 * size * rng.uniform(0.7, 1.3)
        fade = math.sin(q * math.pi) ** 0.5
        if hit:
            hx, hy, hr = hit; dy = yb - hy
            if abs(dy) < hr:
                xh = hx - math.sqrt(hr * hr - dy * dy)
                if x > xh:
                    age = (x - xh) / (x1 - x0) * 6
                    if age < 1: circle(c, xh, yb, (6 + 22 * age) * size, "#ffe2a8", a * (1 - age) * 0.8)
                    continue
                L = min(L, xh - x + L)
        y_prev = y
        if bow:
            nx, cy, kk = bow
            for xx, sgn in ((x, 1), (x - L, 0)):
                if xx > nx:
                    d = math.sqrt((xx - nx) * kk)
                    if abs(yb - cy) < d:
                        yy = cy + (d if yb >= cy else -d)
                    else: yy = yb
                else: yy = yb
                if sgn: y = yy
                else: y_prev = yy
        c.drawLine(x - L, y_prev, x, y, paint(WIND, a * fade * 0.85, stroke=3.2 * size))
        circle(c, x, y, 3.4 * size, "#ffe2a8", a * fade)

def earth(c, x, y, R, t, a=1.0, rot0=-20, spin=3.0, tilt=18, night=0.0, glow=1.0, **kw):
    geo.globe(c, x, y, R, rot=rot0 + t * spin, tilt=tilt, a=a, night=night, glow=glow, **kw)

_GLOBES = {}
def still_earth(c, x, y, R, rot=-20, tilt=18):
    """Globe + glow cached as one image (for big, non-spinning globes)."""
    R = max(4, int(R) // 4 * 4); k = (R, rot, tilt)
    if k not in _GLOBES:
        pad = int(R * 0.3); n = 2 * (R + pad)
        surf = skia.Surface(n, n); cc = surf.getCanvas(); cc.clear(skia.ColorTRANSPARENT)
        geo.globe(cc, n / 2, n / 2, R, rot=rot, tilt=tilt)
        _GLOBES[k] = (surf.makeImageSnapshot(), pad)
    img, pad = _GLOBES[k]
    c.drawImage(img, x - R - pad, y - R - pad, skia.SamplingOptions(skia.FilterMode.kLinear))

def mars(c, x, y, R, a=1.0, crust=0.0):
    if a <= 0: return
    circle(c, x, y, R * 1.06, "#ff9a6a", 0.18 * a, blur=R * 0.06)
    c.save(); pth = skia.Path(); pth.addCircle(x, y, R); c.clipPath(pth, doAntiAlias=True)
    circle(c, x, y, R, "#c8552e", a)
    rng = random.Random(5)
    for _ in range(12):
        oval(c, x + rng.uniform(-0.8, 0.8) * R, y + rng.uniform(-0.6, 0.7) * R, R * rng.uniform(0.12, 0.35), R * rng.uniform(0.06, 0.16), "#8e3a1f", a * 0.7)
    oval(c, x, y - R * 0.93, R * 0.42, R * 0.14, "#f4ece6", a)
    if crust > 0:  # striped crustal magnetism in the south
        for k in range(7):
            yy = y + R * (0.25 + k * 0.09)
            line(c, x - R * 0.7, yy + R * 0.08, x + R * 0.2, yy - R * 0.05, CYAN if k % 2 else "#ff6b8a", R * 0.035, a * crust * 0.85)
    c.drawCircle(x, y, R, paint(shader=rad(x - R * 0.4, y - R * 0.35, R * 2.0, [(0, "#ffffff", 0.2), (0.5, "#000000", 0.0), (1, "#000000", 0.6)]), a=a))
    c.restore()

def venus(c, x, y, R, t, a=1.0):
    if a <= 0: return
    circle(c, x, y, R * 1.12, "#ffe7a8", 0.25 * a, blur=R * 0.1)
    c.save(); pth = skia.Path(); pth.addCircle(x, y, R); c.clipPath(pth, doAntiAlias=True)
    circle(c, x, y, R, "#e8c98a", a)
    for k in range(9):
        yy = y - R + k * R * 0.25 + math.sin(t * 0.5 + k) * 6
        p = skia.Path(); p.moveTo(x - R * 1.2, yy)
        p.cubicTo(x - R * 0.4, yy - R * 0.2, x + R * 0.3, yy + R * 0.25, x + R * 1.2, yy - R * 0.05)
        c.drawPath(p, paint("#fff3d0" if k % 2 else "#d9b47a", a * 0.22, stroke=R * 0.12, blur=R * 0.03))
    c.drawCircle(x, y, R, paint(shader=rad(x - R * 0.4, y - R * 0.35, R * 2.0, [(0, "#ffffff", 0.2), (0.5, "#000000", 0.0), (1, "#000000", 0.55)]), a=a))
    c.restore()

def compass(c, x, y, r, ang, a=1.0, lab=True):
    if a <= 0: return
    circle(c, x, y, r * 1.08, "#000000", 0.35 * a, blur=r * 0.12)
    circle(c, x, y, r, "#d9c38f", a); circle(c, x, y, r * 0.88, "#f6f1e3", a)
    for k in range(36):
        an = k * math.pi / 18; L = 0.1 if k % 9 == 0 else 0.05
        line(c, x + math.sin(an) * r * 0.86, y - math.cos(an) * r * 0.86, x + math.sin(an) * r * (0.86 - L), y - math.cos(an) * r * (0.86 - L), "#3a3a4a", r * 0.012, a)
    if lab:
        for s_, an in (("N", 0), ("E", 90), ("S", 180), ("W", 270)):
            text(c, s_, x + math.sin(math.radians(an)) * r * 0.66, y - math.cos(math.radians(an)) * r * 0.66, r * 0.17, "#c0392b" if s_ == "N" else "#1b2233", a, w=900)
    c.save(); c.translate(x, y); c.rotate(ang)
    c.drawPath(poly([(0, -r * 0.72), (r * 0.09, 0), (-r * 0.09, 0)]), paint("#e23b2e", a))
    c.drawPath(poly([(0, r * 0.72), (r * 0.09, 0), (-r * 0.09, 0)]), paint("#e9edf5", a))
    c.drawPath(poly([(0, r * 0.72), (r * 0.09, 0), (-r * 0.09, 0)]), paint("#8a93a8", a, stroke=r * 0.012))
    c.restore()
    circle(c, x, y, r * 0.05, "#2a2a35", a)

def needle_angle(t, ts, final, base=0.0):
    if t < ts: return base + 2 * math.sin(t * 3)
    q = t - ts
    return final + (base - final - 720) * math.exp(-q * 1.5) + 6 * math.sin(q * 2.3) * math.exp(-q * 0.5)

def satellite(c, x, y, s, a=1.0, ang=0, hitp=0.0):
    if a <= 0: return
    c.save(); c.translate(x, y); c.rotate(ang)
    rect(c, -s * 0.25, -s * 0.2, s * 0.5, s * 0.4, "#d9dee8", a)
    for sd in (-1, 1):
        rect(c, sd * s * 0.3 - (s * 0.75 if sd < 0 else 0), -s * 0.16, s * 0.75, s * 0.32, "#2f5fd0", a)
        for k in range(4): line(c, sd * s * 0.3 + (-1 if sd < 0 else 0) * s * 0.75 + k * s * 0.19 + s * 0.09, -s * 0.16, sd * s * 0.3 + (-1 if sd < 0 else 0) * s * 0.75 + k * s * 0.19 + s * 0.09, s * 0.16, "#9fc0ff", s * 0.02, a)
    line(c, 0, -s * 0.2, 0, -s * 0.38, "#d9dee8", s * 0.04, a); circle(c, 0, -s * 0.4, s * 0.06, "#ffffff", a)
    c.restore()
    if hitp > 0:
        circle(c, x, y, s * (0.6 + hitp), "#ff5a3c", a * (1 - hitp) * 0.8, stroke=s * 0.08)
        circle(c, x, y, s * 0.6, "#ff9a4a", a * (1 - hitp) * 0.4, blur=s * 0.3)

def station(c, x, y, s, a=1.0):
    rect(c, x - s * 0.06, y - s * 0.5, s * 0.12, s, "#cfd6e2", a)
    for sd in (-1, 1):
        for k in (-0.35, 0.15):
            rect(c, x + sd * s * 0.12 + (-s * 0.62 if sd < 0 else 0), y + k * s, s * 0.62, s * 0.2, "#c9a24a", a)
    rect(c, x - s * 0.22, y - s * 0.12, s * 0.44, s * 0.24, "#e8ecf3", a)

def plane(c, x, y, s, a=1.0, colr="#e8eef8"):
    rrect(c, x - s, y - s * 0.09, s * 2, s * 0.18, s * 0.09, colr, a)
    c.drawPath(poly([(x - s * 0.15, y), (x + s * 0.25, y), (x - s * 0.35, y + s * 0.75), (x - s * 0.55, y + s * 0.75)]), paint(colr, a))
    c.drawPath(poly([(x - s * 0.15, y), (x + s * 0.25, y), (x - s * 0.35, y - s * 0.75), (x - s * 0.55, y - s * 0.75)]), paint(colr, a))
    c.drawPath(poly([(x - s * 0.8, y), (x - s * 0.95, y - s * 0.4), (x - s * 1.02, y - s * 0.4), (x - s * 0.95, y)]), paint(colr, a))

def switch(c, x, y, s, on, a=1.0):
    rrect(c, x - s * 0.55, y - s, s * 1.1, s * 2, s * 0.2, "#1b2a33", a)
    rrect(c, x - s * 0.55, y - s, s * 1.1, s * 2, s * 0.2, "#ffffff", 0.25 * a, stroke=s * 0.04)
    yy = lerp(s * 0.45, -s * 0.45, on)
    rrect(c, x - s * 0.32, y + yy - s * 0.35, s * 0.64, s * 0.7, s * 0.12, mix("#ff4d4d", "#4cd964", on), a)
    text(c, "ON", x, y - s * 1.25, s * 0.28, "#4cd964", a * (0.4 + 0.6 * on), w=900)
    text(c, "OFF", x, y + s * 1.25, s * 0.28, "#ff4d4d", a * (1 - 0.6 * on), w=900)

def thermo(c, x, y, h, temp, a=1.0, size=1.0):
    thermometer(c, x, y, h, temp, tmax=45, tmin=-5, a=a, size=size)

def turtle(c, x, y, s, t, a=1.0):
    fl = math.sin(t * 4) * 0.3
    for sd in (-1, 1):
        c.save(); c.translate(x + s * 0.25, y + sd * s * 0.35); c.rotate(sd * (30 + fl * 40))
        oval(c, s * 0.25, 0, s * 0.35, s * 0.11, "#5f8f4a", a); c.restore()
        oval(c, x - s * 0.45, y + sd * s * 0.3, s * 0.18, s * 0.08, "#5f8f4a", a)
    oval(c, x, y, s * 0.55, s * 0.42, "#6b4f2a", a)
    for k in range(3): circle(c, x - s * 0.25 + k * s * 0.25, y, s * 0.12, "#8a6a3a", a)
    circle(c, x + s * 0.62, y, s * 0.17, "#5f8f4a", a)

def salmon(c, x, y, s, t, a=1.0, colr="#ff8a6a"):
    w_ = math.sin(t * 6) * s * 0.08
    p = skia.Path(); p.moveTo(x + s * 0.6, y); p.quadTo(x, y - s * 0.32, x - s * 0.5, y + w_); p.quadTo(x, y + s * 0.3, x + s * 0.6, y)
    c.drawPath(p, paint(colr, a))
    c.drawPath(poly([(x - s * 0.45, y + w_), (x - s * 0.8, y - s * 0.25 + w_), (x - s * 0.8, y + s * 0.25 + w_)]), paint(colr, a))
    circle(c, x + s * 0.4, y - s * 0.05, s * 0.04, "#1b2233", a)

def robin(c, x, y, s, t, a=1.0):
    f = math.sin(t * 9) * 0.5
    c.drawPath(poly([(x - s * 0.1, y), (x - s * 0.4, y - s * (0.6 + f * 0.5)), (x + s * 0.15, y - s * 0.05)]), paint("#6b5a4a", a))
    oval(c, x, y, s * 0.42, s * 0.26, "#7a6555", a); oval(c, x + s * 0.12, y + s * 0.06, s * 0.22, s * 0.16, "#e8743a", a)
    circle(c, x + s * 0.38, y - s * 0.12, s * 0.17, "#7a6555", a)
    c.drawPath(poly([(x + s * 0.52, y - s * 0.14), (x + s * 0.68, y - s * 0.1), (x + s * 0.52, y - s * 0.06)]), paint("#e0a43a", a))
    c.drawPath(poly([(x - s * 0.38, y - s * 0.05), (x - s * 0.7, y - s * 0.12), (x - s * 0.68, y + s * 0.08)]), paint("#6b5a4a", a))

def dashed_path(c, pts, colr, w, a, t=0.0, wob=0.0, seed=1, grow=1.0):
    if a <= 0: return
    rng = random.Random(seed)
    p = skia.Path(); n = len(pts); m = max(2, int((n - 1) * clamp(grow)) + 1)
    for i in range(m):
        x, y = pts[i]
        if wob and 0 < i < n - 1: x += math.sin(i * 1.7 + t * 2 + seed) * wob * rng.uniform(0.5, 1.5); y += math.cos(i * 2.3 + t * 1.6) * wob * rng.uniform(0.5, 1.5)
        if i == 0: p.moveTo(x, y)
        else: p.lineTo(x, y)
    c.drawPath(p, paint(colr, a, stroke=w, dash=([w * 3, w * 2.4], -t * 30)))

def curve_pts(x0, y0, x1, y1, bend, n=24):
    out = []
    for i in range(n):
        q = i / (n - 1); out.append((lerp(x0, x1, q), lerp(y0, y1, q) - math.sin(q * math.pi) * bend))
    return out

def aurora_curtain(c, x0, x1, ybase, h, t, a=1.0, colr=AUR_G, colr2=AUR_M, seed=1, n=26):
    if a <= 0.01: return
    rng = random.Random(seed)
    for k in range(n):
        q = k / (n - 1); x = lerp(x0, x1, q) + math.sin(t * 0.6 + k * 0.7) * 30
        hh = h * (0.6 + 0.4 * math.sin(k * 0.9 + t * 0.8 + seed)) * rng.uniform(0.7, 1.1)
        yb = ybase + math.sin(q * 3 + t * 0.4) * 30
        c.drawRect(skia.Rect.MakeLTRB(x - 26, yb - hh, x + 26, yb), paint(shader=lin(0, yb - hh, 0, yb, [(0, colr2, 0), (0.45, colr2, 0.25 * a), (0.75, colr, 0.55 * a), (1, colr, 0.0)]), blur=12))

def cityline(c, x0, x1, base, lights, a=1.0, seed=4):
    rng = random.Random(seed); x = x0
    while x < x1:
        bw = rng.uniform(50, 110); bh = rng.uniform(80, 260)
        rect(c, x, base - bh, bw, bh + 2, "#0b1620", a)
        for wy in range(int(bh / 26) - 1):
            for wx in range(int(bw / 22)):
                if rng.random() < 0.5:
                    rect(c, x + 8 + wx * 22, base - bh + 14 + wy * 26, 10, 12, "#ffd27a", a * lights)
        x += bw + rng.uniform(4, 12)

def ground_scene(c, horizon, sky_t, sky_b, gnd_t, gnd_b):
    vrect(c, -1, horizon, sky_t, sky_b)
    vrect(c, horizon, VH + 2, gnd_t, gnd_b)

def tractor(c, x, y, s, a=1.0):
    rect(c, x - s * 0.6, y - s * 0.55, s * 0.8, s * 0.35, "#3fae4a", a)
    rect(c, x - s * 0.1, y - s * 0.95, s * 0.4, s * 0.45, "#3fae4a", a)
    rect(c, x - s * 0.04, y - s * 0.88, s * 0.28, s * 0.22, "#bfe3ff", a)
    circle(c, x + s * 0.05, y - s * 0.2, s * 0.32, "#20242c", a); circle(c, x + s * 0.05, y - s * 0.2, s * 0.13, "#c9a24a", a)
    circle(c, x - s * 0.5, y - s * 0.14, s * 0.18, "#20242c", a)

def telegraph(c, x, base, s, spark, t, a=1.0):
    rect(c, x - s * 0.04, base - s * 1.6, s * 0.08, s * 1.6, "#5b3e2a", a)
    rect(c, x - s * 0.4, base - s * 1.5, s * 0.8, s * 0.06, "#5b3e2a", a)
    for k in (-0.3, 0, 0.3):
        circle(c, x + k * s, base - s * 1.53, s * 0.04, "#d0d6e0", a)
    if spark > 0:
        rng = random.Random(int(t * 12))
        for k in range(6):
            sx = x + rng.uniform(-0.4, 0.4) * s; sy = base - s * 1.5
            for j in range(3):
                an = rng.uniform(0, 6.28); L = rng.uniform(0.05, 0.2) * s
                line(c, sx, sy, sx + math.cos(an) * L, sy + math.sin(an) * L, "#fff1a0", s * 0.012, a * spark)
            circle(c, sx, sy, s * 0.05, "#fff6c8", a * spark * 0.6, blur=s * 0.03)

def telegraph_key(c, x, y, s, press, a=1.0):
    rrect(c, x - s, y - s * 0.12, s * 2, s * 0.24, s * 0.05, "#5b3e2a", a)
    c.save(); c.translate(x - s * 0.7, y - s * 0.15); c.rotate(-6 + 6 * press)
    rect(c, 0, -s * 0.06, s * 1.5, s * 0.08, "#c9a24a", a); circle(c, s * 1.5, -s * 0.06, s * 0.14, "#1b1b22", a)
    c.restore()

def solar_panel(c, x, y, s, a=1.0, glint=0.0):
    c.drawPath(poly([(x - s, y), (x + s * 0.8, y), (x + s, y - s * 0.6), (x - s * 0.8, y - s * 0.6)]), paint("#1d3f8f", a))
    for k in range(1, 4):
        q = k / 4; line(c, lerp(x - s, x - s * 0.8, 0) + q * s * 1.8, y, lerp(x - s * 0.8, x - s * 0.8, 0) + q * s * 1.8 + s * 0.2 - s * 0.0, y - s * 0.6, "#7fa8ff", s * 0.02, a)
    line(c, x - s * 0.9, y - s * 0.3, x + s * 0.9, y - s * 0.3, "#7fa8ff", s * 0.02, a)
    rect(c, x - s * 0.04, y, s * 0.08, s * 0.4, "#9aa4b8", a)
    if glint: circle(c, x + s * 0.3, y - s * 0.35, s * 0.25, "#ffffff", a * glint * 0.6, blur=s * 0.12)

def cracked_ground(c, x0, x1, y0, y1, a=1.0, seed=2):
    rect(c, x0, y0, x1 - x0, y1 - y0, "#b08a5a", a)
    rng = random.Random(seed)
    for _ in range(40):
        x = rng.uniform(x0, x1); y = rng.uniform(y0, y1); pts = [(x, y)]
        for k in range(4):
            x += rng.uniform(-40, 40); y += rng.uniform(-14, 14); pts.append((x, y))
        c.drawPath(poly(pts, close=False), paint("#6b4f2a", a, stroke=3))

def raindrops(c, x0, x1, ytop, ybot, t, a=1.0, n=40, seed=5):
    if a <= 0.01: return
    rng = random.Random(seed)
    for k in range(n):
        x = rng.uniform(x0, x1); ph = rng.random(); q = (t * 1.2 + ph) % 1
        y = lerp(ytop, ybot, q)
        line(c, x, y, x - 4, y + 26, "#9fd3ff", 4, a * 0.85)

def ammonite(c, x, y, r, a=1.0):
    p = skia.Path()
    for i in range(160):
        an = i / 160 * 3.2 * math.pi; rr = r * math.exp(-0.18 * (3.2 * math.pi - an))
        X, Y = x + math.cos(an) * rr, y + math.sin(an) * rr
        if i == 0: p.moveTo(X, Y)
        else: p.lineTo(X, Y)
    circle(c, x, y, r * 1.02, "#c9a77a", a)
    c.drawPath(p, paint("#7a5a3a", a, stroke=r * 0.07))
    for k in range(14):
        an = k / 14 * 2 * math.pi
        line(c, x + math.cos(an) * r * 0.55, y + math.sin(an) * r * 0.55, x + math.cos(an) * r * 0.95, y + math.sin(an) * r * 0.95, "#7a5a3a", r * 0.03, a * 0.8)

def tree_rings(c, x, y, r, a=1.0):
    circle(c, x, y, r, "#8a5a32", a)
    circle(c, x, y, r * 0.94, "#e2b67c", a)
    for k in range(1, 12):
        circle(c, x, y, r * 0.94 * k / 12, "#a8743f", a * 0.8, stroke=max(1.5, r * 0.012))
    line(c, x, y, x + r * 0.9, y - r * 0.2, "#6b3f1f", r * 0.02, a * 0.5)

def ice_core(c, x, y, w, h, a=1.0):
    rrect(c, x - w / 2, y - h / 2, w, h, w * 0.5, "#dff3ff", a)
    for k in range(18):
        yy = y - h / 2 + h * (k + 0.5) / 18
        line(c, x - w * 0.45, yy, x + w * 0.45, yy, "#9fc7e6", 3, a * 0.8)
    rrect(c, x - w / 2, y - h / 2, w, h, w * 0.5, "#ffffff", a * 0.6, stroke=3)

def graph_axes(c, x0, y0, w, h, a, ts, xl="", yl=""):
    line(c, x0, y0 + h, x0 + w, y0 + h, "#ffffff", 3, a * 0.8)
    line(c, x0, y0, x0, y0 + h, "#ffffff", 3, a * 0.8)
    if xl: T(c, xl, x0 + w / 2, y0 + h + 44 * ts, 26, ts, "#bfe9e1", a, w=700, fam="Inter")
    if yl: T(c, yl, x0 + 10, y0 - 30 * ts, 26, ts, "#bfe9e1", a, w=700, fam="Inter", align="l")

def magnet_bar(c, x, y, s, a=1.0):
    rrect(c, x - s, y - s * 0.4, s * 2, s * 0.8, s * 0.12, "#e23b2e", a)
    rrect(c, x, y - s * 0.4, s, s * 0.8, s * 0.12, "#2f5fd0", a)
    rect(c, x, y - s * 0.4, s * 0.15, s * 0.8, "#2f5fd0", a)
    text(c, "N", x - s * 0.5, y, s * 0.42, "#ffffff", a, w=900); text(c, "S", x + s * 0.5, y, s * 0.42, "#ffffff", a, w=900)

def sun_left(c, t, a=1.0, y=540, x=-120, r=300):
    sun(c, x, y, r, t, a=a, glow=0.9)

# ------------------------------------------------------------------ motif / kit scenes
def bg_mag(c, W, H, t, S): bg_space(c, W, H, t, S, seed=22)

def motif_mag(c, W, H, t, S, cx, cy, s):
    u = S.u; R = int(120 * s * u * (1.25 if S.P else 1))
    k = max(1, R * 3.8)
    wind(c, t, 0.9, cx - W * 0.6, cx + W * 0.6, cy - R * 2.2, cy + R * 2.2, n=36, bow=(cx - R * 2.2, cy, R * 1.6), size=u * s * 1.2)
    dipole(c, cx, cy, R, [1.6, 2.3, 3.1, 4.0], 0.9, comp=0.62, stretch=1.35, tilt=-11, width=3.2 * u * s, flow=True, t=t)
    earth(c, cx, cy, R, t)

def m_title(c, W, H, t, S): kit.title(c, W, H, t, S, bg_mag, motif_mag, PAL)
def m_card(c, W, H, t, S):
    def bgc(c, W, H, t, S):
        bg_mag(c, W, H, t, S); motif_mag(c, W, H, t, S, W / 2, H / 2, 1.5 if not S.P else 1.2)
    kit.card(c, W, H, t, S, bgc, PAL)
def m_end(c, W, H, t, S):
    def mot(c, W, H, t, S, cx, cy, s):
        aurora_curtain(c, cx - W * 0.45, cx + W * 0.45, cy + 60 * S.u, 260 * S.u, t, 0.8)
        motif_mag(c, W, H, t, S, cx, cy + 40 * S.u, s)
    kit.end(c, W, H, t, S, bg_mag, mot, PAL)
def m_endshort(c, W, H, t, S): kit.end_short(c, W, H, t, S, bg_mag, motif_mag, PAL)

# ------------------------------------------------------------------ m_wind
def m_wind(c, W, H, t, S):
    o = S.opts; mode = o.get("mode", "shield")
    bg_space(c, W, H, t, S, seed=23)
    with Stage(c, S) as ts:
        ex, ey, R = 1180, 560, 152
        sun_left(c, t)
        if mode == "shield":
            B = B_(S, 3); long_ = S.n() >= 3
            off = prog(t, B(2, 0.55), 0.5) if long_ else 0.0
            flick = 1.0 if off == 0 else (1 - off) * (0.6 + 0.4 * math.sin(t * 40))
            bowa = 1 - off
            wind(c, t, 1, 120, 2000, 140, 960, n=70, bow=(ex - R * 2.3, ey, R * 1.9) if bowa > 0.5 else None)
            # magnetopause glow
            if flick > 0.02:
                p = skia.Path(); first = True
                for i in range(41):
                    yy = ey - 420 + i * 21; xx = ex - R * 2.3 + (yy - ey) ** 2 / (R * 1.9)
                    (p.moveTo if first else p.lineTo)(xx, yy); first = False
                c.drawPath(p, paint(CYAN, 0.35 * flick, stroke=10)); c.drawPath(p, paint(CYAN, 0.8 * flick, stroke=3))
            dipole(c, ex, ey, R, [1.5, 2.1, 2.9, 3.8], flick, comp=0.6, stretch=1.5, tilt=-11, width=3.2, flow=True, t=t)
            earth(c, ex, ey, R, t)
            C(c, "SOLAR WIND: ~400 KM/S", 560, 110, vis(t, B(0, 0.15)), ts, dot=WIND)
            C(c, "COAST TO COAST (USA) IN ~11 SECONDS", 960, 990, vis(t, B(0, 0.55), B(1, 0)) if long_ else 0, ts, size=30)
            C(c, "MAGNETIC SHIELD", ex + 40, 990 if long_ else 200, vis(t, B(1, 0.2) if long_ else B(0, 0.75)), ts, dot=CYAN, bg="#0d3a44")
            if long_:
                T(c, "?", 1650, 560, 220, ts, CYAN, prog(t, B(2, 0.3), 0.4), shadow=18)
        else:
            B = B_(S, 2)
            wind(c, t, 1, 120, 2000, 140, 960, n=80, hit=(ex, ey, R * 1.08))
            circle(c, ex, ey, R * 1.08, "#ffb06a", 0.25 + 0.1 * math.sin(t * 6), blur=14)
            earth(c, ex, ey, R, t)
            C(c, "NO SHIELD", 560, 110, vis(t, B(0, 0.05)), ts, dot="#ff4d4d")
            C(c, "SOLAR WIND HITS THE UPPER AIR", 960, 990, vis(t, B(0, 0.4), B(1, 0)), ts)
            pg = vis(t, B(1, 0.45))
            C(c, "ON THE GROUND: MOSTLY FINE", 960, 990, pg, ts, bg="#123d2a")
            check(c, 1520, 300, 50, pg)
    kit.hook(c, W, H, t, S)

# ------------------------------------------------------------------ m_core
def m_core(c, W, H, t, S):
    B = B_(S, 2); bg_space(c, W, H, t, S, seed=24)
    with Stage(c, S) as ts:
        cx, cy, R = 700, 560, 400
        grow = eout(prog(t, B(1, 0.35), 2.5))
        dipole(c, cx, cy, R, [1.35, 1.7, 2.2], grow * 0.9, width=4, grow=grow, flow=True, t=t, tilt=-11)
        z = 1 + 0.03 * t / S.dur  # slow push-in instead of spinning (globe cached)
        c.save(); c.translate(cx, cy); c.scale(z, z); c.translate(-cx, -cy)
        still_earth(c, cx, cy, R)
        # cutaway wedge (quarter, upper right)
        op = eout(prog(t, 0.2, 0.8))
        c.save(); p = skia.Path(); p.moveTo(cx, cy); p.arcTo(skia.Rect.MakeXYWH(cx - R, cy - R, 2 * R, 2 * R), -90, 90 * op, False); p.close(); c.clipPath(p, doAntiAlias=True)
        circle(c, cx, cy, R, "#5a2a1a"); circle(c, cx, cy, R * 0.97, "#b5532e")
        c.drawCircle(cx, cy, R * 0.97, paint(shader=rad(cx, cy, R * 0.97, [(0, "#ff7a3a", 1), (1, "#7a2a1a", 1)])))
        rc = R * 0.55
        c.drawCircle(cx, cy, rc, paint(shader=rad(cx, cy, rc, [(0, "#fff0a0", 1), (0.6, "#ffb03a", 1), (1, "#ff7a1a", 1)])))
        for k in range(8):  # swirl
            r_ = rc * (0.4 + 0.07 * k); a0 = (t * (40 + k * 6) + k * 47) % 360
            pp = skia.Path(); pp.addArc(skia.Rect.MakeXYWH(cx - r_, cy - r_, 2 * r_, 2 * r_), a0, 50)
            c.drawPath(pp, paint("#fff4c8", 0.55, stroke=5))
        circle(c, cx, cy, R * 0.19, "#fffbe6")
        c.restore()
        pl = vis(t, B(0, 0.1))
        # depth bracket
        line(c, cx + 18, cy - R, cx + 18, cy - rc, ACCENT, 5, pl)
        line(c, cx + 8, cy - R, cx + 28, cy - R, ACCENT, 5, pl); line(c, cx + 8, cy - rc, cx + 28, cy - rc, ACCENT, 5, pl)
        c.restore()  # end push-in
        C(c, "~2,900 KM DOWN", 1440, 260, pl, ts, dot=ACCENT)
        C(c, "LIQUID IRON + NICKEL", 1440, 380, vis(t, B(0, 0.45)), ts, dot="#ffb03a")
        C(c, "THOUSANDS OF °C", 1440, 500, vis(t, B(0, 0.7)), ts, dot="#ff7a3a")
        pd = vis(t, B(1, 0.05))
        C(c, "CHURNING = DYNAMO", 1440, 680, pd, ts, dot=CYAN)
        for k in range(3):
            q = (t * 0.6 + k / 3) % 1; an = math.radians(-80 + q * 70)
            if pd > 0: arrow(c, cx + math.cos(an) * rc * 0.8, cy + math.sin(an) * rc * 0.8, cx + math.cos(an + 0.3) * rc * 0.8, cy + math.sin(an + 0.3) * rc * 0.8, "#ffffff", 5, pd * math.sin(q * math.pi))
        C(c, "FIELD IN THE CORE: ~50× STRONGER", 1440, 800, vis(t, B(1, 0.7)), ts, size=30, bg="#0d3a44")

# ------------------------------------------------------------------ m_field
def m_field(c, W, H, t, S):
    B = B_(S, 3); bg_space(c, W, H, t, S, seed=25)
    with Stage(c, S) as ts:
        pA = phase(t, None, B(1, 0))
        with Layer(c, pA) as on:
            if on:
                magnet_bar(c, 560, 560, 150)
                for k in range(3):
                    r_ = 210 + k * 60
                    oval(c, 560, 560, r_, r_ * 0.55, "#ff6b8a", 0.6 - 0.15 * k, stroke=5)
                earth(c, 1360, 560, 152, t)
                dipole(c, 1360, 560, 152, [1.6, 2.2], 0.5, width=2, tilt=-11)
                T(c, "FRIDGE MAGNET", 560, 820, 44, ts)
                T(c, "EARTH (SURFACE)", 1360, 820, 44, ts)
                T(c, ">", 960, 560, 160, ts, ACCENT, prog(t, 0.6, 0.4))
                C(c, "~20× STRONGER", 960, 160, vis(t, B(0, 0.45)), ts, size=40, bg=ACCENT, fg="#0b1030", a=1)
        pB = phase(t, B(1, 0))
        with Layer(c, pB) as on:
            if on:
                ex, ey, R = 560, 560, 46
                pan = eout(prog(t, B(2, 0), 2.5))
                c.save(); c.translate(-pan * 380, 0)
                sun(c, -260, 560, 160, t)
                wind(c, t, 1, -120, 2700, 160, 960, n=60, bow=(ex - R * 10 * 0.62, ey, R * 7))
                dipole(c, ex, ey, R, [2.2, 4, 6, 8, 10.3], 0.95, comp=0.62, stretch=1.0, tilt=-11, width=3, flow=True, t=t)
                # tail
                for k, dy in enumerate((-1, 1)):
                    for j in range(4):
                        yy = ey + dy * (60 + j * 55)
                        line(c, ex + 60, yy, 2600, ey + dy * (90 + j * 70), CYAN, 3, 0.6 * pan * (1 - j * 0.15), dash=([20, 14], -t * 40))
                earth(c, ex, ey, R, t)
                # 10 RE arrow
                xb = ex - R * 10 * 0.62
                pd = vis(t, B(1, 0.35))
                arrow(c, ex - R - 6, ey + 260, xb + 12, ey + 260, ACCENT, 5, pd); arrow(c, xb + 12, ey + 260, ex - R - 6, ey + 260, ACCENT, 5, pd)
                moon(c, 1980, 600, 30, lit=1, a=pan)
                text(c, "MOON", 1980, 660, 30, "#ffffff", pan, w=800)
                c.restore()
                C(c, "~10 EARTH RADII  ·  60,000+ KM", 520, 120, vis(t, B(1, 0.35), B(2, 0)), ts, dot=ACCENT)
                C(c, "TAIL REACHES FAR PAST THE MOON", 960, 120, vis(t, B(2, 0.3)), ts, dot=CYAN)

# ------------------------------------------------------------------ m_rules
def m_rules(c, W, H, t, S):
    B = B_(S, 2); bg_space(c, W, H, t, S, seed=26)
    with Stage(c, S) as ts:
        ex, ey, R = 620, 540, 170
        tsw = B(0, 0.22); on = 1 - eout(prog(t, tsw, 0.25))
        if prog(t, tsw, 0.01) > 0 and t < tsw + 0.3: circle(c, 1500, 470, 260, "#ffffff", 0.15 * (1 - (t - tsw) / 0.3), blur=40)
        dipole(c, ex, ey, R, [1.6, 2.3, 3.1], on, width=3.5, tilt=-11, flow=True, t=t)
        earth(c, ex, ey, R, t, spin=6)
        circle(c, ex, ey, R * 0.35, "#ffb03a", 0.0)
        switch(c, 1500, 430, 150, on)
        T(c, "DYNAMO", 1500, 140, 40, ts, "#bfe9e1")
        C(c, "CORE STAYS HOT", 620, 840, vis(t, B(0, 0.5), B(1, 0)), ts, dot="#ff7a3a")
        C(c, "PLANET KEEPS SPINNING", 620, 930, vis(t, B(0, 0.62), B(1, 0)), ts, dot="#4cd964")
        C(c, "MAGNETISM: GONE", 1500, 760, vis(t, B(0, 0.8)), ts, dot="#ff4d4d")
        stamp(c, "CAN'T REALLY HAPPEN", 620, 880, prog(t, B(1, 0.05), 0.35), ts * 0.55, color="#ff8a5a", rot=-6)
        C(c, "CORE ENERGY LEFT: HUNDREDS OF MILLIONS OF YEARS+", 960, 1010, vis(t, B(1, 0.35)), ts, size=28)

# ------------------------------------------------------------------ m_compass
NMP = [(-96.5, 70.1), (-96.0, 70.8), (-100.0, 72.5), (-101.0, 76.0), (-104.0, 78.5), (-110.8, 81.3), (-117.8, 83.1), (-130, 85.0), (-160, 86.3), (162.9, 86.5), (139.3, 85.8)]

def m_compass(c, W, H, t, S):
    long_ = S.n() >= 4; B = B_(S, 4)
    bg_space(c, W, H, t, S, seed=27)
    with Stage(c, S) as ts:
        if not long_:
            tsp = S.lt(0, 0.45)
            ang = needle_angle(t, tsp, 137)
            compass(c, 960, 540, 380, ang)
            C(c, "NO MORE NORTH", 960, 60, vis(t, S.lt(0, 0.55)), ts, size=40, bg="#5a1520")
            return
        pA = phase(t, None, B(2, 0))
        with Layer(c, pA) as on:
            if on:
                ang = needle_angle(t, B(1, 0.1), 137)
                compass(c, 960, 560, 360, ang)
                C(c, "POINTS NORTH", 960, 110, vis(t, B(0, 0.2), B(1, 0.1)), ts, dot="#4cd964")
                C(c, "NO MORE NORTH", 960, 110, vis(t, B(1, 0.2)), ts, dot="#ff4d4d", bg="#5a1520")
        pB = phase(t, B(2, 0), B(3, 0))
        with Layer(c, pB) as on:
            if on:
                gx, gy, R, rot, tilt = 960, 640, 400, -100, 58
                geo.globe(c, gx, gy, R, rot=rot, tilt=tilt)
                pts = [geo.globe_xy(lo, la, gx, gy, R, rot, tilt) for lo, la in NMP]
                q = eout(prog(t, B(2, 0.05), (B(2, 0.7) - B(2, 0.05))))
                n = len(pts); kq = q * (n - 1)
                gone = prog(t, B(2, 0.8), 0.4)
                for i in range(n - 1):
                    if i + 1 <= kq + 1e-6 or i < kq:
                        f = clamp(kq - i)
                        x0, y0, _ = pts[i]; x1, y1, _ = pts[i + 1]
                        line(c, x0, y0, lerp(x0, x1, f), lerp(y0, y1, f), ACCENT, 6, 1 - gone * 0.6)
                for i in range(n):
                    if i <= kq: circle(c, pts[i][0], pts[i][1], 8, ACCENT, 1 - gone * 0.6)
                i0 = min(int(kq), n - 2); f = kq - i0
                px = lerp(pts[i0][0], pts[i0 + 1][0], f); py = lerp(pts[i0][1], pts[i0 + 1][1], f)
                circle(c, px, py, 30 + 6 * math.sin(t * 5), "#ff4d4d", 0.35 * (1 - gone)); circle(c, px, py, 15, "#ff4d4d", 1 - gone)
                circle(c, px, py, 15, "#ffffff", 1 - gone, stroke=3)
                xmark(c, px, py, 40, gone)
                text(c, "1831", pts[0][0] - 60, pts[0][1] + 20, 34, "#ffffff", vis(t, B(2, 0.1)), w=900, shadow=8)
                if q > 0.95: text(c, "TODAY", pts[-1][0] + 80, pts[-1][1] + 10, 34, "#ffffff", 1 - gone, w=900, shadow=8)
                C(c, "MAGNETIC NORTH: 1,100+ KM SINCE 1831", 960, 80, vis(t, B(2, 0.1)), ts, size=32, dot=ACCENT)
                C(c, "UP TO ~55 KM A YEAR", 960, 170, vis(t, B(2, 0.45)), ts, size=30)
        pC = phase(t, B(3, 0))
        with Layer(c, pC) as on:
            if on:
                # phone + GPS
                rrect(c, 520, 290, 300, 560, 40, "#1b2233"); rrect(c, 540, 330, 260, 480, 20, "#0e3a4a")
                compass(c, 670, 560, 100, 30 * math.sin(t * 3) + 90 * math.sin(t * 1.1), lab=False)
                T(c, "?", 670, 760, 80, ts, "#ff6b6b")
                ang = t * 8
                sx, sy = 1340 + math.cos(math.radians(ang)) * 60, 360
                satellite(c, sx, sy, 140)
                for k in range(3):
                    r_ = 60 + ((t * 120 + k * 80) % 240)
                    pp = skia.Path(); pp.addArc(skia.Rect.MakeXYWH(sx - r_, sy + 40 - r_, 2 * r_, 2 * r_), 50, 80)
                    c.drawPath(pp, paint(CYAN, 1 - r_ / 300, stroke=5))
                rect(c, 1240, 760, 200, 30, "#2a3a44"); text(c, "GPS", 1340, 720, 48, CYAN, 1, w=900)
                C(c, "PHONE COMPASS: GIVES UP", 670, 120, vis(t, B(3, 0.1)), ts, dot="#ff4d4d")
                C(c, "GPS: STILL WORKS (FOR NOW)", 1340, 900, vis(t, B(3, 0.4)), ts, dot="#4cd964")

# ------------------------------------------------------------------ m_air
def m_air(c, W, H, t, S):
    long_ = S.n() >= 3; B = B_(S, 3)
    fill_bg(c, W, H, "#06182a", "#1d4a6a"); stars(c, W, H, t, 0.5, seed=28)
    with Stage(c, S) as ts:
        vrect(c, 900, VH + 2, "#20402e", "#0e1e16")
        pA = phase(t, None, B(2, 0)) if long_ else 1.0
        with Layer(c, pA) as on:
            if on:
                cx = 720 if long_ else 960
                c.drawRect(skia.Rect.MakeLTRB(cx - 120, -2000, cx + 120, 900), paint(shader=lin(0, 80, 0, 900, [(0, "#7fd3ff", 0.05), (1, "#7fd3ff", 0.45)])))
                rect(c, cx - 120, 80, 240, 820, "#bfe9ff", 0.6, stroke=3)
                person(c, cx, 900, 250, "#e8eef8")
                rng = random.Random(4)
                for k in range(14):
                    x = cx + rng.uniform(-110, 110); ph = rng.random(); q = (t * 0.9 + ph) % 1
                    y = -60 + q * 700; stop = 160 + rng.random() * 480
                    if y < stop:
                        line(c, x, y - 60, x, y, "#ff9a4a", 4, 0.9)
                    else:
                        age = (y - stop) / 120
                        if age < 1: circle(c, x, stop, 8 + 20 * age, "#ffd27a", 1 - age)
                C(c, "THE AIR IS THE REAL SHIELD", 1520 if long_ else 960, 200 if long_ else 30, vis(t, B(0, 0.1) if long_ else S.lt(0, 0.4)), ts, dot=CYAN)
                pk = vis(t, B(0, 0.45)) if long_ else 0
                C(c, "≈1 KG OF AIR ON EVERY CM²", 1520, 320, pk, ts, dot="#bfe9ff")
                if long_:
                    # water column
                    pw = vis(t, B(1, 0.0))
                    wx = 1060
                    rect(c, wx - 90, 900 - 640 * eout(pw), 180, 640 * eout(pw), "#2f86d8", 0.75 * pw)
                    line(c, wx + 120, 260, wx + 120, 900, ACCENT, 4, pw)
                    T(c, "≈ 10 M OF WATER", wx + 150, 580, 40, ts, ACCENT, pw, align="l")
                    T(c, "=", 900, 580, 90, ts, "#ffffff", pw)
                    C(c, "TODAY: ~0.33 mSv / YEAR ≈ 1/10 OF BACKGROUND", 960, 1010, vis(t, B(1, 0.5)), ts, size=28)
        if long_:
            pB = phase(t, B(2, 0))
            with Layer(c, pB) as on:
                if on:
                    rect(c, -600, -4000, 3200, 10000, "#071a26", 0.92)
                    C(c, "MODEL OF A MUCH WEAKER FIELD", 960, 110, vis(t, B(2, 0.0)), ts, dot=CYAN)
                    rows = [("GROUND, WORLDWIDE", 0.13, "+13%"), ("GROUND, NEAR EQUATOR", 0.25, "~+25%"), ("HIGH IN THE ATMOSPHERE", 1.0, "SEVERAL ×")]
                    for k, (lab, f, val) in enumerate(rows):
                        p = eout(prog(t, B(2, 0.1 + k * 0.25), 0.6))
                        bar(c, 300, 330 + k * 230, 1000, 70, f * p, [CYAN, ACCENT, "#ff6b4a"][k], 1, label=lab, val=val if p > 0.5 else None, a=prog(t, B(2, 0.05 + k * 0.25), 0.3))
    kit.hook(c, W, H, t, S)

# ------------------------------------------------------------------ m_aurora
def m_aurora(c, W, H, t, S):
    B = B_(S, 3); bg_space(c, W, H, t, S, seed=29)
    with Stage(c, S) as ts:
        pA = phase(t, None, B(1, 0))
        with Layer(c, pA) as on:
            if on:
                gx, gy, R, rot, tilt = 960, 600, 360, -90, 40
                dipole(c, gx, gy, R, [1.25, 1.5, 1.9], 0.7, width=3, flow=True, t=t)
                geo.globe(c, gx, gy, R, rot=rot + t * 2, tilt=tilt, night=0.55)
                # auroral oval around north pole
                pts = []
                for i in range(60):
                    lo = i * 6; x, y, v = geo.globe_xy(lo, 67 + 2 * math.sin(i * 0.5 + t), gx, gy, R, rot + t * 2, tilt)
                    pts.append((x, y, v))
                for i in range(60):
                    x0, y0, v0 = pts[i]; x1, y1, v1 = pts[(i + 1) % 60]
                    if v0 and v1:
                        line(c, x0, y0, x1, y1, AUR_G, 22, 0.35); line(c, x0, y0, x1, y1, "#c8ffe0", 6, 0.9)
                C(c, "TODAY: AURORAS HUG THE POLES", 960, 100, vis(t, B(0, 0.1)), ts, dot=AUR_G)
                C(c, "THE FIELD FUNNELS PARTICLES IN", 960, 1010, vis(t, B(0, 0.55)), ts)
        pB = phase(t, B(1, 0), B(2, 0))
        with Layer(c, pB) as on:
            if on:
                mars(c, 960, 560, 330)
                glow = 0.5 + 0.2 * math.sin(t * 2)
                circle(c, 960, 560, 330, "#9a6bff", 0.3 * glow)
                circle(c, 960, 560, 360, "#b48aff", 0.35 * glow, stroke=26, blur=14)
                C(c, "MARS: NO GLOBAL FIELD", 960, 100, vis(t, B(1, 0.05)), ts, dot="#ff7a3a")
                C(c, "STORMS LIGHT UP THE WHOLE SKY", 960, 1010, vis(t, B(1, 0.4)), ts, dot="#b48aff")
        pC = phase(t, B(2, 0))
        with Layer(c, pC) as on:
            if on:
                vrect(c, -1, 760, "#020814", "#0b2a3a")
                aurora_curtain(c, -100, 2020, 560, 420, t, 0.75, seed=3)
                aurora_curtain(c, 200, 1800, 680, 300, t + 3, 0.5, colr="#7affc0", seed=7)
                vrect(c, 760, VH + 2, "#0a1612", "#04080a")
                cityline(c, -40, 1960, 800, 0.8)
                C(c, "DIM GLOWS AT EVERY LATITUDE?", 960, 100, vis(t, B(2, 0.05)), ts, dot=AUR_G)
                C(c, "MAY 2024: AURORAS SEEN IN MEXICO", 960, 1000, vis(t, B(2, 0.6)), ts, dot=AUR_M)

# ------------------------------------------------------------------ m_orbit
def m_orbit(c, W, H, t, S):
    long_ = S.n() >= 3; B = B_(S, 3)
    bg_space(c, W, H, t, S, seed=30)
    with Stage(c, S) as ts:
        ex, ey, R = (760, 560, 150) if long_ else (960, 560, 220)
        pA = phase(t, None, B(2, 0)) if long_ else 1.0
        with Layer(c, pA) as on:
            if on:
                drain = eout(prog(t, B(0, 0.3), 2.0)) if long_ else eout(prog(t, 0.0, 1.2))
                for L, colr in ((1.6, "#ff7a3a"), (3.6, "#ff4fd8")):
                    dipole(c, ex, ey, R, [L], 0.8 * (1 - drain), colr=colr, width=36, tilt=-11)
                wa = vis(t, B(1, 0.0)) if long_ else vis(t, S.lt(0, 0.1))
                wind(c, t, wa, -200, 2200, 120, 980, n=60, hit=(ex, ey, R * 1.08))
                earth(c, ex, ey, R, t)
                for k in range(4):
                    an = t * (0.5 - k * 0.07) + k * 1.6; rr = R * (1.9 + k * 0.7)
                    sx, sy = ex + math.cos(an) * rr, ey + math.sin(an) * rr * 0.5
                    hp = ((t * 0.9 + k * 0.3) % 1.4) / 0.6 if wa > 0.3 else 2
                    if k == 1: station(c, sx, sy, 70)
                    else: satellite(c, sx, sy, 60, ang=an * 30, hitp=hp if hp < 1 else 0)
                C(c, "VAN ALLEN BELTS: DRAINED", 960, 90, vis(t, B(0, 0.35), B(1, 0)) if long_ else vis(t, 0.3, S.lt(0, 0.35)), ts, dot="#ff7a3a")
                C(c, "SATELLITES + ASTRONAUTS EXPOSED", 960, 90 if long_ else 1000, vis(t, B(1, 0.2)) if long_ else vis(t, S.lt(0, 0.4)), ts, dot="#ff4d4d", bg="#5a1520")
        if long_:
            pB = phase(t, B(2, 0))
            with Layer(c, pB) as on:
                if on:
                    c.drawCircle(960, 2600, 1900, paint(shader=rad(960, 2600, 1900, [(0.9, "#1f6fd1", 1), (1, "#7fc8ff", 1)])))
                    circle(c, 960, 2600, 1960, "#7fc8ff", 0.25, blur=30)
                    px = 300 + (t - B(2, 0)) * 120
                    plane(c, px % 2100 - 100, 640, 90)
                    rng = random.Random(9)
                    for k in range(18):
                        x = rng.uniform(0, 1920); ph = rng.random(); q = (t * 0.8 + ph) % 1
                        line(c, x, -60 + q * 700, x - 10, q * 700, "#ff9a4a", 3, 0.7 * math.sin(q * math.pi))
                    gauge(c, 1560, 330, 150, 0.35 + 0.35 * eout(prog(t, B(2, 0.4), 1.5)), "FLIGHT DOSE", 1, colr="#ff9a4a")
                    C(c, "2026 STUDY: HIGHER DOSE ON SOME ROUTES", 960, 110, vis(t, B(2, 0.35)), ts, dot="#ff9a4a")
    kit.hook(c, W, H, t, S)

# ------------------------------------------------------------------ m_storm
def m_storm(c, W, H, t, S):
    B = B_(S, 4); bg_space(c, W, H, t, S, seed=31)
    with Stage(c, S) as ts:
        p0 = phase(t, None, B(1, 0))
        with Layer(c, p0) as on:
            if on:
                sun(c, 420, 540, 240, t)
                q = prog(t, B(0, 0.25), 2.2)
                for k in range(26):
                    an = (k / 26 - 0.5) * 0.9; d = 260 + q * 1300 * (0.8 + 0.3 * math.sin(k))
                    circle(c, 420 + math.cos(an) * d, 540 + math.sin(an) * d, 10 + q * 22, "#ffb06a", 0.7 * (1 - q * 0.6), blur=6)
                earth(c, 1700, 540, 90, t)
                C(c, "THE SUN THROWS STORMS. OFTEN.", 960, 950, vis(t, B(0, 0.2)), ts, dot=WIND)
        p1 = phase(t, B(1, 0), B(2, 0))
        with Layer(c, p1) as on:
            if on:
                vrect(c, -1, 760, "#120a26", "#3a1a4a")
                aurora_curtain(c, 0, 1920, 520, 380, t, 0.8, colr="#ff5a6a", colr2="#ff9ad8", seed=5)
                vrect(c, 760, VH + 2, "#2a1e16", "#120c08")
                for k, x in enumerate((300, 800, 1300, 1800)):
                    telegraph(c, x, 780, 300, 1.0 if t > B(1, 0.15) else 0, t + k)
                for k in range(3):
                    p = skia.Path(); p.moveTo(-50, 780 - 300 * 1.53 + k * 0); p.lineTo(2000, 780 - 300 * 1.53)
                for k in (-0.3, 0, 0.3):
                    line(c, -50, 780 - 459 + 4, 2000, 780 - 459 + 4, "#2a2a2a", 2, 0.8)
                telegraph_key(c, 960, 930, 120, 0.5 + 0.5 * math.sin(t * 9))
                C(c, "1859 · CARRINGTON EVENT", 960, 90, vis(t, B(1, 0.05)), ts, dot="#ff5a6a")
                C(c, "TELEGRAPHS RAN WITH BATTERIES UNPLUGGED", 960, 180, vis(t, B(1, 0.5)), ts, size=30)
        p2 = phase(t, B(2, 0), B(2, 0.42))
        with Layer(c, p2) as on:
            if on:
                vrect(c, -1, 820, "#03060e", "#0b1428")
                stars(c, VW, VH, t, 0.6, seed=12)
                off = prog(t, B(2, 0.12), 0.25)
                cityline(c, -40, 1960, 820, 1 - off, seed=9)
                vrect(c, 820, VH + 2, "#05080c", "#020305")
                C(c, "1989 · QUEBEC", 960, 90, vis(t, B(2, 0.0)), ts, dot=ACCENT)
                C(c, "6 MILLION PEOPLE · 9 HOURS", 960, 180, vis(t, B(2, 0.18)), ts, size=30)
        p3 = phase(t, B(2, 0.42), B(2, 0.78))
        with Layer(c, p3) as on:
            if on:
                c.drawCircle(960, 2500, 1700, paint(shader=rad(960, 2500, 1700, [(0.92, "#1f6fd1", 1), (1, "#9fd3ff", 1)])))
                for k in range(10):
                    st_ = B(2, 0.45) + k * 0.12; q = prog(t, st_, 2.2)
                    x = 200 + k * 160 + q * 220; y = 220 + (k % 3) * 60 + q * q * 520
                    satellite(c, x, y, 34, a=1 - q * 0.5, ang=q * 90)
                    if q > 0: line(c, x - 40 * q, y - 60 * q, x, y, "#ff9a4a", 4, 0.8 * q)
                C(c, "2022 · 38 STARLINK SATELLITES LOST", 960, 90, vis(t, B(2, 0.44)), ts, dot="#ff9a4a")
        p4 = phase(t, B(2, 0.78), B(3, 0))
        with Layer(c, p4) as on:
            if on:
                vrect(c, -1, 500, "#7fb8ff", "#d6ecff"); vrect(c, 500, VH + 2, "#6b8f3a", "#3a5a20")
                for k in range(9): line(c, 960 + (k - 4) * 60, 500, 960 + (k - 4) * 420, 1200, "#4f6f2a", 10, 0.8)
                q = prog(t, B(2, 0.8), 3.0)
                tx = 960 + q * 400; ty = 900 - q * 300
                dashed_path(c, [(960, 1100), (960, 600)], "#ffffff", 6, 0.8)
                c.save(); c.translate(tx, ty); c.rotate(15 * q); tractor(c, 0, 0, 220); c.restore()
                C(c, "2024 · GPS TRACTORS DRIFTED OFF COURSE", 960, 90, vis(t, B(2, 0.8)), ts, dot="#3fae4a")
        p5 = phase(t, B(3, 0))
        with Layer(c, p5) as on:
            if on:
                ex, ey, R = 960, 560, 170
                wind(c, t, 1, -200, 2200, 120, 980, n=60, bow=(ex - R * 2.3, ey, R * 1.9))
                dipole(c, ex, ey, R, [1.5, 2.1, 2.9, 3.8], 1, comp=0.6, stretch=1.5, tilt=-11, width=4, flow=True, t=t)
                earth(c, ex, ey, R, t)
                C(c, "ALL OF THAT: WITH THE SHIELD UP", 960, 1000, vis(t, B(3, 0.1)), ts, size=40, bg=ACCENT, fg="#0b1030", a=1)

# ------------------------------------------------------------------ m_ozone
def m_ozone(c, W, H, t, S):
    B = B_(S, 3); long_ = S.n() >= 3
    fill_bg(c, W, H, "#020a14", "#06223a"); stars(c, W, H, t, 0.6, seed=32)
    with Stage(c, S) as ts:
        cy0 = 2300; Rr = 1700
        thin = eout(prog(t, B(0, 0.4), (B(1, 0.6) - B(0, 0.4)) + 0.01))
        c.drawCircle(960, cy0, Rr + 260, paint(shader=rad(960, cy0, Rr + 260, [(0.84, "#2b7fd8", 0.8), (1, "#2b7fd8", 0)])))
        # ozone layer band
        oz = 1 - 0.75 * thin
        seg = 140
        c.drawCircle(960, cy0, Rr + 150, paint("#8a7bff", 0.6 * oz + 0.15, stroke=60 * (0.45 + 0.55 * oz), cap="butt",
                     dash=([seg * (1 - 0.55 * thin), seg * 0.55 * thin + 0.01], 0)))
        rng = random.Random(3)
        c.drawCircle(960, cy0, Rr, paint(shader=rad(960, cy0, Rr, [(0.95, "#1f6fd1", 1), (1, "#3dbb6c", 1)])))
        T(c, "OZONE LAYER", 1500, cy0 - Rr - 150 + 10, 30, ts, "#c8bfff", 1, w=800)
        # particles from above
        pa = vis(t, B(0, 0.0))
        for k in range(40):
            x = rng.uniform(100, 1820); ph = rng.random(); q = (t * 0.7 + ph) % 1
            y = -100 + q * 520
            line(c, x - 20, y - 50, x, y, "#ff9a4a", 4, pa * math.sin(q * math.pi))
        # UV arrows
        pu = vis(t, B(1, 0.4))
        for k in range(5):
            x = 400 + k * 280; q = (t * 0.8 + k * 0.2) % 1
            arrow(c, x, 120 + q * 200, x + 30, 260 + q * 300, "#d06bff", 8, pu * math.sin(q * math.pi))
        C(c, "STORM PARTICLES → OZONE-EATING CHEMICALS", 960, 90, vis(t, B(0, 0.25), B(1, 0) if long_ else None), ts, size=30, dot="#ff9a4a")
        C(c, "2024 MODEL: SEVERE LOSS FOR YEARS", 960, 90 if long_ else 180, vis(t, B(1, 0.15)), ts, dot="#8a7bff")
        C(c, "UV AT THE SURFACE: UP TO ~25% MORE", 960, 190 if long_ else 270, vis(t, B(1, 0.6)), ts, dot="#d06bff")
        if long_:
            pp = vis(t, B(2, 0.3))
            for k, x in enumerate((560, 760, 1160, 1360)):
                if k < 2: leaf_icon(c, x, 470, 50, a=pp)
                else: microbe(c, x, 470, 40, t, pp, colr="#7ee0c8")
            C(c, "PLANTS + PLANKTON STRESSED", 960, 330, pp, ts, dot="#7ee081")

# ------------------------------------------------------------------ m_animals
def m_animals(c, W, H, t, S):
    B = B_(S, 3)
    fill_bg(c, W, H, "#0c3550", "#1e6a8a")
    with Stage(c, S) as ts:
        vrect(c, -1, 520, "#5fa8d8", "#b8e2f6")
        vrect(c, 520, VH + 2, "#1f6fa8", "#0a2e4a")
        c.drawPath(poly([(1650, 520), (2600, 520), (2600, 1200), (1500, 1200)]), paint("#e8d39a"))
        scr = prog(t, B(2, 0.25), 1.0) if S.n() >= 3 else 0
        pt = vis(t, B(0, 0.0))
        tp = curve_pts(150, 900, 1620, 620, 160)
        dashed_path(c, tp, "#ffffff", 5, pt * 0.8, t, wob=60 * scr, seed=1)
        q = (t * 0.06) % 1 if scr == 0 else 0.4 + 0.05 * math.sin(t)
        i = int(q * (len(tp) - 1)); turtle(c, tp[i][0] + math.sin(t * 2) * 30 * scr, tp[i][1] + math.cos(t * 2.3) * 30 * scr, 90, t, pt)
        nest = vis(t, B(0, 0.5))
        for k in range(5): circle(c, 1780 + (k % 3) * 34, 600 + (k // 3) * 30, 14, "#f4eedd", nest)
        C(c, "TURTLES RETURN TO THEIR BIRTH BEACH", 860, 600, vis(t, B(0, 0.3), B(1, 0)), ts, dot="#5f8f4a")
        ps = vis(t, B(1, 0.0))
        sp = curve_pts(1400, 980, 300, 760, -80)
        dashed_path(c, sp, "#ffc0a8", 5, ps * 0.8, t, wob=60 * scr, seed=2)
        i = int(((t * 0.08) % 1) * (len(sp) - 1)); salmon(c, sp[i][0] + math.sin(t * 2) * 40 * scr, sp[i][1], 110, t, ps)
        rp = curve_pts(200, 380, 1700, 160, 120)
        dashed_path(c, rp, "#ffffff", 5, ps * 0.8, t, wob=70 * scr, seed=3)
        i = int(((t * 0.07) % 1) * (len(rp) - 1)); robin(c, rp[i][0] + math.sin(t * 2.7) * 50 * scr, rp[i][1] + math.cos(t * 2) * 40 * scr, 120, t, ps)
        C(c, "SALMON FIND HOME BY THE FIELD", 960, 1010, vis(t, B(1, 0.05), B(2, 0)), ts, dot="#ff8a6a")
        C(c, "ROBINS: BUILT-IN MAGNETIC COMPASS", 960, 60, vis(t, B(1, 0.45), B(2, 0)), ts, dot="#e8743a")
        C(c, "BACKUPS: SUN · STARS · SMELL", 960, 60, vis(t, B(2, 0.05)), ts, dot=ACCENT)
        C(c, "MESSY MIGRATIONS", 960, 1010, vis(t, B(2, 0.45)), ts, dot="#ff4d4d", bg="#5a1520")

# ------------------------------------------------------------------ m_mars
def m_mars(c, W, H, t, S):
    B = B_(S, 2); bg_space(c, W, H, t, S, seed=33)
    with Stage(c, S) as ts:
        mx, my, R = 820, 560, 300
        wind(c, t, 1, -200, 2200, 140, 980, n=60, hit=(mx, my, R * 1.05))
        rng = random.Random(8)
        for k in range(40):  # escaping atmosphere
            ph = rng.random(); q = (t * 0.25 + ph) % 1; an = rng.uniform(-1.3, 1.3)
            sx = mx + math.cos(an) * R * 1.05; sy = my + math.sin(an) * R * 1.05
            x = sx + q * 900; y = sy + math.sin(an) * q * 300
            circle(c, x, y, 5 + q * 10, "#cfe6ff", 0.6 * (1 - q))
        mars(c, mx, my, R, crust=vis(t, B(1, 0.65)))
        C(c, "MARS: GLOBAL FIELD DIED ~4 BILLION YEARS AGO", 960, 90, vis(t, B(0, 0.4)), ts, size=30, dot="#ff7a3a")
        C(c, "MAVEN: ~100 G OF AIR STRIPPED EVERY SECOND", 960, 1010, vis(t, B(1, 0.1)), ts, size=30, dot="#cfe6ff")
        C(c, "FOSSIL MAGNETISM IN THE CRUST", 1500, 860, vis(t, B(1, 0.7)), ts, size=30, dot=CYAN)

# ------------------------------------------------------------------ m_venus
def m_venus(c, W, H, t, S):
    B = B_(S, 3); bg_space(c, W, H, t, S, seed=34)
    with Stage(c, S) as ts:
        pA = phase(t, None, B(1, 0))
        with Layer(c, pA) as on:
            if on:
                vx, vy, R = 1000, 560, 260
                wind(c, t, 1, -200, 2200, 120, 980, n=60, bow=(vx - R * 1.25, vy, R * 1.0))
                sh = vis(t, B(0, 0.7))
                for k in range(4):
                    rr = R * (1.25 + k * 0.14)
                    p = skia.Path(); p.addArc(skia.Rect.MakeXYWH(vx - rr, vy - rr, 2 * rr, 2 * rr), 110, 140)
                    c.drawPath(p, paint(CYAN, sh * (0.7 - k * 0.12), stroke=4))
                venus(c, vx, vy, R, t)
                C(c, "VENUS: NO FIELD OF ITS OWN", 960, 90, vis(t, B(0, 0.1)), ts, dot="#e8c98a")
                C(c, "AIR ~90× HEAVIER THAN EARTH'S", 960, 1010, vis(t, B(0, 0.35)), ts, dot=ACCENT)
                C(c, "INDUCED SHELL FROM THE SOLAR WIND", 420, 860, vis(t, B(0, 0.75)), ts, size=28, dot=CYAN)
        pB = phase(t, B(1, 0), B(2, 0))
        with Layer(c, pB) as on:
            if on:
                for k, (nm, xx) in enumerate((("EARTH", 480), ("MARS", 960), ("VENUS", 1440))):
                    if k == 0: earth(c, xx, 520, 140, t)
                    elif k == 1: mars(c, xx, 520, 110)
                    else: venus(c, xx, 520, 150, t)
                    for j in range(4):
                        q = (t * 0.5 + j / 4) % 1
                        circle(c, xx + 150 + q * 120, 450 + j * 40, 6, "#cfe6ff", 0.8 * (1 - q))
                    T(c, nm, xx, 760, 40, ts)
                C(c, "2018 STUDY: ~0.5–2 KG/S EACH", 960, 100, vis(t, B(1, 0.4)), ts, dot=CYAN)
                C(c, "FIELD OR NO FIELD", 960, 900, vis(t, B(1, 0.6)), ts)
        pC = phase(t, B(2, 0))
        with Layer(c, pC) as on:
            if on:
                earth(c, 760, 560, 260, t)
                circle(c, 760, 560, 300, "#7fc8ff", 0.25 + 0.05 * math.sin(t * 2), stroke=30, blur=10)
                gauge(c, 1450, 600, 220, 0.995 - 0.01 * prog(t, B(2, 0.2), 3), "AIR LEFT AFTER 1 MILLION YEARS", 1, valtxt="~ALL", colr="#4cd964")
                C(c, "STILL BREATHING", 1450, 860, vis(t, B(2, 0.7)), ts, size=40, bg="#123d2a", dot="#4cd964")

# ------------------------------------------------------------------ m_laschamp
def laschamp_curve(x):  # x: years ago 60000..0 -> field %
    d = 1 - math.exp(-((x - 41000) / 2400) ** 2) * 0.95
    base = 75 + 25 * (1 - x / 60000) + 6 * math.sin(x / 5000)
    return base * d

def m_laschamp(c, W, H, t, S):
    long_ = S.n() >= 4; B = B_(S, 4)
    bg_space(c, W, H, t, S, seed=35)
    with Stage(c, S) as ts:
        gx0, gy0, gw, gh = 260, 200, 1400, 600
        pA = phase(t, None, B(2, 0)) if long_ else 1.0
        with Layer(c, pA) as on:
            if on:
                ap = vis(t, 0.0)
                graph_axes(c, gx0, gy0, gw, gh, ap, ts, xl="THOUSANDS OF YEARS AGO", yl="FIELD STRENGTH")
                for v, lab in ((60, "60"), (40, "40"), (20, "20"), (0, "NOW")):
                    x = gx0 + (60 - v) / 60 * gw
                    text(c, lab, x, gy0 + gh + 22, 24 * ts, "#bfe9e1", ap, w=700, fam="Inter")
                dr = eout(prog(t, B(1, 0.0) if long_ else 0.2, (B(1, 0.7) - B(1, 0.0)) if long_ else S.dur * 0.6))
                p = skia.Path(); n = 140
                for i in range(int(n * dr) + 1):
                    yrs = 60000 - 60000 * i / n; v = laschamp_curve(yrs)
                    x = gx0 + i / n * gw; y = gy0 + gh - v / 110 * gh
                    (p.moveTo if i == 0 else p.lineTo)(x, y)
                c.drawPath(p, paint(CYAN, 0.3, stroke=14)); c.drawPath(p, paint(CYAN, 1, stroke=5))
                xd = gx0 + (60 - 41) / 60 * gw; yd = gy0 + gh - laschamp_curve(41000) / 110 * gh
                pd = prog(t, (B(1, 0.45) if long_ else S.lt(0, 0.6)), 0.4)
                circle(c, xd, yd, 16, "#ff4d4d", pd); circle(c, xd, yd, 34 + 6 * math.sin(t * 5), "#ff4d4d", 0.3 * pd)
                T(c, "~5%", xd + 50, yd - 110, 64, ts, "#ff6b6b", pd, align="l")
                C(c, "41,000 YEARS AGO · LASCHAMP", 960, 90, vis(t, B(1, 0.2)) if long_ else 0, ts, dot="#ff4d4d")
                if long_:
                    C(c, "NEANDERTHALS STILL ALIVE", 1350, 980, vis(t, B(1, 0.75)), ts, dot=ACCENT)
                    C(c, "IT REALLY HAPPENED", 960, 90, vis(t, B(0, 0.2), B(1, 0.15)), ts, dot=CYAN)
        if long_:
            pB = phase(t, B(2, 0))
            with Layer(c, pB) as on:
                if on:
                    tree_rings(c, 560, 540, 300)
                    C(c, "ANCIENT KAURI TREES: OZONE HIT? EXTINCTIONS?", 960, 90, vis(t, B(2, 0.05)), ts, size=30, dot="#e2b67c")
                    pi_ = vis(t, B(3, 0.05))
                    ice_core(c, 1360, 560, 140, 640, pi_)
                    xmark(c, 1360, 560, 70, prog(t, B(3, 0.4), 0.35))
                    C(c, "ICE CORES: NO CLEAR CLIMATE SIGNAL", 1360, 960, vis(t, B(3, 0.3)), ts, size=28, dot="#9fd3ff")
                    stamp(c, "DEBATED", 960, 560, prog(t, B(3, 0.7), 0.35), ts, color=ACCENT, rot=-12)
    kit.hook(c, W, H, t, S)

# ------------------------------------------------------------------ m_today
TB = (-180, -60, 180, 80)
_MAPS = {}
def _map_img(rr):
    if rr not in _MAPS:
        surf = skia.Surface(rr[2], rr[3]); cc = surf.getCanvas()
        cc.translate(-rr[0], -rr[1])
        geo.draw_map(cc, TB, rr, land="#2f5a4a", sea="#0b2e3a", outline_w=2)
        _MAPS[rr] = surf.makeImageSnapshot()
    return _MAPS[rr]

def m_today(c, W, H, t, S):
    B = B_(S, 3); bg_space(c, W, H, t, S, seed=36)
    with Stage(c, S) as ts:
        pA = phase(t, None, B(1, 0))
        with Layer(c, pA) as on:
            if on:
                gx0, gy0, gw, gh = 300, 230, 1320, 560
                graph_axes(c, gx0, gy0, gw, gh, 1, ts, xl="YEAR", yl="FIELD STRENGTH")
                for k, yr in enumerate((1825, 1875, 1925, 1975, 2025)):
                    text(c, str(yr), gx0 + gw * k / 4, gy0 + gh + 22, 24 * ts, "#bfe9e1", 1, w=700, fam="Inter")
                dr = eout(prog(t, 0.2, max(0.5, B(0, 0.8) - 0.2)))
                p = skia.Path()
                for i in range(int(80 * dr) + 1):
                    q = i / 80; v = 1 - 0.09 * q + 0.004 * math.sin(q * 20)
                    x = gx0 + q * gw; y = gy0 + gh * (1 - (v - 0.85) / 0.18)
                    (p.moveTo if i == 0 else p.lineTo)(x, y)
                c.drawPath(p, paint(CYAN, 0.3, stroke=14)); c.drawPath(p, paint(CYAN, 1, stroke=5))
                C(c, "~9% WEAKER IN ~200 YEARS", 960, 110, vis(t, B(0, 0.4)), ts, size=40, dot="#ff6b6b")
        pB = phase(t, B(1, 0), B(2, 0))
        with Layer(c, pB) as on:
            if on:
                rr = geo.map_rect(TB, 960, 560, width=1800)
                c.drawImage(_map_img(rr), rr[0], rr[1])
                ax, ay = geo.lonlat_xy(-45, -25, TB, rr)
                g = eout(prog(t, B(1, 0.2), 3.0))
                c.save(); c.clipRect(skia.Rect.MakeXYWH(*rr))
                for k in range(5):
                    oval(c, ax, ay, (180 + 160 * g) * (1 - k * 0.17), (120 + 70 * g) * (1 - k * 0.17), "#ff4d4d", 0.16 + 0.06 * k)
                if g > 0.3:
                    oval(c, ax + 330 * g, ay + 10, 90 * g, 60 * g, "#ff4d4d", 0.3)
                c.restore()
                rect(c, rr[0], rr[1], rr[2], rr[3], "#ffffff", 0.6, stroke=3)
                sx = rr[0] + ((t * 140) % rr[2]); sy = ay - 40
                satellite(c, sx, sy, 50, hitp=((t * 1.5) % 1) if abs(sx - ax) < 260 else 0)
                C(c, "SOUTH ATLANTIC ANOMALY", 960, 90, vis(t, B(1, 0.05)), ts, dot="#ff4d4d")
                C(c, "SINCE 2014: + ~HALF THE AREA OF EUROPE", 960, 1010, vis(t, B(1, 0.45)), ts, size=30)
        pC = phase(t, B(2, 0))
        with Layer(c, pC) as on:
            if on:
                gauge(c, 960, 600, 320, 0.66 + 0.01 * math.sin(t), "FIELD STRENGTH TODAY", 1, colr=CYAN)
                T(c, "~2× ITS MILLION-YEAR AVERAGE", 960, 900, 80, ts, CYAN, vis(t, B(2, 0.4)))
                C(c, "ESA: STILL NORMAL UPS AND DOWNS", 960, 110, vis(t, B(2, 0.1)), ts, dot="#4cd964")

# ------------------------------------------------------------------ m_flip (Shorts)
def m_flip(c, W, H, t, S):
    mode = S.opts.get("mode", "intro"); bg_space(c, W, H, t, S, seed=37)
    L0 = S.lt(0, 0); L1 = S.lt(0, 1)
    with Stage(c, S) as ts:
        if mode == "intro":
            ex, ey, R = 760, 560, 200
            fl = eout(prog(t, lerp(L0, L1, 0.45), 1.2))
            dipole(c, ex, ey, R, [1.5, 2.1, 2.8], 1, width=4, tilt=-11 + 180 * fl, flow=True, t=t)
            earth(c, ex, ey, R, t)
            nlab, slab = ("N", "S") if fl < 0.5 else ("S", "N")
            al = abs(fl - 0.5) * 2
            T(c, nlab, ex, ey - R - 70, 70, ts, "#ff6b6b", al); T(c, slab, ex, ey + R + 70, 70, ts, CYAN, al)
            ang = 0 if fl < 0.5 else needle_angle(t, lerp(L0, L1, 0.6), 180)
            compass(c, 1460, 560, 260, ang)
            C(c, "COMPASS POINTS SOUTH", 1460, 920, vis(t, lerp(L0, L1, 0.7)), ts, size=30, dot="#ff6b6b")
        elif mode == "timeline":
            rng = random.Random(11); x = 80; k = 0
            q = eout(prog(t, 0.2, max(0.5, L1 * 0.7)))
            while x < 1840:
                wdt = rng.uniform(8, 50); xx = x
                if (xx - 80) / 1760 <= q:
                    rect(c, xx, 360, wdt, 300, "#e8eef8" if k % 2 == 0 else "#0a1a20")
                x += wdt; k += 1
            rect(c, 80, 360, 1760, 300, "#ffffff", 0.5, stroke=3)
            T(c, "83 MILLION YEARS AGO", 120, 720, 26, ts, "#bfe9e1", 1, w=700, fam="Inter", align="l")
            T(c, "NOW", 1800, 720, 26, ts, "#bfe9e1", 1, w=700, fam="Inter", align="r")
            C(c, "NORMAL / REVERSED", 960, 280, vis(t, 0.3), ts, size=30)
            pm = vis(t, lerp(L0, L1, 0.55))
            line(c, 1828, 330, 1828, 690, ACCENT, 8, pm)
            C(c, "LAST FULL FLIP: ~780,000 YEARS AGO", 960, 860, pm, ts, size=30, dot=ACCENT)
        elif mode == "messy":
            ex, ey, R = 960, 560, 220
            dipole(c, ex, ey, R, [1.5, 2.0, 2.6], 0.85, width=3.5, tilt=-11, wob=0.25, t=t, flow=True)
            earth(c, ex, ey, R, t)
            rng = random.Random(4)
            for k in range(6):
                an = rng.uniform(0, 6.28); d = R * rng.uniform(1.05, 1.6)
                x, y = ex + math.cos(an) * d, ey + math.sin(an) * d
                p = vis(t, lerp(L0, L1, 0.15 + k * 0.1))
                circle(c, x, y, 34, "#ff6b6b" if k % 2 else CYAN, p * 0.9)
                text(c, "N" if k % 2 else "S", x, y, 40, "#0b1030", p, w=900)
            C(c, "HUNDREDS TO THOUSANDS OF YEARS", 960, 90, vis(t, 0.2), ts, size=30, dot=ACCENT)
            C(c, "WEAKER FIELD · EXTRA POLES", 960, 1010, vis(t, lerp(L0, L1, 0.5)), ts, size=30, dot="#ff6b6b")
        elif mode == "effects":
            p1, p2, p3 = (vis(t, lerp(L0, L1, f)) for f in (0.0, 0.3, 0.62))
            compass(c, 380, 520, 200, 90 * math.sin(t * 2.3) + 60 * math.sin(t * 0.9), a=p1)
            T(c, "?", 380, 790, 80, ts, "#ff6b6b", p1)
            satellite(c, 960, 500, 170, a=p2, hitp=(t * 1.2) % 1)
            for k in range(8):
                q = (t * 0.8 + k / 8) % 1
                line(c, 960 - 300 + k * 70, 150 + q * 260, 960 - 320 + k * 70, 100 + q * 260, "#ff9a4a", 4, p2 * math.sin(q * math.pi))
            c.save(); c.clipRect(skia.Rect.MakeXYWH(1300, 260, 520, 560))
            rect(c, 1300, 260, 520, 560, "#03101c", p3)
            aurora_curtain(c, 1300, 1820, 640, 340, t, p3, seed=4)
            cityline(c, 1300, 1820, 820, 0.8, a=p3, seed=3)
            c.restore()
            rrect(c, 1300, 260, 520, 560, 20, "#ffffff", 0.4 * p3, stroke=3)
            T(c, "CONFUSED", 380, 900, 34, ts, "#ffffff", p1)
            T(c, "RADIATION", 960, 900, 34, ts, "#ffffff", p2)
            T(c, "AURORAS", 1560, 900, 34, ts, "#ffffff", p3)
        elif mode == "life":
            vrect(c, -1, 700, "#0b2e3a", "#1d5a6a"); vrect(c, 700, VH + 2, "#6b5a3a", "#3a2e1e")
            ammonite(c, 330, 860, 160)
            small_mammal(c, 820, 700, 150, colr="#8a6a5a"); small_mammal(c, 1120, 700, 110, colr="#a07a5a")
            bird(c, 980, 380, 80, t, "#e8eef8"); bird(c, 1150, 300, 60, t + 1, "#e8eef8")
            sauropod(c, 1560, 700, 300, colr="#2e4a3a", t=t)
            C(c, "NO MASS EXTINCTIONS FROM FLIPS", 960, 90, vis(t, lerp(L0, L1, 0.25)), ts, size=30, dot="#4cd964")
    kit.hook(c, W, H, t, S)

# ------------------------------------------------------------------ m_clouds (Short)
def big_cloud(c, x, y, s, a=1.0, colr="#ffffff"):
    for dx, dy, r in [(-0.55, 0.15, 0.38), (-0.15, -0.2, 0.52), (0.35, -0.05, 0.44), (0.72, 0.18, 0.3), (0.1, 0.2, 0.4)]:
        circle(c, x + dx * s, y + dy * s, r * s, colr, a)
    circle(c, x - 0.1 * s, y + 0.35 * s, 0.5 * s, "#000000", 0.0)

def m_clouds(c, W, H, t, S):
    mode = S.opts.get("mode", "globe"); L0 = S.lt(0, 0); L1 = S.lt(0, 1)
    if mode in ("globe",):
        bg_space(c, W, H, t, S, seed=38)
    elif mode == "night":
        fill_bg(c, W, H, "#020614", "#0b1a3a"); stars(c, W, H, t, 1.0, seed=39)
    else:
        fill_bg(c, W, H, "#4aa8ff", "#c4e8ff")
    with Stage(c, S) as ts:
        if mode == "globe":
            gx, gy, R = 960, 560, 400
            earth(c, gx, gy, R, t, spin=4)
            gone = eout(prog(t, lerp(L0, L1, 0.55), 1.5))
            rng = random.Random(6)
            c.save(); pth = skia.Path(); pth.addCircle(gx, gy, R); c.clipPath(pth, doAntiAlias=True)
            for k in range(70):
                an = rng.uniform(0, 6.28); d = R * rng.random() ** 0.6
                x = gx + math.cos(an) * d + ((t * 12) % 60); y = gy + math.sin(an) * d * 0.9
                circle(c, x, y, R * rng.uniform(0.06, 0.16), "#ffffff", 0.7 * (1 - gone), blur=R * 0.025)
            c.restore()
            C(c, "~67% COVERED ON A TYPICAL DAY", 960, 60, vis(t, lerp(L0, L1, 0.1), lerp(L0, L1, 0.55)), ts, size=32, dot="#ffffff")
            C(c, "0%", 960, 60, vis(t, lerp(L0, L1, 0.62)), ts, size=40, bg="#5a1520")
        elif mode == "rain":
            vrect(c, 860, VH + 2, "#6b8f3a", "#3a5a20")
            stop = prog(t, lerp(L0, L1, 0.6), 0.8)
            raindrops(c, 520, 1400, 520, 860, t, 1 - stop, n=60)
            big_cloud(c, 960, 340, 440, 1 - stop * 0.9, "#e8eef5")
            C(c, "≈ 500 TONNES OF WATER", 960, 60, vis(t, lerp(L0, L1, 0.15)), ts, size=36, dot="#9fd3ff")
            C(c, "NO CLOUDS = NO RAIN", 960, 1010, vis(t, lerp(L0, L1, 0.65)), ts, size=34, bg="#5a1520")
        elif mode == "day":
            vrect(c, 860, VH + 2, "#d8b07a", "#a8804a")
            sun(c, 330, 230, 170, t)
            for k in range(6):
                q = (t * 0.6 + k / 6) % 1; x0 = 420 + k * 70; y0 = 280 + k * 20
                arrow(c, x0 + q * 500, y0 + q * 560, x0 + q * 500 + 80, y0 + q * 560 + 90, ACCENT, 16, math.sin(q * math.pi))
            thermo(c, 1450, 480, 640, lerp(28, 38, eout(prog(t, L0, L1 - L0))), size=1.4)
            C(c, "CLOUDS COOL EARTH: NET ~20 W/M²", 900, 1010, vis(t, lerp(L0, L1, 0.45)), ts, size=30, dot="#ffffff")
        elif mode == "night":
            vrect(c, 820, VH + 2, "#1a1410", "#0a0806")
            for k, (x, h) in enumerate(((200, 260), (520, 200), (1700, 240))):
                c.drawPath(poly([(x - h, 820), (x, 820 - h * 0.7), (x + h, 820)]), paint("#2a1e16"))
            for x in (900, 1150):
                rect(c, x - 14, 640, 28, 180, "#1f3a20"); rect(c, x - 60, 690, 50, 18, "#1f3a20"); rect(c, x - 60, 640, 18, 60, "#1f3a20")
            moon(c, 1600, 180, 70)
            for k in range(4):
                q = (t * 0.4 + k / 4) % 1
                arrow(c, 600 + k * 120, 760 - q * 600, 600 + k * 120, 700 - q * 600, "#ff9a4a", 8, math.sin(q * math.pi) * 0.8)
            thermo(c, 1400, 470, 600, lerp(32, 12, eout(prog(t, L0, L1 - L0))), size=1.4)
            C(c, "NO BLANKET: HEAT ESCAPES", 700, 60, vis(t, lerp(L0, L1, 0.15)), ts, size=30, dot="#ff9a4a")
            C(c, "~20 °C DROP", 960, 1010, vis(t, lerp(L0, L1, 0.55)), ts, size=40, bg="#0d3a44")
        elif mode == "end":
            vrect(c, 760, VH + 2, "#c9a46a", "#8a6a3a")
            sun(c, 960, 200, 150, t)
            for k, x in enumerate((230, 560, 890)):
                solar_panel(c, x, 820, 180, glint=0.5 + 0.5 * math.sin(t * 3 + k))
            cracked_ground(c, 1080, 1900, 760, 1080)
            for x in (1250, 1450, 1650):
                line(c, x, 820, x - 20, 700, "#9a8a4a", 8); line(c, x - 10, 760, x - 50, 720, "#9a8a4a", 6)
            C(c, "SOLAR PANELS: LOVE IT", 520, 1000, vis(t, lerp(L0, L1, 0.05)), ts, size=30, dot="#4cd964")
            C(c, "FARMERS: NOT SO MUCH", 1490, 1000, vis(t, lerp(L0, L1, 0.3)), ts, size=30, dot="#ff4d4d")
    kit.hook(c, W, H, t, S)

SCENES = {k: v for k, v in globals().items() if k.startswith("m_") and callable(v)}
