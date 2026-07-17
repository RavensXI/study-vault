import math
P=math.pi
r=lambda x,n=1:round(x,n)
res=[]
def ck(name,got,exp):
    ok=abs(got-exp)<0.05
    res.append(f"{'OK ' if ok else 'XX '}{name}: got {got:.4f} exp {exp}")
# solutions
ck("b0 rect7x5",7*5,35); ck("b1 peri9x4",2*(9+4),26); ck("b2 tri12x8",0.5*12*8,48)
ck("b3 para10x6",10*6,60); ck("b4 sq P36",(36/4)**2,81); ck("b5 tri14x6",0.5*14*6,42)
ck("b6 w=48/8",48/8,6); ck("b7 equi 3x9",3*9,27)
ck("s0 C=2*3.14*7",2*3.14*7,43.96); ck("s1 A d10",P*25,78.5); ck("s2 trap",0.5*16*4,32)
ck("s3 arc r10 72",(72/360)*2*P*10,12.6); ck("s4 sec r6 120",(120/360)*P*36,37.7)
ck("s5 semi d14",0.5*P*49,77.0); ck("s6 semiPeri r5",P*5+10,25.7)
ck("g0 rect-quarter",60-0.25*P*36,31.7); ck("g1 r from154",math.sqrt(154/P),7.0)
ck("g2 angle",24*360/144,60); ck("g3 track",200+P*60,388)
ck("g4 annulus",P*100-P*36,201.1)
# expects
ck("g0 added",60+0.25*P*36,88.3); ck("g0 semicirc",60-0.5*P*36,3.5)
ck("g1 forgotroot",154/P,49.0); ck("g1 usedcirc",154/(2*P),24.5)
ck("g2 forgotsq",24*360/12,720); ck("g2 usedarc",360,360)
ck("g3 straightonly",200,200); ck("g3 usedradius",2*P*60+200,577)
ck("g4 subradii",P*16,50.3); ck("g4 forgotsub",P*100,314.2)
ck("s0 area misc",3.14*49,153.86); ck("s0 diam misc",3.14*7,21.98)
ck("s1 useddiam",P*100,314.2); ck("s1 circ",2*P*5,31.4)
ck("s3 fullcirc",2*P*10,62.8); ck("s3 fracinv",(360/72)*2*P*10,314.2)
ck("s4 fullcirc",P*36,113.1); ck("s4 arcnotarea",(120/360)*2*P*6,12.6)
ck("s5 fullcirc",P*49,153.9); ck("s5 useddiam",0.5*P*196,307.9)
ck("s6 arconly",P*5,15.7); ck("s6 fullcirc",2*P*5+10,41.4)
open("_final_out.txt","w").write("\n".join(res))
print("\n".join(res))
