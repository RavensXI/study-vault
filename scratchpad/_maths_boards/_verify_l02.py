# -*- coding: utf-8 -*-
# Fresh-solve every problem in ratio-proportion-L02
def r2(x): return round(x+1e-12, 2)

print("BRONZE")
print(" 0:", 0.25*80, "==20")
print(" 1:", 0.10*350, "==35")
print(" 2:", 60*1.2, "==72")
print(" 3:", 200*0.85, "==170")
print(" 4:", 1+0.30, "==1.3")
print(" 5:", 1-0.05, "==0.95")
print(" 6:", 40*0.9, "==36")
print(" 7:", 0.5*84, "==42")

print("SILVER")
print(" 0 simple int:", 2000*0.05*3, "==300")
print(" 1 house:", 200000*1.1**2, "==242000")
print(" 2 reverse:", 96/1.2, "==80")
print(" 3 pct dec:", (15000-9600)/15000*100, "==36")
print(" 4 pop:", 5000*1.02**3, "->", round(5000*1.02**3), "==5306")
print(" 5 VAT:", 84/1.2, "==70")
print(" 6 laptop:", 800*0.75**2, "==450")

print("GOLD")
print(" 0 reverse:", 340/0.85, "==400")
print(" 1 first exceed 9000 @4%:")
v=8000
for n in range(1,6):
    v=8000*1.04**n
    print("     yr",n,"=",round(v,2), ">9000?" , v>9000)
print(" 2 pop 8% dec 5yr:", 12000*0.92**5, "->", round(12000*0.92**5))
print(" 3 +10% then -10% final=?:  orig 500 ->", 500*1.1*0.9)
print(" 4 3.5% 6000 4yr interest:", r2(6000*1.035**4-6000), "total", 6000*1.035**4)
