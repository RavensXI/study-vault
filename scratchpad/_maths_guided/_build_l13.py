# -*- coding: utf-8 -*-
import json, io

pd = json.load(io.open("_l13_live.json", encoding="utf-8"))
pb = pd["problem_bank"]

# ---------------------------------------------------------------- helpers
def box(pre, answer, hint, post="", phase=None, done=None, say=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if phase: d["phase"] = phase
    if done: d["done"] = done
    if say: d["say"] = say
    return d

def sayonly(text):
    return {"say": text}

# ================================================================ 1. HINTS
bronze_hints = [
    "The step is 3, so start with 3n; the constant is the first term minus 3.",
    "The step is 4, so start with 4n; the constant is 6 minus 4.",
    "The step is 3, so start with 3n; the constant is 1 minus 3.",
    "The step is 5, so start with 5n; the constant is 7 minus 5.",
    "Put n equals 10 into 2n + 3.",
    "The step is 2, so start with 2n; the constant is 3 minus 2.",
    None,  # B6 replaced below
    "The step is 5, so start with 5n; the constant is 10 minus 5.",
]
for i, h in enumerate(bronze_hints):
    if h is not None:
        pb["bronze"][i]["hint"] = h

silver_hints = [
    "The sequence falls by 3, so use minus 3 as the step; the constant is 20 minus that step.",
    "The step is minus 7; remember subtracting a negative adds when you find the constant.",
    "Find the rule first (step 5), then put n equals 15 into it.",
    "The step is 4; the constant is minus 1 minus 4.",
    "The nth term is 3n minus 1. Solve 3n minus 1 equals 41.",
    None,  # S5 replaced below
    "The nth term is 3n plus 2. Solve 3n plus 2 is less than 50 and count the whole-number positions.",
]
for i, h in enumerate(silver_hints):
    if h is not None:
        pb["silver"][i]["hint"] = h

gold_hints = [
    "Set 3n plus 7 equal to 100 and solve for n.",
    "Set the two formulas equal to each other and solve for n.",
    "List the five terms, then add them up.",
    "The value rises 16 over 4 steps, so the step is 4; then find the constant.",
    "The nth term is 5n minus 2. Find the smallest n where 5n minus 2 is over 200.",
]
for i, h in enumerate(gold_hints):
    pb["gold"][i]["hint"] = h

# ================================================================ 2. REPLACE DUPLICATE PROBLEMS
# --- B6 (was 'Find the 8th term of 4n-1', duplicate of B4) -> generate first terms (MC)
pb["bronze"][6] = {
    "display": "The nth term of a sequence is \\(4n - 1\\). What are the first three terms?",
    "options": ["\\(3, 7, 11\\)", "\\(4, 8, 12\\)", "\\(0, 3, 6\\)", "\\(-1, 3, 7\\)"],
    "solutions": [0],
    "calculator": False,
    "input_type": "multiple_choice",
    "hint": "Put n equals 1, then 2, then 3 into the formula.",
    "misconceptions": [
        {"check": "dropped_constant", "expect": 1,
         "message": "Don't forget the \\(-1\\). Each term is \\(4n - 1\\): at \\(n = 1\\) that is \\(4 - 1 = 3\\), not \\(4\\).",
         "pattern": "ignored_constant",
         "expect_note": "Uses 4n only (4, 8, 12), option index 1"},
        {"check": "start_at_zero", "expect": 3,
         "message": "Start counting positions at \\(n = 1\\), not \\(n = 0\\). The first term is \\(4(1) - 1 = 3\\), so \\(-1, 3, 7\\) begins one place too early.",
         "pattern": "off_by_one_start",
         "expect_note": "Uses n=0,1,2 giving -1,3,7, option index 3"},
    ],
}

# --- S5 (was '100,93,86,79 d=-7', near-duplicate of S1 d=-7) -> new d=-6 sequence (MC)
pb["silver"][5] = {
    "display": "Find the nth term of 31, 25, 19, 13, ...",
    "options": ["\\(-6n + 37\\)", "\\(-6n + 31\\)", "\\(6n - 37\\)", "\\(-6n + 25\\)"],
    "solutions": [0],
    "calculator": False,
    "input_type": "multiple_choice",
    "hint": "The sequence falls by 6 each time; the constant is 31 minus negative 6.",
    "misconceptions": [
        {"check": "zero_term", "expect": 1,
         "message": "The nth term formula is \\(dn + (a - d)\\) where \\(d\\) is the common difference and \\(a\\) is the first term. Don't forget to subtract \\(d\\) from \\(a\\) for the constant.",
         "pattern": "forgot_adjust",
         "expect_note": "d=-6, c=a=31 (no subtraction) gives -6n+31, option index 1"},
        {"check": "calculation", "expect": 3,
         "message": "Watch the double negative: the constant is \\(31 - (-6) = 37\\), not \\(31 - 6 = 25\\).",
         "pattern": "arithmetic",
         "expect_note": "c computed as 31-6=25 gives -6n+25, option index 3"},
    ],
}

# ================================================================ 3. FIX S4 (hint 40->41 + consolidated misconceptions)
s4 = pb["silver"][4]
s4["hint"] = "The nth term is 3n minus 1. Solve 3n minus 1 equals 41."
s4["misconceptions"] = [
    {"check": "equals_21", "expect": 21.0,
     "message": "You correctly reached \\(3n = 42\\), which is a great start. Now divide by 3, not 2: \\(42 \\div 3 = 14\\), so 41 is the 14th term.",
     "pattern": "arithmetic_slip_dividing_42"},
    {"check": "equals_13", "expect": 13.0,
     "message": "Check your nth term: first term 2, common difference 3, so the rule is \\(3n - 1\\), not \\(3n + 2\\). Solving \\(3n - 1 = 41\\) gives \\(n = 14\\).",
     "pattern": "wrong_nth_term_formula"},
    {"check": "equals_15", "expect": 15.0,
     "message": "The formula gives the term number directly: \\(n = 14\\) means 41 is the 14th term, so there is no need to add 1.",
     "pattern": "adds_one_to_correct_answer"},
]

# ================================================================ 4. FIX S6 misconceptions (tailored + de-duplicated expects)
s6 = pb["silver"][6]
s6["misconceptions"] = [
    {"check": "equals_16", "expect": 16,
     "message": "The 16th term is \\(3(16) + 2 = 50\\), which is not less than 50, so it does not count. Only the first 15 terms are below 50.",
     "pattern": "includes_boundary_term",
     "expect_note": "Solving 3n+2=50, or misreading the strict inequality, gives 16"},
    {"check": "zero_term", "expect": 14,
     "message": "Check your nth term formula: using the first term (5) as the constant gives \\(3n + 5\\) instead of \\(3n + 2\\). The constant is first term minus d: \\(5 - 3 = 2\\), which shifts the boundary.",
     "pattern": "forgot_adjust",
     "expect_note": "d=3, c=a=5 gives 3n+5; 3n+5<50 gives n<15, so 14 terms"},
]

# ================================================================ 5. GUIDED_STEPS on single_value problems
pb["bronze"][4]["guided_steps"] = [
    sayonly("The formula \\(2n + 3\\) gives the value at position \\(n\\). For the 10th term, put \\(n = 10\\)."),
    box("First the 2n part: 2 × 10 = ", 20, "Multiply 2 by 10."),
    box("Now add the constant: 20 + 3 = ", 23, "Add 3 to 20.", phase="substitute"),
    box("Check: the 9th term is 2 × 9 + 3 = 21, and terms rise by 2, so 21 + 2 = ", 23,
        "Add 2 to 21.", phase="substitute", done="It matches 23, so the 10th term is 23."),
]

pb["silver"][2]["guided_steps"] = [
    sayonly("The formula is not given, so find it first. Start with the common difference."),
    box("Common difference: 9 − 4 = ", 5, "Subtract the first term from the second."),
    box("Constant: first term − d = 4 − 5 = ", -1, "Take the common difference off the first term.",
        done="So the nth term is 5n − 1."),
    sayonly("Now use \\(5n - 1\\) to find the 15th term. Put \\(n = 15\\)."),
    box("5 × 15 = ", 75, "Multiply 5 by 15.", phase="substitute"),
    box("Subtract 1: 75 − 1 = ", 74, "Take 1 away from 75.", phase="substitute"),
    box("Check the rule on the 3rd term: 5 × 3 − 1 = ", 14, "15 minus 1.", phase="substitute",
        done="It gives 14, the listed 3rd term, so 5n − 1 is right and the 15th term is 74."),
]

pb["silver"][4]["guided_steps"] = [
    sayonly("Find the rule for \\(2, 5, 8, 11, \\ldots\\) first."),
    box("Common difference: 5 − 2 = ", 3, "Subtract consecutive terms."),
    box("Constant: first term − d = 2 − 3 = ", -1, "Take the common difference off the first term.",
        done="So the nth term is 3n − 1."),
    sayonly("To test if 41 is in the sequence, solve \\(3n - 1 = 41\\). If \\(n\\) is a whole number, 41 is a term."),
    box("Add 1 to both sides: 41 + 1 = ", 42, "This gives 3n = 42.", phase="substitute"),
    box("Divide by 3: 42 ÷ 3 = ", 14, "Divide 42 by 3.", phase="substitute"),
    box("Check: 3 × 14 − 1 = ", 41, "42 minus 1.", phase="substitute",
        done="It gives 41 and 14 is a whole number, so 41 is the 14th term."),
]

pb["silver"][6]["guided_steps"] = [
    sayonly("Find the rule for \\(5, 8, 11, \\ldots\\) first."),
    box("Common difference: 8 − 5 = ", 3, "Subtract consecutive terms."),
    box("Constant: first term − d = 5 − 3 = ", 2, "Take the common difference off the first term.",
        done="So the nth term is 3n + 2."),
    sayonly("We want terms below 50, so solve \\(3n + 2 < 50\\). Take 2 from both sides first."),
    box("50 − 2 = ", 48, "This leaves 3n < 48.", phase="substitute"),
    box("48 ÷ 3 = ", 16, "Divide 48 by 3, giving n < 16.", phase="substitute"),
    sayonly("So \\(n < 16\\). As \\(n\\) must be a whole number, the largest is 15."),
    box("Check the 15th term: 3 × 15 + 2 = ", 47, "45 plus 2.", phase="substitute",
        done="47 is below 50, and the 16th term is exactly 50, so 15 terms are less than 50."),
]

pb["gold"][0]["guided_steps"] = [
    sayonly("We want the position whose value is 100, so solve \\(3n + 7 = 100\\)."),
    box("Take 7 from both sides: 100 − 7 = ", 93, "This leaves 3n = 93."),
    box("Divide by 3: 93 ÷ 3 = ", 31, "Divide 93 by 3.", phase="substitute"),
    box("Check: 3 × 31 + 7 = ", 100, "93 plus 7.", phase="substitute",
        done="It gives 100, so the 31st term has value 100."),
]

pb["gold"][1]["guided_steps"] = [
    sayonly("The two sequences are equal when \\(4n + 1 = 3n + 5\\). Get the n terms on one side by subtracting \\(3n\\)."),
    box("4n − 3n = ", 1, "Subtract the n terms: 4 − 3.", post="n", done="This leaves n + 1 = 5."),
    box("Take 1 from both sides: 5 − 1 = ", 4, "Subtract 1 from 5.", phase="substitute"),
    box("Check the first sequence at n = 4: 4 × 4 + 1 = ", 17, "16 plus 1.", phase="substitute"),
    box("Check the second at n = 4: 3 × 4 + 5 = ", 17, "12 plus 5.", phase="substitute",
        done="Both give 17, so position 4 is where they first match."),
]

pb["gold"][2]["guided_steps"] = [
    sayonly("List the first five terms of \\(2n + 1\\). Each is 2 more than the last."),
    box("The 5th term: 2 × 5 + 1 = ", 11, "10 plus 1.", done="So the terms are 3, 5, 7, 9, 11."),
    sayonly("Now add the five terms together."),
    box("3 + 5 + 7 = ", 15, "Add the first three terms.", phase="substitute"),
    box("15 + 9 + 11 = ", 35, "Add on the last two terms.", phase="substitute"),
    box("Check: the middle term 7 times the 5 terms: 5 × 7 = ", 35, "5 times 7.", phase="substitute",
        done="5 × 7 = 35 matches the total, so the sum is 35."),
]

pb["gold"][4]["guided_steps"] = [
    sayonly("Find the rule for \\(3, 8, 13, 18, \\ldots\\) first."),
    box("Common difference: 8 − 3 = ", 5, "Subtract consecutive terms."),
    box("Constant: first term − d = 3 − 5 = ", -2, "Take the common difference off the first term.",
        done="So the nth term is 5n − 2."),
    sayonly("We want the first term over 200, so solve \\(5n - 2 > 200\\). Add 2 to both sides."),
    box("200 + 2 = ", 202, "This gives 5n > 202.", phase="substitute"),
    sayonly("Now find the smallest whole \\(n\\). Since \\(5 \\times 40 = 200\\) is too small, try \\(n = 41\\)."),
    box("5 × 41 = ", 205, "Multiply 5 by 41; it is over 202.", phase="substitute"),
    box("The term value: 205 − 2 = ", 203, "Subtract 2 from 205.", phase="substitute",
        done="203 is the first term over 200; the 40th term is only 198."),
]

# ================================================================ 6. TIER GUIDES
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: nth term of an increasing sequence",
        "steps": [
            "Find the <strong>common difference</strong> \\(d\\): subtract one term from the next.",
            "Write the formula as \\(dn\\) plus a constant.",
            "The constant is \\(c = \\text{first term} - d\\). The nth term is \\(dn + c\\).",
        ],
        "example": {
            "question": "Find the nth term of 5, 9, 13, 17, ...",
            "steps": [
                {"label": "Common difference", "content": "<p>\\(d = 9 - 5 = 4\\)</p>"},
                {"label": "Constant", "content": "<p>\\(c = 5 - 4 = 1\\)</p>"},
                {"label": "Check", "content": "<p>\\(4(1) + 1 = 5\\) ✔</p>"},
                {"label": "Answer", "content": "<p><strong>\\(4n + 1\\)</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: decreasing sequences and finding a term",
        "steps": [
            "For a falling sequence, \\(d\\) is <strong>negative</strong>.",
            "The constant is \\(c = \\text{first term} - d\\); subtracting a negative adds.",
            "To find a term, substitute its position; to test membership, set \\(dn + c\\) equal to the number and solve.",
        ],
        "example": {
            "question": "Find the nth term of 25, 21, 17, 13, ...",
            "steps": [
                {"label": "Common difference", "content": "<p>\\(d = 21 - 25 = -4\\)</p>"},
                {"label": "Constant", "content": "<p>\\(c = 25 - (-4) = 29\\)</p>"},
                {"label": "Check", "content": "<p>\\(-4(1) + 29 = 25\\) ✔</p>"},
                {"label": "Answer", "content": "<p><strong>\\(-4n + 29\\)</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: working backwards and comparing sequences",
        "steps": [
            "To find which term has a value, set \\(dn + c\\) equal to it and solve for \\(n\\).",
            "A positive whole-number \\(n\\) means the value is in the sequence.",
            "To compare two sequences, set the formulas equal; to sum terms, list them and add.",
        ],
        "example": {
            "question": "The nth term is \\(3n + 2\\). Which term equals 47?",
            "steps": [
                {"label": "Set equal", "content": "<p>\\(3n + 2 = 47\\)</p>"},
                {"label": "Solve", "content": "<p>\\(3n = 45\\), so \\(n = 15\\)</p>"},
                {"label": "Check", "content": "<p>\\(3(15) + 2 = 47\\) ✔</p>"},
                {"label": "Answer", "content": "<p><strong>the 15th term</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ================================================================ 7. GUIDED (opener + teach)
pd["guided"] = {
    "opener": {
        "steps": [
            sayonly("No algebra yet. A plumber charges a £20 call-out, then £15 for each hour.<br>1 hour → £35, 2 hours → £50, 3 hours → £65."),
            box("So 4 hours would cost £", 80, "Add one more £15 onto the 3-hour price of £65."),
            sayonly("You added £15 because that is the <strong>common difference</strong>: the fixed step between the terms £35, £50, £65, ..."),
            box("Jump ahead. For 10 hours the hours cost 10 × £15 = £150, plus the £20 call-out, so £", 170, "Add 150 and 20."),
            sayonly("That is the whole idea. The step (£15) becomes \\(15n\\), the call-out (£20) is the constant, so the cost is \\(15n + 20\\). Algebra writes any linear sequence as \\(T(n) = dn + c\\), and putting \\(n = 10\\) gives £170 straight away."),
        ],
    },
    "teach": {
        "bronze": {
            "display": "Find the nth term of \\(3, 7, 11, 15, \\ldots\\)",
            "steps": [
                sayonly("Turn a sequence into a formula \\(dn + c\\). That is the whole bronze move. Find the rule for \\(3, 7, 11, 15, \\ldots\\)"),
                box("Common difference: 7 − 3 = ", 4, "Subtract the first term from the second."),
                box("So the dn part is 4n. Constant: first term − d = 3 − 4 = ", -1, "Take 4 off the first term.",
                    done="So the nth term is 4n − 1."),
                sayonly("Check the rule regenerates the sequence."),
                box("Term 1: 4 × 1 − 1 = ", 3, "4 minus 1."),
                box("Term 2: 4 × 2 − 1 = ", 7, "8 minus 1.",
                    done="Both match, so 4n − 1 is the rule. Gone. That was the whole point."),
            ],
        },
        "silver": {
            "display": "Find the nth term of \\(30, 26, 22, 18, \\ldots\\)",
            "steps": [
                sayonly("This sequence goes DOWN. The new move: a <strong>negative</strong> common difference. Find the rule for \\(30, 26, 22, 18, \\ldots\\)"),
                box("Common difference: 26 − 30 = ", -4, "Second term minus first; it comes out negative."),
                box("Constant: first term − d = 30 − (−4) = ", 34, "Subtracting a negative adds: 30 + 4.",
                    done="The double negative is the trap. Gone. That was the whole point."),
                sayonly("So the nth term is \\(-4n + 34\\). Check it."),
                box("Term 1: −4 × 1 + 34 = ", 30, "−4 plus 34."),
                box("Term 3: −4 × 3 + 34 = ", 22, "−12 plus 34.",
                    done="Both match, so −4n + 34 is right."),
            ],
        },
        "gold": {
            "display": "The nth term of a sequence is \\(4n + 3\\). Which term equals 51?",
            "steps": [
                sayonly("Now work BACKWARDS: given a value, find its position. Solve \\(4n + 3 = 51\\). That reversal is the gold move."),
                box("Take 3 from both sides: 51 − 3 = ", 48, "This leaves 4n = 48."),
                box("Divide by 4: 48 ÷ 4 = ", 12, "Divide 48 by 4.", done="So 51 is the 12th term."),
                sayonly("Check by working forwards."),
                box("4 × 12 = ", 48, "4 times 12."),
                box("48 + 3 = ", 51, "Add 3.",
                    done="It gives 51, so position 12 is right. Gone. That was the whole point."),
            ],
        },
    },
}

# ================================================================ 8. METHOD CARD trim + em-dash cleanup
pd["method_card"]["content"] = (
    "<p>A <strong>linear sequence</strong> goes up or down by the same amount each time. "
    "That fixed step is the <strong>common difference</strong> \\(d\\).</p>"
    "<p>The nth term is \\(T(n) = dn + c\\). Find \\(d\\) by subtracting consecutive terms, "
    "then the constant \\(c = \\text{first term} - d\\).</p>"
    "<p>To find a term, substitute its position \\(n\\). To test whether a number is in the sequence, "
    "set \\(dn + c\\) equal to it and solve: a positive whole-number \\(n\\) means it is a term.</p>"
)

# ================================================================ 9. TIER DESCRIPTION em-dash fix
pb["gold_description"] = "Reverse problems: find n given a term value, and recognise other sequence types"

# ================================================================ 10. Preserve-field em-dash cleanup (validator scans all except 'note')
# worked_examples labels use em dashes -> colons
for we in pd.get("worked_examples", []):
    for st in we.get("steps", []):
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")
# G4 kept misconception expect_note had an em dash
for m in pb["gold"][4].get("misconceptions", []):
    if "expect_note" in m and "—" in m["expect_note"]:
        m["expect_note"] = m["expect_note"].replace(" — ", ", ").replace("—", ",")

# ================================================================ WRITE
with open("lesson_algebra-L13.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("written lesson_algebra-L13.json")

# quick em-dash self-scan
EM = "—"
def scan(o, p):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "note":
                continue
            scan(v, p + "." + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            scan(v, p + "[%d]" % i)
    elif isinstance(o, str) and EM in o:
        print("EMDASH", p)
scan(pd, "pd")
print("self-scan done")
