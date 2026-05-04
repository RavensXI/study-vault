"""Drop Film Studies foundation L2 (Slumdog) and L4 (Wadjda) from the
merged Global Film and UK Film unit.

These were Slumdog-and-Wadjda-specific case studies dressed as foundations.
Phase 7 added dedicated case studies for every film in the spec, making
these redundant for students who picked Slumdog/Wadjda (double-coverage)
and irrelevant for students who picked any other film.

Drops 2 lessons. Foundation framings L1, L3, L5 stay. Total Film Studies
goes from 44 → 42 lessons. The unit's lesson_count goes from 20 → 18.

Idempotent: re-runs detect the lessons are already gone and no-op.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

sb = get_client()

SUBJECT_SLUG = "film-studies-eduqas"
UNIT_SLUG = "global-and-uk-film"
DROP_SLUGS = [
    "analysing-narrative-slumdog-millionaire-and-frame-devices",
    "analysing-representation-wadjda-girlhood-and-power",
]

sid = sb.table("subjects").select("id").eq("slug", SUBJECT_SLUG).is_("school_id", "null").execute().data[0]["id"]
unit = sb.table("units").select("id, lesson_count").eq("subject_id", sid).eq("slug", UNIT_SLUG).execute().data[0]

print(f"Targeting unit '{UNIT_SLUG}' ({unit['id'][:8]}...)")

dropped = 0
for slug in DROP_SLUGS:
    rows = sb.table("lessons").select("id, lesson_number, title, status").eq("unit_id", unit["id"]).eq("slug", slug).execute().data
    if not rows:
        print(f"  SKIP '{slug}' — already gone")
        continue
    L = rows[0]
    if L["status"] == "archived":
        print(f"  SKIP L{L['lesson_number']} '{slug}' — already archived")
        continue
    sb.table("lessons").update({"status": "archived"}).eq("id", L["id"]).execute()
    print(f"  archived L{L['lesson_number']:2d} '{L['title']}'")
    dropped += 1

# Recalculate visible lesson_count for the unit (live only)
actual = sb.table("lessons").select("id", count="exact").eq("unit_id", unit["id"]).neq("status", "archived").execute().count
sb.table("units").update({"lesson_count": actual}).eq("id", unit["id"]).execute()
print(f"\n  unit lesson_count: {unit['lesson_count']} -> {actual}")
print(f"  archived {dropped} lesson(s)")
