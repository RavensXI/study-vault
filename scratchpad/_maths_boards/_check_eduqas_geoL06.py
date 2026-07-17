# -*- coding: utf-8 -*-
import json, io, re, math
pd = json.load(io.open("lesson_maths-eduqas_geometry-L06.json", encoding="utf-8"))
issues = []

# 1. each bank problem: last box answer == solution; boxes present; svg labels vs text
for tier in ("bronze","silver","gold"):
    for i, p in enumerate(pd["problem_bank"][tier]):
        tag = "%s[%d]" % (tier, i)
        sol = p["solutions"][0]
        gs = p.get("guided_steps") or []
        boxes = [s for s in gs if s.get("answer") is not None]
        if not boxes:
            issues.append(tag+" no boxes"); continue
        last = boxes[-1]["answer"]
        if abs(float(last) - float(sol)) > 0.05:
            issues.append("%s last box %s != solution %s" % (tag, last, sol))
        # phase boundary
        subs = [j for j,s in enumerate(gs) if s.get("phase")=="substitute"]
        if not subs: issues.append(tag+" no substitute phase")
        # svg numeric labels must appear in the display text (numbers from the problem)
        disp = p["display"]
        svg = disp.split(CAP)[0] if (CAP:="</text>") else disp
        # collect number labels inside svg text tags before caption
        head = disp.split('<span class="figure-caption"')[0]
        labels = re.findall(r">([^<]+)</text>", head)
        textpart = disp.split('Diagram not drawn accurately</span>')[-1]
        for lab in labels:
            nums = re.findall(r"\d+\.?\d*", lab)
            for nnum in nums:
                if nnum not in textpart and nnum not in ("2",):  # 2 could be from 2ab etc
                    # allow labels like "Area = 30" -> 30 must be in text
                    if nnum not in textpart:
                        issues.append("%s figure label '%s' number %s not in problem text" % (tag, lab, nnum))

# 2. misconception expects reproduce (recompute quickly from known derivations)
r=math.radians; sin=lambda d:math.sin(r(d)); cos=lambda d:math.cos(r(d))
asin=lambda x:math.degrees(math.asin(x)); acos=lambda x:math.degrees(math.acos(x))
exp = {
 ("bronze",0):round(6*sin(30)/sin(50),1),
 ("bronze",1):round(10*sin(45)/sin(65),1),
 ("bronze",2):round(asin(8*sin(40)/10),1),
 ("bronze",3):round(9*sin(50)/sin(40),1),
 ("bronze",4):round(5*8*sin(30)),
 ("bronze",5):round(15*sin(80)/sin(35),1),
 ("bronze",6):round(asin(7*sin(35)/9),1),
 ("bronze",7):round(12*7*sin(90)),
 ("silver",0):round(math.sqrt(149),1),
 ("silver",1):round(acos((64+81-81)/(2*8*9))) if False else 84.3,  # angle opp 9
 ("silver",2):round(11*14*sin(42),1),
 ("silver",3):round(acos((64+100-36)/(2*8*10)),1),
 ("silver",4):round(math.sqrt(81+169-2*9*13*abs(cos(110))),1),
 ("silver",5):round(15*20*sin(75),1),
 ("silver",6):round(acos(16/56),1),
 ("gold",0):round(math.sqrt(325),1),
 ("gold",1):round(0.5*13*14),
 ("gold",2):round(math.sqrt(64+121-2*8*11*abs(cos(100))),1),
 ("gold",3):round(asin(30/40)),
 ("gold",4):round(0.5*6*10*sin(70),1),
}
# recompute silver1 angle opp 9: cosX=(a2+b2-c2)/... with c=9 subtracted: (25+64-81)/(2*5*8)
exp[("silver",1)] = round(acos((25+64-81)/(2*5*8)),1)
exp[("gold",3)] = round(asin(30/40),1)

for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        for m in p.get("misconceptions",[]):
            e = m.get("expect")
            want = exp.get((tier,i))
            if want is None: continue
            if e is None: continue
            if abs(float(e)-float(want))>0.06:
                issues.append("%s[%d] expect %s but derived error = %s" % (tier,i,e,want))

# 3. teach + opener final boxes sanity
tb=8*sin(90)/sin(30); assert abs(tb-16)<0.01
ts=math.sqrt(25+64-2*5*8*cos(60)); assert abs(ts-7)<0.01
assert abs((180-asin(12*sin(35)/9))-130.1)<0.1

print("ISSUES:", len(issues))
for x in issues: print("  -", x)
if not issues: print("ALL CHECKS PASS")
