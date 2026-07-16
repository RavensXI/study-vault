import json
pd=json.load(open("_live_geometry-L03.json",encoding="utf-8"))
bank=pd["problem_bank"]
for tier in ["gold","bronze","silver"]:
    for i,p in enumerate(bank[tier]):
        gs=p.get("guided_steps")
        if not gs: 
            print(f"{tier}[{i}] NO guided_steps (input {p.get('input_type')})"); continue
        boxes=[s for s in gs if "answer" in s]
        # phase boundary
        phase_idx=[j for j,s in enumerate(gs) if s.get("phase")=="substitute"]
        first_phase = phase_idx[0] if phase_idx else None
        steps_before = first_phase  # count of steps before boundary
        live_boxes_after = sum(1 for j,s in enumerate(gs) if j>=first_phase and "answer" in s) if first_phase is not None else 0
        # last box vs solution
        lastbox=boxes[-1]["answer"] if boxes else None
        sol=p["solutions"][0]
        print(f"{tier}[{i}] boxes={len(boxes)} lastbox={lastbox} sol={sol} phase@{first_phase} before={steps_before} live_after={live_boxes_after}")
# teach & opener box count
print("--- teach ---")
for t in ["bronze","silver","gold"]:
    st=pd["guided"]["teach"][t]["steps"]
    nb=sum(1 for s in st if "answer" in s)
    print(f"{t}: {nb} boxes, all numeric={all(isinstance(s.get('answer'),(int,float)) for s in st if 'answer' in s)}")
op=pd["guided"]["opener"]["steps"]
print("opener boxes:", sum(1 for s in op if "answer" in s))
