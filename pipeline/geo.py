"""Real-coastline maps and a rotating textured globe (Natural Earth, public domain)."""
import json, math
from functools import lru_cache
import numpy as np, cv2, skia
from core import *

DATA = "/home/claude/data"

@lru_cache(maxsize=2)
def land_polys(res="50m"):
    gj = json.load(open(f"{DATA}/ne_{res}_land.geojson"))
    polys = []
    for f in gj["features"]:
        g = f["geometry"]
        rings = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
        for poly in rings:
            polys.append(np.array(poly[0], dtype=np.float64))  # outer ring only
    return polys

PANGEA = [(-70, 70), (-20, 76), (40, 72), (90, 64), (112, 48), (100, 30), (62, 26), (30, 16), (55, 4), (72, -12),
          (64, -36), (40, -60), (0, -80), (-40, -72), (-62, -46), (-56, -20), (-72, 0), (-82, 25), (-86, 50)]

def _smooth(pts, it=3):
    P = np.array(pts, np.float64)
    for _ in range(it):
        Q = np.roll(P, -1, axis=0)
        P = np.stack([0.75 * P + 0.25 * Q, 0.25 * P + 0.75 * Q], 1).reshape(-1, 2)
    return P

@lru_cache(maxsize=8)
def texture(kind="earth", W=2048, H=1024):
    """Equirectangular RGBA texture. kinds: earth, ice, pangea_none"""
    surf = skia.Surface(W, H); c = surf.getCanvas()
    ocean = {"earth": "#1f6fd1", "ice": "#a9c9e6", "dark": "#0b1a3a", "pangea": "#1f6fd1"}[kind]
    land = {"earth": "#3dbb6c", "ice": "#eef5fb", "dark": "#1b2b3a", "pangea": "#4caf5a"}[kind]
    c.clear(col(ocean))
    p = paint(land)
    src = land_polys("50m") if kind != "pangea" else [_smooth(PANGEA)]
    for poly in src:
        x = (poly[:, 0] + 180) / 360 * W; y = (90 - poly[:, 1]) / 180 * H
        path = skia.Path(); path.moveTo(x[0], y[0])
        for i in range(1, len(x)): path.lineTo(x[i], y[i])
        path.close(); c.drawPath(path, p)
    arr = surf.makeImageSnapshot().toarray().copy()  # BGRA or RGBA depending on platform
    img = surf.makeImageSnapshot()
    arr = np.frombuffer(img.tobytes(), np.uint8).reshape(H, W, 4).copy()
    info = img.imageInfo().colorType()
    if info == skia.kBGRA_8888_ColorType: arr = arr[:, :, [2, 1, 0, 3]]
    if kind == "earth":
        lat = 90 - (np.arange(H) + 0.5) / H * 180
        landmask = (np.abs(arr[:, :, 1].astype(int) - rgb(land)[1]) < 30)
        polar = (np.abs(lat) > 64)[:, None] & landmask
        arr[polar] = (238, 245, 251, 255)
    return np.ascontiguousarray(arr)

_grid = {}
def _disk(R):
    if R not in _grid:
        if len(_grid) > 24: _grid.clear()
        n = 2 * R
        yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
        nx = (xx + 0.5 - R) / R; ny = (yy + 0.5 - R) / R
        r2 = nx * nx + ny * ny
        nz = np.sqrt(np.clip(1 - r2, 0, 1))
        alpha = np.clip((1 - np.sqrt(r2)) * R * 1.0, 0, 1)
        _grid[R] = (nx, -ny, nz, alpha)
    return _grid[R]

def globe_img(R, rot, tilt=18, kind="earth", light=(-0.75, 0.35, 0.55), night=0.0, ice=0.0, ambient=0.25, blend_kind=None,
              cap_s=None, cap_n=None, haze=0.0, haze_col=(190, 170, 120)):
    R = int(R)
    nx, ny, nz, alpha = _disk(R)
    tr = math.radians(tilt)
    # inverse tilt (rotate around x axis)
    y2 = ny * math.cos(tr) + nz * math.sin(tr)
    z2 = -ny * math.sin(tr) + nz * math.cos(tr)
    lat = np.arcsin(np.clip(y2, -1, 1))
    lon = np.arctan2(nx, z2) + math.radians(rot)
    tex = texture(kind)
    Ht, Wt = tex.shape[:2]
    mx = ((lon / (2 * math.pi) + 0.5) % 1.0 * Wt).astype(np.float32)
    my = ((0.5 - lat / math.pi) * Ht).astype(np.float32)
    out = cv2.remap(tex, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP)
    if blend_kind and ice > 0:
        out2 = cv2.remap(texture(blend_kind), mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP)
        out = (out.astype(np.float32) * (1 - ice) + out2.astype(np.float32) * ice).astype(np.uint8)
    if cap_s is not None or cap_n is not None:
        latd = np.degrees(lat)
        m = np.zeros(latd.shape, bool)
        if cap_s is not None: m |= latd < cap_s
        if cap_n is not None: m |= latd > cap_n
        out[m, :3] = (236, 244, 252)
    if haze > 0:
        out[:, :, :3] = (out[:, :, :3].astype(np.float32) * (1 - haze) + np.array(haze_col, np.float32) * haze).astype(np.uint8)
    L = np.array(light, np.float32); L /= np.linalg.norm(L)
    lam = np.clip(nx * L[0] + ny * L[1] + nz * L[2], 0, 1)
    shade = ambient + (1 - ambient) * lam
    shade = shade * (1 - night) + night * 0.12
    rgbf = out[:, :, :3].astype(np.float32) * shade[:, :, None]
    # rim highlight (atmosphere)
    rim = np.clip((np.sqrt(nx * nx + ny * ny) - 0.82) / 0.18, 0, 1) ** 2
    rgbf = rgbf * (1 - 0.35 * rim[:, :, None]) + np.array([140, 200, 255], np.float32) * 0.35 * rim[:, :, None] * (1 - night * 0.7)
    a = (alpha * 255).astype(np.uint8)
    res = np.dstack([np.clip(rgbf, 0, 255).astype(np.uint8), a])
    # premultiply for skia
    res[:, :, :3] = (res[:, :, :3].astype(np.uint16) * a[:, :, None] // 255).astype(np.uint8)
    return np.ascontiguousarray(res)

def globe(c, x, y, R, rot, tilt=18, kind="earth", light=(-0.75, 0.35, 0.55), night=0.0, glow=1.0, a=1.0, **kw):
    if R < 2: return
    R = max(4, int(R) // 4 * 4)
    img = globe_img(R, rot, tilt, kind, light, night, **kw)
    if glow > 0:
        circle(c, x, y, R * 1.08, "#6fb6ff", 0.3 * glow * a * (1 - night * 0.6), blur=R * 0.07)
    im = skia.Image.fromarray(img, colorType=skia.kRGBA_8888_ColorType, alphaType=skia.kPremul_AlphaType)
    p = skia.Paint(); p.setAlphaf(a)
    c.drawImageRect(im, skia.Rect.MakeXYWH(x - R, y - R, 2 * R, 2 * R), skia.SamplingOptions(skia.FilterMode.kLinear), p)

# ---------------- flat maps ----------------
_paths = {}
def land_path(bbox, rect, res="50m"):
    key = (bbox, rect, res)
    if key in _paths: return _paths[key]
    lon0, lat0, lon1, lat1 = bbox; X, Y, Wd, Hd = rect
    path = skia.Path()
    for poly in land_polys(res):
        if poly[:, 0].max() < lon0 - 5 or poly[:, 0].min() > lon1 + 5 or poly[:, 1].max() < lat0 - 5 or poly[:, 1].min() > lat1 + 5:
            continue
        xs = X + (poly[:, 0] - lon0) / (lon1 - lon0) * Wd
        ys = Y + (lat1 - poly[:, 1]) / (lat1 - lat0) * Hd
        path.moveTo(xs[0], ys[0])
        for i in range(1, len(xs)): path.lineTo(xs[i], ys[i])
        path.close()
    _paths[key] = path
    return path

def lonlat_xy(lon, lat, bbox, rect):
    lon0, lat0, lon1, lat1 = bbox; X, Y, Wd, Hd = rect
    return X + (lon - lon0) / (lon1 - lon0) * Wd, Y + (lat1 - lat) / (lat1 - lat0) * Hd

def draw_map(c, bbox, rect, land="#3dbb6c", sea="#1f6fd1", rim=None, rim_w=0, shrink_land=0, sea_col_for_shrink=None,
             outline="#0b1030", outline_w=2.0, res="50m"):
    X, Y, Wd, Hd = rect
    c.save(); c.clipRect(skia.Rect.MakeXYWH(X, Y, Wd, Hd))
    c.drawRect(skia.Rect.MakeXYWH(X, Y, Wd, Hd), paint(sea))
    path = land_path(bbox, rect, res)
    if rim and rim_w > 0:
        c.drawPath(path, paint(rim, 1, stroke=rim_w * 2))
    c.drawPath(path, paint(land))
    if shrink_land > 0:
        c.drawPath(path, paint(sea_col_for_shrink or sea, 1, stroke=shrink_land * 2))
    if outline_w:
        c.drawPath(path, paint(outline, 0.35, stroke=outline_w))
    c.restore()
    return path


def map_rect(bbox, cx, cy, width=None, height=None):
    """Integer rect for a bbox with a roughly true aspect (cos-lat corrected), centred on cx, cy."""
    lon0, lat0, lon1, lat1 = bbox
    k = (lat1 - lat0) / ((lon1 - lon0) * math.cos(math.radians((lat0 + lat1) / 2)))
    if width is None: width = height / k
    height = width * k
    return (int(cx - width / 2), int(cy - height / 2), int(width), int(height))

def globe_xy(lon, lat, cx, cy, R, rot, tilt=18):
    """screen position of lon/lat on a globe drawn with globe(c, cx, cy, R, rot, tilt); returns (x, y, visible)."""
    R = max(4, int(R) // 4 * 4)
    la, lo = math.radians(lat), math.radians(lon - rot)
    nxp, y2, z2 = math.cos(la) * math.sin(lo), math.sin(la), math.cos(la) * math.cos(lo)
    tr = math.radians(tilt)
    ny = y2 * math.cos(tr) - z2 * math.sin(tr); nz = y2 * math.sin(tr) + z2 * math.cos(tr)
    return cx + nxp * R, cy - ny * R, nz > 0
