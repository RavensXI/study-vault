# -*- coding: utf-8 -*-
import json, sys, re
sys.stdout.reconfigure(encoding="utf-8")
shard = json.load(open("_ps03e_shard.json", encoding="utf-8"))
live = json.load(open("_ps03e_live.json", encoding="utf-8"))["practice_data"]
fails = []
def F(m): fails.append(m)

pb = shard["problem_bank"]
# 1. solutions fresh-solve (recorded expected)
EXP = {
 "bronze":[25,10,[1,2],28,30,54,0,0],
 "silver":[10,0,100,30,8,0,0],
 "gold":[40,0,29,0,6],
}
for t in ("bronze","silver","gold"):
    for i,p in enumerate(pb[t]):
        sol=p["solutions"]
        exp=EXP[t][i]
        exp=exp if isinstance(exp,list) else [exp]
        if [float(x) for x in sol]!=[float(x) for x in exp]:
            F(f"{t}[{i}] solution {sol} != fresh {exp}")

# 2. expects must not equal correct; and present
for t in ("bronze","silver","gold"):
    for i,p in enumerate(pb[t]):
        for j,m in enumerate(p.get("misconceptions") or []):
            if "expect" not in m: F(f"{t}[{i}].mis[{j}] no expect key")
            e=m.get("expect")
            if e is not None:
                sol=[float(x) for x in p["solutions"]]
                ev=e if isinstance(e,list) else [e]
                if len(ev)==len(sol) and all(abs(float(a)-b)<0.011 for a,b in zip(ev,sol)):
                    F(f"{t}[{i}].mis[{j}] expect==correct")

# 3. guided_steps: every box numeric; boundary; final lands on solution (single_value)
for t in ("bronze","silver","gold"):
    for i,p in enumerate(pb[t]):
        gs=p.get("guided_steps")
        if not gs: continue
        boxes=[st for st in gs if st.get("answer") is not None]
        for st in boxes:
            if not isinstance(st["answer"],(int,float)): F(f"{t}[{i}] non-numeric box {st}")
        # boundary
        subs=[k for k,st in enumerate(gs) if st.get("phase")=="substitute"]
        if not subs: F(f"{t}[{i}] no substitute boundary")
        else:
            live_after=sum(1 for st in gs[subs[0]:] if st.get("answer") is not None)
            if live_after<2: F(f"{t}[{i}] only {live_after} live boxes after boundary")

# 4. teach boxes >=4, opener box present
g=shard["guided"]
for t in ("bronze","silver","gold"):
    tb=g["teach"][t]["steps"]
    nb=sum(1 for st in tb if st.get("answer") is not None)
    if nb<4: F(f"teach.{t} only {nb} boxes")
if not any(st.get("answer") is not None for st in g["opener"]["steps"]):
    F("opener no box")

# 5. SVG checks: viewBox/role/aria, no external, text uses currentColor
def check_svg(s,path):
    for chunk in s.split("<svg")[1:]:
        tag=chunk.split(">",1)[0]
        for need in ("viewBox",'role="img"',"aria-label"):
            if need not in tag: F(f"{path} svg missing {need}")
    low=s.lower()
    if "http://" in low or "https://" in low or "xlink" in low: F(f"{path} external ref")
    # every <text has currentColor
    for tchunk in s.split("<text")[1:]:
        ttag=tchunk.split(">",1)[0]
        if "currentColor" not in ttag: F(f"{path} text not currentColor: {ttag[:60]}")
def walk_svg(o,path):
    if isinstance(o,dict):
        for k,v in o.items(): walk_svg(v,path+"."+str(k))
    elif isinstance(o,list):
        for k,v in enumerate(o): walk_svg(v,f"{path}[{k}]")
    elif isinstance(o,str) and "<svg" in o: check_svg(o,path)
walk_svg(shard,"pd")

# 6. figure numbers appear in problem text
def figtext(p): return p.get("display","")
# bronze[4] History 54 + 200
assert "History 54°" in pb["bronze"][4]["display"] and "54°" in pb["bronze"][4]["display"]
if "54°" not in pb["bronze"][4]["display"]: F("b4 fig")
# silver[2] 100/90/70 + ?
for lab in ("100°","90°","70°","?"):
    if lab not in pb["silver"][2]["display"]: F(f"s2 fig missing {lab}")
# silver[3] A 60
if "A 60°" not in pb["silver"][3]["display"]: F("s3 fig")
# gold[1] two pies
for lab in ("Drama 72°","Drama 54°","School A (150)","School B (200)"):
    if lab not in pb["gold"][1]["display"]: F(f"g1 fig missing {lab}")

# 7. preservation: related_videos, topic_links, worked_examples (except we[2] emdash), method_card except emdash
if shard["related_videos"]!=live["related_videos"]: F("related_videos changed")
if shard["topic_links"]!=live["topic_links"]: F("topic_links changed")
# worked_examples: only we[2].steps[1].content changed (em dash)
for k in range(len(live["worked_examples"])):
    a=json.dumps(shard["worked_examples"][k],ensure_ascii=False)
    b=json.dumps(live["worked_examples"][k],ensure_ascii=False)
    if a!=b and not (k==2): F(f"worked_examples[{k}] changed unexpectedly")
if "—" in json.dumps(shard,ensure_ascii=False): F("EM DASH still present somewhere")

# 8. no em dash in any student-facing string already covered by validator
print("Checked. FAILS:",len(fails))
for f in fails: print("  -",f)
if not fails: print("ALL VERIFY CHECKS PASS")
