# -*- coding: utf-8 -*-
import json, io

pd = json.load(io.open('_live_ps_L03_pd.json', encoding='utf-8'))
pb = pd['problem_bank']
bronze, silver, gold = pb['bronze'], pb['silver'], pb['gold']

def box(pre, answer, hint, post='', say=None, done=None, phase=None):
    d = {}
    if say is not None: d['say'] = say
    d['pre'] = pre
    d['post'] = post
    d['answer'] = answer
    d['hint'] = hint
    if done is not None: d['done'] = done
    if phase is not None: d['phase'] = phase
    return d

def say(text):
    return {'say': text}

# ---------------------------------------------------------------------------
# 1. AUDIT FIX: bronze[6] dangling "table above" -> embed the data
bronze[6]['display'] = ("A frequency table shows: Red 12, Blue 8, Green 10. "
    "What fraction of students chose Blue? Give as a simplified fraction.")

# 1b. AUDIT FIX: gold[1] misleading misconception message + expect stays null
gold[1]['misconceptions'][0]['message'] = ("School A sport students = (100 ÷ 360) × 360 = 100. "
    "School B sport students = (120 ÷ 360) × 240 = 80. School A has 20 more. "
    "School A's total happens to equal 360, so its count matches its angle, but you must always "
    "multiply by the number of people, not by 360.")

# 1c. gold[2] composite bar: replace non-derivable expect 100 with a real slip (forgot x100)
gold[2]['misconceptions'][0]['message'] = ("Q2 total = 60 + 45 + 35 = 140. Annual total = 110 + 140 + 120 + 130 = 500. "
    "Percentage = (140 ÷ 500) × 100 = 28%. If you got 0.28 you found the fraction but forgot to × 100.")
gold[2]['misconceptions'][0]['expect'] = 0.28

# 1d. gold[0] scatter: keep expect 160, clarify why it is wrong
gold[0]['misconceptions'][0]['message'] = ("The line of best fit rises 40 across 40, so its gradient is 1. "
    "At height 160: arm span = 138 + (160 − 140) × 1 = 158 cm. Reading a nearby dot instead of the line gives about 160, which is too high.")

# 1e. gold[3] histogram: keep expect 0.32, add note
gold[3]['misconceptions'][0]['message'] = ("Class width = 15 − 5 = 10. Frequency = frequency density × width = 3.2 × 10 = 32. "
    "Dividing instead (3.2 ÷ 10 = 0.32) is the slip.")

# 1f. silver[2] em dash fix
silver[2]['misconceptions'][0]['message'] = ("As revision hours increase, scores increase steadily and the points hug a straight line, "
    "so this is strong positive correlation.")

# ---------------------------------------------------------------------------
# 2. HINTS on every problem
bronze[0]['hint'] = "Read the Pizza bar straight across to the number axis."
bronze[1]['hint'] = "The most popular choice is the tallest bar."
bronze[2]['hint'] = "A quarter of the circle means a quarter of the 60 students, then simplify."
bronze[3]['hint'] = "Read the Cats bar and the Fish bar, then subtract."
bronze[4]['hint'] = "The slice is 90° out of 360°, a quarter, so take a quarter of 200."
bronze[5]['hint'] = "Add the three frequencies together."
bronze[6]['hint'] = "Find the total, then write Blue over the total and simplify."
bronze[7]['hint'] = "As one value rises the other rises: that direction has a special name."

silver[0]['hint'] = "Read both football bars and subtract the smaller from the larger."
silver[1]['hint'] = "Find the tallest point, then read off its month number."
silver[2]['hint'] = "The points climb steadily and lie close to a straight line."
silver[3]['hint'] = "Use (angle ÷ 360) × total with 54° and 100 students."
silver[4]['hint'] = "Substitute x = 8 into y = 2x + 5."
silver[5]['hint'] = "Frequency = frequency density × class width."
silver[6]['hint'] = "Ignore the small dips, compare the start value with the end value."

gold[0]['hint'] = "Find the gradient from the two given points, then read the line at height 160."
gold[1]['hint'] = "Convert each pie to a real count first, because the totals differ, then subtract."
gold[2]['hint'] = "Add the Q2 segments, find the annual total, then work out the percentage."
gold[3]['hint'] = "Frequency = frequency density × class width, and the width is 10."
gold[4]['hint'] = "Work out the car users for each chart separately, then add."

# ---------------------------------------------------------------------------
# 3. guided_steps on every non-MC problem

# BRONZE 0 (pizza = 20)
bronze[0]['guided_steps'] = [
    say("Read the height of each bar off the number axis. The Pizza bar sits between Sandwiches and Pasta."),
    box("Read the Sandwiches bar first: ", 25, "Read straight across from the top of the Sandwiches bar."),
    box("Now the one asked for: how many chose Pizza? ", 20, "Read straight across from the top of the Pizza bar.", phase="substitute"),
    box("Check it sits halfway between Sandwiches (25) and Pasta (15): (25 + 15) ÷ 2 = ", 20,
        "Average the two neighbouring bars.", phase="substitute", done="20 sits exactly between them, so the reading is right."),
]

# BRONZE 2 (pie fraction 1/4)
bronze[2]['guided_steps'] = [
    say("The Walk slice is exactly one quarter of the circle, so one quarter of the 60 students walk."),
    box("One quarter of the students: 60 ÷ 4 = ", 15, "A quarter means divide by 4."),
    box("So 15 out of 60 walk. Simplify by dividing both by 15. Top: 15 ÷ 15 = ", 1,
        "15 divided by 15.", phase="substitute"),
    box("Bottom: 60 ÷ 15 = ", 4, "60 divided by 15.", phase="substitute",
        done="So 15/60 = 1/4, the simplified fraction."),
]

# BRONZE 3 (cats - fish = 5)
bronze[3]['guided_steps'] = [
    say("Read the two bars you need off the number axis."),
    box("Read the Cats bar: ", 10, "Read across from the top of the Cats bar."),
    box("Read the Fish bar: ", 5, "Read across from the top of the Fish bar.", phase="substitute"),
    box("How many more chose cats than fish? 10 − 5 = ", 5, "Subtract the smaller from the larger.", phase="substitute"),
    box("Check: fish plus that difference should give cats. 5 + 5 = ", 10, "Add the difference back on.",
        phase="substitute", done="Equals the Cats bar, so 5 is right."),
]

# BRONZE 4 (football pie -> 50)
bronze[4]['guided_steps'] = [
    say("A pie chart is one full turn, 360°. Work out what fraction of the circle the football slice is."),
    box("The football slice is 90° out of 360°. 360 ÷ 90 = ", 4,
        "How many 90s fit into 360? This tells you the slice is one quarter."),
    box("So football is one quarter of the 200 students. 200 ÷ 4 = ", 50,
        "One quarter of 200.", phase="substitute"),
    box("Check by turning 50 back into an angle: (50 ÷ 200) × 360 = ", 90,
        "Fraction of students times 360.", phase="substitute", done="Back to 90°, so 50 is right."),
]

# BRONZE 5 (table total = 30)
bronze[5]['guided_steps'] = [
    say("Add the three frequencies: Red 12, Blue 8, Green 10."),
    box("Add the first two: 12 + 8 = ", 20, "Red plus Blue."),
    box("Now add Green: 20 + 10 = ", 30, "Add the Green frequency to the running total.", phase="substitute"),
    box("Check by adding in a different order: 12 + 10 + 8 = ", 30,
        "Red plus Green plus Blue.", phase="substitute", done="Same total, so 30 is right."),
]

# BRONZE 6 (table fraction 4/15)
bronze[6]['guided_steps'] = [
    say("First find the total, then write Blue over the total and simplify."),
    box("Total frequency: 12 + 8 + 10 = ", 30, "Add all three frequencies."),
    box("Blue is 8 out of 30. Simplify by dividing both by 2. Top: 8 ÷ 2 = ", 4,
        "8 divided by 2.", phase="substitute"),
    box("Bottom: 30 ÷ 2 = ", 15, "30 divided by 2.", phase="substitute",
        done="So 8/30 = 4/15."),
]

# SILVER 0 (dual bar boys - girls football = 10)
silver[0]['guided_steps'] = [
    say("Read the football bar for each group off the number axis."),
    box("Read the boys' football bar (blue): ", 30, "Read the blue Football bar."),
    box("Read the girls' football bar (pink): ", 20, "Read the pink Football bar.", phase="substitute"),
    box("How many more boys than girls chose football? 30 − 20 = ", 10,
        "Subtract the girls from the boys.", phase="substitute", done="Boys lead football by 10."),
]

# SILVER 1 (line graph highest month = 7)
silver[1]['guided_steps'] = [
    say("Find the tallest point on the line, then read off which month it is."),
    box("Read the value at the peak. July is the highest point, at £", 400, "The tallest point on the line."),
    box("Which month number is July? Count from January = 1. July is month ", 7,
        "Jan 1, Feb 2, Mar 3, Apr 4, May 5, Jun 6, Jul 7.", phase="substitute"),
    box("Check the neighbours are lower: August (month 8) is £350, less than £400. So the peak month number is ", 7,
        "The highest bar's month.", phase="substitute", done="July, month 7, is the highest."),
]

# SILVER 3 (grade A pie -> 15)
silver[3]['guided_steps'] = [
    say("Use (angle ÷ 360) × total. The angle is 54° and the total is 100 students."),
    box("Work out the top of the calculation first: 54 × 100 = ", 5400, "54 times 100."),
    box("Now divide by 360: 5400 ÷ 360 = ", 15, "5400 divided by 360.", phase="substitute"),
    box("Check by turning 15 back into an angle: (15 ÷ 100) × 360 = ", 54,
        "Fraction of students times 360.", phase="substitute", done="Back to 54°, so 15 is right."),
]

# SILVER 4 (line of best fit y = 2x + 5 at x = 8 -> 21)
silver[4]['guided_steps'] = [
    say("Substitute x = 8 into y = 2x + 5, one step at a time."),
    box("Work out the 2x part: 2 × 8 = ", 16, "Multiply 2 by 8."),
    box("Now add the 5: 16 + 5 = ", 21, "Add the constant term.", phase="substitute"),
    box("Check the equation at x = 0, which should give the intercept: 2 × 0 + 5 = ", 5,
        "Put x = 0 into the equation.", phase="substitute", done="Gives the intercept 5 as expected, so y = 21 at x = 8 is right."),
]

# SILVER 5 (frequency density 4, width 10 -> 40)
silver[5]['guided_steps'] = [
    say("Frequency = frequency density × class width. First find the width."),
    box("Class width: 25 − 15 = ", 10, "Top of the class minus the bottom."),
    box("Frequency = density × width = 4 × 10 = ", 40, "Multiply density by width.", phase="substitute"),
    box("Check: density = frequency ÷ width = 40 ÷ 10 = ", 4,
        "Divide frequency back by the width.", phase="substitute", done="Back to a density of 4, so 40 is right."),
]

# GOLD 0 (scatter arm span at height 160 -> 158)
gold[0]['guided_steps'] = [
    say("The line of best fit passes through (140, 138) and (180, 178). Find its gradient first."),
    box("Rise: 178 − 138 = ", 40, "Top y minus bottom y."),
    box("Run: 180 − 140 = ", 40, "Top x minus bottom x."),
    box("Gradient = rise ÷ run = 40 ÷ 40 = ", 1, "Divide the rise by the run."),
    box("At height 160, that is 20 cm past the first point, rising 20 × 1 = 20. Arm span = 138 + 20 = ", 158,
        "Start at 138 and add the rise.", phase="substitute"),
    box("Check the line at height 180: 138 + (180 − 140) × 1 = ", 178,
        "Put height 180 into the same line.", phase="substitute", done="Matches the second point, so 158 cm is right."),
]

# GOLD 1 (comparative pie -> A has 20 more)
gold[1]['guided_steps'] = [
    say("The totals differ (360 and 240), so convert each pie to a real count before comparing."),
    box("School A: (100 ÷ 360) × 360. Here the total happens to be 360, so this equals ", 100,
        "The two 360s cancel this time, but always multiply by the number of people."),
    box("School B: (120 ÷ 360) × 240. Since 120 ÷ 360 = one third, take a third of 240: 240 ÷ 3 = ", 80,
        "A third of 240.", phase="substitute"),
    box("How many more sport students does School A have? 100 − 80 = ", 20,
        "Subtract School B's count from School A's.", phase="substitute"),
    box("Check School B as an angle: (80 ÷ 240) × 360 = ", 120,
        "Fraction of students times 360.", phase="substitute", done="Back to 120°, so School B's 80 is right and A has 20 more."),
]

# GOLD 2 (composite bar Q2 percentage -> 28)
gold[2]['guided_steps'] = [
    say("Add the parts of the Q2 bar, find the annual total, then work out the percentage."),
    box("Stack the three Q2 segments: Electronics 60 + Clothing 45 + Food 35 = ", 140, "Add the three Q2 parts."),
    box("Annual total. Q1 = 110, Q3 = 120, Q4 = 130. Add all four: 110 + 140 + 120 + 130 = ", 500,
        "Add the four quarter totals."),
    box("Q2 as a percentage: (140 ÷ 500) × 100 = ", 28,
        "Divide Q2 by the annual total, then times 100.", phase="substitute"),
    box("Check: 28% of 500 should give Q2 back. (28 ÷ 100) × 500 = ", 140,
        "Take 28% of the annual total.", phase="substitute", done="Returns 140, so 28% is right."),
]

# GOLD 3 (histogram frequency 5-15, fd 3.2 -> 32)
gold[3]['guided_steps'] = [
    say("Frequency = frequency density × class width. Use the 5 to 15 class; ignore the other one."),
    box("Class width for 5 to 15: 15 − 5 = ", 10, "Top of the class minus the bottom."),
    box("Frequency = density × width = 3.2 × 10 = ", 32, "Multiply density by width.", phase="substitute"),
    box("Check: density = frequency ÷ width = 32 ÷ 10 = ", 3.2,
        "Divide frequency back by the width.", phase="substitute", done="Back to a density of 3.2, so 32 is right."),
]

# GOLD 4 (two pies car users total -> 170)
gold[4]['guided_steps'] = [
    say("Work out the car users for each chart separately, then add. The angles cannot be added directly because the totals differ."),
    box("Chart A: (144 ÷ 360) × 200. Since 144 ÷ 360 = 0.4, take 0.4 × 200 = ", 80,
        "144/360 = 0.4, then 0.4 of 200."),
    box("Chart B: (108 ÷ 360) × 300. Since 108 ÷ 360 = 0.3, take 0.3 × 300 = ", 90,
        "108/360 = 0.3, then 0.3 of 300.", phase="substitute"),
    box("Total car users across both charts: 80 + 90 = ", 170, "Add the two counts.", phase="substitute"),
    box("Check Chart A as an angle: (80 ÷ 200) × 360 = ", 144,
        "Fraction of Chart A times 360.", phase="substitute", done="Back to 144°, so 80 is right and the total is 170."),
]

# ---------------------------------------------------------------------------
# 4. tier descriptions
pb['bronze_description'] = "Read one value off a bar, pie or table, or do a single-step calculation."
pb['silver_description'] = "Put a number into a formula, or compare and describe a data set."
pb['gold_description'] = "Combine several steps: different totals, percentages, or histogram frequencies."

# ---------------------------------------------------------------------------
# 5. tier_guides
pd['tier_guides'] = {
    "bronze": {
        "title": "Bronze: read the chart",
        "steps": [
            "A chart or table is a set of numbers drawn as a picture. Read a value by finding the label, then reading across to the axis.",
            "For a simple pie chart, a right angle (90°) is a quarter of the circle and a straight line (180°) is a half.",
            "To compare two bars, read both and subtract. To turn a pie slice into people, use (angle ÷ 360) × total."
        ],
        "example": {
            "question": "A bar chart shows: Apple 12, Banana 9, Pear 6. How many more chose Apple than Pear?",
            "steps": [
                {"label": "Read Apple", "content": "<p>The Apple bar reaches 12.</p>"},
                {"label": "Read Pear", "content": "<p>The Pear bar reaches 6.</p>"},
                {"label": "Subtract", "content": "<p>\\(12 - 6 = 6\\)</p>"},
                {"label": "Answer", "content": "<p><strong>6 more chose Apple</strong></p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: use a formula or compare",
        "steps": [
            "Now you feed one number into a rule. Pie chart: people = (angle ÷ 360) × total. Line of best fit: put the x-value into its equation.",
            "Histogram: frequency = frequency density × class width.",
            "For graphs over time or dual bar charts, read the exact point asked for and describe the pattern, not just the biggest bar."
        ],
        "example": {
            "question": "90 people were surveyed. The pie-chart slice for tennis is 72°. How many chose tennis?",
            "steps": [
                {"label": "Fraction", "content": "<p>\\(72 \\div 360 = \\tfrac{1}{5}\\)</p>"},
                {"label": "Apply", "content": "<p>\\(\\tfrac{1}{5} \\times 90 = 18\\)</p>"},
                {"label": "Check", "content": "<p>\\((18 \\div 90) \\times 360 = 72\\) ✓</p>"},
                {"label": "Answer", "content": "<p><strong>18 chose tennis</strong></p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: combine steps",
        "steps": [
            "Gold questions need two or more moves. With two pie charts of different totals you cannot compare angles: turn each into real counts first, then compare.",
            "For a composite (stacked) bar chart, add the parts of each bar, find the grand total, then work out the percentage asked for.",
            "For a scatter line of best fit, find the gradient from two points, then calculate the value you need."
        ],
        "example": {
            "question": "Pie A: 200 people, bus = 90°. Pie B: 300 people, bus = 60°. How many bus users in total?",
            "steps": [
                {"label": "Pie A", "content": "<p>\\((90 \\div 360) \\times 200 = 50\\)</p>"},
                {"label": "Pie B", "content": "<p>\\((60 \\div 360) \\times 300 = 50\\)</p>"},
                {"label": "Add", "content": "<p>\\(50 + 50 = 100\\)</p>"},
                {"label": "Answer", "content": "<p><strong>100 bus users</strong></p>", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

# ---------------------------------------------------------------------------
# 6. guided (opener + teach)
pd['guided'] = {
    "opener": {
        "label": "Before any formula",
        "display": "20 friends order pizza. On the chart:<br>Half the circle = Margherita<br>A quarter = Pepperoni<br>A quarter = Veggie",
        "steps": [
            box("Half of the 20 friends chose Margherita. How many is that? ", 10,
                "Half of 20.", say="No formula needed, just common sense. Look at the slices."),
            box("A quarter chose Pepperoni. How many is that? ", 5,
                "A quarter of 20, or 20 ÷ 4.",
                say="You just turned a fraction of the whole into a count. A pie chart does exactly this: a full circle is 360°, and a slice's share of 360° is its share of the people."),
            say("A quarter of the circle is 90° (because 360 ÷ 4 = 90). So a real pie chart labels Pepperoni as 90°, and you find the count with (90 ÷ 360) × 20 = 5. Same answer. That formula, <strong>(angle ÷ 360) × total</strong>, is the heart of this whole topic.")
        ]
    },
    "teach": {
        "bronze": {
            "display": "A bar chart shows how a class travels to school: Walk 9, Bus 7, Car 5, Cycle 4. How many more walk than cycle?",
            "label": "Together: your first one",
            "steps": [
                say("Read each bar off the number axis first. The height is the number of students."),
                box("How many walk? Read the Walk bar: ", 9, "Read across from the top of the Walk bar."),
                box("How many cycle? Read the Cycle bar: ", 4, "Read across from the top of the Cycle bar."),
                box("How many more walk than cycle? 9 − 4 = ", 5, "Subtract the smaller from the larger.",
                    done="Gone. Reading two bars and subtracting is the whole bronze move."),
                box("Check: cycle plus that difference should give walk. 4 + 5 = ", 9,
                    "Add the difference back on.", done="Equals the Walk bar, so 5 is right.")
            ]
        },
        "silver": {
            "display": "120 people were surveyed. On a pie chart the slice for rugby is 60°. How many people chose rugby?",
            "label": "Together: the silver move",
            "steps": [
                say("A pie chart is one full turn, 360°. A slice's share of 360° equals its share of the people. Formula: people = (angle ÷ 360) × total."),
                box("Read the rugby slice size off the chart: it is how many degrees? ", 60,
                    "The slice is labelled with its angle."),
                box("How many 60s fit into 360? 360 ÷ 60 = ", 6,
                    "This tells you the slice is one sixth of the circle."),
                box("So rugby is one sixth of the 120 people. 120 ÷ 6 = ", 20,
                    "One sixth of 120.", done="That is the silver move: one number into the formula."),
                box("Check by turning 20 back into an angle: (20 ÷ 120) × 360 = ", 60,
                    "Fraction of people times 360.", done="Back to 60°, so 20 is right.")
            ]
        },
        "gold": {
            "display": "Club A has 240 members; its juniors slice is 90°. Club B has 300 members; its juniors slice is 60°. Which club has more juniors, and how many more?",
            "label": "Together: the gold move",
            "steps": [
                say("The totals differ, so comparing 90° with 60° directly is a trap. Turn each into a real count first, then compare."),
                box("Club A: 90° out of 360° is a quarter. A quarter of 240 = 240 ÷ 4 = ", 60,
                    "360 ÷ 90 = 4, so divide the total by 4."),
                box("Club B: 60° out of 360° is one sixth. One sixth of 300 = 300 ÷ 6 = ", 50,
                    "360 ÷ 60 = 6, so divide the total by 6."),
                box("Which is bigger, and by how much? 60 − 50 = ", 10,
                    "Subtract the smaller count.", done="Club A, by 10. The bigger angle was the smaller count, because the totals differ."),
                box("Check Club B as an angle: (50 ÷ 300) × 360 = ", 60,
                    "Fraction of Club B times 360.", done="Back to 60°, so 50 is right.")
            ]
        }
    }
}

# ---------------------------------------------------------------------------
# 7. method_card trim (<= 4 steps, content <= 140 words)
pd['method_card'] = {
    "title": "Representing and Interpreting Data",
    "steps": [
        "Read a value: find the label, then read across to the axis.",
        "Pie chart: people = (angle ÷ 360) × total, and reverse it to find an angle.",
        "Scatter: describe the correlation and use the line of best fit to estimate.",
        "Histogram: frequency = frequency density × class width."
    ],
    "content": ("<p><strong>Pie charts:</strong> a slice's share of 360° is its share of the people. "
        "Count = (angle ÷ 360) × total; reverse to find an angle.</p>"
        "<p><strong>Scatter graphs:</strong> positive (both rise), negative (one rises as the other falls) or none. "
        "The line of best fit estimates one value from the other.</p>"
        "<p><strong>Bar charts and tables:</strong> read heights directly and compare by subtracting. A composite bar stacks its parts.</p>"
        "<p><strong>Histograms:</strong> frequency = frequency density × class width.</p>"
        "<p><strong>Time series:</strong> plot over time and describe the trend as rising, falling or steady.</p>"),
    "example": ("<p><strong>60 people were surveyed about favourite fruit. 15 chose apple. Find the pie chart angle.</strong></p>"
        "<p>Angle = \\(\\frac{15}{60} \\times 360 = 90°\\)</p>")
}

# ---------------------------------------------------------------------------
io.open('lesson_probability-statistics-L03.json', 'w', encoding='utf-8').write(
    json.dumps(pd, ensure_ascii=False, indent=1))
print("written")
