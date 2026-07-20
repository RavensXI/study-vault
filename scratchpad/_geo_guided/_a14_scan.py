from PIL import Image
import sys
im=Image.open(sys.argv[1]).convert("RGB")
y0=int(sys.argv[2]); x0=int(sys.argv[3]); x1=int(sys.argv[4])
rows=[y0] if len(sys.argv)<6 else [y0+i for i in range(0,int(sys.argv[5]))]
for y in rows:
    runs=[]; cur=None
    for x in range(x0,x1):
        r,g,b=im.getpixel((x,y))
        brown = r>70 and r<200 and g<r-20 and b<g and (r-b)>30
        if brown:
            if cur is None: cur=[x,x]
            else: cur[1]=x
        else:
            if cur: runs.append((cur[0],cur[1]-cur[0]+1)); cur=None
    if cur: runs.append((cur[0],cur[1]-cur[0]+1))
    print(y, [f"{a}w{w}" for a,w in runs])
