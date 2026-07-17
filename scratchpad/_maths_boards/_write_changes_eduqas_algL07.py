# -*- coding: utf-8 -*-
import json, io

changes = {
 "key": "algebra-L07",
 "board": "maths-eduqas",
 "lesson_id": "5ead70d6-f265-4790-86b5-573b9b16606a",
 "problems_fixed": [
  {"tier": "bronze", "index": 4, "what": "duplicate solution 4 within tier (clashed with bronze[3]); reposed as a distinct difference-of-squares",
   "old": "Solve x^2 - 16 = 0. Find the positive solution. -> [4]",
   "new": "Solve x^2 - 25 = 0. Find the positive solution. -> [5]"},
  {"tier": "bronze", "index": 6, "what": "duplicate solution 2 within tier (clashed with bronze[5]); changed constant so smaller root is distinct",
   "old": "Solve x^2 - 6x + 8 = 0. Find the smaller solution. -> [2]",
   "new": "Solve x^2 - 6x + 5 = 0. Find the smaller solution. -> [1]"},
  {"tier": "silver", "index": 3, "what": "duplicate solution 3 within tier (clashed with silver[1]); new rearrange problem with distinct larger root",
   "old": "Solve x^2 = 5x - 6. Find the larger solution. -> [3]",
   "new": "Solve x^2 = 7x - 12. Find the larger solution. -> [4]"},
  {"tier": "silver", "index": 5, "what": "duplicate solution 2 within tier (clashed with silver[4]); new rearrange problem, asks larger root",
   "old": "Solve x^2 = 7x - 10. Find the smaller solution. -> [2]",
   "new": "Solve x^2 = 8x - 7. Find the larger solution. -> [7]"},
  {"tier": "gold", "index": 2, "what": "duplicate solution [1] within tier (clashed with gold[0] numerator); switched to the negative root's denominator so the stored answer is distinct",
   "old": "Solve 6x^2 + x - 2 = 0. Find the positive solution as a fraction (numerator). -> [1]",
   "new": "Solve 6x^2 + x - 2 = 0. Find the negative solution as a fraction (give the denominator). -> [3]"},
 ],
 "issues_resolved": 5,
 "opener_concept": "Two-part common-sense hook: (1) find two numbers that multiply to 10 and add to 7 (that IS factorising), then (2) 6 x (something) = 0 forces the something to be 0 (the zero-product rule). Together they are the whole method.",
 "notes": "No prior audit for Eduqas: fresh-solved all 20 problems from their displays. Maths was correct on every stored answer; the only disease found was the validator-fatal 'duplicate solution tuple within tier' (bronze 4&4, 2&2; silver 3&3, 2&2; gold [1]&[1]) - fixed with 5 minimal clean-integer reposals. Added the full guided stack: opener, per-tier teach walks (>=4 boxes), guided_steps on all 20 bank problems (completion boundary at first bracket-solve; set-up pre-worked, solve-through + pick-the-asked-value + check live), per-problem hints, tier_descriptions, and tier_guides. Misconceptions had NO expect keys (player at practice.html:4689 needs them for honest matching); rederived a determinate expect for every one by committing the error (sign-flip, larger-magnitude-of-negatives, picked-wrong-root, product-vs-sum, numerator-vs-denominator, no-rearrange, two-always). Preserved method_card, topic_links, worked_examples (3), related_videos ([]). All minus signs are unicode U+2212, no em dashes. Independent fresh-solve verifier + _validate_guided.py both clean; PATCH 204, round-trip confirmed.",
}
json.dump(changes, io.open("changes_maths-eduqas_algebra-L07.json", "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)

diag = {
 "key": "algebra-L07",
 "board": "maths-eduqas",
 "figures_added": [],
 "opener_touched": False,
 "notes": "Exam-realism test applied: 'Solving Quadratics by Factorising' is a purely algebraic topic. GCSE papers print no figure for 'solve x^2 - 5x + 6 = 0' style items (no shape, graph, tree, Venn, grid, or chart in any of the 20 bank problems, the opener, or the teach walks). Per SPEC_DIAGRAMS 'do NOT add decoration to problems that are genuinely textual', zero figures is the correct call. The opener is purely numeric/imaginative (two numbers multiplying) and claims no figure, so 'show what you say' is satisfied without SVG.",
}
json.dump(diag, io.open("changes_maths-eduqas_algebra-L07_diagrams.json", "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print("changes files written")
