# -*- coding: utf-8 -*-
import os, json, re, urllib.request
from fractions import Fraction as F

LID = "fe589e29-485c-4272-94df-41687f398c1b"
BASE = "https://baipckgywpnwapobwtsy.supabase.co/rest/v1/lessons"
KEY = os.environ["SUPABASE_SERVICE_KEY"]

def fetch():
    url = BASE + "?id=eq." + LID + "&select=practice_data"
    req = urllib.request.Request(url, headers={"apikey": KEY, "Authorization": "Bearer " + KEY})
    return json.load(urllib.request.urlopen(req))[0]["practice_data"]

pd = fetch()
json.dump(pd, open("_L02_fresh.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("Fetched fresh. Top keys:", sorted(pd.keys()))

# ---- fresh-solve every problem from its LaTeX display ----
def parse_frac(s):
    # mixed number  a\frac{b}{c}
    m = re.match(r'^(\d+)\\t?frac\{(\d+)\}\{(\d+)\}$', s)
    if m:
        a,b,c = map(int, m.groups()); return F(a)*1 + F(b,c) if False else F(a*c+b, c)
    m = re.match(r'^\\t?frac\{(\d+)\}\{(\d+)\}$', s)
    if m:
        b,c = map(int, m.groups()); return F(b,c)
    if re.match(r'^\d+$', s):
        return F(int(s))
    raise ValueError("cannot parse operand: %r" % s)

def solve(display):
    # strip \( \)
    e = display.strip()
    e = e.replace("\\(","").replace("\\)","").strip()
    # tokenise operands and ops (+,-,\times,\div). minus only as operator between operands here.
    # replace operators with spaces markers
    e2 = e.replace("\\times"," * ").replace("\\div"," / ").replace("+"," + ").replace("−"," - ").replace("-"," - ")
    toks = e2.split()
    # rebuild: operands may have been split? our operand regex has no spaces, ok.
    # evaluate with precedence: * and / left-to-right before + and -
    # first pass parse operands
    vals=[]; ops=[]
    i=0
    for t in toks:
        if t in ("+","-","*","/"):
            ops.append(t)
        else:
            vals.append(parse_frac(t))
    # do * and /
    v=[vals[0]]; o=[]
    k=0
    # rebuild sequence
    seq=[vals[0]]
    for idx,op in enumerate(ops):
        seq.append(op); seq.append(vals[idx+1])
    # pass 1 * /
    res=[seq[0]]
    j=1
    while j < len(seq):
        op=seq[j]; nxt=seq[j+1]
        if op=="*": res[-1]=res[-1]*nxt
        elif op=="/": res[-1]=res[-1]/nxt
        else: res.append(op); res.append(nxt)
        j+=2
    # pass 2 + -
    total=res[0]; j=1
    while j<len(res):
        op=res[j]; nxt=res[j+1]
        total = total+nxt if op=="+" else total-nxt
        j+=2
    return total

def sol_to_frac(sols):
    if len(sols)==1: return F(sols[0])
    return F(sols[0], sols[1])

problems=[]
pb=pd["problem_bank"]
errors=[]
for tier in ("bronze","silver","gold"):
    for idx,p in enumerate(pb[tier]):
        disp=p["display"]
        try:
            got=solve(disp)
        except Exception as ex:
            errors.append("%s[%d] PARSE FAIL %r: %s"%(tier,idx,disp,ex)); continue
        stored=sol_to_frac(p["solutions"])
        # stored fraction may be unsimplified representation; compare value
        if got != stored:
            errors.append("%s[%d] %s -> solve=%s stored=%s(%s)"%(tier,idx,disp,got,stored,p["solutions"]))
        # also check stored solutions in lowest terms for fraction type
        if p.get("input_type")=="fraction" and len(p["solutions"])==2:
            n,d=p["solutions"]
            g=F(n,d)
            if (g.numerator, g.denominator) != (n, d):
                errors.append("%s[%d] solutions not lowest terms: %s vs %s/%s"%(tier,idx,p["solutions"],g.numerator,g.denominator))

print("\n=== FRESH-SOLVE ===")
if errors:
    for e in errors: print("  MISMATCH:", e)
else:
    print("  All %d problems: stored solutions match fresh-solve, fraction answers in lowest terms."%(sum(len(pb[t]) for t in ('bronze','silver','gold'))))

# ---- misconception expects: check they are NOT the correct answer and are 2-int lists where present ----
print("\n=== MISCONCEPTION EXPECTS ===")
mprob=[]
for tier in ("bronze","silver","gold"):
    for idx,p in enumerate(pb[tier]):
        stored=p["solutions"]
        for j,m in enumerate(p.get("misconceptions",[])):
            e=m.get("expect")
            if e is None: continue
            if e==stored:
                mprob.append("%s[%d].mis[%d] expect equals answer"%(tier,idx,j))
print("  expects present, none equal the correct answer" if not mprob else "\n".join("  "+x for x in mprob))

# ---- teach + opener box internal consistency (final boxes exist) ----
print("\n=== TEACH/OPENER present ===")
for t in ("bronze","silver","gold"):
    tt=pd["guided"]["teach"][t]
    nb=sum(1 for s in tt["steps"] if s.get("answer") is not None)
    print("  teach.%s boxes=%d display=%s"%(t,nb,tt["display"]))
opb=sum(1 for s in pd["guided"]["opener"]["steps"] if s.get("answer") is not None)
print("  opener boxes=%d"%opb)

# ---- preservation vs pre-dump ----
print("\n=== PRESERVATION vs pre-dump ===")
pre=json.load(open("_pre_dump_maths-ocr.json",encoding="utf-8"))
def find_pre(pre):
    if isinstance(pre,list):
        for r in pre:
            if r.get("id")==LID: return r
    elif isinstance(pre,dict):
        if LID in pre: return pre[LID]
        for k,v in pre.items():
            if isinstance(v,dict) and v.get("id")==LID: return v
    return None
pr=find_pre(pre)
if pr is None:
    print("  pre-dump entry NOT FOUND (keys sample:", (list(pre)[:3] if isinstance(pre,dict) else type(pre)), ")")
else:
    ppd = pr.get("practice_data", pr)
    for fld in ("related_videos","topic_links","worked_examples"):
        a=json.dumps(ppd.get(fld),sort_keys=True,ensure_ascii=False)
        b=json.dumps(pd.get(fld),sort_keys=True,ensure_ascii=False)
        print("  %s: %s"%(fld, "SAME" if a==b else "DIFF"))
        if a!=b:
            print("     pre :", (a[:200] if a else a))
            print("     live:", (b[:200] if b else b))
