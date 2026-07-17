import json,re
live=json.load(open("_chk_gL01_live.json",encoding="utf-8"))["practice_data"]
bank=live["problem_bank"]
MUL="×"; DIV="÷"; MIN="−"
issues=[]
def num(t): return int(t.replace(MIN,'-'))
def pairs(s): return re.findall(r'\(\s*('+MIN+r'?-?\d+)\s*,\s*('+MIN+r'?-?\d+)\s*\)', s)

for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(bank[tier]):
        d=p["display"]; sol=p["solutions"][0]; tag=f"{tier}[{i}]"
        pr=[(num(a),num(b)) for a,b in pairs(d)]
        if "gradient" in d.lower() and len(pr)==2 and "midpoint" not in d.lower():
            (x1,y1),(x2,y2)=pr; m=(y2-y1)/(x2-x1)
            if m!=sol: issues.append(f"{tag} gradient {m} != sol {sol}")
        for j,st in enumerate(p.get("guided_steps",[])):
            if "answer" not in st: continue
            pre=st["pre"].replace(MIN,'-')
            m2=re.search(r'(-?\d+)\s*(['+MUL+DIV+r'+-])\s*\(?(-?\d+)\)?\s*=\s*$',pre)
            if m2:
                a=int(m2.group(1));op=m2.group(2);b=int(m2.group(3))
                if op==DIV and b==0: continue
                r={'+':a+b,'-':a-b,MUL:a*b,DIV:(a/b if b else 0)}[op]
                if float(r)==int(r): r=int(r)
                if r!=st["answer"]:
                    issues.append(f"{tag}.guided_steps[{j}] '{st['pre'].strip()}' computes {r} != answer {st['answer']}")
# reproduce misconception expects for two-point gradient sign-drop / invert patterns
print("ISSUES" if issues else "no box-arithmetic mismatches")
for x in issues: print(" -",x)
EOF_MARK=None
