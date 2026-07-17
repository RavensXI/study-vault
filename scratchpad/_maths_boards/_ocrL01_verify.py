# -*- coding: utf-8 -*-
import json, io
live = json.load(io.open("_ocrL01_live.json", encoding="utf-8"))
new = json.load(io.open("lesson_maths-ocr_algebra-L01.json", encoding="utf-8"))

ok = True
# preservation
if live["related_videos"] != new["related_videos"]: print("DIFF related_videos"); ok=False
if live["topic_links"] != new["topic_links"]: print("DIFF topic_links"); ok=False
# worked_examples: only labels changed (em dash -> colon)
for wi,(a,b) in enumerate(zip(live["worked_examples"], new["worked_examples"])):
    if a["question"]!=b["question"] or a.get("difficulty")!=b.get("difficulty"):
        print("DIFF we",wi,"q/diff"); ok=False
    for si,(x,y) in enumerate(zip(a["steps"],b["steps"])):
        if x.get("content")!=y.get("content"): print("DIFF we",wi,"step",si,"content"); ok=False
        if x.get("label")!=y.get("label") and "—" not in x.get("label",""):
            print("UNEXPECTED label change we",wi,si); ok=False
print("preservation ok" if ok else "PRESERVATION FAIL")

# solutions unchanged, all option[0] correct (already fresh-solved)
for t in ("bronze","silver","gold"):
    for i,(a,b) in enumerate(zip(live["problem_bank"][t], new["problem_bank"][t])):
        if a["solutions"]!=b["solutions"] or a["display"]!=b["display"] or a["options"]!=b["options"]:
            print("DIFF problem",t,i); ok=False

# recompute teach terminal boxes
checks = {
 "opener":[6,8], "bronze":[9,7,16,16], "silver":[10,4,5,10], "gold":[3,2,2,5],
}
for tier,exp in checks.items():
    if tier=="opener":
        boxes=[s["answer"] for s in new["guided"]["opener"]["steps"] if s.get("answer") is not None]
    else:
        boxes=[s["answer"] for s in new["guided"]["teach"][tier]["steps"] if s.get("answer") is not None]
    print(tier,"boxes",boxes,"expected",exp,"OK" if boxes==exp else "MISMATCH")

# em dash sweep on new
EM="—"
def scan(o,p,hits):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("note","guided_skip_reason"): continue
            scan(v,p+"."+str(k),hits)
    elif isinstance(o,list):
        for i,v in enumerate(o): scan(v,p+"[%d]"%i,hits)
    elif isinstance(o,str) and EM in o: hits.append(p)
hits=[]; scan(new,"pd",hits)
print("em dashes remaining:",hits if hits else "none")
print("ALL OK" if ok and not hits else "REVIEW")
