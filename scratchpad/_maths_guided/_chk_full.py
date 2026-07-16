import json, re

live = json.load(open("_chk_L01_live.json", encoding="utf-8"))
findings = []

# --- em dash scan across student-facing strings ---
def scan(obj, path, is_note=False):
    if isinstance(obj, dict):
        for k,v in obj.items():
            note = (k == "note")
            scan(v, f"{path}.{k}", note or is_note)
    elif isinstance(obj, list):
        for i,v in enumerate(obj):
            scan(v, f"{path}[{i}]", is_note)
    elif isinstance(obj, str):
        if not is_note and "—" in obj:
            findings.append(f"EM DASH at {path}: {obj[:60]}")

scan(live, "root")

# --- bank expects: for MC, expect must equal an option index and correct sol distinct ---
bank = live["problem_bank"]
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(bank[tier]):
        sols = p.get("solutions")
        opts = p.get("options",[])
        # duplicate options within a problem
        if len(set(opts)) != len(opts):
            findings.append(f"{tier}[{i}] duplicate options")
        for j,m in enumerate(p.get("misconceptions",[])):
            e = m.get("expect")
            if e is not None:
                if not isinstance(e,int) or e<0 or e>=len(opts):
                    findings.append(f"{tier}[{i}].misconceptions[{j}] expect={e} not a valid option index")
                if e in sols:
                    findings.append(f"{tier}[{i}].misconceptions[{j}] expect equals the CORRECT option {e}")

# duplicate correct answers within a tier
for tier in ["bronze","silver","gold"]:
    correct = [bank[tier][i]["options"][bank[tier][i]["solutions"][0]] for i in range(len(bank[tier]))]
    dup = [c for c in set(correct) if correct.count(c)>1]
    if dup:
        findings.append(f"{tier} duplicate correct answers: {dup}")

# --- numeric-only boxes in guided teach + opener ---
def check_boxes(walk, path):
    for i,s in enumerate(walk.get("steps",[])):
        if "answer" in s:
            a = s["answer"]
            if not isinstance(a,(int,float)):
                findings.append(f"{path}.steps[{i}] answer not numeric: {a}")

for t in ["bronze","silver","gold"]:
    check_boxes(live["guided"]["teach"][t], f"guided.teach.{t}")
check_boxes(live["guided"]["opener"], "guided.opener")

print("FINDINGS:", len(findings))
for f in findings:
    print(" -", f)
