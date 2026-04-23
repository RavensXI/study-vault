"""
Helper for cross-board builds: given a plan with content_transfer blocks,
fetch the full content JSON of each source lesson from Supabase and write it
to per-lesson files that the content agents can read.

Output: one JSON per target lesson at scripts/_source_content/{target_unit}_{target_num}.json
Each file contains: content_html, exam_tip_html, conclusion_html, glossary_terms,
flashcard_questions, knowledge_checks from the SOURCE lesson.

Practice questions are NOT included — always regenerated for target board.
"""
import sys, os, json, argparse
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.supabase_client import get_client


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("plan_path")
    parser.add_argument("--out-dir", default="scripts/_source_content")
    args = parser.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    sb = get_client()

    with open(args.plan_path, "r", encoding="utf-8") as f:
        plan = json.load(f)

    all_units = (plan.get("article_units") or []) + (plan.get("practice_units") or [])

    fetched = 0
    skipped_fresh = 0
    skipped_low = 0

    for unit in all_units:
        for lesson in unit.get("lessons", []):
            ct = lesson.get("content_transfer") or {}
            score = ct.get("transfer_score")

            if score in (None, "fresh"):
                skipped_fresh += 1
                continue
            if score == "low":
                # Low means tone reference only, agent generates fresh — no content needed
                skipped_low += 1
                continue

            source_slug = ct.get("source_subject_slug")
            source_unit_slug = ct.get("source_unit_slug")
            source_lesson_num = ct.get("source_lesson_number")
            if not (source_slug and source_unit_slug and source_lesson_num):
                print(f"  [SKIP] {unit['slug']}/L{lesson['number']}: incomplete content_transfer block")
                continue

            # Look up source lesson
            source_subj = sb.table("subjects").select("id").eq("slug", source_slug).execute().data
            if not source_subj:
                print(f"  [ERR] source subject {source_slug} not found")
                continue
            source_unit = (
                sb.table("units")
                .select("id")
                .eq("subject_id", source_subj[0]["id"])
                .eq("slug", source_unit_slug)
                .execute()
                .data
            )
            if not source_unit:
                print(f"  [ERR] source unit {source_slug}/{source_unit_slug} not found")
                continue
            source_lesson = (
                sb.table("lessons")
                .select("title,content_html,exam_tip_html,conclusion_html,glossary_terms,flashcard_questions,knowledge_checks")
                .eq("unit_id", source_unit[0]["id"])
                .eq("lesson_number", source_lesson_num)
                .single()
                .execute()
                .data
            )

            target_path = os.path.join(
                args.out_dir, f"{unit['slug']}_L{lesson['number']:02d}.json"
            )
            with open(target_path, "w", encoding="utf-8") as f:
                json.dump({
                    "_source_meta": {
                        "source_subject_slug": source_slug,
                        "source_unit_slug": source_unit_slug,
                        "source_lesson_number": source_lesson_num,
                        "source_lesson_title": source_lesson["title"],
                        "transfer_score": score,
                        "adaptation_notes": ct.get("adaptation_notes", ""),
                    },
                    "content_html": source_lesson.get("content_html") or "",
                    "exam_tip_html": source_lesson.get("exam_tip_html") or "",
                    "conclusion_html": source_lesson.get("conclusion_html") or "",
                    "glossary_terms": source_lesson.get("glossary_terms") or [],
                    "flashcard_questions": source_lesson.get("flashcard_questions") or [],
                    "knowledge_checks": source_lesson.get("knowledge_checks") or [],
                }, f, indent=2, ensure_ascii=False)
            fetched += 1
            print(f"  [{score:6s}] {unit['slug']}/L{lesson['number']:02d}: {source_lesson['title']} → {os.path.basename(target_path)}")

    print(f"\n[DONE] Fetched {fetched} source lessons. Skipped {skipped_fresh} fresh + {skipped_low} low.")


if __name__ == "__main__":
    main()
