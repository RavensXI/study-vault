import json
live=json.load(open('_live_graphs-L07_pd.json',encoding='utf-8'))
pb=live['problem_bank']
# Confirm final guided box lands on solution & list expects
for tier in ['bronze','silver','gold']:
    for i,p in enumerate(pb[tier]):
        if p.get('input_type')=='multiple_choice':
            sol=p['solutions'][0]
            # verify option index in range
            assert 0<=sol<len(p['options'])
        gs=p.get('guided_steps')
        if gs:
            boxes=[s for s in gs if 'answer' in s]
            final=boxes[-1]['answer']
            sol=p['solutions']
            # for fraction sol like [1,2]
            solval = sol[0]/sol[1] if len(sol)==2 and p.get('input_type')=='fraction' else sol[0]
            ok = abs(final-solval)<1e-9
            print(f"{tier}[{i}] final_box={final} sol={sol} {'OK' if ok else 'MISMATCH!!'}")
        for m in p.get('misconceptions',[]):
            e=m.get('expect')
            if e is not None:
                print(f"   {tier}[{i}] expect={e} note={m.get('note')}")
