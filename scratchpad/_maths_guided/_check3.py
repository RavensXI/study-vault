import json
aud=json.load(open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_audit\_audit_result.json",encoding="utf-8"))
for k in ("issues","unconfirmed"):
    for e in aud.get(k,[]):
        if e.get("key")=="algebra-L06":
            print("====",k,e.get("tier"),"idx",e.get("index"),e.get("type"))
            print("detail:",e.get("detail"))
            print("fix:",e.get("proposed_fix"))
            print()
