# -*- coding: utf-8 -*-
import json
live = json.load(open("_live_L05.json", encoding="utf-8"))
dump = json.load(open("_pre_fanout_dump.json", encoding="utf-8"))
ID = "75d6eee2-25e6-4977-b549-e965ddd6c735"
def find_entry(d):
    if isinstance(d, dict):
        if d.get("id") == ID: return d
        for v in d.values():
            r = find_entry(v)
            if r: return r
    elif isinstance(d, list):
        for v in d:
            r = find_entry(v)
            if r: return r
    return None
pre = find_entry(dump).get("practice_data")
pwe = pre["worked_examples"]; lwe = live["worked_examples"]
print("pre count:", len(pwe), "live count:", len(lwe))
for i in range(max(len(pwe),len(lwe))):
    a = pwe[i] if i<len(pwe) else None
    b = lwe[i] if i<len(lwe) else None
    sa=json.dumps(a,sort_keys=True,ensure_ascii=False)
    sb=json.dumps(b,sort_keys=True,ensure_ascii=False)
    if sa!=sb:
        print(f"\n=== [{i}] DIFFERS ===\nPRE : {sa}\nLIVE: {sb}")
    else:
        print(f"[{i}] identical")
