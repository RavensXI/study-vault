import os, json, urllib.request, io, sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
ID="ee087e5f-7971-4f5d-b6e0-2fe13585d6f4"
key=os.environ["SUPABASE_SERVICE_KEY"]
url=f"https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.{ID}&select=practice_data"
req=urllib.request.Request(url, headers={"apikey":key,"Authorization":f"Bearer {key}"})
raw=json.load(urllib.request.urlopen(req))
pd=raw[0]["practice_data"]
json.dump(pd,open("_pd.json","w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("top keys:",list(pd.keys()))

# em/en dash scan (exclude note)
hits=[]
def walk(o,path):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=="note": continue
            walk(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,f"{path}[{i}]")
    elif isinstance(o,str):
        if "—" in o: hits.append(("EM",path,o))
        if "–" in o: hits.append(("EN",path,o))
walk(pd,"")
print("dash hits:",len(hits))
for t,p,s in hits: print("  ",t,p,"::",s[:70])

# numeric answer boxes
bad=[]
def cb(o,path):
    if isinstance(o,dict):
        if "answer" in o:
            a=o["answer"]
            if isinstance(a,bool) or not isinstance(a,(int,float)): bad.append((path,repr(a)))
        for k,v in o.items(): cb(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o): cb(v,f"{path}[{i}]")
cb(pd,"")
print("non-numeric answer boxes:",bad)

pb=pd["problem_bank"]
for t in ["gold","bronze","silver"]:
    arr=pb[t]; print(t,"size",len(arr))
    for i,p in enumerate(arr):
        sol=p["solutions"];opts=p.get("options",[]);it=p.get("input_type")
        if it=="multiple_choice":
            for s in sol:
                if not (0<=s<len(opts)): print("  BAD SOL",t,i,s)
        if opts and len(set(opts))!=len(opts): print("  DUP OPTS",t,i)
        # expects within options range
        for j,m in enumerate(p.get("misconceptions",[])):
            e=m.get("expect")
            if e is not None and it=="multiple_choice" and not(0<=e<len(opts)):
                print("  BAD EXPECT",t,i,j,e)
            if e is not None and e in sol:
                print("  EXPECT==SOLUTION",t,i,j,e)
print("done")
