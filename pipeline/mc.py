"""The channel's 2D main character, Kai, and "the Crush" silhouette (the crush series; see STYLE.md).

Flat cartoon style with thick navy outlines, drawn entirely in code so every video matches the
character sheet. Kai is 19: the crush series stays PG and wholesome.

    kai(c, x, y, h, t, pose="idle", expr="neutral", look=(0, 0), flip=False, P=KAI, ...)

draws Kai with the feet at screen point (x, y) and a total height of h pixels; plant him in a 3D
set with kit3d.anchor(). The figure is built in units where the feet are at (0, 0) and the top of
the hair is at about (0, -104), so 1 unit = h / 100 px.

Poses:       idle, wave, phone, think, shrug, point, cheeks, fist
Expressions: neutral, happy, blush, nervous, shocked, lovestruck, sad, curious, talk
"""
import math
import skia
from core import *

KAI = dict(
    skin="#b07045", skin_sh="#93573a", hair="#1e1b33", hair_hi="#4a4580",
    hoodie="#3a4fd0", hoodie_sh="#2c3ca6", string=ACCENT, patch=ACCENT,
    pants="#2b2e3d", pants_sh="#1f2130", shoe="#f5f2ea", shoe_acc=ACCENT, sole="#cfc8b8",
    phones="#ff5c8a", phones_sh="#d9436f", iris="#3b2416", blush="#ff6f91",
    mouth="#6e1f2e", tongue="#ff7a8a", ol="#0b1030", olw=1.6, hair_style="messy", headphones=True)

CRUSH = dict(KAI, skin="#3a2a63", skin_sh="#3a2a63", hair="#3a2a63", hair_hi="#3a2a63",
             hoodie="#3a2a63", hoodie_sh="#3a2a63", string="#3a2a63", patch=None,
             pants="#3a2a63", pants_sh="#3a2a63", shoe="#3a2a63", shoe_acc="#3a2a63", sole="#3a2a63",
             ol="#ff8fb1", olw=1.3, hair_style="fluffy", headphones=False, face=False)

SHOULDER_L, SHOULDER_R = (-12.0, -59.5), (12.0, -59.5)

# arms: (shoulder, elbow, hand) for the left and right arm; "front": hands go over the face
POSES = {
    "idle":   dict(L=[SHOULDER_L, (-15.2, -49.0), (-15.0, -39.5)], R=[SHOULDER_R, (15.2, -49.0), (15.0, -39.5)]),
    "wave":   dict(L=[SHOULDER_L, (-15.2, -49.0), (-15.0, -39.5)], R=[SHOULDER_R, (20.5, -63.0), (24.0, -75.0)], open_r=True),
    "phone":  dict(L=[SHOULDER_L, (-14.5, -46.5), (-5.6, -48.6)], R=[SHOULDER_R, (14.5, -46.5), (5.6, -48.6)], phone=True),
    "think":  dict(L=[SHOULDER_L, (-11.5, -48.5), (8.0, -50.5)], R=[SHOULDER_R, (17.5, -51.0), (5.5, -67.6)], front=True),
    "shrug":  dict(L=[SHOULDER_L, (-19.5, -52.0), (-25.0, -59.0)], R=[SHOULDER_R, (19.5, -52.0), (25.0, -59.0)], open_l=True, open_r=True),
    "point":  dict(L=[SHOULDER_L, (-15.2, -49.0), (-15.0, -39.5)], R=[SHOULDER_R, (21.0, -61.0), (29.5, -64.5)], finger_r=True),
    "cheeks": dict(L=[SHOULDER_L, (-17.0, -52.0), (-12.8, -73.0)], R=[SHOULDER_R, (17.0, -52.0), (12.8, -73.0)], front=True),
    "fist":   dict(L=[SHOULDER_L, (-15.2, -49.0), (-15.0, -39.5)], R=[SHOULDER_R, (20.0, -63.0), (21.5, -75.0)]),
}

# eyes, brows, mouth, extras
EXPRS = {
    "neutral":    dict(eyes="open", brows="flat", mouth="smile"),
    "happy":      dict(eyes="happy", brows="up", mouth="grin"),
    "blush":      dict(eyes="open", brows="worried", mouth="small", blush=1.0, look=(0.6, 0.4)),
    "nervous":    dict(eyes="small", brows="worried", mouth="wobble", sweat=True, blush=0.4),
    "shocked":    dict(eyes="wide", brows="high", mouth="o"),
    "lovestruck": dict(eyes="heart", brows="up", mouth="grin", blush=1.0, hearts=True),
    "sad":        dict(eyes="sad", brows="worried", mouth="frown"),
    "curious":    dict(eyes="open", brows="one", mouth="smirk", look=(0.5, -0.2)),
    "talk":       dict(eyes="open", brows="flat", mouth="talk"),
}


# ------------------------------------------------------------------ helpers
def _pp(P, colr, stroke=0, a=1.0, cap="round"):
    return paint(colr, a, stroke=stroke, blur=P.get("blur", 0), cap=cap)

def _shape(c, path, fill, P, a=1.0, ol=1.0):
    if fill:
        c.drawPath(path, _pp(P, fill, a=a))
    if ol:
        c.drawPath(path, _pp(P, P["ol"], stroke=P["olw"] * ol, a=a))

def _cap(c, pts, w, fill, P, a=1.0):
    """Outlined capsule along a polyline (limbs, sleeves)."""
    path = skia.Path(); path.moveTo(*pts[0])
    if len(pts) == 3:
        path.quadTo(pts[1][0], pts[1][1], pts[2][0], pts[2][1])
    else:
        for q in pts[1:]: path.lineTo(*q)
    c.drawPath(path, _pp(P, P["ol"], stroke=w + 2 * P["olw"], a=a))
    c.drawPath(path, _pp(P, fill, stroke=w, a=a))

def _bez(pts):
    """Smooth closed path through points (Catmull-Rom to cubic)."""
    n = len(pts); p = skia.Path(); p.moveTo(*pts[0])
    for i in range(n):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        p.cubicTo(c1[0], c1[1], c2[0], c2[1], p2[0], p2[1])
    p.close(); return p

def heart_path(x, y, s):
    p = skia.Path(); p.moveTo(x, y + s * 0.35)
    p.cubicTo(x - s * 1.05, y - s * 0.35, x - s * 0.45, y - s * 1.05, x, y - s * 0.45)
    p.cubicTo(x + s * 0.45, y - s * 1.05, x + s * 1.05, y - s * 0.35, x, y + s * 0.35)
    p.close(); return p

def sparkle(c, x, y, s, colr="#ffffff", a=1.0):
    p = skia.Path(); p.moveTo(x, y - s)
    for dx, dy, ex, ey in ((0.18, -0.18, s, 0), (0.18, 0.18, 0, s), (-0.18, 0.18, -s, 0), (-0.18, -0.18, 0, -s)):
        p.quadTo(x + dx * s, y + dy * s, x + ex, y + ey)
    p.close(); c.drawPath(p, paint(colr, a))


# ------------------------------------------------------------------ body parts
def _legs(c, P, a):
    for sx in (-1, 1):
        _cap(c, [(sx * 5.2, -37.5), (sx * 5.6, -21.0), (sx * 5.8, -5.5)], 9.0, P["pants"], P, a)
    c.drawPath(_bez([(-9.8, -40.5), (9.8, -40.5), (9.4, -34.0), (0.0, -32.0), (-9.4, -34.0)]), _pp(P, P["pants"], a=a))
    for sx in (-1, 1):           # shoes
        r = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(sx * 6.0 - 6.5 + sx * 1.8, -6.6, sx * 6.0 + 6.5 + sx * 1.8, 0.4), 3.3, 3.3)
        c.drawRRect(r, _pp(P, P["shoe"], a=a))
        c.drawRect(skia.Rect.MakeLTRB(sx * 6.0 - 6.2 + sx * 1.8, -1.6, sx * 6.0 + 6.2 + sx * 1.8, 0.0), _pp(P, P["sole"], a=a))
        line(c, sx * 6.0 - 3.0 + sx * 1.8, -4.4, sx * 6.0 + 2.5 + sx * 1.8, -3.0, P["shoe_acc"], 1.3, a)
        c.drawRRect(r, _pp(P, P["ol"], stroke=P["olw"], a=a))

def _torso(c, P, a, flip):
    body = skia.Path()
    body.moveTo(-5.5, -64.2)
    body.cubicTo(-9.5, -63.8, -12.8, -63.0, -13.3, -59.0)
    body.cubicTo(-13.8, -52.0, -13.6, -44.0, -13.3, -38.5)
    body.cubicTo(-8.0, -36.4, 8.0, -36.4, 13.3, -38.5)
    body.cubicTo(13.6, -44.0, 13.8, -52.0, 13.3, -59.0)
    body.cubicTo(12.8, -63.0, 9.5, -63.8, 5.5, -64.2)
    body.quadTo(0.0, -60.5, -5.5, -64.2); body.close()
    c.drawPath(body, _pp(P, P["hoodie"], a=a))
    c.save(); c.clipPath(body, doAntiAlias=True)            # cel shade on the far side + hem band
    c.drawPath(_bez([(7.5, -66), (16, -66), (16, -34), (9.0, -34), (10.5, -50)]), _pp(P, P["hoodie_sh"], a=a))
    c.drawRect(skia.Rect.MakeLTRB(-15, -41.2, 15, -34), _pp(P, P["hoodie_sh"], a=a))
    c.restore()
    c.drawPath(body, _pp(P, P["ol"], stroke=P["olw"], a=a))
    pocket = poly([(-7.8, -48.0), (7.8, -48.0), (9.0, -41.6), (-9.0, -41.6)])
    c.drawPath(pocket, _pp(P, P["ol"], stroke=P["olw"] * 0.6, a=a * 0.8))
    if P.get("patch"):                                   # the "?" patch: the channel's what-if mark
        px, py = 6.5, -53.6
        circle(c, px, py, 3.2, P["patch"], a)
        c.drawCircle(px, py, 3.2, _pp(P, P["ol"], stroke=P["olw"] * 0.7, a=a))
        c.save(); c.translate(px, py)
        if flip: c.scale(-1, 1)
        q = skia.Path(); q.moveTo(-1.35, -0.9); q.cubicTo(-1.35, -2.7, 1.45, -2.7, 1.45, -1.0)
        q.cubicTo(1.45, 0.1, 0.0, 0.1, 0.0, 1.0)
        c.drawPath(q, _pp(P, P["ol"], stroke=0.95, a=a)); c.drawCircle(0.0, 2.15, 0.55, _pp(P, P["ol"], a=a))
        c.restore()
    for sx in (-1, 1):                                    # drawstrings
        line(c, sx * 2.6, -61.8, sx * 3.1, -53.5 + (sx > 0) * 1.2, P["string"], 0.9, a)
        circle(c, sx * 3.1, -53.2 + (sx > 0) * 1.2, 0.8, P["string"], a)

def _hood(c, P, a):
    _shape(c, _bez([(-11.5, -63.0), (-6.0, -67.5), (6.0, -67.5), (11.5, -63.0), (6.0, -60.8), (-6.0, -60.8)]), P["hoodie_sh"], P, a)

def _headphones(c, P, a):
    """Headphones resting around the neck: two cups under the jaw (drawn after the face)."""
    if not P.get("headphones"):
        return
    for sx in (-1, 1):
        c.save(); c.translate(sx * 10.6, -63.6); c.rotate(sx * 18)
        r = skia.Rect.MakeLTRB(-3.3, -3.9, 3.3, 3.9)
        c.drawOval(r, _pp(P, P["phones"], a=a)); c.drawOval(r, _pp(P, P["ol"], stroke=P["olw"] * 0.9, a=a))
        oval(c, -sx * 0.6, 0.2, 1.7, 2.4, P["phones_sh"], a)
        c.restore()

def _hand(c, x, y, P, a, open_=False, finger=False, fist=False):
    r = 3.7 if open_ else 3.4
    if finger:
        _cap(c, [(x, y), (x + 4.2, y - 1.6)], 1.9, P["skin"], P, a)
    circle(c, x, y, r, P["skin"], a); c.drawCircle(x, y, r, _pp(P, P["ol"], stroke=P["olw"], a=a))
    if open_:
        for k in (-1, 0, 1):
            line(c, x + k * 1.3, y - 3.0, x + k * 1.6, y - 0.8, P["ol"], 0.6, a * 0.7)
    if fist:
        line(c, x - 1.8, y - 0.6, x + 1.8, y - 0.6, P["ol"], 0.6, a * 0.7)

def _arms(c, P, a, pose, t):
    pz = POSES[pose]
    for side in ("L", "R"):
        pts = [list(q) for q in pz[side]]
        if pose == "wave" and side == "R":
            pts[2][0] += 2.2 * math.sin(t * 9.0); pts[1][0] += 0.8 * math.sin(t * 9.0)
        _cap(c, pts, 7.6, P["hoodie"], P, a)
        hx, hy = pts[2]; ex, ey = pts[1]
        d = math.hypot(hx - ex, hy - ey) or 1
        cx_, cy_ = hx - (hx - ex) / d * 2.4, hy - (hy - ey) / d * 2.4      # cuff
        c.drawCircle(cx_, cy_, 4.3, _pp(P, P["hoodie_sh"], a=a)); c.drawCircle(cx_, cy_, 4.3, _pp(P, P["ol"], stroke=P["olw"] * 0.7, a=a))
        _hand(c, hx, hy, P, a, open_=pz.get("open_" + side.lower(), False),
              finger=pz.get("finger_" + side.lower(), False), fist=(pose == "fist" and side == "R"))

def _phone(c, P, a, glow):
    r = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-4.6, -61.5, 4.6, -46.0), 1.6, 1.6)
    c.drawRRect(r, _pp(P, "#1c1f33", a=a)); c.drawRRect(r, _pp(P, P["ol"], stroke=P["olw"] * 0.8, a=a))
    scr = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-3.6, -60.4, 3.6, -47.2), 1.0, 1.0)
    c.drawRRect(scr, paint("#bfe9ff", a * (0.35 + 0.65 * glow)))

def _head_back(c, P, a):
    if P["hair_style"] == "fluffy":
        _shape(c, _bez([(0, -106), (13, -103), (19, -92), (20, -78), (18, -66), (13, -63), (-13, -63), (-18, -66),
                        (-20, -78), (-19, -92), (-13, -103)]), P["hair"], P, a)
    else:
        _shape(c, _bez([(0, -104.5), (12, -101.5), (18, -92), (17.5, -80), (15.5, -74), (-15.5, -74), (-17.5, -80),
                        (-18, -92), (-12, -101.5)]), P["hair"], P, a)
    for sx in (-1, 1):                                   # ears
        circle(c, sx * 15.2, -79.0, 3.1, P["skin"], a); c.drawCircle(sx * 15.2, -79.0, 3.1, _pp(P, P["ol"], stroke=P["olw"], a=a))

def _face(c, P, a):
    f = skia.Path()
    f.moveTo(0, -99.0)
    f.cubicTo(9.5, -99.0, 15.6, -93.0, 15.6, -84.0)
    f.cubicTo(15.6, -79.0, 15.0, -76.0, 13.6, -73.5)
    f.cubicTo(10.5, -68.5, 5.0, -66.3, 0, -66.3)
    f.cubicTo(-5.0, -66.3, -10.5, -68.5, -13.6, -73.5)
    f.cubicTo(-15.0, -76.0, -15.6, -79.0, -15.6, -84.0)
    f.cubicTo(-15.6, -93.0, -9.5, -99.0, 0, -99.0); f.close()
    _shape(c, f, P["skin"], P, a)
    return f

def _fringe_path(P):
    if P["hair_style"] == "fluffy":
        pts = [(-17.5, -80), (-17, -95), (-8, -104), (6, -104), (16, -97), (17.5, -82), (13, -88), (9, -85),
               (5, -89.5), (0, -86.5), (-5, -90), (-10, -86), (-14, -89)]
    else:
        pts = [(-16.8, -82.5), (-16.4, -95.0), (-9.0, -103.0), (0, -104.8), (9.5, -102.5), (16.4, -95.0), (16.8, -82.5),
               (13.6, -88.6), (11.0, -85.6), (8.6, -89.8), (4.8, -86.2), (1.2, -90.2), (-2.8, -86.6), (-6.0, -90.0),
               (-9.6, -86.0), (-12.4, -89.4), (-14.6, -85.2)]
    return poly(pts)

def _hair_front(c, P, a, t):
    _shape(c, _fringe_path(P), P["hair"], P, a)
    if P["hair_style"] != "fluffy":
        hi = skia.Path(); hi.moveTo(-9.0, -99.5); hi.quadTo(-1.0, -102.5, 7.0, -100.0)
        c.drawPath(hi, _pp(P, P["hair_hi"], stroke=1.6, a=a))
        sway = math.sin(t * 2.2) * 0.8                    # the cowlick
        ah = skia.Path(); ah.moveTo(1.0, -103.8)
        ah.cubicTo(2.0 + sway, -110.0, 7.5 + sway, -111.5, 8.5 + sway, -108.0)
        ah.cubicTo(6.5 + sway, -108.8, 4.5, -106.5, 4.2, -103.6); ah.close()
        _shape(c, ah, P["hair"], P, a)


# ------------------------------------------------------------------ face
def _eye(c, P, a, x, y, kind, lx, ly):
    ol = P["ol"]
    if kind in ("open", "small", "sad", "wide"):
        ry = {"open": 4.4, "small": 3.6, "sad": 4.0, "wide": 4.9}[kind]
        rx = {"open": 3.4, "small": 2.9, "sad": 3.3, "wide": 3.7}[kind]
        oval(c, x, y, rx, ry, "#ffffff", a)
        if kind == "wide":
            circle(c, x + lx * 0.6, y + ly * 0.6, 1.25, ol, a)
        else:
            ir = (2.35, 3.2) if kind != "small" else (1.8, 2.5)
            ix, iy = x + lx * 0.9, y + ly * 0.9 + 0.3
            oval(c, ix, iy, ir[0], ir[1], P["iris"], a)
            oval(c, ix, iy + 0.3, ir[0] * 0.5, ir[1] * 0.5, "#120a06", a)
            circle(c, ix - 0.8, iy - 1.3, 0.85, "#ffffff", a); circle(c, ix + 0.9, iy + 1.2, 0.4, "#ffffff", a)
        c.drawOval(skia.Rect.MakeLTRB(x - rx, y - ry, x + rx, y + ry), _pp(P, ol, stroke=0.8, a=a))
        lid = skia.Path(); lid.moveTo(x - rx - 0.4, y - ry * 0.35)
        lid.quadTo(x - rx * 0.3, y - ry - 1.0, x + rx + 0.5, y - ry * 0.55)
        c.drawPath(lid, _pp(P, ol, stroke=1.4, a=a))
        if kind == "sad":                                # heavy lid
            cover = skia.Path(); cover.moveTo(x - rx - 0.6, y - ry - 0.6); cover.lineTo(x + rx + 0.6, y - ry - 0.6)
            cover.lineTo(x + rx + 0.6, y - ry * 0.25); cover.quadTo(x, y - ry * 0.05, x - rx - 0.6, y - ry * 0.25); cover.close()
            c.drawPath(cover, _pp(P, P["skin"], a=a))
            l2 = skia.Path(); l2.moveTo(x - rx - 0.4, y - ry * 0.25); l2.quadTo(x, y - ry * 0.05, x + rx + 0.4, y - ry * 0.25)
            c.drawPath(l2, _pp(P, ol, stroke=1.3, a=a))
    elif kind == "closed":
        p = skia.Path(); p.moveTo(x - 3.4, y + 0.2); p.quadTo(x, y + 2.0, x + 3.4, y + 0.2)
        c.drawPath(p, _pp(P, ol, stroke=1.3, a=a))
    elif kind == "happy":
        p = skia.Path(); p.moveTo(x - 3.4, y + 1.4); p.quadTo(x, y - 3.2, x + 3.4, y + 1.4)
        c.drawPath(p, _pp(P, ol, stroke=1.5, a=a))
    elif kind == "heart":
        h = heart_path(x, y, 4.6); c.drawPath(h, _pp(P, "#ff3d6e", a=a)); c.drawPath(h, _pp(P, ol, stroke=0.9, a=a))
        circle(c, x - 1.5, y - 1.6, 0.8, "#ffffff", a * 0.9)

def _brows(c, P, a, kind, lx):
    for sx in (-1, 1):
        x = sx * 6.2 + lx * 0.8; y = -86.6
        inner, outer = (x - sx * 2.6, y - 0.5), (x + sx * 2.8, y - 0.3)
        if kind == "up":       inner, outer = (inner[0], y - 1.2), (outer[0], y - 1.9)
        if kind == "high":     inner, outer = (inner[0], y - 2.4), (outer[0], y - 2.8)
        if kind == "worried":  inner, outer = (inner[0], y - 1.9), (outer[0], y + 0.4)
        if kind == "one" and sx > 0: inner, outer = (inner[0], y - 2.0), (outer[0], y - 3.0)
        mid = ((inner[0] + outer[0]) / 2, min(inner[1], outer[1]) - 0.7)
        p = skia.Path(); p.moveTo(*inner); p.quadTo(mid[0], mid[1], outer[0], outer[1])
        c.drawPath(p, _pp(P, P["ol"], stroke=1.5, a=a))

def _mouth(c, P, a, kind, lx, t):
    x = lx * 0.8; y = -72.6; ol = P["ol"]
    if kind == "talk":
        kind = "grin" if (int(t * 7) % 2) else "small"
    if kind == "smile":
        p = skia.Path(); p.moveTo(x - 2.7, y - 0.4); p.quadTo(x, y + 2.0, x + 2.7, y - 0.4)
        c.drawPath(p, _pp(P, ol, stroke=1.1, a=a))
    elif kind == "small":
        p = skia.Path(); p.moveTo(x - 1.5, y); p.quadTo(x, y + 1.0, x + 1.5, y)
        c.drawPath(p, _pp(P, ol, stroke=1.0, a=a))
    elif kind == "grin":
        p = skia.Path(); p.moveTo(x - 3.7, y - 0.9); p.lineTo(x + 3.7, y - 0.9)
        p.cubicTo(x + 3.4, y + 3.6, x - 3.4, y + 3.6, x - 3.7, y - 0.9); p.close()
        c.drawPath(p, _pp(P, P["mouth"], a=a))
        c.save(); c.clipPath(p, doAntiAlias=True)
        oval(c, x, y + 2.6, 2.4, 1.6, P["tongue"], a); c.drawRect(skia.Rect.MakeLTRB(x - 4, y - 1.2, x + 4, y + 0.3), _pp(P, "#ffffff", a=a))
        c.restore(); c.drawPath(p, _pp(P, ol, stroke=1.0, a=a))
    elif kind == "o":
        oval(c, x, y + 0.6, 1.8, 2.3, P["mouth"], a); c.drawOval(skia.Rect.MakeLTRB(x - 1.8, y - 1.7, x + 1.8, y + 2.9), _pp(P, ol, stroke=1.0, a=a))
    elif kind == "wobble":
        p = skia.Path(); p.moveTo(x - 3.0, y)
        for k in range(1, 7):
            p.lineTo(x - 3.0 + k, y + (0.7 if k % 2 else -0.5))
        c.drawPath(p, _pp(P, ol, stroke=1.0, a=a))
    elif kind == "frown":
        p = skia.Path(); p.moveTo(x - 2.4, y + 1.0); p.quadTo(x, y - 1.2, x + 2.4, y + 1.0)
        c.drawPath(p, _pp(P, ol, stroke=1.1, a=a))
    elif kind == "smirk":
        p = skia.Path(); p.moveTo(x - 2.4, y + 0.3); p.quadTo(x + 0.6, y + 1.3, x + 3.0, y - 1.3)
        c.drawPath(p, _pp(P, ol, stroke=1.1, a=a))

def _blink(t, seed=0.0):
    ph = (t + seed * 1.7) % 3.7
    return ph < 0.12


# ------------------------------------------------------------------ main entry points
def kai(c, x, y, h, t=0.0, pose="idle", expr="neutral", look=None, flip=False, P=None, a=1.0,
        phone_glow=1.0, blink=True, bob=True, seed=0.0, bust=False):
    """Draw Kai (or any palette P) with feet at (x, y), h pixels tall."""
    P = P or KAI
    E = EXPRS[expr]
    lx, ly = look if look is not None else E.get("look", (0.0, 0.0))
    if pose == "phone" and look is None:
        lx, ly = 0.0, 0.8
    s = h / 100.0
    c.save(); c.translate(x, y)
    br = 1.0 + (0.008 * math.sin(t * 2.4 + seed) if bob else 0.0)
    c.scale(s * (-1 if flip else 1), s * br)
    pz = POSES[pose]
    _hood(c, P, a)
    _head_back(c, P, a)
    if not bust:
        _legs(c, P, a)
    _torso(c, P, a, flip)
    if pz.get("phone"):
        _phone(c, P, a, phone_glow)
    if not pz.get("front"):
        _arms(c, P, a, pose, t)
    neck = skia.Rect.MakeLTRB(-3.4, -68.0, 3.4, -62.4)
    c.drawRect(neck, _pp(P, P["skin_sh"], a=a))
    face = _face(c, P, a)
    if P.get("face", True):                              # soft shadow under the fringe
        c.save(); c.clipPath(face, doAntiAlias=True); c.translate(0.6, 2.0)
        c.drawPath(_fringe_path(P), _pp(P, P["skin_sh"], a=a * 0.8)); c.restore()
    _headphones(c, P, a)
    if P.get("face", True):
        eyes = E["eyes"]
        if blink and eyes in ("open", "small", "wide") and _blink(t, seed):
            eyes = "closed"
        for sx in (-1, 1):
            _eye(c, P, a, sx * 6.2 + lx * 0.8, -79.6 + ly * 0.5, eyes, lx, ly)
        _mouth(c, P, a, E["mouth"], lx, t)
        if E.get("blush"):
            for sx in (-1, 1):
                oval(c, sx * 9.6 + lx * 0.6, -74.6, 3.1, 1.7, P["blush"], 0.55 * E["blush"] * a)
                for k in range(3):
                    line(c, sx * 9.6 - 1.6 + k * 1.3, -73.8, sx * 9.6 - 0.9 + k * 1.3, -75.4, "#ff4f7b", 0.45, 0.8 * E["blush"] * a)
    _hair_front(c, P, a, t)
    if P.get("face", True):
        _brows(c, P, a, E["brows"], lx)
        if E.get("sweat"):
            d = skia.Path(); d.moveTo(15.0, -95.5); d.cubicTo(17.5, -91.0, 18.0, -88.0, 15.6, -87.0)
            d.cubicTo(13.4, -88.0, 13.2, -91.0, 15.0, -95.5); d.close()
            c.drawPath(d, _pp(P, "#9fe3ff", a=a)); c.drawPath(d, _pp(P, P["ol"], stroke=0.8, a=a))
    if pz.get("front"):
        _arms(c, P, a, pose, t)
    c.restore()
    if E.get("hearts") and P.get("face", True):
        for k in range(3):
            ph = (t * 0.6 + k / 3.0) % 1.0
            hx = x + (k - 1) * 12 * s + math.sin(t * 2 + k) * 2 * s
            hy = y - (104 + ph * 24) * s
            hp = heart_path(hx, hy, 3.6 * s)
            c.drawPath(hp, paint("#ff3d6e", a * (1 - ph))); c.drawPath(hp, paint(P["ol"], a * (1 - ph), stroke=0.8 * s))


def crush(c, x, y, h, t=0.0, a=1.0, glow=1.0, flip=False, seed=1.3, hearts=True, pose="idle"):
    """'The Crush': a faceless glowing silhouette so every viewer can picture their own.
    Pass 1 is a blurred pink halo, pass 2 the solid silhouette (outline = fill, so no inner lines)."""
    s = h / 100.0
    halo = {k: ("#ff8fb1" if isinstance(v, str) and v.startswith("#") else v) for k, v in CRUSH.items()}
    halo.update(blur=4.0, olw=5.0)                       # blur is in figure units (it scales with h)
    solid = dict(CRUSH, ol=CRUSH["hoodie"], olw=1.6)
    kai(c, x, y, h, t, pose, "neutral", flip=flip, P=halo, a=a * glow * 0.85, blink=False, seed=seed)
    kai(c, x, y, h, t, pose, "neutral", flip=flip, P=solid, a=a, blink=False, seed=seed)
    s = h / 100.0
    for k in range(5):
        ph = (t * 0.35 + k / 5.0) % 1.0
        sparkle(c, x + math.sin(k * 2.1 + t) * 22 * s, y - (20 + 80 * ph) * s, (1.6 + k % 2) * s, "#ffd6e4", a * glow * math.sin(math.pi * ph))
    if hearts:
        hp = heart_path(x, y - (112 + math.sin(t * 2) * 2) * s, 5 * s)
        c.drawPath(hp, paint("#ff8fb1", a * glow)); c.drawPath(hp, paint("#ffffff", a * glow * 0.6, stroke=0.8 * s))
