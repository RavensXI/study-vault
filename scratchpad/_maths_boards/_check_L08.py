# -*- coding: utf-8 -*-
import json, io, re, math
pd=json.load(io.open('lesson_maths-eduqas_algebra-L08.json',encoding='utf-8'))

def norm(s):
    return (s.replace('−','-').replace('×','*').replace('÷','/')
             .replace('²','**2').replace('√','sqrt'))

# collect all boxes with their pre expression
issues=[]
def check_expr(pre, ans, path):
    p=norm(pre)
    # find the arithmetic just before the trailing '='
    m=re.search(r'([-+()0-9\.\s\*/]+?)=\s*(\(2 d\.p\.\)\s*)?$', p)
    if not m: return
    expr=m.group(1).strip()
    if not re.search(r'[\d]',expr): return
    if not re.search(r'[-+*/]', expr): return  # single number, skip
    try:
        val=eval(expr, {'__builtins__':None,'sqrt':math.sqrt})
    except Exception as e:
        return
    # 2dp boxes
    if '(2 d.p.)' in pre or (isinstance(ans,float) and round(ans,2)==ans and abs(ans)<1000 and ('.' in str(ans))):
        if abs(round(val,2)-ans)>0.011 and abs(val-ans)>0.011:
            issues.append(f"{path}: '{expr}' = {val:.4f} but answer {ans}")
    else:
        if abs(val-ans)>1e-9:
            issues.append(f"{path}: '{expr}' = {val} but answer {ans}")

def walk_steps(steps, path):
    for i,st in enumerate(steps):
        if st.get('answer') is not None and st.get('pre'):
            check_expr(st['pre'], st['answer'], f"{path}[{i}]")

# opener
walk_steps(pd['guided']['opener']['steps'],'opener')
# teach
for t in ('bronze','silver','gold'):
    walk_steps(pd['guided']['teach'][t]['steps'],f'teach.{t}')
# bank
for t in ('bronze','silver','gold'):
    for j,p in enumerate(pd['problem_bank'][t]):
        walk_steps(p['guided_steps'], f'{t}[{j}].gs')

# final box lands on solution (single-solution problems)
def final_check():
    for t in ('bronze','silver','gold'):
        for j,p in enumerate(pd['problem_bank'][t]):
            sols=p['solutions']; gs=p['guided_steps']
            boxes=[s for s in gs if s.get('answer') is not None]
            vals=[b['answer'] for b in boxes]
            if len(sols)==1:
                if sols[0] not in vals:
                    issues.append(f"{t}[{j}] solution {sols} not among box answers {vals}")
            else:
                # fraction: numerator & denominator should both appear
                for s in sols:
                    if s not in vals:
                        issues.append(f"{t}[{j}] frac part {s} not in {vals}")

final_check()

# expect != solution & sanity
for t in ('bronze','silver','gold'):
    for j,p in enumerate(pd['problem_bank'][t]):
        for k,m in enumerate(p.get('misconceptions',[])):
            e=m['expect']; s=p['solutions']
            ev=e if isinstance(e,list) else [e]
            if len(ev)==len(s) and all(abs(float(a)-float(b))<0.011 for a,b in zip(ev,s)):
                issues.append(f"{t}[{j}].mc[{k}] expect==solution")

print("ISSUES:",len(issues))
for x in issues: print("  -",x)
