"""The Crush Files #1: what your brain does when your crush texts back (Short, 1080x1920).

One scene function, cf1_room, with a mode per beat. The bedroom is a low-poly 3D set from kit3d
(rendered once per size and cached); Kai and the Crush are the flat 2D characters from mc,
planted on the floor with kit3d.anchor. Kai stays inside the Shorts content band
(head ~0.20H, feet ~0.57H); captions burn in at 0.635H.
"""
import math
import skia
from core import *
from scenes import vis
import kit3d as K
import mc

NAVY = "#0b1030"
PINK = "#ff3d6e"
CAM = ((0.3, 1.7, 3.2), (-0.2, 0.2, -1.5), 60)
KAI_AT = (-0.15, 0.0, -0.9)
CRUSH_AT = (0.75, 0.0, -2.05)
_SET = []


def _cam():
    return K.Cam(*CAM[:2], fov=CAM[2])


def _bedroom(c, W, H, cam):
    if not _SET:
        _SET.extend(K.bedroom())
    M, G = _SET

    def draw(cc):
        fill_bg(cc, W, H, "#0b1030", "#1b2350")
        K.render(cc, W, H, cam, M)
        K.glow_points(cc, W, H, cam, G)
    K.CACHE.draw(c, W, H, "cf1_bedroom", draw)


def _shadow(c, x, y, h, a=1.0):
    c.drawOval(skia.Rect.MakeLTRB(x - h * 0.16, y - h * 0.025, x + h * 0.16, y + h * 0.025), paint("#000000", 0.25 * a, blur=8))


def _bubble(c, x, y, s, p, kind="heart", a=1.0):
    """Message bubble that pops in with progress p. kind: heart | dots | lines."""
    if p <= 0:
        return
    sc = lerp(0.6, 1.0, eback(p)); al = a * clamp(p * 2)
    w, h = 150 * s, 92 * s
    c.save(); c.translate(x, y); c.scale(sc, sc)
    r = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-w / 2, -h / 2, w / 2, h / 2), 26 * s, 26 * s)
    tail = poly([(-w * 0.28, h / 2 - 4 * s), (-w * 0.42, h / 2 + 22 * s), (-w * 0.08, h / 2 - 4 * s)])
    for shp in (r, tail):
        (c.drawRRect if shp is r else c.drawPath)(shp, paint("#ffffff", al))
    c.drawRRect(r, paint(NAVY, al, stroke=5 * s)); c.drawPath(tail, paint(NAVY, al, stroke=5 * s))
    c.drawRect(skia.Rect.MakeLTRB(-w * 0.3, h / 2 - 7 * s, -w * 0.06, h / 2 - 1 * s), paint("#ffffff", al))
    if kind == "heart":
        hp = mc.heart_path(0, 6 * s, 30 * s); c.drawPath(hp, paint(PINK, al)); c.drawPath(hp, paint(NAVY, al, stroke=4 * s))
    elif kind == "dots":
        for k in range(3):
            circle(c, (k - 1) * 34 * s, 0, 10 * s, NAVY, al * (0.4 + 0.6 * (k == int(p * 6) % 3)))
    else:
        for k, ww in enumerate((0.62, 0.42)):
            rrect(c, -w * 0.36, -22 * s + k * 30 * s, w * ww, 14 * s, 7 * s, "#b9c2e8", al)
    c.restore()


def _butterfly(c, x, y, s, t, colr, a=1.0, ang=0.0):
    flap = 0.25 + 0.75 * abs(math.sin(t * 13.0))
    c.save(); c.translate(x, y); c.rotate(ang)
    for side in (-1, 1):
        c.save(); c.scale(side * flap, 1)
        oval(c, 14 * s, -9 * s, 15 * s, 11 * s, colr, a); oval(c, 11 * s, 9 * s, 10 * s, 8 * s, mix(colr, "#ffffff", 0.35), a)
        c.drawOval(skia.Rect.MakeLTRB(-1 * s, -20 * s, 29 * s, 2 * s), paint(NAVY, a, stroke=3 * s))
        c.restore()
    rrect(c, -3 * s, -14 * s, 6 * s, 28 * s, 3 * s, NAVY, a)
    c.restore()


def _brain(beat):
    """Low-poly brain from spheres, a little bigger on each heartbeat-ish pulse."""
    cx, cy, cz = -0.98, 1.5, -1.1
    k = 1.0 + 0.05 * beat
    pts = [(-0.16, 0.06, 0.0, 0.17), (0.0, 0.11, 0.02, 0.19), (0.16, 0.05, 0.0, 0.17), (-0.1, -0.08, 0.04, 0.15),
           (0.1, -0.08, 0.04, 0.15), (0.0, 0.0, -0.1, 0.2), (0.21, -0.1, -0.02, 0.1)]
    return [K.sphere(cx + dx * k, cy + dy * k, cz + dz * k, r * k, "#ff9eb8" if i % 2 else "#f78fae", 5, 9)
            for i, (dx, dy, dz, r) in enumerate(pts)], (cx, cy, cz)


def cf1_room(c, W, H, t, S):
    o = S.opts; mode = o.get("mode", "hook"); u = S.u
    cam = _cam()
    z = 1.0 + 0.035 * t / max(S.dur, 0.1)                 # slow push-in
    a_k = K.anchor(cam, W, H, KAI_AT, 1.75)
    kx, ky, kh = a_k
    c.save(); c.translate(kx, ky - kh * 0.5); c.scale(z, z); c.translate(-kx, -(ky - kh * 0.5))
    _bedroom(c, W, H, cam)
    s = kh / 100.0
    props, pose, expr, glow = [], "phone", "neutral", 1.0

    if mode == "hook":
        hit = S.lt(0, 0.0) + 0.05
        expr = "neutral" if t < hit else ("shocked" if t < hit + 0.9 else "blush")
        glow = 0.35 + 0.65 * (t > hit) * (0.6 + 0.4 * math.sin(t * 12))
    elif mode == "maybe":
        expr = "nervous"
        props = K.question_mark(0.72, 1.05, -1.0, 0.85, NAVY, side=ACCENT, turn=25 * math.sin(t * 1.6))
    elif mode == "reward":
        expr = "lovestruck" if t > S.lt(0, 0.25) else "shocked"
        beat = max(0.0, math.sin(t * 7.0)) ** 4
        props, _ = _brain(beat)
    elif mode == "flutter":
        if t < S.ls(1) - 0.1:
            pose, expr = "wave", "happy"
        else:
            pose, expr = "cheeks", "blush"
        beat = max(0.0, math.sin(t * 2 * math.pi * 1.9)) ** 6
        props = [K.heart(0.74, 1.2, -1.0, 0.42 * (1 + 0.18 * beat), PINK, turn=18 * math.sin(t))]
    elif mode == "reread":
        expr = "curious"
    elif mode == "end":
        pose = "wave"; expr = "happy"

    if props:
        K.render(c, W, H, cam, props, light=K.Light((-0.45, 0.8, 0.6), 0.62, 0.48))
    if mode == "reward":                                   # glowing reward spot + dopamine sparks
        _, (bx, by, bz) = _brain(0)
        g = K.anchor(cam, W, H, (bx, by - 0.12, bz), 0.1)
        if g:
            gx, gy, _ = g; pulse = 0.6 + 0.4 * math.sin(t * 7.0)
            c.drawCircle(gx, gy, 60 * u, paint(shader=rad(gx, gy, 60 * u, [(0, ACCENT, 0.9 * pulse), (1, ACCENT, 0)])))
            for k in range(7):
                ph = (t * 0.7 + k / 7.0) % 1.0
                px = lerp(gx, kx + 6 * s, ph); py = lerp(gy, ky - kh * 0.86, ph) - math.sin(math.pi * ph) * 70 * u
                circle(c, px, py, 7 * u, ACCENT, math.sin(math.pi * ph))
    if mode == "end":
        ca = K.anchor(cam, W, H, CRUSH_AT, 1.75)
        if ca:
            cx_, cy_, ch_ = ca; al = vis(t, S.lt(0, 0.35), d=0.6)
            if al > 0:
                _shadow(c, cx_, cy_, ch_, al); mc.crush(c, cx_, cy_, ch_, t, a=al, flip=True)

    _shadow(c, kx, ky, kh)
    mc.kai(c, kx, ky, kh, t, pose, expr, phone_glow=glow, seed=0.7)

    if mode == "hook":
        _bubble(c, kx + 30 * s, ky - 84 * s, 1.1 * u, prog(t, S.lt(0, 0.0) + 0.05, 0.35), "heart")
    elif mode == "maybe":
        _bubble(c, kx + 30 * s, ky - 84 * s, 1.1 * u, 1.0, "dots")
        p50 = vis(t, S.ls(1))
        if p50 > 0:                                        # 50/50 chance dial
            dx, dy, r = kx - 30 * s, ky - 75 * s, 15 * s
            c.save(); c.translate(dx, dy); sc = lerp(0.6, 1, eback(p50)); c.scale(sc, sc)
            c.drawArc(skia.Rect.MakeLTRB(-r, -r, r, r), 90, 180, True, paint(ACCENT, p50))
            c.drawArc(skia.Rect.MakeLTRB(-r, -r, r, r), -90, 180, True, paint("#ff8fb1", p50))
            c.drawCircle(0, 0, r, paint(NAVY, p50, stroke=4 * u))
            text(c, "50/50", 0, r + 34 * u, 44 * u, "#ffffff", p50, w=900, stroke=8 * u, stroke_col=NAVY)
            c.restore()
    elif mode == "flutter" and t >= S.ls(1) - 0.1:
        for k in range(6):
            ang = t * (1.1 + 0.15 * k) + k * 1.05
            bx = kx + math.cos(ang) * (16 + 3 * (k % 3)) * s
            by = ky - (48 + 8 * math.sin(ang * 1.7 + k)) * s
            _butterfly(c, bx, by, 1.6 * u, t + k * 0.3, (ACCENT, "#ff8fb1", "#7fd8ff")[k % 3], vis(t, S.ls(1) + k * 0.12), 20 * math.sin(ang))
    elif mode == "reread":
        for k in range(4):
            p = prog(t, 0.2 + k * 0.45, 0.35)
            _bubble(c, kx + (29 + 5 * (k % 2)) * s, ky - (62 + 13 * k) * s, 0.85 * u, p, "lines" if k < 3 else "heart")
        n = min(10, 1 + int(t / max(S.dur, 0.1) * 12))
        chip(c, f"READ ×{n}", kx - 24 * s, ky - 66 * s, 1.0, 34 * u, bg=PINK, fg="#ffffff", a=1)
    c.restore()

    if mode != "end":
        chip(c, "THE CRUSH FILES", W / 2, 0.085 * H, 1.0, 30 * u, bg=NAVY, fg=ACCENT, a=0.9, dot=PINK)
    else:
        p = prog(t, 0.1, 0.4)
        sz = fit("THE CRUSH FILES", W * 0.86, 96 * u, 900)
        text(c, "THE CRUSH FILES", W / 2, 0.11 * H, sz, ACCENT, p, w=900, stroke=10 * u, stroke_col=NAVY)
        chip(c, "MORE ON THE CHANNEL", W / 2, 0.17 * H, vis(t, S.lt(0, 0.4)), 40 * u, bg="#ffffff", fg=NAVY, a=1)
    if o.get("hook"):                                      # hook text between the series tag and Kai's head
        sz = fit(o["hook"], W * 0.9, 92 * u, 900)
        text(c, o["hook"], W / 2, 0.165 * H, sz, "#ffffff", eout(t / 0.25), w=900, stroke=10 * u, stroke_col=NAVY)


SCENES = {"cf1_room": cf1_room}
