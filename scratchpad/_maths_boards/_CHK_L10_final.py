import json
pd=json.load(open("_CHK_L10_live.json",encoding="utf-8"))
s=json.dumps(pd,ensure_ascii=False)
# em dash check
print("em-dash count:", s.count("—"))
# phase boundary check on every bank problem + teach
def chk(name, steps):
    boxes=[st for st in steps if 'answer' in st]
    phases=[i for i,st in enumerate(steps) if st.get('phase')=='substitute']
    if not phases:
        print(f"  {name}: NO phase tag ({len(boxes)} boxes)"); return
    pi=phases[0]
    before_boxes=[st for st in steps[:pi] if 'answer' in st]
    at_after=[st for st in steps[pi:] if 'answer' in st]
    ok = len(before_boxes)>=1 and len(at_after)>=2
    print(f"  {name}: boxesBefore={len(before_boxes)} boxesAtAfter={len(at_after)} {'OK' if ok else '**FAIL**'}")
bank=pd['problem_bank']
for tier in ['bronze','silver','gold']:
    for i,p in enumerate(bank[tier]):
        chk(f"{tier}[{i}]", p['guided_steps'])
for tier,w in pd['guided']['teach'].items():
    chk(f"teach.{tier}", w['steps'])
# all box answers numeric?
bad=[]
for tier in ['bronze','silver','gold']:
    for i,p in enumerate(bank[tier]):
        for j,st in enumerate(p['guided_steps']):
            if 'answer' in st and not isinstance(st['answer'],(int,float)):
                bad.append(f"{tier}[{i}].step{j} answer={st['answer']!r}")
print("non-numeric answers:", bad)
