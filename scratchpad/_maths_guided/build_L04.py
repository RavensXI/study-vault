# -*- coding: utf-8 -*-
import json, io

live = json.load(io.open("_live_L04.json", encoding="utf-8"))

# ---- preserved (byte-for-byte, except mandatory em-dash style fix in labels) ----
related_videos = live["related_videos"]
topic_links = live["topic_links"]
worked_examples = json.loads(json.dumps(live["worked_examples"]))
for we in worked_examples:
    for st in we.get("steps", []):
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ")

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def sy(say):
    return {"say": say}

# =========================== BRONZE ===========================
bronze = [
 {  # B0 mean of 5,8,3,10,4 = 6
  "display": "Find the mean of: 5, 8, 3, 10, 4",
  "solutions": [6], "calculator": False, "input_type": "single_value",
  "hint": "Add all five numbers, then divide by 5.",
  "misconceptions": [
    {"pattern": "forgot_to_divide", "expect": 30,
     "message": "30 is the total. The mean also needs you to divide by how many numbers there are: 30 ÷ 5 = 6.",
     "note": "error: gave the sum, skipped dividing"}],
  "guided_steps": [
    sy("The mean is add-them-all-up, then divide by how many."),
    box("5 + 8 + 3 + 10 + 4 = ", 30, "Add left to right: 5 and 8 is 13, plus 3 is 16, plus 10 is 26, plus 4."),
    box("How many numbers are there? ", 5, "Count them."),
    box("30 ÷ 5 = ", 6, "How many 5s make 30?", say="Now divide the total by how many:", phase="substitute"),
    box("6 × 5 = ", 30, "Multiply the mean by how many numbers.", say="Check by multiplying back:", done="Back to the total 30, so the mean of 6 is right.", phase="substitute")]},
 {  # B1 median of 2,5,8,11,14 = 8
  "display": "Find the median of: 2, 5, 8, 11, 14",
  "solutions": [8], "calculator": False, "input_type": "single_value",
  "hint": "Put them in order and take the middle value.",
  "misconceptions": [],
  "guided_steps": [
    sy("The median is the middle value once the numbers are in order. This list is already in order."),
    box("How many numbers are in the list? ", 5, "Count them."),
    box("The middle position is (5 + 1) ÷ 2 = ", 3, "Add one, then halve: (5 + 1) ÷ 2.", post="rd value"),
    box("Count along: the 3rd value is ", 8, "2 is 1st, 5 is 2nd, so the 3rd is next.", say="Now read off that position:", phase="substitute"),
    box("How many numbers are below 8? ", 2, "Count the values smaller than 8.", say="Check: the median should have equal counts either side.", done="Two below (2, 5) and two above (11, 14), so 8 is the median.", phase="substitute")]},
 {  # B2 mode of 3,5,5,7,8,5,9 = 5
  "display": "Find the mode of: 3, 5, 5, 7, 8, 5, 9",
  "solutions": [5], "calculator": False, "input_type": "single_value",
  "hint": "Find the value that appears most often.",
  "misconceptions": [
    {"pattern": "frequency_not_value", "expect": 3,
     "message": "3 is how many times 5 appears, its frequency. The mode is the value that repeats, which is 5.",
     "note": "error: gave the count of appearances, not the value"}],
  "guided_steps": [
    sy("The mode is the value that appears most often. Tally how many times each number shows up."),
    box("How many times does 5 appear? ", 3, "Scan the list and count the 5s."),
    box("How many times does 3 appear? ", 1, "Count the 3s."),
    box("The value that repeats most is ", 5, "The value with the highest count.", say="5 appears more than any other value:", done="5 appears 3 times, more than any other, so it is the mode.", phase="substitute"),
    box("The next most common values each appear how many times? ", 1, "3, 7, 8 and 9 each appear how many times?", say="Check nothing beats three appearances:", done="Every other value appears just once, so 5 is clearly the mode.", phase="substitute")]},
 {  # B3 range of 4,9,2,15,7 = 13
  "display": "Find the range of: 4, 9, 2, 15, 7",
  "solutions": [13], "calculator": False, "input_type": "single_value",
  "hint": "Subtract the smallest value from the largest.",
  "misconceptions": [
    {"pattern": "added_not_subtracted", "expect": 17,
     "message": "Range is largest minus smallest, not plus. 15 + 2 = 17 is the trap; the answer is 15 − 2 = 13.",
     "note": "error: added the two ends"}],
  "guided_steps": [
    sy("Range measures spread: largest minus smallest. Find each end first."),
    box("Largest value = ", 15, "Scan for the biggest number."),
    box("Smallest value = ", 2, "Scan for the smallest number."),
    box("15 − 2 = ", 13, "Subtract the smallest from the largest.", say="Range is largest minus smallest:", done="Range 13.", phase="substitute"),
    box("2 + 13 = ", 15, "Add the range to the smallest.", say="Check: adding the range back to the smallest should reach the largest.", done="Back to 15, the largest, so the range 13 is right.", phase="substitute")]},
 {  # B4 median of 3,6,8,12 = 7
  "display": "Find the median of: 3, 6, 8, 12 (even number of values)",
  "solutions": [7], "calculator": False, "input_type": "single_value",
  "hint": "Average the two middle numbers.",
  "misconceptions": [
    {"pattern": "picked_one_middle", "expect": 6,
     "message": "With an even count there are two middle values, 6 and 8. Do not pick just 6; average them: (6 + 8) ÷ 2 = 7.",
     "note": "error: took the lower of the two middles"}],
  "guided_steps": [
    sy("An even number of values has two middle numbers. The list is already ordered, so find the middle pair."),
    box("How many numbers are there? ", 4, "Count them."),
    box("The two middle values are 6 and ", 8, "The 2nd and 3rd of four values."),
    box("(6 + 8) ÷ 2 = ", 7, "Add them and halve.", say="The median is halfway between the two middle values:", done="Median 7.", phase="substitute"),
    box("8 − 7 = ", 1, "Subtract 7 from 8.", say="Check: 7 should sit exactly between 6 and 8.", done="7 is 1 away from both 6 and 8, so it is the midpoint, the median.", phase="substitute")]},
 {  # B5 total: mean 8 of 5 numbers = 40
  "display": "The mean of 5 numbers is 8. Find the total.",
  "solutions": [40], "calculator": False, "input_type": "single_value",
  "hint": "Multiply the mean by how many numbers there are.",
  "misconceptions": [
    {"pattern": "divided_not_multiplied", "expect": 1.6,
     "message": "To turn a mean back into a total you multiply: 8 × 5 = 40. Dividing (8 ÷ 5 = 1.6) goes the wrong way.",
     "note": "error: divided instead of multiplying"}],
  "guided_steps": [
    sy("The mean is the total shared equally. To go backwards from the mean to the total, multiply."),
    box("The mean is 8 and there are how many numbers? ", 5, "Read it from the question."),
    box("8 × 5 = ", 40, "Multiply the mean by the count.", say="Total = mean × how many:", done="Total 40.", phase="substitute"),
    box("40 ÷ 5 = ", 8, "Divide the total by 5.", say="Check: sharing 40 between 5 should give the mean back.", done="Back to the mean of 8, so the total 40 is right.", phase="substitute")]},
 {  # B6 mean of 12,15,18,20,25 = 18
  "display": "Find the mean of: 12, 15, 18, 20, 25",
  "solutions": [18], "calculator": False, "input_type": "single_value",
  "hint": "Add all five numbers, then divide by 5.",
  "misconceptions": [
    {"pattern": "forgot_to_divide", "expect": 90,
     "message": "90 is the total. Divide by how many numbers there are, 5: 90 ÷ 5 = 18.",
     "note": "error: gave the sum, skipped dividing"}],
  "guided_steps": [
    sy("Mean: add them all, then divide by how many."),
    box("12 + 15 + 18 + 20 + 25 = ", 90, "Add in pairs: 12 + 18 = 30, 15 + 25 = 40, then add 20."),
    box("How many numbers? ", 5, "Count them."),
    box("90 ÷ 5 = ", 18, "How many 5s make 90?", say="Divide the total by how many:", done="Mean 18.", phase="substitute"),
    box("18 × 5 = ", 90, "Mean times count.", say="Check by multiplying back:", done="Back to the total 90, so the mean 18 is right.", phase="substitute")]},
 {  # B7 range of -3,5,-1,7,2 = 10
  "display": "Find the range of: −3, 5, −1, 7, 2",
  "solutions": [10], "calculator": False, "input_type": "single_value",
  "hint": "Largest minus smallest, and subtracting a negative adds.",
  "misconceptions": [
    {"pattern": "sign_error", "expect": 4,
     "message": "The smallest value is −3. Range = 7 − (−3) = 7 + 3 = 10. Writing 7 − 3 = 4 drops the double negative.",
     "note": "error: ignored the minus on the smallest"}],
  "guided_steps": [
    sy("Range = largest minus smallest. Take care with the negative numbers."),
    box("Largest value = ", 7, "The biggest number."),
    box("Smallest value = ", -3, "The most negative number is the smallest."),
    box("7 − (−3) = 7 + 3 = ", 10, "Two minuses make a plus.", say="Range is largest minus smallest. Subtracting a negative adds:", done="Range 10.", phase="substitute"),
    box("−3 + 10 = ", 7, "Add the range to the smallest.", say="Check: adding the range to the smallest should reach the largest.", done="Back to 7, the largest, so the range 10 is right.", phase="substitute")]},
]

# =========================== SILVER ===========================
silver = [
 {  # S0 freq table mean = 2.45
  "display": "Frequency table: x = 1(f=4), 2(f=7), 3(f=5), 4(f=4). Find the mean.",
  "solutions": [2.45], "calculator": True, "input_type": "single_value",
  "hint": "Work out fx for each row, add them, then divide by the total frequency.",
  "misconceptions": [
    {"pattern": "divided_by_rows", "expect": 12.25,
     "message": "Divide Σfx by the total frequency Σf = 20, not by the number of rows (4). 49 ÷ 20 = 2.45, not 49 ÷ 4 = 12.25.",
     "note": "error: divided by number of classes"}],
  "guided_steps": [
    sy("Mean from a frequency table: multiply each value by its frequency, add those, then divide by the total frequency."),
    box("1 × 4 = ", 4, "Value times frequency."),
    box("2 × 7 = ", 14, "Value times frequency."),
    box("3 × 5 = ", 15, "Value times frequency."),
    box("4 × 4 = ", 16, "Value times frequency."),
    box("Σfx = 4 + 14 + 15 + 16 = ", 49, "Add the four products."),
    box("Σf = 4 + 7 + 5 + 4 = ", 20, "Add the frequencies.", say="Now the total frequency Σf:", phase="substitute"),
    box("49 ÷ 20 = ", 2.45, "49 divided by 20.", say="Mean = Σfx ÷ Σf:", done="Mean 2.45.", phase="substitute"),
    box("2.45 × 20 = ", 49, "Multiply the mean by 20.", say="Check: multiplying back should return Σfx.", done="Back to Σfx = 49, so 2.45 is right.", phase="substitute")]},
 {  # S1 new mean after adding = 12
  "display": "The mean of 4 numbers is 10. A 5th number (20) is added. Find the new mean.",
  "solutions": [12], "calculator": False, "input_type": "single_value",
  "hint": "Rebuild the total, add the new number, then divide by 5.",
  "misconceptions": [
    {"pattern": "averaged_values", "expect": 15,
     "message": "Do not average 10 and 20 to get 15. Rebuild the total: old total 40 plus 20 is 60, shared by 5 numbers, giving 12.",
     "note": "error: averaged the old mean with the new value"}],
  "guided_steps": [
    sy("Turn the old mean back into a total, add the new number, then re-average."),
    box("Old total = mean × count = 10 × 4 = ", 40, "Mean times how many."),
    box("Add the new number: 40 + 20 = ", 60, "Add 20 to the old total."),
    box("60 ÷ 5 = ", 12, "How many 5s make 60?", say="There are now 5 numbers. New mean = new total ÷ 5:", done="New mean 12.", phase="substitute"),
    box("12 × 5 = ", 60, "Mean times 5.", say="Check: adding a 20 (above the old mean of 10) should pull the mean up, and 12 is above 10.", done="Back to 60, so the new mean 12 is right.", phase="substitute")]},
 {  # S2 grouped mean = 16.2 (was 15.4, already corrected in live)
  "display": "Grouped data: 0-10 (f=5), 10-20 (f=12), 20-30 (f=8). Estimate the mean.",
  "solutions": [16.2], "calculator": True, "input_type": "single_value",
  "hint": "Use the class midpoints, then divide the total by the total frequency.",
  "misconceptions": [
    {"pattern": "used_lower_bounds", "expect": 11.2,
     "message": "Use each class midpoint (5, 15, 25), not the lower bound. Σfx = 25 + 180 + 200 = 405, and 405 ÷ 25 = 16.2.",
     "note": "error: used lower class bounds 0,10,20 giving 280/25=11.2"}],
  "guided_steps": [
    sy("Grouped data: use each class midpoint as a stand-in value, then it is just a frequency-table mean."),
    box("Midpoint of 0-10 = ", 5, "Halfway between 0 and 10."),
    box("Midpoint of 10-20 = ", 15, "Halfway between 10 and 20."),
    box("Midpoint of 20-30 = ", 25, "Halfway between 20 and 30."),
    box("Σfx = 5×5 + 15×12 + 25×8 = 25 + 180 + 200 = ", 405, "Add the three products 25, 180 and 200."),
    box("Σf = 5 + 12 + 8 = ", 25, "Add the frequencies.", say="Total frequency Σf:", phase="substitute"),
    box("405 ÷ 25 = ", 16.2, "405 divided by 25.", say="Mean = Σfx ÷ Σf:", done="Estimated mean 16.2.", phase="substitute"),
    box("16.2 × 25 = ", 405, "Multiply the mean by 25.", say="Check: multiplying back should return Σfx.", done="Back to Σfx = 405, so 16.2 is right.", phase="substitute")]},
 {  # S3 IQR = 7
  "display": "Find Q1 and Q3 of: 2, 3, 5, 7, 8, 10, 12. What is the IQR?",
  "solutions": [7], "calculator": False, "input_type": "single_value",
  "hint": "Find Q1 and Q3, then subtract.",
  "misconceptions": [
    {"pattern": "included_median", "expect": 5,
     "message": "With 7 values, leave the median (7) out when finding the quartiles. Then Q1 = 3 and Q3 = 10, so IQR = 7. Including the median in both halves gives 5.",
     "note": "error: included median in both halves -> Q1=4, Q3=9, IQR=5"}],
  "guided_steps": [
    sy("IQR = Q3 minus Q1. With 7 values the median is the 4th; the quartiles are the middles of the lower and upper halves, leaving the median out."),
    box("The median (4th value) is ", 7, "The middle of seven ordered values."),
    box("Lower half is 2, 3, 5. Its middle, Q1 = ", 3, "The middle of 2, 3, 5."),
    box("Upper half is 8, 10, 12. Its middle, Q3 = ", 10, "The middle of 8, 10, 12."),
    box("10 − 3 = ", 7, "Subtract Q1 from Q3.", say="IQR = Q3 − Q1:", done="IQR 7.", phase="substitute"),
    box("12 − 2 = ", 10, "Largest minus smallest.", say="Check: the IQR should be smaller than the full range.", done="The IQR 7 is less than the range 10, as it should be.", phase="substitute")]},
 {  # S4 combined mean = 69.2
  "display": "Class A mean = 65, Class B mean = 72. Class A has 20 students, Class B has 30. Find the combined mean.",
  "solutions": [69.2], "calculator": True, "input_type": "single_value",
  "hint": "Weight each mean by its class size before combining.",
  "misconceptions": [
    {"pattern": "averaged_means", "expect": 68.5,
     "message": "You cannot just average 65 and 72. Weight by class size: (20 × 65 + 30 × 72) ÷ 50 = 3460 ÷ 50 = 69.2.",
     "note": "error: averaged the two means ignoring sizes"}],
  "guided_steps": [
    sy("You cannot just average the two means, because the classes are different sizes. Turn each mean into a total first."),
    box("Class A total = 65 × 20 = ", 1300, "Mean times number of students."),
    box("Class B total = 72 × 30 = ", 2160, "Mean times number of students."),
    box("Combined total = 1300 + 2160 = ", 3460, "Add the two totals."),
    box("3460 ÷ 50 = ", 69.2, "3460 divided by 50.", say="Total students = 20 + 30 = 50. Combined mean = combined total ÷ 50:", done="Combined mean 69.2.", phase="substitute"),
    box("Which mean is 69.2 nearer, 65 or 72? Type it: ", 72, "Class B is bigger, so the combined mean is pulled toward its mean.", say="Check: the combined mean should lie between 65 and 72, nearer the bigger class.", done="69.2 lies between 65 and 72 and nearer 72, exactly as the bigger class demands.", phase="substitute")]},
 {  # S5 modal class lower bound = 10
  "display": "The modal class of grouped data is the class with the highest frequency. Data: 0-5 (f=3), 5-10 (f=8), 10-15 (f=12), 15-20 (f=7). What is the modal class? Give the lower bound.",
  "solutions": [10], "calculator": False, "input_type": "single_value",
  "hint": "Pick the class with the highest frequency and give its lower bound.",
  "misconceptions": [
    {"pattern": "gave_upper_bound", "expect": 15,
     "message": "The modal class is 10-15. Give its lower bound, 10, not the upper bound 15.",
     "note": "error: read the upper bound of the modal class"}],
  "guided_steps": [
    sy("The modal class is simply the class with the highest frequency. Compare the frequencies."),
    box("The highest frequency in the table is ", 12, "The biggest f value."),
    box("The lower bound of the class with frequency 12 (the 10-15 class) = ", 10, "The smaller number in 10-15.", say="That frequency belongs to the class 10-15, and the question wants its lower bound:", done="Modal class 10-15, lower bound 10.", phase="substitute"),
    box("The next highest frequency is ", 8, "After 12, the biggest f is for 5-10.", say="Check nothing beats a frequency of 12:", done="12 is the largest, so 10-15 is the modal class.", phase="substitute")]},
 {  # S6 median class lower bound = 20
  "display": "The median of grouped data with 50 values is in the \\(\\frac{50}{2} = 25\\text{th}\\) position. If the cumulative frequencies are: <15 (8), <20 (22), <25 (38), <30 (50). Which class contains the median? Give the lower bound.",
  "solutions": [20], "calculator": False, "input_type": "single_value",
  "hint": "Find which class the 25th value falls in using the cumulative totals.",
  "misconceptions": [
    {"pattern": "off_by_one_class", "expect": 15,
     "message": "The cumulative total reaches 22 at under 20 and 38 at under 25, so the 25th value is in the 20-25 class. Its lower bound is 20, not 15.",
     "note": "error: picked the class just before the median position"}],
  "guided_steps": [
    sy("The median is the 25th value. Walk up the cumulative frequencies until you first pass 25."),
    box("Up to under 20, the running total is ", 22, "Read the cumulative frequency at under 20."),
    box("The lower bound of the 20-25 class = ", 20, "The smaller number in 20-25.", say="22 is still below 25, so the 25th value has not appeared yet; the next class 20-25 pushes the total to 38, so the 25th lands there:", done="The 25th value is in 20-25, lower bound 20.", phase="substitute"),
    box("The 20-25 class covers positions 23 up to ", 38, "The cumulative frequency at under 25.", say="Check the class straddles position 25:", done="Positions 23 to 38 include the 25th, so 20-25 holds the median.", phase="substitute")]},
]

# =========================== GOLD ===========================
gold = [
 {  # G0 largest = 18 (problem re-posed to be consistent)
  "display": "Five numbers have a mean of 12, a median of 10 and a mode of 10. The range is 10 and the smallest number is 8. What is the largest number?",
  "solutions": [18], "calculator": False, "input_type": "single_value",
  "hint": "The range gives the largest directly: smallest plus range.",
  "misconceptions": [
    {"pattern": "range_is_largest", "expect": 10,
     "message": "The range is the gap between the largest and smallest, not the largest itself. Largest = smallest + range = 8 + 10 = 18.",
     "note": "error: read the range value 10 as the answer"}],
  "guided_steps": [
    sy("The range links the largest and smallest directly: range = largest − smallest. You already know two of these three."),
    box("The smallest number is given as ", 8, "Read it from the question."),
    box("The range is ", 10, "Read it from the question."),
    box("8 + 10 = ", 18, "Add the range to the smallest.", say="Rearrange range = largest − smallest into largest = smallest + range:", done="Largest 18.", phase="substitute"),
    box("8 + 10 + 10 + 14 + 18 = ", 60, "Add the five numbers.", say="Check the other clues fit. The total should be mean × 5 = 12 × 5 = 60. A set 8, 10, 10, 14, 18 has smallest 8, mode 10, median 10 and range 10:", done="Total 60 gives mean 12, and every clue checks out, so the largest is 18.", phase="substitute")]},
 {  # G1 new mean = 40/3 (fraction)
  "display": "A set of 10 numbers has mean 15. When the largest number (30) is removed, find the new mean.",
  "solutions": [40, 3], "calculator": False, "input_type": "fraction",
  "hint": "Rebuild the total, remove 30, then divide by 9.",
  "misconceptions": [
    {"pattern": "wrong_count", "expect": [120, 10],
     "message": "After removing a number there are 9 left, not 10. New mean = 120 ÷ 9 = 40/3, not 120 ÷ 10.",
     "note": "error: divided by the original count 10"}],
  "guided_steps": [
    sy("Turn the mean into a total, take the removed number off, then re-average over the smaller count."),
    box("Original total = mean × count = 15 × 10 = ", 150, "Mean times how many."),
    box("Remove the largest: 150 − 30 = ", 120, "Subtract 30 from 150."),
    box("Numerator: 120 ÷ 3 = ", 40, "120 divided by 3.", say="One number was removed, so 9 remain. The new mean is 120 ÷ 9. As a fraction that is 120/9, which cancels: divide top and bottom by 3.", phase="substitute"),
    box("Denominator: 9 ÷ 3 = ", 3, "9 divided by 3.", done="New mean = 40/3.", phase="substitute"),
    box("40 × 9 ÷ 3 = ", 120, "40 times 9 is 360, divided by 3.", say="Check: 40/3 is about 13.3, a little below the old mean 15, which makes sense after removing the largest value. Multiplying back over 9 should return the total:", done="Back to the total 120, so 40/3 is right.", phase="substitute")]},
 {  # G2 combined mean = 25
  "display": "Combined mean: Group X (n=15, mean=20) and Group Y (n=25, mean=28). Find the combined mean.",
  "solutions": [25], "calculator": True, "input_type": "single_value",
  "hint": "Weight each mean by its group size before combining.",
  "misconceptions": [
    {"pattern": "averaged_means", "expect": 24,
     "message": "You cannot just average 20 and 28. Weight by size: (15 × 20 + 25 × 28) ÷ 40 = 1000 ÷ 40 = 25.",
     "note": "error: averaged the two means ignoring sizes"}],
  "guided_steps": [
    sy("Different group sizes, so weight by size. Turn each mean into a total first."),
    box("Group X total = 15 × 20 = ", 300, "Size times mean."),
    box("Group Y total = 25 × 28 = ", 700, "Size times mean."),
    box("Combined total = 300 + 700 = ", 1000, "Add the two totals."),
    box("1000 ÷ 40 = ", 25, "1000 divided by 40.", say="Total members = 15 + 25 = 40. Combined mean = 1000 ÷ 40:", done="Combined mean 25.", phase="substitute"),
    box("25 × 40 = ", 1000, "25 times 40.", say="Check: 25 lies between 20 and 28, nearer 28 because Y is the bigger group. Multiplying back should return the total:", done="Back to 1000, so the combined mean 25 is right.", phase="substitute")]},
 {  # G3 grouped mean = 23.67
  "display": "A teacher needs to estimate the mean from grouped data: 0-10(f=6), 10-30(f=14), 30-50(f=10). Calculate it.",
  "solutions": [23.67], "calculator": True, "input_type": "single_value",
  "hint": "Use the class midpoints, then divide by the total frequency and round.",
  "misconceptions": [
    {"pattern": "used_lower_bounds", "expect": 14.67,
     "message": "Use each class midpoint (5, 20, 40), not the lower bound. Σfx = 30 + 280 + 400 = 710, and 710 ÷ 30 = 23.67.",
     "note": "error: used lower bounds 0,10,30 giving 440/30=14.67"}],
  "guided_steps": [
    sy("Grouped data: replace each class by its midpoint, then take a frequency-table mean. Watch the middle class, it is wider."),
    box("Midpoint of 0-10 = ", 5, "Halfway between 0 and 10."),
    box("Midpoint of 10-30 = ", 20, "Halfway between 10 and 30."),
    box("Midpoint of 30-50 = ", 40, "Halfway between 30 and 50."),
    box("Σfx = 6×5 + 14×20 + 10×40 = 30 + 280 + 400 = ", 710, "Add 30, 280 and 400."),
    box("Σf = 6 + 14 + 10 = ", 30, "Add the frequencies.", say="Total frequency Σf:", phase="substitute"),
    box("710 ÷ 30 = ", 23.67, "710 divided by 30 is 23.666..., round to 23.67.", say="Mean = Σfx ÷ Σf = 710 ÷ 30. This does not come out exactly, so round to 2 decimal places:", done="Estimated mean 23.67.", phase="substitute"),
    box("30 + 280 + 400 = ", 710, "Add the three products again.", say="Check: re-add the products to confirm Σfx.", done="Σfx = 710, and 710 ÷ 30 = 23.67, so the estimate is right.", phase="substitute")]},
 {  # G4 find n = 11
  "display": "The mean of \\(n\\) numbers is 24. When one more number (36) is added, the mean becomes 25. Find \\(n\\).",
  "solutions": [11], "calculator": False, "input_type": "single_value",
  "hint": "Set the total before equal to the total after: 24n + 36 = 25(n+1).",
  "misconceptions": [
    {"pattern": "forgot_extra_count", "expect": 36,
     "message": "Adding a number makes n+1 numbers, so the new total is 25(n+1), not 25n. Then 24n + 36 = 25n + 25 gives n = 11. Using 25n wrongly gives 36.",
     "note": "error: used 25n on the right, so 24n+36=25n gives n=36"}],
  "guided_steps": [
    sy("Set up two totals. Before, the total is 24n. After adding 36 there are n+1 numbers with mean 25, so the total is 25(n+1). The totals must match: 24n + 36 = 25(n+1)."),
    box("Expand the right side: 25 × (n + 1) = 25n + ", 25, "25 times 1."),
    box("The n terms give 25n − 24n = n; the numbers give 36 − 25 = ", 11, "Take 24n from both sides, then 36 − 25.", say="So 24n + 36 = 25n + 25. Bring the n terms together and the numbers together:", done="n = 11.", phase="substitute"),
    box("Check with n = 11. Before: 24 × 11 = ", 264, "24 times 11.", say="Rebuild the totals to be sure:", phase="substitute"),
    box("Add 36, then share over 12 numbers: 300 ÷ 12 = ", 25, "300 divided by 12.", say="After adding 36 the total is 264 + 36 = 300, over 12 numbers:", done="The new mean is 25, exactly as stated, so n = 11 is right.", phase="substitute")]},
]

problem_bank = {
 "bronze_description": "Find one average (mean, median or mode) or the range from a short list of numbers.",
 "silver_description": "Averages and spread from frequency tables and grouped data, including quartiles, the IQR and combined means.",
 "gold_description": "Work backwards from an average to a missing value, and estimate means from grouped or combined data.",
 "bronze": bronze, "silver": silver, "gold": gold,
}

# =========================== tier_guides ===========================
tier_guides = {
 "bronze": {
   "title": "Bronze: one average from a list",
   "steps": [
     "<strong>Mean</strong>: add every value, then divide by how many there are.",
     "<strong>Median</strong>: put the values in order and take the middle one. With an even count, average the middle two.",
     "<strong>Mode</strong> is the most common value. <strong>Range</strong> is largest minus smallest, a measure of spread."],
   "example": {
     "question": "Find the median of 7, 2, 9, 4, 6",
     "steps": [
       {"label": "Order", "content": "2, 4, 6, 7, 9"},
       {"label": "Check", "content": "Five values, so the middle is the 3rd."},
       {"label": "Answer", "content": "Median = <strong>6</strong>", "isAnswer": True, "is_answer": True}]}},
 "silver": {
   "title": "Silver: tables, groups and spread",
   "steps": [
     "<strong>Frequency table mean</strong>: multiply each value by its frequency, add to get \\(\\sum fx\\), then divide by the total frequency \\(\\sum f\\).",
     "<strong>Grouped data</strong>: use the midpoint of each class as its value, then take the same \\(\\sum fx \\div \\sum f\\).",
     "<strong>IQR</strong> is Q3 minus Q1. The <strong>modal class</strong> has the highest frequency; the <strong>median class</strong> holds the middle position."],
   "example": {
     "question": "Estimate the mean of 0-10 (f=2), 10-20 (f=3)",
     "steps": [
       {"label": "Midpoints", "content": "5 and 15"},
       {"label": "\\(\\sum fx\\)", "content": "5×2 + 15×3 = 10 + 45 = 55"},
       {"label": "Check", "content": "\\(\\sum f = 5\\), so divide 55 by 5."},
       {"label": "Answer", "content": "Mean = \\(55 \\div 5 = 11\\)", "isAnswer": True, "is_answer": True}]}},
 "gold": {
   "title": "Gold: work backwards and estimate",
   "steps": [
     "<strong>Missing value</strong>: turn the mean into a total (mean × how many), then use what you know to find the gap.",
     "<strong>Combined mean</strong>: add the group totals, add the group sizes, then divide. Never just average the two means.",
     "<strong>Grouped estimate</strong>: midpoints give \\(\\sum fx\\), then divide by \\(\\sum f\\); round if it does not come out exactly."],
   "example": {
     "question": "The mean of 5 numbers is 9. Four of them are 6, 8, 10, 11. Find the fifth.",
     "steps": [
       {"label": "Total", "content": "Mean × 5 = 9 × 5 = 45"},
       {"label": "Known sum", "content": "6 + 8 + 10 + 11 = 35"},
       {"label": "Check", "content": "The fifth is the total minus the known sum."},
       {"label": "Answer", "content": "Fifth = 45 − 35 = <strong>10</strong>", "isAnswer": True, "is_answer": True}]}},
}

# =========================== guided (opener + teach) ===========================
guided = {
 "opener": {
   "display": "Three friends empty their pockets onto the table:<br><strong>£2, £4, £9</strong><br>They decide to pool it all and split it equally.",
   "steps": [
     sy("No formulas. Just look at the money on the table."),
     box("Altogether they have £", 15, "Add the three amounts: 2 + 4 + 9.", say="First, how much is on the table in total?"),
     sy("Now share that total equally between the 3 of them."),
     box("Each friend gets £", 5, "Divide the total by how many friends: 15 ÷ 3.", say="Split it three ways:"),
     sy("That number, £5, is the <strong>mean</strong>. You found it the natural way: pool everything, then share it equally. \"Add them all up, divide by how many\" is the whole idea. The mean is the fair share, the amount each would have if it were levelled out.")]},
 "teach": {
   "bronze": {
     "display": "Find the mean of \\(6, 9, 4, 5\\)",
     "steps": [
       sy("The mean is add-them-all-up, then divide by how many. Add first."),
       box("6 + 9 + 4 + 5 = ", 24, "Add left to right: 6 and 9 is 15, plus 4 is 19, plus 5."),
       box("How many numbers are there? ", 4, "Just count them."),
       box("24 ÷ 4 = ", 6, "How many 4s make 24?", say="Now divide the total by how many:", done="Gone. Add up, divide by how many, that is the whole move."),
       box("6 × 4 = ", 24, "Multiply the mean by how many numbers.", say="Check by multiplying back:", done="Back to 24, so the mean of 6 is right.")]},
   "silver": {
     "display": "A dice is rolled 10 times. Score 1 (f=2), 2 (f=3), 3 (f=5). Find the mean score.",
     "steps": [
       sy("The new move: each score happened several times, so multiply score × frequency before adding. Do each row:"),
       box("1 × 2 = ", 2, "Score times frequency."),
       box("2 × 3 = ", 6, "Score times frequency."),
       box("3 × 5 = ", 15, "Score times frequency."),
       box("Σfx = 2 + 6 + 15 = ", 23, "Add the three products.", say="Add those up to get Σfx, the grand total of all the scores:"),
       box("Σf = 2 + 3 + 5 = ", 10, "Add the frequencies.", say="Now the total number of rolls, Σf:"),
       box("23 ÷ 10 = ", 2.3, "Dividing by 10 just moves the decimal point.", say="Mean = Σfx ÷ Σf:", done="Gone. Multiply each value by its frequency, that is the frequency-table move."),
       box("2.3 × 10 = ", 23, "Multiply the mean by 10.", say="Check: multiplying back should return Σfx.", done="Back to 23, the total we started with, so 2.3 is right.")]},
   "gold": {
     "display": "Estimate the mean of grouped data: 0-10 (f=3), 10-20 (f=5), 20-30 (f=2).",
     "steps": [
       sy("With grouped data you do not know the exact values, only the class each falls in. The new move: use the midpoint of each class as a stand-in."),
       box("Midpoint of 0-10 = ", 5, "Halfway between 0 and 10."),
       box("Midpoint of 10-20 = ", 15, "Halfway between 10 and 20."),
       box("Midpoint of 20-30 = ", 25, "Halfway between 20 and 30."),
       box("5 × 3 = ", 15, "Midpoint times frequency.", say="Now treat each midpoint like a score and multiply by its frequency:"),
       box("15 × 5 = ", 75, "Midpoint times frequency."),
       box("25 × 2 = ", 50, "Midpoint times frequency."),
       box("Σfx = 15 + 75 + 50 = ", 140, "Add the three products."),
       box("Σf = 3 + 5 + 2 = ", 10, "Add the frequencies.", say="Divide by Σf, the total frequency:"),
       box("140 ÷ 10 = ", 14, "Divide 140 by 10.", done="Gone. Midpoints turn a grouped table into an ordinary frequency-table mean."),
       box("14 × 10 = ", 140, "Multiply 14 by 10.", say="Check: multiplying back should return Σfx.", done="Back to Σfx = 140, so the estimate 14 is right.")]},
 },
}

# =========================== method_card (slim) ===========================
method_card = {
 "title": "Averages and Spread",
 "steps": [
   "Mean: add all values, divide by how many (\\(\\sum fx \\div \\sum f\\) for a table).",
   "Median: middle of the ordered data. Mode: most common value.",
   "Grouped data: use class midpoints for the mean; highest frequency gives the modal class.",
   "Range = largest − smallest. IQR = Q3 − Q1, less swayed by outliers."],
 "content": "<p><strong>Averages</strong> summarise data with one number; <strong>spread</strong> says how varied it is.</p><p>The <strong>mean</strong> shares the total equally: \\(\\frac{\\sum fx}{\\sum f}\\) for a frequency table. For <strong>grouped</strong> data, use each class midpoint. The <strong>median</strong> is the middle of the ordered values; the <strong>mode</strong> is the most common.</p><p><strong>Range</strong> = largest − smallest. The <strong>interquartile range</strong>, Q3 − Q1, ignores the extremes, so it is steadier when there are outliers.</p>",
 "example": "<p><strong>Find the mean of: 4, 7, 9, 3, 12</strong></p><p>Mean = \\(\\frac{4 + 7 + 9 + 3 + 12}{5} = \\frac{35}{5} = 7\\)</p>",
}

out = {
 "method_card": method_card,
 "topic_links": topic_links,
 "problem_bank": problem_bank,
 "tier_guides": tier_guides,
 "guided": guided,
 "related_videos": related_videos,
 "worked_examples": worked_examples,
}

json.dump(out, io.open("lesson_probability-statistics-L04.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("written lesson_probability-statistics-L04.json")
