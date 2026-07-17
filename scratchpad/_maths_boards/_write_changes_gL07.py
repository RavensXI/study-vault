# -*- coding: utf-8 -*-
import json

changes = {
 "key":"graphs-L07",
 "board":"maths-ocr",
 "lesson_id":"5ea35085-7e2c-4216-9829-f0eda94acb67",
 "problems_fixed": [],
 "bank_correctness":"Fresh-solved all 20 stored problems (bronze 8, silver 7, gold 5) from their displays. Every stored solution was already mathematically correct; no wrong answers, degenerate cases, messy non-calculator decimals, or intra-tier duplicate answers found.",
 "added_structure":"Full guided-learning conversion. Reshaped 13 of 20 problems from bare multiple_choice into single_value numeric problems (bronze[0,1,4,7], all 7 silver, gold[0,2]) so each carries a guided_steps walk with a phase:'substitute' completion boundary (mirrors the approved OCR graphs-L03/L05 shape). Kept 7 genuine multiple_choice (direction/axis/equation-choice) that need no numeric walk. Added tier_guides (bronze/silver/gold), guided.opener, guided.teach walks (>=4 boxes each), per-problem hints, and *_description fields.",
 "misconceptions_rebuilt":"Every misconception given a derived expect by committing the specific error (e.g. B1 expect 5 = using x not y; S3 expect -2 = 3-5 left instead of right; G1 expect 0 = vertical shift ignored; G5 expects 0/2/3 for the three (x-axis)/(horizontal-forgotten)/(right-shift) errors). MC expects use the wrong option's index.",
 "figures_added": 4,
 "figures":[
   {"where":"guided.opener.display","kind":"svg","what":"gull 4 m above a lake with its dashed reflection 4 m below, marked ?, currentColor strokes/labels, translucent water fill (theme-safe)"},
   {"where":"gold[0]","kind":"chart","what":"y = x^2 parabola with vertex (0,0) highlighted, for the (x+1)^2-4 vertex question"},
   {"where":"gold[1]","kind":"chart","what":"y = sin x over 0-360 deg, for the reflect-in-x-axis equation question"},
   {"where":"silver[3]","kind":"chart","what":"y = x^2 parabola for the (x+2)^2+1 translation-vector question"}
 ],
 "style_fixes":"Removed em dashes from the two preserved worked_examples labels ('Step 1 — ...' -> 'Step 1: ...') to satisfy the no-em-dash rule; no other worked_examples content changed.",
 "opener_concept":"Two everyday reflections/translations: a resurveyed hillwalk where every height is 2 m higher (adding to every reading = slide the graph UP = f(x)+2, outside the bracket), then a gull 4 m above a lake whose reflection is 4 m below (flip every height = reflect in x-axis = -f(x)). Common sense first, then named as the method.",
 "preservation":"topic_links and related_videos byte-identical to pre-dump; worked_examples identical except the two em-dash label fixes; problem displays kept in LaTeX.",
 "issues_resolved": 0,
 "validator":"PASS",
 "notes":"Bank was clean on fresh-solve, so problems_fixed is empty (no answer corrections). All guided-step boxes, teach walks, opener boxes, misconception expects, chart points (y=x^2 and sin) and the SVG were independently recomputed and cross-checked against the numbers; validator PASS; PATCH round-trip matches."
}
json.dump(changes, open("changes_maths-ocr_graphs-L07.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)

diagchanges = {
 "key":"graphs-L07",
 "board":"maths-ocr",
 "figures_added":[
   {"tier":"opener","index":None,"kind":"svg","what":"gull-and-lake reflection figure in guided.opener.display; theme-safe (currentColor, translucent water)"},
   {"tier":"gold","index":0,"kind":"chart","what":"y = x^2 parabola, vertex highlighted, for (x+1)^2-4 vertex question"},
   {"tier":"gold","index":1,"kind":"chart","what":"y = sin x, 0-360 deg, for reflection-in-x-axis question"},
   {"tier":"silver","index":3,"kind":"chart","what":"y = x^2 parabola for (x+2)^2+1 translation-vector question"}
 ],
 "opener_touched": True,
 "notes":"Diagrams added in the same pass as the guided conversion. Charts sit only on problems where the exam would print the curve (a quadratic vertex, a sin reflection, a parabola translation); direction/axis multiple-choice problems are pure notation and get none. Every chart point recomputed against its equation; SVG uses currentColor and fill-opacity for light/dark safety."
}
json.dump(diagchanges, open("changes_maths-ocr_graphs-L07_diagrams.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote changes files")
