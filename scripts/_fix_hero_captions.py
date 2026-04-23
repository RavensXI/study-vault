"""
Retroactively rewrite hero_image_caption for lessons so the caption matches
what's in the image (from hero_image_alt) plus Unsplash attribution.

Previously, captions came from content agents' imagined captions, which
often didn't match the downloaded image. Now they're derived from the
image's actual Unsplash alt_description + "Photo via Unsplash" attribution.

Usage:
  python scripts/_fix_hero_captions.py --subject business-aqa
  python scripts/_fix_hero_captions.py --subject business-edexcel
  python scripts/_fix_hero_captions.py --subject all       # all free-tier subjects
"""
import sys, os, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.supabase_client import get_client


def truncate(s, n=110):
    s = (s or "").strip()
    if len(s) <= n:
        return s
    cut = s[:n].rsplit(" ", 1)[0]
    return cut.rstrip(".,;:-") + "…"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", required=True, help="subject slug or 'all'")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    sb = get_client()

    if args.subject == "all":
        subjects = sb.table("subjects").select("id,slug").is_("school_id", "null").execute().data
    else:
        subjects = sb.table("subjects").select("id,slug").eq("slug", args.subject).is_("school_id", "null").execute().data

    if not subjects:
        print(f"No subjects matched.")
        return

    for subj in subjects:
        units = sb.table("units").select("id").eq("subject_id", subj["id"]).execute().data
        unit_ids = [u["id"] for u in units]
        if not unit_ids:
            continue
        lessons = (
            sb.table("lessons")
            .select("id,title,hero_image_alt,hero_image_caption")
            .in_("unit_id", unit_ids)
            .not_.is_("hero_image_url", "null")
            .execute()
            .data
        )
        updated = 0
        # Strip captions down to attribution only. Unsplash alt_descriptions
        # are often auto-generated nonsense ("white and black love letter"
        # for a business-ideas photo) and content-agent captions describe
        # what the agent wanted, not what got downloaded. A clean "Photo via
        # Unsplash" line is the honest baseline.
        new_caption = "Photo via Unsplash"
        for l in lessons:
            if l.get("hero_image_caption") == new_caption:
                continue
            if args.dry_run:
                print(f"  [DRY] {subj['slug']} / {l['title'][:40]:40s} → {new_caption[:80]}")
            else:
                sb.table("lessons").update({"hero_image_caption": new_caption}).eq("id", l["id"]).execute()
                updated += 1
        print(f"{subj['slug']}: {updated} captions updated")


if __name__ == "__main__":
    main()
