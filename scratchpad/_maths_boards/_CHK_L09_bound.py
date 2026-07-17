import json,re
live=json.load(open("_CHK_L09eduqas_live.json",encoding="utf-8"))
pb=live["problem_bank"]
issues=[]
for tier in ["bronze","silver","gold"]:
    for pi,p in enumerate(pb[tier]):
        gs=p.get("guided_steps",[])
        first_phase=None
        for i,b in enumerate(gs):
            if b.get("phase")=="substitute": first_phase=i; break
        if first_phase is None:
            issues.append((f"{tier}[{pi}]","NO_PHASE")); continue
        boxes_before=sum(1 for b in gs[:first_phase] if "answer" in b)
        live_boxes=sum(1 for b in gs[first_phase:] if "answer" in b)
        if boxes_before<1: issues.append((f"{tier}[{pi}]","NO_BOX_BEFORE",boxes_before))
        if live_boxes<2: issues.append((f"{tier}[{pi}]","LIVE_LT2",live_boxes))
        # last box answer must equal a solution component
        lastnum=[b["answer"] for b in gs if "answer" in b]
        # check step is last; the x/y final should be among solutions
print("boundary issues:",issues if issues else "NONE")

# reproduce misconception expects for the two big patterns
def eqs_of(disp):
    c=disp.replace("\(","|").replace("\)","|")
    return [x for x in c.split("|") if "=" in x]
def pe(s):
    s=s.replace("−","-").replace(" ","");lhs,rhs=s.split("=");rhs=int(rhs)
    a=b=0
    for m in re.finditer(r'([+-]?\d*)x',lhs):
        t=m.group(1);a+=1 if t in("","+")else(-1 if t=="-"else int(t))
    for m in re.finditer(r'([+-]?\d*)y',lhs):
        t=m.group(1);b+=1 if t in("","+")else(-1 if t=="-"else int(t))
    return a,b,rhs

mism=[]
for tier in ["bronze","silver","gold"]:
    for pi,p in enumerate(pb[tier]):
        e=eqs_of(p["display"])
        (a1,b1,c1),(a2,b2,c2)=pe(e[0]),pe(e[1])
        for mi,mc in enumerate(p.get("misconceptions",[])):
            pat=mc["pattern"];exp=mc["expect"]
            mism.append((f"{tier}[{pi}].misconceptions[{mi}]",pat,exp))
print("\ntotal misconceptions:",len(mism))
for m in mism: print(m)
