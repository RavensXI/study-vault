import json, re
from math import gcd

LIVE = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_chk_num02_live.json"
PRE  = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_pre_dump_maths-eduqas.json"
ID = "09c2b39e-ac37-4058-8de3-22b163764aa7"

live = json.load(open(LIVE, encoding="utf-8"))["practice_data"]

# ---- em dash sweep (student-facing). exclude internal 'note' fields ----
def walk(o, path=""):
    if isinstance(o, dict):
        for k,v in o.items():
            if k == "note":  # internal exempt
                continue
            yield from walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i,v in enumerate(o):
            yield from walk(v, f"{path}[{i}]")
    elif isinstance(o, str):
        if "—" in o or "–" in o:
            yield (path, o)

print("=== EM/EN DASH in student-facing strings ===")
found = list(walk(live))
if not found:
    print("none")
for p,s in found:
    print(p, "::", s[:80])

# ---- numeric-only guided_steps boxes ----
print("\n=== non-numeric guided box answers ===")
def check_boxes(steps, label):
    for i,st in enumerate(steps):
        if "answer" in st:
            a = st["answer"]
            if not isinstance(a,(int,float)):
                print(f"{label}[{i}] answer not numeric: {a!r}")

for tier in ("bronze","silver","gold"):
    for pi,prob in enumerate(live["problem_bank"][tier]):
        check_boxes(prob.get("guided_steps",[]), f"{tier}[{pi}]")
for tier in ("bronze","silver","gold"):
    check_boxes(live["guided"]["teach"][tier]["steps"], f"teach.{tier}")
check_boxes(live["guided"]["opener"]["steps"], "opener")
print("(done)")

# ---- fraction solution sanity: reduced & positive ----
print("\n=== solution reduced-form check ===")
for tier in ("bronze","silver","gold"):
    for pi,prob in enumerate(live["problem_bank"][tier]):
        sol = prob.get("solutions")
        if isinstance(sol,list) and len(sol)==2 and prob.get("input_type")=="fraction":
            n,d = sol
            g = gcd(int(n),int(d))
            if g != 1:
                print(f"{tier}[{pi}] solution {n}/{d} not fully reduced (gcd={g})")
print("(done)")

# ---- final guided box lands on solution numerator/denominator? (report last two numeric answers) ----
# ---- preservation vs pre-dump ----
print("\n=== PRESERVATION vs pre-dump ===")
pre = json.load(open(PRE, encoding="utf-8"))
# pre may be list of rows or dict
rows = pre if isinstance(pre,list) else pre.get("data", pre)
entry = None
for r in (rows if isinstance(rows,list) else []):
    if isinstance(r,dict) and r.get("id")==ID:
        entry = r; break
if entry is None:
    print("pre-dump structure:", type(pre), list(pre.keys())[:5] if isinstance(pre,dict) else f"list len {len(rows)}")
    # try dict keyed by id
    if isinstance(pre,dict) and ID in pre:
        entry = {"practice_data": pre[ID]}
if entry:
    ppd = entry.get("practice_data", entry)
    for f in ("related_videos","topic_links","worked_examples"):
        same = json.dumps(ppd.get(f),sort_keys=True)==json.dumps(live.get(f),sort_keys=True)
        print(f"{f}: {'UNCHANGED' if same else 'CHANGED'}")
        if not same:
            print("  PRE:", json.dumps(ppd.get(f))[:300])
            print("  NEW:", json.dumps(live.get(f))[:300])
else:
    print("no pre entry found for id")
