# -*- coding: utf-8 -*-
import json, io, re

pd = json.load(io.open("_canon_09acbba067.json", encoding="utf-8"))

pd["method_card"] = {
    "title": "Half-Life and Nuclear Equations",
    "steps": [
        "Half-life: find n = total time ÷ half-life, then halve the activity n times (never divide by n).",
        "Going back in time, double the activity once for each half-life instead of halving.",
        "Alpha decay: mass number − 4, atomic number − 2. The alpha particle is \\(^{4}_{2}\\text{He}\\).",
        "Beta decay: mass number unchanged, atomic number + 1. The beta particle is an electron.",
    ],
    "content": "<p><strong>Half-life</strong> is the time for the activity of a source to halve. To find the activity after a time t, work out n = t ÷ half-life, then halve the starting activity n times. Never divide the activity by n itself.</p><p>To go backwards in time, double the activity once for each half-life instead of halving.</p><p><strong>Nuclear equations</strong> must balance: the mass numbers on each side must add up, and so must the atomic numbers. Alpha decay drops the mass number by 4 and the atomic number by 2. Beta decay leaves the mass number the same and raises the atomic number by 1. Check whether your board gives you the particle symbols.</p>",
}

pb = pd["problem_bank"]
pb["bronze_description"] = "One half-life at a time: halve the activity, or recall the alpha and beta decay rules."
pb["silver_description"] = "Find the number of half-lives first (n = time ÷ half-life), then halve that many times."
pb["gold_description"] = "Multi-step problems: work backwards in time, find an unknown time, or balance a decay."

def setp(prob, hint, mis_expect, mis_msg, mis_pattern, steps):
    prob["hint"] = hint
    prob["misconceptions"] = [{
        "pattern": mis_pattern,
        "message": mis_msg,
        "expect": mis_expect,
        "note": "derived by committing the error",
    }]
    prob["guided_steps"] = steps

b = pb["bronze"]

setp(b[0],
     "One half-life means halve the activity once.",
     800, "One half-life halves the activity: 400 ÷ 2 = 200 Bq. Doubling to 800 goes the wrong way.", "inverse_error",
     [
        {"say": "One half-life is the time for the activity to halve. Start at 400 Bq."},
        {"pre": "How many times does the sample halve here? Number of half-lives = ", "post": "", "answer": 1, "hint": "The question says after one half-life."},
        {"phase": "substitute", "pre": "Halve once: 400 ÷ 2 = ", "post": "", "answer": 200, "hint": "Divide the activity by 2."},
        {"pre": "Check by going back up: 200 × 2 = ", "post": "", "answer": 400, "done": "Back to 400 Bq, so 200 Bq after one half-life is right.", "hint": "Doubling should return the starting activity."},
        {"say": "So the activity is <strong>200 Bq</strong>."},
     ])

setp(b[1],
     "Two half-lives: halve, then halve again.",
     800, "Two half-lives means halving twice: 1600 → 800 → 400 Bq. Stopping after one halving leaves 800.", "forgot_step",
     [
        {"say": "Two half-lives means the activity halves twice. Start at 1600 Bq."},
        {"pre": "Number of half-lives = ", "post": "", "answer": 2, "hint": "The question says after two half-lives."},
        {"phase": "substitute", "pre": "Halve once: 1600 ÷ 2 = ", "post": "", "answer": 800, "hint": "Divide by 2."},
        {"pre": "Halve again: 800 ÷ 2 = ", "post": "", "answer": 400, "done": "Two halvings done.", "hint": "Divide by 2 again."},
        {"pre": "Check: 400 × 2 × 2 = ", "post": "", "answer": 1600, "done": "Back to 1600 Bq, so 400 Bq is right.", "hint": "Doubling twice returns the start."},
        {"say": "So the activity is <strong>400 Bq</strong>."},
     ])

setp(b[2],
     "Halve three times, one step at a time.",
     200, "Three half-lives means halving three times: 800 → 400 → 200 → 100 Bq. Stopping at two halvings leaves 200.", "forgot_step",
     [
        {"say": "Three half-lives means halving three times. Start at 800 Bq."},
        {"pre": "Number of half-lives = ", "post": "", "answer": 3, "hint": "The question says after three half-lives."},
        {"phase": "substitute", "pre": "Halve once: 800 ÷ 2 = ", "post": "", "answer": 400, "hint": "Divide by 2."},
        {"pre": "Halve again: 400 ÷ 2 = ", "post": "", "answer": 200, "hint": "Divide by 2."},
        {"pre": "Halve a third time: 200 ÷ 2 = ", "post": "", "answer": 100, "done": "Three halvings done.", "hint": "Divide by 2."},
        {"pre": "Check: 100 × 2 × 2 × 2 = ", "post": "", "answer": 800, "done": "Back to 800 Bq, so 100 Bq is right.", "hint": "Doubling three times returns the start."},
        {"say": "So the activity is <strong>100 Bq</strong>."},
     ])

setp(b[3],
     "Multiply by one half for each half-life: (1/2) four times.",
     0.125, "Four half-lives multiplies the fraction by (1/2)⁴ = 1/16 = 0.0625. Writing 1 ÷ (2 × 4) = 0.125 treats the halvings as one division.", "wrong_factor",
     [
        {"say": "Each half-life leaves half as much. Start with the whole sample as a fraction: 1."},
        {"pre": "Number of half-lives = ", "post": "", "answer": 4, "hint": "The question says after four half-lives."},
        {"phase": "substitute", "pre": "After 1 half-life: 1 ÷ 2 = ", "post": "", "answer": 0.5, "hint": "Half of 1."},
        {"pre": "After 2: 0.5 ÷ 2 = ", "post": "", "answer": 0.25, "hint": "Half of 0.5."},
        {"pre": "After 3: 0.25 ÷ 2 = ", "post": "", "answer": 0.125, "hint": "Half of 0.25."},
        {"pre": "After 4: 0.125 ÷ 2 = ", "post": "", "answer": 0.0625, "done": "That is 1/16 of the original.", "hint": "Half of 0.125."},
        {"say": "So <strong>1/16 (0.0625)</strong> of the activity remains."},
     ])

setp(b[4],
     "An alpha particle is a helium-4 nucleus, \\(^{4}_{2}\\text{He}\\).",
     2, "An alpha particle carries away 4 nucleons (2 protons + 2 neutrons), so the mass number drops by 4. The atomic number is what drops by 2.", "wrong_value",
     [
        {"say": "An alpha particle is a helium nucleus, written \\(^{4}_{2}\\text{He}\\). Count what it takes away."},
        {"pre": "Protons in the alpha particle = ", "post": "", "answer": 2, "hint": "The bottom number of \\(^{4}_{2}\\text{He}\\)."},
        {"phase": "substitute", "pre": "Neutrons in the alpha particle = ", "post": "", "answer": 2, "hint": "Helium-4 has 2 protons and 2 neutrons."},
        {"pre": "Nucleons lost = protons + neutrons = 2 + 2 = ", "post": "", "answer": 4, "done": "The mass number counts nucleons, so it drops by 4.", "hint": "Add the protons and neutrons."},
        {"say": "So the mass number decreases by <strong>4</strong>."},
     ])

setp(b[5],
     "In beta decay a neutron turns into a proton.",
     2, "In beta decay a neutron becomes a proton, so the atomic number rises by 1. A change of 2 is alpha decay, not beta.", "wrong_value",
     [
        {"say": "In beta decay a neutron changes into a proton and an electron. The electron leaves as the beta particle."},
        {"pre": "Protons the nucleus gains = ", "post": "", "answer": 1, "hint": "One neutron becomes one proton."},
        {"phase": "substitute", "pre": "Atomic number counts protons, so it changes by = ", "post": "", "answer": 1, "hint": "One extra proton means +1."},
        {"pre": "Mass number change (a neutron just became a proton, total nucleons the same) = ", "post": "", "answer": 0, "done": "Atomic number goes up by 1; mass number is unchanged.", "hint": "Nucleon count does not change."},
        {"say": "So the atomic number changes by <strong>1</strong> (it increases)."},
     ])

s = pb["silver"]

setp(s[0],
     "Find n = time ÷ half-life first, then halve n times.",
     160, "n = 4 half-lives means halving four times: 640 → 320 → 160 → 80 → 40 Bq. Dividing 640 by 4 gives 160, treating four halvings as one division.", "inverse_error",
     [
        {"say": "First find n, the number of half-lives: n = total time ÷ half-life."},
        {"pre": "n = 32 ÷ 8 = ", "post": "", "answer": 4, "hint": "Divide the total time by the half-life."},
        {"phase": "substitute", "pre": "Halve once: 640 ÷ 2 = ", "post": "", "answer": 320, "hint": "Divide by 2."},
        {"pre": "Halve again: 320 ÷ 2 = ", "post": "", "answer": 160, "hint": "Divide by 2."},
        {"pre": "160 ÷ 2 = ", "post": "", "answer": 80, "hint": "Divide by 2."},
        {"pre": "80 ÷ 2 = ", "post": "", "answer": 40, "done": "Four halvings done.", "hint": "Divide by 2."},
        {"pre": "Check: 40 × 16 = ", "post": "", "answer": 640, "done": "That is 40 × 2⁴ = 640 Bq, the start, so 40 Bq is right.", "hint": "2⁴ = 16; multiplying back should give the start."},
        {"say": "So the activity is <strong>40 Bq</strong>."},
     ])

setp(s[1],
     "Work out how many half-lives fit in 18 hours, then halve that many times.",
     800, "n = 3, so halve three times: 2400 → 1200 → 600 → 300 Bq. Dividing 2400 by 3 gives 800, which is not how halving works.", "inverse_error",
     [
        {"say": "Find n first: n = total time ÷ half-life."},
        {"pre": "n = 18 ÷ 6 = ", "post": "", "answer": 3, "hint": "Divide the total time by the half-life."},
        {"phase": "substitute", "pre": "Halve once: 2400 ÷ 2 = ", "post": "", "answer": 1200, "hint": "Divide by 2."},
        {"pre": "Halve again: 1200 ÷ 2 = ", "post": "", "answer": 600, "hint": "Divide by 2."},
        {"pre": "Halve a third time: 600 ÷ 2 = ", "post": "", "answer": 300, "done": "Three halvings done.", "hint": "Divide by 2."},
        {"pre": "Check: 300 × 8 = ", "post": "", "answer": 2400, "done": "That is 300 × 2³ = 2400 Bq, so 300 Bq is right.", "hint": "2³ = 8."},
        {"say": "So the activity is <strong>300 Bq</strong>."},
     ])

setp(s[2],
     "Alpha decay lowers the atomic number by 2.",
     88, "Alpha decay lowers the atomic number by 2: 92 − 2 = 90 (thorium). Subtracting 4 (the mass-number change) gives 88, mixing the two up.", "wrong_value",
     [
        {"say": "Alpha decay emits \\(^{4}_{2}\\text{He}\\): the nucleus loses 2 protons and 2 neutrons."},
        {"pre": "Protons lost = ", "post": "", "answer": 2, "hint": "An alpha particle has 2 protons."},
        {"phase": "substitute", "pre": "New atomic number = 92 − 2 = ", "post": "", "answer": 90, "hint": "Take 2 from the atomic number."},
        {"pre": "Check the loss: 92 − 90 = ", "post": "", "answer": 2, "done": "2 protons lost, so the daughter has atomic number 90 (thorium).", "hint": "The difference should be 2."},
        {"say": "So the daughter's atomic number is <strong>90</strong>."},
     ])

setp(s[3],
     "Beta decay raises the atomic number by 1.",
     5, "Beta decay raises the atomic number by 1: 6 + 1 = 7 (nitrogen). Lowering it to 5 goes the wrong way; a neutron becomes a proton, adding one.", "wrong_value",
     [
        {"say": "Beta decay: a neutron becomes a proton, so the nucleus gains one proton."},
        {"pre": "Protons gained = ", "post": "", "answer": 1, "hint": "One neutron becomes one proton."},
        {"phase": "substitute", "pre": "New atomic number = 6 + 1 = ", "post": "", "answer": 7, "hint": "Add 1 to the atomic number."},
        {"pre": "Mass number stays the same at = ", "post": "", "answer": 14, "done": "Atomic number 7 (nitrogen), mass number unchanged at 14.", "hint": "Beta decay does not change the mass number."},
        {"say": "So the daughter's atomic number is <strong>7</strong>."},
     ])

setp(s[4],
     "Find n = 20 ÷ 4, then halve the activity n times.",
     192, "n = 5, halve five times: 960 → 480 → 240 → 120 → 60 → 30 Bq. Dividing 960 by 5 gives 192, treating five halvings as one division.", "inverse_error",
     [
        {"say": "Find n first: n = total time ÷ half-life."},
        {"pre": "n = 20 ÷ 4 = ", "post": "", "answer": 5, "hint": "Divide the total time by the half-life."},
        {"phase": "substitute", "pre": "Halve once: 960 ÷ 2 = ", "post": "", "answer": 480, "hint": "Divide by 2."},
        {"pre": "Halve again: 480 ÷ 2 = ", "post": "", "answer": 240, "hint": "Divide by 2."},
        {"pre": "240 ÷ 2 = ", "post": "", "answer": 120, "hint": "Divide by 2."},
        {"pre": "120 ÷ 2 = ", "post": "", "answer": 60, "hint": "Divide by 2."},
        {"pre": "60 ÷ 2 = ", "post": "", "answer": 30, "done": "Five halvings done.", "hint": "Divide by 2."},
        {"pre": "Check: 30 × 32 = ", "post": "", "answer": 960, "done": "That is 30 × 2⁵ = 960 Bq, so 30 Bq is right.", "hint": "2⁵ = 32."},
        {"say": "So the activity is <strong>30 Bq</strong>."},
     ])

g = pb["gold"]

setp(g[0],
     "Going back in time, double the activity once for each half-life.",
     1.5625, "Going back 25 years is 5 half-lives earlier, when activity was higher: 50 × 2⁵ = 1600 Bq. Halving instead (50 ÷ 32) gives about 1.56 Bq, which is the future, not the past.", "direction_error",
     [
        {"say": "Going back in time, the activity was higher. Each half-life earlier it was double. First find how many half-lives fit in 25 years."},
        {"pre": "n = 25 ÷ 5 = ", "post": "", "answer": 5, "hint": "Divide the time by the half-life."},
        {"phase": "substitute", "pre": "Double once (one half-life earlier): 50 × 2 = ", "post": "", "answer": 100, "hint": "Going back, multiply by 2."},
        {"pre": "Double again: 100 × 2 = ", "post": "", "answer": 200, "hint": "Multiply by 2."},
        {"pre": "200 × 2 = ", "post": "", "answer": 400, "hint": "Multiply by 2."},
        {"pre": "400 × 2 = ", "post": "", "answer": 800, "hint": "Multiply by 2."},
        {"pre": "800 × 2 = ", "post": "", "answer": 1600, "done": "Five doublings back through time.", "hint": "Multiply by 2."},
        {"pre": "Check forwards: 1600 ÷ 32 = ", "post": "", "answer": 50, "done": "Halving 5 times (÷32) returns 50 Bq now, so 1600 Bq is right.", "hint": "2⁵ = 32; this should give today's activity."},
        {"say": "So the activity 25 years ago was <strong>1600 Bq</strong>."},
     ])

g[1]["display"] = "Thorium-234 undergoes beta decay. Its mass number is 234 and atomic number is 90. What is the atomic number of the daughter nucleus?"
setp(g[1],
     "Beta decay leaves the mass number alone and adds 1 to the atomic number.",
     89, "Beta decay raises the atomic number by 1: 90 + 1 = 91 (protactinium). Lowering it to 89 goes the wrong way.", "wrong_value",
     [
        {"say": "Beta decay: the mass number stays the same and the atomic number rises by 1 (a neutron becomes a proton)."},
        {"pre": "Protons gained = ", "post": "", "answer": 1, "hint": "One neutron becomes one proton."},
        {"phase": "substitute", "pre": "New atomic number = 90 + 1 = ", "post": "", "answer": 91, "hint": "Add 1 to the atomic number."},
        {"pre": "Mass number stays at = ", "post": "", "answer": 234, "done": "Daughter is protactinium-234: atomic number 91, mass number 234.", "hint": "Beta decay leaves the mass number unchanged."},
        {"say": "So the daughter's atomic number is <strong>91</strong>."},
     ])

setp(g[2],
     "Alpha decay lowers the mass number by 4.",
     208, "Alpha decay lowers the mass number by 4: 210 − 4 = 206. Subtracting 2 (the atomic-number change) gives 208, mixing the two up.", "wrong_value",
     [
        {"say": "Alpha decay: the mass number drops by 4 and the atomic number drops by 2."},
        {"pre": "Nucleons carried off by the alpha particle = ", "post": "", "answer": 4, "hint": "\\(^{4}_{2}\\text{He}\\) has 4 nucleons."},
        {"phase": "substitute", "pre": "New mass number = 210 − 4 = ", "post": "", "answer": 206, "hint": "Take 4 from the mass number."},
        {"pre": "New atomic number = 84 − 2 = ", "post": "", "answer": 82, "done": "Daughter is lead-206: mass number 206, atomic number 82.", "hint": "Take 2 from the atomic number."},
        {"say": "So the daughter's mass number is <strong>206</strong>."},
     ])

setp(g[3],
     "Count how many halvings reach 160 Bq, then multiply by the half-life.",
     5, "Five halvings take you from 5120 to 160 Bq, so n = 5. But the question asks for time: 5 × 8 = 40 days. Answering 5 gives the number of half-lives, not the time.", "forgot_step",
     [
        {"say": "Halve from 5120 Bq until you reach 160 Bq, counting the steps. Each step is one half-life."},
        {"pre": "5120 ÷ 2 = ", "post": "", "answer": 2560, "hint": "Divide by 2."},
        {"pre": "2560 ÷ 2 = ", "post": "", "answer": 1280, "hint": "Divide by 2."},
        {"pre": "1280 ÷ 2 = ", "post": "", "answer": 640, "hint": "Divide by 2."},
        {"pre": "640 ÷ 2 = ", "post": "", "answer": 320, "hint": "Divide by 2."},
        {"pre": "320 ÷ 2 = ", "post": "", "answer": 160, "done": "Reached 160 Bq.", "hint": "Divide by 2."},
        {"pre": "Count the halving steps you did: n = ", "post": "", "answer": 5, "hint": "How many times did you divide by 2?"},
        {"phase": "substitute", "pre": "Time = n × half-life = 5 × 8 = ", "post": "", "answer": 40, "done": "40 days.", "hint": "Multiply the number of half-lives by the half-life."},
        {"pre": "Check: 5120 ÷ 32 = ", "post": "", "answer": 160, "done": "5 halvings (÷32) reach 160 Bq, so 40 days is right.", "hint": "2⁵ = 32."},
        {"say": "So it takes <strong>40 days</strong>."},
     ])

setp(g[4],
     "Find n = 50 ÷ 10, then halve five times.",
     640, "n = 5, halve five times: 3200 → 1600 → 800 → 400 → 200 → 100 Bq. Dividing 3200 by 5 gives 640, which is not halving.", "inverse_error",
     [
        {"say": "Find n first: n = total time ÷ half-life."},
        {"pre": "n = 50 ÷ 10 = ", "post": "", "answer": 5, "hint": "Divide the time by the half-life."},
        {"phase": "substitute", "pre": "Halve once: 3200 ÷ 2 = ", "post": "", "answer": 1600, "hint": "Divide by 2."},
        {"pre": "Halve again: 1600 ÷ 2 = ", "post": "", "answer": 800, "hint": "Divide by 2."},
        {"pre": "800 ÷ 2 = ", "post": "", "answer": 400, "hint": "Divide by 2."},
        {"pre": "400 ÷ 2 = ", "post": "", "answer": 200, "hint": "Divide by 2."},
        {"pre": "200 ÷ 2 = ", "post": "", "answer": 100, "done": "Five halvings done.", "hint": "Divide by 2."},
        {"pre": "Check: 100 × 32 = ", "post": "", "answer": 3200, "done": "That is 100 × 2⁵ = 3200 Bq, so 100 Bq is right.", "hint": "2⁵ = 32."},
        {"say": "So the activity is <strong>100 Bq</strong>."},
     ])

pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one halving at a time",
        "steps": [
            "Activity halves every half-life. After each half-life, divide the activity by 2.",
            "When the question tells you the number of half-lives, just halve that many times.",
            "For decay: an alpha particle is \\(^{4}_{2}\\text{He}\\); a beta particle is an electron. Check whether your board gives you these symbols.",
        ],
        "example": {
            "question": "A sample of 320 Bq decays. Find the activity after 3 half-lives.",
            "steps": [
                {"label": "Halve three times", "content": "<p>320 → 160 → 80 → 40 Bq</p>"},
                {"label": "Check", "content": "<p>40 × 2 × 2 × 2 = 320 ✓</p>"},
                {"label": "Answer", "content": "<p><strong>40 Bq</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: find n first, then halve",
        "steps": [
            "First find n, the number of half-lives: n = total time ÷ half-life.",
            "Then halve the activity n times. Never divide the activity by n; that is the classic slip.",
            "For decay: alpha lowers the mass number by 4 and the atomic number by 2; beta raises the atomic number by 1 and leaves the mass number unchanged.",
        ],
        "example": {
            "question": "A source has a half-life of 5 days and an initial activity of 800 Bq. Find the activity after 15 days.",
            "steps": [
                {"label": "Find n", "content": "<p>n = 15 ÷ 5 = 3 half-lives</p>"},
                {"label": "Halve n times", "content": "<p>800 → 400 → 200 → 100 Bq</p>"},
                {"label": "Check", "content": "<p>100 × 2³ = 100 × 8 = 800 ✓</p>"},
                {"label": "Answer", "content": "<p><strong>100 Bq</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: multi-step and working backwards",
        "steps": [
            "Chain two ideas: find n, then halve (or double) that many times.",
            "Going backwards in time, activity was higher, so double for each half-life instead of halving.",
            "To find a time, count how many halvings reach the target activity, then multiply n by the half-life.",
        ],
        "example": {
            "question": "Radon-222 undergoes alpha decay (atomic number 86, mass number 222). Give the daughter's mass number and atomic number.",
            "steps": [
                {"label": "Apply the alpha change", "content": "<p>Mass: 222 − 4 = 218. Atomic: 86 − 2 = 84 (polonium).</p>"},
                {"label": "Check", "content": "<p>222 = 218 + 4 ✓ and 86 = 84 + 2 ✓</p>"},
                {"label": "Answer", "content": "<p><strong>Mass number 218, atomic number 84</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

pd["guided"] = {
    "opener": {
        "label": "Before any physics",
        "display": "A glow stick loses half its brightness every hour.<br>It starts at 80 units of brightness.",
        "steps": [
            {"say": "No physics yet, just common sense. Half the brightness is gone after one hour.",
             "pre": "After 1 hour, brightness = ", "post": "", "answer": 40, "hint": "Half of 80."},
            {"say": "Another hour goes by, so it halves again.",
             "pre": "After 2 hours, brightness = ", "post": "", "answer": 20, "hint": "Half of 40."},
            {"say": "That fixed time for the amount to halve is called the <strong>half-life</strong>. Radioactive activity works exactly the same way: each half-life, halve the activity. To find the amount after several half-lives, just halve again and again."},
        ],
    },
    "teach": {
        "bronze": {
            "label": "Halving a known number of times",
            "display": "A sample has an activity of 240 Bq. Find the activity after 2 half-lives.",
            "steps": [
                {"say": "Each half-life halves the activity. Here we halve twice."},
                {"pre": "Number of half-lives = ", "post": "", "answer": 2, "hint": "The question says after two half-lives."},
                {"pre": "Halve once: 240 ÷ 2 = ", "post": "", "answer": 120, "hint": "Divide by 2."},
                {"pre": "Halve again: 120 ÷ 2 = ", "post": "", "answer": 60, "done": "Two halvings done.", "hint": "Divide by 2."},
                {"pre": "Check: 60 × 2 × 2 = ", "post": "", "answer": 240, "done": "Back to 240 Bq, so 60 Bq is right.", "hint": "Doubling twice returns the start."},
                {"say": "So the activity is <strong>60 Bq</strong>."},
            ],
        },
        "silver": {
            "label": "Find n from the time, then halve",
            "display": "A source has a half-life of 3 hours and an initial activity of 4800 Bq. Find the activity after 12 hours.",
            "steps": [
                {"say": "The time is given, not the number of half-lives. Find n first."},
                {"pre": "n = 12 ÷ 3 = ", "post": "", "answer": 4, "hint": "Total time ÷ half-life."},
                {"pre": "Halve once: 4800 ÷ 2 = ", "post": "", "answer": 2400, "hint": "Divide by 2."},
                {"pre": "Halve again: 2400 ÷ 2 = ", "post": "", "answer": 1200, "hint": "Divide by 2."},
                {"pre": "1200 ÷ 2 = ", "post": "", "answer": 600, "hint": "Divide by 2."},
                {"pre": "600 ÷ 2 = ", "post": "", "answer": 300, "done": "Four halvings, because n = 4.", "hint": "Divide by 2."},
                {"say": "So the activity is <strong>300 Bq</strong>."},
            ],
        },
        "gold": {
            "label": "Working backwards in time",
            "display": "A sample now reads 12 Bq. Its half-life is 2 years. What was the activity 8 years ago?",
            "steps": [
                {"say": "Going back in time, the activity was higher, so double for each half-life. Find n first."},
                {"pre": "n = 8 ÷ 2 = ", "post": "", "answer": 4, "hint": "Total time ÷ half-life."},
                {"pre": "Double once (going back): 12 × 2 = ", "post": "", "answer": 24, "hint": "Multiply by 2."},
                {"pre": "24 × 2 = ", "post": "", "answer": 48, "hint": "Multiply by 2."},
                {"pre": "48 × 2 = ", "post": "", "answer": 96, "hint": "Multiply by 2."},
                {"pre": "96 × 2 = ", "post": "", "answer": 192, "done": "Four doublings back, so 192 Bq eight years ago.", "hint": "Multiply by 2."},
                {"say": "So the activity was <strong>192 Bq</strong> eight years ago."},
            ],
        },
    },
}

# Clean em dashes from preserved fields (ship-gate style rule: none anywhere student-facing)
def declash(o):
    if isinstance(o, dict):
        return {k: declash(v) for k, v in o.items()}
    if isinstance(o, list):
        return [declash(v) for v in o]
    if isinstance(o, str):
        return o.replace(" — ", ": ").replace("—", ", ")
    return o
pd = declash(pd)

OUT = "lesson_higher-calculations-L05@09acbba067.json"
with io.open(OUT, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)

c = re.sub("<[^>]+>", " ", pd["method_card"]["content"])
print("written", OUT)
print("method_card content words:", len(c.split()))
