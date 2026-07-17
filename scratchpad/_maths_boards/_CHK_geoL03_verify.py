import math
pi=math.pi
def r1(x): return round(x,1)
def rn(x): return round(x)
def r2(x): return round(x,2)
out=[]
def chk(label,got,exp,tol=0.06):
    ok = abs(got-exp)<=tol
    out.append((("OK " if ok else "FAIL"),label,f"got={got}",f"exp={exp}"))

# GOLD
# g0 cone V150 h12 find r
chk("g0 r", math.sqrt(150/(4*pi)), 3.5, 0.05)
chk("g0 box 1/3*12",12/3,4)
chk("g0 box 150/(4pi)",150/(4*pi),11.94,0.01)
chk("g0 box sqrt11.94",math.sqrt(11.94),3.5,0.05)
chk("g0 check 1/3*pi*11.94*12",(1/3)*pi*11.94*12,150,0.2)
chk("g0 misc no_third r",math.sqrt(150/(12*pi)),2.0,0.05)
# g1 sphere V904.8 find r
chk("g1 box *3",904.8*3,2714.4)
chk("g1 box /(4pi)",2714.4/(4*pi),216,0.5)
chk("g1 cbrt216",216**(1/3),6,0.01)
chk("g1 check 4/3 pi 216",(4/3)*pi*216,904.8,0.1)
# g2 ratio
chk("g2 cyl 3^2*9",9*9,81)
chk("g2 cone 1/3*81",81/3,27)
chk("g2 ratio",81/27,3)
chk("g2 misc wrong_way",27/81,0.3,0.04)   # 0.333 vs 0.3
# g3 frustum
big=(1/3)*pi*36*12; small=(1/3)*pi*9*6
chk("g3 big 1/3*432",432/3,144)
chk("g3 small 1/3*54",54/3,18)
chk("g3 frustum 126pi",126*pi,396,0.5)
chk("g3 misc kept_radius",big-(1/3)*pi*36*6,226.2,0.1)
chk("g3 misc forgot_subtract",big,452.4,0.1)
# g4 sphere in cylinder
chk("g4 cyl 250pi",250*pi,785.4,0.1)
chk("g4 sphere 500pi/3",500*pi/3,523.6,0.1)
chk("g4 empty",250*pi-500*pi/3,261.8,0.1)
chk("g4 empty 250pi/3",250*pi/3,261.8,0.1)

# BRONZE
chk("b0 V",6*4*3,72)
chk("b0 SA",2*(24+18+12),108)
chk("b1 V",5**3,125); chk("b1 SA",6*25,150)
chk("b2 SA",6*16,96); chk("b2 V",4**3,64)
chk("b3 V",15*8,120); chk("b3 added",15+8,23)
chk("b4 V",0.5*6*4*7,84); chk("b4 forgot_half",6*4*7,168)
chk("b5 SA",2*(15+10+6),62); chk("b5 half",15+10+6,31); chk("b5 V",5*3*2,30)
chk("b6 h",180/60,3); chk("b6 one_dim",180/10,18)
chk("b7 V",20*pi,63,0.5); chk("b7 no_square",10*pi,31,0.5)

# SILVER
chk("s0 V",300*pi,942.5,0.1); chk("s0 no_square",60*pi,188.5,0.1)
chk("s1 SA",78*pi,245.0,0.1); chk("s1 forgot_ends",60*pi,188.5,0.1)
chk("s2 V",48*pi,150.8,0.1); chk("s2 no_third",144*pi,452.4,0.1)
chk("s3 V",36*pi,113.1,0.1); chk("s3 squared_radius",12*pi,37.7,0.1)
chk("s4 V hemi",250*pi/3,261.8,0.1); chk("s4 full",500*pi/3,523.6,0.1)
chk("s5 SA",64*pi,201.1,0.1); chk("s5 gave_volume",(4/3)*pi*64,268.1,0.1)

# TEACH
chk("teach gold cyl 96pi",96*pi,301.6,0.1)
chk("teach gold cone 32pi",32*pi,100.5,0.1)
chk("teach gold add",301.6+100.5,402.1,0.05)
chk("teach gold 96+32",128,128)
chk("teach gold 128pi",128*pi,402.1,0.1)
chk("teach silver cone 18pi",18*pi,56.5,0.1)
# OPENER
chk("opener 4*2",8,8); chk("opener 8*3",24,24); chk("opener 4*2*3",24,24)
# tier examples
chk("tg gold hemi 18pi",18*pi,56.5,0.1)
chk("tg silver cone 12pi",12*pi,37.7,0.1)
chk("tg bronze cuboid",4*3*5,60)
# method card
chk("mc cyl 160pi",160*pi,502.7,0.1)
# worked examples
chk("we1 63pi",63*pi,197.9,0.1)
chk("we2 288pi",288*pi,904.8,0.1)

fails=[o for o in out if o[0]=="FAIL"]
for o in out:
    if o[0]=="FAIL": print(o)
print("TOTAL",len(out),"FAILS",len(fails))
