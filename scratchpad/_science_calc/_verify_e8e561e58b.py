# -*- coding: utf-8 -*-
import json, io
pd = json.load(io.open("lesson_physics-calculations-L05@e8e561e58b.json", encoding="utf-8"))
problems_true = {
 # (fresh-solved answer, list of last box answers that must include the solution)
 "bronze": [2.7, 200, 45, 81000, 66800, 2700],
 "silver": [173250, 504000, 1130000, 1000],
 "gold": [3894000, 18, 1200],
}
fail = []
for tier, truth in problems_true.items():
    for i, p in enumerate(pd["problem_bank"][tier]):
        sol = p["solutions"][0]
        if abs(sol - truth[i]) > 1e-6:
            fail.append("%s[%d] stored sol %s != fresh %s" % (tier, i, sol, truth[i]))
        # last box of guided_steps must equal sol OR be a check that recomputes; ensure
        # a substitute box equals sol
        boxes = [s["answer"] for s in p["guided_steps"] if s.get("answer") is not None]
        if sol not in boxes:
            fail.append("%s[%d] sol %s not among walk boxes %s" % (tier, i, sol, boxes))
        acc = p.get("accept", 0)
        for m in p.get("misconceptions", []):
            e = m.get("expect")
            if e is None: continue
            if abs(e - sol) <= acc:
                fail.append("%s[%d] expect %s inside accept window (sol %s +-%s)" % (tier,i,e,sol,acc))
            if abs(e - sol) < 0.011:
                fail.append("%s[%d] expect==sol" % (tier,i))
# recompute walk continuity for a few key boxes
def val(tier,i): return pd["problem_bank"][tier][i]["guided_steps"]
# expects derived independently
checks = {
 ("bronze",0):[("inv",200/540)],   # 0.370
 ("bronze",3):[("finaltemp",2*900*65)],  # 117000
 ("bronze",4):[("vap",0.2*2260000)],  # 452000
 ("silver",0):[("use200",3*385*200)],  # 231000
 ("silver",1):[("use100",1.5*4200*100)],  # 630000
 ("gold",0):[("onlyboil",1.5*2260000),("fusiontotal",504000+1.5*334000)],
 ("gold",1):[("squared",486/9)],  # 54
 ("gold",2):[("massonly",120000/4)],  # 30000
}
for (t,i),lst in checks.items():
    exps = [m["expect"] for m in pd["problem_bank"][t][i]["misconceptions"]]
    for name,v in lst:
        if not any(abs(v-e)<0.5 for e in exps):
            fail.append("%s[%d] derived %s=%s not in expects %s" % (t,i,name,v,exps))

# opener + teach arithmetic
op = pd["guided"]["opener"]["steps"]
assert op[0]["answer"]==3 and op[1]["answer"]==6
tb = [s.get("answer") for s in pd["guided"]["teach"]["bronze"]["steps"]]
assert 2.5 in tb and 750/300==2.5
ts = [s.get("answer") for s in pd["guided"]["teach"]["silver"]["steps"]]
assert 36000 in ts and 2*450*40==36000
tg = [s.get("answer") for s in pd["guided"]["teach"]["gold"]["steps"]]
assert 230000 in tg and 0.5*334000+0.5*4200*30==230000

if fail:
    print("VERIFY FAIL:")
    for f in fail: print("  -", f)
else:
    print("VERIFY OK: all solutions, walk boxes, expects, opener/teach arithmetic clean")
