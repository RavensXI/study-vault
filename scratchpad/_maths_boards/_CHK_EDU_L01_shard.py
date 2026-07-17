import json
live=json.load(open("_CHK_EDU_L01_live.json",encoding="utf-8"))["practice_data"]
json.dump(live, open("_CHK_EDU_L01_shard.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote shard")
