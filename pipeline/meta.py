import json, sys, re
sys.path.insert(0, "/home/claude/proj")
from narration import CHAPTERS
B = "/home/claude/proj/build"
tl = json.load(open(f"{B}/long/timeline.json")); st = {s["key"]: s["start"] for s in tl["scenes"]}
def mmss(t): t = int(t); return f"{t // 60}:{t % 60:02d}"
ch = "\n".join(f"{'0:00' if k == 'hook' else mmss(st[k])} {lab}" for k, lab in CHAPTERS)
print(ch); print("total", mmss(tl["total"]))
# SRT for long-form
def ts(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h:02d}:{m:02d}:{int(s):02d},{int((s - int(s)) * 1000):03d}"
out, n = [], 1
for s in tl["scenes"]:
    for L in s["lines"]:
        parts = [p.strip() for p in re.split(r"(?<=[.?!:;])\s+", L["text"]) if p.strip()]
        # merge very short parts, split long ones at commas
        segs = []
        for p in parts:
            if len(p) > 84 and "," in p:
                bits = p.split(", "); cur = ""
                for b in bits:
                    if len(cur) + len(b) > 70 and cur: segs.append(cur + ","); cur = b
                    else: cur = (cur + ", " + b) if cur else b
                segs.append(cur)
            else: segs.append(p)
        tot = sum(len(x) for x in segs); a = s["start"] + L["start"]; d = L["end"] - L["start"]
        for x in segs:
            dd = d * len(x) / tot
            out.append(f"{n}\n{ts(a)} --> {ts(a + dd)}\n{x}\n"); n += 1; a += dd
open("/home/claude/out/what_if_the_sun_vanished.en.srt", "w").write("\n".join(out))
open(f"{B}/long/chapters.txt", "w").write(ch)
