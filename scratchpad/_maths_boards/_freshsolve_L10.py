# -*- coding: utf-8 -*-
# Independent fresh-solve of the AQA L10 raw bank to catch diseases.
import math

def solve_line_parab(lx, lc, qx, qc):
    # y=lx*x+lc ; y=x^2+qx*x+qc -> x^2 + (qx-lx)x + (qc-lc)=0
    B, C = qx - lx, qc - lc
    disc = B*B - 4*C
    r = math.isqrt(disc) if disc >= 0 and int(math.isqrt(disc))**2 == disc else None
    if r is None:
        return ("nonint", B, C, disc)
    x1 = (-B + r)//2 if (-B + r) % 2 == 0 else (-B+r)/2
    x2 = (-B - r)//2 if (-B - r) % 2 == 0 else (-B-r)/2
    return sorted([x1, x2])

def solve_circle(lx, lc, r2):
    # x^2 + (lx x + lc)^2 = r2 -> (1+lx^2)x^2 + 2 lx lc x + (lc^2 - r2)=0
    a = 1 + lx*lx; b = 2*lx*lc; c = lc*lc - r2
    disc = b*b - 4*a*c
    sq = math.isqrt(disc) if disc>=0 and int(math.isqrt(disc))**2==disc else math.sqrt(disc)
    x1 = (-b + sq)/(2*a); x2 = (-b - sq)/(2*a)
    return sorted([x1, x2])

print("BRONZE raw:")
print(" b0 y=x,y=x^2:", solve_line_parab(1,0,0,0))
print(" b1 y=3,y=x^2-1:", solve_line_parab(0,3,0,-1))
print(" b2 y=x+2,y=x^2:", solve_line_parab(1,2,0,0))
print(" b3 y=2x,y=x^2+x:", solve_line_parab(2,0,1,0))
print(" b4 y=5,y=x^2+1:", solve_line_parab(0,5,0,1))
print(" b5 y=x+6,y=x^2+2x:", solve_line_parab(1,6,2,0))
print(" b6 y=7,y=x^2-2:", solve_line_parab(0,7,0,-2))
print("SILVER raw:")
print(" s0 y=x+3,y=x^2+1:", solve_line_parab(1,3,0,1))
print(" s1 y=x+1,circ13:", solve_circle(1,1,13))
print(" s2 y=x-2,circ10:", solve_circle(1,-2,10))
print(" s3 y=x+5,y=x^2+x+1:", solve_line_parab(1,5,1,1))
print(" s4 y=3x+2,y=x^2+2x-4:", solve_line_parab(3,2,2,-4))
print("GOLD raw:")
print(" g0 y=2-x,y=x^2-4:", solve_line_parab(-1,2,0,-4))
print(" g1 y=x+1,circ13:", solve_circle(1,1,13))
print(" g2 y=2x+3,y=x^2+5x+3:", solve_line_parab(2,3,5,3))
print(" g3 x+y=5,xy=6 -> y=5-x, x(5-x)=6 -> x^2-5x+6:", sorted([r for r in [2,3]]))
print(" g4 tangent y=kx+2 to y=x^2+3: x^2-kx+1=0 disc k^2-4=0 -> k=2")
print("REPLACEMENTS:")
print(" b3' y=4x,y=x^2+3:", solve_line_parab(4,0,0,3))
print(" b4' y=2x,y=x^2-3:", solve_line_parab(2,0,0,-3))
print(" g1' y=x-1,circ25:", solve_circle(1,-1,25))
