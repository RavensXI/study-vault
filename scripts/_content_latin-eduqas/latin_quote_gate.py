# -*- coding: utf-8 -*-
"""Deterministic Latin-quotation gate for the Latin literature lessons.

The poetry build's gate looks inside quotation marks. Latin lessons put their
quotations inside <em> and <strong> instead (that is the platform's house style
and how the narration pipeline segments foreign text), so this gate walks those
tags rather than quote marks.

Every <em>/<strong> span in a set-text lesson must appear VERBATIM, after
normalisation, somewhere in that unit's published booklets — the prescribed
text, the student booklet, the board's translation and its commentary. A span
that matches nothing in any of them is either an invented Latin phrase or an
English emphasis the corpus happens not to contain; both are worth a human or
fact-checker glance, which is exactly what the report is for.

Lessons in the language unit are skipped: that component is unseen, so its
illustrative Latin is legitimately composed rather than quoted.

Usage: python scripts/_content_latin-eduqas/latin_quote_gate.py [out.json]
Exit 0 = clean, 1 = misses found.
"""
import html
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "scripts", "api_build"))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

import driver as D  # noqa: E402

CFG_PATH = os.path.join(HERE, "config_latin-eduqas.json")

CORPORA = {
    "heroes-and-villains": ["comp2_heroes_and_villains", "comp2_heroes_student_booklet",
                            "comp2_heroes_translation", "comp2_heroes_notes_commentary",
                            "comp2_heroes_vocabulary"],
    "come-dine-with-me": ["comp2_come_dine_with_me", "comp2_come_dine_student_booklet",
                          "comp2_come_dine_translation",
                          "comp2_come_dine_notes_commentary",
                          "comp2_come_dine_vocabulary"],
    "narratives-livy-and-virgil": [
        "comp3a_livy_hannibal", "comp3a_livy_hannibal_student_booklet",
        "comp3a_livy_hannibal_translation", "comp3a_livy_hannibal_notes_commentary",
        "comp3a_livy_hannibal_vocabulary",
        "comp3a_virgil_hercules_cacus", "comp3a_virgil_hercules_cacus_student_booklet",
        "comp3a_virgil_hercules_cacus_translation",
        "comp3a_virgil_hercules_cacus_notes_commentary",
        "comp3a_virgil_hercules_cacus_vocabulary"],
    "roman-civilisation": ["comp3b_slavery", "comp3b_festivals"],
}

TAG_RE = re.compile(r"<(em|strong)\b[^>]*>(.*?)</\1>", re.S | re.I)


def norm(s):
    s = html.unescape(s)
    s = s.replace("‘", "'").replace("’", "'")
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"[^a-z0-9' ]", " ", s.casefold())
    return re.sub(r"\s+", " ", s).strip()


def spans(obj):
    for field in ("content_html", "exam_tip_html", "conclusion_html"):
        for m in TAG_RE.finditer(obj.get(field) or ""):
            span = norm(m.group(2))
            if span and len(span) >= 4:
                yield span


def main():
    cfg = D.load_config(CFG_PATH)
    out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        cfg["run_dir"], "latin_quote_gate.json")
    corpora = {}
    for unit, names in CORPORA.items():
        corpora[unit] = norm("\n".join(
            D.read(os.path.join(cfg["source_dir"], n + ".md")) for n in names))

    lessons_dir = os.path.join(cfg["run_dir"], "lessons")
    report, total, misses = {}, 0, 0
    for fn in sorted(os.listdir(lessons_dir)):
        if not fn.endswith(".json"):
            continue
        unit = fn[:-5].rsplit("-L", 1)[0]
        corpus = corpora.get(unit)
        if not corpus:
            continue
        obj = json.load(io.open(os.path.join(lessons_dir, fn), encoding="utf-8"))
        bad = []
        for span in spans(obj):
            total += 1
            if span not in corpus:
                bad.append(span)
        if bad:
            report[fn[:-5]] = sorted(set(bad))
            misses += len(set(bad))
    io.open(out_path, "w", encoding="utf-8").write(json.dumps(
        {"total_spans": total, "lessons_with_misses": report},
        ensure_ascii=False, indent=1))
    print("latin quote gate: %d emphasised spans checked, %d distinct misses "
          "across %d lessons" % (total, misses, len(report)))
    for les, bads in sorted(report.items()):
        for b in bads[:8]:
            print("  MISS %s: %s" % (les, b[:90]))
    return 1 if report else 0


if __name__ == "__main__":
    sys.exit(main())
