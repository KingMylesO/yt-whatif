"""Batch 04 thumbnail: What If You Shrank Down Inside a Computer Chip? (1280x720)."""
import sys, os
import numpy as np, skia
sys.path.insert(0, "/home/claude/proj")
from common2 import *
from scenes_b4_chip import Iso, explorer, _traces, BG_T, BG_B, CY, MG, CU, CU2
from PIL import Image

W, H = 1280, 720
OUT = "/home/claude/out/b4"
os.makedirs(OUT, exist_ok=True)

def title(c, txt, x, y, size, colr="#ffffff", maxw=760, align="l"):
    sz = fit(txt, maxw, size, 900)
    text(c, txt, x, y, sz, "#000000", 0.55, w=900, align=align, shadow=24)
    text(c, txt, x, y, sz, colr, 1, w=900, align=align, stroke=16, stroke_col="#0b1030")
    text(c, txt, x, y, sz, colr, 1, w=900, align=align)

arr = np.zeros((H, W, 4), np.uint8); c = skia.Surface(arr).getCanvas()
fill_bg(c, W, H, BG_T, BG_B)
c.drawImage(_traces(W, H)[0], 0, 0)
circle(c, 880, 360, 420, CY, 0.16, blur=120)
I = Iso(830, 215, 46)
for k in range(5):  # copper wiring overhead
    I.box(c, -1.5 + k * 2.8, -3, 6.2, 0.9, 13, 0.6, mix("#b8652e", CU, 0.6), top=CU2)
I.box(c, -1, -1, -0.8, 14, 10, 0.8, "#3a3f6e", top="#5e6f9e")
for fy in (0.8, 3.0, 5.2, 7.4):
    I.box(c, 0, fy, 0, 12, 0.7, 3.0, "#8a9bc4", top="#d4dcf8")
    for k in range(6):  # electrons streaming along the fin tops
        x, y = I.P(0.5 + k * 2.0, fy + 0.35, 3.1)
        circle(c, x, y, 13, CY, 0.4); circle(c, x, y, 5, "#ffffff", 1)
I.box(c, 4.6, -0.5, 0, 1.8, 9.6, 3.8, mix("#7a2a6a", MG, 0.55), a=0.92, top=mix(MG, "#ffffff", 0.3))
ex, ey = I.P(10.0, 3.0 + 0.35, 3.0)
circle(c, ex, ey - 20, 55, CY, 0.4, blur=22)
explorer(c, ex, ey, 40, 1.0, 0.0)
arrow(c, ex + 120, ey - 190, ex + 22, ey - 50, ACCENT, 14, 1.0, head=50)
title(c, "YOU ARE", 46, 170, 150, "#ffffff", 560)
title(c, "HERE", 46, 345, 190, ACCENT, 520)
Image.fromarray(arr[:, :, :3].copy()).save(f"{OUT}/thumbnail_shrink.png", optimize=True)
print("thumbnail_shrink.png")
