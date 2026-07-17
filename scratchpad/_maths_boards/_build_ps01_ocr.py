# -*- coding: utf-8 -*-
"""Full guided-learning + diagrams build for probability-statistics-L01 (maths-ocr).
Starts from the LIVE practice_data (preserving worked_examples, related_videos,
topic_links) and adds method_card trim, tier_guides, guided (opener+teach),
per-problem hints/misconceptions(expect)/guided_steps, tier descriptions, and
inline SVG figures. Numbers verified independently by fresh-solve."""
import io, json
import _svglib_ps01 as S

live = json.load(io.open("_ps01_live.json", encoding="utf-8"))
pd = json.loads(json.dumps(live))  # deep copy, preserves worked_examples etc.

# ---- figures (inline SVG prepended to display) ----
BAG = S.bag(1, 3, "A bag holding 1 red and 3 blue balls")
FIG = {
    "s2": S.tree2(8, 'R', 5, 'B', 3, False, {'RR'}, "Tree diagram, with replacement, 5 red and 3 blue, both-red path highlighted"),
    "s3": S.tree2(8, 'R', 5, 'B', 3, True, {'RR'}, "Tree diagram, without replacement, 5 red and 3 blue, both-red path highlighted"),
    "s5": S.dice_grid("Sample space grid of two dice, the six cells totalling 7 highlighted"),
    "s7": S.tree2(10, 'R', 6, 'B', 4, True, {'RB', 'BR'}, "Tree diagram, without replacement, 6 red and 4 blue, both one-of-each paths highlighted"),
    "g1": S.tree3_redspine(12, 8, 4, "Three-stage tree, without replacement, all-red spine 8/12, 7/11, 6/10 highlighted"),
    "g5": S.tree2(12, 'R', 7, 'B', 5, True, {'BB'}, "Tree diagram, without replacement, 7 red and 5 blue, both-blue path highlighted"),
}
TS_TREE = S.tree2(10, 'R', 4, 'B', 6, True, {'RR'}, "Tree diagram, without replacement, 4 red and 6 blue, both-red path highlighted")
TG_TREE = S.tree2(9, 'R', 5, 'B', 4, True, {'RB', 'BR'}, "Tree diagram, without replacement, 5 red and 4 blue, one-of-each paths highlighted")

def box(pre, answer, hint, post="", say=None, done=None, phase=None):
    d = {"pre": pre, "post": post, "answer": answer, "hint": hint}
    if say is not None: d["say"] = say
    if done is not None: d["done"] = done
    if phase is not None: d["phase"] = phase
    return d

def sayonly(say):
    return {"say": say}

def mc(pattern, expect, message):
    return {"pattern": pattern, "check": pattern, "expect": expect, "message": message}

# =================== METHOD CARD (slim) ===================
pd["method_card"] = {
    "title": "Probability Basics & Tree Diagrams",
    "steps": [
        "P(event) = favourable ÷ total, always between 0 and 1",
        "P(not A) = 1 − P(A)",
        "AND: multiply along branches. OR: add the separate paths",
        "Without replacement: drop the total (and the colour taken) by 1 each draw",
    ],
    "content": "<p><strong>Probability</strong> = favourable outcomes ÷ total outcomes, always between 0 and 1. <strong>AND</strong> means multiply along branches. <strong>OR</strong> means add the probabilities of separate paths.</p><p>On a <strong>tree diagram</strong> each branch shows its probability, and branches from one point sum to 1. <strong>With replacement</strong>: probabilities stay the same. <strong>Without replacement</strong>: the denominator drops by 1.</p>",
    "example": "<p><strong>Bag: 3 red, 7 blue. Find P(red).</strong></p><p>P(red) = 3 ÷ 10 = 3/10.</p>",
}

# =================== TIER DESCRIPTIONS ===================
pb = pd["problem_bank"]
pb["bronze_description"] = "Single events: count the favourable outcomes over the total, then simplify"
pb["silver_description"] = "Two events combined: multiply along tree branches, or add separate paths"
pb["gold_description"] = "Several stages or combined outcomes: chain the products, then add and simplify"

# =================== TIER GUIDES ===================
pd["tier_guides"] = {
    "bronze": {
        "title": "Bronze: one event, count and simplify",
        "steps": [
            "Probability is <strong>favourable ÷ total</strong>: the ways you want over the ways altogether. Every answer sits between 0 and 1.",
            "Count the favourable outcomes and the total, then write the fraction. For 'not' or 'at least', use \\(P(A') = 1 - P(A)\\).",
            "Simplify by dividing top and bottom by their highest common factor. For a decimal, divide top by bottom.",
        ],
        "example": {
            "question": "A bag has 4 red and 6 blue. Find P(red).",
            "steps": [
                {"label": "Count", "content": "<p>Red = 4, total = 4 + 6 = 10.</p>"},
                {"label": "Fraction", "content": "<p>P(red) = 4/10.</p>"},
                {"label": "Simplify", "content": "<p>Divide by 2: 4/10 = 2/5.</p>"},
                {"label": "Answer", "content": "<p>P(red) = 2/5</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "silver": {
        "title": "Silver: two events, multiply along branches",
        "steps": [
            "A two-stage event uses a <strong>tree</strong>. Each branch carries its probability, and branches from one point add to 1.",
            "<strong>AND</strong> (this then that): multiply along a path. Two separate paths (an <strong>OR</strong>): add them.",
            "<strong>With replacement</strong>, probabilities stay the same. <strong>Without replacement</strong>, the total drops by 1 and the colour taken drops by 1.",
        ],
        "example": {
            "question": "A bag has 5 red, 3 blue. Two drawn without replacement. Find P(both red).",
            "steps": [
                {"label": "Set up", "content": "<p>First red = 5/8. Second red = 4/7 (one red gone).</p>"},
                {"label": "Multiply", "content": "<p>5/8 × 4/7 = 20/56</p>"},
                {"label": "Simplify", "content": "<p>Divide by 4: 20/56 = 5/14.</p>"},
                {"label": "Answer", "content": "<p>P(both red) = 5/14</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
    "gold": {
        "title": "Gold: several stages and combined paths",
        "steps": [
            "Longer problems chain more branches: three draws multiply three probabilities, dropping the total each time when there is no replacement.",
            "'At least one' is quickest as \\(1 - P(\\text{none})\\). 'One of each' or 'exactly two' means adding every path that fits.",
            "Work each path as a product, then add the paths you want and simplify.",
        ],
        "example": {
            "question": "A bag has 8 red, 4 blue. Three drawn without replacement. Find P(all red).",
            "steps": [
                {"label": "Chain", "content": "<p>8/12 × 7/11 × 6/10</p>"},
                {"label": "Multiply", "content": "<p>= 336/1320</p>"},
                {"label": "Simplify", "content": "<p>Divide by 24: 336/1320 = 14/55.</p>"},
                {"label": "Answer", "content": "<p>P(all red) = 14/55</p>", "isAnswer": True, "is_answer": True},
            ],
        },
    },
}

# =================== GUIDED: OPENER + TEACH ===================
pd["guided"] = {
    "opener": {
        "label": "Before any formula",
        "display": BAG + "<div style=\"margin-top:6px\">A bag holds <strong>1 red</strong> sweet and <strong>3 blue</strong> sweets. You reach in without looking and grab one.</div>",
        "steps": [
            box("How many sweets are in the bag altogether? ", 4,
                "Count them all: the red one and the blue ones.",
                say="Just look at the bag and count."),
            box("How many of them are red? ", 1,
                "Only the red sweet counts.",
                say="Now count only the ones you want."),
            sayonly("So on average 1 grab in every 4 comes out red. That fraction, 1 over 4, IS the probability. <strong>P(red) = favourable ÷ total = 1/4</strong>. Every probability is just what you want divided by everything there is."),
        ],
    },
    "teach": {
        "bronze": {
            "label": "Together: your first one",
            "display": "A bag has 4 red and 6 blue. Find P(red).",
            "steps": [
                box("Red balls (favourable): ", 4, "There are 4 red.", say="Probability is favourable ÷ total. Count the red first."),
                box("Total balls, 4 + 6 = ", 10, "Add red and blue."),
                box("So P(red) = 4/10. Divide top and bottom by 2. Top, 4 ÷ 2 = ", 2, "4 ÷ 2.", say="Now simplify."),
                box("Bottom, 10 ÷ 2 = ", 5, "10 ÷ 2.", done="P(red) = 2/5. Favourable over total, then simplify. That is the whole move."),
            ],
        },
        "silver": {
            "label": "Together: two draws",
            "display": TS_TREE + "<div style=\"margin-top:6px\">A bag has 4 red and 6 blue. Two drawn WITHOUT replacement. Find P(both red).</div>",
            "steps": [
                box("P(first red), top number: ", 4, "4 red out of 10.", say="First draw: 4 red out of 10 balls."),
                box("P(second red), top number (red now left): ", 3, "4 − 1 = 3 red remain.", say="One red is gone and kept out, so 3 red remain and 9 balls in total."),
                box("Multiply the branches: (4/10) × (3/9). New top, 4 × 3 = ", 12, "Multiply the numerators."),
                box("New bottom, 10 × 9 = ", 90, "Multiply the denominators."),
                box("Simplify 12/90 by dividing by 6. Top, 12 ÷ 6 = ", 2, "12 ÷ 6.", say="Now simplify."),
                box("Bottom, 90 ÷ 6 = ", 15, "90 ÷ 6.", done="P(both red) = 2/15. The new move: the second denominator drops to 9. That is the whole point."),
            ],
        },
        "gold": {
            "label": "Together: one of each",
            "display": TG_TREE + "<div style=\"margin-top:6px\">A bag has 5 red and 4 blue. Two drawn without replacement. Find P(one of each colour).</div>",
            "steps": [
                box("Red then blue: top is 5 × 4 = ", 20, "5 red, then 4 blue.", say="'One of each' has two paths. Total balls = 9. Start with red then blue."),
                box("Its bottom, 9 × 8 = ", 72, "9 balls then 8 balls."),
                box("Blue then red gives (4/9) × (5/8) = 20/72 too. Its top, 4 × 5 = ", 20, "4 blue, then 5 red."),
                box("Add the two paths: 20/72 + 20/72. Top, 20 + 20 = ", 40, "Add the numerators, keep 72.", say="Now add both orders."),
                box("Simplify 40/72 by dividing by 8. Top, 40 ÷ 8 = ", 5, "40 ÷ 8."),
                box("Bottom, 72 ÷ 8 = ", 9, "72 ÷ 8.", done="P(one of each) = 5/9. The new move: add both orders. That is the whole point."),
            ],
        },
    },
}

# =================== PER-PROBLEM: hints, misconceptions, guided_steps ===================
def simplify_check_frac(a_top, a_bot, s_top, s_bot):
    """cross-multiply check step: s_top × a_bot vs s_bot × a_top."""
    return box("%d × %d = " % (s_top, a_bot), s_top * a_bot,
               "Multiply the top of one fraction by the bottom of the other.",
               say="Check the two fractions are equal by cross-multiplying:",
               done="and %d × %d = %d too, so %d/%d = %d/%d. Correct." % (
                   s_bot, a_top, s_bot * a_top, s_top, s_bot, a_top, a_bot))

BRONZE = [
    {"hint": "Count the red balls, then divide by the total number of balls.",
     "mis": [mc("over_wrong_group", [1, 4], "P(red) is red ÷ total, not red ÷ blue. There are 2 + 8 = 10 balls, so P(red) = 2/10 = 1/5. Using 2/8 compares red to blue only.")],
     "gs": [
        box("Red balls (favourable): ", 2, "There are 2 red.", say="Probability is what you want ÷ everything there is. Count the red first."),
        box("Total balls, 2 + 8 = ", 10, "Add red and blue."),
        box("So P(red) = 2/10. Divide top and bottom by 2. Top, 2 ÷ 2 = ", 1, "2 ÷ 2.", say="Now simplify.", phase="substitute"),
        box("Bottom, 10 ÷ 2 = ", 5, "10 ÷ 2.", done="P(red) = 1/5."),
        simplify_check_frac(2, 10, 1, 5),
     ]},
    {"hint": "How many of the six faces are even, out of 6?",
     "mis": [mc("missed_outcome", [1, 3], "6 is even too. The even faces are 2, 4 and 6, that is 3 out of 6, so P(even) = 3/6 = 1/2. Counting only 2 and 4 gives 2/6 = 1/3.")],
     "gs": [
        box("How many faces are even (2, 4, 6)? ", 3, "Count 2, 4 and 6.", say="List the even faces on a fair die."),
        box("How many faces in total? ", 6, "A die has 6 faces."),
        box("So P(even) = 3/6. Divide top and bottom by 3. Top, 3 ÷ 3 = ", 1, "3 ÷ 3.", say="Now simplify.", phase="substitute"),
        box("Bottom, 6 ÷ 3 = ", 2, "6 ÷ 3.", done="P(even) = 1/2."),
        simplify_check_frac(3, 6, 1, 2),
     ]},
    {"hint": "There are 13 hearts in a deck of 52 cards.",
     "mis": [],
     "gs": [
        box("How many hearts are in the deck? ", 13, "One full suit is 13 cards.", say="A standard deck has four suits of 13 cards each."),
        box("How many cards in total? ", 52, "52 cards in a deck."),
        box("So P(heart) = 13/52. Divide top and bottom by 13. Top, 13 ÷ 13 = ", 1, "13 ÷ 13.", say="Now simplify.", phase="substitute"),
        box("Bottom, 52 ÷ 13 = ", 4, "52 ÷ 13.", done="P(heart) = 1/4."),
        simplify_check_frac(13, 52, 1, 4),
     ]},
    {"hint": "Everything adds to 1, so subtract P(rain) from 1.",
     "mis": [mc("gave_complement", 0.3, "0.3 is P(rain). The question asks for P(no rain), which is 1 − 0.3 = 0.7.")],
     "gs": [
        box("P(rain) = ", 0.3, "It is given as 0.3.", say="Rain or no rain covers everything, so the two add up to 1."),
        box("P(no rain) is what is left to reach 1. 1 − 0.3 = ", 0.7, "Take 0.3 away from 1.", phase="substitute", done="P(no rain) = 0.7."),
        box("Check the two total 1: 0.3 + 0.7 = ", 1, "Add both probabilities.", say="Check:", done="They add to 1, so 0.7 is right."),
     ]},
    {"hint": "Blue balls divided by the total number of balls.",
     "mis": [mc("over_wrong_group", [3, 5], "P(blue) is blue ÷ total, not blue ÷ red. There are 5 + 3 = 8 balls, so P(blue) = 3/8. Using 3/5 compares blue to red only.")],
     "gs": [
        box("Blue balls (favourable): ", 3, "There are 3 blue.", say="Count the blue balls, then the total."),
        box("Total balls, 5 + 3 = ", 8, "Add red and blue."),
        box("P(blue) = 3/8. The red balls are the rest. Red balls: ", 5, "Number of red balls.", say="3 and 8 share no common factor, so 3/8 is already simplest.", phase="substitute"),
        box("Check both colours cover everything: blue top 3 + red 5 = ", 8, "Add the two counts.", done="3 + 5 = 8 = the total, so P(blue) = 3/8 is right."),
     ]},
    {"hint": "Which sections are 3 or higher? Count them out of 5.",
     "mis": [mc("excluded_boundary", [2, 5], "'3 or higher' includes the 3. The sections are 3, 4 and 5, that is 3 out of 5. Leaving out the 3 gives 2/5 by mistake.")],
     "gs": [
        box("How many sections are 3, 4 or 5? ", 3, "Count 3, 4 and 5.", say="'3 or higher' includes the 3 itself."),
        box("How many sections in total? ", 5, "Sections 1 to 5."),
        box("So P(3 or higher) = 3/5. Sections below 3 are 1 and 2. How many is that? ", 2, "Count 1 and 2.", say="3 and 5 share no factor, so 3/5 is already simplest.", phase="substitute"),
        box("Check: favourable 3 + below-3 count = ", 5, "Add the two counts.", done="3 + 2 = 5 = total, so P(3 or higher) = 3/5 is right."),
     ]},
    {"hint": "Not green means red or blue: count those out of the total.",
     "mis": [mc("gave_complement", [1, 5], "That is P(green). 'Not green' is the other 8 balls: P(not green) = 8/10 = 4/5. P(green) = 2/10 = 1/5 is the opposite.")],
     "gs": [
        box("Total balls, 4 + 4 + 2 = ", 10, "Add all three colours.", say="'Not green' means everything except green. Find the total first."),
        box("Green balls: ", 2, "There are 2 green."),
        box("Not green = total − green. 10 − 2 = ", 8, "Take the green away from the total.", phase="substitute"),
        box("So P(not green) = 8/10. Divide top and bottom by 2. Top, 8 ÷ 2 = ", 4, "8 ÷ 2."),
        box("Bottom, 10 ÷ 2 = ", 5, "10 ÷ 2.", done="P(not green) = 4/5."),
     ]},
    {"hint": "Less than 3 means 1 and 2 only, out of 6 faces.",
     "mis": [mc("included_boundary", [1, 2], "'Less than 3' does not include 3 itself. Only 1 and 2 count, giving 2/6 = 1/3. Including the 3 gives 3/6 = 1/2.")],
     "gs": [
        box("How many faces are less than 3 (just 1 and 2)? ", 2, "Count 1 and 2.", say="'Less than 3' means below 3, so 3 is not included."),
        box("How many faces in total? ", 6, "A die has 6 faces."),
        box("So P(less than 3) = 2/6. Divide top and bottom by 2. Top, 2 ÷ 2 = ", 1, "2 ÷ 2.", say="Now simplify.", phase="substitute"),
        box("Bottom, 6 ÷ 2 = ", 3, "6 ÷ 2.", done="P(less than 3) = 1/3."),
        simplify_check_frac(2, 6, 1, 3),
     ]},
]

SILVER = [
    {"hint": "List all four outcomes of two tosses, then count those with exactly one head.",
     "mis": [mc("one_order_only", [1, 4], "Exactly one head happens two ways, HT and TH, not one. That is 2 out of 4 = 1/2. Counting a single order gives 1/4.")],
     "gs": [
        box("How many outcomes are there in total? ", 4, "Two tosses, 2 × 2 outcomes.", say="Two tosses give four equally likely outcomes: HH, HT, TH, TT."),
        box("How many have exactly one head (HT and TH)? ", 2, "Count HT and TH.", say="'Exactly one head' means one H and one T, in either order."),
        box("So P = 2/4. Divide top and bottom by 2. Top, 2 ÷ 2 = ", 1, "2 ÷ 2.", say="Now simplify.", phase="substitute"),
        box("Bottom, 4 ÷ 2 = ", 2, "4 ÷ 2.", done="P(exactly one head) = 1/2."),
        simplify_check_frac(2, 4, 1, 2),
     ]},
    {"fig": "s2",
     "hint": "With replacement the bag is unchanged, so multiply 5/8 by 5/8.",
     "mis": [
        mc("used_without_replacement", [5, 14], "This is WITH replacement, so the ball returns and the second draw is still 5/8, not 4/7. Multiplying 5/8 × 5/8 = 25/64. Using 4/7 (without replacement) gives 5/14."),
        mc("single_draw_only", [5, 8], "P(both red) needs both draws multiplied: 5/8 for the first AND 5/8 for the second. 5/8 alone is just the first draw."),
     ],
     "gs": [
        box("P(red) on the first draw, top number: ", 5, "5 red out of 8.", say="With replacement the ball goes back, so both draws face the same 8 balls."),
        box("P(red) on the second draw is the same, top number: ", 5, "Still 5 red out of 8."),
        box("Multiply along the branches: (5/8) × (5/8). New top, 5 × 5 = ", 25, "Multiply the numerators.", say="Tops multiply, bottoms multiply.", phase="substitute"),
        box("New bottom, 8 × 8 = ", 64, "Multiply the denominators.", done="P(both red) = 25/64."),
        box("Check the first-draw branches cover the bag: red 5 + blue 3 = ", 8, "Add the two counts.", say="Check:", done="5 + 3 = 8 = the denominator, so the tree is set up right and 25/64 stands."),
     ]},
    {"fig": "s3",
     "hint": "After one red is taken, 4 red remain out of 7. Multiply 5/8 by 4/7.",
     "mis": [mc("used_with_replacement", [25, 64], "Without replacement the first red is not returned, so the second draw is 4/7, not 5/8. That gives 5/8 × 4/7 = 5/14. Using 5/8 twice (with replacement) gives 25/64.")],
     "gs": [
        box("P(first red), top number: ", 5, "5 red out of 8.", say="First draw: 5 red out of 8."),
        box("P(second red), top number (red now left): ", 4, "5 − 1 = 4 red remain.", say="One red is gone and kept out, so 4 red remain and 7 balls in total."),
        box("Multiply the branches: (5/8) × (4/7). New top, 5 × 4 = ", 20, "Multiply the numerators.", phase="substitute"),
        box("New bottom, 8 × 7 = ", 56, "Multiply the denominators."),
        box("Simplify 20/56 by dividing by 4. Top, 20 ÷ 4 = ", 5, "20 ÷ 4.", say="Now simplify."),
        box("Bottom, 56 ÷ 4 = ", 14, "56 ÷ 4.", done="P(both red) = 5/14."),
     ]},
    {"hint": "Independent 'and' means multiply the two probabilities.",
     "mis": [mc("added_not_multiplied", 0.7, "'And' for independent events multiplies, it does not add. 0.4 × 0.3 = 0.12. Adding gives 0.7, which is bigger than each part, so cannot be an 'and'.")],
     "gs": [
        box("P(A) = ", 0.4, "Given as 0.4.", say="Independent events do not affect each other, so 'A and B' multiplies."),
        box("P(B) = ", 0.3, "Given as 0.3."),
        box("Multiply them. 0.4 × 0.3 = ", 0.12, "4 × 3 = 12, then two decimal places.", phase="substitute", done="P(A and B) = 0.12."),
        box("Check the other way (it must match): 0.3 × 0.4 = ", 0.12, "Same numbers, same answer.", say="Check:", done="Same both ways, so 0.12 is right."),
     ]},
    {"fig": "s5",
     "hint": "There are 36 equally likely pairs; count how many add to 7.",
     "mis": [mc("unordered_count", [1, 12], "Order matters here: (1,6) and (6,1) are different rolls. There are 6 ordered pairs totalling 7, so P = 6/36 = 1/6. Counting 3 unordered pairs gives 1/12.")],
     "gs": [
        box("Total number of outcomes, 6 × 6 = ", 36, "6 faces times 6 faces.", say="Two dice give 6 × 6 outcomes. The grid shows them all."),
        box("How many pairs total 7 (the highlighted diagonal)? ", 6, "Count (1,6)(2,5)(3,4)(4,3)(5,2)(6,1).", say="Now count the pairs that add to 7."),
        box("So P = 6/36. Divide top and bottom by 6. Top, 6 ÷ 6 = ", 1, "6 ÷ 6.", say="Now simplify.", phase="substitute"),
        box("Bottom, 36 ÷ 6 = ", 6, "36 ÷ 6.", done="P(total 7) = 1/6."),
        simplify_check_frac(6, 36, 1, 6),
     ]},
    {"hint": "Subtract P(A) from 1.",
     "mis": [mc("gave_event", 0.6, "0.6 is P(A) itself. P(not A) = 1 − 0.6 = 0.4.")],
     "gs": [
        box("P(A) = ", 0.6, "Given as 0.6.", say="An event and its opposite always add to 1."),
        box("P(not A) is what is left to reach 1. 1 − 0.6 = ", 0.4, "Take 0.6 from 1.", phase="substitute", done="P(not A) = 0.4."),
        box("Check they total 1: 0.6 + 0.4 = ", 1, "Add both.", say="Check:", done="They add to 1, so 0.4 is right."),
     ]},
    {"fig": "s7",
     "hint": "One of each can be red-then-blue or blue-then-red: work out both and add.",
     "mis": [mc("one_path_only", [4, 15], "One of each can happen two ways, red then blue AND blue then red. Adding both gives 48/90 = 8/15. Only one path gives 24/90 = 4/15.")],
     "gs": [
        box("Red then blue: top is 6 × 4 = ", 24, "Multiply the numerators 6 and 4.", say="'One of each' has two paths: red then blue, or blue then red. Total balls = 10."),
        box("Its bottom, 10 × 9 = ", 90, "10 balls then 9 balls."),
        box("Blue then red gives (4/10) × (6/9), the same 24/90. Its top, 4 × 6 = ", 24, "Multiply 4 and 6."),
        box("Add the two paths: 24/90 + 24/90. Top, 24 + 24 = ", 48, "Add the numerators, keep the bottom 90.", say="Now add both orders.", phase="substitute"),
        box("Simplify 48/90 by dividing by 6. Top, 48 ÷ 6 = ", 8, "48 ÷ 6."),
        box("Bottom, 90 ÷ 6 = ", 15, "90 ÷ 6.", done="P(one of each) = 8/15."),
     ]},
]

GOLD = [
    {"fig": "g1",
     "hint": "Each draw removes a red: 8/12, then 7/11, then 6/10, all multiplied.",
     "mis": [mc("two_draws_only", [14, 33], "Three balls are drawn, so there are three factors: 8/12 × 7/11 × 6/10. Stopping after two draws gives 56/132 = 14/33.")],
     "gs": [
        box("Total balls = 8 + 4 = 12. P(first red), top: ", 8, "8 red out of 12.", say="First draw: 8 red out of 12."),
        box("P(second red), top (red now left): ", 7, "8 − 1 = 7 red remain.", say="One red gone: 7 red left, 11 balls."),
        box("P(third red), top (red now left): ", 6, "7 − 1 = 6 red remain.", say="Another red gone: 6 red left, 10 balls."),
        box("Multiply all three tops: 8 × 7 × 6 = ", 336, "8 × 7 = 56, then × 6.", say="Multiply the three tops and the three bottoms.", phase="substitute"),
        box("Multiply the bottoms: 12 × 11 × 10 = ", 1320, "12 × 11 = 132, then × 10."),
        box("Simplify 336/1320 by dividing by 24. Top, 336 ÷ 24 = ", 14, "336 ÷ 24."),
        box("Bottom, 1320 ÷ 24 = ", 55, "1320 ÷ 24.", done="P(all red) = 14/55."),
     ]},
    {"hint": "At least one = 1 minus the probability of no rain on either day.",
     "mis": [
        mc("added_probs", 0.7, "Adding 0.3 + 0.4 = 0.7 double-counts the day both are rainy. Use 1 − P(no rain) = 1 − 0.7 × 0.6 = 0.58 instead."),
        mc("forgot_complement", 0.42, "0.42 is P(no rain on either day). 'At least one' is the rest: 1 − 0.42 = 0.58."),
     ],
     "gs": [
        box("P(no rain Mon), 1 − 0.3 = ", 0.7, "1 − 0.3.", say="'At least one' is the opposite of 'none'. Find P(no rain) each day first."),
        box("P(no rain Tue), 1 − 0.4 = ", 0.6, "1 − 0.4."),
        box("P(no rain either day) = 0.7 × 0.6 = ", 0.42, "7 × 6 = 42, two decimal places."),
        box("'At least one' is everything else. 1 − 0.42 = ", 0.58, "Take 0.42 from 1.", phase="substitute", done="P(at least one) = 0.58."),
        box("Check the two opposites total 1: 0.58 + 0.42 = ", 1, "Add both.", say="Check:", done="The opposites total 1, so 0.58 is right."),
     ]},
    {"hint": "Each head is 1/2, and three in a row multiply: 1/2 × 1/2 × 1/2.",
     "mis": [mc("two_coins_only", [1, 4], "There are three coins, so 1/2 × 1/2 × 1/2 = 1/8. Using only two gives 1/4.")],
     "gs": [
        box("How many tosses are there? ", 3, "Three coins.", say="Each toss is independent with P(head) = 1/2. Three heads multiply."),
        box("Multiply the tops: 1 × 1 × 1 = ", 1, "1 times 1 times 1."),
        box("Multiply the bottoms: 2 × 2 × 2 = ", 8, "2 × 2 = 4, then × 2.", say="The denominator is the total number of outcomes.", phase="substitute"),
        box("There are 8 equally likely outcomes and only HHH works. Favourable outcomes: ", 1, "Only HHH.", done="1 out of 8, so P(all heads) = 1/8."),
     ]},
    {"hint": "Count the arrangements with exactly two heads out of 8 outcomes.",
     "mis": [mc("one_arrangement", [1, 8], "Two heads can land three ways: HHT, HTH, THH. That is 3 out of 8. Counting one arrangement gives 1/8.")],
     "gs": [
        box("Total outcomes of three coins, 2 × 2 × 2 = ", 8, "2 × 2 × 2.", say="Three coins give 8 equally likely outcomes."),
        box("How many have exactly two heads (HHT, HTH, THH)? ", 3, "Count HHT, HTH, THH.", say="List those with exactly two heads."),
        box("So P = 3/8, and 3 and 8 share no factor. Numerator (favourable): ", 3, "3 arrangements.", say="Already in lowest terms.", phase="substitute"),
        box("Check all outcomes: 1 (HHH) + 3 (two H) + 3 (one H) + 1 (no H) = ", 8, "Add the four counts.", done="They total 8, and the two-head group is 3, so P = 3/8 is right."),
     ]},
    {"fig": "g5",
     "hint": "After one blue is taken, 4 blue remain out of 11. Multiply 5/12 by 4/11.",
     "mis": [mc("used_with_replacement", [25, 144], "Without replacement the first blue is not returned, so the second draw is 4/11, not 5/12. That gives 5/12 × 4/11 = 5/33. Using 5/12 twice gives 25/144.")],
     "gs": [
        box("Total balls = 7 + 5 = 12. P(first blue), top: ", 5, "5 blue out of 12.", say="First draw: 5 blue out of 12."),
        box("P(second blue), top (blue now left): ", 4, "5 − 1 = 4 blue remain.", say="One blue gone and kept out: 4 blue left, 11 balls."),
        box("Multiply the branches: (5/12) × (4/11). New top, 5 × 4 = ", 20, "Multiply the numerators.", phase="substitute"),
        box("New bottom, 12 × 11 = ", 132, "Multiply the denominators."),
        box("Simplify 20/132 by dividing by 4. Top, 20 ÷ 4 = ", 5, "20 ÷ 4.", say="Now simplify."),
        box("Bottom, 132 ÷ 4 = ", 33, "132 ÷ 4.", done="P(both blue) = 5/33."),
     ]},
]

def apply(tier_list, spec_list):
    assert len(tier_list) == len(spec_list), "count mismatch %d vs %d" % (len(tier_list), len(spec_list))
    for prob, spec in zip(tier_list, spec_list):
        prob["hint"] = spec["hint"]
        prob["misconceptions"] = spec["mis"]
        prob["guided_steps"] = spec["gs"]
        if spec.get("fig"):
            fig = FIG[spec["fig"]]
            prob["display"] = fig + "<div style=\"margin-top:6px\">" + prob["display"] + "</div>"

apply(pb["bronze"], BRONZE)
apply(pb["silver"], SILVER)
apply(pb["gold"], GOLD)

OUT = "lesson_maths-ocr_probability-statistics-L01.json"
with io.open(OUT, "w", encoding="utf-8") as f:
    json.dump(pd, f, indent=1, ensure_ascii=False)
print("wrote", OUT)
print("bronze", len(pb["bronze"]), "silver", len(pb["silver"]), "gold", len(pb["gold"]))
print("preserved worked_examples:", len(pd.get("worked_examples", [])),
      "| related_videos:", len(pd.get("related_videos", [])),
      "| topic_links keys:", list(pd.get("topic_links", {}).keys()))
