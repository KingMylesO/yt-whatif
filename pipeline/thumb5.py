"""Batch 05 thumbnails (1280x720): moon, ice, microbes. Built from each video's own scene helpers."""
import sys, os, random
import numpy as np, skia
sys.path.insert(0, "/home/claude/proj")
from common2 import *
from PIL import Image
W, H = 1280, 720
OUT = "/home/claude/out/b5"

def title(c, txt, x, y, size, colr="#ffffff", maxw=700, align="l"):
    sz = fit(txt, maxw, size, 900)
    text(c, txt, x, y, sz, "#000000", 0.55, w=900, align=align, shadow=24)
    text(c, txt, x, y, sz, colr, 1, w=900, align=align, stroke=18, stroke_col="#0b1030")
    text(c, txt, x, y, sz, colr, 1, w=900, align=align)

def canvas():
    arr = np.zeros((H, W, 4), np.uint8); return arr, skia.Surface(arr).getCanvas()

def save(arr, fn):
    Image.fromarray(arr[:, :, :3].copy()).save(f"{OUT}/{fn}", optimize=True); print(fn)

def moon():
    import scenes_b5_moon as M
    arr, c = canvas(); c.drawImage(M.bg_img(W, H), 0, 0); stars(c, W, H, 0, 0.8, seed=12, twinkle=False)
    ex, ey, R = 880, 380, 300
    circle(c, ex, ey, R * 1.25, M.TIDE, 0.18, blur=60)
    M.tide_bulge(c, ex, ey, R, 0.0, 0.10, 0.0, a=0.9)
    M.earth(c, ex, ey, R, 40, tilt=18)
    # empty dashed Moon outline
    mx, my, mr = 250, 210, 110
    circle(c, mx, my, mr * 1.4, M.MBLUE, 0.20, blur=40)
    p = skia.Paint(Color=skia.Color4f.FromColor(skia.Color(230, 236, 248, 230)), Style=skia.Paint.kStroke_Style, StrokeWidth=8, AntiAlias=True,
                   PathEffect=skia.DashPathEffect.Make([28, 18], 0))
    c.drawCircle(mx, my, mr, p)
    title(c, "IT'S", 60, 470, 150, "#ffffff", 520)
    title(c, "GONE", 60, 640, 190, ACCENT, 560)
    save(arr, "thumbnail_moon.png")

def ice():
    import scenes_b5_ice as I
    arr, c = canvas(); c.drawImage(I.bg_img(W, H), 0, 0)
    gx, gy, R = 860, 380, 300
    circle(c, gx, gy, R * 1.2, "#5ee0ff", 0.16, blur=60)
    I.globe2(c, gx, gy, R, 300, tilt=18, melt=0.0)
    # rising water across the lower part of the frame
    I.water(c, 0, W, 560, H, 0.4, a=1.0, amp=10)
    # gauge
    I.gauge(c, 1215, 660, 7.6, 70, 70, 1.0, step=10, w=50, label_side="l", readout=None)
    title(c, "+70", 60, 330, 230, ACCENT, 560)
    title(c, "METERS", 60, 470, 130, "#ffffff", 560)
    save(arr, "thumbnail_ice.png")

def microbes():
    import scenes_b5_microbes as X
    arr, c = canvas(); c.drawImage(X.bg_img(W, H), 0, 0)
    cx, top, h = 930, 40, 650
    X.body(c, cx, top, h, colon=1.0, glow=1.2)
    X.swarm(c, 0.5, cx, top, h, n=320, grow=1.25)
    title(c, "STERILE", 60, 330, 170, "#ffffff", 620)
    title(c, "YOU?", 60, 520, 200, X.LIME, 560)
    save(arr, "thumbnail_microbes.png")

if __name__ == "__main__":
    for f in (sys.argv[1:] or ["moon", "ice", "microbes"]): globals()[f]()
