import json, math, re
pd=json.load(open("lesson_algebra-L10_diagrams.json",encoding="utf-8"))
gold=pd["problem_bank"]["gold"]
for idx in (0,1,2,3):
    d=gold[idx]["display"]
    r=float(re.search(r'<circle cx="130" cy="105" r="([\d.]+)"',d).group(1))
    dots=re.findall(r'<circle cx="([\d.]+)" cy="([\d.]+)" r="3.2"',d)
    ds=[math.hypot(float(x)-130,float(y)-105) for x,y in dots]
    ok=all(abs(dd-r)<1.5 for dd in ds)
    # confirm original question text still present
    qtext = "Give the two x-values." in d and "\(" in d
    print("gold[%d] r_px=%.1f dot_dists=%s ON_CIRCLE=%s qtext_kept=%s ndots=%d"%(idx,r,[round(x,1) for x in ds],ok,qtext,len(dots)))
# preservation: everything except the 4 gold displays unchanged vs live
live=json.load(open("_L10_live_fresh.json",encoding="utf-8"))
diffs=[]
def walk(a,b,path):
    if isinstance(a,dict):
        for k in a:
            walk(a[k],b.get(k),path+"."+str(k))
    elif isinstance(a,list):
        for i,x in enumerate(a):
            walk(x,b[i] if isinstance(b,list) and i<len(b) else None,path+"[%d]"%i)
    else:
        if a!=b: diffs.append(path)
walk(pd,live,"pd")
print("changed paths:",diffs)
