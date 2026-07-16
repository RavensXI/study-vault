import json
ID = "ea8d68a2-63b8-40e9-87de-f879156e0d93"
pre = json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
def search(obj):
    r=[]
    if isinstance(obj,dict):
        if obj.get("id")==ID: r.append(obj)
        for v in obj.values(): r+=search(v)
    elif isinstance(obj,list):
        for v in obj: r+=search(v)
    return r
res=search(pre)
print("found",len(res))
if res:
    e=res[0]
    pd=e.get("practice_data") or e
    if "practice_data" in e: pd=e["practice_data"]
    json.dump(pd,open("_pre_l05.json","w",encoding="utf-8"),indent=2,ensure_ascii=False)
    print("pre keys:",list(pd.keys()))
    for k in ["related_videos","topic_links","worked_examples"]:
        print(k,"present:",k in pd)
