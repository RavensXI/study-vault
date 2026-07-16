import json,sys,io,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
live=json.load(open("_CHK_graphsL08_live.json",encoding="utf-8"))

def evalexpr(s):
    # extract the last arithmetic expression before '='
    # normalize unicode operators
    s=s.replace("×","*").replace("÷","/").replace("−","-").replace("–","-")
    # find pattern 'expr =' possibly with words; take substring, find rightmost run of math chars ending at '='
    m=re.search(r'([0-9\.\(\)\+\-\*/ ]+)=\s*$', s.strip())
    if not m: 
        # maybe '= ' then nothing, expr before
        m=re.search(r'([0-9\.\(\)\+\-\*/ ]+)=', s)
    if not m: return None
    expr=m.group(1).strip()
    # guard: must contain an operator
    if not re.search(r'[\+\-\*/]',expr): return None
    try:
        return eval(expr)
    except: return None

problems=[]
issues=[]
def check_steps(steps,path):
    for i,st in enumerate(steps):
        if "answer" not in st: continue
        pre=st.get("pre","")
        ans=st["answer"]
        # hint plain text check
        h=st.get("hint","")
        if "\(" in h or "<" in h:
            issues.append(f"{path}[{i}] hint not plain: {h}")
        if not isinstance(ans,(int,float)):
            issues.append(f"{path}[{i}] answer non-numeric: {ans}")
        val=evalexpr(pre)
        if val is not None:
            if abs(val-ans)>1e-9:
                issues.append(f"{path}[{i}] pre='{pre}' evals {val} != answer {ans}")

g=live["guided"]
for tier in ["bronze","silver","gold"]:
    check_steps(g["teach"][tier]["steps"],f"teach.{tier}")
check_steps(g["opener"]["steps"],"opener")
pb=live["problem_bank"]
for tier in ["bronze","silver","gold"]:
    for pi,p in enumerate(pb[tier]):
        if "guided_steps" in p:
            check_steps(p["guided_steps"],f"{tier}[{pi}].guided_steps")

if issues:
    print("ISSUES:")
    for x in issues: print(" ",x)
else:
    print("All parseable box expressions match their answers; all hints plain; all answers numeric.")
