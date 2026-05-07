"""Quick verification of the sociology-eduqas activation."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

sb = get_client()

# Subject
subj = (
    sb.table("subjects")
    .select("id, slug, name, exam_board, spec_code, status, school_id, color, sort_order, settings")
    .eq("slug", "sociology-eduqas")
    .is_("school_id", "null")
    .execute()
    .data
)
print(f"=== subjects rows for slug=sociology-eduqas, school_id=null ===")
print(f"  count: {len(subj)}")
for s in subj:
    print(f"  id={s['id']}")
    print(f"  name={s['name']}  exam_board={s['exam_board']}  spec_code={s['spec_code']}")
    print(f"  status={s['status']}  school_id={s['school_id']}  color={s['color']}")
    settings = s.get("settings") or {}
    print(f"  settings keys: {sorted(settings.keys())}")
    print(f"    has_exam_guides={settings.get('has_exam_guides')}")
    print(f"    practice_units={settings.get('practice_units')}")
    print(f"    question_type_names count={len(settings.get('question_type_names', []))}")
    qth = settings.get("quote_ticker_html", "") or ""
    print(f"    quote_ticker_html length={len(qth)} chars")
    print(f"    unit_image_positions={settings.get('unit_image_positions')}")

if not subj:
    print("  NO ROW FOUND")
    sys.exit(1)

SUBJECT_ID = subj[0]["id"]

# Units
units = (
    sb.table("units")
    .select("id, slug, name, body_class, accent, accent_light, accent_badge, lesson_count, sort_order")
    .eq("subject_id", SUBJECT_ID)
    .order("sort_order")
    .execute()
    .data
)
print(f"\n=== units rows ({len(units)}) ===")
for u in units:
    print(
        f"  [{u['sort_order']}] {u['slug']:42s} "
        f"accent={u['accent']} body_class={u['body_class']:30s} "
        f"lesson_count={u['lesson_count']}"
    )

# Lessons — count by status
print(f"\n=== lessons rows by status ===")
for status in ["pending_review", "live", "draft", "archived"]:
    cnt = 0
    for u in units:
        c = (
            sb.table("lessons")
            .select("id", count="exact")
            .eq("unit_id", u["id"])
            .eq("status", status)
            .execute()
            .count
        )
        cnt += c
    if cnt:
        print(f"  {status}: {cnt}")

total = 0
for u in units:
    total += (
        sb.table("lessons")
        .select("id", count="exact")
        .eq("unit_id", u["id"])
        .execute()
        .count
    )
print(f"\n=== lessons total across all units: {total} ===")

# Spot-check first 3 lessons
print(f"\n=== first 3 lessons in unit 1 ===")
u1 = units[0]
ls = (
    sb.table("lessons")
    .select("lesson_number, slug, title, description, status, tier")
    .eq("unit_id", u1["id"])
    .order("lesson_number")
    .limit(3)
    .execute()
    .data
)
for L in ls:
    print(f"  L{L['lesson_number']} [{L['status']}] tier={L['tier']}")
    print(f"    slug: {L['slug']}")
    print(f"    title: {L['title']}")
    print(f"    desc: {(L['description'] or '')[:100]}")
