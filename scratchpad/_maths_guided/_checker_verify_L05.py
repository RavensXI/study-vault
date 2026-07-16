# -*- coding: utf-8 -*-
import json, io, re

live = json.load(io.open('_checker_live_L05.json', encoding='utf-8'))[0]['practice_data']

# ---- pre-dump preservation ----
pre = json.load(io.open('_pre_fanout_dump.json', encoding='utf-8'))
LID = 'ea8d68a2-63b8-40e9-87de-f879156e0d93'
pre_entry = None
if isinstance(pre, dict):
    if LID in pre:
        pre_entry = pre[LID]
    else:
        for k,v in pre.items():
            if isinstance(v,dict) and v.get('id')==LID:
                pre_entry=v; break
elif isinstance(pre, list):
    for v in pre:
        if isinstance(v,dict) and v.get('id')==LID:
            pre_entry=v; break
print("PRE ENTRY FOUND:", pre_entry is not None)
if pre_entry is not None:
    pd = pre_entry.get('practice_data', pre_entry)
    for f in ['related_videos','topic_links','worked_examples','passages']:
        a = json.dumps(pd.get(f), sort_keys=True, ensure_ascii=False) if f in pd else None
        b = json.dumps(live.get(f), sort_keys=True, ensure_ascii=False) if f in live else None
        print(f"{f}: pre_present={f in pd} live_present={f in live} EQUAL={a==b}")

# ---- em dash scan ----
def walk(o, path=''):
    if isinstance(o, dict):
        for k,v in o.items():
            # skip internal note fields
            if k=='note': continue
            yield from walk(v, path+'.'+k)
    elif isinstance(o, list):
        for i,v in enumerate(o):
            yield from walk(v, path+f'[{i}]')
    elif isinstance(o, str):
        yield path, o

emdash = []
for p,s in walk(live):
    if '—' in s or '–' in s:
        emdash.append((p,s))
print("EM/EN DASH HITS:", len(emdash))
for p,s in emdash[:20]: print("  ",p, repr(s))

# ---- box numeric check ----
def check_boxes(steps, label):
    errs=[]
    for i,st in enumerate(steps):
        if 'answer' in st:
            a=st['answer']
            if not isinstance(a,(int,float)):
                errs.append(f"{label}[{i}] answer not numeric: {a!r}")
    return errs

allerr=[]
g=live['guided']
allerr+=check_boxes(g['opener']['steps'],'opener')
for t in ['bronze','silver','gold']:
    allerr+=check_boxes(g['teach'][t]['steps'],'teach.'+t)
for t in ['bronze','silver','gold']:
    for j,pr in enumerate(live['problem_bank'][t]):
        gs=pr.get('guided_steps',[])
        allerr+=check_boxes(gs,f'{t}[{j}].guided_steps')
print("NON-NUMERIC BOX ERRORS:", allerr)

# ---- boundary check ----
print("\nBOUNDARY CHECK")
for t in ['bronze','silver','gold']:
    for j,pr in enumerate(live['problem_bank'][t]):
        gs=pr.get('guided_steps',[])
        if not gs:
            print(f"{t}[{j}] NO guided_steps (input={pr.get('input_type')})"); continue
        # find first phase substitute among box steps
        boxidx=[i for i,s in enumerate(gs) if 'answer' in s]
        bidx=None
        for i,s in enumerate(gs):
            if s.get('phase')=='substitute':
                bidx=i; break
        if bidx is None:
            print(f"{t}[{j}] NO phase boundary"); continue
        before=[i for i in boxidx if i<bidx]
        after=[i for i in boxidx if i>=bidx]
        ok = len(before)>=1 and len(after)>=2
        print(f"{t}[{j}] before={len(before)} after={len(after)} OK={ok}")
