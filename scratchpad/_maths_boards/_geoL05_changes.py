import io, json

changes = {
 "key": "maths-eduqas_geometry-L05",
 "problems_fixed": [
   {"tier": "bronze", "index": 7, "what": "Original rectangle problem (diagonal 10 cm, side 6 cm) gave answer 8, a duplicate of bronze[3] (hyp 10, side 6, also 8) and identical maths. Re-posed as diagonal 20 cm, width 12 cm -> length 16, clean integer, distinct within tier.",
    "old": "diagonal 10 cm, side 6 cm -> 8 cm", "new": "diagonal 20 cm, width 12 cm -> 16 cm"},
 ],
 "issues_resolved": 1,
 "opener_concept": "Tiled squares on a 3-4-5 triangle: student counts 9 tiles + 16 tiles = 25 tiles, then finds the edge (5) of a 25-tile square. Names Pythagoras (a^2 + b^2 = c^2) as squaring = counting tiles, rooting = length. Same concrete angle as the Edexcel sibling, rewritten with fresh text; SVG figure supplied.",
 "notes": "All 18 computational MCQs converted to single_value with full guided_steps (phase:'substitute' completion boundary, check step landing on the stored solution) plus honest single-error misconception expects derived by committing the error. Two genuinely conceptual items kept as multiple_choice (bronze[5] 'is 9,12,15 right-angled', silver[5] 'which ratio uses O and A'); walks omitted per spec, expect:null on their misconceptions. Added guided.opener + teach walks (bronze 9,12->15; silver opp5/adj12->22.6; gold slide 2/5->21.8) and tier_guides for all three tiers; slimmed method_card. Every box, solution and expect recomputed in Python. Fresh-solve found NO wrong stored answers (all MCQ option 0 were correct); only defect was the B8 duplicate. Preserved topic_links, related_videos ([]), worked_examples byte-for-byte EXCEPT worked_examples step labels where preserved em dashes were replaced with colons to satisfy the banned-em-dash style rule / validator.",
}
json.dump(changes, io.open("changes_maths-eduqas_geometry-L05.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

diag = {
 "key": "maths-eduqas_geometry-L05",
 "figures_added": [
   {"tier": "opener", "index": 0, "kind": "svg", "what": "3-4-5 right triangle with a tiled square on each side (9, 16, ? tiles)"},
   {"tier": "bronze", "index": 0, "kind": "svg", "what": "right triangle, legs 3 cm and 4 cm, hypotenuse ?"},
   {"tier": "bronze", "index": 1, "kind": "svg", "what": "right triangle, legs 8 cm and 15 cm, hypotenuse ?"},
   {"tier": "bronze", "index": 2, "kind": "svg", "what": "right triangle, hyp 13 cm, side 5 cm, other side ?"},
   {"tier": "bronze", "index": 3, "kind": "svg", "what": "right triangle, hyp 10 cm, side 6 cm, other side ?"},
   {"tier": "bronze", "index": 4, "kind": "svg", "what": "right triangle, legs 7 cm and 24 cm, hypotenuse ?"},
   {"tier": "bronze", "index": 5, "kind": "svg", "what": "triangle labelled 9, 12, 15 (right-angle test)"},
   {"tier": "bronze", "index": 6, "kind": "svg", "what": "right triangle, legs 9 and 40, hypotenuse x"},
   {"tier": "bronze", "index": 7, "kind": "svg", "what": "rectangle, width 12 cm, diagonal 20 cm, length ?"},
   {"tier": "silver", "index": 1, "kind": "svg", "what": "right triangle, 40deg angle, hyp 15 cm, opposite ?"},
   {"tier": "silver", "index": 2, "kind": "svg", "what": "right triangle, 55deg angle, hyp 20 cm, adjacent ?"},
   {"tier": "silver", "index": 3, "kind": "svg", "what": "right triangle, opposite 8, adjacent 15, angle theta"},
   {"tier": "silver", "index": 4, "kind": "svg", "what": "right triangle, 30deg angle, opposite 6 cm, hypotenuse ?"},
   {"tier": "silver", "index": 6, "kind": "svg", "what": "right triangle, 50deg angle, adjacent 10 cm, opposite ?"},
   {"tier": "gold", "index": 0, "kind": "svg", "what": "ladder 5 m (hyp), foot 1.5 m, height ?"},
   {"tier": "gold", "index": 1, "kind": "svg", "what": "isosceles triangle, equal sides 10 cm, base 12 cm, height ?"},
   {"tier": "gold", "index": 2, "kind": "svg", "what": "40 m cliff, 25deg angle of depression, distance ? to boat"},
   {"tier": "gold", "index": 3, "kind": "svg", "what": "coordinate grid, (1,2) to (4,6), legs 3 and 4, distance ?"},
   {"tier": "gold", "index": 4, "kind": "svg", "what": "ship 12 km east, 9 km north, North arrow, return path (bearing)"},
 ],
 "opener_touched": True,
 "notes": "19 inline SVG figures (theme-safe: text currentColor, region fills soft with fill-opacity, no external refs). No figure on silver[0] (sinθ=0.6, abstract) or silver[5]/bronze[5] wording-only MCQ ('which ratio'). Every figure generated programmatically from the problem's own numbers; every label re-read against the text. Right-angle squares, angle arcs and 'not drawn accurately' captions per exam convention.",
}
json.dump(diag, io.open("changes_maths-eduqas_geometry-L05_diagrams.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote both changes files")
