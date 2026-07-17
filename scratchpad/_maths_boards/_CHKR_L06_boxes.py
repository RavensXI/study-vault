import json, math
pd = json.load(open("_CHKR_L06_live.json", encoding="utf-8"))

def r(x,n): return round(x,n)
issues=[]

# Manually recompute each guided step chain's numeric answers and compare.
# I'll list expected computations keyed by path.
S=lambda d: math.sin(math.radians(d))
C=lambda d: math.cos(math.radians(d))

checks = []
# ---- teach ----
# gold: 9sin45=6.364; /7=0.9091; asin=65.4; 180-65.4=114.6
checks += [("teach.gold[1]",9*S(45),6.364,3),("teach.gold[2]",6.3640/7,0.9091,4),
 ("teach.gold[3]",math.degrees(math.asin(0.9091)),65.4,1),("teach.gold[4]",180-65.4,114.6,1)]
# bronze: .5*7*10=35; sin40=0.6428; 35*0.6428=22.5; 22.5
checks += [("teach.bronze[1]",0.5*7*10,35.0,1),("teach.bronze[2]",S(40),0.6428,4),
 ("teach.bronze[3]",35*0.6428,22.5,1),("teach.bronze[4]",22.5,22.5,1)]
# silver: 6^2+9^2=117; 2*6*9*cos55=61.9463; 117-that=55.0537; sqrt=7.4
checks += [("teach.silver[1]",36+81,117,0),("teach.silver[2]",2*6*9*C(55),61.9463,4),
 ("teach.silver[3]",117-61.9463,55.0537,4),("teach.silver[4]",math.sqrt(55.0537),7.4,1)]
# opener box1=60, box2=10
checks += [("opener[0]",60,60,0),("opener[1]",5*2,10,0)]

# ---- gold bank ----
# g0: .5*10*12=60; 40/60=0.6667; asin=41.8; check ~40
checks += [("gold[0].gs[1]",0.5*10*12,60,0),("gold[0].gs[2]",40/60,0.6667,4),
 ("gold[0].gs[3]",math.degrees(math.asin(0.6667)),41.8,1),
 ("gold[0].gs[4]",0.5*10*12*S(41.8),40,0)]
# g1: 64+81-169=-24; 2*8*9=144; -24/144=-0.1667; acos=99.6
checks += [("gold[1].gs[1]",64+81-169,-24,0),("gold[1].gs[2]",2*8*9,144,0),
 ("gold[1].gs[3]",-24/144,-0.1667,4),("gold[1].gs[4]",math.degrees(math.acos(-0.1667)),99.6,1)]
# g2: 7sin100=6.8937; /10=0.6894; asin=43.6; 100+136.4=236.4
checks += [("gold[2].gs[1]",7*S(100),6.8937,4),("gold[2].gs[2]",6.8937/10,0.6894,4),
 ("gold[2].gs[3]",math.degrees(math.asin(0.6894)),43.6,1),
 ("gold[2].gs[4]",100+(180-43.6),236.4,1)]
# g3: (34)/2=17; 17*9*6*2=1836; sqrt=42.8
checks += [("gold[3].gs[1]",(8+11+15)/2,17,0),("gold[3].gs[2]",17*9*6*2,1836,0),
 ("gold[3].gs[3]",math.sqrt(1836),42.8,1),("gold[3].gs[4]",42.8,42.8,1)]
# g4: 8*12=96; sin65=0.9063; 96*0.9063=87; 87
checks += [("gold[4].gs[1]",8*12,96,0),("gold[4].gs[2]",S(65),0.9063,4),
 ("gold[4].gs[3]",96*0.9063,87,0),("gold[4].gs[4]",87,87,0)]

# ---- bronze bank ----
checks += [("bronze[0].gs[1]",0.5*8*6,24,0),("bronze[0].gs[2]",S(90),1.0,1),
 ("bronze[0].gs[3]",24*1,24,0),("bronze[0].gs[4]",24,24,0)]
checks += [("bronze[1].gs[1]",0.5*10*12,60,0),("bronze[1].gs[2]",S(30),0.5,1),
 ("bronze[1].gs[3]",60*0.5,30,0),("bronze[1].gs[4]",30,30,0)]
checks += [("bronze[2].gs[1]",0.5*5*8,20,0),("bronze[2].gs[2]",S(60),0.866,3),
 ("bronze[2].gs[3]",20*0.866,17.3,1),("bronze[2].gs[4]",17.3,17.3,1)]
checks += [("bronze[3].gs[1]",25+49,74,0),("bronze[3].gs[2]",2*5*7*C(90),0.0,1),
 ("bronze[3].gs[3]",74-0,74,0),("bronze[3].gs[4]",math.sqrt(74),8.6,1)]
# bronze[4] MCQ no gs
checks += [("bronze[5].gs[1]",0.5*9*9,40.5,1),("bronze[5].gs[2]",S(45),0.7071,4),
 ("bronze[5].gs[3]",40.5*0.7071,28.6,1),("bronze[5].gs[4]",28.6,28.6,1)]
checks += [("bronze[6].gs[1]",36+64-100,0,0),("bronze[6].gs[2]",2*6*8,96,0),
 ("bronze[6].gs[3]",0/96,0.0,1),("bronze[6].gs[4]",math.degrees(math.acos(0)),90,0)]
checks += [("bronze[7].gs[1]",S(30),0.5,1),("bronze[7].gs[2]",10/0.5,20,0),
 ("bronze[7].gs[3]",20*0.5,10,0)]

# ---- silver bank ----
checks += [("silver[0].gs[1]",64+121,185,0),("silver[0].gs[2]",2*8*11*C(55),100.9495,4),
 ("silver[0].gs[3]",185-100.9495,84.0505,4),("silver[0].gs[4]",math.sqrt(84.0505),9.2,1)]
checks += [("silver[1].gs[1]",15*S(42),10.037,3),("silver[1].gs[2]",S(65),0.9063,4),
 ("silver[1].gs[3]",10.0370/0.9063,11.1,1),("silver[1].gs[4]",11.1*S(65)/S(42),15,0)]
checks += [("silver[2].gs[1]",49+81-144,-14,0),("silver[2].gs[2]",2*7*9,126,0),
 ("silver[2].gs[3]",-14/126,-0.1111,4),("silver[2].gs[4]",math.degrees(math.acos(-0.1111)),96.4,1)]
checks += [("silver[3].gs[1]",0.5*13*17,110.5,1),("silver[3].gs[2]",S(72),0.9511,4),
 ("silver[3].gs[3]",110.5*0.9511,105.1,1),("silver[3].gs[4]",105.1,105.1,1)]
checks += [("silver[4].gs[1]",12*S(40),7.7135,4),("silver[4].gs[2]",7.7135/9,0.8571,4),
 ("silver[4].gs[3]",math.degrees(math.asin(0.8571)),59.0,1),("silver[4].gs[4]",180-40-59.0,81,0)]
checks += [("silver[5].gs[1]",25+36,61,0),("silver[5].gs[2]",2*5*6*C(100),-10.4189,4),
 ("silver[5].gs[3]",61-(-10.4189),71.4189,4),("silver[5].gs[4]",math.sqrt(71.4189),8.5,1)]
checks += [("silver[6].gs[1]",25+36-49,12,0),("silver[6].gs[2]",2*5*6,60,0),
 ("silver[6].gs[3]",12/60,0.2,1),("silver[6].gs[4]",math.degrees(math.acos(0.2)),78.5,1),
 ("silver[6].gs[5]",0.5*5*6*S(78.5),14.7,1)]

for path, comp, stored, nd in checks:
    rc = round(comp, nd)
    if abs(rc - stored) > 10**(-nd)*0.5 + 1e-9:
        # allow tiny rounding at boundary
        if abs(comp-stored) > 0.06:
            issues.append(f"{path}: computed {comp:.5f} (->{rc}) vs stored {stored}")
print("BOX MISMATCHES:", len(issues))
for i in issues: print("  ", i)
