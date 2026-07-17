# -*- coding: utf-8 -*-
import json

MINUS = "−"  # −
TIMES = "×"  # ×
SUP2 = "²"   # ²

d = json.load(open('_L06alg_live.json', encoding='utf-8'))
pd = d['practice_data']
pb = pd['problem_bank']

# ---- 1. method_card: trim to 4 steps, slim content ----
pd['method_card']['steps'] = [
    "Multiply the two ends, a " + TIMES + " c",
    "Find two numbers that multiply to ac and add to b",
    "Split the middle bx term into those two numbers, then group into pairs",
    "Factorise each pair and write the two brackets, then check by expanding",
]
pd['method_card']['content'] = (
    "<p>When the coefficient of \\(x^2\\) is not 1, use the <strong>ac method</strong> "
    "(split the middle, then group).</p>"
    "<p>For \\(ax^2 + bx + c\\): multiply \\(a \\times c\\), find two numbers that "
    "multiply to \\(ac\\) and add to \\(b\\), split the middle term with them, group "
    "into two pairs, and factorise each pair to reach two brackets.</p>"
)
# keep existing method_card example (no em dash, fine)

# ---- 2. fix worked_examples em dashes (label " — " -> ": ") ----
for ex in pd.get('worked_examples', []):
    for st in ex.get('steps', []):
        if 'label' in st and '—' in st['label']:
            st['label'] = st['label'].replace(' — ', ': ')

# ---- 3. tier descriptions ----
pb['bronze_description'] = "All terms positive: multiply the ends, split the middle term, then group into two brackets."
pb['silver_description'] = "Negative signs appear: find two numbers that still multiply to ac and add to b, signs and all."
pb['gold_description'] = "Tougher coefficients and factorising completely: take out any common factor first, then split."

# ---- 4. per-problem hints + rewritten misconceptions (with expect index) ----
# table: {(tier,i): (hint, [ (expect, pattern, message, note), ... ]) }
def M(expect, pattern, message, note):
    return {"pattern": pattern, "expect": expect, "message": message, "note": note}

data = {
 ("bronze",0): ("Multiply the ends (2" + TIMES + "3 = 6), find two numbers that multiply to 6 and add to 7, then split the middle.", [
    M(1, "bracket_swap", "You have the right numbers but in the wrong brackets. (2x+3)(x+1) expands to 2x" + SUP2 + "+5x+3, not 2x" + SUP2 + "+7x+3. Swap them to (2x+1)(x+3).", "opt1 (2x+3)(x+1) gives middle 5x"),
    M(3, "sign_error", "With +3 at the end and +7 in the middle, both brackets need a plus. (2x" + MINUS + "1)(x" + MINUS + "3) gives a middle of " + MINUS + "7x. Use (2x+1)(x+3).", "opt3 gives -7x"),
 ]),
 ("bronze",1): ("Multiply the ends (3" + TIMES + "2 = 6), find two numbers that multiply to 6 and add to 7, then split the middle.", [
    M(1, "bracket_swap", "Right numbers, wrong brackets. (3x+2)(x+1) expands to 3x" + SUP2 + "+5x+2. Put the 1 next to the 3x: (3x+1)(x+2).", "opt1 gives 5x"),
    M(3, "sign_error", "The ends are both +, so both brackets need a plus. (3x" + MINUS + "1)(x" + MINUS + "2) gives " + MINUS + "7x in the middle. Use (3x+1)(x+2).", "opt3 gives -7x"),
 ]),
 ("bronze",2): ("Multiply the ends (2" + TIMES + "4 = 8), find two numbers that multiply to 8 and add to 9, then split the middle.", [
    M(1, "bracket_swap", "Right numbers, wrong brackets. (2x+4)(x+1) expands to 2x" + SUP2 + "+6x+4. Put the 1 with the 2x: (2x+1)(x+4).", "opt1 gives 6x"),
    M(3, "sign_error", "Everything is positive, so both brackets need a plus. (2x" + MINUS + "1)(x" + MINUS + "4) gives " + MINUS + "9x. Use (2x+1)(x+4).", "opt3 gives -9x"),
 ]),
 ("bronze",3): ("Multiply the ends (5" + TIMES + "2 = 10), find two numbers that multiply to 10 and add to 11, then split the middle.", [
    M(1, "bracket_swap", "Right numbers, wrong brackets. (5x+2)(x+1) expands to 5x" + SUP2 + "+7x+2. Put the 1 with the 5x: (5x+1)(x+2).", "opt1 gives 7x"),
    M(3, "sign_error", "Both ends are positive, so both brackets take a plus. (5x" + MINUS + "1)(x" + MINUS + "2) gives " + MINUS + "11x. Use (5x+1)(x+2).", "opt3 gives -11x"),
 ]),
 ("bronze",4): ("Multiply the ends (3" + TIMES + "4 = 12), find two numbers that multiply to 12 and add to 8, then split the middle.", [
    M(1, "wrong_pair", "(3x+4)(x+1) expands to 3x" + SUP2 + "+7x+4, so the middle is one short. The pair that multiplies to 12 and adds to 8 is 2 and 6: (3x+2)(x+2).", "opt1 gives 7x"),
    M(3, "wrong_pair", "(3x+1)(x+4) expands to 3x" + SUP2 + "+13x+4, so the middle is too big. Use the pair 2 and 6: (3x+2)(x+2).", "opt3 gives 13x"),
 ]),
 ("bronze",5): ("Multiply the ends (2" + TIMES + "5 = 10), find two numbers that multiply to 10 and add to 11, then split the middle.", [
    M(1, "bracket_swap", "Right numbers, wrong brackets. (2x+5)(x+1) expands to 2x" + SUP2 + "+7x+5. Put the 1 with the 2x: (2x+1)(x+5).", "opt1 gives 7x"),
    M(3, "sign_error", "Both ends are positive, so both brackets need a plus. (2x" + MINUS + "1)(x" + MINUS + "5) gives " + MINUS + "11x. Use (2x+1)(x+5).", "opt3 gives -11x"),
 ]),
 ("bronze",6): ("The ends are 4 and 3; try splitting the 4x" + SUP2 + " as 2x times 2x. Find two numbers that multiply to 12 and add to 8.", [
    M(3, "perfect_square", "(2x+3)" + SUP2 + " is 4x" + SUP2 + "+12x+9, which has the wrong middle and end. The two brackets differ here: (2x+1)(2x+3).", "opt3 is (2x+3)^2 = 4x^2+12x+9"),
    M(1, "wrong_pair", "(4x+3)(x+1) expands to 4x" + SUP2 + "+7x+3, so the middle is short. Split the 4x" + SUP2 + " as 2x" + TIMES + "2x: (2x+1)(2x+3).", "opt1 gives 7x"),
 ]),
 ("bronze",7): ("Multiply the ends (2" + TIMES + "1 = 2), find two numbers that multiply to 2 and add to 3, then split the middle.", [
    M(3, "dropped_leading", "(x+1)" + SUP2 + " is x" + SUP2 + "+2x+1, but the x" + SUP2 + " term must be 2x" + SUP2 + ". One bracket needs a 2x: (2x+1)(x+1).", "opt3 is (x+1)^2, no leading 2"),
    M(1, "bracket_swap", "(x+1)(2x+3) expands to 2x" + SUP2 + "+5x+3, the wrong middle and end. Use (2x+1)(x+1).", "opt1 gives 5x+3"),
 ]),
 ("silver",0): ("ac = 3" + TIMES + "6 = 18 and the middle is " + MINUS + "11, so both numbers are negative: " + MINUS + "2 and " + MINUS + "9.", [
    M(1, "not_complete", "(3x" + MINUS + "3)(x" + MINUS + "2) expands to 3x" + SUP2 + MINUS + "9x+6, the wrong middle, and 3x" + MINUS + "3 = 3(x" + MINUS + "1) is not fully factorised. Use (3x" + MINUS + "2)(x" + MINUS + "3).", "opt1 gives -9x"),
    M(2, "sign_error", "With +6 at the end, both brackets need the same sign. (3x+2)(x" + MINUS + "3) gives " + MINUS + "6 at the end. Both are negative here: (3x" + MINUS + "2)(x" + MINUS + "3).", "opt2 gives -7x-6"),
 ]),
 ("silver",1): ("ac = 5" + TIMES + "6 = 30 and the middle is " + MINUS + "13, so both numbers are negative: " + MINUS + "3 and " + MINUS + "10.", [
    M(1, "bracket_swap", "Right numbers, wrong brackets. (5x" + MINUS + "2)(x" + MINUS + "3) expands to 5x" + SUP2 + MINUS + "17x+6. Put the " + MINUS + "3 with the 5x: (5x" + MINUS + "3)(x" + MINUS + "2).", "opt1 gives -17x"),
    M(3, "sign_error", "With +6 at the end both brackets are negative. (x" + MINUS + "3)(5x+2) gives " + MINUS + "6 at the end. Use (5x" + MINUS + "3)(x" + MINUS + "2).", "opt3 gives constant -6"),
 ]),
 ("silver",2): ("ac = 2" + TIMES + "(" + MINUS + "6) = " + MINUS + "12 and the middle is +1, so one number is positive and one negative: +4 and " + MINUS + "3.", [
    M(1, "sign_error", "(2x+3)(x" + MINUS + "2) expands to 2x" + SUP2 + MINUS + "x" + MINUS + "6, so the middle sign is flipped. Swap the signs: (2x" + MINUS + "3)(x+2).", "opt1 gives -x"),
 ]),
 ("silver",3): ("ac = 4" + TIMES + "(" + MINUS + "3) = " + MINUS + "12 and the middle is " + MINUS + "4, so one number is positive and one negative: +2 and " + MINUS + "6.", [
    M(1, "sign_error", "(2x+3)(2x" + MINUS + "1) expands to 4x" + SUP2 + "+4x" + MINUS + "3, so the middle sign is flipped. Swap the signs: (2x" + MINUS + "3)(2x+1).", "opt1 gives +4x"),
 ]),
 ("silver",4): ("ac = 6" + TIMES + "3 = 18, add to 11: the numbers are 2 and 9. Split the 6x" + SUP2 + " as 3x" + TIMES + "2x.", [
    M(1, "wrong_pair", "(6x+1)(x+3) expands to 6x" + SUP2 + "+19x+3, so the middle is too big. Split the 6x" + SUP2 + " as 3x" + TIMES + "2x: (3x+1)(2x+3).", "opt1 gives 19x"),
    M(2, "not_complete", "(6x+3)(x+1) expands to 6x" + SUP2 + "+9x+3, the wrong middle, and 6x+3 = 3(2x+1) is not fully factorised. Use (3x+1)(2x+3).", "opt2 gives 9x"),
 ]),
 ("silver",5): ("ac = 3" + TIMES + "(" + MINUS + "10) = " + MINUS + "30 and the middle is +1, so one is positive and one negative: +6 and " + MINUS + "5.", [
    M(1, "sign_error", "(3x+5)(x" + MINUS + "2) expands to 3x" + SUP2 + MINUS + "x" + MINUS + "10, so the middle sign is flipped. Swap the signs: (3x" + MINUS + "5)(x+2).", "opt1 gives -x"),
 ]),
 ("silver",6): ("ac = 2" + TIMES + "5 = 10 and the middle is " + MINUS + "7, so both numbers are negative: " + MINUS + "2 and " + MINUS + "5.", [
    M(1, "bracket_swap", "Right numbers, wrong brackets. (2x" + MINUS + "1)(x" + MINUS + "5) expands to 2x" + SUP2 + MINUS + "11x+5. Put the " + MINUS + "5 with the 2x: (2x" + MINUS + "5)(x" + MINUS + "1).", "opt1 gives -11x"),
    M(3, "sign_error", "With +5 at the end both brackets are negative. (2x+5)(x" + MINUS + "1) gives " + MINUS + "5 at the end. Use (2x" + MINUS + "5)(x" + MINUS + "1).", "opt3 gives constant -5"),
 ]),
 ("gold",0): ("ac = 6" + TIMES + "(" + MINUS + "2) = " + MINUS + "12, add to +1: the numbers are +4 and " + MINUS + "3. Split the 6x" + SUP2 + " as 3x" + TIMES + "2x.", [
    M(1, "sign_error", "(3x" + MINUS + "2)(2x+1) expands to 6x" + SUP2 + MINUS + "x" + MINUS + "2, so the middle sign is flipped. Swap the signs inside: (3x+2)(2x" + MINUS + "1).", "opt1 gives -x"),
 ]),
 ("gold",1): ("ac = 8" + TIMES + "(" + MINUS + "3) = " + MINUS + "24, add to " + MINUS + "2: the numbers are +4 and " + MINUS + "6.", [
    M(1, "sign_error", "(4x+3)(2x" + MINUS + "1) expands to 8x" + SUP2 + "+2x" + MINUS + "3, so the middle sign is flipped. Swap the signs: (4x" + MINUS + "3)(2x+1).", "opt1 gives +2x"),
 ]),
 ("gold",2): ("ac = 10" + TIMES + "(" + MINUS + "3) = " + MINUS + "30, add to " + MINUS + "13: the numbers are +2 and " + MINUS + "15. Split the 10x" + SUP2 + " as 5x" + TIMES + "2x.", [
    M(2, "sign_error", "(5x" + MINUS + "1)(2x+3) expands to 10x" + SUP2 + "+13x" + MINUS + "3, so the middle sign is flipped. Swap the signs: (5x+1)(2x" + MINUS + "3).", "opt2 gives +13x"),
 ]),
 ("gold",3): ("ac = 12" + TIMES + "(" + MINUS + "2) = " + MINUS + "24, add to +5: the numbers are +8 and " + MINUS + "3.", [
    M(1, "sign_error", "(4x+1)(3x" + MINUS + "2) expands to 12x" + SUP2 + MINUS + "5x" + MINUS + "2, so the middle sign is flipped. Swap the signs: (4x" + MINUS + "1)(3x+2).", "opt1 gives -5x"),
 ]),
 ("gold",4): ("Every term shares a factor of 2. Take it out first, then factorise what is left completely.", [
    M(1, "not_complete", "(4x+2)(x" + MINUS + "3) does expand to 4x" + SUP2 + MINUS + "10x" + MINUS + "6, but 4x+2 = 2(2x+1), so it is not factorised completely. Take the 2 out: 2(2x+1)(x" + MINUS + "3).", "opt1 correct but not fully factorised"),
    M(3, "not_complete", "(2x+1)(2x" + MINUS + "6) expands correctly, but 2x" + MINUS + "6 = 2(x" + MINUS + "3) still has a common factor. Complete it: 2(2x+1)(x" + MINUS + "3).", "opt3 correct but not fully factorised"),
 ]),
}

for (t,i),(hint,miscs) in data.items():
    p = pb[t][i]
    p['hint'] = hint
    p['misconceptions'] = miscs

# ---- 5. guided.opener ----
opener = {
    "display": ("Picture two number cards lying face down.<br>"
                "Multiplied together they make <strong>6</strong>. "
                "Added together they make <strong>7</strong>.<br>"
                "What are the two numbers?"),
    "steps": [
        {"pre": "The larger number is ", "post": "", "answer": 6,
         "hint": "Which pairs multiply to 6? Try 1 and 6, or 2 and 3. Which pair adds to 7?"},
        {"pre": "And the smaller number is ", "post": "", "answer": 1,
         "hint": "1 " + TIMES + " 6 = 6 and 1 + 6 = 7. So the pair is 1 and 6."},
        {"say": "That hunt, a pair with a fixed <strong>product</strong> and a fixed <strong>sum</strong>, is the whole engine of factorising \\(ax^2 + bx + c\\). You multiply the two ends, \\(a \\times c\\), to get the product, and the middle number \\(b\\) is the sum. For \\(2x^2 + 7x + 3\\) that is product \\(2 \\times 3 = 6\\) and sum 7: your pair 1 and 6. Splitting the middle \\(7x\\) into \\(1x + 6x\\) lets the quadratic break into two brackets."}
    ]
}

# ---- 6. guided.teach (one walk per tier, fresh problems) ----
teach = {}
teach['bronze'] = {
    "display": "Factorise \\(2x^2 + 7x + 6\\)",
    "steps": [
        {"say": "First multiply the two ends together.",
         "pre": "a " + TIMES + " c = 2 " + TIMES + " 6 = ", "post": "", "answer": 12,
         "hint": "Multiply the number in front of x squared by the number on its own."},
        {"say": "Now find two numbers that multiply to 12 and add to 7.",
         "pre": "The larger number is ", "post": "", "answer": 4,
         "hint": "Pairs for 12: 1 and 12, 2 and 6, 3 and 4. Which adds to 7?"},
        {"pre": "The smaller number is ", "post": "", "answer": 3,
         "hint": "3 " + TIMES + " 4 = 12 and 3 + 4 = 7."},
        {"say": "Split the middle 7x into 4x + 3x, then group: \\(2x^2 + 4x + 3x + 6 = 2x(x+2) + 3(x+2)\\). The repeated bracket is \\((x+2)\\), so the answer is \\((2x+3)(x+2)\\). Check it by expanding.",
         "pre": "The x squared term: 2 " + TIMES + " 1 = ", "post": "", "answer": 2,
         "hint": "Multiply the two x-terms: 2x times x."},
        {"pre": "The number term: 3 " + TIMES + " 2 = ", "post": "", "answer": 6,
         "hint": "Multiply the two constants."},
        {"pre": "The middle term: 2 " + TIMES + " 2 + 3 " + TIMES + " 1 = ", "post": "", "answer": 7,
         "done": "The middle comes back as 7x, so \\((2x+3)(x+2)\\) is right.",
         "hint": "Outer plus inner: 2x times 2, plus 3 times x."}
    ]
}
teach['silver'] = {
    "display": "Factorise \\(3x^2 - 5x - 2\\)",
    "steps": [
        {"say": "Multiply the ends. The constant is negative, so keep its sign.",
         "pre": "a " + TIMES + " c = 3 " + TIMES + " (" + MINUS + "2) = ", "post": "", "answer": -6,
         "hint": "A positive times a negative is negative: 3 times " + MINUS + "2."},
        {"say": "Find two numbers that multiply to " + MINUS + "6 and add to " + MINUS + "5. A negative product means one number is positive and one is negative.",
         "pre": "The negative number is ", "post": "", "answer": -6,
         "hint": "Pairs for " + MINUS + "6: " + MINUS + "6 and +1, or " + MINUS + "1 and +6. Which adds to " + MINUS + "5?"},
        {"pre": "The positive number is ", "post": "", "answer": 1,
         "hint": "(" + MINUS + "6) " + TIMES + " 1 = " + MINUS + "6 and (" + MINUS + "6) + 1 = " + MINUS + "5."},
        {"say": "Split the middle: \\(3x^2 - 6x + x - 2 = 3x(x-2) + 1(x-2)\\), giving \\((x-2)(3x+1)\\). Check by expanding.",
         "pre": "The x squared term: 1 " + TIMES + " 3 = ", "post": "", "answer": 3,
         "hint": "Multiply the two x-terms: x times 3x."},
        {"pre": "The number term: (" + MINUS + "2) " + TIMES + " 1 = ", "post": "", "answer": -2,
         "hint": "Multiply the two constants, keeping the minus."},
        {"pre": "The middle term: 1 " + TIMES + " 1 + (" + MINUS + "2) " + TIMES + " 3 = ", "post": "", "answer": -5,
         "done": "The middle comes back as " + MINUS + "5x, so \\((x-2)(3x+1)\\) is right.",
         "hint": "Outer plus inner: x times 1, plus (" + MINUS + "2) times 3x."}
    ]
}
teach['gold'] = {
    "display": "Factorise completely \\(6x^2 - 2x - 4\\)",
    "steps": [
        {"say": "Before splitting, check every term for a common factor. 6, 2 and 4 all divide by the same number.",
         "pre": "The common factor is ", "post": "", "answer": 2,
         "hint": "What is the biggest number that goes into 6, 2 and 4?"},
        {"say": "Take it out: \\(6x^2 - 2x - 4 = 2(3x^2 - x - 2)\\). Now factorise the bracket. Multiply its ends.",
         "pre": "a " + TIMES + " c = 3 " + TIMES + " (" + MINUS + "2) = ", "post": "", "answer": -6,
         "hint": "Inside the bracket: 3 times " + MINUS + "2."},
        {"say": "Find two numbers that multiply to " + MINUS + "6 and add to " + MINUS + "1.",
         "pre": "The negative number is ", "post": "", "answer": -3,
         "hint": "Pairs for " + MINUS + "6: " + MINUS + "3 and +2, or " + MINUS + "2 and +3. Which adds to " + MINUS + "1?"},
        {"pre": "The positive number is ", "post": "", "answer": 2,
         "hint": "(" + MINUS + "3) " + TIMES + " 2 = " + MINUS + "6 and (" + MINUS + "3) + 2 = " + MINUS + "1."},
        {"say": "Split: \\(3x^2 - 3x + 2x - 2 = 3x(x-1) + 2(x-1) = (x-1)(3x+2)\\). Keep the 2 out front, so the full answer is \\(2(x-1)(3x+2)\\). Check the bracket by expanding.",
         "pre": "The middle term of the bracket: 1 " + TIMES + " 2 + (" + MINUS + "1) " + TIMES + " 3 = ", "post": "", "answer": -1,
         "done": "The bracket's middle is " + MINUS + "x, so \\(2(x-1)(3x+2)\\) is the complete factorisation.",
         "hint": "Outer plus inner: x times 2, plus (" + MINUS + "1) times 3x."}
    ]
}

pd['guided'] = {"opener": opener, "teach": teach}

# ---- 7. tier_guides ----
def step(label, content, ans=False):
    s = {"label": label, "content": content}
    if ans:
        s["isAnswer"] = True; s["is_answer"] = True
    return s

pd['tier_guides'] = {
 "bronze": {
   "title": "Bronze: the ac method with all-positive terms",
   "steps": [
     "Multiply the two ends, a " + TIMES + " c. Find two numbers that multiply to this and add to the middle number b.",
     "Split the middle term into those two numbers, then group the four terms into two pairs.",
     "Factorise each pair. The bracket that repeats is one factor; what you took out forms the other."
   ],
   "example": {
     "question": "Factorise \\(2x^2 + 5x + 2\\)",
     "steps": [
       step("Multiply the ends", "\\(ac = 2 \\times 2 = 4\\)"),
       step("Find the pair", "1 and 4 (product 4, sum 5)"),
       step("Split the middle", "\\(2x^2 + x + 4x + 2\\)"),
       step("Group", "\\(x(2x+1) + 2(2x+1)\\)"),
       step("Check", "\\((2x+1)(x+2)\\) expands to \\(2x^2 + 5x + 2\\)"),
       step("Answer", "<strong>\\((2x+1)(x+2)\\)</strong>", ans=True)
     ]
   }
 },
 "silver": {
   "title": "Silver: tracking signs in the number pair",
   "steps": [
     "The method is the same, but ac or b can be negative, so watch the signs at every step.",
     "If ac is negative, one number is positive and one is negative. If ac is positive but b is negative, both numbers are negative.",
     "Split, group, then check by expanding: the middle term must come back exactly."
   ],
   "example": {
     "question": "Factorise \\(2x^2 - 5x - 3\\)",
     "steps": [
       step("Multiply the ends", "\\(ac = 2 \\times (-3) = -6\\)"),
       step("Find the pair", "\\(-6\\) and 1 (product \\(-6\\), sum \\(-5\\))"),
       step("Split the middle", "\\(2x^2 - 6x + x - 3\\)"),
       step("Group", "\\(2x(x-3) + 1(x-3)\\)"),
       step("Check", "\\((x-3)(2x+1)\\) expands to \\(2x^2 - 5x - 3\\)"),
       step("Answer", "<strong>\\((x-3)(2x+1)\\)</strong>", ans=True)
     ]
   }
 },
 "gold": {
   "title": "Gold: common factors and factorising completely",
   "steps": [
     "First check for a number that divides every term. Take it outside a bracket before you start.",
     "Factorise what is left with the ac method, keeping the common factor at the front.",
     "Factorising completely means no bracket can be broken down further, so simplify fully."
   ],
   "example": {
     "question": "Factorise completely \\(6x^2 + 9x - 6\\)",
     "steps": [
       step("Common factor", "\\(6, 9, 6\\) share 3: \\(3(2x^2 + 3x - 2)\\)"),
       step("Multiply the ends", "\\(ac = 2 \\times (-2) = -4\\)"),
       step("Find the pair", "\\(-1\\) and 4 (product \\(-4\\), sum 3)"),
       step("Split and group", "\\(x(2x-1) + 2(2x-1)\\)"),
       step("Check", "\\(3(2x-1)(x+2)\\) expands to \\(6x^2 + 9x - 6\\)"),
       step("Answer", "<strong>\\(3(2x-1)(x+2)\\)</strong>", ans=True)
     ]
   }
 }
}

# write out
out = 'lesson_maths-ocr_algebra-L06.json'
with open(out, 'w', encoding='utf-8') as f:
    json.dump(pd, f, indent=2, ensure_ascii=False)
print("written", out)
