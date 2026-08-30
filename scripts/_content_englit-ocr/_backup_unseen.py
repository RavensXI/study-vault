"""Back up the six english-literature-ocr / unseen-poetry lesson rows before rebuild."""
import sys, os, json
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from lib.supabase_client import get_client

UNIT_ID = "d15cce20-ab7f-4b4b-849f-53fd6595785d"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_unseen_backup_2026-08-30.json")

sb = get_client()
rows = sb.table("lessons").select("*").eq("unit_id", UNIT_ID).execute().data
rows.sort(key=lambda r: r["lesson_number"])

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(rows, f, ensure_ascii=False, indent=1)

print("Backed up %d rows -> %s" % (len(rows), OUT))
for r in rows:
    print("  L%s %s (%s)" % (r["lesson_number"], r["title"], r["id"]))
