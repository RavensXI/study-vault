# -*- coding: utf-8 -*-
import math, json, io
P = math.pi
def r1(x): return round(x, 1)

checks = []
def ck(name, got, exp):
    ok = abs(got-exp) < 0.05
    checks.append((ok, name, got, exp))

# BRONZE solutions
ck("B0 cuboid V", 6*4*3, 72)
ck("B0 mc SA", 2*(6*4+6*3+4*3), 108)
ck("B1 cube SA", 6*5**2, 150); ck("B1 mc vol", 5**3, 125)
ck("B2 prism V", 12*10, 120)
ck("B3 cyl V", r1(P*9*7), 197.9); ck("B3 mc nosquare", r1(P*3*7), 66.0)
ck("B4 h", 180/(9*5), 4); ck("B4 mc one_dim", 180/9, 20)
ck("B5 cube V", 4**3, 64); ck("B5 mc sa", 6*16, 96)
ck("B6 cyl V", r1(P*25*6), 471.2); ck("B6 mc dia", r1(P*100*6), 1885.0)
ck("B7 cuboid SA", 2*(8*3+8*2+3*2), 92); ck("B7 mc vol", 8*3*2, 48)
# SILVER
ck("S0 cone V", r1(P*25*12/3), 314.2); ck("S0 mc nothird", r1(P*25*12), 942.5)
ck("S1 sphere V", r1(4/3*P*216), 904.8); ck("S1 mc sq", r1(4/3*P*36), 150.8)
ck("S2 sphere SA", r1(4*P*16), 201.1); ck("S2 mc vol", r1(4/3*P*64), 268.1)
ck("S3 cyl h", (150-50)/10, 10); ck("S3 mc ends", 150/10, 15)
ck("S4 pyr V", 36*10/3, 120); ck("S4 mc nothird", 36*10, 360)
ck("S5 hemi V", r1(2/3*P*729), 1526.8); ck("S5 mc full", r1(4/3*P*729), 3053.6)
ck("S6 cone h", 450/25, 18); ck("S6 mc drop", 150/25, 6)
# GOLD
ck("G0 cone totSA", r1(24*P), 75.4); ck("G0 mc nobase", r1(15*P), 47.1)
ck("G1 frustum", r1((108-4)*P), 326.7); ck("G1 mc add", r1(112*P), 351.9)
ck("G2 gap", r1(250*P/3), 261.8); ck("G2 cyl", r1(250*P), 785.4); ck("G2 sphere", r1(500*P/3), 523.6); ck("G2 mc", r1(250*P), 785.4)
ck("G3 total", r1(160*P + 128*P/3), 636.7); ck("G3 cyl", r1(160*P), 502.7); ck("G3 hemi", r1(128*P/3), 134.0); ck("G3 mc full", r1(160*P + 256*P/3), 770.7)
ck("G4 r", math.sqrt(25), 5); ck("G4 mc root", 25, 25); ck("G4 mc four", math.sqrt(100), 10)
# teach/opener
ck("opener", 3*2*2, 12)
ck("teach bronze", 5*4*2, 40)
ck("teach silver cone", r1(P*36*6/3), 226.2)
ck("teach gold total", r1(72*P + 12*P), 263.9)

bad = [c for c in checks if not c[0]]
for ok,n,g,e in checks:
    print(("OK " if ok else "XX "), n, g, "vs", e)
print("\nFAILURES:", len(bad))

# check expects != solution and box finals land on solutions
pd = json.load(io.open("lesson_maths-aqa_geometry-L03.json", encoding="utf-8"))
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        sol = p["solutions"][0]
        # last box with phase substitute that is the 'answer' step -> just check a box equals sol exists
        finals = [s["answer"] for s in p["guided_steps"] if s.get("answer") is not None]
        if sol not in finals:
            print("WARN no box lands on solution", tier, i, sol, finals)
        for m in p.get("misconceptions",[]):
            if abs(float(m["expect"]) - sol) < 0.011:
                print("WARN expect==sol", tier, i, m["expect"])
print("done")
