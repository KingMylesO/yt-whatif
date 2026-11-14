"""Render frames / previews / full videos from a timeline."""
import json, os, re, subprocess, sys, time
import numpy as np, skia
sys.path.insert(0, os.path.dirname(__file__))
from core import *
import scenes as SC
import glob as _glob
ALL = dict(SC.SCENES)
for _m in ["common2"] + sorted(os.path.basename(p)[:-3] for p in _glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "scenes_*.py"))):
    ALL.update(__import__(_m).SCENES)

FPS = 30
B = "/home/claude/proj/build"

def load(name): return json.load(open(f"{B}/{name}/timeline.json"))
def size(name): return (1080, 1920) if name.startswith("short") else (1920, 1080)

def chunks(text, maxw=3):
    words = text.replace("…", "… ").split()
    out, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) >= maxw or w[-1] in ".,?!:;…" or len(" ".join(cur)) > 15:
            out.append(" ".join(cur)); cur = []
    if cur: out.append(" ".join(cur))
    return out

def caption_at(sc, t):
    for L in sc["lines"]:
        if L["start"] - 0.05 <= t <= L["end"] + 0.25:
            ch = chunks(L["text"])
            wts = [len(c_) + (4 if c_[-1] in ".,?!:;…" else 0) for c_ in ch]
            tot = sum(wts); d = L["end"] - L["start"]; acc = L["start"]
            for c_, w in zip(ch, wts):
                seg = d * w / tot
                if t < acc + seg or c_ is ch[-1]:
                    return c_, (t - acc)
                acc += seg
    return None, 0

def overlay_short(c, W, H, t, sc):
    u = min(W, H) / 1080
    o = sc.get("opts", {})
    if o.get("badge"):
        p = prog(t, 0.0, 0.35)
        chip(c, o["badge"], W / 2, 0.14 * H, p, 52 * u, bg=ACCENT, fg="#0b1030", a=1)
    cap, age = caption_at(sc, t)
    if cap:
        s = cap.upper().replace("…", "…")
        sz = fit(s, W * 0.86, 84 * u, 900)
        pop = lerp(0.86, 1.0, eback(clamp(age / 0.12)))
        c.save(); c.translate(W / 2, 0.635 * H); c.scale(pop, pop)
        text(c, s, 0, 0, sz, "#ffffff", 1, w=900, stroke=14 * u, stroke_col="#0b1030")
        text(c, s, 0, 0, sz, "#ffffff", 1, w=900)
        c.restore()

class Drawer:
    def __init__(self, name):
        self.name = name; self.W, self.H = size(name)
        self.arr = np.zeros((self.H, self.W, 4), np.uint8)
        self.surf = skia.Surface(self.arr); self.c = self.surf.getCanvas()
        self.short = name.startswith("short")
    def frame(self, sc, t):
        c = self.c; c.clear(skia.Color(0, 0, 0)); c.save()
        S = SC.Ctx(sc["dur"], sc["lines"], sc.get("opts", {}), self.W, self.H)
        ALL[sc["scene"]](c, self.W, self.H, t, S)
        c.restore()
        if self.short: overlay_short(c, self.W, self.H, t, sc)
        return self.arr

def preview(name, keys=None, fracs=(0.3, 0.85), out=None, scale=0.33):
    from PIL import Image
    tl = load(name); d = Drawer(name); ims = []
    for sc in tl["scenes"]:
        if keys and sc["key"] not in keys: continue
        for f in fracs:
            a = d.frame(sc, sc["dur"] * f).copy()
            im = Image.fromarray(a[:, :, :3]); im = im.resize((int(d.W * scale), int(d.H * scale)))
            ims.append((sc["key"], f, im))
    cols = 4 if not d.short else 6
    w, h = ims[0][2].size; rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w, rows * h), (40, 40, 40))
    for i, (_, _, im) in enumerate(ims): sheet.paste(im, ((i % cols) * w, (i // cols) * h))
    out = out or f"{B}/{name}/preview.jpg"; sheet.save(out, quality=85); return out

def still(name, key, t, out):
    from PIL import Image
    tl = load(name); d = Drawer(name)
    sc = [s for s in tl["scenes"] if s["key"] == key][0]
    Image.fromarray(d.frame(sc, t)[:, :, :3].copy()).save(out, quality=92)

def render_scene(name, sc, d, path):
    n = max(1, round(sc["dur"] * FPS)); tmp = path[:-4] + ".tmp.mp4"
    cmd = ["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{d.W}x{d.H}", "-r", str(FPS),
           "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-g", "60", tmp]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n):
        pr.stdin.write(d.frame(sc, i / FPS).tobytes())
    pr.stdin.close(); rc = pr.wait()
    if rc == 0: os.replace(tmp, path)
    else: raise RuntimeError(f"ffmpeg failed on {sc['key']}")

def render_all(name, only=None):
    tl = load(name); d = Drawer(name); od = f"{B}/{name}/scenes"; os.makedirs(od, exist_ok=True)
    t0 = time.time()
    for i, sc in enumerate(tl["scenes"]):
        p = f"{od}/{i:02d}_{sc['key']}.mp4"
        if only is not None and sc["key"] not in only and os.path.exists(p): continue
        if only is None and os.path.exists(p): continue
        render_scene(name, sc, d, p)
        print(f"{name} {sc['key']} {sc['dur']:.1f}s done ({time.time() - t0:.0f}s)", flush=True)
    with open(f"{od}/list.txt", "w") as f:
        for i, sc in enumerate(tl["scenes"]): f.write(f"file '{i:02d}_{sc['key']}.mp4'\n")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{od}/list.txt", "-c", "copy", f"{B}/{name}/video_only.mp4"], check=True)
    print(name, "video done", flush=True)

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "preview": print(preview(sys.argv[2], sys.argv[3].split(",") if len(sys.argv) > 3 and sys.argv[3] else None))
    elif cmd == "render": render_all(sys.argv[2], sys.argv[3].split(",") if len(sys.argv) > 3 else None)
