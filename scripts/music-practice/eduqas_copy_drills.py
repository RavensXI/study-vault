# -*- coding: utf-8 -*-
"""Phase 3: copy the drill units from music-aqa into music-eduqas.

  western-classical-1650-1910 -> forms-devices-listening (8 lessons)
  aos-listening               -> ensemble-film-pop-listening (3 lessons)

Same neutral-phrasing pass and checks as eduqas_copy_skills.py. The
forms-question ADDITIONS (binary/ternary/rondo asks per work) are a
Phase-4-adjacent authoring step, logged as TODO — the copies carry the
verified AQA banks as-is.

Run: python eduqas_copy_drills.py [--apply]
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from lib.supabase_client import get_client

APPLY = "--apply" in sys.argv
UNIT_MAP = [
    ("western-classical-1650-1910", "forms-devices-listening"),
    ("aos-listening", "ensemble-film-pop-listening"),
]


def neutralise(s):
    s = re.sub(r"(^|[.!?]\s+|[\"“>]\s*)Section A\b", r"\1The listening exam", s)
    s = s.replace("Section A", "the listening exam")
    return s


def main():
    sb = get_client()
    src_sub = sb.table("subjects").select("id").eq("slug", "music-aqa").execute().data[0]["id"]
    dst_sub = sb.table("subjects").select("id").eq("slug", "music-eduqas").execute().data[0]["id"]
    units = sb.table("units").select("id,slug,subject_id").execute().data
    copied = 0
    for src_slug, dst_slug in UNIT_MAP:
        src_u = next(u for u in units if u["subject_id"] == src_sub and u["slug"] == src_slug)
        dst_u = next(u for u in units if u["subject_id"] == dst_sub and u["slug"] == dst_slug)
        # resume-safe: a prior partial run may have landed some lessons
        existing = {r["lesson_number"] for r in sb.table("lessons")
                    .select("lesson_number").eq("unit_id", dst_u["id"]).execute().data}
        if existing:
            print("%s: %d already present, skipping those" % (dst_slug, len(existing)))
        rows = sb.table("lessons").select(
            "lesson_number,slug,title,description,practice_data") \
            .eq("unit_id", src_u["id"]).order("lesson_number").execute().data
        for l in rows:
            if l["lesson_number"] in existing:
                continue
            blob = json.dumps(l["practice_data"])
            prose = re.sub(r"https://\S+", "", blob)
            assert not re.search(r"(?i)\bAQA\b|\bEdexcel\b|\bWJEC\b", prose), \
                "board name in source %s L%d" % (src_slug, l["lesson_number"])
            n_sec = blob.count("Section A")
            blob = neutralise(blob)
            assert "Section A" not in blob
            title = neutralise(l["title"])
            desc = neutralise(l["description"] or "")
            print("%s L%d -> %s: %d neutralised | %s"
                  % (src_slug, l["lesson_number"], dst_slug, n_sec, title[:46]))
            if APPLY:
                sb.table("lessons").insert({
                    "unit_id": dst_u["id"], "lesson_number": l["lesson_number"],
                    "slug": l["slug"], "title": title, "description": desc,
                    "practice_data": json.loads(blob),
                    "status": "pending_review",
                }).execute()
            copied += 1
    print("\n%s %d lessons" % ("copied" if APPLY else "would copy", copied))


if __name__ == "__main__":
    main()
