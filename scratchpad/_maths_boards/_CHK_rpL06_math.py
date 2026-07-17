import math
def r(x,n): return round(x,n)

print("== GOLD ==")
# g0 tangent (0,1)(4,13)
print("g0", (13-1)/(4-0), "inv", round(4/12,3))
# g1 NR (2x^3+5)/(3x^2) x0=2 x2 3dp
x=2; num=2*x**3+5; den=3*x**2; x1=num/den; print("g1 x1",x1)
x2=(2*x1**3+5)/(3*x1**2); print("g1 x2",r(x2,3), "num",round(2*x1**3+5,3),"den",round(3*x1**2,3))
# misc: x^3+5 throughout
x=2; a=(x**3+5)/(3*x**2); b=(a**3+5)/(3*a**2); print("g1 misc drop2: x1",round(a,3),"x2",round(b,3))
# g2 pop
P0=2000; P10=2000*1.05**10; print("g2 P10",round(P10),"chg",round(P10)-2000,"rate",round((round(P10)-2000)/10),"exactrate",round((P10-2000)/10))
# g3 trapezium
h=[0,1,4,9,16]; area=0.5*1*(h[0]+h[-1]+2*(h[1]+h[2]+h[3])); print("g3 area",area,"misc no double",0.5*(h[0]+h[-1]+h[1]+h[2]+h[3]))
# g4 x=sqrt(2x+15)
import numpy as np
print("g4 roots", np.roots([1,-2,-15]))

print("== BRONZE ==")
print("b0",80/4,"b1",(20-4)/(5-1),"b2 x2",3+4+4,"b3",2*4-1,"b3misc",2*(4-1))
print("b4 accel",0,"misc",12/8,"b5",3**2-4,"b6",48/6,"b6misc",round(6/48,3))
print("== SILVER ==")
x=3;x1=10/(x+1);x2=10/(x1+1);print("s0 x1",x1,"x2",r(x2,2),"chk",round(2.86*3.5,2))
print("s1",(25-5)/4,"s2",r((3**2+5)/(2*3),3),"s2misc",r(14/3,3))
print("s3 f2",2**3-2-5,"f1",1-1-5,"misc 2^3=6",6-2-5)
print("s4",(20-8)/3)
x=1;i1=3*x+1;x1=math.sqrt(i1);i2=3*x1+1;x2=math.sqrt(i2);print("s5 x1",x1,"x2",r(x2,2))
x=4;i1=2*x+3;x1=math.sqrt(i1);print("s6 x1 4dp",r(x1,4));x1r=r(x1,4);i2=2*x1r+3;x2=math.sqrt(round(i2,4));print("s6 i2",round(i2,4),"x2",r(x2,3),"misc x1 3dp",r(x1,3))
print("== TEACH ==")
x=3;num=2*x**3+20;den=3*x**2;x1=num/den;print("tg num",num,"den",den,"x1 4dp",r(x1,4));x1r=r(x1,4)
x2=(2*x1r**3+20)/(3*x1r**2);print("tg x2",r(x2,3),"chk 2.715^3",round(2.715**3))
x=2;x1=12/(x+2);x2=12/(x1+2);print("ts x1",x1,"x2",x2)
print("tb", (15-3)/(5-1))
print("== TIER EX ==")
x=2;print("gold ex",r((2*x**3+7)/(3*x**2),3),"cbrt7",round(7**(1/3),4))
x=1;x1=math.sqrt(4*x+5);x2=math.sqrt(4*x1+5);print("silver ex x1",x1,"x2",r(x2,2))
x=1;x1=math.sqrt(3*x+1);x2=math.sqrt(3*x1+1);print("mcard x1",x1,"x2",round(x2,2))
print("== OPENER ==")
t=200;d1=t/2+60;d2=d1/2+60;print("opener",d1,d2,"fixed",120)
print("== WE ==")
print("we0",120/4,"we1 x2",r((1.75**2+3)/(2*1.75),3),"we2",(30-10)/5)
