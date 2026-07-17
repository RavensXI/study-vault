# -*- coding: utf-8 -*-
"""Build guided practice_data for ratio-proportion-L01 (maths-ocr).
Every number is asserted before it is written."""
import json, io

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def sayonly(say):
    return {"say": say}

# ---------- load live for preservation of untouched fields ----------
live = json.load(io.open("_rp_L01_live.json", encoding="utf-8"))

pd = {}
# preserve untouched
pd["topic_links"] = live["topic_links"]
pd["related_videos"] = live["related_videos"]
# worked_examples preserved, but strip pre-existing em dashes in labels (style-rule repair)
we = json.loads(json.dumps(live["worked_examples"]))
for ex in we:
    for st in ex.get("steps", []):
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")
pd["worked_examples"] = we

# ---------- method_card (slim to <=4 steps) ----------
pd["method_card"] = {
    "title": "Ratio & Proportion",
    "steps": [
        "Simplify: divide every part by the highest common factor.",
        "Change to the same units first (m to cm, kg to g).",
        "To share a total: add the parts, find one part (total ÷ parts), then multiply.",
        "Check: the shares must add back to the original total.",
    ],
    "content": live["method_card"]["content"],
    "example": live["method_card"]["example"],
}

# ================= PROBLEM BANK =================
pb = {}

# ---- BRONZE ----
bronze = []

# b0 simplify 15:25 -> 3
assert 15//5==3 and 25//5==5
bronze.append({
    "display": "Simplify 15 : 25. Give the first number.",
    "solutions": [3], "calculator": False, "input_type": "single_value",
    "hint": "Divide both parts by their highest common factor.",
    "misconceptions": [
        {"pattern": "gave_second_part", "expect": 5,
         "message": "5 is the second part. The first part is 15 ÷ 5 = 3.",
         "note": "answered the second simplified number"}],
    "guided_steps": [
        sayonly("Find the biggest number that divides BOTH 15 and 25 (the highest common factor)."),
        box("HCF of 15 and 25 = ", 5, "5 divides both: 15 = 3×5, 25 = 5×5."),
        sayonly("Now divide each part by 5."),
        box("15 ÷ 5 = ", 3, "That is the first number of the simplified ratio.", phase="substitute"),
        box("25 ÷ 5 = ", 5, "That is the second number.", phase="substitute"),
        box("3 and 5 share no common factor, so 3 : 5 is fully simplified. The first number is ", 3,
            "Read off the first number.", done="3 : 5 cannot be reduced further, so 3 is right."),
    ]})

# b1 CHANGED 18:24 -> 24:30 -> 4  (was duplicate 3)
assert 24//6==4 and 30//6==5
bronze.append({
    "display": "Simplify 24 : 30. Give the first number.",
    "solutions": [4], "calculator": False, "input_type": "single_value",
    "hint": "Divide both parts by their highest common factor.",
    "misconceptions": [
        {"pattern": "gave_second_part", "expect": 5,
         "message": "5 is the second part. The first part is 24 ÷ 6 = 4.",
         "note": "answered the second simplified number"}],
    "guided_steps": [
        sayonly("Find the highest common factor of 24 and 30."),
        box("HCF of 24 and 30 = ", 6, "6 divides both: 24 = 4×6, 30 = 5×6."),
        sayonly("Divide each part by 6."),
        box("24 ÷ 6 = ", 4, "That is the first number.", phase="substitute"),
        box("30 ÷ 6 = ", 5, "That is the second number.", phase="substitute"),
        box("4 and 5 share no common factor, so 4 : 5 is simplest. The first number is ", 4,
            "Read off the first number.", done="4 : 5 is fully simplified, so 4 is right."),
    ]})

# b2 share £60 ratio 1:2 larger -> 40
assert 60//3==20 and 2*20==40 and 40+20==60
bronze.append({
    "display": "Share £60 in the ratio 1 : 2. What is the larger share?",
    "solutions": [40], "calculator": False, "input_type": "single_value",
    "hint": "Add the parts, find one part, then multiply by the larger part number.",
    "misconceptions": [
        {"pattern": "gave_one_part", "expect": 20,
         "message": "£20 is one part (the smaller share). The larger is 2 parts: 2 × £20 = £40.",
         "note": "stopped at one-part value"},
        {"pattern": "split_equally", "expect": 30,
         "message": "Splitting £60 into two equal £30 halves ignores the ratio. Divide by 1 + 2 = 3 parts, not 2.",
         "note": "60/2 equal split"}],
    "guided_steps": [
        box("Add the parts: 1 + 2 = ", 3, "This is how many equal shares there are."),
        box("One part = £60 ÷ 3 = £", 20, "Divide the total by the number of parts."),
        sayonly("The larger share is the 2-part share."),
        box("Larger = 2 × £20 = £", 40, "Multiply one part by 2.", phase="substitute"),
        box("Check: smaller (1 part) = £20, and 40 + 20 = £", 60,
            "The two shares must add to the total.", phase="substitute",
            done="It gives £60 back, so £40 is right."),
    ]})

# b3 share 45 sweets 2:3 first -> 18
assert 45//5==9 and 2*9==18 and 3*9==27 and 18+27==45
bronze.append({
    "display": "Share 45 sweets in the ratio 2 : 3. How many does the first person get?",
    "solutions": [18], "calculator": False, "input_type": "single_value",
    "hint": "Add the parts, find one part, then multiply by the first part number.",
    "misconceptions": [
        {"pattern": "gave_other_share", "expect": 27,
         "message": "27 is the other person's share (3 parts). The first person gets 2 parts: 2 × 9 = 18.",
         "note": "answered the 3-part share"},
        {"pattern": "gave_one_part", "expect": 9,
         "message": "9 is one part. The first person gets 2 parts: 2 × 9 = 18.",
         "note": "stopped at one-part value"}],
    "guided_steps": [
        box("Add the parts: 2 + 3 = ", 5, "This is how many equal shares there are."),
        box("One part = 45 ÷ 5 = ", 9, "Divide the total by the number of parts."),
        sayonly("The first person gets the 2-part share."),
        box("First person = 2 × 9 = ", 18, "Multiply one part by 2.", phase="substitute"),
        box("Check: other person = 3 × 9 = 27, and 18 + 27 = ", 45,
            "The shares must add to 45.", phase="substitute",
            done="It gives 45 back, so 18 is right."),
    ]})

# b4 40cm:1m -> 2
assert 100//20==5 and 40//20==2
bronze.append({
    "display": "Write 40 cm : 1 m as a simplified ratio. Give the first number.",
    "solutions": [2], "calculator": False, "input_type": "single_value",
    "hint": "Change 1 m to 100 cm first, then simplify.",
    "misconceptions": [
        {"pattern": "forgot_convert", "expect": 40,
         "message": "40 : 1 forgets that 1 m = 100 cm. Convert first: 40 : 100 = 2 : 5.",
         "note": "left 1 m as 1"},
        {"pattern": "gave_second_part", "expect": 5,
         "message": "5 is the second part. The first is 40 ÷ 20 = 2.",
         "note": "answered second number"}],
    "guided_steps": [
        sayonly("The units must match before you simplify."),
        box("Change 1 m to centimetres: 1 m = ", 100, "1 m = 100 cm."),
        box("HCF of 40 and 100 = ", 20, "20 divides both: 40 = 2×20, 100 = 5×20."),
        box("40 ÷ 20 = ", 2, "That is the first number.", phase="substitute"),
        box("100 ÷ 20 = 5, so the ratio is 2 : 5. The first number is ", 2,
            "Read off the first number.", phase="substitute",
            done="2 : 5 is fully simplified, so 2 is right."),
    ]})

# b5 recipe 4 uses 200g, for 6 -> 300
assert 200//4==50 and 50*6==300
bronze.append({
    "display": "A recipe for 4 uses 200 g flour. How much for 6?",
    "solutions": [300], "calculator": False, "input_type": "single_value",
    "hint": "Find the amount for one, then multiply by 6.",
    "misconceptions": [
        {"pattern": "no_unit_first", "expect": 1200,
         "message": "1200 g multiplies by 6 but forgets the recipe already feeds 4. Find the amount for one first: 200 ÷ 4 = 50 g.",
         "note": "200 × 6 without unitary step"}],
    "guided_steps": [
        box("Amount for one: 200 ÷ 4 = ", 50, "Divide by the number the recipe feeds."),
        sayonly("Now scale up to 6 people."),
        box("For 6: 50 × 6 = ", 300, "Multiply the per-person amount by 6.", phase="substitute"),
        box("Check: 300 ÷ 6 = ", 50, "Should match the per-person amount.", phase="substitute",
            done="50 g each, so 300 g is right."),
    ]})

# b6 CHANGED 12:8 -> 30:42 -> 5  (was duplicate 3)
assert 30//6==5 and 42//6==7
bronze.append({
    "display": "Simplify 30 : 42. Give the first number.",
    "solutions": [5], "calculator": False, "input_type": "single_value",
    "hint": "Divide both parts by their highest common factor.",
    "misconceptions": [
        {"pattern": "gave_second_part", "expect": 7,
         "message": "7 is the second part. The first part is 30 ÷ 6 = 5.",
         "note": "answered second number"}],
    "guided_steps": [
        sayonly("Find the highest common factor of 30 and 42."),
        box("HCF of 30 and 42 = ", 6, "6 divides both: 30 = 5×6, 42 = 7×6."),
        sayonly("Divide each part by 6."),
        box("30 ÷ 6 = ", 5, "That is the first number.", phase="substitute"),
        box("42 ÷ 6 = ", 7, "That is the second number.", phase="substitute"),
        box("5 and 7 share no common factor, so 5 : 7 is simplest. The first number is ", 5,
            "Read off the first number.", done="5 : 7 is fully simplified, so 5 is right."),
    ]})

# b7 share £100 3:2 larger -> 60
assert 100//5==20 and 3*20==60 and 2*20==40 and 60+40==100
bronze.append({
    "display": "Share £100 in the ratio 3 : 2. What is the larger share?",
    "solutions": [60], "calculator": False, "input_type": "single_value",
    "hint": "Add the parts, find one part, then multiply by 3.",
    "misconceptions": [
        {"pattern": "gave_other_share", "expect": 40,
         "message": "£40 is the smaller share (2 parts). The larger is 3 parts: 3 × £20 = £60.",
         "note": "answered the 2-part share"},
        {"pattern": "gave_one_part", "expect": 20,
         "message": "£20 is one part. The larger is 3 parts: 3 × £20 = £60.",
         "note": "stopped at one-part value"}],
    "guided_steps": [
        box("Add the parts: 3 + 2 = ", 5, "This is how many equal shares there are."),
        box("One part = £100 ÷ 5 = £", 20, "Divide the total by the number of parts."),
        sayonly("The larger share is the 3-part share."),
        box("Larger = 3 × £20 = £", 60, "Multiply one part by 3.", phase="substitute"),
        box("Check: smaller (2 parts) = £40, and 60 + 40 = £", 100,
            "The two shares must add to the total.", phase="substitute",
            done="It gives £100 back, so £60 is right."),
    ]})

pb["bronze"] = bronze
pb["bronze_description"] = "Simplify a ratio, or share a total between two parts."

# ---- SILVER ----
silver = []

# s0 £360 1:2:3 largest -> 180
assert 360//6==60 and 3*60==180 and 60+120+180==360
silver.append({
    "display": "Share £360 in the ratio 1 : 2 : 3. What is the largest share?",
    "solutions": [180], "calculator": False, "input_type": "single_value",
    "hint": "Add all three parts, find one part, then multiply by the largest.",
    "misconceptions": [
        {"pattern": "gave_one_part", "expect": 60,
         "message": "£60 is one part. The largest is 3 parts: 3 × £60 = £180.",
         "note": "stopped at one-part value"},
        {"pattern": "split_equally", "expect": 120,
         "message": "Dividing £360 three equal ways ignores the ratio. There are 1 + 2 + 3 = 6 parts, so one part is £60.",
         "note": "360/3 equal split"}],
    "guided_steps": [
        box("Add the parts: 1 + 2 + 3 = ", 6, "This is how many equal shares there are."),
        box("One part = £360 ÷ 6 = £", 60, "Divide the total by the number of parts."),
        sayonly("The largest share is the 3-part share."),
        box("Largest = 3 × £60 = £", 180, "Multiply one part by 3.", phase="substitute"),
        box("Check: shares are 60, 120, 180, adding to £", 360,
            "All three shares must add to the total.", phase="substitute",
            done="They give £360 back, so £180 is right."),
    ]})

# s1 Ali Ben 3:5, Ali £45, Ben -> 75
assert 45//3==15 and 5*15==75
silver.append({
    "display": "Ali and Ben share money in the ratio 3 : 5. Ali gets £45. How much does Ben get?",
    "solutions": [75], "calculator": False, "input_type": "single_value",
    "hint": "Ali's 3 parts are worth £45, so find one part first.",
    "misconceptions": [
        {"pattern": "treated_share_as_one_part", "expect": 225,
         "message": "£45 is Ali's 3 parts, not one part. One part is 45 ÷ 3 = £15, so Ben = 5 × 15 = £75.",
         "note": "multiplied the whole £45 by 5"}],
    "guided_steps": [
        sayonly("Ali's share of £45 is his 3 parts."),
        box("One part = £45 ÷ 3 = £", 15, "Divide Ali's share by his number of parts."),
        sayonly("Ben has 5 parts."),
        box("Ben = 5 × £15 = £", 75, "Multiply one part by Ben's 5 parts.", phase="substitute"),
        box("Check: Ben ÷ one part = 75 ÷ 15 = ", 5,
            "Ben should be exactly 5 parts.", phase="substitute",
            done="5 parts, matching the ratio 3 : 5, so £75 is right."),
    ]})

# s2 5 books £35, 8 books -> 56
assert 35//5==7 and 7*8==56
silver.append({
    "display": "5 books cost £35. How much do 8 books cost?",
    "solutions": [56], "calculator": False, "input_type": "single_value",
    "hint": "Find the cost of one book, then multiply by 8.",
    "misconceptions": [
        {"pattern": "no_unit_first", "expect": 280,
         "message": "£280 multiplies by 8 but forgets it is 5 books for £35. One book is 35 ÷ 5 = £7.",
         "note": "35 × 8 without unitary step"}],
    "guided_steps": [
        box("One book: £35 ÷ 5 = £", 7, "Divide the cost by the number of books."),
        sayonly("Now scale up to 8 books."),
        box("8 books: £7 × 8 = £", 56, "Multiply the per-book cost by 8.", phase="substitute"),
        box("Check: £56 ÷ 8 = £", 7, "Should match the price of one book.", phase="substitute",
            done="£7 each, so £56 is right."),
    ]})

# s3 CHANGED 3:5 -> 2:5 in form 1:n -> 2.5 (was messy 1.667)
assert 5/2==2.5
silver.append({
    "display": "Express 2 : 5 in the form 1 : n. Give n as a decimal.",
    "solutions": [2.5], "calculator": False, "input_type": "single_value",
    "hint": "Divide both parts by the left-hand number.",
    "misconceptions": [
        {"pattern": "inverted_ratio", "expect": 0.4,
         "message": "0.4 is 2 ÷ 5. For 1 : n, divide the SECOND part by the first: 5 ÷ 2 = 2.5.",
         "note": "divided first by second"}],
    "guided_steps": [
        sayonly("To get 1 on the left, divide BOTH parts by the left-hand part, 2."),
        box("Left part: 2 ÷ 2 = ", 1, "The left-hand side becomes 1."),
        box("Right part: 5 ÷ 2 = ", 2.5, "This is n.", phase="substitute"),
        box("Check: scale 1 : 2.5 back up by 2. 2.5 × 2 = ", 5,
            "It should return the original second part.", phase="substitute",
            done="Back to 2 : 5, so n = 2.5 is right."),
    ]})

# s4 map 1:50000, 3cm -> 1500 m
assert 3*50000==150000 and 150000//100==1500
silver.append({
    "display": "A map scale is 1 : 50000. A distance is 3 cm on the map. What is the real distance in metres?",
    "solutions": [1500], "calculator": False, "input_type": "single_value",
    "hint": "Multiply by the scale, then change centimetres to metres.",
    "misconceptions": [
        {"pattern": "forgot_convert", "expect": 150000,
         "message": "150000 is the real distance in centimetres. Change to metres by dividing by 100: 1500 m.",
         "note": "left answer in cm"}],
    "guided_steps": [
        box("Real distance in cm: 3 × 50000 = ", 150000, "Multiply the map distance by the scale."),
        sayonly("Now change centimetres to metres."),
        box("150000 ÷ 100 = ", 1500, "100 cm make 1 m.", phase="substitute"),
        box("Check: 1500 m = 150000 cm, and 150000 ÷ 50000 = ", 3,
            "Should return the 3 cm on the map.", phase="substitute",
            done="Back to 3 cm, so 1500 m is right."),
    ]})

# s5 concrete 1:2:4, sand for 350 -> 100
assert 350//7==50 and 2*50==100 and 50+100+200==350
silver.append({
    "display": "Concrete is mixed in the ratio 1 : 2 : 4 (cement : sand : gravel). How much sand for 350 kg?",
    "solutions": [100], "calculator": False, "input_type": "single_value",
    "hint": "Add the parts, find one part, then multiply by the sand parts.",
    "misconceptions": [
        {"pattern": "gave_one_part", "expect": 50,
         "message": "50 kg is one part (the cement). Sand is 2 parts: 2 × 50 = 100 kg.",
         "note": "stopped at one-part value"},
        {"pattern": "gave_wrong_ingredient", "expect": 200,
         "message": "200 kg is the gravel (4 parts). Sand is 2 parts: 2 × 50 = 100 kg.",
         "note": "answered the 4-part share"}],
    "guided_steps": [
        box("Add the parts: 1 + 2 + 4 = ", 7, "This is how many equal shares there are."),
        box("One part = 350 ÷ 7 = ", 50, "Divide the total mass by the number of parts."),
        sayonly("Sand is 2 parts."),
        box("Sand = 2 × 50 = ", 100, "Multiply one part by the sand's 2 parts.", phase="substitute"),
        box("Check: 50 + 100 + 200 = ", 350, "All three add to the total mass.", phase="substitute",
            done="They give 350 kg back, so 100 kg is right."),
    ]})

# s6 recipe 6 uses 450ml, for 10 -> 750
assert 450//6==75 and 75*10==750
silver.append({
    "display": "A recipe for 6 uses 450 ml milk. How much for 10?",
    "solutions": [750], "calculator": False, "input_type": "single_value",
    "hint": "Find the amount for one, then multiply by 10.",
    "misconceptions": [
        {"pattern": "no_unit_first", "expect": 4500,
         "message": "4500 ml multiplies by 10 but forgets the recipe feeds 6. Find the amount for one first: 450 ÷ 6 = 75 ml.",
         "note": "450 × 10 without unitary step"}],
    "guided_steps": [
        box("Amount for one: 450 ÷ 6 = ", 75, "Divide by the number the recipe feeds."),
        sayonly("Now scale up to 10."),
        box("For 10: 75 × 10 = ", 750, "Multiply the per-person amount by 10.", phase="substitute"),
        box("Check: 750 ÷ 10 = ", 75, "Should match the per-person amount.", phase="substitute",
            done="75 ml each, so 750 ml is right."),
    ]})

pb["silver"] = silver
pb["silver_description"] = "Three-part ratios, unitary scaling, and converting to 1 : n or a map scale."

# ---- GOLD ----
gold = []

# g0 Amy Ben 2:5, Ben £36 more, total -> 84
assert (5-2)==3 and 36//3==12 and (2+5)*12==84 and 5*12-2*12==36
gold.append({
    "display": "Amy and Ben share money 2 : 5. Ben gets £36 more than Amy. What is the total?",
    "solutions": [84], "calculator": False, "input_type": "single_value",
    "hint": "The difference in parts is worth £36, so find one part.",
    "misconceptions": [
        {"pattern": "diff_as_one_part", "expect": 252,
         "message": "£36 is the difference of 3 parts, not one part. One part is 36 ÷ 3 = £12, so total = 7 × 12 = £84.",
         "note": "treated £36 as one part, 7×36"}],
    "guided_steps": [
        sayonly("Ben has 5 parts, Amy has 2. The gap between them is worth £36."),
        box("Gap in parts: 5 − 2 = ", 3, "Subtract the two part numbers."),
        box("One part = £36 ÷ 3 = £", 12, "The £36 gap is 3 parts."),
        box("Total parts = 2 + 5 = ", 7, "Add both part numbers.", phase="substitute"),
        box("Total = 7 × £12 = £", 84, "Multiply total parts by one part.", phase="substitute"),
        box("Check: Amy 2×12 = 24, Ben 5×12 = 60, gap 60 − 24 = £", 36,
            "The gap must come back to £36.", phase="substitute",
            done="£36 more, matching the question, so £84 is right."),
    ]})

# g1 a:b=2:3, b:c=4:5, a:c first -> 8
assert 2*4==8 and 5*3==15  # scale first ratio by 4 (b:3->12), second by 3 (b:4->12)
gold.append({
    "display": "The ratio a : b = 2 : 3 and b : c = 4 : 5. Find a : c. Give the first number in simplest form.",
    "solutions": [8], "calculator": False, "input_type": "single_value",
    "hint": "Make b match by scaling both ratios to the same b value.",
    "misconceptions": [
        {"pattern": "ignored_b", "expect": 2,
         "message": "Combining a : b and b : c is not just reading off a and c. Scale so b matches (b = 12): a : c = 8 : 15, so the first number is 8.",
         "note": "took a=2 directly"}],
    "guided_steps": [
        sayonly("Make b the same in both ratios. b is 3 in the first and 4 in the second; the common value is 12."),
        box("Scale a : b so b = 12: multiply by 12 ÷ 3 = ", 4, "3 goes into 12 four times."),
        box("Then a = 2 × 4 = ", 8, "Scale a by the same 4."),
        box("Scale b : c so b = 12: multiply by 12 ÷ 4 = ", 3, "4 goes into 12 three times."),
        box("Then c = 5 × 3 = ", 15, "Scale c by the same 3.", phase="substitute"),
        box("So a : c = 8 : 15. The first number is ", 8,
            "Read off the first number of a : c.", phase="substitute",
            done="8 and 15 share no factor, so 8 : 15 is simplest and 8 is right."),
    ]})

# g2 best value A 750g £2.70, B 1.2kg £4.20 -> B=2
assert round(270/750,4)==0.36 and round(420/1200,4)==0.35 and 1.2*1000==1200
gold.append({
    "display": "Pack A: 750 g for £2.70. Pack B: 1.2 kg for £4.20. Which is better value? Enter A=1, B=2.",
    "solutions": [2], "calculator": True, "input_type": "single_value",
    "hint": "Work out the price per gram for each pack, then compare.",
    "misconceptions": [
        {"pattern": "compared_total_price", "expect": 1,
         "message": "Pack A is cheaper overall but smaller. Per gram, A is 0.36p and B is 0.35p, so B is the better value.",
         "note": "picked cheaper total price"}],
    "guided_steps": [
        box("Pack B in grams: 1.2 × 1000 = ", 1200, "1 kg = 1000 g."),
        box("Pack A pence per gram: 270 ÷ 750 = ", 0.36, "Price in pence divided by grams."),
        box("Pack B pence per gram: 420 ÷ 1200 = ", 0.35, "Price in pence divided by grams.", phase="substitute"),
        box("0.35p is less than 0.36p, so B is cheaper per gram. Enter B as ", 2,
            "The lower price per gram is the better value.", phase="substitute",
            done="B costs less per gram, so 2 (B) is right."),
    ]})

# g3 boys:girls 3:4, 35, boys -> 15
assert 35//7==5 and 3*5==15 and 4*5==20 and 15+20==35
gold.append({
    "display": "In a class, boys : girls = 3 : 4. There are 35 students. How many boys?",
    "solutions": [15], "calculator": False, "input_type": "single_value",
    "hint": "Add the parts, find one part, then multiply by the boys' parts.",
    "misconceptions": [
        {"pattern": "gave_other_share", "expect": 20,
         "message": "20 is the number of girls (4 parts). Boys are 3 parts: 3 × 5 = 15.",
         "note": "answered the 4-part share"},
        {"pattern": "gave_one_part", "expect": 5,
         "message": "5 is one part. Boys are 3 parts: 3 × 5 = 15.",
         "note": "stopped at one-part value"}],
    "guided_steps": [
        box("Add the parts: 3 + 4 = ", 7, "This is how many equal shares there are."),
        box("One part = 35 ÷ 7 = ", 5, "Divide the total students by the number of parts."),
        sayonly("Boys are 3 parts."),
        box("Boys = 3 × 5 = ", 15, "Multiply one part by the boys' 3 parts.", phase="substitute"),
        box("Check: girls = 4 × 5 = 20, and 15 + 20 = ", 35,
            "Boys and girls must add to 35.", phase="substitute",
            done="They give 35 back, so 15 boys is right."),
    ]})

# g4 juice:water 2:5, 3.5L, juice -> 1
assert 3.5/7==0.5 and 2*0.5==1.0 and 5*0.5==2.5 and 1+2.5==3.5
gold.append({
    "display": "A drink is mixed from juice and water in ratio 2 : 5. How many litres of juice in 3.5 litres?",
    "solutions": [1], "calculator": False, "input_type": "single_value",
    "hint": "Add the parts, find one part, then multiply by the juice parts.",
    "misconceptions": [
        {"pattern": "gave_other_share", "expect": 2.5,
         "message": "2.5 L is the water (5 parts). Juice is 2 parts: 2 × 0.5 = 1 L.",
         "note": "answered the 5-part share"},
        {"pattern": "gave_one_part", "expect": 0.5,
         "message": "0.5 L is one part. Juice is 2 parts: 2 × 0.5 = 1 L.",
         "note": "stopped at one-part value"}],
    "guided_steps": [
        box("Add the parts: 2 + 5 = ", 7, "This is how many equal shares there are."),
        box("One part = 3.5 ÷ 7 = ", 0.5, "Divide the total litres by the number of parts."),
        sayonly("Juice is 2 parts."),
        box("Juice = 2 × 0.5 = ", 1, "Multiply one part by the juice's 2 parts.", phase="substitute"),
        box("Check: water = 5 × 0.5 = 2.5, and 1 + 2.5 = ", 3.5,
            "Juice and water must add to 3.5 L.", phase="substitute",
            done="They give 3.5 L back, so 1 L of juice is right."),
    ]})

pb["gold"] = gold
pb["gold_description"] = "Work backwards from a difference, combine two ratios, or compare best value."

pd["problem_bank"] = pb

# ================= TIER GUIDES =================
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: simplify and share two parts",
        "steps": [
            "A ratio compares parts. To <strong>simplify</strong>, divide every part by the highest common factor, so 15 : 25 becomes 3 : 5.",
            "To <strong>share</strong> a total: add the parts to get the number of equal shares, divide the total by that for one part, then multiply each person's parts.",
            "Always change to the <strong>same units</strong> first, and check the shares add back to the total.",
        ],
        "example": {
            "question": "Share £40 in the ratio 3 : 2. Find the larger share.",
            "steps": [
                {"label": "Add parts", "content": "<p>3 + 2 = 5 parts.</p>"},
                {"label": "One part", "content": "<p>£40 ÷ 5 = £8.</p>"},
                {"label": "Check", "content": "<p>Larger 3 parts = £24, smaller 2 parts = £16, and 24 + 16 = 40 ✓</p>"},
                {"label": "Answer", "content": "<p>Larger share = 3 × £8 = £24.</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: three parts and scaling",
        "steps": [
            "Three-part ratios work the same way: add all the parts, find one part, then multiply for each share.",
            "For <strong>recipes and rates</strong>, use the unitary method: find the value of one item first, then scale up or down.",
            "To write a ratio as <strong>1 : n</strong>, divide both parts by the left-hand number.",
        ],
        "example": {
            "question": "Share £120 in the ratio 2 : 3 : 5. Find the largest share.",
            "steps": [
                {"label": "Add parts", "content": "<p>2 + 3 + 5 = 10 parts.</p>"},
                {"label": "One part", "content": "<p>£120 ÷ 10 = £12.</p>"},
                {"label": "Check", "content": "<p>24 + 36 + 60 = 120 ✓</p>"},
                {"label": "Answer", "content": "<p>Largest = 5 × £12 = £60.</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: work backwards and combine",
        "steps": [
            "Sometimes you are given the <strong>difference</strong> between two shares, not the total. Work out how many parts that difference is, then find one part.",
            "To <strong>combine</strong> two ratios a : b and b : c, scale each so the shared letter b matches, then read off a : c.",
            "For <strong>best value</strong>, work out the price per unit (per gram or per ml) and compare.",
        ],
        "example": {
            "question": "Ann and Ben share money in the ratio 2 : 5. Ben gets £30 more than Ann. Find the total.",
            "steps": [
                {"label": "Gap in parts", "content": "<p>5 − 2 = 3 parts = £30.</p>"},
                {"label": "One part", "content": "<p>£30 ÷ 3 = £10.</p>"},
                {"label": "Check", "content": "<p>Ann 2×10 = 20, Ben 5×10 = 50, gap 50 − 20 = 30 ✓</p>"},
                {"label": "Answer", "content": "<p>Total = 7 × £10 = £70.</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ================= GUIDED (opener + teach) =================
guided = {}

# ---- opener: sharing sweets ----
assert 12//3==4 and 1*4==4 and 2*4==8 and 4+8==12
guided["opener"] = {
    "label": "Before any algebra",
    "display": "12 sweets to share.<br>Deal them out in rounds: 1 for Sam, 2 for Alex, again and again, until the bowl is empty.",
    "steps": [
        {"say": "No formula needed. Just picture dealing the sweets out.",
         "pre": "Each round hands out 1 + 2 = 3 sweets. Number of rounds: 12 ÷ 3 = ",
         "post": "", "answer": 4, "hint": "How many groups of 3 sweets are in 12?"},
        {"say": "So there are 4 rounds.",
         "pre": "Sam gets 1 sweet each round: 1 × 4 = ",
         "post": "", "answer": 4, "hint": "One per round, four rounds."},
        {"pre": "Alex gets 2 sweets each round: 2 × 4 = ",
         "post": "", "answer": 8, "hint": "Two per round, four rounds.",
         "done": "Check: 4 + 8 = 12, the whole bowl."},
        {"say": "That is <strong>dividing in a ratio</strong>. The ratio 1 : 2 means 1 + 2 = 3 equal parts. You found one part (4 sweets), then gave Sam 1 part and Alex 2 parts. Every ratio question is this: add the parts, find one part, then multiply."},
    ],
}

# ---- teach.bronze: share £48 in 3:5 ----
assert 48//8==6 and 5*6==30 and 3*6==18 and 30+18==48
teach_bronze = {
    "display": "Share £48 in the ratio 3 : 5. Find the larger share.",
    "label": "Together: your first one",
    "steps": [
        {"say": "Start by counting the equal parts.",
         "pre": "Add the parts: 3 + 5 = ", "post": "", "answer": 8, "hint": "Add both part numbers."},
        {"pre": "One part = £48 ÷ 8 = £", "post": "", "answer": 6, "hint": "Divide the total by the number of parts."},
        {"say": "The larger share is the 5-part share.",
         "pre": "Larger = 5 × £6 = £", "post": "", "answer": 30, "hint": "Multiply one part by 5."},
        {"pre": "Smaller = 3 × £6 = £", "post": "", "answer": 18, "hint": "Multiply one part by 3."},
        {"pre": "Check: 30 + 18 = £", "post": "", "answer": 48,
         "hint": "The two shares must add to the total.",
         "done": "It gives £48 back, so the larger share £30 is right."},
    ],
}

# ---- teach.silver: share £96 in 1:3:4 ----
assert 96//8==12 and 4*12==48 and 3*12==36 and 1*12==12 and 12+36+48==96
teach_silver = {
    "display": "Share £96 in the ratio 1 : 3 : 4. Find the largest share.",
    "label": "Together: your first one",
    "steps": [
        {"say": "Count all the parts, even for three shares.",
         "pre": "Add the parts: 1 + 3 + 4 = ", "post": "", "answer": 8, "hint": "Add all three part numbers."},
        {"pre": "One part = £96 ÷ 8 = £", "post": "", "answer": 12, "hint": "Divide the total by the number of parts."},
        {"say": "The largest share is the 4-part share.",
         "pre": "Largest = 4 × £12 = £", "post": "", "answer": 48, "hint": "Multiply one part by 4."},
        {"pre": "Middle = 3 × £12 = £", "post": "", "answer": 36, "hint": "Multiply one part by 3."},
        {"pre": "Check: 12 + 36 + 48 = £", "post": "", "answer": 96,
         "hint": "All three shares must add to the total.",
         "done": "It gives £96 back, so the largest share £48 is right."},
    ],
}

# ---- teach.gold: Sam Tom 3:7, Tom £40 more, total ----
assert (7-3)==4 and 40//4==10 and (3+7)*10==100 and 7*10-3*10==40
teach_gold = {
    "display": "Sam and Tom share money in the ratio 3 : 7. Tom gets £40 more than Sam. Find the total.",
    "label": "Together: your first one",
    "steps": [
        {"say": "You are given the gap, not the total. Turn the gap into parts first.",
         "pre": "Gap in parts: 7 − 3 = ", "post": "", "answer": 4, "hint": "Subtract the two part numbers."},
        {"pre": "One part = £40 ÷ 4 = £", "post": "", "answer": 10, "hint": "The £40 gap is 4 parts."},
        {"pre": "Total parts = 3 + 7 = ", "post": "", "answer": 10, "hint": "Add both part numbers."},
        {"pre": "Total = 10 × £10 = £", "post": "", "answer": 100, "hint": "Multiply total parts by one part."},
        {"pre": "Check: Sam 3×10 = 30, Tom 7×10 = 70, gap 70 − 30 = £", "post": "", "answer": 40,
         "hint": "The gap must come back to £40.",
         "done": "£40 more, matching the question, so the total £100 is right."},
    ],
}

guided["teach"] = {"bronze": teach_bronze, "silver": teach_silver, "gold": teach_gold}
pd["guided"] = guided

# ---------- verify every guided_steps final box lands on a solution ----------
def final_box_values(steps):
    return [s["answer"] for s in steps if s.get("answer") is not None]

for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pb[tier]):
        gs = p.get("guided_steps") or []
        vals = final_box_values(gs)
        sol = p["solutions"][0]
        assert sol in vals, "%s[%d] solution %r not produced in walk %r" % (tier, i, sol, vals)
        # every expect != correct
        for m in p.get("misconceptions", []):
            assert m["expect"] != sol, "%s[%d] expect equals solution" % (tier, i)

# write
with open("lesson_maths-ocr_ratio-proportion-L01.json", "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("BUILT ok. top keys:", list(pd.keys()))
print("bronze", len(pb["bronze"]), "silver", len(pb["silver"]), "gold", len(pb["gold"]))
