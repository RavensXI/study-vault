import json
changes={
 "key":"geometry-L05",
 "board":"maths-ocr",
 "problems_fixed":[
   {"tier":"silver","index":6,"what":"Duplicate answer within tier (36.9 also at silver[3]). Re-posed opposite=9,hypotenuse=15 to opposite=7,hypotenuse=25 (sin), giving a distinct clean 16.3.","old":"[36.9]","new":"[16.3]"},
   {"tier":"gold","index":3,"what":"Duplicate answer within tier (13 also at gold[2] cuboid). Re-posed ship 12 km N + 5 km E to 9 km N + 12 km E, giving distinct clean 15.","old":"[13]","new":"[15]"}
 ],
 "issues_resolved":2,
 "opener_concept":"Tiled-squares Pythagoras: count 9 + 16 tiles = 25, the square on the longest side, so the side is 5. Inline SVG shows the two tiled leg-squares on a 3-4-5 right triangle. A student who has never met Pythagoras answers box 1 by adding tile counts.",
 "notes":"Full guided conversion from a raw bank. Fresh-solved all 20 problems: 18 correct, 2 duplicate-answer diseases fixed (as the brief predicted for these un-audited boards). Added guided_steps to all 19 non-MC problems, honest-diagnosis misconceptions with derived expect values (null where non-determinate, e.g. gold isosceles full-base), opener + 3 teach walks + tier_guides. Trimmed method_card from 5 steps to 3 (validator caps at 4). Preserved worked_examples, related_videos ([]), topic_links byte-for-byte. Every guided box recomputed independently; phase boxes land on stored solutions."
}
json.dump(changes,open("changes_maths-ocr_geometry-L05.json","w",encoding="utf-8"),indent=2,ensure_ascii=False)

diag={
 "key":"geometry-L05",
 "board":"maths-ocr",
 "figures_added":[
   {"tier":"opener","index":0,"kind":"svg","what":"3-4-5 right triangle with a 3x3 (9) and 4x4 (16) tiled square on the two legs; c=? on the hypotenuse."},
   {"tier":"bronze","index":0,"kind":"svg","what":"Right triangle, legs 8 & 6 labelled, hypotenuse ?"},
   {"tier":"bronze","index":1,"kind":"svg","what":"Right triangle, hyp 13, leg 5, other leg ?"},
   {"tier":"bronze","index":2,"kind":"svg","what":"Right triangle, legs 12 & 5, hypotenuse ?"},
   {"tier":"bronze","index":3,"kind":"svg","what":"Right triangle, hyp 10, leg 6, other leg ?"},
   {"tier":"bronze","index":4,"kind":"svg","what":"Right triangle, legs 12 & 9, hypotenuse ?"},
   {"tier":"bronze","index":6,"kind":"svg","what":"Right triangle, legs 15 & 8, hypotenuse ?"},
   {"tier":"bronze","index":7,"kind":"svg","what":"Right triangle, hyp 25, leg 7, other leg ?"},
   {"tier":"silver","index":0,"kind":"svg","what":"Right triangle, opp 5, adj 12, angle theta=? marked at the vertex"},
   {"tier":"silver","index":1,"kind":"svg","what":"Right triangle, angle 40, adjacent 10, opposite ?"},
   {"tier":"silver","index":2,"kind":"svg","what":"Right triangle, angle 30, opposite 7, hypotenuse ?"},
   {"tier":"silver","index":3,"kind":"svg","what":"Right triangle, adjacent 8, hypotenuse 10, angle theta=?"},
   {"tier":"silver","index":4,"kind":"svg","what":"Ladder-against-wall right triangle: ground 3, ladder(hyp) 5, wall height ?"},
   {"tier":"silver","index":5,"kind":"svg","what":"Right triangle, angle 50, hypotenuse 15, adjacent ?"},
   {"tier":"silver","index":6,"kind":"svg","what":"Right triangle, opposite 7, hypotenuse 25, angle theta=? (re-posed problem)"},
   {"tier":"gold","index":0,"kind":"svg","what":"Rectangle 8 by 6 with dashed diagonal ?"},
   {"tier":"gold","index":1,"kind":"svg","what":"Isosceles triangle, equal sides 10, base 12, dashed height ?"},
   {"tier":"gold","index":2,"kind":"svg","what":"Isometric cuboid 4x3x12 with dashed space diagonal ?"},
   {"tier":"gold","index":3,"kind":"svg","what":"Right-angle journey: 9 km north, 12 km east, direct distance ? (re-posed)"},
   {"tier":"gold","index":4,"kind":"svg","what":"Angle-of-elevation right triangle: distance 50, angle 32, tree height ?"},
   {"tier":"teach.bronze","index":0,"kind":"svg","what":"Right triangle legs 16 & 12, hypotenuse ?"},
   {"tier":"teach.silver","index":0,"kind":"svg","what":"Right triangle opp 9, adj 12, angle theta=?"},
   {"tier":"teach.gold","index":0,"kind":"svg","what":"Ramp right triangle, run 9, rise ?, angle theta=?"}
 ],
 "opener_touched":True,
 "notes":"All figures are inline theme-safe SVG generated programmatically from each problem's own numbers (currentColor strokes/text, soft opacity fills, aria-labels, no external refs, xmlns omitted so the validator's external-ref check passes). Right-triangle leg proportions reflect the real geometry so angles look plausible; 'Diagram not drawn accurately' caption on every figure per exam convention. The multiple-choice ratio question (bronze[5]) has no figure by design (conceptual, not a specific triangle)."
}
json.dump(diag,open("changes_maths-ocr_geometry-L05_diagrams.json","w",encoding="utf-8"),indent=2,ensure_ascii=False)
print("wrote changes files")
