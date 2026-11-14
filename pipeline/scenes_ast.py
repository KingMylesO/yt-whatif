"""Scenes: What If the Asteroid Was 30 Seconds Late? (+ 30 s and asteroid-belt Shorts)."""
from common2 import *
import geo

IMPACT = (-89.5, 21.4)  # Chicxulub lon, lat
GULF = (-99, 13, -77, 31)

# ---------------- props ----------------
def cretaceous_bg(c, W, H, t, u, hy=0.62, dusk=0.3, dark=0.0):
    top = mix(mix("#6fb6e8", "#ff9a6b", dusk), "#050816", dark); bot = mix(mix("#d8ecf5", "#ffd9a0", dusk), "#121a33", dark)
    fill_bg(c, W, H, top, bot)
    if dark > 0.3: stars(c, W, H, t, dark, seed=6)
    hills(c, W, hy * H, 60 * u, mix("#7a9a6a", "#0a1020", dark), 4, H=H)
    hills(c, W, hy * H + 0.05 * H, 40 * u, mix("#5a8250", "#080d18", dark), 5, H=H)
    for k in range(9):
        x = W * (k + 0.3) / 9; h = (200 + 70 * (k % 3)) * u
        conifer(c, x, hy * H + 0.06 * H, h, mix("#3a6a4a", "#070b14", dark))
    rect(c, 0, hy * H + 0.12 * H, W, H, mix("#6a7a3a", "#070b12", dark))
    for k in range(12):
        x = W * (k + 0.5) / 12; treefern(c, x, hy * H + 0.14 * H, (120 + 30 * (k % 2)) * u, a=1 - 0.5 * dark, t=t)

def pterosaur(c, x, y, s, t=0.0, colr="#1a1f2e", a=1.0):
    fl = math.sin(t * 5) * 0.3
    for sg in (-1, 1):
        c.drawPath(poly([(x, y), (x + sg * s, y - s * (0.2 + fl)), (x + sg * s * 0.5, y + s * 0.05)]), paint(colr, a))
    c.drawPath(poly([(x - s * 0.08, y), (x + s * 0.5, y - s * 0.12), (x + s * 0.08, y + s * 0.05)]), paint(colr, a))
    c.drawPath(poly([(x + s * 0.3, y - s * 0.1), (x + s * 0.15, y - s * 0.3), (x + s * 0.4, y - s * 0.12)]), paint(colr, a))

def plesiosaur(c, x, y, s, colr="#1a1f2e", a=1.0):
    oval(c, x, y, s * 0.5, s * 0.22, colr, a)
    p = skia.Path(); p.moveTo(x + s * 0.4, y - s * 0.05); p.quadTo(x + s * 0.8, y - s * 0.6, x + s * 1.1, y - s * 0.55)
    c.drawPath(p, paint(colr, a, stroke=s * 0.1)); circle(c, x + s * 1.12, y - s * 0.55, s * 0.08, colr, a)
    for dx, dy in ((0.2, 0.18), (-0.25, 0.18)):
        c.drawPath(poly([(x + dx * s, y + s * 0.1), (x + dx * s - s * 0.15, y + dy * s + s * 0.2), (x + dx * s + s * 0.05, y + s * 0.12)]), paint(colr, a))
    c.drawPath(poly([(x - s * 0.45, y), (x - s * 0.85, y - s * 0.05), (x - s * 0.45, y + s * 0.08)]), paint(colr, a))

def ammonite(c, x, y, s, colr="#c9a36a", a=1.0):
    p = skia.Path(); n = 80
    for i in range(n):
        th = i / n * 4 * math.pi; r = s * 0.12 * math.exp(0.17 * th)
        px, py = x + math.cos(th) * r, y + math.sin(th) * r
        (p.moveTo if i == 0 else p.lineTo)(px, py)
    circle(c, x, y, s * 0.95, colr, a * 0.9)
    c.drawPath(p, paint(mix(colr, "#000000", 0.4), a, stroke=s * 0.08))

def chicken(c, x, y, s, colr="#f4ead8", a=1.0):
    oval(c, x, y - s * 0.45, s * 0.45, s * 0.33, colr, a)
    c.drawPath(poly([(x - s * 0.4, y - s * 0.55), (x - s * 0.75, y - s * 0.95), (x - s * 0.55, y - s * 0.45)]), paint(colr, a))
    circle(c, x + s * 0.35, y - s * 0.85, s * 0.17, colr, a); rect(c, x + s * 0.25, y - s * 0.8, s * 0.15, s * 0.3, colr, a)
    for k in range(3): circle(c, x + s * (0.27 + k * 0.08), y - s * 1.02, s * 0.06, "#e8443a", a)
    c.drawPath(poly([(x + s * 0.5, y - s * 0.88), (x + s * 0.65, y - s * 0.84), (x + s * 0.5, y - s * 0.8)]), paint("#e0a43a", a))
    circle(c, x + s * 0.4, y - s * 0.88, s * 0.03, "#0b1030", a)
    for dx in (-0.08, 0.1): line(c, x + dx * s, y - s * 0.15, x + dx * s, y, "#e0a43a", s * 0.05, a)

def lizard(c, x, y, s, colr="#4caf50", a=1.0):
    oval(c, x, y, s * 0.4, s * 0.12, colr, a); oval(c, x + s * 0.45, y - s * 0.02, s * 0.14, s * 0.09, colr, a)
    p = skia.Path(); p.moveTo(x - s * 0.35, y); p.quadTo(x - s * 0.8, y + s * 0.1, x - s * 1.0, y - s * 0.12)
    c.drawPath(p, paint(colr, a, stroke=s * 0.07))
    for dx in (-0.2, 0.2):
        line(c, x + dx * s, y, x + dx * s - s * 0.1, y + s * 0.18, colr, s * 0.05, a); line(c, x + dx * s, y, x + dx * s + s * 0.08, y + s * 0.18, colr, s * 0.05, a)

def whale(c, x, y, s, colr="#5a7a9a", a=1.0):
    oval(c, x, y, s * 0.6, s * 0.22, colr, a)
    c.drawPath(poly([(x - s * 0.55, y), (x - s * 0.9, y - s * 0.22), (x - s * 0.8, y), (x - s * 0.9, y + s * 0.2)]), paint(colr, a))
    circle(c, x + s * 0.35, y - s * 0.04, s * 0.03, "#ffffff", a)

def monkey(c, x, y, s, colr="#8a6a4a", a=1.0):
    circle(c, x, y - s * 0.75, s * 0.18, colr, a); oval(c, x, y - s * 0.4, s * 0.18, s * 0.25, colr, a)
    oval(c, x, y - s * 0.72, s * 0.11, s * 0.09, "#d9b48a", a)
    for sg in (-1, 1):
        line(c, x + sg * s * 0.12, y - s * 0.5, x + sg * s * 0.35, y - s * 0.75, colr, s * 0.07, a)
        line(c, x + sg * s * 0.08, y - s * 0.2, x + sg * s * 0.12, y, colr, s * 0.07, a)
    p = skia.Path(); p.moveTo(x, y - s * 0.2); p.quadTo(x - s * 0.5, y - s * 0.05, x - s * 0.4, y - s * 0.45)
    c.drawPath(p, paint(colr, a, stroke=s * 0.05))

def bat(c, x, y, s, colr="#3a3a4a", a=1.0):
    c.drawPath(poly([(x, y - s * 0.1), (x - s * 0.9, y - s * 0.3), (x - s * 0.7, y), (x - s * 0.45, y - s * 0.05), (x - s * 0.25, y + s * 0.12),
                     (x, y + s * 0.05), (x + s * 0.25, y + s * 0.12), (x + s * 0.45, y - s * 0.05), (x + s * 0.7, y), (x + s * 0.9, y - s * 0.3)]), paint(colr, a))
    circle(c, x, y - s * 0.05, s * 0.12, colr, a)

def mammoth(c, x, y, s, colr="#7a5a3a", a=1.0):
    oval(c, x, y - s * 0.5, s * 0.5, s * 0.35, colr, a); circle(c, x + s * 0.45, y - s * 0.6, s * 0.25, colr, a)
    for dx in (-0.3, -0.1, 0.15, 0.3): rect(c, x + dx * s - s * 0.06, y - s * 0.3, s * 0.12, s * 0.3, colr, a)
    p = skia.Path(); p.moveTo(x + s * 0.6, y - s * 0.5); p.quadTo(x + s * 0.75, y - s * 0.1, x + s * 0.6, y - s * 0.05)
    c.drawPath(p, paint(colr, a, stroke=s * 0.08))
    p2 = skia.Path(); p2.moveTo(x + s * 0.55, y - s * 0.45); p2.quadTo(x + s * 0.95, y - s * 0.3, x + s * 0.85, y - s * 0.6)
    c.drawPath(p2, paint("#f4ead8", a, stroke=s * 0.05))

def spaceship(c, x, y, s, ang=0, a=1.0):
    c.save(); c.translate(x, y); c.rotate(ang)
    c.drawPath(poly([(s, 0), (-s * 0.6, -s * 0.45), (-s * 0.35, 0), (-s * 0.6, s * 0.45)]), paint("#d8dee9", a))
    circle(c, s * 0.25, 0, s * 0.12, "#7ec8ff", a)
    circle(c, -s * 0.5, 0, s * 0.18, "#ffb347", a * (0.6 + 0.4 * random.random()), blur=s * 0.1)
    c.restore()

def probe(c, x, y, s, a=1.0, kind="lucy"):
    rect(c, x - s * 0.2, y - s * 0.2, s * 0.4, s * 0.4, "#d9b45a", a)
    if kind == "lucy":
        for sg in (-1, 1):
            line(c, x + sg * s * 0.2, y, x + sg * s * 0.55, y, "#cfd8e3", s * 0.05, a)
            circle(c, x + sg * s * 1.0, y, s * 0.45, "#2a3a6a", a); circle(c, x + sg * s * 1.0, y, s * 0.45, "#9aa4c8", a, stroke=s * 0.04)
            for k in range(1, 4): circle(c, x + sg * s * 1.0, y, s * 0.45 * k / 4, "#9aa4c8", a * 0.5, stroke=s * 0.02)
    else:
        for sg in (-1, 1):
            rect(c, x + sg * s * 0.25 - (s * 1.2 if sg < 0 else 0), y - s * 0.12, s * 1.2, s * 0.24, "#2a3a6a", a)
            rect(c, x + sg * s * 0.25 - (s * 1.2 if sg < 0 else 0), y - s * 0.12, s * 1.2, s * 0.24, "#9aa4c8", a, stroke=s * 0.03)
    circle(c, x, y - s * 0.32, s * 0.12, "#ffffff", a)

def gulf_map(c, rect_, u, impact_a=1.0, shelf_a=1.0, t=0.0):
    geo.draw_map(c, GULF, rect_, land="#c9b98a", sea="#1a4f9a", outline_w=2 * u)
    if shelf_a > 0:
        pts = [(-92.2, 19.5), (-92.6, 21.0), (-91.8, 22.6), (-90, 23.7), (-88, 23.6), (-86.6, 22.5), (-86.7, 21.3)]
        c.save(); c.clipRect(skia.Rect.MakeXYWH(*rect_))
        c.drawPath(poly([geo.lonlat_xy(lo, la, GULF, rect_) for lo, la in pts]), paint("#4fb6d8", 0.55 * shelf_a))
        c.drawPath(geo.land_path(GULF, rect_), paint("#c9b98a"))
        c.drawPath(geo.land_path(GULF, rect_), paint("#0b1030", 0.35, stroke=2 * u))
        c.restore()
    if impact_a > 0:
        x, y = geo.lonlat_xy(*IMPACT, GULF, rect_)
        circle(c, x, y, (22 + 6 * math.sin(t * 4)) * u, "#ff4d4d", impact_a * 0.35)
        circle(c, x, y, 12 * u, "#ff4d4d", impact_a); circle(c, x, y, 12 * u, "#ffffff", impact_a, stroke=3 * u)
    return rect_

def burst(c, x, y, r, p, a=1.0):
    if p <= 0 or p >= 1: return
    circle(c, x, y, r * eout(p), "#fff3c4", a * (1 - p) ** 0.6, blur=r * 0.2)
    circle(c, x, y, r * 0.6 * eout(p), "#ffffff", a * (1 - p))

# ---------------- scenes ----------------
def b_plain(c, W, H, t, S):
    u = S.u; o = S.opts; B = beats(S, 3)
    outro = o.get("outro")
    hy = 0.33 if S.P else 0.55
    cretaceous_bg(c, W, H, t, u, hy=hy, dusk=0.6 if outro else 0.35)
    gy = (hy + 0.14) * H
    for k, (fx, sc_) in enumerate([(0.25, 1.0), (0.62, 1.4)] if not S.P else [(0.3, 0.9), (0.7, 1.2)]):
        x = (fx * W + t * (12 if k == 0 else -6) * u) % (W * 1.1)
        if k == 0: trex(c, x, gy, 120 * u * sc_, t)
        else: sauropod(c, x, gy, 130 * u * sc_, t=t)
    for k in range(2): pterosaur(c, W * (0.2 + 0.4 * k) + t * 25 * u, (0.12 + 0.05 * k) * H, 40 * u, t + k)
    if not outro:
        p = prog(t, 0.0, S.dur)
        ax, ay = lerp(W * 0.9, W * 0.62, p), lerp(0.05 * H, 0.18 * H, p)
        asteroid(c, ax, ay, (14 + 10 * p) * u, t, trail=1.0, ang=-35 + 180 + 10, glow=0.5)
        if S.n() >= 3:
            chip(c, "~10 KM WIDE", ax - 40 * u, ay + 80 * u, vis(t, B(0, 0.2), B(1, 0)), 34 * u, dot="#ffb347")
            chip(c, "WHERE IT LANDED", W / 2, 0.85 * H, vis(t, B(1, 0.45), B(2, 0)), 40 * u, bg=ACCENT, fg="#0b1030", a=1)
            pc = prog(t, B(2, 0.2), 0.4)
            if pc > 0:
                clock(c, W / 2, 0.83 * H, 70 * u, ease(prog(t, B(2, 0.2), 2.5)) * 0.5, a=pc)
                text(c, "+30 SECONDS", W / 2 + 110 * u, 0.83 * H, 54 * u, ACCENT, pc, w=900, align="l", shadow=10)
        elif S.P:
            chip(c, "66 MILLION YEARS AGO", W / 2, 0.27 * H, vis(t, 0.3), 36 * u)
    else:
        B2 = beats(S, 2)
        big_text(c, W, H, "30 SECONDS", 0.3 * H, prog(t, B2(1, 0.1), 0.4), u, colr=ACCENT, size=150)
        chip(c, "THAT NEVER HAPPENED", W / 2, 0.42 * H, prog(t, B2(1, 0.4), 0.4), 40 * u)
    hook_text(c, W, H, t, S, y=0.2)

def _orbit_geom(W, H, u):
    return W * 0.08, H * 1.9, H * 1.55  # sun x, sun y (off-screen below), orbit radius

def b_orbit(c, W, H, t, S):
    u = S.u; o = S.opts; move = o.get("move"); B = beats(S, 2 if move else 1)
    space_bg(c, W, H, t, 1, seed=21)
    sx, sy, R = -0.3 * W, 0.55 * H, 0.8 * W
    c.drawCircle(-0.02 * W, sy, 420 * u, paint(shader=rad(-0.02 * W, sy, 420 * u, [(0, "#ffd166", 0.55), (1, "#ff6b35", 0)])))
    sun(c, -0.06 * W, sy, 160 * u, t, glow=0.5)
    c.drawCircle(sx, sy, R, paint("#ffffff", 0.3, stroke=3 * u, dash=([14 * u, 10 * u], 0)))
    a0 = 9.0
    da = (18 * ease(prog(t, B(1, 0.15), max(1, B(1, 0.9) - B(1, 0.15))))) if move else 0
    drift = (2 * ease(prog(t, B(0, 0.2), 2.5))) if move else 0
    def P(a): return sx + math.cos(math.radians(a)) * R, sy + math.sin(math.radians(a)) * R
    ex, ey = P(a0 - drift)
    if move and da > 0:
        p = skia.Path(); p.addArc(skia.Rect.MakeXYWH(sx - R, sy - R, 2 * R, 2 * R), a0 - drift - da, da)
        c.drawPath(p, paint(ACCENT, 1, stroke=10 * u))
        geo.globe(c, ex, ey, int(90 * u), rot=-90, tilt=20, a=0.3)
        mx, my = P(a0 - drift - da / 2)
        text(c, "~900 KM IN 30 S", mx - 60 * u, my - 40 * u, 46 * u, ACCENT, 1, w=900, align="r", shadow=8)
        ex, ey = P(a0 - drift - da)
    if move:
        arrow(c, ex + 30 * u, ey - 150 * u, ex + 10 * u, ey - 260 * u, "#7ec8ff", 8 * u, vis(t, B(0, 0.2)))
    geo.globe(c, ex, ey, int(110 * u), rot=-90 + t * 20, tilt=20)
    tx, ty = P(a0)
    tx += 80 * u; ty -= 60 * u
    aq = ease(prog(t, 0.4, 2.0)) * 0.92
    line(c, W * 0.98, 0.0 * H, tx, ty, "#ffb347", 4 * u, 0.5, dash=([16 * u, 12 * u], -t * 40))
    asteroid(c, lerp(W * 0.98, tx, aq), lerp(0.0, ty, aq), 22 * u, t, trail=0.8, ang=-35 + 180 + 8, glow=0.4)
    if not move:
        chips(c, t, [(S.lt(0, 0.15), None, "SAME ASTEROID", "#ffb347"), (S.lt(0, 0.3), None, "SAME SPEED", "#ffb347"),
                     (S.lt(0, 0.45), None, "SAME PATH", "#ffb347")], W * 0.72, 0.55 * H, 80 * u, u, 34, align="l")
        pc = prog(t, S.lt(0, 0.65), 0.4)
        if pc > 0:
            clock(c, W * 0.88, 0.22 * H, 90 * u, ease(prog(t, S.lt(0, 0.65), 2)) * 0.5, a=pc)
            text(c, "30 S LATE", W * 0.88, 0.22 * H + 140 * u, 56 * u, ACCENT, pc, w=900)
    else:
        chip(c, "EARTH: ~30 KM/S AROUND THE SUN", W * 0.3, 0.1 * H, vis(t, B(0, 0.2)), 38 * u, dot="#7ec8ff")
        chip(c, "A LATE ASTEROID HITS A DIFFERENT SPOT", W / 2, 0.92 * H, vis(t, B(1, 0.6)), 36 * u, bg=ACCENT, fg="#0b1030", a=1)

def b_everest(c, W, H, t, S):
    u = S.u; B = beats(S, 1)
    fill_bg(c, W, H, "#7fb8e6", "#dcefff")
    gy = 0.82 * H; km = 0.062 * H
    rect(c, 0, gy, W, H - gy, "#6a7a5a")
    ex = W * 0.3
    p_m = poly([(ex - 300 * u, gy), (ex - 80 * u, gy - 6 * km), (ex, gy - 8.85 * km), (ex + 60 * u, gy - 7.6 * km), (ex + 320 * u, gy)])
    c.drawPath(p_m, paint("#7a8a9a")); c.drawPath(poly([(ex - 70 * u, gy - 6.6 * km), (ex, gy - 8.85 * km), (ex + 50 * u, gy - 7.7 * km), (ex - 10 * u, gy - 7.3 * km)]), paint("#ffffff"))
    text(c, "EVEREST  8.8 KM", ex, gy + 50 * u, 38 * u, "#0b1030", 1, w=900)
    pa = eout(prog(t, 0.3, 1.0))
    axx = W * 0.62
    asteroid(c, axx, gy - 5 * km - (1 - pa) * H, 5 * km, t * 0.2, a=1)
    text(c, "ASTEROID ~10 KM", axx, gy + 50 * u, 38 * u, "#0b1030", pa, w=900)
    lx = axx + 5 * km + 60 * u
    line(c, lx, gy, lx, gy - 10 * km, "#0b1030", 5 * u, pa); text(c, "10 KM", lx + 20 * u, gy - 5 * km, 40 * u, "#0b1030", pa, w=900, align="l")
    ps = vis(t, S.lt(0, 0.6))
    if ps > 0:
        rrect(c, W * 0.5, 0.06 * H, W * 0.46, 0.26 * H, 30 * u, "#0b1030", 0.85 * ps)
        text(c, "RIFLE BULLET  ~1 KM/S", W * 0.53, 0.12 * H, 32 * u, "#ffffff", ps, w=800, align="l", fam="Inter")
        bar(c, W * 0.53, 0.15 * H, W * 0.38, 22 * u, 0.06 * ps, "#cfd8e3", u)
        text(c, "ASTEROID  ~20 KM/S", W * 0.53, 0.22 * H, 32 * u, ACCENT, ps, w=800, align="l", fam="Inter")
        bar(c, W * 0.53, 0.25 * H, W * 0.38, 22 * u, ease(prog(t, S.lt(0, 0.7), 1.0)) * ps, ACCENT, u)

def b_gulfmap(c, W, H, t, S):
    u = S.u; B = beats(S, 3)
    dark_bg(c, W, H, "#081226", "#0f1f3a")
    if S.P: rr = geo.map_rect(GULF, W / 2, 0.38 * H, width=W * 0.98)
    else: rr = geo.map_rect(GULF, W / 2, 0.52 * H, height=H * 0.86)
    gulf_map(c, rr, u, t=t)
    ix, iy = geo.lonlat_xy(*IMPACT, GULF, rr)
    chip(c, "IMPACT SITE", ix, iy + 50 * u, vis(t, 0.3), 30 * u, bg="#ff4d4d")
    alts = [(-93.5, 25.2), (-84.6, 19.2)]
    pa = prog(t, B(0, 0.45), 0.6)
    for k, (lo, la) in enumerate(alts):
        x, y = geo.lonlat_xy(lo, la, GULF, rr)
        q = prog(t, B(0, 0.45) + k * 0.4, 0.6)
        line(c, ix, iy, lerp(ix, x, eout(q)), lerp(iy, y, eout(q)), "#ffffff", 4 * u, q, dash=([12 * u, 10 * u], -t * 30))
        circle(c, x, y, 14 * u, "#7ec8ff", q); circle(c, x, y, 14 * u, "#ffffff", q, stroke=3 * u)
    chip(c, "30 S EARLIER OR LATER: DEEP OCEAN?", W / 2, (0.12 if S.P else 0.07) * H if not S.P else 0.62 * H - 140 * u,
         vis(t, B(0, 0.6), B(1, 0) if S.n() >= 3 else None), 32 * u, dot="#7ec8ff")
    chip(c, "SHALLOW, SULFUR-RICH SEAFLOOR", ix, iy - 60 * u, vis(t, B(1, 0.05) if S.n() >= 3 else 99, B(2, 0)), 30 * u, dot="#4fb6d8")
    if S.n() >= 3:
        chip(c, "EXACT NUMBERS: DEBATED", W * 0.2, 0.93 * H, vis(t, B(1, 0.1)), 30 * u)
        chip(c, "AN UNUSUALLY BAD SPOT", W * 0.8, 0.93 * H, vis(t, B(1, 0.45)), 30 * u, bg="#ff4d4d")
    chip(c, "ILLUSTRATIVE", rr[0] + rr[2] - 100 * u, rr[1] + 30 * u, 0.8 * pa, 20 * u)

def b_impact(c, W, H, t, S):
    u = S.u; B = beats(S, 2); ti = 1.0
    shake = (1 - prog(t, ti, 2.5)) * (t > ti) * 14 * u
    c.save(); c.translate(math.sin(t * 60) * shake, math.cos(t * 47) * shake)
    fill_bg(c, W, H, "#0b1a3a", "#4f7fb8")
    hy = 0.62 * H
    c.drawRect(skia.Rect.MakeLTRB(0, hy, W, H), paint(shader=lin(0, hy, 0, H, [(0, "#2f86b8", 1), (1, "#0f3a5a", 1)])))
    c.drawPath(poly([(W * 0.55, hy), (W * 0.62, hy - 30 * u), (W, hy - 40 * u), (W, hy)]), paint("#c9b98a"))
    ix, iy = W * 0.42, hy + 10 * u
    pa = prog(t, 0, ti)
    if t < ti:
        asteroid(c, lerp(W * 1.05, ix, ein(pa) * 0.6 + pa * 0.4), lerp(-0.1 * H, iy, ein(pa) * 0.6 + pa * 0.4), 40 * u, t, trail=1.0, ang=140, glow=0.8)
    else:
        q = prog(t, ti, 6.0)
        for k in range(3):
            r = (0.2 + 0.4 * k) * W * eout(q)
            oval(c, ix, iy, r, r * 0.12, "#ffffff", 0.6 * (1 - q), stroke=8 * u)
        h = 0.62 * H * eout(q); wt = (120 + 520 * eout(q)) * u
        c.drawPath(poly([(ix - 70 * u, iy), (ix - wt, iy - h), (ix - wt * 0.75, iy - h * 1.02), (ix, iy - h * 0.25),
                         (ix + wt * 0.75, iy - h * 1.02), (ix + wt, iy - h), (ix + 70 * u, iy)]),
                   paint(shader=lin(0, iy - h, 0, iy, [(0, "#ffd166", 0.0), (0.4, "#ff9a3a", 0.75), (1, "#ff5a1a", 1.0)]), blur=10 * u))
        for k in range(40):
            rng = random.Random(k + 40); sg = rng.choice((-1, 1)); f = rng.random()
            circle(c, ix + sg * (70 * u + (wt - 70 * u) * f) + rng.uniform(-30, 30) * u, iy - h * f + rng.uniform(-20, 20) * u, rng.uniform(4, 10) * u, "#3a2a1e", 0.8 * (1 - q))
        circle(c, ix, iy - 40 * u, 260 * u * eout(q) + 1, "#ffb347", 0.75 * (1 - q * 0.5), blur=60 * u)
        circle(c, ix, iy - 20 * u, 110 * u * eout(q) + 1, "#fff3c4", 0.9 * (1 - q * 0.6), blur=20 * u)
        for k in range(30):
            rng = random.Random(k); an = rng.uniform(-170, -10); sp = rng.uniform(0.3, 1)
            d = q * sp * W * 0.5
            circle(c, ix + math.cos(math.radians(an)) * d, iy + math.sin(math.radians(an)) * d * 0.8 + q * q * 200 * u, 6 * u, "#ffb347", 1 - q)
    burst(c, ix, iy, W * 0.9, prog(t, ti, 1.2))
    c.restore()
    chip(c, "CHICXULUB, YUCATÁN", W / 2, 0.1 * H, vis(t, B(0, 0.45)), 40 * u, dot="#ff4d4d")
    pb = prog(t, B(1, 0.1), 0.5)
    if pb > 0:
        rrect(c, W / 2 - 480 * u, 0.74 * H, 960 * u, 0.2 * H, 30 * u, "#0b1030", 0.85 * pb)
        text(c, "1,000,000,000 ×", W / 2, 0.8 * H, 76 * u, ACCENT, pb, w=900)
        text(c, "THE HIROSHIMA + NAGASAKI BOMBS", W / 2, 0.88 * H, 36 * u, "#ffffff", pb, w=800)

def b_crater(c, W, H, t, S):
    u = S.u; B = beats(S, 3)
    fill_bg(c, W, H, "#ffb37a", "#ffd9b0")
    gy = 0.35 * H
    cols = ["#c9a36a", "#b58a55", "#9a7046", "#7a5a3a", "#5a4430"]
    for k in range(5): rect(c, 0, gy + k * 0.13 * H, W, 0.13 * H, cols[k])
    cx = W / 2; Rw = W * 0.36
    dig = ease(prog(t, B(0, 0.1), 2.0)); reb = ease(prog(t, B(1, 0.1), 2.5))
    depth = 0.5 * H * dig * (1 - 0.65 * reb)
    p = skia.Path(); p.moveTo(cx - Rw, gy)
    p.cubicTo(cx - Rw * 0.6, gy + depth, cx - Rw * 0.2, gy + depth, cx, gy + depth - 0.12 * H * reb)
    p.cubicTo(cx + Rw * 0.2, gy + depth, cx + Rw * 0.6, gy + depth, cx + Rw, gy); p.close()
    c.drawPath(p, paint("#ffcf9a"))
    if reb > 0:
        for sg in (-1, 1):
            x = cx + sg * Rw * 0.32
            c.drawPath(poly([(x - 60 * u, gy + depth * 0.95), (x, gy + depth * 0.95 - 90 * u * reb), (x + 60 * u, gy + depth * 0.95)]), paint("#9a7046"))
    c.drawPath(p, paint("#ff7a1a", 0.6 * (1 - reb), stroke=6 * u))
    if dig > 0.2 and reb < 0.5:
        line(c, cx + Rw * 0.5, gy, cx + Rw * 0.5, gy + depth, "#0b1030", 5 * u, 1 - reb * 2)
        text(c, "~30 KM DEEP", cx + Rw * 0.5 + 20 * u, gy + depth * 0.5, 40 * u, "#0b1030", (1 - reb * 2) * dig, w=900, align="l")
        chip(c, "~20 SECONDS AFTER IMPACT", cx, 0.12 * H, vis(t, B(0, 0.45), B(1, 0)), 36 * u)
    pw = vis(t, B(0, 0.2))
    line(c, cx - Rw, gy - 50 * u, cx + Rw, gy - 50 * u, "#0b1030", 5 * u, pw)
    for sg in (-1, 1): line(c, cx + sg * Rw, gy - 70 * u, cx + sg * Rw, gy - 30 * u, "#0b1030", 5 * u, pw)
    text(c, "~180 KM ACROSS", cx, gy - 90 * u, 44 * u, "#0b1030", pw, w=900)
    chip(c, "ROCK REBOUNDS INTO A RING OF MOUNTAINS", cx, 0.12 * H, vis(t, B(1, 0.2), B(2, 0)), 34 * u)
    pf = phase(t, B(2, 0))
    if pf > 0:
        for k in range(4): flame(c, W * (0.04 + 0.04 * k), gy, 80 * u, t, seed=k, a=pf)
        for k in range(4): flame(c, W * (0.84 + 0.04 * k), gy, 70 * u, t, seed=k + 5, a=pf)
        wx = lerp(W * 0.95, cx + Rw * 0.3, ease(prog(t, B(2, 0.4), 2)))
        p2 = skia.Path(); p2.moveTo(wx - 140 * u, gy); p2.quadTo(wx, gy - 160 * u, wx + 60 * u, gy - 40 * u); p2.lineTo(wx + 300 * u, gy); p2.close()
        c.drawPath(p2, paint("#3f8fd1", pf))
        chip(c, "FIRES + TSUNAMI, WITHIN A DAY", cx, 0.12 * H, vis(t, B(2, 0.1)), 36 * u, bg="#ff4d4d")

def b_layers(c, W, H, t, S):
    u = S.u; B = beats(S, 2)
    top = (0.22 if S.P else 0.45) * H
    fill_bg(c, W, H, "#7ab3e0", "#d0e8f7")
    seah = 60 * u
    layers = [("#2f86b8", seah, "SHALLOW SEA"), ("#e8dcc0", 70 * u, "LIMESTONE"), ("#f2d45a", 90 * u, "GYPSUM: RICH IN SULFUR"),
              ("#2a2420", 80 * u, "CARBON-RICH SEDIMENT"), ("#8a6a4a", H, "")]
    y = top
    for k, (colr, h, lab) in enumerate(layers):
        rect(c, 0, y, W, h, colr)
        if lab and k > 0:
            chip(c, lab, W * 0.05, y + h / 2, vis(t, B(0, 0.25 + 0.15 * k) if S.n() >= 2 else 0.2 + 0.4 * k), 30 * u, align="l",
                 dot=colr if k != 1 else "#e8dcc0")
        y += h
    pb = phase(t, B(1, 0) if S.n() >= 2 else S.lt(0, 0.45))
    if pb > 0:
        ix = W * 0.62
        rng = random.Random(4)
        q = (t - (B(1, 0) if S.n() >= 2 else S.lt(0, 0.45)))
        for k in range(90):
            ph = (rng.random() * 0.6 + q * rng.uniform(0.25, 0.5)) % 1.2
            if ph > 1: continue
            an = math.radians(rng.uniform(-125, -55)); d = ph * top * 1.4
            colr = "#f2d45a" if k % 2 else "#1a1a1e"
            circle(c, ix + math.cos(an) * d, top - 20 * u + math.sin(an) * d, rng.uniform(6, 14) * u, colr, pb * (1 - ph * 0.6))
        c.drawPath(poly([(ix - 90 * u, top + 260 * u), (ix - 260 * u, top), (ix + 260 * u, top), (ix + 90 * u, top + 260 * u)]), paint("#ffb347", pb * 0.9))
        circle(c, ix, top, 160 * u, "#fff3c4", pb * 0.6, blur=40 * u)
        chip(c, "BLASTED INTO THE SKY", ix, (0.16 if S.P else 0.12) * H, pb, 36 * u, bg="#ff4d4d")

def b_haze(c, W, H, t, S):
    u = S.u; B = beats(S, 2)
    space_bg(c, W, H, t, 1, seed=22)
    hz = ease(prog(t, B(0, 0.1), 3)) * 0.55
    gx, gy, R = W * 0.42, 0.52 * H, 320 * u
    geo.globe(c, gx, gy, int(R), rot=-90 + t * 3, tilt=15, haze=hz, light=(-0.75, 0.35, 0.55))
    circle(c, gx, gy, R * 1.06, "#d9c27a", 0.5 * hz / 0.55, stroke=26 * u, blur=10 * u)
    for k in range(5):
        y = gy - R * 0.7 + k * R * 0.35
        q = (t * 0.4 + k * 0.2) % 1
        x0 = -0.05 * W; xh = gx - R * 1.1 - 10 * u
        x = lerp(x0, xh, min(q * 2, 1)); a_ = vis(t, B(0, 0.2))
        line(c, x0, y, x, y, "#ffd166", 8 * u, a_ * 0.8)
        if q > 0.5:
            xb = lerp(xh, x0 + 100 * u, (q - 0.5) * 2)
            arrow(c, xh, y, xb, y - (q - 0.5) * 200 * u, "#ffd166", 6 * u, a_ * 0.7)
    chip(c, "SULFUR HAZE REFLECTS SUNLIGHT", W * 0.42, 0.08 * H, vis(t, B(0, 0.2)), 36 * u, dot="#d9c27a")
    chip(c, "+ SOOT", W * 0.42, 0.93 * H, vis(t, B(0, 0.65)), 34 * u, dot="#1a1a1e")
    temp = lerp(20, 10, ease(prog(t, B(1, 0.1), 2.5)))
    pt = vis(t, B(1, 0.05))
    thermometer(c, W * 0.8, 0.5 * H, 420 * u, temp, tmax=25, tmin=0, a=pt, label=False)
    text(c, "−8 TO −11 °C", W * 0.8, 0.14 * H, 54 * u, "#7ec8ff", pt * prog(t, B(1, 0.3), 0.5), w=900)
    text(c, "GLOBAL COOLING (ONE STUDY)", W * 0.8, 0.2 * H, 26 * u, "#cfe3ff", pt * prog(t, B(1, 0.3), 0.5), w=700, fam="Inter")

def b_collapse(c, W, H, t, S):
    u = S.u; B = beats(S, 2); dark_bg(c, W, H)
    pA = phase(t, None, B(1, 0)); pB = phase(t, B(1, 0))
    with Layer(c, pA) as on:
        if on:
            cx = W * 0.5; base = 0.86 * H
            dim = ease(prog(t, B(0, 0.05), 1.5))
            sun(c, W * 0.85, 0.16 * H, 70 * u, t, a=1 - 0.75 * dim, glow=1 - dim)
            tiers = [("PLANTS + PLANKTON", "#4caf50", 760), ("PLANT-EATERS", "#e0a43a", 540), ("MEAT-EATERS", "#e8443a", 320)]
            for k, (lab, colr, w) in enumerate(tiers):
                fall = ease(prog(t, B(0, 0.35 + 0.15 * k), 0.8))
                y = base - (k + 1) * 150 * u + fall * (k * 40) * u
                cc = mix(colr, "#4a4a55", fall)
                c.save(); c.translate(cx, y + 75 * u); c.rotate(fall * (8 if k % 2 else -8))
                rrect(c, -w / 2 * u, -70 * u, w * u, 140 * u, 20 * u, cc)
                text(c, lab, 0, 0, 40 * u, "#ffffff", 1, w=900)
                c.restore()
            chip(c, "FOOD CHAINS COLLAPSE FROM THE BOTTOM UP", W / 2, 0.1 * H, vis(t, B(0, 0.5)), 34 * u, bg="#ff4d4d")
    with Layer(c, pB) as on:
        if on:
            donut(c, W * 0.25, 0.48 * H, 190 * u, 0.75 * ease(prog(t, B(1, 0.05), 1.2)), "#ff4d4d", label="~75%", sub="OF SPECIES GONE", u=u)
            icons = [("NON-BIRD DINOSAURS", lambda x, y: trex(c, x + 30 * u, y + 60 * u, 90 * u, 0, "#e8eef8", walk=False)),
                     ("PTEROSAURS", lambda x, y: pterosaur(c, x, y, 110 * u, 0.3, "#e8eef8")),
                     ("MARINE REPTILES", lambda x, y: plesiosaur(c, x - 40 * u, y + 20 * u, 110 * u, "#e8eef8")),
                     ("AMMONITES", lambda x, y: ammonite(c, x, y, 60 * u))]
            for k, (lab, fn) in enumerate(icons):
                x = W * (0.5 + 0.22 * (k % 2)) + 60 * u; y = (0.33 + 0.33 * (k // 2)) * H
                p = prog(t, B(1, 0.3 + 0.12 * k), 0.4)
                if p <= 0: continue
                with Layer(c, p): fn(x, y)
                text(c, lab, x, y + 110 * u, 28 * u, "#ffffff", p, w=800)
                xmark(c, x, y, 70 * u, prog(t, B(1, 0.35 + 0.12 * k), 0.3) * 0.8)

def b_globe13(c, W, H, t, S):
    u = S.u; B = beats(S, 4)
    space_bg(c, W, H, t, 1, seed=23)
    gx, gy, R = W * 0.3, 0.52 * H, 330 * u
    rot = -89 + 30 * math.sin(t * 0.15)
    geo.globe(c, gx, gy, int(R), rot=rot, tilt=18)
    x, y, v = geo.globe_xy(*IMPACT, gx, gy, R, rot, 18)
    if v:
        circle(c, x, y, (26 + 8 * math.sin(t * 4)) * u, "#ff4d4d", 0.4); circle(c, x, y, 13 * u, "#ff4d4d"); circle(c, x, y, 13 * u, "#ffffff", 1, stroke=3 * u)
    chip(c, "2017 STUDY: SOOT-RICH ROCK", W * 0.3, 0.08 * H, vis(t, B(0, 0.1)), 32 * u)
    p13 = ease(prog(t, B(1, 0.05), 1.0))
    donut(c, W * 0.72, 0.45 * H, 200 * u, 0.13 * p13, "#ff4d4d", a=vis(t, B(1, 0.0)), label="13%", sub="OF EARTH'S SURFACE", u=u)
    chip(c, "OTHER 87%: PROBABLY NO MASS EXTINCTION", W * 0.72, 0.76 * H, vis(t, B(2, 0.1), B(3, 0)), 30 * u, dot="#7ec8ff")
    chip(c, "CRITICS: SULFUR MAY MATTER MORE THAN SOOT", W * 0.72, 0.76 * H, vis(t, B(3, 0.05)), 28 * u)
    chip(c, "BOTH SIDES: ONLY A FEW SPOTS THIS DEADLY", W * 0.72, 0.85 * H, vis(t, B(3, 0.45)), 28 * u, bg="#ff4d4d")

def b_othercraters(c, W, H, t, S):
    u = S.u; B = beats(S, 3); dark_bg(c, W, H)
    pA = phase(t, None, B(2, 0))
    with Layer(c, pA) as on:
        if on:
            maps = [((-80, 34.5, -72, 40.5), (-76.0, 37.3), "CHESAPEAKE BAY, USA", "~35 MILLION YEARS AGO"),
                    ((6, 46, 15, 51.5), (10.6, 48.9), "RIES, GERMANY", "~15 MILLION YEARS AGO")]
            for k, (bb, (lo, la), lab, when) in enumerate(maps):
                p = prog(t, B(0, 0.2 + 0.35 * k), 0.5)
                if p <= 0: continue
                rr = geo.map_rect(bb, W * (0.27 + 0.46 * k), 0.5 * H, height=0.56 * H)
                with Layer(c, eout(p)):
                    geo.draw_map(c, bb, rr, land="#c9b98a", sea="#1a4f9a", outline_w=2 * u)
                    rrect(c, rr[0], rr[1], rr[2], rr[3], 20 * u, "#ffffff", stroke=4 * u)
                    x, y = geo.lonlat_xy(lo, la, bb, rr)
                    circle(c, x, y, 24 * u, "#ff4d4d", 0.4); circle(c, x, y, 12 * u, "#ff4d4d"); circle(c, x, y, 12 * u, "#ffffff", stroke=3 * u)
                text(c, lab, rr[0] + rr[2] / 2, rr[1] - 50 * u, 40 * u, "#ffffff", eout(p), w=900)
                text(c, when, rr[0] + rr[2] / 2, rr[1] + rr[3] + 45 * u, 30 * u, "#cfe3ff", eout(p), w=700, fam="Inter")
            chip(c, "NO MASS EXTINCTION", W / 2, 0.93 * H, vis(t, B(1, 0.05)), 40 * u, bg="#4cd964", fg="#0b1030", a=1)
    pB = phase(t, B(2, 0))
    with Layer(c, pB) as on:
        if on:
            fill_bg(c, W, H, "#0a2a4a", "#1f5f8f")
            q = prog(t, B(2, 0), S.dur - B(2, 0))
            asteroid(c, lerp(W * 0.9, W * 0.55, q), lerp(0.1 * H, 0.45 * H, q), 40 * u, t, trail=1.0, ang=150, glow=0.6)
            chip(c, "TIMELINE B: DEEP OCEAN", W / 2, 0.85 * H, pB, 44 * u, bg=ACCENT, fg="#0b1030", a=1)

def b_oceanimpact(c, W, H, t, S):
    u = S.u; B = beats(S, 2); ti = 2.0
    shake = (1 - prog(t, ti, 2.5)) * (t > ti) * 12 * u
    c.save(); c.translate(math.sin(t * 60) * shake, math.cos(t * 47) * shake)
    fill_bg(c, W, H, "#16304f", "#6f9ac0")
    hy = 0.6 * H
    c.drawRect(skia.Rect.MakeLTRB(0, hy, W, H), paint(shader=lin(0, hy, 0, H, [(0, "#1f5f8f", 1), (1, "#06203a", 1)])))
    ix = W / 2
    if t < ti:
        pa = prog(t, 0, ti)
        asteroid(c, lerp(W * 1.05, ix, pa), lerp(-0.1 * H, hy, pa), 40 * u, t, trail=1.0, ang=150, glow=0.8)
    else:
        q = prog(t, ti, 8)
        h = 0.55 * H * eout(q)
        col_w = 90 * u + 160 * u * q
        c.drawPath(poly([(ix - col_w, hy), (ix - col_w * 1.6, hy - h), (ix + col_w * 1.6, hy - h), (ix + col_w, hy)]),
                   paint(shader=lin(0, hy - h, 0, hy, [(0, "#f4f8ff", 0.95), (1, "#b8c4d4", 0.95)])))
        for k in range(14):
            rng = random.Random(k)
            circle(c, ix + rng.uniform(-1, 1) * col_w * 2.2, hy - h * rng.uniform(0.85, 1.12), rng.uniform(70, 150) * u * eout(q), "#eef3fa", 0.85, blur=18 * u)
        for k in range(3):
            r = ((q * 2.5 + k * 0.3) % 1) * W * 0.6
            p = skia.Path(); p.moveTo(ix - r - 120 * u, hy + 30 * u); p.quadTo(ix - r, hy - 90 * u * (1 - r / W), ix - r + 80 * u, hy + 30 * u)
            c.drawPath(p, paint("#2f7fbf", 1)); c.drawPath(p, paint("#ffffff", 0.6, stroke=5 * u))
            p2 = skia.Path(); p2.moveTo(ix + r + 120 * u, hy + 30 * u); p2.quadTo(ix + r, hy - 90 * u * (1 - r / W), ix + r - 80 * u, hy + 30 * u)
            c.drawPath(p2, paint("#2f7fbf", 1)); c.drawPath(p2, paint("#ffffff", 0.6, stroke=5 * u))
    burst(c, ix, hy, W * 0.8, prog(t, ti, 1.0))
    c.restore()
    chip(c, "STEAM + SEAFLOOR ROCK", W / 2, 0.08 * H, vis(t, ti + 1.5), 36 * u, dot="#e8eef8")
    chip(c, "MONSTER TSUNAMIS", W / 2, 0.92 * H, vis(t, B(0, 0.75)), 36 * u, bg="#ff4d4d")
    chip(c, "STILL THE WORST DAY IMAGINABLE", W / 2, 0.16 * H, vis(t, B(1, 0.1)), 36 * u, bg="#0b1030")

def b_skyclear(c, W, H, t, S):
    u = S.u; B = beats(S, 3)
    P = S.P
    if P: dark_bg(c, W, H)
    panels = [("REAL: SULFUR + SOOT", 0.85, False), ("30 S LATE: STEAM + ROCK", 0.3, True)]
    for k, (lab, dark, alive) in enumerate(panels):
        if P: rx, ry, rw, rh = 0, (0.08 + 0.27 * k) * H, W, 0.26 * H
        else: rx, ry, rw, rh = k * W / 2, 0, W / 2, H
        c.save(); c.clipRect(skia.Rect.MakeXYWH(rx, ry, rw, rh)); c.translate(rx, ry)
        d = dark * (0.4 + 0.6 * vis(t, 0.2))
        if alive and S.n() >= 3: d *= 1 - 0.6 * ease(prog(t, B(1, 0.4), 3))
        fill_bg(c, rw, rh, mix("#7ab3e0", "#3a3226", d), mix("#d0e8f7", "#5a4a3a", d))
        sun(c, rw * 0.8, rh * 0.2, 40 * u, t, a=1 - d * 0.9, glow=0.4)
        gy = rh * 0.72
        rect(c, 0, gy, rw, rh - gy, mix("#5a8a4a", "#4a3a2a", 1 - alive))
        for j in range(6):
            x = rw * (j + 0.5) / 6
            if alive: tree2(c, x, gy + 10 * u, rh * 0.45, leaf="#2f8f55")
            else:
                line(c, x, gy + 10 * u, x, gy - rh * 0.3, "#3a2a1e", 8 * u)
                line(c, x, gy - rh * 0.2, x + 30 * u, gy - rh * 0.3, "#3a2a1e", 5 * u)
        c.restore()
        chip(c, lab, rx + rw / 2, ry + (0.08 * H if not P else 30 * u), 1, (34 if not P else 30) * u, bg="#ff4d4d" if not alive else "#2f8f55")
    if not P: line(c, W / 2, 0, W / 2, H, "#ffffff", 6 * u)
    if S.n() >= 3:
        chips(c, t, [(B(1, 0.55), None, "FORESTS SURVIVE", "#4cd964"), (B(1, 0.7), None, "PLANKTON SURVIVE", "#4cd964")], W * 0.75, 0.2 * H, 80 * u, u, 32)
        chip(c, "SOME SPECIES STILL DIE OUT", W * 0.75, 0.9 * H, vis(t, B(2, 0.1)), 32 * u, bg="#0b1030")

def b_deccan(c, W, H, t, S):
    u = S.u; B = beats(S, 3); dark_bg(c, W, H)
    bb = (64, 5, 94, 31)
    rr = geo.map_rect(bb, W * 0.3, 0.52 * H, height=0.84 * H)
    geo.draw_map(c, bb, rr, land="#c9b98a", sea="#1a4f9a", outline_w=2 * u)
    dec = [(73.0, 16.0), (72.8, 20.5), (74.5, 22.8), (77.5, 23.6), (80.8, 22.4), (80.5, 19.0), (77.5, 16.5), (75.5, 15.2)]
    pulse = 0.5 + 0.5 * math.sin(t * 2.2)
    c.save(); c.clipRect(skia.Rect.MakeXYWH(*rr))
    c.drawPath(poly([geo.lonlat_xy(lo, la, bb, rr) for lo, la in dec]), paint(mix("#7a1a0a", "#ff5a1a", pulse * 0.6), 0.9 * vis(t, B(0, 0.1))))
    c.restore()
    x, y = geo.lonlat_xy(76.5, 19.5, bb, rr)
    chip(c, "DECCAN TRAPS", x, y, vis(t, B(0, 0.2)), 34 * u, bg="#7a1a0a")
    chip(c, "PULSES OVER HUNDREDS OF THOUSANDS OF YEARS", W * 0.3, 0.06 * H, vis(t, B(0, 0.55)), 26 * u)
    px = W * 0.74
    chips(c, t, [(B(1, 0.1), None, "2020 CLIMATE-MODEL STUDY", "#ffffff"),
                 (B(1, 0.35), None, "ASTEROID ALONE WAS ENOUGH", "#ff4d4d"),
                 (B(1, 0.7), None, "VOLCANOES MAY HAVE HELPED RECOVERY", "#4cd964")], px, 0.28 * H, 95 * u, u, 32)
    pc = prog(t, B(2, 0.2), 0.5)
    if pc > 0:
        rrect(c, px - 330 * u, 0.66 * H, 660 * u, 0.2 * H, 30 * u, "#0b1030", 0.9 * pc)
        text(c, "VOLCANOES ALONE?", px, 0.72 * H, 52 * u, ACCENT, pc, w=900)
        text(c, "MIGHT NOT END THE DINOSAURS", px, 0.8 * H, 32 * u, "#ffffff", pc, w=800)

def b_mammals(c, W, H, t, S):
    u = S.u; o = S.opts; short = o.get("short") or S.n() < 4; B = beats(S, 4)
    hy = 0.33 if S.P else 0.55
    door = 0 if short else phase(t, B(2, 0), B(3, 0))
    shut = 0 if short else phase(t, B(3, 0))
    cretaceous_bg(c, W, H, t, u, hy=hy, dusk=0.2, dark=0.85)
    gy = (hy + 0.14) * H
    trex(c, (W * 0.3 + t * 15 * u) % (W * 1.2), gy, 200 * u, t, "#020308")
    sauropod(c, W * 0.75, gy, 200 * u, "#020308", t=t)
    mx = W * (0.5 if S.P else 0.45); my = gy + 70 * u
    oval(c, mx, my + 20 * u, 120 * u, 40 * u, "#0a0f1a")
    small_mammal(c, mx, my, 70 * u, "#2a2a33")
    chip(c, "DINOSAURS STILL RULE", W / 2, (0.24 if S.P else 0.1) * H, vis(t, B(0, 0.15)), 38 * u, dot="#ff4d4d")
    chip(c, "MAMMALS: SMALL, HIDDEN, NOCTURNAL", W / 2, (0.29 if S.P else 0.18) * H, vis(t, B(1, 0.1) if not short else S.lt(0, 0.5)), 34 * u, dot="#ffe58a")
    if door + shut > 0:
        with Layer(c, max(door, shut)):
            rrect(c, 0, 0, W, H, 0, "#0b1030", 0.8)
            ox, oy = W * 0.18, 0.55 * H
            small_mammal(c, ox, oy, 80 * u, "#8a7a6a")
            text(c, "REAL TIMELINE", ox, oy + 90 * u, 30 * u, "#cfe3ff", 1, w=800)
            icons = [("WHALES", lambda x, y: whale(c, x, y, 150 * u)), ("PRIMATES", lambda x, y: monkey(c, x, y + 60 * u, 150 * u)),
                     ("BATS", lambda x, y: bat(c, x, y, 110 * u, "#9aa4c8")), ("MAMMOTHS", lambda x, y: mammoth(c, x, y + 60 * u, 140 * u))]
            for k, (lab, fn) in enumerate(icons):
                x = W * (0.45 + 0.15 * k); y = (0.32 + 0.36 * (k % 2)) * H
                p = prog(t, B(2, 0.2 + 0.15 * k), 0.4) if not shut else 1
                arrow(c, ox + 100 * u, oy, lerp(ox + 100 * u, x - 100 * u, eout(p)), lerp(oy, y, eout(p)), "#ffffff", 5 * u, p * 0.7 * (1 - shut))
                with Layer(c, p * (1 - 0.75 * shut)): fn(x, y)
                text(c, lab, x, y + 110 * u, 28 * u, "#ffffff", p * (1 - 0.6 * shut), w=800)
            if shut > 0:
                padlock(c, W * 0.66, 0.5 * H, 100 * u, a=shut)
                chip(c, "THIS TIMELINE: THE DOOR STAYS SHUT", W / 2, 0.9 * H, shut, 40 * u, bg="#ff4d4d")

def b_today(c, W, H, t, S):
    u = S.u; B = beats(S, 4)
    p0 = phase(t, None, B(2, 0)); p2 = phase(t, B(2, 0))
    with Layer(c, p0) as on:
        if on:
            cretaceous_bg(c, W, H, t, u, hy=0.55, dusk=0.1)
            for k in range(3): trex(c, W * (0.2 + 0.3 * k) + math.sin(t + k) * 20 * u, 0.69 * H, (110 + 30 * k) * u, t + k, "#2a3a4a")
            for k in range(3):
                text(c, "?", W * (0.25 + 0.25 * k), 0.3 * H + math.sin(t * 2 + k) * 15 * u, (160 + 40 * (k == 1)) * u, ACCENT,
                     prog(t, B(1, 0.1 + 0.15 * k), 0.4), w=900, shadow=14)
            chip(c, "66 MILLION YEARS LATER", W / 2, 0.1 * H, vis(t, B(0, 0.1)), 40 * u)
            chip(c, "EVOLUTION HAS NO SCRIPT", W / 2, 0.9 * H, vis(t, B(1, 0.4)), 36 * u)
    with Layer(c, p2) as on:
        if on:
            dark_bg(c, W, H)
            bx, by = W * 0.12, 0.85 * H
            line(c, bx, by, bx, 0.2 * H, "#9aa4c8", 10 * u)
            fade = ease(prog(t, B(2, 0.4), 2.0))
            br = [(0.3, "RODENTS", "#9aa4c8"), (0.45, "WHALES", "#9aa4c8"), (0.6, "PRIMATES → YOU", ACCENT)]
            for k, (fy, lab, colr) in enumerate(br):
                y = by - (by - 0.2 * H) * fy
                ex = W * (0.42 + 0.12 * k)
                a_ = 1 - fade * 0.85 if k == 2 else 1
                p = skia.Path(); p.moveTo(bx, y); p.quadTo(ex * 0.6, y, ex, y - 0.12 * H)
                c.drawPath(p, paint(colr, a_, stroke=8 * u, dash=([18 * u, 12 * u], 0) if k == 2 and fade > 0.3 else None))
                text(c, lab, ex + 20 * u, y - 0.12 * H, 40 * u, colr, a_, w=900, align="l")
            big_text(c, W, H, "NO PRIMATES. NO PEOPLE.", 0.12 * H, prog(t, B(3, 0.05), 0.4), u, size=80)

def b_birds(c, W, H, t, S):
    u = S.u; B = beats(S, 4)
    fill_bg(c, W, H, "#9fd3ff", "#e6f4ff")
    gy = 0.82 * H; rect(c, 0, gy, W, H - gy, "#7cc56f")
    p1 = prog(t, B(1, 0.1), 0.5)
    trex(c, W * 0.3, gy, 260 * u, t * 0.3, "#3a4a5a", walk=False)
    chicken(c, W * 0.72, gy, 220 * u * eout(p1) + 1, a=p1)
    if p1 > 0:
        arrow(c, W * 0.45, 0.55 * H, lerp(W * 0.45, W * 0.62, eout(p1)), 0.55 * H, "#0b1030", 10 * u, p1, dash=([20 * u, 14 * u], 0))
        text(c, "SAME FAMILY", W * 0.535, 0.5 * H, 34 * u, "#0b1030", p1, w=900)
        chip(c, "BIRDS ARE DINOSAURS", W / 2, 0.15 * H, p1, 44 * u, bg=ACCENT, fg="#0b1030", a=1)
    for k in range(7):
        x = ((t * 0.06 + k * 0.14) % 1.1 - 0.05) * W; y = (0.3 + 0.04 * (k % 3)) * H + math.sin(t * 2 + k) * 10 * u
        bird(c, x, y, 18 * u, t + k, a=vis(t, B(2, 0.2)))
    n = int(11000 * ease(prog(t, B(2, 0.3), 1.5)))
    pc = vis(t, B(2, 0.3), B(3, 0))
    if pc > 0:
        chip(c, f"{n:,}+ SPECIES TODAY", W / 2, 0.25 * H, pc, 40 * u, dot="#4cd964")
        chip(c, "T. REX: CLOSER TO A CHICKEN THAN TO ANY LIZARD", W / 2, 0.92 * H, vis(t, B(2, 0.6), B(3, 0)), 30 * u)
    big_text(c, W, H, "SMALLER, WITH WINGS", 0.92 * H, prog(t, B(3, 0.4), 0.4), u, colr="#ffffff", size=80)

def b_jupiter(c, W, H, t, S):
    u = S.u; B = beats(S, 3)
    pA = phase(t, None, B(1, 0)); pB = phase(t, B(1, 0), B(2, 0)); pC = phase(t, B(2, 0))
    space_bg(c, W, H, t, 1, seed=24)
    with Layer(c, pA) as on:
        if on:
            cx, cy = W * 0.32, 0.5 * H
            sun(c, cx, cy, 45 * u, t)
            for r, colr in ((120, "#7ec8ff"), (420, "#e0a46a")):
                circle(c, cx, cy, r * u, colr, 0.35, stroke=3 * u)
            rng = random.Random(3)
            for k in range(400):
                an = rng.random() * 6.28 + t * 0.03; r = rng.uniform(220, 310) * u
                circle(c, cx + math.cos(an) * r, cy + math.sin(an) * r, 2.2 * u, "#cfd8e3", 0.6)
            ea = t * 0.4; ja = 1.2 + t * 0.05
            geo.globe(c, cx + math.cos(ea) * 120 * u, cy + math.sin(ea) * 120 * u, int(22 * u), rot=t * 30, tilt=10, glow=0.5)
            jx, jy = cx + math.cos(ja) * 420 * u, cy + math.sin(ja) * 420 * u
            circle(c, jx, jy, 46 * u, "#d9a86a")
            for k in range(3): line(c, jx - 42 * u, jy - 15 * u + k * 15 * u, jx + 42 * u, jy - 15 * u + k * 15 * u, "#a8784a", 6 * u)
            text(c, "JUPITER", jx, jy + 75 * u, 28 * u, "#e0a46a", 1, w=800)
            q = ease(prog(t, B(0, 0.1), max(1, B(1, 0) - B(0, 0.1))))
            pts = []
            for i in range(int(q * 80) + 1):
                s_ = i / 80; an = 2.5 + s_ * 7; r = lerp(500, 135, s_ ** 0.8) * u
                pts.append((cx + math.cos(an) * r, cy + math.sin(an) * r))
            if len(pts) > 1: c.drawPath(poly(pts, close=False), paint("#ff7a4d", 0.8, stroke=4 * u, dash=([12 * u, 8 * u], 0)))
            asteroid(c, *pts[-1], 12 * u, t, a=1)
            chips(c, t, [(B(0, 0.15), None, "CARBON-RICH TYPE", "#16161c"), (B(0, 0.3), None, "FORMED BEYOND JUPITER", "#e0a46a"),
                         (B(0, 0.55), None, "PARKED IN THE ASTEROID BELT?", "#cfd8e3")], W * 0.78, 0.3 * H, 95 * u, u, 32)
            chip(c, "2024 STUDY", W * 0.78, 0.18 * H, vis(t, B(0, 0.1)), 28 * u)
    with Layer(c, pB) as on:
        if on:
            x0, x1, y = W * 0.08, W * 0.92, 0.55 * H
            line(c, x0, y, x1, y, "#ffffff", 5 * u)
            span = 230.0
            def X(ma): return lerp(x0, x1, (230 - ma) / span)
            rrect(c, X(230), y - 120 * u, X(66) - X(230), 60 * u, 30 * u, "#4caf50", vis(t, B(1, 0.4)))
            text(c, "DINOSAURS: 160+ MILLION YEARS", (X(230) + X(66)) / 2, y - 90 * u, 34 * u, "#ffffff", vis(t, B(1, 0.4)), w=900)
            for k, ma in enumerate((200, 100, 0)):
                p = prog(t, B(1, 0.1 + 0.1 * k), 0.3)
                circle(c, X(ma), y, 16 * u, "#ff4d4d", p)
            text(c, "BIG HITS: VERY ROUGHLY 1 PER 100 MILLION YEARS", W / 2, y + 80 * u, 34 * u, "#ff9a9a", vis(t, B(1, 0.15)), w=800)
            text(c, "66 MYA", X(66), y + 140 * u, 28 * u, "#cfe3ff", vis(t, B(1, 0.4)), w=700, fam="Inter")
    with Layer(c, pC) as on:
        if on:
            gx, gy, R = W / 2, 0.55 * H, 330 * u
            rot = -89
            geo.globe(c, gx, gy, int(R), rot=rot, tilt=18)
            x, y, v = geo.globe_xy(*IMPACT, gx, gy, R, rot, 18)
            circle(c, x, y, (30 + 8 * math.sin(t * 4)) * u, "#ff4d4d", 0.4); circle(c, x, y, 14 * u, "#ff4d4d")
            chip(c, "ONE OF THE WORST SPOTS ON THE PLANET", W / 2, 0.1 * H, vis(t, B(2, 0.3)), 38 * u, bg="#ff4d4d")

def b_dart(c, W, H, t, S):
    u = S.u; B = beats(S, 3)
    space_bg(c, W, H, t, 1, seed=25)
    pA = phase(t, None, B(1, 0)); pB = phase(t, B(1, 0), B(2, 0)); pC = phase(t, B(2, 0))
    with Layer(c, pA) as on:
        if on:
            cx, cy = W * 0.4, 0.52 * H
            asteroid(c, cx, cy, 150 * u, t * 0.1)
            ti = B(0, 0.45); shrink = ease(prog(t, ti, 1.5))
            rx = lerp(360, 320, shrink) * u; ry = rx * 0.35
            oval(c, cx, cy, rx, ry, "#ffffff", 0.3, stroke=3 * u, dash=([10 * u, 8 * u], 0))
            an = t * 0.7 + 1.0
            mx, my = cx + math.cos(an) * rx, cy + math.sin(an) * ry
            if t < ti:
                pa = prog(t, B(0, 0.1), ti - B(0, 0.1))
                mx0, my0 = cx + math.cos(ti * 0.7 + 1.0) * rx, cy + math.sin(ti * 0.7 + 1.0) * ry
                probe(c, lerp(W * 1.05, mx0, pa), lerp(0.15 * H, my0, pa), 34 * u, kind="dart")
            asteroid(c, mx, my, 36 * u, t * 0.3)
            burst(c, cx + math.cos(ti * 0.7 + 1.0) * rx, cy + math.sin(ti * 0.7 + 1.0) * ry, 260 * u, prog(t, ti, 0.9))
            text(c, "DIDYMOS", cx, cy + 200 * u, 34 * u, "#cfe3ff", 1, w=800)
            chip(c, "DIMORPHOS", mx, my - 70 * u, vis(t, B(0, 0.25)), 28 * u)
            chip(c, "NASA DART · 2022", W * 0.4, 0.1 * H, vis(t, B(0, 0.05)), 38 * u)
            pr = prog(t, ti + 0.6, 0.5)
            if pr > 0:
                rrect(c, W * 0.66, 0.38 * H, W * 0.3, 0.26 * H, 30 * u, "#0b1030", 0.85 * pr)
                text(c, "ORBIT", W * 0.81, 0.44 * H, 36 * u, "#cfe3ff", pr, w=800)
                text(c, "−32 MIN", W * 0.81, 0.54 * H, 90 * u, ACCENT, pr, w=900)
    with Layer(c, pB) as on:
        if on:
            ex, ey = W * 0.2, 0.55 * H
            geo.globe(c, ex, ey, int(130 * u), rot=t * 10, tilt=15)
            nud = ease(prog(t, B(1, 0.3), 2.0))
            line(c, W * 0.95, 0.2 * H, ex + 130 * u, ey - 10 * u, "#ff4d4d", 5 * u, 0.7, dash=([14 * u, 10 * u], 0))
            p = skia.Path(); p.moveTo(W * 0.95, 0.2 * H); p.quadTo(W * 0.6, 0.3 * H, lerp(ex + 130 * u, ex + 60 * u, nud), lerp(ey - 10 * u, ey - 330 * u, nud))
            c.drawPath(p, paint("#4cd964", nud, stroke=6 * u))
            asteroid(c, W * 0.8, 0.24 * H, 26 * u, t)
            arrow(c, W * 0.8, 0.3 * H, W * 0.8 - 40 * u, 0.3 * H - 80 * u, ACCENT, 8 * u, prog(t, B(1, 0.2), 0.4))
            chip(c, "A NUDGE, EARLY ENOUGH", W * 0.62, 0.1 * H, vis(t, B(1, 0.2)), 36 * u, dot=ACCENT)
            chip(c, "DIRECT HIT → NEAR MISS", W * 0.62, 0.9 * H, vis(t, B(1, 0.55)), 36 * u, bg="#4cd964", fg="#0b1030", a=1)
    with Layer(c, pC) as on:
        if on:
            clock(c, W / 2, 0.45 * H, 170 * u, ease(prog(t, B(2, 0.1), 2.5)) * 0.5)
            big_text(c, W, H, "+30 SECONDS", 0.78 * H, prog(t, B(2, 0.3), 0.4), u, colr=ACCENT, size=110)

# ---------------- asteroid-belt Short ----------------
def b_movie(c, W, H, t, S):
    u = S.u
    space_bg(c, W, H, t, 1, seed=26)
    rng = random.Random(6)
    for k in range(70):
        z = (rng.random() + t * 0.35) % 1
        sc = 0.2 + z * 2.0
        x = W / 2 + (rng.random() - 0.5) * W * 1.8 * z; y = 0.4 * H + (rng.random() - 0.5) * H * 0.9 * z
        asteroid(c, x, y, rng.uniform(20, 50) * u * sc, t * rng.uniform(-1, 1) + k, a=min(1, z * 3))
    sx = W / 2 + math.sin(t * 2.3) * 220 * u; sy = 0.42 * H + math.sin(t * 3.1) * 90 * u
    spaceship(c, sx, sy, 70 * u, ang=-90 + math.sin(t * 2.3) * 25)
    chip(c, "MOVIES", W / 2, 0.27 * H, vis(t, 0.5), 44 * u, bg="#ff4d4d")
    hook_text(c, W, H, t, S, y=0.2)

def b_emptybelt(c, W, H, t, S):
    u = S.u; o = S.opts; wide = o.get("wide")
    space_bg(c, W, H, t, 1, seed=27, drift=(-4, 0))
    if not wide:
        y = 0.38 * H
        x0, x1 = W * 0.12, W * 0.88
        asteroid(c, x0, y, 10 * u, t); asteroid(c, x1, y, 8 * u, t + 1)
        p = ease(prog(t, S.lt(0, 0.1), 1.5))
        line(c, x0 + 20 * u, y, lerp(x0 + 20 * u, x1 - 20 * u, p), y, ACCENT, 5 * u, 1, dash=([14 * u, 10 * u], 0))
        text(c, "~1,000,000 KM", W / 2, y - 70 * u, 64 * u, ACCENT, prog(t, S.lt(0, 0.25), 0.4), w=900, shadow=10)
        q = prog(t, S.lt(0, 0.5), 0.6)
        if q > 0:
            y2 = 0.5 * H; Lm = (x1 - x0) / 2.6
            for k in range(3):
                xa = x0 + k * Lm
                if xa + Lm > x1 + 5: Lm2 = x1 - xa
                else: Lm2 = Lm
                geo.globe(c, xa, y2, int(28 * u), rot=t * 20, tilt=10, glow=0.3, a=q)
                circle(c, xa + Lm2, y2, 9 * u, "#cfd8e3", q)
                line(c, xa + 20 * u, y2, xa + Lm2 - 8 * u, y2, "#7ec8ff", 3 * u, q * 0.8)
            text(c, "≈ 2.6 × EARTH–MOON DISTANCE", W / 2, y2 + 60 * u, 36 * u, "#7ec8ff", q, w=800)
    else:
        cx, cy = W / 2, 0.38 * H
        z = lerp(1.0, 0.35, ease(t / S.dur))
        sun(c, cx, cy, 30 * u, t, glow=0.5)
        rng = random.Random(8)
        for k in range(420):
            an = rng.random() * 6.28 + t * 0.02; r = rng.uniform(300, 430) * u * z * 1.6
            circle(c, cx + math.cos(an) * r, cy + math.sin(an) * r * 0.9, 3.2 * u, "#cfd8e3", 0.85)
        circle(c, cx, cy, 120 * u * z * 1.6, "#7ec8ff", 0.4, stroke=2 * u)
        text(c, "ASTEROID BELT", cx, cy + 470 * u * z * 1.6 * 0.9 + 40 * u, 34 * u, "#cfd8e3", 1, w=800) if z > 0.6 else None
        chip(c, "MORE DESERT THAN MINEFIELD", W / 2, 0.24 * H, vis(t, S.lt(0, 0.4)), 38 * u)

def b_probe(c, W, H, t, S):
    u = S.u
    space_bg(c, W, H, t, 1, seed=28, drift=(-20, 0))
    rng = random.Random(9)
    for k in range(10):
        x = (rng.random() * W * 1.3 - t * 15 * u) % (W * 1.3) - 0.15 * W; y = rng.uniform(0.15, 0.58) * H
        circle(c, x, y, 3 * u, "#cfd8e3", 0.8)
    probe(c, W / 2, 0.4 * H + math.sin(t) * 10 * u, 190 * u, kind="lucy")
    chip(c, "NASA LUCY", W / 2, 0.27 * H, vis(t, S.lt(0, 0.05)), 40 * u)
    chip(c, "NO DODGING NEEDED", W / 2, 0.53 * H, vis(t, S.lt(0, 0.4)), 38 * u, bg="#4cd964", fg="#0b1030", a=1)

def b_beltmass(c, W, H, t, S):
    u = S.u
    space_bg(c, W, H, t, 1, seed=29)
    mx, my, R = W * 0.36, 0.38 * H, 230 * u
    moon(c, mx, my, R)
    text(c, "OUR MOON", mx, my + R + 40 * u, 36 * u, "#ffffff", 1, w=800)
    p = ease(prog(t, S.lt(0, 0.15), 1.2))
    r2 = R * (0.035 ** (1 / 3))
    ax, ay = W * 0.78, my + R - r2
    if p > 0:
        rng = random.Random(10)
        for k in range(18):
            an = rng.random() * 6.28; d = rng.random() * r2 * 0.8
            asteroid(c, ax + math.cos(an) * d, ay + math.sin(an) * d * 0.7, rng.uniform(0.25, 0.45) * r2 * p, k)
        text(c, "EVERY ASTEROID", ax, my + R + 40 * u, 36 * u, "#ffffff", p, w=800)
        text(c, "≈ 3–4% OF THE MOON'S MASS", W / 2, 0.15 * H + 30 * u, 44 * u, ACCENT, p, w=900, shadow=8) if not S.P else \
            chip(c, "≈ 3–4% OF THE MOON'S MASS", W / 2, 0.25 * H, p, 38 * u, bg=ACCENT, fg="#0b1030", a=1)
    q = prog(t, S.lt(0, 0.6), 0.5)
    if q > 0:
        circle(c, ax, ay - r2 * 2.6, r2 * 0.75, "#9aa4b8", q)
        text(c, "CERES ≈ 1/3", ax, ay - r2 * 2.6 - r2 - 30 * u, 34 * u, ACCENT, q, w=900)

SCENES = {k: v for k, v in globals().items() if k.startswith("b_") and callable(v)}
