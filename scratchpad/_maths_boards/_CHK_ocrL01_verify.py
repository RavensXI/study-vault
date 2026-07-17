import json, re
from fractions import Fraction as F
pd = json.load(open("_CHK_ocrL01_live.json", encoding="utf-8"))
pb = pd["problem_bank"]
issues = []

def num(x):
    return x

# ---- fresh solve each bank problem ----
def solve_share(total, parts, want_idx):
    one = F(total, sum(parts))
    return one*parts[want_idx]

# Bronze
B = pb["bronze"]
checks = {
 0: ("Simplify 15:25 first", 15//5, 3),
 1: ("Simplify 24:30 first", 24//6, 4),
 2: ("Share £60 1:2 larger", solve_share(60,[1,2],1), 40),
 3: ("Share 45 2:3 first", solve_share(45,[2,3],0), 18),
 4: ("40cm:1m first -> 40:100 /20", 40//20, 2),
 5: ("recipe 4->6 200g", F(200,4)*6, 300),
 6: ("Simplify 30:42 first", 30//6, 5),
 7: ("Share £100 3:2 larger", solve_share(100,[3,2],0), 60),
}
for i,(desc,got,stored) in checks.items():
    if F(got)!=F(stored) or F(B[i]["solutions"][0])!=F(stored):
        issues.append(f"BRONZE[{i}] {desc}: got {got} stored {B[i]['solutions']}")

# Silver
S = pb["silver"]
schecks = {
 0: ("Share £360 1:2:3 largest", solve_share(360,[1,2,3],2), 180),
 1: ("Ali 3:5 Ali=45 Ben", F(45,3)*5, 75),
 2: ("5 books £35 -> 8", F(35,5)*8, 56),
 3: ("2:5 as 1:n", F(5,2), F(5,2)),
 4: ("map 1:50000 3cm metres", F(3*50000,100), 1500),
 5: ("concrete 1:2:4 sand 350", solve_share(350,[1,2,4],1), 100),
 6: ("recipe 6->10 450ml", F(450,6)*10, 750),
}
for i,(desc,got,stored) in schecks.items():
    if F(got)!=F(S[i]["solutions"][0]):
        issues.append(f"SILVER[{i}] {desc}: got {got} stored {S[i]['solutions']}")

# Gold
G = pb["gold"]
# G1 diff share
g1_one = F(36,5-2); g1_total = (2+5)*g1_one
# G2 a:c
import math
b1,b2=3,4; L=b1*b2//math.gcd(b1,b2)
a=2*(L//3); c=5*(L//4); g2=a  # a:c = a:c, first number a scaled -> simplest
gg=math.gcd(a,c); g2first=a//gg
# G3 per gram
pa=F(270,750); pbv=F(420,1200); g3 = 2 if pbv<pa else 1
# G4 boys
g4=solve_share(35,[3,4],0)
# G5 juice
g5=solve_share(F(35,10),[2,5],0)
gchecks = {
 0: ("Amy 2:5 Ben+36 total", g1_total, 84),
 1: ("a:b=2:3 b:c=4:5 first", g2first, 8),
 2: ("Pack A 750/2.70 vs B 1200/4.20", g3, 2),
 3: ("boys 3:4 of 35", g4, 15),
 4: ("juice 2:5 of 3.5", g5, 1),
}
for i,(desc,got,stored) in gchecks.items():
    if F(got)!=F(G[i]["solutions"][0]):
        issues.append(f"GOLD[{i}] {desc}: got {got} stored {G[i]['solutions']}")
print("a:c =", a, ":", c, " first sim:", g2first)
print("perg A", float(pa), "B", float(pbv))

print("=== SOLVE ISSUES ===")
for x in issues: print(x)
if not issues: print("none")
