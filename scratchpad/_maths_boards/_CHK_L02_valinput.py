import json
live=json.load(open("_CHK_L02_livefresh.json",encoding="utf-8"))["practice_data"]
json.dump(live,open("_CHK_L02_forvalidate.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("written")
