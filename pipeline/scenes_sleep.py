"""Scenes for 'What If You Never Slept Again?' (vertical Short)."""
import math, random, colorsys
import skia
from core import *
from scenes import vis, until_next

SKIN, HAIR, SHIRT = "#e8b98f", "#2b2118", "#4d6cfa"

def face(c, x, y, r, t, eyes="wide", yawn=0.0, bags=0.0, blink=True, look=(0, 0)):
    circle(c, x, y, r, SKIN)
    p = skia.Path(); p.addArc(skia.Rect.MakeLTRB(x - r * 1.02, y - r * 1.05, x + r * 1.02, y + r * 0.95), 190, 160); p.close()
    c.drawPath(p, paint(HAIR))
    ex = r * 0.38; ey = y - r * 0.02
    bl = 1.0
    if blink and eyes == "wide":
        q = (t % 3.1)
        bl = 0.1 if 1.5 < q < 1.62 else 1.0
    for sx in (-1, 1):
        cx = x + sx * ex
        if bags > 0:
            p = skia.Path(); p.addArc(skia.Rect.MakeXYWH(cx - r * 0.24, ey - r * 0.02, r * 0.48, r * 0.36), 20, 140)
            c.drawPath(p, paint("#7b4f8c", bags, stroke=r * 0.06))
        if eyes == "closed":
            p = skia.Path(); p.addArc(skia.Rect.MakeXYWH(cx - r * 0.18, ey - r * 0.12, r * 0.36, r * 0.24), 20, 140)
            c.drawPath(p, paint("#3a2a20", 1, stroke=r * 0.06)); continue
        er = r * (0.22 if eyes == "wide" else 0.18)
        oval(c, cx, ey, er, er * bl, "#ffffff")
        if bl > 0.5:
            circle(c, cx + look[0] * er * 0.4, ey + look[1] * er * 0.4, er * (0.42 if eyes == "wide" else 0.5), "#1d1a2a")
        if eyes == "tired":
            c.drawPath(_lid(cx, ey, er), paint(SKIN))
            line(c, cx - er, ey - er * 0.1, cx + er, ey - er * 0.1, "#3a2a20", r * 0.04)
    my = y + r * 0.48
    if yawn > 0.05:
        oval(c, x, my, r * 0.16, r * 0.24 * yawn, "#5a1e2a")
    elif eyes == "closed":
        p = skia.Path(); p.addArc(skia.Rect.MakeXYWH(x - r * 0.18, my - r * 0.14, r * 0.36, r * 0.2), 20, 140)
        c.drawPath(p, paint("#3a2a20", 1, stroke=r * 0.05))
    else:
        line(c, x - r * 0.14, my, x + r * 0.14, my, "#3a2a20", r * 0.05)

def _lid(cx, ey, er):
    p = skia.Path(); p.addArc(skia.Rect.MakeLTRB(cx - er * 1.05, ey - er * 1.05, cx + er * 1.05, ey + er * 1.05), 180, 180)
    p.lineTo(cx - er * 1.05, ey - er * 0.1); p.close(); return p

def bedroom(c, W, H, t, S, eyes, clock_txt, night=1.0):
    u = S.u
    fill_bg(c, W, H, "#0e1030", "#1d1f45")
    wx, wy, ww, wh = 0.1 * W, 0.16 * H, 0.36 * W, 0.18 * H
    rect(c, wx, wy, ww, wh, "#060a20")
    c.save(); c.clipRect(skia.Rect.MakeXYWH(wx, wy, ww, wh)); stars(c, W, H, t, 1, seed=41)
    moon(c, wx + ww * 0.7, wy + wh * 0.35, 40 * u); c.restore()
    rect(c, wx, wy, ww, wh, "#3a2d55", stroke=14 * u); line(c, wx + ww / 2, wy, wx + ww / 2, wy + wh, "#3a2d55", 10 * u)
    rect(c, 0, 0.6 * H, W, 0.4 * H, "#15132e")
    # nightstand + clock
    nx, ny = 0.72 * W, 0.4 * H
    rect(c, nx, ny, 0.22 * W, 0.2 * H, "#4a3326")
    rrect(c, nx + 0.02 * W, ny - 90 * u, 0.18 * W, 90 * u, 14 * u, "#111")
    text(c, clock_txt, nx + 0.11 * W, ny - 45 * u, 52 * u, "#ff3b3b", 0.95, w=800, fam="Inter")
    circle(c, nx + 0.11 * W, ny - 45 * u, 90 * u, "#ff3b3b", 0.08, blur=30 * u)
    # bed
    bx, by, bw = 0.06 * W, 0.42 * H, 0.62 * W
    rrect(c, bx - 20 * u, by - 60 * u, 40 * u, 0.22 * H, 12 * u, "#6b4630")
    rrect(c, bx, by + 0.08 * H, bw, 0.1 * H, 20 * u, "#6b4630")
    rrect(c, bx + 10 * u, by, bw * 0.4, 0.07 * H, 30 * u, "#e8ecf7")
    hx, hy, hr = bx + bw * 0.2, by + 0.01 * H, 95 * u
    face(c, hx, hy, hr, t, eyes=eyes, bags=0.8 if eyes != "closed" else 0, look=(0.3, -0.6) if eyes == "wide" else (0, 0))
    rrect(c, bx + 0.02 * W, by + 0.055 * H, bw * 0.98, 0.12 * H, 36 * u, "#4d6cfa")
    rrect(c, bx + 0.02 * W, by + 0.055 * H, bw * 0.98, 26 * u, 13 * u, "#7b93ff")

def bed_awake(c, W, H, t, S):
    u = S.u
    bedroom(c, W, H, t, S, "wide", "3:00 AM")
    if S.opts.get("hook"):
        sz = fit(S.opts["hook"], W * 0.9, 90 * u, 900)
        text(c, S.opts["hook"], W / 2, 0.08 * H, sz, "#ffffff", eout(t / 0.25), w=900, stroke=10 * u, stroke_col="#0b1030")

def bed_asleep(c, W, H, t, S):
    u = S.u
    bedroom(c, W, H, t, S, "closed", "10:30 PM")
    for i in range(3):
        q = (t * 0.35 + i / 3) % 1
        text(c, "Z", 0.3 * W + q * 160 * u + i * 20 * u, 0.36 * H - q * 260 * u, (50 + 30 * i) * u, "#cfd8ff", math.sin(q * math.pi), w=900)
    chip(c, "YOUR BRAIN WILL THANK YOU", W / 2, 0.08 * H, vis(t, S.lt(0, 0.6)), 38 * u, bg="#1b2250")

def desk(c, W, H, t, S, blur=6.0, nod=1.0, eyes="tired"):
    u = S.u
    fill_bg(c, W, H, "#141633", "#232650")
    rect(c, 0, 0.53 * H, W, 0.47 * H, "#3b2a22")
    # monitor
    mx, my, mw, mh = 0.06 * W, 0.24 * H, 0.46 * W, 0.17 * H
    rrect(c, mx - 12 * u, my - 12 * u, mw + 24 * u, mh + 24 * u, 18 * u, "#1a1a22")
    rect(c, mx, my, mw, mh, "#dfe9ff")
    rng = random.Random(3)
    for k in range(9):
        lw = mw * rng.uniform(0.4, 0.9)
        line(c, mx + 30 * u, my + 28 * u + k * mh / 10, mx + 30 * u + lw, my + 28 * u + k * mh / 10, "#4a5a80", 9 * u, 0.85, blur=blur * u)
    rect(c, mx + mw / 2 - 20 * u, my + mh + 12 * u, 40 * u, 0.53 * H - my - mh - 12 * u, "#1a1a22")
    # person
    px = 0.73 * W; nodp = nod * max(0, math.sin(t * 1.4)) ** 6
    rrect(c, px - 150 * u, 0.4 * H, 300 * u, 0.2 * H, 90 * u, SHIRT)
    c.save(); c.translate(px, 0.34 * H); c.rotate(-12 * nodp); c.translate(0, 18 * u * nodp)
    yawn = max(0, math.sin(t * 0.9 - 1)) ** 4
    face(c, 0, 0, 120 * u, t, eyes=eyes, yawn=yawn, bags=1)
    c.restore()
    # desk + mug
    rect(c, 0, 0.53 * H, W, 30 * u, "#7a5236")
    rrect(c, 0.55 * W, 0.49 * H, 70 * u, 80 * u, 14 * u, "#f2f2f2")
    circle(c, 0.55 * W + 80 * u, 0.49 * H + 40 * u, 22 * u, "#f2f2f2", stroke=10 * u)
    for i in range(3):
        q = (t * 0.4 + i / 3) % 1
        circle(c, 0.55 * W + 35 * u + math.sin(q * 6 + i) * 10 * u, 0.49 * H - q * 120 * u, (12 + q * 14) * u, "#ffffff", 0.3 * (1 - q), blur=6 * u)

def desk_tired(c, W, H, t, S):
    u = S.u
    desk(c, W, H, t, S, blur=lerp(2, 9, t / S.dur))
    chip(c, "≈ LEGALLY DRUNK", W / 2, 0.22 * H, vis(t, S.lt(0, 0.75)), 44 * u, dot="#ff4d4d")

def _blackouts(t, S, starts):
    for b in starts:
        if b <= t < b + 0.4: return True
    return False

def microsleep(c, W, H, t, S):
    u = S.u
    if S.n() > 1 and t >= S.ls(1) - 0.1:
        fill_bg(c, W, H, "#05070f", "#0d1020")
        hy = 0.34 * H
        c.drawPath(poly([(0, H), (W * 0.42, hy), (W * 0.58, hy), (W, H)]), paint("#1c1f2a"))
        for k in range(10):
            q = ((k / 10) + t * 0.9) % 1; z = q ** 2.2
            y0 = lerp(hy, H, z); y1 = lerp(hy, H, min(1, z + 0.03 + 0.05 * z))
            line(c, W / 2, y0, W / 2, y1, "#ffd166", lerp(2, 30, z) * u)
        c.drawPaint(paint(shader=rad(W / 2, hy, W * 0.6, [(0, "#ffe9a8", 0.25), (1, "#ffe9a8", 0)])))
        p = skia.Path(); p.addArc(skia.Rect.MakeXYWH(W * 0.05, 0.5 * H, W * 0.9, W * 0.9), 200, 140)
        c.drawPath(p, paint("#0b0b10", 1, stroke=60 * u))
        rect(c, 0, 0.58 * H, W, 0.42 * H, "#0b0b10")
        if _blackouts(t, S, [S.ls(1) + 0.3, S.ls(1) + 1.2]):
            c.drawPaint(paint("#000000", 1)); text(c, "MICROSLEEP", W / 2, 0.3 * H, 60 * u, "#ff4d4d", 0.9, w=900)
        return
    desk(c, W, H, t, S, blur=8, nod=0.4, eyes="tired")
    bl = [S.lt(0, f) for f in (0.3, 0.55, 0.78)]
    if _blackouts(t, S, bl):
        c.drawPaint(paint("#000000", 1)); text(c, "MICROSLEEP", W / 2, 0.3 * H, 60 * u, "#ffffff", 0.85, w=900)
    else:
        chip(c, "BLACKOUTS YOU DON'T NOTICE", W / 2, 0.22 * H, vis(t, S.lt(0, 0.6)), 36 * u)

def hallucinate(c, W, H, t, S):
    u = S.u
    fill_bg(c, W, H, "#170d2e", "#2a0f3a")
    k = lerp(0.2, 1.6, ease(t / S.dur))
    sp = 110 * u
    eyes_on = t > S.lt(0, 0.45)
    rng = random.Random(8)
    for j in range(-1, int(H / sp) + 2):
        for i in range(-1, int(W / sp) + 2):
            x0, y0 = i * sp + (j % 2) * sp / 2, j * sp
            x = x0 + math.sin(y0 * 0.006 + t * 2.1) * 30 * u * k
            y = y0 + math.cos(x0 * 0.006 + t * 1.6) * 30 * u * k
            hue = (x0 / W * 0.4 + t * 0.08 * k + y0 / H * 0.3) % 1
            r_, g_, b_ = colorsys.hsv_to_rgb(hue, 0.55, 0.85)
            rr = (22 + 10 * math.sin(t * 3 + i + j)) * u
            if eyes_on and rng.random() < 0.04:
                oval(c, x, y, rr * 1.3, rr * 0.8, "#ffffff", 0.9); circle(c, x + math.sin(t) * rr * 0.3, y, rr * 0.4, "#111")
            else:
                circle(c, x, y, rr, (int(r_ * 255), int(g_ * 255), int(b_ * 255)), 0.85)
    c.drawPaint(paint(shader=rad(W / 2, H / 2, H * 0.6, [(0.4, "#000000", 0), (1, "#000000", 0.75)])))
    circle(c, 0.3 * W, 0.62 * H, 210 * u, "#06040c"); rrect(c, 0.3 * W - 260 * u, 0.7 * H, 520 * u, 0.4 * H, 160 * u, "#06040c")
    for n, (lab, f) in enumerate([("HALLUCINATIONS", 0.25), ("PARANOIA", 0.48), ("TROUBLE SPEAKING", 0.72)]):
        chip(c, lab, W / 2, (0.25 + 0.075 * n) * H, vis(t, S.lt(0, f)), 40 * u)

def record_1964(c, W, H, t, S):
    u = S.u
    fill_bg(c, W, H, "#2a1f14", "#433222")
    fx, fy, fw, fh = 0.18 * W, 0.17 * H, 0.64 * W, 0.4 * H
    c.save(); c.translate(W / 2, fy + fh / 2); c.rotate(-3); c.translate(-W / 2, -(fy + fh / 2))
    rect(c, fx, fy, fw, fh, "#f3e9d2")
    ix, iy, iw, ih = fx + 40 * u, fy + 40 * u, fw - 80 * u, fh * 0.68
    rect(c, ix, iy, iw, ih, "#c9b48f")
    day = 1 + int(10 * clamp(t / max(S.le(0), 0.1)))
    rrect(c, ix + iw * 0.2, iy + ih * 0.12, iw * 0.6, ih * 0.76, 16 * u, "#fffaf0")
    rect(c, ix + iw * 0.2, iy + ih * 0.12, iw * 0.6, ih * 0.2, "#b33a2b")
    text(c, "DAY", ix + iw / 2, iy + ih * 0.22, 46 * u, "#fffaf0", 1, w=800)
    text(c, str(day), ix + iw / 2, iy + ih * 0.58, 190 * u, "#3a2a1a", 1, w=900)
    text(c, "1964", fx + fw / 2, fy + fh * 0.86, 90 * u, "#5a4630", 1, w=900, fam="Inter")
    c.restore()
    hrs = int(264 * clamp(t / max(S.le(0), 0.1)))
    text(c, f"{hrs} HOURS AWAKE", W / 2, 0.71 * H, 70 * u, ACCENT, 1, w=900, shadow=10)
    chip(c, "DON'T TRY THIS", W / 2, 0.78 * H, vis(t, S.lt(1, 0.2)), 40 * u, dot="#ff4d4d") if S.n() > 1 else None

def lab_rat(c, W, H, t, S):
    u = S.u
    fill_bg(c, W, H, "#dfe7ee", "#b9c6d3")
    rect(c, 0, 0.52 * H, W, 0.48 * H, "#8c9aa8")
    cx, cy, cw, ch = 0.12 * W, 0.26 * H, 0.76 * W, 0.28 * H
    rect(c, cx, cy + ch - 20 * u, cw, 40 * u, "#5b6672")
    rr = 1 - ease(prog(t, S.dur * 0.55, S.dur * 0.3))
    rx = W / 2 + math.sin(t * 1.2) * 120 * u * rr; ry = cy + ch - 70 * u
    p = skia.Path(); p.moveTo(rx - 110 * u, ry + 20 * u); p.cubicTo(rx - 220 * u, ry + 40 * u, rx - 230 * u, ry - 40 * u, rx - 300 * u, ry - 10 * u)
    c.drawPath(p, paint("#f2a7b0", 1, stroke=10 * u))
    oval(c, rx, ry, 130 * u, 65 * u, "#ece7df")
    circle(c, rx + 120 * u, ry - 20 * u, 55 * u, "#ece7df")
    circle(c, rx + 100 * u, ry - 70 * u, 26 * u, "#f2a7b0")
    circle(c, rx + 168 * u, ry - 14 * u, 9 * u, "#f2a7b0")
    if rr > 0.3: circle(c, rx + 135 * u, ry - 32 * u, 8 * u, "#c22")
    else: line(c, rx + 127 * u, ry - 32 * u, rx + 143 * u, ry - 32 * u, "#333", 4 * u)
    for k in range(13):
        x = cx + k * cw / 12; line(c, x, cy, x, cy + ch, "#6d7884", 6 * u)
    rect(c, cx, cy - 10 * u, cw, 20 * u, "#6d7884")
    chip(c, "1980s UNIVERSITY LAB STUDIES", W / 2, 0.18 * H, vis(t, 0.3), 36 * u, bg="#1b2250")
    fade = ease(prog(t, S.dur - 1.3, 1.1))
    if fade > 0: c.drawPaint(paint("#000000", fade))

SCENES = {"bed_awake": bed_awake, "bed_asleep": bed_asleep, "desk_tired": desk_tired, "microsleep": microsleep,
          "hallucinate": hallucinate, "record_1964": record_1964, "lab_rat": lab_rat}
