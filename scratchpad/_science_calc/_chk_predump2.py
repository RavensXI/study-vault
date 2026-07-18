import json, io, re
canon="e68bcd00-8b3f-47d3-9a5b-e327a9ddde48"
prop="3848d92a-26c5-4ebf-a4d4-7f55b392e888"
pd=json.load(open("_pre_dump_all.json",encoding="utf-8"))
print("list len:", len(pd))
print("item0 keys:", list(pd[0].keys()) if pd else None)
def find(rid):
    for it in pd:
        if it.get("id")==rid: return it
    return None
c=find(canon)
print("canon found:", c is not None)
if c:
    p=c.get("practice_data",{})
    print("pre title:", p.get("method_card",{}).get("title"))
    pb=p.get("problem_bank",{})
    for t in ["bronze","silver","gold"]:
        arr=pb.get(t,[])
        print(f"pre {t}: {len(arr)} problems; sols={[x.get('solutions') for x in arr]}")
        for i,x in enumerate(arr):
            print(f"   {t}[{i}] accept={x.get('accept')} unit={x.get('unit')!r} higher_only={x.get('higher_only')} disp={re.sub('<[^>]+>','',str(x.get('display','')))[:70]}")
    print("pre top keys:", sorted(p.keys()))
