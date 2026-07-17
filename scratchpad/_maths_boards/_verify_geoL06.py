import math

def r1(x): return round(x,1)

print("=== GOLD ===")
# G1 ambiguous: a=10,b=7,B=40
sinA=10*math.sin(math.radians(40))/7
A1=math.degrees(math.asin(sinA)); A2=180-A1
print("G1 sinA=%.5f A1=%.3f A2=%.3f -> %.1f, %.1f (stored 66.7,113.3)"%(sinA,A1,A2,r1(A1),r1(A2)))
# G2 ship: angle 70, sides 8,6
AC=math.sqrt(64+36-96*math.cos(math.radians(70)))
print("G2 AC=%.4f -> %.1f (stored 8.2)"%(AC,r1(AC)))
# G3 area 40, PQ10 PR12 find P
P=math.degrees(math.asin(40/60))
print("G3 P=%.4f -> %.1f (stored 41.8)"%(P,r1(P)))
# G4 13,14,15 area (Heron)
s=(13+14+15)/2; ar=math.sqrt(s*(s-13)*(s-14)*(s-15))
print("G4 area=%.4f -> %.1f (stored 84)"%(ar,r1(ar)))
# G5 x9 y11 Z120 find z
z=math.sqrt(81+121-2*9*11*math.cos(math.radians(120)))
print("G5 z=%.4f -> %.1f (stored 17.3)"%(z,r1(z)))

print("=== BRONZE ===")
# B1 a: A40 B60 b12
a=12*math.sin(math.radians(40))/math.sin(math.radians(60))
print("B1 a=%.4f -> %.1f (stored 8.9)"%(a,r1(a)))
# B2 angle B: a9 b12 A35
sinB=12*math.sin(math.radians(35))/9
B=math.degrees(math.asin(sinB))
print("B2 B=%.4f -> %.1f (stored 49.5)"%(B,r1(B)))
# B3 area 6,10 inc45
ar=0.5*6*10*math.sin(math.radians(45))
print("B3 area=%.4f -> %.1f (stored 21.2)"%(ar,r1(ar)))
# B4 area 8,5 inc30
ar=0.5*8*5*math.sin(math.radians(30))
print("B4 area=%.4f -> %.1f (stored 10)"%(ar,r1(ar)))
# B5 side b: A50 B80 a7
b=7*math.sin(math.radians(80))/math.sin(math.radians(50))
print("B5 b=%.4f -> %.1f (stored 9)"%(b,r1(b)))
# B6 side c cosine: a6 b8 C90
c=math.sqrt(36+64-2*6*8*math.cos(math.radians(90)))
print("B6 c=%.4f -> %.1f (stored 10)"%(c,r1(c)))
# B7 area 12,9 inc60
ar=0.5*12*9*math.sin(math.radians(60))
print("B7 area=%.4f -> %.1f (stored 46.8)"%(ar,r1(ar)))
# B8 side a cosine: b10 c7 A50
a=math.sqrt(100+49-2*10*7*math.cos(math.radians(50)))
print("B8 a=%.4f -> %.1f (stored 7.7)"%(a,r1(a)))

print("=== SILVER ===")
# S1 angle A cosine: a8 b6 c10
A=math.degrees(math.acos((36+100-64)/(2*6*10)))
print("S1 A=%.4f -> %.1f (stored 53.1)"%(A,r1(A)))
# S2 angle C: a12 b9 c7
C=math.degrees(math.acos((144+81-49)/(2*12*9)))
print("S2 C=%.4f -> %.1f (stored 35.2)"%(C,r1(C)))
# S3 third side 11,14 inc75
c=math.sqrt(121+196-2*11*14*math.cos(math.radians(75)))
print("S3 c=%.4f -> %.1f (stored 15.4)"%(c,r1(c)))
# S4 area PQ15 PR11 P42
ar=0.5*15*11*math.sin(math.radians(42))
print("S4 area=%.4f -> %.1f (stored 55.2)"%(ar,r1(ar)))
# S5 a5 A30 B105 find b
b=5*math.sin(math.radians(105))/math.sin(math.radians(30))
print("S5 b=%.4f -> %.1f (stored 9.7)"%(b,r1(b)))
# S6 side a cosine b15 c20 A110
a=math.sqrt(225+400-2*15*20*math.cos(math.radians(110)))
print("S6 a=%.4f -> %.1f (stored 28.8)"%(a,r1(a)))
# S7 hikers 3,5 angle 60
d=math.sqrt(9+25-2*3*5*math.cos(math.radians(60)))
print("S7 d=%.4f -> %.1f (stored 4.4)"%(d,r1(d)))
