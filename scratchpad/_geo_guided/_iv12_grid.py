from PIL import Image
import numpy as np, glob
def gridlines(f):
    im=np.array(Image.open(f).convert("RGB")).astype(int)
    r,g,b=im[:,:,0],im[:,:,1],im[:,:,2]
    # OS grid lines are blue/purple thin lines
    mask=(b>120)&(b-r>40)&(b-g>30)
    cols=mask.sum(axis=0); rows=mask.sum(axis=1)
    def peaks(v, thr):
        out=[]; i=0
        while i<len(v):
            if v[i]>thr:
                j=i
                while j<len(v) and v[j]>thr: j+=1
                out.append(sum(range(i,j))/ (j-i)); i=j
            else: i+=1
        return out
    return peaks(cols, len(rows)*0.5), peaks(rows, len(cols)*0.5)
for f in sorted(glob.glob("_m_*.jpg")):
    c,r=gridlines(f)
    dc=[round(c[i+1]-c[i],1) for i in range(len(c)-1)]
    dr=[round(r[i+1]-r[i],1) for i in range(len(r)-1)]
    print(f)
    print("   x lines:", [round(x) for x in c], "gaps", dc)
    print("   y lines:", [round(y) for y in r], "gaps", dr)
