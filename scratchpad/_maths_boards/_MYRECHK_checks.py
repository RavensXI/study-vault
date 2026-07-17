import json, re
pd = json.load(open("_MYRECHK_live.json", encoding="utf-8"))

# Find pre-dump entry for graphs-L03 (id fc1f101a...)
ID="fc1f101a-9d1b-4eab-8bf8-8159f78caea2"
pre=json.load(open("_pre_dump_maths-ocr.json", encoding="utf-8"))
def findpre(o):
    if isinstance(o,dict):
        if o.get("id")==ID: return o
        for v in o.values():
            r=findpre(v)
            if r: return r
    elif isinstance(o,list):
        for v in o:
            r=findpre(v)
            if r: return r
    return None
pe=findpre(pre)
print("pre-dump found:", pe is not None)
if pe:
    ppd = pe.get("practice_data", pe)
    if "practice_data" in pe: ppd=pe["practice_data"]
    print("pre top keys:", list(ppd.keys()) if isinstance(ppd,dict) else type(ppd))
    for k in ["related_videos","topic_links","worked_examples"]:
        same = json.dumps(ppd.get(k),sort_keys=True)==json.dumps(pd.get(k),sort_keys=True)
        print(f"  preserve {k}: {'SAME' if same else 'CHANGED'}")
        if not same:
            print("   PRE:", json.dumps(ppd.get(k))[:400])
            print("   NOW:", json.dumps(pd.get(k))[:400])

# em dash sweep in student-facing strings
def walk(o, path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=="note": continue
            walk(v, f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o):
            walk(v, f"{path}[{i}]")
    elif isinstance(o,str):
        if "—" in o:
            print("EM DASH at", path, ":", o[:80])
walk(pd)
print("em dash sweep done")
