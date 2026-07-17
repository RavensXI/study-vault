import json, re

live = json.load(open(r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_maths_boards\_CHK_algL01ocr_live.json", encoding="utf-8"))

# 1. em dash / entity scan over student-facing strings
EMDASH = "—"
ENDASH = "–"  # allowed? spec says use minus sign; en dash also suspect
findings = []

def walk(obj, path):
    if isinstance(obj, dict):
        for k,v in obj.items():
            # note fields exempt from em-dash
            walk(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i,v in enumerate(obj):
            walk(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        if EMDASH in obj:
            findings.append(("EMDASH", path, obj[:80]))
        if re.search(r"&[a-zA-Z]+;|&#\d+;", obj):
            findings.append(("ENTITY", path, obj[:80]))

walk(live, "root")
print("=== em-dash / entity findings ===")
for f in findings:
    print(f)
if not findings:
    print("none")

# 2. duplicate option VALUE check per problem (normalise LaTeX loosely)
def norm(s):
    return re.sub(r"\s+","", s)

pb = live["problem_bank"]
print("\n=== duplicate / equivalent option check (raw string) ===")
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        opts = p.get("options",[])
        seen = {}
        for j,o in enumerate(opts):
            n = norm(o)
            if n in seen:
                print(f"{tier}[{i}] DUP raw option {seen[n]} & {j}: {o}")
            seen[n]=j
print("(raw-string dup check done; mathematical equivalence checked manually)")

# 3. solutions index sanity
print("\n=== solutions index sanity ===")
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        sol = p.get("solutions")
        it = p.get("input_type")
        n = len(p.get("options",[]))
        if it=="multiple_choice":
            for s in sol:
                if not (0<=s<n):
                    print(f"{tier}[{i}] BAD sol idx {s} of {n}")
print("done")

# 4. list all misconception expects (should be null for MC)
print("\n=== misconception expects ===")
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pb[tier]):
        for k,m in enumerate(p.get("misconceptions",[])):
            print(f"{tier}[{i}].misc[{k}] expect={m.get('expect')} pattern={m.get('pattern')}")
