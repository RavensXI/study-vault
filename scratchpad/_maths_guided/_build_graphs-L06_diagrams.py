# -*- coding: utf-8 -*-
"""Diagram pass for graphs-L06 (Trigonometric Graphs, id 4aa9afe1-...).

The checker FAILed four trig-GRAPH charts that had nothing to do with the
sine/cosine-rule + area-of-triangle solves they were pinned to, and raised a
coverage FAIL: none of the triangle problems carried a labelled triangle.

graphs-L06 shares its problem bank 1:1 with geometry-L06, whose diagram pass
is already verified: correct labelled-triangle SVGs on every geometric
problem, no figure on the two purely-arithmetic ones (bronze[4], bronze[6]),
and an opener that carries the flag SVG in its display (no non-sequitur
sin-graph). We adopt that treatment surgically: replace only `display` on each
problem (question text is byte-identical between the two lessons) and the
opener; drop the four bad charts; touch nothing else.
"""
import json, io

SRC = "_L06_diag_fresh.json"        # fresh live graphs-L06 practice_data
REF = "lesson_geometry-L06_diagrams.json"  # verified sibling figures
OUT = "lesson_graphs-L06_diagrams.json"

pd  = json.load(io.open(SRC, encoding="utf-8"))
ref = json.load(io.open(REF, encoding="utf-8"))

def tail(disp):
    i = disp.rfind("</span>")
    if i >= 0: return disp[i + 7:].strip()
    i = disp.rfind("</svg>")
    if i >= 0: return disp[i + 6:].strip()
    return disp.strip()

figures = []
charts_removed = []

for tier in ("bronze", "silver", "gold"):
    xprobs = pd["problem_bank"][tier]
    gprobs = ref["problem_bank"][tier]
    for i, p in enumerate(xprobs):
        t = tail(p["display"])
        matches = [q for q in gprobs if tail(q["display"]) == t]
        assert len(matches) == 1, "ambiguous/no match for %s[%d]: %r" % (tier, i, t)
        g = matches[0]
        # sanity: identical question text preserved
        assert tail(g["display"]) == t
        had_chart = "chart" in p
        new_disp = g["display"]
        has_svg = "<svg" in new_disp
        if p["display"] != new_disp:
            p["display"] = new_disp
        if had_chart:
            del p["chart"]
            charts_removed.append("%s[%d]" % (tier, i))
        if has_svg:
            figures.append({"tier": tier, "index": i, "kind": "svg",
                            "what": t[:70]})

# Opener: adopt sibling's (flag SVG in display, no non-sequitur sin-graph).
pd["guided"]["opener"] = ref["guided"]["opener"]
opener_touched = True

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("charts removed:", charts_removed)
print("svg figures now present on:", len(figures), "problems")
print("opener touched:", opener_touched)
