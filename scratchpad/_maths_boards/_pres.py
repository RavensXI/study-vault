import json, io
pd=json.load(io.open("_live_L06.json",encoding="utf-8"))
pre=json.load(io.open("_pre_dump_maths-aqa.json",encoding="utf-8"))
ID="e15d6925-608b-4c05-aa82-c4782d1657b3"
row=None
for r in pre:
    if r.get("id")==ID or (isinstance(r,dict) and r.get("id")==ID):
        row=r; break
if row is None:
    # maybe keyed differently
    print("keys of first:", list(pre[0].keys()))
    for r in pre:
        pdp=r.get("practice_data") or {}
        # match by topic_links slug
    row=None
print("found:", row is not None)
if row:
    ppd=row.get("practice_data",{})
    for f in ("topic_links","related_videos","worked_examples"):
        same = json.dumps(ppd.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(pd.get(f),sort_keys=True,ensure_ascii=False)
        print(f, "preserved:", same)
        if not same:
            print("  PRE:", json.dumps(ppd.get(f),ensure_ascii=False)[:300])
            print("  NEW:", json.dumps(pd.get(f),ensure_ascii=False)[:300])
