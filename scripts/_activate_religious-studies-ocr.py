"""Phase 2 — Subject activation for OCR GCSE (9-1) Religious Studies (J625), free tier.

Reads scripts/_content_religious-studies-ocr/_plan.json and creates:
  - 1 subjects row (status=live, school_id=null)
  - 14 units rows (sort_order 1..14)
  - ~50 empty lesson shells (status=pending_review)

Cover-all build: every OCR religion (Christianity, Islam, Judaism, Buddhism,
Hinduism) for Beliefs+Practices, plus the 4 Group-2 themes, so any centre's
two-religion choice is served. No route-picker needed (students browse all units).

Idempotent guard: if a subjects row with slug 'religious-studies-ocr' already
exists (school_id NULL) the script ABORTS without modifying anything
(per memory/feedback_dont_wipe_existing_supabase_rows.md).
"""
import json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

scripts = Path(__file__).resolve().parent
plan = json.loads((scripts / "_content_religious-studies-ocr" / "_plan.json").read_text(encoding="utf-8"))
sb = get_client()

SUBJECT_SLUG = plan["subject"]["slug"]   # religious-studies-ocr
SCHOOL_ID = None                          # free tier


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[''′']", "", s)
    s = re.sub(r"[–—]", "-", s)
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:80]


print(f"=== Activating {SUBJECT_SLUG} ===\n")

existing = (sb.table("subjects").select("id, slug, status").eq("slug", SUBJECT_SLUG)
            .is_("school_id", "null").execute().data)
if existing:
    print(f"ERROR: subjects row '{SUBJECT_SLUG}' already exists (id={existing[0]['id']}, "
          f"status={existing[0]['status']}). Aborting to avoid overwriting data.")
    sys.exit(1)
print(f"  Clean slate — no existing '{SUBJECT_SLUG}' row. Proceeding with INSERT.")

settings = {
    "has_exam_guides": False,
    "practice_units": [],
    "question_type_names": plan.get("question_type_names", []),
    "unit_image_positions": {u["slug"]: "center center" for u in plan["article_units"]},
}

subject_payload = {
    "name": plan["subject"]["name"],            # Religious Studies
    "slug": SUBJECT_SLUG,                        # religious-studies-ocr
    "exam_board": plan["subject"]["exam_board"], # OCR
    "spec_code": plan["subject"]["spec_code"],   # J625
    "school_id": SCHOOL_ID,
    "color": plan["subject"]["target_hero_colour"],
    "is_active": True,
    "status": "live",
    "sort_order": 0,
    "image_url": None,
    "settings": settings,
}
SUBJECT_ID = sb.table("subjects").insert(subject_payload).execute().data[0]["id"]
print(f"\n  Subject row INSERTED: {SUBJECT_ID}")

print(f"\n--- Inserting {len(plan['article_units'])} units ---")
unit_rows = {}
for pu in plan["article_units"]:
    payload = {
        "subject_id": SUBJECT_ID, "slug": pu["slug"], "name": pu["name"], "subtitle": pu["subtitle"],
        "body_class": pu["body_class"], "accent": pu["accent"], "accent_light": pu["accent_light"],
        "accent_badge": pu["accent_badge"], "lesson_count": pu["lesson_count"],
        "sort_order": pu["sort_order"], "image_url": None,
    }
    unit_rows[pu["slug"]] = sb.table("units").insert(payload).execute().data[0]
    print(f"  INSERTED unit {pu['sort_order']:2d}  [{pu['slug'][:50]}]  id={unit_rows[pu['slug']]['id']}")

print(f"\n--- Inserting lesson shells ---")
total = 0
for pu in plan["article_units"]:
    unit_id = unit_rows[pu["slug"]]["id"]
    used = set(); n_in = 0
    for L in pu["lessons"]:
        n = L["number"]; title = L["title"].strip()
        desc = (L.get("description") or "").strip()[:300]
        base = slugify(title) or f"lesson-{n}"; slug = base; i = 2
        while slug in used:
            slug = f"{base}-{i}"; i += 1
        used.add(slug)
        sb.table("lessons").insert({
            "unit_id": unit_id, "lesson_number": n, "slug": slug, "title": title,
            "description": desc, "status": "pending_review", "tier": "both",
            "content_html": None, "youtube_video_id": None,
        }).execute()
        n_in += 1; total += 1
    print(f"  [{pu['slug'][:50]}] {n_in} lessons")

print("\n--- Verification ---")
expected = sum(u["lesson_count"] for u in plan["article_units"])
db_total = 0; all_ok = True
for pu in plan["article_units"]:
    cnt = sb.table("lessons").select("id", count="exact").eq("unit_id", unit_rows[pu["slug"]]["id"]).execute().count
    db_total += cnt
    ok = cnt == pu["lesson_count"]; all_ok = all_ok and ok
    print(f"  {pu['slug'][:50]:50s}  {cnt:3d} lessons  [{'OK' if ok else 'MISMATCH exp '+str(pu['lesson_count'])}]")
print(f"\n  Total lessons : {db_total} / Expected : {expected}")

if all_ok and db_total == expected:
    print(f"\n=== DB activation COMPLETE for {SUBJECT_SLUG} ===  subject={SUBJECT_ID}  units={len(unit_rows)}  lessons={db_total}")
else:
    print("\n  WARN: verification failed"); sys.exit(1)
