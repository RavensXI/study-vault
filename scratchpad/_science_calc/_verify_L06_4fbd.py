# -*- coding: utf-8 -*-
import json, io
pd = json.load(io.open("lesson_higher-calculations-L06@4fbd5cf5b9.json", encoding="utf-8"))
pb = pd["problem_bank"]
errs = []

# independent fresh solutions keyed by (tier, index)
expected = {
 ("bronze",0):340, ("bronze",1):3000000000, ("bronze",2):2.0, ("bronze",3):400,
 ("bronze",4):40, ("bronze",5):3, ("bronze",6):7800, ("bronze",7):200,
 ("silver",0):10, ("silver",1):10000000, ("silver",2):400, ("silver",3):11400,
 ("silver",4):2700, ("silver",5):12000,
 ("gold",0):20, ("gold",1):120, ("gold",2):0, ("gold",3):13.7, ("gold",4):3.0, ("gold",5):0,
}
for (tier,i),val in expected.items():
    p = pb[tier][i]
    sol = p["solutions"][0]
    if abs(sol - val) > 1e-9:
        errs.append("SOLUTION %s[%d] stored %s expected %s" % (tier,i,sol,val))

# expects outside accept window
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        sol = p["solutions"][0]
        acc = p.get("accept", 0)
        for j,mc in enumerate(p.get("misconceptions",[])):
            e = mc.get("expect")
            if e is None: continue
            if abs(e - sol) <= max(acc, 0.011):
                errs.append("EXPECT inside accept %s[%d].mis[%d] expect=%s sol=%s acc=%s" % (tier,i,j,e,sol,acc))

# guided_steps: final numeric box must equal solution (for single_value non-MC), boundary sanity
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        gs = p.get("guided_steps")
        if not gs: continue
        boxes = [s for s in gs if s.get("answer") is not None]
        # find the phase box index within gs
        phase_idx = next((k for k,s in enumerate(gs) if s.get("phase")=="substitute"), None)
        if phase_idx is None:
            errs.append("NO PHASE %s[%d]"%(tier,i))
        live = sum(1 for s in gs[phase_idx:] if s.get("answer") is not None) if phase_idx is not None else 0
        if live < 2:
            errs.append("LIVE<2 %s[%d]=%d"%(tier,i,live))
        # the answer-bearing box that computes the result (not the trailing check) should include the solution value
        sol = p["solutions"][0]
        vals = [s["answer"] for s in boxes]
        if sol not in [round(v,6) for v in vals]:
            errs.append("SOL not in guided boxes %s[%d] sol=%s vals=%s"%(tier,i,sol,vals))

# SVG cleanliness
def scan(o,path):
    if isinstance(o,dict):
        for k,v in o.items(): scan(v,path+"."+str(k))
    elif isinstance(o,list):
        for k,v in enumerate(o): scan(v,path+"[%d]"%k)
    elif isinstance(o,str) and "<svg" in o:
        tag = o.split("<svg",1)[1].split(">",1)[0]
        if "role=\"img\"" not in tag: errs.append("svg no role "+path)
        if "aria-label" not in tag: errs.append("svg no aria "+path)
        low=o.lower()
        if "http://" in low or "https://" in low or "xlink:href" in low:
            errs.append("svg external ref "+path)
scan(pd,"pd")

# em dash
def emscan(o,path):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("note",): continue
            emscan(v,path+"."+str(k))
    elif isinstance(o,list):
        for k,v in enumerate(o): emscan(v,path+"[%d]"%k)
    elif isinstance(o,str) and "—" in o:
        errs.append("EMDASH "+path)
emscan(pd,"pd")

# preservation of untouched fields
canon = json.load(io.open("_my_L06_4fbd_canonical.json", encoding="utf-8"))
for f in ("related_videos","topic_links","exam_context","worked_examples"):
    # exam_context / worked_examples had em dashes replaced, so only check related_videos/topic_links byte-equal
    pass
if pd["related_videos"] != canon["related_videos"]: errs.append("related_videos changed")
if pd["topic_links"] != canon["topic_links"]: errs.append("topic_links changed")

if errs:
    print("FAIL", len(errs))
    for e in errs: print("  -",e)
else:
    print("VERIFY CLEAN: solutions, expects, guided boxes, svg, em-dash, preservation all good")
