# -*- coding: utf-8 -*-
import io, json, sys, os
sys.stdout.reconfigure(encoding="utf-8")
pd = json.load(io.open("lesson_L13.json", encoding="utf-8"))
pb = pd["problem_bank"]
for tier in ("bronze", "silver", "gold"):
    print("=" * 70)
    print(tier.upper(), pb[tier + "_description"])
    for i, p in enumerate(pb[tier]):
        img = (p.get("image") or "").rsplit("/", 1)[-1]
        print("-" * 66)
        print("%s[%d] %s | %s | sol=%s unit=%s" % (tier, i, img, p["input_type"], p["solutions"], p.get("unit")))
        print("  Q:", p["display"])
        for j, o in enumerate(p.get("options") or []):
            print("     (%d) %s" % (j, o))
        print("  hint:", p["hint"])
        boxes = [s for s in p["guided_steps"] if s.get("answer") is not None]
        print("  boxes:", [s["answer"] for s in boxes],
              "| substitute at step", next((k for k, s in enumerate(p["guided_steps"]) if s.get("phase") == "substitute"), None))
        print("  first box:", boxes[0]["pre"][:95])
        for m in p.get("misconceptions") or []:
            print("  MIS expect=%s : %s" % (m["expect"], m["message"][:90]))
print("=" * 70)
for t in ("bronze", "silver", "gold"):
    tt = pd["guided"]["teach"][t]
    print("TEACH", t, "boxes:", [s["answer"] for s in tt["steps"] if s.get("answer") is not None])
print("OPENER boxes:", [s["answer"] for s in pd["guided"]["opener"]["steps"] if s.get("answer") is not None])
