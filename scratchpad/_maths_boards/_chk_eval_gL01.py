import json,re,sys
sys.stdout.reconfigure(encoding="utf-8")
live=json.load(open("_chk_gL01_live.json",encoding="utf-8"))["practice_data"]
bank=live["problem_bank"]
issues=[]
def norm(s):
    return s.replace("×","*").replace("÷","/").replace("−","-")
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(bank[tier]):
        for j,st in enumerate(p.get("guided_steps",[])):
            if "answer" not in st: continue
            pre=norm(st["pre"])
            # take the rightmost arithmetic expression ending in '='
            m=re.search(r'([-()0-9.\s*/+]+)=\s*$',pre)
            if not m: continue
            expr=m.group(1).strip()
            # must contain an operator to be a computation
            if not re.search(r'[*/+]|(?<=\d)\s*-\s*(?=[-(0-9])',expr):
                # still allow simple 'a - b'
                pass
            if not re.search(r'[*/]|\d\s*[+\-]\s*[-(0-9]',expr): continue
            try:
                val=eval(expr,{"__builtins__":{}})
            except Exception:
                continue
            if float(val)==int(val): val=int(val)
            if val!=st["answer"]:
                issues.append(f"{tier}[{i}].guided_steps[{j}] '{st['pre'].strip()}' = {val} != answer {st['answer']}")
print("BOX ARITHMETIC:", "clean" if not issues else "MISMATCHES")
for x in issues: print(" -",x)
