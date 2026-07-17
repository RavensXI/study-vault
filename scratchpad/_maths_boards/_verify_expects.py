# -*- coding: utf-8 -*-
from fractions import Fraction as F
# commit each described error, confirm it equals my planned expect
checks = []
def add(tag, val, planned):
    if isinstance(val, F): got=[val.numerator, val.denominator]
    else: got=list(val)
    checks.append((tag, got, planned, got==planned))

# BRONZE
add("B1 add-both 1/4,1/3", [1+1,4+3], [2,7])
add("B2 add-both 3/5,1/10", [3+1,5+10], [4,15])
add("B3 sub-both 5/6,1/3", [5-1,6-3], [4,3])
add("B3 no-simplify 3/6", [3,6], [3,6])
add("B4 sub-both 7/8,1/4", [7-1,8-4], [6,4])
add("B5 no-simplify 6/15", [6,15], [6,15])
add("B6 no-simplify 4/14", [4,14], [4,14])
add("B7 no-flip 3/4*1/2", F(3,4)*F(1,2), [3,8])
add("B7 no-simplify 6/4", [6,4], [6,4])
add("B8 no-flip 2/5*3/5", F(2,5)*F(3,5), [6,25])
add("B8 no-simplify 10/15", [10,15], [10,15])
# SILVER
add("S1 add-both 2/3,5/8", [2+5,3+8], [7,11])
add("S2 prod-denom no-scale (5-3)/(6*8)", F(5-3,6*8), [1,24])
add("S3 add-both improper 4/3,9/4", [4+9,3+4], [13,7])
add("S4 split no-borrow 2+(2/3-1/2)", 2+(F(2,3)-F(1,2)), [13,6])
add("S5 no-simplify 24/36", [24,36], [24,36])
add("S6 whole-only 2*5/11", 2*F(5,11), [10,11])
add("S7 no-flip 7/4*7/8", F(7,4)*F(7,8), [49,32])
add("S7 no-convert 3/4÷7/8", F(3,4)/F(7,8), [6,7])
# GOLD
add("G1 combine-both (2+3-1)/(3+4-6)", F(2+3-1,3+4-6), [4,1])
add("G1 no-simplify 15/12", [15,12], [15,12])
add("G2 whole+part 2 + (2/3*1/4)", 2+(F(2,3)*F(1,4)), [13,6])
add("G2 no-simplify 40/12", [40,12], [40,12])
add("G3 no-flip 21/5*7/5", F(21,5)*F(7,5), [147,25])
add("G4 add-first 5/6÷(2/3+1/4)", F(5,6)/(F(2,3)+F(1,4)), [10,11])
add("G5 no-flip last 2/3*2/3", F(2,3)*F(2,3), [4,9])

allok=True
for tag,got,planned,ok in checks:
    if not ok: allok=False
    print(f"{'OK ' if ok else 'BAD'} {tag}: committed={got} planned={planned}")
print("ALL EXPECTS MATCH" if allok else "MISMATCH FOUND")
