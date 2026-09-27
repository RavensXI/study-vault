#!/bin/bash
# Re-mix the audio of rendered files without re-encoding the picture (same chain as render.cjs):
#   VIDEOS="students" DEPTS="general history" bash reaudio.sh
cd "$(dirname "$0")"
D="C:/Users/tshau/Documents/StudyVault Business/marketing/launch-video-v2"
CHAIN='alimiter=limit=0.76:attack=1:release=50:level=disabled,aresample=192000,alimiter=limit=0.77:attack=0.5:release=40:level=disabled,aresample=48000'
for dept in ${DEPTS:-general history geography science}; do for v in ${VIDEOS:-students teachers}; do
  wav=out/score-$dept-$v.wav
  I=$(ffmpeg -hide_banner -nostats -i $wav -af ebur128 -f null - 2>&1 | grep -E "^\s+I:" | tail -1 | grep -oE -- "-?[0-9.]+")
  gain=$(python -c "print(round(-12.2 - ($I), 2))")
  for ar in 16x9 1x1 9x16; do
    f=$dept-$v-$ar
    ffmpeg -v error -y -i out/$f.mp4 -i $wav -map 0:v -map 1:a -c:v copy -af "volume=${gain}dB,$CHAIN" -c:a aac -b:a 256k -ar 48000 -movflags +faststart -shortest out/_tmp.mp4 && mv out/_tmp.mp4 out/$f.mp4
    cp out/$f.mp4 "$D/$dept/"
    ffmpeg -v error -y -i "$D/$dept/$f-web.mp4" -i $wav -map 0:v -map 1:a -c:v copy -af "volume=${gain}dB,$CHAIN" -c:a aac -b:a 160k -ar 48000 -movflags +faststart -shortest out/_tmp.mp4 && mv out/_tmp.mp4 "$D/$dept/$f-web.mp4"
    echo "$f gain $gain"
  done
done; done
