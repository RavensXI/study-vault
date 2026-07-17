import json, io
changes = {
 "key": "geometry-L03",
 "board": "maths-aqa",
 "lesson_id": "28c3fccf-544d-4e44-a03f-635e88222391",
 "problems_fixed": [],
 "issues_resolved": 0,
 "opener_concept": "Filling a shoebox with 1 cm sugar cubes: a 3x2 layer stacked 2 high is counted by common sense (3x2x2=12), naming volume as length x width x height before any formula.",
 "notes": ("Fresh-solved all 20 bank problems from their displays: every stored "
           "solution was correct (bronze 72/150/120/197.9/4/64/471.2/92, silver "
           "314.2/904.8/201.1/10/120/1526.8/18, gold 75.4/326.7/261.8/636.7/5). "
           "No within-tier duplicates; frustum is similar-cone consistent (6/9=2/3). "
           "Zero maths repairs needed. Full guided conversion added: tier descriptions, "
           "per-problem hints and guided_steps (completion boundary at phase:substitute), "
           "honest-diagnosis misconceptions with derived expects (one per problem, two on G4), "
           "tier_guides, cube-grid opener, and one teach walk per tier. method_card, "
           "topic_links, related_videos (3), worked_examples (3) preserved byte-for-byte.")
}
json.dump(changes, io.open("changes_maths-aqa_geometry-L03.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)

figs = {
 "key": "geometry-L03",
 "board": "maths-aqa",
 "figures_added": [
  {"tier":"bronze","index":0,"kind":"svg","what":"cuboid 6x4x3 labelled"},
  {"tier":"bronze","index":1,"kind":"svg","what":"cube side 5"},
  {"tier":"bronze","index":2,"kind":"svg","what":"triangular prism, cross-section 12 cm2, length 10 cm"},
  {"tier":"bronze","index":3,"kind":"svg","what":"cylinder r=3, h=7"},
  {"tier":"bronze","index":4,"kind":"svg","what":"cuboid l=9, w=5, h=? "},
  {"tier":"bronze","index":5,"kind":"svg","what":"cube side 4"},
  {"tier":"bronze","index":6,"kind":"svg","what":"cylinder d=10, h=6"},
  {"tier":"bronze","index":7,"kind":"svg","what":"cuboid 8x3x2"},
  {"tier":"silver","index":0,"kind":"svg","what":"cone r=5, h=12"},
  {"tier":"silver","index":1,"kind":"svg","what":"sphere r=6"},
  {"tier":"silver","index":2,"kind":"svg","what":"sphere r=4 (surface area)"},
  {"tier":"silver","index":3,"kind":"svg","what":"cylinder r=5, h=? (SA=150pi)"},
  {"tier":"silver","index":4,"kind":"svg","what":"square-based pyramid base 6, h=10"},
  {"tier":"silver","index":5,"kind":"svg","what":"hemisphere r=9"},
  {"tier":"silver","index":6,"kind":"svg","what":"cone r=5, h=? (V=150pi)"},
  {"tier":"gold","index":0,"kind":"svg","what":"cone r=3, slant l=5 (total SA)"},
  {"tier":"gold","index":1,"kind":"svg","what":"frustum: large cone r6/h9 with small tip r2/h3 removed"},
  {"tier":"gold","index":2,"kind":"svg","what":"sphere r=5 inscribed in cylinder"},
  {"tier":"gold","index":3,"kind":"svg","what":"cylinder r=4/h=10 with hemisphere r=4 on top"},
  {"tier":"gold","index":4,"kind":"svg","what":"sphere with SA=100pi, r=?"},
  {"tier":"opener","index":0,"kind":"svg","what":"box split into 1 cm cubes, 3x2x2"},
  {"tier":"teach.bronze","index":0,"kind":"svg","what":"cuboid 5x4x2"},
  {"tier":"teach.silver","index":0,"kind":"svg","what":"cone r=6, h=6"},
  {"tier":"teach.gold","index":0,"kind":"svg","what":"cylinder+cone composite r=3"},
 ],
 "opener_touched": True,
 "notes": ("All figures generated programmatically from each problem's own numbers and "
           "re-read against the text/solutions. Theme-safe (currentColor strokes/text, "
           "soft fill-opacity regions), self-contained, viewBox+role+aria-label, "
           "'Diagram not drawn accurately' caption on the not-to-scale solids.")
}
json.dump(figs, io.open("changes_maths-aqa_geometry-L03_diagrams.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("changes files written")
