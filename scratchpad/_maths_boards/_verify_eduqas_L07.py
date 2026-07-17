# -*- coding: utf-8 -*-
import json, io, re
pd = json.load(io.open("lesson_maths-eduqas_graphs-L07.json", encoding="utf-8"))
pb = pd["problem_bank"]
errs = []

# Independent fresh-solve model for point-transform problems.
# Parse display for the given point and the target function form.
def solve(disp, ask):
    return None  # solved manually below

# Manual fresh-solve table: (tier, idx) -> expected solution list
expected = {
 ("bronze",0):[9], ("bronze",1):[3], ("bronze",2):[11], ("bronze",3):[5],
 ("bronze",4):[0], ("bronze",5):[2], ("bronze",6):[15], ("bronze",7):[10],
 ("silver",0):[-6], ("silver",1):[3], ("silver",2):[-4], ("silver",3):[0],
 ("silver",4):[-5], ("silver",5):[7], ("silver",6):[1],
 ("gold",0):[8], ("gold",1):[3], ("gold",2):[4], ("gold",3):[2], ("gold",4):[0],
}
for (t,i),sol in expected.items():
    got = pb[t][i]["solutions"]
    if got != sol:
        errs.append("SOLUTION MISMATCH %s[%d]: stored %s expected %s" % (t,i,got,sol))

# final live boxes must land on stored solution (for single_value with guided_steps)
for t in ("bronze","silver","gold"):
    for i,p in enumerate(pb[t]):
        gs = p.get("guided_steps")
        if not gs: continue
        sol = p["solutions"][0]
        # find the box tagged phase substitute that produces the answer == sol
        subs = [s for s in gs if s.get("phase")=="substitute" and s.get("answer") is not None]
        if not any(abs(s["answer"]-sol)<1e-9 for s in subs):
            errs.append("%s[%d] no substitute box equals solution %s (subs=%s)" % (t,i,sol,[s['answer'] for s in subs]))
        # at least 1 box before boundary, >=2 live at/after
        idx=[j for j,s in enumerate(gs) if s.get("phase")=="substitute"]
        if idx:
            b0=idx[0]
            live=sum(1 for s in gs[b0:] if s.get("answer") is not None)
            pre=sum(1 for s in gs[:b0] if s.get("answer") is not None)
            if live<2: errs.append("%s[%d] <2 live boxes after boundary"%(t,i))
            if pre<1: errs.append("%s[%d] no pre-worked box"%(t,i))

# expects must not equal correct answer (numeric) and should be the wrong value
for t in ("bronze","silver","gold"):
    for i,p in enumerate(pb[t]):
        sol=p["solutions"]
        for j,m in enumerate(p.get("misconceptions",[])):
            e=m.get("expect")
            if e is None: continue
            ev=e if isinstance(e,list) else [e]
            sv=[float(x) for x in sol]
            if len(ev)==len(sv) and all(abs(float(a)-b)<0.011 for a,b in zip(ev,sv)):
                errs.append("%s[%d].misc[%d] expect==solution %s"%(t,i,j,e))

# Verify chart points satisfy their equations
def check_chart(t,i,eqs):
    ch=pb[t][i].get("chart")
    if not ch: errs.append("%s[%d] expected chart missing"%(t,i)); return
    ds=ch["data"]["datasets"]
    for k,eq in enumerate(eqs):
        for pt in ds[k]["data"]:
            y=eq(pt["x"])
            if abs(y-pt["y"])>1e-9:
                errs.append("%s[%d] ds%d point (%s,%s) != eq %s"%(t,i,k,pt["x"],pt["y"],y))
check_chart("silver",3,[lambda x:x*x, lambda x:-x*x])
check_chart("silver",4,[lambda x:x*x, lambda x:x*x-5])
check_chart("gold",4,[lambda x:x*x, lambda x:(x-3)**2+5])

# Theme safety: scan SVG text fills
full=json.dumps(pd,ensure_ascii=False)
for m in re.finditer(r'fill="(#[0-9a-fA-F]{3,6})"', full):
    pass
# check no near-black text fill in <text>
for svg in re.findall(r'<svg.*?</svg>', full):
    for tx in re.findall(r'<text[^>]*fill="([^"]+)"', svg):
        if tx!="currentColor":
            errs.append("svg <text> fill not currentColor: %s"%tx)
    if "http://" in svg or "https://" in svg or "xlink" in svg:
        errs.append("svg external ref")

# em dash sweep (excluding note keys)
def sweep(o,path):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("note","guided_skip_reason"): continue
            sweep(v,path+"."+str(k))
    elif isinstance(o,list):
        for j,v in enumerate(o): sweep(v,path+"[%d]"%j)
    elif isinstance(o,str) and "—" in o:
        errs.append("EM DASH at "+path)
sweep(pd,"pd")

# opener boxes recompute
op=pd["guided"]["opener"]["steps"]
opbox=[s["answer"] for s in op if s.get("answer") is not None]
if opbox!=[27,-5]: errs.append("opener boxes %s expected [27,-5]"%opbox)

# teach final images
for t,exp in (("bronze",[2,9,5,0]),("silver",[3,2,2,-3]),("gold",[2,9,3,0])):
    boxes=[s["answer"] for s in pd["guided"]["teach"][t]["steps"] if s.get("answer") is not None]
    if boxes!=exp: errs.append("teach.%s boxes %s expected %s"%(t,boxes,exp))

# preservation vs live
live=json.load(io.open("_live_eduqas_graphs-L07.json",encoding="utf-8"))
if pd["related_videos"]!=live["related_videos"]: errs.append("related_videos changed")
if pd["topic_links"]!=live["topic_links"]: errs.append("topic_links changed")
# worked_examples: only labels changed (em dash fix)
wl=json.dumps(live["worked_examples"]).replace(" — ",": ")
if json.dumps(pd["worked_examples"])!=wl: errs.append("worked_examples changed beyond em-dash label fix")

if errs:
    print("VERIFY FAIL (%d):"%len(errs))
    for e in errs: print("  -",e)
else:
    print("VERIFY PASS: solutions, boxes, expects, charts, theme, preservation all clean")
