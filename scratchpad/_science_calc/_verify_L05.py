import json, io, re
pd=json.load(io.open("lesson_higher-calculations-L05@f4fdd10261.json",encoding="utf-8"))
issues=[]
# board neutrality
blob=json.dumps(pd).lower()
for b in ["aqa","edexcel"," ocr","eduqas","wjec","equation sheet","must memorise","on your sheet"]:
    if b in blob: issues.append("board/sheet phrase: "+b)
# em dash
if "—" in json.dumps({k:v for k,v in pd.items()}): 
    # allow in note
    def scan(o,p=""):
        if isinstance(o,dict):
            for k,v in o.items():
                if k in("note","guided_skip_reason"):continue
                scan(v,p+"."+k)
        elif isinstance(o,list):
            for i,v in enumerate(o):scan(v,p+f"[{i}]")
        elif isinstance(o,str) and "—" in o: issues.append("emdash "+p)
    scan(pd,"pd")
# walk endpoints land on solution
pb=pd["problem_bank"]
for t in("bronze","silver","gold"):
    for i,pr in enumerate(pb[t]):
        sol=float(pr["solutions"][0])
        ans=[s["answer"] for s in pr["guided_steps"] if s.get("answer") is not None]
        if not any(abs(a-sol)<0.02 for a in ans):
            issues.append(f"{t}[{i}] solution {sol} not hit by walk {ans}")
        # completion boundary
        gs=pr["guided_steps"]
        sub=[j for j,s in enumerate(gs) if s.get("phase")=="substitute"]
        live=sum(1 for s in gs[sub[0]:] if s.get("answer") is not None) if sub else 0
        if not sub or sub[0]<1 or live<2:
            issues.append(f"{t}[{i}] boundary bad sub={sub} live={live}")
        # expects outside accept window
        acc=pr.get("accept",0)
        for m in pr.get("misconceptions",[]):
            e=m.get("expect")
            if e is not None and abs(float(e)-sol)<=max(acc,0.011):
                issues.append(f"{t}[{i}] expect {e} inside accept of {sol}")
# svg present on S4
if "<svg" not in pb["silver"][3]["display"]: issues.append("S4 svg missing")
# svg only shows numbers in problem
import re as _re
svg=pb["silver"][3]["display"].split("</svg>")[0]
print("S4 svg labels:", _re.findall(r">([^<>]+)</text>", svg))
# preservation check: related_videos, topic_links unchanged
live=json.load(io.open("_live_L05.json",encoding="utf-8"))
for f in ("related_videos","topic_links"):
    if json.dumps(pd.get(f))!=json.dumps(live.get(f)): issues.append("changed preserved field "+f)
# equation_hint preserved (except B1 emdash fix)
for i,pr in enumerate(pb["bronze"]):
    lh=live["problem_bank"]["bronze"][i].get("equation_hint")
    nh=pr.get("equation_hint")
    if i!=0 and lh!=nh: issues.append(f"bronze[{i}] equation_hint changed")
print("ISSUES:", issues if issues else "NONE")
