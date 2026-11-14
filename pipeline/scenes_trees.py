"""Scenes: What If Trees Could Never Rot? (+ wood / oxygen Shorts)."""
from common2 import *
import geo

WOOD = "#7a5236"

def _hyphae(seed, x0, y0, x1, y1, n=160):
    rng = random.Random(seed); segs = []; tips = [(x0, y0 + (y1 - y0) * (k + 0.5) / 10, 0.0) for k in range(10)]
    k = 0
    while len(segs) < n:
        i = rng.randrange(len(tips)); x, y, ang = tips[i]
        L = rng.uniform(30, 70); ang = ang * 0.7 + rng.uniform(-0.6, 0.6)
        nx_, ny_ = x + math.cos(ang) * L, y + math.sin(ang) * L
        if not (x0 - 40 <= nx_ <= x1 + 40 and y0 <= ny_ <= y1): ang = -ang; continue
        segs.append((x, y, nx_, ny_)); tips[i] = (nx_, ny_, ang)
        if rng.random() < 0.18: tips.append((nx_, ny_, ang + rng.choice([-0.9, 0.9])))
    return segs

# ------------------------------------------------------------------ hook / outro / wood short
def a_logfloor(c, W, H, t, S):
    o = S.opts; u = S.u; outro = o.get("outro"); frozen = o.get("frozen")
    hy = 0.3 if S.P else 0.5
    forest_bg(c, W, H, t, u, dark=0.12, hy=hy)
    if outro: c.drawPaint(paint("#ffb347", 0.13))
    gy = (hy + 0.05) * H
    soil(c, W, gy + (0.07 if S.P else 0.09) * H, H)
    lx, ly = W / 2, (0.47 if S.P else 0.74) * H
    L, r = (820 if S.P else 1100) * u, (90 if S.P else 100) * u
    B = beats(S, 2)
    if frozen or outro: cr, fa = 0.0, (1.0 if outro else 0.0)
    else:
        cr = 0.8 * ease(prog(t, B(0, 0.15), max(0.1, B(0, 0.95) - B(0, 0.15))))
        rest = xfade(t, B(1, 0.0), 0.7); cr *= 1 - rest; fa = 1 - rest
    # soil mound from rotting
    if cr > 0: oval(c, lx, ly + r * 0.9, L * 0.5 * cr + 1, r * 0.55 * cr + 1, "#3b2a1e")
    log(c, lx, ly, L, r, WOOD, moss=0.8, crumble=cr, a=1)
    for k, dx in enumerate((-0.3, -0.1, 0.12, 0.3)):
        s_ = (52 - 6 * k) * u * (0.6 + 0.4 * math.sin(k * 2.1) ** 2)
        shelf(c, lx + dx * L, ly - r * 0.75, s_, a=fa * (1 - cr * 0.5))
    if fa > 0:
        mushroom(c, lx - 0.42 * L, ly + r * 0.95, 60 * u, a=fa); mushroom(c, lx + 0.4 * L, ly + r * 1.0, 44 * u, "#e0a43a", a=fa)
        for i in range(3):
            bx = lx - L * 0.35 + ((t * 30 * u + i * 260 * u) % (L * 0.7))
            beetle(c, bx, ly - r * 1.02, 16 * u, a=fa * 0.9)
    if frozen:
        yrs = int(lerp(1, 500, ease(t / S.dur)))
        chip(c, f"YEAR {yrs}", W / 2, ly - r - 120 * u, 1, 46 * u, bg="#0b1030")
        chip(c, "STILL THERE", W / 2, ly + r + 90 * u, vis(t, S.dur * 0.55), 40 * u, bg="#ff4d4d")
    elif outro:
        B2 = beats(S, 2); p = phase(t, B2(1, 0.0))
        if p > 0:
            cx_, cy_ = (W * 0.5, 0.22 * H) if S.P else (W * 0.78, 0.3 * H)
            sun(c, cx_, cy_ - 120 * u, 50 * u, t, a=p, glow=0.6)
            coal_lump(c, cx_, cy_ + 40 * u, 70 * u, a=p, glow=0.6 + 0.3 * math.sin(t * 3))
            chip(c, "300-MILLION-YEAR-OLD SUNLIGHT", cx_, cy_ + 150 * u, p, 32 * u)
        chip(c, "THE DECOMPOSERS", W / 2, ly - r - 110 * u, vis(t, B2(0, 0.3), B2(1, 0.0)), 40 * u, dot="#e0a43a")
    else:
        p = prog(t, B(1, 0.35), 0.4)
        stamp(c, "NEVER ROTS", W / 2, (0.22 if S.P else 0.3) * H, p, u, size=96)
    hook_text(c, W, H, t, S, y=0.2)

def a_rules(c, W, H, t, S):
    u = S.u; B = beats(S, 3); dark_bg(c, W, H)
    pA = phase(t, None, B(1, 0)); pB = phase(t, B(1, 0), B(2, 0)); pC = phase(t, B(2, 0))
    xs = [0.2, 0.4, 0.6, 0.8]; y = 0.45 * H
    with Layer(c, pA) as on:
        if on:
            items = [("LEAVES", lambda x, y_: leaf_icon(c, x, y_, 70 * u)), ("FRUIT", lambda x, y_: apple(c, x, y_, 70 * u)),
                     ("ANIMALS", lambda x, y_: fishbone(c, x, y_, 75 * u)), ("WOOD", lambda x, y_: log(c, x, y_, 190 * u, 42 * u, WOOD))]
            for k, (lab, fn) in enumerate(items):
                p = prog(t, B(0, 0.12 + k * 0.18), 0.4)
                if p <= 0: continue
                x = xs[k] * W
                rrect(c, x - 150 * u, y - 170 * u, 300 * u, 340 * u, 30 * u, "#ffffff", 0.07 * eout(p))
                if k == 3: rrect(c, x - 150 * u, y - 170 * u, 300 * u, 340 * u, 30 * u, "#ff4d4d", eout(p), stroke=5 * u)
                with Layer(c, eout(p)): fn(x, y - 30 * u)
                text(c, lab, x, y + 90 * u, 40 * u, "#ffffff", eout(p), w=800)
                if k < 3: chip(c, "STILL ROTS", x, y + 205 * u, p, 28 * u, dot="#4cd964")
                else: chip(c, "NEVER ROTS", x, y + 205 * u, p, 28 * u, bg="#ff4d4d")
    with Layer(c, pB) as on:
        if on:
            for k, (lab, fn) in enumerate([("FUNGI", lambda x, y_: fungus_icon(c, x, y_, 80 * u)), ("MICROBES", lambda x, y_: microbe(c, x, y_, 70 * u, t)),
                                           ("TERMITES", lambda x, y_: termite(c, x, y_, 95 * u))]):
                x = (0.27 + k * 0.23) * W
                fn(x, y - 30 * u); text(c, lab, x, y + 100 * u, 40 * u, "#ffffff", 1, w=800)
                xmark(c, x, y - 30 * u, 95 * u, prog(t, B(1, 0.25 + k * 0.15), 0.3))
            chip(c, "CAN'T BREAK DOWN WOOD", W / 2, 0.18 * H, prog(t, B(1, 0.6), 0.4), 40 * u, bg="#ff4d4d")
    with Layer(c, pC) as on:
        if on:
            for k in range(3): log(c, W * (0.32 + 0.18 * k), 0.62 * H - k * 10 * u, 300 * u, 50 * u, WOOD, ang=(-4, 3, -2)[k])
            tx = W * 0.5 + math.sin(t * 1.3) * 40 * u
            termite(c, tx, 0.42 * H, 110 * u)
            for k in range(3):
                pp = prog(t, B(2, 0.3 + k * 0.15), 0.3)
                text(c, "?", tx + (-60 + 60 * k) * u, 0.3 * H - k * 20 * u, (70 + 15 * k) * u, ACCENT, pp, w=900)

def a_lignin(c, W, H, t, S):
    u = S.u; B = beats(S, 2)
    fill_bg(c, W, H, "#2a1a10", "#3a2414")
    z = 1 + 0.06 * t / S.dur
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-W / 2, -H / 2)
    pf = prog(t, B(1, 0.05), max(0.5, B(1, 0.9) - B(1, 0.05)))
    nf = 13; fw = W / nf
    segs = _hyphae(5, 0, 0.08 * H, W, 0.92 * H, 520)
    front = pf * (W + 200 * u) - 100 * u
    for i in range(nf):
        x = (i + 0.5) * fw
        rect(c, i * fw, 0, fw, H, "#8a5a2e", 1 - 0.75 * clamp((front - i * fw) / (fw * 3)))  # lignin (glue)
        for k in range(3):
            xx = x - fw * 0.3 + k * fw * 0.3
            rrect(c, xx - fw * 0.12, -20, fw * 0.24, H + 40, fw * 0.12, "#e9d3a8", 1)
            line(c, xx, 0, xx, H, "#c9ad7a", 2 * u, 0.6)
    if pf > 0:
        nshow = int(len(segs) * pf)
        for (x0, y0, x1, y1) in segs[:nshow]:
            line(c, x0, y0, x1, y1, "#ffffff", 5 * u, 0.95)
    c.restore()
    chip(c, "CELLULOSE FIBERS", W * 0.3, 0.16 * H, vis(t, B(0, 0.15), B(1, 0)), 38 * u, dot="#e9d3a8")
    chip(c, "LIGNIN = THE GLUE", W * 0.7, 0.16 * H, vis(t, B(0, 0.4), B(1, 0)), 38 * u, dot="#8a5a2e")
    chip(c, "ONE OF NATURE'S TOUGHEST MATERIALS", W / 2, 0.86 * H, vis(t, B(0, 0.7), B(1, 0)), 36 * u)
    if pf > 0:
        chip(c, "WHITE-ROT FUNGI", W / 2, 0.16 * H, vis(t, B(1, 0.1)), 46 * u, bg="#0b1030", dot="#ffffff")
        chip(c, "THE LIGNIN-EATING CHAMPIONS", W / 2, 0.86 * H, vis(t, B(1, 0.45)), 36 * u)

def a_carbon(c, W, H, t, S):
    u = S.u; B = beats(S, 3)
    pA = phase(t, None, B(1, 0)); pB = phase(t, B(1, 0), B(2, 0)); pC = phase(t, B(2, 0))
    with Layer(c, pA) as on:
        if on:
            forest_bg(c, W, H, t, u, dark=0.2, hy=0.5)
            soil(c, W, 0.66 * H, H)
            tree2(c, W * 0.32, 0.68 * H, 520 * u)
            for k in range(10):
                rng = random.Random(k)
                xc, yc = W * 0.32 + rng.uniform(-110, 110) * u, 0.68 * H - rng.uniform(120, 440) * u
                circle(c, xc, yc, 20 * u, "#1b1b22", 0.85); text(c, "C", xc, yc, 24 * u, "#ffffff", 0.9, w=900)
            chip(c, "WOOD = STORED CARBON", W * 0.32, 0.12 * H, vis(t, B(0, 0.1)), 38 * u, dot="#1b1b22")
            log(c, W * 0.7, 0.7 * H, 520 * u, 60 * u, WOOD, moss=0.6, crumble=0.4)
            for k in range(9):
                q = (t * 0.25 + k / 9) % 1
                x = W * 0.7 + (k - 4) * 50 * u + math.sin(q * 6 + k) * 20 * u; y = 0.66 * H - q * 0.5 * H
                circle(c, x, y, 26 * u, "#cfd8e3", 0.8 * (1 - q) * vis(t, B(0, 0.45)))
                text(c, "CO2", x, y, 18 * u, "#2a3344", 0.9 * (1 - q) * vis(t, B(0, 0.45)), w=900)
            chip(c, "ROTTING RELEASES IT", W * 0.7, 0.12 * H, vis(t, B(0, 0.5)), 38 * u, dot="#cfd8e3")
    with Layer(c, pB) as on:
        if on:
            dark_bg(c, W, H)
            text(c, "CARBON RELEASED EACH YEAR", W / 2, 0.2 * H, 56 * u, "#ffffff", 1, w=900)
            bw = W * 0.5; x0 = W * 0.25
            p1 = ease(prog(t, B(1, 0.15), 1.2)); p2 = ease(prog(t, B(1, 0.55), 1.2))
            bar(c, x0, 0.42 * H, bw, 70 * u, p1 * 1.0, "#c98a4a", u, label="DEAD WOOD ROTTING", val="≈ 11 BILLION T")
            bar(c, x0, 0.66 * H, bw, 70 * u, p2 * 0.93, "#9aa4b8", u, label="ALL HUMAN COAL, OIL AND GAS", val="≈ 10 BILLION T")
            chip(c, "SAME LEAGUE", W / 2, 0.85 * H, vis(t, B(1, 0.85)), 40 * u, bg=ACCENT, fg="#0b1030", a=1)
    with Layer(c, pC) as on:
        if on:
            dark_bg(c, W, H)
            off = ease(prog(t, B(2, 0.35), 0.35))
            cx, cy = W / 2, 0.48 * H
            rrect(c, cx - 230 * u, cy - 110 * u, 460 * u, 220 * u, 110 * u, mix("#4cd964", "#ff4d4d", off))
            circle(c, cx + lerp(120, -120, off) * u, cy, 90 * u, "#ffffff")
            text(c, "ROT", cx, cy - 190 * u, 80 * u, "#ffffff", 1, w=900)
            text(c, "ON" if off < 0.5 else "OFF", cx + lerp(-110, 110, off) * u, cy, 64 * u, "#0b1030", 1, w=900)

def a_branch(c, W, H, t, S):
    u = S.u; B = beats(S, 2)
    hy = 0.36
    forest_bg(c, W, H, t, u, dark=0.1, hy=hy)
    gy = 0.52 * H
    rect(c, 0, gy, W, H - gy, "#3a2a1c")
    # branch
    c.save(); c.translate(W / 2, gy - 22 * u)
    oval(c, 0, 30 * u, 520 * u, 18 * u, "#000000", 0.25, blur=8 * u)
    line(c, -480 * u, 0, 480 * u, -14 * u, "#a8784a", 40 * u)
    line(c, -480 * u, -8 * u, 480 * u, -22 * u, "#c99a66", 8 * u, 0.6)
    for k, (bx, ang, L) in enumerate([(-260, -40, 190), (60, -60, 230), (280, -30, 160)]):
        line(c, bx * u, -6 * u, bx * u + math.cos(math.radians(ang)) * L * u, -6 * u + math.sin(math.radians(ang)) * L * u, "#a8784a", 18 * u)
    c.restore()
    d = 1 + int(prog(t, B(0, 0.1), max(0.1, B(0, 0.6) - B(0, 0.1))) * 1)
    chip(c, f"DAY {d}", W / 2, 0.14 * H, vis(t, 0.1, B(1, 0)), 44 * u)
    chip(c, "LOOKS THE SAME", W / 2, 0.22 * H, vis(t, B(0, 0.45), B(1, 0)), 34 * u)
    # hidden network
    reveal = xfade(t, B(1, 0.0), 0.8); dim = ease(prog(t, B(1, 0.45), 1.2))
    rng = random.Random(9); nodes = [(rng.uniform(0.05, 0.95) * W, rng.uniform(gy + 60 * u, H - 40 * u)) for _ in range(40)]
    colr = mix("#9ef0c0", "#5a5a66", dim)
    for i, (x, y) in enumerate(nodes):
        for j in range(i + 1, len(nodes)):
            x2, y2 = nodes[j]
            if abs(x - x2) + abs(y - y2) < 260 * u:
                line(c, x, y, x2, y2, colr, 2.5 * u, 0.6 * reveal * (1 - 0.5 * dim))
        pulse = 0.5 + 0.5 * math.sin(t * 4 + i) * (1 - dim)
        circle(c, x, y, 8 * u * (1 + pulse * 0.4), colr, reveal * 0.9)
    chip(c, "THE HIDDEN ECONOMY", W / 2, gy + 80 * u, vis(t, B(1, 0.1)), 40 * u, dot="#9ef0c0")
    chip(c, "SHUT DOWN", W / 2, gy + 170 * u, vis(t, B(1, 0.55)), 40 * u, bg="#ff4d4d")

def a_logsection(c, W, H, t, S):
    u = S.u; B = beats(S, 2)
    forest_bg(c, W, H, t, u, dark=0.35, hy=0.42)
    cx, cy = W / 2, 0.6 * H; L, r = 1300 * u, 200 * u
    rrect(c, cx - L / 2, cy - r, L, 2 * r, r * 0.5, "#9a6a40")
    rrect(c, cx - L / 2, cy - r, L, 2 * r, r * 0.5, "#5b3e2a", 1, stroke=18 * u)
    rng = random.Random(4)
    for k in range(7):
        x = cx - L * 0.4 + k * L * 0.13; p = skia.Path(); p.moveTo(x, cy - r * 0.6)
        p.cubicTo(x + 60 * u, cy - r * 0.2, x - 40 * u, cy + r * 0.2, x + 30 * u, cy + r * 0.6)
        c.drawPath(p, paint("#5b3e2a", 1, stroke=22 * u))
    starve = lambda i: prog(t, B(0, 0.12 + 0.25 * i), 0.4)
    for k in range(4):  # fungi threads
        segs = _hyphae(20 + k, cx - L * 0.45 + k * L * 0.23, cy - r * 0.8, cx - L * 0.45 + k * L * 0.23 + 220 * u, cy + r * 0.8, 25)
        for s_ in segs: line(c, *s_, mix("#ffffff", "#777777", starve(0)), 3 * u, 0.8 * (1 - 0.6 * starve(0)))
    for k in range(3): beetle(c, cx - L * 0.25 + k * 260 * u, cy + (k % 2 - 0.5) * r * 0.6, 26 * u, a=1 - 0.6 * starve(1))
    for k in range(3): termite(c, cx + L * 0.2 + k * 90 * u, cy + r * 0.3, 40 * u, a=1 - 0.4 * starve(2))
    # shelves fade in line 1
    sf = 1 - ease(prog(t, B(1, 0.4), 1.2))
    for k, dx in enumerate((-0.35, -0.15, 0.08, 0.3)):
        shelf(c, cx + dx * L, cy - r * 1.02, (70 - 8 * k) * u, a=sf)
    lab = [("FUNGI: STARVING", 0, -0.32), ("BEETLES: STARVING", 1, -0.05), ("TERMITE GUT MICROBES: STUCK", 2, 0.28)]
    for (txt, i, dx) in lab:
        chip(c, txt, cx + dx * L, 0.14 * H if i != 1 else 0.22 * H, vis(t, B(0, 0.12 + 0.25 * i), B(1, 0)), 30 * u, bg="#ff4d4d")
    # gut microbe zoom
    zp = vis(t, B(0, 0.62), B(1, 0))
    if zp > 0:
        zx, zy = cx + L * 0.36, 0.3 * H
        circle(c, zx, zy, 120 * u, "#1b2a40", zp); circle(c, zx, zy, 120 * u, "#ffffff", zp, stroke=5 * u)
        for k in range(4): microbe(c, zx + (k % 2 - 0.5) * 100 * u, zy + (k // 2 - 0.5) * 90 * u, 28 * u, t + k, a=zp)
        xmark(c, zx, zy, 70 * u, zp * prog(t, B(0, 0.8), 0.3))
    chip(c, "SHELF FUNGI = FRUIT OF WOOD-EATERS", W / 2, 0.14 * H, vis(t, B(1, 0.05)), 34 * u, dot="#c9853a")
    chip(c, "GONE FROM EVERY DEAD TREE", W / 2, 0.24 * H, vis(t, B(1, 0.6)), 34 * u, bg="#ff4d4d")

def a_pileup(c, W, H, t, S):
    u = S.u; B = beats(S, 2); long_ = S.n() >= 2
    hy = 0.3 if S.P else 0.42
    forest_bg(c, W, H, t, u, dark=0.15, hy=hy)
    gy = (hy + 0.12) * H
    soil(c, W, gy + (0.18 if S.P else 0.28) * H, H)
    base = (0.56 if S.P else 0.82) * H
    rng = random.Random(11); n = 26
    end = B(1, 0) if long_ else S.dur
    for k in range(n):
        tk = k / n * end * 0.95
        p = eout(prog(t, tk, 0.6))
        if p <= 0: continue
        row = k % 7; lay = k // 7
        x = W * (0.12 + 0.76 * (row + 0.5 * (lay % 2)) / 7) + rng.uniform(-30, 30) * u
        y = base - lay * 58 * u - (1 - p) * 500 * u
        log(c, x, y, rng.uniform(260, 420) * u * (0.8 if S.P else 1), rng.uniform(24, 34) * u, mix(WOOD, "#5b3e2a", rng.random()),
            ang=rng.uniform(-12, 12), moss=rng.random() * 0.4, seed=k)
    yrs = 1 + int(ease(t / max(end, 0.1)) * (0 if long_ else 49))
    chip(c, "YEAR 1" if long_ else f"YEAR {yrs}", W / 2, (0.22 if S.P else 0.12) * H, vis(t, 0.1, end - 0.2 if long_ else None), 44 * u)
    if long_:
        p = phase(t, B(1, 0.0))
        if p > 0:
            rrect(c, 0, 0, W, H, 0, "#0b1030", 0.55 * p)
            donut(c, W * 0.35, 0.47 * H, 170 * u, 0.29 * ease(prog(t, B(1, 0.25), 1.0)), ACCENT, a=p, label="~29%", sub="BY INSECTS", u=u)
            text(c, "OF THE WORLD'S", W * 0.35, 0.79 * H, 34 * u, "#ffffff", p, w=700, fam="Inter")
            text(c, "DEAD-WOOD DECAY", W * 0.35, 0.84 * H, 34 * u, "#ffffff", p, w=700, fam="Inter")
            q = prog(t, B(1, 0.65), 0.5)
            c.save(); c.translate(W * 0.68, 0.47 * H); c.rotate(-6 * eout(q))
            rrect(c, -230 * u, -110 * u, 460 * u, 220 * u, 20 * u, "#f4ead8", p); rrect(c, -230 * u, -110 * u, 460 * u, 220 * u, 20 * u, "#7a2a1f", p, stroke=10 * u)
            text(c, "BUFFET", 0, -40 * u, 70 * u, "#7a2a1f", p, w=900); text(c, "CLOSED", 0, 50 * u, 80 * u, "#ff4d4d", p * eout(q), w=900)
            c.restore()

def a_split(c, W, H, t, S):
    u = S.u; B = beats(S, 2)
    hl = ease(prog(t, B(1, 0), 0.6))
    half = W / 2
    # tropics
    c.save(); c.clipRect(skia.Rect.MakeXYWH(0, 0, half, H))
    fill_bg(c, W, H, "#5fae8a", "#2f6b4a")
    for k in range(9): tree2(c, half * (k + 0.5) / 9 + (k % 2) * 20 * u, 0.85 * H, (380 + 90 * (k % 3)) * u, leaf="#1f7a44")
    for k in range(40):
        rng = random.Random(k); x = rng.random() * half; y = ((rng.random() + t * 1.2) % 1) * H
        line(c, x, y, x - 6 * u, y + 30 * u, "#cfe8ff", 3 * u, 0.5)
    c.restore()
    # boreal
    c.save(); c.clipRect(skia.Rect.MakeXYWH(half, 0, half, H))
    fill_bg(c, W, H, "#c9d6e3", "#7f93a8")
    for k in range(10): conifer(c, half + half * (k + 0.5) / 10, 0.86 * H, (300 + 60 * (k % 3)) * u, snow=0.8)
    for k in range(50):
        rng = random.Random(k + 99); x = half + rng.random() * half; y = ((rng.random() + t * 0.15) % 1) * H
        circle(c, x, y, 4 * u, "#ffffff", 0.8)
    c.restore()
    c.drawRect(skia.Rect.MakeXYWH(0, 0, half, H), paint("#000000", 0.45 * hl))
    c.drawRect(skia.Rect.MakeXYWH(half, 0, half, H), paint("#000000", 0.45 * (1 - hl) * prog(t, B(0, 0.1), 0.5)))
    line(c, half, 0, half, H, "#ffffff", 6 * u)
    log(c, half * 0.5, 0.88 * H, 380 * u, 40 * u, WOOD, crumble=0.6 * (0.5 + 0.5 * math.sin(t)))
    log(c, half * 1.5, 0.9 * H, 420 * u, 46 * u, "#6b4a33", moss=0.3)
    chip(c, "TROPICS", half * 0.5, 0.1 * H, 1, 40 * u)
    chip(c, "COLD NORTH", half * 1.5, 0.1 * H, 1, 40 * u)
    chip(c, "ROTS FAST", half * 0.5, 0.2 * H, vis(t, B(0, 0.2)), 34 * u, dot="#4cd964")
    chip(c, ">90% OF DEAD-WOOD CARBON", half * 0.5, 0.29 * H, vis(t, B(0, 0.55)), 30 * u, dot=ACCENT)
    chip(c, "CENTURIES (NORMALLY)", half * 1.5, 0.2 * H, vis(t, B(1, 0.15)), 34 * u, dot="#9fd3ff")
    stamp(c, "NOW: NEVER", half * 1.5, 0.45 * H, prog(t, B(1, 0.7), 0.4), u, size=80)

def a_nutrients(c, W, H, t, S):
    u = S.u; B = beats(S, 2)
    hy = 0.22 if S.P else 0.3
    fill_bg(c, W, H, "#bfe6d2", "#e9f6e8")
    gy = (0.42 if S.P else 0.55) * H
    soil(c, W, gy, H)
    lock = ease(prog(t, B(1, 0.0), 0.6))
    lx, sx = (W * 0.32, W * 0.75)
    log(c, lx, gy - 45 * u, (480 if S.P else 640) * u, 55 * u, WOOD, moss=0.5)
    # seedling
    grow = 1 - 0.3 * lock; wilt = lock
    sh = 220 * u * grow
    p = skia.Path(); p.moveTo(sx, gy); p.quadTo(sx + 30 * u * wilt, gy - sh * 0.6, sx + 70 * u * wilt, gy - sh + 40 * u * wilt)
    c.drawPath(p, paint(mix("#3a9a4a", "#b59a3a", wilt), 1, stroke=12 * u))
    for s_ in (-1, 1):
        leaf_icon(c, sx + s_ * 40 * u + 60 * u * wilt, gy - sh * 0.75 + 40 * u * wilt, 36 * u, mix("#4caf50", "#c9a23a", wilt))
    for k in range(5):  # roots
        line(c, sx, gy, sx + (k - 2) * 30 * u, gy + 110 * u, "#d9c8a8", 4 * u, 0.7)
    rng = random.Random(3)
    for k in range(16):
        nm = "N" if k % 2 else "P"; colr = "#7ec8ff" if nm == "N" else "#ff9ad5"
        ph = (t * 0.25 + k / 16) % 1
        if lock < 0.5:
            # path: log -> soil -> roots -> up stem
            if ph < 0.6: x = lerp(lx + rng.uniform(-150, 150) * u, sx, ph / 0.6); y = gy + 70 * u + math.sin(ph * 9 + k) * 30 * u
            else: q = (ph - 0.6) / 0.4; x = sx; y = lerp(gy + 60 * u, gy - sh * 0.8, q)
            a_ = 1 - lock * 2
        else:
            x = lx + rng.uniform(-200, 200) * u + math.sin(t * 5 + k) * 6 * u; y = gy - 45 * u + rng.uniform(-30, 30) * u; a_ = (lock - 0.5) * 2
        circle(c, x, y, 17 * u, colr, a_); text(c, nm, x, y, 20 * u, "#0b1030", a_, w=900)
    if lock > 0: padlock(c, lx, gy - 170 * u, 70 * u, a=lock)
    chip(c, "NUTRIENTS RECYCLED", W / 2, (0.16 if S.P else 0.12) * H, vis(t, B(0, 0.15), B(1, 0)), 40 * u, dot="#7ec8ff")
    chip(c, "LOCKED IN THE WOOD", W / 2, (0.16 if S.P else 0.12) * H, vis(t, B(1, 0.15)), 40 * u, bg="#ff4d4d")

def a_lumberyard(c, W, H, t, S):
    u = S.u; B = beats(S, 2)
    forest_bg(c, W, H, t, u, dark=0.2, hy=0.38)
    gy = 0.6 * H
    soil(c, W, gy + 0.2 * H, H, colr=mix("#4a3424", "#8a8a80", ease(prog(t, B(1, 0.3), 3))))
    rng = random.Random(21)
    for stack in range(4):
        sx = W * (0.15 + stack * 0.24)
        for k in range(10):
            row = k // 4; col_i = k % 4
            log(c, sx + (col_i - 1.5) * 52 * u + row * 26 * u, gy + 0.18 * H - row * 46 * u, 300 * u, 24 * u, mix(WOOD, "#5b3e2a", rng.random()), ang=90 - 70, seed=k)
    sp = phase(t, B(1, 0))
    for k in range(5):
        x = W * (0.12 + k * 0.19); hh = 60 * u * (1 - 0.4 * ease(prog(t, B(1, 0.4), 2)))
        line(c, x, gy + 0.2 * H, x, gy + 0.2 * H - hh, "#8a9a3a", 6 * u, sp)
        leaf_icon(c, x + 14 * u, gy + 0.2 * H - hh, 16 * u, "#b5a33a", sp)
    chip(c, "10 YEARS IN", W / 2, 0.1 * H, vis(t, 0.1, B(1, 0)), 44 * u)
    chip(c, "SEEDLINGS STRUGGLE", W * 0.3, 0.1 * H, vis(t, B(1, 0.05)), 34 * u, bg="#ff4d4d")
    if S.n() >= 2:
        fr = 1 - 0.7 * ease(prog(t, B(1, 0.4), max(0.5, S.dur - B(1, 0.4))))
        bar(c, W * 0.55, 0.1 * H - 15 * u, W * 0.25, 30 * u, fr * vis(t, B(1, 0.3)), mix("#ff4d4d", "#4cd964", fr), u, label=None, val="SOIL", a=vis(t, B(1, 0.3)))

def a_barn(c, W, H, t, S):
    u = S.u; B = beats(S, 2)
    fill_bg(c, W, H, "#9fd3ff", "#e6f4ff")
    hills(c, W, 0.62 * H, 30 * u, "#7cc56f", 1, H=H)
    gy = 0.8 * H
    barn(c, W * 0.25, gy, 360 * u); house(c, W * 0.6, gy, 300 * u); fence(c, W * 0.7, W * 0.95, gy, 160 * u)
    fence(c, W * 0.03, W * 0.13, gy, 160 * u)
    yrs = int(lerp(1, 300, ease(prog(t, B(0, 0.1), max(0.5, B(1, 0) - B(0, 0.1))))))
    chip(c, f"YEAR {yrs}", W / 2, 0.1 * H, vis(t, 0.1, B(1, 0)), 46 * u)
    chips(c, t, [(B(0, 0.15), B(1, 0), "HOUSES: NO ROT", "#4cd964"), (B(0, 0.3), B(1, 0), "FENCES: NO ROT", "#4cd964"),
                 (B(0, 0.45), B(1, 0), "TERMITES: HARMLESS", "#4cd964")], W * 0.82, 0.24 * H, 80 * u, u, 30)
    termite(c, W * 0.47, 0.82 * H, 50 * u); xmark(c, W * 0.47, 0.82 * H, 50 * u, prog(t, B(0, 0.5), 0.3))
    # fuel
    fp = phase(t, B(1, 0))
    if fp > 0:
        c.drawRect(skia.Rect.MakeXYWH(0, 0, W, H), paint("#ff7a1a", 0.12 * fp))
        for k in range(6):
            x = W * (0.08 + k * 0.17); y = 0.92 * H
            for j in range(3): log(c, x + j * 14 * u, y - j * 22 * u, 200 * u, 18 * u, "#9a7a52", ang=(-8 + 8 * j))
            c.drawRect(skia.Rect.MakeXYWH(x - 110 * u, y - 80 * u, 240 * u, 100 * u), paint("#ff7a1a", fp * (0.5 + 0.5 * math.sin(t * 4 + k)), stroke=4 * u, dash=([14 * u, 10 * u], t * 20)))
        chip(c, "ALL OF IT IS FUEL", W / 2, 0.12 * H, vis(t, B(1, 0.35)), 46 * u, bg="#ff7a1a", fg="#0b1030", a=1)

def a_fire(c, W, H, t, S):
    u = S.u; o = S.opts; B = beats(S, 2)
    fill_bg(c, W, H, "#2a0f0a", "#ff6a1a")
    hy = 0.5 if S.P else 0.7
    for k in range(14):
        x = W * (k + 0.5) / 14; h_ = (260 + 80 * (k % 3)) * u
        tree2(c, x, hy * H + 0.05 * H, h_, leaf="#1a0d08", trunk="#120806")
        flame(c, x + 10 * u, hy * H - h_ * 0.4, h_ * 0.55, t, seed=k)
    rect(c, 0, hy * H + 0.05 * H, W, H, "#120806")
    for k in range(5): smoke(c, W * (0.1 + 0.2 * k), hy * H - 200 * u, t + k, u, a=0.9, seed=k, rise=500)
    rng = random.Random(1)
    for k in range(60):
        ph = (rng.random() + t * rng.uniform(0.1, 0.3)) % 1
        x = rng.random() * W + math.sin(ph * 8 + k) * 30 * u; y = (hy + 0.05) * H - ph * hy * H
        circle(c, x, y, 4 * u, "#ffd166", 1 - ph)
    if o.get("bugs"):
        for k in range(3):
            x = ((t * 0.12 + k * 0.33) % 1.2 - 0.1) * W; y = (0.25 + 0.06 * k) * H + math.sin(t * 2 + k) * 30 * u
            c.save(); c.translate(x, y); c.rotate(90); dragonfly(c, 0, 0, (150 - 30 * k) * u, t, col_="#140a06"); c.restore()
        chip(c, "GIANT BUGS + CONSTANT FIRE", W / 2, 0.22 * H, vis(t, S.lt(0, 0.4)), 38 * u)
    elif o.get("badge") == "FIRE":
        chips(c, t, [(S.lt(0, 0.2), None, "ABOVE ~25% OXYGEN: FORESTS CAN'T REGROW", ACCENT),
                     (S.lt(0, 0.62), None, "~35%: EVEN WET PLANTS BURN", "#ff4d4d")], W / 2, 0.24 * H, 90 * u, u, 33)
    else:
        chip(c, "BIGGER, HOTTER WILDFIRES", W / 2, 0.12 * H, vis(t, B(0, 0.1), B(0, 0.5)), 40 * u, bg="#0b1030")
        chip(c, "FIRE = THE NEW DECOMPOSER", W / 2, 0.12 * H, vis(t, B(0, 0.55)), 44 * u, bg=ACCENT, fg="#0b1030", a=1)
        pa = vis(t, B(1, 0.1))
        for k in range(5):
            q = (t * 0.3 + k / 5) % 1; x = W * (0.15 + 0.17 * k); y = 0.5 * H - q * 0.3 * H
            arrow(c, x, y + 60 * u, x, y - 30 * u, "#cfd8e3", 10 * u, pa * (1 - q))
            text(c, "CO2", x + 50 * u, y, 30 * u, "#cfd8e3", pa * (1 - q), w=900)
        chip(c, "WOOD  →  CO2", W / 2, 0.22 * H, pa, 36 * u)

def a_swamp(c, W, H, t, S):
    u = S.u; B = beats(S, 2)
    wl = (0.3 if S.P else 0.42) * H
    fill_bg(c, W, H, "#9fbfa8", "#cfe0c8")
    for k in range(7): tree2(c, W * (k + 0.5) / 7, wl, (240 + 40 * (k % 2)) * u, leaf="#4f7f4a")
    c.drawRect(skia.Rect.MakeLTRB(0, wl, W, H), paint(shader=lin(0, wl, 0, H, [(0, "#3c5a4a", 1), (1, "#1a2620", 1)])))
    # mud layers rising
    mud_top = lerp(H * 0.92, H * (0.5 if S.P else 0.62), ease(t / S.dur))
    for k in range(5):
        y = mud_top + k * 60 * u
        rect(c, 0, y, W, H - y, mix("#4a3a2a", "#2a1f17", k / 5), 1)
    rng = random.Random(7)
    for k in range(14):
        t0 = k / 14 * S.dur * 0.8; p = prog(t, t0, 3.0)
        if p <= 0: continue
        x = W * (0.08 + 0.84 * rng.random())
        yend = lerp(H * 0.95, mud_top + 30 * u, k / 14) if True else 0
        y = lerp(wl - 100 * u, max(yend, wl + 40 * u), ease(p))
        log(c, x, y, rng.uniform(200, 320) * u, 22 * u, "#6b4a33", ang=rng.uniform(-20, 20) * (1 - p) + rng.uniform(-6, 6), seed=k)
    # CO2 meter
    co2 = 1 - 0.45 * ease(prog(t, B(1, 0.0) if S.n() >= 2 else S.dur * 0.4, 3))
    bx = W * (0.5 if S.P else 0.78); by = (0.15 if S.P else 0.12) * H
    bar(c, bx - 200 * u, by, 400 * u, 34 * u, co2, "#cfd8e3", u, label="CO2 IN THE AIR", a=1)
    chip(c, "BURIED WOOD = CARBON OUT OF THE SKY", W / 2, (0.22 if S.P else 0.3) * H, vis(t, B(1, 0.2) if S.n() >= 2 else S.lt(0, 0.4)), 30 * u)
    if S.n() < 2:
        chip(c, "PLANET COOLS", W / 2, 0.79 * H, vis(t, S.lt(0, 0.75)), 36 * u, dot="#7ec8ff")

def a_graph(c, W, H, t, S):
    u = S.u; B = beats(S, 2); dark_bg(c, W, H)
    x0, x1, y0, y1 = W * 0.14, W * 0.86, 0.2 * H, 0.82 * H
    line(c, x0, y1, x1, y1, "#ffffff", 4 * u, 0.6); line(c, x0, y0, x0, y1, "#ffffff", 4 * u, 0.6)
    text(c, "TIME  →", x1, y1 + 45 * u, 32 * u, "#cfe3ff", 1, w=700, fam="Inter", align="r")
    def curve(fn, p, colr, lab):
        if p <= 0: return
        pts = [(lerp(x0, x1, i / 60), lerp(y1, y0, fn(i / 60))) for i in range(int(60 * p) + 1)]
        c.drawPath(poly(pts, close=False), paint(colr, 1, stroke=10 * u))
        x, y = pts[-1]; circle(c, x, y, 14 * u, colr)
        text(c, lab, x + 26 * u, y, 36 * u, colr, 1, w=900, align="l") if p > 0.98 else None
    pa = ease(prog(t, B(0, 0.05), max(0.5, B(0, 0.6))))
    curve(lambda x: 0.8 - 0.45 * x ** 0.8, pa, "#cfd8e3", "CO2")
    curve(lambda x: 0.7 - 0.4 * x, ease(prog(t, B(0, 0.4), max(0.5, B(1, 0) - B(0, 0.4)))), "#7ec8ff", "TEMP")
    curve(lambda x: 0.3 + 0.5 * x ** 1.2, ease(prog(t, B(1, 0.35), max(0.5, S.dur - B(1, 0.35) - 0.6))), "#4cd9a0", "OXYGEN")
    chip(c, "PLANTS RELEASE OXYGEN, ROTTING USES IT UP", W / 2, 0.1 * H, vis(t, B(1, 0.1)), 32 * u)

def a_coal(c, W, H, t, S):
    u = S.u; B = beats(S, 3)
    pA = phase(t, None, B(2, 0))
    with Layer(c, pA) as on:
        if on:
            fill_bg(c, W, H, "#3a2a1c", "#1a120c")
            cols = ["#6b5038", "#5a4430", "#7a6046", "#4a3828", "#5f4a36"]
            for k in range(5): rect(c, 0, H * k / 5, W, H / 5, cols[k], 0.7)
            press = ease(prog(t, B(0, 0.1), max(0.5, B(1, 0.3) - B(0, 0.1))))
            y = 0.62 * H; th = lerp(150, 70, press) * u
            rect(c, 0, y - th / 2, W, th, mix("#9a6a40", "#121216", press))
            rect(c, 0, y - th / 2, W, th, mix("#e0b07a", "#3a3a48", press), 1, stroke=5 * u)
            for k in range(9):
                rng = random.Random(k + 300)
                log(c, (k + 0.5) / 9 * W, y + rng.uniform(-0.15, 0.15) * th, 200 * u, th * 0.28, mix("#7a5236", "#121216", press), ang=rng.uniform(-6, 6), a=1 - press)
            text(c, "BURIED WOOD", W * 0.12, y - th / 2 - 30 * u, 32 * u, "#ffffff", 1 - press, w=800, align="l")
            if press > 0.9:
                for k in range(20):
                    rng = random.Random(k); circle(c, rng.random() * W, y + rng.uniform(-0.4, 0.4) * th, 3 * u, "#9aa4c8", 0.6 + 0.4 * math.sin(t * 3 + k))
            for k in range(6):
                x = W * (k + 0.5) / 6; arrow(c, x, 0.2 * H, x, 0.38 * H + press * 0.04 * H, "#ffffff", 12 * u, 0.7)
            c.drawRect(skia.Rect.MakeXYWH(0, 0.8 * H, W, 0.2 * H), paint(shader=lin(0, 0.8 * H, 0, H, [(0, "#ff5a1a", 0), (1, "#ff5a1a", 0.6 * press)])))
            chip(c, "PRESSURE", W / 2, 0.12 * H, vis(t, B(0, 0.25)), 36 * u, dot="#ffffff")
            chip(c, "HEAT", W / 2, 0.92 * H, vis(t, B(0, 0.5)), 36 * u, dot="#ff5a1a")
            stamp(c, "COAL", W / 2, 0.45 * H, prog(t, B(1, 0.05), 0.4), u, color=ACCENT, rot=-6, size=120)
    pB = phase(t, B(2, 0))
    with Layer(c, pB) as on:
        if on:
            space_bg(c, W, H, t, 1, seed=8)
            cap = lerp(68, 45, ease(prog(t, B(2, 0.2), 4)))
            geo.globe(c, W * 0.66, 0.5 * H, int(330 * u), rot=20 + t * 3, tilt=22, cap_n=cap, cap_s=-cap)
            gauge(c, W * 0.25, 0.6 * H, 230 * u, lerp(0.21, 0.3, ease(prog(t, B(2, 0.5), 3))) / 0.4, "OXYGEN", u,
                  valtxt=f"{lerp(21, 30, ease(prog(t, B(2, 0.5), 3))):.0f}%", colr="#4cd9a0")
            chip(c, "ICE SPREADS", W * 0.66, 0.1 * H, vis(t, B(2, 0.3)), 36 * u, dot="#ffffff")

def _o2(c, x, y, r, pct, u, a=1.0):
    gauge(c, x, y, r, (pct - 15) / 25, "OXYGEN", u, valtxt=f"{pct:.0f}%", colr=mix("#4cd9a0", "#ff7a1a", (pct - 21) / 14), a=a)

def a_oxygen(c, W, H, t, S):
    u = S.u; o = S.opts
    fill_bg(c, W, H, "#0f2a2a", "#1d3f3a")
    bugs_only = o.get("bugs_only"); n = S.n()
    E = 5 if n >= 5 else 3
    B = beats(S, E)
    if bugs_only:
        pct = 21 + 14 * ease(prog(t, S.lt(0, 0.1), S.dur * 0.6)); grow = (pct - 21) / 14; fire = 0
    elif E == 3:
        pct = 21 + 14 * ease(prog(t, B(0, 0.05), B(1, 0) - B(0, 0.05))); grow = ease(prog(t, B(1, 0), 1.0)); fire = xfade(t, B(2, 0), 0.6)
    else:
        pct = 21 + 14 * ease(prog(t, 0.3, B(1, 0))); grow = ease(prog(t, 0.3, B(1, 0))); fire = phase(t, B(1, 0), B(2, 0))
    summary = phase(t, B(2, 0), B(3, 0)) if E == 5 else 0
    finale = xfade(t, B(3, 0)) if E == 5 else 0
    with Layer(c, 1 - summary - finale * (1 - summary)) as on:
        if on:
            cx, cy = (W / 2, 0.36 * H) if S.P else (W * 0.58, 0.45 * H)
            s_ = lerp(150, 380, grow) * u
            c.save(); c.translate(cx, cy); c.rotate(90)
            dragonfly(c, 0, 0, s_, t, col_="#2a4a5a")
            # tracheae
            for k in range(9):
                yy = -0.1 * s_ + k * 0.11 * s_
                for sgn in (-1, 1):
                    line(c, sgn * 0.05 * s_, yy, 0, yy + 0.07 * s_, "#8fe8ff", max(2, 0.012 * s_), 0.85)
                q = (t * 0.6 + k / 9) % 1
                circle(c, 0.05 * s_ * (1 - q), yy + 0.07 * s_ * q, max(3, 0.018 * s_), "#ffffff", 0.9 * (0.4 + 0.6 * grow))
            c.restore()
            if fire > 0:
                for k in range(8): flame(c, W * (k + 0.5) / 8, H * (0.58 if S.P else 0.98), (140 + 40 * (k % 3)) * u, t, seed=k, a=fire)
            gx, gy = (W * 0.5, 0.8 * H) if S.P else (W * 0.2, 0.58 * H)
            _o2(c, gx, gy, (170 if S.P else 200) * u, pct, u)
            if S.P: pass
            else:
                chip(c, "NO LUNGS: BREATHING TUBES", W * 0.58, 0.1 * H, vis(t, B(0, 0.2), B(1, 0)), 34 * u, dot="#8fe8ff")
                chip(c, "HOTTER, FASTER FIRES", W * 0.58, 0.1 * H, vis(t, B(1, 0.1)) * (1 - summary), 34 * u, bg="#ff7a1a", fg="#0b1030", a=1)
            if bugs_only:
                chip(c, "RICHER AIR REACHES DEEPER", W / 2, 0.24 * H, vis(t, S.lt(0, 0.55)), 32 * u, dot="#8fe8ff")
    if summary > 0:
        with Layer(c, summary):
            items = [("COLDER", "#7ec8ff"), ("OXYGEN-RICH", "#4cd9a0"), ("GIANT BUGS", ACCENT), ("ON TOP OF COAL", "#9aa4b8")]
            for k, (lab, colr) in enumerate(items):
                p = prog(t, B(2, 0.1 + 0.18 * k), 0.4)
                chip(c, lab, W * (0.17 + 0.22 * k), 0.5 * H, p, 34 * u, dot=colr)
    if finale > 0:
        big_text(c, W, H, "SOUNDS MADE UP.", 0.42 * H, prog(t, B(3, 0), 0.3) * finale, u, size=130)
        big_text(c, W, H, "EXCEPT IT ISN'T.", 0.6 * H, prog(t, B(4, 0), 0.3), u, colr=ACCENT, size=130)

def a_gauge(c, W, H, t, S):
    u = S.u; o = S.opts
    fill_bg(c, W, H, "#0f2a2a", "#1d3f3a")
    rng = random.Random(2)
    for k in range(40):
        x = (rng.random() + t * 0.02 * (1 + k % 3)) % 1 * W; y = rng.random() * H
        circle(c, x, y, rng.uniform(6, 14) * u, "#8fe8ff", 0.15)
        if k % 3 == 0: text(c, "O2", x, y, 18 * u, "#8fe8ff", 0.35, w=900)
    swing = ease(prog(t, S.lt(0, 0.62), 1.0))
    pct = lerp(21, 35, swing)
    _o2(c, W / 2, 0.47 * H, 330 * u, pct, u)
    chip(c, "TODAY", W / 2, 0.47 * H + 200 * u, 1 - swing, 40 * u)
    chip(c, "WHAT IF?", W / 2, 0.47 * H + 200 * u, swing, 40 * u, bg="#ff7a1a", fg="#0b1030", a=1)
    hook_text(c, W, H, t, S, y=0.22)

def _swamp_bg(c, W, H, t, u, wl, mist=0.4):
    fill_bg(c, W, H, "#5f7f5a", "#a8c09a")
    for k in range(6):
        lycopsid(c, W * (0.05 + 0.18 * k) + (k % 2) * 40 * u, wl + 10 * u, (520 + 120 * (k % 3)) * u, a=0.55, t=t)
    for k in range(5): treefern(c, W * (0.12 + 0.2 * k), wl + 10 * u, (300 + 60 * (k % 2)) * u, a=0.9, t=t)
    for k in range(4): lycopsid(c, W * (0.1 + 0.27 * k), wl + 20 * u, (700 + 100 * (k % 2)) * u, a=1, t=t + k)
    c.drawRect(skia.Rect.MakeLTRB(0, wl, W, H), paint(shader=lin(0, wl, 0, H, [(0, "#3d5a40", 1), (1, "#1f2e22", 1)])))
    for k in range(6):
        y = wl + 20 * u + k * 22 * u; line(c, 0, y, W, y, "#9fc0a0", 2 * u, 0.15)
    c.drawRect(skia.Rect.MakeLTRB(0, wl - 200 * u, W, wl + 30 * u), paint("#e8f0e0", mist * 0.35, blur=40 * u))

def a_carbswamp(c, W, H, t, S):
    u = S.u; o = S.opts; B = beats(S, 3)
    wl = (0.5 if S.P else 0.7) * H
    _swamp_bg(c, W, H, t, u, wl)
    for k in range(2):
        x = ((t * 0.08 + k * 0.5) % 1.3 - 0.15) * W; y = (0.3 + 0.08 * k) * H + math.sin(t * 1.5 + k) * 20 * u
        c.save(); c.translate(x, y); c.rotate(90); dragonfly(c, 0, 0, (120 - 20 * k) * u, t + k, col_="#1c2a20"); c.restore()
    millipede(c, W * 0.3 + t * 15 * u, wl + 40 * u, 280 * u, t)
    short = S.n() < 3; badge = o.get("badge")
    top = 0.24 * H if S.P else 0.1 * H
    if short and not badge:
        chip(c, "~300 MILLION YEARS AGO", W / 2, top, vis(t, S.lt(0, 0.05)), 40 * u, dot=ACCENT)
        p = vis(t, S.lt(0, 0.62))
        coal_lump(c, W / 2, top + 150 * u, 60 * u, a=p, glow=0.3)
        chip(c, "WHERE COAL COMES FROM", W / 2, top + 260 * u, p, 34 * u)
        return
    if not short:
        chip(c, "THE CARBONIFEROUS", W / 2, top, vis(t, B(0, 0.05), B(1, 0)), 46 * u, dot=ACCENT)
        chip(c, "360–300 MILLION YEARS AGO", W / 2, top + 90 * u, vis(t, B(0, 0.15), B(1, 0)), 34 * u)
        chip(c, "NAMED AFTER COAL", W / 2, top + 175 * u, vis(t, B(0, 0.4), B(1, 0)), 34 * u, dot="#16161c")
    # oxygen beat
    po = phase(t, B(1, 0), B(2, 0))
    if po > 0:
        with Layer(c, po):
            gx, gy = (W / 2, 0.36 * H) if S.P else (W / 2, 0.42 * H)
            rrect(c, gx - 360 * u, gy - 250 * u, 720 * u, 380 * u, 40 * u, "#0b1030", 0.75)
            _o2(c, gx, gy + 40 * u, 230 * u, lerp(21, 32.5, ease(prog(t, B(1, 0.15), 1.5))), u)
            text(c, "THEN: ~30–35%   ·   TODAY: 21%", gx, gy - 200 * u, 34 * u, "#ffffff", 1, w=800, fam="Inter")
    pm = phase(t, B(2, 0))
    if pm > 0:
        with Layer(c, pm):
            mx, my = (W / 2, 0.38 * H) if S.P else (W * 0.45, 0.42 * H)
            rrect(c, 0, 0, W, H, 0, "#0b1030", 0.45)
            c.save(); c.translate(mx, my); c.rotate(90); dragonfly(c, 0, 0, 330 * u, t, col_="#24384a"); c.restore()
            span = 330 * u * 1.1 * 2 * 0.55 * 0.92
            ry = my + 240 * u
            line(c, mx - span / 2 - 120 * u, ry, mx + span / 2 + 120 * u, ry, ACCENT, 6 * u)
            for sx in (-1, 1): line(c, mx + sx * (span / 2 + 120 * u), ry - 20 * u, mx + sx * (span / 2 + 120 * u), ry + 20 * u, ACCENT, 6 * u)
            text(c, "~70 CM WINGSPAN", mx, ry + 50 * u, 44 * u, ACCENT, 1, w=900)
            chip(c, "MEGANEURA", mx, my - 260 * u, 1, 40 * u)
            px_, py_ = (W * 0.5, 0.56 * H) if S.P else (W * 0.82, 0.45 * H)
            if not S.P:
                pigeon(c, px_, py_, 180 * u, a=prog(t, B(2, 0.55), 0.4))
                text(c, "PIGEON", px_, py_ + 110 * u, 36 * u, "#cfe3ff", prog(t, B(2, 0.55), 0.4), w=800)

def a_giants(c, W, H, t, S):
    u = S.u; B = beats(S, 2)
    pA = phase(t, None, B(1, 0)); pB = phase(t, B(1, 0))
    with Layer(c, pA) as on:
        if on:
            wl = 0.82 * H
            _swamp_bg(c, W, H, t, u, wl, mist=0.2)
            sc = ease(prog(t, B(0, 0.45), 1.5))  # zoom out to show lycopsid
            k = lerp(1.0, 0.32, sc)
            c.save(); c.translate(W * 0.3, wl); c.scale(k, k)
            millipede(c, 300 * u, -20 * u, 1300 * u, t)
            human(c, -300 * u, 0, 175 * 2.6 * u, colr="#e8eef8")
            text(c, "2+ METERS", 60 * u, -150 * u, 60 * u, ACCENT, 1 - sc, w=900)
            c.restore()
            hp = sc
            lycopsid(c, W * 0.72, wl, 0.7 * H, a=hp, t=t)
            human(c, W * 0.6, wl, 0.7 * H * 1.75 / 35, colr="#e8eef8", a=hp)
            line(c, W * 0.8, wl, W * 0.8, wl - 0.7 * H, ACCENT, 6 * u, hp)
            text(c, "30–40 M", W * 0.81, wl - 0.35 * H, 54 * u, ACCENT, hp, w=900, align="l")
            chip(c, "ARTHROPLEURA", W * 0.3, 0.12 * H, vis(t, B(0, 0.05), B(0, 0.45)), 40 * u)
            chip(c, "GIANT LYCOPSIDS", W * 0.72, 0.12 * H, vis(t, B(0, 0.55)), 40 * u)
    with Layer(c, pB) as on:
        if on:
            dark_bg(c, W, H, "#1a1410", "#2a1e16")
            coal_lump(c, W * 0.3, 0.5 * H, 200 * u)
            for k in range(4): flame(c, W * (0.18 + 0.08 * k), 0.85 * H, 120 * u, t, seed=k, a=0.8)
            donut(c, W * 0.68, 0.48 * H, 200 * u, 0.7 * ease(prog(t, B(1, 0.2), 1.2)), "#ff7a1a", label="70%", sub="FOSSIL CHARCOAL", u=u)
            chip(c, "UP TO", W * 0.68, 0.18 * H, vis(t, B(1, 0.2)), 34 * u)
            chip(c, "FREQUENT, INTENSE FIRES", W / 2, 0.86 * H, vis(t, B(1, 0.6)), 36 * u, bg="#ff7a1a", fg="#0b1030", a=1)

def a_icearth(c, W, H, t, S):
    u = S.u; B = beats(S, 2)
    space_bg(c, W, H, t, 1, seed=12)
    cap = lerp(-78, -38, ease(prog(t, B(0, 0.1), max(1, B(1, 0) - B(0, 0.1)))))
    q = phase(t, B(1, 0))
    gx = lerp(W / 2, W * 0.3, q)
    pangea_globe(c, gx, 0.52 * H, 360 * u, rot=10 + t * 4, tilt=-28, cap_s=cap)
    chip(c, "ICE SHEETS SPREAD", W / 2, 0.1 * H, vis(t, B(0, 0.1), B(1, 0)), 40 * u, dot="#ffffff")
    chip(c, "CLOSE TO FREEZING OVER (ONE MODEL)", W / 2, 0.93 * H, vis(t, B(0, 0.5), B(1, 0)), 32 * u)
    if q > 0:
        text(c, "?", W * 0.72, 0.42 * H, 300 * u, ACCENT, q, w=900, shadow=20)
        text(c, "WHY WAS THE", W * 0.72, 0.68 * H, 48 * u, "#ffffff", q, w=900)
        text(c, "WOOD BURIED?", W * 0.72, 0.75 * H, 48 * u, "#ffffff", q, w=900)

def a_fungitree(c, W, H, t, S):
    u = S.u; B = beats(S, 4); dark_bg(c, W, H)
    x0, x1 = W * 0.08, W * 0.92; ya = 0.62 * H
    def X(ma): return lerp(x0, x1, (420 - ma) / 160)
    dim = phase(t, B(2, 0))
    with Layer(c, 1 - 0.75 * dim):
        line(c, x0, ya, x1, ya, "#ffffff", 5 * u, 0.8)
        for ma in range(420, 259, -20):
            line(c, X(ma), ya - 12 * u, X(ma), ya + 12 * u, "#ffffff", 3 * u, 0.6)
            text(c, f"{ma}", X(ma), ya + 45 * u, 26 * u, "#cfe3ff", 0.8, w=700, fam="Inter")
        text(c, "MILLION YEARS AGO", W / 2, ya + 95 * u, 28 * u, "#cfe3ff", 0.8, w=700, fam="Inter")
        p1 = ease(prog(t, B(0, 0.1), 1.2))
        rrect(c, X(385), ya - 150 * u, (X(260) - X(385)) * p1, 50 * u, 25 * u, "#4caf50")
        text(c, "TREES WITH LIGNIN", X(385) + 20 * u, ya - 125 * u, 30 * u, "#ffffff", p1, w=900, align="l")
        p2 = ease(prog(t, B(0, 0.5), 1.2))
        rrect(c, X(360), ya - 240 * u, (X(300) - X(360)) * p2, 50 * u, 25 * u, "#16161c")
        rrect(c, X(360), ya - 240 * u, (X(300) - X(360)) * p2, 50 * u, 25 * u, ACCENT, p2, stroke=3 * u)
        text(c, "COAL BOOM", X(360) + 20 * u, ya - 215 * u, 30 * u, ACCENT, p2, w=900, align="l")
        p3 = prog(t, B(1, 0.4), 0.5)
        if p3 > 0:
            fx = X(300); line(c, fx, ya - 330 * u, fx, ya, "#ffffff", 4 * u, p3, dash=([12 * u, 10 * u], 0))
            fungus_icon(c, fx, ya - 370 * u, 50 * u, a=p3)
            chip(c, "LIGNIN-EATING FUNGI APPEAR?", fx, ya - 450 * u, p3, 32 * u, dot="#ffffff")
        chip(c, "2012: GENOMES OF 31 FUNGI", W / 2, 0.1 * H, vis(t, B(1, 0.05), B(2, 0)), 34 * u)
    if dim > 0:
        big_text(c, W, H, "ONE FUNGUS CHANGED THE PLANET", 0.42 * H, prog(t, B(2, 0), 0.4), u, size=96)
        stamp(c, "MIGHT BE WRONG", W / 2, 0.62 * H, prog(t, B(3, 0), 0.4), u, size=90)

def a_bark(c, W, H, t, S):
    u = S.u; B = beats(S, 2); dark_bg(c, W, H)
    pA = phase(t, None, B(1, 0)); pB = phase(t, B(1, 0))
    with Layer(c, pA) as on:
        if on:
            for (x, R, bark_f, lab) in [(W * 0.3, 230 * u, 0.8, "CARBONIFEROUS LYCOPSID"), (W * 0.72, 180 * u, 0.12, "TYPICAL TREE TODAY")]:
                p = prog(t, B(0, 0.1 if x < W / 2 else 0.5), 0.6)
                if p <= 0: continue
                rin = R * math.sqrt(1 - bark_f)
                circle(c, x, 0.48 * H, R, "#5a4a3a", eout(p)); circle(c, x, 0.48 * H, rin, "#e0c08a", eout(p))
                for k in range(1, 6): circle(c, x, 0.48 * H, rin * k / 6, "#b08a5a", eout(p) * 0.7, stroke=2 * u)
                for k in range(40):
                    an = k / 40 * 6.28; circle(c, x + math.cos(an) * (rin + R) / 2, 0.48 * H + math.sin(an) * (rin + R) / 2, 5 * u, "#3a2e24", eout(p))
                text(c, lab, x, 0.48 * H + R + 60 * u, 32 * u, "#ffffff", eout(p), w=800)
                chip(c, f"{int(bark_f * 100)}% BARK", x, 0.48 * H - R - 60 * u, p, 34 * u, bg="#5a4a3a")
            chip(c, "VERY LITTLE LIGNIN", W * 0.3, 0.9 * H, vis(t, B(0, 0.35)), 32 * u, dot="#e0c08a")
    with Layer(c, pB) as on:
        if on:
            fx, fy = W * 0.27, 0.5 * H
            rrect(c, fx - 260 * u, fy - 90 * u, 520 * u, 180 * u, 40 * u, "#6a6058")
            for k in range(7): line(c, fx - 240 * u, fy - 60 * u + k * 20 * u, fx + 240 * u, fy - 60 * u + k * 20 * u, "#5a5048", 3 * u)
            mp = prog(t, B(1, 0.1), 0.5)
            mx, my = fx + 80 * u, fy
            circle(c, mx, my, 110 * u, "#2a2420", mp); circle(c, mx, my, 110 * u, "#ffffff", mp, stroke=10 * u)
            line(c, mx + 78 * u, my + 78 * u, mx + 170 * u, my + 170 * u, "#ffffff", 18 * u, mp)
            for k in range(8):
                rng = random.Random(k); oval(c, mx + rng.uniform(-60, 60) * u, my + rng.uniform(-60, 60) * u, 16 * u, 9 * u, "#e9d3a8", mp)
            chip(c, "FOSSIL WOOD: ALREADY ROTTED BY FUNGI", fx, 0.2 * H, mp, 30 * u, dot="#e9d3a8")
            gx0, gx1, gy = W * 0.56, W * 0.92, 0.66 * H
            gp = prog(t, B(1, 0.45), 0.5)
            line(c, gx0, gy, gx1, gy, "#ffffff", 4 * u, gp)
            line(c, gx0, gy, gx0, gy - 300 * u, "#ffffff", 4 * u, gp)
            mid = (gx0 + gx1) / 2
            rect(c, gx0 + 5 * u, gy - 300 * u, mid - gx0 - 5 * u, 300 * u, "#4caf50", 0.15 * gp)
            rect(c, mid, gy - 300 * u, gx1 - mid, 300 * u, "#9aa4b8", 0.15 * gp)
            pl = ease(prog(t, B(1, 0.55), 1.0))
            line(c, gx0, gy - 160 * u, lerp(gx0, gx1, pl), gy - 160 * u + math.sin(t * 2) * 2, ACCENT, 9 * u, gp)
            text(c, "WOODY SWAMPS", (gx0 + mid) / 2, gy + 40 * u, 24 * u, "#cfe3ff", gp, w=700, fam="Inter")
            text(c, "NON-WOODY", (mid + gx1) / 2, gy + 40 * u, 24 * u, "#cfe3ff", gp, w=700, fam="Inter")
            chip(c, "COAL PILED UP AT THE SAME RATE", (gx0 + gx1) / 2, gy - 380 * u, vis(t, B(1, 0.7)), 28 * u, bg=ACCENT, fg="#0b1030", a=1)

def a_pangea(c, W, H, t, S):
    u = S.u; B = beats(S, 5)
    p0 = phase(t, None, B(1, 0)); p1 = phase(t, B(1, 0), B(2, 0)); p2 = phase(t, B(2, 0), B(3, 0)); p3 = phase(t, B(3, 0), B(4, 0)); p4 = phase(t, B(4, 0))
    if p0 + p2 > 0: space_bg(c, W, H, t, 1, seed=13)
    with Layer(c, p0) as on:
        if on:
            pangea_globe(c, W / 2, 0.52 * H, 360 * u, rot=-10 + t * 4, tilt=12)
            line(c, W / 2 - 400 * u, 0.52 * H + 40 * u, W / 2 + 400 * u, 0.52 * H + 40 * u, ACCENT, 3 * u, 0.6, dash=([16 * u, 12 * u], 0))
            chip(c, "PANGEA", W / 2, 0.1 * H, vis(t, B(0, 0.2)), 46 * u, dot="#4caf5a")
            chip(c, "WET, SINKING BASINS AT THE EQUATOR", W / 2, 0.93 * H, vis(t, B(0, 0.6)), 32 * u, dot="#7ec8ff")
    with Layer(c, p1) as on:
        if on:
            wl = 0.45 * H
            _swamp_bg(c, W, H, t, u, wl, mist=0.2)
            sink = ease(prog(t, B(1, 0), 4))
            for k in range(5):
                y = 0.7 * H + k * 50 * u - sink * 40 * u
                rect(c, 0, y, W, 50 * u, mix("#4a3a2a", "#20180f", k / 5))
                for j in range(6):
                    rng = random.Random(k * 10 + j); log(c, rng.random() * W, y + 25 * u, 200 * u, 12 * u, "#5b4030", ang=rng.uniform(-8, 8))
            for k in range(6):
                rng = random.Random(k + 50); pp = prog(t, B(1, 0) + k * 0.6, 2.5)
                log(c, rng.uniform(0.1, 0.9) * W, lerp(wl - 60 * u, 0.68 * H, ease(pp)), 220 * u, 16 * u, "#6b4a33", ang=rng.uniform(-30, 30) * (1 - pp))
            chip(c, "WATERLOGGED: ROT SLOWS TO A CRAWL", W / 2, 0.1 * H, vis(t, B(1, 0.2)), 34 * u)
    if p2 > 0:
        big_text(c, W, H, "BURIED FASTER", 0.42 * H, p2 * prog(t, B(2, 0), 0.4), u, size=130)
        big_text(c, W, H, "THAN THEY COULD ROT", 0.58 * H, p2 * prog(t, B(2, 0.2), 0.4), u, colr=ACCENT, size=110)
    with Layer(c, p3) as on:
        if on:
            dark_bg(c, W, H)
            for k, (lab, out, colr, dx) in enumerate([("CARBON BURIED", "COOLER", "#7ec8ff", -0.22), ("CARBON RELEASED", "WARMER", "#ff7a4d", 0.22)]):
                p = prog(t, B(3, 0.1 + 0.3 * k), 0.4); x = W * (0.5 + dx)
                chip(c, lab, x, 0.35 * H, p, 40 * u, dot=colr)
                arrow(c, x, 0.43 * H, x, 0.55 * H, "#ffffff", 10 * u, eout(p))
                text(c, out, x, 0.64 * H, 90 * u, colr, eout(p), w=900, shadow=10)
            chip(c, "NOT IN DOUBT", W / 2, 0.85 * H, vis(t, B(3, 0.7)), 36 * u, bg=ACCENT, fg="#0b1030", a=1)
    with Layer(c, p4) as on:
        if on:
            fill_bg(c, W, H, "#3a3a46", "#8a8a96")
            fx = W * 0.62
            rect(c, fx - 260 * u, 0.62 * H, 520 * u, 0.38 * H, "#2a2a33")
            for k in range(3):
                rect(c, fx - 200 * u + k * 150 * u, 0.3 * H, 60 * u, 0.32 * H, "#2a2a33")
                smoke(c, fx - 170 * u + k * 150 * u, 0.3 * H, t + k, u, a=1, seed=k, col_="#4a4a55", rise=280)
            coal_lump(c, W * 0.22, 0.6 * H, 120 * u, glow=0.4 + 0.2 * math.sin(t * 3))
            arrow(c, W * 0.32, 0.6 * H, fx - 300 * u, 0.6 * H, "#ffffff", 10 * u, 0.9)
            chips(c, t, [(B(4, 0.2), None, "LOCKED AWAY: MILLIONS OF YEARS", "#16161c"), (B(4, 0.6), None, "RELEASED: A COUPLE OF CENTURIES", "#ff7a4d")],
                  W / 2, 0.1 * H, 80 * u, u, 34)

SCENES = {k: v for k, v in globals().items() if k.startswith("a_") and callable(v)}
