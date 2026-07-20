from PIL import Image
import sys
im=Image.open(sys.argv[1]).convert("RGB")
mode=sys.argv[2]  # 'h' or 'v'
fixed=int(sys.argv[3]); a=int(sys.argv[4]); b=int(sys.argv[5])
runs=[];cur=None
for t in range(a,b):
    x,y=(t,fixed) if mode=='h' else (fixed,t)
    r,g,bb=im.getpixel((x,y))
    brown = r<210 and g<r-15 and bb<g-5
    if brown:
        if cur is None: cur=[t,t,r]
        else: cur[1]=t; cur[2]=min(cur[2],r)
    else:
        if cur: runs.append(tuple(cur)); cur=None
if cur: runs.append(tuple(cur))
for s,e,mn in runs:
    print(f"pos {s}-{e} w={e-s+1} dark={mn} {'INDEX' if (e-s+1)>=3 or mn<110 else ''}")
