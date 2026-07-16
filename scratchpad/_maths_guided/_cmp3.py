import json, io
live=json.load(io.open("_live_graphs_L07.json",encoding="utf-8"))
preobj=json.load(io.open("_pre_L07.json",encoding="utf-8"))
pre=preobj["practice_data"]
print("pre pd keys:", list(pre.keys()))
for k in ["related_videos","topic_links","worked_examples"]:
    same=json.dumps(live.get(k),sort_keys=True,ensure_ascii=False)==json.dumps(pre.get(k),sort_keys=True,ensure_ascii=False)
    print(f"{k}: {'UNCHANGED' if same else 'CHANGED'}")
print("gold[3] options pre :", pre["problem_bank"]["gold"][3].get("options"))
print("gold[3] sol pre     :", pre["problem_bank"]["gold"][3].get("solutions"))
print("gold[3] options live:", live["problem_bank"]["gold"][3].get("options"))
print("gold[3] sol live    :", live["problem_bank"]["gold"][3].get("solutions"))
