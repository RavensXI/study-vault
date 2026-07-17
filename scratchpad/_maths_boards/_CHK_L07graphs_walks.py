import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
pd = json.load(open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\_CHK_L07graphs_live.json", encoding="utf-8"))
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        if p.get("input_type")=="multiple_choice": continue
        print(f"\n=== {tier}[{i}] {p['display']}  sol={p['solutions']}")
        for s in p.get("guided_steps",[]):
            if "say" in s and "answer" not in s:
                print("   say:", s["say"][:90])
            else:
                ph=" [PHASE]" if s.get("phase")=="substitute" else ""
                print(f"   BOX{ph}: '{s.get('pre','')}'[{s['answer']}]'{s.get('post','')}'")
