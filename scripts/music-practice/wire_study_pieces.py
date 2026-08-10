# -*- coding: utf-8 -*-
"""Validate and wire the Queen + Spalding study-piece lessons.

Append-only; the YouTube whitelist is the check that matters — an id we did
not oEmbed-verify must not reach a student.

Usage:
    python scripts/music-practice/wire_study_pieces.py --dry-run
    python scripts/music-practice/wire_study_pieces.py
"""
import re
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from lib.supabase_client import get_client
from study_piece_lessons import LESSONS

DRY = "--dry-run" in sys.argv
ENTITY = re.compile(r"&(?:[a-zA-Z]+|#\d+);")
NARR = re.compile(r'data-narration-id="(n\d+)"')
YT = re.compile(r'youtube\.com/watch\?v=([\w-]{11})')
ALLOWED_YT = {"fJ9rUzIMcZQ", "0e4Odk-v3oU", "sUJkCXE4sAA",
              "0NfQmoouvTY", "w2JRGv91urY", "evjfOnvIPLk"}


def validate(lesson):
    errs = []
    plains = [lesson["description"]]
    for g in lesson["glossary_terms"]:
        plains += [g["term"], g["definition"]]
    for k in lesson["knowledge_checks"]:
        plains += [k["q"]] + k["options"]
    for q in lesson["practice_questions"]:
        plains += [q["text"], q["marks"]]
    for f in lesson["flashcard_questions"]:
        plains += [f["q"], f["a"]]
    for p in plains:
        if ENTITY.search(p):
            errs.append("entity in plain-text field: %r" % ENTITY.search(p).group())
    if len(lesson["knowledge_checks"]) != 5:
        errs.append("KC count != 5")
    if len(lesson["practice_questions"]) != 6:
        errs.append("PQ count != 6")
    if len(lesson["flashcard_questions"]) != 5:
        errs.append("flashcard count != 5")
    for k in lesson["knowledge_checks"]:
        if set(k) != {"q", "type", "correct", "options"} or k["type"] != "mcq" \
                or len(k["options"]) != 4 or not 0 <= k["correct"] < 4:
            errs.append("KC shape wrong: %r" % k["q"][:40])
    ids = NARR.findall(lesson["content_html"]) + NARR.findall(
        lesson["exam_tip_html"]) + NARR.findall(lesson["conclusion_html"])
    if ids != ["n%d" % i for i in range(1, len(ids) + 1)]:
        errs.append("narration ids not sequential: %s..." % ids[:6])
    for field in ("content_html", "exam_tip_html", "conclusion_html"):
        if "style=" in lesson[field]:
            errs.append("inline style in %s" % field)
    yt = set(YT.findall(lesson["content_html"]))
    bad = yt - ALLOWED_YT
    if bad:
        errs.append("UNVERIFIED YouTube ids: %s" % sorted(bad))
    return ids, sorted(yt), errs


sb = get_client()
ok = True
plans = []
for lesson in LESSONS:
    slug, unit_slug = lesson["unit_match"]
    ids, yt, errs = validate(lesson)
    sub = [s for s in sb.table("subjects").select("id,school_id").eq(
        "slug", slug).execute().data if s["school_id"] is None][0]
    unit = [u for u in sb.table("units").select("id,slug").eq(
        "subject_id", sub["id"]).execute().data if u["slug"] == unit_slug][0]
    existing = sb.table("lessons").select("lesson_number,slug").eq(
        "unit_id", unit["id"]).execute().data
    nums = [l["lesson_number"] for l in existing]
    if lesson["lesson_number"] != max(nums) + 1:
        errs.append("NOT AN APPEND: want L%d, unit max is L%d"
                    % (lesson["lesson_number"], max(nums)))
    if any(l["slug"] == lesson["slug"] for l in existing):
        errs.append("slug collision")
    print("%s  %-64s L%d  %d narr ids, yt=%s"
          % ("FAIL" if errs else " ok ", lesson["title"][:64],
             lesson["lesson_number"], len(ids), ",".join(yt)))
    for e in errs:
        print("        - %s" % e)
        ok = False
    plans.append((lesson, unit["id"]))

if not ok:
    print("\nvalidation failed - nothing written")
    sys.exit(1)
if DRY:
    print("\nDRY RUN - nothing written")
    sys.exit(0)

for lesson, unit_id in plans:
    sb.table("lessons").insert({
        "unit_id": unit_id,
        "lesson_number": lesson["lesson_number"],
        "title": lesson["title"],
        "slug": lesson["slug"],
        "description": lesson["description"],
        "tier": lesson["tier"],
        "status": "pending_review",
        "content_html": lesson["content_html"],
        "conclusion_html": lesson["conclusion_html"],
        "exam_tip_html": lesson["exam_tip_html"],
        "glossary_terms": lesson["glossary_terms"],
        "knowledge_checks": lesson["knowledge_checks"],
        "practice_questions": lesson["practice_questions"],
        "flashcard_questions": lesson["flashcard_questions"],
    }).execute()
    print("inserted: %s" % lesson["title"])
print("\ndone - 2 lessons at pending_review")
