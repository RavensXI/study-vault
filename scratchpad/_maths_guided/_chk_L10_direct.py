# Direct verification: each problem's two equations as functions; check stored x-solutions
# yield a y that satisfies BOTH equations.
probs = [
 # (tier, idx, display, sols, eq1(x,y), eq2(x,y), how to get y)
 ("gold",0,"x+y=7 & x2+y2=25",[4,3], lambda x,y: x+y==7, lambda x,y: x*x+y*y==25),
 ("gold",1,"y=2x+1 & x2+y2=10",[1,-1.8], lambda x,y: y==2*x+1, lambda x,y: abs(x*x+y*y-10)<1e-9),
 ("gold",2,"x-y=1 & x2+y2=13",[3,-2], lambda x,y: x-y==1, lambda x,y: x*x+y*y==13),
 ("gold",3,"y=x+2 & x2+y2=20",[2,-4], lambda x,y: y==x+2, lambda x,y: x*x+y*y==20),
 ("gold",4,"x+y=5 & x2-y=7",[3,-4], lambda x,y: x+y==5, lambda x,y: x*x-y==7),
 ("bronze",0,"y=x+3 & y=x2+1",[2,-1], lambda x,y: y==x+3, lambda x,y: y==x*x+1),
 ("bronze",1,"y=x+6 & y=x2",[3,-2], lambda x,y: y==x+6, lambda x,y: y==x*x),
 ("bronze",2,"y=x+1 & y=x2-2x-3",[4,-1], lambda x,y: y==x+1, lambda x,y: y==x*x-2*x-3),
 ("bronze",3,"y=2x & y=x2",[0,2], lambda x,y: y==2*x, lambda x,y: y==x*x),
 ("bronze",4,"y=x & y=x2+5x+3",[-1,-3], lambda x,y: y==x, lambda x,y: y==x*x+5*x+3),
 ("bronze",5,"y=x-1 & y=x2-3x+2",[1,3], lambda x,y: y==x-1, lambda x,y: y==x*x-3*x+2),
 ("bronze",6,"y=3x & y=x2+2",[1,2], lambda x,y: y==3*x, lambda x,y: y==x*x+2),
 ("bronze",7,"y=x+4 & y=x2+x",[2,-2], lambda x,y: y==x+4, lambda x,y: y==x*x+x),
 ("silver",0,"y=2x+1 & y=x2+x-1",[2,-1], lambda x,y: y==2*x+1, lambda x,y: y==x*x+x-1),
 ("silver",1,"y=x+3 & y=x2-2x-1",[4,-1], lambda x,y: y==x+3, lambda x,y: y==x*x-2*x-1),
 ("silver",2,"y=3-x & y=x2-3",[2,-3], lambda x,y: y==3-x, lambda x,y: y==x*x-3),
 ("silver",3,"y=2x-3 & y=x2-3",[0,2], lambda x,y: y==2*x-3, lambda x,y: y==x*x-3),
 ("silver",4,"x+y=4 & xy=3",[3,1], lambda x,y: x+y==4, lambda x,y: x*y==3),
 ("silver",5,"y=5-2x & y=x2-4x+2",[3,-1], lambda x,y: y==5-2*x, lambda x,y: y==x*x-4*x+2),
 ("silver",6,"y=x+2 & y=x2+x-2",[2,-2], lambda x,y: y==x+2, lambda x,y: y==x*x+x-2),
]

# derive y from eq1 for each; for gold circle probs eq1 gives line so we can solve y
def yfrom(tier,idx,x):
    d = {
     ("gold",0): 7-x, ("gold",1): 2*x+1, ("gold",2): x-1, ("gold",3): x+2, ("gold",4): 5-x,
     ("bronze",0): x+3,("bronze",1):x+6,("bronze",2):x+1,("bronze",3):2*x,("bronze",4):x,
     ("bronze",5):x-1,("bronze",6):3*x,("bronze",7):x+4,
     ("silver",0):2*x+1,("silver",1):x+3,("silver",2):3-x,("silver",3):2*x-3,("silver",4):4-x,
     ("silver",5):5-2*x,("silver",6):x+2,
    }
    return d[(tier,idx)]

bad=0
for tier,idx,disp,sols,e1,e2 in probs:
    for x in sols:
        y=yfrom(tier,idx,x)
        ok1=e1(x,y); ok2=e2(x,y)
        if not (ok1 and ok2):
            print(f"FAIL {tier}[{idx}] {disp} x={x} y={y} eq1={ok1} eq2={ok2}")
            bad+=1
print("done, failures:",bad)
