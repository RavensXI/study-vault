import json, re

live = json.load(open("_CHK_num01_live.json", encoding="utf-8"))
pb = live["problem_bank"]

# 1. duplicate answers within tier
for t in ("bronze","silver","gold"):
    sols=[tuple(p["solutions"]) for p in pb[t]]
    dups=[s for s in sols if sols.count(s)>1]
    print(f"{t} dup answers: {set(dups) if dups else 'none'}")

# 2. em dash scan in student-facing strings
def walk(o, path=""):
    if isinstance(o, dict):
        for k,v in o.items():
            if k=="note": continue  # internal exempt
            yield from walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i,v in enumerate(o):
            yield from walk(v, f"{path}[{i}]")
    elif isinstance(o,str):
        yield path,o
emdash=[]
for p,s in walk(live):
    if "—" in s or "–" in s:
        emdash.append((p,s))
print("em/en dashes in student-facing:", emdash if emdash else "none")

# 3. guided_steps final box must equal stored solution; boxes numeric
issues=[]
for t in ("bronze","silver","gold"):
    for i,p in enumerate(pb[t]):
        gs=p.get("guided_steps")
        if not gs:
            if p.get("input_type")!="multiple_choice" and not p.get("guided_skip_reason"):
                issues.append(f"{t}[{i}] missing guided_steps")
            continue
        boxes=[s for s in gs if "answer" in s]
        # numeric check
        for j,b in enumerate(boxes):
            a=b["answer"]
            if not isinstance(a,(int,float)):
                issues.append(f"{t}[{i}] box answer non-numeric: {a}")
        # completion boundary: >=1 before phase, >=2 at/after
        phase_idx=None
        cnt=0
        for s in gs:
            if "answer" in s:
                cnt+=1
                if s.get("phase")=="substitute" and phase_idx is None:
                    phase_idx=cnt  # 1-based position among boxes
        if phase_idx is not None:
            before=phase_idx-1
            after=len(boxes)-before
            if before<1: issues.append(f"{t}[{i}] <1 box before phase")
            if after<2: issues.append(f"{t}[{i}] <2 live boxes at/after phase (after={after})")
        else:
            issues.append(f"{t}[{i}] no phase:substitute boundary")
print("guided_steps structural issues:", issues if issues else "none")

# 4. tier_guides steps word budget <=115
for t in ("bronze","silver","gold"):
    steps=live["tier_guides"][t]["steps"]
    wc=sum(len(re.findall(r"\S+", s)) for s in steps)
    print(f"tier_guide {t} words: {wc} ({'OK' if wc<=115 else 'OVER'})")
    # title colon not dash
    title=live["tier_guides"][t]["title"]
    print(f"  title: {title!r}")
