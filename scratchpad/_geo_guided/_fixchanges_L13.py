# -*- coding: utf-8 -*-
import json, io, os
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'changes_L13.json')
d = json.load(io.open(P, encoding='utf-8'))

d['map_facts_verified'][7] = (
    "CORRECTED 21 Jul after checker challenge. Worsaw Hill (pendle-hill-z16): thick index "
    "contour labelled 200 at approx (1440,168). TWO closed rings are drawn inside it, not one. "
    "Vertical pixel scan at x=1377 returns brown runs at y=23-24 (index, 200 N), y=60-61 "
    "(thin, 210 N), y=165-167 and y=174-176 (the two limbs of a small closed loop, 220), "
    "y=287 (thin, 210 S), y=317 (index, 200 S). The small loop was re-imaged at 16x: it is a "
    "closed ring about 3 px wide and 12 px tall spanning x 1376-1379, y 165-176, in thin-contour "
    "brown (145,118,97) against the thin-contour reference and clearly not an index line "
    "(index runs on this sheet read approx (135,90,55)). So the highest ring drawn is 220 m and "
    "the first undrawn contour is 230 m. Independently consistent with Worsaw Hill's real summit "
    "height of 228 m. The original entry claiming 'exactly one thin ring inside' was WRONG and had "
    "cleared two defective problems (gold[4], bronze[1]); both have been rewritten."
)
d['map_facts_verified'].append(
    "Worsaw Hill north slope re-verified for silver[4]: at x=1250 the only brown runs between "
    "y=0 and y=320 are y=219-222 and y=26-27, i.e. one interval crossed in about 193 px (0.27 km). "
    "On the south at x=1330 the 200 index at y=289-292 is followed by the next line at y=319, "
    "30 px (0.04 km). The southern side is far steeper, as silver[4] states."
)
d['map_facts_verified'].append(
    "silver[6] re-verified: vertical scan at x=1330 south of the summit gives index 200 at "
    "y=289-292, four thin lines at y=319/334/350/362, then the next index at y=374-375, so the "
    "lower thick line is 150 m."
)

d['problems_fixed'] = [
    {"tier": "gold", "index": 4,
     "what": "Display asserted an invented map fact ('the highest ring drawn is the 210 m contour'). The 220 ring is drawn. Display, solution, guided_steps 2/4/5 and all misconception expects rewritten; the walk now makes the student COUNT the rings instead of being handed the count.",
     "old": {"solutions": [220], "gs2.answer": 210, "gs4.answer": 220,
             "expects": [200, 260]},
     "new": {"solutions": [230], "gs2.answer": 2, "gs3.answer": 220, "gs4.answer": 230,
             "expects": [220, 210, 270]}},
    {"tier": "bronze", "index": 1,
     "what": "Display said 'there is one more, smaller ring' (there are two) and guided_steps[2] asked for that count with answer 1, so a student reading the map correctly was marked wrong. Reworded to 'the next ring in from the labelled line' and the ring-counting box removed; stored solution 210 is unchanged and is now true under the wording given.",
     "old": {"gs2": "Type how many closed rings are drawn inside the labelled contour -> 1"},
     "new": {"gs2": "Type the height printed on the labelled contour -> 200"}},
    {"tier": "-", "index": -1,
     "what": "exam_context.paper was 'Paper 3: Geographical Applications', a board-specific name on a board-neutral row propagated to six subjects. Replaced with neutral wording. NOTE: L11 and L12 still carry the board-specific string and need the same sweep.",
     "old": "Paper 3: Geographical Applications",
     "new": "Map and fieldwork skills questions, on whichever paper your board sets them"},
    {"tier": "bronze", "index": 4,
     "what": "guided_steps[1].hint stated the box answer ('if there are no brown lines at all, the answer is zero'). Rewritten to a counting instruction.",
     "old": "Look between those grid lines. If there are no brown lines at all, the answer is zero.",
     "new": "Trace each edge of that square in turn and count every brown line that crosses into it."},
    {"tier": "bronze", "index": 6,
     "what": "guided_steps[3].hint handed over the box answer. Rewritten to a comparison instruction.",
     "old": "Fifty metres of climb inside a few hundred metres of walking is hard work.",
     "new": "Put the climb you have just worked out next to the ground you cover to gain it, and compare the two."},
    {"tier": "silver", "index": 4,
     "what": "guided_steps[3].hint and [4].hint gave both box answers and, because the walk is also the post-wrong-answer lifeline, the multiple-choice answer with them. Both rewritten to measuring instructions.",
     "old": ["On the southern side the lines are almost touching.",
             "There is a wide white gap before the next line appears."],
     "new": ["Put a fingertip on the labelled line and slide it south, then note how far you go before you meet the next brown line.",
             "Slide from the same labelled line northwards instead, and compare that distance with the one you have just measured."]},
    {"tier": "-", "index": -1,
     "what": "tier_guides.gold.example repeated the Gold teach walk's figures (80 m over 0.4 km, 200 m per km, 1 in 5). Reworked to a distinct demonstration.",
     "old": "80 m over 0.4 km -> 200 m per km, 1 in 5",
     "new": "75 m over 0.6 km -> 125 m per km, 1 in 8"},
]

d['checker_findings_rejected'] = [
    {"finding": "silver[3].guided_steps[1].answer stored as 9 while the map prints '09'; a string compare would fail a correct student.",
     "reason": "Not a defect. practice.html line 5571 checks guided boxes with parseFloat((input.value||'').trim()) and Math.abs(v - st.answer) < 0.005. There is no string compare anywhere in the guided-step path, so a student typing 09 parses to 9 and is marked right. The spec also requires guided-step answers to be plain numbers, and 09 is not a valid JSON number. Left as 9. The only residual is cosmetic: after a second wrong attempt the reveal writes String(9) = '9' rather than '09'."}
]

d['note'] = (
    "Brand new lesson. practice_data was {} before this run, so nothing was repaired, everything "
    "was authored. Repaired 21 Jul after an independent checker found an invented map fact on "
    "Worsaw Hill; see problems_fixed and map_facts_verified[7]."
)

with io.open(P, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
print('written', P)
