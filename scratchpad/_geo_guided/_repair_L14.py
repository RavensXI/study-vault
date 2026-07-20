# -*- coding: utf-8 -*-
"""Repair pass on Geography Skills L14 after checker findings."""
import json, io, os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lesson_L14.json')
d = json.load(io.open(P, encoding='utf-8'))
pb = d['problem_bank']
changes = []


def rec(tier, idx, what, old, new):
    changes.append({"tier": tier, "index": idx, "what": what, "old": old, "new": new})


# ---------------------------------------------------------------- gold say-steps
# MC options are Fisher-Yates shuffled at render (practice.html ~4798-4816),
# so a positional pointer ("the first one") is right only 25% of the time.
g = pb['gold']

old = g[0]['guided_steps'][6]['say']
g[0]['guided_steps'][6]['say'] = (
    "The option built on that evidence is the one saying the west is <strong>low, "
    "near the contour labelled 100 m, with widely spaced contours and a main road "
    "along the valley floor</strong>, while the land eastwards climbs steeply.")
rec('gold', 0, 'guided_steps[6].say: positional pointer replaced with option text', old, g[0]['guided_steps'][6]['say'])

old = g[1]['guided_steps'][6]['say']
g[1]['guided_steps'][6]['say'] = (
    "The option resting on that evidence is the one saying the road <strong>keeps to "
    "lower, gently sloping ground where the contours are widely spaced, rather than "
    "climbing the hill ringed by the 200 m contour</strong>.")
rec('gold', 1, 'guided_steps[6].say: positional pointer replaced with option text', old, g[1]['guided_steps'][6]['say'])

old = g[2]['guided_steps'][6]['say']
g[2]['guided_steps'][6]['say'] = (
    "The option listing that evidence is the one naming <strong>level land on the "
    "valley floor with no contour lines, a river alongside for water and a road "
    "running the length of the dale</strong>.")
rec('gold', 2, 'guided_steps[6].say: positional pointer replaced with option text', old, g[2]['guided_steps'][6]['say'])

# gold[3]: two options both open "Square 9893:", so the square number cannot
# identify the answer either. Name the distinguishing evidence instead.
old = g[3]['guided_steps'][6]['say']
g[3]['guided_steps'][6]['say'] = (
    "The evidence that answers the question is the <strong>woodland covering most of "
    "square 9893 together with the straight working tracks running through the "
    "trees</strong>, so choose the option that names that cover and those tracks, not "
    "the one that offers a single small pond.")
rec('gold', 3, 'guided_steps[6].say: positional pointer plus ambiguous square number replaced with the distinguishing evidence', old, g[3]['guided_steps'][6]['say'])

old = g[4]['guided_steps'][7]['say']
g[4]['guided_steps'][7]['say'] = (
    "The choice and reason the map supports is the option picking <strong>7642 for its "
    "road, its named brook and its more widely spaced contours</strong>, not the one "
    "that claims 7642 has no roads at all.")
rec('gold', 4, 'guided_steps[7].say: positional pointer replaced with option text (7642 alone is ambiguous, two options name it)', old, g[4]['guided_steps'][7]['say'])

# --------------------------------------------- square 9074 clipped at the sheet edge
old = pb['bronze'][7]['display']
pb['bronze'][7]['display'] = ("Litton stands in grid square <strong>9074</strong>. How many contour lines "
                              "cross that square on this extract?")
rec('bronze', 7, 'display: scoped the count to the visible extract (northing 75 falls above the top edge)', old, pb['bronze'][7]['display'])

old = pb['bronze'][7]['guided_steps'][3]['pre']
pb['bronze'][7]['guided_steps'][3]['pre'] = ("Now look inside that square. Type how many brown contour lines you can find "
                                             "inside it on this extract.")
rec('bronze', 7, 'guided_steps[3].pre: scoped to the visible extract', old, pb['bronze'][7]['guided_steps'][3]['pre'])

old = g[2]['guided_steps'][2]['pre']
g[2]['guided_steps'][2]['pre'] = "Type the number of contour lines crossing that square on this extract."
rec('gold', 2, 'guided_steps[2].pre: scoped to the visible extract', old, g[2]['guided_steps'][2]['pre'])

old = g[2]['options'][0]
g[2]['options'][0] = ("Level land on the valley floor with no contour lines drawn across it, a river "
                      "alongside for water, and a road running the length of the dale")
rec('gold', 2, 'options[0]: "no contour lines crossing the square" reworded so a clipped square edge cannot make it false', old, g[2]['options'][0])

# ------------------------------------------------ silver[5]: razor-thin west margin
old = pb['silver'][5]['guided_steps'][1]['pre']
pb['silver'][5]['guided_steps'][1]['pre'] = ("Find the label 450 in the south of the map. Type the easting of the numbered "
                                             "vertical line that runs closest to it.")
rec('silver', 5, 'guided_steps[1].pre: "immediately to its west" replaced with "closest to it" (the label straddles the line, so west was ambiguous)', old, pb['silver'][5]['guided_steps'][1]['pre'])

old = pb['silver'][5]['guided_steps'][1]['hint']
pb['silver'][5]['guided_steps'][1]['hint'] = ("One numbered vertical line runs right past that label; read its number off "
                                              "the bottom edge.")
rec('silver', 5, 'guided_steps[1].hint: matched to the reworded step', old, pb['silver'][5]['guided_steps'][1]['hint'])

# ------------------------------------------------- silver[3]: hint overstates closeness
old = pb['silver'][3]['guided_steps'][4]['hint']
pb['silver'][3]['guided_steps'][4]['hint'] = ("Compare how far up the page each one sits against how far across the map they "
                                              "are from each other.")
rec('silver', 3, 'guided_steps[4].hint: dropped the false claim that both sit only a little above the 94 line', old, pb['silver'][3]['guided_steps'][4]['hint'])

# ------------------------------------------- bronze[3]: river vs grid line ambiguity
old = pb['bronze'][3]['guided_steps'][2]['pre']
pb['bronze'][3]['guided_steps'][2]['pre'] = ("Now find the blue horizontal grid line that passes just below the village. "
                                             "Follow it to the edge of the map and type the number printed on it.")
rec('bronze', 3, 'guided_steps[2].pre: says "grid line" so the River Skirfare cannot be mistaken for it', old, pb['bronze'][3]['guided_steps'][2]['pre'])

# ------------------------------- bronze[1]: map cannot prove coniferous, only woodland
old = pb['bronze'][1]['options'][1]
pb['bronze'][1]['options'][1] = "Woodland"
rec('bronze', 1, 'options[1]: "Coniferous forest" is not distinguishable in this rendering; the shading proves woodland', old, pb['bronze'][1]['options'][1])

old = pb['bronze'][1]['guided_steps'][5]['say']
pb['bronze'][1]['guided_steps'][5]['say'] = "The option describing that cover is <strong>Woodland</strong>."
rec('bronze', 1, 'guided_steps[5].say: matched to the reworded option', old, pb['bronze'][1]['guided_steps'][5]['say'])

# ------------------------------------- bronze[6]: debatable counts against the sheet
b6 = pb['bronze'][6]['guided_steps']
old = b6[2]['pre']
b6[2]['pre'] = "Type the number of yellow roads the line of houses is strung along."
rec('bronze', 6, 'guided_steps[2].pre: limited to yellow roads, so the grey spurs off the junction cannot change the count', old, b6[2]['pre'])

old = b6[2]['hint']
b6[2]['hint'] = "Trace the yellow road through the village and check whether a second yellow road joins it."
rec('bronze', 6, 'guided_steps[2].hint: matched to the reworded step', old, b6[2]['hint'])

old = json.dumps(b6[4], ensure_ascii=False)
b6[4] = {
    "pre": ("Check the alternative. Type the number of sides of that road that carry houses: "
            "1 if they all sit on one side, 2 if they line both sides."),
    "answer": 2,
    "hint": "Look above the road and then below it as it runs through the village.",
    "done": ("Houses down both sides of one road, and none gathered into a block away from it, is "
             "what fixes the shape.")
}
rec('bronze', 6, 'guided_steps[4]: replaced the "houses with no road beside them" count (two or three blocks off the road make 0 debatable) with a both-sides count', old, json.dumps(b6[4], ensure_ascii=False))

# ------------------------------------------------------- board-neutral exam context
old = json.dumps(d['exam_context'], ensure_ascii=False)
d['exam_context']['paper'] = "The paper that carries a printed map extract"
d['exam_context']['frequency'] = ("Very common: interpretation is usually the longest question set on the map "
                                  "extract")
rec('exam_context', None, 'paper/frequency: removed board-specific paper naming (this row serves six subjects)', old, json.dumps(d['exam_context'], ensure_ascii=False))

with io.open(P, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=1)

with io.open(os.path.join(os.path.dirname(P), 'repairs_L14.json'), 'w', encoding='utf-8') as f:
    json.dump(changes, f, ensure_ascii=False, indent=1)

print("edits:", len(changes))
