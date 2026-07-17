# -*- coding: utf-8 -*-
import json, io

changes = {
    "key": "number-L03",
    "board": "maths-ocr",
    "problems_fixed": [],  # bank fresh-solved: all 20 solutions correct, no dups, non-calc clean
    "issues_resolved": 0,
    "opener_concept": "Rounding a £3.84 bill to whole pounds on a number line: read the part after the point, cross the 0.5 halfway mark, round up or stay. Names the halfway-mark rule that underlies d.p. and s.f.",
    "notes": ("Full guided conversion. Added hint + guided_steps to all 20 problems "
        "(single_value), tier_guides (bronze/silver/gold), guided.opener with number-line "
        "SVG, guided.teach walks per tier, slim method_card. Honest-diagnosis expects added "
        "where a determinate wrong value exists AND it clears the validator's 0.011 tolerance: "
        "bronze[0,1,4,5,6], silver[0,3,4,5,6], gold[0,1,4]. Misconceptions dropped where the "
        "natural wrong answer sits within 0.011 of the solution (bronze[2]=0.73/0.72, "
        "bronze[3]=5.99/6, silver[1]=0.0034/0.0035, gold[2]=0.99/1) and where no single "
        "determinate wrong value exists (bronze[7] add, silver[2] estimate, gold[3] estimate). "
        "Preservation: topic_links, related_videos, worked_examples kept; only worked_examples "
        "step labels de-em-dashed (' — ' to ': ') to satisfy the hard no-em-dash style law. "
        "Every guided box verified to recompute and land on stored solutions; completion "
        "boundaries validated (>=1 pre-worked box, >=2 live boxes).")
}
json.dump(changes, io.open("changes_maths-ocr_number-L03.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)

diagrams = {
    "key": "number-L03",
    "board": "maths-ocr",
    "figures_added": [
        {"tier": "opener", "index": 0, "kind": "svg",
         "what": "Number line from £3 to £4 with the £3.50 halfway tick and a marker at £3.84 past halfway; shows what the opener text claims (Tom's show-what-you-say rule) and makes the round-to-nearest idea concrete."}
    ],
    "opener_touched": True,
    "notes": ("Decimals & Rounding is a textual number unit: exam papers print no figure for "
        "'round 3.847 to 1 dp', estimation, or decimal arithmetic, so no problem-level figures "
        "were added (exam-realism test). The single figure is a theme-safe inline number-line "
        "SVG in the opener (currentColor strokes/text, soft-opacity marker, Inter labels, no "
        "external refs) supporting the halfway-mark hook. No question text, solutions, steps, "
        "hints, or misconceptions changed in the figure pass.")
}
json.dump(diagrams, io.open("changes_maths-ocr_number-L03_diagrams.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote changes + diagrams files")
