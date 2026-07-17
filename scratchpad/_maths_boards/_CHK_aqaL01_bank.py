import json
ID = "f4f1368e-d7c2-41f1-8459-de2c0d500c3b"
live = json.load(open("_CHK_aqaL01_live.json", encoding="utf-8"))
pre_raw = json.load(open("_pre_dump_maths-aqa.json", encoding="utf-8"))
entry = [r for r in pre_raw if r.get("id")==ID][0]
pre_pd = entry.get("practice_data", entry)

lpb = live["problem_bank"]; ppb = pre_pd["problem_bank"]
for t in ["bronze","silver","gold"]:
    lp = lpb[t]; pp = ppb.get(t, [])
    print(f"\n### {t}: live {len(lp)} / pre {len(pp)}")
    for i, prob in enumerate(lp):
        opts = prob.get("options", [])
        sols = prob.get("solutions")
        dup = len(opts) != len(set(opts))
        # compare display/solution to pre if same index
        pre_disp = pp[i]["display"] if i < len(pp) else "<none>"
        pre_sol = pp[i].get("solutions") if i < len(pp) else "<none>"
        changed = (i>=len(pp)) or (pp[i].get("display")!=prob.get("display")) or (pre_sol!=sols)
        flag = "DUP!" if dup else ""
        ch = "CHANGED" if changed else "same"
        print(f"  [{i}] sols={sols} ndup={dup} {flag} {ch}")
        if changed:
            print(f"       LIVE disp: {prob.get('display')}")
            print(f"       PRE  disp: {pre_disp}  sol={pre_sol}")
        print(f"       correct(opt0)= {opts[0] if opts else '?'}")
