import json, re, math
pd=json.load(open("lesson_geometry-L06.json",encoding="utf-8"))
d=pd["problem_bank"]["silver"][0]["display"]
# check degree char
for m in re.finditer(r'>([^<]*)<', d):
    t=m.group(1)
    if any(ord(c)>127 for c in t):
        print("nonascii text:", repr(t))
# vertices
P1=(80.7,141.0); P2=(159.3,141.0); P3=(109.4,34.0)
def ang(A,B,C):
    # angle at B
    v1=(A[0]-B[0],A[1]-B[1]); v2=(C[0]-B[0],C[1]-B[1])
    d=(v1[0]*v2[0]+v1[1]*v2[1])/(math.hypot(*v1)*math.hypot(*v2))
    return math.degrees(math.acos(d))
print("angle P1 (bottom-left):", round(ang(P2,P1,P3),1))
print("angle P2 (bottom-right):", round(ang(P1,P2,P3),1))
print("angle P3 (apex):", round(ang(P1,P3,P2),1))
