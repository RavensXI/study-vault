import json,re
pd=json.load(open("_CHKR_ps03_live.json",encoding="utf-8"))["practice_data"]
out=[]
# tier_guides
tg=pd.get("tier_guides",{})
for tier,g in tg.items():
    out.append(f"\n=== tier_guide {tier}: title={g.get('title')!r}")
    steps=g.get("steps",[])
    wc=sum(len(re.sub('<[^>]+>','',s).split()) for s in steps)
    out.append(f"  steps({len(steps)}, wordcount={wc}): "+ " || ".join(steps))
    ex=g.get("example",{})
    out.append(f"  example.q: {ex.get('question')}")
    for st in ex.get("steps",[]):
        out.append(f"    - {st.get('label')}: {st.get('content')} [isAnswer={st.get('isAnswer')}/{st.get('is_answer')}]")
# em dash sweep across student-facing strings
out.append("\n=== EM DASH / entity sweep ===")
def walk(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=="note": continue
            walk(v,path+"."+k)
    elif isinstance(o,list):
        for i,v in enumerate(o):
            walk(v,f"{path}[{i}]")
    elif isinstance(o,str):
        if "—" in o or "–" in o:
            out.append(f"  DASH at {path}: {o[:90]}")
        for ent in ["&rsquo;","&amp;","&deg;","&times;","&nbsp;","&mdash;"]:
            if ent in o:
                out.append(f"  ENTITY {ent} at {path}: {o[:70]}")
walk(pd)
open("_CHKR_ps03_style.txt","w",encoding="utf-8").write("\n".join(out))
print("done")
