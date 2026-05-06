"""One-shot prep script for Edexcel German (1GN1) Phase 3 scaffolding.

- Fetches the Edexcel subject + 27 lesson IDs from Supabase (subjects.slug = 'german-edexcel').
- Pulls the AQA German source lessons' practice_data for every plan lesson with
  transfer_score in (high, medium). Writes them to _source/aqa_<unit>_lesson_<N>.json.
- Pulls a complete AQA German lesson with practice_data as the canonical
  reference and writes it to _reference_lesson.json.
- Builds the 6 batch JSONs (one per Edexcel theme), enriching each plan lesson
  with the Supabase lesson_id and a source_aqa_file path (where applicable).

Idempotent: overwrites files. Reads only — no Supabase writes.

Run from repo root: python scripts/_content_german-edexcel/_prep_fetch.py
"""
import json
import os
import sys
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = THIS_DIR.parent
sys.path.insert(0, str(SCRIPTS_DIR))
from lib.supabase_client import get_client  # noqa: E402

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

OUT_DIR = THIS_DIR
SOURCE_DIR = OUT_DIR / "_source"
PLAN_PATH = SCRIPTS_DIR / "_plan_german-edexcel.json"

OUT_DIR.mkdir(exist_ok=True)
SOURCE_DIR.mkdir(exist_ok=True)
(OUT_DIR / "lessons").mkdir(exist_ok=True)

sb = get_client()
plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))


# ============================================================ Resolve subjects
print("=== Resolving Supabase subject + lesson IDs ===\n")

target_subject = (
    sb.table("subjects")
    .select("id, slug, name")
    .eq("slug", "german-edexcel")
    .is_("school_id", "null")
    .single()
    .execute()
    .data
)
TARGET_SUBJECT_ID = target_subject["id"]
print(f"  target subject: {target_subject['slug']}  ({TARGET_SUBJECT_ID})")

source_subject = (
    sb.table("subjects")
    .select("id, slug, name")
    .eq("slug", "german-aqa")
    .is_("school_id", "null")
    .single()
    .execute()
    .data
)
SOURCE_SUBJECT_ID = source_subject["id"]
print(f"  source subject: {source_subject['slug']}  ({SOURCE_SUBJECT_ID})")


# ============================================================ Target lesson map
target_units = (
    sb.table("units")
    .select("id, slug, name, sort_order")
    .eq("subject_id", TARGET_SUBJECT_ID)
    .order("sort_order")
    .execute()
    .data
)
target_unit_by_slug = {u["slug"]: u for u in target_units}

target_lesson_map = {}  # (unit_slug, lesson_number) -> {id, slug, title}
for u in target_units:
    rows = (
        sb.table("lessons")
        .select("id, lesson_number, slug, title")
        .eq("unit_id", u["id"])
        .order("lesson_number")
        .execute()
        .data
    )
    for row in rows:
        target_lesson_map[(u["slug"], row["lesson_number"])] = row
print(f"  target units: {len(target_units)}, target lessons: {len(target_lesson_map)}")


# ============================================================ Source unit map
source_units = (
    sb.table("units")
    .select("id, slug, name")
    .eq("subject_id", SOURCE_SUBJECT_ID)
    .execute()
    .data
)
source_unit_by_slug = {u["slug"]: u for u in source_units}
print(f"  source units: {[u['slug'] for u in source_units]}\n")


# ============================================================ Pull source lessons
def fetch_source_lesson(unit_slug, lesson_number):
    if unit_slug not in source_unit_by_slug:
        return None, f"source unit {unit_slug} not found"
    uid = source_unit_by_slug[unit_slug]["id"]
    res = (
        sb.table("lessons")
        .select("id, lesson_number, slug, title, practice_data")
        .eq("unit_id", uid)
        .eq("lesson_number", lesson_number)
        .execute()
        .data
    )
    if not res:
        return None, f"source lesson {unit_slug}/L{lesson_number} not found"
    return res[0], None


print("=== Pulling source AQA lessons (high/medium transfer only) ===\n")
source_files_written = 0
unmatched = []
counts_by_score = {"high": 0, "medium": 0, "low": 0, "fresh": 0}

for unit in plan["practice_units"]:
    for L in unit["lessons"]:
        ct = L["content_transfer"]
        score = ct["transfer_score"]
        counts_by_score[score] = counts_by_score.get(score, 0) + 1
        if score not in ("high", "medium"):
            continue
        src_unit = ct["source_unit_slug"]
        src_num = ct["source_lesson_number"]
        src, err = fetch_source_lesson(src_unit, src_num)
        if err:
            unmatched.append((unit["slug"], L["number"], src_unit, src_num, err))
            print(f"  [MISS]  {unit['slug']}/L{L['number']:02d}  -> aqa {src_unit}/L{src_num}  ({err})")
            continue
        out_path = SOURCE_DIR / f"aqa_{src_unit}_lesson_{src_num}.json"
        if out_path.exists():
            print(f"  [skip]  aqa_{src_unit}_lesson_{src_num}.json already written")
            continue
        out_path.write_text(
            json.dumps(
                {
                    "_source_meta": {
                        "source_subject_slug": "german-aqa",
                        "source_unit_slug": src_unit,
                        "source_lesson_number": src_num,
                        "source_lesson_id": src["id"],
                        "source_lesson_title": src["title"],
                    },
                    "practice_data": src.get("practice_data") or {},
                },
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        source_files_written += 1
        print(f"  [{score:6s}] {unit['slug']}/L{L['number']:02d}  -> aqa_{src_unit}_lesson_{src_num}.json  ({src['title']})")

print(
    f"\n  source files written: {source_files_written}"
    f"\n  transfer score totals: {counts_by_score}"
    f"\n  unmatched: {len(unmatched)}"
)


# ============================================================ Reference lesson
print("\n=== Pulling canonical reference lesson (AQA German people-and-lifestyle L01) ===\n")
ref_lesson, err = fetch_source_lesson("people-and-lifestyle", 1)
if not ref_lesson:
    print(f"  ERROR: {err}")
    sys.exit(1)
ref_path = OUT_DIR / "_reference_lesson.json"
ref_path.write_text(
    json.dumps(
        {
            "_source_meta": {
                "source_subject_slug": "german-aqa",
                "source_unit_slug": "people-and-lifestyle",
                "source_lesson_number": 1,
                "source_lesson_id": ref_lesson["id"],
                "source_lesson_title": ref_lesson["title"],
                "purpose": "Canonical structural reference for Edexcel German Phase 3 content agents. Match SHAPE only — adapt vocab and Edexcel theme framing.",
            },
            "practice_data": ref_lesson.get("practice_data") or {},
        },
        indent=2,
        ensure_ascii=False,
    ),
    encoding="utf-8",
)
print(f"  reference lesson: {ref_lesson['title']}  ->  {ref_path.name}")


# ============================================================ Batch JSONs
print("\n=== Building batch JSONs (one per theme) ===\n")

THEME_BATCH_IDS = {
    "my-personal-world": "t1_personal_world",
    "lifestyle-and-wellbeing": "t2_lifestyle_wellbeing",
    "my-neighbourhood": "t3_neighbourhood",
    "media-and-technology": "t4_media_tech",
    "studying-and-my-future": "t5_studying_future",
    "travel-and-tourism": "t6_travel_tourism",
}

SUBJECT_META = {
    "name": "German",
    "slug": "german-edexcel",
    "exam_board": "Edexcel",
    "spec_code": "1GN1",
    "target_audience": "free-tier",
    "subject_id": TARGET_SUBJECT_ID,
    "subject_type": "gcse-tiered",
    "format": "practice-first",
    "language": "German",
    "language_code": "de",
}

SHARED = {
    "spec_slice_path": "scripts/_content_german-edexcel/_spec_german-edexcel.txt",
    "reference_lesson_path": "scripts/_content_german-edexcel/_reference_lesson.json",
    "schema_path": "scripts/language-practice/PRACTICE_DATA_SCHEMA.md",
    "agent_prompt_path": "scripts/_content_german-edexcel/_AGENT_PROMPT.md",
    "subject_level_teaching_brief": plan["teaching_brief"],
    "edexcel_role_play_settings": [
        "Café / restaurant",
        "Shop / market / shopping centre",
        "Hotel",
        "Train station",
        "Tourist information office",
        "Cinema / theatre / concert hall",
        "Campsite",
        "Leisure centre",
        "Doctor's surgery / hospital",
        "In town",
    ],
    "output_dir": "scripts/_content_german-edexcel/lessons",
}

batches_written = []
batch_breakdown = {}

for unit in plan["practice_units"]:
    bid = THEME_BATCH_IDS[unit["slug"]]
    lessons_in_batch = []
    for L in unit["lessons"]:
        key = (unit["slug"], L["number"])
        if key not in target_lesson_map:
            print(f"  WARNING: target lesson {unit['slug']}/L{L['number']} not in Supabase")
            continue
        target_row = target_lesson_map[key]

        ct = L["content_transfer"]
        source_aqa_file = None
        if ct["transfer_score"] in ("high", "medium"):
            src_unit = ct["source_unit_slug"]
            src_num = ct["source_lesson_number"]
            candidate = SOURCE_DIR / f"aqa_{src_unit}_lesson_{src_num}.json"
            if candidate.exists():
                source_aqa_file = f"scripts/_content_german-edexcel/_source/aqa_{src_unit}_lesson_{src_num}.json"

        lessons_in_batch.append(
            {
                "lesson_id": target_row["id"],
                "lesson_number": L["number"],
                "slug": target_row["slug"],
                "title": L["title"],
                "description": L["description"],
                "tier": L["tier"],
                "spec_references": L["spec_references"],
                "section_markers": L["section_markers"],
                "content_transfer": ct,
                "source_aqa_file": source_aqa_file,
            }
        )

    batch = {
        "batch_id": bid,
        "subject": SUBJECT_META,
        "unit": {
            "name": unit["name"],
            "slug": unit["slug"],
            "subtitle": unit["subtitle"],
            "body_class": unit["body_class"],
            "accent": unit["accent"],
            "accent_light": unit["accent_light"],
            "accent_badge": unit["accent_badge"],
            "lesson_count": unit["lesson_count"],
            "sort_order": unit["sort_order"],
            "unit_id": target_unit_by_slug[unit["slug"]]["id"],
        },
        **SHARED,
        "lessons_in_batch": lessons_in_batch,
    }

    batch_path = OUT_DIR / f"_batch_{bid}.json"
    batch_path.write_text(json.dumps(batch, indent=2, ensure_ascii=False), encoding="utf-8")
    batches_written.append(batch_path.name)
    batch_breakdown[bid] = {"unit_slug": unit["slug"], "lesson_count": len(lessons_in_batch)}
    print(f"  {batch_path.name}  ->  {len(lessons_in_batch)} lessons")

print("\n=== DONE ===")
print(json.dumps({
    "source_files_written": source_files_written,
    "transfer_score_counts": counts_by_score,
    "unmatched": unmatched,
    "batches": batch_breakdown,
}, indent=2))
