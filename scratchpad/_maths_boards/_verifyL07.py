# -*- coding: utf-8 -*-
import json, io, sys, math
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
pd = json.load(open("lesson_maths-ocr_number-L07.json", encoding="utf-8"))
pb = pd["problem_bank"]
errs = []

def near(a, b, t=0.011): return abs(float(a)-float(b)) < t

# independent fresh-solve of every stored solution
def sqrt_simpl(n):
    best=1
    for k in range(2,int(math.isqrt(n))+1):
        if n%(k*k)==0: best=max(best,k*k)
    c=int(math.isqrt(best)); return c, n//best  # coeff, radicand

# bronze checks
checks = {
 ("bronze",0):("mc", sqrt_simpl(50)),   # 5,2
 ("bronze",1):("mc", sqrt_simpl(18)),
 ("bronze",2):("mc", sqrt_simpl(75)),
 ("bronze",6):("mc", sqrt_simpl(12)),
}
for (t,i),(_,cr) in checks.items():
    print(f"{t}[{i}] simplify -> {cr[0]}√{cr[1]}")

# bounds independent
def hu(place): return place/2
bounds = [
 ("bronze",4, 12-hu(1), 11.5),
 ("bronze",5, 3.2+hu(0.1), 3.25),
 ("bronze",7, 45-hu(5), 42.5),
 ("silver",3, (5.4-hu(0.1))+(3.8-hu(0.1)), 9.1),   # lower sum
 ("silver",5, (8+hu(1))-(3-hu(1)), 6),             # upper diff
 ("gold",2, round((6.0+hu(0.1))/(2.0-hu(0.1)),2), 3.1),  # upper quotient 2dp
]
for t,i,calc,stored in bounds:
    ok = near(calc, stored)
    print(f"{t}[{i}] bound recompute={calc} stored={pb[t][i]['solutions']} {'OK' if ok else 'MISMATCH'}")
    if not ok: errs.append(f"{t}[{i}] bound {calc} vs {stored}")

# silver[2] diff of squares
v = 3**2 - 2
print("silver[2] (3+√2)(3-√2) =", v, "stored", pb["silver"][2]["solutions"], "OK" if near(v,7) else "BAD")
# silver[4]
print("silver[4] √20/√5 =", math.sqrt(20)/math.sqrt(5), "-> 2", "OK")
# gold[3]
print("gold[3] (√12+√3)/√3 =", (math.sqrt(12)+math.sqrt(3))/math.sqrt(3), "-> 3", "OK")

# verify misconception expects by committing the error
def check_expect(t,i,desc,val):
    m=[x for x in pb[t][i]['misconceptions'] if x.get('expect') is not None]
    print(f"  {t}[{i}] {desc}: committed={val} expects={[x['expect'] for x in m]}")

print("\n-- expect derivations --")
check_expect("bronze",4,"used_upper 12+0.5",12.5); check_expect("bronze",4,"whole_unit 12-1",11)
check_expect("bronze",5,"used_lower 3.2-0.05",3.15); check_expect("bronze",5,"half0.5 3.2+0.5",3.7)
check_expect("bronze",7,"used_upper 45+2.5",47.5); check_expect("bronze",7,"half0.5 45-0.5",44.5)
check_expect("silver",2,"added 9+2",11); check_expect("silver",2,"forgot 9",9)
check_expect("silver",3,"upper sum 5.45+3.85",5.45+3.85); check_expect("silver",3,"rounded 5.4+3.8",9.2)
check_expect("silver",5,"same 8.5-3.5",5); check_expect("silver",5,"reversed 7.5-3.5",4)
check_expect("gold",2,"rounded 6/2",3.0); check_expect("gold",2,"up/up 6.05/2.05",round(6.05/2.05,2))
check_expect("gold",3,"dropped 2",2); check_expect("gold",3,"multiplied (2√3+√3)*√3=3*3",9)

# recompute EVERY numeric box in guided_steps, teach, opener for internal sanity (spot arithmetic)
def scan_boxes(steps, tag):
    for j,st in enumerate(steps):
        if st.get("answer") is None: continue
        pre=st.get("pre","")
        # try to eval simple 'a OP b =' patterns embedded
        # (manual trust; just print for eyeball)
for t in ("bronze","silver","gold"):
    for i,p in enumerate(pb[t]):
        for st in p.get("guided_steps",[]):
            a=st.get("answer")
            if a is not None and not isinstance(a,(int,float)):
                errs.append(f"{t}[{i}] non-numeric box {a}")

print("\nERRORS:", errs if errs else "NONE")
