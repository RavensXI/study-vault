# -*- coding: utf-8 -*-
import math, sys
sys.stdout.reconfigure(encoding="utf-8")
def r(v,n): return round(v,n)
def disc(a,b,c): return b*b-4*a*c
def roots(a,b,c):
    d=disc(a,b,c); s=math.sqrt(d)
    return ((-b+s)/(2*a),(-b-s)/(2*a))

print("gold0 x^2+4x+1 cts n:", "(x+2)^2=", -(-4+1), "-> n=3")  # (x+2)^2 -3=0
print("gold1 k^2=4*9=",4*9,"k=",math.sqrt(36))
print("gold2 2(x+3)^2, q=-2*9+5=",-2*9+5)
print("gold3 5x^2-2x-1 disc=",disc(5,-2,-1),"sqrt=",r(math.sqrt(24),3),"posroot=",r((2+math.sqrt(24))/10,3))
print("gold4 4ac=",4*2*8,"sqrt64=8 largest int p<8 =7")
print("bronze1 x^2+2x-8 pos root=",roots(1,2,-8))
print("bronze3 x^2-4x+3 roots=",roots(1,-4,3))
print("bronze7 x^2+6x+5 roots=",roots(1,6,5))
print("silver0 x^2+3x-7 disc=",disc(1,3,-7),"sqrt=",r(math.sqrt(37),2),"pos=",r((-3+math.sqrt(37))/2,2))
print("silver3 2x^2-5x+1 disc=",disc(2,-5,1),"sqrt=",r(math.sqrt(17),2),"larger=",r((5+math.sqrt(17))/4,2),"smaller=",r((5-math.sqrt(17))/4,2))
print("silver4 3x^2+2x-4 disc=",disc(3,2,-4),"sqrt=",r(math.sqrt(52),2),"pos=",r((-2+math.sqrt(52))/6,2))
print("silver6 4x^2-12x+9 disc=",disc(4,-12,9))
print("method 2x^2+3x-5 roots=",roots(2,3,-5))
# expect checks for calculator
print("silver0 plus_b (3+sqrt37)/2=",r((3+math.sqrt(37))/2,2))
print("silver3 div2 (5+sqrt17)/2=",r((5+math.sqrt(17))/2,2),"took_smaller",r((5-math.sqrt(17))/4,2))
print("silver4 div2 (-2+sqrt52)/2=",r((-2+math.sqrt(52))/2,2))
print("gold3 div2 (2+sqrt24)/2=",r((2+math.sqrt(24))/2,2))
print("bronze7 plus_b roots with +6:",(6+4)/2,(6-4)/2)
