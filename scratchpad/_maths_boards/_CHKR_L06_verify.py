import json, math

pd = json.load(open("_CHKR_L06_live.json", encoding="utf-8"))
errs = []

def approx(a, b, tol=0.06):
    return abs(a-b) <= tol

def solve_area(s1,s2,ang):
    return 0.5*s1*s2*math.sin(math.radians(ang))

def cosrule_side(b,c,A):
    return math.sqrt(b*b+c*c-2*b*c*math.cos(math.radians(A)))

def cosrule_angle(a,b,c):
    # angle opposite c
    return math.degrees(math.acos((a*a+b*b-c*c)/(2*a*b)))

# ---- BANK ----
pb = pd["problem_bank"]
print("=== FRESH SOLVE BANK ===")

# gold
g = pb["gold"]
# g0: area 40, sides 10,12, find acute included angle
sinC = 40/(0.5*10*12); a0 = math.degrees(math.asin(sinC)); print("gold0 angle", round(a0,1), "stored", g[0]["solutions"])
# g1: cos rule angle C, a8 b9 c13
a1 = cosrule_angle(8,9,13); print("gold1 C", round(a1,1), "stored", g[1]["solutions"])
# g2: sine ambiguous a10 b7 A100 find B
sinB = 7*math.sin(math.radians(100))/10; b2 = math.degrees(math.asin(sinB)); print("gold2 B", round(b2,1), "stored", g[2]["solutions"])
# g3: heron 8,11,15
s=(8+11+15)/2; ar=math.sqrt(s*(s-8)*(s-11)*(s-15)); print("gold3 area", round(ar,1), "stored", g[3]["solutions"])
# g4: parallelogram 8,12,65
par=8*12*math.sin(math.radians(65)); print("gold4 area", round(par,1), "stored", g[4]["solutions"])

# bronze
b = pb["bronze"]
print("--bronze--")
print("b0 area", round(solve_area(8,6,90),1), g[0]["solutions"])
print("b1 area", round(solve_area(10,12,30),1), b[1]["solutions"])
print("b2 area", round(solve_area(5,8,60),1), b[2]["solutions"])
print("b3 cos side a b5 c7 A90", round(cosrule_side(5,7,90),1), b[3]["solutions"])
print("b4 MCQ", b[4]["solutions"])
print("b5 area 9,9,45", round(solve_area(9,9,45),1), b[5]["solutions"])
print("b6 cos angle a6 b8 c10", round(cosrule_angle(6,8,10),1), b[6]["solutions"])
print("b7 ratio 10/sin30", round(10/math.sin(math.radians(30)),1), b[7]["solutions"])

# silver
s_ = pb["silver"]
print("--silver--")
print("s0 cos side b8 c11 A55", round(cosrule_side(8,11,55),1), s_[0]["solutions"])
# s1 sine side b, a15 A65 B42
b_=15*math.sin(math.radians(42))/math.sin(math.radians(65)); print("s1 side b", round(b_,1), s_[1]["solutions"])
# s2 largest angle sides 7,9,12 -> angle opp 12
print("s2 largest angle", round(cosrule_angle(7,9,12),1), s_[2]["solutions"])
print("s3 area 13,17,72", round(solve_area(13,17,72),1), s_[3]["solutions"])
# s4 sine angle B, a9 A40 b12
sinB4=12*math.sin(math.radians(40))/9; print("s4 B", round(math.degrees(math.asin(sinB4)),1), s_[4]["solutions"])
# s5 cos side c, a5 b6 C100
print("s5 side c", round(cosrule_side(5,6,100),1), s_[5]["solutions"])
# s6 area sides 5,6,7 find angle then area
C=cosrule_angle(5,6,7); ar6=solve_area(5,6,C); print("s6 area", round(ar6,1), s_[6]["solutions"])
