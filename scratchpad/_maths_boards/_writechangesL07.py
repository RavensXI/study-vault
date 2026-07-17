# -*- coding: utf-8 -*-
import json
changes = {
    "key": "number-L07",
    "board": "maths-ocr",
    "problems_fixed": [],
    "issues_resolved": 0,
    "opener_concept": ("A square tile of area 9 tiles (shown as a 3x3 grid): count the tiles "
                       "along one edge to get 3, which IS taking a square root. The reveal names it "
                       "(sqrt9=3, sqrt25=5) and extends to simplifying a surd by pulling the biggest "
                       "square factor out of a non-square area (sqrt50 = sqrt25 x sqrt2 = 5 root 2)."),
    "figures_added": [
        {"tier": "opener", "index": 0, "kind": "svg",
         "what": "3x3 unit-tile grid, area 9, theme-safe (currentColor strokes/text, soft blue fill), "
                 "makes the square-root hook concrete (student counts the side)."}
    ],
    "opener_touched": True,
    "notes": ("Full guided + diagrams conversion of maths-ocr number-L07 (Indices, Surds & Bounds) in one pass. "
              "BANK CORRECTNESS: fresh-solved all 20 problems (8 bronze / 7 silver / 5 gold) from their displays; "
              "every stored solution and every MC option index was already correct, no within-tier duplicate "
              "solutions, no degenerate/non-calculator-messy problems, so ZERO correctness repairs were needed. "
              "ADDED: bronze/silver/gold tier descriptions; per-problem plain-text hints on all 20; full guided_steps "
              "on all 20 problems (MC included) with numeric-only boxes, >=3 boxes each, a phase:'substitute' "
              "completion boundary leaving >=2 live boxes, and a closing check box; guided.opener (2 boxes + reveal, "
              "with SVG); guided.teach.{bronze:sqrt32, silver:10/root5, gold:1/(4+root3)} each >=4 boxes; tier_guides "
              "for all three tiers within the 115-word budget with a worked example each. "
              "MISCONCEPTIONS: rewrote every message as an honest diagnosis and derived a determinate numeric expect "
              "for every single_value error by committing it (verified: bronze[4]=12.5/11, bronze[5]=3.15/3.7, "
              "bronze[7]=47.5/44.5, silver[2]=11/9, silver[3]=9.3/9.2, silver[5]=5/4, gold[2]=3/2.95, gold[3]=2/9); "
              "MC misconceptions keep expect=null (no single typed numeric answer; the distractors carry the error). "
              "method_card slimmed to 4 steps / <140 words. FIGURES: surds and bounds are textual/numeric and exams "
              "print no figure for them, so no per-problem figures were added (exam-realism test); the only figure is "
              "the opener tile-grid SVG. PRESERVED byte-for-byte: related_videos ([]), topic_links, all displays, all "
              "solutions, all MC options; worked_examples preserved except pre-existing em-dash step labels "
              "(' — ' -> ': ') which the validator's style rule forbids. Validator PASS; live PATCH round-trip equal."),
}
json.dump(changes, open("changes_maths-ocr_number-L07.json", "w", encoding="utf-8"),
          indent=2, ensure_ascii=False)
print("written changes_maths-ocr_number-L07.json")
