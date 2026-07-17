# -*- coding: utf-8 -*-
import json, io

pd = json.load(io.open("_L04rp_live.json", encoding="utf-8"))

# ---- METHOD CARD: trim steps to 4 (validator max 4) ----
pd["method_card"]["steps"] = [
    "Direct: \\(y = kx\\). Find k = y ÷ x, then use it.",
    "Inverse: \\(y = k/x\\). Find k = x × y, then use it.",
    "Direct: as x increases, y increases at the same rate.",
    "Inverse: as x increases, y decreases (product stays fixed).",
]

pb = pd["problem_bank"]

# ---- tier descriptions ----
pb["bronze_description"] = "Everyday and simple algebraic proportion: find the constant or the value of one unit, then scale."
pb["silver_description"] = "Algebraic proportion (y = kx or y = k/x): find k, then use it forwards or backwards, including word problems."
pb["gold_description"] = "Reverse and multi-step proportion: scale factors, work rates, gears, and finding x from y."

def setp(prob, hint, expect, message, steps):
    prob["hint"] = hint
    mc = prob.get("misconceptions") or [{}]
    mc[0]["expect"] = expect
    mc[0]["message"] = message
    if "check" not in mc[0]:
        mc[0]["check"] = "common"
    if "pattern" not in mc[0]:
        mc[0]["pattern"] = "wrong_formula"
    prob["misconceptions"] = mc
    if steps is not None:
        prob["guided_steps"] = steps

def box(pre, answer, hint, post="", say=None, phase=None, done=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if phase is not None: d["phase"] = phase
    if done is not None: d["done"] = done
    return d

def sayonly(s):
    return {"say": s}

B = pb["bronze"]; S = pb["silver"]; G = pb["gold"]

# ===================== BRONZE =====================
# B0: y∝x x=2 y=8 -> y at x=5 = 20
setp(B[0], "Divide y by x to get k, then multiply k by the new x.", 40,
     "Find k first: k = 8 ÷ 2 = 4. Then y = 4 × 5 = 20. Multiplying 8 × 5 skips finding k.",
     [ sayonly("Direct means \\(y = kx\\). Find the constant \\(k\\) from the pair."),
       box("k = 8 ÷ 2 = ", 4, "Divide y by the matching x."),
       box("y = 4 × 5 = ", 20, "Multiply k by the new x.", say="Now use \\(y = kx\\) at the new x.", phase="substitute"),
       box("Check: 4 × 2 = ", 8, "k times the first x should give the first y.", say="Check with the first pair.", phase="substitute", done="That returns the given y = 8, so 20 is right.") ])

# B1: y∝x x=3 y=15 -> find k = 5
setp(B[1], "The constant k is y divided by x.", 45,
     "For direct, k = y ÷ x = 15 ÷ 3 = 5. Multiplying gives 45, which is wrong.",
     [ sayonly("Direct means \\(y = kx\\), so the constant is \\(k = y \\div x\\)."),
       box("k = 15 ÷ 3 = ", 5, "Divide y by the matching x."),
       box("Check: 5 × 3 = ", 15, "k times x should give y back.", say="Verify the constant rebuilds the pair.", phase="substitute"),
       box("And at x = 1: 5 × 1 = ", 5, "At x = 1, y equals k.", phase="substitute", done="y ÷ x is 5 every time, so k = 5.") ])

# B2: 4 workers 6h -> 12 workers = 2 (inverse)
setp(B[2], "Multiply workers by hours to get the fixed total, then divide by the new number of workers.", 18,
     "Inverse: more workers, less time. Total = 4 × 6 = 24. Time = 24 ÷ 12 = 2 hours.",
     [ sayonly("Inverse proportion: more workers, LESS time. The total (worker-hours) stays fixed."),
       box("Total = 4 × 6 = ", 24, "Multiply workers by hours."),
       box("12 workers: 24 ÷ 12 = ", 2, "Divide the total by 12.", say="Share the total among 12 workers.", phase="substitute"),
       box("Check: 12 × 2 = ", 24, "Workers times time should return the total.", phase="substitute", done="Same total 24, so 2 hours is right.") ])

# B3: y=kx k=7 x=4 -> 28
setp(B[3], "Substitute k and x straight into y = kx.", 11,
     "y = kx means multiply: 7 × 4 = 28. Adding gives 11, which is wrong.",
     [ sayonly("Here \\(k\\) is already given. Just substitute into \\(y = kx\\)."),
       box("y = 7 × 4 = ", 28, "Multiply k by x."),
       box("Check: 28 ÷ 4 = ", 7, "Dividing y by x should return k.", say="Verify k.", phase="substitute"),
       box("And 28 ÷ 7 = ", 4, "Dividing y by k should return x.", phase="substitute", done="Both checks agree, so y = 28.") ])

# B4: y∝x x=10 y=40 -> y at x=3 = 12
setp(B[4], "Divide y by x to get k, then multiply k by the new x.", 120,
     "Find k = 40 ÷ 10 = 4 first. Then y = 4 × 3 = 12. Multiplying 40 × 3 skips k.",
     [ sayonly("Direct means \\(y = kx\\). Find k from the pair first."),
       box("k = 40 ÷ 10 = ", 4, "Divide y by x."),
       box("y = 4 × 3 = ", 12, "Multiply k by the new x.", say="Use \\(y = kx\\) at x = 3.", phase="substitute"),
       box("Check: 4 × 10 = ", 40, "k times the first x gives the first y.", phase="substitute", done="Returns 40, so 12 is right.") ])

# B5: MC graph -> index 0 (multiple_choice, guided_steps optional)
B[5]["hint"] = "Direct proportion gives a straight line that passes through the origin."
B[5]["misconceptions"] = [{
    "check": "common",
    "expect": 1,
    "message": "Direct proportion (y = kx) is a straight line through the origin. A curve through the origin is not direct proportion.",
    "pattern": "confused_type",
}]

# B6 EDIT: was y∝1/x x=4 y=3 -> k=12 (DUP with B4=12). New: x=4 y=6 -> k=24
B[6]["display"] = "\\(y \\propto \\frac{1}{x}\\). When \\(x = 4\\), \\(y = 6\\). Find \\(k\\)."
B[6]["solutions"] = [24]
setp(B[6], "For inverse proportion, k is x multiplied by y.", 1.5,
     "For inverse, k = x × y = 4 × 6 = 24. Dividing gives 1.5, which uses the direct rule by mistake.",
     [ sayonly("Inverse means \\(y = \\frac{k}{x}\\), so the constant is the product \\(k = x \\times y\\)."),
       box("k = 4 × 6 = ", 24, "Multiply x by y."),
       box("Check: 24 ÷ 4 = ", 6, "k divided by x should return y.", say="Verify with the pair.", phase="substitute"),
       box("And 24 ÷ 6 = ", 4, "k divided by y should return x.", phase="substitute", done="Both return the pair, so k = 24.") ])
B[6]["pattern"] = "wrong_k"

# B7: y∝x x=5 y=30 -> y at x=8 = 48
setp(B[7], "Divide y by x to get k, then multiply by the new x.", 240,
     "Find k = 30 ÷ 5 = 6 first. Then y = 6 × 8 = 48.",
     [ sayonly("Direct means \\(y = kx\\). Find k first."),
       box("k = 30 ÷ 5 = ", 6, "Divide y by x."),
       box("y = 6 × 8 = ", 48, "Multiply k by the new x.", say="Use the rule at x = 8.", phase="substitute"),
       box("Check: 6 × 5 = ", 30, "k times the first x gives the first y.", phase="substitute", done="Returns 30, so 48 is right.") ])

# ===================== SILVER =====================
# S0: y∝1/x x=5 y=8 -> y at x=10 = 4
setp(S[0], "Multiply x by y to get k, then divide k by the new x.", 16,
     "Inverse: k = 5 × 8 = 40. y = 40 ÷ 10 = 4. Treating it as direct gives 16.",
     [ sayonly("Inverse means \\(y = \\frac{k}{x}\\), so k is the product."),
       box("k = 5 × 8 = ", 40, "Multiply the pair together."),
       box("y = 40 ÷ 10 = ", 4, "Divide k by the new x.", say="Use \\(y = \\frac{k}{x}\\) at x = 10.", phase="substitute"),
       box("Check: 10 × 4 = ", 40, "x times y should return k.", phase="substitute", done="Same product 40, so 4 is right.") ])

# S1 EDIT: was 3 taps 8h -> 4 (DUP). New: 4 taps 9h -> 6 taps = 6
S[1]["display"] = "4 taps fill a tank in 9 hours. How long for 6 taps?"
S[1]["solutions"] = [6]
setp(S[1], "Multiply taps by hours to get the fixed total, then divide by the new number of taps.", 13.5,
     "Inverse: more taps, less time. Total = 4 × 9 = 36. Time = 36 ÷ 6 = 6 hours.",
     [ sayonly("Inverse: more taps, LESS time. The total (tap-hours) stays fixed."),
       box("Total = 4 × 9 = ", 36, "Multiply taps by hours."),
       box("6 taps: 36 ÷ 6 = ", 6, "Divide the total by 6.", say="Share the total among 6 taps.", phase="substitute"),
       box("Check: 6 × 6 = ", 36, "Taps times time should return the total.", phase="substitute", done="Same total 36, so 6 hours is right.") ])
S[1]["pattern"] = "inverse_error"

# S2: y∝x x=4 y=20 -> x at y=35 = 7
setp(S[2], "Find k, then divide the new y by k to get x.", 175,
     "k = 20 ÷ 4 = 5. x = 35 ÷ 5 = 7. Multiplying by k instead of dividing gives 175.",
     [ sayonly("Direct means \\(y = kx\\). Find the constant k first."),
       box("k = 20 ÷ 4 = ", 5, "Divide y by the matching x."),
       box("x = 35 ÷ 5 = ", 7, "Divide the new y by k.", say="We know y = 35 and want x, so \\(x = y \\div k\\).", phase="substitute"),
       box("Check: 5 × 7 = ", 35, "k times x should give the new y.", phase="substitute", done="Gives 35, so x = 7 is right.") ])

# S3: C∝w 5kg £12 -> 8kg = 19.2 (calculator)
setp(S[3], "Find the cost per kg, then multiply by the new weight.", 2.4,
     "Cost per kg = 12 ÷ 5 = £2.40. For 8 kg, C = 2.40 × 8 = £19.20.",
     [ sayonly("Direct proportion: the cost per kg is fixed. Find it first."),
       box("Per kg: 12 ÷ 5 = £", 2.4, "Divide the cost by the weight."),
       box("8 kg: 2.4 × 8 = £", 19.2, "Multiply the per-kg cost by 8.", say="Scale up to 8 kg.", phase="substitute"),
       box("Check: 19.2 ÷ 8 = £", 2.4, "Dividing back should give the per-kg cost.", phase="substitute", done="Back to £2.40 per kg, so £19.20 is right.") ])

# S4 EDIT: was y∝1/x x=3 y=12 -> 4 (DUP). New: x=2 y=9 -> y at x=6 = 3
S[4]["display"] = "\\(y \\propto \\frac{1}{x}\\). When \\(x = 2\\), \\(y = 9\\). Find \\(y\\) when \\(x = 6\\)."
S[4]["solutions"] = [3]
setp(S[4], "Multiply x by y to get k, then divide by the new x.", 27,
     "Inverse: k = 2 × 9 = 18. y = 18 ÷ 6 = 3. Treating it as direct gives 27.",
     [ sayonly("Inverse means \\(y = \\frac{k}{x}\\), so k is the product."),
       box("k = 2 × 9 = ", 18, "Multiply the pair together."),
       box("y = 18 ÷ 6 = ", 3, "Divide k by the new x.", say="Use \\(y = \\frac{k}{x}\\) at x = 6.", phase="substitute"),
       box("Check: 6 × 3 = ", 18, "x times y should return k.", phase="substitute", done="Same product 18, so 3 is right.") ])
S[4]["pattern"] = "inverse_error"

# S5: classify direct/inverse, enter 1 for inverse -> 1
setp(S[5], "Multiply painters by days for each pair. Equal products mean inverse.", None,
     "Multiply painters by days: 2 × 6 = 12 and 3 × 4 = 12. The product is fixed, so it is inverse. Enter 1.",
     [ sayonly("Inverse means painters times days gives the same total each time. Check both pairs."),
       box("First pair: 2 × 6 = ", 12, "Multiply painters by days."),
       box("Second pair: 3 × 4 = ", 12, "Multiply painters by days again.", say="Now the second pair.", phase="substitute"),
       box("Both give 12, so it is inverse. Enter ", 1, "Enter 1 for inverse.", phase="substitute", done="Equal products mean inverse proportion.") ])
S[5]["pattern"] = "confused_type"

# S6: y∝1/x x=2 y=15 -> x at y=6 = 5
setp(S[6], "Multiply x by y to get k, then divide k by the new y.", 0.2,
     "k = 2 × 15 = 30. x = 30 ÷ 6 = 5. Dividing 6 ÷ 30 by mistake gives 0.2.",
     [ sayonly("Inverse means \\(y = \\frac{k}{x}\\), so k is the product."),
       box("k = 2 × 15 = ", 30, "Multiply the pair together."),
       box("x = 30 ÷ 6 = ", 5, "Divide k by the new y.", say="We know y = 6, and \\(x = k \\div y\\).", phase="substitute"),
       box("Check: 5 × 6 = ", 30, "x times y should return k.", phase="substitute", done="Same product 30, so x = 5 is right.") ])

# ===================== GOLD =====================
# G0: y∝x, x triples, y 12 -> 36
setp(G[0], "If x is multiplied by 3, y is multiplied by 3 as well.", 4,
     "Direct: x triples, so y triples. 12 × 3 = 36. Dividing (as if inverse) gives 4.",
     [ sayonly("Direct proportion keeps y ÷ x fixed. If x triples, y triples by the same factor."),
       box("The factor: x triples, so multiply y by ", 3, "Triples means times 3."),
       box("New y = 12 × 3 = ", 36, "Multiply the old y by 3.", say="Apply the factor to y.", phase="substitute"),
       box("Check the ratio: 36 ÷ 12 = ", 3, "The ratio should equal the factor, 3.", phase="substitute", done="y grew by the same factor as x, so 36 is right.") ])
G[0]["pattern"] = "wrong_formula"

# G1: y∝1/x, x doubles, y was 20 -> 10
setp(G[1], "If x is doubled, y is halved.", 40,
     "Inverse: x doubles, so y halves. 20 ÷ 2 = 10. Doubling gives 40, the wrong direction.",
     [ sayonly("Inverse proportion: if x doubles, y halves, because the product x × y stays fixed."),
       box("Doubling x means dividing y by ", 2, "Double one, halve the other."),
       box("New y = 20 ÷ 2 = ", 10, "Halve the old y.", say="Apply it to y.", phase="substitute"),
       box("Product check: 10 × 2 = ", 20, "The new product should match the starting value.", phase="substitute", done="Product is unchanged, so 10 is right.") ])
G[1]["pattern"] = "wrong_formula"

# G2: y∝x (3,12) (a,28) -> a = 7
setp(G[2], "Find k from the first point, then divide 28 by k.", 112,
     "k = 12 ÷ 3 = 4. a = 28 ÷ 4 = 7. Multiplying by k instead gives 112.",
     [ sayonly("Both points fit \\(y = kx\\). Find k from the first point (3, 12)."),
       box("k = 12 ÷ 3 = ", 4, "Divide y by x for the first point."),
       box("a = 28 ÷ 4 = ", 7, "Divide the second y by k.", say="The second point (a, 28) fits \\(a = y \\div k\\).", phase="substitute"),
       box("Check: 4 × 7 = ", 28, "k times a should give 28.", phase="substitute", done="Gives 28, so a = 7 is right.") ])
G[2]["pattern"] = "wrong_k"

# G3: 5 machines 200/h -> 560/h = 14 machines
setp(G[3], "Find how many items one machine makes, then divide 560 by that.", 40,
     "One machine = 200 ÷ 5 = 40 items/h. Machines = 560 ÷ 40 = 14.",
     [ sayonly("Direct proportion: more machines, more items. Find the rate for ONE machine."),
       box("One machine: 200 ÷ 5 = ", 40, "Divide the output by the number of machines.", post=" items/h"),
       box("Machines needed: 560 ÷ 40 = ", 14, "Divide the target output by the one-machine rate.", say="How many of those rates make 560?", phase="substitute"),
       box("Check: 14 × 40 = ", 560, "Machines times rate should give the target.", phase="substitute", done="Returns 560 items/h, so 14 machines is right.") ])
G[3]["pattern"] = "wrong_formula"

# G4: y∝1/x x=4 y=9 -> y at x=12 = 3
setp(G[4], "Multiply x by y to get k, then divide k by the new x.", 27,
     "Inverse: k = 4 × 9 = 36. y = 36 ÷ 12 = 3. Treating it as direct gives 27.",
     [ sayonly("Inverse means \\(y = \\frac{k}{x}\\), so k is the product."),
       box("k = 4 × 9 = ", 36, "Multiply the pair together."),
       box("y = 36 ÷ 12 = ", 3, "Divide k by the new x.", say="Use \\(y = \\frac{k}{x}\\) at x = 12.", phase="substitute"),
       box("Check: 12 × 3 = ", 36, "x times y should return k.", phase="substitute", done="Same product 36, so 3 is right.") ])

# ===================== TIER GUIDES =====================
pd["tier_guides"] = {
 "bronze": {
  "title": "Bronze: find the constant, or find one unit",
  "steps": [
   "Decide the type. If more means more, it is <strong>direct</strong>. If more means less (more workers, less time), it is <strong>inverse</strong>.",
   "Direct: the constant is \\(k = y \\div x\\), or find the value of ONE unit by dividing. Inverse: the constant is \\(k = x \\times y\\).",
   "Put the constant back to find the missing value, then check it fits the numbers you started with."
  ],
  "example": {
   "question": "y is directly proportional to x. When x = 4, y = 24. Find y when x = 9.",
   "steps": [
    {"label": "Type", "content": "<p>More x, more y: direct proportion.</p>"},
    {"label": "Find k", "content": "<p>\\(k = 24 \\div 4 = 6\\).</p>"},
    {"label": "Use it", "content": "<p>\\(y = 6 \\times 9 = 54\\).</p>"},
    {"label": "Check", "content": "<p>\\(54 \\div 9 = 6 = k\\) ✓</p>"},
    {"label": "Answer", "content": "<p><strong>54</strong></p>", "isAnswer": True, "is_answer": True}
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
   "question": "y is inversely proportional to x. When x = 3, y = 10. Find y when x = 6.",
   "steps": [
    {"label": "Rule", "content": "<p>Inverse, so \\(y = \\frac{k}{x}\\).</p>"},
    {"label": "Find k", "content": "<p>\\(k = 3 \\times 10 = 30\\).</p>"},
    {"label": "Use it", "content": "<p>\\(y = 30 \\div 6 = 5\\).</p>"},
    {"label": "Check", "content": "<p>\\(6 \\times 5 = 30 = k\\) ✓</p>"},
    {"label": "Answer", "content": "<p><strong>5</strong></p>", "isAnswer": True, "is_answer": True}
   ]
  }
 },
 "gold": {
  "title": "Gold: reverse and multi-step proportion",
  "steps": [
   "Same rules, harder set-ups: gears and work rates are <strong>inverse</strong>, so the product stays fixed.",
   "Given \\(y\\) and asked for \\(x\\)? Rearrange \\(y = kx\\) to \\(x = y \\div k\\), or \\(y = \\frac{k}{x}\\) to \\(x = k \\div y\\).",
   "For scale-factor questions, use the same factor: triple x means triple y (direct), double x means halve y (inverse)."
  ],
  "example": {
   "question": "y is directly proportional to x. When x triples, y goes from 12 to what?",
   "steps": [
    {"label": "Type", "content": "<p>Direct: x and y change by the same factor.</p>"},
    {"label": "Factor", "content": "<p>x triples, so multiply y by 3.</p>"},
    {"label": "Use it", "content": "<p>\\(12 \\times 3 = 36\\).</p>"},
    {"label": "Check", "content": "<p>\\(36 \\div 12 = 3\\) ✓</p>"},
    {"label": "Answer", "content": "<p><strong>36</strong></p>", "isAnswer": True, "is_answer": True}
   ]
  }
 }
}

# ===================== GUIDED (opener + teach) =====================
pd["guided"] = {
 "opener": {
  "label": "Before any algebra",
  "display": "6 cupcakes cost £9<br>2 cleaners take 6 hours to clean an office",
  "steps": [
   {"say": "Two everyday puzzles. No algebra, just common sense. Start with the cupcakes.",
    "pre": "12 cupcakes would cost £", "post": "", "answer": 18,
    "hint": "Twice as many cupcakes means twice the cost."},
   {"say": "Now the cleaners. Same office, but send 4 cleaners instead of 2.",
    "pre": "With 4 cleaners it takes ", "post": " hours", "answer": 3,
    "hint": "Twice as many cleaners means half the time."},
   {"say": "Two everyday moves. Cupcakes: <strong>more means more</strong>, that is <strong>direct proportion</strong>. Cleaners: <strong>more means less</strong>, that is <strong>inverse proportion</strong>. The trick for both is to find ONE first (one cupcake is £1.50; the whole clean is 2 × 6 = 12 cleaner-hours), then scale. Algebra just writes direct as \\(y = kx\\) and inverse as \\(y = \\frac{k}{x}\\)."}
  ]
 },
 "teach": {
  "bronze": {
   "display": "8 identical mugs weigh 2000 g. How much do 5 mugs weigh?",
   "label": "Together: your first one",
   "steps": [
    {"say": "Direct proportion: more mugs, more weight. The safest route is to find ONE mug first.",
     "pre": "One mug: 2000 ÷ 8 = ", "post": " g", "answer": 250,
     "hint": "Divide the total weight by the number of mugs."},
    {"say": "Now scale up. Five mugs is five lots of that.",
     "pre": "5 mugs: 250 × 5 = ", "post": " g", "answer": 1250,
     "hint": "Multiply the one-mug weight by 5."},
    {"say": "The one-mug value works backwards too. How many mugs weigh 1000 g?",
     "pre": "1000 ÷ 250 = ", "post": " mugs", "answer": 4,
     "hint": "Divide the weight by the one-mug weight.",
     "done": "Find one, then multiply or divide. That is the whole bronze method."},
    {"say": "Check against the start.",
     "pre": "8 mugs: 250 × 8 = ", "post": " g", "answer": 2000,
     "hint": "Eight mugs should return the starting weight.",
     "done": "Back to the given 2000 g, so 250 g per mug is right."}
   ]
  },
  "silver": {
   "display": "\\(y\\) is directly proportional to \\(x\\). When \\(x = 6\\), \\(y = 21\\). Find \\(y\\) when \\(x = 10\\).",
   "label": "Together: the silver move",
   "steps": [
    {"say": "Now it is written in algebra. Direct means \\(y = kx\\). First find the constant \\(k\\).",
     "pre": "k = 21 ÷ 6 = ", "post": "", "answer": 3.5,
     "hint": "Divide the y value by the matching x value."},
    {"say": "So the rule is \\(y = 3.5x\\). Use it at the new x.",
     "pre": "y = 3.5 × 10 = ", "post": "", "answer": 35,
     "hint": "Multiply k by the new x."},
    {"say": "It runs backwards too. If y were 49, what is x?",
     "pre": "x = 49 ÷ 3.5 = ", "post": "", "answer": 14,
     "hint": "Divide y by k to get x.",
     "done": "Find k once, then multiply or divide. That is the silver move."},
    {"say": "Check with the first pair.",
     "pre": "3.5 × 6 = ", "post": "", "answer": 21,
     "hint": "k times the original x should give the original y.",
     "done": "That returns the given y = 21, so k = 3.5 is right."}
   ]
  },
  "gold": {
   "display": "\\(y\\) is inversely proportional to \\(x\\). When \\(x = 4\\), \\(y = 15\\). Find \\(x\\) when \\(y = 10\\).",
   "label": "Together: the gold move",
   "steps": [
    {"say": "Inverse means \\(y = \\frac{k}{x}\\), so the constant is the PRODUCT: \\(k = x \\times y\\).",
     "pre": "k = 4 × 15 = ", "post": "", "answer": 60,
     "hint": "Multiply the pair together for inverse."},
    {"say": "The rule is \\(y = \\frac{60}{x}\\). This time we know y = 10 and want x. Rearrange: \\(x = \\frac{k}{y}\\).",
     "pre": "x = 60 ÷ 10 = ", "post": "", "answer": 6,
     "hint": "Divide the constant by y."},
    {"say": "Sense check: y dropped from 15 to 10, so x should rise. It did, from 4 to 6. Confirm the product.",
     "pre": "6 × 10 = ", "post": "", "answer": 60,
     "hint": "x times y should return the constant.",
     "done": "Same 60, so x = 6 fits."},
    {"say": "One more, to prove the product never changes. What is x when y = 5?",
     "pre": "x = 60 ÷ 5 = ", "post": "", "answer": 12,
     "hint": "Divide the constant by the new y.",
     "done": "12 × 5 = 60 again. The product stays fixed: that is the gold idea."}
   ]
  }
 }
}

# ---- fix em dashes in preserved worked_examples labels (student-facing) ----
for we in pd.get("worked_examples", []):
    for st in we.get("steps", []):
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

with io.open("lesson_maths-ocr_ratio-proportion-L04.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)
print("written; bronze/silver/gold sizes:", len(B), len(S), len(G))
print("bronze sols:", [p["solutions"] for p in B])
print("silver sols:", [p["solutions"] for p in S])
print("gold sols:", [p["solutions"] for p in G])
