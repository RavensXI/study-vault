#!/bin/bash
# Rebuild media/ (gitignored): each department's own R2 explainer frames and narration clip.
#   frames: 2.8 s from a single slide (after the scene cut, clear of the NotebookLM endcard), cropped
#           1088x612 at x16 so the NotebookLM watermark (bottom right) is outside the picture
#   narration: the lesson's n2 section, leading silence removed, first 1.45 s with a 0.2 s fade
# general uses the history media. The envelope in departments/<dept>.json (media.env) is the clip's
# per-frame RMS, normalised; re-derive it if the clip changes.
cd "$(dirname "$0")" && mkdir -p media && cd media
V=https://video.studyvault-media.co.uk; A=https://audio.studyvault-media.co.uk
while read d vid at narr; do
  curl -sfo $d-explainer.mp4 "$V/$vid"; curl -sfo $d-narr.mp3 "$A/$narr"
  rm -rf frames/$d; mkdir -p frames/$d
  ffmpeg -v error -ss $at -i $d-explainer.mp4 -t 2.8 -vf "fps=30,crop=1088:612:16:0,scale=768:432" -q:v 3 frames/$d/f%03d.jpg
  ffmpeg -v error -y -i $d-narr.mp3 -af "silenceremove=start_periods=1:start_threshold=-45dB,atrim=0:1.45,afade=t=out:st=1.25:d=0.2,aresample=48000" -ac 1 -f f32le $d-narr.f32
done <<'LIST'
history history-aqa/conflict-tension-inter-war/explainer_l07.mp4 133.4 history-aqa/conflict-tension-inter-war/narration_lesson-07_n2.mp3
geography geography-aqa/paper-1/explainer_l23.mp4 121.8 geography/paper-1/narration_lesson-23_n2.mp3
science science-aqa/biology-paper-1/explainer_l02.mp4 417.6 science/biology-paper-1/narration_lesson-02_n2.mp3
LIST
