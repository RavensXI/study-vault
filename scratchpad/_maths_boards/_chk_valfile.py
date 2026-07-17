import json
live=json.load(open("_chk_L02_live.json",encoding="utf-8"))["practice_data"]
json.dump(live, open("_chk_L02_valinput.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
