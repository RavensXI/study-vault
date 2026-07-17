# -*- coding: utf-8 -*-
import json, io, shutil
SRC = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_guided/lesson_maths-ocr_probability-statistics-L02.json"
DST = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-ocr_probability-statistics-L02.json"
shutil.copyfile(SRC, DST)

changes = {
 "key": "probability-statistics-L02",
 "board": "maths-ocr",
 "lesson_id": "1a8441e6-115c-473e-a9b7-a2276e5b7faa",
 "problems_fixed": [
  {"tier":"gold","index":1,"what":"Duplicate solution within tier: gold[0] and gold[1] both answered 0.3. Re-posed gold[1] with a distinct clean answer.","old":"P(A)=0.4, P(B|A)=0.75 -> 0.3","new":"P(A)=0.4, P(B|A)=0.6 -> 0.24"},
  {"tier":"all","index":"*","what":"Rewrote all 20 misconceptions from legacy {check,message,pattern} shape to honest-diagnosis {pattern,message,expect,note}. Each expect derived by committing the specific error so the message fires only on that exact wrong answer.","old":"check field, no expect","new":"derived expect per problem"}
 ],
 "issues_resolved": 2,
 "opener_concept": "12 pupils in chess and art clubs shown as a Venn; the student reads the chess loop and finds 3 of 6 chess players also do art, discovering conditional probability P(art|chess)=1/2 by looking only inside the given group.",
 "notes": "Fresh-solved all 20 problems from display; arithmetic all correct as stored (only the gold duplicate needed a numeric change). Added guided_steps to every problem (completion boundary at phase:substitute, >=2 live boxes), per-problem hints, tier_guides (bronze/silver/gold), guided opener + three teach walks, trimmed method_card to 4 steps. Preserved worked_examples, topic_links, related_videos byte-for-byte. Validator PASS; independent re-check clean (figure region sums, box landings, expects != solutions, no tier duplicates)."
}
json.dump(changes, io.open("C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/changes_maths-ocr_probability-statistics-L02.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)

diagrams = {
 "key": "probability-statistics-L02",
 "board": "maths-ocr",
 "figures_added": [
  {"tier":"bronze","index":0,"kind":"svg","what":"Venn football/rugby, all four regions filled (20,15,13,12/60)"},
  {"tier":"bronze","index":1,"kind":"svg","what":"Venn football/rugby, neither marked ? (asked)"},
  {"tier":"bronze","index":2,"kind":"svg","what":"Venn football/rugby, only-football marked ? (asked)"},
  {"tier":"bronze","index":3,"kind":"svg","what":"Venn sport/music, neither marked ? (asked)"},
  {"tier":"bronze","index":4,"kind":"svg","what":"Probability Venn A/B (0.45,0.15,0.15,0.25)"},
  {"tier":"bronze","index":5,"kind":"svg","what":"Venn cats/dogs, cats-only marked ? (asked)"},
  {"tier":"bronze","index":6,"kind":"svg","what":"Venn French/German, only-German marked ? (asked)"},
  {"tier":"silver","index":0,"kind":"svg","what":"Venn sport/music 100 (40,20,25,15)"},
  {"tier":"silver","index":1,"kind":"svg","what":"Probability Venn A/B (0.4,0.3,0.2,0.1)"},
  {"tier":"silver","index":2,"kind":"svg","what":"Venn tea/coffee 80 (35,15,20,10)"},
  {"tier":"silver","index":4,"kind":"svg","what":"Two disjoint circles: mutually exclusive A(0.3), B(0.4)"},
  {"tier":"silver","index":6,"kind":"svg","what":"Venn bus/walk 120 (50,20,35,15)"},
  {"tier":"gold","index":2,"kind":"svg","what":"Venn maths/physics 200 (50,50,30,70)"},
  {"tier":"gold","index":4,"kind":"svg","what":"Probability Venn A/B, B-only marked ? (P(B) asked)"},
  {"tier":"opener","index":0,"kind":"svg","what":"Venn chess/art 12 pupils (3,3,4,2)"},
  {"tier":"teach.bronze","index":0,"kind":"svg","what":"Venn guitar/piano, neither ?"},
  {"tier":"teach.silver","index":0,"kind":"svg","what":"Venn burger/salad 50 (18,12,8,12)"},
  {"tier":"teach.gold","index":0,"kind":"svg","what":"Probability Venn independent A/B (0.3,0.3,0.2,0.2)"}
 ],
 "opener_touched": True,
 "notes": "All SVGs theme-safe (currentColor strokes/text, soft fill-opacity 0.15), role=img + aria-label + viewBox, self-contained. Every visible number follows from the problem text; unknown asked region marked ?. Skipped figures on pure-formula problems (P(A|B) multiply rules, addition-rule where the overlap is the unknown, the independence test) where a Venn would either give the answer away or is not determinable. Figures built programmatically and re-checked: region sums equal the stated total."
}
json.dump(diagrams, io.open("C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/changes_maths-ocr_probability-statistics-L02_diagrams.json","w",encoding="utf-8"), indent=1, ensure_ascii=False)
print("changes + diagrams + shard copy written")
