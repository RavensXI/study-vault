# -*- coding: utf-8 -*-
import json, io, math
d = json.load(io.open("lesson_number-L04.json", encoding="utf-8"))
pb = d["problem_bank"]

def hcf(a,b): return math.gcd(a,b)
def lcm(a,b): return a*b//math.gcd(a,b)
def lcm3(a,b,c): return lcm(lcm(a,b),c)
def factors(n): return [k for k in range(1,n+1) if n%k==0]

# expected solutions computed independently from the display semantics
expected = {
 "bronze":[4,6,30,5,12,3,10,24],
 "silver":[2,12,60,24,72,7,45],
 "gold":[12,30,600,180,36],
}
# independent recompute:
checks = {
 "bronze":[
   2+2,               # 36=2^2*3^2 a+b
   hcf(12,18),        # 6
   lcm(6,10),         # 30
   hcf(15,25),        # 5
   lcm(4,6),          # 12
   len(set([2,3,5])), # 3 distinct primes of 30
   hcf(20,30),        # 10
   lcm(8,12),         # 24
 ],
 "silver":[
   2,                 # power of 2 in 180
   hcf(36,84),        # 12
   lcm(15,20),        # 60
   hcf(72,120),       # 24
   lcm(18,24),        # 72
   3+3+1,             # 1080=2^3*3^3*5 sum indices
   lcm(9,15),         # 45
 ],
 "gold":[
   hcf(48,180),       # 12
   720//24,           # HCF*LCM=6*120=720, /24 =30
   8*3*25,            # 600
   lcm3(12,18,30),    # 180
   lcm(12,18),        # 36
 ],
}
ok=True
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[tier]):
        sol=p["solutions"][0]
        exp=checks[tier][i]
        stored_exp=expected[tier][i]
        if not (sol==exp==stored_exp):
            ok=False; print("SOLUTION MISMATCH",tier,i,"stored",sol,"recompute",exp)
        # final answer-bearing walk box must produce solution somewhere
        vals=[st["answer"] for st in p["guided_steps"] if st.get("answer") is not None]
        if sol not in vals:
            ok=False; print("SOLUTION not a box value",tier,i,sol,vals)
        # completion boundary
        gs=p["guided_steps"]
        sub=[j for j,st in enumerate(gs) if st.get("phase")=="substitute"]
        if not sub: ok=False; print("no substitute",tier,i)
        else:
            si=sub[0]
            live=sum(1 for st in gs[si:] if st.get("answer") is not None)
            if live<2: ok=False; print("live<2",tier,i,live)
            if si<1: ok=False; print("sub at 0",tier,i)
        # expects: not equal solution; if determinate, sanity
        for m in p.get("misconceptions",[]):
            e=m.get("expect")
            if e is not None and e==sol:
                ok=False; print("expect==sol",tier,i,m["pattern"])

# manual expect verifications (independent)
def check_expect(tier,i,pat,val):
    p=pb[tier][i]
    got=next((m["expect"] for m in p["misconceptions"] if m["pattern"]==pat),"MISSING")
    if got!=val: 
        print("EXPECT WRONG",tier,i,pat,"stored",got,"want",val)
        return False
    return True

exp_ok=True
exp_ok&=check_expect("bronze",1,"lcm_not_hcf",lcm(12,18))   # 36
exp_ok&=check_expect("bronze",1,"wrong_factor",3)
exp_ok&=check_expect("bronze",2,"hcf_not_lcm",hcf(6,10))    # 2
exp_ok&=check_expect("bronze",2,"multiply",6*10)            # 60
exp_ok&=check_expect("bronze",3,"lcm_not_hcf",lcm(15,25))   # 75
exp_ok&=check_expect("bronze",4,"multiply",4*6)             # 24
exp_ok&=check_expect("bronze",4,"hcf_not_lcm",hcf(4,6))     # 2
exp_ok&=check_expect("bronze",5,"count_all",len(factors(30)))  # 8
exp_ok&=check_expect("bronze",6,"lcm_not_hcf",lcm(20,30))   # 60
exp_ok&=check_expect("bronze",6,"wrong_factor",5)
exp_ok&=check_expect("bronze",7,"multiply",8*12)            # 96
exp_ok&=check_expect("bronze",7,"hcf_not_lcm",hcf(8,12))    # 4
exp_ok&=check_expect("silver",0,"count_all",5)             # total prime factors of 180 w/ mult =2+2+1
exp_ok&=check_expect("silver",1,"lcm_not_hcf",lcm(36,84))  # 252
exp_ok&=check_expect("silver",2,"multiply",15*20)          # 300
exp_ok&=check_expect("silver",2,"hcf_not_lcm",hcf(15,20))  # 5
exp_ok&=check_expect("silver",3,"lcm_not_hcf",lcm(72,120)) # 360
exp_ok&=check_expect("silver",4,"multiply",18*24)          # 432
exp_ok&=check_expect("silver",4,"wrong_powers",hcf(18,24)) # 6 (lowest powers = HCF)
exp_ok&=check_expect("silver",5,"multiply_indices",3*3*1)  # 9
exp_ok&=check_expect("silver",6,"multiply",9*15)           # 135
exp_ok&=check_expect("silver",6,"hcf_not_lcm",hcf(9,15))   # 3
exp_ok&=check_expect("gold",0,"lcm_not_hcf",lcm(48,180))   # 720
exp_ok&=check_expect("gold",1,"product_is_lcm",120//24)    # 5
exp_ok&=check_expect("gold",2,"index_error",6*3*10)        # 180
exp_ok&=check_expect("gold",3,"multiply_all",12*18*30)     # 6480
exp_ok&=check_expect("gold",4,"hcf_not_lcm",hcf(12,18))    # 6
exp_ok&=check_expect("gold",4,"multiply",12*18)            # 216

# total prime factors of 180 with multiplicity
tot=0; n=180
for pr in [2,3,5]:
    while n%pr==0: tot+=1; n//=pr
assert tot==5

print("solutions/boundaries OK" if ok else "SOLUTION ISSUES")
print("expects OK" if exp_ok else "EXPECT ISSUES")
# em dash scan on live-facing strings
import re
def scan(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("note","guided_skip_reason"): continue
            scan(v,path+"."+k)
    elif isinstance(o,list):
        for j,v in enumerate(o): scan(v,path+f"[{j}]")
    elif isinstance(o,str) and "—" in o: print("EMDASH",path)
scan(d)
print("done")
