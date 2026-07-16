import json, re

SID = "4d1ac99e-f293-4cce-a4d3-c276c5f8f24b"
live = json.load(open("_CHK_algL08_LIVE_verify.json", encoding="utf-8"))

# pre-dump
pre = json.load(open("_pre_fanout_dump.json", encoding="utf-8"))
entry = None
if isinstance(pre, list):
    for e in pre:
        if e.get("id")==SID: entry=e; break
elif isinstance(pre, dict):
    entry = pre.get(SID) or (pre.get("lessons",{}) or {}).get(SID)
    if entry is None:
        # maybe keyed differently
        for k,v in pre.items():
            if isinstance(v,dict) and v.get("id")==SID: entry=v;break
print("pre entry found:", entry is not None)
if entry:
    pd_pre = entry.get("practice_data", entry)
    for f in ["related_videos","topic_links","worked_examples"]:
        same = json.dumps(pd_pre.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
        print(f"{f}: {'UNCHANGED' if same else 'CHANGED'}")
    # method_card presence
    print("method_card in pre:", "method_card" in pd_pre, "keys pre:", list(pd_pre.keys()))

# em dash scan (U+2014) and en dash (U+2013) in student-facing strings
emdash_hits=[]
def walk(o,path):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=="note": continue  # internal exempt
            walk(v,f"{path}.{k}")
    elif isinstance(o,list):
        for i,v in enumerate(o):
            walk(v,f"{path}[{i}]")
    elif isinstance(o,str):
        if "—" in o: emdash_hits.append((path,"EM",o))
walk(live,"root")
print("em dash hits:", len(emdash_hits))
for h in emdash_hits: print("  ",h)
