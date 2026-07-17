# -*- coding: utf-8 -*-
import io, json

changes = {
    "key": "geometry-L08",
    "board": "maths-ocr",
    "lesson_id": "47a41e5d-3d22-45fd-a1c0-b29405585d87",
    "problems_fixed": [
        {"tier": "bronze", "index": 0,
         "what": "Duplicate solution 5 within bronze (also |(3,4)|=5). Changed the added vector (3,-1)->(1,-1) so x-component = 3; b1 y-component stays 4.",
         "old": 5, "new": 3},
        {"tier": "silver", "index": 4,
         "what": "Duplicate solution 5 within silver (three 5s). Changed B (8,10)->(10,10) so midpoint x-component = 6.",
         "old": 5, "new": 6},
        {"tier": "silver", "index": 5,
         "what": "Duplicate solution 5 within silver. Changed |(-3,4)|=5 to |(-6,8)|=10 (6-8-10 triple, clean integer).",
         "old": 5, "new": 10},
    ],
    "issues_resolved": 3,
    "opener_concept": "Treasure-map walk on a counted grid: 3 east + 2 north, then 1 east + 4 north. Counting total east (4) and total north (6) IS adding the column vectors (3,2)+(1,4)=(4,6).",
    "notes": "Full fresh conversion (row was un-converted: only method_card/problem_bank/related_videos/topic_links/worked_examples existed). All 20 stored solutions fresh-solved and correct; the only bank defects were within-tier duplicate answers (validator-fatal) fixed with minimal clean-integer edits. method_card trimmed 5->4 steps (validator max). Every misconception given a derived 'expect' (committed the error); none equals the correct answer. Added guided_steps to all 20 problems, tier_guides x3, opener, teach x3. related_videos/topic_links/worked_examples preserved byte-for-byte. PATCH 204, round-trip equal. Validator PASS.",
}
json.dump(changes, io.open('changes_maths-ocr_geometry-L08.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

diagrams = {
    "key": "geometry-L08",
    "board": "maths-ocr",
    "figures_added": [
        {"tier": "bronze", "index": 4, "kind": "svg", "what": "Right triangle legs 3 and 4, hypotenuse ? for |(3,4)|."},
        {"tier": "bronze", "index": 7, "kind": "svg", "what": "Right triangle legs 5 and 12, hypotenuse ? for |(5,12)|."},
        {"tier": "silver", "index": 0, "kind": "svg", "what": "Coordinate grid with A(1,3), B(5,7) and vector AB drawn (run/rise dashed)."},
        {"tier": "silver", "index": 3, "kind": "svg", "what": "Two vectors (2,6) and (3,9) from one point, same direction (parallel)."},
        {"tier": "silver", "index": 4, "kind": "svg", "what": "Segment AB with midpoint M marked halfway."},
        {"tier": "silver", "index": 5, "kind": "svg", "what": "Right triangle legs 6 and 8, hypotenuse ? for |(-6,8)| (magnitude ignores sign)."},
        {"tier": "gold", "index": 0, "kind": "svg", "what": "Position-vector diagram: O, a to A, b to B, midpoint M with OM = ?."},
        {"tier": "gold", "index": 1, "kind": "svg", "what": "Segment AB with P one third along (AP:PB = 1:2)."},
        {"tier": "gold", "index": 2, "kind": "svg", "what": "Three equally spaced collinear points A, B, C."},
        {"tier": "gold", "index": 3, "kind": "svg", "what": "Right triangle legs a and a, hypotenuse 10 for |(a,a)|=10."},
        {"tier": "gold", "index": 4, "kind": "svg", "what": "Segment AB with P two thirds along (AP:PB = 2:1)."},
    ],
    "opener_touched": True,
    "notes": "Opener carries a counted coordinate grid (to scale). Magnitude problems get exam-style right triangles (labels = |x|,|y|, hypotenuse ?). Position-vector/ratio/collinear figures are exam-realistic schematics with 'Diagram not drawn accurately' captions. All theme-safe (currentColor strokes/text, soft opacity fills), self-contained, each <3KB. Every visible label cross-checked against the problem numbers.",
}
json.dump(diagrams, io.open('changes_maths-ocr_geometry-L08_diagrams.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print("wrote changes files")
