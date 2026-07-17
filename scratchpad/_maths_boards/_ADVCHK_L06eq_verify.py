# -*- coding: utf-8 -*-
import json, math

pd = json.load(open("_ADVCHK_L06eq_live.json", encoding="utf-8"))
issues = []

def approx(a, b, tol=0.06):
    return abs(a-b) <= tol

def r1(x): return round(x,1)

# ---- Fresh solve each bank problem ----
def solve_report():
    pb = pd["problem_bank"]
    # BRONZE
    b = pb["bronze"]
    checks = []
    # B1 a=6,A=30,B=50 find b
    checks.append(("bronze[0]", 6*math.sin(math.radians(50))/math.sin(math.radians(30)), b[0]["solutions"][0]))
    # B2 a=10,A=45,B=65
    checks.append(("bronze[1]", 10*math.sin(math.radians(65))/math.sin(math.radians(45)), b[1]["solutions"][0]))
    # B3 a=8,A=40,b=10 find B
    checks.append(("bronze[2]", math.degrees(math.asin(10*math.sin(math.radians(40))/8)), b[2]["solutions"][0]))
    # B4 a=9,A=50,B=40
    checks.append(("bronze[3]", 9*math.sin(math.radians(40))/math.sin(math.radians(50)), b[3]["solutions"][0]))
    # B5 area 5,8,30
    checks.append(("bronze[4]", 0.5*5*8*math.sin(math.radians(30)), b[4]["solutions"][0]))
    # B6 c=15,C=80,A=35 find a
    checks.append(("bronze[5]", 15*math.sin(math.radians(35))/math.sin(math.radians(80)), b[5]["solutions"][0]))
    # B7 a=7,A=35,b=9 find B
    checks.append(("bronze[6]", math.degrees(math.asin(9*math.sin(math.radians(35))/7)), b[6]["solutions"][0]))
    # B8 area 12,7,90
    checks.append(("bronze[7]", 0.5*12*7*math.sin(math.radians(90)), b[7]["solutions"][0]))

    s = pb["silver"]
    # S1 b=7,c=10,A=60 find a
    checks.append(("silver[0]", math.sqrt(49+100-2*7*10*math.cos(math.radians(60))), s[0]["solutions"][0]))
    # S2 a=5,b=8,c=9 find A
    checks.append(("silver[1]", math.degrees(math.acos((64+81-25)/(2*8*9))), s[1]["solutions"][0]))
    # S3 area 11,14,42
    checks.append(("silver[2]", 0.5*11*14*math.sin(math.radians(42)), s[2]["solutions"][0]))
    # S4 6,8,10 largest angle opp 10
    checks.append(("silver[3]", math.degrees(math.acos((36+64-100)/(2*6*8))), s[3]["solutions"][0]))
    # S5 9,13,110 find third side
    checks.append(("silver[4]", math.sqrt(81+169-2*9*13*math.cos(math.radians(110))), s[4]["solutions"][0]))
    # S6 area 15,20,75
    checks.append(("silver[5]", 0.5*15*20*math.sin(math.radians(75)), s[5]["solutions"][0]))
    # S7 a=4,b=7,c=9 find C
    checks.append(("silver[6]", math.degrees(math.acos((16+49-81)/(2*4*7))), s[6]["solutions"][0]))

    g = pb["gold"]
    # G1 ships 10@40,15@120 angle 80
    checks.append(("gold[0]", math.sqrt(100+225-2*10*15*math.cos(math.radians(80))), g[0]["solutions"][0]))
    # G2 13,14,15 area (Heron)
    s0=21; checks.append(("gold[1]", math.sqrt(s0*(s0-13)*(s0-14)*(s0-15)), g[1]["solutions"][0]))
    # G3 PQ8,QR11,angle100 find PR
    checks.append(("gold[2]", math.sqrt(64+121-2*8*11*math.cos(math.radians(100))), g[2]["solutions"][0]))
    # G4 area30,sides10,8 find angle
    checks.append(("gold[3]", math.degrees(math.asin(2*30/(10*8))), g[3]["solutions"][0]))
    # G5 parallelogram 6,10,70
    checks.append(("gold[4]", 6*10*math.sin(math.radians(70)), g[4]["solutions"][0]))

    for path, computed, stored in checks:
        cr = round(computed, 1) if isinstance(stored,float) else round(computed)
        # decide rounding by stored type
        if isinstance(stored, int) and float(stored).is_integer():
            comp = round(computed)
        else:
            comp = round(computed,1)
        ok = approx(computed, stored, 0.06)
        print(f"{path}: computed={computed:.4f} rounded~{cr} stored={stored} {'OK' if ok else '*** MISMATCH'}")
        if not ok:
            issues.append(f"{path} solution mismatch computed {computed:.4f} vs stored {stored}")

solve_report()

# ---- Expects ----
print("\n--- EXPECTS ---")
def check_expect(path, computed, stored):
    ok = approx(computed, stored, 0.15)
    print(f"{path}: expect computed={computed:.3f} stored={stored} {'OK' if ok else '*** MISMATCH'}")
    if not ok:
        issues.append(f"{path} expect mismatch computed {computed:.3f} vs stored {stored}")

# bronze expects (inverted ratio / dropped half etc.)
check_expect("bronze[0].misc", 6*math.sin(math.radians(30))/math.sin(math.radians(50)), 3.9)
check_expect("bronze[1].misc", 10*math.sin(math.radians(45))/math.sin(math.radians(65)), 7.8)
check_expect("bronze[2].misc", math.degrees(math.asin(8*math.sin(math.radians(40))/10)), 30.9)
check_expect("bronze[3].misc", 9*math.sin(math.radians(50))/math.sin(math.radians(40)), 10.7)
check_expect("bronze[4].misc", 5*8*math.sin(math.radians(30)), 20)
check_expect("bronze[5].misc", 15*math.sin(math.radians(80))/math.sin(math.radians(35)), 25.8)
check_expect("bronze[6].misc", math.degrees(math.asin(7*math.sin(math.radians(35))/9)), 26.5)
check_expect("bronze[7].misc", 12*7*math.sin(math.radians(90)), 84)
# silver
check_expect("silver[0].misc", math.sqrt(149), 12.2)
check_expect("silver[1].misc", math.degrees(math.acos((25+64-81)/(2*5*8))), 84.3)  # angle opp 9
check_expect("silver[2].misc", 11*14*math.sin(math.radians(42)), 103.0)
check_expect("silver[3].misc", math.degrees(math.acos((64+100-36)/(2*8*10))), 36.9)  # angle opp 6
check_expect("silver[4].misc", math.sqrt(250-234*abs(math.cos(math.radians(110)))), 13.0)  # cos taken positive
check_expect("silver[5].misc", 15*20*math.sin(math.radians(75)), 289.8)
check_expect("silver[6].misc", math.degrees(math.acos(16/56)), 73.4)  # +16
# gold
check_expect("gold[0].misc", math.sqrt(325), 18.0)
check_expect("gold[1].misc", 0.5*13*14, 91)
check_expect("gold[2].misc", math.sqrt(185-176*abs(math.cos(math.radians(100)))), 12.4)  # cos positive
check_expect("gold[3].misc", math.degrees(math.asin(30/80)), 22.0)  # no half
check_expect("gold[4].misc", 6*10*math.sin(math.radians(70))/2, 28.2)  # one triangle

# ---- em dashes ----
print("\n--- EM DASH SCAN ---")
raw = json.dumps(pd, ensure_ascii=False)
em = raw.count("—")
print("em dash count:", em)
# find where (excluding note fields would need parse; just report)
def walk(o, path=""):
    if isinstance(o, dict):
        for k,v in o.items():
            walk(v, path+"/"+k)
    elif isinstance(o, list):
        for i,v in enumerate(o):
            walk(v, f"{path}[{i}]")
    elif isinstance(o, str):
        if "—" in o:
            print("EMDASH at", path, repr(o[:60]))
walk(pd)

print("\n=== ISSUES ===")
for i in issues: print(i)
print("total issues:", len(issues))
