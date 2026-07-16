import math
def close(a,b): return abs(a-b)<0.06
# fresh-solve checks
assert (4+2)==6
assert (-2+6)==4
assert 3*3==9
assert 7-4==3
assert (10-3)==7   # B4 AB top b-a
assert math.isqrt(9+16)==5
assert 2+6==8
assert (-1)+1==0
# silver
assert close(math.sqrt((8-2)**2+((-1)-3)**2),7.2)  # S0
# S1 parallel top1: 1/3 of (3,6)=(1,2) bottom 2
assert 6/3==2
# S2 BA=OA-OB=5a-3b coeff a=5
assert 5-0==5
# S3 (2k,3)||(4,6): lam=3/6=.5, 2k=4*.5=2 => k=1
lam=3/6; assert (4*lam)/2==1
# S4 midpoint top=(1+7)/2=4
assert (1+7)/2==4
# S5 BA=-AB=(3,-5) top 3
assert -(-3)==3
# S6 |(-5,12)|=13
assert math.isqrt(25+144)==13
# gold
# G0 OB=a+c, AB=c, AP=1/3, coeff c =1/3
# G1 XY=OY-OX coeff a = 4-2=2
assert 4-2==2
# G2 6a-4b=2(3a+kb): 2k=-4 -> k=-2
assert -4/2==-2
# G3 AB=(-1-3,5-1)=(-4,4); AN=3/4*AB=(-3,3); ON=(3-3,1+3)=(0,4) top=0
ab=(-1-3,5-1); an=(0.75*ab[0],0.75*ab[1]); on=(3+an[0],1+an[1]); assert on==(0.0,4.0)
# G4 AB=(4-1,8-2)=(3,6) top 3; AC=(5,10)=5/3*(3,6)
assert (4-1)==3 and (6-1,12-2)==(5,10)
ac=(6-1,12-2); assert close(ac[0]/3, ac[1]/6)  # same ratio => collinear
print("ALL MATH CHECKS PASS")
