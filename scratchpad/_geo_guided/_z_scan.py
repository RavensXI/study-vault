import json,re
live=json.load(open('_CHK_L09_live.json',encoding='utf-8'))
s=json.dumps(live,ensure_ascii=False)
print('check:wrong count', s.count('"check"'))
print('em dash count', s.count('—'), 'en dash', s.count('–'))
for m in re.finditer(r'.{60}[—–].{60}', s):
    print('  DASH>', m.group(0))
pb=live['problem_bank']
for t in ['bronze','silver','gold']:
    print(t+'_description:', repr(pb.get(t+'_description')))
    for i,p in enumerate(pb[t]):
        issues=[]
        if 'hint' not in p: issues.append('no hint')
        if 'guided_steps' not in p and 'guided_skip_reason' not in p: issues.append('no guided_steps')
        for j,st in enumerate(p.get('guided_steps',[])):
            if 'answer' in st and not isinstance(st['answer'],(int,float)): issues.append(f'step{j} non-numeric answer {st["answer"]!r}')
            if 'pre' in st and re.search(r'<',st['pre']): issues.append(f'step{j} html in pre')
        subs=[j for j,st in enumerate(p.get('guided_steps',[])) if st.get('phase')=='substitute']
        boxes=[j for j,st in enumerate(p.get('guided_steps',[])) if 'answer' in st]
        if len(subs)!=1: issues.append('subs='+str(subs))
        else:
            after=[j for j in boxes if j>=subs[0]]
            before=[j for j in boxes if j<subs[0]]
            if len(after)<2: issues.append('after<2')
            if len(before)<1: issues.append('before<1')
        for mc in p.get('misconceptions',[]):
            if 'check' in mc: issues.append('check key present')
            if 'expect' not in mc: issues.append('no expect')
        print(f'  {t}[{i}] boxes={len(boxes)} sub={subs} mc={[m.get("expect") for m in p.get("misconceptions",[])]} sol={p.get("solutions")} {"; ".join(issues) if issues else "ok"}')
