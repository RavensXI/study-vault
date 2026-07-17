# -*- coding: utf-8 -*-
"""Build maths-eduqas probability-statistics-L02 guided + diagrams practice_data."""
import json, io

MINUS = "−"  # minus sign
CAP = "∩"    # intersection
CUP = "∪"    # union

def venn(labelA, labelB, aOnly, both, bOnly, neither, total, aria, bold=None):
    def fw(name):
        return ' font-weight="700"' if bold == name else ''
    def s(v):
        return '' if v is None else str(v)
    p = []
    p.append('<svg viewBox="0 0 260 180" role="img" aria-label="%s" style="max-width:260px">' % aria)
    p.append('<rect x="8" y="10" width="244" height="150" rx="6" fill="none" stroke="currentColor" stroke-width="1"/>')
    p.append('<circle cx="100" cy="90" r="52" fill="#60a5fa" fill-opacity="0.15" stroke="currentColor" stroke-width="1"/>')
    p.append('<circle cx="160" cy="90" r="52" fill="#f59e0b" fill-opacity="0.15" stroke="currentColor" stroke-width="1"/>')
    p.append('<text x="72" y="54" font-family="Inter, sans-serif" font-size="12" fill="currentColor" text-anchor="middle" font-weight="700">%s</text>' % labelA)
    p.append('<text x="188" y="54" font-family="Inter, sans-serif" font-size="12" fill="currentColor" text-anchor="middle" font-weight="700">%s</text>' % labelB)
    p.append('<text x="76" y="96" font-family="Inter, sans-serif" font-size="12" fill="currentColor" text-anchor="middle"%s>%s</text>' % (fw('aOnly'), s(aOnly)))
    p.append('<text x="130" y="96" font-family="Inter, sans-serif" font-size="12" fill="currentColor" text-anchor="middle"%s>%s</text>' % (fw('both'), s(both)))
    p.append('<text x="184" y="96" font-family="Inter, sans-serif" font-size="12" fill="currentColor" text-anchor="middle"%s>%s</text>' % (fw('bOnly'), s(bOnly)))
    p.append('<text x="236" y="150" font-family="Inter, sans-serif" font-size="12" fill="currentColor" text-anchor="middle"%s>%s</text>' % (fw('neither'), s(neither)))
    p.append('<text x="14" y="26" font-family="Inter, sans-serif" font-size="11" fill="currentColor" text-anchor="start">Total: %s</text>' % s(total))
    p.append('</svg>')
    return ''.join(p)

def box(pre, answer, hint, post="", say=None, phase=None, done=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if phase: d["phase"] = phase
    if done: d["done"] = done
    return d

def say(text):
    return {"say": text}

MUL = chr(215)   # ×
DIV = chr(247)   # ÷
NE = chr(8800)   # ≠

pd = {}

pd["method_card"] = {
    "title": "Venn Diagrams & Conditional Probability",
    "steps": [
        "Draw two overlapping circles inside a rectangle.",
        "Fill the intersection first, then subtract it from each set total.",
        "Put the rest in the 'neither' region; all regions total the whole group.",
        "Conditional: P(A|B) = n(A%sB) / n(B), dividing by the given group." % CAP,
    ],
    "content": ("<p><strong>Venn diagrams</strong> show overlapping sets. "
                "\\(P(A \\cup B) = P(A) + P(B) - P(A \\cap B)\\). The region outside both circles is \\(P(\\text{neither})\\).</p>"
                "<p><strong>Conditional probability:</strong> \\(P(A | B) = \\frac{P(A \\cap B)}{P(B)}\\), read as 'probability of A given B has happened'.</p>"
                "<p>Fill a Venn diagram from the <strong>intersection first</strong>, then work outward. All regions total 1 (or the whole count).</p>"),
    "example": ("<p><strong>40 students: 24 like football, 16 like tennis, 8 like both.</strong></p>"
                "<p>Football only: 16, Both: 8, Tennis only: 8, Neither: 8. P(football | tennis) = 8/16 = 1/2.</p>"),
}

live = json.load(io.open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\_ps02_live.json", encoding="utf-8"))
pd["topic_links"] = live["topic_links"]
pd["related_videos"] = live["related_videos"]
pd["worked_examples"] = live["worked_examples"]

bronze = []

bronze.append({
    "display": venn("Maths", "Science", 18, 10, 12, "?", 50, "Venn: maths and science, overlap 10", bold="neither")
        + "<br>50 students: 28 like maths, 22 like science, 10 like both. How many like neither?",
    "solutions": [10], "calculator": False, "input_type": "single_value",
    "hint": "Fill the overlap first, then subtract it from each total; neither is the rest.",
    "misconceptions": [{"pattern": "forget_intersection",
        "message": "If you add 28 + 22 = 50 you count the 10 both twice, leaving neither = 0. Subtract the overlap: 18 + 10 + 12 = 40, so neither = 50 " + MINUS + " 40 = 10.",
        "expect": [0], "note": "double-counted both"}],
    "guided_steps": [
        say("Fill the Venn from the middle out: the overlap first, then each single region, then what is left."),
        box("Both maths and science (the overlap) = ", 10, "Given as 10."),
        box("Maths only: 28 " + MINUS + " 10 = ", 18, "Take the overlap off the maths total."),
        box("Science only: 22 " + MINUS + " 10 = ", 12, "Take the overlap off the science total."),
        box("Add the three filled regions: 18 + 10 + 12 = ", 40, "Everyone who likes at least one.", say="Add the three filled regions.", phase="substitute"),
        box("Neither: 50 " + MINUS + " 40 = ", 10, "The rest of the group.", phase="substitute", done="10 like neither."),
    ],
})

bronze.append({
    "display": venn("Maths", "Science", 18, 10, 12, 10, 50, "Venn: maths and science, maths only 18", bold="aOnly")
        + "<br>From the same data (50 students, 28 maths, 22 science, 10 both), find P(maths only) as a simplified fraction.",
    "solutions": [9, 25], "calculator": False, "input_type": "fraction",
    "hint": "Maths only is 28 minus the 10 overlap, then put it over 50.",
    "misconceptions": [{"pattern": "include_both",
        "message": "28/50 counts the overlap as maths only. Maths ONLY is 28 " + MINUS + " 10 = 18, so P = 18/50 = 9/25.",
        "expect": [14, 25], "note": "used n(A)=28 not A-only"}],
    "guided_steps": [
        say("Maths only means maths but NOT the overlap. Find that count, then put it over the total."),
        box("Maths only: 28 " + MINUS + " 10 = ", 18, "Take the overlap off."),
        box("Total students = ", 50, "The whole group."),
        box("So P(maths only) = 18/50. Simplify by 2, top: 18 " + DIV + " 2 = ", 9, "Halve the top.", say="Simplify by dividing top and bottom by 2.", phase="substitute"),
        box("50 " + DIV + " 2 = ", 25, "Halve the bottom.", phase="substitute", done="P(maths only) = 9/25."),
    ],
})

bronze.append({
    "display": venn("Cat", "Dog", 30, 15, 20, 15, 80, "Venn: cat and dog owners, overlap 15", bold="both")
        + "<br>80 people: 45 own a cat, 35 own a dog, 15 own both. Find P(cat or dog) as a simplified fraction.",
    "solutions": [13, 16], "calculator": False, "input_type": "fraction",
    "hint": "Add both totals and subtract the overlap once, then divide by 80.",
    "misconceptions": [{"pattern": "add_without_subtract",
        "message": "(45 + 35)/80 counts the 15 both twice. Subtract the overlap once: 65/80 = 13/16.",
        "expect": [80, 80], "note": "no subtract overlap, 80/80"}],
    "guided_steps": [
        say("Cat or dog means in either circle. Add the totals, then subtract the overlap once so it is not double counted."),
        box("Cats plus dogs: 45 + 35 = ", 80, "Add both totals."),
        box("Subtract the overlap once: 80 " + MINUS + " 15 = ", 65, "The 15 both were counted twice."),
        box("Total people = ", 80, "The whole group."),
        box("So P(cat or dog) = 65/80. Simplify by 5, top: 65 " + DIV + " 5 = ", 13, "Divide the top by 5.", say="Simplify by dividing by 5.", phase="substitute"),
        box("80 " + DIV + " 5 = ", 16, "Divide the bottom by 5.", phase="substitute", done="P(cat or dog) = 13/16."),
    ],
})

bronze.append({
    "display": venn("A", "B", 12, 6, 18, 14, "?", "Venn: sets A and B, find the total")
        + "<br>A Venn diagram has: A only = 12, B only = 18, A " + CAP + " B = 6, neither = 14. What is the total?",
    "solutions": [50], "calculator": False, "input_type": "single_value",
    "hint": "Add all four regions, including the neither group outside the circles.",
    "misconceptions": [{"pattern": "miss_neither",
        "message": "12 + 6 + 18 = 36 leaves out the 14 in the neither region. The total includes them: 12 + 6 + 18 + 14 = 50.",
        "expect": [36], "note": "forgot neither"}],
    "guided_steps": [
        say("The total is every region added together, including the neither region outside the circles."),
        box("Overlap (A and B) = ", 6, "Given as 6."),
        box("In the circles: 12 + 6 + 18 = ", 36, "A only, both, then B only."),
        box("Now add the neither region: 36 + 14 = ", 50, "Include those outside the circles.", say="Add the neither region to reach the total.", phase="substitute"),
        box("Check: 12 + 6 + 18 + 14 = ", 50, "All four regions.", phase="substitute", done="Total = 50."),
    ],
})

bronze.append({
    "display": "P(A) = 0.7, P(A " + CAP + " B) = 0.3. Find P(A only) as a decimal.",
    "solutions": [0.4], "calculator": False, "input_type": "single_value",
    "hint": "A only is P(A) minus the overlap P(A and B).",
    "misconceptions": [{"pattern": "forgot_subtract",
        "message": "0.7 is all of A. A only removes the overlap: 0.7 " + MINUS + " 0.3 = 0.4.",
        "expect": [0.7], "note": "gave P(A)"}],
    "guided_steps": [
        say("A only means the part of A that does not overlap B. Subtract the overlap from all of A."),
        box("All of A, P(A) = ", 0.7, "Given as 0.7."),
        box("The overlap P(A " + CAP + " B) = ", 0.3, "Given as 0.3."),
        box("A only: 0.7 " + MINUS + " 0.3 = ", 0.4, "Take the overlap off.", say="A only is what is left after removing the overlap.", phase="substitute"),
        box("Check: A only plus overlap gives all of A. 0.4 + 0.3 = ", 0.7, "Should return P(A).", phase="substitute", done="P(A only) = 0.4."),
    ],
})

bronze.append({
    "display": venn("English", "History", 24, 12, 12, "?", 60, "Venn: English and History, overlap 12", bold="neither")
        + "<br>60 students: 36 like English, 24 like History, 12 like both. Find P(neither) as a simplified fraction.",
    "solutions": [1, 5], "calculator": False, "input_type": "fraction",
    "hint": "Find how many like at least one, then the rest like neither.",
    "misconceptions": [{"pattern": "gave_at_least_one",
        "message": "48/60 = 4/5 is P(likes at least one). Neither is the rest: 1 " + MINUS + " 4/5 = 1/5.",
        "expect": [4, 5], "note": "complement of neither"}],
    "guided_steps": [
        say("Find how many like at least one subject, then the rest of the group like neither."),
        box("English only: 36 " + MINUS + " 12 = ", 24, "Take the overlap off English."),
        box("History only: 24 " + MINUS + " 12 = ", 12, "Take the overlap off History."),
        box("At least one: 24 + 12 + 12 = ", 48, "Add the three circle regions."),
        box("Neither: 60 " + MINUS + " 48 = ", 12, "The rest of the group.", say="Neither is the total minus those 48.", phase="substitute"),
        box("So P(neither) = 12/60. Simplify by 12, top: 12 " + DIV + " 12 = ", 1, "Numerator over 12.", phase="substitute"),
        box("60 " + DIV + " 12 = ", 5, "Denominator over 12.", phase="substitute", done="P(neither) = 1/5."),
    ],
})

bronze.append({
    "display": venn("A", "B", 22, 8, "", "", 60, "Venn: 30 students in set A out of 60", bold="aOnly")
        + "<br>A Venn diagram shows 30 students in set A and 8 in A " + CAP + " B, out of 60 total. Find P(A) as a simplified fraction.",
    "solutions": [1, 2], "calculator": False, "input_type": "fraction",
    "hint": "Everyone in circle A counts, both the overlap and A only: 30 out of 60.",
    "misconceptions": [{"pattern": "just_intersection",
        "message": "8/60 is only the overlap. Circle A holds everyone in A: 30/60 = 1/2.",
        "expect": [2, 15], "note": "used intersection 8/60"}],
    "guided_steps": [
        say("P(A) uses everyone inside circle A: both the overlap and the A-only part."),
        box("Number in set A = ", 30, "Given as 30."),
        box("Total students = ", 60, "Out of 60."),
        box("So P(A) = 30/60. Simplify by 30, top: 30 " + DIV + " 30 = ", 1, "Top divided by 30.", say="Simplify by dividing by 30.", phase="substitute"),
        box("60 " + DIV + " 30 = ", 2, "Bottom divided by 30.", phase="substitute", done="P(A) = 1/2."),
    ],
})

bronze.append({
    "display": venn("A", "B", "?", 15, 20, 25, 100, "Venn: sets A and B out of 100", bold="aOnly")
        + "<br>100 people: P(A) = 0.55, P(B) = 0.35, P(A " + CAP + " B) = 0.15. How many are in A only?",
    "solutions": [40], "calculator": False, "input_type": "single_value",
    "hint": "Turn the probabilities into counts out of 100, then take the overlap off A.",
    "misconceptions": [{"pattern": "forgot_subtract",
        "message": "55 is all of A. A only removes the overlap: 55 " + MINUS + " 15 = 40.",
        "expect": [55], "note": "gave n(A)"}],
    "guided_steps": [
        say("Turn each probability into a count out of 100, then take the overlap off A."),
        box("n(A) = 0.55 " + MUL + " 100 = ", 55, "0.55 of 100."),
        box("n(A " + CAP + " B) = 0.15 " + MUL + " 100 = ", 15, "0.15 of 100."),
        box("A only: 55 " + MINUS + " 15 = ", 40, "Take the overlap off.", say="A only removes the overlap from A.", phase="substitute"),
        box("Check: A only plus overlap = 40 + 15 = ", 55, "Should return n(A).", phase="substitute", done="n(A only) = 40."),
    ],
})

silver = []

silver.append({
    "display": venn("Football", "Rugby", 35, 25, 20, 10, 90, "Venn: football and rugby, overlap 25", bold="both")
        + "<br>90 students: 60 like football, 45 like rugby, 25 like both. Find P(football | rugby) as a simplified fraction.",
    "solutions": [5, 9], "calculator": False, "input_type": "fraction",
    "hint": "Given rugby, divide the overlap by the rugby total, not by 90.",
    "misconceptions": [{"pattern": "used_total",
        "message": "25/90 divides by the whole group. Given rugby, divide by the rugby total: 25/45 = 5/9.",
        "expect": [5, 18], "note": "divided by 90"}],
    "guided_steps": [
        say("Given rugby, we only look inside the rugby group. P(F|R) = both, over the rugby total."),
        box("Both football and rugby = ", 25, "The overlap."),
        box("Rugby total (the given group) = ", 45, "All who like rugby."),
        box("So P(F|R) = 25/45. Simplify by 5, top: 25 " + DIV + " 5 = ", 5, "Top over 5.", say="Simplify by dividing by 5.", phase="substitute"),
        box("45 " + DIV + " 5 = ", 9, "Bottom over 5.", phase="substitute", done="P(F|R) = 5/9."),
    ],
})

silver.append({
    "display": "P(A) = 0.6, P(B) = 0.5, P(A " + CAP + " B) = 0.2. Find P(A " + CUP + " B).",
    "solutions": [0.9], "calculator": False, "input_type": "single_value",
    "hint": "Add P(A) and P(B), then subtract the overlap once.",
    "misconceptions": [{"pattern": "add_only",
        "message": "0.6 + 0.5 = 1.1 double counts the overlap. Subtract it once: 1.1 " + MINUS + " 0.2 = 0.9.",
        "expect": [1.1], "note": "no subtract"}],
    "guided_steps": [
        say("Union is everything in either set. Add the two, then subtract the overlap so it is counted once."),
        box("P(A) + P(B) = 0.6 + 0.5 = ", 1.1, "Add the two."),
        box("The overlap P(A " + CAP + " B) = ", 0.2, "Given as 0.2."),
        box("Subtract the overlap once: 1.1 " + MINUS + " 0.2 = ", 0.9, "Remove the double count.", say="Subtract the overlap once.", phase="substitute"),
        box("Check: 0.6 + 0.5 " + MINUS + " 0.2 = ", 0.9, "The addition rule.", phase="substitute", done="P(A " + CUP + " B) = 0.9."),
    ],
})

silver.append({
    "display": "P(A) = 0.8, P(B) = 0.5, P(A " + CUP + " B) = 0.9. Find P(A " + CAP + " B).",
    "solutions": [0.4], "calculator": False, "input_type": "single_value",
    "hint": "The overlap is P(A) plus P(B) minus the union.",
    "misconceptions": [{"pattern": "subtracted_one_set",
        "message": "0.9 " + MINUS + " 0.8 = 0.1 subtracts only P(A) from the union. The overlap is P(A) + P(B) " + MINUS + " P(A " + CUP + " B) = 0.8 + 0.5 " + MINUS + " 0.9 = 0.4.",
        "expect": [0.1], "note": "union minus P(A) only"}],
    "guided_steps": [
        say("Rearrange the addition rule: the overlap equals P(A) + P(B) minus the union."),
        box("P(A) + P(B) = 0.8 + 0.5 = ", 1.3, "Add the two sets."),
        box("The union P(A " + CUP + " B) = ", 0.9, "Given as 0.9."),
        box("Subtract the union: 1.3 " + MINUS + " 0.9 = ", 0.4, "This gives the overlap.", say="Subtract the union from that sum.", phase="substitute"),
        box("Check: 0.8 + 0.5 " + MINUS + " 0.4 = 0.9, the union. Type the overlap again: ", 0.4, "It stays 0.4.", phase="substitute", done="P(A " + CAP + " B) = 0.4."),
    ],
})

silver.append({
    "display": venn("Netball", "Hockey", 20, 15, 15, 10, 60, "Venn: netball and hockey, overlap 15", bold="both")
        + "<br>60 students: 35 play netball, 30 play hockey, 15 play both. Find P(hockey | netball) as a simplified fraction.",
    "solutions": [3, 7], "calculator": False, "input_type": "fraction",
    "hint": "Given netball, divide the overlap by the netball total, not by 60.",
    "misconceptions": [{"pattern": "used_total",
        "message": "15/60 divides by the whole group. Given netball, divide by the netball total: 15/35 = 3/7.",
        "expect": [1, 4], "note": "divided by 60"}],
    "guided_steps": [
        say("Given netball, look only inside the netball group. P(H|N) = both, over the netball total."),
        box("Both hockey and netball = ", 15, "The overlap."),
        box("Netball total (the given group) = ", 35, "All who play netball."),
        box("So P(H|N) = 15/35. Simplify by 5, top: 15 " + DIV + " 5 = ", 3, "Top over 5.", say="Simplify by dividing by 5.", phase="substitute"),
        box("35 " + DIV + " 5 = ", 7, "Bottom over 5.", phase="substitute", done="P(H|N) = 3/7."),
    ],
})

silver.append({
    "display": "Are events A and B independent if P(A) = 0.4, P(B) = 0.3, P(A " + CAP + " B) = 0.12?",
    "options": [
        "Yes, because P(A)" + MUL + "P(B) = P(A" + CAP + "B)",
        "No, because P(A)" + MUL + "P(B) " + NE + " P(A" + CAP + "B)",
        "Yes, because P(A" + CUP + "B) = P(A)+P(B)",
        "Cannot tell",
    ],
    "solutions": [0], "calculator": False, "input_type": "multiple_choice",
    "hint": "Events are independent when P(A) times P(B) equals P(A and B).",
    "misconceptions": [{"pattern": "wrong_test",
        "message": "0.4 " + MUL + " 0.3 = 0.12, which equals P(A " + CAP + " B), so the events ARE independent.",
        "expect": [1], "note": "chose No"}],
})

silver.append({
    "display": "P(B) = 0.5, P(A " + CAP + " B) = 0.2. Find P(A | B) as a simplified fraction.",
    "solutions": [2, 5], "calculator": False, "input_type": "fraction",
    "hint": "Divide the overlap P(A and B) by P(B).",
    "misconceptions": [{"pattern": "gave_intersection",
        "message": "0.2 = 1/5 is the overlap itself. Divide by P(B): 0.2/0.5 = 2/5.",
        "expect": [1, 5], "note": "gave intersection 0.2=1/5"}],
    "guided_steps": [
        say("Conditional formula: P(A|B) = P(A " + CAP + " B) over P(B)."),
        box("P(A " + CAP + " B) = ", 0.2, "Given as 0.2."),
        box("P(B) = ", 0.5, "Given as 0.5."),
        box("Divide the overlap by P(B): 0.2 " + DIV + " 0.5 = ", 0.4, "Overlap over the given set.", say="Divide the overlap by P(B).", phase="substitute"),
        box("0.4 = 4/10, simplify by 2, top: 4 " + DIV + " 2 = ", 2, "Numerator over 2.", phase="substitute"),
        box("10 " + DIV + " 2 = ", 5, "Denominator over 2.", phase="substitute", done="P(A|B) = 2/5."),
    ],
})

silver.append({
    "display": venn("Girl", "Drama", 20, 60, 30, 40, 150, "Venn: girls and drama students, overlap 60", bold="both")
        + "<br>150 students: 80 girls, 90 do drama, 60 girls do drama. Find P(girl | does drama) as a simplified fraction.",
    "solutions": [2, 3], "calculator": False, "input_type": "fraction",
    "hint": "Given drama, divide the girls-who-do-drama by the total who do drama.",
    "misconceptions": [{"pattern": "used_total",
        "message": "60/150 divides by everyone. Given drama, divide by the 90 who do drama: 60/90 = 2/3.",
        "expect": [2, 5], "note": "divided by 150"}],
    "guided_steps": [
        say("Given drama, look only inside the drama group. P(girl|drama) = girls who do drama, over all who do drama."),
        box("Girls who do drama = ", 60, "The overlap of girl and drama."),
        box("Total who do drama (the given group) = ", 90, "All drama students."),
        box("So P(girl|drama) = 60/90. Simplify by 30, top: 60 " + DIV + " 30 = ", 2, "Top over 30.", say="Simplify by dividing by 30.", phase="substitute"),
        box("90 " + DIV + " 30 = ", 3, "Bottom over 30.", phase="substitute", done="P(girl|drama) = 2/3."),
    ],
})

gold = []

gold.append({
    "display": "P(A) = 0.4, P(B|A) = 0.5. Find P(A " + CAP + " B).",
    "solutions": [0.2], "calculator": False, "input_type": "single_value",
    "hint": "Multiply: P(A and B) = P(A) times P(B given A).",
    "misconceptions": [{"pattern": "added_not_multiplied",
        "message": "0.4 + 0.5 = 0.9 adds instead of multiplying. For P(A " + CAP + " B) multiply: 0.4 " + MUL + " 0.5 = 0.2.",
        "expect": [0.9], "note": "added"}],
    "guided_steps": [
        say("Multiply rule: P(A " + CAP + " B) = P(A) " + MUL + " P(B given A)."),
        box("P(A) = ", 0.4, "Given as 0.4."),
        box("P(B given A) = ", 0.5, "Given as 0.5."),
        box("Multiply them: 0.4 " + MUL + " 0.5 = ", 0.2, "Two fifths of a half.", say="Multiply them together.", phase="substitute"),
        box("Check: an overlap is smaller than each part. Type 0.2 again: ", 0.2, "It stays 0.2.", phase="substitute", done="P(A " + CAP + " B) = 0.2."),
    ],
})

gold.append({
    "display": venn("Tea", "Coffee", 45, 25, 15, 15, 100, "Venn: tea and coffee drinkers, overlap 25", bold="both")
        + "<br>100 people: 70 like tea, 40 like coffee, 25 like both. A person who likes tea is chosen. Find P(also likes coffee) as a simplified fraction.",
    "solutions": [5, 14], "calculator": False, "input_type": "fraction",
    "hint": "Given tea, divide the overlap by the tea total, not by 100.",
    "misconceptions": [{"pattern": "used_total",
        "message": "25/100 divides by everyone. Given tea, divide by the 70 who like tea: 25/70 = 5/14.",
        "expect": [1, 4], "note": "divided by 100"}],
    "guided_steps": [
        say("Given tea, look only inside the tea group. P(coffee|tea) = both, over the tea total."),
        box("Both tea and coffee = ", 25, "The overlap."),
        box("Tea total (the given group) = ", 70, "All who like tea."),
        box("So P(coffee|tea) = 25/70. Simplify by 5, top: 25 " + DIV + " 5 = ", 5, "Top over 5.", say="Simplify by dividing by 5.", phase="substitute"),
        box("70 " + DIV + " 5 = ", 14, "Bottom over 5.", phase="substitute", done="P(coffee|tea) = 5/14."),
    ],
})

gold.append({
    "display": "P(A|B) = 0.7, P(B) = 0.4. P(A|B') = 0.3, P(B') = 0.6. Find P(A).",
    "solutions": [0.46], "calculator": True, "input_type": "single_value",
    "hint": "Add both routes to A: through B and through not B.",
    "misconceptions": [{"pattern": "one_branch_only",
        "message": "0.7 " + MUL + " 0.4 = 0.28 is only the route through B. Add the other route: 0.28 + 0.3 " + MUL + " 0.6 = 0.46.",
        "expect": [0.28], "note": "one branch"}],
    "guided_steps": [
        say("A can happen through B or through not B. Total probability adds both routes."),
        box("Route through B: 0.7 " + MUL + " 0.4 = ", 0.28, "P(A|B) times P(B)."),
        box("Route through not B: 0.3 " + MUL + " 0.6 = ", 0.18, "P(A|B') times P(B')."),
        box("Add the two routes: 0.28 + 0.18 = ", 0.46, "Both ways of reaching A.", say="Add the two routes.", phase="substitute"),
        box("Check: the two routes cover everything, so this is P(A). Type it again: ", 0.46, "It stays 0.46.", phase="substitute", done="P(A) = 0.46."),
    ],
})

gold.append({
    "display": "P(A) = 0.3, P(B) = 0.6. A and B are independent. Find P(A' " + CAP + " B') as a simplified fraction.",
    "solutions": [7, 25], "calculator": False, "input_type": "fraction",
    "hint": "Independent neither: multiply the complements P(A') and P(B').",
    "misconceptions": [{"pattern": "used_events",
        "message": "0.3 " + MUL + " 0.6 = 0.18 = 9/50 multiplies the events, not their complements. Use P(A') " + MUL + " P(B') = 0.7 " + MUL + " 0.4 = 0.28 = 7/25.",
        "expect": [9, 50], "note": "used events"}],
    "guided_steps": [
        say("Neither event means A' and B'. For independent events, multiply the complements."),
        box("P(A') = 1 " + MINUS + " 0.3 = ", 0.7, "The complement of A."),
        box("P(B') = 1 " + MINUS + " 0.6 = ", 0.4, "The complement of B."),
        box("Independent, so multiply: 0.7 " + MUL + " 0.4 = ", 0.28, "Both complements together.", say="Independent, so multiply the complements.", phase="substitute"),
        box("0.28 = 28/100. Simplify by 4, top: 28 " + DIV + " 4 = ", 7, "Numerator over 4.", phase="substitute"),
        box("100 " + DIV + " 4 = ", 25, "Denominator over 4.", phase="substitute", done="P(A' " + CAP + " B') = 7/25."),
    ],
})

gold.append({
    "display": "P(A " + CUP + " B) = 0.85, P(A) = 0.6, P(B) = 0.5. Find P(A | B) as a simplified fraction.",
    "solutions": [1, 2], "calculator": False, "input_type": "fraction",
    "hint": "Find the overlap from the addition rule first, then divide by P(B).",
    "misconceptions": [{"pattern": "used_union",
        "message": "0.85/0.5 divides the union. First find the overlap 0.6 + 0.5 " + MINUS + " 0.85 = 0.25, then 0.25/0.5 = 1/2.",
        "expect": [17, 10], "note": "divided union"}],
    "guided_steps": [
        say("First find the overlap from the addition rule, then divide by P(B)."),
        box("P(A) + P(B) = 0.6 + 0.5 = ", 1.1, "Add the two sets."),
        box("Subtract the union: 1.1 " + MINUS + " 0.85 = ", 0.25, "This is P(A " + CAP + " B)."),
        box("Now the conditional: 0.25 " + DIV + " 0.5 = ", 0.5, "Overlap over the given set.", say="Divide the overlap by P(B).", phase="substitute"),
        box("Write 0.5 as a fraction. Numerator (0.5 = 1/2) = ", 1, "One half, top.", phase="substitute"),
        box("Denominator = ", 2, "Out of two.", phase="substitute", done="P(A|B) = 1/2."),
    ],
})

pd["problem_bank"] = {
    "bronze": bronze, "silver": silver, "gold": gold,
    "bronze_description": "Read and fill a Venn diagram: work from the intersection outward, then find a count or a simple probability over the total.",
    "silver_description": "Conditional probability and the addition rule: P(A|B) restricts to the given group, and P(A" + CUP + "B) = P(A) + P(B) " + MINUS + " P(A" + CAP + "B).",
    "gold_description": "Combine the rules: the multiplication rule, testing independence, and total probability across both branches.",
}

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
            "question": "40 people: 22 like tea, 16 like coffee, 8 like both. Find P(neither).",
            "steps": [
                {"label": "Overlap", "content": "both = 8"},
                {"label": "Only regions", "content": "tea only 14, coffee only 8"},
                {"label": "Neither", "content": "40 " + MINUS + " (14 + 8 + 8) = 10"},
                {"label": "Answer", "content": "P(neither) = 10/40 = 1/4", "isAnswer": True, "is_answer": True},
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
            "question": "40 people: 24 like tea, 16 like both tea and cake. Find P(cake | tea).",
            "steps": [
                {"label": "Given group", "content": "tea total = 24"},
                {"label": "Overlap", "content": "both = 16"},
                {"label": "Check", "content": "P(cake|tea) = 16/24"},
                {"label": "Answer", "content": "16/24 = 2/3", "isAnswer": True, "is_answer": True},
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
            "question": "P(A) = 0.3, P(B) = 0.5, independent. Find P(A " + CAP + " B).",
            "steps": [
                {"label": "Test", "content": "independent, so multiply"},
                {"label": "Multiply", "content": "0.3 " + MUL + " 0.5"},
                {"label": "Check", "content": "smaller than each part"},
                {"label": "Answer", "content": "P(A " + CAP + " B) = 0.15", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

pd["guided"] = {
    "opener": {
        "steps": [
            {"say": "Here are 8 friends. One loop is who swims, the other is who cycles. The numbers show how many are in each part.",
             "display": venn("Swim", "Cycle", 2, 3, 2, 1, 8, "Venn: 8 friends, swim and cycle loops")},
            box("How many swim in total (both parts of the swim loop)? ", 5, "Add the swim-only 2 and the overlap 3."),
            box("Of those swimmers, how many also cycle? ", 3, "The overlap, inside both loops."),
            {"say": "Pick a swimmer at random: 3 of the 5 also cycle, so the chance is \\(\\tfrac{3}{5}\\). You just found a <strong>conditional</strong> probability: you looked only inside the swim group. That is P(cycle given swim)."},
        ],
    },
    "teach": {
        "bronze": {
            "display": venn("Bike", "Scooter", 16, 12, 8, "?", 45, "Venn: bike and scooter owners, overlap 12", bold="neither")
                + "<br>45 people: 28 own a bike, 20 own a scooter, 12 own both. How many own neither?",
            "steps": [
                say("Fill from the overlap out, then the total minus the circles gives neither."),
                box("Both bike and scooter = ", 12, "Given as 12."),
                box("Bike only: 28 " + MINUS + " 12 = ", 16, "Take the overlap off the bike total."),
                box("Scooter only: 20 " + MINUS + " 12 = ", 8, "Take the overlap off the scooter total."),
                box("In the circles: 16 + 12 + 8 = ", 36, "Everyone who owns at least one."),
                box("Neither: 45 " + MINUS + " 36 = ", 9, "The rest of the group.", done="9 own neither. Total minus the circles, every time."),
            ],
        },
        "silver": {
            "display": venn("Tea", "Biscuits", 18, 12, 8, 12, 50, "Venn: tea and biscuits, overlap 12", bold="both")
                + "<br>50 people: 30 like tea, 20 like biscuits, 12 like both. Find P(biscuits given tea).",
            "steps": [
                say("Given tea, only look inside the tea group. The given total is the denominator."),
                box("Both tea and biscuits = ", 12, "The overlap."),
                box("Tea total (the given group) = ", 30, "All who like tea."),
                box("So P(biscuits|tea) = 12/30. Simplify by 6, top: 12 " + DIV + " 6 = ", 2, "Top over 6."),
                box("30 " + DIV + " 6 = ", 5, "Bottom over 6.", done="P(biscuits|tea) = 2/5. The given group is the denominator: that is the whole move."),
            ],
        },
        "gold": {
            "display": venn("A", "B", 0.2, 0.3, 0.3, 0.2, 1, "Venn: independent events A and B as probabilities", bold="both")
                + "<br>P(A) = 0.5, P(B) = 0.6, and A and B are independent. Find P(A " + CUP + " B).",
            "steps": [
                say("Independent, so the overlap is the product. Then use the addition rule for the union."),
                box("P(A " + CAP + " B) = 0.5 " + MUL + " 0.6 = ", 0.3, "Multiply for independent events."),
                box("P(A) + P(B) = 0.5 + 0.6 = ", 1.1, "Add the two."),
                box("Union: 1.1 " + MINUS + " 0.3 = ", 0.8, "Subtract the overlap once."),
                box("Check: A only 0.2, both 0.3, B only 0.3 add to 0.8. Type it: ", 0.8, "Read from the Venn.", done="P(A " + CUP + " B) = 0.8. Independent gives the overlap by multiplying: that is the new move."),
            ],
        },
    },
}

OUT = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_guided\lesson_maths-eduqas_probability-statistics-L02.json"
with io.open(OUT, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("wrote", OUT)
print("bronze", len(bronze), "silver", len(silver), "gold", len(gold))
