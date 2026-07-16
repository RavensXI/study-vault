# -*- coding: utf-8 -*-
import json, io

MINUS = "−"  # −

def box(pre, answer, hint, post="", phase=None, done=None, say=None):
    d = {"pre": pre, "answer": answer, "hint": hint}
    if post:
        d["post"] = post
    if phase:
        d["phase"] = phase
    if done:
        d["done"] = done
    if say is not None:
        d["say"] = say
    return d

def say(text):
    return {"say": text}

def mc(pattern, message, expect):
    return {"pattern": pattern, "check": "common", "message": message, "expect": expect}

# ---------------- BRONZE ----------------
bronze = [
  {"display": "Angles on a straight line are \\(x°\\) and \\(72°\\). Find \\(x\\).",
   "solutions": [108], "input_type": "single_value", "calculator": False,
   "hint": "Angles on a straight line add to 180, so subtract 72 from 180.",
   "misconceptions": [mc("wrong_total",
     "It looks like you used 360° for a straight line. A straight line is a half turn, 180°, so x = 180 " + MINUS + " 72 = 108°.", 288)],
   "guided_steps": [
     say("The two angles sit on a straight line, which is a half turn."),
     box("Angles on a straight line add up to ", 180, "A straight line is a half turn.", post="°."),
     box("So x = 180 " + MINUS + " 72 = ", 108, "Subtract 72 from 180.", post="°.", phase="substitute"),
     box("Check they make a straight line: 108 + 72 = ", 180, "Add your answer to 72.", post="°.", phase="substitute",
         done="That is a straight line, so x = 108° is right."),
   ]},
  {"display": "Vertically opposite angles: one is \\(68°\\). What is the other?",
   "solutions": [68], "input_type": "single_value", "calculator": False,
   "hint": "Vertically opposite angles are equal, so the other is the same size.",
   "misconceptions": [mc("supplementary_not_equal",
     "You may have treated these as angles on a straight line. Vertically opposite angles are equal, not supplementary, so the other is 68°.", 112)],
   "guided_steps": [
     say("Two straight lines cross, making an X shape. The 68° angle and the one directly opposite are vertically opposite."),
     box("Track it through the straight line first. The angle beside 68° is 180 " + MINUS + " 68 = ", 112, "Angles on a straight line add to 180.", post="°."),
     box("The angle opposite 68° sits beside that 112° angle, also on a straight line: 180 " + MINUS + " 112 = ", 68, "Subtract 112 from 180.", post="°.", phase="substitute",
         done="That is why vertically opposite angles are always equal."),
     box("Check all four fill the point: 68 + 112 + 68 + 112 = ", 360, "Angles at a point add to 360.", post="°.", phase="substitute",
         done="They fill the full turn, so the other angle is 68°."),
   ]},
  {"display": "Triangle angles are \\(40°\\), \\(75°\\) and \\(x°\\). Find \\(x\\).",
   "solutions": [65], "input_type": "single_value", "calculator": False,
   "hint": "The three angles of a triangle add to 180.",
   "misconceptions": [mc("wrong_total",
     "It looks like you used 360° for the triangle. A triangle's angles add to 180°, so x = 180 " + MINUS + " 40 " + MINUS + " 75 = 65°.", 245)],
   "guided_steps": [
     say("All three angles of a triangle add to 180°."),
     box("Add the two you know: 40 + 75 = ", 115, "Just add them."),
     box("Take that from 180: x = 180 " + MINUS + " 115 = ", 65, "Subtract 115 from 180.", post="°.", phase="substitute"),
     box("Check the three add to 180: 40 + 75 + 65 = ", 180, "Add all three.", post="°.", phase="substitute",
         done="That is a full triangle, so x = 65° is right."),
   ]},
  {"display": "Three angles at a point are \\(90°\\), \\(145°\\) and \\(x°\\). Find \\(x\\).",
   "solutions": [125], "input_type": "single_value", "calculator": False,
   "hint": "Angles around a point add to 360.",
   "misconceptions": [mc("added_givens",
     "It looks like you added the two known angles. They meet at a point (360°), so subtract: x = 360 " + MINUS + " 90 " + MINUS + " 145 = 125°.", 235)],
   "guided_steps": [
     say("These three angles meet at a single point and go all the way round, a full turn of 360°."),
     box("Add the two you know: 90 + 145 = ", 235, "Just add them."),
     box("Take that from the full turn: x = 360 " + MINUS + " 235 = ", 125, "Subtract 235 from 360.", post="°.", phase="substitute"),
     box("Check they fill the turn: 90 + 145 + 125 = ", 360, "Add all three.", post="°.", phase="substitute",
         done="A full turn, so x = 125° is right."),
   ]},
  {"display": "A transversal crosses two parallel lines. Angle \\(a\\) is alternate to an angle of \\(58°\\). Angle \\(b\\) lies on a straight line with \\(a\\). Find \\(b\\).",
   "solutions": [122], "input_type": "single_value", "calculator": False,
   "hint": "Alternate angles are equal, so find a first, then use the straight line for b.",
   "misconceptions": [mc("stopped_early",
     "That is angle a, the alternate angle, which is 58°. The question asks for b, which is on a straight line with a: b = 180 " + MINUS + " 58 = 122°.", 58)],
   "guided_steps": [
     say("Two parallel lines with a transversal. Alternate angles (the Z shape) are equal."),
     box("Angle a is alternate to 58°, so a = ", 58, "Alternate angles are equal.", post="°."),
     box("Angle b is on a straight line with a, so b = 180 " + MINUS + " 58 = ", 122, "Straight line, subtract from 180.", post="°.", phase="substitute"),
     box("Check a and b make a straight line: 58 + 122 = ", 180, "Add a and b.", post="°.", phase="substitute",
         done="A straight line, so b = 122° is right."),
   ]},
  {"display": "Co-interior angles: one is \\(110°\\). Find the other.",
   "solutions": [70], "input_type": "single_value", "calculator": False,
   "hint": "Co-interior (allied) angles add to 180.",
   "misconceptions": [mc("treated_as_equal",
     "You may have treated these as equal, like alternate angles. Co-interior angles add to 180°, so the other is 180 " + MINUS + " 110 = 70°.", 110)],
   "guided_steps": [
     say("Co-interior angles (the C shape between parallel lines, on the same side) add up to 180°."),
     box("Write the rule as a sum. The two angles total ", 180, "Co-interior angles add to 180.", post="°."),
     box("So the other angle = 180 " + MINUS + " 110 = ", 70, "Subtract 110 from 180.", post="°.", phase="substitute"),
     box("Check they add to 180: 110 + 70 = ", 180, "Add both angles.", post="°.", phase="substitute",
         done="They add to 180°, so the other is 70°."),
   ]},
  {"display": "An isosceles triangle has a base angle of \\(70°\\). Find the top angle.",
   "solutions": [40], "input_type": "single_value", "calculator": False,
   "hint": "The two base angles are equal, and all three add to 180.",
   "misconceptions": [mc("one_base_only",
     "It looks like you subtracted only one base angle. An isosceles triangle has TWO equal base angles: top = 180 " + MINUS + " 70 " + MINUS + " 70 = 40°.", 110)],
   "guided_steps": [
     say("An isosceles triangle has two equal base angles. Both are 70°."),
     box("Add the two base angles: 70 + 70 = ", 140, "Two base angles, both 70."),
     box("All three add to 180, so the top = 180 " + MINUS + " 140 = ", 40, "Subtract 140 from 180.", post="°.", phase="substitute"),
     box("Check: 70 + 70 + 40 = ", 180, "Add all three.", post="°.", phase="substitute",
         done="A full triangle, so the top is 40°."),
   ]},
  {"display": "A quadrilateral has angles \\(80°\\), \\(100°\\), \\(95°\\) and \\(x°\\). Find \\(x\\).",
   "solutions": [85], "input_type": "single_value", "calculator": False,
   "hint": "The four angles of a quadrilateral add to 360.",
   "misconceptions": [mc("added_givens",
     "It looks like you added the three known angles. A quadrilateral's angles add to 360°, so x = 360 " + MINUS + " 275 = 85°.", 275)],
   "guided_steps": [
     say("The four angles of any quadrilateral add up to 360°."),
     box("Add the three you know: 80 + 100 + 95 = ", 275, "Add all three."),
     box("Take that from 360: x = 360 " + MINUS + " 275 = ", 85, "Subtract 275 from 360.", post="°.", phase="substitute"),
     box("Check all four add to 360: 80 + 100 + 95 + 85 = ", 360, "Add all four.", post="°.", phase="substitute",
         done="They add to 360°, so x = 85°."),
   ]},
]

# ---------------- SILVER ----------------
silver = [
  {"display": "Find the interior angle sum of a nonagon (9 sides).",
   "solutions": [1260], "input_type": "single_value", "calculator": False,
   "hint": "Interior angle sum = (n " + MINUS + " 2) × 180 with n = 9.",
   "misconceptions": [mc("forgot_minus_two",
     "It looks like you multiplied 9 × 180. Subtract 2 from the number of sides first: (9 " + MINUS + " 2) × 180 = 7 × 180 = 1260°.", 1620)],
   "guided_steps": [
     say("The interior angle sum of a polygon is (n " + MINUS + " 2) × 180°. A nonagon has n = 9."),
     box("First work out n " + MINUS + " 2: 9 " + MINUS + " 2 = ", 7, "Take 2 off the number of sides."),
     box("Multiply by 180: 7 × 180 = ", 1260, "7 lots of 180.", post="°.", phase="substitute"),
     box("Check by splitting the nonagon into 7 triangles, each 180°: 7 × 180 = ", 1260, "Same multiplication confirms it.", post="°.", phase="substitute",
         done="A nonagon splits into 7 triangles, so 1260° is right."),
   ]},
  {"display": "Find each interior angle of a regular hexagon.",
   "solutions": [120], "input_type": "single_value", "calculator": False,
   "hint": "Find the interior sum with (n " + MINUS + " 2) × 180, then divide by 6.",
   "misconceptions": [
     mc("gave_exterior",
       "60° is the exterior angle (360 ÷ 6). The interior angle is 180 " + MINUS + " 60 = 120°, or the interior sum 720 ÷ 6 = 120°.", 60),
     mc("gave_sum",
       "720° is the total of all six angles. Divide by 6 for each one: 720 ÷ 6 = 120°.", 720),
   ],
   "guided_steps": [
     say("A regular hexagon has 6 equal angles. Find the total, then share it out."),
     box("Interior sum = (6 " + MINUS + " 2) × 180 = 4 × 180 = ", 720, "4 lots of 180.", post="°."),
     box("Regular, so divide by 6: 720 ÷ 6 = ", 120, "Share the total between 6 angles.", post="°.", phase="substitute"),
     box("Check: 6 × 120 = ", 720, "Multiply back.", post="°.", phase="substitute",
         done="Six 120° angles total 720°, so each is 120°."),
   ]},
  {"display": "Each exterior angle of a regular polygon is \\(40°\\). How many sides?",
   "solutions": [9], "input_type": "single_value", "calculator": False,
   "hint": "Exterior angles add to 360, so divide 360 by the exterior angle.",
   "misconceptions": [mc("used_180",
     "It looks like you divided into 180°. The exterior angles add to a full turn, 360°, so n = 360 ÷ 40 = 9.", 4.5)],
   "guided_steps": [
     say("The exterior angles of any polygon add up to 360°. Each one here is 40°."),
     box("The exterior angles total ", 360, "A full turn.", post="°."),
     box("Number of sides = 360 ÷ 40 = ", 9, "Divide 360 by 40.", phase="substitute"),
     box("Check: 9 × 40 = ", 360, "Multiply back.", post="°.", phase="substitute",
         done="Nine 40° exterior angles make 360°, so 9 sides."),
   ]},
  {"display": "The interior angle of a regular polygon is \\(156°\\). Find the exterior angle.",
   "solutions": [24], "input_type": "single_value", "calculator": False,
   "hint": "Interior and exterior angles add to 180.",
   "misconceptions": [mc("used_360",
     "It looks like you subtracted from 360°. An interior and its exterior angle sit on a straight line and add to 180°, so exterior = 180 " + MINUS + " 156 = 24°.", 204)],
   "guided_steps": [
     say("An interior angle and its exterior angle lie on a straight line, so they add to 180°."),
     box("They add to ", 180, "Straight line.", post="°."),
     box("Exterior = 180 " + MINUS + " 156 = ", 24, "Subtract 156 from 180.", post="°.", phase="substitute"),
     box("Check they make a straight line: 156 + 24 = ", 180, "Add both.", post="°.", phase="substitute",
         done="A straight line, so the exterior is 24°."),
   ]},
  {"display": "Two angles in a triangle are \\(3x°\\) and \\(5x°\\). The third is \\(44°\\). Find \\(x\\).",
   "solutions": [17], "input_type": "single_value", "calculator": False,
   "hint": "Add all three angles, set the total to 180, then solve for x.",
   "misconceptions": [mc("dropped_constant",
     "It looks like you left out the 44°. All three add to 180: 3x + 5x + 44 = 180, so 8x = 136 and x = 17.", 22.5)],
   "guided_steps": [
     say("The three angles of a triangle add to 180°. Add the expressions and the number."),
     box("Combine the x terms: 3x + 5x = ", 8, "Add the coefficients 3 and 5.", post="x"),
     box("The total is 180 and 44 is known, so 8x = 180 " + MINUS + " 44 = ", 136, "Subtract 44 from 180.", phase="substitute"),
     box("x = 136 ÷ 8 = ", 17, "Divide by 8.", phase="substitute"),
     box("Check: 3(17) + 5(17) + 44 = 51 + 85 + 44 = ", 180, "Work out each angle and add.", post="°.", phase="substitute",
         done="The angles total 180°, so x = 17."),
   ]},
  {"display": "The interior angle of a regular polygon is \\(108°\\). How many sides does it have?",
   "solutions": [5], "input_type": "single_value", "calculator": False,
   "hint": "Find the exterior angle (180 " + MINUS + " interior), then divide 360 by it.",
   "misconceptions": [mc("gave_exterior",
     "72° is the exterior angle (180 " + MINUS + " 108). The number of sides is 360 ÷ 72 = 5.", 72)],
   "guided_steps": [
     say("Work backwards. First the exterior angle, then how many fit into 360°."),
     box("Exterior = 180 " + MINUS + " 108 = ", 72, "Interior and exterior add to 180.", post="°."),
     box("Number of sides = 360 ÷ 72 = ", 5, "Divide 360 by the exterior angle.", phase="substitute"),
     box("Check a regular pentagon: interior sum = (5 " + MINUS + " 2) × 180 = 540, each = 540 ÷ 5 = ", 108, "Find each interior angle of a 5-sided shape.", post="°.", phase="substitute",
         done="Each interior angle is 108°, so 5 sides is right."),
   ]},
  {"display": "A pentagon has angles \\(100°\\), \\(110°\\), \\(120°\\), \\(130°\\) and \\(x°\\). Find \\(x\\).",
   "solutions": [80], "input_type": "single_value", "calculator": False,
   "hint": "A pentagon's angles add to (5 " + MINUS + " 2) × 180 = 540.",
   "misconceptions": [mc("added_givens",
     "It looks like you added the four known angles. A pentagon's angles add to 540°, so x = 540 " + MINUS + " 460 = 80°.", 460)],
   "guided_steps": [
     say("A pentagon has 5 angles that add up to (5 " + MINUS + " 2) × 180 = 540°."),
     box("Add the four you know: 100 + 110 + 120 + 130 = ", 460, "Add all four."),
     box("Take that from 540: x = 540 " + MINUS + " 460 = ", 80, "Subtract 460 from 540.", post="°.", phase="substitute"),
     box("Check all five add to 540: 100 + 110 + 120 + 130 + 80 = ", 540, "Add all five.", post="°.", phase="substitute",
         done="They total 540°, so x = 80°."),
   ]},
]

# ---------------- GOLD ----------------
gold = [
  {"display": "A regular polygon has interior angle \\(162°\\). How many sides?",
   "solutions": [20], "input_type": "single_value", "calculator": False,
   "hint": "Find the exterior angle (180 " + MINUS + " 162), then divide 360 by it.",
   "misconceptions": [mc("gave_exterior",
     "18° is the exterior angle (180 " + MINUS + " 162). The number of sides is 360 ÷ 18 = 20.", 18)],
   "guided_steps": [
     say("From the interior angle, find the exterior, then see how many exterior angles fit into 360°."),
     box("Exterior = 180 " + MINUS + " 162 = ", 18, "Interior and exterior add to 180.", post="°."),
     box("Number of sides = 360 ÷ 18 = ", 20, "Divide 360 by 18.", phase="substitute"),
     box("Check: 20 × 18 = ", 360, "Multiply back to 360.", post="°.", phase="substitute",
         done="Twenty 18° exterior angles make 360°, so 20 sides."),
   ]},
  {"display": "In a parallelogram, one angle is \\((3x + 10)°\\) and the adjacent angle is \\((2x + 20)°\\). Find \\(x\\).",
   "solutions": [30], "input_type": "single_value", "calculator": False,
   "hint": "Adjacent angles in a parallelogram add to 180; form an equation and solve.",
   "misconceptions": [mc("set_equal",
     "It looks like you set the two angles equal. Adjacent angles in a parallelogram add to 180°, not equal: (3x + 10) + (2x + 20) = 180, so 5x + 30 = 180 and x = 30.", 10)],
   "guided_steps": [
     say("Adjacent angles in a parallelogram (a co-interior pair) add to 180°. Add the two expressions."),
     box("Combine the x terms: 3x + 2x = ", 5, "Add 3 and 2.", post="x"),
     box("Combine the numbers: 10 + 20 = ", 30, "Add 10 and 20."),
     box("So 5x + 30 = 180, giving 5x = 180 " + MINUS + " 30 = ", 150, "Subtract 30 from 180.", phase="substitute"),
     box("x = 150 ÷ 5 = ", 30, "Divide by 5.", phase="substitute"),
     box("Check the angles: 3(30) + 10 = 100 and 2(30) + 20 = 80, so 100 + 80 = ", 180, "Work out both angles and add.", post="°.", phase="substitute",
         done="Adjacent angles add to 180°, so x = 30."),
   ]},
  {"display": "The interior angles of a polygon sum to \\(1620°\\). How many sides does it have?",
   "solutions": [11], "input_type": "single_value", "calculator": False,
   "hint": "Use (n " + MINUS + " 2) × 180 = 1620 and solve for n.",
   "misconceptions": [mc("forgot_add_two",
     "9 comes from 1620 ÷ 180, but that equals n " + MINUS + " 2, not n. Add 2 back: n = 9 + 2 = 11.", 9)],
   "guided_steps": [
     say("The interior angle sum is (n " + MINUS + " 2) × 180°. Set it equal to 1620 and solve for n."),
     box("Divide the sum by 180: 1620 ÷ 180 = ", 9, "How many 180s in 1620."),
     box("That result is n " + MINUS + " 2, so n = 9 + 2 = ", 11, "Add the 2 back.", phase="substitute"),
     box("Check: (11 " + MINUS + " 2) × 180 = 9 × 180 = ", 1620, "Put n = 11 back into the formula.", post="°.", phase="substitute",
         done="An 11-sided polygon has an interior sum of 1620°, so 11 sides."),
   ]},
  {"display": "Two regular polygons share a side. One is a square and the other is a regular hexagon. Find the angle between the unshared sides at the shared vertex.",
   "solutions": [150], "input_type": "single_value", "calculator": False,
   "hint": "The three angles at the shared vertex fill 360; subtract the square and hexagon angles.",
   "misconceptions": [mc("added_two_angles",
     "210° is the square and hexagon angles added (90 + 120). The three angles at the vertex fill a full turn, so the gap = 360 " + MINUS + " 210 = 150°.", 210)],
   "guided_steps": [
     say("At the shared vertex, three angles meet and fill a full turn of 360°: the square's angle, the hexagon's angle, and the gap."),
     box("A square's interior angle is ", 90, "A square has right angles.", post="°."),
     box("A regular hexagon's interior angle is (6 " + MINUS + " 2) × 180 ÷ 6 = ", 120, "720 shared between 6 angles.", post="°."),
     box("The gap = 360 " + MINUS + " 90 " + MINUS + " 120 = ", 150, "Subtract both from 360.", post="°.", phase="substitute"),
     box("Check they fill the turn: 90 + 120 + 150 = ", 360, "Add all three.", post="°.", phase="substitute",
         done="The three angles make a full turn, so the gap is 150°."),
   ]},
  {"display": "An exterior angle of a regular polygon is \\(x°\\). The interior angle is \\(4x°\\). Find \\(x\\).",
   "solutions": [36], "input_type": "single_value", "calculator": False,
   "hint": "Interior and exterior angles add to 180; use x + 4x = 180.",
   "misconceptions": [mc("used_360",
     "It looks like you used 360°. An interior and exterior angle sit on a straight line and add to 180°: x + 4x = 180, so 5x = 180 and x = 36.", 72)],
   "guided_steps": [
     say("An interior angle and its exterior angle add to 180° (a straight line). Here they are 4x and x."),
     box("Combine: x + 4x = ", 5, "Add the coefficients 1 and 4.", post="x"),
     box("So 5x = 180, giving x = 180 ÷ 5 = ", 36, "Divide 180 by 5.", post="°.", phase="substitute"),
     box("Check: exterior 36 and interior 4 × 36 = 144, and 36 + 144 = ", 180, "Add the two angles.", post="°.", phase="substitute",
         done="They make a straight line, so x = 36."),
   ]},
]

# ---------------- tier_guides ----------------
tier_guides = {
  "bronze": {
    "title": "Bronze: one angle fact, one step",
    "steps": [
      "Spot the setup: a straight line (angles add to <strong>180°</strong>), a point (<strong>360°</strong>), a triangle (<strong>180°</strong>) or a quadrilateral (<strong>360°</strong>).",
      "Parallel lines give equal angles: <strong>alternate</strong> (Z) and <strong>corresponding</strong> (F) are equal; <strong>co-interior</strong> (C) add to 180°. Vertically opposite angles are <strong>equal</strong>.",
      "Add the angles you know, then subtract from the total to find the missing one.",
    ],
    "example": {
      "question": "Angles on a straight line are 130° and x°. Find x.",
      "steps": [
        {"label": "Rule", "content": "Angles on a straight line add to \\(180°\\)."},
        {"label": "Subtract", "content": "\\(x = 180 - 130\\)"},
        {"label": "Check", "content": "\\(50 + 130 = 180°\\) ✓"},
        {"label": "Answer", "content": "\\(x = 50°\\)", "isAnswer": True, "is_answer": True},
      ],
    },
  },
  "silver": {
    "title": "Silver: polygons and simple angle algebra",
    "steps": [
      "Interior angle sum of an n-sided polygon = <strong>\\((n-2) \\times 180°\\)</strong>. For a regular polygon, divide that sum by n for each angle.",
      "Exterior angles of any polygon add to <strong>360°</strong>, so each exterior angle of a regular polygon = <strong>\\(360° \\div n\\)</strong>, and interior + exterior = 180°.",
      "For angle algebra, add the expressions, set the total to 180° (triangle) or the correct polygon sum, then solve for the letter.",
    ],
    "example": {
      "question": "Find each interior angle of a regular pentagon.",
      "steps": [
        {"label": "Rule", "content": "Sum \\(= (5-2) \\times 180 = 540°\\)"},
        {"label": "Divide", "content": "\\(540 \\div 5\\)"},
        {"label": "Check", "content": "\\(5 \\times 108 = 540°\\) ✓"},
        {"label": "Answer", "content": "\\(108°\\)", "isAnswer": True, "is_answer": True},
      ],
    },
  },
  "gold": {
    "title": "Gold: work backwards and combine facts",
    "steps": [
      "Reverse the formulas: from an interior angle find the exterior (180 − interior), then \\(n = 360 \\div \\text{exterior}\\). From an angle sum, solve \\((n-2) \\times 180 = \\text{sum}\\).",
      "Combine several facts in one figure: shared vertices, ratios of interior to exterior, or angle expressions that must add to a known total.",
      "Always finish by checking your angle fits the rule you started from.",
    ],
    "example": {
      "question": "A regular polygon has exterior angle 24°. How many sides?",
      "steps": [
        {"label": "Rule", "content": "Exterior angles add to \\(360°\\)."},
        {"label": "Divide", "content": "\\(360 \\div 24\\)"},
        {"label": "Check", "content": "\\(15 \\times 24 = 360°\\) ✓"},
        {"label": "Answer", "content": "\\(15\\) sides", "isAnswer": True, "is_answer": True},
      ],
    },
  },
}

# ---------------- guided ----------------
guided = {
  "opener": {
    "steps": [
      say("You have probably heard skaters or gamers talk about pulling a '180' or a '360'. Those are angles, and you already know what they mean."),
      box("A '180' spins you to face the exact opposite way. A full spin, right back to where you started, is a '", 360, "A complete turn, all the way round.", post="'."),
      say("So a full turn is 360° and a half turn, facing the opposite way, is 180°. A straight line is exactly that half turn."),
      box("Two angles sit on a straight line. One is 120°. The line is a half turn (180°), so the other is 180 " + MINUS + " 120 = ", 60, "Both angles share the 180° of the half turn.", post="°."),
      say("That is the whole lesson in miniature: angles on a straight line share 180°, angles round a point share 360°, and nearly every fact here is one of those two turns split up. In algebra we call the missing angle \\(x\\) and write \\(x + 120 = 180\\)."),
    ],
  },
  "teach": {
    "bronze": {
      "display": "A triangle has angles \\(50°\\), \\(60°\\) and \\(x°\\). Find \\(x\\).",
      "steps": [
        say("Every triangle's angles add up to 180°."),
        box("The angles of a triangle add up to ", 180, "A triangle always totals this.", post="°."),
        box("Add the two you know: 50 + 60 = ", 110, "Just add them."),
        box("So x = 180 " + MINUS + " 110 = ", 70, "Subtract 110 from 180.", post="°."),
        box("Check the three add to 180: 50 + 60 + 70 = ", 180, "Add all three.", post="°.",
            done="A full triangle, so x = 70°. That is the one move: known angles subtracted from the total."),
      ],
    },
    "silver": {
      "display": "Find each interior angle of a regular octagon.",
      "steps": [
        say("An octagon has 8 sides. Find the interior total, then share it between the 8 equal angles."),
        box("First n " + MINUS + " 2: 8 " + MINUS + " 2 = ", 6, "Two fewer than the number of sides."),
        box("Multiply by 180: 6 × 180 = ", 1080, "6 lots of 180.", post="°."),
        box("Regular, so divide by 8: 1080 ÷ 8 = ", 135, "Share the total between 8 angles.", post="°."),
        box("Check: 8 × 135 = ", 1080, "Multiply back.", post="°.",
            done="Eight 135° angles total 1080°, so each is 135°. The new move: find the sum, then divide."),
      ],
    },
    "gold": {
      "display": "A regular polygon has interior angle \\(150°\\). How many sides?",
      "steps": [
        say("Work backwards. Turn the interior angle into an exterior angle, then count how many fit into 360°."),
        box("Exterior = 180 " + MINUS + " 150 = ", 30, "Interior and exterior add to 180.", post="°."),
        box("Number of sides = 360 ÷ 30 = ", 12, "Divide 360 by the exterior angle."),
        box("Check the interior sum: (12 " + MINUS + " 2) × 180 = ", 1800, "10 lots of 180.", post="°."),
        box("And each interior angle = 1800 ÷ 12 = ", 150, "Share between 12.", post="°.",
            done="Back to 150°, so 12 sides is right. The new move: reverse the formula to find n."),
      ],
    },
  },
}

# ---------------- method_card ----------------
method_card = {
  "title": "Finding Missing Angles",
  "steps": [
    "Name the setup: straight line (180°), point (360°), triangle (180°), quadrilateral (360°), or parallel lines.",
    "Parallel lines: alternate and corresponding angles are equal; co-interior angles add to 180°.",
    "Polygons: interior sum = (n " + MINUS + " 2) × 180°; each exterior angle of a regular polygon = 360° ÷ n; interior + exterior = 180°.",
    "Add what you know, subtract from the total (or solve the equation), then check it fits.",
  ],
  "content": "<p>Almost every angle problem shares out a known total. A <strong>straight line</strong> holds 180°, a <strong>point</strong> holds 360°, a <strong>triangle</strong> 180°, a <strong>quadrilateral</strong> 360°.</p><p>For an n-sided polygon the interior angles total \\((n-2)\\times 180°\\); each exterior angle of a regular polygon is \\(360°\\div n\\), and interior + exterior = 180°.</p>",
  "example": "<p><strong>Find each interior angle of a regular hexagon.</strong></p><p>Sum \\(= (6-2)\\times 180 = 720°\\); each \\(= 720\\div 6 = 120°\\).</p>",
}

# ---------------- preserved fields ----------------
with io.open("_live_geometry_L01.json", encoding="utf-8") as f:
    live = json.load(f)

# Style fix: strip em dashes from preserved worked_examples labels (validator hard-rejects them)
for we in live.get("worked_examples", []):
    for st in we.get("steps", []):
        if isinstance(st.get("label"), str) and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

pd = {
  "method_card": method_card,
  "topic_links": live["topic_links"],
  "problem_bank": {
    "bronze": bronze,
    "silver": silver,
    "gold": gold,
    "bronze_description": "One angle fact applied in a single step: straight lines, points, triangles, quadrilaterals and parallel-line angles.",
    "silver_description": "Polygon angle sums and regular-polygon angles, plus simple angle equations to solve.",
    "gold_description": "Work backwards from angle facts and combine several of them in one figure.",
  },
  "tier_guides": tier_guides,
  "guided": guided,
  "related_videos": live["related_videos"],
  "worked_examples": live["worked_examples"],
}

# ================= INDEPENDENT ARITHMETIC VERIFICATION =================
import re
errs = []

expected_solutions = {
  ("bronze",0):108, ("bronze",1):68, ("bronze",2):65, ("bronze",3):125,
  ("bronze",4):122, ("bronze",5):70, ("bronze",6):40, ("bronze",7):85,
  ("silver",0):1260, ("silver",1):120, ("silver",2):9, ("silver",3):24,
  ("silver",4):17, ("silver",5):5, ("silver",6):80,
  ("gold",0):20, ("gold",1):30, ("gold",2):11, ("gold",3):150, ("gold",4):36,
}
for (tier,i),want in expected_solutions.items():
    got = pd["problem_bank"][tier][i]["solutions"][0]
    if got != want:
        errs.append(f"{tier}[{i}] solution {got} != fresh-solved {want}")

def eval_boxes(steps, label):
    for j, st in enumerate(steps):
        if st.get("answer") is None:
            continue
        pre = st.get("pre","")
        m = re.search(r'([0-9−+×÷().\s]+)=\s*$', pre)
        if not m:
            continue
        expr = m.group(1)
        py = expr.replace("−","-").replace("×","*").replace("÷","/").strip()
        if not py or py == "-":
            continue
        try:
            val = eval(py)
        except Exception:
            continue
        if abs(val - st["answer"]) > 1e-9:
            errs.append(f"{label}[{j}] pre-arith '{expr.strip()}' = {val} but answer={st['answer']}")

for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        eval_boxes(p["guided_steps"], f"{tier}[{i}].guided_steps")
eval_boxes(guided["opener"]["steps"], "opener")
for tier in ("bronze","silver","gold"):
    eval_boxes(guided["teach"][tier]["steps"], f"teach.{tier}")

for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        sol = p["solutions"][0]
        answers = [st["answer"] for st in p["guided_steps"] if st.get("answer") is not None]
        if sol not in answers:
            errs.append(f"{tier}[{i}] solution {sol} never a box answer {answers}")

for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        sol = float(p["solutions"][0])
        for k,m in enumerate(p.get("misconceptions",[])):
            e = m.get("expect")
            if e is not None and abs(float(e)-sol) < 0.011:
                errs.append(f"{tier}[{i}].mc[{k}] expect {e} == solution {sol}")

if errs:
    print("ARITH ERRORS:")
    for e in errs:
        print("  -", e)
    raise SystemExit(1)

with io.open("lesson_geometry-L01.json","w",encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)
print("built lesson_geometry-L01.json  (arith self-check clean)")
