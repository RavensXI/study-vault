#!/bin/bash
# Full student walk for one subject, start to report. Log: scripts/_studentwalk/run.log
cd "C:/Users/tshau/Documents/Study Vault"
export PYTHONIOENCODING=utf-8 SV_QA_BASE=http://127.0.0.1:8910
SUB=${1:-english-language-2-edexcel}
W="python scripts/_qa_student_walk.py"
echo "== extract $(date)"; $W extract --subject $SUB | tail -3
echo "== attempt $(date)"; $W attempt | tail -1
until $W collect | tee /dev/stderr | grep -q "attempts on file"; do sleep 60; done
echo "== mark $(date)"; $W mark | tail -3
echo "== adjudicate $(date)"; $W adjudicate | tail -1
until $W collect-adjudication | tee /dev/stderr | grep -q "adjudications on file"; do sleep 60; done
echo "== report $(date)"; $W report
