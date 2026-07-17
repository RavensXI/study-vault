import json
pd=json.load(open("_CHK_L10_live.json",encoding="utf-8"))
bank=pd['problem_bank']
errs=[]

# (tier, index, eq1(x,y)->bool via residual, eq2, stored_sols, y_from_x)
# Encode each equation as residual function; check =0.
tests = {
 'gold':[
   # 0: y=2x+1, x^2+y^2=10 ; sols[1,-1.8]
   (lambda x,y: y-(2*x+1), lambda x,y: x*x+y*y-10, lambda x:2*x+1, [1,-1.8]),
   # 1: x+y=5, x^2+y^2=13
   (lambda x,y: x+y-5, lambda x,y: x*x+y*y-13, lambda x:5-x, [2,3]),
   # 2: y=x-1, x^2+y^2=25
   (lambda x,y: y-(x-1), lambda x,y: x*x+y*y-25, lambda x:x-1, [4,-3]),
   # 3: y=3-x, xy=2
   (lambda x,y: y-(3-x), lambda x,y: x*y-2, lambda x:3-x, [1,2]),
   # 4: x+y=7, xy=10
   (lambda x,y: x+y-7, lambda x,y: x*y-10, lambda x:7-x, [2,5]),
 ],
 'bronze':[
   (lambda x,y: y-x, lambda x,y: y-x*x, lambda x:x, [0,1]),
   (lambda x,y: y-2*x, lambda x,y: y-x*x, lambda x:2*x, [0,2]),
   (lambda x,y: y-3, lambda x,y: y-(x*x-1), lambda x:3, [2,-2]),
   (lambda x,y: y-(x+2), lambda x,y: y-x*x, lambda x:x+2, [2,-1]),
   (lambda x,y: y-10, lambda x,y: y-(x*x+1), lambda x:10, [3,-3]),
   (lambda x,y: y-(x+6), lambda x,y: y-x*x, lambda x:x+6, [3,-2]),
   (lambda x,y: y-(-x), lambda x,y: y-(x*x-2), lambda x:-x, [-2,1]),
   (lambda x,y: y-4*x, lambda x,y: y-(x*x+3), lambda x:4*x, [1,3]),
 ],
 'silver':[
   (lambda x,y: y-(x+3), lambda x,y: y-(x*x+1), lambda x:x+3, [2,-1]),
   (lambda x,y: y-(2-x), lambda x,y: y-(x*x-4), lambda x:2-x, [2,-3]),
   (lambda x,y: y-(2*x-1), lambda x,y: y-(x*x-2*x+2), lambda x:2*x-1, [1,3]),
   (lambda x,y: y-(x+1), lambda x,y: y-(x*x-x-2), lambda x:x+1, [3,-1]),
   (lambda x,y: y-3*x, lambda x,y: y-(x*x+2), lambda x:3*x, [1,2]),
   (lambda x,y: y-x, lambda x,y: y-(x*x-4*x+4), lambda x:x, [1,4]),
   (lambda x,y: y-(5-2*x), lambda x,y: y-(x*x-3), lambda x:5-2*x, [2,-4]),
 ],
}
for tier in tests:
    for i,(e1,e2,yf,expsols) in enumerate(tests[tier]):
        stored=bank[tier][i]['solutions']
        if sorted(stored)!=sorted(expsols):
            errs.append(f"{tier}[{i}] stored solutions {stored} != my {expsols}")
        for xv in stored:
            y=yf(xv)
            if abs(e1(xv,y))>1e-9 or abs(e2(xv,y))>1e-9:
                errs.append(f"{tier}[{i}] x={xv} y={y}: eq1res={e1(xv,y)} eq2res={e2(xv,y)}")
print("SOLUTION+PAIR errors:", len(errs))
for e in errs: print("  ",e)

# Now teach walks
teach=pd['guided']['teach']
tests_teach={
 'gold':(lambda x,y: x+y-6, lambda x,y: x*x+y*y-20, lambda x:6-x,[2,4]),
 'bronze':(lambda x,y: y-5*x, lambda x,y: y-(x*x+4), lambda x:5*x,[1,4]),
 'silver':(lambda x,y: y-(4*x-5), lambda x,y: y-(x*x-x+1), lambda x:4*x-5,[2,3]),
}
terr=[]
for tier,(e1,e2,yf,roots) in tests_teach.items():
    for xv in roots:
        y=yf(xv)
        if abs(e1(xv,y))>1e-9 or abs(e2(xv,y))>1e-9:
            terr.append(f"teach.{tier} x={xv} fails")
print("TEACH roots errors:", len(terr)); 
for e in terr: print("  ",e)
