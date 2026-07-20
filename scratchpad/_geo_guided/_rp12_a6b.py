import os
from PIL import Image
import numpy as np
d=os.path.dirname(os.path.abspath(__file__))
im=Image.open(os.path.join(d,"_m_ribble-valley-z16-final.jpg")).convert("RGB")
a=np.asarray(im).astype(int)
r,g,b=a[:,:,0],a[:,:,1],a[:,:,2]
m=(r>215)&(g>80)&(g<160)&(b>110)&(b<180)&(r-g>70)
last=None
for y in range(1200,1302):
    xs=np.where(m[y])[0]
    if len(xs): last=(y,xs.min(),xs.max())
print("last pink row",last)
# also check bottom strip colour
print(a[1290,700], a[1275,700], a[1260,700])
