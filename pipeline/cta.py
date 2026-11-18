"""Mid-video like-and-subscribe overlay (owner's rule, 2026-11-18).

render.Drawer.frame draws this on top of a scene whose opts has "cta": <line index>,
from that line's start - 0.1 s to its end + 0.6 s. Everything is code-drawn:
a red SUBSCRIBE pill, a thumbs-up and a bell. No platform logos or brand marks."""
import math
import skia
from core import *

RED, GREY, DARK = "#E5281F", "#3b3f4a", "#0b1030"
# layout in local units: [like 120] gap [pill 400] gap [bell 120]
ICON, PILL_W, PILL_H, GAP = 120, 400, 120, 26
TOTAL = ICON + GAP + PILL_W + GAP + ICON
CLICK = 0.8   # seconds after pop-in start when the pointer taps the button

def _thumb(c, s, fill, a):
    """thumbs-up in a box of half-size s, centred on 0,0. fill: 0 outline .. 1 accent."""
    u = s / 50.0
    cuff = skia.RRect.MakeRectXY(skia.Rect.MakeLTRB(-44 * u, -6 * u, -24 * u, 42 * u), 4 * u, 4 * u)
    p = skia.Path()
    p.moveTo(-16 * u, -4 * u)
    p.lineTo(-2 * u, -24 * u)
    p.cubicTo(2 * u, -30 * u, 2 * u, -40 * u, 2 * u, -44 * u)
    p.cubicTo(2 * u, -50 * u, 16 * u, -50 * u, 18 * u, -38 * u)
    p.cubicTo(19 * u, -30 * u, 16 * u, -20 * u, 12 * u, -12 * u)
    p.lineTo(36 * u, -12 * u)
    p.cubicTo(46 * u, -12 * u, 48 * u, -2 * u, 42 * u, 4 * u)
    p.cubicTo(47 * u, 10 * u, 44 * u, 18 * u, 38 * u, 20 * u)
    p.cubicTo(42 * u, 26 * u, 38 * u, 34 * u, 32 * u, 34 * u)
    p.cubicTo(34 * u, 40 * u, 30 * u, 44 * u, 24 * u, 44 * u)
    p.lineTo(-16 * u, 44 * u)
    p.close()
    if fill > 0:
        c.drawRRect(cuff, paint(ACCENT, a * fill)); c.drawPath(p, paint(ACCENT, a * fill))
    st = mix("#ffffff", ACCENT, fill)
    c.drawRRect(cuff, paint(st, a, stroke=5 * u)); c.drawPath(p, paint(st, a, stroke=5 * u))

def _bell(c, s, fill, a, swing=0.0):
    u = s / 50.0
    c.save(); c.translate(0, -40 * u); c.rotate(swing); c.translate(0, 40 * u)
    p = skia.Path()
    p.moveTo(-34 * u, 26 * u)
    p.cubicTo(-26 * u, 18 * u, -26 * u, 8 * u, -26 * u, -6 * u)
    p.cubicTo(-26 * u, -26 * u, -14 * u, -36 * u, 0, -36 * u)
    p.cubicTo(14 * u, -36 * u, 26 * u, -26 * u, 26 * u, -6 * u)
    p.cubicTo(26 * u, 8 * u, 26 * u, 18 * u, 34 * u, 26 * u)
    p.close()
    if fill > 0: c.drawPath(p, paint("#ffffff", a * fill))
    c.drawPath(p, paint("#ffffff", a, stroke=5 * u))
    circle(c, 0, -40 * u, 5 * u, "#ffffff", a)
    circle(c, 0, 36 * u, 8 * u, "#ffffff", a)
    c.restore()
    if fill > 0:  # little ring marks either side once subscribed
        for sg in (-1, 1):
            arc = skia.Path(); r = 46 * u
            arc.addArc(skia.Rect.MakeLTRB(-r, -r - 4 * u, r, r - 4 * u), (200 if sg < 0 else -20) - 20, 40)
            c.drawPath(arc, paint(ACCENT, a * fill, stroke=4 * u))

def _cursor(c, x, y, s, a):
    u = s / 50.0
    p = poly([(0, 0), (0, 46 * u), (11 * u, 35 * u), (19 * u, 54 * u), (27 * u, 50 * u), (19 * u, 32 * u), (34 * u, 32 * u)])
    c.save(); c.translate(x, y)
    c.drawPath(p, paint("#000000", a * 0.45, blur=6 * u))
    c.drawPath(p, paint("#ffffff", a)); c.drawPath(p, paint(DARK, a, stroke=4 * u))
    c.restore()

def _icon_disc(c, x, y, r, a):
    circle(c, x, y + r * 0.12, r, "#000000", a * 0.45, blur=r * 0.25)
    circle(c, x, y, r, DARK, a * 0.88)
    circle(c, x, y, r, "#ffffff", a * 0.35, stroke=r * 0.05)

def cta_box(W, H, short):
    """(centre x, centre y, scale) for the overlay; scale converts local units to pixels."""
    gw = (0.62 if short else 0.30) * W
    return W / 2, (0.75 if short else 0.82) * H, gw / TOTAL

def cta_overlay(c, W, H, t, dur, short):
    """t: seconds since the overlay started; dur: how long it stays up."""
    if t < 0 or t > dur: return
    pin = prog(t, 0, 0.3)
    a = eout(pin * 1.4) * (1 - ease(prog(t, dur - 0.4, 0.4)))
    if a <= 0.003: return
    cx, cy, k = cta_box(W, H, short)
    sc = k * lerp(0.55, 1.0, eback(pin))
    clk = ease(prog(t, CLICK, 0.12))                  # 0 before tap, 1 after
    press = 1 - 0.06 * math.sin(math.pi * prog(t, CLICK - 0.06, 0.18))
    like = eback(prog(t, CLICK + 0.12, 0.25))         # thumbs-up pops slightly after the tap
    swing = 18 * math.sin((t - CLICK - 0.2) * 22) * math.exp(-3.5 * max(0, t - CLICK - 0.2)) if t > CLICK + 0.2 else 0

    c.save(); c.translate(cx, cy); c.scale(sc, sc)
    x0 = -TOTAL / 2
    # like
    lx = x0 + ICON / 2
    _icon_disc(c, lx, 0, ICON / 2, a)
    c.save(); c.translate(lx, 0); z = 1 + 0.18 * math.sin(math.pi * clamp(like)) * (like < 1)
    c.scale(z, z); _thumb(c, ICON * 0.3, clamp(like), a); c.restore()
    # pill
    px = x0 + ICON + GAP; pcx = px + PILL_W / 2
    c.save(); c.translate(pcx, 0); c.scale(press, press)
    rrect(c, -PILL_W / 2, -PILL_H / 2 + 10, PILL_W, PILL_H, PILL_H / 2, "#000000", a * 0.5, blur=14)
    rrect(c, -PILL_W / 2, -PILL_H / 2, PILL_W, PILL_H, PILL_H / 2, mix(RED, GREY, clk), a)
    rrect(c, -PILL_W / 2, -PILL_H / 2, PILL_W, PILL_H, PILL_H / 2, "#ffffff", a * 0.25, stroke=3)
    lab = "SUBSCRIBED" if t >= CLICK + 0.06 else "SUBSCRIBE"
    sz = fit("SUBSCRIBED", PILL_W - 70, 54, 900)
    text(c, lab, 0, 0, sz, "#ffffff", a, w=900)
    c.restore()
    # bell
    bx = x0 + ICON + GAP + PILL_W + GAP + ICON / 2
    _icon_disc(c, bx, 0, ICON / 2, a)
    c.save(); c.translate(bx, 2); _bell(c, ICON * 0.28, clk, a, swing); c.restore()
    # pointer: glides in, taps, drifts off
    tgt = (pcx + PILL_W * 0.38, PILL_H * 0.30)   # lower-right of the pill, clear of the lettering
    st = (pcx + PILL_W * 0.62, PILL_H * 1.35)
    mv = ease(prog(t, 0.3, CLICK - 0.3)); out_ = ease(prog(t, CLICK + 0.35, 0.4))
    pxp = lerp(st[0], tgt[0], mv) + out_ * 40; pyp = lerp(st[1], tgt[1], mv) + out_ * 50
    pa = a * eout(prog(t, 0.25, 0.2)) * (1 - out_)
    if t >= CLICK - 0.02:  # tap ring
        q = prog(t, CLICK - 0.02, 0.45)
        if q < 1: circle(c, tgt[0], tgt[1], lerp(14, 70, eout(q)), "#ffffff", a * 0.9 * (1 - q), stroke=lerp(8, 2, q))
    if pa > 0: _cursor(c, pxp, pyp, 50 * (0.92 if CLICK - 0.06 < t < CLICK + 0.1 else 1.0), pa)
    c.restore()

def cta_window(sc):
    """(t0, t1) in scene time for a scene whose opts has "cta", else None."""
    i = sc.get("opts", {}).get("cta")
    if i is None or not sc.get("lines"): return None
    L = sc["lines"][int(i)]
    return max(0.0, L["start"] - 0.1), min(sc["dur"], L["end"] + 0.6)
