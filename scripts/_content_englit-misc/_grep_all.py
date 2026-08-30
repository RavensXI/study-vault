"""Grep every field of every fetched lesson for a pattern."""
import json, os, re, sys
os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass
OUT = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(OUT, "_targets_raw.json"), encoding="utf-8"))

prefix = sys.argv[1]
pat = sys.argv[2]
ctx = int(sys.argv[3]) if len(sys.argv) > 3 else 260
rx = re.compile(pat)

FIELDS = ["title", "description", "content_html", "exam_tip_html", "conclusion_html",
          "knowledge_checks", "practice_questions", "flashcard_questions", "glossary_terms"]

for key in sorted(d, key=lambda k: (k.rsplit("/", 1)[0], int(k.rsplit("/", 1)[1]))):
    if not key.startswith(prefix):
        continue
    row = d[key]
    for f in FIELDS:
        v = row.get(f)
        if v is None:
            continue
        s = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
        for m in rx.finditer(s):
            a, b = max(0, m.start() - ctx), min(len(s), m.end() + ctx)
            print(f"\n----- {key} :: {f} @{m.start()} -----")
            print("..." + s[a:b].replace("\n", " ") + "...")
