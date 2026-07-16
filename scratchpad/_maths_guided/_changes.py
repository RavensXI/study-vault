# -*- coding: utf-8 -*-
import json, io
changes = {
 "key": "number-L03",
 "problems_fixed": [
  {"tier":"bronze","index":2,"what":"Removed degenerate 'drop_zero' misconception (filed issue): its check equals_8 fired on the correct answer 8.0=8, undiagnosable. Kept round_up (expect 8.1).","old":"drop_zero check=equals_8 expect=null + round_up","new":"round_up expect 8.1 only"},
  {"tier":"silver","index":4,"what":"Merged duplicate misconceptions (filed issue): 'decimal_places' and 'wrong_count' both produced 7.2 for 2.4x0.3. Kept one.","old":"decimal_places(7.2) + wrong_count(7.2)","new":"decimal_places expect 7.2"},
  {"tier":"silver","index":3,"what":"Repaired dead expect on 'divide_wrong' (198/0.48): expect 0.5 is not a derivable final answer. Set expect 100 (multiply-by-0.5 slip) and added round_wrong expect 500.","old":"divide_wrong expect 0.5","new":"divide_wrong expect 100 + round_wrong expect 500"},
  {"tier":"gold","index":1,"what":"Merged duplicate misconceptions on 0.07x0.004: both 'wrong_places' and 'too_few_zeros' expected 0.0028, which is inside the player's 0.01 correct-tolerance so could never fire. Replaced with one 'too_few_places' expect 0.028 (distinct, derivable).","old":"wrong_places(0.0028) + too_few_zeros(0.0028)","new":"too_few_places expect 0.028"},
 ],
 "issues_resolved": 2,
 "opener_concept": "Rough shopping bill: round three shop prices (£3.89, £2.10, £6.95) to the nearest pound and add in your head to estimate the total, then round one price to the nearest 10p. This is exactly rounding + estimating, which the reveal names as the whole topic (nearest 10p = 1 decimal place).",
 "notes": "All 20 bank solutions fresh-solved and confirmed correct; no problem numbers changed. Added tier_guides, tier_descriptions, guided.opener, guided.teach (bronze/silver/gold), and per-problem guided_steps + refreshed hints. Slimmed method_card to <=140 words. Every guided box and check box recomputed independently and lands on the stored solution. Beyond the 2 filed audit issues, repaired 2 further honest-diagnosis defects (silver[3] dead expect, gold[1] tolerance-swallowed duplicate) and rewrote all misconceptions with concrete derivable expects, each >=0.02 from the correct answer to clear both validator (0.011) and player (0.01) thresholds. De-dashed pre-existing em dashes in preserved worked_examples labels (hard style rule); related_videos and topic_links preserved unchanged."
}
json.dump(changes, io.open("changes_number-L03.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("written changes_number-L03.json")
