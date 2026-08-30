"""Print selected fields of a fetched lesson, plus keyword hits."""
import json, os, re, sys
os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass
OUT = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(OUT, "_targets_raw.json"), encoding="utf-8"))

key = sys.argv[1]
mode = sys.argv[2] if len(sys.argv) > 2 else "all"
row = d[key]

TEXT_FIELDS = ["content_html", "exam_tip_html", "conclusion_html", "description"]
JSON_FIELDS = ["knowledge_checks", "practice_questions", "flashcard_questions", "glossary_terms"]

if mode == "grep":
    pat = sys.argv[3]
    rx = re.compile(pat, re.I)
    for f in TEXT_FIELDS + JSON_FIELDS:
        v = row.get(f)
        if v is None:
            continue
        s = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
        for m in rx.finditer(s):
            a, b = max(0, m.start() - 400), min(len(s), m.end() + 400)
            print(f"\n===== {f} @{m.start()} =====")
            print(s[a:b])
else:
    for f in TEXT_FIELDS:
        if mode not in ("all", f):
            continue
        print(f"\n########## {f} ##########")
        print(row.get(f) or "(none)")
    for f in JSON_FIELDS:
        if mode not in ("all", f):
            continue
        print(f"\n########## {f} ##########")
        print(json.dumps(row.get(f), indent=2, ensure_ascii=False))
