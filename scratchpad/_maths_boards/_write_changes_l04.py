import json,io
changes={
 "key":"maths-ocr_number-L04",
 "problems_fixed":[
   {"tier":"silver","index":4,"what":"Duplicate solution: three silver problems all had HCF = 12 (indices 0, 4, 6). Changed this one to keep answers distinct within the tier.",
    "old":"Find the HCF of 36 and 84 (solution 12)","new":"Find the HCF of 36 and 90 (solution 18)"},
   {"tier":"silver","index":6,"what":"Duplicate solution: same 3-way collision on 12. Re-posed as a three-number HCF with a distinct clean answer.",
    "old":"Find the HCF of 24, 36 and 48 (solution 12)","new":"Find the HCF of 24, 40 and 56 (solution 8)"}
 ],
 "issues_resolved":2,
 "opener_concept":"12 cupcakes shared into equal rows (an SVG array): rows of 3 give 4 rows, rows of 4 give 3 rows, rows of 5 leave a remainder. The divisors that leave none are its factors; a number like 7 has only two arrangements, so it is prime.",
 "notes":"Fresh-solved all 20 problems (8 bronze / 7 silver / 5 gold); every stored solution matched except the two silver duplicate collisions above (three problems shared HCF=12). All are non-calculator with integer answers, so no messy-decimal repairs needed. Added the full guided stack: tier descriptions, one-sentence hints per problem, guided_steps walks (each substitute box lands on the solution, each ends with an independent check step), tier_guides, guided.opener, and one teach walk per tier (HCF 6&8; LCM 10&15; reverse HCF/LCM 8,96,32). Rewrote every misconception into the {pattern,message,expect} shape with expects derived by committing the error (none equal the correct answer). Trimmed method_card content to 82 words. Replaced em dashes in the preserved worked_examples labels (validator-enforced). related_videos, topic_links, worked_examples otherwise preserved."
}
json.dump(changes,io.open("changes_maths-ocr_number-L04.json","w",encoding="utf-8"),indent=1,ensure_ascii=False)

diag={
 "key":"maths-ocr_number-L04",
 "figures_added":[
   {"tier":"opener","index":0,"kind":"svg","what":"12-cupcake array (4 rows of 3), currentColor strokes, soft amber fills at 0.3 opacity, role=img + aria-label. Makes factors-as-equal-rows concrete before any rule, matching the show-what-you-say rule."}
 ],
 "opener_touched":True,
 "notes":"Factors/Multiples/Primes is a textual number topic: OCR prints these HCF/LCM/prime-factorisation and worded-LCM questions as plain text (students draw their own factor trees/Venns), so by the exam-realism test the bank problems warrant no printed figure, and a completed prime Venn would hand over the HCF/LCM answer. The one genuine, non-trivialising figure is the opener array, which mirrors how equal-row arrangements motivate factors. All SVG is theme-safe and self-contained; no chart configs needed (no x-y graph problems in this lesson)."
}
json.dump(diag,io.open("changes_maths-ocr_number-L04_diagrams.json","w",encoding="utf-8"),indent=1,ensure_ascii=False)
print("wrote changes files")
