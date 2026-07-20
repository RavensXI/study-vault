from PIL import Image
import sys, numpy as np
D=r"C:\Users\tshau\Documents\Study Vault\.claude\worktrees\sandbox\scratchpad\_geo_guided\zz13"
def brownmask(a):
    r=a[...,0].astype(int); g=a[...,1].astype(int); b=a[...,2].astype(int)
    return (r>80)&(r<200)&(g<r-25)&(b<g)&(b<150)
def vscan(f,x,y0,y1,w=1):
    im=Image.open(D+"\\"+f).convert("RGB"); a=np.array(im)
    m=brownmask(a)
    col=m[y0:y1, x-w:x+w+1].any(axis=1)
    runs=[];i=0
    while i<len(col):
        if col[i]:
            j=i
            while j<len(col) and col[j]: j+=1
            runs.append((y0+i, j-i)); i=j
        else: i+=1
    return runs
def hscan(f,y,x0,x1,w=1):
    im=Image.open(D+"\\"+f).convert("RGB"); a=np.array(im)
    m=brownmask(a)
    row=m[y-w:y+w+1, x0:x1].any(axis=0)
    runs=[];i=0
    while i<len(row):
        if row[i]:
            j=i
            while j<len(row) and row[j]: j+=1
            runs.append((x0+i, j-i)); i=j
        else: i+=1
    return runs
if __name__=="__main__":
    pass
