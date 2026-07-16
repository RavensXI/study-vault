import json
d=json.load(open("_CHK_L04_live.json",encoding="utf-8"))
json.dump(d["practice_data"],open("_CHK_L04_livepd.json","w",encoding="utf-8"),ensure_ascii=False)
print("wrote")
