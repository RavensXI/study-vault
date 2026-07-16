# -*- coding: utf-8 -*-
import json, io

live = json.load(io.open("_live_L02.json", encoding="utf-8"))

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def sayonly(say):
    return {"say": say}

MINUS = "−"  # unicode minus, not em dash

# ---------------- METHOD CARD (slim) ----------------
method_card = {
    "title": "Venn Diagrams & Conditional Probability",
    "steps": [
        "Fill the overlap (both) first, then subtract it from each circle. Whatever is left sits outside.",
        "Every region adds up to the total. Divide a region by the total to get its probability.",
        "Addition rule: \\(P(A \\cup B) = P(A) + P(B) - P(A \\cap B)\\).",
        "Conditional: \\(P(A|B) = \\frac{P(A \\cap B)}{P(B)}\\), the overlap over the condition."
    ],
    "content": "<p>A <strong>Venn diagram</strong> sorts items into overlapping circles inside a rectangle (everyone). Fill the <strong>intersection</strong> \\(A \\cap B\\) first, then peel it off each circle so nobody is counted twice.</p><p><strong>Conditional probability</strong> \\(P(A|B) = \\frac{P(A \\cap B)}{P(B)}\\) shrinks the world down to B, then finds the share that is also A. For <strong>independent</strong> events, \\(P(A \\cap B) = P(A) \\times P(B)\\).</p>",
    "example": live["method_card"]["example"]
}

# ---------------- PROBLEM BANK ----------------
gold = [
 {  # G0
  "display": "P(A) = 0.55, P(B) = 0.4, P(A' ∩ B') = 0.25. Find P(A ∩ B).",
  "solutions": [0.2], "calculator": True, "input_type": "single_value",
  "hint": "Change 'neither' into the union using 1 minus, then apply the addition rule.",
  "misconceptions": [
    {"pattern": "complement_as_intersection", "expect": 0.25,
     "message": "0.25 is P(A' ∩ B'), the chance of NEITHER event, not the overlap. First turn it into the union: P(A ∪ B) = 1 − 0.25 = 0.75, then P(A ∩ B) = 0.55 + 0.4 − 0.75 = 0.2.",
     "note": "student copies the given complement as the intersection"},
    {"pattern": "forgot_complement", "expect": 0.7,
     "message": "You used 0.25 straight as the union, but 0.25 is 'neither'. The union is 1 − 0.25 = 0.75. Then P(A ∩ B) = 0.55 + 0.4 − 0.75 = 0.2.",
     "note": "0.55+0.4-0.25 = 0.7"}
  ],
  "guided_steps": [
    box("0.25 is the chance of NEITHER event. Everything else is the union. P(A ∪ B) = 1 − 0.25 = ", 0.75,
        "Take the 'neither' probability away from 1.", say="Start by turning 'neither' into the union."),
    box("First add the two singles: 0.55 + 0.4 = ", 0.95,
        "Just add the two given probabilities.", phase="substitute",
        say="Now use the addition rule, P(A ∪ B) = P(A) + P(B) − P(A ∩ B), to dig out the overlap."),
    box("Now subtract the union: 0.95 − 0.75 = ", 0.2,
        "Take the union away from that total.", phase="substitute"),
    box("Check the four regions total 1. Both 0.2, A only 0.35, B only 0.2, neither 0.25: 0.2 + 0.35 + 0.2 + 0.25 = ", 1.0,
        "Add all four regions together.", phase="substitute",
        done="Every region totals 1, so P(A ∩ B) = 0.2 is right.")
  ]
 },
 {  # G1
  "display": "120 students: 70 like A, 55 like B, 45 like C. 30 like A∩B, 20 like B∩C, 25 like A∩C, 10 like all three. How many like none?",
  "solutions": [15], "calculator": False, "input_type": "single_value",
  "hint": "Add the three totals, subtract the three pair-overlaps, add back the triple, then take from 120.",
  "misconceptions": [
    {"pattern": "forgot_triple", "expect": 25,
     "message": "The 10 who like all three get subtracted too many times, so add them back once: 70 + 55 + 45 − 30 − 20 − 25 + 10 = 105, and none = 120 − 105 = 15. Leaving off the +10 gives 25.",
     "note": "170-75 = 95, 120-95 = 25"}
  ],
  "guided_steps": [
    box("Add the three single totals: 70 + 55 + 45 = ", 170,
        "Just add the three group sizes.", say="Build the union with inclusion-exclusion. Singles first."),
    box("Now the three pair overlaps: 30 + 20 + 25 = ", 75,
        "Add the three 'both' numbers."),
    box("Singles minus pairs, then add the triple back: 170 − 75 + 10 = ", 105,
        "Take off the 75, then add the 10 who like all three.",
        say="Inclusion-exclusion subtracts each pair once, then restores the triple."),
    box("That 105 like at least one thing, so the rest like none: 120 − 105 = ", 15,
        "Subtract from the group of 120.", phase="substitute",
        say="Now finish: everyone not in the union likes none."),
    box("Check the two parts rebuild the group: 105 + 15 = ", 120,
        "Add the in-circles count to the none count.", phase="substitute",
        done="105 in circles plus 15 with none is everyone, so 15 like none.")
  ]
 },
 {  # G2  (FIXED: solutions duplicated + d.p. mismatch)
  "display": "A medical test: P(disease) = 0.01, P(positive|disease) = 0.95, P(positive|no disease) = 0.05. Find P(positive). Give as a decimal.",
  "solutions": [0.059], "calculator": True, "input_type": "single_value",
  "hint": "A positive comes two ways: add disease-and-positive to healthy-and-false-positive.",
  "misconceptions": [
    {"pattern": "only_true_positive", "expect": 0.95,
     "message": "0.95 is only P(positive given disease). Positives also come from the 99% who are healthy: P(+) = 0.01 × 0.95 + 0.99 × 0.05 = 0.059.",
     "note": "reports the conditional, not the total"},
    {"pattern": "forgot_healthy_branch", "expect": 0.0095,
     "message": "0.0095 is just the disease route. Add the false positives from healthy people: 0.99 × 0.05 = 0.0495, giving 0.0095 + 0.0495 = 0.059.",
     "note": "0.01*0.95 only"}
  ],
  "guided_steps": [
    box("Route one, has the disease AND tests positive: 0.01 × 0.95 = ", 0.0095,
        "Multiply along the disease branch.", say="Two separate routes lead to a positive test."),
    box("Route two, no disease (that is 0.99) but a false positive: 0.99 × 0.05 = ", 0.0495,
        "Multiply along the healthy branch.", say="A healthy person can still test positive."),
    box("A positive can come from either route, so add them: 0.0095 + 0.0495 = ", 0.059,
        "Add the two branch probabilities.", phase="substitute",
        say="Now finish by combining the routes."),
    box("Check with 10000 people: 100 diseased give 95 positives, 9900 healthy give 495; 95 + 495 = ", 590,
        "Add the true positives and false positives.", phase="substitute",
        done="590 out of 10000 is 0.059, so it checks out.")
  ]
 },
 {  # G3
  "display": "P(A) = 0.3, P(B|A) = 0.5, P(B|A') = 0.2. Find P(B). Give to 2 d.p.",
  "solutions": [0.29], "calculator": True, "input_type": "single_value",
  "hint": "Weight each branch and add: P(B|A) times P(A), plus P(B|A') times P(A').",
  "misconceptions": [
    {"pattern": "wrong_weight", "expect": 0.21,
     "message": "The second branch must be weighted by P(A') = 0.7, not by P(A). P(B) = 0.5 × 0.3 + 0.2 × 0.7 = 0.15 + 0.14 = 0.29.",
     "note": "0.5*0.3 + 0.2*0.3 = 0.21"},
    {"pattern": "only_one_branch", "expect": 0.15,
     "message": "0.15 is only the route through A. B can also happen without A: add 0.2 × 0.7 = 0.14, giving 0.29.",
     "note": "0.5*0.3 only"}
  ],
  "guided_steps": [
    box("Route one, B with A: 0.5 × 0.3 = ", 0.15,
        "Multiply along the A branch.", say="B can happen with A or without A. Take each route."),
    box("Route two, B without A (P(A') = 0.7): 0.2 × 0.7 = ", 0.14,
        "Multiply along the not-A branch.", say="First P(A') = 1 − 0.3 = 0.7."),
    box("B arrives by either route, so add them: 0.15 + 0.14 = ", 0.29,
        "Add the two branch probabilities.", phase="substitute",
        say="Now finish by combining the routes."),
    box("Check with 100 people: 30 in A give 15, 70 not in A give 14; 15 + 14 = ", 29,
        "Add the two counts.", phase="substitute",
        done="29 out of 100 is 0.29, so it checks out.")
  ]
 },
 {  # G4  (multiple_choice - no guided_steps)
  "display": "Two events: P(A ∪ B) = 0.8, P(A) = 0.5, P(B) = 0.6. Are A and B mutually exclusive? Answer yes or no.",
  "options": ["Yes: \\(P(A) + P(B) = P(A \\cup B)\\)", "No: \\(P(A) + P(B) \\neq P(A \\cup B)\\)"],
  "solutions": [1], "calculator": False, "input_type": "multiple_choice",
  "hint": "Work out P(A intersect B) with the addition rule; not zero means they can overlap.",
  "misconceptions": [
    {"pattern": "assumed_exclusive", "expect": 0,
     "message": "Work out the overlap: P(A ∩ B) = 0.5 + 0.6 − 0.8 = 0.3. Since 0.3 is not 0, both events can happen together, so they are NOT mutually exclusive.",
     "note": "picks Yes"}
  ]
 }
]

bronze = [
 {  # B0
  "display": "40 people: 25 like tea (T), 18 like coffee (C), 8 like both. How many like neither?",
  "solutions": [5], "calculator": False, "input_type": "single_value",
  "hint": "Take the 8 'both' out of each circle, add the regions, then subtract from 40.",
  "misconceptions": [
    {"pattern": "counted_overlap_twice", "expect": 3,
     "message": "The 8 who like both sit inside the 25 and the 18, so 25 + 18 = 43 counts them twice. People in a circle = 17 + 10 + 8 = 35, and neither = 40 − 35 = 5.",
     "note": "43 - 40 = 3"}
  ],
  "guided_steps": [
    box("Tea only, peel off the 8 who also like coffee: 25 − 8 = ", 17,
        "Take the 8 'both' out of the 25 tea-likers.", say="Fill the overlap first: 8 like both. Now peel it off each circle."),
    box("Coffee only: 18 − 8 = ", 10, "Take the 8 'both' out of the 18 coffee-likers."),
    box("Add the three regions inside the circles: 17 + 10 + 8 = ", 35,
        "Add tea-only, coffee-only and both.", say="These are everyone who likes at least one drink."),
    box("Everyone else likes neither: 40 − 35 = ", 5,
        "Subtract from the group of 40.", phase="substitute", say="Now finish."),
    box("Check every region totals 40: 17 + 10 + 8 + 5 = ", 40,
        "Add all four regions.", phase="substitute",
        done="It adds back to 40, so 5 like neither.")
  ]
 },
 {  # B1  (FIXED: restated context, was 'In the Venn diagram above')
  "display": "40 people: 25 like tea (T), 18 like coffee (C), 8 like both. Find P(T only) as a decimal.",
  "solutions": [0.425], "calculator": False, "input_type": "single_value",
  "hint": "Tea only is 25 minus the 8 who also like coffee, then divide by 40.",
  "misconceptions": [
    {"pattern": "used_whole_circle", "expect": 0.625,
     "message": "T only leaves out the 8 who also like coffee: 25 − 8 = 17, so P(T only) = 17/40 = 0.425. Using the whole 25 gives 0.625.",
     "note": "25/40 = 0.625"}
  ],
  "guided_steps": [
    box("How many like tea only? 25 − 8 = ", 17,
        "Take the 8 'both' out of the 25.", say="Find the tea-only region first."),
    box("Probability is that region out of 40. 17 ÷ 40 = ", 0.425,
        "17 ÷ 40 = 0.425.", phase="substitute", say="Now turn the count into a probability."),
    box("Check: 0.425 × 40 should give the tea-only count back: 0.425 × 40 = ", 17,
        "Multiply the decimal back by 40.", phase="substitute",
        done="It returns 17, so P(T only) = 0.425.")
  ]
 },
 {  # B2
  "display": "A = {1,2,3,4,5}, B = {3,4,5,6,7}. How many elements in \\(A \\cap B\\)?",
  "solutions": [3], "calculator": False, "input_type": "single_value",
  "hint": "Keep only the elements that appear in both lists.",
  "misconceptions": [
    {"pattern": "found_union", "expect": 7,
     "message": "A ∩ B means in BOTH sets, which is {3, 4, 5} = 3. Counting everything in either set, {1,2,3,4,5,6,7} = 7, is the union A ∪ B instead.",
     "note": "gives the union"}
  ],
  "guided_steps": [
    box("How many elements does set A have in total? ", 5,
        "Count A = {1,2,3,4,5}.", say="Start with set A."),
    box("Intersect: keep only A's elements that are also in B = {3,4,5,6,7}. 1 and 2 are not in B; 3, 4, 5 are. How many is that? ", 3,
        "Count the shared list {3,4,5}.", phase="substitute", say="Now find the overlap."),
    box("Check: 6 and 7 are only in B, so they do not count. Shared count = ", 3,
        "Only 3, 4 and 5 are in both.", phase="substitute",
        done="A ∩ B = {3,4,5}, so 3 elements.")
  ]
 },
 {  # B3
  "display": "A = {1,2,3,4,5}, B = {3,4,5,6,7}. How many elements in \\(A \\cup B\\)?",
  "solutions": [7], "calculator": False, "input_type": "single_value",
  "hint": "List every element once; B only adds the ones not already in A.",
  "misconceptions": [
    {"pattern": "double_counted", "expect": 10,
     "message": "A ∪ B lists each element once: {1,2,3,4,5,6,7} = 7. Adding the sizes 5 + 5 = 10 counts 3, 4 and 5 twice.",
     "note": "5+5 = 10"}
  ],
  "guided_steps": [
    box("How many elements in A alone? ", 5,
        "Count {1,2,3,4,5}.", say="Start with set A."),
    box("Union lists every element once. A already has {1,2,3,4,5}; B adds 6 and 7 (3,4,5 are already listed). How many NEW elements does B add? ", 2,
        "Only 6 and 7 are not already in A.", phase="substitute", say="Now add B's new elements."),
    box("Total in the union: 5 + 2 = ", 7,
        "A's five plus the two new ones.", phase="substitute"),
    box("Check by listing: {1,2,3,4,5,6,7}, count = ", 7,
        "Count each element once.", phase="substitute",
        done="Each element appears once, so A ∪ B has 7.")
  ]
 },
 {  # B4
  "display": "P(A) = 0.5, P(B) = 0.4, P(A ∩ B) = 0.2. Find P(A ∪ B).",
  "solutions": [0.7], "calculator": False, "input_type": "single_value",
  "hint": "Add P(A) and P(B), then subtract the overlap once.",
  "misconceptions": [
    {"pattern": "forgot_subtract_overlap", "expect": 0.9,
     "message": "The 0.2 overlap is inside both P(A) and P(B), so subtract it once: 0.5 + 0.4 − 0.2 = 0.7. Just adding gives 0.9.",
     "note": "0.5+0.4 = 0.9"}
  ],
  "guided_steps": [
    box("Add the two probabilities: 0.5 + 0.4 = ", 0.9,
        "Just add P(A) and P(B).", say="Addition rule: P(A ∪ B) = P(A) + P(B) − P(A ∩ B)."),
    box("The 0.2 overlap was counted in both, so take it off once: 0.9 − 0.2 = ", 0.7,
        "Subtract the intersection.", phase="substitute", say="Now finish by removing the double count."),
    box("Check with regions. A only 0.3, B only 0.2, both 0.2: 0.3 + 0.2 + 0.2 = ", 0.7,
        "Add the three union regions.", phase="substitute",
        done="The union regions total 0.7, so it is right.")
  ]
 },
 {  # B5
  "display": "60 students: 35 study maths (M), 28 study science (S), 15 study both. Find the number studying maths only.",
  "solutions": [20], "calculator": False, "input_type": "single_value",
  "hint": "Maths only is the maths total minus the 15 who do both.",
  "misconceptions": [
    {"pattern": "used_whole_total", "expect": 35,
     "message": "Maths only leaves out the 15 who do both: 35 − 15 = 20. The full 35 still includes them.",
     "note": "reports all of maths"}
  ],
  "guided_steps": [
    box("Start from the overlap of 15. Science only: 28 − 15 = ", 13,
        "Peel the 15 'both' off the 28 scientists.", say="Fill the overlap first, then peel it off each circle."),
    box("Maths only peels the same 15 off the 35: 35 − 15 = ", 20,
        "Subtract the overlap from the maths total.", phase="substitute", say="Now the maths-only region."),
    box("Check the three circle regions do not exceed 60: 20 + 13 + 15 = ", 48,
        "Add maths-only, science-only and both.", phase="substitute",
        done="48 is within 60, so maths only = 20 is correct.")
  ]
 },
 {  # B6  (FIXED: restated context, was 'From the question above')
  "display": "60 students: 35 study maths (M), 28 study science (S), 15 study both. How many study neither maths nor science?",
  "solutions": [12], "calculator": False, "input_type": "single_value",
  "hint": "Take both overlaps out, add the regions, then subtract from 60.",
  "misconceptions": [
    {"pattern": "forgot_overlap", "expect": 3,
     "message": "The 15 who do both are counted in the 35 and the 28. In a circle = 20 + 13 + 15 = 48, so neither = 60 − 48 = 12.",
     "note": "60-35-28 = -3"}
  ],
  "guided_steps": [
    box("Maths only: 35 − 15 = ", 20,
        "Peel the 15 'both' off the 35.", say="Peel the overlap off each subject."),
    box("Science only: 28 − 15 = ", 13, "Peel the 15 'both' off the 28."),
    box("Add the three regions inside the circles: 20 + 13 + 15 = ", 48,
        "Add maths-only, science-only and both.", say="These study at least one subject."),
    box("Everyone else studies neither: 60 − 48 = ", 12,
        "Subtract from 60.", phase="substitute", say="Now finish."),
    box("Check every region totals 60: 20 + 13 + 15 + 12 = ", 60,
        "Add all four regions.", phase="substitute",
        done="It adds back to 60, so 12 study neither.")
  ]
 },
 {  # B7
  "display": "If P(A') = 0.35, find P(A).",
  "solutions": [0.65], "calculator": False, "input_type": "single_value",
  "hint": "P(A) is 1 minus P(A').",
  "misconceptions": [
    {"pattern": "gave_complement", "expect": 0.35,
     "message": "0.35 is P(A'), the chance of NOT A. P(A) = 1 − 0.35 = 0.65.",
     "note": "returns the complement"}
  ],
  "guided_steps": [
    box("A and not-A together must total 1. So P(A) + 0.35 must equal ", 1,
        "All probability totals 1.", say="Something must happen, so the two probabilities add to 1."),
    box("Therefore P(A) = 1 − 0.35 = ", 0.65,
        "Subtract 0.35 from 1.", phase="substitute", say="Now finish."),
    box("Check: 0.65 + 0.35 = ", 1.0,
        "Add P(A) and P(A').", phase="substitute",
        done="They add to 1, so P(A) = 0.65.")
  ]
 }
]

silver = [
 {  # S0
  "display": "P(A) = 0.7, P(B) = 0.5, P(A ∩ B) = 0.35. Find P(A|B).",
  "solutions": [0.7], "calculator": False, "input_type": "single_value",
  "hint": "Divide the overlap by the condition: P(A intersect B) over P(B).",
  "misconceptions": [
    {"pattern": "divided_by_wrong", "expect": 0.5,
     "message": "P(A|B) divides by the condition B, not A: 0.35 ÷ 0.5 = 0.7. Dividing by P(A) = 0.7 gives 0.5.",
     "note": "0.35/0.7 = 0.5"}
  ],
  "guided_steps": [
    box("Numerator, the overlap P(A ∩ B) = ", 0.35,
        "It is the overlap, given as 0.35.", say="Conditional formula: P(A|B) = P(A ∩ B) ÷ P(B). The condition B is on the bottom."),
    box("Denominator, the condition P(B) = ", 0.5,
        "The condition is B, given as 0.5.", phase="substitute", say="Now divide."),
    box("Divide: 0.35 ÷ 0.5 = ", 0.7, "0.35 ÷ 0.5 = 0.7.", phase="substitute"),
    box("Check: 0.7 × 0.5 should give the overlap back: 0.7 × 0.5 = ", 0.35,
        "Multiply the answer by P(B).", phase="substitute",
        done="It returns 0.35, so P(A|B) = 0.7.")
  ]
 },
 {  # S1
  "display": "80 people: 50 speak French (F), 30 speak German (G), 15 both. Find P(G|F).",
  "solutions": [0.3], "calculator": False, "input_type": "single_value",
  "hint": "Shrink to the 50 French speakers, then divide the 15 who do both by 50.",
  "misconceptions": [
    {"pattern": "divided_by_total", "expect": 0.1875,
     "message": "Given French, restrict to the 50 French speakers: P(G|F) = 15 ÷ 50 = 0.3. Dividing by all 80 gives 0.1875.",
     "note": "15/80 = 0.1875"}
  ],
  "guided_steps": [
    box("The condition F has how many people? ", 50,
        "50 speak French.", say="Given they speak French, shrink the world down to the 50 French speakers."),
    box("Of those, how many also speak German (the overlap)? ", 15,
        "15 speak both.", phase="substitute", say="Now count the ones that also match."),
    box("P(G|F) = 15 ÷ 50 = ", 0.3, "15 ÷ 50 = 0.3.", phase="substitute"),
    box("Check: 0.3 × 50 should give the both count: 0.3 × 50 = ", 15,
        "Multiply the answer by 50.", phase="substitute",
        done="It returns 15, so P(G|F) = 0.3.")
  ]
 },
 {  # S2
  "display": "P(A) = 0.6, P(B) = 0.4. A and B are independent. Find P(A ∩ B).",
  "solutions": [0.24], "calculator": False, "input_type": "single_value",
  "hint": "Independent events multiply: P(A) times P(B).",
  "misconceptions": [
    {"pattern": "added_not_multiplied", "expect": 1.0,
     "message": "Independent events multiply, they do not add: 0.6 × 0.4 = 0.24. Adding gives 1.0, which cannot be an overlap here.",
     "note": "0.6+0.4 = 1.0"}
  ],
  "guided_steps": [
    box("Write the first probability: P(A) = ", 0.6,
        "Given as 0.6.", say="Independent means one does not affect the other, so multiply, not add."),
    box("Multiply by P(B): 0.6 × 0.4 = ", 0.24,
        "0.6 × 0.4 = 0.24.", phase="substitute", say="Now finish the multiplication."),
    box("Check it behaves independently: P(A|B) = 0.24 ÷ 0.4 = ", 0.6,
        "Divide the overlap by P(B).", phase="substitute",
        done="0.6 equals P(A), confirming independence, so P(A ∩ B) = 0.24.")
  ]
 },
 {  # S3
  "display": "P(A) = 0.5, P(A ∩ B) = 0.15, P(A ∪ B) = 0.75. Find P(B).",
  "solutions": [0.4], "calculator": False, "input_type": "single_value",
  "hint": "Rearrange the addition rule to make P(B) the subject.",
  "misconceptions": [
    {"pattern": "forgot_intersection_term", "expect": 0.25,
     "message": "Rearrange P(A ∪ B) = P(A) + P(B) − P(A ∩ B) to get P(B) = 0.75 − 0.5 + 0.15 = 0.4. Dropping the 0.15 gives 0.25.",
     "note": "0.75-0.5 = 0.25"}
  ],
  "guided_steps": [
    box("Start with P(A ∪ B) − P(A): 0.75 − 0.5 = ", 0.25,
        "Subtract P(A) from the union.", say="Rearrange the addition rule: P(B) = P(A ∪ B) − P(A) + P(A ∩ B)."),
    box("That is missing the overlap that belongs to B, so add it back: 0.25 + 0.15 = ", 0.4,
        "Add the intersection 0.15.", phase="substitute", say="Now finish."),
    box("Check the addition rule forwards: 0.5 + 0.4 − 0.15 = ", 0.75,
        "Put P(B) = 0.4 back in.", phase="substitute",
        done="It gives the union 0.75, so P(B) = 0.4.")
  ]
 },
 {  # S4  (fraction)
  "display": "100 students: 60 play sport, 45 play music, 20 do both. A student who plays sport is picked at random. Find P(also plays music).",
  "solutions": [1, 3], "calculator": False, "input_type": "fraction",
  "hint": "Restrict to the 60 sport players, then simplify 20 out of 60.",
  "misconceptions": [
    {"pattern": "used_whole_group", "expect": [1, 5],
     "message": "Given they play sport, restrict to the 60 sport players: 20 ÷ 60 = 1/3. Using all 100 gives 20/100 = 1/5.",
     "note": "20/100 simplifies to 1/5"}
  ],
  "guided_steps": [
    box("How many play sport (the condition)? ", 60,
        "60 play sport.", say="Given they play sport, shrink the world down to the 60 sport players."),
    box("Of those, how many also play music (the overlap)? ", 20,
        "20 do both.", phase="substitute", say="Now count the ones that also match."),
    box("So it is 20 out of 60. Simplify by dividing by 20. Numerator: 20 ÷ 20 = ", 1,
        "20 ÷ 20 = 1.", phase="substitute", say="Simplify the fraction."),
    box("Denominator: 60 ÷ 20 = ", 3, "60 ÷ 20 = 3.", phase="substitute"),
    box("Check: does one third of 60 give the 20 who do both? 60 ÷ 3 = ", 20,
        "Divide 60 by the denominator.", phase="substitute",
        done="20 matches, so P(music given sport) = 1/3.")
  ]
 },
 {  # S5  (RENUMBERED to avoid duplicate 0.3 with S1: was 0.6 x 0.5 = 0.3)
  "display": "P(A|B) = 0.7 and P(B) = 0.5. Find P(A ∩ B).",
  "solutions": [0.35], "calculator": False, "input_type": "single_value",
  "hint": "Multiply the conditional by the condition: P(A|B) times P(B).",
  "misconceptions": [
    {"pattern": "divided_not_multiplied", "expect": 1.4,
     "message": "P(A ∩ B) = P(A|B) × P(B) = 0.7 × 0.5 = 0.35. Dividing instead gives 1.4, which is impossible for a probability.",
     "note": "0.7/0.5 = 1.4"}
  ],
  "guided_steps": [
    box("Write the conditional: P(A|B) = ", 0.7,
        "Given as 0.7.", say="Rearrange the conditional formula: P(A ∩ B) = P(A|B) × P(B)."),
    box("Multiply by P(B): 0.7 × 0.5 = ", 0.35,
        "0.7 × 0.5 = 0.35.", phase="substitute", say="Now finish."),
    box("Check with the formula forwards: P(A|B) = 0.35 ÷ 0.5 = ", 0.7,
        "Divide the overlap by P(B).", phase="substitute",
        done="It returns 0.7, so P(A ∩ B) = 0.35.")
  ]
 },
 {  # S6  (multiple_choice - no guided_steps)
  "display": "Are A and B independent if P(A) = 0.3, P(B) = 0.4, P(A ∩ B) = 0.12? Answer yes or no.",
  "options": ["Yes: \\(P(A) \\times P(B) = P(A \\cap B)\\)", "No: \\(P(A) \\times P(B) \\neq P(A \\cap B)\\)"],
  "solutions": [0], "calculator": False, "input_type": "multiple_choice",
  "hint": "Check whether P(A) times P(B) equals P(A intersect B).",
  "misconceptions": [
    {"pattern": "assumed_dependent", "expect": 1,
     "message": "P(A) × P(B) = 0.3 × 0.4 = 0.12, which equals P(A ∩ B), so the events ARE independent.",
     "note": "picks No"}
  ]
 }
]

problem_bank = {
    "gold": gold, "bronze": bronze, "silver": silver,
    "bronze_description": "Fill the overlap first, then subtract it from each circle and count what is left.",
    "silver_description": "Conditional probability: shrink to the condition, then find the proportion.",
    "gold_description": "Combine several regions or branches: total probability and three-set counting."
}

# ---------------- TIER GUIDES ----------------
tier_guides = {
 "bronze": {
  "title": "Bronze: fill the overlap first",
  "steps": [
    "Two overlapping circles sit inside a rectangle that holds everyone. Always write the middle (both) number in first.",
    "Peel the middle off each circle: only A = A's total minus both, and the same for B. Anything left over goes outside the circles.",
    "All the regions add up to the group total. To turn a region into a probability, divide it by that total."
  ],
  "example": {
    "question": "40 people: 25 like tea (T), 18 like coffee (C), 8 like both. How many like neither?",
    "steps": [
      {"label": "Overlap first", "content": "<p>8 like both. Tea only \\(= 25 - 8 = 17\\), coffee only \\(= 18 - 8 = 10\\).</p>"},
      {"label": "Add the circle regions", "content": "<p>\\(17 + 10 + 8 = 35\\) like at least one drink.</p>"},
      {"label": "Check", "content": "<p>\\(17 + 10 + 8 + 5 = 40\\) ✓</p>"},
      {"label": "Answer", "content": "<p><strong>Neither \\(= 40 - 35 = 5\\)</strong></p>", "isAnswer": True, "is_answer": True}
    ]
  }
 },
 "silver": {
  "title": "Silver: shrink to the condition",
  "steps": [
    "Conditional probability P(A|B) asks: given B has already happened, how likely is A? The world shrinks down to just the B outcomes.",
    "Formula: \\(P(A|B) = \\frac{P(A \\cap B)}{P(B)}\\), the overlap divided by the condition. With counts, it is (in both) ÷ (in B).",
    "For independent events, one has no effect on the other, so \\(P(A \\cap B) = P(A) \\times P(B)\\)."
  ],
  "example": {
    "question": "80 people: 50 speak French (F), 30 speak German (G), 15 both. Find P(G|F).",
    "steps": [
      {"label": "Shrink to the condition", "content": "<p>Given French, use only the 50 French speakers.</p>"},
      {"label": "Divide", "content": "<p>Of those 50, 15 also speak German: \\(P(G|F) = \\frac{15}{50}\\).</p>"},
      {"label": "Check", "content": "<p>\\(0.3 \\times 50 = 15\\) ✓</p>"},
      {"label": "Answer", "content": "<p><strong>\\(P(G|F) = 0.3\\)</strong></p>", "isAnswer": True, "is_answer": True}
    ]
  }
 },
 "gold": {
  "title": "Gold: combine the regions",
  "steps": [
    "Gold problems combine several pieces: three overlapping sets, or branches that split and then recombine.",
    "Total probability: an outcome can arrive by more than one route, so add every route. \\(P(+) = P(+|D)P(D) + P(+|D')P(D')\\).",
    "Three sets add the singles, subtract each pair, then add the triple back: \\(|A \\cup B \\cup C| = |A| + |B| + |C| - |A \\cap B| - |A \\cap C| - |B \\cap C| + |A \\cap B \\cap C|\\)."
  ],
  "example": {
    "question": "A test: P(disease) = 0.02, P(positive|disease) = 0.9, P(positive|healthy) = 0.1. Find P(positive).",
    "steps": [
      {"label": "Two routes", "content": "<p>Disease route: \\(0.02 \\times 0.9 = 0.018\\). Healthy route: \\(0.98 \\times 0.1 = 0.098\\).</p>"},
      {"label": "Add the routes", "content": "<p>\\(0.018 + 0.098 = 0.116\\).</p>"},
      {"label": "Check", "content": "<p>Per 1000: \\(20 \\times 0.9 + 980 \\times 0.1 = 18 + 98 = 116\\), i.e. 0.116 ✓</p>"},
      {"label": "Answer", "content": "<p><strong>\\(P(positive) = 0.116\\)</strong></p>", "isAnswer": True, "is_answer": True}
    ]
  }
 }
}

# ---------------- GUIDED (opener + teach) ----------------
guided = {
 "opener": {
  "label": "Before any formulas",
  "display": "A group of 10 friends.<br>7 like pizza. 5 like burgers. 3 like both.",
  "steps": [
    box("Who likes ONLY pizza, not burgers? ", 4,
        "7 like pizza, but 3 of those also like burgers, so take them out.", post=" people",
        say="No formulas yet. Just picture the group."),
    sayonly("That little subtraction, taking the shared 3 out of the 7, is the whole idea of a <strong>Venn diagram</strong>: fill the overlap first, then peel it off each circle so nobody is counted twice."),
    box("Now only the 5 burger-lovers matter. How many of THEM also like pizza? ", 3,
        "3 people like both, and all 3 are among the burger-lovers.", post=" people"),
    sayonly("You just shrank the world down to the 5 burger-lovers and found 3 like pizza. That is <strong>conditional probability</strong>: given they like burgers, the chance they also like pizza is 3 out of 5. Shrink to the condition, then count.")
  ]
 },
 "teach": {
  "bronze": {
   "display": "A survey of 30 people: 16 own a bike (B), 14 own a scooter (S), 6 own both. How many own neither?",
   "label": "Together: your first one",
   "steps": [
     box("The overlap is given: 6 own both. Bike only: 16 − 6 = ", 10,
         "Take the 6 'both' out of the 16 bike owners.", say="Fill the overlap first, then peel it off each circle."),
     box("Scooter only: 14 − 6 = ", 8, "Take the 6 'both' out of the 14 scooter owners."),
     box("Add the three regions inside the circles: 10 + 8 + 6 = ", 24,
         "Add bike-only, scooter-only and both.", say="These own at least one."),
     box("Everyone else owns neither: 30 − 24 = ", 6,
         "Subtract from the group of 30.", say="Now finish."),
     box("Check every region totals 30: 10 + 8 + 6 + 6 = ", 30,
         "Add all four regions.", done="Every region adds back to 30, so 6 own neither.")
   ]
  },
  "silver": {
   "display": "40 people: 20 own a dog (D), 24 own a cat (C), 5 own both. A dog owner is picked at random. Find P(they also own a cat).",
   "label": "Together: the silver move",
   "steps": [
     box("Given they own a dog, the world shrinks. How many dog owners are there? ", 20,
         "20 own a dog.", say="Conditional probability restricts to the condition."),
     box("Of those 20 dog owners, how many also own a cat (the overlap)? ", 5,
         "5 own both."),
     box("So it is 5 out of 20. As a decimal, 5 ÷ 20 = ", 0.25,
         "5 ÷ 20 = 0.25.", done="That is P(cat given dog)."),
     box("Compare: without the condition, P(cat) = 24 ÷ 40 = ", 0.6,
         "24 ÷ 40 = 0.6.", done="The condition changed the answer from 0.6 to 0.25. That is why 'given' matters.")
   ]
  },
  "gold": {
   "display": "A factory: machine X makes 60% of parts, Y makes 40%. X is faulty 5% of the time, Y is faulty 10%. Find P(a random part is faulty).",
   "label": "Together: the gold move",
   "steps": [
     box("Route through X: P(X) × P(faulty|X) = 0.6 × 0.05 = ", 0.03,
         "Multiply along the X branch.", say="A faulty part can come from either machine. Take each route."),
     box("Route through Y: P(Y) × P(faulty|Y) = 0.4 × 0.10 = ", 0.04,
         "Multiply along the Y branch."),
     box("A part is faulty if it came from EITHER route, so add them: 0.03 + 0.04 = ", 0.07,
         "Add the two branch probabilities.", done="That is the total probability across both machines."),
     box("Sense check with 100 parts: 0.07 × 100 = ", 7,
         "Multiply the probability by 100.", done="About 7 in 100 are faulty, which matches 0.07.")
   ]
  }
 }
}

# worked_examples preserved, but one label has an em dash ("Step 1 — Addition rule")
# which is student-facing and the style gate forbids. Minimal fix: em dash -> colon.
def dedash(o):
    if isinstance(o, dict): return {k: dedash(v) for k, v in o.items()}
    if isinstance(o, list): return [dedash(v) for v in o]
    if isinstance(o, str): return o.replace(" — ", ": ").replace("—", ": ")
    return o

worked_examples = dedash(live["worked_examples"])

# ---------------- ASSEMBLE (preserve untouched fields) ----------------
out = {
    "method_card": method_card,
    "topic_links": live["topic_links"],
    "problem_bank": problem_bank,
    "related_videos": live["related_videos"],
    "worked_examples": worked_examples,
    "tier_guides": tier_guides,
    "guided": guided
}

json.dump(out, io.open("lesson_probability-statistics-L02.json", "w", encoding="utf-8"),
          indent=1, ensure_ascii=False)
print("written lesson_probability-statistics-L02.json")
