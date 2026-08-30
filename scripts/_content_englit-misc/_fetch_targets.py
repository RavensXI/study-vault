"""Fetch the four target lessons for the EngLit surgical fixes."""
import json, os, sys
os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SCRIPT_DIR)
from lib.supabase_client import get_client

sb = get_client()
OUT = os.path.dirname(os.path.abspath(__file__))

TARGETS = [
    ("english-literature-aqa", "frankenstein", [6]),
    ("english-literature-aqa", "leave-taking", [1, 2, 3, 4, 5, 6, 7, 8]),
    ("english-literature-edexcel", "boys-dont-cry", [6]),
]

dump = {}
for subj_slug, unit_slug, nums in TARGETS:
    subj = sb.table("subjects").select("id,slug,name,school_id").eq("slug", subj_slug).execute().data
    print(f"subject {subj_slug}: {len(subj)} rows -> {[(s['id'], s['school_id']) for s in subj]}")
    for s in subj:
        units = sb.table("units").select("*").eq("subject_id", s["id"]).eq("slug", unit_slug).execute().data
        for u in units:
            rows = sb.table("lessons").select("*").eq("unit_id", u["id"]).in_("lesson_number", nums).order("lesson_number").execute().data
            for r in rows:
                key = f"{subj_slug}/{unit_slug}/{r['lesson_number']}"
                dump[key] = r
                print(f"  {key}  id={r['id']}  status={r.get('status')}  title={r['title']!r}")

with open(os.path.join(OUT, "_targets_raw.json"), "w", encoding="utf-8") as f:
    json.dump(dump, f, indent=2, ensure_ascii=False)
print(f"\nWrote {len(dump)} lessons.")
print("FIELDS:", sorted(next(iter(dump.values())).keys()))
