import json,re,io,sys
import sympy as sp
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
x=sp.symbols('x')
pd=json.load(open("_pd.json",encoding="utf-8"))

def latex_to_expr(s):
    # strip \( \)
    s=s.replace("\(","").replace("\)","").strip()
    # unicode minus -> ascii
    s=s.replace("−","-")
    # x^2 -> x**2 ; handle superscripts too
    s=s.replace("x²","x**2").replace("^2","**2")
    # implicit multiplication: sympify handles with * needed. Insert * between number and x, and )( 
    s=re.sub(r'(\d)([x(])', r'\1*\2', s)
    s=re.sub(r'([x)])(\()', r'\1*\2', s)
    s=re.sub(r'\)(\d)', r')*\1', s)
    return sp.expand(sp.sympify(s))

issues=[]
for tier in ["gold","bronze","silver"]:
    for i,p in enumerate(pd["problem_bank"][tier]):
        disp=p["display"].replace("Factorise","").strip()
        target=latex_to_expr(disp)
        opts=p["options"]; sol=p["solutions"][0]
        # which options expand to target
        matches=[j for j,o in enumerate(opts) if sp.simplify(latex_to_expr(o)-target)==0]
        if sol not in matches:
            issues.append(f"{tier}[{i}] SOLUTION WRONG: stored sol={sol}, options matching target={matches}, display={p['display']}")
        if len(matches)!=1:
            issues.append(f"{tier}[{i}] NON-UNIQUE/NO match: matches={matches} display={p['display']}")
print("=== BANK SOLUTION CHECK ===")
for it in issues: print(it)
if not issues: print("all bank solutions correct & unique")
