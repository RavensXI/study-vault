import json
pd=json.load(open('_live_canonical.json'))
bank=pd['problem_bank']
errs=[];notes=[]
for tier in ['bronze','silver','gold']:
    for pi,p in enumerate(bank[tier]):
        sol=p['solutions'][0]
        acc=p.get('accept',0.005)
        for mi,m in enumerate(p.get('misconceptions',[])):
            e=m.get('expect',None)
            if e is None: continue
            # dead expect if inside accept window of correct answer
            if abs(e-sol)<=acc:
                errs.append(f"{tier}[{pi}].misconceptions[{mi}] DEAD expect={e} within accept {acc} of sol {sol} (pattern {m['pattern']})")
# Now recompute what each expect SHOULD be by committing the described error
print("DEAD EXPECT errs:")
for e in errs: print(" ",e)
print("total",len(errs))
