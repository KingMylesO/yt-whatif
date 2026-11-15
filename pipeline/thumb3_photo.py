"""Batch 03 thumbnail: What If Humans Could Photosynthesize? (1280x720)."""
import sys, math, random
import numpy as np, skia
sys.path.insert(0, "/home/claude/proj")
from common2 import *
from scenes_b3_photo import figure, leaf_rot, GSKIN, LEAF
from PIL import Image

W, H = 1280, 720
OUT = "/home/claude/out/b3"

def title(c, txt, x, y, size, colr="#ffffff", maxw=760, align="l"):
    sz = fit(txt, maxw, size, 900)
    text(c, txt, x, y, sz, "#000000", 0.55, w=900, align=align, shadow=24)
    text(c, txt, x, y, sz, colr, 1, w=900, align=align, stroke=14, stroke_col="#0b1030")
    text(c, txt, x, y, sz, colr, 1, w=900, align=align)

arr = np.zeros((H, W, 4), np.uint8); c = skia.Surface(arr).getCanvas()
fill_bg(c, W, H, "#0e3a14", "#05160a")
sx, sy = 930, 250
c.drawPaint(paint(shader=rad(sx, sy, 700, [(0, "#ffe27a", 0.9), (0.35, "#ffb300", 0.35), (1, "#ffb300", 0)])))
for i in range(24):
    an = math.radians(i * 15)
    c.drawPath(poly([(sx + math.cos(an - 0.05) * 120, sy + math.sin(an - 0.05) * 120), (sx + math.cos(an) * 900, sy + math.sin(an) * 900),
                     (sx + math.cos(an + 0.05) * 120, sy + math.sin(an + 0.05) * 120)]), paint("#fff1b0", 0.18))
rng = random.Random(4)
for k in range(22):
    leaf_rot(c, rng.uniform(560, 1280), rng.uniform(0, 720), rng.uniform(26, 50), rng.uniform(0, 360), mix(LEAF, "#b8f25c", rng.random() * 0.5), 0.85, vein=False)
figure(c, 920, 1260, 1250, GSKIN, 1, flat=0.15, leaves=1.0, arms=0.75)
# chloroplast texture inside the figure only
m = np.zeros((H, W, 4), np.uint8); mc = skia.Surface(m).getCanvas()
figure(mc, 920, 1260, 1250, "#ffffff", 1, arms=0.75)
pat = np.zeros((H, W, 4), np.uint8); pc = skia.Surface(pat).getCanvas()
from scenes_b3_photo import chloroplast
rr = random.Random(2)
for k in range(260):
    chloroplast(pc, rr.uniform(300, 1280), rr.uniform(0, 720), rr.uniform(12, 22), rr.uniform(0, 180), 1, "#2f8f3a")
pc.drawPaint(paint(shader=rad(820, 200, 700, [(0, "#ffffff", 0.0), (1, "#000000", 0.0)])))
al = (m[:, :, 3:4].astype(np.float32) / 255) * (pat[:, :, 3:4].astype(np.float32) / 255) * 0.55
arr[:, :, :3] = (arr[:, :, :3] * (1 - al) + pat[:, :, :3] * al).astype(np.uint8)
# shading: darken lower-left of the figure
sh = np.linspace(0, 1, H, dtype=np.float32)[:, None, None] * 0.35 * (m[:, :, 3:4].astype(np.float32) / 255)
arr[:, :, :3] = (arr[:, :, :3] * (1 - sh)).astype(np.uint8)
c = skia.Surface(arr).getCanvas()
# glow rim
title(c, "EAT", 60, 230, 210, "#ffffff", 520)
title(c, "SUNLIGHT?", 60, 430, 170, ACCENT, 620)
Image.fromarray(arr[:, :, :3].copy()).save(f"{OUT}/thumbnail_photo.png", optimize=True)
print("thumbnail_photo.png")
