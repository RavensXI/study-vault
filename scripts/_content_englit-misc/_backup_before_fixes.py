"""Back up every field the four EngLit surgical fixes will touch.

Writes scripts/_content_englit-misc/_final_fixes_backup.json in the same
shape _bdc_renarrate.py consumes:
    {lesson_id: {"label", "fields": {...}, "narration_manifest": [...]}}

Read-only against Supabase. MUST run before the first PATCH.
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

# lesson id -> label. Every row any fix will PATCH.
TOUCHED = {
    "0581f441-6e06-475c-b1b3-36d8184b8673": "frankenstein L6 (Walton/Creature ambiguity)",
    "e832b6dd-6e34-4e53-b71b-78c8ece8e905": "leave-taking L2 (Act 1 title)",
    "4038c672-d9f6-4924-9195-71745f273f3c": "leave-taking L3 (Act 2 title + Enid marriage)",
    "dfc930cd-8246-46cc-9d9b-4fc16885d08e": "leave-taking L5 (Enid marriage)",
    "c81cefe5-ecc1-4cc0-a8c6-1e30dbb7aee5": "boys-dont-cry L6 (n28 playwright->novelist)",
}

# Full snapshot of every field that could conceivably be written.
FIELDS = ["title", "description", "content_html", "exam_tip_html", "conclusion_html",
          "knowledge_checks", "practice_questions", "flashcard_questions",
          "glossary_terms"]

if os.path.exists(BACKUP):
    print(f"REFUSING: {BACKUP} already exists — not overwriting a backup.")
    sys.exit(1)

sb = get_client()
out = {}
for lid, label in TOUCHED.items():
    row = sb.table("lessons").select(
        "id,lesson_number,title,unit_id,narration_manifest," + ",".join(
            f for f in FIELDS if f != "title")
    ).eq("id", lid).single().execute().data
    out[lid] = {
        "label": label,
        "lesson_number": row["lesson_number"],
        "unit_id": row["unit_id"],
        "fields": {f: row.get(f) for f in FIELDS},
        "narration_manifest": row.get("narration_manifest"),
    }
    nm = row.get("narration_manifest") or []
    print(f"  backed up {lid}  L{row['lesson_number']}  {len(nm)} manifest entries  {label}")

with open(BACKUP, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print(f"\nWrote backup: {BACKUP}  ({len(out)} lessons)")
