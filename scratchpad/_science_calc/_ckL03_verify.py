import json, re

pd = json.load(open("_ckL03_canonical.json", encoding="utf-8"))
problems_report = []

def near(a, b, tol):
    return abs(a-b) <= tol

# ---- 1. Fresh-solve bank ----
bank = pd["problem_bank"]
expected = {
    "bronze": [2,30,60,20,24,1.5,None,12],
    "silver": [6,8,2,4,300,1],
    "gold":   [1.5,9,12,4,10,120],
}
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(bank[tier]):
        sol = p.get("solutions")
        exp = expected[tier][i]
        if p.get("input_type")=="multiple_choice":
            problems_report.append((tier,i,"MC sol="+str(sol)))
            continue
        problems_report.append((tier,i,f"sol={sol} expect={exp} ok={near(sol[0],exp,1e-9) if exp is not None else 'skip'}"))

# ---- 2. Recompute every guided_steps final box lands on solution ----
box_issues=[]
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(bank[tier]):
        gs=p.get("guided_steps")
        if not gs: continue
        # find last box with 'answer'
        boxes=[s for s in gs if "answer" in s]
        # count live boxes after phase
        phase_idx=None
        for k,s in enumerate(gs):
            if s.get("phase")=="substitute": phase_idx=k
        live_after=[s for k,s in enumerate(gs) if phase_idx is not None and k>=phase_idx and "answer" in s]
        before=[s for k,s in enumerate(gs) if phase_idx is not None and k<phase_idx and "answer" in s]
        if phase_idx is None:
            box_issues.append(f"{tier}[{i}] NO phase")
        elif len(live_after)<2:
            box_issues.append(f"{tier}[{i}] live_after={len(live_after)} <2")
        elif len(before)<1:
            box_issues.append(f"{tier}[{i}] before={len(before)} <1")

# ---- 3. Expects outside accept window ----
exp_issues=[]
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(bank[tier]):
        acc=p.get("accept")
        sol=p.get("solutions")
        for j,m in enumerate(p.get("misconceptions",[])):
            e=m.get("expect")
            if e is None: continue
            if sol and acc is not None and near(e,sol[0],acc):
                exp_issues.append(f"{tier}[{i}].misc[{j}] expect={e} INSIDE accept of {sol[0]}±{acc}")

# ---- 4. em-dash + board scan on student-facing text ----
raw=json.dumps(pd, ensure_ascii=False)
emdash = raw.count("—")
boards = re.findall(r'\b(AQA|Edexcel|OCR|WJEC|Eduqas)\b', raw)
sheet = re.findall(r'equation sheet|on your.{0,20}sheet|memoris|must memor', raw, re.I)

print("=== SOLUTIONS ===")
for r in problems_report: print(r)
print("\n=== BOX/BOUNDARY ISSUES ===", box_issues or "none")
print("\n=== EXPECT-INSIDE-ACCEPT ===", exp_issues or "none")
print("\n=== em-dashes:", emdash, "| boards:", boards, "| sheet-claims:", sheet)

# ---- 5. higher_only sanity ----
ho=[(t,i) for t in ["bronze","silver","gold"] for i,p in enumerate(bank[t]) if p.get("higher_only")]
print("higher_only flagged:", ho or "none (correct, all foundation)")
