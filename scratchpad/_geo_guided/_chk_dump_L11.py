# -*- coding: utf-8 -*-
import json, io, os, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
H = os.path.dirname(os.path.abspath(__file__))
pd = json.load(io.open(os.path.join(H, "_CHK_L11_live.json"), encoding="utf-8"))
out = []
def w(s=""): out.append(s)

w("TOP KEYS: " + repr(sorted(pd.keys())))
g = pd.get("guided") or {}
w("\n===== OPENER =====")
w("display: " + repr((g.get("opener") or {}).get("display")))
for i, st in enumerate((g.get("opener") or {}).get("steps") or []):
    w("  [%d] %s" % (i, json.dumps(st, ensure_ascii=False)))
for tier in ("bronze", "silver", "gold"):
    t = (g.get("teach") or {}).get(tier) or {}
    w("\n===== TEACH %s =====" % tier)
    w("display: " + repr(t.get("display")))
    w("image: " + repr(t.get("image")))
    for k in t:
        if k not in ("display", "steps", "image"):
            w("  extra %s: %s" % (k, json.dumps(t[k], ensure_ascii=False)[:300]))
    for i, st in enumerate(t.get("steps") or []):
        w("  [%d] %s" % (i, json.dumps(st, ensure_ascii=False)))

w("\n===== TIER GUIDES =====")
w(json.dumps(pd.get("tier_guides"), ensure_ascii=False, indent=1))
w("\n===== METHOD CARD =====")
w(json.dumps(pd.get("method_card"), ensure_ascii=False, indent=1))

pb = pd.get("problem_bank") or {}
for tier in ("bronze", "silver", "gold"):
    w("\n\n########## %s_description: %s" % (tier, pb.get(tier + "_description")))
    for i, p in enumerate(pb.get(tier) or []):
        w("\n--- %s[%d] ---" % (tier, i))
        w("display: " + str(p.get("display")))
        w("image: " + str(p.get("image")))
        if p.get("chart"): w("chart: " + json.dumps(p["chart"], ensure_ascii=False)[:400])
        w("input_type: %s  solutions: %s  options: %s" % (p.get("input_type"), p.get("solutions"), p.get("options")))
        w("hint: " + str(p.get("hint")))
        for k in p:
            if k not in ("display","image","chart","input_type","solutions","options","hint","guided_steps","misconceptions"):
                w("  other %s: %s" % (k, json.dumps(p[k], ensure_ascii=False)[:300]))
        for j, m in enumerate(p.get("misconceptions") or []):
            w("  MIS[%d] %s" % (j, json.dumps(m, ensure_ascii=False)))
        for j, st in enumerate(p.get("guided_steps") or []):
            w("  GS[%d] %s" % (j, json.dumps(st, ensure_ascii=False)))
io.open(os.path.join(H, "_CHK_L11_dump.txt"), "w", encoding="utf-8").write("\n".join(out))
print("written", len(out))
