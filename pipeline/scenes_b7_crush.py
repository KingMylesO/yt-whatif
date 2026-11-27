"""Batch 07 Crush Files Shorts (1080x1920): #2 why you blush (cr7_hall), #3 why you get butterflies (cr7_park).

Same "3D world, 2D character" look as Crush Files #1 (scenes_cf01.py) but new sets, light and props:
  cr7_hall - kit3d.hallway() at golden hour: warm end window, light shafts, dust motes; slow dolly-in
             with a little sideways swing per beat. Props: alarm beacon, a widening blood vessel with
             cells, a cheek magnifier, a toggle switch that won't flip, an open book, rating frames.
  cr7_park - a new low-poly park at dusk (ground, path, bench, lamp post, trees, hills, purple-orange
             sky): the camera orbits slowly around Kai. Props: a brain from spheres, a pumping heart,
             a coiled gut from spheres, the vagus-nerve "hotline", butterflies.
Every camera is built around Kai's feet (kcam), so Kai keeps the same screen spot and size whatever
the yaw: head ~0.21H, feet ~0.57H (captions burn in at 0.635H, the CTA button sits at 0.75H).
Static cameras would cache the set with kit3d.CACHE; these cameras move every frame, so the sets are
kept small (about 70 meshes) and rendered per frame.
"""
import math
import numpy as np
import skia
from core import *
from scenes import vis
import kit3d as K
import mc
from scenes_cf01 import _butterfly, _shadow

NAVY = "#0b1030"
PINK = "#ff3d6e"
RED = "#e8344e"
OFF = np.array((0.45, 1.7, 4.1))           # camera offset from Kai's feet (same framing as Crush Files #1)
TGT = np.array((-0.05, 0.2, -0.6))


def _rot(v, yaw):
    a = math.radians(yaw); ca, sa = math.cos(a), math.sin(a)
    return np.array((v[0] * ca + v[2] * sa, v[1], -v[0] * sa + v[2] * ca))


def kcam(kp, yaw=0.0, push=1.0):
    """Camera that frames Kai standing at kp; yaw orbits around him, push > 1 pulls back."""
    kp = np.array(kp, float)
    o = _rot(OFF, yaw); o = np.array((o[0] * push, o[1] + (push - 1) * 0.6, o[2] * push))
    return K.Cam(kp + o, kp + _rot(TGT, yaw), fov=60)


def _p(kp, dx, dy, dz=0.0, yaw=0.0):
    """World point beside Kai: dx right / dz toward the camera as seen at this yaw."""
    v = _rot((dx, dy, dz), yaw)
    return (kp[0] + v[0], kp[1] + v[1], kp[2] + v[2])


def _heat(c, x, y, s, a):
    """Soft red flush over Kai's cheeks (drawn after Kai)."""
    if a <= 0:
        return
    for sx in (-1, 1):
        cx, cy = x + sx * 9.6 * s, y - 74.6 * s
        c.drawCircle(cx, cy, 9 * s, paint(shader=rad(cx, cy, 9 * s, [(0, "#ff2d55", 0.55 * a), (1, "#ff2d55", 0)])))


def _heatlines(c, x, y, s, t, a):
    for k in range(3):
        ph = (t * 0.9 + k / 3) % 1.0
        xx = x + (k - 1) * 12 * s; yy = y - (108 + 16 * ph) * s
        p = skia.Path(); p.moveTo(xx, yy)
        p.cubicTo(xx - 3 * s, yy - 3 * s, xx + 3 * s, yy - 6 * s, xx, yy - 9 * s)
        c.drawPath(p, paint("#ff6f91", a * math.sin(math.pi * ph), stroke=1.6 * s))


def _stomach(c, x, y, s, ang=0.0, colr="#ff8fb1", a=1.0, sign=None):
    """Small 2D stomach icon (an x-ray style badge on Kai's belly)."""
    if a <= 0:
        return
    c.save(); c.translate(x, y); c.rotate(ang); c.scale(s, s)
    p = skia.Path()
    p.moveTo(-3, -12); p.cubicTo(-3, -6, -1, -4, 2, -5); p.cubicTo(9, -8, 13, 0, 9, 7)
    p.cubicTo(5, 13, -6, 13, -9, 6); p.cubicTo(-11, 2, -8, -2, -7, -4); p.cubicTo(-6, -7, -6, -10, -7, -12); p.close()
    c.drawCircle(0, 0, 16, paint("#ffffff", 0.85 * a)); c.drawCircle(0, 0, 16, paint(NAVY, a, stroke=1.6))
    c.drawPath(p, paint(colr, a)); c.drawPath(p, paint(NAVY, a, stroke=1.4))
    if sign:
        text(c, sign, 11, -10, 12, NAVY, a, w=900)
    c.restore()


def _end_title(c, W, H, t, S, u):
    p = prog(t, 0.1, 0.4)
    sz = fit("THE CRUSH FILES", W * 0.86, 96 * u, 900)
    text(c, "THE CRUSH FILES", W / 2, 0.11 * H, sz, ACCENT, p, w=900, stroke=10 * u, stroke_col=NAVY)
    chip(c, "MORE ON THE CHANNEL", W / 2, 0.17 * H, vis(t, S.lt(0, 0.62)), 40 * u, bg="#ffffff", fg=NAVY, a=1)


def _series(c, W, H, t, S, u, mode):
    if mode != "end":
        chip(c, "THE CRUSH FILES", W / 2, 0.085 * H, 1.0, 30 * u, bg=NAVY, fg=ACCENT, a=0.9, dot=PINK)
    else:
        _end_title(c, W, H, t, S, u)
    o = S.opts
    if o.get("hook"):
        sz = fit(o["hook"], W * 0.9, 92 * u, 900)
        text(c, o["hook"], W / 2, 0.165 * H, sz, "#ffffff", eout(t / 0.25), w=900, stroke=10 * u, stroke_col=NAVY)


def _label(c, s, x, y, size, a=1.0, fg="#ffffff", bg=NAVY, W=1080):
    """Chip kept inside the frame (chip() pads to about width + 1.4 * size)."""
    half = (tw(s, size * 1.15, 700, "Inter") + 1.43 * size * 1.15) / 2 + 18 * W / 1080
    chip(c, s, clamp(x, half, W - half), y, a, size, bg=bg, fg=fg, a=1)


# ====================================================================== #2 BLUSH: hallway at golden hour
KP_H = (-0.3, 0.0, -1.0)
CRUSH_FAR = (1.25, 0.0, -7.6)
CRUSH_NEAR = (0.62, 0.0, -3.3)
_HALL = []
GOLD_LIGHT = K.Light((-0.3, 0.75, 0.6), 0.6, 0.5, tint="#ffe2b8")


def _hall_set():
    if not _HALL:
        M = K.hallway(lockers=("#3f6fd8", "#e8657f", "#2fb7a5"), wall="#f1d6b0", floor="#c49f86")
        # big end window with the low sun, plus a frame
        M.append(K.quad((-1.45, 0.55, -13.98), (1.45, 0.55, -13.98), (1.45, 2.65, -13.98), (-1.45, 2.65, -13.98),
                        "#ffb862", layer=1, glow="#ffd9a0"))
        M.append(K.sphere(0.35, 1.25, -13.97, 0.42, "#fff1c4", 5, 12, layer=1))
        for x0, y0, x1, y1 in ((-1.5, 0.5, 1.5, 0.58), (-1.5, 2.62, 1.5, 2.7), (-1.5, 0.5, -1.42, 2.7),
                               (1.42, 0.5, 1.5, 2.7), (-0.04, 0.55, 0.04, 2.65), (-1.45, 1.56, 1.45, 1.62)):
            M.append(K.box(x0, y0, -14.0, x1, y1, -13.95, "#fff4e0", layer=1, outline=0.6))
        # warm sun patches on the floor and a notice board
        for z0, w in ((-12.5, 1.6), (-9.6, 1.3), (-6.9, 1.0)):
            M.append(K.quad((-w / 2, 0.006, z0 + 0.7), (w / 2, 0.006, z0 + 0.7), (w / 2, 0.006, z0), (-w / 2, 0.006, z0),
                            "#ffd49a", layer=1))
        _HALL.extend(M)
    return _HALL


def _hall_bg(c, W, H, t, cam):
    fill_bg(c, W, H, "#ffcf98", "#f0b884")
    K.render(c, W, H, cam, _hall_set(), light=GOLD_LIGHT, fog=("#ffc98e", 3.0, 15.0, 0.55))
    win = K.anchor(cam, W, H, (0.0, 1.6, -13.9), 1.0)
    if win:                                                   # light shafts + dust from the window
        wx, wy, wh = win
        for k, (dx, ang, wd) in enumerate(((-0.35, -0.55, 0.16), (0.05, 0.05, 0.12), (0.4, 0.6, 0.15))):
            c.save(); c.translate(wx + dx * W * 0.2, wy); c.rotate(math.degrees(ang) * 0.25)
            pth = poly([(-wd * W * 0.1, 0), (wd * W * 0.1, 0), (wd * W * 1.6, H * 1.2), (-wd * W * 1.6, H * 1.2)])
            c.drawPath(pth, paint(shader=lin(0, 0, 0, H * 1.2, [(0, "#fff3d6", 0.0), (0.25, "#fff3d6", 0.13), (1, "#fff3d6", 0.0)])))
            c.restore()
        c.drawCircle(wx, wy, 0.5 * W, paint(shader=rad(wx, wy, 0.5 * W, [(0, "#fff0c8", 0.45), (1, "#fff0c8", 0)])))
    rnd = np.random.default_rng(11)
    for k in range(26):
        x0, y0, sp = rnd.random(), rnd.random(), 0.01 + 0.02 * rnd.random()
        x = (x0 + 0.02 * math.sin(t * 0.7 + k)) * W; y = ((y0 - t * sp) % 1.0) * H * 0.62
        circle(c, x, y, (2 + 2 * rnd.random()) * W / 1080, "#fff6dd", 0.35 + 0.3 * math.sin(t * 2 + k))


def _beacon(kp, yaw, on, spin):
    b = _p(kp, 0.95, 1.05, 0.15, yaw)
    M = [K.cylinder(b[0], b[1], b[2], 0.17, 0.09, "#2b2f45", top="#3a3f5c"),
         K.sphere(b[0], b[1] + 0.12, b[2], 0.15, mix("#a0283a", "#ff3b4e", on), 6, 12, bias=0.2)]
    return M, b


def _vessel(kp, yaw, r, t):
    """Horizontal blood vessel (tube along screen x) and the cells moving through it."""
    c0 = _p(kp, 0.86, 1.2, 0.1, yaw)
    tube = K.cylinder(0, -0.3, 0, r, 0.6, "#ff8f9e", n=16, r_top=r).tilted(90).turned(90 + yaw).moved(*c0)
    cells = []
    for k in range(6):
        ph = ((t * 0.35 + k / 6.0) % 1.0) - 0.5
        off = _rot((ph * 0.56, 0.35 * r * math.sin(k * 2.3), 0), yaw)
        cells.append(K.sphere(c0[0] + off[0], c0[1] + off[1], c0[2] + off[2], r * 0.42, "#c8102e", 4, 8))
    return tube, cells, c0


def _switch(kp, yaw, flip):
    b = _p(kp, 0.95, 1.0, 0.1, yaw)
    base = K.box(b[0] - 0.2, b[1] - 0.28, b[2] - 0.06, b[0] + 0.2, b[1] + 0.28, b[2] + 0.06, "#f4f1ea").turned(yaw, b)
    slot = K.box(b[0] - 0.06, b[1] - 0.16, b[2] + 0.06, b[0] + 0.06, b[1] + 0.16, b[2] + 0.075, "#2b2f45", bias=0.1).turned(yaw, b)
    lever = K.box(b[0] - 0.05, b[1], b[2] + 0.06, b[0] + 0.05, b[1] + 0.2, b[2] + 0.13, PINK, bias=0.2)
    lever = lever.tilted(-25 + 50 * flip, (b[0], b[1], b[2] + 0.07)).turned(yaw, b)
    return [base, slot, lever], b


def _book(kp, yaw, t):
    b = _p(kp, -0.95, 1.05, 0.1, yaw)
    bob = 0.03 * math.sin(t * 1.4)
    L = K.box(-0.34, -0.01, -0.22, 0.0, 0.01, 0.22, "#7b3fa0").tilted(70).turned(-28)
    R = K.box(0.0, -0.01, -0.22, 0.34, 0.01, 0.22, "#7b3fa0").tilted(70).turned(28)
    P1 = K.box(-0.31, 0.012, -0.2, 0.0, 0.03, 0.2, "#fffaf0").tilted(70).turned(-28)
    P2 = K.box(0.0, 0.012, -0.2, 0.31, 0.03, 0.2, "#fffaf0").tilted(70).turned(28)
    return [m.turned(yaw).moved(b[0], b[1] + bob, b[2]).biased(0.05 * i) for i, m in enumerate((L, R, P1, P2))], b


def _frame(cx, cy, cz, yaw, colr):
    f = K.box(cx - 0.27, cy - 0.33, cz - 0.03, cx + 0.27, cy + 0.33, cz + 0.03, colr).turned(yaw, (cx, cy, cz))
    inner = K.box(cx - 0.22, cy - 0.28, cz + 0.03, cx + 0.22, cy + 0.28, cz + 0.035, "#fff7ec", bias=0.1).turned(yaw, (cx, cy, cz))
    return [f, inner]


def _face_icon(c, x, y, r, blush, a=1.0):
    """Generic rating-photo face (round, simple), with or without a blush."""
    circle(c, x, y, r, "#f2b48a", a); circle(c, x, y, r, NAVY, a, stroke=r * 0.08)
    for sx in (-1, 1):
        circle(c, x + sx * r * 0.36, y - r * 0.12, r * 0.1, NAVY, a)
        if blush:
            oval(c, x + sx * r * 0.5, y + r * 0.2, r * 0.2, r * 0.12, "#ff4f7b", 0.8 * a)
    p = skia.Path(); p.moveTo(x - r * 0.28, y + r * 0.38); p.quadTo(x, y + r * (0.5 if blush else 0.4), x + r * 0.28, y + r * 0.38)
    c.drawPath(p, paint(NAVY, a, stroke=r * 0.08))


def _magnifier(c, x, y, R, cx, cy, grow, a, t):
    """Lens linked to Kai's cheek, showing a capillary network that widens with `grow`."""
    line(c, x, y, cx, cy, "#ffffff", 4, a * 0.9)
    circle(c, cx, cy, 6, "#ffffff", a)
    c.save(); c.clipPath(skia.Path().addCircle(x, y, R), doAntiAlias=True)
    circle(c, x, y, R, "#f4b48c", a)
    rnd = np.random.default_rng(5)
    for k in range(9):                                        # branching vessels
        y0 = y - R + (k + 0.5) * 2 * R / 9 + rnd.normal() * 6
        p = skia.Path(); p.moveTo(x - R, y0)
        for j in range(1, 7):
            p.lineTo(x - R + j * R / 3, y0 + 14 * math.sin(j * 1.3 + k) + rnd.normal() * 4)
        c.drawPath(p, paint(mix("#e4787e", "#d61f3c", grow), a, stroke=(2.5 + 5 * grow) * (1.3 if k % 3 == 0 else 0.8)))
    c.drawCircle(x, y, R, paint(shader=rad(x, y, R, [(0, "#ff2d55", 0.0), (1, "#ff2d55", 0.25 * grow * a)])))
    c.restore()
    circle(c, x, y, R, "#ffffff", a, stroke=10); circle(c, x, y, R + 5, NAVY, a, stroke=3)


def cr7_hall(c, W, H, t, S):
    o = S.opts; mode = o.get("mode", "hook"); u = S.u; p = clamp(t / max(S.dur, 0.1))
    yaw = {"hook": -6, "alarm": 7, "vessels": -9, "auto": 5, "darwin": -5, "study": 0, "end": 8}[mode]
    yaw += 5 * (p - 0.5) * (1 if yaw <= 0 else -1)                    # slow sideways swing
    cam = kcam(KP_H, yaw, push=1.06 - 0.05 * ease(p))                  # slow dolly-in
    _hall_bg(c, W, H, t, cam)
    kx, ky, kh = K.anchor(cam, W, H, KP_H, 1.75); s = kh / 100.0
    pose, expr, heat = "idle", "neutral", 0.0
    props, light = [], GOLD_LIGHT

    # ---------------------------------------------------------------- Crush down the hall
    if mode in ("hook", "end"):
        at = CRUSH_FAR if mode == "hook" else CRUSH_NEAR
        if mode == "end":
            at = (lerp(CRUSH_FAR[0], CRUSH_NEAR[0], eout(prog(t, 0, 1.6))), 0, lerp(-5.0, CRUSH_NEAR[2], eout(prog(t, 0, 1.6))))
        ca = K.anchor(cam, W, H, at, 1.75)
        al = vis(t, 0.2, d=0.5) if mode == "hook" else vis(t, 0.0, d=0.6)
        if ca and al > 0:
            _shadow(c, ca[0], ca[1], ca[2], al); mc.crush(c, ca[0], ca[1], ca[2], t, a=al, flip=True)

    if mode == "hook":
        hit = S.lt(0, 0.3)
        expr = "neutral" if t < hit else ("shocked" if t < hit + 0.8 else "blush")
        heat = ease(prog(t, hit + 0.5, 0.8))
    elif mode == "alarm":
        expr = "nervous"; on = 0.5 + 0.5 * math.sin(t * 9)
        props, b = _beacon(KP_H, yaw, on, t)
    elif mode == "vessels":
        expr = "blush"; pose = "cheeks"
        heat = ease(prog(t, S.lt(0, 0.6), 1.0))
        r = lerp(0.07, 0.14, ease(prog(t, 0.2, 1.6)))
        tube, cells, vc = _vessel(KP_H, yaw, r, t)
    elif mode == "auto":
        if t < S.ls(1) - 0.15:
            pose, expr = "shrug", "blush"; heat = 0.6
            fl = max(0.0, math.sin(min(t, S.le(0)) * 3.2)) ** 3 * 0.45       # tries to flip, springs back
            props, sb = _switch(KP_H, yaw, fl)
        else:
            pose, expr = "wave", "happy"
    elif mode == "darwin":
        pose, expr = "think", "curious"
        props, bb = _book(KP_H, yaw, t)
    elif mode == "study":
        pose, expr = "point", "curious"
        fL = _p(KP_H, -0.95, 1.25, 0.0, yaw); fR = _p(KP_H, 0.95, 1.25, 0.0, yaw)
        pin = vis(t, 0.3)
        if pin > 0:
            props = _frame(*fL, yaw, "#8a93b8") + _frame(*fR, yaw, PINK)
    elif mode == "end":
        pose, expr = "wave", "blush"; heat = 0.5

    if mode == "vessels":
        cl = K.render(c, W, H, cam, cells, light=light)
        K.render(c, W, H, cam, [tube], light=light, a=0.62)
        a1 = K.anchor(cam, W, H, vc, 0.2)
        if a1:
            _label(c, "VESSELS WIDEN", a1[0], a1[1] - 120 * u, 30 * u, vis(t, 0.5), W=W)
    elif props:
        K.render(c, W, H, cam, props, light=light)

    if mode == "alarm":                                        # rotating beacon rays + adrenaline drops
        a1 = K.anchor(cam, W, H, (b[0], b[1] + 0.12, b[2]), 0.15)
        if a1:
            bx, by, _ = a1
            for k in range(3):
                ang = t * 4 + k * 2.094
                pth = poly([(bx, by), (bx + math.cos(ang - 0.18) * 300 * u, by + math.sin(ang - 0.18) * 300 * u),
                            (bx + math.cos(ang + 0.18) * 300 * u, by + math.sin(ang + 0.18) * 300 * u)])
                c.drawPath(pth, paint(shader=rad(bx, by, 300 * u, [(0, "#ff3b4e", 0.45), (1, "#ff3b4e", 0)])))
            _label(c, "ADRENALINE", bx, by - 105 * u, 30 * u, vis(t, 0.6), fg=NAVY, bg=ACCENT, W=W)
            for k in range(6):
                ph = (t * 0.8 + k / 6) % 1.0
                dx = lerp(bx, kx + 6 * s, ph); dy = lerp(by, ky - 75 * s, ph) - math.sin(math.pi * ph) * 50 * u
                d = skia.Path(); r = 9 * u
                d.moveTo(dx, dy - 2 * r); d.cubicTo(dx + r, dy - r, dx + r, dy + r * 0.6, dx, dy + r * 0.6)
                d.cubicTo(dx - r, dy + r * 0.6, dx - r, dy - r, dx, dy - 2 * r); d.close()
                c.drawPath(d, paint(ACCENT, math.sin(math.pi * ph))); c.drawPath(d, paint(NAVY, math.sin(math.pi * ph), stroke=2 * u))

    _shadow(c, kx, ky, kh)
    mc.kai(c, kx, ky, kh, t, pose, expr, seed=1.1)
    _heat(c, kx, ky, s, heat)
    if heat > 0.3:
        _heatlines(c, kx, ky, s, t, heat)

    if mode == "vessels":                                      # cheek magnifier
        pm = vis(t, S.lt(0, 0.05))
        if pm > 0:
            _magnifier(c, kx - 40 * s, ky - 66 * s, 100 * u * lerp(0.7, 1, eback(pm)), kx - 8 * s, ky - 75 * s,
                       ease(prog(t, S.lt(0, 0.35), 1.2)), pm, t)
            _label(c, "TINY VESSELS", kx - 40 * s, ky - 66 * s + 130 * u, 28 * u, pm, W=W)
    elif mode == "auto" and t < S.ls(1) - 0.15:
        a1 = K.anchor(cam, W, H, sb, 0.3)
        if a1:
            _label(c, "OFF?  NOPE", a1[0], a1[1] - 140 * u, 30 * u, vis(t, S.lt(0, 0.35)), bg=PINK, W=W)
    elif mode == "darwin":
        pq = vis(t, 0.25)
        if pq > 0:                                             # quote card to the right of Kai's head
            x0, y0, w, h = kx + 19 * s, ky - 101 * s, W - (kx + 19 * s) - 22 * u, 360 * u
            c.save(); c.translate(x0 + w / 2, y0 + h / 2); sc = lerp(0.8, 1, eback(pq)); c.scale(sc, sc)
            rrect(c, -w / 2, -h / 2, w, h, 26 * u, "#fffaf0", pq); rrect(c, -w / 2, -h / 2, w, h, 26 * u, NAVY, pq, stroke=5 * u)
            lines_ = ["\u201cThe most", "peculiar and", "the most human", "of all", "expressions.\u201d"]
            fs = fit("the most human", w - 34 * u, 46 * u, 800)
            for i, ln in enumerate(lines_):
                text(c, ln, 0, -h / 2 + 58 * u + i * fs * 1.22, fs, NAVY, pq, w=800)
            text(c, "— Charles Darwin", 0, h / 2 - 22 * u, 28 * u, "#7b3fa0", pq, w=700)
            c.restore()
    elif mode == "study":
        for k, (pt, bl, lab) in enumerate(((fL, False, "NO BLUSH"), (fR, True, "BLUSH"))):
            a1 = K.anchor(cam, W, H, (pt[0], pt[1] - 0.33, pt[2]), 0.66)
            if not a1:
                continue
            fx, fy, fh = a1; pk = vis(t, 0.5 + 0.4 * k)
            if pk <= 0:
                continue
            _face_icon(c, fx, fy - fh * 0.52, fh * 0.28, bl, pk)
            _label(c, lab, fx, fy + 34 * u, 26 * u, pk, bg=PINK if bl else "#5b6488", W=W)
            pr = vis(t, S.lt(0, 0.7))                          # verdict: the blushing face rated kinder
            if pr > 0:
                n = 3 if bl else 2
                for j in range(3):
                    hp = mc.heart_path(fx + (j - 1) * 40 * u, fy - fh - 34 * u, 15 * u)
                    on = j < n
                    c.drawPath(hp, paint(PINK if on else "#ffffff", pr * (1 if on else 0.6)))
                    c.drawPath(hp, paint(NAVY, pr, stroke=3 * u))
        if vis(t, S.lt(0, 0.7)) > 0:
            _label(c, "ILLUSTRATION", kx, ky + 22 * u, 22 * u, vis(t, S.lt(0, 0.7)) * 0.9, fg="#ffffff", bg="#5b6488", W=W)
    _series(c, W, H, t, S, u, mode)


# ====================================================================== #3 BUTTERFLIES: park at dusk
KP_P = (0.0, 0.0, 0.0)
_PARK = []
DUSK_LIGHT = K.Light((0.6, 0.55, 0.5), 0.6, 0.5, tint="#ffdccb")


def _tree(x, z, h, leaf):
    return [K.cylinder(x, 0, z, 0.12, h * 0.45, "#6b4a3a", n=8),
            K.sphere(x, h * 0.62, z, h * 0.3, leaf, 5, 9, bias=0.3),
            K.sphere(x + h * 0.12, h * 0.85, z + 0.05, h * 0.2, mix(leaf, "#ffffff", 0.08), 4, 8, bias=0.5)]


def _park_set():
    if not _PARK:
        M = [K.quad((-24, 0, 9), (24, 0, 9), (24, 0, -34), (-24, 0, -34), "#5a9a6a", layer=0)]
        M.append(K.quad((-24, 0.006, -1.6), (24, 0.006, -1.6), (24, 0.006, -3.0), (-24, 0.006, -3.0), "#c9a98e", layer=1))
        M += [K.box(-24, 0.0, -1.65, 24, 0.05, -1.55, "#9f8a76", layer=1, outline=0.4)]
        # bench behind Kai, to the right
        bx, bz = 1.15, -2.15
        M += [K.box(bx - 0.75, 0.42, bz - 0.2, bx + 0.75, 0.48, bz + 0.2, "#b9754a", bias=0.2),
              K.box(bx - 0.75, 0.55, bz - 0.24, bx + 0.75, 0.85, bz - 0.18, "#b9754a", bias=0.15),
              K.box(bx - 0.7, 0, bz - 0.18, bx - 0.62, 0.42, bz + 0.18, "#2b2f45"),
              K.box(bx + 0.62, 0, bz - 0.18, bx + 0.7, 0.42, bz + 0.18, "#2b2f45")]
        # lamp post behind Kai, to the left
        M += [K.cylinder(-1.65, 0, -2.6, 0.06, 2.4, "#2b2f45", n=8),
              K.cylinder(-1.65, 2.4, -2.6, 0.16, 0.12, "#2b2f45", n=8, r_top=0.05)]
        lamp = K.sphere(-1.65, 2.32, -2.6, 0.14, "#ffe6a8", 4, 8, bias=0.2); lamp.glow = "#ffd27a"
        M.append(lamp)
        for x, z, h, leaf in ((-3.4, -5.0, 3.0, "#2f7a5e"), (3.6, -6.2, 3.4, "#3a8a63"), (-6.0, -9.5, 3.8, "#2c6b58"),
                              (6.5, -10.5, 4.0, "#346f5a"), (0.8, -13.0, 4.2, "#2f6656"), (-2.2, -15, 3.6, "#2b5e52"),
                              (-9.0, -6.0, 3.5, "#2f7a5e"), (9.5, -4.5, 3.2, "#3a8a63")):
            M += _tree(x, z, h, leaf)
        for x, z, r in ((-2.6, -3.4, 0.45), (2.6, -3.5, 0.5), (-0.4, -4.2, 0.35), (4.4, -2.9, 0.4)):
            M.append(K.sphere(x, r * 0.55, z, r, "#3d8061", 4, 8))
        rnd = np.random.default_rng(21)                       # grass patches + little flowers in the foreground
        for k in range(14):
            x, z, w = rnd.uniform(-4, 4), rnd.uniform(-1.2, 3.2), rnd.uniform(0.3, 0.8)
            if z > -1.5:
                M.append(K.quad((x - w, 0.004, z + w * 0.5), (x + w, 0.004, z + w * 0.5), (x + w * 0.7, 0.004, z - w * 0.5),
                                (x - w * 0.8, 0.004, z - w * 0.5), "#67a874" if k % 2 else "#4f8c60", layer=1))
        for k in range(26):
            x, z = rnd.uniform(-2.6, 2.6), rnd.uniform(-1.3, 0.9)
            if abs(x) < 0.45 and z < 0.6:
                continue
            M.append(K.sphere(x, 0.05, z, 0.045, ("#ffd6e4", "#ffe28a", "#ffffff", "#c9b8ff")[k % 4], 3, 6))
        for x, r, colr in ((-14, 9, "#5b3f78"), (2, 11, "#6a4884"), (18, 10, "#5b3f78")):
            M.append(K.sphere(x, -r * 0.62, -32, r, colr, 5, 12, layer=0))
        _PARK.extend(M)
    return _PARK


def _park_bg(c, W, H, t, cam):
    fill_bg(c, W, H, "#2c2463", "#ff9a76")
    c.drawRect(skia.Rect.MakeLTRB(0, 0.0, W, 0.3 * H), paint(shader=lin(0, 0, 0, 0.3 * H, [(0, "#1d1850", 1), (1, "#e9787a", 1)])))
    rnd = np.random.default_rng(3)
    for k in range(28):
        x, y = rnd.random() * W, rnd.random() * 0.17 * H
        circle(c, x, y, (1.5 + 2 * rnd.random()) * W / 1080, "#fff6e0", 0.35 + 0.35 * math.sin(t * 2 + k * 1.7))
    hz = K.anchor(cam, W, H, (0, 0, -60), 1.0)
    if hz:
        c.drawCircle(W * 0.8, hz[1] - 0.012 * H, 0.06 * W, paint("#ffd7a0", 0.9))
        c.drawCircle(W * 0.8, hz[1] - 0.012 * H, 0.2 * W, paint(shader=rad(W * 0.8, hz[1], 0.2 * W, [(0, "#ffd7a0", 0.5), (1, "#ffd7a0", 0)])))
    K.render(c, W, H, cam, _park_set(), light=DUSK_LIGHT, fog=("#b8789a", 6.0, 30.0, 0.6))
    K.glow_points(c, W, H, cam, [((-1.65, 2.3, -2.6), 1.2, "#ffd27a")])


def _brain_at(p, k=1.0, red=0.0):
    cx, cy, cz = p
    pts = [(-0.16, 0.06, 0.0, 0.17), (0.0, 0.11, 0.02, 0.19), (0.16, 0.05, 0.0, 0.17), (-0.1, -0.08, 0.04, 0.15),
           (0.1, -0.08, 0.04, 0.15), (0.0, 0.0, -0.1, 0.2), (0.21, -0.1, -0.02, 0.1)]
    return [K.sphere(cx + dx * k, cy + dy * k, cz + dz * k, r * k,
                     mix("#ff9eb8" if i % 2 else "#f78fae", "#ff3b4e", red), 5, 9) for i, (dx, dy, dz, r) in enumerate(pts)]


def _gut_at(p, yaw, k=1.0, t=0.0):
    """A coiled gut from a chain of spheres."""
    cx, cy, cz = p; M = []; pts = []
    for i in range(27):
        u_ = min(i / 26.0, 0.999)
        row = int(u_ * 3); f = u_ * 3 - row
        x = (-0.28 + 0.56 * f) if row % 2 == 0 else (0.28 - 0.56 * f)
        y = 0.2 - row * 0.2 + 0.07 * math.sin(f * math.pi) * (1 if row % 2 else -1)
        x *= k; y *= k
        v = _rot((x, y, 0.04 * math.sin(i)), yaw)
        pts.append((cx + v[0], cy + v[1], cz + v[2]))
        M.append(K.sphere(cx + v[0], cy + v[1], cz + v[2], 0.07 * k, "#ff9aa8" if i % 2 else "#f58595", 4, 8))
    return M, pts


def cr7_park(c, W, H, t, S):
    o = S.opts; mode = o.get("mode", "hook"); u = S.u; p = clamp(t / max(S.dur, 0.1))
    yaw0 = {"hook": -14, "alarm": -4, "blood": 8, "gut": -10, "hotline": 4, "flutter": 14, "end": -2}[mode]
    yaw = yaw0 + 9 * (p - 0.5)                                         # slow orbit around Kai
    cam = kcam(KP_P, yaw, push=1.05 - 0.04 * ease(p))
    _park_bg(c, W, H, t, cam)
    kx, ky, kh = K.anchor(cam, W, H, KP_P, 1.75); s = kh / 100.0
    pose, expr = "idle", "neutral"
    props, belly = [], ky - 46 * s

    if mode in ("hook", "end"):                                         # the Crush walks in along the path
        if mode == "hook":
            wk = eout(prog(t, 0.0, 2.4)); at = (lerp(3.4, 1.25, wk), 0.0, -2.35)
        else:
            at = (1.15, 0.0, -2.3)
        ca = K.anchor(cam, W, H, at, 1.75)
        al = vis(t, 0.0, d=0.5)
        if ca:
            _shadow(c, ca[0], ca[1], ca[2], al); mc.crush(c, ca[0], ca[1], ca[2], t, a=al, flip=True)

    if mode == "hook":
        hit = S.lt(0, 0.35)
        expr = "neutral" if t < hit else ("shocked" if t < hit + 0.9 else "nervous")
    elif mode == "alarm":
        expr = "nervous"
        bp = _p(KP_P, -0.82, 1.38, 0.15, yaw)
        props = _brain_at(bp, 0.85 + 0.04 * math.sin(t * 8), red=0.3 + 0.25 * math.sin(t * 7))
    elif mode == "blood":
        pose, expr = "fist", "nervous"
        hp = _p(KP_P, 0.92, 1.35, 0.15, yaw)
        beat = max(0.0, math.sin(t * 2 * math.pi * 1.8)) ** 6
        props = [K.heart(hp[0], hp[1], hp[2], 0.42 * (1 + 0.2 * beat), PINK, turn=yaw + 15 * math.sin(t))]
    elif mode == "gut":
        pose, expr = "point", "curious"
        gp = _p(KP_P, 0.8, 1.15, 0.15, yaw)
        props, gpts = _gut_at(gp, yaw, lerp(0.5, 0.85, eback(prog(t, 0.2, 0.6))), t)
    elif mode == "hotline":
        cta_on = t < S.ls(1) - 0.15
        pose, expr = ("wave", "happy") if cta_on else ("think", "curious")
        bp = _p(KP_P, 0.68, 1.62, 0.15, yaw); gp = _p(KP_P, 0.68, 0.6, 0.15, yaw)
        props = _brain_at(bp, 0.7) + _gut_at(gp, yaw, 0.55)[0]
        props.append(K.cylinder(bp[0], gp[1] + 0.12, bp[2], 0.025, bp[1] - gp[1] - 0.24, ACCENT, n=8, bias=-0.3))
    elif mode == "flutter":
        pose, expr = "cheeks", "blush"
    elif mode == "end":
        pose, expr = "wave", "lovestruck"

    if props:
        K.render(c, W, H, cam, props, light=K.Light((0.4, 0.8, 0.6), 0.62, 0.48, tint="#fff0e6"))

    if mode == "alarm":
        a1 = K.anchor(cam, W, H, bp, 0.3)
        if a1:
            bx, by, _ = a1; fl = 0.5 + 0.5 * math.sin(t * 7)
            c.drawCircle(bx, by, 150 * u, paint(shader=rad(bx, by, 150 * u, [(0, "#ff3b4e", 0.45 * fl), (1, "#ff3b4e", 0)])))
            _label(c, "BIG DEAL!", bx, by - 125 * u, 30 * u, vis(t, 0.3), bg=RED, W=W)
    elif mode == "blood":
        a1 = K.anchor(cam, W, H, hp, 0.3)
        if a1:
            hx, hy, _ = a1
            targets = [(kx - 15 * s, ky - 42 * s), (kx + 15 * s, ky - 42 * s), (kx - 6 * s, ky - 14 * s), (kx + 6 * s, ky - 14 * s)]
            pb = vis(t, S.lt(0, 0.2))
            for k in range(16):
                ph = (t * 0.6 + k / 16) % 1.0; tx, ty = targets[k % 4]
                x = lerp(hx, tx, ph); y = lerp(hy, ty, ph) - math.sin(math.pi * ph) * 40 * u
                circle(c, x, y, 12 * u, "#d61f3c", pb * math.sin(math.pi * ph)); circle(c, x, y, 12 * u, NAVY, pb * math.sin(math.pi * ph), stroke=2 * u)
    elif mode == "gut":
        a1 = K.anchor(cam, W, H, gp, 0.5)
        if a1:
            gx, gy, gh = a1; pn = vis(t, S.lt(0, 0.3))
            rnd = np.random.default_rng(9)
            for k in range(40):                                         # neurons twinkling over the gut
                q = gpts[int(rnd.random() * len(gpts))]
                a2 = K.anchor(cam, W, H, q, 0.1)
                if a2:
                    tw_ = 0.5 + 0.5 * math.sin(t * 5 + k * 1.3)
                    mc.sparkle(c, a2[0] + rnd.normal() * 14 * u, a2[1] + rnd.normal() * 14 * u, 10 * u, ACCENT, pn * tw_)
            _label(c, "200–600 MILLION", gx, gy - 210 * u, 34 * u, pn, fg=NAVY, bg=ACCENT, W=W)
            _label(c, "NERVE CELLS", gx, gy - 152 * u, 28 * u, pn, W=W)
    elif mode == "hotline":
        top = K.anchor(cam, W, H, (bp[0], bp[1] - 0.12, bp[2]), 0.1); bot = K.anchor(cam, W, H, (gp[0], gp[1] + 0.12, gp[2]), 0.1)
        ph_ = vis(t, S.ls(1))
        if top and bot and ph_ > 0:
            (x1, y1, _), (x0, y0, _) = top, bot
            for k in range(10):                                         # 9 of 10 pulses travel up, 1 down
                ph = (t * 0.55 + k / 10) % 1.0
                up = k != 4
                y = lerp(y0, y1, ph if up else 1 - ph); x = lerp(x0, x1, ph if up else 1 - ph)
                circle(c, x, y, 11 * u, ACCENT if up else "#7fd8ff", ph_); circle(c, x, y, 11 * u, NAVY, ph_, stroke=2.5 * u)
            _label(c, "BRAIN", x1, y1 - 112 * u, 24 * u, ph_, W=W)
            _label(c, "GUT", x0, y0 + 92 * u, 24 * u, ph_, W=W)
            _label(c, "↑ 8–9 IN 10", (x0 + x1) / 2 + 150 * u, (y0 + y1) / 2, 28 * u, vis(t, S.lt(1, 0.55)), fg=NAVY, bg=ACCENT, W=W)

    _shadow(c, kx, ky, kh)
    mc.kai(c, kx, ky, kh, t, pose, expr, seed=2.3)
    if mode == "alarm":                                                 # adrenaline sparks spread down the body
        pa = vis(t, S.lt(0, 0.72))
        for k in range(14):
            ph = (t * 0.7 + k / 14) % 1.0
            ang = k * 2.4
            px = kx + math.cos(ang) * (12 + 14 * ph) * s; py = ky - (88 - 70 * ph) * s
            mc.sparkle(c, px, py, 16 * u * (1 - ph * 0.4), ACCENT, pa * math.sin(math.pi * ph))

    # stomach badge on Kai's belly
    if mode == "hook":
        hit = S.lt(0, 0.35); f = prog(t, hit, 0.7)
        _stomach(c, kx, belly, 0.62 * s, 360 * ease(f), a=vis(t, hit - 0.1, d=0.2))
    elif mode == "blood":
        dim = ease(prog(t, S.lt(0, 0.55), 0.8))
        _stomach(c, kx, belly, 0.62 * s, 0, colr=mix("#ff8fb1", "#9aa0b8", dim), a=vis(t, S.lt(0, 0.45)), sign="−" if dim > 0.5 else None)
    elif mode == "flutter":
        _stomach(c, kx, belly, 0.62 * s, 8 * math.sin(t * 9), colr="#b9bfd6", a=vis(t, 0.1))
        for k in range(7):
            ang = t * (1.0 + 0.13 * k) + k * 0.9
            bx = kx + math.cos(ang) * (20 + 4 * (k % 3)) * s
            by = belly - (6 + 10 * math.sin(ang * 1.6 + k)) * s
            _butterfly(c, bx, by, 1.6 * u, t + k * 0.3, (ACCENT, "#ff8fb1", "#7fd8ff")[k % 3], vis(t, 0.3 + k * 0.12), 20 * math.sin(ang))
    elif mode == "end":
        for k in range(4):
            ang = t * (0.9 + 0.1 * k) + k * 1.6
            _butterfly(c, kx + math.cos(ang) * 26 * s, ky - (60 + 14 * math.sin(ang * 1.3)) * s, 1.4 * u, t + k * 0.4,
                       (ACCENT, "#ff8fb1", "#7fd8ff", ACCENT)[k], vis(t, 0.4 + 0.2 * k))
    _series(c, W, H, t, S, u, mode)


SCENES = {"cr7_hall": cr7_hall, "cr7_park": cr7_park}
