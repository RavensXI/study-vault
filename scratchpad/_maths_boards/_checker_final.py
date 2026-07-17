from fractions import Fraction as F
# Independent fresh-solve of every problem + expect reproduction
checks = []
def rec(label, got, exp):
    checks.append((label, got==exp, got, exp))

# BRONZE
rec("b0 P(red 2/8)", F(2,2+8), F(1,5)); rec("b0 exp red/blue", F(2,8), F(1,4))
rec("b1 P(even)", F(3,6), F(1,2)); rec("b1 exp only2,4", F(2,6), F(1,3))
rec("b2 P(heart)", F(13,52), F(1,4))
rec("b3 P(not rain)", 1-0.3, 0.7); rec("b3 exp gave rain", 0.3, 0.3)
rec("b4 P(blue)", F(3,8), F(3,8)); rec("b4 exp blue/red", F(3,5), F(3,5))
rec("b5 P(>=3 of5)", F(3,5), F(3,5)); rec("b5 exp excl3", F(2,5), F(2,5))
rec("b6 P(not green)", F(8,10), F(4,5)); rec("b6 exp green", F(2,10), F(1,5))
rec("b7 P(<3)", F(2,6), F(1,3)); rec("b7 exp incl3", F(3,6), F(1,2))
# SILVER
rec("s0 exactly1H", F(2,4), F(1,2)); rec("s0 exp one order", F(1,4), F(1,4))
rec("s1 both red WITH", F(5,8)*F(5,8), F(25,64)); rec("s1 exp WO", F(5,8)*F(4,7), F(5,14)); rec("s1 exp single", F(5,8), F(5,8))
rec("s2 both red WO", F(5,8)*F(4,7), F(5,14)); rec("s2 exp WITH", F(5,8)*F(5,8), F(25,64))
rec("s3 A and B", round(0.4*0.3,2), 0.12); rec("s3 exp add", round(0.4+0.3,2), 0.7)
rec("s4 total7", F(6,36), F(1,6)); rec("s4 exp unordered", F(3,36), F(1,12))
rec("s5 not A", round(1-0.6,2), 0.4); rec("s5 exp gave A", 0.6, 0.6)
rec("s6 one of each 6/4", 2*F(6,10)*F(4,9), F(8,15)); rec("s6 exp one path", F(6,10)*F(4,9), F(4,15))
# GOLD
rec("g0 all red 3draw", F(8,12)*F(7,11)*F(6,10), F(14,55)); rec("g0 exp 2draw", F(8,12)*F(7,11), F(14,33))
rec("g1 at least one", round(1-0.7*0.6,2), 0.58); rec("g1 exp add", round(0.3+0.4,2),0.7); rec("g1 exp comp", round(0.7*0.6,2),0.42)
rec("g2 all heads", F(1,2)**3, F(1,8)); rec("g2 exp 2coins", F(1,2)**2, F(1,4))
rec("g3 exactly2H", F(3,8), F(3,8)); rec("g3 exp 1arr", F(1,8), F(1,8))
rec("g4 both blue 7/5", F(5,12)*F(4,11), F(5,33)); rec("g4 exp WITH", F(5,12)*F(5,12), F(25,144))

bad=[c for c in checks if not c[1]]
for l,ok,g,e in checks:
    if not ok: print("FAIL", l, "got",g,"exp",e)
print(f"\n{len(checks)-len(bad)}/{len(checks)} independent solves+expects match")
print("RESULT:", "ALL PASS" if not bad else f"{len(bad)} FAIL")
