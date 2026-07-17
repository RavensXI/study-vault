import json, re
base = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/"
pd = json.load(open(base+"_CHK_geoL07_pd.json", encoding="utf-8"))

# 1. em-dash scan across all string values
def walk(o, path=""):
    if isinstance(o, dict):
        for k,v in o.items():
            yield from walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i,v in enumerate(o):
            yield from walk(v, f"{path}[{i}]")
    elif isinstance(o, str):
        yield path, o

emdash_hits = []
for path, s in walk(pd):
    if "note" in path.lower(): continue
    if "—" in s:
        emdash_hits.append(path)
print("EM DASH hits (student-facing):", emdash_hits or "none")

# 2. verify each problem's final guided_steps box lands on solutions, and boundary rules
pb = pd["problem_bank"]
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[tier]):
        sol = p.get("solutions")
        gs = p.get("guided_steps")
        it = p.get("input_type")
        if it == "multiple_choice":
            continue
        if not gs:
            print(f"{tier}[{i}] NO guided_steps (input {it})")
            continue
        boxes = [s for s in gs if "answer" in s]
        # last box value
        last = boxes[-1]["answer"] if boxes else None
        # find phase substitute
        phase_idx = None
        for j,s in enumerate(gs):
            if s.get("phase")=="substitute":
                phase_idx=j
        before = sum(1 for s in gs[:phase_idx] if "answer" in s) if phase_idx is not None else None
        after  = sum(1 for s in gs[phase_idx:] if "answer" in s) if phase_idx is not None else None
        # does any box equal the solution
        vals = [b["answer"] for b in boxes]
        hit = sol[0] in vals if sol else False
        flag = ""
        if not hit: flag += " SOL-NOT-IN-BOXES"
        if phase_idx is None: flag += " NO-PHASE"
        elif before<1 or after<2: flag += f" BOUNDARY(before={before},after={after})"
        print(f"{tier}[{i}] sol={sol} boxvals={vals} phase@{phase_idx} b/a={before}/{after}{flag}")

# 3. misconception expects sanity: list them
print("\n--- misconceptions ---")
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[tier]):
        for m in p.get("misconceptions",[]):
            print(f"{tier}[{i}] pattern={m.get('pattern')} expect={m.get('expect')}")
