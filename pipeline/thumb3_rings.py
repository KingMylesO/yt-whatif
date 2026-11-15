"""Batch 03 thumbnail: What If Earth Had Rings? (1280x720)."""
import sys
import numpy as np, skia
sys.path.insert(0, "/home/claude/proj")
from common2 import *
import geo
from scenes_b3_rings import ring, ROCK
from PIL import Image

W, H = 1280, 720
OUT = "/home/claude/out/b3"

def title(c, txt, x, y, size, colr="#ffffff", maxw=760, align="l"):
    sz = fit(txt, maxw, size, 900)
    text(c, txt, x, y, sz, "#000000", 0.55, w=900, align=align, shadow=24)
    text(c, txt, x, y, sz, colr, 1, w=900, align=align, stroke=16, stroke_col="#0b1030")
    text(c, txt, x, y, sz, colr, 1, w=900, align=align)

arr = np.zeros((H, W, 4), np.uint8); c = skia.Surface(arr).getCanvas()
fill_bg(c, W, H, "#0d0a24", "#2a1a4a")
stars(c, W, H, 0, 1.0, seed=7, twinkle=False)
circle(c, 1180, 80, 60, "#ffd166", 0.25, blur=40)
gx, gy, R = 860, 400, 260
c.save(); c.translate(gx, gy); c.rotate(-16)
ring(c, 0, 0, R * 1.22, R * 2.5, 0.3, "back", "#e6d6b8", 1.0, n=8, gap=0.55)
geo.globe(c, 0, 0, R, rot=-20, tilt=20, glow=1.4)
ring(c, 0, 0, R * 1.22, R * 2.5, 0.3, "front", "#e6d6b8", 1.0, n=8, gap=0.55)
c.restore()
title(c, "WE HAD", 50, 190, 170, "#ffffff", 520)
title(c, "ONE?", 50, 370, 200, ACCENT, 480)
Image.fromarray(arr[:, :, :3].copy()).save(f"{OUT}/thumbnail_rings.png", optimize=True)
print("thumbnail_rings.png")
