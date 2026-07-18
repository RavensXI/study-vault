import json, io
pd = json.load(io.open("lesson_chemistry-calculations-L04@6f3d09988e.json", encoding="utf-8"))
pb = pd["problem_bank"]
# fresh-solve each problem's stored solution and check final guided box lands on it
def lastbox(gs):
    vals=[s["answer"] for s in gs if s.get("answer") is not None]
    return vals
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        sol=p["solutions"]
        gs=p.get("guided_steps",[])
        boxes=[s["answer"] for s in gs if s.get("answer") is not None]
        # find the compute box = first box at/after phase
        subidx=None
        for j,s in enumerate(gs):
            if s.get("phase")=="substitute": subidx=j;break
        live=[s["answer"] for s in gs[subidx:] if s.get("answer") is not None] if subidx is not None else []
        # the compute (first live box) should equal solution (except g2 where 2nd live is final)
        print(tier,i,"sol",sol,"liveboxes",live)
        for m in p.get("misconceptions",[]):
            e=m.get("expect")
            if e is not None:
                assert abs(float(e)-float(sol[0]))>=0.011, (tier,i,"expect==sol")
print("method_card content words:", len([w for c in [pd['method_card']['content']] for w in c.replace('\(',' ').replace('\)',' ').split()]))
print("bronze n",len(pb["bronze"]),"silver",len(pb["silver"]),"gold",len(pb["gold"]))
# check all solutions distinct within tier
for tier in ("bronze","silver","gold"):
    sols=[tuple(p["solutions"]) for p in pb[tier]]
    print(tier,"sols",sols,"dupes" if len(sols)!=len(set(sols)) else "unique")
