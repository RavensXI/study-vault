import json
d=json.load(open("_CHKR_canon_live.json",encoding="utf-8"))
json.dump(d["practice_data"], open("_CHKR_val_input.json","w",encoding="utf-8"), ensure_ascii=False)
print("written")
