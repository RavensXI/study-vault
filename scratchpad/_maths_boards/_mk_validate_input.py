import json
live = json.load(open("_live_ocr_numberL03.json",encoding="utf-8"))
# validator likely expects a shard with practice_data or the pd itself; try wrapping
json.dump(live, open("_chk_numL03_validate.json","w",encoding="utf-8"), ensure_ascii=False, indent=2)
print("ok")
