import json
live=json.load(open("_CHKR_L01_live.json",encoding="utf-8"))
json.dump(live["practice_data"],open("_CHKR_L01_pd.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("wrote")
