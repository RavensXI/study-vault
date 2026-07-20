import json, io, sys
b = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_geo_guided"
live = json.load(open(b + r"\_CHK_L09_live.json", encoding="utf-8"))
out = io.open(b + r"\_CHK_L09_dump.txt", "w", encoding="utf-8")
w = out.write

pb = live["problem_bank"]
for k in pb:
    if not isinstance(pb[k], list):
        w("PB.%s = %s\n" % (k, json.dumps(pb[k], ensure_ascii=False)))
w("\n")
for t in ["bronze", "silver", "gold"]:
    for i, p in enumerate(pb[t]):
        w("\n========== %s[%d] ==========\n" % (t, i))
        w("input_type: %s\n" % p.get("input_type"))
        w("display: %s\n" % p.get("display"))
        if p.get("image"): w("IMAGE: %s\n" % p["image"])
        if p.get("chart"): w("CHART: %s\n" % json.dumps(p["chart"], ensure_ascii=False))
        if p.get("ruler"): w("RULER: %s\n" % json.dumps(p["ruler"], ensure_ascii=False))
        if p.get("options"): w("options: %s\n" % json.dumps(p["options"], ensure_ascii=False))
        w("SOLUTIONS: %s\n" % json.dumps(p.get("solutions"), ensure_ascii=False))
        w("hint: %s\n" % p.get("hint"))
        for mi, m in enumerate(p.get("misconceptions", []) or []):
            w("  misc[%d]: %s\n" % (mi, json.dumps(m, ensure_ascii=False)))
        gs = p.get("guided_steps")
        if gs is None:
            w("  NO guided_steps  skip_reason=%s\n" % p.get("guided_skip_reason"))
        else:
            for si, s in enumerate(gs):
                w("  gs[%d]: %s\n" % (si, json.dumps(s, ensure_ascii=False)))
        for kk in p:
            if kk not in ("input_type","display","image","chart","ruler","options","solutions","hint","misconceptions","guided_steps","guided_skip_reason"):
                w("  OTHER %s: %s\n" % (kk, json.dumps(p[kk], ensure_ascii=False)[:400]))

w("\n\n########## GUIDED ##########\n")
w(json.dumps(live["guided"], ensure_ascii=False, indent=1))
w("\n\n########## TIER_GUIDES ##########\n")
w(json.dumps(live["tier_guides"], ensure_ascii=False, indent=1))
w("\n\n########## METHOD_CARD ##########\n")
w(json.dumps(live["method_card"], ensure_ascii=False, indent=1))
out.close()
print("done")
