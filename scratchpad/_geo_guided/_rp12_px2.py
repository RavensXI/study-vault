import os
from PIL import Image
import numpy as np
d=os.path.dirname(os.path.abspath(__file__))
def grid(name,frac=0.35):
    im=Image.open(os.path.join(d,"_m_"+name)).convert("RGB")
    a=np.asarray(im).astype(int)
    r,g,b=a[:,:,0],a[:,:,1],a[:,:,2]
    m=(b>140)&(b-r>25)&(b-g>15)
    colsum=m.sum(axis=0); rowsum=m.sum(axis=1)
    H,W=m.shape
    cols=[i for i in range(W) if colsum[i]>H*frac]
    rows=[i for i in range(H) if rowsum[i]>W*frac]
    def group(xs):
        out=[];cur=[xs[0]] if xs else []
        for x in xs[1:]:
            if x-cur[-1]<=4: cur.append(x)
            else: out.append(sum(cur)/len(cur)); cur=[x]
        if cur: out.append(sum(cur)/len(cur))
        return out
    return group(cols), group(rows)
for n in ["lake-district-z15-final.jpg","dorset-coast-z16-final.jpg","peak-district-z16-final.jpg","yorkshire-dales-z16-final.jpg","dorset-coast-z15-final.jpg","peak-district-z15-final.jpg"]:
    for f in (0.35,0.25):
        c,r=grid(n,f)
        dc=[round(c[i+1]-c[i],1) for i in range(len(c)-1)]
        dr=[round(r[i+1]-r[i],1) for i in range(len(r)-1)]
        print(n,f,"cols",[round(x,1) for x in c],dc,"rows",[round(x,1) for x in r],dr)
