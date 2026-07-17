import json
live=json.load(open("_CHKR_ps03_live.json",encoding="utf-8"))["practice_data"]
json.dump(live,open("_CHKR_ps03_shard.json","w",encoding="utf-8"),ensure_ascii=False)
print("written")
