import json, io, re
ID="865c281d-5f92-4fb7-b30d-4ae2d604a404"
live=json.load(io.open("_chk02_live.json",encoding="utf-8"))
dump=json.load(io.open("_pre_fanout_dump.json",encoding="utf-8"))
# find pre entry
pre=None
def find(o):
    global pre
    if isinstance(o,dict):
        if o.get("id")==ID or o.get("lesson_id")==ID: 
            pre=o; return
        for v in o.values(): find(v)
    elif isinstance(o,list):
        for v in o: find(v)
find(dump)
if pre is None:
    # dump maybe keyed by id
    if ID in dump: pre=dump[ID]
print("pre found:", pre is not None)
if pre:
    ppd = pre.get("practice_data") or pre
    print("pre keys:", list(ppd.keys()) if isinstance(ppd,dict) else type(ppd))
    for f in ["related_videos","topic_links","worked_examples"]:
        same = json.dumps(ppd.get(f),sort_keys=True,ensure_ascii=False)==json.dumps(live.get(f),sort_keys=True,ensure_ascii=False)
        print(f"{f}: {'UNCHANGED' if same else 'CHANGED'}")
        if not same:
            print("  PRE:", json.dumps(ppd.get(f),ensure_ascii=False)[:500])
            print("  LIVE:", json.dumps(live.get(f),ensure_ascii=False)[:500])
