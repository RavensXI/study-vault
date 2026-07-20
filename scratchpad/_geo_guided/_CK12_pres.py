import json,io
pre=json.load(open('_CK12_pre.json',encoding='utf-8'))['pd']
live=json.load(open('_CK12_live.json',encoding='utf-8'))
o=[]
for f in ("worked_examples","exam_context","method_card"):
    o.append("== PRE %s ==\n%s"%(f,json.dumps(pre.get(f),ensure_ascii=False,indent=1)))
    o.append("== LIVE %s ==\n%s"%(f,json.dumps(live.get(f),ensure_ascii=False,indent=1)))
open('_CK12_pres.txt','w',encoding='utf-8').write("\n".join(o))
