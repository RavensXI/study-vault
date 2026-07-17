import json
ID="5c10e089-e2cc-4a61-b6b3-951a8994a1a0"
pre=json.load(open("_pre_dump_maths-eduqas.json",encoding="utf-8"))
# figure out structure
if isinstance(pre,dict):
    print("dict keys sample:", list(pre.keys())[:5])
    entry=pre.get(ID)
elif isinstance(pre,list):
    entry=None
    for r in pre:
        if r.get("id")==ID: entry=r;break
    print("list len", len(pre))
print("found entry:", entry is not None)
pd = entry.get("practice_data") if entry and "practice_data" in entry else entry
if pd:
    print("pre top keys:", list(pd.keys()))
    print("related_videos:", json.dumps(pd.get("related_videos")))
    print("topic_links:", json.dumps(pd.get("topic_links")))
    we=pd.get("worked_examples")
    print("worked_examples n:", len(we) if we else we)
    print("has guided pre?:", "guided" in pd, "tier_guides pre?:", "tier_guides" in pd)
    # dump questions displays for compare
    pb=pd.get("problem_bank",{})
    for t in ("bronze","silver","gold"):
        arr=pb.get(t,[])
        print(t, "pre n=", len(arr))
