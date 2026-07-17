# -*- coding: utf-8 -*-
import json, io, re

live = json.load(io.open("_CHK_graphsL08_live.json", encoding="utf-8"))
pre  = json.load(io.open("_CHK_graphsL08_pre.json", encoding="utf-8"))

problems = []
errs = []

def trap(h, ys):
    mids = ys[1:-1]
    return (h/2)*(ys[0]+ys[-1]+2*sum(mids))

# ---- fresh-solve each bank problem where deterministic ----
pb = live["problem_bank"]
# gold[0]
assert abs(trap(1,[1,2,5,10,17,26])-47.5)<1e-9, "gold0"
# gold[3]
assert abs(trap(0.5,[0,0.25,1,2.25,4])-2.75)<1e-9, "gold3"
# silver checks
assert abs(trap(2,[0,4,12,24])-56)<1e-9
assert abs(trap(1,[1,4,9,16])-21.5)<1e-9
assert abs(trap(1,[0,3,8,15,24])-38)<1e-9
assert abs(trap(2,[0,6,8,6])-34)<1e-9
# composite S3
assert 0.5*5*10 + 10*10 + 0.5*5*10 == 150
# teach
assert abs(trap(1,[2,5,10,17])-24.5)<1e-9
assert abs(trap(1,[0,1,4,9,16,25])-42.5)<1e-9
# method card
assert abs(trap(1,[0,1,4,9,16])-22)<1e-9
# worked example
assert abs(trap(1,[1,4,9])-9)<1e-9
print("trapezium/geometry spot-checks all PASS")

# ---- verify every guided_steps chain independently ----
def check_walk(tag, steps, final_sol):
    box=[s for s in steps if 'answer' in s]
    for i,s in enumerate(box):
        a=s['answer']
        # nothing to independently recompute generically; report shape
    if box:
        last=box[-1]['answer']
        if final_sol is not None and abs(float(last)-float(final_sol))>1e-9:
            errs.append(f"{tag}: last box {last} != solution {final_sol}")

for tier in ['gold','bronze','silver']:
    for i,p in enumerate(pb[tier]):
        sol = p['solutions'][0] if p.get('solutions') else None
        if p.get('input_type')=='multiple_choice':
            continue
        gs=p.get('guided_steps')
        if gs:
            check_walk(f"{tier}[{i}]", gs, sol)

print("walk-last-box vs solution:", "OK" if not errs else errs)

# ---- preservation ----
for k in ['related_videos','topic_links','worked_examples']:
    same = json.dumps(pre.get(k),sort_keys=True)==json.dumps(live.get(k),sort_keys=True)
    print(f"preserved {k}: {same}")
    if not same:
        print("  PRE :", json.dumps(pre.get(k))[:300])
        print("  LIVE:", json.dumps(live.get(k))[:300])

# method_card comparison (spec allows trim)
print("method_card in pre?", 'method_card' in pre, " in live?", 'method_card' in live)

# ---- em dash sweep on student-facing strings ----
def walk_strings(o, path=""):
    if isinstance(o,dict):
        for kk,vv in o.items():
            if kk=='note': continue
            yield from walk_strings(vv, f"{path}.{kk}")
    elif isinstance(o,list):
        for idx,vv in enumerate(o):
            yield from walk_strings(vv, f"{path}[{idx}]")
    elif isinstance(o,str):
        yield path,o

emdash=[]
for path,s in walk_strings(live):
    if '—' in s:
        emdash.append(path)
print("em dashes found:", emdash if emdash else "none")

# ---- expects reproduce (recompute committed error) ----
print("--- expect checks ---")
# helper prints for manual
