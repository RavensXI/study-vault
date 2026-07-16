import json
live = json.load(open("_CHK_L06_LIVE_fresh.json", encoding="utf-8"))

def walk(o, path=""):
    if isinstance(o, dict):
        for k,v in o.items():
            walk(v, f"{path}/{k}")
    elif isinstance(o, list):
        for i,v in enumerate(o):
            walk(v, f"{path}[{i}]")
    elif isinstance(o, str):
        for dash in ["—","–"]:
            if dash in o:
                # note fields exempt
                if path.endswith("/note"): continue
                print(f"EMDASH({repr(dash)}) at {path}: {o[:80]}")

walk(live)
print("--- em-dash scan done ---")

# Check all guided_steps/opener/teach box answers are numeric
def check_boxes(steps, label):
    for i,s in enumerate(steps):
        if isinstance(s,dict) and "answer" in s:
            a=s["answer"]
            if not isinstance(a,(int,float)) or isinstance(a,bool):
                print(f"NON-NUMERIC answer {label}[{i}]: {repr(a)}")

for tier in ["gold","silver","bronze"]:
    check_boxes(live["guided"]["teach"][tier]["steps"], f"teach.{tier}")
check_boxes(live["guided"]["opener"]["steps"], "opener")
for tier,probs in live["problem_bank"].items():
    if isinstance(probs,list):
        for pi,p in enumerate(probs):
            for gi,s in enumerate(p.get("guided_steps",[])):
                if "answer" in s and (not isinstance(s["answer"],(int,float)) or isinstance(s["answer"],bool)):
                    print(f"NON-NUMERIC {tier}[{pi}].guided_steps[{gi}]: {repr(s['answer'])}")
print("--- numeric scan done ---")

# hint fields: no LaTeX backslash
def check_hints(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=="hint" and isinstance(v,str) and ("\\(" in v or "$" in v):
                print(f"HINT has LaTeX {path}: {v}")
            walk_h(v,f"{path}/{k}")
def walk_h(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=="hint" and isinstance(v,str) and ("\\(" in v or "$" in v):
                print(f"HINT has LaTeX {path}/{k}: {v}")
            walk_h(v,f"{path}/{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o): walk_h(v,f"{path}[{i}]")
walk_h(live)
print("--- hint LaTeX scan done ---")
