# -*- coding: utf-8 -*-
import json, re, math

pd = json.load(open("_chk32_canonical.json", encoding="utf-8"))
blob = json.dumps(pd, ensure_ascii=False)

# board neutrality
for term in ["AQA","Edexcel","OCR","Eduqas","WJEC","equation sheet","formula sheet","must memoris","must memoriz","on your sheet","given to you"]:
    if term.lower() in blob.lower():
        print("BOARD/SHEET TERM FOUND:", term)

# em/en dash scan in student-facing (exclude note)
def scan(o, path):
    if isinstance(o, dict):
        for k,v in o.items():
            if k=="note": continue
            scan(v, path+"."+str(k))
    elif isinstance(o, list):
        for i,v in enumerate(o): scan(v, path+"[%d]"%i)
    elif isinstance(o, str):
        if "—" in o: print("EM DASH at",path,":",o[:60])
        if "–" in o: print("EN DASH at",path,":",o[:60])
scan(pd,"pd")

# expects vs accept window
def solve_bank():
    pb=pd["problem_bank"]
    for tier in ("bronze","silver","gold"):
        for i,p in enumerate(pb[tier]):
            sols=p.get("solutions"); acc=p.get("accept")
            for j,m in enumerate(p.get("misconceptions") or []):
                e=m.get("expect")
                if e is None: continue
                ev=e if isinstance(e,list) else [e]
                if len(ev)==len(sols):
                    for a,b in zip(ev,sols):
                        d=abs(float(a)-float(b))
                        win = acc if acc is not None else 0.011
                        if d<=win:
                            print("DEAD EXPECT %s[%d].misc[%d] expect=%s sol=%s acc=%s"%(tier,i,j,a,b,acc))
solve_bank()
print("done scan")
