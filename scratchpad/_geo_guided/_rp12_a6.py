import os
from PIL import Image
import numpy as np
d=os.path.dirname(os.path.abspath(__file__))
im=Image.open(os.path.join(d,"_m_ribble-valley-z16-final.jpg")).convert("RGB")
a=np.asarray(im).astype(int)
r,g,b=a[:,:,0],a[:,:,1],a[:,:,2]
# pink A road approx (233,109,140)? find pinkish
m=(r>215)&(g>80)&(g<160)&(b>110)&(b<180)&(r-g>70)
for y in [0,1,2,5,10,300,650,1000,1290,1295,1299,1301]:
    xs=np.where(m[y])[0]
    print(y, xs.min() if len(xs) else None, xs.max() if len(xs) else None, len(xs))
