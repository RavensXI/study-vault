import math

def sin(d): return math.sin(math.radians(d))
def cos(d): return math.cos(math.radians(d))
def asin(x): return math.degrees(math.asin(x))
def acos(x): return math.degrees(math.acos(x))

def r(x,n=1): return round(x,n)

print("=== TEACH ===")
# gold teach: a=9,b=6,B=35, find A both
t=9*sin(35); print("gold t1 9sin35=",round(t,4), "exp 5.1622")
print("gold t2 /6=",round(t/6,4),"exp 0.8604")
A=asin(t/6); print("gold t3 asin=",round(A,1),"exp 59.4")
print("gold t4 180-=",round(180-round(A,1),1),"exp 120.6")
# bronze teach A=40,B=75,b=13 find a
print("bronze t1 13sin40=",round(13*sin(40),4),"exp 8.3562")
print("bronze t2 sin75=",round(sin(75),4),"exp 0.9659")
print("bronze t3 a=",round(8.3562/0.9659,1),"exp 8.7")
print("bronze t4 check 8.7sin75/sin40=",round(8.7*sin(75)/sin(40)),"exp 13")
# silver teach sides7,9 incl50
print("silver t1 49+81=",130)
print("silver t2 2*7*9cos50=",round(2*7*9*cos(50),4),"exp 80.9912")
print("silver t3 130-=",round(130-80.9912,4),"exp 49.0088")
print("silver t4 sqrt=",round(math.sqrt(49.0088),1),"exp 7.0")

print("\n=== OPENER ===")
print("box1 bigger angle 60; box2 5*2=10")

print("\n=== GOLD BANK ===")
# g0 a=10,b=7,B=40
s=10*sin(40); print("g0 10sin40=",round(s,4),"exp 6.4279")
print("g0 /7=",round(s/7,4),"exp 0.9183")
A=asin(s/7); print("g0 asinA=",round(A,1),"exp 66.7","; 180-=",round(180-round(A,1),1),"exp 113.3")
print("g0 misc acute only expect 66.7 both")
# g1 ship 8@040 then6@150
print("g1 interior 220-150=",70)
print("g1 8^2+6^2=",100)
print("g1 2*8*6cos70=",round(2*8*6*cos(70),4),"exp 32.8339")
print("g1 100-=",round(100-32.8339,4),"exp 67.1661")
print("g1 sqrt=",round(math.sqrt(67.1661),1),"exp 8.2")
print("g1 misc wrong angle 110: sqrt(100-96cos110)=",round(math.sqrt(100-96*cos(110)),1),"exp 11.5")
# g2 area40 PQ10 PR12 find P
print("g2 half prod=",60)
print("g2 40/60=",round(40/60,4),"exp 0.6667")
print("g2 asin=",round(asin(40/60),1),"exp 41.8")
print("g2 check half*sin41.8=",round(60*sin(41.8)),"exp 40")
print("g2 misc no half asin(40/120)=",round(asin(40/120),1),"exp 19.5")
# g3 13,14,15 area
print("g3 top 196+225-169=",196+225-169,"exp 252")
print("g3 bottom 2*14*15=",420)
print("g3 cosA=252/420=",round(252/420,4),"exp 0.6")
print("g3 acos0.6=",round(acos(0.6),1),"exp 53.1")
print("g3 area .5*14*15*sin53.1=",round(0.5*14*15*sin(53.1),1),"exp 84")
print("g3 heron:",math.sqrt(21*8*7*6))
print("g3 misc assume right .5*13*14=",0.5*13*14,"exp 91")
# g4 x9 y11 Z120 find z
print("g4 81+121=",202)
print("g4 2*9*11cos120=",round(2*9*11*cos(120),4),"exp -99")
print("g4 202-(-99)=",301)
print("g4 sqrt301=",round(math.sqrt(301),1),"exp 17.3")
print("g4 misc sign +0.5: sqrt(202-99)=",round(math.sqrt(202-99),1),"exp 10.1")

print("\n=== BRONZE BANK ===")
# b0 A40 B60 b12 find a
print("b0 12sin40=",round(12*sin(40),4),"exp 7.7135","; sin60=",round(sin(60),4),"exp 0.866")
print("b0 a=",round(12*sin(40)/sin(60),1),"exp 8.9")
print("b0 misc inv 12sin60/sin40=",round(12*sin(60)/sin(40),1),"exp 16.2")
# b1 a9 b12 A35 find B  -- AMBIGUOUS CHECK
print("b1 12sin35=",round(12*sin(35),4),"exp 6.8829","; /9=",round(12*sin(35)/9,4),"exp 0.7648")
B=asin(12*sin(35)/9); print("b1 asinB=",round(B,1),"exp 49.9","; other=",round(180-B,1))
print("b1 AMBIG check b>a? b=12>a=9; b sinA=",round(12*sin(35),3),"< a=9 so TWO triangles. Other B=",round(180-B,1),"valid? A+B2=",35+round(180-B,1))
print("b1 misc swapped 9sin35/12 -> asin=",round(asin(9*sin(35)/12),1),"exp 25.5")
# b2 area 6,10,45
print("b2 half=30 sin45=",round(sin(45),4),"->",round(30*sin(45),1),"exp 21.2; misc no half 60sin45=",round(60*sin(45),1),"exp 42.4")
# b3 area 8,6,30
print("b3 half=24 sin30=0.5 ->12; misc 48*0.5=24")
# b4 A50 B80 a7 find b
print("b4 7sin80=",round(7*sin(80),4),"exp 6.8937; sin50=",round(sin(50),4),"exp 0.766")
print("b4 b=",round(7*sin(80)/sin(50),1),"exp 9; misc inv 7sin50/sin80=",round(7*sin(50)/sin(80),1),"exp 5.4")
# b5 cos c a6 b8 C90
print("b5 100 - 2*6*8cos90=",round(2*6*8*cos(90),4),"-> c=",round(math.sqrt(100-0),1),"exp 10; misc no sqrt 100")
# b6 area 12,9,60
print("b6 half=54 sin60=0.866 ->",round(54*sin(60),1),"exp 46.8; misc 108sin60=",round(108*sin(60),1),"exp 93.5")
# b7 cos a b10 c7 A50
print("b7 100+49=149; 2*10*7cos50=",round(2*10*7*cos(50),4),"exp 89.9903; a=",round(math.sqrt(149-89.9903),1),"exp 7.7")
print("b7 misc sign add sqrt(149+89.99)=",round(math.sqrt(149+2*10*7*cos(50)),1),"exp 15.5")

print("\n=== SILVER BANK ===")
# s0 cosA a8 b6 c10
print("s0 top 36+100-64=",72,"; bot 120; cosA=0.6; acos=",round(acos(0.6),1),"exp 53.1; misc -0.6:",round(acos(-0.6),1),"exp 126.9")
# s1 cosC a12 b9 c7
print("s1 top 144+81-49=",176,"; bot 2*12*9=",216,"; cosC=",round(176/216,4),"exp 0.8148; acos=",round(acos(176/216),1),"exp 35.4; misc:",round(acos(-176/216),1),"exp 144.6")
# s2 third 11,14,75
print("s2 121+196=317; 2*11*14cos75=",round(2*11*14*cos(75),4),"exp 79.7163; c=",round(math.sqrt(317-79.7163),1),"exp 15.4; misc add sqrt(396.7)=",round(math.sqrt(317+2*11*14*cos(75)),1),"exp 19.9")
# s3 area PQ15 PR11 P42
print("s3 half=82.5 sin42=",round(sin(42),4),"exp 0.6691 ->",round(82.5*sin(42),1),"exp 55.2; misc 165sin42=",round(165*sin(42),1),"exp 110.4")
# s4 b a5 A30 B105
print("s4 5sin105=",round(5*sin(105),4),"exp 4.8296; /sin30 ->",round(5*sin(105)/sin(30),1),"exp 9.7; misc inv 5sin30/sin105=",round(5*sin(30)/sin(105),1),"exp 2.6")
# s5 a b15 c20 A110
print("s5 225+400=625; 2*15*20cos110=",round(2*15*20*cos(110),4),"exp -205.2121; a=",round(math.sqrt(625+205.2121),1),"exp 28.8; misc pos sqrt(625-205.2)=",round(math.sqrt(625-205.212),1),"exp 20.5")
# s6 hikers
print("s6 angle60; 34-15=19; d=",round(math.sqrt(19),1),"exp 4.4; misc add sqrt49=7")

print("\n=== TIER GUIDE EXAMPLES ===")
print("gold ex sinC=48/96=0.5 C=30; bronze ex a=8sin30/sin90=",8*sin(30)/sin(90),"=4; silver ex cosA=12/60=0.2 acos=",round(acos(0.2),1),"exp 78.5")
print("method ex a=8sin50/sin70=",round(8*sin(50)/sin(70),1),"exp 6.5")
print("worked0 sinB=5/7=",round(5/7,4)," asin=",round(asin(5/7),1),"exp 45.6; worked1 c=sqrt(49)=7")
