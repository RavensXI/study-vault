# -*- coding: utf-8 -*-
import math

print("=== GOLD[1] Newton-Raphson (2x^3+5)/(3x^2), x0=2, x2 to 3dp ===")
def nr(x, a=5):
    return (2*x**3 + a)/(3*x**2)
x0=2.0
x1=nr(x0); x2=nr(x1)
print("x1=",x1,"x2=",round(x2,3))  # expect 1.711

print("\n-- misconception 'missing_coefficient' expect 1.119, error: numerator x^3+5 --")
# variant A: full wrong iteration numerator x^3+5
def wrongA(x,a=5): return (x**3+a)/(3*x**2)
xa1=wrongA(x0); xa2=wrongA(xa1)
print("A full-wrong x2 =", round(xa2,3))
# variant B: correct x1=1.75 then wrong numerator at x2
def x2_from(x1val): return (x1val**3+5)/(3*x1val**2)
print("B keep x1=1.75, wrong x2 =", round(x2_from(1.75),3))
# variant C: drop 2 only denominator? numerator 2x^3+5, denom x^2
def wrongC(x): return (2*x**3+5)/(x**2)
xc1=wrongC(x0); xc2=wrongC(xc1)
print("C denom x^2 x2 =", round(xc2,3))
# search: what single-formula fixed-point / iterate gives 1.119?
# try (x^3+5)/(3x^2) many iterations
xx=2.0
for i in range(8): xx=wrongA(xx)
print("A converged:", round(xx,4))

print("\n=== SVG checks ===")
print("-- gold[3] trapezium y=x^2, viewBox 0 0 250 175, axis y from 18..155, x-axis at y=155 --")
# baseline y=155, x0=0 at x-pixel 45, x=4 at pixel 225 => 45 + x*45
# heights 0,1,4,9,16 -> pixel y = 155 - h*scale. At h=16 pixel=20 => scale=(155-20)/16=8.4375
scale=(155-20)/16
for h in [0,1,4,9,16]:
    print(f"  h={h}: y-pixel={155-h*scale}")
# polygons listed: strip from x=0..1: points 45,155 45,155 90,146.6 90,155
# top-left height at x=0 -> y=155 (h=0), top-right x=1 -> h=1 -> y=155-8.4375=146.5625 ~146.6 OK
# strip1..2: 90,155 90,146.6 135,121.2 135,155  -> x=1 h=1 146.6, x=2 h=4 ->155-33.75=121.25~121.2 OK
# strip2..3: 135,121.2 180,79.1 -> x=3 h=9 ->155-75.9375=79.06~79.1 OK
# strip3..4: 180,79.1 225,20 -> x=4 h=16 -> 20 OK
print("  polygon tops match heights 0,1,4,9,16 -> OK")

print("\n-- bronze[0] distance-time to (4,80), line 40,135 -> 215,20 --")
# origin pixel (40,135); endpoint (4,80). x=4 -> 215 => x scale (215-40)/4=43.75/...
# y: 80 -> 20 => baseline 135, top 20 => scale=(135-20)/80=1.4375; endpoint y=135-80*1.4375=135-115=20 OK
print("  endpoint 215,20 consistent; label 80 and 4 OK")

print("\n-- bronze[4] speed-time horizontal at 12 for 8s, line y=48.8 from 40 to 210 --")
# y for speed 12: baseline 135, need scale. text '12' at y~53 near line 48.8. Just constant line, accel=0. label 12 and 8 present.
print("  horizontal line, accel 0, labels 12 & 8 OK")
