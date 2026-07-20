# -*- coding: utf-8 -*-
"""Build the guided practice_data for Geography Skills L03 (Scatter Graphs & Correlation)."""
import json, io, os

HERE = os.path.dirname(os.path.abspath(__file__))
pd = json.load(io.open(os.path.join(HERE, "_L03_live.json"), encoding="utf-8"))

# ---------------------------------------------------------------- SVG helper
def scatter_svg(aria, pts, xlab, ylab, xticks, yticks, colour="#3b82f6"):
    """pts/xticks/yticks are already in pixel space where needed."""
    s = ['<svg viewBox="0 0 300 210" role="img" aria-label="%s" style="max-width:340px;width:100%%">' % aria]
    s.append('<line x1="45" y1="170" x2="285" y2="170" stroke="#8a8580" stroke-width="1"/>')
    s.append('<line x1="45" y1="20" x2="45" y2="170" stroke="#8a8580" stroke-width="1"/>')
    for (px, py) in pts:
        s.append('<circle cx="%.1f" cy="%.1f" r="4.5" fill="%s"/>' % (px, py, colour))
    for (px, lab) in xticks:
        s.append('<text x="%.1f" y="184" font-size="10" text-anchor="middle" fill="#5a554f">%s</text>' % (px, lab))
    for (py, lab) in yticks:
        s.append('<text x="38" y="%.1f" font-size="10" text-anchor="end" fill="#5a554f">%s</text>' % (py + 3.5, lab))
    s.append('<text x="168" y="203" font-size="11" text-anchor="middle" fill="#2d2a26">%s</text>' % xlab)
    s.append('<text x="13" y="95" font-size="11" text-anchor="middle" fill="#2d2a26" transform="rotate(-90 13 95)">%s</text>' % ylab)
    s.append('</svg>')
    return "".join(s)

# opener: height vs shoe size
op_pts = [(66, 126), (106, 104), (146, 82), (186, 60), (226, 38), (266, 148)]
opener_svg = scatter_svg(
    "Scatter graph of six friends: height in centimetres along the bottom against shoe size up the side. "
    "Five dots climb steadily from left to right; a sixth dot on the far right sits very low.",
    op_pts, "Height (cm)", "Shoe size",
    [(66, "150"), (106, "155"), (146, "160"), (186, "165"), (226, "170"), (266, "175")],
    [(148, "3"), (126, "4"), (104, "5"), (82, "6"), (60, "7"), (38, "8")])

# teach bronze: altitude vs temperature
tb_pts = [(55, 38), (97, 60), (139, 82), (181, 104), (223, 126), (265, 148)]
teach_b_svg = scatter_svg(
    "Scatter graph of six weather stations: altitude in metres along the bottom against mean temperature "
    "in degrees Celsius up the side. The dots fall steadily from left to right.",
    tb_pts, "Altitude (m)", "Temperature (°C)",
    [(55, "0"), (139, "200"), (223, "400"), (265, "500")],
    [(148, "7"), (104, "9"), (60, "11"), (38, "12")], "#059669")

# teach silver: distance from centre vs pedestrian count
ts_pts = [(55, 44), (97, 71), (139, 89), (181, 116), (223, 134), (265, 161)]
teach_s_svg = scatter_svg(
    "Scatter graph of six survey sites: distance from the city centre in metres along the bottom against "
    "pedestrian count up the side. The dots fall steadily from left to right.",
    ts_pts, "Distance from centre (m)", "Pedestrians counted",
    [(55, "0"), (139, "400"), (181, "600"), (265, "1000")],
    [(161, "50"), (116, "100"), (71, "150"), (44, "180")], "#7c3aed")

# teach gold: rainfall vs wheat yield with one anomaly
tg_pts = [(55, 136), (90, 119), (125, 102), (160, 85), (177.5, 153), (195, 68), (230, 51), (265, 34)]
teach_g_svg = scatter_svg(
    "Scatter graph of eight farms: growing season rainfall in millimetres along the bottom against wheat "
    "yield in tonnes per hectare up the side. Seven dots climb steadily from left to right; one dot near "
    "the middle sits far below the rest.",
    tg_pts, "Rainfall (mm)", "Yield (t/ha)",
    [(55, "300"), (177.5, "650"), (265, "900")],
    [(153, "1"), (136, "2"), (102, "4"), (68, "6"), (34, "8")], "#f59e0b")

# ---------------------------------------------------------------- method card
pd["method_card"] = {
    "title": "Scatter Graphs & Correlation",
    "steps": [
        "Plot each pair as one point, with the influencing variable along the bottom",
        "Follow the points left to right: climbing, falling or scattered",
        "Name it: positive, negative or no correlation",
        "Add a line of best fit, read estimates off it, and mark any anomaly"
    ],
    "content": (
        "<p>A <strong>scatter graph</strong> plots two variables against each other to test whether they are "
        "related. The variable doing the influencing goes along the bottom.</p>"
        "<p><strong>Positive correlation:</strong> points climb left to right, so both rise together. "
        "<strong>Negative correlation:</strong> points fall left to right, so one rises as the other drops. "
        "<strong>No correlation:</strong> no pattern at all.</p>"
        "<p>A <strong>line of best fit</strong> runs through the middle of the points with roughly equal "
        "numbers above and below. Reading a value inside the plotted range (interpolation) is reliable; "
        "predicting beyond it (extrapolation) is not.</p>"
        "<p>An <strong>anomaly</strong> sits far from the pattern and usually has a geographical explanation. "
        "Correlation never proves cause.</p>"
    ),
    "example": (
        "<p><strong>Question:</strong> Points plotted for altitude against temperature fall steadily from left "
        "to right. Name the correlation.</p>"
        "<p><strong>Step 1:</strong> Altitude increases along the bottom axis.</p>"
        "<p><strong>Step 2:</strong> Temperature drops as you move right, so they move in opposite "
        "directions.</p>"
        "<p><strong>Answer:</strong> Negative correlation.</p>"
    )
}

# ---------------------------------------------------------------- tier guides
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: naming the pattern",
        "steps": [
            "A scatter graph plots two things at once: one along the bottom, one up the side. Each point is one place, one country or one person.",
            "Read the points from left to right. Climbing means <strong>positive correlation</strong>, falling means <strong>negative correlation</strong>, no pattern at all means <strong>no correlation</strong>.",
            "Then check it makes geographical sense: which of the two could actually influence the other?"
        ],
        "example": {
            "question": "Points plotted for altitude (m) against temperature (°C) fall steadily from left to right. Name the correlation.",
            "steps": [
                {"label": "Read left to right", "content": "<p>Altitude increases along the bottom axis.</p>"},
                {"label": "Watch the other axis", "content": "<p>Temperature drops as you move right.</p>"},
                {"label": "Check", "content": "<p>One rises while the other falls, so the two move in opposite directions.</p>"},
                {"label": "Answer", "content": "<p>Negative correlation.</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "silver": {
        "title": "Silver: reading values off the trend",
        "steps": [
            "Silver asks for a value. Draw a <strong>line of best fit</strong> through the middle of the points, with roughly as many above it as below.",
            "To estimate, go up from your value on the bottom axis to the line, then straight across. If nothing is plotted at your value, use the points either side and take the value midway between them.",
            "Then say why the link exists in geographical terms, not just that it exists."
        ],
        "example": {
            "question": "Channel width is plotted against distance downstream. Points sit at 4 km (12 m wide) and 6 km (18 m wide). Estimate the width at 5 km.",
            "steps": [
                {"label": "Locate", "content": "<p>Nothing is plotted at 5 km, so use the points either side.</p>"},
                {"label": "Read both", "content": "<p>4 km gives 12 m; 6 km gives 18 m.</p>"},
                {"label": "Go midway", "content": "<p>12 + 18 = 30, and 30 ÷ 2 = 15.</p>"},
                {"label": "Check", "content": "<p>15 sits between 12 and 18, just as 5 km sits between 4 km and 6 km.</p>"},
                {"label": "Answer", "content": "<p>About 15 m.</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    },
    "gold": {
        "title": "Gold: anomalies, strength and limits",
        "steps": [
            "Gold judges the graph. An <strong>anomaly</strong> sits far from the pattern the other points make, and usually has a real explanation.",
            "Strength matters too. Tightly packed points mean a strong correlation; a coefficient near +1 or −1 is strong, near 0 is weak.",
            "Estimating inside the plotted range is reasonable. Predicting beyond it is not, because nobody measured out there. Correlation never proves cause."
        ],
        "example": {
            "question": "Yield rises steadily with rainfall, except one farm at 650 mm yielding 1 t/ha while its neighbours at 600 mm and 700 mm yield 5 and 6. Is it an anomaly?",
            "steps": [
                {"label": "Predict from the trend", "content": "<p>Midway between 5 and 6 is 5.5 t/ha.</p>"},
                {"label": "Measure the gap", "content": "<p>5.5 − 1 = 4.5 t/ha below the trend.</p>"},
                {"label": "Compare", "content": "<p>The other seven farms rise by only 6 t/ha across the whole graph.</p>"},
                {"label": "Check", "content": "<p>One gap is almost as large as the entire trend, so the point does not belong to the pattern.</p>"},
                {"label": "Answer", "content": "<p>Yes, it is an anomaly, perhaps waterlogged or poor soil.</p>", "isAnswer": True, "is_answer": True}
            ]
        }
    }
}

# ---------------------------------------------------------------- guided
pd["guided"] = {
    "opener": {
        "label": "Before any of the words",
        "display": opener_svg,
        "steps": [
            {"say": "Six friends measured their height and their shoe size. Just look at the dots.",
             "pre": "The shortest friend is 150 cm tall. Her shoe size is ", "post": "",
             "answer": 4,
             "hint": "Find the dot above the 150 label, then read straight across to the shoe size numbers."},
            {"pre": "Now the friend who is 165 cm. Her shoe size is ", "post": "",
             "answer": 7,
             "done": "You used the pattern, not a rule.",
             "hint": "Go along to the fourth dot from the left, then read across."},
            {"say": "One friend does not fit at all.",
             "pre": "The tallest friend, at 175 cm, wears shoe size ", "post": "",
             "answer": 3,
             "hint": "Look at the dot on the far right, low down near the bottom."},
            {"say": "Nothing formal happened there, but you just read a <strong>scatter graph</strong>. Dots that climb as you move right mean the two things grow together: that is <strong>positive correlation</strong>. The friend who broke the pattern is an <strong>anomaly</strong>. Naming the pattern and spotting the odd one out is the whole of this topic."}
        ]
    },
    "teach": {
        "bronze": {
            "label": "Together: name the pattern",
            "display": "Six weather stations in the same valley. Altitude against mean temperature.<br>" + teach_b_svg,
            "steps": [
                {"say": "Start by finding your way around the graph, not by calculating anything.",
                 "pre": "The point furthest left sits at 0 m. Its temperature in °C is ", "post": "",
                 "answer": 12,
                 "hint": "Read straight across from that dot to the numbers up the side."},
                {"pre": "Now the point furthest right, at 500 m. Its temperature is ", "post": "",
                 "answer": 7,
                 "done": "Two ends located. Now the graph can be read.",
                 "hint": "The last dot on the right, read across to the side axis."},
                {"pre": "Across the whole graph the temperature has changed by 12 − 7 = ", "post": " °C",
                 "answer": 5,
                 "hint": "Subtract the right hand reading from the left hand one."},
                {"say": "A fall, but is it steady or does it jump about?", "phase": "substitute",
                 "pre": "At 200 m the temperature is ", "post": " °C",
                 "answer": 10,
                 "hint": "Find 200 on the bottom axis and read the dot above it."},
                {"pre": "So every 100 m of climb costs ", "post": " °C",
                 "answer": 1,
                 "done": "Perfectly even, which is why the dots make a straight line.",
                 "hint": "Six readings drop from 12 to 7 in equal steps of 100 m."},
                {"say": "Now name it. Type <strong>1</strong> if the dots climb to the right, <strong>2</strong> if they fall, <strong>3</strong> if there is no pattern.",
                 "pre": "Pattern number: ", "post": "",
                 "answer": 2,
                 "hint": "You just watched the temperature drop from 12 down to 7 as altitude rose."},
                {"say": "Last thing, check the naming against a point you have not used yet.",
                 "pre": "At 400 m the temperature reads ", "post": " °C",
                 "answer": 8,
                 "done": "8 sits between 7 and 10, so the fall really does continue all the way. Altitude up, temperature down: negative correlation, and it matches the geography, because air cools as it rises.",
                 "hint": "Find 400 on the bottom axis and read the dot above it."}
            ]
        },
        "silver": {
            "label": "Together: read a value off the trend",
            "display": "A pedestrian count taken at six points on a road running out from a city centre.<br>" + teach_s_svg,
            "steps": [
                {"say": "First get your bearings on the graph.",
                 "pre": "At the city centre, 0 m, the pedestrian count is ", "post": "",
                 "answer": 180,
                 "hint": "The dot furthest left, read across to the numbers up the side."},
                {"say": "We want the count at 500 m, but nobody counted there. Use the neighbours.",
                 "pre": "The nearest point to the left is at 400 m. Its count is ", "post": "",
                 "answer": 130,
                 "hint": "Find 400 on the bottom axis and read the dot above it."},
                {"pre": "The nearest point to the right is at 600 m. Its count is ", "post": "",
                 "answer": 100,
                 "done": "Both neighbours located. Everything else is arithmetic.",
                 "hint": "Find 600 on the bottom axis and read the dot above it."},
                {"say": "500 m sits exactly halfway between 400 m and 600 m, so the estimate sits halfway between their counts.", "phase": "substitute",
                 "pre": "130 + 100 = ", "post": "",
                 "answer": 230,
                 "hint": "Add the two counts you just read."},
                {"pre": "230 ÷ 2 = ", "post": "",
                 "answer": 115,
                 "hint": "Halve the total to land midway between the two readings."},
                {"say": "Check it sits where it should.",
                 "pre": "130 − 115 = ", "post": "",
                 "answer": 15,
                 "done": "And 115 − 100 is 15 as well, so the estimate is exactly midway between the two counts, just as 500 m is midway between 400 m and 600 m.",
                 "hint": "Subtract your estimate from the left hand neighbour's count."}
            ]
        },
        "gold": {
            "label": "Together: is that point an anomaly?",
            "display": "Eight farms in one region. Growing season rainfall against wheat yield.<br>" + teach_g_svg,
            "steps": [
                {"say": "Before judging anything, find out what is actually on the graph.",
                 "pre": "Number of farms plotted: ", "post": "",
                 "answer": 8,
                 "hint": "Count every dot, including the low one."},
                {"pre": "One dot sits far below the rest. Its yield in t/ha is ", "post": "",
                 "answer": 1,
                 "done": "Located. That is the point under suspicion.",
                 "hint": "Read across from the low dot to the numbers up the side."},
                {"say": "Its neighbours at 600 mm and 700 mm yield 5 and 6 t/ha, so the trend predicts something midway between them.",
                 "pre": "(5 + 6) ÷ 2 = ", "post": " t/ha",
                 "answer": 5.5,
                 "hint": "Add the two neighbouring yields and halve the total."},
                {"say": "Now measure how far off the point really is.", "phase": "substitute",
                 "pre": "5.5 − 1 = ", "post": " t/ha below the trend",
                 "answer": 4.5,
                 "hint": "Take the low dot's yield away from what the trend predicted."},
                {"pre": "Across the whole graph the other farms rise from 2 t/ha to 8 t/ha, a climb of ", "post": " t/ha",
                 "answer": 6,
                 "hint": "Subtract the lowest trend yield from the highest."},
                {"say": "Compare the two numbers you have.",
                 "pre": "Farms that sit on the steady climb: ", "post": "",
                 "answer": 7,
                 "done": "One point misses the trend by 4.5 t/ha while the whole trend only spans 6 t/ha, so it is nowhere near the pattern the other seven make. That is a genuine anomaly, and a waterlogged or thin soiled field would explain it.",
                 "hint": "Take the odd one away from the total number of farms."}
            ]
        }
    }
}

# ---------------------------------------------------------------- bank
pb = pd["problem_bank"]
pb["bronze_description"] = "Name the pattern: read the points across the graph and say whether they climb, fall or scatter."
pb["silver_description"] = "Use the trend: read a value off the line of best fit and explain the link geographically."
pb["gold_description"] = "Judge the graph: anomalies, how strong the correlation is, and how far a prediction can be trusted."

B, S, G = pb["bronze"], pb["silver"], pb["gold"]

def setp(prob, hint, steps, misc, display=None, options=None, solutions=None):
    if display is not None:
        prob["display"] = display
    if options is not None:
        prob["options"] = options
    if solutions is not None:
        prob["solutions"] = solutions
    prob["hint"] = hint
    prob["guided_steps"] = steps
    prob["misconceptions"] = misc

# ---- BRONZE ----------------------------------------------------------------
setp(B[0],
     "Follow the points from the left edge to the right edge and see whether they rise or fall.",
     [
         {"say": "Find your way around the graph first.",
          "pre": "The point furthest left sits at a GDP of $2,000. Its life expectancy in years is ", "post": "",
          "answer": 55, "hint": "Read straight across from that dot to the years axis."},
         {"pre": "The point furthest right, at $50,000, has a life expectancy of ", "post": " years",
          "answer": 82, "done": "Both ends of the graph located.",
          "hint": "The last dot on the right, read across to the side axis."},
         {"say": "Now compare the two ends.", "phase": "substitute",
          "pre": "82 − 55 = ", "post": " years",
          "answer": 27, "hint": "Subtract the left hand reading from the right hand one."},
         {"pre": "Check the rise is steady, not a fluke. At $20,000 the life expectancy is ", "post": " years",
          "answer": 75,
          "done": "75 sits neatly between 55 and 82, so the points climb the whole way across.",
          "hint": "Find $20,000 on the bottom axis and read the dot above it."},
         {"say": "Both values rise together as you move right, so the points climb. Choose the option that says the two variables increase together."}
     ],
     [
         {"pattern": "direction_reversed", "expect": 1,
          "message": "You have read the slope the wrong way round. Track the points from the left edge to the right edge and check whether they are getting higher or lower up the graph."},
         {"pattern": "perfect_overclaim", "expect": 3,
          "message": "Perfect correlation would mean every point sitting exactly on one straight line with no scatter at all. Look at how loosely these points sit before claiming that."}
     ])

setp(B[1],
     "Decide which way the points travel as you move right along the altitude axis.",
     [
         {"say": "Picture two of the plotted points: one at 0 m with 15 °C, and one at 2,000 m with 3 °C.",
          "pre": "Moving right along the bottom axis, altitude climbs from 0 m to 2,000 m, a rise of ", "post": " m",
          "answer": 2000, "hint": "Subtract the left hand altitude from the right hand one."},
         {"pre": "Over that same stretch the temperature goes from 15 °C to 3 °C, a fall of 15 − 3 = ", "post": " °C",
          "answer": 12, "done": "One variable up, the other down.",
          "hint": "Take the higher altitude reading away from the lower altitude one."},
         {"say": "Turn that into a direction.", "phase": "substitute",
          "pre": "Type 1 if points like these climb to the right, or 2 if they fall: ", "post": "",
          "answer": 2, "hint": "The temperature values got smaller as you moved right."},
         {"pre": "Check the middle. Halfway up, at 1,000 m, the temperature sits at (15 + 3) ÷ 2 = ", "post": " °C",
          "answer": 9,
          "done": "9 °C is below 15 and above 3, so the line falls steadily the whole way rather than jumping.",
          "hint": "Add the two temperatures and halve the total."},
         {"say": "One variable rises while the other falls, which is what a downward slope means. Choose that option."}
     ],
     [
         {"pattern": "both_change_equals_positive", "expect": 0,
          "message": "Both variables changing is not the same as both rising. Check whether temperature goes up or down as altitude increases."},
         {"pattern": "needs_more_info", "expect": 3,
          "message": "The direction of the slope is all you need to name a correlation, and you have been told which way it slopes."}
     ],
     display=("On a scatter graph, altitude (m) is plotted along the bottom and temperature (°C) up the side. "
              "The points slope downward from left to right. What type of correlation is this?"))

setp(B[2],
     "Find the point that sits far away from the line the others make, not simply the highest or lowest one.",
     [
         {"say": "Get oriented on the graph before judging any point.",
          "pre": "The point furthest right sits at 32 °C. Its sales figure is ", "post": "",
          "answer": 380, "hint": "Read across from the right hand dot to the sales axis."},
         {"pre": "The point at 25 °C has a sales figure of ", "post": "",
          "answer": 300, "done": "Two of the ordinary points located.",
          "hint": "Find 25 on the bottom axis and read the dot above it."},
         {"say": "Most points climb steadily, but one sits far below the rest.", "phase": "substitute",
          "pre": "That low point's temperature in °C is ", "post": "",
          "answer": 30, "hint": "Look along the bottom axis for the dot that is stranded near the floor of the graph."},
         {"pre": "Its sales figure is ", "post": "",
          "answer": 50, "hint": "Read across from that low dot to the sales axis."},
         {"pre": "Its neighbours at 28 °C and 32 °C sell 320 and 380. The smaller of those two is ", "post": "",
          "answer": 320,
          "done": "50 is nowhere near 320, so that point sits far below the pattern its neighbours make. That is what an anomaly looks like.",
          "hint": "Compare the two neighbouring sales figures and pick the lower one."},
         {"say": "So the odd point is the warm day with almost no sales. Choose that option."}
     ],
     [
         {"pattern": "picked_trend_point", "expect": 0,
          "message": "That point sits right on the rising trend with its neighbours. An anomaly is the point that sits far away from the pattern."},
         {"pattern": "picked_trend_point_mid", "expect": 3,
          "message": "That point follows the climb of the ones either side of it, so it is part of the pattern rather than the exception to it."}
     ])

setp(B[3],
     "Read the price axis as you move right along the distance axis.",
     [
         {"say": "Locate the two ends of the graph first.",
          "pre": "The point closest to the centre, at 1 km, has a house price of £", "post": " thousand",
          "answer": 450, "hint": "The dot furthest left, read across to the price axis."},
         {"pre": "The point furthest right, at 15 km, has a house price of £", "post": " thousand",
          "answer": 160, "done": "Both ends located.",
          "hint": "The last dot on the right, read across to the price axis."},
         {"say": "Compare the ends.", "phase": "substitute",
          "pre": "450 − 160 = ", "post": " thousand pounds of change",
          "answer": 290, "hint": "Subtract the right hand price from the left hand one."},
         {"pre": "Check the middle. At 7 km the price is £", "post": " thousand",
          "answer": 250,
          "done": "250 sits between 160 and 450, so prices drop steadily the whole way out of the city.",
          "hint": "Find 7 on the bottom axis and read the dot above it."},
         {"say": "Distance rises while price falls, so the two variables move in opposite directions. Choose that option."}
     ],
     [
         {"pattern": "direction_reversed", "expect": 0,
          "message": "That option needs both variables to climb together. Track the prices from the left edge to the right edge again before deciding."},
         {"pattern": "strength_not_direction", "expect": 3,
          "message": "You have judged the strength but not the direction. Look again at whether the points rise or fall as you move right."}
     ])

setp(B[4],
     "Decide the direction first, then check which of the two variables could sensibly influence the other.",
     [
         {"say": "Picture two of the resort's records: a day with 3 hours of sunshine and 200 visitors, and a day with 9 hours and 800 visitors.",
          "pre": "Along the bottom axis sunshine rises from 3 hours to 9 hours, a rise of ", "post": " hours",
          "answer": 6, "hint": "Subtract the smaller number of hours from the larger."},
         {"pre": "Over the same stretch visitors go from 200 to 800, a rise of ", "post": "",
          "answer": 600, "done": "Both variables moved the same way.",
          "hint": "Subtract 200 from 800."},
         {"say": "Turn that into a direction.", "phase": "substitute",
          "pre": "Type 1 if points like these climb to the right, or 2 if they fall: ", "post": "",
          "answer": 1, "hint": "Both readings got larger as you moved right."},
         {"pre": "Now the cause. Type 1 if sunshine can change visitor numbers, or 2 if visitor numbers can change the weather: ", "post": "",
          "answer": 1,
          "done": "Only one direction makes physical sense, which is why sunshine belongs along the bottom axis. Even so, a correlation on its own never proves which variable causes which.",
          "hint": "Ask which of the two things could physically affect the other."},
         {"say": "Rising together, with the weather doing the influencing. Choose the option that says both."}
     ],
     [
         {"pattern": "reversed_causation", "expect": 3,
          "message": "You have the direction right, but the cause is the wrong way round. Ask which of the two could physically change the other."},
         {"pattern": "direction_reversed", "expect": 1,
          "message": "Check whether the visitor numbers rise or fall as sunshine hours increase before choosing a direction."}
     ],
     options=[
         "Positive correlation, because more sunshine attracts more tourists",
         "Negative correlation, because more sunshine reduces tourist numbers",
         "No correlation, because sunshine does not affect tourism",
         "Positive correlation, because tourists cause more sunshine"
     ])

setp(B[5],
     "Find the two plotted points either side of 40 mm and take the value midway between them.",
     [
         {"say": "Start on the axis, not on the calculator.",
          "pre": "Find 40 mm along the bottom axis. Nothing is plotted there, so use the neighbours. The nearest point to the left is at 35 mm, with a discharge of ", "post": " cumecs",
          "answer": 16, "hint": "Find 35 on the bottom axis and read the dot above it."},
         {"pre": "The nearest point to the right is at 45 mm, with a discharge of ", "post": " cumecs",
          "answer": 20, "done": "Both neighbours located, so the estimate is boxed in.",
          "hint": "Find 45 on the bottom axis and read the dot above it."},
         {"say": "40 mm sits exactly halfway between 35 mm and 45 mm, so the estimate sits halfway between their discharges.", "phase": "substitute",
          "pre": "16 + 20 = ", "post": "",
          "answer": 36, "hint": "Add the two discharges you just read."},
         {"pre": "36 ÷ 2 = ", "post": " cumecs",
          "answer": 18, "hint": "Halve the total to land midway between the two readings."},
         {"pre": "Check the spacing. Your estimate minus the 35 mm reading gives ", "post": "",
          "answer": 2,
          "done": "The 45 mm reading is the same distance above your estimate, so it really does sit midway, exactly where 40 mm sits between 35 mm and 45 mm.",
          "hint": "Subtract the discharge at 35 mm from the value you just worked out."}
     ],
     [
         {"pattern": "read_left_neighbour", "expect": 16,
          "message": "That is the reading at the plotted point to the left, not at 40 mm. The estimate belongs between the two neighbours."},
         {"pattern": "read_right_neighbour", "expect": 20,
          "message": "That is the reading at the plotted point to the right of 40 mm. The estimate should sit between the two neighbours."},
         {"pattern": "echoed_x_value", "expect": 40,
          "message": "You have typed the rainfall back. Discharge is read off the vertical axis."}
     ])

setp(B[6],
     "Rule out the pairs where one thing could physically affect the other.",
     [
         {"say": "Four pairs are offered, and only one has no geographical link.",
          "pre": "Number of pairs you must rule out to be left with the odd one: ", "post": "",
          "answer": 3, "hint": "There are four pairs and only one survives."},
         {"pre": "Rainfall and river discharge. Type 1 if more rain puts more water into a river, or 2 if it makes no difference: ", "post": "",
          "answer": 1, "done": "Ruled in as a real relationship.",
          "hint": "Think where the water in a river comes from."},
         {"say": "Two more to test.", "phase": "substitute",
          "pre": "Population density and distance from the capital. Type 1 if settlement thins out with distance, or 2 if distance is irrelevant: ", "post": "",
          "answer": 1, "hint": "Capital cities pull people and jobs towards them."},
         {"pre": "Temperature and altitude. Type 1 if climbing higher changes the temperature, or 2 if it does not: ", "post": "",
          "answer": 1, "hint": "Think about the air on top of a mountain."},
         {"pre": "Three pairs ruled in. Number of pairs left: ", "post": "",
          "answer": 1,
          "done": "The pair still standing measures two things with no physical connection at all, so its points would just scatter.",
          "hint": "Take the three you ruled in away from the four on the list."}
     ],
     [
         {"pattern": "ruled_out_real_link", "expect": 1,
          "message": "There is a real link there: settlement and jobs thin out with distance from a capital city. Look for the pair with no physical connection at all."},
         {"pattern": "ruled_out_lapse_rate", "expect": 3,
          "message": "Temperature and altitude are strongly linked, because air cools as it rises. Try the pair whose two measurements have nothing to do with each other."}
     ])

setp(B[7],
     "Picture one line up from the GDP value and one across from the life expectancy value, then count what lands in the top right.",
     [
         {"say": "Two tests have to be passed at once, so split the graph up first.",
          "pre": "Picture a vertical line at $20,000. Points sitting to the right of it: ", "post": "",
          "answer": 4, "hint": "Count only the dots further right than $20,000 on the bottom axis."},
         {"pre": "Now the second test. The leftmost of those four sits at $22,000. Its life expectancy is ", "post": " years",
          "answer": 76, "done": "Both tests are now set up.",
          "hint": "Read across from that dot to the years axis."},
         {"say": "Check each of the four against the 75 year line.", "phase": "substitute",
          "pre": "Of your four points, the number with a life expectancy above 75 is ", "post": "",
          "answer": 4, "hint": "The lowest of the four already clears 75, and the rest sit higher still."},
         {"pre": "Check nothing is missed. Points that fail at least one of the two tests: ", "post": "",
          "answer": 4,
          "done": "4 pass and 4 fail, and 4 + 4 = 8, which is every country on the graph, so nothing has been double counted or dropped.",
          "hint": "Count the dots that are either left of $20,000 or below 75 years."}
     ],
     [
         {"pattern": "counted_all_points", "expect": 8,
          "message": "You have counted every point on the graph. Only the points that pass both tests at once should be counted."},
         {"pattern": "included_below_threshold", "expect": 5,
          "message": "One of the points you counted sits to the left of the $20,000 line. Test each point on GDP before you count it."},
         {"pattern": "missed_a_point", "expect": 3,
          "message": "A point just past the $20,000 line has probably been missed. Sweep from that line to the right edge and count every dot."}
     ])

# ---- SILVER ----------------------------------------------------------------
setp(S[0],
     "Read the temperature range at the coast and far inland, then decide which places the sea is steadying.",
     [
         {"say": "Locate the two ends of the graph before explaining anything.",
          "pre": "The point nearest the coast, 10 km from the sea, has a temperature range of ", "post": " °C",
          "answer": 8, "hint": "The dot furthest left, read across to the range axis."},
         {"pre": "The point furthest inland, 400 km from the sea, has a range of ", "post": " °C",
          "answer": 30, "done": "Both ends located.",
          "hint": "The last dot on the right, read across to the range axis."},
         {"say": "Compare the two ends.", "phase": "substitute",
          "pre": "30 − 8 = ", "post": " °C",
          "answer": 22, "hint": "Subtract the coastal range from the inland range."},
         {"pre": "Check the middle. At 100 km the range is ", "post": " °C",
          "answer": 16,
          "done": "16 sits between 8 and 30, so the range grows steadily with distance inland. The sea warms and cools slowly, so it holds coastal temperatures close together all year.",
          "hint": "Find 100 on the bottom axis and read the dot above it."},
         {"say": "Both variables rise together, and the reason is the sea steadying the places closest to it. Choose the option that says both."}
     ],
     [
         {"pattern": "explanation_inverted", "expect": 3,
          "message": "The direction is right but the explanation is upside down. Compare the range at 10 km with the range at 400 km before deciding which places are steadiest."},
         {"pattern": "range_vs_average", "expect": 1,
          "message": "The side axis shows the temperature range, not the average temperature, so a claim about places being cooler does not describe these points."}
     ],
     options=[
         "Positive, because the sea has a moderating effect, so inland areas have a greater temperature range",
         "Negative, because further from the sea means cooler temperatures overall",
         "No correlation, because the sea does not affect temperature range",
         "Positive, because coastal areas have the greatest temperature range"
     ])

setp(S[1],
     "Use the plotted points either side of 25 and take the value midway between them, then round it.",
     [
         {"say": "Start on the axis.",
          "pre": "Find 25 along the bottom axis. Nothing is plotted there, so use the neighbours. The nearest point to the left is at a birth rate of 22, with infant mortality of ", "post": "",
          "answer": 32, "hint": "Find 22 on the bottom axis and read the dot above it."},
         {"pre": "The nearest point to the right is at a birth rate of 28, with infant mortality of ", "post": "",
          "answer": 45, "done": "Both neighbours located, so the estimate is boxed in.",
          "hint": "Find 28 on the bottom axis and read the dot above it."},
         {"say": "25 sits exactly halfway between 22 and 28, so the trend value sits halfway between their readings.", "phase": "substitute",
          "pre": "32 + 45 = ", "post": "",
          "answer": 77, "hint": "Add the two readings you just took."},
         {"pre": "77 ÷ 2 = ", "post": "",
          "answer": 38.5, "hint": "Halve the total to land midway between the two readings."},
         {"pre": "The question asks for a whole number, so round it to ", "post": "",
          "answer": 39,
          "done": "It sits between the 32 below and the 45 above, exactly where a birth rate of 25 sits between 22 and 28.",
          "hint": "Round the midpoint to the nearest whole number."}
     ],
     [
         {"pattern": "read_left_neighbour", "expect": 32,
          "message": "That is the reading at the point to the left of 25, not at 25 itself. The estimate belongs between the two neighbours."},
         {"pattern": "read_right_neighbour", "expect": 45,
          "message": "That is the reading at the point to the right. Take a value between the two neighbouring points instead."},
         {"pattern": "unrounded_midpoint", "expect": 38.5,
          "message": "That is the midpoint before rounding. Check what form the question asks the answer in."},
         {"pattern": "echoed_x_value", "expect": 25,
          "message": "You have typed the birth rate back. Infant mortality is read off the vertical axis."}
     ],
     display=("The scatter graph shows birth rate and infant mortality for 10 countries. Using the line of best fit, "
              "estimate the infant mortality rate for a country with a birth rate of 25. Give your answer to the "
              "nearest whole number."),
     solutions=[39])

setp(S[2],
     "Ask what a country's emissions depend on besides how developed it is.",
     [
         {"say": "Place the country on the graph before judging the explanations.",
          "pre": "Human Development Index runs from 0 to 1 along the bottom. This country's HDI is ", "post": "",
          "answer": 0.85, "hint": "The value is given in the question itself."},
         {"pre": "Strong positive correlation means high development usually comes with high emissions. Type 1 if this country sits above the trend, or 2 if it sits below: ", "post": "",
          "answer": 2, "done": "Below the trend, so the explanation must account for low emissions at high development.",
          "hint": "Its emissions were described as very low for its level of development."},
         {"say": "Now thin the four options out.", "phase": "substitute",
          "pre": "Number of the four options that simply dismiss the data, either as an error or as no relationship: ", "post": "",
          "answer": 2, "hint": "One calls it a data entry error, one denies any relationship exists."},
         {"pre": "Emissions on this kind of graph are measured per person. Type 1 if a bigger population automatically lowers a per person figure, or 2 if it does not: ", "post": "",
          "answer": 2, "hint": "Population has already been divided out of a per person figure."},
         {"pre": "Two options dismissed and one ruled out on population. Options left: ", "post": "",
          "answer": 1,
          "done": "Only one explanation survives, and it works because a country can be highly developed and still generate its electricity without burning fossil fuels.",
          "hint": "Take the three you ruled out away from the four offered."}
     ],
     [
         {"pattern": "blames_the_data", "expect": 0,
          "message": "Unusual points are usually real. Look for a geographical reason before deciding the data must be faulty."},
         {"pattern": "population_confusion", "expect": 2,
          "message": "Emissions here are measured per person, so population size has already been divided out."},
         {"pattern": "denies_relationship", "expect": 3,
          "message": "The other countries follow a clear pattern, so a relationship plainly exists. The question is why this one country sits apart from it."}
     ],
     options=[
         "Data entry error, so the point should be deleted",
         "The country may rely heavily on renewable energy despite high development",
         "The country has a very large population diluting emissions",
         "HDI and CO₂ have no relationship"
     ])

setp(S[3],
     "Read the velocity at the source end and at the mouth end, then check whether gradient could really be the cause.",
     [
         {"say": "Locate the two ends of the river on the graph.",
          "pre": "At 0 km downstream the velocity is ", "post": " m/s",
          "answer": 0.3, "hint": "The dot furthest left, read across to the velocity axis."},
         {"pre": "At 25 km downstream the velocity is ", "post": " m/s",
          "answer": 1.5, "done": "Both ends located.",
          "hint": "The last dot on the right, read across to the velocity axis."},
         {"say": "Compare them.", "phase": "substitute",
          "pre": "1.5 − 0.3 = ", "post": " m/s",
          "answer": 1.2, "hint": "Subtract the source velocity from the mouth velocity."},
         {"pre": "Now test the explanation. Type 1 if a river's gradient gets steeper towards the sea, or 2 if it gets gentler: ", "post": "",
          "answer": 2, "hint": "Think of the shape of a long profile from source to mouth."},
         {"pre": "Check the middle. At 12 km the velocity is ", "post": " m/s",
          "answer": 1.1,
          "done": "1.1 sits between 0.3 and 1.5, so velocity rises the whole way even though the gradient is easing. The cause must be the larger, smoother channel and the water added by tributaries.",
          "hint": "Find 12 on the bottom axis and read the dot above it."},
         {"say": "Rising velocity downstream, explained by channel efficiency rather than gradient. Choose the option that says both."}
     ],
     [
         {"pattern": "gradient_mistake", "expect": 3,
          "message": "The direction is right but the reason is wrong. A river's gradient actually eases towards its mouth, so something else must be speeding the water up."},
         {"pattern": "direction_reversed", "expect": 1,
          "message": "Check the velocity readings at the left and right ends of the graph before deciding which way the trend runs."}
     ],
     options=[
         "Positive, because rivers flow faster downstream as tributaries add water and the channel becomes more efficient",
         "Negative, because rivers slow down as they approach the sea",
         "No correlation, because velocity is random along a river",
         "Positive, because rivers flow faster downstream due to steeper gradients"
     ])

setp(S[4],
     "Ask what else land close to a city centre gets used for besides homes.",
     [
         {"say": "Place the odd point before explaining it.",
          "pre": "The graph runs outwards from the city centre. The unusual point sits at ", "post": " km",
          "answer": 3, "hint": "The distance is stated in the question."},
         {"pre": "Negative correlation means density is highest near the centre. Type 1 if the trend expects high density at 3 km, or 2 if it expects low density: ", "post": "",
          "answer": 1, "done": "The trend expects high density there, but this point is low, so it sits below the trend.",
          "hint": "Close to the centre means near the left of the graph, where density is greatest."},
         {"say": "Now thin the four explanations out.", "phase": "substitute",
          "pre": "Number of options that simply claim the data must be wrong: ", "post": "",
          "answer": 1, "hint": "Look for the option that blames the figures rather than the geography."},
         {"pre": "Number of options that claim nobody could live 3 km from a centre: ", "post": "",
          "answer": 1, "hint": "Plenty of people live 3 km from a city centre, so that option cannot stand."},
         {"pre": "One more option misreads negative correlation as a rule every point must obey. Options left: ", "post": "",
          "answer": 1,
          "done": "The surviving explanation works because land near a centre is not all housing, so a single site can hold very few residents while its neighbours are packed.",
          "hint": "Take the three ruled out away from the four offered."}
     ],
     [
         {"pattern": "blames_the_data", "expect": 1,
          "message": "Unusual points are usually real. Look for a land use reason before deciding the figures are faulty."},
         {"pattern": "impossible_claim", "expect": 2,
          "message": "People certainly live 3 km from a city centre, so that cannot be the explanation."},
         {"pattern": "trend_as_rule", "expect": 3,
          "message": "Negative correlation describes the overall trend, not a rule that every single point must obey."}
     ])

setp(S[5],
     "Use the plotted points either side of 35°N and take the value midway between them, then round it.",
     [
         {"say": "Start on the axis.",
          "pre": "Find 35 along the bottom axis. Nothing is plotted there, so use the neighbours. The nearest point to the left is at 30°N, with a temperature of ", "post": " °C",
          "answer": 20, "hint": "Find 30 on the bottom axis and read the dot above it."},
         {"pre": "The nearest point to the right is at 40°N, with a temperature of ", "post": " °C",
          "answer": 15, "done": "Both neighbours located, so the estimate is boxed in.",
          "hint": "Find 40 on the bottom axis and read the dot above it."},
         {"say": "35°N sits exactly halfway between 30 and 40, so the estimate sits halfway between their temperatures.", "phase": "substitute",
          "pre": "20 + 15 = ", "post": "",
          "answer": 35, "hint": "Add the two temperatures you just read."},
         {"pre": "Halve that total: ", "post": " °C",
          "answer": 17.5, "hint": "Divide the total by 2 to land midway between the two readings."},
         {"pre": "The question asks for a whole number, so round it to ", "post": " °C",
          "answer": 18,
          "done": "It sits between the 15 °C at 40°N and the 20 °C at 30°N, exactly as a latitude midway between them should.",
          "hint": "Round the midpoint to the nearest whole number."}
     ],
     [
         {"pattern": "read_left_neighbour", "expect": 20,
          "message": "That is the reading at 30°N, not at 35°N. The estimate belongs between the two neighbours."},
         {"pattern": "read_right_neighbour", "expect": 15,
          "message": "That is the reading at 40°N. Take a value between the two neighbouring points instead."},
         {"pattern": "unrounded_midpoint", "expect": 17.5,
          "message": "That is the midpoint before rounding. Check what form the question asks the answer in."}
     ],
     display=("The scatter graph shows latitude and average annual temperature. Using the graph, estimate the "
              "temperature at latitude 35°N. Give your answer to the nearest whole number."))

setp(S[6],
     "Ask whether anyone actually collected data in the range being predicted.",
     [
         {"say": "Picture a study that measured rainfall from 10 mm up to 80 mm, then tried to predict at 120 mm.",
          "pre": "The largest rainfall value actually measured is ", "post": " mm",
          "answer": 80, "hint": "It is the top of the range the data was collected over."},
         {"pre": "The prediction is wanted at 120 mm, which is beyond the data by ", "post": " mm",
          "answer": 40, "done": "That gap is the whole issue.",
          "hint": "Subtract the largest measured value from the value being predicted."},
         {"say": "Now weigh the four options.", "phase": "substitute",
          "pre": "Type 1 if anyone measured what happens at 120 mm, or 2 if nobody did: ", "post": "",
          "answer": 2, "hint": "The study stopped at the top of its measured range."},
         {"pre": "Two options claim extrapolation only works with one type of correlation or is always wrong. Options left after ruling those out: ", "post": "",
          "answer": 2, "hint": "Four options, two ruled out."},
         {"pre": "One of the two left says interpolation uses a wider range of data, which is the wrong way round. Options left: ", "post": "",
          "answer": 1,
          "done": "The surviving option is the one that names the real problem: the prediction sits outside the range anybody measured, so the pattern out there is unknown.",
          "hint": "Take the ruled out option away from the two remaining."}
     ],
     [
         {"pattern": "always_wrong", "expect": 3,
          "message": "Extrapolation is not banned, it is just less trustworthy. Choose the option that explains why."},
         {"pattern": "range_confusion", "expect": 2,
          "message": "Interpolation works inside the measured range, so it does not use a wider spread of data than extrapolation does."}
     ])

# ---- GOLD ------------------------------------------------------------------
setp(G[0],
     "Compare the top right point with its nearest neighbour before describing the overall pattern.",
     [
         {"say": "Locate the suspect point on the graph first.",
          "pre": "The point furthest right sits at a GDP of $65,000. Its CO₂ figure in tonnes is ", "post": "",
          "answer": 35, "hint": "Read across from the top right dot to the emissions axis."},
         {"pre": "Its nearest neighbour, at $60,000, has a CO₂ figure of ", "post": " tonnes",
          "answer": 14, "done": "Located, and already the gap looks large.",
          "hint": "Find $60,000 on the bottom axis and read the dot above it."},
         {"say": "Measure the gap.", "phase": "substitute",
          "pre": "35 − 14 = ", "post": " tonnes",
          "answer": 21, "hint": "Subtract the neighbour's emissions from the top right point's emissions."},
         {"pre": "Ignore that point. The others climb from 1 tonne at $2,000 to 14 tonnes at $60,000, a rise of ", "post": " tonnes",
          "answer": 13, "hint": "Subtract the lowest emissions figure from 14."},
         {"pre": "Points making up that steady climb: ", "post": "",
          "answer": 11,
          "done": "One single gap of 21 tonnes is larger than the entire 13 tonne climb of the other eleven points, so those eleven form a tight rising pattern and the last one does not belong to it.",
          "hint": "Twelve countries are plotted; take away the one that sits apart."},
         {"say": "A tight rising pattern plus one point far above it: an economy built on oil and gas with very few people to divide the emissions between produces exactly this outlier."}
     ],
     [
         {"pattern": "weak_and_fits", "expect": 1,
          "message": "A weak correlation would show points scattered loosely. Check how tightly the other points follow one line, and whether the top right point really sits on it."},
         {"pattern": "direction_reversed", "expect": 2,
          "message": "Check the direction: follow the points from the left edge to the right edge and see whether emissions rise or fall."},
         {"pattern": "no_pattern", "expect": 3,
          "message": "The emissions figures run from 1 tonne to 35 tonnes, so these countries are nowhere near similar."}
     ])

setp(G[1],
     "Compare the value being predicted with the largest value that was actually measured.",
     [
         {"say": "Pin down the range the student actually has evidence for.",
          "pre": "The largest rainfall the student collected data for is ", "post": " mm",
          "answer": 800, "hint": "The question states where the data stops."},
         {"pre": "The prediction is at 1200 mm, which is beyond the data by ", "post": " mm",
          "answer": 400, "done": "That gap is the whole problem.",
          "hint": "Subtract 800 from 1200."},
         {"say": "Now test the options.", "phase": "substitute",
          "pre": "Type 1 if the student has any evidence about what happens above 800 mm, or 2 if they have none: ", "post": "",
          "answer": 2, "hint": "Nobody measured a plot that wet."},
         {"pre": "Type 1 if crops can be harmed by too much water, or 2 if more rain always means more yield: ", "post": "",
          "answer": 1,
          "done": "There is no evidence above 800 mm and good reason to think the rising trend would break down, since waterlogged roots rot. A prediction that far out cannot be trusted.",
          "hint": "Think about waterlogged fields and flooded roots."},
         {"say": "Choose the option that names the missing data range as the problem."}
     ],
     [
         {"pattern": "blames_the_line", "expect": 1,
          "message": "A line of best fit is a useful summary. The problem here is where it is being used, not the line itself."},
         {"pattern": "irrelevant_objection", "expect": 3,
          "message": "How likely that rainfall total is somewhere is not the issue. The issue is whether any data was collected that far out."}
     ],
     options=[
         "1200 mm is outside the data range (extrapolation), and too much rain may flood crops, reversing the trend",
         "The line of best fit is always wrong",
         "You can only interpolate with negative correlation",
         "1200 mm of rainfall is impossible"
     ])

setp(G[2],
     "Read the direction off the points, then judge how close the coefficient is to the end of its scale.",
     [
         {"say": "Locate the two ends of the graph before interpreting the number.",
          "pre": "The point furthest left sits at a literacy rate of 40%. Its birth rate per 1000 is ", "post": "",
          "answer": 42, "hint": "Read across from the left hand dot to the birth rate axis."},
         {"pre": "The point furthest right, at 99% literacy, has a birth rate of ", "post": "",
          "answer": 9, "done": "Both ends located.",
          "hint": "The last dot on the right, read across to the birth rate axis."},
         {"say": "Compare the ends.", "phase": "substitute",
          "pre": "42 − 9 = ", "post": "",
          "answer": 33, "hint": "Subtract the right hand birth rate from the left hand one."},
         {"pre": "A coefficient runs from −1 to +1. Type 1 if −0.92 sits close to −1, or 2 if it sits close to 0: ", "post": "",
          "answer": 1, "hint": "How far is 0.92 from 1?"},
         {"pre": "Check the middle. At 70% literacy the birth rate is ", "post": "",
          "answer": 25,
          "done": "25 sits between 9 and 42 and the points barely stray from a single falling line, which is exactly what a coefficient that close to the end of the scale describes.",
          "hint": "Find 70 on the bottom axis and read the dot above it."},
         {"say": "A large value with a minus sign means the points fall steeply and hug the line. It still does not prove that one variable causes the other."}
     ],
     [
         {"pattern": "causation", "expect": 3,
          "message": "Correlation never proves cause on its own. Healthcare, income and access to family planning all move alongside both of these variables."},
         {"pattern": "strength_misjudged", "expect": 1,
          "message": "Judge the strength by how close the value sits to the end of its scale, not by whether the sign is negative."},
         {"pattern": "sign_ignored", "expect": 2,
          "message": "Check the sign in front of the coefficient, and the direction the points travel, before choosing."}
     ],
     options=[
         "Strong negative correlation, so as literacy increases the birth rate falls sharply",
         "Weak negative correlation, so there is only a slight relationship",
         "Strong positive correlation, so both increase together",
         "The value proves that literacy causes lower birth rates"
     ])

setp(G[3],
     "Ask how many of the points each line actually takes account of.",
     [
         {"say": "Take stock of the two lines before judging them.",
          "pre": "Ten points are plotted. Points sitting above Student A's line: ", "post": "",
          "answer": 5, "hint": "The question tells you how Student A's line splits the points."},
         {"pre": "Points sitting below Student A's line: ", "post": "",
          "answer": 5, "done": "An even split, which is the test a line of best fit has to pass.",
          "hint": "Ten points in total, and you have already placed five of them."},
         {"say": "Now measure how balanced that is.", "phase": "substitute",
          "pre": "Difference between those two counts: ", "post": "",
          "answer": 0, "hint": "Subtract one count from the other."},
         {"pre": "Student B's line is fixed by only the first and last points. Points that had no say in where it went: ", "post": "",
          "answer": 8, "hint": "Take the two end points away from the ten."},
         {"pre": "Options describing a line judged against every point rather than just a couple: ", "post": "",
          "answer": 1,
          "done": "Only one option describes a line answerable to all ten points, and balancing the points either side is exactly how a line of best fit is judged.",
          "hint": "Read the four options and count how many use the whole data set."}
     ],
     [
         {"pattern": "endpoints_rule", "expect": 1,
          "message": "Joining the first and last points ignores everything in between, including an anomaly sitting at either end."},
         {"pattern": "must_pass_origin", "expect": 3,
          "message": "A line of best fit follows the data. Nothing forces it through the origin."},
         {"pattern": "both_valid", "expect": 2,
          "message": "Both lines are judged by the same test, and they do not perform equally well on it."}
     ],
     display=("A class adds a line of best fit to the same scatter graph of 10 points. Student A's line ends up with "
              "5 points above it and 5 below. Student B's line is drawn straight from the first point to the last "
              "point. Whose line is more appropriate?"),
     options=[
         "Student A, because a good line of best fit has roughly equal numbers of points above and below",
         "Student B, because the line should connect the end points",
         "Both are equally valid",
         "Neither, because the line must pass through the origin"
     ])

setp(G[4],
     "Use the plotted points either side of 45° and take the value midway between them, then round it.",
     [
         {"say": "Start on the axis.",
          "pre": "Find 45 along the bottom axis. Nothing is plotted there, so use the neighbours. The nearest point to the left is at 40°, with a daylight variation of ", "post": " hours",
          "answer": 7, "hint": "Find 40 on the bottom axis and read the dot above it."},
         {"pre": "The nearest point to the right is at 50°, with a daylight variation of ", "post": " hours",
          "answer": 10, "done": "Both neighbours located, so the estimate is boxed in.",
          "hint": "Find 50 on the bottom axis and read the dot above it."},
         {"say": "45° sits exactly halfway between 40° and 50°, so the estimate sits halfway between their readings.", "phase": "substitute",
          "pre": "7 + 10 = ", "post": "",
          "answer": 17, "hint": "Add the two readings you just took."},
         {"pre": "Halve that total: ", "post": " hours",
          "answer": 8.5, "hint": "Divide the total by 2 to land midway between the two readings."},
         {"pre": "The question asks for a whole number, so round it to ", "post": " hours",
          "answer": 9,
          "done": "It sits between the 7 hours at 40° and the 10 hours at 50°, exactly as a latitude midway between them should.",
          "hint": "Round the midpoint to the nearest whole number."}
     ],
     [
         {"pattern": "read_left_neighbour", "expect": 7,
          "message": "That is the reading at 40°, not at 45°. The estimate belongs between the two neighbours."},
         {"pattern": "read_right_neighbour", "expect": 10,
          "message": "That is the reading at 50°. Take a value between the two neighbouring points instead."},
         {"pattern": "unrounded_midpoint", "expect": 8.5,
          "message": "That is the midpoint before rounding. Check what form the question asks the answer in."},
         {"pattern": "echoed_x_value", "expect": 45,
          "message": "You have typed the latitude back. The daylight variation is read off the vertical axis."}
     ],
     display=("The scatter graph shows distance from the equator and daylight variation. Estimate the variation at "
              "45° latitude. Give your answer to the nearest whole number."))

# ---------------------------------------------------------------- worked examples: de-dash
we = pd["worked_examples"]
we[0]["steps"][0]["content"] = "<p>Positive correlation, because as rainfall increases, river discharge increases.</p>"

# ---------------------------------------------------------------- write
out = os.path.join(HERE, "lesson_L03.json")
with io.open(out, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("written", out)
