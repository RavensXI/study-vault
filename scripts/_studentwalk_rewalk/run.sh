#!/bin/bash
# Re-walk of the 68 questions the 23 Sep student walk found faulty, after the fixes.
cd "C:/Users/tshau/Documents/Study Vault"
export PYTHONIOENCODING=utf-8 SV_QA_BASE=http://127.0.0.1:8910 SV_WALK_DIR=scripts/_studentwalk_rewalk
W="python scripts/_qa_student_walk.py"
echo "== extract $(date)"; $W extract --keys scripts/_studentwalk_rewalk/keys.json | tail -1
echo "== attempt $(date)"; $W attempt | tail -1
until $W collect | tee /dev/stderr | grep -q "attempts on file"; do sleep 60; done
echo "== mark $(date)"; $W mark | tail -2
echo "== adjudicate $(date)"; $W adjudicate | tail -1
until $W collect-adjudication | tee /dev/stderr | grep -q "adjudications on file"; do sleep 60; done
echo "== report $(date)"; $W report
echo "== done $(date)"
