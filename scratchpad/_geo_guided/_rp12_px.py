import os
from PIL import Image
import numpy as np
d=os.path.dirname(os.path.abspath(__file__))
def grid(name):
    im=Image.open(os.path.join(d,"_m_"+name)).convert("RGB")
    a=np.asarray(im).astype(int)
    r,g,b=a[:,:,0],a[:,:,1],a[:,:,2]
    # OS grid lines are light blue/violet thin lines
    m=(b>150)&(b-r>30)&(b-g>20)&(r>60)
    colsum=m.sum(axis=0); rowsum=m.sum(axis=1)
    H,W=m.shape
    cols=[i for i in range(W) if colsum[i]>H*0.5]
    rows=[i for i in range(H) if rowsum[i]>W*0.5]
    def group(xs):
        out=[];cur=[xs[0]] if xs else []
        for x in xs[1:]:
            if x-cur[-1]<=3: cur.append(x)
            else: out.append(sum(cur)/len(cur)); cur=[x]
        if cur: out.append(sum(cur)/len(cur))
        return out
    return group(cols), group(rows), im.size
for n in ["ribble-valley-z16-final.jpg","lake-district-z15-final.jpg","dorset-coast-z16-final.jpg","peak-district-z16-final.jpg","yorkshire-dales-z16-final.jpg","ribble-valley-z15-final.jpg","dorset-coast-z15-final.jpg","peak-district-z15-final.jpg"]:
    c,r,s=grid(n)
    dc=[round(c[i+1]-c[i],1) for i in range(len(c)-1)]
    dr=[round(r[i+1]-r[i],1) for i in range(len(r)-1)]
    print(n, s, "cols",[round(x,1) for x in c], dc, "rows",[round(x,1) for x in r], dr)
