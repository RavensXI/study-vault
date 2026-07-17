# -*- coding: utf-8 -*-
import json, io

changes = {
 "key": "maths-eduqas_number-L03",
 "problems_fixed": [
  {"tier":"silver","index":5,
   "what":"Duplicate solution within tier (silver[4] 7.2/0.09 and silver[5] estimate both = 80), which the validator rejects. Re-posed the estimate to a distinct clean answer.",
   "old":"Estimate 4.1 x 19.7 by rounding each to 1 s.f. = 80",
   "new":"Estimate 6.2 x 4.8 by rounding each to 1 s.f. = 30"},
  {"tier":"gold","index":1,
   "what":"Mis-posed: display said 'to 1 s.f.' but 48.6 to 1 s.f. is 50, giving sqrt(50)/0.2 ~= 40, not the stored 35. Reworded to instruct the nearest-square method (the intended GCSE approach), which yields sqrt(49)/0.2 = 35 cleanly.",
   "old":"Estimate sqrt(48.6)/0.21 to 1 s.f.",
   "new":"Estimate sqrt(48.6)/0.21. Round 48.6 to the nearest square number and 0.21 to 1 s.f."}
 ],
 "issues_resolved": 2,
 "opener_concept": "Number line from 3 to 4 (SVG) with a marker: is 3.7 nearer 3 or 4? then 3.2? The halfway value 3.5 is the tipping point. Names rounding by pure common sense before any dp/sf rule.",
 "notes": "Full guided conversion: all 20 bank problems given guided_steps with substitute completion boundaries, plain-text hints, and honest-diagnosis misconceptions with derived expects. Bank was arithmetically correct on fresh-solve except the two fixes above. Four rounding misconceptions (bronze[2] 12.365->12.37, bronze[3] 0.5482->0.55, silver[1] 0.00372->0.0037, silver[6] 0.06049->0.0605) could not use their natural round-direction expect because the wrong value sits within the validator's 0.011 absolute tolerance of the answer; bronze[2]/[3] were re-diagnosed as 1-dp errors (12.4, 0.5), silver[1]/[6] set expect null (message retained as guidance). tier_guides + teach walks (bronze/silver/gold) + 3 method-card-slim preserved. method_card, topic_links, related_videos, worked_examples preserved byte-for-byte. Validator PASS; independent fresh-solve verifier PASS."
}
json.dump(changes, io.open("changes_maths-eduqas_number-L03.json","w",encoding="utf-8"), indent=2, ensure_ascii=False)

diagrams = {
 "key": "maths-eduqas_number-L03",
 "figures_added": [
  {"tier":"opener","index":0,"kind":"svg",
   "what":"Number line 3 to 4 with a marker at 3.7 and the halfway value 3.5 dashed; theme-safe (currentColor strokes/text, soft-fill marker). Makes the 'nearer to which whole' rounding hook concrete, mirroring how a rounding figure would appear."}
 ],
 "opener_touched": True,
 "notes": "Rounding, decimal arithmetic and estimation are textual by exam convention: the bank problems are pure calculation and the real exam prints no figure on them, so no per-problem figures were added (exam-realism test). The single figure is the opener number line, which shows what its text claims (Tom's show-what-you-say rule)."
}
json.dump(diagrams, io.open("changes_maths-eduqas_number-L03_diagrams.json","w",encoding="utf-8"), indent=2, ensure_ascii=False)
print("wrote changes + diagrams changes")
