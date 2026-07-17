import json
base = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/"
live = json.load(open(base+"_CHK_L13_live.json", encoding="utf-8"))

hits=[]
def walk(o,path):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("pre","post") and isinstance(v,str) and ("\\(" in v or "\\[" in v):
                hits.append((path+"."+k, v))
            walk(v,path+"."+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,f"{path}[{i}]")
walk(live,"root")
print("pre/post fields containing LaTeX:", len(hits))
for p,v in hits:
    print("  ",p)
    print("     ", v)
