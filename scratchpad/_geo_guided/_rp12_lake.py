import os
from PIL import Image
import numpy as np
d=os.path.dirname(os.path.abspath(__file__))
im=Image.open(os.path.join(d,"_m_lake-district-z15-final.jpg")).convert("RGB")
a=np.asarray(im).astype(int)
r,g,b=a[:,:,0],a[:,:,1],a[:,:,2]
# water fill light blue approx (168,220,240)?
w=(b>200)&(b-r>30)&(g>180)&(g<235)&(r<200)
ys,xs=np.where(w)
print("water px",len(xs))
# cluster by rows
import collections
for y0 in range(0,1302,100):
    sel=(ys>=y0)&(ys<y0+100)
    if sel.sum()>200:
        print(y0, sel.sum(), xs[sel].min(), xs[sel].max())
# northern tip of big lake: min y among x 200-650, y>1000
sel=(xs>200)&(xs<700)&(ys>1050)
print("lake region count",sel.sum(), "min y", ys[sel].min() if sel.sum() else None)
sub_y=ys[sel]; sub_x=xs[sel]
i=np.argmin(sub_y); print("tip at", sub_x[i], sub_y[i])
for yy in range(int(sub_y.min()), int(sub_y.min())+60,10):
    s2=sel&(ys==yy)
    if s2.sum(): print(yy, xs[s2].min(), xs[s2].max(), s2.sum())
