from fractions import Fraction as F
# Reproduce each expect by committing the error; compare to stored expect.
# Format: (label, computed_pair_or_None, stored)
def pair(fr):
    return [fr.numerator, fr.denominator]
checks=[]
# gold0 combine_across: (2+3-1)/(3+4-6)
checks.append(("gold0 combine_across",[2+3-1,3+4-6],[4,1]))
# gold0 no_simplify: 15/12 unsimplified
checks.append(("gold0 no_simplify",[15,12],[15,12]))
# gold1 ignore_whole: null
# gold2 split_no_borrow: wholes 3-1=2 ; parts 2/3-1/4=5/12 -> 2+5/12=29/12
g2=2+F(2,3)-F(1,4)
checks.append(("gold2 split_no_borrow",pair(g2),[29,12]))
# gold3 no_flip: 3/8*9/16
checks.append(("gold3 no_flip",pair(F(3,8)*F(9,16)),[27,128]))
# gold4 order_error: 5/6*(3/10+1/4)
checks.append(("gold4 order_error",pair(F(5,6)*(F(3,10)+F(1,4))),[11,24]))
# bronze0 add_denominators (1+1)/(4+3)
checks.append(("bronze0 add_denom",[2,7],[2,7]))
# bronze1 add_denom (3+1)/(5+5)
checks.append(("bronze1 add_denom",[4,10],[4,10]))
# bronze2 subtract_across (5-1)/(6-3)
checks.append(("bronze2 sub_across",[4,3],[4,3]))
# bronze2 no_simplify 3/6
checks.append(("bronze2 no_simplify",[3,6],[3,6]))
# bronze3 add_denom (2+3)/(7+7)
checks.append(("bronze3 add_denom",[5,14],[5,14]))
# bronze5 no_simplify 6/8
checks.append(("bronze5 no_simplify",[6,8],[6,8]))
# bronze6 no_simplify 10/30
checks.append(("bronze6 no_simplify",[10,30],[10,30]))
# bronze7 add_denom (1+1)/(2+6)
checks.append(("bronze7 add_denom",[2,8],[2,8]))
# bronze7 no_simplify 4/6
checks.append(("bronze7 no_simplify",[4,6],[4,6]))
# silver0 add_denom (2+5)/(3+8)
checks.append(("silver0 add_denom",[7,11],[7,11]))
# silver1 no_scale 3/20-2/20=1/20
checks.append(("silver1 no_scale",[3-2,20],[1,20]))
# silver2 no_simplify 30/45
checks.append(("silver2 no_simplify",[30,45],[30,45]))
# silver3 no_flip 4/5*2/3
checks.append(("silver3 no_flip",pair(F(4,5)*F(2,3)),[8,15]))
# silver4 ignore_whole 1/3+2/5
checks.append(("silver4 ignore_whole",pair(F(1,3)+F(2,5)),[11,15]))
# silver6 no_scale 7/20-1/20=6/20
checks.append(("silver6 no_scale",[7-1,20],[6,20]))

bad=0
for label,comp,stored in checks:
    ok = comp==stored
    if not ok: bad+=1
    print(("OK " if ok else "XX ")+label+f"  computed={comp} stored={stored}")
print("\nEXPECT MISMATCHES:",bad)
