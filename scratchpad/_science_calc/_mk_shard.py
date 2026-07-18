import json
d = json.load(open("_live_canonical.json", encoding="utf-8"))
json.dump(d["practice_data"], open("_live_pd_only.json","w",encoding="utf-8"), ensure_ascii=False)
print("wrote shard")
