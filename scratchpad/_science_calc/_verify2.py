import json, math
pd=json.load(open('_chk_8a0771_live.json',encoding='utf-8'))
issues=[]
def close(a,b,tol):
    return abs(a-b)<=tol

# Independent fresh solve
fresh={
 'bronze':[40*0.05, 5.0/0.10, 10/200, 3/((23-20)/100), 0.5*50*0.04**2],
 'silver':[0.5*120*0.08**2, math.sqrt(2*(0.5*500*0.10**2)/0.20), 15/0.06, math.sqrt(2*5.4/300), 2*(0.5*60*0.15**2)],
 'gold':[math.sqrt(2*(0.5*400*0.12**2)/0.16), 2*0.450/((30-24)/100)**2, 0.20*9.8*3.0, 10/100+10/200],
}
pb=pd['problem_bank']
for tier in ('bronze','silver','gold'):
    for i,p in enumerate(pb[tier]):
        sol=p['solutions'][0]; fr=fresh[tier][i]
        tol=max(p.get('accept',0.01), abs(fr)*0.005)
        if not close(sol,fr,tol):
            issues.append(f"{tier}[{i}] stored {sol} vs fresh {round(fr,5)}")
        # expects vs accept window
        acc=p.get('accept',0.005)
        for j,m in enumerate(p.get('misconceptions',[])):
            e=m.get('expect')
            if e is None: continue
            if abs(e-sol)<=acc:
                issues.append(f"{tier}[{i}].misc[{j}] DEAD expect {e} within ±{acc} of {sol}")
        # guided last computational box lands on solution
        gs=p.get('guided_steps',[])
        # find phase-substitute boxes; the answer at/after boundary should include sol
        boxvals=[s.get('answer') for s in gs if s.get('answer') is not None]
        if not any(close(bv,sol,tol) for bv in boxvals):
            issues.append(f"{tier}[{i}] no guided box equals solution {sol}; boxes={boxvals}")
print("ISSUES:", issues if issues else "NONE - all solutions, expects, guided boxes verified")
