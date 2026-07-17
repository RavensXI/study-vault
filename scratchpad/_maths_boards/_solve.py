import math
def disc(a,b,c): return b*b-4*a*c
def bigroot(a,b,c,sign): return (-b+sign*math.sqrt(disc(a,b,c)))/(2*a)
checks = [
 ("gold0 sum roots 3x2-5x+1", 5/3, "5/3 [5,3]"),
 ("gold1 k one soln", (6*6)/4, "9"),
 ("gold2 q 2x2+12x+5", 5-2*(6/2)**2, "-13"),
 ("gold3 disc k=5", disc(5,8,11), "-156"),
 ("gold4 yTP x2-4x+7", 7-(4/2)**2, "3"),
 ("b0 b", 3, "3"),
 ("b1 disc x2+4x+1", disc(1,4,1), "12"),
 ("b2 disc x2-6x+9", disc(1,-6,9), "0"),
 ("b3 disc x2+2x+5", disc(1,2,5), "-16"),
 ("b4 p x2+6x", 6/2, "3"),
 ("b5 q x2+6x", (6/2)**2, "9"),
 ("b6 disc 2x2+3x-1", disc(2,3,-1), "17"),
 ("b7 roots x2+2x+5", 0 if disc(1,2,5)<0 else '?', "0"),
 ("s0 pos x2+4x-3", round(bigroot(1,4,-3,1),2), "0.65"),
 ("s1 larger x2-6x+4", round(bigroot(1,-6,4,1),2), "5.24"),
 ("s2 q x2+8x+5", 5-(8/2)**2, "-11"),
 ("s3 min x2-10x+3", 3-(10/2)**2, "-22"),
 ("s4 pos 2x2+3x-4", round(bigroot(2,3,-4,1),2), "0.85"),
 ("s5 larger x2+5x+2", round(bigroot(1,5,2,1),2), "-0.44"),
 ("s6 q x2+2x-7", -7-(2/2)**2, "-8"),
]
for n,v,s in checks:
    print(f"{n:22} computed={str(v):8} stored={s}")
