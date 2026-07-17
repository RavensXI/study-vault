# -*- coding: utf-8 -*-
import json, io

changes = {
 "key": "geometry-L06",
 "problems_fixed": [
  {"tier": "silver", "index": 6, "what": "Stored MC 'correct' answer disagreed with its own working. Fresh-solve a=4,b=7,c=9: cosC=(16+49-81)/56=-0.2857, C=106.6 deg.", "old": "111.8", "new": "106.6"},
  {"tier": "gold", "index": 0, "what": "Two-ships bearings distance: angle=80 deg, d2=325-300cos80=272.9, d=16.5 km. Stored MC option said 16.6 (its own message said 16.5).", "old": "16.6", "new": "16.5"},
  {"tier": "gold", "index": 2, "what": "PQR PR with angle 100 deg: PR2=185+30.6=215.6, PR=14.7 cm. Stored MC option said 14.8 (its own message said 14.7).", "old": "14.8", "new": "14.7"},
  {"tier": "bronze", "index": 3, "what": "Re-posed: conceptual MC 'When do you use the sine rule?' had no numeric answer for guided learning; replaced with a sine-rule find-side (A=50,a=9,B=40) = 7.6.", "old": "concept MC", "new": "single_value 7.6"},
  {"tier": "bronze", "index": 6, "what": "Re-posed: conceptual MC 'which info lets you use the sine rule' replaced with a sine-rule find-angle (a=7,A=35,b=9) = 47.5 deg.", "old": "concept MC", "new": "single_value 47.5"},
  {"tier": "silver", "index": 3, "what": "Re-posed: yes/no 'is 6,8,10 right-angled?' turned into cosine-rule find largest angle (opposite 10) = 90 deg, which surfaces the right angle by working.", "old": "yes/no MC", "new": "single_value 90"},
  {"tier": "silver", "index": 4, "what": "Removed a mis-posed trick MC (a=12,b=9,A=120 'cannot be solved directly'). Replaced with a clean obtuse SAS cosine-rule side (9,13, angle 110) = 18.2 cm, teaching the negative-cosine move.", "old": "trick MC", "new": "single_value 18.2"},
 ],
 "issues_resolved": 3,
 "opener_concept": "Triangular flag: a right-angled triangle is half a rectangle (6x8 -> 24). Tilt the corner and the true height shrinks to side x sinC, so Area = 1/2 ab sinC for ANY triangle; at 90 deg sin=1 recovers 1/2 base x height. Names the sinC factor that powers the area formula, sine rule and cosine rule.",
 "notes": "Full guided conversion: whole bank (8/7/5) converted from multiple_choice to single_value with numeric guided_steps (phase:substitute completion boundary on each), fresh openers + 3 teach walks, tier_guides, slim method_card. Every solution and every misconception expect independently recomputed (see _solve/_check scripts). Tier sizes preserved (8/7/5). Preserved related_videos (empty), topic_links, worked_examples from live; only edit to worked_examples was swapping em dashes in step LABELS for colons (style rule / validator). Misconception expects derived by committing the error (drop the half -> 2x area; invert the sine ratio; treat obtuse cosine as positive; sign slip on cosine numerator; Pythagoras instead of cosine for bearings). Validator PASS.",
}
json.dump(changes, io.open("changes_maths-eduqas_geometry-L06.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)

diagrams = {
 "key": "geometry-L06",
 "figures_added": [
  {"tier": "opener", "index": 0, "kind": "svg", "what": "Right-angled triangular flag, legs 8 m and 6 m, right-angle mark, Area = ?"},
  {"tier": "teach", "index": "bronze", "kind": "svg", "what": "Triangle side 8 cm opposite 30 deg, right angle, side b unknown (sine rule)"},
  {"tier": "teach", "index": "silver", "kind": "svg", "what": "Triangle sides 5 and 8 cm meeting at 60 deg, opposite side c unknown (cosine rule)"},
  {"tier": "teach", "index": "gold", "kind": "svg", "what": "Triangle side 9 opposite 35 deg, side 12 opposite the obtuse angle ? (ambiguous case)"},
  {"tier": "bronze", "index": 0, "kind": "svg", "what": "Side 6 opp 30 deg, angle 50 deg, side b = ?"},
  {"tier": "bronze", "index": 1, "kind": "svg", "what": "Side 10 opp 45 deg, angle 65 deg, side b = ?"},
  {"tier": "bronze", "index": 2, "kind": "svg", "what": "Side 8 opp 40 deg, side 10 opp unknown angle B"},
  {"tier": "bronze", "index": 3, "kind": "svg", "what": "Side 9 opp 50 deg, angle 40 deg, side b = ?"},
  {"tier": "bronze", "index": 4, "kind": "svg", "what": "Sides 5 and 8 cm at 30 deg, Area = ?"},
  {"tier": "bronze", "index": 5, "kind": "svg", "what": "Side 15 opp 80 deg, angle 35 deg, side a = ?"},
  {"tier": "bronze", "index": 6, "kind": "svg", "what": "Side 7 opp 35 deg, side 9 opp unknown angle B"},
  {"tier": "bronze", "index": 7, "kind": "svg", "what": "Right-angled triangle sides 12 and 7 cm, Area = ?"},
  {"tier": "silver", "index": 0, "kind": "svg", "what": "Sides 7 and 10 cm at 60 deg, opposite side a = ?"},
  {"tier": "silver", "index": 1, "kind": "svg", "what": "SSS 5, 8, 9; angle A opposite 5 = ?"},
  {"tier": "silver", "index": 2, "kind": "svg", "what": "Sides 11 and 14 cm at 42 deg, Area = ?"},
  {"tier": "silver", "index": 3, "kind": "svg", "what": "SSS 6, 8, 10; largest angle opposite 10 = ?"},
  {"tier": "silver", "index": 4, "kind": "svg", "what": "Sides 9 and 13 cm at 110 deg (obtuse), opposite side x = ?"},
  {"tier": "silver", "index": 5, "kind": "svg", "what": "Sides 15 and 20 cm at 75 deg, Area = ?"},
  {"tier": "silver", "index": 6, "kind": "svg", "what": "SSS 4, 7, 9; angle C opposite 9 = ? (obtuse)"},
  {"tier": "gold", "index": 1, "kind": "svg", "what": "SSS 13, 14, 15; Area = ?"},
  {"tier": "gold", "index": 2, "kind": "svg", "what": "Triangle PQR: PQ 8, QR 11 at 100 deg at Q, PR = ?"},
  {"tier": "gold", "index": 3, "kind": "svg", "what": "Sides 10 and 8 cm, Area = 30, included angle = ?"},
  {"tier": "gold", "index": 4, "kind": "svg", "what": "Parallelogram sides 10 and 6 cm, 70 deg angle, Area = ?"},
 ],
 "opener_touched": True,
 "notes": "Figures generated programmatically from each problem's own numbers (sss/render/tri engine reused from the Edexcel geometry-L06 pass). All theme-safe: currentColor strokes/text, soft #60a5fa fill-opacity regions, Inter labels, 'Diagram not drawn accurately' caption on every not-to-scale triangle. Every visible number cross-checked against the problem text (see _check script, 0 label mismatches). gold[0] (two-ships bearings) deliberately has NO figure: a faithful exam figure needs North lines and bearing arcs, and drawing the 80 deg angle would hand over the derive-the-angle step; kept as a pure word problem. 23 figures total.",
}
json.dump(diagrams, io.open("changes_maths-eduqas_geometry-L06_diagrams.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote both changes files")
