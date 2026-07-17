# -*- coding: utf-8 -*-
import json, io

live = json.load(io.open("_ES_L01_live.json", encoding="utf-8"))
pd = live["practice_data"]
pb = pd["problem_bank"]

# ---------- SVG helpers (programmatic, labels derived from numbers) ----------
END_Y = [24, 68, 120, 164]
LBL_Y = [28, 72, 124, 168]
S_XY = [(170, 32), (170, 68), (170, 129), (170, 165)]

def tree2(aria, p1a, p1b, La, Lb, s0, s1, s2, s3, ends, hi):
    P = []
    P.append('<svg viewBox="0 0 250 190" role="img" aria-label="%s" style="max-width:250px">' % aria)
    for (x1,y1,x2,y2) in [(16,95,108,46),(16,95,108,144),(108,46,232,24),(108,46,232,68),(108,144,232,120),(108,144,232,164)]:
        P.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="currentColor" stroke-width="1"/>' % (x1,y1,x2,y2))
    for (cx,cy) in [(16,95),(108,46),(108,144),(232,24),(232,68),(232,120),(232,164)]:
        P.append('<circle cx="%d" cy="%d" r="3" fill="currentColor"/>' % (cx,cy))
    def txt(x,y,t,anchor="middle",bold=False):
        w = ' font-weight="600"' if bold else ''
        return '<text x="%d" y="%d" font-family="Inter, sans-serif" font-size="11" fill="currentColor" text-anchor="%s"%s>%s</text>' % (x,y,anchor,w,t)
    P.append(txt(62,67,p1a)); P.append(txt(62,131,p1b))
    P.append(txt(104,40,La,bold=True)); P.append(txt(104,158,Lb,bold=True))
    for (sx,sy),s in zip(S_XY,[s0,s1,s2,s3]):
        P.append(txt(sx,sy,s))
    for i,e in enumerate(ends):
        bold = i in hi
        P.append(txt(240,LBL_Y[i],e,anchor="start",bold=bold))
        if bold:
            P.append('<circle cx="232" cy="%d" r="3" fill="currentColor"/>' % END_Y[i])
    P.append('</svg>')
    return "".join(P)

def chain3(aria, f0, f1, f2, letter, result):
    P = []
    P.append('<svg viewBox="0 0 250 90" role="img" aria-label="%s" style="max-width:250px">' % aria)
    segs = [(22,80,51),(92,150,121),(162,220,191)]
    fr = [f0,f1,f2]
    for (x1,x2,lx),f in zip(segs,fr):
        P.append('<line x1="%d" y1="40" x2="%d" y2="40" stroke="currentColor" stroke-width="1"/>' % (x1,x2))
        P.append('<text x="%d" y="34" font-family="Inter, sans-serif" font-size="11" fill="currentColor" text-anchor="middle">%s</text>' % (lx,f))
    for cx in [16,86,156,226]:
        P.append('<circle cx="%d" cy="40" r="3" fill="currentColor"/>' % cx)
    for cx,lab in [(86,letter),(156,letter),(226,letter)]:
        P.append('<text x="%d" y="56" font-family="Inter, sans-serif" font-size="11" fill="currentColor" text-anchor="middle">%s</text>' % (cx,lab))
    P.append('<text x="125" y="74" font-family="Inter, sans-serif" font-size="11" fill="currentColor" text-anchor="middle" font-weight="600">%s</text>' % result)
    P.append('</svg>')
    return "".join(P)

def bag(aria, counters):
    # counters: list of (cx,cy,color)
    P = []
    P.append('<svg viewBox="0 0 200 130" role="img" aria-label="%s" style="max-width:200px">' % aria)
    P.append('<path d="M36 40 L164 40 L152 118 L48 118 Z" fill="#fbbf24" fill-opacity="0.12" stroke="currentColor" stroke-width="1.5"/>')
    P.append('<line x1="52" y1="40" x2="68" y2="22" stroke="currentColor" stroke-width="1.5"/>')
    P.append('<line x1="148" y1="40" x2="132" y2="22" stroke="currentColor" stroke-width="1.5"/>')
    for cx,cy,col in counters:
        P.append('<circle cx="%d" cy="%d" r="11" fill="%s" fill-opacity="0.55" stroke="currentColor" stroke-width="1"/>' % (cx,cy,col))
    P.append('</svg>')
    return "".join(P)

RED="#f87171"; GREEN="#34d399"; YELLOW="#fbbf24"; BLUE="#60a5fa"

# ---------- box/say builders ----------
def b(pre, ans, hint, post="", say=None, phase=False, done=None):
    d = {"pre": pre, "post": post, "answer": ans, "hint": hint}
    if say is not None: d["say"] = say
    if phase: d["phase"] = "substitute"
    if done is not None: d["done"] = done
    return d
def s(say):
    return {"say": say}
def mc(pattern, message, expect, note=None):
    d = {"pattern": pattern, "message": message, "expect": expect}
    if note is not None: d["note"] = note
    return d

# ---------- per-problem specs ----------
# BRONZE
bronze = []
# b0
bronze.append(dict(hint="Count the reds, then divide by the total number of balls.",
    svg=None, misc=[mc("fav_over_unfav","Probability is favourable over the TOTAL, not over the rest. There are 3 red out of 8 balls, so P(red) = 3/8. Writing 3/5 compares reds to blues instead.",[3,5],"reds/blues")],
    gs=[s("Probability is favourable outcomes over the total. Start by counting."),
        b("How many red balls? ",3,"The bag has 3 red."),
        b("Total balls: 3 + 5 = ",8,"Add reds and blues."),
        b("P(red) numerator (the reds) = ",3,"The number of reds you counted.",say="So P(red) = favourable over total. Now write the fraction.",phase=True),
        b("P(red) denominator (the total) = ",8,"The total you found.",phase=True,done="P(red) = 3/8, already simplest.")]))
# b1
bronze.append(dict(hint="Even numbers on a dice are 2, 4 and 6, out of six faces.",
    svg=None, misc=[mc("did_not_simplify","3 out of 6 is right, but simplify: divide top and bottom by 3 to get 1/2.",[3,6],"unsimplified 3/6")],
    gs=[s("A fair dice has faces 1, 2, 3, 4, 5, 6. Count the even ones."),
        b("How many even faces (2, 4, 6)? ",3,"Count 2, 4 and 6."),
        b("Total faces = ",6,"A dice has six faces."),
        b("3 ÷ 3 = ",1,"3 divided by 3.",say="So P(even) = 3/6. That simplifies: divide top and bottom by 3.",phase=True),
        b("6 ÷ 3 = ",2,"6 divided by 3.",phase=True,done="P(even) = 1/2.")]))
# b2
bronze.append(dict(hint="P(not win) = 1 minus P(win); then write the decimal as tenths.",
    svg=None, misc=[mc("forgot_complement","That is P(win). The question asks P(not win) = 1 − 0.3 = 0.7 = 7/10.",[3,10],"gave P(win)=3/10")],
    gs=[s("P(not win) means everything except winning: 1 − P(win)."),
        b("1 − 0.3 = ",0.7,"One take away nought point three."),
        b("Write 0.7 as tenths, numerator = ",7,"Seven tenths.",say="Now turn 0.7 into a fraction: 0.7 = 7/10.",phase=True),
        b("Denominator = ",10,"Out of ten.",phase=True,done="P(not win) = 7/10.")]))
# b3
bronze.append(dict(hint="Favourable over total: mints over all the sweets, then simplify.",
    svg=None, misc=[mc("fav_over_unfav","Put mints over the TOTAL of 15 sweets: 6/15 = 2/5. 6/9 compares mints to toffees instead.",[6,9],"mint/toffee"),
                    mc("did_not_simplify","6 out of 15 is right, but simplify: divide top and bottom by 3 to get 2/5.",[6,15],"unsimplified")],
    gs=[s("Favourable over total. The mints are what we want, then simplify."),
        b("How many mint sweets? ",6,"Six mints."),
        b("Total sweets = ",15,"Fifteen sweets in all."),
        b("6 ÷ 3 = ",2,"Simplify the top.",say="So P(mint) = 6/15. Simplify by dividing top and bottom by 3.",phase=True),
        b("15 ÷ 3 = ",5,"Simplify the bottom.",phase=True,done="P(mint) = 2/5.")]))
# b4
bronze.append(dict(hint="Add all the counters for the total, then greens over it, and simplify.",
    svg=None, misc=[mc("fav_over_unfav","Put greens over the TOTAL of 12: 3/12 = 1/4. 3/9 compares greens to the other colours instead.",[3,9],"green/others"),
                    mc("did_not_simplify","3 out of 12 is right, but simplify: divide top and bottom by 3 to get 1/4.",[3,12],"unsimplified")],
    gs=[s("Total everything first, then put greens over the total and simplify."),
        b("Total counters: 4 + 3 + 5 = ",12,"Add all three colours."),
        b("How many green? ",3,"Three green."),
        b("3 ÷ 3 = ",1,"Simplify the top.",say="So P(green) = 3/12. Simplify by dividing top and bottom by 3.",phase=True),
        b("12 ÷ 3 = ",4,"Simplify the bottom.",phase=True,done="P(green) = 1/4.")]))
# b5 (single_value)
bronze.append(dict(hint="Expected number = probability × number of trials.",
    svg=None, misc=[mc("divide_not_multiply","Expected number = probability × trials = 0.2 × 50 = 10. Dividing 50 by 0.2 gives 250, far too many.",[250],"50/0.2")],
    gs=[s("Expected number = probability × number of trials."),
        b("The probability of rain each day = ",0.2,"Given as 0.2."),
        b("Number of days (trials) = ",50,"The event is repeated 50 times."),
        b("0.2 × 50 = ",10,"Two tenths of fifty.",say="Now multiply them together.",phase=True),
        b("Check: 10 ÷ 50 = ",0.2,"Divide to get back the probability.",phase=True,done="Expected = 10 rainy days.")]))
# b6
bronze.append(dict(hint="Count the letter B's, then divide by the total number of letters.",
    svg=None, misc=[mc("wrong_count","PROBABILITY has 11 letters and exactly 2 of them are B, so P(B) = 2/11.",[1,11],"counted one B")],
    gs=[s("Spell out PROBABILITY and count the letters."),
        b("How many letters in PROBABILITY? ",11,"P-R-O-B-A-B-I-L-I-T-Y."),
        b("How many are the letter B? ",2,"B appears twice."),
        b("Numerator = ",2,"The two B's.",say="So P(B) = B's over total letters.",phase=True),
        b("Denominator = ",11,"The total letters.",phase=True,done="P(B) = 2/11.")]))
# b7 (FIXED: 12 sections instead of 8 to remove duplicate 1/2)
bronze.append(dict(hint="Primes from 1 to 12 are 2, 3, 5, 7 and 11. Remember 1 is not prime.",
    svg=None, misc=[mc("counted_one_prime","1 is not prime. The primes from 1 to 12 are 2, 3, 5, 7 and 11: five of them, so 5/12. Counting 1 as prime gives 6/12.",[6,12],"included 1")],
    gs=[s("A prime has exactly two factors. List the primes from 1 to 12."),
        b("How many primes from 1 to 12 (2, 3, 5, 7, 11)? ",5,"Count 2, 3, 5, 7 and 11."),
        b("Total sections = ",12,"Twelve equal sections."),
        b("Numerator = ",5,"The five primes.",say="So P(prime) = primes over total. 5/12 is already simplest.",phase=True),
        b("Denominator = ",12,"The total sections.",phase=True,done="P(prime) = 5/12.")],
    override_display="A fair spinner has 12 equal sections numbered 1 to 12. Find P(prime number) as a simplified fraction.",
    override_solutions=[5,12]))

# SILVER
silver = []
# s0 two coins
silver.append(dict(hint="Multiply along the branch: P(H) then P(H) again.",
    svg=tree2("Probability tree for two coin flips","1/2","1/2","H","T","1/2","1/2","1/2","1/2",["HH","HT","TH","TT"],{0}),
    misc=[mc("one_flip_only","Two heads needs BOTH flips: 1/2 × 1/2 = 1/4. 1/2 is the chance of just one head.",[1,2],"single flip")],
    gs=[s("Two flips: draw two branches each time. P(H) = 1/2 every flip."),
        b("P(H) on flip 1, numerator = ",1,"One head out of two."),
        b("P(H) denominator = ",2,"Two equally likely faces."),
        b("Two heads needs H then H. Multiply tops: 1 × 1 = ",1,"Top times top.",say="Multiply along the H-then-H branch.",phase=True),
        b("Multiply bottoms: 2 × 2 = ",4,"Bottom times bottom.",phase=True,done="P(two heads) = 1/4.")]))
# s1 with replacement both blue 6R4B
silver.append(dict(hint="With replacement the second pick is identical, so multiply the two equal fractions.",
    svg=tree2("Probability tree for two picks with replacement","6/10","4/10","R","B","6/10","4/10","6/10","4/10",["RR","RB","BR","BB"],{3}),
    misc=[mc("without_replacement","The ball is replaced, so the second pick is still 4/10: 4/10 × 4/10 = 4/25. Dropping the total gives 3/45 = 1/15, the without-replacement answer.",[1,15],"used 4/10*3/9")],
    gs=[s("With replacement the bag is the same each time. P(blue) = 4/10 both picks."),
        b("P(blue) numerator = ",4,"Four blue."),
        b("P(blue) denominator = ",10,"Ten balls in total."),
        b("Multiply tops: 4 × 4 = ",16,"Top times top."),
        b("Multiply bottoms: 10 × 10 = ",100,"Bottom times bottom."),
        b("16 ÷ 4 = ",4,"Simplify the top.",say="Now simplify 16/100 by dividing by 4.",phase=True),
        b("100 ÷ 4 = ",25,"Simplify the bottom.",phase=True,done="P(both blue) = 4/25.")]))
# s2 without replacement both red 5R3B
silver.append(dict(hint="Without replacement the second red is 4/7, not 5/8.",
    svg=tree2("Probability tree for two picks without replacement","5/8","3/8","R","B","4/7","3/7","5/7","2/7",["RR","RB","BR","BB"],{0}),
    misc=[mc("with_replacement","Without replacement the second red is 4/7, not 5/8: 5/8 × 4/7 = 5/14. Keeping 5/8 twice gives 25/64.",[25,64],"used 5/8*5/8")],
    gs=[s("Without replacement the second pick has one fewer red and one fewer in total."),
        b("First pick P(red) numerator = ",5,"Five red at the start."),
        b("First pick denominator = ",8,"Eight balls at the start."),
        b("After one red is gone, reds left = ",4,"One red removed from five."),
        b("Total left = ",7,"One ball removed from eight."),
        b("20 ÷ 4 = ",5,"Simplify the top.",say="So P(both red) = 5/8 × 4/7 = 20/56. Simplify by dividing by 4.",phase=True),
        b("56 ÷ 4 = ",14,"Simplify the bottom.",phase=True,done="P(both red) = 5/14.")]))
# s3 independent AND decimals (textual)
silver.append(dict(hint="Independent AND means multiply the two probabilities.",
    svg=None, misc=[mc("added_not_multiplied","Independent AND means multiply: 0.4 × 0.5 = 0.2 = 1/5. Adding gives 0.9 = 9/10.",[9,10],"0.4+0.5")],
    gs=[s("Independent AND means multiply the probabilities."),
        b("0.4 × 0.5 = ",0.2,"Four tenths of a half."),
        b("2 ÷ 2 = ",1,"Simplify the top.",say="Now 0.2 = 2/10. Simplify by dividing by 2.",phase=True),
        b("10 ÷ 2 = ",5,"Simplify the bottom.",phase=True,done="P(A and B) = 1/5.")]))
# s4 red or green single pick (textual)
silver.append(dict(hint="OR with separate colours means add the two probabilities.",
    svg=None, misc=[mc("multiplied_not_added","Separate colours on one pick is OR, so add: 4/10 + 3/10 = 7/10. Multiplying gives 12/100 = 3/25.",[3,25],"P(red)*P(green)")],
    gs=[s("One pick, two acceptable colours: this is OR, so add the probabilities."),
        b("Total balls: 4 + 3 + 3 = ",10,"Add all colours."),
        b("Reds plus greens: 4 + 3 = ",7,"Add the two wanted colours."),
        b("Numerator = ",7,"Reds plus greens.",say="So P(red or green) = 7 over the total.",phase=True),
        b("Denominator = ",10,"The total.",phase=True,done="P(red or green) = 7/10.")]))
# s5 no wins 3 spins, P(win)=1/3
silver.append(dict(hint="P(lose) is 2/3 each spin; three losses means cubing it.",
    svg=chain3("Three losing spins","2/3","2/3","2/3","L","8/27"),
    misc=[mc("forgot_to_cube","Three spins means cubing: (2/3)³ = 8/27. 2/3 is only one spin.",[2,3],"one spin")],
    gs=[s("No wins in three spins means losing every spin. P(lose) = 1 − 1/3."),
        b("P(lose) numerator (1 − 1/3 = 2/3) = ",2,"Two thirds lose."),
        b("P(lose) denominator = ",3,"Out of three."),
        b("Cube the top: 2 × 2 × 2 = ",8,"2 cubed.",say="Three losses in a row: cube the fraction.",phase=True),
        b("Cube the bottom: 3 × 3 × 3 = ",27,"3 cubed.",phase=True,done="P(no wins) = 8/27.")]))
# s6 one of each 8R2B without replacement
silver.append(dict(hint="Two orders give one of each: red then blue, and blue then red. Add them.",
    svg=tree2("Probability tree for one of each colour","8/10","2/10","R","B","7/9","2/9","8/9","1/9",["RR","RB","BR","BB"],{1,2}),
    misc=[mc("one_order_only","One of each happens two ways: red-blue AND blue-red, each 16/90. Add them: 32/90 = 16/45. One order alone is 16/90.",[16,90],"RB only")],
    gs=[s("One of each can happen two ways: red then blue, or blue then red. Without replacement."),
        b("P(red-blue) top: 8 × 2 = ",16,"Reds times blues along the path."),
        b("P(red-blue) bottom: 10 × 9 = ",90,"Ten then nine."),
        b("16 + 16 = ",32,"The two equal paths.",say="P(blue-red) works out the same, 16/90. Two paths, so add the tops.",phase=True),
        b("Simplify 32/90 by 2, top: 32 ÷ 2 = ",16,"Halve the top.",phase=True),
        b("Bottom: 90 ÷ 2 = ",45,"Halve the bottom.",phase=True,done="P(one of each) = 16/45.")]))

# GOLD
gold = []
# g0 one of each 6R4B without replacement
gold.append(dict(hint="One of each happens two ways: red then blue, and blue then red. Add them.",
    svg=tree2("Probability tree for one of each colour","6/10","4/10","R","B","5/9","4/9","6/9","3/9",["RR","RB","BR","BB"],{1,2}),
    misc=[mc("one_order_only","One of each happens two ways: red-blue AND blue-red, each 24/90. Add them: 48/90 = 8/15. One order alone is 24/90.",[24,90],"RB only")],
    gs=[s("One of each can happen two ways: red then blue, or blue then red. Without replacement."),
        b("P(red-blue) top: 6 × 4 = ",24,"Reds times blues along the path."),
        b("P(red-blue) bottom: 10 × 9 = ",90,"Ten then nine."),
        b("24 + 24 = ",48,"The two equal paths.",say="Blue-red is the same, 24/90. Add the two paths.",phase=True),
        b("Simplify 48/90 by 6, top: 48 ÷ 6 = ",8,"48 divided by 6.",phase=True),
        b("Bottom: 90 ÷ 6 = ",15,"90 divided by 6.",phase=True,done="P(one of each) = 8/15.")]))
# g1 all red, 3 picks, 7R3B
gold.append(dict(hint="Three reds without replacement: reds and total both drop each pick.",
    svg=chain3("Three reds without replacement","7/10","6/9","5/8","R","7/24"),
    misc=[mc("with_replacement","The reds drop each pick: 7/10 × 6/9 × 5/8 = 7/24. Treating it as 7/10 cubed gives 343/1000.",[343,1000],"(7/10)^3")],
    gs=[s("Three reds without replacement: reds and total both drop each pick."),
        b("Pick 1 P(red) = 7 over ",10,"Seven reds out of ten."),
        b("Pick 2: reds now 6, total now ",9,"One red and one ball removed."),
        b("Pick 3: reds now 5, total now ",8,"Another of each removed."),
        b("Multiply tops: 7 × 6 × 5 = ",210,"All three numerators."),
        b("210 ÷ 30 = ",7,"Simplify the top.",say="Multiply bottoms: 10 × 9 × 8 = 720, then simplify 210/720 by 30.",phase=True),
        b("720 ÷ 30 = ",24,"Simplify the bottom.",phase=True,done="P(all red) = 7/24.")]))
# g2 at least one head, 4 flips (textual)
gold.append(dict(hint="Easier as 1 minus P(no heads at all).",
    svg=None, misc=[mc("counted_none_case","At least one head = 1 − P(no heads) = 1 − 1/16 = 15/16. 1/16 is the chance of NO heads.",[1,16],"gave P(no heads)")],
    gs=[s("At least one head is easiest as 1 − P(no heads at all)."),
        b("P(no heads) bottom: 2 × 2 × 2 × 2 = ",16,"Two to the power four."),
        b("P(no heads) top: 1 × 1 × 1 × 1 = ",1,"One tail each flip."),
        b("16 − 1 = ",15,"One whole minus one sixteenth.",say="So P(no heads) = 1/16, and P(at least one) = 16/16 − 1/16.",phase=True),
        b("Denominator stays = ",16,"Same bottom.",phase=True,done="P(at least one head) = 15/16.")]))
# g3 total probability
gold.append(dict(hint="Add the two routes to B: through A and through not A.",
    svg=tree2("Tree for total probability of B","0.6","0.4","A","A'","0.5","0.5","0.25","0.75",["B","B'","B","B'"],{0,2}),
    misc=[mc("one_path_only","B can arrive two ways. Add them: 0.5×0.6 + 0.25×0.4 = 0.4 = 2/5. The A path alone is 0.30 = 3/10.",[3,10],"P(B|A)P(A) only")],
    gs=[s("B can be reached two ways: through A, or through not A. Total-probability rule."),
        b("Path through A: 0.6 × 0.5 = ",0.3,"P(A) times P(B given A)."),
        b("P(not A) = 1 − 0.6 = ",0.4,"The rest."),
        b("Path through not A: 0.4 × 0.25 = ",0.1,"P(not A) times P(B given not A)."),
        b("4 ÷ 2 = ",2,"Halve the top.",say="Add the paths: 0.30 + 0.10 = 0.4 = 4/10. Simplify by 2.",phase=True),
        b("10 ÷ 2 = ",5,"Halve the bottom.",phase=True,done="P(B) = 2/5.")]))
# g4 biased coin exactly one head
gold.append(dict(hint="Exactly one head means head-then-tail or tail-then-head; add both.",
    svg=tree2("Probability tree for a biased coin flipped twice","2/3","1/3","H","T","2/3","1/3","2/3","1/3",["HH","HT","TH","TT"],{1,2}),
    misc=[mc("one_order_only","Exactly one head is HT OR TH: 2/9 + 2/9 = 4/9. One order alone is 2/9.",[2,9],"HT only")],
    gs=[s("Biased coin: P(H) = 2/3, so P(T) = 1/3. Exactly one head is HT or TH."),
        b("P(HT) top: 2 × 1 = ",2,"P(H) top times P(T) top."),
        b("P(HT) bottom: 3 × 3 = ",9,"Three times three."),
        b("2 + 2 = ",4,"The two equal paths.",say="P(TH) is the same, 2/9. Two paths, so add the tops.",phase=True),
        b("Denominator stays = ",9,"Same bottom.",phase=True,done="P(exactly one head) = 4/9.")]))

# ---------- assemble problem_bank preserving order & untouched fields ----------
def build(tier_list, specs):
    out = []
    for i, p in enumerate(tier_list):
        sp = specs[i]
        disp = sp.get("override_display") or p["display"]
        if sp.get("svg"):
            disp = sp["svg"] + "<br>" + disp
        sols = sp.get("override_solutions") or p["solutions"]
        np = {
            "display": disp,
            "solutions": sols,
            "calculator": p.get("calculator", False),
            "input_type": p.get("input_type", "fraction"),
            "hint": sp["hint"],
            "misconceptions": sp["misc"],
            "guided_steps": sp["gs"],
        }
        out.append(np)
    return out

pb["bronze"] = build(pb["bronze"], bronze)
pb["silver"] = build(pb["silver"], silver)
pb["gold"]   = build(pb["gold"], gold)
pb["bronze_description"] = "Single-event probability: count the favourable outcomes over the total, then write it as a fraction in its simplest form."
pb["silver_description"] = "Two-stage probability: multiply along the branches of a tree for AND, add branches for OR, and drop the second fraction when there is no replacement."
pb["gold_description"] = "Multi-stage and conditional probability: combine several paths, handle picks without replacement, and use the total-probability rule."

# ---------- tier_guides ----------
pd["tier_guides"] = {
 "bronze": {
   "title": "Bronze: single-event probability",
   "steps": [
     "Count the <strong>favourable</strong> outcomes: the ones you want.",
     "Count the <strong>total</strong> number of equally likely outcomes.",
     "Write favourable over total, then simplify. For 'not', use \\(P(\\text{not }A) = 1 - P(A)\\)."
   ],
   "example": {"question":"A bag has 4 red and 6 green. Find P(red).","steps":[
     {"label":"Favourable","content":"4 red"},
     {"label":"Total","content":"4 + 6 = 10"},
     {"label":"Check","content":"4 out of 10, divide by 2"},
     {"label":"Answer","content":"P(red) = 4/10 = 2/5","isAnswer":True,"is_answer":True}]}
 },
 "silver": {
   "title": "Silver: two-stage probability",
   "steps": [
     "Draw a tree: one set of branches for each stage.",
     "Multiply along a branch for <strong>AND</strong> (both happen).",
     "Add branch results for <strong>OR</strong> (either happens).",
     "<strong>Without replacement</strong>: drop the picked item and the total by one on the second pick."
   ],
   "example": {"question":"A bag has 3 red, 2 blue. Two picked without replacement. Find P(both red).","steps":[
     {"label":"First pick","content":"P(red) = 3/5"},
     {"label":"Second pick","content":"reds and total drop: 2/4"},
     {"label":"Check","content":"3/5 × 2/4 = 6/20"},
     {"label":"Answer","content":"6/20 = 3/10","isAnswer":True,"is_answer":True}]}
 },
 "gold": {
   "title": "Gold: multi-stage and conditional",
   "steps": [
     "Split the event into every path that works, e.g. red-blue AND blue-red.",
     "Multiply along each path, then <strong>add</strong> the paths.",
     "Conditional: \\(P(B) = P(B|A)P(A) + P(B|A')P(A')\\).",
     "'At least one' is quickest as \\(1 - P(\\text{none})\\)."
   ],
   "example": {"question":"P(H) = 2/3. Two flips. Find P(exactly one head).","steps":[
     {"label":"HT","content":"2/3 × 1/3 = 2/9"},
     {"label":"TH","content":"1/3 × 2/3 = 2/9"},
     {"label":"Check","content":"add the paths: 2/9 + 2/9"},
     {"label":"Answer","content":"4/9","isAnswer":True,"is_answer":True}]}
 }
}

# ---------- guided (opener + teach) ----------
opener_bag = bag("A bag holding 3 red sweets and 2 green sweets",
    [(72,68,RED),(100,64,RED),(128,68,RED),(88,94,GREEN),(112,94,GREEN)])
teach_bronze_bag = bag("A bag with 2 red and 6 yellow counters",
    [(64,66,RED),(88,62,RED),(112,62,YELLOW),(136,66,YELLOW),(72,92,YELLOW),(96,96,YELLOW),(120,96,YELLOW),(144,92,YELLOW)])
teach_silver_tree = tree2("Tree for two picks with replacement from 3 red and 2 blue","3/5","2/5","R","B","3/5","2/5","3/5","2/5",["RR","RB","BR","BB"],{0})
teach_gold_tree = tree2("Tree for two picks without replacement from 4 red and 2 blue","4/6","2/6","R","B","3/5","2/5","4/5","1/5",["RR","RB","BR","BB"],{0})

pd["guided"] = {
 "opener": {
   "label": "Before any formulas",
   "steps": [
     {"say":"Picture this bag. You can see every sweet inside it.","display":opener_bag},
     {"pre":"How many sweets are red? ","post":"","answer":3,"hint":"Count the red circles."},
     {"pre":"How many sweets are there altogether? ","post":"","answer":5,"hint":"Count every circle."},
     {"say":"Reach in without looking and pick one. You just found the chance of red: 3 red out of 5 sweets, written \\(\\tfrac{3}{5}\\). That is all probability is: <strong>favourable over total</strong>."}
   ]
 },
 "teach": {
   "bronze": {
     "label":"Together: your first one",
     "display": teach_bronze_bag + "<br>A bag has 2 red and 6 yellow counters. Find P(yellow) as a fraction.",
     "steps": [
       {"say":"Favourable over total. The yellows are what we want."},
       {"pre":"How many yellow counters? ","post":"","answer":6,"hint":"Six yellow."},
       {"pre":"Total counters: 2 + 6 = ","post":"","answer":8,"hint":"Add red and yellow."},
       {"pre":"6 ÷ 2 = ","post":"","answer":3,"hint":"Simplify the top.","say":"So P(yellow) = 6/8. Simplify by dividing top and bottom by 2."},
       {"pre":"8 ÷ 2 = ","post":"","answer":4,"hint":"Simplify the bottom.","done":"P(yellow) = 3/4. Favourable over total, then simplify."}
     ]
   },
   "silver": {
     "label":"Together: the silver move",
     "display": teach_silver_tree + "<br>A bag has 3 red and 2 blue. One is taken, its colour noted, then put back and another taken. Find P(both red).",
     "steps": [
       {"say":"Two stages, so two sets of branches. Replaced, so P(red) = 3/5 both times."},
       {"pre":"First pick P(red), numerator = ","post":"","answer":3,"hint":"Three red."},
       {"pre":"First pick denominator = ","post":"","answer":5,"hint":"Five balls."},
       {"pre":"Multiply along the red-red branch, top: 3 × 3 = ","post":"","answer":9,"hint":"Top times top."},
       {"pre":"Bottom: 5 × 5 = ","post":"","answer":25,"hint":"Bottom times bottom.","done":"P(both red) = 9/25. Multiply ALONG a branch for AND."}
     ]
   },
   "gold": {
     "label":"Together: the gold move",
     "display": teach_gold_tree + "<br>A bag has 4 red and 2 blue. Two are taken without replacement. Find P(both red).",
     "steps": [
       {"say":"Without replacement, the second pick changes. Start with the first."},
       {"pre":"First pick P(red), numerator = ","post":"","answer":4,"hint":"Four red of six."},
       {"pre":"First pick denominator = ","post":"","answer":6,"hint":"Six balls."},
       {"pre":"A red is gone. Second pick reds left = ","post":"","answer":3,"hint":"One red removed."},
       {"pre":"Second pick total left = ","post":"","answer":5,"hint":"One ball removed."},
       {"pre":"Multiply: 4/6 × 3/5 = 12/30, simplify by 6. Numerator = ","post":"","answer":2,"hint":"12 ÷ 6.","done":"P(both red) = 2/5. The denominator dropped: that is the new move."}
     ]
   }
 }
}

# worked_examples preserved, except one pre-existing em dash (house style forbids em dashes).
for we in pd.get("worked_examples", []):
    for st in we.get("steps", []):
        if isinstance(st.get("content"), str) and "—" in st["content"]:
            st["content"] = st["content"].replace(" — ", ", ").replace("—", ", ")
# method_card, topic_links, related_videos otherwise preserved as-is from live pd.

json.dump(pd, io.open("lesson_maths-eduqas_probability-statistics-L01.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("written. top keys:", list(pd.keys()))
print("bronze n=%d silver n=%d gold n=%d" % (len(pb["bronze"]),len(pb["silver"]),len(pb["gold"])))
