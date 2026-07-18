import json
pd=json.load(open('_pd_live.json',encoding='utf-8'))
issues=[]

def approx(a,b,tol=0.005):
    return abs(a-b)<=tol

# check expects sit outside accept window
def check_expect(prob,path,sol,accept):
    for i,m in enumerate(prob.get('misconceptions',[])):
        e=m.get('expect')
        if e is None: continue
        lo,hi=sol-accept,sol+accept
        if lo<=e<=hi:
            issues.append(f"{path}.misconceptions[{i}] DEAD expect {e} inside accept window [{lo},{hi}] of sol {sol}")

for tier in ['bronze','silver','gold']:
    for idx,prob in enumerate(pd['problem_bank'][tier]):
        path=f"{tier}[{idx}]"
        sols=prob.get('solutions',[])
        accept=prob.get('accept',0.005)
        if prob.get('input_type')=='single_value' and len(sols)==1:
            check_expect(prob,path,sols[0],accept)
        # verify final guided box lands on solution
        gs=prob.get('guided_steps',[])
        boxes=[s for s in gs if 'answer' in s]
        # the solution should appear among box answers (usually the substitute/final compute)
        if sols:
            found=any(approx(float(b['answer']),float(sols[0]),max(accept,0.005)) for b in boxes)
            if not found:
                issues.append(f"{path} solution {sols[0]} not matched by any guided box answer {[b['answer'] for b in boxes]}")

print("EXPECT/SOLUTION issues:")
for i in issues: print("  ",i)
if not issues: print("   none")
