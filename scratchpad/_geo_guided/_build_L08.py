# -*- coding: utf-8 -*-
"""Build the guided-learning practice_data for Geography Skills L08."""
import io, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = "https://pub-aeb94e100e5a48f4a133be5bf206aecb.r2.dev/geography/geographical-skills/maps/"
CHORO = IMG + "choropleth-uk.png"
ISOT = IMG + "isotherm-uk.png"
ISOB = IMG + "isobar-uk.png"
ISOH = IMG + "isohyet-uk.png"


def box(pre, answer, hint, post=None, done=None, say=None, phase=None):
    d = {"pre": pre, "answer": answer, "hint": hint}
    if post: d["post"] = post
    if done: d["done"] = done
    if say: d["say"] = say
    if phase: d["phase"] = phase
    return d


def say(text):
    return {"say": text}


# ---------------------------------------------------------------- SVGs -----
SHADES = ["#f5efe4", "#dccdb1", "#b09a72", "#6f5a38"]

def band_svg(labels, aria):
    parts = ['<svg viewBox="0 0 440 210" role="img" aria-label="%s">' % aria]
    for i in range(4):
        parts.append('<rect x="%d" y="10" width="95" height="80" fill="%s" stroke="#8a7f6d"/>'
                     % (10 + i * 105, SHADES[i]))
        parts.append('<text x="%d" y="110" font-size="15" text-anchor="middle" fill="#2d2a26">%s</text>'
                     % (57 + i * 105, labels[i]))
    parts.append('<text x="10" y="140" font-size="13" fill="#2d2a26">Key: people per km²</text>')
    keys = ["under 50", "50 to 200", "200 to 1000", "1000 or more"]
    for i in range(4):
        parts.append('<rect x="%d" y="152" width="16" height="16" fill="%s" stroke="#8a7f6d"/>'
                     % (10 + i * 105, SHADES[i]))
        parts.append('<text x="%d" y="165" font-size="12" fill="#2d2a26">%s</text>'
                     % (32 + i * 105, keys[i]))
    parts.append('</svg>')
    return "".join(parts)


OPENER_SVG = band_svg(["1", "2", "3", "4"],
                      "Four map areas shaded from light to dark with a key of four population density bands")
TEACH_B_SVG = band_svg(["A", "B", "C", "D"],
                       "Four shaded areas labelled A to D with a key of four population density bands")

TEACH_S_SVG = (
    '<svg viewBox="0 0 440 190" role="img" aria-label="Three isotherms labelled 10, 12 and 14 degrees Celsius '
    'with point T lying midway between the 12 and 14 lines">'
    '<rect x="0" y="0" width="440" height="190" fill="#faf8f5"/>'
    '<path d="M20,45 C140,25 280,65 420,45" fill="none" stroke="#6b8ea8" stroke-width="2"/>'
    '<path d="M20,95 C140,75 280,115 420,95" fill="none" stroke="#6b8ea8" stroke-width="2"/>'
    '<path d="M20,145 C140,125 280,165 420,145" fill="none" stroke="#6b8ea8" stroke-width="2"/>'
    '<text x="24" y="38" font-size="13" fill="#2d2a26">10°C</text>'
    '<text x="24" y="88" font-size="13" fill="#2d2a26">12°C</text>'
    '<text x="24" y="138" font-size="13" fill="#2d2a26">14°C</text>'
    '<circle cx="220" cy="120" r="5" fill="#8a4b2f"/>'
    '<text x="230" y="125" font-size="13" fill="#2d2a26">T</text>'
    '<text x="150" y="180" font-size="12" fill="#2d2a26">T sits midway between two lines</text>'
    '</svg>')

TEACH_G_SVG = (
    '<svg viewBox="0 0 440 190" role="img" aria-label="Two isobars labelled 996 and 1004 millibars with the gap '
    'between them marked as 200 kilometres">'
    '<rect x="0" y="0" width="440" height="190" fill="#faf8f5"/>'
    '<path d="M110,20 C90,70 130,120 110,170" fill="none" stroke="#6b8ea8" stroke-width="2"/>'
    '<path d="M330,20 C310,70 350,120 330,170" fill="none" stroke="#6b8ea8" stroke-width="2"/>'
    '<text x="70" y="30" font-size="13" fill="#2d2a26">996 mb</text>'
    '<text x="300" y="30" font-size="13" fill="#2d2a26">1004 mb</text>'
    '<line x1="120" y1="100" x2="320" y2="100" stroke="#8a4b2f" stroke-width="2"/>'
    '<polygon points="120,100 132,95 132,105" fill="#8a4b2f"/>'
    '<polygon points="320,100 308,95 308,105" fill="#8a4b2f"/>'
    '<text x="180" y="92" font-size="13" fill="#2d2a26">200 km</text>'
    '</svg>')

# ------------------------------------------------------------- opener ------
opener = {
    "display": ("<p>Four areas of a map have been shaded. The key underneath tells you what each shade means.</p>"
                + OPENER_SVG),
    "steps": [
        say("No method needed yet. Just look at the picture and trust your eyes."),
        box("The four areas are numbered 1 to 4. Type the number of the area with the darkest shading.",
            4,
            "Darkest means the deepest, heaviest colour, not the palest one.",
            done="Darker shading means a bigger number. Your eyes read that before anyone taught you a rule."),
        box("The key says the darkest shade means 1000 or more people per km². Type the smallest number of "
            "people per km² an area in that band could have.",
            1000,
            "The band starts at one value and has no upper limit, so type where it starts."),
        box("Area 1 has the palest shade. Type the largest number of people per km² it could have.",
            50,
            "Look at the first band in the key and type the value it stops at.",
            done="You can pin an area to a band, but not to one exact figure. That is the big limitation."),
        say("<strong>That is a choropleth map.</strong> Areas are shaded by value, light to dark, and the key "
            "turns each shade into a range of numbers. The rest of this lesson does exactly what you just did, "
            "plus isoline maps, where lines join places of equal value instead of shading whole areas."),
    ],
}

# -------------------------------------------------------------- teach ------
teach = {
    "bronze": {
        "display": ("<p>Areas A to D are shaded by population density. What can you say about area C?</p>"
                    + TEACH_B_SVG),
        "steps": [
            say("Always start at the key, never at the map."),
            box("Type how many shading bands the key shows.", 4,
                "Count the small coloured squares in the key.",
                done="Four bands means four possible answers, so your job is to pick one."),
            box("Counting from the palest as band 1, type the band number that matches area C.", 3,
                "Compare C's shade with each key square in turn until they match."),
            box("Type the lower limit of that band, in people per km².", 200,
                "Read the first number printed beside that key square.", phase="substitute"),
            box("Type the upper limit of that band, in people per km².", 1000,
                "Read the second number printed beside that key square."),
            box("Check: type the width of the band you have quoted (upper limit minus lower limit).", 800,
                "Subtract the smaller limit from the larger one.",
                done="That width is the honest size of your answer. C is somewhere inside it, and the map "
                     "cannot tell you where."),
            say("<strong>Bronze move:</strong> match the shade to the key and quote the band, never a single "
                "exact figure."),
        ],
    },
    "silver": {
        "display": ("<p>Isotherms join places with the same temperature. Estimate the temperature at point T.</p>"
                    + TEACH_S_SVG),
        "steps": [
            say("With isolines you get more than a band. You can estimate a value between the lines."),
            box("Type the value, in °C, of the line immediately above T (the cooler one it sits between).", 12,
                "The label sits at the left-hand end of each line.",
                done="Locating T between two named lines is the whole set-up."),
            box("Type the value, in °C, of the line on the other side of T.", 14,
                "That is the next line down from T."),
            box("Type the gap between the two lines, in °C.", 2,
                "Subtract the cooler line's value from the warmer one.", phase="substitute"),
            box("T sits midway across the gap. Type half of the gap, in °C.", 1,
                "Halve the number you just worked out."),
            box("Add that to the cooler line's value. Type your estimate for T, in °C.", 13,
                "Start at the cooler line and move up by the amount you just found."),
            box("Check: type the difference in °C between your estimate and the warmer line.", 1,
                "Subtract your estimate from the warmer line's value.",
                done="Your estimate sits the same distance from each line, which is what midway means. If it "
                     "did not, the estimate would be outside the two lines and wrong."),
            say("<strong>Silver move:</strong> interpolate. Fraction of the way across × the gap, added to the "
                "lower line."),
        ],
    },
    "gold": {
        "display": ("<p>Two isobars are drawn 200 km apart. Work out the pressure gradient in mb per 100 km.</p>"
                    + TEACH_G_SVG),
        "steps": [
            say("A gradient answers: how fast does the value change as you move across the map?"),
            box("Type the value, in mb, of the lower-pressure isobar shown.", 996,
                "Read the two labels and type the smaller one.",
                done="Naming both lines before touching the maths keeps the gradient the right way up."),
            box("Type the value, in mb, of the higher-pressure isobar.", 1004,
                "Type the larger of the two labels."),
            box("Type the pressure change between the two lines, in mb.", 8,
                "Subtract the smaller reading from the larger one.", phase="substitute"),
            box("The gap is 200 km. Type how many 100 km lengths fit into that gap.", 2,
                "Divide the distance by 100."),
            box("Divide the pressure change by that number. Type the gradient in mb per 100 km.", 4,
                "Share the total change out evenly across each 100 km length."),
            box("Check: multiply your gradient by the number of 100 km lengths. Type the result in mb.", 8,
                "If the gradient is right, this must rebuild the total pressure change.",
                done="It rebuilds the change across the whole gap, so the rate per 100 km is right."),
            say("<strong>Gold move:</strong> a gradient is change ÷ distance, then scaled to the units the "
                "question asks for. Tight isobars mean a steep gradient and stronger winds."),
        ],
    },
}

# ---------------------------------------------------------- tier guides ----
tier_guides = {
    "bronze": {
        "title": "Bronze: read the key, then read the map",
        "steps": [
            "Start at the key. Shading runs light to dark, and darker nearly always means a higher value.",
            "Find your area, match its shade to a band, and quote the band rather than one exact figure.",
            "On isoline maps, read the value printed on the line. A point between two lines lies between "
            "their two values.",
        ],
        "example": {
            "question": "A key runs light (0 to 50), medium (50 to 200), dark (200 to 1000). Area M is medium. "
                        "What can you say about M?",
            "steps": [
                {"label": "Match the shade to the key",
                 "content": "<p>Medium is the second band of three</p>"},
                {"label": "Check it makes sense",
                 "content": "<p>M must be denser than the light band and less dense than the dark band</p>"},
                {"label": "Answer",
                 "content": "<p>M has between <strong>50 and 200 people per km²</strong></p>",
                 "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: estimate between the lines",
        "steps": [
            "Name the two isolines your point sits between, then work out the gap between them.",
            "Judge how far across the gap the point lies: midway, a quarter, three quarters.",
            "Take that fraction of the gap and add it to the lower line's value. That is interpolation.",
            "A shaded band is a range, so never report a choropleth value as an exact figure.",
        ],
        "example": {
            "question": "A point lies midway between the 12°C and 16°C isotherms. Estimate its temperature.",
            "steps": [
                {"label": "Gap between the lines", "content": "<p>16 − 12 = 4°C</p>"},
                {"label": "Fraction across", "content": "<p>Midway, so half of 4 = 2°C</p>"},
                {"label": "Check", "content": "<p>The estimate must sit between 12 and 16</p>"},
                {"label": "Answer", "content": "<p>12 + 2 = <strong>14°C</strong></p>",
                 "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: compare, calculate, criticise",
        "steps": [
            "Estimate both points first, then subtract your estimates. Do not subtract the line labels instead.",
            "For a gradient, divide the change in value by the distance, then scale it to the units asked for.",
            "Finish by naming a limitation: a choropleth averages a whole area and hides the variation inside it.",
        ],
        "example": {
            "question": "Pressure rises from 1000 mb to 1012 mb across 300 km. Find the gradient in mb per 100 km.",
            "steps": [
                {"label": "Change in pressure", "content": "<p>1012 − 1000 = 12 mb</p>"},
                {"label": "Lengths of 100 km", "content": "<p>300 ÷ 100 = 3</p>"},
                {"label": "Check", "content": "<p>4 × 3 rebuilds the 12 mb change, so the rate fits</p>"},
                {"label": "Answer", "content": "<p><strong>4 mb per 100 km</strong></p>",
                 "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# ------------------------------------------------------------- bronze ------
bronze = [
    {   # 0
        "image": CHORO,
        "display": "Look at the choropleth map below. Region X is marked in the Scottish Highlands. "
                   "What is the population density at X?",
        "options": ["0–50 people/km²", "50–200 people/km²", "200–1000 people/km²", "1000+ people/km²"],
        "solutions": [0],
        "calculator": False,
        "input_type": "multiple_choice",
        "hint": "Match the shade printed over Region X to the key squares one at a time, palest first.",
        "guided_steps": [
            say("Key first, map second."),
            box("Type how many shading bands the key on this map shows.", 4,
                "Count the coloured squares listed in the key.",
                done="Four bands, so your answer has to be one of four ranges."),
            box("Counting the palest shade as band 1, type the band number that matches the shading over "
                "Region X.", 1,
                "Hold the shade over X against each key square until one matches.", phase="substitute"),
            box("Type the lower limit of that band, in people per km².", 0,
                "Read the first number printed beside that key square."),
            box("Check: type the upper limit of the same band, in people per km².", 50,
                "Read the second number beside that key square.",
                done="Both limits come from the same key square, so the band you quote is the one X is "
                     "actually shaded in."),
            say("The option that names that band is the answer: <strong>0 to 50 people per km²</strong>."),
        ],
        "misconceptions": [
            {"pattern": "read_key_upside_down",
             "message": "You matched X to the darkest key square rather than to the shade actually printed "
                        "over it. Put the map shade next to each key square in turn.",
             "expect": 3},
            {"pattern": "off_by_one_band",
             "message": "You landed one band too high. Count the key squares from the palest and check which "
                        "number you stopped on.",
             "expect": 1},
        ],
    },
    {   # 1
        "image": CHORO,
        "display": "Look at the choropleth map. Which area has the highest population density?",
        "options": ["Scottish Highlands", "Rural Wales", "London", "Northern Ireland"],
        "solutions": [2],
        "calculator": False,
        "input_type": "multiple_choice",
        "hint": "Highest density means darkest shading, so find the top band in the key before you scan the map.",
        "guided_steps": [
            say("Highest value means darkest shade, so start by working out what the darkest shade means."),
            box("Type how many bands the key shows.", 4,
                "Count the coloured squares in the key.",
                done="You now know which key square is the top of the scale."),
            box("Type the lower limit of the darkest band, in people per km².", 1000,
                "Read the number beside the last key square.", phase="substitute"),
            box("Scan the four listed places on the map. Type how many of them are shaded in that darkest "
                "band.", 1,
                "Only count places whose shading really matches the last key square."),
            box("Check: type how many of the four listed places are shaded more darkly than that one place.", 0,
                "If your choice is the darkest, nothing can be darker than it.",
                done="Nothing outranks it, so the place you picked really is the densest of the four."),
            say("That single darkest place is <strong>London</strong>."),
        ],
        "misconceptions": [
            {"pattern": "picked_lightest",
             "message": "You picked the palest area on the map. Check which end of the key means more people, "
                        "not fewer.",
             "expect": 0},
            {"pattern": "chose_rural",
             "message": "You chose a largely rural area. Density is people per km², so judge it by shade, not "
                        "by how big the region looks.",
             "expect": 1},
        ],
    },
    {   # 2
        "image": ISOT,
        "display": "The isotherm map shows January temperatures across the UK. Point P is in southern England, "
                   "just south of the 8°C isotherm. Is the temperature at P likely to be warmer or cooler than 8°C?",
        "options": [
            "Cooler than 8°C, since P sits on the cooler side of the line",
            "Exactly 8°C, since P sits on the line itself",
            "Warmer than 8°C, since P sits on the warmer side of the line",
            "Cannot tell from an isotherm map",
        ],
        "solutions": [2],
        "calculator": False,
        "input_type": "multiple_choice",
        "hint": "Work out which way the isotherm values are climbing, then see which side of the line P is on.",
        "guided_steps": [
            say("First place P against the lines, then work out which way the numbers run."),
            box("Type the value, in °C, of the isotherm that P sits just south of.", 8,
                "The question names it, and the label is printed on the line."),
            box("The isotherms on this map are labelled 4, 6 and 8. Type the gap, in °C, between one isotherm "
                "and the next.", 2,
                "Subtract one label from the next label along.",
                done="A steady 2°C step means you can predict the next line's value in either direction."),
            box("The cooler values (4°C) lie towards the north. If the 2°C steps continue southwards, type the "
                "value of the next isotherm south of the 8°C line, in °C.", 10,
                "Add one step to 8.", phase="substitute"),
            box("P lies between the 8°C line and that next line south. Type your midway estimate for P, in °C.",
                9, "Add half the gap to the cooler line's value."),
            box("Check: type the difference in °C between your estimate for P and the 8°C line.", 1,
                "Subtract 8 from your estimate.",
                done="A positive difference means P is above the line's value, so P is on the warm side."),
            say("So P is <strong>warmer than 8°C</strong>."),
        ],
        "misconceptions": [
            {"pattern": "wrong_side_of_line",
             "message": "You put P on the cooler side. Check which direction the isotherm labels increase in "
                        "before deciding which side is which.",
             "expect": 0},
            {"pattern": "point_on_line",
             "message": "P is described as just south of the line, not on it, so it cannot take the line's own "
                        "value.",
             "expect": 1},
        ],
    },
    {   # 3
        "image": ISOB,
        "display": "On the weather map, Point A is in northern England between two isobars. "
                   "Which two isobars is A between?",
        "options": ["1004 mb and 1008 mb", "1008 mb and 1012 mb", "1012 mb and 1016 mb", "1016 mb and 1020 mb"],
        "solutions": [2],
        "calculator": False,
        "input_type": "multiple_choice",
        "hint": "Read the label on the line each side of A, not the labels on the lines further away.",
        "guided_steps": [
            say("Find A first, then read the label on each side of it."),
            box("Find Point A in northern England. Type the value, in mb, of the lower-pressure isobar of the "
                "two lines either side of it.", 1012,
                "Follow the line on one side of A until you meet its printed label.",
                done="Locating A between two labelled lines is the whole task here."),
            box("Type the value, in mb, of the higher-pressure isobar of that pair.", 1016,
                "Follow the line on the other side of A to its label.", phase="substitute"),
            box("Type the interval between one isobar and the next on this map, in mb.", 4,
                "Subtract the smaller of your two readings from the larger."),
            box("Check: type the pressure you would estimate at a point exactly midway between your two lines, "
                "in mb.", 1014,
                "Add half the interval to the lower reading.",
                done="Your midway value sits inside the pair you named, which is only possible if you read the "
                     "right two lines."),
            say("A therefore lies between <strong>1012 mb and 1016 mb</strong>."),
        ],
        "misconceptions": [
            {"pattern": "one_interval_low",
             "message": "Your pair is one interval too low. Trace each line out from A to its own label instead "
                        "of counting lines by eye.",
             "expect": 1},
            {"pattern": "one_interval_high",
             "message": "Your pair is one interval too high. Check you followed the lines immediately either "
                        "side of A.",
             "expect": 3},
        ],
    },
    {   # 4
        "image": ISOH,
        "display": "Look at the rainfall map. Point P is in North Wales and Point Q is on the east coast. "
                   "Which point receives more rainfall?",
        "options": ["Point P", "Point Q", "They receive the same", "Cannot tell from this map"],
        "solutions": [0],
        "calculator": False,
        "input_type": "multiple_choice",
        "hint": "Pin each point to the pair of isohyets it lies between, then compare the two bands.",
        "guided_steps": [
            say("Two points means two separate readings, then one comparison."),
            box("Find Point P in North Wales. Type the value, in mm, of the drier of the two isohyets it lies "
                "between.", 800,
                "Follow the line on the drier side of P until you reach its label.",
                done="P is now pinned between two named lines."),
            box("Type the value, in mm, of the wetter isohyet P lies between.", 1000,
                "Follow the line on P's other side to its label."),
            box("Now find Point Q on the east coast. Type the value, in mm, of the wetter of the two isohyets "
                "Q lies between.", 800,
                "Read the label on the line to Q's west.", phase="substitute"),
            box("Type the value, in mm, of the drier isohyet Q lies between.", 600,
                "Read the label on the line on Q's other side."),
            box("Check: type the difference in mm between P's wetter limit and Q's wetter limit.", 200,
                "Subtract Q's upper figure from P's upper figure.",
                done="P's whole band starts where Q's band ends, so every value P could take is at least as "
                     "high as any value Q could take."),
            say("<strong>Point P</strong> receives more rainfall."),
        ],
        "misconceptions": [
            {"pattern": "east_assumed_wetter",
             "message": "You chose the east coast point. Compare the isohyet labels either side of each point "
                        "rather than guessing from position.",
             "expect": 1},
            {"pattern": "bands_treated_as_equal",
             "message": "The two points do not sit between the same pair of lines, so their bands are not the "
                        "same. Read both pairs of labels again.",
             "expect": 2},
        ],
    },
    {   # 5
        "image": CHORO,
        "display": "A student says the choropleth map proves that everyone in London lives in a crowded area. "
                   "Why is this conclusion unreliable?",
        "options": [
            "Choropleth maps hide variation within areas, so parts of London are far less dense than others",
            "The map uses the wrong colours",
            "London is too small to show on a choropleth map",
            "Choropleth maps cannot display population data",
        ],
        "solutions": [0],
        "calculator": False,
        "input_type": "multiple_choice",
        "hint": "Think about what one shade has to do to a whole area before it can be printed on the map.",
        "guided_skip_reason": "Evaluative: judges the reliability of a claim about averaging. There is no "
                              "reading or calculation procedure that reaches the option.",
        "misconceptions": [
            {"pattern": "blames_colour_scheme",
             "message": "The colour choice is not the flaw here. Think about what a single shade does to the "
                        "range of values inside one area.",
             "expect": 1},
            {"pattern": "rejects_technique",
             "message": "Choropleths handle population data perfectly well. The weakness is in what one shade "
                        "per area conceals.",
             "expect": 3},
        ],
    },
    {   # 6
        "image": ISOB,
        "display": "On the weather map, the isobars are much closer together near the L (low pressure) in the "
                   "north-west than near the H (high pressure) in the south-east. What does this tell us?",
        "options": [
            "Wind speeds are stronger near the low pressure",
            "Wind speeds are stronger near the high pressure",
            "Wind speeds are the same everywhere",
            "Isobar spacing has nothing to do with wind",
        ],
        "solutions": [0],
        "calculator": False,
        "input_type": "multiple_choice",
        "hint": "Turn spacing into a gradient: the same pressure step squeezed into a shorter distance.",
        "guided_steps": [
            say("Spacing is really a gradient in disguise. Put numbers on it and it becomes obvious."),
            box("Look at the isobars near the L in the north-west and near the H in the south-east. Type the "
                "interval, in mb, between one isobar and the next on this map.", 4,
                "Subtract one printed isobar label from the next one along.",
                done="The step is the same everywhere, so only the distance between lines can differ."),
            box("Suppose that near the L the lines are 100 km apart. Type the pressure change per 100 km "
                "there, in mb.", 4,
                "One whole interval fits into one 100 km length."),
            box("Suppose that near the H the same interval is spread over 400 km. Type how many 100 km lengths "
                "that is.", 4, "Divide the distance by 100.", phase="substitute"),
            box("Type the pressure change per 100 km near the H, in mb.", 1,
                "Share the interval evenly across those 100 km lengths."),
            box("Check: type how many times steeper the gradient near the L is than the gradient near the H.", 4,
                "Divide the larger gradient by the smaller one.",
                done="A steeper pressure gradient drives faster air movement, so the tightly packed side is "
                     "the windy one."),
            say("Tightly packed isobars sit near the L, so <strong>wind speeds are stronger near the low "
                "pressure</strong>."),
        ],
        "misconceptions": [
            {"pattern": "spacing_inverted",
             "message": "You picked the side where the lines are spread out. Work out the pressure change per "
                        "100 km on each side and compare them.",
             "expect": 1},
            {"pattern": "spacing_ignored",
             "message": "Spacing is not decoration. The same pressure step over a shorter distance is a "
                        "steeper gradient.",
             "expect": 2},
        ],
    },
    {   # 7
        "image": ISOH,
        "display": "The rainfall map shows that the west of the UK receives more rainfall than the east. "
                   "What is the main reason for this pattern?",
        "options": [
            "The west is closer to cities which produce more rain",
            "Prevailing winds bring moist air from the Atlantic, which rises over western mountains causing rainfall",
            "The east coast is sheltered by Europe",
            "Eastern rivers carry water away faster",
        ],
        "solutions": [1],
        "calculator": False,
        "input_type": "multiple_choice",
        "hint": "Ask where the UK's wet air arrives from and what the land makes that air do first.",
        "guided_skip_reason": "Explanatory: asks for the physical cause of a pattern already read off the map. "
                              "No value can be read or calculated to reach the option.",
        "misconceptions": [
            {"pattern": "urban_cause",
             "message": "Cities do not create this national pattern. Think about the direction the UK's wet "
                        "air arrives from.",
             "expect": 0},
            {"pattern": "drainage_cause",
             "message": "Rivers move water after it has fallen. The pattern is about where the rain falls in "
                        "the first place.",
             "expect": 3},
        ],
    },
]

# ------------------------------------------------------------- silver ------
silver = [
    {   # 0
        "image": ISOT,
        "display": "On the isotherm map, Point Q is located in central Scotland between the 4°C and 6°C "
                   "isotherms, roughly midway between them. Estimate the January temperature at Q.",
        "solutions": [5],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Find the gap between the two lines, take the fraction of it the question describes, then add "
                "it to the cooler line.",
        "guided_steps": [
            say("Interpolation: how far across the gap is the point?"),
            box("Find Q in central Scotland. Type the value, in °C, of the cooler isotherm it sits between.", 4,
                "The question names both lines, and each label is printed on its line.",
                done="Q is now pinned between two named lines, which is all interpolation needs."),
            box("Type the value, in °C, of the warmer isotherm Q sits between.", 6,
                "Type the larger of the two labels."),
            box("Type the gap between the two isotherms, in °C.", 2,
                "Subtract the cooler label from the warmer one.", phase="substitute"),
            box("Q is midway across the gap. Type half of the gap, in °C.", 1, "Halve the gap."),
            box("Add that to the cooler isotherm. Type your estimate for Q, in °C.", 5,
                "Start at the cooler line and step up by the amount you just found."),
            box("Check: type the difference in °C between your estimate and the warmer isotherm.", 1,
                "Subtract your estimate from the warmer label.",
                done="Your estimate is the same distance from each line, which is exactly what midway means."),
        ],
        "misconceptions": [
            {"pattern": "took_lower_line",
             "message": "You quoted the cooler line itself instead of estimating between the lines. Q is "
                        "described as midway, not on a line.",
             "expect": 4},
            {"pattern": "took_upper_line",
             "message": "You quoted the warmer line itself. Interpolate across the gap rather than jumping to "
                        "a printed label.",
             "expect": 6},
        ],
    },
    {   # 1
        "image": ISOT,
        "display": "The isotherm map shows that south-western areas of the UK are warmer than the north-east "
                   "in January. The isotherms also bend slightly, with coastal areas warmer than inland areas "
                   "at the same latitude. What mainly explains the warmer coastal temperatures?",
        "options": [
            "Altitude, because coastal areas are lower",
            "Maritime influence, because the sea keeps coastal areas warmer in winter",
            "Latitude, because southern areas are always warmer",
            "Urbanisation, because coastal cities are warmer",
        ],
        "solutions": [1],
        "calculator": False,
        "input_type": "multiple_choice",
        "hint": "The comparison is coast against inland at the same latitude, so latitude cannot be the cause.",
        "guided_skip_reason": "Explanatory: asks for the physical control behind a bend in the isotherms. "
                              "Nothing on the map can be read or calculated to reach the option.",
        "misconceptions": [
            {"pattern": "latitude_confusion",
             "message": "The places being compared share a latitude, so latitude cannot explain the difference "
                        "between them.",
             "expect": 2},
            {"pattern": "urban_heat",
             "message": "Urban warming is local and small. Look for something that affects every stretch of "
                        "coast, city or not.",
             "expect": 3},
        ],
    },
    {   # 2
        "image": ISOB,
        "display": "On the weather map, Point B is located in south Wales between the 1012 mb and 1016 mb "
                   "isobars, roughly three-quarters of the way from 1012 towards 1016. Estimate the pressure at B.",
        "solutions": [1015],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Take three quarters of the gap between the two isobars and add it to the lower one.",
        "guided_steps": [
            say("Same interpolation as before, but the fraction is no longer a half."),
            box("Find B in south Wales. Type the value, in mb, of the lower-pressure isobar it sits between.",
                1012, "The question names both lines; type the smaller label.",
                done="B is pinned between two named isobars, ready to interpolate."),
            box("Type the value, in mb, of the higher-pressure isobar B sits between.", 1016,
                "Type the larger label."),
            box("Type the gap between the two isobars, in mb.", 4,
                "Subtract the lower label from the higher one.", phase="substitute"),
            box("B lies three quarters of the way across. Type three quarters of the gap, in mb.", 3,
                "Divide the gap by 4, then multiply by 3."),
            box("Add that to the lower isobar. Type your estimate for B, in mb.", 1015,
                "Start at the lower line and step up by the amount you just found."),
            box("Check: type the difference in mb between your estimate and the higher isobar.", 1,
                "Subtract your estimate from the higher label.",
                done="One quarter of the gap is left above your estimate, which is what three quarters across "
                     "should leave."),
        ],
        "misconceptions": [
            {"pattern": "quarter_not_three_quarters",
             "message": "You moved one quarter across instead of three quarters. Re-read which line the "
                        "question measures from.",
             "expect": 1013},
            {"pattern": "assumed_midway",
             "message": "You interpolated as if B were midway. The fraction given is not a half.",
             "expect": 1014},
        ],
    },
    {   # 3
        "image": CHORO,
        "display": "A geography student says: \"The choropleth map shows that Scotland has a low population "
                   "density everywhere.\" Using the map, explain why this statement is not fully accurate.",
        "options": [
            "Scotland has the same density as England",
            "The Central Belt (Glasgow, Edinburgh) has a much higher density than the Highlands, so the "
            "choropleth does show variation within Scotland",
            "Choropleth maps cannot show Scotland",
            "Scotland has a higher density than London",
        ],
        "solutions": [1],
        "calculator": False,
        "input_type": "multiple_choice",
        "hint": "Count how many different shades appear inside Scotland before you accept the word everywhere.",
        "guided_steps": [
            say("The word everywhere is testable. Count shades inside Scotland."),
            box("Type how many shading bands the key shows.", 4,
                "Count the coloured squares in the key.",
                done="Four bands means Scotland could contain up to four different shades."),
            box("Counting the palest as band 1, type the band number that matches the Highlands.", 1,
                "Compare the Highlands shading with each key square in turn.", phase="substitute"),
            box("The Glasgow and Edinburgh area is shaded more darkly than the Highlands. Type the smallest "
                "band number it could therefore be.", 2,
                "Darker means further along the key than band 1."),
            box("Check: type how many different shading bands you have now found inside Scotland.", 2,
                "Count the band numbers you typed.",
                done="More than one band inside one country means the density is not the same everywhere, so "
                     "the claim overreaches."),
            say("The option naming the Central Belt against the Highlands is the answer."),
        ],
        "misconceptions": [
            {"pattern": "compared_wrong_places",
             "message": "You compared Scotland with somewhere else. The claim is about variation inside "
                        "Scotland, so compare places within it.",
             "expect": 3},
            {"pattern": "flattened_to_one_band",
             "message": "You treated the whole country as one shade. Look for more than one band inside "
                        "Scotland's borders.",
             "expect": 0},
        ],
    },
    {   # 4  (was silver[5])
        "display": "A geography student says: \"Choropleth maps are better than dot maps because they show "
                   "exact values.\" Is this statement correct?",
        "options": [
            "Yes, choropleths always show exact values",
            "No, choropleths show ranges (bands), not exact values",
            "No, dot maps are always more accurate",
            "Yes, but only for population data",
        ],
        "solutions": [1],
        "calculator": False,
        "input_type": "multiple_choice",
        "hint": "Ask how many different true values one single shade on the map could stand for.",
        "guided_steps": [
            say("Test the claim by asking what one shade can and cannot pin down."),
            box("A key runs 0 to 50, 50 to 200, 200 to 1000, 1000 or more. Type how many bands that is.", 4,
                "Count the ranges listed.",
                done="Four shades have to cover every possible density in the country."),
            box("An area is shaded in the second band. Type the lowest density, in people per km², it could "
                "have.", 50, "Read where that band starts.", phase="substitute"),
            box("Type the highest density, in people per km², that same area could have.", 200,
                "Read where that band stops."),
            box("Check: type the width of that band, in people per km² (upper limit minus lower limit).", 150,
                "Subtract the lower limit from the upper limit.",
                done="One shade stands for a whole spread of possible values, so it cannot be an exact figure."),
            say("So the statement is wrong: a choropleth reports <strong>bands, not exact values</strong>."),
        ],
        "misconceptions": [
            {"pattern": "band_read_as_exact",
             "message": "You treated a shade as a precise figure. Look at how wide one band in the key is.",
             "expect": 0},
            {"pattern": "overclaims_dot_maps",
             "message": "The question is about what a choropleth reports, not about ranking the two "
                        "techniques in every situation.",
             "expect": 2},
        ],
    },
    {   # 5  (was silver[6])
        "image": ISOT,
        "display": "Using the isotherm map, estimate the temperature at Point P in southern England and Point Q "
                   "in central Scotland. What is the temperature difference between them?",
        "solutions": [2],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Estimate each point separately first, then subtract the estimates, not the printed labels.",
        "guided_steps": [
            say("Two estimates, then one subtraction. Never subtract the line labels."),
            box("Find P in southern England. Type the value, in °C, of the cooler isotherm it sits between.", 6,
                "Trace out from P to the cooler of the two lines either side.",
                done="P is pinned between two lines, so it can be estimated."),
            box("Type the value, in °C, of the warmer isotherm P sits between.", 8,
                "Trace out to the line on P's other side."),
            box("P lies roughly midway between them. Type your estimate for P, in °C.", 7,
                "Add half the gap to the cooler line.", phase="substitute"),
            box("Q sits roughly midway between the 4°C and 6°C isotherms. Type your estimate for Q, in °C.", 5,
                "Add half of that gap to its cooler line."),
            box("Subtract your estimate for Q from your estimate for P. Type the difference, in °C.", 2,
                "Take the smaller estimate away from the larger one."),
            box("Check: add your difference to your estimate for Q. Type the result, in °C.", 7,
                "A correct difference must rebuild the warmer estimate.",
                done="It rebuilds P exactly, so the gap between the two places is right."),
        ],
        "misconceptions": [
            {"pattern": "line_label_for_estimate",
             "message": "You used a printed line label for one point and an interpolated estimate for the "
                        "other. Estimate both the same way before subtracting.",
             "expect": 3},
            {"pattern": "added_instead_of_subtracted",
             "message": "You combined the two estimates instead of comparing them. A difference is one taken "
                        "away from the other.",
             "expect": 12},
        ],
    },
    {   # 6  (was silver[4])
        "image": ISOH,
        "display": "On the rainfall map, Point Q is on the east coast just east of the 800 mm isohyet. "
                   "Is the annual rainfall at Q likely to be more or less than 800 mm?",
        "options": [
            "More than 800 mm, because Q is on the wetter side of the line",
            "Exactly 800 mm, because Q is on the line",
            "Less than 800 mm, because Q is on the drier side of the line",
            "Cannot tell from this map",
        ],
        "solutions": [2],
        "calculator": False,
        "input_type": "multiple_choice",
        "hint": "Work out which way the isohyet values fall as you cross the country, then place Q on that scale.",
        "guided_steps": [
            say("Which way do the numbers run? Answer that and the side question answers itself."),
            box("Find Q on the east coast. Type the value, in mm, of the isohyet it sits just east of.", 800,
                "The question names it and the label is printed on the line."),
            box("The isohyets on this map are labelled 600, 800 and 1000. Type the gap between one isohyet and "
                "the next, in mm.", 200,
                "Subtract one label from the next along.",
                done="A steady 200 mm step lets you name the next line in either direction."),
            box("Rainfall totals fall towards the east coast. Type the value of the next isohyet east of the "
                "800 mm line, in mm.", 600, "Take one step down from 800.", phase="substitute"),
            box("Q lies between those two lines. Type your midway estimate for Q, in mm.", 700,
                "Add half the gap to the drier line."),
            box("Check: type the difference in mm between the 800 mm line and your estimate for Q.", 100,
                "Subtract your estimate from 800.",
                done="Your estimate falls short of the line's value, so Q must be drier than it."),
            say("So Q receives <strong>less than 800 mm</strong>."),
        ],
        "misconceptions": [
            {"pattern": "wetter_side_inverted",
             "message": "You placed Q on the wetter side. Check which direction the isohyet labels are falling "
                        "in before choosing a side.",
             "expect": 0},
            {"pattern": "point_on_line",
             "message": "Q is described as just east of the line, not on it, so it cannot take the line's own "
                        "value.",
             "expect": 1},
        ],
    },
]

# --------------------------------------------------------------- gold ------
gold = [
    {   # 0
        "image": ISOH,
        "display": "Using the rainfall map, estimate the annual rainfall at Point P and Point Q. Calculate the "
                   "difference in rainfall between them. Give your answer in mm.",
        "solutions": [200],
        "calculator": True,
        "input_type": "single_value",
        "hint": "Interpolate each point on its own, then take the smaller estimate away from the larger.",
        "guided_steps": [
            say("Two interpolations, then one subtraction."),
            box("Find Point P on the map. Type the value, in mm, of the drier isohyet it sits between.", 800,
                "Trace out from P to the lower of the two labels either side.",
                done="P is pinned between two named lines."),
            box("Type the value, in mm, of the wetter isohyet P sits between.", 1000,
                "Trace out to the line on P's other side."),
            box("P lies roughly midway between them. Type your estimate for P, in mm.", 900,
                "Add half the gap to the drier line.", phase="substitute"),
            box("Point Q sits roughly midway between the 600 mm and 800 mm isohyets. Type your estimate for Q, "
                "in mm.", 700, "Add half of that gap to its drier line."),
            box("Subtract your estimate for Q from your estimate for P. Type the difference, in mm.", 200,
                "Take the smaller estimate away from the larger one."),
            box("Check: add your difference to your estimate for Q. Type the result, in mm.", 900,
                "A correct difference must rebuild the wetter estimate.",
                done="It rebuilds P exactly, so the gap between the two places is right."),
        ],
        "misconceptions": [
            {"pattern": "used_line_labels",
             "message": "You subtracted a line label from a line label instead of subtracting your two "
                        "estimates. Interpolate both points first.",
             "expect": 0},
            {"pattern": "added_estimates",
             "message": "You combined the two rainfall figures rather than comparing them. A difference is one "
                        "taken away from the other.",
             "expect": 1600},
        ],
    },
    {   # 1
        "display": "A geographer creates a choropleth map of mean household income by local authority. One area "
                   "has a mean of £45,000, but 80% of households earn under £25,000. What problem does this "
                   "illustrate?",
        "options": [
            "The colour is too dark for this area",
            "The mean is skewed by extreme values, hiding the fact that most residents have lower incomes",
            "Choropleth maps cannot display income data",
            "The area is too small to shade accurately",
        ],
        "solutions": [1],
        "calculator": True,
        "input_type": "multiple_choice",
        "hint": "Work out what the remaining fifth of households must earn for the mean to come out that high.",
        "guided_steps": [
            say("Put numbers on it. Imagine 100 households in this area."),
            box("Read the figure in the question. Type the percentage of households earning under £25,000.", 80,
                "It is stated in the question.",
                done="So 80 of every 100 households sit below £25,000."),
            box("The map shades this area by a mean of £45,000. For 100 households, type the total income in £ "
                "that mean implies.", 4500000, "Multiply the mean by 100.", phase="substitute"),
            box("Type the largest total, in £, those 80 lower-earning households could contribute.", 2000000,
                "Multiply 80 by £25,000."),
            box("Type the smallest total, in £, the remaining 20 households must contribute.", 2500000,
                "Subtract the lower earners' total from the whole area's total."),
            box("Check: divide that by 20. Type the smallest mean income, in £, of those 20 households.", 125000,
                "Share their total out between the 20 households.",
                done="A small group on very high incomes drags the mean far above what most households "
                     "actually earn, so the shade misrepresents the typical resident."),
            say("That is <strong>a mean skewed by extreme values</strong>. A median would describe the typical "
                "household far better."),
        ],
        "misconceptions": [
            {"pattern": "blames_shading",
             "message": "The shade follows the statistic it was given. The problem is in the statistic, not "
                        "the colour.",
             "expect": 0},
            {"pattern": "rejects_technique",
             "message": "Income maps like this are common. Ask instead what an average does to a very uneven "
                        "spread of values.",
             "expect": 2},
        ],
    },
    {   # 2
        "image": ISOB,
        "display": "On the weather map, the distance between the 1000 mb and 1008 mb isobars is approximately "
                   "400 km. Calculate the pressure gradient in mb per 100 km.",
        "solutions": [2],
        "calculator": True,
        "input_type": "single_value",
        "hint": "Find the pressure change first, then share it evenly across each 100 km of the distance.",
        "guided_steps": [
            say("A gradient is change ÷ distance, scaled to the units asked for."),
            box("Find the two isobars named in the question on the map. Type the value, in mb, of the "
                "lower-pressure one.", 1000,
                "Type the smaller of the two labels.",
                done="Naming both lines before any maths keeps the gradient the right way up."),
            box("Type the value, in mb, of the higher-pressure isobar.", 1008, "Type the larger label."),
            box("Type the pressure change between them, in mb.", 8,
                "Subtract the lower reading from the higher one.", phase="substitute"),
            box("The gap is 400 km. Type how many 100 km lengths that is.", 4, "Divide the distance by 100."),
            box("Divide the pressure change by that number. Type the gradient in mb per 100 km.", 2,
                "Share the total change evenly across each 100 km length."),
            box("Check: multiply your gradient by the number of 100 km lengths. Type the result in mb.", 8,
                "This must rebuild the total pressure change.",
                done="It rebuilds the change across the whole 400 km, so the rate per 100 km is right."),
        ],
        "misconceptions": [
            {"pattern": "divided_upside_down",
             "message": "You divided distance by pressure change. The units asked for are millibars per "
                        "distance, so the pressure change goes on top.",
             "expect": 50},
            {"pattern": "no_scaling",
             "message": "You stopped at the total change across the whole gap. The question wants the change "
                        "per 100 km.",
             "expect": 8},
        ],
    },
    {   # 3
        "image": ISOT,
        "display": "On the isotherm map, a town is located three-quarters of the way from the 4°C isotherm "
                   "towards the 6°C isotherm. Estimate the temperature at the town. Give your answer to 1 "
                   "decimal place.",
        "solutions": [5.5],
        "calculator": False,
        "input_type": "single_value",
        "hint": "Take three quarters of the gap between the two isotherms and add it to the line you start from.",
        "guided_steps": [
            say("Fraction of the gap, added to the line the question measures from."),
            box("Find the town on the map. Type the value, in °C, of the isotherm the question measures from.",
                4, "It is the line named first in the question.",
                done="Interpolation always runs from the line you start at, so fixing that first matters."),
            box("Type the value, in °C, of the isotherm the town is measured towards.", 6,
                "It is the second line named."),
            box("Type the gap between the two isotherms, in °C.", 2,
                "Subtract the starting line's value from the other.", phase="substitute"),
            box("Type three quarters of that gap, in °C.", 1.5, "Divide the gap by 4, then multiply by 3."),
            box("Add that to the starting isotherm. Type your estimate for the town, in °C.", 5.5,
                "Step up from the line you started at by the amount you just found."),
            box("Check: type the difference in °C between your estimate and the 6°C isotherm.", 0.5,
                "Subtract your estimate from 6.",
                done="One quarter of the gap is left above your estimate, which is exactly what three quarters "
                     "of the way across should leave."),
        ],
        "misconceptions": [
            {"pattern": "assumed_midway",
             "message": "You interpolated as if the town were midway between the lines. The fraction given is "
                        "not a half.",
             "expect": 5},
            {"pattern": "measured_from_wrong_line",
             "message": "You measured three quarters down from the warmer line instead of up from the line the "
                        "question starts at.",
             "expect": 4.5},
        ],
    },
    {   # 4
        "display": "A student needs to compare literacy rates across African countries. She has exact percentage "
                   "data for each country. Suggest why a choropleth map would be an appropriate technique.",
        "options": [
            "Literacy rate is a ratio measured per area, making area-shading ideal for comparing countries at a glance",
            "Dot maps cannot show African countries",
            "Choropleths are always better than other map types",
            "Choropleth maps show exact values rather than estimates",
        ],
        "solutions": [0],
        "calculator": False,
        "input_type": "multiple_choice",
        "hint": "Ask what kind of data suits shading a whole area rather than plotting points inside it.",
        "guided_skip_reason": "Evaluative: judges the fit between a data type and a technique. No value can be "
                              "read or calculated to reach the option.",
        "misconceptions": [
            {"pattern": "claims_exact_values",
             "message": "A choropleth reports bands, so exactness is not the reason to choose it. Think about "
                        "the type of data instead.",
             "expect": 3},
            {"pattern": "always_better",
             "message": "No technique is always best. The justification has to come from this particular data.",
             "expect": 2},
        ],
    },
]

# ------------------------------------------------------------- assemble ----
pd = json.load(io.open(os.path.join(HERE, "_live_L08.json"), encoding="utf-8"))

pd["method_card"] = {
    "title": "Choropleth & Isoline Maps",
    "steps": [
        "Check the key: match shading or lines to values",
        "Read values for each area, or interpolate between lines",
        "Describe spatial patterns: clusters, gradients",
        "Isolines close together = steep; far apart = gentle",
    ],
    "content": ("<p><strong>Choropleth maps</strong> shade whole areas by value, and darker usually means "
                "higher. They suit rates and densities. Read the key first, then match each area to a band. "
                "A choropleth gives a range, not an exact figure, and it averages the whole area, so any "
                "variation inside it is hidden.</p>"
                "<p><strong>Isoline maps</strong> join points of equal value: contours (height), isotherms "
                "(temperature), isobars (pressure), isohyets (rainfall). A point between two lines lies "
                "between their values, so interpolate: take the fraction of the way across, multiply by the "
                "gap, add it to the lower line. Lines close together mean a steep gradient; lines far apart "
                "mean gradual change.</p>"),
    "example": ("<p>A point midway between the 15°C and 20°C isotherms: gap = 5, half of 5 = 2.5, so about "
                "<strong>17.5°C</strong>. On a choropleth with bands 0 to 100 and 100 to 250, an area in the "
                "second band has between <strong>100 and 250 people per km²</strong>, and no closer figure "
                "than that.</p>"),
}

pd["problem_bank"] = {
    "bronze": bronze,
    "silver": silver,
    "gold": gold,
    "bronze_description": "Read one value straight off a map: match a shade to its key band, or read the "
                          "isoline a point sits on or beside.",
    "silver_description": "Estimate a value between two isolines by interpolating, and judge what a shaded "
                          "band does and does not tell you.",
    "gold_description": "Combine two readings into a difference or a gradient, and weigh up what the technique "
                        "hides as well as what it shows.",
}

pd["tier_guides"] = tier_guides
pd["guided"] = {"opener": opener, "teach": teach}

out = os.path.join(HERE, "lesson_L08.json")
io.open(out, "w", encoding="utf-8").write(json.dumps(pd, ensure_ascii=False, indent=1))
print("wrote", out, os.path.getsize(out))
