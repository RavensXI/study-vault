import json, io
ID="865c281d-5f92-4fb7-b30d-4ae2d604a404"
live=json.load(io.open("_chk02_live.json",encoding="utf-8"))
dump=json.load(io.open("_pre_fanout_dump.json",encoding="utf-8"))
pre=None
def find(o):
    global pre
    if isinstance(o,dict):
        if o.get("id")==ID or o.get("lesson_id")==ID: pre=o; return
        for v in o.values(): find(v)
    elif isinstance(o,list):
        for v in o: find(v)
find(dump)
ppd=pre.get("practice_data") or pre
io.open("_we_pre02.txt","w",encoding="utf-8").write(json.dumps(ppd.get("worked_examples"),indent=2,ensure_ascii=False))
io.open("_we_live02.txt","w",encoding="utf-8").write(json.dumps(live.get("worked_examples"),indent=2,ensure_ascii=False))
# also method_card and topic_links pre for reference
io.open("_mc_pre02.txt","w",encoding="utf-8").write(json.dumps(ppd.get("method_card"),indent=2,ensure_ascii=False))
print("written")
