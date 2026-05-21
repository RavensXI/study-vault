"""Count free-tier lessons that are eligible for NotebookLM standard video overviews.

Definition:
  - school_id IS NULL (free tier)
  - subject is article-format (we skip practice-first subjects entirely)
  - OR for mixed-format subjects: lesson is in an article unit (not in
    subjects.settings.practice_units)
  - Optionally split by "already has a video URL" vs "needs one" so the
    estimate accounts for any related-media YouTube embeds already wired up.

NotebookLM standard video cap: 200/day. We report:
  - per-subject counts (article-eligible only)
  - global total of article-eligible lessons missing a video
  - days at 200/day to fill the gap
"""
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.supabase_client import get_client

sb = get_client()

# All free-tier subjects.
subjects = (
    sb.table("subjects")
    .select("id, slug, name, exam_board, settings")
    .is_("school_id", "null")
    .execute()
    .data
)

# Index practice units per subject so we can drop those lessons.
practice_unit_slugs_by_subject = {}
for s in subjects:
    settings = s.get("settings") or {}
    practice_unit_slugs_by_subject[s["id"]] = set(settings.get("practice_units") or [])

# Pull all free-tier lessons in one go with unit slug for filtering.
# We page through to handle the >1,000 row response cap on Supabase REST.
all_lessons = []
page_size = 1000
offset = 0
while True:
    page = (
        sb.table("lessons")
        .select(
            "id, slug, status, youtube_video_id, "
            "units!inner(slug, subject_id, subjects!inner(id, slug, name, school_id))"
        )
        .is_("units.subjects.school_id", "null")
        .range(offset, offset + page_size - 1)
        .execute()
        .data
    )
    if not page:
        break
    all_lessons.extend(page)
    if len(page) < page_size:
        break
    offset += page_size

print(f"pulled {len(all_lessons)} free-tier lessons total\n")

# Group counts per subject.
counts = defaultdict(lambda: {
    "total": 0,
    "practice_dropped": 0,
    "article_total": 0,
    "article_has_video": 0,
    "article_needs_video": 0,
})

# Subjects we class as practice-first end-to-end (no video overviews planned).
# These have all their lessons treated as practice (we drop them from the total).
PRACTICE_FIRST_SUBJECT_SLUGS = {
    "maths", "maths-aqa", "maths-edexcel", "maths-ocr", "maths-eduqas",
    "english-language", "english-language-aqa", "english-language-edexcel",
    "english-language-ocr", "english-language-eduqas",
    "spanish", "french", "german",
}

for lesson in all_lessons:
    unit = lesson.get("units") or {}
    subj = unit.get("subjects") or {}
    subj_slug = subj.get("slug") or "?"
    subj_name = subj.get("name") or "?"
    subj_id = subj.get("id")
    key = (subj_slug, subj_name)
    counts[key]["total"] += 1

    # Skip whole-subject practice-first first.
    if subj_slug in PRACTICE_FIRST_SUBJECT_SLUGS:
        counts[key]["practice_dropped"] += 1
        continue

    # Skip lessons that sit in a practice unit on a mixed-format subject.
    unit_slug = unit.get("slug")
    if unit_slug in practice_unit_slugs_by_subject.get(subj_id, set()):
        counts[key]["practice_dropped"] += 1
        continue

    counts[key]["article_total"] += 1
    if lesson.get("youtube_video_id"):
        counts[key]["article_has_video"] += 1
    else:
        counts[key]["article_needs_video"] += 1

# Print a tidy report sorted by needs_video desc.
print(f"{'Subject':<55} {'total':>6} {'practice':>9} {'article':>8} {'has_vid':>8} {'needs':>6}")
print("-" * 100)
needs_total = 0
article_total = 0
sorted_keys = sorted(counts.keys(), key=lambda k: counts[k]["article_needs_video"], reverse=True)
for key in sorted_keys:
    c = counts[key]
    label = f"{key[1]} [{key[0]}]"
    if len(label) > 53:
        label = label[:52] + "…"
    print(
        f"{label:<55} "
        f"{c['total']:>6} "
        f"{c['practice_dropped']:>9} "
        f"{c['article_total']:>8} "
        f"{c['article_has_video']:>8} "
        f"{c['article_needs_video']:>6}"
    )
    needs_total += c["article_needs_video"]
    article_total += c["article_total"]

print("-" * 100)
print(f"{'TOTAL':<55} {'':>6} {'':>9} {article_total:>8} {article_total - needs_total:>8} {needs_total:>6}")
print()
print(f"Article-format free-tier lessons missing a video: {needs_total}")
print(f"At NotebookLM standard-video cap of 200/day: {needs_total / 200:.1f} days of pipeline time")
print(f"Realistic end-to-end (10-30% overhead for retries + manual click-through): "
      f"{(needs_total / 200) * 1.2:.1f} – {(needs_total / 200) * 1.4:.1f} days")
