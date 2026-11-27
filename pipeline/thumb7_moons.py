"""Batch 07 thumbnail (1280x720) for b7_moons: the Moon and its peach twin about to collide over Earth's limb,
plum night look from the video. Built from the video's own helpers. Text: COLLISION COURSE (no title words)."""
import sys, os
import numpy as np, skia
sys.path.insert(0, "/home/claude/proj")
from common2 import *
from PIL import Image
import geo
import scenes_b7_moons as M
W, H = 1280, 720
OUT = "/home/claude/out/b7"

def title(c, txt, x, y, size, colr="#ffffff", maxw=700, align="l"):
    sz = fit(txt, maxw, size, 900)
    text(c, txt, x, y, sz, "#000000", 0.55, w=900, align=align, shadow=24)
    text(c, txt, x, y, sz, colr, 1, w=900, align=align, stroke=18, stroke_col="#0b1030")
    text(c, txt, x, y, sz, colr, 1, w=900, align=align)

def moons():
    os.makedirs(OUT, exist_ok=True)
    arr = np.zeros((H, W, 4), np.uint8); c = skia.Surface(arr).getCanvas()
    c.drawImage(M.bg_img(W, H), 0, 0); stars(c, W, H, 0, 0.9, seed=14, twinkle=False)
    # Earth's limb along the bottom
    R = 760
    img = geo.globe_img(R, 20, tilt=-20, light=(0.2, 0.75, 0.6), ambient=0.3)
    im = skia.Image.fromarray(img, colorType=skia.kRGBA_8888_ColorType, alphaType=skia.kPremul_AlphaType)
    ex, ey = 820, 720 + 560
    c.drawCircle(ex, ey, R * 1.03, paint(shader=rad(ex, ey, R * 1.03, [(0.95, "#6fb6ff", 0.0), (0.97, "#8fd0ff", 0.55), (1, "#6fb6ff", 0)])))
    c.drawImageRect(im, skia.Rect.MakeXYWH(ex - R, ey - R, 2 * R, 2 * R), skia.SamplingOptions(skia.FilterMode.kLinear), skia.Paint())
    # the two moons, nearly touching, with a spark between them
    mx, my, tx, ty, r = 760, 300, 1075, 250, 165
    M.moon_d(c, mx, my, r, "moon", frac=0.97, sun_ang=200, glow=1.2)
    M.moon_d(c, tx, ty, r, "twin", frac=0.97, sun_ang=200, glow=1.3)
    sx, sy = (mx + tx) / 2 + 8, (my + ty) / 2 - 6
    c.drawCircle(sx, sy, 70, paint(shader=rad(sx, sy, 70, [(0, "#ffffff", 1.0), (0.35, "#ffe2b0", 0.7), (1, "#ff9a5a", 0)])))
    for k in range(8):
        an = k * math.pi / 4 + 0.3
        line(c, sx, sy, sx + math.cos(an) * 85, sy + math.sin(an) * 85, "#fff4dc", 4, 0.8)
    # motion streaks
    for k in range(4):
        line(c, mx - r - 30 - k * 10, my - 60 + k * 40, mx - r - 140 - k * 25, my - 60 + k * 40 + 18, M.SILVER, 6, 0.35)
        line(c, tx + r + 20 + k * 6, ty - 70 + k * 40, tx + r + 120 + k * 20, ty - 70 + k * 40 - 16, M.PEACH, 6, 0.35)
    title(c, "COLLISION", 40, 470, 170, ACCENT, 620)
    title(c, "COURSE", 44, 620, 150, "#ffffff", 560)
    Image.fromarray(arr[:, :, :3].copy()).save(f"{OUT}/thumbnail_moons.png", optimize=True); print("thumbnail_moons.png")

if __name__ == "__main__":
    moons()
