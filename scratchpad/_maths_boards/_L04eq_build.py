# -*- coding: utf-8 -*-
"""Build full guided-learning + diagrams practice_data for maths-eduqas algebra-L04
Formulae & Substitution. Preserves topic_links/related_videos/worked_examples."""
import json, io

MINUS = "−"  # unicode minus
live = json.load(io.open("_L04eq_live.json", encoding="utf-8"))

# ---- SVG figures (theme-safe, currentColor, soft fills) ----
SVG_RECT = (
    '<svg viewBox="0 0 240 130" role="img" '
    'aria-label="A rectangle with length 7 and width 3">'
    '<rect x="40" y="30" width="150" height="70" fill="#60a5fa" fill-opacity="0.3" '
    'stroke="currentColor" stroke-width="1.5"/>'
    '<text x="115" y="120" fill="currentColor" font-family="Inter,sans-serif" '
    'font-size="12" text-anchor="middle">7</text>'
    '<text x="26" y="69" fill="currentColor" font-family="Inter,sans-serif" '
    'font-size="12" text-anchor="middle">3</text>'
    '</svg>'
    '<span class="figure-caption">Diagram not drawn accurately</span><br>'
)
# Parallelogram: base 6 along bottom, perpendicular height 9 (dashed), right-angle mark.
SVG_PARA = (
    '<svg viewBox="0 0 240 150" role="img" '
    'aria-label="A parallelogram with base 6 and perpendicular height 9">'
    '<polygon points="45,120 155,120 195,45 85,45" fill="#34d399" fill-opacity="0.3" '
    'stroke="currentColor" stroke-width="1.5"/>'
    '<line x1="85" y1="120" x2="85" y2="45" stroke="currentColor" stroke-width="1.2" '
    'stroke-dasharray="4 3"/>'
    '<rect x="85" y="108" width="12" height="12" fill="none" stroke="currentColor" '
    'stroke-width="1"/>'
    '<text x="100" y="137" fill="currentColor" font-family="Inter,sans-serif" '
    'font-size="12" text-anchor="middle">6</text>'
    '<text x="74" y="86" fill="currentColor" font-family="Inter,sans-serif" '
    'font-size="12" text-anchor="middle">9</text>'
    '</svg>'
    '<span class="figure-caption">Diagram not drawn accurately</span><br>'
)

pb = live["problem_bank"]

# ---------- tier descriptions ----------
pb["bronze_description"] = "Put the given numbers straight into the formula and work it out."
pb["silver_description"] = "Substitute into trickier formulae, or rearrange a simple formula to change its subject."
pb["gold_description"] = "Change the subject when it takes several moves: squares, roots, brackets, or the letter appearing twice."

# ================= BRONZE =================
B = pb["bronze"]

B[0]["hint"] = "Replace x with 4, then work out 3 times 4 before adding 2."
B[0]["misconceptions"] = [{
    "pattern": "dropped_constant", "expect": 12,
    "message": "3 × 4 is 12, but the formula adds 2 more: 12 + 2 = 14. Do not drop the + 2.",
    "note": "student stops at 3x"}]
B[0]["guided_steps"] = [
    {"say": "Substitute x = 4 into \\(y = 3x + 2\\). Replace the x, so y = 3 × 4 + 2.",
     "pre": "First work out 3 × 4 = ", "post": "", "answer": 12, "hint": "Just 3 times 4."},
    {"phase": "substitute", "say": "Now finish the arithmetic.",
     "pre": "12 + 2 = ", "post": "", "answer": 14, "hint": "Add the 2 that was waiting."},
    {"phase": "substitute", "pre": "Check by reversing: (14 " + MINUS + " 2) ÷ 3 = ", "post": "",
     "answer": 4, "done": "That is the x we started with, so y = 14 is right.",
     "hint": "Subtract 2, then divide by 3."}]

B[1]["display"] = SVG_RECT + B[1]["display"]
B[1]["hint"] = "Double the length and double the width, then add the two results."
B[1]["misconceptions"] = [{
    "pattern": "forgot_to_double", "expect": 10,
    "message": "The 2s matter: P = 2 × 7 + 2 × 3 = 14 + 6 = 20. Just adding 7 + 3 gives 10, which is only halfway round.",
    "note": "l + w without doubling"}]
B[1]["guided_steps"] = [
    {"say": "Substitute l = 7 and w = 3 into \\(P = 2l + 2w\\).",
     "pre": "Two lots of the length: 2 × 7 = ", "post": "", "answer": 14, "hint": "Double the 7."},
    {"phase": "substitute", "say": "Now the width part and the total.",
     "pre": "Two lots of the width: 2 × 3 = ", "post": "", "answer": 6, "hint": "Double the 3."},
    {"phase": "substitute", "pre": "Add them: 14 + 6 = ", "post": "", "answer": 20,
     "done": "P = 20. That is 2 × (7 + 3) = 2 × 10, which agrees.", "hint": "Add your two results."}]

B[2]["hint"] = "Square the 3 first (3 times 3), then add 1."
B[2]["misconceptions"] = [{
    "pattern": "squared_as_times_two", "expect": 7,
    "message": "\\(x^2\\) means x × x = 3 × 3 = 9, not 3 × 2. Then 9 + 1 = 10. Treating it as 3 × 2 gives 7.",
    "note": "x^2 read as 2x"}]
B[2]["guided_steps"] = [
    {"say": "Substitute x = 3 into \\(y = x^2 + 1\\). The \\(x^2\\) means x × x.",
     "pre": "Square it: 3 × 3 = ", "post": "", "answer": 9, "hint": "3 times 3, not 3 times 2."},
    {"phase": "substitute", "pre": "Add 1: 9 + 1 = ", "post": "", "answer": 10, "hint": "Add the 1."},
    {"phase": "substitute", "pre": "Check: your answer minus 1 should be 3 squared. 10 " + MINUS + " 1 = ",
     "post": "", "answer": 9, "done": "9 is 3², so y = 10 is right.", "hint": "Subtract 1."}]

B[3]["hint"] = "5 times negative 2 is negative 10, then subtract 3."
B[3]["misconceptions"] = [{
    "pattern": "lost_negative", "expect": 7,
    "message": "5 × (" + MINUS + "2) = " + MINUS + "10, a negative. Then " + MINUS + "10 " + MINUS + " 3 = " + MINUS + "13. Treating it as +10 gives 7.",
    "note": "sign dropped on 5x"}]
B[3]["guided_steps"] = [
    {"say": "Substitute x = " + MINUS + "2 into \\(y = 5x " + MINUS + " 3\\). Keep the negative in brackets: y = 5 × (" + MINUS + "2) " + MINUS + " 3.",
     "pre": "Work out 5 × (" + MINUS + "2) = ", "post": "", "answer": -10, "hint": "A positive times a negative is negative."},
    {"phase": "substitute", "pre": MINUS + "10 " + MINUS + " 3 = ", "post": "", "answer": -13, "hint": "Going more negative."},
    {"phase": "substitute", "pre": "Check by reversing: (" + MINUS + "13 + 3) ÷ 5 = ", "post": "", "answer": -2,
     "done": "That is the x we started with, so y = " + MINUS + "13 is right.", "hint": "Add 3, then divide by 5."}]

B[4]["display"] = SVG_PARA + B[4]["display"]
B[4]["hint"] = "bh means b times h, so multiply 6 by 9."
B[4]["misconceptions"] = [{
    "pattern": "added_not_multiplied", "expect": 15,
    "message": "bh means b × h = 6 × 9 = 54. Adding, 6 + 9, gives 15, which is the wrong operation.",
    "note": "b+h"}]
B[4]["guided_steps"] = [
    {"say": "Substitute b = 6 and h = 9 into \\(A = bh\\). To multiply 6 × 9 without a calculator, split the 9.",
     "pre": "First 6 × 10 = ", "post": "", "answer": 60, "hint": "Six times ten."},
    {"phase": "substitute", "pre": "Then 6 × 1 = ", "post": "", "answer": 6, "hint": "Six ones."},
    {"phase": "substitute", "pre": "6 × 9 = 60 " + MINUS + " 6 = ", "post": "", "answer": 54,
     "done": "A = 54.", "hint": "Subtract to finish."}]

B[5]["hint"] = "Square the 5 first to get 25, then double it."
B[5]["misconceptions"] = [{
    "pattern": "doubled_before_squaring", "expect": 100,
    "message": "Square first, then double: 5² = 25, then 2 × 25 = 50. Doubling first, (2 × 5)² = 100, breaks the order.",
    "note": "(2x)^2"}]
B[5]["guided_steps"] = [
    {"say": "Substitute x = 5 into \\(y = 2x^2\\). Square first (BIDMAS), then double.",
     "pre": "Square it: 5 × 5 = ", "post": "", "answer": 25, "hint": "Five fives."},
    {"phase": "substitute", "pre": "Now double: 2 × 25 = ", "post": "", "answer": 50, "hint": "Two lots of 25."},
    {"phase": "substitute", "pre": "Check: halve your answer to get back x². 50 ÷ 2 = ", "post": "",
     "answer": 25, "done": "25 is 5², so y = 50 is right.", "hint": "Divide by 2."}]

B[6]["hint"] = "Work out a times t first, then add u."
B[6]["misconceptions"] = [{
    "pattern": "added_before_multiplying", "expect": 36,
    "message": "Do a × t first (2 × 3 = 6), then add u: 10 + 6 = 16. Adding u and a first, (10 + 2) × 3, gives 36.",
    "note": "(u+a)t"}]
B[6]["guided_steps"] = [
    {"say": "Substitute u = 10, a = 2, t = 3 into \\(v = u + at\\). Do a × t before adding u.",
     "pre": "Work out a × t: 2 × 3 = ", "post": "", "answer": 6, "hint": "Multiply a and t first."},
    {"phase": "substitute", "pre": "Add u: 10 + 6 = ", "post": "", "answer": 16, "hint": "Add the 10."},
    {"phase": "substitute", "pre": "Check by reversing: (16 " + MINUS + " 10) ÷ 2 = ", "post": "", "answer": 3,
     "done": "That is t = 3, so v = 16 is right.", "hint": "Subtract u, then divide by a."}]

B[7]["hint"] = "Square the 6 to get 36, then subtract 4 times 6."
B[7]["misconceptions"] = [{
    "pattern": "forgot_square", "expect": -18,
    "message": "\\(x^2\\) = 6 × 6 = 36, then 36 " + MINUS + " 24 = 12. Missing the square, 6 " + MINUS + " 24, gives " + MINUS + "18.",
    "note": "x not squared"}]
B[7]["guided_steps"] = [
    {"say": "Substitute x = 6 into \\(y = x^2 " + MINUS + " 4x\\). Two parts: \\(x^2\\) and 4x.",
     "pre": "Square it: 6 × 6 = ", "post": "", "answer": 36, "hint": "Six sixes."},
    {"phase": "substitute", "say": "Now the 4x part and subtract.",
     "pre": "Work out 4 × 6 = ", "post": "", "answer": 24, "hint": "Four sixes."},
    {"phase": "substitute", "pre": "Subtract: 36 " + MINUS + " 24 = ", "post": "", "answer": 12,
     "done": "y = 12.", "hint": "Take 24 from 36."}]

# ================= SILVER =================
S = pb["silver"]

S[0]["hint"] = "Square negative 4 to get positive 16, then add 3 times negative 4, then subtract 5."
S[0]["misconceptions"] = [
    {"pattern": "sign_on_3x", "expect": 23,
     "message": "3 × (" + MINUS + "4) = " + MINUS + "12, keep the minus: 16 " + MINUS + " 12 " + MINUS + " 5 = " + MINUS + "1. Making it +12 gives 23.",
     "note": "3x sign lost"},
    {"pattern": "neg_squared_wrong", "expect": -33,
     "message": "(" + MINUS + "4)² = (" + MINUS + "4) × (" + MINUS + "4) = +16. A negative times a negative is positive; using " + MINUS + "16 gives " + MINUS + "33.",
     "note": "(-4)^2 taken as -16"}]
S[0]["guided_steps"] = [
    {"say": "Substitute x = " + MINUS + "4 into \\(y = x^2 + 3x " + MINUS + " 5\\). Watch the signs: use brackets.",
     "pre": "Square it: (" + MINUS + "4) × (" + MINUS + "4) = ", "post": "", "answer": 16, "hint": "Negative times negative is positive."},
    {"say": None, "pre": "The 3x part: 3 × (" + MINUS + "4) = ", "post": "", "answer": -12, "hint": "Positive times negative is negative."},
    {"phase": "substitute", "pre": "Combine: 16 + (" + MINUS + "12) = ", "post": "", "answer": 4, "hint": "Adding a negative is subtracting."},
    {"phase": "substitute", "pre": "Subtract the 5: 4 " + MINUS + " 5 = ", "post": "", "answer": -1,
     "done": "y = " + MINUS + "1.", "hint": "Four minus five."}]

S[1]["hint"] = "d is divided by t, so multiply both sides by t to free it."
S[1]["misconceptions"] = [{
    "pattern": "divided_not_multiplied", "expect": 1,
    "message": "To free d you multiply both sides by t, giving d = st. Dividing instead leaves d = s/t, which is wrong.",
    "note": "picks option d=s/t"}]

S[2]["hint"] = "Subtract u from both sides first, then divide by a."
S[2]["misconceptions"] = [{
    "pattern": "added_u", "expect": 1,
    "message": "Subtract u first (v " + MINUS + " u), then divide by a. Adding u gives (v + u)/a, the wrong sign.",
    "note": "picks (v+u)/a"}]

S[3]["hint"] = "The half means multiply both sides by 2, then divide by b."
S[3]["misconceptions"] = [{
    "pattern": "halved_not_doubled", "expect": 1,
    "message": "The ½ means multiply by 2: 2A = bh, so h = 2A/b. Writing A/(2b) halves when you should double.",
    "note": "picks A/(2b)"}]

S[4]["hint"] = "Add inside the bracket first, then divide the total by 2."
S[4]["misconceptions"] = [{
    "pattern": "divided_only_the_3", "expect": 8.5,
    "message": "Work out the top first: (7 + 3) = 10, then ÷ 2 = 5. Dividing only the 3, 7 + 3/2, gives 8.5.",
    "note": "7 + 1.5"}]
S[4]["guided_steps"] = [
    {"say": "Substitute x = 7 into \\(y = \\frac{x+3}{2}\\). The bracket on top is worked out first.",
     "pre": "Top first: 7 + 3 = ", "post": "", "answer": 10, "hint": "Add inside the bracket."},
    {"phase": "substitute", "pre": "Now divide by 2: 10 ÷ 2 = ", "post": "", "answer": 5, "hint": "Half of 10."},
    {"phase": "substitute", "pre": "Check by reversing: 5 × 2 " + MINUS + " 3 = ", "post": "", "answer": 7,
     "done": "That is the x we started with, so y = 5 is right.", "hint": "Times 2, then subtract 3."}]

S[5]["hint"] = "Square the v first, then multiply by m, then halve."
S[5]["misconceptions"] = [
    {"pattern": "forgot_square", "expect": 10,
     "message": "Square v first: 5² = 25. Then ½ × 4 × 25 = 50. Forgetting the square, ½ × 4 × 5, gives 10.",
     "note": "v not squared"},
    {"pattern": "squared_everything", "expect": 100,
     "message": "Only the v is squared, not the whole thing. ½ × 4 × 25 = 50; (½ × 4 × 5)² = 100 squares too much.",
     "note": "(1/2 mv)^2"}]
S[5]["guided_steps"] = [
    {"say": "Substitute m = 4, v = 5 into \\(E = \\frac{1}{2}mv^2\\). Square v first (BIDMAS).",
     "pre": "Square v: 5 × 5 = ", "post": "", "answer": 25, "hint": "Five fives."},
    {"say": None, "pre": "Times m: 4 × 25 = ", "post": "", "answer": 100, "hint": "Four lots of 25."},
    {"phase": "substitute", "pre": "Halve it: 100 ÷ 2 = ", "post": "", "answer": 50, "hint": "Half of 100."},
    {"phase": "substitute", "pre": "Check: double, then divide by m to get v². (50 × 2) ÷ 4 = ", "post": "",
     "answer": 25, "done": "25 is 5², so E = 50 is right.", "hint": "Times 2, then divide by 4."}]

S[6]["hint"] = "Subtract 32 inside the bracket first, then multiply by 5 and divide by 9."
S[6]["misconceptions"] = [{
    "pattern": "stopped_before_dividing", "expect": 180,
    "message": "After 5 × (68 " + MINUS + " 32) = 180 you must divide by 9: 180 ÷ 9 = 20. Stopping at 180 skips the last step.",
    "note": "no divide by 9"}]
S[6]["guided_steps"] = [
    {"say": "Substitute F = 68 into \\(C = \\frac{5(F-32)}{9}\\). Do the bracket first.",
     "pre": "Inside the bracket: 68 " + MINUS + " 32 = ", "post": "", "answer": 36, "hint": "Subtract 32."},
    {"say": None, "pre": "Multiply by 5: 5 × 36 = ", "post": "", "answer": 180, "hint": "Five lots of 36."},
    {"phase": "substitute", "pre": "Now divide by 9: 180 ÷ 9 = ", "post": "", "answer": 20, "hint": "How many 9s in 180?"},
    {"phase": "substitute", "pre": "Check by reversing: (20 × 9) ÷ 5 + 32 = ", "post": "", "answer": 68,
     "done": "That is F = 68, so C = 20 is right.", "hint": "Times 9, divide by 5, add 32."}]

# ================= GOLD (all multiple_choice) =================
G = pb["gold"]
G[0]["hint"] = "Subtract u squared from both sides, then divide by 2a."
G[0]["misconceptions"] = [{
    "pattern": "added_u2", "expect": 1,
    "message": "Subtract u² from both sides first: v² " + MINUS + " u² = 2as. Adding it, (v² + u²)/(2a), is the wrong sign.",
    "note": "picks +u^2 option"}]
G[1]["hint"] = "Divide by pi to get r squared, then take the square root."
G[1]["misconceptions"] = [{
    "pattern": "no_square_root", "expect": 1,
    "message": "After r² = A/π you must square root: r = √(A/π). Stopping at A/π forgets to undo the square.",
    "note": "picks A/pi"}]
G[2]["hint"] = "Multiply both sides by (x minus 1), gather the x terms on one side, then factorise."
G[2]["misconceptions"] = [{
    "pattern": "inner_sign_slip", "expect": 1,
    "message": "Cross-multiply: y(x " + MINUS + " 1) = x + 3, gather x terms, x(y " + MINUS + " 1) = y + 3, so x = (y + 3)/(y " + MINUS + " 1). Flipping the inner signs gives (y " + MINUS + " 3)/(y + 1).",
    "note": "picks (y-3)/(y+1)"}]
G[3]["hint"] = "Look at whether t appears in more than one term."
G[3]["misconceptions"] = [{
    "pattern": "factorise_wont_isolate", "expect": 2,
    "message": "Factorising gives t(u + ½at) = s, but t is still inside the bracket, so it is not isolated. Because t appears as t and t², you need the quadratic formula.",
    "note": "picks factorise option"}]
G[4]["hint"] = "Divide by 2 pi, square both sides, then multiply by g."
G[4]["misconceptions"] = [{
    "pattern": "divided_by_g", "expect": 1,
    "message": "After (T/(2π))² = l/g, multiply by g: l = gT²/(4π²). Dividing by g instead gives T²/(4π²g).",
    "note": "picks /g option"}]

# ---------- tier_guides ----------
tier_guides = {
    "bronze": {
        "title": "Bronze: put the numbers in",
        "steps": [
            "Substitution means swapping each letter for its given number, then calculating. Write brackets around any negative value so its sign stays safe.",
            "Follow <strong>BIDMAS</strong>: do powers (like \\(x^2\\)) and brackets before you multiply, and multiply before you add.",
            "Work through what is left and write the single number that comes out."
        ],
        "example": {
            "question": "Find y when x = 3, given y = 4x + 5",
            "steps": [
                {"label": "Substitute", "content": "<p>\\(y = 4(3) + 5\\)</p>"},
                {"label": "Multiply", "content": "<p>\\(4 \\times 3 = 12\\)</p>"},
                {"label": "Add", "content": "<p>\\(12 + 5 = 17\\)</p>"},
                {"label": "Check", "content": "<p>\\((17 " + MINUS + " 5) \\div 4 = 3\\), the x we started with ✓</p>"},
                {"label": "Answer", "content": "<p>\\(y = 17\\)</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: harder formulae, or a one-step rearrange",
        "steps": [
            "Substituting into powers and fractions: work out the top of a fraction fully before dividing, and square a value before multiplying it.",
            "To <strong>change the subject</strong>, undo the operations around the new letter in reverse. Whatever you do to one side, do to the other.",
            "A fraction like \\(\\frac{1}{2}bh\\) means the new letter is being divided, so multiply both sides to release it."
        ],
        "example": {
            "question": "Make t the subject of v = u + at",
            "steps": [
                {"label": "Subtract u", "content": "<p>\\(v " + MINUS + " u = at\\)</p>"},
                {"label": "Divide by a", "content": "<p>\\(\\frac{v " + MINUS + " u}{a} = t\\)</p>"},
                {"label": "Check", "content": "<p>Put it back: \\(u + a \\cdot \\frac{v-u}{a} = u + (v-u) = v\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(t = \\frac{v " + MINUS + " u}{a}\\)</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: several moves to change the subject",
        "steps": [
            "When the new letter is squared or under a root, undo that last: square both sides to remove a root, or square-root both sides to remove a square.",
            "If the new letter appears in <strong>two</strong> places, gather those terms on one side and factorise it out before dividing.",
            "If the letter appears as both itself and its square (like \\(t\\) and \\(t^2\\)), no rearrangement isolates it: it is a quadratic."
        ],
        "example": {
            "question": "Make r the subject of A = πr²",
            "steps": [
                {"label": "Divide by π", "content": "<p>\\(\\frac{A}{\\pi} = r^2\\)</p>"},
                {"label": "Square root", "content": "<p>\\(r = \\sqrt{\\frac{A}{\\pi}}\\)</p>"},
                {"label": "Check", "content": "<p>Squaring gives \\(r^2 = \\frac{A}{\\pi}\\), so \\(A = \\pi r^2\\) ✓</p>"},
                {"label": "Answer", "content": "<p>\\(r = \\sqrt{\\frac{A}{\\pi}}\\)</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

# ---------- guided (opener + teach) ----------
guided = {
    "opener": {
        "label": "Before any algebra",
        "display": "A taxi charges £3 the moment you get in, then £2 for every mile you travel.",
        "steps": [
            {"say": "No algebra needed, just common sense.",
             "pre": "For a 4-mile trip you pay £", "post": "", "answer": 11,
             "hint": "£3 to start, plus 2 × 4 miles."},
            {"say": "Same rule, longer journey.",
             "pre": "For a 7-mile trip you pay £", "post": "", "answer": 17,
             "hint": "£3 to start, plus 2 × 7 miles."},
            {"say": "You just used a formula: cost = 3 + 2 × (miles). Swapping the miles for a number and working it out is called <strong>substitution</strong>. In algebra we write it \\(C = 3 + 2m\\), and every question here is that same move: put the numbers in, then calculate."}
        ]
    },
    "teach": {
        "bronze": {
            "label": "Together: your first substitution",
            "display": "\\(y = x^2 + 2x\\). Find \\(y\\) when \\(x = 5\\).",
            "steps": [
                {"say": "Substitute x = 5 into \\(y = x^2 + 2x\\). It has two parts.",
                 "pre": "Square x: 5 × 5 = ", "post": "", "answer": 25, "hint": "Five fives."},
                {"pre": "Now the 2x part: 2 × 5 = ", "post": "", "answer": 10, "hint": "Two fives."},
                {"pre": "Add them: 25 + 10 = ", "post": "", "answer": 35, "done": "That is y.", "hint": "Add your two parts."},
                {"say": "Check it.", "pre": "Take the 2x part off again: 35 " + MINUS + " 10 = ", "post": "",
                 "answer": 25, "done": "25 is 5², so y = 35 is right.", "hint": "Subtract 10."}
            ]
        },
        "silver": {
            "label": "Together: rearrange, then substitute",
            "display": "\\(v = u + at\\). A car speeds up from \\(u = 5\\) to \\(v = 29\\) with \\(a = 6\\). Find \\(t\\).",
            "steps": [
                {"say": "t is stuck inside u + at. Rearrange first: \\(t = \\frac{v - u}{a}\\). Now put the numbers in.",
                 "pre": "Top first: 29 " + MINUS + " 5 = ", "post": "", "answer": 24, "hint": "Subtract u from v."},
                {"pre": "Divide by a: 24 ÷ 6 = ", "post": "", "answer": 4, "done": "So t = 4.", "hint": "How many 6s in 24?"},
                {"say": "Check by substituting t = 4 back into \\(v = u + at\\).",
                 "pre": "a × t: 6 × 4 = ", "post": "", "answer": 24, "hint": "Six fours."},
                {"pre": "u + that: 5 + 24 = ", "post": "", "answer": 29,
                 "done": "That is v, so t = 4 is right.", "hint": "Add u."}
            ]
        },
        "gold": {
            "label": "Together: change the subject, then use it",
            "display": "\\(v^2 = u^2 + 2as\\). A stone has \\(v = 10\\), \\(u = 6\\), \\(a = 8\\). Find the distance \\(s\\).",
            "steps": [
                {"say": "s is inside 2as. Rearrange: \\(s = \\frac{v^2 - u^2}{2a}\\). Now the numbers.",
                 "pre": "Square v: 10 × 10 = ", "post": "", "answer": 100, "hint": "Ten tens."},
                {"pre": "Square u: 6 × 6 = ", "post": "", "answer": 36, "hint": "Six sixes."},
                {"pre": "Subtract: 100 " + MINUS + " 36 = ", "post": "", "answer": 64, "hint": "Take 36 from 100."},
                {"pre": "Work out 2a: 2 × 8 = ", "post": "", "answer": 16, "hint": "Double the a."},
                {"pre": "Divide: 64 ÷ 16 = ", "post": "", "answer": 4,
                 "done": "s = 4. That is the whole gold move: rearrange, then substitute.", "hint": "How many 16s in 64?"}
            ]
        }
    }
}

# ---------- slim method_card ----------
method_card = {
    "title": "How to Substitute and Rearrange Formulae",
    "steps": [
        "Substitute: swap each letter for its value, using brackets for negatives.",
        "Evaluate with BIDMAS: powers and brackets before multiply, multiply before add.",
        "Rearrange: undo the operations around the new subject in reverse.",
        "Squared subject? Square root at the end. Under a root? Square both sides."
    ],
    "content": "<p><strong>Substitution:</strong> Replace each letter with its value and calculate, using brackets around negatives and BIDMAS order.</p><p><strong>Rearranging:</strong> Isolate the new subject with inverse operations, just like solving an equation. If it is squared, square root at the end; if it appears twice, factorise it out.</p>"
}

out = {
    "method_card": method_card,
    "topic_links": live.get("topic_links", {"prerequisites": []}),
    "problem_bank": pb,
    "related_videos": live.get("related_videos", []),
    "worked_examples": live.get("worked_examples", []),
    "tier_guides": tier_guides,
    "guided": guided
}

with io.open("lesson_maths-eduqas_algebra-L04.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1, ensure_ascii=False)
print("written. em-dash present:", "—" in json.dumps(out, ensure_ascii=False))
