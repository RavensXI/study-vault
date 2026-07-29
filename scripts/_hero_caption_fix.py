# -*- coding: utf-8 -*-
"""Rewrite dishonest hero captions from the vision-audit ledger.

Scope: lessons whose image graded A or B (image stays) but whose stored
caption does not honestly describe it (caption_ok=false). New caption =
the audit's SHOWS sentence + any credit carried in the old caption:
    "What the image actually shows (Photo: X / Unsplash)"
C-graded lessons are excluded — they get a new image AND caption from the
repair pass. School (bespoke) subjects are excluded — report only.

    python scripts/_hero_caption_fix.py             # dry run, prints a sample
    python scripts/_hero_caption_fix.py --apply     # write to Supabase
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

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from lib.supabase_client import get_client
from lib.hero_pipeline import briticise

LEDGER = os.path.join(
    r"C:\Users\tshau\AppData\Local\Temp\claude\C--Users-tshau-Documents-Study-Vault",
    r"b7ce0950-5850-4b5c-8f69-ce16ff3c08b6\scratchpad", "_hero_vision_audit.jsonl")


def extract_credit(caption):
    """Rescue attribution from any known caption style, normalised."""
    c = caption or ""
    m = re.search(r"\(([^()]*(?:Unsplash|Wikimedia|Photo|Geograph|©)[^()]*)\)\s*$", c)
    if m:
        return m.group(1)
    m = re.search(r"Photo(?:\s+by|:)\s+([^/()—-]+?)\s*(?:on|/)\s*Unsplash", c)
    if m:
        return f"Photo: {m.group(1).strip()} / Unsplash"
    if re.search(r"Unsplash", c):
        return "Unsplash"
    if re.search(r"Wikimedia|wikipedia", c, re.I):
        return "Wikimedia Commons"
    if re.search(r"Geograph", c):
        return "Geograph"
    return ""


def is_deficient(old, title):
    """Only clearly-bad captions are auto-rewritten; substantive ones that the
    grader flagged go to a review list — an editorial caption on an engraving
    can be better teaching than a literal visual description."""
    c = (old or "").strip()
    if not c:
        return True
    if c.lower().rstrip(".") == (title or "").lower().rstrip("."):
        return True
    body = re.sub(r"\(([^()]*)\)\s*$", "", c).strip()  # caption minus credit
    if extract_credit(c) and (not body or re.fullmatch(
            r"(?:Photo|Image)[^a-zA-Z]*(?:by|:)?.{0,40}", body)):
        return True  # credit-only, no description
    return len(c) < 45


def main():
    apply = "--apply" in sys.argv
    by_id = {}
    with io.open(LEDGER, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            by_id[r["lesson_id"]] = r  # newest wins across retries

    jobs = []
    review = []
    skipped_school = 0
    for r in by_id.values():
        if r["grade"] not in ("A", "B") or r.get("caption_ok"):
            continue
        if not r.get("shows"):
            continue
        if r.get("school"):
            skipped_school += 1
            continue
        credit = extract_credit(r.get("caption"))
        shows = briticise(r["shows"].rstrip("."))
        new_caption = f"{shows} ({credit})" if credit else f"{shows}."
        job = {"lesson_id": r["lesson_id"], "subject": r["subject"],
               "unit": r["unit"], "n": r["n"], "title": r["title"],
               "old": r.get("caption") or "", "new": new_caption}
        if is_deficient(job["old"], job["title"]):
            jobs.append(job)
        else:
            review.append(job)

    print(f"captions to rewrite (deficient): {len(jobs)}")
    print(f"flagged but substantive — review list, untouched: {len(review)}")
    print(f"school-bespoke excluded: {skipped_school}")
    review_path = os.path.join(os.path.dirname(LEDGER), "_hero_caption_review.json")
    with io.open(review_path, "w", encoding="utf-8") as f:
        json.dump(review, f, indent=1, ensure_ascii=False)
    for j in jobs[:8]:
        print(f"\n[{j['subject']}/{j['unit']} L{j['n']}] {j['title'][:50]}")
        print(f"  OLD: {j['old'][:100]}")
        print(f"  NEW: {j['new'][:100]}")

    if not apply:
        print("\nDRY RUN — nothing written. Re-run with --apply.")
        return

    sb = get_client()
    n = 0
    for j in jobs:
        sb.table("lessons").update({"hero_image_caption": j["new"]}) \
            .eq("id", j["lesson_id"]).execute()
        n += 1
        if n % 100 == 0:
            print(f"  {n}/{len(jobs)}")
    print(f"applied {n} caption rewrites")


if __name__ == "__main__":
    main()
