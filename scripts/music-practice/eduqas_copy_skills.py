# -*- coding: utf-8 -*-
"""Phase 2: copy listening-skills + score-reading from music-aqa into
music-eduqas with the terminology/neutral-phrasing pass.

- "Section A" is the AQA paper's structure — replaced with neutral exam
  language ("the listening exam" / "The listening exam").
- Asserts the source contains no board names (house rule says it never
  did; verify, don't assume).
- Lessons land pending_review. Audio URLs inside practice_data stay on the
  music-aqa R2 paths — same public bucket, verified below.

Run: python eduqas_copy_skills.py [--apply]
"""
import json
import os
import re
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

APPLY = "--apply" in sys.argv
UNITS = ["listening-skills", "score-reading"]


def neutralise(s):
    # sentence-initial occurrences keep the capital; mid-sentence lowercase
    import re as _re
    s = _re.sub(r'(^|[.!?]\s+|["“>]\s*)Section A', r'The listening exam', s)
    s = s.replace('Section A', 'the listening exam')
    return s


def main():
    sb = get_client()
    src_sub = sb.table("subjects").select("id").eq("slug", "music-aqa").execute().data[0]["id"]
    dst_sub = sb.table("subjects").select("id").eq("slug", "music-eduqas").execute().data[0]["id"]
    units = sb.table("units").select("id,slug,subject_id").execute().data
    copied = 0
    for uslug in UNITS:
        src_u = next(u for u in units if u["subject_id"] == src_sub and u["slug"] == uslug)
        dst_u = next(u for u in units if u["subject_id"] == dst_sub and u["slug"] == uslug)
        rows = sb.table("lessons").select(
            "lesson_number,slug,title,description,practice_data") \
            .eq("unit_id", src_u["id"]).order("lesson_number").execute().data
        for l in rows:
            blob = json.dumps(l["practice_data"])
            # URLs/slugs legitimately contain 'aqa' (music-aqa R2 paths) —
            # check the prose only
            prose = re.sub(r"https://\S+", "", blob)
            assert not re.search(r"(?i)\bAQA\b|\bEdexcel\b|\bWJEC\b", prose), \
                "board name in source %s L%d" % (uslug, l["lesson_number"])
            n_sec = blob.count("Section A")
            blob = neutralise(blob)
            assert "Section A" not in blob
            title = neutralise(l["title"])
            desc = neutralise(l["description"] or "")
            print("%s L%d: %d 'Section A' neutralised | %s"
                  % (uslug, l["lesson_number"], n_sec, title[:50]))
            if APPLY:
                sb.table("lessons").insert({
                    "unit_id": dst_u["id"], "lesson_number": l["lesson_number"],
                    "slug": l["slug"], "title": title, "description": desc,
                    "practice_data": json.loads(blob),
                    "status": "pending_review",
                }).execute()
            copied += 1
    print("\n%s %d lessons" % ("copied" if APPLY else "would copy", copied))

    # verify one audio URL from the copied data still serves
    l1 = sb.table("lessons").select("practice_data").eq(
        "unit_id", next(u["id"] for u in units
                        if u["subject_id"] == src_sub and u["slug"] == "listening-skills")) \
        .eq("lesson_number", 1).execute().data[0]
    m = re.search(r"https://[^\"]+\.mp3", json.dumps(l1["practice_data"]))
    if m:
        code = urllib.request.urlopen(m.group(0), timeout=20).status
        print("sample audio URL HTTP:", code)


if __name__ == "__main__":
    main()
