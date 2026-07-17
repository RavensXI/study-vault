import json
changes={
 "key":"geometry-L07",
 "problems_fixed":[
   {"tier":"gold","index":3,
    "what":"Stored question asked 'Find angle ADB' with AB a diameter, but ADB always equals 90 (angle in a semicircle), not the stored 62. The 62 was actually angle ABC. Reframed to a self-contained, correct two-step question.",
    "old":"A, B, C, D are on a circle. AB is a diameter. Angle CAB = 28°. Find angle ADB.  solutions:[62]",
    "new":"AB is a diameter of the circle. C is a point on the circle. Angle CAB = 28°. Find angle ABC.  solutions:[62] (ACB=90 semicircle, then 180-90-28=62)"}
 ],
 "issues_resolved":1,
 "opener_concept":"Runners on a circular track: the person at the centre swings through 124 to look from A to B; a spectator on the far circumference turns half as much. The halving IS the angle-at-centre-is-twice-circumference theorem.",
 "notes":"Fresh-solved all 20 problems from display text; only gold[3] was mathematically wrong. Rewrote all misconceptions to the required {pattern,message,expect} shape with derived numeric expects (null where no single wrong answer exists, e.g. s2 forgot-factor-two, s3 equal-tangents). Added guided_steps to all 19 non-multiple-choice problems with phase:'substitute' completion boundaries, tier_guides (3), tier descriptions, opener, three teach walks, and a slimmed method_card. No em dashes; British English; boxes numeric-only. Preserved related_videos, topic_links, worked_examples byte-for-byte."
}
json.dump(changes,open("changes_maths-aqa_geometry-L07.json","w",encoding="utf-8"),indent=1,ensure_ascii=False)

diagrams={
 "key":"geometry-L07",
 "figures_added":[
   {"tier":"bronze","index":0,"kind":"svg","what":"Circle, centre O, radii to A,B and chords to C: angle at centre 124 labelled, ? at circumference."},
   {"tier":"bronze","index":1,"kind":"svg","what":"Same centre/circumference figure: ? at centre, 48 at circumference."},
   {"tier":"bronze","index":2,"kind":"svg","what":"Diameter AB with C on circle, angle ACB marked ? (semicircle)."},
   {"tier":"bronze","index":3,"kind":"svg","what":"Cyclic quadrilateral, one angle 72 and its opposite marked ?."},
   {"tier":"bronze","index":4,"kind":"svg","what":"Chord AB with two points P,Q on the same arc: 35 and x subtending it."},
   {"tier":"bronze","index":5,"kind":"svg","what":"Tangent meeting a radius at T with the ? angle (multiple choice)."},
   {"tier":"bronze","index":6,"kind":"svg","what":"Centre/circumference figure: 150 at centre, ? at circumference."},
   {"tier":"bronze","index":7,"kind":"svg","what":"Right-angled triangle in a semicircle: right-angle square at C, 32 at A, ? at B."},
   {"tier":"silver","index":0,"kind":"svg","what":"Cyclic quadrilateral with all four angles 3x, 2x+10, x+40, 100 placed at the correct vertices (opposite pair 3x / x+40)."},
   {"tier":"silver","index":1,"kind":"svg","what":"Tangent and chord with 64, and the ? angle in the alternate segment."},
   {"tier":"silver","index":2,"kind":"svg","what":"Centre/circumference figure with expressions x+50 at centre and x at circumference."},
   {"tier":"silver","index":3,"kind":"svg","what":"Two tangents from external point T: TA=12 cm, TB=? ."},
   {"tier":"silver","index":4,"kind":"svg","what":"Angle BOC 140 at the centre with the reflex angle marked ?."},
   {"tier":"silver","index":5,"kind":"svg","what":"Tangent-chord 52 with radii to the centre and AOB marked ?."},
   {"tier":"silver","index":6,"kind":"svg","what":"Triangle inscribed in a circle: 40 at A, 55 at C, ? at B."},
   {"tier":"gold","index":0,"kind":"svg","what":"Two radii forming isosceles triangle OAB, OAB=25, C on major arc, ACB=?."},
   {"tier":"gold","index":1,"kind":"svg","what":"Cyclic quadrilateral with opposite angles 3x+10 (B) and 2x+20 (D)."},
   {"tier":"gold","index":2,"kind":"svg","what":"Tangent PT at T, chord TA, point B in alternate segment, PTA=70, ABT=?."},
   {"tier":"gold","index":3,"kind":"svg","what":"Diameter AB, right-angle square at C, angle CAB=28, ABC=? (repaired problem)."},
   {"tier":"gold","index":4,"kind":"svg","what":"Two radii isosceles, OAB=35, C on the minor arc, obtuse ACB=?."},
   {"tier":"opener","index":0,"kind":"svg","what":"Centre-and-circumference figure supporting the running-track hook."},
   {"tier":"teach.bronze","index":0,"kind":"svg","what":"Angle at centre 80, find circumference."},
   {"tier":"teach.silver","index":0,"kind":"svg","what":"Tangent-chord 50 with centre angle."},
   {"tier":"teach.gold","index":0,"kind":"svg","what":"Isosceles radii, OAB=20, C on major arc."}
 ],
 "opener_touched":True,
 "notes":"Circle theorems is a fully figured exam topic, so every non-trivial problem, the opener and all three teach walks carry an inline SVG. All figures are theme-safe (currentColor strokes/text, soft fills at 0.16 opacity), <3KB, role=img + aria-label, right-angle squares only where a 90 is given (not where it is the unknown), ? marks the asked angle, and 'Diagram not drawn accurately' captions on the geometric figures. Every visible label was cross-checked against the problem numbers programmatically (_verify_geoL07.py: 0 issues)."
}
json.dump(diagrams,open("changes_maths-aqa_geometry-L07_diagrams.json","w",encoding="utf-8"),indent=1,ensure_ascii=False)
print("changes files written")
