import json

ID = "2603a7c5-7660-4a4c-943d-78f2a112009e"
live = json.load(open("_ck_L01_live.json", encoding="utf-8"))
dump = json.load(open("_pre_fanout_dump.json", encoding="utf-8"))

# find pre entry
pre = None
if isinstance(dump, list):
    for e in dump:
        if e.get("id") == ID:
            pre = e.get("practice_data"); break
elif isinstance(dump, dict):
    if ID in dump:
        pre = dump[ID].get("practice_data", dump[ID])
    else:
        for k,v in dump.items():
            if isinstance(v,dict) and v.get("id")==ID:
                pre = v.get("practice_data"); break
print("pre found:", pre is not None)
if pre is None:
    # maybe dump keyed differently
    print("dump type", type(dump))
    if isinstance(dump, dict):
        print("sample keys", list(dump.keys())[:5])
    raise SystemExit

for field in ["related_videos","topic_links","worked_examples"]:
    a = json.dumps(pre.get(field), sort_keys=True, ensure_ascii=False)
    b = json.dumps(live.get(field), sort_keys=True, ensure_ascii=False)
    print(f"{field}: {'SAME' if a==b else 'DIFF'}")
    if a!=b:
        print("  PRE :", a[:400])
        print("  LIVE:", b[:400])

# input types of bank
print("\n-- input types + solutions (live) --")
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(live["problem_bank"][tier]):
        print(tier, i, p.get("input_type"), "sol", p.get("solutions"), "gs", "guided_steps" in p)

print("\n-- pre bank input types --")
for tier in ["bronze","silver","gold"]:
    arr = pre.get("problem_bank",{}).get(tier,[])
    for i,p in enumerate(arr):
        print(tier, i, p.get("input_type"), "sol", p.get("solutions"), "disp", p.get("display"))
