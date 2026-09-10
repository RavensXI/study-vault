# -*- coding: utf-8 -*-
"""Normalise practice-question `type` labels across the rebuilt Drama units.

Why this exists. The cross-lesson unitcheck ruled — correctly — that presenting
a fixed ladder of per-question mark tariffs as though it were the structure of
the set-text section is unevidenced: the specification gives only the 4 / 44 / 32
part totals. The fix pass therefore stripped the tariffs from the question-type
labels. But each play's fix pass invented its own wording, and one play was left
half-converted, so the three units disagreed with each other.

This maps every observed variant onto one canonical set, deterministically, with
no model call. The canonical names keep the command word (which is what the
student needs to recognise) and drop the invented tariff.

Usage:
  python scripts/api_build/normalise_drama_question_types.py <lessons_dir>
  python scripts/api_build/normalise_drama_question_types.py <lessons_dir> --write
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

CANON = {
    "identify": "Identify",
    "define": "Define",
    "explain the effect": "Explain the effect",
    "explain effect": "Explain the effect",
    "short analysis": "Short analysis",
    "interpret as performer": "Interpret as a performer",
    "interpret as a performer": "Interpret as a performer",
    "interpret as designer": "Interpret as a designer",
    "interpret as a designer": "Interpret as a designer",
    "analyse intentions": "Analyse the playwright's intentions",
    "analyse the playwright's intentions": "Analyse the playwright's intentions",
    "extended staging response": "Extended staging response",
    "extended practice": "Extended staging response",
}

STRIP = re.compile(
    r"^\s*(?:\d+\s*marks?\s*[—\-–]\s*)?"      # "8 marks — "
    r"(?:practice:\s*)?"                        # "Practice: "
    r"(.*?)"
    r"\s*(?:\((?:short|extended)\s+answer\))?\s*$",  # " (short answer)"
    re.IGNORECASE)


def canon(label):
    m = STRIP.match(label or "")
    core = (m.group(1) if m else label or "").strip().lower().rstrip(".")
    return CANON.get(core)


def main(lessons_dir, write):
    unmapped = {}
    changed = 0
    for fn in sorted(os.listdir(lessons_dir)):
        if not fn.endswith(".json"):
            continue
        p = os.path.join(lessons_dir, fn)
        obj = json.load(io.open(p, encoding="utf-8"))
        touched = False
        for q in obj.get("practice_questions", []):
            new = canon(q.get("type"))
            if new is None:
                unmapped.setdefault(q.get("type"), []).append(fn[:-5])
                continue
            if new != q.get("type"):
                q["type"] = new
                touched = True
                changed += 1
        if touched:
            print("  %-34s normalised" % fn[:-5])
            if write:
                io.open(p, "w", encoding="utf-8").write(
                    json.dumps(obj, ensure_ascii=False, indent=1))
    if unmapped:
        print("UNMAPPED types (fix by hand):")
        for k, v in unmapped.items():
            print("   %r in %s" % (k, sorted(set(v))))
    print(("WROTE " if write else "DRY RUN ") + "%d label changes" % changed)


if __name__ == "__main__":
    main(sys.argv[1], "--write" in sys.argv)
