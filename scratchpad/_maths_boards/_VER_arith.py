import json, re

live = json.load(open("_VER_live_pd.json", encoding="utf-8"))

# Find trailing arithmetic "A op B [op C ...] = " at end of pre (ignoring earlier text)
# op in × x * ÷ + - −
def check_expr(pre, ans):
    if not isinstance(pre, str): return None
    # take substring after last sentence boundary containing '='
    m = re.search(r'([0-9][0-9.\s×x*÷+\-−]*?)\s*=\s*$', pre)
    if not m: return None
    expr = m.group(1)
    e = expr.replace('×','*').replace('x','*').replace('÷','/').replace('−','-').strip()
    # must contain an operator to be a real computation
    if not re.search(r'[*/+\-]', e): return None
    try:
        val = eval(e)
    except Exception:
        return None
    ok = abs(val - ans) < 1e-9
    return (expr.strip(), val, ans, ok)

problems = 0
issues = []
def scan(path, steps):
    global problems
    for i, st in enumerate(steps or []):
        if 'answer' not in st: continue
        r = check_expr(st.get('pre',''), st['answer'])
        problems += 1
        if r and not r[3]:
            issues.append((f"{path}[{i}]", r[0], r[1], r[2]))

g = live['guided']
for tier in ['bronze','silver','gold']:
    scan(f"guided.teach.{tier}", g['teach'][tier]['steps'])
scan("guided.opener", g['opener']['steps'])
for tier in ['bronze','silver','gold']:
    for pi, prob in enumerate(live['problem_bank'][tier]):
        scan(f"{tier}[{pi}].guided_steps", prob.get('guided_steps'))

print("boxes with checkable arithmetic scanned")
print("ISSUES:", len(issues))
for it in issues:
    print("  ", it)
