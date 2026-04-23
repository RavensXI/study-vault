"""
Generic insert script for practice-format lessons (languages, Maths, Eng Lang, etc.).

Reads JSON files with a `_meta` block and `practice_data` object, updates the
matching lesson row in Supabase. Unlike article format, practice lessons store
all content in the `practice_data` JSONB column — no content_html, exam_tip_html, etc.

Usage:
  python scripts/_insert_practice_lessons.py scripts/_gen_french/
  python scripts/_insert_practice_lessons.py scripts/_gen_french/ --dry-run

Each JSON must have:
  _meta: { subject_slug, exam_board, school_id, unit_slug, lesson_number }
  practice_data: { method_card, exam_context, worked_examples, problem_bank, ai_marking_prompts }
"""
import sys, os, json, argparse, glob

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.supabase_client import get_client


def validate_practice_data(pd, lesson_id_for_log):
    """Basic structural sanity check. Returns list of violations."""
    violations = []
    if not isinstance(pd, dict):
        return [f"{lesson_id_for_log}: practice_data is not a dict"]
    mc = pd.get("method_card") or {}
    if not mc.get("content"):
        violations.append(f"{lesson_id_for_log}: method_card.content missing")
    pb = pd.get("problem_bank") or {}
    if not pb.get("bronze") or not pb.get("silver") or not pb.get("gold"):
        violations.append(f"{lesson_id_for_log}: incomplete problem_bank tiers")
    total = len(pb.get("bronze", [])) + len(pb.get("silver", [])) + len(pb.get("gold", []))
    if total < 15 or total > 25:
        violations.append(f"{lesson_id_for_log}: problem_bank total {total} (want ~20)")
    for tier in ["bronze", "silver", "gold"]:
        for i, p in enumerate(pb.get(tier, [])):
            if not p.get("input_type"):
                violations.append(f"{lesson_id_for_log}: {tier}[{i}] missing input_type")
    return violations


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--allow-partial", action="store_true")
    args = parser.parse_args()

    sb = get_client()
    paths = sorted(glob.glob(os.path.join(args.directory, "*.json")))
    if not paths:
        print(f"No JSONs in {args.directory}")
        sys.exit(1)

    print(f"Found {len(paths)} JSON files")

    updated = 0
    subject_ids_touched = set()
    all_unit_slugs = {}  # subject_id → set of unit_slugs

    for p in paths:
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)

        meta = data.get("_meta") or {}
        if not meta:
            print(f"  [SKIP] {os.path.basename(p)}: no _meta block")
            continue

        subject_slug = meta["subject_slug"]
        unit_slug = meta["unit_slug"]
        lesson_number = meta["lesson_number"]
        school_id = meta.get("school_id")
        exam_board = meta.get("exam_board")

        pd = data.get("practice_data")
        if pd is None:
            print(f"  [ERROR] {os.path.basename(p)}: no practice_data")
            continue

        # Validate
        violations = validate_practice_data(pd, os.path.basename(p))
        if violations and not args.allow_partial:
            for v in violations:
                print(f"  [INVALID] {v}")
            continue
        elif violations:
            for v in violations:
                print(f"  [WARN] {v}")

        # Find subject
        q = sb.table("subjects").select("id").eq("slug", subject_slug)
        if exam_board:
            q = q.eq("exam_board", exam_board)
        if school_id is None:
            q = q.is_("school_id", "null")
        else:
            q = q.eq("school_id", school_id)
        subj = q.execute().data
        if not subj:
            print(f"  [ERROR] {os.path.basename(p)}: subject {subject_slug} ({exam_board}) not found")
            continue
        sid = subj[0]["id"]
        subject_ids_touched.add(sid)
        all_unit_slugs.setdefault(sid, set()).add(unit_slug)

        # Find unit
        unit = sb.table("units").select("id").eq("subject_id", sid).eq("slug", unit_slug).execute().data
        if not unit:
            print(f"  [ERROR] {os.path.basename(p)}: unit {unit_slug} not found")
            continue
        uid = unit[0]["id"]

        # Find lesson
        lesson = sb.table("lessons").select("id,title").eq("unit_id", uid).eq("lesson_number", lesson_number).execute().data
        if not lesson:
            print(f"  [ERROR] {os.path.basename(p)}: lesson {lesson_number} in {unit_slug} not found")
            continue
        lid = lesson[0]["id"]
        title = lesson[0]["title"]

        if args.dry_run:
            pb = pd.get("problem_bank", {})
            b = len(pb.get("bronze", []))
            s = len(pb.get("silver", []))
            g = len(pb.get("gold", []))
            print(f"  [DRY] L{lesson_number:02d} {title[:45]:45s} ({b}B/{s}S/{g}G)")
        else:
            sb.table("lessons").update({"practice_data": pd}).eq("id", lid).execute()
            updated += 1
            print(f"  [OK] L{lesson_number:02d} {title[:50]}")

    if not args.dry_run:
        print(f"\n[DONE] Updated {updated} practice lessons.")
        # Ensure practice_units is set on subjects.settings
        for sid in subject_ids_touched:
            unit_slugs = sorted(all_unit_slugs[sid])
            settings_result = sb.table("subjects").select("settings").eq("id", sid).execute().data
            settings = (settings_result[0]["settings"] if settings_result else {}) or {}
            if isinstance(settings, str):
                try:
                    settings = json.loads(settings)
                except Exception:
                    settings = {}
            settings["practice_units"] = sorted(set((settings.get("practice_units") or []) + unit_slugs))
            sb.table("subjects").update({"settings": settings}).eq("id", sid).execute()
            print(f"  [settings] subject {sid}: practice_units = {settings['practice_units']}")


if __name__ == "__main__":
    main()
