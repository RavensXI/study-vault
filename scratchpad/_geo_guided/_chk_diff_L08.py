# -*- coding: utf-8 -*-
import json, io, os, sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
pd = json.load(io.open(os.path.join(HERE, "_chk_L08_live.json"), encoding="utf-8"))
pre = json.load(io.open(os.path.join(HERE, "..", "_geo_audit", "_pre_dump_all.json"), encoding="utf-8"))
old = [r for r in pre if r["key"] == "L08"][0]["pd"]

def norm(s):
    s = re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip()
    return s

print("OLD top keys:", sorted(old.keys()))
print("NEW top keys:", sorted(pd.keys()))
for k in ("related_videos", "topic_links", "worked_examples"):
    print(k, "IDENTICAL" if old.get(k) == pd.get(k) else "*** CHANGED ***")
    if old.get(k) != pd.get(k):
        print("  OLD:", json.dumps(old.get(k), ensure_ascii=False)[:1500])
        print("  NEW:", json.dumps(pd.get(k), ensure_ascii=False)[:1500])

print("\n--- method_card OLD ---")
print(json.dumps(old.get("method_card"), ensure_ascii=False, indent=1)[:2500])
print("\n--- method_card NEW ---")
print(json.dumps(pd.get("method_card"), ensure_ascii=False, indent=1)[:2500])

print("\n=== bank matching (by normalised display) ===")
for tier in ("bronze", "silver", "gold"):
    o = old["problem_bank"][tier]; n = pd["problem_bank"][tier]
    print("\n##", tier, "old", len(o), "new", len(n))
    om = {norm(p["display"]): (i, p) for i, p in enumerate(o)}
    for i, p in enumerate(n):
        k = norm(p["display"])
        if k in om:
            j, q = om.pop(k)
            flags = []
            if q.get("solutions") != p.get("solutions"):
                flags.append("SOLUTIONS %r -> %r" % (q.get("solutions"), p.get("solutions")))
            if q.get("image") != p.get("image"):
                flags.append("IMAGE %r -> %r" % (q.get("image"), p.get("image")))
            if q.get("input_type") != p.get("input_type"):
                flags.append("TYPE %r -> %r" % (q.get("input_type"), p.get("input_type")))
            oo, no_ = q.get("options"), p.get("options")
            if oo != no_ and oo and no_:
                for a, b in zip(oo, no_):
                    if norm(a) != norm(b):
                        flags.append("OPT reworded beyond punctuation: %r -> %r" % (a, b))
            print(" new %s[%d] <- old[%d] %s" % (tier, i, j, ("| " + " ; ".join(flags)) if flags else "ok"))
        else:
            print(" new %s[%d] NO OLD MATCH: %s" % (tier, i, p["display"][:110]))
    for k, (j, q) in om.items():
        print(" OLD %s[%d] UNMATCHED (display rewritten or dropped): %s" % (tier, j, q["display"][:110]))
