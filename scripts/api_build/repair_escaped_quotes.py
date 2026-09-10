# -*- coding: utf-8 -*-
"""Repair literal backslash-escaped quotes in generated lesson JSON.

Symptom: a lesson's stored text contains a LITERAL backslash before a quote
mark — the student sees \"brighter lights\" instead of a quoted phrase. The
model double-escaped the quote while writing JSON, so the escape survived
json.loads and became part of the value.

Found on 9 September 2026 in all 24 lessons of the Drama set-play rebuild: 728
occurrences, mostly in practice_questions.marks (the rubric strings, which quote
weak student phrasing a lot), flashcards, glossary definitions and content_html.

The repair is deterministic and pairs-aware:
  *_html fields      -> &ldquo;...&rdquo;   (entities, per the house rule)
  plain-text fields  -> curly quotes         (unicode, per the house rule)
  unpaired leftovers -> the backslash is dropped, the quote kept

Run with --write to save; without it, prints what it would change.

Usage:
  python scripts/api_build/repair_escaped_quotes.py <lessons_dir>
  python scripts/api_build/repair_escaped_quotes.py <lessons_dir> --write
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HTML_FIELDS = {"content_html", "exam_tip_html", "conclusion_html"}
PAIR = re.compile(r'\\"([^"\\]{0,200}?)\\"')
SINGLE_PAIR = re.compile(r"\\'([^'\\]{0,200}?)\\'")


UNI = re.compile(r"\\u([0-9a-fA-F]{4})")


def repair(text, html):
    open_q, close_q = ("&ldquo;", "&rdquo;") if html else ("“", "”")
    out = PAIR.sub(lambda m: open_q + m.group(1) + close_q, text)
    out = SINGLE_PAIR.sub(lambda m: "‘" + m.group(1) + "’", out)
    # anything still escaped was unpaired: keep the quote, drop the backslash
    out = out.replace('\\"', "&quot;" if html else '"').replace("\\'", "'")
    # a surviving \uXXXX escape renders to the student as those six characters
    out = UNI.sub(lambda m: chr(int(m.group(1), 16)), out)
    return out


def walk(node, html):
    """Rewrite every string in place. `html` tracks whether we are inside an
    *_html field, because the two field families use different quote styles."""
    if isinstance(node, dict):
        return {k: walk(v, html or k in HTML_FIELDS) for k, v in node.items()}
    if isinstance(node, list):
        return [walk(v, html) for v in node]
    if isinstance(node, str):
        return repair(node, html)
    return node


def count(node):
    if isinstance(node, dict):
        return sum(count(v) for v in node.values())
    if isinstance(node, list):
        return sum(count(v) for v in node)
    if isinstance(node, str):
        return (node.count('\\"') + node.count("\\'")
                + len(UNI.findall(node)))
    return 0


def main(lessons_dir, write):
    total = 0
    for fn in sorted(os.listdir(lessons_dir)):
        if not fn.endswith(".json"):
            continue
        p = os.path.join(lessons_dir, fn)
        obj = json.load(io.open(p, encoding="utf-8"))
        n = count(obj)
        if not n:
            continue
        total += n
        fixed = walk(obj, False)
        left = count(fixed)
        print("%-34s %3d artefacts -> %d remaining" % (fn[:-5], n, left))
        if write:
            io.open(p, "w", encoding="utf-8").write(
                json.dumps(fixed, ensure_ascii=False, indent=1))
    print(("REPAIRED" if write else "DRY RUN") + ": %d artefacts across %s"
          % (total, lessons_dir))


if __name__ == "__main__":
    main(sys.argv[1], "--write" in sys.argv)
