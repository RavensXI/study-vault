import json

CANON = "af432bd7-94b6-4601-a30d-4356767061bb"
p = json.load(open("C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_science_calc/_pre_dump_all.json", encoding="utf-8"))

# figure out structure
print("type:", type(p))
if isinstance(p, dict):
    print("keys sample:", list(p.keys())[:5])
    entry = p.get(CANON)
elif isinstance(p, list):
    entry = None
    for row in p:
        if row.get("id") == CANON:
            entry = row
            break
    print("list len:", len(p), "sample keys:", list(p[0].keys()) if p else None)

if entry is None:
    print("CANON NOT FOUND in predump")
else:
    pd = entry.get("practice_data", entry)
    s = json.dumps(pd)
    print("higher_only in predump:", s.count("higher_only"))
    print("accept in predump:", s.count('"accept"'))
    # print each problem's higher_only/accept/unit
    pb = pd.get("problem_bank", {})
    for tier in ["bronze","silver","gold"]:
        for i,prob in enumerate(pb.get(tier,[])):
            print(tier,i,"unit=",prob.get("unit"),"accept=",prob.get("accept"),"higher_only=",prob.get("higher_only"),"sol=",prob.get("solutions"),"disp=",prob.get("display","")[:45])
