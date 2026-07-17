# -*- coding: utf-8 -*-
import json, io
DIV="÷"
changes={
 "key":"probability-statistics-L04",
 "board":"maths-ocr",
 "lesson_id":"6e383a58-7e5b-4917-a28d-2881938a3def",
 "problems_fixed":[
   {"tier":"silver","index":2,"what":"stored solution 15 did not match the displayed grouped data (midpoints 5,15,25 with freq 8,12,10 give 470/30 = 15.67, a messy non-calculator answer); message was garbled ('Hmm: ...'). Changed frequencies to 8,14,8 so the estimated mean is exactly 15.","old":"freq 8,12,10 -> stored 15 (actually 15.67)","new":"freq 8,14,8 -> mean 450/30 = 15"},
   {"tier":"gold","index":0,"what":"stored solution 15.83 matched nothing (classes 0-10,10-20,20-30 with freq 5,15,10 give 500/30 = 16.67); message garbled ('Let me recalculate...'). Changed frequencies to 6,15,9 so the estimated mean is exactly 16.","old":"freq 5,15,10 -> stored 15.83 (actually 16.67)","new":"freq 6,15,9 -> mean 480/30 = 16"},
 ],
 "issues_resolved":2,
 "opener_concept":"Three friends pool birthday money (£2, £3, £7) and share it equally: the fair share IS the mean (12 "+DIV+" 3 = 4), and biggest minus smallest IS the range (7 − 2 = 5). Names both an average and a spread by common sense before any formula.",
 "notes":"Full guided conversion from a bare practice bank: added guided.opener, guided.teach (bronze/silver/gold), tier_guides, tier descriptions, per-problem hint + guided_steps with completion boundaries, and honest-diagnosis misconceptions with derived expects (each error committed by hand). Trimmed method_card to slim reference. Every box and every solution independently fresh-solved (_verify_psL04_ocr.py) and validator PASS. worked_examples, related_videos, topic_links preserved verbatim from the live pre-dump. S3 (median class) kept as multiple_choice, no guided_steps."
}
json.dump(changes, io.open("changes_maths-ocr_probability-statistics-L04.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)

diag={
 "key":"probability-statistics-L04",
 "board":"maths-ocr",
 "figures_added":[
   {"tier":"silver","index":0,"kind":"svg","what":"Discrete frequency table (Value 1-4 / Frequency 4,6,5,5) as a theme-safe SVG grid, replacing cramped inline '1(f=4)...' text."},
   {"tier":"silver","index":2,"kind":"svg","what":"Grouped midpoint/frequency table (Midpoint 5,15,25 / Frequency 8,14,8)."},
   {"tier":"silver","index":3,"kind":"svg","what":"Grouped frequency table (Class 0-10..30-40 / Frequency 3,7,10,5) for the median-class question."},
   {"tier":"silver","index":6,"kind":"svg","what":"Discrete frequency table (Value 0-4 / Frequency 2,5,8,3,2) for the median-from-table question."},
   {"tier":"gold","index":0,"kind":"svg","what":"Grouped frequency table (Class 0-10,10-20,20-30 / Frequency 6,15,9) for the estimated-mean question."},
   {"tier":"teach.silver","index":None,"kind":"svg","what":"Frequency table (Value 2,3,4 / Frequency 3,4,3) in the silver teach-walk display."},
   {"tier":"teach.gold","index":None,"kind":"svg","what":"Grouped table (Class 0-10,10-20,20-30 / Frequency 6,8,6) in the gold teach-walk display."},
 ],
 "opener_touched":True,
 "notes":"Averages & spread rarely prints geometric figures; the exam figure here is the frequency/grouped table itself, so those were rendered as self-contained SVG grids (viewBox + role=img + aria-label, text and strokes in currentColor, soft header fill at 0.15 opacity, Inter labels, <=286px wide). No box plots/number lines added on the IQR and outlier problems because printing quartiles would give away the answer. Every SVG's cells were generated from the same source numbers as the problem text and solutions."
}
json.dump(diag, io.open("changes_maths-ocr_probability-statistics-L04_diagrams.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("changes files written")
