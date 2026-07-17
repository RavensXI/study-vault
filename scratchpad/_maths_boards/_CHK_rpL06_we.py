import json
live = json.load(open("C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_CHK_rpL06_live.json", encoding="utf-8"))["practice_data"]
pre = json.load(open("C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_pre_dump_maths-eduqas.json", encoding="utf-8"))
LID="ca643606-adf3-40c8-a4dd-8dfb8c25a21f"
entry=[v for v in (pre if isinstance(pre,list) else pre.values()) if isinstance(v,dict) and v.get("id")==LID][0]
pwe=entry.get("practice_data",entry)["worked_examples"]
lwe=live["worked_examples"]
for i,(p,l) in enumerate(zip(pwe,lwe)):
    for k in set(list(p.keys())+list(l.keys())):
        if k=="steps": continue
        if p.get(k)!=l.get(k): print(f"we[{i}].{k}: PRE={p.get(k)} LIVE={l.get(k)}")
    for j,(ps,ls) in enumerate(zip(p["steps"],l["steps"])):
        for k in set(list(ps.keys())+list(ls.keys())):
            if ps.get(k)!=ls.get(k):
                print(f"we[{i}].steps[{j}].{k}:")
                print("   PRE :", repr(ps.get(k)))
                print("   LIVE:", repr(ls.get(k)))
