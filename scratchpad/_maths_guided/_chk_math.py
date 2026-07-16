import json, math
live=json.load(open("_CHK_live_geomL02.json",encoding="utf-8"))
pi=math.pi
def r1(x): return round(x,1)
issues=[]
# ---- fresh solve bank ----
sols={}
# gold
def chk(path,got,exp,tol=0.05):
    ok = abs(got-exp)<=tol
    if not ok: issues.append(f"{path}: computed {got} vs stored {exp}")
    return ok

# G1 track
chk("gold[0]", round(200+pi*60), 388)
# G2 sector r8 135
chk("gold[1]", r1(135/360*pi*64), 75.4)
# G3 area200 -> circ
r=math.sqrt(200/pi); chk("gold[2]", r1(2*pi*r), 50.1)
# G4 arc12 r9 angle
chk("gold[3]", round(12/(2*pi*9)*360), 76)
# G5 annulus
chk("gold[4]", r1((100-36)*pi), 201.1)
# bronze
chk("bronze[0]", 9*5, 45)
chk("bronze[1]", 2*(12+7), 38)
chk("bronze[2]", 10*6/2, 30)
chk("bronze[3]", 8*5, 40)
chk("bronze[4]", r1(pi*14), 44.0)
chk("bronze[5]", r1(pi*25), 78.5)
chk("bronze[6]", (5+9)*6/2, 42)
chk("bronze[7]", (48/4)**2, 144)
# silver
chk("silver[0]", r1(pi*81), 254.5)
chk("silver[1]", r1(31.4/(2*3.14)), 5.0)
chk("silver[2]", 8*4+3*5, 47)
chk("silver[3]", r1(pi*100/4), 78.5)
chk("silver[4]", 60/((8+12)/2), 6)
chk("silver[5]", r1(pi*7+14), 36.0)
chk("silver[6]", r1(math.sqrt(50.3/pi)), 4.0)

# ---- expects (commit the error) ----
# G1 radius30
chk("gold[0].misc r30", round(200+pi*30), 294)
# G2 135/180
chk("gold[1].misc", r1(135/180*pi*64), 150.8)
# G3 skip sqrt
chk("gold[2].misc", r1(2*pi*(200/pi)), 400.0)
# G4 omit 2
chk("gold[3].misc", round(12*360/(pi*9)), 153)
# G5 subtract radii first
chk("gold[4].misc", r1(pi*(10-6)**2), 50.3)
# B1 perimeter
chk("bronze[0].misc", 2*(9+5), 28)
# B2 no double
chk("bronze[1].misc", 12+7, 19)
# B3 no half
chk("bronze[2].misc", 10*6, 60)
# B4 half
chk("bronze[3].misc", 8*5/2, 20)
# B5 radius7
chk("bronze[4].misc", r1(pi*7), 22.0)
# B6 no square
chk("bronze[5].misc", r1(pi*5), 15.7)
# B7 no half
chk("bronze[6].misc", (5+9)*6, 84)
# B8a perim as area
chk("bronze[7].misc0", 48, 48)
# B8b square perim
chk("bronze[7].misc1", 48**2, 2304)
# S1 diameter as radius
chk("silver[0].misc", r1(pi*18**2), 1017.9)
# S2 divide by pi only
chk("silver[1].misc", r1(31.4/3.14), 10.0)
# S3 null -> skip
# S4 full circle
chk("silver[3].misc", r1(pi*100), 314.2)
# S5 omit half
chk("silver[4].misc", 60/(8+12), 3.0)
# S6 only curved
chk("silver[5].misc", r1(pi*7), 22.0)
# S7 stop at r^2
chk("silver[6].misc", r1(50.3/pi), 16.0)

# ---- teach walks ----
chk("teach.bronze b1",7+11,18); chk("teach.bronze b2",18*4,72); chk("teach.bronze b3",72/2,36); chk("teach.bronze b4",36*2,72)
chk("teach.silver b1",20/2,10); chk("teach.silver b2",10**2,100); chk("teach.silver b3",r1(100*pi),314.2); chk("teach.silver b4",10*2,20)
chk("teach.gold b1",45/360,0.125,0.001); chk("teach.gold b2",8**2,64); chk("teach.gold b3",0.125*64,8); chk("teach.gold b4",r1(8*pi),25.1); chk("teach.gold b5",0.125*360,45)
# opener
chk("opener b1",4*3,12); chk("opener b2",4+3+4+3,14)
# tier_guide examples
chk("tg.gold",r1(0.375*64*pi),75.4); chk("tg.bronze",0.5*12*8,48); chk("tg.silver",r1(pi*81),254.5)
# method_card example
chk("mc.example",0.5*(6+10)*4,32)
# worked_examples
chk("we0",0.5*12*8,48); chk("we1",r1(pi*49),153.9); chk("we2",r1(5*pi+10),25.7)

print("ISSUES:", len(issues))
for i in issues: print(" ", i)
