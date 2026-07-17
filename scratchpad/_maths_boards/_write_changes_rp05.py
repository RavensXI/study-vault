# -*- coding: utf-8 -*-
import json, io
changes = {
 "key": "ratio-proportion-L05",
 "problems_fixed": [
   {"tier": "bronze", "index": 2, "what": "Duplicate answer within bronze (B0 and B2 both k=3). Changed y from 24 to 16 so k=2.",
    "old": "y \\propto x^3, x=2, y=24, k=3", "new": "y \\propto x^3, x=2, y=16, k=2"},
   {"tier": "gold", "index": 1, "what": "Duplicate answer within gold (G1 and G3 both 3). Changed target x from 16 to 36 so y=2.",
    "old": "find y at x=16 -> y=3", "new": "find y at x=36 -> y=2"}
 ],
 "issues_resolved": 2,
 "opener_concept": "Two square patios, sides 2 m and 4 m, laid with the same slabs. Student computes areas 4 and 16 by common sense and sees doubling the side quadruples the area (2 squared). That IS area proportional to side squared: A = k s squared. Names the find-k-then-use method with a power. Inline SVG shows the two squares to scale.",
 "notes": "Fresh-solved all 20 problems from display: every stored solution was mathematically correct; the only defects were the two within-tier duplicate answers (the exact disease flagged in the board brief), fixed with minimal clean-integer edits and full recompute of steps/misconceptions. Converted all misconceptions from the old {check,message} format to honest-diagnosis {pattern,expect,message} with expect committed by actually making the error (nulls where the wrong answer is non-clean, e.g. forgot-to-root cases). Added guided_steps to all 19 non-MC problems plus a walk to the MC problem, tier_guides, teach walks (bronze/silver/gold, fresh numbers not in bank), and slimmed method_card from 5 steps to 4. All boxes independently recomputed and land on stored solutions. No em dashes. Non-calculator answers all clean integers or 2.5. Preserved topic_links, related_videos, worked_examples byte-for-byte."
}
io.open("changes_maths-aqa_ratio-proportion-L05.json","w",encoding="utf-8").write(json.dumps(changes, indent=1, ensure_ascii=False))

diagrams = {
 "key": "ratio-proportion-L05",
 "figures_added": [
   {"tier": "opener", "index": 0, "kind": "svg",
    "what": "Two squares (side 2 m and side 4 m, drawn roughly to scale, soft blue/amber fills, currentColor strokes and labels) so the 'two square patios' hook is shown, not just claimed."}
 ],
 "opener_touched": True,
 "notes": "Proportion-with-powers is a textual/algebraic topic: the exam prints no figure for the equation problems (light intensity, magnets, gas law are stated in words), so per the exam-realism test no bank problem gets a decorative diagram. The one figure added is the opener's two-squares SVG, required by the show-what-you-say rule because the opener text refers to two square patios. Theme-safe: text and strokes use currentColor, region fills use fill-opacity 0.3."
}
io.open("changes_maths-aqa_ratio-proportion-L05_diagrams.json","w",encoding="utf-8").write(json.dumps(diagrams, indent=1, ensure_ascii=False))
print("changes files written")
