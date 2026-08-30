# -*- coding: utf-8 -*-
"""Render a lesson JSON row into readable text for register review."""
import sys, os, json, glob
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass

def render(r):
    L = []
    L.append("TITLE: %s" % r.get("title"))
    L.append("SLUG: %s  LESSON_NUMBER: %s  STATUS: %s" % (r.get("slug"), r.get("lesson_number"), r.get("status")))
    L.append("\n--- DESCRIPTION ---\n%s" % r.get("description"))
    for f in ("content_html","exam_tip_html","conclusion_html"):
        v = r.get(f)
        if v: L.append("\n--- %s ---\n%s" % (f.upper(), v))
    for f in ("practice_questions","knowledge_checks","flashcard_questions","glossary_terms"):
        v = r.get(f)
        if v:
            L.append("\n--- %s ---\n%s" % (f.upper(), json.dumps(v, ensure_ascii=False, indent=1)))
    return "\n".join(L)

for p in sorted(glob.glob(sys.argv[1])):
    r = json.load(open(p, encoding="utf-8"))
    out = os.path.splitext(p)[0] + ".txt"
    open(out,"w",encoding="utf-8").write(render(r))
    print("wrote", out)
