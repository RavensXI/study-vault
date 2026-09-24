#!/bin/bash
# Student walk on the other English Language subjects (24 Sep 2026), one after another
# (the live marker's hourly limit is per address). Each subject gets its own directory.
cd "C:/Users/tshau/Documents/Study Vault"
export PYTHONIOENCODING=utf-8 SV_QA_BASE=http://127.0.0.1:8910
W="python scripts/_qa_student_walk.py"
for SUB in english-language-edexcel english-language-aqa english-language-ocr english-language-eduqas english-language; do
  export SV_WALK_DIR=scripts/_studentwalk_$SUB
  echo "######## $SUB $(date)"
  [ -f $SV_WALK_DIR/views.json ] || $W extract --subject $SUB | tail -3
  [ -f $SV_WALK_DIR/attempts.json ] || $W attempt | tail -1
  until $W collect 2>&1 | tail -1 | grep -q "attempts on file"; do sleep 60; done
  $W mark | tail -2
  $W adjudicate | tail -1
  until $W collect-adjudication 2>&1 | tail -1 | grep -q "adjudications on file"; do sleep 60; done
  $W report | tail -2
done
echo "######## all done $(date)"
