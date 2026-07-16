import math
# Figure 1 teach.gold grid: origin x=16 y=106, unit=16px
def px2c(cx,cy,ox,oy,u): return ((cx-ox)/u,(oy-cy)/u)
print("teach P:", px2c(80,74,16,106,16), "expect (4,2)")
# gold[3] grid origin x=34 y=100 unit=18
print("gold3 A:",px2c(88,82,34,100,18),"B:",px2c(16,10,34,100,18),"N:",px2c(34,28,34,100,18))
# N=A+3/4(B-A)
A=(3,1);B=(-1,5); N=(A[0]+0.75*(B[0]-A[0]),A[1]+0.75*(B[1]-A[1])); print("N calc",N,"ON top sol=0")
# gold4 origin x=16 y=166 unit=13
print("gold4 A:",px2c(29,140,16,166,13),"B:",px2c(68,62,16,166,13),"C:",px2c(94,10,16,166,13))
# collinear check
print("slopes",(8-2)/(4-1),(12-8)/(6-4))
# silver midpoint origin x=16 y=100 unit=18
print("mid A:",px2c(34,10,16,100,18),"B:",px2c(142,46,16,100,18),"M:",px2c(88,28,16,100,18),"mid=",( (1+7)/2,(5+3)/2))
# triangles proportionality
print("bronze5 tri 66:88 =",66/88, "vs 3/4=",3/4)
print("silver7 tri 45:108 =",45/108,"vs 5/12=",5/12)
# parallelogram P
Ax,Ay=42,52;Bx,By=190,52; Px=Ax+(1/3)*(Bx-Ax); print("para P x",Px,"svg 91.3")
# magnitudes
print("mag(3,4)=",math.hypot(3,4),"mag(-5,12)=",math.hypot(-5,12),"mag AB(6,-4)=",round(math.hypot(6,-4),1))
