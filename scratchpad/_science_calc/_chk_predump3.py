import json, re
canon="e68bcd00-8b3f-47d3-9a5b-e327a9ddde48"
prop="3848d92a-26c5-4ebf-a4d4-7f55b392e888"
pd=json.load(open("_pre_dump_all.json",encoding="utf-8"))
def find(rid):
    for it in pd:
        if it.get("id")==rid: return it
    return None
for rid,name in [(canon,"CANON"),(prop,"PROP")]:
    c=find(rid)
    print(f"=== {name} {rid} found={c is not None}")
    if c:
        print("  title:", c.get("title"), "| subject:", c.get("subject"),"| unit:",c.get("unit"),"| n:",c.get("n"),"| fp:",c.get("fp"))
        p=c.get("pd",{})
        print("  pd top keys:", sorted(p.keys()))
        print("  method_card.title:", p.get("method_card",{}).get("title"))
        pb=p.get("problem_bank",{})
        for t in ["bronze","silver","gold"]:
            arr=pb.get(t,[])
            print(f"  pre {t}: {len(arr)}; sols={[x.get('solutions') for x in arr]}")
            for i,x in enumerate(arr):
                print(f"     {t}[{i}] accept={x.get('accept')} unit={x.get('unit')!r} ho={x.get('higher_only')} :: {re.sub('<[^>]+>','',str(x.get('display','')))[:65]}")
