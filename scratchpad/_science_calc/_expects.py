import json
pd=json.load(open('_CK_live.json',encoding='utf-8'))
for tier in ['bronze','silver','gold']:
    for i,p in enumerate(pd['problem_bank'][tier]):
        sol=p.get('solutions'); acc=p.get('accept') or 0
        for m in p.get('misconceptions',[]):
            e=m.get('expect')
            if e is None: 
                print(f"{tier}[{i}] expect=null pattern={m.get('pattern')}"); continue
            # inside accept window of any solution?
            inside=any(abs(e-s)<=acc for s in sol if isinstance(s,(int,float)))
            flag="  <-- DEAD (inside accept!)" if inside else ""
            print(f"{tier}[{i}] sol={sol} acc={acc} expect={e} pat={m.get('pattern')}{flag}")
# verify final guided box lands on solution
print("--- final-box-vs-solution ---")
for tier in ['bronze','silver','gold']:
    for i,p in enumerate(pd['problem_bank'][tier]):
        gs=p.get('guided_steps')
        if not gs: continue
        sol=p['solutions'][0]
        boxes=[s['answer'] for s in gs if 'answer' in s]
        # find the box that equals solution (not necessarily last, since last is a check)
        hit = sol in boxes
        print(f"{tier}[{i}] sol={sol} solInBoxes={hit} boxvals={boxes}")
