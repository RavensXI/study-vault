import json
d=json.load(open('_live_L05.json',encoding='utf-8'))['canonical']
def is_box(s): return 'answer' in s
def analyse(name, steps):
    idx=[i for i,s in enumerate(steps) if s.get('phase')=='substitute']
    boxes=[i for i,s in enumerate(steps) if is_box(s)]
    if not idx:
        print(f"{name}: NO PHASE TAG (boxes={len(boxes)})"); return
    b=idx[0]
    before=[i for i in boxes if i<b]
    after=[i for i in boxes if i>=b]
    ok = len(before)>=1 and len(after)>=2
    print(f"{name}: phase@{b} before={len(before)} live={len(after)} {'OK' if ok else 'VIOLATION'}")
    if 'done' not in steps[boxes[-1]]:
        print(f"   note: last box no 'done' check")

for tier,walk in d['guided']['teach'].items():
    analyse(f"teach.{tier}", walk['steps'])
for tier in ['bronze','silver','gold']:
    for i,p in enumerate(d['problem_bank'][tier]):
        gs=p.get('guided_steps')
        if gs: analyse(f"{tier}[{i}]", gs)
        else: print(f"{tier}[{i}]: no guided_steps (input_type={p.get('input_type')})")
