import json
live = json.load(open("_recheck_rp01_live.json", encoding="utf-8"))
pre = json.load(open("_recheck_rp01_pre.json", encoding="utf-8"))

print("===== WORKED_EXAMPLES diff =====")
lwe = live.get("worked_examples"); pwe = pre.get("worked_examples")
print("pre count:", len(pwe) if pwe else 0, "live count:", len(lwe) if lwe else 0)
for i in range(max(len(pwe or []), len(lwe or []))):
    p = pwe[i] if pwe and i<len(pwe) else None
    l = lwe[i] if lwe and i<len(lwe) else None
    if json.dumps(p,sort_keys=True,ensure_ascii=False)!=json.dumps(l,sort_keys=True,ensure_ascii=False):
        print(f"  [{i}] DIFFERS")
        print("    PRE q:", (p or {}).get("question"))
        print("    LIVE q:", (l or {}).get("question"))
    else:
        print(f"  [{i}] same")

print("\n===== METHOD_CARD diff =====")
lmc = live.get("method_card"); pmc = pre.get("method_card")
for k in set(list(lmc.keys())+list(pmc.keys())):
    if json.dumps(pmc.get(k),ensure_ascii=False)!=json.dumps(lmc.get(k),ensure_ascii=False):
        print(f"  key '{k}' DIFFERS")
        print("    PRE:", json.dumps(pmc.get(k),ensure_ascii=False)[:300])
        print("    LIVE:", json.dumps(lmc.get(k),ensure_ascii=False)[:300])

print("\n===== PROBLEM_BANK diff (displays/solutions/options) =====")
lpb=live["problem_bank"]; ppb=pre["problem_bank"]
for tier in ["bronze","silver","gold"]:
    lp=lpb.get(tier,[]); pp=ppb.get(tier,[])
    print(f"-- {tier}: pre {len(pp)} live {len(lp)}")
    for i in range(max(len(lp),len(pp))):
        pi = pp[i] if i<len(pp) else None
        li = lp[i] if i<len(lp) else None
        if pi is None: print(f"   [{i}] ADDED in live: {li.get('display')}"); continue
        if li is None: print(f"   [{i}] REMOVED: {pi.get('display')}"); continue
        for fld in ["display","options","solutions","input_type","calculator"]:
            if json.dumps(pi.get(fld),ensure_ascii=False)!=json.dumps(li.get(fld),ensure_ascii=False):
                print(f"   [{i}].{fld}: PRE={json.dumps(pi.get(fld),ensure_ascii=False)} LIVE={json.dumps(li.get(fld),ensure_ascii=False)}")
