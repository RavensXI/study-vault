#!/bin/bash
# Catch-up (25 Sep 2026): questions whose subscription answer call failed or came back incomplete.
# Up to three rounds per board; each round redoes only what is still missing.
cd "C:/Users/tshau/Documents/Study Vault"
export PYTHONIOENCODING=utf-8 SV_QA_BASE=http://127.0.0.1:8910 SV_WALK_BUDGET=400
W="python scripts/_qa_student_walk.py"
for SUB in english-language-aqa english-language-ocr english-language-eduqas; do
  export SV_WALK_DIR=scripts/_studentwalk_$SUB
  echo "######## $SUB $(date)"
  for round in 1 2 3; do $W attempt-sub --no-ai | tail -1; done
  $W mark --no-ai | tail -1
  $W adjudicate --sub --no-ai | tail -1
  $W report | tail -1
done
echo "######## catch-up done $(date)"
