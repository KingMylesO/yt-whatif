"""Batch 02 thumbnails (1280x720)."""
import sys, math, random
import numpy as np, skia
sys.path.insert(0, "/home/claude/proj")
from common2 import *
import geo
from scenes_ast import trex as _trex, IMPACT
from scenes_med import med_map, MED
from PIL import Image

W, H = 1280, 720
OUT = "/home/claude/out/batch2"

def new():
    arr = np.zeros((H, W, 4), np.uint8); s = skia.Surface(arr); return arr, s.getCanvas()

def save(arr, name):
    Image.fromarray(arr[:, :, :3].copy()).save(f"{OUT}/{name}", optimize=True); print(name)

def title(c, txt, x, y, size, colr="#ffffff", maxw=760, align="l"):
    sz = fit(txt, maxw, size, 900)
    text(c, txt, x, y, sz, "#000000", 0.55, w=900, align=align, shadow=24)
    text(c, txt, x, y, sz, colr, 1, w=900, align=align, stroke=14, stroke_col="#0b1030")
    text(c, txt, x, y, sz, colr, 1, w=900, align=align)

# ---------- 1. trees ----------
arr, c = new(); u = 1.0
forest_bg(c, W, H, 0, 1.6, dark=0.45, hy=0.42)
rect(c, 0, 0.62 * H, W, H, "#1e1712")
rng = random.Random(3)
cx, base = 800, 700
for k in range(140):
    row = rng.random() ** 0.8
    y = base - row * 560
    half = (1 - row) * 520 + 60
    x = cx + rng.uniform(-half, half)
    log(c, x, y, rng.uniform(170, 300), rng.uniform(16, 26), mix("#8a8378", "#5d564d", rng.random()), ang=rng.uniform(-25, 25), seed=k)
circle(c, 330, 640, 120, "#ffb347", 0.35, blur=50)
mushroom(c, 330, 680, 90, colr="#ff7a1a")
circle(c, 330, 600, 60, "#ffe58a", 0.25, blur=30)
title(c, "ZERO", 60, 150, 190, "#ffffff", 560)
title(c, "DECAY", 60, 330, 190, ACCENT, 600)
save(arr, "thumbnail_trees_zero_decay.png")

# ---------- 2. asteroid ----------
arr, c = new()
space_bg(c, W, H, 0, 1, seed=41)
gx, gy, R = 790, 470, 400
rot, tilt = -82, 22
geo.globe(c, gx, gy, R, rot=rot, tilt=tilt, glow=1.3)
ix, iy, _ = geo.globe_xy(*IMPACT, gx, gy, R, rot, tilt)
ax, ay, _ = geo.globe_xy(-40, 28, gx, gy, R, rot, tilt)
p = skia.Path(); p.moveTo(ix, iy); p.quadTo((ix + ax) / 2 + 20, min(iy, ay) - 120, ax, ay)
c.drawPath(p, paint("#ffffff", 0.95, stroke=7, dash=([22, 16], 0)))
circle(c, ax, ay, 26, "#4cd964"); circle(c, ax, ay, 26, "#ffffff", stroke=5)
xmark(c, ix, iy, 46, 1, colr="#ff2d2d")
asteroid(c, 330, 150, 46, 0, trail=1.6, ang=-38 + 180 + 5, glow=1.0)
# horizon with T. rex
c.drawPath(poly([(0, H), (0, 610), (260, 598), (520, 630), (640, H)]), paint("#1c2747"))
c.drawPath(poly([(0, 610), (260, 598), (520, 630)], close=False), paint("#ffb37a", 0.6, stroke=3))
_trex(c, 250, 604, 150, 0.3, "#020308", walk=False)
title(c, "30", 50, 230, 230, ACCENT, 360)
title(c, "SECONDS", 50, 400, 150, "#ffffff", 560)
save(arr, "thumbnail_asteroid_30_seconds.png")

# ---------- 3. Mediterranean ----------
arr, c = new()
fill_bg(c, W, H, "#081226", "#0f1f3a")
TB = (-13, 29.0, 37, 47.0)
rr = geo.map_rect(TB, 640, 360, width=1290)
med_map(c, rr, dry=0.042, u=1.4, bbox=TB)
gxp, gyp = geo.lonlat_xy(-5.6, 35.97, TB, rr)
c.save(); c.clipRect(skia.Rect.MakeXYWH(*rr))
rng = random.Random(7)
blobs = []
for k in range(160):
    f = k / 160
    x = gxp - 120 + f * 420; spread = 10 + max(0, x - gxp) * 0.45
    y = gyp + rng.uniform(-1, 1) * spread * 0.6 - max(0, x - gxp) * 0.12
    r = 14 + max(0, x - gxp) * 0.16 * rng.uniform(0.6, 1.1)
    blobs.append((x, y, r))
for (x, y, r) in blobs: circle(c, x, y, r + 6, "#e6f6ff", 0.95)
for (x, y, r) in blobs: circle(c, x, y, r, "#1f7fe8")
for k in range(60):
    x, y, r = blobs[rng.randrange(len(blobs))]
    line(c, x - r * 0.6, y, x + r * 0.6, y + rng.uniform(-4, 4), "#cfeeff", 3, 0.8)
c.restore()
circle(c, gxp + 40, gyp, 90, "#9fe0ff", 0.35, blur=30)
title(c, "IT HAPPENED", W / 2 + 120, 610, 150, "#ffffff", 900, align="c")
text(c, "HAPPENED", 0, 0, 1, "#000", 0)
save(arr, "thumbnail_mediterranean_it_happened.png")
