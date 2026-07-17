import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
live = json.load(open("_CHKrp05_live.json", encoding="utf-8"))[0]["practice_data"]

for tier in ["bronze","silver","gold"]:
    for j, prob in enumerate(live["problem_bank"][tier]):
        gs = prob.get("guided_steps", [])
        boxes = [(i,st) for i,st in enumerate(gs) if "answer" in st]
        # find phase boundary
        pidx = None
        for i, st in enumerate(gs):
            if st.get("phase") == "substitute":
                pidx = i; break
        before = [i for i,st in boxes if i < pidx]
        atafter = [i for i,st in boxes if i >= pidx]
        sol = prob["solutions"][0]
        vals = [st["answer"] for i,st in boxes]
        reaches = sol in vals
        flag = ""
        if pidx is None: flag += " NO_PHASE"
        if len(before) < 1: flag += " <1_BEFORE"
        if len(atafter) < 2: flag += " <2_AFTER"
        if not reaches: flag += " SOL_NOT_IN_BOXES"
        print(f"{tier}[{j}] sol={sol} before={len(before)} at/after={len(atafter)} boxvals={vals}{flag}")
