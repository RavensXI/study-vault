import json, re
pd = json.load(open("_live_43820341-3858-411e-83f2-3eb799cb438c.json", encoding="utf-8"))

def norm(s):
    return (s.replace("−","-").replace("×","*").replace("÷","/")
             .replace("(","(").replace(")",")"))

def check_steps(steps, label):
    for i,st in enumerate(steps):
        if "answer" not in st: continue
        pre=st.get("pre","")
        # find last '=' ; take expression between previous ':' or start and last '='
        if "=" not in pre: continue
        expr=pre.rsplit("=",1)[0]
        # take substring after last ':' or 'so' if present to isolate arithmetic
        # try progressively: find the rightmost arithmetic run
        e=norm(expr)
        # extract trailing arithmetic: numbers and + - * / and spaces and parens
        m=re.search(r'([-()\d\s\.\+\*/]+)$', e)
        if not m: continue
        frag=m.group(1).strip()
        # must contain an operator to be a computation
        if not re.search(r'[\+\*/]|(?<=\d)\s*-\s*(?=[\(\d])', frag): 
            continue
        try:
            val=eval(frag)
        except Exception as ex:
            continue
        if abs(val-st["answer"])>1e-6:
            print(f"MISMATCH {label}[{i}] frag='{frag}' -> {val} but answer={st['answer']}")

# teach
for t,w in pd["guided"]["teach"].items():
    check_steps(w["steps"], f"teach.{t}")
check_steps(pd["guided"]["opener"]["steps"], "opener")
for tier,arr in pd["problem_bank"].items():
    if not isinstance(arr,list): continue
    for idx,p in enumerate(arr):
        if p.get("guided_steps"):
            check_steps(p["guided_steps"], f"{tier}[{idx}]")
print("box arithmetic scan done")
