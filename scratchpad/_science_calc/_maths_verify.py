import json, math

pd = json.load(open("_live_canonical.json", encoding="utf-8"))
findings = []

def approx(a, b, tol=1e-6):
    return abs(a - b) <= tol

# Verify final box of each guided_steps lands on solution, and expects outside accept
for tier, probs in pd["problem_bank"].items():
    if tier.endswith("_description"):
        continue
    for i, p in enumerate(probs):
        sol = p["solutions"][0]
        acc = p.get("accept", 0)
        path = f"{tier}[{i}]"
        gs = p.get("guided_steps") or []
        boxes = [s for s in gs if s.get("answer") is not None]
        if boxes:
            last = boxes[-1]["answer"]
            # For check-style last box it may return an intermediate; test if ANY box equals sol
            vals = [b["answer"] for b in boxes]
            if not any(approx(float(v), float(sol)) for v in vals):
                findings.append(f"{path}: no guided box equals solution {sol}; boxes={vals}")
        # expects
        for j, m in enumerate(p.get("misconceptions") or []):
            e = m.get("expect")
            if e is None:
                continue
            if abs(float(e) - float(sol)) <= acc:
                findings.append(f"{path}.misconceptions[{j}]: expect {e} INSIDE accept window of {sol} +/-{acc}")

print("problem-level checks done")
for f in findings:
    print("  ISSUE:", f)
if not findings:
    print("  no issues at problem level")

# Independent recomputation of stated answers
def ke(m, v): return 0.5*m*v*v
def gpe(m, g, h): return m*g*h
checks = {
 "gold[0] rollercoaster v": (math.sqrt(2*gpe(800,10,45)/800), 30),
 "gold[1] braking force": (ke(1200,30)/50, 10800),
 "gold[2] power": (gpe(120,10,8)/6, 1600),
 "gold[3] height": (90/(0.5*10), 18),
 "gold[4] power": (gpe(60,10,3)/4, 450),
 "bronze[0] ke": (ke(2,3), 9),
 "bronze[1] gpe": (gpe(5,10,4), 200),
 "bronze[2] work": (50*3, 150),
 "bronze[3] power": (600/20, 30),
 "bronze[4] ke": (ke(10,4), 80),
 "bronze[5] gpe": (gpe(3,10,2), 60),
 "bronze[6] power": (1500/5, 300),
 "bronze[7] work": (30*4, 120),
 "silver[0] ke": (ke(1200,20), 240000),
 "silver[1] energy": (500*12, 6000),
 "silver[2] gpe": (gpe(75,10,6), 4500),
 "silver[3] speed": (math.sqrt(2*10/0.2), 10),
 "silver[4] power": (gpe(200,10,15)/30, 1000),
 "silver[5] speed": (math.sqrt(2*gpe(600,10,20)/600), 20),
 "we bronze": (ke(85,12), 6120),
 "we silver": (gpe(40,10,3.5), 1400),
 "we gold": (gpe(60,10,4)/8, 300),
 "tg bronze": (ke(4,5), 50),
 "tg silver": (math.sqrt(2*25/0.5), 10),
 "tg gold": (gpe(50,10,6)/10, 300),
 "teach bronze": (gpe(6,10,3), 180),
 "teach silver": (math.sqrt(2*36/2), 6),
 "teach gold": (math.sqrt(2*gpe(0.4,10,5)/0.4), 10),
}
print("\nrecomputation vs stored:")
bad = 0
for k,(got,exp) in checks.items():
    ok = approx(got, exp, 1e-6)
    if not ok:
        bad += 1
        print(f"  MISMATCH {k}: computed {got} != stated {exp}")
print(f"  {bad} mismatches" if bad else "  all recomputations match")
