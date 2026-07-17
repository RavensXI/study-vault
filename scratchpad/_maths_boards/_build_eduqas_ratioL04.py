# -*- coding: utf-8 -*-
"""Build guided conversion for maths-eduqas ratio-proportion-L04 (Direct & Inverse
Proportion). Keeps MC input types (board convention, matches shipped L03).
Adds hints, honest misconception expects (distractor index), tier_guides,
guided opener/teach, one chart (g1). Fixes em dashes."""
import json, io

SRC = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_live_eduqas_ratioL04.json"
OUT = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-eduqas_ratio-proportion-L04.json"

pd = json.load(io.open(SRC, encoding="utf-8"))
pb = pd["problem_bank"]

# ---- hints (plain text, one sentence, no LaTeX/HTML/em dash) ----
HINTS = {
 ("bronze",0): "Find k by dividing y by x (10 divided by 2), then multiply k by 6.",
 ("bronze",1): "Work out k = 15 divided by 5, then multiply by 9.",
 ("bronze",2): "Find the cost of one pen first, then multiply by 10.",
 ("bronze",3): "Find k = 24 divided by 4, then divide 42 by k to get x.",
 ("bronze",4): "Direct proportion is a straight line that passes through the origin (0, 0).",
 ("bronze",5): "Fewer workers means more time: multiply 6 by 12 for the fixed total, then divide by 4.",
 ("bronze",6): "Inverse: multiply 3 by 12 for the constant, then divide by 6.",
 ("bronze",7): "Faster speed means less time: multiply 60 by 3 for the distance, then divide by 90.",
 ("silver",0): "Find k = y divided by x, then write the rule as y = kx.",
 ("silver",1): "Inverse: multiply 4 by 5 for k, then divide by 2.",
 ("silver",2): "More people means less time: multiply 8 by 6, then divide by 12.",
 ("silver",3): "Find k = 20 divided by 8, then multiply by 12.",
 ("silver",4): "Inverse: multiply 10 by 6 for k, then divide by 15.",
 ("silver",5): "Find k = 9 divided by 6, then divide 15 by k to get x.",
 ("silver",6): "Direct: find the stretch per newton (4.5 divided by 6), then multiply by 10.",
 ("gold",0): "Inverse: multiply 3 by 8 for the constant, then divide by 2 hours.",
 ("gold",1): "The gradient of y = kx is k, found by dividing y by x.",
 ("gold",2): "Inverse: multiply 2 by 150 for k, then divide by 50.",
 ("gold",3): "Direct proportion must pass through (0, 0), with no amount added on.",
 ("gold",4): "Inverse means the opposite effect: if x goes up, y comes down.",
}

# ---- misconceptions: expect = index of the distractor the error produces (or null) ----
def mc(check, message, expect):
    return {"check": check, "pattern": check, "message": message, "expect": expect}

MIS = {
 ("bronze",0): [mc("multiplied_given","60 is 10 × 6. First find k = 10 ÷ 2 = 5, then y = 5 × 6 = 30.",3),
                mc("wrong_k","Find k first: k = y ÷ x = 10 ÷ 2 = 5, then y = 5 × 6 = 30.",None)],
 ("bronze",1): [mc("added_difference","19 adds the change in x (15 + 4). Use the multiplier: k = 3, so y = 3 × 9 = 27.",2),
                mc("answered_k","3 is only k. Finish the job: y = k × 9 = 3 × 9 = 27.",3)],
 ("bronze",2): [mc("multiplied_total","£60 is 6 × 10. Find one pen first: 6 ÷ 4 = £1.50, then × 10 = £15.",1),
                mc("added","£16 adds 6 + 10. Use the cost of one pen (£1.50) and scale to 10.",2)],
 ("bronze",3): [mc("multiplied_by_k","252 multiplies 42 × 6. To reverse it, divide: x = 42 ÷ 6 = 7.",1),
                mc("wrong_method","Find k = 24 ÷ 4 = 6, then x = 42 ÷ k = 7.",None)],
 ("bronze",4): [mc("not_through_origin","A line crossing the y-axis at 5 is not direct proportion. Direct proportion passes through (0, 0).",3),
                mc("curve","y = kx gives a straight line, not a curve.",1)],
 ("bronze",5): [mc("used_direct","8 treats it as direct. Fewer workers means MORE time: k = 6 × 12 = 72, time = 72 ÷ 4 = 18 days.",1),
                mc("inverse_reminder","This is inverse: workers × days stays fixed at 72.",None)],
 ("bronze",6): [mc("used_direct","24 treats it as direct. Inverse: k = 3 × 12 = 36, then y = 36 ÷ 6 = 6.",1),
                mc("answered_k","36 is the constant k. Finish: y = k ÷ 6 = 6.",2)],
 ("bronze",7): [mc("used_direct","4.5 treats it as direct. Faster speed means LESS time: distance = 60 × 3 = 180, time = 180 ÷ 90 = 2 hours.",1),
                mc("inverse_reminder","Inverse: speed × time = distance = 180, which stays fixed.",None)],
 ("silver",0): [mc("multiplied","k = y ÷ x = 7.5 ÷ 3 = 2.5, not 7.5 × 3. The rule is y = 2.5x.",1),
                mc("used_inverse","This is direct (y ∝ x), so y = kx, not y = k ÷ x.",2)],
 ("silver",1): [mc("halved","2.5 halves y because x halved, but inverse does the opposite: k = 4 × 5 = 20, y = 20 ÷ 2 = 10.",1),
                mc("answered_k","20 is the constant k. Finish: y = k ÷ 2 = 10.",2)],
 ("silver",2): [mc("used_direct","9 treats it as direct. More people means less time: k = 8 × 6 = 48, time = 48 ÷ 12 = 4 hours.",1),
                mc("inverse_reminder","Inverse: people × hours = 48, which stays fixed.",None)],
 ("silver",3): [mc("added","24 adds 20 + 4. Use the multiplier: k = 20 ÷ 8 = 2.5, y = 2.5 × 12 = 30.",2),
                mc("wrong_k","Find k = 20 ÷ 8 = 2.5 first, then multiply by 12.",None)],
 ("silver",4): [mc("used_direct","£9 treats it as direct. Inverse: k = 10 × 6 = 60, C = 60 ÷ 15 = £4.",1),
                mc("multiplied","£90 is 6 × 15. Rearrange C = k ÷ n with k = 60 to get £4.",3)],
 ("silver",5): [mc("multiplied_by_k","22.5 multiplies 15 × 1.5. To find x, divide: x = 15 ÷ 1.5 = 10.",1),
                mc("wrong_rearrangement","Find k = 9 ÷ 6 = 1.5, then x = y ÷ k = 10.",None)],
 ("silver",6): [mc("added","10.5 adds 4.5 + 6. Direct: k = 4.5 ÷ 6 = 0.75 cm per N, extension = 0.75 × 10 = 7.5 cm.",1),
                mc("used_inverse","Hooke's Law is direct proportion: more force means more extension, so use y = kx.",3)],
 ("gold",0): [mc("multiplied","48 multiplies 24 × 2. To find hoses, divide: k = 3 × 8 = 24, hoses = 24 ÷ 2 = 12.",2),
              mc("used_direct","This is inverse: hoses × hours = 24, so more hoses means less time.",None)],
 ("gold",1): [mc("added","14 adds 10 + 4. The gradient is the ratio y ÷ x = 10 ÷ 4 = 2.5.",1),
              mc("multiplied","40 multiplies 10 × 4. The gradient k is y ÷ x, not the product.",3)],
 ("gold",2): [mc("used_direct","0.67 treats it as direct. Inverse: k = 2 × 150 = 300, V = 300 ÷ 50 = 6.",1),
              mc("answered_k","300 is the constant k = P × V. Finish: V = k ÷ 50 = 6.",3)],
 ("gold",3): [mc("thinks_yes_increases","It does increase with distance, but the £3 fixed charge means it is not direct proportion (it must pass through (0, 0)).",1),
              mc("thinks_straight_line","It is a straight line, but it does not pass through the origin, so it is linear, not directly proportional.",2)],
 ("gold",4): [mc("thinks_direct","Doubling only doubles y in direct proportion. Inverse does the opposite, so y is halved.",1),
              mc("no_change","y and x are linked, so changing x must change y. Doubling x halves y.",2)],
}

# g3 options: strip em dashes -> commas
pb["gold"][3]["options"] = [
 "No, there is a fixed charge",
 "Yes, it increases with distance",
 "Yes, it is a straight line",
 "No, it is inverse",
]

# apply hints + misconceptions
for tier in ("bronze","silver","gold"):
    for i, p in enumerate(pb[tier]):
        p["hint"] = HINTS[(tier,i)]
        p["misconceptions"] = MIS[(tier,i)]

# g1 chart: straight line y = 2.5x through origin and (4,10)
pb["gold"][1]["chart"] = {
 "type": "scatter",
 "data": {"datasets": [{
   "type": "line",
   "label": "y = kx",
   "data": [{"x":0,"y":0},{"x":1,"y":2.5},{"x":2,"y":5},{"x":3,"y":7.5},{"x":4,"y":10}],
   "tension": 0, "fill": False,
   "borderColor": "#3b82f6", "pointRadius": 4, "pointBackgroundColor": "#3b82f6"
 }]},
 "options": {"plugins": {"legend": {"display": False}},
   "scales": {
     "x": {"min":0,"max":5,"ticks":{"stepSize":1},"grid":{"color":"rgba(128,128,128,0.2)"},"title":{"text":"x","display":True}},
     "y": {"min":0,"max":12,"ticks":{"stepSize":2},"grid":{"color":"rgba(128,128,128,0.2)"},"title":{"text":"y","display":True}}
   }}
}

# fix em dashes in worked_examples labels
for we in pd.get("worked_examples", []):
    for st in we.get("steps", []):
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ": ")

# ---- tier_guides ----
pd["tier_guides"] = {
 "bronze": {
   "title": "Bronze: find one, then scale",
   "steps": [
     "Decide the type. If more means more, it is <strong>direct</strong>. If more means less (more workers, less time), it is <strong>inverse</strong>.",
     "Direct: divide to find ONE unit, then multiply by how many you want.",
     "Inverse: multiply the pair to get the fixed total, then divide by the new amount."
   ],
   "example": {
     "question": "6 pens cost £9. Find the cost of 10 pens.",
     "steps": [
       {"label":"Type","content":"<p>More pens, more money: direct proportion.</p>"},
       {"label":"One unit","content":"<p>One pen \\(= 9 \\div 6 = \\pounds1.50\\).</p>"},
       {"label":"Scale","content":"<p>Ten pens \\(= 1.5 \\times 10 = \\pounds15\\).</p>"},
       {"label":"Check","content":"<p>\\(15 \\div 10 = \\pounds1.50\\) each ✓</p>"},
       {"label":"Answer","content":"<p><strong>£15</strong></p>","isAnswer":True,"is_answer":True}
     ]
   }
 },
 "silver": {
   "title": "Silver: find the constant k",
   "steps": [
     "Write the rule: direct is \\(y = kx\\), inverse is \\(y = \\frac{k}{x}\\).",
     "Find \\(k\\) from the pair you are given: direct \\(k = y \\div x\\), inverse \\(k = y \\times x\\).",
     "Put \\(k\\) back into the rule and solve for the missing value, forwards or backwards."
   ],
   "example": {
     "question": "y is directly proportional to x. When x = 4, y = 10. Find y when x = 6.",
     "steps": [
       {"label":"Rule","content":"<p>Direct, so \\(y = kx\\).</p>"},
       {"label":"Find k","content":"<p>\\(k = 10 \\div 4 = 2.5\\).</p>"},
       {"label":"Use it","content":"<p>\\(y = 2.5 \\times 6 = 15\\).</p>"},
       {"label":"Check","content":"<p>\\(15 \\div 6 = 2.5 = k\\) ✓</p>"},
       {"label":"Answer","content":"<p><strong>15</strong></p>","isAnswer":True,"is_answer":True}
     ]
   }
 },
 "gold": {
   "title": "Gold: reverse and context proportion",
   "steps": [
     "Same rules, trickier set-ups: gears, work rates and pressure are <strong>inverse</strong>, so the product stays fixed.",
     "Given \\(y\\) and asked for \\(x\\)? Rearrange \\(y = kx\\) to \\(x = y \\div k\\), or \\(y = \\frac{k}{x}\\) to \\(x = k \\div y\\).",
     "Read the context: an amount added on (like a fixed charge) means it is NOT direct proportion."
   ],
   "example": {
     "question": "P is inversely proportional to V. When V = 2, P = 150. Find V when P = 50.",
     "steps": [
       {"label":"Rule","content":"<p>Inverse, so \\(P = \\frac{k}{V}\\).</p>"},
       {"label":"Find k","content":"<p>\\(k = 2 \\times 150 = 300\\).</p>"},
       {"label":"Use it","content":"<p>\\(V = 300 \\div 50 = 6\\).</p>"},
       {"label":"Check","content":"<p>\\(6 \\times 50 = 300 = k\\) ✓</p>"},
       {"label":"Answer","content":"<p><strong>6</strong></p>","isAnswer":True,"is_answer":True}
     ]
   }
 }
}

# ---- guided: opener + teach ----
pd["guided"] = {
 "opener": {
   "label": "Before any algebra",
   "display": "5 apples cost £2<br>2 taps fill a bath in 10 minutes",
   "steps": [
     {"say":"Two everyday puzzles, no algebra. Start with the apples: twice as many apples cost twice as much.",
      "pre":"10 apples would cost £","post":"","answer":4,
      "hint":"Double the apples means double the money."},
     {"say":"Now the taps. Same bath, but turn on 4 taps instead of 2.",
      "pre":"With 4 taps it fills in ","post":" minutes","answer":5,
      "hint":"Twice as many taps means half the time."},
     {"say":"Two everyday moves. Apples: <strong>more means more</strong>, that is <strong>direct proportion</strong>. Taps: <strong>more means less</strong>, that is <strong>inverse proportion</strong>. For both, find the value of ONE first (one apple is 40p; two taps take 20 tap-minutes), then scale. Algebra just writes direct as \\(y = kx\\) and inverse as \\(y = \\frac{k}{x}\\)."}
   ]
 },
 "teach": {
   "bronze": {
     "display": "4 books cost £10. How much do 6 books cost?",
     "label": "Together: your first one",
     "steps": [
       {"say":"Direct proportion: more books, more money. Find ONE book first.",
        "pre":"One book: 10 ÷ 4 = £","post":"","answer":2.5,
        "hint":"Divide the total cost by the number of books."},
       {"say":"Now scale up. Six books is six lots of that.",
        "pre":"6 books: 2.5 × 6 = £","post":"","answer":15,
        "hint":"Multiply the one-book cost by 6."},
       {"say":"The one-book value works backwards too. How many books cost £20?",
        "pre":"20 ÷ 2.5 = ","post":" books","answer":8,
        "hint":"Divide the money by the one-book cost.",
        "done":"Find one, then multiply or divide. That is the whole bronze method."},
       {"say":"Check against the start.",
        "pre":"4 books: 2.5 × 4 = £","post":"","answer":10,
        "hint":"Four books should return the starting cost.",
        "done":"Back to the given £10, so £2.50 per book is right."}
     ]
   },
   "silver": {
     "display": "\\(y\\) is directly proportional to \\(x\\). When \\(x = 4\\), \\(y = 18\\). Find \\(y\\) when \\(x = 10\\).",
     "label": "Together: the silver move",
     "steps": [
       {"say":"Now it is in algebra. Direct means \\(y = kx\\). First find the constant \\(k\\).",
        "pre":"k = 18 ÷ 4 = ","post":"","answer":4.5,
        "hint":"Divide the y value by the matching x value."},
       {"say":"So the rule is \\(y = 4.5x\\). Use it at the new x.",
        "pre":"y = 4.5 × 10 = ","post":"","answer":45,
        "hint":"Multiply k by the new x."},
       {"say":"It runs backwards too. If y were 27, what is x?",
        "pre":"x = 27 ÷ 4.5 = ","post":"","answer":6,
        "hint":"Divide y by k to get x.",
        "done":"Find k once, then multiply or divide. That is the silver move."},
       {"say":"Check with the first pair.",
        "pre":"4.5 × 4 = ","post":"","answer":18,
        "hint":"k times the original x should give the original y.",
        "done":"That returns the given y = 18, so k = 4.5 is right."}
     ]
   },
   "gold": {
     "display": "\\(y\\) is inversely proportional to \\(x\\). When \\(x = 4\\), \\(y = 15\\). Find \\(x\\) when \\(y = 12\\).",
     "label": "Together: the gold move",
     "steps": [
       {"say":"Inverse means \\(y = \\frac{k}{x}\\), so the constant is the PRODUCT: \\(k = x \\times y\\).",
        "pre":"k = 4 × 15 = ","post":"","answer":60,
        "hint":"Multiply the pair together for inverse."},
       {"say":"The rule is \\(y = \\frac{60}{x}\\). This time we know y = 12 and want x. Rearrange: \\(x = \\frac{k}{y}\\).",
        "pre":"x = 60 ÷ 12 = ","post":"","answer":5,
        "hint":"Divide the constant by y."},
       {"say":"Sense check: y dropped from 15 to 12, so x should rise. It did, from 4 to 5.",
        "pre":"Confirm the product: 5 × 12 = ","post":"","answer":60,
        "hint":"x times y should return the constant.",
        "done":"Same 60, so x = 5 fits."},
       {"say":"One more, to prove the product never changes. What is x when y = 10?",
        "pre":"x = 60 ÷ 10 = ","post":"","answer":6,
        "hint":"Divide the constant by the new y.",
        "done":"6 × 10 = 60 again. The product stays fixed: that is the gold idea."}
     ]
   }
 }
}

json.dump(pd, io.open(OUT,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
# sanity: em dash sweep
s = io.open(OUT,encoding="utf-8").read()
print("em dashes remaining:", s.count("—"))
print("wrote", OUT)
