import json, io
changes={
 "key":"geometry-L01",
 "problems_fixed":[
   {"tier":"bronze","index":0,"what":"duplicate answer within bronze (65 shared with B4 triangle); changed 115 to 110 so x=70, clearing the collision","old":"x and 115 (x=65)","new":"x and 110 (x=70)"}
 ],
 "issues_resolved":1,
 "opener_concept":"Flat table + pencil (straight line = 180 minus the given angle), then a pencil at a clock centre (full turn = 360 minus the two known angles). Names the two foundational facts.",
 "notes":"Fresh-solved all 15 problems from display; every stored solution was already correct. Full guided conversion added: opener (with straight-line SVG), three teach walks (bronze triangle SVG, silver polygon, gold parallel-lines SVG), guided_steps on all 15 problems with phase:substitute boundaries, plain hints, tier_guides, tier descriptions. Misconceptions rebuilt to honest-diagnosis format with derivable expect values (single_value). Preserved related_videos, worked_examples, topic_links, method_card byte-for-byte."
}
json.dump(changes, io.open("changes_maths-aqa_geometry-L01.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)

figs={
 "key":"geometry-L01",
 "figures_added":[
  {"tier":"bronze","index":0,"kind":"svg","what":"Straight line, two angles 110 and ? at a point"},
  {"tier":"bronze","index":1,"kind":"svg","what":"Around a point: sectors 120, 85, ?"},
  {"tier":"bronze","index":2,"kind":"svg","what":"Vertically opposite angles 70 and 3x+10 across an X"},
  {"tier":"bronze","index":3,"kind":"svg","what":"Triangle with angles 40, 75, ?"},
  {"tier":"bronze","index":5,"kind":"svg","what":"Quadrilateral with angles 90, 80, 110, ?"},
  {"tier":"bronze","index":6,"kind":"svg","what":"Straight line, angles 3x+30 and 2x"},
  {"tier":"silver","index":0,"kind":"svg","what":"Triangle with side extended, exterior 130, interior 55 and x"},
  {"tier":"silver","index":2,"kind":"svg","what":"Parallel lines + transversal, alternate angles 65 and x"},
  {"tier":"silver","index":3,"kind":"svg","what":"Parallel lines + transversal, co-interior 72 and ?"},
  {"tier":"silver","index":4,"kind":"svg","what":"Pentagon with angles x, 2x, 3x, 90, 120"},
  {"tier":"silver","index":5,"kind":"svg","what":"Isosceles triangle, equal-side ticks, base angle 50, apex ?"},
  {"tier":"gold","index":0,"kind":"svg","what":"Parallel lines + transversal, corresponding 3x+15 and 5x-25"},
  {"tier":"gold","index":2,"kind":"svg","what":"Hexagon with six labelled angles"}
 ],
 "opener_touched":True,
 "notes":"13 bank SVGs plus opener straight-line figure and two teach-walk figures (bronze triangle, gold parallel lines). All theme-safe (currentColor strokes/text, soft fills with fill-opacity), self-contained, exam 'not drawn accurately' captions. Figures generated programmatically from each problem's own values; labels cross-checked against solutions."
}
json.dump(figs, io.open("changes_maths-aqa_geometry-L01_diagrams.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote changes files")
