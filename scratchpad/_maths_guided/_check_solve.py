from fractions import Fraction as F
# verify each problem's stored solution
def rng_count(lo, lo_incl, hi, hi_incl):
    import math
    ints=[]
    n=math.floor(hi) if hi_incl else math.ceil(hi-1) if hi==int(hi) else math.floor(hi)
    # brute
    lo_i=math.ceil(lo) if not lo_incl or lo!=int(lo) else int(lo)
    res=[]
    x=lo_i-3
    for x in range(int(lo)-3,int(hi)+3):
        okL = (x>lo) or (lo_incl and x==lo) or x>lo
        okL = (x>lo) if not lo_incl else (x>=lo)
        okH = (x<hi) if not hi_incl else (x<=hi)
        if okL and okH: res.append(x)
    return res
print("S2 1<x+3<=6 -> -2<x<=3:", rng_count(-2,False,3,True), "count", len(rng_count(-2,False,3,True)))
print("G0 -3<2x+1<=7 -> -2<x<=3:", rng_count(-2,False,3,True), len(rng_count(-2,False,3,True)))
print("S5 2<=4x-6<10 -> 2<=x<4 smallest:", rng_count(2,True,4,False), "min", min(rng_count(2,True,4,False)))
print("G3 3n+7<25 -> n<6 largest:", rng_count(-10,False,6,False), "max", max(rng_count(-10,False,6,False)))
# spot check a few MC
print("S0 -3x>12 -> x<-4 correct")
print("S1 4-x<=7 -> x>=-3")
print("G1 (5-x)/3>=2 -> 5-x>=6 -> -x>=1 -> x<=-1")
print("G2 4(2x-3)<5x+6 -> 8x-12<5x+6 -> 3x<18 -> x<6")
print("G4 2x+1>5(x>2) & 3x-4<11(x<5) -> 2<x<5")
