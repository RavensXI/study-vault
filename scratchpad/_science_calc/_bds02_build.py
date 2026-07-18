# -*- coding: utf-8 -*-
"""Build guided practice_data for biology-data-skills-L02 (Punnett Squares)."""
import json, io

# ---------- Punnett square SVG (2x2), self-contained, currentColor ----------
def punnett(top, side, cells, aria):
    # top = [labelL, labelR]; side = [labelT, labelB]; cells = [(text,fill) x4] row-major
    xm = [101, 194]      # inner column centres
    ym = [107, 200]      # inner row centres
    fills = ""
    rects = [(55, 55), (148, 55), (55, 148), (148, 148)]  # x,y of each inner cell
    for (rx, ry), (_txt, fill) in zip(rects, cells):
        fills += ('<rect x="%d" y="%d" width="92" height="92" fill="%s" fill-opacity="0.3"/>'
                  % (rx, ry, fill))
    grid = ('<rect x="55" y="55" width="185" height="185" fill="none" stroke="currentColor" stroke-width="1.5"/>'
            '<line x1="148" y1="55" x2="148" y2="240" stroke="currentColor" stroke-width="1.5"/>'
            '<line x1="55" y1="148" x2="240" y2="148" stroke="currentColor" stroke-width="1.5"/>')
    lbl = ('<text x="101" y="42" text-anchor="middle" font-family="Inter,sans-serif" font-size="20" font-weight="700" fill="currentColor">%s</text>'
           '<text x="194" y="42" text-anchor="middle" font-family="Inter,sans-serif" font-size="20" font-weight="700" fill="currentColor">%s</text>'
           '<text x="27" y="113" text-anchor="middle" font-family="Inter,sans-serif" font-size="20" font-weight="700" fill="currentColor">%s</text>'
           '<text x="27" y="206" text-anchor="middle" font-family="Inter,sans-serif" font-size="20" font-weight="700" fill="currentColor">%s</text>'
           % (top[0], top[1], side[0], side[1]))
    ctext = ""
    for (cx, cy), (txt, _f) in zip([(101,113),(194,113),(101,206),(194,206)], cells):
        ctext += ('<text x="%d" y="%d" text-anchor="middle" font-family="Inter,sans-serif" font-size="18" fill="currentColor">%s</text>'
                  % (cx, cy, txt))
    return ('<svg viewBox="0 0 250 250" role="img" aria-label="%s">%s%s%s%s</svg>'
            % (aria, fills, grid, lbl, ctext))

BLUE = "#60a5fa"; AMBER = "#f59e0b"; GREEN = "#34d399"

svg_opener = punnett(["B", "b"], ["B", "b"],
    [("BB", BLUE), ("Bb", BLUE), ("bB", BLUE), ("bb", AMBER)],
    "Punnett square: B and b from each parent give BB, Bb, bB and bb")
svg_bronze = punnett(["B", "b"], ["B", "b"],
    [("BB", BLUE), ("Bb", BLUE), ("Bb", BLUE), ("bb", AMBER)],
    "Punnett square for Bb crossed with Bb, giving BB, Bb, Bb and bb")
svg_silver = punnett(["R", "r"], ["R", "r"],
    [("RR", BLUE), ("Rr", BLUE), ("Rr", BLUE), ("rr", AMBER)],
    "Punnett square for Rr crossed with Rr, giving RR, Rr, Rr and rr")
svg_gold = punnett(["R", "R"], ["R", "W"],
    [("RR", AMBER), ("RR", AMBER), ("RW", GREEN), ("RW", GREEN)],
    "Punnett square for RR crossed with RW, giving RR, RR, RW and RW")


def sv(display, sol, unit, calc, hint, misc, steps, higher=False):
    d = {"display": display, "input_type": "single_value", "solutions": [sol],
         "calculator": calc, "higher_only": higher, "hint": hint,
         "misconceptions": misc, "guided_steps": steps}
    if unit is not None:
        d["unit"] = unit
    return d


def mc(display, options, sol, hint, misc, steps=None):
    d = {"display": display, "input_type": "multiple_choice", "options": options,
         "solutions": [sol], "calculator": False, "higher_only": False,
         "hint": hint, "misconceptions": misc}
    if steps is not None:
        d["guided_steps"] = steps
    return d


def m(pattern, message, expect):
    return {"pattern": pattern, "check": "common", "message": message, "expect": expect}


# ---------------- BRONZE ----------------
b0_steps = [
    {"say": "Each parent is Bb, so each can pass B or b. Fill the 2 by 2 grid: BB, Bb, Bb, bb."},
    {"pre": "How many boxes are BB? ", "post": "", "answer": 1,
     "hint": "Only the top-left box takes B from both parents."},
    {"pre": "How many boxes are Bb (count Bb and bB together)? ", "post": "", "answer": 2,
     "hint": "Two boxes mix one B with one b."},
    {"say": "So far 1 BB and 2 Bb. One box is left."},
    {"phase": "substitute", "pre": "How many boxes are bb? ", "post": "", "answer": 1,
     "hint": "The bottom-right box takes b from both parents."},
    {"phase": "substitute", "pre": "Check they total four: 1 + 2 + 1 = ", "post": "", "answer": 4,
     "done": "That gives 1 BB : 2 Bb : 1 bb, which is the first option.",
     "hint": "Add the three counts."},
]
g0_steps = [
    {"say": "The child has NO dimples. Dimples (D) is dominant, so the no-dimples child must be the double-recessive genotype dd."},
    {"pre": "How many capital D alleles does a dd child carry? ", "post": "", "answer": 0,
     "hint": "A recessive trait shows only with two lowercase alleles."},
    {"say": "So the child inherited one d from EACH parent. But both parents SHOW dimples, so each also carries a D. A parent with one D and one d is written Dd."},
    {"pre": "How many d alleles must each dimpled parent carry to give a dd child? ", "post": "", "answer": 1,
     "hint": "The child needs one d from each side."},
    {"phase": "substitute", "pre": "From Dd × Dd, how many of the four boxes are dd? ", "post": "", "answer": 1,
     "hint": "Only the box taking d from both parents is dd."},
    {"phase": "substitute", "pre": "From DD × Dd, how many boxes could be dd? ", "post": "", "answer": 0,
     "done": "Only Dd × Dd can give a dd child, so both parents are Dd (the third option).",
     "hint": "DD has no d to pass, so no box can be dd."},
]
bronze = [
    mc("In a cross between two heterozygous parents (Bb × Bb), what ratio of offspring genotypes would you expect?",
       ["1 BB : 2 Bb : 1 bb", "2 BB : 1 Bb : 1 bb", "1 BB : 1 Bb : 2 bb", "3 BB : 1 bb"], 0,
       "Build the 2 by 2 grid for Bb by Bb, then count how many BB, Bb and bb you get.",
       [m("wrong_ratio", "Bb × Bb gives BB, Bb, Bb, bb, which is 1 BB : 2 Bb : 1 bb.", None)],
       b0_steps),
    mc("Tall pea plants (T) are dominant to short (t). If two heterozygous plants (Tt × Tt) are crossed, what fraction of offspring would you expect to be short?",
       ["1/2", "1/4", "3/4", "1/3"], 1,
       "Only tt gives the short plant. Count how many of the four boxes are tt.",
       [m("wrong_ratio", "Tt × Tt gives TT, Tt, Tt, tt. Only tt is short = 1 out of 4 = 1/4.", None)]),
    mc("What is the genotype of an organism that is homozygous dominant for a trait represented by the letter A?",
       ["aa", "Aa", "AA", "aA"], 2,
       "Homozygous means two identical alleles; dominant means capital letters.",
       [m("confused_terms", "Homozygous = two identical alleles. Dominant = capital letter. So homozygous dominant = AA.", None)]),
    sv("A homozygous dominant parent (BB) is crossed with a homozygous recessive parent (bb). What percentage of offspring will be heterozygous (Bb)?",
       100, "%", False,
       "One parent gives only B, the other gives only b, so every box is Bb.",
       [m("wrong_ratio", "If you answered 50, remember every box mixes B from BB with b from bb, so all four are Bb: 100%.", 50)],
       [
        {"say": "BB can only pass B. bb can only pass b. So every box mixes one B with one b."},
        {"pre": "How many of the four boxes are Bb? ", "post": "", "answer": 4,
         "hint": "Every box gets B from one parent and b from the other."},
        {"pre": "How many boxes are BB or bb (homozygous)? ", "post": "", "answer": 0,
         "hint": "Neither parent can give a matching pair."},
        {"phase": "substitute", "pre": "Heterozygous as a percentage: (4 ÷ 4) × 100 = ", "post": "", "answer": 100,
         "hint": "All four boxes count."},
        {"phase": "substitute", "pre": "Check they total four: Bb (4) + others (0) = ", "post": "", "answer": 4,
         "done": "All four offspring are Bb, so 100% heterozygous is right.",
         "hint": "Add the two counts."},
       ]),
    sv("In a Bb × Bb cross, how many out of 4 offspring would you expect to show the dominant phenotype?",
       3, "", False,
       "Any box with at least one capital B shows the dominant phenotype.",
       [m("confused_terms", "If you answered 1, that is the recessive count. BB, Bb and Bb all show the dominant phenotype, so it is 3.", 1)],
       [
        {"say": "Bb × Bb gives BB, Bb, Bb, bb. Any box with at least one B shows the dominant phenotype."},
        {"pre": "How many boxes contain at least one B? ", "post": "", "answer": 3,
         "hint": "BB, Bb and Bb all have a capital B."},
        {"pre": "How many boxes are bb (recessive)? ", "post": "", "answer": 1,
         "hint": "Only the bb box shows the recessive phenotype."},
        {"phase": "substitute", "pre": "Dominant phenotype out of four = 4 − 1 = ", "post": "", "answer": 3,
         "hint": "Take the one recessive box away from four."},
        {"phase": "substitute", "pre": "Check: dominant (3) + recessive (1) = ", "post": "", "answer": 4,
         "done": "All four boxes accounted for, so 3 show the dominant phenotype.",
         "hint": "Add the two counts."},
       ]),
    mc("A parent with genotype Bb produces gametes. Which alleles can be in the gametes?",
       ["Only B", "Only b", "B or b", "Bb"], 2,
       "A gamete carries just one allele from the pair, not both.",
       [m("gamete_error", "Each gamete gets one allele from each pair. A Bb parent makes gametes with either B or b, never both.", None)]),
    sv("Two homozygous recessive parents (bb × bb) are crossed. How many out of 4 offspring will show the recessive phenotype?",
       4, "", False,
       "Both parents can only pass b, so work out how many boxes are bb.",
       [m("wrong_ratio", "If you answered 1, you assumed a 3:1 cross. Here BOTH parents are bb, so every box is bb: all 4 show the recessive phenotype.", 1)],
       [
        {"say": "Each parent is bb, so each parent can only pass a b allele."},
        {"pre": "How many different alleles can a bb parent pass? ", "post": "", "answer": 1,
         "hint": "Both of its alleles are b."},
        {"pre": "So how many of the four boxes contain a capital B? ", "post": "", "answer": 0,
         "hint": "Neither parent has a B to give."},
        {"phase": "substitute", "pre": "Recessive phenotype (bb) out of four = 4 − 0 = ", "post": "", "answer": 4,
         "hint": "Every box is bb."},
        {"phase": "substitute", "pre": "Check: recessive (4) + dominant (0) = ", "post": "", "answer": 4,
         "done": "Every offspring is bb, so all 4 show the recessive phenotype.",
         "hint": "Add the two counts."},
       ]),
    sv("A Bb × Bb cross produces four offspring. What percentage of the offspring would you expect to be homozygous (either BB or bb)?",
       50, "%", False,
       "Homozygous means BB or bb. Count both, not just one.",
       [m("only_counted_one", "If you answered 25, you counted only BB. Homozygous also includes bb, so BB + bb = 2 out of 4 = 50%.", 25),
        m("confused_terms", "Homozygous means two identical alleles, so both BB and bb count. 1 BB + 1 bb = 2 out of 4 = 50%.", None)],
       [
        {"say": "Bb × Bb gives BB, Bb, Bb, bb. Homozygous means two identical letters, so BB and bb both count."},
        {"pre": "How many boxes are BB? ", "post": "", "answer": 1,
         "hint": "Only the top-left box is BB."},
        {"pre": "How many boxes are bb? ", "post": "", "answer": 1,
         "hint": "Only the bottom-right box is bb."},
        {"phase": "substitute", "pre": "Homozygous total: 1 + 1 = ", "post": "", "answer": 2,
         "hint": "Add the BB and bb counts."},
        {"phase": "substitute", "pre": "As a percentage of four: (2 ÷ 4) × 100 = ", "post": "", "answer": 50,
         "done": "2 of the 4 boxes are homozygous, so 50% is right.",
         "hint": "Divide by four, then times 100."},
       ]),
]

# ---------------- SILVER ----------------
silver = [
    sv("Cystic fibrosis is caused by a recessive allele (f). Two parents who are both carriers (Ff) have a child. What is the percentage chance that the child is a carrier but does NOT have cystic fibrosis?",
       50, "%", False,
       "Carriers are Ff. Do not count the affected ff or the unaffected FF.",
       [m("wrong_genotype", "If you answered 75, you counted ff as well. A carrier is Ff only: 2 out of 4 = 50%.", 75)],
       [
        {"say": "Ff × Ff gives FF, Ff, Ff, ff. A carrier is Ff: two different alleles, but no disease."},
        {"pre": "How many boxes are Ff (carriers)? ", "post": "", "answer": 2,
         "hint": "Two boxes mix one F with one f."},
        {"pre": "How many boxes are ff (affected)? ", "post": "", "answer": 1,
         "hint": "Only the ff box has the condition."},
        {"phase": "substitute", "pre": "Carriers as a percentage: (2 ÷ 4) × 100 = ", "post": "", "answer": 50,
         "hint": "Divide by four, then times 100."},
        {"phase": "substitute", "pre": "Check: FF (1) + Ff (2) + ff (1) = ", "post": "", "answer": 4,
         "done": "2 of 4 are carriers, so 50% is right.",
         "hint": "Add the three counts."},
       ]),
    sv("In a cross Bb × bb, how many out of 4 offspring would you expect to show the recessive phenotype?",
       2, "", False,
       "Cross Bb with bb, then count how many boxes are bb.",
       [m("wrong_ratio", "If you answered 1, you used a Bb × Bb ratio. Bb × bb gives Bb, Bb, bb, bb, so 2 boxes are recessive.", 1)],
       [
        {"say": "Bb passes B or b. bb passes only b. So the grid is Bb, Bb, bb, bb."},
        {"pre": "How many boxes are Bb (dominant)? ", "post": "", "answer": 2,
         "hint": "Two boxes take the B from the Bb parent."},
        {"pre": "How many boxes are bb (recessive)? ", "post": "", "answer": 2,
         "hint": "Two boxes take the b from the Bb parent."},
        {"phase": "substitute", "pre": "Recessive phenotype out of four = ", "post": "", "answer": 2,
         "hint": "The bb boxes show the recessive phenotype."},
        {"phase": "substitute", "pre": "Check: dominant (2) + recessive (2) = ", "post": "", "answer": 4,
         "done": "2 of 4 are recessive, so the answer is 2.",
         "hint": "Add the two counts."},
       ]),
    mc("Polydactyly is caused by a dominant allele (D). A father with polydactyly (Dd) and an unaffected mother (dd) have children. What is the probability of a child having polydactyly?",
       ["1 in 4 (25%)", "1 in 2 (50%)", "3 in 4 (75%)", "1 in 1 (100%)"], 1,
       "Cross Dd with dd and count how many boxes carry a D.",
       [m("wrong_cross", "Dd × dd gives Dd, Dd, dd, dd. Two have polydactyly (Dd) = 2 out of 4 = 50% = 1 in 2.", None)]),
    sv("If 200 offspring are produced from a Bb × Bb cross, how many would you expect to show the DOMINANT phenotype?",
       150, "", True,
       "Three out of four boxes show the dominant phenotype; scale that up to 200.",
       [m("wrong_ratio", "If you answered 50, that is the recessive quarter. The dominant phenotype is 3 out of 4, so 3/4 of 200 = 150.", 50)],
       [
        {"say": "Bb × Bb gives BB, Bb, Bb, bb. Three of the four boxes show the dominant phenotype."},
        {"pre": "How many of the four boxes show the dominant phenotype? ", "post": "", "answer": 3,
         "hint": "Any box with at least one B."},
        {"phase": "substitute", "pre": "Each box stands for 200 ÷ 4 = ", "post": "", "answer": 50,
         "hint": "Split 200 equally between the four boxes."},
        {"phase": "substitute", "pre": "Dominant offspring = 3 × 50 = ", "post": "", "answer": 150,
         "hint": "Three boxes, 50 each."},
        {"phase": "substitute", "pre": "Check: dominant (150) + recessive (50) = ", "post": "", "answer": 200,
         "done": "150 of 200 show the dominant phenotype.",
         "hint": "Add the dominant and recessive totals."},
       ]),
    sv("Tongue rolling (R) is dominant to non-rolling (r). A roller (Rr) and a non-roller (rr) have 80 children. How many would you expect to be non-rollers?",
       40, "", True,
       "Half the boxes are non-rollers (rr); find half of 80.",
       [m("wrong_ratio", "If you answered 20, you used 1/4. Rr × rr gives Rr, Rr, rr, rr, so HALF are non-rollers: 1/2 of 80 = 40.", 20)],
       [
        {"say": "Rr passes R or r. rr passes only r. The grid is Rr, Rr, rr, rr."},
        {"pre": "How many of the four boxes are non-rollers (rr)? ", "post": "", "answer": 2,
         "hint": "Two boxes take the r from the Rr parent."},
        {"phase": "substitute", "pre": "Each box stands for 80 ÷ 4 = ", "post": "", "answer": 20,
         "hint": "Split 80 equally between the four boxes."},
        {"phase": "substitute", "pre": "Non-rollers = 2 × 20 = ", "post": "", "answer": 40,
         "hint": "Two non-roller boxes, 20 each."},
        {"phase": "substitute", "pre": "Check: rollers (40) + non-rollers (40) = ", "post": "", "answer": 80,
         "done": "40 of 80 are non-rollers.",
         "hint": "Add rollers and non-rollers."},
       ]),
    sv("Sickle cell trait is caused by allele S. A carrier (AS) and an unaffected person (AA) have 20 children. How many would you expect to be carriers (AS)?",
       10, "", True,
       "Half the children are carriers; find half of 20.",
       [m("wrong_ratio", "If you answered 5, you used 1/4. AS × AA gives AA, AA, AS, AS, so HALF are carriers: 1/2 of 20 = 10.", 5)],
       [
        {"say": "The carrier AS passes A or S. The unaffected AA passes only A. The grid is AA, AA, AS, AS."},
        {"pre": "How many of the four boxes are carriers (AS)? ", "post": "", "answer": 2,
         "hint": "Two boxes take the S from the AS parent."},
        {"phase": "substitute", "pre": "Each box stands for 20 ÷ 4 = ", "post": "", "answer": 5,
         "hint": "Split 20 equally between the four boxes."},
        {"phase": "substitute", "pre": "Carriers = 2 × 5 = ", "post": "", "answer": 10,
         "hint": "Two carrier boxes, 5 each."},
        {"phase": "substitute", "pre": "Check: carriers (10) + non-carriers (10) = ", "post": "", "answer": 20,
         "done": "10 of 20 are carriers.",
         "hint": "Add carriers and non-carriers."},
       ]),
]

# ---------------- GOLD ----------------
gold = [
    mc("A couple both have dimples (dominant trait, D). They have a child without dimples. What are the genotypes of both parents?",
       ["DD × DD", "DD × Dd", "Dd × Dd", "Dd × dd"], 2,
       "The no-dimples child must be dd, so each parent had a d to give while still showing dimples.",
       [m("wrong_logic", "The child without dimples is dd, so inherited a d from each parent. Both parents show dimples, so each also has a D. Both must be Dd.", None),
        m("impossible_cross", "DD × DD can only give DD. DD × Dd cannot give dd. Only Dd × Dd can produce a dd child.", None)],
       g0_steps),
    sv("Red flower colour (R) is incompletely dominant with white (W). Heterozygous (RW) flowers are pink. If two pink flowers are crossed, what percentage of offspring will be pink?",
       50, "%", False,
       "With incomplete dominance the RW heterozygote is pink; count the RW boxes.",
       [m("wrong_ratio", "If you answered 25, you counted only one box. RW × RW gives RR, RW, RW, WW, so 2 of 4 are pink = 50%.", 25),
        m("confused_dominance", "With incomplete dominance the heterozygote has a blend phenotype. RW × RW gives 1 red : 2 pink : 1 white.", None)],
       [
        {"say": "RW × RW gives RR (red), RW (pink), RW (pink), WW (white). With incomplete dominance, RW shows as pink."},
        {"pre": "How many boxes are RW (pink)? ", "post": "", "answer": 2,
         "hint": "Two boxes mix one R with one W."},
        {"pre": "How many boxes are RR (red)? ", "post": "", "answer": 1,
         "hint": "Only the top-left box is RR."},
        {"phase": "substitute", "pre": "Pink as a percentage: (2 ÷ 4) × 100 = ", "post": "", "answer": 50,
         "hint": "Divide by four, then times 100."},
        {"phase": "substitute", "pre": "Check: red (1) + pink (2) + white (1) = ", "post": "", "answer": 4,
         "done": "2 of 4 are pink, so 50% is right.",
         "hint": "Add the three counts."},
       ]),
    sv("Colour blindness is sex-linked and recessive, carried on the X chromosome. A carrier mother (Xb on one X) and a father with normal vision have children. What percentage of ALL their children would you expect to have normal colour vision?",
       75, "%", False,
       "Only the affected son (Xb Y) is colour-blind; the other three boxes have normal vision.",
       [m("wrong_percentage", "If you answered 25, that is the colour-blind fraction. Three of the four children have normal vision, so 75%.", 25),
        m("wrong_parent", "The father's Y chromosome carries no allele for this trait. Only the son who gets Xb from his mother is colour-blind.", None)],
       [
        {"say": "The four children are: a normal-vision daughter, a carrier daughter, a normal-vision son, and a colour-blind son (Xb Y). Only that last son is affected."},
        {"pre": "How many of the four children are colour-blind? ", "post": "", "answer": 1,
         "hint": "Only the son who inherits Xb from his mother."},
        {"pre": "How many have normal colour vision? ", "post": "", "answer": 3,
         "hint": "Four children minus the one affected son."},
        {"phase": "substitute", "pre": "Normal vision as a percentage: (3 ÷ 4) × 100 = ", "post": "", "answer": 75,
         "hint": "Divide by four, then times 100."},
        {"phase": "substitute", "pre": "Check: colour-blind (1) + normal (3) = ", "post": "", "answer": 4,
         "done": "3 of 4 children have normal vision, so 75% is right.",
         "hint": "Add the two counts."},
       ]),
    mc("In a genetics experiment, 120 pea plants are produced from a monohybrid cross. 91 have round seeds and 29 have wrinkled seeds. What is the expected ratio, and does the actual data closely fit it?",
       ["Expected 3:1, and yes: 91:29 is about 3.1:1, which is close",
        "Expected 1:1, and no: the data does not fit",
        "Expected 3:1, but no: 91:29 is too far from 90:30",
        "Expected 1:3, and yes: the data fits well"], 0,
       "A 3 to 1 ratio predicts 90 to 30; check how close 91 to 29 is.",
       [m("wrong_ratio", "A 3:1 ratio predicts 90 round : 30 wrinkled. Actual is 91:29. 91 ÷ 29 is about 3.1:1, very close to 3:1.", None),
        m("exact_match", "Real data rarely matches predicted ratios exactly. 91:29 is close enough to 3:1 (predicted 90:30) to support the model.", None)]),
    sv("A man with blood type A (genotype AO) and a woman with blood type B (genotype BO) have children. What percentage of their children could have blood type O?",
       25, "%", False,
       "Only the OO box gives type O; that is one box out of four.",
       [m("codominance_error", "If you answered 0, remember each parent carries a hidden O. AO × BO gives AB, AO, BO, OO, so the OO box is type O: 25%.", 0),
        m("wrong_cross", "A and B are codominant with each other but both are dominant over O. Only OO gives type O blood.", None)],
       [
        {"say": "The father AO passes A or O. The mother BO passes B or O. The grid is AB, AO, BO, OO."},
        {"pre": "How many boxes are OO (type O)? ", "post": "", "answer": 1,
         "hint": "Only the box taking O from both parents."},
        {"pre": "How many boxes are NOT type O? ", "post": "", "answer": 3,
         "hint": "AB, AO and BO all carry an A or a B."},
        {"phase": "substitute", "pre": "Type O as a percentage: (1 ÷ 4) × 100 = ", "post": "", "answer": 25,
         "hint": "Divide by four, then times 100."},
        {"phase": "substitute", "pre": "Check: type O (1) + not O (3) = ", "post": "", "answer": 4,
         "done": "1 of 4 is type O, so 25% is right.",
         "hint": "Add the two counts."},
       ]),
    sv("Two parents who are both heterozygous (Ff) for cystic fibrosis already have 3 children, none affected. Out of every 4 children from this cross, how many would you expect to have cystic fibrosis?",
       1, "", False,
       "Each pregnancy is independent, so the earlier children do not change the odds.",
       [m("gambler_fallacy", "If you answered 0, that is the gambler's fallacy. The 3 healthy children do not change the odds: Ff × Ff still expects 1 in 4 affected.", 0),
        m("wrong_logic", "Previous children being unaffected does NOT raise or lower the chance for the next. It stays at 1 in 4.", None)],
       [
        {"say": "Each pregnancy is independent, so the 3 healthy children already born do not change anything. Ff × Ff gives FF, Ff, Ff, ff."},
        {"pre": "How many of the four boxes are ff (cystic fibrosis)? ", "post": "", "answer": 1,
         "hint": "Only the ff box has the condition."},
        {"pre": "How many are unaffected (FF or Ff)? ", "post": "", "answer": 3,
         "hint": "Four boxes minus the one ff box."},
        {"phase": "substitute", "pre": "Expected affected out of four = ", "post": "", "answer": 1,
         "hint": "Only the ff box."},
        {"phase": "substitute", "pre": "Check: affected (1) + unaffected (3) = ", "post": "", "answer": 4,
         "done": "1 in 4, no matter how many healthy children came before.",
         "hint": "Add the two counts."},
       ]),
]

# ---------------- tier_guides ----------------
def guide(title, steps, q, ex_steps):
    return {"title": title, "steps": steps,
            "example": {"question": q, "steps": ex_steps}}

tier_guides = {
    "bronze": guide(
        "Bronze: read the cross and count",
        ["You are given both parents' genotypes. Write the gametes each can pass (one allele each), then draw a 2 by 2 grid.",
         "Fill the four boxes by combining the top allele with the side allele. <strong>Bb and bB are the same</strong>, so count them together.",
         "Count the genotype or phenotype the question asks for. The recessive phenotype (lowercase pair, like bb) shows only when both alleles are recessive."],
        "Brown fur (B) is dominant to white (b). Cross Bb × Bb. What fraction is white?",
        [{"label": "Grid", "content": "<p>Bb × Bb gives BB, Bb, Bb, bb.</p>"},
         {"label": "Count", "content": "<p>Only bb is white: 1 out of 4 boxes.</p>"},
         {"label": "Check", "content": "<p>1 white + 3 brown = 4 offspring.</p>"},
         {"label": "Answer", "content": "<p>1/4 are white.</p>", "isAnswer": True, "is_answer": True}]),
    "silver": guide(
        "Silver: turn the ratio into a number",
        ["Work out the cross yourself, then find the fraction with the phenotype you want (for example 1/4 recessive, or 1/2 in a cross with one recessive parent).",
         "To scale to a real population, split the total equally between the four boxes: each box is total ÷ 4.",
         "Multiply that share by how many boxes match. Always check your groups add back to the total."],
        "Tt × Tt gives 40 plants. How many are short (tt)?",
        [{"label": "Fraction", "content": "<p>Short (tt) is 1 out of 4.</p>"},
         {"label": "Share", "content": "<p>Each box = 40 ÷ 4 = 10.</p>"},
         {"label": "Scale", "content": "<p>Short = 1 × 10 = 10.</p>"},
         {"label": "Answer", "content": "<p>10 short plants.</p>", "isAnswer": True, "is_answer": True}]),
    "gold": guide(
        "Gold: special inheritance and reverse clues",
        ["Some crosses are not simple dominant and recessive. In <strong>codominance</strong> and <strong>incomplete dominance</strong> the heterozygote has its own phenotype (roan, pink), so count it separately.",
         "<strong>Sex-linked</strong> alleles sit on the X chromosome; a son has only one X, so one recessive X allele already shows.",
         "To work backwards, use a recessive child (double-recessive genotype) to pin down what alleles each parent must carry."],
        "Red (R) and white (W) coat alleles are codominant; RW is roan. Cross RR × RW. What fraction is roan?",
        [{"label": "Grid", "content": "<p>RR × RW gives RR, RR, RW, RW.</p>"},
         {"label": "Count", "content": "<p>Roan (RW) = 2 out of 4 boxes.</p>"},
         {"label": "Check", "content": "<p>2 red + 2 roan = 4 calves.</p>"},
         {"label": "Answer", "content": "<p>1/2 are roan.</p>", "isAnswer": True, "is_answer": True}]),
}

# ---------------- guided (opener + teach) ----------------
opener = {
    "label": "Before any genetics",
    "display": svg_opener,
    "steps": [
        {"say": "Each parent carries two alleles, one B and one b, like two tokens in a bag. Each parent passes ONE token to the child, at random. The grid shows every equally likely pair the child could end up with.",
         "pre": "How many equally likely combinations are in the grid? ", "post": "", "answer": 4,
         "hint": "Count the four boxes."},
        {"say": "A recessive trait, say blue eyes, only appears when the child gets TWO b tokens, bb.",
         "pre": "How many of the four boxes are bb? ", "post": "", "answer": 1,
         "hint": "Only the bottom-right box has b and b."},
        {"say": "So 1 out of 4, a quarter, 25%. That grid IS a <strong>Punnett square</strong>, and the cross is written <strong>Bb × Bb</strong>. Filling boxes and counting them is the whole skill."},
    ],
}
teach = {
    "bronze": {
        "label": "Together: read and count",
        "display": svg_bronze + "Brown fur (B) is dominant to white (b). Two heterozygous mice, Bb × Bb, are crossed. What percentage of offspring have white fur?",
        "steps": [
            {"say": "The grid is BB, Bb, Bb, bb. White fur needs two recessive alleles, bb."},
            {"pre": "How many boxes are bb (white)? ", "post": "", "answer": 1,
             "hint": "Only the bottom-right box."},
            {"pre": "How many boxes are brown (have a B)? ", "post": "", "answer": 3,
             "hint": "BB, Bb and Bb all have a capital B."},
            {"pre": "White as a percentage: (1 ÷ 4) × 100 = ", "post": "", "answer": 25,
             "hint": "One box out of four."},
            {"pre": "Check: white (1) + brown (3) = ", "post": "", "answer": 4,
             "done": "1 of 4 is white, so 25%. That is the whole bronze move: read the grid and count.",
             "hint": "Add the two counts."},
        ],
    },
    "silver": {
        "label": "Together: scale to a population",
        "display": svg_silver + "Tongue rolling (R) is dominant to non-rolling (r). Two heterozygous parents, Rr × Rr, have 60 children. How many would you expect to be non-rollers?",
        "steps": [
            {"say": "The grid is RR, Rr, Rr, rr. Non-rollers need two recessive alleles, rr."},
            {"pre": "How many of the four boxes are non-rollers (rr)? ", "post": "", "answer": 1,
             "hint": "Only the rr box."},
            {"pre": "Each box stands for 60 ÷ 4 = ", "post": "", "answer": 15,
             "hint": "Split 60 equally between four boxes."},
            {"pre": "Non-rollers = 1 × 15 = ", "post": "", "answer": 15,
             "hint": "One non-roller box, 15 each."},
            {"pre": "Check: rollers (45) + non-rollers (15) = ", "post": "", "answer": 60,
             "done": "15 non-rollers. The silver move is turning 1/4 into a real number.",
             "hint": "Add rollers and non-rollers."},
        ],
    },
    "gold": {
        "label": "Together: codominance",
        "display": svg_gold + "In cattle, coat colour alleles R (red) and W (white) are codominant: RW cattle are roan. A red bull (RR) is crossed with a roan cow (RW). What percentage of calves are roan?",
        "steps": [
            {"say": "The bull RR passes only R. The cow RW passes R or W. The grid is RR, RR, RW, RW. Because the alleles are codominant, RW shows as roan, not red."},
            {"pre": "How many boxes are RW (roan)? ", "post": "", "answer": 2,
             "hint": "Two boxes take the W from the cow."},
            {"pre": "How many boxes are RR (red)? ", "post": "", "answer": 2,
             "hint": "Two boxes take the R from the cow."},
            {"pre": "Roan as a percentage: (2 ÷ 4) × 100 = ", "post": "", "answer": 50,
             "hint": "Two boxes out of four."},
            {"pre": "Check: red (2) + roan (2) = ", "post": "", "answer": 4,
             "done": "2 of 4 are roan, so 50%. The gold move is spotting that the heterozygote has its own phenotype.",
             "hint": "Add the two counts."},
        ],
    },
}

# ---------------- method_card, exam_context, worked_examples ----------------
method_card = {
    "title": "Punnett Squares and Genetic Probability",
    "steps": [
        "Write each parent's two alleles, then list the gametes each can pass.",
        "Draw a 2 by 2 grid: one parent's gametes across the top, the other's down the side.",
        "Fill the four boxes by combining the row and column alleles.",
        "Count the genotypes or phenotypes, then give a ratio, fraction, or percentage.",
    ],
    "content": ("<p>A <strong>Punnett square</strong> shows the four equally likely allele "
                "combinations a child can inherit. A capital letter is a <strong>dominant</strong> "
                "allele (shown if present); a lowercase letter is <strong>recessive</strong> (shown "
                "only as two copies, like bb).</p><p><strong>Homozygous</strong> means two identical "
                "alleles (BB or bb); <strong>heterozygous</strong> means two different (Bb), also "
                "called a <em>carrier</em> when the recessive allele causes a disorder. Bb and bB are "
                "the same genotype, so count them together. Read carefully whether the question wants "
                "a ratio, a fraction, or a percentage.</p>"),
}

exam_context = {
    "marks": "2 to 4 marks",
    "paper": "Paper 2 (Biology)",
    "frequency": "Very common: Punnett squares appear on nearly every Paper 2",
}

worked_examples = [
    {"difficulty": "Bronze",
     "question": "Two heterozygous parents (Bb × Bb) are crossed. Brown fur (B) is dominant to white fur (b). What percentage of offspring would you expect to have white fur?",
     "steps": [
        {"label": "Step 1: Draw the Punnett square",
         "content": "<table><tr><td></td><td><strong>B</strong></td><td><strong>b</strong></td></tr><tr><td><strong>B</strong></td><td>BB</td><td>Bb</td></tr><tr><td><strong>b</strong></td><td>Bb</td><td>bb</td></tr></table>"},
        {"label": "Step 2: Count phenotypes",
         "content": "<p>BB = brown, Bb = brown (dominant), Bb = brown, bb = white</p><p>3 brown : 1 white</p>"},
        {"label": "Answer", "content": "<p><strong>25%</strong> would have white fur (1 out of 4)</p>", "is_answer": True},
     ]},
    {"difficulty": "Silver",
     "question": "Cystic fibrosis is caused by a recessive allele (f). Two carrier parents (Ff × Ff) have a child. What is the probability that the child will have cystic fibrosis?",
     "steps": [
        {"label": "Step 1: Draw the Punnett square",
         "content": "<table><tr><td></td><td><strong>F</strong></td><td><strong>f</strong></td></tr><tr><td><strong>F</strong></td><td>FF</td><td>Ff</td></tr><tr><td><strong>f</strong></td><td>Ff</td><td>ff</td></tr></table>"},
        {"label": "Step 2: Identify affected offspring",
         "content": "<p>Only ff has cystic fibrosis (homozygous recessive). That is 1 out of 4 boxes.</p>"},
        {"label": "Answer", "content": "<p>Probability = <strong>1 in 4</strong> (25% or 0.25)</p>", "is_answer": True},
     ]},
    {"difficulty": "Gold",
     "question": "A couple has four children. Three have brown eyes and one has blue eyes. Blue eyes are recessive (bb). Determine the genotypes of both parents. Explain your reasoning.",
     "steps": [
        {"label": "Step 1: Work backwards from the offspring",
         "content": "<p>One child has blue eyes (bb). This means the child must have inherited one b from each parent.</p>"},
        {"label": "Step 2: Determine parent genotypes",
         "content": "<p>Both parents must carry at least one b allele. Since both parents have brown eyes (dominant phenotype), they must each also carry one B allele.</p>"},
        {"label": "Answer", "content": "<p>Both parents are <strong>Bb</strong> (heterozygous). This gives a 3:1 ratio, matching 3 brown : 1 blue.</p>", "is_answer": True},
     ]},
]

pd = {
    "method_card": method_card,
    "topic_links": {"prerequisites": [
        "Inheritance and genetics (Biology Paper 2)",
        "Genetic disorders (Biology Paper 2)"]},
    "exam_context": exam_context,
    "problem_bank": {
        "bronze": bronze,
        "silver": silver,
        "gold": gold,
        "bronze_description": "Read a ready-made cross, fill the grid, and count genotypes or phenotypes.",
        "silver_description": "Work out the cross yourself, then turn the ratio into a percentage or a real number of offspring.",
        "gold_description": "Handle codominance, sex linkage, blood groups, or reason backwards from the offspring.",
    },
    "related_videos": [],
    "worked_examples": worked_examples,
    "tier_guides": tier_guides,
    "guided": {"opener": opener, "teach": teach},
}

OUT = "lesson_biology-data-skills-L02@551b362537.json"
with io.open(OUT, "w", encoding="utf-8") as f:
    json.dump(pd, f, ensure_ascii=False, indent=1)
print("wrote", OUT)
