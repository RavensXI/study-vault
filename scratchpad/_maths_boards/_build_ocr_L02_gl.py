# -*- coding: utf-8 -*-
import json, io

LIVE = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_live_ocr_L02.json"
OUT  = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_guided/lesson_maths-ocr_probability-statistics-L02.json"

pd = json.load(io.open(LIVE, encoding="utf-8"))

# ---------- SVG helpers (theme-safe, currentColor, Inter) ----------
def T(x, y, val, bold=False, size=12, anchor="middle"):
    w = ' font-weight="700"' if bold else ''
    return ('<text x="%s" y="%s" font-family="Inter, sans-serif" font-size="%s" '
            'fill="currentColor" text-anchor="%s"%s>%s</text>') % (x, y, size, anchor, w, val)

def venn(aria, left_lbl, right_lbl, lo, both, ro, neither, total, bold=None):
    if bold is None:
        bold = {"both"}
    s = ('<svg viewBox="0 0 260 180" role="img" aria-label="%s" style="max-width:260px">' % aria)
    s += '<rect x="8" y="10" width="244" height="150" rx="6" fill="none" stroke="currentColor" stroke-width="1"/>'
    s += '<circle cx="100" cy="90" r="52" fill="#60a5fa" fill-opacity="0.15" stroke="currentColor" stroke-width="1"/>'
    s += '<circle cx="160" cy="90" r="52" fill="#f59e0b" fill-opacity="0.15" stroke="currentColor" stroke-width="1"/>'
    s += T(72, 54, left_lbl, bold=True)
    s += T(188, 54, right_lbl, bold=True)
    s += T(76, 96, lo, bold=("lo" in bold))
    s += T(130, 96, both, bold=("both" in bold))
    s += T(184, 96, ro, bold=("ro" in bold))
    s += T(236, 150, neither, bold=("neither" in bold))
    s += T(14, 26, "Total: %s" % total, size=11, anchor="start")
    s += '</svg>'
    return s

def venn_disjoint(aria, left_lbl, right_lbl, lval, rval, neither, total):
    s = ('<svg viewBox="0 0 260 170" role="img" aria-label="%s" style="max-width:260px">' % aria)
    s += '<rect x="8" y="10" width="244" height="140" rx="6" fill="none" stroke="currentColor" stroke-width="1"/>'
    s += '<circle cx="70" cy="88" r="42" fill="#60a5fa" fill-opacity="0.15" stroke="currentColor" stroke-width="1"/>'
    s += '<circle cx="190" cy="88" r="42" fill="#f59e0b" fill-opacity="0.15" stroke="currentColor" stroke-width="1"/>'
    s += T(70, 50, left_lbl, bold=True)
    s += T(190, 50, right_lbl, bold=True)
    s += T(70, 94, lval)
    s += T(190, 94, rval)
    s += T(236, 142, neither, size=11)
    s += T(14, 26, "Total: %s" % total, size=11, anchor="start")
    s += '</svg>'
    return s

def box(pre, answer, hint, phase=None, say=None, done=None):
    d = {"pre": pre, "post": "", "answer": answer, "hint": hint}
    if phase: d["phase"] = phase
    if say: d["say"] = say
    if done: d["done"] = done
    return d
def sayonly(s):
    return {"say": s}

# ===== BRONZE =====
bronze = []
bronze.append({
 "display": venn("Venn: football and rugby, 60 students", "Football", "Rugby", 20, 15, 13, 12, 60)
   + "<br>60 students: 35 play football, 28 play rugby, 15 play both. How many play at least one?",
 "solutions": [48], "calculator": False, "input_type": "single_value",
 "misconceptions": [{"pattern":"forgot_overlap","message":"35 + 28 = 63 counts the 15 who play both twice. Subtract the overlap once: 35 + 28 − 15 = 48.","expect":[63],"note":"no subtract"}],
 "hint": "Add both totals, then subtract the overlap once so the 15 are not counted twice.",
 "guided_steps": [
   sayonly("Add both totals, then remove the overlap once so no one is counted twice."),
   box("Football total = ", 35, "Given as 35."),
   box("Rugby total = ", 28, "Given as 28."),
   box("Add them: 35 + 28 = ", 63, "Both totals together."),
   box("63 − 15 = ", 48, "Remove the double count.", phase="substitute", say="The 15 who play both were counted twice. Subtract the overlap once."),
   box("Check by regions: football only 20, both 15, rugby only 13 add to ", 48, "The three inside regions.", phase="substitute", done="48 play at least one.")
 ]})
bronze.append({
 "display": venn("Venn: football and rugby, neither unknown", "Football", "Rugby", 20, 15, 13, "?", 60, bold={"neither"})
   + "<br>Same data (60, 35, 28, 15). How many play neither?",
 "solutions": [12], "calculator": False, "input_type": "single_value",
 "misconceptions": [{"pattern":"gave_at_least_one","message":"48 is how many play at least one. Neither is the rest of the 60: 60 − 48 = 12.","expect":[48],"note":"gave at least one"}],
 "hint": "Find how many play at least one, then subtract from 60.",
 "guided_steps": [
   sayonly("Neither is the whole group minus those who play at least one."),
   box("Football only: 35 − 15 = ", 20, "Take the overlap off football."),
   box("Rugby only: 28 − 15 = ", 13, "Take the overlap off rugby."),
   box("At least one: 20 + 15 + 13 = ", 48, "The three inside regions."),
   box("60 − 48 = ", 12, "The whole group minus at least one.", phase="substitute", say="Neither is the rest of the 60."),
   box("Check: 20 + 15 + 13 + 12 = ", 60, "All four regions total 60.", phase="substitute", done="12 play neither.")
 ]})
bronze.append({
 "display": venn("Venn: football and rugby, only football unknown", "Football", "Rugby", "?", 15, 13, 12, 60, bold={"lo"})
   + "<br>Same data. How many play ONLY football?",
 "solutions": [20], "calculator": False, "input_type": "single_value",
 "misconceptions": [{"pattern":"used_total","message":"35 is all who play football. Only football removes the 15 who also play rugby: 35 − 15 = 20.","expect":[35],"note":"gave n(football)"}],
 "hint": "Only football is the 35 minus the 15 who also play rugby.",
 "guided_steps": [
   sayonly("Only football means football but not the overlap."),
   box("Football total = ", 35, "Given as 35."),
   box("Both football and rugby = ", 15, "The overlap."),
   box("35 − 15 = ", 20, "Take the 15 off.", phase="substitute", say="Only football removes the overlap from the football total."),
   box("Check: only football plus both = 20 + 15 = ", 35, "Should return the football total.", phase="substitute", done="20 play only football.")
 ]})
bronze.append({
 "display": venn("Venn: sport and music, neither unknown", "Sport", "Music", 40, 20, 25, "?", 100, bold={"neither"})
   + "<br>100 students: 60 play sport, 45 play music, 20 do both. How many do neither?",
 "solutions": [15], "calculator": False, "input_type": "single_value",
 "misconceptions": [{"pattern":"gave_at_least_one","message":"85 play at least one of sport or music. Neither is the rest: 100 − 85 = 15.","expect":[85],"note":"gave at least one"}],
 "hint": "Add sport and music, subtract the overlap, then take that from 100.",
 "guided_steps": [
   sayonly("Add sport and music, subtract the overlap, then take that from 100."),
   box("Sport plus music: 60 + 45 = ", 105, "Add both totals."),
   box("Subtract the overlap once: 105 − 20 = ", 85, "The 20 both were counted twice."),
   box("100 − 85 = ", 15, "The whole group minus at least one.", phase="substitute", say="Neither is the rest of the 100."),
   box("Check: sport only 40, music only 25, both 20, neither 15 add to ", 100, "All four regions.", phase="substitute", done="15 do neither.")
 ]})
bronze.append({
 "display": venn("Venn: events A and B as probabilities", "A", "B", 0.45, 0.15, 0.15, 0.25, 1)
   + "<br>P(A) = 0.6, P(B) = 0.3, P(A∩B) = 0.15. Find P(A∪B).",
 "solutions": [0.75], "calculator": False, "input_type": "single_value",
 "misconceptions": [{"pattern":"add_only","message":"0.6 + 0.3 = 0.9 counts the 0.15 overlap twice. Subtract it once: 0.9 − 0.15 = 0.75.","expect":[0.9],"note":"no subtract"}],
 "hint": "Add P(A) and P(B), then subtract the overlap once.",
 "guided_steps": [
   sayonly("Union adds the two sets, then removes the overlap once."),
   box("P(A) + P(B) = 0.6 + 0.3 = ", 0.9, "Add the two sets."),
   box("The overlap P(A∩B) = ", 0.15, "Given as 0.15."),
   box("0.9 − 0.15 = ", 0.75, "Remove the double count.", phase="substitute", say="Subtract the overlap once."),
   box("Check by regions: 0.45 + 0.15 + 0.15 = ", 0.75, "A only, both, B only.", phase="substitute", done="P(A∪B) = 0.75.")
 ]})
bronze.append({
 "display": venn("Venn: cats and dogs, cats only unknown", "Cats", "Dogs", "?", 10, 15, 3, 40, bold={"lo"})
   + "<br>40 students: 22 like cats, 25 like dogs, 10 like both. P(likes cats only) out of 40.",
 "solutions": [3,10], "calculator": False, "input_type": "fraction",
 "misconceptions": [{"pattern":"include_both","message":"22/40 counts the 10 who like both. Cats only is 22 − 10 = 12, so 12/40 = 3/10.","expect":[11,20],"note":"used n(cats)"}],
 "hint": "Cats only is 22 minus the 10 both, then put it over 40.",
 "guided_steps": [
   sayonly("Cats only means cats but not the overlap. Find that count over the total."),
   box("Cats only: 22 − 10 = ", 12, "Take the 10 both off."),
   box("Total students = ", 40, "Out of 40."),
   box("12 ÷ 4 = ", 3, "Top over 4.", phase="substitute", say="So P(cats only) = 12/40. Simplify by dividing by 4."),
   box("40 ÷ 4 = ", 10, "Bottom over 4.", phase="substitute", done="P(cats only) = 3/10.")
 ]})
bronze.append({
 "display": venn("Venn: French and German, only German unknown", "French", "German", 10, 8, "?", 5, 30, bold={"ro"})
   + "<br>30 students: 18 study French, 15 study German, 8 both. How many study only German?",
 "solutions": [7], "calculator": False, "input_type": "single_value",
 "misconceptions": [{"pattern":"used_total","message":"15 is all who study German. Only German removes the 8 who also study French: 15 − 8 = 7.","expect":[15],"note":"gave n(German)"}],
 "hint": "Only German is 15 minus the 8 who also study French.",
 "guided_steps": [
   sayonly("Only German means German but not the overlap."),
   box("German total = ", 15, "Given as 15."),
   box("Both French and German = ", 8, "The overlap."),
   box("15 − 8 = ", 7, "Take the 8 off.", phase="substitute", say="Only German removes the overlap from the German total."),
   box("Check: only German plus both = 7 + 8 = ", 15, "Should return the German total.", phase="substitute", done="7 study only German.")
 ]})
bronze.append({
 "display": "P(A) = 0.5, P(A∩B) = 0.2. Find P(A only, not B).",
 "solutions": [0.3], "calculator": False, "input_type": "single_value",
 "misconceptions": [{"pattern":"forgot_subtract","message":"0.5 is all of A. A only removes the overlap: 0.5 − 0.2 = 0.3.","expect":[0.5],"note":"gave P(A)"}],
 "hint": "A only is P(A) minus the overlap P(A and B).",
 "guided_steps": [
   sayonly("A only is all of A with the overlap removed."),
   box("All of A, P(A) = ", 0.5, "Given as 0.5."),
   box("The overlap P(A∩B) = ", 0.2, "Given as 0.2."),
   box("0.5 − 0.2 = ", 0.3, "What is left of A.", phase="substitute", say="Take the overlap off P(A)."),
   box("Check: A only plus overlap = 0.3 + 0.2 = ", 0.5, "Should return P(A).", phase="substitute", done="P(A only) = 0.3.")
 ]})

# ===== SILVER =====
silver = []
silver.append({
 "display": venn("Venn: sport and music, 100 students", "Sport", "Music", 40, 20, 25, 15, 100)
   + "<br>100 students: 60 play sport, 45 play music, 20 both. P(music | sport).",
 "solutions": [1,3], "calculator": False, "input_type": "fraction",
 "misconceptions": [{"pattern":"used_total","message":"20/100 divides by everyone. Given sport, divide by the 60 who play sport: 20/60 = 1/3.","expect":[1,5],"note":"divided by 100"}],
 "hint": "Given sport, divide the overlap by the sport total, not by 100.",
 "guided_steps": [
   sayonly("Given sport, look only inside the sport group. Divide the overlap by the sport total."),
   box("Both sport and music = ", 20, "The overlap."),
   box("Sport total (the given group) = ", 60, "All who play sport."),
   box("20 ÷ 20 = ", 1, "Top over 20.", phase="substitute", say="So P(music|sport) = 20/60. Simplify by dividing by 20."),
   box("60 ÷ 20 = ", 3, "Bottom over 20.", phase="substitute", done="P(music|sport) = 1/3.")
 ]})
silver.append({
 "display": venn("Venn: events A and B as probabilities", "A", "B", 0.4, 0.3, 0.2, 0.1, 1)
   + "<br>P(A) = 0.7, P(B) = 0.5, P(A∩B) = 0.3. Find P(B|A).",
 "solutions": [0.429], "calculator": True, "input_type": "single_value",
 "misconceptions": [{"pattern":"divided_by_wrong","message":"0.3/0.5 = 0.6 divides by P(B). For P(B|A) divide by P(A): 0.3/0.7 ≈ 0.429.","expect":[0.6],"note":"divided by P(B)"}],
 "hint": "For P(B given A), divide the overlap by P(A).",
 "guided_steps": [
   sayonly("For P(B given A), divide the overlap by P(A)."),
   box("The overlap P(A∩B) = ", 0.3, "Given as 0.3."),
   box("The given group P(A) = ", 0.7, "We are told A has happened."),
   box("0.3 ÷ 0.7 = ", 0.429, "About 0.4286, rounded to 3 d.p.", phase="substitute", say="Divide the overlap by P(A). Round to 3 decimal places."),
   box("Check: 0.429 × 0.7 ≈ 0.3, the overlap. Type the answer again: ", 0.429, "It stays 0.429.", phase="substitute", done="P(B|A) ≈ 0.429.")
 ]})
silver.append({
 "display": venn("Venn: tea and coffee, 80 people", "Tea", "Coffee", 35, 15, 20, 10, 80)
   + "<br>80 people: 50 tea, 35 coffee, 15 both. P(tea | coffee).",
 "solutions": [3,7], "calculator": False, "input_type": "fraction",
 "misconceptions": [{"pattern":"used_total","message":"15/80 divides by everyone. Given coffee, divide by the 35 who drink coffee: 15/35 = 3/7.","expect":[3,16],"note":"divided by 80"}],
 "hint": "Given coffee, divide the overlap by the coffee total, not by 80.",
 "guided_steps": [
   sayonly("Given coffee, look only inside the coffee group. Divide the overlap by the coffee total."),
   box("Both tea and coffee = ", 15, "The overlap."),
   box("Coffee total (the given group) = ", 35, "All who drink coffee."),
   box("15 ÷ 5 = ", 3, "Top over 5.", phase="substitute", say="So P(tea|coffee) = 15/35. Simplify by dividing by 5."),
   box("35 ÷ 5 = ", 7, "Bottom over 5.", phase="substitute", done="P(tea|coffee) = 3/7.")
 ]})
silver.append({
 "display": "P(A∪B) = 0.8, P(A) = 0.5, P(B) = 0.4. Find P(A∩B).",
 "solutions": [0.1], "calculator": False, "input_type": "single_value",
 "misconceptions": [{"pattern":"assumed_independent","message":"0.5 × 0.4 = 0.2 assumes independence. Use the addition rule: 0.5 + 0.4 − 0.8 = 0.1.","expect":[0.2],"note":"multiplied"}],
 "hint": "Rearrange the addition rule: overlap = P(A) + P(B) − P(A∪B).",
 "guided_steps": [
   sayonly("Rearrange the addition rule: the overlap equals P(A) + P(B) minus the union."),
   box("P(A) + P(B) = 0.5 + 0.4 = ", 0.9, "Add the two sets."),
   box("The union P(A∪B) = ", 0.8, "Given as 0.8."),
   box("0.9 − 0.8 = ", 0.1, "This gives the overlap.", phase="substitute", say="Subtract the union from that sum."),
   box("Check: 0.5 + 0.4 − 0.1 = 0.8, the union. Type the overlap again: ", 0.1, "It stays 0.1.", phase="substitute", done="P(A∩B) = 0.1.")
 ]})
silver.append({
 "display": venn_disjoint("Two separate circles: mutually exclusive events A and B", "A", "B", 0.3, 0.4, "neither 0.3", 1)
   + "<br>Events A and B are mutually exclusive. P(A) = 0.3, P(B) = 0.4. P(A∪B)?",
 "solutions": [0.7], "calculator": False, "input_type": "single_value",
 "misconceptions": [{"pattern":"assumed_overlap","message":"Mutually exclusive means the events cannot both happen, so P(A∩B) = 0, not 0.3 × 0.4. Then P(A∪B) = 0.3 + 0.4 = 0.7.","expect":[0.58],"note":"subtracted 0.12"}],
 "hint": "Mutually exclusive means the overlap is zero, so just add.",
 "guided_steps": [
   sayonly("Mutually exclusive means the events cannot both happen, so the overlap is zero."),
   box("The overlap P(A∩B) for mutually exclusive events = ", 0, "They never happen together."),
   box("P(A) + P(B) = 0.3 + 0.4 = ", 0.7, "Add the two."),
   box("0.7 − 0 = ", 0.7, "Nothing to remove.", phase="substitute", say="With no overlap to subtract, the union is just the sum."),
   box("Check: the two separate slices give 0.3 + 0.4 = ", 0.7, "Read from the two circles.", phase="substitute", done="P(A∪B) = 0.7.")
 ]})
silver.append({
 "display": "Are A and B independent if P(A) = 0.5, P(B) = 0.4, P(A∩B) = 0.2? Enter 1 yes, 0 no.",
 "solutions": [1], "calculator": False, "input_type": "single_value",
 "misconceptions": [{"pattern":"wrong_test","message":"0.5 × 0.4 = 0.2, which equals P(A∩B), so the events ARE independent. Enter 1.","expect":[0],"note":"chose no"}],
 "hint": "Independent when P(A) times P(B) equals P(A and B).",
 "guided_steps": [
   sayonly("Independent when P(A) × P(B) equals P(A∩B)."),
   box("P(A) × P(B) = 0.5 × 0.4 = ", 0.2, "Multiply the two."),
   box("The given overlap P(A∩B) = ", 0.2, "Given as 0.2."),
   box("They are equal, so enter 1 for yes: ", 1, "0.2 = 0.2, so yes.", phase="substitute", say="Compare the product with the overlap."),
   box("Check: independent needs 0.5 × 0.4 = 0.2 = P(A∩B). Enter 1 again: ", 1, "It stays 1.", phase="substitute", done="Yes, independent, so 1.")
 ]})
silver.append({
 "display": venn("Venn: bus and walk, 120 students", "Bus", "Walk", 50, 20, 35, 15, 120)
   + "<br>120 students: 70 bus, 55 walk, 20 both. P(walk | not bus).",
 "solutions": [7,10], "calculator": False, "input_type": "fraction",
 "misconceptions": [{"pattern":"used_total","message":"35/120 divides by everyone. Restrict to the 50 who do not take the bus: 35/50 = 7/10.","expect":[7,24],"note":"divided by 120"}],
 "hint": "Not bus is 120 − 70; walkers among them is 55 − 20; then divide.",
 "guided_steps": [
   sayonly("Given not bus, restrict to those who do not take the bus, then find the walkers among them."),
   box("Not bus: 120 − 70 = ", 50, "Everyone who does not take the bus."),
   box("Walk and not bus: 55 − 20 = ", 35, "Walkers, minus the 20 who also take the bus."),
   box("35 ÷ 5 = ", 7, "Top over 5.", phase="substitute", say="So P(walk|not bus) = 35/50. Simplify by dividing by 5."),
   box("50 ÷ 5 = ", 10, "Bottom over 5.", phase="substitute", done="P(walk|not bus) = 7/10.")
 ]})

# ===== GOLD =====
gold = []
gold.append({
 "display": "P(A|B) = 0.6, P(B) = 0.5. Find P(A∩B).",
 "solutions": [0.3], "calculator": False, "input_type": "single_value",
 "misconceptions": [{"pattern":"added_not_multiplied","message":"0.6 + 0.5 = 1.1 adds instead of multiplying. P(A∩B) = P(A|B) × P(B) = 0.6 × 0.5 = 0.3.","expect":[1.1],"note":"added"}],
 "hint": "Multiply: P(A and B) = P(A given B) × P(B).",
 "guided_steps": [
   sayonly("Multiply rule: P(A∩B) = P(A|B) × P(B)."),
   box("P(A|B) = ", 0.6, "Given as 0.6."),
   box("P(B) = ", 0.5, "Given as 0.5."),
   box("0.6 × 0.5 = ", 0.3, "Six tenths of a half.", phase="substitute", say="Multiply them together."),
   box("Check: an overlap is smaller than each part. Type 0.3 again: ", 0.3, "It stays 0.3.", phase="substitute", done="P(A∩B) = 0.3.")
 ]})
gold.append({
 "display": "P(A) = 0.4, P(B|A) = 0.6. Find P(A∩B).",
 "solutions": [0.24], "calculator": False, "input_type": "single_value",
 "misconceptions": [{"pattern":"added_not_multiplied","message":"0.4 + 0.6 = 1 adds instead of multiplying. P(A∩B) = P(B|A) × P(A) = 0.6 × 0.4 = 0.24.","expect":[1.0],"note":"added"}],
 "hint": "Multiply: P(A and B) = P(B given A) × P(A).",
 "guided_steps": [
   sayonly("Multiply rule: P(A∩B) = P(B|A) × P(A)."),
   box("P(B|A) = ", 0.6, "Given as 0.6."),
   box("P(A) = ", 0.4, "Given as 0.4."),
   box("0.6 × 0.4 = ", 0.24, "Six tenths of 0.4.", phase="substitute", say="Multiply them together."),
   box("Check: the overlap is smaller than each part. Type 0.24 again: ", 0.24, "It stays 0.24.", phase="substitute", done="P(A∩B) = 0.24.")
 ]})
gold.append({
 "display": venn("Venn: A-level maths and physics, 200 students", "Maths", "Physics", 50, 50, 30, 70, 200)
   + "<br>200 students: 100 A-level maths, 80 A-level physics, 50 both. A student who does physics is chosen. P(also does maths).",
 "solutions": [5,8], "calculator": False, "input_type": "fraction",
 "misconceptions": [{"pattern":"used_total","message":"50/200 divides by everyone. Given physics, divide by the 80 who do physics: 50/80 = 5/8.","expect":[1,4],"note":"divided by 200"}],
 "hint": "Given physics, divide the both count by the physics total, not by 200.",
 "guided_steps": [
   sayonly("Given physics, look only inside the physics group. Divide the both count by the physics total."),
   box("Both maths and physics = ", 50, "The overlap."),
   box("Physics total (the given group) = ", 80, "All who do physics."),
   box("50 ÷ 10 = ", 5, "Top over 10.", phase="substitute", say="So P(maths|physics) = 50/80. Simplify by dividing by 10."),
   box("80 ÷ 10 = ", 8, "Bottom over 10.", phase="substitute", done="P(maths|physics) = 5/8.")
 ]})
gold.append({
 "display": "P(A) = 0.3, P(B) = 0.6, events independent. P(neither A nor B)?",
 "solutions": [0.28], "calculator": True, "input_type": "single_value",
 "misconceptions": [{"pattern":"used_events","message":"0.3 × 0.6 = 0.18 multiplies the events. For neither, multiply the complements: P(A')×P(B') = 0.7 × 0.4 = 0.28.","expect":[0.18],"note":"used events"}],
 "hint": "For neither of two independent events, multiply the complements P(A') and P(B').",
 "guided_steps": [
   sayonly("Neither means not A and not B. For independent events, multiply the complements."),
   box("P(A') = 1 − 0.3 = ", 0.7, "The complement of A."),
   box("P(B') = 1 − 0.6 = ", 0.4, "The complement of B."),
   box("0.7 × 0.4 = ", 0.28, "Both complements together.", phase="substitute", say="Independent, so multiply the complements."),
   box("Check: overlap 0.18, A only 0.12, B only 0.42, neither 0.28 add to ", 1, "All four regions total 1.", phase="substitute", done="P(neither) = 0.28.")
 ]})
gold.append({
 "display": venn("Venn: events A and B, B only unknown", "A", "B", 0.4, 0.2, "?", 0.1, 1, bold={"ro"})
   + "<br>P(A∪B) = 0.9, P(A) = 0.6, P(A∩B) = 0.2. Find P(B).",
 "solutions": [0.5], "calculator": False, "input_type": "single_value",
 "misconceptions": [{"pattern":"forgot_add_overlap","message":"0.9 − 0.6 = 0.3 forgets the shared part. P(B) = P(A∪B) − P(A) + P(A∩B) = 0.9 − 0.6 + 0.2 = 0.5.","expect":[0.3],"note":"did not add overlap back"}],
 "hint": "Rearrange the addition rule to make P(B) the subject.",
 "guided_steps": [
   sayonly("Rearrange the addition rule to make P(B) the subject: P(B) = P(A∪B) − P(A) + P(A∩B)."),
   box("P(A∪B) − P(A) = 0.9 − 0.6 = ", 0.3, "Start from the union."),
   box("The overlap P(A∩B) = ", 0.2, "Given as 0.2."),
   box("0.3 + 0.2 = ", 0.5, "Put the overlap back.", phase="substitute", say="Add the overlap back, because subtracting P(A) also removed the shared part."),
   box("Check: 0.6 + 0.5 − 0.2 = 0.9, the union. Type P(B) again: ", 0.5, "It stays 0.5.", phase="substitute", done="P(B) = 0.5.")
 ]})

pd["problem_bank"] = {
 "bronze": bronze, "silver": silver, "gold": gold,
 "bronze_description": "Read and fill a Venn diagram: work from the intersection outward, then find a count or a simple probability over the total.",
 "silver_description": "Conditional probability and the addition rule: P(A|B) restricts to the given group, and P(A∪B) = P(A) + P(B) − P(A∩B).",
 "gold_description": "Combine the rules: the multiplication rule, testing independence, and finding neither for independent events.",
}

pd["tier_guides"] = {
 "bronze": {
  "title": "Bronze: reading and filling a Venn diagram",
  "steps": [
   "Fill the <strong>intersection</strong> (the overlap) first.",
   "Subtract it from each set total to get the <strong>only</strong> regions.",
   "The rest of the group goes in <strong>neither</strong>, outside the circles.",
   "A probability is that region divided by the total."
  ],
  "example": {
   "question": "30 people: 16 like tea, 14 like coffee, 6 like both. Find P(neither).",
   "steps": [
    {"label":"Overlap","content":"both = 6"},
    {"label":"Only regions","content":"tea only 10, coffee only 8"},
    {"label":"Neither","content":"30 − (10 + 6 + 8) = 6"},
    {"label":"Answer","content":"P(neither) = 6/30 = 1/5","isAnswer":True,"is_answer":True}
   ]
  }
 },
 "silver": {
  "title": "Silver: conditional probability and the addition rule",
  "steps": [
   "Conditional: \\(P(A|B) = \\frac{n(A \\cap B)}{n(B)}\\), dividing by the <strong>given</strong> group.",
   "Addition rule: \\(P(A \\cup B) = P(A) + P(B) - P(A \\cap B)\\).",
   "Rearrange it to find any one missing part."
  ],
  "example": {
   "question": "50 people: 30 like tea, 18 like both tea and cake. Find P(cake | tea).",
   "steps": [
    {"label":"Given group","content":"tea total = 30"},
    {"label":"Overlap","content":"both = 18"},
    {"label":"Check","content":"P(cake|tea) = 18/30"},
    {"label":"Answer","content":"18/30 = 3/5","isAnswer":True,"is_answer":True}
   ]
  }
 },
 "gold": {
  "title": "Gold: independence and combined rules",
  "steps": [
   "Multiply: \\(P(A \\cap B) = P(B|A)\\,P(A)\\).",
   "Independent when \\(P(A) \\times P(B) = P(A \\cap B)\\).",
   "For neither of independent events, multiply \\(P(A')\\) and \\(P(B')\\)."
  ],
  "example": {
   "question": "P(A) = 0.4, P(B) = 0.5, independent. Find P(A ∩ B).",
   "steps": [
    {"label":"Test","content":"independent, so multiply"},
    {"label":"Multiply","content":"0.4 × 0.5"},
    {"label":"Check","content":"smaller than each part"},
    {"label":"Answer","content":"P(A ∩ B) = 0.2","isAnswer":True,"is_answer":True}
   ]
  }
 }
}

opener_svg = venn("Venn: 12 pupils, chess and art clubs", "Chess", "Art", 3, 3, 4, 2, 12)
pd["guided"] = {
 "opener": {
  "steps": [
   {"say": "Here are 12 pupils. One loop is the chess club, the other is the art club. The numbers show how many are in each part.",
    "display": opener_svg},
   {"pre": "How many are in the chess club in total (both parts of the chess loop)? ", "post": "", "answer": 6,
    "hint": "Add the chess-only 3 and the overlap 3."},
   {"pre": "Of those chess players, how many also do art? ", "post": "", "answer": 3,
    "hint": "The overlap, inside both loops."},
   {"say": "Pick a chess player at random: 3 of the 6 also do art, so the chance is \\(\\tfrac{3}{6} = \\tfrac{1}{2}\\). You just found a <strong>conditional</strong> probability by looking only inside the chess group. That is P(art given chess)."}
  ]
 },
 "teach": {
  "bronze": {
   "display": venn("Venn: guitar and piano, neither unknown", "Guitar", "Piano", 15, 10, 8, "?", 40, bold={"neither"})
     + "<br>40 students: 25 play guitar, 18 play piano, 10 play both. How many play neither?",
   "steps": [
    sayonly("Fill from the overlap out, then the total minus the circles gives neither."),
    box("Both guitar and piano = ", 10, "Given as 10."),
    box("Guitar only: 25 − 10 = ", 15, "Take the overlap off guitar."),
    box("Piano only: 18 − 10 = ", 8, "Take the overlap off piano."),
    box("In the circles: 15 + 10 + 8 = ", 33, "Everyone who plays at least one."),
    box("Neither: 40 − 33 = ", 7, "The rest of the group.", done="7 play neither. Total minus the circles, every time.")
   ]
  },
  "silver": {
   "display": venn("Venn: burgers and salad, 50 people", "Burger", "Salad", 18, 12, 8, 12, 50)
     + "<br>50 people: 30 like burgers, 20 like salad, 12 like both. Find P(salad given burger).",
   "steps": [
    sayonly("Given burger, only look inside the burger group. The given total is the denominator."),
    box("Both burger and salad = ", 12, "The overlap."),
    box("Burger total (the given group) = ", 30, "All who like burgers."),
    box("So P(salad|burger) = 12/30. Simplify by 6, top: 12 ÷ 6 = ", 2, "Top over 6."),
    box("30 ÷ 6 = ", 5, "Bottom over 6.", done="P(salad|burger) = 2/5. The given group is the denominator: that is the whole move.")
   ]
  },
  "gold": {
   "display": venn("Venn: independent events A and B as probabilities", "A", "B", 0.3, 0.3, 0.2, 0.2, 1)
     + "<br>P(A) = 0.6, P(B) = 0.5, and A and B are independent. Find P(A∪B).",
   "steps": [
    sayonly("Independent, so the overlap is the product. Then use the addition rule for the union."),
    box("P(A∩B) = 0.6 × 0.5 = ", 0.3, "Multiply for independent events."),
    box("P(A) + P(B) = 0.6 + 0.5 = ", 1.1, "Add the two."),
    box("Union: 1.1 − 0.3 = ", 0.8, "Subtract the overlap once."),
    box("Check: A only 0.3, both 0.3, B only 0.2 add to ", 0.8, "Read from the Venn.", done="P(A∪B) = 0.8. Independent gives the overlap by multiplying: that is the new move.")
   ]
  }
 }
}

pd["method_card"] = {
 "title": "Venn Diagrams & Conditional Probability",
 "steps": [
  "Fill the intersection first, then the 'only' regions, then neither.",
  "P(A∪B) = P(A) + P(B) − P(A∩B).",
  "P(A|B) = n(A∩B) / n(B): divide by the given group.",
  "Independent: P(A∩B) = P(A) × P(B)."
 ],
 "content": "<p><strong>Venn diagrams</strong> show overlapping sets. \\(P(A \\cup B) = P(A) + P(B) - P(A \\cap B)\\). The region outside both circles is P(neither).</p><p><strong>Conditional:</strong> \\(P(A | B) = \\frac{P(A \\cap B)}{P(B)}\\), the probability of A given B has occurred. Fill a Venn from the intersection outward; all regions total the whole group.</p>",
 "example": "<p><strong>40 students: 25 play football, 18 play tennis, 10 play both. P(football | plays tennis)?</strong></p><p>P(F|T) = 10/18 = 5/9.</p>"
}

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("written", OUT)
print("bronze", len(bronze), "silver", len(silver), "gold", len(gold))
