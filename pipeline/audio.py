"""Original synth music bed + SFX + final mix (all generated here, no licensed audio)."""
import json, os, sys, subprocess
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt, fftconvolve

SR = 48000
B = "/home/claude/proj/build"
rng = np.random.default_rng(7)

def mtof(m): return 440.0 * 2 ** ((m - 69) / 12)
def lp(x, f, o=2): return sosfilt(butter(o, f, "low", fs=SR, output="sos"), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, "high", fs=SR, output="sos"), x)

def pad_bar(notes, length, detune):
    n = int((length + 3.0) * SR); t = np.arange(n) / SR; y = np.zeros(n)
    for m in notes:
        for d in (-detune, 0, detune):
            f = mtof(m) * 2 ** (d / 1200)
            for h in range(1, 6):
                y += np.sin(2 * np.pi * f * h * t + rng.random() * 6.28) / h ** 1.6
    env = np.minimum(1, t / 1.6) * np.where(t < length, 1, np.exp(-(t - length) / 0.9))
    y = lp(y * env, 1800)
    return y / (len(notes) * 3)

def pluck(m, dur=1.2, bright=1.0):
    n = int(dur * SR); t = np.arange(n) / SR; f = mtof(m)
    y = np.sin(2 * np.pi * f * t) + 0.35 * bright * np.sin(4 * np.pi * f * t) + 0.12 * bright * np.sin(6 * np.pi * f * t)
    return y * np.exp(-t / 0.35) * np.minimum(1, t / 0.004)

def reverb(x, secs=2.6, mix=0.32):
    n = int(secs * SR); ir = rng.standard_normal(n) * np.exp(-np.arange(n) / SR / (secs / 5))
    ir = lp(ir, 5000); ir /= np.sqrt(np.sum(ir ** 2))
    wet = fftconvolve(x, ir)[: len(x)]
    return (1 - mix) * x + mix * wet

PRESETS = {
    # chords as MIDI notes; bar seconds; arp step seconds
    "space": dict(chords=[[57, 64, 67, 71], [53, 60, 64, 69], [48, 55, 64, 67], [55, 62, 66, 71]], bar=8.0, step=0.5, bright=0.6),
    "short": dict(chords=[[57, 64, 67, 71], [53, 60, 64, 69], [48, 55, 64, 67], [55, 62, 66, 71]], bar=4.0, step=0.25, bright=0.9),
    "sleep": dict(chords=[[53, 57, 60, 64], [52, 55, 59, 62], [50, 53, 57, 60], [48, 52, 55, 59]], bar=4.0, step=0.25, bright=1.0),
    "forest": dict(chords=[[50, 57, 60, 64], [46, 53, 57, 62], [53, 57, 60, 65], [48, 55, 60, 64]], bar=8.0, step=0.5, bright=0.5),
    "forest_s": dict(chords=[[50, 57, 60, 64], [46, 53, 57, 62], [53, 57, 60, 65], [48, 55, 60, 64]], bar=4.0, step=0.25, bright=0.8),
    "sea": dict(chords=[[50, 57, 62, 66], [52, 59, 64, 67], [47, 54, 59, 62], [45, 52, 57, 61]], bar=8.0, step=0.5, bright=0.6),
    "sea_s": dict(chords=[[50, 57, 62, 66], [52, 59, 64, 67], [47, 54, 59, 62], [45, 52, 57, 61]], bar=4.0, step=0.25, bright=0.9),
    # batch 03
    "rings": dict(chords=[[53, 57, 60, 64], [55, 59, 62, 67], [52, 55, 59, 64], [57, 60, 64, 67]], bar=8.0, step=0.5, bright=0.55),
    "rings_s": dict(chords=[[53, 57, 60, 64], [55, 59, 62, 67], [52, 55, 59, 64], [57, 60, 64, 67]], bar=4.0, step=0.25, bright=0.85),
    "magnet": dict(chords=[[45, 52, 55, 60], [41, 48, 52, 57], [43, 50, 53, 58], [40, 47, 50, 55]], bar=8.0, step=0.5, bright=0.7),
    "magnet_s": dict(chords=[[45, 52, 55, 60], [41, 48, 52, 57], [43, 50, 53, 58], [40, 47, 50, 55]], bar=4.0, step=0.25, bright=0.9),
    "photo": dict(chords=[[48, 55, 60, 64], [53, 57, 60, 65], [45, 52, 57, 60], [50, 55, 59, 62]], bar=8.0, step=0.5, bright=0.6),
    "photo_s": dict(chords=[[48, 55, 60, 64], [53, 57, 60, 65], [45, 52, 57, 60], [50, 55, 59, 62]], bar=4.0, step=0.25, bright=0.9),
    "sky_s": dict(chords=[[50, 57, 62, 66], [47, 54, 59, 62], [43, 50, 55, 59], [45, 52, 57, 61]], bar=4.0, step=0.25, bright=0.8),
    "reef_s": dict(chords=[[52, 59, 64, 68], [49, 56, 61, 64], [45, 52, 57, 61], [47, 54, 59, 63]], bar=4.0, step=0.25, bright=0.9),
}
PRESET_FOR = {"long": "space", "short_sun": "short", "short_sleep": "sleep",
              "b2_trees": "forest", "b2_asteroid": "space", "b2_med": "sea",
              "short_b2_wood": "forest_s", "short_b2_oxygen": "forest_s", "short_b2_30s": "short", "short_b2_belt": "short",
              "short_b2_med": "sea_s", "short_b2_amoc": "sea_s"}

def music(total, preset, arp_gain, pad_gain):
    P = PRESETS[preset]; n = int(total * SR) + SR
    L = np.zeros(n); R = np.zeros(n); A = np.zeros(n); SUB = np.zeros(n)
    cache = {}
    nb = int(total / P["bar"]) + 1
    for b in range(nb):
        ch = P["chords"][b % len(P["chords"])]; k = tuple(ch)
        if k not in cache: cache[k] = (pad_bar(ch, P["bar"], 7), pad_bar(ch, P["bar"], 11))
        i = int(b * P["bar"] * SR)
        for buf, src in ((L, cache[k][0]), (R, cache[k][1])):
            seg = src[: max(0, n - i)]; buf[i:i + len(seg)] += seg
        # sub
        tt = np.arange(int(P["bar"] * SR)) / SR
        sub = np.sin(2 * np.pi * mtof(ch[0] - 12) * tt) * np.minimum(1, tt / 0.5) * np.minimum(1, (P["bar"] - tt) / 0.5)
        seg = sub[: max(0, n - i)]; SUB[i:i + len(seg)] += seg
        # arp
        steps = int(P["bar"] / P["step"])
        pat = [0, 1, 2, 3, 2, 1, 3, 2]
        for s in range(steps):
            m = ch[pat[s % len(pat)]] + 12
            j = int((b * P["bar"] + s * P["step"]) * SR)
            pl = pluck(m, bright=P["bright"]) * (0.9 if s % 2 == 0 else 0.6)
            seg = pl[: max(0, n - j)]; A[j:j + len(seg)] += seg
    A = reverb(A, 2.4, 0.45)
    padL = reverb(L, 3.0, 0.35); padR = reverb(R, 3.0, 0.35)
    g_arp = np.interp(np.arange(n) / SR, *arp_gain); g_pad = np.interp(np.arange(n) / SR, *pad_gain)
    outL = (padL * 0.55 + SUB * 0.25) * g_pad + A * 0.22 * g_arp
    outR = (padR * 0.55 + SUB * 0.25) * g_pad + A * 0.22 * g_arp
    return np.stack([outL, outR], 1)[: int(total * SR)]

# ---------------- SFX ----------------
def sfx(name):
    if name == "rumble":
        n = int(3.6 * SR); t = np.arange(n) / SR
        y = lp(rng.standard_normal(n), 110, 4) * 4 + np.sin(2 * np.pi * 42 * t) * 0.5
        env = np.minimum(1, t / 1.5) * np.exp(-np.maximum(0, t - 2.2) / 0.5)
        return y * env * 0.7
    if name == "whoosh":
        n = int(0.9 * SR); t = np.arange(n) / SR
        y = hp(lp(rng.standard_normal(n), 2500), 250)
        env = np.sin(np.pi * np.clip(t / 0.75, 0, 1)) ** 2
        return y * env * 0.5
    if name == "pop":
        n1 = int(0.3 * SR); t1 = np.arange(n1) / SR
        sw = hp(rng.standard_normal(n1), 1500) * (t1 / 0.3) ** 3 * 0.35
        n2 = int(0.7 * SR); t2 = np.arange(n2) / SR
        th = np.sin(2 * np.pi * (70 * t2 - 20 * t2 ** 2)) * np.exp(-t2 / 0.18) * 0.9
        return np.concatenate([sw, th])
    if name == "click":
        n = int(0.5 * SR); t = np.arange(n) / SR
        y = hp(rng.standard_normal(n), 2000) * np.exp(-t / 0.006) * 0.8
        y += np.sin(2 * np.pi * 85 * t) * np.exp(-t / 0.07) * 0.9
        return y
    if name == "fire":
        n = int(4.5 * SR); t = np.arange(n) / SR
        y = lp(rng.standard_normal(n), 900, 2) * 0.6
        cr = np.zeros(n); idx = rng.integers(0, n - 2000, 260)
        for i in idx: cr[i:i + 300] += hp(rng.standard_normal(300), 2500) * np.exp(-np.arange(300) / 40) * rng.uniform(0.3, 1)
        env = np.minimum(1, t / 0.8) * np.minimum(1, (4.5 - t) / 1.5)
        return (y + cr * 0.8) * env * 0.6
    if name == "scratch":
        n = int(0.55 * SR); t = np.arange(n) / SR
        f = 400 + 1600 * np.abs(np.sin(2 * np.pi * 3.2 * t))
        ph = 2 * np.pi * np.cumsum(f) / SR
        y = (np.sin(ph) * 0.4 + bp_noise(n, f)) * np.exp(-t / 0.35)
        return y * 0.7
    if name == "boom":
        n = int(5.0 * SR); t = np.arange(n) / SR
        y = np.sin(2 * np.pi * (55 * t - 6 * t ** 2).clip(0) ) * np.exp(-t / 1.4)
        y += lp(rng.standard_normal(n), 300, 4) * 5 * np.exp(-t / 0.9)
        y += hp(rng.standard_normal(n), 1200) * np.exp(-t / 0.06) * 0.6
        return y * 0.9
    if name == "chirp":
        n = int(1.2 * SR); y = np.zeros(n)
        for k, st in enumerate((0.0, 0.18, 0.32, 0.7, 0.85)):
            m = int(0.09 * SR); tt = np.arange(m) / SR
            f = 2600 + 1800 * tt / 0.09 * (1 if k % 2 == 0 else -0.5)
            sig = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * tt / 0.09) ** 2
            i = int(st * SR); y[i:i + m] += sig
        return y * 0.25
    if name == "grind":
        n = int(2.8 * SR); t = np.arange(n) / SR
        y = lp(rng.standard_normal(n), 400, 3) * 3 * (0.6 + 0.4 * np.sin(2 * np.pi * 7 * t) ** 2)
        y += np.sin(2 * np.pi * 38 * t) * 0.3
        env = np.minimum(1, t / 0.4) * np.minimum(1, (2.8 - t) / 0.6)
        return y * env * 0.6
    if name == "roar":
        n = int(6.0 * SR); t = np.arange(n) / SR
        y = lp(rng.standard_normal(n), 700, 2) * 1.6 + lp(rng.standard_normal(n), 120, 2) * 3
        env = np.minimum(1, t / 2.0) * np.minimum(1, (6.0 - t) / 2.0)
        return y * env * 0.5
    raise KeyError(name)

def bp_noise(n, f):
    y = rng.standard_normal(n)
    return hp(lp(y, 3000), 300) * 0.3

def envelope_points(tl, name):
    """Gain keyframes (times, values) for arps and pads from the scene list."""
    sc = {s["key"]: s for s in tl["scenes"]}; T = tl["total"]
    if name == "long":
        t820 = sc["c820"]["start"]; tlo = sc["lightsout"]["start"]
        sw = tlo + sc["lightsout"]["lines"][0]["start"] + 0.86 * (sc["lightsout"]["lines"][0]["end"] - sc["lightsout"]["lines"][0]["start"])
        tw_ = sc["twist"]["start"] + sc["twist"]["lines"][1]["start"]
        arp = ([0, t820 - 0.3, t820, tw_, tw_ + 3, T], [1, 1, 0, 0, 1, 1])
        pad = ([0, 2.0, t820 - 0.05, t820, sw + 0.4, sw + 4, T - 3, T], [0.6, 1, 1, 0, 0, 0.9, 0.9, 0])
        return arp, pad
    if "twist" in sc:
        tw = sc["twist"]["start"]
        arp = ([0, tw - 0.2, tw, tw + 5, tw + 7, T], [1, 1, 0, 0, 1, 1])
        pad = ([0, 0.5, tw - 0.2, tw, tw + 1.5, tw + 3.5, T - 1.0, T], [0.7, 1, 1, 0.15, 0.15, 1, 1, 0])
        return arp, pad
    return ([0, T], [1, 1]), ([0, 0.5, T - 1.0, T], [0.7, 1, 1, 0])

def _music_map():
    import glob, importlib, os
    m = {}
    for p in sorted(glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "narration*.py"))):
        m.update(getattr(importlib.import_module(os.path.basename(p)[:-3]), "MUSIC", {}))
    return m

def mix(name):
    tl = json.load(open(f"{B}/{name}/timeline.json")); T = tl["total"]; n = int(T * SR)
    voice, _ = sf.read(f"{B}/{name}/voice.wav", dtype="float64")
    voice = hp(voice[:n], 70); voice = np.pad(voice, (0, max(0, n - len(voice))))
    voice /= np.max(np.abs(voice)) + 1e-9
    preset = PRESET_FOR.get(name) or _music_map().get(name) or ("short" if name.startswith("short") else "space")
    arp, pad = envelope_points(tl, name)
    m = music(T, preset, arp, pad)
    m /= np.max(np.abs(m)) + 1e-9
    # duck under narration
    k = int(0.25 * SR)
    env = np.convolve(np.abs(voice), np.ones(k) / k, mode="same"); env /= np.percentile(env, 99) + 1e-9
    duck = 1 - 0.45 * np.clip(env * 3, 0, 1)
    mlev = 0.16 if not name.startswith("short") else 0.2
    out = np.zeros((n, 2))
    out += voice[:, None] * 0.9
    out += m[:n] * mlev * duck[:, None]
    for s in tl["scenes"]:
        for nm, at in s["sfx"]:
            y = sfx(nm); i = int(at * SR); seg = y[: max(0, n - i)]
            out[i:i + len(seg)] += seg[:, None] * 0.55
    out /= np.max(np.abs(out)) + 1e-9
    sf.write(f"{B}/{name}/mix_raw.wav", (out * 0.9).astype(np.float32), SR)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f"{B}/{name}/mix_raw.wav", "-af",
                    "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000", f"{B}/{name}/mix.wav"], check=True)
    print(name, "mix done", flush=True)

if __name__ == "__main__":
    from concurrent.futures import ProcessPoolExecutor
    names = sys.argv[1:] or ["short_sun", "short_sleep", "long"]
    with ProcessPoolExecutor(3) as ex: list(ex.map(mix, names))
