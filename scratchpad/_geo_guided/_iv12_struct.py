import json, os, re
d=os.path.dirname(os.path.abspath(__file__))
pd=json.load(open(os.path.join(d,"_iv12_live.json"),encoding="utf-8"))
def words(s): return len(re.findall(r"\S+", re.sub("<[^>]+>"," ",s)))
out=[]
for t in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][t]):
        path="%s[%d]"%(t,i)
        gs=p.get("guided_steps")
        if not gs:
            out.append("%s: NO guided_steps (skip_reason=%s)"%(path,p.get("guided_skip_reason")))
            continue
        boxes=[j for j,s in enumerate(gs) if "answer" in s]
        ph=[j for j,s in enumerate(gs) if s.get("phase")=="substitute"]
        if len(ph)!=1: out.append("%s: phase tags = %s"%(path,ph))
        else:
            pre=[j for j in boxes if j<ph[0]]; post=[j for j in boxes if j>=ph[0]]
            if len(pre)<1: out.append("%s: 0 boxes before boundary"%path)
            if len(post)<2: out.append("%s: only %d live boxes at/after boundary"%(path,len(post)))
        # last step
        last=gs[-1]
        if "answer" not in last and "say" not in last: out.append("%s: odd last step"%path)
        # numeric answers
        for j,s in enumerate(gs):
            a=s.get("answer")
            if a is not None and not isinstance(a,(int,float)): out.append("%s.guided_steps[%d].answer not numeric: %r"%(path,j,a))
            for k in ("pre","post","hint"):
                if k in s and re.search(r"<[a-zA-Z/]", s[k]): out.append("%s.guided_steps[%d].%s has HTML"%(path,j,k))
        if not p.get("hint"): out.append("%s: missing hint"%path)
        for m in p.get("misconceptions",[]):
            if "check" in m: out.append("%s: SURVIVING check=%r"%(path,m["check"]))
            if "expect" not in m: out.append("%s: misconception missing expect"%path)
            if p.get("input_type")=="multiple_choice" and isinstance(m.get("expect"),int):
                if not (0<=m["expect"]<len(p.get("options",[]))): out.append("%s: expect index out of range %s"%(path,m["expect"]))
            if m.get("expect")==p["solutions"][0]: out.append("%s: expect EQUALS solution (%s)"%(path,m["expect"]))
        # em dash
        blob=json.dumps(p,ensure_ascii=False)
        for ch in ["—","–"]:
            if ch in blob: out.append("%s: contains %r"%(path,ch))
# budgets
for t,g in pd["tier_guides"].items():
    w=sum(words(s) for s in g["steps"])
    if w>115: out.append("tier_guides.%s steps = %d words"%(t,w))
    if "-" in g["title"] and ":" not in g["title"]: out.append("tier_guides.%s title uses dash"%t)
mc=pd["method_card"]
out.append("method_card: %d steps, content %d words"%(len(mc["steps"]), words(mc["content"])))
blob=json.dumps(pd,ensure_ascii=False)
for ch in ["—","–","&nbsp;","&amp;"]:
    if ch in blob: out.append("TOP-LEVEL contains %r"%ch)
# board neutral
for w_ in ["AQA","Edexcel","OCR","Eduqas","WJEC","mark","marks"]:
    if re.search(r"\b%s\b"%w_, blob): out.append("board/mark word present: %s"%w_)
print("\n".join(out) if out else "structural: clean")
