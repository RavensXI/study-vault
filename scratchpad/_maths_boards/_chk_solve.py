import math, json
pd = json.load(open("_chk_live_numberL01.json", encoding="utf-8"))
# Manually transcribe each display (LaTeX) to a correct-BIDMAS python expr
solve = {
 # bronze
 ("bronze",0): (6 + 4*3, 18),
 ("bronze",1): (20 - 8//2, 16),
 ("bronze",2): (3 + 5*2, 13),
 ("bronze",3): (24//6 + 2, 6),
 ("bronze",4): (10 - 3 + 7, 14),
 ("bronze",5): (2*5 + 4*3, 22),
 ("bronze",6): (18//3 * 2, 12),
 ("bronze",7): (14 - 8//2, 10),
 # silver
 ("silver",0): ((3+5)*4, 32),
 ("silver",1): (4**2 + 3*5, 31),
 ("silver",2): (50 - (4+6)**2, -50),
 ("silver",3): (36//(2+4) * 3, 18),
 ("silver",4): (2*(9-4)**2, 50),
 ("silver",5): (100//(5**2), 4),
 ("silver",6): (7 + 2*(8-3), 17),
 # gold
 ("gold",0): ((18+6)//(2**2) + 5*3, 21),
 ("gold",1): ((2+3)**2 - 4*(7-5), 17),
 ("gold",2): ((3**3 - 7)//(2*5), 2),
 ("gold",3): ((-3)**2 + 4*(-2), 1),
 ("gold",4): (int(math.isqrt(49)) + 2**3*3 - 8, 23),
}
bad=[]
for (t,i),(got,stored) in solve.items():
    real=pd["problem_bank"][t][i]["solutions"][0]
    if real != stored:
        bad.append(f"{t}[{i}] my-key {stored} != stored {real}")
    if got != stored:
        bad.append(f"{t}[{i}] eval {got} != {stored}")
print("SOLVE mismatches:", len(bad))
for b in bad: print(" -",b)

# teach walks + method card + tier examples + opener sanity
checks = {
 "teach.gold (20+4)/2^3+sqrt25": ((20+4)//(2**3)+math.isqrt(25), 8),
 "teach.bronze 4+7x2-3": (4+7*2-3, 15),
 "teach.silver 60-4x2^3": (60-4*2**3, 28),
 "method_card 5+2x3^2-(8/4)": (5+2*3**2-(8//4), 21),
 "tierguide.gold (8+8)/2^3+sqrt16": ((8+8)//(2**3)+math.isqrt(16), 6),
 "tierguide.bronze 18/6+5": (18//6+5, 8),
 "tierguide.silver 40-2x3^2": (40-2*3**2, 22),
 "opener box1 4+3x2": (4+3*2, 10),
 "opener box2 20-4x3": (20-4*3, 8),
 "worked_ex bronze 8+12/4x3": (8+12//4*3, 17),
 "worked_ex silver (7+3)^2/5": ((7+3)**2//5, 20),
 "worked_ex gold (18+6)/2^2+5x3": ((18+6)//(2**2)+5*3, 21),
}
for name,(got,exp) in checks.items():
    print(("OK " if got==exp else "FAIL ")+name, got, "vs", exp)
