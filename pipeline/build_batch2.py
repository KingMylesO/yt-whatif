"""Render all Batch 02 videos (2 at a time), then mux each with its mix."""
import os, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

B = "/home/claude/proj/build"; OUT = "/home/claude/out/batch2"
NAMES = {
    "short_b2_wood": "short_wood_never_rots.mp4",
    "short_b2_oxygen": "short_35_percent_oxygen.mp4",
    "short_b2_30s": "short_asteroid_30_seconds.mp4",
    "short_b2_belt": "short_asteroid_belt_empty.mp4",
    "short_b2_med": "short_mediterranean_vanished.mp4",
    "short_b2_amoc": "short_atlantic_current_off.mp4",
    "b2_trees": "what_if_trees_never_rot.mp4",
    "b2_asteroid": "what_if_asteroid_30_seconds_late.mp4",
    "b2_med": "what_if_mediterranean_dried_up.mp4",
}

def job(name):
    t0 = time.time()
    r = subprocess.run([sys.executable, "render.py", "render", name], cwd="/home/claude/proj", capture_output=True, text=True)
    if r.returncode != 0:
        print(name, "RENDER FAILED", r.stderr[-2000:], flush=True); return
    while not os.path.exists(f"{B}/{name}/mix.wav"): time.sleep(5)
    time.sleep(2)
    out = f"{OUT}/{NAMES[name]}"; tmp = out[:-4] + ".tmp.mp4"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f"{B}/{name}/video_only.mp4", "-i", f"{B}/{name}/mix.wav",
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest",
                    "-movflags", "+faststart", tmp], check=True)
    os.replace(tmp, out)
    print(name, "DONE", f"{time.time() - t0:.0f}s", flush=True)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    names = sys.argv[1:] or list(NAMES)
    with ThreadPoolExecutor(2) as ex: list(ex.map(job, names))
    print("ALL DONE", flush=True)
