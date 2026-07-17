# -*- coding: utf-8 -*-
import json, io

changes = {
    "key": "geometry-L05",
    "problems_fixed": [
        {"tier": "bronze", "index": 6, "what": "Duplicate solution within bronze (was 10, same as bronze[0]). Changed hypotenuse 20 cm -> 18 cm so sin30 gives O = 9 cm, a clean non-calculator integer.", "old": "H=20, sol=10", "new": "H=18, sol=9"},
        {"tier": "gold", "index": 0, "what": "Duplicate solution within gold (was 40.0, same as gold[4]). Changed angle of depression 32 deg -> 35 deg so distance = 25/tan35 = 35.7 m, distinct from the field problem.", "old": "angle=32, sol=40", "new": "angle=35, sol=35.7"}
    ],
    "issues_resolved": 2,
    "opener_concept": "Tiled squares on a 3-4-5 right triangle: count 9 + 16 = 25 tiles, edge of the big square = 5, which IS Pythagoras before any formula. Inline SVG figure shown.",
    "notes": "Full guided-learning + diagrams conversion in one pass. Fresh-solved all 20 problems from display; every stored solution was mathematically correct, but two within-tier duplicate solutions would fail the validator (bronze had 10 twice, gold had 40 twice) - fixed with minimal edits above. Every misconception lacked the required expect key (these boards never got the enrichment pass); rewrote all 20 misconceptions as honest-diagnosis {pattern, message, expect} with every expect derived by committing the error (e.g. bronze[0] add-sides 6+8=14; silver[0] cos-instead-of-sin 11.5; gold[2] 2D-only diagonal 5). gold[1] isosceles expect=null (forgetting to halve gives no real root). Added guided_steps (with phase:'substitute' completion boundary) + plain-text hint to every problem, tier_descriptions, tier_guides (bronze/silver/gold), guided.opener + three teach walks, and slimmed method_card. Preserved related_videos, worked_examples, topic_links byte-for-byte. Diagrams: 20 exam-realism figures (SVG right triangles, trig triangles, isosceles, rectangle-free cliff, cuboid space diagonal, right-angled field) all theme-safe (currentColor text, fill-opacity regions) plus the tiled-squares opener figure. Validator PASS; independent recompute of every box, solution, and expect PASS; preservation check PASS."
}
json.dump(changes, io.open("changes_maths-aqa_geometry-L05.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

diagchanges = {
    "key": "geometry-L05",
    "figures_added": [
        {"tier": "opener", "index": 0, "kind": "svg", "what": "3-4-5 right triangle with a tiled square on each side (9, 16, ? tiles)."},
        {"tier": "bronze", "index": 0, "kind": "svg", "what": "Right triangle, legs 6 cm and 8 cm, hypotenuse ?."},
        {"tier": "bronze", "index": 1, "kind": "svg", "what": "Right triangle, hypotenuse 13 cm, leg 5 cm, other leg ?."},
        {"tier": "bronze", "index": 2, "kind": "svg", "what": "Right triangle, legs 9 cm and 12 cm, hypotenuse ?."},
        {"tier": "bronze", "index": 3, "kind": "svg", "what": "Right triangle, hypotenuse 10 cm, leg 6 cm, other leg ?."},
        {"tier": "bronze", "index": 4, "kind": "svg", "what": "Right triangle, legs 8 cm and 15 cm, hypotenuse ?."},
        {"tier": "bronze", "index": 5, "kind": "svg", "what": "Right triangle, legs 7 cm and 24 cm, hypotenuse ?."},
        {"tier": "bronze", "index": 6, "kind": "svg", "what": "Right triangle, 30 deg angle, hypotenuse 18 cm, opposite ?."},
        {"tier": "bronze", "index": 7, "kind": "svg", "what": "Right triangle, 60 deg angle, hypotenuse 14 cm, adjacent ?."},
        {"tier": "silver", "index": 0, "kind": "svg", "what": "Right triangle, 40 deg angle, hypotenuse 15 cm, opposite ?."},
        {"tier": "silver", "index": 1, "kind": "svg", "what": "Right triangle, 55 deg angle, hypotenuse 12 cm, adjacent ?."},
        {"tier": "silver", "index": 2, "kind": "svg", "what": "Right triangle, opposite 7 cm, hypotenuse 10 cm, angle theta."},
        {"tier": "silver", "index": 3, "kind": "svg", "what": "Right triangle, opposite 8 cm, adjacent 6 cm, angle theta."},
        {"tier": "silver", "index": 4, "kind": "svg", "what": "Ladder 5 m at 70 deg to the ground, height up wall ?."},
        {"tier": "silver", "index": 5, "kind": "svg", "what": "Right triangle, 38 deg angle, adjacent 9 cm, opposite x."},
        {"tier": "silver", "index": 6, "kind": "svg", "what": "Right triangle, legs 3.5 cm and 4.8 cm, hypotenuse ?."},
        {"tier": "gold", "index": 0, "kind": "svg", "what": "25 m cliff, angle of depression 35 deg to a boat, distance ?."},
        {"tier": "gold", "index": 1, "kind": "svg", "what": "Isosceles triangle, equal sides 10 cm, base 12 cm, height ?."},
        {"tier": "gold", "index": 2, "kind": "svg", "what": "Cuboid 4 x 3 x 12 cm with the space diagonal marked ?."},
        {"tier": "gold", "index": 3, "kind": "svg", "what": "Right triangle, 25 deg angle, adjacent 11 cm, hypotenuse ?."},
        {"tier": "gold", "index": 4, "kind": "svg", "what": "Right-angled field, legs 120 m and 50 m, diagonal path."}
    ],
    "opener_touched": True,
    "notes": "Diagrams done in the same pass as the guided conversion (board fan-out spec). Every figure generated programmatically from the problem's own numbers and re-checked against the display text and solution; all theme-safe (text fill=currentColor, region fills use fill-opacity)."
}
json.dump(diagchanges, io.open("changes_maths-aqa_geometry-L05_diagrams.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("changes files written")
