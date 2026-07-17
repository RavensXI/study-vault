# -*- coding: utf-8 -*-
import json, io

live = json.load(io.open("_rp01_live2.json", encoding="utf-8"))
pd = live  # mutate in place

# --- method_card: remove em dash, keep slim ---
mc = pd["method_card"]
mc["content"] = mc["content"].replace("unitary method — find", "unitary method: find")

# worked_examples labels carry em dashes ("Step 1 — ..."); style law forbids them.
for we in pd.get("worked_examples", []):
    for st in we.get("steps", []):
        if isinstance(st.get("label"), str) and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ").replace("—", ":")

# --- per-problem hints + misconceptions (expect = distractor OPTION INDEX) ---
# keyed (tier, index) -> (hint, [misconceptions])
N = None
DATA = {
 ("gold",0): ("Add all three parts, find one part, then multiply by Ben's ratio number.",[
   {"pattern":"found_wrong_person","expect":1,"message":"£80 is Ali's share (the 2 part). Total = 9 parts, one part = £40, so Ben (3 parts) = £120."},
   {"pattern":"miscounted_parts","expect":3,"message":"You divided by 10 parts, but 2 + 3 + 4 = 9. One part = £40, so Ben = 3 × £40 = £120."}]),
 ("gold",1): ("The £40 is a difference worth 2 parts; find one part, then Beth's 3 parts.",[
   {"pattern":"used_total","expect":2,"message":"£40 is the difference, not the total. As a difference it is 2 parts, so one part = £20 and Beth = 3 × £20 = £60."},
   {"pattern":"found_amy","expect":1,"message":"£100 is Amy's share. The question asks for Beth: 3 × £20 = £60."}]),
 ("gold",2): ("The 18 is a difference worth 3 parts; find one part, then add all 11 parts.",[
   {"pattern":"only_one_group","expect":N,"message":"That is only one group. The 18 is a difference worth 3 parts, so one part = 6 and the total is 11 × 6 = 66."},
   {"pattern":"multiplied_difference","expect":3,"message":"You multiplied 18 by 3. Instead 18 is 3 parts, so one part = 18 ÷ 3 = 6 and the total is 11 × 6 = 66."}]),
 ("gold",3): ("Work out what the 4 was multiplied by to reach 12, then do the same to the 3.",[
   {"pattern":"inverted","expect":1,"message":"You matched the parts the wrong way. The 4 scales to 12 (× 3), so x = 3 × 3 = 9."},
   {"pattern":"forgot_to_divide","expect":3,"message":"You worked out 3 × 12 = 36 but did not divide by 4. x = 36 ÷ 4 = 9."}]),
 ("gold",4): ("The 12 green is 3 parts; find one part, then multiply by the total parts.",[
   {"pattern":"multiplied_given","expect":1,"message":"You multiplied 12 by 4. Instead 12 is 3 parts, so one part = 4 and the total is 10 × 4 = 40."},
   {"pattern":"found_blue","expect":2,"message":"20 is the blue share (5 × 4). The total is all parts: 10 × 4 = 40."}]),

 ("bronze",0): ("Divide both numbers by their highest common factor.",[
   {"pattern":"wrong_divisor","expect":2,"message":"You divided the two parts by different numbers. Divide both by the HCF, 5: 15 ÷ 5 = 3 and 25 ÷ 5 = 5, giving 3 : 5."},
   {"pattern":"reversed","expect":1,"message":"You reversed the order. 15 comes first, so the answer is 3 : 5, not 5 : 3."}]),
 ("bronze",1): ("Find the largest number that divides into both 18 and 12.",[
   {"pattern":"not_fully_simplified","expect":1,"message":"6 : 4 is not fully simplified. The HCF of 18 and 12 is 6: 18 ÷ 6 = 3 and 12 ÷ 6 = 2, giving 3 : 2."},
   {"pattern":"reversed","expect":3,"message":"You reversed the order. 18 comes before 12, so the answer is 3 : 2, not 2 : 3."}]),
 ("bronze",2): ("Add the parts, divide £40 by the total, then multiply by the smaller ratio number.",[
   {"pattern":"wrong_share","expect":2,"message":"£30 is the larger share (3 parts). The smaller share is 1 part: £40 ÷ 4 = £10."},
   {"pattern":"halved","expect":1,"message":"Do not split in half. Total parts = 1 + 3 = 4, so one part = £40 ÷ 4 = £10."}]),
 ("bronze",3): ("Add the parts, divide 60 by the total, then multiply by the second ratio number.",[
   {"pattern":"wrong_share","expect":0,"message":"24 is the first person's share (2 parts). The second person gets 3 parts: 3 × 12 = 36."},
   {"pattern":"halved","expect":2,"message":"Do not halve. Total parts = 5, so one part = 60 ÷ 5 = 12 and the second person gets 3 × 12 = 36."}]),
 ("bronze",4): ("Convert to the same units first, then simplify by the highest common factor.",[
   {"pattern":"different_units","expect":1,"message":"Convert to the same units first. 1 litre = 1000 ml, so it is 400 : 1000, which simplifies to 2 : 5."},
   {"pattern":"not_simplified","expect":2,"message":"4 : 10 still simplifies. Divide both parts by 200 to reach 2 : 5."}]),
 ("bronze",5): ("Add the parts, divide £80 by the total, then multiply by the larger ratio number.",[
   {"pattern":"wrong_share","expect":1,"message":"£20 is the smaller share (1 part). The larger share is 3 parts: 3 × £20 = £60."},
   {"pattern":"halved","expect":2,"message":"Do not split in half. Total parts = 4, so one part = £20 and the larger share is 3 × £20 = £60."}]),
 ("bronze",6): ("Divide all three numbers by their highest common factor.",[
   {"pattern":"not_fully_simplified","expect":1,"message":"9 : 6 : 3 still simplifies (all divide by 3). The HCF of 45, 30 and 15 is 15, giving 3 : 2 : 1."},
   {"pattern":"not_started","expect":3,"message":"This is not simplified. Divide all three parts by their HCF, 15, to get 3 : 2 : 1."}]),
 ("bronze",7): ("Find the multiplier by dividing 300 by 5, then multiply by the sugar ratio number.",[
   {"pattern":"divided_wrong","expect":1,"message":"You divided 300 by 2. First find the multiplier: 300 ÷ 5 = 60, then sugar = 2 × 60 = 120 g."},
   {"pattern":"stopped_at_one_part","expect":3,"message":"60 g is one part (300 ÷ 5). Sugar is 2 parts: 2 × 60 = 120 g."}]),

 ("silver",0): ("Find one part first, then note the difference is just one part.",[
   {"pattern":"found_a_share","expect":2,"message":"£150 is the second person's whole share. The question asks how much more, which is 5 − 4 = 1 part = £30."},
   {"pattern":"wrong_total_parts","expect":1,"message":"You divided by 5, but total parts = 4 + 5 = 9. One part = £270 ÷ 9 = £30, and that is the 1-part difference."}]),
 ("silver",1): ("The 15 boys are 3 parts; find one part, then add all 8 parts.",[
   {"pattern":"found_girls_only","expect":1,"message":"25 is just the girls. Add the boys: 15 + 25 = 40, or 8 parts × 5 = 40."},
   {"pattern":"miscounted_parts","expect":3,"message":"Total parts = 3 + 5 = 8, not 7. One part = 5, so the total is 8 × 5 = 40."}]),
 ("silver",2): ("Multiply 8 by the scale for centimetres, then convert to kilometres.",[
   {"pattern":"stopped_at_metres","expect":3,"message":"8 × 25 000 = 200 000 cm. Divide by 100 000 to get km: 200 000 ÷ 100 000 = 2 km, not 200."},
   {"pattern":"wrong_conversion","expect":2,"message":"There are 100 000 cm in 1 km, so 200 000 ÷ 100 000 = 2 km. Dividing by 10 000 gives 20 by mistake."}]),
 ("silver",3): ("Add the parts, find one part of 2 litres, then multiply by the blue ratio number.",[
   {"pattern":"found_red","expect":1,"message":"0.6 litres is the red (3 parts). Blue is 7 parts: 7 × 0.2 = 1.4 litres."},
   {"pattern":"halved","expect":2,"message":"Do not halve. Total parts = 10, so one part = 2 ÷ 10 = 0.2 and blue = 7 × 0.2 = 1.4 litres."}]),
 ("silver",4): ("Find the cost of one book, then multiply by 8.",[
   {"pattern":"scaled_to_ten","expect":1,"message":"£85 is the cost of 10 books (42.50 × 2). One book = £42.50 ÷ 5 = £8.50, so 8 books = 8 × £8.50 = £68."},
   {"pattern":"added_instead","expect":N,"message":"Do not add on to £42.50. Find one book first: £42.50 ÷ 5 = £8.50, then 8 × £8.50 = £68."}]),
 ("silver",5): ("Add the parts, divide 35 by the total, then multiply by the sand ratio number.",[
   {"pattern":"found_cement","expect":1,"message":"5 kg is one part (the cement). Sand is 2 parts: 2 × 5 = 10 kg."},
   {"pattern":"forgot_total","expect":3,"message":"Total parts = 1 + 2 + 4 = 7, so one part = 5 kg and sand = 2 × 5 = 10 kg."}]),
 ("silver",6): ("Add the parts, divide 750 by the total, then multiply by the cordial ratio number.",[
   {"pattern":"found_water","expect":3,"message":"600 ml is the water (4 parts). Cordial is 1 part: 750 ÷ 5 = 150 ml."},
   {"pattern":"divided_by_4","expect":1,"message":"You divided by 4. Total parts = 1 + 4 = 5, so cordial = 750 ÷ 5 = 150 ml."}]),
}

pb = pd["problem_bank"]
for (tier, idx), (hint, miscs) in DATA.items():
    prob = pb[tier][idx]
    prob["hint"] = hint
    prob["misconceptions"] = miscs

# --- tier_guides ---
pd["tier_guides"] = {
 "bronze": {
  "title": "Bronze: simplify and share",
  "steps": [
   "A ratio like \\(3 : 2\\) splits something into equal parts. Simplify first where you can by dividing both parts by their highest common factor.",
   "To <strong>share a total</strong>: add the parts to find the number of shares, divide the total by that to find <strong>one part</strong>, then multiply one part by each ratio number.",
   "Always check that the shares add back up to the original total."
  ],
  "example": {
   "question": "Share £54 in the ratio 4 : 5",
   "steps": [
    {"label":"Add parts","content":"<p>\\(4 + 5 = 9\\) parts</p>"},
    {"label":"One part","content":"<p>\\(54 \\div 9 = £6\\)</p>"},
    {"label":"Shares","content":"<p>\\(4 \\times 6 = £24\\) and \\(5 \\times 6 = £30\\)</p>"},
    {"label":"Check","content":"<p>\\(24 + 30 = £54\\) ✔</p>"},
    {"label":"Answer","content":"<p>\\(£24\\) and \\(£30\\)</p>","isAnswer":True,"is_answer":True}
   ]
  }
 },
 "silver": {
  "title": "Silver: scale from one known part",
  "steps": [
   "Sometimes you are given <strong>one quantity</strong>, not the total. Find what <strong>one part</strong> is worth by dividing that quantity by its ratio number.",
   "Then multiply one part by another ratio number to get that share, or by the total parts to get the whole amount.",
   "Scale and map problems work the same way: multiply by the scale, then convert units carefully (100 cm in a metre, 100 000 cm in a kilometre)."
  ],
  "example": {
   "question": "The ratio of red to blue beads is 5 : 2. There are 30 red beads. How many blue?",
   "steps": [
    {"label":"One part","content":"<p>\\(30 \\div 5 = 6\\) beads</p>"},
    {"label":"Blue","content":"<p>\\(2 \\times 6 = 12\\) beads</p>"},
    {"label":"Check","content":"<p>\\(12 \\div 6 = 2\\), matching the blue ratio part ✔</p>"},
    {"label":"Answer","content":"<p>\\(12\\) blue beads</p>","isAnswer":True,"is_answer":True}
   ]
  }
 },
 "gold": {
  "title": "Gold: reason from a difference or one share",
  "steps": [
   "In gold problems the number given is often a <strong>difference</strong> between shares, or a single share, or the total. Decide which before doing anything.",
   "For a difference, the parts differ too: divide the amount by the <strong>difference in parts</strong> to find one part. For one share, divide by that share's parts.",
   "Once one part is known, multiply to reach whatever the question asks, then check your answer fits the wording."
  ],
  "example": {
   "question": "Anna and Beth share money in the ratio 7 : 5. Anna gets £16 more than Beth. How much does Beth get?",
   "steps": [
    {"label":"Difference in parts","content":"<p>\\(7 - 5 = 2\\) parts represent £16</p>"},
    {"label":"One part","content":"<p>\\(16 \\div 2 = £8\\)</p>"},
    {"label":"Beth","content":"<p>\\(5 \\times 8 = £40\\)</p>"},
    {"label":"Check","content":"<p>Anna \\(7 \\times 8 = £56\\), and \\(56 - 40 = £16\\) ✔</p>"},
    {"label":"Answer","content":"<p>\\(£40\\)</p>","isAnswer":True,"is_answer":True}
   ]
  }
 }
}

# --- guided (opener + teach) ---
pd["guided"] = {
 "opener": {
  "label": "Before any method",
  "display": "Priya and Sam share 15 stickers.<br>For every 2 stickers Priya takes, Sam takes 3.",
  "steps": [
   {"say":"A sharing puzzle. No method needed yet, just count.",
    "pre":"In one fair round Priya takes 2 and Sam takes 3. How many stickers is that altogether? ","post":"","answer":5,
    "hint":"Just add 2 and 3."},
   {"say":"So the 15 stickers get handed out in equal rounds of 5.",
    "pre":"How many rounds of 5 are in 15 stickers? ","post":"","answer":3,
    "hint":"How many 5s make 15?"},
   {"say":"Priya takes 2 stickers every round.",
    "pre":"Over 3 rounds Priya gets 2 × 3 = ","post":"","answer":6,
    "hint":"2 stickers a round, for 3 rounds."},
   {"say":"You just shared in the ratio \\(2 : 3\\) with no algebra. Adding the parts (2 + 3 = 5), finding one round, then scaling up is the whole method. Priya gets 6, Sam gets 9, and \\(6 + 9 = 15\\)."}
  ]
 },
 "teach": {
  "bronze": {
   "display": "Share £48 in the ratio \\(5 : 1\\)",
   "label": "Together: your first share",
   "steps": [
    {"say":"Sharing has three moves: add the parts, find one part, then multiply. Watch.",
     "pre":"Add the parts: 5 + 1 = ","post":"","answer":6,"hint":"Add the two ratio numbers."},
    {"pre":"One part = 48 ÷ 6 = £","post":"","answer":8,"hint":"Divide the money by the total parts.","done":"One part is worth £8."},
    {"say":"Now scale each share up from one part.",
     "pre":"Larger share: 5 × 8 = £","post":"","answer":40,"hint":"Multiply one part by 5."},
    {"pre":"Smaller share: 1 × 8 = £","post":"","answer":8,"hint":"Multiply one part by 1."},
    {"say":"Check they add back to the total.",
     "pre":"40 + 8 = £","post":"","answer":48,"hint":"The shares must total £48.","done":"They add to £48, so add, divide, multiply is the whole method."}
   ]
  },
  "silver": {
   "display": "The ratio of red to green counters is \\(3 : 8\\). There are 12 red counters. How many green?",
   "label": "Together: the silver move",
   "steps": [
    {"say":"You are given one quantity, not the total. Find one part from it first.",
     "pre":"Red is the 3 part and equals 12, so one part = 12 ÷ 3 = ","post":"","answer":4,"hint":"Divide the known quantity by its ratio number."},
    {"say":"Now every part is worth 4.",
     "pre":"Green is the 8 part: 8 × 4 = ","post":"","answer":32,"hint":"Multiply one part by 8.","done":"Knowing one part unlocks every other quantity."},
    {"pre":"How many counters altogether? Parts = 3 + 8 = ","post":"","answer":11,"hint":"Add the two ratio numbers."},
    {"pre":"Total counters = 11 × 4 = ","post":"","answer":44,"hint":"Multiply total parts by one part."},
    {"say":"Check the two shares add to the total.",
     "pre":"12 + 32 = ","post":"","answer":44,"hint":"It should match the total.","done":"12 + 32 = 44 matches, so one part = 4 was right."}
   ]
  },
  "gold": {
   "display": "Lena and Max share money in the ratio \\(8 : 5\\). Lena gets £24 more than Max. How much does Max get?",
   "label": "Together: the gold move",
   "steps": [
    {"say":"The £24 is a difference, not a total. The parts differ too.",
     "pre":"Difference in parts: 8 − 5 = ","post":"","answer":3,"hint":"Subtract the smaller ratio number from the larger."},
    {"say":"That 3-part gap is worth the £24.",
     "pre":"One part = 24 ÷ 3 = £","post":"","answer":8,"hint":"Divide the money gap by the part gap.","done":"The trick is spotting that £24 is a difference, not a total."},
    {"pre":"Max has the 5 part: 5 × 8 = £","post":"","answer":40,"hint":"Multiply one part by Max's ratio number."},
    {"pre":"Lena has the 8 part: 8 × 8 = £","post":"","answer":64,"hint":"Multiply one part by 8."},
    {"say":"Check the gap between them.",
     "pre":"64 − 40 = £","post":"","answer":24,"hint":"It should equal the £24 difference.","done":"The gap is £24, so Max gets £40."}
   ]
  }
 }
}

with io.open("lesson_maths-eduqas_ratio-proportion-L01.json","w",encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("written shard. top keys:", list(pd.keys()))
