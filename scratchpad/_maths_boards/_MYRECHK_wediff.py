import json
ID="fc1f101a-9d1b-4eab-8bf8-8159f78caea2"
pd=json.load(open("_MYRECHK_live.json",encoding="utf-8"))
pre=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
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
ppd=findpre(pre)["practice_data"]
# normalize by removing em dash / colon distinction in labels
def norm(s): return s.replace("—",":").replace(" :",":") if isinstance(s,str) else s
def deep(o):
    if isinstance(o,dict): return {k:deep(v) for k,v in o.items()}
    if isinstance(o,list): return [deep(v) for v in o]
    return norm(o)
a=json.dumps(deep(ppd["worked_examples"]),sort_keys=True)
b=json.dumps(deep(pd["worked_examples"]),sort_keys=True)
print("worked_examples identical after em-dash→colon normalisation:", a==b)
