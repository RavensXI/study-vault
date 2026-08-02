# -*- coding: utf-8 -*-
"""Deterministic quotation gate for anthology lesson builds.

Every quoted span found in the generated lesson JSONs must appear VERBATIM
(after quote/dash/whitespace normalisation) somewhere in the anthology poems
file. Reports misses per lesson — the model-based fact-check then adjudicates
whether each miss is a hallucinated poem quote or an innocently quoted term.

Usage: python quote_gate.py <poems.txt> <lessons_dir> <out_report.json>
Exit 0 = all clean, 1 = misses found.
"""
import io
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def norm(s):
    """Word-level normalisation: case-, punctuation- and line-break-insensitive.
    An invented WORD still misses; sentence styling around a real quote does not."""
    s = s.replace("‘", "'").replace("’", "'")
    s = re.sub(r"[^a-z0-9' ]", " ", s.casefold())
    return re.sub(r"\s+", " ", s).strip()


QUOTE_RE = re.compile(
    r"“([^”]{6,160})”"    # curly double
    r"|\"([^\"]{6,160})\""               # straight double
    r"|‘([^’]{6,160})’",  # curly single
)


def spans_in(text):
    for m in QUOTE_RE.finditer(text):
        span = next(g for g in m.groups() if g)
        if len(span.split()) >= 2:
            yield span


def walk_strings(node):
    if isinstance(node, dict):
        for v in node.values():
            yield from walk_strings(v)
    elif isinstance(node, list):
        for v in node:
            yield from walk_strings(v)
    elif isinstance(node, str):
        yield node


def main(poems_path, lessons_dir, out_path):
    corpus = norm(io.open(poems_path, encoding="utf-8").read())
    report = {}
    total = misses = 0
    for fn in sorted(os.listdir(lessons_dir)):
        if not fn.endswith(".json"):
            continue
        obj = json.load(io.open(os.path.join(lessons_dir, fn), encoding="utf-8"))
        bad = []
        for text in walk_strings(obj):
            plain = re.sub(r"<[^>]+>", " ", text)
            for span in spans_in(plain):
                total += 1
                if norm(span) not in corpus:
                    bad.append(span)
        if bad:
            report[fn[:-5]] = sorted(set(bad))
            misses += len(set(bad))
    io.open(out_path, "w", encoding="utf-8").write(
        json.dumps({"total_quoted_spans": total, "lessons_with_misses": report},
                   ensure_ascii=False, indent=1))
    print("quote gate: %d quoted spans checked, %d distinct misses in %d lessons"
          % (total, misses, len(report)))
    for les, bads in sorted(report.items()):
        for b in bads[:6]:
            print("  MISS %s: %s" % (les, b[:90]))
    return 1 if report else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3]))
