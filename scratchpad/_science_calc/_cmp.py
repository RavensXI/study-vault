import json
ids=["48cb4395","ed42ef31","9e971a6c"]
data={}
for i in ids:
    with open(f"_live_{i}.json",encoding="utf-8") as f:
        data[i]=f.read()
# compare canonical JSON string of parsed objects (byte-identical serialization)
objs={i:json.loads(data[i]) for i in ids}
c=json.dumps(objs["48cb4395"],sort_keys=True,ensure_ascii=False)
for i in ids[1:]:
    s=json.dumps(objs[i],sort_keys=True,ensure_ascii=False)
    print(i,"identical" if s==c else "DIFFERENT")
