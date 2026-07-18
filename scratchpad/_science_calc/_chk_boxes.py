import json, re
c=json.load(open('_live_canonical.json',encoding='utf-8'))
issues=[]
def evalexpr(txt):
    # find (a op b) with op in × x * + - − ÷ /
    m=re.search(r'\(([-\d\.]+)\s*([×x\*\+\-−÷/])\s*([-\d\.]+)\)', txt)
    if not m: return None
    a=float(m.group(1)); op=m.group(2); b=float(m.group(3))
    if op in '×x*': return a*b
    if op in '+': return a+b
    if op in '-−': return a-b
    if op in '÷/': return a/b
    return None
def checkwalk(path, steps):
    live=0
    boundary_idx=None
    for i,st in enumerate(steps):
        if 'say' in st and 'answer' not in st: 
            continue
        if 'answer' in st:
            if st.get('phase')=='substitute' and boundary_idx is None:
                boundary_idx=i
            ans=st['answer']
            pre=st.get('pre','')
            ev=evalexpr(pre)
            if ev is not None and abs(ev-ans)>0.005:
                issues.append(f'{path}[{i}] pre-arith {pre!r} = {ev} but answer={ans}')
    # count live boxes at/after boundary
    if boundary_idx is not None:
        after=sum(1 for j,st in enumerate(steps) if j>=boundary_idx and 'answer' in st)
        before=sum(1 for j,st in enumerate(steps) if j<boundary_idx and 'answer' in st)
        if before<1: issues.append(f'{path} boundary has {before} boxes before')
        if after<2: issues.append(f'{path} boundary has {after} live boxes at/after')

for tier,arr in c['problem_bank'].items():
    if not isinstance(arr,list): continue
    for i,p in enumerate(arr):
        gs=p.get('guided_steps')
        if gs: checkwalk(f'{tier}[{i}].guided_steps', gs)
for tier,t in c['guided']['teach'].items():
    checkwalk(f'teach.{tier}', t['steps'])
# opener boxes
checkwalk('opener', c['guided']['opener']['steps'])
if issues:
    for x in issues: print('ISSUE:', x)
else:
    print('All box arithmetic and boundaries OK')
