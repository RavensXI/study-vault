import json, math
S=lambda d: math.sin(math.radians(d)); C=lambda d: math.cos(math.radians(d))
A=lambda x: math.degrees(math.asin(x)); AC=lambda x: math.degrees(math.acos(x))

exp=[]
# gold[0] no_half: asin(40/120)
exp+=[("gold[0]",A(40/120),19.5)]
# gold[1] sign_slip arccos(+0.1667)
exp+=[("gold[1]",AC(0.1667),80.4)]
# gold[2] extra_solution 180-43.6
exp+=[("gold[2]",180-43.6,136.4)]
# gold[3] no_sqrt stops at product 1836
exp+=[("gold[3]",1836,1836)]
# gold[4] used_half 0.5*96*sin65
exp+=[("gold[4]",0.5*96*S(65),43.5)]
# bronze[0] no_half 8*6*sin90
exp+=[("bronze[0]",8*6*S(90),48)]
# bronze[1] no_half 10*12*sin30
exp+=[("bronze[1]",10*12*S(30),60)]
# bronze[2] no_half 5*8*sin60
exp+=[("bronze[2]",5*8*S(60),34.6)]
# bronze[3] no_sqrt stops at a^2 =74
exp+=[("bronze[3]",74,74)]
# bronze[4] MCQ expect null -> skip
# bronze[5] no_half 9*9*sin45
exp+=[("bronze[5]",9*9*S(45),57.3)]
# bronze[6] no_inverse types cos value 0
exp+=[("bronze[6]",0,0)]
# bronze[7] wrong_operation 10*sin30
exp+=[("bronze[7]",10*S(30),5)]
# silver[0] two: sign_add 185+100.9494 sqrt ->16.9 ; no_sqrt a^2 84.1
exp+=[("silver[0]a",math.sqrt(185+100.9495),16.9),("silver[0]b",84.1,84.1)]
# silver[1] inverted_ratio 15 sin65/sin42
exp+=[("silver[1]",15*S(65)/S(42),20.3)]
# silver[2] sign_slip arccos(+0.1111)
exp+=[("silver[2]",AC(0.1111),83.6)]
# silver[3] no_half 13*17*sin72
exp+=[("silver[3]",13*17*S(72),210.2)]
# silver[4] swapped_sides asin(9 sin40/12)
exp+=[("silver[4]",A(9*S(40)/12),28.8)]
# silver[5] sign_cos sqrt(61-10.4189)
exp+=[("silver[5]",math.sqrt(61-10.4189),7.1)]
# silver[6] assume_right 0.5*5*6
exp+=[("silver[6]",0.5*5*6,15)]

bad=[]
for path,comp,stored in exp:
    if abs(round(comp,1)-stored)>0.06:
        bad.append(f"{path}: committed error -> {comp:.4f} (~{round(comp,1)}) but expect={stored}")
print("EXPECT MISMATCHES:", len(bad))
for b in bad: print("  ",b)
