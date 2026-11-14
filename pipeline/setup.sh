#!/bin/bash
# One-time setup for a fresh cloud workspace. Run from the repo root: bash pipeline/setup.sh
set -e
REPO="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p /home/claude/proj /home/claude/data /home/claude/tts /home/claude/out
cp "$REPO"/pipeline/*.py /home/claude/proj/
pip install --break-system-packages -q skia-python kokoro-onnx soundfile scipy opencv-python-headless numpy pillow 2>&1 | tail -1 || true
command -v ffmpeg >/dev/null || (apt-get install -y -q ffmpeg >/dev/null 2>&1 || pip install --break-system-packages -q imageio-ffmpeg)
fc-list | grep -q "Inter Display" || echo "WARNING: Inter Display font missing (fonts-inter package)"
cd /home/claude/tts
[ -s kokoro-v1.0.onnx ] || curl -sSL -o kokoro-v1.0.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
[ -s voices-v1.0.bin ] || curl -sSL -o voices-v1.0.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
cd /home/claude/data
NE=https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson
for f in ne_110m_land ne_50m_land ne_50m_coastline; do [ -s $f.geojson ] || curl -sSL -o $f.geojson $NE/$f.geojson; done
cd /home/claude/proj
python3 voice.py short_selftest >/dev/null 2>&1
python3 render.py render short_selftest >/dev/null 2>&1
python3 -c "import audio; audio.mix('short_selftest')" >/dev/null 2>&1
ffprobe -v error -show_entries format=duration -of csv=p=0 build/short_selftest/video_only.mp4 >/dev/null && echo "SETUP OK: voice, render and mix all work"
