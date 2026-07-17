import json
live=json.load(open("_chk_gL01_live.json",encoding="utf-8"))["practice_data"]
json.dump(live,open("_chk_gL01_validate.json","w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("written")
