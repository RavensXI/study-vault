# -*- coding: utf-8 -*-
"""L12 (Distance & Direction) checker-repair. Minimal targeted edits only."""
import json, io, os

HERE = os.path.dirname(os.path.abspath(__file__))
pd = json.load(io.open(os.path.join(HERE, "_rp12_live.json"), encoding="utf-8"))
pb = pd["problem_bank"]
B, S, G = pb["bronze"], pb["silver"], pb["gold"]
changes = []


def note(path, what, old, new):
    changes.append({"path": path, "what": what, "old": old, "new": new})


# ---------------------------------------------------------------- exam_context
old = pd["exam_context"]["marks"]
pd["exam_context"]["marks"] = ("Short answers: give the number, the unit and "
                              "the compass point exactly as the question asks.")
note("exam_context.marks", "en dash removed and mark tariff dropped (board neutrality)",
     old, pd["exam_context"]["marks"])

# ---------------------------------------------------------------- bronze[4]
p = B[4]
old = p["misconceptions"][1]["expect"]
p["misconceptions"][1]["expect"] = 5
note("bronze[4].misconceptions[1].expect",
     "Hare Runs (x~536) is slightly WEST of the roundabout (x~611), so inflating the "
     "sideways shift gives SW (index 5), not SE",
     old, 5)

# ---------------------------------------------------------------- bronze[5]
# dorset-coast-z16: Kingston (1160,900) to West Orchard Farm (150,137) = 1266 px.
# Ruler config pxPerKm 719, cmPerKm 4  ->  1266/719*4 = 7.04 cm  -> reads 7, not 8.
p = B[5]
old = p["misconceptions"][0]["expect"]
p["misconceptions"][0]["expect"] = 7
note("bronze[5].misconceptions[0].expect", "ruler reading is 7 cm, not 8", old, 7)
old = p["misconceptions"][1]["expect"]
p["misconceptions"][1]["expect"] = 3.5
note("bronze[5].misconceptions[1].expect", "dividing 7 by 2 instead of 4 gives 3.5", old, 3.5)

gs = p["guided_steps"]
old = gs[2]["answer"]
gs[2]["answer"] = 7
note("bronze[5].guided_steps[2].answer",
     "measured span is 1266 px = 7.04 cm on this problem's ruler, so an honest reading is 7",
     old, 7)
old = json.loads(json.dumps(gs[3]))
gs[3] = {
    "pre": "On this map 4 cm stands for 1 km. Type your reading divided by 4.",
    "hint": "Divide your centimetre reading by 4.",
    "done": "That is the raw distance in kilometres, before any rounding.",
    "answer": 1.75,
}
note("bronze[5].guided_steps[3]", "7 divided by 4 is 1.75, so the box now asks for the raw value",
     old, gs[3])
old = json.loads(json.dumps(gs[4]))
gs[4] = {
    "pre": "The question asks for the nearest 0.5 km. Type the distance in km.",
    "hint": "Decide whether your figure is nearer 1.5 km or nearer 2.0 km.",
    "answer": 2,
}
note("bronze[5].guided_steps[4]", "rounding step replaces the old multiply-back check", old, gs[4])
gs.append({
    "pre": "Check against the grid: type how many vertical grid lines fall between "
           "Kingston and West Orchard Farm.",
    "hint": "Count the blue vertical lines your measuring line crosses.",
    "done": "One easting line falls between them, so they are at least 1 km apart from "
            "east to west, and a diagonal line has to be longer still.",
    "answer": 1,
})
note("bronze[5].guided_steps[5]", "new closing check that uses the grid on the stimulus",
     None, gs[5])

# ---------------------------------------------------------------- silver[0]
# ribble-valley-z15: Scale Hall (334,1067) to Newton (985,1037) crosses eastings 47 and 48.
p = S[0]
old = json.loads(json.dumps(p["guided_steps"][4]))
p["guided_steps"][4] = {
    "pre": "Check against the grid: type how many vertical grid lines your line crosses "
           "between Scale Hall and Newton.",
    "hint": "Count the blue vertical lines the measuring line passes over.",
    "done": "Crossing two easting lines means the line spans more than 1 km and less than "
            "3 km, which sits comfortably with the ruler reading.",
    "answer": 2,
}
note("silver[0].guided_steps[4]",
     "old box asked for whole grid squares spanned, which is 1 by the strict reading and 3 by "
     "the touched reading; counting lines crossed is unambiguous and still gives 2",
     old, p["guided_steps"][4])

# ---------------------------------------------------------------- silver[2]
p = S[2]
old = p["misconceptions"][1]["expect"]
p["misconceptions"][1]["expect"] = 5
note("silver[2].misconceptions[1].expect",
     "Castleton (x~788) is WEST of Riding House Farm (x~899), so inflating the sideways "
     "shift gives SW (index 5), not SE",
     old, 5)

# ---------------------------------------------------------------- silver[3]
# ribble-valley-z16 (grid 718.5 px/km): Hasty Brow Road over Lancaster Canal (127,225)
# to the museum symbol (1272,1210) = 1510 px = 2.10 km. Ruler reads 8.4 cm, not 16.
p = S[3]
old = p["solutions"]
p["solutions"] = [2000]
note("silver[3].solutions",
     "stored 4000 m is geometrically impossible: the whole sheet is only 2.14 km wide, and "
     "the measured span is 1510 px = 2.10 km",
     old, [2000])
old = p["misconceptions"][0]["expect"]
p["misconceptions"][0]["expect"] = 2
note("silver[3].misconceptions[0].expect", "stopping at kilometres now gives 2", old, 2)
old = p["misconceptions"][1]["expect"]
p["misconceptions"][1]["expect"] = 8000
note("silver[3].misconceptions[1].expect", "reading 8 cm turned straight into metres gives 8000",
     old, 8000)
gs = p["guided_steps"]
for idx, new in ((2, 8), (3, 2), (4, 2000), (5, 2)):
    old = gs[idx]["answer"]
    gs[idx]["answer"] = new
    note("silver[3].guided_steps[%d].answer" % idx,
         "walk rebased on the real measurement (8 cm, 2 km, 2000 m)", old, new)

# ---------------------------------------------------------------- silver[4]
# yorkshire-dales-z16 labels the fell "Cow Close Fell". The old name appears nowhere.
p = S[4]
def fix_name(s):
    return s.replace("How Close Fell", "Cow Close Fell")
old = p["display"]
p["display"] = fix_name(p["display"])
note("silver[4].display", "map labels this fell Cow Close Fell", old, p["display"])
old = p["hint"]
p["hint"] = fix_name(p["hint"])
note("silver[4].hint", "map labels this fell Cow Close Fell", old, p["hint"])
for i, st in enumerate(p["guided_steps"]):
    for k in ("pre", "say", "done", "hint"):
        if k in st and isinstance(st[k], str) and "How Close Fell" in st[k]:
            o = st[k]
            st[k] = fix_name(st[k])
            note("silver[4].guided_steps[%d].%s" % (i, k), "map labels this fell Cow Close Fell",
                 o, st[k])

# ---------------------------------------------------------------- silver[5]
p = S[5]
old = p["misconceptions"][1]["expect"]
p["misconceptions"][1]["expect"] = 3
note("silver[5].misconceptions[1].expect",
     "Barham Farm House (1233,650) is LOWER than Willwood House (450,494), so wrongly "
     "promoting the vertical gap gives SE (index 3), not NE",
     old, 3)

# ---------------------------------------------------------------- gold[0]
p = G[0]
gs = p["guided_steps"]
locate = {
    "pre": "Start on the map. Go along the bottom edge to the line labelled 47, then up the "
           "side to the line labelled 63: the first house sits in that square. Type the "
           "easting of the line along the right-hand edge of that square.",
    "hint": "Eastings go up by 1 for every square you move right.",
    "done": "Along the corridor then up the stairs. Landing on the square first is what makes "
            "the digits mean something.",
    "answer": 48,
}
gs.insert(1, locate)
note("gold[0].guided_steps[1]",
     "walk opened on digit-splitting and never used the map; a locating box now comes first",
     None, locate)

# ---------------------------------------------------------------- gold[2]
# lake-district-z15 has no lake at the top-centre (all open water is bottom-centre-left).
# Re-anchored on two features that are genuinely there; measured span 1218 px = 6.8 cm,
# so the stored answer of 3.5 km is preserved exactly.
p = G[2]
old = p["display"]
p["display"] = ("What is the straight-line distance from <strong>Town Head Cottages</strong> "
                "in the north-west of the map to <strong>Nab Scar</strong> in the south-east? "
                "Give your answer in km to the nearest 0.5 km.")
note("gold[2].display",
     "there is no lake at the top-centre of this sheet; re-anchored on two named features that "
     "are on the map, chosen so the stored 3.5 km answer still holds",
     old, p["display"])
old = p["hint"]
p["hint"] = "Find both named places first, then measure the straight line and convert it."
note("gold[2].hint", "hint referred to the lake that is not there", old, p["hint"])
gs = p["guided_steps"]
old = json.loads(json.dumps(gs[1]))
gs[1] = {
    "pre": "Type 1 if Nab Scar is lower down the map than Town Head Cottages, 2 if it is higher up.",
    "hint": "One is named as being in the north-west and the other in the south-east.",
    "done": "North-west corner to south-east corner is a long diagonal, so expect one of the "
            "bigger distances on this map.",
    "answer": 1,
}
note("gold[2].guided_steps[1]", "step asserted the lake was higher than the settlement", old, gs[1])
old = gs[2]["pre"]
gs[2]["pre"] = ("Drag the ruler from Town Head Cottages to Nab Scar. Type the reading in "
                "centimetres, to the nearest centimetre.")
note("gold[2].guided_steps[2].pre", "endpoints renamed to the real features (reading stays 7 cm)",
     old, gs[2]["pre"])

# ---------------------------------------------------------------- gold[4]
# ribble-valley-z16 (correctly calibrated at 719 px/km): the A6 enters at x=774,y=0 and
# leaves at x=792,y=1279, a span of 1279 px = 7.1 cm. Stored 2 km survives (1.75 rounds up).
p = G[4]
old = p["misconceptions"][0]["expect"]
p["misconceptions"][0]["expect"] = 7
note("gold[4].misconceptions[0].expect", "ruler reading is 7 cm, not 8", old, 7)
old = p["misconceptions"][1]["expect"]
p["misconceptions"][1]["expect"] = 3.5
note("gold[4].misconceptions[1].expect", "dividing 7 by 2 instead of 4 gives 3.5", old, 3.5)
gs = p["guided_steps"]
old = gs[2]["answer"]
gs[2]["answer"] = 7
note("gold[4].guided_steps[2].answer",
     "the A6 spans 1279 px = 7.1 cm on this ruler, so a reading of 8 can never be shown",
     old, 7)
old = json.loads(json.dumps(gs[3]))
gs[3] = {
    "pre": "On this map 4 cm stands for 1 km. Type your reading divided by 4.",
    "hint": "Divide your centimetre reading by 4.",
    "done": "That is the raw distance in kilometres, before any rounding.",
    "answer": 1.75,
}
note("gold[4].guided_steps[3]", "7 divided by 4 is 1.75", old, gs[3])
old = json.loads(json.dumps(gs[4]))
gs[4] = {
    "pre": "The question asks for the nearest 0.5 km. Type the distance in km.",
    "hint": "Decide whether your figure is nearer 1.5 km or nearer 2.0 km.",
    "answer": 2,
}
note("gold[4].guided_steps[4]", "rounding step replaces the old multiply-back check", old, gs[4])
gs.append({
    "pre": "Check against the grid: type how many horizontal grid lines the A6 crosses on its "
           "way down the map.",
    "hint": "Count the blue horizontal lines the pink road passes over.",
    "done": "It crosses two northing lines, so the road covers one whole kilometre square plus "
            "part of the ones above and below, which is the size of answer you got.",
    "answer": 2,
})
note("gold[4].guided_steps[5]", "new closing check that uses the grid on the stimulus",
     None, gs[5])

# ---------------------------------------------------------------- write
json.dump(pd, io.open(os.path.join(HERE, "lesson_L12.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
json.dump(changes, io.open(os.path.join(HERE, "_rp12_changes_raw.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("edits:", len(changes))
