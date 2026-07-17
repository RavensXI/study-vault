import json, re, math
pd=json.load(open("_live_L06_fetched.json",encoding="utf-8"))

def poly_angles(pts):
    # pts list of (x,y); svg y is downward. return interior angles in order
    n=len(pts); out=[]
    for i in range(n):
        p=pts[i]; a=pts[(i-1)%n]; b=pts[(i+1)%n]
        v1=(a[0]-p[0],a[1]-p[1]); v2=(b[0]-p[0],b[1]-p[1])
        d=v1[0]*v2[0]+v1[1]*v2[1]
        m=math.hypot(*v1)*math.hypot(*v2)
        out.append(math.degrees(math.acos(max(-1,min(1,d/m)))))
    return out

def get_poly(disp):
    m=re.search(r'points="([^"]+)"',disp)
    nums=re.findall(r'[-\d.]+',m.group(1))
    return [(float(nums[i]),float(nums[i+1])) for i in range(0,len(nums),2)]

def check(label, disp, claimed):
    pts=get_poly(disp)
    angs=poly_angles(pts)
    print(f"{label}: drawn interior angles = {[round(a,1) for a in angs]}  (claimed set: {claimed})")

# opener 30-60-90
check("OPENER", pd["guided"]["opener"]["display"], "30/60/90")
for tier in ["gold","bronze","silver"]:
    for i,p in enumerate(pd["problem_bank"][tier]):
        d=p["display"]
        if "<svg" in d:
            # extract angle labels shown
            labs=re.findall(r'>(\d+°|\?)</text>',d)
            check(f"{tier}[{i}]", d, "".join(labs))
