# -*- coding: utf-8 -*-
import json, io

src = json.load(io.open("_pd_live.json", encoding="utf-8"))
MINUS = "−"   # minus sign
ARROW = "→"   # right arrow

def alpha_mass_walk(A):
    return [
        {"say": "Alpha decay throws out a helium nucleus. On the mass line (the top numbers) that helium nucleus carries away 4."},
        {"pre": "Mass number of the alpha particle = ", "post": "", "answer": 4,
         "hint": "A helium nucleus is 2 protons plus 2 neutrons, so 4."},
        {"pre": "So the daughter's mass number = " + str(A) + " " + MINUS + " 4 = ", "post": "", "answer": A - 4, "phase": "substitute",
         "hint": "Take 4 off the parent's mass number."},
        {"pre": "Check the mass line balances: daughter + alpha = " + str(A - 4) + " + 4 = ", "post": "", "answer": A,
         "hint": "Add them back; it should return to " + str(A) + ".",
         "done": "Back to " + str(A) + ", so the mass numbers balance. Daughter mass number = " + str(A - 4) + "."},
    ]

def alpha_atomic_walk(A, Z):
    return [
        {"say": "Alpha decay throws out a helium nucleus. On the atomic line (the bottom numbers, the proton count) that helium nucleus carries away 2."},
        {"pre": "Atomic number of the alpha particle (its protons) = ", "post": "", "answer": 2,
         "hint": "A helium nucleus has 2 protons."},
        {"pre": "So the daughter's atomic number = " + str(Z) + " " + MINUS + " 2 = ", "post": "", "answer": Z - 2, "phase": "substitute",
         "hint": "Take 2 off the parent's atomic number."},
        {"pre": "Check the atomic line: daughter + alpha = " + str(Z - 2) + " + 2 = ", "post": "", "answer": Z,
         "hint": "Add them back to " + str(Z) + ".",
         "done": "Balances at " + str(Z) + ". Daughter atomic number = " + str(Z - 2) + "."},
    ]

def beta_atomic_walk(Z):
    return [
        {"say": "In beta decay a neutron turns into a proton, so the nucleus gains one proton. The emitted beta particle counts as " + MINUS + "1 on the atomic line."},
        {"pre": "Number of protons gained in beta decay = ", "post": "", "answer": 1,
         "hint": "One neutron becomes one proton, so +1 proton."},
        {"pre": "New atomic number = " + str(Z) + " + 1 = ", "post": "", "answer": Z + 1, "phase": "substitute",
         "hint": "Add 1 to the parent's atomic number."},
        {"pre": "Check the atomic line balances: daughter + beta particle = " + str(Z + 1) + " + (" + MINUS + "1) = ", "post": "", "answer": Z,
         "hint": "The beta particle counts as " + MINUS + "1, so it returns to " + str(Z) + ".",
         "done": "Balances at " + str(Z) + ". Daughter atomic number = " + str(Z + 1) + "."},
    ]

pb = src["problem_bank"]

# ---- BRONZE ----
b = pb["bronze"]
b[0]["guided_steps"] = alpha_mass_walk(226)
b[0]["misconceptions"][0]["expect"] = 224
b[0]["misconceptions"][1]["expect"] = 226

b[1]["guided_steps"] = alpha_atomic_walk(226, 88)
b[1]["misconceptions"][0]["expect"] = 84

b[2]["guided_steps"] = beta_atomic_walk(6)
b[2]["misconceptions"][0]["expect"] = 5
b[2]["misconceptions"][1]["expect"] = 4

b[3]["guided_steps"] = [
    {"say": "Each half-life halves the activity. Do it four times."},
    {"pre": "After 1 half-life: 800 ÷ 2 = ", "post": "", "answer": 400, "hint": "Half of 800."},
    {"pre": "After 2: 400 ÷ 2 = ", "post": "", "answer": 200, "hint": "Half of 400."},
    {"pre": "After 3: 200 ÷ 2 = ", "post": "", "answer": 100, "phase": "substitute", "hint": "Half of 200."},
    {"pre": "After 4: 100 ÷ 2 = ", "post": "", "answer": 50, "hint": "Half of 100.",
     "done": "Four halvings from 800: 50 Bq."},
    {"pre": "Check by doubling back four times: 50 × 16 = ", "post": "", "answer": 800,
     "hint": "16 is 2 to the power 4.", "done": "Back to 800 Bq, so the answer is 50 Bq."},
]
b[3]["misconceptions"][0]["expect"] = 100

b[4]["guided_steps"] = [
    {"say": "Each half-life halves the activity. Do it three times."},
    {"pre": "After 1 half-life: 2000 ÷ 2 = ", "post": "", "answer": 1000, "hint": "Half of 2000."},
    {"pre": "After 2: 1000 ÷ 2 = ", "post": "", "answer": 500, "phase": "substitute", "hint": "Half of 1000."},
    {"pre": "After 3: 500 ÷ 2 = ", "post": "", "answer": 250, "hint": "Half of 500.",
     "done": "Three halvings from 2000: 250 Bq."},
    {"pre": "Check by doubling back three times: 250 × 8 = ", "post": "", "answer": 2000,
     "hint": "8 is 2 to the power 3.", "done": "Back to 2000 Bq, so the answer is 250 Bq."},
]
b[4]["misconceptions"][0]["expect"] = 500

b[5]["guided_steps"] = alpha_mass_walk(238)
b[5]["misconceptions"][0]["expect"] = 236

b[6]["guided_steps"] = beta_atomic_walk(82)
b[6]["misconceptions"][0]["expect"] = 81

b[7]["guided_steps"] = beta_atomic_walk(27)
b[7]["misconceptions"][0]["expect"] = 26
b[7]["misconceptions"][1]["expect"] = 25

# ---- SILVER ----
s = pb["silver"]
s[0]["guided_steps"] = [
    {"say": "Each half-life halves the activity. Count the halvings from 6400 down to 400."},
    {"pre": "Halve once: 6400 ÷ 2 = ", "post": "", "answer": 3200, "hint": "Half of 6400."},
    {"pre": "3200 ÷ 2 = ", "post": "", "answer": 1600, "hint": "Half of 3200."},
    {"pre": "1600 ÷ 2 = ", "post": "", "answer": 800, "hint": "Half of 1600."},
    {"pre": "800 ÷ 2 = ", "post": "", "answer": 400, "phase": "substitute", "hint": "Half of 800.",
     "done": "That is four halvings to reach 400."},
    {"pre": "Half-life = total time ÷ halvings = 20 ÷ 4 = ", "post": "", "answer": 5,
     "hint": "Divide 20 minutes by the 4 halvings."},
    {"pre": "Check: 4 half-lives × 5 = ", "post": "", "answer": 20,
     "hint": "Multiply back.", "done": "Matches the 20 minutes given. Half-life = 5 minutes."},
]
s[0]["misconceptions"][0]["expect"] = 4
s[0]["misconceptions"][1]["expect"] = 1.25

s[1]["guided_steps"] = [
    {"say": "Count the halvings from 1200 down to 150."},
    {"pre": "Halve once: 1200 ÷ 2 = ", "post": "", "answer": 600, "hint": "Half of 1200."},
    {"pre": "600 ÷ 2 = ", "post": "", "answer": 300, "hint": "Half of 600."},
    {"pre": "300 ÷ 2 = ", "post": "", "answer": 150, "phase": "substitute", "hint": "Half of 300.",
     "done": "Three halvings to reach 150."},
    {"pre": "Half-life = 30 ÷ 3 = ", "post": "", "answer": 10, "hint": "Divide 30 minutes by 3 halvings."},
    {"pre": "Check: 3 × 10 = ", "post": "", "answer": 30,
     "hint": "Multiply back.", "done": "Matches the 30 minutes. Half-life = 10 minutes."},
]
s[1]["misconceptions"][0]["expect"] = 7.5

s[2]["guided_steps"] = alpha_mass_walk(241)
s[2]["misconceptions"][0]["expect"] = 239

s[3]["guided_steps"] = beta_atomic_walk(38)
s[3]["misconceptions"][0]["expect"] = 37

s[4]["guided_steps"] = [
    {"say": "First find how many half-lives fit in the time, then halve the mass that many times."},
    {"pre": "Number of half-lives = 15 ÷ 3 = ", "post": "", "answer": 5, "hint": "Total time ÷ half-life."},
    {"pre": "Halve once: 50 ÷ 2 = ", "post": "", "answer": 25, "phase": "substitute", "hint": "Half of 50."},
    {"pre": "25 ÷ 2 = ", "post": "", "answer": 12.5, "hint": "Half of 25."},
    {"pre": "12.5 ÷ 2 = ", "post": "", "answer": 6.25, "hint": "Half of 12.5."},
    {"pre": "6.25 ÷ 2 = ", "post": "", "answer": 3.125, "hint": "Half of 6.25."},
    {"pre": "3.125 ÷ 2 = ", "post": "", "answer": 1.5625, "hint": "Half of 3.125.",
     "done": "Five halvings from 50 g: 1.5625 g."},
]
s[4]["misconceptions"][0]["expect"] = 3.125
s[4]["misconceptions"][1]["expect"] = None

s[5]["guided_steps"] = alpha_mass_walk(210)
s[5]["misconceptions"][0]["expect"] = 208

# ---- GOLD ----
g = pb["gold"]
g[0]["hint"] = "Count how many times the activity halves, then divide the time by that count."
g[0]["guided_steps"] = [
    {"say": "Each half-life halves the activity. Count the halvings from 5000 down to 312.5."},
    {"pre": "Halve once: 5000 ÷ 2 = ", "post": "", "answer": 2500, "hint": "Half of 5000."},
    {"pre": "2500 ÷ 2 = ", "post": "", "answer": 1250, "hint": "Half of 2500."},
    {"pre": "1250 ÷ 2 = ", "post": "", "answer": 625, "hint": "Half of 1250."},
    {"pre": "625 ÷ 2 = ", "post": "", "answer": 312.5, "phase": "substitute", "hint": "Half of 625.",
     "done": "Reached 312.5 after four halvings."},
    {"pre": "Four halvings, so half-life = 52 ÷ 4 = ", "post": "", "answer": 13,
     "hint": "Divide 52 days by the 4 halvings."},
    {"pre": "Check: 4 × 13 = ", "post": "", "answer": 52,
     "hint": "Multiply back.", "done": "Matches the 52 days. Half-life = 13 days."},
]
g[0]["misconceptions"][0]["expect"] = 10.4
g[0]["misconceptions"][1]["expect"] = 3.25

g[1]["hint"] = "Divide the total time by the half-life to get n, then the denominator is 2 to the power n."
g[1]["guided_steps"] = [
    {"say": "The fraction left is one half to the power of the number of half-lives. Find that number first, then the denominator."},
    {"pre": "Number of half-lives = 56 ÷ 8 = ", "post": "", "answer": 7, "hint": "Total time ÷ half-life."},
    {"pre": "The denominator doubles each half-life. Start at 1 and double seven times: 1, 2, 4, 8, 16, 32, 64, then ",
     "post": "", "answer": 128, "phase": "substitute", "hint": "Double 64.",
     "done": "So the fraction remaining is 1/128."},
    {"pre": "Check: the denominator 128 times the fraction should give one whole sample: 128 × (1/128) = ",
     "post": "", "answer": 1, "hint": "A number over itself is 1.",
     "done": "One whole sample accounted for. Denominator = 128."},
]
g[1]["misconceptions"][0]["expect"] = 64
g[1]["misconceptions"][1]["expect"] = 14

# gold[2]: convert to multiple_choice (string answer cannot validate)
g[2]["display"] = "Thorium-234 (atomic number 90) decays to protactinium-234 (atomic number 91). What type of decay is this?"
g[2]["input_type"] = "multiple_choice"
g[2]["options"] = ["Alpha decay", "Beta decay"]
g[2]["solutions"] = [1]
g[2]["calculator"] = False
g[2]["hint"] = "Compare the atomic numbers: did the bottom number go up or down?"
g[2].pop("guided_steps", None)
g[2]["misconceptions"] = [{
    "check": "common", "pattern": "wrong_type", "expect": None,
    "message": "The mass number stays at 234 and the atomic number rises from 90 to 91 (up by 1). A rise of 1 in the atomic number with no change in mass is beta decay: a neutron has turned into a proton."
}]

g[3]["hint"] = "Do the beta decay first, then apply alpha to the daughter nucleus."
g[3]["guided_steps"] = [
    {"say": "Two decays in a row. Apply beta first, then alpha to the new nucleus."},
    {"pre": "Beta decay leaves the mass number unchanged, so after beta the mass is still ", "post": "", "answer": 24,
     "hint": "Beta decay does not change the mass number."},
    {"pre": "Now alpha decay on that nucleus: mass drops by 4. 24 " + MINUS + " 4 = ", "post": "", "answer": 20, "phase": "substitute",
     "hint": "Take 4 off.", "done": "Final mass number = 20."},
    {"pre": "Track the atomic number too: beta 11 " + ARROW + " 12, then alpha 12 " + MINUS + " 2 = ", "post": "", "answer": 10,
     "hint": "Alpha drops the atomic number by 2.",
     "done": "Neon-20: mass number 20, atomic number 10. Both lines balance."},
]
g[3]["misconceptions"][0]["expect"] = 24
g[3]["misconceptions"][1]["expect"] = None

g[4]["hint"] = "Convert the time to minutes first, then count the halvings."
g[4]["guided_steps"] = [
    {"say": "The count rate halves each half-life. But the time is in hours and the answer is wanted in minutes, so convert first."},
    {"pre": "Convert the time to minutes: 2 hours = 2 × 60 = ", "post": "", "answer": 120, "hint": "60 minutes in an hour."},
    {"pre": "Now count the halvings. Halve once: 480 ÷ 2 = ", "post": "", "answer": 240, "hint": "Half of 480."},
    {"pre": "240 ÷ 2 = ", "post": "", "answer": 120, "hint": "Half of 240."},
    {"pre": "120 ÷ 2 = ", "post": "", "answer": 60, "hint": "Half of 120."},
    {"pre": "60 ÷ 2 = ", "post": "", "answer": 30, "phase": "substitute", "hint": "Half of 60.",
     "done": "Four halvings to reach 30."},
    {"pre": "Half-life = 120 ÷ 4 = ", "post": "", "answer": 30, "hint": "Divide 120 minutes by 4 halvings."},
    {"pre": "Check: 4 × 30 = ", "post": "", "answer": 120,
     "hint": "Multiply back.", "done": "Matches 120 minutes. Half-life = 30 minutes."},
]
g[4]["misconceptions"][0]["expect"] = 24
g[4]["misconceptions"][1]["expect"] = 0.5

g[5]["hint"] = "Beta decay raises the atomic number by 1."
g[5]["guided_steps"] = beta_atomic_walk(53)
g[5]["misconceptions"][0]["expect"] = 52

pb["bronze_description"] = "One decay, or a whole number of half-lives, with the values ready to use."
pb["silver_description"] = "Count the halvings, rearrange for the half-life, or convert the time unit first."
pb["gold_description"] = "Chain two decays, work with fractions remaining, or find a half-life from awkward numbers."

# ---- tier_guides ----
src["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one decay, read off the change",
        "steps": [
            "Alpha decay: mass number drops by 4, atomic number drops by 2.",
            "Beta decay: mass number stays the same, atomic number rises by 1.",
            "For activity, halve the number once for each half-life.",
        ],
        "example": {
            "question": "Radon-220 (atomic number 86) undergoes alpha decay. What is the mass number of the daughter nucleus?",
            "steps": [
                {"label": "Alpha rule", "content": "Alpha decay drops the mass number by 4."},
                {"label": "Calculate", "content": "220 " + MINUS + " 4 = 216"},
                {"label": "Check", "content": "216 + 4 = 220, so the mass line balances."},
                {"label": "Answer", "content": "Mass number = <strong>216</strong>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: count or convert first",
        "steps": [
            "Count how many times you halve from the start value to the end value.",
            "Half-life = total time ÷ number of halvings.",
            "If the time is in hours but the answer wants minutes, convert first: 1 hour = 60 minutes.",
        ],
        "example": {
            "question": "A source falls from 6400 Bq to 800 Bq in 24 minutes. Find the half-life.",
            "steps": [
                {"label": "Count halvings", "content": "6400 " + ARROW + " 3200 " + ARROW + " 1600 " + ARROW + " 800 is 3 halvings."},
                {"label": "Divide", "content": "24 ÷ 3 = 8"},
                {"label": "Check", "content": "3 × 8 = 24 minutes, which matches."},
                {"label": "Answer", "content": "Half-life = <strong>8 minutes</strong>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: chain the steps",
        "steps": [
            "Two decays in a row: apply the first, then apply the second to the new nucleus.",
            "Fraction remaining after n half-lives = one half to the power n, so the denominator is 2 to the power n.",
            "Finish by checking the mass and atomic numbers balance on both sides.",
        ],
        "example": {
            "question": "A sample drops to one eighth of its starting activity. How many half-lives have passed?",
            "steps": [
                {"label": "Write as a power", "content": "One eighth = one half cubed."},
                {"label": "Read off n", "content": "The power is 3, so 3 half-lives."},
                {"label": "Check", "content": "1 " + ARROW + " 1/2 " + ARROW + " 1/4 " + ARROW + " 1/8 is 3 steps."},
                {"label": "Answer", "content": "<strong>3 half-lives</strong>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---- guided (opener + teach) ----
src["guided"] = {
    "opener": {
        "display": "You have 800 sweets in a jar. Every day, half of whatever is left vanishes. Not 100 a day: HALF of what remains.",
        "steps": [
            {"pre": "How many are left after day 1? 800 ÷ 2 = ", "post": "", "answer": 400, "hint": "Half of 800."},
            {"pre": "And after day 2? 400 ÷ 2 = ", "post": "", "answer": 200, "hint": "Half of 400."},
            {"pre": "After day 3? 200 ÷ 2 = ", "post": "", "answer": 100, "hint": "Half of 200.",
             "done": "Notice it never quite hits zero: it just keeps halving."},
            {"say": "You just did <strong>half-life</strong>. Radioactive atoms do not disappear at a steady rate, they halve. Each 'day' here is one half-life. Count the halvings and you can find how long each one takes, or how much is left."},
        ],
    },
    "teach": {
        "bronze": {
            "display": "Radon-222 (atomic number 86) undergoes alpha decay. Find the daughter's mass number and atomic number.",
            "steps": [
                {"say": "Alpha decay emits a helium nucleus: 4 on the mass line, 2 on the atomic line."},
                {"pre": "Alpha particle mass number = ", "post": "", "answer": 4, "hint": "Helium nucleus mass is 4."},
                {"pre": "Daughter mass number = 222 " + MINUS + " 4 = ", "post": "", "answer": 218, "hint": "Take 4 off 222."},
                {"pre": "Alpha particle atomic number = ", "post": "", "answer": 2, "hint": "Helium has 2 protons."},
                {"pre": "Daughter atomic number = 86 " + MINUS + " 2 = ", "post": "", "answer": 84, "hint": "Take 2 off 86."},
                {"pre": "Check the mass line: 218 + 4 = ", "post": "", "answer": 222,
                 "hint": "Add the daughter and the alpha particle.",
                 "done": "Balances at 222. The daughter is polonium-218."},
            ],
        },
        "silver": {
            "display": "A source falls from 3200 Bq to 200 Bq in 16 minutes. Find the half-life.",
            "steps": [
                {"say": "Count how many times the activity halves from 3200 down to 200."},
                {"pre": "3200 ÷ 2 = ", "post": "", "answer": 1600, "hint": "Half of 3200."},
                {"pre": "1600 ÷ 2 = ", "post": "", "answer": 800, "hint": "Half of 1600."},
                {"pre": "800 ÷ 2 = ", "post": "", "answer": 400, "hint": "Half of 800."},
                {"pre": "400 ÷ 2 = ", "post": "", "answer": 200, "hint": "Half of 400.",
                 "done": "Four halvings to reach 200."},
                {"pre": "Half-life = 16 ÷ 4 = ", "post": "", "answer": 4, "hint": "Divide 16 minutes by 4 halvings.",
                 "done": "Half-life = 4 minutes."},
            ],
        },
        "gold": {
            "display": "Uranium-238 (atomic number 92) decays by alpha, then that daughter decays by beta. Find the final atomic number and mass number.",
            "steps": [
                {"say": "Apply the first decay, then the second to the new nucleus."},
                {"pre": "Alpha decay: atomic number 92 " + MINUS + " 2 = ", "post": "", "answer": 90, "hint": "Alpha drops atomic number by 2."},
                {"pre": "Alpha also drops the mass: 238 " + MINUS + " 4 = ", "post": "", "answer": 234, "hint": "Alpha drops mass by 4."},
                {"pre": "That daughter is thorium-234. Now beta decay: atomic number 90 + 1 = ", "post": "", "answer": 91, "hint": "Beta raises atomic number by 1."},
                {"pre": "Beta leaves the mass unchanged, so the final mass number = ", "post": "", "answer": 234, "hint": "Beta does not change mass.",
                 "done": "Protactinium-234: atomic number 91, mass number 234."},
            ],
        },
    },
}

# ---- method_card (slim, no em dash) ----
src["method_card"]["title"] = "Nuclear Equations and Half-Life"
src["method_card"]["steps"] = [
    "For nuclear equations: check both the mass numbers and the atomic numbers balance on each side.",
    "Alpha: mass " + MINUS + "4, atomic number " + MINUS + "2. Beta: mass same, atomic number +1.",
    "For half-life: keep halving the value until you reach the target, and count the halvings.",
    "Half-life = total time ÷ number of halvings.",
]
src["method_card"]["content"] = (
    "<p>Two skills, both really just <strong>counting</strong>.</p>"
    "<p><strong>Nuclear equations:</strong> the mass numbers (top) and atomic numbers (bottom) must balance on both sides. "
    "Alpha decay drops the mass number by 4 and the atomic number by 2. "
    "Beta decay leaves the mass number the same and raises the atomic number by 1.</p>"
    "<p><strong>Half-life:</strong> the time for the activity to halve. Count how many times you halve from the start value to the end value. "
    "Each halving is one half-life, so half-life = total time ÷ number of halvings. "
    "After \\(n\\) half-lives the fraction left is \\(\\left(\\tfrac{1}{2}\\right)^n\\).</p>"
)

src["exam_context"]["frequency"] = "High: nuclear equations and half-life appear on almost every Paper 1"

for we in src.get("worked_examples", []):
    for st in we.get("steps", []):
        if "label" in st and "—" in st["label"]:
            st["label"] = st["label"].replace(" — ", ": ")

with io.open("lesson_higher-calculations-L05@b2761124fc.json", "w", encoding="utf-8") as f:
    json.dump(src, f, indent=1, ensure_ascii=False)
print("written")
