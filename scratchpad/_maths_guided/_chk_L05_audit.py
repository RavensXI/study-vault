import json
d=json.load(open("_maths_audit/_audit_result.json",encoding="utf-8")) if False else None
import os
p="C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_audit/_audit_result.json"
d=json.load(open(p,encoding="utf-8"))
for sect in ["issues","unconfirmed"]:
    print("==",sect,"==")
    for it in d.get(sect,[]):
        key=json.dumps(it)
        if "L05" in key or "number-L05" in key or "Percentage" in key or "ea8d68a2" in key:
            print(json.dumps(it,ensure_ascii=False))
