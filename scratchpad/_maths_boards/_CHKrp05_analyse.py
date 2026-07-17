import json, re

live = json.load(open("_CHKrp05_live.json", encoding="utf-8"))[0]["practice_data"]

# 1. em dash sweep on student-facing strings (exclude internal 'note')
def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "note":
                continue
            yield from walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, f"{path}[{i}]")
    elif isinstance(o, str):
        yield path, o

emdash = []
for p, s in walk(live):
    if "—" in s:
        emdash.append((p, s))
print("=== EM DASHES ===", len(emdash))
for p, s in emdash:
    print(p, "::", s[:80])

# 2. non-numeric answer boxes
print("\n=== NON-NUMERIC answer boxes ===")
bad = 0
def check_boxes(steps, where):
    global bad
    for i, st in enumerate(steps):
        if "answer" in st and not isinstance(st["answer"], (int, float)):
            print(where, i, repr(st.get("answer")))
            bad += 1
for tier in ["bronze","silver","gold"]:
    check_boxes(live["guided"]["teach"][tier]["steps"], f"teach.{tier}")
check_boxes(live["guided"]["opener"]["steps"], "opener")
for tier in ["bronze","silver","gold"]:
    for j, prob in enumerate(live["problem_bank"][tier]):
        gs = prob.get("guided_steps", [])
        check_boxes(gs, f"{tier}[{j}].guided_steps")
print("bad boxes:", bad)

# 3. LaTeX/HTML in pre/post (should be plain text)
print("\n=== LaTeX in pre/post ===")
for tier in ["bronze","silver","gold"]:
    for j, prob in enumerate(live["problem_bank"][tier]):
        for i, st in enumerate(prob.get("guided_steps", [])):
            for f in ("pre","post"):
                v = st.get(f,"")
                if "\\(" in v or "\\frac" in v or "<" in v:
                    print(f"{tier}[{j}].guided_steps[{i}].{f}", repr(v))

# 4. hint plain-text (no LaTeX/HTML)
print("\n=== hints with LaTeX/HTML ===")
for tier in ["bronze","silver","gold"]:
    for j, prob in enumerate(live["problem_bank"][tier]):
        h = prob.get("hint","")
        if "\\(" in h or "<" in h:
            print(f"{tier}[{j}].hint", repr(h))

print("\nDONE")
