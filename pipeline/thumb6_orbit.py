"""Batch 06 thumbnail (1280x720): b6_orbit. One big subject: the floating body in the station porthole."""
import sys, os, math
import numpy as np, skia
sys.path.insert(0, "/home/claude/proj")
from common2 import *
from PIL import Image
W, H = 1280, 720
OUT = "/home/claude/out/b6"

def title(c, txt, x, y, size, colr="#ffffff", maxw=700, align="l"):
    sz = fit(txt, maxw, size, 900)
    text(c, txt, x, y, sz, "#000000", 0.55, w=900, align=align, shadow=24)
    text(c, txt, x, y, sz, colr, 1, w=900, align=align, stroke=18, stroke_col="#0b1030")
    text(c, txt, x, y, sz, colr, 1, w=900, align=align)

def orbit():
    import scenes_b6_orbit as O
    arr = np.zeros((H, W, 4), np.uint8); c = skia.Surface(arr).getCanvas()
    c.drawImage(O.bg_img(W, H), 0, 0); stars(c, W, H, 0, 0.8, seed=14, twinkle=False)
    cx, cy, r = 905, 360, 300
    circle(c, cx, cy, r * 1.25, O.TEAL, 0.18, blur=60)
    def inner():
        O.globe_c(c, cx + r * 0.25, cy + r * 1.5, r * 0.95, rot=10, tilt=30, spin=0, glow=0.8, light=(0.2, 0.8, 0.6))
        O.body(c, cx - 10, cy + r * 0.4, r * 1.0, puff=0.8, legs=0.7, arms=0.6, spread=0.5, rot=-12, fluid=0.85, glow=1.0)
    O.porthole(c, cx, cy, r, 0.0, inner=inner, clock=0.83)
    O.station(c, 520, 105, 85, 0.0, rot=-12)
    title(c, "3,652", 50, 330, 190, "#ffffff", 600)
    title(c, "DAYS UP", 50, 510, 150, ACCENT, 560)
    os.makedirs(OUT, exist_ok=True)
    Image.fromarray(arr[:, :, :3].copy()).save(f"{OUT}/thumbnail_orbit.png", optimize=True); print("thumbnail_orbit.png")

if __name__ == "__main__":
    orbit()
