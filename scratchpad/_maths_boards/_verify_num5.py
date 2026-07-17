# -*- coding: utf-8 -*-
import json
pd = json.load(open("C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-aqa_number-L05.json", encoding="utf-8"))
bad = []

# fresh-solve each display (hard-coded independent recompute)
solve = {
 ("bronze",0): 0.25*360, ("bronze",1): 0.40*250, ("bronze",2): 0.15*80,
 ("bronze",3): 200*1.10, ("bronze",4): 90*0.80, ("bronze",5): 3/5*100,
 ("bronze",6): 0.35*100, ("bronze",7): 45/100,
 ("silver",0): 350*1.12, ("silver",1): 240*0.65, ("silver",2): (30-25)/25*100,
 ("silver",3): (12000-9000)/12000*100, ("silver",4): 45*1.20, ("silver",5): 18/45*100,
 ("silver",6): 640*0.175,
 ("gold",0): 510/0.85, ("gold",1): 27000/1.20, ("gold",2): 5000*1.03**2,
 ("gold",3): 20000*0.9**3, ("gold",4): 288/(0.9*0.8),
}
pb = pd["problem_bank"]
for tier in ("bronze","silver","gold"):
    probs = pb[tier]
    seen = set()
    for i,p in enumerate(probs):
        sol = p["solutions"][0]
        exp = round(solve[(tier,i)], 6)
        if abs(exp - sol) > 1e-6:
            bad.append("%s[%d] fresh-solve %s != stored %s" % (tier,i,exp,sol))
        if tuple(p["solutions"]) in seen:
            bad.append("%s[%d] DUP solution %s" % (tier,i,p["solutions"]))
        seen.add(tuple(p["solutions"]))
        # final box lands on solution
        boxes = [s for s in p["guided_steps"] if s.get("answer") is not None]
        if abs(boxes[-1]["answer"] - sol) > 1e-6:
            bad.append("%s[%d] final box %s != sol %s" % (tier,i,boxes[-1]["answer"],sol))
        # expect != solution and present
        for m in p.get("misconceptions",[]):
            e = m["expect"]
            if e is not None and abs(float(e)-float(sol)) < 0.011:
                bad.append("%s[%d] expect==sol" % (tier,i))

# opener boxes
opb = [s for s in pd["guided"]["opener"]["steps"] if s.get("answer") is not None]
if opb[0]["answer"] != 10 or opb[1]["answer"] != 30:
    bad.append("opener boxes wrong: %s" % [b["answer"] for b in opb])

# teach final boxes
tf = {"bronze":24, "silver":92, "gold":80}
for t,exp in tf.items():
    tb = [s for s in pd["guided"]["teach"][t]["steps"] if s.get("answer") is not None]
    if abs(tb[-1]["answer"]-exp) > 1e-6:
        bad.append("teach %s final %s != %s" % (t,tb[-1]["answer"],exp))

# preservation
live = json.load(open("C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_live_number-L05.json", encoding="utf-8"))
for f in ("related_videos","worked_examples","topic_links"):
    if json.dumps(pd[f],sort_keys=True) != json.dumps(live[f],sort_keys=True):
        bad.append("PRESERVATION broken: "+f)

# report expects for manual eye
print("EXPECTS:")
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        for m in p.get("misconceptions",[]):
            print("  %s[%d] sol=%s expect=%s" % (tier,i,p["solutions"][0],m["expect"]))

print("\nRESULT:", "ALL CLEAN" if not bad else "PROBLEMS:")
for b in bad: print("  -", b)
