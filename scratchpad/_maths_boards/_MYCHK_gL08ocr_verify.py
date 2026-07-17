# -*- coding: utf-8 -*-
import json, io, re

pd = json.load(io.open("_MYCHK_gL08ocr_live.json", encoding="utf-8"))
pre = json.load(io.open("_MYCHK_gL08ocr_pre.json", encoding="utf-8"))
findings = []

def trap(h, ys):
    inside = sum(ys[1:-1])
    return (h/2.0)*(ys[0]+ys[-1]+2*inside)

# --- fresh-solve each problem bank display (manual reference solutions) ---
# We recompute independently from the display numbers.
expected = {
 ("gold",0): trap(1,[1,2,5,10,17]),          #26
 ("gold",1): trap(2,[0,8,12,20]),            #60
 ("gold",2): round((48.5-45)/45*100,1),      #7.8
 ("gold",3): round((9.261-6.859)/0.2,3),     #12.01
 ("gold",4): trap(0.5,[1,1.5,2.5,4,6]),      #5.75
 ("bronze",0): (12-4)/(6-2),                 #2
 ("bronze",1): (11-5)/(3-1),                 #3
 ("bronze",2): (10-2)/(2-0),                 #4
 ("bronze",3): 3*5,                          #15
 ("bronze",4): 4*6/2,                        #12
 ("bronze",5): 1,                            #increasing
 ("bronze",6): (4+6)/2*4,                    #20
 ("bronze",7): (7-7)/(5-3),                  #0
 ("silver",0): trap(2,[1,6,13]),             #26
 ("silver",1): trap(1,[0,1,4,9]),            #9.5
 ("silver",2): (-2-6)/(3-(-1)),              #-2
 ("silver",3): trap(0.5,[2,3,5,8,12]),       #11.5
 ("silver",4): 0,                            #MC index 0 = Turning point
 ("silver",5): trap(1,[2,4,8]),              #9
 ("silver",6): trap(2,[0,4,16]),             #24
}
for tier in ["gold","bronze","silver"]:
    arr = pd["problem_bank"][tier]
    for i,p in enumerate(arr):
        sol = p["solutions"][0]
        exp = expected[(tier,i)]
        if abs(sol-exp) > 1e-9:
            findings.append(f"SOLUTION MISMATCH {tier}[{i}]: stored {sol} vs computed {exp}  display={p['display'][:60]}")

# --- recompute every guided_steps box (arithmetic in 'pre') ---
def eval_pre(pre_str):
    # extract an arithmetic expression from a 'pre' like "16.81 - 15.21 = "
    s = pre_str.replace("−","-").replace("×","*").replace("÷","/")
    # take substring before '='
    if "=" in s:
        s = s.split("=")[0]
    # strip leading words: keep only the trailing math expression
    m = re.search(r'[-+]?[0-9().\s+\-*/]+$', s)
    if not m: return None
    expr = m.group(0).strip()
    # guard: must contain an operator or be a bare number
    try:
        return eval(expr, {"__builtins__":{}}, {})
    except Exception:
        return None

def check_boxes(steps, label):
    for j,st in enumerate(steps):
        if "answer" not in st: continue
        pre = st.get("pre","")
        val = eval_pre(pre)
        if val is None:
            # boxes like "base = ", "answer = " that are read-offs; skip arithmetic
            continue
        if abs(val - st["answer"]) > 1e-6:
            findings.append(f"BOX MISMATCH {label}[{j}]: pre='{pre}' evaluates {val} but answer={st['answer']}")

for tier in ["gold","bronze","silver"]:
    for i,p in enumerate(pd["problem_bank"][tier]):
        if "guided_steps" in p:
            check_boxes(p["guided_steps"], f"{tier}[{i}].guided_steps")
for tier in ["bronze","silver","gold"]:
    check_boxes(pd["guided"]["teach"][tier]["steps"], f"teach.{tier}")
check_boxes(pd["guided"]["opener"]["steps"], "opener")

# --- reproduce misconception expects ---
# committed-error recompute per pattern
def mc_expect(tier,i,p):
    disp = p["display"]
    d = {}
    return None
# manual expected wrong-answers
mc_manual = {
 ("gold",0): 0.5*(1+17+(2+5+10)),   # middle once =17.5
 ("gold",1): (2/2)*(0+20+(8+12)),   # 40
 ("gold",2): round(3.5/48.5*100,1), # 7.2
 ("gold",3): 2.402,                 # wrong_run /1
 ("gold",4): 0.25*(1+6+(1.5+2.5+4)),# 3.75
 ("bronze",0): 4/8,                 #0.5
 ("bronze",1): 6,                   #rise only
 ("bronze",2): 2/8,                 #0.25
 ("bronze",3): 3+5,                 #8
 ("bronze",4): 24,                  #forgot half
 ("bronze",5): 0,
 ("bronze",6): (4+6)*4,             #40
 ("bronze",7): 2,                   #used run
 ("silver",0): 1*(1+13+6),          #20
 ("silver",1): 0.5*(0+9+(1+4)),     #7
 ("silver",2): 2,                   #sign
 ("silver",3): 0.25*(2+12+(3+5+8)), #7.5
 ("silver",4): None,
 ("silver",5): 0.5*(2+8+4),         #7
 ("silver",6): 1*(0+16+4),          #20
}
for tier in ["gold","bronze","silver"]:
    for i,p in enumerate(pd["problem_bank"][tier]):
        for k,mc in enumerate(p.get("misconceptions",[])):
            exp = mc.get("expect")
            man = mc_manual.get((tier,i))
            if exp is None:
                continue
            if man is None:
                findings.append(f"EXPECT check {tier}[{i}].mc[{k}]: stored {exp} but no manual model")
                continue
            if abs(exp-man) > 1e-6:
                findings.append(f"EXPECT MISMATCH {tier}[{i}].mc[{k}]: stored {exp} vs committed-error {man} (pattern {mc.get('pattern')})")

# --- em dash sweep in student-facing strings ---
def walk(o, path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=="note": continue
            walk(v, path+"/"+k)
    elif isinstance(o,list):
        for idx,v in enumerate(o):
            walk(v, f"{path}[{idx}]")
    elif isinstance(o,str):
        if "—" in o:
            findings.append(f"EM DASH at {path}: {o[:60]}")
walk(pd)

# --- preservation vs pre-dump: related_videos, topic_links, worked_examples ---
for key in ["related_videos","topic_links","worked_examples"]:
    if json.dumps(pre.get(key),sort_keys=True) != json.dumps(pd.get(key),sort_keys=True):
        findings.append(f"PRESERVATION CHANGED: {key}")

# display/solutions preserved per problem (numbers/text unchanged)
for tier in ["gold","bronze","silver"]:
    pre_arr = pre["problem_bank"].get(tier,[])
    live_arr = pd["problem_bank"].get(tier,[])
    if len(pre_arr)!=len(live_arr):
        findings.append(f"PB LENGTH CHANGED {tier}: pre {len(pre_arr)} live {len(live_arr)}")
        continue
    for i,(a,b) in enumerate(zip(pre_arr,live_arr)):
        if json.dumps(a.get("solutions"))!=json.dumps(b.get("solutions")):
            findings.append(f"SOLUTION CHANGED vs predump {tier}[{i}]: {a.get('solutions')} -> {b.get('solutions')}")

print("FINDINGS:", len(findings))
for f in findings: print(" -", f)
