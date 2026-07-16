import json, io
ID="76260360-c757-49f2-a1c6-cf0e389564c3"
live=json.load(io.open("_checker_live.json",encoding="utf-8"))
dump=json.load(io.open("_pre_fanout_dump.json",encoding="utf-8"))
entry=[e for e in dump if e.get("id")==ID][0]
pre=entry.get("practice_data",entry)
io.open("_we_pre.json","w",encoding="utf-8").write(json.dumps(pre.get("worked_examples"),indent=2,ensure_ascii=False))
io.open("_we_live.json","w",encoding="utf-8").write(json.dumps(live.get("worked_examples"),indent=2,ensure_ascii=False))
# also dump full pre for reference
print("wrote _we_pre.json _we_live.json")
# quick question-list compare
pq=[w.get("question") for w in pre.get("worked_examples",[])]
lq=[w.get("question") for w in live.get("worked_examples",[])]
print("PRE questions:", pq)
print("LIVE questions:", lq)
