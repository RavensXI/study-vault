from fractions import Fraction as F
# Fresh-solve every problem independently
res={}
# BRONZE
res['b0']=15/5*8            # 24
res['b1']=6/4*10            # 15
res['b2']=12/3              # 4 (k)
res['b3']=5*12/1            # 60 (1 worker inverse)
res['b4']=10*2              # 20 (k inverse)
res['b5']=750/3*5           # 1250
res['b6']=200/4*6           # 300
res['b7']=7*9               # 63
# SILVER
res['s0']=35/(F(21,6))      # x when y=35, k=21/6 -> 10
res['s1']=(4*15)/12         # 5
res['s2']=(6*8)/4           # 12
res['s3']=540/36*20         # 300
res['s4']=(5*24)/40         # 3
res['s5']='MC idx0 y=3x (k=12/4=3)'
res['s6']=500/8*12          # 750
# GOLD
res['g0']=(15/3)*4          # k=5, y=20
res['g1']=(8*15-8*5)/5      # 16
res['g2']=(2*18)/4          # 9
res['g3']=180/6-180/8       # 7.5
res['g4']=(36/9)*25         # 100
for k,v in res.items():
    print(k, v)
