# -*- coding: utf-8 -*-
"""Surgical fix: align English Language 8700 practice drills with AQA's 2026
Paper 1 format changes (source: https://www.aqa.org.uk/english-language-changes).

Changes applied:
  Q1  — now multiple choice (shade the four true statements); drills reworded
        away from the dead "List four things" free-response framing.
  Q3  — now names a single effect ("...to create suspense"); the old
        "interest you as a reader" wording replaced in L4/L5 exam-info cards.
  Q5  — narrative option may now be an OPENING; walkthrough method card notes it.

Touches: free-tier english-language-aqa (paper-1-reading L1/L4/L5/L8,
paper-1-writing L7) and Unity english-language (paper-1-reading L8).
Backups of each lesson's practice_data land in scripts/_englang_8700_backup/.
Every needle must match EXACTLY the expected number of times or the lesson is
skipped with an error — no partial writes.
"""
import json
import os
import sys
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

URL = os.environ["SUPABASE_URL"]
KEY = os.environ["SUPABASE_SERVICE_KEY"]
BACKUP_DIR = Path(__file__).resolve().parent / "_englang_8700_backup"
BACKUP_DIR.mkdir(exist_ok=True)


def req(path, method="GET", body=None):
    headers = {"apikey": KEY, "Authorization": "Bearer " + KEY,
               "Content-Type": "application/json", "Prefer": "return=representation"}
    r = urllib.request.Request(URL + "/rest/v1/" + path, method=method,
                               data=json.dumps(body).encode() if body else None,
                               headers=headers)
    return json.load(urllib.request.urlopen(r))


# (subject_slug, school_filter, unit_slug, lesson_number, [(needle, replacement, expected_count)])
JOBS = [
    ("english-language-aqa", "is.null", "paper-1-reading", 1, [
        ("List four things you learn about Nadia from Extract A.",
         "Identify four things you learn about Nadia from Extract A. (In the exam, Q1 is now multiple choice — you shade the four true statements.)", 1),
    ]),
    ("english-language-aqa", "is.null", "paper-1-reading", 4, [
        ("how does the writer structure the text to interest you as a reader?",
         "how has the writer structured the text to create a specific effect, such as suspense or tension?", 1),
    ]),
    ("english-language-aqa", "is.null", "paper-1-reading", 5, [
        ("how does the writer structure the text to interest you as a reader?",
         "how has the writer structured the text to create a specific effect, such as suspense or tension?", 1),
    ]),
    ("english-language-aqa", "is.null", "paper-1-reading", 8, [
        ("List four things you learn about the boat journey from Extract A.",
         "Identify four things you learn about the boat journey from Extract A.", 1),
        ("For Q1, scan for directly stated facts. Do not infer — only list what the text explicitly says.",
         "For Q1, scan for directly stated facts. In the exam you shade the four true statements in a multiple-choice list — check each against the text, and do not infer.", 1),
        ("List four things you learn about the crossing.",
         "Shade the four true statements about the crossing.", 1),
        ("Q1 asks for directly stated facts — 4 marks, about 5 minutes.",
         "Q1 is multiple choice — you shade the four true statements. Directly stated facts, 4 marks, about 5 minutes.", 1),
        ("Q1 (4 marks, ~5 mins): list explicit information. Short, factual points.",
         "Q1 (4 marks, ~5 mins): multiple choice — shade the four true statements. Explicit information only.", 1),
        ("Q3 asks about beginnings, endings, focus shifts, and pacing — 8 marks, about 10 minutes.",
         "Q3 names one effect (such as suspense) and asks how the structure creates it — through beginnings, endings, focus shifts, and pacing. 8 marks, about 10 minutes.", 1),
        ("Q3 (8 marks, ~10 mins): analyse structure. Consider beginnings, endings, focus shifts.",
         "Q3 (8 marks, ~10 mins): analyse how the structure creates the named effect — beginnings, endings, focus shifts.", 1),
    ]),
    ("english-language-aqa", "is.null", "paper-1-writing", 7, [
        ("Read the prompt carefully — choose the option that sparks a vivid image",
         "Read the prompt carefully — choose the option that sparks a vivid image (for the story option, you may write just the opening)", 1),
    ]),
    ("english-language", "not.is.null", "paper-1-reading", 8, [
        ("List four things you learn about Agnes from this part of the source.",
         "Identify four things you learn about Agnes from this part of the source.", 1),
        ("This is a Q1-style question — you need four clear pieces of information.",
         "This is a Q1-style question — you need four clear pieces of information. (In the exam, Q1 is now multiple choice — you shade the four true statements.)", 1),
    ]),
]


def replace_in(node, needle, replacement, counter):
    if isinstance(node, dict):
        return {k: replace_in(v, needle, replacement, counter) for k, v in node.items()}
    if isinstance(node, list):
        return [replace_in(v, needle, replacement, counter) for v in node]
    if isinstance(node, str) and needle in node:
        counter[0] += node.count(needle)
        return node.replace(needle, replacement)
    return node


def main():
    ok = fail = 0
    for slug, school_filter, unit_slug, lesson_number, edits in JOBS:
        s = req(f"subjects?select=id&slug=eq.{slug}&school_id={school_filter}")[0]
        unit = [u for u in req(f"units?select=id,slug&subject_id=eq.{s['id']}")
                if u["slug"] == unit_slug][0]
        lesson = req(f"lessons?select=id,practice_data&unit_id=eq.{unit['id']}"
                     f"&lesson_number=eq.{lesson_number}")[0]

        backup = BACKUP_DIR / f"{slug}__{unit_slug}__L{lesson_number}.json"
        backup.write_text(json.dumps(lesson["practice_data"], ensure_ascii=False, indent=1),
                          encoding="utf-8")

        data = lesson["practice_data"]
        problems = []
        for needle, replacement, expected in edits:
            counter = [0]
            data = replace_in(data, needle, replacement, counter)
            if counter[0] != expected:
                problems.append(f"needle matched {counter[0]}x (expected {expected}): {needle[:70]}")
        if problems:
            fail += 1
            print(f"SKIP {slug} {unit_slug} L{lesson_number} — no write:")
            for p in problems:
                print("   ", p)
            continue

        req(f"lessons?id=eq.{lesson['id']}", method="PATCH", body={"practice_data": data})
        ok += 1
        print(f"FIXED {slug} {unit_slug} L{lesson_number} ({len(edits)} edits, backup {backup.name})")

    print(f"\ndone: {ok} lessons patched, {fail} skipped")
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
