import math
def r1(x): return round(x,1)
# Reproduce each misconception error -> compare to stored expect
checks = [
 # tier,idx,pattern, committed-error value, stored expect
 ("gold",0,"whole_circle", r1(math.pi*64), 201.1),
 ("gold",0,"arc_not_area", r1(135/360*2*math.pi*8), 18.8),
 ("gold",1,"area_not_arc", r1(72/360*math.pi*100), 62.8),
 ("gold",2,"radius_for_diameter", round(2*math.pi*60+200), 577),
 ("gold",3,"forgot_sqrt", round(154/math.pi), 49),
 ("gold",4,"subtract_radii", r1(math.pi*16), 50.3),
 ("bronze",0,"perimeter", 2*(12+5), 34),
 ("bronze",1,"area", 9*4, 36),
 ("bronze",2,"no_half", 10*6, 60),
 ("bronze",3,"halve", 8*5//2, 20),
 ("bronze",4,"no_half", 14*6, 84),
 ("bronze",5,"half_perimeter", (28//2)**2, 196),
 ("bronze",6,"area_confusion", r1(math.pi*49), 153.9),
 ("bronze",7,"circumference_confusion", r1(2*math.pi*5), 31.4),
 ("silver",0,"full_circle", r1(math.pi*36), 113.1),
 ("silver",0,"diameter_as_radius", r1(0.5*math.pi*144), 226.2),
 ("silver",1,"add_not_subtract", r1(120+math.pi*9), 148.3),
 ("silver",2,"forgot_half", 36//9, 4),
 ("silver",3,"arc_only", round(25.7/math.pi), 8),
 ("silver",4,"one_triangle", 6*4//2, 12),
 ("silver",5,"forgot_half_radius", r1(math.pi*(31.4/math.pi)**2), 314.2),
 ("silver",6,"forgot_subtract", 6*5, 30),
]
bad=0
for t,i,pat,val,exp in checks:
    ok = abs(val-exp)<0.06
    if not ok:
        bad+=1; print(f"MISMATCH {t}[{i}] {pat}: committed {val} vs stored expect {exp}")
print(f"expects checked: {len(checks)}, mismatches: {bad}")

# teach + opener boxes
teach = {
 "teach.gold": [6*6==36, r1(math.pi*36)==113.1, 90/360==0.25, r1(0.25*113.1)==28.3, 28.3*4==113.2],
 "teach.bronze":[4+10==14, 14/2==7, 7*6==42, 14*6==84, 84/2==42],
 "teach.silver":[20/2==10, 10*10==100, r1(math.pi*100)==314.2, r1(314.2/2)==157.1, 157.1*2==314.2],
 "opener":[5*3==15, 5+3+5+3==16],
}
for k,v in teach.items():
    for j,ok in enumerate(v):
        if not ok: print(f"TEACHBOX FAIL {k} box{j}")
print("teach/opener box arithmetic verified")
