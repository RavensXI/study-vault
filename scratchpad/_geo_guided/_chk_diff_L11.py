# -*- coding: utf-8 -*-
import json, io, os, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
H = os.path.dirname(os.path.abspath(__file__))
live = json.load(io.open(os.path.join(H, "_CHK_L11_live.json"), encoding="utf-8"))
dump = json.load(io.open(os.path.join(H, "..", "_geo_audit", "_pre_dump_all.json"), encoding="utf-8"))
pre = [r for r in dump if r["key"] == "L11"][0]["pd"]
io.open(os.path.join(H, "_CHK_L11_pre.json"), "w", encoding="utf-8").write(json.dumps(pre, ensure_ascii=False, indent=1))

print("PRE keys :", sorted(pre.keys()))
print("LIVE keys:", sorted(live.keys()))
for k in sorted(set(pre) | set(live)):
    if k in ("problem_bank", "guided", "tier_guides", "method_card"):
        continue
    same = json.dumps(pre.get(k), sort_keys=True, ensure_ascii=False) == json.dumps(live.get(k), sort_keys=True, ensure_ascii=False)
    print("field %-18s identical=%s" % (k, same))
    if not same:
        print("   PRE :", json.dumps(pre.get(k), ensure_ascii=False)[:1500])
        print("   LIVE:", json.dumps(live.get(k), ensure_ascii=False)[:1500])

print("\n--- method_card ---")
print("PRE :", json.dumps(pre.get("method_card"), ensure_ascii=False)[:2500])

for tier in ("bronze", "silver", "gold"):
    a = (pre.get("problem_bank") or {}).get(tier) or []
    b = (live.get("problem_bank") or {}).get(tier) or []
    print("\n=== %s  pre=%d live=%d" % (tier, len(a), len(b)))
    for i in range(max(len(a), len(b))):
        pa = a[i] if i < len(a) else None
        pb = b[i] if i < len(b) else None
        if pa is None: print("  %s[%d] ADDED" % (tier, i)); continue
        if pb is None: print("  %s[%d] REMOVED" % (tier, i)); continue
        for k in ("display", "image", "solutions", "input_type", "options", "chart", "ruler", "calculator", "tolerance", "unit"):
            va, vb = pa.get(k), pb.get(k)
            if json.dumps(va, sort_keys=True, ensure_ascii=False) != json.dumps(vb, sort_keys=True, ensure_ascii=False):
                print("  %s[%d].%s CHANGED\n     PRE : %s\n     LIVE: %s" % (tier, i, k,
                      json.dumps(va, ensure_ascii=False)[:400], json.dumps(vb, ensure_ascii=False)[:400]))
        extra_pre = set(pa) - set(pb)
        if extra_pre:
            print("  %s[%d] keys DROPPED: %s" % (tier, i, sorted(extra_pre)))
            for k in sorted(extra_pre):
                print("      %s = %s" % (k, json.dumps(pa[k], ensure_ascii=False)[:600]))
