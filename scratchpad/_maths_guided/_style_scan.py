import json,io,sys,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
live=json.load(open('_live_ratio_L01.json',encoding='utf-8'))
# recursively find student-facing strings; skip 'note' keys
hits=[]
def walk(o,path):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=='note': continue
            walk(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,f"{path}[{i}]")
    elif isinstance(o,str):
        if '—' in o: hits.append(("EMDASH",path,o))
        if '&' in o and any(e in o for e in ['&rsquo;','&amp;','&ndash;','&mdash;','&pound;']): hits.append(("ENTITY",path,o))
walk(live,'root')
for h in hits: print(h)
print("emdash/entity hits:", len(hits))

# Check hints are plain text (no latex/html) and boxes numeric
for tier in ['bronze','silver','gold']:
    for i,p in enumerate(live['problem_bank'][tier]):
        h=p.get('hint','')
        if '\(' in h or '<' in h: print(f"HINT NONPLAIN {tier}[{i}]: {h}")
        for j,s in enumerate(p.get('guided_steps',[])):
            if 'answer' in s and not isinstance(s['answer'],(int,float)):
                print(f"NONNUM {tier}[{i}].guided_steps[{j}]: {s['answer']!r}")
print("style scan done")
