import json, io
main={
 "key":"maths-ocr_algebra-L12",
 "board":"maths-ocr",
 "lesson_id":"971cfba0-badb-4c6b-b0f8-e9d33d450b8c",
 "problems_fixed":[
  {"tier":"gold","index":2,"what":"Reworded confusing display 'Solve x^2-2x and x+4 simultaneously where x^2-2x > x+4' to 'Find the set of values of x for which x^2 - 2x > x + 4'. Same maths, same answer (x<-1 or x>4); the old phrasing implied a simultaneous-equations task.","old":"Solve \(x^2 - 2x\) and \(x + 4\) simultaneously where \(x^2 - 2x > x + 4\). What is the range?","new":"Find the set of values of \(x\) for which \(x^2 - 2x > x + 4\). What is the range?"},
  {"tier":"bronze","index":4,"what":"Normalised plain-text unicode minus in display to LaTeX for consistent rendering; no maths change.","old":"How many integers from −10 to 10","new":"How many integers from \(-10\) to \(10\)"},
  {"tier":"worked_examples","index":"all","what":"Replaced em dashes in step labels ('Step 1 — Factorise') with colons to satisfy the no-em-dash style rule and validator. Content unchanged.","old":"Step 1 — Factorise","new":"Step 1: Factorise"}
 ],
 "issues_resolved":0,
 "opener_concept":"A number machine multiplies (x-2)(x-6). Testing x=7 (both brackets positive, product +5) then x=4 (one positive 2, one negative -2, product -4) shows a positive times a negative is negative, so the expression drops below zero only BETWEEN the roots 2 and 6. The reveal names 'between the roots' as the whole quadratic-inequality method.",
 "notes":"NO prior audit for OCR; trusted nothing. Fresh-solved all 20 problems (8 bronze, 7 silver, 5 gold) from their displays: every stored solution was already correct (multiple_choice correct answer at option index 0 in all 15 MC items; all 6 single_value counts/roots correct: B5=10, B7=6, S3=8, S6=7, S7=1, G4=4). No degenerate/messy non-calculator cases, no duplicate answers within a tier. problems_fixed holds only the two display clarity edits and the em-dash label fix; no solution was wrong. Full guided conversion added: fresh opener ((x-2)(x-6) machine), three teach walks (bronze x^2-8x+15 between/<0, silver x^2+2x-8 outside/>=0, gold 2x^2+x-6 with a!=1 outside/>0) each with its own verified numbers, tier_guides for all three tiers with fresh worked examples (x^2-49, x^2-x-12, 3x^2-5x-2) and tier descriptions, a plain-text hint on every one of the 20 problems, honest-diagnosis misconceptions with derived expects on every problem (MC expect = the wrong OPTION INDEX the error selects, verified in option range and != 0; single_value expect = the numeric wrong answer, verified != solution), and guided_steps with a factorise+roots / count-or-finish completion boundary (phase:substitute) on all 6 single_value problems. method_card slimmed to 4 steps. Preserved byte-for-byte: related_videos (empty), topic_links, worked_examples (bar the em-dash label fix). Validator PASS; live PATCH status 204; readback byte-matches local."
}
diag={
 "key":"maths-ocr_algebra-L12",
 "board":"maths-ocr",
 "lesson_id":"971cfba0-badb-4c6b-b0f8-e9d33d450b8c",
 "figures_added":[
  {"tier":"teach","index":"bronze","kind":"svg","what":"Exam-style sketch of y = x^2 - 8x + 15 (teach walk, not a bank question). U-shape crossing the x-axis at two marked points with the region below the axis BETWEEN the roots shaded, for the < 0 case. Roots (3 and 5) left unlabelled because the walk's boxes ask the student to find them; equation labelled. Sketch, not drawn to scale."},
  {"tier":"teach","index":"silver","kind":"svg","what":"Exam-style sketch of y = x^2 + 2x - 8. U-shape with the two regions ABOVE the axis OUTSIDE the roots shaded, for the >= 0 case (the silver 'outside' move). Roots (-4 and 2) unlabelled (walk finds them); equation labelled. Sketch, not drawn to scale."},
  {"tier":"teach","index":"gold","kind":"svg","what":"Exam-style sketch of y = 2x^2 + x - 6 (a != 1). U-shape with the above-axis regions OUTSIDE the roots shaded, for the > 0 case. Roots (-2 and 1.5) unlabelled because the gold walk derives them by splitting the middle term; equation labelled. Sketch, not drawn to scale."}
 ],
 "opener_touched":False,
 "notes":"Figures added to the three teach walks only, where showing shape + the tier's region move is teaching (not answer-revealing) and roots are kept unlabelled to preserve the walk's boxes. Deliberately NO figure on any bank problem: the multiple_choice 'Solve x^2 ... > 0' items are textual (an exam would not print a sketch, and a labelled parabola would reveal the roots the student must find); a number line on the six single_value integer-count/root problems would show the very integers being counted, giving the answer away (the sibling board shipped such number lines but its own diagram notes argue against them, and honest diagnosis is the house rule). All three SVG theme-safe: currentColor text/axes, soft #60a5fa region fill at fill-opacity 0.3, viewBox + role=img + aria-label, self-contained, each ~2.1-2.4KB. Every visible SVG number cross-checked against its teach quadratic; parabola roots recomputed via the discriminant and matched to the marked points. Validator PASS; figures shipped in the same PATCH; readback byte-matches."
}
json.dump(main, io.open("changes_maths-ocr_algebra-L12.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(diag, io.open("changes_maths-ocr_algebra-L12_diagrams.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote both changes files")
