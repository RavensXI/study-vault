# -*- coding: utf-8 -*-
import json, re

LIVE = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_CHK_rpL02_live.json"
pd = json.load(open(LIVE, encoding="utf-8"))["practice_data"]
pb = pd["problem_bank"]

issues = []

def approx(a, b, tol=0.01):
    try:
        return abs(float(a) - float(b)) <= tol
    except Exception:
        return False

# ---- 1. Fresh solve each bank problem (independent formulas) ----
# I encode the correct answer independently per problem.
expected = {
  ("gold",0): 3244.8,   # 3000*1.04^2
  ("gold",1): 10222,    # round(15000*0.88^3)
  ("gold",2): 1000,     # 1102.5/1.1025
  ("gold",3): 5,        # first year below 7000
  ("gold",4): 61.8,     # 500*1.06^2 - 500
  ("bronze",0): 220,    # 200*1.1
  ("bronze",1): 120,    # 150*0.8
  ("bronze",2): 15,     # 0.25*60
  ("bronze",3): 36,     # 40*0.9
  ("bronze",4): 1.05,
  ("bronze",5): 0.7,
  ("bronze",6): 20,     # 10/50*100
  ("bronze",7): 450,    # 300*1.5
  ("silver",0): round(510/1.15,2),  # 443.48
  ("silver",1): 150,    # 1000*0.05*3
  ("silver",2): 10800,  # 12000*0.9
  ("silver",3): 70,     # 56/0.8
  ("silver",4): 5100,   # 5000*1.02
  ("silver",5): 576,    # 480*1.2
  ("silver",6): 20,     # 16/80*100
}
# verify my independent compute matches expected literals too
assert round(510/1.15,2)==443.48
assert round(15000*0.88**3)==10222
assert round(500*1.06**2-500,2)==61.8

for (tier,i),ans in expected.items():
    stored = pb[tier][i]["solutions"]
    if not (len(stored)==1 and approx(stored[0], ans)):
        issues.append(f"{tier}[{i}] SOLUTION mismatch: stored {stored} vs computed {ans} | display: {pb[tier][i]['display']}")

# non-calc must be clean (integer or terminating simple)
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        if p.get("calculator") is False:
            for s in p["solutions"]:
                if abs(s-round(s))>1e-9:
                    # allow .05 etc? flag anything non-integer on non-calc
                    issues.append(f"{tier}[{i}] non-calc has non-integer solution {s}")

# ---- 2. Recompute every guided_steps box: walk continuity & land on solution ----
def check_walk(tier, i, steps, sol):
    boxes = [s for s in steps if "answer" in s]
    if not boxes:
        return
    # final box or the solution-bearing box should equal solution somewhere
    # check every box answer is a number
    for j,s in enumerate(steps):
        if "answer" in s and not isinstance(s["answer"], (int,float)):
            issues.append(f"{tier}[{i}].guided_steps[{j}] answer not numeric: {s['answer']}")

# We independently recompute each box using the pre text - done manually below via a table.
box_expected = {
 # gold
 ("gold",0): [1.04, 1.0816, 3244.8, 244.8],
 ("gold",1): [0.88, 0.681472, 10222.08, 10222],
 ("gold",2): [1.05, 1.1025, 1000, 1102.5],
 ("gold",3): [0.97, 7082, 6870, 5],
 ("gold",4): [1.06, 1.1236, 561.8, 61.8],
 # bronze
 ("bronze",0): [1.1, 220, 20],
 ("bronze",1): [0.8, 120, 30],
 ("bronze",2): [0.25, 15, 60],
 ("bronze",3): [0.9, 36, 4],
 ("bronze",4): [0.05, 1.05, 5],
 ("bronze",5): [0.3, 0.7, 30],
 ("bronze",6): [10, 0.2, 20, 60],
 ("bronze",7): [1.5, 450, 150],
 # silver
 ("silver",0): [1.15, 443.48, 510],
 ("silver",1): [50, 150, 1150],
 ("silver",2): [0.9, 10800, 1200],
 ("silver",3): [0.8, 70, 56],
 ("silver",4): [1.02, 5100, 100],
 ("silver",5): [1.2, 576, 96],
 ("silver",6): [16, 0.2, 20, 64],
}
# recompute independently
recompute = {
 ("gold",0): [1+0.04, round((1.04)**2,4), round(3000*1.0816,2), round(3000*1.0816-3000,2)],
 ("gold",1): [1-0.12, round(0.88**3,6), round(15000*0.88**3,2), round(15000*0.88**3)],
 ("gold",2): [1+0.05, round(1.05**2,4), round(1102.5/1.1025,2), round(1000*1.1025,2)],
 ("gold",3): [1-0.03, round(8000*0.97**4), round(8000*0.97**5), 5],
 ("gold",4): [1+0.06, round(1.06**2,4), round(500*1.1236,2), round(500*1.1236-500,2)],
 ("bronze",0): [1+0.10, round(200*1.1,2), round(220-200,2)],
 ("bronze",1): [1-0.20, round(150*0.8,2), round(150-120,2)],
 ("bronze",2): [round(25/100,2), round(0.25*60,2), 15*4],
 ("bronze",3): [1-0.10, round(40*0.9,2), 40-36],
 ("bronze",4): [round(5/100,2), round(1+0.05,2), round((1.05-1)*100)],
 ("bronze",5): [round(30/100,2), round(1-0.3,2), round((1-0.7)*100)],
 ("bronze",6): [60-50, round(10/50,2), round(0.2*100), round(50*1.2,2)],
 ("bronze",7): [1+0.50, round(300*1.5,2), 450-300],
 ("silver",0): [1+0.15, round(510/1.15,2), round(443.48*1.15)],
 ("silver",1): [round(1000*0.05,2), 50*3, 1000+150],
 ("silver",2): [1-0.10, round(12000*0.9,2), 12000-10800],
 ("silver",3): [1-0.20, round(56/0.8,2), round(70*0.8,2)],
 ("silver",4): [1+0.02, round(5000*1.02,2), 5100-5000],
 ("silver",5): [1+0.20, round(480*1.2,2), 576-480],
 ("silver",6): [80-64, round(16/80,2), round(0.2*100), round(80*0.8,2)],
}

for key in box_expected:
    tier,i = key
    steps = pb[tier][i]["guided_steps"]
    boxes = [s["answer"] for s in steps if "answer" in s]
    exp = box_expected[key]
    rec = recompute[key]
    # first check my box_expected equals my independent recompute
    for a,b in zip(exp,rec):
        if not approx(a,b):
            issues.append(f"SELFCHECK {key}: table {a} vs recompute {b}")
    if len(boxes)!=len(exp):
        issues.append(f"{tier}[{i}] box count {len(boxes)} != expected {len(exp)}: stored {boxes}")
        continue
    for j,(got,want) in enumerate(zip(boxes,exp)):
        if not approx(got,want):
            issues.append(f"{tier}[{i}].guided_steps box#{j} stored {got} vs computed {want}")

# ---- 3. Reproduce every misconception expect ----
misc_expected = {
 ("gold",0): {"simple_not_compound": 3000+2*(0.04*3000)},          # 3240
 ("gold",1): {"simple_not_compound": 15000*(1-0.36)},              # 9600
 ("gold",2): {"undid_one_year": round(1102.5/1.05,2)},            # 1050
 ("gold",3): {"off_by_one": 4},
 ("gold",4): {"gave_total_not_interest": 561.8, "simple_not_compound": 2*(0.06*500)}, # 561.8, 60
 ("bronze",0): {"part_not_total": 0.10*200},   # 20
 ("bronze",1): {"part_not_total": 0.20*150},   # 30
 ("bronze",2): {"took_off_instead_of_found": 60*0.75}, # 45
 ("bronze",3): {"gave_discount_not_price": 0.10*40},   # 4
 ("bronze",4): {"decimal_not_multiplier": 0.05},
 ("bronze",5): {"decimal_not_multiplier": 0.3},
 ("bronze",6): {"gave_difference_not_percent": 10, "divided_by_new": round(10/60*100,2)}, # 10, 16.67
 ("bronze",7): {"part_not_total": 0.50*300},   # 150
 ("silver",0): {"subtracted_from_final": round(510*0.85,2)},       # 433.5
 ("silver",1): {"one_year_only": 50, "gave_total_not_interest": 1150},
 ("silver",2): {"gave_loss_not_value": 0.10*12000}, # 1200
 ("silver",3): {"added_to_final": round(56*1.2,2)}, # 67.2
 ("silver",4): {"part_not_total": 0.02*5000},   # 100
 ("silver",5): {"gave_vat_not_total": 0.20*480}, # 96
 ("silver",6): {"gave_difference_not_percent": 16, "divided_by_new": round(16/64*100,2)}, # 16, 25
}
for (tier,i),mp in misc_expected.items():
    stored = {m["pattern"]: m.get("expect") for m in pb[tier][i].get("misconceptions",[])}
    for pat,want in mp.items():
        if pat not in stored:
            issues.append(f"{tier}[{i}] misconception pattern '{pat}' missing")
        elif not approx(stored[pat], want):
            issues.append(f"{tier}[{i}] misconception '{pat}' expect {stored[pat]} vs computed {want}")

# ---- 4. Completion boundary: >=1 before phase, >=2 live boxes at/after ----
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        steps = p.get("guided_steps")
        if not steps: continue
        phase_idx = next((k for k,s in enumerate(steps) if s.get("phase")=="substitute"), None)
        if phase_idx is None:
            issues.append(f"{tier}[{i}] no phase:substitute boundary")
            continue
        boxes_before = sum(1 for s in steps[:phase_idx] if "answer" in s)
        boxes_after = sum(1 for s in steps[phase_idx:] if "answer" in s)
        if boxes_before < 1:
            issues.append(f"{tier}[{i}] <1 box before boundary")
        if boxes_after < 2:
            issues.append(f"{tier}[{i}] only {boxes_after} live box(es) at/after boundary")

# ---- 5. Em dash & style scan on student-facing strings ----
def walk_strings(obj, path=""):
    if isinstance(obj, dict):
        for k,v in obj.items():
            if k == "note":  # internal exempt
                continue
            yield from walk_strings(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for idx,v in enumerate(obj):
            yield from walk_strings(v, f"{path}[{idx}]")
    elif isinstance(obj, str):
        yield path, obj

for path, s in walk_strings(pd):
    if "—" in s:  # em dash
        issues.append(f"EM DASH at {path}: {s[:60]}")

# ---- Report ----
print("ISSUES:", len(issues))
for x in issues:
    print(" -", x)
if not issues:
    print("ALL CLEAN")
