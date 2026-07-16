import json
live=json.load(open('_live_L12.json',encoding='utf-8'))
for tier in ['gold','bronze','silver']:
    for pi,prob in enumerate(live['problem_bank'][tier]):
        gs=prob.get('guided_steps')
        print(f"--- {tier}[{pi}] {prob['display'][:55]}")
        if gs:
            phase_seen=False; live_after=0; before=0
            for i,st in enumerate(gs):
                if st.get('phase')=='substitute': phase_seen=True
                if 'answer' in st:
                    tagp = st.get('phase','')
                    print(f"    box[{i}] ans={st['answer']!r} phase={tagp} pre={st.get('pre','')!r}")
                    if phase_seen: live_after+=1
                    else: before+=1
            print(f"    -> before-boundary boxes={before}, at/after boundary boxes={live_after}")
        for mi,mc in enumerate(prob.get('misconceptions',[])):
            print(f"    misc[{mi}] expect={mc.get('expect')!r} pattern={mc.get('pattern')}")
