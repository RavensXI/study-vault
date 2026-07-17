# -*- coding: utf-8 -*-
import json, io
from math import gcd
def lcm(a,b): return a*b//gcd(a,b)
def lcm3(a,b,c): return lcm(lcm(a,b),c)
def nfac(n): return sum(1 for d in range(1,n+1) if n%d==0)

pd=json.load(io.open("lesson_maths-eduqas_number-L04.json",encoding="utf-8"))
# independent expected solutions keyed by display essence
checks={
 ("bronze",0):("factors 24",nfac(24)),
 ("bronze",2):("4th mult 7",7*4),
 ("bronze",3):("2s in 60",2),
 ("bronze",4):("HCF12,18",gcd(12,18)),
 ("bronze",5):("LCM4,6",lcm(4,6)),
 ("bronze",6):("LCM5,8",lcm(5,8)),
 ("bronze",7):("HCF20,30",gcd(20,30)),
 ("silver",0):("HCF48,60",gcd(48,60)),
 ("silver",1):("LCM12,20",lcm(12,20)),
 ("silver",2):("HCF36,90",gcd(36,90)),
 ("silver",3):("LCM9,15",lcm(9,15)),
 ("silver",4):("idx3 180",2),
 ("silver",5):("LCM12,18",lcm(12,18)),
 ("silver",6):("HCF56,84",gcd(56,84)),
 ("gold",0):("LCM6,9,10",lcm3(6,9,10)),
 ("gold",1):("HCF idx",2**2*3*5),
 ("gold",2):("LCM idx",2**3*3**2*5**2),
 ("gold",3):("product other",6*120//24),
 ("gold",4):("LCM8,12,18",lcm3(8,12,18)),
}
ok=True
for (t,i),(name,exp) in checks.items():
    got=pd["problem_bank"][t][i]["solutions"][0]
    flag="OK" if got==exp else "*** MISMATCH ***"
    if got!=exp: ok=False
    print(f"{t}[{i}] {name}: stored={got} expected={exp} {flag}")
# duplicate solution check per tier
for t in ("bronze","silver","gold"):
    sols=[tuple(p["solutions"]) for p in pd["problem_bank"][t] if p.get("input_type")!="multiple_choice"]
    dup=[s for s in set(sols) if sols.count(s)>1]
    print(f"{t} dup solutions: {dup}")
    if dup: ok=False
# expect != solution and expect derivations spot
print("ALL SOLUTIONS OK" if ok else "PROBLEMS FOUND")
