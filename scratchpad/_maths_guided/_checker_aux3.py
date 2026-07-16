# -*- coding: utf-8 -*-
import json,io,sys
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
aud=json.load(open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_audit\_audit_result.json",encoding="utf-8"))
for sec in ["issues","unconfirmed","confirmed"]:
    lst=aud.get(sec,[])
    matched=[e for e in lst if isinstance(e,dict) and str(e.get("key","")).lower() in ("algebra-l02","algebra-l2")]
    print(f"--- {sec}: {len(matched)} ---")
    for e in matched: print(json.dumps(e,ensure_ascii=False))
# also list all distinct keys containing algebra
keys=set()
for sec in ["issues","unconfirmed","confirmed","audited"]:
    for e in aud.get(sec,[]):
        if isinstance(e,dict) and "key" in e: keys.add(e["key"])
print("algebra keys present:", sorted(k for k in keys if "algebra" in k.lower()))
