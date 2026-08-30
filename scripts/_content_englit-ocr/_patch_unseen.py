# -*- coding: utf-8 -*-
"""
PATCH the six english-literature-ocr / unseen-poetry lesson rows in place.

Updates ONLY: description, content_html, exam_tip_html, conclusion_html,
practice_questions, knowledge_checks, flashcard_questions, glossary_terms.
Plus lessons.title for L5 only (slot re-aimed per brief).

Never touches: slug, lesson_number, hero_*, status, narration_manifest,
related_media, youtube_video_id, diagrams, practice_data.
"""
import sys, os, json

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
from lib.supabase_client import get_client

FIELDS = ["description", "content_html", "exam_tip_html", "conclusion_html",
          "practice_questions", "knowledge_checks", "flashcard_questions", "glossary_terms"]

rows = json.load(open(os.path.join(HERE, "_unseen_rebuild.json"), encoding="utf-8"))
sb = get_client()

for r in rows:
    payload = {k: r[k] for k in FIELDS}
    if r["lesson_number"] == 5:
        payload["title"] = r["title"]
    res = sb.table("lessons").update(payload).eq("id", r["lesson_id"]).execute()
    print("L%d patched (%d fields) -> %s" % (r["lesson_number"], len(payload), r["lesson_id"]))
print("done")
