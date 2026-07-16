import json
pre=json.load(open("_pre_fanout_dump.json",encoding="utf-8"))
lid="d9ac5103-221b-441e-81f2-d95e77269ea3"
ppd=[v for v in pre if v.get("id")==lid][0]["practice_data"]
for i,p in enumerate(ppd["problem_bank"]["gold"]):
    print("gold",i,repr(p["display"][:70]))
# count problems per tier pre vs live
live=json.load(open("_live_graphs_l04.json",encoding="utf-8"))
for t in ["bronze","silver","gold"]:
    print(t,"pre",len(ppd["problem_bank"][t]),"live",len(live["problem_bank"][t]))
