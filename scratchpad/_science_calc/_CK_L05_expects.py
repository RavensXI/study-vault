import json
pd = json.load(open("_CK_L05_row0.json", encoding="utf-8"))
for tier, probs in pd["problem_bank"].items():
    if not isinstance(probs, list): continue
    for pi, p in enumerate(probs):
        sol = p.get("solutions",[None])[0]
        acc = p.get("accept", 0)  # default tolerance
        for mi, m in enumerate(p.get("misconceptions",[])):
            e = m.get("expect")
            if e is None: continue
            if sol is not None and isinstance(e,(int,float)) and isinstance(sol,(int,float)):
                inside = abs(e - sol) <= (acc if acc else 0)
                flag = "  <-- DEAD (inside accept)" if inside else ""
                # also flag if within default small window when accept unset
                if inside:
                    print(f"{tier}[{pi}].misc[{mi}] expect={e} sol={sol} accept={acc}{flag}")
print("expect check done (only dead ones printed)")
