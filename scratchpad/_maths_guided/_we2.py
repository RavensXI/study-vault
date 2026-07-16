import json
live=json.load(open("_live_L07.json",encoding="utf-8"))
pre=json.load(open("_pre_L07.json",encoding="utf-8"))["practice_data"]
lw=live["worked_examples"]; pw=pre["worked_examples"]
lines=[]
for i in range(4):
    for si,(ls,ps) in enumerate(zip(lw[i]["steps"],pw[i]["steps"])):
        if ls.get("label")!=ps.get("label"):
            lines.append(f"we[{i}].steps[{si}].label  PRE={ps.get('label')!r}  LIVE={ls.get('label')!r}")
        if ls.get("content")!=ps.get("content"):
            lines.append(f"we[{i}].steps[{si}].content PRE={ps.get('content')!r} LIVE={ls.get('content')!r}")
# check em dash and arrow anywhere in live student-facing
import re
def walk(o,path):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=="note": continue
            walk(v,path+"."+k)
    elif isinstance(o,list):
        for j,v in enumerate(o): walk(v,f"{path}[{j}]")
    elif isinstance(o,str):
        if "—" in o: lines.append("EM DASH at "+path+": "+o[:80])
        if "->" in o: lines.append("ASCII ARROW -> at "+path+": "+o[:80])
walk(live,"root")
open("_we_out.txt","w",encoding="utf-8").write("\n".join(lines))
print("done")
