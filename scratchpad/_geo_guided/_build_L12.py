# -*- coding: utf-8 -*-
"""Build the guided practice_data for Geography Skills L12 (Distance & Direction)."""
import io, json, os, copy

HERE = os.path.dirname(os.path.abspath(__file__))
pd = json.load(io.open(os.path.join(HERE, "_live_L12.json"), encoding="utf-8"))

COMPASS = "N=1, NE=2, E=3, SE=4, S=5, SW=6, W=7, NW=8"
OPP = lambda n: n + 4 if n <= 4 else n - 4


def compass_walk(start, target, q_up, a_up, q_side, a_side, dirnum, locate_done,
                 side_hint="Compare how far across the page each one sits.",
                 final_word=None):
    opp = OPP(dirnum)
    return [
        {"say": "Direction runs from the place you stand in to the place you look at. Here you stand at <strong>%s</strong>." % start},
        {"pre": q_up, "answer": a_up,
         "hint": "Compare how far up the page each one sits.",
         "done": locate_done},
        {"pre": q_side, "answer": a_side, "hint": side_hint, "phase": "substitute"},
        {"pre": "Up the map is north and right is east. Using %s, type the number for the direction of %s from %s." % (COMPASS, target, start),
         "answer": dirnum,
         "hint": "Put your two answers together, then find that combination in the list."},
        {"pre": "Check by turning round: from %s, %s lies in the exact opposite direction. Type its number from the same list." % (target, start),
         "answer": opp,
         "hint": "Opposite points sit four places apart on the list, so add 4 or take 4 away.",
         "done": "Opposites are always four apart on that list. If your two answers are not four apart, one of them is wrong."},
        {"say": "The option that names that point is the answer: <strong>%s</strong>." % (final_word or "")},
    ]


def ruler_walk(a_place, b_place, cm, cmper, km, locate_pre, locate_ans, locate_hint,
               locate_done, check_step=None, tail=None):
    steps = [
        {"say": "Find both places first, then let the ruler do the work."},
        {"pre": locate_pre, "answer": locate_ans, "hint": locate_hint, "done": locate_done},
        {"pre": "Drag the ruler from %s to %s. Type the reading in centimetres, to the nearest centimetre." % (a_place, b_place),
         "answer": cm,
         "hint": "Put one end of the ruler on each place, then read the scale printed on it.",
         "phase": "substitute"},
        {"pre": "On this map %d cm stands for 1 km. Type the real distance in km." % cmper,
         "answer": km,
         "hint": "Divide your centimetre reading by %d." % cmper},
    ]
    if tail:
        steps.extend(tail)
    steps.append(check_step or {
        "pre": "Check: multiply your kilometre answer back by %d and type the centimetres you should get." % cmper,
        "answer": cm,
        "hint": "Undo the division you just did.",
        "done": "It matches the reading you took, so the conversion went the right way round."})
    return steps


def scale_miscs(cm, cmper, km, other=None):
    """Standard determinate scale errors for a ruler distance problem."""
    out = [{
        "pattern": "answered_in_centimetres",
        "message": "That is the ruler reading, not the real distance. Convert it using the number of centimetres that stand for 1 km on this map.",
        "expect": cm,
    }]
    if other:
        out.append({
            "pattern": "used_the_wrong_scale",
            "message": "You divided by a scale this map does not use. Check how many centimetres stand for 1 km before you divide.",
            "expect": other,
        })
    return out


pb = pd["problem_bank"]
B, S, G = pb["bronze"], pb["silver"], pb["gold"]

# ---------------------------------------------------------------- BRONZE ----
B[0]["hint"] = "Read the numbers printed on the vertical grid lines and count the squares between them."
B[0]["guided_steps"] = [
    {"say": "Eastings are the numbers along the bottom edge. They count up as you move right."},
    {"pre": "Find the vertical line labelled 46. Type the easting of the line one square to its right.",
     "answer": 47,
     "hint": "Eastings go up by 1 for every square you move right.",
     "done": "One square right is one whole easting. That is the fact the rest of this rests on."},
    {"pre": "Type how many whole grid squares lie between line 46 and line 49.",
     "answer": 3,
     "hint": "Take the smaller easting away from the larger one.",
     "phase": "substitute"},
    {"pre": "Each grid square on this map is 1 km across. Type the distance between the two lines in km.",
     "answer": 3,
     "hint": "One square is one kilometre, so the number of squares is the number of kilometres."},
    {"pre": "Check with the ruler: 2 cm stands for 1 km here. Type the reading in centimetres you would expect between the two lines.",
     "answer": 6,
     "hint": "Multiply your kilometre answer by the number of centimetres that stand for 1 km.",
     "done": "The ruler and the grid squares agree, which is the sign the count was right."},
]
B[0]["misconceptions"] = [
    {"pattern": "counted_lines_not_gaps",
     "message": "You counted the grid lines instead of the gaps between them. Four lines have one fewer gap.",
     "expect": 4},
    {"pattern": "answered_in_centimetres",
     "message": "That is the centimetre reading rather than the ground distance. Divide by the number of centimetres that stand for 1 km.",
     "expect": 6},
]

B[1]["hint"] = "Stand at Kingston, face Corfe Castle, and remember that up the map is north."
B[1]["guided_steps"] = compass_walk(
    "Kingston", "Corfe Castle",
    "Find Kingston near the bottom of the map. Type 1 if Corfe Castle is higher up the map than Kingston, 2 if it is lower down.", 1,
    "Type 1 if Corfe Castle is clearly further left than Kingston, 2 if clearly further right, 3 if it sits roughly straight above it.", 3,
    1, "That one look settles north or south before anything else.",
    final_word="N")
B[1]["misconceptions"] = [
    {"pattern": "reversed_the_two_places",
     "message": "You gave the direction from Corfe Castle to Kingston. The place named after the word from is where you stand.",
     "expect": 4},
    {"pattern": "let_the_wording_add_east",
     "message": "The words top-right pulled you off the vertical. Judge how far across the page each place sits before adding any east or west.",
     "expect": 1},
]

B[2]["hint"] = "Measure Kingston to Corfe Castle in centimetres, then divide by the number of centimetres that stand for 1 km."
B[2]["guided_steps"] = ruler_walk(
    "Kingston", "Corfe Castle", 5, 2, 2.5,
    "Type 1 if Corfe Castle is higher up the map than Kingston, 2 if it is lower down.", 1,
    "Look at how far up the page each place sits.",
    "Knowing which way the line runs stops you measuring to the wrong feature.")
B[2]["misconceptions"] = [
    {"pattern": "answered_in_centimetres",
     "message": "That is the ruler reading, not the ground distance. Divide it by the number of centimetres that stand for 1 km.",
     "expect": 5},
    {"pattern": "multiplied_by_the_scale",
     "message": "You went the wrong way with the scale, which makes the ground shorter or longer than it can be. Decide whether centimetres on paper turn into more kilometres or fewer.",
     "expect": 10},
]

B[3]["hint"] = "Stand in Castleton and face the dense contour lines, then read up and across."
B[3]["guided_steps"] = compass_walk(
    "Castleton", "the upland",
    "Find Castleton in the bottom right. Type 1 if the upland is higher up the map than Castleton, 2 if it is lower down.", 1,
    "Type 1 if the upland is further left than Castleton, 2 if it is further right.", 1,
    8, "Up or down comes first, and it already rules out half the compass.",
    final_word="NW")
B[3]["misconceptions"] = [
    {"pattern": "reversed_the_two_places",
     "message": "That is the direction from the upland back to Castleton. Stand in the place named after the word from.",
     "expect": 3},
    {"pattern": "swapped_left_and_right",
     "message": "The up and down half is right but the sideways half is flipped. The left of a map is west.",
     "expect": 1},
]

B[4]["hint"] = "Stand at the roundabout in the north of the map and look towards Hare Runs."
B[4]["guided_steps"] = compass_walk(
    "the roundabout", "Hare Runs",
    "Find the roundabout in the north of the map. Type 1 if Hare Runs is higher up the map, 2 if it is lower down.", 2,
    "Type 1 if Hare Runs is clearly further left, 2 if clearly further right, 3 if it lies roughly straight below the roundabout.", 3,
    5, "Hare Runs sits below the roundabout, so the answer lives in the lower half of the compass.",
    final_word="S")
B[4]["misconceptions"] = [
    {"pattern": "reversed_the_two_places",
     "message": "That is the direction from Hare Runs back to the roundabout. Stand at the place named after the word from.",
     "expect": 0},
    {"pattern": "added_a_sideways_point",
     "message": "A small sideways shift has been turned into a full compass point. Only add east or west when the sideways gap is about as big as the up and down gap.",
     "expect": 3},
]

B[5]["hint"] = "Measure in centimetres first, then convert using this map's scale of 4 cm to 1 km."
B[5]["guided_steps"] = ruler_walk(
    "Kingston", "West Orchard Farm", 8, 4, 2,
    "Type 1 if West Orchard Farm is higher up the map than Kingston, 2 if it is lower down.", 1,
    "The farm is named as being in the top left, so compare it with Kingston.",
    "Both ends of the line are now fixed, so the ruler has somewhere to go.")
B[5]["misconceptions"] = scale_miscs(8, 4, 2, other=4)

B[6]["hint"] = "Stand in Worston and face the densest contour lines."
B[6]["guided_steps"] = compass_walk(
    "Worston", "Pendle Hill",
    "Find Worston on the map. Type 1 if Pendle Hill is higher up the map than Worston, 2 if it is lower down.", 2,
    "Type 1 if Pendle Hill is further left than Worston, 2 if it is further right.", 2,
    4, "Fixing up or down first cuts the compass in half.",
    final_word="SE")
B[6]["misconceptions"] = [
    {"pattern": "reversed_the_two_places",
     "message": "That is the direction from Pendle Hill back to Worston. Stand in the place named after the word from.",
     "expect": 7},
    {"pattern": "swapped_left_and_right",
     "message": "The up and down half is right but the sideways half is flipped. The right of a map is east.",
     "expect": 5},
]

B[7]["hint"] = "Measure the full diagonal in centimetres, then convert with the 2 cm to 1 km scale."
B[7]["guided_steps"] = ruler_walk(
    "the bottom left corner", "the top right corner", 11, 2, 5.5,
    "Type 1 if the line between those two corners runs up to the right, 2 if it runs down to the right.", 1,
    "Picture the line joining the two corners named in the question.",
    "Fixing which diagonal you want stops you measuring the other one.")
B[7]["misconceptions"] = [
    {"pattern": "answered_in_centimetres",
     "message": "That is the ruler reading, not the ground distance. Divide by the number of centimetres that stand for 1 km.",
     "expect": 11},
    {"pattern": "rounded_to_a_whole_km",
     "message": "You have dropped a half kilometre. The question asks to the nearest 0.5 km, so halves are allowed.",
     "expect": 5},
]

# ---------------------------------------------------------------- SILVER ----
S[0]["hint"] = "Both places sit along the south of the map, so the line runs across rather than up."
S[0]["guided_steps"] = ruler_walk(
    "Scale Hall", "Newton", 4, 2, 2,
    "Both places lie along the south of the map. Type 1 if Newton is further right than Scale Hall, 2 if it is further left.", 1,
    "South-west is the left end of the bottom edge, south-east the right end.",
    "Knowing the line runs across the map, not up it, tells you what a sensible answer looks like.",
    check_step={"pre": "Check against the grid: each square is 1 km across. Type how many whole grid squares your line spans.",
                "answer": 2,
                "hint": "Count the full squares the line crosses from end to end.",
                "done": "The squares and the ruler give the same figure, so the measurement is sound."})
S[0]["misconceptions"] = scale_miscs(4, 2, 2, other=1)

S[1]["hint"] = "Find both places first, then measure and convert with the 2 cm to 1 km scale."
S[1]["guided_steps"] = ruler_walk(
    "Church Knowle", "Kingston", 5, 2, 2.5,
    "Type 1 if Kingston is lower down the map than Church Knowle, 2 if it is higher up.", 1,
    "One is named as top-centre and the other as bottom-right.",
    "The line runs down the map and across it, so it is a genuine diagonal.")
S[1]["misconceptions"] = [
    {"pattern": "answered_in_centimetres",
     "message": "That is the ruler reading rather than the ground distance. Divide by the number of centimetres that stand for 1 km.",
     "expect": 5},
    {"pattern": "rounded_to_a_whole_km",
     "message": "You have rounded away a half kilometre. This question allows halves, so keep one if your measurement lands there.",
     "expect": 2},
]

S[2]["hint"] = "Stand at Riding House Farm and look towards Castleton."
S[2]["guided_steps"] = compass_walk(
    "Riding House Farm", "Castleton",
    "Find Riding House Farm. Type 1 if Castleton is higher up the map than the farm, 2 if it is lower down.", 2,
    "Type 1 if Castleton is clearly further left, 2 if clearly further right, 3 if it lies roughly straight below the farm.", 3,
    5, "Up or down first: that alone decides which half of the compass you are in.",
    final_word="S")
S[2]["misconceptions"] = [
    {"pattern": "reversed_the_two_places",
     "message": "That is the direction from Castleton back to the farm. Stand in the place named after the word from.",
     "expect": 0},
    {"pattern": "added_a_sideways_point",
     "message": "A slight sideways shift has become a full compass point. Only add east or west when that gap is about as big as the up and down gap.",
     "expect": 3},
]

S[3]["display"] = ("What is the straight-line distance from where <strong>Hasty Brow Road</strong> goes over "
                   "<strong>Lancaster Canal</strong> to the <strong>museum</strong> in the south-east of the map? "
                   "Give your answer in metres, to the nearest 500 m.")
S[3]["solutions"] = [4000]
S[3]["hint"] = "Start where the road crosses the canal, measure to the museum, convert with the scale, then turn kilometres into metres."
S[3]["guided_steps"] = ruler_walk(
    "the canal crossing", "the museum", 16, 4, 4,
    "Find where Hasty Brow Road crosses the Lancaster Canal. Type 1 if the museum lies lower down the map than that crossing, 2 if it lies higher up.", 1,
    "The museum is named as being in the south-east of the map.",
    "A road and a canal cross at one point only, so that gives you an exact starting place.",
    tail=[{"pre": "The question wants metres. Type that distance in metres.",
           "answer": 4000,
           "hint": "There are 1000 m in 1 km, so multiply."}],
    check_step={"pre": "Check: divide your answer in metres by 1000 and type the kilometres you get back.",
                "answer": 4,
                "hint": "Undo the multiplication you just did.",
                "done": "It lands back on the figure you converted from, so the units were handled properly."})
S[3]["misconceptions"] = [
    {"pattern": "left_it_in_kilometres",
     "message": "You stopped at kilometres. Read the units the question asks for, then convert.",
     "expect": 4},
    {"pattern": "centimetres_straight_to_metres",
     "message": "The ruler reading has been turned straight into metres. Use the map scale to reach kilometres first, then convert.",
     "expect": 16000},
]

S[4]["hint"] = "Stand at How Close Fell and look towards Fosse Beck."
S[4]["guided_steps"] = compass_walk(
    "How Close Fell", "Fosse Beck",
    "Find How Close Fell. Type 1 if Fosse Beck is higher up the map than the fell, 2 if it is lower down.", 1,
    "Type 1 if Fosse Beck is further left than the fell, 2 if it is further right.", 2,
    2, "Higher up the map means the answer is in the northern half of the compass.",
    final_word="NE")
S[4]["misconceptions"] = [
    {"pattern": "reversed_the_two_places",
     "message": "That is the direction from Fosse Beck back to the fell. Stand in the place named after the word from.",
     "expect": 5},
    {"pattern": "swapped_left_and_right",
     "message": "The up and down half is right but the sideways half is flipped. The right of a map is east.",
     "expect": 7},
]

S[5]["hint"] = "Stand at Willwood House and look towards Barham Farm House."
S[5]["guided_steps"] = compass_walk(
    "Willwood House", "Barham Farm House",
    "Find Willwood House. Type 1 if Barham Farm House is clearly higher up the map, 2 if clearly lower down, 3 if it is roughly level with it.", 3,
    "Type 1 if Barham Farm House is further left than Willwood House, 2 if it is further right.", 2,
    3, "Level with each other means neither north nor south belongs in the answer.",
    side_hint="Compare how far across the page each house sits.",
    final_word="E")
S[5]["misconceptions"] = [
    {"pattern": "reversed_the_two_places",
     "message": "That is the direction from Barham Farm House back to Willwood House. Stand in the place named after the word from.",
     "expect": 6},
    {"pattern": "added_a_vertical_point",
     "message": "A tiny height difference has become a full compass point. Only add north or south when that gap is about as big as the sideways gap.",
     "expect": 1},
]

S[6]["display"] = ("What is the <strong>straight-line distance</strong> from <strong>Castleton</strong> "
                   "to the very top of the <strong>hill in the west</strong> of the map? "
                   "Give your answer in metres, to the nearest 500 m.")
S[6]["solutions"] = [2500]
S[6]["hint"] = "Measure in centimetres, convert to kilometres with the map scale, then turn kilometres into metres."
S[6]["guided_steps"] = ruler_walk(
    "Castleton", "the hilltop in the west", 5, 2, 2.5,
    "Type 1 if the hilltop is further left than Castleton, 2 if it is further right.", 1,
    "West is the left-hand side of the map.",
    "The line runs across the map, which is what west of tells you.",
    tail=[{"pre": "The question wants metres. Type that distance in metres.",
           "answer": 2500,
           "hint": "There are 1000 m in 1 km, so multiply."}],
    check_step={"pre": "Check: divide your answer in metres by 1000 and type the kilometres you get back.",
                "answer": 2.5,
                "hint": "Undo the multiplication you just did.",
                "done": "It lands back on the figure you converted from, so the units were handled properly."})
S[6]["misconceptions"] = [
    {"pattern": "left_it_in_kilometres",
     "message": "You stopped at kilometres. Read the units the question asks for, then convert.",
     "expect": 2.5},
    {"pattern": "centimetres_straight_to_metres",
     "message": "The ruler reading has been turned straight into metres. Use the map scale to reach kilometres first, then convert.",
     "expect": 5000},
]

# ------------------------------------------------------------------ GOLD ----
G[0]["hint"] = "Split it into how far east and how far north or south first, using the six-figure references."
G[0]["guided_steps"] = [
    {"say": "A six-figure reference splits into three easting digits and three northing digits."},
    {"pre": "Type the three-figure easting of the starting house, 476636.",
     "answer": 476,
     "hint": "The easting is the first half of the reference.",
     "done": "Splitting the reference is how you find the house: eastings across the bottom, northings up the side."},
    {"pre": "Type the three-figure northing of the finishing house, 488625.",
     "answer": 625,
     "hint": "The northing is the second half of the reference."},
    {"pre": "Each step in the third digit is 100 m. Type how far east the walker moved, in metres.",
     "answer": 1200,
     "hint": "Take 476 from 488, then multiply by 100.",
     "phase": "substitute"},
    {"pre": "Type how far south the walker moved, in metres.",
     "answer": 1100,
     "hint": "Take 625 from 636, then multiply by 100."},
    {"pre": "In kilometres the two legs are 1.2 and 1.1. Type 1.2 squared added to 1.1 squared.",
     "answer": 2.65,
     "hint": "Square each leg on its own, then add the two results."},
    {"pre": "The square root of that total is a little over 1.6. Type the straight-line distance in km, to the nearest 0.5 km.",
     "answer": 1.5,
     "hint": "Decide whether a value just over 1.6 is closer to 1.5 or to 2.0."},
    {"pre": "Check the direction. The easting rose and the northing fell. Using N=1, NE=2, E=3, SE=4, type the number for the direction walked.",
     "answer": 4,
     "hint": "Rising eastings mean east, falling northings mean south.",
     "done": "The straight line is longer than either leg but shorter than the two added together, which is exactly what Pythagoras should give."},
    {"say": "The option carrying that distance and that direction is the answer: <strong>1.5 km, SE</strong>."},
]
G[0]["misconceptions"] = [
    {"pattern": "northing_read_as_rising",
     "message": "You treated the northing as going up. Compare the two northings and check which of them is the bigger.",
     "expect": 0},
    {"pattern": "rounded_to_a_whole_km",
     "message": "The direction is right but the distance has been pushed up to a whole kilometre. This question allows halves.",
     "expect": 2},
]

G[1]["hint"] = "Both places sit towards the right of the map, so measure that line and convert it."
G[1]["guided_steps"] = ruler_walk(
    "Corfe Castle", "Kingston", 5, 2, 2.5,
    "Both places lie towards the right of the map. Type 1 if Kingston is lower down than Corfe Castle, 2 if it is higher up.", 1,
    "One is named as top-right and the other as bottom-right.",
    "The line runs mainly down the map, so most of the distance is north to south.",
    check_step={"pre": "Check against the grid: each square is 1 km across. Type how many whole grid squares your line spans.",
                "answer": 2,
                "hint": "Count only the complete squares the line passes through.",
                "done": "Two full squares plus part of a third fits the figure you converted, so the two methods agree."})
G[1]["misconceptions"] = [
    {"pattern": "answered_in_centimetres",
     "message": "That is the ruler reading, not the ground distance. Divide by the number of centimetres that stand for 1 km.",
     "expect": 5},
    {"pattern": "rounded_to_a_whole_km",
     "message": "You have rounded away a half kilometre. The question allows halves, so keep one if the measurement lands there.",
     "expect": 2},
]

G[2]["hint"] = "Find the settlement and the lake first, then measure the straight line and convert it."
G[2]["guided_steps"] = ruler_walk(
    "the settlement", "the lake", 7, 2, 3.5,
    "Type 1 if the lake is higher up the map than the settlement, 2 if it is lower down.", 1,
    "One is named as bottom-left and the other as top-centre.",
    "Bottom-left to top-centre is a long diagonal, so expect one of the bigger distances on this map.")
G[2]["misconceptions"] = scale_miscs(7, 2, 3.5, other=1.75)

G[3]["hint"] = "Stand in Castleton and look towards the farm, then read up and across."
G[3]["guided_steps"] = compass_walk(
    "Castleton", "Only Grange Farm",
    "Find Castleton. Type 1 if Only Grange Farm is higher up the map than Castleton, 2 if it is lower down.", 1,
    "Type 1 if the farm is further left than Castleton, 2 if it is further right.", 1,
    8, "Above Castleton means the answer sits in the northern half of the compass.",
    final_word="NW")
G[3]["misconceptions"] = [
    {"pattern": "reversed_the_two_places",
     "message": "That is the direction from the farm back to Castleton. Stand in the place named after the word from.",
     "expect": 3},
    {"pattern": "swapped_left_and_right",
     "message": "The up and down half is right but the sideways half is flipped. The left of a map is west.",
     "expect": 1},
]

G[4]["hint"] = "Measure from where the pink road enters the map to where it leaves, then convert with the 4 cm scale."
G[4]["guided_steps"] = ruler_walk(
    "one end of the A6", "the other end of the A6", 8, 4, 2,
    "Trace the pink A6 across the map. Type how many ends of it you can see, counting where it enters the map and where it leaves.", 2,
    "Follow the pink road until it runs off the edge of the map in each direction.",
    "Both ends are on the map, so the whole length shown can be measured in one go.")
G[4]["misconceptions"] = scale_miscs(8, 4, 2, other=4)

# ------------------------------------------------------- tier descriptions ---
pb["bronze_description"] = "One step at a time: read a distance straight off the ruler, or name a direction with both places pointed out for you."
pb["silver_description"] = "Find both places on the map yourself, then measure across it or name a direction that falls between two compass points."
pb["gold_description"] = "Put the skills together: work a distance from grid references or a long ruler line, and give distance and direction in one answer."

# ------------------------------------------------------------- tier guides ---
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one measurement or one direction",
        "steps": [
            "Distance: line the ruler up from the first place to the second, read the centimetres, then divide by the number of centimetres that stand for 1 km.",
            "One grid square is 1 km across, so use the squares to check your answer looks sensible.",
            "Direction: stand at the place named first and face the other. Up is north, down is south, right is east, left is west.",
        ],
        "example": {
            "question": "A map uses 2 cm for 1 km. A footpath measures 6 cm. How long is it on the ground?",
            "steps": [
                {"label": "Read the scale", "content": "<p>2 cm on the map stands for 1 km on the ground</p>"},
                {"label": "Divide the measurement by the scale", "content": "<p>6 ÷ 2</p>"},
                {"label": "Check it makes sense", "content": "<p>6 cm is three lots of 2 cm, so the answer must be three lots of 1 km</p>"},
                {"label": "Answer", "content": "<p><strong>3 km</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: locate the places, then measure",
        "steps": [
            "Nothing is labelled for you here, so find both places on the map before you measure anything.",
            "Read the ruler to the nearest centimetre, divide by the scale, then round to the precision the question asks for.",
            "If a place sits both to the side and above or below, the direction is one of the in-between points: NE, SE, SW or NW.",
        ],
        "example": {
            "question": "A map uses 4 cm for 1 km. Two farms are 10 cm apart. How far apart are they, to the nearest 0.5 km?",
            "steps": [
                {"label": "Read the scale", "content": "<p>4 cm on the map stands for 1 km on the ground</p>"},
                {"label": "Divide the measurement by the scale", "content": "<p>10 ÷ 4 = 2.5</p>"},
                {"label": "Check it makes sense", "content": "<p>2.5 × 4 = 10 cm, which is the reading taken, so the conversion went the right way</p>"},
                {"label": "Answer", "content": "<p><strong>2.5 km</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: distance and direction together",
        "steps": [
            "Six-figure references give a distance without a ruler: every step in the third digit is 100 m.",
            "Work out how far east or west and how far north or south, square both, add them, then take the square root.",
            "Finish with the direction: rising eastings mean east, falling northings mean south, and the two together give the diagonal.",
        ],
        "example": {
            "question": "A walker goes from 320450 to 344474. How far, and in which direction?",
            "steps": [
                {"label": "Eastings", "content": "<p>344 − 320 = 24, so 2.4 km east</p>"},
                {"label": "Northings", "content": "<p>474 − 450 = 24, so 2.4 km north</p>"},
                {"label": "Pythagoras", "content": "<p>2.4² + 2.4² = 11.52, and √11.52 = 3.39</p>"},
                {"label": "Check it makes sense", "content": "<p>The two legs are equal, so the line must sit exactly halfway between north and east</p>"},
                {"label": "Answer", "content": "<p><strong>3.4 km, north-east</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ----------------------------------------------------------------- guided ---
OPENER_SVG = (
    '<svg viewBox="0 0 440 180" role="img" aria-label="A straight path measuring six centimetres drawn above a scale bar two centimetres long labelled one kilometre">'
    '<rect x="0" y="0" width="440" height="180" fill="#faf8f5"/>'
    '<line x1="40" y1="55" x2="280" y2="55" stroke="#8a4b2f" stroke-width="4"/>'
    '<circle cx="40" cy="55" r="5" fill="#8a4b2f"/><circle cx="280" cy="55" r="5" fill="#8a4b2f"/>'
    '<text x="40" y="38" font-size="13" fill="#2d2a26">The path measures 6 cm on the map</text>'
    '<line x1="40" y1="115" x2="120" y2="115" stroke="#2d2a26" stroke-width="4"/>'
    '<line x1="40" y1="107" x2="40" y2="123" stroke="#2d2a26" stroke-width="2"/>'
    '<line x1="120" y1="107" x2="120" y2="123" stroke="#2d2a26" stroke-width="2"/>'
    '<text x="40" y="145" font-size="13" fill="#2d2a26">Scale bar: this 2 cm length stands for 1 km</text>'
    '<text x="300" y="120" font-size="12" fill="#6b6257">Same map, same scale</text>'
    '</svg>'
)

BRONZE_TEACH_SVG = (
    '<svg viewBox="0 0 360 215" role="img" aria-label="Grid map with eastings 32 to 36, a church between eastings 32 and 33 and a school between eastings 34 and 35, both at the same height">'
    '<rect x="0" y="0" width="360" height="215" fill="#faf8f5"/>'
    '<rect x="40" y="50" width="280" height="140" fill="#f3efe6" stroke="#8a7f6d"/>'
    '<line x1="110" y1="50" x2="110" y2="190" stroke="#8a7f6d"/>'
    '<line x1="180" y1="50" x2="180" y2="190" stroke="#8a7f6d"/>'
    '<line x1="250" y1="50" x2="250" y2="190" stroke="#8a7f6d"/>'
    '<line x1="40" y1="120" x2="320" y2="120" stroke="#8a7f6d"/>'
    '<text x="40" y="205" font-size="12" fill="#2d2a26" text-anchor="middle">32</text>'
    '<text x="110" y="205" font-size="12" fill="#2d2a26" text-anchor="middle">33</text>'
    '<text x="180" y="205" font-size="12" fill="#2d2a26" text-anchor="middle">34</text>'
    '<text x="250" y="205" font-size="12" fill="#2d2a26" text-anchor="middle">35</text>'
    '<text x="320" y="205" font-size="12" fill="#2d2a26" text-anchor="middle">36</text>'
    '<text x="30" y="124" font-size="12" fill="#2d2a26" text-anchor="end">56</text>'
    '<text x="30" y="54" font-size="12" fill="#2d2a26" text-anchor="end">57</text>'
    '<text x="30" y="194" font-size="12" fill="#2d2a26" text-anchor="end">55</text>'
    '<circle cx="75" cy="85" r="5" fill="#8a4b2f"/>'
    '<text x="84" y="89" font-size="12" fill="#2d2a26">Church</text>'
    '<rect x="210" y="80" width="10" height="10" fill="#4a6b52"/>'
    '<text x="225" y="89" font-size="12" fill="#2d2a26">School</text>'
    '<text x="40" y="34" font-size="12" fill="#6b6257">Each grid square is 1 km. Scale: 2 cm stands for 1 km.</text>'
    '<text x="335" y="70" font-size="12" fill="#2d2a26">N</text>'
    '<line x1="339" y1="95" x2="339" y2="75" stroke="#2d2a26" stroke-width="2"/>'
    '<polygon points="339,70 335,79 343,79" fill="#2d2a26"/>'
    '</svg>'
)

SILVER_TEACH_SVG = (
    '<svg viewBox="0 0 340 215" role="img" aria-label="Grid map with eastings 44 to 47, a village in the square east of 46 and a windmill higher up and to the left in the square east of 44">'
    '<rect x="0" y="0" width="340" height="215" fill="#faf8f5"/>'
    '<rect x="50" y="50" width="210" height="140" fill="#f3efe6" stroke="#8a7f6d"/>'
    '<line x1="120" y1="50" x2="120" y2="190" stroke="#8a7f6d"/>'
    '<line x1="190" y1="50" x2="190" y2="190" stroke="#8a7f6d"/>'
    '<line x1="50" y1="120" x2="260" y2="120" stroke="#8a7f6d"/>'
    '<text x="50" y="205" font-size="12" fill="#2d2a26" text-anchor="middle">44</text>'
    '<text x="120" y="205" font-size="12" fill="#2d2a26" text-anchor="middle">45</text>'
    '<text x="190" y="205" font-size="12" fill="#2d2a26" text-anchor="middle">46</text>'
    '<text x="260" y="205" font-size="12" fill="#2d2a26" text-anchor="middle">47</text>'
    '<text x="40" y="194" font-size="12" fill="#2d2a26" text-anchor="end">21</text>'
    '<text x="40" y="124" font-size="12" fill="#2d2a26" text-anchor="end">22</text>'
    '<text x="40" y="54" font-size="12" fill="#2d2a26" text-anchor="end">23</text>'
    '<circle cx="225" cy="155" r="5" fill="#8a4b2f"/>'
    '<text x="180" y="175" font-size="12" fill="#2d2a26">Village</text>'
    '<polygon points="85,78 79,92 91,92" fill="#4a6b52"/>'
    '<text x="60" y="70" font-size="12" fill="#2d2a26">Windmill</text>'
    '<text x="290" y="70" font-size="12" fill="#2d2a26">N</text>'
    '<line x1="294" y1="95" x2="294" y2="75" stroke="#2d2a26" stroke-width="2"/>'
    '<polygon points="294,70 290,79 298,79" fill="#2d2a26"/>'
    '</svg>'
)

GOLD_TEACH_SVG = (
    '<svg viewBox="0 0 320 275" role="img" aria-label="Grid map with eastings 21 to 24 and northings 56 to 59, point A in the square east of 21 and north of 56, point B in the square east of 23 and north of 58">'
    '<rect x="0" y="0" width="320" height="275" fill="#faf8f5"/>'
    '<rect x="50" y="20" width="210" height="210" fill="#f3efe6" stroke="#8a7f6d"/>'
    '<line x1="120" y1="20" x2="120" y2="230" stroke="#8a7f6d"/>'
    '<line x1="190" y1="20" x2="190" y2="230" stroke="#8a7f6d"/>'
    '<line x1="50" y1="160" x2="260" y2="160" stroke="#8a7f6d"/>'
    '<line x1="50" y1="90" x2="260" y2="90" stroke="#8a7f6d"/>'
    '<text x="50" y="248" font-size="12" fill="#2d2a26" text-anchor="middle">21</text>'
    '<text x="120" y="248" font-size="12" fill="#2d2a26" text-anchor="middle">22</text>'
    '<text x="190" y="248" font-size="12" fill="#2d2a26" text-anchor="middle">23</text>'
    '<text x="260" y="248" font-size="12" fill="#2d2a26" text-anchor="middle">24</text>'
    '<text x="40" y="234" font-size="12" fill="#2d2a26" text-anchor="end">56</text>'
    '<text x="40" y="164" font-size="12" fill="#2d2a26" text-anchor="end">57</text>'
    '<text x="40" y="94" font-size="12" fill="#2d2a26" text-anchor="end">58</text>'
    '<text x="40" y="24" font-size="12" fill="#2d2a26" text-anchor="end">59</text>'
    '<circle cx="78" cy="188" r="5" fill="#8a4b2f"/>'
    '<text x="88" y="192" font-size="12" fill="#2d2a26">A at 214566</text>'
    '<circle cx="204" cy="62" r="5" fill="#8a4b2f"/>'
    '<text x="150" y="52" font-size="12" fill="#2d2a26">B at 232584</text>'
    '<line x1="78" y1="188" x2="204" y2="62" stroke="#8a4b2f" stroke-width="2" stroke-dasharray="5 4"/>'
    '<text x="290" y="40" font-size="12" fill="#2d2a26">N</text>'
    '<line x1="294" y1="65" x2="294" y2="45" stroke="#2d2a26" stroke-width="2"/>'
    '<polygon points="294,40 290,49 298,49" fill="#2d2a26"/>'
    '</svg>'
)

pd["guided"] = {
    "opener": {
        "display": "<p>Here is a straight path drawn on a map, with the map's scale bar underneath it.</p>" + OPENER_SVG,
        "steps": [
            {"say": "No method yet. Just count."},
            {"pre": "The scale bar is 2 cm long and stands for 1 km. Type how many whole 2 cm lengths fit along the 6 cm path.",
             "answer": 3,
             "hint": "Count along the path in twos: 2 cm, 4 cm, and so on until you reach the end.",
             "done": "Each of those lengths is 1 km on the ground, so counting them counts kilometres."},
            {"pre": "Type the real length of the path, in km.",
             "answer": 3,
             "hint": "Every 2 cm length you counted is worth 1 km."},
            {"pre": "A second path on the same map measures 5 cm. Type its real length, in km.",
             "answer": 2.5,
             "hint": "5 cm is two full 2 cm lengths with half of another one left over.",
             "done": "You halved the centimetres without being told to. That is the scale doing its job."},
            {"say": "<strong>That is scale conversion.</strong> Every map tells you how many centimetres stand for 1 km. Measure in centimetres, divide by that number, and you have the real distance. This lesson does exactly that, then adds direction: which way you would walk to get from one place to the other."},
        ],
    },
    "teach": {
        "bronze": {
            "display": "<p>A church and a school on a grid map. Each grid square is 1 km across, and 2 cm on this map stands for 1 km.</p>" + BRONZE_TEACH_SVG,
            "steps": [
                {"say": "Locate both features first. Measuring comes second."},
                {"pre": "The eastings are printed along the bottom. Type the easting of the line immediately to the left of the church.",
                 "answer": 32,
                 "hint": "Look straight down from the church to the numbers on the bottom edge.",
                 "done": "Locating first is the habit. Never measure before you know where both places are."},
                {"pre": "Type the easting of the line immediately to the left of the school.",
                 "answer": 34,
                 "hint": "Look straight down from the school to the bottom edge."},
                {"pre": "The two are at the same height on the map. Type how many whole grid squares apart they are from side to side.",
                 "answer": 2,
                 "hint": "Take the smaller easting away from the larger one.",
                 "phase": "substitute"},
                {"pre": "Each grid square is 1 km across. Type the distance between them, in km.",
                 "answer": 2,
                 "hint": "One square across is one kilometre across."},
                {"pre": "Check with the scale: 2 cm stands for 1 km here. Type the ruler reading, in centimetres, you would expect between the two symbols.",
                 "answer": 4,
                 "hint": "Multiply your kilometre answer by the centimetres that stand for 1 km.",
                 "done": "Counting squares and reading the ruler give the same distance, so either route can be used to check the other."},
                {"say": "<strong>Bronze move:</strong> count squares or read the ruler, then convert once with the scale."},
            ],
        },
        "silver": {
            "display": "<p>A village and a windmill on a grid map. Which direction is the windmill from the village?</p>" + SILVER_TEACH_SVG,
            "steps": [
                {"say": "The direction runs from the village, because that is where you are standing."},
                {"pre": "Type the easting of the line immediately to the left of the village.",
                 "answer": 46,
                 "hint": "Look straight down from the village to the numbers on the bottom edge.",
                 "done": "Pinning both places to a square is the set-up for every direction question."},
                {"pre": "Type the easting of the line immediately to the left of the windmill.",
                 "answer": 44,
                 "hint": "Look straight down from the windmill to the bottom edge."},
                {"pre": "A smaller easting means further west. Type 1 if the windmill is higher up the map than the village, 2 if it is lower down.",
                 "answer": 1,
                 "hint": "Compare how far up the page each symbol sits.",
                 "phase": "substitute"},
                {"pre": "Up the map is north and left is west. Using %s, type the number for the direction of the windmill from the village." % COMPASS,
                 "answer": 8,
                 "hint": "Put west and north together, then find that pair in the list."},
                {"pre": "Check by turning round: from the windmill, the village lies in the exact opposite direction. Type its number from the same list.",
                 "answer": 4,
                 "hint": "Opposites sit four places apart on that list.",
                 "done": "Your two answers are four apart, which is what turning through half a circle must give. If they were not, one of them would be wrong."},
                {"say": "<strong>Silver move:</strong> use the grid to prove east or west, then read up or down off the page, and combine them into one of the in-between points."},
            ],
        },
        "gold": {
            "display": "<p>Two points given as six-figure references. Find the straight-line distance from A to B, and the direction walked.</p>" + GOLD_TEACH_SVG,
            "steps": [
                {"say": "Six-figure references carry the distance inside them, so no ruler is needed here."},
                {"pre": "Point A sits in the square with easting 21 and northing 56. Type the easting of the square that B sits in.",
                 "answer": 23,
                 "hint": "Read the number on the vertical line immediately to the left of B.",
                 "done": "Both points are now placed on the grid, which is what makes the arithmetic mean something."},
                {"pre": "Type the northing of the square that B sits in.",
                 "answer": 58,
                 "hint": "Read the number on the horizontal line immediately below B."},
                {"pre": "A is 214566 and B is 232584. Each step in the third digit is 100 m. Type how far east B is from A, in metres.",
                 "answer": 1800,
                 "hint": "Take 214 from 232, then multiply by 100.",
                 "phase": "substitute"},
                {"pre": "Type how far north B is from A, in metres.",
                 "answer": 1800,
                 "hint": "Take 566 from 584, then multiply by 100."},
                {"pre": "Both legs are 1.8 km. Type 1.8 squared added to 1.8 squared.",
                 "answer": 6.48,
                 "hint": "Square one leg, then double it, since both legs match."},
                {"pre": "The square root of that total is just over 2.5. Type the distance in km, to the nearest 0.5 km.",
                 "answer": 2.5,
                 "hint": "Decide whether a value just above 2.5 is closer to 2.5 or to 3.0."},
                {"pre": "Check the direction. Using %s, type the number for the direction from A to B." % COMPASS,
                 "answer": 2,
                 "hint": "B is east of A and north of A by the same amount.",
                 "done": "Equal legs east and north put the line exactly halfway between north and east, and the straight line is longer than either leg, which is what Pythagoras must give."},
                {"say": "<strong>Gold move:</strong> turn the reference digits into metres, use Pythagoras for the distance, then read the direction off the same two differences."},
            ],
        },
    },
}

# ------------------------------------------------------------ method card ---
pd["method_card"] = {
    "title": "Distance & Direction on a Map",
    "steps": [
        "Find both places first, the starting one before the finishing one",
        "Distance: measure the straight line, then convert with the scale",
        "Direction: run it from the place named first to the place named second",
        "Up the map is north, right is east",
    ],
    "content": (
        "<p><strong>Distance.</strong> One grid square on these maps is 1 km across. For a straight line, "
        "measure it with the ruler, then divide the centimetres by the number of centimetres that stand for "
        "1 km at that scale. Round the way the question asks.</p>"
        "<p><strong>Pythagoras.</strong> If you know how far east and how far north the line runs, square both, "
        "add them, then take the square root. Six-figure references give those two legs without any measuring: "
        "each step in the third digit is 100 m.</p>"
        "<p><strong>Direction.</strong> Stand at the first place named and face the second. Up is north, down is "
        "south, right is east, left is west, and the points between are NE, SE, SW and NW. Swapping the two "
        "places reverses the direction.</p>"
    ),
    "example": (
        "<p><strong>Question:</strong> A path measures 4 cm on a map where 2 cm stands for 1 km. It runs up the "
        "map and to the right. How long is it, and which way does it head?</p>"
        "<p>4 ÷ 2 = 2 km. Up is north and right is east, so it heads north-east.</p>"
        "<p><strong>Answer:</strong> 2 km, NE.</p>"
    ),
}

# ----------------------------------------- de-em-dash preserved text fields ---
def dedash(obj):
    if isinstance(obj, dict):
        return {k: dedash(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [dedash(v) for v in obj]
    if isinstance(obj, str):
        return obj.replace(" — ", ": ").replace("—", ":")
    return obj

pd["worked_examples"] = dedash(pd["worked_examples"])
pd["exam_context"] = dedash(pd["exam_context"])

out = os.path.join(HERE, "lesson_L12.json")
with io.open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("written", out)
