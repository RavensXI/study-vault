import json
live=json.load(open("_CHK_L03rp_live.json",encoding="utf-8"))["practice_data"]
open("_CHK_L03rp_shard.json","w",encoding="utf-8").write(json.dumps(live,ensure_ascii=False,indent=1))
print("wrote shard")
