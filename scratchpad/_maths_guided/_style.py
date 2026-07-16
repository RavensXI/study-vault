import json,io
live=json.load(io.open('_live_geometry_L06.json',encoding='utf-8'))[0]['practice_data']
pre=json.load(io.open('_pre_fanout_dump.json',encoding='utf-8'))
row=[r for r in pre if r['id']=='4e2bb5ad-e75a-48be-951a-0e8b8db75296'][0]['practice_data']
# worked_examples: normalize em dash in pre and compare
import re
def norm(o): return json.dumps(o,ensure_ascii=False).replace('—',':').replace('–',':')
print("worked_examples equal after em-dash norm:", norm(row['worked_examples'])==json.dumps(live['worked_examples'],ensure_ascii=False))
# scan whole live for em dash / en dash, excluding internal 'note' fields
def scan(o,path=''):
    hits=[]
    if isinstance(o,dict):
        for k,v in o.items():
            if k=='note': continue
            hits+=scan(v,path+'.'+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): hits+=scan(v,f'{path}[{i}]')
    elif isinstance(o,str):
        if '—' in o or '–' in o: hits.append((path,o))
    return hits
h=scan(live)
print("EM/EN DASH hits (excl note):", len(h))
for p,s in h: print("  ",p,repr(s[:80]))
# check hints are plain text (no LaTeX backslash, no HTML tags)
def check_hints(o,path=''):
    bad=[]
    if isinstance(o,dict):
        for k,v in o.items():
            if k=='hint' and isinstance(v,str):
                if '\(' in v or '<' in v or '$' in v: bad.append((path,v))
            else: bad+=check_hints(v,path+'.'+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): bad+=check_hints(v,f'{path}[{i}]')
    return bad
print("hint LaTeX/HTML issues:", check_hints(live))
# check all guided_steps/teach/opener box answers are numeric
def check_ans(o,path=''):
    bad=[]
    if isinstance(o,dict):
        if 'answer' in o and not isinstance(o['answer'],(int,float)):
            bad.append((path,o['answer']))
        for k,v in o.items(): bad+=check_ans(v,path+'.'+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): bad+=check_ans(v,f'{path}[{i}]')
    return bad
print("non-numeric answers:", check_ans(live))
