import json
pd = json.load(open("_CHKR_L06_live.json", encoding="utf-8"))
issues=[]

def is_num(x): return isinstance(x,(int,float)) and not isinstance(x,bool)

# em dash sweep in student-facing strings (exclude internal 'note')
EM="—"
def sweep(obj, path):
    if isinstance(obj, dict):
        for k,v in obj.items():
            if k=="note": continue
            sweep(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i,v in enumerate(obj): sweep(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        if EM in obj: issues.append(f"EM-DASH at {path}: {obj[:60]}")
sweep(pd, "pd")

# completion boundary + numeric boxes per bank problem
pb=pd["problem_bank"]
for tier in ["gold","silver","bronze"]:
    for i,p in enumerate(pb[tier]):
        gs=p.get("guided_steps")
        if p.get("input_type")=="multiple_choice":
            if gs: issues.append(f"{tier}[{i}] MCQ has guided_steps")
            continue
        if not gs:
            issues.append(f"{tier}[{i}] missing guided_steps"); continue
        # numeric boxes
        before=0; atafter=0; seen=False
        for j,st in enumerate(gs):
            if "answer" in st:
                if not is_num(st["answer"]):
                    issues.append(f"{tier}[{i}].gs[{j}] non-numeric answer {st['answer']!r}")
                if st.get("phase")=="substitute": seen=True
                if seen: atafter+=1
                else: before+=1
            if st.get("phase")=="substitute" and "answer" not in st:
                seen=True
        # count phase tags
        nph=sum(1 for st in gs if st.get("phase")=="substitute")
        if nph!=1: issues.append(f"{tier}[{i}] has {nph} phase tags")
        if before<1: issues.append(f"{tier}[{i}] <1 box before phase (before={before})")
        if atafter<2: issues.append(f"{tier}[{i}] <2 live boxes at/after phase (atafter={atafter})")

# teach walks numeric + >=4 boxes
for t in ["gold","silver","bronze"]:
    w=pd["guided"]["teach"][t]["steps"]
    nb=sum(1 for st in w if "answer" in st)
    if nb<4: issues.append(f"teach.{t} has {nb} boxes (<4)")
    for j,st in enumerate(w):
        if "answer" in st and not is_num(st["answer"]):
            issues.append(f"teach.{t}[{j}] non-numeric")
# opener numeric
for j,st in enumerate(pd["guided"]["opener"]["steps"]):
    if "answer" in st and not is_num(st["answer"]):
        issues.append(f"opener[{j}] non-numeric")

# tier guide word budget <=115 words
for t in ["gold","silver","bronze"]:
    steps=pd["tier_guides"][t]["steps"]
    wc=sum(len(s.split()) for s in steps)
    if wc>115: issues.append(f"tier_guides.{t} steps {wc} words >115")

print("STRUCT/STYLE ISSUES:", len(issues))
for i in issues: print("  ",i)
