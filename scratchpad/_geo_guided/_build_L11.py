# -*- coding: utf-8 -*-
"""Build the guided-learning practice_data for Geography Skills L11."""
import json, io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
pd = json.load(io.open(os.path.join(HERE, "_live_L11.json"), encoding="utf-8"))

EM = "—"

# ---------------------------------------------------------------- em dashes
def de_em(s):
    return s.replace(" " + EM + " ", ": ").replace(EM, ",")

pd["exam_context"]["frequency"] = "Almost every year, an essential skill"

for we in pd["worked_examples"]:
    for st in we["steps"]:
        st["label"] = st["label"].replace(" " + EM + " ", ": ")
        st["content"] = st["content"].replace(
            " " + EM + " much more precise", ", much more precise")
        st["content"] = st["content"].replace(EM, ",")
    we["question"] = we["question"].replace(EM, ",")

# ---------------------------------------------------------------- method card
pd["method_card"] = {
    "title": "Grid References (4 and 6 Figure)",
    "steps": [
        "Easting first: read along the bottom of the map",
        "Northing second: read up the side of the map",
        "Four figures name the whole square",
        "Six figures add a tenth to each half",
    ],
    "content": (
        "<p><strong>Grid references</strong> locate places using the numbered lines "
        "printed on a map. Read the <em>easting</em> (along the bottom) first, then the "
        "<em>northing</em> (up the side): along the corridor, up the stairs.</p>"
        "<p>A <strong>four figure</strong> reference names a whole square, 1 km by 1 km. "
        "Take the easting of the line down the left of the square, then the northing of "
        "the line along its bottom.</p>"
        "<p>A <strong>six figure</strong> reference pins a point to the nearest 100 m. "
        "After each two figure line number, add how many tenths across (or up) the square "
        "the feature sits.</p>"
        "<p><strong>Watch out for:</strong> writing the northing first, and using the lines "
        "on the right and top of the square instead of the left and bottom.</p>"
    ),
    "example": (
        "<p><strong>Question:</strong> A church sits halfway across square 3832 and three "
        "tenths up. Give the six figure reference.</p>"
        "<p>Easting: line 38, plus 5 tenths, gives 385. Northing: line 32, plus 3 tenths, "
        "gives 323. Reference: <strong>385323</strong>.</p>"
    ),
}

# ---------------------------------------------------------------- tier guides
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: name the whole square",
        "steps": [
            "Find the feature, then look at the square it sits inside.",
            "Read the two figure number of the grid line down the <strong>left</strong> "
            "side of that square, using the numbers along the bottom of the map.",
            "Read the two figure number of the line along the <strong>bottom</strong> of "
            "the square, using the numbers up the side.",
            "Write the easting pair first, then the northing pair, with no gap.",
        ],
        "example": {
            "question": "A farm sits in the square whose left hand line is 27 and whose "
                        "bottom line is 14. Give the four figure grid reference.",
            "steps": [
                {"label": "Read the easting",
                 "content": "<p>The line down the left of the square is <strong>27</strong></p>"},
                {"label": "Read the northing",
                 "content": "<p>The line along the bottom of the square is <strong>14</strong></p>"},
                {"label": "Check the order",
                 "content": "<p>Easting leads, so the pair read along the bottom of the map goes first</p>"},
                {"label": "Answer", "content": "<p><strong>2714</strong></p>",
                 "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: pin a point inside the square",
        "steps": [
            "Start with the four figure square, exactly as at bronze.",
            "Split the square into ten strips across and judge how many tenths from the "
            "left line the feature sits. Add that digit to the easting.",
            "Do the same upwards from the bottom line and add that digit to the northing.",
            "Six figures in all: three for the easting, then three for the northing.",
        ],
        "example": {
            "question": "A post office sits 4 tenths across and 7 tenths up square 5238. "
                        "Give the six figure grid reference.",
            "steps": [
                {"label": "Build the easting",
                 "content": "<p>Line 52, plus 4 tenths across, gives <strong>524</strong></p>"},
                {"label": "Build the northing",
                 "content": "<p>Line 38, plus 7 tenths up, gives <strong>387</strong></p>"},
                {"label": "Check the halves",
                 "content": "<p>Three figures each, easting half first</p>"},
                {"label": "Answer", "content": "<p><strong>524387</strong></p>",
                 "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: find the feature, then reference it",
        "steps": [
            "The feature is described rather than labelled: a junction, a bridge, a fork, "
            "a river merge. Trace both things until they meet.",
            "Mark the meeting point itself, not the nearest label or name.",
            "Then give the six figure reference of that point in the usual order.",
        ],
        "example": {
            "question": "A road crosses a stream 8 tenths across and 2 tenths up square "
                        "4419. Give the six figure grid reference of the crossing.",
            "steps": [
                {"label": "Locate the crossing",
                 "content": "<p>Take the point where the two lines actually meet</p>"},
                {"label": "Build both halves",
                 "content": "<p>Easting 44 plus 8 tenths gives <strong>448</strong>; northing 19 plus 2 tenths gives <strong>192</strong></p>"},
                {"label": "Check the order",
                 "content": "<p>Easting half leads, northing half follows</p>"},
                {"label": "Answer", "content": "<p><strong>448192</strong></p>",
                 "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---------------------------------------------------------------- opener SVG
def carpark_svg():
    p = ['<svg viewBox="0 0 440 250" role="img" aria-label="A car park drawn as a grid '
         'of four numbered columns and three numbered rows with one car parked in column '
         'three, row two">']
    p.append('<rect x="50" y="20" width="360" height="180" fill="#f7f3ec" stroke="#8a7f6d"/>')
    for x in (140, 230, 320):
        p.append('<line x1="%d" y1="20" x2="%d" y2="200" stroke="#8a7f6d"/>' % (x, x))
    for y in (80, 140):
        p.append('<line x1="50" y1="%d" x2="410" y2="%d" stroke="#8a7f6d"/>' % (y, y))
    for i, cx in enumerate((95, 185, 275, 365)):
        p.append('<text x="%d" y="222" font-size="14" text-anchor="middle" fill="#2d2a26">%d</text>'
                 % (cx, i + 1))
    for i, cy in enumerate((176, 116, 56)):
        p.append('<text x="34" y="%d" font-size="14" text-anchor="middle" fill="#2d2a26">%d</text>'
                 % (cy, i + 1))
    p.append('<rect x="243" y="98" width="64" height="22" rx="6" fill="#b8543f"/>')
    p.append('<rect x="257" y="87" width="36" height="14" rx="4" fill="#d68b74"/>')
    p.append('<circle cx="256" cy="122" r="6" fill="#2d2a26"/>')
    p.append('<circle cx="294" cy="122" r="6" fill="#2d2a26"/>')
    p.append('<text x="275" y="136" font-size="11" text-anchor="middle" fill="#2d2a26">your car</text>')
    p.append('<text x="230" y="243" font-size="12" text-anchor="middle" fill="#6b6459">columns along the bottom</text>')
    p.append('</svg>')
    return "".join(p)

pd["guided"] = {}
pd["guided"]["opener"] = {
    "display": "<p>You have parked in a multi storey car park. The floor is marked out in "
               "a grid: columns are numbered along the bottom, rows are numbered up the "
               "side. You want to text a friend where the car is.</p>" + carpark_svg(),
    "steps": [
        {"say": "No method needed yet. Just look at the picture and count."},
        {"pre": "Count along the bottom. Type the column number your car is parked in.",
         "answer": 3,
         "hint": "Start at the left hand column and count across until you reach the car.",
         "done": "That is the along value. You read it without anybody teaching you a rule."},
        {"pre": "Now count up the side. Type the row number your car is parked in.",
         "answer": 2,
         "hint": "Start at the bottom row and count upwards until you reach the car.",
         "done": "That is the up value. Two numbers, and the car is pinned."},
        {"pre": "Text it as one number, along first and up second. Type the two digit number.",
         "answer": 32,
         "hint": "Put the column number down first, then write the row number straight after it.",
         "done": "Order matters. Swap them and your friend walks to the wrong bay."},
        {"say": "<strong>That is a grid reference.</strong> Maps do exactly this, but the "
                "numbers label the grid lines rather than the bays, and each half has two "
                "figures instead of one. Along first, up second: <strong>along the "
                "corridor, up the stairs</strong>. The rest of this lesson is that one "
                "habit, first for a whole square, then for a point inside it."},
    ],
}

# ---------------------------------------------------------------- teach SVGs
def teach_bronze_svg():
    p = ['<svg viewBox="0 0 460 300" role="img" aria-label="A small map with vertical grid '
         'lines numbered 37 to 40 along the bottom and horizontal lines numbered 21 to 23 '
         'up the side, with a church drawn in one square">']
    p.append('<rect x="60" y="40" width="300" height="200" fill="#f7f3ec" stroke="#8a7f6d"/>')
    for x, lab in ((60, "37"), (160, "38"), (260, "39"), (360, "40")):
        p.append('<line x1="%d" y1="40" x2="%d" y2="240" stroke="#8a7f6d"/>' % (x, x))
        p.append('<text x="%d" y="262" font-size="14" text-anchor="middle" fill="#2d2a26">%s</text>' % (x, lab))
    for y, lab in ((240, "21"), (140, "22"), (40, "23")):
        p.append('<line x1="60" y1="%d" x2="360" y2="%d" stroke="#8a7f6d"/>' % (y, y))
        p.append('<text x="38" y="%d" font-size="14" text-anchor="middle" fill="#2d2a26">%s</text>' % (y + 5, lab))
    p.append('<circle cx="205" cy="98" r="8" fill="none" stroke="#2d2a26" stroke-width="2"/>')
    p.append('<line x1="205" y1="68" x2="205" y2="90" stroke="#2d2a26" stroke-width="2"/>')
    p.append('<line x1="196" y1="76" x2="214" y2="76" stroke="#2d2a26" stroke-width="2"/>')
    p.append('<text x="205" y="124" font-size="12" text-anchor="middle" fill="#2d2a26">church</text>')
    p.append('<text x="210" y="286" font-size="12" text-anchor="middle" fill="#6b6459">eastings along the bottom, northings up the side</text>')
    p.append('</svg>')
    return "".join(p)

def tenths_square_svg(label, left, right, bottom, top, tx, ty, dotlab, aria, extra=""):
    """One grid square, 300 by 300, with tenth ticks. tx/ty are tenths (0-10)."""
    x0, y0, side = 90, 30, 300
    px = x0 + tx * (side / 10.0)
    py = y0 + side - ty * (side / 10.0)
    p = ['<svg viewBox="0 0 440 400" role="img" aria-label="%s">' % aria]
    p.append('<rect x="%d" y="%d" width="%d" height="%d" fill="#f7f3ec" stroke="#8a7f6d" stroke-width="2"/>'
             % (x0, y0, side, side))
    for k in range(1, 10):
        gx = x0 + k * 30
        p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#c3b9a6"/>' % (gx, y0 + side - 8, gx, y0 + side))
        gy = y0 + k * 30
        p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="#c3b9a6"/>' % (x0, gy, x0 + 8, gy))
    p.append('<text x="%d" y="%d" font-size="14" text-anchor="middle" fill="#2d2a26">%s</text>' % (x0, y0 + side + 24, left))
    p.append('<text x="%d" y="%d" font-size="14" text-anchor="middle" fill="#2d2a26">%s</text>' % (x0 + side, y0 + side + 24, right))
    p.append('<text x="60" y="%d" font-size="14" text-anchor="middle" fill="#2d2a26">%s</text>' % (y0 + side + 5, bottom))
    p.append('<text x="60" y="%d" font-size="14" text-anchor="middle" fill="#2d2a26">%s</text>' % (y0 + 5, top))
    p.append(extra)
    p.append('<circle cx="%d" cy="%d" r="6" fill="#b8543f"/>' % (px, py))
    p.append('<text x="%d" y="%d" font-size="12" text-anchor="middle" fill="#2d2a26">%s</text>'
             % (px, py - 12, dotlab))
    p.append('<text x="220" y="392" font-size="12" text-anchor="middle" fill="#6b6459">each tick is one tenth of the square</text>')
    p.append('</svg>')
    return "".join(p)

teach_silver_display = (
    "<p>This is one grid square from a map, blown up. Its left hand line is 38 and its "
    "bottom line is 22. Ticks mark each tenth of the way across and up.</p>"
    + tenths_square_svg("38", "38", "39", "22", "23", 6, 3, "post office",
                        "One enlarged grid square with tenth ticks and a post office marked "
                        "six tenths across and three tenths up")
)

_gold_extra = ('<polyline points="90,290 190,255 290,210 390,150" fill="none" stroke="#5b8fb0" stroke-width="3"/>'
               '<line x1="290" y1="330" x2="290" y2="30" stroke="#a8734a" stroke-width="4"/>')
teach_gold_display = (
    "<p>One grid square, blown up. Its left hand line is 45 and its bottom line is 31. A "
    "road (brown) runs across it and a river (blue) winds through it. Nothing is labelled.</p>"
    + tenths_square_svg("45", "45", "46", "31", "32", 7, 4, "bridge",
                        "One enlarged grid square with tenth ticks, a brown road and a blue "
                        "river crossing seven tenths across and four tenths up",
                        _gold_extra)
)

pd["guided"]["teach"] = {
    "bronze": {
        "display": "<p>Give the four figure grid reference of the square containing the "
                   "church.</p>" + teach_bronze_svg(),
        "steps": [
            {"say": "Find the church first. After that it is only reading numbers off the edges."},
            {"pre": "The church sits in one square. A vertical grid line runs down the left "
                    "side of that square. Type the two figure number printed under it.",
             "answer": 38,
             "hint": "Follow the left hand edge of the church's square straight down to the numbers along the bottom.",
             "done": "That is the easting, and it always comes first."},
            {"pre": "A horizontal grid line runs along the bottom of the same square. Type "
                    "the two figure number printed beside it.",
             "answer": 22,
             "hint": "Follow the bottom edge of the church's square straight across to the numbers up the side.",
             "phase": "substitute",
             "done": "That is the northing."},
            {"pre": "Join the two pairs, easting first, into one four figure number and type it.",
             "answer": 3822,
             "hint": "Write the pair you read along the bottom of the map, then the pair you read up the side."},
            {"pre": "Check it: type the last two figures of the reference you just wrote.",
             "answer": 22,
             "hint": "Copy them straight off your own answer, there is nothing new to work out.",
             "done": "Those two must be the line you read up the side. If they are not, the "
                     "halves are the wrong way round and the reference lands in a different square."},
            {"say": "<strong>Bronze move:</strong> two lines, the one down the left and the "
                    "one along the bottom, in that order. Four figures name a whole square, "
                    "1 km across."},
        ],
    },
    "silver": {
        "display": "<p>Give the six figure grid reference of the post office.</p>" + teach_silver_display,
        "steps": [
            {"say": "The square is already given to you, so the new work is the tenths."},
            {"pre": "Type the two figure number of the grid line down the left of the square.",
             "answer": 38,
             "hint": "It is printed under the left hand edge of the square.",
             "done": "That is the first two figures of the easting."},
            {"pre": "Count the ticks along the bottom. Type how many tenths across the "
                    "square the post office sits.",
             "answer": 6,
             "hint": "Each tick is one tenth, so count from the left hand edge to the dot.",
             "phase": "substitute",
             "done": "That tenth becomes the third figure of the easting."},
            {"pre": "Type the two figure number of the grid line along the bottom of the square.",
             "answer": 22,
             "hint": "It is printed beside the bottom edge of the square.",
             "done": "That is the first two figures of the northing."},
            {"pre": "Count the ticks up the side. Type how many tenths up the square the "
                    "post office sits.",
             "answer": 3,
             "hint": "Each tick is one tenth, so count from the bottom edge up to the dot."},
            {"pre": "Put the three easting figures first, then the three northing figures, "
                    "and type the six figure reference.",
             "answer": 386223,
             "hint": "Line number then tenth for the easting, then line number then tenth for the northing."},
            {"pre": "Check it: type the last three figures of the reference you just wrote.",
             "answer": 223,
             "hint": "Copy them straight off your own answer.",
             "done": "Those three must be the northing: the line read up the side, then its "
                     "tenth. If they are not, the two halves have swapped."},
            {"say": "<strong>Silver move:</strong> each half gains a third figure, the "
                    "tenths. Six figures pin a point to about 100 m."},
        ],
    },
    "gold": {
        "display": "<p>The road crosses the river at a bridge. Give the six figure grid "
                   "reference of the bridge.</p>" + teach_gold_display,
        "steps": [
            {"say": "Nothing is labelled here. The first job is deciding which point on the "
                    "square you are actually referencing."},
            {"pre": "The bridge is where the brown road and the blue river meet. Type how "
                    "many tenths across the square that meeting point sits.",
             "answer": 7,
             "hint": "Drop straight down from the crossing point to the ticks along the bottom and count from the left.",
             "done": "You have found the feature before touching any numbers. That is the gold habit."},
            {"pre": "Type the two figure number of the grid line down the left of the square.",
             "answer": 45,
             "hint": "It is printed under the left hand edge of the square.",
             "phase": "substitute"},
            {"pre": "Now the vertical direction. Type how many tenths up the square the "
                    "crossing point sits.",
             "answer": 4,
             "hint": "Track straight across from the crossing point to the ticks on the left and count from the bottom."},
            {"pre": "Type the two figure number of the grid line along the bottom of the square.",
             "answer": 31,
             "hint": "It is printed beside the bottom edge of the square."},
            {"pre": "Build the reference: easting line, its tenth, northing line, its tenth. "
                    "Type the six figures.",
             "answer": 457314,
             "hint": "Three figures for the easting half, then three for the northing half."},
            {"pre": "Check it: type the first three figures of the reference you just wrote.",
             "answer": 457,
             "hint": "Copy them straight off your own answer.",
             "done": "Those three must be the easting: the line down the left, then the "
                     "tenths across. If a river merge or a fork moved, only the tenths would change."},
            {"say": "<strong>Gold move:</strong> the question describes the feature instead "
                    "of naming it. Trace both features, mark where they meet, then reference "
                    "that exact point."},
        ],
    },
}

# ---------------------------------------------------------------- bank rebuild
pb = pd["problem_bank"]

pb["bronze_description"] = ("Name the whole square a labelled feature sits in: a four figure "
                            "reference, easting pair then northing pair.")
pb["silver_description"] = ("Pin a labelled feature inside its square with six figures by "
                            "adding tenths across and tenths up.")
pb["gold_description"] = ("Work out where an unlabelled feature is, such as a junction, a "
                          "fork or a river merge, then give its six figure reference.")

FOUR = {
    "bronze": [
        ("the two train station symbols", "the square they share"),
        ("the Fulledge label", "the square it sits in"),
        ("the Walker Fold label", "the square it sits in"),
        ("the Thurne label", "the square it sits in"),
        ("the Pyecombe label", "the square it sits in"),
        ("the Clayton Windmills label", "the square it sits in"),
        ("the police station symbol", "the square it sits in"),
        ("the Low Farm label", "the square it sits in"),
    ],
}
SIX = {
    "silver": [
        "the library symbol on Red Lion Street",
        "the water feature beside Chaigley Hall",
        "the New Barn Farm label",
        "the Burnley Manchester Road station symbol",
        "the turning off the yellow road towards Nu Farm",
        "the cul-de-sac off Underhill Lane",
        "the Low Farm label",
    ],
    "gold": [
        "the junction where Towneley Holmes Road meets Todmorden Road",
        "the point where the road forks on top of the hill",
        "the point where the A273 reaches School Lane",
        "the point where two waterways merge into one channel",
        "the education symbol nearest the Burnley Wood label",
    ],
}

BRONZE_HINTS = [
    "Find the two station symbols, then read the grid line down the left of their square before the line along its bottom.",
    "Find Fulledge, then read the grid line down the left of its square before the line along its bottom.",
    "Find Walker Fold, then read the grid line down the left of its square before the line along its bottom.",
    "Find Thurne, then read the grid line down the left of its square before the line along its bottom.",
    "Find Pyecombe, then read the grid line down the left of its square before the line along its bottom.",
    "Find Clayton Windmills, then read the grid line down the left of its square before the line along its bottom.",
    "Find the police station symbol, then read the grid line down the left of its square before the line along its bottom.",
    "Find Low Farm, then read the grid line down the left of its square before the line along its bottom.",
]
SILVER_HINTS = [
    "Find the library on Red Lion Street, read its two grid lines first, then judge the tenths across and up.",
    "Find Chaigley Hall and the water beside it, read its two grid lines first, then judge the tenths across and up.",
    "Find New Barn Farm, read its two grid lines first, then judge the tenths across and up.",
    "Find the station in the centre west of the map, read its two grid lines first, then judge the tenths across and up.",
    "Follow the yellow road east until a track leaves it towards Nu Farm, then read the lines and the tenths at that turning.",
    "Find Underhill Lane and the dead end road off it, read the two grid lines, then judge the tenths across and up.",
    "Find Low Farm in the south east, read its two grid lines first, then judge the tenths across and up.",
]
GOLD_HINTS = [
    "Trace Towneley Holmes Road until it reaches Todmorden Road, then read the easting and its tenth before the northing and its tenth.",
    "Follow the road up the hill to the point where it splits in two, then read the easting and its tenth before the northing and its tenth.",
    "Follow the thick pink road until School Lane joins it, then read the easting and its tenth before the northing and its tenth.",
    "Trace the blue channels until two of them join into a single wider one, then read the easting and its tenth before the northing and its tenth.",
    "Find the Burnley Wood label, look for the nearest education symbol, then read the easting and its tenth before the northing and its tenth.",
]


def four_steps(feat, sq, ans):
    e, n = divmod(ans, 100)
    return [
        {"say": "Find %s on the map. Nothing here is a calculation, it is all reading "
                "numbers off the edges." % feat},
        {"pre": "Look at %s. A vertical grid line runs down its left side. Read that "
                "line's two figure number from the numbers along the bottom of the map "
                "and type it." % sq,
         "answer": e,
         "hint": "The easting is the line touching the left edge of the square, and its number is printed along the bottom of the map.",
         "done": "That is the easting, and it always comes first."},
        {"pre": "Now the horizontal grid line along the bottom of that same square. Read "
                "its two figure number from the numbers up the side of the map and type it.",
         "answer": n,
         "hint": "The northing is the line touching the bottom of the square, and its number is printed up the side.",
         "phase": "substitute",
         "done": "That is the northing, and it always comes second."},
        {"pre": "Join the two pairs, easting first, into one four figure reference and type it.",
         "answer": ans,
         "hint": "Along the corridor before up the stairs: the pair read along the bottom of the map goes first."},
        {"pre": "Check it: type the last two figures of the reference you just wrote.",
         "answer": n,
         "hint": "Copy them straight off your own answer, there is nothing new to work out.",
         "done": "Those two must be the line you read up the side of the map. If they are "
                 "not, the halves are the wrong way round and the reference lands in a "
                 "different square."},
    ]


def six_steps(feat, ans):
    east, north = divmod(ans, 1000)
    e_line, e_tenth = divmod(east, 10)
    n_line, n_tenth = divmod(north, 10)
    return [
        {"say": "Find %s on the map. Six figures means two readings each way: the grid "
                "line, then the tenths." % feat},
        {"pre": "Start with the square it sits in. Read the two figure number of the grid "
                "line down its left side, from the numbers along the bottom of the map, "
                "and type it.",
         "answer": e_line,
         "hint": "The easting line is the one touching the left edge of the square, numbered along the bottom of the map.",
         "done": "That is the first two figures of the easting."},
        {"pre": "Picture that square split into ten strips from left to right. Type how "
                "many tenths across the square the feature sits, to the nearest whole tenth.",
         "answer": e_tenth,
         "hint": "Halfway across the square is 5 tenths, so judge the position against the middle."},
        {"pre": "Now the northing. Read the two figure number of the grid line along the "
                "bottom of the square, from the numbers up the side, and type it.",
         "answer": n_line,
         "hint": "The northing line is the one touching the bottom of the square, numbered up the side of the map.",
         "phase": "substitute",
         "done": "That is the first two figures of the northing."},
        {"pre": "Now split the square into ten strips from bottom to top. Type how many "
                "tenths up the square the feature sits.",
         "answer": n_tenth,
         "hint": "Halfway up the square is 5 tenths, so judge the position against the middle."},
        {"pre": "Put the three easting figures first, then the three northing figures, and "
                "type the six figure reference.",
         "answer": ans,
         "hint": "Line number then tenth for the easting, then line number then tenth for the northing, with no gap."},
        {"pre": "Check it: type the last three figures of the reference you just wrote.",
         "answer": north,
         "hint": "Copy them straight off your own answer.",
         "done": "Those three must be the northing: the line read up the side, then its "
                 "tenth. If they are not, the two halves have swapped and the point moves "
                 "right off the map."},
    ]


def four_misc(ans):
    e, n = divmod(ans, 100)
    return [
        {"pattern": "reversed_pairs",
         "message": "You have led with the pair read up the side of the map. A grid "
                    "reference always starts with the figures read along the bottom.",
         "expect": n * 100 + e,
         "note": "northing pair placed first"},
        {"pattern": "lines_above_and_right",
         "message": "You have read the lines on the right hand side and the top of the "
                    "square. Both figures come from the lines that touch the square on its "
                    "left and along its bottom.",
         "expect": (e + 1) * 100 + (n + 1),
         "note": "square identified by its top right corner"},
    ]


def six_misc(ans):
    east, north = divmod(ans, 1000)
    e_line = east // 10
    n_line = north // 10
    return [
        {"pattern": "reversed_halves",
         "message": "You have led with the northing half. The three figures read along the "
                    "bottom of the map always come first.",
         "expect": north * 1000 + east,
         "note": "northing half placed first"},
        {"pattern": "tenths_dropped",
         "message": "You have named the whole square instead of a point inside it. Each "
                    "half still needs its tenth adding on.",
         "expect": e_line * 100 + n_line,
         "note": "four figure answer given where six were asked"},
    ]


# bronze -----------------------------------------------------------------
b7 = pb["bronze"][7]
b7["display"] = ("What is the <strong>four-figure</strong> grid reference of the grid "
                 "square containing <strong>Low Farm</strong>?")
b7["solutions"] = [4018]
b7["image"] = "https://pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev/geography/os-maps/norfolk-broads-z16-final.jpg"

for i, p in enumerate(pb["bronze"]):
    ans = p["solutions"][0]
    feat, sq = FOUR["bronze"][i]
    p["hint"] = BRONZE_HINTS[i]
    p["guided_steps"] = four_steps(feat, sq, ans)
    p["misconceptions"] = four_misc(ans)

for i, p in enumerate(pb["silver"]):
    ans = p["solutions"][0]
    p["hint"] = SILVER_HINTS[i]
    p["guided_steps"] = six_steps(SIX["silver"][i], ans)
    p["misconceptions"] = six_misc(ans)

for i, p in enumerate(pb["gold"]):
    ans = p["solutions"][0]
    p["hint"] = GOLD_HINTS[i]
    p["guided_steps"] = six_steps(SIX["gold"][i], ans)
    p["misconceptions"] = six_misc(ans)

# ---------------------------------------------------------------- self-check
def verify():
    bad = []
    for tier in ("bronze", "silver", "gold"):
        for i, p in enumerate(pb[tier]):
            ans = p["solutions"][0]
            gs = p["guided_steps"]
            last_boxes = [s for s in gs if s.get("answer") is not None]
            if ans not in [s["answer"] for s in last_boxes]:
                bad.append("%s[%d] walk never reaches the stored answer" % (tier, i))
            for m in p["misconceptions"]:
                if m["expect"] == ans:
                    bad.append("%s[%d] expect equals answer" % (tier, i))
            digits = 4 if tier == "bronze" else 6
            if len(str(ans)) != digits:
                bad.append("%s[%d] answer has wrong digit count" % (tier, i))
    seen = {}
    for tier in ("bronze", "silver", "gold"):
        vals = [tuple(p["solutions"]) for p in pb[tier]]
        if len(set(vals)) != len(vals):
            bad.append("%s duplicate solutions" % tier)
    return bad

errs = verify()
out = os.path.join(HERE, "lesson_L11.json")
json.dump(pd, io.open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("self-check:", errs or "clean")
print("wrote", out, os.path.getsize(out), "bytes")
