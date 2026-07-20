import json, re
live = json.load(open(r"_CHK_L02_live.json", encoding="utf-8"))
s = json.dumps(live, ensure_ascii=False)
print("em dash count:", s.count("—"), "en dash:", s.count("–"))
print('check wrong:', s.count('"wrong"'))
print("entities:", re.findall(r"&[a-z]+;", s)[:10])
# boards
for b in ["AQA","Edexcel","OCR","Eduqas","WJEC","mark"]:
    if b.lower() in s.lower(): print("board/mark mention:", b)
# hint html
for t in ("bronze","silver","gold"):
    for i,q in enumerate(live["problem_bank"][t]):
        h = q.get("hint","")
        if not h: print(f"{t}[{i}] MISSING hint")
        if re.search(r"<[a-z/]", h or ""): print(f"{t}[{i}] hint has HTML")
        gs = q.get("guided_steps")
        if not gs: print(f"{t}[{i}] NO guided_steps, skip_reason={q.get('guided_skip_reason')}")
        else:
            boxes=[x for x in gs if "answer" in x]
            ph=[j for j,x in enumerate(gs) if x.get("phase")=="substitute"]
            if not ph: print(f"{t}[{i}] NO phase boundary")
            else:
                k=ph[0]
                after=[x for x in gs[k:] if "answer" in x]
                before=[x for x in gs[:k]]
                if len(after)<2: print(f"{t}[{i}] only {len(after)} live boxes")
                if len(before)<1: print(f"{t}[{i}] no pre-boundary step")
            for j,x in enumerate(gs):
                if "answer" in x and not isinstance(x["answer"],(int,float)):
                    print(f"{t}[{i}].guided_steps[{j}] non-numeric answer {x['answer']!r}")
                for f in ("pre","post","hint"):
                    if f in x and re.search(r"<[a-z/]", str(x[f])):
                        print(f"{t}[{i}].guided_steps[{j}].{f} has HTML")
        for j,m in enumerate(q.get("misconceptions",[])):
            if "expect" not in m: print(f"{t}[{i}].misconceptions[{j}] no expect")
            if m.get("check")=="wrong": print(f"{t}[{i}].misconceptions[{j}] check wrong")
            # leakage: does message contain a solution string
            sol = q.get("solutions")
            msg = m.get("message","")
            for v in sol:
                if re.search(r"(?<![\d.])"+re.escape(str(v))+r"(?![\d.])", msg):
                    print(f"{t}[{i}].misconceptions[{j}] MESSAGE contains solution {v}: {msg}")
            if re.search(r"(?<![\d.])"+re.escape(str(sol[0]))+r"(?![\d.])", q.get("hint","")):
                print(f"{t}[{i}].hint contains solution: {q['hint']}")
print("tier counts", {t:len(live["problem_bank"][t]) for t in ("bronze","silver","gold")})
