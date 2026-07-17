# -*- coding: utf-8 -*-
"""Fresh-solve every problem I will ship for eduqas geometry-L06."""
import math
r = math.radians
def sin(d): return math.sin(r(d))
def cos(d): return math.cos(r(d))
def asin(x): return math.degrees(math.asin(x))
def acos(x): return math.degrees(math.acos(x))

def rnd(x, n=1): return round(x, n)

print("== BRONZE ==")
# b0 sine side A=30,a=6,B=50 -> b
b0 = 6*sin(50)/sin(30); print("b0 b=", rnd(b0), "invert=", rnd(6*sin(30)/sin(50)))
# b1 a=10,A=45,B=65 -> b
b1 = 10*sin(65)/sin(45); print("b1 b=", rnd(b1), "invert=", rnd(10*sin(45)/sin(65)))
# b2 a=8,A=40,b=10 -> B
sinB=10*sin(40)/8; b2=asin(sinB); print("b2 B=", rnd(b2), "sinB=",round(sinB,4), "invert(a sinA/b)=", rnd(asin(8*sin(40)/10)))
# b3 A=50,a=9,B=40 -> b
b3 = 9*sin(40)/sin(50); print("b3 b=", rnd(b3), "invert=", rnd(9*sin(50)/sin(40)))
# b4 area 5,8,30
b4 = 0.5*5*8*sin(30); print("b4 area=", rnd(b4), "no-half=", rnd(5*8*sin(30)))
# b5 sine side C=80,c=15,A=35 -> a
b5 = 15*sin(35)/sin(80); print("b5 a=", rnd(b5), "invert=", rnd(15*sin(80)/sin(35)))
# b6 a=7,A=35,b=9 -> B
sB=9*sin(35)/7; b6=asin(sB); print("b6 B=", rnd(b6), "sinB=",round(sB,4), "invert=", rnd(asin(7*sin(35)/9)))
# b7 area 12,7,90 (non-calc)
b7 = 0.5*12*7*sin(90); print("b7 area=", rnd(b7), "no-half=", rnd(12*7*sin(90)))

print("\n== SILVER ==")
# s0 cosine side b=7,c=10,A=60 -> a
a2=49+100-2*7*10*cos(60); s0=math.sqrt(a2); print("s0 a2=",a2,"a=", rnd(s0), "drop-term sqrt149=", rnd(math.sqrt(149)))
# s1 cosine angle a=5,b=8,c=9 -> A
cA=(64+81-25)/(2*8*9); s1=acos(cA); print("s1 cosA=",round(cA,4),"A=", rnd(s1))
# angle opposite 9 (C):
cC=(25+64-81)/(2*5*8); print("   angle opp 9 =", rnd(acos(cC)))
# s2 area 11,14,42
s2=0.5*11*14*sin(42); print("s2 area=", rnd(s2), "no-half=", rnd(11*14*sin(42)))
# s3 sides 6,8,10 largest angle (opp 10)
cC3=(36+64-100)/(2*6*8); s3=acos(cC3); print("s3 C=", rnd(s3), "cos=",cC3, "angle opp6=", rnd(acos((64+100-36)/(2*8*10))))
# s4 obtuse SAS sides 9,13 angle 110 -> third
c2=81+169-2*9*13*cos(110); s4=math.sqrt(c2); print("s4 c2=",round(c2,4),"c=", rnd(s4), "sign-err(+cos)=", rnd(math.sqrt(81+169-2*9*13*abs(cos(110)))))
# s5 area 15,20,75
s5=0.5*15*20*sin(75); print("s5 area=", rnd(s5), "no-half=", rnd(15*20*sin(75)))
# s6 cosine angle a=4,b=7,c=9 -> C
cC6=(16+49-81)/(2*4*7); s6=acos(cC6); print("s6 cosC=",round(cC6,4),"C=", rnd(s6), "sign-err(+16)=", rnd(acos(16/56)))

print("\n== GOLD ==")
# g0 ships 10@040, 15@120 angle=80
ang=120-40; d2=100+225-2*10*15*cos(ang); g0=math.sqrt(d2); print("g0 ang=",ang,"d2=",round(d2,4),"d=", rnd(g0), "pythag sqrt325=", rnd(math.sqrt(325)))
# g1 area 13,14,15 via angle between 13,14 (opp 15)
cth=(169+196-225)/(2*13*14); sth=math.sin(math.acos(cth)); g1=0.5*13*14*sth; print("g1 cos=",round(cth,4),"sin=",round(sth,4),"area=", rnd(g1), "as int=",round(g1), "halfbh 13*14/2=",0.5*13*14)
# g2 PQR PQ=8,QR=11,angle Q=100 -> PR
p2=64+121-2*8*11*cos(100); g2=math.sqrt(p2); print("g2 PR2=",round(p2,4),"PR=", rnd(g2), "sign-err(+cos)=", rnd(math.sqrt(64+121-2*8*11*abs(cos(100)))))
# g3 area=30 sides 10,8 -> angle
sC=2*30/(10*8); g3=asin(sC); print("g3 sinC=",sC,"C=", rnd(g3), "no-half(30/80)=", rnd(asin(30/80)))
# g4 parallelogram 6,10,70
g4=6*10*sin(70); print("g4 area=", rnd(g4), "with-half(triangle)=", rnd(0.5*6*10*sin(70)))

print("\n== TEACH ==")
# tb sine A=30,a=8,B=90 -> b
tb=8*sin(90)/sin(30); print("teach_bronze b=", rnd(tb))
# ts cosine a=5,b=8,C=60 -> c
tc2=25+64-2*5*8*cos(60); print("teach_silver c2=",tc2,"c=", rnd(math.sqrt(tc2)))
# tg ambiguous a=9,b=12,A=35 -> obtuse B
sBt=12*sin(35)/9; acute=asin(sBt); print("teach_gold sinB=",round(sBt,4),"acute=",rnd(acute),"obtuse=",rnd(180-acute))

print("\n== OPENER ==")
print("box1 half of 8*6 rect=48 ->",0.5*8*6)
print("box2 0.5*8*6*sin30=",0.5*8*6*sin(30))
