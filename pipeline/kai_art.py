"""Character sheet, profile-picture options and style frames for Kai (the crush series).

    python3 kai_art.py OUT_DIR

Writes kai_character_sheet.png, profile_A_space.png, profile_B_crush.png, profile_C_bold.png
(800x800, circle-safe for YouTube) and style_short.png / style_long.png.
"""
import math, os, sys
import numpy as np
import skia
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import *
import kit3d as K
import mc

FAM = "Inter Display" if skia.FontMgr().matchFamily("Inter Display").count() else "Segoe UI"
FAM2 = "Inter" if skia.FontMgr().matchFamily("Inter").count() else "Segoe UI"
NAVY = "#0b1030"


def T(c, s, x, y, size, colr=NAVY, w=900, align="c", fam=None, a=1.0):
    return text(c, s, x, y, size, colr, a, w=w, fam=fam or FAM, align=align)


def save(surf, path):
    surf.makeImageSnapshot().save(path, skia.kPNG); print(path)


def bust(c, cx, cy, head_px, expr, pose="idle", P=None, t=0.3, look=None):
    """Draw Kai so the face (about 34 units tall) is head_px tall and centred on (cx, cy)."""
    h = head_px / 0.34
    mc.kai(c, cx, cy + 0.83 * h, h, t, pose, expr, look=look, P=P, blink=False, bob=False)


# ---------------------------------------------------------------- character sheet
def sheet(out):
    W, H = 2400, 1500
    s = skia.Surface(W, H); c = s.getCanvas()
    fill_bg(c, W, H, "#f6f1e7", "#ece4d6")
    rect(c, 0, 0, W, 150, NAVY)
    T(c, "KAI", 70, 75, 92, ACCENT, align="l")
    T(c, "Main character  ·  Myles AI stories  ·  crush series", 330, 78, 40, "#ffffff", w=600, align="l", fam=FAM2)
    T(c, "3D world · 2D character", W - 70, 78, 36, "#ffffff", w=600, align="r", fam=FAM2)

    # hero
    circle(c, 330, 840, 300, "#e2d8c6")
    mc.kai(c, 330, 1290, 1000, 0.4, "wave", "happy", bob=False, blink=False)
    T(c, "19  ·  curious  ·  always asking \"what if?\"", 330, 1380, 30, NAVY, w=600, fam=FAM2)
    T(c, "Hoodie \"?\" patch = the channel's what-if mark", 330, 1425, 26, "#4a4f6a", w=500, fam=FAM2)

    # expressions
    T(c, "EXPRESSIONS", 700, 210, 40, NAVY, align="l")
    ex = ["neutral", "happy", "blush", "nervous", "shocked", "lovestruck", "sad", "curious"]
    for i, e in enumerate(ex):
        cx, cy = 790 + (i % 4) * 230, 360 + (i // 4) * 290
        circle(c, cx, cy, 108, "#ffffff"); c.drawCircle(cx, cy, 108, paint(NAVY, 0.12, stroke=4))
        c.save(); c.clipPath(poly([(cx - 108, cy - 140), (cx + 108, cy - 140), (cx + 108, cy + 108), (cx - 108, cy + 108)]))
        bust(c, cx, cy + 6, 150, e)
        c.restore()
        T(c, e.upper(), cx, cy + 135, 24, NAVY, w=700, fam=FAM2)

    # poses
    T(c, "POSES", 700, 830, 40, NAVY, align="l")
    ps = ["idle", "phone", "think", "cheeks", "fist", "shrug", "point"]
    for i, p in enumerate(ps):
        x = 770 + i * 142
        mc.kai(c, x, 1290, 330, 0.7 + i * 0.5, p, "neutral" if p != "cheeks" else "blush", bob=False, blink=False)
        T(c, p.upper(), x, 1330, 22, NAVY, w=700, fam=FAM2)

    # the crush
    rrect(c, 1720, 190, 620, 560, 30, "#1b1440")
    T(c, "THE CRUSH", 2030, 232, 34, "#ffd6e4")
    mc.crush(c, 2030, 650, 370, t=0.5, hearts=False)
    T(c, "never shows a face: every viewer", 2030, 690, 22, "#ffd6e4", w=600, fam=FAM2)
    T(c, "pictures their own", 2030, 716, 22, "#ffd6e4", w=600, fam=FAM2)

    # palette
    T(c, "PALETTE", 1720, 830, 40, NAVY, align="l")
    pal = [("skin", mc.KAI["skin"]), ("hair", mc.KAI["hair"]), ("hoodie", mc.KAI["hoodie"]),
           ("accent", ACCENT), ("headphones", mc.KAI["phones"]), ("pants", mc.KAI["pants"]),
           ("outline", mc.KAI["ol"]), ("blush", mc.KAI["blush"])]
    for i, (name, hx) in enumerate(pal):
        x, y = 1720 + (i % 4) * 160, 890 + (i // 4) * 150
        rrect(c, x, y, 130, 80, 16, hx); rrect(c, x, y, 130, 80, 16, NAVY, 0.25, stroke=3)
        T(c, name, x + 65, y + 102, 20, NAVY, w=700, fam=FAM2)
        T(c, hx.upper(), x + 65, y + 126, 18, "#4a4f6a", w=500, fam=FAM2)
    T(c, "Rules: PG and wholesome · the Crush never has a face", 1720, 1215, 22, "#4a4f6a", w=500, align="l", fam=FAM2)
    T(c, "Thick navy outlines · flat 2D characters on low-poly 3D sets", 1720, 1247, 22, "#4a4f6a", w=500, align="l", fam=FAM2)
    save(s, os.path.join(out, "kai_character_sheet.png"))


# ---------------------------------------------------------------- profile pictures (800 x 800, circle-safe)
def ring_mesh(cx, cy, cz, r0, r1, colr, n=40, tilt=24):
    V, F = [], []
    for i in range(n):
        a = 2 * math.pi * i / n
        V += [(cx + r0 * math.cos(a), cy, cz + r0 * math.sin(a)), (cx + r1 * math.cos(a), cy, cz + r1 * math.sin(a))]
    for i in range(n):
        j = (i + 1) % n
        F.append((2 * i, 2 * i + 1, 2 * j + 1, 2 * j))
    return K.Mesh(V, F, colr, double=True, outline=0.0).tilted(tilt, (cx, cy, cz))


def profile_space(out):
    S = 800; s = skia.Surface(S, S); c = s.getCanvas()
    fill_bg(c, S, S, "#0b1030", "#24306b")
    stars(c, S, S, 0.0, 0.9, seed=7)
    cam = K.Cam((0, 0, 6.0), (0, 0, 0), 40)
    planet = K.sphere(1.25, 0.95, -1.5, 1.05, "#ff8fb1", 8, 14)
    planet.C = [mix("#ff8fb1", "#ffb38a", (k % 3) / 3) for k in range(len(planet.F))]
    K.render(c, S, S, cam, [planet, ring_mesh(1.25, 0.95, -1.5, 1.35, 1.85, ACCENT)], light=K.Light((-0.6, 0.7, 0.6), 0.55, 0.6))
    circle(c, 400, 400, 330, ACCENT, 0.10)
    bust(c, 400, 410, 330, "curious", "think")
    save(s, os.path.join(out, "profile_A_space.png"))


def profile_crush(out):
    S = 800; s = skia.Surface(S, S); c = s.getCanvas()
    fill_bg(c, S, S, "#ff9eb8", "#7a4bd6")
    cam = K.Cam((0, 0, 7.0), (0, 0, 0), 40)
    hearts = [K.heart(-1.9, 1.5, -1, 1.1, "#ff3d6e", turn=25), K.heart(2.0, 1.7, -2, 0.9, "#ffffff", turn=-30),
              K.heart(-2.3, -1.4, -2, 0.8, ACCENT, turn=40), K.heart(2.1, -1.2, -0.5, 0.7, "#ff3d6e", turn=-15)]
    K.render(c, S, S, cam, hearts, light=K.Light((-0.4, 0.7, 0.7), 0.6, 0.5))
    bust(c, 400, 410, 330, "blush", "cheeks")
    save(s, os.path.join(out, "profile_B_crush.png"))


def profile_bold(out):
    S = 800; s = skia.Surface(S, S); c = s.getCanvas()
    c.clear(col(ACCENT))
    cam = K.Cam((0, 0, 7.0), (0, 0, 0), 40)
    q = K.question_mark(-1.75, 0.95, -2.5, 2.5, NAVY, side="#2c3ca6", turn=22)
    K.render(c, S, S, cam, q, light=K.Light((-0.5, 0.6, 0.7), 0.9, 0.35))
    bust(c, 400, 410, 330, "happy", "wave")
    save(s, os.path.join(out, "profile_C_bold.png"))


# ---------------------------------------------------------------- style frames
def style_short(out):
    W, H = 1080, 1920; s = skia.Surface(W, H); c = s.getCanvas()
    fill_bg(c, W, H, "#0b1030", "#1b2350")
    cam = K.Cam((0.3, 1.7, 3.2), (-0.2, 0.2, -1.5), 60)          # Kai fills the 0.20H-0.58H band
    M, G = K.bedroom()
    M.append(K.heart(-0.6, 1.95, -0.6, 0.38, "#ff3d6e", turn=20))
    K.render(c, W, H, cam, M); K.glow_points(c, W, H, cam, G)
    x, y, h = K.anchor(cam, W, H, (-0.15, 0, -0.9), 1.75)
    c.drawOval(skia.Rect.MakeLTRB(x - h * 0.16, y - h * 0.025, x + h * 0.16, y + h * 0.025), paint("#000000", 0.25, blur=8))
    mc.kai(c, x, y, h, 0.4, "phone", "lovestruck", blink=False)
    chip(c, "THE CRUSH FILES", W / 2, 0.14 * H, 1.0, 52 * W / 1080, bg=ACCENT, fg=NAVY, a=1)
    cap = "WHEN YOUR CRUSH TEXTS BACK"
    sz = fit(cap, W * 0.86, 84, 900, FAM)
    text(c, cap, W / 2, 0.635 * H, sz, "#ffffff", 1, w=900, fam=FAM, stroke=14, stroke_col=NAVY)
    text(c, cap, W / 2, 0.635 * H, sz, "#ffffff", 1, w=900, fam=FAM)
    save(s, os.path.join(out, "style_short.png"))


def style_long(out):
    W, H = 1920, 1080; s = skia.Surface(W, H); c = s.getCanvas()
    fill_bg(c, W, H, "#f3ead8", "#d9cfe8")
    cam = K.Cam((0.6, 1.5, 3.8), (0.0, 1.1, -6), 55)
    K.render(c, W, H, cam, K.hallway(), fog=("#f3ead8", 4, 16, 0.5))
    for p, who in (((0.35, 0, -4.5), "crush"), ((-0.55, 0, 1.6), "kai")):
        x, y, h = K.anchor(cam, W, H, p, 1.75)
        c.drawOval(skia.Rect.MakeLTRB(x - h * 0.16, y - h * 0.025, x + h * 0.16, y + h * 0.025), paint("#000000", 0.2, blur=8))
        if who == "kai":
            mc.kai(c, x, y, h, 0.4, "cheeks", "nervous", blink=False)
        else:
            mc.crush(c, x, y, h, 0.4, flip=True)
    chip(c, "Your heart rate: 72 → 110 bpm", 1420, 160, 1.0, 40, bg=NAVY, fg="#ffffff", dot="#ff3d6e")
    save(s, os.path.join(out, "style_long.png"))


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(out, exist_ok=True)
    for fn in (sheet, profile_space, profile_crush, profile_bold, style_short, style_long):
        fn(out)
