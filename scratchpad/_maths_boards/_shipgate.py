import json, shutil
pd=json.load(open("lesson_geometry-L01.json",encoding="utf-8"))
# shard
json.dump(pd, open("lesson_maths-eduqas_geometry-L01.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)

changes={
 "key":"geometry-L01",
 "problems_fixed":[
   {"tier":"gold","index":1,
    "what":"Stored solution was index 0 (48°) but a regular pentagon (108°) and hexagon (120°) around a point leave x = 360 − 108 − 120 = 132°. Corrected to index 1 (132°); the misconception message itself already computed 132.",
    "old":"solutions:[0] -> 48°","new":"solutions:[1] -> 132°"}
 ],
 "issues_resolved":1,
 "opener_concept":"Pizza cut from the centre into three slices (120°, 150°, ?): the slices fill a full turn, 360°, so the last is 90°. A second box shares 360° between 4 equal slices. Reveal names the two foundational facts: angles at a point = 360°, angles on a straight line = 180°. SVG-drawn pizza.",
 "notes":"Fresh-solved all 20 problems (8 bronze / 7 silver / 5 gold) from display text; every stored solution was correct except gold[1] (pentagon+hexagon), fixed. All items are multiple_choice, so guided_steps are optional (validator) and the guided experience is carried by the opener + three teach walks (bronze triangle-then-line, silver 12-gon interior/exterior, gold quadrilateral algebra) plus tier_guides. Added a plain-text hint to every problem and rebuilt every misconception to honest-diagnosis format with an expect equal to the specific distractor option index the error yields (null where non-determinate). Slimmed method_card to reference size; de-em-dashed worked_examples step labels (Step 1 — ... -> Step 1: ...). Preserved related_videos, topic_links, worked_examples content, options, tier sizes and input types. Validator PASS; PATCHed practice_data only."
}
json.dump(changes, open("changes_maths-eduqas_geometry-L01.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)

# diagrams changes: reconstruct figure list
figs=[]
def has_svg(p): return "<svg" in (p.get("display") or "")
descr={
 ("bronze",0):"Straight line: known angle 130° and unknown x on it",
 ("bronze",1):"Two crossing lines: vertically opposite angles, 72° and ?",
 ("bronze",2):"Triangle with angles 55°, 80° and ?",
 ("bronze",3):"Three angles at a point: 90°, 150° and ? (rays from a point)",
 ("bronze",4):"Isosceles triangle: apex 40°, two equal base angles ? (tick marks on equal sides)",
 ("bronze",6):"Right-angled triangle: right-angle square, 35° and ?",
 ("bronze",7):"Straight line split into three angles x, x and 60° (not to scale)",
 ("silver",0):"Parallel lines + transversal, alternate angle 65° and ? (Z-shape)",
 ("silver",1):"Parallel lines + transversal, co-interior angle 110° and ? (C-shape)",
 ("silver",2):"Regular hexagon outline",
 ("silver",4):"Regular decagon outline",
 ("silver",6):"Triangle with angles 3x, 4x and 5x (not to scale)",
 ("gold",1):"Pentagon (108°) and hexagon (120°) interiors meeting at a point with gap x",
 ("gold",2):"Parallel lines + transversal, alternate angles 3x+10 and 5x−20 (Z-shape)",
}
pb=pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        if has_svg(p):
            figs.append({"tier":tier,"index":i,"kind":"svg","what":descr.get((tier,i),"figure")})
dch={"key":"geometry-L01","figures_added":figs,"opener_touched":True,
 "notes":"14 problem figures plus an SVG pizza in the opener, all generated programmatically from each problem's own numbers and theme-safe (currentColor strokes/text, soft fills at low opacity, no external refs). Polygon-computation problems given as pure text (S4, S6, G1, G4, G5) and the quadrilateral fact-recall (B6) left without figures, matching how an exam prints them. Every visible label matches the problem text; unknowns marked ? or x. Rendered and eyeballed in-browser."}
json.dump(dch, open("changes_maths-eduqas_geometry-L01_diagrams.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote shard + 2 changes files; figures:",len(figs))
