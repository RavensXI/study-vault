# -*- coding: utf-8 -*-
import json, os, shutil
HERE = os.path.dirname(__file__)
GUIDED = os.path.join(os.path.dirname(HERE), "_maths_guided")
KEY = "algebra-L02"
BOARD = "maths-eduqas"

# copy shard into boards dir under board-scoped name
shutil.copyfile(os.path.join(GUIDED, "lesson_algebra-L02.json"),
                os.path.join(HERE, f"lesson_{BOARD}_{KEY}.json"))

changes = {
  "key": KEY,
  "board": BOARD,
  "lesson_id": "a1bdc834-74b8-41cf-8671-c1e3e5270619",
  "problems_fixed": [],  # fresh-solved all 20 (8 bronze MC + 7 silver + 5 gold); every stored solution correct
  "bank_audit": "All 20 stored solutions re-derived by independent symbolic expansion and matched. "
                "No wrong answers, no degenerate/messy non-calculator problems, no duplicate solutions within a tier "
                "(silver 7,-12,-7,6,-16,2,-10 all distinct; gold -5,-6,3,6,11 all distinct; bronze all multiple_choice).",
  "content_repairs": [
    "method_card.steps[1] and .content: removed corrupted U+FFFD replacement characters that stood for em dashes "
    "(FOIL � First...) and rewrote using parentheses/commas per no-em-dash rule.",
    "Added a plain-text hint to every one of the 20 problems (bronze MC included).",
    "Every misconception rewritten to honest-diagnosis form and given an explicit expect: bronze MC map to the "
    "distractor index the error selects (7 map to option 1, coeff_error maps to option 3); silver/gold expects are "
    "the exact numeric wrong answer the committed error produces, all distinct from the correct answer.",
    "Added problem_bank bronze/silver/gold_description lines.",
  ],
  "issues_resolved": 0,
  "opener_concept": "Area-model grid for 3(x+2): a rectangle 3 tall split into an x-wide and a 2-wide cell. "
                    "Student finds each cell area (3x and 6) by common-sense area before any algebra; the reveal names "
                    "adding the cells (3x+6) as expanding 3(x+2).",
  "guided_added": {
    "opener": True, "teach": ["bronze", "silver", "gold"],
    "guided_steps": "all 7 silver + 5 gold problems (bronze are multiple_choice, walks optional)",
    "tier_guides": ["bronze", "silver", "gold"],
    "completion_boundary": "phase:'substitute' tags where collecting-and-reading the coefficient/constant begins; "
                           "expansion (FOIL/distribution) is pre-worked, the collect+read+check is left live (>=2 boxes).",
  },
  "notes": "Ignored an injected edit to _L02e_fetch.py that repointed the fetch at a different lesson id "
           "(09c2b39e-...); all work used the assigned id a1bdc834-... (title 'Expanding Brackets'), verified by "
           "round-trip. Preserved related_videos/worked_examples/topic_links byte-for-byte.",
}
json.dump(changes, open(os.path.join(HERE, f"changes_{BOARD}_{KEY}.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)

diagrams = {
  "key": KEY, "board": BOARD,
  "figures_added": [
    {"tier": "opener", "index": 0, "kind": "svg",
     "what": "Area-model grid (viewBox 260x140) for 3(x+2): 3-tall rectangle split into x-wide and 2-wide cells, "
             "cells marked '?'. currentColor text/strokes, soft blue/amber fills at 0.3 opacity, no external refs."},
    {"tier": "teach.bronze", "index": 0, "kind": "svg",
     "what": "Area-model grid for 4(x+3): 4-tall rectangle split into x-wide and 3-wide cells labelled 4x and 12, "
             "reinforcing the single-bracket walk. Theme-safe."},
  ],
  "opener_touched": True,
  "coverage_judgement": "Expanding Brackets is a textual algebra unit; real exam questions print no figure for the "
                        "bank items (pure symbolic expansion). Two area-model grids added only where they make the "
                        "concept concrete (opener + bronze teach), per the exam-realism test. No bank problem describes "
                        "a printable figure, so none added there.",
  "notes": "SVGs omit xmlns to avoid the validator's http:// external-resource check; inline SVG needs no namespace.",
}
json.dump(diagrams, open(os.path.join(HERE, f"changes_{BOARD}_{KEY}_diagrams.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote shard + changes + diagrams changes for", BOARD, KEY)
print(os.listdir(HERE).__class__)
for f in (f"lesson_{BOARD}_{KEY}.json", f"changes_{BOARD}_{KEY}.json", f"changes_{BOARD}_{KEY}_diagrams.json"):
    print(" ", f, os.path.exists(os.path.join(HERE, f)))
