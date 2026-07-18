import json, re
live = json.load(open("C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_science_calc/_CK_L08_canonical.json", encoding="utf-8"))

def try_eval(pre):
    if pre is None: return None
    s = pre
    s = s.replace("⁸","**8").replace("¹","1").replace("⁰","0")  # rough superscript
    s = s.replace("×","*").replace("÷","/").replace("−","-")
    # handle "10**8"
    s = s.replace("10**8","100000000")
    # find all "a op b" numeric binary ops
    m = re.findall(r'(-?\d+\.?\d*)\s*([*/+\-])\s*(-?\d+\.?\d*)', s)
    if not m: return None
    a,op,b = m[-1]
    a=float(a); b=float(b)
    if op=='*': return a*b
    if op=='/': return a/b
    if op=='+': return a+b
    if op=='-': return a-b

def check(steps, label):
    for i,st in enumerate(steps):
        if "answer" not in st: continue
        val = try_eval(st.get("pre"))
        ans = st["answer"]
        if val is None:
            print(f"  {label}[{i}] pre={st.get('pre')!r} -> NO-PARSE answer={ans}")
        else:
            ok = abs(val-ans) < 1e-6
            print(f"  {label}[{i}] {'OK ' if ok else 'MISMATCH'} eval={val} answer={ans}  pre={st.get('pre')!r}")

print("=== OPENER ==="); check(live["guided"]["opener"]["steps"],"op")
for t in ["bronze","silver","gold"]:
    print(f"=== TEACH {t} ==="); check(live["guided"]["teach"][t]["steps"],t)
for t in ["bronze","silver","gold"]:
    for pi,prob in enumerate(live["problem_bank"][t]):
        print(f"=== BANK {t}[{pi}] sol={prob['solutions']} ===")
        check(prob.get("guided_steps",[]), f"{t}{pi}")
