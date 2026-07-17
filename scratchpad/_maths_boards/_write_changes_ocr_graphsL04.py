# -*- coding: utf-8 -*-
import json, io

changes = {
 "key": "graphs-L04",
 "board": "maths-ocr",
 "lesson_id": "fb13c12c-f5c1-4832-871b-40440d729361",
 "problems_fixed": [
  {"tier": "bronze", "index": 5,
   "what": "Mis-posed problem: 'a flat line means the object is ___. Enter 1 for stationary, 0 for moving' encoded a concept as an arbitrary number and its answer (1) duplicated bronze[1]'s stop-duration answer of 1. Replaced with a genuine conversion-graph question (5 miles approx 8 km, convert 15 miles) giving a clean distinct integer.",
   "old": {"display": "On a distance-time graph, a flat line means the object is _____. Enter 1 for stationary, 0 for moving.", "solution": 1},
   "new": {"display": "A conversion graph shows 5 miles approx 8 km. Convert 15 miles to kilometres.", "solution": 24}},
  {"tier": "silver", "index": 2,
   "what": "Duplicate solution within silver: 'decelerates from 20 m/s to 0 in 4 s' gave 5 m/s2, identical to silver[0]'s acceleration answer of 5. Changed to 24 m/s to 0 in 3 s so the deceleration is a distinct clean 8 m/s2 (and the upside-down error 3/24=0.125 is clean).",
   "old": {"display": "A car decelerates from 20 m/s to 0 in 4 seconds.", "solution": 5},
   "new": {"display": "A car decelerates from 24 m/s to 0 in 3 seconds.", "solution": 8}},
  {"tier": "gold", "index": 4,
   "what": "Duplicate solution within gold: 'accelerates from rest at 3 m/s2 for 10 s' gave 30 m/s, identical to gold[2]'s final-section speed of 30. Changed the acceleration to 4 m/s2 so the final speed is a distinct 40 m/s.",
   "old": {"display": "A car accelerates from rest at 3 m/s2 for 10 seconds.", "solution": 30},
   "new": {"display": "A car accelerates from rest at 4 m/s2 for 10 seconds.", "solution": 40}}
 ],
 "issues_resolved": 3,
 "opener_concept": "Read a real journey. A distance-time graph (inline SVG) of Maya driving to her aunt's house and back: the student reads the aunt's distance (30 km), the flat rest section (1 hour) and the finish time (3 hours) by pure common sense, then the reveal names height = distance, flat = stopped, slope = speed, area (on speed-time) = distance.",
 "notes": "Fresh-solved all 20 stored answers from their displays and charts: every one correct on the maths. The only defects were three within-tier duplicate answers (bronze 1/1, silver 5/5, gold 30/30) plus one mis-posed numeric-encoded concept problem (bronze[5]); all fixed above with minimal clean-integer edits. Added the full guided stack: opener, three teach walks (bronze steady-speed calc, silver speed-time SVG triangle+rectangle, gold trapezium SVG), tier_guides with examples, tier descriptions, per-problem plain-text hints, and guided_steps on all 20 single_value problems (completion boundary tagged phase:'substitute' after the main method move, every walk ends on the stored solution with a check step, >=2 live boxes after the boundary). Every misconception rewritten as honest diagnosis with a derived numeric expect (each recomputed by committing the named error; all != the correct answer). method_card trimmed to 4 steps. Preserved bronze[5] em-dash-free; fixed pre-existing em dashes in worked_examples step labels (em dash -> colon, required by style law). related_videos, topic_links and worked_examples questions/content preserved. Validator PASS; independent recompute of every box, boundary, expect, chart and SVG label ALL CLEAR."
}
io.open("changes_maths-ocr_graphs-L04.json", "w", encoding="utf-8").write(
    json.dumps(changes, ensure_ascii=False, indent=1))

diagrams = {
 "key": "graphs-L04",
 "board": "maths-ocr",
 "figures_added": [
  {"tier": "gold", "index": 0, "kind": "chart",
   "what": "Speed-time graph (Chart.js line): points (0,0),(4,10),(10,10),(15,0). Matches the described 0->10 m/s in 4 s, constant 10 m/s for 6 s, 10->0 in 5 s; area = 105 m."},
  {"tier": "gold", "index": 2, "kind": "chart",
   "what": "Distance-time graph (Chart.js line): points (0,0),(2,40),(3,40),(5,100). Matches the stated coordinates; final-section speed (100-40)/(5-3)=30 km/h."},
  {"tier": "gold", "index": 3, "kind": "svg",
   "what": "Inline SVG right triangle for the reverse-area problem: base labelled 8 s, height labelled v (the unknown), soft-fill area labelled 80 m. Theme-safe (currentColor text, fill-opacity region). Half*8*20 = 80 confirms."},
  {"tier": "opener", "index": 0, "kind": "svg",
   "what": "Distance-time graph (inline SVG) of Maya's out-and-back drive: (0,0),(1,30),(2,30),(3,0). Height=distance, flat=rest, currentColor labels."},
  {"tier": "teach-silver", "index": 0, "kind": "svg",
   "what": "Speed-time graph (inline SVG): rises 0->16 m/s by 4 s then flat to 12 s. Used to walk triangle+rectangle area = 160 m."},
  {"tier": "teach-gold", "index": 0, "kind": "svg",
   "what": "Speed-time trapezium (inline SVG): 0->20 in 4 s, hold to 14 s, down to 0 by 20 s. Walk gives 40+200+60 = 300 m."}
 ],
 "opener_touched": True,
 "notes": "Preserved the two existing bronze distance-time charts (B0/B1, data [0,30,60,60,90]) and the silver speed-time chart (S1, [0,10,20,20,20,0]); cross-checked their readings against the questions. New figures generated programmatically from each problem's own numbers and re-read against the text. All inline SVG uses viewBox + role=img + aria-label, currentColor strokes/text, soft fill-opacity regions, Inter labels, no external refs. Validator PASS."
}
io.open("changes_maths-ocr_graphs-L04_diagrams.json", "w", encoding="utf-8").write(
    json.dumps(diagrams, ensure_ascii=False, indent=1))
print("changes files written")
