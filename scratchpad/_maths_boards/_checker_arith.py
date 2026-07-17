import json, re
live = json.load(open("_live_L01.json", encoding="utf-8"))
mism=[]
# match a simple arithmetic expr ending the pre text before "= "
pat = re.compile(r'([-−]?\d+(?:\.\d+)?)\s*([×x*+÷/−-])\s*([-−]?\d+(?:\.\d+)?)\s*(?:[×x*+÷/−-]\s*([-−]?\d+(?:\.\d+)?)\s*)?=\s*$')
def norm(x): return float(x.replace("−","-"))
def ev(a,op,b):
    if op in "×x*": return a*b
    if op=="+": return a+b
    if op in "÷/": return a/b
    if op in "−-": return a-b
def check(steps, tag):
    for i,st in enumerate(steps):
        pre=st.get("pre","")
        if "answer" not in st: continue
        m=pat.search(pre)
        if not m: continue
        a=norm(m.group(1)); op=m.group(2); b=norm(m.group(3))
        r=ev(a,op,b)
        if m.group(4):
            c=norm(m.group(4)); r=ev(r,op,c)
        exp=st["answer"]
        if abs(r-exp)>1e-9:
            mism.append(f"{tag}[{i}] '{pre.strip()}' computes {r} but answer={exp}")
for tier in ["bronze","silver","gold"]:
    check(live["guided"]["teach"][tier]["steps"], f"teach.{tier}")
    for i,p in enumerate(live["problem_bank"][tier]):
        check(p.get("guided_steps",[]), f"{tier}[{i}]")
check(live["guided"]["opener"]["steps"], "opener")
print("arithmetic mismatches:", mism or "none (all parsed arith boxes match)")

# Verify final fraction boxes land on solutions
def frac_check():
    out=[]
    for tier in ["bronze","silver","gold"]:
        for i,p in enumerate(live["problem_bank"][tier]):
            sol=p.get("solutions"); gs=p.get("guided_steps",[])
            if p.get("input_type")=="fraction" and len(sol)==2:
                # find last two distinct numerator/denominator? just report done line
                pass
    return out
