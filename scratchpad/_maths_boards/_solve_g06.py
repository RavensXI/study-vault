# -*- coding: utf-8 -*-
import math

def r1(x): return round(x, 1)

print("=== BRONZE ===")
print("b0 area 8,6,inc90:", r1(0.5*8*6*math.sin(math.radians(90))), "stored 24")
print("b1 area 10,12,inc30:", r1(0.5*10*12*math.sin(math.radians(30))), "stored 30")
print("b2 area 5,8,inc60:", r1(0.5*5*8*math.sin(math.radians(60))), "stored 17.3")
print("b3 cos a: b5 c7 A90:", r1(math.sqrt(5**2+7**2-2*5*7*math.cos(math.radians(90)))), "stored 8.6")
print("b5 area 9,9,45:", r1(0.5*9*9*math.sin(math.radians(45))), "stored 28.6")
print("b6 cosC a6 b8 c10:", r1(math.degrees(math.acos((6**2+8**2-10**2)/(2*6*8)))), "stored 90")
print("b7 a/sinA a10 A30:", r1(10/math.sin(math.radians(30))), "stored 20")

print("=== SILVER ===")
print("s0 cos a: b8 c11 A55:", r1(math.sqrt(8**2+11**2-2*8*11*math.cos(math.radians(55)))), "stored 9.1")
print("s1 sine b: a15 A65 B42:", r1(15*math.sin(math.radians(42))/math.sin(math.radians(65))), "stored 11.1")
print("s2 cos largest angle 7,9,12 (opp 12):", r1(math.degrees(math.acos((7**2+9**2-12**2)/(2*7*9)))), "stored 99.6")
print("s3 area 13,17,inc72:", r1(0.5*13*17*math.sin(math.radians(72))), "stored 105.1")
print("s4 sine B: a9 A40 b12:", r1(math.degrees(math.asin(12*math.sin(math.radians(40))/9))), "stored 58.8")
print("s5 cos c: a5 b6 C100:", r1(math.sqrt(5**2+6**2-2*5*6*math.cos(math.radians(100)))), "stored 8.5")
print("s6 area heron 5,6,7:")
s=(5+6+7)/2; print("   ", r1(math.sqrt(s*(s-5)*(s-6)*(s-7))), "stored 14.7")

print("=== GOLD ===")
print("g0 inc angle area40 s10,12:", r1(math.degrees(math.asin(40/(0.5*10*12)))), "stored 41.8")
print("g1 cosC a8 b9 c13:", r1(math.degrees(math.acos((8**2+9**2-13**2)/(2*8*9)))), "stored 107.1")
print("g2 ambiguous B: a10 b7 A100:", r1(math.degrees(math.asin(7*math.sin(math.radians(100))/10))), "stored 43.5")
s=(8+11+15)/2; print("g3 heron 8,11,15:", r1(math.sqrt(s*(s-8)*(s-11)*(s-15))), "stored 36.9")
print("g4 parallelogram 8,12,65:", r1(8*12*math.sin(math.radians(65))), "stored 87")
