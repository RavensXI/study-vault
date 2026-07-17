import json, re

live = json.load(open("_chk_numL04_live.json", encoding="utf-8"))

issues = []

def walk_strings(obj, path=""):
    if isinstance(obj, str):
        yield path, obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk_strings(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_strings(v, f"{path}[{i}]")

# em dash sweep (exclude internal note fields)
for path, s in walk_strings(live):
    if "—" in s and ".note" not in path and not path.endswith("note"):
        issues.append(f"EM DASH at {path}: {s[:80]}")

# numeric box check
pb = live["problem_bank"]
for tier in ["bronze","silver","gold"]:
    for i, prob in enumerate(pb[tier]):
        for j, st in enumerate(prob.get("guided_steps", [])):
            if "answer" in st and not isinstance(st["answer"], (int, float)):
                issues.append(f"NON-NUMERIC {tier}[{i}].guided_steps[{j}].answer = {st['answer']!r}")
        # pre/post plain text: no LaTeX backslash
        for j, st in enumerate(prob.get("guided_steps", [])):
            for fld in ("pre","post"):
                if fld in st and "\\" in st[fld]:
                    issues.append(f"LATEX in {tier}[{i}].guided_steps[{j}].{fld}")

# teach/opener boxes numeric
for tier, walk in live["guided"]["teach"].items():
    for j, st in enumerate(walk["steps"]):
        if "answer" in st and not isinstance(st["answer"], (int,float)):
            issues.append(f"NON-NUMERIC teach.{tier}.steps[{j}]")
for j, st in enumerate(live["guided"]["opener"]["steps"]):
    if "answer" in st and not isinstance(st["answer"], (int,float)):
        issues.append(f"NON-NUMERIC opener.steps[{j}]")

# completion boundary check: >=1 before first phase:substitute, >=2 at/after
for tier in ["bronze","silver","gold"]:
    for i, prob in enumerate(pb[tier]):
        gs = prob.get("guided_steps")
        if not gs:
            continue
        box_idx = [j for j,st in enumerate(gs) if "answer" in st]
        first_sub = None
        for j,st in enumerate(gs):
            if st.get("phase") == "substitute":
                first_sub = j; break
        if first_sub is None:
            issues.append(f"NO phase:substitute in {tier}[{i}]")
            continue
        before = [j for j in box_idx if j < first_sub]
        after = [j for j in box_idx if j >= first_sub]
        if len(before) < 1:
            issues.append(f"BOUNDARY {tier}[{i}]: <1 box before boundary")
        if len(after) < 2:
            issues.append(f"BOUNDARY {tier}[{i}]: <2 live boxes ({len(after)})")

# duplicate solutions within a tier
for tier in ["bronze","silver","gold"]:
    seen = {}
    for i, prob in enumerate(pb[tier]):
        key = (prob["display"], tuple(prob["solutions"]))
        sol = tuple(prob["solutions"])
        # only flag identical display+sol duplicates
    sols = [tuple(p["solutions"]) for p in pb[tier]]
    # not necessarily an error to repeat a numeric answer, skip

print("ISSUES:" if issues else "NO STYLE/STRUCTURE ISSUES")
for x in issues:
    print(" -", x)
