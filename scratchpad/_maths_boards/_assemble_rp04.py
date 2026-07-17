# -*- coding: utf-8 -*-
import json

live = json.load(open("_live_rp04.json", encoding="utf-8"))
parts = json.load(open("_rp04_parts.json", encoding="utf-8"))
pb = live["problem_bank"]

def M(pattern, expect, message):
    return {"pattern": pattern, "check": pattern, "expect": expect, "message": message}

def box(pre, answer, hint, say=None, post="", phase=None, done=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if phase is not None: d["phase"] = phase
    if done is not None: d["done"] = done
    return d

# ============ ENRICHMENT (live order) ============
# GOLD (5)
gold = [
  dict(  # gold[0] change 6->9, +15, find y at x=4 -> 20
    hint="The change in y over the change in x gives k, then use k with x = 4.",
    misconceptions=[M("wrong_change_base", 10,
      "10 divides the increase 15 by the starting x-value 6. The 15 is the increase across the change in x, which is 9 − 6 = 3, so k = 15 ÷ 3 = 5 and y = 5 × 4 = 20.")],
    guided_steps=[
      box("9 − 6 = ", 3, "Subtract the x-values.", say="y rises by 15 as x goes from 6 to 9. First find the change in x."),
      box("15 ÷ 3 = ", 5, "Divide 15 by 3.", say="k is the change in y over the change in x."),
      box("5 × 4 = ", 20, "Multiply k by 4.", say="Now use y = kx with x = 4.", phase="substitute", done="y = 20 when x = 4."),
      box("45 − 30 = ", 15, "Subtract 30 from 45.", say="Check against the original. With k = 5, y is 30 at x = 6 and 45 at x = 9.", done="The increase is 15, so k = 5 is correct."),
    ]),
  dict(  # gold[1] 8 workers 15 days, after 5 days 3 leave -> 16
    hint="Work in worker-days: find the total, take off what is done, then share among the workers left.",
    misconceptions=[
      M("keeps_all_workers", 10, "10 shares the remaining 80 worker-days among the original 8 workers, but 3 have left. There are 8 − 3 = 5 workers now, so 80 ÷ 5 = 16 days."),
      M("forgets_work_done", 24, "24 shares all 120 worker-days among 5 workers, but 5 days of work are already finished. Work left = 120 − 40 = 80, so 80 ÷ 5 = 16 days."),
    ],
    guided_steps=[
      box("8 × 15 = ", 120, "Multiply 8 by 15.", say="Total work in worker-days is workers × days."),
      box("8 × 5 = ", 40, "Multiply 8 by 5.", say="Work done in the first 5 days, still with 8 workers."),
      box("120 − 40 = ", 80, "Subtract 40 from 120.", say="Work still to do."),
      box("80 ÷ 5 = ", 16, "Divide 80 by 5.", say="Now only 8 − 3 = 5 workers remain. Days left = work ÷ workers.", phase="substitute", done="16 more days are needed."),
      box("5 × 16 = ", 80, "Multiply 5 by 16.", say="Check: 5 workers for 16 days is how much work?", done="80 worker-days finishes the remaining job, correct."),
    ]),
  dict(  # gold[2] inv, x=2 y=18; y=4 find a -> 9
    hint="Find k by multiplying x and y, then divide k by the new y to get a.",
    misconceptions=[M("multiplies_not_divides", 144,
      "144 multiplies k by y, but for inverse proportion a = k ÷ y. With k = 2 × 18 = 36, a = 36 ÷ 4 = 9.")],
    guided_steps=[
      box("2 × 18 = ", 36, "Multiply 2 by 18.", say="Inverse proportion: k = x × y. Find k from the first pair."),
      box("36 ÷ 4 = ", 9, "Divide 36 by 4.", say="When y = 4, the x value is a, and a = k ÷ y.", phase="substitute", done="a = 9."),
      box("9 × 4 = ", 36, "Multiply 9 by 4.", say="Check: does a × y equal k?", done="9 × 4 = 36 = k, correct."),
    ]),
  dict(  # gold[3] taxi 180/6 -> 180/8, save -> 7.5
    hint="Find the cost each way (6 people, then 8 people), then subtract.",
    misconceptions=[M("gives_new_cost", 22.5,
      "22.50 is the new cost per person, not the saving. Before: 180 ÷ 6 = £30 each. After: 180 ÷ 8 = £22.50 each. Saving = 30 − 22.50 = £7.50.")],
    guided_steps=[
      box("180 ÷ 6 = ", 30, "Divide £180 by 6.", say="Find the cost per person with 6 people."),
      box("180 ÷ 8 = ", 22.5, "Divide £180 by 8.", say="Two more join, making 8. Find the new cost per person."),
      box("30 − 22.5 = ", 7.5, "Subtract £22.50 from £30.", say="The saving is the difference.", phase="substitute", done="Each person saves £7.50."),
      box("8 × 22.5 = ", 180, "Multiply 8 by 22.5.", say="Check: 8 people each paying £22.50 covers the fare.", done="8 × £22.50 = £180, correct."),
    ]),
  dict(  # gold[4] y prop x^2, x=3 y=36, find y at x=5 -> 100
    hint="y = kx². Find k using x² = 9, then use x² = 25.",
    misconceptions=[
      M("forgets_square", 60, "60 uses y = kx, but here y is proportional to x². k = 36 ÷ 3² = 36 ÷ 9 = 4, so y = 4 × 5² = 4 × 25 = 100."),
      M("forgets_new_square", 20, "20 forgets to square the new x. k = 4 and y = k × 5² = 4 × 25 = 100, not 4 × 5."),
    ],
    guided_steps=[
      box("3 × 3 = ", 9, "Work out 3 squared.", say="y = kx². First square the given x."),
      box("36 ÷ 9 = ", 4, "Divide 36 by 9.", say="Find k by dividing y by x²."),
      box("5 × 5 = ", 25, "Work out 5 squared.", say="Now square the new x = 5.", phase="substitute"),
      box("4 × 25 = ", 100, "Multiply 4 by 25.", say="Then y = k × 25.", done="y = 100 when x = 5."),
      box("100 ÷ 25 = ", 4, "Divide 100 by 25.", say="Check: divide y by x² to recover k.", done="100 ÷ 25 = 4 = k, correct."),
    ]),
]

# BRONZE (8)
bronze = [
  dict(  # b0 direct x=5 y=15 find y at x=8 -> 24
    hint="Find k by dividing y by x, then multiply k by the new x.",
    misconceptions=[M("additive", 18,
      "18 adds 3 to y because x rose by 3, but proportion scales by multiplying. k = 15 ÷ 5 = 3, so y = 3 × 8 = 24.")],
    guided_steps=[
      box("15 ÷ 5 = ", 3, "Divide 15 by 5.", say="Direct proportion means y = kx. Find k by dividing y by x."),
      box("3 × 8 = ", 24, "Multiply k by 8.", say="Now use k = 3 with the new x = 8.", phase="substitute", done="y = 24 when x = 8."),
      box("24 ÷ 8 = ", 3, "Divide 24 by 8.", say="Check: does the new pair give the same k?", done="24 ÷ 8 = 3 = k, correct."),
    ]),
  dict(  # b1 4 pens £6, 10 pens -> 15
    hint="Find the cost of one pen, then multiply by 10.",
    misconceptions=[M("doubles_only", 12,
      "12 is the cost of 8 pens (double 4). You need 10 pens. One pen costs 6 ÷ 4 = £1.50, so 10 pens cost 10 × 1.50 = £15.")],
    guided_steps=[
      box("6 ÷ 4 = ", 1.5, "Divide £6 by 4 pens.", say="Find the cost of one pen."),
      box("1.5 × 10 = ", 15, "Multiply the price of one pen by 10.", say="Now multiply by 10 pens.", phase="substitute", done="10 pens cost £15."),
      box("15 ÷ 10 = ", 1.5, "Divide £15 by 10.", say="Check by working back to one pen.", done="£1.50 per pen matches, correct."),
    ]),
  dict(  # b2 direct x=3 y=12 find k -> 4
    hint="For direct proportion, k = y ÷ x.",
    misconceptions=[M("inverts", 0.25,
      "0.25 divides x by y. For direct proportion k = y ÷ x = 12 ÷ 3 = 4.")],
    guided_steps=[
      box("12 ÷ 3 = ", 4, "Divide 12 by 3.", say="Direct proportion means y = kx, so k = y ÷ x."),
      box("4 × 3 = ", 12, "Multiply 4 by 3.", say="Check k rebuilds the pair.", phase="substitute"),
      box("4 × 5 = ", 20, "Multiply k by 5.", say="k works for any x. If x were 5, y would be:", done="k = 4 rebuilds y and works for every x, so k = 4."),
    ]),
  dict(  # b3 5 workers 12 days, 1 worker inverse -> 60
    hint="Fewer workers means more days. Multiply workers by days to get the constant.",
    misconceptions=[M("uses_direct", 2.4,
      "2.4 divides the days by workers, treating it as direct. With fewer workers the job takes longer. Total work = 5 × 12 = 60 worker-days, so 1 worker takes 60 days.")],
    guided_steps=[
      box("5 × 12 = ", 60, "Multiply workers by days.", say="Inverse proportion: workers × days stays constant. Find that constant."),
      box("60 ÷ 1 = ", 60, "Divide 60 by 1 worker.", say="For 1 worker, days = constant ÷ workers.", phase="substitute", done="1 worker takes 60 days."),
      box("1 × 60 = ", 60, "Multiply 1 by 60.", say="Check: 1 worker for 60 days is how many worker-days?", done="60 worker-days matches, correct."),
    ]),
  dict(  # b4 inv x=2 y=10 find k -> 20
    hint="For inverse proportion, k = y × x.",
    misconceptions=[M("uses_direct", 5,
      "5 divides y by x, which is the direct rule. For inverse proportion k = y × x = 10 × 2 = 20.")],
    guided_steps=[
      box("10 × 2 = ", 20, "Multiply y by x.", say="Inverse proportion means y = k ÷ x, so k = y × x. Multiply the pair."),
      box("20 ÷ 2 = ", 10, "Divide 20 by 2.", say="Check k rebuilds y.", phase="substitute"),
      box("20 ÷ 4 = ", 5, "Divide k by 4.", say="And for x = 4, y would be:", done="k = 20 rebuilds y, so k = 20."),
    ]),
  dict(  # b5 3 items 750g, 5 items -> 1250
    hint="Find the weight of one item, then multiply by 5.",
    misconceptions=[M("wrong_divisor", 750,
      "750 g divides by 5 instead of 3. There are 3 items weighing 750 g, so one weighs 750 ÷ 3 = 250 g, and 5 weigh 5 × 250 = 1250 g.")],
    guided_steps=[
      box("750 ÷ 3 = ", 250, "Divide 750 g by 3 items.", say="Find the weight of one item."),
      box("250 × 5 = ", 1250, "Multiply one item by 5.", say="Now find 5 items.", phase="substitute", done="5 items weigh 1250 g."),
      box("1250 ÷ 5 = ", 250, "Divide 1250 by 5.", say="Check by working back to one item.", done="250 g each matches, correct."),
    ]),
  dict(  # b6 recipe 4 people 200g, 6 people -> 300
    hint="Find the flour for one person, then multiply by 6.",
    misconceptions=[M("stops_at_unit", 50,
      "50 g is the flour for one person. The recipe is for 6 people, so multiply: 6 × 50 = 300 g.")],
    guided_steps=[
      box("200 ÷ 4 = ", 50, "Divide 200 g by 4 people.", say="Find the flour for one person."),
      box("50 × 6 = ", 300, "Multiply one person by 6.", say="Now find 6 people.", phase="substitute", done="6 people need 300 g."),
      box("300 ÷ 6 = ", 50, "Divide 300 by 6.", say="Check by working back to one person.", done="50 g each matches, correct."),
    ]),
  dict(  # b7 y=kx k=7 x=9 -> 63
    hint="Substitute k = 7 and x = 9 into y = kx.",
    misconceptions=[M("adds", 16,
      "16 adds k and x. The rule y = kx multiplies them: 7 × 9 = 63.")],
    guided_steps=[
      box("7 × 9 = ", 63, "Multiply 7 by 9.", say="Substitute k = 7 and x = 9 into y = kx."),
      box("63 ÷ 9 = ", 7, "Divide 63 by 9.", say="Check: divide y by x to recover k.", phase="substitute"),
      box("7 × 2 = ", 14, "Multiply k by 2.", say="And k works for any x. If x = 2, y would be:", done="y = kx with k = 7 gives 63 when x = 9, correct."),
    ]),
]

# SILVER (7)
silver = [
  dict(  # s0 direct x=6 y=21 find x at y=35 -> 10
    hint="Find k by dividing y by x, then divide the new y by k to get x.",
    misconceptions=[M("additive", 20,
      "20 adds 14 to x because y rose by 14. Proportion scales by multiplying, not adding. k = 21 ÷ 6 = 3.5, and x = 35 ÷ 3.5 = 10.")],
    guided_steps=[
      box("21 ÷ 6 = ", 3.5, "Divide 21 by 6.", say="Find k for the direct proportion."),
      box("35 ÷ 3.5 = ", 10, "Divide 35 by 3.5.", say="Now x = y ÷ k with the new y = 35.", phase="substitute", done="x = 10 when y = 35."),
      box("3.5 × 10 = ", 35, "Multiply k by 10.", say="Check: does x = 10 give y = 35?", done="3.5 × 10 = 35, correct."),
    ]),
  dict(  # s1 inv x=4 y=15 find y at x=12 -> 5
    hint="Find k by multiplying x and y, then divide k by the new x.",
    misconceptions=[M("uses_direct", 45,
      "45 triples y because x tripled, but this is inverse. When x triples, y is divided by 3. k = 4 × 15 = 60, and y = 60 ÷ 12 = 5.")],
    guided_steps=[
      box("4 × 15 = ", 60, "Multiply 4 by 15.", say="Inverse proportion: k = x × y. Find k."),
      box("60 ÷ 12 = ", 5, "Divide 60 by 12.", say="Now y = k ÷ x with the new x = 12.", phase="substitute", done="y = 5 when x = 12."),
      box("12 × 5 = ", 60, "Multiply 12 by 5.", say="Check: does x × y still equal 60?", done="12 × 5 = 60 = k, correct."),
    ]),
  dict(  # s2 6 machines 8 hours, 4 machines -> 12
    hint="Fewer machines means more time. Multiply machines by hours for the constant.",
    misconceptions=[M("gives_constant", 48,
      "48 is the total machine-hours (6 × 8), not the time. Share it among 4 machines: 48 ÷ 4 = 12 hours.")],
    guided_steps=[
      box("6 × 8 = ", 48, "Multiply machines by hours.", say="Inverse proportion: machines × hours is constant. Find it."),
      box("48 ÷ 4 = ", 12, "Divide 48 by 4.", say="For 4 machines, hours = constant ÷ machines.", phase="substitute", done="4 machines take 12 hours."),
      box("4 × 12 = ", 48, "Multiply 4 by 12.", say="Check: 4 machines for 12 hours is how many machine-hours?", done="48 machine-hours matches, correct."),
    ]),
  dict(  # s3 36L 540km, 20L -> 300
    hint="Find the distance per litre, then multiply by 20.",
    misconceptions=[M("stops_at_unit", 15,
      "15 km is the distance on one litre. On 20 litres the car goes 20 × 15 = 300 km.")],
    guided_steps=[
      box("540 ÷ 36 = ", 15, "Divide 540 km by 36 litres.", say="Find the distance the car travels on one litre."),
      box("15 × 20 = ", 300, "Multiply 15 by 20.", say="Now multiply by 20 litres.", phase="substitute", done="20 litres gives 300 km."),
      box("300 ÷ 20 = ", 15, "Divide 300 by 20.", say="Check the distance per litre from your answer.", done="15 km per litre matches, correct."),
    ]),
  dict(  # s4 inv x=5 y=24 find x at y=40 -> 3
    hint="Find k by multiplying x and y, then divide k by the new y to get x.",
    misconceptions=[M("gives_constant", 120,
      "120 is the constant x × y, not x. To find x when y = 40, divide: x = 120 ÷ 40 = 3.")],
    guided_steps=[
      box("5 × 24 = ", 120, "Multiply 5 by 24.", say="Inverse proportion: k = x × y. Find k from the first pair."),
      box("120 ÷ 40 = ", 3, "Divide 120 by 40.", say="Now x = k ÷ y with the new y = 40.", phase="substitute", done="x = 3 when y = 40."),
      box("3 × 40 = ", 120, "Multiply 3 by 40.", say="Check: does x × y equal 120?", done="3 × 40 = 120 = k, correct."),
    ]),
  dict(  # s5 MC graph through (4,12) -> y=3x (index 0). chart added, guided walk numeric.
    hint="Direct proportion is y = kx through the origin. Find k = y ÷ x from the point.",
    misconceptions=[
      M("x_as_gradient", 1, "y = 4x uses the x-coordinate as the gradient. The gradient is k = y ÷ x = 12 ÷ 4 = 3, so y = 3x."),
      M("y_as_gradient", 2, "y = 12x uses the y-coordinate as the gradient. The gradient is k = y ÷ x = 12 ÷ 4 = 3, so y = 3x."),
    ],
    guided_steps=[
      box("12 ÷ 4 = ", 3, "Divide the y-coordinate by the x-coordinate.", say="Direct proportion always passes through the origin with the form y = kx. Find k from the point (4, 12)."),
      box("3 × 4 = ", 12, "Multiply 3 by 4.", say="So the equation is y = 3x. Check it passes through (4, 12): put x = 4.", phase="substitute", done="3 × 4 = 12, so the point lies on y = 3x."),
      box("3 × 0 = ", 0, "Multiply 3 by 0.", say="Check the origin: put x = 0.", done="The line goes through (0, 0), so y = 3x is the answer."),
    ],
    chart={
      "type": "scatter",
      "data": {"datasets": [
        {"type": "line", "label": "y = 3x", "data": [{"x": 0, "y": 0}, {"x": 5, "y": 15}],
         "borderColor": "#3b82f6", "borderWidth": 2, "fill": False, "tension": 0, "pointRadius": 0},
        {"type": "scatter", "label": "point", "data": [{"x": 4, "y": 12}],
         "pointRadius": 6, "pointBackgroundColor": "#f59e0b", "pointBorderColor": "#f59e0b"},
      ]},
      "options": {"plugins": {"legend": {"display": False}}, "scales": {
        "x": {"min": 0, "max": 6, "ticks": {"stepSize": 1}, "grid": {"color": "rgba(0,0,0,0.05)"}, "title": {"display": True, "text": "x"}},
        "y": {"min": 0, "max": 16, "ticks": {"stepSize": 2}, "grid": {"color": "rgba(0,0,0,0.05)"}, "title": {"display": True, "text": "y"}},
      }},
    }),
  dict(  # s6 recipe 8 servings 500ml, 12 servings -> 750
    hint="Find the milk for one serving, then multiply by 12.",
    misconceptions=[M("stops_at_unit", 62.5,
      "62.5 ml is the milk for one serving. For 12 servings multiply: 12 × 62.5 = 750 ml.")],
    guided_steps=[
      box("500 ÷ 8 = ", 62.5, "Divide 500 ml by 8 servings.", say="Find the milk for one serving."),
      box("62.5 × 12 = ", 750, "Multiply 62.5 by 12.", say="Now multiply by 12 servings.", phase="substitute", done="12 servings need 750 ml."),
      box("750 ÷ 12 = ", 62.5, "Divide 750 by 12.", say="Check by working back to one serving.", done="62.5 ml per serving matches, correct."),
    ]),
]

def apply(tier_list, enrich):
    for prob, e in zip(tier_list, enrich):
        prob["hint"] = e["hint"]
        prob["misconceptions"] = e["misconceptions"]
        if "guided_steps" in e:
            prob["guided_steps"] = e["guided_steps"]
        if "chart" in e:
            prob["chart"] = e["chart"]

apply(pb["gold"], gold)
apply(pb["bronze"], bronze)
apply(pb["silver"], silver)

pb["bronze_description"] = "One step: find k, or find the value of one unit and scale up (direct or inverse)."
pb["silver_description"] = "Two steps: find k from a pair, then find a missing x or y, including inverse and graphs."
pb["gold_description"]   = "Multi-step proportion: changes, worker-days, reverse inverse problems, and proportion to a square."

out = {
    "method_card": parts["method_card"],
    "tier_guides": parts["tier_guides"],
    "guided": parts["guided"],
    "topic_links": live["topic_links"],
    "problem_bank": pb,
    "related_videos": live["related_videos"],
    "worked_examples": live["worked_examples"],
}
json.dump(out, open("lesson_maths-aqa_ratio-proportion-L04.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("assembled ->", sum(len(pb[t]) for t in ("bronze", "silver", "gold")), "problems")
