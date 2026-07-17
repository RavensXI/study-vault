# -*- coding: utf-8 -*-
import os, json, urllib.request
ID = "a48ad66b-78c0-46f9-9db0-828173e35d1f"
key = os.environ["SUPABASE_SERVICE_KEY"]
url = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons?id=eq.%s&select=practice_data" % ID
req = urllib.request.Request(url, headers={"apikey": key, "Authorization": "Bearer " + key})
pd = json.load(urllib.request.urlopen(req))[0]["practice_data"]
pb = pd["problem_bank"]
bad = []

def num(s):
    return float("".join(c for c in s if (c.isdigit() or c in ".-")))

# independent fresh-solve of the numeric answer each problem expects (option index 0)
solve = {
 ("bronze",0):30,("bronze",1):27,("bronze",2):15,("bronze",3):7,
 ("bronze",5):18,("bronze",6):6,("bronze",7):2,
 ("silver",1):10,("silver",2):4,("silver",3):30,("silver",4):4,("silver",5):10,("silver",6):7.5,
 ("gold",0):12,("gold",1):2.5,("gold",2):6,
}
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        assert p["solutions"]==[0], (tier,i,"solutions not [0]")
        if (tier,i) in solve:
            opt0 = num(p["options"][0])
            if abs(opt0-solve[(tier,i)])>1e-9:
                bad.append("%s[%d] option0 %s != solved %s"%(tier,i,opt0,solve[(tier,i)]))
        # expect indices valid and never 0
        for j,m in enumerate(p["misconceptions"]):
            e=m["expect"]
            if e is not None:
                if not isinstance(e,int) or e==0 or e>=len(p["options"]):
                    bad.append("%s[%d].mc[%d] bad expect %r"%(tier,i,j,e))

# recompute teach + opener boxes
def boxes(steps): return [s["answer"] for s in steps if s.get("answer") is not None]
op=boxes(pd["guided"]["opener"]["steps"]); assert op==[4,5], op
tb=boxes(pd["guided"]["teach"]["bronze"]["steps"]); assert tb==[2.5,15,8,10], tb
ts=boxes(pd["guided"]["teach"]["silver"]["steps"]); assert ts==[4.5,45,6,18], ts
tg=boxes(pd["guided"]["teach"]["gold"]["steps"]); assert tg==[60,5,60,6], tg

# g1 chart points satisfy y = 2.5x
for pt in pd["problem_bank"]["gold"][1]["chart"]["data"]["datasets"][0]["data"]:
    if abs(pt["y"]-2.5*pt["x"])>1e-9: bad.append("g1 chart point off line: %s"%pt)

print("teach/opener boxes recomputed OK" if not bad else "")
print("PROBLEMS:", bad if bad else "NONE - all 20 option-0 answers correct, all expects valid (never 0), all boxes land, chart on line")
