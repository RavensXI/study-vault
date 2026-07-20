# -*- coding: utf-8 -*-
"""Build the guided practice_data for Geography Skills L07 (Percentage Change & Proportions)."""
import json, io, os, sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
pd = json.load(io.open(os.path.join(HERE, "_live_L07.json"), encoding="utf-8"))
pb = pd["problem_bank"]


def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say:
        d["say"] = say
    if done:
        d["done"] = done
    if phase:
        d["phase"] = phase
    return d


def say(text):
    return {"say": text}


def mis(pattern, message, expect, note=None):
    d = {"pattern": pattern, "message": message, "expect": expect}
    if note:
        d["note"] = note
    return d


# ---------------------------------------------------------------- change walk
def change_walk(orig_label, orig, other_label, new, diff, dec, pct, rising,
                check_pre, check_ans, check_done, unit=""):
    """Standard four-move percentage-change walk plus a check."""
    word = "rise" if rising else "fall"
    return [
        say("Before any arithmetic, pin down which of the two figures you are "
            "measuring the change <strong>from</strong>."),
        box(orig_label, orig,
            "It is the figure the question starts at, not the one it ends at.",
            post=unit),
        box(other_label, diff,
            "Take the smaller figure away from the larger one.", post=unit),
        box("Now compare that %s with the value you started from. %s ÷ %s = "
            % (word, fmt(diff), fmt(orig)), dec,
            "Divide the change by the starting value. Your calculator will give "
            "a decimal below 1.", phase="substitute",
            say="The %s on its own means little until you set it against the "
                "starting value." % word),
        box("%s × 100 = " % fmt(dec), pct,
            "Multiply the decimal by 100 to turn it into a percentage.",
            post=" %"),
        box(check_pre, check_ans,
            "Work it out. If it does not land back on the figure in the "
            "question, something has slipped.",
            done=check_done,
            say="Last move: run the percentage forwards and see if it returns "
                "the figure the question gave you."),
    ]


def fmt(x):
    if isinstance(x, float) and x == int(x):
        x = int(x)
    return ("%g" % x)


# ================================================================== BRONZE ===
b = pb["bronze"]

# b0: 2,000 -> 2,500, 25%
b[0]["hint"] = ("Work out the rise first, then compare it with the population "
                "the village started at.")
b[0]["misconceptions"] = [
    mis("divided_by_new",
        "You compared the rise with the population the village ended at. "
        "Percentage change is always measured against the value you started "
        "from.", 20),
    mis("forgot_multiply",
        "That is the decimal fraction, not a percentage. One step is missing "
        "at the end.", 0.25),
]
b[0]["guided_steps"] = change_walk(
    "The population before the growth was ", 2000,
    "Rise = 2500 − 2000 = ", 2500, 500, 0.25, 25, True,
    "Check: 2000 × 1.25 = ", 2500,
    "It lands exactly on the later population, so the percentage is right.")

# b1: rainfall 120 mm -> 102 mm, 15%
b[1]["display"] = ("Rainfall decreased from 120 mm to 102 mm. What is the "
                   "percentage decrease?")
b[1]["solutions"] = [15]
b[1]["hint"] = ("Find how many millimetres were lost, then compare that loss "
                "with the rainfall before the drop.")
b[1]["misconceptions"] = [
    mis("remaining_not_change",
        "That is how much of the original rainfall is left, not how much was "
        "lost. The question asks about the size of the drop.", 85),
    mis("forgot_multiply",
        "That is the decimal fraction. Percentages need one more step.", 0.15),
]
b[1]["guided_steps"] = change_walk(
    "Rainfall before the drop, in mm, was ", 120,
    "Fall = 120 − 102 = ", 102, 18, 0.15, 15, False,
    "Check: 120 × 0.85 = ", 102,
    "It returns the later rainfall figure, so the percentage is right.")

# b2: GDP 50 -> 60, 20%
b[2]["hint"] = ("Compare the rise in GDP with the 2015 figure, not the 2020 "
                "one.")
b[2]["misconceptions"] = [
    mis("gave_difference",
        "That is the rise in billions of dollars, not a percentage. You still "
        "need to compare it with the starting GDP.", 10),
    mis("forgot_multiply",
        "That is the decimal fraction. Multiply by 100 to make it a "
        "percentage.", 0.2),
]
b[2]["guided_steps"] = change_walk(
    "GDP in 2015, in billions of dollars, was ", 50,
    "Rise = 60 − 50 = ", 60, 10, 0.2, 20, True,
    "Check: 50 × 1.2 = ", 60,
    "It gives the 2020 GDP back, so the percentage is right.")

# b3: 240 of 800 -> 30%
b[3]["hint"] = ("A proportion is the part divided by the whole, so find the "
                "total number of jobs first.")
b[3]["misconceptions"] = [
    mis("used_the_remainder",
        "You worked out the share of jobs that are not in tourism. Read which "
        "group the question actually asks about.", 70),
    mis("forgot_multiply",
        "That is the proportion as a decimal. A percentage needs one more "
        "step.", 0.3),
]
b[3]["guided_steps"] = [
    say("A proportion question needs two things: the <strong>whole</strong> "
        "and the <strong>part</strong>. Locate them before dividing."),
    box("The whole, meaning every job in the town, is ", 800,
        "It is the larger of the two figures in the question."),
    box("The part we want, the tourism jobs, is ", 240,
        "It is the group the question names."),
    box("240 ÷ 800 = ", 0.3,
        "Divide the part by the whole. The answer must be less than 1.",
        phase="substitute",
        say="Now divide the part by the whole, in that order."),
    box("0.3 × 100 = ", 30, "Multiply the decimal by 100.", post=" %"),
    box("Check: 0.3 × 800 = ", 240,
        "Take your percentage as a decimal and apply it to the total.",
        done="It returns the tourism jobs figure, so the proportion is right.",
        say="Check by running the percentage back over the whole."),
]

# b4: glacier 5.0 -> 4.5, 10%
b[4]["hint"] = ("Find the area of ice lost, then compare it with the ice "
                "cover before the melt.")
b[4]["misconceptions"] = [
    mis("gave_difference",
        "That is the area lost in square kilometres, not a percentage of the "
        "original ice cover.", 0.5),
    mis("forgot_multiply",
        "That is the decimal fraction. Turn it into a percentage.", 0.1),
]
b[4]["guided_steps"] = change_walk(
    "Ice cover before the melt, in km², was ", 5,
    "Loss = 5.0 − 4.5 = ", 4.5, 0.5, 0.1, 10, False,
    "Check: 5 × 0.9 = ", 4.5,
    "It returns the later ice cover, so the percentage is right.")

# b5: cars 150,000 -> 210,000, 40%
b[5]["display"] = ("A city had 150,000 cars in 2010 and 210,000 in 2020. What "
                   "is the percentage increase?")
b[5]["solutions"] = [40]
b[5]["hint"] = ("Work out how many extra cars there are, then compare that "
                "with the 2010 total.")
b[5]["misconceptions"] = [
    mis("new_as_percent_of_old",
        "You worked out the 2020 total as a percentage of the 2010 total. The "
        "question asks only about the extra cars.", 140),
    mis("forgot_multiply",
        "That is the decimal fraction. Percentages need one more step.", 0.4),
]
b[5]["guided_steps"] = change_walk(
    "Cars in 2010: ", 150000,
    "Rise = 210000 − 150000 = ", 210000, 60000, 0.4, 40, True,
    "Check: 150000 × 1.4 = ", 210000,
    "It returns the 2020 total, so the percentage is right.")

# b6: 175 of 500 -> 35%
b[6]["hint"] = ("Divide the number who use public transport by the number of "
                "people surveyed.")
b[6]["misconceptions"] = [
    mis("used_the_remainder",
        "You worked out the share who do not use public transport. Check "
        "which group the question asks about.", 65),
    mis("forgot_multiply",
        "That is the proportion as a decimal. One step still to go.", 0.35),
]
b[6]["guided_steps"] = [
    say("Find the <strong>whole</strong> first, then the <strong>part</strong>."),
    box("The whole, meaning everyone surveyed, is ", 500,
        "It is the total number of people asked."),
    box("The part, meaning public transport users, is ", 175,
        "It is the group named in the question."),
    box("175 ÷ 500 = ", 0.35,
        "Divide the part by the whole. The answer must be less than 1.",
        phase="substitute",
        say="Divide the part by the whole, in that order."),
    box("0.35 × 100 = ", 35, "Multiply the decimal by 100.", post=" %"),
    box("Check: 0.35 × 500 = ", 175,
        "Apply your percentage back to the 500 people surveyed.",
        done="It returns the number of public transport users, so the "
             "proportion is right.",
        say="Check by running the percentage back over the whole."),
]

# b7: discharge 40 -> 35 cumecs, 12.5%
b[7]["display"] = ("A river's average discharge fell from 40 cumecs to 35 "
                   "cumecs after a drought. What is the percentage decrease?")
b[7]["solutions"] = [12.5]
b[7]["hint"] = ("Find the drop in cumecs, then compare it with the discharge "
                "before the drought.")
b[7]["misconceptions"] = [
    mis("remaining_not_change",
        "That is the discharge that is left as a percentage of the original, "
        "not the size of the drop.", 87.5),
    mis("gave_difference",
        "That is the drop measured in cumecs. The question asks for it as a "
        "percentage.", 5),
]
b[7]["guided_steps"] = change_walk(
    "Discharge before the drought, in cumecs, was ", 40,
    "Fall = 40 − 35 = ", 35, 5, 0.125, 12.5, False,
    "Check: 40 × 0.875 = ", 35,
    "It returns the drought discharge, so the percentage is right.")

# ================================================================== SILVER ===
s = pb["silver"]

# s0: chart, percentage points, 20
s[0]["hint"] = ("Read both Primary bars off the chart and subtract, because "
                "percentage points are a straight difference.")
s[0]["misconceptions"] = [
    mis("read_wrong_series",
        "Those are not the Primary bars. Match the colour in the legend to "
        "the bars before reading any heights.", 25,
        note="Tertiary series: 60 - 35 = 25"),
    mis("gave_one_reading",
        "That is a single bar height, not the gap between two of them.", 15),
]
s[0]["guided_steps"] = [
    say("Chart first, arithmetic second. The legend has three sectors in "
        "order: Primary, Secondary, Tertiary."),
    box("Counting from the left of the legend, Primary is series number ", 1,
        "It is listed first in the legend, before Secondary and Tertiary."),
    box("Find the 2000 group on the horizontal axis and read the Primary bar. "
        "Its height, in % of the workforce, is ", 35,
        "Follow the top of that bar across to the vertical axis, which is "
        "marked every 10."),
    box("Now the Primary bar in the 2020 group: ", 15,
        "Same colour, second group along the horizontal axis."),
    box("Difference in percentage points = 35 − 15 = ", 20,
        "Percentage points are just one reading taken away from the other.",
        phase="substitute",
        say="Both readings are already percentages, so the gap between them "
            "is measured in <strong>percentage points</strong>: subtract."),
    box("Check: 15 + 20 = ", 35,
        "Add your gap back on to the 2020 reading.",
        done="It returns the 2000 reading, so the gap is right."),
]

# s1: forest 12,400 -> 8,680, 30
s[1]["display"] = ("A tropical forest covered 12,400 km² in 1990 and 8,680 "
                   "km² in 2020. Calculate the percentage decrease.")
s[1]["hint"] = ("Find the area lost, then compare it with the 1990 forest "
                "area.")
s[1]["misconceptions"] = [
    mis("remaining_not_change",
        "That is the share of the 1990 forest still standing, not the share "
        "that has gone.", 70),
    mis("forgot_multiply",
        "That is the decimal fraction. Percentages need one more step.", 0.3),
]
s[1]["guided_steps"] = change_walk(
    "Forest area in 1990, in km², was ", 12400,
    "Loss = 12400 − 8680 = ", 8680, 3720, 0.3, 30, False,
    "Check: 12400 × 0.7 = ", 8680,
    "It returns the 2020 forest area, so the percentage is right.")

# s2: 2m -> 3.5m, 75
s[2]["hint"] = ("Work out the extra millions of urban residents, then compare "
                "that with the year 2000 figure.")
s[2]["misconceptions"] = [
    mis("new_as_percent_of_old",
        "You worked out the 2020 population as a percentage of the 2000 one. "
        "The question asks only about the growth.", 175),
    mis("gave_difference",
        "That is the growth in millions of people, not a percentage.", 1.5),
]
s[2]["guided_steps"] = change_walk(
    "Urban residents in 2000, in millions, was ", 2,
    "Rise = 3.5 − 2 = ", 3.5, 1.5, 0.75, 75, True,
    "Check: 2 × 1.75 = ", 3.5,
    "It returns the 2020 figure in millions, so the percentage is right.")

# s3: land use, commercial 25 of 100, 25
s[3]["hint"] = ("Add all four land uses to get the total, then divide the "
                "commercial figure by it.")
s[3]["misconceptions"] = [
    mis("read_wrong_row",
        "That is a different land use. Check which one the question names.",
        45, note="residential 45 ha of 100 ha"),
    mis("forgot_multiply",
        "That is the proportion as a decimal, not a percentage.", 0.25),
]
s[3]["guided_steps"] = [
    say("The total is not given, so you have to build it before anything else."),
    box("Total land = 45 + 25 + 15 + 15 = ", 100,
        "Add all four land uses together.", post=" ha"),
    box("The commercial area, in hectares, is ", 25,
        "It is the second figure listed in the question."),
    box("25 ÷ 100 = ", 0.25,
        "Divide the part by the total you just built.",
        phase="substitute",
        say="Now the proportion: part ÷ whole."),
    box("0.25 × 100 = ", 25, "Multiply the decimal by 100.", post=" %"),
    box("Check: 0.25 × 100 ha = ", 25,
        "Apply your percentage back to the total land area.",
        done="It returns the commercial area in hectares, so the proportion "
             "is right."),
]

# s4: 4,200 -> 6,930, 65
s[4]["hint"] = ("Find the rise in migrants, then compare it with the 2015 "
                "figure.")
s[4]["misconceptions"] = [
    mis("new_as_percent_of_old",
        "You worked out the 2020 figure as a percentage of the 2015 one, "
        "rather than the size of the rise.", 165),
    mis("gave_difference",
        "That is the rise in numbers of people, not a percentage.", 2730),
]
s[4]["guided_steps"] = change_walk(
    "Net migration in 2015 was ", 4200,
    "Rise = 6930 − 4200 = ", 6930, 2730, 0.65, 65, True,
    "Check: 4200 × 1.65 = ", 6930,
    "It returns the 2020 migration figure, so the percentage is right.")

# s5: tourists 1.8 -> 2.43, 35
s[5]["display"] = ("Tourist arrivals rose from 1.8 million to 2.43 million. "
                   "What is the percentage increase?")
s[5]["solutions"] = [35]
s[5]["hint"] = ("Work out the extra arrivals, then compare them with the "
                "earlier figure.")
s[5]["misconceptions"] = [
    mis("new_as_percent_of_old",
        "You worked out the later figure as a percentage of the earlier one. "
        "The question asks only about the increase.", 135),
    mis("forgot_multiply",
        "That is the decimal fraction. One step still to go.", 0.35),
]
s[5]["guided_steps"] = change_walk(
    "Arrivals before the rise, in millions, was ", 1.8,
    "Rise = 2.43 − 1.8 = ", 2.43, 0.63, 0.35, 35, True,
    "Check: 1.8 × 1.35 = ", 2.43,
    "It returns the later arrivals figure, so the percentage is right.")

# s6: CO2 450 -> 351, 22
s[6]["display"] = ("CO₂ emissions fell from 450 Mt to 351 Mt. What is the "
                   "percentage reduction?")
s[6]["solutions"] = [22]
s[6]["hint"] = ("Find the reduction in megatonnes, then compare it with the "
                "emissions before the fall.")
s[6]["misconceptions"] = [
    mis("remaining_not_change",
        "That is the share of emissions still being produced, not the share "
        "cut.", 78),
    mis("gave_difference",
        "That is the cut measured in megatonnes. The question asks for it as "
        "a percentage.", 99),
]
s[6]["guided_steps"] = change_walk(
    "Emissions before the fall, in Mt, was ", 450,
    "Fall = 450 − 351 = ", 351, 99, 0.22, 22, False,
    "Check: 450 × 0.78 = ", 351,
    "It returns the later emissions figure, so the percentage is right.")

# ==================================================================== GOLD ===
g = pb["gold"]

# g0: 250,000 +12% then -5% -> 266,000
g[0]["hint"] = ("Apply the changes one at a time, and remember the second "
                "change acts on the 2015 population.")
g[0]["misconceptions"] = [
    mis("combined_percentages",
        "You added the two percentages together and applied them once. "
        "Percentages do not add like that: each change acts on the value "
        "that exists at the time.", 267500,
        note="250000 x 1.07"),
    mis("stopped_early",
        "That is the population after the first change only. There is still "
        "a second change to apply.", 280000),
]
g[0]["guided_steps"] = [
    say("Two changes, so two separate stages. Never fold them into one."),
    box("Population at the start, in 2010: ", 250000,
        "It is the figure given for the earliest year."),
    box("First change, a 12% rise: 250000 × 1.12 = ", 280000,
        "A 12% rise means multiplying by 1.12."),
    box("The second change acts on that 2015 figure. 5% of 280000 = ", 14000,
        "Multiply the 2015 population by 0.05.",
        phase="substitute",
        say="Now the second stage. The base has moved: it is the "
            "<strong>2015</strong> population, not the 2010 one."),
    box("280000 − 14000 = ", 266000,
        "Take the 5% you just found off the 2015 population."),
    box("Check: 266000 ÷ 280000 = ", 0.95,
        "Divide your final figure by the 2015 population.",
        done="0.95 is a 5% fall measured from the 2015 population, exactly as "
             "the question describes."),
]

# g1: A 8000 -15%, B 5000 +20% -> 12,800
g[1]["hint"] = ("Work each area out separately, then add the two new "
                "populations together.")
g[1]["misconceptions"] = [
    mis("one_area_only",
        "That is area A after its loss. Area B still has to be worked out and "
        "added on.", 6800),
    mis("ignored_changes",
        "That is the two starting populations added together, with neither "
        "change applied.", 13000),
]
g[1]["guided_steps"] = [
    say("Two places, two different changes. Keep them apart until the very "
        "end."),
    box("Area A's starting population: ", 8000,
        "It is the figure in brackets after area A."),
    box("Area A after losing 15%: 8000 × 0.85 = ", 6800,
        "Losing 15% leaves 85%, so multiply by 0.85."),
    box("Area B after gaining 20%: 5000 × 1.2 = ", 6000,
        "Gaining 20% means multiplying by 1.2.",
        phase="substitute",
        say="Now area B, on its own starting figure."),
    box("Total = 6800 + 6000 = ", 12800,
        "Add the two new populations."),
    box("Check: the two starting populations were 8000 + 5000 = ", 13000,
        "Add the two original figures.",
        done="A lost 1,200 while B gained 1,000, so the total should sit 200 "
             "below 13,000, and it does."),
]

# g2: chart, Nigeria 206 -> 401, 95
g[2]["hint"] = ("Find Nigeria's two bars first, then compare the rise with "
                "the 2020 figure.")
g[2]["misconceptions"] = [
    mis("divided_by_new",
        "You compared the rise with the 2050 projection. Percentage change is "
        "measured against the earlier value.", 49,
        note="195 / 401 x 100 = 48.6, rounded to 49"),
    mis("read_wrong_country",
        "Those are not Nigeria's bars. Find the country label on the "
        "horizontal axis before reading any heights.", 21,
        note="India: (1670-1380)/1380 x 100 = 21"),
]
g[2]["guided_steps"] = [
    say("Locate Nigeria on the chart before touching the numbers. The "
        "countries run left to right along the horizontal axis."),
    box("Counting the country labels from the left, Nigeria is number ", 2,
        "India is first; Nigeria comes next."),
    box("Nigeria's 2020 bar, in millions, reads ", 206,
        "The vertical axis is marked every 200 million, so read carefully "
        "between the gridlines."),
    box("Nigeria's projected 2050 bar reads ", 401,
        "It is the second, differently coloured bar in the same group."),
    box("Rise = 401 − 206 = ", 195,
        "Take the 2020 reading away from the 2050 one.",
        phase="substitute",
        say="Both readings are in place, so now do the percentage change."),
    box("195 ÷ 206 × 100, to the nearest whole number = ", 95,
        "Divide by the 2020 figure, then multiply by 100 and round.",
        post=" %"),
    box("Check: 206 × 2 = ", 412,
        "Double the 2020 reading.",
        done="Doubling would overshoot the 2050 bar slightly, so a rise of "
             "just under 100% fits."),
]

# g3: farmland 420 -> 357, 15
g[3]["hint"] = ("Find the area of farmland lost, then compare it with the "
                "farmland there was before.")
g[3]["misconceptions"] = [
    mis("remaining_not_change",
        "That is the share of farmland still remaining, not the share lost "
        "to urbanisation.", 85),
    mis("gave_difference",
        "That is the loss in square kilometres, not a percentage.", 63),
]
g[3]["guided_steps"] = change_walk(
    "Farmland before urbanisation, in km², was ", 420,
    "Loss = 420 − 357 = ", 357, 63, 0.15, 15, False,
    "Check: 420 × 0.85 = ", 357,
    "It returns the later farmland figure, so the percentage is right.")

# g4: natural increase 24 -> 19, 20.8
g[4]["hint"] = ("Natural increase is the birth rate minus the death rate, so "
                "build it for each period before comparing them.")
g[4]["misconceptions"] = [
    mis("birth_rate_only",
        "You found the change in the birth rate on its own. Natural increase "
        "needs the death rate taken off first.", 33.3,
        note="(42-28)/42 x 100 = 33.3"),
    mis("gave_difference",
        "That is the drop in the natural increase rate per 1000, not a "
        "percentage of what it was.", 5),
]
g[4]["guided_steps"] = [
    say("The question is about <strong>natural increase</strong>, which is "
        "not given. Build it for both periods first."),
    box("Natural increase at the start = 42 − 18 = ", 24,
        "Take the death rate away from the birth rate, both per 1000."),
    box("Natural increase at the end = 28 − 9 = ", 19,
        "Same subtraction, using the later pair of rates."),
    box("Fall in natural increase = 24 − 19 = ", 5,
        "Take the later rate away from the earlier one.",
        phase="substitute",
        say="Now you have two comparable rates, so treat this like any "
            "percentage change."),
    box("5 ÷ 24 × 100, to 1 decimal place = ", 20.8,
        "Divide the fall by the earlier natural increase, then multiply by "
        "100.", post=" %"),
    box("Rough check: 5 ÷ 25 × 100 = ", 20,
        "Round the bottom number up to 25 and redo it in your head.",
        done="Dividing by a slightly smaller number gives a slightly larger "
             "percentage, so a value just above 20 is right."),
]

# ============================================================ descriptions ===
pb["bronze_description"] = ("One move: find the change or the part, then turn "
                            "it into a percentage of the value you started "
                            "with.")
pb["silver_description"] = ("Two moves: build a total or read values off a "
                            "chart first, then do the percentage.")
pb["gold_description"] = ("Several moves: apply changes in sequence, or "
                          "construct the figures you need before finding the "
                          "percentage.")

# ============================================================= tier_guides ===
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one change, one percentage",
        "steps": [
            "Find the value you are measuring from. In a change question it "
            "is the earlier figure; in a proportion question it is the whole.",
            "Work out the part you care about: the rise, the fall, or the "
            "slice of the total.",
            "Divide that part by the starting value, multiply by 100, and say "
            "whether it is an increase or a decrease.",
        ],
        "example": {
            "question": "A hedgerow shrank from 250 m to 200 m. What is the "
                        "percentage decrease?",
            "steps": [
                {"label": "Starting value",
                 "content": "<p>The hedge before the loss: 250 m</p>"},
                {"label": "Change",
                 "content": "<p>250 − 200 = 50 m lost</p>"},
                {"label": "Divide, then × 100",
                 "content": "<p>50 ÷ 250 = 0.2, and 0.2 × 100 = 20</p>"},
                {"label": "Check",
                 "content": "<p>250 × 0.8 = 200 ✓</p>"},
                {"label": "Answer",
                 "content": "<p><strong>20% decrease</strong></p>",
                 "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: build the number you need first",
        "steps": [
            "Silver questions hide one of the two numbers. You may have to "
            "add a set of figures to reach the total, or read two values off "
            "a chart, before you can start.",
            "Once you hold the starting value and the part, the percentage "
            "move is unchanged: part ÷ starting value × 100.",
            "Watch the wording. A gap in percentage points is a plain "
            "subtraction of two percentages, not a percentage change.",
        ],
        "example": {
            "question": "In a village of 400 homes, 90 are second homes and "
                        "60 are rented. The rest are owner occupied. What "
                        "percentage are owner occupied?",
            "steps": [
                {"label": "Whole",
                 "content": "<p>400 homes altogether</p>"},
                {"label": "Build the part",
                 "content": "<p>400 − (90 + 60) = 250 owner occupied</p>"},
                {"label": "Divide, then × 100",
                 "content": "<p>250 ÷ 400 = 0.625, and 0.625 × 100 = 62.5</p>"},
                {"label": "Check",
                 "content": "<p>0.625 × 400 = 250 ✓</p>"},
                {"label": "Answer",
                 "content": "<p><strong>62.5%</strong></p>",
                 "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: changes in sequence",
        "steps": [
            "Gold questions stack two or more stages. Apply each change to "
            "the value that exists at that moment, never back to the "
            "original.",
            "Multipliers keep it tidy: a 12% rise is × 1.12, a 5% fall is × "
            "0.95. Chain them in the order the question gives.",
            "Percentages do not add. A rise then an equal fall does not bring "
            "you back to where you began.",
        ],
        "example": {
            "question": "A shop's footfall of 4,000 rises by 10%, then falls "
                        "by 10%. What is the final footfall?",
            "steps": [
                {"label": "First stage",
                 "content": "<p>4000 × 1.1 = 4400</p>"},
                {"label": "Second stage",
                 "content": "<p>The fall acts on 4400, not 4000: 4400 × 0.9 = "
                            "3960</p>"},
                {"label": "Check",
                 "content": "<p>3960 is below 4000, because the 10% fall was "
                            "taken off a bigger number than the 10% rise was "
                            "added to ✓</p>"},
                {"label": "Answer",
                 "content": "<p><strong>3,960 people</strong></p>",
                 "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ================================================================== guided ===
HOODIE_SVG = (
    '<svg viewBox="0 0 340 96" role="img" aria-label="Two price labels for the '
    'same hoodie: last month twenty pounds, this month twenty five pounds" '
    'width="340" height="96">'
    '<rect x="6" y="18" width="130" height="62" rx="12" fill="#eef2f7" '
    'stroke="#94a3b8"/>'
    '<text x="71" y="42" text-anchor="middle" font-size="13" fill="#475569">'
    'Last month</text>'
    '<text x="71" y="68" text-anchor="middle" font-size="24" fill="#1e293b">'
    '£20</text>'
    '<path d="M150 49 h34" stroke="#64748b" stroke-width="3"/>'
    '<path d="M184 49 l-10 -7 v14 z" fill="#64748b"/>'
    '<rect x="200" y="18" width="130" height="62" rx="12" fill="#fdeeee" '
    'stroke="#ef4444"/>'
    '<text x="265" y="42" text-anchor="middle" font-size="13" fill="#7f1d1d">'
    'This month</text>'
    '<text x="265" y="68" text-anchor="middle" font-size="24" fill="#7f1d1d">'
    '£25</text>'
    '</svg>'
)

pd["guided"] = {
    "opener": {
        "label": "Before any formula",
        "display": "The same hoodie, two months apart:<br>" + HOODIE_SVG,
        "steps": [
            {
                "say": "No formula yet. Just look at the two price labels.",
                "pre": "The price has gone up by £",
                "post": "",
                "answer": 5,
                "hint": "Take last month's price away from this month's.",
            },
            {
                "say": "Now the bit that matters. £5 sounds small on a "
                       "hoodie and huge on a chocolate bar, so it only means "
                       "something next to what you were paying before.",
                "pre": "£5 set against the old £20 price, written as a "
                       "percentage of it: ",
                "post": "%",
                "answer": 25,
                "hint": "Work out how many £5 notes fit into £20, then turn "
                        "that fraction into a percentage out of 100.",
                "done": "That is the whole idea in one line.",
            },
            {
                "say": "You just did <strong>percentage change</strong>: find "
                       "the change, then compare it with the value you "
                       "started from. Geography uses exactly this for "
                       "population growth, deforestation and falling "
                       "emissions. The classic trap is comparing with the "
                       "<strong>new</strong> value instead of the old one.",
            },
        ],
    },
    "teach": {
        "bronze": {
            "label": "Together: your first one",
            "display": "A sand dune fell in height from 6 m to 4.8 m over one "
                       "winter. What is the percentage decrease?",
            "steps": [
                {
                    "say": "First decide which figure you are measuring "
                           "<strong>from</strong>. It is the earlier one.",
                    "pre": "Dune height before the winter, in m: ",
                    "post": "",
                    "answer": 6,
                    "hint": "It is the height the dune started at.",
                },
                {
                    "pre": "Loss = 6 − 4.8 = ",
                    "post": " m",
                    "answer": 1.2,
                    "hint": "Subtract the later height from the earlier one.",
                    "done": "That is the change. On its own it says nothing "
                            "about how serious the loss is.",
                },
                {
                    "say": "Now set the loss against the height you started "
                           "with.",
                    "phase": "substitute",
                    "pre": "1.2 ÷ 6 = ",
                    "post": "",
                    "answer": 0.2,
                    "hint": "Divide the loss by the starting height.",
                },
                {
                    "pre": "0.2 × 100 = ",
                    "post": " %",
                    "answer": 20,
                    "hint": "Multiply the decimal by 100.",
                    "done": "A fifth of the dune's height, gone in a winter.",
                },
                {
                    "say": "Always check by running it forwards.",
                    "pre": "6 × 0.8 = ",
                    "post": " m",
                    "answer": 4.8,
                    "hint": "Losing 20% leaves 80%, so multiply by 0.8.",
                    "done": "It lands on the height the question gave, so 20% "
                            "is right.",
                },
            ],
        },
        "silver": {
            "label": "Together: the total is hidden",
            "display": "A survey of 250 households found 90 with no car, 110 "
                       "with one car and 50 with two or more. What percentage "
                       "own at least one car?",
            "steps": [
                {
                    "say": "The new move at silver: one of the two numbers is "
                           "not handed to you. Find the <strong>whole</strong> "
                           "first.",
                    "pre": "Households surveyed altogether: ",
                    "post": "",
                    "answer": 250,
                    "hint": "The question states it in the first line.",
                },
                {
                    "say": "Now build the part. Two of the three groups own "
                           "at least one car.",
                    "pre": "110 + 50 = ",
                    "post": "",
                    "answer": 160,
                    "hint": "Add the one car group to the two or more group.",
                    "done": "The no car group is deliberately left out.",
                },
                {
                    "say": "With both numbers in hand, the percentage move is "
                           "the usual one.",
                    "phase": "substitute",
                    "pre": "160 ÷ 250 = ",
                    "post": "",
                    "answer": 0.64,
                    "hint": "Divide the part by the whole.",
                },
                {
                    "pre": "0.64 × 100 = ",
                    "post": " %",
                    "answer": 64,
                    "hint": "Multiply the decimal by 100.",
                },
                {
                    "say": "Check it back against the survey.",
                    "pre": "0.64 × 250 = ",
                    "post": " households",
                    "answer": 160,
                    "hint": "Apply your percentage to the 250 households.",
                    "done": "It returns the car owning households, so 64% is "
                            "right.",
                },
            ],
        },
        "gold": {
            "label": "Together: two changes, one after the other",
            "display": "A reservoir held 60 million m³. It fell by 25% during "
                       "a drought, then rose by 40% after heavy rain. How "
                       "much does it hold now?",
            "steps": [
                {
                    "say": "The new move at gold: the second change does not "
                           "act on the original figure.",
                    "pre": "Starting volume, in million m³: ",
                    "post": "",
                    "answer": 60,
                    "hint": "It is the figure before either change.",
                },
                {
                    "pre": "After the 25% drought loss: 60 × 0.75 = ",
                    "post": "",
                    "answer": 45,
                    "hint": "Losing 25% leaves 75%, so multiply by 0.75.",
                    "done": "This is now the reservoir's real volume, so it "
                            "becomes the base for what comes next.",
                },
                {
                    "say": "The rain falls on a reservoir holding 45, not 60.",
                    "phase": "substitute",
                    "pre": "45 × 1.4 = ",
                    "post": "",
                    "answer": 63,
                    "hint": "A 40% rise means multiplying by 1.4.",
                },
                {
                    "say": "Now see why the shortcut fails.",
                    "pre": "The tempting shortcut, −25% then +40% as +15%: 60 "
                           "× 1.15 = ",
                    "post": "",
                    "answer": 69,
                    "hint": "Multiply the starting volume by 1.15.",
                    "done": "That is 6 million m³ too high. Percentages "
                            "cannot be added like that.",
                },
                {
                    "say": "Check the real answer against the start.",
                    "pre": "63 ÷ 60 = ",
                    "post": "",
                    "answer": 1.05,
                    "hint": "Divide the final volume by the starting volume.",
                    "done": "Just 5% above where it began, not 15%, which is "
                            "exactly the point of doing the stages in order.",
                },
            ],
        },
    },
}

# ============================================================= method_card ===
pd["method_card"] = {
    "title": "Percentage Change & Proportions",
    "steps": [
        "Find the difference: new value minus original value",
        "Divide by the ORIGINAL value",
        "Multiply by 100",
        "State increase or decrease",
    ],
    "content": (
        "<p><strong>Percentage change</strong> = ((new − original) ÷ "
        "<strong>original</strong>) × 100. Positive means an increase, "
        "negative a decrease. Geography uses it for population growth, "
        "deforestation, urbanisation and emissions.</p>"
        "<p><strong>Proportion</strong> = (part ÷ whole) × 100. If 15 of 60 "
        "workers are in the primary sector, that is 15 ÷ 60 = 25%.</p>"
        "<p>Three traps: dividing by the new value, forgetting the × 100, and "
        "adding two percentage changes together instead of applying them one "
        "after the other.</p>"
    ),
    "example": (
        "<p><strong>Question:</strong> A town grew from 45,000 to 54,000. "
        "Percentage change?</p>"
        "<p>54,000 − 45,000 = 9,000 → 9,000 ÷ 45,000 = 0.2 → "
        "<strong>20% increase</strong></p>"
    ),
}

out = os.path.join(HERE, "lesson_L07.json")
io.open(out, "w", encoding="utf-8").write(
    json.dumps(pd, indent=1, ensure_ascii=False))
print("written", out)
