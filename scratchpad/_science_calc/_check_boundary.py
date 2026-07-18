import json
pd=json.load(open('_live_1fcee1e4.json',encoding='utf-8'))
bank=pd['problem_bank']
for tier in ['bronze','silver','gold']:
    for i,p in enumerate(bank[tier]):
        gs=p.get('guided_steps')
        if not gs: continue
        # index of first phase==substitute among steps
        phase_idx=[j for j,st in enumerate(gs) if st.get('phase')=='substitute']
        boxes_before=sum(1 for st in gs[:phase_idx[0]] if 'answer' in st) if phase_idx else None
        boxes_after=sum(1 for st in gs[phase_idx[0]:] if 'answer' in st) if phase_idx else None
        flag=''
        if not phase_idx: flag='NO PHASE TAG'
        elif boxes_before<1 or boxes_after<2: flag='BOUNDARY VIOLATION'
        print(f"{tier}[{i}] before={boxes_before} after={boxes_after} {flag}")
