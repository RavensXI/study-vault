# -*- coding: utf-8 -*-
import json, io, os

HERE = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_geo_guided"
src = os.path.join(HERE, "_rp9_live.json")
dst = os.path.join(HERE, "lesson_L09.json")
pd = json.load(io.open(src, encoding="utf-8"))
pb = pd["problem_bank"]
changes = []


def rec(path, what, old, new):
    changes.append({"path": path, "what": what, "old": old, "new": new})


# ---------------------------------------------------------------- FAIL 1
# bronze[0].misconceptions[1] : label-offset story cannot produce Glasgow.
m = pb["bronze"][0]["misconceptions"][1]
old = dict(m)
m["pattern"] = "size_misjudged"
m["message"] = ("That circle is one of the narrower ones among your four options. "
                "Judge each option by the width actually drawn on the map, not by "
                "how well known the city is.")
rec("bronze[0].misconceptions[1]", "wrong-diagnosis message replaced (label swap cannot yield this option)",
    old, dict(m))

# ---------------------------------------------------------------- NIT 3
m0 = pb["bronze"][0]["misconceptions"][0]
old = m0["message"]
m0["message"] = ("That is one of the wider circles, but another circle on the map is "
                 "wider still. Compare all four options by width before you decide.")
rec("bronze[0].misconceptions[0].message", "removed soft pointer to the answer's location", old, m0["message"])

# ---------------------------------------------------------------- FAIL 2
# Key prints 15,000 / 30,000 / 60,000 under the heading "Migration (thousands/yr)".
# Boxes must not tell the student to type the printed figure when the stored
# answer is the thousands value.
s = pb["bronze"][1]["guided_steps"][3]
old = dict(s)
s["pre"] = ("The key prints 60,000 people a year beside its thickest arrow. "
            "Give that same flow in thousands.")
s["hint"] = "Convert 60,000 people into thousands."
rec("bronze[1].guided_steps[3]", "box now matches its stored answer (printed figure is in people)", old, dict(s))

s = pb["bronze"][6]["guided_steps"][2]
old = dict(s)
s["pre"] = ("Look at the key. Its thickest arrow is printed as 60,000 people a year. "
            "Give that flow in thousands.")
s["hint"] = "Convert 60,000 people into thousands."
rec("bronze[6].guided_steps[2]", "box now matches its stored answer (printed figure is in people)", old, dict(s))

s = pb["bronze"][6]["guided_steps"][3]
old = dict(s)
s["pre"] = ("Birmingham's arrow matches that widest key arrow. Leeds' arrow matches the "
            "middle key arrow, which is printed as 30,000 people a year. Give that flow "
            "in thousands.")
s["hint"] = "Convert 30,000 people into thousands."
rec("bronze[6].guided_steps[3]", "box now matches its stored answer (printed figure is in people)", old, dict(s))

# ---------------------------------------------------------------- NIT 4
p = pb["silver"][2]
old = p["hint"]
p["hint"] = ("Study the cluster of symbols on the map itself, decide what makes it awkward "
             "to read, then test each option against what you saw.")
rec("silver[2].hint", "hint no longer restates the correct option", old, p["hint"])

p = pb["gold"][3]
old = p["hint"]
p["hint"] = ("Gather two pieces of evidence from the map first, then reject any statement "
             "the map itself contradicts.")
rec("gold[3].hint", "hint no longer restates the correct option", old, p["hint"])

# ---------------------------------------------------------------- NIT 7
# gold[2] sits on the flow line map, which draws no circles at all.
s = pb["gold"][2]["guided_steps"][3]
old = dict(s)
s["pre"] = ("Follow each red arrow to its point. How many of the two land on a place "
            "away from the capital?")
s["hint"] = "Trace the pointed end of each red arrow and see which place it finishes on."
rec("gold[2].guided_steps[3]", "step referred to circles, which this map does not draw", old, dict(s))

# ---------------------------------------------------------------- NIT 5
# tier_guide examples were number-for-number copies of the teach walks.
tg = pd["tier_guides"]

old = json.loads(json.dumps(tg["bronze"]["example"]))
tg["bronze"]["example"] = {
    "question": ("A key shows circles for 300 thousand and 1,200 thousand people. "
                 "Thornby's circle is the same size as the smaller key circle. "
                 "What is Thornby's population?"),
    "steps": [
        {"label": "Find the key",
         "content": "<p>The key gives two reference circles: 300 thousand and 1,200 thousand.</p>"},
        {"label": "Match the symbol",
         "content": "<p>Thornby's circle is the same width as the 300 thousand circle.</p>"},
        {"label": "Check",
         "content": "<p>Thornby's circle is the narrower of the two key circles, so its value must be the smaller key value, not the larger one.</p>"},
        {"label": "Answer",
         "content": "<p><strong>300,000 people</strong></p>",
         "isAnswer": True, "is_answer": True},
    ],
}
rec("tier_guides.bronze.example", "fresh example so the card is not a copy of the bronze teach walk",
    old, tg["bronze"]["example"])

old = json.loads(json.dumps(tg["silver"]["example"]))
tg["silver"]["example"] = {
    "question": ("A key circle for 400 thousand people is 12 mm across. Netherby's circle "
                 "is 24 mm across. Estimate Netherby's population."),
    "steps": [
        {"label": "Divide the diameters",
         "content": "<p>24 mm ÷ 12 mm = 2, so Netherby's circle is 2 times as wide.</p>"},
        {"label": "Square it for area",
         "content": "<p>2² = 4, so the circle covers 4 times the area.</p>"},
        {"label": "Scale the key value",
         "content": "<p>4 × 400 thousand = 1,600 thousand.</p>"},
        {"label": "Check",
         "content": "<p>1,600 ÷ 400 = 4, which returns the area factor, so the squaring was applied once and the right way round.</p>"},
        {"label": "Answer",
         "content": "<p><strong>About 1,600,000 people</strong></p>",
         "isAnswer": True, "is_answer": True},
    ],
}
rec("tier_guides.silver.example", "fresh example so the card is not a copy of the silver teach walk",
    old, tg["silver"]["example"])

old = json.loads(json.dumps(tg["gold"]["example"]))
tg["gold"]["example"] = {
    "question": ("Two arrows point into Kesthaven, worth 35 and 20 thousand a year. Two "
                 "arrows point out, worth 12 and 8 thousand a year. Find the net gain."),
    "steps": [
        {"label": "Total the inward flows",
         "content": "<p>35 + 20 = 55 thousand a year.</p>"},
        {"label": "Total the outward flows",
         "content": "<p>12 + 8 = 20 thousand a year.</p>"},
        {"label": "Subtract",
         "content": "<p>55 − 20 = 35 thousand a year.</p>"},
        {"label": "Check",
         "content": "<p>35 + 20 = 55, which gives the inward total back, so the subtraction went the right way round.</p>"},
        {"label": "Answer",
         "content": "<p><strong>A net gain of 35,000 people a year</strong></p>",
         "isAnswer": True, "is_answer": True},
    ],
}
rec("tier_guides.gold.example", "fresh example so the card is not a copy of the gold teach walk",
    old, tg["gold"]["example"])

json.dump(pd, io.open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(changes, io.open(os.path.join(HERE, "_rp9_changes_raw.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("edits:", len(changes))
