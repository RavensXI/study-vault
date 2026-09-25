#!/bin/bash
# Overnight English Language student walk, 24-25 Sep 2026. The student answers and the
# adjudications go through the Claude Code SUBSCRIPTION (no API credit), capped by
# SV_WALK_BUDGET in API-equivalent dollars (raised 25 Sep: Tom, only 6% of the weekly allowance used) (_studentwalk_spend.json).
# Click-and-choose questions only (Tom, 25 Sep: the AI-marked written answers are proven).
# Order: finish Edexcel 1EN0, then AQA (the biggest board), then OCR, Eduqas, Unity while budget lasts.
cd "C:/Users/tshau/Documents/Study Vault"
export PYTHONIOENCODING=utf-8 SV_QA_BASE=http://127.0.0.1:8910 SV_WALK_BUDGET=400
W="python scripts/_qa_student_walk.py"
# the Edexcel mark pass started earlier is still running on its own; wait for it
while tasklist //FI "PID eq $1" 2>/dev/null | grep -q python; do sleep 60; done
for SUB in english-language-edexcel english-language-aqa english-language-ocr english-language-eduqas english-language; do
  export SV_WALK_DIR=scripts/_studentwalk_$SUB
  echo "######## $SUB $(date)"
  [ -f $SV_WALK_DIR/views.json ] || $W extract --subject $SUB | tail -3
  $W attempt-sub --no-ai | tail -2
  $W mark --no-ai | tail -2
  $W mark --no-ai | tail -2          # a second pass picks up any lesson the first could not load
  $W adjudicate --sub --no-ai | tail -2
  $W report | tail -2
  python -c "import json;print('spent so far (API-equivalent): \$%.2f' % json.load(open('scripts/_studentwalk_spend.json'))['usd'])"
done
echo "######## all done $(date)"
