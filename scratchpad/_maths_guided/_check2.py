import json
d=json.load(open('_checker_live.json',encoding='utf-8'))
out=[]
pb=d['problem_bank']

# Verify: final two solve-box answers (phase substitute boxes) == solutions
for tier in ['bronze','silver','gold']:
    for i,p in enumerate(pb[tier]):
        gs=p.get('guided_steps',[])
        solve_boxes=[s['answer'] for s in gs if s.get('phase')=='substitute']
        if sorted(solve_boxes)!=sorted(p['solutions']):
            out.append(f"{tier}[{i}] phase-substitute boxes {solve_boxes} != solutions {p['solutions']}")
        # last box must be a check landing on 0
        boxes=[s for s in gs if 'answer' in s]
        if boxes and boxes[-1]['answer']!=0:
            out.append(f"{tier}[{i}] final check box answer {boxes[-1]['answer']} (expected 0)")
        # >=1 before boundary, >=2 live at/after
        idxs=[j for j,s in enumerate(gs) if s.get('phase')=='substitute']
        if idxs:
            b=idxs[0]
            before=[s for s in gs[:b] if 'answer' in s]
            after=[s for s in gs[b:] if 'answer' in s]
            if len(before)<1: out.append(f"{tier}[{i}] <1 box before boundary")
            if len(after)<2: out.append(f"{tier}[{i}] <2 live boxes at/after boundary ({len(after)})")
        else:
            out.append(f"{tier}[{i}] NO phase:substitute boundary")

        # expect check: negated misconception expect == -solutions (as set)
        for m in p.get('misconceptions',[]):
            if m.get('check')=='negated':
                neg=sorted([-s for s in p['solutions']])
                if sorted(m['expect'])!=neg:
                    out.append(f"{tier}[{i}] negated expect {m['expect']} != -solutions {neg}")

print("SECONDARY CHECKS:")
for o in out: print(" -",o)
if not out: print("  all clean")

# Preservation vs pre-dump
pre=json.load(open('_pre_fanout_dump.json',encoding='utf-8'))
