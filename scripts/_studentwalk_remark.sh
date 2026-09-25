#!/bin/bash
# Re-mark (25 Sep 2026): answers the walk could not enter (quote marks), then judge and report.
cd "C:/Users/tshau/Documents/Study Vault"
export PYTHONIOENCODING=utf-8 SV_QA_BASE=http://127.0.0.1:8910 SV_WALK_BUDGET=400 SV_WALK_CHUNK=1
W="python scripts/_qa_student_walk.py"
for SUB in english-language-edexcel english-language-aqa english-language-ocr english-language-eduqas english-language; do
  export SV_WALK_DIR=scripts/_studentwalk_$SUB
  echo "######## $SUB $(date)"


  $W mark --no-ai | tail -1
  $W adjudicate --sub --no-ai | tail -1
  $W report | tail -1
done
echo "######## residue done $(date)"
