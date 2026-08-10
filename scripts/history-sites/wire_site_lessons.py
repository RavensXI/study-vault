# -*- coding: utf-8 -*-
"""Validate and wire the 2027 historic-environment site lessons.

Five lessons: four free-tier (history-aqa) + one Unity (history). APPEND ONLY —
each lesson must land at max(lesson_number)+1 in its unit, and the script
refuses to touch any existing row.

Usage:
    python scripts/history-sites/wire_site_lessons.py --dry-run            # 2027 set
    python scripts/history-sites/wire_site_lessons.py --set 2028 --dry-run
    python scripts/history-sites/wire_site_lessons.py --set 2028
"""
import re
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from lib.supabase_client import get_client

if "2028" in (sys.argv[sys.argv.index("--set") + 1] if "--set" in sys.argv else "2027"):
    from site_lessons_2028_a import LESSONS as LESSONS_A
    from site_lessons_2028_b import LESSONS as LESSONS_B
else:
    from site_lessons_a import LESSONS as LESSONS_A
    from site_lessons_b import LESSONS as LESSONS_B

DRY = "--dry-run" in sys.argv
ALL = LESSONS_A + LESSONS_B
ENTITY = re.compile(r"&(?:[a-zA-Z]+|#\d+);")
NARR = re.compile(r'data-narration-id="(n\d+)"')

def fail(msgs, m):
    msgs.append(m)

def validate(lesson):
    errs = []
    t = lesson["title"]
    # --- plain-text fields must not contain HTML entities ---
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
            fail(errs, "entity in plain-text field: %r" % ENTITY.search(p).group())
        if "<" in p and ">" in p:
            fail(errs, "HTML in plain-text field: %r" % p[:60])
    # --- counts ---
    if len(lesson["knowledge_checks"]) != 5:
        fail(errs, "KC count %d != 5" % len(lesson["knowledge_checks"]))
    if len(lesson["practice_questions"]) != 6:
        fail(errs, "PQ count %d != 6" % len(lesson["practice_questions"]))
    if len(lesson["flashcard_questions"]) != 5:
        fail(errs, "flashcard count %d != 5" % len(lesson["flashcard_questions"]))
    if len(lesson["glossary_terms"]) < 5:
        fail(errs, "glossary %d < 5" % len(lesson["glossary_terms"]))
    # --- KC shape ---
    for k in lesson["knowledge_checks"]:
        if set(k) != {"q", "type", "correct", "options"} or k["type"] != "mcq":
            fail(errs, "KC shape wrong: %r" % sorted(k))
        elif not (len(k["options"]) == 4 and 0 <= k["correct"] < 4):
            fail(errs, "KC options/correct wrong: %r" % k["q"][:40])
    # --- narration ids sequential + unique across the three html fields ---
    ids = NARR.findall(lesson["content_html"]) + NARR.findall(
        lesson["exam_tip_html"]) + NARR.findall(lesson["conclusion_html"])
    want = ["n%d" % i for i in range(1, len(ids) + 1)]
    if ids != want:
        fail(errs, "narration ids not sequential: %s..." % ids[:8])
    # --- style hygiene ---
    for field in ("content_html", "exam_tip_html", "conclusion_html"):
        if "style=" in lesson[field]:
            fail(errs, "inline style in %s" % field)
        if "border-left" in lesson[field]:
            fail(errs, "border-left in %s" % field)
    return t, ids, errs

sb = get_client()
ok = True
plans = []
for lesson in ALL:
    slug, unit_frag = lesson["unit_match"]
    title, ids, errs = validate(lesson)
    subs = sb.table("subjects").select("id,school_id").eq("slug", slug).execute().data
    # history-aqa is generic; 'history' must be the Unity row
    sub = [s for s in subs if (s["school_id"] is None) == (slug == "history-aqa")][0]
    unit = [u for u in sb.table("units").select("id,name").eq(
        "subject_id", sub["id"]).execute().data if unit_frag in u["name"]][0]
    existing = sb.table("lessons").select("lesson_number,slug").eq(
        "unit_id", unit["id"]).execute().data
    nums = [l["lesson_number"] for l in existing]
    if lesson["lesson_number"] != max(nums) + 1:
        fail(errs, "NOT AN APPEND: want L%d but unit max is L%d"
             % (lesson["lesson_number"], max(nums)))
    if lesson["lesson_number"] in nums:
        fail(errs, "L%d already exists in unit" % lesson["lesson_number"])
    if any(l["slug"] == lesson["slug"] for l in existing):
        fail(errs, "slug collision: %s" % lesson["slug"])
    tag = "UNITY" if sub["school_id"] else "free"
    print("%s  %-58s -> %s L%d  (%d narration ids)"
          % ("FAIL" if errs else " ok ", title[:58], tag,
             lesson["lesson_number"], len(ids)))
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
    row = {
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
    }
    sb.table("lessons").insert(row).execute()
    print("inserted: %s" % lesson["title"])
print("\ndone - 5 lessons at pending_review")
