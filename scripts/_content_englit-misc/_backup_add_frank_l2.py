"""Append Frankenstein L2 to the existing fixes backup.

L2 n13 repeats the same Walton-ambiguity error corrected in L6, so it is
being written too. Existing backup entries are left untouched.
"""
import json, os, sys
os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SCRIPT_DIR)
from lib.supabase_client import get_client

OUT = os.path.dirname(os.path.abspath(__file__))
BACKUP = os.path.join(OUT, "_final_fixes_backup.json")

LID = "07d83404-fde9-43ab-8461-2064e8bb282b"
LABEL = "frankenstein L2 (Walton ambiguity, same error as L6)"
FIELDS = ["title", "description", "content_html", "exam_tip_html", "conclusion_html",
          "knowledge_checks", "practice_questions", "flashcard_questions",
          "glossary_terms"]

data = json.load(open(BACKUP, encoding="utf-8"))
if LID in data:
    print("Already backed up — leaving as is.")
    sys.exit(0)

sb = get_client()
row = sb.table("lessons").select(
    "id,lesson_number,title,unit_id,narration_manifest," + ",".join(
        f for f in FIELDS if f != "title")).eq("id", LID).single().execute().data
data[LID] = {
    "label": LABEL,
    "lesson_number": row["lesson_number"],
    "unit_id": row["unit_id"],
    "fields": {f: row.get(f) for f in FIELDS},
    "narration_manifest": row.get("narration_manifest"),
}
with open(BACKUP, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print(f"Appended {LID} (L{row['lesson_number']}, "
      f"{len(row.get('narration_manifest') or [])} manifest entries). "
      f"Backup now holds {len(data)} lessons.")
