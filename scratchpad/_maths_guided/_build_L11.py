# -*- coding: utf-8 -*-
import json, io

pd = json.load(io.open("_live_L11.json", encoding="utf-8"))
pb = pd["problem_bank"]

# ---- reusable messages (no em dashes; plain unicode) ----
FLIP = "When you multiply or divide both sides by a negative number, flip the inequality sign: < becomes >, and > becomes <."
REV  = "You have the right boundary number, but the arrow points the wrong way. Remember x > 3 means x is bigger than 3, and x < 3 means x is smaller than 3."
STRICT = "Look at the inequality symbol. A strict symbol (< or >) does not include the boundary value, while ≤ or ≥ does. Your answer must use the same type of symbol as the question."

def mc(pattern, expect, message, note):
    return {"pattern": pattern, "check": pattern, "expect": expect, "message": message, "note": note}

# ---------------- BRONZE misconceptions + hints ----------------
bronze_specs = [
    # (hint, [misconceptions])
    ("Subtract 3 from both sides to get x on its own.", [
        mc("strict_vs_nonstrict", 3, STRICT, "Confuses > with >=, picks x>=4."),
        mc("wrong_direction", 2, REV, "Reverses direction, picks x<4."),
        mc("arithmetic", 1, "Take 3 off both sides, do not add it: x > 7 − 3 = 4.", "Adds 3 instead of subtracting: x>7+3=10."),
    ]),
    ("Divide both sides by 2.", [
        mc("strict_vs_nonstrict", 3, STRICT, "Confuses < with <=, picks x<=5."),
        mc("wrong_direction", 2, REV, "Reverses direction, picks x>5."),
        mc("arithmetic", 1, "To undo 2 times x, divide by 2, do not subtract 2: x < 5.", "Subtracts 2 instead of dividing: 10-2=8."),
    ]),
    ("Add 1 to both sides, then divide by 3.", [
        mc("strict_vs_nonstrict", 0, STRICT, "Confuses >= with >, picks x>3."),
        mc("wrong_direction", 3, REV, "Reverses direction, picks x<=3."),
        mc("arithmetic", 2, "After 3x ≥ 9 you still divide by 3, giving x ≥ 3.", "Forgets to divide by 3: keeps x>=9."),
    ]),
    ("Subtract 2 from both sides, then divide by 4.", [
        mc("strict_vs_nonstrict", 1, STRICT, "Confuses <= with <, picks x<4."),
        mc("wrong_direction", 3, REV, "Reverses direction, picks x>=4."),
        mc("arithmetic", 2, "Subtract the 2 first: 4x ≤ 18 − 2 = 16, then divide by 4.", "Adds 2 instead of subtracting: 4x<=20, x<=5."),
    ]),
    ("Add 3 to both sides, then divide by 5.", [
        mc("strict_vs_nonstrict", 3, STRICT, "Confuses > with >=, picks x>=3."),
        mc("wrong_direction", 2, REV, "Reverses direction, picks x<3."),
    ]),
    ("Multiply both sides by 2 to undo the divide.", [
        mc("strict_vs_nonstrict", 3, STRICT, "Confuses > with >=, picks x>=6."),
        mc("wrong_direction", 2, REV, "Reverses direction, picks x<6."),
        mc("arithmetic", 0, "To undo dividing by 2, multiply by 2: x > 3 × 2 = 6.", "Divides by 2 instead of multiplying: 3/2=1.5."),
    ]),
    ("Subtract 1 from both sides, then divide by 7.", [
        mc("strict_vs_nonstrict", 1, STRICT, "Confuses <= with <, picks x<3."),
        mc("wrong_direction", 3, REV, "Reverses direction, picks x>=3."),
        mc("arithmetic", 2, "After 7x ≤ 21, divide by 7 to finish: x ≤ 3.", "Forgets to divide by 7: keeps x<=21."),
    ]),
    ("Subtract 5 from both sides, then divide by 2.", [
        mc("strict_vs_nonstrict", 3, STRICT, "Confuses < with <=, picks x<=4."),
        mc("wrong_direction", 2, REV, "Reverses direction, picks x>4."),
        mc("arithmetic", 1, "Take the 5 off both sides: 2x < 13 − 5 = 8, then divide by 2.", "Adds 5 instead of subtracting: 2x<18, x<9."),
    ]),
]

# ---------------- SILVER misconceptions + hints + guided_steps ----------------
silver_specs = [
    # S0 -3x>12 -> x<-4 (index1)
    ("Divide by minus 3 and flip the inequality sign.", [
        mc("didnt_flip", 0, FLIP, "Divides by -3 without flipping: keeps x>-4."),
        mc("arithmetic", 3, "The coefficient is minus 3, not 3. Divide by minus 3 and flip: x < −4.", "Treats -3 as 3: 3x>12, x>4."),
    ], None),
    # S1 4-x<=7 -> x>=-3 (index1)
    ("Subtract 4, then divide by minus 1 and flip the sign.", [
        mc("didnt_flip", 0, FLIP, "Gets -x<=3, divides by -1 without flipping: x<=-3."),
        mc("strict_vs_nonstrict", 3, STRICT, "Confuses >= with >, picks x>-3."),
        mc("arithmetic", 2, "Watch the constant: moving 4 across gives x ≥ 4 − 7 = −3, not 3.", "Sign slip on constant: x>=7-4=3."),
    ], None),
    # S2 count 1<x+3<=6 -> -2<x<=3 = 5 (single_value)
    ("Subtract 3 from all three parts, then list the integers including negatives.", [
        mc("wrong_integers", 6, "The left symbol is strict (<), so −2 is NOT included. Count only −1, 0, 1, 2, 3, which is 5 integers.", "Treats < as <=, includes -2: counts 6."),
        mc("arithmetic", 4, "Do not skip the negative integers. −1 is greater than −2, so it counts: −1, 0, 1, 2, 3 gives 5.", "Ignores negatives, counts only 0,1,2,3=4."),
    ], "count"),
    # S3 -2x+5>1 -> x<2 (index0)
    ("Subtract 5, then divide by minus 2 and flip the sign.", [
        mc("didnt_flip", 1, FLIP, "Gets -2x>-4, divides by -2 without flipping: x>2."),
    ], None),
    # S4 10-3x<1 -> x>3 (index1)
    ("Subtract 10, then divide by minus 3 and flip the sign.", [
        mc("didnt_flip", 0, FLIP, "Gets -3x<-9, divides by -3 without flipping: x<3."),
        mc("strict_vs_nonstrict", 3, STRICT, "Confuses > with >=, picks x>=3."),
        mc("arithmetic", 2, "A negative divided by a negative is positive: −9 ÷ −3 = 3, so x > 3.", "Computes -9/-3 as -3: x>-3."),
    ], None),
    # S5 smallest 2<=4x-6<10 -> 2<=x<4 smallest 2 (single_value)
    ("Add 6 to all three parts, divide by 4, then pick the smallest integer allowed.", [
        mc("wrong_integers", 3, "The lower symbol is ≤, so x = 2 is allowed. The smallest integer is 2, not 3.", "Treats 2<=x as 2<x, gives smallest 3."),
        mc("arithmetic", -1, "To undo minus 6, add 6 to all three parts: 2 + 6 ≤ 4x < 10 + 6.", "Subtracts 6 instead of adding: -4<=4x<4, smallest -1."),
    ], "smallest"),
    # S6 3(x+1)>18 -> x>5 (index0)
    ("Divide both sides by 3 first, then subtract 1.", [
        mc("strict_vs_nonstrict", 3, STRICT, "Confuses > with >=, picks x>=5."),
        mc("arithmetic", 1, "After dividing by 3 you get x + 1 > 6; now subtract 1 to get x > 5.", "Divides by 3 then forgets to subtract 1: x>6."),
        mc("arithmetic", 2, "Divide the whole left side by 3 too: 3(x + 1) ÷ 3 is x + 1, so x + 1 > 6.", "Drops the 3 without dividing: x+1>18, x>17."),
    ], None),
]

# ---------------- GOLD misconceptions + hints + guided_steps ----------------
gold_specs = [
    # G0 count -3<2x+1<=7 -> -2<x<=3 = 5 (single_value)
    ("Subtract 1 from all three parts, divide by 2, then list the integers including negatives.", [
        mc("wrong_integers", 6, "The left symbol is strict, so −2 is NOT included. The integers are −1, 0, 1, 2, 3, which is 5.", "Treats < as <=, includes -2: counts 6."),
        mc("arithmetic", 4, "Do not skip negative integers. −1 is in the range, so the full list is −1, 0, 1, 2, 3, giving 5.", "Ignores negatives, counts only 0,1,2,3=4."),
    ], "count"),
    # G1 (5-x)/3>=2 -> x<=-1 (index0)
    ("Multiply by 3, then divide by minus 1 and flip the sign.", [
        mc("didnt_flip", 1, FLIP, "Gets -x>=1, divides by -1 without flipping: x>=-1."),
        mc("strict_vs_nonstrict", 3, "The answer uses ≤, so −1 is included. x < −1 wrongly leaves out −1.", "Confuses <= with <, picks x<-1."),
    ], None),
    # G2 4(2x-3)<5x+6 -> x<6 (index0)
    ("Expand the bracket, then gather the x terms on one side.", [
        mc("strict_vs_nonstrict", 3, STRICT, "Confuses < with <=, picks x<=6."),
        mc("wrong_direction", 1, "You have x < 6 but the arrow is reversed. No negative was involved, so the sign does not flip.", "Reverses to x>6."),
    ], None),
    # G3 largest n 3n+7<28 -> n<7 largest 6 (single_value)
    ("Subtract 7, divide by 3, then take the largest integer below the bound.", [
        mc("wrong_integers", 7, "n < 7 is strict, so 7 is not allowed. The largest integer is 6.", "Treats n<7 as n<=7, gives 7."),
        mc("arithmetic", 11, "Subtract the 7, do not add it: 3n < 28 − 7 = 21, then divide by 3.", "Adds 7: 3n<35, n<11.67, largest 11."),
    ], "largest"),
    # G4 combined 2x+1>5 & 3x-4<11 -> 2<x<5 (index0)
    ("Solve each inequality, then combine them into one range.", [
        mc("strict_vs_nonstrict", 3, STRICT, "Confuses strict with non-strict, picks 2<=x<=5."),
        mc("arithmetic", 1, "That is only the first inequality. You must also use 3x − 4 < 11, which gives x < 5.", "Gives only x>2 (first inequality)."),
        mc("arithmetic", 2, "That is only the second inequality. You must also use 2x + 1 > 5, which gives x > 2.", "Gives only x<5 (second inequality)."),
    ], None),
]

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def sayonly(say):
    return {"say": say}

# ---- guided_steps for the four single_value problems ----
GS = {}
# silver[2]: 1<x+3<=6 count 5
GS[("silver",2)] = [
    sayonly("Subtract 3 from all three parts of \\(1 < x + 3 \\leq 6\\), the same step done to each part."),
    box("Left part: 1 − 3 = ", -2, "Subtract 3 from 1."),
    box("Right part: 6 − 3 = ", 3, "Subtract 3 from 6."),
    sayonly("So the range is \\(-2 < x \\leq 3\\). The left is strict, so −2 is left out; the right includes 3."),
    box("−2 is excluded, so the smallest integer allowed is ", -1, "The next integer above −2.", phase="substitute"),
    box("Count the integers from −1 up to 3 inclusive: ", 5, "Count −1, 0, 1, 2, 3.", phase="substitute",
        done="Five integers. The trap is forgetting the negative one, −1."),
]
# silver[5]: 2<=4x-6<10 smallest 2
GS[("silver",5)] = [
    sayonly("Add 6 to all three parts of \\(2 \\leq 4x - 6 < 10\\)."),
    box("Left part: 2 + 6 = ", 8, "Add 6 to 2."),
    box("Right part: 10 + 6 = ", 16, "Add 6 to 10."),
    sayonly("So \\(8 \\leq 4x < 16\\). Divide all three parts by 4."),
    box("Left part: 8 ÷ 4 = ", 2, "Divide 8 by 4."),
    box("Right part: 16 ÷ 4 = ", 4, "Divide 16 by 4."),
    sayonly("So \\(2 \\leq x < 4\\). The left symbol is \\(\\leq\\), so 2 itself is allowed."),
    box("The smallest integer that fits is ", 2, "The left symbol is ≤, so start at 2 itself.", phase="substitute"),
    box("Check it: 4 × 2 − 6 = ", 2, "Work out 4 × 2 − 6.", phase="substitute",
        done="That equals the lower bound 2, and the symbol is ≤, so 2 is the smallest integer."),
]
# gold[0]: -3<2x+1<=7 count 5
GS[("gold",0)] = [
    sayonly("Subtract 1 from all three parts of \\(-3 < 2x + 1 \\leq 7\\)."),
    box("Left part: −3 − 1 = ", -4, "Subtract 1 from −3."),
    box("Right part: 7 − 1 = ", 6, "Subtract 1 from 7."),
    sayonly("So \\(-4 < 2x \\leq 6\\). Divide all three parts by 2."),
    box("Left part: −4 ÷ 2 = ", -2, "Divide −4 by 2."),
    box("Right part: 6 ÷ 2 = ", 3, "Divide 6 by 2."),
    sayonly("So \\(-2 < x \\leq 3\\). The left is strict, so −2 is out, but −1 is in."),
    box("−2 is excluded, so the smallest integer allowed is ", -1, "The next integer above −2.", phase="substitute"),
    box("Count the integers from −1 up to 3 inclusive: ", 5, "Count −1, 0, 1, 2, 3.", phase="substitute",
        done="Five integers. The trap is dropping the negative integer −1."),
]
# gold[3]: 3n+7<28 largest 6
GS[("gold",3)] = [
    sayonly("Solve \\(3n + 7 < 28\\) like an equation. Take 7 off both sides."),
    box("28 − 7 = ", 21, "Subtract 7 from 28."),
    sayonly("So \\(3n < 21\\). Divide both sides by 3."),
    box("21 ÷ 3 = ", 7, "Divide 21 by 3."),
    sayonly("So \\(n < 7\\). The symbol is strict, so n = 7 is NOT allowed."),
    box("The largest integer below 7 is ", 6, "The integer just under 7.", phase="substitute"),
    box("Check it: 3 × 6 + 7 = ", 25, "Work out 3 × 6 + 7.", phase="substitute",
        done="25 is less than 28, so n = 6 works. n = 7 would give 28, which is not less than 28."),
]

def apply_specs(tier, specs):
    for i, (hint, misc, *rest) in enumerate(specs):
        p = pb[tier][i]
        p["hint"] = hint
        p["misconceptions"] = misc
        if (tier, i) in GS:
            p["guided_steps"] = GS[(tier, i)]
        # ensure key order stays fine (json dump handles it)

# gold[3]: retune RHS 25 -> 28 to clear duplicate-answer-within-tier (both were 5)
pb["gold"][3]["display"] = "Find the largest integer \\(n\\) such that \\(3n + 7 < 28\\)"
pb["gold"][3]["solutions"] = [6]

apply_specs("bronze", bronze_specs)
apply_specs("silver", silver_specs)
apply_specs("gold", gold_specs)

# ---------------- method_card (slim, no em dash) ----------------
pd["method_card"] = {
    "title": "Solving Inequalities",
    "steps": [
        "Solve it like an equation: do the same thing to both sides until x is on its own.",
        "If you multiply or divide by a negative number, flip the inequality sign.",
        "Keep the right symbol in your answer (\\(<\\), \\(>\\), \\(\\leq\\), \\(\\geq\\)).",
        "To list integers, find the range and write every whole number in it, negatives included.",
    ],
    "content": "<p><strong>Inequalities</strong> use \\(<\\), \\(>\\), \\(\\leq\\), \\(\\geq\\) instead of \\(=\\). Solve them exactly like equations, with one rule: if you multiply or divide both sides by a <strong>negative</strong> number, flip the sign, so \\(<\\) becomes \\(>\\).</p><p>A strict symbol (\\(<\\), \\(>\\)) does not include the boundary; \\(\\leq\\) and \\(\\geq\\) do. For a double inequality like \\(2 < x + 1 \\leq 5\\), do the same step to all three parts: \\(1 < x \\leq 4\\).</p>",
    "example": "<p><strong>Solve</strong> \\(3x + 5 > 14\\)</p><p>Subtract 5: \\(3x > 9\\). Divide by 3: \\(x > 3\\). The answer is every number greater than 3.</p>",
}

# ---------------- worked_examples: strip em dashes from labels ----------------
for we in pd.get("worked_examples", []):
    for st in we.get("steps", []):
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

# ---------------- tier_guides ----------------
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one and two step inequalities",
        "steps": [
            "Solve an inequality just like an equation. Undo the <strong>+</strong> or <strong>−</strong> first, then the <strong>×</strong> or <strong>÷</strong>.",
            "Do the same thing to both sides, and keep the same symbol the whole way through.",
            "Your answer is a range, like \\(x > 3\\): every number bigger than 3, not a single value.",
        ],
        "example": {
            "question": "Solve \\(2x + 1 < 9\\)",
            "steps": [
                {"label": "Subtract 1", "content": "\\(2x < 8\\)"},
                {"label": "Divide by 2", "content": "\\(x < 4\\)"},
                {"label": "Check", "content": "Try \\(x = 3\\): \\(2(3)+1 = 7 < 9\\), so 3 fits."},
                {"label": "Answer", "content": "\\(x < 4\\)", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: negatives and double inequalities",
        "steps": [
            "If you divide or multiply by a <strong>negative</strong>, flip the sign: \\(<\\) becomes \\(>\\).",
            "For a double inequality like \\(1 < 2x \\leq 8\\), do the same step to all three parts.",
            "A strict symbol (\\(<\\)) leaves the boundary out; \\(\\leq\\) keeps it in.",
        ],
        "example": {
            "question": "Solve \\(5 - 2x \\geq 1\\)",
            "steps": [
                {"label": "Subtract 5", "content": "\\(-2x \\geq -4\\)"},
                {"label": "Divide by −2 and flip", "content": "\\(x \\leq 2\\)"},
                {"label": "Check", "content": "Try \\(x = 2\\): \\(5 - 2(2) = 1 \\geq 1\\), so 2 fits."},
                {"label": "Answer", "content": "\\(x \\leq 2\\)", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: integer solutions and combined inequalities",
        "steps": [
            "Rearrange to a range first, then <strong>list every integer</strong> inside it, negatives included.",
            "Watch each end: a strict symbol excludes the boundary, \\(\\leq\\) or \\(\\geq\\) includes it.",
            "For two separate inequalities, solve each, then combine them into one overlapping range.",
        ],
        "example": {
            "question": "List the integers satisfying \\(-2 \\leq 3x - 1 < 11\\)",
            "steps": [
                {"label": "Add 1 to all parts", "content": "\\(-1 \\leq 3x < 12\\)"},
                {"label": "Divide by 3", "content": "\\(-\\tfrac{1}{3} \\leq x < 4\\)"},
                {"label": "Check ends", "content": "0 is the first integer above \\(-\\tfrac13\\); 4 is excluded, so 3 is the last."},
                {"label": "Answer", "content": "0, 1, 2, 3", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---------------- guided.opener + teach ----------------
opener = {
    "steps": [
        sayonly("A puzzle first, no algebra needed. A £14 game: you have £5 now and save £3 a week."),
        box("Fewest whole weeks until you can afford it? ", 3, "You need £9 more and save £3 each week.", post="weeks"),
        sayonly("3 weeks works, and so does 4, or 5. The answer is a whole <strong>range</strong>, 3 or more, not a single number. Writing your money as \\(5 + 3w\\), you found where \\(5 + 3w \\geq 14\\). That is an <strong>inequality</strong>: you solve it just like an equation, but the answer is a range."),
        box("Check the boundary: after exactly 3 weeks, how much money do you have, in £? ", 14, "Start with £5 and add £3 three times.", post=""),
        sayonly("£14, exactly enough. That boundary comes from solving \\(5 + 3w = 14\\), and the inequality then says 3 weeks or more. One warning for later: if you ever divide by a negative, the inequality sign flips over."),
    ],
}

teach = {
    "bronze": {
        "display": "Solve \\(2x + 3 < 11\\)",
        "steps": [
            sayonly("Solve \\(2x + 3 < 11\\) the same way you solve an equation. First take 3 off both sides."),
            box("11 − 3 = ", 8, "Subtract 3 from the right-hand side."),
            sayonly("So \\(2x < 8\\). Now divide both sides by 2."),
            box("8 ÷ 2 = ", 4, "Divide the right-hand side by 2."),
            sayonly("So \\(x < 4\\): every number less than 4. Keep the same symbol, \\(<\\), because we did not divide by a negative."),
            box("Test x = 3: 2 × 3 + 3 = ", 9, "Work out 2 × 3 + 3.", done="9 is less than 11, so x = 3 fits. The range x < 4 is right."),
            box("Test the boundary x = 4: 2 × 4 + 3 = ", 11, "Work out 2 × 4 + 3.", done="11 is not less than 11, so 4 is NOT included. That is why its circle is open."),
        ],
    },
    "silver": {
        "display": "Solve \\(4 - 2x < 10\\)",
        "steps": [
            sayonly("Solve \\(4 - 2x < 10\\). Take 4 off both sides first."),
            box("10 − 4 = ", 6, "Subtract 4 from the right."),
            sayonly("So \\(-2x < 6\\). Now divide by −2. Because we divide by a NEGATIVE, the sign flips: \\(<\\) becomes \\(>\\)."),
            box("6 ÷ (−2) = ", -3, "A positive divided by a negative is negative."),
            sayonly("So \\(x > -3\\). The flip is the whole point: dividing by a negative reverses the arrow."),
            box("Test x = 0 (more than −3): 4 − 2 × 0 = ", 4, "2 × 0 is 0.", done="4 is less than 10, so x = 0 fits, confirming x > −3."),
            box("Test x = −4 (less than −3): 4 − 2 × (−4) = ", 12, "−2 × −4 = +8, then add 4.", done="12 is NOT less than 10, so −4 fails. The arrow really does point the other way."),
        ],
    },
    "gold": {
        "display": "List the integers satisfying \\(-1 \\leq 2x + 3 < 9\\)",
        "steps": [
            sayonly("List the integers satisfying \\(-1 \\leq 2x + 3 < 9\\). Do the same step to all three parts. First subtract 3 from each part."),
            box("Left part: −1 − 3 = ", -4, "Subtract 3 from −1."),
            box("Right part: 9 − 3 = ", 6, "Subtract 3 from 9."),
            sayonly("So \\(-4 \\leq 2x < 6\\). Divide all three parts by 2."),
            box("−4 ÷ 2 = ", -2, "Divide −4 by 2."),
            box("6 ÷ 2 = ", 3, "Divide 6 by 2."),
            sayonly("So \\(-2 \\leq x < 3\\). Now list every integer, negatives included. −2 is included (\\(\\leq\\)), 3 is not (\\(<\\))."),
            box("How many integers satisfy −2 ≤ x < 3? Count −2, −1, 0, 1, 2: ", 5, "Count −2, −1, 0, 1, 2.", done="Five integers. The trap is forgetting −2 and −1."),
        ],
    },
}

pd["guided"] = {"opener": opener, "teach": teach}

json.dump(pd, io.open("lesson_algebra-L11.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("written")
