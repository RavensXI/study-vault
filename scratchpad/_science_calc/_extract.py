import json, re
d=json.load(open('_live_canon.json'))
def strip(s):
    if not isinstance(s,str): return s
    # remove svg
    s=re.sub(r'<svg.*?</svg>','[SVG]',s,flags=re.S)
    s=re.sub(r'<[^>]+>','',s)
    return s.strip()
pb=d['problem_bank']
for tier in ['bronze','silver','gold']:
    print("="*80)
    print("TIER",tier, "count", len(pb[tier]))
    for i,p in enumerate(pb[tier]):
        print(f"\n--- {tier}[{i}] ---")
        print("DISPLAY:", strip(p.get('display','')))
        print("input_type:",p.get('input_type'),"solutions:",p.get('solutions'),"unit:",p.get('unit'),"accept:",p.get('accept'),"higher_only:",p.get('higher_only'),"calc:",p.get('calculator'))
        if 'options' in p: print("options:",[strip(o) for o in p['options']])
        print("hint:",p.get('hint'))
        for gi,g in enumerate(p.get('guided_steps',[])):
            if 'say' in g and 'pre' not in g:
                print(f"  gs[{gi}] SAY:",strip(g['say']))
            else:
                print(f"  gs[{gi}] pre={strip(g.get('pre',''))!r} post={g.get('post','')!r} answer={g.get('answer')} phase={g.get('phase','')} done={g.get('done','')!r}")
        for mi,m in enumerate(p.get('misconceptions',[])):
            print(f"  mc[{mi}] pattern={m.get('pattern')} expect={m.get('expect')} msg={m.get('message')}")
