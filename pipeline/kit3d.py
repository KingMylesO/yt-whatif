"""Low-poly 3D sets for the "3D world, 2D characters" style (the crush series; see STYLE.md).

World: y is up, units are metres. A Mesh holds vertices (N, 3), faces (tuples of vertex indices,
counter-clockwise seen from outside) and one colour per face. render() projects through a
pinhole Cam, clips faces at the near plane, culls back faces and paints far to near: layer 0
(room shell: floor, walls, ceiling), then layer 1 (decals lying on the shell: windows, posters,
rugs), then layer 2 (objects), sorted object by object by distance minus `bias` (give a thing
resting on another a positive bias so it's painted after it). Each face gets flat Lambert
shading, a little depth fog and an optional thin outline, so the sets read as toon-ish 3D next
to the flat 2D characters.

anchor() gives the screen point and pixel height for planting a 2D character (mc.py) at a world
position, so characters sit on the 3D floor with the right size.
"""
import math
import numpy as np
import skia
from core import *

OUTLINE = "#0b1030"


# ---------------------------------------------------------------- camera
class Cam:
    def __init__(self, pos, target, fov=50.0, near=0.05):
        self.pos = np.array(pos, float); self.target = np.array(target, float)
        self.fov, self.near = fov, near
        f = self.target - self.pos; self.f = f / np.linalg.norm(f)
        r = np.cross(self.f, (0.0, 1.0, 0.0)); self.r = r / np.linalg.norm(r)
        self.u = np.cross(self.r, self.f)

    def to_cam(self, P):
        rel = np.asarray(P, float) - self.pos
        return np.stack([rel @ self.r, rel @ self.u, rel @ self.f], axis=-1)

    def focal(self, H): return (H / 2) / math.tan(math.radians(self.fov) / 2)

    def project(self, Pc, W, H):
        """camera-space points (N, 3) with z > 0 -> screen (N, 2)."""
        f = self.focal(H)
        return np.stack([W / 2 + Pc[:, 0] * f / Pc[:, 2], H / 2 - Pc[:, 1] * f / Pc[:, 2]], axis=-1)


def orbit(target, dist, yaw, pitch, fov=50.0):
    """Camera looking at target from dist metres, yaw/pitch in degrees (yaw 0 = from +z)."""
    y, p = math.radians(yaw), math.radians(pitch)
    off = (dist * math.cos(p) * math.sin(y), dist * math.sin(p), dist * math.cos(p) * math.cos(y))
    return Cam(np.add(target, off), target, fov)


def anchor(cam, W, H, p, height=1.7):
    """Screen x, y of world point p and the pixel height of a figure `height` m tall standing there."""
    pc = cam.to_cam(np.array([p, np.add(p, (0, height, 0))], float))
    if pc[0, 2] <= cam.near or pc[1, 2] <= cam.near:
        return None
    s = cam.project(pc, W, H)
    return float(s[0, 0]), float(s[0, 1]), float(s[0, 1] - s[1, 1])


# ---------------------------------------------------------------- meshes
class Mesh:
    def __init__(self, V, F, colors, layer=2, outline=1.0, double=False, glow=None, bias=0.0):
        self.V = np.asarray(V, float); self.F = [tuple(f) for f in F]
        self.C = colors if isinstance(colors, list) else [colors] * len(self.F)
        self.layer, self.outline, self.double, self.glow, self.bias = layer, outline, double, glow, bias

    def _copy(self, V):
        return Mesh(V, self.F, self.C, self.layer, self.outline, self.double, self.glow, self.bias)

    def biased(self, b):
        m = self._copy(self.V); m.bias = b; return m

    def moved(self, dx=0.0, dy=0.0, dz=0.0):
        return self._copy(self.V + (dx, dy, dz))

    def turned(self, deg, about=(0.0, 0.0, 0.0)):
        """Rotate around a vertical axis through `about`."""
        a = math.radians(deg); ca, sa = math.cos(a), math.sin(a)
        V = self.V - about
        V = np.stack([V[:, 0] * ca + V[:, 2] * sa, V[:, 1], -V[:, 0] * sa + V[:, 2] * ca], axis=-1) + about
        return self._copy(V)

    def tilted(self, deg, about=(0.0, 0.0, 0.0)):
        """Rotate around the x axis through `about` (positive tips +y toward +z)."""
        a = math.radians(deg); ca, sa = math.cos(a), math.sin(a)
        V = self.V - about
        V = np.stack([V[:, 0], V[:, 1] * ca - V[:, 2] * sa, V[:, 1] * sa + V[:, 2] * ca], axis=-1) + about
        return self._copy(V)

    def scaled(self, s, about=(0.0, 0.0, 0.0)):
        return self._copy((self.V - about) * s + about)


def box(x0, y0, z0, x1, y1, z1, color, top=None, layer=2, outline=1.0, bias=0.0):
    """Axis-aligned box from corner (x0, y0, z0) to (x1, y1, z1)."""
    V = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
         (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    F = [(4, 5, 6, 7), (1, 0, 3, 2), (0, 4, 7, 3), (5, 1, 2, 6), (3, 7, 6, 2), (0, 1, 5, 4)]
    C = [color] * 4 + [top or color, color]
    return Mesh(V, F, C, layer, outline, bias=bias)


def quad(p0, p1, p2, p3, color, layer=0, outline=0.0, double=False, glow=None):
    """One flat face; points counter-clockwise as seen from the side that should show."""
    return Mesh([p0, p1, p2, p3], [(0, 1, 2, 3)], color, layer, outline, double, glow)


def cylinder(cx, y0, cz, r, h, color, n=14, top=None, layer=2, outline=1.0, r_top=None, bias=0.0):
    r_top = r if r_top is None else r_top
    V = []
    for i in range(n):
        a = 2 * math.pi * i / n
        V.append((cx + r * math.cos(a), y0, cz + r * math.sin(a)))
    for i in range(n):
        a = 2 * math.pi * i / n
        V.append((cx + r_top * math.cos(a), y0 + h, cz + r_top * math.sin(a)))
    F = [(i, (i + 1) % n, n + (i + 1) % n, n + i)[::-1] for i in range(n)]
    C = [color] * n
    if r_top > 0.001:
        F.append(tuple(range(n, 2 * n))[::-1]); C.append(top or color)
    F.append(tuple(range(n))); C.append(color)
    return Mesh(V, F, C, layer, outline, bias=bias)


def sphere(cx, cy, cz, r, color, rings=6, segs=10, layer=2, outline=0.0, bias=0.0):
    V = [(cx, cy + r, cz)]
    for i in range(1, rings):
        ph = math.pi * i / rings
        for j in range(segs):
            th = 2 * math.pi * j / segs
            V.append((cx + r * math.sin(ph) * math.cos(th), cy + r * math.cos(ph), cz + r * math.sin(ph) * math.sin(th)))
    V.append((cx, cy - r, cz)); bot = len(V) - 1
    F = []
    ring = lambda i, j: 1 + (i - 1) * segs + j % segs
    for j in range(segs):
        F.append((0, ring(1, j + 1), ring(1, j)))
    for i in range(1, rings - 1):
        for j in range(segs):
            F.append((ring(i, j), ring(i, j + 1), ring(i + 1, j + 1), ring(i + 1, j)))
    for j in range(segs):
        F.append((bot, ring(rings - 1, j), ring(rings - 1, j + 1)))
    return Mesh(V, F, color, layer, outline, bias=bias)


def _ear_clip(pts):
    """Triangulate a simple polygon given counter-clockwise in 2D."""
    idx = list(range(len(pts))); tris = []
    cross = lambda a, b, c: (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    def inside(p, a, b, c):
        return cross(a, b, p) >= 0 and cross(b, c, p) >= 0 and cross(c, a, p) >= 0
    guard = 0
    while len(idx) > 3 and guard < 10000:
        guard += 1
        for k in range(len(idx)):
            i0, i1, i2 = idx[k - 1], idx[k], idx[(k + 1) % len(idx)]
            a, b, c = pts[i0], pts[i1], pts[i2]
            if cross(a, b, c) <= 1e-9:
                continue
            if any(inside(pts[j], a, b, c) for j in idx if j not in (i0, i1, i2)):
                continue
            tris.append((i0, i1, i2)); idx.pop(k); break
        else:
            break
    if len(idx) == 3:
        tris.append(tuple(idx))
    return tris


def extrude(outline2d, depth, color, side=None, layer=2, outline=1.0):
    """Prism from a 2D outline in the x-y plane (counter-clockwise), centred on z = 0."""
    pts = list(outline2d); n = len(pts)
    area = sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n))
    if area < 0:
        pts = pts[::-1]
    V = [(x, y, depth / 2) for x, y in pts] + [(x, y, -depth / 2) for x, y in pts]
    tris = _ear_clip(pts)
    F, C = [], []
    for a, b, c in tris:
        F.append((a, b, c)); C.append(color)                      # front (+z)
        F.append((n + c, n + b, n + a)); C.append(color)          # back (-z)
    for i in range(n):
        j = (i + 1) % n
        F.append((i, n + i, n + j, j)); C.append(side or color)
    return Mesh(V, F, C, layer, outline)


def heart(cx, cy, cz, size, color, depth=None, side=None, turn=0.0, layer=2, outline=0.0):
    pts = []
    for k in range(40):
        t = 2 * math.pi * k / 40
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((x * size / 32, y * size / 32))
    m = extrude(pts, depth if depth is not None else size * 0.35, color, side or mix(color, OUTLINE, 0.25), layer, outline)
    return m.turned(turn).moved(cx, cy, cz)


def ribbon(centerline, width):
    """Closed 2D outline of a thick stroke along a polyline (for extruding letters and marks)."""
    pts = np.asarray(centerline, float); L, R = [], []
    for i in range(len(pts)):
        a, b = pts[max(i - 1, 0)], pts[min(i + 1, len(pts) - 1)]
        d = b - a; d = d / (np.linalg.norm(d) or 1.0); n = np.array([-d[1], d[0]]) * width / 2
        L.append(tuple(pts[i] + n)); R.append(tuple(pts[i] - n))
    return L + R[::-1]


def question_mark(cx, cy, cz, size, color, side=None, depth=0.35, turn=0.0):
    """The channel's chunky 3D "?" (size = total height in metres). Returns a list of meshes."""
    k = size / 1.9
    arc = [(0.56 * math.cos(a), 0.62 + 0.56 * math.sin(a)) for a in np.linspace(math.radians(195), math.radians(-35), 26)]
    tail = [(0.46 - 0.46 * t, 0.30 - 0.38 * t + 0.08 * math.sin(math.pi * t)) for t in np.linspace(0.12, 1.0, 6)]
    stem = [(0.0, -0.14), (0.0, -0.36)]
    line_ = [(x * k, y * k) for x, y in arc + tail + stem]
    side = side or mix(color, "#ffffff", 0.25)
    body = extrude(ribbon(line_, 0.34 * k), depth * k, color, side, outline=0.0)
    dot = sphere(0.0, -0.74 * k, 0.0, 0.2 * k, color, 5, 10)
    return [m.turned(turn).moved(cx, cy, cz) for m in (body, dot)]


# ---------------------------------------------------------------- render
class Light:
    def __init__(self, direction=(-0.45, 0.8, 0.55), ambient=0.58, diffuse=0.5, tint="#ffffff"):
        d = np.array(direction, float); self.d = d / np.linalg.norm(d)
        self.ambient, self.diffuse, self.tint = ambient, diffuse, tint


def _clip_near(P, near):
    out = []
    for i in range(len(P)):
        a, b = P[i], P[(i + 1) % len(P)]
        ia, ib = a[2] >= near, b[2] >= near
        if ia:
            out.append(a)
        if ia != ib:
            t = (near - a[2]) / (b[2] - a[2]); out.append(a + (b - a) * t)
    return np.array(out) if len(out) >= 3 else None


def render(c, W, H, cam, meshes, light=None, fog=("#10142e", 6.0, 22.0, 0.0), outline_px=1.4, a=1.0):
    """Draw meshes. fog = (colour, start m, end m, strength 0..1)."""
    light = light or Light()
    groups = []
    for m in meshes:
        faces = []
        Vc = cam.to_cam(m.V)
        for fi, f in enumerate(m.F):
            P = m.V[list(f)]
            n = np.cross(P[1] - P[0], P[2] - P[0]); ln = np.linalg.norm(n)
            if ln < 1e-12:
                continue
            n = n / ln
            centre = P.mean(axis=0)
            if not m.double and np.dot(n, cam.pos - centre) <= 0:
                continue
            Pc = _clip_near(Vc[list(f)], cam.near)
            if Pc is None:
                continue
            if m.double and np.dot(n, cam.pos - centre) < 0:
                n = -n
            depth = float(np.linalg.norm(centre - cam.pos))
            faces.append((-depth, Pc, n, m.C[fi], depth))
        if faces:
            faces.sort(key=lambda x: x[0])
            key = float(np.linalg.norm(m.V.mean(axis=0) - cam.pos)) - m.bias
            if m.layer < 2:          # shell and decals: sort face by face
                groups += [((m.layer, f[0] + m.bias), m, [f]) for f in faces]
            else:
                groups.append(((m.layer, -key), m, faces))
    groups.sort(key=lambda g: g[0])
    for _, m, faces in groups:
        for _, Pc, n, colr, depth in faces:
            _face(c, W, H, cam, m, Pc, n, colr, depth, light, fog, outline_px, a)


def _face(c, W, H, cam, m, Pc, n, colr, depth, light, fog, outline_px, a):
    S = cam.project(Pc, W, H)
    if m.glow is not None:
        cc = rgb(colr)
    else:
        shade = light.ambient + light.diffuse * max(0.0, float(np.dot(n, light.d)))
        base, tint = rgb(colr), rgb(light.tint)
        cc = tuple(int(clamp(base[i] * shade * tint[i] / 255 / 255) * 255) for i in range(3))
    fcol, f0, f1, fk = fog
    if fk > 0:
        cc = mix(cc, fcol, fk * clamp((depth - f0) / max(f1 - f0, 1e-6)))
    path = poly([(float(x), float(y)) for x, y in S])
    c.drawPath(path, paint(cc, a))
    c.drawPath(path, paint(cc, a, stroke=0.9))          # closes anti-aliasing seams between faces
    if m.glow is not None:
        c.drawPath(path, paint(m.glow, 0.5 * a, blur=6))
    if m.outline > 0 and outline_px > 0:
        c.drawPath(path, paint(mix(cc, OUTLINE, 0.55), 0.85 * a, stroke=outline_px * m.outline))


class Cache:
    """Renders a static camera's set once and reuses the image (camera key -> skia.Image)."""
    def __init__(self): self.store = {}
    def draw(self, c, W, H, key, fn):
        img = self.store.get((key, W, H))
        if img is None:
            surf = skia.Surface(W, H); fn(surf.getCanvas()); img = surf.makeImageSnapshot()
            self.store[(key, W, H)] = img
        c.drawImage(img, 0, 0)

CACHE = Cache()


# ---------------------------------------------------------------- sets
def bedroom(night=1.0, wall="#4a4f8f", floor="#7a5a48", bed="#e96f8f", accent=ACCENT):
    """A small bedroom: back wall with window, side wall, floor, bed, desk, lamp, shelf, rug.
    Floor spans x -3..3, z -2.5..2.5; the back wall is at z = -2.5. Returns (meshes, glows),
    glows = list of (world point, radius m, colour) for lamp and window light."""
    wall_l = mix(wall, "#0b1030", 0.15 * night)
    M = [
        quad((-3, 0, 2.5), (3, 0, 2.5), (3, 0, -2.5), (-3, 0, -2.5), floor, layer=0),
        quad((-3, 0, -2.5), (3, 0, -2.5), (3, 2.8, -2.5), (-3, 2.8, -2.5), wall, layer=0),
        quad((-3, 0, 2.5), (-3, 0, -2.5), (-3, 2.8, -2.5), (-3, 2.8, 2.5), wall_l, layer=0),
        quad((3, 0, -2.5), (3, 0, 2.5), (3, 2.8, 2.5), (3, 2.8, -2.5), wall_l, layer=0),
        quad((-3, 2.8, -2.5), (3, 2.8, -2.5), (3, 2.8, 2.5), (-3, 2.8, 2.5), mix(wall, "#000000", 0.35), layer=0),
        # skirting and rug
        box(-3, 0, -2.5, 3, 0.12, -2.42, mix(wall, "#ffffff", 0.25), layer=1, outline=0.6),
        Mesh([(-1.6, 0.012, 0.2), (0.4, 0.012, 0.2), (0.4, 0.012, -1.2), (-1.6, 0.012, -1.2)],
             [(0, 1, 2, 3)], mix(accent, "#ff8fb1", 0.4), layer=1, outline=0.5),
    ]
    # window (glowing night sky) with frame
    sky = mix("#7fb7ff", "#1b2a6b", night)
    M.append(quad((0.6, 1.1, -2.49), (2.2, 1.1, -2.49), (2.2, 2.3, -2.49), (0.6, 2.3, -2.49), sky, layer=1, glow=mix(sky, "#ffffff", 0.2)))
    M.append(sphere(1.85, 2.0, -2.495, 0.13, "#fff4c8", 4, 10, layer=1).scaled(1.0))
    for x0, y0, x1, y1 in ((0.55, 1.05, 2.25, 1.12), (0.55, 2.28, 2.25, 2.35), (0.55, 1.05, 0.62, 2.35),
                           (2.18, 1.05, 2.25, 2.35), (1.37, 1.1, 1.43, 2.3)):
        M.append(box(x0, y0, -2.5, x1, y1, -2.44, "#f2efe6", layer=1, outline=0.6))
    # posters
    M.append(quad((-2.4, 1.3, -2.49), (-1.5, 1.3, -2.49), (-1.5, 2.3, -2.49), (-2.4, 2.3, -2.49), accent, layer=1, outline=0.8))
    M.append(quad((-1.25, 1.55, -2.49), (-0.55, 1.55, -2.49), (-0.55, 2.2, -2.49), (-1.25, 2.2, -2.49), "#5fd3c4", layer=1, outline=0.8))
    # bed against the left wall
    M += [box(-3, 0, -2.5, -1.5, 0.45, 0.0, "#6b4a3a"),
          box(-2.95, 0.45, -2.45, -1.55, 0.62, -0.05, "#f4f1ea", bias=0.2),
          box(-2.97, 0.6, -1.7, -1.53, 0.7, -0.03, bed, top=mix(bed, "#ffffff", 0.15), bias=0.4),
          box(-2.8, 0.62, -2.4, -1.7, 0.8, -1.95, "#ffffff", bias=0.45),
          box(-3, 0.0, -2.5, -1.5, 1.05, -2.38, "#6b4a3a")]
    # desk, chair, lamp, laptop on the right
    M += [box(1.2, 0.72, -2.45, 2.8, 0.8, -1.6, "#c8996b"),
          box(1.25, 0, -2.4, 1.33, 0.72, -1.65, "#a57b55"), box(2.67, 0, -2.4, 2.75, 0.72, -1.65, "#a57b55"),
          box(1.6, 0.8, -2.25, 2.15, 0.82, -1.85, "#2b2f45", bias=0.3),
          box(1.6, 0.82, -2.27, 2.15, 1.15, -2.22, "#2b2f45", bias=0.3).tilted(-12, (1.9, 0.82, -2.25)),
          box(1.64, 0.85, -2.24, 2.11, 1.12, -2.225, "#7fd8ff", bias=0.35).tilted(-12, (1.9, 0.82, -2.25)),
          cylinder(2.5, 0.8, -2.2, 0.09, 0.03, "#2b2f45", bias=0.3), cylinder(2.5, 0.83, -2.2, 0.02, 0.38, "#2b2f45", bias=0.3),
          cylinder(2.5, 1.15, -2.2, 0.16, 0.14, accent, r_top=0.07, bias=0.3),
          box(2.3, 0.0, -1.25, 2.8, 0.45, -0.75, "#3d4a8a"), box(2.7, 0.45, -1.25, 2.8, 1.0, -0.75, "#3d4a8a", bias=0.1)]
    # shelf with books + plant
    M.append(box(-0.9, 1.15, -2.5, 0.3, 1.2, -2.25, "#c8996b"))
    for i, colr in enumerate(("#ff6b6b", "#5fd3c4", accent, "#9b8cff", "#ff9e6b")):
        M.append(box(-0.85 + i * 0.12, 1.2, -2.45, -0.75 + i * 0.12, 1.42 - (i % 2) * 0.05, -2.3, colr, outline=0.7, bias=0.1))
    M += [cylinder(0.12, 1.2, -2.37, 0.07, 0.12, "#c86b4a", bias=0.1), sphere(0.12, 1.42, -2.37, 0.12, "#3fae6a", 4, 7, bias=0.12)]
    glows = [((2.5, 1.2, -2.2), 1.1, "#ffd27a"), ((1.4, 1.7, -2.45), 1.4, mix(sky, "#ffffff", 0.3))]
    return M, glows


def hallway(lockers=("#4f7be8", "#ef6f8f", "#5fd3c4"), wall="#e8e2d6", floor="#b9b2c9"):
    """A school/college corridor along -z: floor x -2..2 from z 4 to -14, lockers on both walls."""
    M = [quad((-2, 0, 4), (2, 0, 4), (2, 0, -14), (-2, 0, -14), floor, layer=0),
         quad((-2, 0, 4), (-2, 0, -14), (-2, 3, -14), (-2, 3, 4), wall, layer=0),
         quad((2, 0, -14), (2, 0, 4), (2, 3, 4), (2, 3, -14), wall, layer=0),
         quad((-2, 3, -14), (2, 3, -14), (2, 3, 4), (-2, 3, 4), mix(wall, "#8a86a8", 0.3), layer=0),
         quad((-2, 0, -14), (2, 0, -14), (2, 3, -14), (-2, 3, -14), mix(wall, "#ffd27a", 0.25), layer=0)]
    for i in range(-14, 4, 2):           # floor tiles stripes
        M.append(quad((-2, 0.004, i + 1), (2, 0.004, i + 1), (2, 0.004, i), (-2, 0.004, i), mix(floor, "#ffffff", 0.18), layer=1))
    for side in (-1, 1):
        x0 = -2 if side < 0 else 1.62
        for k in range(16):
            z = 3.4 - k * 1.05
            colr = lockers[(k + (side > 0)) % len(lockers)]
            m = box(x0, 0.1, z - 0.48, x0 + 0.38, 2.05, z + 0.48, colr, outline=1.0)
            M.append(m)
    for k in range(5):                   # ceiling lights
        z = 2 - k * 3.5
        M.append(Mesh([(-0.5, 2.98, z + 0.3), (0.5, 2.98, z + 0.3), (0.5, 2.98, z - 0.3), (-0.5, 2.98, z - 0.3)][::-1],
                      [(0, 1, 2, 3)], "#fffbe8", layer=1, outline=0.0, glow="#fff6d0"))
    return M


def glow_points(c, W, H, cam, glows, a=1.0):
    """Soft additive-looking light pools for lamps/windows (drawn after render)."""
    for p, r, colr in glows:
        pc = cam.to_cam(np.array([p], float))
        if pc[0, 2] <= cam.near:
            continue
        s = cam.project(pc, W, H)[0]; rp = r * cam.focal(H) / pc[0, 2]
        c.drawCircle(float(s[0]), float(s[1]), rp, paint(shader=rad(float(s[0]), float(s[1]), rp,
                     [(0, colr, 0.35 * a), (1, colr, 0.0)])))
