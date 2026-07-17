import json, io

changes = {
 "key": "maths-ocr_algebra-L09",
 "lesson_id": "ee2766ef-5043-457b-b6b3-4e38d5ed9d0e",
 "title": "Simultaneous Equations (Linear)",
 "problems_fixed": [
  {"tier":"bronze","index":6,"what":"within-tier duplicate answer (3,2) shared with bronze[2]; re-posed to a distinct already-matching problem",
   "old":"Solve 4x+y=14 and 2x+y=8  -> (3,2)","new":"Solve 3x+y=14 and x+y=6  -> (4,2)"},
  {"tier":"silver","index":0,"what":"mis-tiered: coefficients already matched (bronze skill); re-posed to need a single multiplication",
   "old":"Solve 3x+2y=16 and x-2y=0  -> (4,2)","new":"Solve 3x+2y=16 and x+y=6  -> (4,2), multiply eq2 by 2"},
  {"tier":"silver","index":1,"what":"mis-tiered: 3y already matched in both (bronze skill); re-posed to need one multiplication",
   "old":"Solve 2x+3y=18 and 4x+3y=24  -> (3,4)","new":"Solve 2x+3y=18 and x+y=7  -> (3,4), multiply eq2 by 3"},
  {"tier":"silver","index":2,"what":"mis-tiered: needed multiplying BOTH equations (gold skill); re-posed to a single-multiply problem, answer preserved",
   "old":"Solve 3x+2y=11 and 2x+3y=9  -> (3,1)","new":"Solve 3x+2y=11 and x+y=4  -> (3,1), multiply eq2 by 2"},
  {"tier":"silver","index":3,"what":"mis-tiered: opposite 2y already matched (bronze skill); re-posed to need one multiplication",
   "old":"Solve 5x-2y=4 and 3x+2y=12  -> (2,3)","new":"Solve 5x-2y=4 and x+y=5  -> (2,3), multiply eq2 by 2 then add"},
  {"tier":"silver","index":4,"what":"non-integer answer y=3/5 on a non-calculator problem; re-posed to clean integers and a genuine single multiplication",
   "old":"Solve 4x+5y=23 and 3x+5y=18  -> (5, 0.6)","new":"Solve 3x+4y=23 and x+2y=11  -> (1,5), multiply eq2 by 2"},
  {"tier":"gold","index":2,"what":"word problem reframed from single_value (adults only) to xy_pair (adults x, children y) to match the L09 xy_pair contract; numbers preserved",
   "old":"How many adult tickets?  -> 60 (single_value)","new":"How many of each?  -> x=60 adults, y=60 children (xy_pair)"}
 ],
 "structural_conversion": "All problems converted from split single_value ('Enter x' / 'Enter y' as two rows) to a single ordered xy_pair problem, per the algebra-L09 board delta. Bronze 8->7, silver 7->5, gold 5->3 distinct problems (each split pair merged into one xy_pair).",
 "issues_resolved": 7,
 "opener_concept": "Cinema tickets + popcorn: 2 tickets+1 popcorn=£25, 1 ticket+1 popcorn=£16. Comparing the two orders (elimination) gives ticket=£9; then popcorn=£7 (substitution). Names the two moves before any algebra; ties into the gold cinema word problem.",
 "guided_added": "tier_guides (bronze/silver/gold), guided.opener, guided.teach (one walk per tier: 3x+y=12&x+y=6; 2x+3y=13&x+y=5 x3; 4x+3y=18&3x+2y=13 x2/x3), guided_steps on every bank problem with a phase:substitute completion boundary and a final check step. hint added to every problem.",
 "misconceptions": "Every abstract problem given one determinate, error-simulated expect (rhs_not_subtracted / scaled_lhs_only / substitute_sign_slip / add_rhs_wrong). Every expect derived by committing the error in code and verified != solution. Word problem left with none (no single determinate wrong pair).",
 "method_card": "Trimmed to 4 steps + <=140-word content (slim reference); teaching now lives in the walks.",
 "preserved": "topic_links, related_videos, worked_examples all kept from live. worked_examples step labels had pre-existing em dashes (banned, student-facing) replaced with colons ('Step 1 — Add' -> 'Step 1: Add').",
 "notes": "Fresh-solved every problem from its display before conversion. Diseases found and fixed: 1 within-tier duplicate (bronze), 1 non-integer non-calc answer (silver), and a silver tier that taught no silver skill (4 problems re-posed to single-multiply). Validator PASS; PATCH 204 with round-trip equality confirmed."
}
json.dump(changes, io.open("changes_maths-ocr_algebra-L09.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)

diagrams = {
 "key": "maths-ocr_algebra-L09",
 "figures_added": [],
 "opener_touched": False,
 "notes": "No figures added. Textual algebra lesson (solving simultaneous linear equations by elimination/substitution); an OCR exam prints no figure for these items. The one context problem (cinema tickets) is a pure word problem with no printable diagram. Exam-realism test => zero figures is correct for this lesson."
}
json.dump(diagrams, io.open("changes_maths-ocr_algebra-L09_diagrams.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote changes files")
