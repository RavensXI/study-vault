# -*- coding: utf-8 -*-
import json, io

changes = {
 "key": "graphs-L07",
 "board": "maths-aqa",
 "lesson_id": "063c867c-7ba6-4879-9747-c3546382aaf2",
 "title": "Graph Transformations",
 "problems_fixed": [
  {"tier":"gold","index":0,
   "what":"Within-tier duplicate answer: three gold single_value problems all answered 2 (gold[0] horizontal component, gold[1] x-coord, gold[4] b). Renumbered gold[0] from (x-2)^2+3 to (x-4)^2+3 so the horizontal component is 4, breaking the collision. Recomputed its two misconception expects (swap-to-vertical 3, sign-kept -4).",
   "old":"y=(x-2)^2+3, horizontal component = 2",
   "new":"y=(x-4)^2+3, horizontal component = 4"},
  {"tier":"gold","index":4,
   "what":"Within-tier duplicate answer (same collision on 2): changed the crossing point from (4,0) to (6,0) so f(2x) gives b = 6/2 = 3, distinct from gold[1]=2. Recomputed misconception expects (x2 -> 12, x-unchanged -> 6).",
   "old":"f(x) through (0,3),(4,0); find b for f(2x)  (b=2)",
   "new":"f(x) through (0,3),(6,0); find b for f(2x)  (b=3)"},
  {"tier":"gold","index":3,
   "what":"Mis-posed display: asked 'What is the maximum of y=-f(x)?' while the correct option is a MINIMUM at (1,-4), a self-contradiction. Reworded to 'Describe the corresponding turning point on y=-f(x).' Options and correct index unchanged.",
   "old":"What is the maximum of y = -f(x)?",
   "new":"Describe the corresponding turning point on y = -f(x)."},
 ],
 "issues_resolved": 3,
 "solutions_audit": "Fresh-solved all 20 bank problems from display text. Every stored solution was mathematically correct (shift directions, inside-opposite rule, vertical/horizontal stretch factors 3 and 1/2, point images, and the combined-transformation coordinates). Defects were structural: a triple within-tier duplicate answer (2) across the gold single_value problems, and one self-contradictory multiple_choice stem. No wrong numeric answers and no non-calculator messiness.",
 "opener_concept": "A drone's height over time (inline-SVG hill curve peaking at height 5). To fly the whole path 3 m higher you add 3 to every height: the peak 5 becomes 8, a point at height 1 becomes 4. That IS y=f(x)+3, a vertical translation up. The reveal then names the inside/outside, stretch and reflection moves the lesson covers.",
 "guided_added": {
  "tier_descriptions": "Added bronze/silver/gold_description one-liners.",
  "tier_guides": "bronze (shifts and reflections), silver (stretches and scale factors), gold (combined transformations and vectors); each with a 4-step worked example landing on an answer step, all within the 115-word budget.",
  "opener": "SVG height curve + 2 read-off boxes (8, 4) + reveal naming f(x)+a.",
  "teach_walks": {"bronze":"image of (2,5) under f(x-3)+1 (inside-opposite plus outside shift)","silver":"image of (4,6) under 2f(x) and f(2x), deriving factors 2 and 1/2","gold":"vertex of y=(x+1)^2-4 by combining left 1 and down 4, with a Chart.js figure"},
  "guided_steps": "Added to all 7 non-multiple-choice bank problems (bronze[0], silver[2], silver[3], gold[0], gold[1], gold[2], gold[4]); each has a phase:substitute completion boundary (>=1 step before, >=2 live boxes after) and a final check step landing exactly on the stored solution. The 13 multiple_choice problems keep no walk (permitted).",
  "hints": "Added one plain-text hint to every problem (the live rows had none).",
  "misconceptions": "Every misconception given the pattern/message/expect/note shape with a derived, error-committing expect where determinate (swap horizontal/vertical component -> 3; keep inside sign -> -4; wrong-direction inside shift -> 8; sign slip on outside shift -> 1; ignore outside shift -> -1; multiply instead of divide under f(2x) -> 12; leave x unchanged -> 6). Recognition/direction and all multiple_choice items use expect:null (no single determinate wrong number)."
 },
 "method_card_trimmed": "Cut from 5 steps to 4 and slimmed the content within the 140-word budget; keeps the (x-3)^2+2 -> vector (3,2) example.",
 "preserved": ["topic_links (prerequisites graphs/3 Quadratic Graphs, graphs/6 Trigonometric Graphs)","related_videos ([])","worked_examples (y=sin x -> y=2sin x, Silver) preserved byte-for-byte"],
 "notes": "All solutions verified on fresh-solve; independent box/expect/chart re-computation script passed; validator PASS; live PATCH 204 and normalized roundtrip confirmed identical (Postgres stored 7.0 as 7 only). Diagrams added in the same pass (see diagrams changes file)."
}
json.dump(changes, io.open("changes_maths-aqa_graphs-L07.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)

diagrams = {
 "key":"graphs-L07",
 "board":"maths-aqa",
 "lesson_id":"063c867c-7ba6-4879-9747-c3546382aaf2",
 "figures_added":[
  {"tier":"opener","index":0,"kind":"svg","what":"Drone height-vs-time curve (peak 5 m) plotting (0,1),(1,3),(2,5),(3,4),(4,2). Theme-safe: axes and labels currentColor, curve soft amber #f59e0b, viewBox+role=img+aria-label. Supports the two opener boxes (new peak 8, point 4) that introduce f(x)+3 as a vertical shift."},
  {"tier":"silver","index":0,"kind":"chart","what":"Chart.js y=x^2 (blue) and y=x^2+7 (orange), x from -3 to 3. The exam figure for 'describe y=x^2 -> y=x^2+7': every plotted point on the orange curve is 7 above the blue (verified), showing the up-7 translation."},
  {"tier":"silver","index":1,"kind":"chart","what":"Chart.js y=x^2 (blue) and y=(x+5)^2 (orange), x from -7 to 2. Shows the vertex moving from x=0 to x=-5, i.e. left 5; every plotted point satisfies its equation (verified)."},
  {"tier":"silver","index":6,"kind":"chart","what":"Chart.js y=sin x (blue) and y=-sin x (orange) over 0 to 360 degrees. Every orange y is the negation of the blue y (verified), showing the reflection in the x-axis."},
  {"tier":"gold","index":3,"kind":"svg","what":"Coordinate grid marking the maximum (1,4) and its image (1,-4) after reflection in the x-axis, with a dashed connector through the axis. The '?' marks the turning point the student must classify. Theme-safe (currentColor axes/labels; #60a5fa max, #f59e0b image)."},
  {"tier":"teach.gold","index":0,"kind":"chart","what":"Chart.js y=x^2 (blue) and y=(x+1)^2-4 (orange) for the gold teach walk, x from -5 to 3. Confirms the vertex moving to (-1,-4); every plotted point satisfies its equation (verified)."}
 ],
 "opener_touched": True,
 "coverage_note": "Figures were added exactly where an exam paper prints one: the two concrete parabola translations, the sine reflection, the reflected turning point, and the opener/teach scenes. The bronze/silver direction-and-axis recall items are stated on a generic y=f(x) with no specific curve, so the exam prints only the algebra; the point-image multiple_choice items give the coordinates in words and need no grid. No missed printable figures.",
 "notes":"validator PASS; all figure numbers generated programmatically from each problem's own values and re-read against the text; single combined pass so the live row carries walks and figures together."
}
json.dump(diagrams, io.open("changes_maths-aqa_graphs-L07_diagrams.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("changes files written")
