"""Batch 04 thumbnail: What If the Transistor Was Never Invented? (1280x720)."""
import sys
import numpy as np, skia
sys.path.insert(0, "/home/claude/proj")
from common2 import *
import scenes_b4_tubes as TB
from PIL import Image

W, H = 1280, 720
OUT = "/home/claude/out/b4"

def title(c, txt, x, y, size, colr="#ffffff", maxw=760, align="l"):
    sz = fit(txt, maxw, size, 900)
    text(c, txt, x, y, sz, "#000000", 0.55, w=900, align=align, shadow=24)
    text(c, txt, x, y, sz, colr, 1, w=900, align=align, stroke=16, stroke_col="#0b1030")
    text(c, txt, x, y, sz, colr, 1, w=900, align=align)

class _S: u = 720 / 1080; P = False; W = 1280; H = 720
arr = np.zeros((H, W, 4), np.uint8); c = skia.Surface(arr).getCanvas()
TB.bg_tube(c, W, H, 0.0, _S)
c.drawPaint(paint(shader=rad(900, 380, 520, [(0, "#ff7a1a", 0.35), (1, "#000000", 0.0)])))
# small tubes behind, one giant glowing tube in front
for x, s_ in ((640, 120), (1180, 130)):
    TB.tube(c, x, 700, s_, 0.4, 0.9, 0.85, seed=x)
circle(c, 900, 380, 300, "#ff9a3a", 0.35, blur=110)
TB.tube(c, 900, 700, 270, 0.7, 1.0, 1.0, seed=2)
title(c, "NO", 50, 230, 210, "#ffffff", 420)
title(c, "CHIPS?", 50, 430, 190, ACCENT, 560)
Image.fromarray(arr[:, :, :3].copy()).save(f"{OUT}/thumbnail_tubes.png", optimize=True)
print("thumbnail_tubes.png")
