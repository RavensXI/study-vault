"""Strip board-specific phrasing ('Eduqas Film Studies (C670QS)' etc.) from
Film Studies revision-technique guide pages.

Lessons themselves are already neutral. Only 3 mentions exist across the 8
revision guides. Narration regen NOT needed (guides have no narration; the
lessons table is untouched).
"""
import sys
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

sb = get_client()

SUBJECT_SLUG = "film-studies-eduqas"

# Order matters: longer phrases first so they're swapped before the shorter
# 'Eduqas Film Studies' subset matches.
SWAPS = [
    (r"\bEduqas Film Studies \(C670QS\)\b", "GCSE Film Studies"),
    (r"\bEduqas Film Studies\b", "GCSE Film Studies"),
    (r"\bWJEC Film Studies\b", "GCSE Film Studies"),
]


def strip_urls(html):
    """Remove URL attributes so we don't accidentally rewrite slug paths."""
    return re.sub(r'(href|src)=([\'\"])[^\'\"]*\2', '', html)


sid = sb.table("subjects").select("id").eq("slug", SUBJECT_SLUG).is_("school_id", "null").execute().data[0]["id"]
guides = sb.table("guide_pages").select("id, slug, content_html").eq("subject_id", sid).execute().data

total_changed = 0
total_swaps = 0
for g in guides:
    html = g["content_html"] or ""
    new_html = html
    swap_count = 0
    for pattern, replacement in SWAPS:
        # Apply swap only outside URL/href contexts. Easiest: split into URL
        # vs non-URL spans and only rewrite non-URL.
        parts = re.split(r'((?:href|src)=[\'\"][^\'\"]*[\'\"])', new_html)
        for i in range(len(parts)):
            if i % 2 == 0:  # non-URL chunks
                new_chunk, n = re.subn(pattern, replacement, parts[i], flags=re.IGNORECASE)
                if n > 0:
                    parts[i] = new_chunk
                    swap_count += n
        new_html = "".join(parts)

    if new_html != html:
        sb.table("guide_pages").update({"content_html": new_html}).eq("id", g["id"]).execute()
        print(f"  {g['slug']:30s}: {swap_count} swap(s)")
        total_changed += 1
        total_swaps += swap_count

print(f"\nGuides changed: {total_changed}, total swaps: {total_swaps}")
