# -*- coding: utf-8 -*-
"""Confirm-then-rewrite lesson descriptions that do not describe their lesson.

Found 30 Jul 2026 while repairing heroes: science-edexcel descriptions are
systematically mis-assigned (chemistry L08 "Electrolysis & Extraction of
Metals" was described as "Reversible reactions... the Haber process"), which
also broke hero selection. `description` is student-facing on browse cards.

Two stages, so a keyword false-positive never rewrites good copy:
  1. VERDICT — Haiku reads the title + the lesson's own opening content and
     judges the stored description MATCH / MISMATCH.
  2. REWRITE — only MISMATCH rows get a new description generated from the
     real content, in house style (one sentence, British English, ~12-22
     words, no "This lesson..." preamble).

School-bespoke rows are reported, never written.

    python scripts/_fix_lesson_descriptions.py            # dry run
    python scripts/_fix_lesson_descriptions.py --apply
"""
import io
import json
import os
import re
import sys

if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    os.environ["PYTHONUTF8"] = "1"
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.supabase_client import get_client
from lib.hero_pipeline import briticise

import anthropic

MODEL = "claude-haiku-4-5-20251001"
SCRATCH = os.path.join(
    r"C:\Users\tshau\AppData\Local\Temp\claude\C--Users-tshau-Documents-Study-Vault",
    r"b7ce0950-5850-4b5c-8f69-ce16ff3c08b6\scratchpad")
FLAGS = os.path.join(SCRATCH, "_desc_selfmatch.json")
LEDGER = os.path.join(SCRATCH, "_desc_fix_ledger.json")

VERDICT_PROMPT = """A GCSE revision lesson has a one-line description shown to students on browse cards.

LESSON TITLE: {title}
SUBJECT: {subject}
STORED DESCRIPTION: {description}

THE LESSON'S ACTUAL CONTENT:
{body}

Does the stored description describe THIS lesson? Judge against the WHOLE
lesson: the section headings show its full scope, so a description covering
material that only appears in a later heading is still a MATCH. Answer
MISMATCH only if the description is about a genuinely different topic.

Reply in EXACTLY this format:
VERDICT: MATCH or MISMATCH
NEW: if MISMATCH, one sentence (12-22 words) describing what this lesson actually covers, based only on the content above. British English. No "This lesson..." preamble — start with the substance, e.g. "How enzymes work, the factors affecting activity, and transport across membranes." If MATCH, write NONE."""


def plain(html, limit=1400):
    t = re.sub(r"<[^>]+>", " ", html or "")
    t = re.sub(r"&[a-z]+;", " ", t)
    return re.sub(r"\s+", " ", t).strip()[:limit]


def body_digest(html):
    """A view of the WHOLE lesson, not just its opening. Feeding only the first
    1400 characters made the judge call good descriptions mismatched whenever
    they covered later material (e.g. a two-poem lesson whose second poem sits
    below the fold) and propose a narrower replacement. Headings give whole-
    lesson scope cheaply; the opening gives voice and detail."""
    heads = re.findall(r"<h[23][^>]*>(.*?)</h[23]>", html or "", re.S | re.I)
    heads = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h)).strip() for h in heads]
    heads = [h for h in heads if h]
    out = ""
    if heads:
        out += "SECTION HEADINGS: " + " | ".join(heads[:24]) + "\n\n"
    return out + "OPENING: " + plain(html, 1100)


def main():
    apply = "--apply" in sys.argv
    flags = json.load(io.open(FLAGS, encoding="utf-8"))
    ledger = json.load(io.open(LEDGER, encoding="utf-8")) if os.path.exists(LEDGER) else {}

    sb = get_client()
    client = anthropic.Anthropic()

    todo = [f for f in flags if not f["school"] and f["lesson_id"] not in ledger]
    school = [f for f in flags if f["school"]]
    print(f"flagged: {len(flags)} | to check: {len(todo)} | "
          f"school-bespoke (report only): {len(school)} | already checked: {len(ledger)}")

    for f in todo:
        row = (sb.table("lessons").select("title,description,content_html")
               .eq("id", f["lesson_id"]).execute()).data
        if not row:
            continue
        row = row[0]
        msg = client.messages.create(
            model=MODEL, max_tokens=300,
            messages=[{"role": "user", "content": VERDICT_PROMPT.format(
                title=row["title"], subject=f["subject"],
                description=row["description"], body=body_digest(row["content_html"]))}])
        text = msg.content[0].text
        verdict = "MISMATCH" if re.search(r"VERDICT:\s*MISMATCH", text) else "MATCH"
        m = re.search(r"NEW:\s*(.+)", text, re.S)
        new = briticise((m.group(1).strip().split("\n")[0] if m else "")) if verdict == "MISMATCH" else ""
        if new.upper().startswith("NONE"):
            new, verdict = "", "MATCH"
        ledger[f["lesson_id"]] = {
            "subject": f["subject"], "unit": f["unit"], "n": f["n"],
            "title": row["title"], "verdict": verdict,
            "old": row["description"], "new": new}
        json.dump(ledger, io.open(LEDGER, "w", encoding="utf-8"),
                  indent=1, ensure_ascii=False)
        print(f"  [{verdict}] {f['subject']}/{f['unit']} L{f['n']}: {row['title'][:42]}")
        if verdict == "MISMATCH":
            print(f"      old: {(row['description'] or '')[:80]}")
            print(f"      new: {new[:80]}")

    bad = {k: v for k, v in ledger.items() if v["verdict"] == "MISMATCH" and v["new"]}
    print(f"\nconfirmed mismatches: {len(bad)} of {len(ledger)} checked "
          f"({len(ledger) - len(bad)} were false positives)")

    if not apply:
        print("DRY RUN — nothing written. Re-run with --apply.")
        return

    n = 0
    for lid, v in bad.items():
        if v.get("applied"):
            continue
        sb.table("lessons").update({"description": v["new"]}).eq("id", lid).execute()
        v["applied"] = True
        n += 1
    json.dump(ledger, io.open(LEDGER, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"applied {n} description rewrites")
    if school:
        print(f"\nschool-bespoke rows NOT touched ({len(school)}):")
        for f in school:
            print(f"  {f['subject']}/{f['unit']} L{f['n']}: {f['title'][:45]}")


if __name__ == "__main__":
    main()
