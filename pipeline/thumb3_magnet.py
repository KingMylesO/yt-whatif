"""Batch 03 thumbnail: What If Earth's Magnetic Field Switched Off? (1280x720)."""
import sys, math, random
import numpy as np, skia
sys.path.insert(0, "/home/claude/proj")
from common2 import *
import geo
from scenes_b3_magnet import wind, dipole, CYAN
from PIL import Image

W, H = 1280, 720
OUT = "/home/claude/out/b3"
arr = np.zeros((H, W, 4), np.uint8); surf = skia.Surface(arr); c = surf.getCanvas()
fill_bg(c, W, H, "#03141c", "#0b2e3a")
stars(c, W, H, 0, 0.9, seed=8)
c.drawPaint(paint(shader=rad(-80, 360, 700, [(0, "#ffb347", 0.55), (0.5, "#ff6b35", 0.15), (1, "#ff6b35", 0)])))
gx, gy, R = 900, 380, 260
wind(c, 0.37, 1, -50, W + 60, 40, H - 40, n=90, hit=(gx, gy, R * 1.04), size=1.6, seed=9)
# broken shield shards
rng = random.Random(3)
for k in range(9):
    a0 = 110 + k * 16 + rng.uniform(-4, 4); sweep = rng.uniform(6, 11); rr = R * 1.45 + rng.uniform(-14, 30)
    p = skia.Path(); p.addArc(skia.Rect.MakeXYWH(gx - rr, gy - rr, 2 * rr, 2 * rr), a0, sweep)
    c.drawPath(p, paint(CYAN, 0.35, stroke=26, cap="butt")); c.drawPath(p, paint(CYAN, 0.95, stroke=8, cap="butt"))
geo.globe(c, gx, gy, R, rot=-30, tilt=18, glow=1.2)
circle(c, gx - R * 0.95, gy, R * 0.5, "#ffb06a", 0.3, blur=40)
def title(txt, x, y, size, colr, maxw):
    sz = fit(txt, maxw, size, 900)
    text(c, txt, x, y, sz, "#000000", 0.55, w=900, align="l", shadow=24)
    text(c, txt, x, y, sz, colr, 1, w=900, align="l", stroke=16, stroke_col="#0b1030")
    text(c, txt, x, y, sz, colr, 1, w=900, align="l")
title("SHIELD", 50, 250, 190, "#ffffff", 640)
title("DOWN", 50, 450, 230, ACCENT, 600)
Image.fromarray(arr[:, :, :3].copy()).save(f"{OUT}/thumbnail_magnet.png", optimize=True); print("thumbnail_magnet.png")
