"""Mix + mux one rendered video (used after build_batch when a mix had to be redone)."""
import subprocess, sys, os
sys.path.insert(0, "/home/claude/proj"); import audio
B = "/home/claude/proj/build"
name, out = sys.argv[1], sys.argv[2]
audio.mix(name)
tmp = out[:-4] + ".tmp.mp4"
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f"{B}/{name}/video_only.mp4", "-i", f"{B}/{name}/mix.wav", "-map", "0:v", "-map", "1:a",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", tmp], check=True)
os.replace(tmp, out); print(name, "DONE", out)
