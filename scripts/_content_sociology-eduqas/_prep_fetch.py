"""One-shot prep script for Eduqas/WJEC Sociology (C200QS / 3200QS) Phase 3 scaffolding.

Path A twin build — single Supabase row (slug 'sociology-eduqas') serves both
Eduqas (C200QS, England) and WJEC (3200QS, Wales). The two specs are
byte-identical, so the content row is shared and prose is neutral.

What this script does:

1. Reads the plan at scripts/_plan_sociology-eduqas.json.
2. Resolves the Supabase target subject (sociology-eduqas) + its 5 units +
   33 lesson IDs.
3. Resolves the Supabase source subject (sociology-aqa) + its units + lessons.
4. For each plan lesson with transfer_score in (high, medium, low), pulls the
   AQA source lesson's content fields (content_html, exam_tip_html,
   conclusion_html, practice_questions, knowledge_checks, flashcard_questions,
   glossary_terms, hero_keywords, hero_image_caption) live from Supabase.
   For 'fresh' lessons (no AQA equivalent), records source as null.
5. Builds 5 batch JSONs (one per Eduqas/WJEC unit), named
   _batch_u{N}_{unit_slug_short}.json. Each batch has:
   - batch_id, subject metadata, unit metadata
   - subject_level_teaching_brief (copied from plan)
   - registered_question_type_names + allowed_question_types_for_this_unit
   - lessons_in_batch — for each lesson: target row metadata + content_transfer
     block + source block (the AQA content) or null

Idempotent: overwrites files. Reads only — no Supabase writes.

Run from repo root:
    python scripts/_content_sociology-eduqas/_prep_fetch.py
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
PLAN_PATH = SCRIPTS_DIR / "_plan_sociology-eduqas.json"

OUT_DIR.mkdir(exist_ok=True)
(OUT_DIR / "lessons").mkdir(exist_ok=True)

sb = get_client()
plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))


# ============================================================ Resolve subjects
print("=== Resolving Supabase target + source subjects ===\n")

target_subject = (
    sb.table("subjects")
    .select("id, slug, name")
    .eq("slug", "sociology-eduqas")
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
    .eq("slug", "sociology-aqa")
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
print(
    f"  target units: {len(target_units)}, target lessons: {len(target_lesson_map)}"
)


# ============================================================ Source unit + lesson maps
source_units = (
    sb.table("units")
    .select("id, slug, name")
    .eq("subject_id", SOURCE_SUBJECT_ID)
    .execute()
    .data
)
source_unit_by_slug = {u["slug"]: u for u in source_units}
print(f"  source AQA units: {[u['slug'] for u in source_units]}\n")


SOURCE_FIELDS = (
    "id, lesson_number, slug, title, description, "
    "content_html, exam_tip_html, conclusion_html, "
    "practice_questions, knowledge_checks, flashcard_questions, "
    "glossary_terms, hero_image_caption"
)


def fetch_source_lesson(unit_slug, lesson_number):
    if unit_slug not in source_unit_by_slug:
        return None, f"source unit {unit_slug} not found"
    uid = source_unit_by_slug[unit_slug]["id"]
    res = (
        sb.table("lessons")
        .select(SOURCE_FIELDS)
        .eq("unit_id", uid)
        .eq("lesson_number", lesson_number)
        .execute()
        .data
    )
    if not res:
        return None, f"source lesson {unit_slug}/L{lesson_number} not found"
    return res[0], None


# ============================================================ Batch JSONs

# Map plan unit slug -> short batch_id
UNIT_BATCH_IDS = {
    "cultural-transmission-research-methods": "u1_methods",
    "families": "u2_families",
    "education": "u3_education",
    "social-differentiation-stratification": "u4_stratification",
    "crime-deviance": "u5_crime",
}

SUBJECT_META = {
    "name": plan["subject"]["name"],
    "slug": plan["subject"]["slug"],
    "exam_board": plan["subject"]["exam_board"],
    "spec_codes": plan["subject"]["spec_codes"],
    "target_audience": plan["subject"]["target_audience"],
    "subject_id": TARGET_SUBJECT_ID,
    "subject_type": plan["subject"]["subject_type"],
    "twin_build_note": plan["subject"]["twin_build_note"],
}

REGISTERED_QUESTION_TYPES = plan["question_type_names"]

# quote_ticker_html — render the plan's quotes into the AQA-batch shape
quote_blocks = []
for q in plan.get("quote_ticker_quotes", []):
    quote_text = q["quote"].replace("‘", "&lsquo;").replace("’", "&rsquo;")
    quote_text = quote_text.replace("“", "&ldquo;").replace("”", "&rdquo;")
    quote_blocks.append(
        f"<blockquote>&ldquo;{quote_text}&rdquo; "
        f"<cite>&mdash; {q['author']}</cite></blockquote>"
    )
QUOTE_TICKER_HTML = "\n".join(quote_blocks)

SHARED = {
    "spec_slice_path": "specs/eduqas/sociology-C200QS.md",
    "reference_lesson_path": "scripts/_content_sociology-aqa/_reference_lesson.json",
    "agent_prompt_path": "scripts/_content_sociology-eduqas/_AGENT_PROMPT.md",
    "schema_path": "docs/CONTENT_PROMPT.md",
    "subject_level_teaching_brief": plan["teaching_brief"],
    "unit_level_teaching_brief": {},
    "quote_ticker_html_for_unit": QUOTE_TICKER_HTML,
    "registered_question_type_names": REGISTERED_QUESTION_TYPES,
    "allowed_question_types_for_this_unit": REGISTERED_QUESTION_TYPES,
    "named_sociologist_deltas": plan["named_sociologist_deltas"],
    "unique_to_target": plan["unique_to_target"],
    "unique_to_source": plan["unique_to_source"],
    "output_dir": "scripts/_content_sociology-eduqas/lessons",
}


print("=== Building batch JSONs (one per unit) ===\n")
batches_written = []
batch_breakdown = {}
unmatched_targets = []  # plan lessons with no Supabase row
unmatched_sources = []  # AQA lookups that returned no row
fresh_lessons = []  # transfer_score == "fresh" lessons
counts_by_score = {"high": 0, "medium": 0, "low": 0, "fresh": 0}

for unit in plan["article_units"]:
    bid = UNIT_BATCH_IDS[unit["slug"]]
    lessons_in_batch = []
    for L in unit["lessons"]:
        key = (unit["slug"], L["number"])
        if key not in target_lesson_map:
            unmatched_targets.append(f"{unit['slug']}/L{L['number']}")
            print(
                f"  WARNING: target lesson {unit['slug']}/L{L['number']} "
                f"not in Supabase — SKIP"
            )
            continue
        target_row = target_lesson_map[key]

        ct = L["content_transfer"]
        score = ct.get("transfer_score", "fresh")
        counts_by_score[score] = counts_by_score.get(score, 0) + 1

        # Build the source block (AQA content) for non-fresh lessons
        source_block = None
        if score == "fresh":
            fresh_lessons.append(
                f"{unit['slug']}/L{L['number']} ({L['title']})"
            )
            source_block = {
                "_note": (
                    "No AQA source — this lesson is unique to Eduqas/WJEC. "
                    "Build fresh from the spec slice + general GCSE "
                    "Sociology knowledge consistent with the Eduqas/WJEC "
                    "spec. See content_transfer.adaptation_notes."
                ),
                "transfer_score": "fresh",
            }
        else:
            src_unit = ct["source_unit_slug"]
            src_num = ct["source_lesson_number"]
            src, err = fetch_source_lesson(src_unit, src_num)
            if err:
                unmatched_sources.append(
                    f"{unit['slug']}/L{L['number']} -> aqa "
                    f"{src_unit}/L{src_num} ({err})"
                )
                print(
                    f"  [MISS]  {unit['slug']}/L{L['number']:02d}  -> "
                    f"aqa {src_unit}/L{src_num}  ({err})"
                )
                source_block = {
                    "_note": (
                        f"AQA source lookup FAILED: {err}. "
                        "Treat as fresh build per spec slice."
                    ),
                    "transfer_score": score,
                    "lookup_failed": True,
                }
            else:
                source_block = {
                    "_source_meta": {
                        "source_subject_slug": "sociology-aqa",
                        "source_unit_slug": src_unit,
                        "source_lesson_number": src_num,
                        "source_lesson_id": src["id"],
                        "source_lesson_title": src["title"],
                    },
                    "transfer_score": score,
                    "content_html": src.get("content_html"),
                    "exam_tip_html": src.get("exam_tip_html"),
                    "conclusion_html": src.get("conclusion_html"),
                    "practice_questions": src.get("practice_questions") or [],
                    "knowledge_checks": src.get("knowledge_checks") or [],
                    "flashcard_questions": src.get("flashcard_questions") or [],
                    "glossary_terms": src.get("glossary_terms") or [],
                    "hero_image_caption": src.get("hero_image_caption"),
                }
                print(
                    f"  [{score:6s}] {unit['slug']}/L{L['number']:02d}  -> "
                    f"aqa {src_unit}/L{src_num}  ({src['title']})"
                )

        suggested_qts = REGISTERED_QUESTION_TYPES  # all 6 allowed each lesson

        lessons_in_batch.append(
            {
                "lesson_id": target_row["id"],
                "lesson_number": L["number"],
                "slug": target_row["slug"],
                "title": L["title"],
                "description": L["description"],
                "spec_references": L["spec_references"],
                "section_markers": L["section_markers"],
                "suggested_question_types": suggested_qts,
                "content_transfer": ct,
                "source": source_block,
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
    batch_path.write_text(
        json.dumps(batch, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    batches_written.append(batch_path.name)
    batch_breakdown[bid] = {
        "unit_slug": unit["slug"],
        "unit_name": unit["name"],
        "lesson_count": len(lessons_in_batch),
    }
    size_kb = batch_path.stat().st_size / 1024
    print(
        f"  {batch_path.name}  ->  {len(lessons_in_batch)} lessons  "
        f"({size_kb:,.1f} KB)"
    )


print("\n=== DONE ===")
summary = {
    "transfer_score_counts": counts_by_score,
    "batches_written": batches_written,
    "batch_breakdown": batch_breakdown,
    "unmatched_target_lessons": unmatched_targets,
    "unmatched_source_lookups": unmatched_sources,
    "fresh_lessons (no AQA source by design)": fresh_lessons,
}
print(json.dumps(summary, indent=2, ensure_ascii=False))
