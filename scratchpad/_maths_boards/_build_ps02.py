# -*- coding: utf-8 -*-
"""Full guided-learning + diagrams conversion for probability-statistics-L02 (maths-aqa).
Venn Diagrams & Conditional Probability. id ec35471d-bdb2-419a-9f86-1b8b85d6d5a7."""
import json, io

SRC = "_live_ps02.json"
KEY = "probability-statistics-L02"
OUT = "lesson_maths-aqa_%s.json" % KEY

pd = json.load(io.open(SRC, encoding="utf-8"))
pb = pd["problem_bank"]
b, s, g = pb["bronze"], pb["silver"], pb["gold"]

# ---------- Venn SVG ----------
def venn(aria, la, lb, a_only, both, b_only, neither, total=None, wanted=None):
    wanted = wanted or set()
    def txt(x, y, sv, anchor="middle", bold=False, size=12):
        w = ' font-weight="700"' if bold else ''
        return ('<text x="%d" y="%d" font-family="Inter, sans-serif" font-size="%d" '
                'fill="currentColor" text-anchor="%s"%s>%s</text>') % (x, y, size, anchor, w, sv)
    p = ['<svg viewBox="0 0 260 180" role="img" aria-label="%s" style="max-width:260px">' % aria]
    p.append('<rect x="8" y="10" width="244" height="150" rx="6" fill="none" stroke="currentColor" stroke-width="1"/>')
    p.append('<circle cx="100" cy="90" r="52" fill="#60a5fa" fill-opacity="0.15" stroke="currentColor" stroke-width="1"/>')
    p.append('<circle cx="160" cy="90" r="52" fill="#f59e0b" fill-opacity="0.15" stroke="currentColor" stroke-width="1"/>')
    p.append(txt(72, 54, la, bold=True))
    p.append(txt(188, 54, lb, bold=True))
    if a_only != "": p.append(txt(76, 96, str(a_only), bold=("a_only" in wanted)))
    if both != "": p.append(txt(130, 96, str(both), bold=("both" in wanted)))
    if b_only != "": p.append(txt(184, 96, str(b_only), bold=("b_only" in wanted)))
    if neither != "": p.append(txt(236, 150, str(neither), bold=("neither" in wanted)))
    if total is not None:
        p.append(txt(14, 26, "Total: %s" % total, anchor="start", size=11, bold=("total" in wanted)))
    p.append('</svg>')
    return "".join(p)

def prepend(prob, svg):
    prob["display"] = svg + "<br>" + prob["display"]

# ---------- descriptions ----------
pb["bronze_description"] = "Read and fill a Venn diagram: work from the intersection outward, then find a count or a simple probability over the total."
pb["silver_description"] = "Conditional probability and the addition rule: P(A|B) restricts to the given group, and P(A∪B) = P(A) + P(B) − P(A∩B)."
pb["gold_description"] = "Combine the rules: the multiplication rule, testing independence, and the total-probability rule across both branches."

# ---------- hints ----------
hints = {
 "bronze": [
  "Fill the overlap first, then subtract it from each total; neither is the rest.",
  "Maths only is 22 minus the 8 overlap, then put it over 40.",
  "Add both totals and subtract the overlap once, then divide by 60.",
  "Add all four regions, including the neither group outside the circles.",
  "A only is P(A) minus the overlap P(A and B).",
  "Find how many like at least one, then the rest like neither.",
  "Everyone in circle A counts, both the overlap and A only: 25 out of 50.",
  "Turn the probabilities into counts out of 100, then take the overlap off A.",
 ],
 "silver": [
  "Given rugby, divide the overlap by the rugby total, not by 80.",
  "Add P(A) and P(B), then subtract the overlap once.",
  "The overlap is P(A) plus P(B) minus the union.",
  "Given football, divide the overlap by the football total, not by 60.",
  "Events are independent when P(A) times P(B) equals P(A and B).",
  "Divide the overlap P(A and B) by P(B).",
  "Given art, divide the girls-who-do-art by the total who do art.",
 ],
 "gold": [
  "Multiply: P(A and B) = P(A) times P(B given A).",
  "Given tea, divide the overlap by the tea total, not by 120.",
  "Add both routes to A: through B and through not B.",
  "Independent neither: multiply the complements P(A') and P(B').",
  "Find the overlap from the addition rule first, then divide by P(B).",
 ],
}
for tier in ("bronze", "silver", "gold"):
    for i, h in enumerate(hints[tier]):
        pb[tier][i]["hint"] = h

# ---------- misconceptions ----------
def mc(pattern, message, expect, note):
    return {"pattern": pattern, "message": message, "expect": expect, "note": note}

miscon = {
 "bronze": [
  [mc("forget_intersection", "If you add 22 + 18 = 40 you count the 8 both twice, leaving neither = 0. Subtract the overlap: 14 + 8 + 10 = 32, so neither = 40 − 32 = 8.", [0], "double-counted both")],
  [mc("include_both", "22/40 counts the overlap as maths only. Maths ONLY is 22 − 8 = 14, so P = 14/40 = 7/20.", [11, 20], "used n(A) not A-only")],
  [mc("add_without_subtract", "(35 + 28)/60 counts the 13 both twice. Subtract the overlap once: 50/60 = 5/6.", [63, 60], "no subtract overlap")],
  [mc("miss_neither", "10 + 5 + 15 = 30 leaves out the 20 in the neither region. The total includes them: 10 + 5 + 15 + 20 = 50.", [30], "forgot neither")],
  [mc("forgot_subtract", "0.6 is all of A. A only removes the overlap: 0.6 − 0.2 = 0.4.", [0.6], "gave P(A)")],
  [mc("gave_at_least_one", "40/50 = 4/5 is P(likes at least one). Neither is the rest: 1 − 4/5 = 1/5.", [4, 5], "complement of neither")],
  [mc("just_intersection", "5/50 is only the overlap. Circle A holds everyone in A: 25/50 = 1/2.", [1, 10], "used intersection")],
  [mc("forgot_subtract", "45 is all of A. A only removes the overlap: 45 − 15 = 30.", [45], "gave n(A)")],
 ],
 "silver": [
  [mc("used_total", "20/80 divides by the whole group. Given rugby, divide by the rugby total: 20/40 = 1/2.", [1, 4], "divided by 80")],
  [mc("add_only", "0.5 + 0.4 = 0.9 double counts the overlap. Subtract it once: 0.9 − 0.2 = 0.7.", [0.9], "no subtract")],
  [mc("assumed_independent", "0.7 × 0.5 = 0.35 only works if independent. Use P(A ∩ B) = P(A) + P(B) − P(A ∪ B) = 0.3.", [0.35], "multiplied")],
  [mc("used_total", "15/60 divides by the whole group. Given football, divide by the football total: 15/35 = 3/7.", [1, 4], "divided by 60")],
  [mc("wrong_test", "0.3 × 0.4 = 0.12, which equals P(A ∩ B), so the events ARE independent.", [1], "chose No")],
  [mc("gave_intersection", "0.24 = 6/25 is the overlap itself. Divide by P(B): 0.24/0.6 = 2/5.", [6, 25], "gave intersection")],
  [mc("used_total", "70/200 divides by everyone. Given art, divide by the 120 who do art: 70/120 = 7/12.", [7, 20], "divided by 200")],
 ],
 "gold": [
  [mc("added_not_multiplied", "0.3 + 0.5 = 0.8 adds instead of multiplying. For P(A ∩ B) multiply: 0.3 × 0.5 = 0.15.", [0.8], "added")],
  [mc("used_total", "30/120 divides by everyone. Given tea, divide by the 80 who like tea: 30/80 = 3/8.", [1, 4], "divided by 120")],
  [mc("one_branch_only", "0.6 × 0.5 = 0.3 is only the route through B. Add the other route: 0.3 + 0.2 × 0.5 = 0.4.", [0.3], "one branch")],
  [mc("used_events", "0.4 × 0.5 = 0.2 = 1/5 multiplies the events, not their complements. Use P(A') × P(B') = 0.6 × 0.5 = 0.3 = 3/10.", [1, 5], "used events")],
  [mc("used_union", "0.8/0.6 divides the union. First find the overlap 0.5 + 0.6 − 0.8 = 0.3, then 0.3/0.6 = 1/2.", [4, 3], "divided union")],
 ],
}
for tier in ("bronze", "silver", "gold"):
    for i, m in enumerate(miscon[tier]):
        pb[tier][i]["misconceptions"] = m

# ---------- guided_steps helpers ----------
def say(t): return {"say": t}
def box(pre, ans, hint, done=None, phase=None):
    d = {"pre": pre, "post": "", "answer": ans, "hint": hint}
    if done: d["done"] = done
    if phase: d["phase"] = phase
    return d
def sbox(sayt, pre, ans, hint, done=None):  # substitute box carrying a say line
    d = {"say": sayt, "phase": "substitute", "pre": pre, "post": "", "answer": ans, "hint": hint}
    if done: d["done"] = done
    return d

# BRONZE walks
b[0]["guided_steps"] = [
 say("Fill the Venn from the middle out: the overlap first, then each single region, then what is left."),
 box("Both maths and science (the overlap) = ", 8, "Given as 8."),
 box("Maths only: 22 − 8 = ", 14, "Take the overlap off the maths total."),
 box("Science only: 18 − 8 = ", 10, "Take the overlap off the science total."),
 sbox("Add the three filled regions.", "14 + 8 + 10 = ", 32, "Everyone who likes at least one."),
 box("Neither: 40 − 32 = ", 8, "The rest of the group.", done="8 like neither.", phase="substitute"),
]
b[1]["guided_steps"] = [
 say("Maths only means maths but NOT the overlap. Find that count, then put it over the total."),
 box("Maths only: 22 − 8 = ", 14, "Take the overlap off."),
 box("Total students = ", 40, "The whole group."),
 sbox("So P(maths only) = 14/40. Simplify by dividing top and bottom by 2.", "14 ÷ 2 = ", 7, "Halve the top."),
 box("40 ÷ 2 = ", 20, "Halve the bottom.", done="P(maths only) = 7/20.", phase="substitute"),
]
b[2]["guided_steps"] = [
 say("Cat or dog means in either circle. Add the totals, then subtract the overlap once so it is not double counted."),
 box("Cats plus dogs: 35 + 28 = ", 63, "Add both totals."),
 box("Subtract the overlap once: 63 − 13 = ", 50, "The 13 both were counted twice."),
 box("Total people = ", 60, "The whole group."),
 sbox("So P(cat or dog) = 50/60. Simplify by dividing by 10.", "50 ÷ 10 = ", 5, "Divide the top by 10."),
 box("60 ÷ 10 = ", 6, "Divide the bottom by 10.", done="P(cat or dog) = 5/6.", phase="substitute"),
]
b[3]["guided_steps"] = [
 say("The total is every region added together, including the neither region outside the circles."),
 box("Overlap (A and B) = ", 5, "Given as 5."),
 box("In the circles: 10 + 5 + 15 = ", 30, "A only, both, then B only."),
 sbox("Now add the neither region to reach the total.", "30 + 20 = ", 50, "Include those outside the circles."),
 box("Check: 10 + 5 + 15 + 20 = ", 50, "All four regions.", done="Total = 50.", phase="substitute"),
]
b[4]["guided_steps"] = [
 say("A only means the part of A that does not overlap B. Subtract the overlap from all of A."),
 box("All of A, P(A) = ", 0.6, "Given as 0.6."),
 box("The overlap P(A ∩ B) = ", 0.2, "Given as 0.2."),
 sbox("A only is what is left after removing the overlap.", "0.6 − 0.2 = ", 0.4, "Take the overlap off."),
 box("Check: A only plus overlap gives all of A. 0.4 + 0.2 = ", 0.6, "Should return P(A).", done="P(A only) = 0.4.", phase="substitute"),
]
b[5]["guided_steps"] = [
 say("Find how many like at least one subject, then the rest of the group like neither."),
 box("English only: 30 − 10 = ", 20, "Take the overlap off English."),
 box("History only: 20 − 10 = ", 10, "Take the overlap off History."),
 box("At least one: 20 + 10 + 10 = ", 40, "Add the three circle regions."),
 sbox("Neither is the total minus those 40.", "50 − 40 = ", 10, "The rest of the group."),
 box("So P(neither) = 10/50. Simplify by 10, top: 10 ÷ 10 = ", 1, "Numerator over 10.", phase="substitute"),
 box("50 ÷ 10 = ", 5, "Denominator over 10.", done="P(neither) = 1/5.", phase="substitute"),
]
b[6]["guided_steps"] = [
 say("P(A) uses everyone inside circle A: both the overlap and the A-only part."),
 box("Number in set A = ", 25, "Given as 25."),
 box("Total students = ", 50, "Out of 50."),
 sbox("So P(A) = 25/50. Simplify by dividing by 25.", "25 ÷ 25 = ", 1, "Top divided by 25."),
 box("50 ÷ 25 = ", 2, "Bottom divided by 25.", done="P(A) = 1/2.", phase="substitute"),
]
b[7]["guided_steps"] = [
 say("Turn each probability into a count out of 100, then take the overlap off A."),
 box("n(A) = 0.45 × 100 = ", 45, "0.45 of 100."),
 box("n(A ∩ B) = 0.15 × 100 = ", 15, "0.15 of 100."),
 sbox("A only removes the overlap from A.", "45 − 15 = ", 30, "Take the overlap off."),
 box("Check: A only plus overlap = 30 + 15 = ", 45, "Should return n(A).", done="n(A only) = 30.", phase="substitute"),
]

# SILVER walks
s[0]["guided_steps"] = [
 say("Given rugby, we only look inside the rugby group. P(F|R) = both, over the rugby total."),
 box("Both football and rugby = ", 20, "The overlap."),
 box("Rugby total (the given group) = ", 40, "All who play rugby."),
 sbox("So P(F|R) = 20/40. Simplify by dividing by 20.", "20 ÷ 20 = ", 1, "Top over 20."),
 box("40 ÷ 20 = ", 2, "Bottom over 20.", done="P(F|R) = 1/2.", phase="substitute"),
]
s[1]["guided_steps"] = [
 say("Union is everything in either set. Add the two, then subtract the overlap so it is counted once."),
 box("P(A) + P(B) = 0.5 + 0.4 = ", 0.9, "Add the two."),
 box("The overlap P(A ∩ B) = ", 0.2, "Given as 0.2."),
 sbox("Subtract the overlap once.", "0.9 − 0.2 = ", 0.7, "Remove the double count."),
 box("Check: 0.5 + 0.4 − 0.2 = ", 0.7, "The addition rule.", done="P(A ∪ B) = 0.7.", phase="substitute"),
]
s[2]["guided_steps"] = [
 say("Rearrange the addition rule: the overlap equals P(A) + P(B) minus the union."),
 box("P(A) + P(B) = 0.7 + 0.5 = ", 1.2, "Add the two sets."),
 box("The union P(A ∪ B) = ", 0.9, "Given as 0.9."),
 sbox("Subtract the union from that sum.", "1.2 − 0.9 = ", 0.3, "This gives the overlap."),
 box("Check: 0.7 + 0.5 − 0.3 = 0.9, the union. Type the overlap again: ", 0.3, "It stays 0.3.", done="P(A ∩ B) = 0.3.", phase="substitute"),
]
s[3]["guided_steps"] = [
 say("Given football, look only inside the football group. P(C|F) = both, over the football total."),
 box("Both cricket and football = ", 15, "The overlap."),
 box("Football total (the given group) = ", 35, "All who play football."),
 sbox("So P(C|F) = 15/35. Simplify by dividing by 5.", "15 ÷ 5 = ", 3, "Top over 5."),
 box("35 ÷ 5 = ", 7, "Bottom over 5.", done="P(C|F) = 3/7.", phase="substitute"),
]
# s[4] multiple_choice: no guided_steps
s[5]["guided_steps"] = [
 say("Conditional formula: P(A|B) = P(A ∩ B) over P(B)."),
 box("P(A ∩ B) = ", 0.24, "Given as 0.24."),
 box("P(B) = ", 0.6, "Given as 0.6."),
 sbox("Divide the overlap by P(B).", "0.24 ÷ 0.6 = ", 0.4, "Overlap over the given set."),
 box("0.4 = 4/10, simplify by 2, top: 4 ÷ 2 = ", 2, "Numerator over 2.", phase="substitute"),
 box("10 ÷ 2 = ", 5, "Denominator over 2.", done="P(A|B) = 2/5.", phase="substitute"),
]
s[6]["guided_steps"] = [
 say("Given art, look only inside the art group. P(girl|art) = girls who do art, over all who do art."),
 box("Girls who do art = ", 70, "The overlap of girl and art."),
 box("Total who do art (the given group) = ", 120, "All art students."),
 sbox("So P(girl|art) = 70/120. Simplify by dividing by 10.", "70 ÷ 10 = ", 7, "Top over 10."),
 box("120 ÷ 10 = ", 12, "Bottom over 10.", done="P(girl|art) = 7/12.", phase="substitute"),
]

# GOLD walks
g[0]["guided_steps"] = [
 say("Multiply rule: P(A ∩ B) = P(A) × P(B given A)."),
 box("P(A) = ", 0.3, "Given as 0.3."),
 box("P(B given A) = ", 0.5, "Given as 0.5."),
 sbox("Multiply them together.", "0.3 × 0.5 = ", 0.15, "Three tenths of a half."),
 box("Check: an overlap is smaller than each part. Type 0.15 again: ", 0.15, "It stays 0.15.", done="P(A ∩ B) = 0.15.", phase="substitute"),
]
g[1]["guided_steps"] = [
 say("Given tea, look only inside the tea group. P(coffee|tea) = both, over the tea total."),
 box("Both tea and coffee = ", 30, "The overlap."),
 box("Tea total (the given group) = ", 80, "All who like tea."),
 sbox("So P(coffee|tea) = 30/80. Simplify by dividing by 10.", "30 ÷ 10 = ", 3, "Top over 10."),
 box("80 ÷ 10 = ", 8, "Bottom over 10.", done="P(coffee|tea) = 3/8.", phase="substitute"),
]
g[2]["guided_steps"] = [
 say("A can happen through B or through not B. Total probability adds both routes."),
 box("Route through B: 0.6 × 0.5 = ", 0.3, "P(A|B) times P(B)."),
 box("Route through not B: 0.2 × 0.5 = ", 0.1, "P(A|B') times P(B')."),
 sbox("Add the two routes.", "0.3 + 0.1 = ", 0.4, "Both ways of reaching A."),
 box("Check: the two routes cover everything, so this is P(A). Type it again: ", 0.4, "It stays 0.4.", done="P(A) = 0.4.", phase="substitute"),
]
g[3]["guided_steps"] = [
 say("Neither event means A' and B'. For independent events, multiply the complements."),
 box("P(A') = 1 − 0.4 = ", 0.6, "The complement of A."),
 box("P(B') = 1 − 0.5 = ", 0.5, "The complement of B."),
 sbox("Independent, so multiply the complements.", "0.6 × 0.5 = ", 0.3, "Both complements together."),
 box("Write 0.3 as a fraction. Numerator (0.3 = 3/10) = ", 3, "Three tenths, top.", phase="substitute"),
 box("Denominator = ", 10, "Out of ten.", done="P(A' ∩ B') = 3/10.", phase="substitute"),
]
g[4]["guided_steps"] = [
 say("First find the overlap from the addition rule, then divide by P(B)."),
 box("P(A) + P(B) = 0.5 + 0.6 = ", 1.1, "Add the two sets."),
 box("Subtract the union: 1.1 − 0.8 = ", 0.3, "This is P(A ∩ B)."),
 sbox("Now the conditional: divide the overlap by P(B).", "0.3 ÷ 0.6 = ", 0.5, "Overlap over the given set."),
 box("Write 0.5 as a fraction. Numerator (0.5 = 1/2) = ", 1, "One half, top.", phase="substitute"),
 box("Denominator = ", 2, "Out of two.", done="P(A|B) = 1/2.", phase="substitute"),
]

# ---------- figures (Venn) on concrete/explicit problems ----------
prepend(b[0], venn("Venn: maths and science, overlap 8", "Maths", "Science", 14, 8, 10, "?", total=40, wanted={"neither"}))
prepend(b[1], venn("Venn: maths and science, overlap 8", "Maths", "Science", 14, 8, 10, 8, total=40, wanted={"a_only"}))
prepend(b[2], venn("Venn: cat and dog owners, overlap 13", "Cat", "Dog", 22, 13, 15, 10, total=60))
prepend(b[3], venn("Venn: sets A and B", "A", "B", 10, 5, 15, 20, total="?", wanted={"total"}))
prepend(b[5], venn("Venn: English and History, overlap 10", "English", "History", 20, 10, 10, "?", total=50, wanted={"neither"}))
prepend(b[6], venn("Venn: set A with 25 members out of 50", "A", "B", 20, 5, "", "", total=50, wanted={"a_only"}))
prepend(b[7], venn("Venn: sets A and B out of 100", "A", "B", "?", 15, 20, 35, total=100, wanted={"a_only"}))

prepend(s[0], venn("Venn: football and rugby, overlap 20", "Football", "Rugby", 30, 20, 20, 10, total=80, wanted={"both"}))
prepend(s[3], venn("Venn: football and cricket, overlap 15", "Football", "Cricket", 20, 15, 15, 10, total=60, wanted={"both"}))
prepend(s[6], venn("Venn: girls and art students, overlap 70", "Girl", "Art", 40, 70, 50, 40, total=200, wanted={"both"}))

prepend(g[1], venn("Venn: tea and coffee drinkers, overlap 30", "Tea", "Coffee", 50, 30, 20, 20, total=120, wanted={"both"}))

# ---------- tier_guides ----------
pd["tier_guides"] = {
 "bronze": {
  "title": "Bronze: reading and filling a Venn diagram",
  "steps": [
   "Fill the <strong>intersection</strong> (the overlap) first.",
   "Subtract it from each set total to get the <strong>only</strong> regions.",
   "The rest of the group goes in <strong>neither</strong>, outside the circles.",
   "A probability is that region divided by the total.",
  ],
  "example": {
   "question": "30 people: 16 like tea, 14 like coffee, 6 like both. Find P(neither).",
   "steps": [
    {"label": "Overlap", "content": "both = 6"},
    {"label": "Only regions", "content": "tea only 10, coffee only 8"},
    {"label": "Neither", "content": "30 − (10 + 6 + 8) = 6"},
    {"label": "Answer", "content": "P(neither) = 6/30 = 1/5", "isAnswer": True, "is_answer": True},
   ],
  },
 },
 "silver": {
  "title": "Silver: conditional probability and the addition rule",
  "steps": [
   "Conditional: \\(P(A|B) = \\frac{n(A \\cap B)}{n(B)}\\), dividing by the <strong>given</strong> group.",
   "Addition rule: \\(P(A \\cup B) = P(A) + P(B) - P(A \\cap B)\\).",
   "Rearrange it to find any one missing part.",
  ],
  "example": {
   "question": "50 people: 30 like tea, 18 like both tea and cake. Find P(cake | tea).",
   "steps": [
    {"label": "Given group", "content": "tea total = 30"},
    {"label": "Overlap", "content": "both = 18"},
    {"label": "Check", "content": "P(cake|tea) = 18/30"},
    {"label": "Answer", "content": "18/30 = 3/5", "isAnswer": True, "is_answer": True},
   ],
  },
 },
 "gold": {
  "title": "Gold: independence and combined rules",
  "steps": [
   "Multiply: \\(P(A \\cap B) = P(B|A)\\,P(A)\\).",
   "Independent when \\(P(A) \\times P(B) = P(A \\cap B)\\).",
   "Total probability: \\(P(A) = P(A|B)P(B) + P(A|B')P(B')\\).",
  ],
  "example": {
   "question": "P(A) = 0.2, P(B) = 0.5, independent. Find P(A ∩ B).",
   "steps": [
    {"label": "Test", "content": "independent, so multiply"},
    {"label": "Multiply", "content": "0.2 × 0.5"},
    {"label": "Check", "content": "smaller than each part"},
    {"label": "Answer", "content": "P(A ∩ B) = 0.1", "isAnswer": True, "is_answer": True},
   ],
  },
 },
}

# ---------- guided (opener + teach) ----------
opener_venn = venn("Venn: 10 friends, football and chess loops", "Football", "Chess", 2, 4, 3, 1, total=10)
pd["guided"] = {
 "opener": {
  "steps": [
   {"say": "Here are 10 friends. One loop is who plays football, the other is who plays chess. The numbers show how many are in each part.",
    "display": opener_venn},
   {"pre": "How many play football in total (both parts of the football loop)? ", "post": "", "answer": 6,
    "hint": "Add the football-only 2 and the overlap 4."},
   {"pre": "Of those footballers, how many also play chess? ", "post": "", "answer": 4,
    "hint": "The overlap, inside both loops."},
   {"say": "Pick a footballer at random: 4 of the 6 also play chess, so the chance is \\(\\tfrac{4}{6} = \\tfrac{2}{3}\\). You just found a <strong>conditional</strong> probability: you looked only inside the football group. That is P(chess given football)."},
  ],
 },
 "teach": {
  "bronze": {
   "display": venn("Venn: phone and tablet owners, overlap 10", "Phone", "Tablet", 15, 10, 10, "?", total=40, wanted={"neither"})
              + "<br>40 people: 25 own a phone, 20 own a tablet, 10 own both. How many own neither?",
   "steps": [
    say("Fill from the overlap out, then the total minus the circles gives neither."),
    box("Both phone and tablet = ", 10, "Given as 10."),
    box("Phone only: 25 − 10 = ", 15, "Take the overlap off the phone total."),
    box("Tablet only: 20 − 10 = ", 10, "Take the overlap off the tablet total."),
    box("In the circles: 15 + 10 + 10 = ", 35, "Everyone who owns at least one."),
    box("Neither: 40 − 35 = ", 5, "The rest of the group.",
        done="5 own neither. Total minus the circles, every time."),
   ],
  },
  "silver": {
   "display": venn("Venn: pizza and pasta, overlap 15", "Pizza", "Pasta", 25, 15, 10, 10, total=60, wanted={"both"})
              + "<br>60 people: 40 like pizza, 25 like pasta, 15 like both. Find P(pasta given pizza).",
   "steps": [
    say("Given pizza, only look inside the pizza group. The given total is the denominator."),
    box("Both pizza and pasta = ", 15, "The overlap."),
    box("Pizza total (the given group) = ", 40, "All who like pizza."),
    box("So P(pasta|pizza) = 15/40. Simplify by 5, top: 15 ÷ 5 = ", 3, "Top over 5."),
    box("40 ÷ 5 = ", 8, "Bottom over 5.",
        done="P(pasta|pizza) = 3/8. The given group is the denominator: that is the whole move."),
   ],
  },
  "gold": {
   "display": venn("Venn: independent events A and B as probabilities", "A", "B", 0.3, 0.2, 0.2, 0.3, total=1, wanted={"both"})
              + "<br>P(A) = 0.5, P(B) = 0.4, and A and B are independent. Find P(A ∪ B).",
   "steps": [
    say("Independent, so the overlap is the product. Then use the addition rule for the union."),
    box("P(A ∩ B) = 0.5 × 0.4 = ", 0.2, "Multiply for independent events."),
    box("P(A) + P(B) = 0.5 + 0.4 = ", 0.9, "Add the two."),
    box("Union: 0.9 − 0.2 = ", 0.7, "Subtract the overlap once."),
    box("Check: A only 0.3, both 0.2, B only 0.2 add to 0.7. Type it: ", 0.7, "Read from the Venn.",
        done="P(A ∪ B) = 0.7. Independent gives the overlap by multiplying: that is the new move."),
   ],
  },
 },
}

# ---------- method_card: trim to <= 4 steps ----------
pd["method_card"]["steps"] = [
 "Draw two overlapping circles inside a rectangle.",
 "Fill the intersection first, then subtract it from each set total.",
 "Put the rest in the 'neither' region; all regions total the whole group.",
 "Conditional: P(A|B) = n(A∩B) / n(B), dividing by the given group.",
]

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote", OUT)

def wc(sv):
    return len([w for w in (sv or "").replace("\\(", " ").replace("\\)", " ").split() if w])
print("method_card content words:", wc(pd["method_card"].get("content")))
for tier in ("bronze","silver","gold"):
    tot = sum(wc(x) for x in pd["tier_guides"][tier]["steps"])
    print("tier_guide", tier, "step words:", tot)
