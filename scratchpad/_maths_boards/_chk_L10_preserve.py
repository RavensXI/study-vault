import json
ID="0c881c07-49bb-49cd-8c89-41b971335061"
live=json.load(open("_CHK_L10_live.json",encoding="utf-8"))
dump=json.load(open("_pre_dump_maths-aqa.json",encoding="utf-8"))
# find the lesson in dump
def find(d):
    if isinstance(d,list):
        for it in d:
            r=find(it)
            if r: return r
    elif isinstance(d,dict):
        if d.get("id")==ID: return d
        for v in d.values():
            r=find(v)
            if r: return r
    return None
pre=find(dump)
print("found pre-dump:", pre is not None)
if pre:
    ppd=pre.get("practice_data",pre)
    for f in ["related_videos","topic_links","worked_examples"]:
        a=json.dumps(ppd.get(f),sort_keys=True,ensure_ascii=False)
        b=json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
        print(f"{f}: {'UNCHANGED' if a==b else 'CHANGED'}")
        if a!=b:
            print("  PRE :",a[:300])
            print("  LIVE:",b[:300])
    print("pre keys:",list(ppd.keys()))
