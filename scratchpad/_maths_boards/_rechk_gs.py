import json,re
pd=json.load(open("_rechk_live.json",encoding="utf-8"))
pb=pd["problem_bank"]
def clean(s): return re.sub(r'<svg.*?</svg>','[SVG]',s,flags=re.S) if isinstance(s,str) else s
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[tier]):
        gs=p.get("guided_steps")
        print(f"\n### {tier}[{i}]  (sol option {p['solutions']}) display: {clean(p['display'])[:70]}")
        if gs is None:
            print("  guided_steps: NONE  skip_reason:",p.get("guided_skip_reason"))
            continue
        nboxes=sum(1 for s in gs if 'answer' in s)
        phase_idx=[j for j,s in enumerate(gs) if s.get('phase')=='substitute']
        print(f"  boxes={nboxes} phase@={phase_idx}")
        for j,s in enumerate(gs):
            if 'answer' in s:
                tag=' [PHASE]' if s.get('phase')=='substitute' else ''
                print(f"   box[{j}]{tag} pre={clean(s.get('pre',''))!r} post={clean(s.get('post',''))!r} ans={s.get('answer')}")
