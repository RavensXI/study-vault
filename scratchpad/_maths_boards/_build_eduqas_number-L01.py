# -*- coding: utf-8 -*-
"""Build guided practice_data for maths-eduqas number-L01 (BIDMAS)."""
import json, io

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def say(s):
    return {"say": s}

def mc(pattern, expect, message, note=None):
    d = {"pattern": pattern, "check": pattern, "expect": expect, "message": message}
    if note: d["note"] = note
    return d

# ---------- PROBLEM BANK ----------
bronze = [
 {"display": "\\(6 + 4 \\times 3\\)", "solutions":[18], "calculator":False, "input_type":"single_value",
  "hint":"Multiply before you add: do 4 × 3 first.",
  "misconceptions":[mc("left_to_right",30,"Multiply before adding: 4 × 3 = 12, then 6 + 12 = 18.","(6+4)x3=30")],
  "guided_steps":[
    say("No brackets or indices. Multiplication comes before addition, so do 4 × 3 first."),
    box("4 × 3 = ",12,"Just the multiplication."),
    box("6 + 12 = ",18,"Add the two numbers.",say="Now it is 6 + 12.",phase="substitute"),
    box("Check: 18 − 6 = ",12,"Take the 6 back off.",done="That is 4 × 3, so 18 is right.",phase="substitute"),
  ]},
 {"display": "\\(20 - 8 \\div 2\\)", "solutions":[16], "calculator":False, "input_type":"single_value",
  "hint":"Divide before you subtract: do 8 ÷ 2 first.",
  "misconceptions":[mc("left_to_right",6,"Divide first: 8 ÷ 2 = 4, then 20 − 4 = 16.","(20-8)/2=6")],
  "guided_steps":[
    say("No brackets or indices. Division comes before subtraction, so do 8 ÷ 2 first."),
    box("8 ÷ 2 = ",4,"Just the division."),
    box("20 − 4 = ",16,"Subtract.",say="Now it is 20 − 4.",phase="substitute"),
    box("Check: 16 + 4 = ",20,"Add the 4 back on.",done="That rebuilds the 20, so 16 is right.",phase="substitute"),
  ]},
 {"display": "\\(3 + 5 \\times 2\\)", "solutions":[13], "calculator":False, "input_type":"single_value",
  "hint":"Multiply before you add: do 5 × 2 first.",
  "misconceptions":[mc("left_to_right",16,"Multiply first: 5 × 2 = 10, then 3 + 10 = 13.","(3+5)x2=16")],
  "guided_steps":[
    say("No brackets or indices. Multiply before you add, so do 5 × 2 first."),
    box("5 × 2 = ",10,"Just the multiplication."),
    box("3 + 10 = ",13,"Add.",say="Now it is 3 + 10.",phase="substitute"),
    box("Check: 13 − 3 = ",10,"Take the 3 back off.",done="That is 5 × 2, so 13 is right.",phase="substitute"),
  ]},
 {"display": "\\(24 \\div 6 + 2\\)", "solutions":[6], "calculator":False, "input_type":"single_value",
  "hint":"Divide before you add: do 24 ÷ 6 first.",
  "misconceptions":[mc("add_first",3,"Divide first: 24 ÷ 6 = 4, then 4 + 2 = 6.","24/(6+2)=3")],
  "guided_steps":[
    say("Division outranks addition, so do 24 ÷ 6 first."),
    box("24 ÷ 6 = ",4,"Just the division."),
    box("4 + 2 = ",6,"Add.",say="Now it is 4 + 2.",phase="substitute"),
    box("Check: 6 − 2 = ",4,"Take the 2 back off.",done="That is 24 ÷ 6, so 6 is right.",phase="substitute"),
  ]},
 {"display": "\\(10 - 3 + 7\\)", "solutions":[14], "calculator":False, "input_type":"single_value",
  "hint":"Add and subtract are equal priority, so work left to right.",
  "misconceptions":[mc("wrong_order",0,"Left to right: 10 − 3 = 7, then 7 + 7 = 14.","10-(3+7)=0")],
  "guided_steps":[
    say("Only subtraction and addition here, equal priority, so work left to right. Subtract first."),
    box("10 − 3 = ",7,"Left to right, so subtract first."),
    box("7 + 7 = ",14,"Add the 7.",say="Now add the 7.",phase="substitute"),
    box("Check: 14 − 7 + 3 = ",10,"Undo: take off 7, add the 3 back.",done="That rebuilds the 10, so 14 is right.",phase="substitute"),
  ]},
 {"display": "\\(2 \\times 5 + 4 \\times 3\\)", "solutions":[22], "calculator":False, "input_type":"single_value",
  "hint":"Do both multiplications first, then add the two results.",
  "misconceptions":[mc("left_to_right",42,"Do both multiplications first: 2 × 5 = 10 and 4 × 3 = 12, then 10 + 12 = 22.","2x5=10,+4=14,x3=42")],
  "guided_steps":[
    say("Two separate multiplications, both done before the add. Work out each one."),
    box("2 × 5 = ",10,"First multiplication."),
    box("4 × 3 = ",12,"Second multiplication."),
    box("10 + 12 = ",22,"Add.",say="Now add the two parts: 10 + 12.",phase="substitute"),
    box("Check: 22 − 12 = ",10,"Take the 12 back off.",done="That is 2 × 5, so 22 is right.",phase="substitute"),
  ]},
 {"display": "\\(18 \\div 3 \\times 2\\)", "solutions":[12], "calculator":False, "input_type":"single_value",
  "hint":"Divide and multiply are equal priority, so work left to right.",
  "misconceptions":[mc("right_first",3,"Left to right: 18 ÷ 3 = 6, then 6 × 2 = 12.","18/(3x2)=3")],
  "guided_steps":[
    say("Divide and multiply are equal priority, so work left to right. Divide first."),
    box("18 ÷ 3 = ",6,"Left operation first."),
    box("6 × 2 = ",12,"Multiply.",say="Now multiply: 6 × 2.",phase="substitute"),
    box("Check: 12 ÷ 2 = ",6,"Divide by the last 2.",done="That is 18 ÷ 3, so 12 is right.",phase="substitute"),
  ]},
 {"display": "\\(14 - 8 \\div 2\\)", "solutions":[10], "calculator":False, "input_type":"single_value",
  "hint":"Divide before you subtract: do 8 ÷ 2 first.",
  "misconceptions":[mc("left_to_right",3,"Divide first: 8 ÷ 2 = 4, then 14 − 4 = 10.","(14-8)/2=3")],
  "guided_steps":[
    say("Division comes before subtraction, so do 8 ÷ 2 first."),
    box("8 ÷ 2 = ",4,"Just the division."),
    box("14 − 4 = ",10,"Subtract.",say="Now it is 14 − 4.",phase="substitute"),
    box("Check: 10 + 4 = ",14,"Add the 4 back on.",done="That rebuilds the 14, so 10 is right.",phase="substitute"),
  ]},
]

silver = [
 {"display": "\\((3 + 5) \\times 4\\)", "solutions":[32], "calculator":False, "input_type":"single_value",
  "hint":"Brackets first (3 + 5), then multiply.",
  "misconceptions":[mc("no_bracket",23,"Do the brackets first: 3 + 5 = 8, then 8 × 4 = 32.","ignore bracket: 3+5x4=23")],
  "guided_steps":[
    say("Brackets first: work out 3 + 5."),
    box("3 + 5 = ",8,"Just inside the brackets."),
    box("8 × 4 = ",32,"Multiply.",say="Now multiply the bracket result by 4.",phase="substitute"),
    box("Check: 32 ÷ 4 = ",8,"Divide by the 4.",done="That is 3 + 5, so 32 is right.",phase="substitute"),
  ]},
 {"display": "\\(4^2 + 3 \\times 5\\)", "solutions":[31], "calculator":False, "input_type":"single_value",
  "hint":"Index first (4² = 16), then multiply, then add.",
  "misconceptions":[
    mc("index_error",23,"4² means 4 × 4 = 16, not 4 × 2 = 8. Then add 3 × 5 = 15 to get 31.","4^2=8: 8+15=23"),
    mc("add_before_multiply",95,"Multiply 3 × 5 = 15 before adding it to 16, not 16 + 3 = 19 then × 5.","(16+3)x5=95"),
  ],
  "guided_steps":[
    say("Indices first: work out 4²."),
    box("4² = ",16,"4 × 4."),
    box("3 × 5 = ",15,"Multiply before adding."),
    box("16 + 15 = ",31,"Add.",say="Now add the two parts: 16 + 15.",phase="substitute"),
    box("Check: 31 − 15 = ",16,"Take the 15 back off.",done="That is 4², so 31 is right.",phase="substitute"),
  ]},
 {"display": "\\(50 - (4 + 6)^2\\)", "solutions":[-50], "calculator":False, "input_type":"single_value",
  "hint":"Brackets first (4 + 6), then square, then subtract.",
  "misconceptions":[mc("no_bracket",10,"Add inside the bracket first: 4 + 6 = 10, then square: 10² = 100, then 50 − 100 = −50.","4+6^2=40: 50-40=10")],
  "guided_steps":[
    say("Brackets first, then its index. Work out 4 + 6."),
    box("4 + 6 = ",10,"Inside the bracket."),
    box("10² = ",100,"The index on the bracket: 10 × 10."),
    box("50 − 100 = ",-50,"Fifty take away one hundred drops below zero.",say="Now subtract: 50 − 100.",phase="substitute"),
    box("Check: −50 + 100 = ",50,"Add the 100 back on.",done="That rebuilds the 50, so −50 is right.",phase="substitute"),
  ]},
 {"display": "\\(36 \\div (2 + 4) \\times 3\\)", "solutions":[18], "calculator":False, "input_type":"single_value",
  "hint":"Bracket first (2 + 4), then divide and multiply left to right.",
  "misconceptions":[
    mc("multiply_before_divide",2,"After the bracket, work left to right: divide before you multiply. 36 ÷ 6 = 6, then 6 × 3 = 18.","36/(6x3)=2"),
    mc("no_bracket",66,"Do the bracket first: 2 + 4 = 6, then 36 ÷ 6 = 6, then × 3 = 18.","ignore bracket: 36/2=18,+4=22,x3=66"),
  ],
  "guided_steps":[
    say("Brackets first: work out 2 + 4."),
    box("2 + 4 = ",6,"Inside the bracket."),
    box("36 ÷ 6 = ",6,"Divide first, working left to right."),
    box("6 × 3 = ",18,"Multiply.",say="Now multiply: 6 × 3.",phase="substitute"),
    box("Check: 18 ÷ 3 = ",6,"Divide by the last 3.",done="That is 36 ÷ 6, so 18 is right.",phase="substitute"),
  ]},
 {"display": "\\(2 \\times (9 - 4)^2\\)", "solutions":[50], "calculator":False, "input_type":"single_value",
  "hint":"Bracket first (9 − 4), then its square, then multiply.",
  "misconceptions":[mc("index_first",-14,"Do the bracket before squaring: 9 − 4 = 5, then 5² = 25. Squaring the 4 first gives the wrong sign.","9-4^2=-7: 2x-7=-14")],
  "guided_steps":[
    say("Brackets first, then its index. Work out 9 − 4."),
    box("9 − 4 = ",5,"Inside the bracket."),
    box("5² = ",25,"The index: 5 × 5."),
    box("2 × 25 = ",50,"Multiply.",say="Now multiply: 2 × 25.",phase="substitute"),
    box("Check: 50 ÷ 2 = ",25,"Divide by the 2.",done="That is 5², so 50 is right.",phase="substitute"),
  ]},
 {"display": "\\(100 \\div (5^2)\\)", "solutions":[4], "calculator":False, "input_type":"single_value",
  "hint":"Work out the index inside the brackets first: 5² = 25.",
  "misconceptions":[mc("index_error",10,"5² means 5 × 5 = 25, not 5 × 2 = 10. Then 100 ÷ 25 = 4.","5^2=10: 100/10=10")],
  "guided_steps":[
    say("Work out the index inside the brackets first: 5²."),
    box("5² = ",25,"5 × 5."),
    box("100 ÷ 25 = ",4,"Divide.",say="Now divide: 100 ÷ 25.",phase="substitute"),
    box("Check: 4 × 25 = ",100,"Multiply back by the 25.",done="That rebuilds the 100, so 4 is right.",phase="substitute"),
  ]},
 {"display": "\\(7 + 2 \\times (8 - 3)\\)", "solutions":[17], "calculator":False, "input_type":"single_value",
  "hint":"Bracket first (8 − 3), then multiply, then add.",
  "misconceptions":[mc("add_before_multiply",45,"Multiply before adding: 8 − 3 = 5, then 2 × 5 = 10, then 7 + 10 = 17. Adding 7 + 2 first is the slip.","(7+2)x5=45")],
  "guided_steps":[
    say("Brackets first: work out 8 − 3."),
    box("8 − 3 = ",5,"Inside the bracket."),
    box("2 × 5 = ",10,"Multiply before adding."),
    box("7 + 10 = ",17,"Add.",say="Now add: 7 + 10.",phase="substitute"),
    box("Check: 17 − 7 = ",10,"Take the 7 back off.",done="That is 2 × 5, so 17 is right.",phase="substitute"),
  ]},
]

gold = [
 {"display": "\\(\\dfrac{18 + 6}{2^2} + 5 \\times 3\\)", "solutions":[21], "calculator":False, "input_type":"single_value",
  "hint":"Treat the fraction bar as brackets: work out the top and bottom separately, then divide.",
  "misconceptions":[
    mc("no_fraction_bracket",34.5,"The fraction bar groups the whole top: work out 18 + 6 = 24 before dividing by 4.","6/2^2=1.5: 18+1.5+15=34.5"),
    mc("index_error",27,"2² = 4, not 2. So 24 ÷ 4 = 6, then + 15 = 21.","denom 2^2=2: 24/2+15=27"),
  ],
  "guided_steps":[
    say("The fraction bar acts like brackets. Work out the top: 18 + 6."),
    box("18 + 6 = ",24,"Top of the fraction."),
    box("2² = ",4,"The bottom: 2 × 2."),
    box("24 ÷ 4 = ",6,"Divide top by bottom."),
    box("5 × 3 = ",15,"The other term: multiply before adding."),
    box("6 + 15 = ",21,"Add the two parts.",say="Now add the two parts: 6 + 15.",phase="substitute"),
    box("Check: 21 − 15 = ",6,"Take the 15 back off.",done="That is the fraction value 24 ÷ 4, so 21 is right.",phase="substitute"),
  ]},
 {"display": "\\((2 + 3)^2 - 4 \\times (7 - 5)\\)", "solutions":[17], "calculator":False, "input_type":"single_value",
  "hint":"Both brackets first, then the index, then multiply, then subtract.",
  "misconceptions":[
    mc("square_separately",5,"(2 + 3)² means square the bracket total: 5² = 25, not 2² + 3² = 13.","(2+3)^2=13: 13-8=5"),
    mc("subtract_before_multiply",42,"Multiply 4 × 2 = 8 before subtracting: 25 − 8 = 17, not (25 − 4) × 2.","(25-4)x2=42"),
  ],
  "guided_steps":[
    say("Both brackets first: 2 + 3 and 7 − 5."),
    box("2 + 3 = ",5,"First bracket."),
    box("7 − 5 = ",2,"Second bracket."),
    box("5² = ",25,"The index on the first bracket: 5 × 5."),
    box("4 × 2 = ",8,"Multiply the 4 by the second bracket."),
    box("25 − 8 = ",17,"Subtract.",say="Now subtract: 25 − 8.",phase="substitute"),
    box("Check: 17 + 8 = ",25,"Add the 8 back on.",done="That is 5², so 17 is right.",phase="substitute"),
  ]},
 {"display": "\\(\\dfrac{3^3 - 7}{2 \\times 5}\\)", "solutions":[2], "calculator":False, "input_type":"single_value",
  "hint":"Work out the whole top and the whole bottom separately, then divide.",
  "misconceptions":[mc("index_error",0.2,"3³ means 3 × 3 × 3 = 27, not 3 × 3 = 9. Top is 27 − 7 = 20, bottom is 10, so 20 ÷ 10 = 2.","3^3=9: (9-7)/10=0.2")],
  "guided_steps":[
    say("The fraction bar groups the whole top and the whole bottom. Start with the top: 3³."),
    box("3³ = ",27,"3 × 3 × 3."),
    box("27 − 7 = ",20,"Finish the top."),
    box("2 × 5 = ",10,"The bottom."),
    box("20 ÷ 10 = ",2,"Divide.",say="Now divide top by bottom: 20 ÷ 10.",phase="substitute"),
    box("Check: 2 × 10 = ",20,"Multiply back by the 10.",done="That is the top, 27 − 7, so 2 is right.",phase="substitute"),
  ]},
 {"display": "\\((-3)^2 + 4 \\times (-2)\\)", "solutions":[1], "calculator":False, "input_type":"single_value",
  "hint":"Square the bracket first, remembering a negative times a negative is positive.",
  "misconceptions":[
    mc("sign_error",-17,"(−3)² = (−3) × (−3) = 9, a positive, because a negative times a negative is positive.","(-3)^2=-9: -9-8=-17"),
    mc("sign_error_product",17,"4 × (−2) = −8. A positive times a negative is negative, so this part lowers the total.","4x-2=+8: 9+8=17"),
  ],
  "guided_steps":[
    say("Indices first. Square the bracket: (−3)², remembering a negative times a negative is positive."),
    box("(−3) × (−3) = ",9,"Negative times negative is positive."),
    box("4 × (−2) = ",-8,"Positive times negative is negative."),
    box("9 + (−8) = ",1,"Adding a negative is the same as subtracting 8.",say="Now add the two parts: 9 + (−8).",phase="substitute"),
    box("Check: 1 + 8 = ",9,"Add the 8 back on.",done="That is (−3)², so 1 is right.",phase="substitute"),
  ]},
 {"display": "\\(\\sqrt{49} + 2^3 \\times 3 - 8\\)", "solutions":[23], "calculator":False, "input_type":"single_value",
  "hint":"Roots and indices first, then multiply, then add and subtract left to right.",
  "misconceptions":[
    mc("index_error",17,"2³ = 2 × 2 × 2 = 8, not 2 × 3 = 6. Then 8 × 3 = 24, and 7 + 24 − 8 = 23.","2^3=6: 7+18-8=17"),
    mc("add_before_multiply",37,"Multiply 2³ × 3 = 24 before adding the 7: 7 + 24 − 8 = 23, not (7 + 8) × 3 − 8.","(7+8)x3-8=37"),
  ],
  "guided_steps":[
    say("Indices and roots first: √49 and 2³."),
    box("√49 = ",7,"What number times itself is 49?"),
    box("2³ = ",8,"2 × 2 × 2."),
    box("8 × 3 = ",24,"Multiply before adding."),
    box("7 + 24 = ",31,"Add first, working left to right.",say="Now work left to right: add 7 + 24 first.",phase="substitute"),
    box("31 − 8 = ",23,"Now take off 8.",phase="substitute"),
    box("Check: 23 + 8 − 24 = ",7,"Undo: add the 8, take off 24.",done="That rebuilds the √49 value, so 23 is right.",phase="substitute"),
  ]},
]

problem_bank = {
 "bronze": bronze, "silver": silver, "gold": gold,
 "bronze_description": "One calculation mixing a times or divide with an add or subtract, or two equal operations: do any times or divide first, then work left to right.",
 "silver_description": "Brackets and powers join in: sort out brackets first, then indices, before any times, divide, add or subtract.",
 "gold_description": "Fraction bars, roots, negatives and nested brackets: treat the top and bottom of a fraction as bracketed, then finish with the outer operations.",
}

# ---------- TIER GUIDES ----------
tier_guides = {
 "bronze": {
  "title": "Bronze: one operation outranks the other",
  "steps": [
   "<strong>BIDMAS</strong> sets the order: Brackets, Indices, Division and Multiplication, then Addition and Subtraction.",
   "At Bronze, each calculation mixes a times or divide with an add or subtract. Always do the times or divide first.",
   "When two operations share a tier (both + and −, or both × and ÷), just work left to right.",
  ],
  "example": {"question":"Work out 18 ÷ 6 + 5", "steps":[
    {"label":"Divide first","content":"18 ÷ 6 = 3"},
    {"label":"Then add","content":"3 + 5 = 8"},
    {"label":"Check","content":"8 − 5 = 3, which is 18 ÷ 6"},
    {"label":"Answer","content":"8","isAnswer":True,"is_answer":True},
  ]},
 },
 "silver": {
  "title": "Silver: powers and brackets step in",
  "steps": [
   "Now calculations include indices (powers like \\(2^3\\)) and brackets.",
   "Do everything inside brackets first, then indices, before any times, divide, add or subtract.",
   "Inside a bracket, BIDMAS still applies, so sort out any power there before you add.",
  ],
  "example": {"question":"Work out 40 − 2 × 3²", "steps":[
    {"label":"Index first","content":"3² = 9"},
    {"label":"Multiply","content":"2 × 9 = 18"},
    {"label":"Subtract","content":"40 − 18 = 22"},
    {"label":"Check","content":"22 + 18 = 40"},
    {"label":"Answer","content":"22","isAnswer":True,"is_answer":True},
  ]},
 },
 "gold": {
  "title": "Gold: fractions, roots and nested brackets",
  "steps": [
   "A fraction bar groups the whole top and the whole bottom, like invisible brackets around each.",
   "Work out the top and bottom fully, then divide. Roots such as \\(\\sqrt{49}\\) count as indices.",
   "Watch signs: \\((-3)^2\\) is a positive, and for brackets inside brackets, start with the innermost pair.",
  ],
  "example": {"question":"Work out (8 + 8) ÷ 2³ + √16", "steps":[
    {"label":"Top and bottom","content":"8 + 8 = 16 and 2³ = 8"},
    {"label":"Divide","content":"16 ÷ 8 = 2"},
    {"label":"Root","content":"√16 = 4"},
    {"label":"Add","content":"2 + 4 = 6"},
    {"label":"Check","content":"6 − 4 = 2, the fraction value"},
    {"label":"Answer","content":"6","isAnswer":True,"is_answer":True},
  ]},
 },
}

# ---------- GUIDED (opener + teach) ----------
guided = {
 "opener": {"steps":[
   say("A snack order, no maths rules needed, just common sense. You buy 1 baguette for £4 and 3 bottles of water at £2 each."),
   box("Total cost, in £: £",10,"The three waters come to £6. Add on the £4 baguette."),
   say("Notice what you did: you worked out the three waters (3 × £2 = £6) BEFORE adding the baguette. You did the multiplication first without being told. That is the whole rule: <strong>multiplication before addition</strong>. As maths it is \\(4 + 3 \\times 2\\), and the answer is 10, not 14."),
   box("Now change from a £20 note after buying 4 pens at £3 each, in £: £",8,"Four pens cost £12. Take that off £20."),
   say("Again you multiplied first (4 pens = £12) then subtracted, giving £8. That is <strong>BIDMAS</strong>: Brackets, Indices, Division and Multiplication, then Addition and Subtraction. The steps ahead just apply this rule to bigger calculations."),
 ]},
 "teach": {
  "bronze": {"display":"Work out \\(4 + 7 \\times 2 - 3\\)", "steps":[
    say("No brackets or indices here. Multiplication comes before add and subtract, so do 7 × 2 first."),
    box("7 × 2 = ",14,"Just the multiplication."),
    say("Now add and subtract, left to right: 4 + 14, then take off 3."),
    box("4 + 14 = ",18,"Add first, working left to right."),
    box("18 − 3 = ",15,"Now subtract the 3."),
    box("Check: 15 + 3 − 14 = ",4,"Undo the steps: add the 3, take off 14.",done="That rebuilds the 4 you started with. Multiply first was the whole point."),
  ]},
  "silver": {"display":"Work out \\(60 - 4 \\times 2^3\\)", "steps":[
    say("Now a power appears. Indices come before multiplication, so work out 2³ first."),
    box("2³ = ",8,"2 × 2 × 2."),
    say("Now multiply before subtracting: 4 × 8."),
    box("4 × 8 = ",32,"Multiply."),
    say("Now the subtraction: 60 − 32."),
    box("60 − 32 = ",28,"Subtract."),
    box("Check: 28 + 32 = ",60,"Add the 32 back on.",done="That rebuilds the 60. Doing the index first was the whole point."),
  ]},
  "gold": {"display":"Work out \\(\\dfrac{20 + 4}{2^3} + \\sqrt{25}\\)", "steps":[
    say("The fraction bar groups the whole top and the whole bottom. Work out the top: 20 + 4."),
    box("20 + 4 = ",24,"Top of the fraction."),
    say("Now the bottom: 2³."),
    box("2³ = ",8,"2 × 2 × 2."),
    say("Divide top by bottom: 24 ÷ 8."),
    box("24 ÷ 8 = ",3,"Divide."),
    say("Now the root: √25."),
    box("√25 = ",5,"What number times itself is 25?"),
    say("Now add the two parts: 3 + 5."),
    box("3 + 5 = ",8,"Add."),
    box("Check: 8 − 5 = ",3,"Take the root back off.",done="That is the fraction value 24 ÷ 8. Treating the bar as brackets was the whole point."),
  ]},
 },
}

# ---------- METHOD CARD (slim) ----------
method_card = {
 "title": "How to Use BIDMAS (Order of Operations)",
 "steps": [
  "Brackets first (innermost pair outward).",
  "Then Indices: powers and roots.",
  "Then Division and Multiplication, left to right.",
  "Then Addition and Subtraction, left to right.",
 ],
 "content": "<p><strong>BIDMAS</strong> gives the order for a calculation: <strong>B</strong>rackets, <strong>I</strong>ndices, <strong>D</strong>ivision and <strong>M</strong>ultiplication, <strong>A</strong>ddition and <strong>S</strong>ubtraction.</p><p>Division and multiplication share a tier, so work them left to right; the same goes for addition and subtraction. A fraction bar groups its whole top and bottom like brackets.</p>",
 "example": "<p><strong>Calculate</strong> \\(5 + 2 \\times 3^2 - (8 \\div 4)\\)</p><p>Bracket: \\(8 \\div 4 = 2\\). Index: \\(3^2 = 9\\). Multiply: \\(2 \\times 9 = 18\\). Then \\(5 + 18 - 2 = 21\\).</p>",
}

# ---------- PRESERVED (from live) ----------
live = json.load(io.open("_live_number-L01.json", encoding="utf-8"))
topic_links = live["topic_links"]
related_videos = live["related_videos"]
worked_examples = live["worked_examples"]

pd = {
 "method_card": method_card,
 "topic_links": topic_links,
 "problem_bank": problem_bank,
 "tier_guides": tier_guides,
 "guided": guided,
 "related_videos": related_videos,
 "worked_examples": worked_examples,
}

io.open("lesson_maths-eduqas_number-L01.json","w",encoding="utf-8").write(json.dumps(pd,indent=1,ensure_ascii=False))
print("written lesson_maths-eduqas_number-L01.json")
# quick self-check: solution uniqueness per tier
for t in ("bronze","silver","gold"):
    sols=[tuple(p["solutions"]) for p in problem_bank[t]]
    dup=set([x for x in sols if sols.count(x)>1])
    print(t, "dups:", dup if dup else "none")
