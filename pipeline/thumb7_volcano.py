"""Batch 07 thumbnail (1280x720) for b7_volcano: the glowing Ring of Fire on a dark ash globe. Built from the video's own helpers."""
import sys, os
import numpy as np, skia
sys.path.insert(0, "/home/claude/proj")
from common2 import *
from PIL import Image
import scenes_b7_volcano as V
W, H = 1280, 720
OUT = "/home/claude/out/b7"

def title(c, txt, x, y, size, colr="#ffffff", maxw=700, align="l"):
    sz = fit(txt, maxw, size, 900)
    text(c, txt, x, y, sz, "#000000", 0.55, w=900, align=align, shadow=24)
    text(c, txt, x, y, sz, colr, 1, w=900, align=align, stroke=18, stroke_col="#0b1030")
    text(c, txt, x, y, sz, colr, 1, w=900, align=align)

def volcano():
    os.makedirs(OUT, exist_ok=True)
    arr = np.zeros((H, W, 4), np.uint8); c = skia.Surface(arr).getCanvas()
    c.drawImage(V.bg_img(W, H, "ash"), 0, 0); V.flakes(c, W, H, 3.0, 1.0)
    gx, gy, R = 900, 380, 310
    c.drawCircle(gx, gy, R * 1.45, paint(shader=rad(gx, gy, R * 1.45, [(0.6, V.MAGMA, 0.0), (0.72, V.MAGMA, 0.55), (1, V.EMBER, 0)])))
    V.vglobe(c, gx, gy, R, -172, 0.0, ign=1.0, ring_only=1.0)
    c.drawOval(skia.Rect.MakeLTRB(gx - R * 1.3, gy - R * 0.33, gx + R * 1.3, gy + R * 0.33), paint(V.LAVA, 0.5, stroke=4, dash=([18, 12], 0)))
    title(c, "1,350", 56, 290, 230, ACCENT, 560)
    title(c, "ERUPTIONS", 60, 470, 130, "#ffffff", 590)
    Image.fromarray(arr[:, :, :3].copy()).save(f"{OUT}/thumbnail_volcano.png", optimize=True); print("thumbnail_volcano.png")

if __name__ == "__main__":
    volcano()
