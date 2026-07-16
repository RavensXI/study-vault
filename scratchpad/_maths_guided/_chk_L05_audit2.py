import json,io,sys
p="C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_audit/_audit_result.json"
d=json.load(open(p,encoding="utf-8"))
out=open("_CHK_L05_audit.txt","w",encoding="utf-8")
for sect in ["issues","unconfirmed"]:
    out.write(f"== {sect} ==\n")
    for it in d.get(sect,[]):
        if it.get("key")=="number-L05":
            out.write(json.dumps(it,ensure_ascii=False,indent=2)+"\n")
out.close()
print("done; top keys:", list(d.keys()))
