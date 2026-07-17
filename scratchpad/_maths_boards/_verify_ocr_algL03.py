# -*- coding: utf-8 -*-
import json, io
live = json.load(io.open("_live_ocr_algL03.json", encoding="utf-8"))
new = json.load(io.open("lesson_maths-ocr_algebra-L03.json", encoding="utf-8"))
prob=[]

# preservation: bank display/options/solutions/input_type unchanged
for t in ("bronze","silver","gold"):
    if len(live["problem_bank"][t])!=len(new["problem_bank"][t]):
        prob.append("tier size changed "+t)
    for i,(a,b) in enumerate(zip(live["problem_bank"][t],new["problem_bank"][t])):
        for f in ("display","options","solutions","input_type","calculator"):
            if a.get(f)!=b.get(f):
                prob.append("%s[%d].%s CHANGED"%(t,i,f))

# related_videos, topic_links, worked_examples count preserved
if live["related_videos"]!=new["related_videos"]: prob.append("related_videos changed")
if live["topic_links"]!=new["topic_links"]: prob.append("topic_links changed")
if len(live["worked_examples"])!=len(new["worked_examples"]): prob.append("worked_examples count changed")
# worked example questions/content unchanged (only labels edited)
for i,(a,b) in enumerate(zip(live["worked_examples"],new["worked_examples"])):
    if a.get("question")!=b.get("question"): prob.append("we[%d] question changed"%i)
    for j,(sa,sb) in enumerate(zip(a["steps"],b["steps"])):
        if sa.get("content")!=sb.get("content"): prob.append("we[%d].steps[%d] content changed"%(i,j))

# em dash sweep on new
def walk(o,p,acc):
    if isinstance(o,dict):
        for k,v in o.items():
            if k in ("note","guided_skip_reason"): continue
            walk(v,p+"."+str(k),acc)
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,p+"[%d]"%i,acc)
    elif isinstance(o,str) and "—" in o: acc.append(p)
acc=[]; walk(new,"pd",acc)
if acc: prob.append("EM DASH at: "+", ".join(acc))

# every misconception has expect key + hint present
for t in ("bronze","silver","gold"):
    for i,p in enumerate(new["problem_bank"][t]):
        if not p.get("hint"): prob.append("%s[%d] no hint"%(t,i))
        for j,m in enumerate(p.get("misconceptions",[])):
            if "expect" not in m: prob.append("%s[%d].misc[%d] no expect"%(t,i,j))

# recompute opener + teach boxes
def check_boxes(steps, name, expected):
    got=[s["answer"] for s in steps if s.get("answer") is not None]
    if got!=expected: prob.append("%s boxes %s != expected %s"%(name,got,expected))
check_boxes(new["guided"]["opener"]["steps"],"opener",[4,3,2])
check_boxes(new["guided"]["teach"]["bronze"]["steps"],"teach.bronze",[4,2,5,28])
check_boxes(new["guided"]["teach"]["silver"]["steps"],"teach.silver",[15,8,15,24])
check_boxes(new["guided"]["teach"]["gold"]["steps"],"teach.gold",[6,7,3,12])

# SVG label/number match
svg=new["guided"]["opener"]["display"]
n_circ=svg.count("<circle"); n_rect=svg.count("<rect")
if n_circ!=12: prob.append("opener SVG circles=%d expected 12"%n_circ)
if n_rect!=8: prob.append("opener SVG rects=%d expected 8"%n_rect)
if "12 sweets" not in svg or "8 chocolates" not in svg: prob.append("opener SVG labels missing")

print("PROBLEMS:" if prob else "ALL CHECKS CLEAN")
for p in prob: print("  -",p)
