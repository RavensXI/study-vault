# -*- coding: utf-8 -*-
# Fresh-solve every problem in the live AQA algebra-L11 bank; compare to stored.
import json, re
from fractions import Fraction as F

pd = json.load(open("_live_aqa_algL11.json", encoding="utf-8"))
pb = pd["problem_bank"]

def rng(lo, hi, loinc, hiinc):
    # integers in (lo,hi) with inclusivity flags
    import math
    a = math.ceil(lo) if not loinc else math.ceil(lo)
    # careful: strict lower -> smallest int > lo
    lo_int = math.floor(lo) + 1 if (lo == int(lo) and not loinc) else math.ceil(lo)
    hi_int = math.ceil(hi) - 1 if (hi == int(hi) and not hiinc) else math.floor(hi)
    return list(range(lo_int, hi_int + 1))

# Manual fresh solves keyed by display fragment -> expected answer/idx
checks = []

def show(tier, i, note, ok):
    checks.append(ok)
    print(("OK " if ok else "XX ") + f"{tier}[{i}] {note}")

# BRONZE
b = pb["bronze"]
show("bronze",0,"x+4>9 -> x>5 idx0", b[0]["options"][b[0]["solutions"][0]]=="\\(x > 5\\)")
show("bronze",1,"3x<=15 -> x<=5 idx0", b[1]["options"][b[1]["solutions"][0]]=="\\(x \\le 5\\)")
show("bronze",2,"2x-1<9 -> x<5 idx0", b[2]["options"][b[2]["solutions"][0]]=="\\(x < 5\\)")
show("bronze",3,"5x+2>=17 -> x>=3 idx0", b[3]["options"][b[3]["solutions"][0]]=="\\(x \\ge 3\\)")
show("bronze",4,"-2<n<=3 -> -1,0,1,2,3 idx0", b[4]["solutions"][0]==0 and b[4]["options"][0]=="\\(-1, 0, 1, 2, 3\\)" and rng(-2,3,False,True)==[-1,0,1,2,3])
show("bronze",5,"4x>2x+6 -> x>3 idx0", b[5]["options"][b[5]["solutions"][0]]=="\\(x > 3\\)")
show("bronze",6,"10-x<4 -> x>6 idx0", b[6]["options"][b[6]["solutions"][0]]=="\\(x > 6\\)")
show("bronze",7,"x/2+1>4 -> x>6 idx0 (DUP with b6)", b[7]["options"][b[7]["solutions"][0]]=="\\(x > 6\\)")

# SILVER
s = pb["silver"]
show("silver",0,"-2x+5>11 -> x<-3 idx0", s[0]["options"][s[0]["solutions"][0]]=="\\(x < -3\\)")
show("silver",1,"3(x-2)<=12 -> x<=6 idx0", s[1]["options"][s[1]["solutions"][0]]=="\\(x \\le 6\\)")
show("silver",2,"7-3x>=1 -> x<=2 idx0", s[2]["options"][s[2]["solutions"][0]]=="\\(x \\le 2\\)")
show("silver",3,"1<2x-3<=9 -> 3,4,5,6 idx0", s[3]["solutions"][0]==0 and rng(2,6,False,True)==[3,4,5,6])
show("silver",4,"5x+3>2x+15 -> x>4 idx0", s[4]["options"][s[4]["solutions"][0]]=="\\(x > 4\\)")
show("silver",5,"-4<=3x+2<11 -> -2,-1,0,1,2 idx0", s[5]["solutions"][0]==0 and rng(-2,3,True,False)==[-2,-1,0,1,2])
show("silver",6,"largest n: 4n-7<20 -> 6", s[6]["solutions"][0]==6 and (4*6-7<20) and not(4*7-7<20))

# GOLD
g = pb["gold"]
show("gold",0,"x^2<16 -> -4<x<4 idx0", g[0]["options"][g[0]["solutions"][0]]=="\\(-4 < x < 4\\)")
show("gold",1,"x^2>=9 -> x<=-3 or x>=3 idx0", g[1]["solutions"][0]==0)
show("gold",2,"2x+1>5 & 3x-4<14 -> 2<x<6 idx0", g[2]["options"][g[2]["solutions"][0]]=="\\(2 < x < 6\\)" and (5-1)/2==2 and (14+4)/3==6)
show("gold",3,"n^2<50 largest n -> 7", g[3]["solutions"][0]==7 and 7*7<50 and not(8*8<50))
show("gold",4,"-3<(2x-1)/3<=5 list idx0", g[4]["solutions"][0]==0 and rng(-4,8,False,True)==[-3,-2,-1,0,1,2,3,4,5,6,7,8])

print("\nALL PASS" if all(checks) else "\nFAILURES PRESENT")
