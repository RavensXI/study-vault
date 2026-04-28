"""Insert/update revision-technique guide pages for History (AQA 8145), free-tier.

The example-filling step has already been done by a content agent — the agent
filled {{SUBJECT_NAME}}, {{SUBJECT_SLUG}}, {{SUBJECT_EXAMPLE_1}}, and
{{SUBJECT_EXAMPLE_2}} into the 8 templates and saved them under
scripts/_content_history-aqa/guides/. This script only handles the RUNTIME
placeholders (HUB_INTRO, OTHER_TECHNIQUES_LINKS, OPTIONAL_SUBJECT_SPECIFIC_CARD)
plus the Supabase upsert.
"""
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from lib.supabase_client import get_client

SUBJECT_SLUG = "history-aqa"
SUBJECT_NAME = "History"
GUIDE_TYPE = "revision-technique"
GUIDES_DIR = ROOT / "scripts" / "_content_history-aqa" / "guides"

HUB_INTRO = (
    "Evidence-based revision strategies from cognitive science, tailored to GCSE History. "
    "Each technique is backed by peer-reviewed research and shown in action with a History example "
    "drawn from across the AQA options."
)

TECHNIQUE_ORDER = [
    ("retrieval-practice", "Retrieval Practice"),
    ("spaced-repetition", "Spaced Repetition"),
    ("interleaving", "Interleaving"),
    ("dual-coding", "Dual Coding"),
    ("elaborative-interrogation", "Elaborative Interrogation"),
    ("knowledge-organisers", "Knowledge Organisers"),
    ("timed-practice", "Timed Practice"),
]


def other_links_for(current_slug: str) -> str:
    parts = []
    for slug, name in TECHNIQUE_ORDER:
        if slug == current_slug:
            continue
        parts.append(
            f'<a href="/guide/{SUBJECT_SLUG}/revision-technique/{slug}" '
            f'class="sidebar-media-item"><strong>{name}</strong></a>'
        )
    return "\n".join(parts)


def runtime_fill(html: str, slug: str) -> str:
    html = html.replace("{{HUB_INTRO}}", HUB_INTRO)
    html = html.replace("{{OPTIONAL_SUBJECT_SPECIFIC_CARD}}", "")
    html = html.replace("{{OTHER_TECHNIQUES_LINKS}}", other_links_for(slug))
    return html


pages = [
    {"slug": "index", "title": "Revision Techniques", "file": "index.html", "sort_order": 0},
    {"slug": "retrieval-practice", "title": "Retrieval Practice", "file": "retrieval-practice.html", "sort_order": 1},
    {"slug": "spaced-repetition", "title": "Spaced Repetition", "file": "spaced-repetition.html", "sort_order": 2},
    {"slug": "interleaving", "title": "Interleaving", "file": "interleaving.html", "sort_order": 3},
    {"slug": "dual-coding", "title": "Dual Coding", "file": "dual-coding.html", "sort_order": 4},
    {"slug": "elaborative-interrogation", "title": "Elaborative Interrogation", "file": "elaborative-interrogation.html", "sort_order": 5},
    {"slug": "knowledge-organisers", "title": "Knowledge Organisers", "file": "knowledge-organisers.html", "sort_order": 6},
    {"slug": "timed-practice", "title": "Timed Practice", "file": "timed-practice.html", "sort_order": 7},
]

for p in pages:
    path = GUIDES_DIR / p["file"]
    raw = path.read_text(encoding="utf-8")
    p["content_html"] = runtime_fill(raw, p["slug"])

PLACEHOLDER_RE = re.compile(r"\{\{[^}]+\}\}")
leaks_found = False
for p in pages:
    leaks = PLACEHOLDER_RE.findall(p["content_html"])
    if leaks:
        print(f"ABORT — placeholder leak in {p['slug']}: {leaks}")
        leaks_found = True
if leaks_found:
    sys.exit(1)
print("Pre-flight OK — no placeholder leaks in any of the 8 pages.\n")

sb = get_client()
SUBJECT_ID = (
    sb.table("subjects")
    .select("id")
    .eq("slug", SUBJECT_SLUG)
    .is_("school_id", "null")
    .single()
    .execute()
    .data["id"]
)
print(f"Subject ID: {SUBJECT_ID}\n")

inserted, updated = 0, 0
for p in pages:
    existing = (
        sb.table("guide_pages")
        .select("id")
        .eq("subject_id", SUBJECT_ID)
        .eq("guide_type", GUIDE_TYPE)
        .eq("slug", p["slug"])
        .execute()
        .data
    )
    if existing:
        sb.table("guide_pages").update(
            {
                "title": p["title"],
                "content_html": p["content_html"],
                "sort_order": p["sort_order"],
            }
        ).eq("id", existing[0]["id"]).execute()
        updated += 1
        print(f"  updated  {p['slug']:<28} (sort {p['sort_order']})")
    else:
        sb.table("guide_pages").insert(
            {
                "subject_id": SUBJECT_ID,
                "guide_type": GUIDE_TYPE,
                "slug": p["slug"],
                "title": p["title"],
                "content_html": p["content_html"],
                "sort_order": p["sort_order"],
            }
        ).execute()
        inserted += 1
        print(f"  inserted {p['slug']:<28} (sort {p['sort_order']})")

print(f"\nDone. inserted={inserted}, updated={updated}, total={inserted + updated}")

print("\nVerification query…")
rows = (
    sb.table("guide_pages")
    .select("slug,title,sort_order,content_html")
    .eq("subject_id", SUBJECT_ID)
    .eq("guide_type", GUIDE_TYPE)
    .order("sort_order")
    .execute()
    .data
)
print(f"  rows: {len(rows)}")
for r in rows:
    leaks = PLACEHOLDER_RE.findall(r["content_html"] or "")
    status = "OK" if not leaks else f"LEAK: {leaks}"
    print(f"  [{r['sort_order']}] {r['slug']:<28} {r['title']:<28} len={len(r['content_html'] or ''):>5}  {status}")
