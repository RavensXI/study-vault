from fractions import Fraction as F
def solve(a1,b1,c1,a2,b2,c2):
    det=a1*b2-a2*b1
    return F(c1*b2-c2*b1,det), F(a1*c2-a2*c1,det)

# repaired bank
bank={
 'bronze':[(1,1,10,1,-1,4),(2,1,9,1,1,6),(3,1,11,1,1,5),(1,2,8,1,1,5),(2,1,7,3,-1,8),(1,3,13,1,1,7),(3,1,14,1,1,6)],
 'silver':[(3,2,16,1,1,6),(2,3,18,1,1,7),(3,2,11,1,1,4),(5,-2,4,1,1,5),(3,4,23,1,2,11)],
 'gold':[(2,3,12,5,-2,11),(3,4,5,2,-3,9)],
}
# teach
teach={'bronze':(3,1,12,1,1,6),'silver':(2,3,13,1,1,5),'gold':(4,3,18,3,2,13)}
def single_multiply_ok(p):
    a1,b1,c1,a2,b2,c2=p
    # can a single scale of one eq match a coeff (x or y)?
    for var in ('x','y'):
        if var=='x': u,v=a1,a2
        else: u,v=b1,b2
        if u==0 or v==0: continue
        if abs(v)%abs(u)==0 and abs(v)!=abs(u): return True
        if abs(u)%abs(v)==0 and abs(u)!=abs(v): return True
    return False
def already_match(p):
    a1,b1,c1,a2,b2,c2=p
    return abs(a1)==abs(a2) or abs(b1)==abs(b2)
for t,ps in bank.items():
    print('==',t)
    seen={}
    for i,p in enumerate(ps):
        x,y=solve(*p)
        key=(x,y); dup=' DUP' if key in seen else ''; seen[key]=i
        integ=x.denominator==1 and y.denominator==1
        print("  [%d] %s -> (%s,%s) int=%s match=%s single=%s%s"%(i,p,x,y,integ,already_match(p),single_multiply_ok(p),dup))
print('== teach')
for t,p in teach.items():
    x,y=solve(*p)
    print("  %s %s -> (%s,%s) match=%s single=%s"%(t,p,x,y,already_match(p),single_multiply_ok(p)))
# word problem
from fractions import Fraction as F2
# a+c=120, 8a+5c=780
x,y=solve(1,1,120,8,5,780)
print('word cinema adults,children=',x,y)
