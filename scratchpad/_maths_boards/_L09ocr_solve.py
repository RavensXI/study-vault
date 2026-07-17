from fractions import Fraction as F
def solve(a1,b1,c1,a2,b2,c2):
    det=a1*b2-a2*b1
    x=F(c1*b2-c2*b1,det); y=F(a1*c2-a2*c1,det)
    return x,y
# original OCR bank (distinct problems, before repair)
probs={
 'bronze':[(1,1,10,1,-1,4),(2,1,9,1,1,6),(3,1,11,1,1,5),(1,2,8,1,1,5),(2,1,7,3,-1,8),(1,3,13,1,1,7),(4,1,14,2,1,8)],
 'silver':[(3,2,16,1,-2,0),(2,3,18,4,3,24),(3,2,11,2,3,9),(5,-2,4,3,2,12),(4,5,23,3,5,18)],
 'gold':[(2,3,12,5,-2,11),(3,4,5,2,-3,9)],
}
for t,ps in probs.items():
    print('==',t)
    seen={}
    for i,p in enumerate(ps):
        x,y=solve(*p)
        key=(x,y)
        dup=' <DUP with %d>'%seen[key] if key in seen else ''
        seen[key]=i
        integ = (x.denominator==1 and y.denominator==1)
        print("  [%d] %s -> x=%s y=%s int=%s%s"%(i,p,x,y,integ,dup))
