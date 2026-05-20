"""One-shot: set religious-studies-aqa spec_code to '8062 / 8061'.

After 20 May 2026 wizard wiring, AQA Short Course (8061) is served from the
same Supabase row as AQA Spec A (8062). Build-status counts spec codes by
splitting on ' / ', so this row needs both codes to register as built.
Idempotent.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

sb = get_client()

row = (
    sb.table("subjects")
    .select("id, slug, spec_code")
    .eq("slug", "religious-studies-aqa")
    .is_("school_id", "null")
    .execute()
    .data
)

if not row:
    print("ERROR: no free-tier religious-studies-aqa row found")
    sys.exit(1)

subject = row[0]
current = subject.get("spec_code") or ""
print(f"current spec_code: {current!r}")

if current == "8062 / 8061":
    print("already set, nothing to do")
    sys.exit(0)

sb.table("subjects").update({"spec_code": "8062 / 8061"}).eq(
    "id", subject["id"]
).execute()

print(f"updated subjects.spec_code for {subject['slug']} ({subject['id']}) to '8062 / 8061'")
