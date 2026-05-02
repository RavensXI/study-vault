"""Clone Unity Spanish / French / German practice subjects to the free tier.

Unity has practice-first language subjects (school_id = Unity, slugs:
spanish / french / german). Free tier currently has none. This script:
  1. Clones each subject row with school_id=NULL, slug + '-aqa' suffix
  2. Clones all units under each new subject
  3. Clones all lessons under each new unit, preserving every field
     (practice_data, related_media, narration_manifest, etc.)
  4. Audio URLs (R2) and hero image URLs are reused as-is — no re-upload

Idempotent: skips a free-tier subject if its target slug already exists.

Usage:
    python scripts/_migrate_languages_to_free.py
    python scripts/_migrate_languages_to_free.py --dry-run
    python scripts/_migrate_languages_to_free.py --only spanish
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

# Source slug -> target slug
TARGETS = {
    "spanish": "spanish-aqa",
    "french": "french-aqa",
    "german": "german-aqa",
}

# Subject row columns to clone (excluding id / school_id / slug / created_at / updated_at)
SUBJECT_CLONE_COLS = [
    "name", "exam_board", "spec_code", "color", "image_url", "status",
    "is_active", "sort_order", "settings",
]
# Unit row columns
UNIT_CLONE_COLS = [
    "slug", "name", "subtitle", "body_class", "accent", "accent_light",
    "accent_badge", "lesson_count", "sort_order", "image_url",
]
# Lesson row columns — clone EVERYTHING that the practice loader / lesson
# loader cares about. Excludes: id, unit_id, created_at, updated_at, status_changed_by,
# approved_at, reviewed_at, reviewed_by, published_at, published_by, rejection_notes,
# enrichment_started_at, enrichment_completed_at, enrichment_error, source_ppt_hash.
LESSON_CLONE_COLS = [
    "lesson_number", "slug", "title", "description",
    "content_html", "exam_tip_html", "conclusion_html",
    "practice_data", "practice_questions", "knowledge_checks",
    "flashcard_questions", "glossary_terms", "diagrams", "related_media",
    "narration_manifest", "youtube_video_id",
    "hero_image_url", "hero_image_alt", "hero_image_caption", "hero_image_position",
    "tier", "status",
]


def clone_subject(sb, source_slug, target_slug, dry_run):
    # Find Unity school
    schools = sb.table("schools").select("id").ilike("slug", "%unity%").execute().data
    if not schools:
        raise RuntimeError("Unity school not found")
    unity_id = schools[0]["id"]

    # Pull source subject (Unity-scoped)
    source = (
        sb.table("subjects")
        .select("*")
        .eq("slug", source_slug)
        .eq("school_id", unity_id)
        .execute()
        .data
    )
    if not source:
        raise RuntimeError(f"Source subject {source_slug} (Unity) not found")
    source = source[0]
    print(f"  Source: {source['id'][:8]}  {source_slug}  ({source['name']})")

    # Check target doesn't already exist
    existing = (
        sb.table("subjects")
        .select("id")
        .eq("slug", target_slug)
        .is_("school_id", "null")
        .execute()
        .data
    )
    if existing:
        print(f"  [SKIP] target {target_slug} (free) already exists at {existing[0]['id'][:8]}")
        return existing[0]["id"]

    # Clone subject row
    payload = {k: source.get(k) for k in SUBJECT_CLONE_COLS}
    payload["slug"] = target_slug
    payload["school_id"] = None
    if dry_run:
        print(f"  [DRY] would create subject {target_slug} (free)")
        return None
    new_subj = sb.table("subjects").insert(payload).execute().data[0]
    print(f"  Created: {new_subj['id'][:8]}  {target_slug}")
    return new_subj["id"]


def clone_units_and_lessons(sb, source_subject_id, target_subject_id, dry_run):
    units = (
        sb.table("units")
        .select("*")
        .eq("subject_id", source_subject_id)
        .order("sort_order")
        .execute()
        .data
    )
    print(f"  {len(units)} units to clone")

    total_lessons = 0
    for u in units:
        unit_payload = {k: u.get(k) for k in UNIT_CLONE_COLS}
        unit_payload["subject_id"] = target_subject_id
        if dry_run:
            print(f"    [DRY] unit {u['slug']:35s}  ({u.get('lesson_count')} lessons)")
            new_unit_id = None
        else:
            new_unit = sb.table("units").insert(unit_payload).execute().data[0]
            new_unit_id = new_unit["id"]
            print(f"    [OK]  unit {u['slug']:35s}  -> {new_unit_id[:8]}")

        # Clone lessons
        lessons = (
            sb.table("lessons")
            .select("*")
            .eq("unit_id", u["id"])
            .order("lesson_number")
            .execute()
            .data
        )
        if dry_run:
            print(f"          [DRY] would clone {len(lessons)} lessons")
            total_lessons += len(lessons)
            continue

        # Insert in batches to keep payloads sensible
        BATCH = 10
        for i in range(0, len(lessons), BATCH):
            batch_payloads = []
            for L in lessons[i:i + BATCH]:
                p = {k: L.get(k) for k in LESSON_CLONE_COLS}
                p["unit_id"] = new_unit_id
                batch_payloads.append(p)
            sb.table("lessons").insert(batch_payloads).execute()
        total_lessons += len(lessons)
        print(f"          cloned {len(lessons)} lessons")

    return total_lessons


def delete_existing_target(sb, target_slug):
    """Bottom-up delete of any existing free-tier subject with this slug.
    Clears child references in content_pipeline_logs / lesson_visits /
    knowledge_check_scores first to avoid FK constraint violations."""
    rows = (
        sb.table("subjects")
        .select("id")
        .eq("slug", target_slug)
        .is_("school_id", "null")
        .execute()
        .data
    )
    if not rows:
        return False
    subject_id = rows[0]["id"]
    units = sb.table("units").select("id").eq("subject_id", subject_id).execute().data
    unit_ids = [u["id"] for u in units]
    # Collect lesson ids first
    lesson_ids = []
    for uid in unit_ids:
        lessons = sb.table("lessons").select("id").eq("unit_id", uid).execute().data
        lesson_ids.extend([L["id"] for L in lessons])
    # Clear FK-bearing child rows (defensive: try each, ignore "table does not exist")
    for child_table in ("content_pipeline_logs", "lesson_visits", "knowledge_check_scores"):
        for lid in lesson_ids:
            try:
                sb.table(child_table).delete().eq("lesson_id", lid).execute()
            except Exception:
                # Table may not exist or no rows; safe to ignore
                pass
    # Now bottom-up delete
    for uid in unit_ids:
        sb.table("lessons").delete().eq("unit_id", uid).execute()
    sb.table("units").delete().eq("subject_id", subject_id).execute()
    sb.table("subjects").delete().eq("id", subject_id).execute()
    print(f"  [DELETED] stale free-tier {target_slug} ({subject_id[:8]}, {len(unit_ids)} units, {len(lesson_ids)} lessons + child refs)")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--only", choices=list(TARGETS.keys()), help="Only clone one language")
    parser.add_argument("--force", action="store_true", help="Delete + re-clone if free-tier target already exists")
    args = parser.parse_args()

    sb = get_client()
    targets = {args.only: TARGETS[args.only]} if args.only else TARGETS

    total_subjects = 0
    total_units = 0
    total_lessons = 0
    for source_slug, target_slug in targets.items():
        print(f"\n=== {source_slug} -> {target_slug} ===")
        # Source subject
        schools = sb.table("schools").select("id").ilike("slug", "%unity%").execute().data
        unity_id = schools[0]["id"]
        source = (
            sb.table("subjects")
            .select("id")
            .eq("slug", source_slug)
            .eq("school_id", unity_id)
            .execute()
            .data
        )
        if not source:
            print(f"  [ERR] source {source_slug} not found")
            continue
        source_id = source[0]["id"]

        # Force-mode: nuke any existing free-tier target before cloning
        if args.force and not args.dry_run:
            delete_existing_target(sb, target_slug)

        target_id = clone_subject(sb, source_slug, target_slug, args.dry_run)
        if target_id is None and args.dry_run:
            # Dry run: show units we'd clone using source subject_id with notional target
            n = clone_units_and_lessons(sb, source_id, "(dry)", args.dry_run)
            total_lessons += n
            total_subjects += 1
            continue

        if target_id is None:
            continue

        # Skip cloning units if target already had units (means a prior partial run)
        existing_units = (
            sb.table("units")
            .select("id", count="exact")
            .eq("subject_id", target_id)
            .execute()
        )
        if (existing_units.count or 0) > 0:
            print(f"  [SKIP] target subject already has {existing_units.count} units; not re-cloning (use --force to wipe and re-clone)")
            continue

        n_lessons = clone_units_and_lessons(sb, source_id, target_id, args.dry_run)
        total_subjects += 1
        total_lessons += n_lessons

    print(f"\n=== Summary ===")
    print(f"  Subjects cloned: {total_subjects}")
    print(f"  Lessons cloned: {total_lessons}")


if __name__ == "__main__":
    main()
