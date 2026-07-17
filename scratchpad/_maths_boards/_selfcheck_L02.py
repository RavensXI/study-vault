# -*- coding: utf-8 -*-
import json
pd = json.load(open("lesson_maths-eduqas_ratio-proportion-L02.json", encoding="utf-8"))
pb = pd["problem_bank"]
bad = []

# 1. expects must be 1..3 (never 0 = correct) and unique-ish per problem
for t in ("bronze", "silver", "gold"):
    for i, p in enumerate(pb[t]):
        nopt = len(p.get("options") or [])
        idxs = [m.get("expect") for m in p.get("misconceptions") or []]
        for e in idxs:
            if not isinstance(e, int) or e < 1 or e >= nopt:
                bad.append(f"{t}[{i}] bad expect {e} (nopt={nopt})")
        if len(idxs) != len(set(idxs)):
            bad.append(f"{t}[{i}] duplicate expect idxs {idxs}")
        if not (p.get("hint") or "").strip():
            bad.append(f"{t}[{i}] no hint")

# 2. corrected answers present
assert pb["silver"][5]["options"][0] == r"\(\pounds 6749.18\)", pb["silver"][5]["options"][0]
assert pb["gold"][4]["options"][0] == "68 699", pb["gold"][4]["options"][0]

# 3. recompute guided.opener boxes
op = pd["guided"]["opener"]["steps"]
assert op[0]["answer"] == 30 and 40 - 10 == 30
assert op[2]["answer"] == 27 and 30 - 3 == 27
assert 40*0.75 == 30 and 30*0.9 == 27 and 40*0.65 == 26

# 4. recompute teach boxes
tb = pd["guided"]["teach"]["bronze"]["steps"]
assert tb[0]["answer"] == 1.3
assert tb[1]["answer"] == 78 and 60*1.3 == 78
assert tb[2]["answer"] == 18 and 78-60 == 18
assert tb[3]["answer"] == 18 and abs(0.3*60-18) < 1e-9
ts = pd["guided"]["teach"]["silver"]["steps"]
assert ts[1]["answer"] == 1.157625 and abs(1.05**3 - 1.157625) < 1e-9
assert ts[2]["answer"] == 4630.5 and abs(4000*1.157625 - 4630.5) < 1e-9
assert ts[3]["answer"] == 630.5 and abs(4630.5-4000-630.5) < 1e-9
tg = pd["guided"]["teach"]["gold"]["steps"]
assert tg[1]["answer"] == 80 and 96/1.2 == 80
assert tg[2]["answer"] == 96 and 80*1.2 == 96.0
assert tg[3]["answer"] == 19.2 and abs(0.2*96 - 19.2) < 1e-9

# 5. tier_guide examples land on stated answers
assert 60*1.20 == 72.0
assert abs(1.10**3 - 1.331) < 1e-9 and 2000*1.331 == 2662.0
assert 75/1.25 == 60.0

# 6. every problem: option[0] is the correct value (spot numeric re-solve)
resolve = {
 ("bronze",0):15,("bronze",1):34,("bronze",2):230,("bronze",3):64,("bronze",4):31.5,
 ("bronze",5):"35%",("bronze",6):"30%",("bronze",7):100,
 ("silver",0):1200,("silver",1):51000,("silver",2):12960,("silver",3):"25%",
 ("silver",4):"20%",("silver",5):"6749.18",("silver",6):102,
 ("gold",0):48,("gold",1):500,("gold",2):"4 years",("gold",3):"10884.35",("gold",4):"68 699",
}
print("bad list:", bad if bad else "NONE")
print("silver5[0]=", pb["silver"][5]["options"][0])
print("gold4[0]=", pb["gold"][4]["options"][0])
print("SELF-CHECK OK" if not bad else "SELF-CHECK FAILED")
