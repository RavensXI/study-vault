# -*- coding: utf-8 -*-
import json, math
pi = math.pi
def r(x, n): return round(x, n)

print("=== rounding-sensitive boxes ===")
checks = [
 ("silver0 check 113.1/36", r(113.1/36,1), 3.1),
 ("silver4 sector 0.25*113.1", r(0.25*113.1,1), 28.3),
 ("silver4 check 28.3*4", r(28.3*4,1), 113.2),
 ("silver5 arc 0.2*62.8", r(0.2*62.8,1), 12.6),
 ("silver5 check 12.6*5", r(12.6*5,0), 63),
 ("silver6 subtract 96-28.3", r(96-28.3,1), 67.7),
 ("gold0 semicircle 0.5*pi*36", r(0.5*pi*36,1), 56.5),
 ("gold0 check 56.5*2", r(56.5*2,0), 113),
 ("gold1 arc 0.375*50.265", r(0.375*(2*pi*8),1), 18.8),
 ("gold1 check 18.8/0.375", r(18.8/0.375,1), 50.1),
 ("gold2 circ 2pi*5", r(2*pi*5,1), 31.4),
 ("gold2 frac 10/31.416", r(10/31.416,4), 0.3183),
 ("gold2 angle 0.3183*360", r(0.3183*360,0), 115),
 ("gold2 check 0.3183*31.416", r(0.3183*31.416,0), 10),
 ("gold3 ring pi*16", r(pi*16,1), 50.3),
 ("gold3 check pi*25", r(pi*25,1), 78.5),
 ("gold4 fullcircle pi*100", r(pi*100,1), 314.2),
 ("gold4 frac 75/314.16", r(75/314.16,4), 0.2387),
 ("gold4 angle 0.2387*360", r(0.2387*360,0), 86),
 ("gold4 check 0.2387*314.16", r(0.2387*314.16,0), 75),
 ("silver0 area pi*36", r(pi*36,1), 113.1),
 ("silver2 50.3/pi", r(50.3/pi,0), 16),
 ("silver2 check pi*16", r(pi*16,1), 50.3),
 ("bronze5 pi*14", r(pi*14,1), 44),
 ("teach silver 0.5*pi*64", r(0.5*pi*64,1), 100.5),
 ("teach silver 100.5*2", r(100.5*2,0), 201),
 ("teach gold 113.097/6", r((pi*36)/6,1), 18.8),
 ("teach gold 18.8*6", r(18.8*6,1), 112.8),
]
bad=0
for name, got, exp in checks:
    ok = abs(got-exp) < 0.05
    if not ok: bad+=1
    print(f"  {'OK ' if ok else '**BAD**'} {name}: got={got} expect_in_walk={exp}")

print("\n=== misconception expects (must be wrong, must reproduce error) ===")
me = [
 ("b0 perimeter", 2*(9+4), 26, "!=36"),
 ("b1 forgot_half", 10*6, 60, "!=30"),
 ("b2 area", 8*5, 40, "!=26"),
 ("b3 halved", 7*4/2, 14, "!=28"),
 ("b4 no_average", 16*4, 64, "!=32"),
 ("b5 used_area", r(pi*49,1), 153.9, "!=44"),
 ("b5 radius_as_diam", r(pi*7,1), 22.0, "!=44"),
 ("b6 perimeter", 4*9, 36, "!=81"),
 ("b7 two_sides", 2*5, 10, "!=15"),
 ("s0 forgot_square", r(pi*6,1), 18.8, "!=113.1"),
 ("s0 used_circ", r(2*pi*6,1), 37.7, "!=113.1"),
 ("s1 used_area", r(pi*49,1), 153.9, "!=44"),
 ("s1 doubled_diam", r(2*pi*14,1), 88.0, "!=44"),
 ("s2 forgot_root", round(50.3/pi), 16, "!=4"),
 ("s2 div_2pi", r(50.3/(2*pi),1), 8.0, "!=4"),
 ("s3 no_average", 16*8, 128, "!=64"),
 ("s4 forgot_fraction", r(pi*36,1), 113.1, "!=28.3"),
 ("s5 forgot_fraction", r(2*pi*10,1), 62.8, "!=12.6"),
 ("s6 added", r(96+pi*9,1), 124.3, "!=67.7"),
 ("g0 forgot_half", r(pi*36,1), 113.1, "!=56.5"),
 ("g0 diam_as_radius", r(0.5*pi*144,1), 226.2, "!=56.5"),
 ("g1 used_area", r(0.375*pi*64,1), 75.4, "!=18.8"),
 ("g1 forgot_fraction", r(2*pi*8,1), 50.3, "!=18.8"),
 ("g2 half_circle", round(10/(2*pi*5)*180), 57, "!=115"),
 ("g3 subtracted_radii", r(pi*(5-3)**2,1), 12.6, "!=50.3"),
 ("g3 added", r(pi*25+pi*9,1), 106.8, "!=50.3"),
 ("g4 half_circle", round(75/(pi*100)*180), 43, "!=86"),
]
for name, computed, stated, note in me:
    ok = abs(computed-stated) < 0.06
    if not ok: bad+=1
    print(f"  {'OK ' if ok else '**BAD**'} {name}: committed_error={r(computed,2)} stated_expect={stated} {note}")

print("\nBAD count:", bad)
