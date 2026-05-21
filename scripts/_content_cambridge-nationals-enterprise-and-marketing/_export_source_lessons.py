"""Export source business-edexcel lessons used as port basis for R067.

Reads the plan, pulls each content_transfer.source_subject_slug /
source_unit_slug / source_lesson_number tuple, dumps the full lesson row
to scripts/_content_cambridge-nationals-enterprise-and-marketing/_source_lessons/{NN}.json
so the Phase 3 content agents have everything offline.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.supabase_client import get_client

sb = get_client()
here = Path(__file__).resolve().parent
plan = json.loads(
    (here.parent / "_plan_cambridge-nationals-enterprise-and-marketing.json").read_text(encoding="utf-8")
)

source_dir = here / "_source_lessons"
source_dir.mkdir(exist_ok=True)

# Cache lesson rows by (subject_slug, unit_slug, lesson_number) to dedupe.
to_fetch = []
for unit in plan["article_units"]:
    for L in unit["lessons"]:
        ct = L.get("content_transfer") or {}
        if not ct.get("source_subject_slug"):
            continue
        to_fetch.append({
            "lesson_number_in_plan": L["number"],
            "title_in_plan": L["title"],
            "source_subject_slug": ct["source_subject_slug"],
            "source_unit_slug": ct["source_unit_slug"],
            "source_lesson_number": ct["source_lesson_number"],
            "transfer_score": ct["transfer_score"],
            "adaptation_notes": ct["adaptation_notes"],
        })

print(f"=== Exporting {len(to_fetch)} source lessons ===\n")

# Pre-resolve subject_id and unit_id.
unique_subj = set((p["source_subject_slug"]) for p in to_fetch)
unique_unit = set((p["source_subject_slug"], p["source_unit_slug"]) for p in to_fetch)

subj_rows = (
    sb.table("subjects")
    .select("id, slug")
    .in_("slug", list(unique_subj))
    .is_("school_id", "null")
    .execute()
    .data
)
subj_id_by_slug = {r["slug"]: r["id"] for r in subj_rows}

unit_id_by_pair = {}
for subj_slug, unit_slug in unique_unit:
    rows = (
        sb.table("units")
        .select("id, slug, subject_id")
        .eq("slug", unit_slug)
        .eq("subject_id", subj_id_by_slug[subj_slug])
        .execute()
        .data
    )
    if rows:
        unit_id_by_pair[(subj_slug, unit_slug)] = rows[0]["id"]
    else:
        print(f"  WARN: no unit row for {subj_slug}/{unit_slug}")

# Pull each source lesson.
exported = 0
for p in to_fetch:
    pair = (p["source_subject_slug"], p["source_unit_slug"])
    unit_id = unit_id_by_pair.get(pair)
    if not unit_id:
        print(f"  L{p['lesson_number_in_plan']:02d} SKIP — no unit_id for {pair}")
        continue
    rows = (
        sb.table("lessons")
        .select(
            "id, lesson_number, slug, title, description, content_html, "
            "exam_tip_html, conclusion_html, practice_questions, knowledge_checks, "
            "flashcard_questions, glossary_terms, narration_manifest"
        )
        .eq("unit_id", unit_id)
        .eq("lesson_number", p["source_lesson_number"])
        .execute()
        .data
    )
    if not rows:
        print(
            f"  L{p['lesson_number_in_plan']:02d} SKIP — no source lesson at "
            f"{pair} #{p['source_lesson_number']}"
        )
        continue
    src = rows[0]
    payload = {
        "_export_meta": {
            "plan_lesson_number": p["lesson_number_in_plan"],
            "plan_lesson_title": p["title_in_plan"],
            "source_subject_slug": p["source_subject_slug"],
            "source_unit_slug": p["source_unit_slug"],
            "source_lesson_number": p["source_lesson_number"],
            "transfer_score": p["transfer_score"],
            "adaptation_notes": p["adaptation_notes"],
        },
        "source_lesson": src,
    }
    out_path = source_dir / f"{p['lesson_number_in_plan']:02d}.json"
    out_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(
        f"  L{p['lesson_number_in_plan']:02d} OK   - "
        f"{p['source_subject_slug']}/{p['source_unit_slug']}#{p['source_lesson_number']} "
        f"({p['transfer_score']}) -> {out_path.name}"
    )
    exported += 1

print(f"\n  Exported {exported} of {len(to_fetch)} source lessons")
