import json
pd=json.load(open("_CHK_graphsL05_live.json",encoding="utf-8"))
bank=pd["problem_bank"]
errs=[]
def near(a,b,t=0.02): return abs(a-b)<=t
# define expected fn per chart problem by (tier,idx)
def check(tier,idx,fn,label):
    p=bank[tier][idx]
    if "chart" not in p:
        errs.append(f"{tier}[{idx}] MISSING chart ({label})"); return
    for ds_i,ds in enumerate(p["chart"]["data"]["datasets"]):
        f=fn.get(ds_i)
        if f is None: continue
        for pt in ds["data"]:
            x,y=pt["x"],pt["y"]
            ey=f(x)
            if ey is None: continue
            if not near(y,ey):
                errs.append(f"{tier}[{idx}] ds{ds_i} x={x}: chart y={y} expected {round(ey,4)}")
# gold[4]: 1/x (ds0,ds1), y=4x (ds2)
check("gold",4,{0:lambda x:1/x,1:lambda x:1/x,2:lambda x:4*x},"1/x & 4x")
# bronze[3]: 1/x
check("bronze",3,{0:lambda x:1/x,1:lambda x:1/x},"1/x")
# bronze[5]: x^3
check("bronze",5,{0:lambda x:x**3},"x^3")
# bronze[6]: 1/x
check("bronze",6,{0:lambda x:1/x,1:lambda x:1/x},"1/x")
# silver[4]: -1/x
check("silver",4,{0:lambda x:-1/x,1:lambda x:-1/x},"-1/x")
# silver[6]: x^3 (ds0), -x^3 (ds1)
check("silver",6,{0:lambda x:x**3,1:lambda x:-(x**3)},"x^3 & -x^3")
print("CHART ERRORS:",len(errs))
for e in errs: print(" ",e)
