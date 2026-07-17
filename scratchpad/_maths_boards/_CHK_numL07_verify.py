import math
def sf(x,n):
    if x==0: return 0.0
    from decimal import Decimal
    d=round(x, -int(math.floor(math.log10(abs(x))))+(n-1))
    return d
# gold[2] perimeter lower bound
print("gold2 LB perim", 2*(12.35+5.75), "exp 36.2; misc used_rounded", 2*(12.4+5.8))
# gold[4] speed upper bound 3sf
v=245/8.35; print("gold4 vmax", v, "3sf", sf(v,3), "; misc 245/8.45=", 245/8.45, "3sf", sf(245/8.45,3))
# worked example gold area
print("WE area", 8.35*3.65)
# 81^(3/4)
print("81^3/4", 81**0.75)
# check all bronze/silver bank solutions by recompute
checks = {
 "b0 27^1/3":27**(1/3),"b1 16^3/4":16**0.75,"b2 5^-2 denom":5**2,
 "b3 sqrt50 a":math.sqrt(50)/math.sqrt(2),"b4 sqrt8 a":math.sqrt(8)/math.sqrt(2),
 "b5 lb6.5":6.5-0.05,"b6 ub340":340+5,"b7 sqrt108 a":math.sqrt(108)/math.sqrt(3),
 "s0 x n":5+3-2,"s1 coef 2^4":2**4,"s2 sqrt12+27 a":(math.sqrt(12)+math.sqrt(27))/math.sqrt(3),
 "s3 6/sqrt2 a":6/2,"s4 81^-3/4 n":81**0.75,"s5 ub4.6":4.6+0.05,
 "s6 sqrt8*6 a":math.sqrt(48)/math.sqrt(3),
 "g0 denom":9-2,"g1 a":5-6,"g3":(math.sqrt(20)+math.sqrt(5))/math.sqrt(5),
}
for k,v in checks.items(): print(k, round(v,6))
