#!/bin/bash
# Re-walk of the 180 corrected questions (25 Sep 2026): blind attempt, site marks, examiner judges.
cd "C:/Users/tshau/Documents/Study Vault"
export PYTHONIOENCODING=utf-8 SV_QA_BASE=http://127.0.0.1:8910 SV_WALK_BUDGET=100000 SV_WALK_DIR=scripts/_studentwalk_fixcheck
W="python scripts/_qa_student_walk.py"
$W extract --keys scripts/_studentwalk_fixed_keys.json | tail -2
for r in 1 2; do $W attempt-sub --no-ai | tail -1; done
SV_WALK_CHUNK=1 $W attempt-sub --no-ai | tail -1
$W mark --no-ai | tail -1
$W adjudicate --sub --no-ai | tail -1
$W report | tail -1
