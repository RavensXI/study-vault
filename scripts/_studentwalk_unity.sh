#!/bin/bash
# Unity English Language, click-and-choose questions only (25 Sep 2026)
cd "C:/Users/tshau/Documents/Study Vault"
export PYTHONIOENCODING=utf-8 SV_QA_BASE=http://127.0.0.1:8910 SV_WALK_BUDGET=400 SV_WALK_DIR=scripts/_studentwalk_english-language
W="python scripts/_qa_student_walk.py"
$W extract --subject english-language | tail -3
$W attempt-sub --no-ai | tail -2
$W mark --no-ai | tail -2
$W mark --no-ai | tail -2
$W adjudicate --sub --no-ai | tail -2
$W report | tail -2
python -c "import json;print('spent so far (API-equivalent): \$%.2f' % json.load(open('scripts/_studentwalk_spend.json'))['usd'])"
