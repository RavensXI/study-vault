# -*- coding: utf-8 -*-
"""Targeted checker repairs for Geography Skills L03 (Scatter Graphs & Correlation)."""
import json, io, os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "_rp_L03_live.json")
OUT = os.path.join(HERE, "lesson_L03.json")

pd = json.load(io.open(SRC, encoding="utf-8"))
pb = pd["problem_bank"]

log = []

def setv(obj, key, new, label):
    old = obj.get(key)
    assert old != new, label + " (no change)"
    obj[key] = new
    log.append({"path": label, "old": old, "new": new})

# ---------------------------------------------------------------- FAIL 1
# gold[3] display claimed "the same scatter graph" with no chart present.
g3 = pb["gold"][3]
setv(g3, "display",
     "Two students each draw a line of best fit through the same set of 10 plotted "
     "points. Student A's line ends up with 5 points above it and 5 below. Student B's "
     "line is drawn straight from the first point to the last point. Whose line is more "
     "appropriate?",
     "gold[3].display")

# ---------------------------------------------------------------- NIT 2
# silver[1]: display asked for a line of best fit but the stored answer (and the
# walk, and the hint) use the neighbouring-points method. A true line of best fit
# over these 10 points gives 38.15, so the wording is now matched to the method.
s1 = pb["silver"][1]
setv(s1, "display",
     "The scatter graph shows birth rate and infant mortality for 10 countries. No "
     "country has a birth rate of exactly 25, so estimate the infant mortality rate at "
     "a birth rate of 25 using the plotted points either side of it. Give your answer "
     "to the nearest whole number.",
     "silver[1].display")

# ---------------------------------------------------------------- NIT 3
# bronze[1] walk asserted "the plotted points" on a problem carrying no figure.
b1 = pb["bronze"][1]
setv(b1["guided_steps"][0], "say",
     "Picture the graph being described: one point at 0 m with 15 °C, and another at "
     "2,000 m with 3 °C.",
     "bronze[1].guided_steps[0].say")

# ---------------------------------------------------------------- NIT 4
# Direction-naming hints handed over the answer instead of unsticking it.
setv(pd["guided"]["teach"]["bronze"]["steps"][5], "hint",
     "Compare the temperature you read at the left hand end with the one at the right "
     "hand end.",
     "guided.teach.bronze.steps[5].hint")
setv(b1["guided_steps"][2], "hint",
     "Look back at the two temperatures you just used and decide which end is higher.",
     "bronze[1].guided_steps[2].hint")
setv(pb["bronze"][4]["guided_steps"][2], "hint",
     "Look at the two changes you just worked out and decide whether each one was a "
     "rise or a fall.",
     "bronze[4].guided_steps[2].hint")

# ---------------------------------------------------------------- NIT 5
# Five multiple-choice walks ended on an elimination box; add the closing
# say-step that names the surviving option, matching the rest of the lesson.
CLOSERS = [
    (("bronze", 6),
     "The pair still standing is the one whose two measurements have no physical "
     "connection at all. Choose that pair."),
    (("silver", 2),
     "One explanation is left standing: a highly developed country that generates its "
     "energy without burning much fossil fuel. Choose that option."),
    (("silver", 4),
     "One explanation is left standing: land close to the centre that is used for "
     "something other than housing. Choose that option."),
    (("silver", 6),
     "One option is left standing: the prediction sits outside the range anyone "
     "measured. Choose that option."),
    (("gold", 3),
     "One line is answerable to all ten points rather than just two. Choose that "
     "option."),
]
for (tier, idx), say in CLOSERS:
    steps = pb[tier][idx]["guided_steps"]
    assert steps[-1].get("answer") is not None, (tier, idx)
    steps.append({"say": say})
    log.append({"path": "%s[%d].guided_steps[+]" % (tier, idx),
                "old": None, "new": say})

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("edits:", len(log))
for e in log:
    print(" -", e["path"])
