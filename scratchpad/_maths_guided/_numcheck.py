import json
live=json.load(open("_L04_truth.json",encoding="utf-8"))
pb=live["problem_bank"]
# reference solves computed by hand encoded here
refs={
 ("bronze",0):11,("bronze",1):23,("bronze",2):22,("bronze",3):-13,
 ("bronze",4):17,("bronze",5):8,("bronze",6):14,("bronze",7):-5,
 ("silver",0):21,("silver",1):6,("silver",2):19,("silver",3):17,
 ("silver",4):12,("silver",5):2,("silver",6):0,
}
bad=[]
for tier in ("bronze","silver"):
    for i,p in enumerate(pb[tier]):
        sol=p["solutions"][0]
        r=refs[(tier,i)]
        if sol!=r: bad.append(f"{tier}[{i}] stored {sol} != my {r}  ({p['display']})")
        # final guided box lands on solution
        boxes=[s for s in p.get("guided_steps",[]) if "answer" in s]
        if boxes and boxes[-1]["answer"]!=sol:
            bad.append(f"{tier}[{i}] final box {boxes[-1]['answer']} != sol {sol}")
        # count live boxes at/after phase
        gs=p.get("guided_steps",[])
        seen=False; live_after=0; before=0
        for s in gs:
            if "answer" not in s: continue
            if s.get("phase")=="substitute": seen=True
            if seen: live_after+=1
            else: before+=1
        if gs and (before<1 or live_after<2):
            bad.append(f"{tier}[{i}] boundary before={before} after={live_after}")
print("BRONZE/SILVER solve+box+boundary problems:", bad if bad else "ALL CLEAN")
# check duplicate answers within tier
for tier in ("bronze","silver"):
    ans=[p["solutions"][0] for p in pb[tier]]
    dups=[a for a in set(ans) if ans.count(a)>1]
    print(f"{tier} dup answers:", dups if dups else "none")
# gold multiple choice: verify solution index option text and expects
print("\n=== GOLD MC ===")
for i,p in enumerate(pb["gold"]):
    print(f"gold[{i}] sol_idx={p['solutions']} opts_ok display={p['display']}")
    for m in p.get("misconceptions",[]):
        print(f"    expect={m['expect']} note={m.get('note')}")
