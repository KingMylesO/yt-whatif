import sys, numpy as np, skia
sys.path.insert(0, "/home/claude/proj")
from core import *
from PIL import Image

W, H = 1280, 720
arr = np.zeros((H, W, 4), np.uint8); s = skia.Surface(arr); c = s.getCanvas()
fill_bg(c, W, H, "#03061a", "#10173a"); stars(c, W, H, 0, 1, seed=3, density=0.8)
# empty Sun: dark disc with a dying orange rim
sx, sy, sr = 270, 250, 150
circle(c, sx, sy, sr * 1.6, "#ff8a3d", 0.22, blur=60)
circle(c, sx, sy, sr, "#000000")
circle(c, sx, sy, sr, "#ffb347", 0.95, stroke=7, dash=([28, 20], 0))
circle(c, sx, sy, sr + 14, "#ff8a3d", 0.35, stroke=3)
# Earth: lit half + frozen half
ex, ey, R = 905, 420, 305
c.drawLine(sx + sr, sy + 30, ex - R + 40, ey - 40, paint("#ffcf5a", 0.0))
earth(c, ex, ey, R, rot=-30, day=1.0, sun_dir=-1, night_side=False, glow=1.4)
c.save()
p = skia.Path(); p.moveTo(ex - 10, ey - R - 20)
import random
rng = random.Random(4); y = ey - R - 20
while y < ey + R + 20:
    y += 40; p.lineTo(ex + rng.uniform(-45, 25), y)
p.lineTo(ex + R + 60, ey + R + 40); p.lineTo(ex + R + 60, ey - R - 40); p.close()
c.clipPath(p, doAntiAlias=True)
cp = skia.Path(); cp.addCircle(ex, ey, R); c.clipPath(cp, doAntiAlias=True)
earth(c, ex, ey, R, rot=-30, day=0.9, night_side=False, ice=1.0, starlight=1, clouds=False)
circle(c, ex, ey, R, "#9fd3ff", 0.18)
for k in range(9):
    a0 = rng.uniform(-1.3, 1.3); r0 = rng.uniform(0.2, 0.9) * R
    x0, y0 = ex + 60 + math.cos(a0) * r0 * 0.6, ey + math.sin(a0) * r0
    line(c, x0, y0, x0 + rng.uniform(30, 90), y0 + rng.uniform(-50, 50), "#e8f4ff", 3, 0.7)
c.restore()
circle(c, ex, ey, R, "#bfe3ff", 0.6, stroke=4)
# text
txt = "8 MINUTES"
sz = 150
sz = fit(txt, 680, 140, 900); tx, ty = 410, 625
text(c, txt, tx, ty, sz, "#000000", 0.6, w=900, shadow=26)
text(c, txt, tx, ty, sz, ACCENT, 1, w=900, stroke=16, stroke_col="#0b1030")
text(c, txt, tx, ty, sz, ACCENT, 1, w=900)
Image.fromarray(arr[:, :, :3].copy()).save("/home/claude/out/thumbnail_sun_vanished.png")
print("ok")
