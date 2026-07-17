# -*- coding: utf-8 -*-
import json, re, sys
io = sys.stdout
pd = json.load(open("_chk_L06_live_v2.json", encoding="utf-8"))

def norm(s):
    return s.replace("−","-").replace("−","-").replace("×","*").replace("·","*")

# Parse a factorisation option string into list of linear factors, handle leading integer and ^2
def parse_expr(s):
    s = norm(s)
    s = s.replace("\\(","").replace("\\)","").strip()
    s = s.replace(" ","")
    # handle leading integer coefficient e.g. 2(2x+1)(x-3) or 3(...)
    lead = 1
    m = re.match(r'^(-?\d+)\(', s)
    if m:
        lead = int(m.group(1))
        s = s[m.end()-1:]
    # find all (...) groups
    groups = re.findall(r'\(([^()]*)\)', s)
    # handle ^2
    sq = re.search(r'\)\^2|\)\^\{2\}|\)²', s) or ('²' in s) or ('^2' in s)
    factors = []
    for g in groups:
        factors.append(parse_linear(g))
    if ('^2' in s or '²' in s) and len(groups)==1:
        factors.append(parse_linear(groups[0]))
    return lead, factors

def parse_linear(g):
    # returns (a,b) meaning a*x + b
    g = g.replace(" ","")
    # tokens like 2x+1, x-3, -x+2, 3x, 5
    a = 0; b = 0
    # split into terms preserving sign
    terms = re.findall(r'[+-]?[^+-]+', g)
    for t in terms:
        if 'x' in t:
            coef = t.replace('x','')
            if coef in ('','+'): coef='1'
            if coef=='-': coef='-1'
            a += int(coef)
        else:
            b += int(t)
    return (a,b)

def poly_mult(lead, factors):
    # multiply factors -> dict power->coef
    poly = {0:lead}
    for (a,b) in factors:
        new = {}
        for p,c in poly.items():
            new[p+1] = new.get(p+1,0)+c*a
            new[p] = new.get(p,0)+c*b
        poly = new
    return poly  # {2:.., 1:.., 0:..}

def parse_display_quad(disp):
    # extract ax^2+bx+c from display like 'Factorise \\(6x^2 + x - 2\\)'
    d = norm(disp)
    m = re.search(r'\\\(([^\\]*)\\\)', d)
    s = m.group(1) if m else d
    s = s.replace("^2","²").replace(" ","")
    # a x² + b x + c
    a=b=c=0
    # x² term
    ma = re.search(r'([+-]?\d*)x²', s)
    if ma:
        v=ma.group(1); a=1 if v in('','+') else (-1 if v=='-' else int(v))
    mb = re.search(r'([+-]?\d*)x(?!²)', s)
    if mb:
        v=mb.group(1); b=1 if v in('','+') else (-1 if v=='-' else int(v))
    # constant: term without x, after removing x terms
    s2 = re.sub(r'[+-]?\d*x²','',s)
    s2 = re.sub(r'[+-]?\d*x','',s2)
    mc = re.search(r'([+-]?\d+)', s2)
    if mc: c=int(mc.group(1))
    return a,b,c

problems=0; errs=[]
pb = pd["problem_bank"]
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[tier]):
        problems+=1
        a,b,c = parse_display_quad(p["display"])
        target = {2:a,1:b,0:c}
        opts = p["options"]
        sol = p["solutions"][0]
        # verify solution option expands to target
        lead,facs = parse_expr(opts[sol])
        got = poly_mult(lead,facs)
        g2,g1,g0 = got.get(2,0),got.get(1,0),got.get(0,0)
        if (g2,g1,g0)!=(a,b,c):
            errs.append(f"{tier}[{i}] SOLUTION option {sol} '{opts[sol]}' expands {g2}x^2+{g1}x+{g0} != display {a}x^2+{b}x+{c}")
        # verify other options don't also equal (uniqueness) -- for 'completely' allow
        completely = 'completely' in p['display'].lower()
        for j,o in enumerate(opts):
            if j==sol: continue
            l2,f2=parse_expr(o); gg=poly_mult(l2,f2)
            eq = (gg.get(2,0),gg.get(1,0),gg.get(0,0))==(a,b,c)
            if eq and not completely:
                errs.append(f"{tier}[{i}] DUP option {j} '{o}' also equals target (non-completely q)")
        # verify each misconception expect points to option that expands as message implies
        for k,mc in enumerate(p.get("misconceptions",[])):
            exp = mc["expect"]
            if not isinstance(exp,int) or exp>=len(opts):
                errs.append(f"{tier}[{i}].misc[{k}] expect {exp} not valid index"); continue
            l3,f3=parse_expr(opts[exp]); gg3=poly_mult(l3,f3)
            e2,e1,e0 = gg3.get(2,0),gg3.get(1,0),gg3.get(0,0)
            # pull claimed expansion numbers from message if present
            msg = norm(mc["message"])
            io.write(f"{tier}[{i}].misc[{k}] expect=opt{exp} '{opts[exp]}' -> {e2}x^2+{e1}x+{e0} | pattern={mc['pattern']}\n")

io.write(f"\nProblems checked: {problems}\n")
if errs:
    io.write("ERRORS:\n"+"\n".join(errs)+"\n")
else:
    io.write("No expansion/solution/expect-index errors found.\n")

# em dash scan on student-facing strings
def walk(o,path=""):
    if isinstance(o,dict):
        for k,v in o.items():
            if k=="note": continue
            walk(v,path+"."+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,path+f"[{i}]")
    elif isinstance(o,str):
        if "—" in o or "—" in o:
            io.write(f"EM DASH at {path}: {o[:60]}\n")
walk(pd)
io.write("em dash scan done\n")
