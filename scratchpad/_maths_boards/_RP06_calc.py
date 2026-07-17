# -*- coding: utf-8 -*-
import math

def r(x, n): return round(x, n)

print("== BRONZE ==")
print("B1 speed 80/4 =", 80/4)
print("B2 grad (20-4)/(5-1) =", (20-4)/(5-1))
print("B3 x_{n+1}=x+4 x0=3: x1", 3+4, "x2", 3+4+4)
print("B4 2*4-1 =", 2*4-1, "misc 2*(4-1)=", 2*(4-1))
print("B5 accel horizontal =", 0, "misc 12/8=", 12/8)
print("B6 x^2-4 x0=3:", 3**2-4, "misc forgot", 3**2)
print("B7 accel 48/6 =", 48/6, "misc 6/48=", 6/48)

print("== SILVER ==")
x=3
x1=10/(x+1); x2=10/(x1+1)
print("S1 x1",x1,"x2",x2, "->2dp", r(x2,2))
print("S2 decel (25-5)/4 =", (25-5)/4)
x=3; x1=(x**2+5)/(2*x)
print("S3 x1 (9+5)/6 =", x1, "->3dp", r(x1,3), "misc 14/3=", r(14/3,3))
print("S4 f(x)=x^3-x-5 f(1)",1-1-5,"f(2)",8-2-5, "misc 6-2-5=",6-2-5)
print("S5 accel (20-8)/3 =", (20-8)/3)
x=1; x1=math.sqrt(3*x+1); x2=math.sqrt(3*x1+1)
print("S6 x1",x1,"x2",x2,"->2dp",r(x2,2))
x=4; x1=math.sqrt(2*x+3); x2=math.sqrt(2*x1+3)
print("S7 x1",x1,"->3dp",r(x1,3),"x2",x2,"->3dp",r(x2,3))

print("== GOLD ==")
print("G1 grad (13-1)/(4-0) =", (13-1)/(4-0), "misc run/rise 4/12=", r(4/12,3))
x=2.0
n1=2*x**3+5; d1=3*x**2; x1=n1/d1
n2=2*x1**3+5; d2=3*x1**2; x2=n2/d2
print("G2 x1", x1, "x2", x2, "->3dp", r(x2,3), "cbrt5", 5**(1/3))
P0=2000*1.05**0; P10=2000*1.05**10
print("G3 P10",P10,"round",round(P10),"change",round(P10)-2000,"rate",(round(P10)-2000)/10)
print("   exact change/10:", (P10-2000)/10)
# trapezium
h=[0,1,4,9,16]
area=0.5*1*(h[0]+h[-1]+2*(h[1]+h[2]+h[3]))
print("G4 trapezium area", area, "misc forgot double 0.5*(16+14)=", 0.5*(0+16+14))
print("G5 x^2-2x-15=0 roots", 5, -3)

print("== TEACH GOLD (2x^3+20)/(3x^2) x0=3 ==")
x=3.0
n1=2*x**3+20; d1=3*x**2; x1=n1/d1
n2=2*x1**3+20; d2=3*x1**2; x2=n2/d2
print("num",n1,"den",d1,"x1",x1,"->4dp",r(x1,4))
print("x2",x2,"->3dp",r(x2,3),"cbrt20",20**(1/3))
print("check 2.715^3", r(2.715**3,2))
print("== TEACH SILVER 12/(x+2) x0=2 ==")
x=2; x1=12/(x+2); x2=12/(x1+2)
print("x1",x1,"x2",x2,"check 2.4*5",2.4*5)
print("== TEACH BRONZE (1,3)(5,15) ==")
print("rise",15-3,"run",5-1,"grad",(15-3)/(5-1),"check 3*4",3*4)
print("== OPENER fish tank x/2+60 x0=200 ==")
v=200; v1=v/2+60; v2=v1/2+60
print("v1",v1,"v2",v2,"fixed",120)
