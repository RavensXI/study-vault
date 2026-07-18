import json
def load(p):
    with open(p,encoding="utf-8") as f: return json.load(f)
canon=load("_live_1fcee1e4.json")
r2=load("_live_97b8c30d.json")
r3=load("_live_becf88af.json")
cs=json.dumps(canon,sort_keys=True,ensure_ascii=False)
print("canon==97b8c30d:", cs==json.dumps(r2,sort_keys=True,ensure_ascii=False))
print("canon==becf88af:", cs==json.dumps(r3,sort_keys=True,ensure_ascii=False))
# compare to shard on disk
shard=load("lesson_physics-calculations-L02@d5abd25397.json")
print("canon==shard:", cs==json.dumps(shard,sort_keys=True,ensure_ascii=False))
