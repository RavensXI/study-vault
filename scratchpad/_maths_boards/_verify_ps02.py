import json, io, re
pd=json.load(io.open("lesson_maths-aqa_probability-statistics-L02.json",encoding="utf-8"))
pb=pd["problem_bank"]
bad=0
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        sol=p["solutions"]; gs=p.get("guided_steps")
        it=p.get("input_type")
        if it=="multiple_choice":
            print(f"{tier}[{i}] MC sol={sol} (no walk) OK"); continue
        ans=[st["answer"] for st in gs if st.get("answer") is not None]
        # last boxes should reconstruct solution
        if len(sol)==2:
            ok = ans[-2:]==sol
        else:
            ok = ans[-1]==sol[0] or (sol[0] in ans)
        # completion boundary check
        sub=[k for k,st in enumerate(gs) if st.get("phase")=="substitute"]
        live=sum(1 for st in gs[sub[0]:] if st.get("answer") is not None) if sub else 0
        if not ok or not sub or live<2 or sub[0]<1:
            bad+=1; print(f"** {tier}[{i}] sol={sol} lastans={ans[-3:]} sub@{sub} live={live}")
        else:
            print(f"{tier}[{i}] sol={sol} lastans={ans[-2:]} sub@{sub[0]} live={live} OK")
# expect != solution sanity + figure count
figs=sum(1 for tier in ("bronze","silver","gold") for p in pb[tier] if "<svg" in p.get("display",""))
print("figures on bank problems:", figs)
print("BAD:", bad)
