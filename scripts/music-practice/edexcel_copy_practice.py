# -*- coding: utf-8 -*-
"""Edexcel Phase 2: copy the practice units from music-aqa into
music-edexcel.

  listening-skills            -> listening-skills (3, as-is)
  score-reading               -> score-reading (4, as-is)
  western-classical-1650-1910 -> unfamiliar-listening L1-L2 (K.622 1791,
                                 Beethoven Sym 1 1800 — both inside this
                                 spec's AoS1 era 1700-1820, so the AoS
                                 number carries but the SPAN is fixed)
  aos-listening               -> unfamiliar-listening L3-L4 (pop,
                                 orchestral colour; Broadway problem
                                 dropped and AQA strand refs rewritten,
                                 as on the OCR copy)

Same neutral-phrasing pass, board-name assert, resume-safe,
pending_review. Run: python edexcel_copy_practice.py [--apply]
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
    ("listening-skills", "listening-skills", None, {}),
    ("score-reading", "score-reading", None, {}),
    ("western-classical-1650-1910", "unfamiliar-listening",
     {3: 1, 1: 2}, {}),
    ("aos-listening", "unfamiliar-listening",
     {1: 3, 3: 4},
     {1: "Popular Music — Unfamiliar Listening",
      3: "Orchestral Colour — Unfamiliar Listening"}),
]


def neutralise(s):
    s = re.sub(r"(^|[.!?]\s+|[\"“>]\s*)Section A\b", r"\1The listening exam", s)
    s = s.replace("Section A", "the listening exam")
    return s


def transform(dst_slug, dst_n, pd):
    if dst_slug == "unfamiliar-listening":
        # AQA paper furniture out; this spec's appraising paper in
        pd["exam_context"] = {
            "marks": "varies — questions are 1–6 marks",
            "paper": "Appraising (Component 3)",
            "frequency": "Unfamiliar music appears in the listening "
                         "questions and in the comparison essay, which "
                         "sets an unfamiliar piece against a set work"}
    blob = json.dumps(pd)
    if dst_slug == "unfamiliar-listening" and dst_n in (1, 2):
        blob = blob.replace("1650-1910", "1700-1820")
        blob = blob.replace("1650\\u20131910", "1700\\u20131820")
        blob = blob.replace("1650–1910", "1700–1820")
    if dst_slug == "unfamiliar-listening" and dst_n == 3:
        pd = json.loads(blob)
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
    if dst_slug == "unfamiliar-listening" and dst_n in (3, 4):
        assert "Area of Study" not in blob, \
            "unresolved AoS reference in %s L%d" % (dst_slug, dst_n)
    return json.loads(blob)


def main():
    sb = get_client()
    src_sub = sb.table("subjects").select("id").eq("slug", "music-aqa").execute().data[0]["id"]
    dst_sub = sb.table("subjects").select("id").eq("slug", "music-edexcel").execute().data[0]["id"]
    units = sb.table("units").select("id,slug,subject_id").execute().data
    copied = 0
    flags = []
    for src_slug, dst_slug, num_map, retitles in UNIT_MAP:
        src_u = next(u for u in units if u["subject_id"] == src_sub and u["slug"] == src_slug)
        dst_u = next(u for u in units if u["subject_id"] == dst_sub and u["slug"] == dst_slug)
        existing = {r["lesson_number"] for r in sb.table("lessons")
                    .select("lesson_number").eq("unit_id", dst_u["id"]).execute().data}
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
            assert not re.search(r"(?i)\bAQA\b|\bEdexcel\b|\bWJEC\b|\bEduqas\b|\bOCR\b",
                                 prose), "board name in source %s L%d" % (src_slug, src_n)
            n_sec = blob.count("Section A")
            blob = neutralise(blob)
            assert "Section A" not in blob
            pd = transform(dst_slug, dst_n, json.loads(blob))
            final_prose = re.sub(r"https://\S+", "", json.dumps(pd))
            for m in re.finditer(r"(Area of Study \d|1650)[^\"]{0,50}", final_prose):
                flags.append("%s L%d: %s" % (dst_slug, dst_n, m.group(0)))
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
    if flags:
        print("!! flags to resolve:")
        for f in flags:
            print("   ", f)


if __name__ == "__main__":
    main()
