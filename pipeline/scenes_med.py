"""Scenes: What If the Mediterranean Dried Up? (+ Mediterranean and AMOC Shorts)."""
from common2 import *
import geo

MED = (-6.5, 29.5, 37, 46.5)
SEA = "#1f6fd1"; LAND = "#d9c48a"; SALT = "#f3efe4"
GIB = (-5.6, 35.95)
NATL = (-85, -2, 32, 74)

def med_rect(S, cy=None, wfrac=0.94):
    W, H = S.W, S.H
    if S.P: return geo.map_rect(MED, W / 2, cy or 0.36 * H, width=W * 0.99)
    return geo.map_rect(MED, W / 2, cy or 0.52 * H, width=W * wfrac)

def med_map(c, rr, dry=0.0, u=1.0, salt=SALT, sea=SEA, land=LAND, extra=None, bbox=MED):
    """dry: 0..1 fraction of map width used as the salt rim (sea shrinking)."""
    MED_ = bbox
    geo.draw_map(c, MED_, rr, land=land, sea=sea, outline_w=2 * u)
    if dry > 0:
        X, Y, Wd, Hd = rr
        path = geo.land_path(MED_, rr)
        c.save(); c.clipRect(skia.Rect.MakeXYWH(*rr))
        for bb in [(-7, 29, -5.55, 47), (27.2, 40.75, 42, 48), (32.4, 25, 40, 31.3)]:
            x0, y1 = geo.lonlat_xy(bb[0] if bb[0] > -7 else -60, bb[1], MED_, rr); x1, y0 = geo.lonlat_xy(bb[2], bb[3], MED_, rr)
            c.clipRect(skia.Rect.MakeLTRB(x0, y0, x1, y1), skia.ClipOp.kDifference)
        c.drawPath(path, paint(salt, 1, stroke=dry * Wd * 2))
        c.drawPath(path, paint("#c9b48a", 0.5, stroke=dry * Wd * 2 * 0.15 + 2))
        c.restore()
        c.save(); c.clipRect(skia.Rect.MakeXYWH(*rr))
        c.drawPath(path, paint(land))
        c.drawPath(path, paint("#0b1030", 0.35, stroke=2 * u))
        c.restore()
    if extra:
        c.save(); c.clipRect(skia.Rect.MakeXYWH(*rr)); extra(c, rr); c.restore()

def pin(c, x, y, u, colr="#ff4d4d", a=1.0, t=0.0):
    circle(c, x, y, (22 + 5 * math.sin(t * 4)) * u, colr, 0.35 * a); circle(c, x, y, 11 * u, colr, a); circle(c, x, y, 11 * u, "#ffffff", a, stroke=3 * u)

def evap(c, x0, x1, ybase, t, u, a=1.0, n=10, rise=220):
    for k in range(n):
        q = (t * 0.35 + k / n) % 1
        x = lerp(x0, x1, (k + 0.5) / n) + math.sin(q * 6 + k) * 14 * u
        y = ybase - q * rise * u
        p = skia.Path(); p.moveTo(x, y)
        for j in range(4): p.quadTo(x + (12 if j % 2 else -12) * u, y - (j + 0.5) * 14 * u, x, y - (j + 1) * 14 * u)
        c.drawPath(p, paint("#ffffff", a * 0.7 * math.sin(q * math.pi), stroke=4 * u))

def boat(c, x, y, s, a=1.0, colr="#ffffff"):
    c.drawPath(poly([(x - s, y - s * 0.25), (x + s, y - s * 0.25), (x + s * 0.7, y + s * 0.12), (x - s * 0.7, y + s * 0.12)]), paint(colr, a))
    rect(c, x - s * 0.05, y - s * 1.2, s * 0.08, s, "#5b3e2a", a)
    c.drawPath(poly([(x + s * 0.05, y - s * 1.15), (x + s * 0.65, y - s * 0.35), (x + s * 0.05, y - s * 0.35)]), paint("#f4ead8", a))

def med_town(c, W, x0, x1, base, u, a=1.0, seed=3):
    rng = random.Random(seed); x = x0
    while x < x1:
        w = rng.uniform(70, 130) * u; h = rng.uniform(60, 160) * u
        rect(c, x, base - h, w, h, rng.choice(["#f4ead8", "#ffffff", "#f2d7b0", "#e9e2d0"]), a)
        for k in range(int(w / (34 * u))):
            rect(c, x + 12 * u + k * 34 * u, base - h + 20 * u, 14 * u, 20 * u, "#4f7fb8", a)
        if rng.random() < 0.4: c.drawPath(poly([(x - 6 * u, base - h), (x + w / 2, base - h - 30 * u), (x + w + 6 * u, base - h)]), paint("#c9653a", a))
        x += w + rng.uniform(4, 16) * u

def sub(c, x, y, s, a=1.0, colr="#2a3344"):
    rrect(c, x - s, y - s * 0.16, s * 2, s * 0.32, s * 0.16, colr, a)
    rrect(c, x - s * 0.15, y - s * 0.42, s * 0.42, s * 0.3, s * 0.06, colr, a)
    line(c, x + s * 0.05, y - s * 0.42, x + s * 0.05, y - s * 0.6, colr, s * 0.04, a)

# ---------------- scenes ----------------
def c_harbor(c, W, H, t, S):
    u = S.u; B = beats(S, 3)
    long_ = S.n() >= 3
    pA = phase(t, None, B(1, 0)) if long_ else 1.0
    with Layer(c, pA) as on:
        if on:
            fill_bg(c, W, H, "#5fb0ff", "#d6efff")
            sun(c, W * 0.8, (0.12 if S.P else 0.15) * H, 70 * u, t)
            hy = (0.4 if S.P else 0.5) * H
            med_town(c, W, -20 * u, W + 20 * u, hy, u)
            c.drawRect(skia.Rect.MakeLTRB(0, hy, W, H), paint(shader=lin(0, hy, 0, H, [(0, "#2f9fd8", 1), (1, "#0b4f8f", 1)])))
            for k in range(4):
                boat(c, W * (0.15 + 0.22 * k) + math.sin(t + k) * 10 * u, hy + (60 + 40 * (k % 2)) * u + math.sin(t * 1.5 + k) * 4 * u, (40 + 10 * (k % 2)) * u)
            evap(c, W * 0.05, W * 0.95, hy + 160 * u, t, u, n=12, rise=260)
            chip(c, "EVAPORATION > RIVERS + RAIN", W / 2, (0.24 if S.P else 0.1) * H, vis(t, B(0, 0.3) if long_ else S.lt(0, 0.35)), 36 * u, dot="#ffffff")
    if long_:
        pB = phase(t, B(1, 0))
        with Layer(c, pB) as on:
            if on:
                bb = (-8.5, 34.6, -3.0, 37.4)
                dark_bg(c, W, H)
                rr = geo.map_rect(bb, W / 2, 0.52 * H, height=0.86 * H)
                geo.draw_map(c, bb, rr, land=LAND, sea=SEA, outline_w=2 * u)
                x0, y0 = geo.lonlat_xy(-5.6, 36.02, bb, rr); x1, y1 = geo.lonlat_xy(-5.6, 35.9, bb, rr)
                line(c, x0, y0 - 6 * u, x1, y1 + 6 * u, ACCENT, 6 * u)
                text(c, "~14 KM", x0 + 20 * u, (y0 + y1) / 2, 44 * u, ACCENT, 1, w=900, align="l", shadow=8)
                for k in range(5):
                    q = (t * 0.4 + k / 5) % 1; xa = lerp(rr[0] + 40 * u, x0 + 140 * u, q)
                    arrow(c, xa - 40 * u, (y0 + y1) / 2, xa + 40 * u, (y0 + y1) / 2, "#9fe0ff", 8 * u, math.sin(q * math.pi))
                tx, ty = geo.lonlat_xy(-4.6, 36.9, bb, rr); text(c, "SPAIN", tx, ty, 40 * u, "#5a4a2a", 1, w=900)
                tx, ty = geo.lonlat_xy(-5.4, 35.0, bb, rr); text(c, "MOROCCO", tx, ty, 40 * u, "#5a4a2a", 1, w=900)
                chip(c, "STRAIT OF GIBRALTAR", W / 2, 0.08 * H, pB, 38 * u, dot=ACCENT)
                text(c, "?", W * 0.82, 0.5 * H, 260 * u, ACCENT, prog(t, B(2, 0.3), 0.4), w=900, shadow=14)
    hook_text(c, W, H, t, S, y=0.2)

def c_strait(c, W, H, t, S):
    u = S.u; B = beats(S, 4); long_ = S.n() >= 4
    top = (0.2 if S.P else 0.3) * H; bot = (0.58 if S.P else 0.9) * H
    fill_bg(c, W, H, "#9fd3ff", "#e6f4ff")
    c.drawRect(skia.Rect.MakeLTRB(0, top, W, bot), paint(shader=lin(0, top, 0, bot, [(0, "#2f86b8", 1), (1, "#0a2a4a", 1)])))
    mid = (top + bot) / 2
    sill = poly([(0, bot), (W * 0.32, bot), (W * 0.45, top + (bot - top) * 0.42), (W * 0.55, top + (bot - top) * 0.42), (W * 0.68, bot), (W, bot), (W, H), (0, H)])
    c.drawPath(sill, paint("#8a6a4a"))
    rect(c, 0, bot, W, H - bot, "#8a6a4a")
    text(c, "ATLANTIC", W * 0.14, top - 40 * u, 44 * u, "#0b1030", 1, w=900)
    text(c, "MEDITERRANEAN", W * 0.84, top - 40 * u, 44 * u, "#0b1030", 1, w=900)
    for k in range(6):  # surface inflow
        q = (t * 0.25 + k / 6) % 1; x = q * W
        arrow(c, x - 60 * u, top + 45 * u, x + 60 * u, top + 45 * u, "#9fe0ff", 12 * u, math.sin(q * math.pi))
    pd = vis(t, B(0, 0.45) if long_ else S.lt(0, 0.4))
    for k in range(5):  # deep outflow
        q = (t * 0.18 + k / 5) % 1; x = W * 0.9 - q * W * 0.9
        y = top + (bot - top) * 0.5 if 0.38 < x / W < 0.62 else top + (bot - top) * 0.62
        arrow(c, x + 60 * u, y, x - 60 * u, y, "#ffb37a", 12 * u, pd * math.sin(q * math.pi))
    chip(c, "ATLANTIC WATER POURS IN", W * 0.3, top + 110 * u, vis(t, B(0, 0.15) if long_ else S.lt(0, 0.2)), 30 * u, dot="#9fe0ff")
    chip(c, "SALTIER, HEAVIER WATER OUT", W * 0.72, top + (bot - top) * 0.82, pd, 30 * u, dot="#ffb37a")
    if not long_:
        chip(c, "GAP: ~14 KM WIDE", W / 2, 0.1 * H + 20 * u, vis(t, S.lt(0, 0.55)), 40 * u, bg=ACCENT, fg="#0b1030", a=1)
        return
    ps = vis(t, B(1, 0.45), B(2, 0))
    sy = top + (bot - top) * 0.42
    line(c, W * 0.5, top, W * 0.5, sy, "#ffffff", 4 * u, ps, dash=([10 * u, 8 * u], 0))
    chip(c, "SILL: ~300 M DOWN", W * 0.5, sy + 60 * u, ps, 30 * u, bg="#0b1030")
    chip(c, "MED: SALTIER THAN THE ATLANTIC", W / 2, 0.1 * H, vis(t, B(1, 0.1), B(2, 0)), 34 * u)
    chip(c, "FULL REFRESH: ~A CENTURY", W / 2, 0.1 * H, vis(t, B(2, 0.1), B(3, 0)), 38 * u, dot=ACCENT)
    pu = phase(t, B(3, 0))
    if pu > 0:
        q = prog(t, B(3, 0), S.dur - B(3, 0))
        sub(c, lerp(W * 0.1, W * 0.8, q), top + 90 * u, 110 * u, a=pu)
        chip(c, "WWII: U-BOATS DRIFTED IN, ENGINES OFF", W / 2, 0.1 * H, vis(t, B(3, 0.1)), 34 * u, dot="#2a3344")

def c_wall(c, W, H, t, S):
    u = S.u
    dark_bg(c, W, H)
    bb = (-7.0, 35.1, -4.2, 36.9)
    rr = geo.map_rect(bb, W / 2, 0.52 * H, height=0.86 * H)
    geo.draw_map(c, bb, rr, land=LAND, sea=SEA, outline_w=2 * u)
    p = ease(prog(t, S.lt(0, 0.25), 1.6))
    x0, y0 = geo.lonlat_xy(-5.62, 36.12, bb, rr); x1, y1 = geo.lonlat_xy(-5.62, 35.82, bb, rr)
    ym = lerp(y0, y1, p)
    shake = math.sin(t * 50) * 3 * u * (0 < p < 1)
    rrect(c, x0 - 34 * u + shake, y0 - 10 * u, 68 * u, ym - y0 + 20 * u, 14 * u, "#7a6a5a")
    for k in range(int(6 * p)):
        rect(c, x0 - 34 * u + shake, y0 + k * (y1 - y0) / 6, 68 * u, 4 * u, "#5a4a3a")
    stamp(c, "SEALED", W * 0.73, 0.3 * H, prog(t, S.lt(0, 0.55), 0.4), u, size=110)
    chips(c, t, [(S.lt(0, 0.4), None, "SOLID ROCK, SPAIN TO MOROCCO", "#7a6a5a"), (S.lt(0, 0.7), None, "EVERYTHING ELSE STAYS THE SAME", "#4cd964")],
          W * 0.28, 0.8 * H, 80 * u, u, 32)

def c_budget(c, W, H, t, S):
    u = S.u; B = beats(S, 4); dark_bg(c, W, H)
    cx, cy = W / 2, 0.6 * H
    bw, bh = 900 * u, 300 * u
    p = skia.Path(); p.moveTo(cx - bw / 2, cy - bh / 2); p.quadTo(cx - bw * 0.45, cy + bh / 2, cx, cy + bh / 2); p.quadTo(cx + bw * 0.45, cy + bh / 2, cx + bw / 2, cy - bh / 2); p.close()
    c.save(); c.clipPath(p, doAntiAlias=True)
    lvl = cy - bh / 2 + 30 * u + 25 * u * ease(prog(t, B(2, 0.5), 8))
    rect(c, cx - bw / 2, lvl, bw, bh, SEA)
    c.restore()
    c.drawPath(p, paint("#ffffff", 0.8, stroke=6 * u))
    text(c, "3.7 MILLION KM³", cx, cy + 40 * u, 56 * u, "#ffffff", vis(t, B(0, 0.1)), w=900, shadow=8)
    # evaporation
    pe = vis(t, B(2, 0.05))
    for k in range(5):
        x = cx - 320 * u + k * 160 * u
        arrow(c, x, cy - bh / 2 - 10 * u, x, cy - bh / 2 - 230 * u, "#ffffff", 16 * u, pe)
    chip(c, "EVAPORATION", cx, 0.12 * H, pe, 40 * u, dot="#ffffff")
    # inputs
    ins = [("RIVERS", "#7ec8ff", -1, 0.25), ("RAIN", "#7ec8ff", -1, 0.4), ("BLACK SEA", "#7ec8ff", 1, 0.25)]
    for k, (lab, colr, side, f) in enumerate(ins):
        pi = vis(t, B(2, f) if k < 2 else B(3, 0.1))
        y = cy - bh / 2 + 10 * u + (k % 2) * 70 * u
        x0_ = cx + side * (bw / 2 + 260 * u)
        arrow(c, x0_, y, cx + side * (bw / 2 - 20 * u), y, colr, 8 * u, pi)
        text(c, lab, x0_, y - 40 * u, 30 * u, colr, pi, w=900)
    pa = vis(t, B(2, 0.6))
    ax = cx - bw / 2 - 300 * u; ay = cy + 60 * u
    arrow(c, ax, ay, cx - bw / 2 + 10 * u, cy - 40 * u, "#4cd9a0", 18 * u, pa)
    text(c, "ATLANTIC ~1,000 KM³ / YEAR", ax + 40 * u, ay + 60 * u, 30 * u, "#4cd9a0", pa, w=900)
    xmark(c, ax + 140 * u, ay - 40 * u, 60 * u, prog(t, B(2, 0.8), 0.3))
    chip(c, "THE MATH HAS TURNED", cx, 0.92 * H, vis(t, B(1, 0.05), B(2, 0.5)), 38 * u, bg="#ff4d4d")
    chip(c, "NOT ENOUGH TO KEEP UP", cx, 0.92 * H, vis(t, B(3, 0.5)), 38 * u, bg="#ff4d4d")

def c_harborwall(c, W, H, t, S):
    u = S.u; o = S.opts; drop = o.get("drop", 0.4); B = beats(S, 2)
    fill_bg(c, W, H, "#7cc3ff", "#e0f2ff")
    sun(c, W * 0.85, 0.12 * H, 60 * u, t)
    wall_x = W * 0.38
    rect(c, 0, 0.25 * H, wall_x, 0.75 * H, "#c9b48a")
    for r in range(10):
        for k in range(6):
            rect(c, (k + (r % 2) * 0.5) * wall_x / 6, 0.25 * H + r * 0.075 * H, wall_x / 6 - 4 * u, 0.075 * H - 4 * u, "#b8a07a", 0.7)
    scale_px = (0.32 * H) / max(drop, 0.4)  # px per metre
    lvl0 = 0.45 * H
    d = drop * ease(prog(t, B(0, 0.05), max(1, S.dur * 0.6)))
    lvl = lvl0 + d * scale_px * (0.75 if drop > 1 else 0.9)
    if drop > 1:
        c.drawPath(poly([(wall_x, lvl0), (W, lvl0 + 40 * u), (W, H), (wall_x, H)]), paint("#e9d6a8"))
    c.drawRect(skia.Rect.MakeLTRB(wall_x - 2, lvl, W, H), paint(shader=lin(0, lvl, 0, H, [(0, "#2f9fd8", 0.95), (1, "#0b4f8f", 1)])))
    # stain line + ruler
    line(c, wall_x - 30 * u, lvl0, wall_x, lvl0, "#5a7a4a", 10 * u)
    rx = wall_x - 70 * u
    line(c, rx, lvl0, rx, lvl, "#ff4d4d", 6 * u)
    lab = f"−{int(round(d * 100))} CM" if drop < 1 else f"−{d:.1f} M"
    text(c, lab, rx - 20 * u, (lvl0 + lvl) / 2, 60 * u, "#ff4d4d", vis(t, B(0, 0.1)), w=900, align="r", shadow=8)
    boat(c, W * 0.6, lvl - 10 * u + math.sin(t * 1.5) * 4 * u, 70 * u)
    boat(c, W * 0.82, lvl - 10 * u + math.sin(t * 1.3 + 1) * 4 * u, 55 * u)
    sal = 0.3 + 0.5 * ease(prog(t, B(1, 0.05), 3))
    bar(c, W * 0.55, 0.1 * H, W * 0.3, 30 * u, sal * vis(t, B(1, 0.05)), "#ffffff", u, label="SALTINESS", a=vis(t, B(1, 0.05)))
    if drop > 1:
        chips(c, t, [(B(0, 0.4), None, "BEACHES STRETCH OUT", "#e9d6a8"), (B(0, 0.6), None, "HARBORS NEED DIGGING", "#c9b48a")],
              W * 0.7, 0.22 * H, 80 * u, u, 30)
        chip(c, "FISH + CORALS STRUGGLE", W * 0.7, 0.4 * H, vis(t, B(1, 0.1)), 30 * u, bg="#ff4d4d")
    else:
        chip(c, "SATELLITES WOULD SPOT IT", W * 0.7, 0.24 * H, vis(t, B(0, 0.35)), 30 * u, dot="#7ec8ff")

def c_suez(c, W, H, t, S):
    u = S.u; B = beats(S, 2); dark_bg(c, W, H)
    bb = (29.0, 27.0, 36.5, 33.0)
    rr = geo.map_rect(bb, W * 0.32, 0.52 * H, height=0.86 * H)
    geo.draw_map(c, bb, rr, land=LAND, sea=SEA, outline_w=2 * u)
    canal = [(32.32, 31.25), (32.33, 30.9), (32.3, 30.6), (32.35, 30.3), (32.56, 29.95)]
    pts = [geo.lonlat_xy(lo, la, bb, rr) for lo, la in canal]
    c.drawPath(poly(pts, close=False), paint("#4fb6ff", 1, stroke=7 * u))
    for k in range(3):
        q = (t * 0.3 + k / 3) % 1; i = q * (len(pts) - 1); j = int(i); f = i - j
        x0, y0 = pts[len(pts) - 1 - j]; x1, y1 = pts[max(0, len(pts) - 2 - j)]
        x, y = lerp(x0, x1, f), lerp(y0, y1, f)
        arrow(c, x, y + 30 * u, x, y - 30 * u, "#ffffff", 8 * u, math.sin(q * math.pi))
    tx, ty = geo.lonlat_xy(31.0, 32.4, bb, rr); text(c, "MEDITERRANEAN", tx, ty, 30 * u, "#ffffff", 1, w=900)
    tx, ty = geo.lonlat_xy(34.5, 28.0, bb, rr); text(c, "RED SEA", tx, ty, 30 * u, "#ffffff", 1, w=900)
    chip(c, "SUEZ CANAL: NO LOCKS", W * 0.32, 0.06 * H, vis(t, B(0, 0.1)), 32 * u, dot="#4fb6ff")
    pb = vis(t, B(1, 0.05))
    if pb > 0:
        x0 = W * 0.62
        text(c, "WHAT THE SEA LOSES", x0, 0.3 * H, 34 * u, "#ffffff", pb, w=800, align="l")
        rrect(c, x0, 0.34 * H, W * 0.32, 80 * u, 40 * u, "#ff7a4d", pb)
        text(c, "WHAT SUEZ ADDS", x0, 0.55 * H, 34 * u, "#ffffff", pb, w=800, align="l")
        rrect(c, x0, 0.59 * H, 30 * u * ease(prog(t, B(1, 0.3), 0.6)) + 4, 80 * u, 10 * u, "#4fb6ff", pb)
        chip(c, "A GARDEN HOSE", x0 + 260 * u, 0.62 * H, vis(t, B(1, 0.45)), 32 * u, dot="#4fb6ff")

def c_map(c, W, H, t, S):
    u = S.u; o = S.opts; stage = o.get("stage", 1); B = beats(S, 3 if stage == 2 else 2)
    dark_bg(c, W, H, "#0a1424", "#14243a")
    rr = med_rect(S)
    Wd = rr[2]
    if stage == 1: dry = lerp(0.0, 0.006, ease(prog(t, 0.2, S.dur * 0.6))); start = 0
    elif stage == 2: dry = lerp(0.006, 0.034, ease(prog(t, 0.2, S.dur * 0.75)))
    else: dry = lerp(0.0, 0.034, ease(prog(t, S.lt(0, 0.1), S.dur * 0.8)))
    def extra(c, rr):
        if stage == 1:
            pa = ease(prog(t, B(0, 0.3), 2))
            for poly_ in ([(12.2, 45.8), (13.8, 45.8), (13.6, 44.9), (12.4, 44.6)], [(10.0, 34.6), (11.4, 34.6), (11.0, 33.6), (10.2, 33.6)]):
                c.drawPath(poly([geo.lonlat_xy(lo, la, MED, rr) for lo, la in poly_]), paint(SALT, pa))
            c.drawPath(geo.land_path(MED, rr), paint("#0b1030", 0.35, stroke=2 * u))
    med_map(c, rr, dry=dry, u=u, extra=extra)
    def lab(txt, lo, la, p, size=30, colr="#ffffff"):
        x, y = geo.lonlat_xy(lo, la, MED, rr); chip(c, txt, x, y, p, size * u, bg="#0b1030")
    if stage == 1:
        x, y = geo.lonlat_xy(12.33, 45.44, MED, rr); pin(c, x, y, u, t=t, a=vis(t, B(0, 0.5)))
        lab("VENICE LAGOON → SALT FLAT", 7.5, 45.2, vis(t, B(0, 0.55)), 28)
        chip(c, "100 YEARS: ~ −40 M", W * 0.72, 0.9 * H if not S.P else 0.14 * H + 20 * u, vis(t, 0.2), 38 * u, bg="#ff4d4d")
        chip(c, "PORTS NOW FACE MUDFLATS", W * 0.3, 0.9 * H, vis(t, B(1, 0.2)), 32 * u)
    elif stage == 2:
        chip(c, "HUNDREDS OF METERS DOWN", W / 2, 0.08 * H, vis(t, B(0, 0.1), B(1, 0)), 36 * u, bg="#ff4d4d")
        chip(c, "SALT LEFT BEHIND, TENS OF METERS THICK", W / 2, 0.08 * H, vis(t, B(1, 0.1), B(2, 0)), 34 * u, dot=SALT)
        pl = vis(t, B(2, 0.2))
        x, y = geo.lonlat_xy(13.5, 36.3, MED, rr); pin(c, x, y, u, colr=ACCENT, a=pl, t=t)
        lab("LAND BRIDGE: ITALY–SICILY–AFRICA", 13.5, 34.0, pl, 28)
        lab("WEST", 4.0, 39.0, vis(t, B(2, 0.5)), 30); lab("EAST", 24.0, 34.2, vis(t, B(2, 0.5)), 30)
        chip(c, "A CHAIN OF SUPER-SALTY LAKES", W / 2, 0.94 * H, vis(t, B(2, 0.6)), 34 * u, bg=ACCENT, fg="#0b1030", a=1)
    else:
        chip(c, "OVER THOUSANDS OF YEARS", W / 2, 0.14 * H + 20 * u, vis(t, S.lt(0, 0.05)), 42 * u)

def c_basin(c, W, H, t, S):
    u = S.u; B = beats(S, 2)
    fill_bg(c, W, H, "#ffcf8a", "#ff9a5a")
    y0 = 0.22 * H; kmpx = 0.17 * H
    line(c, 0, y0, W, y0, "#1f6fd1", 6 * u, 1, dash=([18 * u, 12 * u], 0))
    text(c, "OLD SEA LEVEL", W * 0.02, y0 - 30 * u, 30 * u, "#1f6fd1", 1, w=900, align="l")
    prof = [(0, y0 - 40 * u), (W * 0.1, y0 + 0.2 * kmpx), (W * 0.2, y0 + 2.5 * kmpx), (W * 0.4, y0 + 3.2 * kmpx), (W * 0.6, y0 + 3.6 * kmpx),
            (W * 0.8, y0 + 2.6 * kmpx), (W * 0.92, y0 + 0.3 * kmpx), (W, y0 - 50 * u), (W, H), (0, H)]
    c.drawPath(poly(prof), paint("#b07a4a"))
    c.drawPath(poly(prof[:-2], close=False), paint(SALT, 1, stroke=14 * u))
    for km in range(1, 4):
        y = y0 + km * kmpx; line(c, W * 0.03, y, W * 0.06, y, "#0b1030", 4 * u, 0.7)
        text(c, f"−{km} KM", W * 0.065, y, 30 * u, "#0b1030", 0.8, w=900, align="l")
    pd = vis(t, B(0, 0.25))
    yd = y0 + 0.43 * kmpx
    line(c, W * 0.12, yd, W * 0.3, yd, "#0b1030", 4 * u, pd, dash=([10 * u, 8 * u], 0))
    chip(c, "DEAD SEA SHORE TODAY: −430 M", W * 0.3, yd, pd, 28 * u, align="l")
    ph = vis(t, B(1, 0.1))
    for k in range(8):
        x = W * (0.35 + 0.05 * k); y = y0 + 3.3 * kmpx - 60 * u
        p = skia.Path(); p.moveTo(x, y)
        for j in range(4): p.quadTo(x + (10 if j % 2 else -10) * u, y - (j + 0.5) * 18 * u - (t * 30 % 18) * u, x, y - (j + 1) * 18 * u)
        c.drawPath(p, paint("#fff3c4", ph * 0.6, stroke=4 * u))
    human(c, W * 0.6, y0 + 3.6 * kmpx - 8 * u, 40 * u, colr="#0b1030", a=ph)
    thermometer(c, W * 0.85, 0.5 * H, 300 * u, lerp(25, 50, ease(prog(t, B(1, 0.1), 2))), tmax=55, tmin=0, a=ph, label=False)
    chip(c, "SINKING AIR HEATS UP", W * 0.85, 0.15 * H, ph, 30 * u, bg="#ff4d4d")

def c_world(c, W, H, t, S):
    u = S.u; B = beats(S, 2)
    space_bg(c, W, H, t, 1, seed=31)
    if S.P: gx, gy, R = W / 2, 0.3 * H, 290 * u
    else: gx, gy, R = W * 0.33, 0.52 * H, 360 * u
    rot, tilt = 15, 30
    geo.globe(c, gx, gy, int(R), rot=rot, tilt=tilt)
    mx, my, _ = geo.globe_xy(18, 36, gx, gy, R, rot, tilt)
    for k in range(8):
        an = k / 8 * 6.28 + 0.3; q = (t * 0.4 + k / 8) % 1
        d = (40 + q * 260) * u
        circle(c, mx + math.cos(an) * d, my + math.sin(an) * d * 0.7, 10 * u, "#9fe0ff", math.sin(q * math.pi) * 0.9)
    # city flooding panel
    if S.P: bx, by, bw, bh = W * 0.12, 0.47 * H, W * 0.76, 0.14 * H
    else: bx, by, bw, bh = W * 0.6, 0.25 * H, W * 0.34, 0.55 * H
    rrect(c, bx, by, bw, bh, 30 * u, "#0b1030", 0.85)
    c.save(); c.clipRect(skia.Rect.MakeXYWH(bx, by, bw, bh))
    skyline(c, bw, by + bh, H, 5, "#3a4a6a", win=0.6, maxh=0.35 * bh / H) if False else None
    rng = random.Random(4); x = bx + 10 * u
    while x < bx + bw:
        w_ = rng.uniform(40, 90) * u; h_ = rng.uniform(0.25, 0.8) * bh
        rect(c, x, by + bh - h_, w_, h_, "#3a4a6a"); x += w_ + 8 * u
    fl = ease(prog(t, B(0, 0.5) if S.n() >= 2 else S.lt(0, 0.4), 3))
    rect(c, bx, by + bh - fl * bh * 0.32, bw, bh, "#2f86d8", 0.85)
    c.restore()
    big = "+~10 M" if fl > 0.05 else ""
    text(c, "GLOBAL SEA LEVEL", bx + bw / 2, by + 40 * u, 30 * u, "#ffffff", 1, w=800)
    text(c, "+~10 M", bx + bw / 2, by + (100 if not S.P else 90) * u, 70 * u, "#9fe0ff", vis(t, B(0, 0.6) if S.n() >= 2 else S.lt(0, 0.5)), w=900, shadow=8)
    if S.n() >= 2:
        chip(c, "DRY THE MED, FLOOD EVERYWHERE ELSE", W / 2, 0.92 * H, vis(t, B(1, 0.15)), 36 * u, bg="#ff4d4d")

def _salt_floor(c, W, H, t, u, hy):
    fill_bg(c, W, H, "#ffd9a0", "#fff0d0")
    c.drawPath(poly([(0, hy), (W * 0.15, hy - 160 * u), (W * 0.3, hy - 60 * u), (W * 0.55, hy - 200 * u), (W * 0.75, hy - 90 * u), (W, hy - 180 * u), (W, hy), (0, hy)]), paint("#c9a37a"))
    rect(c, 0, hy, W, H - hy, "#f4f0e6")
    rng = random.Random(5)
    for k in range(60):
        x = rng.random() * W; y = hy + (rng.random() ** 1.6) * (H - hy)
        s_ = (20 + (y - hy) / (H - hy) * 140) * u
        c.drawPath(poly([(x - s_, y), (x - s_ * 0.3, y - s_ * 0.25), (x + s_ * 0.6, y - s_ * 0.15), (x + s_, y + s_ * 0.1), (x + s_ * 0.2, y + s_ * 0.3)]),
                   paint("#d9d2c0", 0.9, stroke=max(1.5, s_ * 0.04)))

def c_saltdesert(c, W, H, t, S):
    u = S.u; B = beats(S, 2)
    hy = (0.36 if S.P else 0.5) * H
    _salt_floor(c, W, H, t, u, hy)
    for k in range(6):
        y = hy - 40 * u - k * 14 * u
        line(c, 0, y + math.sin(t * 3 + k) * 4 * u, W, y + math.sin(t * 3 + k + 1) * 4 * u, "#ffffff", 3 * u, 0.25)
    top = (0.24 if S.P else 0.1) * H
    chip(c, "~6 MILLION YEARS AGO", W / 2, top, vis(t, B(0, 0.2) if S.n() >= 2 else S.lt(0, 0.05)), 40 * u, dot=ACCENT)
    if S.n() >= 2:
        stamp(c, "IT HAPPENED", W / 2, 0.32 * H, prog(t, B(0, 0.3), 0.4), u, size=110)
        chip(c, "THE MESSINIAN SALINITY CRISIS", W / 2, 0.86 * H, vis(t, B(1, 0.6)), 40 * u, bg="#0b1030")
    else:
        q = ease(prog(t, S.lt(0, 0.5), 3))
        if q > 0:
            x = lerp(-0.2 * W, 1.1 * W, q)
            p = skia.Path(); p.moveTo(-10, hy - 120 * u); p.lineTo(x, hy - 120 * u); p.quadTo(x + 120 * u, hy - 60 * u, x + 60 * u, H); p.lineTo(-10, H); p.close()
            c.drawPath(p, paint("#2f86d8", 0.95)); c.drawPath(p, paint("#ffffff", 0.7, stroke=8 * u))
            chip(c, "THE ATLANTIC BREAKS BACK IN", W / 2, top + 80 * u, vis(t, S.lt(0, 0.55)), 36 * u, bg="#2f86d8")

def c_drill(c, W, H, t, S):
    u = S.u; B = beats(S, 2)
    sea_y = 0.26 * H; floor_y = 0.78 * H
    fill_bg(c, W, H, "#9fd3ff", "#e6f4ff")
    c.drawRect(skia.Rect.MakeLTRB(0, sea_y, W, floor_y), paint(shader=lin(0, sea_y, 0, floor_y, [(0, "#2f86b8", 1), (1, "#06203a", 1)])))
    rect(c, 0, floor_y, W, H - floor_y, "#8a6a4a")
    rect(c, 0, floor_y + 40 * u, W, 60 * u, SALT); rect(c, 0, floor_y + 100 * u, W, 40 * u, "#f2d45a")
    sx = W * 0.3
    c.drawPath(poly([(sx - 220 * u, sea_y - 30 * u), (sx + 220 * u, sea_y - 30 * u), (sx + 170 * u, sea_y + 20 * u), (sx - 170 * u, sea_y + 20 * u)]), paint("#e8eef8"))
    c.drawPath(poly([(sx - 40 * u, sea_y - 30 * u), (sx, sea_y - 230 * u), (sx + 40 * u, sea_y - 30 * u)]), paint("#b23a2a", 1, stroke=6 * u))
    pd = ease(prog(t, B(0, 0.05), 2.5))
    line(c, sx, sea_y, sx, lerp(sea_y, floor_y + 130 * u, pd), "#cfd8e3", 5 * u)
    chip(c, "1970: DEEP-SEA DRILLING", sx, 0.07 * H, vis(t, B(0, 0.05)), 34 * u)
    # core sample
    pc = prog(t, B(0, 0.45), 0.6)
    if pc > 0:
        cx, cy, cw, ch = W * 0.68, 0.18 * H, 160 * u, 0.66 * H
        layers = [("MUD", "#8a7a6a", 0.3), ("SALT", SALT, 0.25), ("GYPSUM", "#f2d45a", 0.2), ("WIND-BLOWN DUST", "#d9b48a", 0.25)]
        y = cy
        for k, (lab, colr, f) in enumerate(layers):
            show = 1 if k < 3 else prog(t, B(1, 0.1), 0.5)
            hh = ch * f
            rrect(c, cx, y, cw, hh, 10 * u, colr, eout(pc) * (show if k == 3 else 1))
            if k == 3 and show > 0:
                rng = random.Random(2)
                for j in range(30): circle(c, cx + rng.random() * cw, y + rng.random() * hh, 3 * u, "#a8784a", show)
            text(c, lab, cx + cw + 30 * u, y + hh / 2, 32 * u, "#0b1030", eout(pc) * (show if k == 3 else 1), w=900, align="l")
            y += hh
        rrect(c, cx, cy, cw, ch, 10 * u, "#ffffff", eout(pc), stroke=4 * u)
    chip(c, "SANDSTORMS. AT THE BOTTOM OF THE SEA.", W / 2, 0.94 * H, vis(t, B(1, 0.55)), 36 * u, bg="#ff4d4d")

def c_saltlayer(c, W, H, t, S):
    u = S.u; B = beats(S, 3)
    p0 = phase(t, None, B(1, 0)); p1 = phase(t, B(1, 0), B(2, 0)); p2 = phase(t, B(2, 0))
    with Layer(c, p0) as on:
        if on:
            fill_bg(c, W, H, "#0a2a4a", "#1f5f8f")
            fy = 0.35 * H
            rect(c, 0, fy, W, 0.1 * H, "#8a7a6a")
            th = 0.36 * H * ease(prog(t, B(0, 0.1), 1.5))
            rect(c, 0, fy + 0.1 * H, W, th, SALT)
            rect(c, 0, fy + 0.1 * H + th, W, H, "#6a5a4a")
            line(c, W * 0.9, fy + 0.1 * H, W * 0.9, fy + 0.1 * H + th, "#0b1030", 6 * u)
            text(c, "UP TO 3 KM", W * 0.89, fy + 0.1 * H + th / 2, 44 * u, "#0b1030", vis(t, B(0, 0.4)), w=900, align="r")
            chip(c, "~1 MILLION KM³ OF SALT", W / 2, 0.15 * H, vis(t, B(0, 0.2)), 44 * u, dot=SALT)
    with Layer(c, p1) as on:
        if on:
            dark_bg(c, W, H)
            for k in range(5):
                x = W * (0.15 + 0.175 * k); dry = (k % 2 == 0)
                pp = prog(t, B(1, 0.1 + 0.12 * k), 0.4)
                rrect(c, x - 110 * u, 0.4 * H, 220 * u, 160 * u, 30 * u, SALT if dry else SEA, pp)
                text(c, "DRY" if dry else "REFILL", x, 0.4 * H + 80 * u, 40 * u, "#0b1030" if dry else "#ffffff", pp, w=900)
                if k < 4: arrow(c, x + 120 * u, 0.4 * H + 80 * u, x + 175 * u, 0.4 * H + 80 * u, "#ffffff", 6 * u, pp)
            chip(c, "AGAIN AND AGAIN", W / 2, 0.75 * H, vis(t, B(1, 0.6)), 44 * u, bg=ACCENT, fg="#0b1030", a=1)
    with Layer(c, p2) as on:
        if on:
            fill_bg(c, W, H, "#ffd9a0", "#fff0d0")
            gy = 0.35 * H
            cut = poly([(W * 0.3, gy), (W * 0.45, 0.85 * H), (W * 0.55, 0.85 * H), (W * 0.7, gy)])
            rect(c, 0, gy, W, H - gy, "#b07a4a")
            fill = ease(prog(t, B(2, 0.5), 2))
            c.drawPath(cut, paint("#d9c08a" if fill > 0 else "#ffd9a0"))
            if fill < 1:
                c.save(); c.clipPath(cut, doAntiAlias=True); rect(c, 0, gy, W, (0.85 * H - gy) * (1 - fill), "#ffd9a0"); c.restore()
            c.drawPath(cut, paint("#7a5a3a", 1, stroke=4 * u))
            line(c, W * 0.5, 0.5 * H, W * 0.5, 0.82 * H, "#2f86d8", 10 * u, 1 - fill)
            chip(c, "RIVERS CARVED GRAND-CANYON-SCALE GORGES", W / 2, 0.15 * H, vis(t, B(2, 0.05)), 34 * u)
            chip(c, "NOW BURIED", W / 2, 0.92 * H, vis(t, B(2, 0.6)), 40 * u, bg="#0b1030")

def c_gauge(c, W, H, t, S):
    u = S.u; B = beats(S, 2); dark_bg(c, W, H)
    pA = phase(t, None, B(1, 0)); pB = phase(t, B(1, 0))
    with Layer(c, pA) as on:
        if on:
            base = 0.22 * H; kmpx = 0.28 * H
            for k, (lab, km, x) in enumerate([("WEST", 0.9, 0.2), ("EAST", 2.0, 0.42)]):
                p = ease(prog(t, B(0, 0.2 + 0.15 * k), 1.2))
                rrect(c, W * x - 70 * u, base, 140 * u, km * kmpx * p, 20 * u, "#ff7a4d")
                text(c, lab, W * x, base - 40 * u, 40 * u, "#ffffff", 1, w=900)
                text(c, f"−{km:g} KM" if k else "~ −0.9 KM", W * x, base + km * kmpx * p + 40 * u, 40 * u, "#ff7a4d", p, w=900)
            chip(c, "SEA-LEVEL DROP (2024 STUDY)", W * 0.31, 0.08 * H, vis(t, B(0, 0.1)), 32 * u)
            donut(c, W * 0.74, 0.5 * H, 210 * u, 0.7 * ease(prog(t, B(0, 0.6), 1.2)), "#ff7a4d", label="70%", sub="OF ITS WATER, LOST", u=u)
            chip(c, "UP TO", W * 0.74, 0.2 * H, vis(t, B(0, 0.6)), 30 * u)
    with Layer(c, pB) as on:
        if on:
            fill_bg(c, W, H, "#0a2a4a", "#1f5f8f")
            for k in range(6):
                x = W * (0.55 + 0.07 * k); y = 0.4 * H + (k % 2) * 80 * u
                fade = ease(prog(t, B(1, 0.05) + k * 0.15, 0.6))
                fishbone(c, x, y, 40 * u, a=1 - 0.9 * fade) if fade > 0.5 else _fish(c, x, y, 40 * u, a=1 - fade)
            for k in range(5):
                q = ease(prog(t, B(1, 0.5) + k * 0.2, 2.0))
                _fish(c, lerp(-0.1 * W, W * (0.15 + 0.08 * k), q), 0.65 * H + (k % 2) * 70 * u, 40 * u, colr="#ffd166", a=q)
            chip(c, "MANY SPECIES VANISHED", W * 0.7, 0.18 * H, vis(t, B(1, 0.1)), 34 * u, bg="#ff4d4d")
            chip(c, "NEWCOMERS FROM THE ATLANTIC", W * 0.3, 0.85 * H, vis(t, B(1, 0.55)), 34 * u, dot="#ffd166")

def _fish(c, x, y, s, colr="#7ec8ff", a=1.0):
    oval(c, x, y, s, s * 0.45, colr, a)
    c.drawPath(poly([(x - s * 0.9, y), (x - s * 1.4, y - s * 0.4), (x - s * 1.4, y + s * 0.4)]), paint(colr, a))
    circle(c, x + s * 0.55, y - s * 0.1, s * 0.09, "#0b1030", a)

def c_flood(c, W, H, t, S):
    u = S.u; B = beats(S, 4)
    fill_bg(c, W, H, "#7ab3e0", "#d0e8f7")
    hi = 0.32 * H; lo = 0.82 * H
    ground = poly([(0, hi + 30 * u), (W * 0.25, hi + 30 * u), (W * 0.85, lo + 20 * u), (W, lo + 20 * u), (W, H), (0, H)])
    c.drawPath(ground, paint("#b08a5a"))
    rect(c, 0, hi, W * 0.22, 30 * u, "#2f86d8")
    rect(c, W * 0.85, lo + 20 * u - (lo - hi) * 0.25 * ease(prog(t, B(2, 0), 6)), W * 0.15, H, "#2f86d8")
    p = skia.Path(); p.moveTo(W * 0.2, hi); p.lineTo(W * 0.25, hi); p.lineTo(W * 0.86, lo + 20 * u); p.lineTo(W * 0.86, lo - 50 * u); p.lineTo(W * 0.25, hi - 40 * u); p.close()
    c.drawPath(p, paint("#3f9fe8"))
    rng = random.Random(3)
    for k in range(70):
        q = (rng.random() + t * rng.uniform(0.3, 0.6)) % 1
        x = lerp(W * 0.25, W * 0.86, q); y = lerp(hi - 20 * u, lo - 15 * u, q) + rng.uniform(-18, 18) * u
        line(c, x, y, x + 30 * u, y + 30 * u * (lo - hi) / (W * 0.61), "#ffffff", 4 * u, 0.7 * math.sin(q * math.pi))
    text(c, "ATLANTIC", W * 0.1, hi - 50 * u, 40 * u, "#0b1030", 1, w=900)
    text(c, "EMPTY BASIN", W * 0.88, lo - 120 * u, 34 * u, "#0b1030", 1 - phase(t, B(2, 0)), w=900)
    c1 = vis(t, B(1, 0.1), B(2, 0))
    if c1 > 0:
        rrect(c, W * 0.42, 0.06 * H, W * 0.54, 0.22 * H, 30 * u, "#0b1030", 0.85 * c1)
        text(c, "~100,000,000 M³ / S", W * 0.69, 0.12 * H, 60 * u, ACCENT, c1, w=900)
        text(c, "≈ 1,000 × THE AMAZON", W * 0.69, 0.19 * H, 40 * u, "#ffffff", vis(t, B(1, 0.3), B(2, 0)), w=900)
        text(c, "LAKE GENEVA IN ~15 MINUTES", W * 0.69, 0.245 * H, 30 * u, "#9fe0ff", vis(t, B(1, 0.6), B(2, 0)), w=800)
    c2 = vis(t, B(2, 0.1), B(3, 0))
    if c2 > 0:
        bx = W * 0.65; by = 0.6 * H
        for k in range(3):
            rect(c, bx, by - (k + 1) * 60 * u, 120 * u, 56 * u, "#e9e2d0", c2)
            rect(c, bx + 20 * u, by - (k + 1) * 60 * u + 15 * u, 30 * u, 26 * u, "#4f7fb8", c2); rect(c, bx + 70 * u, by - (k + 1) * 60 * u + 15 * u, 30 * u, 26 * u, "#4f7fb8", c2)
        wl = ease(prog(t, B(2, 0.2), 2.5))
        rect(c, bx - 30 * u, by - 180 * u * wl, 180 * u, 180 * u * wl, "#2f86d8", 0.7 * c2)
        chip(c, "+10 M A DAY (AT THE PEAK)", W * 0.62, 0.15 * H, c2, 40 * u, bg="#2f86d8")
    c3 = vis(t, B(3, 0.1))
    chip(c, "~90% REFILLED IN MONTHS TO 2 YEARS (ONE MODEL)", W * 0.55, 0.15 * H, c3, 32 * u, bg="#0b1030")

def c_channel(c, W, H, t, S):
    u = S.u; B = beats(S, 4)
    p0 = phase(t, None, B(1, 0)); p1 = phase(t, B(1, 0), B(2, 0)); p2 = phase(t, B(2, 0))
    with Layer(c, p0) as on:
        if on:
            dark_bg(c, W, H)
            bb = (-8.2, 34.9, -3.0, 37.3)
            rr = geo.map_rect(bb, W / 2, 0.52 * H, height=0.86 * H)
            geo.draw_map(c, bb, rr, land=LAND, sea="#1a4f9a", outline_w=2 * u)
            ch = [(-6.9, 35.95), (-6.2, 35.92), (-5.6, 35.96), (-5.0, 36.0), (-4.3, 36.02), (-3.6, 36.0)]
            pts = [geo.lonlat_xy(lo, la, bb, rr) for lo, la in ch]
            q = ease(prog(t, B(0, 0.1), 2.5))
            n = max(2, int(q * len(pts) * 10))
            dense = []
            for i in range(len(pts) - 1):
                for j in range(10): dense.append((lerp(pts[i][0], pts[i + 1][0], j / 10), lerp(pts[i][1], pts[i + 1][1], j / 10)))
            c.drawPath(poly(dense[:n], close=False), paint("#7ef0ff", 0.9, stroke=16 * u, blur=4 * u))
            chip(c, "~200 KM CARVED CHANNEL", W / 2, 0.08 * H, vis(t, B(0, 0.2)), 38 * u, dot="#7ef0ff")
            chip(c, "FOUND WHILE SURVEYING FOR A SPAIN–MOROCCO TUNNEL", W / 2, 0.93 * H, vis(t, B(0, 0.55)), 28 * u)
    with Layer(c, p1) as on:
        if on:
            fill_bg(c, W, H, "#7ab3e0", "#d0e8f7")
            hi, lo = 0.35 * H, 0.75 * H
            c.drawPath(poly([(0, hi), (W, lo), (W, H), (0, H)]), paint("#b08a5a"))
            rng = random.Random(1)
            for k in range(120):
                q = (rng.random() + t * rng.uniform(0.2, 0.4)) % 1
                x = q * W; y = lerp(hi, lo, q) - rng.uniform(5, 50) * u
                c.drawPath(poly([(x, y), (x + 40 * u, y + 20 * u), (x + 10 * u, y + 25 * u)]), paint("#ffffff", 0.6 * math.sin(q * math.pi)))
            c.drawPath(poly([(0, hi - 60 * u), (W, lo - 60 * u), (W, lo), (0, hi)]), paint("#3f9fe8", 0.75))
            chip(c, "NOT A WATERFALL: GIANT RAPIDS, KILOMETERS WIDE", W / 2, 0.12 * H, vis(t, B(1, 0.2)), 32 * u)
    with Layer(c, p2) as on:
        if on:
            dark_bg(c, W, H)
            gx = W * 0.3
            rect(c, gx - 60 * u, 0.2 * H, 120 * u, 0.6 * H, "#ffffff", 0.1)
            lvl = 0.35 * H + 0.2 * H * ease(prog(t, B(2, 0.2), 2))
            rect(c, gx - 60 * u, lvl, 120 * u, 0.8 * H - lvl, "#2f86d8")
            text(c, "GLOBAL SEA LEVEL", gx, 0.15 * H, 34 * u, "#ffffff", 1, w=900)
            text(c, "~ −10 M", gx + 90 * u, lvl, 60 * u, "#9fe0ff", vis(t, B(2, 0.5)), w=900, align="l")
            chip(c, "OTHER SCIENTISTS: SLOWER, OR IN PULSES", W * 0.68, 0.4 * H, vis(t, B(3, 0.1)), 30 * u)
            chip(c, "FAST VERSION = LARGEST KNOWN FLOOD", W * 0.68, 0.55 * H, vis(t, B(3, 0.5)), 32 * u, bg=ACCENT, fg="#0b1030", a=1)

def c_africa(c, W, H, t, S):
    u = S.u; B = beats(S, 3)
    pA = phase(t, None, B(1, 0)); pB = phase(t, B(1, 0))
    with Layer(c, pA) as on:
        if on:
            dark_bg(c, W, H)
            bb = (-20, 0, 50, 58)
            rr = geo.map_rect(bb, W / 2, 0.52 * H, height=0.92 * H)
            geo.draw_map(c, bb, rr, land=LAND, sea=SEA, outline_w=2 * u)
            x0, y0 = geo.lonlat_xy(15, 20, bb, rr); x1, y1 = geo.lonlat_xy(15, 33, bb, rr)
            q = (t * 0.3) % 1
            arrow(c, x0, y0 + 40 * u * q, x1, y1 + 40 * u * q, "#ff4d4d", 18 * u, 0.9)
            chip(c, "AFRICA PUSHES NORTH", x0, y0 + 80 * u, vis(t, B(0, 0.1)), 34 * u, bg="#ff4d4d")
            gx, gy = geo.lonlat_xy(-5.6, 36, bb, rr); pin(c, gx, gy, u, colr=ACCENT, t=t, a=vis(t, B(0, 0.45)))
            chip(c, "CLOSED AGAIN, MILLIONS OF YEARS FROM NOW?", W / 2, 0.06 * H, vis(t, B(0, 0.45)), 30 * u)
    with Layer(c, pB) as on:
        if on:
            fill_bg(c, W, H, "#5fb0ff", "#d6efff")
            hy = 0.55 * H
            c.drawRect(skia.Rect.MakeLTRB(0, hy, W, H), paint("#2f9fd8"))
            c.drawPath(poly([(0, 0.72 * H), (W, 0.62 * H), (W, H), (0, H)]), paint("#f2d7a0"))
            ux, uy = W * 0.8, 0.8 * H
            line(c, ux, uy, ux - 30 * u, uy - 300 * u, "#5b3e2a", 8 * u)
            p = skia.Path(); p.addArc(skia.Rect.MakeXYWH(ux - 30 * u - 180 * u, uy - 300 * u - 90 * u, 360 * u, 180 * u), 180, 180); p.close()
            c.drawPath(p, paint("#ff4d4d"))
            chip(c, "SAFE ON HUMAN TIMESCALES", W / 2, 0.12 * H, vis(t, B(1, 0.2)), 40 * u, dot="#4cd964")
            chip(c, "ON EARTH'S TIMESCALE, SEAS COME AND GO", W / 2, 0.22 * H, vis(t, B(1, 0.6)), 34 * u)
            big_text(c, W, H, "IT MAY DO IT AGAIN", 0.42 * H, prog(t, B(2, 0.3), 0.4), u, colr=ACCENT, size=100)

def c_dive(c, W, H, t, S):
    u = S.u
    surf = 0.14 * H; floor_y = 0.55 * H
    fill_bg(c, W, H, "#9fd3ff", "#e6f4ff")
    c.drawRect(skia.Rect.MakeLTRB(0, surf, W, floor_y), paint(shader=lin(0, surf, 0, floor_y, [(0, "#2f9fd8", 1), (1, "#06203a", 1)])))
    rect(c, 0, floor_y, W, 0.08 * H, "#6a5a4a")
    reveal = ease(prog(t, S.lt(0, 0.4), 2))
    rect(c, 0, floor_y + 0.08 * H, W, 0.3 * H, SALT, reveal)
    rect(c, 0, floor_y + 0.38 * H, W, H, "#4a3a2a")
    sx = W * 0.5 + math.sin(t) * 40 * u
    human(c, sx, surf + 10 * u, 90 * u, colr="#ffd9b0")
    for k in range(4):
        q = (t * 0.5 + k / 4) % 1; circle(c, sx + 10 * u, surf - q * 20 * u, 5 * u, "#ffffff", 0.5 * (1 - q))
    for k in range(6): _fish(c, ((t * 0.05 + k * 0.17) % 1.2 - 0.1) * W, surf + (0.08 + 0.05 * k) * H, 22 * u, colr="#ffd166")
    line(c, W * 0.9, floor_y + 0.08 * H, W * 0.9, floor_y + 0.38 * H, "#0b1030", 5 * u, reveal)
    chip(c, "KILOMETERS OF SALT BENEATH YOU", W / 2, floor_y + 0.23 * H, vis(t, S.lt(0, 0.55)), 40 * u, bg="#0b1030")

# ---------------- AMOC Short ----------------
def _natl_rect(S):
    return geo.map_rect(NATL, S.W / 2, 0.39 * S.H, width=S.W * 0.99)

WARM = [(-90, 24), (-82, 25), (-79, 30), (-74, 36), (-60, 41), (-45, 45), (-30, 50), (-18, 55), (-8, 60), (2, 64)]
COLD = [(-25, 63), (-38, 58), (-48, 48), (-58, 36), (-52, 22), (-40, 10), (-34, 0)]

def _flow(c, rr, pts_ll, colr, t, u, a=1.0, width=10, dash=False, speed=1.0):
    pts = [geo.lonlat_xy(lo, la, NATL, rr) for lo, la in pts_ll]
    c.drawPath(poly(pts, close=False), paint(colr, a * 0.35, stroke=width * 2.4 * u))
    c.drawPath(poly(pts, close=False), paint(colr, a, stroke=width * u, dash=([28 * u, 18 * u], -t * 60 * speed)))
    x0, y0 = pts[-2]; x1, y1 = pts[-1]
    arrow(c, x0, y0, x1, y1, colr, width * u, a)

def _natl_base(c, S, t, warm=0.0, ice=0.0, off=0.0):
    u = S.u; W, H = S.W, S.H
    dark_bg(c, W, H, "#081226", "#0f1f3a")
    rr = _natl_rect(S)
    geo.draw_map(c, NATL, rr, land=LAND, sea="#1a4f9a", outline_w=2 * u)
    if warm > 0:
        x, y = geo.lonlat_xy(10, 55, NATL, rr)
        c.save(); c.clipPath(geo.land_path(NATL, rr), doAntiAlias=True)
        circle(c, x, y, 230 * u, "#ff7a1a", 0.45 * warm, blur=60 * u); c.restore()
    if ice > 0:
        top = [(-75, 74), (32, 74), (32, 68), (10, 62 - 6 * ice), (0, 60 - 8 * ice), (-6, 56 - 6 * ice), (-20, 60 - 3 * ice), (-45, 55 - 3 * ice), (-62, 52 - 3 * ice), (-75, 58)]
        c.save(); c.clipRect(skia.Rect.MakeXYWH(*rr))
        sm = geo._smooth(top, 3)
        c.drawPath(poly([geo.lonlat_xy(lo, la, NATL, rr) for lo, la in sm]), paint("#eef5fb", 0.8 * ice, blur=14 * u))
        c.drawPath(geo.land_path(NATL, rr), paint(LAND, 0.5 * ice))
        c.restore()
    return rr

def c_amoc(c, W, H, t, S):
    u = S.u; o = S.opts
    warm = o.get("warm")
    rr = _natl_base(c, S, t, warm=vis(t, S.lt(0, 0.2)) if warm else 0)
    _flow(c, rr, WARM, "#ff5a3a", t, u, a=1, width=10)
    pc = vis(t, S.lt(0, 0.4)) if not warm else 1
    _flow(c, rr, COLD, "#4fb6ff", t, u, a=pc, width=8, speed=0.6)
    for lo, la in ((-30, 62), (-50, 58)):
        x, y = geo.lonlat_xy(lo, la, NATL, rr)
        arrow(c, x, y - 30 * u, x, y + 30 * u, "#ffffff", 8 * u, pc)
    if warm:
        chip(c, "SURPRISINGLY MILD", W / 2, 0.71 * H, vis(t, S.lt(0, 0.3)), 40 * u, bg="#ff7a1a", fg="#0b1030", a=1)
    else:
        chip(c, "WARM WATER NORTH", W * 0.28, 0.71 * H, vis(t, S.lt(0, 0.1)), 30 * u, dot="#ff5a3a")
        chip(c, "COLD WATER SOUTH", W * 0.72, 0.71 * H, pc, 30 * u, dot="#4fb6ff")
        chip(c, "THE AMOC", W / 2, 0.78 * H, vis(t, S.lt(0, 0.8)), 44 * u, bg=ACCENT, fg="#0b1030", a=1)
    hook_text(c, W, H, t, S, y=0.11)

def c_amocoff(c, W, H, t, S):
    u = S.u
    off = ease(prog(t, S.lt(0, 0.05), 2.0)); ice = ease(prog(t, S.lt(0, 0.35), 3))
    rr = _natl_base(c, S, t, ice=ice)
    _flow(c, rr, WARM, mix("#ff5a3a", "#5a6070", off), t * (1 - off), u, a=1 - 0.6 * off, width=10)
    _flow(c, rr, COLD, mix("#4fb6ff", "#5a6070", off), t * (1 - off), u, a=1 - 0.6 * off, width=8)
    x, y = geo.lonlat_xy(-0.1, 51.5, NATL, rr); pin(c, x, y, u, colr="#7ec8ff", a=vis(t, S.lt(0, 0.65)), t=t)
    chips(c, t, [(S.lt(0, 0.12), None, "2025 SIMULATION, IN A WORLD 2 °C WARMER", "#ffffff"),
                 (S.lt(0, 0.4), None, "SEA ICE TO BRITAIN + SCANDINAVIA", "#eef5fb"),
                 (S.lt(0, 0.7), None, "LONDON COLD SNAPS: −20 °C", "#7ec8ff")], W / 2, 0.71 * H, 75 * u, u, 30)

def c_rainbelt(c, W, H, t, S):
    u = S.u
    bb = (-100, -40, 120, 50)
    dark_bg(c, W, H, "#081226", "#0f1f3a")
    rr = geo.map_rect(bb, W / 2, 0.36 * H, width=W * 0.99)
    geo.draw_map(c, bb, rr, land=LAND, sea="#1a4f9a", outline_w=1.5 * u)
    sh = ease(prog(t, S.lt(0, 0.1), 2.5))
    lat = lerp(8, 1, sh)
    x0, ya = geo.lonlat_xy(-100, lat + 6, bb, rr); x1, yb = geo.lonlat_xy(120, lat - 6, bb, rr)
    c.save(); c.clipRect(skia.Rect.MakeXYWH(*rr))
    rect(c, x0, ya, x1 - x0, yb - ya, "#7ec8ff", 0.35)
    for k in range(40):
        rng = random.Random(k); x = lerp(x0, x1, rng.random()); y = lerp(ya, yb, ((rng.random() + t * 0.8) % 1))
        line(c, x, y, x - 4 * u, y + 14 * u, "#cfe8ff", 2 * u, 0.7)
    c.restore()
    chip(c, "TROPICAL RAIN BELT SHIFTS SOUTH", W / 2, rr[1] - 40 * u, vis(t, S.lt(0, 0.1)), 30 * u, dot="#7ec8ff")
    for lo, la, lab in ((78, 22, "MONSOONS WEAKEN"), (0, 12, "")):
        x, y = geo.lonlat_xy(lo, la, bb, rr)
        pin(c, x, y, u, colr="#ff7a1a", a=vis(t, S.lt(0, 0.3)), t=t)
        if lab: chip(c, lab, x, y - 50 * u, vis(t, S.lt(0, 0.3)), 28 * u, bg="#ff7a1a", fg="#0b1030", a=1)
    x, y = geo.lonlat_xy(-75, 38, bb, rr)
    pe = vis(t, S.lt(0, 0.65))
    arrow(c, x - 20 * u, y + 40 * u, x - 20 * u, y - 50 * u, "#4fb6ff", 10 * u, pe)
    chip(c, "FASTER SEA-LEVEL RISE: US EAST COAST", W / 2, rr[1] + rr[3] + 50 * u, pe, 28 * u, dot="#4fb6ff")

def c_amocgauge(c, W, H, t, S):
    u = S.u
    dark_bg(c, W, H)
    rows = [("WEAKENS THIS CENTURY", "VERY LIKELY", 0.9, "#ff7a4d", 0.1), ("COLLAPSE BEFORE 2100", "NOT EXPECTED (MEDIUM CONFIDENCE)", 0.25, "#7ec8ff", 0.35),
            ("SOME NEWER STUDIES", "RISK MAY BE HIGHER", 0.55, ACCENT, 0.65)]
    for k, (lab, val, f, colr, at) in enumerate(rows):
        y = 0.24 * H + k * 0.115 * H
        p = vis(t, S.lt(0, at))
        text(c, lab, W * 0.08, y, 40 * u, "#ffffff", p, w=900, align="l")
        bar(c, W * 0.08, y + 50 * u, W * 0.84, 34 * u, f * ease(prog(t, S.lt(0, at), 1.0)), colr, u, a=p)
        text(c, val, W * 0.08, y + 120 * u, 30 * u, colr, p, w=800, align="l", fam="Inter")
    chip(c, "UN CLIMATE PANEL (IPCC)", W / 2, 0.2 * H, vis(t, S.lt(0, 0.05)), 32 * u)

SCENES = {k: v for k, v in globals().items() if k.startswith("c_") and callable(v)}
