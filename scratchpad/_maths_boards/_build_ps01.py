# -*- coding: utf-8 -*-
"""Full guided-learning + diagrams conversion for probability-statistics-L01 (maths-aqa)."""
import json, io

SRC = "_live_ps01.json"
KEY = "probability-statistics-L01"
OUT = "lesson_maths-aqa_%s.json" % KEY

pd = json.load(io.open(SRC, encoding="utf-8"))

# ---------- SVG helpers ----------
def tree2(aria, labA, pA, labB, pB, s2, leaves, wanted):
    """2-stage, 4-leaf tree. s2 = [pAA,pAB,pBA,pBB] second-stage prob strings.
    leaves = ['RR','RB','BR','BB']; wanted = set of indices to highlight."""
    # coords
    rx, ry = 16, 95
    n1 = (108, 46); n2 = (108, 144)
    lf = [(232, 24), (232, 68), (232, 120), (232, 164)]
    def line(x1, y1, x2, y2):
        return '<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1"/>' % (x1, y1, x2, y2)
    def txt(x, y, s, anchor="middle", bold=False, size=11):
        w = ' font-weight="600"' if bold else ''
        return '<text x="%d" y="%d" font-family="Inter, sans-serif" font-size="%d" fill="currentColor" text-anchor="%s"%s>%s</text>' % (x, y, size, anchor, w, s)
    def dot(x, y):
        return '<circle cx="%d" cy="%d" r="3" fill="currentColor"/>' % (x, y)
    p = ['<svg viewBox="0 0 250 190" role="img" aria-label="%s" style="max-width:250px">' % aria]
    p.append(line(rx, ry, n1[0], n1[1]))
    p.append(line(rx, ry, n2[0], n2[1]))
    p.append(line(n1[0], n1[1], lf[0][0], lf[0][1]))
    p.append(line(n1[0], n1[1], lf[1][0], lf[1][1]))
    p.append(line(n2[0], n2[1], lf[2][0], lf[2][1]))
    p.append(line(n2[0], n2[1], lf[3][0], lf[3][1]))
    p.append(dot(rx, ry))
    p.append(dot(*n1)); p.append(dot(*n2))
    for L in lf:
        p.append(dot(*L))
    # stage-1 branch labels
    p.append(txt((rx+n1[0])//2, (ry+n1[1])//2 - 3, pA))
    p.append(txt((rx+n2[0])//2, (ry+n2[1])//2 + 12, pB))
    p.append(txt(n1[0]-4, n1[1]-6, labA, anchor="middle", bold=True))
    p.append(txt(n2[0]-4, n2[1]+14, labB, anchor="middle", bold=True))
    # stage-2 branch labels
    p.append(txt((n1[0]+lf[0][0])//2, (n1[1]+lf[0][1])//2 - 3, s2[0]))
    p.append(txt((n1[0]+lf[1][0])//2, (n1[1]+lf[1][1])//2 + 11, s2[1]))
    p.append(txt((n2[0]+lf[2][0])//2, (n2[1]+lf[2][1])//2 - 3, s2[2]))
    p.append(txt((n2[0]+lf[3][0])//2, (n2[1]+lf[3][1])//2 + 11, s2[3]))
    # leaf labels
    for i, L in enumerate(lf):
        bold = i in wanted
        p.append(txt(L[0]+8, L[1]+4, leaves[i], anchor="start", bold=bold))
        if bold:
            p.append(dot(L[0], L[1]))
    p.append('</svg>')
    return "".join(p)

def chain(aria, labels, probs, result):
    """Linear chain: node -prob-> node -prob-> ... => result."""
    n = len(probs)
    xs = [16 + i * (210 // n) for i in range(n + 1)]
    y = 40
    def txt(x, yy, s, anchor="middle", bold=False, size=11):
        w = ' font-weight="600"' if bold else ''
        return '<text x="%d" y="%d" font-family="Inter, sans-serif" font-size="%d" fill="currentColor" text-anchor="%s"%s>%s</text>' % (x, yy, size, anchor, w, s)
    p = ['<svg viewBox="0 0 250 90" role="img" aria-label="%s" style="max-width:250px">' % aria]
    for i in range(n):
        p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1"/>' % (xs[i]+6, y, xs[i+1]-6, y))
        p.append(txt((xs[i]+xs[i+1])//2, y-6, probs[i]))
    for i in range(n + 1):
        p.append('<circle cx="%d" cy="%d" r="3" fill="currentColor"/>' % (xs[i], y))
        if i < len(labels):
            p.append(txt(xs[i], y+16, labels[i]))
    p.append(txt(125, 74, result, bold=True))
    p.append('</svg>')
    return "".join(p)

def balls_svg(aria, colours):
    """Draw a bag holding len(colours) balls (up to 8), colours = list of hex fills."""
    n = len(colours)
    # layout: up to 4 per row, two rows
    positions_by_n = {
        4: [(72, 72), (100, 68), (128, 72), (100, 96)],
        8: [(64, 66), (88, 62), (112, 62), (136, 66),
            (72, 92), (96, 96), (120, 96), (144, 92)],
    }
    xs = positions_by_n.get(n)
    if xs is None:
        xs = [(60 + 22 * (i % 4), 66 + 28 * (i // 4)) for i in range(n)]
    p = ['<svg viewBox="0 0 200 130" role="img" aria-label="%s" style="max-width:200px">' % aria]
    p.append('<path d="M36 40 L164 40 L152 118 L48 118 Z" fill="#fbbf24" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>')
    p.append('<line x1="52" y1="40" x2="68" y2="22" stroke="currentColor" stroke-width="1.5"/>')
    p.append('<line x1="148" y1="40" x2="132" y2="22" stroke="currentColor" stroke-width="1.5"/>')
    for i in range(n):
        p.append('<circle cx="%d" cy="%d" r="11" fill="%s" fill-opacity="0.55" stroke="currentColor" stroke-width="1"/>' % (xs[i][0], xs[i][1], colours[i]))
    p.append('</svg>')
    return "".join(p)

def bag_svg(aria, reds, greens):
    return balls_svg(aria, ["#f87171"] * reds + ["#34d399"] * greens)

# ---------- descriptions ----------
pb = pd["problem_bank"]
pb["bronze_description"] = "Single-event probability: count the favourable outcomes over the total, then write it as a fraction in its simplest form."
pb["silver_description"] = "Two-stage probability: multiply along the branches of a tree for AND, add branches for OR, and adjust the second fraction when there is no replacement."
pb["gold_description"] = "Multi-stage and conditional probability: combine several paths, handle picks without replacement, and use the total-probability rule."

# ---------- fix bronze[4] duplicate: coin (1/2) -> spinner (2/5) ----------
b = pb["bronze"]
b[4]["display"] = "A spinner has 5 equal sections. 2 of them are red. Find P(red) as a fraction."
b[4]["solutions"] = [2, 5]

# ---------- hints ----------
hints = {
 "bronze": [
  "Count the reds, then divide by the total number of balls.",
  "Even numbers on a dice are 2, 4 and 6, out of six faces.",
  "P(not win) = 1 minus P(win); turn the decimal into a fraction.",
  "Favourable over total: toffees over all the sweets.",
  "Count the red sections over the total number of sections.",
  "Add up all the balls for the total, then put greens over it.",
  "Expected number = probability × number of trials.",
  "Count how many letter A's, then divide by the total letters.",
 ],
 "silver": [
  "Multiply along the branch: P(H) then P(H) again.",
  "With replacement the second pick is identical, so multiply the two equal fractions.",
  "Without replacement the second fraction has one fewer red and one fewer in total.",
  "Independent AND means multiply the two probabilities.",
  "List the ways to get exactly two heads, each worth one eighth.",
  "OR with separate colours means add the two probabilities.",
  "P(lose) is 3/4 each spin; three losses means cubing it.",
 ],
 "gold": [
  "Two orders give one of each: red then blue, and blue then red. Add them.",
  "Three reds without replacement: reds and total both drop each pick.",
  "Add the two routes to B: through A and through not A.",
  "Easier as 1 minus P(no heads at all).",
  "Exactly one head means head-then-tail or tail-then-head; add both.",
 ],
}
for tier in ("bronze", "silver", "gold"):
    for i, h in enumerate(hints[tier]):
        pb[tier][i]["hint"] = h

# ---------- misconceptions (with expect derived by committing the error) ----------
def mc(pattern, message, expect, note):
    return {"pattern": pattern, "message": message, "expect": expect, "note": note}

miscon = {
 "bronze": [
  [mc("fav_over_unfav", "Probability is favourable over the TOTAL, not over the rest. There are 5 red out of 8 balls, so P(red) = 5/8. Writing 5/3 compares reds to blues instead.", [5, 3], "reds/blues")],
  [],
  [mc("forgot_complement", "That is P(win). The question asks P(not win) = 1 − 0.4 = 0.6 = 3/5.", [2, 5], "gave P(win)=2/5")],
  [mc("fav_over_unfav", "Put toffees over the TOTAL of 12 sweets: 7/12. 7/5 compares toffees to mints instead.", [7, 5], "toffee/mint")],
  [mc("fav_over_unfav", "Put red sections over the TOTAL of 5: 2/5. 2/3 compares red to non-red instead.", [2, 3], "red/other")],
  [mc("fav_over_unfav", "Total the balls first: 2 + 3 + 5 = 10, so P(green) = 3/10. 3/7 compares green to the others.", [3, 7], "green/others")],
  [mc("divide_not_multiply", "Expected number = probability × trials = 0.2 × 50 = 10. Dividing 50 by 0.2 gives 250, far too many.", [250], "50/0.2")],
  [mc("wrong_count", "MATHEMATICS has 11 letters and exactly 2 of them are A, so P(A) = 2/11.", [1, 11], "counted one A")],
 ],
 "silver": [
  [mc("one_flip_only", "Two heads needs BOTH flips: 1/2 × 1/2 = 1/4. 1/2 is the chance of just one head.", [1, 2], "single flip")],
  [mc("without_replacement", "The ball is replaced, so the second pick is still 4/10: 4/10 × 4/10 = 4/25. Dropping the total gives 2/15, the without-replacement answer.", [2, 15], "used 4/10*3/9")],
  [mc("with_replacement", "Without replacement the second red is 4/7, not 5/8: 5/8 × 4/7 = 5/14. Keeping 5/8 twice gives 25/64.", [25, 64], "used 5/8*5/8")],
  [mc("added_not_multiplied", "Independent AND means multiply: 0.3 × 0.5 = 0.15 = 3/20. Adding gives 0.8 = 4/5.", [4, 5], "0.3+0.5")],
  [mc("one_branch_only", "There are three ways to get exactly two heads (HHT, HTH, THH), each 1/8, so 3/8. One branch alone is only 1/8.", [1, 8], "single arrangement")],
  [mc("multiplied_not_added", "Separate colours on one pick is OR, so add: 4/10 + 3/10 = 7/10. Multiplying gives 12/100 = 3/25.", [3, 25], "P(red)*P(green)")],
  [mc("forgot_to_cube", "Three spins means cubing: (3/4)³ = 27/64. 3/4 is only one spin.", [3, 4], "one spin")],
 ],
 "gold": [
  [mc("one_order_only", "One of each happens two ways: red-blue AND blue-red, each 35/132. Add them: 70/132 = 35/66. One order alone is 35/132.", [35, 132], "RB only")],
  [mc("with_replacement", "The reds drop each pick: 8/12 × 7/11 × 6/10 = 14/55. Treating it as 8/12 cubed gives 8/27.", [8, 27], "(2/3)^3")],
  [mc("one_path_only", "B can arrive two ways. Add them: 0.5×0.6 + 0.2×0.4 = 0.38 = 19/50. The A path alone is 0.30 = 3/10.", [3, 10], "P(B|A)P(A) only")],
  [mc("counted_none_case", "At least one head = 1 − P(no heads) = 1 − 1/16 = 15/16. 1/16 is the chance of NO heads.", [1, 16], "P(no heads)")],
  [mc("one_order_only", "Exactly one head is HT OR TH: 2/9 + 2/9 = 4/9. One order alone is 2/9.", [2, 9], "HT only")],
 ],
}
for tier in ("bronze", "silver", "gold"):
    for i, m in enumerate(miscon[tier]):
        pb[tier][i]["misconceptions"] = m

# ---------- guided_steps ----------
def say(s): return {"say": s}
def box(pre, ans, hint, post="", done=None, phase=None, sy=None):
    d = {"pre": pre, "post": post, "answer": ans, "hint": hint}
    if done: d["done"] = done
    if phase: d["phase"] = phase
    if sy: d["say"] = sy
    return d

# BRONZE walks
b[0]["guided_steps"] = [
 say("Probability is favourable outcomes over the total. Start by counting."),
 box("How many red balls? ", 5, "The bag has 5 red."),
 box("Total number of balls: 5 + 3 = ", 8, "Add reds and blues."),
 {"say": "So P(red) = favourable over total. Now write the fraction.", "phase": "substitute",
  "pre": "P(red) numerator (the reds) = ", "post": "", "answer": 5, "hint": "The number of reds you counted."},
 box("P(red) denominator (the total) = ", 8, "The total you found.", phase="substitute"),
 box("Check: 5 out of 8, and 5/8 is already simplest. Type the numerator once more: ", 5,
     "It stays 5.", done="P(red) = 5/8.", phase="substitute"),
]
b[1]["guided_steps"] = [
 say("A fair dice has faces 1, 2, 3, 4, 5, 6. Count the even ones."),
 box("How many even faces (2, 4, 6)? ", 3, "Count 2, 4 and 6."),
 box("Total faces = ", 6, "A dice has six faces."),
 {"say": "So P(even) = 3/6. That simplifies: divide top and bottom by 3.", "phase": "substitute",
  "pre": "3 ÷ 3 = ", "post": "", "answer": 1, "hint": "3 divided by 3."},
 box("6 ÷ 3 = ", 2, "6 divided by 3.", done="P(even) = 1/2.", phase="substitute"),
]
b[2]["guided_steps"] = [
 say("P(not win) means everything except winning: 1 − P(win)."),
 box("1 − 0.4 = ", 0.6, "One take away nought point four."),
 {"say": "Now turn 0.6 into a fraction. 0.6 = 6/10, then simplify by 2.", "phase": "substitute",
  "pre": "6 ÷ 2 = ", "post": "", "answer": 3, "hint": "6 divided by 2."},
 box("10 ÷ 2 = ", 5, "10 divided by 2.", done="P(not win) = 3/5.", phase="substitute"),
]
b[3]["guided_steps"] = [
 say("Favourable over total. The toffees are what we want."),
 box("How many toffees? ", 7, "Seven toffees."),
 box("Total sweets = ", 12, "Twelve sweets in all."),
 {"say": "So P(toffee) = toffees over total.", "phase": "substitute",
  "pre": "Numerator = ", "post": "", "answer": 7, "hint": "The toffees."},
 box("Denominator = ", 12, "The total.", done="P(toffee) = 7/12, already simplest.", phase="substitute"),
]
b[4]["guided_steps"] = [
 say("Favourable over total. Each equal section is one outcome."),
 box("How many red sections? ", 2, "Two are red."),
 box("Total sections = ", 5, "Five equal sections."),
 {"say": "So P(red) = reds over total.", "phase": "substitute",
  "pre": "Numerator = ", "post": "", "answer": 2, "hint": "The red sections."},
 box("Denominator = ", 5, "The total sections.", done="P(red) = 2/5, already simplest.", phase="substitute"),
]
b[5]["guided_steps"] = [
 say("Total everything first, then put greens over the total."),
 box("Total balls: 2 + 3 + 5 = ", 10, "Add all three colours."),
 box("How many green? ", 3, "Three green."),
 {"say": "So P(green) = greens over total.", "phase": "substitute",
  "pre": "Numerator = ", "post": "", "answer": 3, "hint": "The greens."},
 box("Denominator = ", 10, "The total.", done="P(green) = 3/10.", phase="substitute"),
]
b[6]["guided_steps"] = [
 say("Expected number = probability × number of trials."),
 box("The probability of rain each day = ", 0.2, "Given as 0.2."),
 box("Number of days (trials) = ", 50, "The event is repeated 50 times."),
 {"say": "Now multiply them together.", "phase": "substitute",
  "pre": "0.2 × 50 = ", "post": "", "answer": 10, "hint": "Two tenths of fifty."},
 box("Check: 10 rainy days out of 50, and 10 ÷ 50 = ", 0.2,
     "Divide to get back the probability.", done="Expected = 10 rainy days.", phase="substitute"),
]
b[7]["guided_steps"] = [
 say("Spell out MATHEMATICS and count the letters."),
 box("How many letters in MATHEMATICS? ", 11, "M-A-T-H-E-M-A-T-I-C-S."),
 box("How many are the letter A? ", 2, "A appears twice."),
 {"say": "So P(A) = A's over total letters.", "phase": "substitute",
  "pre": "Numerator = ", "post": "", "answer": 2, "hint": "The two A's."},
 box("Denominator = ", 11, "The total letters.", done="P(A) = 2/11.", phase="substitute"),
]

# SILVER walks
s = pb["silver"]
s[0]["guided_steps"] = [
 say("Two flips: draw two branches each time. P(H) = 1/2 every flip."),
 box("P(H) on flip 1, numerator = ", 1, "One head out of two."),
 box("P(H) on flip 1, denominator = ", 2, "Two equally likely faces."),
 say("Two heads needs H then H, so multiply along that branch."),
 {"say": "Multiply the tops.", "phase": "substitute",
  "pre": "1 × 1 = ", "post": "", "answer": 1, "hint": "Top times top."},
 box("Multiply the bottoms: 2 × 2 = ", 4, "Bottom times bottom.",
     done="P(two heads) = 1/4.", phase="substitute"),
]
s[1]["guided_steps"] = [
 say("With replacement the bag is the same each time. P(blue) = 4/10 both picks."),
 box("P(blue) numerator = ", 4, "Four blue."),
 box("P(blue) denominator = ", 10, "Ten balls in total."),
 box("Multiply tops: 4 × 4 = ", 16, "Top times top."),
 {"say": "Multiply bottoms, then simplify 16/100 by dividing by 4.", "phase": "substitute",
  "pre": "10 × 10 = ", "post": "", "answer": 100, "hint": "Bottom times bottom."},
 box("16 ÷ 4 = ", 4, "Simplify the top.", phase="substitute"),
 box("100 ÷ 4 = ", 25, "Simplify the bottom.", done="P(both blue) = 4/25.", phase="substitute"),
]
s[2]["guided_steps"] = [
 say("Without replacement the second pick has one fewer red and one fewer in total."),
 box("First pick P(red) numerator = ", 5, "Five red at the start."),
 box("First pick P(red) denominator = ", 8, "Eight balls at the start."),
 box("After one red is gone, reds left = ", 4, "One red removed from five."),
 box("Total left = ", 7, "One ball removed from eight."),
 {"say": "So P(both red) = 5/8 × 4/7 = 20/56. Simplify by dividing by 4.", "phase": "substitute",
  "pre": "20 ÷ 4 = ", "post": "", "answer": 5, "hint": "Simplify the top."},
 box("56 ÷ 4 = ", 14, "Simplify the bottom.", done="P(both red) = 5/14.", phase="substitute"),
]
s[3]["guided_steps"] = [
 say("Independent AND means multiply the probabilities."),
 box("0.3 × 0.5 = ", 0.15, "Three tenths of a half."),
 {"say": "Now 0.15 = 15/100. Simplify by dividing by 5.", "phase": "substitute",
  "pre": "15 ÷ 5 = ", "post": "", "answer": 3, "hint": "Simplify the top."},
 box("100 ÷ 5 = ", 20, "Simplify the bottom.", done="P(A and B) = 3/20.", phase="substitute"),
]
s[4]["guided_steps"] = [
 say("Three flips give 2 × 2 × 2 outcomes. List the ones with exactly two heads."),
 box("Total outcomes: 2 × 2 × 2 = ", 8, "Two choices, three times."),
 box("Ways to get exactly two heads (HHT, HTH, THH) = ", 3, "Count the arrangements."),
 {"say": "So P = favourable over total.", "phase": "substitute",
  "pre": "Numerator = ", "post": "", "answer": 3, "hint": "The three arrangements."},
 box("Denominator = ", 8, "The eight outcomes.", done="P(exactly two heads) = 3/8.", phase="substitute"),
]
s[5]["guided_steps"] = [
 say("One pick, two acceptable colours: this is OR, so add the probabilities."),
 box("Total balls: 4 + 3 + 3 = ", 10, "Add all colours."),
 box("Reds = 4, greens = 3. Reds plus greens = ", 7, "Add the two wanted colours."),
 {"say": "So P(red or green) = 7 over the total.", "phase": "substitute",
  "pre": "Numerator = ", "post": "", "answer": 7, "hint": "Reds plus greens."},
 box("Denominator = ", 10, "The total.", done="P(red or green) = 7/10.", phase="substitute"),
]
s[6]["guided_steps"] = [
 say("No wins in three spins means losing every spin. P(lose) = 1 − 1/4."),
 box("P(lose) numerator (1 − 1/4 = 3/4) = ", 3, "Three quarters lose."),
 box("P(lose) denominator = ", 4, "Out of four."),
 say("Three losses in a row: cube the fraction."),
 {"say": "Cube the top.", "phase": "substitute",
  "pre": "3 × 3 × 3 = ", "post": "", "answer": 27, "hint": "3 cubed."},
 box("Cube the bottom: 4 × 4 × 4 = ", 64, "4 cubed.",
     done="P(no wins) = 27/64.", phase="substitute"),
]

# GOLD walks
g = pb["gold"]
g[0]["guided_steps"] = [
 say("One of each can happen two ways: red then blue, or blue then red. Without replacement."),
 box("P(red-blue) top: 7 × 5 = ", 35, "Reds times blues along the path."),
 box("P(red-blue) bottom: 12 × 11 = ", 132, "Twelve then eleven."),
 say("P(blue-red) works out the same, 35/132. Two paths, so add them."),
 {"say": "Add the tops.", "phase": "substitute",
  "pre": "35 + 35 = ", "post": "", "answer": 70, "hint": "The two equal paths."},
 box("Simplify 70/132 by 2, top: 70 ÷ 2 = ", 35, "Halve the top.", phase="substitute"),
 box("Bottom: 132 ÷ 2 = ", 66, "Halve the bottom.",
     done="P(one of each) = 35/66.", phase="substitute"),
]
g[1]["guided_steps"] = [
 say("Three reds without replacement: reds and total drop each pick."),
 box("Pick 1 P(red) = 8 over ", 12, "Eight reds out of twelve."),
 box("Pick 2: reds now 7, total now ", 11, "One red and one ball removed."),
 box("Pick 3: reds now 6, total now ", 10, "Another of each removed."),
 box("Multiply tops: 8 × 7 × 6 = ", 336, "All three numerators."),
 {"say": "Multiply bottoms, then simplify 336/1320 (divide by 24).", "phase": "substitute",
  "pre": "12 × 11 × 10 = ", "post": "", "answer": 1320, "hint": "All three denominators."},
 box("336 ÷ 24 = ", 14, "Simplify the top.", phase="substitute"),
 box("1320 ÷ 24 = ", 55, "Simplify the bottom.", done="P(all red) = 14/55.", phase="substitute"),
]
g[2]["guided_steps"] = [
 say("B can be reached two ways: through A, or through not A. Total-probability rule."),
 box("Path through A: 0.6 × 0.5 = ", 0.3, "P(A) times P(B given A)."),
 box("P(not A) = 1 − 0.6 = ", 0.4, "The rest."),
 box("Path through not A: 0.4 × 0.2 = ", 0.08, "P(not A) times P(B given not A)."),
 {"say": "Add the paths: 0.30 + 0.08 = 0.38 = 38/100. Simplify by 2.", "phase": "substitute",
  "pre": "38 ÷ 2 = ", "post": "", "answer": 19, "hint": "Halve the top."},
 box("100 ÷ 2 = ", 50, "Halve the bottom.", done="P(B) = 19/50.", phase="substitute"),
]
g[3]["guided_steps"] = [
 say("At least one head is easiest as 1 − P(no heads at all)."),
 box("P(no heads) bottom: 2 × 2 × 2 × 2 = ", 16, "Two to the power four."),
 box("P(no heads) top: 1 × 1 × 1 × 1 = ", 1, "One tail each flip."),
 say("So P(no heads) = 1/16, and P(at least one) = 16/16 − 1/16."),
 {"say": "Subtract the tops.", "phase": "substitute",
  "pre": "16 − 1 = ", "post": "", "answer": 15, "hint": "One whole minus one sixteenth."},
 box("Denominator stays = ", 16, "Same bottom.", done="P(at least one head) = 15/16.", phase="substitute"),
]
g[4]["guided_steps"] = [
 say("Biased coin: P(H) = 2/3, so P(T) = 1/3. Exactly one head is HT or TH."),
 box("P(HT) top: 2 × 1 = ", 2, "P(H) top times P(T) top."),
 box("P(HT) bottom: 3 × 3 = ", 9, "Three times three."),
 say("P(TH) is the same, 2/9. Two paths, so add."),
 {"say": "Add the tops.", "phase": "substitute",
  "pre": "2 + 2 = ", "post": "", "answer": 4, "hint": "The two equal paths."},
 box("Denominator stays = ", 9, "Same bottom.", done="P(exactly one head) = 4/9.", phase="substitute"),
]

# ---------- add SVG figures to displays ----------
def prepend(prob, svg):
    prob["display"] = svg + "<br>" + prob["display"]

prepend(s[0], tree2("Probability tree for two coin flips", "H", "1/2", "T", "1/2",
        ["1/2", "1/2", "1/2", "1/2"], ["HH", "HT", "TH", "TT"], {0}))
prepend(s[1], tree2("Probability tree for two picks with replacement", "R", "6/10", "B", "4/10",
        ["6/10", "4/10", "6/10", "4/10"], ["RR", "RB", "BR", "BB"], {3}))
prepend(s[2], tree2("Probability tree for two picks without replacement", "R", "5/8", "B", "3/8",
        ["4/7", "3/7", "5/7", "2/7"], ["RR", "RB", "BR", "BB"], {0}))
prepend(s[6], chain("Three losing spins", ["", "L", "L", "L"], ["3/4", "3/4", "3/4"], "27/64"))
prepend(g[0], tree2("Probability tree for one of each colour", "R", "7/12", "B", "5/12",
        ["6/11", "5/11", "7/11", "4/11"], ["RR", "RB", "BR", "BB"], {1, 2}))
prepend(g[1], chain("Three reds without replacement", ["", "R", "R", "R"], ["8/12", "7/11", "6/10"], "14/55"))
prepend(g[2], tree2("Tree for total probability of B", "A", "0.6", "A'", "0.4",
        ["0.5", "0.5", "0.2", "0.8"], ["B", "B'", "B", "B'"], {0, 2}))
prepend(g[4], tree2("Probability tree for a biased coin flipped twice", "H", "2/3", "T", "1/3",
        ["2/3", "1/3", "2/3", "1/3"], ["HH", "HT", "TH", "TT"], {1, 2}))

# ---------- tier_guides ----------
pd["tier_guides"] = {
 "bronze": {
  "title": "Bronze: single-event probability",
  "steps": [
   "Count the <strong>favourable</strong> outcomes (the ones you want).",
   "Count the <strong>total</strong> number of equally likely outcomes.",
   "Write favourable over total, then simplify the fraction.",
   "For 'not', use \\(P(\\text{not }A) = 1 - P(A)\\).",
  ],
  "example": {
   "question": "A bag has 4 red and 6 green. Find P(red).",
   "steps": [
    {"label": "Favourable", "content": "4 red"},
    {"label": "Total", "content": "4 + 6 = 10"},
    {"label": "Check", "content": "4 out of 10, simplify by 2"},
    {"label": "Answer", "content": "P(red) = 4/10 = 2/5", "isAnswer": True, "is_answer": True},
   ],
  },
 },
 "silver": {
  "title": "Silver: two-stage probability",
  "steps": [
   "Draw a tree: one set of branches for each stage.",
   "Multiply along a branch for <strong>AND</strong> (both happen).",
   "Add branch results for <strong>OR</strong> (either happens).",
   "<strong>Without replacement</strong>: drop the picked colour and the total by one on the second pick.",
  ],
  "example": {
   "question": "A bag has 3 red, 2 blue. Two picked without replacement. Find P(both red).",
   "steps": [
    {"label": "First pick", "content": "P(red) = 3/5"},
    {"label": "Second pick", "content": "reds and total drop: 2/4"},
    {"label": "Check", "content": "3/5 × 2/4 = 6/20"},
    {"label": "Answer", "content": "6/20 = 3/10", "isAnswer": True, "is_answer": True},
   ],
  },
 },
 "gold": {
  "title": "Gold: multi-stage and conditional",
  "steps": [
   "Split the event into every path that works, e.g. red-blue AND blue-red.",
   "Multiply along each path, then <strong>add</strong> the paths.",
   "Conditional: \\(P(B) = P(B|A)P(A) + P(B|A')P(A')\\).",
   "'At least one' is quickest as \\(1 - P(\\text{none})\\).",
  ],
  "example": {
   "question": "P(H) = 2/3. Two flips. Find P(exactly one head).",
   "steps": [
    {"label": "HT", "content": "2/3 × 1/3 = 2/9"},
    {"label": "TH", "content": "1/3 × 2/3 = 2/9"},
    {"label": "Check", "content": "add the paths: 2/9 + 2/9"},
    {"label": "Answer", "content": "4/9", "isAnswer": True, "is_answer": True},
   ],
  },
 },
}

# ---------- guided (opener + teach) ----------
pd["guided"] = {
 "opener": {
  "steps": [
   {"say": "Picture this bag. You can see every sweet inside it.",
    "display": bag_svg("A bag holding 3 red sweets and 1 green sweet", 3, 1)},
   {"pre": "How many sweets are red? ", "post": "", "answer": 3,
    "hint": "Count the red circles."},
   {"pre": "How many sweets are there altogether? ", "post": "", "answer": 4,
    "hint": "Count every circle."},
   {"say": "Reach in without looking and pick one. You just worked out the chance of red: 3 red out of 4 sweets, written \\(\\tfrac{3}{4}\\). That is all probability is: <strong>favourable over total</strong>."},
  ],
 },
 "teach": {
  "bronze": {
   "display": balls_svg("A bag with 3 red and 5 yellow counters", ["#f87171"] * 3 + ["#fbbf24"] * 5)
              + "<br>A bag has 3 red and 5 yellow counters. Find P(yellow) as a fraction.",
   "steps": [
    say("Favourable over total. The yellows are what we want."),
    box("How many yellow counters? ", 5, "Five yellow."),
    box("Total counters: 3 + 5 = ", 8, "Add red and yellow."),
    box("P(yellow) numerator = ", 5, "The yellows."),
    box("P(yellow) denominator = ", 8, "The total.",
        done="P(yellow) = 5/8. Favourable over total, every time."),
   ],
  },
  "silver": {
   "display": tree2("Tree for two picks with replacement from 2 red and 3 blue", "R", "2/5", "B", "3/5",
            ["2/5", "3/5", "2/5", "3/5"], ["RR", "RB", "BR", "BB"], {0}) +
            "<br>A bag has 2 red and 3 blue. One is taken, its colour noted, then it is put back and another is taken. Find P(both red).",
   "steps": [
    say("Two stages, so two sets of branches. Replaced, so P(red) = 2/5 both times."),
    box("First pick P(red), numerator = ", 2, "Two red."),
    box("First pick denominator = ", 5, "Five balls."),
    box("Multiply along the red-red branch, top: 2 × 2 = ", 4, "Top times top."),
    box("Bottom: 5 × 5 = ", 25, "Bottom times bottom.",
        done="P(both red) = 4/25. Multiply ALONG a branch for AND."),
   ],
  },
  "gold": {
   "display": tree2("Tree for two picks without replacement from 3 red and 2 blue", "R", "3/5", "B", "2/5",
            ["2/4", "2/4", "3/4", "1/4"], ["RR", "RB", "BR", "BB"], {0}) +
            "<br>A bag has 3 red and 2 blue. Two are taken without replacement. Find P(both red).",
   "steps": [
    say("Without replacement, the second pick changes. Start with the first."),
    box("First pick P(red), numerator = ", 3, "Three red of five."),
    box("First pick denominator = ", 5, "Five balls."),
    box("A red is gone. Second pick reds left = ", 2, "One red removed."),
    box("Second pick total left = ", 4, "One ball removed."),
    box("Multiply: 3/5 × 2/4 = 6/20, simplify by 2. Numerator = ", 3, "6 ÷ 2.",
        done="P(both red) = 3/10. The denominator dropped: that is the new move."),
   ],
  },
 },
}

# ---------- method_card: keep, ensure budget ----------
mc0 = pd.get("method_card") or {}
def wc(sv):
    return len([w for w in (sv or "").replace("\\(", " ").replace("\\)", " ").split() if w])
print("method_card content words:", wc(mc0.get("content")), "steps:", len(mc0.get("steps") or []))

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote", OUT)
