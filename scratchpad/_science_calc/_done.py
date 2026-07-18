import json,re
d=json.load(open('_live_L03.json'))
unit_re=re.compile(r'(mol/dm|g/dm|\bg\b|\bmol\b|\bdm³\b|cm³)')
for tier,probs in d['problem_bank'].items():
    if not isinstance(probs,list): continue
    for pi,p in enumerate(probs):
        dones=[s['done'] for s in p.get('guided_steps',[]) if 'done' in s]
        last=dones[-1] if dones else ''
        has=bool(unit_re.search(last))
        print(f"{tier}[{pi}] unit_in_done={has} :: {last[-60:]}")
for tier,w in d['guided']['teach'].items():
    dones=[s['done'] for s in w['steps'] if 'done' in s]
    print(f"teach.{tier}: {dones}")
# propagation
import os,urllib.request
wl=json.load(open('_worklist_versions.json'))
e=wl['higher-calculations-L03@b360dedf84']
print("all_row_ids:",e['all_row_ids'])
