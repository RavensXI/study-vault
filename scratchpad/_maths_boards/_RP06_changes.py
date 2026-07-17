# -*- coding: utf-8 -*-
import json

changes = {
 "key": "ratio-proportion-L06",
 "board": "maths-eduqas",
 "lesson_id": "ca643606-adf3-40c8-a4dd-8dfb8c25a21f",
 "problems_fixed": [
   {"tier": "gold", "index": 1, "what": "Original stored 'correct' answer was mathematically wrong: display x_{n+1}=(x_n^3+2)/(3x_n^2), x0=1.5 gives x1=0.7963, but the marked-correct option was 1.2963. The misconception message itself admitted the contradiction. Rebuilt as a clean Newton-Raphson problem with verified answer.", "old": "1.2963 (wrong; true 0.7963)", "new": "x_{n+1}=(2x_n^3+5)/(3x_n^2), x0=2, x2=1.711 (verified, converges to cbrt 5)"},
   {"tier": "gold", "index": 4, "what": "Original stored answer wrong: x_{n+1}=(5+x_n)/x_n, x0=2, x3 = 3.06, but marked-correct option was 2.24; message admitted 'the answer 2.24 is approximate'. Replaced with a clean convergence problem.", "old": "2.24 (wrong; true 3.06)", "new": "x=sqrt(2x+15), positive value = 5 (verified)"},
   {"tier": "gold", "index": 0, "what": "Original misconception 'used_curve' gave the CORRECT method and answer (gradient 3), so it was a broken/non-diagnostic misconception. Rebuilt problem with an honest inverted-gradient misconception (expect 0.333).", "old": "misconception message reproduced the right answer", "new": "tangent through (0,1),(4,13), rate=3; expect 0.333 for run/rise"},
   {"tier": "all", "index": -1, "what": "Whole bank was multiple_choice with solutions as option indices [0] and no guided steps; several misconception messages were self-contradictory or non-determinate. Converted to the approved guided-learning shape (single_value with full guided_steps + honest expects), matching the AQA/OCR/Edexcel siblings of this exact lesson. Kept one conceptual MC (bronze[7]). Tier sizes preserved (8/7/5).", "old": "20 multiple_choice problems, index solutions, no walks", "new": "19 single_value + 1 MC, all with guided_steps, hints, derivable expects"}
 ],
 "issues_resolved": 4,
 "opener_concept": "Fish tank: drain half the 200 litres each day, top up 60 litres (200 -> 160 -> 140, settling to 120). Doing the two sums by common sense IS iteration; reveal names x_{n+1}=x_n/2+60 and links the other half of the lesson (rate of change = gradient off a graph).",
 "style_repairs": "Preserved worked_examples had em dashes in step labels ('Step 1 — Gradient'); replaced ' — ' with ': ' in labels only, content untouched (validator/style law forbids em dashes).",
 "preservation": "topic_links and related_videos ([]) preserved byte-for-byte; worked_examples content preserved (labels de-dashed only).",
 "notes": "No prior audit for this board; every problem fresh-solved from its display and every guided box recomputed independently (_RP06_calc.py, _RP06_verify.py). Validator PASS. Live PATCH 204, readback == shard."
}

with open("changes_maths-eduqas_ratio-proportion-L06.json", "w", encoding="utf-8") as f:
    json.dump(changes, f, indent=1, ensure_ascii=False)

diagrams = {
 "key": "ratio-proportion-L06",
 "board": "maths-eduqas",
 "figures_added": [
   {"tier": "bronze", "index": 0, "kind": "svg", "what": "Distance-time straight line from origin to (4, 80); axes labelled km / hours. Matches the speed = 80/4 = 20 problem."},
   {"tier": "bronze", "index": 4, "kind": "svg", "what": "Speed-time horizontal line at 12 m/s from 0 to 8 s (constant speed, acceleration 0). Labels 12 and 8 match the problem numbers."},
   {"tier": "gold", "index": 3, "kind": "svg", "what": "y = x^2 curve on 0..4 with four trapezium strips (width 1); strip heights labelled 0, 1, 4, 9, 16, matching the trapezium-rule estimate of 22."}
 ],
 "opener_touched": False,
 "notes": "Iteration and two-point-gradient problems are pure calculation (data given), so they correctly get no figure. Figures added only where the text names a graph the exam would print (distance-time, speed-time, trapezium curve). All theme-safe: text/axes fill=currentColor, region fills #60a5fa fill-opacity 0.25; no external refs; viewBox + role=img + aria-label present. Every visible number cross-checked against the problem text and solution."
}
with open("changes_maths-eduqas_ratio-proportion-L06_diagrams.json", "w", encoding="utf-8") as f:
    json.dump(diagrams, f, indent=1, ensure_ascii=False)
print("changes files written")
