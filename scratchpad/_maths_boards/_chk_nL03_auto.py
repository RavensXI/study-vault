import json, re
live = json.load(open('_chk_nL03_live.json', encoding='utf-8'))
pb = live['problem_bank']
issues = []

def scan_text(path, s):
    if not isinstance(s, str): return
    if '—' in s:  # em dash
        issues.append(f"EM DASH in {path}: {s[:60]}")

# em dash sweep across student-facing fields
def walk(obj, path):
    if isinstance(obj, dict):
        for k,v in obj.items():
            if k == 'note':  # internal exempt
                continue
            walk(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i,v in enumerate(obj):
            walk(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        scan_text(path, obj)
walk(live, 'root')

# boundary + last-box-lands-on-solution check
for tier in ['bronze','silver','gold']:
    for i,p in enumerate(pb[tier]):
        gs = p.get('guided_steps')
        sols = p.get('solutions')
        if not gs:
            if p.get('input_type')!='multiple_choice' and 'guided_skip_reason' not in p:
                issues.append(f"{tier}[{i}] missing guided_steps")
            continue
        box_idx = [j for j,s in enumerate(gs) if 'answer' in s]
        phase_idx = [j for j,s in enumerate(gs) if s.get('phase')=='substitute']
        if not phase_idx:
            issues.append(f"{tier}[{i}] no phase:substitute boundary")
        else:
            pi = phase_idx[0]
            before = [j for j in box_idx if j < pi]
            atafter = [j for j in box_idx if j >= pi]
            if len(before) < 1:
                issues.append(f"{tier}[{i}] <1 box before boundary (idx {pi})")
            if len(atafter) < 2:
                issues.append(f"{tier}[{i}] <2 live boxes at/after boundary: {len(atafter)}")
        # numeric-only boxes
        for j in box_idx:
            a = gs[j]['answer']
            if not isinstance(a,(int,float)):
                issues.append(f"{tier}[{i}].guided_steps[{j}] non-numeric answer {a!r}")

print("ISSUES:" if issues else "No automated issues.")
for x in issues: print(" -", x)

# print all misconception expects for manual cross-check
print("\n--- misconceptions ---")
for tier in ['bronze','silver','gold']:
    for i,p in enumerate(pb[tier]):
        for m in p.get('misconceptions',[]):
            print(f"{tier}[{i}] pat={m['pattern']} expect={m['expect']!r} check={m.get('check')}")
