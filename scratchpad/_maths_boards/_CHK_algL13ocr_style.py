import json, io
live=json.load(io.open("_CHK_algL13ocr_live.json",encoding="utf-8"))
s=json.dumps(live,ensure_ascii=False)
# em dash / corrupted char scan
for ch,name in [("—","EM DASH"),("�","REPLACEMENT CHAR"),("―","HORIZ BAR")]:
    print(name, "count:", s.count(ch))

# collect all box answers, ensure numeric
bad=[]
def walk_steps(steps,path):
    for i,st in enumerate(steps):
        if "answer" in st:
            a=st["answer"]
            if not isinstance(a,(int,float)):
                bad.append(f"{path}[{i}].answer = {a!r} (non-numeric)")
g=live["guided"]
walk_steps(g["opener"]["steps"],"opener")
for t in ["bronze","silver","gold"]:
    walk_steps(g["teach"][t]["steps"],f"teach.{t}")
pb=live["problem_bank"]
for t in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[t]):
        for j,st in enumerate(p.get("guided_steps",[])):
            if "answer" in st and not isinstance(st["answer"],(int,float)):
                bad.append(f"{t}[{i}].guided_steps[{j}].answer={st['answer']!r}")
        # solutions numeric
        for sol in p.get("solutions",[]):
            if not isinstance(sol,(int,float)):
                bad.append(f"{t}[{i}].solutions has {sol!r}")
print("non-numeric box/solution issues:", bad if bad else "NONE")

# phase boundary check
for t in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[t]):
        gs=p.get("guided_steps")
        if not gs: continue
        boxes=[k for k,st in enumerate(gs) if "answer" in st]
        ph=[k for k,st in enumerate(gs) if st.get("phase")=="substitute"]
        if not ph:
            if p.get("input_type")!="multiple_choice":
                print(f"{t}[{i}] NO phase tag (input={p.get('input_type')})")
            continue
        pk=ph[0]
        before=[b for b in boxes if b<pk]
        after=[b for b in boxes if b>=pk]
        if len(before)<1 or len(after)<2:
            print(f"{t}[{i}] boundary weak: before={len(before)} after={len(after)}")
print("phase check done")
