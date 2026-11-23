"""Batch 06 thumbnail (1280x720) for b6_mercury: scorched-glare Mercury, half fire, half frost. Built from the video's own helpers."""
import sys
import numpy as np, skia
sys.path.insert(0, "/home/claude/proj")
from common2 import *
from PIL import Image
import scenes_b6_mercury as M
W, H = 1280, 720
OUT = "/home/claude/out/b6"

def title(c, txt, x, y, size, colr="#ffffff", maxw=700, align="l"):
    sz = fit(txt, maxw, size, 900)
    text(c, txt, x, y, sz, "#000000", 0.55, w=900, align=align, shadow=24)
    text(c, txt, x, y, sz, colr, 1, w=900, align=align, stroke=18, stroke_col="#0b1030")
    text(c, txt, x, y, sz, colr, 1, w=900, align=align)

def mercury():
    import os; os.makedirs(OUT, exist_ok=True)
    arr = np.zeros((H, W, 4), np.uint8); c = skia.Surface(arr).getCanvas()
    c.drawImage(M.bg_img(W, H), 0, 0); stars(c, W, H, 0, 0.8, seed=12, twinkle=False)
    mx, my, R = 880, 400, 290
    M.glare_sun(c, 1235, 40, 70, 0.0, flare_to=(mx - 200, my + 250), flare=0.6)
    c.drawCircle(mx, my, R * 1.25, paint(shader=rad(mx, my, R * 1.25, [(0.75, M.EMBER, 0.0), (0.8, M.EMBER, 0.35), (1, M.EMBER, 0)])))
    M.merc(c, mx, my, R, sun_ang=-40, night=0.88)
    c.save(); p = skia.Path(); p.addCircle(mx, my, R); c.clipPath(p, doAntiAlias=True)
    # scorched day side / frosted night side
    c.drawCircle(mx, my, R, paint(shader=lin(mx + R * 0.77, my - R * 0.64, mx - R * 0.77, my + R * 0.64,
                                             [(0, "#ff7a2a", 0.45), (0.35, "#ff7a2a", 0.0), (0.62, M.ICE, 0.0), (1, M.ICE, 0.32)])))
    c.restore()
    arc = skia.Path(); arc.addArc(skia.Rect.MakeLTRB(mx - R, my - R, mx + R, my + R), 100, 120)
    c.drawPath(arc, paint(M.ICE, 0.8, stroke=7))
    title(c, "FRY", 60, 250, 200, ACCENT, 420)
    title(c, "OR", 64, 405, 110, "#ffffff", 300)
    title(c, "FREEZE?", 60, 555, 160, M.ICE, 560)
    Image.fromarray(arr[:, :, :3].copy()).save(f"{OUT}/thumbnail_mercury.png", optimize=True); print("thumbnail_mercury.png")

if __name__ == "__main__":
    mercury()
