# -*- coding: utf-8 -*-
"""OCR Phase 2: copy the practice units from music-aqa into music-ocr.

  listening-skills            -> listening-skills (3, as-is numbering)
  score-reading               -> score-reading (4, as-is)
  western-classical-1650-1910 -> aos2-concerto-listening (7 of 8, RENUMBERED
                                 chronologically Baroque->Classical->Romantic;
                                 Schumann miniatures left out — weakest fit
                                 for a concerto/orchestral unit)
  aos-listening               -> aos45-unfamiliar-listening (3; ensemble
                                 lesson retitled to band textures)

Same neutral-phrasing pass as the Eduqas copiers ("Section A" -> listening
exam), board-name assert on prose (URLs excluded), resume-safe, lessons
land pending_review. Audio stays on the music-aqa R2 paths (same public
bucket). Any 'Area of Study' text in copied prose is flagged loudly — AQA
AoS numbering is wrong for this spec and must be resolved, not shipped.

Run: python ocr_copy_practice.py [--apply]
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

# (src_unit, dst_unit, {src_lesson: dst_lesson} or None for identity,
#  {src_lesson: new_title} retitles)
UNIT_MAP = [
    ("listening-skills", "listening-skills", None, {}),
    ("score-reading", "score-reading", None, {}),
    ("western-classical-1650-1910", "aos2-concerto-listening",
     {5: 1,   # Handel, Zadok the Priest (Baroque)
      3: 2,   # Mozart, Clarinet Concerto K.622 (the real concerto)
      1: 3,   # Beethoven, Symphony No.1
      2: 4,   # Mozart, Symphony No.40
      4: 5,   # Haydn, Symphony No.94
      6: 6,   # Chopin, Nocturne (Romantic)
      8: 7},  # Verdi, Requiem Dies irae (Romantic)
     {}),
    ("aos-listening", "aos45-unfamiliar-listening",
     {1: 1, 2: 2, 3: 3},
     {1: "Popular Music — Unfamiliar Listening",
      2: "Band and Ensemble Textures — Unfamiliar Listening",
      3: "Orchestral Colour — Unfamiliar Listening"}),
]


def transform(dst_slug, dst_n, pd):
    """Per-destination spec fixes. Returns the transformed practice_data."""
    blob = json.dumps(pd)
    if dst_slug == "aos2-concerto-listening":
        # the source unit is AQA's AoS1; this spec's 1650-1910 area is AoS2
        blob = blob.replace("Area of Study 1", "Area of Study 2")
    if dst_slug == "aos45-unfamiliar-listening" and dst_n == 1:
        pd = json.loads(blob)
        # Broadway is an AQA pop strand, not one of this spec's four — drop
        # the Broadway excerpt and everything built on it
        pid = "p-aos2_broadway_pit"
        pd["passages"] = [p for p in pd["passages"] if p["id"] != pid]
        for tier, probs in pd["problem_bank"].items():
            pd["problem_bank"][tier] = [
                p for p in probs if p.get("passage_id") != pid
                and pid not in json.dumps(p)]
        if isinstance(pd.get("worked_examples"), list):
            pd["worked_examples"] = [
                w for w in pd["worked_examples"] if pid not in json.dumps(w)]
        blob = json.dumps(pd)
        blob = blob.replace(
            "That combination points to the rock strand of Area of Study 2 "
            "\\u2014 the music of the 1960s and 1970s.",
            "That combination points to a classic rock line-up of the late "
            "1960s and 1970s.")
        blob = blob.replace(
            "pointing to the rock strand of Area of Study 2 from the 1960s "
            "and 1970s",
            "pointing to a classic rock band of the late 1960s and 1970s")
    assert "Area of Study 1" not in blob or dst_slug != "aos2-concerto-listening"
    if dst_slug == "aos45-unfamiliar-listening":
        assert "Area of Study" not in blob, \
            "unresolved AoS reference in %s L%d" % (dst_slug, dst_n)
    return json.loads(blob)


def neutralise(s):
    s = re.sub(r"(^|[.!?]\s+|[\"“>]\s*)Section A\b", r"\1The listening exam", s)
    s = s.replace("Section A", "the listening exam")
    return s


def main():
    sb = get_client()
    src_sub = sb.table("subjects").select("id").eq("slug", "music-aqa").execute().data[0]["id"]
    dst_sub = sb.table("subjects").select("id").eq("slug", "music-ocr").execute().data[0]["id"]
    units = sb.table("units").select("id,slug,subject_id").execute().data
    copied = 0
    aos_flags = []
    for src_slug, dst_slug, num_map, retitles in UNIT_MAP:
        src_u = next(u for u in units if u["subject_id"] == src_sub and u["slug"] == src_slug)
        dst_u = next(u for u in units if u["subject_id"] == dst_sub and u["slug"] == dst_slug)
        existing = {r["lesson_number"] for r in sb.table("lessons")
                    .select("lesson_number").eq("unit_id", dst_u["id"]).execute().data}
        if existing:
            print("%s: %d already present, skipping those" % (dst_slug, len(existing)))
        rows = sb.table("lessons").select(
            "lesson_number,slug,title,description,practice_data") \
            .eq("unit_id", src_u["id"]).order("lesson_number").execute().data
        for l in rows:
            src_n = l["lesson_number"]
            if num_map is not None and src_n not in num_map:
                continue
            dst_n = num_map[src_n] if num_map else src_n
            if dst_n in existing:
                continue
            blob = json.dumps(l["practice_data"])
            prose = re.sub(r"https://\S+", "", blob)
            assert not re.search(r"(?i)\bAQA\b|\bEdexcel\b|\bWJEC\b|\bEduqas\b",
                                 prose), \
                "board name in source %s L%d" % (src_slug, src_n)
            n_sec = blob.count("Section A")
            blob = neutralise(blob)
            assert "Section A" not in blob
            pd = transform(dst_slug, dst_n, json.loads(blob))
            final_prose = re.sub(r"https://\S+", "", json.dumps(pd))
            ok_aos = ("Area of Study 2"
                      if dst_slug == "aos2-concerto-listening" else None)
            for m in re.finditer(r"Area of Study \d[^\"]{0,60}", final_prose):
                if ok_aos and m.group(0).startswith(ok_aos):
                    continue
                aos_flags.append("%s L%d: %s" % (dst_slug, dst_n, m.group(0)))
            title = retitles.get(src_n) or neutralise(l["title"])
            desc = neutralise(l["description"] or "")
            print("%s L%d -> %s L%d: %d neutralised | %s"
                  % (src_slug, src_n, dst_slug, dst_n, n_sec, title[:46]))
            if APPLY:
                sb.table("lessons").insert({
                    "unit_id": dst_u["id"], "lesson_number": dst_n,
                    "slug": l["slug"], "title": title, "description": desc,
                    "practice_data": pd,
                    "status": "pending_review",
                }).execute()
            copied += 1
    print("\n%s %d lessons" % ("copied" if APPLY else "would copy", copied))
    if aos_flags:
        print("\n!! 'Area of Study' references in copied prose — RESOLVE:")
        for f in aos_flags:
            print("   ", f)


if __name__ == "__main__":
    main()
