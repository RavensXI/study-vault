# -*- coding: utf-8 -*-
import json,re
pd=json.load(open('_live_canonical.json',encoding='utf-8'))
issues=[]
mathserr=0

def approx(a,b,tol): return abs(a-b)<=tol

# --- fresh-solve each problem ---
g=9.8
def upthrust(rho,V): return rho*V*g

tests=[]
pb=pd['problem_bank']
# BRONZE
b=pb['bronze']
tests.append(('bronze[0]',2.0*1000*g,b[0]['solutions'][0]))
tests.append(('bronze[1]',5.0*1000*g,b[1]['solutions'][0]))
tests.append(('bronze[2]',1000*(0.1**3)*g,b[2]['solutions'][0]))
tests.append(('bronze[3]',50*1000*g+101000,b[3]['solutions'][0]))
tests.append(('bronze[4]',200000/(1025*g),b[4]['solutions'][0]))
# SILVER
s=pb['silver']
tests.append(('silver[0]',40*1025*g+101000,s[0]['solutions'][0]))
tests.append(('silver[1]',1000*5e-4*g-0.30*g,s[1]['solutions'][0]))
tests.append(('silver[2]',3.92/(4e-4*g),s[2]['solutions'][0]))
tests.append(('silver[3]',50/0.002,s[3]['solutions'][0]))
tests.append(('silver[4]',1025*2e-4*g-0.18*g,s[4]['solutions'][0]))
# GOLD
go=pb['gold']
tests.append(('gold[0]',11000*1025*g+101000,go[0]['solutions'][0]))
tests.append(('gold[1]',1025*0.005*g-3.0*g,go[1]['solutions'][0]))
tests.append(('gold[2]',(60000/1000)/20,go[2]['solutions'][0]))
tests.append(('gold[3]',13600*0.0006*g,go[3]['solutions'][0]))

print("=== FRESH SOLVE vs STORED (with accept window) ===")
def acc(prob): return prob.get('accept',0.005)
allprobs={'bronze':b,'silver':s,'gold':go}
idx=0
for name,computed,stored in tests:
    tier,i=name[:-3],int(name[-2])
    prob=allprobs[tier][i]
    a=acc(prob)
    ok=approx(computed,stored,a)
    if not ok: mathserr+=1; issues.append(f"{name}: computed {computed} vs stored {stored}, accept {a} -> OUT")
    print(f"{name}: computed={computed:.5f} stored={stored} accept={a} {'OK' if ok else 'FAIL'}")

# --- expects outside accept window ---
print("\n=== EXPECT vs ACCEPT WINDOW ===")
for tier,arr in allprobs.items():
    for i,prob in enumerate(arr):
        sol=prob['solutions'][0]; a=acc(prob)
        for mc in prob.get('misconceptions',[]):
            e=mc.get('expect')
            if e is None: continue
            inside = abs(e-sol)<=a
            if inside:
                mathserr+=1; issues.append(f"{tier}[{i}] DEAD EXPECT {e} inside accept window of {sol}+-{a}")
            print(f"{tier}[{i}] expect={e} sol={sol} accept={a} {'DEAD(inside)!' if inside else 'ok(outside)'}")

print("\nMATHS ERRORS:",mathserr)
for x in issues: print(" -",x)
