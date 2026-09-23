#!/bin/bash
# Resume a student walk from wherever it stopped. Every stage skips work already on file.
cd "C:/Users/tshau/Documents/Study Vault"
export PYTHONIOENCODING=utf-8 SV_QA_BASE=http://127.0.0.1:8910
W="python scripts/_qa_student_walk.py"
unusable=$(python -c "import json,io;a=json.load(io.open('scripts/_studentwalk/attempts.json',encoding='utf-8'));v=json.load(io.open('scripts/_studentwalk/views.json',encoding='utf-8'));print(sum(1 for k in v if k not in a or 'answer' not in a[k]))")
if [ "$unusable" -gt 0 ]; then
  echo "== re-attempt $unusable $(date)"; $W attempt | tail -1
  until $W collect | tee /dev/stderr | grep -q "attempts on file"; do sleep 60; done
fi
echo "== mark $(date)"; $W mark | tail -3
echo "== adjudicate $(date)"; $W adjudicate | tail -1
until $W collect-adjudication | tee /dev/stderr | grep -q "adjudications on file"; do sleep 60; done
echo "== report $(date)"; $W report
echo "== done $(date)"
