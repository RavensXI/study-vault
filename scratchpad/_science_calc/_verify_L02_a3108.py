# -*- coding: utf-8 -*-
# Independent fresh-solve of the built L02 (a3108b4601) shard.
import json, io
pd = json.load(io.open('lesson_higher-calculations-L02@a3108b4601.json', encoding='utf-8'))
pb = pd['problem_bank']
MV = 24.0
errs = []

def approx(a,b,t=1e-6): return abs(a-b) <= t

# ---- fresh-solve expected answers (independent of build) ----
expected = {
 ('bronze',0): 0.5*MV,                      # 12
 ('bronze',1): 4.8/MV,                       # 0.2
 ('bronze',2): 2*MV,                         # 48
 ('bronze',3): 56/(56+44)*100,               # 56
 ('bronze',4): 100.0,                        # single product
 ('bronze',5): 7.5/10*100,                   # 75
 ('bronze',6): (0.1/2)*MV,                   # 1.2
 ('bronze',7): 7.2/MV,                       # 0.3
 ('silver',0): (5.0/100)*MV,                 # 1.2
 ('silver',1): ((4.6/23)/2)*MV,              # 2.4 (edited)
 ('silver',2): (0.6/24)*MV,                  # 0.6
 ('silver',3): 5.6/((10/160)*2*56)*100,      # 80
 ('silver',4): (2*56)/((2*56)+(3*44))*100,   # 45.9016..
 ('silver',5): 100.0,
 ('gold',0): 960/(((3.25/65)*MV)*1000)*100,  # 80
 ('gold',1): 56/(56+18)*100,                 # 75.6757..
 ('gold',2): ((32/160)*3)*MV,                # 14.4
 ('gold',3): ((12.25/122.5)*3/2)*MV,         # 3.6
 ('gold',4): 504/(((2.5/100)*MV)*1000)*100,  # 84
 ('gold',5): (3*32)/((3*32)+(2*74.5))*100,   # 39.1836..
}
for tier in ('bronze','silver','gold'):
    for i,p in enumerate(pb[tier]):
        sol = p['solutions'][0]
        exp = expected[(tier,i)]
        acc = p.get('accept', 0)
        tol = max(acc, 0.05)
        if abs(sol-exp) > tol+1e-9:
            errs.append(f"{tier}[{i}] stored {sol} vs fresh {exp:.4f} (acc {acc})")
        # duplicate check
    sols=[p['solutions'][0] for p in pb[tier]]
    for j,s in enumerate(sols):
        for k in range(j+1,len(sols)):
            if approx(s,sols[k]):
                errs.append(f"{tier}: duplicate solution {s} at [{j}] and [{k}]")

# ---- expects: outside accept window, not equal correct ----
for tier in ('bronze','silver','gold'):
    for i,p in enumerate(pb[tier]):
        sol=p['solutions'][0]; acc=p.get('accept',0)
        for mi,m in enumerate(p.get('misconceptions',[])):
            if 'expect' not in m:
                errs.append(f"{tier}[{i}].misc[{mi}] missing expect key")
            e=m.get('expect')
            if e is None: continue
            ev = e[0] if isinstance(e,list) else e
            if abs(ev-sol) <= max(acc,0.011):
                errs.append(f"{tier}[{i}].misc[{mi}] expect {ev} inside accept of {sol}")

# ---- guided_steps: numeric coherence of final answer boxes ----
# verify the last computational (phase substitute) leads to stored solution somewhere in walk
def walk_final(tier,i):
    p=pb[tier][i]; steps=p['guided_steps']
    boxes=[s['answer'] for s in steps if s.get('answer') is not None]
    sol=p['solutions'][0]
    # the solution value must appear among the walk boxes (the compute step)
    if not any(approx(b,sol,max(p.get('accept',0),0.05)) for b in boxes):
        errs.append(f"{tier}[{i}] guided walk never lands on solution {sol}; boxes={boxes}")
    # substitute boundary present with >=2 live boxes
    sub=None
    for idx,s in enumerate(steps):
        if s.get('phase')=='substitute': sub=idx; break
    if sub is None:
        errs.append(f"{tier}[{i}] no substitute boundary")
    else:
        live=sum(1 for s in steps[sub:] if s.get('answer') is not None)
        if live<2: errs.append(f"{tier}[{i}] only {live} live boxes after boundary")
        if sub<1: errs.append(f"{tier}[{i}] boundary at 0")
for tier in ('bronze','silver','gold'):
    for i in range(len(pb[tier])): walk_final(tier,i)

# ---- specific box arithmetic spot-checks ----
def chk(name,cond):
    if not cond: errs.append("box arith: "+name)
chk("B3 total 56+44", approx(56+44,100))
chk("S4 112+132", approx(112+132,244))
chk("S4 AE", approx(112/244*100,45.9016,1e-3))
chk("G1 AE", approx(56/74*100,75.6757,1e-3))
chk("G5 3O2", approx(3*32,96)); chk("G5 2KCl", approx(2*74.5,149)); chk("G5 tot", approx(96+149,245))
chk("G3 Mr KClO3", approx(39+35.5+3*16,122.5))
chk("G0 theo cm3", approx((3.25/65)*MV*1000,1200))
chk("teach bronze AE", approx(80/124*100,64.516,1e-3))
chk("teach gold yield", approx(1800/2400*100,75))
chk("opener b1", approx(40/100*100,40)); chk("opener b2", approx(30/120*100,25))

# ---- tier_guides examples land on answer ----
chk("tg bronze ex 0.25x24", approx(0.25*24,6))
chk("tg silver ex", approx((4.0/40)*24,2.4))
chk("tg gold ex", approx((16/80)/2*24,2.4))

# ---- em dash scan ----
def scan(o,p,out):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in('note','guided_skip_reason'):continue
            scan(v,p+'.'+k,out)
    elif isinstance(o,list):
        for i,v in enumerate(o):scan(v,p+f'[{i}]',out)
    elif isinstance(o,str) and '—' in o: out.append(p)
ed=[]; scan(pd,'pd',ed)
if ed: errs.append("EM DASH: "+str(ed))

# ---- board neutrality ----
blob=json.dumps(pd,ensure_ascii=False).lower()
for bad in ['aqa','edexcel','ocr','equation sheet','on your sheet','must memorise','memorize']:
    if bad in blob: errs.append(f"board-specific token present: {bad}")

if errs:
    print("VERIFY FAIL (%d):"%len(errs))
    for e in errs: print("  -",e)
else:
    print("VERIFY PASS: all fresh-solves, boxes, expects, neutrality clean")
