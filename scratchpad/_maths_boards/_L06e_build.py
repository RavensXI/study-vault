# -*- coding: utf-8 -*-
import json, io

live = json.load(io.open("_L06e_live.json", encoding="utf-8"))

# ---- Preserve untouched fields ----
method_card = live["method_card"]          # already slim (4 steps, ~85 words)
topic_links = live.get("topic_links", {"prerequisites": []})
related_videos = live.get("related_videos", [])
worked_examples = live["worked_examples"]   # byte-for-byte

def P(display, solutions, calculator, input_type, hint, misconceptions, guided_steps):
    return {
        "display": display, "solutions": solutions, "calculator": calculator,
        "input_type": input_type, "hint": hint,
        "misconceptions": misconceptions, "guided_steps": guided_steps,
    }

def say(s): return {"say": s}
def box(pre, answer, hint, done=None, phase=None):
    d = {"pre": pre, "answer": answer, "hint": hint}
    if phase: d["phase"] = phase
    if done: d["done"] = done
    return d

bronze = [
 # 0: 3^4 = 81
 P("\\(3^4\\)", [81], False, "single_value",
   "A power means repeated multiplying, so multiply four 3s together.",
   [{"pattern":"multiply_base","expect":12,
     "message":"12 comes from 3 × 4. A power means repeated multiplying, so 3⁴ = 3 × 3 × 3 × 3 = 81."}],
   [say("A power counts how many of the same number are multiplied. \\(3^4\\) means four 3s."),
    box("Start with the first two: 3 × 3 =", 9, "3 × 3 = 9."),
    box("Multiply by the third 3: 9 × 3 =", 27, "9 × 3 = 27.", phase="substitute"),
    box("Multiply by the fourth 3: 27 × 3 =", 81, "27 × 3 = 81.", done="3⁴ = 81.")]),
 # 1: 2^6 = 64
 P("\\(2^6\\)", [64], False, "single_value",
   "Multiply 2 by itself six times, one factor at a time.",
   [{"pattern":"multiply_base","expect":12,
     "message":"12 comes from 2 × 6. A power multiplies repeatedly, so 2⁶ = 2 × 2 × 2 × 2 × 2 × 2 = 64."}],
   [say("\\(2^6\\) means six 2s multiplied together."),
    box("First three 2s: 2 × 2 × 2 =", 8, "2 × 2 × 2 = 8."),
    box("That is 2³. Multiply by the fourth 2: 8 × 2 =", 16, "8 × 2 = 16.", phase="substitute"),
    box("Multiply by the fifth 2: 16 × 2 =", 32, "16 × 2 = 32."),
    box("Multiply by the sixth 2: 32 × 2 =", 64, "32 × 2 = 64.", done="2⁶ = 64.")]),
 # 2: sqrt(144) = 12
 P("\\(\\sqrt{144}\\)", [12], False, "single_value",
   "Ask what number times itself gives 144.",
   [{"pattern":"halved","expect":72,
     "message":"72 halves 144. A square root asks what number times itself gives 144, and 12 × 12 = 144."}],
   [say("A square root reverses squaring: it asks what number times itself gives 144."),
    box("Try 11 × 11 =", 121, "11 × 11 = 121, a little too small."),
    box("Try the next one: 12 × 12 =", 144, "12 × 12 = 144.", phase="substitute"),
    box("12 lands on 144, so write \\(\\sqrt{144}\\).", 12, "It is 12.", done="√144 = 12, since 12² = 144.")]),
 # 3: cbrt(27) = 3
 P("\\(\\sqrt[3]{27}\\)", [3], False, "single_value",
   "Ask what number multiplied by itself three times gives 27.",
   [{"pattern":"divide_by_three","expect":9,
     "message":"9 divides 27 by 3. A cube root asks what number cubed gives 27, and 3 × 3 × 3 = 27."}],
   [say("A cube root asks what number times itself three times gives 27."),
    box("Try 2 × 2 × 2 =", 8, "2³ = 8, too small."),
    box("Try 3 × 3 × 3 =", 27, "3³ = 27.", phase="substitute"),
    box("3 cubed lands on 27, so write \\(\\sqrt[3]{27}\\).", 3, "It is 3.", done="³√27 = 3.")]),
 # 4: Write 34000 in standard form. Give A. -> 3.4
 P("Write \\(34\\,000\\) in standard form. Give \\(A\\).", [3.4], False, "single_value",
   "Place the decimal point after the first digit to get A between 1 and 10.",
   [{"pattern":"front_not_below_10","expect":34,
     "message":"34 is not between 1 and 10. Standard form needs a single digit before the point: 34000 = 3.4 × 10⁴, so A = 3.4."}],
   [say("Standard form is \\(A \\times 10^n\\) with A between 1 and 10. This question wants A."),
    box("Read the first non-zero digit of 34000.", 3, "The first digit is 3."),
    box("Place the point just after that first digit. Enter the front number A.", 3.4, "34000 becomes 3.4.", phase="substitute"),
    box("Check A sits between 1 and 10, then re-enter it.", 3.4, "A = 3.4.", done="34000 = 3.4 × 10⁴, so A = 3.4.")]),
 # 5: 7.2 x 10^3 as ordinary -> 7200
 P("Write \\(7.2 \\times 10^3\\) as an ordinary number.", [7200], False, "single_value",
   "A positive power makes the number bigger, so move the decimal point right.",
   [{"pattern":"wrong_direction","expect":0.0072,
     "message":"0.0072 moves the point the wrong way. A positive power makes the number bigger, so move 3 places right: 7200."}],
   [say("A power of 3 means move the decimal point 3 places. A positive power makes it bigger, so move right."),
    box("First place right: 7.2 × 10 =", 72, "7.2 × 10 = 72."),
    box("Second place: 72 × 10 =", 720, "72 × 10 = 720.", phase="substitute"),
    box("Third place: 720 × 10 =", 7200, "720 × 10 = 7200.", done="7.2 × 10³ = 7200.")]),
 # 6: 5^3 = 125
 P("\\(5^3\\)", [125], False, "single_value",
   "Cubing means multiplying the number by itself three times.",
   [{"pattern":"multiply_base","expect":15,
     "message":"15 comes from 5 × 3. A power means repeated multiplying, so 5³ = 5 × 5 × 5 = 125."}],
   [say("A power counts how many of the same number are multiplied. \\(5^3\\) means three 5s."),
    box("Start with the first two: 5 × 5 =", 25, "5 × 5 = 25."),
    box("Now multiply by the third 5: 25 × 5 =", 125, "25 × 5 = 125.", phase="substitute"),
    box("Confirm the three factors: 5 × 5 × 5 =", 125, "It comes to 125.", done="5³ = 125.")]),
 # 7: 10^0 = 1
 P("\\(10^0\\)", [1], False, "single_value",
   "Any non-zero number to the power 0 equals 1.",
   [{"pattern":"power_zero_is_zero","expect":0,
     "message":"0 assumes a power of 0 gives nothing, but any non-zero number to the power 0 is 1."},
    {"pattern":"keeps_base","expect":10,
     "message":"10 keeps the base, but a power of 0 gives 1, not the number itself."}],
   [say("Powers of 10 drop by dividing by 10 each step: \\(10^2=100\\), \\(10^1=10\\). Watch the pattern."),
    box("10² = 100. Divide by 10 to reach 10¹: 100 ÷ 10 =", 10, "100 ÷ 10 = 10."),
    box("Divide again to reach 10⁰: 10 ÷ 10 =", 1, "10 ÷ 10 = 1.", phase="substitute"),
    box("So 10⁰ equals:", 1, "It is 1.", done="10⁰ = 1, and any non-zero number to the power 0 is 1.")]),
]

silver = [
 # 0: 0.0045 -> [4.5,-3]
 P("Write \\(0.0045\\) in standard form.", [4.5,-3], False, "standard_form",
   "The number is below 1, so move the point right and the power is negative.",
   [{"pattern":"positive_power","expect":[4.5,3],
     "message":"4.5 × 10³ has the sign wrong. Numbers below 1 take a negative power: 0.0045 = 4.5 × 10⁻³."},
    {"pattern":"count_zeros","expect":[4.5,-2],
     "message":"4.5 × 10⁻² counts only the two leading zeros. Count every place the point moves to reach 4.5: that is 3 places, so 4.5 × 10⁻³."}],
   [say("Standard form needs A between 1 and 10, times a power of 10. Find A, then the power."),
    box("Place the point after the first non-zero digit of 0.0045 to get A.", 4.5, "0.0045 becomes 4.5."),
    box("Count how many places the point moved from 0.0045 to 4.5.", 3, "It moved 3 places right.", phase="substitute"),
    box("The number is below 1, so the power is negative. Enter the power.", -3, "The power is −3.", done="0.0045 = 4.5 × 10⁻³.")]),
 # 1: 5600000 -> [5.6,6]
 P("Write \\(5\\,600\\,000\\) in standard form.", [5.6,6], False, "standard_form",
   "Place the point after the first digit, then count the places to the end.",
   [{"pattern":"count_zeros","expect":[5.6,5],
     "message":"5.6 × 10⁵ counts only the five zeros. Count every place the point moves: 5600000 to 5.6 is 6 places, so 5.6 × 10⁶."}],
   [say("A is between 1 and 10. Move the point to sit after the first digit, then count the places."),
    box("Place the point after the first digit of 5600000 to get A.", 5.6, "5600000 becomes 5.6."),
    box("Count how many places the point moved from 5600000 to 5.6.", 6, "5600000, 560000, 56000, 5600, 560, 56, 5.6 is 6 moves.", phase="substitute"),
    box("The number is above 1, so the power is positive. Enter the power.", 6, "The power is 6.", done="5600000 = 5.6 × 10⁶.")]),
 # 2: (4e3)(3e5) -> [1.2,9]
 P("Calculate \\((4 \\times 10^3) \\times (3 \\times 10^5)\\). Give your answer in standard form.", [1.2,9], False, "standard_form",
   "Multiply the fronts, add the powers, then adjust if the front reaches 10.",
   [{"pattern":"no_adjust","expect":[12,8],
     "message":"12 × 10⁸ is right but not in standard form: A must be below 10. Move one place: 1.2 × 10⁹."}],
   [say("For a product in standard form: multiply the fronts, add the powers, then fix the front if needed."),
    box("Multiply the fronts: 4 × 3 =", 12, "4 × 3 = 12."),
    box("Add the powers: 3 + 5 =", 8, "3 + 5 = 8."),
    box("That is 12 × 10⁸, but A must be below 10. Write 12 as 1.2 × 10, so the new A is:", 1.2, "12 becomes 1.2.", phase="substitute"),
    box("Moving 12 down to 1.2 adds 1 to the power: 8 + 1 =", 9, "8 + 1 = 9.", done="1.2 × 10⁹. Check: 4000 × 300000 = 1.2 × 10⁹.")]),
 # 3: (8e7)/(2e3) -> [4,4]
 P("Calculate \\((8 \\times 10^7) \\div (2 \\times 10^3)\\). Give your answer in standard form.", [4,4], False, "standard_form",
   "Divide the front numbers and subtract the powers.",
   [{"pattern":"added_powers","expect":[4,10],
     "message":"Adding the powers gives 4 × 10¹⁰. Division subtracts them: 7 − 3 = 4, so 4 × 10⁴."}],
   [say("For a quotient in standard form: divide the fronts and subtract the powers."),
    box("Divide the fronts: 8 ÷ 2 =", 4, "8 ÷ 2 = 4."),
    box("Subtract the powers: 7 − 3 =", 4, "7 − 3 = 4.", phase="substitute"),
    box("Check with ordinary numbers: 80000000 ÷ 2000 =", 40000, "80000000 ÷ 2000 = 40000.", done="40000 = 4 × 10⁴, so A = 4 and the power is 4.")]),
 # 4: 2.8e-4 as ordinary -> 0.00028
 P("Write \\(2.8 \\times 10^{-4}\\) as an ordinary number.", [0.00028], False, "single_value",
   "A negative power makes the number smaller, so move the decimal point left.",
   [{"pattern":"wrong_direction","expect":28000,
     "message":"28000 moves the point right. A negative power makes the number smaller, so move 4 places left: 0.00028."}],
   [say("A negative power means move the decimal point left, making the number smaller. Here that is 4 places."),
    box("First place left: 2.8 ÷ 10 =", 0.28, "2.8 ÷ 10 = 0.28."),
    box("Second place: 0.28 ÷ 10 =", 0.028, "0.28 ÷ 10 = 0.028.", phase="substitute"),
    box("Third place: 0.028 ÷ 10 =", 0.0028, "0.028 ÷ 10 = 0.0028."),
    box("Fourth place: 0.0028 ÷ 10 =", 0.00028, "0.0028 ÷ 10 = 0.00028.", done="2.8 × 10⁻⁴ = 0.00028.")]),
 # 5: 4^-2 -> fraction [1,16]
 P("\\(4^{-2}\\)", [1,16], False, "fraction",
   "A negative power means one over the positive power.",
   [{"pattern":"multiply_base","expect":[1,8],
     "message":"1/8 comes from 4 × 2 in the denominator. A power multiplies repeatedly: 4⁻² = 1 ÷ (4 × 4) = 1/16."},
    {"pattern":"forgot_reciprocal","expect":[16,1],
     "message":"16 is 4², but the negative index means one over that: 4⁻² = 1/16."}],
   [say("A negative power flips the number: \\(4^{-2}\\) means one over \\(4^2\\)."),
    box("Work out the positive power first: 4 × 4 =", 16, "4 × 4 = 16."),
    box("So 4⁻² = 1/16. The numerator (top) of the fraction is:", 1, "The top is 1.", phase="substitute"),
    box("The denominator (bottom) is 4 squared:", 16, "The bottom is 16.", done="4⁻² = 1/16.")]),
 # 6: 0.000072 -> [7.2,-5]
 P("Write \\(0.000\\,072\\) in standard form.", [7.2,-5], False, "standard_form",
   "Move the point right to just after the 7, and count the places for a negative power.",
   [{"pattern":"positive_power","expect":[7.2,5],
     "message":"7.2 × 10⁵ has the sign wrong. Numbers below 1 take a negative power: 0.000072 = 7.2 × 10⁻⁵."},
    {"pattern":"count_zeros","expect":[7.2,-4],
     "message":"7.2 × 10⁻⁴ counts only the four leading zeros. Count every place the point moves to reach 7.2: that is 5 places, so 7.2 × 10⁻⁵."}],
   [say("A is between 1 and 10. Move the point to sit after the first non-zero digit, then count."),
    box("Place the point after the first non-zero digit (7) of 0.000072 to get A.", 7.2, "0.000072 becomes 7.2."),
    box("Count how many places the point moved from 0.000072 to 7.2.", 5, "It moved 5 places right.", phase="substitute"),
    box("The number is below 1, so the power is negative. Enter the power.", -5, "The power is −5.", done="0.000072 = 7.2 × 10⁻⁵.")]),
]

gold = [
 # 0: (3e4)^2 -> [9,8]
 P("Calculate \\((3 \\times 10^4)^2\\). Give your answer in standard form.", [9,8], False, "standard_form",
   "Square the front and double the power.",
   [{"pattern":"doubled_not_squared","expect":[6,8],
     "message":"6 doubles the front instead of squaring it. Squaring means 3 × 3 = 9, so 9 × 10⁸."},
    {"pattern":"added_to_power","expect":[9,6],
     "message":"9 × 10⁶ adds 2 to the power, but squaring a power multiplies it: 4 × 2 = 8, so 9 × 10⁸."}],
   [say("Squaring \\((3 \\times 10^4)^2\\) squares the front and multiplies the power by 2."),
    box("Square the front: 3 × 3 =", 9, "3 × 3 = 9."),
    box("Square the power part: (10⁴)² multiplies the power by 2, so 4 × 2 =", 8, "4 × 2 = 8.", phase="substitute"),
    box("9 is already below 10, so no adjusting. Enter the power to finish 9 × 10 to the n.", 8, "The power is 8.", done="9 × 10⁸. Check: 30000² = 900000000 = 9 × 10⁸.")]),
 # 1: (2.4e5)+(3.6e4) -> [2.76,5] calc True
 P("Calculate \\((2.4 \\times 10^5) + (3.6 \\times 10^4)\\). Give your answer in standard form.", [2.76,5], True, "standard_form",
   "The powers differ, so write both as ordinary numbers and add.",
   [{"pattern":"added_fronts","expect":[6,5],
     "message":"Adding the fronts gives 6 × 10⁵, but the powers differ so you cannot add directly. Line them up: 240000 + 36000 = 276000 = 2.76 × 10⁵."}],
   [say("You can only add standard-form numbers directly when the powers match. Here they differ, so expand first."),
    box("Write the first as an ordinary number: 2.4 × 10⁵ =", 240000, "2.4 × 10⁵ = 240000."),
    box("Write the second: 3.6 × 10⁴ =", 36000, "3.6 × 10⁴ = 36000."),
    box("Add them: 240000 + 36000 =", 276000, "240000 + 36000 = 276000."),
    box("Write 276000 in standard form. Enter A, a number below 10.", 2.76, "276000 becomes 2.76.", phase="substitute"),
    box("Count the places from 276000 back to 2.76 for the power.", 5, "It moved 5 places.", done="2.76 × 10⁵. Check: 2.76 × 100000 = 276000.")]),
 # 2: (6e8)/(1.5e-2) -> [4,10]
 P("Calculate \\(\\dfrac{6 \\times 10^8}{1.5 \\times 10^{-2}}\\). Standard form.", [4,10], False, "standard_form",
   "Divide the fronts and subtract the powers, minding the double negative.",
   [{"pattern":"sign_on_power","expect":[4,6],
     "message":"4 × 10⁶ forgets the minus on the second power. Subtracting −2 adds: 8 − (−2) = 10, so 4 × 10¹⁰."}],
   [say("Divide the fronts and subtract the powers. Watch the second power: it is negative."),
    box("Divide the fronts: 6 ÷ 1.5 =", 4, "6 ÷ 1.5 = 4."),
    box("Subtract the powers. Subtracting a negative adds: 8 − (−2) = 8 + 2 =", 10, "8 + 2 = 10.", phase="substitute"),
    box("4 is already below 10, so no adjusting. Enter the power to finish 4 × 10 to the n.", 10, "The power is 10.", done="4 × 10¹⁰. Check: 600000000 ÷ 0.015 = 4 × 10¹⁰.")]),
 # 3: star distance -> 5000 years, calc True
 P("A star is \\(4.5 \\times 10^{12}\\) km away. Light travels \\(9 \\times 10^{8}\\) km per year. How many years to reach us?", [5000], True, "single_value",
   "Number of years is the distance divided by the distance light covers each year.",
   [{"pattern":"divided_wrong_way","expect":0.0002,
     "message":"0.0002 divides the wrong way round. Years is distance ÷ speed: 4.5 × 10¹² ÷ 9 × 10⁸ = 5000."},
    {"pattern":"front_only","expect":0.5,
     "message":"0.5 is only the front numbers divided; you still need the powers: 0.5 × 10⁴ = 5000."}],
   [say("Number of years is the distance divided by how far light travels each year, so divide."),
    box("Divide the fronts: 4.5 ÷ 9 =", 0.5, "4.5 ÷ 9 = 0.5."),
    box("Subtract the powers: 12 − 8 =", 4, "12 − 8 = 4.", phase="substitute"),
    box("So far that is 0.5 × 10⁴. Write it as an ordinary number: 0.5 × 10000 =", 5000, "0.5 × 10000 = 5000.", done="5000 years. Check: 5000 × 9 × 10⁸ = 4.5 × 10¹².")]),
 # 4: (2e3)^3/(4e5) -> [2,4]
 P("Simplify \\(\\dfrac{(2 \\times 10^3)^3}{4 \\times 10^5}\\). Standard form.", [2,4], False, "standard_form",
   "Cube the top first, then divide the fronts and subtract the powers.",
   [{"pattern":"multiplied_not_cubed","expect":[1.5,4],
     "message":"1.5 × 10⁴ comes from 2 × 3 instead of cubing: 2³ = 2 × 2 × 2 = 8, giving 8 × 10⁹ ÷ 4 × 10⁵ = 2 × 10⁴."},
    {"pattern":"power_not_cubed","expect":[2,-2],
     "message":"2 × 10⁻² leaves the top power as 3, but cubing multiplies it: 3 × 3 = 9, giving 8 × 10⁹ ÷ 4 × 10⁵ = 2 × 10⁴."}],
   [say("Cube the top bracket first: cube the front and multiply its power by 3. Then divide."),
    box("Cube the front of the top: 2 × 2 × 2 =", 8, "2³ = 8."),
    box("Cube its power: (10³)³ multiplies the power by 3, so 3 × 3 =", 9, "3 × 3 = 9."),
    box("So the top is 8 × 10⁹. Divide the fronts: 8 ÷ 4 =", 2, "8 ÷ 4 = 2.", phase="substitute"),
    box("Subtract the powers: 9 − 5 =", 4, "9 − 5 = 4.", done="2 × 10⁴. Check: 8000000000 ÷ 400000 = 20000 = 2 × 10⁴.")]),
]

problem_bank = {
 "bronze": bronze, "silver": silver, "gold": gold,
 "bronze_description": "Work out powers and square or cube roots, and convert between ordinary numbers and standard form.",
 "silver_description": "Write numbers in standard form, multiply and divide in standard form, and handle negative indices.",
 "gold_description": "Square standard-form numbers, add them, and solve real-life problems, adjusting the front back below 10.",
}

# ---- guided.opener (fresh: distance to the Sun, 150,000,000 km) ----
opener_svg = (
 '<div style="text-align:center">'
 '<svg viewBox="0 0 250 78" role="img" aria-label="The number 150,000,000 with its seven trailing zeros highlighted, showing seven zeros make ten to the power seven">'
 '<text x="125" y="16" font-family="Inter, sans-serif" font-size="11" fill="currentColor" text-anchor="middle">Distance to the Sun (km)</text>'
 '<rect x="96" y="30" width="96" height="30" rx="4" fill="#60a5fa" fill-opacity="0.3"/>'
 '<text x="125" y="51" font-family="Inter, sans-serif" font-size="18" fill="currentColor" text-anchor="middle" letter-spacing="2">150000000</text>'
 '<text x="144" y="72" font-family="Inter, sans-serif" font-size="10" fill="currentColor" text-anchor="middle">7 zeros = ×10⁷</text>'
 '</svg></div>'
)
opener = {
 "label": "Before any powers",
 "display": opener_svg +
   "The Sun is about <strong>150,000,000 km</strong> away. Writing all those zeros is slow and easy to slip on, "
   "so scientists pack them into a power of 10.<br>The highlighted part is the seven trailing zeros.",
 "steps": [
   box("How many zeros are on the end of 150,000,000?", 7, "After the 15 there are seven 0s."),
   box("Each zero is one ×10. Seven zeros multiplied is 10 to the power of what?", 7, "Seven 10s multiplied is 10⁷."),
   say("Those seven zeros are exactly \\(10^7\\), so \\(150{,}000{,}000 = 15 \\times 10^7\\). Tidy the front to a single "
       "digit and it becomes <strong>\\(1.5 \\times 10^8\\)</strong>. That is <strong>standard form</strong>: one digit "
       "before the point, times a power of 10, where the power counts how far the point moved. Big numbers get positive "
       "powers, tiny numbers get negative ones."),
 ],
}

teach = {
 "bronze": {
   "display": "Write 63000 in standard form.",
   "label": "Together: your first one",
   "steps": [
     say("Standard form is \\(A \\times 10^n\\) with A between 1 and 10. Find A first."),
     box("Place the point after the first digit of 63000 to get the front A.", 6.3, "63000 becomes 6.3."),
     box("Count how many places the point moved from 63000 to 6.3.", 4, "63000, 6300, 630, 63, 6.3 is 4 moves."),
     box("The number is above 1, so the power is positive. Write the power.", 4, "The power is 4."),
     box("Check by expanding: 6.3 × 10000 =", 63000, "6.3 × 10000 = 63000.", done="63000 = 6.3 × 10⁴. That was the whole point."),
   ],
 },
 "silver": {
   "display": "Calculate \\((6 \\times 10^2) \\times (5 \\times 10^4)\\). Give your answer in standard form.",
   "label": "Together: the silver move",
   "steps": [
     say("Multiply the fronts, add the powers, then adjust the front if it reaches 10."),
     box("Multiply the fronts: 6 × 5 =", 30, "6 × 5 = 30."),
     box("Add the powers: 2 + 4 =", 6, "2 + 4 = 6."),
     box("30 is not below 10. Write it as 3 × 10, so the new front A is:", 3, "30 becomes 3."),
     box("Adjusting 30 to 3 adds 1 to the power: 6 + 1 =", 7, "6 + 1 = 7.", done="3 × 10⁷. Check: 600 × 50000 = 30000000 = 3 × 10⁷."),
   ],
 },
 "gold": {
   "display": "Calculate \\((6.3 \\times 10^4) \\div (9 \\times 10^{-3})\\). Give your answer in standard form.",
   "label": "Together: the gold move",
   "steps": [
     say("Divide the fronts, subtract the powers, then adjust, even when the front comes out below 1."),
     box("Divide the fronts: 6.3 ÷ 9 =", 0.7, "6.3 ÷ 9 = 0.7."),
     box("Subtract the powers. Subtracting a negative adds: 4 − (−3) = 4 + 3 =", 7, "4 + 3 = 7."),
     box("0.7 is below 1, so it is not standard form. Write 0.7 as 7 × 10⁻¹, giving new A:", 7, "0.7 becomes 7."),
     box("Moving 0.7 up to 7 takes 1 off the power: 7 − 1 =", 6, "7 − 1 = 6.", done="7 × 10⁶. Check: 63000 ÷ 0.009 = 7000000 = 7 × 10⁶."),
   ],
 },
}

guided = {"opener": opener, "teach": teach}

def ex(label, content, ans=False):
    d = {"label": label, "content": content}
    if ans:
        d["isAnswer"] = True; d["is_answer"] = True
    return d

tier_guides = {
 "bronze": {
   "title": "Bronze: Powers, roots and writing standard form",
   "steps": [
     "A <strong>power</strong> is repeated multiplying: \\(3^4 = 3 \\times 3 \\times 3 \\times 3\\). A <strong>square root</strong> undoes squaring, a <strong>cube root</strong> undoes cubing.",
     "<strong>Standard form</strong> is \\(A \\times 10^n\\) with A between 1 and 10. Move the point to sit after the first digit and count the places.",
     "Big numbers (above 1) get a positive power; small numbers (below 1) get a negative power.",
   ],
   "example": {
     "question": "Write 4200 in standard form",
     "steps": [
       ex("Front", "Point after the first digit: 4.2"),
       ex("Count", "4200 to 4.2 is 3 places, and 4200 is above 1."),
       ex("Check", "4.2 × 1000 = 4200."),
       ex("Answer", "\\(4.2 \\times 10^3\\)", ans=True),
     ],
   },
 },
 "silver": {
   "title": "Silver: Multiplying and dividing in standard form",
   "steps": [
     "<strong>Multiply:</strong> multiply the fronts and <strong>add</strong> the powers. <strong>Divide:</strong> divide the fronts and <strong>subtract</strong> the powers.",
     "Then <strong>adjust</strong>: if the front reaches 10 or more, move it below 10 and add 1 to the power.",
     "A <strong>negative index</strong> means one over the positive power: \\(4^{-2} = \\frac{1}{4^2} = \\frac{1}{16}\\).",
   ],
   "example": {
     "question": "Calculate (5 × 10³) × (4 × 10⁴)",
     "steps": [
       ex("Fronts", "5 × 4 = 20"),
       ex("Powers", "3 + 4 = 7, giving 20 × 10⁷"),
       ex("Adjust", "20 = 2 × 10, so add 1 to the power."),
       ex("Answer", "\\(2 \\times 10^8\\)", ans=True),
     ],
   },
 },
 "gold": {
   "title": "Gold: Adjusting, adding and real contexts",
   "steps": [
     "After multiplying or dividing, always <strong>adjust</strong> the front back between 1 and 10. A front below 1 (like 0.7) means take 1 off the power.",
     "To <strong>add or subtract</strong>, the powers must match. If they differ, write both as ordinary numbers, combine, then rewrite in standard form.",
     "In word problems, pick the operation first (years is distance ÷ speed), then work the fronts and powers.",
   ],
   "example": {
     "question": "Calculate (6.4 × 10⁵) ÷ (8 × 10⁻²)",
     "steps": [
       ex("Fronts", "6.4 ÷ 8 = 0.8"),
       ex("Powers", "5 − (−2) = 7, giving 0.8 × 10⁷"),
       ex("Adjust", "0.8 is below 1, so 8 × 10⁻¹ × 10⁷ = 8 × 10⁶."),
       ex("Answer", "\\(8 \\times 10^6\\)", ans=True),
     ],
   },
 },
}

pd = {
 "method_card": method_card,
 "topic_links": topic_links,
 "problem_bank": problem_bank,
 "related_videos": related_videos,
 "worked_examples": worked_examples,
 "tier_guides": tier_guides,
 "guided": guided,
}

with open("lesson_maths-eduqas_number-L06.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)

# word-budget report for tier_guides
def words(s): return len([w for w in s.replace("\\("," ").replace("\\)"," ").split() if w])
for tier in ("bronze","silver","gold"):
    tot = sum(words(s) for s in tier_guides[tier]["steps"])
    print(tier, "tier_guide steps words:", tot)
print("method_card content words:", words(method_card["content"]))
print("wrote lesson_maths-eduqas_number-L06.json")
