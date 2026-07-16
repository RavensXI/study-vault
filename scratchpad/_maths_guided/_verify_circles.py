import math
# gold circle problems: (label, r2, line_fn given x, sols x)
cases = [
 ("gold0", 25, lambda x: 7-x, [4,3], "x+y=7"),
 ("gold1", 10, lambda x: 2*x+1, [1,-1.8], "y=2x+1"),
 ("gold2", 13, lambda x: x-1, [3,-2], "x-y=1"),
 ("gold3", 20, lambda x: x+2, [2,-4], "y=x+2"),
]
for name,r2,f,xs,ln in cases:
    print(name, ln, "r=%.4f"%math.sqrt(r2))
    for x in xs:
        y=f(x)
        chk=x*x+y*y
        print("   x=%s y=%s  x^2+y^2=%.4f (want %d) %s"%(x,y,chk,r2,"OK" if abs(chk-r2)<1e-6 else "MISMATCH"))
