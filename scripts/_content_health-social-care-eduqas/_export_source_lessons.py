"""Export source lessons referenced as content_transfer in the HSC Eduqas/WJEC plan.

Sources: health-social-care-edexcel and health-social-care-ocr free-tier rows.
Output: _source_lessons/{NN}.json where NN is the plan lesson number (across both units).
"""
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.supabase_client import get_client

sb = get_client()
here = Path(__file__).resolve().parent
plan = json.loads(
    (here.parent / "_plan_health-social-care-eduqas.json").read_text(encoding="utf-8")
)

source_dir = here / "_source_lessons"
source_dir.mkdir(exist_ok=True)

# Walk all lessons across both units, assign a global lesson_idx
to_fetch = []
global_idx = 0
for unit in plan["article_units"]:
    for L in unit["lessons"]:
        global_idx += 1
        ct = L.get("content_transfer") or {}
        if not ct.get("source_subject_slug") or ct.get("source_lesson_number") is None:
            continue
        to_fetch.append({
            "global_idx": global_idx,
            "unit_in_target": unit["slug"],
            "lesson_in_target": L["number"],
            "title_in_target": L["title"],
            "source_subject_slug": ct["source_subject_slug"],
            "source_unit_slug": ct.get("source_unit_slug"),
            "source_lesson_number": ct["source_lesson_number"],
            "transfer_score": ct["transfer_score"],
            "adaptation_notes": ct.get("adaptation_notes", ""),
        })

print(f"=== Exporting {len(to_fetch)} source lessons ===\n")

# Pre-resolve subject_id and unit_id where source_unit_slug is given.
unique_subj = {p["source_subject_slug"] for p in to_fetch}
subj_rows = sb.table("subjects").select("id, slug").in_("slug", list(unique_subj)).is_("school_id", "null").execute().data
subj_id_by_slug = {r["slug"]: r["id"] for r in subj_rows}

exported = 0
for p in to_fetch:
    sid = subj_id_by_slug.get(p["source_subject_slug"])
    if not sid:
        print(f"  G{p['global_idx']:02d} SKIP - no subject row for {p['source_subject_slug']}")
        continue
    # If source_unit_slug given, scope to that unit; else search across all units of the source subject.
    if p.get("source_unit_slug"):
        units = sb.table("units").select("id").eq("subject_id", sid).eq("slug", p["source_unit_slug"]).execute().data
        unit_ids = [u["id"] for u in units]
    else:
        units = sb.table("units").select("id").eq("subject_id", sid).execute().data
        unit_ids = [u["id"] for u in units]
    if not unit_ids:
        print(f"  G{p['global_idx']:02d} SKIP - no units in source subject")
        continue
    rows = sb.table("lessons").select(
        "id, lesson_number, slug, title, description, content_html, exam_tip_html, conclusion_html, "
        "practice_questions, knowledge_checks, flashcard_questions, glossary_terms"
    ).in_("unit_id", unit_ids).eq("lesson_number", p["source_lesson_number"]).execute().data
    if not rows:
        print(f"  G{p['global_idx']:02d} SKIP - no source lesson at {p['source_subject_slug']}#{p['source_lesson_number']}")
        continue
    src = rows[0]
    payload = {
        "_export_meta": {
            "target_unit": p["unit_in_target"],
            "target_lesson_number": p["lesson_in_target"],
            "target_lesson_title": p["title_in_target"],
            "source_subject_slug": p["source_subject_slug"],
            "source_lesson_number": p["source_lesson_number"],
            "transfer_score": p["transfer_score"],
            "adaptation_notes": p["adaptation_notes"],
        },
        "source_lesson": src,
    }
    out_path = source_dir / f"{p['global_idx']:02d}.json"
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(
        f"  G{p['global_idx']:02d} OK   - {p['source_subject_slug']}#{p['source_lesson_number']} "
        f"({p['transfer_score']}) -> {out_path.name}"
    )
    exported += 1

print(f"\n  Exported {exported} of {len(to_fetch)} source lessons")
