import json,io,sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
pd = json.load(open("_CHK_L02_live.json",encoding="utf-8"))[0]["practice_data"]

# recursive walk collecting student-facing strings with path
findings=[]
def walk(o,path):
    if isinstance(o,dict):
        for k,v in o.items(): walk(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,f"{path}[{i}]")
    elif isinstance(o,str):
        for bad,name in [("—","EMDASH"),("–","ENDASH")]:
            if bad in o: findings.append((name,path,o[:80]))
walk(pd,"pd")
print("EM/EN DASH hits:", len(findings))
for f in findings: print(" ",f)

# hints must be plain text (no LaTeX \( )
print("\n--- hints containing LaTeX or HTML ---")
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pd["problem_bank"][tier]):
        h=p.get("hint","")
        if "\(" in h or "<" in h: print(f"  {tier}[{i}] hint: {h!r}")

# boxes must be numeric
print("\n--- non-numeric guided box answers ---")
def chkboxes(steps,path):
    for j,s in enumerate(steps):
        if "answer" in s and not isinstance(s["answer"],(int,float)):
            print(f"  {path}[{j}] answer={s['answer']!r}")
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pd["problem_bank"][tier]):
        if p.get("guided_steps"): chkboxes(p["guided_steps"],f"{tier}[{i}].guided_steps")
    chkboxes(pd["guided"]["teach"][tier]["steps"],f"teach.{tier}")
chkboxes(pd["guided"]["opener"]["steps"],"opener")
print("done")
