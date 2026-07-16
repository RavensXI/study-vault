# -*- coding: utf-8 -*-
import math
def r(x,d): return round(x,d)
out=[]
def chk(name, got, exp, tol=0.05):
    ok = abs(got-exp)<=tol
    out.append(("OK " if ok else "!!!",name,round(got,4),exp))

# GOLD bank
chk("G1 15^2",15**2,225); chk("G1 20^2",20**2,400); chk("G1 sum",625,625); chk("G1 sqrt",math.sqrt(625),25); chk("G1 sol",math.hypot(15,20),25); chk("G1 exp 15+20",35,35)
chk("G2 30/50",30/50,0.6); chk("G2 atan",math.degrees(math.atan(0.6)),31.0,0.06); chk("G2 sol",math.degrees(math.atan(30/50)),31.0,0.06); chk("G2 exp asin",math.degrees(math.asin(0.6)),36.9,0.06); chk("G2 check tan31",math.tan(math.radians(31)),0.6,0.005)
chk("G3 mid1",2,2); chk("G3 mid2",4,4); chk("G3 xterm 2-4",-2,-2); chk("G3 const 1-4",-3,-3); chk("G3 x",3,3); chk("G3 check 9+16",9+16,25); chk("G3 exp lin",1,1)
chk("G4 tan25",math.tan(math.radians(25)),0.466,0.001); chk("G4 d",40/math.tan(math.radians(25)),85.8,0.06); chk("G4 sol",40/math.tan(math.radians(25)),85.8,0.06); chk("G4 check",85.8*math.tan(math.radians(25)),40,0.5); chk("G4 exp mult",40*math.tan(math.radians(25)),18.7,0.06)
chk("G5 17^2",289,289); chk("G5 8^2",64,64); chk("G5 sub",225,225); chk("G5 sqrt",math.sqrt(225),15); chk("G5 sol",math.sqrt(17**2-8**2),15); chk("G5 check",15**2+8**2,289); chk("G5 exp add",math.hypot(17,8),18.8,0.06)

# BRONZE
chk("B1 sol",math.hypot(3,4),5); chk("B1 exp",7,7)
chk("B2 sol",math.hypot(7,24),25); chk("B2 exp",31,31)
chk("B3 sol",math.hypot(8,15),17); chk("B3 exp",23,23)
chk("B4 sol",math.sqrt(100-36),8); chk("B4 exp",math.hypot(10,6),11.7,0.06)
chk("B5 sol",math.sqrt(676-100),24); chk("B5 exp",math.hypot(26,10),27.9,0.06)
chk("B6 O",20*0.5,10); chk("B6 exp",20/0.5,40)
chk("B7 A",14*0.5,7); chk("B7 exp",14/0.5,28)
chk("B8 ratio",5/12,0.42,0.01); chk("B8 sol",math.degrees(math.atan(5/12)),22.6,0.06); chk("B8 exp",math.degrees(math.atan(12/5)),67.4,0.06); chk("B8 chk tan22.6",math.tan(math.radians(22.6)),0.42,0.005)

# SILVER
chk("S1 sol",math.sqrt(169-25),12); chk("S1 exp",math.hypot(13,5),13.9,0.06)
chk("S2 ratio",8/6,1.33,0.01); chk("S2 sol",math.degrees(math.atan(8/6)),53.1,0.06); chk("S2 exp",math.degrees(math.atan(6/8)),36.9,0.06)
chk("S3 cos40",math.cos(math.radians(40)),0.77,0.005); chk("S3 sol",12*math.cos(math.radians(40)),9.2,0.06); chk("S3 exp",12*math.sin(math.radians(40)),7.7,0.06)
chk("S4 tan35",math.tan(math.radians(35)),0.70,0.005); chk("S4 sol",10*math.tan(math.radians(35)),7.0,0.06); chk("S4 exp",10*math.sin(math.radians(35)),5.7,0.06)
chk("S5 sub",36-4,32); chk("S5 sqrt",math.sqrt(32),5.7,0.06); chk("S5 sol",math.sqrt(36-4),5.7,0.06); chk("S5 check",5.7**2+4,36,0.5); chk("S5 exp",math.hypot(6,2),6.3,0.06)
chk("S6 ratio",12/20,0.6); chk("S6 sol",math.degrees(math.asin(0.6)),36.9,0.06); chk("S6 exp",math.degrees(math.acos(0.6)),53.1,0.06)
chk("S7 half",12/2,6); chk("S7 sub",100-36,64); chk("S7 sol",math.sqrt(64),8)

# TEACH
chk("Tb 12^2",144,144); chk("Tb 16^2",256,256); chk("Tb sqrt",math.sqrt(400),20)
chk("Ts 9/12",9/12,0.75); chk("Ts atan",math.degrees(math.atan(0.75)),36.9,0.06); chk("Ts other",90-36.9,53.1,0.06); chk("Ts chk",math.tan(math.radians(36.9)),0.75,0.005)
chk("Tg ratio",1.5/8,0.19,0.005); chk("Tg atan",math.degrees(math.atan(1.5/8)),10.6,0.06); chk("Tg chk",math.tan(math.radians(10.6)),0.19,0.005); chk("Tg hyp",math.sqrt(1.5**2+8**2),8.1,0.06)

# OPENER
chk("Op sum",9+16,25); chk("Op edge",math.sqrt(25),5)

for tag,n,g,e in out:
    if tag!="OK ": print(tag,n,"got",g,"exp",e)
print("TOTAL",len(out),"checks;", sum(1 for t,*_ in out if t!="OK "),"failures")
