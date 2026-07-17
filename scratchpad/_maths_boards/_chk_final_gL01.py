import json,sys
sys.stdout.reconfigure(encoding="utf-8")
live=json.load(open("_chk_gL01_live.json",encoding="utf-8"))["practice_data"]
b=live["problem_bank"]
def g(x1,y1,x2,y2): return (y2-y1)/(x2-x1)
# fresh-solve each stored solution manually encoded
checks=[
 # tier,i, computed solution
 ("gold",0, g(-3,11,5,-5)),
 ("gold",1, 5-3*2),                 # c: m=(17-5)/(6-2)=3; 5=3*2+c
 ("gold",2, 0),                     # A=2, B=(3-7)/(2-0)=-2, not parallel
 ("gold",3, -5/2),                  # 5x+2y=20 -> y=-2.5x+10
 ("gold",4, 2*5-7),                 # a: (a+7)/2=5
 ("bronze",0, g(0,2,3,8)),
 ("bronze",1, g(1,4,5,16)),
 ("bronze",2, 5),
 ("bronze",3, 4),
 ("bronze",4, g(2,1,6,5)),
 ("bronze",5, 5*3+1),
 ("bronze",6, 2*3+1),               # chart y=2x+1 at x=3
 ("bronze",7, -2),                  # chart y=10-2x gradient
 ("silver",0, g(-1,4,3,-8)),
 ("silver",1, (11-3)/2),            # y=mx+3 through(2,11)
 ("silver",2, 6/2),                 # 2y=6x+10 -> y=3x+5
 ("silver",3, g(-2,-3,4,9)),
 ("silver",4, g(0,-2,4,18)),
 ("silver",5, 18/3),               # 3y-9x=18 -> y=3x+6, intercept 6
 ("silver",6, 7-(g(1,7,3,3))*1),   # c: m=-2, 7=-2*1+c -> 9
]
bad=[]
for tier,i,comp in checks:
    sol=b[tier][i]["solutions"][0]
    if float(comp)==int(comp): comp=int(comp)
    if comp!=sol: bad.append(f"{tier}[{i}] computed {comp} != stored {sol}")
print("SOLUTIONS:","all match" if not bad else "MISMATCH")
for x in bad: print(" -",x)

# reproduce determinate misconception expects
def expect_check(tier,i,fn):
    mc=b[tier][i]["misconceptions"][0]
    got=fn()
    if float(got)==int(got): got=int(got)
    if got!=mc["expect"]:
        print(f" EXPECT MISMATCH {tier}[{i}]: reproduced {got} != stored {mc['expect']}")
# a few key ones
expect_check("gold",0, lambda: abs(g(-3,11,5,-5)))          # drop sign -> 2
expect_check("gold",1, lambda: 5+3*2)                        # add instead -> 11
expect_check("bronze",0, lambda: 3/6)                        # invert -> 0.5
expect_check("bronze",5, lambda: 5*(3+1))                    # oop -> 20
expect_check("silver",3, lambda: 12/2)                       # run as 2 -> 6
print("expects (spot) reproduced")
