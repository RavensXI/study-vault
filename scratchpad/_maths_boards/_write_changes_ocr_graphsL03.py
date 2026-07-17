# -*- coding: utf-8 -*-
import json, io

changes = {
 "key": "graphs-L03",
 "board": "maths-ocr",
 "problems_fixed": [
  {"tier": "bronze", "index": 5, "what": "de-duplicated intra-tier answer (bronze[0] also = 7); changed constant 7 to 6 so y-intercept = 6",
   "old": "y = x^2 - 3x + 7 (y-intercept 7)", "new": "y = x^2 - 3x + 6 (y-intercept 6)"},
  {"tier": "gold", "index": 2, "what": "de-duplicated intra-tier answer (gold[0] also = 2); changed root 5 to 9 so turning-point x = 4",
   "old": "roots x = -1 and x = 5, TP x = 2", "new": "roots x = -1 and x = 9, TP x = 4"},
  {"tier": "worked_examples", "index": -1, "what": "replaced em dashes in step labels with colons (style-law compliance)",
   "old": "'Step 1 — Factorise' etc.", "new": "'Step 1: Factorise' etc."},
  {"tier": "method_card", "index": -1, "what": "trimmed steps 5 -> 4 (validator budget) and reworded arch shape without em dash",
   "old": "5 steps", "new": "4 steps"}
 ],
 "issues_resolved": 4,
 "opener_concept": "Garden sprinkler water arch (inline SVG parabola): read the peak height (3 m, turning point) and landing distance (8 m, root) by common sense, then name them as turning point and roots.",
 "notes": "All 20 stored solutions fresh-solved from display: every one correct (no wrong answers found). Added guided-learning stack: opener (SVG), 3 teach walks (bronze reads features of y=x^2-4; silver roots+turning point of x^2-6x+8; gold a!=1 via 2x^2-12x+10), guided_steps on all 22 bank problems (every box value computed in Python, verified to land on stored solutions), tier_guides, tier descriptions, hints, and honest-diagnosis misconceptions (19 derivable expects, all distinct from the correct answer). No em dashes anywhere student-facing. related_videos and topic_links preserved byte-for-byte."
}
json.dump(changes, io.open("changes_maths-ocr_graphs-L03.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)

diagrams = {
 "key": "graphs-L03",
 "board": "maths-ocr",
 "figures_added": [
  {"tier": "bronze", "index": 2, "kind": "svg", "what": "opener figure is separate; this chart shows y = x^2 with the minimum vertex at the origin"},
  {"tier": "bronze", "index": 2, "kind": "chart", "what": "y = x^2 parabola (U-shape), vertex (0,0) marked as the minimum point"},
  {"tier": "bronze", "index": 6, "kind": "chart", "what": "y = -x^2 + 4 downward parabola so the student sees it has a maximum"},
  {"tier": "silver", "index": 5, "kind": "chart", "what": "y = -x^2 + 2x + 3 downward parabola, peak at (1,4) shows the maximum value"},
  {"tier": "silver", "index": 6, "kind": "chart", "what": "y = x^2 + 4 parabola sitting entirely above the x-axis: visibly 0 roots"},
  {"tier": "gold", "index": 4, "kind": "chart", "what": "y = -3x^2 + 12x - 9 steep downward parabola, peak at (2,3) shows the maximum value"}
 ],
 "opener_touched": True,
 "notes": "Opener uses an inline SVG parabola (sprinkler water arch) generated programmatically from f(x) = -3/16 x(x-8): peak (4,3), roots 0 and 8; theme-safe (currentColor text/axes, #3b82f6 curve). 5 Chart.js quadratic figures added on the problems where an exam would print the graph: direction/max-min, how-many-roots, and max-value questions. Every plotted point recomputed against its equation (all match). Textual problems (substitution, y-intercept, sum/product of roots, factorising roots) left without figures per the exam-realism test."
}
json.dump(diagrams, io.open("changes_maths-ocr_graphs-L03_diagrams.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("changes files written")
