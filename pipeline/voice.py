"""Generate narration with Kokoro (af_heart) and build per-video timelines."""
import hashlib, json, os, sys
import numpy as np, soundfile as sf
from scipy.signal import resample_poly
sys.path.insert(0, os.path.dirname(__file__))
from narration import VIDEOS as V1
from narration2 import VIDEOS as V2
VIDEOS = {**V1, **V2}

SR = 48000
CACHE = "/home/claude/proj/build/tts_cache"
os.makedirs(CACHE, exist_ok=True)
_k = None

def kokoro():
    global _k
    if _k is None:
        from kokoro_onnx import Kokoro
        _k = Kokoro("/home/claude/tts/kokoro-v1.0.onnx", "/home/claude/tts/voices-v1.0.bin")
    return _k

def tts(text, speed):
    h = hashlib.md5(f"af_heart|{speed}|{text}".encode()).hexdigest()[:16]
    p = f"{CACHE}/{h}.wav"
    if not os.path.exists(p):
        s, sr = kokoro().create(text, voice="af_heart", speed=speed, lang="en-us")
        s = resample_poly(s.astype(np.float64), SR, sr)
        # trim leading/trailing near-silence
        env = np.abs(s)
        idx = np.where(env > 0.01)[0]
        if len(idx):
            a = max(0, idx[0] - int(0.03 * SR)); b = min(len(s), idx[-1] + int(0.08 * SR))
            s = s[a:b]
        sf.write(p, s.astype(np.float32), SR)
    s, _ = sf.read(p, dtype="float32")
    return s

def build(name):
    short = name.startswith("short")
    speed = 1.0 if short else 0.95
    pre, gap, post = (0.15, 0.3, 0.35) if short else (0.3, 0.5, 0.55)
    scenes, t = [], 0.0
    clips = []
    for sc in VIDEOS[name]:
        lines = []
        if sc["lines"]:
            lt = pre
            for i, text in enumerate(sc["lines"]):
                a = tts(text, speed)
                d = len(a) / SR
                lines.append(dict(text=text, start=round(lt, 3), end=round(lt + d, 3)))
                clips.append((t + lt, a))
                lt += d + (gap if i < len(sc["lines"]) - 1 else 0)
            dur = lt + post + sc.get("hold", 0)
        else:
            dur = sc.get("hold", 1.5)
        dur = round(dur * 30) / 30  # whole frames
        sfx = []
        for nm, off in sc.get("sfx", []):
            if isinstance(off, str):  # "L1+0.32" -> line 1 start + 0.32*len
                li, frac = off[1:].split("+"); L = lines[int(li)]
                off = L["start"] + float(frac) * (L["end"] - L["start"])
            sfx.append((nm, round(t + off, 3)))
        scenes.append(dict(key=sc["key"], scene=sc["scene"], start=round(t, 4), dur=dur,
                           lines=lines, sfx=sfx, opts=sc.get("opts", {})))
        t += dur
    total = t
    voice = np.zeros(int(total * SR) + SR, dtype=np.float32)
    for st, a in clips:
        i = int(st * SR); voice[i:i + len(a)] += a
    voice = voice[: int(total * SR)]
    out = f"/home/claude/proj/build/{name}"
    os.makedirs(out, exist_ok=True)
    sf.write(f"{out}/voice.wav", voice, SR)
    json.dump(dict(name=name, total=total, scenes=scenes), open(f"{out}/timeline.json", "w"), indent=1)
    print(name, f"{total:.1f}s", len(scenes), "scenes", flush=True)

if __name__ == "__main__":
    for n in (sys.argv[1:] or ["short_sun", "short_sleep", "long"]):
        build(n)
