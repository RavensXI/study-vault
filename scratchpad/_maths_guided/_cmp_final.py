import json, io
ID="6623fba3-fb9e-4353-80c4-35ed1d88f47e"
d=json.load(io.open("_pre_fanout_dump.json",encoding="utf-8"))
pre=None
for o in d:
    if isinstance(o,dict) and o.get("id")==ID:
        pre=o["practice_data"]; break
live=json.load(io.open("_live_graphs_L07.json",encoding="utf-8"))

for k in ["related_videos","topic_links","worked_examples"]:
    same=json.dumps(live.get(k),sort_keys=True,ensure_ascii=False)==json.dumps(pre.get(k),sort_keys=True,ensure_ascii=False)
    print(f"{k}: {'UNCHANGED' if same else '*** CHANGED ***'}")

print("\n-- gold[3] --")
print("pre  display:", pre["problem_bank"]["gold"][3].get("display"))
print("pre  options:", pre["problem_bank"]["gold"][3].get("options"))
print("pre  sol    :", pre["problem_bank"]["gold"][3].get("solutions"))
print("live display:", live["problem_bank"]["gold"][3].get("display"))
print("live options:", live["problem_bank"]["gold"][3].get("options"))
print("live sol    :", live["problem_bank"]["gold"][3].get("solutions"))

print("\n-- silver[4] --")
print("pre :", pre["problem_bank"]["silver"][4].get("display"), pre["problem_bank"]["silver"][4].get("solutions"))
print("live:", live["problem_bank"]["silver"][4].get("display"), live["problem_bank"]["silver"][4].get("solutions"))
