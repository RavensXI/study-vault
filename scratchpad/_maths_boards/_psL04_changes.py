import json, io
changes = {
 "key":"probability-statistics-L04",
 "board":"maths-eduqas",
 "problems_fixed":[],
 "issues_resolved":0,
 "opener_concept":"Three friends pool their pocket money (Ben £5, Amy £7, Cal £9), add it, then share it equally 3 ways to get £7. That shared-out figure IS the mean; reveal names pool-then-share as mean = total / how many.",
 "notes":"No audit existed for this board; fresh-solved all 20 problems (8 bronze / 7 silver / 5 gold) from display. ALL stored solutions were already correct (B6 median 6.5, S1 3.55, S2 16.7, S5 median class 10-20, G1 31.7, G5 k=10 all reconfirmed), so zero answer/pose repairs were needed. Full guided-learning build added: guided.opener (money-share), guided.teach bronze/silver/gold (all-fresh numbers, mean+median / freq-table / grouped estimate), tier_guides with worked examples, tier descriptions, per-problem hints, and guided_steps with a phase:substitute completion boundary on every non-MC problem. Misconceptions rebuilt with honest derivable expects (original bank had mislabelled patterns e.g. a mean problem tagged 'median' and non-firing 'check' strings, all with NO expect): every expect committed by simulating the error (gave_total, no_order, found_median 62.5, ignored_frequency, used_upper_bounds, used_new_mean, forgot_to_subtract, range_unchanged/gave_mean, mean_unchanged, position_as_value 15); the three MC problems (modal class, median class, median-becomes-7) use expect:null. Preserved method_card, topic_links, worked_examples, related_videos byte-for-byte vs pre-dump."
}
json.dump(changes, io.open("changes_maths-eduqas_probability-statistics-L04.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)

figs = {
 "key":"probability-statistics-L04",
 "board":"maths-eduqas",
 "figures_added":[
   {"tier":"opener","index":1,"kind":"svg","what":"Bar chart of three pocket-money amounts (Ben £5, Amy £7, Cal £9) with a baseline, heights scaled 8px/£, so 'pool then share' is visual."},
   {"tier":"silver","index":0,"kind":"svg","what":"Frequency table (Score/Frequency) 2:3, 3:7, 4:6, 5:4 for the mean."},
   {"tier":"silver","index":1,"kind":"svg","what":"Grouped frequency table (Class/Frequency) 0-10:5, 10-20:15, 20-30:10 for the estimated mean."},
   {"tier":"silver","index":3,"kind":"svg","what":"Grouped frequency table 0-20:8, 20-40:12, 40-60:10 for the modal class."},
   {"tier":"silver","index":4,"kind":"svg","what":"Grouped frequency table 0-10:8, 10-20:15, 20-30:12, 30-40:5 for the median class."},
   {"tier":"silver","index":5,"kind":"svg","what":"Frequency table 1:4, 2:6, 3:10, 4:5, 5:5 for the median."},
   {"tier":"gold","index":0,"kind":"svg","what":"Grouped frequency table 10-20:4, 20-30:8, 30-40:12, 40-50:6 for the estimated mean."},
   {"tier":"gold","index":4,"kind":"svg","what":"Grouped frequency table 0-20:5, 20-40:10, 40-60:k, 60-80:5 (k shown literally) for the missing-frequency solve."}
 ],
 "opener_touched":True,
 "notes":"8 theme-safe inline SVGs (currentColor strokes/text, soft #60a5fa header shade / #34d399 bars at 0.15-0.35 opacity), generated programmatically from each problem's own numbers; viewBox height = 22*(rows+1)+2 verified per table; labels cross-checked against problem data and solutions. Figures added exactly where an exam would print a table/chart; the three reverse-mean / range / shift word problems and the small-list median-becomes-7 MC stay textual (no figure needed). No question text, solutions, guided steps, hints or misconceptions changed by the diagram pass."
}
json.dump(figs, io.open("changes_maths-eduqas_probability-statistics-L04_diagrams.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("changes files written")
