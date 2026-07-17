import json
pre=json.load(open("_pre_dump_maths-ocr.json", encoding="utf-8"))
def find(o):
    if isinstance(o,dict):
        if o.get("id")=="24e576f2-0e8a-43bc-bacd-5397b4da617b":
            return o
        for v in o.values():
            r=find(v)
            if r: return r
    if isinstance(o,list):
        for v in o:
            r=find(v)
            if r: return r
    return None
e = pre.get("24e576f2-0e8a-43bc-bacd-5397b4da617b") if isinstance(pre,dict) else None
if e is None: e=find(pre)
print("found:", e is not None)
pd=e.get("practice_data", e)
print("pd keys:", list(pd.keys()))
for f in ["related_videos","topic_links","worked_examples"]:
    json.dump(pd.get(f), open(f"_pre_{f}.json","w"))
    print(f, "->", json.dumps(pd.get(f), ensure_ascii=False)[:300])
