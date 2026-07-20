# -*- coding: utf-8 -*-
import json, io, os, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
pd = json.load(io.open(os.path.join(HERE, "_chk_L08_live.json"), encoding="utf-8"))
pre = json.load(io.open(os.path.join(HERE, "..", "_geo_audit", "_pre_dump_all.json"), encoding="utf-8"))
old = [r for r in pre if r["key"] == "L08"][0]["pd"]

def show(p, path):
    print("=" * 78)
    print(path, "| type:", p.get("input_type", "single_value"))
    print("DISPLAY:", p.get("display"))
    if p.get("image"): print("IMAGE:", p["image"])
    if p.get("chart"): print("CHART:", json.dumps(p["chart"])[:300])
    if p.get("ruler"): print("RULER:", p["ruler"])
    if p.get("options"):
        for i, o in enumerate(p["options"]): print("   opt[%d]: %s" % (i, o))
    print("SOLUTIONS:", p.get("solutions"))
    print("HINT:", p.get("hint"))
    for j, m in enumerate(p.get("misconceptions") or []):
        print("  MIS[%d] pattern=%s expect=%r check=%r" % (j, m.get("pattern"), m.get("expect"), m.get("check")))
        print("        msg:", m.get("message"))
        if m.get("note"): print("        note:", m.get("note"))
    gs = p.get("guided_steps")
    if p.get("guided_skip_reason"): print("SKIP:", p["guided_skip_reason"])
    if gs:
        for j, s in enumerate(gs):
            if s.get("answer") is not None:
                print("  [%d] BOX phase=%s ans=%r" % (j, s.get("phase"), s.get("answer")))
                print("      pre:", s.get("pre"))
                if s.get("post"): print("      post:", s.get("post"))
                print("      hint:", s.get("hint"))
                if s.get("done"): print("      done:", s.get("done"))
                if s.get("say"): print("      say:", s.get("say"))
            else:
                print("  [%d] SAY: %s" % (j, s.get("say")))

pb = pd["problem_bank"]
opb = old["problem_bank"]
for tier in ("bronze", "silver", "gold"):
    print("\n\n########## %s (%d) desc=%r" % (tier.upper(), len(pb[tier]), pb.get(tier + "_description")))
    for i, p in enumerate(pb[tier]):
        show(p, "%s[%d]" % (tier, i))
        o = opb[tier][i] if i < len(opb[tier]) else None
        if o:
            if o.get("display") != p.get("display"):
                print("  !! DISPLAY CHANGED. OLD:", o.get("display"))
            if o.get("solutions") != p.get("solutions"):
                print("  !! SOLUTIONS CHANGED. OLD:", o.get("solutions"))
            if o.get("options") != p.get("options"):
                print("  !! OPTIONS CHANGED. OLD:", o.get("options"))
            if o.get("image") != p.get("image"):
                print("  !! IMAGE CHANGED. OLD:", o.get("image"))
            if o.get("input_type") != p.get("input_type"):
                print("  !! TYPE CHANGED. OLD:", o.get("input_type"))
