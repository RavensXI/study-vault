# -*- coding: utf-8 -*-
import json, io

pd = json.load(io.open("_live_raw.json", encoding="utf-8"))

# ---------------------------------------------------------------- method_card (slim)
pd["method_card"]["content"] = (
    "<p>A <strong>ratio</strong> compares quantities in the same units and simplifies by "
    "dividing every part by their highest common factor.</p>"
    "<p>To <strong>share an amount</strong>: add the parts, divide the total by the sum of "
    "parts to find one part, then multiply each ratio number by one part.</p>"
    "<p>The <strong>unitary method</strong> handles proportion: find one unit first, then "
    "scale. If 5 pens cost £3.50, one pen is \\(\\frac{3.50}{5} = £0.70\\), so 8 pens cost "
    "\\(8 \\times 0.70 = £5.60\\).</p>"
)

# ---------------------------------------------------------------- worked_examples: strip em dashes from labels
for we in pd["worked_examples"]:
    for st in we["steps"]:
        st["label"] = st["label"].replace(" — ", ": ")

# ---------------------------------------------------------------- helper builders
def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def say(text):
    return {"say": text}

def misc(expect, message, pattern="wrong_formula"):
    return {"check": "common", "expect": expect, "message": message, "pattern": pattern}

pb = pd["problem_bank"]

# ================================================================ BRONZE
b_share100 = {
    "display": "Share £100 in the ratio \\(3 : 2\\). How much is the larger share?",
    "solutions": [60], "calculator": False, "input_type": "single_value",
    "hint": "Add the parts, divide £100 by the total, then multiply by the larger ratio number.",
    "misconceptions": [misc(40,
        "Total parts = 3 + 2 = 5, so one part = 100 ÷ 5 = £20. The larger share uses the 3: 3 × 20 = £60. Getting £40 means you multiplied by the 2, which is the smaller share.")],
    "guided_steps": [
        say("Sharing means add the parts, find one part, then multiply."),
        box("Add the parts: 3 + 2 = ", 5, "Add the two ratio numbers."),
        box("One part = 100 ÷ 5 = £", 20, "Divide the money by the total parts.", done="That £20 is what one share-part is worth."),
        box("3 × 20 = £", 60, "Multiply one part by 3.", say="The larger share uses the 3.", phase="substitute"),
        box("Check the shares total: 60 + (2 × 20) = £", 100, "Both shares should add to £100.", done="60 + 40 = 100, so the larger share is £60.", phase="substitute"),
    ],
}
b_simp12 = {
    "display": "Simplify the ratio \\(12 : 18\\)",
    "options": ["\\(2 : 3\\)", "\\(3 : 2\\)", "\\(4 : 6\\)", "\\(6 : 9\\)"],
    "solutions": [0], "calculator": False, "input_type": "multiple_choice",
    "hint": "Divide both numbers by their highest common factor.",
    "misconceptions": [misc(2,
        "Divide both parts by the HCF (6), not just any common factor. 12 ÷ 6 = 2 and 18 ÷ 6 = 3, giving 2 : 3. Dividing by 3 leaves 4 : 6, which is not fully simplified.", "forgot_step")],
}
b_simp45 = {
    "display": "Simplify the ratio \\(45 : 30\\)",
    "options": ["\\(9 : 6\\)", "\\(2 : 3\\)", "\\(3 : 2\\)", "\\(15 : 10\\)"],
    "solutions": [2], "calculator": False, "input_type": "multiple_choice",
    "hint": "Find the largest number that divides into both 45 and 30.",
    "misconceptions": [misc(0,
        "The HCF of 45 and 30 is 15, not 5. Dividing by 5 gives 9 : 6, which still simplifies. Divide both by 15 to reach 3 : 2.", "forgot_step")],
}
b_equiv = {
    "display": "The ratio \\(2 : 5\\) is equivalent to \\(6 : n\\). What is the value of \\(n\\)?",
    "solutions": [15], "calculator": False, "input_type": "single_value",
    "hint": "Work out what the first part was multiplied by, then do the same to the second.",
    "misconceptions": [misc(9,
        "Find the multiplier: 6 ÷ 2 = 3, so n = 5 × 3 = 15. Adding 4 to each part gives 9, but equivalent ratios scale by multiplying, not adding.", "wrong_formula")],
    "guided_steps": [
        say("Equivalent ratios keep the same shape by multiplying both parts by the same number."),
        box("The first part goes 2 to 6, so the multiplier is 6 ÷ 2 = ", 3, "Divide the new first part by the old first part.", done="Every part is multiplied by 3."),
        box("n = 5 × 3 = ", 15, "Multiply the second part by 3.", say="Apply the same multiplier to the second part.", phase="substitute"),
        box("Check the first parts match: 2 × 3 = ", 6, "It should give the 6 shown.", done="2 × 3 = 6 matches, so n = 15 is right.", phase="substitute"),
    ],
}
b_1n = {
    "display": "Write \\(5 : 20\\) in the form \\(1 : n\\)",
    "options": ["\\(1 : 5\\)", "\\(1 : 4\\)", "\\(1 : 3\\)", "\\(4 : 1\\)"],
    "solutions": [1], "calculator": False, "input_type": "multiple_choice",
    "hint": "Divide both parts by the first number.",
    "misconceptions": [misc(3,
        "Divide both parts by the first number: 5 ÷ 5 = 1 and 20 ÷ 5 = 4, giving 1 : 4. Writing 4 : 1 reverses the order; the 1 must come first.", "forgot_step")],
}
b_pens = {
    "display": "If 4 pens cost £2.60, how much do 7 pens cost? Give your answer in £.",
    "solutions": [4.55], "calculator": False, "input_type": "single_value",
    "hint": "Find the cost of one pen first, then multiply by seven.",
    "misconceptions": [misc(18.2,
        "Find one pen first: £2.60 ÷ 4 = £0.65, then 7 × £0.65 = £4.55. Multiplying £2.60 by 7 skips finding the price of one pen.", "forgot_step")],
    "guided_steps": [
        say("Unitary method: find the cost of one first, then scale up."),
        box("One pen: 2.60 ÷ 4 = £", 0.65, "Divide the total cost by 4.", done="One pen costs £0.65."),
        box("7 × 0.65 = £", 4.55, "Multiply one pen by 7.", say="Now scale up to 7 pens.", phase="substitute"),
        box("Check by scaling back: 4.55 ÷ 7 = £", 0.65, "It should return the price of one pen.", done="It gives £0.65 a pen, so £4.55 is right.", phase="substitute"),
    ],
}
b_sweets = {
    "display": "Share 72 sweets in the ratio \\(5 : 3 : 1\\). How many does the largest share get?",
    "solutions": [40], "calculator": False, "input_type": "single_value",
    "hint": "Add all three parts, divide 72, then multiply by the largest ratio number.",
    "misconceptions": [misc(45,
        "Total parts = 5 + 3 + 1 = 9, so one part = 72 ÷ 9 = 8, and the largest = 5 × 8 = 40. Getting 45 means the 1 part was forgotten, dividing by 8 instead of 9.")],
    "guided_steps": [
        say("Three-part share, same three moves: add, divide, multiply."),
        box("Add the parts: 5 + 3 + 1 = ", 9, "Add all three ratio numbers."),
        box("One part = 72 ÷ 9 = ", 8, "Divide the sweets by the total parts.", done="One part is 8 sweets."),
        box("5 × 8 = ", 40, "Multiply one part by 5.", say="The largest share uses the 5.", phase="substitute"),
        box("Check all shares total: 40 + (3 × 8) + (1 × 8) = ", 72, "They should add to 72 sweets.", done="40 + 24 + 8 = 72, so the largest share is 40.", phase="substitute"),
    ],
}
b_units = {
    "display": "Express \\(300\\text{ ml} : 1.2\\text{ litres}\\) as a simplified ratio.",
    "options": ["\\(1 : 4\\)", "\\(3 : 12\\)", "\\(1 : 3\\)", "\\(300 : 1200\\)"],
    "solutions": [0], "calculator": False, "input_type": "multiple_choice",
    "hint": "Convert to the same unit before simplifying.",
    "misconceptions": [misc(3,
        "Convert to the same unit first: 1.2 litres = 1200 ml. Then 300 : 1200 divides by 300 to give 1 : 4. Leaving it as 300 : 1200 is not simplified.", "unit_error")],
}
pb["bronze"] = [b_share100, b_simp12, b_simp45, b_equiv, b_1n, b_pens, b_sweets, b_units]

# ================================================================ SILVER
s_450 = {
    "display": "Share £450 in the ratio \\(2 : 3 : 4\\). How much is the middle share?",
    "solutions": [150], "calculator": False, "input_type": "single_value",
    "hint": "Add the parts, divide £450, then multiply by the middle ratio number.",
    "misconceptions": [misc(100,
        "Total parts = 2 + 3 + 4 = 9, so one part = 450 ÷ 9 = £50. The middle share uses the 3: 3 × 50 = £150. Getting £100 means you multiplied by the 2, which is the smallest share.")],
    "guided_steps": [
        say("Add the parts, find one part, then pick out the share you need."),
        box("Add the parts: 2 + 3 + 4 = ", 9, "Add all three ratio numbers."),
        box("One part = 450 ÷ 9 = £", 50, "Divide the money by the total parts.", done="One part is £50."),
        box("3 × 50 = £", 150, "Multiply one part by 3.", say="The middle share uses the 3.", phase="substitute"),
        box("Check all shares total: (2 × 50) + 150 + (4 × 50) = £", 450, "They should add to £450.", done="100 + 150 + 200 = 450, so the middle share is £150.", phase="substitute"),
    ],
}
s_recipe = {
    "display": "A recipe for 4 people uses 300 g of flour. How many grams are needed for 10 people?",
    "solutions": [750], "calculator": False, "input_type": "single_value",
    "hint": "Find the amount for one person, then multiply by ten.",
    "misconceptions": [misc(3000,
        "One person needs 300 ÷ 4 = 75 g, then 10 × 75 = 750 g. Multiplying 300 by 10 gives 3000 g but skips finding the amount per person.", "forgot_step")],
    "guided_steps": [
        say("Find the amount for one person, then scale to ten."),
        box("One person: 300 ÷ 4 = ", 75, "Divide the flour by 4 people.", done="One person needs 75 g."),
        box("10 × 75 = ", 750, "Multiply one person by 10.", say="Now scale up to 10 people.", phase="substitute"),
        box("Check by scaling back: 750 ÷ 10 = ", 75, "It should return the amount for one person.", done="75 g each, so 750 g for ten is right.", phase="substitute"),
    ],
}
s_map = {
    "display": "A map scale is \\(1 : 50\\,000\\). Two points are 8 cm apart on the map. What is the real distance in km?",
    "solutions": [4], "calculator": False, "input_type": "single_value",
    "hint": "Multiply by the scale for centimetres, then convert to kilometres.",
    "misconceptions": [misc(4000,
        "8 × 50 000 = 400 000 cm. There are 100 000 cm in 1 km, so 400 000 ÷ 100 000 = 4 km. Dividing by 100 instead gives 4000, which is the distance in metres.", "unit_error")],
    "guided_steps": [
        say("A scale of 1 : 50 000 means every 1 cm on the map is 50 000 cm in real life."),
        box("Real distance in cm: 8 × 50000 = ", 400000, "Multiply the map distance by the scale.", done="That is 400 000 cm on the ground."),
        box("400000 ÷ 100000 = ", 4, "Divide by 100 000.", say="Convert centimetres to kilometres. There are 100 000 cm in 1 km.", phase="substitute"),
        box("Check by scaling back: 4 km is 400 000 cm, and 400000 ÷ 50000 = ", 8, "It should return the 8 cm on the map.", done="It gives 8 cm, so 4 km is right.", phase="substitute"),
    ],
}
s_dogs = {
    "display": "The ratio of dogs to cats in a shelter is \\(3 : 5\\). There are 24 dogs. How many cats are there?",
    "solutions": [40], "calculator": False, "input_type": "single_value",
    "hint": "The dogs are the 3 part, so find one part, then multiply by 5.",
    "misconceptions": [misc(120,
        "The 24 dogs are 3 parts, so one part = 24 ÷ 3 = 8, and cats = 5 × 8 = 40. Getting 120 means you multiplied 24 by 5 without finding one part first.")],
    "guided_steps": [
        say("The 24 dogs are the 3 part. Find one part first."),
        box("One part = 24 ÷ 3 = ", 8, "Divide the dogs by their ratio number.", done="One part is 8 animals."),
        box("5 × 8 = ", 40, "Multiply one part by 5.", say="Cats are the 5 part.", phase="substitute"),
        box("Check the ratio: 40 ÷ 8 = ", 5, "It should give the cats ratio number.", done="40 ÷ 8 = 5, matching the ratio, so 40 cats is right.", phase="substitute"),
    ],
}
s_paint = {
    "display": "Purple paint is mixed using red and blue in the ratio \\(3 : 7\\). How many ml of blue are needed to mix with 150 ml of red?",
    "solutions": [350], "calculator": False, "input_type": "single_value",
    "hint": "The red is the 3 part, so find one part, then multiply by 7.",
    "misconceptions": [misc(1050,
        "The 150 ml of red is 3 parts, so one part = 150 ÷ 3 = 50, and blue = 7 × 50 = 350. Getting 1050 means you multiplied 150 by 7 without finding one part first.")],
    "guided_steps": [
        say("The 150 ml of red is the 3 part. Find one part first."),
        box("One part = 150 ÷ 3 = ", 50, "Divide the red by its ratio number.", done="One part is 50 ml."),
        box("7 × 50 = ", 350, "Multiply one part by 7.", say="Blue is the 7 part.", phase="substitute"),
        box("Check the ratio: 350 ÷ 50 = ", 7, "It should give the blue ratio number.", done="350 ÷ 50 = 7, matching the ratio, so 350 ml is right.", phase="substitute"),
    ],
}
# S5 replaces the off-topic inverse-proportion problem with a direct-proportion speed problem.
s_train = {
    "display": "A train travels 180 km in 4 hours at a constant speed. How far does it travel in 7 hours? Give your answer in km.",
    "solutions": [315], "calculator": False, "input_type": "single_value",
    "hint": "Find the distance in one hour, then multiply by seven.",
    "misconceptions": [misc(1260,
        "Find the speed first: 180 ÷ 4 = 45 km each hour, then 45 × 7 = 315 km. Multiplying 180 by 7 gives 1260 but skips the one-hour distance.", "forgot_step")],
    "guided_steps": [
        say("Direct proportion: find the distance for one hour, then scale up."),
        box("Distance in one hour: 180 ÷ 4 = ", 45, "Divide the distance by the time.", done="The train covers 45 km each hour."),
        box("7 × 45 = ", 315, "Multiply one hour by 7.", say="Now scale up to 7 hours.", phase="substitute"),
        box("Check by scaling back: 315 ÷ 7 = ", 45, "It should return the one-hour distance.", done="45 km an hour, so 315 km in 7 hours is right.", phase="substitute"),
    ],
}
s_1n = {
    "display": "Write \\(4 : 14\\) in the form \\(1 : n\\). Give \\(n\\) as a decimal.",
    "solutions": [3.5], "calculator": False, "input_type": "single_value",
    "hint": "Divide both parts by the first number.",
    "misconceptions": [misc(14,
        "Divide both parts by the first number: 4 ÷ 4 = 1 and 14 ÷ 4 = 3.5, giving 1 : 3.5. Leaving n as 14 means the second part was not divided.", "forgot_step")],
    "guided_steps": [
        say("To reach the form 1 : n, divide both parts by the first number."),
        box("Divide the first part by itself: 4 ÷ 4 = ", 1, "Anything divided by itself is 1.", done="The first part becomes 1."),
        box("n = 14 ÷ 4 = ", 3.5, "Divide 14 by 4.", say="Do the same to the second part.", phase="substitute"),
        box("Check: 3.5 × 4 = ", 14, "It should return the original second part.", done="3.5 × 4 = 14, so 1 : 3.5 is right.", phase="substitute"),
    ],
}
pb["silver"] = [s_450, s_recipe, s_map, s_dogs, s_paint, s_train, s_1n]

# ================================================================ GOLD
g_alibob = {
    "display": "Ali and Bob share money in the ratio \\(5 : 3\\). Ali gets £40 more than Bob. How much does Bob get?",
    "solutions": [60], "calculator": False, "input_type": "single_value",
    "hint": "The £40 is the difference, worth 2 parts. Find one part, then Bob's 3 parts.",
    "misconceptions": [misc(24,
        "The £40 is the difference between the shares, worth 5 − 3 = 2 parts, so one part = £20 and Bob = 3 × 20 = £60. Getting £24 means you treated £40 as the total and found three fifths of it.")],
    "guided_steps": [
        say("The £40 is the difference between the shares, not the total. Work in parts."),
        box("Difference in parts: 5 − 3 = ", 2, "Subtract the smaller ratio number from the larger."),
        box("That 2-part gap is £40, so one part = 40 ÷ 2 = £", 20, "Divide the £40 gap by the 2 parts.", done="One part is £20."),
        box("3 × 20 = £", 60, "Multiply one part by 3.", say="Bob has the 3 part.", phase="substitute"),
        box("Check the gap: Ali is 5 × 20 = £100, so 100 − 60 = £", 40, "It should equal the £40 difference.", done="The gap is £40, so Bob gets £60.", phase="substitute"),
    ],
}
g_prize = {
    "display": "Three friends share a prize in the ratio \\(2 : 5 : 8\\). The smallest share is £90. What is the total prize?",
    "solutions": [675], "calculator": False, "input_type": "single_value",
    "hint": "£90 is 2 parts. Find one part, then multiply by the total number of parts.",
    "misconceptions": [misc(1350,
        "The smallest share is 2 parts = £90, so one part = £45. Total = 15 × 45 = £675. Getting £1350 means £90 was treated as one part, giving 15 × 90.")],
    "guided_steps": [
        say("The £90 is the smallest share, worth 2 parts. Find one part first."),
        box("One part = 90 ÷ 2 = £", 45, "Divide the smallest share by its 2 parts.", done="One part is £45."),
        box("Total parts = 2 + 5 + 8 = ", 15, "Add all three ratio numbers."),
        box("15 × 45 = £", 675, "Multiply total parts by one part.", say="The whole prize is all 15 parts.", phase="substitute"),
        box("Check the smallest share: 2 × 45 = £", 90, "It should give the £90 stated.", done="2 × 45 = 90 matches, so the total is £675.", phase="substitute"),
    ],
}
g_model = {
    "display": "A model car is built to a scale of \\(1 : 18\\). The real car is 4.5 m long. What is the model length in cm?",
    "solutions": [25], "calculator": False, "input_type": "single_value",
    "hint": "Change 4.5 m to centimetres, then divide by 18.",
    "misconceptions": [misc(0.25,
        "Change 4.5 m to 450 cm first, then 450 ÷ 18 = 25 cm. Dividing 4.5 by 18 without converting gives 0.25, which is in metres, not centimetres.", "unit_error")],
    "guided_steps": [
        say("Scale 1 : 18 means the real car is 18 times the model. Work in the same units: centimetres."),
        box("Real length in cm: 4.5 m = ", 450, "There are 100 cm in 1 m, so multiply by 100.", done="The real car is 450 cm."),
        box("450 ÷ 18 = ", 25, "Divide the real length by 18.", say="The model is 18 times smaller.", phase="substitute"),
        box("Check by scaling up: 25 × 18 = ", 450, "It should return the real length in cm.", done="25 × 18 = 450 cm, so the model is 25 cm.", phase="substitute"),
    ],
}
g_oj = {
    "display": "Orange juice and water are mixed \\(2 : 5\\). 350 ml of water is used. How much orange juice is needed (in ml)?",
    "solutions": [140], "calculator": False, "input_type": "single_value",
    "hint": "The water is the 5 part. Find one part, then multiply by 2.",
    "misconceptions": [misc(875,
        "The 350 ml of water is the 5 part, so one part = 70 ml and orange = 2 × 70 = 140 ml. Getting 875 means 350 was divided by 2 and multiplied by 5, using the wrong parts.")],
    "guided_steps": [
        say("The 350 ml of water is the 5 part. Find one part first."),
        box("One part = 350 ÷ 5 = ", 70, "Divide the water by its ratio number.", done="One part is 70 ml."),
        box("2 × 70 = ", 140, "Multiply one part by 2.", say="Orange juice is the 2 part.", phase="substitute"),
        box("Check the ratio: 140 ÷ 70 = ", 2, "It should give the orange ratio number.", done="140 ÷ 70 = 2, matching the ratio, so 140 ml is right.", phase="substitute"),
    ],
}
g_concrete = {
    "display": "Concrete is mixed using cement, sand and gravel in the ratio \\(1 : 3 : 5\\). 360 kg of concrete is needed. How much sand is required (in kg)?",
    "solutions": [120], "calculator": False, "input_type": "single_value",
    "hint": "Add the parts, divide 360, then multiply by the sand ratio number.",
    "misconceptions": [misc(135,
        "Total parts = 1 + 3 + 5 = 9, so one part = 360 ÷ 9 = 40 and sand = 3 × 40 = 120 kg. Getting 135 means the parts were added as 8, giving 360 ÷ 8 = 45, then × 3.")],
    "guided_steps": [
        say("Here you know the total, so add the parts and find one part."),
        box("Total parts = 1 + 3 + 5 = ", 9, "Add all three ratio numbers."),
        box("One part = 360 ÷ 9 = ", 40, "Divide the total mass by the total parts.", done="One part is 40 kg."),
        box("3 × 40 = ", 120, "Multiply one part by 3.", say="Sand is the 3 part.", phase="substitute"),
        box("Check all parts total: (1 × 40) + 120 + (5 × 40) = ", 360, "They should add to 360 kg.", done="40 + 120 + 200 = 360, so sand is 120 kg.", phase="substitute"),
    ],
}
pb["gold"] = [g_alibob, g_prize, g_model, g_oj, g_concrete]

# ---------------------------------------------------------------- tier descriptions
pb["bronze_description"] = "Simplify a ratio, then share a total: add the parts, find one part, multiply."
pb["silver_description"] = "Work from one known quantity or a scale, using the unitary method and unit conversions."
pb["gold_description"] = "Reason from a difference or a single share to find the total or another share."

# ================================================================ tier_guides
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: simplify and share",
        "steps": [
            "A ratio like \\(3 : 2\\) splits something into equal parts. Simplify first where you can by dividing both parts by their highest common factor.",
            "To <strong>share a total</strong>: add the parts to get the number of shares, divide the total by that to find <strong>one part</strong>, then multiply one part by each ratio number.",
            "Always check: the shares should add back up to the original total.",
        ],
        "example": {
            "question": "Share £40 in the ratio 3 : 5",
            "steps": [
                {"label": "Add parts", "content": "<p>\\(3 + 5 = 8\\) parts</p>"},
                {"label": "One part", "content": "<p>\\(40 \\div 8 = £5\\)</p>"},
                {"label": "Shares", "content": "<p>\\(3 \\times 5 = £15\\) and \\(5 \\times 5 = £25\\)</p>"},
                {"label": "Check", "content": "<p>\\(15 + 25 = £40\\) ✔</p>"},
                {"label": "Answer", "content": "<p>\\(£15\\) and \\(£25\\)</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: scale from one known part",
        "steps": [
            "Sometimes you are given <strong>one quantity</strong>, not the total. Find what <strong>one part</strong> is worth by dividing that quantity by its ratio number.",
            "Then multiply one part by any other ratio number to get that share, or by the total parts to get the whole amount.",
            "Scale and map problems work the same way: multiply by the scale, then convert units carefully (100 cm in a metre, 100 000 cm in a kilometre).",
        ],
        "example": {
            "question": "The ratio of red to blue beads is 4 : 3. There are 20 red beads. How many blue?",
            "steps": [
                {"label": "One part", "content": "<p>\\(20 \\div 4 = 5\\) beads</p>"},
                {"label": "Blue", "content": "<p>\\(3 \\times 5 = 15\\) beads</p>"},
                {"label": "Check", "content": "<p>\\(15 \\div 5 = 3\\), matching the blue ratio part ✔</p>"},
                {"label": "Answer", "content": "<p>\\(15\\) blue beads</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: reason from a difference or one share",
        "steps": [
            "In gold problems the number given is a <strong>difference</strong> between shares, or a single share, or the total. Decide which before doing anything.",
            "For a difference, the parts differ too: divide the amount by the <strong>difference in parts</strong> to find one part. For one share, divide by that share's parts.",
            "Once one part is known, multiply to reach whatever the question asks, then check your answer fits the original wording.",
        ],
        "example": {
            "question": "Anna and Beth share money in the ratio 7 : 5. Anna gets £16 more than Beth. How much does Beth get?",
            "steps": [
                {"label": "Difference in parts", "content": "<p>\\(7 - 5 = 2\\) parts represent £16</p>"},
                {"label": "One part", "content": "<p>\\(16 \\div 2 = £8\\)</p>"},
                {"label": "Beth", "content": "<p>\\(5 \\times 8 = £40\\)</p>"},
                {"label": "Check", "content": "<p>Anna \\(7 \\times 8 = £56\\), and \\(56 - 40 = £16\\) ✔</p>"},
                {"label": "Answer", "content": "<p>\\(£40\\)</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ================================================================ guided (opener + teach)
pd["guided"] = {
    "opener": {
        "label": "Before any method",
        "display": "Maya and Leo share 10 sweets.<br>For every 2 sweets Maya takes, Leo takes 3.",
        "steps": [
            {"say": "A sharing puzzle. No method needed yet, just count.",
             "pre": "In one fair round Maya takes 2 and Leo takes 3. How many sweets is that altogether? ", "post": "",
             "answer": 5, "hint": "Just add 2 and 3."},
            {"say": "So the 10 sweets get handed out in equal rounds of 5.",
             "pre": "How many rounds of 5 are in 10 sweets? ", "post": "",
             "answer": 2, "hint": "How many 5s make 10?"},
            {"say": "Maya takes 2 sweets every round.",
             "pre": "Over 2 rounds Maya gets 2 × 2 = ", "post": "",
             "answer": 4, "hint": "2 sweets a round, for 2 rounds."},
            {"say": "You just shared in the ratio \\(2 : 3\\) with no algebra. Adding the parts (2 + 3 = 5), finding one round, then scaling up is the whole method. Maya gets 4, Leo gets 6, and \\(4 + 6 = 10\\)."},
        ],
    },
    "teach": {
        "bronze": {
            "display": "Share £60 in the ratio \\(3 : 1\\)",
            "label": "Together: your first share",
            "steps": [
                {"say": "Sharing has three moves: add the parts, find one part, then multiply. Watch.",
                 "pre": "Add the parts: 3 + 1 = ", "post": "", "answer": 4, "hint": "Add the two ratio numbers."},
                {"pre": "One part = 60 ÷ 4 = £", "post": "", "answer": 15, "hint": "Divide the money by the total parts.", "done": "One part is worth £15."},
                {"say": "Now scale each share up from one part.",
                 "pre": "Larger share: 3 × 15 = £", "post": "", "answer": 45, "hint": "Multiply one part by 3."},
                {"pre": "Smaller share: 1 × 15 = £", "post": "", "answer": 15, "hint": "Multiply one part by 1."},
                {"say": "Check they add back to the total.",
                 "pre": "45 + 15 = £", "post": "", "answer": 60, "hint": "The shares must total £60.", "done": "They add to £60, so add, divide, multiply is the whole method."},
            ],
        },
        "silver": {
            "display": "The ratio of blue to green counters is \\(2 : 7\\). There are 8 blue counters. How many green?",
            "label": "Together: the silver move",
            "steps": [
                {"say": "You are given one quantity, not the total. Find one part from it first.",
                 "pre": "Blue is the 2 part and equals 8, so one part = 8 ÷ 2 = ", "post": "", "answer": 4, "hint": "Divide the known quantity by its ratio number."},
                {"say": "Now every part is worth 4.",
                 "pre": "Green is the 7 part: 7 × 4 = ", "post": "", "answer": 28, "hint": "Multiply one part by 7.", "done": "Knowing one part unlocks every other quantity."},
                {"pre": "How many counters altogether? Parts = 2 + 7 = ", "post": "", "answer": 9, "hint": "Add the two ratio numbers."},
                {"pre": "Total counters = 9 × 4 = ", "post": "", "answer": 36, "hint": "Multiply total parts by one part."},
                {"say": "Check the two shares add to the total.",
                 "pre": "8 + 28 = ", "post": "", "answer": 36, "hint": "It should match the total.", "done": "8 + 28 = 36 matches, so one part = 4 was right."},
            ],
        },
        "gold": {
            "display": "Sara and Tom share money in the ratio \\(7 : 4\\). Sara gets £27 more than Tom. How much does Tom get?",
            "label": "Together: the gold move",
            "steps": [
                {"say": "The £27 is a difference, not a total. The parts differ too.",
                 "pre": "Difference in parts: 7 − 4 = ", "post": "", "answer": 3, "hint": "Subtract the smaller ratio number from the larger."},
                {"say": "That 3-part gap is worth the £27.",
                 "pre": "One part = 27 ÷ 3 = £", "post": "", "answer": 9, "hint": "Divide the money gap by the part gap.", "done": "The trick is spotting that £27 is a difference, not a total."},
                {"pre": "Tom has the 4 part: 4 × 9 = £", "post": "", "answer": 36, "hint": "Multiply one part by Tom's ratio number."},
                {"pre": "Sara has the 7 part: 7 × 9 = £", "post": "", "answer": 63, "hint": "Multiply one part by 7."},
                {"say": "Check the gap between them.",
                 "pre": "63 − 36 = £", "post": "", "answer": 27, "hint": "It should equal the £27 difference.", "done": "The gap is £27, so Tom gets £36."},
            ],
        },
    },
}

json.dump(pd, io.open("lesson_ratio-proportion-L01.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("written lesson_ratio-proportion-L01.json")
