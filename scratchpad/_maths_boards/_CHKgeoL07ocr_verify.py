import json, re
base = "C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/"
pd = json.load(open(base+"_CHKgeoL07ocr_live.json", encoding="utf-8"))["practice_data"]

issues = []

# Verify arithmetic inside each box 'pre' when it contains an explicit "A op B =" ending
op = {'+':lambda a,b:a+b,'−':lambda a,b:a-b,'-':lambda a,b:a-b,'×':lambda a,b:a*b,'÷':lambda a,b:a/b,'*':lambda a,b:a*b}
pat = re.compile(r'(\d+(?:\.\d+)?)\s*([+\-−×÷*])\s*(\d+(?:\.\d+)?)\s*=\s*$')

def check_boxes(steps, path):
    for i, s in enumerate(steps):
        if 'answer' not in s:
            continue
        pre = (s.get('pre') or '')
        # find last "a op b =" occurrence at end
        m = None
        for mm in pat.finditer(pre.replace('²','')):
            m = mm
        if m:
            a,o,b = float(m.group(1)), m.group(2), float(m.group(3))
            val = op[o](a,b)
            if abs(val - s['answer']) > 1e-9:
                issues.append(f"{path}[{i}] '{pre.strip()}' computes {val} but answer={s['answer']}")

for tier in ['bronze','silver','gold']:
    for pi,p in enumerate(pd['problem_bank'][tier]):
        gs = p.get('guided_steps',[])
        check_boxes(gs, f"{tier}[{pi}].guided_steps")
        # final numeric box must equal a check or solution; check last box lands sensibly
        sol = p['solutions'][0]
        # find the box whose answer equals solution (solve box)
        answers = [s['answer'] for s in gs if 'answer' in s]
        if sol not in answers:
            issues.append(f"{tier}[{pi}] solution {sol} not reached by any box answers {answers}")
        # expects
        for mi,mc in enumerate(p.get('misconceptions',[])):
            exp = mc.get('expect')
            # nothing deterministic to recompute generically; just flag null
for t in ['bronze','silver','gold']:
    tw = pd['guided']['teach'][t]
    check_boxes(tw['steps'], f"teach.{t}.steps")
check_boxes(pd['guided']['opener']['steps'], "opener.steps")

print("ARITHMETIC/REACH ISSUES:", len(issues))
for x in issues: print(" -", x)

# em dash scan in student-facing
em = []
def scan(o, path):
    if isinstance(o,str):
        if '—' in o or '–' in o:
            em.append(path)
    elif isinstance(o,dict):
        for k,v in o.items():
            if k=='note': continue
            scan(v, path+"."+k)
    elif isinstance(o,list):
        for i,v in enumerate(o):
            scan(v, f"{path}[{i}]")
scan(pd, "pd")
print("EM-DASH HITS:", em)
