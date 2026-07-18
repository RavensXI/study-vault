import json, hashlib
ids=["a5766e06","9c6e0eaf","617bc3d1","027dc8ab","bee74705","c9af77cf","f8582151"]
for i in ids:
    pd=json.load(open(f"_chk_{i}.json",encoding="utf-8"))
    h=hashlib.sha256(json.dumps(pd,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    print(i, h[:16])
