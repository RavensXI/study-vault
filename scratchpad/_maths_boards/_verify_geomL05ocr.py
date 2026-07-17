# -*- coding: utf-8 -*-
import json, io, re, math
pd = json.load(io.open("lesson_maths-ocr_geometry-L05.json", encoding="utf-8"))
pre = json.load(io.open("_geomL05ocr_live.json", encoding="utf-8"))
bad=[]
# 1 duplicates within tier
for tier in ("bronze","silver","gold"):
    seen={}
    for i,p in enumerate(pd["problem_bank"][tier]):
        if p.get("input_type")=="multiple_choice": continue
        k=tuple(p["solutions"])
        if k in seen: bad.append("DUP %s[%d] %s == %s[%d]"%(tier,i,k,tier,seen[k]))
        seen[k]=i
# 2 last guided box lands on solution (for numeric single_value with pyth-style final==check)
def last_box(gs):
    return [s for s in gs if s.get("answer") is not None][-1]["answer"]
def phase_box(gs):
    for s in gs:
        if s.get("phase")=="substitute": return s["answer"]
    return None
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        gs=p.get("guided_steps")
        if not gs: continue
        sol=p["solutions"][0]
        pb=phase_box(gs)
        # the substitute-phase box should equal the solution for these walks
        if abs(float(pb)-float(sol))>0.05:
            bad.append("%s[%d] phase box %s != sol %s"%(tier,i,pb,sol))
# 3 svg label vs number sanity: every 'cm'/'m'/'km' number in svg must appear in display text or be '?'
def svg_numbers(disp):
    m=re.search(r'<svg.*?</svg>', disp, re.S)
    if not m: return None
    return re.findall(r'>([\d.]+ ?(?:cm|m|km))<', m.group(0))
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        disp=p["display"]
        nums=svg_numbers(disp)
        if not nums: continue
        text=re.sub(r'<svg.*?</svg>','',disp,flags=re.S)
        for n in nums:
            val=n.split()[0]
            if val not in text:
                bad.append("%s[%d] svg label %s not in problem text"%(tier,i,n))
# 4 preservation
for f in ("related_videos","worked_examples"):
    if json.dumps(pd.get(f),sort_keys=True)!=json.dumps(pre.get(f),sort_keys=True):
        bad.append("PRESERVE changed: "+f)
if json.dumps(pd.get("topic_links"))!=json.dumps(pre.get("topic_links")):
    bad.append("PRESERVE changed: topic_links")
# 5 method_card steps count
if len(pd["method_card"]["steps"])>4: bad.append("method_card steps>4")
# 6 no em dash anywhere student-facing already validated; count
raw=io.open("lesson_maths-ocr_geometry-L05.json",encoding="utf-8").read()
if "—" in raw: bad.append("em dash present")
# report
if bad:
    print("ISSUES:")
    for b in bad: print("  -",b)
else:
    print("ALL CLEAN: no dup, phase boxes land on solutions, svg labels match text, preservation intact")
# also print solutions summary
for tier in ("bronze","silver","gold"):
    print(tier, [p["solutions"] for p in pd["problem_bank"][tier]])
