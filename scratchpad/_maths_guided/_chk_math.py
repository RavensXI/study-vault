import math
pi=math.pi
def r1(x): return round(x,1)
checks=[]
# GOLD
checks.append(("G1 track",2*100+pi*60,388, round(2*100+pi*60)))
checks.append(("G2 sector135",0.375*64*pi,75.4,r1(0.375*64*pi)))
checks.append(("G3 area200->C", 2*pi*math.sqrt(200/pi),50.1,r1(2*pi*math.sqrt(200/pi))))
checks.append(("G4 arc12r9->ang",12/(2*pi*9)*360,76,round(12/(2*pi*9)*360)))
checks.append(("G5 annulus",64*pi,201.1,r1(64*pi)))
# BRONZE
checks.append(("B1 rect9x5",9*5,45,9*5))
checks.append(("B2 perim12,7",2*(12+7),38,2*(12+7)))
checks.append(("B3 tri10,6",0.5*10*6,30,0.5*10*6))
checks.append(("B4 para8,5",8*5,40,8*5))
checks.append(("B5 circ d14",14*pi,44.0,r1(14*pi)))
checks.append(("B6 area r5",25*pi,78.5,r1(25*pi)))
checks.append(("B7 trap5,9,6",0.5*(5+9)*6,42,0.5*(5+9)*6))
checks.append(("B8 sq perim48 area",(48/4)**2,144,(48/4)**2))
# SILVER
checks.append(("S1 area d18",81*pi,254.5,r1(81*pi)))
checks.append(("S2 C31.4 r pi3.14",31.4/(2*3.14),5.0,r1(31.4/(2*3.14))))
checks.append(("S3 Lshape",8*4+3*5,47,8*4+3*5))
checks.append(("S4 qcircle r10",pi*100/4,78.5,r1(pi*100/4)))
checks.append(("S5 trap area60 h",60/(0.5*(8+12)),6,60/(0.5*(8+12))))
checks.append(("S6 semicirc r7 perim",pi*7+14,36.0,r1(pi*7+14)))
checks.append(("S7 area50.3 r",math.sqrt(50.3/pi),4.0,r1(math.sqrt(50.3/pi))))
for name,raw,stored,comp in checks:
    ok = abs(comp-stored)<1e-6
    print(("OK " if ok else "MISMATCH ")+f"{name}: raw={raw:.4f} computed={comp} stored={stored}")
