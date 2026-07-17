# -*- coding: utf-8 -*-
import json, io

BASE = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\_L04ocr_live.json"
OUT  = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\lesson_maths-ocr_algebra-L04.json"

pd = json.load(io.open(BASE, encoding="utf-8"))

# ---------- method_card (slim reference) ----------
pd["method_card"] = {
    "title": "Formulae & Substitution",
    "steps": [
        "Substitute: replace each letter with its value, using brackets for negatives.",
        "Calculate using BIDMAS: powers first, then × and ÷, then + and −.",
        "To rearrange, undo operations with inverses to isolate the new subject.",
        "If the subject appears twice, collect the terms, factorise it out, then divide.",
    ],
    "content": ("<p><strong>Substitution</strong> means replacing letters with numbers, then "
                "calculating with BIDMAS. Always bracket negatives: if \\(x = -3\\), then "
                "\\(x^2 = (-3)^2 = 9\\), not \\(-9\\).</p>"
                "<p><strong>Rearranging</strong> a formula makes a different letter the subject. "
                "Use inverse operations, just like solving an equation. Multiply out fractions, "
                "and square both sides to remove a square root. If the new subject appears more "
                "than once, gather its terms on one side, factorise it out, then divide.</p>"),
    "example": ("<p><strong>Given</strong> \\(y = 3x^2 - 5\\), find \\(y\\) when \\(x = -2\\)</p>"
                "<p><strong>Step 1:</strong> Substitute: \\(y = 3(-2)^2 - 5\\)</p>"
                "<p><strong>Step 2:</strong> \\(= 3(4) - 5 = 12 - 5 = 7\\)</p>"
                "<p><strong>Answer:</strong> \\(y = 7\\)</p>"),
}

# ---------- worked_examples: strip em dashes from labels ----------
for we in pd.get("worked_examples", []):
    for st in we.get("steps", []):
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

pb = pd["problem_bank"]

# ---------- tier descriptions ----------
pb["bronze_description"] = "Substitute whole and negative numbers into a simple expression and calculate with BIDMAS."
pb["silver_description"] = "Substitute into expressions with powers and negatives, or rearrange a two-step formula."
pb["gold_description"]   = "Substitute into harder formulae, or make a variable the subject when it sits in a fraction, a root, or appears twice."

def box(pre, answer, hint, post="", say=None, done=None, phase=False):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase: d["phase"] = "substitute"
    return d

def sayonly(say):
    return {"say": say}

# =========================================================
# BRONZE
# =========================================================
b = pb["bronze"]

b[0]["hint"] = "Multiply 3 by 5 first, then add 2."
b[0]["misconceptions"] = [
    {"pattern": "wrong_order", "message": "BIDMAS says multiply before you add. 3 × 5 = 15, then + 2 = 17. Adding first gives 3 × 7 = 21, which is wrong.", "expect": 21},
    {"pattern": "drops_constant", "message": "Do not forget the + 2. After 3 × 5 = 15 you still add 2 to reach 17.", "expect": 15},
]
b[0]["guided_steps"] = [
    sayonly("Substitute a = 5 into \\(3a + 2\\)."),
    box("Multiply first: 3 × 5 = ", 15, "Multiply 3 by 5."),
    box("Now add 2: 15 + 2 = ", 17, "Add 2 to 15.", phase=True),
    box("Check, all at once: 3(5) + 2 = ", 17, "Work out 3 times 5, then add 2.",
        done="15 + 2 = 17, matching the original expression, so the answer is 17."),
]

b[1]["hint"] = "Only the x is doubled: work out 2 times 4, then add y."
b[1]["misconceptions"] = [
    {"pattern": "brackets_all", "message": "Only x is doubled, not y. 2 × 4 = 8, then + 3 = 11. Doubling the total gives 2 × 7 = 14, which is wrong.", "expect": 14},
    {"pattern": "drops_coeff", "message": "The 2 multiplies x. 2 × 4 = 8, plus y = 3, gives 11. Just adding 4 + 3 = 7 ignores the 2.", "expect": 7},
]
b[1]["guided_steps"] = [
    sayonly("Substitute x = 4 and y = 3 into \\(2x + y\\)."),
    box("Only x is doubled: 2 × 4 = ", 8, "Multiply 2 by 4."),
    box("Add y = 3: 8 + 3 = ", 11, "Add 3 to 8.", phase=True),
    box("Check: 2(4) + 3 = ", 11, "Double 4, then add 3.",
        done="8 + 3 = 11, so the answer is 11."),
]

b[2]["hint"] = "Square 6 first (6 times 6), then subtract 10."
b[2]["misconceptions"] = [
    {"pattern": "double_not_square", "message": "n² means n × n = 36, not 2 × 6 = 12. Then 36 − 10 = 26.", "expect": 2},
    {"pattern": "arithmetic", "message": "Square first, then subtract: 6² = 36, and 36 − 10 = 26.", "expect": None},
]
b[2]["guided_steps"] = [
    sayonly("Substitute n = 6 into \\(n^2 - 10\\)."),
    box("Square first: 6 × 6 = ", 36, "n² means 6 times 6."),
    box("Subtract 10: 36 − 10 = ", 26, "Take 10 away from 36.", phase=True),
    box("Check: 6² − 10 = ", 26, "36 minus 10.",
        done="36 − 10 = 26, so the answer is 26. Square the number, do not double it."),
]

b[3]["hint"] = "pq means p times q, so multiply 3 by 7."
b[3]["misconceptions"] = [
    {"pattern": "add", "message": "pq means p × q, not p + q. 3 × 7 = 21, not 3 + 7 = 10.", "expect": 10},
    {"pattern": "arithmetic", "message": "Letters next to each other multiply: 3 × 7 = 21.", "expect": None},
]
b[3]["guided_steps"] = [
    sayonly("pq means p × q. Substitute p = 3 and q = 7, and build 3 × 7."),
    box("Two sevens: 7 + 7 = ", 14, "Add two sevens."),
    box("Add one more 7: 14 + 7 = ", 21, "Add 7 to 14.", phase=True),
    box("So pq = 3 × 7 = ", 21, "Three sevens make 21.",
        done="3 × 7 = 21. pq means multiply, not add."),
]

b[4]["hint"] = "Multiply 5 by negative 2; the answer is negative."
b[4]["misconceptions"] = [
    {"pattern": "sign_error", "message": "A positive times a negative is negative. 5 × (−2) = −10, not +10.", "expect": 10},
    {"pattern": "arithmetic", "message": "5 × 2 = 10, and the sign is negative, so 5x = −10.", "expect": None},
]
b[4]["guided_steps"] = [
    sayonly("Substitute x = −2 into \\(5x\\), which means 5 × x."),
    box("Ignore the sign for a moment: 5 × 2 = ", 10, "Five twos make 10."),
    box("Positive × negative is negative, so 5 × (−2) = ", -10, "Put the negative sign back on.", phase=True),
    box("Check: 5 × (−2) = ", -10, "Multiply 5 by negative 2.",
        done="5 × 2 = 10 and the sign is negative, so 5x = −10."),
]

b[5]["hint"] = "Divide 8 by 2 first, then add 3."
b[5]["misconceptions"] = [
    {"pattern": "wrong_order", "message": "Divide before you add (BIDMAS). 8 ÷ 2 = 4, then + 3 = 7. Adding first gives 11 ÷ 2 = 5.5.", "expect": 5.5},
    {"pattern": "arithmetic", "message": "Halve 8 to get 4, then add 3 to reach 7.", "expect": None},
]
b[5]["guided_steps"] = [
    sayonly("Substitute t = 8 into \\(\\frac{t}{2} + 3\\)."),
    box("Divide first (BIDMAS): 8 ÷ 2 = ", 4, "Halve 8."),
    box("Add 3: 4 + 3 = ", 7, "Add 3 to 4.", phase=True),
    box("Check: 8 ÷ 2 + 3 = ", 7, "Halve 8, then add 3.",
        done="4 + 3 = 7, so the answer is 7. Divide before you add."),
]

b[6]["hint"] = "Square each number separately, then add the two squares."
b[6]["misconceptions"] = [
    {"pattern": "add_then_square", "message": "Square each term on its own: 3² + 4² = 9 + 16 = 25. Squaring the sum gives (3 + 4)² = 49, which is wrong.", "expect": 49},
    {"pattern": "arithmetic", "message": "9 + 16 = 25.", "expect": None},
]
b[6]["guided_steps"] = [
    sayonly("Substitute a = 3 and b = 4 into \\(a^2 + b^2\\). Square each letter separately."),
    box("a² = 3 × 3 = ", 9, "3 times 3."),
    box("b² = 4 × 4 = ", 16, "4 times 4."),
    box("Add the two squares: 9 + 16 = ", 25, "Add 9 and 16.", phase=True),
    box("Check: 3² + 4² = ", 25, "9 plus 16.",
        done="9 + 16 = 25. Square each term on its own, do not add first and then square."),
]

b[7]["hint"] = "A negative number squared is positive: multiply negative 4 by negative 4."
b[7]["misconceptions"] = [
    {"pattern": "negative_square", "message": "(−4)² = (−4) × (−4) = +16. A negative squared is positive, so it is not −16.", "expect": -16},
    {"pattern": "arithmetic", "message": "4 × 4 = 16, and negative times negative is positive.", "expect": None},
]
b[7]["guided_steps"] = [
    sayonly("Substitute m = −4 into \\(m^2\\). Write it in brackets: (−4)²."),
    box("Ignoring signs, 4 × 4 = ", 16, "Four fours make 16."),
    box("Negative × negative is positive, so (−4)² = ", 16, "The result is positive 16.", phase=True),
    box("Check: (−4) × (−4) = ", 16, "Multiply negative 4 by negative 4.",
        done="(−4)(−4) = +16, so m² = 16, not −16."),
]

# =========================================================
# SILVER
# =========================================================
s = pb["silver"]

s[0]["hint"] = "Square negative 3 to get 9, then watch the double negative in minus 4x."
s[0]["misconceptions"] = [
    {"pattern": "negative_square", "message": "(−3)² = 9, a positive. So 2 × 9 = 18 and −4 × (−3) = +12, giving 30. Treating (−3)² as −9 gives 2(−9) + 12 = −6.", "expect": -6},
    {"pattern": "sign_error", "message": "−4 × (−3) = +12, not −12. So 18 + 12 = 30, not 18 − 12 = 6.", "expect": 6},
]
s[0]["guided_steps"] = [
    sayonly("Substitute x = −3 into \\(2x^2 - 4x\\), keeping brackets round the negative."),
    box("Square first: (−3)² = ", 9, "Negative 3 times negative 3."),
    box("So 2x² = 2 × 9 = ", 18, "Multiply 2 by 9."),
    box("Second term: −4 × (−3) = ", 12, "Negative 4 times negative 3 is positive.", phase=True),
    box("Add: 18 + 12 = ", 30, "Add 18 and 12."),
    box("Check: 2(−3)² − 4(−3) = 18 + 12 = ", 30, "18 plus 12.",
        done="18 + 12 = 30. The square is positive and minus a negative adds."),
]

s[1]["hint"] = "Subtracting a negative adds: minus 2 times negative 5 is plus 10."
s[1]["misconceptions"] = [
    {"pattern": "sign_error", "message": "−2 × (−5) = +10. So 6 + 10 = 16. Making it 6 − 10 gives −4.", "expect": -4},
    {"pattern": "arithmetic", "message": "3(2) − 2(−5) = 6 + 10 = 16.", "expect": None},
]
s[1]["guided_steps"] = [
    sayonly("Substitute a = 2 and b = −5 into \\(3a - 2b\\)."),
    box("First term: 3 × 2 = ", 6, "Multiply 3 by 2."),
    box("Second term: −2 × (−5) = ", 10, "Negative 2 times negative 5 is positive.", phase=True),
    box("Combine: 6 + 10 = ", 16, "Add 6 and 10."),
    box("Check: 3(2) − 2(−5) = 6 + 10 = ", 16, "6 plus 10.",
        done="Subtracting −5 adds 10, so 6 + 10 = 16."),
]

# s[2] MC: y = 4x + 7
s[2]["hint"] = "Subtract 7 from both sides first, then divide by 4."
for m in s[2]["misconceptions"]:
    m["expect"] = None

# s[3] MC: A = pi r^2
s[3]["hint"] = "Divide by pi first, then take the square root of both sides."
s[3]["misconceptions"][1]["message"] = "A = πr² is the area. Divide by π, then square root. Do not use the circumference formula."
for m in s[3]["misconceptions"]:
    m["expect"] = None

s[4]["hint"] = "Work out a times t first, then add u."
s[4]["misconceptions"] = [
    {"pattern": "wrong_order", "message": "Multiply at before adding u. 3 × 4 = 12, then + 5 = 17. Adding first gives (5 + 3) × 4 = 32.", "expect": 32},
    {"pattern": "arithmetic", "message": "at = 3 × 4 = 12, then v = 5 + 12 = 17.", "expect": None},
]
s[4]["guided_steps"] = [
    sayonly("Substitute u = 5, a = 3, t = 4 into \\(v = u + at\\)."),
    box("Multiply at first: 3 × 4 = ", 12, "Multiply a by t."),
    box("Add u = 5: 5 + 12 = ", 17, "Add 5 to 12.", phase=True),
    box("Check: 5 + 3 × 4 = ", 17, "Times 3 by 4, then add 5.",
        done="3 × 4 = 12, then + 5 = 17. Multiply before adding."),
]

s[5]["hint"] = "Cube keeps the sign: negative 1 cubed is negative 1."
s[5]["misconceptions"] = [
    {"pattern": "minus_sign", "message": "The last term is −x = −(−1) = +1. So −1 + 2 + 1 = 2. Reading −x as −1 gives −1 + 2 − 1 = 0.", "expect": 0},
    {"pattern": "cube_sign", "message": "(−1)³ = −1 (odd power keeps the sign). Using (−1)³ = +1 gives 1 + 2 + 1 = 4.", "expect": 4},
]
s[5]["guided_steps"] = [
    sayonly("Substitute x = −1 into \\(x^3 + 2x^2 - x\\), keeping brackets."),
    box("Cube: (−1)³ = ", -1, "Negative 1 times negative 1 times negative 1."),
    box("Square term: 2 × (−1)² = 2 × 1 = ", 2, "Negative 1 squared is 1, then times 2."),
    box("Last term: −x = −(−1) = ", 1, "Subtracting negative 1 gives plus 1.", phase=True),
    box("Add them: −1 + 2 + 1 = ", 2, "Combine negative 1, 2 and 1."),
    box("Check: (−1)³ + 2(−1)² − (−1) = −1 + 2 + 1 = ", 2, "Add the three terms.",
        done="−1 + 2 + 1 = 2. Odd powers keep the sign, even powers turn positive."),
]

# s[6] MC: make t the subject of v = u + at
s[6]["hint"] = "Subtract u first, then divide by a."
for m in s[6]["misconceptions"]:
    m["expect"] = None

# =========================================================
# GOLD
# =========================================================
g = pb["gold"]

# g[0] MC: make x subject of y = (3x+1)/(x-2)
g[0]["hint"] = "Cross multiply, gather the x terms on one side, then factorise x out."
for m in g[0]["misconceptions"]:
    m["expect"] = None

# g[1] MC: make a subject of s = ut + 1/2 a t^2
g[1]["hint"] = "Subtract ut, multiply both sides by 2, then divide by t squared."
for m in g[1]["misconceptions"]:
    m["expect"] = None

# g[2] single_value: (3x^3 + x^2 - 4)/(x+1), x=2 -> 8
g[2]["hint"] = "Work out the numerator and denominator separately, then divide."
g[2]["misconceptions"] = [
    {"pattern": "cube_as_mult", "message": "x³ means 2 × 2 × 2 = 8, so 3x³ = 24. Using 3 × 2 × 3 = 18 by mistake gives 18 ÷ 3 = 6.", "expect": 6},
    {"pattern": "arithmetic", "message": "Numerator: 3(8) + 4 − 4 = 24. Denominator: 2 + 1 = 3. So 24 ÷ 3 = 8.", "expect": None},
]
g[2]["guided_steps"] = [
    sayonly("Substitute x = 2 into \\(\\frac{3x^3 + x^2 - 4}{x + 1}\\). Work the numerator and denominator separately."),
    box("Cube term: 3 × 2³ = 3 × 8 = ", 24, "2 cubed is 8, then times 3."),
    box("Square term: 2² = ", 4, "2 times 2."),
    box("Numerator: 24 + 4 − 4 = ", 24, "Add 4 then subtract 4.", phase=True),
    box("Denominator: 2 + 1 = ", 3, "Add 1 to 2."),
    box("Divide: 24 ÷ 3 = ", 8, "Share 24 into 3 equal parts."),
    box("Check: numerator 24, denominator 3, so 24 ÷ 3 = ", 8, "24 divided by 3.",
        done="24 ÷ 3 = 8, so the answer is 8."),
]

# g[3] MC: make x subject of y = sqrt(5x-1)
g[3]["hint"] = "Square both sides to remove the root, then rearrange for x."
for m in g[3]["misconceptions"]:
    m["expect"] = None

# g[4] single_value: b^2 - 4ac, a=-2,b=3,c=-1 -> 1
g[4]["hint"] = "Square b, then work out 4ac carefully with the signs, and subtract."
g[4]["misconceptions"] = [
    {"pattern": "sign_error", "message": "4ac = 4 × (−2) × (−1) = +8, so 9 − 8 = 1. Treating 4ac as −8 gives 9 − (−8) = 17.", "expect": 17},
    {"pattern": "square_sign", "message": "b² = 3² = 9. The two negatives in 4ac multiply to +8, so 9 − 8 = 1.", "expect": None},
]
g[4]["guided_steps"] = [
    sayonly("Substitute a = −2, b = 3, c = −1 into \\(b^2 - 4ac\\)."),
    box("Square b: 3² = ", 9, "3 times 3."),
    box("Start 4ac: 4 × (−2) = ", -8, "4 times negative 2."),
    box("Times the last −1: (−8) × (−1) = ", 8, "Negative times negative is positive.", phase=True),
    box("Subtract: 9 − 8 = ", 1, "Take 8 from 9."),
    box("Check: 3² − 4(−2)(−1) = 9 − 8 = ", 1, "9 minus 8.",
        done="4ac = +8, so 9 − 8 = 1."),
]

# =========================================================
# tier_guides
# =========================================================
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: substitute a number into an expression",
        "steps": [
            "Replace each letter with its value. Put negatives in brackets, so 5x with x = −2 becomes 5(−2).",
            "Follow BIDMAS: powers and brackets first, then × and ÷, then + and −.",
            "Write the final number, then read the original expression back to check every term was used.",
        ],
        "example": {
            "question": "If x = 4, find 3x − 5",
            "steps": [
                {"label": "Substitute", "content": "<p>\\(3(4) - 5\\)</p>"},
                {"label": "Multiply", "content": "<p>\\(3 \\times 4 = 12\\)</p>"},
                {"label": "Check", "content": "<p>\\(12 - 5 = 7\\), and \\(3(4) - 5 = 7\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(7\\)</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: powers, negatives, and two-step formulae",
        "steps": [
            "For powers, square or cube the value on its own. A negative squared is positive: (−3)² = 9, but (−1)³ = −1.",
            "Subtracting a negative adds: −2 × (−5) = +10. Keep every sign inside brackets as you work.",
            "To rearrange, undo the operations in reverse order using inverses, one step at a time.",
        ],
        "example": {
            "question": "If x = −2, find x² + 3x",
            "steps": [
                {"label": "Substitute", "content": "<p>\\((-2)^2 + 3(-2)\\)</p>"},
                {"label": "Powers", "content": "<p>\\((-2)^2 = 4\\), so \\(4 + 3(-2)\\)</p>"},
                {"label": "Check", "content": "<p>\\(4 - 6 = -2\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(-2\\)</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: harder formulae and rearranging",
        "steps": [
            "Substitute exactly, keeping powers and brackets, then simplify the numerator and denominator separately before dividing.",
            "To make a new subject, use inverses: square both sides to remove a root, or multiply out a fraction first.",
            "If the new subject appears twice, gather those terms on one side, factorise it out, then divide.",
        ],
        "example": {
            "question": "Make x the subject: y = (x + 4)/3",
            "steps": [
                {"label": "Clear the fraction", "content": "<p>Multiply by 3: \\(3y = x + 4\\)</p>"},
                {"label": "Isolate x", "content": "<p>Subtract 4: \\(x = 3y - 4\\)</p>"},
                {"label": "Check", "content": "<p>\\((3y - 4 + 4) \\div 3 = 3y \\div 3 = y\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(x = 3y - 4\\)</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# =========================================================
# guided: opener + teach
# =========================================================
FM_SVG = ('<svg viewBox="0 0 260 84" role="img" aria-label="A function machine: miles go in, '
          'are multiplied by 2, then 3 is added, and the cost in pounds comes out" '
          'style="max-width:260px;font-family:Inter,sans-serif">'
          '<text x="6" y="46" fill="currentColor" font-size="11">miles</text>'
          '<line x1="40" y1="42" x2="60" y2="42" stroke="currentColor" stroke-width="1.5"/>'
          '<polygon points="60,38 68,42 60,46" fill="currentColor"/>'
          '<rect x="70" y="28" width="42" height="28" rx="4" fill="#60a5fa" fill-opacity="0.3" stroke="currentColor" stroke-width="1.2"/>'
          '<text x="91" y="46" fill="currentColor" font-size="12" text-anchor="middle">× 2</text>'
          '<line x1="114" y1="42" x2="136" y2="42" stroke="currentColor" stroke-width="1.5"/>'
          '<polygon points="136,38 144,42 136,46" fill="currentColor"/>'
          '<rect x="146" y="28" width="42" height="28" rx="4" fill="#34d399" fill-opacity="0.3" stroke="currentColor" stroke-width="1.2"/>'
          '<text x="167" y="46" fill="currentColor" font-size="12" text-anchor="middle">+ 3</text>'
          '<line x1="190" y1="42" x2="210" y2="42" stroke="currentColor" stroke-width="1.5"/>'
          '<polygon points="210,38 218,42 210,46" fill="currentColor"/>'
          '<text x="222" y="46" fill="currentColor" font-size="11">cost £</text>'
          '</svg>')

pd["guided"] = {
    "opener": {
        "label": "Before any formula",
        "display": (FM_SVG +
                    "<p>A taxi charges £3 to get in, plus £2 for every mile. "
                    "The machine above is that rule: put in the miles, times 2, add 3, out comes the cost.</p>"),
        "steps": [
            box("A 4-mile trip: £3 + £2 × 4 = £", 11,
                "Two pounds each for 4 miles is £8, plus the £3 start.",
                say="You do not need algebra yet. Just work out the cost with common sense."),
            box("A 6-mile trip: £3 + £2 × 6 = £", 15,
                "Two pounds times 6 miles is £12, plus the £3 start."),
            sayonly("Each time you did the same thing: times the miles by 2, then add 3. "
                    "Written as a formula that is \\(C = 3 + 2m\\), where m is the number of miles. "
                    "Putting a number in place of m and working it out is called <strong>substitution</strong>. "
                    "You already know how to do it."),
        ],
    },
    "teach": {
        "bronze": {
            "label": "Together: your first one",
            "display": "If \\(x = 5\\) and \\(y = 2\\), find \\(3x - 2y\\)",
            "steps": [
                box("Substitute both letters. First 3 × 5 = ", 15, "Multiply 3 by 5.",
                    say="Replace x with 5 and y with 2, then work out each part."),
                box("Second term: 2 × 2 = ", 4, "Multiply 2 by y = 2."),
                box("Now subtract: 15 − 4 = ", 11, "Take 4 away from 15."),
                box("Check, all at once: 3(5) − 2(2) = ", 11, "15 minus 4.",
                    done="15 − 4 = 11. Substitute every letter, then follow BIDMAS."),
            ],
        },
        "silver": {
            "label": "Together: the silver move",
            "display": "If \\(x = -4\\), find \\(x^2 + 5x\\)",
            "steps": [
                box("Square the value: (−4)² = ", 16, "Negative 4 times negative 4.",
                    say="Substitute x = −4. Deal with the power first, keeping the bracket."),
                box("The 5x term: 5 × (−4) = ", -20, "Positive 5 times negative 4 is negative."),
                box("Add them: 16 + (−20) = ", -4, "16 minus 20."),
                box("Check: (−4)² + 5(−4) = 16 − 20 = ", -4, "16 minus 20.",
                    done="16 − 20 = −4. The square is positive, the 5x term is negative: mind every sign."),
            ],
        },
        "gold": {
            "label": "Together: the gold move",
            "display": "If \\(x = -3\\), find \\(\\frac{2x^2 - x}{x + 4}\\)",
            "steps": [
                box("Numerator first. 2 × (−3)² = 2 × 9 = ", 18, "Square negative 3 to get 9, then times 2.",
                    say="Substitute x = −3. Work the top and the bottom separately."),
                box("Subtract the −x term: 18 − (−3) = ", 21, "Subtracting negative 3 adds 3."),
                box("Denominator: −3 + 4 = ", 1, "Add 4 to negative 3."),
                box("Divide: 21 ÷ 1 = ", 21, "Anything divided by 1 is itself.",
                    done="Top 21, bottom 1, so 21 ÷ 1 = 21. Simplify numerator and denominator separately, then divide."),
            ],
        },
    },
}

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("written", OUT)
print("bronze", len(pb["bronze"]), "silver", len(pb["silver"]), "gold", len(pb["gold"]))
