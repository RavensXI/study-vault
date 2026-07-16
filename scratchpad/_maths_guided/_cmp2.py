import json
ID="68997180-8486-4551-ab42-0a1b98384336"
live=json.load(open("_live_L01.json",encoding="utf-8"))
dump=json.load(open("_pre_fanout_dump.json",encoding="utf-8"))

def locate(o):
    if isinstance(o,dict):
        if o.get("id")==ID: return o
        for v in o.values():
            r=locate(v)
            if r: return r
    if isinstance(o,list):
        for x in o:
            r=locate(x)
            if r: return r
    return None
e=locate(dump)
if e is None:
    print("NOT FOUND; top type", type(dump), list(dump)[:5] if isinstance(dump,dict) else len(dump))
else:
    pre=e.get("practice_data") or e
    for f in ["related_videos","topic_links","worked_examples","method_card"]:
        a=json.dumps(pre.get(f),sort_keys=True,ensure_ascii=False)
        b=json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
        print(f, "SAME" if a==b else "DIFFERENT")
    print("PRE keys:", list(pre.keys()))
