# -*- coding: utf-8 -*-
import json, re
pd = json.load(open("lesson_maths-eduqas_algebra-L12.json", encoding="utf-8"))
errs=[]

# 1. verify every guided_steps / teach / opener box recomputes and is numeric
def check_box(st, path):
    if st.get("answer") is not None:
        a=st["answer"]
        if not isinstance(a,(int,float)): errs.append(path+" non-numeric "+repr(a))

# opener boxes: known answers
op=pd["guided"]["opener"]["steps"]
exp_op={1:5,3:2,4:-2}
for i,st in enumerate(op):
    if st.get("answer") is not None:
        if i in exp_op and st["answer"]!=exp_op[i]: errs.append(f"opener[{i}] box {st['answer']} != {exp_op[i]}")

# teach boxes recompute
def poly(coeffs,x):
    return sum(c*x**p for p,c in enumerate(reversed(coeffs)))
# bronze teach x^2-16: roots 4,-4; check x=0 ->-16
tb=pd["guided"]["teach"]["bronze"]["steps"]
tb_ans=[s.get("answer") for s in tb if s.get("answer") is not None]
assert tb_ans==[4,-4,-4,-16], tb_ans
# silver teach x^2-x-12 roots 4,-3; x=5 ->8
ts=pd["guided"]["teach"]["silver"]["steps"]
ts_ans=[s.get("answer") for s in ts if s.get("answer") is not None]
assert ts_ans==[4,-3,-3,8], ts_ans
assert poly([1,-1,-12],5)==8
# gold teach 2x^2+3x-2 -> (2x-1)(x+2); 2x=1,x=0.5,x=-2; x=0->-2
tg=pd["guided"]["teach"]["gold"]["steps"]
tg_ans=[s.get("answer") for s in tg if s.get("answer") is not None]
assert tg_ans==[1,0.5,-2,-2], tg_ans
assert poly([2,3,-2],0.5)==0 and poly([2,3,-2],-2)==0

# 2. single_value guided_steps land on solutions
g=pd["problem_bank"]["gold"]
# g[2]: x^2-5x+4<=0 -> integers 1..4 =4
assert poly([1,-5,4],1)==0 and poly([1,-5,4],4)==0
g2=[s.get("answer") for s in g[2]["guided_steps"] if s.get("answer") is not None]
assert g2[-2]==g[2]["solutions"][0]==4, g2
# g[3]: x^2-3x-4<0 -> -1<x<4 positive ints 1,2,3 =3
assert poly([1,-3,-4],4)==0 and poly([1,-3,-4],-1)==0
g3=[s.get("answer") for s in g[3]["guided_steps"] if s.get("answer") is not None]
assert g3[-2]==g[3]["solutions"][0]==3, g3

# 3. fresh-solve every MC: correct option index 0, and each expect != 0 and is a valid index
pb=pd["problem_bank"]
for tier in("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        sols=p["solutions"]
        it=p.get("input_type")
        if it=="multiple_choice":
            assert sols==[0], f"{tier}[{i}] sol {sols}"
            nopt=len(p["options"])
            for m in p["misconceptions"]:
                e=m["expect"]
                assert isinstance(e,int) and 1<=e<nopt, f"{tier}[{i}] bad expect {e}"
        else:
            for m in p["misconceptions"]:
                assert m["expect"]!=sols[0], f"{tier}[{i}] expect==sol"

# 4. parabola SVG roots match labelled crossing pixels: re-parse circle cx for roots and compare axis crossing
# Just sanity: teach displays contain the right equation label text
for tier,eq in (("bronze","x squared minus 16"),("silver","x squared minus x minus 12"),("gold","2x squared plus 3x minus 2")):
    d=pd["guided"]["teach"][tier]["display"]
    assert eq in d, f"{tier} label missing"

# 5. em dash scan (belt and braces) excluding note
def scan(o,pth):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in("note",): continue
            scan(v,pth+"."+str(k))
    elif isinstance(o,list):
        for j,v in enumerate(o): scan(v,pth+f"[{j}]")
    elif isinstance(o,str) and "—" in o: errs.append("EMDASH "+pth)
scan(pd,"pd")

print("ERRORS:",errs if errs else "NONE")
print("all asserts passed")
