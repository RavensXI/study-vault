# -*- coding: utf-8 -*-
"""Build guided practice_data for Geography Skills L04 Population Pyramids."""
import io, json, os, copy

HERE = os.path.dirname(os.path.abspath(__file__))
pd = json.load(io.open(os.path.join(HERE, "_L04_live.json"), encoding="utf-8"))
pb = pd["problem_bank"]
B, S, G = pb["bronze"], pb["silver"], pb["gold"]


# ---------------------------------------------------------------- svg helpers
def blocks_svg():
    s, pitch, base = 14, 16, 130
    parts = []
    for cx, rows, name in ((90, [5, 4, 3, 2, 1], "Shape A"),
                           (250, [3, 3, 3, 3, 2], "Shape B")):
        for i, n in enumerate(rows):
            y = base - (i + 1) * pitch
            x0 = cx - (n * pitch - 2) / 2.0
            for j in range(n):
                parts.append(
                    '<rect x="%.1f" y="%d" width="%d" height="%d" rx="2" '
                    'fill="#cfe0f0" stroke="#5b7fa6" stroke-width="1"/>'
                    % (x0 + j * pitch, y, s, s))
        parts.append('<text x="%d" y="152" text-anchor="middle" '
                     'font-size="13" fill="#2d2a26">%s</text>' % (cx, name))
    parts.append('<text x="170" y="20" text-anchor="middle" font-size="12" '
                 'fill="#5f5a52">bottom row = youngest people</text>')
    return ('<svg viewBox="0 0 340 160" width="100%" role="img" '
            'aria-label="Two block shapes. Shape A has rows of 5, 4, 3, 2 and 1 '
            'blocks from bottom to top. Shape B has rows of 3, 3, 3, 3 and 2 '
            'blocks from bottom to top.">' + "".join(parts) + "</svg>")


def pyramid_svg(bands, scale, tick, label, title):
    """bands: list bottom-first of (name, male, female)."""
    cx, bh, pitch, top = 200.0, 15, 19, 26
    n = len(bands)
    height = top + n * pitch + 34
    maxv = max(max(m, f) for _, m, f in bands)
    span = scale * maxv
    parts = []
    ticks = []
    t = 0
    while t <= maxv + 1e-9:
        ticks.append(t)
        t += tick
    for t in ticks:
        for sgn in (-1, 1):
            x = cx + sgn * t * scale
            parts.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" '
                         'stroke="#d8d2c8" stroke-width="1"/>'
                         % (x, top - 6, x, top + n * pitch))
            parts.append('<text x="%.1f" y="%d" text-anchor="middle" '
                         'font-size="9" fill="#7a736a">%g</text>'
                         % (x, top + n * pitch + 13, t))
            if t == 0:
                break
    for i, (name, m, f) in enumerate(bands):
        y = top + (n - 1 - i) * pitch
        parts.append('<rect x="%.1f" y="%d" width="%.1f" height="%d" '
                     'fill="rgba(59,130,246,0.55)" stroke="#3b82f6" '
                     'stroke-width="0.8"/>' % (cx - m * scale, y, m * scale, bh))
        parts.append('<rect x="%.1f" y="%d" width="%.1f" height="%d" '
                     'fill="rgba(239,68,68,0.5)" stroke="#ef4444" '
                     'stroke-width="0.8"/>' % (cx, y, f * scale, bh))
        parts.append('<text x="8" y="%d" font-size="10" fill="#2d2a26">%s</text>'
                     % (y + 11, name))
    parts.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="#2d2a26" '
                 'stroke-width="1"/>' % (cx, top - 6, cx, top + n * pitch))
    parts.append('<text x="%.1f" y="14" text-anchor="end" font-size="11" '
                 'fill="#3b82f6">males</text>' % (cx - 8))
    parts.append('<text x="%.1f" y="14" font-size="11" fill="#ef4444">females'
                 '</text>' % (cx + 8))
    parts.append('<text x="%.1f" y="%d" text-anchor="middle" font-size="10" '
                 'fill="#5f5a52">%% of total population</text>'
                 % (cx, height - 4))
    return ('<svg viewBox="0 0 340 %d" width="100%%" role="img" aria-label="%s">'
            % (height, label) + "".join(parts) + "</svg>")


BRONZE_BANDS = [("0-14", 8, 8), ("15-29", 7, 7), ("30-44", 5, 5),
                ("45-59", 3, 4), ("60-74", 2, 2), ("75+", 1, 1)]
SILVER_BANDS = [("0-14", 3, 3), ("15-29", 4, 4), ("30-44", 5, 5),
                ("45-59", 6, 6), ("60-74", 5, 6), ("75+", 3, 5)]
GOLD_BANDS = [("0-14", 15, 15), ("15-29", 11, 11), ("30-44", 9, 9),
              ("45-64", 6, 6), ("65-79", 5, 5), ("80+", 4, 4)]


def box(pre, answer, hint, post=None, done=None, phase=None, say=None):
    d = {"pre": pre, "answer": answer, "hint": hint}
    if post:
        d["post"] = post
    if done:
        d["done"] = done
    if phase:
        d["phase"] = phase
    if say:
        d["say"] = say
    return d


def say(text):
    return {"say": text}


# ---------------------------------------------------------------- opener
opener = {
    "display": ("Two countries drew their people as stacks of blocks. Each block "
                "is a group of people, and the bottom row is the youngest.<br>"
                + blocks_svg()),
    "steps": [
        say("Forget the geography for a moment. Just count blocks."),
        box("Count the blocks in the bottom row of Shape A.", 5,
            "The bottom row is the widest row of Shape A. Count the squares one "
            "by one."),
        box("Now count the blocks in the bottom row of Shape B.", 3,
            "Look at the lowest row of the second shape only."),
        box("How many more young people does Shape A have than Shape B?", 2,
            "Take the smaller bottom row away from the bigger one.",
            done="Shape A has the wider base, so it has more children."),
        say("You have just read a <strong>population pyramid</strong>. Each row is "
            "an age group, the bottom row is the youngest, and the width of a row "
            "tells you how many people are in it. A wide base means lots of "
            "children being born. A narrow top means few people reach old age. "
            "Everything else in this lesson is that one idea, with real numbers "
            "attached."),
    ],
}

# ---------------------------------------------------------------- teach walks
teach_bronze = {
    "display": ("Country P. Read the bars off the scale at the bottom: males run "
                "left from the centre line, females run right.<br>"
                + pyramid_svg(BRONZE_BANDS, 8.0, 2,
                              "Population pyramid for Country P with six age "
                              "bands. Bars get steadily shorter from the wide "
                              "0-14 band at the bottom to the short 75+ band at "
                              "the top.", "Country P")),
    "steps": [
        say("Bronze work is <strong>find the band, read the bar</strong>. Nothing "
            "else."),
        box("Counting the bottom band as band 1, which band number is 45-59?", 4,
            "Run your finger up the age labels: 0-14, 15-29, 30-44, then 45-59.",
            done="Always locate the band before you read anything."),
        box("Read the male bar for 0-14 against the scale.", 8,
            "Follow the blue bar left and see which tick it reaches."),
        box("Now read the female bar for 0-14.", 8,
            "Follow the red bar right to the scale."),
        box("Add those two to get the whole 0-14 band as a percentage.", 16,
            "Male share plus female share gives the band total."),
        box("Read the male bar for 75+.", 1,
            "That is the shortest blue bar, right at the top.",
            done="The base band is many times the size of the top band, so this "
                 "is a triangular pyramid: high birth rate, few reaching old age."),
    ],
}

teach_silver = {
    "display": ("Country Q. Same scale, but this pyramid has a very different "
                "shape.<br>"
                + pyramid_svg(SILVER_BANDS, 8.0, 2,
                              "Population pyramid for Country Q with six age "
                              "bands. The 0-14 band is narrow, the middle bands "
                              "are the widest, and the 60-74 and 75+ bands are "
                              "still substantial.", "Country Q")),
    "steps": [
        say("Silver work adds <strong>totalling several bands</strong> and saying "
            "what the shape means."),
        box("Counting the top band as band 1 and working down, which band number "
            "is 60-74?", 2,
            "The top band is 75+, so count down from there."),
        box("Read the male bar for 60-74.", 5,
            "Follow the blue bar left to the nearest tick."),
        box("Read the female bar for 60-74.", 6,
            "Follow the red bar right to the nearest tick."),
        box("Read the male bar for 75+.", 3,
            "Top band, blue side."),
        box("Read the female bar for 75+.", 5,
            "Top band, red side. It is longer than the male one."),
        box("Add all four readings to get the percentage aged 60 and over.", 19,
            "Two bands, two sexes: four numbers to add."),
        box("Now add the male and female bars for 0-14.", 6,
            "Bottom band, both sides.",
            done="Over 60s outnumber under 15s by more than three to one. That is "
                 "an ageing population, and it is the shape that tells you, not "
                 "any single bar."),
    ],
}

teach_gold = {
    "display": ("Country R. Use it to work out the dependency ratio, which "
                "compares people who do not usually work with people who do.<br>"
                + pyramid_svg(GOLD_BANDS, 5.0, 5,
                              "Population pyramid for Country R with six age "
                              "bands: 0-14, 15-29, 30-44, 45-64, 65-79 and 80 "
                              "plus. The base is the widest band and the bars "
                              "narrow steadily towards the top.", "Country R")),
    "steps": [
        say("Gold work adds the <strong>dependency ratio</strong>: "
            "(young + elderly) ÷ working age × 100."),
        box("Counting the bottom band as band 1, which band number is 65-79?", 5,
            "0-14, 15-29, 30-44, 45-64, then 65-79."),
        box("Add male and female for 0-14 to get the young percentage.", 30,
            "Both sides of the base band."),
        box("Add male and female for 65-79 and for 80+ to get the elderly "
            "percentage.", 18,
            "Four numbers: two bands, two sexes."),
        box("Add young and elderly together to get the dependants.", 48,
            "Dependants are the two ends of the pyramid combined."),
        box("Subtract that from 100 to get the working age percentage.", 52,
            "Everyone who is not a dependant is of working age here."),
        box("Now divide dependants by workers and multiply by 100. Give a whole "
            "number.", 92,
            "Dependants go on top of the division, workers underneath.",
            phase="substitute"),
        box("Check: take your ratio away from 100.", 8,
            "A ratio under 100 means workers still outnumber dependants.",
            done="A small positive gap fits 48 dependants against 52 workers, so "
                 "the ratio is just below 100 as expected."),
    ],
}

pd["guided"] = {
    "opener": opener,
    "teach": {"bronze": teach_bronze, "silver": teach_silver, "gold": teach_gold},
}

# ---------------------------------------------------------------- tier guides
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: find the band, read the bar",
        "steps": [
            "Ages stack upwards: the <strong>bottom</strong> row is the youngest, "
            "the top row is the oldest.",
            "Males are drawn to the left of the centre line, females to the right. "
            "Read each bar against the scale.",
            "Judge the shape by comparing the width of the base with the width of "
            "the top.",
        ],
        "example": {
            "question": "On a pyramid, the male 10-14 bar reaches 6 and the female "
                        "10-14 bar reaches 5. What percentage of the population is "
                        "aged 10 to 14?",
            "steps": [
                {"label": "Locate the band",
                 "content": "<p>Count up from the base: 0-4, 5-9, 10-14. That is "
                            "the third row.</p>"},
                {"label": "Read both sides",
                 "content": "<p>Male 6, female 5. Each side is a share of the "
                            "whole population, not of its own sex.</p>"},
                {"label": "Check",
                 "content": "<p>Both readings sit between the 4 and 8 ticks, so a "
                            "total in double figures is sensible.</p>"},
                {"label": "Answer", "isAnswer": True, "is_answer": True,
                 "content": "<p>6 + 5 = <strong>11%</strong></p>"},
            ],
        },
    },
    "silver": {
        "title": "Silver: total several bands and read the story",
        "steps": [
            "To find a group such as 65 and over, add <strong>every</strong> band "
            "inside it, both sexes.",
            "Working age means 15 to 64: start at the 15-19 band and stop at 60-64.",
            "Bulges and dips are events. A bulge is a generation born when births "
            "were high; a dip is a war, a policy or migration.",
        ],
        "example": {
            "question": "Bands 65-74 (male 3, female 4) and 75+ (male 2, female 4). "
                        "What percentage is aged 65 and over?",
            "steps": [
                {"label": "List the bands",
                 "content": "<p>65 and over covers 65-74 and 75+, so four bars in "
                            "all.</p>"},
                {"label": "Add them",
                 "content": "<p>3 + 4 + 2 + 4.</p>"},
                {"label": "Check",
                 "content": "<p>Female bars are longer at both ages, which fits "
                            "women living longer, so the total is credible.</p>"},
                {"label": "Answer", "isAnswer": True, "is_answer": True,
                 "content": "<p><strong>13%</strong> aged 65 and over</p>"},
            ],
        },
    },
    "gold": {
        "title": "Gold: dependency ratios and what the shape predicts",
        "steps": [
            "Dependants are the under 15s plus the over 64s. Everyone else counts "
            "as working age.",
            "Dependency ratio = (dependants ÷ working age) × 100. It is dependants "
            "per 100 workers, so it can go above 100.",
            "To predict, age the pyramid: add the years on and ask which band the "
            "bulge lands in.",
        ],
        "example": {
            "question": "A country has 30% under 15 and 10% aged 65 and over. "
                        "Calculate its dependency ratio.",
            "steps": [
                {"label": "Dependants",
                 "content": "<p>30 + 10 = 40% of the population.</p>"},
                {"label": "Workers",
                 "content": "<p>100 − 40 = 60% of the population.</p>"},
                {"label": "Check",
                 "content": "<p>Dependants are fewer than workers, so the ratio "
                            "must come out below 100.</p>"},
                {"label": "Answer", "isAnswer": True, "is_answer": True,
                 "content": "<p>(40 ÷ 60) × 100 = <strong>67</strong> dependants "
                            "per 100 workers</p>"},
            ],
        },
    },
}

# ---------------------------------------------------------------- descriptions
pb["bronze_description"] = ("Find an age band on the pyramid, read a single bar "
                            "off the scale, and name the shape.")
pb["silver_description"] = ("Add several bands together and explain what a bulge, "
                            "a dip or a narrow base is telling you.")
pb["gold_description"] = ("Calculate dependency ratios and work out what the "
                          "pyramid predicts for the years ahead.")

# ---------------------------------------------------------------- method card
pd["method_card"] = {
    "title": "Population Pyramids",
    "steps": [
        "Bottom row is youngest; males left, females right",
        "Read each bar against the % scale, then add both sexes",
        "Compare base width with top width to name the shape",
        "Dependency ratio = (young + elderly) ÷ working age × 100",
    ],
    "content": ("<p>A <strong>population pyramid</strong> is a double bar chart of "
                "age and sex. Age groups stack upwards from the youngest at the "
                "bottom.</p><p><strong>Three shapes:</strong> a wide base "
                "narrowing sharply to a point means a high birth rate and low life "
                "expectancy. Roughly even bars from bottom to middle mean a stable, "
                "wealthier population. A base narrower than the middle means an "
                "ageing, shrinking population.</p><p><strong>Features:</strong> a "
                "bulge is a generation born when births were high; an indentation "
                "is a war, a policy or emigration; long bars at the top mean high "
                "life expectancy.</p>"),
    "example": ("<p><strong>Question:</strong> 40% are under 15 and 5% are 65 or "
                "over. Find the dependency ratio.</p><p><strong>Step 1:</strong> "
                "Dependants = 40 + 5 = 45%.</p><p><strong>Step 2:</strong> Working "
                "age = 100 − 45 = 55%.</p><p><strong>Answer:</strong> "
                "(45 ÷ 55) × 100 = <strong>82</strong> dependants per 100 "
                "workers.</p>"),
}


# ---------------------------------------------------------------- bank rewrite
def setp(p, hint, misc, steps=None, skip=None, display=None, options=None,
         solutions=None):
    p["hint"] = hint
    p["misconceptions"] = misc
    p.pop("guided_steps", None)
    p.pop("guided_skip_reason", None)
    if steps is not None:
        p["guided_steps"] = steps
    if skip is not None:
        p["guided_skip_reason"] = skip
    if display is not None:
        p["display"] = display
    if options is not None:
        p["options"] = options
    if solutions is not None:
        p["solutions"] = solutions


def mc(pattern, message, expect, note=None):
    d = {"pattern": pattern, "message": message, "expect": expect}
    if note:
        d["note"] = note
    return d


# ---- BRONZE ---------------------------------------------------------------
setp(B[0],
     "Compare how wide the bottom row is with how wide the top row is.",
     [mc("pyramid_upside_down",
         "You have matched the wrong end of the pyramid. The bottom row is the "
         "youngest age group, so a wide base is about births, not about old age.",
         1),
      mc("shapes_all_alike",
         "Pyramid shapes differ enormously between countries. Compare the width "
         "of the base with the width of the top before you decide.", 3)],
     steps=[
         say("Start by working out where you are on the pyramid."),
         box("Counting the bottom bar as row 1, which row number is the 15-19 age "
             "group?", 4,
             "Read the age labels up the side: 0-4, 5-9, 10-14, then 15-19."),
         box("Read the male bar for 0-4 off the scale.", 9,
             "Blue side, bottom row. Ignore the minus sign, it only sends the bar "
             "left."),
         box("Now read the male bar for 75+, the top row.", 0.2,
             "It is a very short blue bar, less than one whole unit.",
             phase="substitute"),
         box("How many times longer is the 0-4 male bar than the 75+ male bar?",
             45,
             "Divide the bottom reading by the top reading."),
         box("Check the base another way: add male and female for 0-4.", 17.5,
             "Both sides of the bottom row.",
             done="Almost a fifth of everyone is under 5, while the over 75s "
                  "barely register. That gap is the signature of a high birth "
                  "rate with a low life expectancy."),
     ])

setp(B[1],
     "The bars get shorter as you go up, so start your comparison at the bottom "
     "row.",
     [mc("read_top_down",
         "You have read the pyramid upside down. Age runs upwards, so the oldest "
         "people are at the top and the youngest at the base.", 3),
      mc("assume_middle_bulge",
         "You have gone for the middle of the pyramid. On this shape every bar is "
         "shorter than the one below it, so check the very bottom row.", 2)],
     steps=[
         say("Locate yourself first, then read."),
         box("Counting the bottom bar as row 1, which row number is 30-34?", 7,
             "Count the age labels upwards: 0-4 is 1, 5-9 is 2, and so on."),
         box("Read the male bar for 0-4.", 9,
             "Bottom row, blue side."),
         box("Read the female bar for 0-4.", 8.5,
             "Bottom row, red side.", phase="substitute"),
         box("Add them to get the whole 0-4 band.", 17.5,
             "Male share plus female share."),
         box("Now do the same for 30-34 to compare.", 8.5,
             "Male 4.5 and female 4 on that row.",
             done="The bottom band is double the 30-34 band, and every band above "
                  "0-4 is shorter than the one below, so no other band can beat "
                  "it."),
     ])

setp(B[2],
     "Ask what the bars do as you move up: shrink steadily, stay similar, or widen.",
     [mc("even_read_as_triangle",
         "Even bars are not a triangle. A triangular shape needs each bar to be "
         "clearly shorter than the one below it.", 0),
      mc("bulge_read_as_inverted",
         "An inverted shape needs the base to be narrower than the middle. Look "
         "again at what happens between age 0 and age 60.", 2)],
     skip="Evaluative shape classification from a written description: there are "
          "no plotted values to read or compute, so a numeric walk would be "
          "invented rather than derived.")

setp(B[3],
     "Count the age labels up from the base to land on the right row, then read "
     "the blue side only.",
     [mc("row_miscount",
         "You have read one row too high. Count the age labels up from the bottom "
         "until you reach 40-44.", 4.2),
      mc("added_both_sexes",
         "You have added both sides of the pyramid. The question asks for males "
         "only, which is one side of the centre line.", 8)],
     steps=[
         say("Find the row before you read anything off it."),
         box("Counting the bottom bar as row 1, which row number is 40-44?", 9,
             "0-4, 5-9, 10-14, 15-19, 20-24, 25-29, 30-34, 35-39, then 40-44."),
         box("Warm up on the row above it: read the male bar for 45-49.", 4.2,
             "Blue side, one row higher than the one you need."),
         box("Now read the male bar for 40-44.", 4,
             "Blue side, the row you located.", phase="substitute"),
         box("Check: subtract your 40-44 reading from your 45-49 reading.", 0.2,
             "Take the smaller from the larger.",
             done="A small positive gap is right: on this pyramid the bars widen "
                  "slightly towards middle age, so 40-44 should sit just inside "
                  "45-49."),
     ])

setp(B[4],
     "The base of a pyramid only ever shows the youngest children, so ask what "
     "makes that group small.",
     [mc("narrow_means_more",
         "You have read narrow as meaning more. A short bar means fewer people in "
         "that age group, not more.", 0),
      mc("death_rate_at_base",
         "Death rates show themselves at the top of a pyramid, where people stop "
         "surviving. The base is about how many are being born.", 2)],
     skip="Evaluative recall of what a pyramid feature means: there is no "
          "stimulus and no quantity to work with.")

setp(B[5],
     "Add twenty years to the ages in the bulge and see which age band they land "
     "in.",
     [mc("aged_wrong_band",
         "You have aged the wrong part of the pyramid. Add the twenty years to "
         "the bulge, not to the base.", 1),
      mc("narrow_base_growth",
         "Rapid growth needs a wide base. Check what a narrow base says about how "
         "many children are being born.", 2)],
     steps=[
         say("To predict from a pyramid you simply age it."),
         box("Someone aged 45 today will be how old in 20 years?", 65,
             "Add twenty to their current age."),
         box("And someone aged 65 today?", 85,
             "Add twenty again.", phase="substitute"),
         box("The base holds children aged 0-4. How old will the oldest of them "
             "be in 20 years?", 24,
             "Add twenty to the top of that band."),
         box("Working age runs from 15 to 64. Of the three ages you have just "
             "worked out (65, 85 and 24), how many fall inside that range?", 1,
             "Check each one against 15 to 64 in turn.",
             done="Only one of the three is still working, and the narrow base "
                  "means very few replacements are coming through behind them."),
     ])

B[6]["options"] = [
    "High dependency ratio, because many young dependants rely on each worker",
    "Low dependency ratio, because few people depend on workers",
    "Dependency ratio is not related to age structure",
    "High dependency ratio, because many elderly dependants rely on each worker",
]
setp(B[6],
     "Work out what is left for the working age group once the under 15s are "
     "taken out.",
     [mc("elderly_dependants",
         "Right idea, wrong dependants. Under 15s are counted at the base of the "
         "pyramid, not at the top.", 3),
      mc("dependants_lighten_load",
         "Nearly half the population is under 15. Think about whether that makes "
         "the load on each worker lighter or heavier.", 1)],
     steps=[
         say("Turn the shape into numbers, then judge it."),
         box("If 44% are under 15, what percentage are aged 15 or over?", 56,
             "Take 44 away from 100."),
         box("Suppose 4% are also over 65. What percentage is then working age, "
             "15 to 64?", 52,
             "Take the elderly share off the figure you just found."),
         box("Add the two dependant groups together.", 48,
             "Young dependants plus elderly dependants.", phase="substitute"),
         box("Divide dependants by workers and multiply by 100. Give a whole "
             "number.", 92,
             "Dependants on top, workers underneath."),
         box("Check: take your ratio away from 100.", 8,
             "A ratio just under 100 means workers barely outnumber dependants.",
             done="Nearly one dependant for every worker, and almost all of them "
                  "are children, which is exactly what a very wide base does to a "
                  "country."),
     ])

setp(B[7],
     "Match the shape to what birth and death rates are doing at each stage of "
     "the model.",
     [mc("late_stage_triangle",
         "The last stage of the model has a narrow base. A steep triangle points "
         "to the opposite end of the model.", 3),
      mc("stage_four_triangle",
         "Stage 4 gives a fairly even column. A steep triangle means births are "
         "still far higher than that.", 2)],
     skip="Evaluative recall linking a shape to a stage of a model: no figure and "
          "no values, so any boxes would be invented.")

# ---- SILVER ---------------------------------------------------------------
S[0]["display"] = ("The population pyramid shows Japan's age structure. "
                   "Approximately what percentage of the total population is aged "
                   "65 and over? Give your answer to the nearest whole number.")
setp(S[0],
     "Three bands sit at 65 and over, and each one has a male bar and a female bar.",
     [mc("one_side_only",
         "You have added only one side of the pyramid. Every age band has a male "
         "bar and a female bar, and both count towards the total.", 8.5),
      mc("missed_top_band",
         "The oldest band is missing from your total. Anything above the 65-69 row "
         "is also aged 65 and over.", 11.7)],
     steps=[
         say("Find the bands you need before you add anything."),
         box("Counting the top bar as row 1 and working down, which row number is "
             "65-69?", 3,
             "The top row is 75+, then 70-74, then 65-69."),
         box("Add the three male bars for 65-69, 70-74 and 75+.", 8.5,
             "Blue side only: 3, 2.5 and 3."),
         box("Now add the three female bars for the same rows.", 10.7,
             "Red side: 3.2, 3 and 4.5.", phase="substitute"),
         box("Add the two totals together.", 19.2,
             "Males aged 65 and over plus females aged 65 and over."),
         box("Round that to the nearest whole number.", 19,
             "Look at the first digit after the decimal point.",
             done="Roughly one person in five is 65 or over, and the female total "
                  "beats the male one, which is what the longer red bars at the "
                  "top should give."),
     ])

S[1]["display"] = ("Country A has a wide base and a narrow top. Country B has "
                   "even bars throughout. Which country is likely to have a "
                   "higher population growth rate?")
S[1]["options"] = [
    "Country A, because a wide base means a high birth rate and rapid growth",
    "Country B, because even bars mean steady growth",
    "Both have equal growth rates",
    "Population pyramids cannot tell you anything about growth",
]
setp(S[1],
     "Growth depends on how many are being born, so compare the youngest bands in "
     "each country.",
     [mc("even_means_growing",
         "Even bars mean a steady population, not a fast growing one. Compare the "
         "size of the youngest bands in each country.", 1),
      mc("pyramid_shows_nothing",
         "A pyramid does show growth: the width of the base tells you how many "
         "children there are compared with everyone else.", 3)],
     skip="Evaluative comparison of two pyramids described only in words: neither "
          "shape carries plotted values, so there is nothing to compute.")

setp(S[2],
     "Work out which years the missing generation would have been born in, then "
     "ask what was happening then.",
     [mc("war_instead_of_policy",
         "A war lowers births only while it is being fought and usually thins the "
         "male side more. Check the birth years of the missing band first.", 1),
      mc("emigration_instead",
         "Emigration moves people who were still born in the normal numbers. A "
         "dip this deep means fewer births, not fewer stayers.", 2)],
     steps=[
         say("Turn ages into birth years, then line them up with the dates."),
         box("Take the survey year as 2025. Someone aged 25 was born in which "
             "year?", 2000,
             "Subtract the age from the survey year."),
         box("And someone aged 35?", 1990,
             "Subtract again."),
         box("The policy in option one began in 1979. How many years before 1990 "
             "was that?", 11, "Take 1979 from 1990.", phase="substitute"),
         box("Of your two birth years, 1990 and 2000, how many fall after 1979?",
             2,
             "Compare each birth year with 1979.",
             done="The whole missing generation was born after the policy started, "
                  "so the dates line up: the dip covers exactly the years the "
                  "policy was in force."),
     ])

setp(S[3],
     "Compare the base with the bands above it: each generation has to replace the "
     "one before it.",
     [mc("elderly_cause_growth",
         "A large elderly population adds deaths, not births. Look at the base to "
         "count the future parents.", 3),
      mc("stays_stable",
         "Staying level needs each generation to be about the size of the one "
         "before it. Compare the base with the widest band.", 2)],
     steps=[
         say("Locate the widest part of the pyramid first, then compare."),
         box("Counting the bottom bar as row 1, which row holds the longest male "
             "bar?", 10,
             "The blue bars grow to a maximum somewhere in middle age, then "
             "shrink. Count up to it."),
         box("Read the male bar for 0-4.", 2,
             "Bottom row, blue side."),
         box("Read the male bar for that widest row, 45-49.", 4.5,
             "Blue side, the row you located.", phase="substitute"),
         box("How many times wider is the widest male bar than the 0-4 male bar?",
             2.25,
             "Divide the larger reading by the smaller one."),
         box("Check the whole base: add male and female for 0-4.", 3.8,
             "Both sides of the bottom row.",
             done="The base is less than half the size of the parents' generation, "
                  "so each new generation is smaller than the one replacing it."),
     ])

setp(S[4],
     "The gap only appears in the oldest band, so think about who survives to get "
     "there.",
     [mc("birth_ratio_reason",
         "Slightly more boys than girls are born everywhere, so births cannot "
         "explain a gap that appears only at the top of the pyramid.", 1),
      mc("elderly_migration",
         "Migration in old age is rare and small. This gap widens with age, which "
         "points at survival instead.", 2)],
     skip="Evaluative reasoning about a cause: the problem carries no figure and "
          "no values, so a numeric walk would be invented.")

S[5]["display"] = ("Using the population pyramid, add together the male and female "
                   "bars for every working age band, 15-19 up to 60-64. What is "
                   "the combined total of those bars?")
S[5]["hint"] = ("Add the male bar and the female bar for every age band from 15-19 "
                "up to 60-64.")
S[5]["solutions"] = [66.5]
setp(S[5],
     "Add the male bar and the female bar for every age band from 15-19 up to "
     "60-64.",
     [mc("one_side_only",
         "Only one side of the pyramid has been added. Every band has a male bar "
         "and a female bar.", 35.5),
      mc("included_65_69",
         "One band too many. Working age stops at 64, so the 65-69 row is outside "
         "it.", 67.9)],
     steps=[
         say("Mark off the working age section of the pyramid before you add."),
         box("Counting the bottom bar as row 1, which row number is 15-19?", 4,
             "0-4, 5-9, 10-14, then 15-19."),
         box("How many rows are there from 15-19 up to 60-64 inclusive?", 10,
             "Count the age labels in that block, including both ends."),
         box("Add the male bars for those ten rows.", 35.5,
             "Blue side: 7, 6, 5, 4, 3.5, 3, 2.5, 2, 1.5 and 1.",
             phase="substitute"),
         box("Now add the female bars for the same ten rows.", 31,
             "Red side: 6.5, 5.5, 4.5, 3.5, 3, 2.5, 2, 1.5, 1.2 and 0.8."),
         box("Add the two totals together.", 66.5,
             "Male working age total plus female working age total.",
             done="The bars either side of this block are the children and the "
                  "elderly, and there are far more children, so a working age "
                  "block that is well under three quarters of the pyramid is what "
                  "a wide base gives you."),
     ])

setp(S[6],
     "A gap that appears in one working age band, in one sex only, is usually "
     "about people arriving rather than people dying.",
     [mc("births_explain_gap",
         "Birth ratios are close to even everywhere, so births cannot create a gap "
         "that shows up only in the 25-40 bands.", 3),
      mc("women_die_younger",
         "Women live longer than men almost everywhere. A gap this large in one "
         "working age band points at people arriving, not at survival.", 1)],
     skip="Evaluative explanation of a cause: the pattern is described in words "
          "with no values attached, so there is nothing to compute.")

# ---- GOLD -----------------------------------------------------------------
G[0]["display"] = ("Country X has 60 million people. 42% are under 15 and 4% are "
                   "over 65. Calculate the dependency ratio, to the nearest whole "
                   "number.")
setp(G[0],
     "Dependants go on top of the division and the working age group goes "
     "underneath.",
     [mc("divided_by_total",
         "You have compared dependants with the whole population. The ratio "
         "compares them with the working age group only.", 46),
      mc("ratio_inverted",
         "The two parts are the wrong way round. Dependants belong on top of the "
         "division, workers underneath.", 117)],
     steps=[
         say("Set the population out in three groups first."),
         box("What percentage are dependants, young and elderly together?", 46,
             "Add the under 15 share to the over 65 share."),
         box("What percentage are therefore of working age?", 54,
             "Take the dependants away from 100."),
         box("The country has 60 million people. How many million are dependants?",
             27.6,
             "Find 46% of 60 million.", phase="substitute"),
         box("And how many million are of working age?", 32.4,
             "Find 54% of 60 million, or take your last answer from 60."),
         box("Now divide dependants by workers and multiply by 100, to the nearest "
             "whole number.", 85,
             "Use the two millions figures; the percentages give the same result.",
             done="Working from millions gives the same ratio as working from "
                  "percentages, which confirms the division was set up the right "
                  "way round."),
     ])

G[1]["options"] = [
    "Country B, because its more even shape means a larger proportion of "
    "working age adults",
    "Country A, because its high birth rate means more workers",
    "They are the same, because the same total population means the same labour "
    "force",
    "Country A, because young populations work harder",
]
setp(G[1],
     "The labour force is the middle of the pyramid, so compare how much of each "
     "shape sits between 15 and 64.",
     [mc("children_as_workers",
         "A high birth rate fills the base with children, and children are not in "
         "the labour force.", 1),
      mc("same_total_same_workers",
         "Equal totals can still be split very differently by age. Compare the "
         "middle section of each pyramid.", 2)],
     skip="Evaluative comparison of two shapes given only in words: no plotted or "
          "stated values exist for either country.")

setp(G[2],
     "Turn both features into birth years, then put those years in order.",
     [mc("rising_births",
         "A rising birth rate would widen the base, not narrow it. Check which end "
         "of the pyramid is shrinking.", 2),
      mc("earliest_stage",
         "The first stage of the model has a very wide base. A bulge of young "
         "adults above a shrinking base points the other way.", 3)],
     steps=[
         say("Convert the ages into birth years so you can date each feature."),
         box("Take the year as 2025. Someone aged 20 was born in which year?",
             2005, "Subtract the age from 2025."),
         box("And someone aged 30?", 1995, "Subtract again."),
         box("How many years wide is that birth window, 1995 to 2005?", 10,
             "Take the earlier year from the later one.", phase="substitute"),
         box("The narrowing base holds children born in the last five years, so "
             "from which year onwards?", 2020,
             "Take five off the survey year."),
         box("How many years pass between the end of the bulge births in 2005 and "
             "the start of the narrow base in 2020?", 15,
             "Subtract one year from the other.",
             done="Births were high across a full decade, then clearly lower 15 "
                  "years later, so the pyramid carries a past boom and a falling "
                  "birth rate at the same time."),
     ])

G[3]["display"] = ("Japan's dependency ratio was 64 in 2020. If the elderly "
                   "percentage rises from 28% to 35% by 2040 while the young "
                   "percentage stays at 12%, what will the new dependency ratio "
                   "be? Give your answer to the nearest whole number.")
setp(G[3],
     "Rebuild the working age percentage from the new figures before you divide.",
     [mc("divided_by_total",
         "Dividing by the whole population loses the point of the ratio, which is "
         "the load carried per worker.", 47),
      mc("old_working_age",
         "The working age share changes when the elderly share changes. Work it "
         "out again from the new figures before dividing.", 78)],
     steps=[
         say("Rebuild the three groups for 2040 before touching the old ratio."),
         box("What percentage will be dependants in 2040?", 47,
             "Add the young percentage to the new elderly percentage."),
         box("What percentage will be of working age?", 53,
             "Take the dependants away from 100."),
         box("Divide dependants by workers and multiply by 100, to the nearest "
             "whole number.", 89,
             "Dependants on top, workers underneath.", phase="substitute"),
         box("How much higher is that than the 2020 ratio of 64?", 25,
             "Subtract 64 from your new ratio."),
         box("Check: take your new ratio away from 100.", 11,
             "A positive result means workers still just outnumber dependants.",
             done="Dependants at 47% against workers at 53% must give a ratio a "
                  "little under 100, so a small positive gap here confirms the "
                  "calculation."),
     ])

setp(G[4],
     "Work out which years the missing generation would have been born in, then "
     "match those years to an event.",
     [mc("whole_cohort_emigrated",
         "Whole ten year cohorts do not emigrate, and the bands either side stayed "
         "wide. Think about what was happening when the missing band was born.",
         1),
      mc("age_specific_disease",
         "A disease that killed one ten year band and spared both its neighbours "
         "is very unlikely. Look at the birth years instead.", 2)],
     steps=[
         say("Date the waist, then see which event sits in those years."),
         box("The waist covers ages 70 to 80. How many years wide is that band?",
             10, "Take 70 from 80."),
         box("The Second World War ran from 1939 to 1945. How many years is that?",
             6, "Take 1939 from 1945."),
         box("If the pyramid was drawn in 2015, someone aged 70 was born in which "
             "year?", 1945,
             "Subtract the age from the year of the pyramid.", phase="substitute"),
         box("And someone aged 80?", 1935, "Subtract again."),
         box("Check: take the war's end year, 1945, away from 2015 to see which "
             "age the waist should start at.", 70,
             "Subtract 1945 from 2015.",
             done="The waist begins at exactly the age you get by dating the end "
                  "of the war, so the missing births sit inside the war years "
                  "rather than beside them."),
     ])

# ---------------------------------------------------------------- write
out = os.path.join(HERE, "lesson_L04.json")
io.open(out, "w", encoding="utf-8").write(
    json.dumps(pd, ensure_ascii=False, indent=1))
print("written", out, len(json.dumps(pd)))
