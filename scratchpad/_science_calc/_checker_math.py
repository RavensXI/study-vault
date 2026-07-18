import json, math
pd = json.load(open("_live_3c4aa292.json", encoding="utf-8"))

# Fresh-solve each problem independently, compare to solutions
def close(a,b,t=0.005): return abs(a-b)<=t
errs=[]

sols_expected = {
 ("bronze",0): 540/60, ("bronze",1): 25*40, ("bronze",2): 30/6,
 ("bronze",3): 24/4, ("bronze",4): 10*3, ("bronze",5): 90/3.6,
 ("silver",0): (25-5)/8, ("silver",1): 0.5*10*20, ("silver",2): 20*20,
 ("silver",3): 30/5, ("silver",4): 0.5*10*30 + 20*30 + 0.5*5*30,
 ("gold",0): abs((0-20**2)/(2*50)), ("gold",1): math.sqrt(2*10*45),
 ("gold",2): 0.5*5*25 + 10*25 + 0.5*5*25,
}
pb=pd["problem_bank"]
for (tier,i),v in sols_expected.items():
    stored=pb[tier][i]["solutions"][0]
    ok=close(float(stored),v)
    if not ok: errs.append(f"{tier}[{i}] stored {stored} != freshsolve {v}")
    print(f"{tier}[{i}]: freshsolve={v:.4f} stored={stored} {'OK' if ok else 'MISMATCH'}")

# Verify every guided_step box lands and is internally continuous (just recompute stated arithmetic)
print("\n--- boxes recompute (final box must equal solution) ---")
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        gs=p.get("guided_steps",[])
        boxes=[s for s in gs if s.get("answer") is not None]
        # final numeric answer among boxes that isn't a 'check' returning input - just print sequence
        seq=[s["answer"] for s in boxes]
        print(f"{tier}[{i}] boxes={seq} sol={p['solutions']}")

print("\n--- expects reproduce error & outside answer ---")
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        sol=p["solutions"][0]
        for m in p.get("misconceptions",[]):
            e=m.get("expect")
            if e is not None and abs(float(e)-sol)<0.011:
                errs.append(f"{tier}[{i}] expect {e} == sol {sol}")
                print(f"DEAD EXPECT {tier}[{i}]: {e}")

# teach & opener boxes
print("\n--- teach/opener ---")
g=pd["guided"]
for t in ("bronze","silver","gold"):
    boxes=[s["answer"] for s in g["teach"][t]["steps"] if s.get("answer") is not None]
    print("teach",t,boxes)
print("opener", [s["answer"] for s in g["opener"]["steps"] if s.get("answer") is not None])

print("\nERRORS:", errs if errs else "NONE")
