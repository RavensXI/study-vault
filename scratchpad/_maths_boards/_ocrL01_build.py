# -*- coding: utf-8 -*-
import json, io

pd = json.load(io.open("_ocrL01_live.json", encoding="utf-8"))
pb = pd["problem_bank"]

# ---------- 1. hints (plain text, one sentence, method move) ----------
hints = {
 "bronze": [
  "Both are x terms, so add the numbers in front: 6 and 3.",
  "Both are y terms, so subtract the numbers in front: 8 take away 3.",
  "Collect the a terms; the 2b has nothing to pair with, so it stays.",
  "Collect the x terms, then add the plain numbers.",
  "Multiply the numbers, then p times p gives p squared.",
  "Collect the x terms and the y terms in separate groups.",
  "Divide the number by 3; the t stays.",
  "They are all m terms, so work left to right: 9, take 4, add 2.",
 ],
 "silver": [
  "Keep the x squared terms apart from the x terms, then collect each group.",
  "Multiply the numbers, then add the powers for a and for b.",
  "Divide the numbers, then subtract the powers of x.",
  "Expand the bracket first, then collect the x terms.",
  "Collect x squared terms, x terms and the number separately, watching signs.",
  "Multiply all three numbers, then add the powers of a.",
  "Divide the numbers, then subtract the powers for x and for y.",
 ],
 "gold": [
  "Divide the numbers, then subtract the powers of x.",
  "Square the bracket first, then multiply by 3x.",
  "Cube the bracket on top first, then divide.",
  "Divide the numbers, then subtract each letter's powers; the b cancels.",
  "Expand both brackets, then collect the like terms.",
 ],
}

# ---------- misconceptions: one clean, em-dash-free message each, expect:null ----------
mc = {
 "bronze": [
  ("multiply",        "Add the coefficients, do not multiply: 6 + 3 = 9. Answer: 9x."),
  ("add_instead",     "Subtract the coefficients: 8 − 3 = 5. Answer: 5y."),
  ("unlike_terms",    "Only combine like terms: 4a + 3a = 7a, and the 2b stays. Answer: 7a + 2b."),
  ("wrong",           "x terms: 5x − 2x = 3x. Numbers: 3 + 7 = 10. Answer: 3x + 10."),
  ("add_not_multiply","Multiply the numbers (2 × 5 = 10) and add the powers (p × p = p²). Answer: 10p²."),
  ("unlike_terms",    "Collect x terms and y terms separately: 3x − x = 2x, 4y + 2y = 6y. Answer: 2x + 6y."),
  ("wrong",           "Divide the number only: 15 ÷ 3 = 5, and the t stays. Answer: 5t."),
  ("wrong",           "Work through the m terms: 9 − 4 + 2 = 7. Answer: 7m."),
 ],
 "silver": [
  ("unlike_terms",    "x² and x are different terms: 3x² + x² = 4x², 5x − 2x = 3x. Answer: 4x² + 3x."),
  ("add_coefficients","Multiply the numbers (4 × 3 = 12) and add the powers: a³, b³. Answer: 12a³b³."),
  ("index_error",     "Divide the numbers (8 ÷ 2 = 4) and subtract the powers (4 − 1 = 3). Answer: 4x³."),
  ("forget_expand",   "Expand first: 6x + 8, then add the 5x. Answer: 11x + 8."),
  ("sign_error",      "x² terms: 5 + 2 = 7. x terms: −3 + 1 = −2. Number: −4. Answer: 7x² − 2x − 4."),
  ("add_coefficients","Multiply, do not add, the numbers: 3 × 2 × 4 = 24, and a × a × a = a³. Answer: 24a³."),
  ("index_error",     "Divide the numbers (15 ÷ 5 = 3) and subtract the powers: x², y. Answer: 3x²y."),
 ],
 "gold": [
  ("index_error",     "Divide the numbers (12 ÷ 4 = 3) and subtract the powers (5 − 2 = 3). Answer: 3x³."),
  ("index_error",     "Square the bracket first: (2x³)² = 4x⁶, then × 3x gives 12x⁷."),
  ("index_error",     "Cube the top: (3x²)³ = 27x⁶, then divide by 9x⁴ to get 3x²."),
  ("index_error",     "Subtract each power: a², b⁰ = 1, c⁻² = 1/c². Answer: 5a²/c²."),
  ("expand_error",    "Expand both: 2x² + 6x and x² − 5x, then collect: 3x² + x."),
 ],
}

for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pb[tier]):
        p["hint"] = hints[tier][i]
        pat, msg = mc[tier][i]
        p["misconceptions"] = [{"check": "wrong", "expect": None, "message": msg, "pattern": pat}]

# ---------- tier descriptions ----------
pb["bronze_description"] = "Collect like terms, or multiply and divide single terms using the index laws."
pb["silver_description"] = "Two steps: use an index law or expand a bracket, then collect the like terms."
pb["gold_description"]   = "Tougher expressions: divide each term, apply a power of a power, or expand then collect."

# ---------- opener SVG (marble jar: 4+2 red, 3+5 blue) ----------
def circ(cx, cy, col):
    return ('<circle cx="%d" cy="%d" r="7" fill="%s" fill-opacity="0.5" '
            'stroke="currentColor" stroke-width="1"/>') % (cx, cy, col)

RED, BLUE = "#f87171", "#60a5fa"
svg = ['<svg viewBox="0 0 260 118" role="img" aria-label="A jar of marbles: a group of 4 red '
       'marbles plus a group of 2 red marbles, and a group of 3 blue marbles plus a group of 5 '
       'blue marbles" style="max-width:260px;font-family:Inter,sans-serif">']
# red row y=30: 4 red, +, 2 red
xs = [24, 42, 60, 78]
for x in xs: svg.append(circ(x, 30, RED))
svg.append('<text x="96" y="35" fill="currentColor" font-size="15" text-anchor="middle">+</text>')
for x in [114, 132]: svg.append(circ(x, 30, RED))
svg.append('<text x="78" y="52" fill="currentColor" font-size="11" text-anchor="middle">red</text>')
# blue row y=82: 3 blue, +, 5 blue
for x in [24, 42, 60]: svg.append(circ(x, 82, BLUE))
svg.append('<text x="78" y="87" fill="currentColor" font-size="15" text-anchor="middle">+</text>')
for x in [96, 114, 132, 150, 168]: svg.append(circ(x, 82, BLUE))
svg.append('<text x="96" y="104" fill="currentColor" font-size="11" text-anchor="middle">blue</text>')
svg.append('</svg>')
opener_svg = "".join(svg)

opener = {
 "label": "Before any algebra",
 "steps": [
  {"pre": "4 red + 2 red = ", "say": "A jar of marbles. Just count what you can see, no algebra yet.",
   "hint": "Count the red marbles: 4, then 2 more.", "post": " red", "answer": 6},
  {"pre": "3 blue + 5 blue = ", "say": "Now the blue ones.",
   "hint": "Count the blue marbles: 3, then 5 more.", "post": " blue", "answer": 8},
  {"say": "You would not say \"6 red + 8 blue = 14 marbles\" and stop, because red and blue are "
          "different things. You leave it as 6 red and 8 blue. Algebra is identical: call a red "
          "marble \\(x\\) and a blue marble \\(y\\), so \\(4x + 2x = 6x\\) and \\(3y + 5y = 8y\\), "
          "giving \\(6x + 8y\\). Grouping the same kind of term together is called "
          "<strong>collecting like terms</strong>, and that is the whole of simplifying."},
 ],
 "display": opener_svg,
}

# ---------- teach walks ----------
teach = {
 "bronze": {
  "label": "Together: your first one",
  "display": "Simplify \\(6a + 5b + 3a + 2b\\)",
  "steps": [
   {"pre": "a terms: 6a + 3a, so 6 + 3 = ",
    "say": "Two kinds of term: a terms and b terms. Keep them in separate groups.",
    "hint": "Add the numbers in front of a.", "post": "a", "answer": 9},
   {"pre": "b terms: 5b + 2b, so 5 + 2 = ",
    "hint": "Add the numbers in front of b.", "post": "b", "answer": 7},
   {"pre": "Check with a = 1 and b = 1. The original is 6 + 5 + 3 + 2 = ",
    "say": "So it tidies to \\(9a + 7b\\). You cannot merge a with b, they are different letters.",
    "hint": "Add all four terms.", "post": "", "answer": 16},
   {"pre": "And 9a + 7b with a = 1, b = 1 is 9 + 7 = ",
    "done": "Both give 16, so 9a + 7b is right. Collecting like terms is just tidy grouping.",
    "hint": "Add 9 and 7.", "post": "", "answer": 16},
  ],
 },
 "silver": {
  "label": "Together: the silver move",
  "display": "Simplify \\(2a^3b \\times 5ab^4\\)",
  "steps": [
   {"pre": "numbers: 2 × 5 = ",
    "say": "Multiply single terms in two moves: multiply the numbers, then handle each letter's powers.",
    "hint": "Just multiply the two numbers in front.", "post": "", "answer": 10},
   {"pre": "a: a³ × a means 3 + 1 = ",
    "say": "For the letters, when you MULTIPLY you ADD the powers.",
    "hint": "Add the powers of a: 3 and 1.", "post": " so a to that power", "answer": 4},
   {"pre": "b: b × b⁴ means 1 + 4 = ",
    "hint": "Add the powers of b: 1 and 4.", "post": " so b to that power", "answer": 5},
   {"pre": "Check with a = 1, b = 1: 10 × 1 × 1 = ",
    "say": "So the answer is \\(10a^4b^5\\).",
    "done": "Multiply the numbers, add the powers. That is the one new move.",
    "hint": "Anything to a power is still 1 when the letter is 1.", "post": "", "answer": 10},
  ],
 },
 "gold": {
  "label": "Together: the gold move",
  "display": "Simplify \\(\\frac{12x^3 + 8x^2}{4x}\\)",
  "steps": [
   {"pre": "First term 12x³ ÷ 4x. Numbers: 12 ÷ 4 = ",
    "say": "A fraction like this splits up: divide EACH top term by the bottom, 4x, separately.",
    "hint": "Divide the numbers only for now.", "post": "", "answer": 3},
   {"pre": "x³ ÷ x means 3 − 1 = ",
    "say": "For the x powers, when you DIVIDE you SUBTRACT them. So the first term is \\(3x^2\\).",
    "hint": "Subtract the powers: 3 take away 1.", "post": " so x to that power", "answer": 2},
   {"pre": "Second term 8x² ÷ 4x. Numbers: 8 ÷ 4 = ",
    "say": "Same again for the second term. The x powers give 2 − 1 = 1, so the term is \\(2x\\).",
    "hint": "Divide the numbers of the second term.", "post": "", "answer": 2},
   {"pre": "Check with x = 1: top is 12 + 8 = 20, bottom is 4, and 20 ÷ 4 = ",
    "say": "So the answer is \\(3x^2 + 2x\\).",
    "done": "And 3(1) + 2 = 5 too, so 3x² + 2x is right. Divide every top term separately.",
    "hint": "Work out 20 divided by 4.", "post": "", "answer": 5},
  ],
 },
}

# ---------- tier_guides ----------
tier_guides = {
 "bronze": {
  "title": "Bronze: collect like terms",
  "steps": [
   "Like terms have the SAME letter and the SAME power, for example \\(3x\\) and \\(5x\\). Group them together.",
   "Add or subtract the numbers in front (the coefficients). The letter part stays: \\(3x + 5x = 8x\\).",
   "Plain numbers combine with each other, and different letters never mix. To multiply or divide single terms, multiply or divide the numbers and use the index laws on the powers.",
  ],
  "example": {
   "question": "Simplify 5a + 4b − 2a + 3b",
   "steps": [
    {"label": "Group", "content": "<p>a terms: \\(5a - 2a\\). b terms: \\(4b + 3b\\).</p>"},
    {"label": "Collect", "content": "<p>\\(5a - 2a = 3a\\) and \\(4b + 3b = 7b\\).</p>"},
    {"label": "Check", "content": "<p>With \\(a=1, b=1\\): original \\(5+4-2+3 = 10\\); answer \\(3+7 = 10\\) ✓</p>"},
    {"label": "Answer", "content": "<p>\\(3a + 7b\\)</p>", "isAnswer": True, "is_answer": True},
   ],
  },
 },
 "silver": {
  "title": "Silver: one index law, then collect",
  "steps": [
   "Multiplying terms: multiply the numbers, ADD the powers, so \\(2x^3 \\times 5x^2 = 10x^5\\).",
   "Dividing terms: divide the numbers, SUBTRACT the powers, so \\(8x^4 \\div 2x = 4x^3\\).",
   "If there are brackets, expand them first, then collect the like terms.",
  ],
  "example": {
   "question": "Simplify 4x²y × 2xy³",
   "steps": [
    {"label": "Numbers", "content": "<p>Multiply the coefficients: \\(4 \\times 2 = 8\\).</p>"},
    {"label": "Powers", "content": "<p>Add the powers: \\(x^{2+1} = x^3\\), \\(y^{1+3} = y^4\\).</p>"},
    {"label": "Check", "content": "<p>With \\(x=1, y=1\\): original \\(4 \\times 2 = 8\\); answer \\(8\\) ✓</p>"},
    {"label": "Answer", "content": "<p>\\(8x^3y^4\\)</p>", "isAnswer": True, "is_answer": True},
   ],
  },
 },
 "gold": {
  "title": "Gold: divide, power of a power, or expand",
  "steps": [
   "For a fraction, divide EVERY top term by the bottom separately: \\(\\frac{6x^2+9x}{3x} = 2x + 3\\).",
   "A power of a power multiplies the indices: \\((2x^3)^2 = 4x^6\\). Deal with brackets before dividing.",
   "To simplify a bracket sum like \\(2x(x+3)\\), expand each bracket in full, then collect like terms.",
  ],
  "example": {
   "question": "Simplify (18x⁵y³) ÷ (6x²y)",
   "steps": [
    {"label": "Numbers", "content": "<p>Divide the coefficients: \\(18 \\div 6 = 3\\).</p>"},
    {"label": "Powers", "content": "<p>Subtract the powers: \\(x^{5-2} = x^3\\), \\(y^{3-1} = y^2\\).</p>"},
    {"label": "Check", "content": "<p>With \\(x=1, y=1\\): top \\(18\\), bottom \\(6\\), \\(18 \\div 6 = 3\\); answer \\(3\\) ✓</p>"},
    {"label": "Answer", "content": "<p>\\(3x^3y^2\\)</p>", "isAnswer": True, "is_answer": True},
   ],
  },
 },
}

pd["guided"] = {"opener": opener, "teach": teach}
pd["tier_guides"] = tier_guides

# ---------- slim method_card content (<=140 words) ----------
pd["method_card"]["content"] = (
 "<p><strong>Simplifying</strong> means writing an expression in its shortest form by "
 "<strong>collecting like terms</strong>. Like terms share the same letter and the same power, "
 "so \\(3x\\) and \\(5x\\) combine but \\(3x\\) and \\(3x^2\\) do not.</p>"
 "<p>Add or subtract the numbers in front of like terms; plain numbers combine with each other. "
 "To <strong>multiply</strong> terms, multiply the numbers and add the powers. To "
 "<strong>divide</strong>, divide the numbers and subtract the powers, and remember "
 "\\((x^a)^b = x^{ab}\\).</p>"
)

# ---------- style repair: em dashes in preserved worked_examples labels ----------
for w in pd.get("worked_examples", []):
    for s in w.get("steps", []):
        if isinstance(s.get("label"), str) and "—" in s["label"]:
            s["label"] = s["label"].replace(" — ", ": ").replace("—", ":")

json.dump(pd, io.open("lesson_maths-ocr_algebra-L01.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("written. method_card content words:",
      len(pd["method_card"]["content"].replace("\\(", " ").replace("\\)", " ").split()))
