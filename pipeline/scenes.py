"""Scenes for 'What If the Sun Vanished?' (long-form + teaser Short)."""
import math, random
import skia
from core import *

class Ctx:
    def __init__(self, dur, lines, opts, W, H):
        self.dur, self.lines, self.opts, self.W, self.H = dur, lines, opts or {}, W, H
        self.P = H > W; self.u = min(W, H) / 1080
    def ls(self, i): return self.lines[i]["start"] if i < len(self.lines) else self.dur + 99
    def le(self, i): return self.lines[i]["end"] if i < len(self.lines) else self.dur + 99
    def lt(self, i, f):
        if i >= len(self.lines): return self.dur + 99
        return self.ls(i) + f * (self.le(i) - self.ls(i))
    def n(self): return len(self.lines)

def vis(t, a, b=None, d=0.45):
    p = prog(t, a, d)
    if b is not None and t > b: p *= 1 - prog(t, b, 0.25)
    return p

def until_next(S, i):  # chip of line i hides at start of line i+1
    return S.ls(i + 1) - 0.15 if i + 1 < S.n() else None

# ======================================================= PARK
def park(c, W, H, t, S, dark=None, star_a=None):
    o = S.opts; u = S.u
    dark = o.get("dark", 0) if dark is None else dark
    gold = 0.35 if o.get("outro") else 0
    fill_bg(c, W, H, mix(mix("#4aa8ff", "#ff9e6b", gold * 0.4), "#03061a", dark),
            mix(mix("#c4e8ff", "#ffe0b0", gold), "#0e1636", dark))
    stars(c, W, H, t, dark if star_a is None else star_a, seed=4)
    sx, sy = (0.22 * W, 0.2 * H) if not S.P else (0.27 * W, 0.15 * H)
    sun(c, sx, sy, 72 * u, t, a=1 - dark, glow=0.8)
    for i in range(4):
        x = ((i * 0.31 + (0.1 if not S.P else 0.3) + t * 0.012) % 1.35 - 0.17) * W
        y = (0.1 + 0.075 * (i % 3)) * H + (0 if not S.P else 0.02 * H)
        cloud(c, x, y, 85 * u * (1 + 0.35 * (i % 2)), mix("#ffffff", "#141a33", dark), 0.95 - 0.55 * dark)
    hy = 0.6 * H
    hills(c, W, hy, 55 * u, mix("#9ad68f", "#0b1320", dark), 1, H=H)
    hills(c, W, hy + 0.07 * H, 38 * u, mix("#63c16a", "#09111b", dark), 2, H=H)
    leaf = mix("#2e9e5b", "#0a1a17", dark); trunk = mix("#6b4a2f", "#120e0c", dark)
    for fx, sc in [(0.07, 1.0), (0.19, 0.8), (0.74, 0.9), (0.9, 1.1)]:
        tree(c, fx * W, hy + 0.1 * H, (250 if not S.P else 330) * u * sc, leaf, trunk)
    hills(c, W, hy + 0.24 * H, 18 * u, mix("#48aa52", "#070e17", dark), 3, H=H)
    pc = ["#ff6b6b", "#4d96ff", "#ffd93d", "#9b5de5", "#00bbf9"]
    for i, fx in enumerate([0.32, 0.4, 0.52, 0.6, 0.67] if not S.P else [0.2, 0.36, 0.5, 0.64, 0.8]):
        colr = mix(pc[i], "#06080f", dark * 0.85)
        bob = math.sin(t * 2 + i) * 3 * u * (1 - dark)
        person(c, fx * W + math.sin(t * 0.4 + i) * 20 * u * (1 - dark), hy + 0.27 * H + bob,
               (150 if not S.P else 230) * u * (0.9 + 0.1 * (i % 2)), colr, look_up=dark, arm_up=dark * (i == 2))
    if dark < 0.5:
        for i in range(3):
            bx = ((0.3 + i * 0.07 + t * 0.035) % 1.3 - 0.1) * W
            bird(c, bx, 0.3 * H + i * 18 * u + math.sin(t + i) * 8, 16 * u, t + i, a=1 - dark * 2)
    if o.get("timer"):
        secs = lerp(440, 499, t / S.dur)
        m, s_ = divmod(int(secs), 60)
        y0 = 0.1 * H if not S.P else 0.3 * H
        chip(c, "SINCE THE SUN VANISHED", W / 2, y0, 1, 30 * u, bg="#0b1030")
        text(c, f"{m}:{s_:02d}", W / 2, y0 + 105 * u, 120 * u, "#ffffff", 1, w=900, shadow=12, stroke=0)
    if o.get("outro"):
        chip(c, "THIS LIGHT IS 8 MINUTES OLD", W / 2, 0.12 * H, vis(t, S.lt(0, 0.7), until_next(S, 0)), 36 * u)
    if o.get("hook"):
        sz = fit(o["hook"], W * 0.9, 96 * u, 900)
        text(c, o["hook"], W / 2, 0.3 * H, sz, "#ffffff", eout(t / 0.25), w=900, stroke=10 * u, stroke_col="#0b1030")

# ======================================================= TITLE + CARDS
def title(c, W, H, t, S):
    u = S.u; space_bg(c, W, H, t, 1, seed=2, drift=(-6, 0))
    tv = S.dur - 1.1
    sun_vanish(c, W / 2, 0.38 * H, 130 * u, t, tv, ghost=True)
    words1 = ["WHAT", "IF", "THE", "SUN"]
    sz = 120 * u; y1 = 0.72 * H; y2 = y1 + 135 * u
    full = " ".join(words1); x = W / 2 - tw(full, sz, 900) / 2
    for i, wd in enumerate(words1):
        p = prog(t, 0.15 + i * 0.12, 0.35)
        text(c, wd, x, y1 + (1 - eout(p)) * 30 * u, sz, "#ffffff", p, w=900, align="l", shadow=14)
        x += tw(wd + " ", sz, 900)
    p = prog(t, 0.75, 0.4)
    text(c, "VANISHED?", W / 2, y2 + (1 - eout(p)) * 30 * u, sz * 1.15, ACCENT, p, w=900, shadow=14)

def card(c, W, H, t, S):
    u = S.u; txt = S.opts["text"]
    space_bg(c, W, H, t, 0.6, seed=3, drift=(-10, 0))
    c.save(); z = 1 + 0.05 * t / S.dur; c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-W / 2, -H / 2)
    lines_ = [txt]
    big = 190 * u
    if tw(txt, big, 900) > W * 0.86 and " " in txt:
        ws = txt.split(" ")
        best = min(range(1, len(ws)), key=lambda k: max(tw(" ".join(ws[:k]), big, 900), tw(" ".join(ws[k:]), big, 900)))
        lines_ = [" ".join(ws[:best]), " ".join(ws[best:])]
    p = eout(prog(t, 0.0, 0.35))
    chip(c, "TIME SINCE THE SUN VANISHED", W / 2, H / 2 - (150 if len(lines_) == 1 else 245) * u, prog(t, 0.05, 0.4), 30 * u, bg="#1b2250")
    for k, ln in enumerate(lines_):
        sz = fit(ln, W * 0.86, big, 900)
        yy = H / 2 + (k - (len(lines_) - 1) / 2) * sz * 1.02 + (1 - p) * 40 * u
        text(c, ln, W / 2, yy, sz, "#ffffff" if k == 0 else ACCENT, p, w=900, shadow=18)
    lw = W * 0.3 * eout(prog(t, 0.2, 0.6))
    yb = H / 2 + (120 if len(lines_) == 1 else 220) * u
    line(c, W / 2 - lw / 2, yb, W / 2 + lw / 2, yb, ACCENT, 8 * u)
    c.restore()

# ======================================================= SETUP
PLANETS = [(150, 7, "#b8b0a5"), (215, 12, "#e8c27a"), (285, 13, "#3b8de0"), (360, 10, "#d9603b"),
           (520, 30, "#d8b48a"), (690, 24, "#e3cf8f")]

def solar_system(c, W, H, t, S):
    u = S.u; space_bg(c, W, H, t, 1, seed=5)
    cx, cy = W / 2, H / 2 + 30 * u; k = u * (1.0 if not S.P else 0.62)
    tv = S.lt(1, 0.32)
    for r, _, _ in PLANETS:
        c.drawOval(skia.Rect.MakeLTRB(cx - r * k, cy - r * k * 0.42, cx + r * k, cy + r * k * 0.42), paint("#ffffff", 0.18, stroke=2))
    pos = []
    for i, (r, pr, colr) in enumerate(PLANETS):
        ang = t * 2.2 / (r / 150) ** 1.5 + i * 1.7
        pos.append((cx + math.cos(ang) * r * k, cy + math.sin(ang) * r * k * 0.42, pr * k, colr, math.sin(ang), i))
    def draw_p(px, py, pr, colr, i):
        circle(c, px, py, pr, colr)
        if i == 5:
            c.drawOval(skia.Rect.MakeLTRB(px - pr * 2.1, py - pr * 0.55, px + pr * 2.1, py + pr * 0.55), paint("#f1e3b5", 0.9, stroke=pr * 0.28))
        if i == 4:
            for b in (-0.35, 0.1, 0.45): line(c, px - pr * 0.9, py + b * pr, px + pr * 0.9, py + b * pr, "#b08560", pr * 0.16, 0.8)
        c.drawCircle(px, py, pr, paint(shader=rad(px - pr * 0.4, py - pr * 0.4, pr * 1.8, [(0, "#ffffff", 0.25), (1, "#000000", 0.5)])))
    for px, py, pr, colr, z, i in pos:
        if z < 0: draw_p(px, py, pr, colr, i)
    sun_vanish(c, cx, cy, 70 * k, t, tv, ghost=False)
    for px, py, pr, colr, z, i in pos:
        if z >= 0: draw_p(px, py, pr, colr, i)
    y = 0.12 * H
    chip(c, "NOT EXPLODING", W * 0.32, y, vis(t, S.lt(0, 0.3), S.ls(1)), 34 * u, dot="#ff4d4d")
    chip(c, "NOT BURNING OUT", W * 0.68, y, vis(t, S.lt(0, 0.62), S.ls(1)), 34 * u, dot="#ff4d4d")
    chip(c, "JUST… GONE", W / 2, 0.88 * H, vis(t, tv + 0.2), 44 * u, bg="#1b2250")

def impossible(c, W, H, t, S):
    u = S.u; space_bg(c, W, H, t, 1, seed=6)
    cx, cy = W / 2, H / 2 - 20 * u
    ghost_ring(c, cx, cy, 190 * u, t, 1)
    text(c, "?", cx, cy + math.sin(t * 2) * 8 * u, 240 * u, ACCENT, 1, w=900)
    p = prog(t, S.lt(0, 0.12), 0.25)
    if p > 0:
        sc = lerp(1.8, 1.0, eout(p))
        c.save(); c.translate(cx, cy + 60 * u); c.rotate(-12); c.scale(sc, sc)
        wdt = tw("IMPOSSIBLE", 120 * u, 900) + 60 * u
        rrect(c, -wdt / 2, -85 * u, wdt, 170 * u, 18 * u, "#ff4d4d", eout(p), stroke=10 * u)
        text(c, "IMPOSSIBLE", 0, 0, 120 * u, "#ff4d4d", eout(p), w=900)
        c.restore()
    chip(c, "MASS CAN'T JUST VANISH", W / 2, 0.86 * H, vis(t, S.lt(0, 0.55)), 38 * u)

def distance(c, W, H, t, S):
    u = S.u; space_bg(c, W, H, t, 1, seed=7)
    sx, ex, y = 0.1 * W, 0.86 * W, 0.47 * H
    sun(c, sx, y, 190 * u, t)
    earth(c, ex, y, 52 * u, rot=t * 8, sun_dir=-1)
    chip(c, "YOU ARE HERE", ex, y + 120 * u, vis(t, S.lt(0, 0.35)), 28 * u)
    p = ease(prog(t, S.lt(0, 0.55), 1.6))
    if p > 0:
        x0 = sx + 230 * u; x1 = lerp(x0, ex - 80 * u, p); yy = 0.72 * H
        line(c, x0, yy, x1, yy, "#ffffff", 5 * u, 0.9)
        line(c, x0, yy - 22 * u, x0, yy + 22 * u, "#ffffff", 5 * u, 0.9)
        if p >= 1: line(c, x1, yy - 22 * u, x1, yy + 22 * u, "#ffffff", 5 * u, 0.9)
        val = int(150_000_000 * p / 1e6) * 1_000_000
        text(c, f"{val:,} km", (x0 + x1) / 2, yy - 70 * u, 64 * u, ACCENT, 1, w=900, shadow=10)

def stopwatch(c, W, H, t, S):
    u = S.u; space_bg(c, W, H, t, 0.7, seed=8)
    cx, cy, r = W / 2, H / 2, 230 * u
    p = eout(prog(t, 0, 0.4)); c.save(); c.translate(cx, cy); c.scale(p, p)
    rrect(c, -35 * u, -r - 70 * u, 70 * u, 50 * u, 10 * u, "#d7dbe8")
    circle(c, 0, 0, r + 22 * u, "#d7dbe8"); circle(c, 0, 0, r, "#0d1330")
    for i in range(60):
        a = math.radians(i * 6); L = 26 * u if i % 5 == 0 else 12 * u
        line(c, math.sin(a) * (r - 14 * u), -math.cos(a) * (r - 14 * u), math.sin(a) * (r - 14 * u - L), -math.cos(a) * (r - 14 * u - L), "#ffffff", 4 * u if i % 5 == 0 else 2 * u, 0.8)
    ang = math.radians(max(0, t - S.lt(0, 0.6)) * 360 / 2.5 * 6)
    line(c, 0, 0, math.sin(ang) * (r - 45 * u), -math.cos(ang) * (r - 45 * u), ACCENT, 9 * u)
    circle(c, 0, 0, 16 * u, ACCENT)
    c.restore()

# ======================================================= 0 - 8 MIN
def _two_pos(W, H, S, far=False):
    if S.P: return (W / 2, 0.24 * H), (W / 2, 0.74 * H)
    return (0.2 * W, 0.5 * H), (0.8 * W, 0.5 * H)

def sun_blink(c, W, H, t, S):
    u = S.u; space_bg(c, W, H, t, 1, seed=9)
    (sx, sy), (ex, ey) = _two_pos(W, H, S)
    tv = 0.55
    f = 0.0 if t < tv else 0.12 * (t - tv) / S.dur
    _beam(c, sx, sy, ex, ey, f, t, u, 70 * u)
    sun_vanish(c, sx, sy, 150 * u, t, tv, ghost=True)
    earth(c, ex, ey, 120 * u, rot=t * 6, sun_dir=-1 if not S.P else -1)
    chip(c, "STILL DAYLIGHT", ex, ey + (200 if not S.P else 190) * u, vis(t, S.lt(0, 0.6)), 34 * u)

def _beam(c, sx, sy, ex, ey, f, t, u, width):
    """Light already in flight: from tail (fraction f of the way) to Earth."""
    tx, ty = lerp(sx, ex, f), lerp(sy, ey, f)
    bp = paint(shader=lin(tx, ty, ex, ey, [(0, "#ffb627", 0.1), (0.12, "#ffcf5a", 0.55), (1, "#ffe9a8", 0.75)]), stroke=width, cap="butt")
    bp.setBlendMode(skia.BlendMode.kPlus); c.drawLine(tx, ty, ex, ey, bp)
    gp = paint(shader=lin(tx, ty, ex, ey, [(0, "#ffb627", 0.0), (0.2, "#ffb627", 0.25), (1, "#ffb627", 0.3)]), stroke=width * 2.2, cap="butt", blur=width * 0.4)
    gp.setBlendMode(skia.BlendMode.kPlus); c.drawLine(tx, ty, ex, ey, gp)
    L = math.hypot(ex - ex + (ex - sx), ey - sy) + 1e-6
    dx, dy = (ex - sx) / L, (ey - sy) / L
    rng = random.Random(3)
    for i in range(40):
        ph = rng.random(); off = rng.uniform(-0.35, 0.35) * width
        q = (ph + t * 0.35) % 1.0
        if q < f: continue
        px, py = lerp(sx, ex, q) - dy * off, lerp(sy, ey, q) + dx * off
        line(c, px, py, px + dx * 26 * u, py + dy * 26 * u, "#fff4cc", 4 * u, 0.85)

def light_beam(c, W, H, t, S):
    u = S.u; space_bg(c, W, H, t, 1, seed=10)
    (sx, sy), (ex, ey) = _two_pos(W, H, S)
    f = 0.06 + 0.86 * t / S.dur
    _beam(c, sx, sy, ex, ey, f, t, u, 80 * u)
    ghost_ring(c, sx, sy, 150 * u, t, 1)
    earth(c, ex, ey, 120 * u, rot=t * 6, sun_dir=-1)
    tx, ty = lerp(sx, ex, f), lerp(sy, ey, f)
    line(c, tx, ty - 70 * u, tx, ty + 70 * u, "#ffffff", 3 * u, 0.6, dash=([10, 8], 0))
    secs = int(500 * f); m, s_ = divmod(secs, 60)
    yt = 0.13 * H if not S.P else 0.5 * H
    xt = W / 2 if not S.P else W * 0.72
    chip(c, "LIGHT TRAVEL TIME", xt, yt - 70 * u, 1, 28 * u)
    text(c, f"{m}:{s_:02d}", xt, yt + 30 * u, 110 * u, ACCENT, 1, w=900, shadow=12)
    if not S.P:
        chip(c, "THE LIGHT YOU SEE IS 8 MINUTES OLD", W / 2, 0.86 * H, vis(t, S.lt(1, 0.3), until_next(S, 1)), 34 * u)
        chip(c, "ALREADY ON ITS WAY", W / 2, 0.86 * H, vis(t, S.lt(2, 0.55)), 34 * u)

def ghost_orbit(c, W, H, t, S):
    u = S.u; space_bg(c, W, H, t, 1, seed=11)
    cx, cy = W / 2, H / 2; Ro = 360 * u if not S.P else 380 * u
    ghost_ring(c, cx, cy, 80 * u, t, 1)
    circle(c, cx, cy, Ro, "#ffffff", 0.25, stroke=2.5 * u, dash=([14, 12], 0))
    # gravity news ripple, never quite reaching the orbit in this scene
    rr = Ro * 0.92 * t / S.dur
    for k in range(3):
        r_ = rr - k * 40 * u
        if r_ > 80 * u: circle(c, cx, cy, r_, "#9fd3ff", 0.5 / (k + 1), stroke=5 * u - k * u)
    th = -0.9 + t * 0.32
    ex, ey = cx + math.cos(th) * Ro, cy + math.sin(th) * Ro
    # trail
    p = skia.Path(); p.addArc(skia.Rect.MakeLTRB(cx - Ro, cy - Ro, cx + Ro, cy + Ro), math.degrees(th) - 50, 50)
    c.drawPath(p, paint(shader=rad(ex, ey, Ro * 0.9, [(0, "#8fd0ff", 0.9), (1, "#8fd0ff", 0)]), stroke=6 * u))
    c.save(); c.translate(ex, ey); c.rotate(math.degrees(math.atan2(cy - ey, cx - ex)) + 180)
    earth(c, 0, 0, 46 * u, rot=t * 20, sun_dir=-1, clouds=False)
    c.restore()
    if S.n() > 1 or S.P:
        chip(c, "GRAVITY TRAVELS AT LIGHT SPEED", W / 2, 0.1 * H if not S.P else 0.18 * H, vis(t, S.lt(0, 0.6), until_next(S, 0)), 32 * u, dot="#9fd3ff")
    chip(c, "ORBITING A GHOST", W / 2, 0.9 * H if not S.P else 0.82 * H, vis(t, S.lt(min(1, S.n() - 1), 0.55)), 36 * u, bg="#1b2250")

# ======================================================= LIGHTS OUT
def lights_out(c, W, H, t, S):
    u = S.u
    if S.n() > 1 and t >= S.ls(1):
        ps = prog(t, S.ls(1), 3.0)
        park(c, W, H, t, S, dark=1.0, star_a=ease(ps))
        chip(c, "3:00 PM", W / 2, 0.1 * H, vis(t, S.ls(1) + 0.3), 36 * u, dot="#ffd166")
        return
    space_bg(c, W, H, t, 1, seed=12)
    ts = S.lt(0, 0.55 if S.opts.get("short_switch") else 0.86)
    on = t < ts
    R = 300 * u if not S.P else 400 * u
    earth(c, W / 2, H / 2, R, rot=t * 5, day=1.0 if on else 0.0, lights=1.0, sun_dir=-1)
    if not on:
        chip(c, "LIGHTS OUT", W / 2, H / 2 + R + 90 * u, vis(t, ts + 0.15), 44 * u, bg="#1b2250")

def moon_fade(c, W, H, t, S):
    u = S.u
    fill_bg(c, W, H, "#03061a", "#0e1636"); stars(c, W, H, t, 1, seed=13)
    tf = S.lt(0, 0.55); lit = 1 - ease(prog(t, tf, 0.35))
    mx, my, r = W / 2, (0.4 if not S.P else 0.38) * H, 150 * u
    moon(c, mx, my, r, lit=lit)
    if lit < 1: ghost_ring(c, mx, my, r * 1.04, t, (1 - lit) * 0.5, color="#9aa4c4")
    hills(c, W, 0.83 * H, 40 * u, "#05080f", 21, H=H)
    if S.n() > 1:
        chip(c, "STILL THERE. JUST DARK.", W / 2, my + r + 110 * u, vis(t, S.lt(1, 0.55)), 38 * u)
    else:
        chip(c, "GONE", W / 2, my + r + 110 * u, vis(t, tf + 0.3), 44 * u)

def planets(c, W, H, t, S):
    u = S.u
    fill_bg(c, W, H, "#02040f", "#0a1029"); stars(c, W, H, t, 0.9, seed=14)
    hills(c, W, 0.84 * H, 40 * u, "#04060c", 22, H=H)
    kt = [0, S.lt(2, 0.12), S.lt(2, 0.42), S.lt(2, 0.72), S.dur]
    kv = [0, 13, 80, 150, 160]
    for i in range(4):
        if t <= kt[i + 1]:
            mins = lerp(kv[i], kv[i + 1], (t - kt[i]) / max(kt[i + 1] - kt[i], 1e-3)); break
    else: mins = kv[-1]
    chip(c, "AFTER LIGHTS OUT", W / 2, 0.08 * H, 1, 28 * u)
    h_, m_ = divmod(int(mins), 60)
    text(c, f"{h_}:{m_:02d}", W / 2, 0.08 * H + 90 * u, 90 * u, ACCENT, 1, w=900, shadow=10)
    ps = [("MARS", 0.78, 0.5, "#ff8a65", kt[1], "+13 MIN"), ("JUPITER", 0.27, 0.36, "#ffe6b3", kt[2], "+1 HOUR"),
          ("SATURN", 0.6, 0.27, "#ffeec2", kt[3], "+2 HOURS")]
    for name, fx, fy, colr, tb, lab in ps:
        x, y = fx * W, fy * H
        a = 1 - prog(t, tb, 0.18)
        if a > 0:
            circle(c, x, y, 30 * u, colr, 0.25 * a, blur=14 * u); circle(c, x, y, 7 * u, colr, a)
            line(c, x - 22 * u, y, x + 22 * u, y, colr, 2, 0.5 * a); line(c, x, y - 22 * u, x, y + 22 * u, colr, 2, 0.5 * a)
        else:
            circle(c, x, y, 10 * u + (t - tb) * 30 * u, colr, max(0, 0.5 - (t - tb)), stroke=2)
        if name != "MARS":
            chip(c, f"{name}  {lab}", x, y + 75 * u, vis(t, S.lt(1, 0.1 if name == "JUPITER" else 0.6)) * a, 34 * u)

def orbit_break(c, W, H, t, S):
    u = S.u; quick = S.opts.get("quick")
    if not quick and S.n() > 2 and t >= S.ls(2):
        tt = t - S.ls(2)
        space_bg(c, W, H, t, 1, seed=16, drift=(-40, 0))
        earth(c, W * 0.45 + tt * 25 * u, H / 2, 140 * u, rot=t * 6, day=0.0, lights=0.9, starlight=0.6)
        chip(c, "DRIFTING", W / 2, 0.85 * H, vis(t, S.ls(2) + 0.6), 40 * u)
        return
    if not quick and S.n() > 1 and t >= S.ls(1):
        tt = t - S.ls(1)
        space_bg(c, W, H, t, 0.6, seed=17)
        x0, x1, y = 0.15 * W, 0.85 * W, 0.55 * H
        p = ease(prog(tt, 0.4, 3.2))
        rrect(c, x0, y - 14 * u, x1 - x0, 28 * u, 14 * u, "#ffffff", 0.15)
        rrect(c, x0, y - 14 * u, (x1 - x0) * p, 28 * u, 14 * u, ACCENT, 0.9)
        earth(c, lerp(x0, x1, p), y, 34 * u, rot=t * 30, day=0.0, lights=1, starlight=1, clouds=False)
        text(c, "USA, COAST TO COAST  ≈ 4,500 KM", W / 2, y - 120 * u, 48 * u, "#ffffff", 1, w=800, shadow=8)
        secs = int(150 * p); text(c, f"{secs // 60}:{secs % 60:02d}", W / 2, y + 140 * u, 110 * u, ACCENT, 1, w=900, shadow=10)
        text(c, "AT 30 KM PER SECOND", W / 2, y + 230 * u, 36 * u, "#cfe3ff", 1, w=600, fam="Inter")
        return
    space_bg(c, W, H, t, 1, seed=15)
    cx, cy = (W / 2, H / 2) if not S.P else (W / 2, H * 0.55)
    Ro = 330 * u
    ghost_ring(c, cx, cy, 40 * u, t, 0.8)
    circle(c, cx, cy, Ro, "#ffffff", 0.22, stroke=2.5 * u, dash=([14, 12], 0))
    tb = S.lt(0, 0.3) if not quick else 0.35
    w_ = 0.55 if not quick else 0.9
    rr = Ro * t / tb if t < tb else Ro + (t - tb) * 600 * u
    if rr > 50 * u: circle(c, cx, cy, rr, "#9fd3ff", 0.55 * clamp(1 - max(0, t - tb) / 1.2), stroke=5 * u)
    th0 = 0.5
    if t < tb:
        th = th0 + w_ * t; ex, ey = cx + math.cos(th) * Ro, cy + math.sin(th) * Ro
        lit = True
    else:
        thb = th0 + w_ * tb; bx, by = cx + math.cos(thb) * Ro, cy + math.sin(thb) * Ro
        v = w_ * Ro; dx, dy = -math.sin(thb), math.cos(thb)
        d = v * (t - tb); ex, ey = bx + dx * d, by + dy * d
        line(c, bx, by, ex, ey, "#8fd0ff", 5 * u, 0.7)
        lit = False
    p = skia.Path(); th_now = th0 + w_ * min(t, tb)
    p.addArc(skia.Rect.MakeLTRB(cx - Ro, cy - Ro, cx + Ro, cy + Ro), math.degrees(th_now) - 60, 60)
    c.drawPath(p, paint("#8fd0ff", 0.6, stroke=5 * u))
    earth(c, ex, ey, 40 * u, rot=t * 20, day=0.0 if not lit else 1.0, lights=1, starlight=0.8, clouds=False)
    chip(c, "30 KM/S", ex, ey - 85 * u, vis(t, tb + 0.4), 34 * u, bg="#1b2250")
    if not quick:
        chip(c, "GRAVITY CATCHES UP", W / 2, 0.08 * H, vis(t, S.lt(0, 0.12)), 32 * u, dot="#9fd3ff")

# ======================================================= 1 DAY
def heat_arrows(c, x, y, R, t, u, a=1.0):
    for i in range(14):
        ang = i * 2 * math.pi / 14 + 0.2
        for k in range(2):
            q = (t * 0.35 + k * 0.5 + i * 0.07) % 1.0
            r0 = R * (1.08 + q * 0.75)
            al = a * math.sin(q * math.pi) * 0.9
            pts = []
            for j in range(9):
                rr = r0 + j * 9 * u
                off = math.sin(j * 1.2 + t * 6) * 6 * u
                pts.append((x + math.cos(ang) * rr - math.sin(ang) * off, y + math.sin(ang) * rr + math.cos(ang) * off))
            c.drawPath(poly(pts, close=False), paint("#ff7b3a", al, stroke=5 * u))

def city_night(c, W, H, t, S):
    u = S.u
    if S.n() > 1 and t >= S.ls(1):
        space_bg(c, W, H, t, 1, seed=18)
        R = 260 * u
        earth(c, W / 2, H / 2, R, rot=t * 5, day=0.0, lights=1, starlight=0.5)
        heat_arrows(c, W / 2, H / 2, R, t, u, ease(prog(t, S.ls(1), 1.0)))
        chip(c, "HEAT LEAKING INTO SPACE", W / 2, 0.9 * H, vis(t, S.lt(1, 0.3)), 38 * u, dot="#ff7b3a")
        return
    fill_bg(c, W, H, "#02040f", "#0d1433"); stars(c, W, H, t, 1, seed=19)
    base = 0.78 * H
    skyline(c, W, base, H, 5, "#0b1124", win=1.0, maxh=0.42)
    rect(c, 0, base, W, H - base, "#070b18")
    for i, fx in enumerate([0.18, 0.26, 0.47, 0.55, 0.72, 0.8]):
        person(c, fx * W, H - 30 * u, 210 * u, "#020308", look_up=1)
    chip(c, "STILL WARM… FOR NOW", W / 2, 0.1 * H, vis(t, S.lt(0, 0.35)), 36 * u)

def plants(c, W, H, t, S):
    u = S.u
    fill_bg(c, W, H, "#02040f", "#0b1230"); stars(c, W, H, t, 1, seed=20)
    hy = 0.62 * H
    hills(c, W, hy, 50 * u, "#0c1a1f", 31, H=H)
    brown = ease(prog(t, S.ls(2), S.le(2) - S.ls(2) + 1)) if S.n() > 2 else 0
    leaf = mix("#1f4a3a", "#2a2a24", 0.5 * brown)
    for fx, sc in [(0.1, 1.2), (0.3, 0.9), (0.72, 1.3), (0.88, 1.0)]:
        tree(c, fx * W, hy + 0.12 * H, 300 * u * sc, leaf, "#1a130e")
    hills(c, W, hy + 0.2 * H, 15 * u, "#0a1410", 32, H=H)
    rng = random.Random(4)
    gcol = mix("#2f6b45", "#6b5a32", brown)
    for i in range(140):
        x = rng.random() * W; h = rng.uniform(40, 90) * u * (1 - 0.45 * brown)
        sway = math.sin(t * 1.5 + i) * 6 * u + brown * 25 * u * (1 if i % 2 else -1)
        line(c, x, H, x + sway, H - h, gcol, 5 * u)
    # battery
    bx, by, bw, bh = W - 300 * u, 0.12 * H, 180 * u, 80 * u
    if S.P: bx, by = W / 2 - bw / 2, 0.08 * H
    lvl = clamp(1 - t / S.dur * 0.95)
    rrect(c, bx, by - bh / 2, bw, bh, 14 * u, "#ffffff", 0.9, stroke=6 * u)
    rect(c, bx + bw + 4 * u, by - 16 * u, 12 * u, 32 * u, "#ffffff", 0.9)
    rrect(c, bx + 10 * u, by - bh / 2 + 10 * u, (bw - 20 * u) * lvl, bh - 20 * u, 6 * u, mix("#ff4d4d", "#4cd964", lvl))
    text(c, "PLANT POWER", bx + bw / 2, by + 80 * u, 26 * u, "#cfe3ff", 1, w=700, fam="Inter")
    chip(c, "PHOTOSYNTHESIS: OFF", W / 2 if S.P else 0.35 * W, 0.12 * H, vis(t, S.lt(0, 0.7), until_next(S, 0)), 38 * u, dot="#ff4d4d")
    for k, nm in enumerate(["TREES", "GRASS", "PLANKTON"]):
        chip(c, nm, W * (0.3 + 0.2 * k), 0.12 * H, vis(t, S.lt(1, 0.2 + 0.22 * k), until_next(S, 1)), 36 * u, dot="#7a7f8f")
    chip(c, "SMALL PLANTS: DAYS TO WEEKS", W * 0.5, 0.12 * H, vis(t, S.lt(2, 0.05), S.lt(2, 0.45)), 36 * u)
    chip(c, "BIG TREES: MUCH LONGER", W * 0.5, 0.12 * H, vis(t, S.lt(2, 0.5), until_next(S, 2)), 36 * u)
    chip(c, "NO NEW GROWTH", W * 0.5, 0.12 * H, vis(t, S.lt(3, 0.2)), 40 * u, dot="#ff4d4d")

def _icon(c, kind, x, y, s, colr):
    if kind == "leaf":
        c.save(); c.translate(x, y); c.rotate(-35)
        p = skia.Path(); p.moveTo(0, -s); p.quadTo(s * 0.9, 0, 0, s); p.quadTo(-s * 0.9, 0, 0, -s)
        c.drawPath(p, paint(colr)); line(c, 0, -s * 0.8, 0, s * 1.2, mix(colr, "#000000", 0.35), s * 0.08)
        c.restore()
    elif kind == "rabbit":
        oval(c, x, y + s * 0.3, s * 0.7, s * 0.5, colr); circle(c, x + s * 0.55, y - s * 0.2, s * 0.35, colr)
        oval(c, x + s * 0.45, y - s * 0.85, s * 0.11, s * 0.38, colr); oval(c, x + s * 0.7, y - s * 0.82, s * 0.11, s * 0.38, colr)
        circle(c, x - s * 0.7, y + s * 0.2, s * 0.16, mix(colr, "#ffffff", 0.4))
    elif kind == "paw":
        oval(c, x, y + s * 0.3, s * 0.5, s * 0.42, colr)
        for dx, dy in [(-0.55, -0.25), (-0.2, -0.6), (0.2, -0.6), (0.55, -0.25)]:
            oval(c, x + dx * s, y + dy * s, s * 0.17, s * 0.22, colr)
    elif kind == "person":
        circle(c, x, y - s * 0.55, s * 0.32, colr); rrect(c, x - s * 0.45, y - s * 0.15, s * 0.9, s * 1.0, s * 0.4, colr)

def food_chain(c, W, H, t, S):
    u = S.u; space_bg(c, W, H, t, 0.5, seed=23)
    items = [("leaf", "PLANTS", "#4cd964"), ("rabbit", "PLANT EATERS", "#d8c3a5"), ("paw", "PREDATORS", "#f08a4b"), ("person", "YOU", "#9fd3ff")]
    tg = S.lt(0, 0.6)
    n = len(items)
    for i, (ic, lab, colr) in enumerate(items):
        if not S.P: x, y = W * (0.14 + 0.24 * i), H * 0.48
        else: x, y = W / 2, H * (0.2 + 0.2 * i)
        p = eback(prog(t, 0.1 + i * 0.18, 0.4))
        if p <= 0: continue
        grey = prog(t, tg + i * 0.35, 0.3)
        c.save(); c.translate(x, y); c.scale(p, p)
        rrect(c, -130 * u, -130 * u, 260 * u, 260 * u, 40 * u, mix("#16204a", "#1a1c24", grey))
        rrect(c, -130 * u, -130 * u, 260 * u, 260 * u, 40 * u, mix(colr, "#4a4f5e", grey), 0.8, stroke=5 * u)
        _icon(c, ic, 0, -10 * u, 85 * u, mix(colr, "#4a4f5e", grey))
        c.restore()
        text(c, lab, x, y + 175 * u, 34 * u, "#ffffff", clamp(p), w=800)
        if i < n - 1 and p >= 0.99:
            if not S.P:
                x0, x1 = x + 145 * u, x + W * 0.24 - 145 * u
                line(c, x0, y, x1, y, "#ffffff", 5 * u, 0.6)
                c.drawPath(poly([(x1 + 4 * u, y), (x1 - 16 * u, y - 14 * u), (x1 - 16 * u, y + 14 * u)]), paint("#ffffff", 0.6))
    chip(c, "IT ALL STARTS WITH PLANTS", W / 2, 0.88 * H, vis(t, tg + 0.3), 38 * u, dot="#4cd964")

# ======================================================= 1 WEEK
@lru_cache(maxsize=4)
def _frost_segments(W, H, seed=5):
    rng = random.Random(seed); segs = []
    def grow(x, y, ang, L, depth, birth):
        steps = int(L / 14)
        for _ in range(steps):
            nx, ny = x + math.cos(ang) * 14, y + math.sin(ang) * 14
            segs.append((x, y, nx, ny, birth, depth)); x, y = nx, ny; birth += 0.012
            ang += rng.uniform(-0.25, 0.25)
            if depth < 3 and rng.random() < 0.22:
                grow(x, y, ang + rng.choice([-1, 1]) * rng.uniform(0.6, 1.1), L * 0.45, depth + 1, birth)
    for _ in range(46):
        side = rng.randrange(4)
        if side == 0: x, y, a = rng.random() * W, 0, math.pi / 2
        elif side == 1: x, y, a = rng.random() * W, H, -math.pi / 2
        elif side == 2: x, y, a = 0, rng.random() * H, 0
        else: x, y, a = W, rng.random() * H, math.pi
        grow(x, y, a + rng.uniform(-0.5, 0.5), rng.uniform(0.18, 0.4) * min(W, H), 0, rng.uniform(0, 0.3))
    return segs

def snow(c, W, H, t, u, n=120, seed=8, speed=60, a=1.0, size=1.0):
    rng = random.Random(seed)
    for i in range(n):
        x0, y0 = rng.random() * W, rng.random() * H; sp = rng.uniform(0.6, 1.4) * speed * u; r = rng.uniform(2, 5) * u * size
        y = (y0 + t * sp) % (H + 20) - 10; x = x0 + math.sin(t * 0.8 + i) * 18 * u
        circle(c, x, y, r, "#ffffff", a * rng.uniform(0.5, 0.95))

def frost(c, W, H, t, S):
    u = S.u
    fill_bg(c, W, H, "#0a1029", "#1d2748"); stars(c, W, H, t, 0.5, seed=24)
    base = 0.8 * H
    skyline(c, W, base, H, 9, "#202b4a", win=0.6, maxh=0.4, win_col="#ffcf8a")
    rng = random.Random(9); x = -20
    rect(c, 0, base, W, H - base, "#c9d6ec")
    snow(c, W, H, t, u, 140)
    # frost growth
    g = ease(t / S.dur) * 1.25
    for x0, y0, x1, y1, b, d in _frost_segments(W, H):
        if b < g: line(c, x0, y0, x1, y1, "#eaf6ff", (3.5 - d * 0.7) * u, 0.75)
    c.drawPaint(paint(shader=rad(W / 2, H / 2, max(W, H) * 0.75, [(0.45, "#eaf6ff", 0), (1, "#eaf6ff", 0.55 * clamp(g))])))
    # window frame
    fw = 40 * u; fc = "#1a1410"
    for (x_, y_, w_, h_) in [(0, 0, W, fw), (0, H - fw, W, fw), (0, 0, fw, H), (W - fw, 0, fw, H)]:
        rect(c, x_, y_, w_, h_, fc)
    if not S.P: rect(c, W / 2 - fw / 2, 0, fw, H, fc); rect(c, 0, H * 0.45 - fw / 2, W, fw, fc)
    else: rect(c, 0, H * 0.42 - fw / 2, W, fw, fc)
    temp_target = S.opts.get("temp", -18)
    tt = lerp(15, temp_target, ease(prog(t, 0.3, (S.le(0) if S.n() else S.dur) - 0.3)))
    tx, ty, th = (0.84 * W, 0.62 * H, 420 * u) if not S.P else (0.62 * W, 0.25 * H, 360 * u)
    rrect(c, tx - 80 * u, ty - th / 2 - 50 * u, 380 * u, th + 160 * u, 30 * u, "#0b1030", 0.75)
    thermometer(c, tx, ty, th, tt, tmax=20, tmin=-30, unit2="0 °F" if (S.n() > 1 and t > S.ls(1)) or S.P else None, size=u)
    chip(c, "BELOW FREEZING", W * (0.3 if not S.P else 0.5), 0.12 * H, vis(t, S.lt(0, 0.75)), 40 * u, dot="#3fa7ff")

def _pylon(c, x, y, s, a, t, strain):
    colr = "#c7cfdf"
    pts = [(-0.35, 1), (-0.12, -0.9), (0.12, -0.9), (0.35, 1)]
    line(c, x - 0.35 * s, y + s, x - 0.1 * s, y - 0.9 * s, colr, 5, a); line(c, x + 0.35 * s, y + s, x + 0.1 * s, y - 0.9 * s, colr, 5, a)
    for k in range(5):
        yy = y + s - k * 0.38 * s
        line(c, x - (0.35 - k * 0.05) * s, yy, x + (0.3 - k * 0.05) * s, yy - 0.38 * s, colr, 3, a * 0.8)
    line(c, x - 0.6 * s, y - 0.55 * s, x + 0.6 * s, y - 0.55 * s, colr, 5, a)
    if strain > 0:
        fl = 0.5 + 0.5 * math.sin(t * 12)
        c.drawPath(poly([(x + 0.25 * s, y - 0.95 * s), (x + 0.05 * s, y - 0.5 * s), (x + 0.22 * s, y - 0.5 * s), (x + 0.0 * s, y - 0.05 * s), (x + 0.42 * s, y - 0.62 * s), (x + 0.25 * s, y - 0.62 * s), (x + 0.42 * s, y - 0.95 * s)]), paint("#ffd166", a * strain * fl))

def grid(c, W, H, t, S):
    u = S.u; fill_bg(c, W, H, "#060a1d", "#121a3d"); snow(c, W, H, t, u, 80, seed=11, a=0.5)
    tiles = [("LAKES FREEZE", S.ls(0)), ("GRIDS STRAINED", S.ls(1)), ("SOLAR: 0%", S.ls(2)), ("WIND WINDS DOWN", S.ls(3))]
    for i, (lab, t0) in enumerate(tiles):
        if not S.P: x, y = W * (0.14 + 0.24 * i), H * 0.5
        else: x, y = W * (0.28 + 0.44 * (i % 2)), H * (0.38 + 0.26 * (i // 2))
        p = eback(prog(t, t0 + 0.1, 0.45))
        if p <= 0: continue
        c.save(); c.translate(x, y); c.scale(p, p)
        rrect(c, -190 * u, -200 * u, 380 * u, 400 * u, 36 * u, "#0d1438", 0.95)
        rrect(c, -190 * u, -200 * u, 380 * u, 400 * u, 36 * u, "#ffffff", 0.15, stroke=3 * u)
        s = 110 * u; tt = t - t0
        if i == 0:
            oval(c, 0, 0, 1.3 * s, 0.6 * s, "#bfe3ff")
            for k in range(5):
                a0 = k * 1.2 + 0.3
                line(c, 0, 0, math.cos(a0) * 1.1 * s * min(1, tt), math.sin(a0) * 0.5 * s * min(1, tt), "#6aa9d9", 4 * u)
        elif i == 1:
            _pylon(c, 0, -0.1 * s, s, 1, t, clamp(tt / 1.0))
        elif i == 2:
            c.save(); c.skew(-0.3, 0)
            rrect(c, -0.9 * s, -0.4 * s, 1.8 * s, 0.9 * s, 8 * u, "#2a4c8a")
            for k in range(1, 4): line(c, -0.9 * s + k * 0.45 * s, -0.4 * s, -0.9 * s + k * 0.45 * s, 0.5 * s, "#9fc3ff", 2 * u, 0.6)
            line(c, -0.9 * s, 0.05 * s, 0.9 * s, 0.05 * s, "#9fc3ff", 2 * u, 0.6)
            c.restore()
            circle(c, 0.75 * s, -0.75 * s, 0.32 * s, "#ffd166", 0.9, stroke=5 * u, dash=([10, 8], 0))
            line(c, 0.45 * s, -1.05 * s, 1.05 * s, -0.45 * s, "#ff4d4d", 7 * u)
        else:
            line(c, 0, -0.3 * s, 0, 1.0 * s, "#e6ebf5", 9 * u)
            om = 5.0 * math.exp(-max(tt, 0) / 2.5)
            ang = 5.0 * 2.5 * (1 - math.exp(-max(tt, 0) / 2.5))
            c.save(); c.translate(0, -0.3 * s); c.rotate(math.degrees(ang) * 3)
            for k in range(3):
                c.rotate(120); c.drawPath(poly([(0, 0), (-0.08 * s, -0.55 * s), (0, -0.95 * s), (0.08 * s, -0.5 * s)]), paint("#e6ebf5"))
            c.restore(); circle(c, 0, -0.3 * s, 0.1 * s, "#c7cfdf")
        c.restore()
        text(c, lab, x, y + 140 * u * p, 34 * u, "#ffffff", clamp(p), w=800)

# ======================================================= 1 YEAR
def earth_ice(c, W, H, t, S):
    u = S.u; space_bg(c, W, H, t, 1, seed=25)
    ex = 0.36 * W if not S.P else W / 2
    ice = lerp(0.45, 0.9, ease(t / S.dur))
    earth(c, ex, H / 2, 330 * u, rot=t * 4, day=0.5, night_side=False, ice=ice, lights=0.2, starlight=1, clouds=False)
    tt = lerp(-18, -73, ease(prog(t, 0.2, S.le(0) - 0.2)))
    thermometer(c, 0.7 * W, H / 2, 480 * u, tt, tmax=20, tmin=-100, unit2="−100 °F" if t > S.lt(0, 0.7) else None, size=u)
    chip(c, "COLDER THAN ALMOST ANYWHERE EVER RECORDED", W / 2, 0.92 * H, vis(t, S.lt(1, 0.1)), 32 * u, dot="#3fa7ff")

def ocean_section(c, W, H, t, S, chips=True, vent_glow=0.0):
    u = S.u
    sky = 0.22 * H
    fill_bg(c, W, H, "#02040f", "#0a1029")
    rect(c, 0, sky, W, H - sky, "#061a33")
    c.drawRect(skia.Rect.MakeXYWH(0, sky, W, H - sky), paint(shader=lin(0, sky, 0, H, [(0, "#0e4a80", 1), (1, "#03101f", 1)])))
    thick = lerp(14, 90, ease(prog(t, S.ls(1), 2.5))) * u if S.n() > 1 else 50 * u
    rect(c, 0, sky - 6 * u, W, thick + 6 * u, "#dff1ff")
    rect(c, 0, sky + thick - 8 * u, W, 8 * u, "#a8d4f5")
    floor_y = 0.86 * H
    hills(c, W, floor_y, 22 * u, "#2a1b12", 41, H=H)
    c.drawRect(skia.Rect.MakeXYWH(0, floor_y + 20 * u, W, H), paint(shader=lin(0, floor_y, 0, H, [(0, "#2a1b12", 1), (1, "#7a2e12", 1)])))
    hp = ease(prog(t, S.ls(2), 1.5)) if S.n() > 2 else 0
    if hp > 0:
        c.drawPaint(paint(shader=rad(W / 2, H * 1.2, H * 0.55, [(0, "#ff7a1a", 0.55 * hp), (1, "#ff7a1a", 0)])))
        rng = random.Random(6)
        for i in range(12):
            x = rng.random() * W; ph = rng.random()
            q = (ph + t * 0.25) % 1
            y0 = floor_y - q * (floor_y - sky - thick) * 0.85
            pts = [(x + math.sin(j * 0.9 + t * 4) * 8 * u, y0 - j * 10 * u) for j in range(8)]
            c.drawPath(poly(pts, close=False), paint("#ff8c3a", hp * math.sin(q * math.pi) * 0.8, stroke=5 * u))
    rng = random.Random(7)
    for i in range(40):
        x = rng.random() * W; y = sky + thick + ((rng.random() + t * 0.02 * rng.random()) % 1) * (floor_y - sky - thick)
        circle(c, x, y, 2 * u, "#9fd3ff", 0.25)
    if vent_glow:
        circle(c, W / 2, floor_y + 5 * u, 30 * u, "#ffb347", vent_glow, blur=12 * u)
        circle(c, W / 2, floor_y + 5 * u, 7 * u, "#fff1c1", vent_glow)
    if chips:
        chip(c, "THE OCEANS DON'T FREEZE SOLID", W / 2, 0.1 * H, vis(t, S.lt(0, 0.5), until_next(S, 0)), 36 * u)
        chip(c, "ICE = A BLANKET", W * 0.5, sky + thick + 70 * u, vis(t, S.lt(1, 0.45)), 34 * u, bg="#0b3050")
        chip(c, "LIQUID WATER", W * 0.25, H * 0.55, vis(t, S.lt(2, 0.6)), 34 * u, bg="#0b3050")
        chip(c, "HEAT FROM EARTH'S CORE", W * 0.68, floor_y - 90 * u, vis(t, S.lt(2, 0.25)), 34 * u, dot="#ff8c3a")

# ======================================================= SURVIVAL
def steam(c, x, y, t, u, a=1.0, seed=1):
    rng = random.Random(seed)
    for i in range(16):
        ph = rng.random(); q = (ph + t * 0.18) % 1
        r = (25 + q * 90) * u
        circle(c, x + math.sin(q * 4 + i) * 30 * u * q, y - q * 360 * u, r, "#e8eef8", a * 0.35 * (1 - q), blur=r * 0.35)

def geothermal(c, W, H, t, S):
    u = S.u
    fill_bg(c, W, H, "#02040f", "#0b1230"); stars(c, W, H, t, 1, seed=27)
    rng = random.Random(3)
    for k in range(6):
        mx = W * (k / 5) + rng.uniform(-80, 80) * u; mh = rng.uniform(0.25, 0.4) * H; base = 0.72 * H; mw = rng.uniform(0.25, 0.4) * W
        c.drawPath(poly([(mx - mw / 2, base), (mx, base - mh), (mx + mw / 2, base)]), paint("#1a2440"))
        c.drawPath(poly([(mx - mw * 0.12, base - mh * 0.76), (mx, base - mh), (mx + mw * 0.12, base - mh * 0.76)]), paint("#5b6b8f"))
    rect(c, 0, 0.72 * H, W, 0.28 * H, "#27324f")
    cx, gy = W / 2, 0.78 * H
    c.drawPaint(paint(shader=rad(cx, gy, 520 * u, [(0, "#ffb347", 0.35), (1, "#ffb347", 0)])))
    for dx in (-200, 160):
        x = cx + dx * u
        c.drawPath(poly([(x - 70 * u, gy), (x - 50 * u, gy - 200 * u), (x + 50 * u, gy - 200 * u), (x + 70 * u, gy)]), paint("#56607a"))
        steam(c, x, gy - 210 * u, t, u, 1, seed=int(dx))
    rect(c, cx - 110 * u, gy - 130 * u, 220 * u, 130 * u, "#3a4460")
    for wx in range(4):
        rect(c, cx - 90 * u + wx * 50 * u, gy - 100 * u, 28 * u, 34 * u, "#ffcf6e", 0.9)
    line(c, cx - 380 * u, gy - 30 * u, cx + 380 * u, gy - 30 * u, "#8a93ab", 10 * u)
    dp = ease(prog(t, S.ls(2), 1.2)) if S.n() > 2 else 0
    for k, dx in enumerate([-560, -420, 430, 580]):
        if dp <= 0: break
        x = cx + dx * u; r = 70 * u * dp
        c.drawPath(_dome(x, gy + 10 * u, r), paint("#9fd3ff", 0.35)); c.drawPath(_dome(x, gy + 10 * u, r), paint("#cfeaff", 0.9, stroke=4 * u))
        circle(c, x, gy - r * 0.3, r * 0.25, "#ffcf6e", 0.8 * dp)
    big = vis(t, 0.15, until_next(S, 0))
    text(c, "COULD ANYONE SURVIVE?", W / 2, 0.12 * H, 80 * u, "#ffffff", big, w=900, shadow=12)
    chip(c, "MAYBE. FOR A WHILE.", W / 2, 0.24 * H, vis(t, S.lt(0, 0.65), until_next(S, 0)), 38 * u, bg="#1b2250")
    chip(c, "GEOTHERMAL HEAT", W / 2, 0.12 * H, vis(t, S.lt(1, 0.4), until_next(S, 1)), 38 * u, dot="#ffb347")
    chip(c, "SEALED HABITATS", W * 0.35, 0.12 * H, vis(t, S.lt(2, 0.3)), 36 * u, dot="#9fd3ff")
    chip(c, "OR NUCLEAR POWER", W * 0.65, 0.12 * H, vis(t, S.lt(2, 0.7)), 36 * u, dot="#7CFC9A")

def _dome(x, y, r):
    p = skia.Path(); p.addArc(skia.Rect.MakeLTRB(x - r, y - r, x + r, y + r), 180, 180); p.close(); return p

def bunker(c, W, H, t, S):
    u = S.u
    fill_bg(c, W, H, "#02040f", "#0b1230"); stars(c, W, int(0.2 * H), t, 1, seed=28)
    sy = 0.2 * H
    rect(c, 0, sy, W, 30 * u, "#c9d6ec")
    c.drawRect(skia.Rect.MakeXYWH(0, sy + 30 * u, W, H), paint(shader=lin(0, sy, 0, H, [(0, "#3a2a1e", 1), (1, "#1c130d", 1)])))
    rect(c, W / 2 - 30 * u, sy, 60 * u, 0.22 * H, "#120c08")
    rooms = [(0.1, 0.42), (0.4, 0.42), (0.7, 0.42), (0.1, 0.7), (0.4, 0.7), (0.7, 0.7)]
    rw, rh = 0.24 * W, 0.22 * H
    for k, (fx, fy) in enumerate(rooms):
        x, y = fx * W, fy * H
        rrect(c, x, y, rw, rh, 16 * u, "#0d0f17")
        if k in (0, 1, 3, 4):
            c.drawRect(skia.Rect.MakeXYWH(x, y, rw, rh), paint(shader=lin(0, y, 0, y + rh, [(0, "#ff5ad1", 0.55), (1, "#7b2ff7", 0.1)])))
            for row in range(3):
                yy = y + rh * (0.45 + row * 0.18)
                line(c, x + 20 * u, yy + 8 * u, x + rw - 20 * u, yy + 8 * u, "#4a3426", 6 * u)
                for j in range(9):
                    px = x + 35 * u + j * (rw - 70 * u) / 8
                    sz = (10 + 3 * math.sin(t * 2 + j + row)) * u
                    circle(c, px, yy, sz, "#56d364")
            for j in range(4): rect(c, x + rw * (0.12 + j * 0.22), y + 6 * u, rw * 0.14, 8 * u, "#ffd1f2")
        elif k == 2:
            cx_, cy_ = x + rw / 2, y + rh / 2
            circle(c, cx_, cy_, rh * 0.36, "#5a6278", stroke=6 * u)
            c.save(); c.translate(cx_, cy_); c.rotate(t * 300)
            for j in range(4):
                c.rotate(90); c.drawPath(poly([(0, 0), (-rh * 0.08, -rh * 0.3), (rh * 0.08, -rh * 0.3)]), paint("#9fb3d9"))
            c.restore()
        else:
            rect(c, x, y, rw, rh, "#ffcf6e", 0.12)
            for j in range(3): person(c, x + rw * (0.25 + 0.25 * j), y + rh - 8 * u, rh * 0.6, "#ffcf9a")
        rrect(c, x, y, rw, rh, 16 * u, "#8a93ab", 0.6, stroke=5 * u)
    chip(c, "GROW LIGHTS", 0.22 * W, 0.37 * H, vis(t, S.lt(0, 0.12)), 30 * u, dot="#ff5ad1")
    chip(c, "RECYCLED AIR", 0.82 * W, 0.37 * H, vis(t, S.lt(0, 0.4)), 30 * u, dot="#9fb3d9")
    chip(c, "ENGINEERING", 0.82 * W, 0.65 * H, vis(t, S.lt(0, 0.75)), 30 * u, dot=ACCENT)
    chip(c, "HARDEST SURVIVAL CHALLENGE IN HISTORY", W / 2, 0.1 * H, vis(t, S.lt(1, 0.2)), 34 * u, bg="#1b2250")

# ======================================================= 1 MILLION YEARS
def deep_freeze(c, W, H, t, S):
    u = S.u; space_bg(c, W, H, t, 1, seed=29)
    ex, ey, R = (0.4 * W if not S.P else W / 2), H / 2, 320 * u
    earth(c, ex, ey, R, rot=t * 3, day=0.5, night_side=False, ice=1.0, starlight=1, clouds=False)
    cp = ease(prog(t, S.ls(1), 1.0)) if S.n() > 1 else 0
    if cp > 0:
        c.save(); p = skia.Path(); p.moveTo(ex, ey); p.arcTo(skia.Rect.MakeLTRB(ex - R, ey - R, ex + R, ey + R), -40, 70 * cp, False); p.close()
        c.clipPath(p, doAntiAlias=True)
        for rr, colr in [(1.0, "#6b7280"), (0.88, "#8a3b1e"), (0.55, "#d9661f"), (0.3, "#ffc04d")]:
            circle(c, ex, ey, R * rr, colr)
        c.restore()
        circle(c, ex, ey, R * 0.3, "#ffb347", 0.4 * cp * (0.7 + 0.3 * math.sin(t * 3)), blur=20 * u)
        chip(c, "THE CORE STILL LEAKS A LITTLE HEAT", W / 2, 0.92 * H, vis(t, S.lt(1, 0.5)), 32 * u, dot="#ffb347")
    tt = lerp(-73, -240, ease(prog(t, 0.2, S.le(0) - 0.2)))
    thermometer(c, 0.68 * W, H / 2, 480 * u, tt, tmax=20, tmin=-273, unit2="ABSOLUTE ZERO: −273 °C", size=u)

def flake(c, x, y, r, a, rot):
    for k in range(3):
        ang = rot + k * math.pi / 3
        line(c, x - math.cos(ang) * r, y - math.sin(ang) * r, x + math.cos(ang) * r, y + math.sin(ang) * r, "#ffffff", max(1.5, r * 0.18), a)

def air_snow(c, W, H, t, S):
    u = S.u
    fill_bg(c, W, H, "#010208", "#070b1c"); stars(c, W, H, t, 1, seed=30)
    hills(c, W, 0.75 * H, 40 * u, "#3a4563", 51, H=H)
    hills(c, W, 0.86 * H, 25 * u, "#58648a", 52, H=H)
    rng = random.Random(12)
    n = int(lerp(30, 160, ease(t / S.dur)))
    labels = {3: "N₂", 9: "O₂", 15: "N₂", 22: "O₂", 28: "N₂"}
    for i in range(160):
        x0, y0 = rng.random() * W, rng.random() * H; sp = rng.uniform(40, 90) * u; r = rng.uniform(5, 14) * u
        if i >= n: continue
        y = (y0 + t * sp) % (H + 40) - 20; x = x0 + math.sin(t * 0.7 + i) * 20 * u
        flake(c, x, y, r, 0.85, t * 0.5 + i)
        if i in labels: text(c, labels[i], x + r + 30 * u, y, 44 * u, "#bfe3ff", 0.9, w=700, fam="Inter")
    chip(c, "THE AIR ITSELF FREEZES", W / 2, 0.12 * H, vis(t, S.lt(0, 0.5), until_next(S, 0)), 38 * u)
    chip(c, "OXYGEN + NITROGEN SNOW", W / 2, 0.12 * H, vis(t, S.lt(1, 0.3)), 38 * u, dot="#bfe3ff")

@lru_cache(maxsize=2)
def _galaxy(seed=4):
    rng = random.Random(seed); pts = []
    for i in range(2600):
        arm = i % 2; r = rng.random() ** 0.6
        th = arm * math.pi + 5.2 * r + rng.gauss(0, 0.28)
        pts.append((r * math.cos(th) + rng.gauss(0, 0.03), r * math.sin(th) + rng.gauss(0, 0.03), rng.choice(["#ffffff", "#bcd4ff", "#ffd1e8", "#fff1c8"]), rng.uniform(0.3, 1)))
    for i in range(900):
        r = abs(rng.gauss(0, 0.13)); th = rng.random() * 6.28
        pts.append((r * math.cos(th), r * math.sin(th), "#fff1c8", rng.uniform(0.5, 1)))
    return pts

def rogue(c, W, H, t, S):
    u = S.u
    if S.n() > 1 and t >= S.ls(1):
        tt = t - S.ls(1)
        fill_bg(c, W, H, "#010208", "#070b1c"); stars(c, W, H, t, 0.5, seed=31)
        cx, cy = W / 2, H / 2; Rg = 520 * u * lerp(1.25, 1.0, eout(tt / 1.5))
        c.drawPaint(paint(shader=rad(cx, cy, Rg * 0.6, [(0, "#fff1c8", 0.55), (1, "#fff1c8", 0)])))
        rot = tt * 0.05
        for x, y, colr, a in _galaxy():
            xr = x * math.cos(rot) - y * math.sin(rot); yr = x * math.sin(rot) + y * math.cos(rot)
            circle(c, cx + xr * Rg, cy + yr * Rg * 0.6, 1.8 * u, colr, a * 0.8)
        rng = random.Random(9); nshow = int(eout(prog(tt, 1.0, 4.5)) * 70)
        for i in range(70):
            x = rng.uniform(-1, 1); y = rng.uniform(-1, 1)
            if i < nshow and x * x + y * y < 1:
                circle(c, cx + x * Rg, cy + y * Rg * 0.6, 7 * u, ACCENT, 0.9, stroke=2.5 * u)
        chip(c, "ROGUE PLANETS: MAYBE MORE COMMON THAN STARS", W / 2, 0.92 * H, vis(t, S.lt(1, 0.55)), 32 * u, dot=ACCENT)
        return
    space_bg(c, W, H, t, 1, seed=32, drift=(-25, 0))
    earth(c, W * 0.3 + t * 30 * u, H / 2, 200 * u, rot=t * 4, day=0.45, night_side=False, ice=1, starlight=1, clouds=False)
    chip(c, "A ROGUE PLANET", W / 2, 0.88 * H, vis(t, S.lt(0, 0.25)), 40 * u, bg="#1b2250")

# ======================================================= TWIST
def vent_objects(c, cx, fy, u, t, L, chimney_h):
    """Vent chimney + life, base centred at (cx, fy)."""
    rng = random.Random(21)
    # plume
    top = fy - chimney_h
    for i in range(60):
        ph = rng.random(); q = (ph + t * 0.12) % 1
        r = (18 + q * 110) * u
        circle(c, cx + math.sin(q * 5 + i) * q * 80 * u, top - q * 520 * u, r, "#1e1c22", L * 0.75 * (1 - q) ** 0.7, blur=r * 0.3)
    # chimney
    segs = 7
    for k in range(segs):
        w = lerp(200, 80, k / segs) * u; h = chimney_h / segs
        y = fy - (k + 1) * h
        rrect(c, cx - w / 2 + math.sin(k * 2.1) * 8 * u, y, w, h + 6 * u, 18 * u, mix("#3b2c24", "#4a3a30", (k % 2) * 0.5), L)
    for k in range(5):
        y = fy - chimney_h * rng.uniform(0.05, 0.9)
        line(c, cx - 40 * u, y, cx + rng.uniform(-30, 30) * u, y - 20 * u, "#ff8a3d", 3 * u, L * 0.8)
    c.drawCircle(cx, fy - chimney_h, 60 * u, paint("#ff8a3d", 0.35 * L, blur=30 * u))
    c.drawCircle(cx, fy, 300 * u, paint(shader=rad(cx, fy, 300 * u, [(0, "#ff8a3d", 0.35 * L), (1, "#ff8a3d", 0)])))
    # floor
    c.drawRect(skia.Rect.MakeLTRB(cx - 4000 * u, fy - 5 * u, cx + 4000 * u, fy + 2000 * u), paint("#1a120d", L))
    for i in range(60):
        x = cx + rng.uniform(-900, 900) * u
        circle(c, x, fy + rng.uniform(-4, 30) * u, rng.uniform(2, 5) * u, "#f2e6a8", 0.6 * L)
    # tube worms
    for i in range(22):
        bx = cx + (rng.choice([-1, 1]) * rng.uniform(130, 420)) * u; h = rng.uniform(110, 230) * u
        sway = math.sin(t * 1.3 + i) * 14 * u
        p = skia.Path(); p.moveTo(bx, fy); p.quadTo(bx + sway * 0.3, fy - h * 0.6, bx + sway, fy - h)
        c.drawPath(p, paint("#e9e4da", L, stroke=14 * u))
        for j in range(5):
            ang = j * 1.25 + t
            circle(c, bx + sway + math.cos(ang) * 9 * u, fy - h - 8 * u + math.sin(ang) * 6 * u, 10 * u, "#e0313a", L)
    # crabs
    for i in range(4):
        x = cx + (-520 + i * 330) * u + math.sin(t * 0.6 + i) * 40 * u; y = fy + 8 * u
        for k in range(3):
            line(c, x - 14 * u, y, x - 40 * u, y + 10 * u - k * 9 * u, "#f3eee6", 4 * u, L); line(c, x + 14 * u, y, x + 40 * u, y + 10 * u - k * 9 * u, "#f3eee6", 4 * u, L)
        oval(c, x, y - 6 * u, 28 * u, 16 * u, "#f3eee6", L)
    # shrimp
    for i in range(9):
        ang = t * 0.5 + i * 0.7
        x = cx + math.cos(ang) * (180 + i * 18) * u; y = fy - chimney_h * 0.35 + math.sin(ang * 1.3) * 120 * u
        p = skia.Path(); p.addArc(skia.Rect.MakeXYWH(x - 18 * u, y - 12 * u, 36 * u, 24 * u), 200, 220)
        c.drawPath(p, paint("#ffd6c9", L, stroke=8 * u))

def vent(c, W, H, t, S, chips=True):
    u = S.u
    fill_bg(c, W, H, "#020a14", "#000204")
    reveal = S.lt(0, 0.6) if S.n() > 1 else 0.15
    L = ease(prog(t, reveal, 1.6))
    rng = random.Random(5)
    for i in range(50):
        x = rng.random() * W; y = (rng.random() * H - t * 6 * u) % H
        circle(c, x, y, 2 * u, "#7fd3ff", 0.2 * L)
    fy = 0.86 * H if not S.P else 0.78 * H
    vent_objects(c, W / 2, fy, u, t, L, (0.45 if not S.P else 0.32) * H)
    if not chips: return
    if S.n() == 1:
        chip(c, "DOESN'T NEED THE SUN", W / 2, 0.2 * H, vis(t, 0.5), 40 * u, dot=ACCENT); return
    chip(c, "HYDROTHERMAL VENT", W / 2, 0.1 * H, vis(t, S.lt(1, 0.45), until_next(S, 1)), 38 * u, dot="#ff8a3d")
    for k, (nm, fx, fy_) in enumerate([("TUBE WORMS", 0.24, 0.62), ("CRABS", 0.78, 0.8), ("SHRIMP", 0.72, 0.42), ("BACTERIA", 0.2, 0.9)]):
        chip(c, nm, fx * W, fy_ * H, vis(t, S.lt(2, 0.22 + 0.1 * k), S.lt(2, 0.98)), 30 * u)
    chip(c, "ENERGY FROM CHEMICALS, NOT SUNLIGHT", W / 2, 0.1 * H, vis(t, S.lt(2, 0.7), until_next(S, 2)), 34 * u, dot=ACCENT)
    chip(c, "THEY'VE NEVER SEEN THE SUN", W / 2, 0.1 * H, vis(t, S.lt(3, 0.1)), 36 * u, bg="#1b2250")

def zoom_out(c, W, H, t, S):
    u = S.u; p = t / S.dur
    a1 = 1 - prog(p, 0.32, 0.1); a2 = prog(p, 0.32, 0.1) * (1 - prog(p, 0.66, 0.1)); a3 = prog(p, 0.66, 0.1)
    if a1 > 0:
        fill_bg(c, W, H, "#020a14", "#000204")
        s = lerp(1.0, 0.25, ease(p / 0.42)); fy = 0.86 * H
        c.save(); c.translate(W / 2, fy); c.scale(s, s); c.translate(-W / 2, -fy)
        vent_objects(c, W / 2, fy, u, t, 1, 0.45 * H)
        c.restore()
    if a2 > 0:
        lay = c.saveLayerAlpha(None, int(255 * a2))
        s = lerp(1.5, 1.0, ease((p - 0.32) / 0.38)); c.save(); c.translate(W / 2, 0.86 * H); c.scale(s, s); c.translate(-W / 2, -0.86 * H)
        ocean_section(c, W, H, t, Ctx(S.dur, [], {}, W, H), chips=False, vent_glow=1)
        c.restore(); c.restore()
    if a3 > 0:
        lay = c.saveLayerAlpha(None, int(255 * a3))
        space_bg(c, W, H, t, 1, seed=33)
        s = lerp(2.2, 1.0, eout((p - 0.66) / 0.34)); R = 300 * u * s
        earth(c, W / 2, H / 2, R, rot=40, day=0.5, night_side=False, ice=1, starlight=1, clouds=False)
        px, py = W / 2 + R * 0.15, H / 2 + R * 0.25
        circle(c, px, py, 24 * u, "#ffb347", 0.6 + 0.3 * math.sin(t * 4), blur=10 * u); circle(c, px, py, 6 * u, "#fff1c1")
        c.restore()
    chip(c, "THE LAST SURVIVORS?", W / 2, 0.1 * H, vis(t, S.lt(0, 0.6)), 38 * u, bg="#1b2250")

# ======================================================= END
def end_screen(c, W, H, t, S):
    u = S.u; space_bg(c, W, H, t, 1, seed=34, drift=(-8, 0))
    earth(c, W / 2, H * 0.62, 170 * u, rot=t * 4, day=0.5, night_side=False, ice=1, starlight=1, clouds=False, a=0.7)
    p = prog(t, 0.2, 0.5)
    text(c, "WOULD HUMANS MAKE IT?", W / 2, 0.18 * H, 96 * u, ACCENT, p, w=900, shadow=14)
    text(c, "Tell me in the comments", W / 2, 0.29 * H, 44 * u, "#ffffff", prog(t, 0.6, 0.5), w=600, fam="Inter")

def end_short(c, W, H, t, S):
    u = S.u; space_bg(c, W, H, t, 1, seed=35, drift=(-8, 0))
    earth(c, W / 2, H * 0.43, 210 * u, rot=t * 6, day=0.5, night_side=False, ice=1, starlight=1, clouds=False)
    p = prog(t, 0.1, 0.4)
    text(c, "WHO SURVIVES?", W / 2, 0.13 * H, 110 * u, "#ffffff", p, w=900, shadow=14)
    chip(c, S.opts.get("text", "FULL VIDEO ON THE CHANNEL"), W / 2, 0.21 * H, vis(t, S.lt(0, 0.5)), 44 * u, bg=ACCENT, fg="#0b1030", a=1)

SCENES = {k: v for k, v in globals().items() if callable(v) and k in (
    "park", "title", "card", "solar_system", "impossible", "distance", "stopwatch", "sun_blink", "light_beam",
    "ghost_orbit", "lights_out", "moon_fade", "planets", "orbit_break", "city_night", "plants", "food_chain",
    "frost", "grid", "earth_ice", "ocean_section", "geothermal", "bunker", "deep_freeze", "air_snow", "rogue",
    "vent", "zoom_out", "end_screen", "end_short")}
