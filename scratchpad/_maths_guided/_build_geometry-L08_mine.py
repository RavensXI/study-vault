# -*- coding: utf-8 -*-
import json, io

MINUS = "−"  # unicode minus for student-facing plain text

def box(pre, answer, hint, say=None, post="", done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def say(text):
    return {"say": text}

def mis(pattern, message, expect, note=None):
    d = {"pattern": pattern, "check": pattern, "message": message, "expect": expect}
    if note is not None: d["note"] = note
    return d

# ---------------- method_card (slim) ----------------
method_card = {
    "title": "Vectors",
    "steps": [
        "Add or subtract column vectors row by row; scalar multiply every row.",
        "A journey between points: \\(\\vec{AB} = \\mathbf{b} - \\mathbf{a}\\) (end minus start).",
        "Length: \\(|\\binom{x}{y}| = \\sqrt{x^2 + y^2}\\).",
        "Parallel means one vector is a scalar multiple of the other."
    ],
    "content": "<p>A <strong>vector</strong> has size and direction, written \\(\\binom{x}{y}\\): x across, y up.</p><p><strong>Add</strong> and <strong>subtract</strong> row by row; <strong>scalar multiply</strong> scales every row. A <strong>position vector</strong> runs from O to a point, so \\(\\vec{AB} = \\mathbf{b} - \\mathbf{a}\\).</p><p>To divide AB in ratio \\(m:n\\), take \\(\\tfrac{m}{m+n}\\) of \\(\\vec{AB}\\) and add it to \\(\\mathbf{a}\\).</p>",
    "example": "<p><strong>Find \\(\\vec{AB}\\)</strong> when \\(\\vec{OA} = \\binom{2}{1}\\), \\(\\vec{OB} = \\binom{6}{4}\\).</p><p>\\(\\vec{AB} = \\mathbf{b} - \\mathbf{a} = \\binom{4}{3}\\), and \\(|\\vec{AB}| = \\sqrt{16 + 9} = 5\\).</p>"
}

# ---------------- topic_links (unchanged) ----------------
topic_links = {"prerequisites": [{"slug": "algebra/1", "title": "Simplifying Expressions"}]}

# ================= BRONZE =================
bronze = []

# B0: (4,1)+(2,3) top = 6
bronze.append({
    "display": "\\(\\binom{4}{1} + \\binom{2}{3}\\) = ? Give the top component.",
    "solutions": [6], "calculator": False, "input_type": "single_value",
    "hint": "Add the top numbers of the two vectors.",
    "misconceptions": [mis("read_wrong_row",
        "The top component adds the top numbers: 4 + 2 = 6. The value 4 is the bottom component (1 + 3), so you read the wrong row.",
        4, note="4 = bottom component")],
    "guided_steps": [
        say("Adding column vectors means adding matching rows. Line them up and start with the bottom."),
        box("Bottom row: 1 + 3 = ", 4, "Add the bottom numbers: 1 + 3."),
        box("Now the row the question wants, the top: 4 + 2 = ", 6, "Add the top numbers: 4 + 2.", phase="substitute"),
        box("So the sum is (6, 4). The top component asked for is ", 6, "Read the top of (6, 4).", phase="substitute", done="Top component is 6."),
    ]})

# B1: (5,-2)+(-3,6) bottom = 4
bronze.append({
    "display": "\\(\\binom{5}{-2} + \\binom{-3}{6}\\). Give the bottom component.",
    "solutions": [4], "calculator": False, "input_type": "single_value",
    "hint": "Add the bottom numbers, keeping the minus on the " + MINUS + "2.",
    "misconceptions": [mis("dropped_negative",
        "Keep the minus on the " + MINUS + "2: (" + MINUS + "2) + 6 = 4. Treating it as +2 gives 2 + 6 = 8.",
        8, note="drop sign: 2+6=8")],
    "guided_steps": [
        say("Add the matching rows, keeping every sign."),
        box("Top row: 5 + (" + MINUS + "3) = ", 2, "Add the tops with signs: 5 + (" + MINUS + "3)."),
        box("Bottom row: (" + MINUS + "2) + 6 = ", 4, "Add the bottoms, keep the minus: (" + MINUS + "2) + 6.", phase="substitute"),
        box("So the sum is (2, 4). The bottom component asked for is ", 4, "Read the bottom of (2, 4).", phase="substitute", done="Bottom component is 4."),
    ]})

# B2: 3 x (3,-1) top = 9  (CHANGED from (2,-1) to remove duplicate with B0)
bronze.append({
    "display": "\\(3 \\times \\binom{3}{-1}\\). Give the top component.",
    "solutions": [9], "calculator": False, "input_type": "single_value",
    "hint": "Multiply the top number by 3.",
    "misconceptions": [mis("added_not_multiplied",
        "Scalar multiply each part: 3 × 3 = 9. Adding (3 + 3 = 6) instead of multiplying is the slip.",
        6, note="3+3=6")],
    "guided_steps": [
        say("A scalar multiplies every row of the vector."),
        box("Bottom row: 3 × (" + MINUS + "1) = ", -3, "Multiply the bottom by 3, keep the minus."),
        box("Top row: 3 × 3 = ", 9, "Multiply the top by 3: 3 × 3.", phase="substitute"),
        box("So 3 × (3, " + MINUS + "1) = (9, " + MINUS + "3). The top component is ", 9, "Read the top of (9, " + MINUS + "3).", phase="substitute", done="Top component is 9."),
    ]})

# B3: (7,3)-(4,1) top = 3
bronze.append({
    "display": "\\(\\binom{7}{3} - \\binom{4}{1}\\). Give the top component.",
    "solutions": [3], "calculator": False, "input_type": "single_value",
    "hint": "Subtract the top numbers in the order given.",
    "misconceptions": [mis("reversed_subtraction",
        "Subtract in the order given: 7 " + MINUS + " 4 = 3. Reversing it (4 " + MINUS + " 7) gives " + MINUS + "3.",
        -3, note="reverse: 4-7=-3")],
    "guided_steps": [
        say("Subtract the matching rows, top from top and bottom from bottom."),
        box("Bottom row: 3 " + MINUS + " 1 = ", 2, "Subtract the bottoms: 3 " + MINUS + " 1."),
        box("Top row: 7 " + MINUS + " 4 = ", 3, "Subtract the tops: 7 " + MINUS + " 4.", phase="substitute"),
        box("So the difference is (3, 2). The top component asked for is ", 3, "Read the top of (3, 2).", phase="substitute", done="Top component is 3."),
    ]})

# B4: OA=(3,5), OB=(10,2) top of AB = 7  (CHANGED OB from (7,2) to remove dup with B1)
bronze.append({
    "display": "If \\(\\vec{OA} = \\binom{3}{5}\\) and \\(\\vec{OB} = \\binom{10}{2}\\), find the top component of \\(\\vec{AB}\\).",
    "solutions": [7], "calculator": False, "input_type": "single_value",
    "hint": "AB = b " + MINUS + " a, so subtract the top of OA from the top of OB.",
    "misconceptions": [mis("reversed_direction",
        "\\(\\vec{AB} = \\mathbf{b} - \\mathbf{a}\\), so the top is 10 " + MINUS + " 3 = 7. Doing a " + MINUS + " b gives " + MINUS + "7, which is BA (the reverse direction).",
        -7, note="a-b: 3-10=-7")],
    "guided_steps": [
        say("\\(\\vec{AB}\\) is the journey from A to B, which is \\(\\mathbf{b} - \\mathbf{a}\\) (end minus start)."),
        box("Bottom of AB: 2 " + MINUS + " 5 = ", -3, "Bottom: 2 " + MINUS + " 5, keep the minus."),
        box("Top of AB: 10 " + MINUS + " 3 = ", 7, "Top: 10 " + MINUS + " 3.", phase="substitute"),
        box("So \\(\\vec{AB}\\) = (7, " + MINUS + "3). The top component is ", 7, "Read the top of (7, " + MINUS + "3).", phase="substitute", done="Top component of AB is 7."),
    ]})

# B5: |(3,4)| = 5
bronze.append({
    "display": "Find \\(|\\binom{3}{4}|\\) (the magnitude).",
    "solutions": [5], "calculator": False, "input_type": "single_value",
    "hint": "Square each number, add them, then take the square root.",
    "misconceptions": [mis("skipped_squaring",
        "Square first: \\(\\sqrt{3^2 + 4^2} = \\sqrt{25} = 5\\). Just adding 3 + 4 = 7 skips the squaring.",
        7, note="3+4=7")],
    "guided_steps": [
        say("Magnitude is Pythagoras on the two components: square, add, square root."),
        box("Square the top: 3 × 3 = ", 9, "Three squared."),
        box("Square the bottom: 4 × 4 = ", 16, "Four squared."),
        box("Add the squares: 9 + 16 = ", 25, "Add the two squares.", phase="substitute"),
        box("Square root the total: √25 = ", 5, "The square root of 25.", phase="substitute", done="√25 = 5, a whole number (a 3-4-5 triangle), so it is right."),
    ]})

# B6: 2a+6a coeff = 8  (CHANGED from 3a to remove dup with B5)
bronze.append({
    "display": "\\(2\\mathbf{a} + 6\\mathbf{a} = ?\\) (in terms of \\(\\mathbf{a}\\)). What is the coefficient?",
    "solutions": [8], "calculator": False, "input_type": "single_value",
    "hint": "Add the number of a's together.",
    "misconceptions": [mis("multiplied_coefficients",
        "Add like terms: 2 + 6 = 8, so \\(8\\mathbf{a}\\). Multiplying (2 × 6 = 12) is the slip.",
        12, note="2x6=12")],
    "guided_steps": [
        say("\\(2\\mathbf{a}\\) and \\(6\\mathbf{a}\\) point the same way, so you just add how many a's there are."),
        box("Count the first: 2a has this many a's: ", 2, "The number in front of a in 2a."),
        box("Add the counts: 2 + 6 = ", 8, "Add the number of a's: 2 + 6.", phase="substitute"),
        box("So \\(2\\mathbf{a} + 6\\mathbf{a} = 8\\mathbf{a}\\). The coefficient (number in front) is ", 8, "Read the number in front of a.", phase="substitute", done="8a, coefficient 8."),
    ]})

# B7: (-1,4)+(1,-4) top = 0
bronze.append({
    "display": "\\(\\binom{-1}{4} + \\binom{1}{-4}\\). Give the top component.",
    "solutions": [0], "calculator": False, "input_type": "single_value",
    "hint": "Add the top numbers with their signs.",
    "misconceptions": [mis("ignored_signs",
        "Add the top numbers with their signs: (" + MINUS + "1) + 1 = 0. Ignoring the minus signs gives 1 + 1 = 2.",
        2, note="ignore signs: 1+1=2")],
    "guided_steps": [
        say("These two vectors point in opposite directions. Add the matching rows with their signs."),
        box("Bottom row: 4 + (" + MINUS + "4) = ", 0, "Add the bottoms: 4 + (" + MINUS + "4)."),
        box("Top row: (" + MINUS + "1) + 1 = ", 0, "Add the tops with signs: (" + MINUS + "1) + 1.", phase="substitute"),
        box("So the sum is (0, 0). The top component is ", 0, "Read the top of (0, 0).", phase="substitute", done="Both components are 0: opposite vectors cancel."),
    ]})

bronze_description = "Add, subtract, scale and measure column vectors, one component at a time."

# ================= SILVER =================
silver = []

# S0: OA=(2,3), OB=(8,-1), |AB| to 1dp = 7.2 (calculator)
silver.append({
    "display": "\\(\\vec{OA} = \\binom{2}{3}\\), \\(\\vec{OB} = \\binom{8}{-1}\\). Find \\(|\\vec{AB}|\\) to 1 d.p.",
    "solutions": [7.2], "calculator": True, "input_type": "single_value",
    "hint": "Find AB = b " + MINUS + " a first, then use Pythagoras on its components.",
    "misconceptions": [mis("subtracted_under_root",
        "Square each component and add: \\(\\sqrt{6^2 + (-4)^2} = \\sqrt{52} \\approx 7.2\\). Treating (" + MINUS + "4) squared as " + MINUS + "16 gives \\(\\sqrt{36 - 16} = \\sqrt{20} \\approx 4.5\\).",
        4.5, note="sqrt(36-16)=4.47->4.5")],
    "guided_steps": [
        say("First find \\(\\vec{AB} = \\mathbf{b} - \\mathbf{a}\\), then its length by Pythagoras."),
        box("AB top: 8 " + MINUS + " 2 = ", 6, "AB = b " + MINUS + " a: 8 " + MINUS + " 2."),
        box("AB bottom: (" + MINUS + "1) " + MINUS + " 3 = ", -4, "Bottom: (" + MINUS + "1) " + MINUS + " 3, keep the minus."),
        box("Square and add: 36 + 16 = ", 52, "Square each of 6 and " + MINUS + "4, then add: 36 + 16.", phase="substitute"),
        box("Square root, to 1 d.p.: √52 = ", 7.2, "Square root 52 and round to 1 decimal place.", phase="substitute", done="√52 ≈ 7.2, a little more than 7 (=√49), which fits."),
    ]})

# S1: p=(3,6) parallel top 1, bottom = 2
silver.append({
    "display": "If \\(\\mathbf{p} = \\binom{3}{6}\\), write a vector parallel to \\(\\mathbf{p}\\) with top component equal to 1. Give the bottom component.",
    "solutions": [2], "calculator": False, "input_type": "single_value",
    "hint": "Scale the whole vector by 1/3 so the top becomes 1.",
    "misconceptions": [mis("scaled_top_only",
        "Scale the whole vector by 1/3: \\(\\tfrac{1}{3}\\binom{3}{6} = \\binom{1}{2}\\), so the bottom is 2. Leaving the bottom as 6 forgets to scale it as well.",
        6, note="unscaled bottom stays 6")],
    "guided_steps": [
        say("A parallel vector is the same vector scaled. To make the top 1, divide everything by 3."),
        box("New top: 3 ÷ 3 = ", 1, "3 divided by 3."),
        box("Do the same to the bottom: 6 ÷ 3 = ", 2, "Scale the bottom by the same 1/3: 6 ÷ 3.", phase="substitute"),
        box("So the parallel vector is (1, 2). Check it is parallel: 3 × 2 should give the original bottom 6, so 3 × 2 = ", 6, "Multiply the new bottom 2 by 3.", phase="substitute", done="3 × (1, 2) = (3, 6) = p, so (1, 2) is parallel. Bottom component is 2."),
    ]})

# S2: OA=5a, OB=3b, BA coeff a = 5  (CHANGED from 2a to remove dup)
silver.append({
    "display": "\\(\\vec{OA} = 5\\mathbf{a}\\), \\(\\vec{OB} = 3\\mathbf{b}\\). Find \\(\\vec{BA}\\) in terms of \\(\\mathbf{a}\\) and \\(\\mathbf{b}\\). What is the coefficient of \\(\\mathbf{a}\\)?",
    "solutions": [5], "calculator": False, "input_type": "single_value",
    "hint": "BA = OA " + MINUS + " OB, then read the number in front of a.",
    "misconceptions": [mis("reversed_direction",
        "\\(\\vec{BA} = \\vec{OA} - \\vec{OB} = 5\\mathbf{a} - 3\\mathbf{b}\\), so the coefficient of a is 5. Doing \\(\\vec{OB} - \\vec{OA}\\) (that is AB) gives " + MINUS + "5.",
        -5, note="AB coeff a = -5")],
    "guided_steps": [
        say("\\(\\vec{BA}\\) is the journey from B to A: \\(\\vec{BA} = \\vec{OA} - \\vec{OB}\\)."),
        box("The a terms: OA has 5a, OB has none, so 5 " + MINUS + " 0 = ", 5, "OA " + MINUS + " OB: 5a minus 0a."),
        box("The b terms: 0 " + MINUS + " 3 = ", -3, "0b minus 3b.", phase="substitute"),
        box("So \\(\\vec{BA} = 5\\mathbf{a} - 3\\mathbf{b}\\). The coefficient of a is ", 5, "Read the number in front of a.", phase="substitute", done="BA = 5a " + MINUS + " 3b, coefficient of a is 5."),
    ]})

# S3: (2k,3) parallel (4,6), k = 1  (CHANGED from (4,3) per audit degenerate fix)
silver.append({
    "display": "If \\(\\binom{2k}{3}\\) is parallel to \\(\\binom{4}{6}\\), find \\(k\\).",
    "solutions": [1], "calculator": False, "input_type": "single_value",
    "hint": "Parallel means one is a scalar multiple: use the cross products top1 × bottom2 = bottom1 × top2.",
    "misconceptions": [mis("matched_tops_directly",
        "Parallel means \\(\\binom{2k}{3} = \\lambda\\binom{4}{6}\\). The bottoms give \\(3 = 6\\lambda\\), so \\(\\lambda = \\tfrac{1}{2}\\), then \\(2k = 4 \\times \\tfrac{1}{2} = 2\\) and \\(k = 1\\). Matching the tops directly (2k = 4, k = 2) forgets the scale factor.",
        2, note="2k=4 -> k=2")],
    "guided_steps": [
        say("Two column vectors are parallel when their cross products are equal: top1 × bottom2 = bottom1 × top2."),
        box("Work the right side: bottom1 × top2 = 3 × 4 = ", 12, "3 × 4."),
        box("The left side is 2k × 6 = 12k, so 12k = 12. Divide: 12 ÷ 12 = ", 1, "12 divided by 12 gives k.", phase="substitute"),
        box("Check: with k = 1 the vector is (2, 3), and doubling the bottom, 2 × 3 = ", 6, "2 × 3 should give the original bottom 6.", phase="substitute", done="k = 1: (2, 3) doubles to (4, 6), so they are parallel."),
    ]})

# S4: midpoint top OA=(1,5),OB=(7,3) = 4
silver.append({
    "display": "M is the midpoint of AB. \\(\\vec{OA} = \\binom{1}{5}\\), \\(\\vec{OB} = \\binom{7}{3}\\). Find the top component of \\(\\vec{OM}\\).",
    "solutions": [4], "calculator": False, "input_type": "single_value",
    "hint": "The midpoint is half of (OA + OB); work out the top only.",
    "misconceptions": [mis("halved_difference",
        "\\(\\vec{OM} = \\tfrac{1}{2}(\\vec{OA} + \\vec{OB}) = \\tfrac{1}{2}(8, 8) = (4, 4)\\), so the top is 4. Halving the difference \\(\\vec{OB} - \\vec{OA}\\) gives \\(\\tfrac{1}{2}(6) = 3\\), which is the vector AM not OM.",
        3, note="half of (OB-OA) top = 3")],
    "guided_steps": [
        say("The midpoint M has \\(\\vec{OM} = \\tfrac{1}{2}(\\vec{OA} + \\vec{OB})\\): add the position vectors, then halve."),
        box("Add the bottoms: 5 + 3 = ", 8, "Bottom of OA plus bottom of OB."),
        box("Now the tops: 1 + 7 = ", 8, "Top of OA plus top of OB.", phase="substitute"),
        box("Halve the top: 8 ÷ 2 = ", 4, "Half of 8.", phase="substitute", done="OM top = 4 (the bottom is 8 ÷ 2 = 4 too), so OM = (4, 4)."),
    ]})

# S5: BA from AB=(-3,5) top = 3  (CHANGED from (-2,5) to remove dup)
silver.append({
    "display": "\\(\\vec{AB} = \\binom{-3}{5}\\). Find \\(\\vec{BA}\\). Give the top component.",
    "solutions": [3], "calculator": False, "input_type": "single_value",
    "hint": "BA = " + MINUS + "AB, so flip the sign of every component.",
    "misconceptions": [mis("did_not_flip",
        "\\(\\vec{BA} = -\\vec{AB} = (3, -5)\\), so the top is 3. Keeping the " + MINUS + "3 (not flipping the sign) is the slip.",
        -3, note="kept AB top")],
    "guided_steps": [
        say("\\(\\vec{BA}\\) is the reverse of \\(\\vec{AB}\\): \\(\\vec{BA} = -\\vec{AB}\\), so flip the sign of each component."),
        box("Flip the bottom: " + MINUS + "(5) = ", -5, "Change the sign of 5."),
        box("Flip the top: " + MINUS + "(" + MINUS + "3) = ", 3, "Minus a minus is plus: " + MINUS + "(" + MINUS + "3).", phase="substitute"),
        box("So \\(\\vec{BA}\\) = (3, " + MINUS + "5). The top component is ", 3, "Read the top of (3, " + MINUS + "5).", phase="substitute", done="BA = " + MINUS + "AB = (3, " + MINUS + "5), top is 3."),
    ]})

# S6: |(-5,12)| = 13
silver.append({
    "display": "Find \\(|\\binom{-5}{12}|\\).",
    "solutions": [13], "calculator": False, "input_type": "single_value",
    "hint": "Square both numbers, add, then square root.",
    "misconceptions": [mis("skipped_squaring",
        "Square first: \\(\\sqrt{(-5)^2 + 12^2} = \\sqrt{169} = 13\\). Adding 5 + 12 = 17 skips the squaring.",
        17, note="5+12=17")],
    "guided_steps": [
        say("Magnitude is Pythagoras on the components: square, add, square root. A negative squares to a positive."),
        box("Square the top: (" + MINUS + "5) × (" + MINUS + "5) = ", 25, "Negative five squared is positive 25."),
        box("Square the bottom: 12 × 12 = ", 144, "Twelve squared."),
        box("Add the squares: 25 + 144 = ", 169, "Add the two squares.", phase="substitute"),
        box("Square root the total: √169 = ", 13, "The square root of 169.", phase="substitute", done="√169 = 13, a whole number (a 5-12-13 triangle), so it is right."),
    ]})

silver_description = "Turn points into journeys (end minus start), then find lengths, midpoints and parallels."

# ================= GOLD =================
gold = []

# G0: parallelogram, coeff of c = 1/3, solutions [1,3], fraction
gold.append({
    "display": "OABC is a parallelogram. \\(\\vec{OA} = \\mathbf{a}\\), \\(\\vec{OC} = \\mathbf{c}\\). P divides AB in ratio 1:2. Express \\(\\vec{OP}\\) in terms of \\(\\mathbf{a}\\) and \\(\\mathbf{c}\\). What is the coefficient of \\(\\mathbf{c}\\)?",
    "solutions": [1, 3], "calculator": False, "input_type": "fraction",
    "hint": "P divides AB in ratio 1:2, so AP is 1/3 of AB; build OP = OA + AP.",
    "misconceptions": [mis("ratio_as_fraction",
        "P divides AB in ratio 1:2, so AP is \\(\\tfrac{1}{1+2} = \\tfrac{1}{3}\\) of AB. Then \\(\\vec{OP} = \\mathbf{a} + \\tfrac{1}{3}\\mathbf{c}\\), coefficient of c is \\(\\tfrac{1}{3}\\). Using \\(\\tfrac{1}{2}\\) (the ratio read as a fraction) is the classic slip.",
        [1, 2], note="1/2 instead of 1/3")],
    "guided_steps": [
        say("In parallelogram OABC, O and B are opposite corners, so \\(\\vec{OB} = \\mathbf{a} + \\mathbf{c}\\)."),
        box("Find \\(\\vec{AB} = \\vec{OB} - \\vec{OA}\\). The c's: OB has 1c, OA has none, so 1 " + MINUS + " 0 = ", 1, "OB = a + c, OA = a; subtract to leave the c."),
        say("So \\(\\vec{AB} = \\mathbf{c}\\). P divides AB in ratio 1:2."),
        box("Turn the ratio 1:2 into a fraction: AP is 1 part out of 1 + 2 = ", 3, "Add the ratio parts: 1 + 2."),
        box("So AP = \\(\\tfrac{1}{3}\\mathbf{c}\\) and \\(\\vec{OP} = \\mathbf{a} + \\tfrac{1}{3}\\mathbf{c}\\). The coefficient of c is a fraction: its numerator (top) is ", 1, "AP is ONE lot of a third of c.", phase="substitute"),
        box("Its denominator (bottom), from AP being one third of AB, is ", 3, "One third has denominator 3.", phase="substitute", done="Coefficient of c is 1/3, so OP = a + (1/3)c."),
    ]})

# G1: XY coeff of a = 2
gold.append({
    "display": "\\(\\vec{OA} = \\mathbf{a}\\), \\(\\vec{OB} = \\mathbf{b}\\). X is such that \\(\\vec{OX} = 2\\mathbf{a} - \\mathbf{b}\\). Y is such that \\(\\vec{OY} = 4\\mathbf{a} - 3\\mathbf{b}\\). Express \\(\\vec{XY}\\) in terms of \\(\\mathbf{a}\\) and \\(\\mathbf{b}\\). What is the coefficient of \\(\\mathbf{a}\\)?",
    "solutions": [2], "calculator": False, "input_type": "single_value",
    "hint": "XY = OY " + MINUS + " OX, then collect the a terms.",
    "misconceptions": [mis("reversed_direction",
        "\\(\\vec{XY} = \\vec{OY} - \\vec{OX} = (4\\mathbf{a} - 3\\mathbf{b}) - (2\\mathbf{a} - \\mathbf{b}) = 2\\mathbf{a} - 2\\mathbf{b}\\), coefficient of a is 2. Doing \\(\\vec{OX} - \\vec{OY}\\) (that is YX) gives " + MINUS + "2.",
        -2, note="YX coeff a = -2")],
    "guided_steps": [
        say("\\(\\vec{XY}\\) is the journey from X to Y: \\(\\vec{XY} = \\vec{OY} - \\vec{OX}\\)."),
        box("The b terms: OY has " + MINUS + "3b, OX has " + MINUS + "b, so " + MINUS + "3 " + MINUS + " (" + MINUS + "1) = ", -2, "" + MINUS + "3b minus (" + MINUS + "1b): " + MINUS + "3 + 1."),
        box("The a terms: OY has 4a, OX has 2a, so 4 " + MINUS + " 2 = ", 2, "4a minus 2a.", phase="substitute"),
        box("So \\(\\vec{XY} = 2\\mathbf{a} - 2\\mathbf{b}\\). The coefficient of a is ", 2, "Read the number in front of a.", phase="substitute", done="XY = 2a " + MINUS + " 2b, coefficient of a is 2."),
    ]})

# G2: 3a+kb parallel 6a-4b, k = -2
gold.append({
    "display": "Vectors \\(3\\mathbf{a} + k\\mathbf{b}\\) and \\(6\\mathbf{a} - 4\\mathbf{b}\\) are parallel. Find \\(k\\).",
    "solutions": [-2], "calculator": False, "input_type": "single_value",
    "hint": "The second vector is 2 times the first; match the b terms to find k.",
    "misconceptions": [mis("dropped_negative",
        "Second = 2 × first: \\(6\\mathbf{a} - 4\\mathbf{b} = 2(3\\mathbf{a} + k\\mathbf{b})\\), so \\(2k = -4\\) and \\(k = -2\\). Dropping the minus gives k = 2.",
        2, note="ignore sign -> 2")],
    "guided_steps": [
        say("Parallel means the second vector is a scalar multiple of the first: \\(6\\mathbf{a} - 4\\mathbf{b} = \\lambda(3\\mathbf{a} + k\\mathbf{b})\\). The a terms fix \\(\\lambda\\)."),
        box("The a terms: 6 = λ × 3, so λ = 6 ÷ 3 = ", 2, "6 divided by 3."),
        box("The b terms: " + MINUS + "4 = λ × k = 2k, so k = " + MINUS + "4 ÷ 2 = ", -2, "" + MINUS + "4 divided by 2.", phase="substitute"),
        box("Check: with k = " + MINUS + "2, the b term of 2 × (3a " + MINUS + " 2b) is 2 × (" + MINUS + "2) = ", -4, "2 × (" + MINUS + "2) should give " + MINUS + "4.", phase="substitute", done="k = " + MINUS + "2 makes the second vector exactly 2× the first, so they are parallel."),
    ]})

# G3: N divides AB 3:1, top of ON = 0
gold.append({
    "display": "\\(\\vec{OA} = \\binom{3}{1}\\), \\(\\vec{OB} = \\binom{-1}{5}\\). N divides AB in ratio 3:1. Find the top component of \\(\\vec{ON}\\).",
    "solutions": [0], "calculator": False, "input_type": "single_value",
    "hint": "AN is 3/4 of AB; work out ON = OA + AN, top component only.",
    "misconceptions": [mis("reversed_ratio",
        "N divides AB in ratio 3:1, so AN is \\(\\tfrac{3}{4}\\) of AB. \\(\\vec{ON} = \\vec{OA} + \\tfrac{3}{4}(-4, 4) = (3, 1) + (-3, 3) = (0, 4)\\), top = 0. Using \\(\\tfrac{1}{4}\\) (reversing the ratio) gives top = 2.",
        2, note="1/4 of AB -> ON=(2,2)")],
    "guided_steps": [
        say("First find \\(\\vec{AB} = \\mathbf{b} - \\mathbf{a}\\), then N is 3/4 of the way along (3 parts out of 3 + 1)."),
        box("AB top: " + MINUS + "1 " + MINUS + " 3 = ", -4, "Top of OB minus top of OA: " + MINUS + "1 " + MINUS + " 3."),
        box("AN top: \\(\\tfrac{3}{4}\\) × (" + MINUS + "4) = ", -3, "Three quarters of " + MINUS + "4."),
        box("ON top = OA top + AN top = 3 + (" + MINUS + "3) = ", 0, "Add the tops: 3 + (" + MINUS + "3).", phase="substitute"),
        box("Check with the bottom: AB bottom = 5 " + MINUS + " 1 = 4, AN bottom = \\(\\tfrac{3}{4}\\)(4) = 3, so ON bottom = 1 + 3 = ", 4, "1 + 3.", phase="substitute", done="ON = (0, 4). The top component asked for is 0."),
    ]})

# G4: collinear, AB top = 3
gold.append({
    "display": "Points A\\((1,2)\\), B\\((4,8)\\) and C\\((6,12)\\) are collinear. Find \\(\\vec{AB}\\) as a column vector and give the top component.",
    "solutions": [3], "calculator": False, "input_type": "single_value",
    "hint": "AB = B " + MINUS + " A, so subtract the coordinates in that order.",
    "misconceptions": [mis("reversed_direction",
        "\\(\\vec{AB} = B - A = (4 - 1,\\ 8 - 2) = (3, 6)\\), so the top is 3. Doing A " + MINUS + " B gives " + MINUS + "3, which is BA (the reverse direction).",
        -3, note="A-B top = -3")],
    "guided_steps": [
        say("For points, \\(\\vec{AB} = B - A\\): the coordinates of B minus the coordinates of A."),
        box("AB bottom: 8 " + MINUS + " 2 = ", 6, "y of B minus y of A: 8 " + MINUS + " 2."),
        box("AB top: 4 " + MINUS + " 1 = ", 3, "x of B minus x of A: 4 " + MINUS + " 1.", phase="substitute"),
        box("Check collinear: \\(\\vec{AC} = C - A = (5, 10)\\), and (5, 10) = \\(\\tfrac{5}{3}\\)(3, 6). The top component of AB asked for is ", 3, "Read the top of (3, 6).", phase="substitute", done="AB = (3, 6) and AC = (5, 10) = (5/3)AB, so A, B, C are collinear. Top of AB is 3."),
    ]})

gold_description = "Divide a line in a given ratio and prove parallel or collinear results."

# ================= tier_guides =================
tier_guides = {
    "bronze": {
        "title": "Bronze: Column vector arithmetic",
        "steps": [
            "A <strong>column vector</strong> \\(\\binom{x}{y}\\) means x across and y up. To <strong>add</strong> or <strong>subtract</strong>, work top-with-top and bottom-with-bottom, keeping every sign.",
            "To <strong>scalar multiply</strong>, multiply both parts by the number: \\(3\\binom{2}{-1} = \\binom{6}{-3}\\).",
            "The <strong>magnitude</strong> (length) is \\(|\\binom{x}{y}| = \\sqrt{x^2 + y^2}\\)."
        ],
        "example": {
            "question": "Work out \\(\\binom{4}{-2} + \\binom{1}{5}\\).",
            "steps": [
                {"label": "Top", "content": "\\(4 + 1 = 5\\)"},
                {"label": "Bottom", "content": "\\(-2 + 5 = 3\\)"},
                {"label": "Check", "content": "The " + MINUS + "2 stayed negative, so the signs were kept."},
                {"label": "Answer", "content": "\\(\\binom{5}{3}\\)", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: Position vectors and length",
        "steps": [
            "A <strong>position vector</strong> runs from the origin O to a point. To travel between two points, go via O: \\(\\vec{AB} = \\mathbf{b} - \\mathbf{a}\\) (end minus start).",
            "<strong>Reverse</strong> a vector by negating it: \\(\\vec{BA} = -\\vec{AB}\\). The <strong>midpoint</strong> of AB has \\(\\vec{OM} = \\tfrac{1}{2}(\\mathbf{a} + \\mathbf{b})\\).",
            "Two vectors are <strong>parallel</strong> when one is a scalar multiple of the other: \\(\\binom{2}{6}\\) is parallel to \\(\\binom{1}{3}\\)."
        ],
        "example": {
            "question": "\\(\\vec{OA} = \\binom{1}{2}\\), \\(\\vec{OB} = \\binom{4}{6}\\). Find \\(|\\vec{AB}|\\).",
            "steps": [
                {"label": "AB = b minus a", "content": "\\(\\binom{4-1}{6-2} = \\binom{3}{4}\\)"},
                {"label": "Square and add", "content": "\\(3^2 + 4^2 = 25\\)"},
                {"label": "Check", "content": "\\(\\sqrt{25}\\) is exact, a 3-4-5 triangle."},
                {"label": "Answer", "content": "\\(|\\vec{AB}| = 5\\)", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: Ratios, parallels and proof",
        "steps": [
            "To find a point <strong>dividing a line</strong> AB in ratio \\(m:n\\), first find \\(\\vec{AB} = \\mathbf{b} - \\mathbf{a}\\), then take \\(\\tfrac{m}{m+n}\\) of it: \\(\\vec{OP} = \\mathbf{a} + \\tfrac{m}{m+n}\\vec{AB}\\).",
            "For a <strong>parallel</strong> condition, set one vector equal to a scalar \\(k\\) times the other and match components to find the unknown.",
            "Points are <strong>collinear</strong> if the vectors between them are parallel and share a point."
        ],
        "example": {
            "question": "\\(\\vec{OA} = \\binom{0}{1}\\), \\(\\vec{OB} = \\binom{6}{4}\\). P divides AB in ratio 2:1. Find \\(\\vec{OP}\\).",
            "steps": [
                {"label": "AB = b minus a", "content": "\\(\\binom{6}{3}\\)"},
                {"label": "Fraction of AB", "content": "\\(\\tfrac{2}{3}\\binom{6}{3} = \\binom{4}{2}\\)"},
                {"label": "Add to OA", "content": "\\(\\binom{0}{1} + \\binom{4}{2} = \\binom{4}{3}\\)"},
                {"label": "Check", "content": "P is \\(\\tfrac{2}{3}\\) along, past the middle, which matches."},
                {"label": "Answer", "content": "\\(\\vec{OP} = \\binom{4}{3}\\)", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

# ================= guided (opener + teach) =================
opener = {
    "steps": [
        say("Forget vectors for a second. Picture yourself walking around a park, counting your steps."),
        box("You walk 4 steps East, then 1 step North. From there you walk 2 more steps East, then 3 more steps North. In total, how many steps East of your start are you? Steps East = ", 6, "Add the two East legs: 4 + 2."),
        say("That is the whole idea of adding vectors: the East parts add together on their own."),
        box("And how many steps North of your start are you? Steps North = ", 4, "Add the two North legs: 1 + 3."),
        say("Each journey is a vector: an amount across and an amount up. Adding them means adding the across parts and the up parts separately. Mathematicians stack across-over-up in a column: \\(\\binom{4}{1} + \\binom{2}{3} = \\binom{6}{4}\\). That is all a column vector is: a journey.")
    ]
}

teach = {
    "bronze": {
        "display": "\\(\\mathbf{u} = \\binom{5}{2}\\) and \\(\\mathbf{v} = \\binom{-1}{4}\\). Work out \\(\\mathbf{u} + \\mathbf{v}\\), then \\(3\\mathbf{u}\\).",
        "steps": [
            say("Everything happens row by row. Start with the sum \\(\\mathbf{u} + \\mathbf{v}\\)."),
            box("Top row: 5 + (" + MINUS + "1) = ", 4, "Add the tops, keep the signs."),
            box("Bottom row: 2 + 4 = ", 6, "Add the bottoms.", done="So u + v = (4, 6): across parts and up parts, added separately."),
            say("Now scale u by 3. A scalar multiplies every row."),
            box("Top of 3u: 3 × 5 = ", 15, "Multiply the top by 3."),
            box("Bottom of 3u: 3 × 2 = ", 6, "Multiply the bottom by 3.", done="3u = (15, 6). A scalar stretches every part. Adding and scaling are the whole of bronze.")
        ]
    },
    "silver": {
        "display": "\\(\\vec{OA} = \\binom{2}{1}\\), \\(\\vec{OB} = \\binom{6}{4}\\). Find \\(\\vec{AB}\\) and its length \\(|\\vec{AB}|\\).",
        "steps": [
            say("A position vector runs from O to a point. To go from A to B, use \\(\\vec{AB} = \\mathbf{b} - \\mathbf{a}\\)."),
            box("Top: 6 " + MINUS + " 2 = ", 4, "AB = b " + MINUS + " a: subtract the tops."),
            box("Bottom: 4 " + MINUS + " 1 = ", 3, "Subtract the bottoms.", done="AB = (4, 3): always end minus start."),
            say("The length is Pythagoras on the components."),
            box("Square and add: \\(4^2 + 3^2\\) = ", 25, "16 + 9."),
            box("Square root: √25 = ", 5, "The square root of 25.", done="|AB| = 5. b minus a, then its length, is the silver move.")
        ]
    },
    "gold": {
        "display": "\\(\\vec{OA} = \\binom{2}{0}\\), \\(\\vec{OB} = \\binom{8}{6}\\). P divides AB in ratio 1:2. Find both components of \\(\\vec{OP}\\).",
        "steps": [
            say("First find \\(\\vec{AB} = \\mathbf{b} - \\mathbf{a}\\)."),
            box("AB top: 8 " + MINUS + " 2 = ", 6, "Subtract the tops."),
            box("AB bottom: 6 " + MINUS + " 0 = ", 6, "Subtract the bottoms.", done="AB = (6, 6)."),
            say("P divides AB in ratio 1:2, so AP is \\(\\tfrac{1}{3}\\) of AB (1 part out of 1 + 2 = 3)."),
            box("AP top: \\(\\tfrac{1}{3}\\) × 6 = ", 2, "One third of 6."),
            box("AP bottom: \\(\\tfrac{1}{3}\\) × 6 = ", 2, "One third of 6.", done="AP = (2, 2)."),
            box("OP top = OA top + AP top = 2 + 2 = ", 4, "Add the tops: 2 + 2."),
            box("OP bottom = 0 + 2 = ", 2, "Add the bottoms: 0 + 2.", done="OP = (4, 2). Turn a ratio into a fraction of AB, then add it to OA: the gold move.")
        ]
    }
}

# ================= preserved fields (worked_examples em dashes -> colon) =================
related_videos = [
    {"url": "https://www.youtube.com/watch?v=xOdkldbusy0", "title": "Vectors - Corbettmaths", "channel": "Corbett Maths"}
]

worked_examples = [
    {
        "steps": [
            {"label": "Answer", "content": "<p>\\(\\binom{3}{2} + \\binom{-1}{5} = \\binom{2}{7}\\)</p>", "isAnswer": True, "is_answer": True}
        ],
        "question": "Add the vectors (3, 2) and (−1, 5). Give as a column vector.",
        "difficulty": "Bronze"
    },
    {
        "steps": [
            {"label": "Step 1: Find AB", "content": "<p>\\(\\vec{AB} = \\mathbf{b} - \\mathbf{a}\\)</p>"},
            {"label": "Step 2: Midpoint", "content": "<p>\\(\\vec{AM} = \\frac{1}{2}(\\mathbf{b} - \\mathbf{a})\\)</p>"},
            {"label": "Answer", "content": "<p>\\(\\vec{OM} = \\mathbf{a} + \\frac{1}{2}(\\mathbf{b} - \\mathbf{a}) = \\frac{1}{2}\\mathbf{a} + \\frac{1}{2}\\mathbf{b} = \\frac{1}{2}(\\mathbf{a} + \\mathbf{b})\\)</p>", "isAnswer": True, "is_answer": True}
        ],
        "question": "OA = a, OB = b. M is the midpoint of AB. Find OM in terms of a and b.",
        "difficulty": "Gold"
    }
]

practice_data = {
    "method_card": method_card,
    "topic_links": topic_links,
    "problem_bank": {
        "gold": gold,
        "bronze": bronze,
        "silver": silver,
        "bronze_description": bronze_description,
        "silver_description": silver_description,
        "gold_description": gold_description
    },
    "tier_guides": tier_guides,
    "guided": {"opener": opener, "teach": teach},
    "related_videos": related_videos,
    "worked_examples": worked_examples
}

with io.open("lesson_geometry-L08.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(practice_data, indent=1, ensure_ascii=False))
print("written lesson_geometry-L08.json")
