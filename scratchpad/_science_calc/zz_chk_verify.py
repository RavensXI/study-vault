import json, re

pd = json.load(open("zz_chk_canonical.json", encoding="utf-8"))

issues = []

# Collect all student-facing strings
def walk_strings(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            # internal 'note' exempt from em dash
            yield from walk_strings(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_strings(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        yield path, obj

# em dash check (exclude .note fields)
for path, s in walk_strings(pd):
    if path.endswith(".note"):
        continue
    if "—" in s or "—" in s:
        issues.append(f"EM DASH at {path}: {s!r}")

# board name / equation-sheet claims
board_pat = re.compile(r"\b(AQA|Edexcel|OCR|WJEC|Eduqas)\b", re.I)
sheet_pat = re.compile(r"equation sheet|on your (equation )?sheet|must memorise|memorise this|given to you in the exam", re.I)
for path, s in walk_strings(pd):
    if path.endswith(".note"):
        continue
    if board_pat.search(s):
        issues.append(f"BOARD NAME at {path}: {s!r}")
    if sheet_pat.search(s):
        issues.append(f"SHEET CLAIM at {path}: {s!r}")

# Check misconception expects vs accept window
def close(a, b, tol):
    return abs(a - b) <= tol

for tier in ["bronze", "silver", "gold"]:
    for pi, prob in enumerate(pd["problem_bank"][tier]):
        sols = prob.get("solutions", [])
        acc = prob.get("accept", None)
        # default accept unknown; engine box tol 0.005; treat expect must differ from every solution beyond accept (or 0.005)
        for mi, mc in enumerate(prob.get("misconceptions", [])):
            exp = mc.get("expect", None)
            if exp is None:
                continue
            for sol in sols:
                tol = acc if acc is not None else 0.005
                if close(float(exp), float(sol), tol):
                    issues.append(f"DEAD EXPECT {tier}[{pi}].misconceptions[{mi}] expect={exp} within accept({tol}) of sol={sol}")

print("Issues found:", len(issues))
for i in issues:
    print(" -", i)
