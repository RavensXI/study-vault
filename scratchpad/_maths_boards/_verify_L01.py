# -*- coding: utf-8 -*-
import json, io
pd = json.load(io.open("_maths_boards/lesson_number-L01.json", encoding="utf-8"))
# Python expressions mirroring each display (BIDMAS via python precedence)
exprs = {
 "bronze": ["6+4*3","20-8/2","5*3+7*2","24/6+2*5","3+5*4-2","18/2*3","40-5*6+2","7+3*8/4"],
 "silver": ["(3+5)*4","6*(9-4)+3**2","2**3+4*(7-3)","50-(2+3)**2","3*(12-4)/6","100/(4+6)*3","4**2-3*(1+1)"],
 "gold":   ["(18+6)/2**2+5*3","(3+4)**2-5*(8-2)","5*6/3+4*(2+1)**2","2**4-(3*2+1)**0*8","((5-2)**3+3)/(2*5)"],
}
ok=True
for tier in ("bronze","silver","gold"):
    probs=pd["problem_bank"][tier]
    assert len(probs)==len(exprs[tier]), (tier,len(probs),len(exprs[tier]))
    seen=set()
    for i,(p,e) in enumerate(zip(probs,exprs[tier])):
        val=eval(e)
        sol=p["solutions"][0]
        if abs(val-sol)>1e-9:
            print("SOLUTION MISMATCH",tier,i,e,"->",val,"stored",sol); ok=False
        if sol in seen:
            print("DUP SOLUTION",tier,i,sol); ok=False
        seen.add(sol)
        # last box in guided_steps that has answer = final; check second-last (finishing) or check equals sol
        boxes=[s for s in p["guided_steps"] if s.get("answer") is not None]
        # the check box (last) should equal sol
        if abs(boxes[-1]["answer"]-sol)>1e-9:
            print("CHECK BOX != sol",tier,i,boxes[-1]["answer"],sol); ok=False
        # expect must not equal sol
        for m in p.get("misconceptions",[]):
            ex=m.get("expect")
            if ex is not None and abs(ex-sol)<1e-9:
                print("EXPECT==SOL",tier,i,ex); ok=False
# verify teach walks final boxes
teach_final={"bronze":11,"silver":8,"gold":2}
for t,v in teach_final.items():
    b=[s for s in pd["guided"]["teach"][t]["steps"] if s.get("answer") is not None]
    if abs(b[-1]["answer"]-v)>1e-9: print("TEACH final",t,b[-1]["answer"],v); ok=False
# opener
ob=[s for s in pd["guided"]["opener"]["steps"] if s.get("answer") is not None]
print("opener boxes",[s["answer"] for s in ob])
print("ALL OK" if ok else "FAILURES ABOVE")
