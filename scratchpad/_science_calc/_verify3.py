import json,re
pd=json.load(open('_live_canonical.json'))
def close(a,b,tol=1e-9): return abs(a-b)<=tol
errs=[]
bank=pd['problem_bank']

# Verify every box 'pre' arithmetic "X op Y = " matches answer
opmap={'÷':lambda a,b:a/b,'×':lambda a,b:a*b,'+':lambda a,b:a+b,'−':lambda a,b:a-b,'-':lambda a,b:a-b}
def check_expr(pre,ans):
    # find last "... = " expression like "a op b = " possibly "a op b op c = "
    m=re.search(r'([-\d\.]+(?:\s*[÷×+−]\s*[-\d\.]+)+)\s*=\s*$',pre.strip())
    if not m: return None
    expr=m.group(1)
    toks=re.split(r'\s*([÷×+−])\s*',expr)
    try:
        val=float(toks[0])
        i=1
        while i<len(toks):
            op=toks[i]; nxt=float(toks[i+1]); val=opmap[op](val,nxt); i+=2
        return val
    except: return None

for tier in ['bronze','silver','gold']:
    for pi,p in enumerate(bank[tier]):
        for si,st in enumerate(p.get('guided_steps',[])):
            if 'answer' not in st: continue
            v=check_expr(st.get('pre',''),st['answer'])
            if v is not None and not close(v,st['answer'],1e-6):
                errs.append(f"{tier}[{pi}].guided_steps[{si}] pre='{st['pre']}' computes {v} != answer {st['answer']}")
# teach + opener too
for tier in ['bronze','silver','gold']:
    for si,st in enumerate(pd['guided']['teach'][tier]['steps']):
        if 'answer' not in st: continue
        v=check_expr(st.get('pre',''),st['answer'])
        if v is not None and not close(v,st['answer'],1e-6):
            errs.append(f"teach.{tier}[{si}] '{st['pre']}' -> {v} != {st['answer']}")
for si,st in enumerate(pd['guided']['opener']['steps']):
    if 'answer' not in st: continue
    v=check_expr(st.get('pre',''),st['answer'])
    if v is not None and not close(v,st['answer'],1e-6):
        errs.append(f"opener[{si}] '{st['pre']}' -> {v} != {st['answer']}")

print("BOX ARITH errs:")
for e in errs: print(" ",e)
print("total",len(errs))
