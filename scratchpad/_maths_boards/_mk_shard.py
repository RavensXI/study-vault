import json
live=json.load(open("_LIVE_eduqas_L12.json",encoding="utf-8"))
json.dump(live["practice_data"], open("_LIVE_shard_L12.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
print("wrote shard")
