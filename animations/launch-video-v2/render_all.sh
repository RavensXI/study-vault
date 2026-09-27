#!/bin/bash
# every department x both videos x three ratios, plus web versions, into the delivery folder
cd "C:/Users/tshau/Documents/Study Vault/animations/launch-video-v2"
export NODE_PATH="$(npm root -g)"
D="C:/Users/tshau/Documents/StudyVault Business/marketing/launch-video-v2"

for dept in ${DEPTS:-general history geography science}; do
  mkdir -p "$D/$dept"; node score.cjs students $dept; node score.cjs teachers $dept
  for v in students teachers; do for ar in 16x9 1x1 9x16; do
    node render.cjs $v $ar --dept=$dept 2>&1 | tail -1
    cp out/$dept-$v-$ar.mp4 "$D/$dept/"
    ffmpeg -loglevel error -y -i out/$dept-$v-$ar.mp4 -c:v libx264 -preset slow -crf 25 -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart "$D/$dept/$dept-$v-$ar-web.mp4"
  done; done
done
echo ALL DONE
