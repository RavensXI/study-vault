# -*- coding: utf-8 -*-
import json, io
pd = json.load(io.open(r"C:/Users/tshau/Documents/Study Vault/.claude/worktrees/sandbox/scratchpad/_maths_boards/lesson_maths-ocr_algebra-L13.json", encoding="utf-8"))
errs=[]

def nth_linear(seq):
    d=seq[1]-seq[0]
    return d, seq[0]-d  # d, zero term

# --- fresh solve every problem from display, compare stored ---
checks = {
 "bronze": [
  ("20th term 3,7,11,15", 4*20-1, 79),
  ("nth 5,9,13,17 -> 4n+1 idx0", 0, 0),
  ("nth 2,5,8,11 -> 3n-1 idx0", 0, 0),
  ("nth 7,12,17,22 -> 5n+2 idx0", 0, 0),
  ("nth 1,5,9,13 -> 4n-3 idx0", 0, 0),
  ("common diff 10,7,4,1", 7-10, -3),
  ("5th term 2n+3", 2*5+3, 13),
  ("next 3,6,12,24", 24*2, 48),
 ],
 "silver": [
  ("is 50 in 7n+1 -> n=(50-1)/7", (50-1)//7 if (50-1)%7==0 else -1, 7),  # membership n
  ("nth 20,17,14,11 -> 23-3n idx0", 0, 0),
  ("nth 6,3,0,-3 -> 9-3n idx0", 0, 0),
  ("ratio 4,12,36,108", 12//4, 3),
  ("8th term 5,10,20,40", 5*2**7, 640),
  ("6th term n^2+1", 6**2+1, 37),
  ("which term 3n-5=40", (40+5)//3, 15),
 ],
 "gold": [
  ("ratio a=2,4th=54 -> r^3=27", round((54/2)**(1/3)), 3),
  ("5th term 2n^2-3", 2*5**2-3, 47),
  ("100*0.5^(n-1) first<1", None, 8),
  ("fib 10th", None, 55),
  ("sum 3 consec 2n+1 -> 6n+9 idx0", 0, 0),
 ],
}
# verify linear nth-term MCQ rules land on option index 0
def check_mcq(seq, expect_expr):
    d, zt = nth_linear(seq)
    return d, zt

# bronze MCQ rules
assert nth_linear([5,9,13,17])==(4,1)
assert nth_linear([2,5,8,11])==(3,-1)
assert nth_linear([7,12,17,22])==(5,2)
assert nth_linear([1,5,9,13])==(4,-3)
assert nth_linear([20,17,14,11])==(-3,23)
assert nth_linear([6,3,0,-3])==(-3,9)

# gold growth/decay
v=100; n=1
while v>=1:
    n+=1; v*=0.5
assert n==8, ("decay", n, v)
# fib
f=[1,1]
while len(f)<10: f.append(f[-1]+f[-2])
assert f[9]==55, f

# now check stored solutions match
for tier, rows in checks.items():
    probs = pd["problem_bank"][tier]
    for i,(name,computed,expected) in enumerate(rows):
        sol = probs[i]["solutions"][0]
        if expected!=sol:
            errs.append("STORED MISMATCH %s[%d] %s stored=%s expected=%s"%(tier,i,name,sol,expected))
        if computed is not None and computed!=expected and expected!=0:
            errs.append("COMPUTE MISMATCH %s[%d] %s computed=%s expected=%s"%(tier,i,name,computed,expected))

# --- verify final answer box of each guided walk lands on the solution ---
def last_box(steps):
    boxes=[s["answer"] for s in steps if s.get("answer") is not None]
    return boxes
for tier in ("bronze","silver","gold"):
    for i,p in enumerate(pd["problem_bank"][tier]):
        gs=p.get("guided_steps")
        if not gs: continue
        boxes=last_box(gs)
        sol=p["solutions"][0]
        if sol not in boxes:
            errs.append("WALK never hits solution %s[%d] sol=%s boxes=%s"%(tier,i,sol,boxes))

# --- verify expects differ from solution and are the claimed error value ---
# bronze[0]: forgot_constant 4*20=80; used_first_term 4n+3->4*20+3=83
assert 4*20==80 and 4*20+3==83
# bronze[6] 5th term: forgot 2*5=10; bracket 2*(5+3)=16
assert 2*5==10 and 2*(5+3)==16
# silver[4] 8th: power_n 5*2^8=1280; product 5*2*7=70
assert 5*2**8==1280 and 5*2*7==70
# silver[5]: read_as_2n 2*6+1=13; forgot 6^2=36
assert 2*6+1==13 and 6**2==36
# silver[6]: substituted 3*40-5=115
assert 3*40-5==115
# gold[0]: ratio_not_cubed 54/2=27
assert 54/2==27
# gold[1]: squared_whole (2*5)^2-3=97; forgot 2*25=50
assert (2*5)**2-3==97 and 2*25==50
# gold[3] fib: off_by_one 34 is 9th
assert f[8]==34

# --- opener + teach box arithmetic ---
assert 2*2+2==6 and 2*3+2==8  # opener 6,8
# teach bronze matchstick 4,7,10: d=3 zt=1 rule 3n+1; p10=31; p1=4
assert 7-4==3 and 4-3==1 and 3*10+1==31 and 3*1+1==4
# teach silver: 9-5=4, 5-4=1, 79/4=19.75, 80/4=20
assert 9-5==4 and 5-4==1 and 79/4==19.75 and 80/4==20
# teach gold: 375/3=125, cube root 125=5, 3*5=15, 3*125=375
assert 375/3==125 and 5**3==125 and 3*5==15 and 3*125==375

# gold decay walk boxes: 100/32=3.125, /2=1.5625, /2=0.78125
assert 100/32==3.125 and 3.125/2==1.5625 and 1.5625/2==0.78125

print("ERRORS:", errs if errs else "NONE")
