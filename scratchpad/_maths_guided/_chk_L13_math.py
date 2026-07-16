import json, re
live = json.load(open("_CHK_L13_live.json", encoding="utf-8"))
pb = live["problem_bank"]
issues=[]

def diff(seq):  # common difference from list
    return seq[1]-seq[0]

# Independently solve each and compare
def report(tier, i, computed, stored):
    ok = computed==stored
    print(f"{tier}[{i}]: computed={computed} stored={stored} {'OK' if ok else '*** MISMATCH'}")
    if not ok: issues.append(f"{tier}[{i}] solution {stored} != {computed}")

# GOLD
g=pb["gold"]
report("gold",0, [ (100-7)//3 ], g[0]["solutions"])   # 3n+7=100
report("gold",1, [ (5-1)//1 ], g[1]["solutions"])      # 4n+1=3n+5 -> n=4
report("gold",2, [ sum(2*n+1 for n in range(1,6)) ], g[2]["solutions"])  # sum 5 terms 2n+1
# gold3 MC: 3rd=11,7th=27 -> d=(27-11)/4=4, c=11-4*3=-1 -> 4n-1 ; find option index
d=(27-11)//4; c=11-d*3; formula=f"{d}n{c:+d}"
opts=["4n-1","4n+1","4n-3","3n+2"]
report("gold",3, [opts.index(formula)], g[3]["solutions"])
# gold4: 3,8,13,18 -> 5n-2; first >200
seq=[3,8,13,18]; dd=diff(seq); cc=seq[0]-dd  # 5n-2
n=1
while dd*n+cc<=200: n+=1
report("gold",4, [dd*n+cc], g[4]["solutions"])

# BRONZE
b=pb["bronze"]
def mc_nth(seq, opts):
    dd=diff(seq); cc=seq[0]-dd; f=f"{dd}n{cc:+d}"
    # normalise option strings like '3n - 1'
    norm=[o.replace(" ","").replace("\\(","").replace("\\)","") for o in opts]
    # build canonical for dd,cc
    if cc==0: cand=f"{dd}n"
    else: cand=f"{dd}n{cc:+d}"
    return norm.index(cand), f
report("bronze",0, [mc_nth([2,5,8,11], b[0]["options"])[0]], b[0]["solutions"])
report("bronze",1, [mc_nth([6,10,14,18], b[1]["options"])[0]], b[1]["solutions"])
report("bronze",2, [mc_nth([1,4,7,10], b[2]["options"])[0]], b[2]["solutions"])
report("bronze",3, [mc_nth([7,12,17,22], b[3]["options"])[0]], b[3]["solutions"])
report("bronze",4, [2*10+3], b[4]["solutions"])  # 10th term 2n+3
report("bronze",5, [mc_nth([3,5,7,9], b[5]["options"])[0]], b[5]["solutions"])
# bronze6: 4n-1 first three -> "3, 7, 11" index0
opts6=["3, 7, 11","4, 8, 12","0, 3, 6","-1, 3, 7"]
first3=[4*n-1 for n in (1,2,3)]
s=", ".join(str(x) for x in first3)
report("bronze",6, [opts6.index(s)], b[6]["solutions"])
report("bronze",7, [mc_nth([10,15,20,25], b[7]["options"])[0]], b[7]["solutions"])

# SILVER
sv=pb["silver"]
def mc_nth_neg(seq, opts):
    dd=diff(seq); cc=seq[0]-dd
    norm=[o.replace(" ","").replace("\\(","").replace("\\)","") for o in opts]
    if cc==0: cand=f"{dd}n"
    else: cand=f"{dd}n{cc:+d}"
    return norm.index(cand)
report("silver",0, [mc_nth_neg([20,17,14,11], sv[0]["options"])], sv[0]["solutions"])
report("silver",1, [mc_nth_neg([50,43,36,29], sv[1]["options"])], sv[1]["solutions"])
# silver2: 4,9,14,19 15th term
seq=[4,9,14,19]; dd=diff(seq); cc=seq[0]-dd
report("silver",2, [dd*15+cc], sv[2]["solutions"])
report("silver",3, [mc_nth_neg([-1,3,7,11], sv[3]["options"])], sv[3]["solutions"])
# silver4: is 41 in 2,5,8,11? 3n-1=41 -> n=14
report("silver",4, [ (41+1)//3 ], sv[4]["solutions"])
report("silver",5, [mc_nth_neg([31,25,19,13], sv[5]["options"])], sv[5]["solutions"])
# silver6: how many terms 5,8,11 <50 ; 3n+2<50 -> n<16 -> 15
seq=[5,8,11]; dd=diff(seq); cc=seq[0]-dd
n=0
while dd*(n+1)+cc<50: n+=1
report("silver",6, [n], sv[6]["solutions"])

print("\n--- guided_steps final box lands on solution ---")
for tier in ("bronze","silver","gold"):
    for i,prob in enumerate(pb[tier]):
        gs=prob.get("guided_steps")
        if not gs: continue
        # last box answer
        boxans=[st["answer"] for st in gs if "answer" in st]
        sol=prob["solutions"][0]
        # solution may be index for MC (none have guided) or value
        print(f"{tier}[{i}] box answers {boxans} sol={sol}")

print("\nISSUES:", issues if issues else "NONE")
