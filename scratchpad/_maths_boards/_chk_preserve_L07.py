import json
ID="80de6f33-3b1d-40af-9068-8e6fc132c36d"
pre=json.load(open("_pre_dump_maths-aqa.json",encoding="utf-8"))
# pre may be list or dict
if isinstance(pre,dict):
    # maybe keyed
    entry=None
    for k,v in pre.items():
        if isinstance(v,dict) and v.get("id")==ID: entry=v; break
        if k==ID: entry=v; break
    rows=pre if entry is None else None
else:
    entry=None
    for r in pre:
        if r.get("id")==ID: entry=r; break
print("found entry:", entry is not None)
if entry is None:
    # print structure
    print("type", type(pre))
    if isinstance(pre,list):
        print("len",len(pre),"sample keys", list(pre[0].keys())[:10] if pre else None)
        # try slug
        for r in pre:
            if r.get("slug")=="solving-quadratics-by-factorising" or (r.get("practice_data") and False):
                print("by slug found"); entry=r; break
    else:
        print("dict keys sample", list(pre.keys())[:5])
if entry:
    pd=entry.get("practice_data",{})
    print("pre related_videos:", json.dumps(pd.get("related_videos")))
    print("pre topic_links:", json.dumps(pd.get("topic_links")))
    print("pre worked_examples count:", len(pd.get("worked_examples",[])) if pd.get("worked_examples") else pd.get("worked_examples"))
    print("pre top keys:", list(pd.keys()))
    json.dump(pd, open("_pre_L07_pd.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
