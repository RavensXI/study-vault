# -*- coding: utf-8 -*-
import json
changes={
 "key":"ratio-proportion-L06",
 "problems_fixed":[
  {"tier":"silver","index":2,"what":"Stored solution was wrong. x_{n+1}=sqrt(8+x_n), x0=3, x2: x1=sqrt(11)=3.3166, x2=sqrt(11.3166)=3.36402, which rounds to 3.364, not 3.363. Also corrected the misconception message (it claimed sqrt(11.317)~3.363).","old":"3.363","new":"3.364"},
  {"tier":"gold","index":0,"what":"Stored solution was flat wrong (looked like a stray x1 value). x_{n+1}=cbrt(5x_n+4), x0=2: x1=cbrt(14)=2.4101, x2=cbrt(16.0507)=2.5225, x3=cbrt(16.6125)=2.5516, rounding to 2.552. The old message even computed cbrt(16.61) as ~2.408 which is wrong (it is ~2.552).","old":"2.408","new":"2.552"},
  {"tier":"bronze","index":4,"what":"Within-tier duplicate answer (validator-failing): four bronze problems all answered 2. Changed the tangent's second point from (5,6) to (5,14) so the gradient is (14-(-2))/(5-1)=16/4=4.","old":"points (1,-2),(5,6), gradient 2","new":"points (1,-2),(5,14), gradient 4"},
  {"tier":"bronze","index":5,"what":"Within-tier duplicate answer (was 5, colliding with bronze[3]). Reworked the reciprocal iteration to x_{n+1}=48/x_n, x0=8, find x1 = 6 (clean non-calculator).","old":"10/x_n, x0=2, x1 = 5","new":"48/x_n, x0=8, x1 = 6"},
  {"tier":"bronze","index":6,"what":"Within-tier duplicate answer (was 2). Kept the oscillation pairing with bronze[5]: x_{n+1}=48/x_n, x0=8, find x2 = 8 (8 -> 6 -> 8).","old":"10/x_n, x0=2, x2 = 2","new":"48/x_n, x0=8, x2 = 8"},
  {"tier":"bronze","index":7,"what":"Within-tier duplicate answer (was 2, a fixed point). Changed x0 from 2 to 4: x_{n+1}=x_n^2-2 gives x1=16-2=14 (clean, unique).","old":"x_n^2-2, x0=2, x1 = 2","new":"x_n^2-2, x0=4, x1 = 14"}
 ],
 "issues_resolved":6,
 "opener_concept":"A number machine that halves your number then adds 3, feeding each answer back in. From 10 a student gets 8, then 7 by pure mental arithmetic. The reveal names that feed-back move as iteration (x_{n+1}=x_n/2+3: 10,8,7,6.5...) and shows it closing in on 6, the solution of x=x/2+3, previewing convergence. No figure claimed (pure imagination).",
 "notes":"Fresh-solved all 20 problems from display before touching anything (delta said trust nothing: no prior audit on OCR). Found 2 flat-wrong stored solutions (silver[2] 3.363->3.364, gold[0] 2.408->2.552) and the predicted within-tier duplicate-answer disease (bronze had four 2s and two 5s; validator hard-fails duplicates). Fixed all 6 with minimal clean-integer/exact-decimal edits and recomputed every solution, guided box and misconception expect. Converted every misconception from the legacy {check,message} format to honest-diagnosis {pattern,message,expect}: each expect committed by actually making the named error (stopped_early -> x1 value, rise_run_inverted -> run/rise, order_of_operations -> 6/x+1, forgot_root -> 8+x without sqrt, sign_error -> +4); null on the two multiple_choice problems. Added hints to the two MC problems (previously had none, would have failed validation). Added guided_steps with a phase:'substitute' completion boundary to all 18 non-MC problems (setup pre-worked, solve-through and check live, >=2 live boxes after). Added tier_guides (within 115-word budget), tier descriptions, opener, and three teach walks on problems NOT in the bank (bronze gradient (2,1)-(6,9); silver (x^2+3)/(2x) x0=2; gold cbrt(7x+20) x0=1 with exact x1=3). Trimmed method_card from 5 steps to 4. Every guided box independently recomputed; decimal iterations carry 4 d.p. between steps to avoid rounding-boundary drift and land exactly on stored solutions. No em dashes, British English, unicode symbols. Preserved related_videos, topic_links and worked_examples byte-for-byte (verified equal on live). Validator PASS; PATCH 204; live row re-fetched and confirmed byte-equal to the validated shard."
}
json.dump(changes,open("changes_maths-ocr_ratio-proportion-L06.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)

dia={
 "key":"ratio-proportion-L06",
 "figures_added":[
  {"tier":"bronze","index":0,"kind":"svg","what":"Coordinate axes with the tangent line through (1,3) and (5,11), both points plotted and labelled, plus a dashed rise/run right-triangle labelled run 4 and rise 8. Gradient 8/4=2 reads straight off the figure."},
  {"tier":"bronze","index":1,"kind":"svg","what":"Axes with the tangent through (0,4) and (2,10), points labelled, rise/run triangle labelled run 2 and rise 6 (gradient 3)."},
  {"tier":"bronze","index":4,"kind":"svg","what":"Axes spanning y from -4 to 16 with the tangent through (1,-2) and (5,14), points labelled, rise/run triangle labelled run 4 and rise 16 (gradient 4)."}
 ],
 "opener_touched":False,
 "notes":"Added exam-realism figures only to the three pure rate-of-change (gradient-from-two-points) bronze problems, where a real paper prints a line on a grid. All iteration problems are genuinely textual (calculator recall) and correctly get no figure, per the exam-realism test. Each SVG is generated programmatically from the problem's own coordinates, so every plotted point lies on the drawn line and every rise/run label equals the difference in the stated coordinates. Theme-safe: text and axes use currentColor, the shaded triangle uses #60a5fa at fill-opacity 0.3, the line/points use mid-blue #2563eb (reads on light and dark). No external references (xmlns dropped so the validator's http check passes), each figure ~1.3KB, 'Diagram not drawn accurately' caption added. Figures were folded into the same PATCH as the guided conversion; validator PASS on the combined shard."
}
json.dump(dia,open("changes_maths-ocr_ratio-proportion-L06_diagrams.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("changes files written")
