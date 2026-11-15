"""Batch 03 scenes: What If Earth Had Rings? (+ Earth-rings teaser and Saturn-losing-its-rings Shorts).
Motif: a planet wrapped by a tilted ring (back half / planet / front half). Palette: violet night + sand-grey rock."""
from common2 import *
import geo
import scenes_b3_kit as kit

PAL = dict(accent="#FFB36B", chip="#2a1a4a", title2=ACCENT)
ROCK = "#c4b49a"; ROCK_D = "#8f8577"; ICE = "#f1e6c8"; ORANGE = "#FFB36B"
SKY_T, SKY_B = "#0d0a24", "#2a1a4a"

# ------------------------------------------------------------------ helpers
def bg(c, W, H, t, S):
    fill_bg(c, W, H, SKY_T, SKY_B)
    stars(c, W, H, t, 0.9, seed=31, drift=(-5, 0))

def lay(S):
    """centre x, centre y, scale of the main art."""
    if S.P: return S.W / 2, 0.415 * S.H, 0.82
    return S.W / 2, 0.53 * S.H, 1.0

def ytop(S): return 0.27 * S.H if S.P else 0.09 * S.H
def ybot(S): return 0.565 * S.H if S.P else 0.92 * S.H

def ring(c, cx, cy, r_in, r_out, k, half=None, colr=ROCK, a=1.0, rot=0.0, n=6, gap=None):
    if a <= 0 or r_out <= 0: return
    c.save(); c.translate(cx, cy); c.rotate(rot)
    if half == "back": c.clipRect(skia.Rect.MakeLTRB(-1e4, -1e4, 1e4, 0))
    elif half == "front": c.clipRect(skia.Rect.MakeLTRB(-1e4, 0, 1e4, 1e4))
    ky = max(k, 0.004)
    p = skia.Path(); p.setFillType(skia.PathFillType.kEvenOdd)
    p.addOval(skia.Rect.MakeLTRB(-r_out, -r_out * ky, r_out, r_out * ky))
    p.addOval(skia.Rect.MakeLTRB(-r_in, -r_in * ky, r_in, r_in * ky))
    c.drawPath(p, paint(colr, a * 0.9))
    w = (r_out - r_in) / n
    for i in range(n):
        r = r_in + w * (i + 0.5)
        shade = mix(colr, "#ffffff" if i % 2 else "#2a2030", 0.18 + 0.1 * (i % 3))
        c.drawOval(skia.Rect.MakeLTRB(-r, -r * ky, r, r * ky), paint(shade, a * 0.45, stroke=w * 0.45))
    if gap:
        r = lerp(r_in, r_out, gap)
        c.drawOval(skia.Rect.MakeLTRB(-r, -r * ky, r, r * ky), paint("#120a26", a * 0.8, stroke=max(2, w * 0.35)))
    if k < 0.03:
        line(c, -r_out, 0, r_out, 0, colr, 3, a)
    c.restore()

def ringed_earth(c, cx, cy, R, t, k=0.34, rin=1.25, rout=2.45, ring_a=1.0, rot=-12, colr=ROCK, spin=8, tilt=20, ice=0.0, a=1.0,
                 cap=None, shadow=0.0):
    R = max(4, int(R) // 4 * 4)
    c.save(); c.translate(cx, cy); c.rotate(rot)
    ring(c, 0, 0, R * rin, R * rout, k, "back", colr, ring_a * a)
    kw = {}
    if cap is not None: kw = dict(cap_s=-cap, cap_n=cap)
    geo.globe(c, 0, 0, R, rot=(t * spin) % 360 - 60, tilt=tilt, a=a, **kw)
    if shadow > 0:  # ring shadow band across the tropics
        c.save(); pth = skia.Path(); pth.addCircle(0, 0, R); c.clipPath(pth, doAntiAlias=True)
        rect(c, -R, -R * 0.28, 2 * R, R * 0.56, "#05030f", 0.45 * shadow * a)
        c.restore()
    ring(c, 0, 0, R * rin, R * rout, k, "front", colr, ring_a * a)
    c.restore()

def motif(c, W, H, t, S, cx, cy, s):
    ringed_earth(c, cx, cy, int(190 * S.u * s), t)

def saturn(c, cx, cy, R, t, k=0.3, ring_a=1.0, rot=-10, a=1.0):
    c.save(); c.translate(cx, cy); c.rotate(rot)
    rings = [(1.11, 1.24, "#7d7360", 0.35), (1.24, 1.53, "#bfae8a", 0.6), (1.53, 1.95, ICE, 0.95), (2.03, 2.27, "#e4d3ab", 0.85)]
    for r0, r1, colr, al in rings: ring(c, 0, 0, R * r0, R * r1, k, "back", colr, al * ring_a * a, n=4)
    ry = R * 0.9
    c.save(); pth = skia.Path(); pth.addOval(skia.Rect.MakeLTRB(-R, -ry, R, ry)); c.clipPath(pth, doAntiAlias=True)
    cols = ["#f0dcae", "#e2c48c", "#d8b77c", "#ecd5a2", "#c9a46a", "#e6cd98", "#d4b07a", "#f0dcae"]
    for i, cl in enumerate(cols):
        y0 = -ry + 2 * ry * i / len(cols)
        rect(c, -R, y0 + math.sin(t * 0.5 + i) * 2, 2 * R, 2 * ry / len(cols) + 3, cl, a)
    c.drawPaint(paint(shader=rad(-R * 0.35, -ry * 0.4, R * 1.8, [(0, "#ffffff", 0.18), (0.6, "#000000", 0.0), (1, "#000000", 0.55)]), a=a))
    c.restore()
    for r0, r1, colr, al in rings: ring(c, 0, 0, R * r0, R * r1, k, "front", colr, al * ring_a * a, n=4)
    c.restore()

def planet(c, x, y, r, colr, a=1.0, bands=None):
    circle(c, x, y, r, colr, a)
    if bands:
        c.save(); p = skia.Path(); p.addCircle(x, y, r); c.clipPath(p, doAntiAlias=True)
        for i, bc in enumerate(bands):
            rect(c, x - r, y - r + 2 * r * (i + 0.3) / len(bands), 2 * r, r * 0.16, bc, a * 0.7)
        c.restore()
    c.drawCircle(x, y, r, paint(shader=rad(x - r * 0.4, y - r * 0.4, r * 1.9, [(0, "#ffffff", 0.2), (0.55, "#000000", 0), (1, "#000000", 0.6)]), a=a))

def chunks_(c, cx, cy, rmin, rmax, k, t, n=90, seed=3, a=1.0, half=None, colr=ROCK, size=4.0, spread=1.0, rot0=0.0, speed=0.15):
    """ring particles as dots (top/bottom half selectable)."""
    rng = random.Random(seed)
    for i in range(n):
        r = lerp(rmin, rmax, rng.random()); ang = rng.random() * 6.283 * spread + rot0 + t * speed * (rmin / max(r, 1e-6)) ** 1.5
        s_ = math.sin(ang)
        if half == "back" and s_ > 0: continue
        if half == "front" and s_ <= 0: continue
        circle(c, cx + math.cos(ang) * r, cy + s_ * r * k, size * rng.uniform(0.5, 1.4), mix(colr, "#ffffff", rng.random() * 0.4), a)

def meteor(c, x, y, ang, L, a=1.0, w=4):
    x1, y1 = x - math.cos(ang) * L, y - math.sin(ang) * L
    c.drawLine(x, y, x1, y1, paint(shader=lin(x, y, x1, y1, [(0, "#fff2c8", a), (0.3, ORANGE, 0.7 * a), (1, "#ff6b35", 0)]), stroke=w))
    circle(c, x, y, w * 1.2, "#fff6dd", a)

def landscape_sky(c, W, H, t, top, bot): fill_bg(c, W, H, top, bot)

def mountains(c, W, base, H, color, seed, amp, n=7):
    rng = random.Random(seed); pts = [(0, H), (0, base)]
    for i in range(n + 1):
        x = W * i / n
        pts.append((x - W / n * 0.5, base - amp * rng.uniform(0.4, 1.0)))
        pts.append((x, base - amp * rng.uniform(0.0, 0.25)))
    pts += [(W, base), (W, H)]
    c.drawPath(poly(pts), paint(color))

def palm(c, x, y, h, color="#14402a", a=1.0):
    p = skia.Path(); p.moveTo(x, y); p.quadTo(x + h * 0.08, y - h * 0.5, x + h * 0.03, y - h)
    c.drawPath(p, paint("#3a2a1a", a, stroke=h * 0.05))
    tx, ty = x + h * 0.03, y - h
    for k in range(7):
        ang = math.radians(-170 + k * 27)
        q = skia.Path(); q.moveTo(tx, ty)
        q.quadTo(tx + math.cos(ang) * h * 0.25, ty + math.sin(ang) * h * 0.25 - h * 0.05, tx + math.cos(ang) * h * 0.42, ty + math.sin(ang) * h * 0.42 + h * 0.12)
        c.drawPath(q, paint(color, a, stroke=h * 0.05))

def arch(c, cx, base, rx, ry, thick, colr="#efe6d6", a=1.0, glow=0.0, gap=None):
    """upper half of an ellipse band, as seen in the sky."""
    if a <= 0: return
    c.save(); c.clipRect(skia.Rect.MakeLTRB(-1e4, -1e4, 1e4, base))
    r_ = skia.Rect.MakeLTRB(cx - rx, base - ry, cx + rx, base + ry)
    if glow: c.drawOval(r_, paint(colr, a * 0.25 * glow, stroke=thick * 3, blur=thick))
    c.drawOval(r_, paint(colr, a * 0.85, stroke=thick))
    for f, al in ((-0.32, 0.5), (0.0, 0.35), (0.3, 0.6)):
        r2 = skia.Rect.MakeLTRB(cx - rx - f * thick, base - ry - f * thick, cx + rx + f * thick, base + ry + f * thick)
        c.drawOval(r2, paint("#ffffff" if f else "#9a8f80", a * al, stroke=max(1.5, thick * 0.08)))
    if gap:  # dark wedge: Earth's shadow on the rings
        a0, a1 = gap
        p = skia.Path(); p.addArc(r_, a0, a1 - a0)
        c.drawPath(p, paint("#06041a", a * 0.92, stroke=thick * 1.15, cap="butt"))
    c.restore()

# ------------------------------------------------------------------ generic
def r_title(c, W, H, t, S): kit.title(c, W, H, t, S, bg, motif, PAL)
def r_card(c, W, H, t, S):
    def cbg(c, W, H, t, S):
        bg(c, W, H, t, S)
        ringed_earth(c, W * 0.5, H * 0.5, int(H * (0.18 if not S.P else 0.1)), t, a=0.5)
    kit.card(c, W, H, t, S, cbg, PAL)
def r_end(c, W, H, t, S): kit.end(c, W, H, t, S, bg, motif, PAL)
def r_endshort(c, W, H, t, S): kit.end_short(c, W, H, t, S, bg, motif, PAL)

# ------------------------------------------------------------------ Saturn
def r_saturn(c, W, H, t, S):
    u = S.u; o = S.opts; mode = o.get("mode", "intro"); cx, cy, sc = lay(S)
    bg(c, W, H, t, S)
    R = 150 * u * sc * (1.0 if not S.P else 1.05)
    if mode == "intro":
        R = (190 if not S.P else 170) * u
        long_ = S.n() >= 3; B = beats(S, 3)
        pA = phase(t, None, B(2, 0)) if long_ else 1.0
        with Layer(c, pA) as on:
            if on:
                # rings tilt toward edge-on during the first line
                q = ease(prog(t, B(0, 0.55), 2.5)) if long_ else ease(prog(t, S.lt(0, 0.5), 1.4))
                k = lerp(0.32, 0.012, q)
                zoom = lerp(1.0, 1.15, q)
                saturn(c, cx, cy, R * zoom, t, k=k, rot=lerp(-10, 0, q))
                ytx = cy + R * zoom * 0.9 + 70 * u
                if q < 0.5:
                    pa = vis(t, B(0, 0.1) if long_ else 0.1, None) * (1 - q * 2)
                    x0, x1 = cx - R * 2.27, cx + R * 2.27
                    arrow(c, cx, cy + R * 1.25, x0, cy + R * 1.25, "#ffffff", 4 * u, pa); arrow(c, cx, cy + R * 1.25, x1, cy + R * 1.25, "#ffffff", 4 * u, pa)
                    chip(c, "273,000+ KM ACROSS", cx, cy + R * 1.25 + 50 * u, pa, 32 * u, bg=PAL["chip"])
                else:
                    chip(c, "~10 M THICK", cx, ytx, prog(t, B(0, 0.75) if long_ else S.lt(0, 0.85), 0.4), 36 * u, bg=ORANGE, fg="#0b1030", a=1)
                if long_:
                    pp = vis(t, B(1, 0.05))
                    if pp > 0:
                        # paper sheet comparison
                        px = W * (0.15 if not S.P else 0.2); py = ytop(S) + (110 if not S.P else 120) * u
                        c.save(); c.translate(px, py); c.rotate(-8); c.scale(1.3, 1.3)
                        rrect(c, -60 * u, -78 * u, 120 * u, 156 * u, 6 * u, "#ffffff", pp)
                        for i in range(5): line(c, -40 * u, (-45 + i * 22) * u, 40 * u, (-45 + i * 22) * u, "#9fb3d6", 2 * u, pp)
                        c.restore()
                        text(c, "A SHEET OF PAPER IS", px, py + 140 * u, 30 * u, "#ffffff", pp, w=800, shadow=6)
                        text(c, "THICKER, FOR ITS SIZE", px, py + 180 * u, 30 * u, ORANGE, pp, w=900, shadow=6)
                    chip(c, "ALL THE RINGS ≈ 40% OF MOON MIMAS", cx, ytop(S), vis(t, B(1, 0.55)), 32 * u, bg=PAL["chip"], dot=ICE)
        if long_:
            pB = phase(t, B(2, 0))
            with Layer(c, pB) as on:
                if on:
                    bg(c, W, H, t, S)
                    ringed_earth(c, cx, cy, int(170 * u * sc), t, ring_a=ease(prog(t, B(2, 0.15), 1.2)))
                    text(c, "?", W * (0.85 if not S.P else 0.82), cy - 40 * u, 200 * u, ORANGE, prog(t, B(2, 0.6), 0.4), w=900, shadow=12)
    elif mode in ("rain", "pool", "fade", "age"):
        long_ = S.n() >= 3; B = beats(S, 3)
        fade = 1.0
        if mode == "fade": fade = 1 - 0.85 * ease(prog(t, S.lt(0, 0.2), S.dur * 0.6))
        if long_: fade = 1 - 0.8 * ease(prog(t, B(1, 0.2), 3.0))
        pA = phase(t, None, B(2, 0)) if long_ else 1.0
        with Layer(c, pA) as on:
            if on:
                big = mode in ("rain",)
                sx, sy = (cx, cy) if (big or S.P) else (W * 0.33, cy)
                RR = R * (1.0 if big or S.P else 0.85)
                if S.P:
                    if mode == "rain": RR = 190 * u; sy = cy
                    else: RR = 125 * u; sy = 0.37 * H
                saturn(c, sx, sy, RR, t, k=0.3, ring_a=fade)
                # ring rain: ice grains curving from the inner ring into mid-latitudes
                if mode in ("rain", "pool") or long_:
                    rng = random.Random(5)
                    c.save(); c.translate(sx, sy); c.rotate(-10)
                    for i in range(40):
                        side = 1 if i % 2 else -1; ph = rng.random(); q = (ph + t * 0.35) % 1
                        x0 = side * RR * rng.uniform(1.15, 1.5); y0 = rng.uniform(-6, 6)
                        lat = rng.uniform(0.35, 0.6) * (1 if i % 4 < 2 else -1)
                        x1 = side * RR * math.cos(lat) * 0.85; y1 = -RR * 0.9 * math.sin(lat)
                        x = lerp(x0, x1, q); y = lerp(y0, y1, q) - math.sin(q * math.pi) * 20 * u * (1 if y1 < 0 else -1)
                        circle(c, x, y, 5 * u, "#dff4ff", math.sin(q * math.pi) * fade)
                        circle(c, x, y, 11 * u, "#bfe8ff", 0.25 * math.sin(q * math.pi) * fade)
                    c.restore()
                if mode == "rain" and not long_:
                    chip(c, "~98% WATER ICE", cx, ybot(S), vis(t, S.lt(0, 0.35)), 34 * u, bg=PAL["chip"], dot=ICE)
                if mode == "pool" or long_:
                    px = (W * 0.72 if not S.P else W / 2); py = (cy if not S.P else 0.5 * H)
                    pw, ph = (420 * u, 190 * u) if not S.P else (520 * u, 150 * u)
                    pp = vis(t, B(0, 0.25) if long_ else S.lt(0, 0.05))
                    if long_ and not S.P: px, py = W * 0.74, cy - 40 * u
                    with Layer(c, pp * (1 - (prog(t, B(1, 0), 0.4) if long_ else 0))) as on2:
                        if on2:
                            rrect(c, px - pw / 2 - 10 * u, py - ph / 2 - 10 * u, pw + 20 * u, ph + 20 * u, 14 * u, "#e9eef6")
                            lvl = ease(prog(t, B(0, 0.3) if long_ else S.lt(0, 0.1), 4.0))
                            rect(c, px - pw / 2, py - ph / 2, pw, ph, "#24304a")
                            rect(c, px - pw / 2, py + ph / 2 - ph * lvl, pw, ph * lvl, "#4fb7ff")
                            for i in range(1, 8): line(c, px - pw / 2, py - ph / 2 + ph * i / 8, px + pw / 2, py - ph / 2 + ph * i / 8, "#ffffff", 2 * u, 0.25)
                            text(c, "OLYMPIC POOL", px, py - ph / 2 - 40 * u, 36 * u, "#ffffff", 1, w=900, shadow=6)
                            clock(c, px + pw / 2 - 10 * u, py - ph / 2 - 10 * u, 34 * u, lvl * 0.5, colr=ORANGE)
                            text(c, "EVERY ~30 MIN", px, py + ph / 2 + 46 * u, 36 * u, ORANGE, 1, w=900, shadow=6)
                    if mode == "pool":
                        chip(c, "CASSINI: UP TO 10,000 KG/S", cx, ytop(S), vis(t, S.lt(0, 0.55)), 34 * u, bg=ORANGE, fg="#0b1030", a=1)
                    if long_:
                        chip(c, "RING RAIN", sx, ytop(S), vis(t, B(0, 0.05), B(1, 0)), 36 * u, bg=PAL["chip"], dot=ICE)
                if mode == "fade" or long_:
                    pf = vis(t, B(1, 0.05)) if long_ else vis(t, 0.2)
                    bx = W * 0.12 if not S.P else W * 0.1; bw = W * 0.76 if not S.P else W * 0.8
                    by = ybot(S) - (10 if not S.P else 0) * u
                    q = ease(prog(t, B(1, 0.2) if long_ else S.lt(0, 0.2), 3.0 if long_ else S.dur * 0.6))
                    bar(c, bx, by, bw, 26 * u, q, ORANGE, u, a=pf)
                    text(c, "NOW", bx, by - 34 * u, 34 * u, "#ffffff", pf, w=800, align="l")
                    text(c, "< 100 MILLION YEARS", bx + bw, by - 34 * u, 34 * u, ORANGE, pf, w=900, align="r")
                if mode == "age":
                    pa = vis(t, S.lt(0, 0.05))
                    bx = W * 0.1; bw = W * 0.8; by = ybot(S) - 40 * u
                    line(c, bx, by, bx + bw, by, "#ffffff", 4 * u, pa)
                    for f_, lab, col_, d in ((0.02, "10–100 MILLION YRS?", ORANGE, 0.1), (0.98, "4.5 BILLION YRS?", "#9fd3ff", 0.55)):
                        pq = vis(t, S.lt(0, d))
                        circle(c, bx + bw * f_, by, 14 * u, col_, pq)
                        text(c, lab, bx + bw * f_, by + 50 * u, 36 * u, col_, pq, w=900, align="l" if f_ < 0.5 else "r")
                    text(c, "CASSINI DATA", bx, by - 40 * u, 30 * u, "#ffffff", vis(t, S.lt(0, 0.1)), w=700, fam="Inter", align="l")
                    text(c, "2024 STUDY", bx + bw, by - 40 * u, 30 * u, "#ffffff", vis(t, S.lt(0, 0.55)), w=700, fam="Inter", align="r")
        if long_:
            pB = phase(t, B(2, 0))
            with Layer(c, pB) as on:
                if on:
                    bg(c, W, H, t, S)
                    ra = 1 - 0.75 * ease(prog(t, B(2, 0.2), 3.0))
                    ringed_earth(c, cx, cy, int(170 * u * sc), t, ring_a=ra)
                    chip(c, "EARTH'S RINGS: A FEW TENS OF MILLIONS OF YEARS?", cx, ytop(S), vis(t, B(2, 0.1)), 30 * u, bg=PAL["chip"], dot=ORANGE)
    kit.hook(c, W, H, t, S)

# ------------------------------------------------------------------ setup
def r_roche(c, W, H, t, S):
    u = S.u; B = beats(S, 3); cx, cy, sc = lay(S); bg(c, W, H, t, S)
    R = int(118 * u * sc) // 4 * 4; LIM = R * 2.9
    k = lerp(1.0, 0.36, ease(prog(t, B(2, 0.3), 2.0)))
    # Roche circle
    pc = 0.35 + 0.65 * vis(t, B(1, 0.0))
    c.drawOval(skia.Rect.MakeLTRB(cx - LIM, cy - LIM * k, cx + LIM, cy + LIM * k), paint(ORANGE, 0.85 * pc, stroke=4 * u, dash=([18 * u, 12 * u], -t * 20)))
    # moon path: spiral in from the right during line 0, break at line 1 end
    tb = B(1, 0.6)
    pieces = []
    if t < tb:
        q = prog(t, 0.0, tb)
        r = lerp(LIM * 1.9, LIM * 0.98, ease(q)); ang = lerp(-0.2, 1.9, q)
        stretch = 1 + 0.6 * clamp((LIM * 1.35 - r) / (LIM * 0.4)) + (0.5 if q > 0.9 else 0)
        mx, my = cx + math.cos(ang) * r, cy + math.sin(ang) * r * k
        c.save(); c.translate(mx, my); c.rotate(math.degrees(ang)); c.scale(stretch, 1 / stretch ** 0.4)
        moon(c, 0, 0, 44 * u * sc, lit=0.9); c.restore()
        if t > 0.3:
            for sgn in (-1, 1):
                ax = mx + math.cos(ang) * sgn * 70 * u; ay = my + math.sin(ang) * sgn * 70 * u * k
                arrow(c, mx + math.cos(ang) * sgn * 40 * u, my + math.sin(ang) * sgn * 40 * u * k, ax, ay, "#ff8a8a", 5 * u, vis(t, 0.3) * 0.9)
    else:
        q = ease(prog(t, tb, 3.5))
        rng = random.Random(9)
        for i in range(160):
            rr = LIM * 0.98 * lerp(1.0, rng.uniform(0.45, 1.0), q)
            ang = 1.9 + (rng.random() - 0.5) * lerp(0.3, 6.28, q) + t * 0.12 * (LIM / rr)
            pieces.append((ang, rr, rng.uniform(2, 5) * u))
    for half in ("back", "front"):
        for ang, rr, s_ in pieces:
            if (math.sin(ang) > 0) != (half == "front"): continue
            circle(c, cx + math.cos(ang) * rr, cy + math.sin(ang) * rr * k, s_, mix(ROCK, "#ffffff", 0.2))
        if half == "back":
            geo.globe(c, cx, cy, R, rot=(t * 8) % 360, tilt=lerp(85, 20, ease(prog(t, B(2, 0.3), 2.0))))
    chip(c, "TIDES BEAT THE MOON'S GRAVITY", cx, ytop(S), vis(t, B(0, 0.4), B(1, 0)), 32 * u, bg=PAL["chip"], dot="#ff8a8a")
    chip(c, "ROCHE LIMIT ≈ 3 EARTH RADII", cx, ytop(S), vis(t, B(1, 0.1), B(2, 0)), 34 * u, bg=ORANGE, fg="#0b1030", a=1)
    chip(c, "~12,000 KM ABOVE YOU", cx + LIM * 0.7, cy + LIM * k + 46 * u if not S.P else ybot(S), vis(t, B(1, 0.55), B(2, 0)), 30 * u, bg=PAL["chip"])
    chip(c, "INSIDE THE LINE: NO NEW MOON", cx, ytop(S), vis(t, B(2, 0.35)), 32 * u, bg=PAL["chip"], dot=ROCK)

def r_material(c, W, H, t, S):
    u = S.u; B = beats(S, 3); cx, cy, sc = lay(S); bg(c, W, H, t, S)
    pA = phase(t, None, B(2, 0))
    with Layer(c, pA) as on:
        if on:
            if S.P:
                boxes = [(W * 0.06, 0.255 * H, W * 0.88, 0.14 * H), (W * 0.06, 0.415 * H, W * 0.88, 0.14 * H)]
            else:
                boxes = [(W * 0.05, 0.17 * H, W * 0.43, 0.62 * H), (W * 0.52, 0.17 * H, W * 0.43, 0.62 * H)]
            for j, (x, y, w, h) in enumerate(boxes):
                pj = vis(t, B(j, 0.0) if j else 0.05)
                if pj <= 0: continue
                with Layer(c, pj) as o2:
                    if not o2: continue
                    rrect(c, x, y, w, h, 18 * u, "#120a26", 0.92)
                    c.save(); c.clipRect(skia.Rect.MakeXYWH(x, y, w, h))
                    rng = random.Random(4 + j)
                    for i in range(70):
                        px = x + ((rng.random() + t * 0.01 * (1 + i % 3)) % 1) * w; py = y + rng.random() * h
                        r = (rng.random() ** 3) * 40 * u + 3 * u
                        if j == 0:
                            circle(c, px, py, r, mix("#ffffff", "#bfe3ff", rng.random()), 0.95)
                            circle(c, px - r * 0.3, py - r * 0.3, r * 0.35, "#ffffff", 0.9)
                        else:
                            pts = [(px + math.cos(a_) * r * rng.uniform(0.7, 1.1), py + math.sin(a_) * r * rng.uniform(0.7, 1.1)) for a_ in [k_ * 0.9 for k_ in range(7)]]
                            c.drawPath(poly(pts), paint(mix(ROCK_D, "#5d5248", rng.random()), 1))
                    c.restore()
                    lab = "SATURN: ~98% WATER ICE" if j == 0 else "EARTH: ROCK + DUST"
                    chip(c, lab, x + w / 2, y + h - 40 * u, 1, 30 * u, bg="#0b1030", dot=ICE if j == 0 else ROCK_D)
            if not S.P:
                ph = vis(t, B(0, 0.55), B(1, 0))
                if ph > 0:
                    x, y, w, h = boxes[0]
                    house(c, x + w * 0.78, y + h * 0.42, 110 * u, a=ph)
                    text(c, "CHUNKS UP TO HOUSE-SIZED", x + w / 2, y - 40 * u, 34 * u, "#ffffff", ph, w=900, shadow=6)
                ps = vis(t, B(1, 0.4))
                if ps > 0:
                    x, y, w, h = boxes[1]
                    sun(c, x + w - 70 * u, y + 70 * u, 40 * u, t, a=ps)
                    text(c, "ICE → VAPOR", x + w * 0.38, y + 60 * u, 34 * u, ORANGE, ps, w=900, shadow=6)
            else:
                chip(c, "PIECES UP TO HOUSE-SIZED", W / 2, ytop(S) - 0 * u, vis(t, B(0, 0.55), B(1, 0)), 28 * u, bg=PAL["chip"])
    pB = phase(t, B(2, 0))
    with Layer(c, pB) as on:
        if on:
            bg(c, W, H, t, S)
            # altitude column
            x0 = W * (0.35 if not S.P else 0.3); gy = (0.86 if not S.P else 0.565) * H; top_ = (0.16 if not S.P else 0.3) * H
            hh = gy - top_
            c.drawRect(skia.Rect.MakeLTRB(0, gy, W, gy + 400 * u), paint(shader=rad(W / 2, gy + 2400 * u, 2400 * u, [(0.97, "#1f6fd1", 1), (1, "#7fd0ff", 1)])))
            c.drawRect(skia.Rect.MakeLTRB(0, gy - 60 * u, W, gy), paint(shader=lin(0, gy - 60 * u, 0, gy, [(0, "#5aa9ff", 0), (1, "#5aa9ff", 0.5)])))
            def yk(km): return gy - hh * km / 12500
            line(c, x0, gy, x0, top_, "#ffffff", 3 * u, 0.8)
            for km in (1000, 6000, 12000):
                line(c, x0 - 12 * u, yk(km), x0 + 12 * u, yk(km), "#ffffff", 3 * u)
                text(c, f"{km:,} KM", x0 - 24 * u, yk(km), 26 * u, "#ffffff", 0.9, w=700, fam="Inter", align="r")
            pr = ease(prog(t, B(2, 0.05), 0.8))
            rrect(c, x0 + 40 * u, yk(12000), W * 0.42 * pr, yk(1000) - yk(12000), 16 * u, ROCK, 0.28)
            text(c, "THE RING", x0 + 40 * u + W * 0.21 * pr, yk(6500), 44 * u, "#ffffff", pr, w=900, shadow=8)
            chunks_(c, x0 + 40 * u + W * 0.21 * pr, (yk(1000) + yk(12000)) / 2, 0, W * 0.2 * pr, (yk(1000) - yk(12000)) / (W * 0.42) , t, n=70, colr=ROCK)
            line(c, x0 + 30 * u, yk(1000), W * 0.95, yk(1000), ORANGE, 4 * u, pr, dash=([14 * u, 10 * u], 0))
            text(c, "INNER EDGE ~1,000 KM", x0 + 60 * u + W * 0.42 * pr * 0.5, yk(1000) + 40 * u, 30 * u, ORANGE, pr, w=900, shadow=6)
            rng = random.Random(2)
            for i in range(6):
                q = (t * 0.6 + i / 6) % 1
                mx = x0 + 80 * u + rng.random() * W * 0.45 + q * 80 * u; my = lerp(yk(1000), gy - 10 * u, q)
                meteor(c, mx, my, math.radians(65), 90 * u, a=vis(t, B(2, 0.5)) * math.sin(q * math.pi), w=4 * u)
            chip(c, "LOWER = BURNS UP AS METEORS", W / 2, ytop(S), vis(t, B(2, 0.55)), 32 * u, bg=PAL["chip"], dot=ORANGE)

# ------------------------------------------------------------------ sky views
PLACES = {0: ("QUITO, ON THE EQUATOR", -78.5, -0.2), 38: ("WASHINGTON, D.C.", -77.0, 38.9), 66: ("ARCTIC CIRCLE", 25.0, 66.6)}

def inset_globe(c, W, H, t, S, lat):
    u = S.u; lab, lon, la = PLACES[lat]
    gx, gy = (W * 0.89, 0.2 * H) if not S.P else (W * 0.84, 0.335 * H)
    R = 76
    rot = lon + 15 * math.sin(t * 0.4); tilt = clamp(la, 10, 50) if lat else 15
    circle(c, gx, gy, R + 8, "#0b1030", 0.6)
    ring(c, gx, gy, R * 1.2, R * 1.9, math.sin(math.radians(tilt)), "back", ROCK, 0.9, n=3)
    geo.globe(c, gx, gy, R, rot=rot, tilt=tilt)
    ring(c, gx, gy, R * 1.2, R * 1.9, math.sin(math.radians(tilt)), "front", ROCK, 0.9, n=3)
    x, y, v = geo.globe_xy(lon, la, gx, gy, R, rot, tilt)
    if v:
        circle(c, x, y, 9, "#ff4d4d"); circle(c, x, y, 9, "#ffffff", stroke=3)

def r_sky(c, W, H, t, S):
    u = S.u; lat = S.opts.get("lat", 0)
    hz = (0.7 if not S.P else 0.53) * H
    if lat == 0:
        landscape_sky(c, W, H, t, "#3d8fe0", "#cfe9ff")
        sun(c, W * 0.2, hz - 0.42 * (hz), 50 * u, t, a=0.9)
        # edge-on ring: a thin line straight up from the horizon
        x = W * 0.58; gp = ease(prog(t, 0.2, 1.4))
        top_ = lerp(hz, -50, gp)
        p = skia.Path(); p.moveTo(x - 2 * u, hz); p.lineTo(x - 16 * u, top_); p.lineTo(x + 16 * u, top_); p.lineTo(x + 2 * u, hz); p.close()
        c.drawPath(p, paint(shader=lin(0, hz, 0, 0, [(0, "#ffffff", 0.5), (1, "#ffffff", 0.95)])))
        line(c, x, hz, x, top_, "#ffffff", 30 * u, 0.15, blur=10)
        mountains(c, W, hz, H, "#5b7aa0", 3, 0.25 * hz)
        mountains(c, W, hz + 0.04 * H, H, "#2f6b4a", 5, 0.12 * hz, n=9)
        rect(c, 0, hz + 0.04 * H, W, H, "#2b5e3e")
        for i, fx in enumerate((0.06, 0.16, 0.8, 0.93)):
            palm(c, fx * W, hz + 0.1 * H, (260 if not S.P else 200) * u * (0.8 + 0.2 * (i % 2)), a=1)
        chip(c, "EDGE-ON: A LINE STRAIGHT OVERHEAD", W / 2, 0.9 * H if not S.P else 0.56 * H, vis(t, S.lt(1, 0.35) if S.n() > 1 else S.lt(0, 0.5)), 30 * u, bg=PAL["chip"], dot=ROCK)
    elif lat == 38:
        landscape_sky(c, W, H, t, "#4a90d9", "#f7d9b5")
        sun(c, W * 0.14, hz - 0.45 * hz, 46 * u, t, a=0.9)
        gp = ease(prog(t, 0.1, 1.5))
        rx = W * (0.62 if not S.P else 0.62); ry = (hz - (0.08 if not S.P else 0.3) * H) * gp
        arch(c, W / 2, hz + 20 * u, rx, ry, (70 if not S.P else 56) * u, "#f2ebe0", 0.92)
        skyline(c, W, hz + 0.05 * H, H, 8, "#25324e", maxh=0.18 if not S.P else 0.08)
        rect(c, 0, hz + 0.05 * H, W, H, "#1c2740")
        for i in range(2):
            x = ((0.3 + i * 0.3 + t * 0.03) % 1.2 - 0.1) * W
            cloud(c, x, (0.2 if not S.P else 0.33) * H + i * 40 * u, 70 * u, "#ffffff", 0.75)
        if S.n() > 1:
            chip(c, "NEVER MOVES · NEVER SETS", W / 2, ytop(S) if S.P else 0.3 * H, vis(t, S.lt(1, 0.05)), 32 * u, bg=PAL["chip"])
            if not S.P:
                ps = vis(t, S.lt(1, 0.45))
                arrow(c, W / 2, hz - 30 * u, W / 2, hz + 60 * u, ORANGE, 8 * u, ps)
                text(c, "SOUTH", W / 2, hz + 100 * u, 40 * u, ORANGE, ps, w=900, shadow=8)
    else:
        landscape_sky(c, W, H, t, "#34507e", "#c9d8ea")
        gp = ease(prog(t, 0.1, 1.2))
        arch(c, W / 2, hz + 10 * u, W * 0.32, 0.08 * H * gp, 46 * u, "#fff4e0", 1.0, glow=0.8)
        mountains(c, W, hz + 0.01 * H, H, "#c9d6e6", 11, 0.07 * H)
        rect(c, 0, hz + 0.01 * H, W, H, "#eef4fb")
        for i, fx in enumerate((0.05, 0.12, 0.2, 0.78, 0.86, 0.95)):
            conifer(c, fx * W, hz + 0.12 * H, (220 if not S.P else 170) * u * (0.8 + 0.25 * (i % 2)), snow=1)
        pp = vis(t, S.lt(0, 0.6))
        chip(c, "AT THE POLES: NO RINGS AT ALL", W / 2, ytop(S), pp, 32 * u, bg=PAL["chip"])
    inset_globe(c, W, H, t, S, lat)
    lab = PLACES[lat][0]
    gy = 0.2 * H if not S.P else 0.335 * H
    chip(c, lab, W * (0.89 if not S.P else 0.84), gy + 120 * u, prog(t, 0.2, 0.4), 22 * u, bg="#0b1030")
    kit.hook(c, W, H, t, S)

def r_night(c, W, H, t, S):
    u = S.u; B = beats(S, 3)
    hz = (0.72 if not S.P else 0.53) * H
    fill_bg(c, W, H, "#050418", "#1a1640")
    sa = 1 - 0.6 * ease(prog(t, B(2, 0.2), 1.5))
    stars(c, W, H, t, sa, seed=41)
    rx = W * 0.62; ry = hz - (0.1 if not S.P else 0.3) * H
    gp = vis(t, B(1, 0.55)) if S.n() >= 3 else vis(t, 0.3)
    arch(c, W / 2, hz + 20 * u, rx, ry, (70 if not S.P else 56) * u, "#ffe7c2", 0.95, glow=1.0, gap=(250, 275) if gp > 0 else None)
    skyline(c, W, hz + 0.04 * H, H, 12, "#0c1024", win=1.0, maxh=0.2 if not S.P else 0.08)
    rect(c, 0, hz + 0.04 * H, W, H, "#0a0d1e")
    if S.n() >= 3:
        chip(c, "RINGSHINE", W / 2, ytop(S) if S.P else 0.3 * H, vis(t, B(0, 0.4), B(1, 0)), 36 * u, bg=PAL["chip"], dot="#ffe7c2")
        pb = vis(t, B(1, 0.15), B(2, 0))
        bx, by = (W * 0.5, 0.5 * H) if not S.P else (W * 0.5, 0.42 * H)
        if pb > 0:
            circle(c, bx, by - 30 * u, 70 * u, "#fff2c0", pb * 0.3, blur=30 * u)
            circle(c, bx, by - 30 * u, 50 * u, "#fff2c0", pb)
            rrect(c, bx - 22 * u, by + 15 * u, 44 * u, 40 * u, 6 * u, "#b8b8c8", pb)
            text(c, "≈130 W PER M² OF RING", bx, by + 100 * u, 38 * u, "#ffffff", pb, w=900, shadow=8)
        pc = vis(t, B(2, 0.1))
        chip(c, "STARGAZING: MUCH HARDER", W / 2, ytop(S) if S.P else 0.93 * H, pc, 32 * u, bg=PAL["chip"])
        # label Earth's shadow gap
        ang = math.radians(262); gx = W / 2 + math.cos(ang) * rx; gy = hz + 20 * u + math.sin(ang) * ry
        pl = vis(t, B(2, 0.45))
        arrow(c, gx + 160 * u, gy + 130 * u, gx + 20 * u, gy + 40 * u, "#ffffff", 5 * u, pl)
        text(c, "EARTH'S SHADOW", gx + 180 * u, gy + 160 * u, 30 * u, "#ffffff", pl, w=900, shadow=8)
    else:
        chip(c, "RINGSHINE", W / 2, ytop(S), vis(t, 0.3), 36 * u, bg=PAL["chip"], dot="#ffe7c2")
    kit.hook(c, W, H, t, S)

# ------------------------------------------------------------------ seasons
def shadow_diag(c, W, H, t, S, tilt, pb):
    """side view: Sun left, tilted ringed Earth; the sunward ring segment shades a band of the globe."""
    u = S.u; cx, cy, sc = lay(S)
    ex = cx + (130 if not S.P else 120) * u; R = int((150 if not S.P else 125) * u)
    sx = W * (0.1 if not S.P else 0.08)
    sun(c, sx, cy, 70 * u * (1 if not S.P else 0.8), t)
    for i in range(9):
        y = cy - R * 1.3 + i * R * 2.6 / 8
        line(c, sx + 80 * u, y, ex - R * 0.95, y, "#ffd166", 4 * u, 0.55)
    ang = math.radians(tilt)
    rin, rout = 1.2 * R, 2.05 * R
    ya, yb = cy + math.sin(ang) * rin, cy + math.sin(ang) * rout
    y0, y1 = min(ya, yb), max(ya, yb)
    if y1 - y0 < 8 * u: ym = (y0 + y1) / 2; y0, y1 = ym - 4 * u, ym + 4 * u
    c.save(); c.translate(ex, cy); c.rotate(-tilt)
    ring(c, 0, 0, rin, rout, 0.12, "back", ROCK, 1.0, n=3)
    geo.globe(c, 0, 0, R, rot=-20, tilt=0, light=(-0.7, 0.0, 0.7), glow=0.5)
    line(c, 0, -R * 1.25, 0, R * 1.25, "#ffffff", 3 * u, 0.6, dash=([10 * u, 8 * u], 0))
    text(c, "N", 0, -R * 1.38, 34 * u, "#ffffff", 1, w=900)
    c.restore()
    c.save(); p = skia.Path(); p.addCircle(ex, cy, R); c.clipPath(p, doAntiAlias=True)
    c.clipRect(skia.Rect.MakeLTRB(ex - R, y0, ex + R * 0.15, y1))
    c.drawPaint(paint("#05030f", 0.6 * pb))
    c.restore()
    for i in range(9):
        y = cy - R * 1.3 + i * R * 2.6 / 8
        if y0 < y < y1: line(c, ex - rout * math.cos(ang) * 0.98, y, ex - R * 0.95, y, "#2a1a4a", 6 * u, 0.95 * pb)
    c.save(); c.translate(ex, cy); c.rotate(-tilt)
    ring(c, 0, 0, rin, rout, 0.12, "front", ROCK, 1.0, n=3)
    c.restore()

def r_shadow(c, W, H, t, S):
    u = S.u; B = beats(S, 3); cx, cy, sc = lay(S); bg(c, W, H, t, S)
    long_ = S.n() >= 3
    q = ease(prog(t, B(1, 0.5), 1.5)) if long_ else 0.0
    shadow_diag(c, W, H, t, S, lerp(23.4, -23.4, q), vis(t, B(0, 0.5)))
    north = q < 0.5
    chip(c, "NORTHERN SUMMER" if north else "SOUTHERN SUMMER", cx, ytop(S), vis(t, B(0, 0.3)), 34 * u, bg=PAL["chip"], dot="#ffd166")
    lab = "RING SHADOW → SOUTHERN WINTER" if north else "RING SHADOW → NORTHERN WINTER"
    chip(c, lab, cx, ybot(S), vis(t, B(0, 0.6) if not long_ else B(2, 0.0)), 30 * u, bg=ORANGE, fg="#0b1030", a=1)
    kit.hook(c, W, H, t, S)

def r_equinox(c, W, H, t, S):
    u = S.u; B = beats(S, 3); cx, cy, sc = lay(S)
    pA = phase(t, None, B(1, 0))
    with Layer(c, pA) as on:
        if on:
            bg(c, W, H, t, S)
            ex = cx + 200 * u; R = 100
            sun(c, W * 0.12, cy, 60 * u, t)
            line(c, W * 0.12, cy, ex + 300 * u, cy, ORANGE, 4 * u, 0.8, dash=([16 * u, 12 * u], -t * 30))
            ring(c, ex, cy, R * 1.2, R * 2.3, 0.06, "back", ROCK); geo.globe(c, ex, cy, R, rot=t * 8, tilt=3); ring(c, ex, cy, R * 1.2, R * 2.3, 0.06, "front", ROCK)
            chip(c, "EQUINOX: SUN IN THE RING PLANE", cx, ytop(S), vis(t, 0.3), 32 * u, bg=PAL["chip"], dot="#ffd166")
    pB = phase(t, B(1, 0), B(2, 0))
    with Layer(c, pB) as on:
        if on:
            hz = (0.7 if not S.P else 0.53) * H
            fill_bg(c, W, H, "#2a1a4a", "#ff9e6b")
            x = W / 2
            line(c, x, hz, x, -20, "#fff3dc", 12 * u, 0.85)
            rise = ease(prog(t, B(1, 0), 3.0))
            sy = hz - 40 * u - rise * 60 * u
            sun(c, x, sy, 80 * u, t, glow=0.9)
            rect(c, x - 7 * u, sy - 90 * u, 14 * u, 180 * u, "#3a2238", 0.85)
            mountains(c, W, hz, H, "#3a2238", 21, 0.08 * H, n=6)
            rect(c, 0, hz, W, H, "#2a1a30")
            chip(c, "THE RINGS SLICE THE SUN", W / 2, ytop(S), vis(t, B(1, 0.3)), 34 * u, bg=PAL["chip"], dot="#ffd166")
    pC = phase(t, B(2, 0))
    with Layer(c, pC) as on:
        if on:
            bg(c, W, H, t, S)
            q = ease(prog(t, B(2, 0.45), max(1.0, S.dur - B(2, 0.45) - 0.4)))
            shadow_diag(c, W, H, t, S, lerp(0.0, -23.4, q), 1.0)
            chip(c, "EQUINOX: A THIN STRIPE ON THE EQUATOR", W / 2, ytop(S), vis(t, B(2, 0.05), B(2, 0.45)), 30 * u, bg=PAL["chip"], dot="#ffd166")
            chip(c, "THEN IT WIDENS OVER THE OTHER HEMISPHERE", W / 2, ytop(S), vis(t, B(2, 0.5)), 30 * u, bg=ORANGE, fg="#0b1030", a=1)

def r_tropics(c, W, H, t, S):
    u = S.u; B = beats(S, 2); cx, cy, sc = lay(S); bg(c, W, H, t, S)
    bb = (-180, -60, 180, 78)
    rr = geo.map_rect(bb, cx, cy + 10 * u, width=W * (0.86 if not S.P else 0.96))
    geo.draw_map(c, bb, rr, land="#3dbb6c", sea="#1f6fd1", outline_w=1.5, res="110m")
    ice = ease(prog(t, B(1, 0.3), 3.0))
    X, Y, Wd, Hd = rr
    if ice > 0:
        _, yn = geo.lonlat_xy(0, lerp(70, 45, ice), bb, rr); _, ys = geo.lonlat_xy(0, lerp(-55, -40, ice), bb, rr)
        rect(c, X, Y, Wd, yn - Y, "#eef5fb", 0.85 * clamp(ice * 2))
        rect(c, X, ys, Wd, Y + Hd - ys, "#eef5fb", 0.85 * clamp(ice * 2))
    _, y0 = geo.lonlat_xy(0, 30, bb, rr); _, y1 = geo.lonlat_xy(0, -30, bb, rr)
    pb = vis(t, B(0, 0.25))
    rect(c, X, y0, Wd, y1 - y0, "#05030f", 0.5 * pb)
    line(c, X, (y0 + y1) / 2, X + Wd, (y0 + y1) / 2, ORANGE, 3 * u, pb, dash=([12 * u, 8 * u], 0))
    rrect(c, X, Y, Wd, Hd, 10 * u, "#ffffff", 0.6, stroke=3 * u)
    # sunlight arrows bouncing off the shaded band
    for i in range(6):
        x = X + Wd * (0.1 + 0.16 * i); q = (t * 0.6 + i / 6) % 1
        arrow(c, x - 50 * u, y0 - 150 * u, x - 6 * u, y0 - 8 * u, "#ffd166", 6 * u, pb * 0.95)
        arrow(c, x + 6 * u, y0 - 8 * u, x + 50 * u, y0 - 150 * u, "#ffe9a8", 6 * u, pb * (0.4 + 0.6 * math.sin(q * math.pi)))
    chip(c, "SANDIA MODEL: TROPICS IN SHADE", cx, ytop(S), vis(t, B(0, 0.1), B(1, 0)), 32 * u, bg=PAL["chip"], dot="#ffd166")
    chip(c, "ENOUGH FOR AN ICE AGE?", cx, ytop(S), vis(t, B(1, 0.2)), 34 * u, bg=ORANGE, fg="#0b1030", a=1)

def r_orbits(c, W, H, t, S):
    u = S.u; B = beats(S, 4); cx, cy, sc = lay(S); bg(c, W, H, t, S)
    k = 0.36; R = int((80 if not S.P else 70) * u) // 4 * 4
    cx = cx - (120 * u if not S.P else 0)
    def orbit(rk, rot=0, a=1.0, col_="#ffffff", half=None):
        c.save(); c.translate(cx, cy); c.rotate(rot)
        if half == "back": c.clipRect(skia.Rect.MakeLTRB(-1e4, -1e4, 1e4, 0))
        elif half == "front": c.clipRect(skia.Rect.MakeLTRB(-1e4, 0, 1e4, 1e4))
        c.drawOval(skia.Rect.MakeLTRB(-R * rk, -R * rk * k, R * rk, R * rk * k), paint(col_, a, stroke=3 * u))
        c.restore()
    def pos(rk, ang, rot=0):
        x, y = math.cos(ang) * R * rk, math.sin(ang) * R * rk * k
        rr_ = math.radians(rot); return cx + x * math.cos(rr_) - y * math.sin(rr_), cy + x * math.sin(rr_) + y * math.cos(rr_)
    pi_ = vis(t, B(0, 0.1)); pg = vis(t, B(1, 0.05)); pgeo = vis(t, B(1, 0.5))
    for half in ("back", "front"):
        orbit(6.6, 0, 0.5 * pgeo, "#9fd3ff", half); orbit(4.17, -18, 0.5 * pg, "#c9f29b", half)
        ring(c, cx, cy, R * 1.16, R * 2.9, k, half, ROCK, 0.9)
        if half == "back":
            geo.globe(c, cx, cy, R, rot=t * 10, tilt=21)
        orbit(1.07, 14, 0.8 * pi_, "#ffffff", half)
    # satellites
    def sat(x, y, a, col_):
        rect(c, x - 6 * u, y - 6 * u, 12 * u, 12 * u, col_, a); rect(c, x - 22 * u, y - 3 * u, 12 * u, 6 * u, "#6fb6ff", a); rect(c, x + 10 * u, y - 3 * u, 12 * u, 6 * u, "#6fb6ff", a)
    x, y = pos(1.07, t * 1.2 + 1.0, 14); sat(x, y, pi_, "#ffffff")
    x, y = pos(4.17, t * 0.3, -18); sat(x, y, pg, "#c9f29b")
    x, y = pos(6.6, t * 0.15 + 0.6, 0); sat(x, y, pgeo, "#9fd3ff")
    fs = 0.85 if S.P else 1.0
    lx = cx + R * 6.6 * 0.72 if not S.P else cx
    labs = [("ISS ~400 KM: BELOW", pi_, B(0, 0.1), None), ("RINGS ~1,000–12,000 KM", vis(t, B(0, 0.3)), None, None),
            ("GPS ~20,200 KM", pg, None, None), ("GEO ~36,000 KM", pgeo, None, None)]
    if not S.P:
        for i, (s_, p_, _, _) in enumerate(labs):
            chip(c, s_, W * 0.84, 0.2 * H + i * 78 * u, p_ * (1 - vis(t, B(2, 0)) * 0.6), 28 * u, bg="#0b1030", dot=["#ffffff", ROCK, "#c9f29b", "#9fd3ff"][i])
    else:
        chip(c, ["ISS ~400 KM: BELOW THE RINGS", "GPS ~20,200 KM · GEO ~36,000 KM", "", ""][0], W / 2, ytop(S), vis(t, B(0, 0.1), B(1, 0)), 28 * u, bg="#0b1030")
        chip(c, "GPS ~20,200 KM · GEO ~36,000 KM: ABOVE", W / 2, ytop(S), vis(t, B(1, 0.1), B(2, 0)), 26 * u, bg="#0b1030")
    # shooting gallery
    pd = vis(t, B(2, 0.0), B(3, 0))
    if pd > 0:
        x, y = pos(2.0, t * 0.6 + 2.5, 0)
        sat(x, y, pd, ORANGE)
        rng = random.Random(int(t * 6))
        for i in range(5):
            circle(c, x + rng.uniform(-30, 30) * u, y + rng.uniform(-20, 20) * u, rng.uniform(3, 9) * u, "#fff2c8", pd * rng.random())
        for j in range(3):
            q = (t * 0.8 + j / 3) % 1
            c.drawCircle(x, y, 20 * u + q * 140 * u, paint("#7fd0ff", pd * (1 - q) * 0.8, stroke=3 * u, dash=([10 * u, 14 * u], 0)))
        chip(c, "EQUATORIAL ORBITS: A SHOOTING GALLERY", W / 2, ytop(S), pd, 30 * u, bg=ORANGE, fg="#0b1030", a=1)
    pr = vis(t, B(3, 0.0))
    if pr > 0:
        q = ease(prog(t, B(3, 0.05), 3.0))
        sx_, sy_, _ = geo.globe_xy(-80, 55, cx, cy, R, t * 10, 21)
        ex_, ey_ = cx + R * 5.5, cy - R * 3.4
        p = skia.Path(); p.moveTo(sx_, sy_); p.quadTo(cx + R * 0.5, cy - R * 5.0, ex_, ey_)
        meas = skia.PathMeasure(p, False); L = meas.getLength()
        seg = skia.Path(); meas.getSegment(0, L * q, seg, True)
        c.drawPath(seg, paint(ORANGE, pr, stroke=5 * u, dash=([16 * u, 10 * u], 0)))
        pt, tan = meas.getPosTan(L * max(q, 0.01))
        circle(c, pt.x(), pt.y(), 10 * u, "#ffffff", pr)
        chip(c, "LAUNCH FAR NORTH, CLIMB OVER THE RINGS", W / 2, ytop(S), pr, 30 * u, bg=PAL["chip"], dot=ORANGE)

# ------------------------------------------------------------------ 1,000 years
def r_navigate(c, W, H, t, S):
    u = S.u; B = beats(S, 4)
    hz = (0.66 if not S.P else 0.5) * H
    pA = phase(t, None, B(1, 0))
    with Layer(c, pA) as on:
        if on:
            fill_bg(c, W, H, "#2a3f7a", "#f5c6a0")
            arch(c, W / 2, hz + 20 * u, W * 0.62, hz - (0.12 if not S.P else 0.3) * H, (60 if not S.P else 50) * u, "#f2ebe0", 0.9)
            c.drawRect(skia.Rect.MakeLTRB(0, hz, W, H), paint(shader=lin(0, hz, 0, H, [(0, "#1d4f8a", 1), (1, "#0b2240", 1)])))
            for i in range(14):
                yy = hz + 20 * u + i * 26 * u; xx = ((i * 0.37 + t * 0.03) % 1) * W
                line(c, xx, yy, xx + 120 * u, yy, "#ffffff", 3 * u, 0.25)
            bx = W * 0.4 + math.sin(t * 0.3) * 30 * u; by = hz + 50 * u + math.sin(t * 1.4) * 5 * u
            c.drawPath(poly([(bx - 120 * u, by - 20 * u), (bx + 130 * u, by - 20 * u), (bx + 90 * u, by + 30 * u), (bx - 90 * u, by + 30 * u)]), paint("#3b2618"))
            rect(c, bx - 4 * u, by - 230 * u, 8 * u, 210 * u, "#3b2618")
            c.drawPath(poly([(bx + 6 * u, by - 225 * u), (bx + 110 * u, by - 40 * u), (bx + 6 * u, by - 40 * u)]), paint("#efe4cc"))
            c.drawPath(poly([(bx - 6 * u, by - 200 * u), (bx - 90 * u, by - 45 * u), (bx - 6 * u, by - 45 * u)]), paint("#e2d6bb"))
            chip(c, "A PERMANENT LANDMARK", W / 2, ytop(S), vis(t, B(0, 0.4)), 34 * u, bg=PAL["chip"], dot=ROCK)
    pB = phase(t, B(1, 0), B(2, 0))
    with Layer(c, pB) as on:
        if on:
            bg(c, W, H, t, S)
            cols = [(10, 70), (30, 36), (50, 10)]
            n = 3; pw = W * (0.28 if not S.P else 0.3); gap = W * (0.03 if not S.P else 0.02)
            x0 = W / 2 - (n * pw + (n - 1) * gap) / 2
            ph_ = (0.5 if not S.P else 0.22) * H; py = cy_ = (0.28 if not S.P else 0.32) * H
            for i, (la, el) in enumerate(cols):
                pi_ = vis(t, B(1, 0.1 + 0.2 * i))
                x = x0 + i * (pw + gap)
                with Layer(c, pi_) as o2:
                    if not o2: continue
                    rrect(c, x, py, pw, ph_, 16 * u, "#120a26")
                    c.save(); c.clipRect(skia.Rect.MakeXYWH(x, py, pw, ph_))
                    base = py + ph_ * 0.85
                    hgt = (ph_ * 0.75) * math.sin(math.radians(el))
                    arch(c, x + pw / 2, base, pw * 0.55, max(hgt, 6 * u), 22 * u, "#f2ebe0", 0.9)
                    rect(c, x, base, pw, ph_, "#1d4f8a")
                    c.restore()
                    text(c, f"{la}° N", x + pw / 2, py + ph_ + 40 * u, 40 * u, "#ffffff", 1, w=900)
                    text(c, f"ARCH ~{el}° HIGH", x + pw / 2, py + ph_ + 88 * u, 32 * u, ORANGE, 1, w=900)
            chip(c, "ARCH HEIGHT → YOUR LATITUDE", W / 2, ytop(S) if not S.P else 0.27 * H, vis(t, B(1, 0.05)), 32 * u, bg=ORANGE, fg="#0b1030", a=1)
    pC = phase(t, B(2, 0), B(3, 0))
    with Layer(c, pC) as on:
        if on:
            bg(c, W, H, t, S)
            cx, cy, sc = lay(S)
            items = ["CALENDARS", "MYTHS", "SUNDIALS"]
            for i, lab in enumerate(items):
                pi_ = vis(t, B(2, 0.1 + 0.25 * i))
                x = W * (0.2 + 0.3 * i); y = cy - 20 * u
                if pi_ <= 0: continue
                s_ = 90 * u * (0.9 if S.P else 1.0)
                if i == 0:
                    rrect(c, x - s_, y - s_, 2 * s_, 2 * s_, 14 * u, "#f2ebe0", pi_)
                    rect(c, x - s_, y - s_, 2 * s_, s_ * 0.45, ORANGE, pi_)
                    for r_ in range(3):
                        for q_ in range(4): circle(c, x - s_ * 0.6 + q_ * s_ * 0.4, y - s_ * 0.1 + r_ * s_ * 0.38, s_ * 0.08, "#5d5248", pi_)
                elif i == 1:
                    ringed_earth(c, x, y, int(s_ * 0.55), t, a=pi_)
                    for j in range(5): circle(c, x + math.cos(j * 1.3 + t) * s_ * 1.1, y + math.sin(j * 1.3 + t) * s_ * 0.6, 4 * u, "#fff2c8", pi_)
                else:
                    oval(c, x, y + s_ * 0.5, s_, s_ * 0.35, "#c9b48a", pi_)
                    c.drawPath(poly([(x, y + s_ * 0.5), (x, y - s_ * 0.6), (x + s_ * 0.4, y + s_ * 0.5)]), paint("#6b5a44", pi_))
                    c.drawPath(poly([(x, y + s_ * 0.5), (x - s_ * 0.9, y + s_ * 0.62), (x - s_ * 0.9, y + s_ * 0.42)]), paint("#2a2030", pi_ * 0.7))
                text(c, lab, x, y + s_ * 1.4, 38 * u * (0.85 if S.P else 1), "#ffffff", pi_, w=900, shadow=6)
    pD = phase(t, B(3, 0))
    with Layer(c, pD) as on:
        if on:
            hz2 = (0.74 if not S.P else 0.53) * H
            fill_bg(c, W, H, "#050418", "#1a1640")
            stars(c, W, H, t, 0.8, seed=43)
            q = prog(t, B(3, 0.1), max(1.0, S.dur - B(3, 0.1) - 0.3))
            mid = lerp(200, 340, q)
            rx = W * 0.62; ry = hz2 - (0.1 if not S.P else 0.3) * H
            arch(c, W / 2, hz2 + 20 * u, rx, ry, (66 if not S.P else 54) * u, "#ffe7c2", 0.95, glow=1.0, gap=(mid - 12, mid + 12))
            ang = math.radians(mid); gx = W / 2 + math.cos(ang) * rx; gy = hz2 + 20 * u + math.sin(ang) * ry
            line(c, W / 2, hz2, gx, gy, "#ffffff", 4 * u, 0.35, dash=([12 * u, 10 * u], 0))
            circle(c, W / 2, hz2, 10 * u, "#ffffff", 0.6)
            c.drawRect(skia.Rect.MakeLTRB(0, hz2, W, H), paint(shader=lin(0, hz2, 0, H, [(0, "#0b1a33", 1), (1, "#050a16", 1)])))
            for i in range(10):
                yy = hz2 + 20 * u + i * 24 * u; xx = ((i * 0.41 + t * 0.02) % 1) * W
                line(c, xx, yy, xx + 100 * u, yy, "#ffe7c2", 2 * u, 0.15)
            chip(c, "DUSK → DAWN", W / 2, (0.9 if not S.P else 0.565) * H, vis(t, B(3, 0.15)), 34 * u, bg=PAL["chip"], dot="#ffe7c2")
            text(c, "EARTH'S SHADOW = CLOCK HAND", W / 2, (0.3 if not S.P else 0.27) * H, 34 * u, "#ffffff", vis(t, B(3, 0.4)), w=900, shadow=8)

def r_astro(c, W, H, t, S):
    u = S.u; B = beats(S, 2)
    hz = (0.78 if not S.P else 0.55) * H
    fill_bg(c, W, H, "#03020e", "#141030")
    stars(c, W, H, t, 1.0, seed=52, density=1.4)
    rx = W * 0.62; ry = hz - (0.12 if not S.P else 0.3) * H
    # blocked stripe
    c.save(); c.clipRect(skia.Rect.MakeLTRB(-1e4, -1e4, 1e4, hz))
    r_ = skia.Rect.MakeLTRB(W / 2 - rx, hz + 20 * u - ry, W / 2 + rx, hz + 20 * u + ry)
    c.drawOval(r_, paint("#03020e", 1, stroke=150 * u))
    c.restore()
    gl = 0.6 + 0.4 * vis(t, B(1, 0.1))
    arch(c, W / 2, hz + 20 * u, rx, ry, 100 * u, "#ffe7c2", 0.8, glow=gl)
    # hill + observatory
    hills(c, W, hz, 30 * u, "#0a0816", 4, H=H)
    ox = W * 0.72; oy = hz - 30 * u
    rect(c, ox - 70 * u, oy - 60 * u, 140 * u, 70 * u, "#cfd3dd")
    p = skia.Path(); p.addArc(skia.Rect.MakeLTRB(ox - 75 * u, oy - 135 * u, ox + 75 * u, oy + 15 * u), 180, 180); p.close()
    c.drawPath(p, paint("#e6e9f0"))
    rect(c, ox - 12 * u, oy - 132 * u, 24 * u, 70 * u, "#0a0816")
    pg = vis(t, B(1, 0.2))
    circle(c, ox - 140 * u, oy - 260 * u, 150 * u, "#ffe7c2", 0.35 * pg, blur=50 * u)
    line(c, ox, oy - 100 * u, ox - 140 * u, oy - 260 * u, "#ffffff", 3 * u, 0.5 * pg, dash=([10 * u, 8 * u], 0))
    chip(c, "A STRIPE OF SKY, HIDDEN FOR GOOD", W / 2, ytop(S), vis(t, B(0, 0.3), B(1, 0)), 32 * u, bg=PAL["chip"])
    chip(c, "TELESCOPES VS RINGSHINE", W / 2, ytop(S), vis(t, B(1, 0.1)), 34 * u, bg=ORANGE, fg="#0b1030", a=1)

# ------------------------------------------------------------------ fading
def r_fade(c, W, H, t, S):
    u = S.u; B = beats(S, 2); cx, cy, sc = lay(S); bg(c, W, H, t, S)
    R = int(150 * u * sc) // 4 * 4; k = 0.32
    ex = cx - (120 if not S.P else 0) * u
    fadeA = 1 - 0.5 * ease(prog(t, 0.5, S.dur))
    c.save(); c.translate(ex, cy); c.rotate(-8)
    ring(c, 0, 0, R * 1.25, R * 2.4, k, "back", ROCK, fadeA * 0.7)
    chunks_(c, 0, 0, R * 1.25, R * 2.4, k, t, n=80, half="back", size=3 * u)
    geo.globe(c, 0, 0, R, rot=t * 8, tilt=18)
    # meteors on the near side, at the equator
    for i in range(5):
        q = (t * 0.5 + i / 5) % 1
        x = lerp(-R * 0.8, R * 0.8, (i + 0.5) / 5) + q * 20 * u
        y = R * 0.32 + lerp(-R * 0.6, 0, q) * 0
        meteor(c, x + 20 * u, R * 0.25 - (1 - q) * 70 * u, math.radians(60), 60 * u, a=math.sin(q * math.pi) * vis(t, B(0, 0.5)), w=3 * u)
    ring(c, 0, 0, R * 1.25, R * 2.4, k, "front", ROCK, fadeA * 0.7)
    chunks_(c, 0, 0, R * 1.25, R * 2.4, k, t, n=80, half="front", size=3 * u)
    # collisions
    rng = random.Random(int(t * 3))
    for i in range(3):
        an = rng.random() * 6.28; rr_ = R * rng.uniform(1.3, 2.3)
        circle(c, math.cos(an) * rr_, math.sin(an) * rr_ * k, 10 * u, "#fff2c8", 0.8 * (1 - (t * 3 % 1)), blur=4)
    c.restore()
    chip(c, "COLLISIONS GRIND ROCK TO DUST", W / 2, ytop(S), vis(t, B(0, 0.1), B(0, 0.6)), 30 * u, bg=PAL["chip"])
    chip(c, "SHOOTING STARS ALONG THE EQUATOR", W / 2, ytop(S), vis(t, B(0, 0.6), B(1, 0)), 30 * u, bg=PAL["chip"], dot=ORANGE)
    pm = vis(t, B(1, 0.0))
    if pm > 0:
        mx = W * (0.85 if not S.P else 0.8); my = cy - (180 if not S.P else 230) * u
        moon(c, mx, my, 55 * u, lit=1.0, a=pm)
        for j in range(3):
            wob = math.sin(t * 3 + j) * 10 * u
            arrow(c, ex + R * (1.6 + 0.3 * j) * 0.9, cy - R * 0.3 * j * 0.5 + wob, mx - 70 * u, my + 30 * u * j, "#ff8a8a", 5 * u, pm * 0.8)
        chip(c, "THE MOON TUGS THE RINGS APART", W / 2, ytop(S), pm, 32 * u, bg=ORANGE, fg="#0b1030", a=1)

# ------------------------------------------------------------------ twist: Ordovician ring
def old_globe(c, x, y, R, t, a=1.0, band=0.0, outside=0.0, craters=0.0, nshow=21):
    circle(c, x, y, R * 1.06, "#6fb6ff", 0.25 * a, blur=R * 0.06)
    c.save(); p = skia.Path(); p.addCircle(x, y, R); c.clipPath(p, doAntiAlias=True)
    circle(c, x, y, R, "#1f5fb0", a)
    rot = t * 6
    rng = random.Random(14)
    for i in range(12):  # stylised ancient landmasses (not modern continents)
        lon = rng.uniform(-180, 180); lat = rng.uniform(-75, 20) if i < 8 else rng.uniform(-20, 40)
        X, Y, Z = (math.cos(math.radians(lat)) * math.sin(math.radians(lon + rot)), math.sin(math.radians(lat)),
                   math.cos(math.radians(lat)) * math.cos(math.radians(lon + rot)))
        if Z > -0.1:
            oval(c, x + X * R, y - Y * R, R * rng.uniform(0.15, 0.35) * max(Z, 0.2), R * rng.uniform(0.12, 0.25), "#9a8a5a", a)
    for la in (-60, -30, 0, 30, 60):
        yy = y - R * math.sin(math.radians(la))
        line(c, x - R, yy, x + R, yy, "#ffffff", 2, a * 0.25 if la else a * 0.5)
    if band > 0:
        y0 = y - R * 0.5; y1 = y + R * 0.5
        rect(c, x - R, y0, 2 * R, y1 - y0, ORANGE, 0.22 * band * a)
        line(c, x - R, y0, x + R, y0, ORANGE, 4, band * a); line(c, x - R, y1, x + R, y1, ORANGE, 4, band * a)
    if outside > 0:
        for yy0, yy1 in ((y - R, y - R * 0.5), (y + R * 0.5, y + R)):
            c.save(); c.clipRect(skia.Rect.MakeLTRB(x - R, yy0, x + R, yy1))
            for j in range(-12, 12):
                line(c, x + j * R * 0.12, yy0, x + j * R * 0.12 + R * 0.5, yy1, "#ffffff", 2, 0.3 * outside * a)
            c.restore()
    if craters > 0:
        rng = random.Random(21)
        for i in range(nshow):
            lon = rng.uniform(-80, 80); lat = rng.uniform(-27, 27)
            pi_ = clamp(craters * nshow - i)
            if pi_ <= 0: continue
            X = math.cos(math.radians(lat)) * math.sin(math.radians(lon)); Y = math.sin(math.radians(lat))
            cx_, cy_ = x + X * R, y - Y * R
            sc_ = eback(pi_)
            circle(c, cx_, cy_, 14 * sc_, "#ff4d4d", a * 0.9); circle(c, cx_, cy_, 14 * sc_, "#ffffff", a, stroke=3)
    c.drawCircle(x, y, R, paint(shader=rad(x - R * 0.35, y - R * 0.35, R * 1.8, [(0, "#ffffff", 0.15), (0.6, "#000000", 0), (1, "#000000", 0.55)]), a=a))
    c.restore()

def r_ordovician(c, W, H, t, S):
    u = S.u; B = beats(S, 4); cx, cy, sc = lay(S); bg(c, W, H, t, S)
    long_ = S.n() >= 4
    R = 290 * u * sc if not S.P else 230 * u
    gx = cx - (260 if not S.P else 0) * u
    crat = prog(t, B(1, 0.3), max(0.5, B(2, 0) - B(1, 0.3))) if long_ else prog(t, S.lt(0, 0.3), S.lt(0, 0.8) - S.lt(0, 0.3))
    band = vis(t, B(2, 0.1)) if long_ else vis(t, S.lt(0, 0.6))
    outside = vis(t, B(3, 0.1)) if long_ else 0
    old_globe(c, gx, cy, R, t, band=band, outside=outside, craters=crat)
    if long_:
        tx = W * 0.75; y0 = cy - 150 * u
        chip(c, "466 MILLION YEARS AGO", tx if not S.P else W / 2, y0 if not S.P else ytop(S), vis(t, B(0, 0.1), B(1, 0.2) if S.P else None), 32 * u, bg=PAL["chip"], dot=ORANGE)
        if not S.P:
            chip(c, "21 IMPACT CRATERS", tx, y0 + 90 * u, vis(t, B(1, 0.3)), 32 * u, bg="#0b1030", dot="#ff4d4d")
            chip(c, "ALL WITHIN 30° OF THE EQUATOR", tx, y0 + 180 * u, vis(t, B(2, 0.1)), 30 * u, bg=ORANGE, fg="#0b1030", a=1)
            chip(c, "~70% OF LAND WAS OUTSIDE", tx, y0 + 270 * u, vis(t, B(3, 0.1)), 30 * u, bg="#0b1030")
            ps = vis(t, B(3, 0.55))
            text(c, "1 IN 25 MILLION", tx, y0 + 380 * u, 64 * u, ORANGE, ps, w=900, shadow=10)
            text(c, "CHANCE BY LUCK", tx, y0 + 440 * u, 28 * u, "#ffffff", ps, w=700, fam="Inter")
        else:
            chip(c, "21 IMPACT CRATERS", W / 2, ytop(S), vis(t, B(1, 0.3), B(2, 0)), 30 * u, bg="#0b1030", dot="#ff4d4d")
            chip(c, "ALL WITHIN 30° OF THE EQUATOR", W / 2, ytop(S), vis(t, B(2, 0.1), B(3, 0)), 28 * u, bg=ORANGE, fg="#0b1030", a=1)
            chip(c, "ODDS BY LUCK: ~1 IN 25 MILLION", W / 2, ytop(S), vis(t, B(3, 0.3)), 28 * u, bg=ORANGE, fg="#0b1030", a=1)
    else:
        chip(c, "21 CRATERS · ALL NEAR THE EQUATOR", W / 2, ybot(S), vis(t, S.lt(0, 0.55)), 28 * u, bg="#0b1030", dot="#ff4d4d")
    kit.hook(c, W, H, t, S)

def r_breakup(c, W, H, t, S):
    u = S.u; B = beats(S, 2); cx, cy, sc = lay(S); bg(c, W, H, t, S)
    R = int(140 * u * sc) // 4 * 4; LIM = R * 2.9; k = 0.34
    c.drawOval(skia.Rect.MakeLTRB(cx - LIM, cy - LIM * k, cx + LIM, cy + LIM * k), paint(ORANGE, 0.6, stroke=3 * u, dash=([16 * u, 12 * u], -t * 20)))
    tb = B(0, 0.45)
    pieces = []
    if t < tb:
        q = prog(t, 0, tb)
        ax = lerp(W * 1.05, cx + LIM * 0.95, ease(q)); ay = lerp(cy - LIM * 0.9, cy + LIM * k * 0.2, ease(q))
        asteroid(c, ax, ay, 34 * u, t, trail=0.8, ang=-150, glow=0.3)
    else:
        q = ease(prog(t, tb, 3.0)); rng = random.Random(3)
        for i in range(150):
            ang = lerp(0.1, rng.uniform(0, 6.28), q) + t * 0.2
            rr = LIM * 0.95 * lerp(1, rng.uniform(0.42, 1.0), q)
            pieces.append((ang, rr, rng.uniform(2, 5) * u))
    for half in ("back", "front"):
        for ang, rr, s_ in pieces:
            if (math.sin(ang) > 0) != (half == "front"): continue
            circle(c, cx + math.cos(ang) * rr, cy + math.sin(ang) * rr * k, s_, mix(ROCK, "#ffffff", 0.2))
        if half == "back":
            old_globe(c, cx, cy, R, t, band=0.0)
    pf = vis(t, B(1, 0.0))
    if pf > 0:
        for i in range(7):
            q = (t * 0.7 + i / 7) % 1
            ang = 0.3 + i * 0.4
            sx_, sy_ = cx + math.cos(ang) * LIM * 0.6, cy + math.sin(ang) * LIM * 0.6 * k
            tx, ty = cx + math.cos(ang) * R * 0.9 * 0.7, cy + R * 0.34 * 0.7
            x = lerp(sx_, tx, q); y = lerp(sy_, ty, q)
            meteor(c, x, y, math.atan2(ty - sy_, tx - sx_), 50 * u, a=pf * math.sin(q * math.pi), w=4 * u)
            if q > 0.92: circle(c, tx, ty, 16 * u, "#fff2c8", pf * 0.9)
    chip(c, "AN ASTEROID, TORN APART", W / 2, ytop(S), vis(t, B(0, 0.4), B(1, 0)), 32 * u, bg=PAL["chip"], dot=ORANGE)
    chip(c, "CHUNKS RAIN DOWN NEAR THE EQUATOR", W / 2, ytop(S), pf, 30 * u, bg=ORANGE, fg="#0b1030", a=1)

def r_iceage(c, W, H, t, S):
    u = S.u; B = beats(S, 2); cx, cy, sc = lay(S); bg(c, W, H, t, S)
    q = ease(prog(t, 0.3, max(1.0, B(1, 0) - 0.3)))
    R = int(170 * u * sc) // 4 * 4
    ringed_earth(c, cx, cy, R, t, cap=lerp(72, 40, q), shadow=1.0, spin=6)
    thermometer(c, W * (0.85 if not S.P else 0.86), cy, 260 * u * (1 if not S.P else 0.7), lerp(15, -10, q), tmax=25, tmin=-25, label=False)
    chip(c, "HIRNANTIAN ICE AGE", W / 2, ytop(S), vis(t, B(0, 0.25), B(1, 0)), 34 * u, bg=PAL["chip"], dot="#bfe3ff")
    chip(c, "RING SHADOW: AN IDEA, NOT A PROOF", W / 2, ytop(S), vis(t, B(1, 0.1)), 32 * u, bg=ORANGE, fg="#0b1030", a=1)

def r_moon(c, W, H, t, S):
    u = S.u; B = beats(S, 2); cx, cy, sc = lay(S); bg(c, W, H, t, S)
    R = 120 * u * sc; k = 0.35
    timp = B(0, 0.45)
    if t < timp:
        q = prog(t, 0, timp)
        tx = lerp(cx + R * 4.5, cx + R * 1.2, ease(q)); ty = lerp(cy - R * 1.8, cy - R * 0.6, ease(q))
        planet(c, tx, ty, R * 0.55, "#c46a3a")
    pdisk = prog(t, timp, 0.6)
    form = ease(prog(t, B(0, 0.75), max(0.5, B(1, 0) - B(0, 0.75))))
    rng = random.Random(8)
    pts = []
    for i in range(170):
        ang = rng.random() * 6.28 + t * 0.4 * (1.5 if i % 2 else 1)
        rr = R * lerp(1.0, rng.uniform(1.3, 2.6), ease(pdisk))
        mx_, my_ = cx + R * 3.0, cy
        px, py = cx + math.cos(ang) * rr, cy + math.sin(ang) * rr * k
        pts.append((lerp(px, mx_, form * (0.7 + 0.3 * rng.random())), lerp(py, my_, form), rng.uniform(2, 5) * u, math.sin(ang)))
    for back in (True, False):
        for px, py, s_, sn in pts:
            if pdisk <= 0 or (sn < 0) != back: continue
            circle(c, px, py, s_, mix("#ff9a4a", ROCK, form), pdisk * (1 - form * 0.8))
        if back:
            bl = ease(prog(t, B(1, 0), 2.0))
            planet(c, cx, cy, R, mix("#b8402a", "#3a6fb8", bl), bands=["#7a2a1a", "#d06a3a"] if bl < 0.5 else None)
    if pdisk > 0 and t < timp + 0.7:
        circle(c, cx + R * 0.8, cy - R * 0.4, R * (0.3 + 1.2 * pdisk), "#fff2c8", 0.9 * (1 - pdisk), blur=20 * u)
    if form > 0:
        drift = ease(prog(t, B(1, 0.3), 3.0)) * 120 * u
        moon(c, cx + R * 3.0 + drift, cy, R * 0.32 * form, lit=1.0, a=form)
        pa = vis(t, B(1, 0.3))
        arrow(c, cx + R * 3.0 + drift + R * 0.45, cy, cx + R * 3.0 + drift + R * 1.2, cy, ORANGE, 6 * u, pa)
    chip(c, "~4.5 BILLION YEARS AGO", W / 2, ytop(S), vis(t, B(0, 0.1), B(1, 0)), 32 * u, bg=PAL["chip"], dot="#ff9a4a")
    chip(c, "STILL DRIFTING AWAY: 3.8 CM A YEAR", W / 2, ytop(S), vis(t, B(1, 0.3)), 30 * u, bg=ORANGE, fg="#0b1030", a=1)

def r_others(c, W, H, t, S):
    u = S.u; B = beats(S, 2); cx, cy, sc = lay(S); bg(c, W, H, t, S)
    pA = phase(t, None, B(1, 0))
    with Layer(c, pA) as on:
        if on:
            P = S.P
            items = [("JUPITER", "#d9a46a", 0.12, 1.4, 1.6, 0.25), ("SATURN", "#e8cf9a", 0.95, 1.3, 2.3, 0.3),
                     ("URANUS", "#9fe3e8", 0.5, 1.5, 2.0, 0.3), ("NEPTUNE", "#4f7fe0", 0.3, 1.6, 2.1, 0.25)]
            n = len(items)
            for i, (nm, colr, ra, r0, r1, k) in enumerate(items):
                pi_ = vis(t, B(0, 0.05 + 0.08 * i))
                if P: x = W * (0.27 + 0.46 * (i % 2)); y = 0.33 * H + (i // 2) * 0.13 * H; R = 46 * u
                else: x = W * (0.14 + 0.24 * i); y = cy - 60 * u; R = 72 * u
                rotd = 80 if nm == "URANUS" else -8
                c.save(); c.translate(x, y); c.rotate(rotd)
                ring(c, 0, 0, R * r0, R * r1, k, "back", "#efe6d6", ra * pi_, n=3)
                c.restore()
                planet(c, x, y, R, colr, pi_, bands=["#b07a4a", "#f0d6a8"] if nm == "JUPITER" else None)
                c.save(); c.translate(x, y); c.rotate(rotd)
                ring(c, 0, 0, R * r0, R * r1, k, "front", "#efe6d6", ra * pi_, n=3)
                c.restore()
                text(c, nm, x, y + R * (1.7 if not P else 1.65), 30 * u * (0.9 if P else 1), "#ffffff", pi_, w=900, shadow=6)
            ps = vis(t, B(0, 0.55))
            if ps > 0:
                for j, (nm, x, y) in enumerate((("HAUMEA", W * 0.36, (0.8 if not S.P else 0.545) * H), ("CHARIKLO", W * 0.64, (0.8 if not S.P else 0.545) * H))):
                    pj = vis(t, B(0, 0.55 + 0.1 * j))
                    ring(c, x, y, 30 * u, 48 * u, 0.3, "back", "#efe6d6", pj, n=2)
                    oval(c, x, y, 24 * u if j == 0 else 14 * u, 14 * u, "#c9c2b8" if j == 0 else "#7a6a5a", pj)
                    ring(c, x, y, 30 * u, 48 * u, 0.3, "front", "#efe6d6", pj, n=2)
                    text(c, nm, x + 70 * u, y, 28 * u, "#ffffff", pj, w=800, align="l")
            chip(c, "ALL FOUR GIANT PLANETS HAVE RINGS", W / 2, ytop(S), vis(t, B(0, 0.1)), 32 * u, bg=PAL["chip"], dot="#efe6d6")
    pB = phase(t, B(1, 0))
    with Layer(c, pB) as on:
        if on:
            bg(c, W, H, t, S)
            R = 130 * u * sc
            planet(c, cx, cy, R, "#c1440e", bands=["#9a3a10", "#d96a3a"])
            q = ease(prog(t, B(1, 0.1), max(1, S.dur - B(1, 0.1) - 0.5)))
            rr = lerp(R * 2.2, R * 1.25, q); ang = t * 1.6
            px, py = cx + math.cos(ang) * rr, cy + math.sin(ang) * rr * 0.35
            c.drawOval(skia.Rect.MakeLTRB(cx - rr, cy - rr * 0.35, cx + rr, cy + rr * 0.35), paint("#ffffff", 0.3, stroke=2 * u, dash=([8 * u, 8 * u], 0)))
            if q > 0.85:
                chunks_(c, cx, cy, R * 1.15, R * 1.5, 0.35, t, n=int(140 * (q - 0.85) / 0.15), seed=5, colr="#9a8a7a", size=3 * u)
            else:
                st = 1 + q * 0.6
                c.save(); c.translate(px, py); c.scale(st, 1 / st ** 0.5)
                oval(c, 0, 0, 16 * u, 11 * u, "#8f8478"); c.restore()
            text(c, "MARS", cx, cy + R + 50 * u, 36 * u, "#ffffff", 1, w=900, shadow=6)
            chip(c, "PHOBOS: ~2 M CLOSER EVERY CENTURY", W / 2, ytop(S), vis(t, B(1, 0.2)), 30 * u, bg=PAL["chip"], dot="#8f8478")
            chip(c, "TORN APART IN 30–50 MILLION YEARS", W / 2, ybot(S), vis(t, B(1, 0.6)), 30 * u, bg=ORANGE, fg="#0b1030", a=1)

SCENES = {"r_title": r_title, "r_card": r_card, "r_end": r_end, "r_endshort": r_endshort, "r_saturn": r_saturn, "r_roche": r_roche,
          "r_material": r_material, "r_sky": r_sky, "r_night": r_night, "r_shadow": r_shadow, "r_equinox": r_equinox,
          "r_tropics": r_tropics, "r_orbits": r_orbits, "r_navigate": r_navigate, "r_astro": r_astro, "r_fade": r_fade,
          "r_ordovician": r_ordovician, "r_breakup": r_breakup, "r_iceage": r_iceage, "r_moon": r_moon, "r_others": r_others}
