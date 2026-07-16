import json, re
from fractions import Fraction as F

live = json.load(open("_CHK_L10_live.json", encoding="utf-8"))
issues = []

def parse_lin(expr):
    # returns (a,b) for a*x+b given linear expression string in x, e.g. "2x+1","x-1","5-x","3-x","x","2x","3x"
    expr = expr.replace(" ", "")
    # handle forms
    # tokenize
    a=F(0); b=F(0)
    # split on + and - keeping signs
    tokens = re.findall(r'[+-]?[^+-]+', expr)
    for t in tokens:
        if 'x' in t:
            coef = t.replace('x','')
            if coef in ('','+'): a+=1
            elif coef=='-': a-=1
            else: a+=F(coef)
        else:
            b+=F(t)
    return a,b

# We'll manually verify each bank problem by re-deriving intersection with the curve type.
# Instead, brute check: for each problem parse display, find both solutions, verify satisfy both eqs.

def solve_line_curve(line_str, curve_str):
    # line y=line_str ; curve y=curve_str (quadratic ax^2+bx+c)
    la,lb = parse_lin_full(line_str)
    ca,cb,cc = parse_quad(curve_str)
    # la*x+lb = ca x^2 + cb x + cc  -> ca x^2 + (cb-la) x + (cc-lb)=0
    A=ca; B=cb-la; C=cc-lb
    return roots(A,B,C), (la,lb)

def parse_lin_full(s):
    s=s.replace(' ','')
    a=F(0);b=F(0)
    for t in re.findall(r'[+-]?[^+-]+', s):
        if 'x' in t:
            c=t.replace('x','')
            a+= F(1) if c in ('','+') else (F(-1) if c=='-' else F(c))
        else:
            b+=F(t)
    return a,b

def parse_quad(s):
    # forms like x^2+1, x^2, x^2-2x-3, x^2+5x+3, x^2+x, x^2-3, x^2-4x+2, x^2+x-2, x^2-3x+2, x^2+x-1
    s=s.replace(' ','').replace('^2','SQ')
    a=F(0);b=F(0);c=F(0)
    for t in re.findall(r'[+-]?[^+-]+', s):
        if 'xSQ' in t or 'SQ' in t and 'x' in t:
            co=t.replace('xSQ','')
            a+= F(1) if co in ('','+') else (F(-1) if co=='-' else F(co))
        elif 'x' in t:
            co=t.replace('x','')
            b+= F(1) if co in ('','+') else (F(-1) if co=='-' else F(co))
        else:
            c+=F(t)
    return a,b,c

def roots(A,B,C):
    disc=B*B-4*A*C
    if A==0:
        return [(-C/B)]
    import math
    sq=math.isqrt(int(disc)) if disc>=0 and int(disc)==disc else None
    sols=[]
    # try rational
    if disc>=0:
        r=disc**0.5
        for s in (1,-1):
            sols.append((-B + s*(F(disc).limit_denominator(10**6)**0)*0)) # placeholder
    # do float
    import math
    r=math.sqrt(float(disc))
    return sorted(set([round((-float(B)+r)/(2*float(A)),6), round((-float(B)-r)/(2*float(A)),6)]))

# Simpler: just verify stored solutions satisfy both equations for each problem.
def verify_pair(display, sols):
    out=[]
    return out

print("manual verification below")
