import json, re

live = json.load(open("_CHK_L09eduqas_live.json", encoding="utf-8"))
pre  = json.load(open("_pre_dump_maths-eduqas.json", encoding="utf-8"))
ID="038c2343-8acf-41e4-b02a-914268bc6572"
pre_pd=None
for v in pre:
    if v.get("id")==ID or v.get("slug")=="simultaneous-equations-linear":
        pre_pd=v.get("practice_data", v); break

errors=[]
EMDASH="—"
def scan(obj, path):
    if isinstance(obj, str):
        if EMDASH in obj: errors.append(("EMDASH", path, obj[:70]))
    elif isinstance(obj, dict):
        for k,val in obj.items():
            if k=="note": continue
            scan(val, path+"."+k)
    elif isinstance(obj, list):
        for i,val in enumerate(obj): scan(val, f"{path}[{i}]")
scan(live, "root")

def parse_eq(s):
    s=s.replace("−","-").replace(" ","")
    lhs,rhs=s.split("=")
    rhs=int(rhs)
    a=b=0
    for m in re.finditer(r'([+-]?\d*)x', lhs):
        t=m.group(1); a+= 1 if t in("","+") else (-1 if t=="-" else int(t))
    for m in re.finditer(r'([+-]?\d*)y', lhs):
        t=m.group(1); b+= 1 if t in("","+") else (-1 if t=="-" else int(t))
    return a,b,rhs

def solve(disp):
    eqs=re.findall(r'\\((.+?)\\)', disp)
    a1,b1,c1=parse_eq(eqs[0]); a2,b2,c2=parse_eq(eqs[1])
    det=a1*b2-a2*b1
    return (c1*b2-c2*b1)/det, (a1*c2-a2*c1)/det

pb=live["problem_bank"]
for tier in ["bronze","silver","gold"]:
    seen={}
    for i,p in enumerate(pb[tier]):
        disp=p["display"]; sol=p["solutions"]
        x,y=solve(disp)
        if abs(x-sol[0])>1e-9 or abs(y-sol[1])>1e-9:
            errors.append(("SOLUTION",f"{tier}[{i}]",f"{disp} stored={sol} fresh=({x},{y})"))
        if p.get("calculator")==False and (abs(x-round(x))>1e-9 or abs(y-round(y))>1e-9):
            errors.append(("NONCALC_MESSY",f"{tier}[{i}]",f"{disp}->({x},{y})"))
        seen.setdefault(disp,[]).append(i)
        # final numeric box must equal a solution component; check last two 'x='/'y=' style
    dups={d:ix for d,ix in seen.items() if len(ix)>1}
    if dups: errors.append(("DUP",tier,str(dups)))

# cross-tier duplicate displays
alldisp={}
for tier in ["bronze","silver","gold"]:
    for i,p in enumerate(pb[tier]):
        alldisp.setdefault(p["display"],[]).append(f"{tier}[{i}]")
xdup={d:ix for d,ix in alldisp.items() if len(ix)>1}
if xdup: errors.append(("XTIER_DUP","-",str(xdup)))

# ---- preservation diff ----
if pre_pd:
    for fld in ["related_videos","topic_links","worked_examples"]:
        a=json.dumps(pre_pd.get(fld),sort_keys=True,ensure_ascii=False)
        b=json.dumps(live.get(fld),sort_keys=True,ensure_ascii=False)
        if a!=b:
            errors.append(("PRESERVE",fld,f"PRE={a[:120]} | LIVE={b[:120]}"))
    print("pre keys:", sorted(pre_pd.keys()))
    print("live keys:", sorted(live.keys()))
else:
    print("!! pre_pd not found")

print("\n=== FINDINGS ===")
for e in errors: print(e)
print("total:",len(errors))
