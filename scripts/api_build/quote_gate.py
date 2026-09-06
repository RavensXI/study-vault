# -*- coding: utf-8 -*-
"""Deterministic quotation gate for anthology lesson builds.

Every quoted span found in the generated lesson JSONs must appear VERBATIM
(after quote/dash/whitespace normalisation) somewhere in the anthology poems
file. Reports misses per lesson — the model-based fact-check then adjudicates
whether each miss is a hallucinated poem quote or an innocently quoted term.

Usage: python quote_gate.py <poems.txt> <lessons_dir> <out_report.json>
Exit 0 = all clean, 1 = misses found.
"""
import html
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


BRACKET_RE = re.compile(r"\[[^\]]*\]")


def variants(span):
    """A quotation may carry an editorial insertion in square brackets — the
    standard way to bend a line into a sentence ("she 'work[s] willingly'").
    Accept the span with the bracketed text removed as well as verbatim, so the
    convention is not reported as a fabrication. An invented word still misses
    both ways."""
    yield norm(span)
    stripped = BRACKET_RE.sub("", span)
    if stripped != span:
        yield norm(stripped)


QUOTE_RE = re.compile(
    r"“([^”]{6,160})”"    # curly double
    r"|\"([^\"]{6,160})\""               # straight double
    r"|‘([^’]{6,160})’"   # curly single
    # Straight single quotes, conservatively: the opening mark must not follow a
    # letter and the closing mark must not precede one, so possessives and
    # contractions ("Lamb's", "don't", "the poets' methods") never open a span.
    r"|(?<![A-Za-z])'([^'\n]{6,160})'(?![A-Za-z])",
)

# A cloze question ("tun _____ upside dung") can never match the corpus and is
# not a claim about wording, so it is not a gate failure.
CLOZE_RE = re.compile(r"_{2,}")
NESTED_RE = re.compile(r"[“”‘’\"]")


def spans_in(text):
    for m in QUOTE_RE.finditer(text):
        span = next(g for g in m.groups() if g)
        if len(span.split()) < 2:
            continue
        if CLOZE_RE.search(span) or NESTED_RE.search(span):
            continue
        yield span


def walk_strings(node, key=None):
    # A multiple-choice question's wrong answers are SUPPOSED to be things the
    # poem does not say, so quoted distractors are not fabrications and must not
    # be gated. The correct answer is still checked wherever the lesson quotes
    # it in prose.
    if key == "options":
        return
    if isinstance(node, dict):
        for k, v in node.items():
            yield from walk_strings(v, k)
    elif isinstance(node, list):
        for v in node:
            yield from walk_strings(v, key)
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
            # *_html fields carry entities, so &ldquo;...&rdquo; is where most
            # quotations actually live. Unescape BEFORE looking for quote marks
            # or the gate silently checks almost nothing.
            plain = html.unescape(re.sub(r"<[^>]+>", " ", html.unescape(text)))
            for span in spans_in(plain):
                total += 1
                if not any(v in corpus for v in variants(span)):
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
