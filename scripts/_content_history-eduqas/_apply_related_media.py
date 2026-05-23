"""Patch related_media into Supabase from local lesson JSONs.

Run after the related-media curation agents have written to lessons/*.json.
"""
import argparse
import glob
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.supabase_client import get_client

SUBJECT_SLUG = "history-eduqas"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    sb = get_client()
    here = Path(__file__).resolve().parent
    lessons_dir = here / "lessons"
    subj = (
        sb.table("subjects")
        .select("id")
        .eq("slug", SUBJECT_SLUG)
        .is_("school_id", "null")
        .execute()
        .data
    )
    if not subj:
        print(f"ERROR: subject '{SUBJECT_SLUG}' not found")
        sys.exit(1)
    subject_id = subj[0]["id"]

    units = sb.table("units").select("id, slug").eq("subject_id", subject_id).execute().data
    unit_id_by_slug = {u["slug"]: u["id"] for u in units}
    lessons = (
        sb.table("lessons")
        .select("id, lesson_number, unit_id")
        .in_("unit_id", list(unit_id_by_slug.values()))
        .execute()
        .data
    )
    unit_slug_by_id = {v: k for k, v in unit_id_by_slug.items()}
    lesson_id_by_pair = {
        (unit_slug_by_id[L["unit_id"]], L["lesson_number"]): L["id"] for L in lessons
    }

    ok = fail = skip = 0
    for p in sorted(lessons_dir.glob("*.json")):
        data = json.loads(p.read_text(encoding="utf-8"))
        rm = data.get("related_media")
        if not rm:
            print(f"  [SKIP] {p.name} - no related_media")
            skip += 1
            continue
        lid = lesson_id_by_pair.get((data.get("_unit_slug"), data.get("_lesson_number")))
        if not lid:
            print(f"  [SKIP] {p.name} - no shell match")
            skip += 1
            continue
        if args.dry_run:
            print(f"  [DRY]  L{data['_lesson_number']:02d} {p.name:55s} -> {lid[:8]}  ({len(rm)} categories)")
            ok += 1
        else:
            sb.table("lessons").update({"related_media": rm}).eq("id", lid).execute()
            print(f"  [OK]   L{data['_lesson_number']:02d} {p.name:55s} -> {lid[:8]}  ({len(rm)} categories)")
            ok += 1

    print(f"\nOK={ok} FAIL={fail} SKIP={skip}")


if __name__ == "__main__":
    main()
