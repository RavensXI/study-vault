import json
guided={
 "key":"geometry-L06",
 "problems_fixed":[
  {"tier":"bronze","index":1,"what":"stored sine-rule angle B was wrong (sinB=0.7648 gives 49.9, not 49.5)","old":49.5,"new":49.9},
  {"tier":"silver","index":1,"what":"stored cosine-rule angle C was wrong (176/216=0.8148 gives 35.4, not 35.2)","old":35.2,"new":35.4},
  {"tier":"bronze","index":3,"what":"duplicate solution 10 within bronze (clashed with bronze[5] cosine-rule c=10); changed sides 8,5,30deg to 8,6,30deg for a clean distinct area","old":10,"new":12},
 ],
 "issues_resolved":3,
 "opener_concept":"Longer side faces the bigger angle: a 30-60-90 triangle (side opposite 30 = 5cm) where the student predicts the hypotenuse is double, then the reveal names the sine rule as making this proportionality exact.",
 "notes":"Full guided conversion: opener (with 30-60-90 SVG), three teach walks (sine-side, cosine-side, ambiguous-case), guided_steps on all 20 problems with phase boundary (setup pre-worked; solve-through + check live), tier_guides, slim method_card (51 words). All 20 misconceptions rebuilt into pattern/message/expect with honest derivable expects (inverted ratio, missing half, sign errors, forgotten sqrt, ambiguous-case one-solution). No em dashes; unicode maths. Validator PASS. Every walk box computed in Python and asserted to land on stored solutions."
}
json.dump(guided,open("changes_maths-aqa_geometry-L06.json","w",encoding="utf-8"),indent=1,ensure_ascii=False)

diagrams={
 "key":"geometry-L06",
 "figures_added":[
  {"tier":"opener","index":0,"kind":"svg","what":"30-60-90 triangle, right angle marked, side opposite 30 = 5cm, hypotenuse '?'"},
  {"tier":"bronze","index":0,"kind":"svg","what":"triangle ABC, angles 40/60, side b=12, side a='?'"},
  {"tier":"bronze","index":1,"kind":"svg","what":"triangle ABC, sides a=9 b=12, angle A=35, angle B='?'"},
  {"tier":"bronze","index":2,"kind":"svg","what":"triangle, sides 6 and 10, included 45, Area='?'"},
  {"tier":"bronze","index":3,"kind":"svg","what":"triangle, sides 8 and 6, included 30, Area='?'"},
  {"tier":"bronze","index":4,"kind":"svg","what":"triangle ABC, angles 50/80, side a=7, side b='?'"},
  {"tier":"bronze","index":5,"kind":"svg","what":"right-angled triangle, legs 6 and 8, right angle at C, c='?'"},
  {"tier":"bronze","index":6,"kind":"svg","what":"triangle, sides 12 and 9, included 60, Area='?'"},
  {"tier":"bronze","index":7,"kind":"svg","what":"triangle, sides b=10 c=7, included A=50, a='?'"},
  {"tier":"silver","index":0,"kind":"svg","what":"triangle ABC, sides 8/6/10, angle A='?'"},
  {"tier":"silver","index":1,"kind":"svg","what":"triangle ABC, sides 12/9/7, angle C='?'"},
  {"tier":"silver","index":2,"kind":"svg","what":"triangle, sides 11 and 14, included 75, third side '?'"},
  {"tier":"silver","index":3,"kind":"svg","what":"triangle PQR, PQ=15 PR=11 angle P=42, Area='?'"},
  {"tier":"silver","index":4,"kind":"svg","what":"triangle ABC, side a=5, angles A=30 B=105, side b='?'"},
  {"tier":"silver","index":5,"kind":"svg","what":"triangle, sides b=15 c=20, obtuse angle A=110, a='?'"},
  {"tier":"gold","index":0,"kind":"svg","what":"triangle ABC, sides a=10 b=7, angle B=40, angle A='?' (ambiguous)"},
  {"tier":"gold","index":2,"kind":"svg","what":"triangle PQR, PQ=10 PR=12, area 40, angle P='?'"},
  {"tier":"gold","index":3,"kind":"svg","what":"triangle sides 13/14/15, Area='?'"},
  {"tier":"gold","index":4,"kind":"svg","what":"triangle XYZ, sides x=9 y=11, obtuse angle Z=120, side z='?'"},
 ],
 "opener_touched":True,
 "notes":"18 problem triangles + 1 opener triangle, all generated programmatically to scale from each problem's own geometry so shapes are plausible; givens labelled, unknown marked '?'/'Area = ?', right angles squared, angle arcs drawn, 'Diagram not drawn accurately' caption. currentColor strokes/text + soft #60a5fa fill (theme-safe). No figures on the two bearings problems (gold[1], silver[6]): a bearings sketch showing north lines would risk mislabelling and the text is self-contained, so none is claimed. All figure numbers cross-checked against problem text/solutions."
}
json.dump(diagrams,open("changes_maths-aqa_geometry-L06_diagrams.json","w",encoding="utf-8"),indent=1,ensure_ascii=False)
print("wrote both changes files")
