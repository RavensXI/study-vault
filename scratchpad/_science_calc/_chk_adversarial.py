# -*- coding: utf-8 -*-
import json, re
pd = json.load(open("_chk_canon_pd.json", encoding="utf-8"))
issues = []

# ---------- board-neutrality scan ----------
def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, f"{path}[{i}]")
    elif isinstance(o, str):
        yield path, o

banned = re.compile(r"\b(AQA|Edexcel|OCR|Eduqas|WJEC)\b|equation sheet|on your (equation |formula )?sheet|must memoris|must remember|you are given this|given to you in the exam|need to memoris", re.I)
for path, s in walk(pd):
    if banned.search(s):
        issues.append(("BOARD/SHEET", path, s[:120]))

# ---------- em dash scan (student-facing) ----------
for path, s in walk(pd):
    if "note" in path.lower():
        continue
    if "—" in s or "—" in s:
        issues.append(("EM_DASH", path, s[:120]))

# ---------- misconception expect vs correct (0.01 correctness tol) ----------
pb = pd["problem_bank"]
CORR_TOL = 0.01
for tier in ("bronze", "silver", "gold"):
    for i, p in enumerate(pb.get(tier, [])):
        sols = p.get("solutions", [])
        it = p.get("input_type")
        for j, m in enumerate(p.get("misconceptions", [])):
            exp = m.get("expect")
            if exp is None:
                continue
            if it == "single_value" and sols:
                if abs(exp - sols[0]) < CORR_TOL:
                    issues.append(("DEAD_EXPECT", f"{tier}[{i}].misconceptions[{j}]",
                                   f"expect={exp} correct={sols[0]} gap={abs(exp-sols[0])}"))

# ---------- box recompute for guided_steps / teach / opener ----------
def check_boxes(steps, label):
    for k, st in enumerate(steps):
        if "answer" not in st:
            continue
        ans = st["answer"]
        pre = st.get("pre", "")
        # try to extract 'a OP b =' pattern from pre
        m = re.search(r"([\d.]+)\s*([+−\-×*÷/])\s*([\d.]+)\s*=", pre)
        if m:
            a = float(m.group(1)); op = m.group(2); b = float(m.group(3))
            if op in "×*": r = a*b
            elif op in "÷/": r = a/b
            elif op in "−-": r = a-b
            elif op == "+": r = a+b
            if abs(r - ans) > 0.005:
                issues.append(("BOX_COMPUTE", f"{label}[{k}]", f"pre='{pre}' computes {r} but answer={ans}"))

for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb.get(tier,[])):
        if "guided_steps" in p:
            check_boxes(p["guided_steps"], f"{tier}[{i}].guided_steps")
for tier in ("bronze","silver","gold"):
    t = pd["guided"]["teach"].get(tier)
    if t: check_boxes(t["steps"], f"teach.{tier}")
check_boxes(pd["guided"]["opener"]["steps"], "opener")

# ---------- completion boundary: at least 1 before phase, >=2 live at/after ----------
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb.get(tier,[])):
        gs = p.get("guided_steps")
        if not gs:
            if p.get("input_type") != "multiple_choice":
                issues.append(("NO_GUIDED", f"{tier}[{i}]", "single_value without guided_steps"))
            continue
        boxidx = [k for k,s in enumerate(gs) if "answer" in s]
        phase_pos = [k for k,s in enumerate(gs) if s.get("phase")=="substitute"]
        if not phase_pos:
            issues.append(("NO_PHASE", f"{tier}[{i}]", "no phase:substitute boundary"))
            continue
        pp = phase_pos[0]
        before = [k for k in boxidx if k < pp]
        after = [k for k in boxidx if k >= pp]
        if len(before) < 1:
            issues.append(("BOUNDARY", f"{tier}[{i}]", f"no box before phase (pp={pp})"))
        if len(after) < 2:
            issues.append(("BOUNDARY", f"{tier}[{i}]", f"<2 live boxes at/after phase (after={len(after)})"))

# ---------- final answer + unit in a done/say? spec wants unit stated in final say/done ----------
# report boxes numeric only (already numeric)

print("TOTAL ISSUES:", len(issues))
for t in issues:
    print(t)
