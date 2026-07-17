# -*- coding: utf-8 -*-
import math

def r(x, d): return round(x, d)

print("=== BRONZE ===")
print("B1 (1,3),(5,11):", (11-3)/(5-1))            # 2
print("B2 (0,4),(2,10):", (10-4)/(2-0))            # 3
x=1; x=x+3; x=x+3; print("B3 x+3 x0=1 x2:", x)     # 7
x=3; x1=2*x-1; print("B4 2x-1 x0=3 x1:", x1)       # 5
print("B5 (1,-2),(5,6):", (6-(-2))/(5-1))          # 2  -> proposed (5,14):
print("   B5 alt (1,-2),(5,14):", (14-(-2))/(5-1)) # 4
x=2; x1=10/x; print("B6 10/x x0=2 x1:", x1)        # 5
x=2; x1=10/x; x2=10/x1; print("B7 10/x x0=2 x2:", x2) # 2
x=2; x1=x**2-2; print("B8 x^2-2 x0=2 x1:", x1)     # 2 -> proposed x0=4:
x=4; x1=x**2-2; print("   B8 alt x0=4 x1:", x1)    # 14

print("=== SILVER ===")
x=3; x1=(x**2+5)/(2*x); print("S1 x0=3 x1:", x1, r(x1,3))   # 2.333
x=3; x1=math.sqrt(8+x); print("S2 sqrt(8+x) x1:", x1, r(x1,3)) # 3.317
x=3; x1=math.sqrt(8+x); x2=math.sqrt(8+x1); print("S3 x2:", x2, r(x2,3)) # ??
print("   S4 pop rate 100*ln2/3:", 100*math.log(2)/3)       # ~23.1
x=2; x1=6/(x+1); print("S5 6/(x+1) x0=2 x1:", x1)           # 2
x=1; x1=(x**3+2)/(3*x**2); print("S6 x0=1 x1:", x1)         # 1
x=1; x1=5/(x+2); print("S7 5/(x+2) x0=1 x1:", x1, r(x1,3))  # 1.667

print("=== GOLD ===")
x=2
x1=(5*x+4)**(1/3); x2=(5*x1+4)**(1/3); x3=(5*x2+4)**(1/3)
print("G1 cbrt(5x+4) x0=2: x1=%.6f x2=%.6f x3=%.6f -> x3 3dp=%s"%(x1,x2,x3,r(x3,3)))
print("G2 constant of x^3-5x-4=0:", -4)
x=3; x1=(x**2+7)/(2*x); x2=(x1**2+7)/(2*x1); print("G3 x2 4dp:", x2, r(x2,4)) # 2.6458
print("G4 2.646^2:", 2.646**2)                             # ~7.001 -> x^2=7
x=3; x1=3+1/x**2; print("G5 3+1/x^2 x0=3 x1:", x1, r(x1,3)) # 3.111
