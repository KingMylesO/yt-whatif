"""Drawing helpers (skia) shared by all scenes."""
import math, random
from functools import lru_cache
import skia

# ---------- math ----------
def clamp(x, a=0.0, b=1.0): return a if x < a else (b if x > b else x)
def lerp(a, b, t): return a + (b - a) * t
def ease(t): t = clamp(t); return t * t * (3 - 2 * t)
def eout(t): t = clamp(t); return 1 - (1 - t) ** 3
def ein(t): t = clamp(t); return t ** 3
def eback(t):
    t = clamp(t); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2
def prog(t, t0, d): return clamp((t - t0) / d) if d > 0 else float(t >= t0)

# ---------- colour ----------
def rgb(h):
    if isinstance(h, tuple): return h
    h = h.lstrip("#")
    if len(h) == 3: h = "".join(ch * 2 for ch in h)
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
def mix(a, b, t):
    a, b = rgb(a), rgb(b); t = clamp(t)
    return tuple(int(round(lerp(a[i], b[i], t))) for i in range(3))
def col(h, a=1.0):
    r, g, b = rgb(h); return skia.Color(r, g, b, int(255 * clamp(a)))

ACCENT = "#FFC93C"
NAVY_T, NAVY_B = "#060a1d", "#141b42"

def paint(c="#ffffff", a=1.0, stroke=0, blur=0, shader=None, dash=None, cap="round"):
    p = skia.Paint(AntiAlias=True, Color=col(c, a))
    if stroke:
        p.setStyle(skia.Paint.kStroke_Style); p.setStrokeWidth(stroke)
        p.setStrokeCap(skia.Paint.kRound_Cap if cap == "round" else skia.Paint.kButt_Cap)
        p.setStrokeJoin(skia.Paint.kRound_Join)
    if blur: p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    if shader is not None:
        p.setShader(shader); p.setColor(col("#ffffff", 1)); p.setAlphaf(clamp(a))
    if dash: p.setPathEffect(skia.DashPathEffect.Make(list(dash[0]), dash[1]))
    return p

def lin(x0, y0, x1, y1, stops):
    return skia.GradientShader.MakeLinear([skia.Point(x0, y0), skia.Point(x1, y1)],
                                          [col(c, a) for _, c, a in stops], [p for p, _, _ in stops])
def rad(cx, cy, r, stops):
    return skia.GradientShader.MakeRadial(skia.Point(cx, cy), max(r, 0.01),
                                          [col(c, a) for _, c, a in stops], [p for p, _, _ in stops])

def fill_bg(c, W, H, top, bot):
    c.drawPaint(paint(shader=lin(0, 0, 0, H, [(0, top, 1), (1, bot, 1)])))

def circle(c, x, y, r, color, a=1.0, **kw): c.drawCircle(x, y, max(r, 0), paint(color, a, **kw))
def rrect(c, x, y, w, h, r, color, a=1.0, **kw):
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r), paint(color, a, **kw))
def rect(c, x, y, w, h, color, a=1.0, **kw): c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), paint(color, a, **kw))
def line(c, x0, y0, x1, y1, color, w, a=1.0, **kw): c.drawLine(x0, y0, x1, y1, paint(color, a, stroke=w, **kw))
def poly(pts, close=True):
    p = skia.Path(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    if close: p.close()
    return p
def oval(c, x, y, rx, ry, color, a=1.0, **kw):
    c.drawOval(skia.Rect.MakeLTRB(x - rx, y - ry, x + rx, y + ry), paint(color, a, **kw))

# ---------- text ----------
_tf = {}
def font(size, w=800, fam="Inter Display"):
    k = (fam, w)
    if k not in _tf:
        _tf[k] = skia.Typeface(fam, skia.FontStyle(w, skia.FontStyle.kNormal_Width, skia.FontStyle.kUpright_Slant))
    f = skia.Font(_tf[k], size); f.setEdging(skia.Font.Edging.kAntiAlias); f.setSubpixel(True)
    return f

def tw(s, size, w=800, fam="Inter Display"): return font(size, w, fam).measureText(s)

def fit(s, maxw, size, w=800, fam="Inter Display"):
    while size > 10 and tw(s, size, w, fam) > maxw: size *= 0.95
    return size

def text(c, s, x, y, size, color="#ffffff", a=1.0, w=800, fam="Inter Display", align="c",
         stroke=0, stroke_col="#000000", shadow=0):
    if a <= 0: return 0
    f = font(size, w, fam); width = f.measureText(s)
    x0 = x - width / 2 if align == "c" else (x - width if align == "r" else x)
    yb = y + size * 0.36
    if shadow: c.drawString(s, x0, yb + shadow * 0.5, f, paint("#000000", a * 0.5, blur=shadow))
    if stroke: c.drawString(s, x0, yb, f, paint(stroke_col, a, stroke=stroke))
    c.drawString(s, x0, yb, f, paint(color, a))
    return width

def chip(c, s, x, y, p, size=34, bg="#0b1030", fg="#ffffff", a=0.88, dot=None, align="c"):
    """Rounded label that pops in with progress p (0..1)."""
    if p <= 0: return
    size *= 1.15
    al = eout(p * 1.6); sc = lerp(0.8, 1.0, eback(p))
    f = font(size, 700, "Inter"); w_ = f.measureText(s); pad = size * 0.62; h = size * 1.75
    extra = size * 0.9 if dot else 0
    w = w_ + 2 * pad + extra
    ox = 0 if align == "c" else (w / 2 if align == "l" else -w / 2)
    c.save(); c.translate(x + ox, y); c.scale(sc, sc)
    rrect(c, -w / 2, -h / 2, w, h, h / 2, bg, a * al)
    rrect(c, -w / 2, -h / 2, w, h, h / 2, "#ffffff", 0.12 * al, stroke=2)
    if dot: circle(c, -w / 2 + pad + size * 0.25, 0, size * 0.25, dot, al)
    text(c, s, extra / 2, 0, size, fg, al, w=700, fam="Inter")
    c.restore()

# ---------- stars ----------
@lru_cache(maxsize=16)
def star_image(W, H, seed=1, density=1.0):
    surf = skia.Surface(W, H); c = surf.getCanvas(); c.clear(skia.ColorTRANSPARENT)
    rng = random.Random(seed); n = int(W * H / 2400 * density)
    for _ in range(n):
        x, y = rng.random() * W, rng.random() * H
        r = 0.5 + rng.random() ** 4 * 2.0
        tint = rng.choice(["#ffffff", "#ffffff", "#cfe0ff", "#fff1d0"])
        c.drawCircle(x, y, r, paint(tint, rng.uniform(0.25, 0.95)))
    for _ in range(int(n / 60)):
        x, y = rng.random() * W, rng.random() * H
        c.drawCircle(x, y, 7, paint("#bcd4ff", 0.18, blur=5)); c.drawCircle(x, y, 1.9, paint("#ffffff", 1))
    return surf.makeImageSnapshot()

def stars(c, W, H, t, a=1.0, seed=1, drift=(0.0, 0.0), density=1.0, twinkle=True):
    if a <= 0.01: return
    img = star_image(W, H, seed, density)
    p = skia.Paint(); p.setAlphaf(clamp(a))
    dx = (drift[0] * t) % W; dy = (drift[1] * t) % H
    for ox in (dx - W, dx):
        for oy in (dy - H, dy):
            c.drawImage(img, ox, oy, skia.SamplingOptions(), p)
    if twinkle:
        rng = random.Random(seed + 99)
        for i in range(18):
            x, y = rng.random() * W, rng.random() * H
            ph = rng.random() * 6.28; sp = rng.uniform(1.5, 3.5)
            al = a * (0.5 + 0.5 * math.sin(t * sp + ph))
            circle(c, (x + dx) % W, (y + dy) % H, 1.8, "#ffffff", al)

def space_bg(c, W, H, t, a_stars=1.0, seed=1, drift=(0, 0), top=NAVY_T, bot=NAVY_B):
    fill_bg(c, W, H, top, bot)
    stars(c, W, H, t, a_stars, seed, drift)

# ---------- sun / moon ----------
def sun(c, x, y, r, t, a=1.0, glow=1.0):
    if a <= 0 or r <= 0: return
    c.drawCircle(x, y, r * 3.4, paint(shader=rad(x, y, r * 3.4, [(0, "#ffd166", 0.55 * glow), (0.3, "#ff9f1c", 0.2 * glow), (1, "#ff6b35", 0)]), a=a))
    c.save(); c.translate(x, y); c.rotate(t * 4)
    for i in range(14):
        c.rotate(360 / 14)
        L = r * (1.5 + 0.12 * math.sin(t * 2 + i))
        c.drawPath(poly([(-r * 0.12, 0), (0, -L), (r * 0.12, 0)]), paint("#ffd166", 0.22 * a))
    c.restore()
    c.drawCircle(x, y, r, paint(shader=rad(x - r * 0.3, y - r * 0.35, r * 1.5, [(0, "#fffbe0", 1), (0.45, "#ffd23f", 1), (1, "#ff9f1c", 1)]), a=a))

def ghost_ring(c, x, y, r, t, a=1.0, color="#ffd166"):
    if a <= 0: return
    c.drawCircle(x, y, r, paint(color, 0.7 * a, stroke=max(2, r * 0.035), dash=([r * 0.18, r * 0.14], -t * 30)))

def sun_vanish(c, x, y, r, t, tv, ghost=False):
    """Sun until tv, then a quick implosion + flash; optional ghost outline."""
    if t < tv:
        sun(c, x, y, r, t); return
    q = t - tv
    if q < 0.16:
        s = 1 + 0.12 * math.sin(q / 0.16 * math.pi) - q / 0.16
        sun(c, x, y, r * max(s, 0), t, a=1 - q / 0.2)
    fl = clamp(1 - q / 0.7)
    if fl > 0:
        circle(c, x, y, r * (1 + q * 5), "#fff4cc", fl * 0.9, stroke=r * 0.12 * fl + 1)
        circle(c, x, y, r * 2.2, "#ffffff", fl * 0.35, blur=r * 0.6)
    if ghost: ghost_ring(c, x, y, r, t, eout((q - 0.3) / 0.8))

def moon(c, x, y, r, lit=1.0, a=1.0):
    if a <= 0: return
    base = mix("#20263b", "#d9dbe3", lit)
    circle(c, x, y, r * 1.8, "#cfd8ff", 0.12 * lit * a, blur=r * 0.5)
    circle(c, x, y, r, base, a)
    rng = random.Random(7)
    for _ in range(9):
        ang = rng.random() * 6.28; d = rng.random() ** 0.7 * r * 0.72; cr = r * rng.uniform(0.07, 0.2)
        circle(c, x + math.cos(ang) * d, y + math.sin(ang) * d, cr, mix("#151a2a", "#b3b6c4", lit), a)
    c.drawCircle(x, y, r, paint(shader=rad(x - r * 0.4, y - r * 0.4, r * 1.6, [(0, "#ffffff", 0.18 * lit), (1, "#000000", 0.35)]), a=a))

# ---------- earth ----------
@lru_cache(maxsize=1)
def land_blobs():
    rng = random.Random(11); blobs = []
    conts = [(-100, 45, 26, 16), (-60, -15, 20, 13), (15, 8, 26, 14), (20, 52, 16, 12), (95, 45, 30, 20),
             (135, -25, 12, 9), (-40, 72, 8, 8), (110, 5, 8, 10)]
    for clon, clat, n, sp in conts:
        for _ in range(n):
            blobs.append((clon + rng.gauss(0, sp), clamp(clat + rng.gauss(0, sp * 0.7), -70, 78), rng.uniform(6, 12)))
    cities = [(b[0] + rng.uniform(-4, 4), b[1] + rng.uniform(-4, 4)) for b in blobs for _ in range(2)]
    cloudb = [(rng.uniform(-180, 180), rng.uniform(-60, 60), rng.uniform(6, 14)) for _ in range(40)]
    return blobs, cities, cloudb

def _proj(lon, lat, rot, tilt=12):
    lo = math.radians(lon + rot); la = math.radians(lat)
    X = math.cos(la) * math.sin(lo); Y = math.sin(la); Z = math.cos(la) * math.cos(lo)
    tr = math.radians(tilt)
    Y2 = Y * math.cos(tr) - Z * math.sin(tr); Z2 = Y * math.sin(tr) + Z * math.cos(tr)
    return X, Y2, Z2

def earth(c, x, y, R, rot=0.0, day=1.0, night_side=True, ice=0.0, lights=0.0, sun_dir=-1, clouds=True,
          a=1.0, glow=1.0, starlight=0.0):
    """day: 1 = lit hemisphere bright, 0 = whole planet dark. ice: 0..1 freeze."""
    if a <= 0: return
    blobs, cities, cloudb = land_blobs()
    # atmosphere glow
    circle(c, x, y, R * 1.12, mix("#5aa9ff", "#9fb8d9", ice), 0.35 * glow * a * max(day, 0.15), blur=R * 0.08)
    c.save()
    pth = skia.Path(); pth.addCircle(x, y, R); c.clipPath(pth, doAntiAlias=True)
    ocean = mix(mix("#1f6fd1", "#bcd7ee", ice * 0.85), "#0a1220", 0)
    circle(c, x, y, R, ocean, a)
    landc = mix(mix("#38b26a", "#e9f3fb", ice), "#3b8f4a", 0)
    for lon, lat, r in blobs:
        X, Y, Z = _proj(lon, lat, rot)
        if Z > -0.15:
            rr = R * math.radians(r) * (0.55 + 0.45 * max(Z, 0))
            circle(c, x + X * R, y - Y * R, rr, landc, a)
    # polar caps
    for lat0 in (90, -90):
        X, Y, Z = _proj(0, lat0, rot)
        rx = R * math.sin(math.radians(min(80, 18 + 45 * ice)))
        oval(c, x + X * R, y - Y * R, rx, rx * 0.42, "#f4f9ff", a)
    if clouds and ice < 0.95:
        for lon, lat, r in cloudb:
            X, Y, Z = _proj(lon, lat, rot * 1.3 + 20)
            if Z > 0:
                circle(c, x + X * R, y - Y * R, R * math.radians(r) * 0.55 * (0.5 + 0.5 * Z), "#ffffff", 0.4 * a * (1 - ice))
    # sphere shading
    lx = x + sun_dir * R * 0.45
    c.drawCircle(x, y, R, paint(shader=rad(lx, y - R * 0.3, R * 2.0, [(0, "#ffffff", 0.18), (0.5, "#000000", 0.0), (1, "#000000", 0.45)]), a=a))
    # terminator
    if night_side:
        x0 = x + sun_dir * R; x1 = x - sun_dir * R
        c.drawCircle(x, y, R, paint(shader=lin(x0, y, x1, y, [(0, "#020510", 0), (0.46, "#020510", 0), (0.58, "#020510", 0.88), (1, "#020510", 0.94)]), a=a))
    dark = 1 - day
    if dark > 0:
        circle(c, x, y, R, mix("#020510", "#0b1a3c", ice), 0.92 * dark * a)
    if starlight > 0:  # faint rim so a dark Earth is still readable
        c.drawCircle(x, y, R, paint(shader=rad(x, y, R, [(0.7, "#9fb8ff", 0), (1, "#9fb8ff", 0.25 * starlight)]), a=a))
    if lights > 0:
        for lon, lat in cities:
            X, Y, Z = _proj(lon, lat, rot)
            if Z > 0.05:
                side = clamp((-sun_dir * X + 0.05) * 6) if night_side else 0
                al = lights * max(side, dark) * a
                if al > 0.02:
                    circle(c, x + X * R, y - Y * R, R * 0.012 + 0.6, "#ffcf6e", al)
                    circle(c, x + X * R, y - Y * R, R * 0.03, "#ffb347", al * 0.25, blur=2)
    c.restore()
    circle(c, x, y, R, mix("#8cc8ff", "#cfe3ff", ice), 0.35 * a * max(day, 0.2), stroke=max(1.5, R * 0.012))

# ---------- landscape bits ----------
def hills(c, W, y0, amp, color, seed, a=1.0, H=None, freq=1.0):
    H = H or y0 + 4000
    rng = random.Random(seed); ph = [rng.random() * 6.28 for _ in range(3)]
    pts = []
    for i in range(0, 41):
        x = W * i / 40
        yy = y0 - amp * (0.55 * math.sin(x / W * 6.28 * freq + ph[0]) + 0.3 * math.sin(x / W * 15 * freq + ph[1]) + 0.15 * math.sin(x / W * 31 + ph[2]))
        pts.append((x, yy))
    pts += [(W, H), (0, H)]
    c.drawPath(poly(pts), paint(color, a))

def tree(c, x, y, h, leaf="#2e9e5b", trunk="#6b4a2f", a=1.0):
    rect(c, x - h * 0.05, y - h * 0.45, h * 0.1, h * 0.45, trunk, a)
    circle(c, x, y - h * 0.62, h * 0.28, leaf, a)
    circle(c, x - h * 0.2, y - h * 0.5, h * 0.2, leaf, a)
    circle(c, x + h * 0.2, y - h * 0.52, h * 0.21, leaf, a)
    circle(c, x - h * 0.08, y - h * 0.72, h * 0.12, mix(leaf, "#ffffff", 0.18), a * 0.7)

def pine(c, x, y, h, color, a=1.0):
    c.drawPath(poly([(x, y - h), (x - h * 0.28, y - h * 0.15), (x + h * 0.28, y - h * 0.15)]), paint(color, a))
    rect(c, x - h * 0.04, y - h * 0.16, h * 0.08, h * 0.16, mix(color, "#000000", 0.4), a)

def cloud(c, x, y, s, color="#ffffff", a=1.0):
    for dx, dy, r in [(-0.5, 0.1, 0.35), (-0.1, -0.15, 0.48), (0.35, 0.0, 0.4), (0.7, 0.15, 0.28)]:
        circle(c, x + dx * s, y + dy * s, r * s, color, a)
    rrect(c, x - 0.85 * s, y + 0.05 * s, 1.8 * s, 0.38 * s, 0.19 * s, color, a)

def bird(c, x, y, s, t, color="#2a2f45", a=1.0):
    f = math.sin(t * 9) * 0.35 * s
    p = skia.Path(); p.moveTo(x - s, y - f); p.quadTo(x - s * 0.4, y - s * 0.35, x, y)
    p.quadTo(x + s * 0.4, y - s * 0.35, x + s, y - f)
    c.drawPath(p, paint(color, a, stroke=max(2, s * 0.16)))

def person(c, x, y, h, color, look_up=0.0, a=1.0, arm_up=0.0):
    """Simple silhouette standing on (x, y)."""
    bw = h * 0.26
    rrect(c, x - bw / 2, y - h * 0.78, bw, h * 0.78, bw / 2, color, a)
    hx = x + h * 0.03 * look_up; hy = y - h * 0.9 - h * 0.02 * look_up
    circle(c, hx, hy, h * 0.13, color, a)
    if arm_up > 0:
        line(c, x + bw * 0.3, y - h * 0.62, x + bw * 0.3 + h * 0.18, y - h * 0.62 - h * 0.3 * arm_up, color, h * 0.07, a)

def skyline(c, W, base, H, seed, color, win=0.0, a=1.0, win_col="#ffd27a", maxh=0.35):
    rng = random.Random(seed); x = -20
    while x < W + 20:
        bw = rng.uniform(0.04, 0.09) * max(W, H) * 0.6; bh = rng.uniform(0.12, maxh) * H
        rect(c, x, base - bh, bw, bh + 4, color, a)
        if win > 0:
            ws = bw / 7
            for wx in range(1, 6, 2):
                for wy in range(1, int(bh / (ws * 2))):
                    if rng.random() < 0.45:
                        rect(c, x + wx * ws, base - bh + wy * ws * 2, ws, ws * 1.1, win_col, a * win * rng.uniform(0.6, 1))
        x += bw + rng.uniform(2, 10)

def thermometer(c, x, y, h, temp, tmax=20, tmin=-30, a=1.0, label=True, size=1.0, unit2=None):
    w = h * 0.12
    rrect(c, x - w / 2 - 6, y - h / 2 - 6, w + 12, h + 12, (w + 12) / 2, "#ffffff", 0.9 * a)
    circle(c, x, y + h / 2 + w * 0.55, w * 1.15, "#ffffff", 0.9 * a)
    f = clamp((temp - tmin) / (tmax - tmin))
    fc = mix("#3fa7ff", "#ff4d4d", clamp((temp + 10) / 35))
    top = y + h / 2 - f * h
    rrect(c, x - w / 2 + 4, top, w - 8, y + h / 2 - top + w * 0.3, (w - 8) / 2, fc, a)
    circle(c, x, y + h / 2 + w * 0.55, w * 0.85, fc, a)
    for i in range(6):
        yy = y - h / 2 + h * i / 5
        line(c, x + w / 2 + 10, yy, x + w / 2 + 26, yy, "#ffffff", 3, 0.6 * a)
    if label:
        s = f"{'−' if temp < 0 else ''}{abs(round(temp))} °C"
        text(c, s, x + w / 2 + 40, top, 64 * size, fc if temp < 0 else "#ffffff", a, w=900, align="l", shadow=8)
        if unit2:
            text(c, unit2, x + w / 2 + 42, top + 62 * size, 34 * size, "#cfe3ff", a * 0.9, w=600, fam="Inter", align="l")
