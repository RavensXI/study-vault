import json, io
pd = json.load(io.open('lesson_biology-data-skills-L03@40fdb75726.json', encoding='utf-8'))
pb = pd["problem_bank"]
problems = []
issues = []
# check em dash
s = json.dumps(pd, ensure_ascii=False)
def scan(o, path):
    if isinstance(o, dict):
        for k,v in o.items():
            if k in ('note','guided_skip_reason'): continue
            scan(v, path+"."+k)
    elif isinstance(o, list):
        for i,v in enumerate(o): scan(v, path+"[%d]"%i)
    elif isinstance(o,str) and '—' in o:
        issues.append("EMDASH "+path)
scan(pd,"pd")

for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        tag = "%s[%d]"%(tier,i)
        sols = p["solutions"]
        acc = p.get("accept", 0.005)
        # last compute box (non-check) should equal solution; but our final numeric answer sits before check.
        gs = p.get("guided_steps")
        if gs:
            boxes = [st for st in gs if st.get("answer") is not None]
            # find the box whose answer equals the solution
            hit = any(abs(float(b["answer"]) - float(sols[0])) < 1e-9 for b in boxes)
            if not hit and p.get("input_type")!="multiple_choice":
                issues.append(tag+" no box equals solution "+str(sols)+" boxes="+str([b['answer'] for b in boxes]))
        # expects outside accept
        for j,m in enumerate(p.get("misconceptions") or []):
            e = m.get("expect")
            if e is not None:
                if abs(float(e)-float(sols[0])) <= acc:
                    issues.append(tag+".misc[%d] expect %s inside accept of %s"%(j,e,sols))
print("issues:", len(issues))
for x in issues: print("  -", x)
# print bank counts + solutions
for tier in ("bronze","silver","gold"):
    print(tier, [p["solutions"][0] for p in pb[tier]])
