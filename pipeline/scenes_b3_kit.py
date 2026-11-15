"""Batch 03 shared kit: palette-aware title, time card, end screen and Short end card.

Each topic module passes its own `bg(c, W, H, t, S)` and `motif(c, W, H, t, S, cx, cy, s)` plus a palette dict:
    pal = dict(accent="#..", chip="#..", glow="#..")
so every long-form gets its own look while sharing layout code.
"""
from common2 import *

def _two_lines(txt, big, W):
    if tw(txt, big, 900) <= W * 0.86 or " " not in txt: return [txt]
    ws = txt.split(" ")
    best = min(range(1, len(ws)), key=lambda k: max(tw(" ".join(ws[:k]), big, 900), tw(" ".join(ws[k:]), big, 900)))
    return [" ".join(ws[:best]), " ".join(ws[best:])]

def title(c, W, H, t, S, bg, motif, pal):
    u = S.u; o = S.opts
    bg(c, W, H, t, S)
    motif(c, W, H, t, S, W / 2, (0.36 if not S.P else 0.38) * H, 0.85 if not S.P else 0.62)
    c.drawRect(skia.Rect.MakeXYWH(0, 0.6 * H, W, 0.4 * H), paint(shader=lin(0, 0.6 * H, 0, H, [(0, "#000000", 0), (1, "#000000", 0.55)])))
    p1 = prog(t, 0.15, 0.4); p2 = prog(t, 0.6, 0.4)
    sz = fit(o["l1"], W * 0.9, 100 * u, 900)
    text(c, o["l1"], W / 2, 0.72 * H + (1 - eout(p1)) * 30 * u, sz, "#ffffff", p1, w=900, shadow=14, stroke=6 * u, stroke_col="#0b1030")
    sz2 = fit(o["l2"], W * 0.9, 125 * u, 900)
    text(c, o["l2"], W / 2, 0.72 * H + 130 * u + (1 - eout(p2)) * 30 * u, sz2, pal.get("title2", ACCENT), p2, w=900, shadow=14, stroke=6 * u, stroke_col="#0b1030")

def card(c, W, H, t, S, bg, pal):
    u = S.u; o = S.opts; txt = o["text"]; lab = o.get("label", "")
    bg(c, W, H, t, S)
    c.drawPaint(paint("#000000", 0.45))
    c.save(); z = 1 + 0.05 * t / S.dur; c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-W / 2, -H / 2)
    big = 190 * u; lines_ = _two_lines(txt, big, W)
    p = eout(prog(t, 0.0, 0.35))
    chip(c, lab, W / 2, H / 2 - (150 if len(lines_) == 1 else 245) * u, prog(t, 0.05, 0.4), 30 * u, bg=pal.get("chip", "#1b2250"))
    for k, ln in enumerate(lines_):
        sz = fit(ln, W * 0.86, big, 900)
        yy = H / 2 + (k - (len(lines_) - 1) / 2) * sz * 1.02 + (1 - p) * 40 * u
        text(c, ln, W / 2, yy, sz, "#ffffff" if k == 0 else pal["accent"], p, w=900, shadow=18)
    lw = W * 0.3 * eout(prog(t, 0.2, 0.6)); yb = H / 2 + (120 if len(lines_) == 1 else 220) * u
    line(c, W / 2 - lw / 2, yb, W / 2 + lw / 2, yb, pal["accent"], 8 * u)
    c.restore()

def end(c, W, H, t, S, bg, motif, pal):
    u = S.u; o = S.opts
    bg(c, W, H, t, S)
    c.saveLayerAlpha(None, 170)
    motif(c, W, H, t, S, W / 2, 0.66 * H, 0.7)
    c.restore()
    p = prog(t, 0.2, 0.5)
    sz = fit(o["q"], W * 0.9, 96 * u, 900)
    text(c, o["q"], W / 2, 0.18 * H, sz, pal["accent"], p, w=900, shadow=14, stroke=6 * u, stroke_col="#0b1030")
    text(c, "Tell me in the comments", W / 2, 0.29 * H, 44 * u, "#ffffff", prog(t, 0.6, 0.5), w=600, fam="Inter", shadow=8)

def end_short(c, W, H, t, S, bg, motif, pal):
    u = S.u; o = S.opts
    bg(c, W, H, t, S)
    motif(c, W, H, t, S, W / 2, 0.42 * H, 0.75)
    p = prog(t, 0.1, 0.4)
    sz = fit(o["top"], W * 0.9, 100 * u, 900)
    text(c, o["top"], W / 2, 0.21 * H, sz, "#ffffff", p, w=900, shadow=14, stroke=8 * u, stroke_col="#0b1030")
    chip(c, "FULL VIDEO ON THE CHANNEL", W / 2, 0.14 * H, vis(t, S.lt(0, 0.4)), 44 * u, bg=pal["accent"], fg="#0b1030", a=1)

def hook(c, W, H, t, S, y=0.2):
    """Shorts hook text (opts['hook']); same position as earlier batches."""
    o = S.opts
    if o.get("hook"):
        u = S.u; sz = fit(o["hook"], W * 0.9, 92 * u, 900)
        text(c, o["hook"], W / 2, y * H, sz, "#ffffff", eout(t / 0.25), w=900, stroke=10 * u, stroke_col="#0b1030")

def region(S):
    """Main content box (x0, y0, x1, y1). Shorts: 0.24H..0.58H (captions at 0.635H, badge 0.14H, hook 0.2H)."""
    W, H = S.W, S.H
    if S.P: return (0.04 * W, 0.25 * H, 0.96 * W, 0.58 * H)
    return (0.04 * W, 0.12 * H, 0.96 * W, 0.94 * H)

SCENES = {}
