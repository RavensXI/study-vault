import math
def r3(x): return round(x,3)
# GOLD
print("G0 x1=cbrt(18):", r3(18**(1/3)), "sqrt18:", r3(18**.5))
print("G1 f(1.5)=1.5^3+2*1.5-7:", 1.5**3+2*1.5-7, "dropped_linear 1.5^3-7:", 1.5**3-7, "f1:",1+2-7,"f2:",8+4-7)
P10=5000*1.03**10
print("G2 P10:", P10, "round", round(P10), "rate:", (round(P10)-5000)/10)
x1=math.sqrt(3*3+1); x2=math.sqrt(3*x1+1)
print("G3 x1:", r3(x1), "x2:", r3(x2))
print("G4 x1=cbrt(13):", r3(13**(1/3)), "sqrt13:", r3(13**.5))
# SILVER
print("S0 10/(2+1):", 10,"/",3)
print("S1 f(2)=8-8-1:", 8-8-1)
print("S2 f(3)=27-12-1:", 27-12-1, "sq_not_cube 9-12-1:", 9-12-1)
print("S3 cbrt(9):", r3(9**(1/3)))
print("S4 y=x^3 (8-1)/1:", (8-1)/1, "cubed_wrong (6-1)/1:", (6-1)/1)
print("S5 f(0)=0-0+1:", 0-0+1)
print("S6 f(1)=1-4+1:", 1-4+1, "added_middle 1+4+1:", 1+4+1)
# BRONZE
print("B0 (9-1)/2:", (9-1)/2)
print("B1 (16-1)/5:", (16-1)/5)
print("B2 4-7:", 4-7, "sign_flip 7-4:", 7-4)
print("B3 9-7:", 9-7, "sign_flip 7-9:", 7-9)
print("B4 2+3:", 2+3, "mult 2*3:", 2*3)
print("B5 5+3:", 5+3)
print("B6 (16-4)/2:", (16-4)/2)
# teach
print("teach gold x1=sqrt12:", r3(math.sqrt(12)), "x2=sqrt(2*3.464+6):", r3(math.sqrt(2*3.464+6)), "fullprec:", r3(math.sqrt(2*math.sqrt(12)+6)))
print("teach bronze (16-1)/3:", (16-1)/3)
print("teach silver f2:",8-4-5,"f3:",27-6-5)
