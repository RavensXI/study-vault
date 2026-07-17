# -*- coding: utf-8 -*-
import json, io

changes = {
    "key": "maths-ocr_geometry-L04",
    "problems_fixed": [],
    "issues_resolved": 0,
    "opener_concept": "A counter on a grid: slide it right/up (translation, revealed as a column vector), then fold the grid to flip a height to its negative (reflection). Names the four moves.",
    "notes": "Fresh-solved all 20 problems (8 bronze, 7 silver, 5 gold) from display: every stored solution was mathematically correct, no maths repairs needed. No degenerate/messy/duplicate-answer problems on this non-calculator lesson. Enrichment added: per-problem hint on all 20; rewrote each misconception with a derivable expect (MC expects = distractor option index reproducing the committed error; single_value expects = the wrong numeric value); guided_steps with completion boundary + check on all 4 single_value problems (silver 4/5, gold 2/4); tier_guides (bronze/silver/gold) with worked example; guided.opener (3 boxes) and guided.teach walks (bronze 4, silver 4, gold 6 boxes); tier descriptions. Trimmed method_card from 5 steps to 4 (validator max). Preserved worked_examples, topic_links, related_videos byte-for-byte.",
}
with io.open("changes_maths-ocr_geometry-L04.json", "w", encoding="utf-8") as f:
    json.dump(changes, f, indent=1, ensure_ascii=False)

diagrams = {
    "key": "maths-ocr_geometry-L04",
    "figures_added": [
        {"tier": "silver", "index": 3, "kind": "svg", "what": "Coordinate grid showing object point (5, 3) and the centre of enlargement (1, 1) for the SF 2 enlargement about a non-origin centre."},
        {"tier": "silver", "index": 4, "kind": "svg", "what": "Coordinate grid showing the object (2, 3) and its image (5, 7) for the describe-the-translation question."},
        {"tier": "gold", "index": 0, "kind": "svg", "what": "Coordinate grid showing point (3, 2) and centre (1, 1) for the SF −2 enlargement."},
        {"tier": "gold", "index": 3, "kind": "svg", "what": "Coordinate grid showing point (4, 6) and centre (2, 2) for the SF −½ enlargement."},
    ],
    "opener_touched": False,
    "notes": "Figures added where the exam prints a coordinate grid: the three enlargement-about-a-centre problems and the describe-the-translation problem. Basic axis/line reflections, origin rotations and origin enlargements posed as pure coordinate rules were left textual (matches the approved AQA sibling). All SVGs generated programmatically from each problem's own numbers, theme-safe (currentColor strokes/text, soft blue object fill #60a5fa, amber image fill #f59e0b, opacity fills), viewBox + role=img + aria-label, self-contained, under 3KB each. Every plotted coordinate/label cross-checked against the problem text.",
}
with io.open("changes_maths-ocr_geometry-L04_diagrams.json", "w", encoding="utf-8") as f:
    json.dump(diagrams, f, indent=1, ensure_ascii=False)
print("changes files written")
