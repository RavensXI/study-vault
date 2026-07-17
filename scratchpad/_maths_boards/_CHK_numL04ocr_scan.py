import json, re
from math import gcd

live = json.load(open("C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_CHK_numL04ocr_live.json", encoding="utf-8"))
pd = live["practice_data"]

problems=[]
issues=[]

# em dash scan across all student-facing strings
def walk(obj, path):
    if isinstance(obj, dict):
        for k,v in obj.items():
            if k=="note": continue
            walk(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i,v in enumerate(obj):
            walk(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        if "—" in obj or "–" in obj:
            issues.append(f"DASH at {path}: {obj[:60]}")
        for ent in ["&rsquo;","&amp;","&quot;","&ndash;","&mdash;","&nbsp;"]:
            if ent in obj:
                issues.append(f"ENTITY {ent} at {path}")
walk(pd, "pd")

# Fresh solve helpers
def factors(n): return [i for i in range(1,n+1) if n%i==0]
def lcm(a,b): return a*b//gcd(a,b)
def lcm3(a,b,c): return lcm(lcm(a,b),c)

checks = []
def chk(name, got, exp):
    ok = got==exp
    checks.append((name, got, exp, ok))
    if not ok: issues.append(f"MATHS {name}: computed {exp}, stored {got}")

# Fresh-solve each bank problem's stored solution
chk("gold0 HCF6 LCM180 one36", pd["problem_bank"]["gold"][0]["solutions"][0], 6*180//36)
chk("gold1 LCM(24,36,40)", pd["problem_bank"]["gold"][1]["solutions"][0], lcm3(24,36,40))
chk("gold2 index2 of 2520", pd["problem_bank"]["gold"][2]["solutions"][0], 3)  # 2520=2^3*315
chk("gold3 HCF4 LCM60 one20", pd["problem_bank"]["gold"][3]["solutions"][0], 4*60//20)
chk("gold4 LCM(4,6,10)", pd["problem_bank"]["gold"][4]["solutions"][0], lcm3(4,6,10))

chk("bronze0 #factors12", pd["problem_bank"]["bronze"][0]["solutions"][0], len(factors(12)))
chk("bronze1 7th mult 6", pd["problem_bank"]["bronze"][1]["solutions"][0], 6*7)
chk("bronze2 is29prime", pd["problem_bank"]["bronze"][2]["solutions"][0], 1)
chk("bronze3 HCF(8,12)", pd["problem_bank"]["bronze"][3]["solutions"][0], gcd(8,12))
chk("bronze4 LCM(4,6)", pd["problem_bank"]["bronze"][4]["solutions"][0], lcm(4,6))
chk("bronze5 2s in 36", pd["problem_bank"]["bronze"][5]["solutions"][0], 2)
chk("bronze6 HCF(15,20)", pd["problem_bank"]["bronze"][6]["solutions"][0], gcd(15,20))
chk("bronze7 LCM(3,5)", pd["problem_bank"]["bronze"][7]["solutions"][0], lcm(3,5))

chk("silver0 HCF(48,60)", pd["problem_bank"]["silver"][0]["solutions"][0], gcd(48,60))
chk("silver1 LCM(8,14)", pd["problem_bank"]["silver"][1]["solutions"][0], lcm(8,14))
chk("silver2 LCM(12,18)", pd["problem_bank"]["silver"][2]["solutions"][0], lcm(12,18))
chk("silver3 sum distinct primes 180", pd["problem_bank"]["silver"][3]["solutions"][0], 2+3+5)
chk("silver4 HCF(36,90)", pd["problem_bank"]["silver"][4]["solutions"][0], gcd(36,90))
chk("silver5 LCM(12,15)", pd["problem_bank"]["silver"][5]["solutions"][0], lcm(12,15))
chk("silver6 HCF(24,40,56)", pd["problem_bank"]["silver"][6]["solutions"][0], gcd(gcd(24,40),56))

# misconception expects reproduce
def me(tier,i): return pd["problem_bank"][tier][i]["misconceptions"]
chk("gold0 exp divide_lcm", me("gold",0)[0]["expect"], 180//36)
chk("gold1 exp pair_only LCM(24,36)", me("gold",1)[0]["expect"], lcm(24,36))
chk("gold2 exp count_primes", me("gold",2)[0]["expect"], 4)  # distinct primes 2,3,5,7
chk("gold3 exp divide_lcm", me("gold",3)[0]["expect"], 60//20)
chk("gold4 exp multiply_all", me("gold",4)[0]["expect"], 4*6*10)
chk("bronze0 exp drop_ends", me("bronze",0)[0]["expect"], len(factors(12))-2)
chk("bronze1 exp off_by_one", me("bronze",1)[0]["expect"], 6*6)
chk("bronze2 exp not_prime", me("bronze",2)[0]["expect"], 0)
chk("bronze3 exp use_lcm", me("bronze",3)[0]["expect"], lcm(8,12))
chk("bronze4 exp multiply", me("bronze",4)[0]["expect"], 4*6)
chk("bronze5 exp count_all", me("bronze",5)[0]["expect"], 4)
chk("bronze6 exp use_lcm", me("bronze",6)[0]["expect"], lcm(15,20))
chk("bronze7 exp use_hcf", me("bronze",7)[0]["expect"], gcd(3,5))
chk("silver0 exp use_lcm", me("silver",0)[0]["expect"], lcm(48,60))
chk("silver1 exp multiply", me("silver",1)[0]["expect"], 8*14)
chk("silver2 exp multiply", me("silver",2)[0]["expect"], 12*18)
chk("silver3 exp product", me("silver",3)[0]["expect"], 2*3*5)
chk("silver3 exp count_repeats", me("silver",3)[1]["expect"], 2+2+3+3+5)
chk("silver4 exp use_lcm", me("silver",4)[0]["expect"], lcm(36,90))
chk("silver5 exp use_hcf", me("silver",5)[0]["expect"], gcd(12,15))
chk("silver6 exp use_lcm", me("silver",6)[0]["expect"], lcm3(24,40,56))

# teach walks final answers
gt = pd["guided"]["teach"]
chk("teach gold HCF8 LCM96 one32", gt["gold"]["steps"][1]["answer"], 8*96//32)
chk("teach bronze HCF(6,8)", gt["bronze"]["steps"][2]["answer"], gcd(6,8))
chk("teach silver LCM(10,15)", gt["silver"]["steps"][2]["answer"], lcm(10,15))

print("=== MATHS CHECKS ===")
for n,g,e,ok in checks:
    if not ok: print("FAIL", n, "stored",g,"expected",e)
print(f"{sum(1 for c in checks if c[3])}/{len(checks)} maths checks pass")
print("\n=== STYLE/OTHER ISSUES ===")
for x in issues: print(x)
if not issues: print("none")
