import json
live = json.load(open("_chk_numL03_live.json", encoding="utf-8"))

# em dash sweep across all strings
def walk(o, path=""):
    if isinstance(o, str):
        if "—" in o:
            print("EM DASH at", path, ":", o[:60])
    elif isinstance(o, dict):
        for k,v in o.items(): walk(v, path+"."+k)
    elif isinstance(o, list):
        for i,v in enumerate(o): walk(v, f"{path}[{i}]")
walk(live)

# completion boundary check
pb = live["problem_bank"]
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        gs = p.get("guided_steps")
        if not gs:
            print(f"{tier}[{i}] NO guided_steps (input {p.get('input_type')})")
            continue
        # find phase index
        boxes = [s for s in gs if "answer" in s]
        phase_idx = next((j for j,s in enumerate(gs) if s.get("phase")=="substitute"), None)
        if phase_idx is None:
            print(f"{tier}[{i}] NO phase tag")
            continue
        before = sum(1 for s in gs[:phase_idx] if "answer" in s)
        after = sum(1 for s in gs[phase_idx:] if "answer" in s)
        final = boxes[-1]["answer"]
        sol = p["solutions"][0]
        ok = final == sol
        flag = "" if (before>=1 and after>=2 and ok) else "  <-- FLAG"
        print(f"{tier}[{i}] before={before} after={after} final={final} sol={sol} match={ok}{flag}")
print("sweep done")
