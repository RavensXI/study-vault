# -*- coding: utf-8 -*-
"""Build the guided practice_data for Geography Skills L10 Fieldwork Data & Sampling."""
import json, io, os

HERE = os.path.dirname(os.path.abspath(__file__))
live = json.load(io.open(os.path.join(HERE, "_L10_live.json"), encoding="utf-8"))

YN = " Type 1 for yes or 0 for no."


def box(pre, answer, hint, done=None, post=None, phase=None, say=None):
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


def sayst(s):
    return {"say": s}


pd = {}

# ---------------------------------------------------------------- method card
pd["method_card"] = {
    "title": "Sampling & Fieldwork Data",
    "steps": [
        "Name the method: chance, fixed interval, or zones first",
        "For a stratified sample, give each group its share of the total",
        "Screen for anomalies against the pattern and against the scale",
        "Judge reliability from repeats and from sample size",
    ],
    "content": (
        "<p>You cannot measure everything, so you take a <strong>sample</strong>.</p>"
        "<p><strong>Random:</strong> points chosen by chance, so every point has an equal chance. "
        "Low bias, but coverage can be patchy.</p>"
        "<p><strong>Systematic:</strong> points at a fixed, repeating interval. Even coverage and easy "
        "to run, but a pattern that repeats at the same spacing can be missed.</p>"
        "<p><strong>Stratified:</strong> the area is split into groups, and each group gets a share of "
        "the sample matching its size. Every group appears, but you must know the area first.</p>"
        "<p>An <strong>anomaly</strong> is a value far outside the pattern, or outside the limits of the "
        "scale. Investigate the cause before removing it.</p>"
        "<p><strong>Reliability</strong> grows with more readings, repeats at each site, and the same "
        "method every time.</p>"
    ),
    "example": (
        "<p><strong>Scenario:</strong> velocity measured at 10 equally spaced points down a river.</p>"
        "<p><strong>Method:</strong> systematic, because the interval repeats.</p>"
        "<p><strong>Anomaly:</strong> a reading of 0.1 m/s where the rest are above 1.5 m/s points to a "
        "weir, a bridge, or a slip in recording.</p>"
    ),
}

pd["topic_links"] = live["topic_links"]
pd["related_videos"] = live["related_videos"]
we = json.loads(json.dumps(live["worked_examples"]))
we[1]["steps"][0]["content"] = (
    "<p>Most values are between 12 and 17 cm. The value <strong>68 cm</strong> is far higher than the "
    "others, so this is the anomaly.</p>"
)
pd["worked_examples"] = we

# ---------------------------------------------------------------- tier guides
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: naming the method and spotting the odd one out",
        "steps": [
            "Ask how the points were chosen. Chance means <strong>random</strong>. A fixed, repeating "
            "interval means <strong>systematic</strong>. Splitting the area into zones first means "
            "<strong>stratified</strong>.",
            "To find an anomaly, look for the value that sits far outside the group the rest fall into, "
            "or outside the limits of the scale.",
            "Do not delete an odd value on sight. Name it, then suggest why it happened.",
        ],
        "example": {
            "question": "Litter counts taken every 20 m along a 100 m path: 4, 5, 3, 41, 4, 5. "
                        "Name the sampling method and the anomaly.",
            "steps": [
                {"label": "Look at the spacing",
                 "content": "<p>A reading every 20 m is a fixed, repeating interval.</p>"},
                {"label": "Name the method",
                 "content": "<p>A fixed interval means systematic sampling.</p>"},
                {"label": "Check the values",
                 "content": "<p>Five counts sit between 3 and 5. One sits nowhere near them.</p>"},
                {"label": "Answer", "isAnswer": True, "is_answer": True,
                 "content": "<p>Systematic sampling, and the anomaly is <strong>41</strong>.</p>"},
            ],
        },
    },
    "silver": {
        "title": "Silver: proportional shares and reliability",
        "steps": [
            "For a stratified sample, find each group's share of the total: group size ÷ total. Then "
            "multiply the sample size by that share.",
            "Check that your shares add back up to the sample size.",
            "Reliability comes from repeats. Work out the range of the repeats at each site: the widest "
            "range is the least consistent.",
        ],
        "example": {
            "question": "A village of 800 people is 60% adults and 40% children. How many of a 40 person "
                        "sample should be children?",
            "steps": [
                {"label": "Find the share", "content": "<p>40% as a decimal is 0.4.</p>"},
                {"label": "Apply it to the sample", "content": "<p>40 × 0.4 = 16.</p>"},
                {"label": "Check", "content": "<p>Adults: 40 × 0.6 = 24. Then 24 + 16 = 40, the whole "
                                              "sample, so nothing is missing.</p>"},
                {"label": "Answer", "isAnswer": True, "is_answer": True,
                 "content": "<p><strong>16 children.</strong></p>"},
            ],
        },
    },
    "gold": {
        "title": "Gold: rebuilding a mean and judging a method",
        "steps": [
            "A mean hides a total. Total = mean × number of readings. Take the faulty reading off the "
            "total, then divide by the count that is left.",
            "Screen data against the scale: a value beyond the highest possible score, or outside the "
            "numbering of the study area, cannot be used.",
            "To judge a method, ask what the study is trying to show, and whether the sample covers it "
            "evenly.",
        ],
        "example": {
            "question": "Ten soil pH readings have a mean of 6.2. One reading of 12.0 came from a spilled "
                        "chemical and is removed. What is the new mean, to 1 decimal place?",
            "steps": [
                {"label": "Rebuild the total", "content": "<p>6.2 × 10 = 62.</p>"},
                {"label": "Remove the faulty reading", "content": "<p>62 − 12.0 = 50.</p>"},
                {"label": "Check the count", "content": "<p>Nine readings are left, so divide by 9: "
                                                        "50 ÷ 9 = 5.55...</p>"},
                {"label": "Answer", "isAnswer": True, "is_answer": True,
                 "content": "<p><strong>5.6</strong></p>"},
            ],
        },
    },
}

# ---------------------------------------------------------------- opener
OPENER_SVG = (
    '<svg viewBox="0 0 320 96" role="img" aria-label="A bar of 200 students split into a large Year 10 '
    'section of 160 and a small Year 11 section of 40">'
    '<rect x="10" y="22" width="240" height="34" fill="#cfe3d8" stroke="#8fb3a2"/>'
    '<rect x="250" y="22" width="60" height="34" fill="#e8d9c0" stroke="#c2ab86"/>'
    '<text x="130" y="44" font-size="13" text-anchor="middle" fill="#2d2a26">Year 10: 160</text>'
    '<text x="280" y="44" font-size="10" text-anchor="middle" fill="#2d2a26">Yr 11: 40</text>'
    '<text x="10" y="80" font-size="11" fill="#2d2a26">200 students altogether</text></svg>'
)

pd["guided"] = {
    "opener": {
        "display": (
            "<p>Your school has 200 students: 160 in Year 10 and 40 in Year 11. You are allowed to ask "
            "only 10 of them what they think of the canteen, and you want the 10 to speak for the whole "
            "school.</p>" + OPENER_SVG
        ),
        "steps": [
            box("Suppose for a moment that the two year groups were exactly the same size. How many of "
                "your 10 students would come from each year?", 5,
                "Share the 10 students out evenly between the two years.",
                done="An even split is the instinct, and it is fair only while the groups are the same size."),
            box("Now look at the real school. Year 10 holds 160 of the 200 students. Write that as a "
                "decimal fraction of the school.", 0.8,
                "Divide the Year 10 number by the number of students in the whole school.",
                done="Year 10 is 0.8 of the school, so it should fill 0.8 of your sample."),
            box("Share the 10 places out fairly. How many of your 10 students should be from Year 10?", 8,
                "Take that same fraction of the 10 places.",
                done="8 places for Year 10 leaves 2 for Year 11, and 8 + 2 = 10."),
            sayst("You have just done <strong>stratified sampling</strong>. You split the school into "
                  "groups, worked out each group's share of the whole, and gave each group that same "
                  "share of your sample. Everything in this lesson builds on that one move, plus two "
                  "others: naming a method from how its points were chosen, and spotting a reading that "
                  "does not belong."),
        ],
    },
    "teach": {
        "bronze": {
            "display": (
                "<p>A student measures pebble length (mm) every 4 metres along a 40 m transect running "
                "from the sea towards the cliff.</p>"
                "<p>Readings: 42, 45, 41, 48, 44, 220, 46, 43, 45, 47</p>"
            ),
            "steps": [
                sayst("Two jobs here: name the method from <strong>how the points were chosen</strong>, "
                      "then screen the readings for one that does not belong. Start by getting your "
                      "bearings in the list."),
                box("How many readings are in the list?", 10,
                    "Count them one at a time from the left.",
                    done="Ten readings along a 40 m transect."),
                box("How many metres apart is one reading from the next?", 4,
                    "The spacing is stated in the first sentence.",
                    done="Every gap is 4 m, and it never changes."),
                box("A gap that is the same size every single time is a fixed, repeating interval." + YN,
                    1, "Compare the first gap with the last gap.",
                    done="A fixed repeating interval is exactly what <strong>systematic sampling</strong> "
                         "means, so the method is named."),
                box("Now screen the values. Nine readings sit between 41 and 48. Type the one reading "
                    "that sits far outside that band.", 220,
                    "Scan the list for the value you would notice from across the room.",
                    phase="substitute"),
                box("Divide that reading by 44, a typical value here, to see how far out it is.", 5,
                    "220 ÷ 44.",
                    done="Five times the typical pebble, so it is not a pebble on this beach at all."),
                box("How many readings should you report as anomalies?", 1,
                    "Count the readings that fall outside the band the rest sit in.",
                    done="Only one reading breaks the pattern, so it alone is the anomaly, most likely a "
                         "recording slip for 22 mm."),
                sayst("Method named from the spacing, anomaly found by comparing each value with the band "
                      "the rest fall into. That is the whole of bronze."),
            ],
        },
        "silver": {
            "display": (
                "<p>A town of 4,000 people has three zones: housing 2,000 people, shops 1,200 people, "
                "industry 800 people.</p>"
                "<p>A student can survey 50 people and wants each zone represented in proportion.</p>"
            ),
            "steps": [
                sayst("Stratified sampling shares the sample out in the same proportions as the "
                      "population. Get the total first, because every share is measured against it."),
                box("Add the three zone populations. What is the total population?", 4000,
                    "2000 + 1200 + 800.",
                    done="Everything from here is a share of 4,000."),
                box("Housing holds 2,000 of them. Write housing's share as a percentage.", 50,
                    "2000 ÷ 4000, then multiply by 100.",
                    done="Housing is half the town, so it should be half the sample."),
                box("Apply that share to the survey: 50% of 50 people.", 25,
                    "Halve the sample size.", phase="substitute",
                    done="Housing gets 25 of the 50 places."),
                box("Now shops: 1200 ÷ 4000 = 0.3. How many of the 50 places is that?", 15,
                    "Multiply 50 by 0.3."),
                box("And industry: 800 ÷ 4000 = 0.2. How many places?", 10,
                    "Multiply 50 by 0.2."),
                box("Add the three shares: 25 + 15 + 10.", 50,
                    "Total them up and compare with the sample size.",
                    done="The shares rebuild the full sample of 50, so no zone has been over or under "
                         "sampled. Always finish a stratified calculation with this check."),
            ],
        },
        "gold": {
            "display": (
                "<p>Twelve infiltration readings have a mean of 3.5 mm per minute.</p>"
                "<p>One reading of 21 mm per minute was taken next to a burst pipe and is removed as an "
                "anomaly.</p>"
            ),
            "steps": [
                sayst("You are not given the readings, only the mean. The gold move is to run the mean "
                      "<strong>backwards</strong> into a total, edit the total, then run it forwards again."),
                box("How many readings were taken before anything was removed?", 12,
                    "The first sentence gives the count."),
                box("Total of all readings = mean × number of readings. Work out 3.5 × 12.", 42,
                    "Multiply the mean by the count.",
                    done="The 12 readings add up to 42, even though you never saw them."),
                box("Take the faulty reading off that total: 42 − 21.", 21,
                    "Subtract the anomaly from the total, not from the mean.", phase="substitute"),
                box("How many readings are left?", 11,
                    "One reading has gone from the original count."),
                box("New mean: 21 ÷ 11, to 1 decimal place.", 1.9,
                    "Divide the corrected total by the corrected count."),
                box("Check by running it forwards: 1.9 × 11, rounded to the nearest whole number.", 21,
                    "Multiply your new mean by the new count.",
                    done="It returns the corrected total, so the mean is right. One faulty reading had "
                         "been dragging the average up by almost double."),
            ],
        },
    },
}

# ---------------------------------------------------------------- problem bank
bronze = []

bronze.append({
    "display": "A student measures soil temperature every 10 metres along a 100 m transect across a field. "
               "What type of sampling is this?",
    "options": ["Random sampling", "Systematic sampling", "Stratified sampling", "Convenience sampling"],
    "solutions": [1],
    "calculator": False,
    "input_type": "multiple_choice",
    "hint": "Ask whether the points were chosen by chance, by a fixed repeating interval, or zone by zone.",
    "guided_steps": [
        sayst("Sampling methods are told apart by <strong>how the points were chosen</strong>. Work the "
              "spacing out before you pick an option."),
        box("What is the gap, in metres, between one reading and the next?", 10,
            "The interval is stated in the question."),
        box("How many of those 10 m gaps fit into the 100 m transect?", 10,
            "Divide the transect length by the gap.",
            done="Ten equal gaps, from one end to the other."),
        box("Were the reading positions picked out of a random number table?" + YN, 0,
            "Ask whether chance played any part in choosing where to stop.", phase="substitute"),
        box("Was the field first split into separate zones with the readings shared out between them?" + YN,
            0, "Look for named groups or zones in the question."),
        box("Is the gap between readings the same size every time?" + YN, 1,
            "Compare the first gap with the last one.",
            done="No chance, no zones, and one fixed repeating interval. That combination names exactly "
                 "one method, and the check holds."),
        sayst("A fixed, repeating interval is the definition of <strong>systematic sampling</strong>. "
              "Choose that option."),
    ],
    "misconceptions": [
        {"pattern": "random", "expect": 0,
         "message": "Random sampling means chance decided every point. Look again at how the student "
                    "decided where to stop walking."},
        {"pattern": "stratified", "expect": 2,
         "message": "Stratified sampling needs the area split into groups first, with the sample shared "
                    "between them. Check whether any groups are named here."},
    ],
})

bronze.append({
    "display": "A student uses a random number table to pick 20 grid squares for a land use survey. "
               "What type of sampling is this?",
    "options": ["Random sampling", "Systematic sampling", "Stratified sampling", "Opportunistic sampling"],
    "solutions": [0],
    "calculator": False,
    "input_type": "multiple_choice",
    "hint": "Work out whether the squares were chosen by chance, by a repeating rule, or group by group.",
    "guided_steps": [
        sayst("Start by pinning down what is being chosen and how many of them."),
        box("How many grid squares will be surveyed?", 20,
            "The number is given in the question.",
            done="Twenty squares, chosen by something. The something is what names the method."),
        box("Does the student use a fixed rule such as taking every 5th square?" + YN, 0,
            "Look for a repeating interval in the question.", phase="substitute"),
        box("Does every grid square in the area have the same chance of coming out of the number table?"
            + YN, 1, "Ask whether the table favours any square over another."),
        box("Were the squares first sorted into zones before sampling?" + YN, 0,
            "Look for named sub-areas in the question.",
            done="Equal chance for every square, no repeating rule and no zones. That check rules out "
                 "every option but one."),
        sayst("Equal chance for every point is the definition of <strong>random sampling</strong>. "
              "Choose that option."),
    ],
    "misconceptions": [
        {"pattern": "systematic", "expect": 1,
         "message": "Systematic sampling uses a repeating interval such as every 5th square. Check "
                    "whether any interval is mentioned here."},
        {"pattern": "stratified", "expect": 2,
         "message": "Stratified sampling divides the area into sub-groups first. No groups are set up "
                    "in this survey."},
    ],
})

bronze.append({
    "display": "River velocity readings (m/s): 0.3, 0.5, 0.4, 0.6, 5.2, 0.5, 0.4. "
               "Which value is most likely an anomaly?",
    "solutions": [5.2],
    "calculator": False,
    "input_type": "single_value",
    "hint": "Find the band that most of the readings fall inside, then pick the one reading sitting far "
            "outside it.",
    "guided_steps": [
        sayst("An anomaly is found by <strong>comparing</strong>, not by calculating. Get your bearings "
              "in the list first."),
        box("How many readings are listed?", 7,
            "Count them one at a time."),
        box("Type the smallest reading in the list.", 0.3,
            "Scan left to right for the lowest value.",
            done="The bottom of the main band."),
        box("Six of the seven readings sit between 0.3 and 0.6. Type the largest reading in the list.",
            5.2, "Scan for the value that stands out from the rest.", phase="substitute"),
        box("Divide that reading by 0.5, a typical value here, to see how far out it is.", 10.4,
            "5.2 ÷ 0.5."),
        box("How many readings lie outside the band 0.3 to 0.6?", 1,
            "Check each reading against the band.",
            done="Only one reading breaks the pattern, and it is over ten times a normal reading for "
                 "this river, so it is the anomaly."),
    ],
    "misconceptions": [
        {"pattern": "lowest", "expect": 0.3,
         "message": "You have picked the smallest number. An anomaly is the reading furthest from the "
                    "pattern, not automatically the lowest one."},
        {"pattern": "range", "expect": 4.9,
         "message": "That is the spread between the highest and lowest readings, not a reading taken "
                    "from the list. The question asks for a value that appears in the data."},
    ],
})

bronze.append({
    "display": "A student needs to survey environmental quality at 30 sites in a town that has three "
               "distinct zones: town centre, suburbs, and industrial area. Which sampling method "
               "should they use?",
    "options": ["Random sampling", "Systematic sampling", "Stratified sampling", "All three are equally good"],
    "solutions": [2],
    "calculator": False,
    "input_type": "multiple_choice",
    "hint": "Ask which method guarantees that every named zone gets some of the 30 sites.",
    "guided_steps": [
        sayst("When a question names separate zones, count them first: the number of zones usually "
              "decides the method."),
        box("How many distinct zones does the town have?", 3,
            "They are listed in the question.",
            done="Three zones, and all three matter to the study."),
        box("If the 30 sites were shared equally between the zones, how many sites would each zone get?",
            10, "Divide the sites between the zones.", phase="substitute"),
        box("Could chance alone leave one zone with no sites at all?" + YN, 1,
            "Picture 30 points dropped at random on a town map."),
        box("Add the three zone shares back together: 10 + 10 + 10.", 30,
            "Total the shares and compare with the number of sites.",
            done="The shares rebuild the full 30 sites with every zone covered, which is what splitting "
                 "the town into groups first achieves."),
        sayst("Splitting the area into groups and sampling within each is <strong>stratified "
              "sampling</strong>. Choose that option."),
    ],
    "misconceptions": [
        {"pattern": "random", "expect": 0,
         "message": "Chance could drop most points in one zone and none in another. Ask which method "
                    "guarantees each zone appears."},
        {"pattern": "systematic", "expect": 1,
         "message": "A fixed interval takes no notice of zone boundaries, so a whole zone can be walked "
                    "straight past."},
    ],
})

bronze.append({
    "display": "A beach profile survey measures beach height every 5 metres from the sea to the cliff. "
               "The student records: 0.2, 0.8, 1.5, 2.3, 3.1, 3.8, 4.5 metres. Are there any anomalies?",
    "options": ["Yes, 0.2 is too low", "Yes, 4.5 is too high",
                "No, the values show a steady increase as expected", "Yes, 3.1 breaks the pattern"],
    "solutions": [2],
    "calculator": False,
    "input_type": "multiple_choice",
    "hint": "Work out the size of each step up in turn: an anomaly has to break the size of the steps, "
            "not just be the biggest or smallest number.",
    "guided_steps": [
        sayst("On a rising profile, single values tell you nothing on their own. The <strong>steps "
              "between</strong> them are where an anomaly shows."),
        box("How many height readings are listed?", 7,
            "Count them one at a time.",
            done="Seven readings, so six steps between them."),
        box("First step up: 0.8 − 0.2.", 0.6,
            "Subtract the first height from the second.", phase="substitute"),
        box("Fourth step up: 3.1 − 2.3.", 0.8,
            "Subtract the fourth height from the fifth."),
        box("Last step up: 4.5 − 3.8.", 0.7,
            "Subtract the sixth height from the seventh."),
        box("How many of those steps are negative, or several times bigger than the others?", 0,
            "Compare each step with the ones either side of it.",
            done="Every step is a rise of roughly 0.6 to 0.8 m, exactly what a beach climbing towards a "
                 "cliff should do, so nothing breaks the pattern."),
        sayst("No step breaks the pattern, so the honest answer is that there are no anomalies here."),
    ],
    "misconceptions": [
        {"pattern": "lowest_is_anomaly", "expect": 0,
         "message": "The first reading is the one nearest the sea, where a beach is at its lowest. A "
                    "small value that fits the trend is not an anomaly."},
        {"pattern": "highest_is_anomaly", "expect": 1,
         "message": "The last reading is the one nearest the cliff, where a beach is at its highest. "
                    "Check the size of each step before calling a value odd."},
        {"pattern": "middle_value", "expect": 3,
         "message": "Compare the step up into that reading with the steps either side of it before "
                    "deciding it breaks anything."},
    ],
})

bronze.append({
    "display": "Give ONE reason why a larger sample size produces more reliable results in geographical "
               "fieldwork.",
    "options": ["Larger samples reduce the effect of anomalies on the overall results",
                "Larger samples are always cheaper to collect",
                "Larger samples do not require a sampling method",
                "Larger samples guarantee no measurement errors"],
    "solutions": [0],
    "calculator": False,
    "input_type": "multiple_choice",
    "hint": "Test the idea with numbers: work out what one odd reading does to the mean of a small set "
            "compared with a big one.",
    "guided_steps": [
        sayst("Do not argue this one, <strong>test</strong> it. Picture a true value of 5 and one faulty "
              "reading of 25, sitting first in a small sample and then in a large one."),
        box("Small sample of four readings: 5, 5, 5, 25. What is the total?", 40,
            "Add the four readings together.",
            done="One faulty reading is a quarter of this sample."),
        box("Mean of the small sample: 40 ÷ 4.", 10,
            "Divide the total by the number of readings.", phase="substitute",
            done="The true value is 5, so the faulty reading has dragged the mean 5 above the truth."),
        box("Larger sample of twenty: nineteen readings of 5, plus the same faulty 25. "
            "Total = 19 × 5 + 25.", 120,
            "Work out 19 × 5, then add 25."),
        box("Mean of the larger sample: 120 ÷ 20.", 6,
            "Divide the total by the number of readings."),
        box("The true value is 5. By how much is the larger sample's mean out?", 1,
            "Subtract 5 from the mean you just found.",
            done="The same faulty reading shifted the small mean by 5 but the large mean by only 1, so "
                 "extra readings dilute the damage one odd value can do."),
        sayst("That is exactly what reliability means here: choose the option about the effect of "
              "anomalies shrinking."),
    ],
    "misconceptions": [
        {"pattern": "cheaper", "expect": 1,
         "message": "More readings cost more time and money, not less. Think about what extra readings "
                    "do to the influence of one odd value."},
        {"pattern": "no_method", "expect": 2,
         "message": "Size never replaces the need to choose where the points go. A big biased sample is "
                    "still biased."},
        {"pattern": "no_errors", "expect": 3,
         "message": "Extra readings cannot stop a measuring mistake happening. They change how much that "
                    "mistake moves the final figure."},
    ],
})

bronze.append({
    "display": "Pebble roundness scores (1–6) at a beach: 2, 3, 2, 4, 3, 2, 9, 3, 2. The scale only goes "
               "to 6. What can you say about the value 9?",
    "options": ["It is a valid high measurement",
                "It is an anomaly, and likely a recording error since the scale maximum is 6",
                "It shows the beach has very round pebbles",
                "It should be kept because removing data is never appropriate"],
    "solutions": [1],
    "calculator": False,
    "input_type": "multiple_choice",
    "hint": "Check every score against the highest and lowest values the scale is able to produce.",
    "guided_steps": [
        sayst("Some anomalies break the pattern. This kind breaks the <strong>scale</strong>, which is "
              "even stronger evidence. Screen the data against the scale's limits."),
        box("How many scores are listed?", 9,
            "Count them one at a time."),
        box("What is the highest score this roundness scale allows?", 6,
            "The range of the scale is given in the question.",
            done="Nothing above 6 can ever be measured on this scale."),
        box("How many scores in the list sit above that maximum?", 1,
            "Check each score against the limit.", phase="substitute"),
        box("By how much does that score exceed the maximum?", 3,
            "Subtract the scale maximum from the score."),
        box("How many of the nine scores are therefore impossible measurements?", 1,
            "Count the scores that could not physically have been recorded.",
            done="One value could not have come off this scale at all, so it is a recording error rather "
                 "than a real pebble, and that is the honest thing to say about it."),
        sayst("Choose the option that calls it an anomaly caused by a recording error."),
    ],
    "misconceptions": [
        {"pattern": "valid", "expect": 0,
         "message": "A scale that stops at 6 cannot produce a higher score, so this reading cannot be a "
                    "real measurement."},
        {"pattern": "roundest", "expect": 2,
         "message": "A score that is off the scale describes nothing about the pebbles. Check the value "
                    "against the limits of the scale before reading meaning into it."},
        {"pattern": "keep_all", "expect": 3,
         "message": "Data that could not physically have been recorded is different from data you simply "
                    "dislike. Investigate impossible values rather than protecting them."},
    ],
})

bronze.append({
    "display": "A student places quadrats every 2 metres along a transect running from the edge of a "
               "footpath into a field. What is the student investigating?",
    "options": ["How vegetation changes with distance from the path",
                "How soil type affects building materials",
                "How weather changes across the field",
                "How population density affects housing"],
    "solutions": [0],
    "calculator": False,
    "input_type": "multiple_choice",
    "hint": "Work out what a quadrat physically encloses, and what changes from one quadrat to the next.",
    "guided_steps": [
        sayst("Every transect pairs two things: <strong>a distance</strong> and <strong>a "
              "measurement</strong>. Pin both down and the aim of the study names itself."),
        box("How many metres apart are the quadrats?", 2,
            "The spacing is given in the question.",
            done="A fixed 2 m interval, so this is a systematic transect."),
        box("Counting the one at 0 m, how many quadrats sit in the first 10 metres?", 6,
            "Positions run 0, 2, 4 and so on up to 10.", phase="substitute"),
        box("Does a quadrat frame a patch of ground and what is growing in it?" + YN, 1,
            "Picture the equipment: a square frame laid on the ground."),
        box("How many things change from one quadrat to the next: the distance from the path, and what "
            "the frame encloses?", 2,
            "Count the distance and the measurement as one each.",
            done="Each stop pairs a distance from the path with a record of the plants inside the frame, "
                 "which is exactly how trampling near a path is tested."),
        sayst("Choose the option about vegetation changing with distance from the path."),
    ],
    "misconceptions": [
        {"pattern": "weather", "expect": 2,
         "message": "A quadrat frames a patch of ground. It cannot record the weather."},
        {"pattern": "housing", "expect": 3,
         "message": "Nothing here counts people or houses. Check what the equipment physically encloses."},
        {"pattern": "soil_building", "expect": 1,
         "message": "Quadrats are laid on the surface to record what grows there, not to test building "
                    "materials."},
    ],
})

silver = []

silver.append({
    "display": "A town has 4 wards with populations: Ward A = 5,000, Ward B = 10,000, Ward C = 3,000, "
               "Ward D = 2,000. A stratified sample of 100 people is needed. How many people should be "
               "sampled from Ward B?",
    "solutions": [50],
    "calculator": True,
    "input_type": "single_value",
    "hint": "Find the ward's share of the total population first, then take that same share of the sample.",
    "guided_steps": [
        sayst("Stratified sampling is always the same two moves: <strong>share of the population</strong>, "
              "then <strong>that share of the sample</strong>."),
        box("Add the four ward populations. What is the total population of the town?", 20000,
            "5000 + 10000 + 3000 + 2000.",
            done="Every share from here is measured against 20,000."),
        box("Divide Ward B's population by the total to get its share as a decimal.", 0.5,
            "10000 ÷ 20000.", phase="substitute"),
        box("Multiply the sample size by that share: 100 × your decimal.", 50,
            "Take that fraction of the 100 places."),
        box("Now check with Ward A: 100 × (5000 ÷ 20000).", 25,
            "Repeat the same two moves for Ward A.",
            done="Ward A takes 25, Ward C takes 15 and Ward D takes 10. Add those to Ward B's share and "
                 "the four come to exactly 100, so the sample is fully shared out."),
    ],
    "misconceptions": [
        {"pattern": "equal_split", "expect": 25,
         "message": "You have shared the sample out evenly between the four wards. A stratified sample "
                    "gives each ward a share that matches its size."},
        {"pattern": "used_whole_sample", "expect": 100,
         "message": "That is the whole sample handed to one ward. Only Ward B's share of the population "
                    "should be taken."},
    ],
})

silver.append({
    "display": "A student repeats river width measurements 3 times at each site and gets: "
               "Site 1: 3.2, 3.4, 3.3; Site 2: 4.1, 2.8, 4.0; Site 3: 5.5, 5.6, 5.4. "
               "Which site has the least reliable measurements?",
    "options": ["Site 1 (range = 0.2)", "Site 2 (range = 1.3)", "Site 3 (range = 0.2)",
                "All sites are equally reliable"],
    "solutions": [1],
    "calculator": False,
    "input_type": "multiple_choice",
    "hint": "Work out how far apart the repeats are at each site, not how large the measurements are.",
    "guided_steps": [
        sayst("Reliability is about whether repeats <strong>agree with each other</strong>. Measure the "
              "disagreement at each site in turn."),
        box("How many repeat measurements were taken at each site?", 3,
            "The question states how many times each measurement was repeated.",
            done="Three repeats per site, so three ranges to compare."),
        box("Site 1 range: 3.4 − 3.2.", 0.2,
            "Largest repeat minus smallest repeat.", phase="substitute"),
        box("Site 2 range: 4.1 − 2.8.", 1.3,
            "Largest repeat minus smallest repeat."),
        box("Site 3 range: 5.6 − 5.4.", 0.2,
            "Largest repeat minus smallest repeat."),
        box("How many of the three ranges are bigger than 1.0 m?", 1,
            "Compare each range with 1.0.",
            done="One site's repeats disagree by more than a metre while the other two agree to within "
                 "0.2 m, so that site is the one you cannot trust."),
        sayst("Choose the site with the widest spread of repeats."),
    ],
    "misconceptions": [
        {"pattern": "biggest_values", "expect": 2,
         "message": "That site has the largest measurements, but its repeats agree closely. Reliability "
                    "is about how far apart the repeats are, not how large they are."},
        {"pattern": "all_equal", "expect": 3,
         "message": "The three sites do not agree equally. Compare each site's largest repeat with its "
                    "smallest before deciding."},
    ],
})

silver.append({
    "display": "A student wants to compare pedestrian counts in a city centre at different times of day. "
               "They count pedestrians for 5 minutes at 9am, 12pm, 3pm, and 6pm. What type of sampling "
               "is this?",
    "options": ["Random", "Systematic", "Stratified", "Opportunity"],
    "solutions": [1],
    "calculator": False,
    "input_type": "multiple_choice",
    "hint": "Sampling can be spaced out in time as well as across space, so measure the gap between the "
            "counts.",
    "guided_steps": [
        sayst("The points here are spread through <strong>time</strong>, not space, but the same test "
              "applies: measure the gaps."),
        box("How many counting times are used?", 4,
            "They are listed in the question.",
            done="Four counts across the day."),
        box("How many hours pass between 9am and 12pm?", 3,
            "Count forward from 9am.", phase="substitute"),
        box("How many hours pass between 3pm and 6pm?", 3,
            "Count forward from 3pm."),
        box("Is every gap the same length?" + YN, 1,
            "Compare the first gap with the last gap."),
        box("Were the times drawn out of a random number table?" + YN, 0,
            "Ask whether chance chose the times, or a rule did.",
            done="Equal gaps chosen by a rule rather than by chance is what decides the method here."),
        sayst("A fixed, repeating interval names the method: choose the systematic option."),
    ],
    "misconceptions": [
        {"pattern": "random", "expect": 0,
         "message": "Nothing here was left to chance. Look at the size of the gap between one count and "
                    "the next."},
        {"pattern": "stratified", "expect": 2,
         "message": "Stratified sampling shares the sample between named groups such as age bands. No "
                    "groups are set up here."},
    ],
})

silver.append({
    "display": "Traffic count data at a junction: 45, 52, 48, 51, 47, 53, 120, 49, 46. Calculate the mean "
               "with and without the anomaly (120). What is the mean WITHOUT the anomaly? "
               "Round to 1 decimal place.",
    "solutions": [48.9],
    "calculator": True,
    "input_type": "single_value",
    "hint": "Take the odd value out of the total first, then divide by the number of counts you have left.",
    "guided_steps": [
        sayst("Removing an anomaly changes <strong>two</strong> things: the total and the count. Miss "
              "either and the mean comes out wrong."),
        box("How many counts are listed?", 9,
            "Count them one at a time.",
            done="Nine counts before anything is removed."),
        box("Add all nine counts together.", 511,
            "45 + 52 + 48 + 51 + 47 + 53 + 120 + 49 + 46."),
        box("Take the anomaly off the total: 511 − 120.", 391,
            "Subtract the odd value from the total.", phase="substitute"),
        box("How many counts are left?", 8,
            "One count has gone from the original nine."),
        box("Divide: 391 ÷ 8, to 1 decimal place.", 48.9,
            "Corrected total divided by corrected count."),
        box("Check by running it forwards: your mean × 8, to the nearest whole number.", 391,
            "Multiply the mean you found by the number of counts left.",
            done="It returns the corrected total, so the mean is right. Note how far below the raw "
                 "average of 56.8 it sits: one lorry surge was distorting the whole picture."),
    ],
    "misconceptions": [
        {"pattern": "included_anomaly", "expect": 56.8,
         "message": "That is the mean with the odd value still inside the total. The question asks for "
                    "the mean once it has been taken out."},
        {"pattern": "divided_by_9", "expect": 43.4,
         "message": "You removed a value from the total but still divided by the original count. Removing "
                    "a reading changes the count too."},
    ],
})

silver.append({
    "display": "A student surveys 60 households in a village with three land use types: residential (50%), "
               "farmland (30%), commercial (20%). Using stratified sampling, how many households should "
               "be surveyed in the farmland area?",
    "solutions": [18],
    "calculator": True,
    "input_type": "single_value",
    "hint": "Turn the land use percentage into a decimal, then take that share of the households being "
            "surveyed.",
    "guided_steps": [
        sayst("The shares are handed to you as percentages here, so the work is one conversion and one "
              "multiplication, then a check."),
        box("How many households will be surveyed altogether?", 60,
            "The sample size is given in the first sentence."),
        box("What percentage of the village is farmland?", 30,
            "Read the figure next to farmland.",
            done="That percentage is farmland's share of the whole village."),
        box("Turn the percentage into a decimal: 30 ÷ 100.", 0.3,
            "Divide the percentage by 100.", phase="substitute"),
        box("Multiply: 60 × 0.3.", 18,
            "Take that share of the households."),
        box("Now add all three shares: residential (60 × 0.5), commercial (60 × 0.2), and the farmland "
            "share you found. What is the total?", 60,
            "Work out the other two shares, then total all three.",
            done="30 + 12 + your farmland share comes to exactly 60, the whole sample, so the shares are "
                 "correctly proportioned."),
    ],
    "misconceptions": [
        {"pattern": "equal_split", "expect": 20,
         "message": "You have split the households evenly between the three land uses. Each share should "
                    "match that land use's percentage of the village."},
        {"pattern": "gave_percentage", "expect": 30,
         "message": "That is the percentage, not a number of households. Turn it into a share of the "
                    "sample before answering."},
    ],
})

silver.append({
    "display": "A student measures temperature at the same location every day for a month. What type of "
               "variable is 'temperature'?",
    "options": ["Categorical (qualitative)", "Continuous (quantitative)", "Discrete (quantitative)",
                "Ordinal"],
    "solutions": [1],
    "calculator": False,
    "input_type": "multiple_choice",
    "hint": "Ask whether a reading can sit between two whole numbers, or whether it can only land on "
            "whole steps.",
    "guided_steps": [
        sayst("Classify data by asking what values are <strong>possible</strong>, not what values you "
              "happen to have written down."),
        box("Across a 30 day month, how many readings are collected?", 30,
            "One reading per day for a month of 30 days.",
            done="Thirty numbers, all on the same scale."),
        box("Is temperature recorded as a number on a scale rather than as a named category?" + YN, 1,
            "Ask whether the reading is a word or a figure.", phase="substitute"),
        box("Between 15°C and 16°C, could a thermometer show a value such as 15.4°C?" + YN, 1,
            "Think about what a finer thermometer would show."),
        box("Can temperature only ever land on whole numbers, the way a count of cars must?" + YN, 0,
            "Compare temperature with something you count in whole units.",
            done="A number that can take any value between two points is measured, not counted, and that "
                 "is the deciding test."),
        sayst("Measured on a scale with values possible in between: choose the continuous option."),
    ],
    "misconceptions": [
        {"pattern": "discrete", "expect": 2,
         "message": "Discrete data comes in whole steps you can count, like the number of cars. Ask "
                    "whether a value can sit between two whole numbers here."},
        {"pattern": "categorical", "expect": 0,
         "message": "Categorical data sorts things into named groups rather than placing them on a "
                    "number scale."},
        {"pattern": "ordinal", "expect": 3,
         "message": "Ordinal data is a rank order such as 1st, 2nd, 3rd, where the gaps need not be "
                    "equal. Ask whether the gaps on this scale are equal."},
    ],
})

silver.append({
    "display": "A fieldwork group collects 50 pebble measurements on a beach. They want to check if beach "
               "material gets rounder with distance from the cliff. They measure roundness on a scale of "
               "1 (angular) to 6 (well-rounded). A student suggests finding the mean roundness at each "
               "sampling point. Why might the median be better than the mean here?",
    "options": ["The median is faster to calculate",
                "The data is on an ordinal scale (ranked categories), so the mean may not be meaningful",
                "The median always gives a higher number",
                "The mean cannot be calculated from integers"],
    "solutions": [1],
    "calculator": False,
    "input_type": "multiple_choice",
    "hint": "Ask whether the gap between score 1 and score 2 is definitely the same size as the gap "
            "between score 5 and score 6.",
    "guided_steps": [
        sayst("Roundness scores are <strong>ranks</strong>, not lengths. Test what an average does to "
              "ranks on a small set."),
        box("How many pebbles are measured altogether?", 50,
            "The sample size is in the first sentence."),
        box("How many different scores can a single pebble be given on this scale?", 6,
            "The scale runs from 1 to 6.",
            done="Six named categories, ranked from angular to well rounded."),
        box("Take five pebbles scoring 2, 2, 3, 6, 6. What is their mean?", 3.8,
            "Add the five scores, then divide by 5.", phase="substitute"),
        box("How many of those five pebbles were actually given a score of 4?", 0,
            "Look back at the five scores.",
            done="The mean has landed between two named categories, describing a pebble nobody measured."),
        box("Put the five scores in order and type the middle one.", 3,
            "Sort them, then take the value in the centre.",
            done="The middle value is always a real score off the scale, which is why it survives ranked "
                 "data better when the gaps between ranks may not be equal."),
        sayst("Choose the option about the scale being ordinal."),
    ],
    "misconceptions": [
        {"pattern": "faster", "expect": 0,
         "message": "Speed is not the reason, and sorting 50 values is not quick. Think about whether "
                    "the gaps between ranks on this scale are equal."},
        {"pattern": "always_higher", "expect": 2,
         "message": "The middle value can be smaller, larger or the same as the average. The issue is "
                    "the type of scale being used."},
        {"pattern": "integers", "expect": 3,
         "message": "Averages can be worked out from whole numbers without difficulty. The question is "
                    "what the numbers on this scale actually stand for."},
    ],
})

gold = []

gold.append({
    "display": "A study area is divided into 200 grid squares. A student uses a random number table and "
               "gets these numbers: 7, 156, 203, 42, 89, 301, 12, 178. How many of these are valid grid "
               "square selections?",
    "solutions": [6],
    "calculator": False,
    "input_type": "single_value",
    "hint": "Reject any number that falls outside the numbering of the grid squares, then count what is "
            "left.",
    "guided_steps": [
        sayst("A random number table does not know how big your study area is. Every number it gives you "
              "has to be <strong>screened</strong> against the numbering first."),
        box("How many numbers did the table produce?", 8,
            "Count the numbers in the list."),
        box("What is the highest grid square number that exists in this study area?", 200,
            "The study area is divided into a stated number of squares.",
            done="Anything above that number points at a square that is not there."),
        box("How many of the eight numbers are bigger than that maximum?", 2,
            "Check each number against the limit.", phase="substitute"),
        box("Take those off the list: 8 − your count of rejects.", 6,
            "Subtract the rejected numbers from the total produced."),
        box("Add the valid and rejected counts back together.", 8,
            "Your valid count plus your reject count.",
            done="They rebuild the original eight numbers, so nothing has been double counted or lost. "
                 "In real fieldwork the student would draw replacements for the rejected numbers."),
    ],
    "misconceptions": [
        {"pattern": "all_valid", "expect": 8,
         "message": "You have counted every number the table produced. Numbers pointing outside the study "
                    "area cannot be used."},
        {"pattern": "one_missed", "expect": 7,
         "message": "One number over the limit has slipped through. Check every value against the "
                    "maximum, not just the largest one."},
    ],
})

gold.append({
    "display": "A river study collects velocity data at 15 sites. The mean velocity is 1.2 m/s. One "
               "reading of 8.5 m/s is identified as an anomaly (equipment malfunction). What is the "
               "corrected mean if this reading is removed? Give to 2 decimal places.",
    "solutions": [0.68],
    "calculator": True,
    "input_type": "single_value",
    "hint": "Turn the mean back into a total first, then remove the faulty reading and divide by the "
            "readings you have left.",
    "guided_steps": [
        sayst("You never see the 15 readings, only their mean. Run the mean <strong>backwards</strong> "
              "into a total, edit the total, then run it forwards again."),
        box("How many sites were sampled before anything was removed?", 15,
            "The number of sites is given in the question."),
        box("Total of all readings = mean × number of sites: 1.2 × 15.", 18,
            "Multiply the mean by the count.",
            done="The 15 readings add up to 18.0 m/s in total."),
        box("Take the faulty reading off the total: 18 − 8.5.", 9.5,
            "Subtract the anomaly from the total, not from the mean.", phase="substitute"),
        box("How many readings are left?", 14,
            "One reading has gone from the original count."),
        box("Corrected mean: 9.5 ÷ 14, to 2 decimal places.", 0.68,
            "Divide the corrected total by the corrected count."),
        box("Check by running it forwards: your mean × 14, to 1 decimal place.", 9.5,
            "Multiply the mean you found by the readings that are left.",
            done="It returns the corrected total, so the mean is right. A single faulty reading had been "
                 "holding the average of this river almost twice as high as it should be."),
    ],
    "misconceptions": [
        {"pattern": "divided_by_15", "expect": 0.63,
         "message": "You corrected the total but divided by the original count. Removing a reading "
                    "changes the count as well."},
        {"pattern": "forgot_to_remove", "expect": 1.29,
         "message": "You reduced the count but left the faulty reading inside the total. Both have to "
                    "change together."},
    ],
})

gold.append({
    "display": "A student needs to survey 80 people in a town. The town has: young adults (18–30) = 25%, "
               "middle-aged (31–55) = 45%, elderly (56+) = 30%. Using stratified sampling, how many "
               "middle-aged people should be surveyed?",
    "solutions": [36],
    "calculator": True,
    "input_type": "single_value",
    "hint": "Turn the age group's percentage into a decimal, then take that share of the people being "
            "surveyed.",
    "guided_steps": [
        sayst("Three age bands, three shares. Take care to read the share belonging to the band the "
              "question actually asks about."),
        box("How many people will be surveyed altogether?", 80,
            "The sample size is in the first sentence."),
        box("What percentage of the town is middle-aged?", 45,
            "Read the figure next to the 31 to 55 band.",
            done="That band is the largest slice of the town, so it should take the largest slice of the "
                 "sample."),
        box("Turn the percentage into a decimal: 45 ÷ 100.", 0.45,
            "Divide the percentage by 100.", phase="substitute"),
        box("Multiply: 80 × 0.45.", 36,
            "Take that share of the 80 people."),
        box("Work out the other two shares (25% and 30% of 80) and add all three together.", 80,
            "20 and 24, plus the share you found.",
            done="The three shares come to exactly 80, the full sample, so no band has been over or "
                 "under represented."),
    ],
    "misconceptions": [
        {"pattern": "gave_percentage", "expect": 45,
         "message": "That is the percentage, not a number of people. Turn it into a share of the sample "
                    "before answering."},
        {"pattern": "wrong_band_young", "expect": 20,
         "message": "That is the share belonging to the youngest band. Check which age group the "
                    "question asks about."},
        {"pattern": "wrong_band_elderly", "expect": 24,
         "message": "That is the share belonging to the oldest band. Check which age group the question "
                    "asks about."},
    ],
})

gold.append({
    "display": "A student collects environmental quality data and calculates the mean score for 5 sites: "
               "14, 12, 16, 13, 15. She wants to check reliability by calculating the range as a "
               "percentage of the mean. What is this percentage? Round to 1 decimal place.",
    "solutions": [28.6],
    "calculator": True,
    "input_type": "single_value",
    "hint": "Work out the range and the mean separately, then divide the range by the mean and multiply "
            "by 100.",
    "guided_steps": [
        sayst("A range on its own says nothing: 4 points of spread is huge on a small score and tiny on "
              "a large one. Measuring it <strong>against the mean</strong> is what makes it useful."),
        box("How many sites were scored?", 5,
            "Count the scores in the list."),
        box("Add the five scores together.", 70,
            "14 + 12 + 16 + 13 + 15.",
            done="That total is what the mean is built from."),
        box("Mean: 70 ÷ 5.", 14,
            "Divide the total by the number of sites.", phase="substitute"),
        box("Range: largest score minus smallest score.", 4,
            "16 − 12."),
        box("Divide the range by the mean: 4 ÷ 14, to 4 decimal places.", 0.2857,
            "Range divided by mean, kept to 4 decimal places."),
        box("Multiply by 100 and round to 1 decimal place.", 28.6,
            "Move the decimal point two places, then round."),
        box("Check: take your percentage of the mean, 0.286 × 14, to the nearest whole number.", 4,
            "Turn your percentage back into a decimal and apply it to the mean.",
            done="It returns the range you started from, so the percentage is right. Under about 30% of "
                 "the mean, these five sites are reasonably consistent."),
    ],
    "misconceptions": [
        {"pattern": "mean_over_range", "expect": 350,
         "message": "You have divided the mean by the range. The question asks what fraction of the mean "
                    "the range makes up, so the range goes on top."},
        {"pattern": "range_only", "expect": 4,
         "message": "That is the range itself, not the range expressed as a percentage of the mean."},
    ],
})

gold.append({
    "display": "Explain why random sampling might be impractical for a river study measuring velocity at "
               "different points along a 5 km river course, even though it reduces bias.",
    "options": ["Random points might all cluster in one section, leaving long stretches unmeasured, so "
                "the downstream trend the study aims to show is missed",
                "Random sampling is always impractical",
                "The river is too short for random sampling",
                "Random sampling requires more than 100 sample points"],
    "solutions": [0],
    "calculator": False,
    "input_type": "multiple_choice",
    "hint": "Think about what chance can do to the spread of points when the whole aim is to show change "
            "along a line.",
    "guided_skip_reason": "Evaluative judgement about the fit between a sampling method and a study aim. "
                          "There is no numeric procedure that reaches the option, so a numeric walk "
                          "would be fake.",
    "misconceptions": [
        {"pattern": "always_impractical", "expect": 1,
         "message": "Random sampling works well in plenty of studies. The difficulty here is specific to "
                    "needing even coverage along a line."},
        {"pattern": "too_short", "expect": 2,
         "message": "5 km gives plenty of room for sampling. Think about where chance might place the "
                    "points along it."},
        {"pattern": "needs_100", "expect": 3,
         "message": "There is no minimum number of points for random sampling. Think about the spread of "
                    "the points instead."},
    ],
})

pd["problem_bank"] = {
    "bronze": bronze,
    "silver": silver,
    "gold": gold,
    "bronze_description": "Name the sampling method from how the points were chosen, and pick out a "
                          "reading that breaks the pattern or breaks the scale.",
    "silver_description": "Work out proportional shares for a stratified sample, and use the spread of "
                          "repeated readings to judge reliability.",
    "gold_description": "Run a mean backwards into a total to correct it, screen data against the limits "
                        "of the study, and judge how well a method fits the aim.",
}

out = os.path.join(HERE, "lesson_L10.json")
json.dump(pd, io.open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", out)
