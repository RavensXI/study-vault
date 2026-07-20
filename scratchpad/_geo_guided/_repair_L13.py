# -*- coding: utf-8 -*-
"""Repair L13 after checker findings. Edits lesson_L13.json in place."""
import json, io, os

P = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lesson_L13.json')
d = json.load(io.open(P, encoding='utf-8'))
pb = d['problem_bank']

# ---------------------------------------------------------------- FINDING 1+3
# gold[4]: the 220 m ring IS drawn on Worsaw Hill (verified: closed thin-contour
# loop at x 1376-1379, y 165-177 on pendle-hill-z16-final.jpg, inside the 210
# ring, inside the labelled 200 index). Highest ring drawn = 220, first undrawn
# contour = 230. (Worsaw Hill's true summit is 228 m, consistent.)
g4 = pb['gold'][4]
g4['display'] = (
    "Worsaw Hill in the north-east of this map is circled by a contour labelled "
    "200 m, and the interval is 10 m. Closed rings are drawn inside that labelled "
    "contour. The summit is higher than the highest ring drawn, but the next "
    "contour above it is not drawn anywhere on the hill. What is the value of "
    "that undrawn contour?"
)
g4['solutions'] = [230]
g4['hint'] = "Count every closed ring inside the labelled contour, then go one interval past the smallest."
g4['guided_steps'] = [
    {"say": "The highest ring drawn sets a floor for the summit. The first undrawn contour sets the ceiling."},
    {"pre": "Type the number on the vertical grid line immediately to the left of Worsaw Hill.",
     "hint": "The eastings read 76, 77, 78.",
     "done": "Hill located, so you are reasoning about the right summit and not one of its neighbours.",
     "answer": 77},
    {"pre": "Type how many closed rings are drawn inside the labelled 200 m contour.",
     "hint": "One is a large loop round the whole top. Look again very close to the summit before you settle on a count.",
     "done": "Small summit rings are easy to miss, and missing one costs you a whole interval.",
     "phase": "substitute",
     "answer": 2},
    {"pre": "Each ring inwards is one interval up. Type the height of the highest ring drawn, in metres.",
     "hint": "Start at the labelled height and add the interval once for each ring you counted.",
     "answer": 220},
    {"pre": "Add one more interval. Type the value of the first contour that is not drawn, in metres.",
     "hint": "One step above the highest ring.",
     "answer": 230},
    {"pre": "Type 1 if the summit must be lower than that undrawn contour, or 2 if it could be higher than it.",
     "hint": "Ask what the map would have done if the land reached that height.",
     "done": "If the ground reached that height the map would have drawn the ring, so the summit is trapped between the two values.",
     "answer": 1},
]
g4['misconceptions'] = [
    {"pattern": "missed_the_small_summit_ring",
     "expect": 220,
     "message": "You have missed one of the closed rings inside the labelled contour. Look again at the ground closest to the summit and recount."},
    {"pattern": "took_a_step_down",
     "expect": 210,
     "message": "You went down a step instead of up. The undrawn line lies above the highest ring, not below it."},
    {"pattern": "used_the_index_gap",
     "expect": 270,
     "message": "You added the gap between thick index lines rather than a single interval."},
]

# ---------------------------------------------------------------- FINDING 2
# bronze[1]: 'one more, smaller ring' is false (there are two). Reword to the
# next ring in from the labelled contour, which keeps the stored answer 210 and
# keeps the rung at bronze difficulty (read what is printed, add one interval).
b1 = pb['bronze'][1]
b1['display'] = (
    "The contour interval on this map is 10 m, so each brown line is 10 m higher "
    "or lower than the one beside it. Worsaw Hill in the north-east is circled by "
    "a contour that carries a printed height. What height is the next ring in "
    "from that labelled line?"
)
b1['guided_steps'] = [
    {"say": "Rings inside rings mean a hill. The smaller the ring, the higher the ground it encloses."},
    {"pre": "Find Worsaw Hill in the north-east. Type the number on the vertical grid line immediately to its left.",
     "hint": "The eastings read 76, 77, 78 from left to right.",
     "done": "Hill located, so the lines you read next belong to it and not to its neighbour.",
     "answer": 77},
    {"pre": "Type the height printed on the labelled contour that circles the hill, in metres.",
     "hint": "It is the small brown number sitting in a gap in one of the rings.",
     "done": "That printed number is the only height on this hill the map states outright. Everything else is counted from it.",
     "answer": 200},
    {"pre": "Type the contour interval on this map, in metres.",
     "hint": "The interval is given to you in the question.",
     "phase": "substitute",
     "answer": 10},
    {"pre": "Moving inwards on a hill is moving uphill. Add one interval to the labelled height. Type the height of the next ring in, in metres.",
     "hint": "One step up from the line you have just read.",
     "answer": 210},
    {"pre": "Type 1 if the ground inside that ring must be higher than the ring itself, or 2 if it must be lower.",
     "hint": "The ring is the last line the land climbs past.",
     "done": "The summit is always higher than the highest ring drawn round it, which is why maps often print a spot height as well.",
     "answer": 1},
]

# ---------------------------------------------------------------- FINDING 4
# Board-neutral exam context (this row is propagated to five boards + Unity).
d['exam_context']['paper'] = (
    "Map and fieldwork skills questions, on whichever paper your board sets them"
)

# ---------------------------------------------------------------- FINDING 5
pb['bronze'][4]['guided_steps'][1]['hint'] = (
    "Trace each edge of that square in turn and count every brown line that crosses into it."
)

# ---------------------------------------------------------------- FINDING 6
pb['bronze'][6]['guided_steps'][3]['hint'] = (
    "Put the climb you have just worked out next to the ground you cover to gain it, and compare the two."
)

# ---------------------------------------------------------------- FINDING 7
s4 = pb['silver'][4]['guided_steps']
s4[3]['hint'] = (
    "Put a fingertip on the labelled line and slide it south, then note how far you go before you meet the next brown line."
)
s4[4]['hint'] = (
    "Slide from the same labelled line northwards instead, and compare that distance with the one you have just measured."
)

# ---------------------------------------------------------------- FINDING 9
# Gold tier guide must not repeat the Gold teach walk's figures (80 m, 0.4 km).
d['tier_guides']['gold']['example'] = {
    "question": "A slope climbs 75 m over 0.6 km. Give the gradient in metres per km and as a ratio.",
    "steps": [
        {"label": "Metres per km", "content": "<p>75 ÷ 0.6 = 125 m per km</p>"},
        {"label": "Convert for the ratio", "content": "<p>0.6 km = 600 m along the ground</p>"},
        {"label": "Check it makes sense", "content": "<p>600 m along for 75 m up is 8 m along for every 1 m up.</p>"},
        {"label": "Answer", "content": "<p><strong>125 m per km, or 1 in 8</strong></p>",
         "isAnswer": True, "is_answer": True},
    ],
}

with io.open(P, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
print('written', P)
