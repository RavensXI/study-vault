import json
pd=json.load(open('_live_1fcee1e4.json',encoding='utf-8'))
bank=pd['problem_bank']
issues=[]
for tier in ['bronze','silver','gold']:
    for i,p in enumerate(bank[tier]):
        if p.get('input_type')=='multiple_choice': continue
        sol=p['solutions'][0]
        acc=p.get('accept',None)
        # default engine accept when None: box exact / single_value uses accept else exact? assume small
        for m in p.get('misconceptions',[]):
            e=m.get('expect',None)
            if e is None: continue
            # dead if within accept window of solution
            win = acc if acc is not None else 0.005
            if abs(e-sol)<=win:
                issues.append(f"{tier}[{i}] DEAD expect {e} within {win} of sol {sol}")
        # final guided box must land on solution
        gs=p.get('guided_steps',[])
        # collect numeric answer boxes
        boxes=[st['answer'] for st in gs if 'answer' in st]
        if boxes:
            # the box that equals solution should exist
            if not any(abs(b-sol)<=(acc if acc is not None else 0.05) for b in boxes):
                issues.append(f"{tier}[{i}] no guided box lands on sol {sol}; boxes={boxes}")
print('\n'.join(issues) if issues else 'ALL EXPECTS LIVE + solution reached in guided boxes')
