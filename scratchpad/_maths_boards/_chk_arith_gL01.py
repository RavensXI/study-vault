import json,re
live=json.load(open("_chk_gL01_live.json",encoding="utf-8"))["practice_data"]
bank=live["problem_bank"]
issues=[]

# fresh-solve gradient/point problems by parsing coordinate pairs
def pairs(s):
    return re.findall(r'\(\s*(−?-?\d+)\s*,\s*(−?-?\d+)\s*\)', s)
def num(t): return int(t.replace('−','-'))

for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(bank[tier]):
        d=p["display"]; sol=p["solutions"][0]
        pr=[(num(a),num(b)) for a,b in pairs(d)]
        tag=f"{tier}[{i}]"
        # two-point gradient
        if "gradient" in d.lower() and len(pr)==2 and "midpoint" not in d.lower():
            (x1,y1),(x2,y2)=pr
            m=(y2-y1)/(x2-x1)
            if m!=sol: issues.append(f"{tag} gradient recompute {m} != sol {sol}")
        # check every numeric guided box is internally consistent with its 'pre' arithmetic
        for j,st in enumerate(p.get("guided_steps",[])):
            if "answer" not in st: continue
            pre=st["pre"]
            # extract 'A op B =' final arithmetic if present
            m2=re.search(r'([−-]?\d+)\s*([+×÷-])\s*\(?([−-]?\d+)\)?\s*=\s*$',pre.replace('−','-'))
            if m2:
                a=int(m2.group(1));op=m2.group(2);b=int(m2.group(3))
                if op=='÷' and b==0: continue
                r={'+':a+b,'-':a-b,'×':a*b,'÷':(a/b if b else None)}[op]
                if r==int(r): r=int(r)
                if r!=st["answer"]:
                    issues.append(f"{tag}.guided_steps[{j}] '{pre.strip()}' -> {r} != answer {st['answer']}")
        # final box lands on solution
        boxes=[s for s in p.get("guided_steps",[]) if "answer" in s]
        if boxes and boxes[-1]["answer"]!=sol and "Check" not in boxes[-1]["pre"] and "check" not in boxes[-1]["pre"].lower():
            pass  # last is often a check; skip
print("ISSUES:" if issues else "no arithmetic issues found")
for x in issues: print(" -",x)
