"""Render videos 2 at a time and mux each with its mix (mixes run one at a time; parallel mixes ran out of memory).

usage: python3 build_batch.py OUT_DIR name=file.mp4 [name=file.mp4 ...]
Expects build/<name>/timeline.json + voice.wav (run voice.py first)."""
import os, subprocess, sys, time, threading
from concurrent.futures import ThreadPoolExecutor

B = "/home/claude/proj/build"
_mix_lock = threading.Lock()

def job(name, out):
    t0 = time.time()
    r = subprocess.run([sys.executable, "render.py", "render", name], cwd="/home/claude/proj", capture_output=True, text=True)
    if r.returncode != 0:
        print(name, "RENDER FAILED", r.stderr[-3000:], flush=True); return False
    with _mix_lock:
        r = subprocess.run([sys.executable, "-c", f"import audio; audio.mix({name!r})"], cwd="/home/claude/proj", capture_output=True, text=True)
        if r.returncode != 0:
            print(name, "MIX FAILED", r.stderr[-3000:], flush=True); return False
    tmp = out[:-4] + ".tmp.mp4"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f"{B}/{name}/video_only.mp4", "-i", f"{B}/{name}/mix.wav",
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
                    "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, out)
    print(name, "DONE", out, f"{time.time() - t0:.0f}s", flush=True)
    return True

if __name__ == "__main__":
    od = sys.argv[1]; os.makedirs(od, exist_ok=True)
    pairs = [a.split("=", 1) for a in sys.argv[2:]]
    with ThreadPoolExecutor(2) as ex:
        res = list(ex.map(lambda p: job(p[0], f"{od}/{p[1]}"), pairs))
    print("ALL DONE", sum(res), "of", len(res), flush=True)
