import json
CANON = "af432bd7-94b6-4601-a30d-4356767061bb"
pre = json.load(open("C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_science_calc/_pre_dump_all.json", encoding="utf-8"))
entry = next(r for r in pre if r["id"] == CANON)
pd = entry["pd"]
print("=== PRE exam_context ===")
print(json.dumps(pd["exam_context"], indent=1, ensure_ascii=False))
print("=== PRE worked_examples (questions+answers) ===")
for w in pd["worked_examples"]:
    print(w["difficulty"],"::", w["question"])
    for s in w["steps"]:
        if s.get("is_answer") or s.get("isAnswer"):
            print("   ANS:", s["content"])
print("=== PRE method_card steps ===")
print(json.dumps(pd["method_card"], indent=1, ensure_ascii=False)[:1200])
