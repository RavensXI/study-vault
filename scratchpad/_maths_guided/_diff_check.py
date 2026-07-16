import json,io
live=json.load(io.open("_geomL07_LIVE_NOW.json",encoding="utf-8"))
new=json.load(io.open("lesson_geometry-L07_diagrams.json",encoding="utf-8"))
def walk(a,b,path,diffs):
    if type(a)!=type(b): diffs.append(path+" TYPE"); return
    if isinstance(a,dict):
        for k in set(a)|set(b):
            if k not in a or k not in b: diffs.append(path+"."+str(k)+" KEY"); continue
            walk(a[k],b[k],path+"."+str(k),diffs)
    elif isinstance(a,list):
        if len(a)!=len(b): diffs.append(path+" LEN %d!=%d"%(len(a),len(b))); return
        for i,(x,y) in enumerate(zip(a,b)): walk(x,y,path+"[%d]"%i,diffs)
    else:
        if a!=b: diffs.append(path)
d=[]
walk(live,new,"pd",d)
print("changed paths (%d):"%len(d))
for p in d: print("  ",p)
