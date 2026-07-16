# -*- coding: utf-8 -*-
import json, io

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def say(s):
    return {"say": s}

def direct_unit(unit_pre, unit_ans, unit_hint, decide, mid_say,
                ans_pre, ans_ans, ans_hint, chk_pre, chk_ans, chk_hint, chk_done):
    return [
        say(decide),
        box(unit_pre, unit_ans, unit_hint),
        say(mid_say),
        box(ans_pre, ans_ans, ans_hint, phase="substitute"),
        box(chk_pre, chk_ans, chk_hint, done=chk_done),
    ]

def inverse_k(decide, k_pre, k_ans, k_hint, mid_say,
              ans_pre, ans_ans, ans_hint, chk_pre, chk_ans, chk_hint, chk_done):
    steps = [say(decide), box(k_pre, k_ans, k_hint)]
    if mid_say: steps.append(say(mid_say))
    steps.append(box(ans_pre, ans_ans, ans_hint, phase="substitute"))
    steps.append(box(chk_pre, chk_ans, chk_hint, done=chk_done))
    return steps

# ===== BRONZE =====
bronze = []

bronze.append({
 "display": "3 pizzas cost £21. How much do 5 pizzas cost?",
 "solutions": [35], "calculator": False, "input_type": "single_value",
 "hint": "Find the cost of one pizza, then multiply by five.",
 "misconceptions": [{"pattern":"forgot_step","check":"common","expect":7,
   "message":"One pizza = 21 ÷ 3 = £7. Five = 7 × 5 = £35. Do not stop at the one-pizza price."}],
 "guided_steps": direct_unit(
   "One pizza: 21 ÷ 3 = £", 7, "Share £21 between 3 pizzas.",
   "Direct or inverse? More pizzas cost more, so direct. Find one, then scale.",
   "So one pizza is £7, the constant.",
   "Five pizzas: 5 × 7 = £", 35, "Five lots of the one-pizza price.",
   "Check: 35 ÷ 5 = £", 7, "Divide back to the one-pizza price.",
   "Back to £7 each, so £35 is right."),
})

bronze.append({
 "display": "A car uses 8 litres of fuel to travel 96 km. How far can it travel on 5 litres?",
 "solutions": [60], "calculator": False, "input_type": "single_value",
 "hint": "Work out the distance on one litre, then multiply by five.",
 "misconceptions": [{"pattern":"forgot_step","check":"common","expect":12,
   "message":"One litre = 96 ÷ 8 = 12 km. Five litres = 5 × 12 = 60 km."}],
 "guided_steps": direct_unit(
   "One litre: 96 ÷ 8 = ", 12, "Share 96 km between 8 litres.",
   "Direct or inverse? More fuel goes further, so direct.",
   "So one litre gives 12 km, the constant.",
   "Five litres: 5 × 12 = ", 60, "Five lots of 12 km.",
   "Check: 60 ÷ 5 = ", 12, "Divide back to km per litre.",
   "12 km per litre again, so 60 km is right."),
})

bronze.append({
 "display": "6 identical bars weigh 900 g. What do 10 bars weigh (in grams)?",
 "solutions": [1500], "calculator": False, "input_type": "single_value",
 "hint": "Find the weight of one bar, then multiply by ten.",
 "misconceptions": [{"pattern":"forgot_step","check":"common","expect":150,
   "message":"One bar = 900 ÷ 6 = 150 g. Ten = 10 × 150 = 1500 g."}],
 "guided_steps": direct_unit(
   "One bar: 900 ÷ 6 = ", 150, "Share 900 g between 6 bars.",
   "Direct or inverse? More bars weigh more, so direct.",
   "So one bar is 150 g, the constant.",
   "Ten bars: 10 × 150 = ", 1500, "Ten lots of 150 g.",
   "Check: 1500 ÷ 10 = ", 150, "Divide back to the one-bar weight.",
   "150 g each again, so 1500 g is right."),
})

bronze.append({
 "display": "A recipe for 6 pancakes uses 180 g of flour. How much flour for 10 pancakes?",
 "solutions": [300], "calculator": False, "input_type": "single_value",
 "hint": "Find the flour for one pancake, then multiply by ten.",
 "misconceptions": [{"pattern":"forgot_step","check":"common","expect":30,
   "message":"One pancake = 180 ÷ 6 = 30 g. Ten = 10 × 30 = 300 g."}],
 "guided_steps": direct_unit(
   "One pancake: 180 ÷ 6 = ", 30, "Share 180 g between 6 pancakes.",
   "Direct or inverse? More pancakes need more flour, so direct.",
   "So one pancake needs 30 g, the constant.",
   "Ten pancakes: 10 × 30 = ", 300, "Ten lots of 30 g.",
   "Check: 300 ÷ 10 = ", 30, "Divide back to flour per pancake.",
   "30 g each again, so 300 g is right."),
})

bronze.append({
 "display": "2 workers take 8 hours to paint a fence. How long for 4 workers?",
 "solutions": [4], "calculator": False, "input_type": "single_value",
 "hint": "Inverse: multiply the two numbers for the constant, then divide by the new number of workers.",
 "misconceptions": [{"pattern":"inverse_error","check":"common","expect":16,
   "message":"Inverse proportion: more workers, less time. Constant = 2 × 8 = 16. Time = 16 ÷ 4 = 4 hours. Answering 16 treats it as direct."}],
 "guided_steps": inverse_k(
   "Direct or inverse? More workers, less time, so inverse. Multiply the pair for the constant.",
   "Constant: 2 × 8 = ", 16, "Multiply workers by hours.",
   "16 worker-hours, and that never changes.",
   "For 4 workers: 16 ÷ 4 = ", 4, "Divide the constant by 4 workers.",
   "Check: 4 × 4 = ", 16, "Multiply back to the constant.",
   "Back to 16 worker-hours, so 4 hours is right."),
})

bronze.append({
 "display": "3 printers finish a batch in 12 hours. How long would 4 printers take?",
 "solutions": [9], "calculator": False, "input_type": "single_value",
 "hint": "Inverse: multiply printers by hours for the constant, then divide by the new number of printers.",
 "misconceptions": [{"pattern":"inverse_error","check":"common","expect":16,
   "message":"Inverse proportion: more printers, less time. Constant = 3 × 12 = 36. Time = 36 ÷ 4 = 9 hours. Answering 16 treats it as direct."}],
 "guided_steps": inverse_k(
   "Direct or inverse? More printers, less time, so inverse. Multiply the pair for the constant.",
   "Constant: 3 × 12 = ", 36, "Multiply printers by hours.",
   "36 printer-hours, fixed for the batch.",
   "For 4 printers: 36 ÷ 4 = ", 9, "Divide the constant by 4 printers.",
   "Check: 4 × 9 = ", 36, "Multiply back to the constant.",
   "Back to 36 printer-hours, so 9 hours is right."),
})

bronze.append({
 "display": "12 sweets cost £1.80. How much do 20 sweets cost?",
 "solutions": [3], "calculator": False, "input_type": "single_value",
 "hint": "Find the cost of one sweet, then multiply by twenty.",
 "misconceptions": [{"pattern":"forgot_step","check":"common","expect":0.15,
   "message":"One sweet = 1.80 ÷ 12 = £0.15. Twenty = 20 × 0.15 = £3."}],
 "guided_steps": direct_unit(
   "One sweet: 1.80 ÷ 12 = £", 0.15, "Share £1.80 between 12 sweets.",
   "Direct or inverse? More sweets cost more, so direct.",
   "So one sweet is 15p, the constant.",
   "Twenty sweets: 20 × 0.15 = £", 3, "Twenty lots of 15p.",
   "Check: 3 ÷ 20 = £", 0.15, "Divide back to the one-sweet price.",
   "15p each again, so £3 is right."),
})

bronze.append({
 "display": "4 taps fill a tank in 12 hours. How long for 6 taps?",
 "solutions": [8], "calculator": False, "input_type": "single_value",
 "hint": "Inverse: multiply taps by hours for the constant, then divide by the new number of taps.",
 "misconceptions": [{"pattern":"inverse_error","check":"common","expect":18,
   "message":"Inverse proportion: more taps, less time. Constant = 4 × 12 = 48. Time = 48 ÷ 6 = 8 hours. Answering 18 treats it as direct."}],
 "guided_steps": inverse_k(
   "Direct or inverse? More taps, less time, so inverse. Multiply the pair for the constant.",
   "Constant: 4 × 12 = ", 48, "Multiply taps by hours.",
   "48 tap-hours, fixed for the tank.",
   "For 6 taps: 48 ÷ 6 = ", 8, "Divide the constant by 6 taps.",
   "Check: 6 × 8 = ", 48, "Multiply back to the constant.",
   "Back to 48 tap-hours, so 8 hours is right."),
})

# ===== SILVER =====
silver = []

silver.append({
 "display": "\\(y\\) is directly proportional to \\(x\\). When \\(x = 3\\), \\(y = 15\\). Find \\(y\\) when \\(x = 7\\).",
 "solutions": [35], "calculator": False, "input_type": "single_value",
 "hint": "Direct: divide y by x to find k, then multiply the new x by k.",
 "misconceptions": [{"pattern":"wrong_formula","check":"common","expect":19,
   "message":"Do not add the change on. \\(y = kx\\), so k = 15 ÷ 3 = 5 and y = 5 × 7 = 35. Adding 4 to 15 to get 19 treats it as adding, not scaling."}],
 "guided_steps": [
   say("Direct proportion: \\(y = kx\\). Find k first."),
   box("k = y ÷ x = 15 ÷ 3 = ", 5, "Divide y by x."),
   say("So the rule is \\(y = 5x\\)."),
   box("y = 5 × 7 = ", 35, "Multiply the new x by k.", phase="substitute"),
   box("Check: 35 ÷ 7 = ", 5, "Must give k = 5 again.", done="Same k, so y = 35 is right."),
 ],
})

silver.append({
 "display": "\\(y\\) is inversely proportional to \\(x\\). When \\(x = 4\\), \\(y = 6\\). Find \\(y\\) when \\(x = 8\\).",
 "solutions": [3], "calculator": False, "input_type": "single_value",
 "hint": "Inverse: multiply x by y to find k, then divide k by the new x.",
 "misconceptions": [{"pattern":"inverse_error","check":"common","expect":12,
   "message":"Inverse means \\(k = xy\\), so k = 4 × 6 = 24 and y = 24 ÷ 8 = 3. Doubling x should halve y, not double it to 12."}],
 "guided_steps": inverse_k(
   "Inverse: \\(y = k/x\\), so \\(k = xy\\).",
   "k = 4 × 6 = ", 24, "Multiply x and y.",
   None,
   "y = 24 ÷ 8 = ", 3, "Divide k by the new x.",
   "Check: 8 × 3 = ", 24, "x times y must give k = 24.",
   "Product is 24, so y = 3 is right."),
})

silver.append({
 "display": "8 identical tiles cover 2400 cm². What area would 14 tiles cover?",
 "solutions": [4200], "calculator": False, "input_type": "single_value",
 "hint": "Find the area of one tile, then multiply by fourteen.",
 "misconceptions": [{"pattern":"forgot_step","check":"common","expect":300,
   "message":"One tile = 2400 ÷ 8 = 300 cm². Fourteen = 14 × 300 = 4200 cm²."}],
 "guided_steps": direct_unit(
   "One tile: 2400 ÷ 8 = ", 300, "Share 2400 cm² between 8 tiles.",
   "Direct or inverse? More tiles cover more, so direct.",
   "So one tile covers 300 cm², the constant.",
   "Fourteen tiles: 14 × 300 = ", 4200, "Fourteen lots of 300 cm².",
   "Check: 4200 ÷ 14 = ", 300, "Divide back to the one-tile area.",
   "300 cm² each again, so 4200 cm² is right."),
})

silver.append({
 "display": "A journey takes 6 hours at 40 km/h. How long at 60 km/h? Give your answer in hours.",
 "solutions": [4], "calculator": False, "input_type": "single_value",
 "hint": "Inverse: multiply speed by time for the distance, then divide by the new speed.",
 "misconceptions": [{"pattern":"inverse_error","check":"common","expect":9,
   "message":"Speed and time are inverse: faster means sooner. Distance = 40 × 6 = 240 km. Time = 240 ÷ 60 = 4 hours. Answering 9 treats time as rising with speed."}],
 "guided_steps": inverse_k(
   "Speed and time are inverse: go faster, arrive sooner. Distance (speed × time) is the constant.",
   "Distance: 40 × 6 = ", 240, "Multiply speed by time.",
   "240 km, the fixed distance.",
   "At 60 km/h: 240 ÷ 60 = ", 4, "Divide the distance by the new speed.",
   "Check: 60 × 4 = ", 240, "Speed times time must give 240 km.",
   "240 km again, so 4 hours is right."),
})

silver.append({
 "display": "\\(y\\) is directly proportional to \\(x\\). When \\(x = 6\\), \\(y = 21\\). Find \\(x\\) when \\(y = 49\\).",
 "solutions": [14], "calculator": False, "input_type": "single_value",
 "hint": "Direct: divide y by x to find k, then divide the new y by k to get x.",
 "misconceptions": [{"pattern":"wrong_formula","check":"common","expect":171.5,
   "message":"k = 21 ÷ 6 = 3.5. To find x from y, divide: x = 49 ÷ 3.5 = 14. Multiplying 49 by 3.5 gives 171.5, which is far too big."}],
 "guided_steps": [
   say("Direct: \\(y = kx\\). Find k, then rearrange to get x."),
   box("k = y ÷ x = 21 ÷ 6 = ", 3.5, "Divide y by x."),
   say("So \\(y = 3.5x\\). To find x, divide y by k."),
   box("x = 49 ÷ 3.5 = ", 14, "Divide 49 by 3.5.", phase="substitute"),
   box("Check: 3.5 × 14 = ", 49, "k times x must give y = 49.", done="Gives 49, so x = 14 is right."),
 ],
})

silver.append({
 "display": "\\(y\\) is inversely proportional to \\(x\\). When \\(x = 6\\), \\(y = 8\\). Find \\(x\\) when \\(y = 4\\).",
 "solutions": [12], "calculator": False, "input_type": "single_value",
 "hint": "Inverse: multiply x by y to find k, then divide k by the new y to get x.",
 "misconceptions": [{"pattern":"inverse_error","check":"common","expect":3,
   "message":"Inverse means \\(k = xy\\), so k = 6 × 8 = 48 and x = 48 ÷ 4 = 12. Halving y should double x, not shrink it to 3."}],
 "guided_steps": inverse_k(
   "Inverse: \\(y = k/x\\), so \\(k = xy\\).",
   "k = 6 × 8 = ", 48, "Multiply x and y.",
   None,
   "x = 48 ÷ 4 = ", 12, "Divide k by the new y.",
   "Check: 12 × 4 = ", 48, "x times y must give k = 48.",
   "48 again, so x = 12 is right."),
})

silver.append({
 "display": "12 workers finish a job in 8 days. How many workers are needed to finish it in 6 days?",
 "solutions": [16], "calculator": False, "input_type": "single_value",
 "hint": "Inverse: multiply workers by days for the constant, then divide by the new number of days.",
 "misconceptions": [{"pattern":"inverse_error","check":"common","expect":9,
   "message":"Fewer days needs more workers, so it is inverse. Constant = 12 × 8 = 96. Workers = 96 ÷ 6 = 16. Answering 9 wrongly cuts workers as days fall."}],
 "guided_steps": inverse_k(
   "Fewer days needs more workers, so inverse. Workers × days is the constant.",
   "Constant: 12 × 8 = ", 96, "Multiply workers by days.",
   "96 worker-days, the fixed job size.",
   "For 6 days: 96 ÷ 6 = ", 16, "Divide the constant by 6 days.",
   "Check: 16 × 6 = ", 96, "Workers times days must give 96.",
   "96 worker-days again, so 16 workers is right."),
})

# ===== GOLD =====
gold = []

gold.append({
 "display": "\\(y\\) is directly proportional to \\(x\\). When \\(x = 5\\), \\(y = 8\\). Find \\(y\\) when \\(x = 12.5\\).",
 "solutions": [20], "calculator": False, "input_type": "single_value",
 "hint": "Direct: divide y by x to find k, then multiply the new x by k.",
 "misconceptions": [{"pattern":"wrong_formula","check":"common","expect":None,
   "message":"\\(y = kx\\), so k = 8 ÷ 5 = 1.6 and y = 1.6 × 12.5 = 20."}],
 "guided_steps": [
   say("Direct: \\(y = kx\\). Find k first."),
   box("k = y ÷ x = 8 ÷ 5 = ", 1.6, "Divide y by x."),
   box("y = 1.6 × 12.5 = ", 20, "Multiply the new x by k.", phase="substitute"),
   box("Check: 20 ÷ 12.5 = ", 1.6, "Must give k = 1.6 again.", done="Same k, so y = 20 is right."),
 ],
})

gold.append({
 "display": "A gear with 20 teeth meshes with a gear of 30 teeth. The small gear rotates at 150 rpm. Find the speed of the large gear.",
 "solutions": [100], "calculator": False, "input_type": "single_value",
 "hint": "Gears are inverse: multiply teeth by rpm for the constant, then divide by the large gear's teeth.",
 "misconceptions": [{"pattern":"inverse_error","check":"common","expect":225,
   "message":"Gears are inverse: more teeth, slower spin. Constant = 20 × 150 = 3000. Large gear = 3000 ÷ 30 = 100 rpm. Answering 225 treats it as direct."}],
 "guided_steps": inverse_k(
   "Gears are inverse: more teeth, slower spin. Teeth × rpm is the constant.",
   "Constant for the small gear: 20 × 150 = ", 3000, "Multiply teeth by rpm.",
   "3000 stays fixed for the meshed pair.",
   "Large gear: 3000 ÷ 30 = ", 100, "Divide the constant by the large gear's teeth.",
   "Check: 30 × 100 = ", 3000, "Teeth times rpm must give 3000.",
   "Back to 3000, so 100 rpm is right."),
})

gold.append({
 "display": "It takes 12 workers 15 days to dig a trench. After 5 days, 4 workers leave. How many more days to finish?",
 "solutions": [15], "calculator": False, "input_type": "single_value",
 "hint": "Find total worker-days, subtract the work already done, then divide the rest by the workers left.",
 "misconceptions": [{"pattern":"wrong_formula","check":"common","expect":22.5,
   "message":"Total = 12 × 15 = 180 worker-days. Done in 5 days = 60, so 120 remain. With 8 workers, 120 ÷ 8 = 15 more days. Dividing 180 by 8 forgets the work already done."}],
 "guided_steps": [
   say("First the total work: workers × days."),
   box("Total: 12 × 15 = ", 180, "Multiply workers by days."),
   box("Work done in the first 5 days: 12 × 5 = ", 60, "12 workers for 5 days."),
   box("Work left: 180 − 60 = ", 120, "Subtract the work done from the total."),
   say("Now 4 leave, so 8 workers remain."),
   box("Days left: 120 ÷ 8 = ", 15, "Divide the remaining work by 8 workers.", phase="substitute"),
   box("Check: 60 + 8 × 15 = ", 180, "Work done plus work still to do must total 180.",
       done="60 + 120 = 180, the whole job, so 15 more days is right."),
 ],
})

gold.append({
 "display": "\\(y\\) is inversely proportional to \\(x\\). When \\(x = 2\\), \\(y = 18\\). Find \\(y\\) when \\(x = 12\\).",
 "solutions": [3], "calculator": False, "input_type": "single_value",
 "hint": "Inverse: multiply x by y to find k, then divide k by the new x.",
 "misconceptions": [{"pattern":"inverse_error","check":"common","expect":108,
   "message":"Inverse means \\(k = xy\\), so k = 2 × 18 = 36 and y = 36 ÷ 12 = 3. Multiplying x by 6 should divide y by 6, not multiply it to 108."}],
 "guided_steps": inverse_k(
   "Inverse: \\(y = k/x\\), so \\(k = xy\\).",
   "k = 2 × 18 = ", 36, "Multiply x and y.",
   None,
   "y = 36 ÷ 12 = ", 3, "Divide k by the new x.",
   "Check: 12 × 3 = ", 36, "x times y must give k = 36.",
   "36 again, so y = 3 is right."),
})

gold.append({
 "display": "\\(y\\) is directly proportional to \\(x\\). When \\(x = 6\\), \\(y = 9\\). Find \\(x\\) when \\(y = 15\\).",
 "solutions": [10], "calculator": False, "input_type": "single_value",
 "hint": "Direct: divide y by x to find k, then divide the new y by k to get x.",
 "misconceptions": [{"pattern":"wrong_formula","check":"common","expect":22.5,
   "message":"k = 9 ÷ 6 = 1.5. To find x from y, divide: x = 15 ÷ 1.5 = 10. Multiplying 15 by 1.5 gives 22.5, which is too big."}],
 "guided_steps": [
   say("Direct: \\(y = kx\\). Find k, then divide to get x."),
   box("k = y ÷ x = 9 ÷ 6 = ", 1.5, "Divide y by x."),
   say("So \\(y = 1.5x\\). To find x, divide y by k."),
   box("x = 15 ÷ 1.5 = ", 10, "Divide 15 by k.", phase="substitute"),
   box("Check: 1.5 × 10 = ", 15, "k times x must give y = 15.", done="Gives 15, so x = 10 is right."),
 ],
})

# ===== tier_guides =====
tier_guides = {
 "bronze": {
   "title": "Bronze: Unitary method for word problems",
   "steps": [
     "Decide the type. If both amounts rise together it is <strong>direct</strong>; if one rises as the other falls it is <strong>inverse</strong>.",
     "Direct: find the value of <strong>one</strong> by dividing, then multiply up to the amount you need.",
     "Inverse: multiply the two linked amounts to get the constant, then divide the constant by the new amount.",
     "Always check by working backwards to the starting numbers."
   ],
   "example": {
     "question": "6 workers build a wall in 10 days. How long would 4 workers take?",
     "steps": [
       {"label":"Type","content":"<p>Fewer workers, more days: inverse proportion.</p>"},
       {"label":"Constant","content":"<p>\\(6 \\times 10 = 60\\) worker-days.</p>"},
       {"label":"Solve","content":"<p>\\(60 \\div 4 = 15\\) days.</p>"},
       {"label":"Check","content":"<p>\\(4 \\times 15 = 60\\), back to the constant.</p>"},
       {"label":"Answer","content":"<p>15 days.</p>","isAnswer":True,"is_answer":True}
     ]
   }
 },
 "silver": {
   "title": "Silver: Using y = kx and y = k/x",
   "steps": [
     "Write the rule: <strong>direct</strong> is \\(y = kx\\), <strong>inverse</strong> is \\(y = \\frac{k}{x}\\).",
     "Find the constant k from the given pair: direct \\(k = y \\div x\\), inverse \\(k = x \\times y\\).",
     "Substitute into the rule to find the missing value, rearranging if you are given y and need x.",
     "Check the constant is the same for your answer."
   ],
   "example": {
     "question": "y is inversely proportional to x. When x = 5, y = 8. Find y when x = 10.",
     "steps": [
       {"label":"Rule","content":"<p>Inverse, so \\(k = xy\\).</p>"},
       {"label":"Constant","content":"<p>\\(k = 5 \\times 8 = 40\\).</p>"},
       {"label":"Solve","content":"<p>\\(y = 40 \\div 10 = 4\\).</p>"},
       {"label":"Check","content":"<p>\\(10 \\times 4 = 40\\), the constant.</p>"},
       {"label":"Answer","content":"<p>\\(y = 4\\).</p>","isAnswer":True,"is_answer":True}
     ]
   }
 },
 "gold": {
   "title": "Gold: Reverse and multi-step proportion",
   "steps": [
     "Spot hidden proportion: gears, worker-days and speed are all <strong>inverse</strong>, so their product is constant.",
     "Find the constant, then work backwards if you are given the second quantity and need the first.",
     "For multi-step problems, track the total work, subtract what is done, then share the rest.",
     "Check every answer returns the original constant or total."
   ],
   "example": {
     "question": "A gear with 15 teeth turns at 200 rpm, meshed with a 25-tooth gear. Find the large gear's speed.",
     "steps": [
       {"label":"Type","content":"<p>Gears are inverse: teeth × rpm is constant.</p>"},
       {"label":"Constant","content":"<p>\\(15 \\times 200 = 3000\\).</p>"},
       {"label":"Solve","content":"<p>\\(3000 \\div 25 = 120\\) rpm.</p>"},
       {"label":"Check","content":"<p>\\(25 \\times 120 = 3000\\), the constant.</p>"},
       {"label":"Answer","content":"<p>120 rpm.</p>","isAnswer":True,"is_answer":True}
     ]
   }
 }
}

# ===== guided (opener + teach) =====
guided = {
 "opener": {
   "display": "A shopping puzzle: no formulas needed.",
   "steps": [
     say("A shopping puzzle. No formulas, just common sense."),
     box("3 identical chocolate bars cost £6, so 1 bar costs £", 2, "Share the £6 equally between the 3 bars."),
     say("Finding the cost of ONE first is the whole trick. It has a name: the <strong>unitary method</strong>."),
     box("So 5 bars cost £", 10, "Five lots of the one-bar price."),
     say("You just did <strong>direct proportion</strong>. Double the bars, double the cost: they climb together in step. Algebra writes it as \\(y = kx\\), where k is the cost of one bar (here k = 2), called the constant of proportionality. When two quantities move in <strong>opposite</strong> directions, that is <strong>inverse</strong> proportion, coming up next.")
   ]
 },
 "teach": {
   "bronze": {
     "display": "4 builders take 6 days to build a wall. How long would 3 builders take?",
     "steps": [
       say("Direct or inverse? Fewer builders means MORE days: one falls as the other rises. That is inverse proportion. For inverse, the two amounts multiply to a fixed constant."),
       box("For the first crew, builders × days = 4 × 6 = ", 24, "Multiply the two numbers."),
       say("Call that 24 the work: 24 builder-days. It never changes, whatever the crew size."),
       box("So the new crew must also give builders × days = ", 24, "The constant does not change: still 24.", done="Same constant. That invariance IS inverse proportion."),
       box("With 3 builders: days = 24 ÷ 3 = ", 8, "Divide the constant by 3 builders."),
       say("8 days, longer than 6, exactly as predicted."),
       box("Check: 3 × 8 = ", 24, "Multiply back; it must return to 24.", done="Back to 24 builder-days, so 8 days is right.")
     ]
   },
   "silver": {
     "display": "\\(y\\) is directly proportional to \\(x\\). When \\(x = 3\\), \\(y = 12\\). Find \\(y\\) when \\(x = 7\\).",
     "steps": [
       say("Now in algebra. Direct proportion means \\(y = kx\\): y is a fixed multiple k of x. Always find k first."),
       box("k = y ÷ x = 12 ÷ 3 = ", 4, "Divide y by x."),
       say("So the rule is \\(y = 4x\\)."),
       box("Check k on the given point: 4 × 3 = ", 12, "k times the first x must give the first y, 12.", done="Gives 12, so k = 4 is correct."),
       box("Now the new value: y = 4 × 7 = ", 28, "Multiply the new x by k."),
       box("Check: 28 ÷ 7 = ", 4, "Must give k = 4 again.", done="Same k, so y = 28 is right.")
     ]
   },
   "gold": {
     "display": "\\(y\\) is inversely proportional to \\(x\\). When \\(x = 4\\), \\(y = 9\\). Find \\(x\\) when \\(y = 6\\).",
     "steps": [
       say("Gold. Inverse means \\(y = \\frac{k}{x}\\), so the product \\(xy = k\\). Here we also work backwards, finding x from y."),
       box("Find k = x × y = 4 × 9 = ", 36, "Multiply x and y."),
       say("So \\(xy\\) is always 36."),
       box("We need x when y = 6, and \\(xy = 36\\), so x × 6 = ", 36, "The product is still 36.", done="Same product 36. That is the inverse rule."),
       box("So x = 36 ÷ 6 = ", 6, "Divide 36 by 6."),
       box("Check: 6 × 6 = ", 36, "x times y must give 36.", done="36 again, so x = 6 is right.")
     ]
   }
 }
}

# ===== method_card (slim) =====
method_card = {
 "title": "Direct & Inverse Proportion",
 "steps": [
   "Decide direct (both rise together) or inverse (one rises as the other falls).",
   "Find the constant k: direct k = y ÷ x, inverse k = x × y.",
   "Use k to find the missing value, then check it returns the same k.",
   "In words: find the value of one, then scale."
 ],
 "content": "<p><strong>Direct proportion:</strong> as one quantity rises, the other rises in step. If \\(y\\) is directly proportional to \\(x\\), then \\(y = kx\\), where \\(k\\) is the constant of proportionality.</p><p><strong>Inverse proportion:</strong> as one quantity rises, the other falls. If \\(y\\) is inversely proportional to \\(x\\), then \\(y = \\frac{k}{x}\\), so the product \\(xy = k\\) is constant.</p><p>The <strong>unitary method</strong> works for both: for direct, find the value of one unit then scale; for inverse, multiply the linked quantities to find \\(k\\), then divide by the new value.</p>",
 "example": "<p><strong>5 identical books weigh 1.2 kg. What do 8 books weigh?</strong></p><p>Direct proportion. One book = \\(\\frac{1.2}{5} = 0.24\\) kg. So 8 books = \\(8 \\times 0.24 = 1.92\\) kg.</p>"
}

# ===== assemble, preserving related_videos / topic_links / worked_examples =====
base = json.load(io.open("_live_ratio_L04.json", encoding="utf-8"))

we = base["worked_examples"]
for ex in we:
    for st in ex["steps"]:
        st["label"] = st["label"].replace(" — ", ": ").replace(" - ", ": ")

pd = {
 "method_card": method_card,
 "topic_links": base["topic_links"],
 "problem_bank": {
   "bronze": bronze, "silver": silver, "gold": gold,
   "bronze_description": "Direct and inverse word problems solved by the unitary method: find the value of one, then scale.",
   "silver_description": "Using y = kx (direct) or y = k/x (inverse): find the constant k, then the missing value, including working backwards.",
   "gold_description": "Multi-step proportion: harder contexts (gears, worker-days), reverse questions and non-integer constants."
 },
 "tier_guides": tier_guides,
 "guided": guided,
 "related_videos": base["related_videos"],
 "worked_examples": we
}

io.open("lesson_ratio-proportion-L04.json","w",encoding="utf-8").write(
    json.dumps(pd, ensure_ascii=False, indent=1))
print("written lesson_ratio-proportion-L04.json")
print("bronze", len(bronze), "silver", len(silver), "gold", len(gold))
