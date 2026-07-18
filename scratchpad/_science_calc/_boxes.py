# -*- coding: utf-8 -*-
import json,io,re
pd=json.load(io.open('_live_fresh.json',encoding='utf-8'))
out=[]
def check_walk(name,steps):
    boxes=[st for st in steps if st.get('answer') is not None]
    sub=[k for k,st in enumerate(steps) if st.get('phase')=='substitute']
    live_after = 0
    if sub:
        s=sub[0]
        live_after=sum(1 for st in steps[s:] if st.get('answer') is not None)
        before=sum(1 for st in steps[:s] if st.get('answer') is not None)
        out.append(f"{name}: boxes={len(boxes)} subIdx={s} before={before} liveAfter={live_after}")
        if live_after<2: out.append(f"   !! liveAfter<2")
        if before<1: out.append(f"   !! nothing pre-worked")
    else:
        out.append(f"{name}: boxes={len(boxes)} NO-SUBSTITUTE")

# openers/teach
check_walk("opener",pd['guided']['opener']['steps'])
for t in ('bronze','silver','gold'):
    check_walk("teach."+t,pd['guided']['teach'][t]['steps'])
for tier in ('bronze','silver','gold'):
    for i,p in enumerate(pd['problem_bank'][tier]):
        gs=p.get('guided_steps')
        if gs: check_walk(f"{tier}[{i}]",gs)
        elif p.get('input_type')!='multiple_choice':
            out.append(f"{tier}[{i}] MISSING guided_steps (not MC)")

# board neutrality scan across all strings
bad=re.compile(r'\b(AQA|Edexcel|OCR|WJEC|Eduqas|equation sheet|on your sheet|memorise this|must memorise|data sheet)\b',re.I)
hits=[]
def scan(o,path):
    if isinstance(o,dict):
        for k,v in o.items(): scan(v,path+'.'+str(k))
    elif isinstance(o,list):
        for k,v in enumerate(o): scan(v,path+f'[{k}]')
    elif isinstance(o,str):
        for m in bad.finditer(o): hits.append((path,m.group(0),o[:80]))
scan(pd,'pd')
out.append("=== BOARD SCAN ===")
if hits:
    for h in hits: out.append(f"HIT {h[0]}: '{h[1]}' :: {h[2]}")
else:
    out.append("no board/sheet terms found")
io.open('_boxes_out.txt','w',encoding='utf-8').write("\n".join(out))
print("done")
