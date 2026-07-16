import json
live=json.load(open("_live_L07.json",encoding="utf-8"))
lines=[]
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(live["problem_bank"][tier]):
        gs=p.get("guided_steps")
        if not gs:
            lines.append(f"{tier}[{i}] NO guided_steps"); continue
        boxes=[s for s in gs if "answer" in s]
        # phase boundary
        phase_idx=[j for j,s in enumerate(gs) if s.get("phase")=="substitute"]
        if not phase_idx:
            lines.append(f"{tier}[{i}] NO phase tag")
        else:
            pi=phase_idx[0]
            before_boxes=[s for s in gs[:pi] if "answer" in s]
            after_boxes=[s for s in gs[pi:] if "answer" in s]
            if len(before_boxes)<1: lines.append(f"{tier}[{i}] <1 box before phase")
            if len(after_boxes)<2: lines.append(f"{tier}[{i}] only {len(after_boxes)} live box(es) at/after phase")
        # check misconception expects present
lines.append("box scan done")
open("_boxchk_out.txt","w",encoding="utf-8").write("\n".join(lines))
print("\n".join(lines))
