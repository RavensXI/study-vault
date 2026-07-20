# -*- coding: utf-8 -*-
"""Build guided practice_data for Geography Skills L02 (Pie Charts & Histograms)."""
import json, io, os, copy

HERE = os.path.dirname(os.path.abspath(__file__))
pd = json.load(io.open(os.path.join(HERE, "_live_L02.json"), encoding="utf-8"))

B = pd["problem_bank"]["bronze"]
S = pd["problem_bank"]["silver"]
G = pd["problem_bank"]["gold"]


def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say: d["say"] = say
    if done: d["done"] = done
    if phase: d["phase"] = phase
    return d


def say(t):
    return {"say": t}


def mis(pattern, message, expect):
    return {"pattern": pattern, "check": pattern, "message": message,
            "expect": expect, "note": "expect derived by committing the error"}


# ---------------------------------------------------------------- SVGs
SVG_OPENER = (
    '<svg viewBox="0 0 300 150" role="img" width="100%" style="max-width:360px" '
    'aria-label="Pie chart of lunch choices in a class of 24 students: half the '
    'circle is chips, a quarter is sandwiches, a quarter is pasta">'
    '<path d="M70,70 L70,10 A60,60 0 0,1 70,130 Z" fill="#f0c36d" stroke="#ffffff" stroke-width="2"/>'
    '<path d="M70,70 L70,130 A60,60 0 0,1 10,70 Z" fill="#a3c4a8" stroke="#ffffff" stroke-width="2"/>'
    '<path d="M70,70 L10,70 A60,60 0 0,1 70,10 Z" fill="#a9bede" stroke="#ffffff" stroke-width="2"/>'
    '<rect x="150" y="34" width="14" height="14" fill="#f0c36d"/>'
    '<text x="172" y="46" font-size="13" fill="#2d2a26">Chips</text>'
    '<rect x="150" y="62" width="14" height="14" fill="#a3c4a8"/>'
    '<text x="172" y="74" font-size="13" fill="#2d2a26">Sandwiches</text>'
    '<rect x="150" y="90" width="14" height="14" fill="#a9bede"/>'
    '<text x="172" y="102" font-size="13" fill="#2d2a26">Pasta</text>'
    '</svg>')

SVG_TEACH_B = (
    '<svg viewBox="0 0 300 150" role="img" width="100%" style="max-width:360px" '
    'aria-label="Pie chart of land use on a farm: wheat 50 percent, barley 25 percent, '
    'grass 15 percent, woodland 10 percent">'
    '<path d="M70,70 L70,10 A60,60 0 0,1 70,130 Z" fill="#f0c36d" stroke="#ffffff" stroke-width="2"/>'
    '<path d="M70,70 L70,130 A60,60 0 0,1 10,70 Z" fill="#d9a06b" stroke="#ffffff" stroke-width="2"/>'
    '<path d="M70,70 L10,70 A60,60 0 0,1 34.7,21.5 Z" fill="#a3c4a8" stroke="#ffffff" stroke-width="2"/>'
    '<path d="M70,70 L34.7,21.5 A60,60 0 0,1 70,10 Z" fill="#6f9d76" stroke="#ffffff" stroke-width="2"/>'
    '<rect x="150" y="20" width="14" height="14" fill="#f0c36d"/>'
    '<text x="172" y="32" font-size="13" fill="#2d2a26">Wheat 50%</text>'
    '<rect x="150" y="48" width="14" height="14" fill="#d9a06b"/>'
    '<text x="172" y="60" font-size="13" fill="#2d2a26">Barley 25%</text>'
    '<rect x="150" y="76" width="14" height="14" fill="#a3c4a8"/>'
    '<text x="172" y="88" font-size="13" fill="#2d2a26">Grass 15%</text>'
    '<rect x="150" y="104" width="14" height="14" fill="#6f9d76"/>'
    '<text x="172" y="116" font-size="13" fill="#2d2a26">Woodland 10%</text>'
    '</svg>')

SVG_TEACH_S = (
    '<svg viewBox="0 0 300 150" role="img" width="100%" style="max-width:360px" '
    'aria-label="Pie chart of where 400 shoppers buy food: supermarket 45 percent, '
    'online 25 percent, market stall 20 percent, corner shop 10 percent">'
    '<path d="M70,70 L70,10 A60,60 0 0,1 88.5,127.1 Z" fill="#a9bede" stroke="#ffffff" stroke-width="2"/>'
    '<path d="M70,70 L88.5,127.1 A60,60 0 0,1 12.9,88.5 Z" fill="#f0c36d" stroke="#ffffff" stroke-width="2"/>'
    '<path d="M70,70 L12.9,88.5 A60,60 0 0,1 34.7,21.5 Z" fill="#a3c4a8" stroke="#ffffff" stroke-width="2"/>'
    '<path d="M70,70 L34.7,21.5 A60,60 0 0,1 70,10 Z" fill="#c98b8b" stroke="#ffffff" stroke-width="2"/>'
    '<rect x="150" y="20" width="14" height="14" fill="#a9bede"/>'
    '<text x="172" y="32" font-size="13" fill="#2d2a26">Supermarket 45%</text>'
    '<rect x="150" y="48" width="14" height="14" fill="#f0c36d"/>'
    '<text x="172" y="60" font-size="13" fill="#2d2a26">Online 25%</text>'
    '<rect x="150" y="76" width="14" height="14" fill="#a3c4a8"/>'
    '<text x="172" y="88" font-size="13" fill="#2d2a26">Market stall 20%</text>'
    '<rect x="150" y="104" width="14" height="14" fill="#c98b8b"/>'
    '<text x="172" y="116" font-size="13" fill="#2d2a26">Corner shop 10%</text>'
    '</svg>')

# Histogram, unequal widths. x: 0-80 mm mapped 20..180 (2 px per mm)
# y: frequency density 0-4 mapped 120..20 (25 px per unit)
SVG_TEACH_G = (
    '<svg viewBox="0 0 200 150" role="img" width="100%" style="max-width:400px" '
    'aria-label="Histogram of pebble sizes with unequal class widths, frequency density '
    'on the vertical axis: 0 to 10 mm density 2.0, 10 to 20 mm density 4.0, '
    '20 to 40 mm density 1.5, 40 to 80 mm density 0.5">'
    '<line x1="20" y1="20" x2="20" y2="120" stroke="#2d2a26" stroke-width="1"/>'
    '<line x1="20" y1="120" x2="185" y2="120" stroke="#2d2a26" stroke-width="1"/>'
    '<rect x="20" y="70" width="20" height="50" fill="#a9bede" stroke="#4a6fa5" stroke-width="1"/>'
    '<rect x="40" y="20" width="20" height="100" fill="#a9bede" stroke="#4a6fa5" stroke-width="1"/>'
    '<rect x="60" y="82.5" width="40" height="37.5" fill="#a9bede" stroke="#4a6fa5" stroke-width="1"/>'
    '<rect x="100" y="107.5" width="80" height="12.5" fill="#a9bede" stroke="#4a6fa5" stroke-width="1"/>'
    '<text x="18" y="124" font-size="7" fill="#2d2a26" text-anchor="middle">0</text>'
    '<text x="40" y="128" font-size="7" fill="#2d2a26" text-anchor="middle">10</text>'
    '<text x="60" y="128" font-size="7" fill="#2d2a26" text-anchor="middle">20</text>'
    '<text x="100" y="128" font-size="7" fill="#2d2a26" text-anchor="middle">40</text>'
    '<text x="180" y="128" font-size="7" fill="#2d2a26" text-anchor="middle">80</text>'
    '<text x="100" y="140" font-size="8" fill="#2d2a26" text-anchor="middle">Pebble length (mm)</text>'
    '<text x="16" y="122" font-size="7" fill="#2d2a26" text-anchor="end">0</text>'
    '<text x="16" y="97" font-size="7" fill="#2d2a26" text-anchor="end">1</text>'
    '<text x="16" y="72" font-size="7" fill="#2d2a26" text-anchor="end">2</text>'
    '<text x="16" y="47" font-size="7" fill="#2d2a26" text-anchor="end">3</text>'
    '<text x="16" y="24" font-size="7" fill="#2d2a26" text-anchor="end">4</text>'
    '<text x="8" y="70" font-size="8" fill="#2d2a26" text-anchor="middle" '
    'transform="rotate(-90 8 70)">Frequency density</text>'
    '</svg>')

# ---------------------------------------------------------------- BRONZE
B[0]["hint"] = "Match the label in the key to its slice, then read the share printed for it."
B[0]["misconceptions"] = [
    mis("read_wrong_sector",
        "That share belongs to a different slice. Match the colour in the key to the sector before you read it.",
        [20]),
    mis("gave_angle_not_percent",
        "You have converted the share into degrees. The question asks for the percentage shown on the chart itself.",
        [144]),
]
B[0]["guided_steps"] = [
    say("Find the right slice first. Reading a pie chart goes wrong far more often from picking the wrong sector than from the arithmetic."),
    box("Sectors shown in the pie chart: ", 5, "Count the entries listed in the key.",
        done="Knowing how many slices there are stops you mixing two of them up."),
    box("Counting down the key from the top, Natural Gas is at position ", 1,
        "Read the key from the top and find the label you were asked about."),
    box("Percentage printed for that sector: ", 40,
        "Now read the share for the slice you located, not the biggest slice.",
        phase="substitute"),
    box("Check: total of all five sector percentages = ", 100,
        "Add every share in the key together.",
        done="A pie chart is one whole thing, so the shares must total a full 100%. They do, so your reading sits in a valid chart."),
]

B[1]["hint"] = "A full pie chart is one complete turn, so a share out of a hundred becomes that share of a whole turn."
B[1]["misconceptions"] = [
    mis("repeated_percentage",
        "You have written the share again rather than an angle. A percentage still has to be turned into part of a full turn.",
        [60]),
    mis("divided_turn_by_share",
        "The full turn has been divided by the share. The share is a part of the circle, so it multiplies the full turn.",
        [6]),
]
B[1]["guided_steps"] = [
    say("A pie chart is one complete turn of <strong>360°</strong>. A sector's angle is its share of that turn."),
    box("Total of the three percentages given: ", 100, "Add primary, secondary and tertiary."),
    box("Percentage in the primary sector: ", 60, "Read the primary figure from the question."),
    box("That share as a decimal (percentage divided by a hundred): ", 0.6,
        "Dividing by a hundred moves the digits two places to the right.", phase="substitute"),
    box("Multiply that decimal by 360 to get the angle in degrees: ", 216,
        "Work out that fraction of a full turn.", done="This is the primary sector angle."),
    box("Check: angle left for the other two sectors (360 minus your angle) = ", 144,
        "Take your sector angle away from a full turn.",
        done="The other two sectors are 40% together, and 144° is 40% of 360°, so the circle adds up."),
]

B[2]["hint"] = "Find the named cause in the key first, then read the share printed for that slice."
B[2]["misconceptions"] = [
    mis("read_wrong_sector",
        "That is the share for a different cause. Check the colour in the key against the sector before reading.",
        [25]),
    mis("gave_angle_not_percent",
        "You have turned the share into degrees. The question asks for the percentage itself.",
        [126]),
]
B[2]["guided_steps"] = [
    say("Locate the slice before you read anything."),
    box("Causes shown in the pie chart: ", 5, "Count the entries in the key."),
    box("Counting down the key from the top, Cattle Ranching is at position ", 1,
        "Find the label you were asked about in the key."),
    box("Percentage printed for that sector: ", 35,
        "Read the share for the slice you just located.", phase="substitute"),
    box("Check: total of all five percentages = ", 100, "Add every share in the key.",
        done="The five causes account for the whole of the deforestation, so they must total 100%, and they do."),
]

B[3]["hint"] = "The class widths are all the same here, so the height of the bar is the frequency."
B[3]["misconceptions"] = [
    mis("off_by_one_bar",
        "You have read one bar too far along. Count the class intervals across the horizontal axis before reading a height.",
        [35]),
    mis("added_two_classes",
        "Two neighbouring classes have been added together. Only one class interval was asked for.",
        [80]),
]
B[3]["guided_steps"] = [
    say("The horizontal axis is split into age classes. Work out which bar you need before reading any height."),
    box("Bars drawn on the histogram: ", 6, "Count the class intervals along the bottom."),
    box("Counting from the left, the 20-30 class is bar number ", 3,
        "0-10 is the first bar, 10-20 the second."),
    box("Height of that bar on the vertical axis: ", 45,
        "Trace the top of the bar across to the frequency axis.", phase="substitute",
        say="Every class here is ten years wide, so the bar height <strong>is</strong> the frequency."),
    box("Check: height of the bar immediately to its right (the 30-40 class) = ", 35,
        "Trace the next bar across to the vertical axis.",
        done="Your bar is the tallest on the chart and its neighbour is lower, which confirms you read the right one."),
]

B[4]["hint"] = "Work out the share of the survey that is commercial, then take that share of a full turn."
B[4]["misconceptions"] = [
    mis("wrong_category",
        "A different land use has been used. Find the commercial figure in the list first.",
        [150]),
    mis("gave_percentage_not_angle",
        "That is the share as a percentage, not an angle. A whole pie chart is a full turn of 360°.",
        [25]),
]
B[4]["guided_steps"] = [
    say("An angle on a pie chart is the category's share of one complete turn."),
    box("Plots surveyed altogether: ", 360, "The survey total is given at the start of the question."),
    box("Plots recorded as commercial: ", 90, "Find commercial in the list of land uses."),
    box("Commercial plots divided by the total, as a decimal: ", 0.25,
        "Work out what fraction of the survey is commercial.", phase="substitute"),
    box("Multiply that decimal by 360 for the angle in degrees: ", 90,
        "Take that fraction of a full turn.", done="This is the commercial sector angle."),
    box("Check: degrees left for the other three land uses (360 minus your angle) = ", 270,
        "Subtract your sector angle from a full turn.",
        done="The other three uses cover 270 plots and get 270°, so with this total each plot is worth exactly one degree."),
]

B[5]["hint"] = "Match the label 'Other' to its colour in the key, then read the share for that slice."
B[5]["misconceptions"] = [
    mis("read_neighbour_sector",
        "That share belongs to a neighbouring group in the key. Match the label you were asked about to its colour first.",
        [8]),
    mis("gave_angle_not_percent",
        "You have turned the share into degrees. The question asks for the percentage on the chart.",
        [36]),
]
B[5]["guided_steps"] = [
    say("Match the label to its slice before reading a number."),
    box("Groups shown in the pie chart: ", 5, "Count the entries in the key."),
    box("Counting down the key from the top, 'Other' is at position ", 5,
        "Grouped leftovers are usually listed last in a key."),
    box("Percentage printed for that sector: ", 10,
        "Read the share for the slice you located.", phase="substitute"),
    box("Check: total of the four named groups (all except 'Other') = ", 90,
        "Add the four groups that are named individually.",
        done="The named groups leave a gap up to 100%, and your reading fills it exactly, so the slice was read correctly."),
]

B[6]["hint"] = "Read the industry share from the key, then take that share of the total usage."
B[6]["misconceptions"] = [
    mis("wrong_sector_share",
        "A different sector's share has been used. Find industry in the key before you multiply.",
        [350]),
    mis("divided_by_share",
        "The total has been divided by the share. Taking a share of an amount means multiplying by it.",
        [25]),
]
B[6]["guided_steps"] = [
    say("Read the share off the chart first, then apply it to the total."),
    box("Sectors shown in the pie chart: ", 3, "Count the entries in the key."),
    box("Percentage of water used by industry: ", 20, "Find industry in the key and read its share."),
    box("That share as a decimal: ", 0.2,
        "Dividing by a hundred moves the digits two places to the right.", phase="substitute"),
    box("Multiply by the total usage of 500 billion litres: ", 100,
        "Work out that fraction of the total supply.", done="This is the industry usage in billions of litres."),
    box("Check: agriculture in the same way, in billions of litres = ", 350,
        "Take the agriculture share of the same total.",
        done="Agriculture 350, industry 100 and domestic 50 rebuild the whole 500 billion litres, so the shares were applied correctly."),
]

B[7]["display"] = ("The chart shows the number of sunny days per month for a tropical city. "
                   "What is the total number of sunny days from January to June?")
B[7]["hint"] = "Work out how far along the chart June sits before you start adding bar heights."
B[7]["misconceptions"] = [
    mis("summed_whole_year",
        "The whole year has been totalled. Stop adding once you reach the sixth bar.",
        [236]),
    mis("stopped_a_month_early",
        "You have stopped one bar early. Count the months carefully, including the last one named.",
        [109]),
]
B[7]["guided_steps"] = [
    say("Work out how far along the chart to go before adding anything."),
    box("Bars drawn on the chart: ", 12, "There is one bar for each month."),
    box("Bars covering January to June: ", 6,
        "Count the months from January up to and including June."),
    box("Total of the first three bars (Jan, Feb, Mar): ", 71,
        "Read each of the first three heights and add them.", phase="substitute"),
    box("Total of the next three bars (Apr, May, Jun): ", 59,
        "Read the next three heights and add them."),
    box("Check: add your two subtotals together = ", 130,
        "Combine the two halves of the six month period.",
        done="Six bars used out of twelve, and the two subtotals agree with the running total, so nothing was missed or double counted."),
]

# ---------------------------------------------------------------- SILVER
S[0]["hint"] = "Read the secondary share from the key, then take that share of the town's population."
S[0]["misconceptions"] = [
    mis("wrong_sector_share",
        "A different sector's share has been used. Match secondary to its colour in the key first.",
        [15600]),
    mis("divided_by_share",
        "The population has been divided by the share. A share of a total means multiply, not divide.",
        [1200]),
]
S[0]["guided_steps"] = [
    say("Read the share off the chart, then apply it to the population."),
    box("Sectors shown in the pie chart: ", 4, "Count the entries in the key."),
    box("Counting down the key from the top, Secondary is at position ", 2,
        "The key runs primary, secondary, tertiary, quaternary."),
    box("Percentage printed for that sector: ", 20,
        "Read the share for the slice you located.", phase="substitute"),
    box("That share as a decimal: ", 0.2, "Divide the percentage by a hundred."),
    box("Multiply by the 24,000 residents: ", 4800,
        "Take that fraction of the town's population.",
        done="This is the number of people working in the secondary sector."),
    box("Check: the tertiary sector in the same way, in people = ", 15600,
        "Take the tertiary share of the same population.",
        done="Applying all four shares this way rebuilds the 24,000 residents, so the method is being used correctly."),
]

S[1]["hint"] = "Work out how many degrees one vehicle is worth, then scale it up to the cars."
S[1]["misconceptions"] = [
    mis("used_half_turn",
        "Half a turn has been used instead of a whole one. A complete pie chart is a full turn.",
        [105]),
    mis("wrong_vehicle_row",
        "A different row of the survey has been used. Find the cars figure before you scale it up.",
        [60]),
]
S[1]["guided_steps"] = [
    say("An angle is the category's share of one full turn of <strong>360°</strong>."),
    box("Vehicles counted altogether: ", 720, "The survey total is given in the question."),
    box("Vehicles that were cars: ", 420, "Find cars in the list."),
    box("Degrees each single vehicle is worth (360 shared between them all): ", 0.5,
        "Divide a full turn by the number of vehicles counted.", phase="substitute"),
    box("Multiply that by the number of cars: ", 210,
        "Scale the degrees per vehicle up to the cars.", done="This is the cars sector angle."),
    box("Check: the angle for vans in the same way, in degrees = ", 60,
        "Scale the degrees per vehicle up to the vans.",
        done="Every category worked this way totals 360°, a full circle, so the scaling is right."),
]

S[2]["hint"] = "Decide which class intervals sit inside the range before you read any bar heights."
S[2]["misconceptions"] = [
    mis("one_class_only",
        "Only one class has been counted. The range asked for spans more than one class interval.",
        [24]),
    mis("included_class_below",
        "You have started one bar too far to the left. Check where the lower limit sits on the horizontal axis.",
        [52]),
]
S[2]["guided_steps"] = [
    say("Decide which bars are inside the range before adding anything."),
    box("Bars drawn on the histogram: ", 5, "Count the class intervals along the horizontal axis."),
    box("Bars falling between 2m and 6m: ", 2,
        "The classes run 0-2, 2-4, 4-6, 6-8 and 8-10."),
    box("Height of the 2-4 bar: ", 20,
        "Trace the top of that bar across to the frequency axis.", phase="substitute"),
    box("Height of the 4-6 bar: ", 24, "Trace the next bar across to the frequency axis."),
    box("Add the two heights: ", 44, "Combine the two classes inside the range.",
        done="This is the number of dunes between 2m and 6m."),
    box("Check: all five bars total 70 dunes, so dunes outside the range = ", 26,
        "Take your answer away from the whole sample.",
        done="The dunes inside and outside the range rebuild the full sample of 70, so no class has been counted twice."),
]

S[3]["hint"] = "Read the nuclear share from the key, then turn that share into part of a full turn."
S[3]["misconceptions"] = [
    mis("repeated_percentage",
        "You have written the share from the chart again. It still has to be converted into an angle.",
        [10]),
    mis("used_half_turn",
        "Half a turn has been used. A complete pie chart is a whole turn.",
        [18]),
]
S[3]["guided_steps"] = [
    say("Take the share off the chart, then convert it into an angle."),
    box("Energy sources shown in the pie chart: ", 5, "Count the entries in the key."),
    box("Counting down the key from the top, Nuclear is at position ", 4,
        "The key runs oil, coal, natural gas, nuclear, renewables."),
    box("Percentage printed for nuclear: ", 10,
        "Read the share for the slice you located.", phase="substitute"),
    box("That share as a decimal: ", 0.1, "Divide the percentage by a hundred."),
    box("Multiply by 360 for the angle in degrees: ", 36,
        "Take that fraction of a full turn.", done="This is the nuclear sector angle."),
    box("Check: the renewables angle to the nearest degree = ", 22,
        "Take the renewables share of a full turn and round it.",
        done="Renewables have the smaller share and get the smaller angle, so the conversion is behaving properly."),
]

S[4]["hint"] = "Read the hydraulic action share from the key, then take that share of the recorded events."
S[4]["misconceptions"] = [
    mis("largest_sector_instead",
        "The largest slice has been used rather than the one named. Match the label in the key first.",
        [80]),
    mis("repeated_percentage",
        "That is the share from the chart, not a number of events. Apply the share to the total recorded.",
        [35]),
]
S[4]["guided_steps"] = [
    say("Find the sector, then turn its share into a number of events."),
    box("Causes shown in the pie chart: ", 4, "Count the entries in the key."),
    box("Percentage for hydraulic action: ", 35, "Match the label in the key to its slice."),
    box("That share as a decimal: ", 0.35, "Divide the percentage by a hundred.", phase="substitute"),
    box("Multiply by the 200 recorded events: ", 70,
        "Take that fraction of all the events.", done="This is the number of hydraulic action events."),
    box("Check: abrasion events worked the same way = ", 80,
        "Take the abrasion share of the same total.",
        done="Abrasion has the larger share and comes out with more events, so the shares are being applied the right way round."),
]

S[5]["hint"] = "The modal class is the class with the tallest bar, so find it before reading a frequency."
S[5]["misconceptions"] = [
    mis("gave_width_not_frequency",
        "That is a value from the horizontal axis, not a count. The question asks how many measurements fall in the class.",
        [5]),
    mis("totalled_all_bars",
        "Every bar has been added together. Only the modal class was asked for.",
        [50]),
]
S[5]["guided_steps"] = [
    say("The modal class is simply the class with the tallest bar."),
    box("Bars drawn on the histogram: ", 5, "Count the class intervals along the horizontal axis."),
    box("Counting from the left, the tallest bar is number ", 3,
        "Compare the bar heights across the chart."),
    box("Height of that bar on the frequency axis: ", 18,
        "Trace the top of the tallest bar across to the vertical axis.", phase="substitute"),
    box("Check: total of the other four bar heights = ", 32,
        "Add the heights of every bar except the tallest.",
        done="The other bars plus your reading rebuild the 50 points measured, so the tallest bar was read correctly."),
]

S[6]["display"] = ("Employment in the UK is compared for two years. In 1900: Primary 40%, "
                   "Secondary 40%, Tertiary 20%. In 2020: Primary 1%, Secondary 15%, "
                   "Tertiary 84%. By how many percentage points did the tertiary sector increase?")
S[6]["hint"] = "Percentage points are just the gap between the two tertiary percentages."
S[6]["misconceptions"] = [
    mis("wrong_sector_compared",
        "A different sector has been compared. Find the tertiary figure in both sets before subtracting.",
        [39]),
    mis("percentage_change_instead",
        "That is a percentage change. Percentage points are the plain difference between two percentages, with no extra scaling.",
        [320]),
]
S[6]["guided_steps"] = [
    say("Percentage points are the plain gap between two percentages."),
    box("Tertiary percentage in 1900: ", 20, "Read the first set of figures."),
    box("Tertiary percentage in 2020: ", 84, "Read the second set of figures."),
    box("Subtract the earlier figure from the later one: ", 64,
        "Take the 1900 tertiary share away from the 2020 one.", phase="substitute",
        done="This is the rise in percentage points."),
    box("Check: total of the three 2020 percentages = ", 100,
        "Add the 2020 primary, secondary and tertiary shares.",
        done="Both years total 100%, so the two tertiary slices are shares of the same whole and can be compared directly."),
]

# ---------------------------------------------------------------- GOLD
G[0]["options"] = [
    "Yes, 2m out of 50m is 4%, which matches the chart",
    "No, 2m out of 50m is 4%, but the chart shows 8%",
    "No, 2m out of 50m is 2%, but the chart shows 4%",
    "Cannot tell without more data",
]
G[0]["hint"] = "Work out the primary share the government's two numbers give, then compare it with the chart."
G[0]["misconceptions"] = [
    mis("misread_chart_share",
        "The primary share has been read too high off the chart. Check the primary slice value again before comparing.",
        [1]),
    mis("millions_read_as_percent",
        "The 2 million has been treated as a percentage. It first has to be worked out as a share of the whole population.",
        [2]),
]
G[0]["guided_steps"] = [
    say("Do not judge by eye. Test the government's figure against the chart yourself."),
    box("Sectors shown in the pie chart: ", 3, "Count the entries in the key."),
    box("Percentage the chart gives for the primary sector: ", 4,
        "Match the primary label in the key to its slice."),
    box("Now use the government figures. 2 million divided by 50 million, as a decimal: ", 0.04,
        "Divide the primary workers by the whole population.", phase="substitute"),
    box("That decimal turned into a percentage: ", 4,
        "Multiply the decimal by a hundred.",
        done="This is the primary share the government's own numbers imply."),
    box("Check: chart percentage subtracted from your calculated percentage = ", 0,
        "Take one percentage away from the other.",
        done="A gap of nothing means the two agree, so the chart is not overstating or understating the primary sector."),
    say("The two figures agree, so the correct option is the first one: the chart is accurate."),
]

G[1]["hint"] = "The vertical axis is a density, so each bar's frequency is its height multiplied by its class width."
G[1]["misconceptions"] = [
    mis("added_densities",
        "The bar heights have been added straight. On this chart the height is a density, not a count.",
        [4]),
    mis("same_width_for_both",
        "Both classes have been given the same width. Check the class boundaries on the horizontal axis.",
        [40]),
]
G[1]["guided_steps"] = [
    say("The vertical axis here is <strong>frequency density</strong>, so a bar height is not a count."),
    box("Bars drawn on the histogram: ", 5, "Count the class intervals along the horizontal axis."),
    box("Bars covering ages 20 to 50: ", 2,
        "The classes run 0-10, 10-20, 20-30, 30-50 and 50-80."),
    box("The 20-30 class: density multiplied by its width of 10 gives a frequency of ", 25,
        "Multiply the density of that bar by its class width.", phase="substitute"),
    box("The 30-50 class is 20 wide. Its frequency is ", 30,
        "Multiply that bar's density by its wider class width."),
    box("Add the two frequencies: ", 55, "Combine the two classes inside the range.",
        done="This is the number of people aged 20 to 50."),
    box("Check: the 10-20 class worked the same way = ", 30,
        "Multiply the tallest bar's density by its class width.",
        done="The tallest bar holds the same number as the low wide 30-50 bar, which is exactly why density must be multiplied by width instead of read as a count."),
]

G[2]["hint"] = "Decide which of the listed sources are renewable before converting anything into degrees."
G[2]["misconceptions"] = [
    mis("only_other_renewables",
        "Only one of the renewable sources has been used. Check which entries in the list are renewable.",
        [40]),
    mis("nuclear_counted_renewable",
        "Nuclear has been counted as renewable. It is low carbon, but its fuel is not replaced naturally.",
        [133]),
]
G[2]["guided_steps"] = [
    say("Decide which categories are renewable before any arithmetic."),
    box("Categories listed in the question: ", 4, "Count the energy sources given."),
    box("Combined percentage of the two renewable sources: ", 27,
        "Add the hydro share to the other renewables share."),
    box("That combined share as a decimal: ", 0.27,
        "Divide the combined percentage by a hundred.", phase="substitute"),
    box("Multiply by 360 and round to the nearest whole degree: ", 97,
        "Take that fraction of a full turn, then round.",
        done="This is the renewables sector angle."),
    box("Check: the fossil fuels angle to the nearest degree = ", 227,
        "Take the fossil fuel share of a full turn and round it.",
        done="Renewables, fossil fuels and the 36° nuclear sector total a full 360°, so the angles fill the circle exactly."),
]

G[3]["display"] = ("A survey of migrants arriving in a UK city recorded their origins: EU 45%, "
                   "Asia 30%, Africa 15%, Other 10%. If 8,000 migrants arrived last year, "
                   "how many came from Asia or Africa combined?")
G[3]["hint"] = "Add the two shares together first, then apply the combined share to the total arrivals."
G[3]["misconceptions"] = [
    mis("one_region_only",
        "Only one of the two named regions has been included. Combine both shares before you multiply.",
        [2400]),
    mis("gave_percentage_not_people",
        "That is the combined share, not a number of people. It still has to be applied to the total who arrived.",
        [45]),
]
G[3]["guided_steps"] = [
    say("Combine the two shares first, then apply them to the total."),
    box("Origin groups listed: ", 4, "Count the categories given in the question."),
    box("Asia and Africa percentages added together: ", 45, "Add the two named shares."),
    box("That combined share as a decimal: ", 0.45,
        "Divide the combined percentage by a hundred.", phase="substitute"),
    box("Multiply by the 8,000 arrivals: ", 3600,
        "Take that fraction of everyone who arrived.",
        done="This is the number who came from Asia or Africa."),
    box("Check: migrants from the EU and Other combined = ", 4400,
        "Add those two shares and take them of the same total.",
        done="The two groups rebuild the full 8,000 arrivals, so nobody has been counted twice or missed."),
]

G[4]["display"] = ("Pebble sizes from a river were grouped into unequal classes and plotted as "
                   "frequency density. The 0-5mm class has a frequency density of 4.0 and the "
                   "5-20mm class has a frequency density of 2.0. How many more pebbles were in "
                   "the 5-20mm class than the 0-5mm class?")
G[4]["hint"] = "Turn each density into a frequency using its own class width before comparing them."
G[4]["misconceptions"] = [
    mis("compared_densities",
        "The densities have been compared directly. A density is not a count until it is multiplied by the class width.",
        [2]),
    mis("subtracted_wrong_way",
        "The subtraction is the wrong way round. Check which class the question asks you to compare with which.",
        [-10]),
]
G[4]["guided_steps"] = [
    say("Densities cannot be compared directly. Turn each one into a count first."),
    box("Width of the 0-5mm class, in mm: ", 5,
        "Subtract the lower class boundary from the upper one."),
    box("Width of the 5-20mm class, in mm: ", 15,
        "Subtract the lower class boundary from the upper one."),
    box("Frequency of the 0-5mm class (density times its width): ", 20,
        "Multiply that class density by the width you just found.", phase="substitute"),
    box("Frequency of the 5-20mm class: ", 30,
        "Multiply that class density by its own wider class width."),
    box("Subtract the smaller frequency from the larger: ", 10,
        "Compare the two counts you have worked out.",
        done="This is how many more pebbles the wider class held."),
    box("Check: pebbles in the two classes altogether = ", 50,
        "Add the two frequencies.",
        done="The wider class holds more than half of the pebbles even though its bar is lower, confirming that density had to be multiplied by width."),
]

# ---------------------------------------------------------------- descriptions
pd["problem_bank"]["bronze_description"] = (
    "Read one value straight off a pie chart or an equal width histogram, and turn a share into a pie chart angle")
pd["problem_bank"]["silver_description"] = (
    "Apply a share to a given total, or combine classes, moving between percentages, angles and real numbers")
pd["problem_bank"]["gold_description"] = (
    "Use frequency density with unequal class widths, and test whether a stated figure agrees with the chart")

# ---------------------------------------------------------------- tier guides
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: read a share straight off the chart",
        "steps": [
            "A pie chart is one whole thing cut into slices. Each slice is labelled with its share, so reading one is really a matching job: find the label in the key, then read its sector.",
            "A histogram with <strong>equal class widths</strong> is just as direct. The bars touch because the data is continuous, and the height of a bar is its frequency.",
            "To turn a share into an angle, take it out of a hundred and multiply by 360, because a full circle is one whole turn.",
        ],
        "example": {
            "question": "A pie chart shows land use in a village: farmland 50%, woodland 25%, houses 25%. What angle does woodland take?",
            "steps": [
                {"label": "Locate", "content": "<p>Find woodland in the key and read its share: 25%.</p>"},
                {"label": "Convert", "content": "<p>(25 ÷ 100) × 360 = 0.25 × 360</p>"},
                {"label": "Check", "content": "<p>Woodland is a quarter of the village, and 90° is a quarter of a full turn. ✓</p>"},
                {"label": "Answer", "content": "<p><strong>90°</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: turn a share into a real number",
        "steps": [
            "Silver questions hand you a total as well as a chart: a population, a sample size, a number of recorded events.",
            "Read the share off the chart, divide it by a hundred, then multiply by the total. That gives the real number the slice stands for. Going the other way, an angle is (value ÷ total) × 360.",
            "Two or more classes can be combined, but add the bars or the shares first, then do the arithmetic once.",
        ],
        "example": {
            "question": "A pie chart shows visitors to a park: adults 60%, children 40%. If 250 people visited, how many were children?",
            "steps": [
                {"label": "Locate", "content": "<p>Children take 40% of the circle.</p>"},
                {"label": "Apply", "content": "<p>(40 ÷ 100) × 250 = 0.4 × 250</p>"},
                {"label": "Check", "content": "<p>Adults would be 150, and 150 + 100 = 250, the whole sample. ✓</p>"},
                {"label": "Answer", "content": "<p><strong>100 children</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: unequal class widths and testing claims",
        "steps": [
            "When a histogram has <strong>unequal class widths</strong> the vertical axis shows frequency density, not frequency. A tall narrow bar can hold fewer items than a low wide one.",
            "Frequency = frequency density × class width, which is the area of the bar. Work each class out on its own, then add or subtract.",
            "Gold also asks you to judge a claim. Work out the figure the numbers give, then compare it with what the chart shows before you decide.",
        ],
        "example": {
            "question": "A histogram has classes 0-10 (density 3.0) and 10-30 (density 2.0). How many items are in the 10-30 class?",
            "steps": [
                {"label": "Width", "content": "<p>The 10-30 class is 30 − 10 = 20 wide.</p>"},
                {"label": "Multiply", "content": "<p>Frequency = 2.0 × 20</p>"},
                {"label": "Check", "content": "<p>The 0-10 class has the taller bar but only 3.0 × 10 = 30 items, fewer than the wide class. ✓</p>"},
                {"label": "Answer", "content": "<p><strong>40 items</strong></p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ---------------------------------------------------------------- guided
pd["guided"] = {
    "opener": {
        "label": "Before any formulas",
        "display": "A class of 24 students said what they had for lunch. Here is the result.<br>" + SVG_OPENER,
        "steps": [
            {"say": "No method needed yet. Just look at how much of the circle each choice takes.",
             "pre": "Students who chose chips: ", "post": "", "answer": 12,
             "hint": "Chips fill half the circle, and there are 24 students in the class."},
            {"say": "You did that by size, not by counting. A slice's share of the circle is its share of the class.",
             "pre": "Degrees of turn the chips slice takes: ", "post": "°", "answer": 180,
             "hint": "All the way round is 360°, and chips take half of that."},
            {"say": "That is the whole technique. A <strong>pie chart</strong> turns a share of a group into a share of one full turn, so half the class becomes half the circle, which is 180°. Read it forwards to get an angle, or backwards to get a number of people. A <strong>histogram</strong> does the same job for measurements grouped into ranges: it is the size of the bar, not its label, that carries the number."},
        ],
    },
    "teach": {
        "bronze": {
            "label": "Together: your first one",
            "display": "The pie chart shows land use on a farm. What percentage is barley, and what angle does that sector take?<br>" + SVG_TEACH_B,
            "steps": [
                {"say": "Locate before you read. Start by seeing how the chart is split.",
                 "pre": "Land uses shown in the key: ", "post": "", "answer": 4,
                 "hint": "Count the entries listed beside the chart."},
                {"pre": "Counting down the key from the top, barley is at position ", "post": "", "answer": 2,
                 "hint": "The key runs wheat, barley, grass, woodland.",
                 "done": "Found the slice first. Most pie chart marks are lost here, not in the arithmetic."},
                {"pre": "Percentage printed for that sector: ", "post": "%", "answer": 25,
                 "hint": "Read the share written next to barley in the key."},
                {"say": "Now the new move: turn that share into an angle. A full pie chart is one complete turn of <strong>360°</strong>.",
                 "phase": "substitute",
                 "pre": "That share as a decimal: ", "post": "", "answer": 0.25,
                 "hint": "Divide the percentage by a hundred."},
                {"pre": "Multiply by 360 for the angle in degrees: ", "post": "°", "answer": 90,
                 "hint": "Take that fraction of a full turn.",
                 "done": "A quarter of the farm, a quarter of the circle."},
                {"say": "Check it against the rest of the chart:",
                 "pre": "Total of all four percentages in the key: ", "post": "%", "answer": 100,
                 "hint": "Add wheat, barley, grass and woodland.",
                 "done": "The shares make a whole 100%, so barley really is a quarter and 90° is right."},
            ],
        },
        "silver": {
            "label": "Together: adding the total",
            "display": "400 shoppers said where they buy most of their food. How many use a market stall?<br>" + SVG_TEACH_S,
            "steps": [
                {"say": "Same start as bronze: find the slice on the chart before touching the total.",
                 "pre": "Places shown in the key: ", "post": "", "answer": 4,
                 "hint": "Count the entries listed beside the chart."},
                {"pre": "Counting down the key from the top, the market stall is at position ", "post": "", "answer": 3,
                 "hint": "The key runs supermarket, online, market stall, corner shop."},
                {"pre": "Percentage printed for that sector: ", "post": "%", "answer": 20,
                 "hint": "Read the share written next to the market stall."},
                {"say": "Here is the silver move: the chart gives a share, the question gives a <strong>total</strong>. Put them together.",
                 "phase": "substitute",
                 "pre": "That share as a decimal: ", "post": "", "answer": 0.2,
                 "hint": "Divide the percentage by a hundred."},
                {"pre": "Multiply by the 400 shoppers: ", "post": " shoppers", "answer": 80,
                 "hint": "Take that fraction of everyone surveyed.",
                 "done": "The share has become a real number of people."},
                {"say": "Check by doing the biggest slice the same way:",
                 "pre": "Shoppers using a supermarket: ", "post": "", "answer": 180,
                 "hint": "Take the supermarket share of the same 400 shoppers.",
                 "done": "180 supermarket, 100 online, 80 market and 40 corner shop rebuild all 400 shoppers, so the shares were applied correctly."},
            ],
        },
        "gold": {
            "label": "Together: when the widths differ",
            "display": "This histogram has unequal class widths, so the vertical axis shows frequency density. How many pebbles are longer than 20mm?<br>" + SVG_TEACH_G,
            "steps": [
                {"say": "Locate first. Look at the horizontal axis and see how the classes are split, because they are not all the same width.",
                 "pre": "Bars drawn on the histogram: ", "post": "", "answer": 4,
                 "hint": "Count the blocks along the horizontal axis."},
                {"pre": "Bars covering pebbles longer than 20mm: ", "post": "", "answer": 2,
                 "hint": "The classes run 0-10, 10-20, 20-40 and 40-80.",
                 "done": "Two classes to work out, and they are different widths, which is the whole point of this tier."},
                {"pre": "Width of the 20-40 class, in mm: ", "post": "mm", "answer": 20,
                 "hint": "Subtract the lower class boundary from the upper one."},
                {"say": "Now the gold move: <strong>frequency = frequency density × class width</strong>. The bar's area is the count, not its height.",
                 "phase": "substitute",
                 "pre": "Pebbles in the 20-40 class: ", "post": "", "answer": 30,
                 "hint": "Multiply that bar's density of 1.5 by the width you just found."},
                {"pre": "Pebbles in the 40-80 class: ", "post": "", "answer": 20,
                 "hint": "That class is 40mm wide and its density is 0.5."},
                {"pre": "Add the two classes: ", "post": " pebbles", "answer": 50,
                 "hint": "Combine the two counts you worked out.",
                 "done": "This is the number longer than 20mm."},
                {"say": "Check against the tallest bar on the chart:",
                 "pre": "Pebbles in the 10-20 class (density 4.0, width 10): ", "post": "", "answer": 40,
                 "hint": "Multiply that bar's density by its class width.",
                 "done": "The tallest bar holds fewer pebbles than the two low wide bars together, which is exactly why height alone cannot be read as a count."},
            ],
        },
    },
}

# ---------------------------------------------------------------- method card
pd["method_card"] = {
    "title": "Pie Charts & Histograms",
    "steps": [
        "Pie chart angle = (value ÷ total) × 360",
        "Reading a pie chart: value = (share ÷ 100) × total",
        "Equal class widths: the bar height is the frequency",
        "Unequal class widths: frequency = density × class width",
    ],
    "content": (
        "<p><strong>Pie charts</strong> show parts of a whole. The full circle is 100%, or 360°, "
        "so a sector's angle is its share of one complete turn. To find what a sector is worth, "
        "take its share of the total.</p>"
        "<p><strong>Histograms</strong> show continuous data grouped into class intervals, so the "
        "bars touch. With equal class widths the bar height is the frequency. With unequal class "
        "widths the vertical axis is frequency density, and frequency = density × class width, "
        "which is the area of the bar.</p>"
        "<p>Always check: sectors should total 100% or 360°, and class frequencies should total "
        "the sample size.</p>"
    ),
    "example": (
        "<p><strong>Question:</strong> 120 people named their main transport: car 50%, bus 25%, "
        "walk 15%, cycle 10%. Find the car sector angle and the number of car users.</p>"
        "<p><strong>Angle:</strong> (50 ÷ 100) × 360 = 180°</p>"
        "<p><strong>People:</strong> (50 ÷ 100) × 120 = 60</p>"
    ),
}

out = os.path.join(HERE, "lesson_L02.json")
io.open(out, "w", encoding="utf-8").write(json.dumps(pd, indent=1, ensure_ascii=False))
print("written", out)
