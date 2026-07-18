import json
d=json.load(open('_live_L03.json'))
for tier,probs in d['problem_bank'].items():
    if not isinstance(probs,list): continue
    for pi,p in enumerate(probs):
        gs=p.get('guided_steps',[])
        boxes=[i for i,s in enumerate(gs) if 'answer' in s]
        ph=[i for i,s in enumerate(gs) if s.get('phase')=='substitute']
        if not ph:
            print(f"{tier}[{pi}]: NO phase boundary"); continue
        pidx=ph[0]
        before=[b for b in boxes if b<pidx]
        atafter=[b for b in boxes if b>=pidx]
        # last box answer vs solution
        lastnonchk=None
        print(f"{tier}[{pi}]: boxes_before_phase={len(before)} live_at/after={len(atafter)} sol={p['solutions']}")
