import json
d=json.load(open('_live_ps_L03.json',encoding='utf-8'))[0]['practice_data']
json.dump(d, open('_live_shard_ps_L03.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
print("shard written")
