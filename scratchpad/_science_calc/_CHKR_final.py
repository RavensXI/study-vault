import json
live=json.load(open('_CHKR_canon_live.json',encoding='utf-8'))['practice_data']
shard=json.load(open('lesson_higher-calculations-L04@57e3210892.json',encoding='utf-8'))
# shard may be {practice_data:...} or bare
sp = shard.get('practice_data', shard)
print('shard==live practice_data:', json.dumps(sp,sort_keys=True,ensure_ascii=False)==json.dumps(live,sort_keys=True,ensure_ascii=False))

# Independent recompute of every bank problem's final answer and phase-box structure
bank=live['problem_bank']
errs=[]
def approx(a,b,tol=1e-6): return abs(a-b)<=tol
for tier in ['bronze','silver','gold']:
    for i,p in enumerate(bank[tier]):
        gs=p.get('guided_steps',[])
        boxes=[s for s in gs if 'answer' in s]
        # find phase boundary
        phase_idx=[j for j,s in enumerate(gs) if s.get('phase')=='substitute']
        live_after=0
        if phase_idx:
            pi=phase_idx[0]
            live_after=len([s for s in gs[pi:] if 'answer' in s])
        # last non-check box should be the solution (before check). Actually solution is stored:
        sol=p['solutions'][0]
        # the compute box (phase substitute) answer should equal solution for most
        if phase_idx:
            comp=gs[phase_idx[0]].get('answer')
            if not approx(float(comp),float(sol)):
                # e.g. gold6 phase is convert step; check anyway
                errs.append(f'{tier}[{i}] phase-box {comp} != solution {sol}')
        if live_after<2:
            errs.append(f'{tier}[{i}] only {live_after} live boxes after boundary')
        # expects outside accept window
        acc=p.get('accept',0.005)
        for m in p.get('misconceptions',[]):
            ex=m.get('expect')
            if ex is not None and approx(float(ex),float(sol),float(acc)):
                errs.append(f'{tier}[{i}] DEAD expect {ex} inside accept {acc} of {sol}')
print('recompute issues:', errs if errs else 'NONE')
