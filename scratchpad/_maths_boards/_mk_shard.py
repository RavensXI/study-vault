import json
live=json.load(open("_live_L06.json",encoding="utf-8"))
json.dump({"practice_data":live},open("_live_L06_shard.json","w",encoding="utf-8"),ensure_ascii=False)
# also raw
json.dump(live,open("_live_L06_raw.json","w",encoding="utf-8"),ensure_ascii=False)
print("done")
