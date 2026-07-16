import json,sys,io,math
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding="utf-8")
live=json.load(open("_CHK_algL08_LIVE_verify.json",encoding="utf-8"))
r2=lambda v:round(v,2)
fails=[]
def parse_disp(d):
    # extract a,b,c from \(...\)
    import re
    m=re.search(r'\\((.*?)\\)',d); return m.group(1) if m else d

# For every bronze/silver two_solutions with sign_of_b: uses +b => roots (b±√)/2a
def sign_of_b(a,b,c):
    d=b*b-4*a*c; s=math.sqrt(d); return (b+s)/(2*a),(b-s)/(2*a)
def divide_by_2(a,b,c):
    d=b*b-4*a*c; s=math.sqrt(d); return (-b+s)/2,(-b-s)/2

bank=live["problem_bank"]
# map each problem: recompute a,b,c by hand table
coef={
 ("gold",2):(2,-12,7),
 ("bronze",0):(1,3,-10),("bronze",1):(1,-5,6),("bronze",2):(1,1,-12),
 ("bronze",3):(1,-7,10),("bronze",4):(1,5,-6),("bronze",5):(1,-4,-5),
 ("bronze",6):(1,6,5),("bronze",7):(1,-2,-3),
 ("silver",0):(1,4,1),("silver",1):(2,3,-4),("silver",4):(3,-2,-4),
}
for tier in ("gold","bronze","silver"):
    for i,prob in enumerate(bank[tier]):
        a,b,c=coef.get((tier,i),(None,None,None))
        for mc in prob.get("misconceptions",[]):
            pat=mc.get("check"); exp=mc.get("expect")
            if pat=="sign_of_b" and a is not None:
                p,m=sign_of_b(a,b,c)
                if prob["input_type"]=="two_solutions":
                    got=sorted([r2(p),r2(m)]); want=sorted(exp)
                    if got!=want: fails.append((tier,i,"sign_of_b",got,want))
                else:
                    # single value -> depends which root; skip
                    pass
            if pat=="divide_by_2" and a is not None:
                p,m=divide_by_2(a,b,c)
                got=sorted([r2(p),r2(m)]); want=sorted(exp)
                if got!=want: fails.append((tier,i,"divide_by_2",got,want))
print("sign_of_b/divide_by_2 fails:",fails)

# completion boundaries
for tier in ("gold","bronze","silver"):
    for i,prob in enumerate(bank[tier]):
        if prob["input_type"]=="multiple_choice": continue
        gs=prob.get("guided_steps",[])
        boxidx=[j for j,s in enumerate(gs) if "answer" in s]
        firstphase=next((j for j,s in enumerate(gs) if s.get("phase")=="substitute"),None)
        if firstphase is None: fails.append((tier,i,"no phase")); continue
        before=[j for j in boxidx if j<firstphase]
        after=[j for j in boxidx if j>=firstphase]
        if len(before)<1 or len(after)<2:
            fails.append((tier,i,"boundary",len(before),len(after)))
print("boundary fails:",[f for f in fails if len(f)>3 and f[2]=='boundary'] )
print("ALL FAILS:",fails)
