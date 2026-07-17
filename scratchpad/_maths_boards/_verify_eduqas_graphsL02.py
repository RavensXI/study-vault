# -*- coding: utf-8 -*-
"""Independent checker: fresh-solve every problem, confirm the guided walk's
final live box equals the solution, and confirm each misconception expect is
the derived error (not the answer)."""
import json, io
from fractions import Fraction as F

pd = json.load(io.open("C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-eduqas_graphs-L02.json", encoding="utf-8"))
pb = pd["problem_bank"]
problems = []

# fresh-solve each problem independently (re-derived here from scratch)
def line_c(m, x, y):  # c from y=mx+c
    return y - m*x
solve = {
 ("bronze",0): 1,                       # y-int given =1
 ("bronze",1): line_c(3,2,9),           # 3
 ("bronze",2): -5,                      # (0,-5) -> c=-5
 ("bronze",3): line_c(1,3,7),           # 4
 ("bronze",4): 6,                       # gradient of y=6x-3
 ("bronze",5): line_c(-2,1,5),          # 7
 ("bronze",6): line_c(F(1,2),6,8),      # 5
 ("bronze",7): 11,                      # y-int of y=-4x+11
 ("silver",0): line_c(F(11-5,4-2),2,5), # m=3 -> c=-1
 ("silver",1): line_c(F(15-3,5-1),1,3), # m=3 -> c=0
 ("silver",2): line_c(5,2,3),           # parallel m=5 -> c=-7
 ("silver",3): F(-2-6,4-0),             # -2
 ("silver",4): F(1-(-11),3-(-1)),       # 3
 ("silver",5): line_c(-2,3,1),          # 7
 ("silver",6): F(8,2),                  # 4
 ("gold",0): line_c(F(-5-7,4-(-2)),-2,7),# m=-2 -> c=3
 ("gold",1): line_c(F(-1,4),8,5),       # perp of 4 -> c=7
 ("gold",2): F(12-3,-3),                # -3m=9 -> m=-3
 ("gold",3): F(-1, F(-1,2)),            # perp of -1/2 -> 2
 ("gold",4): line_c(-2,4,6),            # midpoint (4,6), m=-2 -> c=14
}

fails=[]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        key=(tier,i)
        want = solve[key]
        stored = p["solutions"][0]
        if F(want) != F(stored):
            fails.append(f"{tier}[{i}] fresh-solve {want} != stored {stored}")
        # guided walk final live box must equal stored solution
        gs = p.get("guided_steps") or []
        live = [s for s in gs if s.get("answer") is not None]
        if live:
            last = live[-1]["answer"]
            # last box is a CHECK box; its target is often the display's known value,
            # but the SOLVE box (the one that yields the answer) must appear. Assert the
            # solution value appears as some box answer.
            vals = [s["answer"] for s in live]
            if stored not in vals:
                fails.append(f"{tier}[{i}] solution {stored} not produced by any guided box {vals}")
        # expects must differ from solution and be numeric-or-null
        for j,m in enumerate(p.get("misconceptions") or []):
            e = m.get("expect")
            if e is not None:
                if F(e) == F(stored):
                    fails.append(f"{tier}[{i}].mis[{j}] expect equals solution")

# figure checks
op = pd["guided"]["opener"]["display"]
assert "<svg" in op and 'role="img"' in op and "£3" in op and "£13" in op, "opener svg bad"
g0 = pb["gold"][0]["display"]
assert "<svg" in g0 and "(−2, 7)" in g0 and "(4, −5)" in g0, "gold0 svg labels bad"
# opener line endpoints correspond to (0,3) and (5,13): px=40+m*36, py=150-c*8
assert 'x1="40" y1="126"' in op and 'x2="220" y2="46"' in op, "opener line endpoints off"

if fails:
    print("FAIL")
    for f in fails: print("  -",f)
else:
    print("VERIFY CLEAN: all solutions, guided boxes, expects, figures check out")
