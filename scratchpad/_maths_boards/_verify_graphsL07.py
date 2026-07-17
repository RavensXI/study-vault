# -*- coding: utf-8 -*-
import json, io, math
pd=json.load(io.open("lesson_maths-aqa_graphs-L07.json",encoding="utf-8"))
errs=[]
pb=pd["problem_bank"]

# fresh solutions (from display), keyed by tier,index
expected={
 "bronze":{0:[5]},
 "silver":{2:[3],3:[1,2]},
 "gold":{0:[4],1:[2],2:[-3],4:[3]},
}
for t,mp in expected.items():
    for i,sol in mp.items():
        got=pb[t][i]["solutions"]
        if got!=sol: errs.append(f"{t}[{i}] solution {got} != fresh {sol}")

# check every non-MC guided_steps final box lands on solution (value)
def final_val(p):
    steps=p.get("guided_steps") or []
    for st in reversed(steps):
        if st.get("answer") is not None: return st["answer"]
    return None
for t in ("bronze","silver","gold"):
    for i,p in enumerate(pb[t]):
        if p.get("input_type")=="multiple_choice": continue
        fv=final_val(p)
        sol=p["solutions"]
        target = sol[0] if len(sol)==1 else None
        if len(sol)==2 and sol==[1,2]: target=0.5  # fraction ½
        if target is not None and abs(float(fv)-float(target))>1e-6:
            errs.append(f"{t}[{i}] final box {fv} != target {target}")

# recompute continuity of key guided walks
def bx(p): return [s for s in p["guided_steps"] if s.get("answer") is not None]
# spot-check gold[0]: 4,3,4
assert [s["answer"] for s in bx(pb["gold"][0])]==[4,3,4], "gold0 boxes"
assert [s["answer"] for s in bx(pb["gold"][1])]==[2,-3,2], "gold1 boxes"
assert [s["answer"] for s in bx(pb["gold"][2])]==[2,-3,-3], "gold2 boxes"
assert [s["answer"] for s in bx(pb["gold"][4])]==[3,0,3], "gold4 boxes"
assert [s["answer"] for s in bx(pb["silver"][2])]==[6,15,3], "silver2 boxes"
assert [s["answer"] for s in bx(pb["silver"][3])]==[0.5,3,0.5], "silver3 boxes"
assert [s["answer"] for s in bx(pb["bronze"][0])]==[7,15,5], "bronze0 boxes"

# expects must equal committed error and != correct
def check_expect(t,i,exp_map):
    for m in pb[t][i]["misconceptions"]:
        e=m.get("expect")
        if e is None: continue
        pat=m["pattern"]
        if pat in exp_map and e!=exp_map[pat]:
            errs.append(f"{t}[{i}] expect {pat}={e} != {exp_map[pat]}")
check_expect("gold",0,{"swap_components":3,"inside_sign":-4})
check_expect("gold",1,{"inside_sign":8})
check_expect("gold",2,{"outside_sign":1,"ignore_outside":-1})
check_expect("gold",4,{"multiply_not_divide":12,"x_unchanged":6})

# duplicate non-MC solutions within tier
for t in ("bronze","silver","gold"):
    seen={}
    for i,p in enumerate(pb[t]):
        if p.get("input_type")=="multiple_choice": continue
        key=tuple(p["solutions"])
        if key in seen: errs.append(f"{t}: dup non-MC solution {key} at [{seen[key]}] and [{i}]")
        seen[key]=i

# chart point verification
def verify_chart(t,i,fn,which):
    ch=pb[t][i]["chart"]; ds=ch["data"]["datasets"][which]
    for pt in ds["data"]:
        y=fn(pt["x"])
        if abs(y-pt["y"])>0.01: errs.append(f"{t}[{i}] chart ds{which} at x={pt['x']}: {pt['y']} != {y}")
verify_chart("silver",0,lambda x:x*x,0); verify_chart("silver",0,lambda x:x*x+7,1)
verify_chart("silver",1,lambda x:x*x,0); verify_chart("silver",1,lambda x:(x+5)**2,1)
verify_chart("silver",6,lambda x:math.sin(math.radians(x)),0); verify_chart("silver",6,lambda x:-math.sin(math.radians(x)),1)
# gold teach chart
tc=pd["guided"]["teach"]["gold"]["chart"]
for pt in tc["data"]["datasets"][1]["data"]:
    if abs(((pt["x"]+1)**2-4)-pt["y"])>0.01: errs.append(f"teach.gold chart at x={pt['x']}")

# MC correct-option answers point to a true statement (spot map)
mc_correct={
 ("bronze",1):"Down 3",("bronze",2):"Right 4",("bronze",3):"Left 2",("bronze",4):"x-axis",
 ("bronze",5):"y-axis",("bronze",6):r"\((3, 9)\)",("bronze",7):r"\((3, 6)\)",
 ("silver",0):"Translation up 7",("silver",1):"Translation left 5",("silver",4):r"\((4, 6)\)",
 ("silver",5):r"\((2, 2)\)",("silver",6):"Reflection in the x-axis",
 ("gold",3):r"Minimum at \((1, -4)\)",
}
for (t,i),want in mc_correct.items():
    opt=pb[t][i]["options"][pb[t][i]["solutions"][0]]
    if opt!=want: errs.append(f"{t}[{i}] MC correct option '{opt}' != '{want}'")

# opener boxes
ob=[s for s in pd["guided"]["opener"]["steps"] if s.get("answer") is not None]
assert [s["answer"] for s in ob]==[8,4], "opener boxes"

# every problem has hint
for t in ("bronze","silver","gold"):
    for i,p in enumerate(pb[t]):
        if not (p.get("hint") or "").strip(): errs.append(f"{t}[{i}] no hint")

if errs:
    print("FAIL:")
    for e in errs: print("  -",e)
else:
    print("ALL VERIFY CHECKS PASS")
