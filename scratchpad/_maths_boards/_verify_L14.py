import math
def diffs(s):
    d1=[s[i+1]-s[i] for i in range(len(s)-1)]
    d2=[d1[i+1]-d1[i] for i in range(len(d1)-1)]
    return d1,d2
def quad_nth(seq):
    d1,d2=diffs(seq)
    a=d2[0]/2
    rem=[seq[i]-a*(i+1)**2 for i in range(len(seq))]
    # linear part
    b=rem[1]-rem[0]; c=rem[0]-b
    return a,b,c,rem
seqs={
 "gold[0] 2,8,18,32,50":[2,8,18,32,50],
 "gold[3] 1,7,17,31,49":[1,7,17,31,49],
 "bronze[4] 3,6,11,18,27":[3,6,11,18,27],
 "silver[0] 0,3,8,15,24":[0,3,8,15,24],
 "silver[4] 4,10,18,28,40":[4,10,18,28,40],
 "teach.gold 4,13,26,43,64":[4,13,26,43,64],
 "mcard 3,8,15,24,35":[3,8,15,24,35],
 "we0 2,6,12,20,30":[2,6,12,20,30],
 "goldex 4,13,28,49":[4,13,28,49],
}
for k,s in seqs.items():
    a,b,c,rem=quad_nth(s)
    print(f"{k}: a={a} b={b} c={c} rem={rem}")
# silver6 next term
s=[5,12,23]; d1,_=diffs(s); print("silver6 gaps",d1,"next gap",d1[-1]+(d1[1]-d1[0]),"next term",s[-1]+d1[-1]+(d1[1]-d1[0]))
# gold2 iteration
import math
print("gold2 disc",25+8,"sqrt33",round(math.sqrt(33),4),"L",round((5+math.sqrt(33))/2,4),"x1",round(math.sqrt(17),4))
# gold1 inverse: f=(2x+1)/(x-3)
print("gold1 f^-1 num coeff = 3 (from x(y-2)=3y+1)")
# silver3 iteration
x0=2; x1=(x0**2+5)/4; x2=(x1**2+5)/4; print("silver3 x1",x1,"x2",round(x2,4))
# we2
x=1
for i in range(3): x=(x**2+3)/5
print("we2 x3",round(x,4))
# functions
print("silver1 fg(2)=",3*(2**2)-1,"gf(2)=",(3*2-1)**2)
print("silver5 gf(4)=",3*(4**2+2),"fg(4)=",(3*4)**2+2)
print("silver2 f^-1(17)=",(17-2)/5,"f(17)=",5*17+2)
print("gold4 fg roots (2x-1)^2=25 ->",3,-2)
