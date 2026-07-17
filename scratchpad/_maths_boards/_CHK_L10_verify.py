import json, re
from fractions import Fraction as F
pd=json.load(open("_CHK_L10_live.json",encoding="utf-8"))
errs=[]

def approx(a,b): 
    return abs(float(a)-float(b))<1e-9

# Parse a linear or quadratic expression in x -> function
# We'll just hand-encode per problem via regex extraction is hard; instead evaluate solutions against display equations manually by parsing.
# Simpler: define equation checker by extracting the two equations from display.

def eqs_from_display(disp):
    # strip svg
    disp=re.sub(r'<svg.*?</svg>','',disp,flags=re.S)
    disp=re.sub(r'<span.*?</span>','',disp,flags=re.S)
    m=re.findall(r'\\((.*?)\\)',disp)
    return m

def make_f(expr):
    # expr like 'y = 2x + 1' or 'x^2 + y^2 = 10' or 'xy = 2' or 'y=x' 
    expr=expr.replace(' ','')
    return expr

# We'll check each solution pair by reconstructing. Do it per-tier with explicit equation lambdas isn't automatic; instead
# For verification, solve each problem generically: given two equations in x,y, check that stored x-solutions produce a y satisfying both.
# Build a tiny evaluator.
import ast
def evalexpr(e, x, y):
    e=e.replace('^','**')
    e=re.sub(r'(\d)([xy])', r'\1*\2', e)
    e=re.sub(r'([xy])([xy])', r'\1*\2', e)  # xy -> x*y
    e=re.sub(r'\)(\()', r')*\1', e)
    return eval(e, {'x':x,'y':y})

def check_eq(eqstr, x, y):
    l,r=eqstr.split('=')
    return approx(evalexpr(l,x,y), evalexpr(r,x,y))

bank=pd['problem_bank']
for tier in ['bronze','silver','gold']:
    for i,p in enumerate(bank[tier]):
        disp=p['display']
        eqs=eqs_from_display(disp)
        # keep only equations containing '='
        eqs=[e.replace(' ','') for e in eqs if '=' in e]
        sols=p['solutions']
        # for each x, find y from a 'y=' equation if present else derive
        for xv in sols:
            # find y
            yeq=[e for e in eqs if e.startswith('y=')]
            if yeq:
                y=evalexpr(yeq[0].split('=')[1], xv, None)
            else:
                # linear like x+y=5 -> y = rhs - ...; solve: pick eq with y linear
                # x+y=5
                lin=[e for e in eqs if 'y' in e and '**2' not in e.replace('^','**') and 'y^2' not in e]
                # crude: eq 'x+y=5'
                e=lin[0]
                lhs,rhs=e.split('=')
                # y = rhs - (lhs without y). handle x+y and xy
                if 'xy' in lhs or (lhs=='xy'):
                    y=float(rhs)/xv
                else:
                    # x+y
                    y=float(rhs)-xv  # assumes x+y
            for e in eqs:
                if not check_eq(e, xv, y):
                    errs.append(f"{tier}[{i}] x={xv},y={y} FAILS {e} (display eqs {eqs})")
print("SOLUTION CHECK errors:", len(errs))
for e in errs: print("  ",e)
