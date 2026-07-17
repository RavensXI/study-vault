import json
live=json.load(open('_CHK5_live.json',encoding='utf-8'))
pb=live['problem_bank']

print("=== final guided box vs solution ===")
for t in ['bronze','silver','gold']:
    for i,p in enumerate(pb[t]):
        gs=p.get('guided_steps')
        sol=p.get('solutions')
        if not gs:
            print(f"{t}[{i}] no guided_steps (input={p.get('input_type')})")
            continue
        boxes=[s for s in gs if 'answer' in s]
        # the 'landing' box: the solve box (not the check). Look for box whose answer==sol[0]
        finals=[b['answer'] for b in boxes]
        hit = sol and sol[0] in finals
        # count live boxes at/after phase substitute
        seen=False; live_after=0; pre_boxes=0
        for s in gs:
            if s.get('phase')=='substitute': seen=True
            if 'answer' in s:
                if seen: live_after+=1
                else: pre_boxes+=1
        print(f"{t}[{i}] sol={sol} box_answers={finals} sol_in_boxes={hit} pre_boxes={pre_boxes} live_after={live_after}")

print("\n=== misconception expects (manual reproduce table) ===")
for t in ['bronze','silver','gold']:
    for i,p in enumerate(pb[t]):
        for m in p.get('misconceptions',[]):
            print(f"{t}[{i}] pattern={m.get('pattern')} expect={m.get('expect')}")
