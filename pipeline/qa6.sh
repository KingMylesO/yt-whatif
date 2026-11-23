#!/bin/bash
# usage: qa5.sh name  -> duration, loudness, contact sheet, CTA frame
n=$1; f=/home/claude/out/b6/$n.mp4; d=/home/claude/out/b6/qa; mkdir -p $d
dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $f)
lufs=$(nice ffmpeg -nostats -i $f -af ebur128 -f null - 2>&1 | grep -A2 "Integrated loudness" | grep " I:" | awk '{print $2}')
if [[ $n == short* ]]; then step=3; tile=6x3; sc=180; else step=20; tile=6x5; sc=320; fi
nice ffmpeg -loglevel error -y -i $f -vf fps=1/$step,scale=$sc:-1,tile=$tile -frames:v 1 $d/${n}_sheet.jpg
read cs ce frac <<< $(python3 -c "
import json; tl=json.load(open('/home/claude/proj/build/$n/timeline.json'))
for s in tl['scenes']:
    i=s['opts'].get('cta')
    if i is not None:
        L=s['lines'][i]; a=s['start']+L['start']; print(round(a,2), round(s['start']+L['end'],2), round(a/tl['total'],3))")
nice ffmpeg -loglevel error -y -ss $(python3 -c "print($cs+1.5)") -i $f -frames:v 1 $d/${n}_cta.jpg
echo "$n dur=$dur lufs=$lufs cta_start=$cs frac=$frac"
