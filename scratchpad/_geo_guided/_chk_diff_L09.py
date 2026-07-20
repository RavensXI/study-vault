import json
b = r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_geo_guided"
live = json.load(open(b + r"\_CHK_L09_live.json", encoding="utf-8"))
pre = json.load(open(b + r"\_CHK_L09_pre.json", encoding="utf-8"))["pd"]

print("PRE keys", sorted(pre.keys()))
print("LIVE keys", sorted(live.keys()))
for k in ["related_videos", "topic_links", "worked_examples"]:
    same = json.dumps(pre.get(k), sort_keys=True) == json.dumps(live.get(k), sort_keys=True)
    print(k, "unchanged:", same)

for t in ["bronze", "silver", "gold"]:
    P = pre["problem_bank"][t]
    L = live["problem_bank"][t]
    print("\n===", t, "pre", len(P), "live", len(L))
    for i, (p, l) in enumerate(zip(P, L)):
        issues = []
        if p.get("display") != l.get("display"):
            issues.append("DISPLAY CHANGED")
        if p.get("solutions") != l.get("solutions"):
            issues.append("SOLUTIONS %r -> %r" % (p.get("solutions"), l.get("solutions")))
        if p.get("image") != l.get("image"):
            issues.append("IMAGE %r -> %r" % (p.get("image"), l.get("image")))
        if json.dumps(p.get("chart"), sort_keys=True) != json.dumps(l.get("chart"), sort_keys=True):
            issues.append("CHART CHANGED")
        if p.get("ruler") != l.get("ruler"):
            issues.append("RULER %r -> %r" % (p.get("ruler"), l.get("ruler")))
        if p.get("options") != l.get("options"):
            issues.append("OPTIONS %r -> %r" % (p.get("options"), l.get("options")))
        if p.get("input_type") != l.get("input_type"):
            issues.append("INPUT %r -> %r" % (p.get("input_type"), l.get("input_type")))
        if issues:
            print(" ", t + "[%d]" % i, "; ".join(issues))
