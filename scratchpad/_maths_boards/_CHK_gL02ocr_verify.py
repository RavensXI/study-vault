import json, math

pd = json.load(open("_CHK_gL02ocr_live.json", encoding="utf-8"))["practice_data"]
pi = math.pi
errs = []

def approx(a, b, tol=0.06):
    return abs(a-b) <= tol

# ---- fresh-solve bank ----
def r1(x): return round(x,1)

checks = []
pb = pd["problem_bank"]

# BRONZE
b = pb["bronze"]
checks.append(("bronze[0] rect9x4", 9*4, b[0]["solutions"][0]))
checks.append(("bronze[1] tri10x6", 0.5*10*6, b[1]["solutions"][0]))
checks.append(("bronze[2] perim8,5", 2*(8+5), b[2]["solutions"][0]))
checks.append(("bronze[3] para7x4", 7*4, b[3]["solutions"][0]))
checks.append(("bronze[4] trap6,10,h4", 0.5*(6+10)*4, b[4]["solutions"][0]))
checks.append(("bronze[5] circ r7 C", r1(pi*14), b[5]["solutions"][0]))
checks.append(("bronze[6] sq9", 9*9, b[6]["solutions"][0]))
checks.append(("bronze[7] equilat p5", 3*5, b[7]["solutions"][0]))

# SILVER
s = pb["silver"]
checks.append(("silver[0] circ r6 A", r1(pi*36), s[0]["solutions"][0]))
checks.append(("silver[1] circ d14 C", r1(pi*14), s[1]["solutions"][0]))
checks.append(("silver[2] circ A50.3 r", r1(math.sqrt(50.3/pi)), s[2]["solutions"][0]))
checks.append(("silver[3] trap5,11,h8", 0.5*(5+11)*8, s[3]["solutions"][0]))
checks.append(("silver[4] sector r6 90 A", r1(0.25*pi*36), s[4]["solutions"][0]))
checks.append(("silver[5] arc r10 72", r1((72/360)*2*pi*10), s[5]["solutions"][0]))
checks.append(("silver[6] rect12x8-circ r3", r1(96-pi*9), s[6]["solutions"][0]))

# GOLD
g = pb["gold"]
checks.append(("gold[0] semicirc d12 A", r1(0.5*pi*36), g[0]["solutions"][0]))
checks.append(("gold[1] sector r8 135 arc", r1((135/360)*2*pi*8), g[1]["solutions"][0]))
checks.append(("gold[2] sector r5 arc10 angle", round((10/(2*pi*5))*360), g[2]["solutions"][0]))
checks.append(("gold[3] ring R5 r3", r1(pi*(25-9)), g[3]["solutions"][0]))
checks.append(("gold[4] sector A75 r10 angle", round((75/(pi*100))*360), g[4]["solutions"][0]))

for name, computed, stored in checks:
    ok = approx(float(computed), float(stored), 0.06)
    if not ok:
        errs.append(f"SOLUTION MISMATCH {name}: computed {computed} vs stored {stored}")
    print(f"{'OK ' if ok else 'BAD'} {name}: computed={computed} stored={stored}")

print("\n--- EXPECTS ---")
# expects: (path, computed_wrong, stored_expect)
E = []
E.append(("bronze[0] perimeter", 2*(9+4), 26))
E.append(("bronze[1] forgot_half", 10*6, 60))
E.append(("bronze[2] area", 8*5, 40))
E.append(("bronze[3] halved", 0.5*7*4, 14))
E.append(("bronze[4] no_average", (6+10)*4, 64))
E.append(("bronze[5] used_area", r1(pi*49), 153.9))
E.append(("bronze[5] radius_as_diam", r1(pi*7), 22.0))
E.append(("bronze[6] perimeter", 4*9, 36))
E.append(("bronze[7] two_sides", 2*5, 10))
E.append(("silver[0] forgot_square", r1(pi*6), 18.8))
E.append(("silver[0] used_circ", r1(2*pi*6), 37.7))
E.append(("silver[1] used_area r7", r1(pi*49), 153.9))
E.append(("silver[1] doubled_diameter(2pi*14)", r1(2*pi*14), 88.0))
E.append(("silver[2] forgot_root", 16, 16))
E.append(("silver[2] divided_by_2pi", r1(50.3/(2*pi)), 8.0))
E.append(("silver[3] no_average", (5+11)*8, 128))
E.append(("silver[4] forgot_fraction", r1(pi*36), 113.1))
E.append(("silver[5] forgot_fraction", r1(2*pi*10), 62.8))
E.append(("silver[6] added", r1(96+pi*9), 124.3))
E.append(("gold[0] forgot_half", r1(pi*36), 113.1))
E.append(("gold[0] diameter_as_radius", r1(0.5*pi*144), 226.2))
E.append(("gold[1] used_area", r1((135/360)*pi*64), 75.4))
E.append(("gold[1] forgot_fraction", r1(2*pi*8), 50.3))
E.append(("gold[2] half_circle(180)", round((10/(2*pi*5))*180), 57))
E.append(("gold[3] subtracted_radii", r1(pi*4), 12.6))
E.append(("gold[3] added", r1(pi*34), 106.8))
E.append(("gold[4] half_circle(180)", round((75/(pi*100))*180), 43))

for name, computed, stored in E:
    ok = approx(float(computed), float(stored), 0.06)
    if not ok:
        errs.append(f"EXPECT MISMATCH {name}: committed error gives {computed} vs stored expect {stored}")
    print(f"{'OK ' if ok else 'BAD'} {name}: computed={computed} expect={stored}")

print("\n=== ERRORS:", len(errs))
for e in errs: print(e)
