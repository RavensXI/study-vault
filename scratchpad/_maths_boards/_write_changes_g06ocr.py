import json, io
KEY="maths-ocr_graphs-L06"
changes={
 "key":KEY,
 "problems_fixed":[
  {"tier":"bronze","index":2,"what":"was sin 90° = 1 (duplicate value 1 within tier); reposed as WHERE sin x reaches its maximum","old":"sin 90° = 1","new":"sin x maximum at x = 90°"},
  {"tier":"bronze","index":6,"what":"was sin 270° = −1 (duplicate value −1 within tier); reposed as WHERE sin x reaches its minimum","old":"sin 270° = −1","new":"sin x minimum at x = 270°"},
  {"tier":"bronze","index":7,"what":"was max value of sin x = 1 (duplicate value 1 within tier); reposed as count of x-axis crossings of sin x on 0°-360°","old":"max value of sin x = 1","new":"sin x crossings = 3"},
  {"tier":"silver","index":5,"what":"was sin 180° = 0 (duplicate value 0 within tier); reposed as second (larger) solution of cos x = −0.5","old":"sin 180° = 0","new":"cos x = −0.5 larger = 240°"},
  {"tier":"silver","index":6,"what":"was cos 90° = 0 (duplicate value 0 within tier); reposed as second (larger) solution of cos x = 0.5","old":"cos 90° = 0","new":"cos x = 0.5 larger = 300°"},
  {"tier":"worked_examples","index":1,"what":"em dashes in step labels (validator-blocking) changed to colons","old":"Step 1 — First solution / Step 2 — Second solution","new":"Step 1: First solution / Step 2: Second solution"}
 ],
 "issues_resolved":6,
 "opener_concept":"Big wheel (Ferris wheel), centre 20 m up, radius 15 m, one turn 30 s. Student finds lowest (5 m), highest (35 m) and repeat time (30 s) by common sense; reveal names the height-vs-time trace as y = sin x, with 20 m midline, 15 m amplitude, 30 s period.",
 "notes":"Fresh-solved all 20 problems: every stored answer was mathematically correct, but three tiers carried duplicate solution values within a tier (bronze 1x3 and -1x2; silver 0x3), the 'duplicate answers within tiers' disease flagged in the deltas. Repaired 5 problems into distinct-value equivalents that keep each tier's skill, giving distinct banks (bronze {0,1,-1,360,180,90,270,3}, silver {30,60,150,0,120,240,300}, gold {210,5,-3,4,45} unchanged). Added hints, tier_descriptions, tier_guides, guided.opener and guided.teach walks, and full guided_steps with substitute boundaries and derived misconception expects to every problem. Slimmed method_card from 5 to 4 steps. Gold bank left as-is (already distinct and correct)."
}
json.dump(changes,io.open(f"changes_{KEY}.json","w",encoding="utf-8"),ensure_ascii=False,indent=2)

diagrams={
 "key":KEY,
 "figures_added":[
  {"tier":"bronze","index":7,"kind":"chart","what":"y = sin x over 0°-360° (Chart.js line) so the student can count the three x-axis crossings at 0°, 180°, 360°."},
  {"tier":"silver","index":5,"kind":"chart","what":"y = cos x over 0°-360° with dashed line y = −0.5 marking the two solutions 120° and 240°."},
  {"tier":"gold","index":0,"kind":"chart","what":"y = sin x over 0°-360° with dashed line y = −0.5 showing solutions in Q3/Q4 (210°, 330°)."},
  {"tier":"gold","index":3,"kind":"chart","what":"y = sin x over 0°-720° with dashed line y = 0.3, making the 4 crossings over two periods visible."},
  {"tier":"opener","index":0,"kind":"svg","what":"Inline theme-safe SVG of the big wheel (currentColor strokes/labels, soft fills): ground line, radius, marked car, centre 20 m and 15 m radius labels."}
 ],
 "opener_touched":True,
 "notes":"Charts generated programmatically from math.sin/math.cos (points every 15°, verified against the curve). All figures match the numbers: horizontal reference lines equal the equation constants; sine/cosine points recomputed in _verify_g06ocr.py. SVG is self-contained, <2KB, role=img + aria-label, currentColor + soft fill-opacity for light/dark themes, 'Diagram not drawn accurately' caption. Purely computational max/min problems (gold 3sinx+2, 2cosx-1) left figureless by the exam-realism test."
}
json.dump(diagrams,io.open(f"changes_{KEY}_diagrams.json","w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("wrote changes_%s.json and changes_%s_diagrams.json"%(KEY,KEY))
