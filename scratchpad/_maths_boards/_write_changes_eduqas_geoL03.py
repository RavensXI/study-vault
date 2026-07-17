# -*- coding: utf-8 -*-
import json, io

conv = {"what": "MC->single_value: dropped options, solutions now the numeric value; added figure, hint, guided_steps, derived misconception expects",
        "old": "multiple_choice, solutions=[0]"}
pf = []
for tier, n in (("bronze",8),("silver",7),("gold",5)):
    for i in range(n):
        pf.append({"tier": tier, "index": i, "what": conv["what"], "old": conv["old"], "new": "single_value with guided walk + expect"})

changes = {
    "key": "maths-eduqas_geometry-L03",
    "problems_fixed": pf,
    "issues_resolved": 0,
    "opener_concept": "Packing a tray with 1 cm sugar cubes: count a 4x3 front face (12), then 2 layers deep (24) = length x width x height. Counting the cubes that fill a shape IS its volume.",
    "notes": "Fresh-solved all 20 problems from display: every stored answer (option 0) was already correct, so no wrong-answer repairs were needed. Repair here is the full guided conversion: all 20 MC problems converted to single_value with numeric solutions, each given a theme-safe currentColor SVG figure, a plain-text hint, a full guided_steps walk with completion boundary (phase:substitute), and misconceptions carrying derived numeric expects (committed each error to get the value; expects verified != correct answer). Added tier_guides (3), method_card trimmed, opener with cube-counting figure, teach walk per tier (cuboid 7x3x2=42; cone r6h9=339.3; cylinder+cone r4h6=402.1). Preserved topic_links and related_videos ([]). worked_examples preserved but step labels de-em-dashed ('Step 1 - Formula' -> 'Step 1: Formula') to satisfy the no-em-dash rule."
}
json.dump(changes, io.open("changes_maths-eduqas_geometry-L03.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)

figs = []
kinds = {"bronze":["cuboid","cube","triangular prism","cube","cuboid","cuboid","cube (V given, side ?)","10 cm cube (litre)"],
         "silver":["cylinder","cone","square-based pyramid","cylinder","cylinder (h unknown)","hemisphere","trapezium prism"],
         "gold":["sphere","sphere","sphere (V given, r ?)","cylinder vs cone comparison","cylinder + hemisphere composite"]}
for tier, arr in kinds.items():
    for i, w in enumerate(arr):
        figs.append({"tier": tier, "index": i, "kind": "svg", "what": w})
figs.append({"tier":"opener","index":0,"kind":"svg","what":"box of 1 cm cubes, 4x3 front x 2 deep"})
for tier, w in (("teach.bronze","cuboid 7x3x2"),("teach.silver","cone r6 h9"),("teach.gold","cylinder+cone r4 h6")):
    figs.append({"tier":tier,"index":0,"kind":"svg","what":w})

diag = {
    "key": "maths-eduqas_geometry-L03",
    "figures_added": figs,
    "opener_touched": True,
    "notes": "24 inline SVG figures added (20 bank problems + opener + 3 teach walks), all viewBox+role=img+aria-label, theme-safe (currentColor strokes/text, soft #60a5fa fills at low opacity), 'Diagram not drawn accurately' caption on every solid. Every label matches the problem's numbers (verified). Two figures authored fresh for this board: a trapezium prism (parallel sides 5/9, height 4, length 12) and a side-by-side cylinder-vs-cone comparison (r=5, h=12). No chart.js needed (no coordinate-axis problems in this lesson)."
}
json.dump(diag, io.open("changes_maths-eduqas_geometry-L03_diagrams.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("changes written; figures:", len(figs), "problems:", len(pf))
