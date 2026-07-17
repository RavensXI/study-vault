import math
def r3(x): return round(x,3)
def cbrt(x): return math.copysign(abs(x)**(1/3), x)

print("== gold[1] misconception check ==")
correct = 1.5**3 + 2*1.5 - 7
print("correct f(1.5) =", correct, "(stored -0.625)")
err = 1.5**3 - 7
print("drop-linear error yields =", err, " stored expect = -4.625")

print("\n== spot-check solutions ==")
print("gold0 cbrt(18)=", r3(cbrt(18)), "stored 2.621")
print("gold4 cbrt(13)=", r3(cbrt(13)), "stored 2.351")
print("gold3 x1=sqrt10=", r3(math.sqrt(10)),"x2=", r3(math.sqrt(3*math.sqrt(10)+1)),"stored 3.238; rounded x1:", r3(math.sqrt(3*3.162+1)))
print("gold2 P10=",5000*1.03**10, "->",round(5000*1.03**10),"rate", round((round(5000*1.03**10)-5000)/10))
print("silver3 cbrt(9)=", r3(cbrt(9)),"stored 2.08")
print("teach gold sqrt12=",r3(math.sqrt(12)),"sqrt12.928=",r3(math.sqrt(12.928)))
print("gold0 sqrt18=",r3(math.sqrt(18)),"expect 4.243; gold4 sqrt13=",r3(math.sqrt(13)),"expect 3.606")
print("silver3 sqrt9=",math.sqrt(9),"expect 3")
