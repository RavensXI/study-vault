import json,io
main={
 "key":"algebra-L03","board":"maths-aqa","lesson_id":"55a5af04-f88a-4be7-b4c0-7f89c607e266",
 "problems_fixed":[],
 "issues_resolved":0,
 "bank_verified":"Fresh-solved all 20 problems (8 bronze, 7 silver, 5 gold) from display text with sympy. Every option[0] is the correct fully-factorised form; no wrong stored solutions, no degenerate/non-calculator/duplicate issues. The equal-value distractors (e.g. 2(4x-6) for 8x-12, 3(x^2-4) for 3x^2-12) are legitimate 'factorise fully' completeness traps, kept and now diagnosed by expects. All MC, so multiple_choice retained.",
 "added":"hint on all 20 problems; reshaped every misconception to {pattern, expect=original option index, message, note} (2-3 real distractor diagnoses each, none equal to the correct index 0); bronze/silver/gold _description; tier_guides (all 3, within 115-word budget, worked examples verified by expanding back); guided.opener (equal-rows-of-counters hook with theme-safe inline SVG, currentColor, boxes 7 and 21); guided.teach bronze(6x+15) / silver(x^2+8x+15) / gold(9x^2-16), all >=4 numeric boxes, every box independently recomputed and checked at a test x; slimmed method_card.content to under 140 words.",
 "opener_concept":"3 equal rows of counters, each row 2 blue + 5 gold. One row = 7, three rows = 3x7 = 21 = 3(2+5). Sharing a total into equal rows IS taking out a common factor: swap counts for x and 6x+15 = 3(2x+5).",
 "preserved":"related_videos, topic_links, worked_examples byte-identical to live pre-edit fetch; method_card.title/example unchanged; every problem display/options/solutions unchanged.",
 "notes":"guided_steps omitted on bank problems, sanctioned by SPEC for multiple_choice (answers are factorised expressions, not numbers). One preserved style fix: em dash in method_card.steps[0] ('first — always') changed to a colon to satisfy the no-em-dash law. Validator PASS; PATCH 204; round-trip confirmed. No figures on the textual bank (exam-realism test); the only figure is the opener SVG."
}
json.dump(main,io.open("changes_maths-aqa_algebra-L03.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)

diag={
 "key":"algebra-L03","board":"maths-aqa",
 "figures_added":[{"tier":"opener","index":0,"kind":"svg","what":"Three equal rows of counters (each row 2 blue + 5 gold), theme-safe currentColor strokes and soft fill-opacity 0.3 fills, viewBox 0 0 170 82, role=img + aria-label. Concretises 6x+15 = 3(2x+5) for the common-factor opener."}],
 "opener_touched":True,
 "notes":"Textual factorising unit: the algebra bank (single-bracket HCF, quadratic trinomials, difference of two squares) prints no figures on a GCSE paper, so no bank SVG/chart added per the exam-realism test. Only the opener carries a figure, matching the 'show what you say' rule. All figure numbers (2, 5, 3) appear in the opener text and match the counts drawn."
}
json.dump(diag,io.open("changes_maths-aqa_algebra-L03_diagrams.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("wrote both changes files")
