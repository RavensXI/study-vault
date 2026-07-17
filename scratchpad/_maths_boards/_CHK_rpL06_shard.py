import json
live=json.load(open("_CHK_rpL06_live.json",encoding="utf-8"))["practice_data"]
json.dump(live,open("_CHK_rpL06_livevalidate.json","w",encoding="utf-8"),ensure_ascii=False)
print("wrote")
