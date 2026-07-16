import json
pd = json.load(open("_chk_L05_fresh.json", encoding="utf-8"))
probs=[]
def collect_steps(container, base):
    for i,st in enumerate(container):
        if "answer" in st:
            a=st["answer"]
            if not isinstance(a,(int,float)) or isinstance(a,bool):
                print("NON-NUMERIC BOX", f"{base}[{i}]", a)
        h=st.get("hint")
        if h and ("\(" in h or "<" in h): print("HINT-MARKUP", f"{base}[{i}]", repr(h))
b=pd["problem_bank"]
for t in ["bronze","silver","gold"]:
    for pi,p in enumerate(b[t]):
        h=p.get("hint")
        if h and ("\(" in h or "<" in h): print("PROBHINT-MARKUP", f"{t}[{pi}]", repr(h))
        if "guided_steps" in p: collect_steps(p["guided_steps"], f"{t}[{pi}].guided_steps")
for t in ["bronze","silver","gold"]:
    collect_steps(pd["guided"]["teach"][t]["steps"], f"teach.{t}")
collect_steps(pd["guided"]["opener"]["steps"], "opener")
# completion boundary check: first problem each tier
for t in ["bronze","silver","gold"]:
    gs=b[t][0]["guided_steps"]
    live=[i for i,s in enumerate(gs) if s.get("phase")=="substitute" and "answer" in s]
    before=[i for i,s in enumerate(gs) if "answer" in s and s.get("phase")!="substitute"]
    print(f"{t}[0]: boxes-before-boundary={len(before)} live-boxes={len(live)}")
print("done")
