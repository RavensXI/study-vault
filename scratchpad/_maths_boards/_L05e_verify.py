# -*- coding: utf-8 -*-
import json, io, re
pd=json.load(io.open("lesson_maths-eduqas_probability-statistics-L05.json",encoding="utf-8"))
pre=json.load(io.open("_L05e_live.json",encoding="utf-8"))["practice_data"]
fails=[]

# 1. Re-eval every guided_step box: parse arithmetic in pre "= " and check answer.
def check_walk(steps, tag):
    for i,st in enumerate(steps):
        a=st.get("answer")
        if a is None: continue
        pre_t=st.get("pre","")
        # find an expression like "X op Y = " at end of pre
        m=re.search(r'([0-9.]+(?:\s*[+\-−×x÷/]\s*[0-9.]+)+)\s*=\s*$', pre_t.replace("−","-").replace("×","*").replace("÷","/").replace(" x ", " * "))
        if m:
            expr=m.group(1).replace("−","-").replace("×","*").replace("÷","/")
            try:
                val=eval(expr)
                if abs(val-a)>0.011:
                    fails.append(f"{tag}[{i}] pre '{pre_t}' computes {val} != answer {a}")
            except Exception as e:
                pass

pb=pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    for j,p in enumerate(pb[tier]):
        if p.get("guided_steps"):
            check_walk(p["guided_steps"], f"{tier}[{j}].gs")
            # last box must equal a stored solution
            boxes=[s["answer"] for s in p["guided_steps"] if s.get("answer") is not None]
            sol=p["solutions"][0]
            if sol not in boxes:
                fails.append(f"{tier}[{j}] solution {sol} not hit by any box {boxes}")
        # expects must not equal solution; and be plausible
        for k,mm in enumerate(p.get("misconceptions",[])):
            e=mm.get("expect")
            if e is not None and abs(e-p["solutions"][0])<0.011:
                fails.append(f"{tier}[{j}].misc[{k}] expect==solution")

# teach walks
for tier in ("bronze","silver","gold"):
    t=pd["guided"]["teach"][tier]
    check_walk(t["steps"], f"teach.{tier}")
# opener
check_walk(pd["guided"]["opener"]["steps"], "opener")

# 2. Misconception expects: recompute the committed errors
exp_checks = {
 ("bronze",1):("range",55),("bronze",2):("midpoint",(18+32)/2),
 ("bronze",4):("iqr",15),("bronze",5):("fd_as_freq",5),("bronze",6):("mult",24*8),
 ("bronze",7):("add",50+28),
 ("silver",1):("cf60",78),("silver",2):("height",4),("silver",3):("q3-med",62-48),
 ("silver",4):("addfd",3+5+4+1),("silver",6):("cf",150),
 ("gold",0):("wholebars",4*10+3*10),("gold",4):("q3diff",60-50),
}
for (tier,idx),(desc,val) in exp_checks.items():
    e=pb[tier][idx]["misconceptions"][0]["expect"]
    if e is None or abs(e-val)>0.011:
        fails.append(f"{tier}[{idx}] expect {e} != committed-error {desc}={val}")

# 3. B4 chart fix: Q1 at n/4=20 reads x=10
cf=pb["bronze"][3]["chart"]["data"]["datasets"][0]["data"]
xs=pb["bronze"][3]["chart"]["data"]["labels"]
if cf[xs.index(10)]!=20: fails.append(f"B4 chart cf at x=10 is {cf[xs.index(10)]} not 20")

# 4. Added charts present + match text
for tier,idx,exp_fd in [("gold",2,[2,4,8,1.5]),("gold",3,[3,5,2]),("silver",4,[3,5,4,1])]:
    ch=pb[tier][idx].get("chart")
    if not ch: fails.append(f"{tier}[{idx}] missing added chart")
    elif ch["data"]["datasets"][0]["data"]!=exp_fd: fails.append(f"{tier}[{idx}] chart data {ch['data']['datasets'][0]['data']} != {exp_fd}")

# 5. Preservation: topic_links, related_videos, worked_examples questions unchanged
for f in ("topic_links","related_videos"):
    if pd.get(f)!=pre.get(f): fails.append(f"preservation: {f} changed")
if [w["question"] for w in pd["worked_examples"]]!=[w["question"] for w in pre["worked_examples"]]:
    fails.append("preservation: worked_examples questions changed")

# 6. SVG sizes and theme-safety
import re as _re
for key,svg in [("opener",pd["guided"]["opener"]["display"])]+[("teach."+t, pd["guided"]["teach"][t]["display"]) for t in ("bronze","silver","gold")]:
    for s in _re.findall(r'<svg.*?</svg>', svg):
        if "fill=\"#0" in s.lower() or 'fill="#1' in s.lower() or 'fill="#2' in s.lower():
            fails.append(f"{key} svg has hard-coded dark fill")
        if len(s)>4000: fails.append(f"{key} svg {len(s)} bytes >4000")

# 7. em dash scan already done by validator; double check '—'
def scan(o,pth):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("note","guided_skip_reason"): continue
            scan(v,pth+"."+str(k))
    elif isinstance(o,list):
        for i,v in enumerate(o): scan(v,pth+f"[{i}]")
    elif isinstance(o,str) and "—" in o: fails.append(f"em dash at {pth}")
scan(pd,"pd")

print("FAILS:",len(fails))
for f in fails: print("  -",f)
if not fails: print("ALL CLEAN")
