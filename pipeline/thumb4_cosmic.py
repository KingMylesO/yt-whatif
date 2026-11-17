"""Batch 04 thumbnail: What If a Cosmic Ray Flipped a Bit in Your Computer? (1280x720)."""
import sys, os
import numpy as np, skia
sys.path.insert(0, "/home/claude/proj")
from common2 import *
from scenes_b4_cosmic import bg_img, cell, strike, GREEN, RED, MAG, MONO
from PIL import Image

W, H = 1280, 720
OUT = "/home/claude/out/b4"
os.makedirs(OUT, exist_ok=True)

def title(c, txt, x, y, size, colr="#ffffff", maxw=760, align="l", fam="Inter Display", w=900):
    sz = fit(txt, maxw, size, w, fam)
    text(c, txt, x, y, sz, "#000000", 0.55, w=w, fam=fam, align=align, shadow=24)
    text(c, txt, x, y, sz, colr, 1, w=w, fam=fam, align=align, stroke=16, stroke_col="#0b1030")
    text(c, txt, x, y, sz, colr, 1, w=w, fam=fam, align=align)

arr = np.zeros((H, W, 4), np.uint8); c = skia.Surface(arr).getCanvas()
c.drawImage(bg_img(W, H), 0, 0)
stars(c, W, H, 0, 0.7, seed=44, twinkle=False)
# big memory grid on the right, one cell hit
rng = random.Random(6)
s = 104; gap = 18; cols, rows = 5, 5
x0 = 700; y0 = 60
hit = (2, 2)
for r in range(rows):
    for q in range(cols):
        x = x0 + q * (s + gap) + s / 2; y = y0 + r * (s * 1.15 + gap) + s * 0.575
        if (r, q) == hit: continue
        cell(c, x, y, s, rng.random() < 0.5, a=0.9)
hx = x0 + hit[1] * (s + gap) + s / 2; hy = y0 + hit[0] * (s * 1.15 + gap) + s * 0.575
circle(c, hx, hy, 190, MAG, 0.35, blur=70)
strike(c, hx, hy, 0.12, 0.0, ang=58, w=16, L=900, ring=False)
cell(c, hx, hy, s * 1.25, 0, glow=1.0, col=RED, fill=1.0)
circle(c, hx, hy, s * 1.1, "#ffffff", 0.8, stroke=6)
# text
title(c, "0 → 1", 60, 250, 210, GREEN, 560, fam=MONO, w=800)
title(c, "FROM", 60, 450, 150, "#ffffff", 560)
title(c, "SPACE", 60, 610, 170, ACCENT, 600)
Image.fromarray(arr[:, :, :3].copy()).save(f"{OUT}/thumbnail_cosmic.png", optimize=True)
print("thumbnail_cosmic.png")
