"""
Apply a Phase 1 plan JSON to Supabase: create subject, units, and empty lesson shells.

Reads from a plan JSON matching the schema in docs/PLANNING_PROMPT.md.
Writes subject + units + lessons to Supabase.
Status: status='pending_review' for free-tier, 'live' for Unity.

Usage:
  python scripts/_apply_plan.py scripts/_plan_business_aqa.json
  python scripts/_apply_plan.py scripts/_plan_french_aqa.json --dry-run
"""
import sys, os, json, argparse, re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.supabase_client import get_client


def slugify(title):
    s = title.lower()
    s = re.sub(r"[‘’']", "", s)
    s = re.sub(r"[“”\"]", "", s)
    s = s.replace("&", "and")
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def build_quote_ticker_html(quotes, accent_hex):
    """Build the 5-6 quote scrolling ticker HTML from the plan's quote list."""
    if not quotes:
        return ""

    colours = ["#1d4ed8", "#be185d", "#0369a1", "#7c3aed", "#059669", "#be123c"]
    parts = ['<div class="quote-ticker"><div class="quote-ticker-track">']
    for i, q in enumerate(quotes):
        c = colours[i % len(colours)]
        quote_text = str(q.get("quote", "")).replace("\"", "&ldquo;", 1).replace("\"", "&rdquo;", 1)
        author = q.get("author", "")
        parts.append(f'<span class="quote-item" style="--q-color: {c};">{quote_text} <em>&mdash; {author}</em></span>')
    # Duplicate first two for seamless loop
    for i in range(min(2, len(quotes))):
        c = colours[i % len(colours)]
        q = quotes[i]
        quote_text = str(q.get("quote", "")).replace("\"", "&ldquo;", 1).replace("\"", "&rdquo;", 1)
        author = q.get("author", "")
        parts.append(f'<span class="quote-item" style="--q-color: {c};">{quote_text} <em>&mdash; {author}</em></span>')
    parts.append('</div></div>')
    return "".join(parts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("plan_path")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    with open(args.plan_path, "r", encoding="utf-8") as f:
        plan = json.load(f)

    sb = get_client()

    subj_spec = plan["subject"]
    subject_slug = subj_spec["slug"]
    subject_name = subj_spec["name"]
    board = subj_spec["exam_board"]
    spec_code = subj_spec["spec_code"]
    school_id = subj_spec.get("school_id")  # None for free-tier
    is_free_tier = school_id is None
    lesson_status = "pending_review" if is_free_tier else "live"

    article_units = plan.get("article_units", []) or []
    practice_units = plan.get("practice_units", []) or []
    all_units = article_units + practice_units
    practice_unit_slugs = [u["slug"] for u in practice_units]
    question_type_names = plan.get("question_type_names", []) or []
    quote_ticker_quotes = plan.get("quote_ticker_quotes", []) or []

    # Settings for the subject
    accent_hex = subj_spec.get("target_hero_colour", "#1d4ed8")
    settings = {
        "quote_ticker_html": build_quote_ticker_html(quote_ticker_quotes, accent_hex),
        "unit_image_positions": {},
    }
    if practice_unit_slugs:
        settings["practice_units"] = practice_unit_slugs
    # New subjects default to no exam guides (Tom's decision)
    settings["has_exam_guides"] = False
    if question_type_names:
        settings["question_type_names"] = question_type_names

    print(f"\n=== APPLY PLAN: {subject_name} ({board} {spec_code}) ===")
    print(f"  school_id: {school_id or 'NULL (free-tier)'}")
    print(f"  article units: {len(article_units)}")
    print(f"  practice units: {len(practice_units)}")
    total_lessons = sum(len(u.get("lessons", [])) for u in all_units)
    print(f"  total lessons: {total_lessons}")
    print(f"  lesson status: {lesson_status}")

    if args.dry_run:
        print("\n[DRY RUN] Would create subject, units, and lesson shells. Exiting.")
        return

    # Create subject
    existing = sb.table("subjects").select("id").eq("slug", subject_slug)
    if school_id is None:
        existing = existing.is_("school_id", "null")
    else:
        existing = existing.eq("school_id", school_id)
    existing_data = existing.execute().data

    if existing_data:
        subject_id = existing_data[0]["id"]
        print(f"  Subject already exists, updating (id={subject_id})")
        sb.table("subjects").update({
            "name": subject_name,
            "exam_board": board,
            "spec_code": spec_code,
            "status": "live",
            "settings": settings,
        }).eq("id", subject_id).execute()
    else:
        row = sb.table("subjects").insert({
            "slug": subject_slug,
            "name": subject_name,
            "exam_board": board,
            "spec_code": spec_code,
            "school_id": school_id,
            "status": "live",
            "settings": settings,
        }).execute()
        subject_id = row.data[0]["id"]
        print(f"  Subject created (id={subject_id})")

    # Create units
    unit_ids = {}
    for u in all_units:
        unit_row = {
            "subject_id": subject_id,
            "slug": u["slug"],
            "name": u["name"],
            "subtitle": u.get("subtitle", ""),
            "accent": u.get("accent", accent_hex),
            "accent_light": u.get("accent_light", ""),
            "accent_badge": u.get("accent_badge", ""),
            "body_class": u.get("body_class", f"unit-{subject_slug}-{u.get('sort_order', 1)}"),
            "sort_order": u.get("sort_order", 1),
            "lesson_count": u.get("lesson_count", len(u.get("lessons", []))),
        }
        # Upsert by (subject_id, slug)
        existing_u = sb.table("units").select("id").eq("subject_id", subject_id).eq("slug", u["slug"]).execute().data
        if existing_u:
            uid = existing_u[0]["id"]
            sb.table("units").update(unit_row).eq("id", uid).execute()
            print(f"  Unit updated: {u['slug']} (id={uid})")
        else:
            row = sb.table("units").insert(unit_row).execute()
            uid = row.data[0]["id"]
            print(f"  Unit created: {u['slug']} (id={uid})")
        unit_ids[u["slug"]] = uid

    # Create lesson shells
    for u in all_units:
        uid = unit_ids[u["slug"]]
        for lesson_spec in u.get("lessons", []):
            number = lesson_spec["number"]
            title = lesson_spec["title"]
            slug = lesson_spec.get("slug") or slugify(title)
            description = lesson_spec.get("description", "")
            # Only insert if not already there
            existing_l = (
                sb.table("lessons").select("id")
                .eq("unit_id", uid)
                .eq("lesson_number", number)
                .execute()
            ).data
            if existing_l:
                sb.table("lessons").update({
                    "title": title,
                    "description": description,
                    "slug": slug,
                    "status": lesson_status,
                }).eq("id", existing_l[0]["id"]).execute()
                print(f"    L{number:02d} updated shell: {title}")
            else:
                sb.table("lessons").insert({
                    "unit_id": uid,
                    "lesson_number": number,
                    "title": title,
                    "description": description,
                    "slug": slug,
                    "status": lesson_status,
                    "content_html": "",
                }).execute()
                print(f"    L{number:02d} created shell: {title}")

    print(f"\n[DONE] Subject ID: {subject_id}")
    print(f"Unit IDs:")
    for slug, uid in unit_ids.items():
        print(f"  {slug}: {uid}")
    print(f"\nNext: run content generation agents to fill the lesson bodies.")


if __name__ == "__main__":
    main()
