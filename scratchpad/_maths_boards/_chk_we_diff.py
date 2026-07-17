import json
ID = "1d30ba6e-3b9a-41a9-b192-23cab4fd0d5f"
live = json.load(open("_chk_live_L08.json", encoding="utf-8"))
pre = json.load(open("_pre_dump_maths-eduqas.json", encoding="utf-8"))
entry = pre[ID] if isinstance(pre, dict) and ID in pre else None
if entry is None and isinstance(pre, list):
    entry = next(v for v in pre if v.get("id")==ID)
pd_pre = entry.get("practice_data", entry)
for i,(a,b) in enumerate(zip(pd_pre["worked_examples"], live["worked_examples"])):
    for j,(sa,sb) in enumerate(zip(a["steps"], b["steps"])):
        if sa!=sb:
            print(f"WE[{i}].steps[{j}] pre={sa.get('label')!r} live={sb.get('label')!r} content_same={sa.get('content')==sb.get('content')}")
    if a.get("question")!=b.get("question"): print(f"WE[{i}] question diff")
