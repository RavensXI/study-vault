import json, math
pd=json.load(open("_live_L06_fetched.json",encoding="utf-8"))
def r(x,n=1): return round(x,n)
errs=[]
def chk(name, got, exp, tol=0.05):
    if abs(got-exp)>tol:
        errs.append(f"{name}: computed {got:.4f} vs stored {exp}")

# ---- GOLD ----
g=pd["problem_bank"]["gold"]
# G1 a=10 b=7 B=40
sinA=10*math.sin(math.radians(40))/7
A1=math.degrees(math.asin(sinA)); 
chk("G1 sol0",r(A1),g[0]["solutions"][0]); chk("G1 sol1",r(180-A1),g[0]["solutions"][1])
chk("G1 box 10sin40",10*math.sin(math.radians(40)),6.4279,0.0002)
chk("G1 box /7",6.4279/7,0.9183,0.0002)
chk("G1 asin",math.degrees(math.asin(0.9183)),66.7,0.06)
# G2 ship
ang=220-150; chk("G2 interior",ang,70)
AC2=64+36-96*math.cos(math.radians(70)); chk("G2 AC2",AC2,67.1661,0.001); chk("G2 AC",r(math.sqrt(AC2)),8.2)
chk("G2 term",96*math.cos(math.radians(70)),32.8339,0.001)
# G2 misc expect 11.5 uses 110
chk("G2 misc",r(math.sqrt(100-96*math.cos(math.radians(110)))),11.5)
# G3 area40 PQ10 PR12
sinP=40/60; P=math.degrees(math.asin(sinP)); chk("G3 sol",r(P),41.8)
chk("G3 misc no_half",r(math.degrees(math.asin(40/120))),19.5)
# G4 13,14,15
cosA=(196+225-169)/420; A=math.degrees(math.acos(cosA)); area=0.5*14*15*math.sin(math.radians(A))
chk("G4 cosA",cosA,0.6,0.001); chk("G4 area",area,84,0.1)
# G5 x9 y11 Z120
z2=81+121-2*9*11*math.cos(math.radians(120)); chk("G5 z2",z2,301,0.01); chk("G5 z",r(math.sqrt(z2)),17.3)
chk("G5 misc",r(math.sqrt(202-99)),10.1)

# ---- BRONZE ----
b=pd["problem_bank"]["bronze"]
# B1 A40 B60 b12 find a
a=12*math.sin(math.radians(40))/math.sin(math.radians(60)); chk("B1 a",r(a),8.9)
chk("B1 misc inv",r(12*math.sin(math.radians(60))/math.sin(math.radians(40))),16.2)
# B2 a12 b9 A35 find B
sB=9*math.sin(math.radians(35))/12; B=math.degrees(math.asin(sB)); chk("B2 B",r(B),25.5)
chk("B2 third",180-35-r(B),119.5)
chk("B2 misc swap",r(math.degrees(math.asin(12*math.sin(math.radians(35))/9))),49.9)
# B3 area 6,10,45
chk("B3 area",0.5*6*10*math.sin(math.radians(45)),21.2,0.05); chk("B3 misc",r(6*10*math.sin(math.radians(45))),42.4)
# B4 area 8,6,30
chk("B4 area",0.5*8*6*math.sin(math.radians(30)),12,0.01); chk("B4 misc",r(8*6*math.sin(math.radians(30))),24)
# B5 A50 B80 a7 find b
bb=7*math.sin(math.radians(80))/math.sin(math.radians(50)); chk("B5 b",r(bb),9)
chk("B5 misc",r(7*math.sin(math.radians(50))/math.sin(math.radians(80))),5.4)
# B6 a6 b8 C90 find c
c=math.sqrt(36+64-2*6*8*math.cos(math.radians(90))); chk("B6 c",r(c),10)
# B7 area 12,9,60
chk("B7 area",0.5*12*9*math.sin(math.radians(60)),46.8,0.05); chk("B7 misc",r(12*9*math.sin(math.radians(60))),93.5)
# B8 b10 c7 A50 find a
a8=math.sqrt(100+49-2*10*7*math.cos(math.radians(50))); chk("B8 a",r(a8),7.7)
chk("B8 term",2*10*7*math.cos(math.radians(50)),89.9903,0.001)
chk("B8 misc add",r(math.sqrt(149+2*70*math.cos(math.radians(50)))),15.5)

# ---- SILVER ----
s=pd["problem_bank"]["silver"]
# S1 a8 b6 c10 find A
cA=(36+100-64)/120; chk("S1 A",r(math.degrees(math.acos(cA))),53.1); chk("S1 misc",r(math.degrees(math.acos(-0.6))),126.9)
# S2 a12 b9 c7 find C
cC=(144+81-49)/216; chk("S2 cosC",cC,0.8148,0.0002); chk("S2 C",r(math.degrees(math.acos(cC))),35.4)
chk("S2 misc",r(math.degrees(math.acos(-0.8148))),144.6)
# S3 11,14,75 third
c3=math.sqrt(121+196-2*11*14*math.cos(math.radians(75))); chk("S3 c",r(c3),15.4)
chk("S3 term",2*11*14*math.cos(math.radians(75)),79.7163,0.001)
chk("S3 misc",r(math.sqrt(317+2*11*14*math.cos(math.radians(75)))),19.9)
# S4 PQR 15,11,42
chk("S4 area",0.5*15*11*math.sin(math.radians(42)),55.2,0.05); chk("S4 misc",r(15*11*math.sin(math.radians(42))),110.4)
# S5 a5 A30 B105 find b
b5=5*math.sin(math.radians(105))/math.sin(math.radians(30)); chk("S5 b",r(b5),9.7); chk("S5 misc",r(5*math.sin(math.radians(30))/math.sin(math.radians(105))),2.6)
# S6 b15 c20 A110 find a
a6=math.sqrt(225+400-2*15*20*math.cos(math.radians(110))); chk("S6 a",r(a6),28.8)
chk("S6 term",2*15*20*math.cos(math.radians(110)),-205.2121,0.001)
chk("S6 misc",r(math.sqrt(625-2*15*20*math.cos(math.radians(110))*-1 if False else 625+2*15*20*math.cos(math.radians(110)))),20.5)
# S7 hikers 3,5 bearings 60,120
d=math.sqrt(9+25-2*3*5*math.cos(math.radians(60))); chk("S7 d",r(d),4.4); chk("S7 misc",r(math.sqrt(34+15)),7)

# tier guides
chk("TG gold ex",math.degrees(math.asin(48/96)),30,0.05)
chk("TG bronze ex",8*math.sin(math.radians(30))/math.sin(math.radians(90)),4,0.01)
chk("TG silver ex",math.degrees(math.acos((25+36-49)/60)),78.5,0.06)
# method card
chk("MC ex",8*math.sin(math.radians(50))/math.sin(math.radians(70)),6.5,0.05)
# worked examples
chk("WE1",math.degrees(math.asin(10*0.5/7)),45.6,0.06)
chk("WE2",math.sqrt(25+64-40),7,0.01)

print("ERRORS:" if errs else "ALL NUMERIC CHECKS PASS")
for e in errs: print(" -",e)
