"""Scan a dumped unit for AO2 / assessment-objective passages.

Input is a unit dump written by scripts/_retrofc/_dump_unit.js:
    node scripts/_retrofc/_dump_unit.js <unit_id> <out.json>
    python scripts/_retrofc/_ao2_scan.py <out.json>
"""
import json
import os
import re
import sys

if sys.platform == "win32":
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

PATH = sys.argv[1]
rows = json.load(open(PATH, encoding="utf-8"))
PAT = re.compile(r"AO2|AO1|AO3|AO4|assessment objective|no extract|language analysis|closed book", re.I)

for r in rows:
    fields = {
        "content_html": r.get("content_html") or "",
        "exam_tip_html": r.get("exam_tip_html") or "",
        "conclusion_html": r.get("conclusion_html") or "",
        "description": r.get("description") or "",
        "practice_questions": json.dumps(r.get("practice_questions"), ensure_ascii=False),
        "knowledge_checks": json.dumps(r.get("knowledge_checks"), ensure_ascii=False),
        "flashcard_questions": json.dumps(r.get("flashcard_questions"), ensure_ascii=False),
        "glossary_terms": json.dumps(r.get("glossary_terms"), ensure_ascii=False),
    }
    for f, v in fields.items():
        if f == "practice_questions":
            continue  # band ladders are out of scope for this job
        for m in PAT.finditer(v):
            s = max(0, m.start() - 320)
            print(f"\n### L{r['lesson_number']:02d} [{f}] @{m.start()} ({m.group(0)})")
            print(re.sub(r"\s+", " ", v[s:m.start() + 320]))
