"""Batch 02: chapters, SRT captions and the upload-metadata sheet."""
import json, re, sys
sys.path.insert(0, "/home/claude/proj")
import glob as _glob, importlib as _il, os as _os
CHAPTERS = {}
for _p in sorted(_glob.glob("/home/claude/proj/narration*.py")):
    CHAPTERS.update(getattr(_il.import_module(_os.path.basename(_p)[:-3]), "CHAPTERS", {}))
B = "/home/claude/proj/build"; OUT = "/home/claude/out/batch2"

def mmss(t): t = int(t); return f"{t // 60}:{t % 60:02d}"
def ts(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s - int(s)) * 1000)) % 1000:03d}"

def tts_to_text(s):
    rep = {"Cheek-shoo-loob": "Chicxulub", "tee rex": "T. rex", "A-M-O-C": "AMOC",
           "twenty twenty-four": "2024", "twenty twenty-five": "2025", "twenty twenty-two": "2022", "twenty twenty": "2020",
           "twenty seventeen": "2017", "twenty sixteen": "2016", "twenty twelve": "2012", "nineteen seventy": "1970",
           "twenty-one hundred": "2100"}
    rep.update({"Rosh": "Roche", "La-shom": "Laschamp", "Her-nan-tee-an": "Hirnantian", "Eh-liz-ee-uh klor-ot-ih-kuh": "Elysia chlorotica",
                "Caleb Sharf": "Caleb Scharf", "Sharf": "Scharf", "cow-ree": "kauri", "stoh-mah-tuh": "stomata", "Maven": "MAVEN",
                "twenty twenty-six": "2026", "eighteen fifty-nine": "1859", "eighteen thirty-one": "1831", "nineteen eighty-nine": "1989",
                "twenty eighteen": "2018", "twenty fourteen": "2014"})
    for a in sorted(rep, key=len, reverse=True): s = s.replace(a, rep[a])
    return s

def srt(name, path):
    tl = json.load(open(f"{B}/{name}/timeline.json")); out, n = [], 1
    for s in tl["scenes"]:
        for L in s["lines"]:
            text = tts_to_text(L["text"])
            parts = [p.strip() for p in re.split(r"(?<=[.?!:;])\s+", text) if p.strip()]
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
    open(path, "w").write("\n".join(out))

def chapters(name):
    tl = json.load(open(f"{B}/{name}/timeline.json")); st = {s["key"]: s["start"] for s in tl["scenes"]}
    return "\n".join(f"{'0:00' if k == 'hook' else mmss(st[k])} {lab}" for k, lab in CHAPTERS[name]), mmss(tl["total"])

def length(name): return mmss(json.load(open(f"{B}/{name}/timeline.json"))["total"])

if __name__ == "__main__":
    # usage: python3 meta2.py OUT_DIR name=file.srt [name=file.srt ...] [short_name ...]
    OUT = sys.argv[1]
    for a in sys.argv[2:]:
        if "=" in a:
            name, fn = a.split("=", 1); srt(name, f"{OUT}/{fn}")
            ch, tot = chapters(name); print(f"== {name} ({tot})\n{ch}\n")
        else:
            print(a, length(a))
