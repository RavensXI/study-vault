import json, io
live=json.load(io.open("_LIVE_canon_final.json",encoding="utf-8"))
shard=json.load(io.open("lesson_higher-calculations-L04@b4b6d1f722.json",encoding="utf-8"))
# shard may be full row or practice_data
pd_shard = shard.get("practice_data", shard)
a=json.dumps(live,sort_keys=True,ensure_ascii=False)
b=json.dumps(pd_shard,sort_keys=True,ensure_ascii=False)
print("shard == live practice_data:", a==b)
wl=json.load(io.open("_worklist_versions.json",encoding="utf-8"))
e=wl["higher-calculations-L04@b4b6d1f722"]
print("all_row_ids:", e["all_row_ids"])
print("subjects:", e["subjects"])
