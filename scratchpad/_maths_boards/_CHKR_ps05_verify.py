import json, re

pd = json.load(open("_CHKR_ps05_live.json", encoding="utf-8"))
findings = []

# ---- em dash scan in student-facing strings ----
def walk(obj, path):
    if isinstance(obj, dict):
        for k,v in obj.items():
            if k == "note":  # internal exempt
                continue
            walk(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i,v in enumerate(obj):
            walk(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        if "—" in obj:
            findings.append(f"EM DASH at {path}: {obj[:60]}")

walk(pd, "root")

# ---- recompute every guided_steps final box lands on solutions ----
pb = pd["problem_bank"]
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[tier]):
        sols = p.get("solutions")
        gs = p.get("guided_steps")
        if p.get("input_type")=="multiple_choice":
            continue
        if not gs:
            findings.append(f"{tier}[{i}] no guided_steps")
            continue
        # collect numeric answer boxes
        boxes = [s for s in gs if "answer" in s]
        # final box's answer should relate; the phase-tagged solve should equal solution
        # find phase step
        phase_idx = [j for j,s in enumerate(gs) if s.get("phase")=="substitute"]
        # the solution should appear as one of the box answers
        if sols and sols[0] not in [b["answer"] for b in boxes]:
            findings.append(f"{tier}[{i}] solution {sols} not among box answers {[b['answer'] for b in boxes]}")

# ---- reproduce expects for known patterns (manual list) ----
# We'll just print all misconceptions for manual eyeball
print("=== misconceptions ===")
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[tier]):
        for m in p.get("misconceptions",[]):
            print(f"{tier}[{i}] sol={p.get('solutions')} expect={m.get('expect')} pat={m.get('pattern')}")

print("\n=== FINDINGS ===")
for f in findings:
    print(f)
print("total findings:", len(findings))
