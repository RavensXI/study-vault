# -*- coding: utf-8 -*-
import json, io
KEY="maths-aqa_probability-statistics-L04"
changes={
 "key":KEY,
 "problems_fixed":[
  {"tier":"bronze","index":2,"what":"Duplicate solution within tier (b1, b2, b5 all = 5). Re-posed the mode problem so its answer is distinct.","old":"Find the mode of 2, 5, 3, 5, 8, 5, 1. -> 5","new":"Find the mode of 7, 2, 8, 2, 5, 2, 9. -> 2"},
  {"tier":"bronze","index":5,"what":"Duplicate solution within tier (median = 5, same as b1). Re-posed the even-count median problem so its answer is distinct.","old":"Find the median of 6, 2, 9, 4, 7, 1. -> 5","new":"Find the median of 10, 4, 15, 7, 9, 3. -> 8"}
 ],
 "misconceptions_reworked":"All 20 misconceptions rewritten to honest-diagnosis shape with derivable 'expect' values (13 numeric, distinct from the correct answer; multiple_choice and the indeterminate missing-frequency error set expect:null so they never mis-fire). Every expect committed by simulating the actual student error.",
 "issues_resolved":2,
 "opener_concept":"Three friends pool 4+6+8 pounds and share equally; the shared-out figure IS the mean. Common-sense sharing before any formula, with an inline SVG bar figure.",
 "notes":"All 15 stored numeric solutions fresh-solved and CONFIRMED correct on display; only the two duplicate answers were repaired. Added guided.opener, guided.teach (bronze/silver/gold), tier_guides, tier descriptions, per-problem hints, and full guided_steps with a phase:'substitute' completion boundary on all 17 non-MC problems (3 MC problems keep their feedback but omit walks). method_card slimmed to <=140 words / 4 steps. related_videos, topic_links, worked_examples preserved byte-for-byte. Validator PASS; independent re-solve/box/expect/arithmetic verify clean."
}
json.dump(changes, io.open("changes_maths-aqa_probability-statistics-L04.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)

diagrams={
 "key":KEY,
 "figures_added":[
  {"tier":"silver","index":0,"kind":"svg","what":"Frequency table (Score/Frequency: 1->3, 2->5, 3->8, 4->4) rendered as an exam-style SVG table."},
  {"tier":"silver","index":1,"kind":"svg","what":"Grouped frequency table (0-10->4, 10-20->10, 20-30->6) as SVG table."},
  {"tier":"silver","index":3,"kind":"svg","what":"Grouped table (0-20->5, 20-40->15, 40-60->10) for the modal-class question."},
  {"tier":"silver","index":4,"kind":"svg","what":"Grouped table (0-10->6, 10-20->12, 20-30->8, 30-40->4) for the median-class question."},
  {"tier":"silver","index":5,"kind":"svg","what":"Frequency table (Score/Frequency: 3->2, 4->5, 5->8, 6->3, 7->2) for the median-from-table question."},
  {"tier":"gold","index":0,"kind":"svg","what":"Grouped table (0-10->3, 10-20->7, 20-30->12, 30-40->8) for estimated mean."},
  {"tier":"gold","index":4,"kind":"svg","what":"Grouped table (100-120->5, 120-140->10, 140-160->k, 160-180->5) with the unknown frequency shown as k."}
 ],
 "opener_touched":True,
 "notes":"Opener carries an inline SVG bar figure of the three pooled money amounts (Sam 4, Kim 6, Jo 8). All SVGs generated programmatically from each problem's own numbers: viewBox + role='img' + aria-label, currentColor strokes/text, soft header fill at low opacity (theme-safe), no external refs, each well under budget. The redundant inline '0-10(f=3)...' text was replaced by the table figure plus a concise instruction; every figure number matches the problem's data and guided steps. Chart.js not used: this lesson's exam representation is the printed table, not an x-y graph."
}
json.dump(diagrams, io.open("changes_maths-aqa_probability-statistics-L04_diagrams.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote both changes files")
