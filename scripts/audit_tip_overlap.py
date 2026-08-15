# -*- coding: utf-8 -*-
"""Exam-tip vs body overlap sweep (Tom, 16 Aug — item 4 of the tip/conclusion
fixes): flag lessons whose exam tip is a near-restatement of the final body
section, for a review-gated trim like the AoS2 pair. Reports; changes nothing.

Usage: python scripts/audit_tip_overlap.py music-aqa   (one subject, detailed)
       python scripts/audit_tip_overlap.py --all       (sitewide summary)
Report: scripts/_tip_overlap_report.md
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

TAGS = re.compile(r"<[^>]+>")
STOP = set("the a an of and in on for with to from by at is are was were be "
           "been it its this that these those you your they their which what "
           "how when where not no or as if so than then there here can will "
           "would should could may might must do does did have has had more "
           "most some any each every one two three".split())
FLAG_AT = 0.55


def words(html):
    return set(w for w in re.findall(r"[a-z']+", TAGS.sub(" ", html or "").lower())
               if len(w) > 2 and w not in STOP)


def last_section(content_html):
    parts = re.split(r"<h[23][^>]*>", content_html or "")
    return parts[-1] if len(parts) > 1 else (content_html or "")


def main():
    sb = get_client()
    target = sys.argv[1] if len(sys.argv) > 1 else "music-aqa"
    subs = sb.table("subjects").select("id,slug").execute().data
    if target != "--all":
        subs = [s for s in subs if s["slug"] == target]
    units = sb.table("units").select("id,slug,subject_id").execute().data
    umap = {u["id"]: u for u in units}

    flagged, checked = [], 0
    for s in subs:
        uids = [u["id"] for u in units if u["subject_id"] == s["id"]]
        for uid in uids:
            rows = sb.table("lessons") \
                .select("lesson_number,exam_tip_html,content_html") \
                .eq("unit_id", uid).execute().data
            for l in rows:
                tip = words(l.get("exam_tip_html"))
                if len(tip) < 8:
                    continue
                checked += 1
                body = words(last_section(l.get("content_html")))
                if not body:
                    continue
                ratio = len(tip & body) / len(tip)
                if ratio >= FLAG_AT:
                    flagged.append((s["slug"], umap[uid]["slug"],
                                    l["lesson_number"], round(ratio, 2)))

    flagged.sort(key=lambda x: -x[3])
    lines = ["# Exam-tip overlap report — flag at >=%d%% of tip words present "
             "in the final body section" % (FLAG_AT * 100), "",
             "%d lessons with tips checked, %d flagged" % (checked, len(flagged)), ""]
    for slug, unit, num, ratio in flagged:
        lines.append("- %d%%  %s/%s/L%d" % (int(ratio * 100), slug, unit, num))
    io.open(os.path.join(HERE, "_tip_overlap_report.md"), "w", encoding="utf-8") \
        .write("\n".join(lines))
    print("%d checked, %d flagged (>=%d%%) — scripts/_tip_overlap_report.md"
          % (checked, len(flagged), FLAG_AT * 100))
    for f in flagged[:15]:
        print("  %d%%  %s/%s/L%d" % (int(f[3] * 100), f[0], f[1], f[2]))


if __name__ == "__main__":
    main()
