# -*- coding: utf-8 -*-
"""Build guided-learning practice_data for number-L06 (Powers, Roots & Standard Form)."""
import json, io

SRC = "_fresh_number_L06.json"
OUT = "lesson_number-L06.json"

pd = json.load(io.open(SRC, encoding="utf-8"))


def box(pre, answer, hint, post="", **kw):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    d.update(kw)
    return d


def say(text):
    return {"say": text}


# ---------------------------------------------------------------- method_card
pd["method_card"]["title"] = "How to Use Powers, Roots and Standard Form"
pd["method_card"]["steps"] = [
    "For powers, multiply the base by itself the number of times shown by the index",
    "For roots, find the number that, raised to that power, gives the original",
    "For standard form, write as A × 10ⁿ with 1 ≤ A < 10",
    "Count the places the point moves for n (positive for large, negative for small)",
]
pd["method_card"]["content"] = (
    "<p><strong>Powers:</strong> \\(a^n\\) means \\(a\\) multiplied by itself \\(n\\) times, so "
    "\\(3^4 = 3 \\times 3 \\times 3 \\times 3 = 81\\). Note \\(a^0 = 1\\).</p>"
    "<p><strong>Roots</strong> undo powers: \\(\\sqrt{196} = 14\\) because \\(14^2 = 196\\), and "
    "\\(\\sqrt[3]{64} = 4\\) because \\(4^3 = 64\\).</p>"
    "<p><strong>Standard form</strong> is \\(A \\times 10^n\\) with \\(1 \\le A < 10\\). Slide the point "
    "until one digit is in front and count the places: large numbers give a positive \\(n\\), small "
    "numbers a negative \\(n\\).</p>"
    "<p><strong>Calculating:</strong> to multiply, multiply the fronts and add the powers; to divide, "
    "divide the fronts and subtract the powers. Adjust \\(A\\) back into range if needed.</p>"
)
# method_card.example preserved as-is (compact, single example).

# ---------------------------------------------------------------- tier_guides
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: powers, roots and writing standard form",
        "steps": [
            "A <strong>power</strong> like \\(3^4\\) means the base times itself: "
            "\\(3 \\times 3 \\times 3 \\times 3 = 81\\), not \\(3 \\times 4\\).",
            "A <strong>root</strong> undoes a power. \\(\\sqrt{196}\\) asks what squared makes 196 "
            "(that is 14), and \\(\\sqrt[3]{64}\\) asks what cubed makes 64 (that is 4).",
            "<strong>Standard form</strong> is \\(A \\times 10^n\\) with \\(1 \\le A < 10\\). Put one "
            "digit in front, count the places moved, then use a positive \\(n\\) for big numbers and a "
            "negative \\(n\\) for small ones.",
        ],
        "example": {
            "question": "Write 47 000 in standard form",
            "steps": [
                {"label": "Find A", "content": "Slide the point left to one digit in front: 4.7"},
                {"label": "Find n", "content": "47 000 to 4.7 is 4 places, and it is large, so n = 4"},
                {"label": "Check", "content": "Expand back: 4.7 × 10⁴ = 47 000"},
                {"label": "Answer", "content": "\\(4.7 \\times 10^4\\)", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: calculating and comparing in standard form",
        "steps": [
            "To <strong>multiply</strong>, multiply the fronts and ADD the powers. To "
            "<strong>divide</strong>, divide the fronts and SUBTRACT the powers.",
            "If the new front is not between 1 and 10, tidy it: \\(12 \\times 10^8 = 1.2 \\times 10^9\\), "
            "lifting the power by 1.",
            "To <strong>compare</strong>, the power decides first. A larger power always wins, so "
            "\\(3 \\times 10^4\\) beats \\(9 \\times 10^3\\).",
        ],
        "example": {
            "question": "Calculate (2 × 10⁵) × (4 × 10³) in standard form",
            "steps": [
                {"label": "Fronts", "content": "2 × 4 = 8"},
                {"label": "Powers", "content": "Add: 5 + 3 = 8"},
                {"label": "Check", "content": "A = 8 is between 1 and 10, so no adjusting"},
                {"label": "Answer", "content": "\\(8 \\times 10^8\\)", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: negative powers, adding, and fixing standard form",
        "steps": [
            "Negative powers mean small numbers: \\(5 \\times 10^{-2} = 0.05\\). Keep the signs when you "
            "add or subtract powers.",
            "To <strong>add</strong>, first rewrite both numbers with the SAME power, then add the fronts.",
            "Always finish by checking \\(A\\) is between 1 and 10. If \\(0.36 \\times 10^5\\) is not, "
            "adjust it to \\(3.6 \\times 10^4\\).",
        ],
        "example": {
            "question": "Calculate (4 × 10⁶) + (8 × 10⁵) in standard form",
            "steps": [
                {"label": "Match powers", "content": "8 × 10⁵ = 0.8 × 10⁶"},
                {"label": "Add fronts", "content": "4 + 0.8 = 4.8"},
                {"label": "Check", "content": "4.8 is in range, so the power stays 10⁶"},
                {"label": "Answer", "content": "\\(4.8 \\times 10^6\\)", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---------------------------------------------------------------- guided (opener + teach)
pd["guided"] = {
    "opener": {
        "steps": [
            say("A giant lottery jackpot is £2 000 000. Writing all those zeros is slow and easy to "
                "miscount. Mathematicians have a shortcut: count the zeros, then write it as a power of 10."),
            box("How many zeros are in £2 000 000? ", 6, "Count them one by one: there are 6.", post=""),
            say("So £2 000 000 is a 2 followed by 6 zeros, written \\(2 \\times 10^6\\). The little 6 just "
                "records how many zeros. That is <strong>standard form</strong>: a number between 1 and 10, "
                "times 10 to the power of how many places."),
            box("A tech company is worth £9 000 000 000. How many zeros is that? ", 9,
                "Count the zeros after the 9: there are 9.", post=""),
            say("So £9 000 000 000 = \\(9 \\times 10^9\\). You just wrote nine billion pounds with two "
                "symbols instead of ten digits. Standard form always looks like \\(A \\times 10^n\\), where "
                "\\(A\\) sits between 1 and 10 and \\(n\\) counts the places."),
        ],
    },
    "teach": {
        "bronze": {
            "display": "Write \\(8\\,400\\,000\\) in standard form",
            "steps": [
                say("Write 8 400 000 in standard form, which looks like \\(A \\times 10^n\\) with A between "
                    "1 and 10."),
                box("Slide the point left until one digit is in front. A = ", 8.4,
                    "One digit before the point: 8.4."),
                box("Count how many places the point moved: ", 6, "8 400 000 to 8.4 is 6 places left."),
                say("It is a large number, so the power is positive."),
                box("Write the power: n = ", 6, "Same as the places moved, positive for a big number.",
                    done="That fixes the power at 6."),
                box("Check by expanding: 8.4 × 1 000 000 = ", 8400000, "Move the point 6 places right.",
                    done="Back to 8 400 000, so \\(8.4 \\times 10^6\\) is right."),
            ],
        },
        "silver": {
            "display": "Calculate \\((5 \\times 10^3) \\times (4 \\times 10^6)\\). Give your answer in standard form.",
            "steps": [
                say("Calculate \\((5 \\times 10^3) \\times (4 \\times 10^6)\\) in standard form. Do the "
                    "fronts and the powers separately."),
                box("Multiply the fronts: 5 × 4 = ", 20, "Five fours."),
                box("ADD the powers: 3 + 6 = ", 9, "Add the powers when multiplying."),
                say("That gives 20 × 10⁹, but A = 20 is not between 1 and 10, so adjust."),
                box("Write 20 as 2 × 10, so the tidy A = ", 2, "20 = 2 × 10.", done="A is now in range."),
                box("Moving one 10 into the power lifts it by 1: 9 + 1 = ", 10, "Nine plus one.",
                    done="So the answer is \\(2 \\times 10^{10}\\)."),
            ],
        },
        "gold": {
            "display": "Calculate \\((3.2 \\times 10^5) + (6 \\times 10^4)\\). Give your answer in standard form.",
            "steps": [
                say("Calculate \\((3.2 \\times 10^5) + (6 \\times 10^4)\\) in standard form. You cannot add "
                    "the fronts until the powers match."),
                box("Rewrite 6 × 10⁴ to a power of 10⁵. Drop the front to a tenth: 6 becomes ", 0.6,
                    "6 × 10⁴ = 0.6 × 10⁵."),
                box("Now both are × 10⁵. Add the fronts: 3.2 + 0.6 = ", 3.8, "3.2 plus 0.6.",
                    done="A = 3.8 is in range."),
                box("The power is unchanged: n = ", 5, "Both terms are × 10⁵."),
                box("Check by expanding: 320 000 + 60 000 = ", 380000, "Add the two ordinary numbers.",
                    done="380 000 = 3.8 × 10⁵, so it checks out."),
            ],
        },
    },
}

# ---------------------------------------------------------------- descriptions
pb = pd["problem_bank"]
pb["bronze_description"] = "Recall single powers and roots, and write one number in standard form."
pb["silver_description"] = "Multiply, divide and compare numbers written in standard form."
pb["gold_description"] = "Work with negative powers, addition, real-world contexts and correcting standard form."

# ---------------------------------------------------------------- per-problem content
# Each entry: hint, misconceptions, guided_steps. Some also change display/solutions/input_type.

BRONZE = {
 0: dict(  # 3^4 = 81  (COMPLETION problem)
   hint="Multiply 3 by itself four times: 3 × 3 × 3 × 3.",
   misconceptions=[
     {"pattern": "multiply_by_index", "check": "equals_12", "expect": 12,
      "message": "\\(3^4\\) means 3 × 3 × 3 × 3 = 81, not 3 × 4 = 12."},
     {"pattern": "arithmetic", "check": "wrong", "expect": None,
      "message": "Build it up: 3 × 3 = 9, × 3 = 27, × 3 = 81."},
   ],
   guided_steps=[
     say("\\(3^4\\) means four 3s multiplied together: 3 × 3 × 3 × 3. Build it up one multiply at a time."),
     box("3 × 3 = ", 9, "Three times three is nine."),
     box("Times another 3: 9 × 3 = ", 27, "Nine threes make 27."),
     box("One more 3: 27 × 3 = ", 81, "27 times 3 is the last of the four 3s.", phase="substitute"),
     box("Check a different way. \\(3^4 = 9^2\\), so 9 × 9 = ", 81, "Nine squared is 81.",
         done="Both routes land on 81, so \\(3^4 = 81\\)."),
   ],
 ),
 1: dict(  # sqrt196 = 14
   hint="Find the number that, squared, gives 196. It is between 10 and 15.",
   misconceptions=[
     {"pattern": "halve", "check": "equals_98", "expect": 98,
      "message": "Square root does not mean halve. 14 × 14 = 196, so \\(\\sqrt{196} = 14\\)."},
     {"pattern": "close_guess", "check": "equals_13", "expect": 13,
      "message": "13² = 169, which is too small. Try 14: 14 × 14 = 196, so the root is 14."},
   ],
   guided_steps=[
     say("\\(\\sqrt{196}\\) asks what number, times itself, makes 196. It lies between "
         "\\(\\sqrt{100} = 10\\) and \\(\\sqrt{225} = 15\\), and 196 ends in 6, so 14 is the strong candidate."),
     box("Test 14 by squaring. In parts: 14 × 10 = ", 140, "Ten lots of 14."),
     box("14 × 4 = ", 56, "Four lots of 14.", phase="substitute"),
     box("Add the parts: 140 + 56 = ", 196, "140 plus 56."),
     box("That is 196, the number under the root, so \\(\\sqrt{196}\\) = ", 14, "The number we squared.",
         done="14 × 14 = 196, so \\(\\sqrt{196} = 14\\)."),
   ],
 ),
 2: dict(  # cbrt64 = 4
   hint="Find the number that, cubed, gives 64.",
   misconceptions=[
     {"pattern": "square_not_cube", "check": "equals_8", "expect": 8,
      "message": "That is \\(\\sqrt{64} = 8\\), the square root. The cube root asks what number cubed makes "
                 "64: 4 × 4 × 4 = 64, so \\(\\sqrt[3]{64} = 4\\)."},
     {"pattern": "divide_by_3", "check": "wrong", "expect": None,
      "message": "Cube root does not mean divide by 3. Find the number that cubes to 64: it is 4."},
   ],
   guided_steps=[
     say("\\(\\sqrt[3]{64}\\) asks what number cubed (times itself three times) makes 64."),
     box("Try 4. First 4 × 4 = ", 16, "Four fours."),
     box("Now × 4 again: 16 × 4 = ", 64, "Sixteen times four.", phase="substitute"),
     box("That equals 64, so the cube root is ", 4, "The number we cubed.",
         done="4 × 4 × 4 = 64, so \\(\\sqrt[3]{64} = 4\\)."),
   ],
 ),
 3: dict(  # 56000 -> [5.6, 4]
   hint="Put one digit in front (5.6), then count how many places you moved.",
   misconceptions=[
     {"pattern": "wrong_A", "check": "equals_56", "expect": [56, 3],
      "message": "A must be between 1 and 10. 56 is too big, so slide one more place: 5.6 × 10⁴."},
     {"pattern": "wrong_power", "check": "wrong", "expect": [5.6, 3],
      "message": "A = 5.6 is right. Now count the moves: 56 000 back to 5.6 is 4 places left, and large "
                 "numbers take a positive power, so n = 4."},
   ],
   guided_steps=[
     say("Standard form is \\(A \\times 10^n\\) with A between 1 and 10. Start with A."),
     box("Slide the point left until one digit sits in front. A = ", 5.6,
         "One non-zero digit before the point: 5.6."),
     box("Count how many places the point moved from 56 000 to 5.6: ", 4, "5, 6, 0, 0: four hops left."),
     box("It is a large number, so n is positive. n = ", 4,
         "Same as the places moved, positive for a big number.", phase="substitute"),
     box("Check by expanding: 5.6 × 10 000 = ", 56000, "Move the point 4 places right.",
         done="Back to 56 000, so \\(5.6 \\times 10^4\\) is right."),
   ],
 ),
 4: dict(  # 0.0023 -> [2.3, -3]
   hint="Move to one digit in front (2.3); a small number gives a negative power.",
   misconceptions=[
     {"pattern": "positive_power", "check": "equals_3", "expect": [2.3, 3],
      "message": "Small numbers have negative powers. 0.0023 = 2.3 × 10⁻³, so n = −3, not 3."},
     {"pattern": "count_wrong", "check": "wrong", "expect": None,
      "message": "Move the point 3 places right to reach 2.3. It is a small number, so n = −3."},
   ],
   guided_steps=[
     say("Standard form is \\(A \\times 10^n\\). Find A first, then the power."),
     box("Slide the point right until one non-zero digit is in front: 0.0023 becomes ", 2.3,
         "First non-zero digit is 2, so A = 2.3."),
     box("Count the places the point moved right: ", 3, "0.0023 to 2.3 is 3 hops right."),
     box("It is a small number (less than 1), so n is negative. n = ", -3,
         "Three places right means n = −3.", phase="substitute"),
     box("Check by expanding: 2.3 × 0.001 = ", 0.0023, "Move the point 3 places left.",
         done="Back to 0.0023, so \\(2.3 \\times 10^{-3}\\) is right."),
   ],
 ),
 5: dict(  # 5^3 = 125
   hint="Multiply 5 by itself three times: 5 × 5 × 5.",
   misconceptions=[
     {"pattern": "multiply_by_index", "check": "equals_15", "expect": 15,
      "message": "\\(5^3\\) means 5 × 5 × 5 = 125, not 5 × 3 = 15."},
     {"pattern": "square_not_cube", "check": "equals_25", "expect": 25,
      "message": "That is 5² = 25. For 5³, multiply once more: 25 × 5 = 125."},
   ],
   guided_steps=[
     say("\\(5^3\\) means three 5s multiplied: 5 × 5 × 5."),
     box("First 5 × 5 = ", 25, "Five fives."),
     box("Now × 5 again: 25 × 5 = ", 125, "Twenty-five times five.", phase="substitute"),
     box("Check the count: how many 5s did we multiply? ", 3, "The little 3 in \\(5^3\\).",
         done="Three 5s multiplied make 125, so \\(5^3 = 125\\)."),
   ],
 ),
 6: dict(  # 10^0 = 1
   hint="Any non-zero number to the power 0 is 1.",
   misconceptions=[
     {"pattern": "zero_answer", "check": "equals_0", "expect": 0,
      "message": "Any non-zero number to the power 0 equals 1, not 0. \\(10^0 = 1\\)."},
     {"pattern": "base_answer", "check": "equals_10", "expect": 10,
      "message": "\\(10^0 = 1\\), not 10. The zero power always gives 1."},
   ],
   guided_steps=[
     say("Any non-zero number to the power 0 equals 1. Here is why, using a pattern of dividing by 10."),
     box("\\(10^3 = 1000\\). Divide by 10 for \\(10^2\\): 1000 ÷ 10 = ", 100, "One thousand divided by ten."),
     box("Again for \\(10^1\\): 100 ÷ 10 = ", 10, "One hundred divided by ten."),
     box("Once more for \\(10^0\\): 10 ÷ 10 = ", 1, "Ten divided by ten.", phase="substitute"),
     box("Each step dropped the power by 1 and divided by 10, so \\(10^0\\) must be ", 1,
         "The result of 10 ÷ 10.", done="The pattern forces \\(10^0 = 1\\)."),
   ],
 ),
 7: dict(  # sqrt225 = 15
   hint="Find the number that, squared, gives 225.",
   misconceptions=[
     {"pattern": "halve", "check": "equals_112.5", "expect": 112.5,
      "message": "Square root does not mean halve. 15 × 15 = 225, so \\(\\sqrt{225} = 15\\)."},
     {"pattern": "arithmetic", "check": "wrong", "expect": None,
      "message": "Find the number that squares to 225. Try 15: 15 × 15 = 225."},
   ],
   guided_steps=[
     say("\\(\\sqrt{225}\\) asks what number squared makes 225. It sits between \\(\\sqrt{196} = 14\\) and "
         "\\(\\sqrt{256} = 16\\), and 225 ends in 5, so try 15."),
     box("Test 15 by squaring. In parts: 15 × 10 = ", 150, "Ten lots of 15."),
     box("15 × 5 = ", 75, "Five lots of 15.", phase="substitute"),
     box("Add: 150 + 75 = ", 225, "150 plus 75."),
     box("That is 225, so \\(\\sqrt{225}\\) = ", 15, "The number we squared.",
         done="15 × 15 = 225, so \\(\\sqrt{225} = 15\\)."),
   ],
 ),
}

SILVER = {
 0: dict(  # 7.1e5 -> 710000  (COMPLETION problem)
   hint="Positive power means move the point right; count the places.",
   misconceptions=[
     {"pattern": "wrong_direction", "check": "wrong", "expect": 7.1e-05,
      "message": "A positive power moves the point RIGHT, making the number bigger: 7.1 becomes 710 000."},
     {"pattern": "wrong_places", "check": "wrong", "expect": None,
      "message": "Move the point 5 places right, filling with zeros: 710 000."},
   ],
   guided_steps=[
     say("\\(7.1 \\times 10^5\\) means 7.1 with the point moved 5 places to the right. Work out where the "
         "digits land."),
     box("The power is positive, so we move right. How many places? ", 5, "The power is 5."),
     box("Start at 7.1 and move the point 1 place right: ", 71, "7.1 to 71 is one place."),
     box("Four more places to go, each filled with a zero. After all 5 places the number is ", 710000,
         "71 then four zeros: 710 000.", phase="substitute"),
     box("Check by counting the digits after the leading 7 in 710 000: ", 5, "1, 0, 0, 0, 0: five digits.",
         done="Five places moved, so \\(7.1 \\times 10^5 = 710\\,000\\)."),
   ],
 ),
 1: dict(  # (4e3)*(3e5) -> [1.2, 9]
   hint="Multiply the fronts, add the powers, then adjust A into range.",
   misconceptions=[
     {"pattern": "multiply_powers", "check": "equals_16", "expect": [1.2, 16],
      "message": "When multiplying, ADD the powers: 3 + 5 = 8, do not multiply them to 15. With 4 × 3 = 12 "
                 "adjusted to 1.2 × 10, the answer is 1.2 × 10⁹."},
     {"pattern": "no_adjust", "check": "equals_8", "expect": [12, 8],
      "message": "4 × 3 = 12. Since 12 > 10, adjust: 1.2 × 10⁹. The power becomes 9."},
   ],
   guided_steps=[
     say("Multiplying in standard form: handle the front numbers and the powers separately."),
     box("Multiply the fronts: 4 × 3 = ", 12, "Four threes."),
     box("For multiplying, ADD the powers: 3 + 5 = ", 8, "Add, do not multiply, the powers."),
     say("So far that is 12 × 10⁸, but A = 12 is not between 1 and 10. Adjust it."),
     box("Write 12 as 1.2 × 10, so the tidy A = ", 1.2, "12 = 1.2 × 10.", phase="substitute"),
     box("Moving one 10 into the power lifts it by 1: 8 + 1 = ", 9, "Eight plus one.",
         done="\\(1.2 \\times 10^9\\), with A in range and the power adjusted."),
     say("Check the size: \\(10^3 \\times 10^5 = 10^8\\), and the 12 adds one more ten, giving "
         "\\(10^9\\). The front 1.2 is between 1 and 10, so \\(1.2 \\times 10^9\\) is correct."),
   ],
 ),
 2: dict(  # 0.000061 -> [6.1, -5]
   hint="One digit in front (6.1); a small number gives a negative power.",
   misconceptions=[
     {"pattern": "wrong_A", "check": "equals_61", "expect": [61, -6],
      "message": "A must be between 1 and 10. 0.000061 = 6.1 × 10⁻⁵, so A = 6.1, not 61."},
     {"pattern": "wrong_count", "check": "wrong", "expect": None,
      "message": "Move the point 5 places right to reach 6.1, so n = −5."},
   ],
   guided_steps=[
     say("Standard form \\(A \\times 10^n\\): find A, then the power."),
     box("Slide the point right to the first non-zero digit: 0.000061 becomes ", 6.1,
         "First non-zero digit is 6, so A = 6.1."),
     box("Count the places the point moved right: ", 5, "0.000061 to 6.1 is 5 hops right."),
     box("It is a small number, so n is negative. n = ", -5, "Five places right means n = −5.",
         phase="substitute"),
     box("Check by expanding: 6.1 × 0.00001 = ", 0.000061, "Move the point 5 places left.",
         done="Back to 0.000061, so \\(6.1 \\times 10^{-5}\\) is right."),
   ],
 ),
 3: dict(  # (9e7)/(3e4) -> [3, 3]
   hint="Divide the fronts, subtract the powers.",
   misconceptions=[
     {"pattern": "add_powers", "check": "equals_11", "expect": [3, 11],
      "message": "For division, SUBTRACT the powers: 7 − 4 = 3, do not add them to 11. And 9 ÷ 3 = 3, so "
                 "3 × 10³."},
     {"pattern": "arithmetic", "check": "wrong", "expect": None,
      "message": "Subtract the powers for division: 7 − 4 = 3, and 9 ÷ 3 = 3."},
   ],
   guided_steps=[
     say("Dividing in standard form: handle the fronts and the powers separately."),
     box("Divide the fronts: 9 ÷ 3 = ", 3, "Nine divided by three."),
     box("For dividing, SUBTRACT the powers: 7 − 4 = ", 3, "Subtract, not add, the powers."),
     say("That gives 3 × 10³. A = 3 is already between 1 and 10, so no adjusting."),
     box("Write the power: n = ", 3, "The subtracted power, 7 − 4.", phase="substitute"),
     box("Check by expanding: 3 × 10³ = ", 3000, "3 followed by 3 zeros.",
         done="90 000 000 ÷ 30 000 = 3000, so \\(3 \\times 10^3\\) is right."),
   ],
 ),
 4: dict(  # CHANGED: cbrt1000 -> cbrt729 = 9
   display="Calculate \\(\\sqrt[3]{729}\\)",
   solutions=[9],
   input_type="single_value",
   hint="Find the number that, cubed, gives 729. Try 9.",
   misconceptions=[
     {"pattern": "square_not_cube", "check": "equals_27", "expect": 27,
      "message": "That is \\(\\sqrt{729} = 27\\), the square root. The cube root asks what number cubed "
                 "makes 729: 9 × 9 × 9 = 729, so \\(\\sqrt[3]{729} = 9\\)."},
     {"pattern": "divide_by_3", "check": "equals_243", "expect": 243,
      "message": "Cube root does not mean divide by 3. 729 ÷ 3 = 243, but 243 cubed is far bigger than 729. "
                 "The number that cubes to 729 is 9."},
   ],
   guided_steps=[
     say("\\(\\sqrt[3]{729}\\) asks what number cubed makes 729. Nearby cubes are \\(8^3 = 512\\) and "
         "\\(10^3 = 1000\\), so try 9."),
     box("Test 9. First 9 × 9 = ", 81, "Nine nines."),
     box("Now × 9 again: 81 × 9 = ", 729, "Eighty-one times nine.", phase="substitute"),
     box("That equals 729, so the cube root is ", 9, "The number we cubed.",
         done="9 × 9 × 9 = 729, so \\(\\sqrt[3]{729} = 9\\)."),
   ],
 ),
 5: dict(  # compare 3e4 vs 9e3 -> 30000  (drop inert compare_n_only)
   hint="Turn each into an ordinary number, then compare.",
   misconceptions=[
     {"pattern": "compare_A_only", "check": "equals_9000", "expect": 9000,
      "message": "Do not just compare the front numbers. 3 × 10⁴ = 30 000 and 9 × 10³ = 9 000, so 30 000 is "
                 "larger even though 3 is less than 9."},
   ],
   guided_steps=[
     say("Compare by turning each into an ordinary number, then pick the bigger."),
     box("Expand the first: 3 × 10⁴ = ", 30000, "3 followed by 4 zeros."),
     box("Expand the second: 9 × 10³ = ", 9000, "9 followed by 3 zeros."),
     box("Which is bigger, 30 000 or 9 000? Enter the larger value: ", 30000, "30 000 beats 9 000.",
         phase="substitute"),
     box("Check the shortcut: the bigger power wins. Of the powers 4 and 3, the larger is ", 4,
         "4 is greater than 3.",
         done="\\(10^4 > 10^3\\), so \\(3 \\times 10^4 = 30\\,000\\) is larger. The power decides."),
   ],
 ),
 6: dict(  # CHANGED: 2^6 -> Write 2^10 in standard form -> [1.024, 3]
   display="Write \\(2^{10}\\) in standard form",
   solutions=[1.024, 3],
   input_type="standard_form",
   hint="Work out 2¹⁰ = 1024 first, then write 1024 in standard form.",
   misconceptions=[
     {"pattern": "not_converted", "check": "equals_1024", "expect": [1024, 0],
      "message": "1024 is the right value, but standard form needs A between 1 and 10. Slide the point "
                 "3 places: 1.024 × 10³."},
     {"pattern": "wrong_A", "check": "wrong", "expect": [10.24, 2],
      "message": "10.24 is still too big for A. Move the point one more place: 1.024 × 10³."},
   ],
   guided_steps=[
     say("Two jobs here: work out \\(2^{10}\\), then write it in standard form."),
     box("\\(2^{10}\\) is a well-known power. Build from \\(2^5 = 32\\): 32 × 32 = ", 1024,
         "\\(2^{10} = 2^5 \\times 2^5 = 32 \\times 32 = 1024\\)."),
     box("Now standard form. Slide the point left to one digit in front: 1024 becomes A = ", 1.024,
         "One digit before the point: 1.024."),
     box("Count the places moved from 1024 to 1.024: n = ", 3, "Three hops left, and it is large so positive.",
         phase="substitute"),
     box("Check by expanding: 1.024 × 1000 = ", 1024, "Move the point 3 places right.",
         done="Back to 1024 = \\(2^{10}\\), so \\(1.024 \\times 10^3\\) is right."),
   ],
 ),
}

GOLD = {
 0: dict(  # (6e4)*(5e-2) -> [3, 3]  (COMPLETION problem)
   hint="Multiply the fronts, add the powers (keep the minus sign), then adjust A.",
   misconceptions=[
     {"pattern": "no_adjust", "check": "equals_30", "expect": [30, 2],
      "message": "6 × 5 = 30 and 4 + (−2) = 2, giving 30 × 10². But 30 > 10, so adjust: 3 × 10³."},
     {"pattern": "wrong_power_add", "check": "wrong", "expect": None,
      "message": "Add the powers with their signs: 4 + (−2) = 2. Then 30 × 10² = 3 × 10³."},
   ],
   guided_steps=[
     say("Multiplying in standard form, with a negative power in the mix. Fronts and powers separately."),
     box("Multiply the fronts: 6 × 5 = ", 30, "Six fives."),
     box("ADD the powers, keeping the signs: 4 + (−2) = ", 2, "4 plus negative 2 is 2."),
     say("That gives 30 × 10². A = 30 is not between 1 and 10, so adjust."),
     box("Write 30 as 3 × 10, so the tidy A = ", 3, "30 = 3 × 10.", phase="substitute"),
     box("Moving one 10 into the power lifts it by 1: 2 + 1 = ", 3, "Two plus one."),
     box("Check by expanding: 3 × 10³ = ", 3000, "3 followed by 3 zeros.",
         done="60 000 × 0.05 = 3000, so \\(3 \\times 10^3\\) is right."),
   ],
 ),
 1: dict(  # (2.4e6)+(5e5) -> [2.9, 6]
   hint="Match the powers first, then add the fronts.",
   misconceptions=[
     {"pattern": "add_directly", "check": "equals_7.4", "expect": [7.4, 6],
      "message": "You cannot add the fronts directly. The powers must match first: 5 × 10⁵ = 0.5 × 10⁶, "
                 "then 2.4 + 0.5 = 2.9 × 10⁶."},
     {"pattern": "wrong_power", "check": "wrong", "expect": None,
      "message": "Rewrite 5 × 10⁵ = 0.5 × 10⁶, then 2.4 + 0.5 = 2.9. Answer: 2.9 × 10⁶."},
   ],
   guided_steps=[
     say("Adding in standard form: the powers must match before you add the fronts."),
     box("Rewrite 5 × 10⁵ as a power of 10⁶. Drop the front to a tenth: 5 becomes ", 0.5,
         "5 × 10⁵ = 0.5 × 10⁶."),
     box("Now both are × 10⁶. Add the fronts: 2.4 + 0.5 = ", 2.9, "2.4 plus 0.5.", phase="substitute"),
     box("A = 2.9 is in range, so the power is unchanged. n = ", 6, "Both terms are × 10⁶."),
     box("Check by expanding: 2 400 000 + 500 000 = ", 2900000, "Add the two ordinary numbers.",
         done="2 900 000 = 2.9 × 10⁶, so the answer is right."),
   ],
 ),
 2: dict(  # light: 3e8 * 5e2 -> [1.5, 11]
   hint="Distance = speed × time: multiply the fronts and add the powers.",
   misconceptions=[
     {"pattern": "subtract_powers", "check": "wrong", "expect": [1.5, 7],
      "message": "For multiplication, ADD the powers: 8 + 2 = 10. Then 3 × 5 = 15, so 15 × 10¹⁰ = "
                 "1.5 × 10¹¹. Power = 11."},
     {"pattern": "no_adjust", "check": "equals_10", "expect": [15, 10],
      "message": "3 × 5 = 15, which is > 10. Adjust: 1.5 × 10¹¹. Power = 11."},
   ],
   guided_steps=[
     say("Distance = speed × time. Multiply the fronts and add the powers."),
     box("Multiply the fronts: 3 × 5 = ", 15, "Three fives."),
     box("ADD the powers: 8 + 2 = ", 10, "Add the powers when multiplying."),
     say("That gives 15 × 10¹⁰. A = 15 is too big, so adjust."),
     box("Write 15 as 1.5 × 10, so the tidy A = ", 1.5, "15 = 1.5 × 10.", phase="substitute"),
     box("Lift the power by 1: 10 + 1 = ", 11, "Ten plus one.",
         done="\\(1.5 \\times 10^{11}\\) metres, A in range and the power adjusted."),
     say("Check the size: \\(10^8 \\times 10^2 = 10^{10}\\), and the 15 adds one more ten, giving "
         "\\(10^{11}\\). The front 1.5 is in range, so \\(1.5 \\times 10^{11}\\) m is correct."),
   ],
 ),
 3: dict(  # 0.36e5 -> [3.6, 4]
   hint="A must be between 1 and 10; adjust A and the power together.",
   misconceptions=[
     {"pattern": "already_standard", "check": "equals_0.36", "expect": [0.36, 5],
      "message": "0.36 is not between 1 and 10. Multiply it by 10 to get 3.6, and drop the power to 10⁴: "
                 "3.6 × 10⁴."},
     {"pattern": "wrong_direction", "check": "wrong", "expect": [3.6, 6],
      "message": "0.36 × 10 = 3.6, so A grew by 10. To keep the value, the power must DROP by 1: 10⁴, not 10⁶."},
   ],
   guided_steps=[
     say("\\(0.36 \\times 10^5\\) is not proper standard form because A must be between 1 and 10. Fix A, "
         "then fix the power."),
     box("0.36 is too small. Multiply it by 10 to get into range: 0.36 × 10 = ", 3.6, "0.36 × 10 = 3.6."),
     say("We multiplied A by 10, so to keep the value the same the power part must drop by 1."),
     box("The power falls from 5 to ", 4, "5 − 1 = 4.", phase="substitute"),
     box("Check by expanding: 3.6 × 10⁴ = ", 36000, "3.6 followed by the zeros: 36 000.",
         done="\\(0.36 \\times 10^5 = 36\\,000\\) too, so \\(3.6 \\times 10^4\\) is right."),
   ],
 ),
 4: dict(  # bacteria doubling -> [8, 4]
   hint="Doubling 4 times means multiplying by 2⁴ = 16.",
   misconceptions=[
     {"pattern": "add_not_multiply", "check": "wrong", "expect": None,
      "message": "Doubling means × 2 each time, not adding. After 4 hours: 5000 × 2⁴ = 5000 × 16 = 80 000 = "
                 "8 × 10⁴."},
     {"pattern": "wrong_double", "check": "equals_4", "expect": [4, 4],
      "message": "Doubling 4 times is × 2⁴ = × 16, not × 8. 5000 × 16 = 80 000 = 8 × 10⁴."},
   ],
   guided_steps=[
     say("Doubling every hour for 4 hours means multiplying by 2 four times, that is × 2⁴."),
     box("Work out 2⁴: 2 × 2 × 2 × 2 = ", 16, "2, 4, 8, 16."),
     box("Write the start as an ordinary number: 5 × 10³ = ", 5000, "5 followed by 3 zeros."),
     box("Multiply: 5000 × 16 = ", 80000, "5000 × 16 = 80 000.", phase="substitute"),
     box("Standard form A: slide 80 000 to one digit in front. A = ", 8, "8 with the point after it, so A = 8."),
     box("Count the places moved, giving the power n = ", 4, "80 000 to 8 is 4 places, so n = 4.",
         done="80 000 = 8 × 10⁴, so after 4 hours there are \\(8 \\times 10^4\\) bacteria."),
   ],
 ),
}


def apply(tier_list, edits):
    for i, e in edits.items():
        p = tier_list[i]
        if "display" in e:
            p["display"] = e["display"]
        if "solutions" in e:
            p["solutions"] = e["solutions"]
        if "input_type" in e:
            p["input_type"] = e["input_type"]
        p["hint"] = e["hint"]
        p["misconceptions"] = e["misconceptions"]
        p["guided_steps"] = e["guided_steps"]


apply(pb["bronze"], BRONZE)
apply(pb["silver"], SILVER)
apply(pb["gold"], GOLD)

# Strip em dashes from preserved worked_examples labels (hard style rule / validator).
for we in pd.get("worked_examples", []):
    for st in we.get("steps", []):
        if "label" in st and isinstance(st["label"], str):
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

json.dump(pd, io.open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT)
