import json, re
from sympy import symbols, Eq, solve, nsimplify
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
T = standard_transformations + (implicit_multiplication_application,)
def sympify(s): return parse_expr(s, transformations=T)

live = json.load(open(r"C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/_live_maths-ocr_algebra-L10.json", encoding="utf-8"))
x, y = symbols('x y')

def parse_eqs(disp):
    # strip svg/html
    disp = re.sub(r'<[^>]+>', '', disp)
    # find the "Solve \(...\) and \(...\)" latex parts
    parts = re.findall(r'\\\((.*?)\\\)', disp)
    return parts

def to_expr(s):
    s = s.replace('^', '**').replace('−','-')
    return s

def solve_problem(disp):
    parts = parse_eqs(disp)
    eqs=[]
    for p in parts:
        p=to_expr(p)
        if '=' in p:
            l,r = p.split('=')
            eqs.append(Eq(sympify(l), sympify(r)))
    sol = solve(eqs, [x,y], dict=True)
    xs = sorted(set(nsimplify(s[x]) for s in sol), key=lambda v: float(v))
    return xs

fails=0
for tier in ['gold','bronze','silver']:
    for i,prob in enumerate(live['problem_bank'][tier]):
        xs = solve_problem(prob['display'])
        stored = sorted(prob['solutions'], key=lambda v: float(v))
        xs_f = sorted([float(v) for v in xs])
        ok = len(xs_f)==len(stored) and all(abs(a-b)<1e-9 for a,b in zip(xs_f, [float(s) for s in stored]))
        # misconception expects: verify sign-flip reproduces
        mflag=""
        for m in prob.get('misconceptions',[]):
            if m.get('pattern')=='factor_sign_flip' and m.get('expect'):
                # sign flip = negate each true root
                flipped = sorted([-float(s) for s in stored])
                exp = sorted([float(e) for e in m['expect']])
                if not (len(flipped)==len(exp) and all(abs(a-b)<1e-9 for a,b in zip(flipped,exp))):
                    mflag += f" EXPECT-MISMATCH stored_expect={m['expect']} vs negate-roots={flipped}"
        status = "OK" if ok and not mflag else "FAIL"
        if status=="FAIL": fails+=1
        print(f"{tier}[{i}] solve={xs_f} stored={[float(s) for s in stored]} {status}{mflag}")
print("TOTAL FAILS:", fails)
