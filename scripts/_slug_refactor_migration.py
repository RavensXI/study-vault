"""Slug refactor — Supabase migration.

Renames free-tier subject slugs for consistency (every free-tier subject
ends with -{board}) and renames two Unity bespoke slugs for spec accuracy.

Slug is just a string column — no FK relations reference it; all FKs go via
subject.id. Safe to UPDATE in place.

Usage:
  python scripts/_slug_refactor_migration.py --dry-run
  python scripts/_slug_refactor_migration.py --apply
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

sb = get_client()

# Free-tier renames (school_id IS NULL). Format: (old_slug, new_slug, optional new_name)
FREE_TIER_RENAMES = [
    ("english-language",    "english-language-aqa",        None),
    ("english-literature",  "english-literature-aqa",      None),
    ("maths",               "maths-edexcel",               None),
    ("science",             "science-aqa",                 None),
    ("religious-education", "religious-studies-aqa",       "Religious Studies"),
    ("geography",           "geography-aqa",               None),
    ("health-social-care",  "health-social-care-edexcel",  None),
]

# Unity bespoke renames. Match by (slug, school_name) so we don't risk
# touching another school that shares a slug.
UNITY_RENAMES = [
    ("religious-education", "religious-studies",            None),
    ("food-technology",     "food-preparation-and-nutrition", None),
]
UNITY_SCHOOL_NAME = "Unity College"


def find_unity_school_id():
    rows = sb.table("schools").select("id, name").ilike("name", f"%Unity%").execute().data
    if not rows:
        raise SystemExit("ABORT: Unity school not found in schools table")
    if len(rows) > 1:
        # Pick exact match
        exact = [r for r in rows if r["name"].lower() == UNITY_SCHOOL_NAME.lower() or "unity college" in r["name"].lower()]
        if len(exact) == 1:
            return exact[0]["id"]
        raise SystemExit(f"ABORT: multiple Unity schools found, need to disambiguate: {rows}")
    return rows[0]["id"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Actually apply changes (default is dry-run)")
    ap.add_argument("--dry-run", action="store_true", help="Audit only, no writes")
    args = ap.parse_args()

    if not (args.apply or args.dry_run):
        ap.error("Specify --apply or --dry-run")

    DRY = not args.apply
    print(f"=== Slug refactor migration ({'DRY RUN' if DRY else 'APPLYING'}) ===\n")

    unity_id = find_unity_school_id()
    print(f"Unity school_id: {unity_id}\n")

    # === Free-tier renames ===
    print("--- Free-tier (school_id IS NULL) ---")
    for old_slug, new_slug, new_name in FREE_TIER_RENAMES:
        rows = sb.table("subjects").select("id, slug, name, school_id").eq("slug", old_slug).is_("school_id", "null").execute().data
        if not rows:
            print(f"  SKIP (not found): {old_slug:<25} -> {new_slug}")
            continue
        if len(rows) > 1:
            print(f"  ABORT: {len(rows)} rows match free-tier {old_slug}, expected 1")
            sys.exit(1)
        r = rows[0]
        # Check that the target slug doesn't already exist
        conflict = sb.table("subjects").select("id").eq("slug", new_slug).is_("school_id", "null").execute().data
        if conflict:
            print(f"  ABORT: target slug {new_slug} already exists as free-tier")
            sys.exit(1)

        old_name = r["name"]
        target_name = new_name or old_name
        print(f"  {old_slug:<25} -> {new_slug:<35} (id={r['id'][:8]}, name='{old_name}'{' -> ' + target_name if new_name else ''})")
        if not DRY:
            payload = {"slug": new_slug}
            if new_name:
                payload["name"] = new_name
            sb.table("subjects").update(payload).eq("id", r["id"]).execute()

    # === Unity bespoke renames ===
    print("\n--- Unity bespoke (school_id = Unity) ---")
    for old_slug, new_slug, new_name in UNITY_RENAMES:
        rows = sb.table("subjects").select("id, slug, name, school_id").eq("slug", old_slug).eq("school_id", unity_id).execute().data
        if not rows:
            print(f"  SKIP (not found): {old_slug:<25} -> {new_slug}")
            continue
        if len(rows) > 1:
            print(f"  ABORT: {len(rows)} rows match Unity bespoke {old_slug}")
            sys.exit(1)
        r = rows[0]
        conflict = sb.table("subjects").select("id").eq("slug", new_slug).eq("school_id", unity_id).execute().data
        if conflict:
            print(f"  ABORT: target slug {new_slug} already exists for Unity")
            sys.exit(1)

        print(f"  {old_slug:<25} -> {new_slug:<35} (id={r['id'][:8]}, name='{r['name']}')")
        if not DRY:
            payload = {"slug": new_slug}
            if new_name:
                payload["name"] = new_name
            sb.table("subjects").update(payload).eq("id", r["id"]).execute()

    print(f"\n=== {'DRY RUN COMPLETE — no changes applied' if DRY else 'Migration applied'} ===")


if __name__ == "__main__":
    main()
