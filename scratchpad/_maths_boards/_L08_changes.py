# -*- coding: utf-8 -*-
import json

changes = {
    "key": "maths-eduqas_geometry-L08",
    "problems_fixed": [
        {"tier": "gold", "index": 4,
         "what": "Stored solution marked option 0 ('5') but the correct answer |2a-b|=sqrt26 was option 1; reordered options so sqrt26 is index 0 (house convention, solutions stays [0]).",
         "old": "options ['5','sqrt26','sqrt5','sqrt10'], solutions [0] -> pointed at wrong answer '5'",
         "new": "options ['sqrt26','5','sqrt10','sqrt5'], solutions [0] -> correct"},
        {"tier": "gold", "index": 1,
         "what": "Distractor option[2] '(3/2)a+3b' was algebraically identical to the correct answer (3/2)(a+2b); ambiguous multiple-choice.",
         "old": "\\(\\frac{3}{2}\\mathbf{a} + 3\\mathbf{b}\\)",
         "new": "\\(\\frac{3}{2}\\mathbf{a} + 6\\mathbf{b}\\) (only-first-term-halved error)"},
        {"tier": "gold", "index": 3,
         "what": "Distractor option[1] '2a+b-a' simplifies to a+b = the correct answer; ambiguous multiple-choice.",
         "old": "\\(2\\mathbf{a} + \\mathbf{b} - \\mathbf{a}\\)",
         "new": "\\(2\\mathbf{a} + \\mathbf{b}\\) (forgot-to-subtract error = OC itself)"},
    ],
    "issues_resolved": 3,
    "opener_concept": "A drone flies 3 right/2 up then 1 right/4 up; totalling each direction (4 right, 6 up) IS adding the column vectors (3,2)+(1,4)=(4,6). Grid SVG shows the two-leg journey.",
    "notes": ("All 20 bank problems fresh-solved from display; every stored solution "
              "verified (correct answer = option index 0 throughout, except the gold[4] "
              "flat-wrong solution fixed above). Added missing hint to every problem (none "
              "had one). Added expect (distractor option index) to all 40 misconceptions so "
              "honest diagnosis fires per wrong option; all rewritten to unicode minus, no "
              "em dashes. Added guided.opener, guided.teach (bronze/silver/gold, 4+ numeric "
              "boxes each, verified to land on stored answers), and tier_guides (3). "
              "Stripped em dashes from preserved worked_examples step labels (' — ' -> ': ') "
              "to satisfy the style gate. method_card / topic_links / related_videos / "
              "worked_examples otherwise preserved. Validator PASS.")
}
json.dump(changes, open("changes_maths-eduqas_geometry-L08.json", "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)

diag = {
    "key": "maths-eduqas_geometry-L08",
    "figures_added": [
        {"tier": "bronze", "index": 6, "kind": "svg", "what": "Grid with A, B and a solid arrow A->B labelled (3,4); makes 'reverse direction' concrete."},
        {"tier": "silver", "index": 0, "kind": "svg", "what": "Right-angled triangle, legs 3 and 4, hypotenuse '?' (magnitude via Pythagoras)."},
        {"tier": "silver", "index": 1, "kind": "svg", "what": "Right-angled triangle, legs 6 and 8, hypotenuse '?' for |(-6,8)|."},
        {"tier": "silver", "index": 2, "kind": "svg", "what": "Triangle O-A-B: a=O->A, b=O->B, AB dashed with '?' (find AB)."},
        {"tier": "silver", "index": 3, "kind": "svg", "what": "Coordinate grid plotting O, A(2,6), B(8,2) and midpoint M(5,4) on segment AB."},
        {"tier": "silver", "index": 5, "kind": "svg", "what": "Segment P..R..Q with R one third of the way from P."},
        {"tier": "gold", "index": 0, "kind": "svg", "what": "Triangle O-A-B with P on AB dividing it 2:1 from A (P shown nearer B)."},
        {"tier": "gold", "index": 1, "kind": "svg", "what": "Triangle O-A-B with midpoint M of AB marked (schematic; OA=3a, OB=6b in text)."},
    ],
    "opener_touched": True,
    "notes": ("Figures added only where an exam would print one. Column-vector arithmetic "
              "(bronze 0-5,7; gold 4) left textual per the exam-realism test. All SVGs are "
              "theme-safe (currentColor text/outlines, soft fills with fill-opacity), self-"
              "contained, right angles and tick-free, 'Diagram not drawn accurately' caption "
              "on the not-to-scale triangles. Opener carries a grid SVG of the drone journey. "
              "Every visible number matches the problem text; figures generated "
              "programmatically from each problem's own values and eyeballed in-browser. "
              "Validator PASS on the live data.")
}
json.dump(diag, open("changes_maths-eduqas_geometry-L08_diagrams.json", "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print("wrote both changes files")
