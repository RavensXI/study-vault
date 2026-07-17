import json
changes={
 "key":"algebra-L05",
 "problems_fixed":[
  {"tier":"bronze","index":4,"what":"duplicate answer (4) within tier; changed RHS for a distinct clean integer","old":"Solve 4x + 1 = 17 (x=4)","new":"Solve 4x + 1 = 33 (x=8)"},
  {"tier":"bronze","index":7,"what":"duplicate answer (5) within tier; changed RHS for a distinct clean integer","old":"Solve 20 - 3x = 5 (x=5)","new":"Solve 20 - 3x = 2 (x=6)"},
  {"tier":"silver","index":2,"what":"triple-duplicate answer (3) within tier; changed RHS","old":"Solve 3(x + 4) = 21 (x=3)","new":"Solve 3(x + 4) = 30 (x=6)"},
  {"tier":"silver","index":3,"what":"triple-duplicate answer (3) within tier; reposed to a bracket problem with distinct answer and clean error-expects","old":"Solve 2(3x - 1) = x + 13 (x=3)","new":"Solve 3(x - 1) = x + 15 (x=9)"}
 ],
 "issues_resolved":4,
 "opener_concept":"Taxi fare: £3 to get in plus £2/mile, total £11. Take off the £3, divide by £2 to get 4 miles. This IS solving 2x+3=11 by inverse operations in reverse order.",
 "notes":"Fresh-solved all 20 problems: every stored solution was mathematically correct. The only bank defects were duplicate solutions within tiers (bronze had 4 and 5 twice; silver had 3 three times), which the validator rejects; fixed with minimal RHS edits yielding distinct clean integers (bronze now 4,5,12,7,8,3,9,6; silver 4,5,6,9,7,11,3; gold 10,7,12,29,5 unchanged). Rewrote all misconceptions: the pre-existing set were expect:null restatements of the correct method; replaced with honest diagnoses whose expect is the exact wrong value each committed error produces (forgot-to-divide, added-instead-of-subtracted constant, sign drop on negative x, forgot to scale RHS/second fraction, dropped denominators, forgot to multiply bracket constant). Added guided_steps to all 20 (completion boundary at phase:'substitute' = the final divide + check), teach walks per tier, tier_guides, tier descriptions, and the opener. Preserved related_videos([]), worked_examples(3), topic_links; sanitised em dashes in preserved worked_examples labels to colons (style law). method_card kept as-is (within budget). No figures: solving linear equations is a textual unit; exam prints no figure."
}
json.dump(changes, open("changes_maths-ocr_algebra-L05.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)

diagrams={
 "key":"algebra-L05",
 "figures_added":[],
 "opener_touched":False,
 "notes":"No figures added. Solving Linear Equations is a purely textual algebra unit; GCSE exam papers print no figure for equation-solving problems (no shape, graph, tree, grid or chart). The opener is a taxi-fare word scenario that claims no diagram (show-what-you-say satisfied by pure scenario text), so no SVG is required. Applied the exam-realism test per SPEC_DIAGRAMS: adding decoration here would be non-authentic."
}
json.dump(diagrams, open("changes_maths-ocr_algebra-L05_diagrams.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote both changes files")
