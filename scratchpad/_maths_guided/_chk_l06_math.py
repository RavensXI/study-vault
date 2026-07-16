# -*- coding: utf-8 -*-
import math

def rnd(x,n): return round(x,n)

print("=== GOLD[0] iter (2x^3+5)/(3x^2), x0=2 ===")
x=2
for i in range(1,4):
    x=(2*x**3+5)/(3*x**2)
    print(f"x{i}={x:.6f}")
# expect solution x3 to 3dp
x=2
xs=[]
for i in range(1,4):
    x=(2*x**3+5)/(3*x**2); xs.append(x)
print("x1,x2,x3 =", [round(v,4) for v in xs], "sol x3~", round(xs[2],3))

print("\n=== GOLD[0] misconception missing coeff (x^3+5)/(3x^2) x0=2 -> x3 ===")
x=2
for i in range(1,4):
    x=(x**3+5)/(3*x**2)
print("expect(1.119)=", round(x,3))

print("\n=== GOLD[3] 5-1/x^2 x0=2 ===")
x=2
for i in range(1,4):
    x=5-1/x**2
    print(f"x{i}={x:.6f} -> 4dp {round(x,4)}")

print("\n=== GOLD teach (2x^3+20)/(3x^2) x0=3 x2 ===")
x=3.0
x1=(2*x**3+20)/(3*x**2); print("x1=",x1, "4dp", round(x1,4))
x1r=round(x1,4)
x2=(2*x1r**3+20)/(3*x1r**2); print("x2 using 2.7407=",x2,"3dp",round(x2,3))
print("num=",2*x1r**3+20,"den=",3*x1r**2)
print("check 2.715^3=",2.715**3, "2dp",round(2.715**3,2))

print("\n=== SILVER[0] sqrt(3x+7) x0=2 x2 ===")
x=2
x1=math.sqrt(3*x+7); print("x1=",x1)
inside=3*x1+7; print("inside=",inside)
x2=math.sqrt(inside); print("x2=",x2,"2dp",round(x2,2))
print("check 4.22^2=",4.22**2,"2dp",round(4.22**2,2))

print("\n=== SILVER[2] (x^3+1)/4 x0=1 x3 ===")
x=1
for i in range(1,4):
    x=(x**3+1)/4; print(f"x{i}={x} ")
print("x3 3dp", round(x,3))

print("\n=== SILVER[4] 10/(x+1) x0=3 x2 ===")
x=3
x1=10/(x+1); x2=10/(x1+1); print("x1=",x1,"x2=",x2,"2dp",round(x2,2))
print("check 2.86*3.5=",2.86*3.5)

print("\n=== SILVER[6] cbrt(8x-3) x0=1 x1 ===")
v=8*1-3; print("inside",v,"cbrt",v**(1/3),"3dp",round(v**(1/3),3))
print("check 1.71^3=",1.71**3,"2dp",round(1.71**3,2))

print("\n=== tier gold ex (2x^3+7)/(3x^2) x0=2 ===")
x=2
x1=(2*x**3+7)/(3*x**2); x2=(2*x1**3+7)/(3*x1**2)
print("x1=",round(x1,3),"x2=",round(x2,3), "cbrt7=",7**(1/3))

print("\n=== tier silver ex sqrt(4x+5) x0=1 x2 ===")
x=1; x1=math.sqrt(4*x+5); x2=math.sqrt(4*x1+5)
print("x1=",x1,"inside",4*x1+5,"x2=",x2,"2dp",round(x2,2))

print("\n=== method_card ex sqrt(5x+3) x0=4 ===")
x=4
for i in range(1,4):
    x=math.sqrt(5*x+3); print(f"x{i}={x:.4f}")

print("\n=== trapezium gold[2] ===")
h=[0,1,4,9,16]
area=0.5*1*(h[0]+h[4]+2*(h[1]+h[2]+h[3]))
print("area=",area, "forgot double=",0.5*1*(h[0]+h[4]+(h[1]+h[2]+h[3])))
