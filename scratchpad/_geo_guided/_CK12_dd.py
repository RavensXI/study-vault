import json,difflib
pre=json.load(open('_CK12_pre.json',encoding='utf-8'))['pd']
live=json.load(open('_CK12_live.json',encoding='utf-8'))
o=[]
for f in ("worked_examples","exam_context"):
    a=json.dumps(pre.get(f),ensure_ascii=False,indent=1).splitlines()
    b=json.dumps(live.get(f),ensure_ascii=False,indent=1).splitlines()
    o.append("#### "+f)
    o+= list(difflib.unified_diff(a,b,lineterm="",n=0))
open('_CK12_dd.txt','w',encoding='utf-8').write("\n".join(o))
