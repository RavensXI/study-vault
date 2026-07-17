# -*- coding: utf-8 -*-
import json, io, shutil
# board-named shard copy (ship-gate naming)
shutil.copyfile("lesson_number-L02.json","lesson_maths-aqa_number-L02.json")

changes={
 "key":"number-L02",
 "board":"maths-aqa",
 "problems_fixed":[
   {"tier":"bronze","index":7,"what":"duplicate answer 1/2 within bronze (same as bronze[2] 5/6-1/3); changed divisor to de-duplicate, clean integer-ratio result",
    "old":"\\(\\frac{2}{5} \\div \\frac{4}{5}\\) = 1/2 [1,2]",
    "new":"\\(\\frac{2}{5} \\div \\frac{3}{5}\\) = 2/3 [2,3]"},
 ],
 "issues_resolved":1,
 "misconceptions_enriched":"All 26 misconceptions across 20 problems given a validator-required 'expect' derived by committing the error (add/subtract-both, no-flip, no-simplify, no-convert, whole-only, order-of-operations, no-scale-numerators). Every expect independently reproduced in _verify_expects.py.",
 "figures_added":[
   {"tier":"opener","index":0,"kind":"svg","what":"12-square chocolate bar, 3 squares shaded blue (1/4) and 4 amber (1/3), currentColor strokes/labels, soft fill-opacity 0.35, theme-safe, ~1KB. Makes the counting hook concrete (shows what it says)."},
 ],
 "opener_concept":"Chocolate bar of 12 squares: eat 1/4 (=3 squares) then 1/3 (=4 squares) = 7 squares = 7/12. Student counts squares by common sense; reveal names 12 as the common denominator (12 divides evenly into quarters and thirds).",
 "opener_touched":True,
 "notes":"Fresh-solved all 20 problems: every stored solution correct; only defect was the bronze duplicate (fixed). Added guided.opener (SVG), guided.teach x3 (1/2+1/3; 1.5x2.33; 3/4 div 1/2 minus 1/2), tier_guides x3 with worked examples, per-problem hints and full guided_steps (setup pre-worked to phase:'substitute' at combine/simplify, finish = combine numerators + simplify + check), tier descriptions. Trimmed method_card to 4 steps / 95 words. Preserved related_videos, worked_examples, topic_links byte-for-byte. No diagrams on bank problems: pure fraction arithmetic, exam prints no figure (exam-realism test). Validator PASS; PATCH 204; round-trip exact.",
}
json.dump(changes, io.open("changes_maths-aqa_number-L02.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote lesson_maths-aqa_number-L02.json and changes_maths-aqa_number-L02.json")
