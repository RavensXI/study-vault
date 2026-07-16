# -*- coding: utf-8 -*-
import json, io

M = "−"  # proper minus
pd = json.load(io.open("_live_L01.json", encoding="utf-8"))

def box(pre, answer, hint, post="", say=None, phase=None, done=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if phase is not None: d["phase"] = phase
    if done is not None: d["done"] = done
    return d

def say(text):
    return {"say": text}

# ---------- helper to set a problem's guided fields ----------
def setp(tier, idx, hint, mis, steps, display=None, solutions=None):
    p = pd["problem_bank"][tier][idx]
    if display is not None: p["display"] = display
    if solutions is not None: p["solutions"] = solutions
    p["hint"] = hint
    p["misconceptions"] = mis
    p["guided_steps"] = steps
    # verify: collect numeric box answers
    return p

def mc(pattern, expect, message, note=None):
    d = {"pattern": pattern, "expect": expect, "message": message}
    if note is not None: d["note"] = note
    return d

# =================== BRONZE ===================
setp("bronze", 0,
  "Count how many of 1 to 5 are even, then divide by 5.",
  [mc("counts_odd", 0.6, "0.6 is P(odd): {1, 3, 5} is three outcomes. Even means {2, 4}, so P(even) = 2 out of 5 = 0.4.")],
  [ say("List the outcomes: 1, 2, 3, 4, 5. The even ones are 2 and 4."),
    box("How many outcomes are even? ", 2, "Just 2 and 4."),
    box("How many outcomes in total? ", 5, "Count them all: 1 to 5.", phase="substitute"),
    box("P(even) as a decimal = 2 ÷ 5 = ", 0.4, "Two divided by five.", phase="substitute"),
    box("Check with the opposite: the three odd numbers give P(odd) = 3 ÷ 5 = ", 0.6,
        "Three odds out of five.", phase="substitute", done="0.4 + 0.6 = 1, the whole spinner, so 0.4 is right.") ])

setp("bronze", 1,
  "Rain and no rain add to 1, so subtract from 1.",
  [mc("repeats_given", 0.3, "0.3 is P(rain) itself. 'No rain' is the opposite: 1 − 0.3 = 0.7.")],
  [ say("Rain and no rain are opposites, and opposites always add up to 1."),
    box("Write down P(rain) = ", 0.3, "It is given in the question."),
    box("P(no rain) = 1 − 0.3 = ", 0.7, "One take away nought point three.", phase="substitute"),
    box("Check the two add to 1: 0.7 + 0.3 = ", 1, "Add them up.", phase="substitute",
        done="They fill the whole day, so 0.7 is right.") ])

setp("bronze", 2,
  "Put red over the total number of balls, then simplify.",
  [mc("part_to_part", [1,4], "1/4 compares red to blue (2/8). Probability compares red to the TOTAL: 2 out of 10 = 1/5.")],
  [ say("P(red) is the number of red balls over the total number of balls."),
    box("Total balls = 2 + 8 = ", 10, "Add red and blue."),
    box("Red balls (the top of the fraction) = ", 2, "Just the reds.", phase="substitute"),
    box("So P(red) = 2/10. Simplify by 2: the top 2 ÷ 2 = ", 1, "Two divided by two.", phase="substitute"),
    box("and the bottom 10 ÷ 2 = ", 5, "Ten divided by two.", phase="substitute",
        done="1/5, which is the simplified answer.") ])

setp("bronze", 3,
  "Multiply the two halves: it is an AND.",
  [mc("single_event", 0.5, "0.5 is the chance of heads on ONE toss. For both, multiply: 0.5 × 0.5 = 0.25.")],
  [ say("Two tosses. P(heads) each time is a half, 0.5. 'Both' means AND, so multiply."),
    box("P(heads) on one toss, as a decimal = ", 0.5, "A half."),
    box("Second toss is also 0.5. Multiply: 0.5 × 0.5 = ", 0.25, "Half of a half.", phase="substitute"),
    box("Check by listing HH, HT, TH, TT: only HH is both heads, so 1 ÷ 4 = ", 0.25,
        "One out of four.", phase="substitute", done="Same answer, 0.25.") ])

setp("bronze", 4,
  "Not a 6 covers five of the six faces.",
  [mc("gives_the_event", [1,6], "1/6 is P(6). 'Not 6' is every other face: 1 − 1/6 = 5/6.")],
  [ say("'Not 6' is the opposite of rolling a 6, and opposites subtract from 1."),
    box("A dice has 6 faces. How many are NOT a 6? ", 5, "All except the six."),
    box("So the top of the fraction is ", 5, "The five faces that are not a six.", phase="substitute"),
    box("and the bottom (total faces) is ", 6, "Six faces in all.", phase="substitute",
        done="5/6."),
    box("Check: P(6) + P(not 6) as sixths is 1 + 5 = ", 6, "One sixth plus five sixths.", phase="substitute",
        done="6/6 = 1, so 5/6 is right.") ])

setp("bronze", 5,
  "Only TT has no head, so subtract that from 1, or count the outcomes.",
  [mc("exactly_one", [1,2], "1/2 counts only ONE head (HT, TH). 'At least one' also includes HH, giving 3 out of 4.")],
  [ say("List all outcomes of two coins: HH, HT, TH, TT. That is the sample space."),
    box("How many outcomes are there in total? ", 4, "Count the four listed."),
    box("How many have at least one head? (all except TT) ", 3, "Every outcome but TT.", phase="substitute"),
    box("So the bottom of the fraction is ", 4, "The four outcomes.", phase="substitute",
        done="3/4."),
    box("Check: only TT has no head, and that is 1 outcome, so 4 − 1 = ", 3,
        "Four take away the one bad outcome.", phase="substitute", done="3 out of 4, matches.") ],
  display="Two coins are tossed. Find P(at least one head). Give as a fraction.")

setp("bronze", 6,
  "Blue over the total of all ten balls.",
  [mc("wrong_total", 0.375, "0.375 is 3/8, which leaves out the 2 green. The total is 5 + 3 + 2 = 10, so P(blue) = 3/10 = 0.3.")],
  [ say("P(blue) is the blue balls over ALL the balls, greens included."),
    box("Total = 5 + 3 + 2 = ", 10, "Add all three colours."),
    box("Blue balls = ", 3, "Just the blue.", phase="substitute"),
    box("P(blue) = 3 ÷ 10 = ", 0.3, "Three divided by ten.", phase="substitute"),
    box("Check all three add to 1: 0.5 + 0.3 + 0.2 = ", 1, "Add the three probabilities.", phase="substitute",
        done="The whole bag, so 0.3 is right.") ])

setp("bronze", 7,
  "All three sections add to 1.",
  [mc("forgets_one_term", 0.55, "0.55 is 1 − 0.45, which forgets B. All three sections add to 1: P(C) = 1 − 0.45 − 0.35 = 0.2.")],
  [ say("The three sections fill the whole spinner, so their probabilities add to 1."),
    box("Add the two you know: 0.45 + 0.35 = ", 0.8, "Add A and B."),
    box("P(C) = 1 − 0.8 = ", 0.2, "One take away nought point eight.", phase="substitute"),
    box("Check: 0.45 + 0.35 + 0.2 = ", 1, "Add all three.", phase="substitute",
        done="Adds to 1, so P(C) = 0.2.") ])

# =================== SILVER ===================
setp("silver", 0,
  "With replacement each draw is 0.3, so multiply 0.3 by 0.3.",
  [mc("without_replacement", 0.067, "0.067 comes from reducing the second draw (3/10 × 2/9). WITH replacement the ball goes back, so it stays 0.3 × 0.3 = 0.09.")],
  [ say("With replacement the ball goes back, so each draw is identical. P(red) = 3/10 = 0.3."),
    box("P(red) on one draw, as a decimal = ", 0.3, "Three out of ten."),
    box("Second draw is the same, 0.3. Multiply: 0.3 × 0.3 = ", 0.09, "Nought point three squared.", phase="substitute"),
    box("Check with fractions: 3/10 × 3/10 = 9/100 = ", 0.09, "Nine hundredths.", phase="substitute",
        done="Same as 0.09.") ])

setp("silver", 1,
  "Independent AND means multiply the two probabilities.",
  [mc("adds_instead", 0.9, "0.9 adds the probabilities. 'A and B' means both happen, so multiply: 0.4 × 0.5 = 0.2.")],
  [ say("Independent 'A and B' means both happen, so multiply the two probabilities."),
    box("Write P(A) = ", 0.4, "Given in the question."),
    box("P(A and B) = 0.4 × 0.5 = ", 0.2, "Nought point four times a half.", phase="substitute"),
    box("Check via 4 × 5 = 20, then two decimal places gives 0.2. Type 4 × 5 = ", 20,
        "Four times five.", phase="substitute", done="20 hundredths is 0.2, right.") ],
  display="P(A) = 0.4, P(B) = 0.5. A and B are independent. Find P(A and B). Give as a decimal.")

setp("silver", 2,
  "Without replacement the second draw is 4 out of 7.",
  [mc("with_replacement", [25,64], "25/64 keeps the second draw at 5/8. WITHOUT replacement one red is gone: 5/8 × 4/7 = 5/14.")],
  [ say("Without replacement: after one red leaves, both the reds and the total drop by 1. Draws: 5/8 then 4/7."),
    box("After taking one red, reds left = ", 4, "Five take away one."),
    box("Total balls left = ", 7, "Eight take away one.", phase="substitute"),
    box("Multiply the tops: 5 × 4 = ", 20, "Five times four.", phase="substitute"),
    box("Multiply the bottoms: 8 × 7 = ", 56, "Eight times seven.", phase="substitute"),
    box("Simplify 20/56 by 4: the top 20 ÷ 4 = ", 5, "Twenty divided by four.", phase="substitute"),
    box("and the bottom 56 ÷ 4 = ", 14, "Fifty-six divided by four.", phase="substitute",
        done="5/14.") ])

setp("silver", 3,
  "Multiply 0.6 by itself three times.",
  [mc("wrong_power", 0.36, "0.36 is 0.6², only two tosses. Three tosses: 0.6 × 0.6 × 0.6 = 0.216.")],
  [ say("Three identical tosses, all heads means AND, AND: multiply 0.6 three times."),
    box("First multiply two of them: 0.6 × 0.6 = ", 0.36, "Nought point six squared."),
    box("Now the third toss: 0.36 × 0.6 = ", 0.216, "Multiply by nought point six again.", phase="substitute"),
    box("Check with whole numbers: 6 × 6 × 6 = ", 216, "Six cubed.", phase="substitute",
        done="216/1000 = 0.216, right.") ])

setp("silver", 4,
  "Independent, so multiply the two daily chances.",
  [mc("adds_instead", 0.7, "0.7 adds the two days. 'Both days' means multiply: 0.4 × 0.3 = 0.12.")],
  [ say("'Both days' is AND, and the days are independent, so multiply."),
    box("Write P(rain Monday) = ", 0.4, "Given."),
    box("P(both) = 0.4 × 0.3 = ", 0.12, "Nought point four times nought point three.", phase="substitute"),
    box("Check via 4 × 3 = 12, then two decimal places gives 0.12. Type 4 × 3 = ", 12,
        "Four times three.", phase="substitute", done="0.12, right.") ])

setp("silver", 5,
  "Do 1 minus P(both blue).",
  [mc("exactly_one", [8,15], "8/15 is P(exactly one red). 'At least one' also includes both red: 1 − P(both blue) = 1 − 2/15 = 13/15.")],
  [ say("'At least one red' is easier as 1 minus its opposite, P(both blue). Blue draws: 4/10 then 3/9."),
    box("After one blue leaves, blues left = ", 3, "Four take away one."),
    box("Total balls left = ", 9, "Ten take away one.", phase="substitute"),
    box("P(both blue) = (4/10)(3/9) = 12/90. Simplify by 6: top 12 ÷ 6 = ", 2, "Twelve divided by six.", phase="substitute"),
    box("and bottom 90 ÷ 6 = ", 15, "Ninety divided by six.", phase="substitute", done="P(both blue) = 2/15."),
    box("P(at least one red) = 1 − 2/15. As fifteenths the top is 15 − 2 = ", 13,
        "Fifteen take away two.", phase="substitute"),
    box("and the bottom stays ", 15, "Still fifteenths.", phase="substitute",
        done="13/15, close to 1, sensible.") ],
  display="A bag has 6 red, 4 blue. Two drawn without replacement. Find P(at least one red). Give as a fraction.")

setp("silver", 6,
  "Add P(AA), P(BB) and P(CC).",
  [mc("one_case_only", 0.25, "0.25 is only P(A then A). 'Same result' also covers B and C: 0.25 + 0.09 + 0.04 = 0.38.")],
  [ say("'Same both times' means AA or BB or CC. Each is a multiply, then add the three paths."),
    box("P(AA) = 0.5 × 0.5 = ", 0.25, "Nought point five squared."),
    box("P(BB) = 0.3 × 0.3 = ", 0.09, "Nought point three squared.", phase="substitute"),
    box("P(CC) = 0.2 × 0.2 = ", 0.04, "Nought point two squared.", phase="substitute"),
    box("Add the three: 0.25 + 0.09 + 0.04 = ", 0.38, "Add them up.", phase="substitute", done="0.38."),
    box("Check the spinner is complete: 0.5 + 0.3 + 0.2 = ", 1, "Add A, B, C.", phase="substitute",
        done="Complete, so 0.38 is right.") ])

# =================== GOLD ===================
setp("gold", 0,
  "No replacement: multiply 8/12 by 7/11 by 6/10, then simplify.",
  [mc("with_replacement", [8,27], "8/27 is (8/12)³, treating it as WITH replacement. Each draw removes a red: 8/12 × 7/11 × 6/10 = 14/55.")],
  [ say("No replacement, three reds. The draws are 8/12, then 7/11, then 6/10 (each drops by 1)."),
    box("Multiply the tops: 8 × 7 × 6 = ", 336, "Eight times seven times six."),
    box("Multiply the bottoms: 12 × 11 × 10 = ", 1320, "Twelve times eleven times ten.", phase="substitute"),
    box("Simplify 336/1320 by dividing both by 24: the top 336 ÷ 24 = ", 14, "336 divided by 24.", phase="substitute"),
    box("and the bottom 1320 ÷ 24 = ", 55, "1320 divided by 24.", phase="substitute", done="14/55."),
    box("Check the top: 14 × 24 should give back 336, so 14 × 24 = ", 336,
        "Fourteen times twenty-four.", phase="substitute", done="Matches, so 14/55 is right.") ])

setp("gold", 1,
  "Fail, fail, pass: multiply 0.3 by 0.3 by 0.7.",
  [mc("wrong_events", 0.343, "0.343 is 0.7³, three passes. You need two fails then a pass: 0.3 × 0.3 × 0.7 = 0.063.")],
  [ say("Exactly the 3rd attempt means fail, fail, then pass. P(fail) = 1 − 0.7."),
    box("P(fail) = 1 − 0.7 = ", 0.3, "One take away nought point seven."),
    box("Multiply the three in order: 0.3 × 0.3 × 0.7 = ", 0.063, "Fail, fail, pass.", phase="substitute"),
    box("Check with whole numbers: 3 × 3 × 7 = ", 63, "Three times three times seven.", phase="substitute",
        done="63/1000 = 0.063, right.") ])

setp("gold", 2,
  "Count ordered pairs adding to 7 out of 36.",
  [mc("unordered_pairs", [1,7], "1/7 counts (1,6),(2,5),(3,4) as three outcomes out of 21 unordered pairs. The dice are separate, so (1,6) and (6,1) both count: 6 out of 36 = 1/6.")],
  [ say("Two dice give 6 × 6 = 36 equally likely ordered outcomes. Count the ones totalling 7."),
    box("List them: (1,6)(2,5)(3,4)(4,3)(5,2)(6,1). How many? ", 6, "Count the six pairs."),
    box("Total outcomes = 6 × 6 = ", 36, "Six faces on each die.", phase="substitute"),
    box("P = 6/36. Simplify by 6: the top 6 ÷ 6 = ", 1, "Six divided by six.", phase="substitute"),
    box("and the bottom 36 ÷ 6 = ", 6, "Thirty-six divided by six.", phase="substitute", done="1/6."),
    box("Check: 7 is the most common total, and 1/6 is about 0.167. Confirm 6 × 6 = ", 36,
        "Six times six.", phase="substitute", done="6 out of 36 = 1/6.") ])

setp("gold", 3,
  "Set (5/(5+n))(4/(4+n)) = 2/9 and solve for n.",
  [mc("factor_mismatch", 4, "n = 4 gives (9)(8) = 72, not 90, so P would be 20/72, not 2/9. You need (5+n)(4+n) = 90, which works at n = 5: (10)(9).")],
  [ say("Two reds without replacement: (5/(5+n)) × (4/(4+n)) = 2/9. The tops give 5 × 4."),
    box("Multiply the tops: 5 × 4 = ", 20, "Five times four."),
    box("So 20 ÷ ((5+n)(4+n)) = 2/9. Cross-multiply: (5+n)(4+n) = 20 × 9 ÷ 2 = ", 90,
        "Twenty times nine, then halve.", phase="substitute"),
    box("Find n so (5+n)(4+n) = 90. Try n = 5: (5+5)(4+5) = 10 × 9 = ", 90, "Ten times nine.", phase="substitute"),
    box("It works, so n = ", 5, "The value that made 90.", phase="substitute", done="n = 5."),
    box("Check: with 5 blue, P = (5/10)(4/9) = 20/90. Simplify: 90 ÷ 45 = ", 2,
        "Ninety divided by forty-five gives the 2 in 2/9.", phase="substitute", done="20/90 = 2/9, correct.") ])

setp("gold", 4,
  "Use 2p(1−p) = 0.48 and take the smaller root.",
  [mc("gave_larger_root", 0.6, "0.6 is the other solution. Both 0.4 and 0.6 satisfy the equation, but the question asks for the SMALLER value, 0.4.")],
  [ say("Exactly one head in two tosses is HT or TH, so P = 2 × p × (1 − p) = 0.48."),
    box("Divide both sides by 2: p(1 − p) = 0.48 ÷ 2 = ", 0.24, "Half of 0.48."),
    box("So p² − p + 0.24 = 0. The discriminant is 1 − 4(0.24) = 1 − 0.96 = ", 0.04,
        "One minus nought point nine six.", phase="substitute"),
    box("√0.04 = ", 0.2, "What squares to 0.04?", phase="substitute"),
    box("Smaller root: p = (1 − 0.2) ÷ 2 = ", 0.4, "Use the minus for the smaller value.", phase="substitute",
        done="p = 0.4."),
    box("Check: with p = 0.4, 2 × 0.4 × 0.6 = ", 0.48, "Two times 0.4 times 0.6.", phase="substitute",
        done="Gives 0.48, so p = 0.4.") ],
  solutions=[0.4])

# fix pre-existing em dashes in preserved worked_examples (hard style rule)
we = pd["worked_examples"]
we[0]["steps"][0]["content"] = we[0]["steps"][0]["content"].replace(
    "{5, 6} — 2 outcomes", "{5, 6}, that is 2 outcomes")
we[2]["steps"][0]["label"] = we[2]["steps"][0]["label"].replace(
    "Step 1 — Two paths", "Step 1: Two paths")

# tier descriptions
pd["problem_bank"]["bronze_description"] = "One event: count the favourable outcomes over the total, or use 1 − P for 'not'."
pd["problem_bank"]["silver_description"] = "Two events combined: multiply along the branches, adjusting the fraction if there is no replacement."
pd["problem_bank"]["gold_description"] = "Three or more stages, or work backwards from a given probability to an unknown."

# =================== tier_guides ===================
pd["tier_guides"] = {
 "bronze": {
   "title": "Bronze: one event",
   "steps": [
     "The probability of one event is the number of favourable outcomes over the total number of outcomes. Count carefully, including every possibility.",
     "For 'not' or 'at least one', it is often quicker to work out the opposite and do <strong>1 − P</strong>.",
     "Give a simplified fraction or a decimal, exactly as the question asks."
   ],
   "example": {
     "question": "A bag has 4 red and 6 yellow. Find P(yellow) as a decimal.",
     "steps": [
       {"label": "Count", "content": "<p>Total = 4 + 6 = 10 balls.</p>"},
       {"label": "Favourable", "content": "<p>6 of them are yellow.</p>"},
       {"label": "Divide", "content": "<p>\\(P(\\text{yellow}) = 6 \\div 10 = 0.6\\)</p>"},
       {"label": "Check", "content": "<p>P(not yellow) = 0.4, and \\(0.6 + 0.4 = 1\\) ✓</p>"},
       {"label": "Answer", "content": "<p><strong>0.6</strong></p>", "isAnswer": True, "is_answer": True}
     ]
   }
 },
 "silver": {
   "title": "Silver: two events, multiply",
   "steps": [
     "Two events happening together (AND) means multiply their probabilities along the branches.",
     "<strong>With replacement</strong>, each draw uses the same fraction. <strong>Without replacement</strong>, drop both the top and the total by 1 for the second draw.",
     "For 'at least one', it is usually easier to do 1 − P(none)."
   ],
   "example": {
     "question": "A bag has 5 red and 3 blue. Two drawn without replacement. Find P(both red).",
     "steps": [
       {"label": "Draws", "content": "<p>\\(\\frac{5}{8}\\) then \\(\\frac{4}{7}\\) (one red is gone).</p>"},
       {"label": "Multiply", "content": "<p>\\(\\frac{5}{8} \\times \\frac{4}{7} = \\frac{20}{56}\\)</p>"},
       {"label": "Simplify", "content": "<p>\\(\\frac{20}{56} = \\frac{5}{14}\\)</p>"},
       {"label": "Check", "content": "<p>\\(\\frac{5}{14} \\approx 0.36\\), below one draw \\(\\frac{5}{8}\\) ✓</p>"},
       {"label": "Answer", "content": "<p><strong>\\(\\frac{5}{14}\\)</strong></p>", "isAnswer": True, "is_answer": True}
     ]
   }
 },
 "gold": {
   "title": "Gold: many stages or work backwards",
   "steps": [
     "Three or more stages: multiply along the whole path, dropping the numbers each draw if there is no replacement.",
     "When a probability is given and a value is unknown, set up an equation and solve it.",
     "Always check the answer is between 0 and 1, and re-substitute to confirm."
   ],
   "example": {
     "question": "A bag has 8 red and 4 blue. Three drawn without replacement. Find P(all red).",
     "steps": [
       {"label": "Draws", "content": "<p>\\(\\frac{8}{12} \\times \\frac{7}{11} \\times \\frac{6}{10}\\)</p>"},
       {"label": "Multiply", "content": "<p>\\(= \\frac{336}{1320}\\)</p>"},
       {"label": "Simplify", "content": "<p>\\(\\frac{336}{1320} = \\frac{14}{55}\\)</p>"},
       {"label": "Check", "content": "<p>\\(\\frac{14}{55} \\approx 0.25\\), sensible for three reds ✓</p>"},
       {"label": "Answer", "content": "<p><strong>\\(\\frac{14}{55}\\)</strong></p>", "isAnswer": True, "is_answer": True}
     ]
   }
 }
}

# =================== guided (opener + teach) ===================
pd["guided"] = {
 "opener": {
   "label": "Before any formula",
   "display": "A bag you can see:<br>3 red sweets and 1 green sweet",
   "steps": [
     box("How many sweets are in the bag altogether? ", 4,
         "Count them: 3 red and 1 green.",
         say="Grab one sweet without looking. Start with the easy bit."),
     box("How many of the 4 are red? ", 3, "The red ones.",
         say="That total, 4, is the bottom of every probability: the number of things that could happen."),
     box("How many of the 4 are NOT red? ", 1, "Just the green one.",
         say="So the chance of red is 3 out of 4. You just did the whole rule: favourable outcomes over the total. Now the opposite:"),
     say("1 out of 4. Notice \\(\\frac{3}{4}\\) and \\(\\frac{1}{4}\\) add up to 1: an event and its opposite always fill the whole bag. That is the <strong>1 − P</strong> rule. Every question today is built from these two ideas.")
   ]
 },
 "teach": {
   "bronze": {
     "display": "A box has 3 green and 7 white balls. Find P(green) as a decimal.",
     "label": "Together: your first one",
     "steps": [
       box("Total balls = 3 + 7 = ", 10, "Add green and white."),
       box("Green balls = ", 3, "Just the green ones."),
       box("P(green) = 3 ÷ 10 = ", 0.3, "Three divided by ten.",
           done="Favourable over total. That is the whole bronze move."),
       box("Check with the opposite: P(not green) = 1 − 0.3 = ", 0.7, "One take away nought point three.",
           done="0.3 + 0.7 = 1 ✓")
     ]
   },
   "silver": {
     "display": "A bag has 2 red and 3 blue. Two drawn with replacement. Find P(both blue) as a decimal.",
     "label": "Together: the silver move",
     "steps": [
       box("Total = 2 + 3 = ", 5, "Add red and blue."),
       box("P(blue) on one draw, as a decimal = 3 ÷ 5 = ", 0.6, "Three divided by five."),
       box("With replacement the ball goes back, so the second draw is also 0.6. Multiply: 0.6 × 0.6 = ", 0.36,
           "Nought point six squared.", done="AND means multiply. That is the silver move."),
       box("Check as a fraction: 3/5 × 3/5 = 9/25 = ", 0.36, "Nine twenty-fifths.", done="Same, 0.36.")
     ]
   },
   "gold": {
     "display": "A bag has 3 red and 2 blue. Three drawn without replacement. Find P(all red).",
     "label": "Together: the gold move",
     "steps": [
       box("Start: 3 red out of 5. After one red is taken, reds left = ", 2, "Three take away one."),
       box("and the total left = ", 4, "Five take away one."),
       box("After a second red, reds left = ", 1, "Two take away one."),
       box("and the total left = ", 3, "Four take away one."),
       box("So the draws are 3/5, 2/4, 1/3. Multiply the tops: 3 × 2 × 1 = ", 6, "Three times two times one."),
       box("Multiply the bottoms: 5 × 4 × 3 = ", 60, "Five times four times three."),
       box("Simplify 6/60: 60 ÷ 6 = ", 10, "Sixty divided by six.",
           done="So 1/10. Without replacement, both numbers drop every draw. That is gold.")
     ]
   }
 }
}

# =================== slim method_card ===================
pd["method_card"] = {
 "title": "How to Use Tree Diagrams",
 "steps": [
   "P(event) = favourable outcomes ÷ total outcomes. For 'not', use 1 − P.",
   "Combined events: draw a tree, one branch per outcome; branches from a point sum to 1.",
   "AND: multiply along a path. OR: add the paths.",
   "Without replacement: after each draw, both the count and the total drop by 1."
 ],
 "content": "<p>Probability runs from 0 (impossible) to 1 (certain), and \\(P(A') = 1 - P(A)\\).</p><p>For combined events, multiply along the branches (AND) and add complete paths (OR). With replacement the fractions stay the same; without replacement the numerator and denominator each fall by 1 at every draw.</p>",
 "example": "<p><strong>A bag has 3 red and 5 blue. Two balls drawn without replacement. Find P(both red).</strong></p><p>P(R then R) = \\(\\frac{3}{8} \\times \\frac{2}{7} = \\frac{6}{56} = \\frac{3}{28}\\)</p>"
}

json.dump(pd, io.open("lesson_probability-statistics-L01.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("built. tiers:",
      {t: len(pd["problem_bank"][t]) for t in ("bronze","silver","gold")})
