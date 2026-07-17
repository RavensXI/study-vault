import json, io
KEY="maths-eduqas_geometry-L07"
guided={
 "key":KEY,
 "problems_fixed":[
  {"tier":"silver","index":3,"what":"Degenerate cyclic-quad: angles x,110,y,85 'in order' gave opposite pair 110+85=195 != 180. Reposed to valid ABCD with DAB=85, ABC=110, find BCD (opposite DAB)","old":"x,110,y,85 -> x=95 (no valid quad)","new":"DAB=85, ABC=110, BCD=180-85=95"},
  {"tier":"gold","index":1,"what":"Degenerate cyclic-quad 3x,2x+10,4x-20,y: opposite pair 7x-20=180 -> x=28.57, no option fits. Reposed to opposite 4x and 2x+30","old":"3x,2x+10,4x-20,y (x=30 claimed, unsolvable)","new":"4x and 2x+30 opposite -> 6x=150, x=25"},
  {"tier":"gold","index":3,"what":"Replaced out-of-GCSE-spec tangent-secant power-of-a-point (tan^2=ext*whole) with in-spec isosceles-radii chain","old":"tangent 8, secant ext 4, find whole=16","new":"O centre, OAB=26, C major arc, ACB=64"},
  {"tier":"gold","index":4,"what":"Replaced out-of-GCSE-spec intersecting-chords power-of-a-point (AP*PB=CP*PD) with in-spec semicircle triangle","old":"chords AP=3,PB=8,CP=4, find PD=6","new":"AB diameter, CAB=34, find ABC=56"},
  {"tier":"bronze","index":1,"what":"Changed circumference value 35->34 so centre answer (68) is distinct from bronze[0]'s 70 (avoids within-tier duplicate solution once converted to numeric)","old":"circ 35 -> centre 70","new":"circ 34 -> centre 68"},
  {"tier":"all","index":-1,"what":"Converted every numeric multiple_choice problem to single_value with guided_steps + honest misconception expects; kept 4 genuinely conceptual recalls as multiple_choice (b5 diameter->90, b7 chord-through-centre, s2 tangent-radius, g3 which-theorem)","old":"16/20 multiple_choice, no guided steps","new":"16 single_value guided + 4 MC"},
  {"tier":"worked_examples","index":-1,"what":"Stripped pre-existing em dashes in step labels ('Step 1 — Theorem' -> 'Step 1: Theorem') to satisfy the no-em-dash rule; content otherwise preserved","old":"Step 1 — Theorem","new":"Step 1: Theorem"}
 ],
 "issues_resolved":7,
 "opener_concept":"Lighthouse at the centre O of a circular bay sweeps its beam 120 degrees from boat A to boat B; a watcher on the shore (on the circle) turns half as much. Answering '120 / 2 = 60' by common sense IS the angle-at-centre-is-twice-the-circumference theorem.",
 "notes":"Bank was 100% multiple_choice with no hints/expects and two degenerate cyclic-quad problems plus two out-of-GCSE-spec power-of-a-point problems (matching the AQA/OCR sibling diseases). Fresh-solved all 20; converted to Tom-approved guided shape mirroring maths-aqa geometry-L07. Distinct within-tier answers: bronze {70,68,90,48,55,45}, silver {108,12,95,40,280,30}, gold {130,25,64,56}. topic_links/related_videos([])/worked_examples preserved."
}
json.dump(guided, io.open("changes_maths-eduqas_geometry-L07.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)

diagrams={
 "key":KEY,
 "figures_added":[
  {"tier":"bronze","index":0,"kind":"svg","what":"Angle at centre (140) and circumference (?) on same arc"},
  {"tier":"bronze","index":1,"kind":"svg","what":"Angle at circumference (34) and centre (?)"},
  {"tier":"bronze","index":2,"kind":"svg","what":"Triangle in semicircle, AB diameter, ? at C"},
  {"tier":"bronze","index":3,"kind":"svg","what":"Two same-segment angles on chord AB: 48 and x"},
  {"tier":"bronze","index":4,"kind":"svg","what":"Semicircle: diameter subtends angle (MC)"},
  {"tier":"bronze","index":5,"kind":"svg","what":"Two same-segment angles: x and 55"},
  {"tier":"bronze","index":6,"kind":"svg","what":"Chord through the centre (diameter, MC)"},
  {"tier":"bronze","index":7,"kind":"svg","what":"Angle at centre (90) and circumference (?)"},
  {"tier":"silver","index":0,"kind":"svg","what":"Cyclic quad, angle A=72, opposite C=?"},
  {"tier":"silver","index":1,"kind":"svg","what":"Tangent meets radius at T (MC)"},
  {"tier":"silver","index":2,"kind":"svg","what":"Two tangents from external T: TA=12 cm, TB=?"},
  {"tier":"silver","index":3,"kind":"svg","what":"Cyclic quad ABCD: A=85, B=110, C=?"},
  {"tier":"silver","index":4,"kind":"svg","what":"Tangent, chord and radius at A; 50 marked, chord-radius ?"},
  {"tier":"silver","index":5,"kind":"svg","what":"Inscribed angle 40 at C (reflex centre asked)"},
  {"tier":"silver","index":6,"kind":"svg","what":"Right-angle triangle in semicircle, angles x and 2x"},
  {"tier":"gold","index":0,"kind":"svg","what":"Tangent-chord 65 with centre angle ? (AOB)"},
  {"tier":"gold","index":1,"kind":"svg","what":"Cyclic quad opposite angles 4x and 2x+30"},
  {"tier":"gold","index":3,"kind":"svg","what":"Isosceles radii, OAB=26, C on major arc, ACB=?"},
  {"tier":"gold","index":4,"kind":"svg","what":"Right-angle triangle in semicircle, CAB=34, ABC=?"},
  {"tier":"opener","index":-1,"kind":"svg","what":"Lighthouse-beam angle-at-centre figure (120 at centre)"},
  {"tier":"teach.bronze","index":-1,"kind":"svg","what":"Centre 100, circumference ?"},
  {"tier":"teach.silver","index":-1,"kind":"svg","what":"Cyclic quad opposite 3x and x+40"},
  {"tier":"teach.gold","index":-1,"kind":"svg","what":"Isosceles radii, OAB=20, major arc"}
 ],
 "opener_touched":True,
 "notes":"23 inline SVG figures added in the same pass. All theme-safe (currentColor strokes/text, soft fill-opacity), lean (<2KB each), 'Diagram not drawn accurately' captions on geometric figures. Geometry reuses the Tom-approved maths-aqa geometry-L07 figure coordinates with number/label swaps; two custom figures (tangent-chord-radius split, chord-through-centre). Only g3 (which-theorem, abstract) has no figure by design. Every visible number verified against problem text and solutions."
}
json.dump(diagrams, io.open("changes_maths-eduqas_geometry-L07_diagrams.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote changes_maths-eduqas_geometry-L07.json and _diagrams.json")
