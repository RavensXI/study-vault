import json
ID = "295660a5-6ee6-40a4-9c32-c6aa0de7a590"
live = json.load(open("_CHK2_graphsL05_LIVE.json", encoding="utf-8"))["practice_data"]
pre_all = json.load(open("_pre_dump_maths-eduqas.json", encoding="utf-8"))
def find(obj):
    if isinstance(obj, list):
        for e in obj:
            r=find(e)
            if r: return r
    if isinstance(obj, dict):
        if obj.get("id")==ID: return obj
        for v in obj.values():
            r=find(v)
            if r: return r
    return None
pre_entry=find(pre_all)
pd = pre_entry.get("practice_data", pre_entry)
for tier in ["bronze","silver","gold"]:
    pre_set = {(p.get("display"), tuple(p.get("solutions") or [])) for p in pd["problem_bank"][tier]}
    liv_set = {(p.get("display"), tuple(p.get("solutions") or [])) for p in live["problem_bank"][tier]}
    only_pre = pre_set - liv_set
    only_liv = liv_set - pre_set
    print(f"=== {tier}")
    print("  removed:", only_pre)
    print("  added:  ", only_liv)

print("\n=== worked_examples diff")
pw = pd.get("worked_examples")
lw = live.get("worked_examples")
print("pre count", len(pw), "live count", len(lw))
for i in range(max(len(pw),len(lw))):
    a = json.dumps(pw[i],ensure_ascii=False,sort_keys=True) if i<len(pw) else None
    b = json.dumps(lw[i],ensure_ascii=False,sort_keys=True) if i<len(lw) else None
    if a!=b:
        print(f"  [{i}] DIFF")
        print("   pre :", pw[i] if i<len(pw) else None)
        print("   live:", lw[i] if i<len(lw) else None)
