import json
changes={
 "key":"algebra-L09",
 "board":"maths-aqa",
 "lesson_id":"5ff3e1eb-2284-4096-af06-4bcb6754b0e1",
 "problems_fixed":[
  {"tier":"bronze","index":4,"what":"deduped (was [4,3], collided with bronze[2]); changed second equation x-y=1 -> x-y=4","old":"2x+y=11 and x-y=1 -> [4,3]","new":"2x+y=11 and x-y=4 -> [5,1]"},
  {"tier":"bronze","index":5,"what":"replaced degenerate single_value problem (x=2 given, asked only y) with a proper elimination xy_pair problem","old":"x+2y=8 and x=2, Find y -> [3] single_value","new":"3x+y=17 and x+y=7 -> [5,2] xy_pair"},
  {"tier":"silver","index":2,"what":"re-posed: was a gold-level two-scaling problem (2x+3y=13 & 5x-2y=4) sitting in silver; replaced second equation so a single multiplication matches, keeping answer [2,3]","old":"2x+3y=13 and 5x-2y=4 -> [2,3]","new":"2x+3y=13 and x+4y=14 -> [2,3]"},
  {"tier":"silver","index":4,"what":"deduped (was [3,5], collided with silver[0]); re-posed keeping the multiply-first-then-add structure","old":"4x-y=7 and 2x+3y=21 -> [3,5]","new":"4x-y=17 and 2x+3y=19 -> [5,3]"},
  {"tier":"gold","index":0,"what":"converted single_value (coffee only) to xy_pair by asking for both quantities; assigned x=coffee, y=tea; solutions extended [2.5]->[2.5,2]","old":"...Find the cost of a coffee -> [2.5] single_value","new":"...Taking x as coffee, y as tea, find x and y -> [2.5,2] xy_pair"},
  {"tier":"gold","index":2,"what":"converted two_solutions word problem to xy_pair with explicit x=first number, y=second","old":"sum=15, 2*first-second=6 -> [7,8] two_solutions","new":"same, Taking x as first, y as second -> [7,8] xy_pair"},
  {"tier":"ALL","index":-1,"what":"every remaining problem converted from two_solutions to ordered xy_pair per board delta; stripped 'Find x and y.' suffix; replaced junk placeholder misconceptions (no expect key) with derived, error-simulated expects"}
 ],
 "issues_resolved":7,
 "opener_concept":"Cafe bill: 2 teas + 1 cake = £5, 1 tea + 1 cake = £3; compare orders (elimination) then substitute. Tea £2, cake £1. Maps to 2x+y=5, x+y=3.",
 "figures_added":0,
 "figures_note":"Linear simultaneous equations print no figure in the AQA exam (pure algebra); opener text claims no diagram, so none drawn per exam-realism test.",
 "notes":"Fresh-solved all 17 problems from display. Repairs: 2 within-tier duplicates ([4,3] bronze, [3,5] silver), 1 mis-tiered silver problem re-posed to single-multiplication, 1 degenerate bronze replaced. All input_type now xy_pair. Full guided_steps generated programmatically from each problem's numbers with in-script assertions (kept value, substituted value, and check value all forced to match stored solutions); tier_guides + opener + 3 teach walks added; method_card/worked_examples/topic_links/related_videos preserved. Validator PASS; PATCH 204; readback confirms guided+tier_guides live."
}
json.dump(changes, open("changes_maths-aqa_algebra-L09.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote changes_maths-aqa_algebra-L09.json")
