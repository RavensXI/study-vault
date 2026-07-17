# -*- coding: utf-8 -*-
import math
def r(x,d): return round(x,d)

print("OPENER machine halve+3, x0=10:")
x=10; x1=x/2+3; x2=x1/2+3
print("  x1=",x1,"x2=",x2, " fixed point x=x/2+3 ->",6)

print("BRONZE teach gradient (2,1),(6,9):")
print("  rise",9-1,"run",6-2,"grad",(9-1)/(6-2), "check 4*2=",4*2,"=>y",1+8)

print("SILVER teach (x^2+3)/(2x) x0=2 x1:")
x=2; num=x**2+3; den=2*x; x1=num/den
print("  x^2=",x**2,"num=",num,"den=",den,"x1=",x1,r(x1,3))

print("GOLD teach cbrt(7x+20) x0=1 x2:")
x=1; a=7*x+20; x1=a**(1/3); b=7*x1+20; x2=b**(1/3)
print("  7x+20=",a,"x1=cbrt(27)=",x1,"7x1+20=",b,"x2=cbrt(41)=",x2,r(x2,3))

print("=== expects verification ===")
print("B0 inv (5-1)/(11-3)=",(5-1)/(11-3))
print("B1 inv (2-0)/(10-4)=",r((2-0)/(10-4),3))
print("B4 inv (5-1)/(14-(-2))=",(5-1)/(14-(-2)))
print("S0 forgot double den (9+5)/3=",r((9+5)/3,3))
print("S1 forgot sqrt 8+3=",8+3)
print("S4 order 6/2+1=",6/2+1)
print("S6 order 5/1+2=",5/1+2)
print("G0 stop early x1=cbrt(14)=",r(14**(1/3),3))
print("G2 stop early x1=(9+7)/6=",r((9+7)/6,4))
print("G4 used 1/x not 1/x^2: 3+1/3=",r(3+1/3,3))

print("=== gold G1 full precision recompute x3 ===")
x=2
for i in range(1,4):
    x=(5*x+4)**(1/3)
    print("  x%d="%i, x, r(x,3))
