# -*- coding: utf-8 -*-
"""Strip the baked-in 'Exam Tip' heading text from exam_tip_html (132 lessons
found 16 Aug). The box now carries a proper kicker label, so a leading
'Exam Tip'/'Exam Tips:' inside the content renders as a doubled title.

Removes ONLY a leading heading: an initial heading tag whose text is a bare
'Exam Tip(s)' variant, or a leading '<strong>Exam Tip:</strong>' / bare
'Exam Tip:' prefix inside the first paragraph. Nothing else changes.

Run: python scripts/strip_tip_headings.py [--apply]
Backup: scripts/_tip_headings_backup.json
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

APPLY = "--apply" in sys.argv
BACKUP = os.path.join(HERE, "_tip_headings_backup.json")

# a whole leading heading/strong-para that is JUST the words
LEAD_BLOCK = re.compile(
    r"^\s*<(h[2-6]|strong|b|p|div)[^>]*>\s*(<(strong|b|em)[^>]*>\s*)?"
    r"Exam Tips?:?\s*(</(strong|b|em)>\s*)?</\1>\s*", re.I)
# a leading inline prefix inside the first paragraph
LEAD_INLINE = re.compile(
    r"^(\s*<p[^>]*>)\s*(<(strong|b)[^>]*>\s*)?Exam Tips?:?\s*(</(strong|b)>)?\s*[–—:-]?\s*",
    re.I)
LEAD_BARE = re.compile(r"^\s*Exam Tips?:?\s*[–—:-]?\s*", re.I)


def strip(html):
    out = LEAD_BLOCK.sub("", html, count=1)
    if out != html:
        return out
    out = LEAD_INLINE.sub(r"\1", html, count=1)
    if out != html:
        return out
    return LEAD_BARE.sub("", html, count=1)


def main():
    sb = get_client()
    backup, writes = {}, []
    seen = set()
    start = 0
    while True:
        # ordered + deduplicated: unordered range pagination proved unstable
        # on this table (skipped most rows on the first run)
        rows = sb.table("lessons").select("id,exam_tip_html") \
            .not_.is_("exam_tip_html", "null").order("id") \
            .range(start, start + 499).execute().data
        if not rows:
            break
        for r in rows:
            if r["id"] in seen:
                continue
            seen.add(r["id"])
            h = r["exam_tip_html"] or ""
            if not re.match(r"^\s*(<[^>]+>\s*)*Exam Tips?\b", h, re.I):
                continue
            new = strip(h)
            if new != h and new.strip():
                backup[r["id"]] = h
                writes.append((r["id"], new))
        start += 500
    print("tips to strip: %d" % len(writes))
    for lid, new in writes[:5]:
        print("  ->", re.sub(r"<[^>]+>", " ", new)[:80].strip())
    if not APPLY:
        print("DRY RUN — re-run with --apply")
        return
    # merge into any existing backup — a skip-if-exists guard silently lost
    # the second run's originals once already (16 Aug)
    prior = {}
    if os.path.exists(BACKUP):
        prior = json.load(io.open(BACKUP, encoding="utf-8"))
    prior.update({k: v for k, v in backup.items() if k not in prior})
    io.open(BACKUP, "w", encoding="utf-8").write(json.dumps(prior))
    for lid, new in writes:
        sb.table("lessons").update({"exam_tip_html": new}).eq("id", lid).execute()
    print("applied. backup:", BACKUP)


if __name__ == "__main__":
    main()
