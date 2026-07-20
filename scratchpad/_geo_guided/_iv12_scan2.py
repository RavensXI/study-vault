import json, os, re
d=os.path.dirname(os.path.abspath(__file__))
live=json.load(open(os.path.join(d,"_iv12_live.json"),encoding="utf-8"))
pre=json.load(open(os.path.join(d,"_iv12_pre.json"),encoding="utf-8"))["pd"]
issues=[]
for t in ("bronze","silver","gold"):
    L=live["problem_bank"][t]; P=pre["problem_bank"][t]
    if len(L)!=len(P): issues.append("%s length %d vs pre %d"%(t,len(L),len(P)))
    for i,(l,p) in enumerate(zip(L,P)):
        path="%s[%d]"%(t,i)
        for k in ("image","chart","ruler","options","input_type","display","solutions","calculator"):
            if (k in p) != (k in l):
                issues.append("%s: key %s presence pre=%s live=%s"%(path,k,k in p,k in l))
            elif k in p and p[k]!=l[k]:
                issues.append("%s: %s CHANGED\n   pre=%s\n   live=%s"%(path,k,json.dumps(p[k],ensure_ascii=False)[:400],json.dumps(l[k],ensure_ascii=False)[:400]))
# other top fields
for k in ("worked_examples","topic_links","exam_context","related_videos"):
    if k in pre and pre.get(k)!=live.get(k):
        issues.append("TOP %s changed"%k)
    if k in pre and k not in live: issues.append("TOP %s dropped"%k)
print("\n".join(issues) if issues else "no stimulus/answer diffs")
print("\n--- pre top keys:", list(pre.keys()))
print("--- live top keys:", list(live.keys()))
