# -*- coding: utf-8 -*-
import io, json

changes = {
  "key": "probability-statistics-L05",
  "board": "maths-aqa",
  "problems_fixed": [
    {"tier":"bronze","index":3,"what":"Q1 read from CF curve (60 patients). CF=15 lies between points (5,8) and (10,20), reading x approx 7.9, not 10. Corrected to the graph-faithful value.","old":[10],"new":[8]},
    {"tier":"bronze","index":5,"what":"Frequency = FD x width duplicated bronze IQR answer 20 (tier duplicate). Retuned FD 4 width 5 to FD 5 width 5 for a unique clean answer.","old":[20],"new":[25]},
  ],
  "issues_resolved": 2,
  "structural_changes": [
    "Silver tier reordered so the first problem is single_value (old S1, CF gap-count) rather than a multiple_choice, so the player's completion-problem mechanic works for silver. Solution multiset unchanged.",
    "Converted all 20 misconceptions from legacy {check,message,pattern} to guided {pattern,message,expect} with numeric expects derived by committing each error (MC expects = tempting wrong option index).",
    "Added guided_steps (with phase:'substitute' completion boundary) to all 15 single_value problems; multiple_choice problems left without walks per spec.",
    "Added per-problem hints, tier descriptions, tier_guides (bronze/silver/gold), and guided.opener + guided.teach walks.",
  ],
  "opener_concept": "A cafe counts new customers each hour (5, then 8, then 6). The student keeps a running total (13, then 19) by common sense, then the reveal names that running total as cumulative frequency and links n/2, n/4, 3n/4 to median and quartiles.",
  "preserved": ["related_videos","topic_links","worked_examples","method_card"],
  "notes": "Fresh-solved all 20 problems from display. Only bronze[3] was mathematically wrong (10 -> 8); bronze[5] was a tier-duplicate cleaned to 25. All other stored solutions verified correct. Every guided box recomputed and lands on its solution; every expect reproduces its error and differs from the answer. Validator PASS."
}
json.dump(changes, io.open("changes_maths-aqa_probability-statistics-L05.json","w",encoding="utf-8"),
          indent=1, ensure_ascii=False)

diagrams = {
  "key": "probability-statistics-L05",
  "board": "maths-aqa",
  "figures_added": [
    {"tier":"gold","index":2,"kind":"chart","what":"Histogram (frequency density bars 0-10:3, 10-25:4, 25-30:6, 30-50:2) for the modal-class question, matching the FD values in the text."},
    {"tier":"gold","index":3,"kind":"chart","what":"Histogram (0-20:2, 20-30:5, 30-50:3) for the median-class question, matching the FD values in the text."},
    {"tier":"silver","index":4,"kind":"chart","what":"Histogram (0-5:2, 5-10:6, 10-20:3, 20-40:1) for the total-frequency question, matching the FD values in the text."},
  ],
  "opener_touched": False,
  "notes": "Lesson was already chart-rich (CF curves, box plots, histograms via Chart.js). Added Chart.js bar histograms to the three histogram word-problems that lacked a figure, using the lesson's existing category-label convention (class range as label, FD as bar height). Skipped silver[5] compare-box-plots (only median+IQR given, not a full 5-number summary, so any drawn box plot would fabricate quartiles) and the single-bar/pure-summary definition drills (b5/b6/b7/s3/s6), which state their values directly. Every figure number cross-checked against its problem text."
}
json.dump(diagrams, io.open("changes_maths-aqa_probability-statistics-L05_diagrams.json","w",encoding="utf-8"),
          indent=1, ensure_ascii=False)
print("changes files written")
